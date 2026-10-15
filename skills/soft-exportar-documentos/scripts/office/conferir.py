#!/usr/bin/env python3
"""Confere a estrutura interna de um .docx, .pptx ou .xlsx.

Uso:
    python3 conferir.py ARQUIVO [--original ARQUIVO] [--autor NOME]

O que confere (cada item reprova o arquivo):
- zip: abre, CRC de toda entrada bate, nenhum nome perigoso ou repetido;
- XML: toda parte XML é bem formada e não traz declaração de DTD;
- tipos de conteúdo: [Content_Types].xml existe e toda parte tem tipo
  (por Override ou por Default de extensão); Override sem parte reprova;
- relações: toda relação interna aponta para parte que existe, Id sem
  repetição dentro do mesmo .rels, .rels de parte que não existe;
- partes obrigatórias do formato (documento principal, slides, mestres e
  layouts no deck, abas na planilha);
- identificadores repetidos: slides, mestres e layouts, formas por slide,
  autores de comentário, comentários, notas de rodapé, estilos, numeração,
  abas, nomes definidos e tabelas.

Com --original: lista partes acrescentadas, removidas e mudadas (mudança só de
recuo não conta) e separa os problemas que já existiam no original, que
aparecem no relato mas não reprovam.

Com --autor NOME (só Word): toda alteração rastreada nova precisa ser desse
autor, e o texto do documento com as alterações dele rejeitadas precisa ser
igual ao texto do original (exige --original para a comparação de texto).

Saída: 0 aprovado, 1 reprovado, 2 argumento errado, 3 arquivo ou dependência
faltando.
"""

import argparse
import difflib
import os
import posixpath
import sys
import zipfile
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import comum  # noqa: E402

etree = comum.etree

NS_TIPOS = "http://schemas.openxmlformats.org/package/2006/content-types"
NS_RELS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_R = {
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "http://purl.oclc.org/ooxml/officeDocument/relationships",
}
NS_W = {
    "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "http://purl.oclc.org/ooxml/wordprocessingml/main",
}
NS_P = {
    "http://schemas.openxmlformats.org/presentationml/2006/main",
    "http://purl.oclc.org/ooxml/presentationml/main",
}
NS_MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
TIPO_DOC_PRINCIPAL = ("/officeDocument",)

NOMES_FORMATO = {"docx": "Word", "pptx": "PowerPoint", "xlsx": "Excel", None: "formato não identificado"}

CATEGORIAS = [
    ("zip", "zip íntegro"),
    ("xml", "XML bem formado"),
    ("tipos", "tipos de conteúdo"),
    ("relacoes", "relações internas"),
    ("obrigatorias", "partes obrigatórias"),
    ("ids", "identificadores sem repetição"),
    ("autor", "alterações rastreadas e texto (--autor)"),
]

MUDANCA_INSERE = {"ins", "moveTo"}
MUDANCA_APAGA = {"del", "moveFrom"}
MUDANCA_CONTEUDO = MUDANCA_INSERE | MUDANCA_APAGA
MUDANCA_TODAS = MUDANCA_CONTEUDO | {
    "rPrChange", "pPrChange", "sectPrChange", "tblPrChange", "trPrChange",
    "tcPrChange", "tblGridChange", "tblPrExChange", "numberingChange",
    "cellIns", "cellDel", "cellMerge",
}
PROPRIEDADES = {"pPr", "rPr", "sectPr", "tblPr", "trPr", "tcPr", "tblGrid",
                "tblPrEx", "instrText", "delInstrText", "fldData"}


def nome_local(elem):
    return etree.QName(elem).localname


def eh_w(elem, nome=None):
    if not isinstance(elem.tag, str):
        return False
    q = etree.QName(elem)
    return q.namespace in NS_W and (nome is None or q.localname == nome)


def atributo_ns(elem, nome, espacos):
    for chave, valor in elem.attrib.items():
        if chave.startswith("{"):
            ns, local = chave[1:].split("}", 1)
            if local == nome and ns in espacos:
                return valor
    return None


def atributo_w(elem, nome):
    return atributo_ns(elem, nome, NS_W)


def dentro_de_fallback(elem):
    for anc in elem.iterancestors():
        if isinstance(anc.tag, str) and etree.QName(anc).namespace == NS_MC and etree.QName(anc).localname == "Fallback":
            return True
    return False


