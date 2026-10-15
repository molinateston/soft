#!/usr/bin/env python3
"""Extrai a estrutura de um PDF sem campos: texto com caixa e desenhos.

Uso:
    estrutura.py ENTRADA.pdf [-o estrutura.json] [--sem-palavras] [--sem-desenhos]

Para cada pagina: tamanho (ja girada, como aparece), blocos de texto com
linhas e palavras e suas caixas (do pdftotext -bbox-layout), e o que foi
desenhado com traco: linhas horizontais e verticais (onde se escreve),
quadradinhos (provaveis caixas de marcacao) e retangulos maiores.

Coordenadas em pontos, origem no canto de cima a esquerda da pagina como
ela aparece: [esquerda, topo, direita, base]. E o mesmo sistema "topo" do
campos.json do preencher_texto.py. Formato completo no LEIA-ME-pdf.md.

Saida: 0 ok, 2 argumento errado, 3 falta pypdf, pdftotext ou o arquivo,
4 o pdftotext falhou.
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comum as c  # noqa: E402

PINTAR = {"S", "s", "f", "F", "f*", "B", "B*", "b", "b*"}
LIMITE_XOBJETO = 5


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _caixa(el):
    return [c.r2(el.get(k)) for k in ("xMin", "yMin", "xMax", "yMax")]


def ler_texto(caminho, com_palavras):
    """Roda o pdftotext -bbox-layout e devolve a lista de blocos por pagina."""
    c.exigir_programa("pdftotext")
    r = c.rodar(["pdftotext", "-bbox-layout", caminho, "-"])
    try:
        raiz = ET.fromstring(r.stdout)
    except ET.ParseError as e:
        c.sair(f"Nao entendi a saida do pdftotext: {e}", c.EXTERNO)
    paginas = []
    for pag in raiz.iter():
        if _local(pag.tag) != "page":
            continue
        blocos = []
        for bl in pag.iter():
            if _local(bl.tag) != "block":
                continue
            linhas = []
            for ln in bl:
                if _local(ln.tag) != "line":
                    continue
                palavras = [{"texto": (w.text or ""), "caixa": _caixa(w)}
                            for w in ln if _local(w.tag) == "word"]
                linha = {"texto": " ".join(p["texto"] for p in palavras),
                         "caixa": _caixa(ln)}
                if com_palavras:
                    linha["palavras"] = palavras
                linhas.append(linha)
            blocos.append({"caixa": _caixa(bl), "linhas": linhas})
        paginas.append(blocos)
    return paginas


# ------------------------------------------------------------- desenhos

def _mult(m1, m2):
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return [a1 * a2 + b1 * c2, a1 * b2 + b1 * d2,
            c1 * a2 + d1 * c2, c1 * b2 + d1 * d2,
            e1 * a2 + f1 * c2 + e2, e1 * b2 + f1 * d2 + f2]


def _ponto(m, x, y):
    return m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]


def desenhos_da_pagina(leitor, pagina):
    """Varre o fluxo de desenho e devolve retangulos e segmentos no espaco do PDF."""
    from pypdf.generic import ContentStream
    retangulos, segmentos = [], []

    def varrer(conteudo, recursos, ctm, nivel):
        try:
            ops = ContentStream(conteudo, leitor).operations
        except Exception:
            return
        pilha = []
        caminho_rets, caminho_subs = [], []
        atual = None
        for operandos, op in ops:
            op = op.decode("latin-1") if isinstance(op, bytes) else str(op)
            try:
                nums = [float(v) for v in operandos]
            except (TypeError, ValueError):
                nums = []
            if op == "q":
                pilha.append(ctm)
            elif op == "Q":
                ctm = pilha.pop() if pilha else ctm
            elif op == "cm" and len(nums) == 6:
                ctm = _mult(nums, ctm)
            elif op == "re" and len(nums) == 4:
                x, y, w, h = nums
                cantos = [_ponto(ctm, x, y), _ponto(ctm, x + w, y),
                          _ponto(ctm, x + w, y + h), _ponto(ctm, x, y + h)]
                caminho_rets.append(cantos)
                atual = None
            elif op == "m" and len(nums) == 2:
                atual = [_ponto(ctm, *nums)]
                caminho_subs.append(atual)
            elif op == "l" and len(nums) == 2 and atual is not None:
                atual.append(_ponto(ctm, *nums))
            elif op in ("c", "v", "y"):
                if atual is not None:
                    atual.append(None)  # curva: o subcaminho deixa de ser reto
                    if len(nums) >= 2:
                        atual.append(_ponto(ctm, nums[-2], nums[-1]))
            elif op in PINTAR or op == "n":
                if op != "n":
                    retangulos.extend(caminho_rets)
                    for sub in caminho_subs:
                        segmentos.append(sub)
                caminho_rets, caminho_subs, atual = [], [], None
            elif op == "Do" and operandos and nivel < LIMITE_XOBJETO and recursos is not None:
                xobjs = recursos.get("/XObject")
                if xobjs is None:
                    continue
                xo = xobjs.get_object().get(operandos[0])
                if xo is None:
                    continue
                xo = xo.get_object()
                if xo.get("/Subtype") != "/Form":
                    continue
                matriz = [float(v) for v in xo.get("/Matrix", [1, 0, 0, 1, 0, 0])]
                sub_rec = xo.get("/Resources")
                varrer(xo, sub_rec.get_object() if sub_rec is not None else recursos,
                       _mult(matriz, ctm), nivel + 1)

    conteudo = pagina.get_contents()
    if conteudo is None:
        return [], []
    rec = pagina.get("/Resources")
    varrer(conteudo, rec.get_object() if rec is not None else None,
           [1, 0, 0, 1, 0, 0], 0)
    return retangulos, segmentos


def _eh_retangulo_alinhado(pontos):
    if None in pontos:
        return False
    if len(pontos) == 5 and abs(pontos[0][0] - pontos[4][0]) < 0.5 and abs(pontos[0][1] - pontos[4][1]) < 0.5:
        pontos = pontos[:4]
    if len(pontos) != 4:
        return False
    for i in range(4):
        a, b = pontos[i], pontos[(i + 1) % 4]
        if abs(a[0] - b[0]) > 0.5 and abs(a[1] - b[1]) > 0.5:
            return False
    return True


def classificar(info, retangulos, segmentos):
    """Separa em linhas horizontais, verticais, quadradinhos e retangulos (sistema topo)."""
    horiz, vert, quad, rets = [], [], [], []
    vistos = set()

    def guardar(lista, caixa):
        chave = (id(lista),) + tuple(round(v, 1) for v in caixa)
        if chave not in vistos:
            vistos.add(chave)
            lista.append({"caixa": [c.r2(v) for v in caixa]})

    def caixa_de(pontos):
        xs = [p[0] for p in pontos]
        ys = [p[1] for p in pontos]
        return c.ret_pdf_para_topo(info, [min(xs), min(ys), max(xs), max(ys)])

    formas = list(retangulos)
    for sub in segmentos:
        if _eh_retangulo_alinhado(sub):
            formas.append(sub[:4])
            continue
        anterior = None
        for p in sub:
            if p is None:
                anterior = None
                continue
            if anterior is not None:
                cx = caixa_de([anterior, p])
                w, h = cx[2] - cx[0], cx[3] - cx[1]
                if h <= 0.5 and w >= 10:
                    guardar(horiz, cx)
                elif w <= 0.5 and h >= 10:
                    guardar(vert, cx)
            anterior = p
    for f in formas:
        cx = caixa_de(f)
        w, h = cx[2] - cx[0], cx[3] - cx[1]
        if h <= 2 and w >= 10:
            guardar(horiz, cx)
        elif w <= 2 and h >= 10:
            guardar(vert, cx)
        elif 5 <= w <= 25 and 5 <= h <= 25 and abs(w - h) <= max(2.0, 0.2 * max(w, h)):
            guardar(quad, cx)
        elif w >= 10 and h >= 10:
            guardar(rets, cx)
    ordem = lambda d: (d["caixa"][1], d["caixa"][0])  # noqa: E731
    return {"linhas_horizontais": sorted(horiz, key=ordem),
            "linhas_verticais": sorted(vert, key=ordem),
            "quadrados": sorted(quad, key=ordem),
            "retangulos": sorted(rets, key=ordem)}


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Extrai texto com caixas e desenhos de um PDF sem campos.")
    ap.add_argument("entrada", help="arquivo PDF")
    ap.add_argument("-o", "--saida", help="grava o JSON neste arquivo (padrao: tela)")
    ap.add_argument("--sem-palavras", action="store_true",
                    help="nao lista as palavras, so blocos e linhas")
    ap.add_argument("--sem-desenhos", action="store_true",
                    help="nao procura linhas e quadradinhos desenhados")
    args = ap.parse_args(argv)

    leitor = c.abrir_pdf(args.entrada)
    textos = ler_texto(args.entrada, not args.sem_palavras)
    paginas = []
    total_linhas = 0
    for i, pag in enumerate(leitor.pages):
        info = c.info_pagina(pag)
        w, h = c.tamanho_exibido(info)
        blocos = textos[i] if i < len(textos) else []
        total_linhas += sum(len(b["linhas"]) for b in blocos)
        item = {"pagina": i + 1, "largura": c.r2(w), "altura": c.r2(h),
                "giro": info["giro"], "blocos": blocos}
        if not args.sem_desenhos:
            rets, segs = desenhos_da_pagina(leitor, pag)
            item.update(classificar(info, rets, segs))
        paginas.append(item)

    dados = {"arquivo": os.path.basename(args.entrada), "sistema": "topo",
             "unidade": "pt", "paginas": paginas}
    c.gravar_json(dados, args.saida)
    if args.saida:
        print(f"{len(paginas)} paginas, {total_linhas} linhas de texto, gravado em {args.saida}",
              file=sys.stderr)
    if total_linhas == 0:
        print("Aviso: nenhum texto encontrado. Se o PDF for escaneado, use para_imagens.py "
              "e estime as posicoes pela imagem.", file=sys.stderr)
    return c.OK


if __name__ == "__main__":
    sys.exit(main())
