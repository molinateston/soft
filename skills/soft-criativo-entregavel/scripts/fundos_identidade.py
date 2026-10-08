"""Monta os fundos da oferta na identidade visual do proprio material (padrao desde 2026-10-04).
Em vez de um fundo com objetos ja desenhados nele, usa: tres fundos LIMPOS (sem objetos) + uma folha de elementos soltos,
gerada sobre fundo magenta chapado, que este script recorta e posiciona. Assim nao sobra mancha onde o objeto estava.

    python fundos_identidade.py <pasta_do_kit> recortar     # corta os elementos da folha e numera
    python fundos_identidade.py <pasta_do_kit> montar       # monta a_/b_/dark_ (limpo, elementos, meta) a partir do layout.json

Espera em <kit>/bgs/originais/:  a.png, b.png, dark.png (fundos 9:16 limpos) e objetos.png (folha de elementos em magenta).
'recortar' grava <kit>/bgs/elementos/01.png, 02.png... (da esquerda para a direita, de cima para baixo) e elementos.jpg, uma
folha numerada para voce olhar e dar nome a cada um.
'montar' le <kit>/bgs/layout.json:
    {"a":    [["01", "pill", 905, 1650, 400], ["02", "check", 875, 255, 300], ["07", "spark", 125, 330, 86]],
     "b":    [...], "dark": [...]}
cada linha: numero do elemento, tipo, centro x, centro y, largura — em pixels da tela 1080x1920.
tipos: "pill" e "check" flutuam devagar (use "pill" para os grandes); "spark" gira (para estrelinhas e brilhos pequenos).
Deixe o centro da tela livre: os elementos vao nos cantos e nas bordas. Confira <nome>_recon.png depois.
"""
import sys, os, json
import numpy as np, cv2
from PIL import Image, ImageDraw

def recortar(bgd):
    I = np.asarray(Image.open(os.path.join(bgd, 'originais', 'objetos.png')).convert('RGB')).astype(np.float32); H, W = I.shape[:2]
    M = np.median(I[:40, :40].reshape(-1, 3), 0); d = np.sqrt(((I - M) ** 2).sum(-1)); a = cv2.GaussianBlur(np.clip((d - 70) / 110, 0, 1), (0, 0), 0.8)
    F = np.clip(np.where(a[..., None] > .05, (I - (1 - a[..., None]) * M) / np.maximum(a[..., None], .05), I), 0, 255)   # tira a cor do fundo das bordas
    n, lab, st, cen = cv2.connectedComponentsWithStats((a > .5).astype(np.uint8), 8); comps = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > W * H * .002]
    linha = H / 6; comps.sort(key=lambda i: (int(cen[i][1] // linha), cen[i][0])); out = os.path.join(bgd, 'elementos'); os.makedirs(out, exist_ok=True)
    for f in os.listdir(out): os.remove(os.path.join(out, f))
    tiles = []
    for k, i in enumerate(comps, 1):
        x, y, w, h = st[i, :4]; p = 12; x0, y0, x1, y1 = max(0, x - p), max(0, y - p), min(W, x + w + p), min(H, y + h + p)
        m = cv2.dilate((lab[y0:y1, x0:x1] == i).astype(np.uint8), np.ones((9, 9), np.uint8)).astype(np.float32)
        sp = Image.fromarray(np.dstack([F[y0:y1, x0:x1], a[y0:y1, x0:x1] * m * 255]).astype(np.uint8), 'RGBA'); sp.save(os.path.join(out, '%02d.png' % k)); tiles.append(sp)
    S = Image.new('RGB', (len(tiles) * 260, 290), (120, 120, 120)); dr = ImageDraw.Draw(S)
    for k, sp in enumerate(tiles):
        t = sp.copy(); t.thumbnail((240, 240)); S.paste(t, (k * 260 + 10, 40), t); dr.text((k * 260 + 12, 8), '%02d  %dx%d' % (k + 1, sp.width, sp.height), fill='white')
    S.save(os.path.join(bgd, 'elementos.jpg'), quality=90); print('ok: %d elementos em bgs/elementos/ (veja bgs/elementos.jpg)' % len(tiles))

def montar(bgd):
    lay = json.load(open(os.path.join(bgd, 'layout.json'), encoding='utf-8'))
    for bg, items in lay.items():
        for f in os.listdir(bgd):
            if f.startswith(bg + '_') and f.endswith(('.png', '.json')): os.remove(os.path.join(bgd, f))
        clean = Image.open(os.path.join(bgd, 'originais', bg + '.png')).convert('RGB').resize((1080, 1920), Image.LANCZOS); clean.save(os.path.join(bgd, bg + '_clean.png')); meta = []; rec = clean.convert('RGBA')
        for k, (num, typ, cx, cy, w) in enumerate(items):
            sp = Image.open(os.path.join(bgd, 'elementos', '%02d.png' % int(num))).convert('RGBA'); h = round(sp.height * w / sp.width); s = sp.resize((int(w), h), Image.LANCZOS); nm = 'e%02d_%d' % (int(num), k)
            s.save(os.path.join(bgd, '%s_%s.png' % (bg, nm))); meta.append(dict(name=nm, type=typ, x=cx - w / 2, y=cy - h / 2, w=int(w), h=h, cx=cx, cy=cy, blur=0)); rec.alpha_composite(s, (int(cx - w / 2), int(cy - h / 2)))
        json.dump(meta, open(os.path.join(bgd, bg + '_meta.json'), 'w')); rec.convert('RGB').save(os.path.join(bgd, bg + '_recon.png')); print(bg, 'ok:', len(meta), 'elementos')

if __name__ == '__main__':
    bgd = os.path.join(os.path.abspath(sys.argv[1]), 'bgs'); m = sys.argv[2] if len(sys.argv) > 2 else ''
    if m == 'recortar': recortar(bgd)
    elif m == 'montar': montar(bgd)
    else: raise SystemExit(__doc__)
