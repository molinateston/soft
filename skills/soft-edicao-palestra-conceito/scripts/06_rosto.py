"""Etapa 6b. Rosto: YuNet (assets/modelos) a cada 0,1 s de fonte em cada peca do keep.
ajustes.painel [x0,y0,x1,y1] opcional: regiao da fonte onde esta a camera (slide + camera lado a lado).
uso: python3 06_rosto.py TRAB      saida: rosto.json {raw:[[t, xc, y_topo, w, h], ...] por peca}
criterio de pronto: PRONTO se >= 70% das pecas tem rosto (as sem rosto ficam no centro do painel)."""
import json, os, sys
import cv2, numpy as np
import comum as C

T = C.trab_arg()
A, E, CC = C.ajustes(T), C.lj(T, 'entrada.json'), C.lj(T, 'cortes.json')
MOD = os.path.join(C.RAIZ, 'assets', 'modelos', 'face_detection_yunet_2023mar.onnx')
PX0, PY0, PX1, PY1 = A.get('painel') or [0, 0, E['largura'], E['altura']]
SC = 2 if PX1 - PX0 > 1200 else 1          # detecta em meia resolucao quando o painel e grande
det = cv2.FaceDetectorYN.create(MOD, '', ((PX1 - PX0) // SC, (PY1 - PY0) // SC), 0.6, 0.3, 50)
k = CC['keep']
cap = cv2.VideoCapture(E['fonte'])
res = [[] for _ in k]
for i, (a, b) in enumerate(k):
    cap.set(cv2.CAP_PROP_POS_MSEC, max(0, a - 0.05) * 1000); prox = a
    while True:
        if not cap.grab(): break
        t = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        if t >= b - 0.02: break
        if t + 1e-3 < prox: continue
        ok, fr = cap.retrieve()
        if not ok: break
        prox += 0.1
        p = np.ascontiguousarray(fr[PY0:PY1, PX0:PX1])
        if SC > 1: p = cv2.resize(p, ((PX1 - PX0) // SC, (PY1 - PY0) // SC), interpolation=cv2.INTER_AREA)
        _, f = det.detect(p)
        if f is not None:
            x, y, w, h = [float(v) * SC for v in max(f, key=lambda r: r[2] * r[3])[:4]]
            res[i].append([round(t, 3), PX0 + x + w / 2, PY0 + y, w, h])
com = sum(1 for r in res if r)
for i, (a, b) in enumerate(k):
    r = np.array(res[i]) if res[i] else None
    print(i, f'{a:.2f}', 'SEM ROSTO' if r is None else f'xc {np.median(r[:, 1]):.0f} y {np.median(r[:, 2]):.0f} h {np.median(r[:, 4]):.0f} n {len(r)}')
C.gj(T, 'rosto.json', dict(painel=[PX0, PY0, PX1, PY1], raw=res))
print(f'{com}/{len(k)} pecas com rosto', 'PRONTO' if com >= 0.7 * len(k) else 'ATENCAO: confira painel e luz')
