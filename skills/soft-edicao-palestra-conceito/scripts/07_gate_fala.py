"""Etapa 7a. Gate de fala: a transcricao do bruto (o que devia entrar) contra a transcricao do FINAL (o que entrou).
1) re-transcreve o audio do final.mp4 (02_transcrever no modo extra) -> asr-final.json (cache se o final nao mudou);
2) alinha as palavras esperadas (bruto, dentro das pecas) com as do final (difflib, sem acento e pontuacao);
3) confere fala engolida entre pecas do mesmo bloco, palavra cortada no meio e emenda com energia dos dois lados.
uso: python3 07_gate_fala.py TRAB
saida: gate-fala.json. criterio de pronto (PRONTO, exit 0): nenhuma palavra de 3+ letras ausente no final,
cobertura >= 97%, nenhuma fala entre pecas fora de 'cortar', nenhuma palavra atravessando emenda."""
import difflib, os, re, subprocess, sys, unicodedata
import numpy as np
from scipy.io import wavfile
import comum as C

T = C.trab_arg()
A, E, CC = C.ajustes(T), C.lj(T, 'entrada.json'), C.lj(T, 'cortes.json')
SPD, CM = CC['velocidade'], CC['cut_map']
FIN = os.path.join(T, 'final.mp4')
RL = C.lj(T, 'render-log.json')
DUR = RL['dur']
norm = lambda s: re.sub(r'[^a-z0-9]', '', ''.join(ch for ch in unicodedata.normalize('NFKD', s.lower()) if not unicodedata.combining(ch)))

# ---------- 1. ASR do final ----------
wav, asr = os.path.join(T, 'final16.wav'), os.path.join(T, 'asr-final.json')
if not os.path.exists(asr) or os.path.getmtime(asr) < os.path.getmtime(FIN):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', FIN, '-vn', '-ac', '1', '-ar', '16000', wav], check=True)
    subprocess.run([sys.executable, os.path.join(C.SCRIPTS, '02_transcrever.py'), T, wav, asr, '0'], check=True, stdout=subprocess.DEVNULL)
got = [dict(t0=p['t0'], t1=p['t1'], w=p['w'], n=norm(p['w'])) for s in C.lj(T, 'asr-final.json')['segmentos'] for p in s['palavras']]
got = [g for g in got if g['n']]

# ---------- 2. esperadas: bruto dentro de cada peca, em tempo de saida ----------
ws = C.palavras_bruto(T)
for de, ate, novas in A.get('substituir', []):
    ws = [w for w in ws if not (de <= w['t0'] < ate)] + [dict(w=x[0], t0=x[1], t1=x[2]) for x in novas]
ws.sort(key=lambda w: w['t0'])
REM = A.get('cortar', [])
cortada = lambda w: any(a <= (w['t0'] + w['t1']) / 2 <= b for a, b in REM)
esp, parciais = [], []
for c in CM:
    ss, se = c['source_start'], c['source_end']
    for w in ws:
        if w['t1'] <= ss or w['t0'] >= se or cortada(w): continue
        dentro = (min(w['t1'], se) - max(w['t0'], ss)) / max(w['t1'] - w['t0'], 1e-3)
        mid = (w['t0'] + w['t1']) / 2
        if not ss <= mid < se and dentro < 0.5: continue        # pertence a peca vizinha
        tl = c['timeline_start'] + (max(w['t0'], ss) - ss) / SPD
        if tl >= DUR - 0.3: continue                              # render parcial (--ate)
        esp.append(dict(w=w['w'], n=norm(w['w']), tl=round(tl, 3), src=w['t0']))
        if dentro < 0.85: parciais.append(f"'{w['w']}' {w['t0']:.2f}: so {dentro:.0%} dentro da peca {c['id']}")
esp = [e for i, e in enumerate(esp) if e['n'] and not (i and e['n'] == esp[i - 1]['n'] and abs(e['src'] - esp[i - 1]['src']) < 0.05)]

