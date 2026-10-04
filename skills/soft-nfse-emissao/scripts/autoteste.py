#!/usr/bin/env python3
"""
autoteste.py - prova offline da skill de NFS-e. Nenhum servidor do governo é chamado.

P1  DPS fictício nas versões 1.00 e 1.01: Id de 45 caracteres e composição,
    namespace em todos os níveis, nenhum prefixo. Assinatura com certificado
    AUTOASSINADO de teste (sha256 e sha1) conferida por caminho independente do
    código que assinou: C14N da biblioteca padrão (expat, sem lxml) mais RSA da
    cryptography, openssl e libxmlsec1 quando existirem. Adulterar um valor tem
    que derrubar a conferência.
P2  lição do namespace: leitor da skill x leitor ingênuo num XML autorizado fictício.
P3  PDF a partir do XML fictício: texto conferido (pdftotext) e QR lido (opencv)
    quando houver leitor.
P4  guardas do nfse.py, com a mensagem literal de cada recusa; senha e
    palavra-passe fora de toda saída e arquivo; nenhum temporário de chave sobrando.
P5  envio contra servidor LOCAL de mentira com TLS mútuo em 127.0.0.1: autorizada,
    rejeitada, incerta que virou nota, incerta sem nota, eventos com cancelamento.

Uso: python3 scripts/autoteste.py [--trabalho PASTA] [--manter]
A pasta de trabalho recebe o certificado de teste e é apagada no fim, salvo --manter.
Saída 0 quando tudo passou (itens pulados por falta de ferramenta aparecem como PULADO).
"""
import argparse
import base64
import contextlib
import datetime as dt
import gzip
import hashlib
import http.server
import ipaddress
import json
import os
import re
import secrets
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import xml.etree.ElementTree as ET
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SKILL_DIR = AQUI.parent
sys.path.insert(0, str(AQUI))

from cryptography import x509  # noqa: E402
from cryptography.exceptions import InvalidSignature  # noqa: E402
from cryptography.hazmat.primitives import hashes, serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import padding, rsa  # noqa: E402
from cryptography.hazmat.primitives.serialization import pkcs12  # noqa: E402
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID  # noqa: E402
from lxml import etree  # noqa: E402

import assinatura  # noqa: E402
import cliente_sefin  # noqa: E402
import cofre  # noqa: E402
import dps  # noqa: E402

NS = dps.NS
DSN = "http://www.w3.org/2000/09/xmldsig#"
CNPJ_PRESTADOR = "11222333000181"   # FICTÍCIO, número de exemplo didático
CNPJ_TOMADOR = "99888777000100"     # FICTÍCIO
SENHA_PFX = "senha-teste-" + secrets.token_hex(6)
PALAVRA = "palavra-teste-" + secrets.token_hex(4)
EMPRESA = {
    "_leia": "FICHA FICTÍCIA DE TESTE",
    "razao_social": "EMPRESA FICTICIA PRESTADORA LTDA", "cnpj": CNPJ_PRESTADOR,
    "inscricao_municipal": "12345", "municipio_ibge": "9999999",
    "simples_nacional": {"opSimpNac": 3, "regApTribSN": 1}, "regEspTrib": 0,
    "serie_dps": "1",
    "tributos_aproximados": {"pTotTribFed": "4.50", "pTotTribEst": "0.00", "pTotTribMun": "2.00"},
    "exigir_palavra_passe": True,
}
CLIENTE = {
    "_leia": "FICHA FICTÍCIA DE TESTE",
    "nome": "CLIENTE FICTICIO TOMADOR LTDA",
    "documento": {"tipo": "CNPJ", "numero": CNPJ_TOMADOR},
    "endereco": {"cep": "99999999", "municipio_ibge": "9999999", "logradouro": "Rua Ficticia",
                 "numero": "100", "complemento": "", "bairro": "Bairro Ficticio"},
    "servico": {"cTribNac": "010101", "cLocPrestacao": "9999999",
                "descricao_base": "Servico ficticio de teste"},
    "iss": {"tribISSQN": 1, "tpRetISSQN": 1},
}
NOTA = {"valor": "700", "competencia": "2026-09", "descricao": "referente a setembro"}

RESULTADOS = []
SAIDAS = []


def marca(nome, cond, detalhe="", pulado=False):
    rotulo = "PULADO" if pulado else ("OK    " if cond else "FALHOU")
    RESULTADOS.append((nome, "pulado" if pulado else bool(cond)))
    print(f"{rotulo} {nome}" + (f" | {detalhe}" if detalhe else ""))
    return cond


# ------------------------------------------------------------------ certificados

def _nome(cn):
    return x509.Name([x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
                      x509.NameAttribute(NameOID.ORGANIZATION_NAME, "TESTE AUTOASSINADO SEM VALOR"),
                      x509.NameAttribute(NameOID.COMMON_NAME, cn)])