class Relato:
    """Resultado de uma conferência."""

    def __init__(self, caminho):
        self.caminho = caminho
        self.formato = None
        self.total_partes = 0
        self.falhas = {c: [] for c, _ in CATEGORIAS}
        self.avisos = {c: [] for c, _ in CATEGORIAS}
        self.usadas = {"zip", "xml", "tipos", "relacoes", "obrigatorias", "ids"}
        self.herdadas = []
        self.comparacao = None
        self.nome_original = None
        self.diferenca_texto = []

    def falha(self, cat, msg):
        if msg not in self.falhas[cat]:
            self.falhas[cat].append(msg)

    def aviso(self, cat, msg):
        if msg not in self.avisos[cat]:
            self.avisos[cat].append(msg)

    def total_falhas(self):
        return sum(len(v) for v in self.falhas.values())

    @property
    def reprovou(self):
        return self.total_falhas() > 0

    def todas_falhas(self):
        return [(c, m) for c, _ in CATEGORIAS for m in self.falhas[c]]

    def texto(self):
        linhas = ["Conferência: %s (%s, %d partes)" % (
            os.path.basename(self.caminho), NOMES_FORMATO.get(self.formato), self.total_partes)]
        for cat, titulo in CATEGORIAS:
            if cat not in self.usadas:
                continue
            falhas, avisos = self.falhas[cat], self.avisos[cat]
            if falhas:
                linhas.append("  [FALHOU] %s (%d)" % (titulo, len(falhas)))
                linhas.extend("           - %s" % m for m in falhas)
            else:
                linhas.append("  [ok]     %s" % titulo)
            linhas.extend("  [aviso]  %s" % m for m in avisos)
        for linha in self.diferenca_texto:
            linhas.append("           %s" % linha)
        if self.comparacao is not None:
            linhas.append("Comparação com o original (%s):" % self.nome_original)
            for chave, titulo in (("acrescentadas", "acrescentadas"), ("removidas", "removidas"),
                                  ("mudadas", "mudadas")):
                itens = self.comparacao[chave]
                linhas.append("  %s (%d)%s" % (titulo, len(itens), ": " + ", ".join(itens) if itens else ""))
            linhas.append("  iguais: %d" % self.comparacao["iguais"])
            if self.herdadas:
                linhas.append("  já existiam no original e não reprovam (%d):" % len(self.herdadas))
                linhas.extend("    - %s" % m for _, m in self.herdadas)
        n = self.total_falhas()
        if n:
            linhas.append("Resultado: REPROVADO, %d problema%s." % (n, "" if n == 1 else "s"))
        else:
            linhas.append("Resultado: APROVADO.")
        return "\n".join(linhas)


class Pacote:
    """Leitura de um pacote OPC já aberto."""

    def __init__(self, zf):
        self.zf = zf
        self.partes = [i.filename for i in zf.infolist() if not i.filename.endswith("/")]
        self.por_minuscula = {p.lower(): p for p in self.partes}
        self._xml = {}
        self.ruins = set()
        self.tipos_default = {}
        self.tipos_override = {}

    def existe(self, nome):
        return nome.lower() in self.por_minuscula

    def real(self, nome):
        return self.por_minuscula.get(nome.lower())

    def ler(self, nome):
        return self.zf.read(self.real(nome))

    def xml(self, nome):
        real = self.real(nome)
        if real is None or real in self.ruins:
            return None
        if real not in self._xml:
            try:
                self._xml[real] = comum.ler_xml(self.zf.read(real))
            except (etree.XMLSyntaxError, zipfile.BadZipFile, OSError, ValueError):
                self.ruins.add(real)
                return None
        return self._xml[real]

    def tipo(self, nome):
        chave = "/" + nome.lower()
        if chave in self.tipos_override:
            return self.tipos_override[chave]
        base = posixpath.basename(nome)
        if "." not in base:
            return None
        # rsplit, não splitext: "_rels/.rels" tem extensão "rels" pela regra do OPC.
        return self.tipos_default.get(base.rsplit(".", 1)[1].lower())

    def parece_xml(self, nome):
        if comum.eh_arquivo_xml(nome):
            return True
        tipo = (self.tipo(nome) or "").lower()
        return tipo.endswith("+xml") or tipo in ("application/xml", "text/xml")

    def relacoes(self, origem):
        """Lista (Id, Type, alvo resolvido ou None se externo, alvo bruto) das relações da parte."""
        if origem == "":
            rels = "_rels/.rels"
        else:
            rels = posixpath.join(posixpath.dirname(origem), "_rels", posixpath.basename(origem) + ".rels")
        arvore = self.xml(rels)
        if arvore is None:
            return []
        saida = []
        for rel in arvore.getroot():
            if not isinstance(rel.tag, str) or nome_local(rel) != "Relationship":
                continue
            alvo = rel.get("Target") or ""
            if (rel.get("TargetMode") or "Internal") == "External":
                saida.append((rel.get("Id"), rel.get("Type") or "", None, alvo))
            else:
                saida.append((rel.get("Id"), rel.get("Type") or "", resolver_alvo(origem, alvo), alvo))
        return saida

    def alvo_por_id(self, origem, rid):
        for ident, tipo, alvo, _ in self.relacoes(origem):
            if ident == rid:
                return alvo, tipo
        return None, None


def resolver_alvo(origem, alvo):
    alvo = unquote(alvo.split("#", 1)[0])
    if not alvo:
        return ""
    if alvo.startswith("/"):
        caminho = alvo
    else:
        caminho = posixpath.dirname(origem) + "/" + alvo
    pilha = []
    for seg in caminho.split("/"):
        if seg in ("", "."):
            continue
        if seg == "..":
            if not pilha:
                return "../" + alvo  # sobe além da raiz do pacote
            pilha.pop()
        else:
            pilha.append(seg)
    return "/".join(pilha)


def origem_dos_rels(nome_rels):
    """'word/_rels/document.xml.rels' -> 'word/document.xml'; '_rels/.rels' -> ''."""
    pasta, base = posixpath.split(nome_rels)
    if posixpath.basename(pasta) != "_rels" or not base.lower().endswith(".rels"):
        return None
    alvo = base[:-5]
    pai = posixpath.dirname(pasta)
    return posixpath.join(pai, alvo) if alvo else ("" if pai == "" else None)


