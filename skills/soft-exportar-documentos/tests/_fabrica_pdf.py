"""Gera os PDFs de teste da pasta pdf/ com pypdf, sem reportlab.

criar_formulario: PDF com campos AcroForm de todos os tipos, inclusive
campos aninhados (pai com filhos que herdam o tipo).
criar_chapado: PDF sem campos, com rotulos de texto, linhas e quadradinhos.
"""

from pypdf import PdfWriter
from pypdf.generic import (ArrayObject, BooleanObject, DecodedStreamObject,
                           DictionaryObject, FloatObject, NameObject,
                           NumberObject, TextStringObject)

N = NameObject


def _fonte(w):
    return w._add_object(DictionaryObject({
        N("/Type"): N("/Font"), N("/Subtype"): N("/Type1"),
        N("/BaseFont"): N("/Helvetica"), N("/Encoding"): N("/WinAnsiEncoding")}))


def _conteudo(w, pagina, dados, fonte):
    s = DecodedStreamObject()
    s.set_data(dados)
    pagina[N("/Contents")] = w._add_object(s)
    pagina[N("/Resources")] = DictionaryObject({
        N("/Font"): DictionaryObject({N("/F1"): fonte})})


def _form(w, dados, larg, alt):
    s = DecodedStreamObject()
    s.set_data(dados)
    s.update({N("/Type"): N("/XObject"), N("/Subtype"): N("/Form"),
              N("/BBox"): ArrayObject([FloatObject(0), FloatObject(0),
                                       FloatObject(larg), FloatObject(alt)])})
    return w._add_object(s)


def _rect(*v):
    return ArrayObject([FloatObject(x) for x in v])


