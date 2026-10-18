# Limites exatos de cada tomada de gancho pelo envelope de energia do bruto (48 kHz, janelas de 10 ms), com as palavras do
# transcrever_tomadas.py como guia. Início = primeiro salto acima de -40 dB a partir de 0,5 s antes da 1a palavra, menos 0,05 s,
# arredondado ao quadro (a inspiração fica em -45..-60 dB e não entra). Fim = última janela ativa (piso + 25% até a voz) até 0,5 s
# depois da última palavra, mais 0,11 s de cauda. f0 = quadro do bruto onde o gancho começa; n_h = quadros do gancho a 1,2x.
# Uso: python3 cortes_tomadas.py --bruto bruto.mp4 --palavras analise/tomadas/large-v3.json --saida analise/cortes.json [--chave ep4-B ...]
import json, subprocess, argparse
from pathlib import Path
import numpy as np
ap = argparse.ArgumentParser(description='limites das tomadas pelo envelope de energia')
ap.add_argument('--bruto', required=True); ap.add_argument('--palavras', required=True); ap.add_argument('--saida', required=True)
ap.add_argument('--chave', action='append', help='só estas tomadas (padrão: todas do JSON de palavras)')
ap.add_argument('--fps', type=float, default=30); ap.add_argument('--vel', type=float, default=1.2)
A = ap.parse_args()
W = json.loads(Path(A.palavras).read_text()); SR = 48000
out = json.loads(Path(A.saida).read_text()) if Path(A.saida).exists() else {}
for key, ws in W.items():
    if A.chave and key not in A.chave: continue
    a0, b0 = ws[0][0], ws[-1][1]; s0 = max(0.0, a0 - 1.0)
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(s0), '-t', str(b0 - s0 + 1.0), '-i', A.bruto, '-vn', '-ac', '1', '-ar', str(SR),
                                      '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32)
    h = SR // 100
    e = 20 * np.log10(np.sqrt(np.mean(x[:len(x) // h * h].reshape(-1, h) ** 2, 1)) + 1e-9)
    piso = np.percentile(e, 10); voz = np.percentile(e, 90); lim = piso + 0.25 * (voz - piso)
    t = s0 + np.arange(len(e)) / 100; ativo = e > lim
    i0 = next(i for i in range(len(e)) if t[i] >= a0 - 0.5 and e[i] > -40)
    i1 = max(i for i in range(len(e)) if t[i] <= b0 + 0.5 and ativo[i])
    ini = round(round((float(t[i0]) - 0.05) * A.fps) / A.fps, 4); fim = round(float(t[i1]) + 0.11, 2)
    out[key] = {'ini': ini, 'fim': fim, 'piso_db': round(float(piso), 1), 'voz_db': round(float(voz), 1), 'whisper': [a0, b0],
                'f0': round(ini * A.fps), 'n_h': round((fim - ini) / A.vel * A.fps)}
    print(key, out[key])
Path(A.saida).parent.mkdir(parents=True, exist_ok=True)
Path(A.saida).write_text(json.dumps(out, indent=1))
