#!/usr/bin/env python3
"""Recompacta uma pasta desempacotada em .docx, .pptx ou .xlsx e confere o resultado.

Uso:
    python3 empacotar.py PASTA SAIDA.(docx|pptx|xlsx) [--original ARQUIVO] [--autor NOME] [--manter-recuo]

O que faz:
- grava [Content_Types].xml como primeira entrada do zip, depois _rels/.rels,
  depois o resto em ordem alfabética (se houver um arquivo mimetype, de pacote
  ODF, ele vai antes de tudo e sem compressão);
- tira o recuo do XML só onde o espaço não tem sentido: texto de folha
  (w:t, a:t e afins), xml:space="preserve" e conteúdo misto ficam intactos;
- avisa quando um texto de folha parece ter recebido recuo por engano
  (quebra de linha seguida de espaços dentro de w:t ou a:t);
- ignora links simbólicos e lixo de sistema (.DS_Store, Thumbs.db, cópias de
  editor), avisando;
- grava num arquivo temporário e troca no fim, então nada do arquivo antigo
  sobra dentro do novo;
- roda conferir.py no resultado (com --original e --autor, se dados) e sai 1
  se reprovar. O arquivo fica gravado mesmo reprovado, para você inspecionar.

Saída: 0 aprovado, 1 reprovado, 2 argumento errado, 3 arquivo ou dependência
faltando.
"""

import argparse
import os
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import comum  # noqa: E402
import conferir  # noqa: E402

LIXO_NOMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
LIXO_PASTAS = {"__MACOSX"}
DATA_FIXA = (1980, 1, 1, 0, 0, 0)
FOLHAS_DE_TEXTO = {"t", "delText", "instrText", "delInstrText"}


def eh_lixo(nome_relativo):
    partes = nome_relativo.split("/")
    base = partes[-1]
    if any(p in LIXO_PASTAS for p in partes[:-1]):
        return True
    return (base in LIXO_NOMES or base.endswith("~") or base.endswith(".swp")
            or base.startswith(".~lock."))


def ordem(nome):
    if nome == "mimetype":
        return (0, nome)
    if nome == "[Content_Types].xml":
        return (1, nome)
    if nome == "_rels/.rels":
        return (2, nome)
    return (3, nome)


def recuo_suspeito(raiz):
    """Lista nomes de folhas de texto com quebra de linha seguida de recuo."""
    achados = []
    for e in raiz.iter():
        if not isinstance(e.tag, str) or len(e):
            continue
        if comum.etree.QName(e).localname in FOLHAS_DE_TEXTO and e.text and "\n " in e.text:
            achados.append(e.text.strip()[:40])
    return achados


def listar(pasta):
    """Devolve (arquivos relativos, ignorados com motivo)."""
    arquivos, ignorados = [], []
    for raiz, pastas, nomes in os.walk(pasta, followlinks=False):
        for p in list(pastas):
            if os.path.islink(os.path.join(raiz, p)):
                ignorados.append((os.path.relpath(os.path.join(raiz, p), pasta), "link simbólico"))
                pastas.remove(p)
        pastas.sort()
        for n in sorted(nomes):
            completo = os.path.join(raiz, n)
            rel = os.path.relpath(completo, pasta).replace(os.sep, "/")
            if os.path.islink(completo):
                ignorados.append((rel, "link simbólico"))
            elif not os.path.isfile(completo):
                ignorados.append((rel, "não é arquivo comum"))
            elif eh_lixo(rel):
                ignorados.append((rel, "lixo de sistema ou de editor"))
            else:
                arquivos.append(rel)
    arquivos.sort(key=ordem)
    return arquivos, ignorados


