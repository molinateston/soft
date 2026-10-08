"""
kit.py - motor dos criativos "avatar nas pontas + entregavel no meio".
Le de uma pasta de criativo: projeto.json (config), tempo.json (linha do tempo, feita por montar_base.py), roteiro.json (telas)
e, da pasta do kit da oferta, oferta.json (paleta, paginas, regioes, mockup, takes) e bgs/ (fundos).

    python kit.py <pasta_do_criativo> segs                      # linha do tempo: telas e tempos
    python kit.py <pasta_do_criativo> folha folha.jpg           # folha de conferencia automatica (3 quadros por tela)
    python kit.py <pasta_do_criativo> stills folha.jpg 1.2,3.4  # quadros em tempos do video
    python kit.py <pasta_do_criativo> render [processos=6]      # efeitos sonoros + render em partes + mixagem + conferencia

Tempos no roteiro.json sao SEMPRE segundos do audio original; o kit converte para o tempo do video (pausas cortadas, aceleracao).
"""
import os, sys, math, json, subprocess, functools, glob, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PROJ = os.path.abspath(os.environ.get('CRIATIVO') or (sys.argv[1] if len(sys.argv) > 1 else '.'))
import coral_lib as R
import reel_example as X
from coral_lib import F, tw, draw_txt, rrect, circle, E, W, H, card_base, click_ring
from reel_example import slide_text, glow_disc, zoom_cam, round_img, prop2
from engine import place, paste, pixel_ring
from motion import Track, prog, clamp, lerp

def _json(*p): return json.load(open(os.path.join(*p), encoding='utf-8'))
CFG = _json(PROJ, 'projeto.json'); TEMPO = _json(PROJ, 'tempo.json'); ROT = _json(PROJ, 'roteiro.json')
OFERTA = CFG['kit_oferta'] if os.path.isabs(CFG['kit_oferta']) else os.path.normpath(os.path.join(PROJ, CFG['kit_oferta']))
OF = _json(OFERTA, 'oferta.json'); RAIZ = OF.get('raiz') or os.path.dirname(OFERTA)
FPS = float(TEMPO.get('fps', 30)); K = TEMPO['K']; REG = TEMPO['regioes']; DUR = TEMPO['dur']; NF = int(round(DUR * FPS))
SRC = os.path.join(PROJ, 'base.mp4')

# ------------------------------------------------------------------ tempo do audio -> tempo do video
def _kept(ivs, x): return sum(max(0.0, min(b, x) - a) for a, b in ivs)
def T(c):
    v = REG[0]['v0']
    for r in REG:
        if c < r['c0'] - 1e-6: break
        v = r['v0'] + (min(r['vdur'], _kept(r['manter'], c) / K) if r['tipo'] == 'voz' else (r['vdur'] if c >= r['c1'] else 0.0))
    return v

# ------------------------------------------------------------------ paleta (oferta.json)
WHITE = (255, 255, 255); BLACK = (0, 0, 0)
def _rgb(c):
    if isinstance(c, str): c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(int(v) for v in c)
def mix(a, b, p): return tuple(int(round(x + (y - x) * p)) for x, y in zip(a, b))
def _pal(spec):
    d = spec if isinstance(spec, dict) else {'a': spec}; a = _rgb(d['a']); g = lambda k, dv: _rgb(d[k]) if k in d else dv
    p = dict(a=a, l=g('l', mix(a, WHITE, .42)), d=g('d', mix(a, BLACK, .36)), mark=g('mark', mix(a, WHITE, .58)), tint=g('tint', mix(a, WHITE, .82)), base=g('base', (245, 240, 228)))
    p['blob'] = (g('blob0', mix(a, WHITE, .22)), g('blob1', mix(a, BLACK, .18)), g('blob2', mix(a, WHITE, .68))); return p
PALS = {k: _pal(v) for k, v in OF['paleta'].items() if k != 'dark'}
_dk = OF['paleta'].get('dark', {}); _pa = PALS['a']
DARK = dict(base=_rgb(_dk.get('base', mix(_pa['d'], BLACK, .72))), glow=_rgb(_dk.get('glow', mix(_pa['d'], BLACK, .2))), acento=_rgb(_dk.get('acento', _pa['l'])),
            texto=_rgb(_dk.get('texto', (242, 240, 226))), pill=_rgb(_dk.get('pill', mix(_pa['d'], BLACK, .45))))
PALS['dark'] = dict(PALS['a'], blob=(mix(DARK['base'], WHITE, .14), DARK['base'], mix(DARK['acento'], BLACK, .25)))
for _k, _p in PALS.items(): X.PAL[_k] = (_p['l'], _p['d'], mix(_p['d'], BLACK, .2))
INK = _rgb(OF.get('tinta', (34, 40, 32))); GREY = (140, 142, 130); ROW = (249, 247, 239)

# ------------------------------------------------------------------ mancha de transicao (cor por tela)
@functools.lru_cache(None)
def _fill(pal):
    c0, c1, _ = PALS[pal]['blob']; t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    col = np.array(c0, np.float32) * (1 - t) + np.array(c1, np.float32) * t
    return Image.fromarray(np.repeat(col, W, axis=1).astype(np.uint8), 'RGB').convert('RGBA')

def blob(A, B, p, c1, c2, seed, pal):
    """B None = so a metade que cobre; A None = so a metade que abre."""
    ph = p * 7
    if B is None or (p < .5 and A is not None):
        q = min(1.0, p / .5); Rr = lerp(20, R.maxdist(*c1) * 1.32, E('cine', q)); out = A.copy()
        m = R._up(R.blob_alpha(c1[0], c1[1], Rr, seed, ph)); rim = ImageChops.subtract(m, R._up(R.blob_alpha(c1[0], c1[1], Rr * .93, seed, ph)))
    else:
        q = max(0.0, (p - .5) / .5); Rr = lerp(20, R.maxdist(*c2) * 1.32, E('cine', q)); out = B.copy()
        h = R.blob_alpha(c2[0], c2[1], Rr, seed + 3, ph); m = R._up(1 - h)
        rim = ImageChops.multiply(ImageChops.subtract(R._up(R.blob_alpha(c2[0], c2[1], Rr * 1.07, seed + 3, ph)), R._up(h)), m)
    f = _fill(pal).copy(); f.putalpha(m); out.alpha_composite(f)
    rl = Image.new('RGBA', (W, H), PALS[pal]['blob'][2] + (255,)); rl.putalpha(rim.point(lambda v: int(v * .55))); out.alpha_composite(rl)
    return out

# ------------------------------------------------------------------ fundos (bgs/ do kit da oferta; sem arquivo = degrade gerado)
@functools.lru_cache(None)
def _bg_assets(name):
    d = os.path.join(OFERTA, 'bgs'); clean = os.path.join(d, name + '_clean.png')
    if os.path.exists(clean):
        spr = []
        for k, m in enumerate(_json(d, name + '_meta.json')):
            sp = Image.open(os.path.join(d, f"{name}_{m['name']}.png")).convert('RGBA'); a = np.asarray(sp.getchannel('A'))
            spr.append(dict(m=m, sp=sp, ph=(k * .37 + .11) % 1.0, edge=dict(l=a[:, :2].max() > 40, r=a[:, -2:].max() > 40, t=a[:2, :].max() > 40, b=a[-2:, :].max() > 40)))
        return Image.open(clean).convert('RGBA').resize((W, H)), spr
    if name == 'dark': return X._bg(DARK['base'], [(.5, .45, .55, DARK['glow'], .9), (.5, 1.0, .5, mix(DARK['base'], BLACK, .4), .5)]), []
    p = PALS[name]; return X._bg(p['base'], [(.95, .9, .22, p['a'], .34), (.04, .2, .18, p['a'], .16), (.5, .0, .4, mix(p['base'], WHITE, .6), .6)]), []

_BLUR = {}
def _blurred(sp, key, r):
    r = max(0, int(round(r / 2.0)) * 2)
    if r == 0: return sp
    if (key, r) not in _BLUR:
        P_ = Image.new('RGBA', (sp.width + r * 6, sp.height + r * 6), (0, 0, 0, 0)); P_.alpha_composite(sp, (r * 3, r * 3)); _BLUR[(key, r)] = P_.filter(ImageFilter.GaussianBlur(r))
    return _BLUR[(key, r)]

def scene_bg(name, t, t0, gain=1.0):
    """fundo limpo + objetos que entram do centro e flutuam bem devagar."""
    base, sprites = _bg_assets(name); img = base.copy(); sec = 2 * math.pi
    for i, o in enumerate(sprites):
        m, sp, ed, ph = o['m'], o['sp'], o['edge'], o['ph']; typ = m['type']; p = prog(t, t0 + .1 + .13 * i, t0 + 1.15 + .13 * i)
        if p <= 0: continue
        e = E('expo_out', p); cx, cy = m['cx'], m['cy']
        if ed['l'] or ed['r'] or ed['t'] or ed['b']:
            ax = 0 if ed['l'] else (W if ed['r'] else cx); ay = 0 if ed['t'] else (H if ed['b'] else cy)
            s = 1.0 + .04 * (.5 + .5 * math.sin(sec * (t * .085 + ph))) * gain; px = ax + (cx - ax) * s; py = ay + (cy - ay) * s
            if not (ed['l'] or ed['r']): px += 14 * gain * math.sin(sec * (t * .07 + ph))
            if not (ed['t'] or ed['b']): py += 14 * gain * math.sin(sec * (t * .07 + ph))
            vx, vy = ax - cx, ay - cy; n = math.hypot(vx, vy) or 1; px += vx / n * 380 * (1 - e); py += vy / n * 380 * (1 - e); rot = 0.0; sc = s
        else:
            dy = (13 if typ == 'check' else 11) * gain * math.sin(sec * (t * .11 + ph)); dx = 7 * gain * math.cos(sec * (t * .08 + ph * 1.6))
            vx, vy = cx - 540, cy - 960; n = math.hypot(vx, vy) or 1; px = cx + dx + vx / n * 300 * (1 - e); py = cy + dy + vy / n * 300 * (1 - e)
            if typ == 'spark': rot = t * 16 + ph * 90; sc = (1 + .12 * math.sin(sec * (t * .22 + ph))) * (.35 + .65 * E('back_out_x', p))
            else: rot = 4 * gain * math.sin(sec * (t * .07 + ph * 1.3)); sc = .35 + .65 * E('back_out_x', p)
        bl = 12 * (1 - e)
        place(img, _blurred(sp, (name, m['name']), bl) if bl > 1 else sp, px, py, max(.05, sc), clamp(p * 3.5), blur=0, rot=rot)
    return img

