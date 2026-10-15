"""Funções comuns dos scripts de office/ (Soft Office).

Não é um comando. Os outros scripts da pasta importam daqui:

- leitor de XML seguro (sem entidade externa, sem rede, sem DTD);
- recuo e retirada de recuo que não mudam o sentido do XML;
- leitura segura de um pacote zip (OOXML / Open Packaging Conventions).

Escrito do zero a partir da norma ECMA-376 (partes 1 e 2) e da documentação
pública de lxml e zipfile.
"""

import posixpath
import stat
import sys
import zipfile

SAIDA_OK = 0
SAIDA_REPROVOU = 1
SAIDA_ARGUMENTO = 2
SAIDA_FALTA = 3
SAIDA_EXTERNO = 4

try:
    from lxml import etree
except ImportError:  # pragma: no cover
    etree = None

XML_NS = "http://www.w3.org/XML/1998/namespace"
ATRIB_ESPACO = "{%s}space" % XML_NS
RECUO = "  "

# Limites contra bomba de compressão. Podem ser trocados por quem importa.
LIMITE_TOTAL_BYTES = 2 * 1024 ** 3
LIMITE_RAZAO = 1000
LIMITE_PARTES = 20000


def exigir_lxml():
    """Sai com código 3 se a lxml não estiver instalada."""
    if etree is None:
        print("falta a biblioteca lxml. Instale com: pip install lxml", file=sys.stderr)
        sys.exit(SAIDA_FALTA)


def novo_leitor():
    """Leitor de XML que não resolve entidade, não acessa rede e não carrega DTD."""
    exigir_lxml()
    return etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        dtd_validation=False,
        remove_blank_text=False,
        remove_comments=False,
        strip_cdata=False,
        huge_tree=True,
    )


def ler_xml(dados):
    """Devolve a árvore lxml dos bytes. Levanta etree.XMLSyntaxError se malformado."""
    return etree.fromstring(dados, novo_leitor()).getroottree()


def gravar_xml(arvore, dados_originais):
    """Serializa a árvore mantendo declaração, codificação e standalone.

    Em UTF-8, a declaração original é copiada byte a byte (aspas e quebra de
    linha incluídas), como o Office grava.
    """
    info = arvore.docinfo
    bom = b"\xef\xbb\xbf" if dados_originais.startswith(b"\xef\xbb\xbf") else b""
    sem_bom = dados_originais[len(bom):]
    tem_declaracao = sem_bom.startswith(b"<?xml")
    codificacao = info.encoding or "UTF-8"
    if codificacao.upper().replace("-", "") == "UTF8":
        if not tem_declaracao:
            return bom + etree.tostring(arvore, encoding="UTF-8", xml_declaration=False)
        fim = sem_bom.find(b"?>") + 2
        depois = fim
        while depois < len(sem_bom) and sem_bom[depois:depois + 1] in (b"\r", b"\n"):
            depois += 1
        corpo = etree.tostring(arvore, encoding="UTF-8", xml_declaration=False)
        return bom + sem_bom[:depois] + corpo
    if codificacao.upper().replace("-", "") not in ("UTF8", "UTF16"):
        codificacao = "UTF-8"
    kwargs = {"encoding": codificacao, "xml_declaration": tem_declaracao}
    if tem_declaracao and info.standalone is not None:
        kwargs["standalone"] = bool(info.standalone)
    return etree.tostring(arvore, **kwargs)


def eh_arquivo_xml(nome):
    baixo = nome.lower()
    return baixo.endswith(".xml") or baixo.endswith(".rels")


def _so_espaco(texto):
    return texto is None or texto.strip(" \t\r\n") == ""


def _espaco_preservado(elem, herdado):
    valor = elem.get(ATRIB_ESPACO)
    if valor == "preserve":
        return True
    if valor == "default":
        return False
    return herdado


def _eh_misto(elem):
    """Conteúdo misto: texto de verdade ao lado de elementos filhos."""
    if not _so_espaco(elem.text):
        return True
    for filho in elem:
        if not _so_espaco(filho.tail):
            return True
    return False