# ---------------------------------------------------------------- conferências

def conferir_zip(zf, rel):
    for problema in comum.problemas_do_zip(zf):
        rel.falha("zip", problema)
    try:
        ruim = zf.testzip()
    except Exception as erro:  # zlib e afins
        rel.falha("zip", "não foi possível ler todas as entradas (%s)" % erro)
        return
    if ruim:
        rel.falha("zip", "entrada %s com CRC errado (arquivo corrompido)" % ruim)


def conferir_xml(pac, rel):
    for nome in pac.partes:
        if not pac.parece_xml(nome):
            continue
        try:
            arvore = comum.ler_xml(pac.ler(nome))
        except etree.XMLSyntaxError as erro:
            pac.ruins.add(nome)
            rel.falha("xml", "%s: XML malformado (%s)" % (nome, erro))
            continue
        info = arvore.docinfo
        if info.doctype or arvore.docinfo.internalDTD is not None:
            rel.falha("xml", "%s: traz declaração de DTD, proibida em OOXML" % nome)


def conferir_tipos(pac, rel):
    if not pac.existe("[Content_Types].xml"):
        rel.falha("tipos", "falta [Content_Types].xml")
        return
    arvore = pac.xml("[Content_Types].xml")
    if arvore is None:
        rel.falha("tipos", "[Content_Types].xml não abre como XML")
        return
    raiz = arvore.getroot()
    if etree.QName(raiz).namespace != NS_TIPOS:
        rel.falha("tipos", "[Content_Types].xml com espaço de nome errado")
    for item in raiz:
        if not isinstance(item.tag, str):
            continue
        local = nome_local(item)
        tipo = item.get("ContentType")
        if not tipo:
            rel.falha("tipos", "item %s sem ContentType" % local)
            continue
        if local == "Default":
            ext = (item.get("Extension") or "").lower()
            if not ext:
                rel.falha("tipos", "Default sem Extension")
            elif ext in pac.tipos_default:
                rel.falha("tipos", "Default repetido para a extensão %s" % ext)
            pac.tipos_default[ext] = tipo
        elif local == "Override":
            nome = item.get("PartName") or ""
            if not nome.startswith("/"):
                rel.falha("tipos", "Override com PartName sem barra inicial: %r" % nome)
                nome = "/" + nome
            chave = unquote(nome).lower()
            if chave in pac.tipos_override:
                rel.falha("tipos", "Override repetido para %s" % nome)
            pac.tipos_override[chave] = tipo
    for chave in sorted(pac.tipos_override):
        if not pac.existe(chave[1:]):
            rel.falha("tipos", "Override aponta para parte que não existe: %s" % chave)
    for nome in pac.partes:
        if nome == "[Content_Types].xml":
            continue
        if pac.tipo(nome) is None:
            rel.falha("tipos", "%s sem tipo de conteúdo (falta Override ou Default da extensão)" % nome)


def conferir_relacoes(pac, rel):
    if not pac.existe("_rels/.rels"):
        rel.falha("relacoes", "falta _rels/.rels (relações do pacote)")
    for nome in pac.partes:
        if not nome.lower().endswith(".rels"):
            continue
        origem = origem_dos_rels(nome)
        if origem is None:
            rel.falha("relacoes", "%s fora de uma pasta _rels" % nome)
            continue
        if origem and not pac.existe(origem):
            rel.falha("relacoes", "%s descreve a parte %s, que não existe" % (nome, origem))
        arvore = pac.xml(nome)
        if arvore is None:
            continue
        if etree.QName(arvore.getroot()).namespace != NS_RELS:
            rel.falha("relacoes", "%s com espaço de nome errado" % nome)
        vistos = set()
        for item in arvore.getroot():
            if not isinstance(item.tag, str):
                continue
            ident = item.get("Id")
            if not ident:
                rel.falha("relacoes", "%s: relação sem Id" % nome)
            elif ident in vistos:
                rel.falha("relacoes", "%s: Id %s repetido" % (nome, ident))
            vistos.add(ident)
            if not item.get("Type"):
                rel.falha("relacoes", "%s: %s sem Type" % (nome, ident))
            if (item.get("TargetMode") or "Internal") == "External":
                continue
            bruto = item.get("Target")
            if bruto is None:
                rel.falha("relacoes", "%s: %s sem Target" % (nome, ident))
                continue
            alvo = resolver_alvo(origem or "", bruto)
            if alvo == "":
                rel.aviso("relacoes", "%s: %s com alvo vazio" % (nome, ident))
            elif alvo.startswith(".."):
                rel.falha("relacoes", "%s: %s aponta para fora do pacote (%s)" % (nome, ident, bruto))
            elif not pac.existe(alvo):
                rel.falha("relacoes", "%s: %s aponta para %s, que não existe" % (nome, ident, alvo))


