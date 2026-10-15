#!/usr/bin/env python3
"""Acrescenta um slide numa apresentação desempacotada.

Uso:
    python3 novo_slide.py PASTA_DESEMPACOTADA --de slide2 [--depois slide5]
    python3 novo_slide.py PASTA_DESEMPACOTADA --layout slideLayout3 [--depois slide5]

--de       duplica o slide indicado: copia a parte, as relações, as notas (se
           houver) e os gráficos e diagramas dele (cada cópia fica com os seus).
           Imagens e mídia ficam compartilhadas. Comentários não são copiados.
--layout   cria um slide em branco a partir do layout, com as caixas de texto
           reservadas do layout (título, corpo e afins) vazias.
--depois   põe o slide novo logo depois desse na lista; sem ele, vai para o fim.

Aceita o nome com ou sem .xml, ou só o número: slide2, slide2.xml, 2;
slideLayout3, layout3, 3.

O script registra tudo que o slide novo precisa: a parte em ppt/slides/, a
relação em ppt/_rels/presentation.xml.rels, o tipo em [Content_Types].xml e a
entrada com id novo único em p:sldIdLst. Imprime o identificador novo e a
linha da lista de slides, pronta para colar em outra posição se quiser.

Faça toda a estrutura (somar, apagar, reordenar) antes de escrever o
conteúdo: duplicar depois de editar copia o texto editado.

Códigos de saída: 0 criou, 2 argumento errado, 3 falta pasta, parte ou a
biblioteca lxml, 1 XML quebrado na pasta.
"""
import argparse
import posixpath
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    from lxml import etree
except ImportError:
    print("Falta a biblioteca lxml. Instale com: pip install lxml", file=sys.stderr)
    sys.exit(3)

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NS_P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"

TIPO_REL_SLIDE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
TIPO_REL_LAYOUT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout"
TIPO_CT_SLIDE = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"

# Partes que cada slide precisa ter como suas (o final do tipo da relação).
DUPLICAR = {"notesSlide", "chart", "package", "chartUserShapes", "chartStyle", "chartColorStyle",
            "diagramData", "diagramDrawing", "oleObject"}
# Relações que não fazem sentido na cópia.
DESCARTAR = {"comments"}

PARSER = etree.XMLParser(remove_blank_text=False, resolve_entities=False, no_network=True, huge_tree=True)


def sair(msg, codigo):
    print(msg, file=sys.stderr)
    sys.exit(codigo)


def caminho_rels(parte):
    pasta, nome = posixpath.split(parte)
    return posixpath.join(pasta, "_rels", nome + ".rels")


def resolver(origem, alvo):
    alvo = unquote(alvo.split("#", 1)[0])
    if alvo.startswith("/"):
        return posixpath.normpath(alvo.lstrip("/"))
    return posixpath.normpath(posixpath.join(posixpath.dirname(origem), alvo))


def relativo(origem, alvo):
    return posixpath.relpath(alvo, posixpath.dirname(origem) or ".")


class Pacote:
    def __init__(self, raiz):
        self.raiz = Path(raiz)
        self.cache = {}

    def existe(self, parte):
        return (self.raiz / parte).is_file()

    def xml(self, parte):
        if parte not in self.cache:
            try:
                self.cache[parte] = etree.parse(str(self.raiz / parte), PARSER)
            except etree.XMLSyntaxError as e:
                sair(f"XML quebrado em {parte}: {e}", 1)
        return self.cache[parte]

    def gravar(self, parte, arvore=None):
        arvore = arvore if arvore is not None else self.cache[parte]
        destino = self.raiz / parte
        destino.parent.mkdir(parents=True, exist_ok=True)
        arvore.write(str(destino), xml_declaration=True, encoding="UTF-8", standalone=True)
        self.cache[parte] = arvore

    def tipos(self):
        return self.xml("[Content_Types].xml").getroot()

    def override(self, parte):
        for ov in self.tipos().findall(f"{{{NS_CT}}}Override"):
            if unquote(ov.get("PartName", "")).lstrip("/").lower() == parte.lower():
                return ov.get("ContentType")
        return None

    def por_override(self, parte, tipo):
        raiz = self.tipos()
        if self.override(parte) is None:
            etree.SubElement(raiz, f"{{{NS_CT}}}Override", PartName="/" + parte, ContentType=tipo)

    def nome_livre(self, parte):
        """slide3.xml vira slideN.xml com N acima de todo número usado na pasta e nos tipos."""
        pasta, nome = posixpath.split(parte)
        base, ext = posixpath.splitext(nome)
        prefixo = re.match(r"^(.*?)(\d*)$", base).group(1)
        padrao = re.compile(r"^" + re.escape(prefixo) + r"(\d+)" + re.escape(ext) + r"$", re.I)
        usados = [0]
        d = self.raiz / pasta
        if d.is_dir():
            for f in d.iterdir():
                m = padrao.match(f.name)
                if m:
                    usados.append(int(m.group(1)))
        for ov in self.tipos().findall(f"{{{NS_CT}}}Override"):
            p = unquote(ov.get("PartName", "")).lstrip("/")
            if posixpath.dirname(p) == pasta:
                m = padrao.match(posixpath.basename(p))
                if m:
                    usados.append(int(m.group(1)))
        n = max(usados) + 1
        while self.existe(posixpath.join(pasta, f"{prefixo}{n}{ext}")):
            n += 1
        return posixpath.join(pasta, f"{prefixo}{n}{ext}")