def recuar(raiz, nivel=0, preservado=False):
    """Põe recuo só onde o espaço não tem sentido.

    Não mexe em: elemento sem filhos (o texto dele fica intacto), elemento sob
    xml:space="preserve", e elemento de conteúdo misto (nem nos filhos dele).
    """
    preservado = _espaco_preservado(raiz, preservado)
    if preservado or len(raiz) == 0 or _eh_misto(raiz):
        return
    dentro = "\n" + RECUO * (nivel + 1)
    raiz.text = dentro
    filhos = list(raiz)
    for i, filho in enumerate(filhos):
        filho.tail = dentro if i < len(filhos) - 1 else "\n" + RECUO * nivel
        if isinstance(filho.tag, str):
            recuar(filho, nivel + 1, preservado)


def tirar_recuo(raiz, preservado=False):
    """Desfaz o recuo: apaga o espaço entre elementos onde ele não tem sentido.

    Mesmas proteções do recuar(): texto de folha, xml:space="preserve" e
    conteúdo misto ficam como estão. Devolve quantos nós de espaço apagou.
    """
    preservado = _espaco_preservado(raiz, preservado)
    if preservado or len(raiz) == 0 or _eh_misto(raiz):
        return 0
    apagados = 0
    if raiz.text is not None:
        raiz.text = None
        apagados += 1
    for filho in raiz:
        if filho.tail is not None:
            filho.tail = None
            apagados += 1
        if isinstance(filho.tag, str):
            apagados += tirar_recuo(filho, preservado)
    return apagados


def nome_inseguro(nome):
    """Devolve o motivo se o nome de entrada do zip for perigoso, senão None."""
    if not nome:
        return "nome vazio"
    if "\\" in nome:
        return "usa barra invertida"
    if "\x00" in nome:
        return "tem caractere nulo"
    if nome.startswith("/"):
        return "caminho absoluto"
    if len(nome) >= 2 and nome[1] == ":":
        return "caminho com letra de unidade"
    partes = nome.rstrip("/").split("/")
    if any(p == ".." for p in partes):
        return "sobe de pasta com .."
    if any(p in ("", ".") for p in partes):
        return "segmento vazio ou ponto"
    return None


def eh_link_simbolico(info):
    modo = (info.external_attr >> 16) & 0xFFFF
    return info.create_system == 3 and stat.S_ISLNK(modo)


def problemas_do_zip(zf):
    """Confere o zip sem extrair. Devolve lista de textos de problema."""
    problemas = []
    vistos = {}
    total = 0
    infos = zf.infolist()
    if len(infos) > LIMITE_PARTES:
        problemas.append("zip com %d entradas, acima do limite de %d" % (len(infos), LIMITE_PARTES))
    for info in infos:
        nome = info.filename
        motivo = nome_inseguro(nome)
        if motivo:
            problemas.append("entrada %r: %s" % (nome, motivo))
        if eh_link_simbolico(info):
            problemas.append("entrada %r é link simbólico" % nome)
        if info.flag_bits & 0x1:
            problemas.append("entrada %r está criptografada" % nome)
        chave = nome.lower()
        if chave in vistos:
            problemas.append("entrada %r repetida (igual a %r, sem diferenciar maiúscula)" % (nome, vistos[chave]))
        vistos[chave] = nome
        total += info.file_size
        if info.compress_size > 0 and info.file_size / info.compress_size > LIMITE_RAZAO and info.file_size > 10 * 1024 ** 2:
            problemas.append("entrada %r com compressão suspeita (%d para %d bytes)" % (nome, info.compress_size, info.file_size))
    if total > LIMITE_TOTAL_BYTES:
        problemas.append("conteúdo descompactado de %d bytes passa do limite de %d" % (total, LIMITE_TOTAL_BYTES))
    return problemas


def abrir_zip(caminho):
    """Abre o zip ou devolve (None, motivo)."""
    try:
        return zipfile.ZipFile(caminho), None
    except zipfile.BadZipFile as erro:
        return None, "não é um zip válido (%s)" % erro
    except OSError as erro:
        return None, "não abriu (%s)" % erro


def pasta_da_parte(nome_parte):
    return posixpath.dirname(nome_parte)
