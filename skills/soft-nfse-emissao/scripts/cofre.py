#!/usr/bin/env python3
"""
cofre.py - guardas da emissão de NFS-e: pasta de dados, certificado,
palavra-passe, contador do DPS, cadeado de arquivo e registro.

Regras que nada aqui dobra:
- dado fiscal do dono mora em NFSE_DADOS_DIR, sempre fora da pasta da skill;
- a senha do certificado chega só por NFSE_PFX_PASSWORD e nunca é impressa,
  gravada em arquivo ou repassada como argumento;
- a chave privada só toca o disco em arquivo temporario 0600, cifrado com uma
  senha de uso único, e é apagada logo depois de carregada.
"""
import contextlib
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import stat
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ITERACOES_PP = 600_000
DIAS_AVISO_CERTIFICADO = 30
MARCAS_NUVEM = ("dropbox", "onedrive", "google drive", "googledrive", "icloud",
                "mega", "pcloud", "nextcloud", "syncthing")
STATUS_PENDENTE = ("enviando", "incerta")


class Recusa(Exception):
    """Guarda que mandou parar. A mensagem vai literal ao dono."""


def aviso(msg):
    print(f"AVISO: {msg}", file=sys.stderr)


# ------------------------------------------------------------------ tempo

def fuso():
    nome = os.environ.get("NFSE_FUSO", "America/Sao_Paulo").strip() or "America/Sao_Paulo"
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(nome)
    except Exception:
        return dt.timezone(dt.timedelta(hours=-3))


def agora():
    return dt.datetime.now(fuso()).replace(microsecond=0)


def agora_iso():
    return agora().isoformat()


# ------------------------------------------------------------------ pastas

def dentro_da_skill(caminho):
    p = Path(caminho).expanduser().resolve()
    return p == SKILL_DIR or SKILL_DIR in p.parents


def exigir_fora_da_skill(caminho, rotulo):
    p = Path(caminho).expanduser().resolve()
    if p == SKILL_DIR or SKILL_DIR in p.parents:
        raise Recusa(f"{rotulo} aponta pra dentro da pasta da skill ({p}). A pasta da skill "
                     "é código compartilhado; dado fiscal do dono mora fora dela.")
    return p


def dados_dir(criar=True):
    """Pasta de dados do dono. Recusa sem NFSE_DADOS_DIR e recusa caminho na skill.
    A checagem vem ANTES de qualquer mkdir: pasta recusada nunca é criada."""
    valor = os.environ.get("NFSE_DADOS_DIR", "").strip()
    if not valor:
        raise Recusa("NFSE_DADOS_DIR não está definida. Os scripts não rodam sem a pasta de "
                     "dados do dono (fichas, contador, XML e PDF). Exemplo: "
                     "export NFSE_DADOS_DIR=\"$HOME/nfse-dados\"")
    p = exigir_fora_da_skill(valor, "NFSE_DADOS_DIR")
    if any(m in str(p).lower() for m in MARCAS_NUVEM):
        aviso("a pasta de dados parece sincronizada com nuvem. XML fiscal e registro ficam "
              "melhor numa pasta local só do usuário do agente.")
    if criar:
        p.mkdir(parents=True, exist_ok=True, mode=0o700)
        with contextlib.suppress(OSError):
            os.chmod(p, 0o700)
    elif not p.is_dir():
        raise Recusa(f"a pasta de dados {p} não existe. Rode primeiro: python3 scripts/nfse.py iniciar")
    return p


def escrever_privado(caminho, conteudo, sobrescrever=True):
    """Grava com permissão 0600, de forma atômica, sempre fora da pasta da skill."""
    caminho = exigir_fora_da_skill(caminho, "destino de gravação")
    if caminho.exists() and not sobrescrever:
        raise Recusa(f"{caminho} já existe e não se sobrescreve (XML fiscal nunca se apaga).")
    caminho.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if isinstance(conteudo, str):
        conteudo = conteudo.encode("utf-8")
    tmp = caminho.with_name(f".{caminho.name}.{secrets.token_hex(4)}.parcial")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(conteudo)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, caminho)
    finally:
        if tmp.exists():
            tmp.unlink()
    return caminho


def gravar_json(caminho, obj, sobrescrever=True):
    texto = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    return escrever_privado(caminho, texto, sobrescrever=sobrescrever)