def detectar_formato(pac):
    principal = None
    for _, tipo, alvo, _ in pac.relacoes(""):
        if tipo.endswith(TIPO_DOC_PRINCIPAL) and alvo:
            principal = alvo
            break
    if principal is None:
        return None, None
    ct = (pac.tipo(principal) or "").lower()
    if "wordprocessingml" in ct or "ms-word" in ct:
        return "docx", principal
    if "presentationml" in ct or "ms-powerpoint" in ct:
        return "pptx", principal
    if "spreadsheetml" in ct or "ms-excel" in ct:
        return "xlsx", principal
    arvore = pac.xml(principal)
    if arvore is not None:
        raiz = nome_local(arvore.getroot())
        return {"document": "docx", "presentation": "pptx", "workbook": "xlsx"}.get(raiz), principal
    return None, principal


def conferir_obrigatorias(pac, rel, caminho):
    principais = [r for r in pac.relacoes("") if r[1].endswith(TIPO_DOC_PRINCIPAL)]
    if not principais:
        rel.falha("obrigatorias", "_rels/.rels sem relação officeDocument (documento principal)")
        return None
    if len(principais) > 1:
        rel.falha("obrigatorias", "_rels/.rels com %d relações officeDocument, deve haver uma" % len(principais))
    formato, principal = detectar_formato(pac)
    rel.formato = formato
    if principal and not pac.existe(principal):
        rel.falha("obrigatorias", "documento principal %s não existe" % principal)
        return formato
    ext = os.path.splitext(caminho)[1].lower().lstrip(".")
    familia = {"docx": "docx", "docm": "docx", "dotx": "docx", "dotm": "docx",
               "pptx": "pptx", "pptm": "pptx", "potx": "pptx", "potm": "pptx", "ppsx": "pptx", "ppsm": "pptx",
               "xlsx": "xlsx", "xlsm": "xlsx", "xltx": "xlsx", "xltm": "xlsx"}.get(ext)
    if formato is None:
        rel.falha("obrigatorias", "não reconheci o formato pelo tipo do documento principal")
        return None
    if familia and familia != formato:
        rel.aviso("obrigatorias", "extensão .%s, mas o conteúdo é %s" % (ext, NOMES_FORMATO[formato]))
    arvore = pac.xml(principal)
    if arvore is None:
        return formato
    raiz = arvore.getroot()
    if formato == "docx":
        if nome_local(raiz) != "document":
            rel.falha("obrigatorias", "%s não tem w:document na raiz" % principal)
        elif not any(eh_w(f, "body") for f in raiz):
            rel.falha("obrigatorias", "%s sem w:body" % principal)
    elif formato == "pptx":
        obrigatorias_pptx(pac, rel, principal, raiz)
    elif formato == "xlsx":
        obrigatorias_xlsx(pac, rel, principal, raiz)
    return formato


def _rid(elem):
    return atributo_ns(elem, "id", NS_R)


def _filhos(raiz, nome_lista, nome_item):
    for lista in raiz.iter("{*}" + nome_lista):
        for item in lista.iter("{*}" + nome_item):
            yield item


def obrigatorias_pptx(pac, rel, principal, raiz):
    mestres = list(_filhos(raiz, "sldMasterIdLst", "sldMasterId"))
    if not mestres:
        rel.falha("obrigatorias", "%s sem nenhum slide mestre (sldMasterIdLst)" % principal)
    for m in mestres:
        alvo, _ = pac.alvo_por_id(principal, _rid(m))
        if not alvo or not pac.existe(alvo):
            rel.falha("obrigatorias", "mestre %s sem parte correspondente" % _rid(m))
            continue
        marvore = pac.xml(alvo)
        if marvore is None:
            continue
        for lid in _filhos(marvore.getroot(), "sldLayoutIdLst", "sldLayoutId"):
            lalvo, _ = pac.alvo_por_id(alvo, _rid(lid))
            if not lalvo or not pac.existe(lalvo):
                rel.falha("obrigatorias", "%s: layout %s sem parte correspondente" % (alvo, _rid(lid)))
                continue
            if not any(t.endswith("/slideMaster") for _, t, _, _ in pac.relacoes(lalvo)):
                rel.falha("obrigatorias", "%s sem relação com o slide mestre" % lalvo)
    for sid in _filhos(raiz, "sldIdLst", "sldId"):
        alvo, _ = pac.alvo_por_id(principal, _rid(sid))
        if not alvo or not pac.existe(alvo):
            rel.falha("obrigatorias", "slide id %s (%s) sem parte correspondente" % (sid.get("id"), _rid(sid)))
            continue
        tipo = pac.tipo(alvo) or ""
        if not tipo.endswith("presentationml.slide+xml"):
            rel.falha("obrigatorias", "%s está na lista de slides mas tem tipo %s" % (alvo, tipo or "nenhum"))
        layouts = [a for _, t, a, _ in pac.relacoes(alvo) if t.endswith("/slideLayout")]
        if len(layouts) != 1:
            rel.falha("obrigatorias", "%s precisa de exatamente uma relação de layout, tem %d" % (alvo, len(layouts)))
    for nid in _filhos(raiz, "notesMasterIdLst", "notesMasterId"):
        alvo, _ = pac.alvo_por_id(principal, _rid(nid))
        if not alvo or not pac.existe(alvo):
            rel.falha("obrigatorias", "mestre de notas %s sem parte correspondente" % _rid(nid))