# ------------------------------------------------------------------ pecas: disco, check, cartao, pilula, pagina, take, mockup
def _palk(pal): return 'a' if pal == 'dark' else pal

@functools.lru_cache(None)
def disc(size, pal, txt=None, fs=.5):
    top, bot, shc = X.PAL[_palk(pal)]; ss = 2; pad = int(size * .18); c = size + pad * 2
    mask = Image.new('L', (size * ss, size * ss), 0); ImageDraw.Draw(mask).ellipse((0, 0, size * ss - 1, size * ss - 1), fill=255)
    obj = R._shaded(mask, top, bot, (.34, .24, .55, .45))
    if txt: ImageDraw.Draw(obj).text((size * ss / 2, size * ss * .5), txt, font=F('Outfit-Bold', int(size * ss * fs)), fill=(255, 255, 255, 255), anchor='mm')
    L = Image.new('RGBA', (c * ss, c * ss), (0, 0, 0, 0)); sh = Image.new('RGBA', L.size, (0, 0, 0, 0))
    shm = Image.new('RGBA', mask.size, shc + (120,)); shm.putalpha(mask.point(lambda v: int(v * .55)))
    sh.alpha_composite(shm, (pad * ss, pad * ss + int(size * .07 * ss))); sh = sh.filter(ImageFilter.GaussianBlur(size * .06 * ss))
    L.alpha_composite(sh); L.alpha_composite(obj, (pad * ss, pad * ss)); return L.resize((c, c), Image.LANCZOS)

def check(img, cx, cy, size, p, pal):
    if p > 0: place(img, prop2('check', size, _palk(pal)), cx, cy, max(.05, E('back_out_x', p)), clamp(p * 4))

def shadow_card(im, r, pad=50, a=85, dy=16, blur=18):
    im = round_img(im, r); L = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((pad, pad + dy, pad + im.width, pad + dy + im.height), r, fill=(40, 34, 20, a))
    L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur))); L.alpha_composite(im, (pad, pad)); return L

# ================================================================== TEXTOS ANIMADOS (pilulas com "estilo") =====================
# tema por oferta (oferta.json -> "texto"): fonte, fundo e borda da placa, tinta, cor de destaque e cor do marca-texto
TX = OF.get('texto', {}); TXF = TX.get('fonte', 'Jakarta-Bold'); TXBG = _rgb(TX.get('fundo', WHITE)); TXBD = _rgb(TX['borda']) if TX.get('borda') else None
TXINK = _rgb(TX.get('tinta', INK)); TXHI = _rgb(TX.get('destaque', PALS['a']['d'])); TXMK = _rgb(TX.get('marca', PALS['a']['mark'])); TXDOR = _rgb(TX.get('dor', (150, 44, 40)))
SSZ = 560                                                          # altura da faixa onde cada texto e desenhado (centro em SSZ/2)

def _tfit(txt, size, maxw=985, extra=0):
    while size > 34 and tw(txt, TXF, size) + extra > maxw: size -= 2
    return size

@functools.lru_cache(512)
def _placa(w, h, bg=None, bd=-1):
    """placa do texto: fundo, borda dupla fina (como as etiquetas do material) e sombra. Devolve com 44 px de margem."""
    bg = bg or TXBG; bd = TXBD if bd == -1 else bd; pad = 44; ss = 2; r = h // 2
    L = Image.new('RGBA', ((w + pad * 2) * ss, (h + pad * 2) * ss), (0, 0, 0, 0)); sh = Image.new('RGBA', L.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad * ss, (pad + 12) * ss, (pad + w) * ss, (pad + h + 12) * ss), r * ss, fill=(20, 24, 14, 110))
    L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14 * ss))); d = ImageDraw.Draw(L)
    d.rounded_rectangle((pad * ss, pad * ss, (pad + w) * ss, (pad + h) * ss), r * ss, fill=bg + (255,))
    if bd:
        d.rounded_rectangle((pad * ss + 1, pad * ss + 1, (pad + w) * ss - 1, (pad + h) * ss - 1), r * ss, outline=bd + (255,), width=5)
        d.rounded_rectangle(((pad + 8) * ss, (pad + 8) * ss, (pad + w - 8) * ss, (pad + h - 8) * ss), max(2, r - 8) * ss, outline=bd + (140,), width=2)
    return L.resize((w + pad * 2, h + pad * 2), Image.LANCZOS)

def _palavras(txt, size):
    """[(palavra, x, largura)] com x a partir de 0, e a largura total."""
    f = F(TXF, size); sp = f.getlength(' '); x = 0.0; out = []
    for wd in txt.split(' '):
        w = f.getlength(wd); out.append((wd, x, w)); x += w + sp
    return out, x - sp, f

def _limpa(s): return re.sub(r'[^\w]', '', s.lower())
def _e_destaque(wd, dest): return bool(dest) and _limpa(wd) in [_limpa(d) for d in dest.split(' ')]

def _estrela(d, cx, cy, r, col, a=255):
    d.polygon([(cx, cy - r), (cx + r * .24, cy - r * .24), (cx + r, cy), (cx + r * .24, cy + r * .24), (cx, cy + r), (cx - r * .24, cy + r * .24), (cx - r, cy), (cx - r * .24, cy - r * .24)], fill=col + (a,))

