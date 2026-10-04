#!/usr/bin/env python3
"""
cliente_sefin.py - conversa HTTPS com TLS mútuo com a API do emissor nacional.

Só biblioteca padrão (http.client + ssl). O certificado do cliente vem do .pfx:
chave e certificado vão para arquivo temporário 0600 (chave cifrada com senha
de uso único), entram no contexto TLS e são apagados na mesma hora, antes de
qualquer conexão. A verificação do servidor fica sempre ligada.

Conforme o guia de origem, não confirmado na fonte oficial (o Swagger recusou
acesso): corpo {"dpsXmlGZipB64": ...}, sucesso 201 com "nfseXmlGZipB64". Por isso
o leitor é tolerante: qualquer 2xx sem o campo esperado vira envio incerto com a
resposta bruta guardada, nunca um erro que some com a informação.

Três desfechos de envio, porque o número do DPS depende deles:
- NaoEnviado: a conexão caiu antes do pedido sair. Nada chegou; número intacto.
- Rejeitado: o servidor respondeu com recusa. Nada foi emitido.
- EnvioIncerto: o pedido saiu e a resposta não fechou. Pode ter virado nota.
"""
import base64
import gzip
import http.client
import json
import os
import socket
import ssl
from urllib.parse import quote, urlsplit

import cofre

URL_BASE = {
    "restrita": "https://sefin.producaorestrita.nfse.gov.br/SefinNacional",
    "producao": "https://sefin.nfse.gov.br/SefinNacional",
}
HOSTS_LOCAIS = {"127.0.0.1", "localhost", "::1"}
TEMPO_LIMITE = 60


class NaoEnviado(Exception):
    pass


class EnvioIncerto(Exception):
    def __init__(self, motivo, bruto=b"", chave=None):
        super().__init__(motivo)
        self.bruto = bruto or b""
        self.chave = chave


class Rejeitado(Exception):
    def __init__(self, status, erros, bruto=b""):
        super().__init__(f"HTTP {status}")
        self.status = status
        self.erros = erros
        self.bruto = bruto or b""


class RespostaIlegivel(Exception):
    def __init__(self, motivo, bruto=b""):
        super().__init__(motivo)
        self.bruto = bruto or b""


def url_base(amb):
    """Base da API. NFSE_URL_BASE troca a base do ambiente da vez, com host conferido:
    produção só aceita sefin.nfse.gov.br; restrita aceita host da produção restrita
    (com ou sem o segmento /API) ou endereço local de teste."""
    v = os.environ.get("NFSE_URL_BASE", "").strip().rstrip("/")
    if not v:
        return URL_BASE[amb]
    p = urlsplit(v)
    host = (p.hostname or "").lower()
    if p.scheme != "https":
        raise cofre.Recusa("NFSE_URL_BASE precisa começar com https://")
    if amb == "producao":
        if host != "sefin.nfse.gov.br":
            raise cofre.Recusa("em produção, NFSE_URL_BASE só aceita o host sefin.nfse.gov.br.")
    elif host not in HOSTS_LOCAIS and not host.endswith("producaorestrita.nfse.gov.br"):
        raise cofre.Recusa("na produção restrita, NFSE_URL_BASE só aceita host da produção "
                           "restrita ou endereço local de teste.")
    return v


def contexto_tls(chave, cert, extras):
    ca = os.environ.get("NFSE_CA_BUNDLE", "").strip() or None
    ctx = ssl.create_default_context(cafile=ca)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    with cofre.arquivos_tls_temporarios(chave, cert, extras) as (arq_cert, arq_chave, senha):
        ctx.load_cert_chain(arq_cert, arq_chave, password=senha)
    return ctx


def gz_b64(xml_bytes):
    return base64.b64encode(gzip.compress(xml_bytes, mtime=0)).decode("ascii")


def de_gz_b64(texto):
    return gzip.decompress(base64.b64decode(texto))


def _json(bruto):
    try:
        return json.loads(bruto.decode("utf-8"))
    except Exception:
        return None


def campo(j, nome):
    """Campo do JSON sem depender de maiúscula e minúscula."""
    if not isinstance(j, dict):
        return None
    if nome in j:
        return j[nome]
    for k, v in j.items():
        if k.lower() == nome.lower():
            return v
    return None


def _erros(j, bruto):
    """Lista de 'codigo: descricao' tolerante ao formato da resposta de erro."""
    out = []
    if isinstance(j, dict):
        for k in ("erros", "erro", "mensagens"):
            v = campo(j, k)
            if isinstance(v, dict):
                v = [v]
            if isinstance(v, list):
                for e in v:
                    if isinstance(e, dict):
                        partes = [f"{campo(e, 'codigo')}:" if campo(e, "codigo") else "",
                                  str(campo(e, "descricao") or campo(e, "mensagem") or ""),
                                  str(campo(e, "complemento") or "")]
                        out.append(" ".join(x for x in partes if x).strip())
                    else:
                        out.append(str(e))
        if not out and campo(j, "mensagem"):
            out.append(str(campo(j, "mensagem")))
    if not out:
        out.append(bruto[:500].decode("utf-8", "replace") or "(resposta vazia)")
    return out


