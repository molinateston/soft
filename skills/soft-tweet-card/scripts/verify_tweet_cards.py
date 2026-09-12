#!/usr/bin/env python3
import re
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

# Verde de acento por card e marcador de pendência no cabeçalho.
# O builder grava o HTML de cada card em _fonte/; sem essa pasta o check
# não roda e o verificador diz isso em vez de fingir que aprovou.
fonte = folder / "_fonte"
verdes = []
if fonte.is_dir():
    for number in range(1, expected + 1):
        origem = fonte / f"slide-{number:02d}.html"
        if not origem.is_file():
            errors.append(f"HTML de origem ausente: {origem}")
            continue
        html = origem.read_text(encoding="utf-8")
        n_kw = len(re.findall(r'class="kw"', html))
        verdes.append(f"slide-{number:02d}: verde por card: {n_kw} (máximo 1)")
        if n_kw > 1:
            errors.append(
                f"verde demais em slide-{number:02d}: {n_kw} trechos de acento, máximo 1")
        cabecalho = re.search(r'<div class="autor">.*?</div>\s*</div>', html, re.S)
        alvo = cabecalho.group(0) if cabecalho else html
        if re.search(r'A\s*CONFIRMAR', alvo, re.I):
            errors.append(
                f"marcador de pendência no cabeçalho de slide-{number:02d}: "
                "nome, handle ou avatar carregam [A CONFIRMAR]")
else:
    # Sem _fonte/ o check de verde por card e de cabeçalho NÃO roda, e o
    # verificador não pode sair aprovado: o número declarado pode até estar
    # certo, mas a prova não existe, e "verde por card: 1" declarado com o
    # verificador em NÃO CONFERIDO é declaração sem lastro.
    errors.append(
        f"verde por card NÃO CONFERIDO: {fonte} não existe; rode o builder "
        "atualizado pra gravar o HTML de origem. Declarar `verde por card: N` "
        "com o verificador nesta condição reprova a entrega")

if verdes:
    print("\n".join(verdes))

if errors:
    print("REPROVADO")
    print("\n".join(errors))
    raise SystemExit(1)

print(f"APROVADO: {expected} cards 1080x1350 e mosaico presentes em {folder}")