def ler_json(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


@contextlib.contextmanager
def cadeado(dados):
    """Cadeado exclusivo de arquivo: duas emissões nunca pegam o mesmo número."""
    caminho = Path(dados) / ".cadeado"
    fd = os.open(caminho, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        try:
            import fcntl
        except ImportError:
            fcntl = None
        if fcntl is not None:
            fcntl.flock(fd, fcntl.LOCK_EX)
        else:
            import msvcrt
            msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(fd, fcntl.LOCK_UN)
            else:
                os.lseek(fd, 0, os.SEEK_SET)
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    finally:
        os.close(fd)


# ------------------------------------------------------------------ contador

def _chave_contador(amb, serie):
    return f"{amb}:serie-{int(serie)}"


def contador_ultimo(dados, amb, serie):
    arq = Path(dados) / "contador-dps.json"
    if not arq.exists():
        return 0
    return int(ler_json(arq).get(_chave_contador(amb, serie), {}).get("ultimo", 0))


def contador_avancar(dados, amb, serie, numero):
    """Só sobe. Chamar com o cadeado na mão."""
    arq = Path(dados) / "contador-dps.json"
    d = ler_json(arq) if arq.exists() else {}
    k = _chave_contador(amb, serie)
    atual = int(d.get(k, {}).get("ultimo", 0))
    if int(numero) > atual:
        d[k] = {"ultimo": int(numero), "atualizado_em": agora_iso()}
        gravar_json(arq, d)
    return max(atual, int(numero))


# ------------------------------------------------------------------ registro

def registrar(dados, acao, **campos):
    """Linha de auditoria. Quem chama nunca passa segredo."""
    linha = {"quando": agora_iso(), "acao": acao}
    linha.update(campos)
    arq = Path(dados) / "registro.jsonl"
    fd = os.open(arq, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")


def pendencias(dados):
    """Envios sem desfecho conhecido (incerta ou enviando). Bloqueiam nova emissão."""
    out = []
    base = Path(dados) / "notas"
    if not base.is_dir():
        return out
    for arq in sorted(base.glob("*/*/*/estado.json")):
        try:
            e = ler_json(arq)
        except Exception:
            continue
        if e.get("status") in STATUS_PENDENTE:
            out.append((arq.parent, e))
    return out


# ------------------------------------------------------------------ palavra-passe

def _arquivo_pp(dados):
    return Path(dados) / "palavra-passe.json"


def palavra_passe_definida(dados):
    return _arquivo_pp(dados).exists()


def _derivar(palavra, sal, iteracoes):
    return hashlib.pbkdf2_hmac("sha256", palavra.encode("utf-8"), sal, iteracoes)


def conferir_palavra_passe(dados, palavra):
    d = ler_json(_arquivo_pp(dados))
    calc = _derivar(palavra, bytes.fromhex(d["sal"]), int(d["iteracoes"]))
    return hmac.compare_digest(calc.hex(), d["hash"])


def definir_palavra_passe(dados, nova, atual=None):
    if len(nova) < 6:
        raise Recusa("a palavra-passe precisa de pelo menos 6 caracteres.")
    if palavra_passe_definida(dados):
        if atual is None or not conferir_palavra_passe(dados, atual):
            raise Recusa("já existe palavra-passe e a atual não conferiu. Nada mudou.")
    senha_pfx = os.environ.get("NFSE_PFX_PASSWORD")
    if senha_pfx and hmac.compare_digest(nova.encode("utf-8"), senha_pfx.encode("utf-8")):
        raise Recusa("a palavra-passe não pode ser igual à senha do certificado.")
    sal = secrets.token_bytes(16)
    gravar_json(_arquivo_pp(dados), {
        "algoritmo": "pbkdf2-sha256",
        "iteracoes": ITERACOES_PP,
        "sal": sal.hex(),
        "hash": _derivar(nova, sal, ITERACOES_PP).hex(),
        "definida_em": agora_iso(),
    })


def ler_segredo(rotulo):
    """Lê da entrada padrão (uma linha) ou do terminal sem eco. Nunca de argumento."""
    if sys.stdin is not None and sys.stdin.isatty():
        import getpass
        return getpass.getpass(f"{rotulo}: ")
    linha = sys.stdin.readline() if sys.stdin is not None else ""
    return linha.rstrip("\r\n")


# ------------------------------------------------------------------ certificado

def carregar_certificado():
    """Abre o .pfx de NFSE_PFX_PATH com a senha de NFSE_PFX_PASSWORD."""
    caminho = os.environ.get("NFSE_PFX_PATH", "").strip()
    if not caminho:
        raise Recusa("NFSE_PFX_PATH não está definida. Aponte o arquivo .pfx do e-CNPJ A1, "
                     "guardado fora da pasta da skill.")
    p = exigir_fora_da_skill(caminho, "NFSE_PFX_PATH")
    if not p.is_file():
        raise Recusa(f"não achei o certificado em {p}.")
    modo = stat.S_IMODE(p.stat().st_mode)
    if os.name == "posix" and modo & 0o077:
        raise Recusa(f"o certificado está com permissão {oct(modo)} e outros usuários conseguem "
                     f"ler. Rode: chmod 600 \"{p}\"")
    senha = os.environ.get("NFSE_PFX_PASSWORD")
    if not senha:
        raise Recusa("NFSE_PFX_PASSWORD não está definida. A senha do certificado entra só por "
                     "variável de ambiente ou cofre de segredos, nunca na conversa nem em argumento.")
    from cryptography.hazmat.primitives.serialization import pkcs12
    try:
        chave, cert, extras = pkcs12.load_key_and_certificates(p.read_bytes(), senha.encode("utf-8"))
    except Exception:
        raise Recusa("não consegui abrir o certificado: senha errada ou .pfx corrompido.") from None
    if chave is None or cert is None:
        raise Recusa("o .pfx não traz chave privada e certificado juntos.")
    return chave, cert, list(extras or [])


def _validade(cert):
    fim = getattr(cert, "not_valid_after_utc", None)
    ini = getattr(cert, "not_valid_before_utc", None)
    if fim is None:
        fim = cert.not_valid_after.replace(tzinfo=dt.timezone.utc)
        ini = cert.not_valid_before.replace(tzinfo=dt.timezone.utc)
    return ini, fim


def conferir_validade(cert):
    """Recusa certificado vencido; avisa quando faltam 30 dias ou menos."""
    ini, fim = _validade(cert)
    agora_utc = dt.datetime.now(dt.timezone.utc)
    if agora_utc < ini:
        raise Recusa(f"o certificado só passa a valer em {ini:%d/%m/%Y}.")
    if agora_utc >= fim:
        raise Recusa(f"o certificado venceu em {fim:%d/%m/%Y}. Sem certificado válido nada é "
                     "emitido; renove o e-CNPJ A1.")
    dias = (fim - agora_utc).days
    if dias <= DIAS_AVISO_CERTIFICADO:
        aviso(f"o certificado vence em {dias} dia(s), em {fim:%d/%m/%Y}. Renove antes disso.")
    return dias, fim


def _texto_der(valor):
    """Desembrulha TLV DER simples ([0] explícito e string) e devolve o texto."""
    for _ in range(3):
        if len(valor) < 2:
            break
        tag, tam = valor[0], valor[1]
        ini = 2
        if tam & 0x80:
            n = tam & 0x7F
            tam = int.from_bytes(valor[2:2 + n], "big")
            ini = 2 + n
        conteudo = valor[ini:ini + tam]
        if tag in (0xA0, 0x30):
            valor = conteudo
            continue
        return conteudo.decode("latin-1", "replace")
    return valor.decode("latin-1", "replace")


def cnpj_do_certificado(cert):
    """CNPJ gravado no e-CNPJ (outro nome 2.16.76.1.3.3 ou fim do CN). None se não achar."""
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    try:
        san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        for nome in san.get_values_for_type(x509.OtherName):
            if nome.type_id.dotted_string == "2.16.76.1.3.3":
                txt = re.sub(r"[^0-9A-Z]", "", _texto_der(nome.value).upper())
                if len(txt) >= 14:
                    return txt[-14:]
    except x509.ExtensionNotFound:
        pass
    for at in cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME):
        m = re.search(r":([0-9A-Z]{14})\s*$", str(at.value))
        if m:
            return m.group(1)
    return None


def _gravar_0600(caminho, dados):
    fd = os.open(caminho, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(dados)
        f.flush()
        os.fsync(f.fileno())


@contextlib.contextmanager
def arquivos_tls_temporarios(chave, cert, extras):
    """Chave e certificado em PEM numa pasta 0700, arquivos 0600, chave cifrada com
    senha de uso único. Tudo apagado na saida do bloco, logo depois do carregamento."""
    from cryptography.hazmat.primitives import serialization as s
    pasta = Path(tempfile.mkdtemp(prefix="nfse-tls-"))
    senha_unica = secrets.token_urlsafe(32)
    arq_cert = pasta / "certificado.pem"
    arq_chave = pasta / "chave.pem"
    try:
        cadeia = cert.public_bytes(s.Encoding.PEM) + b"".join(
            e.public_bytes(s.Encoding.PEM) for e in extras)
        _gravar_0600(arq_cert, cadeia)
        _gravar_0600(arq_chave, chave.private_bytes(
            s.Encoding.PEM, s.PrivateFormat.PKCS8,
            s.BestAvailableEncryption(senha_unica.encode("ascii"))))
        yield str(arq_cert), str(arq_chave), senha_unica
    finally:
        for a in (arq_chave, arq_cert):
            with contextlib.suppress(OSError):
                if a.exists():
                    tam = a.stat().st_size
                    with open(a, "r+b") as f:
                        f.write(b"\0" * tam)
                        f.flush()
                        os.fsync(f.fileno())
                    a.unlink()
        shutil.rmtree(pasta, ignore_errors=True)
