#!/usr/bin/env python3
"""Roda o LibreOffice sem janela, com perfil isolado, pasta temporária e limite de tempo.

Uso na linha de comando:
    python3 soffice_seguro.py --converter-para FORMATO ARQUIVO --saida PASTA [--tempo-limite 120]
    python3 soffice_seguro.py [--tempo-limite 120] -- ARGUMENTOS_DO_SOFFICE...
    python3 soffice_seguro.py --verificar

Exemplos:
    python3 soffice_seguro.py --converter-para pdf deck.pptx --saida render/
    python3 soffice_seguro.py --converter-para docx antigo.doc --saida .
    python3 soffice_seguro.py -- --convert-to xlsx planilha.ods

Uso como módulo:
    from soffice_seguro import converter, ErroSoffice
    pdf = converter("deck.pptx", "pdf", "render/", tempo_limite=120)

Como acha o programa: opção --soffice, depois a variável de ambiente SOFFICE,
depois soffice ou libreoffice no PATH.

O que isola a cada execução:
- perfil novo e descartável (-env:UserInstallation) numa pasta temporária,
  então não briga com um LibreOffice aberto nem herda configuração do usuário;
- HOME, TMPDIR e pastas XDG apontando para a pasta temporária;
- sem tela: --headless, DISPLAY e WAYLAND_DISPLAY removidos, desenho interno
  (SAL_USE_VCLPLUGIN=svp), o que funciona em servidor sem display;
- perfil já semeado com macros desligadas, links externos de documento
  bloqueados e verificação de atualização desligada, para não depender de rede;
- limite de tempo: estourou, o grupo de processos inteiro é morto;
- a pasta temporária é apagada no fim, com sucesso ou não.

Saída da linha de comando: 0 ok (imprime o caminho do arquivo convertido),
2 argumento errado, 3 LibreOffice ou arquivo faltando, 4 o LibreOffice falhou
ou estourou o tempo.
"""

import argparse
import os
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

SAIDA_OK = 0
SAIDA_ARGUMENTO = 2
SAIDA_FALTA = 3
SAIDA_EXTERNO = 4

TEMPO_PADRAO = 120

OPCOES_FIXAS = ["--headless", "--invisible", "--nologo", "--nodefault",
                "--norestore", "--nolockcheck", "--nofirststartwizard"]

REGISTRO = """<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<item oor:path="/org.openoffice.Office.Common/Misc"><prop oor:name="FirstRun" oor:op="fuse"><value>false</value></prop></item>
<item oor:path="/org.openoffice.Office.Common/Security/Scripting"><prop oor:name="MacroSecurityLevel" oor:op="fuse"><value>3</value></prop></item>
<item oor:path="/org.openoffice.Office.Common/Security/Scripting"><prop oor:name="DisableMacrosExecution" oor:op="fuse"><value>true</value></prop></item>
<item oor:path="/org.openoffice.Office.Common/Security/Scripting"><prop oor:name="BlockUntrustedRefererLinks" oor:op="fuse"><value>true</value></prop></item>
<item oor:path="/org.openoffice.Office.Jobs/Jobs/org.openoffice.Office.Jobs:Job['UpdateCheck']/Arguments"><prop oor:name="AutoCheckEnabled" oor:op="fuse"><value>false</value></prop></item>
</oor:items>
"""

DICA_AMBIENTE_RESTRITO = (
    "se o ambiente é uma sandbox que bloqueia soquetes locais ou a criação de "
    "processos, o LibreOffice não consegue abrir o canal interno dele e sai sem "
    "converter: rode este comando fora da sandbox ou num contêiner com o "
    "LibreOffice liberado")


class ErroSoffice(Exception):
    """Falha ao rodar o LibreOffice. `codigo` segue os códigos de saída do script."""

    def __init__(self, mensagem, codigo=SAIDA_EXTERNO, saida=""):
        super().__init__(mensagem)
        self.codigo = codigo
        self.saida = saida


