#!/usr/bin/env python3
"""make_mosaic.py: monta o mosaico 16:9 dos PNGs dos slides, com o número de
cada slide no canto. Deck longo sai em folhas (padrão: 24 slides por folha):
mosaico.png quando cabe numa folha; senão mosaico-1.png, mosaico-2.png...

  python3 scripts/make_mosaic.py <pasta-dos-png> <saida.png> [--por-folha 24] [--columns 4]
"""
import argparse
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def natural_key(path: Path):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


def fonte(tam):
    try:
        return ImageFont.load_default(size=tam)
    except TypeError:  # Pillow antigo: fonte bitmap, sem tamanho
        return ImageFont.load_default()


def folha(slides, inicio, cols, thumb_w, gap, destino):
    """Uma folha do mosaico; o número de cada slide fica numa faixa acima da miniatura, fora do desenho."""
    thumb_h = round(thumb_w * 9 / 16)
    faixa = 30
    rows = math.ceil(len(slides) / cols)
    canvas = Image.new("RGB", (cols * thumb_w + (cols + 1) * gap, rows * (thumb_h + faixa) + (rows + 1) * gap), "#121212")
    desenho = ImageDraw.Draw(canvas)
    f = fonte(24)
    for i, path in enumerate(slides):
        thumb = ImageOps.fit(Image.open(path).convert("RGB"), (thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = gap + (i % cols) * (thumb_w + gap)
        y = gap + (i // cols) * (thumb_h + faixa + gap)
        desenho.text((x + 2, y + 2), str(inicio + i), fill="#FFFFFF", font=f)
        canvas.paste(thumb, (x, y + faixa))
    destino.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destino, "PNG", optimize=True)
    return canvas.size


def main():
    ap = argparse.ArgumentParser(description="Mosaico 16:9 dos slides, em folhas.")
    ap.add_argument("input_dir", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--columns", type=int, default=4)
    ap.add_argument("--width", type=int, default=480)
    ap.add_argument("--gap", type=int, default=12)
    ap.add_argument("--por-folha", type=int, default=24)
    a = ap.parse_args()
    slides = sorted(a.input_dir.glob("*.png"), key=natural_key)
    if not slides:
        raise SystemExit(f"Nenhum PNG em {a.input_dir}")
    for velho in a.output.parent.glob(f"{a.output.stem}-*.png"):
        velho.unlink()
    n = max(1, a.por_folha)
    if len(slides) <= n:
        w, h = folha(slides, 1, a.columns, a.width, a.gap, a.output)
        print(f"{len(slides)} slides -> {a.output} ({w}x{h})")
        return
    for k in range(0, len(slides), n):
        destino = a.output.with_name(f"{a.output.stem}-{k // n + 1}{a.output.suffix}")
        w, h = folha(slides[k:k + n], k + 1, a.columns, a.width, a.gap, destino)
        print(f"slides {k + 1} a {min(k + n, len(slides))} -> {destino} ({w}x{h})")
    if a.output.exists():
        a.output.unlink()


if __name__ == "__main__":
    main()
