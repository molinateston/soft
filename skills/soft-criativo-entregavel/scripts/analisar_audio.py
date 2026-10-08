"""Primeiro passo de cada criativo: transcreve o audio, lista as pausas, estima o genero da voz e o ritmo.
    python analisar_audio.py <audio> [pasta_do_criativo]
Imprime (e grava analise.json na pasta do criativo, se dada):
  - a transcricao em blocos (corrigir nomes proprios a mao);
  - os trechos de fala com as pausas entre eles (para escolher onde termina o gancho e onde comeca o CTA);
  - tom medio da voz (Hz) -> feminina / masculina / incerto;
  - palavras por segundo e a aceleracao sugerida (alvo ~3,6 palavras/s; os anuncios aprovados ficaram entre 3,5 e 4,0; maximo 1,35x).
"""
import sys, os, re, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import align_voice as A, transcribe as T
from scipy.signal import butter, sosfiltfilt

def voiced(x, sr, thr=.045):
    y = sosfiltfilt(butter(4, [150, 3000], btype='band', fs=sr, output='sos'), x); hop = int(.005 * sr)
    env = np.array([np.sqrt(np.mean(y[i:i + hop * 4] ** 2)) for i in range(0, len(y) - hop * 4, hop)])
    env = np.convolve(env, np.ones(5) / 5, 'same'); env /= env.max(); t = np.arange(len(env)) * .005; segs = []; s = None
    for i, a in enumerate(env > thr):
        if a and s is None: s = i
        if not a and s is not None:
            if t[i] - t[s] > .05: segs.append([round(float(t[s]), 2), round(float(t[i]), 2)])
            s = None
    if s is not None: segs.append([round(float(t[s]), 2), round(float(t[-1]), 2)])
    return segs

def pitch(x, sr):
    x = x[:sr * 40]; n = int(.04 * sr); hop = int(.02 * sr); out = []
    for i in range(0, len(x) - n, hop):
        w = x[i:i + n] * np.hanning(n)
        if np.sqrt((w ** 2).mean()) < .02: continue
        ac = np.correlate(w, w, 'full')[n - 1:]; lo, hi = int(sr / 400), int(sr / 70); k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > .45 * ac[0]: out.append(sr / k)
    return float(np.median(out)) if out else 0.0

if __name__ == '__main__':
    path = sys.argv[1]; x, sr = A.load(path); x = x.copy(); dur = len(x) / sr
    chunks, _, _, _ = T.transcribe(path, 'pt'); text = ' '.join(c[2] for c in chunks)
    print('TRANSCRICAO (conferir nomes proprios e marcas):')
    for a, b, t in chunks: print('  [%5.1f-%5.1f] %s' % (a, b, t))
    segs = voiced(x, sr); merged = [segs[0][:]]
    for a, b in segs[1:]:
        if a - merged[-1][1] < .20: merged[-1][1] = b
        else: merged.append([a, b])
    print('\nBLOCOS DE FALA (pausas >= 0,20 s entre eles):')
    for i, (a, b) in enumerate(merged): print('  %6.2f - %6.2f%s' % (a, b, '   | pausa %.2f s' % (merged[i + 1][0] - b) if i + 1 < len(merged) else ''))
    f0 = pitch(x, sr); gen = 'feminina' if f0 > 180 else ('masculina' if 0 < f0 < 150 else 'incerto: perguntar ao usuario')
    words = len(re.findall(r'\w+', text)); speech = sum(b - a for a, b in segs); wps = words / max(1e-6, dur)
    k = 1.0 if wps >= 3.4 else round(min(1.35, 3.6 / wps), 3)
    print('\nduracao %.2f s | tom medio %.0f Hz -> voz %s' % (dur, f0, gen))
    print('%d palavras | %.2f palavras/s | aceleracao sugerida K = %.3f' % (words, wps, k))
    if len(sys.argv) > 2:
        os.makedirs(sys.argv[2], exist_ok=True)
        json.dump(dict(audio=os.path.abspath(path), dur=dur, texto=text, blocos=merged, trechos=segs, f0=f0, voz=gen, palavras=words, wps=wps, K=k),
                  open(os.path.join(sys.argv[2], 'analise.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
