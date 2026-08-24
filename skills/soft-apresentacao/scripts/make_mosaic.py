#!/usr/bin/env python3
import argparse
import math
from pathlib import Path

from PIL import Image, ImageOps


def natural_key(path: Path):
    return [int(part) if part.isdigit() else part.lower() for part in __import__("re").split(r"(\d+)", path.name)]


parser = argparse.ArgumentParser(description="Monta um mosaico 16:9 a partir dos slides PNG.")
parser.add_argument("input_dir", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("--columns", type=int, default=4)
parser.add_argument("--width", type=int, default=480)
parser.add_argument("--gap", type=int, default=12)
args = parser.parse_args()

slides = sorted(args.input_dir.glob("*.png"), key=natural_key)
if not slides:
    raise SystemExit(f"Nenhum PNG em {args.input_dir}")

thumb_w = args.width
thumb_h = round(thumb_w * 9 / 16)
rows = math.ceil(len(slides) / args.columns)
canvas_w = args.columns * thumb_w + (args.columns + 1) * args.gap
canvas_h = rows * thumb_h + (rows + 1) * args.gap
canvas = Image.new("RGB", (canvas_w, canvas_h), "#121212")

for index, path in enumerate(slides):
    image = Image.open(path).convert("RGB")
    thumb = ImageOps.fit(image, (thumb_w, thumb_h), Image.Resampling.LANCZOS)
    x = args.gap + (index % args.columns) * (thumb_w + args.gap)
    y = args.gap + (index // args.columns) * (thumb_h + args.gap)
    canvas.paste(thumb, (x, y))

args.output.parent.mkdir(parents=True, exist_ok=True)
canvas.save(args.output, "PNG", optimize=True)
print(f"{len(slides)} slides -> {args.output} ({canvas_w}x{canvas_h})")