def copiar_parte(pac, parte, trocas, criadas):
    """Copia a parte e, recursivamente, as partes que precisam ser só dela. Devolve o caminho novo."""
    nova = pac.nome_livre(parte)
    shutil.copyfile(pac.raiz / parte, pac.raiz / nova)
    criadas.append(nova)
    tipo = pac.override(parte)
    if tipo:
        pac.por_override(nova, tipo)
    trocas[parte] = nova

    rels = caminho_rels(parte)
    if pac.existe(rels):
        arvore = etree.parse(str(pac.raiz / rels), PARSER)
        for rel in list(arvore.getroot().findall(f"{{{NS_REL}}}Relationship")):
            if rel.get("TargetMode") == "External":
                continue
            final = rel.get("Type", "").rstrip("/").rsplit("/", 1)[-1]
            alvo = resolver(parte, rel.get("Target", ""))
            if final in DESCARTAR:
                arvore.getroot().remove(rel)
                continue
            if alvo in trocas:
                novo_alvo = trocas[alvo]
            elif final in DUPLICAR and pac.existe(alvo):
                novo_alvo = copiar_parte(pac, alvo, trocas, criadas)
            else:
                novo_alvo = alvo
            if novo_alvo != alvo or posixpath.dirname(nova) != posixpath.dirname(parte):
                rel.set("Target", relativo(nova, novo_alvo))
        pac.gravar(caminho_rels(nova), arvore)
    return nova


def slide_em_branco(pac, layout):
    """Monta o XML de um slide vazio com as caixas reservadas do layout."""
    raiz_layout = pac.xml(layout).getroot()
    nsmap = {"a": NS_A, "r": NS_R, "p": NS_P}
    sld = etree.Element(f"{{{NS_P}}}sld", nsmap=nsmap)
    csld = etree.SubElement(sld, f"{{{NS_P}}}cSld")
    arvore = etree.SubElement(csld, f"{{{NS_P}}}spTree")
    nv = etree.SubElement(arvore, f"{{{NS_P}}}nvGrpSpPr")
    etree.SubElement(nv, f"{{{NS_P}}}cNvPr", id="1", name="")
    etree.SubElement(nv, f"{{{NS_P}}}cNvGrpSpPr")
    etree.SubElement(nv, f"{{{NS_P}}}nvPr")
    gp = etree.SubElement(arvore, f"{{{NS_P}}}grpSpPr")
    xf = etree.SubElement(gp, f"{{{NS_A}}}xfrm")
    for tag, at in (("off", ("x", "y")), ("ext", ("cx", "cy")), ("chOff", ("x", "y")), ("chExt", ("cx", "cy"))):
        etree.SubElement(xf, f"{{{NS_A}}}{tag}", {at[0]: "0", at[1]: "0"})

    proximo_id = 2
    arvore_layout = raiz_layout.find(f"{{{NS_P}}}cSld/{{{NS_P}}}spTree")
    caixas = []
    if arvore_layout is not None:
        for sp in arvore_layout.findall(f"{{{NS_P}}}sp"):
            ph = sp.find(f"{{{NS_P}}}nvSpPr/{{{NS_P}}}nvPr/{{{NS_P}}}ph")
            if ph is None or ph.get("type") in ("dt", "ftr", "sldNum"):
                continue
            cnv = sp.find(f"{{{NS_P}}}nvSpPr/{{{NS_P}}}cNvPr")
            nome = cnv.get("name") if cnv is not None and cnv.get("name") else f"Espaço reservado {proximo_id}"
            novo = etree.SubElement(arvore, f"{{{NS_P}}}sp")
            nvsp = etree.SubElement(novo, f"{{{NS_P}}}nvSpPr")
            etree.SubElement(nvsp, f"{{{NS_P}}}cNvPr", id=str(proximo_id), name=nome)
            cnvsp = etree.SubElement(nvsp, f"{{{NS_P}}}cNvSpPr")
            etree.SubElement(cnvsp, f"{{{NS_A}}}spLocks", noGrp="1")
            nvpr = etree.SubElement(nvsp, f"{{{NS_P}}}nvPr")
            novo_ph = etree.SubElement(nvpr, f"{{{NS_P}}}ph")
            for at in ("type", "orient", "sz", "idx"):
                if ph.get(at) is not None:
                    novo_ph.set(at, ph.get(at))
            etree.SubElement(novo, f"{{{NS_P}}}spPr")
            corpo = etree.SubElement(novo, f"{{{NS_P}}}txBody")
            etree.SubElement(corpo, f"{{{NS_A}}}bodyPr")
            etree.SubElement(corpo, f"{{{NS_A}}}lstStyle")
            etree.SubElement(corpo, f"{{{NS_A}}}p")
            caixas.append(ph.get("type", "corpo"))
            proximo_id += 1
    clr = etree.SubElement(sld, f"{{{NS_P}}}clrMapOvr")
    etree.SubElement(clr, f"{{{NS_A}}}masterClrMapping")
    return etree.ElementTree(sld), caixas