def _conectar(url, ctx):
    p = urlsplit(url)
    conn = http.client.HTTPSConnection(p.hostname, p.port or 443, context=ctx,
                                       timeout=TEMPO_LIMITE)
    try:
        conn.connect()
    except (OSError, ssl.SSLError, socket.timeout) as e:
        conn.close()
        raise NaoEnviado(f"conexão não abriu ({type(e).__name__}: {e})") from None
    return conn, p.path + (f"?{p.query}" if p.query else "")


def _pedir(metodo, url, ctx, corpo=None):
    conn, caminho = _conectar(url, ctx)
    cab = {"Accept": "application/json", "User-Agent": "nfse-emissao/1.0"}
    dados = None
    if corpo is not None:
        dados = json.dumps(corpo).encode("utf-8")
        cab["Content-Type"] = "application/json"
    try:
        conn.request(metodo, caminho, body=dados, headers=cab)
        r = conn.getresponse()
        return r.status, r.read()
    except (OSError, ssl.SSLError, socket.timeout, http.client.HTTPException) as e:
        raise EnvioIncerto(f"a resposta não fechou ({type(e).__name__}: {e})") from None
    finally:
        conn.close()


def enviar_dps(amb, ctx, xml_assinado):
    """POST do DPS. Devolve (json, xml da NFS-e autorizada, resposta bruta)."""
    status, bruto = _pedir("POST", url_base(amb) + "/nfse", ctx,
                           {"dpsXmlGZipB64": gz_b64(xml_assinado)})
    if 200 <= status < 300:
        j = _json(bruto)
        b64 = campo(j, "nfseXmlGZipB64")
        chave = campo(j, "chaveAcesso")
        if not b64:
            raise EnvioIncerto(f"HTTP {status} sem o campo nfseXmlGZipB64", bruto, chave)
        try:
            return j, de_gz_b64(b64), bruto
        except Exception:
            raise EnvioIncerto(f"HTTP {status} com o XML da nota ilegível", bruto, chave) from None
    if status in (408, 429) or status >= 500:
        raise EnvioIncerto(f"o servidor respondeu HTTP {status}", bruto)
    raise Rejeitado(status, _erros(_json(bruto), bruto), bruto)


def consultar_nfse(amb, ctx, chave):
    """GET da NFS-e pela chave. Devolve (json, xml) ou None quando a resposta é 404."""
    status, bruto = _pedir("GET", f"{url_base(amb)}/nfse/{quote(chave)}", ctx)
    if status == 404:
        return None
    if not 200 <= status < 300:
        raise Rejeitado(status, _erros(_json(bruto), bruto), bruto)
    j = _json(bruto)
    b64 = campo(j, "nfseXmlGZipB64")
    if not b64:
        raise RespostaIlegivel(f"HTTP {status} sem o campo nfseXmlGZipB64", bruto)
    try:
        return j, de_gz_b64(b64)
    except Exception:
        raise RespostaIlegivel(f"HTTP {status} com XML ilegível", bruto) from None


def consultar_dps(amb, ctx, id_dps):
    """GET /dps/{id}. O manual não diz se o id leva o prefixo DPS (45) ou só os 42
    dígitos, então tenta os dois. Devolve (desfecho, chave, bruto) com desfecho em
    achou | nao_achou (404 nos dois formatos) | inconclusivo."""
    candidatos = [id_dps] + ([id_dps[3:]] if id_dps.startswith("DPS") else [])
    for ident in candidatos:
        status, bruto = _pedir("GET", f"{url_base(amb)}/dps/{quote(ident)}", ctx)
        if 200 <= status < 300:
            chave = campo(_json(bruto), "chaveAcesso")
            if chave:
                return "achou", str(chave), bruto
            return "inconclusivo", None, bruto
        if status != 404:
            return "inconclusivo", None, bruto
    return "nao_achou", None, b""


def consultar_eventos(amb, ctx, chave):
    """GET dos eventos da chave. Devolve (json ou None, bruto). 404 vira lista vazia."""
    status, bruto = _pedir("GET", f"{url_base(amb)}/nfse/{quote(chave)}/eventos", ctx)
    if status == 404:
        return [], bruto
    if not 200 <= status < 300:
        raise Rejeitado(status, _erros(_json(bruto), bruto), bruto)
    return _json(bruto), bruto
