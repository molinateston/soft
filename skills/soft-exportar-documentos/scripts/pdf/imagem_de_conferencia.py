#!/usr/bin/env python3
"""Desenha as caixas de um campos.json sobre a pagina, para conferir a olho.

Uso:
    imagem_de_conferencia.py ENTRADA.pdf campos.json --pagina N -o imagem.png
                             [--dpi 100] [--sem-nomes]

Renderiza a pagina N com o pdftoppm e desenha cada caixa daquela pagina com
cor por tipo, mais o nome do campo:
  azul texto, verde rotulo, vermelho caixa_selecao, laranja radio,
  roxo lista e lista_suspensa, cinza botao, marrom assinatura.
Aceita os dois formatos de campos.json (veja o LEIA-ME-pdf.md).

Saida: 0 ok, 2 argumento errado, 3 falta dependencia ou arquivo,
4 o pdftoppm falhou.
"""

import argparse
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comum as c  # noqa: E402

CORES = {
    "texto": (0, 102, 204),
    "rotulo": (0, 150, 70),
    "caixa_selecao": (210, 30, 30),
    "radio": (230, 120, 0),
    "lista": (140, 50, 170),
    "lista_suspensa": (140, 50, 170),
    "botao": (110, 110, 110),
    "assinatura": (140, 90, 40),
}
COR_OUTRO = (220, 0, 160)


def fonte(ImageFont, tamanho):
    try:
        return ImageFont.load_default(size=tamanho)
    except TypeError:  # Pillow antigo, sem tamanho
        return ImageFont.load_default()


def renderizar(entrada, pagina, dpi, pasta):
    c.exigir_programa("pdftoppm")
    prefixo = os.path.join(pasta, "pagina")
    c.rodar(["pdftoppm", "-f", str(pagina), "-l", str(pagina), "-r", str(dpi),
             "-png", "-singlefile", entrada, prefixo])
    caminho = prefixo + ".png"
    if not os.path.isfile(caminho):
        c.sair("O pdftoppm nao gerou a imagem da pagina.", c.EXTERNO)
    return caminho


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Desenha as caixas de um campos.json sobre a pagina do PDF.")
    ap.add_argument("entrada", help="PDF")
    ap.add_argument("campos", help="campos.json")
    ap.add_argument("--pagina", type=int, required=True, help="pagina, a partir de 1")
    ap.add_argument("-o", "--saida", required=True, help="PNG de saida")
    ap.add_argument("--dpi", type=int, default=100, help="resolucao da imagem (padrao 100)")
    ap.add_argument("--sem-nomes", action="store_true", help="desenha so as caixas")
    args = ap.parse_args(argv)
    if args.dpi <= 0:
        c.sair("--dpi precisa ser maior que zero.", c.ARGUMENTO)

    Image, ImageDraw, ImageFont = c.exigir_pillow()
    leitor = c.abrir_pdf(args.entrada)
    total = len(leitor.pages)
    if not 1 <= args.pagina <= total:
        c.sair(f"Pagina {args.pagina} nao existe; o PDF tem {total}.", c.ARGUMENTO)
    caixas, erros = c.ler_caixas(c.ler_json(args.campos))
    if erros:
        c.sair("campos.json fora do formato:\n  " + "\n  ".join(erros), c.ARGUMENTO)
    info = c.info_pagina(leitor.pages[args.pagina - 1])
    escala = args.dpi / 72.0

    with tempfile.TemporaryDirectory(prefix="conferencia-") as pasta:
        img = Image.open(renderizar(args.entrada, args.pagina, args.dpi, pasta)).convert("RGB")
        img.load()
    desenho = ImageDraw.Draw(img, "RGBA")
    letra = fonte(ImageFont, max(10, int(9 * escala)))
    espessura = max(1, round(escala))
    usados = {}
    desenhadas = 0
    for cx in caixas:
        if cx["pagina"] != args.pagina:
            continue
        r = cx["ret"]
        topo = (c.ret_pdf_para_topo(info, r) if cx["sistema"] == "pdf"
                else [min(r[0], r[2]), min(r[1], r[3]), max(r[0], r[2]), max(r[1], r[3])])
        x0, y0, x1, y1 = (v * escala for v in topo)
        cor = CORES.get(cx["tipo"], COR_OUTRO)
        usados[cx["tipo"]] = cor
        desenho.rectangle([x0, y0, x1, y1], fill=cor + (40,), outline=cor + (255,),
                          width=espessura)
        desenhadas += 1
        if not args.sem_nomes:
            nome = cx["nome"]
            caixa_txt = desenho.textbbox((0, 0), nome, font=letra)
            alt_txt = caixa_txt[3] - caixa_txt[1]
            ty = y0 - alt_txt - 3 if y0 - alt_txt - 3 >= 0 else y1 + 2
            fundo = desenho.textbbox((x0, ty), nome, font=letra)
            desenho.rectangle([fundo[0] - 1, fundo[1] - 1, fundo[2] + 1, fundo[3] + 1],
                              fill=(255, 255, 255, 210))
            desenho.text((x0, ty), nome, fill=cor + (255,), font=letra)

    # legenda no canto de cima a direita
    if usados:
        linhas = sorted(usados.items())
        alt_linha = desenho.textbbox((0, 0), "Ag", font=letra)[3] + 4
        larg = max(desenho.textbbox((0, 0), t, font=letra)[2] for t, _ in linhas) + 24
        x = img.width - larg - 8
        y = 8
        desenho.rectangle([x - 4, y - 4, x + larg, y + alt_linha * len(linhas)],
                          fill=(255, 255, 255, 220), outline=(0, 0, 0, 120))
        for tipo, cor in linhas:
            desenho.rectangle([x, y + 2, x + 12, y + alt_linha - 6], fill=cor + (255,))
            desenho.text((x + 18, y), tipo, fill=(0, 0, 0, 255), font=letra)
            y += alt_linha

    try:
        img.save(args.saida, "PNG")
    except OSError as e:
        c.sair(f"Nao consegui gravar {args.saida}: {e}", c.DEPENDENCIA)
    print(f"{desenhadas} caixas desenhadas na pagina {args.pagina}, imagem em {args.saida}")
    if desenhadas == 0:
        print("Aviso: o campos.json nao tem caixa nesta pagina.")
    return c.OK


if __name__ == "__main__":
    sys.exit(main())