def certificado_autoassinado(cn, dias, cliente=True, san=None):
    chave = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    agora = dt.datetime.now(dt.timezone.utc)
    pub = chave.public_key()
    b = (x509.CertificateBuilder().subject_name(_nome(cn)).issuer_name(_nome(cn))
         .public_key(pub).serial_number(x509.random_serial_number())
         .not_valid_before(agora - dt.timedelta(minutes=5))
         .not_valid_after(agora + dt.timedelta(days=dias))
         .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
         .add_extension(x509.KeyUsage(digital_signature=True, content_commitment=cliente,
                                      key_encipherment=True, data_encipherment=False,
                                      key_agreement=False, key_cert_sign=False, crl_sign=False,
                                      encipher_only=False, decipher_only=False), critical=True)
         .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CLIENT_AUTH if cliente
                                               else ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
         .add_extension(x509.SubjectKeyIdentifier.from_public_key(pub), critical=False)
         .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(pub), critical=False))
    if san:
        b = b.add_extension(x509.SubjectAlternativeName(san), critical=False)
    return chave, b.sign(chave, hashes.SHA256())


def gravar_0600(caminho, dados):
    fd = os.open(caminho, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(dados)


# ------------------------------------------------------------------ conferência independente

def _c14n_stdlib(texto_doc, tag, ns):
    """C14N do elemento <tag> pelo ElementTree (expat), sem lxml. Serve aos documentos
    da skill: só namespace padrão, sem prefixo, sem comentário dentro do elemento."""
    can = ET.canonicalize(xml_data=texto_doc, with_comments=False)
    m = re.search(rf"<{tag}(\s[^>]*)?>.*?</{tag}>", can, re.S)
    if not m:
        return None
    return m.group(0).replace(f"<{tag}", f'<{tag} xmlns="{ns}"', 1).encode("utf-8")


DIGESTS = {"http://www.w3.org/2001/04/xmlenc#sha256": "sha256",
           "http://www.w3.org/2000/09/xmldsig#sha1": "sha1"}
ASSINATURAS = {"http://www.w3.org/2001/04/xmldsig-more#rsa-sha256": hashes.SHA256,
               "http://www.w3.org/2000/09/xmldsig#rsa-sha1": hashes.SHA1}


def verificar_independente(xml_assinado, cert_der_esperado):
    """Confere a assinatura sem tocar em assinatura.py nem na C14N do lxml."""
    erros = []
    texto = xml_assinado.decode("utf-8")
    raiz = ET.fromstring(texto)
    sig = raiz.find(f"{{{DSN}}}Signature")
    if sig is None:
        return ["Signature não é filho direto de DPS"], None, None, None
    si = sig.find(f"{{{DSN}}}SignedInfo")
    cm = si.find(f"{{{DSN}}}CanonicalizationMethod").get("Algorithm")
    sm = si.find(f"{{{DSN}}}SignatureMethod").get("Algorithm")
    ref = si.find(f"{{{DSN}}}Reference")
    trs = [t.get("Algorithm") for t in ref.find(f"{{{DSN}}}Transforms")]
    dm = ref.find(f"{{{DSN}}}DigestMethod").get("Algorithm")
    dv = ref.find(f"{{{DSN}}}DigestValue").text.strip()
    if cm != "http://www.w3.org/TR/2001/REC-xml-c14n-20010315":
        erros.append(f"canonicalização inesperada: {cm}")
    if trs != [DSN + "enveloped-signature", "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"]:
        erros.append(f"transformações inesperadas: {trs}")
    alvo = raiz.find(f"{{{NS}}}infDPS")
    if ref.get("URI") != "#" + (alvo.get("Id") if alvo is not None else ""):
        erros.append(f"Reference {ref.get('URI')} não aponta o Id do infDPS")
    c14n_alvo = _c14n_stdlib(texto, "infDPS", NS)
    if hashlib.new(DIGESTS[dm], c14n_alvo).digest() != base64.b64decode(dv):
        erros.append("digest não confere com o infDPS")
    der = base64.b64decode(sig.find(f".//{{{DSN}}}X509Certificate").text)
    if der != cert_der_esperado:
        erros.append("certificado do X509Data difere do certificado de teste")
    cert = x509.load_der_x509_certificate(der)
    si_c14n = _c14n_stdlib(texto, "SignedInfo", DSN)
    valor = base64.b64decode(sig.find(f"{{{DSN}}}SignatureValue").text)
    try:
        cert.public_key().verify(valor, si_c14n, padding.PKCS1v15(), ASSINATURAS[sm]())
    except InvalidSignature:
        erros.append("RSA da SignatureValue não confere")
    return erros, si_c14n, valor, DIGESTS[dm]


def verificar_openssl(si_c14n, valor, cert, alg, pasta):
    if not shutil.which("openssl"):
        return None, "openssl ausente"
    (pasta / "si.c14n").write_bytes(si_c14n)
    (pasta / "sig.bin").write_bytes(valor)
    (pasta / "pub.pem").write_bytes(cert.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
    r = subprocess.run(["openssl", "dgst", f"-{alg}", "-verify", str(pasta / "pub.pem"),
                        "-signature", str(pasta / "sig.bin"), str(pasta / "si.c14n")],
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def verificar_xmlsec(xml_assinado, cert_pem):
    try:
        import xmlsec
    except ImportError:
        return None, "módulo xmlsec ausente"
    doc = etree.fromstring(xml_assinado)
    xmlsec.tree.add_ids(doc, ["Id"])
    no = xmlsec.tree.find_node(doc, xmlsec.constants.NodeSignature)
    ctx = xmlsec.SignatureContext()
    ctx.key = xmlsec.Key.from_memory(cert_pem, xmlsec.constants.KeyDataFormatCertPem, None)
    try:
        ctx.verify(no)
        return True, "libxmlsec1 confere"
    except xmlsec.Error as e:
        return False, f"libxmlsec1 recusou: {e}"


def verificar_xmlsec1(xml_assinado, cert_pem, pasta):
    if not shutil.which("xmlsec1"):
        return None, "xmlsec1 ausente"
    (pasta / "assinado.xml").write_bytes(xml_assinado)
    (pasta / "cert.pem").write_bytes(cert_pem)
    r = subprocess.run(["xmlsec1", "--verify", "--id-attr:Id", f"{NS}:infDPS",
                        "--pubkey-cert-pem", str(pasta / "cert.pem"), str(pasta / "assinado.xml")],
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1:]


# ------------------------------------------------------------------ XML fictícios

def chave_ficticia(n):
    return f"9999999" + "2" + "2" + CNPJ_PRESTADOR + str(n).zfill(13) + "2610" + "000000001" + "0"


def nfse_ficticia(dps_assinado, numero, chave):
    """NFS-e autorizada FICTÍCIA e simplificada, namespace em todos os níveis."""
    d = etree.fromstring(dps_assinado)
    raiz = etree.Element(f"{{{NS}}}NFSe", nsmap={None: NS})
    raiz.set("versao", "1.00")
    raiz.append(etree.Comment(" XML FICTICIO DE TESTE, estrutura simplificada, sem valor "))
    inf = etree.SubElement(raiz, f"{{{NS}}}infNFSe")
    inf.set("Id", "NFS" + chave)
    for nome, valor in [("xLocEmi", "Cidade Ficticia"), ("xLocPrestacao", "Cidade Ficticia"),
                        ("nNFSe", str(numero)), ("xTribNac", "Servico ficticio de teste"),
                        ("verAplic", "TESTE"), ("ambGer", "2"), ("tpEmis", "1"), ("cStat", "100"),
                        ("dhProc", "2026-10-01T10:00:00-03:00"), ("nDFSe", str(numero))]:
        etree.SubElement(inf, f"{{{NS}}}{nome}").text = valor
    emit = etree.SubElement(inf, f"{{{NS}}}emit")
    etree.SubElement(emit, f"{{{NS}}}CNPJ").text = CNPJ_PRESTADOR
    etree.SubElement(emit, f"{{{NS}}}IM").text = "12345"
    etree.SubElement(emit, f"{{{NS}}}xNome").text = "EMPRESA FICTICIA PRESTADORA LTDA"
    val = etree.SubElement(inf, f"{{{NS}}}valores")
    vserv = d.findtext(f".//{{{NS}}}vServ")
    etree.SubElement(val, f"{{{NS}}}vLiq").text = vserv
    inf.append(d)
    return etree.tostring(raiz, xml_declaration=True, encoding="UTF-8")


def evento_cancelamento_ficticio(chave):
    return (f'<?xml version="1.0" encoding="UTF-8"?><evento xmlns="{NS}" versao="1.00">'
            f'<!-- EVENTO FICTICIO DE TESTE --><infEvento Id="EVT{chave}"><pedRegEvento '
            f'versao="1.00"><infPedReg Id="PRE{chave}101101001"><chNFSe>{chave}</chNFSe>'
            f'<e101101><xDesc>Cancelamento de NFS-e</xDesc><cMotivo>1</cMotivo>'
            f'<xMotivo>Teste ficticio</xMotivo></e101101></infPedReg></pedRegEvento>'
            f'</infEvento></evento>').encode("utf-8")


def gzb64(b):
    return base64.b64encode(gzip.compress(b)).decode("ascii")


# ------------------------------------------------------------------ servidor de mentira

class ServidorFalso:
    """HTTPS em 127.0.0.1 com TLS mútuo. Imita o pedaço da API que a skill usa."""

    def __init__(self, pasta, cert_cliente):
        chave, cert = certificado_autoassinado(
            "servidor local de teste", 2, cliente=False,
            san=[x509.DNSName("localhost"),
                 x509.IPAddress(ipaddress.ip_address("127.0.0.1"))])
        self.ca = pasta / "servidor.pem"
        gravar_0600(self.ca, cert.public_bytes(serialization.Encoding.PEM))
        arq_chave = pasta / "servidor-chave.pem"
        gravar_0600(arq_chave, chave.private_bytes(serialization.Encoding.PEM,
                                                   serialization.PrivateFormat.PKCS8,
                                                   serialization.NoEncryption()))
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(str(self.ca), str(arq_chave))
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.verify_flags |= ssl.VERIFY_X509_PARTIAL_CHAIN
        ctx.load_verify_locations(cadata=cert_cliente.public_bytes(serialization.Encoding.PEM).decode())
        self.modo = "ok"
        self.notas = {}
        self.canceladas = set()
        self.pedidos = []
        self.numero = 0
        srv = self

        class Tratador(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _json(self, status, obj):
                corpo = json.dumps(obj).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                self.wfile.write(corpo)

            def do_POST(self):
                corpo = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                srv.pedidos.append(("POST", self.path))
                xml = gzip.decompress(base64.b64decode(corpo["dpsXmlGZipB64"]))
                id_dps = re.search(rb'Id="(DPS[0-9A-Z]{42})"', xml).group(1).decode()
                if srv.modo == "rejeita":
                    return self._json(400, {"erros": [{"Codigo": "E9999", "Descricao":
                                                       "Rejeicao ficticia do servidor de teste"}]})
                if srv.modo in ("ok", "cai_depois"):
                    srv.numero += 1
                    chave = chave_ficticia(srv.numero)
                    srv.notas[id_dps] = (chave, nfse_ficticia(xml, srv.numero, chave))
                if srv.modo in ("cai_depois", "cai_antes"):
                    self.close_connection = True
                    self.connection.close()
                    return
                chave, nfse = srv.notas[id_dps]
                return self._json(201, {"tipoAmbiente": 2, "idDps": id_dps, "chaveAcesso": chave,
                                        "nfseXmlGZipB64": gzb64(nfse)})

            def do_GET(self):
                srv.pedidos.append(("GET", self.path))
                m = re.fullmatch(r"/SefinNacional/dps/([0-9A-Z]+)", self.path)
                if m:
                    for idd, (chave, _) in srv.notas.items():
                        if m.group(1) in (idd, idd[3:]):
                            return self._json(200, {"chaveAcesso": chave, "idDps": idd})
                    return self._json(404, {"erros": [{"Codigo": "E404", "Descricao": "nao achou"}]})
                m = re.fullmatch(r"/SefinNacional/nfse/(\d{50})/eventos", self.path)
                if m:
                    if m.group(1) in srv.canceladas:
                        return self._json(200, {"eventos": [{"arquivoXmlGZipB64": gzb64(
                            evento_cancelamento_ficticio(m.group(1)))}]})
                    return self._json(200, {"eventos": []})
                m = re.fullmatch(r"/SefinNacional/nfse/(\d{50})", self.path)
                if m:
                    for chave, nfse in srv.notas.values():
                        if chave == m.group(1):
                            return self._json(200, {"chaveAcesso": chave, "nfseXmlGZipB64": gzb64(nfse)})
                return self._json(404, {})

        class Servidor(http.server.ThreadingHTTPServer):
            def handle_error(self, request, client_address):
                pass

        self.httpd = Servidor(("127.0.0.1", 0), Tratador)
        self.httpd.socket = ctx.wrap_socket(self.httpd.socket, server_side=True)
        self.url = f"https://127.0.0.1:{self.httpd.server_address[1]}/SefinNacional"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def parar(self):
        self.httpd.shutdown()
        self.httpd.server_close()


# ------------------------------------------------------------------ execução do CLI

def rodar(args, env, entrada=None):
    p = subprocess.run([sys.executable, str(AQUI / "nfse.py")] + args, input=entrada,
                       capture_output=True, text=True, env=env, timeout=180)
    saida = (p.stdout or "") + (p.stderr or "")
    SAIDAS.append(saida)
    return p.returncode, saida


def linha_com(saida, prefixo):
    for ln in saida.splitlines():
        if ln.startswith(prefixo):
            return ln
    return saida.strip().splitlines()[0] if saida.strip() else "(sem saída)"


def hash_de(saida):
    m = re.search(r"hash:\s+([0-9a-f]{12})", saida)
    return m.group(1) if m else None


def preparar_dados(pasta, env):
    pasta.mkdir(parents=True, exist_ok=True, mode=0o700)
    rodar(["iniciar"], env)
    gravar_0600(pasta / "empresa.json", json.dumps(EMPRESA, ensure_ascii=False).encode())
    gravar_0600(pasta / "clientes" / "cliente-ficticio.json",
                json.dumps(CLIENTE, ensure_ascii=False).encode())


def texto_pdf(pdf):
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True)
        return r.stdout, "pdftotext"
    return None, "pdftotext ausente"


def ler_qr(pdf, pasta):
    try:
        import cv2
    except ImportError:
        return None, "opencv ausente"
    if not shutil.which("pdftoppm"):
        return None, "pdftoppm ausente"
    subprocess.run(["pdftoppm", "-r", "200", "-png", "-f", "1", "-l", "1", str(pdf),
                    str(pasta / "pagina")], check=True)
    img = cv2.imread(str(sorted(pasta.glob("pagina*.png"))[0]))
    texto, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    return texto, "opencv"


# ------------------------------------------------------------------ provas

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trabalho")
    ap.add_argument("--manter", action="store_true")
    a = ap.parse_args()
    if a.trabalho:
        trabalho = Path(a.trabalho).expanduser().resolve()
        trabalho.mkdir(parents=True, exist_ok=True, mode=0o700)
        trabalho = Path(tempfile.mkdtemp(prefix="nfse-autoteste-", dir=trabalho))
    else:
        trabalho = Path(tempfile.mkdtemp(prefix="nfse-autoteste-"))
    if trabalho == SKILL_DIR or SKILL_DIR in trabalho.parents:
        print("A pasta de trabalho não pode ficar dentro da skill.")
        return 2
    tmp = trabalho / "tmp"
    tmp.mkdir(mode=0o700)
    servidor = None
    try:
        print(f"pasta de trabalho: {trabalho}")
        chave, cert = certificado_autoassinado(
            f"EMPRESA FICTICIA PRESTADORA LTDA:{CNPJ_PRESTADOR}", 20,
            san=[x509.OtherName(x509.ObjectIdentifier("2.16.76.1.3.3"),
                                b"\x04\x0e" + CNPJ_PRESTADOR.encode())])
        pfx = trabalho / "certificado-teste.pfx"
        gravar_0600(pfx, pkcs12.serialize_key_and_certificates(
            b"teste", chave, cert, None,
            serialization.BestAvailableEncryption(SENHA_PFX.encode())))
        cert_der = cert.public_bytes(serialization.Encoding.DER)
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)
        print("certificado AUTOASSINADO de teste gerado (validade 20 dias, sem valor fiscal)")

        # ---------------- P1
        print("\n== P1 montagem, Id, namespace e assinatura")
        dh = dt.datetime(2026, 10, 1, 9, 30, tzinfo=dt.timezone(dt.timedelta(hours=-3)))
        xml_100 = None
        for versao in dps.VERSOES:
            raiz, id_dps = dps.montar_dps(EMPRESA, CLIENTE, NOTA, "restrita", 42, dh, versao=versao)
            partes = dps.decompor_id(id_dps)
            esperado = {"prefixo": "DPS", "municipio": "9999999", "tipo_inscricao": "2",
                        "inscricao": CNPJ_PRESTADOR, "serie": "00001",
                        "numero": "000000000000042"}
            marca(f"P1 Id com 45 caracteres, versão {versao}", len(id_dps) == 45,
                  f"{id_dps} ({len(id_dps)})")
            marca(f"P1 composição do Id, versão {versao}", partes == esperado,
                  " + ".join(partes.values()))
            elementos = list(raiz.iter(etree.Element))
            fora = [e.tag for e in elementos if etree.QName(e).namespace != NS]
            marca(f"P1 namespace da NFS-e em todos os níveis, versão {versao}", not fora,
                  f"{len(elementos)} elementos, fora do namespace: {len(fora)}")
            erros = dps.validar_estrutura(raiz, versao=versao)
            marca(f"P1 estrutura conferida, versão {versao}", not erros, "; ".join(erros) or
                  f"versao={raiz.get('versao')}")
            if versao == "1.00":
                xml_100 = dps.serializar(raiz)
        assinados = {}
        for alg in ("sha256", "sha1"):
            assinado = assinatura.assinar_dps(xml_100, chave, cert, alg)
            assinados[alg] = assinado
            pre = dps.prefixos(etree.fromstring(assinado))
            marca(f"P1 assinado sem prefixo de namespace ({alg})", not pre and b"xmlns:" not in assinado,
                  "nenhum prefixo" if not pre else pre[0])
            erros, si_c14n, valor, nome_hash = verificar_independente(assinado, cert_der)
            marca(f"P1 conferência independente: C14N da biblioteca padrão + RSA ({alg})", not erros,
                  "; ".join(erros) or "digest e RSA conferem")
            r, txt = verificar_openssl(si_c14n, valor, cert, nome_hash, trabalho)
            marca(f"P1 RSA conferida pelo openssl ({alg})", r, txt, pulado=r is None)
            r, txt = verificar_xmlsec(assinado, cert_pem)
            marca(f"P1 assinatura conferida pela libxmlsec1 ({alg})", r, txt, pulado=r is None)
            r, txt = verificar_xmlsec1(assinado, cert_pem, trabalho)
            marca(f"P1 assinatura conferida pelo xmlsec1 ({alg})", r, str(txt), pulado=r is None)
            adulterado = assinado.replace(b"<vServ>700.00</vServ>", b"<vServ>7000.00</vServ>")
            erros_a, _, _, _ = verificar_independente(adulterado, cert_der)
            marca(f"P1 adulteração do valor derruba a conferência ({alg})",
                  adulterado != assinado and any("digest" in e for e in erros_a), "; ".join(erros_a))
            r, txt = verificar_xmlsec(adulterado, cert_pem)
            marca(f"P1 libxmlsec1 recusa o adulterado ({alg})", r is False, txt, pulado=r is None)

        # ---------------- P2
        print("\n== P2 lição do namespace no XML autorizado")
        chave_p2 = chave_ficticia(1)
        nfse = nfse_ficticia(assinados["sha256"], 1, chave_p2)
        info = dps.ler_nfse(nfse)
        ingenuo = dps.ler_ingenuo(nfse)
        campos = {k: info[k] for k in ("prestador_cnpj", "tomador_nome", "valor_servico")}
        print(f"  leitor da skill:  {campos}")
        print(f"  leitor ingênuo:   {ingenuo}")
        marca("P2 leitor da skill extrai CNPJ, tomador e valor",
              campos == {"prestador_cnpj": CNPJ_PRESTADOR, "tomador_nome": CLIENTE["nome"],
                         "valor_servico": "700.00"})
        marca("P2 leitor ingênuo (só o primeiro nível qualificado) volta vazio",
              all(v is None for v in ingenuo.values()))
        marca("P2 chave lida do Id de infNFSe tem 50 dígitos", info["chave"] == chave_p2
              and len(info["chave"]) == 50, info["chave"])

        # ---------------- P4 (guardas) e P3 (PDF)
        print("\n== P4 guardas")
        base_env = {k: v for k, v in os.environ.items() if not k.startswith("NFSE_")}
        base_env["TMPDIR"] = str(tmp)
        dados = trabalho / "dados-guardas"
        env = dict(base_env, NFSE_DADOS_DIR=str(dados), NFSE_PFX_PATH=str(pfx),
                   NFSE_PFX_PASSWORD=SENHA_PFX)
        cod, s = rodar(["conferir"], base_env)
        marca("P4 recusa sem NFSE_DADOS_DIR", cod == 2 and "NFSE_DADOS_DIR não está definida" in s,
              linha_com(s, "RECUSADO"))
        dentro = SKILL_DIR / "dados-do-dono-teste"
        cod, s = rodar(["iniciar"], dict(env, NFSE_DADOS_DIR=str(dentro)))
        marca("P4 recusa pasta de dados dentro da skill (e não cria a pasta)",
              cod == 2 and "dentro da pasta da skill" in s and not dentro.exists(),
              linha_com(s, "RECUSADO"))
        preparar_dados(dados, env)
        args_prep = ["preparar", "--cliente", "cliente-ficticio", "--valor", "700",
                     "--competencia", "2026-09", "--descricao", "referente a setembro"]
        cod, s = rodar(args_prep, dict(env, NFSE_AMBIENTE="producao"))
        marca("P4 recusa produção sem a flag --producao", cod == 2 and "duas coisas juntas" in s,
              linha_com(s, "RECUSADO"))
        cod, s = rodar(args_prep + ["--producao"], env)
        marca("P4 recusa --producao sem NFSE_AMBIENTE=producao",
              cod == 2 and "duas coisas juntas" in s, linha_com(s, "RECUSADO"))
        cod, s = rodar(args_prep, env)
        h = hash_de(s)
        marca("P4 preparar em produção restrita imprime resumo e hash", cod == 0 and h,
              f"hash {h}")
        marca("P4 aviso de certificado vencendo (30 dias ou menos)", "AVISO: o certificado vence em" in s,
              linha_com(s, "AVISO: o certificado"))
        cod, s = rodar(["emitir", "--hash", "0" * 12], env)
        marca("P4 recusa emitir com hash errado", cod == 2 and "não confere com nenhum rascunho" in s,
              linha_com(s, "RECUSADO"))
        arq = dados / "rascunhos" / h / "dps.xml"
        arq.write_bytes(arq.read_bytes().replace(b"<vServ>700.00</vServ>", b"<vServ>900.00</vServ>"))
        cod, s = rodar(["emitir", "--hash", h], env)
        marca("P4 recusa rascunho alterado depois do resumo", cod == 2 and "não bate com o hash" in s,
              linha_com(s, "RECUSADO"))
        cod, s = rodar(["palavra-passe", "--definir"], env, entrada=PALAVRA + "\n")
        marca("P4 palavra-passe definida pela entrada padrão", cod == 0, s.strip().splitlines()[-1])
        envp = dict(env, NFSE_AMBIENTE="producao")
        cod, s = rodar(args_prep + ["--producao"], envp)
        hp = hash_de(s)
        marca("P4 preparar em produção (env + flag) só monta o rascunho", cod == 0 and hp and
              "PRODUÇÃO" in s, f"hash {hp}")
        sem_cert = dict(envp, NFSE_PFX_PATH=str(trabalho / "nao-existe.pfx"))
        cod, s = rodar(["emitir", "--hash", hp, "--producao"], sem_cert)
        marca("P4 recusa produção sem palavra-passe na entrada", cod == 2 and
              "--palavra-passe-stdin" in s, linha_com(s, "RECUSADO"))
        cod, s = rodar(["emitir", "--hash", hp, "--producao", "--palavra-passe-stdin"], sem_cert,
                       entrada="palavra-errada\n")
        marca("P4 recusa palavra-passe errada em produção", cod == 2 and "palavra-passe não confere" in s,
              linha_com(s, "RECUSADO"))
        cod, s = rodar(["emitir", "--hash", hp, "--producao", "--palavra-passe-stdin"], sem_cert,
                       entrada=PALAVRA + "\n")
        marca("P4 palavra certa passa o portão e para no certificado ausente, sem rede",
              cod == 2 and "não achei o certificado" in s, linha_com(s, "RECUSADO"))
        cod, s = rodar(["emitir", "--hash", hp, "--producao", "--palavra-passe-stdin"],
                       dict(envp, NFSE_URL_BASE="https://outro-host.exemplo/SefinNacional"),
                       entrada=PALAVRA + "\n")
        marca("P4 recusa endereço base fora do host oficial em produção",
              cod == 2 and "só aceita o host sefin.nfse.gov.br" in s, linha_com(s, "RECUSADO"))
        aberto = trabalho / "certificado-aberto.pfx"
        shutil.copy(pfx, aberto)
        os.chmod(aberto, 0o644)
        cod, s = rodar(args_prep, dict(env, NFSE_PFX_PATH=str(aberto)))
        marca("P4 recusa certificado legível por outros usuários", cod == 2 and "chmod 600" in s,
              linha_com(s, "RECUSADO"))
        cod, s = rodar(args_prep, dict(env, NFSE_PFX_PASSWORD="senha-errada-de-teste"))
        marca("P4 recusa senha errada do certificado sem ecoar a senha",
              cod == 2 and "senha errada" in s and "senha-errada-de-teste" not in s,
              linha_com(s, "RECUSADO"))
        cli2 = json.loads(json.dumps(CLIENTE))
        cli2["iss"]["tpRetISSQN"] = 2
        gravar_0600(dados / "clientes" / "cliente-retencao.json", json.dumps(cli2).encode())
        cod, s = rodar(["preparar", "--cliente", "cliente-retencao", "--valor", "700",
                        "--competencia", "2026-09"], env)
        marca("P4 limite declarado: ISS retido pede alíquota que a skill não monta",
              cod == 2 and "LIMITE: tpRetISSQN=2" in s, linha_com(s, "RECUSADO"))
        cli3 = json.loads(json.dumps(CLIENTE))
        cli3["nome"] = "<razão social ou nome completo do cliente>"
        gravar_0600(dados / "clientes" / "cliente-incompleto.json", json.dumps(cli3).encode())
        cod, s = rodar(["preparar", "--cliente", "cliente-incompleto", "--valor", "700",
                        "--competencia", "2026-09"], env)
        marca("P4 marcador de ficha conta como dado faltando, uma pergunta por vez",
              cod == 3 and "Pergunta ao dono: Qual a razão social" in s, linha_com(s, "Pergunta"))
        marca("P4 recusa sem NFSE_DADOS_DIR vale também para o PDF",
              rodar(["pdf", "--xml", "x.xml"], base_env)[0] == 2)
        vistos = []
        original = cofre.arquivos_tls_temporarios

        @contextlib.contextmanager
        def espiao(*args):
            with original(*args) as (arq_c, arq_k, senha):
                vistos.append((Path(arq_k), oct(os.stat(arq_k).st_mode & 0o777),
                               Path(arq_k).read_bytes()[:37]))
                yield arq_c, arq_k, senha

        cofre.arquivos_tls_temporarios = espiao
        try:
            ctx = cliente_sefin.contexto_tls(chave, cert, [])
        finally:
            cofre.arquivos_tls_temporarios = original
        k, modo, inicio = vistos[0]
        marca("P4 chave temporária nasce 0600 e cifrada e some antes de qualquer conexão",
              modo == "0o600" and inicio.startswith(b"-----BEGIN ENCRYPTED " b"PRIVATE KEY")
              and not k.exists() and not k.parent.exists() and isinstance(ctx, ssl.SSLContext),
              f"modo {modo}, {inicio.decode().strip('-')}, apagada antes de conectar: {not k.exists()}")

        # ---------------- P5 servidor local
        print("\n== P5 envio contra servidor LOCAL de mentira (127.0.0.1, TLS mútuo)")
        servidor = ServidorFalso(trabalho, cert)
        dados_e = trabalho / "dados-envio"
        enve = dict(base_env, NFSE_DADOS_DIR=str(dados_e), NFSE_PFX_PATH=str(pfx),
                    NFSE_PFX_PASSWORD=SENHA_PFX, NFSE_URL_BASE=servidor.url,
                    NFSE_CA_BUNDLE=str(servidor.ca))
        preparar_dados(dados_e, enve)

        def ciclo():
            c1, s1 = rodar(args_prep, enve)
            hh = hash_de(s1)
            c2, s2 = rodar(["emitir", "--hash", hh or "x"], enve)
            return c1, c2, s2

        servidor.modo = "ok"
        _, cod, s = ciclo()
        nota1 = next(dados_e.glob("notas/restrita/*/*/nfse.xml"), None)
        marca("P5 autorizada: XML guardado e chave no relato", cod == 0 and "NFS-e AUTORIZADA" in s
              and nota1 is not None, linha_com(s, "  chave de acesso"))
        pdf1 = nota1.with_suffix(".pdf") if nota1 else None
        marca("P5 PDF gerado junto da nota", pdf1 is not None and pdf1.exists(),
              str(pdf1) if pdf1 and pdf1.exists() else linha_com(s, "  PDF"),
              pulado="não gerado" in s)
        servidor.modo = "rejeita"
        _, cod, s = ciclo()
        marca("P5 rejeitada: nada emitido e erro do servidor mostrado",
              cod == 5 and "E9999" in s, linha_com(s, "REJEITADA"))
        servidor.modo = "cai_depois"
        _, cod, s = ciclo()
        m = re.search(r"consultar --dps (DPS[0-9A-Z]{42})", s)
        id_incerto = m.group(1) if m else ""
        marca("P5 incerta: resposta caiu, skill não reenvia e manda consultar", cod == 6 and
              "NÃO emita de novo" in s and id_incerto, linha_com(s, "ENVIO INCERTO"))
        cod, s = rodar(args_prep, enve)
        marca("P5 pendência bloqueia novo preparar", cod == 2 and "sem desfecho conhecido" in s,
              linha_com(s, "RECUSADO"))
        posts_antes = sum(1 for p in servidor.pedidos if p[0] == "POST")
        cod, s = rodar(["consultar", "--dps", id_incerto], enve)
        marca("P5 consulta pelo Id do DPS acha a nota que tinha saído e resolve sem reenvio",
              cod == 0 and "virou nota" in s and
              sum(1 for p in servidor.pedidos if p[0] == "POST") == posts_antes,
              linha_com(s, "O envio"))
        servidor.modo = "cai_antes"
        _, cod, s = ciclo()
        m = re.search(r"consultar --dps (DPS[0-9A-Z]{42})", s)
        id_sem = m.group(1) if m else ""
        cod, s = rodar(["consultar", "--dps", id_sem], enve)
        marca("P5 consulta sem nota não libera sozinha", cod == 0 and "Nenhuma NFS-e encontrada" in s
              and rodar(args_prep, enve)[0] == 2, linha_com(s, "Nenhuma"))
        cod, s = rodar(["resolver", "--dps", id_sem, "--sem-nota"], enve)
        marca("P5 dono libera com resolver --sem-nota depois da consulta", cod == 0,
              s.strip().splitlines()[-1] if s.strip() else "")
        servidor.modo = "ok"
        cod, s = rodar(args_prep, enve)
        marca("P5 próximo preparar usa número novo (contador só avança depois do envio)",
              cod == 0 and "número 5" in s, linha_com(s, "  DPS:"))
        chave1 = dps.ler_nfse(nota1.read_bytes())["chave"] if nota1 else ""
        servidor.canceladas.add(chave1)
        cod, s = rodar(["eventos", "--chave", chave1], enve)
        marca("P5 eventos: cancelamento reconhecido", cod == 0 and "CANCELADA" in s,
              linha_com(s, "A nota"))
        cod, s = rodar(["pdf", "--xml", str(nota1)], enve)
        txt, ferramenta = texto_pdf(pdf1) if pdf1 and pdf1.exists() else (None, "sem PDF")
        marca("P5 PDF refeito mostra CANCELADA", txt is not None and "CANCELADA" in txt,
              ferramenta, pulado=txt is None)
        hosts = {re.sub(r":\d+/.*", "", servidor.url)}
        marca("P5 só houve tráfego com o servidor local", hosts == {"https://127.0.0.1"} and
              len(servidor.pedidos) > 0, f"{len(servidor.pedidos)} pedidos a {hosts.pop()}")

        # ---------------- P3 PDF
        print("\n== P3 PDF a partir do XML autorizado fictício")
        pasta_p3 = dados / "notas" / "restrita" / "2026-09" / "p3"
        pasta_p3.mkdir(parents=True, mode=0o700)
        gravar_0600(pasta_p3 / "nfse.xml", nfse)
        cod, s = rodar(["pdf", "--xml", str(pasta_p3 / "nfse.xml")], env)
        pdf = pasta_p3 / "nfse.pdf"
        if cod == 4:
            marca("P3 PDF gerado", False, linha_com(s, "DEPENDÊNCIA"), pulado=True)
        else:
            marca("P3 PDF gerado a partir do XML", cod == 0 and pdf.exists(), linha_com(s, "PDF"))
            txt, ferramenta = texto_pdf(pdf)
            if txt is None:
                marca("P3 texto do PDF conferido", False, ferramenta, pulado=True)
            else:
                plano = re.sub(r"\s+", " ", txt)
                for rotulo, alvo in [("CNPJ do prestador", "11.222.333/0001-81"),
                                     ("cliente", CLIENTE["nome"]), ("valor", "R$ 700,00"),
                                     ("chave de acesso em bloco único", chave_p2),
                                     ("aviso de ambiente de teste", "SEM VALIDADE JURÍDICA"),
                                     ("frase do documento fiscal", "O documento fiscal é o XML")]:
                    marca(f"P3 PDF traz {rotulo}", alvo in plano, f"{ferramenta}: {alvo}")
            qr, ferramenta = ler_qr(pdf, trabalho)
            url = f"https://www.nfse.gov.br/ConsultaPublica/?tpc=1&chave={chave_p2}"
            marca("P3 QR do PDF aponta para a consulta pública da chave", qr == url,
                  f"{ferramenta}: {qr}", pulado=qr is None)

        # ---------------- P4 segredos e temporários
        print("\n== P4 segredos e temporários")
        vazou = [i for i, s in enumerate(SAIDAS) if SENHA_PFX in s or PALAVRA in s]
        marca("P4 senha do certificado e palavra-passe fora de toda saída", not vazou,
              f"{len(SAIDAS)} saídas varridas")
        arquivos = [p for p in (dados, dados_e) for p in p.rglob("*") if p.is_file()]
        com_segredo = [str(p) for p in arquivos if SENHA_PFX.encode() in p.read_bytes()
                       or PALAVRA.encode() in p.read_bytes()]
        marca("P4 senha e palavra-passe fora de todo arquivo de dados e do registro",
              not com_segredo, f"{len(arquivos)} arquivos varridos, incluindo registro.jsonl")
        sobra = [str(p) for p in tmp.rglob("*")]
        marca("P4 nenhum temporário de chave sobrou", not sobra,
              f"{len(sobra)} itens em TMPDIR depois de {len(servidor.pedidos)} conexões TLS")
        perm = [str(p) for p in arquivos if p.stat().st_mode & 0o077]
        marca("P4 arquivos de dados com permissão 600", not perm,
              f"{len(arquivos)} arquivos" if not perm else perm[0])
    finally:
        if servidor:
            servidor.parar()
        if a.manter:
            print(f"\npasta mantida: {trabalho}")
        else:
            shutil.rmtree(trabalho, ignore_errors=True)
            print(f"\npasta de trabalho apagada, certificado de teste incluído: {not trabalho.exists()}")
    falhas = [n for n, r in RESULTADOS if r is False]
    pulados = [n for n, r in RESULTADOS if r == "pulado"]
    print(f"autoteste: {len(RESULTADOS) - len(falhas) - len(pulados)} ok, {len(falhas)} falha(s), "
          f"{len(pulados)} pulado(s)")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