def obrigatorias_xlsx(pac, rel, principal, raiz):
    abas = list(_filhos(raiz, "sheets", "sheet"))
    if not abas:
        rel.falha("obrigatorias", "%s sem nenhuma aba" % principal)
    usa_compartilhado = False
    for aba in abas:
        alvo, _ = pac.alvo_por_id(principal, _rid(aba))
        if not alvo or not pac.existe(alvo):
            rel.falha("obrigatorias", "aba %r sem parte correspondente" % aba.get("name"))
            continue
        arvore = pac.xml(alvo)
        if arvore is not None and not usa_compartilhado:
            usa_compartilhado = any(c.get("t") == "s" for c in arvore.getroot().iter("{*}c"))
    if usa_compartilhado:
        tem = any(t.endswith("/sharedStrings") and a and pac.existe(a) for _, t, a, _ in pac.relacoes(principal))
        if not tem:
            rel.falha("obrigatorias", "há células de texto compartilhado (t=\"s\") e falta a parte sharedStrings")


def _repetidos(valores):
    vistos, rep = set(), []
    for v in valores:
        if v in vistos and v not in rep:
            rep.append(v)
        vistos.add(v)
    return rep


def _partes_por_tipo(pac, final):
    return [p for p in pac.partes if (pac.tipo(p) or "").endswith(final)]


def ids_pptx(pac, rel, principal):
    arvore = pac.xml(principal)
    if arvore is None:
        return
    raiz = arvore.getroot()
    slides = list(_filhos(raiz, "sldIdLst", "sldId"))
    ids = [s.get("id") for s in slides]
    for r in _repetidos(ids):
        rel.falha("ids", "%s: id de slide %s repetido" % (principal, r))
    for r in _repetidos([_rid(s) for s in slides]):
        rel.falha("ids", "%s: dois slides usam a mesma relação %s" % (principal, r))
    for v in ids:
        try:
            n = int(v)
        except (TypeError, ValueError):
            rel.falha("ids", "%s: id de slide inválido %r" % (principal, v))
            continue
        if not 256 <= n <= 2147483647:
            rel.falha("ids", "%s: id de slide %s fora da faixa 256 a 2147483647" % (principal, v))
    ids_mestres = [m.get("id") for m in _filhos(raiz, "sldMasterIdLst", "sldMasterId")]
    for m in _filhos(raiz, "sldMasterIdLst", "sldMasterId"):
        alvo, _ = pac.alvo_por_id(principal, _rid(m))
        marvore = pac.xml(alvo) if alvo else None
        if marvore is not None:
            ids_mestres += [l.get("id") for l in _filhos(marvore.getroot(), "sldLayoutIdLst", "sldLayoutId")]
    for r in _repetidos([i for i in ids_mestres if i is not None]):
        rel.falha("ids", "id %s repetido entre mestres e layouts" % r)
    finais = ("presentationml.slide+xml", "presentationml.slideLayout+xml",
              "presentationml.slideMaster+xml", "presentationml.notesSlide+xml",
              "presentationml.notesMaster+xml", "presentationml.handoutMaster+xml")
    for parte in pac.partes:
        if not (pac.tipo(parte) or "").endswith(finais):
            continue
        a = pac.xml(parte)
        if a is None:
            continue
        formas = [e.get("id") for e in a.getroot().iter("{*}cNvPr")
                  if etree.QName(e).namespace in NS_P and not dentro_de_fallback(e)]
        # Em slide reprova. Em layout, mestre e notas só avisa: o próprio
        # LibreOffice grava layout com id de forma repetido e o PowerPoint abre.
        no_slide = (pac.tipo(parte) or "").endswith("presentationml.slide+xml")
        for r in _repetidos(formas):
            (rel.falha if no_slide else rel.aviso)("ids", "%s: id de forma %s repetido" % (parte, r))
    for parte in _partes_por_tipo(pac, "presentationml.commentAuthors+xml"):
        a = pac.xml(parte)
        if a is not None:
            for r in _repetidos([e.get("id") for e in a.getroot().iter("{*}cmAuthor")]):
                rel.falha("ids", "%s: autor de comentário %s repetido" % (parte, r))
    for parte in _partes_por_tipo(pac, "presentationml.comments+xml"):
        a = pac.xml(parte)
        if a is not None:
            chaves = [(e.get("authorId"), e.get("idx")) for e in a.getroot().iter("{*}cm")]
            for r in _repetidos(chaves):
                rel.falha("ids", "%s: comentário autor %s índice %s repetido" % (parte, r[0], r[1]))


def _ids_w(raiz, nome):
    return [atributo_w(e, "id") for e in raiz.iter() if eh_w(e, nome)]


