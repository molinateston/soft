# GIF em lote: gera um plano-gif.json (formato de assets/plano-gif-exemplo.json) para cada final do lote (ganchos x normal/espelho).
# Os momentos são escritos UMA vez em quadros da V3 (k0/k1 da V3, ver assets/momentos-v3-exemplo-ep4.json). Em cada final,
# P = quadros do final - corpo e tudo é deslocado por d = P - KG (o corpo da V3 começa no quadro KG e é o mesmo em todos os finais).
# Uso: python3 planos_gif_lote.py --momentos momentos.json --bases '<pasta>/saida/ep4/ep4-*-hlg.mp4' --corpo 1984 --p90 0.0712893 \
#          --saida-dir <pasta>/saida/ep4-gif-meme --trab-dir <pasta>/trab [--kg 120] [--mix voz-sfx-v3.wav] [--sons <skill>/assets/sons-gif]
#   corpo = quadros da V3 final - KG (EP4: 2104 - 120 = 1984; EP3: 2336 - 120 = 2216).
# Saída: <trab-dir>/<nome-do-final>/plano-gif.json e <trab-dir>/planos.json (lista de planos, entrada do lote_gif.sh).
import json, glob, subprocess, argparse
from pathlib import Path
SONS = str(Path(__file__).resolve().parents[1] / 'assets/sons-gif')
ap = argparse.ArgumentParser(description='planos de GIF para o lote de finais')
ap.add_argument('--momentos', required=True, help='JSON: lista de momentos com k0/k1 em quadros da V3')
ap.add_argument('--bases', required=True, nargs='+', help='finais (glob entre aspas ou lista de arquivos)')
ap.add_argument('--corpo', type=int, required=True); ap.add_argument('--kg', type=int, default=120); ap.add_argument('--p90', type=float, required=True)
ap.add_argument('--saida-dir', required=True); ap.add_argument('--trab-dir', required=True); ap.add_argument('--sons', default=SONS)
ap.add_argument('--mix', help='WAV voz+sfx da V3 (usado pelo auditar_gif_meme.py para conferir sincronia)')
ap.add_argument('--sufixo', default='-gif-meme-hlg.mp4')
A = ap.parse_args()
MOM = json.loads(Path(A.momentos).read_text())
for m in MOM:
    assert Path(m['gif']).exists(), f'GIF não encontrado: {m["gif"]}'
    assert (Path(A.sons) / f'{m["som"]}.wav').exists(), f'som não encontrado: {m["som"]}'
bases = sorted({str(Path(f).resolve()) for b in A.bases for f in (glob.glob(b) or [b])}); assert bases, 'nenhuma base'
T = Path(A.trab_dir); planos = []
for b in map(Path, bases):
    n = int(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v', '-count_packets', '-show_entries', 'stream=nb_read_packets',
                                     '-of', 'csv=p=0', str(b)], text=True).strip())
    P = n - A.corpo; d = P - A.kg; nome = b.stem[:-4] if b.stem.endswith('-hlg') else b.stem
    assert P > 0, f'{b.name}: {n} quadros, menor que o corpo {A.corpo}'
    pl = dict(base=str(b), saida=str(Path(A.saida_dir) / f'{nome}{A.sufixo}'), trab=str(T / b.stem), sons=A.sons, p90=A.p90, quadros=n, P=P, kg=A.kg,
              momentos=[dict(m, k0=m['k0'] + d, k1=m['k1'] + d, k_v3=m['k0']) for m in MOM])
    if A.mix: pl['mix'] = str(Path(A.mix).resolve())
    f = T / b.stem / 'plano-gif.json'; f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(pl, ensure_ascii=False, indent=1)); planos.append(str(f))
    print(b.stem, n, 'P', P, [(m['k0'], m['k1']) for m in pl['momentos']])
Path(A.saida_dir).mkdir(parents=True, exist_ok=True)
(T / 'planos.json').write_text(json.dumps(planos, indent=1)); print(len(planos), 'planos ->', T / 'planos.json')
