# Diagnóstico antes do render do GIF: reproduz a soma base + efeitos do gif_meme.py (pop -12 dB e sting -1 dB do p90,
# cada efeito limitado a pico 0,5) e mostra o pico amostral geral e por momento. Se o pico do mix passar de ~0,89
# (true peak acima de -1 dBTP), aplique ganho uniforme pequeno na base (ganho_uniforme.py) e refaça o plano.
# Uso: python3 pico_gif.py <plano-gif.json>
import sys, json, subprocess, argparse
from pathlib import Path
import numpy as np
ap = argparse.ArgumentParser(description='pico da base + efeitos do GIF'); ap.add_argument('plano')
ap.add_argument('--db-pop', type=float, default=-12.0); ap.add_argument('--db-sting', type=float, default=-1.0); ap.add_argument('--pico-fx', type=float, default=0.5)
A = ap.parse_args()
PL = json.loads(Path(A.plano).read_text()); S = Path(PL['sons']); P90 = PL['p90']
def dec(f): return np.frombuffer(subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(f), '-vn', '-f', 'f32le', '-ar', '48000', '-ac', '2', '-']), '<f4').reshape(-1, 2).copy()
def rms(x): return float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))
base = dec(PL['base']); fx = np.zeros_like(base)
print('pico base', round(float(np.abs(base).max()), 4), 'no quadro', int(np.abs(base).max(1).argmax() // 1600))
for m in PL['momentos']:
    a = round(m['k0'] / 30 * 48000)
    for nome, db in (('pop-gif', A.db_pop), (m['som'], A.db_sting)):
        s = dec(S / f'{nome}.wav'); g = min(P90 * 10 ** (db / 20) / rms(s), A.pico_fx / float(np.abs(s).max()))
        n = min(len(s), len(fx) - a); fx[a:a + n] += s[:n] * g
mix = np.abs(base + fx).max(1); i = int(mix.argmax()); print('pico mix', round(float(mix[i]), 4), 'no quadro', i // 1600)
for m in PL['momentos']:
    a = round(m['k0'] / 30 * 48000); b = a + 48000 * 4
    print(m.get('palavra', ''), m['k0'], 'pico mix', round(float(mix[a:b].max()), 4), 'pico base', round(float(np.abs(base[a:b]).max()), 4))