def ids_docx(pac, rel, principal):
    corpo = [p for p in pac.partes if (pac.tipo(p) or "").endswith(
        ("document.main+xml", "template.main+xml", "macroEnabled.main+xml",
         "macroEnabledTemplate.main+xml", "wordprocessingml.header+xml",
         "wordprocessingml.footer+xml", "wordprocessingml.footnotes+xml",
         "wordprocessingml.endnotes+xml"))]
    arvores = {p: pac.xml(p) for p in corpo}
    arvores = {p: a for p, a in arvores.items() if a is not None}

    comentarios = set()
    for parte in _partes_por_tipo(pac, "wordprocessingml.comments+xml"):
        a = pac.xml(parte)
        if a is None:
            continue
        ids = _ids_w(a.getroot(), "comment")
        for r in _repetidos(ids):
            rel.falha("ids", "%s: comentário id %s repetido" % (parte, r))
        comentarios.update(ids)
    for parte, a in arvores.items():
        for nome in ("commentRangeStart", "commentRangeEnd", "commentReference"):
            for i in _ids_w(a.getroot(), nome):
                if i not in comentarios:
                    rel.falha("ids", "%s: %s id %s sem comentário correspondente" % (parte, nome, i))
        for r in _repetidos(_ids_w(a.getroot(), "commentRangeStart")):
            rel.falha("ids", "%s: início de comentário id %s repetido" % (parte, r))
        for r in _repetidos(_ids_w(a.getroot(), "bookmarkStart")):
            rel.aviso("ids", "%s: marcador (bookmark) id %s repetido" % (parte, r))

    for tipo_nota, final in (("footnote", "footnotes+xml"), ("endnote", "endnotes+xml")):
        existentes = set()
        for parte in _partes_por_tipo(pac, "wordprocessingml." + final):
            a = pac.xml(parte)
            if a is None:
                continue
            ids = _ids_w(a.getroot(), tipo_nota)
            for r in _repetidos(ids):
                rel.falha("ids", "%s: nota id %s repetida" % (parte, r))
            existentes.update(ids)
        for parte, a in arvores.items():
            for i in _ids_w(a.getroot(), tipo_nota + "Reference"):
                if i not in existentes:
                    rel.falha("ids", "%s: referência a nota %s que não existe" % (parte, i))

    estilos = set()
    for parte in _partes_por_tipo(pac, "wordprocessingml.styles+xml"):
        a = pac.xml(parte)
        if a is None:
            continue
        ids = [atributo_w(e, "styleId") for e in a.getroot() if eh_w(e, "style")]
        for r in _repetidos(ids):
            rel.falha("ids", "%s: estilo %s repetido" % (parte, r))
        estilos.update(ids)
    if estilos:
        for parte, a in arvores.items():
            usados = set()
            for e in a.getroot().iter():
                if eh_w(e) and nome_local(e) in ("pStyle", "rStyle", "tblStyle"):
                    usados.add(atributo_w(e, "val"))
            for u in sorted(x for x in usados if x and x not in estilos):
                rel.aviso("ids", "%s: usa o estilo %s, que não está em styles.xml" % (parte, u))

    for parte in _partes_por_tipo(pac, "wordprocessingml.numbering+xml"):
        a = pac.xml(parte)
        if a is None:
            continue
        raiz = a.getroot()
        abstratos = [atributo_w(e, "abstractNumId") for e in raiz if eh_w(e, "abstractNum")]
        nums = [atributo_w(e, "numId") for e in raiz if eh_w(e, "num")]
        for r in _repetidos(abstratos):
            rel.falha("ids", "%s: abstractNumId %s repetido" % (parte, r))
        for r in _repetidos(nums):
            rel.falha("ids", "%s: numId %s repetido" % (parte, r))

    for parte, a in arvores.items():
        docpr = [e.get("id") for e in a.getroot().iter("{*}docPr") if not dentro_de_fallback(e)]
        for r in _repetidos(docpr):
            rel.aviso("ids", "%s: id de desenho (docPr) %s repetido" % (parte, r))


def ids_xlsx(pac, rel, principal):
    arvore = pac.xml(principal)
    if arvore is None:
        return
    raiz = arvore.getroot()
    abas = list(_filhos(raiz, "sheets", "sheet"))
    nomes = [(a.get("name") or "") for a in abas]
    for r in _repetidos([n.lower() for n in nomes]):
        rel.falha("ids", "aba %r repetida (o Excel não diferencia maiúscula)" % r)
    for r in _repetidos([a.get("sheetId") for a in abas]):
        rel.falha("ids", "sheetId %s repetido" % r)
    for n in nomes:
        if not n or len(n) > 31 or any(c in n for c in "[]:*?/\\"):
            rel.falha("ids", "nome de aba inválido %r (1 a 31 caracteres, sem []:*?/\\)" % n)
    definidos = [((d.get("name") or "").lower(), d.get("localSheetId")) for d in raiz.iter("{*}definedName")]
    for r in _repetidos(definidos):
        rel.falha("ids", "nome definido %r repetido no mesmo escopo" % r[0])
    tabelas = []
    for parte in _partes_por_tipo(pac, "spreadsheetml.table+xml"):
        a = pac.xml(parte)
        if a is not None:
            tabelas.append(a.getroot())
    for r in _repetidos([t.get("id") for t in tabelas]):
        rel.falha("ids", "id de tabela %s repetido" % r)
    for r in _repetidos([(t.get("displayName") or t.get("name") or "").lower() for t in tabelas]):
        rel.falha("ids", "nome de tabela %r repetido" % r)


# ---------------------------------------------------------------- texto e autor

def _visivel(mudanca, autor):
    """Na leitura 'alterações do autor rejeitadas, as dos outros aceitas'."""
    local = nome_local(mudanca)
    do_autor = atributo_w(mudanca, "author") == autor
    if local in MUDANCA_INSERE:
        return not do_autor
    if local in MUDANCA_APAGA:
        return do_autor
    return True