def achar_soffice(indicado=None):
    """Caminho do executável, ou ErroSoffice(código 3)."""
    candidatos = []
    if indicado:
        candidatos.append(indicado)
    if os.environ.get("SOFFICE"):
        candidatos.append(os.environ["SOFFICE"])
    candidatos += ["soffice", "libreoffice"]
    for c in candidatos:
        achado = shutil.which(c)
        if achado:
            return achado
    raise ErroSoffice(
        "não achei o LibreOffice. Instale (Debian e Ubuntu: apt install libreoffice-core "
        "libreoffice-writer libreoffice-calc libreoffice-impress) ou indique o caminho com "
        "--soffice ou com a variável SOFFICE", SAIDA_FALTA)


def _ambiente(temporaria):
    amb = dict(os.environ)
    for chave in ("DISPLAY", "WAYLAND_DISPLAY", "SESSION_MANAGER", "DBUS_SESSION_BUS_ADDRESS"):
        amb.pop(chave, None)
    casa = temporaria / "casa"
    tmp = temporaria / "tmp"
    for p in (casa, tmp, casa / ".config", casa / ".cache", temporaria / "run"):
        p.mkdir(parents=True, exist_ok=True)
    os.chmod(temporaria / "run", 0o700)
    amb.update({
        "HOME": str(casa),
        "TMPDIR": str(tmp),
        "TMP": str(tmp),
        "TEMP": str(tmp),
        "XDG_CONFIG_HOME": str(casa / ".config"),
        "XDG_CACHE_HOME": str(casa / ".cache"),
        "XDG_RUNTIME_DIR": str(temporaria / "run"),
        "SAL_USE_VCLPLUGIN": "svp",
        "SAL_NO_NWFFRAMES": "1",
    })
    return amb


def _perfil(temporaria):
    perfil = temporaria / "perfil"
    usuario = perfil / "user"
    usuario.mkdir(parents=True, exist_ok=True)
    (usuario / "registrymodifications.xcu").write_text(REGISTRO, encoding="utf-8")
    return perfil


def _matar_grupo(proc):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        try:
            proc.kill()
        except OSError:
            pass


def rodar(argumentos, tempo_limite=TEMPO_PADRAO, soffice=None, pasta_trabalho=None):
    """Roda o soffice isolado com os argumentos dados. Devolve (código, saída de texto).

    As opções de modo sem tela e o perfil isolado são acrescentados aqui.
    Levanta ErroSoffice se o programa não existir ou estourar o tempo.
    """
    executavel = achar_soffice(soffice)
    temporaria = Path(tempfile.mkdtemp(prefix="soffice-seguro-"))
    try:
        perfil = _perfil(temporaria)
        comando = [executavel, "-env:UserInstallation=" + perfil.resolve().as_uri()] + OPCOES_FIXAS
        comando += [a for a in argumentos if a not in OPCOES_FIXAS]
        try:
            proc = subprocess.Popen(
                comando, cwd=pasta_trabalho or str(temporaria), env=_ambiente(temporaria),
                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                start_new_session=True)
        except OSError as erro:
            raise ErroSoffice("não consegui iniciar o LibreOffice (%s); %s" % (erro, DICA_AMBIENTE_RESTRITO))
        try:
            saida, _ = proc.communicate(timeout=tempo_limite)
        except subprocess.TimeoutExpired:
            _matar_grupo(proc)
            proc.communicate()
            raise ErroSoffice("o LibreOffice passou de %s segundos e foi encerrado" % tempo_limite)
        _matar_grupo(proc)  # sobra de processo filho, se houver
        return proc.returncode, saida.decode("utf-8", "replace")
    finally:
        shutil.rmtree(temporaria, ignore_errors=True)