sm = difflib.SequenceMatcher(None, [e['n'] for e in esp], [g['n'] for g in got], autojunk=False)
ach = [False] * len(esp)
for a, b, n in sm.get_matching_blocks():
    for k in range(n): ach[a + k] = True
for i, e in enumerate(esp):   # segunda chance: grafia parecida ou palavra colada/partida pelo whisper
    if ach[i]: continue
    viz = [g for g in got if abs(g['t0'] - e['tl']) <= 1.2]
    junto = ''.join(g['n'] for g in viz)
    if any(len(e['n']) > 3 and difflib.SequenceMatcher(None, e['n'], g['n']).ratio() >= 0.75 for g in viz) or (len(e['n']) > 1 and e['n'] in junto):
        ach[i] = True
aus = [e for i, e in enumerate(esp) if not ach[i]]
cob = 1 - len(aus) / max(len(esp), 1)

# ---------- 3. fala entre pecas e emendas ----------
entre, cruza, emendas = [], [], []
sr, au = wavfile.read(os.path.join(T, 'fonte16.wav'))
au = au.astype(np.float32) / 32768.0
if au.ndim > 1: au = au.mean(1)
off = E['offset']


def rms(t0, t1):
    a, b = int((t0 - off) * sr), int((t1 - off) * sr)
    x = au[max(a, 0):max(b, 0)]
    if len(x) < 64: return 0.0
    q = len(x) // int(0.02 * sr) or 1
    return float(np.max([np.sqrt(np.mean(f ** 2)) for f in np.array_split(x, q)]))


for i in range(len(CM) - 1):
    c, d = CM[i], CM[i + 1]
    if d['timeline_start'] >= DUR: break
    if c['bloco'] == d['bloco']:
        for w in ws:
            if c['source_end'] + 0.02 < (w['t0'] + w['t1']) / 2 < d['source_start'] - 0.02 and not cortada(w):
                entre.append(f"'{w['w']}' {w['t0']:.2f} entre {c['id']} e {d['id']}")
    if abs(d['source_start'] - c['source_end']) < 0.02: continue
    for borda in (c['source_end'], d['source_start']):
        for w in ws:
            if w['t0'] < borda - 0.03 and w['t1'] > borda + 0.03 and not cortada(w) and (w['t1'] - w['t0']) < 1.2:
                cruza.append(f"'{w['w']}' {w['t0']:.2f}-{w['t1']:.2f} atravessa a emenda {borda:.2f}")
    p75 = np.percentile([rms(x['source_start'], x['source_end']) for x in (c, d)], 75) or 1
    fora, dent = rms(c['source_end'] - 0.12, c['source_end']) / p75, rms(d['source_start'], d['source_start'] + 0.06) / p75
    if fora > 0.45 and dent > 0.45:
        emendas.append(f"{c['id']}->{d['id']} saida {c['timeline_end']:.2f}s: energia alta dos dois lados ({fora:.2f}/{dent:.2f}), ouca")
cruza = sorted(set(cruza))
falhas = [f"ausente no final: '{e['w']}' (saida {e['tl']:.2f}s, fonte {e['src']:.2f}s)" for e in aus if len(e['n']) >= 3]
if cob < 0.97: falhas.append(f'cobertura {cob:.1%} < 97%')
falhas += ['fala engolida ' + x for x in entre] + ['palavra cortada ' + x for x in cruza]
avisos = [f"ausente curta: '{e['w']}' saida {e['tl']:.2f}s" for e in aus if len(e['n']) < 3] + ['parcial ' + x for x in parciais] + ['emenda ' + x for x in emendas]
C.gj(T, 'gate-fala.json', dict(esperadas=len(esp), achadas=len(esp) - len(aus), cobertura=round(cob, 4), falhas=falhas, avisos=avisos,
                               asr_final=' '.join(g['w'] for g in got)))
print(f'palavras esperadas {len(esp)} | no final {len(got)} | cobertura {cob:.1%}')
for x in avisos: print('ATENCAO', x)
for x in falhas: print('FALHA', x)
print('PRONTO' if not falhas else 'NAO PRONTO')
sys.exit(1 if falhas else 0)