def normalizar(valor, pasta, prefixos):
    v = valor.strip().replace("\\", "/")
    v = posixpath.basename(v)
    if v.lower().endswith(".xml"):
        v = v[:-4]
    if v.isdigit():
        v = prefixos[0] + v
    for pre in prefixos:
        m = re.fullmatch(re.escape(pre) + r"(\d+)", v, re.I)
        if m:
            return f"{pasta}/{prefixos[0]}{m.group(1)}.xml"
    return f"{pasta}/{v}.xml"


def main():
    ap = argparse.ArgumentParser(description="Duplica um slide ou cria um a partir de um layout, "
                                             "numa apresentação desempacotada.")
    ap.add_argument("pasta", help="pasta com o .pptx descompactado")
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--de", metavar="slideN", help="slide a duplicar (slide2, slide2.xml ou 2)")
    grupo.add_argument("--layout", metavar="layoutN", help="layout de origem do slide em branco "
                                                            "(slideLayout3, layout3 ou 3)")
    ap.add_argument("--depois", metavar="slideN", help="põe o slide novo depois deste na lista (padrão: no fim)")
    a = ap.parse_args()

    pac = Pacote(a.pasta)
    pres = "ppt/presentation.xml"
    rels_pres = caminho_rels(pres)
    if not Path(a.pasta).is_dir():
        sair(f"Pasta não encontrada: {a.pasta}", 3)
    for obrigatoria in (pres, rels_pres, "[Content_Types].xml"):
        if not pac.existe(obrigatoria):
            sair(f"A pasta não parece um .pptx desempacotado: falta {obrigatoria}.", 3)

    raiz_pres = pac.xml(pres).getroot()
    raiz_rels = pac.xml(rels_pres).getroot()
    alvo_por_rid = {r.get("Id"): resolver(pres, r.get("Target", ""))
                    for r in raiz_rels.findall(f"{{{NS_REL}}}Relationship")}

    lista = raiz_pres.find(f"{{{NS_P}}}sldIdLst")
    ref = None
    if a.depois:
        depois = normalizar(a.depois, "ppt/slides", ["slide"])
        for s in (lista.findall(f"{{{NS_P}}}sldId") if lista is not None else []):
            if alvo_por_rid.get(s.get(f"{{{NS_R}}}id")) == depois:
                ref = s
                break
        if ref is None:
            sair(f"--depois: {depois} não está na lista de slides. Nada foi gravado.", 2)

    criadas = []
    trocas = {}
    if a.de:
        origem = normalizar(a.de, "ppt/slides", ["slide"])
        if not pac.existe(origem):
            sair(f"Slide não encontrado: {origem}", 3)
        novo = copiar_parte(pac, origem, trocas, criadas)
        pac.por_override(novo, pac.override(origem) or TIPO_CT_SLIDE)
        descricao = f"cópia de {posixpath.basename(origem)}"
        caixas = None
    else:
        layout = normalizar(a.layout, "ppt/slideLayouts", ["slideLayout", "layout"])
        if not pac.existe(layout):
            sair(f"Layout não encontrado: {layout}", 3)
        novo = pac.nome_livre("ppt/slides/slide1.xml")
        arvore, caixas = slide_em_branco(pac, layout)
        pac.gravar(novo, arvore)
        criadas.append(novo)
        rels = etree.Element(f"{{{NS_REL}}}Relationships", nsmap={None: NS_REL})
        etree.SubElement(rels, f"{{{NS_REL}}}Relationship", Id="rId1", Type=TIPO_REL_LAYOUT,
                         Target=relativo(novo, layout))
        pac.gravar(caminho_rels(novo), etree.ElementTree(rels))
        pac.por_override(novo, TIPO_CT_SLIDE)
        descricao = f"em branco a partir de {posixpath.basename(layout)}"

    # Relação nova na apresentação.
    numeros = [int(m.group(1)) for rid in alvo_por_rid if (m := re.fullmatch(r"rId(\d+)", rid or ""))]
    n = max(numeros, default=0) + 1
    while f"rId{n}" in alvo_por_rid:
        n += 1
    rid = f"rId{n}"
    etree.SubElement(raiz_rels, f"{{{NS_REL}}}Relationship", Id=rid, Type=TIPO_REL_SLIDE,
                     Target=relativo(pres, novo))

    # Entrada nova na lista, com id único entre 256 e 2147483647.
    if lista is None:
        lista = etree.Element(f"{{{NS_P}}}sldIdLst")
        ancora = None
        for nome in ("handoutMasterIdLst", "notesMasterIdLst", "sldMasterIdLst"):
            ancora = raiz_pres.find(f"{{{NS_P}}}{nome}")
            if ancora is not None:
                break
        if ancora is not None:
            ancora.addnext(lista)
        else:
            raiz_pres.insert(0, lista)
    usados = {int(s.get("id")) for s in raiz_pres.iter(f"{{{NS_P}}}sldId") if (s.get("id") or "").isdigit()}
    novo_id = max(usados | {255}) + 1
    if novo_id > 2147483647:
        novo_id = next(i for i in range(256, 2147483648) if i not in usados)
    entrada = etree.Element(f"{{{NS_P}}}sldId", id=str(novo_id))
    entrada.set(f"{{{NS_R}}}id", rid)

    posicao = "no fim da lista"
    if ref is not None:
        ref.addnext(entrada)
        posicao = f"na lista, depois de {posixpath.basename(depois)}"
    else:
        lista.append(entrada)

    # Com seções (p14:sectionLst), todo slide precisa estar numa seção.
    secao_txt = ""
    secoes = list(raiz_pres.iter(f"{{{NS_P14}}}section"))
    if secoes:
        nova_sec = etree.Element(f"{{{NS_P14}}}sldId", id=str(novo_id))
        colocado = False
        if ref is not None:
            for sec_sld in raiz_pres.iter(f"{{{NS_P14}}}sldId"):
                if sec_sld.get("id") == ref.get("id"):
                    sec_sld.addnext(nova_sec)
                    colocado = True
                    break
        if not colocado:
            ultima = secoes[-1]
            sld_lst = ultima.find(f"{{{NS_P14}}}sldIdLst")
            if sld_lst is None:
                sld_lst = etree.SubElement(ultima, f"{{{NS_P14}}}sldIdLst")
            sld_lst.append(nova_sec)
        secao = nova_sec.getparent().getparent()
        secao_txt = f" (seção '{secao.get('name', '')}')"

    pac.gravar(pres)
    pac.gravar(rels_pres)
    pac.gravar("[Content_Types].xml")

    pre_p = raiz_pres.prefix or "p"
    pre_r = next((k for k, v in raiz_pres.nsmap.items() if v == NS_R and k), "r")
    print(f"Slide novo: {novo} ({descricao})")
    for parte in criadas:
        if parte != novo:
            print(f"  parte copiada junto: {parte}")
    if caixas is not None:
        print(f"  caixas reservadas: {', '.join(caixas) if caixas else 'nenhuma'}")
    print(f"Identificador: id {novo_id}, relação {rid}")
    print(f"Já incluído {posicao}{secao_txt}. Linha da lista de slides (p:sldIdLst):")
    print(f'<{pre_p}:sldId id="{novo_id}" {pre_r}:id="{rid}"/>')
    return 0


if __name__ == "__main__":
    sys.exit(main())