def _tx_palavras(S, p, t, ta, ink, hi):
    """palavra por palavra, no ritmo da fala; as palavras de destaque ganham cor e um sublinhado que se desenha."""
    txt = p['texto']; size = _tfit(txt, p.get('tam', 70), extra=96); ws, tot, f = _palavras(txt, size); h = int(size * 1.95); w = int(tot + size * 1.7); cy = SSZ // 2
    pe = prog(t, ta, ta + .4); sc = .82 + .18 * E('back_out', pe)
    place(S, _placa(w, h), 540, cy, sc, clamp(pe * 3), blur=8 * (1 - E('easy_in', pe)))
    tf = T(p['t_fim']) if p.get('t_fim') else ta + .1 + .2 * len(ws); step = max(.07, min(.24, (tf - ta - .1) / max(1, len(ws)))); d = ImageDraw.Draw(S); x0 = 540 - tot / 2
    for i, (wd, x, ww) in enumerate(ws):
        q = prog(t, ta + .1 + i * step, ta + .1 + i * step + .26)
        if q <= 0: continue
        e = E('expo_out', q); hl = _e_destaque(wd, p.get('destaque')); col = hi if hl else ink
        if hl:
            u = E('expo_out', prog(t, ta + .1 + i * step + .12, ta + .1 + i * step + .5))
            if u > 0: d.line([(x0 + x - 2, cy + size * .46), (x0 + x - 2 + (ww + 4) * u, cy + size * .46)], fill=TXMK + (255,), width=max(5, size // 9))
        d.text((x0 + x, cy + 16 * (1 - e)), wd, font=f, fill=col + (int(255 * clamp(q * 2.5)),), anchor='lm')

def _tx_marca(S, p, t, ta, ink, hi):
    """o texto entra inteiro e um marca-texto passa por tras das palavras de destaque."""
    txt = p['texto']; size = _tfit(txt, p.get('tam', 70), extra=96); ws, tot, f = _palavras(txt, size); h = int(size * 1.95); w = int(tot + size * 1.7); cy = SSZ // 2
    pe = prog(t, ta, ta + .45); L = Image.new('RGBA', (W, SSZ), (0, 0, 0, 0)); L.alpha_composite(_placa(w, h), (int(540 - w / 2 - 44), int(cy - h / 2 - 44))); d = ImageDraw.Draw(L); x0 = 540 - tot / 2
    tm = T(p['t_marca']) if p.get('t_marca') else ta + .4; mk = _rgb(p['cor_marca']) if p.get('cor_marca') else TXMK; dw = [(x, ww) for wd, x, ww in ws if _e_destaque(wd, p.get('destaque'))]
    if dw:
        xa = x0 + dw[0][0] - 8; xb = x0 + dw[-1][0] + dw[-1][1] + 8; ph = E('expo_inout', prog(t, tm, tm + .45))
        if ph > .01: d.rounded_rectangle((xa, cy - size * .40, xa + (xb - xa) * ph, cy + size * .44), 9, fill=mk + (255,))
    d.text((x0, cy), txt, font=f, fill=ink + (255,), anchor='lm')
    place(S, L, 540, cy + 40 * (1 - E('expo_out', pe)), .8 + .2 * E('back_out', pe), clamp(pe * 3), blur=9 * (1 - E('easy_in', pe)))

def _tx_soltas(S, p, t, ta, ink, hi):
    """cada palavra na sua propria plaquinha, caindo solta e ficando levemente torta."""
    wds = p['texto'].split(' '); size = p.get('tam', 62); gap = 12
    while True:
        f = F(TXF, size); h = int(size * 1.75); ws = [int(f.getlength(x) + size * 1.0) for x in wds]; tot = sum(ws) + gap * (len(wds) - 1)
        if tot <= 1010 or size <= 34: break
        size -= 2
    x = 540 - tot / 2; cy = SSZ // 2; rots = [-5, 4, -3, 6, -4, 3, -6, 5]; dys = [6, -8, 10, -4, 8, -10, 4, -6]
    for i, wd in enumerate(wds):
        q = prog(t, ta + i * .13, ta + i * .13 + .5)
        if q > 0:
            e = E('back_out', q); pl = _placa(ws[i], h).copy(); hl = _e_destaque(wd, p.get('destaque'))
            ImageDraw.Draw(pl).text((44 + ws[i] / 2, 44 + h / 2 + 1), wd, font=f, fill=(hi if hl else ink) + (255,), anchor='mm')
            wob = 2.0 * math.sin(2 * math.pi * (t * .35 + i * .21))
            place(S, pl, x + ws[i] / 2, cy + dys[i % 8] - 150 * (1 - E('expo_out', q)), 1.0, clamp(q * 4), blur=8 * (1 - E('easy_in', q)), rot=rots[i % 8] * e + 26 * (1 - E('expo_out', q)) + wob)
        x += ws[i] + gap

def _tx_faixa(S, p, t, ta, ink, hi):
    """faixa (como as faixas de titulo do material) que se desenrola do centro, com o texto e um brilho de estrelas."""
    txt = p['texto']; size = _tfit(txt, p.get('tam', 78), maxw=800); f = F(TXF, size); tot = f.getlength(txt); h = int(size * 2.0); w = int(tot + size * 2.2); cy = SSZ // 2
    pe = prog(t, ta, ta + .6); e = E('expo_out', pe)
    if pe <= 0: return
    bd = TXBD or mix(TXBG, BLACK, .25); esc = mix(TXBG, bd, .7); L = Image.new('RGBA', (W, SSZ), (0, 0, 0, 0)); d = ImageDraw.Draw(L); pt = E('back_out', prog(t, ta + .32, ta + .75)); tl = 64 * pt
    if tl > 2:                                                     # pontas da faixa, atras, com recorte em V
        for sg in (-1, 1):
            xe = 540 + sg * (w / 2 - 26); xo = xe + sg * tl; yt, yb = cy - h / 2 + 22, cy + h / 2 + 22
            d.polygon([(xe, yt), (xo, yt), (xo - sg * 24, (yt + yb) / 2), (xo, yb), (xe, yb)], fill=esc + (255,)); d.polygon([(xe, cy + h / 2), (xe, yb), (xe + sg * 26, cy + h / 2)], fill=mix(esc, BLACK, .3) + (255,))
    full = Image.new('RGBA', (w + 88, h + 88), (0, 0, 0, 0)); sh = Image.new('RGBA', full.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((44, 56, 44 + w, 56 + h), fill=(20, 24, 14, 110)); full.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    df = ImageDraw.Draw(full); df.rectangle((44, 44, 44 + w, 44 + h), fill=mix(TXBG, WHITE, .45) + (255,)); df.rectangle((44, 44, 44 + w, 44 + h), outline=bd + (255,), width=5); df.rectangle((55, 55, 33 + w, 33 + h), outline=bd + (170,), width=2)
    df.text((44 + w / 2, 44 + h / 2 + 1), txt, font=f, fill=ink + (int(255 * prog(t, ta + .22, ta + .55)),), anchor='mm')
    wv = max(8, int((w + 88) * e)); L.alpha_composite(full.crop(((w + 88 - wv) // 2, 0, (w + 88 + wv) // 2, h + 88)), (int(540 - wv / 2), int(cy - h / 2 - 44)))
    q = prog(t, ta + .28, ta + 1.15)
    if 0 < q < 1:
        for ax, ay, r in [(-1, -.9, 22), (1, -.8, 26), (-.8, 1, 18), (.85, .95, 22), (0, -1.25, 16), (.35, 1.2, 14), (-1.15, 0, 14), (1.15, .1, 16)]:
            g = E('expo_out', q); _estrela(d, 540 + (w / 2 + 30) * ax * (.75 + .45 * g), cy + (h / 2 + 34) * ay * (.75 + .45 * g), r * (.4 + .8 * math.sin(math.pi * q)), TXBD or hi, int(255 * (1 - q) ** .6))
    S.alpha_composite(L)

def _mini_icone(kind, D, u, fg):
    """icone pequeno e animado (u = segundos desde a entrada), desenhado em 2x num quadrado D."""
    s2 = D * 2; I = Image.new('RGBA', (s2, s2), (0, 0, 0, 0)); d = ImageDraw.Draw(I); c = s2 / 2; cl = fg + (255,); lw = max(6, s2 // 13)
    if kind == 'relogio':
        r = s2 * .30; d.ellipse((c - r, c - r, c + r, c + r), outline=cl, width=lw); a = -90 + 720 * E('expo_out', clamp(u / 1.1)) + 28 * max(0.0, u - 1.1)
        d.line([(c, c), (c + r * .72 * math.cos(math.radians(a)), c + r * .72 * math.sin(math.radians(a)))], fill=cl, width=lw)
        d.line([(c, c), (c + r * .45 * math.cos(math.radians(a / 12 - 60)), c + r * .45 * math.sin(math.radians(a / 12 - 60)))], fill=cl, width=lw)
    elif kind == 'livro':
        w_, h_ = s2 * .30, s2 * .38
        d.polygon([(c - w_, c - h_ * .5), (c, c - h_ * .36), (c, c + h_ * .62), (c - w_, c + h_ * .48)], outline=cl, width=lw); d.polygon([(c + w_, c - h_ * .5), (c, c - h_ * .36), (c, c + h_ * .62), (c + w_, c + h_ * .48)], outline=cl, width=lw)
        k = clamp(((u * .9) % 1.0) * 1.6); px = c + w_ * math.cos(math.pi * E('expo_inout', k))          # uma pagina virando
        d.line([(c, c - h_ * .36), (px, c - h_ * (.5 + .12 * math.sin(math.pi * k))), (px, c + h_ * (.48 - .12 * math.sin(math.pi * k))), (c, c + h_ * .62)], fill=cl, width=max(4, lw - 2), joint='curve')
    elif kind == 'check':
        a_, b_, c_ = (c - s2 * .20, c + s2 * .02), (c - s2 * .05, c + s2 * .17), (c + s2 * .22, c - s2 * .15); q = E('expo_out', clamp((u - .12) / .45))
        if q > 0:
            m = min(1.0, q / .4); seg = [a_, (a_[0] + (b_[0] - a_[0]) * m, a_[1] + (b_[1] - a_[1]) * m)]
            if q > .4: m2 = (q - .4) / .6; seg = [a_, b_, (b_[0] + (c_[0] - b_[0]) * m2, b_[1] + (c_[1] - b_[1]) * m2)]
            d.line(seg, fill=cl, width=lw + 4, joint='curve')
    elif kind in ('interrogacao', 'x'):
        ch = '?' if kind == 'interrogacao' else 'x'; J = Image.new('RGBA', (s2, s2), (0, 0, 0, 0))
        ImageDraw.Draw(J).text((c, c - (0 if ch == '?' else s2 * .05)), ch, font=F('Outfit-Bold', int(s2 * (.62 if ch == '?' else .7))), fill=cl, anchor='mm')
        I.alpha_composite(J.rotate(16 * math.sin(u * 9) * math.exp(-u * 1.1) + 5 * math.sin(u * 2.2), resample=Image.BICUBIC))
    elif kind == 'brilho':
        for k, (dx, dy, r) in enumerate([(0, 0, .30), (.24, -.22, .14), (-.24, .2, .12)]): _estrela(d, c + dx * s2, c + dy * s2, s2 * r * (.75 + .25 * math.sin(u * 5 + k * 2)), fg)
    return I.resize((D, D), Image.LANCZOS)

def _pessoas(Wd, Hd, u, cols, borda):
    """tres cabecinhas que surgem uma a uma (prova social)."""
    I = Image.new('RGBA', (Wd * 2, Hd * 2), (0, 0, 0, 0)); r = Hd * .88
    for k in (2, 1, 0):
        q = clamp((u - .12 * k) / .4)
        if q <= 0: continue
        cx = r * 1.12 + k * r * 1.12; cy = Hd; J = Image.new('RGBA', I.size, (0, 0, 0, 0)); dj = ImageDraw.Draw(J); rr = r * E('back_out', q)
        dj.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=cols[k % len(cols)] + (255,), outline=borda + (255,), width=6)
        dj.ellipse((cx - rr * .30, cy - rr * .56, cx + rr * .30, cy + rr * .04), fill=borda + (255,)); dj.pieslice((cx - rr * .58, cy + rr * .16, cx + rr * .58, cy + rr * 1.32), 180, 360, fill=borda + (255,))
        I.alpha_composite(J)
    return I.resize((Wd, Hd), Image.LANCZOS)

def _tx_icone(S, p, t, ta, ink, hi):
    """um icone animado surge e a placa se abre a partir dele, revelando o texto."""
    txt = p['texto']; kind = p.get('icone', 'check'); size = _tfit(txt, p.get('tam', 68), extra=330 if kind == 'pessoas' else 215); f = F(TXF, size); tot = f.getlength(txt); h = int(size * 1.95); cy = SSZ // 2
    iw = int(h * 2.0) if kind == 'pessoas' else h; w = int(iw + 12 + tot + size * .85); x0 = 540 - w / 2; p0 = prog(t, ta, ta + .34); ex = E('expo_inout', prog(t, ta + .2, ta + .75))
    if p0 <= 0: return
    wc = int(lerp(iw + (8 if kind == 'pessoas' else 0), w, ex)) // 2 * 2
    if p0 > .25: S.alpha_composite(_placa(wc, h), (int(x0 - 44), int(cy - h / 2 - 44)))
    u = t - ta; cor = _rgb(p['cor_icone']) if p.get('cor_icone') else (TXDOR if kind in ('interrogacao', 'x') else ink)
    if kind == 'pessoas': S.alpha_composite(_pessoas(iw - 16, h - 22, u, [TXMK, mix(TXINK, WHITE, .35), mix(TXDOR, WHITE, .25)], ink), (int(x0 + 12), int(cy - (h - 22) / 2)))
    else:
        r = (h / 2 - 9) * max(.05, E('back_out', p0)); bx = x0 + h / 2; ImageDraw.Draw(S).ellipse((bx - r, cy - r, bx + r, cy + r), fill=cor + (255,))
        if p0 > .3: ic = _mini_icone(kind, int(h - 18), u, TXBG); S.alpha_composite(ic, (int(bx - ic.width / 2), int(cy - ic.height / 2)))
    vis = int(wc - iw - 12 - size * .3)
    if vis > 4:
        Tm = Image.new('RGBA', (int(tot) + 6, h), (0, 0, 0, 0)); dt = ImageDraw.Draw(Tm); ws, _, _ = _palavras(txt, size)
        for wd, x, ww in ws: dt.text((x, h / 2 + 1), wd, font=f, fill=(hi if _e_destaque(wd, p.get('destaque')) else ink) + (255,), anchor='lm')
        S.alpha_composite(Tm.crop((0, 0, min(Tm.width, vis), h)), (int(x0 + iw + 12), int(cy - h / 2)))

def _tx_grande(S, p, t, ta, ink, hi):
    """texto grande, sem placa: cada linha sobe de dentro de uma mascara; o destaque muda de cor e ganha um traco."""
    lines = p['texto'].split('|'); size = p.get('tam', 104)
    while size > 50 and max(tw(l, TXF, size) for l in lines) > 960: size -= 2
    f = F(TXF, size); lh = int(size * 1.16); cy0 = SSZ // 2 - lh * (len(lines) - 1) / 2; esc = p.get('escuro'); c1 = DARK['texto'] if esc else ink; c2 = DARK['acento'] if esc else hi
    for i, ln in enumerate(lines):
        q = prog(t, ta + i * .14, ta + i * .14 + .6)
        if q <= 0: continue
        e = E('expo_out', q); ws, tot, _ = _palavras(ln, size); M = Image.new('RGBA', (int(tot) + 20, lh + 8), (0, 0, 0, 0)); dm = ImageDraw.Draw(M)
        for wd, x, ww in ws:
            hl = _e_destaque(wd, p.get('destaque'))
            if not esc: dm.text((10 + x + 3, lh / 2 + 5 + lh * .95 * (1 - e)), wd, font=f, fill=(255, 255, 255, 150), anchor='lm')
            dm.text((10 + x, lh / 2 + 2 + lh * .95 * (1 - e)), wd, font=f, fill=(c2 if hl else c1) + (255,), anchor='lm')
            if hl:
                u = E('expo_out', prog(t, ta + i * .14 + .4, ta + i * .14 + .85))
                if u > 0: dm.line([(10 + x, lh - 4), (10 + x + ww * u, lh - 4)], fill=c2 + (255,), width=max(6, size // 13))
        S.alpha_composite(M, (int(540 - M.width / 2), int(cy0 + i * lh - lh / 2)))

ESTILOS = {'palavras': _tx_palavras, 'marca': _tx_marca, 'soltas': _tx_soltas, 'faixa': _tx_faixa, 'icone': _tx_icone, 'grande': _tx_grande}

def texto_anim(img, p, t, y):
    """pilula com 'estilo': palavras | marca | soltas | faixa | icone | grande. Saida igual para todos (sobe, desfoca e some)."""
    ta = T(p['t']); tb = T(p['t_sai']) if p.get('t_sai') is not None else None
    if t < ta: return
    o = prog(t, tb, tb + .3) if tb is not None else 0.0
    if o >= 1: return
    S = Image.new('RGBA', (W, SSZ), (0, 0, 0, 0)); ESTILOS[p['estilo']](S, p, t, ta, TXINK, TXDOR if p.get('dor') else TXHI)
    place(img, S, 540, y - 30 * o, 1.0, 1 - o, blur=8 * o)

def _cue_texto(p):
    ta = T(p['t']); est = p['estilo']; n = len(p['texto'].replace('|', ' ').split(' '))
    if est == 'palavras':
        cue(ta, 'pop', g=.55)
        for i in range(min(n, 6)): cue(ta + .1 + i * .2, 'plim', g=.22, f=(880, 988, 1047, 1175)[i % 4])
    elif est == 'marca': cue(ta, 'pop', g=.55); cue((T(p['t_marca']) if p.get('t_marca') else ta + .4), 'swoosh', g=.32, dur=.35, seed=31, fc=900)
    elif est == 'soltas':
        for i in range(n): cue(ta + i * .13, 'plim', g=.35, f=(523, 587, 494, 659, 440, 587)[i % 6])
    elif est == 'faixa': cue(ta, 'swoosh', g=.4, dur=.5, seed=33, fc=760); cue(ta + .3, 'plim', g=.5, f=988); cue(ta + .42, 'plim', g=.4, f=1319)
    elif est == 'icone': cue(ta, 'pop', g=.65); cue(ta + .22, 'swoosh', g=.3, dur=.4, seed=35, fc=820)
    elif est == 'grande':
        for i in range(len(p['texto'].split('|'))): cue(ta + i * .14, 'swoosh', g=.33, dur=.4, seed=37 + i, fc=700)
        cue(ta + .45, 'plim', g=.4, f=784)

@functools.lru_cache(None)
def chip_spr(txt, size=62, fg=None, bgc=None, font=None):
    """pilula simples (sem 'estilo'): mesma placa e fonte do tema da oferta."""
    font = font or TXF; fg = fg or TXINK
    while size > 36 and tw(txt, font, size) + size * 1.6 > 980: size -= 2          # cabe na largura da tela
    f = F(font, size); h = int(size * 1.95); w = int(f.getlength(txt)) + int(size * 1.6)
    L = _placa(w, h, bgc).copy(); ImageDraw.Draw(L).text((44 + w / 2, 44 + h / 2 + 1), txt, font=f, fill=fg + (255,), anchor='mm'); return L

def chip_at(img, txt, cy, t, ta, tb=None, size=62, cx=540, a=1.0, font=None):
    """pilula de texto que entra em ta e (se tb) sai em tb."""
    if not txt or ta is None: return
    p = prog(t, ta, ta + .5); o = prog(t, tb, tb + .3) if tb else 0.0
    if p > 0 and o < 1:
        place(img, chip_spr(txt, size, font=font), cx, cy + 44 * (1 - E('expo_out', p)) - 30 * o, .7 + .3 * E('back_out', p), clamp(p * 3) * (1 - o) * a, blur=10 * (1 - E('easy_in', p)) + 8 * o)

def _path(p): return p if os.path.isabs(p) else os.path.join(RAIZ, p)

@functools.lru_cache(None)
def page_raw(pid):
    im = Image.open(_path(OF['paginas'][pid])).convert('RGB')
    return im if im.width == 1024 else im.resize((1024, round(im.height * 1024 / im.width)), Image.LANCZOS)   # regioes sao em 1024 de largura

@functools.lru_cache(None)
def page(pid, w):
    r = page_raw(pid); im = r.resize((w, round(r.height * w / r.width)), Image.LANCZOS)
    return shadow_card(im, max(10, int(w * .035)), pad=max(24, w // 10), a=80, dy=max(6, w // 40), blur=max(8, w // 30))

def PGH(pid, w): r = page_raw(pid); return w * r.height / r.width          # altura da pagina na largura w
def region(pid, r): return tuple(r) if isinstance(r, (list, tuple)) else tuple(OF['regioes'][pid][r])
def ALLP(): return [k for k in OF['paginas'] if k != OF.get('capa', 'capa')]

@functools.lru_cache(None)
def mockup(w):
    im = Image.open(_path(OF['mockup'])).convert('RGBA'); return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)

_TK = {}
def take(name, fi):
    if name not in _TK: _TK[name] = np.load(os.path.join(OFERTA, 'takes', name + '.npy'), mmap_mode='r')
    a = _TK[name]; return np.asarray(a[max(0, min(len(a) - 1, int(fi)))])

def take_card(name, t, ta, speed, w, h, r=50, z1=1.05, zdur=4.0, cyf=.5, border=10):
    im = Image.fromarray(take(name, (t - ta) * 30 * speed)); sw, sh = im.size; ar = w / h
    cw, ch = (sw, sw / ar) if ar >= sw / sh else (sh * ar, sh)
    z = lerp(1.0, z1, prog(t, ta, ta + zdur)); cw /= z; ch /= z; x0 = (sw - cw) / 2; y0 = clamp(sh * cyf - ch / 2, 0, sh - ch)
    im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.BICUBIC)
    base, pad = card_base(w + border * 2, h + border * 2, r + border); c = base.copy(); c.alpha_composite(round_img(im, r), (pad + border, pad + border)); return c

def ring_box(img, box, lx, ly, sc, col, a, pulse=0.0):
    x0, y0, x1, y1 = box; w, h = int((x1 - x0) * sc) + 44, int((y1 - y0) * sc) + 44
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(L).rounded_rectangle((12, 12, w - 12, h - 12), 28, outline=col + (int(255 * clamp(a)),), width=9)
    place(img, L, lx + (x0 + x1) / 2 * sc, ly + (y0 + y1) / 2 * sc, 1 + pulse, 1.0)

def _icon(c0, kind, cx0, cy0, col):
    c = Image.new('RGBA', (60, 60), (0, 0, 0, 0)); cx = cy = 30; d = ImageDraw.Draw(c); cl = col + (255,); kind %= 3
    if kind == 0:
        d.rounded_rectangle((cx - 22, cy - 17, cx + 22, cy + 17), 7, outline=cl, width=5); d.ellipse((cx + 5, cy - 10, cx + 13, cy - 2), fill=cl)
        d.line([(cx - 16, cy + 10), (cx - 5, cy - 3), (cx + 4, cy + 6), (cx + 9, cy + 1), (cx + 16, cy + 10)], fill=cl, width=5, joint='curve')
    elif kind == 1:
        for k, wd in enumerate((40, 40, 24)): d.rounded_rectangle((cx - 20, cy - 16 + k * 13, cx - 20 + wd, cy - 10 + k * 13), 3, fill=cl)
    else:
        d.ellipse((cx - 21, cy - 21, cx + 21, cy + 21), outline=cl, width=5); d.line([(cx, cy - 11), (cx, cy), (cx + 9, cy + 6)], fill=cl, width=5, joint='curve')
    c0.alpha_composite(c.resize((78, 78), Image.LANCZOS), (int(cx0 - 39), int(cy0 - 39)))

def checklist(t, pal, rows):
    """rows = [(rotulo, t_inicio, t_check)]"""
    P = PALS[pal]; n = len(rows); w, h = 900, 84 + n * 172; base, pad = card_base(w, h); c = base.copy(); ox, oy = pad, pad
    for i, (lab, ts, tk) in enumerate(rows):
        y = oy + 44 + i * 172; act = prog(t, ts, ts + .3) * (1 - prog(t, tk + .1, tk + .5)); dn = prog(t, tk, tk + .5)
        rrect(c, (ox + 32, y, ox + w - 32, y + 144), 40, mix(ROW, P['tint'], E('easy', act)))
        rrect(c, (ox + 56, y + 28, ox + 144, y + 116), 26, WHITE if act > .5 else P['tint']); _icon(c, i, ox + 100, y + 72, P['d'])
        size = 49
        while size > 34 and tw(lab, TXF, size) > w - 174 - 150: size -= 2
        draw_txt(c, (ox + 174, y + 73), lab, TXF, size, TXINK, 'lm'); bx, by = ox + w - 32 - 74, y + 72
        if dn < 1: ImageDraw.Draw(c).ellipse((bx - 34, by - 34, bx + 34, by + 34), outline=(206, 208, 192, int(255 * (1 - dn))), width=5)
        check(c, bx, by, 76, dn, pal)
        pr = prog(t, tk + .02, tk + .55)
        if 0 < pr < 1: click_ring(c, bx, by, pr, P['a'])
    return c

def week_card(t, pal, td0, step):
    w, h = 880, 270; base, pad = card_base(w, h); c = base.copy(); ox, oy = pad, pad
    for i, l in enumerate(OF.get('dias', 'STQQSSD')):
        x = ox + 98 + i * 114; y = oy + 168; p = prog(t, td0 + i * step, td0 + i * step + .45)
        draw_txt(c, (x, oy + 66), l, 'Jakarta-Bold', 34, GREY if p < .5 else INK, 'mm')
        if p < 1: ImageDraw.Draw(c).ellipse((x - 42, y - 42, x + 42, y + 42), outline=(226, 222, 204, 255), width=5)
        check(c, x, y, 92, p, pal)
    return c

def arrows(img, t, ta, y0=1560, col=(255, 255, 255), shadow=True):
    """tres setas para baixo em cascata (CTA)."""
    for k in range(3):
        p = prog(t, ta + k * .1, ta + k * .1 + .5)
        if p <= 0: continue
        y = y0 + k * 92; a = .35 + .65 * max(0.0, math.sin(2 * math.pi * (1.35 * (t - ta) - k * .17))) ** 2; dy = 14 * math.sin(2 * math.pi * 1.35 * (t - ta)) ** 2
        L = Image.new('RGBA', (300, 180), (0, 0, 0, 0))
        if shadow:
            sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).line([(60, 58), (150, 130), (240, 58)], fill=(0, 0, 0, 150), width=26, joint='curve'); L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
        d = ImageDraw.Draw(L); d.line([(60, 50), (150, 122), (240, 50)], fill=col + (255,), width=22, joint='curve')
        for px in (60, 240): d.ellipse((px - 11, 39, px + 11, 61), fill=col + (255,))
        place(img, L, 540, y + dy - 40 * (1 - E('expo_out', p)), .7 + .3 * E('back_out', p), clamp(p * 3) * a, blur=8 * (1 - p))

def _chips(img, c, t, y=1700, size=62):
    """pilulas da cena: 'pilula'+'t_pilula' (uma) e/ou 'pilulas': [{texto, t, t_sai, y}]"""
    if c.get('pilula'): chip_at(img, c['pilula'], c.get('y_pilula', y), t, T(c['t_pilula']), size=size)
    for p in c.get('pilulas', []):
        if p.get('estilo'): texto_anim(img, p, t, p.get('y', y))
        else: chip_at(img, p['texto'], p.get('y', y), t, T(p['t']), T(p['t_sai']) if p.get('t_sai') is not None else None, size=p.get('tam', size))

def _cam(img, t, t0, t1, z=1.04): return zoom_cam(img, t, [(t0, 1.0), (t0 + .6, 1.0, 'cine'), (t1, z)])

# ================================================================== CENAS (todas mostram o material) ============================
CUES = []
def cue(t, kind, **kw): CUES.append(dict(t=round(max(0.0, t), 3), kind=kind, **kw))
def _cue_chips(c):
    if c.get('pilula'): cue(T(c['t_pilula']), 'pop', g=.6)
    for p in c.get('pilulas', []):
        if p.get('estilo'): _cue_texto(p)
        else: cue(T(p['t']), 'pop', g=.6)

def cena_parede(c, t0):
    """parede de paginas correndo em 3 colunas, inclinada; opcional: uma pagina salta para a frente (destaque, t_destaque)."""
    ids = c.get('paginas') or ALLP(); cols = c.get('colunas') or [[ids[(ci * 5 + k * 3 + ci) % len(ids)] for k in range(6)] for ci in range(3)]
    pop = c.get('destaque'); tp = T(c['t_destaque']) if pop else None
    cue(t0 + .05, 'swoosh', g=.45, dur=.8, seed=11, fc=520); _cue_chips(c)
    if pop: cue(tp, 'pop', g=.75); cue(tp + .1, 'plim', g=.5, f=784)
    def fn(t, t0, t1, pal):
        img = scene_bg(pal, t, t0); LW, LH = 1500, 2600; L = Image.new('RGBA', (LW, LH), (0, 0, 0, 0)); pw = 340; n = len(cols[0])
        step = int(PGH(cols[0][0], pw)) + 50; kick = 520 * (1 - E('expo_out', prog(t, t0, t0 + 1.2)))
        for ci, col in enumerate(cols):
            dr = -1 if ci % 2 == 0 else 1; off = dr * (62 * (t - t0) + kick) + ci * 190; pe = prog(t, t0 + .05 + ci * .09, t0 + .7 + ci * .09)
            if pe <= 0: continue
            x = LW // 2 + (ci - 1) * 395
            for k, pid in enumerate(col):
                y = ((k * step + off) % (n * step)) - step + 100
                if -400 < y < LH + 400:
                    sp = page(pid, pw); paste(L, sp, (x - sp.width / 2, y - sp.height / 2 + dr * 300 * (1 - E('expo_out', pe))), clamp(pe * 2.5))
        place(img, L, 540, 960, 1.0, 1.0, rot=7)
        if pop:
            pp = prog(t, tp, tp + .7)
            if pp > 0:
                img.alpha_composite(Image.new('RGBA', (W, H), mix(PALS[pal]['base'], WHITE, .2) + (int(110 * E('expo_out', pp)),)))
                place(img, page(pop, 760), 540, 900 + 220 * (1 - E('expo_out', pp)), max(.05, .55 + .45 * E('back_out', pp)) * lerp(1, 1.04, prog(t, tp, t1)), clamp(pp * 3.5), blur=14 * (1 - E('easy_in', pp)), rot=-2.5 * E('expo_out', pp))
        _chips(img, c, t); return _cam(img, t, t0, t1)
    return fn

def cena_carrossel(c, t0):
    """uma pagina grande no centro e as vizinhas menores dos lados; cada uma fica 'passo' segundos no centro."""
    ids = c['paginas']; cue(t0 + .05, 'swoosh', g=.4, dur=.5, seed=12, fc=620); _cue_chips(c)
    def fn(t, t0, t1, pal):
        step = c.get('passo') or max(.9, (t1 - t0 - .35) / len(ids))
        img = scene_bg(pal, t, t0); pin = prog(t, t0 + .02, t0 + .6); tt = t - t0 - .35
        k0 = int(tt / step) if tt > 0 else 0; q = clamp((tt - k0 * step - (step - .55)) / .55) if tt > 0 else 0; u = min(len(ids) - 1, k0 + E('expo_inout', q))
        for k in sorted(range(len(ids)), key=lambda k: -abs(k - u)):
            d = k - u
            if abs(d) > 2.2: continue
            place(img, page(ids[k], 760), 540 + d * 560, 860 + 300 * (1 - E('expo_out', pin)) + 34 * min(1, abs(d)), 1 - .26 * min(1.0, abs(d)),
                  (1 - .30 * min(1.0, abs(d))) * clamp(pin * 2.5) * clamp(2.2 - abs(d)), blur=4 * min(1, abs(d)))
        _chips(img, c, t); return _cam(img, t, t0, t1)
    return fn

def cena_destaque(c, t0):
    """uma pagina grande; 'marcas' [{t, regiao, texto}] = a moldura vai para a regiao e uma pilula se soma embaixo."""
    pid = c['pagina']; marks = [(T(m['t']), region(pid, m['regiao']) if m.get('regiao') else None, m.get('texto')) for m in c.get('marcas', [])]
    cue(t0 + .05, 'swoosh', g=.4, dur=.5, seed=13, fc=620); _cue_chips(c)
    for i, (tm, _, _) in enumerate(marks): cue(tm, 'pop', g=.55); cue(tm, 'plim', g=.5, f=(660, 784, 988, 1175)[i % 4])
    def fn(t, t0, t1, pal):
        P = PALS[pal]; img = scene_bg(pal, t, t0); nm = sum(1 for m in marks if m[2]); pw = 800 if nm else 860
        px, py = 540, (150 + PGH(pid, pw) / 2 if nm else 900); sc = pw / 1024; pe = prog(t, t0 + .04, t0 + .85)
        if pe > 0: place(img, page(pid, pw), px, py + 340 * (1 - E('expo_out', pe)), (.92 + .08 * E('expo_out', pe)) * lerp(1, 1.03, prog(t, t0, t1)), clamp(pe * 3.5), blur=18 * (1 - E('easy_in', pe)))
        lx, ly = px - pw / 2, py - PGH(pid, pw) / 2; act = [i for i, m in enumerate(marks) if t >= m[0] and m[1]]
        if act:
            i = act[-1]; tm, box, _ = marks[i]; g = E('expo_inout', prog(t, tm, tm + .45)); prev = [m[1] for m in marks[:i] if m[1]]
            bx = tuple(lerp(a, b, g) for a, b in zip(prev[-1] if prev else box, box)); ring_box(img, bx, lx, ly, sc, P['a'], prog(t, marks[act[0]][0], marks[act[0]][0] + .3), .012 * math.sin(t * 6))
        k = 0
        for tm, box, txt in marks:
            if txt: chip_at(img, txt, 1420 + (3 - nm) * 60 + k * 138, t, tm, size=58); k += 1
        _chips(img, c, t); return _cam(img, t, t0, t1)
    return fn

def cena_capa(c, t0):
    """folheando as paginas ate parar na capa (t_capa); selo (t_selo); as paginas abrem em leque atras dela (t_leque)."""
    strip = c['tira']; tl = T(c['t_capa']); tb = T(c['t_selo']) if c.get('selo') else None; fan = c.get('leque', []); tf = T(c['t_leque']) if fan else None
    offs = [(-300, -19), (-160, -9.5), (160, 9.5), (300, 19)]
    cue(t0 + .2, 'riser', g=.38, dur=max(.3, tl - t0 - .2)); cue(tl, 'sub_hit', g=.45); cue(tl, 'pop', g=.7); _cue_chips(c)
    if tb: cue(tb, 'pop', g=.8); cue(tb, 'plim', g=.55, f=988)
    if fan: cue(tf, 'swoosh', g=.35, dur=.45, seed=62)
    def fn(t, t0, t1, pal):
        img = scene_bg(pal, t, t0); cx, cy = 540, 960; gap = 780
        tr = Track([(t0 + .1, 0.0, 'cine'), (tl, (len(strip) - 1) * gap)]); off = tr(t); land = prog(t, tl - .05, tl + .5); v = abs(tr(t + .012) - tr(t - .012))
        for k, pid in enumerate(fan[:4]):
            p = prog(t, tf + .07 * abs(k - 1.5), tf + .7 + .07 * abs(k - 1.5))
            if p <= 0: continue
            e = E('expo_out', p); dx, rot = offs[k]
            place(img, page(pid, 640), cx + dx * 1.12 * e, cy + 46 * abs(dx) / 300 * e + 6 * math.sin(2 * math.pi * (t * .2 + k * .23)), .9, clamp(p * 4), rot=-rot * E('back_out', p))
        pin = prog(t, t0 + .05, t0 + .5)
        for k, pid in enumerate(strip):
            x = cx + k * gap - off; last = k == len(strip) - 1
            if x < -450 or x > W + 450: continue
            place(img, page(pid, 720), x, cy + 320 * (1 - E('expo_out', pin)), (1 + .06 * math.sin(math.pi * clamp(land))) if last else 1.0, clamp(pin * 2) * (1.0 if last else 1 - land), blur=min(16, v * .9))
        if tb:
            pb = prog(t, tb, tb + .7)
            if pb > 0:
                bx, by = 890, int(cy - PGH(strip[-1], 720) / 2 + 20)
                sv = str(c['selo']); sv = str(int(round(int(sv) * E('expo_out', prog(t, tb + .05, tb + .85))))) if sv.isdigit() else sv   # numero conta de 0 ate o valor
                place(img, disc(220, pal, sv, .5 if len(str(c['selo'])) <= 2 else .36), bx, by, max(.05, E('back_out_x', pb)), clamp(pb * 4), rot=-12 * (1 - E('expo_out', pb)))
                pixel_ring(img, bx, by, prog(t, tb + .04, tb + .7), r0=110, r1=300, cell=13, color=PALS[pal]['a'], seed=7, count=140)
        _chips(img, c, t); return _cam(img, t, t0, t1, 1.05)
    return fn

def cena_lista(c, t0):
    """pagina em cima + checklist embaixo; a cada item (rotulo, t_inicio, t_check, regiao) um pedaco da pagina salta em zoom
    (o 1o item so ganha moldura); em t_crescer o checklist sai e a pagina cresce e fica na tela."""
    pid = c['pagina']; items = c['itens']; rows = [(i['rotulo'], T(i['t_inicio']), T(i['t_check'])) for i in items]
    boxes = [region(pid, i['regiao']) if i.get('regiao') else None for i in items]; has_tx = c.get('t_crescer') is not None; tx = T(c['t_crescer']) if has_tx else 1e9
    cue(t0 + .05, 'swoosh', g=.4, dur=.5, seed=14, fc=620); _cue_chips(c)
    for i, (lab, ts, tk) in enumerate(rows):
        cue(tk, 'pop', g=.5); cue(tk, 'plim', g=.5, f=(660, 784, 988, 1175)[i % 4])
        if i and boxes[i]: cue(ts, 'swoosh', g=.38, dur=.4, seed=70 + i, fc=700)
    if has_tx: cue(tx, 'swoosh', g=.4, dur=.6, seed=75, fc=560)
    def fn(t, t0, t1, pal):
        P = PALS[pal]; img = scene_bg(pal, t, t0); n = len(rows); ch = 84 + n * 172; pw = 640 if n <= 3 else 540; ph_ = PGH(pid, pw)
        px, py = 540, 110 + ph_ / 2; cyc = 110 + ph_ + 70 + ch / 2; sc0 = pw / 1024
        g = E('expo_inout', prog(t, tx + .05, tx + .8)); pe = prog(t, t0 + .04, t0 + .8)
        if pe > 0:
            if g > 0: place(img, page(pid, 860), px, lerp(py, 880, g), lerp(pw / 860, 1.0, g), 1.0)
            else: place(img, page(pid, pw), px, py - 300 * (1 - E('expo_out', pe)), .92 + .08 * E('expo_out', pe), clamp(pe * 3.5), blur=18 * (1 - E('easy_in', pe)))
        go = E('expo_in', prog(t, tx, tx + .45))
        if go < 1: R.card_in(img, checklist(t, pal, rows), 540, cyc + 900 * go, t, t0 + .16, rise=320, dur=.8)
        lx, ly = px - pw / 2, py - ph_ / 2
        for i, (lab, ts, tk) in enumerate(rows):
            if not boxes[i]: continue
            x0, y0, x1, y1 = boxes[i]; a_in = prog(t, ts, ts + .55); nxt = rows[i + 1][1] if i + 1 < n else (tx - .15 if has_tx else t1 + 1); a_out = prog(t, nxt - .05, nxt + .25)
            if a_in <= 0 or a_out >= 1: continue
            if i == 0: ring_box(img, boxes[i], lx, ly, sc0, P['a'], clamp(a_in * 3) * (1 - a_out), .05 * (1 - E('expo_out', a_in)) + .015 * math.sin(t * 7)); continue
            e = E('expo_out', a_in); bw, bh = x1 - x0, y1 - y0; th_ = min(760, int(ph_ - 60)); tw_ = int(th_ * bw / bh)
            if tw_ > 760: tw_ = 760; th_ = int(tw_ * bh / bw)
            w_ = lerp(bw * sc0, tw_, e); h_ = lerp(bh * sc0, th_, e); cxs = lerp(lx + (x0 + x1) / 2 * sc0, 540, e); cys = lerp(ly + (y0 + y1) / 2 * sc0, py, e)
            crop = page_raw(pid).crop((x0, y0, x1, y1)).resize((max(8, int(w_)), max(8, int(h_))), Image.LANCZOS)
            img.alpha_composite(Image.new('RGBA', (W, int(110 + ph_ + 40)), mix(P['base'], WHITE, .2) + (int(90 * e * (1 - a_out)),)))
            place(img, shadow_card(crop, int(26 * w_ / tw_) + 6, pad=50, a=110, dy=18, blur=20), cxs, cys, 1 + .04 * math.sin(math.pi * clamp(a_in * 1.4)), clamp(a_in * 5) * (1 - a_out))
        _chips(img, c, t, y=1690); return _cam(img, t, t0, t1)
    return fn

def cena_pilha(c, t0):
    """uma folha por vez caindo na pilha (t_inicio, passo), com a semana enchendo de checks ('semana': false desliga);
    em t_crescer a folha de cima (a ultima de 'paginas') sai da pilha e cresce; 'titulo' e a pilula do alto."""
    ids = c['paginas']; td0 = T(c['t_inicio']); step = c.get('passo', .2); has_tx = c.get('t_crescer') is not None; tx = T(c['t_crescer']) if has_tx else 1e9
    week = c.get('semana', True); tt_ = T(c['t_titulo']) if c.get('titulo') else None; rots = [-5, 4, -2.5, 5.5, -4, 2.5, -1.5, 3.5]; capa = OF.get('capa')
    cue(t0 + .2, 'swoosh', g=.4, dur=.5, seed=71, fc=620); _cue_chips(c)
    if tt_: cue(tt_, 'pop', g=.55)
    for i in range(len(ids)): cue(td0 + i * step, 'plim', g=.45, f=(523, 587, 659, 698, 784, 880, 988, 1047)[i % 8])
    if has_tx: cue(tx, 'swoosh', g=.4, dur=.7, seed=77, fc=560)
    def fn(t, t0, t1, pal):
        img = scene_bg(pal, t, t0); cx, cy = 540, 790 if week else 900
        g = E('expo_inout', prog(t, tx + .05, tx + .9)); fo = 1 - prog(t, tx, tx + .4); br = 1 + .012 * math.sin(2 * math.pi * t * .25); p0 = prog(t, t0 + .1, t0 + .7)
        if capa and p0 > 0 and fo > 0: place(img, page(capa, 560), cx, cy + 320 * (1 - E('expo_out', p0)), .9 + .1 * E('expo_out', p0), clamp(p0 * 3) * fo, rot=3 * E('expo_out', p0))
        for i, pid in enumerate(ids):
            td = td0 + i * step - .12; p = prog(t, td, td + .5); top = i == len(ids) - 1; rot = rots[i % 8]
            if p <= 0 or (not top and fo <= 0): continue
            e = E('expo_out', p)
            if top and g > 0: place(img, page(pid, 840), cx, lerp(cy - 3 * i, 880, g), lerp(560 / 840, 1.0, g), 1.0, rot=rot * (1 - g))
            else: place(img, page(pid, 560), cx + 760 * (1 - e), cy + 240 * (1 - e) - 3 * i, (1.12 - .12 * e) * br, clamp(p * 4) * (1.0 if top else fo), blur=14 * (1 - e), rot=rot + 22 * (1 - e))
        go = E('expo_in', prog(t, tx, tx + .45))
        if week and go < 1: R.card_in(img, week_card(t, pal, td0, step * len(ids) / 7), 540, 1500 + 760 * go, t, t0 + .3, rise=300, dur=.8)
        if tt_: chip_at(img, c['titulo'], 240, t, tt_, size=70, a=fo)
        _chips(img, c, t); return _cam(img, t, t0, t1)
    return fn

def cena_mockup(c, t0):
    """o produto inteiro (mockup) em fundo escuro, com pilula."""
    cue(t0 + .2, 'pop', g=.7); _cue_chips(c)
    def fn(t, t0, t1, pal):
        img = scene_bg('dark', t, t0); cx, cy = 540, 760; pa = prog(t, t0 + .12, t0 + .9); beat = 1 + .015 * math.sin((t - t0) * 2 * math.pi * 1.1) ** 2
        glow_disc(img, cx, cy, 460, DARK['acento'], .22 * E('expo_out', pa) * (1 + .12 * math.sin(t * 4)))
        if pa > 0: place(img, mockup(1000), cx, cy + 9 * math.sin(2 * math.pi * t * .22) + 260 * (1 - E('expo_out', pa)), (.82 + .18 * E('back_out', pa)) * beat * lerp(1, 1.04, prog(t, t0, t1)), clamp(pa * 3), blur=16 * (1 - E('easy_in', pa)))
        _chips(img, c, t, y=1480, size=66); return _cam(img, t, t0, t1)
    return fn

def cena_cta(c, t0):
    """fechamento SEM avatar: mockup + texto (padrao 'Link aqui embaixo') + setas para baixo."""
    tt_ = T(c['t_texto']); ts = T(c['t_setas']) if c.get('t_setas') is not None else tt_ + .6; txt = c.get('texto', 'Link aqui embaixo')
    cue(t0 + .2, 'pop', g=.7); cue(tt_, 'swoosh', g=.4, dur=.5, seed=81); cue(tt_ + .3, 'plim', g=.5, f=660)
    for j in range(3): cue(ts + j * .1, 'pop', g=.4)
    def fn(t, t0, t1, pal):
        img = scene_bg('dark', t, t0); cx, cy = 540, 640; pa = prog(t, t0 + .15, t0 + .9); beat = 1 + .018 * math.sin((t - t0) * 2 * math.pi * 1.2) ** 2
        glow_disc(img, cx, cy, 420, DARK['acento'], .22 * E('expo_out', pa) * (1 + .12 * math.sin(t * 4)))
        if pa > 0: place(img, mockup(900), cx, cy + 9 * math.sin(2 * math.pi * t * .22) + 260 * (1 - E('expo_out', pa)), (.82 + .18 * E('back_out', pa)) * beat, clamp(pa * 3), blur=16 * (1 - E('easy_in', pa)))
        size = 104
        while size > 60 and tw(txt, 'Outfit-Bold', size) > 960: size -= 4
        slide_text(img, txt, 'Outfit-Bold', size, DARK['texto'], 540, 1245, t, tt_, .6, hl=DARK['pill'], hlt=.3)
        arrows(img, t, ts, y0=1420, col=DARK['acento'], shadow=False); return _cam(img, t, t0, t1, 1.05)
    return fn

def cena_frase(c, t0):
    """gancho SEM avatar: parede de paginas atras (material ja em cena) e a frase em cartoes grandes, linha a linha ('linhas': [{texto, t}])."""
    ids = c.get('paginas') or ALLP(); cols = [[ids[(ci * 5 + k * 3 + ci) % len(ids)] for k in range(6)] for ci in range(3)]
    lines = [(l['texto'], T(l['t'])) for l in c['linhas']]; cue(max(0, t0 + .05), 'swoosh', g=.45, dur=.8, seed=11, fc=520)
    for _, tl in lines: cue(tl, 'pop', g=.7)
    def fn(t, t0, t1, pal):
        img = scene_bg(pal, t, t0 - .8); LW, LH = 1500, 2600; L = Image.new('RGBA', (LW, LH), (0, 0, 0, 0)); pw = 340; step = int(PGH(cols[0][0], pw)) + 50
        for ci, col in enumerate(cols):
            dr = -1 if ci % 2 == 0 else 1; off = dr * 62 * (t - t0 + 3) + ci * 190; x = LW // 2 + (ci - 1) * 395
            for k, pid in enumerate(col):
                y = ((k * step + off) % (6 * step)) - step + 100
                if -400 < y < LH + 400: sp = page(pid, pw); paste(L, sp, (x - sp.width / 2, y - sp.height / 2), 1.0)
        place(img, L, 540, 960, 1.0, 1.0, rot=7)
        img.alpha_composite(Image.new('RGBA', (W, H), mix(PALS[pal]['base'], WHITE, .2) + (96,)))
        n = len(lines); y0 = 960 - (n - 1) * 150
        for i, (txt, tl) in enumerate(lines):
            p = prog(t, tl - .25, tl + .3)
            if p <= 0: continue
            size = 84
            while size > 44 and tw(txt, 'Outfit-Bold', size) > 880: size -= 4
            sp = chip_spr(txt, size, font=TX.get('fonte', 'Outfit-Bold'))
            place(img, sp, 540, y0 + i * 300 + 60 * (1 - E('expo_out', p)), .8 + .2 * E('back_out', p), clamp(p * 4), blur=10 * (1 - E('easy_in', p)), rot=(-2, 1.5, -1)[i % 3])
        return _cam(img, t, t0, t1)
    return fn

TW_, TH_ = 930, 1590
def cena_take(c, t0):
    """take de video do entregavel quase em tela cheia (takes/<take>.npy); opcionais: selo {texto, t}, titulo/t_titulo, semana {t_inicio, passo}, pilulas."""
    name = c['take']; speed = c.get('velocidade', 1.0); selo = c.get('selo'); sem = c.get('semana')
    cue(t0 + .05, 'swoosh', g=.4, dur=.5, seed=15, fc=620); _cue_chips(c)
    if selo: cue(T(selo['t']), 'pop', g=.8); cue(T(selo['t']), 'plim', g=.55, f=988)
    if c.get('titulo'): cue(T(c['t_titulo']), 'pop', g=.55)
    if sem:
        for i in range(7): cue(T(sem['t_inicio']) + i * sem.get('passo', .13), 'plim', g=.45, f=(523, 587, 659, 698, 784, 880, 988)[i])
    def fn(t, t0, t1, pal):
        img = scene_bg(pal, t, t0); R.card_in(img, take_card(name, t, t0, speed, TW_, TH_, zdur=t1 - t0, cyf=c.get('foco_y', .5)), 540, 960, t, t0 + .04, rise=380, dur=.8)
        if selo:
            tb = T(selo['t']); pb = prog(t, tb, tb + .7)
            if pb > 0:
                place(img, disc(220, pal, str(selo['texto']), .5 if len(str(selo['texto'])) <= 2 else .36), 905, 250, max(.05, E('back_out_x', pb)), clamp(pb * 4), rot=-12 * (1 - E('expo_out', pb)))
                pixel_ring(img, 905, 250, prog(t, tb + .04, tb + .7), r0=110, r1=300, cell=13, color=PALS[pal]['a'], seed=7, count=140)
        if c.get('titulo'): chip_at(img, c['titulo'], 300, t, T(c['t_titulo']), size=70)
        if sem: R.card_in(img, week_card(t, pal, T(sem['t_inicio']), sem.get('passo', .13)), 540, 1560, t, t0 + .3, rise=300, dur=.8)
        _chips(img, c, t, y=1650 if not sem else 1330); return _cam(img, t, t0, t1)
    return fn

def cena_take_lista(c, t0):
    """take de video em cima + checklist embaixo ('itens': [{rotulo, t_inicio, t_check}])."""
    name = c['take']; rows = [(i['rotulo'], T(i['t_inicio']), T(i['t_check'])) for i in c['itens']]
    cue(t0 + .05, 'swoosh', g=.4, dur=.5, seed=16, fc=620); _cue_chips(c)
    for i, (lab, ts, tk) in enumerate(rows): cue(tk, 'pop', g=.5); cue(tk, 'plim', g=.5, f=(660, 784, 988, 1175)[i % 4])
    def fn(t, t0, t1, pal):
        img = scene_bg(pal, t, t0); n = len(rows); ch = 84 + n * 172; th_ = 1920 - 70 - ch - 200
        R.card_in(img, take_card(name, t, t0, c.get('velocidade', 1.0), 940, th_, zdur=t1 - t0, cyf=c.get('foco_y', .42)), 540, 70 + th_ / 2, t, t0 + .04, rise=-300, dur=.8)
        R.card_in(img, checklist(t, pal, rows), 540, 70 + th_ + 80 + ch / 2, t, t0 + .16, rise=320, dur=.8)
        _chips(img, c, t, y=int(70 + th_ - 80)); return _cam(img, t, t0, t1)      # pilula sobre o pe do take, nao sobre o checklist
    return fn

CENAS = dict(parede=cena_parede, carrossel=cena_carrossel, destaque=cena_destaque, capa=cena_capa, lista=cena_lista, pilha=cena_pilha, mockup=cena_mockup,
             cta=cena_cta, frase=cena_frase, take=cena_take, take_lista=cena_take_lista)

# ================================================================== montagem
PRE, ENT, EXT, REVEAL, XD = .30, .42, .40, .36, .50
CEN = [(540, 900), (700, 1000), (380, 1050), (560, 780)]; CIN = (520, 880)

def _build_seq():
    seq = []; cenas = sorted(ROT['cenas'], key=lambda c: c['inicio'])
    for r in REG:
        if r['tipo'] == 'avatar': seq.append((r['nome'], r['v0'], None, None, r)); continue
        mine = [c for c in cenas if r['c0'] - 1e-6 <= c['inicio'] < r['c1'] - 1e-6]
        if not mine: raise SystemExit("roteiro.json: nenhuma cena comeca no trecho de voz '%s' (%.2f-%.2f s do audio)" % (r['nome'], r['c0'], r['c1']))
        for i, c in enumerate(mine):
            if c['tipo'] not in CENAS: raise SystemExit("roteiro.json: tipo de cena desconhecido: %s (existem: %s)" % (c['tipo'], ', '.join(CENAS)))
            t0 = r['v0'] if i == 0 else T(c['inicio']); pal = c.get('fundo') or ('dark' if c['tipo'] in ('mockup', 'cta') else 'ab'[len(seq) % 2])
            seq.append((c['tipo'], t0, CENAS[c['tipo']](c, t0), pal, r))
    for k in range(1, len(seq)):                                  # som das transicoes de mancha
        pf = seq[k - 1][2] is None; f = seq[k][2] is None; t0 = seq[k][1]
        if pf and not f: cue(t0 - PRE, 'swoosh', g=.55, dur=.6, seed=k * 7); cue(t0, 'sub_hit', g=.3)
        elif f and not pf: cue(t0 - EXT, 'swoosh', g=.6, dur=.55, seed=k * 7 + 1); cue(t0, 'sub_hit', g=.3); cue(t0, 'swoosh', g=.4, dur=.5, seed=k * 7 + 2, fc=700)
        elif not f: cue(t0 - XD / 2, 'swoosh', g=.5, dur=.55, seed=k * 7 + 3); cue(t0, 'sub_hit', g=.22)
    return seq
SEQ = _build_seq()
SETAS = ROT.get('setas_no_cta', True)
for _s in SEQ:
    if _s[2] is None and _s[0] == 'cta' and SETAS:
        for _j in range(3): cue(_s[1] + _s[4].get('lead', .4) + .25 + _j * .1, 'pop', g=.4)

# ------------------------------------------------------------------ gancho sobre o material (padrao; roteiro: "gancho_sobre_material": false desliga)
# o avatar do gancho aparece recortado, sem o fundo dele, por cima de um "print" PARADO da 1a tela do corpo (o quadro em que
# ela ja esta montada). O corpo e o mesmo de sempre: quando o avatar termina de falar, ele desce e sai e essa imagem parada comeca
# a se mexer dali, sem mancha de transicao. Precisa de gancho_alpha.npy (recortar_avatar.py).
_GSM = ROT.get('gancho_sobre_material', True); _ALPHA_F = os.path.join(PROJ, 'gancho_alpha.npy'); _ALPHA = None; SAIDA_AV = .45
QUADRO = float(_GSM.get('quadro', 1.0)) if isinstance(_GSM, dict) else 1.0   # o print e a 1a tela 'QUADRO' segundos depois de entrar
SOBRE = bool(_GSM) and len(SEQ) > 1 and SEQ[0][2] is None and SEQ[1][2] is not None
if SOBRE and not os.path.exists(_ALPHA_F): raise SystemExit('falta gancho_alpha.npy (o recorte do avatar): rode montar_base.py de novo ou recortar_avatar.py; para o gancho antigo, com o fundo do quarto, ponha "gancho_sobre_material": false no roteiro.json')

def _recorte(foot, i):
    global _ALPHA
    if _ALPHA is None: _ALPHA = np.load(_ALPHA_F, mmap_mode='r')
    a = Image.fromarray(np.asarray(_ALPHA[min(i, len(_ALPHA) - 1)])).resize((W, H), Image.BILINEAR).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.1))
    im = Image.fromarray(foot).convert('RGBA'); im.putalpha(a); return im

@functools.lru_cache(2)
def _ultimo_gancho(): i = int(round(SEQ[1][1] * FPS)) - 3; return _recorte(_frame_at(i), i)   # 3 quadros antes do fim: no ultimo a busca do ffmpeg pode cair no preto do corpo

@functools.lru_cache(2)
def _print_corpo(): return _scr(1, SEQ[1][1])                    # a 1a tela do corpo no instante em que o corpo comeca (ja montada)

@functools.lru_cache(1)
def _enquadre():
    """(escala, descer) do avatar recortado. Avatar enquadrado normal (cabeca no alto): tamanho original, 170 px mais baixo, para as
    laterais continuarem coladas nas bordas. Avatar gerado pequeno ou baixo no quadro: amplia (ate 1,4x) ate a cabeca chegar perto
    de 20% da altura, senao ele some no pe da tela. 'escala' e 'descer' no roteiro mandam, se existirem."""
    g = _GSM if isinstance(_GSM, dict) else {}
    al = np.load(_ALPHA_F, mmap_mode='r'); tops = []
    for k in range(0, len(al), max(1, len(al) // 12)):
        rows = np.where((np.asarray(al[k]) > 128).mean(1) > .04)[0]
        if len(rows): tops.append(rows[0] / al.shape[1] * H)
    top = float(np.median(tops)) if tops else 0.0; s = min(1.4, max(1.0, .8 * H / max(1.0, H - top))); dy = 170 if s < 1.05 else 0
    return float(g.get('escala', 1.0 if s < 1.05 else s)), int(g.get('descer', dy))

def _sobre(foot, i, t):
    b = SEQ[1][1]; img = _print_corpo().copy() if t < b else _scr(1, t); s, dy = _enquadre()
    av = _recorte(foot, i) if t < b else _ultimo_gancho(); q = 0.0 if t < b else E('expo_in', clamp((t - b) / SAIDA_AV))
    w, h = int(W * s), int(H * s); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); L.paste(av.resize((w, h), Image.LANCZOS), ((W - w) // 2, H - h + dy + int(h * .8 * q)))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * .55)))
    img.alpha_composite(sh); img.alpha_composite(L); return img

def _scr(k, t):
    name, t0, fn, pal, r = SEQ[k]; t1 = SEQ[k + 1][1] if k + 1 < len(SEQ) else DUR
    if SOBRE and k == 1: t0 -= QUADRO                              # a 1a tela ja entra montada: continua do print que estava atras do avatar
    return fn(t, t0, t1, pal).convert('RGBA')

def face(foot, t, k):
    img = Image.fromarray(foot).convert('RGBA'); name, t0, fn, pal, r = SEQ[k]
    if name == 'cta' and SETAS and t >= t0 + r.get('lead', .4): arrows(img, t, t0 + r.get('lead', .4) + .25)
    return img

def seg_at(t):
    k = 0
    while k + 1 < len(SEQ) and t >= SEQ[k + 1][1] - 1e-9: k += 1
    return k

def _bpal(k, kn):
    """cor da mancha entre a tela k e a kn: a da tela que entra (ou a de quem sai, se entra o avatar)."""
    return SEQ[kn][3] or SEQ[k][3] or 'a'

def render(i, foot=None):
    t = i / FPS; k = seg_at(t); cur = SEQ[k]; isf = cur[2] is None; c1 = CEN[k % 4]; c2 = CEN[(k + 1) % 4]
    if SOBRE and (k == 0 or (k == 1 and t - cur[1] < SAIDA_AV)): return _sobre(foot, i, t)
    if k + 1 < len(SEQ):
        nx = SEQ[k + 1]; b = nx[1]; nf = nx[2] is None
        if not isf and not nf and b - t < XD / 2: return blob(_scr(k, t), _scr(k + 1, t), (t - (b - XD / 2)) / XD, c1, c2, k + 3, nx[3])
        if isf and not nf and b - t <= PRE: return blob(face(foot, t, k), None, .5 * clamp((t - (b - PRE)) / PRE), CIN, c2, k + 3, nx[3])
        if not isf and nf and b - t <= EXT: return blob(_scr(k, t), None, .5 * clamp((t - (b - EXT)) / EXT), c1, CIN, k + 3, cur[3])
    if k > 0:
        pv = SEQ[k - 1]; b = cur[1]; pf = pv[2] is None
        if not isf and not pf and t - b < XD / 2: return blob(_scr(k - 1, t), _scr(k, t), (t - (b - XD / 2)) / XD, CEN[(k - 1) % 4], c1, k + 2, cur[3])
        if not isf and pf and t - b < ENT: return blob(None, _scr(k, t), .5 + .5 * clamp((t - b) / ENT), CIN, c1, k + 2, cur[3])
        if isf and not pf and t - b < REVEAL: return blob(None, face(foot, t, k), .5 + .5 * clamp((t - b) / REVEAL), CEN[(k - 1) % 4], CIN, k + 2, pv[3])
    return face(foot, t, k) if isf else _scr(k, t)

def render_frame(i, foot=None): return np.array(render(i, foot).convert('RGB'))

def _frame_at(i):
    buf = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{i / FPS:.4f}', '-i', SRC, '-frames:v', '1', '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(buf, np.uint8).reshape(H, W, 3)

def stills(times, out, cols=6):
    tiles = []
    for t in times:
        i = min(NF - 1, int(round(t * FPS))); foot = _frame_at(i) if SEQ[seg_at(i / FPS)][2] is None else None
        tiles.append(Image.fromarray(render_frame(i, foot)).resize((324, 576), Image.LANCZOS))
    rows = (len(tiles) + cols - 1) // cols; sheet = Image.new('RGB', (cols * 324, rows * 576), (40, 40, 40))
    for k, im in enumerate(tiles): sheet.paste(im, ((k % cols) * 324, (k // cols) * 576))
    sheet.save(out, quality=88)

def auto_times():
    """3 quadros por tela (comeco, meio, perto do fim) + as transicoes."""
    ts = []
    for k, s in enumerate(SEQ):
        t0 = s[1]; t1 = SEQ[k + 1][1] if k + 1 < len(SEQ) else DUR
        ts += [t0 + .15, t0 + min(.9, (t1 - t0) * .3), (t0 + t1) / 2, t1 - .75, t1 - .2]
    return [round(min(DUR - .05, max(0, t)), 2) for t in ts]

def render_range(a, b, out):
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{a / FPS:.5f}', '-i', SRC, '-vf', f'fps={FPS},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', f'{FPS}', '-i', '-',
                            '-c:v', 'libx264', '-threads', '4', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    n = W * H * 3; foot = np.zeros((H, W, 3), np.uint8)
    for i in range(a, b):
        buf = dec.stdout.read(n)
        if len(buf) == n: foot = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        enc.stdin.write(render_frame(i, foot).tobytes())
    enc.stdin.close(); enc.wait(); dec.kill()

def render_all(procs=6):
    """efeitos sonoros + render em partes paralelas + uniao + mixagem + folha de contato. No maximo ~6 processos: mais que isso estoura a memoria."""
    import time, sfx_coral as S
    t_ini = time.time(); pd = os.path.join(PROJ, 'parts'); os.makedirs(pd, exist_ok=True)
    for f in glob.glob(os.path.join(pd, '*')): os.remove(f)
    vol = float(CFG.get('volume_efeitos', .30)); sfx = os.path.join(PROJ, 'sfx.wav'); S.build(sorted(CUES, key=lambda c: c['t']), DUR, sfx)
    step = (NF + procs - 1) // procs; jobs = []
    for j, a in enumerate(range(0, NF, step)):
        log = open(os.path.join(pd, f'log{j}.txt'), 'w')
        jobs.append((subprocess.Popen([sys.executable, os.path.abspath(__file__), PROJ, 'part', str(a), str(min(NF, a + step)), os.path.join(pd, f'p{j}.mp4')], stdout=log, stderr=log), log))
    bad = [j for j, (p, log) in enumerate(jobs) if (p.wait(), log.close(), p.returncode)[2] != 0]
    if bad: raise SystemExit('render falhou nas partes %s: veja parts/logN.txt' % bad)
    parts = sorted(glob.glob(os.path.join(pd, 'p*.mp4')), key=lambda p: int(os.path.basename(p)[1:-4]))
    lst = os.path.join(pd, 'l.txt'); open(lst, 'w', encoding='utf-8').write(''.join("file '%s'\n" % os.path.basename(p) for p in parts))   # nomes relativos: caminhos com acento quebram o ffmpeg
    video = os.path.join(pd, 'video.mp4'); subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', video], check=True)
    out = os.path.join(PROJ, CFG.get('saida', 'final.mp4'))
    fc = f"[2:a]volume={vol}[s];[1:a][s]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-i', SRC, '-i', sfx, '-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    nfr = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip()
    cols = 12; rows = int(math.ceil(DUR / cols)); sheet = os.path.join(PROJ, 'folha_final.jpg')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-vf', f'fps=1,scale=180:320,tile={cols}x{rows}', '-frames:v', '1', sheet])
    vd = subprocess.run(['ffmpeg', '-i', out, '-af', 'volumedetect', '-vn', '-f', 'null', '-'], capture_output=True, text=True).stderr
    print('final:', out); print('quadros %s (esperado %d) | %.1f s | %s' % (nfr, NF, DUR, ' '.join(l.split('] ')[-1] for l in vd.splitlines() if 'mean_volume' in l or 'max_volume' in l)))
    print('folha de contato (1 quadro por segundo):', sheet); print('tempo de render: %.0f s' % (time.time() - t_ini))

def print_segs():
    print('video %.2f s, %d quadros, aceleracao %.3fx' % (DUR, NF, K))
    av = sum((SEQ[k + 1][1] if k + 1 < len(SEQ) else DUR) - s[1] for k, s in enumerate(SEQ) if s[2] is None)
    for k, s in enumerate(SEQ):
        t1 = SEQ[k + 1][1] if k + 1 < len(SEQ) else DUR
        print('  %-11s %6.2f -> %6.2f  (%.1f s)  %s' % (s[0] if s[2] else 'AVATAR ' + s[0], s[1], t1, t1 - s[1], s[3] or ''))
    print('avatar na tela: %.1f s | material/telas: %.1f s' % (av, DUR - av))
    short = [s[0] for k, s in enumerate(SEQ) if s[2] and (SEQ[k + 1][1] if k + 1 < len(SEQ) else DUR) - s[1] < 3.0]
    if short: print('ATENCAO: telas com menos de 3 s (pouco tempo para ver o material):', short)

if __name__ == '__main__':
    m = sys.argv[2] if len(sys.argv) > 2 else 'segs'
    if m == 'segs': print_segs()
    elif m == 'folha': stills(auto_times(), sys.argv[3] if len(sys.argv) > 3 else os.path.join(PROJ, 'folha.jpg'), cols=5); print('ok')
    elif m == 'stills': stills([float(x) for x in sys.argv[4].split(',')], sys.argv[3])
    elif m == 'part': render_range(int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    elif m == 'render': render_all(int(sys.argv[3]) if len(sys.argv) > 3 else 6)
    else: raise SystemExit(__doc__)
