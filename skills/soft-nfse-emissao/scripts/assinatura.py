#!/usr/bin/env python3
"""
assinatura.py - assinatura XMLDSig do DPS, implementação própria e pequena.

Perfil montado: assinatura envelopada, C14N inclusiva, uma referência ao Id do
infDPS com duas transformações (enveloped e C14N, como o XSD 1.00 descreve),
bloco Signature dentro do DPS depois do infDPS, sem prefixo de namespace, e o
certificado em X509Data.

Algoritmo: NFSE_ASSINATURA_ALGORITMO = sha256 (padrão, RSA-SHA256 com digest
SHA-256, como o guia de origem relata) ou sha1 (RSA-SHA1 com digest SHA-1, o que
o XSD 1.00 fixa). Nenhum texto oficial lido decide entre os dois; só o envio na
produção restrita, com o certificado do dono, prova qual o servidor aceita.

Por que sem xmlsec: a biblioteca xmlsec depende de libxmlsec1 do sistema e
precisa casar a versão da libxml2 com a do lxml (erro conhecido de versão
divergente). Para um perfil fixo de uma referência, lxml (C14N) mais
cryptography (RSA) cobrem tudo, sem pacote de sistema. A conferência da
assinatura roda por caminho independente no autoteste.
"""
import base64
import copy
import hashlib
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from lxml import etree

DS = "http://www.w3.org/2000/09/xmldsig#"
ALG_C14N = "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
ALG_ENVELOPADA = "http://www.w3.org/2000/09/xmldsig#enveloped-signature"
ALGORITMOS = {
    "sha256": {"assinatura": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
               "digest": "http://www.w3.org/2001/04/xmlenc#sha256",
               "hashlib": "sha256", "hash": hashes.SHA256},
    "sha1": {"assinatura": "http://www.w3.org/2000/09/xmldsig#rsa-sha1",
             "digest": "http://www.w3.org/2000/09/xmldsig#sha1",
             "hashlib": "sha1", "hash": hashes.SHA1},
}


def algoritmo_configurado():
    v = os.environ.get("NFSE_ASSINATURA_ALGORITMO", "sha256").strip().lower() or "sha256"
    if v not in ALGORITMOS:
        raise ValueError(f"NFSE_ASSINATURA_ALGORITMO só aceita sha256 ou sha1 (veio {v!r})")
    return v


def _c14n(el):
    """C14N inclusiva do elemento como raiz de um documento próprio (cópia).

    Canonicalizar o subelemento direto, no lxml 6.1 com libxml2 2.14, pôs xmlns=""
    nos netos: o digest saiu diferente do da libxmlsec1 e a assinatura seria
    recusada. Com a cópia como raiz, o resultado bate com a libxmlsec1 (autoteste).
    Vale porque o DPS montado só usa o namespace padrão, sem prefixo nenhum."""
    copia = copy.deepcopy(el)
    copia.tail = None
    return etree.tostring(copia, method="c14n", exclusive=False, with_comments=False)


def chave_confere_com_certificado(chave, cert):
    return chave.public_key().public_numbers() == cert.public_key().public_numbers()


def assinar_dps(xml_bytes, chave, cert, algoritmo=None):
    """Recebe o DPS sem assinatura (bytes) e devolve o DPS assinado (bytes)."""
    alg = ALGORITMOS[algoritmo or algoritmo_configurado()]
    if not isinstance(chave, rsa.RSAPrivateKey):
        raise ValueError("a chave do certificado não é RSA; o perfil montado é RSA")
    if not chave_confere_com_certificado(chave, cert):
        raise ValueError("a chave privada do .pfx não corresponde ao certificado")
    parser = etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False)
    raiz = etree.fromstring(xml_bytes, parser)
    ns = etree.QName(raiz).namespace
    if dict(raiz.nsmap) != {None: ns}:
        raise ValueError(f"o DPS só pode declarar o namespace padrão (veio {dict(raiz.nsmap)})")
    inf = raiz.find(f"{{{ns}}}infDPS")
    if inf is None or not inf.get("Id"):
        raise ValueError("DPS sem infDPS com Id")
    if raiz.find(f"{{{DS}}}Signature") is not None:
        raise ValueError("o DPS já vem assinado")

    resumo = hashlib.new(alg["hashlib"], _c14n(inf)).digest()

    sig = etree.SubElement(raiz, f"{{{DS}}}Signature", nsmap={None: DS})
    si = etree.SubElement(sig, f"{{{DS}}}SignedInfo")
    etree.SubElement(si, f"{{{DS}}}CanonicalizationMethod", Algorithm=ALG_C14N)
    etree.SubElement(si, f"{{{DS}}}SignatureMethod", Algorithm=alg["assinatura"])
    ref = etree.SubElement(si, f"{{{DS}}}Reference", URI="#" + inf.get("Id"))
    trs = etree.SubElement(ref, f"{{{DS}}}Transforms")
    etree.SubElement(trs, f"{{{DS}}}Transform", Algorithm=ALG_ENVELOPADA)
    etree.SubElement(trs, f"{{{DS}}}Transform", Algorithm=ALG_C14N)
    etree.SubElement(ref, f"{{{DS}}}DigestMethod", Algorithm=alg["digest"])
    etree.SubElement(ref, f"{{{DS}}}DigestValue").text = base64.b64encode(resumo).decode("ascii")

    valor = chave.sign(_c14n(si), padding.PKCS1v15(), alg["hash"]())
    etree.SubElement(sig, f"{{{DS}}}SignatureValue").text = base64.b64encode(valor).decode("ascii")
    ki = etree.SubElement(sig, f"{{{DS}}}KeyInfo")
    xd = etree.SubElement(ki, f"{{{DS}}}X509Data")
    der = cert.public_bytes(serialization.Encoding.DER)
    etree.SubElement(xd, f"{{{DS}}}X509Certificate").text = base64.b64encode(der).decode("ascii")
    return etree.tostring(raiz, xml_declaration=True, encoding="UTF-8")