def _marca_visivel(props, autor):
    """props é rPr do parágrafo, trPr ou rPr do trecho; devolve se o item aparece."""
    if props is None:
        return True
    for filho in props:
        if eh_w(filho) and nome_local(filho) in MUDANCA_CONTEUDO:
            return _visivel(filho, autor)
    return True


def _filho_w(elem, nome):
    for f in elem:
        if eh_w(f, nome):
            return f
    return None


def _primeira_escolha(alternativa):
    escolhas = [f for f in alternativa if isinstance(f.tag, str) and etree.QName(f).namespace == NS_MC]
    for f in escolhas:
        if etree.QName(f).localname == "Choice":
            return f
    for f in escolhas:
        if etree.QName(f).localname == "Fallback":
            return f
    return None


def _oculto_por_ancestral(par, autor):
    filho = par
    for anc in par.iterancestors():
        if not isinstance(anc.tag, str):
            filho = anc
            continue
        q = etree.QName(anc)
        if q.namespace == NS_MC and q.localname == "AlternateContent":
            if _primeira_escolha(anc) is not filho:
                return True
        elif q.namespace in NS_W:
            if q.localname in MUDANCA_CONTEUDO and not _visivel(anc, autor):
                return True
            if q.localname == "tr" and not _marca_visivel(_filho_w(anc, "trPr"), autor):
                return True
            if q.localname == "r" and not _marca_visivel(_filho_w(anc, "rPr"), autor):
                return True
        filho = anc
    return False


def _texto_do_paragrafo(par, autor):
    pedacos = []

    def andar(elem):
        for f in elem:
            if not isinstance(f.tag, str):
                continue
            q = etree.QName(f)
            if q.namespace == NS_MC and q.localname == "AlternateContent":
                escolha = _primeira_escolha(f)
                if escolha is not None:
                    andar(escolha)
                continue
            if q.namespace not in NS_W:
                andar(f)
                continue
            nome = q.localname
            if nome in ("p", "tbl") or nome in PROPRIEDADES:
                continue
            if nome in MUDANCA_CONTEUDO:
                if _visivel(f, autor):
                    andar(f)
            elif nome == "r":
                if _marca_visivel(_filho_w(f, "rPr"), autor):
                    andar(f)
            elif nome in ("t", "delText"):
                pedacos.append(f.text or "")
            elif nome == "tab":
                pedacos.append("\t")
            elif nome in ("br", "cr"):
                pedacos.append("\n")
            elif nome == "noBreakHyphen":
                pedacos.append("-")
            else:
                andar(f)

    andar(par)
    return "".join(pedacos)


def texto_com_autor_rejeitado(raiz, autor):
    """Texto da parte com as alterações de `autor` rejeitadas e as dos outros aceitas."""
    linhas, atual = [], ""
    for par in raiz.iter():
        if not eh_w(par, "p") or _oculto_por_ancestral(par, autor):
            continue
        atual += _texto_do_paragrafo(par, autor)
        ppr = _filho_w(par, "pPr")
        marca = _filho_w(ppr, "rPr") if ppr is not None else None
        if _marca_visivel(marca, autor):
            linhas.append(atual)
            atual = ""
    if atual:
        linhas.append(atual)
    return linhas


def _partes_de_texto_docx(pac):
    finais = ("document.main+xml", "template.main+xml", "macroEnabled.main+xml",
              "macroEnabledTemplate.main+xml", "wordprocessingml.header+xml",
              "wordprocessingml.footer+xml", "wordprocessingml.footnotes+xml",
              "wordprocessingml.endnotes+xml")
    return sorted(p for p in pac.partes if (pac.tipo(p) or "").endswith(finais))


def _assinaturas_mudancas(pac):
    """Percorre (parte, elemento) de toda alteração rastreada do pacote."""
    for parte in pac.partes:
        if not pac.parece_xml(parte):
            continue
        a = pac.xml(parte)
        if a is None:
            continue
        for e in a.getroot().iter():
            if eh_w(e) and nome_local(e) in MUDANCA_TODAS and (
                    atributo_w(e, "author") is not None or atributo_w(e, "id") is not None):
                yield parte, e


def conferir_autor(pac, rel, autor, pac_original):
    rel.usadas.add("autor")
    if rel.formato != "docx":
        rel.aviso("autor", "--autor só vale para Word, ignorado")
        return
    do_original = set()
    if pac_original is not None:
        for parte, e in _assinaturas_mudancas(pac_original):
            do_original.add((parte.lower(), nome_local(e), atributo_w(e, "id"),
                             atributo_w(e, "author"), atributo_w(e, "date")))
    for parte, e in _assinaturas_mudancas(pac):
        quem = atributo_w(e, "author")
        if quem == autor:
            continue
        chave = (parte.lower(), nome_local(e), atributo_w(e, "id"), quem, atributo_w(e, "date"))
        if chave in do_original:
            continue
        if quem is None:
            rel.falha("autor", "%s: w:%s id %s sem autor" % (parte, nome_local(e), atributo_w(e, "id")))
        else:
            rel.falha("autor", "%s: w:%s id %s do autor %r, esperado %r" % (
                parte, nome_local(e), atributo_w(e, "id"), quem, autor))
    if pac_original is None:
        rel.aviso("autor", "sem --original, o texto não foi comparado")
        return
    novas = {p.lower(): p for p in _partes_de_texto_docx(pac)}
    velhas = {p.lower(): p for p in _partes_de_texto_docx(pac_original)}
    for chave in sorted(set(novas) | set(velhas)):
        a_nova = pac.xml(novas[chave]) if chave in novas else None
        a_velha = pac_original.xml(velhas[chave]) if chave in velhas else None
        t_nova = texto_com_autor_rejeitado(a_nova.getroot(), autor) if a_nova is not None else []
        t_velha = texto_com_autor_rejeitado(a_velha.getroot(), autor) if a_velha is not None else []
        if t_nova == t_velha:
            continue
        nome = novas.get(chave) or velhas.get(chave)
        diferentes = sum(1 for _ in difflib.ndiff(t_velha, t_nova) if _[:1] in "+-")
        rel.falha("autor", "%s: texto sem as alterações de %r difere do original em %d linha(s); "
                  "há mudança sem marca de revisão" % (nome, autor, diferentes))
        trecho = list(difflib.unified_diff(t_velha, t_nova, "original", "novo sem as alterações", lineterm="", n=0))
        rel.diferenca_texto.extend(trecho[:20])
        if len(trecho) > 20:
            rel.diferenca_texto.append("... (%d linhas de diferença omitidas)" % (len(trecho) - 20))


