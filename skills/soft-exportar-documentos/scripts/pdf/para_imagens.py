#!/usr/bin/env python3
"""Converte as paginas de um PDF em PNG, uma imagem por pagina.

Uso:
    para_imagens.py ENTRADA.pdf PASTA [--dpi 100] [--prefixo pagina]

Cria a PASTA se faltar e grava pagina-1.png, pagina-2.png... com o numero
preenchido com zeros conforme o total (pagina-01.png ... pagina-12.png),
para a ordem alfabetica ser a ordem das paginas. Imprime os nomes gerados.

Saida: 0 ok, 2 argumento errado, 3 falta pdftoppm ou o arquivo,
4 o pdftoppm falhou.
"""

import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comum as c  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description="Converte as paginas de um PDF em PNG.")
    ap.add_argument("entrada", help="arquivo PDF")
    ap.add_argument("pasta", help="pasta onde as imagens vao ficar")
    ap.add_argument("--dpi", type=int, default=100, help="resolucao (padrao 100)")
    ap.add_argument("--prefixo", default="pagina", help="inicio do nome das imagens")
    args = ap.parse_args(argv)
    if args.dpi <= 0:
        c.sair("--dpi precisa ser maior que zero.", c.ARGUMENTO)
    if not re.fullmatch(r"[\w.-]+", args.prefixo):
        c.sair("--prefixo so pode ter letras, numeros, ponto, hifen e sublinhado.", c.ARGUMENTO)
    c.exigir_arquivo(args.entrada)
    c.exigir_programa("pdftoppm")
    os.makedirs(args.pasta, exist_ok=True)

    antes = set(glob.glob(os.path.join(args.pasta, args.prefixo + "-*.png")))
    c.rodar(["pdftoppm", "-png", "-r", str(args.dpi), args.entrada,
             os.path.join(args.pasta, args.prefixo)], tempo=900)
    padrao = re.compile(re.escape(args.prefixo) + r"-(\d+)\.png$")
    geradas = []
    for caminho in glob.glob(os.path.join(args.pasta, args.prefixo + "-*.png")):
        m = padrao.search(os.path.basename(caminho))
        if m:
            geradas.append((int(m.group(1)), caminho))
    geradas.sort()
    if not geradas:
        c.sair("O pdftoppm nao gerou nenhuma imagem.", c.EXTERNO)
    for _, caminho in geradas:
        print(caminho)
    velhas = antes - {p for _, p in geradas}
    if velhas:
        print(f"Aviso: a pasta ja tinha {len(velhas)} imagens com o mesmo prefixo que "
              "nao sao desta conversao.", file=sys.stderr)
    print(f"{len(geradas)} paginas convertidas a {args.dpi} dpi em {args.pasta}", file=sys.stderr)
    return c.OK


if __name__ == "__main__":
    sys.exit(main())