def criar_formulario(caminho):
    w = PdfWriter()
    p1 = w.add_blank_page(612, 792)
    p2 = w.add_blank_page(612, 792)
    fonte = _fonte(w)
    _conteudo(w, p1, b"BT /F1 12 Tf 72 700 Td (Nome:) Tj ET\n"
                     b"BT /F1 12 Tf 72 660 Td (Rua:) Tj ET", fonte)
    _conteudo(w, p2, b"BT /F1 12 Tf 72 700 Td (Segunda pagina) Tj ET", fonte)
    ref_p1, ref_p2 = p1.indirect_reference, p2.indirect_reference
    campos = ArrayObject()
    anots1, anots2 = ArrayObject(), ArrayObject()
    da = TextStringObject("/Helv 10 Tf 0 g")

    def widget(extra, pagina_ref, lista):
        d = DictionaryObject({N("/Type"): N("/Annot"), N("/Subtype"): N("/Widget"),
                              N("/F"): NumberObject(4), N("/P"): pagina_ref})
        d.update(extra)
        ref = w._add_object(d)
        lista.append(ref)
        return ref, d

    # texto simples com tamanho maximo
    ref, _ = widget({N("/FT"): N("/Tx"), N("/T"): TextStringObject("nome"),
                     N("/Rect"): _rect(120, 695, 400, 715), N("/DA"): da,
                     N("/MaxLen"): NumberObject(40),
                     N("/TU"): TextStringObject("Nome completo")}, ref_p1, anots1)
    campos.append(ref)

    # pai "endereco" com filhos de texto que herdam /FT e /DA
    pai = DictionaryObject({N("/T"): TextStringObject("endereco"), N("/FT"): N("/Tx"),
                            N("/DA"): da})
    ref_pai = w._add_object(pai)
    kids = ArrayObject()
    for nome, y in (("rua", 655), ("cidade", 625)):
        r, d = widget({N("/T"): TextStringObject(nome), N("/Parent"): ref_pai,
                       N("/Rect"): _rect(120, y, 400, y + 20)}, ref_p1, anots1)
        kids.append(r)
    pai[N("/Kids")] = kids
    campos.append(ref_pai)

    # caixa de selecao com estado ligado "Sim"
    sim = _form(w, b"0 0 0 rg 2 2 10 10 re f", 14, 14)
    off = _form(w, b"0 0 0 RG 0.5 0.5 13 13 re S", 14, 14)
    ref, _ = widget({N("/FT"): N("/Btn"), N("/T"): TextStringObject("aceito"),
                     N("/Rect"): _rect(120, 590, 134, 604), N("/V"): N("/Off"),
                     N("/AS"): N("/Off"),
                     N("/AP"): DictionaryObject({N("/N"): DictionaryObject(
                         {N("/Sim"): sim, N("/Off"): off})})}, ref_p1, anots1)
    campos.append(ref)

    # grupo de radio "plano" com duas opcoes, na pagina 2
    radio = DictionaryObject({N("/T"): TextStringObject("plano"), N("/FT"): N("/Btn"),
                              N("/Ff"): NumberObject(1 << 15), N("/V"): N("/Off")})
    ref_radio = w._add_object(radio)
    kids = ArrayObject()
    for estado, x in (("Basico", 120), ("Premium", 200)):
        r, d = widget({N("/Parent"): ref_radio, N("/Rect"): _rect(x, 600, x + 14, 614),
                       N("/AS"): N("/Off"),
                       N("/AP"): DictionaryObject({N("/N"): DictionaryObject(
                           {N("/" + estado): sim, N("/Off"): off})})}, ref_p2, anots2)
        kids.append(r)
    radio[N("/Kids")] = kids
    campos.append(ref_radio)

    # lista suspensa e caixa de lista com varias escolhas
    ref, _ = widget({N("/FT"): N("/Ch"), N("/T"): TextStringObject("estado"),
                     N("/Ff"): NumberObject(1 << 17), N("/DA"): da,
                     N("/Opt"): ArrayObject([TextStringObject(x) for x in ("SP", "RJ", "MG")]),
                     N("/Rect"): _rect(120, 550, 250, 570)}, ref_p2, anots2)
    campos.append(ref)
    ref, _ = widget({N("/FT"): N("/Ch"), N("/T"): TextStringObject("interesses"),
                     N("/Ff"): NumberObject(1 << 21), N("/DA"): da,
                     N("/Opt"): ArrayObject([
                         ArrayObject([TextStringObject("a"), TextStringObject("Alfa")]),
                         ArrayObject([TextStringObject("b"), TextStringObject("Beta")])]),
                     N("/Rect"): _rect(120, 470, 250, 530)}, ref_p2, anots2)
    campos.append(ref)

    # botao de apertar
    ref, _ = widget({N("/FT"): N("/Btn"), N("/T"): TextStringObject("enviar"),
                     N("/Ff"): NumberObject(1 << 16),
                     N("/Rect"): _rect(120, 400, 200, 420)}, ref_p2, anots2)
    campos.append(ref)

    p1[N("/Annots")] = anots1
    p2[N("/Annots")] = anots2
    w.root_object[N("/AcroForm")] = w._add_object(DictionaryObject({
        N("/Fields"): campos, N("/DA"): da,
        N("/NeedAppearances"): BooleanObject(False),
        N("/DR"): DictionaryObject({N("/Font"): DictionaryObject({N("/Helv"): fonte})})}))
    with open(caminho, "wb") as f:
        w.write(f)


def criar_chapado(caminho, giro=0):
    """Formulario chapado: rotulos, linhas para escrever e dois quadradinhos."""
    w = PdfWriter()
    p = w.add_blank_page(612, 792)
    if giro:
        p[N("/Rotate")] = NumberObject(giro)
    p2 = w.add_blank_page(612, 792)
    fonte = _fonte(w)
    _conteudo(w, p,
              b"BT /F1 12 Tf 72 700 Td (Nome completo:) Tj ET\n"
              b"0.5 w 170 698 m 540 698 l S\n"
              b"BT /F1 12 Tf 72 660 Td (Cidade:) Tj ET\n"
              b"q 1 0 0 1 120 658 cm 0 0 300 0.8 re f Q\n"
              b"BT /F1 12 Tf 72 620 Td (Aceito os termos) Tj ET\n"
              b"0.8 w 180 618 10 10 re S\n"
              b"BT /F1 12 Tf 200 620 Td (Sim) Tj ET\n", fonte)
    _conteudo(w, p2, b"BT /F1 12 Tf 72 700 Td (Pagina dois) Tj ET", fonte)
    with open(caminho, "wb") as f:
        w.write(f)
