# Auditoria do lote: junta os mosaico.png (um por final, gerados pelo verificar_gif.py) num só PNG, com o nome de cada final em cima.
# Uso: python3 mosaico_geral.py <pasta_verif> <saida.png> [--escala 0.5]
#   <pasta_verif> tem uma subpasta por final (verif/<nome>/mosaico.png). Abra o PNG e olhe todos antes de entregar.
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ap = argparse.ArgumentParser(description='mosaico geral do lote'); ap.add_argument('verif'); ap.add_argument('saida')
ap.add_argument('--escala', type=float, default=0.5); ap.add_argument('--padrao', default='*/mosaico.png')
A = ap.parse_args()
fs = sorted(Path(A.verif).glob(A.padrao)); assert fs, f'nenhum {A.padrao} em {A.verif}'
try: f = ImageFont.truetype('DejaVuSans-Bold.ttf', 30)
except OSError:
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
    except OSError: f = ImageFont.load_default()
ims = [Image.open(p).convert('RGB') for p in fs]
ims = [i.resize((int(i.width * A.escala), int(i.height * A.escala))) for i in ims]
h = max(i.height for i in ims) + 44; w = max(i.width for i in ims)
out = Image.new('RGB', (w, h * len(ims)), (20, 20, 20)); d = ImageDraw.Draw(out)
for k, (p, i) in enumerate(zip(fs, ims)):
    d.text((8, k * h + 6), p.parent.name, font=f, fill=(255, 220, 0)); out.paste(i, (0, k * h + 44))
out.save(A.saida); print(len(fs), 'finais', out.size, A.saida)
