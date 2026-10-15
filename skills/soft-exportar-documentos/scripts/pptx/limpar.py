#!/usr/bin/env python3
"""Limpa uma apresentação desempacotada: tira o que ninguém usa mais.

Uso:
    python3 limpar.py PASTA_DESEMPACOTADA [--simular]

A PASTA é o .pptx descompactado (unzip ou desempacotar.py). O script:
  1. apaga os slides que estão na pasta mas fora da lista oficial
     (p:sldIdLst em ppt/presentation.xml), com a relação deles;
  2. tira da lista de seções e das apresentações personalizadas as entradas
     de slides que não estão mais na lista;
  3. percorre as relações a partir de _rels/.rels e apaga toda parte que
     nada alcança: notas de slide apagado, mídia sem uso, gráficos soltos,
     layouts e masters que nenhuma relação cita (layout ligado ao master fica);
  4. tira relações que apontam para arquivo inexistente (relações órfãs) e
     arquivos .rels de parte que não existe mais;
  5. acerta [Content_Types].xml: tira Override de parte apagada e acrescenta
     Default para extensão de mídia que ficou sem tipo.

Imprime cada coisa removida. Rodar duas vezes não muda mais nada.
Com --simular, só mostra o que faria, sem gravar.

Códigos de saída: 0 terminou, 1 XML quebrado na pasta, 2 argumento errado,
3 falta a pasta ou parte obrigatória ou a biblioteca lxml.
"""
import argparse
import os
import posixpath
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    from lxml import etree
except ImportError:
    print("Falta a biblioteca lxml. Instale com: pip install lxml", file=sys.stderr)
    sys.exit(3)

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NS_P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"

TIPOS_POR_EXTENSAO = {
    "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif",
    "bmp": "image/bmp", "tif": "image/tiff", "tiff": "image/tiff", "svg": "image/svg+xml",
    "emf": "image/x-emf", "wmf": "image/x-wmf", "wdp": "image/vnd.ms-photo",
    "mp4": "video/mp4", "m4v": "video/mp4", "mov": "video/quicktime", "avi": "video/x-msvideo",
    "wmv": "video/x-ms-wmv", "mp3": "audio/mpeg", "m4a": "audio/mp4", "wav": "audio/wav",
    "wma": "audio/x-ms-wma", "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "bin": "application/vnd.openxmlformats-officedocument.oleObject",
    "fntdata": "application/x-fontdata", "odttf": "application/vnd.openxmlformats-officedocument.obfuscatedFont",
    "rels": "application/vnd.openxmlformats-package.relationships+xml", "xml": "application/xml",
}

PARSER = etree.XMLParser(remove_blank_text=False, resolve_entities=False, no_network=True, huge_tree=True)

# Elementos que só servem de atalho (hiperlink) e podem sair sem quebrar o slide.
ATALHOS = {f"{{{NS_A}}}hlinkClick", f"{{{NS_A}}}hlinkHover", f"{{{NS_A}}}hlinkMouseOver"}


def caminho_rels(parte):
    """ppt/slides/slide1.xml vira ppt/slides/_rels/slide1.xml.rels; a raiz ('') vira _rels/.rels."""
    pasta, nome = posixpath.split(parte)
    return posixpath.join(pasta, "_rels", nome + ".rels")


def parte_dos_rels(rels):
    """Caminho inverso: de ppt/slides/_rels/slide1.xml.rels volta para ppt/slides/slide1.xml."""
    pasta, nome = posixpath.split(rels)
    acima = posixpath.dirname(pasta)
    return posixpath.join(acima, nome[:-len(".rels")]) if nome != ".rels" else ""


def resolver(origem, alvo):
    alvo = unquote(alvo.split("#", 1)[0])
    if alvo.startswith("/"):
        return posixpath.normpath(alvo.lstrip("/"))
    return posixpath.normpath(posixpath.join(posixpath.dirname(origem), alvo))


