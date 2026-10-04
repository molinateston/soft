#!/usr/bin/env python3
"""
danfse.py - PDF de representação da NFS-e, gerado a partir do XML autorizado.

O documento fiscal é o XML. Este PDF só representa o que está nele, com um QR
que leva à consulta pública da chave (formato da NT 008: tpc=1 e chave=). Segue
pontos da NT 008 (chave em bloco único de 50 dígitos, marca CANCELADA ou
SUBSTITUÍDA, expressão de sem validade jurídica no ambiente de teste) sem
reproduzir o leiaute completo do DANFSe. Quando a situação não foi consultada,
o PDF diz isso.

Dependências: fpdf2 e qrcode (com Pillow). Sem elas, gerar_pdf levanta
FaltaDependencia com o comando de instalação, e a nota segue válida pelo XML.
"""
from decimal import Decimal

URL_CONSULTA = "https://www.nfse.gov.br/ConsultaPublica/?tpc=1&chave={chave}"
RET_ISS = {"1": "ISS não retido", "2": "ISS retido pelo tomador",
           "3": "ISS retido pelo intermediário"}
TROCAS = {"\u2014": "-", "\u2013": "-", "\u201c": '"', "\u201d": '"', "\u2018": "'",
          "\u2019": "'", "\u2026": "...", "\u2022": "-", "\u00a0": " "}


class FaltaDependencia(Exception):
    pass


def url_consulta(chave):
    return URL_CONSULTA.format(chave=chave)


def _l1(s):
    s = "".join(TROCAS.get(c, c) for c in str(s if s is not None else ""))
    return s.encode("latin-1", "replace").decode("latin-1")


def brl(v):
    if v in (None, ""):
        return "-"
    q = Decimal(str(v)).quantize(Decimal("0.01"))
    inteiro, frac = f"{abs(q):.2f}".split(".")
    inteiro = f"{int(inteiro):,}".replace(",", ".")
    return f"{'-' if q < 0 else ''}R$ {inteiro},{frac}"


def fmt_doc(d):
    d = str(d or "")
    if len(d) == 14:
        return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"
    if len(d) == 11:
        return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"
    return d or "-"


def fmt_data(iso):
    if not iso:
        return "-"
    data = str(iso)[:10]
    partes = data.split("-")
    return f"{partes[2]}/{partes[1]}/{partes[0]}" if len(partes) == 3 else str(iso)


def _qr_png(url):
    import qrcode
    q = qrcode.QRCode(border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url)
    q.make(fit=True)
    img = q.make_image(fill_color="black", back_color="white")
    return img.get_image() if hasattr(img, "get_image") else img._img