def converter(arquivo, formato, saida=None, tempo_limite=TEMPO_PADRAO, soffice=None):
    """Converte `arquivo` para `formato` (ex.: "pdf", "docx", "xlsx", "pdf:writer_pdf_Export").

    Grava em `saida` (padrão: a pasta do arquivo) e devolve o Path do arquivo gerado.
    Levanta ErroSoffice com `codigo` 2, 3 ou 4.
    """
    origem = Path(arquivo).resolve()
    if not origem.is_file():
        raise ErroSoffice("arquivo não encontrado: %s" % arquivo, SAIDA_FALTA)
    if not formato or formato.startswith("-"):
        raise ErroSoffice("formato inválido: %r" % formato, SAIDA_ARGUMENTO)
    destino = Path(saida).resolve() if saida else origem.parent
    destino.mkdir(parents=True, exist_ok=True)
    extensao = formato.split(":", 1)[0].strip().lower()
    esperado = destino / (origem.stem + "." + extensao)
    if esperado == origem:
        raise ErroSoffice("a conversão gravaria por cima do próprio arquivo de entrada; "
                          "escolha outra pasta de saída", SAIDA_ARGUMENTO)
    # Converte a partir de uma cópia numa pasta própria: o LibreOffice não toca
    # no original nem deixa arquivo de trava ao lado dele.
    with tempfile.TemporaryDirectory(prefix="soffice-entrada-") as entrada_tmp:
        copia = Path(entrada_tmp) / origem.name
        shutil.copy2(origem, copia)
        saida_tmp = Path(entrada_tmp) / "saida"
        saida_tmp.mkdir()
        codigo, texto = rodar(["--convert-to", formato, "--outdir", str(saida_tmp), str(copia)],
                              tempo_limite=tempo_limite, soffice=soffice)
        gerado = saida_tmp / esperado.name
        if not gerado.is_file():
            candidatos = sorted(saida_tmp.iterdir())
            if len(candidatos) == 1:
                gerado = candidatos[0]
                esperado = destino / gerado.name
            else:
                detalhe = texto.strip()[-800:] or "sem mensagem do programa"
                dica = "" if texto.strip() else "; " + DICA_AMBIENTE_RESTRITO
                raise ErroSoffice("o LibreOffice não gerou o arquivo (código %s): %s%s"
                                  % (codigo, detalhe, dica), SAIDA_EXTERNO, texto)
        shutil.move(str(gerado), str(esperado))
    return esperado


def versao(soffice=None, tempo_limite=60):
    codigo, texto = rodar(["--version"], tempo_limite=tempo_limite, soffice=soffice)
    if codigo != 0:
        raise ErroSoffice("o LibreOffice respondeu com código %s: %s" % (codigo, texto.strip()))
    return texto.strip()


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    repasse = None
    if "--" in argv:
        i = argv.index("--")
        argv, repasse = argv[:i], argv[i + 1:]
    leitor = argparse.ArgumentParser(
        description="Roda o LibreOffice sem janela, com perfil isolado e limite de tempo.",
        epilog="Argumentos depois de -- vão direto para o soffice.")
    leitor.add_argument("arquivo", nargs="?", help="arquivo a converter")
    leitor.add_argument("--converter-para", metavar="FORMATO", help="formato de destino: pdf, docx, xlsx, pptx, png...")
    leitor.add_argument("--saida", metavar="PASTA", help="pasta de saída (padrão: a pasta do arquivo)")
    leitor.add_argument("--tempo-limite", type=float, default=TEMPO_PADRAO, metavar="SEGUNDOS",
                        help="tempo máximo de execução (padrão %d)" % TEMPO_PADRAO)
    leitor.add_argument("--soffice", metavar="CAMINHO", help="executável do LibreOffice")
    leitor.add_argument("--verificar", action="store_true", help="só mostra a versão do LibreOffice achado")
    args = leitor.parse_args(argv)
    if args.tempo_limite <= 0:
        leitor.error("--tempo-limite precisa ser maior que zero")

    modos = sum([bool(args.converter_para), repasse is not None, args.verificar])
    if modos != 1:
        leitor.error("use um modo: --converter-para FORMATO ARQUIVO, --verificar, ou -- argumentos")
    try:
        if args.verificar:
            print(versao(args.soffice, args.tempo_limite))
            return SAIDA_OK
        if args.converter_para:
            if not args.arquivo:
                leitor.error("--converter-para precisa do ARQUIVO")
            print(converter(args.arquivo, args.converter_para, args.saida, args.tempo_limite, args.soffice))
            return SAIDA_OK
        if args.arquivo:
            leitor.error("no modo de repasse, ponha o arquivo depois de --")
        codigo, texto = rodar(repasse, args.tempo_limite, args.soffice, pasta_trabalho=os.getcwd())
        sys.stdout.write(texto)
        return SAIDA_OK if codigo == 0 else SAIDA_EXTERNO
    except ErroSoffice as erro:
        print(str(erro), file=sys.stderr)
        return erro.codigo


if __name__ == "__main__":
    sys.exit(main())