class Pacote:
    def __init__(self, raiz, simular):
        self.raiz = Path(raiz)
        self.simular = simular
        self.cache = {}
        self.sujos = set()
        self.apagados = set()
        self.relatorio = []
        self.avisos = []

    def existe(self, parte):
        return parte not in self.apagados and (self.raiz / parte).is_file()

    def xml(self, parte):
        if parte not in self.cache:
            try:
                self.cache[parte] = etree.parse(str(self.raiz / parte), PARSER)
            except etree.XMLSyntaxError as e:
                print(f"XML quebrado em {parte}: {e}", file=sys.stderr)
                sys.exit(1)
        return self.cache[parte]

    def marcar(self, parte):
        self.sujos.add(parte)

    def apagar(self, parte, motivo):
        if parte in self.apagados or not (self.raiz / parte).is_file():
            return
        self.apagados.add(parte)
        self.cache.pop(parte, None)
        self.sujos.discard(parte)
        self.relatorio.append(f"removido: {parte} ({motivo})")
        r = caminho_rels(parte)
        if (self.raiz / r).is_file() and r not in self.apagados:
            self.apagados.add(r)
            self.cache.pop(r, None)
            self.sujos.discard(r)
            self.relatorio.append(f"removido: {r} (relações de parte removida)")

    def relacoes(self, parte):
        r = caminho_rels(parte)
        if not self.existe(r):
            return []
        return list(self.xml(r).getroot().findall(f"{{{NS_REL}}}Relationship"))

    def tirar_relacao(self, parte, rel, motivo):
        """Tira a relação e trata quem cita o rId dela dentro da parte."""
        rid = rel.get("Id")
        rel.getparent().remove(rel)
        self.marcar(caminho_rels(parte))
        self.relatorio.append(f"relação removida: {rid} de {parte or '(raiz)'} ({motivo})")
        if not parte or not parte.endswith(".xml") or not self.existe(parte):
            return
        arv = self.xml(parte)
        for el in list(arv.getroot().iter()):
            if not isinstance(el.tag, str):
                continue
            citado = [k for k, v in el.attrib.items() if k.startswith(f"{{{NS_R}}}") and v == rid]
            if not citado:
                continue
            if el.tag in ATALHOS:
                el.getparent().remove(el)
                self.marcar(parte)
                self.relatorio.append(f"hiperlink removido em {parte} (apontava para {rid})")
            else:
                self.avisos.append(f"atenção: {etree.QName(el).localname} em {parte} ainda cita {rid}, confira à mão")

    def todas_as_partes(self):
        partes = set()
        for caminho in self.raiz.rglob("*"):
            if not caminho.is_file():
                continue
            rel = caminho.relative_to(self.raiz).as_posix()
            if rel == "[Content_Types].xml" or rel.endswith(".rels"):
                continue
            if rel not in self.apagados:
                partes.add(rel)
        return partes

    def gravar(self):
        if self.simular:
            return
        for parte in sorted(self.sujos):
            if parte in self.apagados:
                continue
            self.cache[parte].write(str(self.raiz / parte), xml_declaration=True,
                                    encoding="UTF-8", standalone=True)
        for parte in sorted(self.apagados):
            alvo = self.raiz / parte
            if alvo.is_file():
                alvo.unlink()
        # Pastas que ficaram vazias saem também.
        for pasta in sorted((p for p in self.raiz.rglob("*") if p.is_dir()), key=lambda p: -len(p.parts)):
            try:
                pasta.rmdir()
            except OSError:
                pass