def gerar_pdf(info, saida, situacao=None):
    """info: dict de dps.ler_nfse. situacao: {'cancelada': bool|None, 'conferida_em': str}."""
    try:
        from fpdf import FPDF
        import qrcode  # noqa: F401
    except ImportError:
        raise FaltaDependencia("faltam fpdf2 e qrcode. Instale com: "
                               "python3 -m pip install --user fpdf2 qrcode pillow") from None
    situacao = situacao or {}
    url = url_consulta(info["chave"])
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(True, 15)
    pdf.set_title(_l1(f"NFS-e {info.get('numero') or ''}"))
    pdf.set_creator("nfse-emissao")
    pdf.add_page()
    larg = pdf.w - pdf.l_margin - pdf.r_margin
    marca = "CANCELADA" if situacao.get("cancelada") else (
        "SUBSTITUÍDA" if situacao.get("substituida") else None)
    if marca:
        pdf.set_text_color(235, 180, 180)
        pdf.set_font("Helvetica", "B", 72)
        with pdf.rotation(35, x=pdf.w / 2, y=pdf.h / 2):
            pdf.text(pdf.w / 2 - pdf.get_string_width(_l1(marca)) / 2, pdf.h / 2, _l1(marca))
        pdf.set_text_color(0, 0, 0)
        pdf.set_xy(pdf.l_margin, pdf.t_margin)

    def titulo(txt):
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(larg, 6, _l1(txt), new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.set_font("Helvetica", "", 9)

    def linha(rotulo, valor):
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(45, 5, _l1(rotulo))
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(larg - 45, 5, _l1(valor if valor not in (None, "") else "-"),
                       new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(larg, 8, _l1("NFS-e  Nota Fiscal de Serviço Eletrônica"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(larg, 5, _l1("Representação em PDF do XML autorizado (padrão nacional)"),
             new_x="LMARGIN", new_y="NEXT")

    if str(info.get("tpAmb")) == "2":
        pdf.set_text_color(170, 0, 0)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(larg, 7, _l1("NFS-e SEM VALIDADE JURÍDICA (produção restrita, ambiente de teste)"),
                 new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
    if marca:
        pdf.set_text_color(200, 0, 0)
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(larg, 10, _l1(f"NOTA {marca}"), new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(larg, 5, _l1(f"Evento registrado na consulta de eventos de "
                              f"{situacao.get('conferida_em', '-')}"),
                 new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.set_text_color(0, 0, 0)

    titulo("Identificação")
    linha("Número da NFS-e", info.get("numero"))
    linha("Processada em", info.get("processada_em"))
    linha("Competência", fmt_data(info.get("competencia")))
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(45, 5, _l1("Chave de acesso"))
    pdf.set_font("Courier", "", 9)
    pdf.cell(larg - 45, 5, _l1(info.get("chave")), new_x="LMARGIN", new_y="NEXT")

    titulo("Prestador")
    linha("Nome", info.get("prestador_nome"))
    linha("CNPJ", fmt_doc(info.get("prestador_cnpj")))
    linha("Inscrição municipal", info.get("prestador_im"))
    linha("Município", info.get("municipio_emissor"))

    titulo("Tomador")
    linha("Nome", info.get("tomador_nome"))
    linha("CNPJ/CPF", fmt_doc(info.get("tomador_doc")))

    titulo("Serviço")
    linha("Código nacional", " ".join(x for x in (info.get("cTribNac"),
                                                  info.get("trib_nacional_desc")) if x))
    linha("Local da prestação", info.get("local_prestacao"))
    linha("Descrição", info.get("descricao"))

    titulo("Valores")
    linha("Valor do serviço", brl(info.get("valor_servico")))
    linha("Retenção", RET_ISS.get(str(info.get("retencao_iss")), info.get("retencao_iss")))
    if info.get("valor_iss"):
        linha("ISS", brl(info.get("valor_iss")))
    if info.get("valor_liquido"):
        linha("Valor líquido", brl(info.get("valor_liquido")))

    titulo("Autenticidade")
    y = pdf.get_y() + 2
    pdf.image(_qr_png(url), x=pdf.l_margin, y=y, w=38, h=38)
    pdf.set_xy(pdf.l_margin + 42, y)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(larg - 42, 5, _l1("Consulte a nota na consulta pública nacional pelo QR "
                                     "ou pelo endereço:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.l_margin + 42)
    pdf.set_font("Courier", "", 7)
    pdf.multi_cell(larg - 42, 4, _l1(url), new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(max(pdf.get_y(), y + 40))

    if situacao.get("cancelada") is None:
        situ = "Situação de cancelamento não consultada para este PDF."
    elif marca:
        situ = f"Nota {marca.lower()} conforme a consulta de eventos."
    else:
        situ = f"Sem evento de cancelamento na consulta de {situacao.get('conferida_em', '-')}."
    pdf.set_font("Helvetica", "I", 8)
    pdf.multi_cell(larg, 4, _l1(f"{situ} O documento fiscal é o XML autorizado; este PDF é "
                                "só a representação dele."), new_x="LMARGIN", new_y="NEXT")
    pdf.output(str(saida))
    return saida
