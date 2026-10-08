"""Separa cada fundo gerado por IA em fundo limpo + objetos soltos, para os objetos entrarem e flutuarem.
    python fundos.py <pasta_do_kit_da_oferta> [a b dark]
Espera em <kit>/bgs/:  a.png, b.png, dark.png (imagens 9:16 geradas) e caixas.json com os recortes de cada objeto, em pixels de
uma imagem 1296x2304 (o script redimensiona a imagem para esse tamanho antes):
    {"a": [["nome", x0, y0, x1, y1, "tipo", desfoque, opacidade], ...], "b": [...], "dark": [...]}
    tipo: "spark" (brilho que gira), "check" (objeto pequeno que flutua), "pill" (objeto grande; se encosta na borda so "respira")
    desfoque: 0 para objetos nitidos; 9-24 para os grandes de canto (ficam atras do conteudo); opacidade .8-1.0
Gera <nome>_clean.png, <nome>_<objeto>.png, <nome>_meta.json e <nome>_recon.png (conferir: o limpo nao pode ter sombra dos objetos).
"""
import os, sys, json
import numpy as np, cv2
from PIL import Image
W0, H0 = 1296, 2304; Sc = 1080 / W0

def build(bgd, name, boxes):
    img = np.asarray(Image.open(os.path.join(bgd, name + '.png')).convert('RGB').resize((W0, H0), Image.LANCZOS)).astype(np.float32); H, W = img.shape[:2]; k = 4
    small = cv2.resize(img, (W // k, H // k), interpolation=cv2.INTER_AREA).astype(np.uint8); hole = np.zeros((H // k, W // k), np.uint8)
    for n, x0, y0, x1, y1, *_ in boxes: hole[y0 // k:(y1 + k - 1) // k, x0 // k:(x1 + k - 1) // k] = 255
    ip = cv2.inpaint(small, hole, 9, cv2.INPAINT_TELEA).astype(np.float32); hf = hole.astype(np.float32) / 255.0; g = ip.copy()
    for _ in range(3):                                   # difusao: desfoca so dentro do buraco, preservando a borda real
        g = cv2.GaussianBlur(g, (0, 0), 16); g = ip * (1 - hf[..., None]) + g * hf[..., None]
    soft = cv2.GaussianBlur(hf, (0, 0), 5)[..., None]; fill_s = g * (1 - soft) + cv2.GaussianBlur(g, (0, 0), 6) * soft
    fill = cv2.resize(fill_s, (W, H), interpolation=cv2.INTER_CUBIC)
    hm = cv2.resize(cv2.GaussianBlur(hf, (0, 0), 1.2), (W, H), interpolation=cv2.INTER_LINEAR)[..., None]; bgc = img * (1 - hm) + fill * hm; meta = []
    for n, x0, y0, x1, y1, typ, blur, am in boxes:
        I = img[y0:y1, x0:x1]; B = bgc[y0:y1, x0:x1]; d = np.sqrt(((I - B) ** 2).sum(-1)); a = np.clip((d - 6) / 30.0, 0, 1); a = cv2.GaussianBlur(a, (0, 0), 0.9)
        m = (a > .2).astype(np.uint8); cnt, lab, stats, cen = cv2.connectedComponentsWithStats(m, 8)
        if cnt > 1:
            cx, cy = (x1 - x0) / 2, (y1 - y0) / 2
            if typ == 'pill': keep = np.isin(lab, [i for i in range(1, cnt) if stats[i, cv2.CC_STAT_AREA] > 900]).astype(np.uint8)   # grupo de objetos grandes
            else: keep = (lab == max(range(1, cnt), key=lambda i: stats[i, cv2.CC_STAT_AREA] - .2 * np.hypot(cen[i][0] - cx, cen[i][1] - cy))).astype(np.uint8)
            a = a * cv2.dilate(keep, np.ones((9, 9), np.uint8)).astype(np.float32)
        a3 = a[..., None]; F = np.clip(np.where(a3 > .04, (I - (1 - a3) * B) / np.maximum(a3, .04), I), 0, 255)
        if blur > 0:
            P = cv2.GaussianBlur(F * a3, (0, 0), blur); A = cv2.GaussianBlur(a, (0, 0), blur); F = np.clip(P / np.maximum(A[..., None], 1e-3), 0, 255); a = A
            lum = F.mean(-1, keepdims=True); F = lum + (F - lum) * .92
        a = np.clip(a * am, 0, 1); w, h = int(round((x1 - x0) * Sc)), int(round((y1 - y0) * Sc))
        Image.fromarray(np.dstack([F, a * 255]).astype(np.uint8), 'RGBA').resize((max(2, w), max(2, h)), Image.LANCZOS).save(os.path.join(bgd, f'{name}_{n}.png'))
        meta.append(dict(name=n, type=typ, x=x0 * Sc, y=y0 * Sc, w=w, h=h, cx=(x0 + x1) / 2 * Sc, cy=(y0 + y1) / 2 * Sc, blur=blur))
    sm = cv2.resize(bgc, (W // k, H // k), interpolation=cv2.INTER_AREA)   # costura: desfoca uma faixa em volta da borda de cada buraco
    for sg in (9, 5):
        s_ = cv2.GaussianBlur(hf, (0, 0), sg); e_ = np.clip(4 * s_ * (1 - s_), 0, 1)[..., None]; sm2 = sm * (1 - e_) + cv2.GaussianBlur(sm, (0, 0), sg * 1.6) * e_
        bgc = bgc + cv2.resize(sm2 - sm, (W, H), interpolation=cv2.INTER_CUBIC); sm = sm2
    bg = Image.fromarray(np.clip(bgc, 0, 255).astype(np.uint8), 'RGB').resize((1080, 1920), Image.LANCZOS); bg.save(os.path.join(bgd, name + '_clean.png'))
    json.dump(meta, open(os.path.join(bgd, name + '_meta.json'), 'w')); rec = bg.convert('RGBA')
    for m_ in meta: rec.alpha_composite(Image.open(os.path.join(bgd, f"{name}_{m_['name']}.png")), (int(round(m_['x'])), int(round(m_['y']))))
    rec.convert('RGB').save(os.path.join(bgd, name + '_recon.png')); print(name, 'ok:', len(meta), 'objetos')

if __name__ == '__main__':
    bgd = os.path.join(sys.argv[1], 'bgs'); caixas = json.load(open(os.path.join(bgd, 'caixas.json'), encoding='utf-8'))
    for n in (sys.argv[2:] or list(caixas)): build(bgd, n, caixas[n])