def empacotar(pasta, saida, manter_recuo=False):
    """Grava o zip. Devolve (arquivos gravados, avisos)."""
    comum.exigir_lxml()
    arquivos, ignorados = listar(pasta)
    avisos = ["ignorado %s (%s)" % (n, m) for n, m in ignorados]
    if "[Content_Types].xml" not in arquivos:
        avisos.append("a pasta não tem [Content_Types].xml na raiz")
    destino_pasta = os.path.dirname(os.path.abspath(saida)) or "."
    fd, temporario = tempfile.mkstemp(prefix=".empacotando-", suffix=".zip", dir=destino_pasta)
    os.close(fd)
    try:
        with zipfile.ZipFile(temporario, "w", zipfile.ZIP_DEFLATED) as zf:
            for rel in arquivos:
                with open(os.path.join(pasta, *rel.split("/")), "rb") as f:
                    dados = f.read()
                if comum.eh_arquivo_xml(rel) and not manter_recuo:
                    try:
                        arvore = comum.ler_xml(dados)
                        for trecho in recuo_suspeito(arvore.getroot()):
                            avisos.append("%s: texto com quebra de linha e recuo, provável recuo por engano: %r"
                                          % (rel, trecho))
                        comum.tirar_recuo(arvore.getroot())
                        dados = comum.gravar_xml(arvore, dados)
                    except comum.etree.XMLSyntaxError:
                        pass  # a conferência acusa
                info = zipfile.ZipInfo(rel, date_time=DATA_FIXA)
                info.external_attr = 0o644 << 16
                if rel == "mimetype":
                    info.compress_type = zipfile.ZIP_STORED
                else:
                    info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, dados)
        mascara = os.umask(0)
        os.umask(mascara)
        os.chmod(temporario, 0o666 & ~mascara)
        os.replace(temporario, saida)
    except BaseException:
        if os.path.exists(temporario):
            os.remove(temporario)
        raise
    return arquivos, avisos


def main(argv=None):
    leitor = argparse.ArgumentParser(
        description="Recompacta uma pasta em docx, pptx ou xlsx e confere o resultado.")
    leitor.add_argument("pasta", help="pasta desempacotada")
    leitor.add_argument("saida", help="arquivo a gravar (.docx, .pptx, .xlsx)")
    leitor.add_argument("--original", help="arquivo de origem para comparar")
    leitor.add_argument("--autor", help="autor das alterações rastreadas (só Word), repassado à conferência")
    leitor.add_argument("--manter-recuo", action="store_true", help="grava o XML como está, sem tirar o recuo")
    args = leitor.parse_args(argv)

    if not os.path.isdir(args.pasta):
        print("pasta não encontrada: %s" % args.pasta, file=sys.stderr)
        return comum.SAIDA_FALTA
    if args.original and not os.path.isfile(args.original):
        print("original não encontrado: %s" % args.original, file=sys.stderr)
        return comum.SAIDA_FALTA
    pasta_real = os.path.realpath(args.pasta)
    saida_real = os.path.realpath(args.saida)
    if os.path.commonpath([pasta_real, saida_real]) == pasta_real:
        print("a saída não pode ficar dentro da pasta que está sendo empacotada", file=sys.stderr)
        return comum.SAIDA_ARGUMENTO
    if os.path.isdir(args.saida):
        print("a saída é uma pasta, informe o nome do arquivo: %s" % args.saida, file=sys.stderr)
        return comum.SAIDA_ARGUMENTO
    if not os.path.isdir(os.path.dirname(saida_real)):
        print("a pasta da saída não existe: %s" % os.path.dirname(saida_real), file=sys.stderr)
        return comum.SAIDA_FALTA

    arquivos, avisos = empacotar(args.pasta, args.saida, args.manter_recuo)
    for aviso in avisos:
        print("aviso: %s" % aviso)
    print("gravado %s com %d partes" % (args.saida, len(arquivos)))
    rel = conferir.conferir(args.saida, args.original, args.autor)
    print(rel.texto())
    if rel.reprovou:
        print("o arquivo foi gravado, mas reprovou na conferência: corrija antes de entregar")
        return comum.SAIDA_REPROVOU
    return comum.SAIDA_OK


if __name__ == "__main__":
    sys.exit(main())
