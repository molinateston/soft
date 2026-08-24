#!/usr/bin/env python3
import sys
from pathlib import Path
from PIL import Image

folder = Path(sys.argv[1])
expected = int(sys.argv[2]) if len(sys.argv) > 2 else 9
errors = []

for number in range(1, expected + 1):
    path = folder / f"slide-{number:02d}.png"
    if not path.is_file() or path.stat().st_size == 0:
        errors.append(f"ausente ou vazio: {path}")
        continue
    with Image.open(path) as image:
        if image.size != (1080, 1350):
            errors.append(f"dimensão errada {image.size}: {path}")

mosaic = folder / "_mosaico.png"
if not mosaic.is_file() or mosaic.stat().st_size == 0:
    errors.append(f"ausente ou vazio: {mosaic}")

if errors:
    print("REPROVADO")
    print("\n".join(errors))
    raise SystemExit(1)

print(f"APROVADO: {expected} cards 1080x1350 e mosaico presentes em {folder}")
