"""Etapa 6c. Reenquadre 16:9 dentro do painel seguindo o rosto -> reframe.json [x0,y0,w,h] por quadro de saida
(coordenadas da fonte, que e o tamanho de base.mkv). Plano = pecas continuas na fonte.
Zoom por plano entre ajustes.zoom [min,max] (padrao [1.15, 1.45]); planos alternados ganham punch-in x1,09
para o corte de pausa nao parecer pulo. Rosto com o topo a 22% da altura da caixa.
uso: python3 06_reframe.py TRAB
criterio de pronto: PRONTO; toda caixa dentro do painel e com proporcao 1080:608."""
import json, sys
import numpy as np
from scipy.ndimage import median_filter
import comum as C

T = C.trab_arg()
A, CC, R = C.ajustes(T), C.lj(T, 'cortes.json'), C.lj(T, 'rosto.json')
SPD, FPS = CC['velocidade'], C.FPS
PX0, PY0, PX1, PY1 = R['painel']
PW, PH = PX1 - PX0, PY1 - PY0
ZMIN, ZMAX = A.get('zoom', [1.15, 1.45]); ZSTEP, PUNCH, TOPO = 0.05, 1.09, 0.22
if A.get('preservar_painel', False):
    if abs(PW / PH - C.WV / C.HV) > .02:
        sys.exit('preservar_painel exige painel 16:9; não recortar silenciosamente')
    NF = int(round(CC['dur_saida'] * FPS))
    C.gj(T, 'reframe.json', [[PX0, PY0, PW, PH] for _ in range(NF)])
    print(f'{NF} quadros: painel integral preservado, sem zoom, recorte ou desfoque. PRONTO')
    sys.exit(0)
RY = A.get('rosto_y')   # [ymin, ymax] opcional: descarta rostos fora (plateia, telao)
amos = [x for p in R['raw'] for x in p if 60 <= x[4] <= 700 and (not RY or RY[0] <= x[2] <= RY[1])]
amos = np.array(sorted(amos)) if amos else np.zeros((0, 5))
cm = CC['cut_map']


def gauss(v, sig):
    if len(v) < 3 or sig <= 0: return v
    k = np.arange(-3 * sig, 3 * sig + 1); g = np.exp(-k ** 2 / (2 * sig ** 2)); g /= g.sum()
    return np.convolve(np.pad(v, (len(k) // 2, len(k) // 2), mode='edge'), g, 'valid')


NF = int(round(CC['dur_saida'] * FPS))
fr_ts = []
for i, c in enumerate(cm):
    n0, n1 = int(round(c['timeline_start'] * FPS)), int(round(c['timeline_end'] * FPS))
    if i == len(cm) - 1: n1 = NF
    for n in range(n0, min(n1, NF)):
        fr_ts.append((n, i, c['source_start'] + (n / FPS - c['timeline_start']) * SPD))
planos = [[fr_ts[0]]]
for a, b in zip(fr_ts, fr_ts[1:]):
    if a[1] == b[1] or abs(cm[b[1]]['source_start'] - cm[a[1]]['source_end']) < 1e-3: planos[-1].append(b)
    else: planos.append([b])
box = [None] * NF; info = []
for pi, pl in enumerate(planos):
    ns = [x[0] for x in pl]; ts = np.array([x[2] for x in pl])
    sel = amos[(amos[:, 0] >= ts[0] - 1.5) & (amos[:, 0] <= ts[-1] + 1.5)] if len(amos) else amos
    if len(sel) >= 5:
        sel = sel.copy(); sel[:, 1] = median_filter(sel[:, 1], 5, mode='nearest'); sel[:, 2] = median_filter(sel[:, 2], 5, mode='nearest')
    if len(sel) == 0:
        xc = np.full(len(ts), PX0 + PW / 2); yt = np.full(len(ts), PY0 + PH * 0.25)
    else:
        xc = np.interp(ts, sel[:, 0], sel[:, 1]); yt = np.interp(ts, sel[:, 0], sel[:, 2])
    xc = gauss(xc, 0.5 * FPS); yt = gauss(yt, 0.8 * FPS)
    d = np.minimum(xc - PX0, PX1 - xc)
    zneed = PW / (2 * max(np.percentile(d, 25), 1))
    z = min(ZMAX, max(ZMIN, np.ceil(zneed / ZSTEP) * ZSTEP))
    if pi % 2 == 1: z = z * PUNCH
    w = PW / z; h = w * C.HV / C.WV
    if h > PH: h = PH; w = h * C.WV / C.HV
    for k, n in enumerate(ns):
        x0 = float(np.clip(xc[k] - w / 2, PX0, PX1 - w)); y0 = float(np.clip(yt[k] - TOPO * h, PY0, PY1 - h))
        box[n] = [round(x0, 2), round(y0, 2), round(w, 2), round(h, 2)]
    info.append((ns[0] / FPS, ts[0], len(sel), round(z, 3)))
for n in range(NF):
    if box[n] is None: box[n] = box[n - 1]
json.dump(box, open(f'{T}/reframe.json', 'w'))
for x in info: print('saida %6.2f fonte %8.2f amostras %3d zoom %.3f' % x)
bad = [n for n, b in enumerate(box) if b[0] < PX0 - 0.5 or b[1] < PY0 - 0.5 or b[0] + b[2] > PX1 + 0.5 or b[1] + b[3] > PY1 + 0.5 or abs(b[2] / b[3] - C.WV / C.HV) > 0.01]
print(f'{len(planos)} planos, {NF} quadros', 'PRONTO' if not bad else f'NAO PRONTO: {len(bad)} caixas fora do painel')
sys.exit(1 if bad else 0)