# ---------------------------------------------------------------- comparação

def forma_normal(pac, nome):
    dados = pac.ler(nome)
    if pac.parece_xml(nome):
        try:
            arvore = comum.ler_xml(dados)
        except etree.XMLSyntaxError:
            return dados
        comum.tirar_recuo(arvore.getroot())
        return etree.tostring(arvore, method="c14n")
    return dados


def comparar(pac, pac_original):
    novas = {p.lower(): p for p in pac.partes}
    velhas = {p.lower(): p for p in pac_original.partes}
    res = {"acrescentadas": sorted(novas[k] for k in set(novas) - set(velhas)),
           "removidas": sorted(velhas[k] for k in set(velhas) - set(novas)),
           "mudadas": [], "iguais": 0}
    for k in sorted(set(novas) & set(velhas)):
        try:
            igual = forma_normal(pac, novas[k]) == forma_normal(pac_original, velhas[k])
        except Exception:
            igual = False
        if igual:
            res["iguais"] += 1
        else:
            res["mudadas"].append(novas[k])
    return res


# ---------------------------------------------------------------- orquestração

def _estrutura(zf, caminho):
    rel = Relato(caminho)
    conferir_zip(zf, rel)
    pac = Pacote(zf)
    rel.total_partes = len(pac.partes)
    conferir_tipos(pac, rel)
    conferir_xml(pac, rel)
    conferir_relacoes(pac, rel)
    formato = conferir_obrigatorias(pac, rel, caminho)
    _, principal = detectar_formato(pac)
    if principal and pac.existe(principal):
        {"docx": ids_docx, "pptx": ids_pptx, "xlsx": ids_xlsx}.get(formato, lambda *a: None)(pac, rel, principal)
    return rel, pac


def conferir(caminho, original=None, autor=None):
    """Confere o arquivo e devolve um Relato. Importável por outros scripts."""
    comum.exigir_lxml()
    zf, motivo = comum.abrir_zip(caminho)
    if zf is None:
        rel = Relato(caminho)
        rel.falha("zip", motivo)
        return rel
    with zf:
        rel, pac = _estrutura(zf, caminho)
        pac_original = None
        zo = None
        if original:
            zo, motivo_o = comum.abrir_zip(original)
            if zo is None:
                rel.aviso("zip", "original não abriu, comparação não feita: %s" % motivo_o)
            else:
                rel_o, pac_original = _estrutura(zo, original)
                ja_havia = set(rel_o.todas_falhas())
                for cat, msg in list(rel.todas_falhas()):
                    if (cat, msg) in ja_havia:
                        rel.falhas[cat].remove(msg)
                        rel.herdadas.append((cat, msg))
                rel.comparacao = comparar(pac, pac_original)
                rel.nome_original = os.path.basename(original)
        try:
            if autor is not None:
                conferir_autor(pac, rel, autor, pac_original)
        finally:
            if zo is not None:
                zo.close()
    return rel


def main(argv=None):
    leitor = argparse.ArgumentParser(
        description="Confere a estrutura interna de docx, pptx e xlsx.")
    leitor.add_argument("arquivo", help="o arquivo a conferir")
    leitor.add_argument("--original", help="arquivo de origem para comparar (o modelo ou a versão anterior)")
    leitor.add_argument("--autor", help="nome do autor das alterações rastreadas (só Word)")
    args = leitor.parse_args(argv)
    if args.autor is not None and not args.autor.strip():
        print("--autor não pode ser vazio", file=sys.stderr)
        return comum.SAIDA_ARGUMENTO
    comum.exigir_lxml()
    for caminho in [args.arquivo] + ([args.original] if args.original else []):
        if not os.path.isfile(caminho):
            print("arquivo não encontrado: %s" % caminho, file=sys.stderr)
            return comum.SAIDA_FALTA
    rel = conferir(args.arquivo, args.original, args.autor)
    print(rel.texto())
    return comum.SAIDA_REPROVOU if rel.reprovou else comum.SAIDA_OK


if __name__ == "__main__":
    sys.exit(main())