def limpar(pac):
    pres = "ppt/presentation.xml"
    if not pac.existe(pres) or not pac.existe("[Content_Types].xml") or not pac.existe("_rels/.rels"):
        print("A pasta não parece um .pptx desempacotado (falta ppt/presentation.xml, "
              "_rels/.rels ou [Content_Types].xml).", file=sys.stderr)
        sys.exit(3)

    raiz_pres = pac.xml(pres).getroot()
    rels_pres = {r.get("Id"): r for r in pac.relacoes(pres)}
    lista = raiz_pres.find(f"{{{NS_P}}}sldIdLst")
    entradas = list(lista) if lista is not None else []

    # 1. Lista oficial: quem está nela, e entradas que apontam para o nada.
    rids_listados, ids_listados, partes_listadas = set(), set(), set()
    for sld in entradas:
        rid = sld.get(f"{{{NS_R}}}id")
        rel = rels_pres.get(rid)
        alvo = resolver(pres, rel.get("Target")) if rel is not None else None
        if alvo is None or not pac.existe(alvo):
            lista.remove(sld)
            pac.marcar(pres)
            pac.relatorio.append(f"entrada removida da lista de slides: id {sld.get('id')} ({rid} sem arquivo)")
            continue
        rids_listados.add(rid)
        ids_listados.add(sld.get("id"))
        partes_listadas.add(alvo)

    for rid, rel in rels_pres.items():
        if rel.get("Type", "").endswith("/slide") and rid not in rids_listados:
            pac.tirar_relacao(pres, rel, "slide fora da lista")

    fora = set()
    for parte in pac.todas_as_partes():
        if posixpath.dirname(parte) == "ppt/slides" and parte.endswith(".xml") and parte not in partes_listadas:
            fora.add(parte)

    # 2. Seções e apresentações personalizadas.
    for sec_sld in list(raiz_pres.iter(f"{{{NS_P14}}}sldId")):
        if sec_sld.get("id") not in ids_listados:
            sec_sld.getparent().remove(sec_sld)
            pac.marcar(pres)
            pac.relatorio.append(f"entrada de seção removida: slide id {sec_sld.get('id')}")
    for cs_sld in list(raiz_pres.iter(f"{{{NS_P}}}sld")):
        if cs_sld.get(f"{{{NS_R}}}id") not in rids_listados:
            cs_sld.getparent().remove(cs_sld)
            pac.marcar(pres)
            pac.relatorio.append(f"slide removido de apresentação personalizada: {cs_sld.get(f'{{{NS_R}}}id')}")

    # 3. Percorre as relações a partir da raiz.
    alcancadas = set()
    fila = [""]
    vistos = {""}
    while fila:
        origem = fila.pop()
        for rel in pac.relacoes(origem):
            if rel.get("TargetMode") == "External":
                continue
            alvo = resolver(origem, rel.get("Target", ""))
            if alvo in fora:
                pac.tirar_relacao(origem, rel, f"apontava para {alvo}, slide fora da lista")
                continue
            if not pac.existe(alvo):
                pac.tirar_relacao(origem, rel, f"alvo inexistente {alvo}")
                continue
            alcancadas.add(alvo)
            if alvo not in vistos:
                vistos.add(alvo)
                fila.append(alvo)

    for parte in sorted(fora):
        pac.apagar(parte, "slide fora da lista")
    for parte in sorted(pac.todas_as_partes() - alcancadas):
        pasta = posixpath.dirname(parte)
        if "notesSlide" in parte:
            motivo = "notas sem slide"
        elif "media" in pasta:
            motivo = "mídia sem uso"
        elif "slideLayout" in parte:
            motivo = "layout sem uso"
        elif "slideMaster" in parte:
            motivo = "master sem uso"
        else:
            motivo = "parte que nada cita"
        pac.apagar(parte, motivo)

    # 4. Arquivos .rels sem a parte dona.
    for caminho in sorted(pac.raiz.rglob("*.rels")):
        rels = caminho.relative_to(pac.raiz).as_posix()
        if rels in pac.apagados or "/_rels/" not in "/" + rels:
            continue
        dona = parte_dos_rels(rels)
        if dona and not pac.existe(dona):
            pac.apagados.add(rels)
            pac.cache.pop(rels, None)
            pac.sujos.discard(rels)
            pac.relatorio.append(f"removido: {rels} (relações de parte que não existe)")

    # 5. Tipos de conteúdo.
    ct = "[Content_Types].xml"
    tipos = pac.xml(ct).getroot()
    existentes = pac.todas_as_partes()
    existentes_min = {p.lower() for p in existentes}
    for ov in list(tipos.findall(f"{{{NS_CT}}}Override")):
        nome = ov.get("PartName", "").lstrip("/")
        if unquote(nome).lower() not in existentes_min:
            tipos.remove(ov)
            pac.marcar(ct)
            pac.relatorio.append(f"tipo de conteúdo removido: /{nome} (parte não existe)")
    defaults = {d.get("Extension", "").lower() for d in tipos.findall(f"{{{NS_CT}}}Default")}
    overrides = {unquote(o.get("PartName", "").lstrip("/")).lower() for o in tipos.findall(f"{{{NS_CT}}}Override")}
    for parte in sorted(existentes):
        ext = posixpath.splitext(parte)[1].lstrip(".").lower()
        if parte.lower() in overrides or ext in defaults:
            continue
        if ext in TIPOS_POR_EXTENSAO:
            novo = etree.Element(f"{{{NS_CT}}}Default", Extension=ext, ContentType=TIPOS_POR_EXTENSAO[ext])
            ultimo_default = tipos.findall(f"{{{NS_CT}}}Default")
            if ultimo_default:
                ultimo_default[-1].addnext(novo)
            else:
                tipos.insert(0, novo)
            defaults.add(ext)
            pac.marcar(ct)
            pac.relatorio.append(f"tipo de conteúdo acrescentado: extensão .{ext}")
        else:
            pac.avisos.append(f"atenção: {parte} não tem tipo de conteúdo declarado")


def main():
    ap = argparse.ArgumentParser(description="Remove slides fora da lista, relações órfãs e partes sem uso "
                                             "de um .pptx desempacotado.")
    ap.add_argument("pasta", help="pasta com o .pptx descompactado")
    ap.add_argument("--simular", action="store_true", help="só mostra o que removeria, sem gravar")
    a = ap.parse_args()
    if not Path(a.pasta).is_dir():
        print(f"Pasta não encontrada: {a.pasta}", file=sys.stderr)
        return 3
    pac = Pacote(a.pasta, a.simular)
    limpar(pac)
    pac.gravar()
    for linha in pac.relatorio:
        print(linha)
    for linha in pac.avisos:
        print(linha)
    removidas = sum(1 for l in pac.relatorio if l.startswith("removido:"))
    if not pac.relatorio:
        print("Nada a remover: a apresentação já está limpa.")
    else:
        prefixo = "Simulação: " if a.simular else ""
        print(f"{prefixo}{removidas} arquivo(s) removido(s), {len(pac.relatorio) - removidas} ajuste(s) em XML.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
