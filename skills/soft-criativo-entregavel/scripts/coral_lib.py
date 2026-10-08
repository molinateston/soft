"""
Edicion estilo referencia (Claude coral/crema): facecam + subtitulos tiza + chips + pantallas de UI + transicion blob.
    python3 coral_lib.py stills hoja.jpg t1,t2,...
    python3 coral_lib.py part A B parts/pNNN.mp4
    python3 coral_lib.py mux parts/ salida.mp4
"""
import os, sys, math, json, subprocess, glob, random, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))          # .../scripts
ROOT = os.path.dirname(HERE)                                # raiz de la skill
sys.path.insert(0, HERE)
import engine
from engine import W, H, paste, place, footage, draw_cursor, rounded_tile, logo_tile
from motion import EASE, get_ease, Track, prog, clamp, lerp, camera, spring

SRC = os.environ.get('CRUDO', 'crudo.mp4')
FPS = 24000 / 1001
NF = 768

CORAL = (240, 69, 47); CORAL_L = (255, 120, 92); CORAL_D = (206, 44, 26); CORAL_K = (255, 96, 70)
CREAM = (244, 239, 230); INK = (24, 22, 22); GREY = (146, 140, 134); LINE = (232, 226, 218)
WHITE = (255, 255, 255); TINT = (253, 228, 221); ROW = (249, 245, 239)

def E(name, p): return EASE[name](p)

# ------------------------------------------------------------------ fuentes y texto
@functools.lru_cache(None)
def F(name, size): return ImageFont.truetype(os.path.join(ROOT, 'assets', 'fonts', name + '.ttf'), size)

@functools.lru_cache(None)
def tsp(txt, fname, size, color, pad=26):
    f = F(fname, size)
    w = int(f.getlength(txt)) + pad * 2; h = int(size * 1.5) + pad * 2
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad, pad), txt, font=f, fill=color + (255,))
    return im

def tw(txt, fname, size): return F(fname, size).getlength(txt)

def draw_txt(img, xy, txt, fname, size, color, anchor='la'):
    ImageDraw.Draw(img).text(xy, txt, font=F(fname, size), fill=color + (255,), anchor=anchor)

def rrect(img, box, r, fill, outline=None, ow=2, ss=3):
    """rectangulo redondeado suavizado (supersampling local)."""
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = x1 - x0, y1 - y0
    if w < 2 or h < 2: return
    L = Image.new('RGBA', (w * ss, h * ss), (0, 0, 0, 0))
    ImageDraw.Draw(L).rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), min(r, h // 2) * ss, fill=fill + (255,) if len(fill) == 3 else fill,
                                        outline=(outline + (255,)) if outline else None, width=ow * ss)
    L = L.resize((w, h), Image.LANCZOS)
    img.alpha_composite(L, (x0, y0)) if x0 >= 0 and y0 >= 0 and x0 + w <= img.width and y0 + h <= img.height else paste(img, L, (x0, y0))

def circle(img, cx, cy, r, fill, ss=3):
    L = Image.new('RGBA', (int(r * 2 * ss), int(r * 2 * ss)), (0, 0, 0, 0))
    ImageDraw.Draw(L).ellipse((0, 0, L.width - 1, L.height - 1), fill=fill + (255,) if len(fill) == 3 else fill)
    L = L.resize((int(r * 2), int(r * 2)), Image.LANCZOS)
    paste(img, L, (cx - r, cy - r))

_lt = functools.lru_cache(None)(lambda kind, size: logo_tile(kind, size))

# ------------------------------------------------------------------ fondo crema
@functools.lru_cache(None)
def cream_bg(variant):
    h, w = 480, 270
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u, v = xx / w, yy / h
    base = np.zeros((h, w, 3), np.float32) + np.array(CREAM, np.float32)
    layouts = {
        0: [(.95, .90, .20, CORAL, .38), (.04, .97, .16, CORAL, .24), (.5, .0, .35, (255, 252, 246), .5)],
        1: [(.06, .86, .22, CORAL, .34), (.97, .30, .15, CORAL, .20), (.5, .0, .35, (255, 252, 246), .5)],
        2: [(.92, .78, .24, CORAL, .36), (.08, .30, .16, CORAL, .16), (.5, .0, .35, (255, 252, 246), .5)],
    }[variant % 3]
    for cx, cy, r, col, a in layouts:
        d = np.sqrt(((u - cx) * .5625) ** 2 + (v - cy) ** 2)
        g = (np.exp(-(d / r) ** 2) * a)[..., None]
        base = base * (1 - g) + np.array(col, np.float32) * g
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), 'RGB').resize((W, H), Image.BICUBIC)
    return im.convert('RGBA')

# ------------------------------------------------------------------ props 3D (pildora, check, destello)
def _shaded(mask, top, bot, hl):
    w, h = mask.size
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    col = np.array(top, np.float32) * (1 - t) + np.array(bot, np.float32) * t
    col = np.repeat(col, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    g = np.exp(-(((xx - hl[0] * w) / (hl[2] * w)) ** 2 + ((yy - hl[1] * h) / (hl[3] * h)) ** 2))
    col = col + (255 - col) * g[..., None] * .5
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    im.putalpha(mask)
    return im

@functools.lru_cache(None)
def prop(kind, size):
    ss = 2
    if kind == 'pill':
        bw, bh = size, int(size * .43)
    else:
        bw = bh = size
    pad = int(size * .18)
    cw, ch = bw + pad * 2, bh + pad * 2
    mask = Image.new('L', (bw * ss, bh * ss), 0)
    md = ImageDraw.Draw(mask)
    if kind == 'pill':
        md.rounded_rectangle((0, 0, bw * ss - 1, bh * ss - 1), bh * ss // 2, fill=255)
    elif kind == 'check':
        md.ellipse((0, 0, bw * ss - 1, bh * ss - 1), fill=255)
    else:  # destello de 4 puntas
        pts = [(0, -1), (.17, -.17), (1, 0), (.17, .17), (0, 1), (-.17, .17), (-1, 0), (-.17, -.17)]
        c = bw * ss / 2
        md.polygon([(c + x * c * .98, c + y * c * .98) for x, y in pts], fill=255)
    obj = _shaded(mask, CORAL_L, CORAL_D, (.34, .24, .55, .45)) if kind != 'spark' else _shaded(mask, CORAL_K, CORAL, (.4, .4, .4, .4))
    if kind == 'check':
        d = ImageDraw.Draw(obj)
        S = bw * ss
        pts = [(S * .27, S * .52), (S * .43, S * .68), (S * .74, S * .34)]
        d.line(pts, fill=(255, 255, 255, 255), width=int(S * .11), joint='curve')
        for p in (pts[0], pts[-1]): d.ellipse((p[0] - S * .055, p[1] - S * .055, p[0] + S * .055, p[1] + S * .055), fill=(255, 255, 255, 255))
    L = Image.new('RGBA', (cw * ss, ch * ss), (0, 0, 0, 0))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0))
    shm = Image.new('RGBA', mask.size, (190, 40, 24, 120)); shm.putalpha(mask.point(lambda v: int(v * .55)))
    sh.alpha_composite(shm, (pad * ss, pad * ss + int(size * .07 * ss)))
    sh = sh.filter(ImageFilter.GaussianBlur(size * .06 * ss))
    L.alpha_composite(sh)
    L.alpha_composite(obj, (pad * ss, pad * ss))
    return L.resize((cw, ch), Image.LANCZOS)

PROPS_FACE = [('pill', 300, 1040, 1585, -30, 5, .0), ('check', 92, 74, 1752, 0, 0, .25), ('spark', 62, 74, 1480, 0, 0, .6)]
PROPS_A = [('pill', 330, 96, 600, -24, 0, .0), ('check', 90, 996, 505, 0, 0, .3), ('pill', 560, 980, 1745, 30, 9, .55),
           ('check', 88, 92, 1712, 0, 0, .1), ('spark', 66, 150, 330, 0, 0, .5), ('spark', 58, 975, 1440, 0, 0, .8)]
PROPS_B = [('pill', 340, 980, 470, 28, 0, .2), ('check', 90, 80, 690, 0, 0, .4), ('pill', 540, 90, 1760, -34, 9, .7),
           ('check', 92, 1000, 1715, 0, 0, .0), ('spark', 64, 960, 330, 0, 0, .6), ('spark', 56, 110, 1480, 0, 0, .2)]

def props(img, t, t0, layout):
    order = sorted(range(len(layout)), key=lambda i: -layout[i][5])
    for i in order:
        kind, size, x, y, rot, blur, ph = layout[i]
        p = prog(t, t0 + .08 + .07 * i, t0 + .8 + .07 * i)
        if p <= 0: continue
        s = E('back_out_x', p)
        dy = 10 * math.sin(2 * math.pi * (t * .42 + ph)); dr = 3.5 * math.sin(2 * math.pi * (t * .31 + ph * 1.3))
        place(img, prop(kind, size), x, y + dy + 60 * (1 - E('expo_out', p)), max(.05, s), clamp(p * 4), blur=blur, rot=rot + dr)

# ------------------------------------------------------------------ texto en pantalla
@functools.lru_cache(None)
def cap_line(parts):
    f = F('Handlee', 94); sp = f.getlength(' ') + 12
    tot = sum(f.getlength(w) for w, _ in parts) + sp * (len(parts) - 1)
    pad = 44; w = int(tot) + pad * 2; h = 150 + pad
    base = Image.new('RGBA', (w, h), (0, 0, 0, 0)); shd = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    x = pad
    for word, key in parts:
        col = CORAL_K if key else (253, 251, 247)
        ImageDraw.Draw(shd).text((x + 3, pad * .5 + 6), word, font=f, fill=(0, 0, 0, 190))
        ImageDraw.Draw(base).text((x, pad * .5), word, font=f, fill=col + (255,), stroke_width=1, stroke_fill=col + (255,))
        x += f.getlength(word) + sp
    shd = shd.filter(ImageFilter.GaussianBlur(7))
    shd.alpha_composite(base)
    return shd

def caption(img, t, ts, te, parts, y=235):
    if t < ts - .02 or t > te + .35: return
    pin = prog(t, ts, ts + .28); pout = prog(t, te, te + .18)
    a = pin * (1 - pout)
    if a <= 0: return
    blur = 14 * (1 - E('easy_in', pin)) + 9 * pout
    place(img, cap_line(parts), 540, y + 18 * (1 - E('expo_out', pin)) - 12 * pout, .95 + .05 * pin, a, blur=blur)

@functools.lru_cache(None)
def asterisk(size):
    lg = Image.open(os.path.join(engine.LG, 'claude_black.png')).convert('RGBA')
    a = np.array(lg); a[..., 0:3] = CORAL
    return Image.fromarray(a, 'RGBA').resize((size, size), Image.LANCZOS)

@functools.lru_cache(None)
def chip_sprite(parts):
    f = F('Jakarta-SemiBold', 42); sp = f.getlength(' ')
    tot = sum(f.getlength(w) for w, _ in parts) + sp * (len(parts) - 1)
    h, padx, ic = 98, 38, 46
    w = int(padx + ic + 20 + tot + padx)
    pad = 50; ss = 2
    L = Image.new('RGBA', ((w + pad * 2) * ss, (h + pad * 2) * ss), (0, 0, 0, 0))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad * ss, (pad + 9) * ss, (pad + w) * ss, (pad + h + 9) * ss), h * ss // 2, fill=(40, 20, 10, 90))
    L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14 * ss)))
    ImageDraw.Draw(L).rounded_rectangle((pad * ss, pad * ss, (pad + w) * ss, (pad + h) * ss), h * ss // 2, fill=(255, 255, 255, 255))
    L = L.resize((w + pad * 2, h + pad * 2), Image.LANCZOS)
    L.alpha_composite(asterisk(ic), (pad + padx, pad + (h - ic) // 2))
    d = ImageDraw.Draw(L); x = pad + padx + ic + 20
    for word, key in parts:
        d.text((x, pad + h / 2), word, font=f, fill=(CORAL if key else INK) + (255,), anchor='lm')
        x += f.getlength(word) + sp
    return L

def chip(img, t, ts, te, parts, y=1335, pulse=False):
    if t < ts or t > te + .3: return
    pin = prog(t, ts, ts + .45); pout = prog(t, te, te + .22)
    s = lerp(.62, 1.0, E('back_out', pin)) * (1 - .08 * pout)
    if pulse and pin >= 1: s *= 1 + .035 * math.sin((t - ts - .45) * 2 * math.pi * 1.8) ** 2
    place(img, chip_sprite(parts), 540, y + 34 * (1 - E('expo_out', pin)) + 14 * pout, s, pin * (1 - pout) * 1.0, blur=10 * (1 - E('easy_in', pin)) + 6 * pout)

# ------------------------------------------------------------------ titulos
def title(img, t, t0, lines, y0, size=128, lh=150):
    for li, line in enumerate(lines):
        sp = tw(' ', 'Outfit-SemiBold', size) * .9
        ws = [tw(w[0], 'Outfit-SemiBold', size) for w in line]
        tot = sum(ws) + sp * (len(line) - 1)
        x = 540 - tot / 2
        for wi, w in enumerate(line):
            ta = t0 + (li * 2 + wi) * .09
            p = prog(t, ta, ta + .55)
            if p > 0:
                e = E('expo_out', p)
                place(img, tsp(w[0], 'Outfit-SemiBold', size, w[1]), x + ws[wi] / 2, y0 + li * lh + 44 * (1 - e), 1.0, clamp(p * 3), blur=18 * (1 - E('easy_in', p)))
            if len(w) > 2 and w[2] == 'u':
                pu = E('expo_out', prog(t, ta + .45, ta + 1.05))
                if pu > 0:
                    uy = y0 + li * lh + size * .62
                    x1 = x + ws[wi] * pu
                    L = Image.new('RGBA', (W, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
                    pts = [(x + k, 30 + 5 * math.sin(k / 38.0)) for k in range(0, int(ws[wi] * pu) + 1, 6)]
                    if len(pts) > 1:
                        d.line(pts, fill=CORAL + (255,), width=11, joint='curve')
                        for p0 in (pts[0], pts[-1]): d.ellipse((p0[0] - 5.5, p0[1] - 5.5, p0[0] + 5.5, p0[1] + 5.5), fill=CORAL + (255,))
                        paste(img, L, (0, uy - 30))
            x += ws[wi] + sp

# ------------------------------------------------------------------ tarjetas
@functools.lru_cache(None)
def card_base(w, h, r=48):
    t, pad = rounded_tile(w, h, r, (255, 255, 255, 255), outline=(240, 234, 226, 255))
    return t, pad

def card_in(img, spr, cx, cy, t, ta, rise=300, dur=.8):
    p = prog(t, ta, ta + dur)
    if p <= 0: return False
    e = E('expo_out', p)
    place(img, spr, cx, cy + rise * (1 - e), .92 + .08 * e, clamp(p * 3.5), blur=20 * (1 - E('easy_in', p)))
    return True

def check_badge(d_img, cx, cy, r, p=1.0):
    if p <= 0: return
    s = E('back_out_x', p)
    sp = prop('check', int(r * 2))
    place(d_img, sp, cx, cy, max(.05, s), clamp(p * 4))

def status_pill(img, x, y, done_p):
    # pendiente (gris) -> listo (coral, pop)
    if done_p < 1:
        a = 1 - clamp(done_p * 4)
        if a > 0:
            L = Image.new('RGBA', (170, 58), (0, 0, 0, 0)); rrect(L, (0, 0, 170, 58), 29, (238, 233, 226))
            draw_txt(L, (85, 29), 'Pendiente', 'Jakarta-SemiBold', 23, GREY, 'mm')
            paste(img, L, (x, y), a)
    if done_p > 0:
        s = E('back_out', done_p)
        L = Image.new('RGBA', (170, 58), (0, 0, 0, 0)); rrect(L, (0, 0, 170, 58), 29, CORAL)
        draw_txt(L, (85, 29), 'Listo', 'Jakarta-Bold', 25, WHITE, 'mm')
        d = ImageDraw.Draw(L)
        d.line([(34, 30), (40, 36), (51, 23)], fill=WHITE + (255,), width=4, joint='curve')
        place(img, L, x + 85, y + 29, .6 + .4 * s, clamp(done_p * 4))

def glyph(img, kind, cx, cy):
    d = ImageDraw.Draw(img)
    if kind == 0:
        d.arc((cx - 14, cy - 12, cx + 16, cy + 18), 190, 285, fill=CORAL + (255,), width=5)
        d.ellipse((cx + 12, cy - 6, cx + 20, cy + 2), fill=CORAL + (255,))
    elif kind == 1:
        draw_txt(img, (cx, cy), 'T', 'Jakarta-ExtraBold', 34, CORAL, 'mm')
    else:
        d.rounded_rectangle((cx - 16, cy - 11, cx + 16, cy + 11), 6, outline=CORAL + (255,), width=4)
        d.line([(cx - 8, cy - 2), (cx + 8, cy - 2)], fill=CORAL + (255,), width=3); d.line([(cx - 8, cy + 5), (cx + 3, cy + 5)], fill=CORAL + (255,), width=3)

def checklist(t, done):
    w, h = 860, 660
    base, pad = card_base(w, h)
    c = base.copy()
    ox, oy = pad, pad
    draw_txt(c, (ox + 44, oy + 44), 'Checklist de edición', 'Jakarta-Bold', 36, INK)
    draw_txt(c, (ox + w - 44, oy + 50), 'este_video.mp4', 'Jakarta-Medium', 26, GREY, 'ra')
    rows = [('Animaciones', 'Movimiento y transiciones'), ('Motion graphics', 'Tarjetas, títulos y UI'), ('Subtítulos', 'Palabra por palabra')]
    n_done = 0
    for i, (a, b) in enumerate(rows):
        y = oy + 118 + i * 132
        rrect(c, (ox + 36, y, ox + w - 36, y + 114), 30, ROW)
        rrect(c, (ox + 56, y + 24, ox + 122, y + 90), 20, TINT)
        glyph(c, i, ox + 89, y + 57)
        draw_txt(c, (ox + 146, y + 24), a, 'Jakarta-Bold', 34, INK)
        draw_txt(c, (ox + 146, y + 66), b, 'Jakarta-Medium', 24, GREY)
        dp = prog(t, done[i], done[i] + .35)
        status_pill(c, ox + w - 36 - 170 - 22, y + 28, dp)
        if dp >= 1: n_done += 1
        elif dp > 0: n_done += dp
        if dp > 0: check_badge(c, ox + w - 36 - 8, y + 6, 20, prog(t, done[i] + .1, done[i] + .6))
    # progreso
    py = oy + 118 + 3 * 132 + 22
    rrect(c, (ox + 44, py, ox + 44 + 600, py + 16), 8, LINE)
    fillw = int(600 * E('easy', clamp(n_done / 3)))
    if fillw > 6: rrect(c, (ox + 44, py, ox + 44 + fillw, py + 16), 8, CORAL)
    draw_txt(c, (ox + w - 44, py + 8), '%d/3' % int(min(3, math.floor(n_done + .02))), 'Jakarta-Bold', 30, INK, 'rm')
    draw_txt(c, (ox + 44, py + 44), 'Sin ediciones manuales', 'Jakarta-Medium', 22, GREY)
    return c

# ------------------------------------------------------------------ cursor / clic
def click_ring(img, cx, cy, p, col=CORAL):
    if p <= 0 or p >= 1: return
    e = E('expo_out', p)
    r = lerp(18, 120, e); wd = max(1, int(lerp(9, 1, p))); a = int(255 * (1 - p) ** 1.3)
    L = Image.new('RGBA', (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((150 - r, 150 - r, 150 + r, 150 + r), outline=col + (a,), width=wd)
    g = L.filter(ImageFilter.GaussianBlur(6))
    paste(img, g, (cx - 150, cy - 150)); paste(img, L, (cx - 150, cy - 150))

def cursor_path(t, ta, tb, p0, p1, pc):
    cp = E('cine', prog(t, ta, tb))
    x = (1 - cp) ** 2 * p0[0] + 2 * (1 - cp) * cp * pc[0] + cp ** 2 * p1[0]
    y = (1 - cp) ** 2 * p0[1] + 2 * (1 - cp) * cp * pc[1] + cp ** 2 * p1[1]
    return x, y

# ------------------------------------------------------------------ blob (transicion)
_YY, _XX = np.mgrid[0:480, 0:270].astype(np.float32)
_XX *= 4; _YY *= 4
_FILL = None

def blob_alpha(cx, cy, R, seed, ph):
    dx = _XX - cx; dy = _YY - cy
    ang = np.arctan2(dy, dx); dist = np.hypot(dx, dy)
    r = R * (1 + .11 * np.sin(3 * ang + ph + seed) + .07 * np.sin(5 * ang - 1.3 * ph + seed * 2) + .04 * np.sin(7 * ang + .7 * ph))
    return np.clip((r - dist) / 12 + .5, 0, 1)

def _up(a): return Image.fromarray((a * 255).astype(np.uint8), 'L').resize((W, H), Image.BICUBIC)

def coral_fill():
    global _FILL
    if _FILL is None:
        t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
        col = np.array((250, 92, 66), np.float32) * (1 - t) + np.array((232, 56, 36), np.float32) * t
        _FILL = Image.fromarray(np.repeat(col, W, axis=1).astype(np.uint8), 'RGB').convert('RGBA')
    return _FILL

def maxdist(cx, cy): return max(math.hypot(cx - x, cy - y) for x in (0, W) for y in (0, H))

def blob_transition(A, B, p, c1, c2, seed):
    ph = p * 7
    fill = coral_fill()
    if p < .5:
        q = p / .5
        R = lerp(20, maxdist(*c1) * 1.32, E('cine', q))
        out = A.copy()
        m = _up(blob_alpha(c1[0], c1[1], R, seed, ph))
        rim = ImageChops.subtract(m, _up(blob_alpha(c1[0], c1[1], R * .93, seed, ph)))
    else:
        q = (p - .5) / .5
        R = lerp(20, maxdist(*c2) * 1.32, E('cine', q))
        out = B.copy()
        h = blob_alpha(c2[0], c2[1], R, seed + 3, ph)
        m = _up(1 - h)
        rim = ImageChops.subtract(_up(blob_alpha(c2[0], c2[1], R * 1.07, seed + 3, ph)), _up(h))
        rim = ImageChops.multiply(rim, m)
    f = fill.copy(); f.putalpha(m); out.alpha_composite(f)
    rl = Image.new('RGBA', (W, H), (255, 160, 135, 255)); rl.putalpha(rim.point(lambda v: int(v * .55))); out.alpha_composite(rl)
    return out

# ------------------------------------------------------------------ facecam
def _build_scr():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    top = np.clip(1 - y / .33, 0, 1) ** 1.6 * .64
    xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :]; yy = np.linspace(-1, 1, H, dtype=np.float32)[:, None]
    vig = np.clip((xx ** 2 * .55 + yy ** 2 * .35) - .25, 0, 1) * .5
    return ((1 - top) * (1 - vig) * .96)[..., None].astype(np.float32)
SCR = _build_scr()

def facecam(t, foot, zoom, caps, chips, ts, dx=0, dy=0):
    img = footage(foot, zoom(t), dx, dy)
    arr = np.asarray(img)[..., :3].astype(np.float32) * SCR
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    props(img, t, ts, PROPS_FACE)
    for c in caps: caption(img, t, *c)
    for c in chips: chip(img, t, *c)
    return img

def s_face0(t, foot):
    z = Track([(0, 1.15, 'expo_out'), (.8, 1.03, 'easy'), (3.5, 1.09)])
    caps = [(.05, 1.15, (('la', 0), ('inteligencia', 0), ('artificial', 1))), (1.15, 1.95, (('acaba', 0), ('de', 0), ('matar', 1))),
            (1.95, 2.45, (('por', 0), ('completo', 0))), (2.45, 3.4, (('a', 0), ('los', 0), ('editores', 1), ('de', 0), ('video', 0)))]
    chips = [(1.6, 3.3, (('IA', 1), ('vs.', 0), ('editores', 0), ('de', 0), ('video', 0)))]
    return facecam(t, foot, z, caps, chips, 0.0)

def s_face2(t, foot):
    z = Track([(8.4, 1.10, 'expo_out'), (9.0, 1.03, 'easy'), (10.3, 1.03, 'cine'), (11.8, 1.14)])
    caps = [(8.42, 9.3, (('y', 0), ('lo', 0), ('mejor', 1), ('de', 0), ('todo', 0))), (9.32, 10.2, (('es', 0), ('que', 0), ('esto', 0), ('lo', 0), ('crea', 1))),
            (10.2, 11.1, (('a', 0), ('partir', 0), ('solamente', 0))), (11.1, 11.85, (('de', 0), ('tres', 1), ('herramientas', 0)))]
    chips = [(10.75, 11.8, (('Solo', 0), ('3', 1), ('herramientas', 0)))]
    return facecam(t, foot, z, caps, chips, 8.4, dx=-20)

def s_face4(t, foot):
    z = Track([(15.85, 1.13, 'expo_out'), (16.6, 1.06, 'easy'), (17.2, 1.09)])
    caps = [(15.9, 17.0, (('que', 0), ('al', 0), ('conectarlas', 1)))]
    chips = [(16.15, 17.1, (('Se', 0), ('conectan', 0), ('las', 0), ('3', 1)))]
    return facecam(t, foot, z, caps, chips, 15.85, dx=20)

def s_face7(t, foot):
    z = Track([(22.9, 1.11, 'expo_out'), (23.5, 1.04, 'easy'), (26.3, 1.11)])
    caps = [(22.9, 23.5, (('y', 0), ('lo', 0), ('mejor', 1), ('de', 0), ('todo', 0))), (23.5, 24.4, (('es', 0), ('que', 0), ('prepararé', 1))),
            (24.4, 24.93, (('una', 0), ('skill', 1))), (24.93, 26.3, (('para', 0), ('poder', 0), ('enviártela', 1)))]
    chips = [(24.0, 26.2, (('Te', 0), ('paso', 0), ('la', 0), ('skill', 1)))]
    return facecam(t, foot, z, caps, chips, 22.9, dx=-15)

def s_face9(t, foot):
    z = Track([(29.55, 1.13, 'expo_out'), (30.3, 1.05, 'easy'), (32.1, 1.10)])
    caps = [(29.65, 30.6, (('para', 0), ('que', 0), ('vos', 0), ('también', 1))), (30.65, 31.2, (('puedas', 0), ('hacer', 0))),
            (31.2, 32.2, (('este', 0), ('estilo', 1), ('de', 0), ('edición', 0)))]
    chips = [(29.95, 32.2, (('Comentá', 0), ('"editor"', 1)))]
    return _face9_build(t, foot, z, caps, chips)

def _face9_build(t, foot, z, caps, chips):
    img = footage(foot, z(t))
    arr = np.asarray(img)[..., :3].astype(np.float32) * SCR
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    props(img, t, 29.55, PROPS_FACE)
    for c in caps: caption(img, t, *c)
    chip(img, t, *chips[0], pulse=True)
    return img

# ------------------------------------------------------------------ pantallas crema
def crema_cam(img, t, zk, cx=540, cy=1000):
    z = zk(t)
    return camera(img, z) if z > 1.0005 else img

def s_edit(t, foot):                                  # 3.4 - 8.4
    t0 = 3.4
    img = cream_bg(0).copy()
    props(img, t, t0 + .1, PROPS_A)
    title(img, t, t0 + .15, [[('Editado', INK), ('100%', CORAL)], [('por', INK), ('IA', CORAL, 'u')]], 330)
    done = [5.25, 6.3, 7.35]
    if t >= t0 + .55:
        card_in(img, checklist(t, done), 540, 1130, t, t0 + .6)
    return crema_cam(img, t, Track([(3.4, 1.0), (4.2, 1.0, 'cine'), (7.6, 1.05, 'easy'), (8.5, 1.05)]), 540, 1080)

def tile_names():
    return [('claude', 'Claude'), ('remotion', 'Remotion'), ('higgs', 'Higgsfield')]

def s_tools(t, foot):                                  # 11.75 - 15.85
    t0 = 11.75
    img = cream_bg(1).copy()
    props(img, t, t0 + .1, PROPS_B)
    title(img, t, t0 + .2, [[('Solo', INK), ('3', CORAL, 'u')], [('herramientas', INK)]], 300)
    xs = [195, 540, 885]; cues = [12.45, 14.15, 15.2]
    for i, (kind, name) in enumerate(tile_names()):
        ta = cues[i]
        p = prog(t, ta, ta + .75)
        if p <= 0: continue
        tile, pd = _lt(kind, 270)
        s = E('back_out_x', p)
        y = Track([(ta, 1200, 'expo_out'), (ta + .75, 1010)])(t)
        place(img, tile, xs[i], y, .25 + .75 * s, clamp(p * 4), blur=Track([(ta, 18, 'expo_out'), (ta + .5, 0)])(t))
        # numero + nombre (follow-through)
        pn = prog(t, ta + .12, ta + .6)
        if pn > 0:
            L = Image.new('RGBA', (110, 110), (0, 0, 0, 0)); circle(L, 55, 55, 42, CORAL)
            draw_txt(L, (55, 57), str(i + 1), 'Outfit-Bold', 46, WHITE, 'mm')
            place(img, L, xs[i], 1235, E('back_out_x', pn), clamp(pn * 4))
        pt = prog(t, ta + .25, ta + .75)
        if pt > 0:
            place(img, tsp(name, 'Outfit-Medium', 46, INK), xs[i], 1330 + 24 * (1 - E('expo_out', pt)), 1.0, clamp(pt * 3), blur=12 * (1 - E('easy_in', pt)))
        pr = prog(t, ta + .03, ta + .6)
        if 0 < pr < 1:
            click_ring(img, xs[i], 1010, pr)
    return crema_cam(img, t, Track([(11.75, 1.0), (12.4, 1.0, 'cine'), (15.8, 1.045)]), 540, 1050)

def stepper(img, t, cx, y, step_idx, labels=('Skill', 'Prompt', 'Listo')):
    wid = [236, 244, 224]; gap = 22
    tot = sum(wid) + gap * 2
    x = cx - tot / 2
    for i, lab in enumerate(labels):
        h = 76
        L = Image.new('RGBA', (wid[i] + 20, h + 20), (0, 0, 0, 0))
        active = step_idx == i; done = step_idx > i
        sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((10, 16, 10 + wid[i], 16 + h), h // 2, fill=(60, 30, 20, 40))
        L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
        rrect(L, (10, 10, 10 + wid[i], 10 + h), h // 2, CORAL if active else WHITE)
        col = WHITE if active else INK
        circle(L, 10 + 40, 10 + h // 2, 22, (255, 255, 255) if active else (CORAL if done else (238, 233, 226)))
        if done:
            ImageDraw.Draw(L).line([(10 + 31, 10 + h // 2), (10 + 38, 10 + h // 2 + 8), (10 + 50, 10 + h // 2 - 8)], fill=WHITE + (255,), width=5, joint='curve')
        else:
            draw_txt(L, (10 + 40, 10 + h // 2 + 1), str(i + 1), 'Jakarta-Bold', 26, CORAL if active else GREY, 'mm')
        draw_txt(L, (10 + 78, 10 + h // 2 + 1), lab, 'Jakarta-Bold', 31, col, 'lm')
        pin = prog(t, 17.15 + i * .1, 17.7 + i * .1)
        place(img, L, x + wid[i] / 2, y - 80 * (1 - E('expo_out', pin)), 1.0, clamp(pin * 3), blur=14 * (1 - E('easy_in', pin)))
        x += wid[i] + gap

def window_card(t):
    w, h = 860, 860
    base, pad = card_base(w, h)
    c = base.copy()
    ox, oy = pad, pad
    c.alpha_composite(asterisk(40), (ox + 40, oy + 36))
    draw_txt(c, (ox + 96, oy + 56), 'Claude', 'Jakarta-Bold', 36, INK, 'lm')
    draw_txt(c, (ox + w - 40, oy + 56), 'Nuevo chat', 'Jakarta-Medium', 25, GREY, 'rm')
    return c, ox, oy, w, h

def s_skill(t, foot):                                  # 17.1 - 22.9
    t0 = 17.1
    img = cream_bg(2).copy()
    props(img, t, t0 + .1, PROPS_A[:4] + [('spark', 64, 160, 300, 0, 0, .5), ('spark', 54, 960, 380, 0, 0, .9)])
    step = 0 if t < 21.6 else (1 if t < 22.5 else 2)
    stepper(img, t, 540, 205, step)
    c, ox, oy, w, h = window_card(t)
    # --- etapa a: tres logos -> archivo skill
    xs = [-215, 0, 215]
    for i, (kind, _) in enumerate(tile_names()):
        ta = 17.35 + i * .13
        p = prog(t, ta, ta + .6)
        conv = E('expo_in', prog(t, 17.95, 18.5))
        if p <= 0 or conv >= 1: continue
        tile, pd = _lt(kind, 150)
        sc = E('back_out_x', p) * (1 - .55 * conv)
        place(c, tile, ox + w // 2 + xs[i] * (1 - conv), oy + 270 + 10 * conv, max(.05, sc), clamp(p * 4) * (1 - clamp(conv * 1.3)))
    # archivo skill
    ps = prog(t, 18.35, 19.0); out_a = E('expo_in', prog(t, 21.55, 21.95))
    if ps > 0 and out_a < 1:
        f = Image.new('RGBA', (700, 230), (0, 0, 0, 0)); rrect(f, (0, 0, 700, 230), 38, ROW)
        rrect(f, (30, 40, 180, 190), 34, CORAL)
        a = np.array(asterisk(86)); a[..., 0:3] = 255
        f.alpha_composite(Image.fromarray(a, 'RGBA'), (62, 72))
        draw_txt(f, (216, 82), 'estilo-edicion.skill', 'Jakarta-Bold', 36, INK)
        draw_txt(f, (216, 134), 'Tu skill de edición', 'Jakarta-Medium', 27, GREY)
        place(c, f, ox + w // 2, oy + 290 + 120 * out_a, E('back_out_x', ps) * (1 - .1 * out_a), clamp(ps * 4) * (1 - out_a), blur=16 * out_a)
        pr = prog(t, 18.4, 19.1)
        if 0 < pr < 1: click_ring(c, ox + w // 2, oy + 290, pr)
    for i, (lab, tg) in enumerate([('Motion graphics', 20.3), ('Animaciones', 21.2)]):
        pt = prog(t, tg, tg + .5)
        if pt <= 0 or out_a >= 1: continue
        wpx = int(tw(lab, 'Jakarta-Bold', 32)) + 64
        L = Image.new('RGBA', (wpx, 76), (0, 0, 0, 0)); rrect(L, (0, 0, wpx, 76), 38, TINT)
        draw_txt(L, (wpx // 2, 39), lab, 'Jakarta-Bold', 32, CORAL, 'mm')
        place(c, L, ox + w // 2 + (-150 if i == 0 else 190), oy + 470 + (0 if i == 0 else 0) + 16 * (1 - E('expo_out', pt)) + out_a * 120, E('back_out', pt), clamp(pt * 4) * (1 - out_a))
    # --- etapa b: prompt
    ip = oy + h - 190
    inp_a = prog(t, 21.45, 21.85)
    rrect(c, (ox + 40, ip, ox + w - 40, ip + 130), 44, ROW)
    txt = 'Editá este video con la skill'
    pt = prog(t, 21.75, 22.4)
    shown = txt[:int(len(txt) * pt)]
    if shown: draw_txt(c, (ox + 76, ip + 65), shown, 'Jakarta-Medium', 33, INK, 'lm')
    else: draw_txt(c, (ox + 76, ip + 65), 'Escribí tu prompt...', 'Jakarta-Medium', 32, (186, 180, 172), 'lm')
    press = prog(t, 22.4, 22.48) * (1 - prog(t, 22.48, 22.62))
    bs = 1 - .12 * press
    circle(c, ox + w - 40 - 52, ip + 65, int(40 * bs), CORAL)
    d = ImageDraw.Draw(c); bx, by = ox + w - 92, ip + 65
    d.line([(bx, by + 13), (bx, by - 13)], fill=WHITE + (255,), width=6); d.line([(bx - 12, by - 2), (bx, by - 14), (bx + 12, by - 2)], fill=WHITE + (255,), width=6, joint='curve')
    pb = prog(t, 22.5, 22.85)
    if pb > 0:
        L = Image.new('RGBA', (150, 54), (0, 0, 0, 0)); rrect(L, (0, 0, 150, 54), 27, CORAL)
        draw_txt(L, (75, 28), '1 prompt', 'Jakarta-Bold', 25, WHITE, 'mm')
        place(c, L, bx - 30, by - 92 - 12 * pb, E('back_out', pb), clamp(pb * 4))
    card_in(img, c, 540, 1060, t, t0 + .12, rise=320)
    # cursor al boton de enviar (coordenadas absolutas)
    cx0, cy0 = 540 - w / 2 - 40 + (ox + w - 92), 1060 - h / 2 - 40 + (by)
    ca = prog(t, 21.9, 22.15) * (1 - prog(t, 22.75, 22.95))
    if ca > 0:
        x, y = cursor_path(t, 21.95, 22.4, (900, 1560), (cx0 + 6, cy0 + 8), (840, cy0 + 380))
        draw_cursor(img, x, y, scale=lerp(.55, 1.0, prog(t, 21.95, 22.35)), alpha=ca, press=press)
    click_ring(img, int(cx0), int(cy0), prog(t, 22.45, 23.0))
    return crema_cam(img, t, Track([(17.1, 1.0), (17.9, 1.0, 'cine'), (19.2, 1.035, 'easy'), (21.5, 1.035, 'cine'), (22.8, 1.07)]), 540, 1080)

def face_avatar(foot, d=96):
    im = Image.fromarray(foot).crop((220, 240, 700, 720)).resize((d * 3, d * 3), Image.LANCZOS)
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse((0, 0, im.width - 1, im.height - 1), fill=255)
    im = im.convert('RGBA'); im.putalpha(m)
    return im.resize((d, d), Image.LANCZOS)

def s_cta(t, foot):                                   # 26.3 - 29.55
    t0 = 26.3
    img = cream_bg(0).copy()
    props(img, t, t0 + .1, PROPS_B)
    title(img, t, t0 + .2, [[('Comentá', INK)], [('"editor"', CORAL, 'u')]], 300)
    w, h = 860, 620
    base, pad = card_base(w, h)
    c = base.copy(); ox, oy = pad, pad
    draw_txt(c, (ox + 44, oy + 52), 'Comentarios', 'Jakarta-Bold', 36, INK, 'lm')
    draw_txt(c, (ox + w - 44, oy + 52), 'Ver todos', 'Jakarta-Medium', 25, GREY, 'rm')
    # fila 1: tu comentario
    pc1 = prog(t, 27.75, 28.2)
    if pc1 > 0:
        L = Image.new('RGBA', (w - 80, 100), (0, 0, 0, 0)); circle(L, 40, 50, 32, (222, 216, 208))
        draw_txt(L, (96, 30), 'vos', 'Jakarta-Medium', 22, GREY); draw_txt(L, (96, 62), 'editor', 'Jakarta-Bold', 34, INK)
        place(c, L, ox + w // 2, oy + 160 + 20 * (1 - E('expo_out', pc1)), 1.0, clamp(pc1 * 3), blur=10 * (1 - pc1))
    pc2 = prog(t, 28.3, 28.8)
    if pc2 > 0:
        L = Image.new('RGBA', (w - 80, 120), (0, 0, 0, 0)); L.alpha_composite(face_avatar(foot, 68), (6, 20))
        draw_txt(L, (96, 24), 'Respuesta automática', 'Jakarta-Medium', 22, GREY)
        rrect(L, (96, 58, 96 + 250, 58 + 54), 27, CORAL); draw_txt(L, (96 + 125, 86), 'Skill enviada', 'Jakarta-Bold', 25, WHITE, 'mm')
        place(c, L, ox + w // 2, oy + 290 + 20 * (1 - E('expo_out', pc2)), 1.0, clamp(pc2 * 3), blur=10 * (1 - pc2))
    # campo de comentario
    iy = oy + h - 150
    rrect(c, (ox + 40, iy, ox + w - 40, iy + 100), 36, ROW)
    typed = 'editor'[:int(6 * prog(t, 26.95, 27.4))] if t < 27.7 else ''
    if typed: draw_txt(c, (ox + 74, iy + 50), typed, 'Jakarta-Medium', 33, INK, 'lm')
    else: draw_txt(c, (ox + 74, iy + 50), 'Agregá un comentario...', 'Jakarta-Medium', 30, (186, 180, 172), 'lm')
    press = prog(t, 27.6, 27.68) * (1 - prog(t, 27.68, 27.82))
    pw = int(150 * (1 - .1 * press)); rrect(c, (ox + w - 60 - pw, iy + 18, ox + w - 60, iy + 82), 32, CORAL)
    draw_txt(c, (ox + w - 60 - pw // 2, iy + 51), 'Publicar', 'Jakarta-Bold', 27, WHITE, 'mm')
    card_in(img, c, 540, 960, t, t0 + .55, rise=300)
    # cuenta regresiva
    cw, ch = 860, 250
    b2, p2 = card_base(cw, ch); c2 = b2.copy()
    prg = prog(t, 28.15, 29.45)
    cx, cy, r = p2 + 150, p2 + ch // 2, 74
    L = Image.new('RGBA', (r * 2 * 4 + 40, r * 2 * 4 + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    bb = (20, 20, 20 + r * 8, 20 + r * 8)
    d.ellipse(bb, outline=LINE + (255,), width=40)
    if prg > .005: d.arc(bb, -90, -90 + 360 * prg, fill=CORAL + (255,), width=40)
    L = L.resize((L.width // 4, L.height // 4), Image.LANCZOS); c2.alpha_composite(L, (cx - L.width // 2, cy - L.height // 2))
    num = max(1, 5 - int(prg * 5)) if prg < 1 else None
    if num: draw_txt(c2, (cx, cy + 2), str(num), 'Outfit-Bold', 70, INK, 'mm')
    else:
        dd = ImageDraw.Draw(c2); dd.line([(cx - 24, cy + 2), (cx - 6, cy + 20), (cx + 28, cy - 20)], fill=CORAL + (255,), width=10, joint='curve')
    draw_txt(c2, (p2 + 270, p2 + 92), 'En menos de 5 segundos', 'Jakarta-Bold', 36, INK, 'lm')
    draw_txt(c2, (p2 + 270, p2 + 144), 'Tu skill llega a tus mensajes', 'Jakarta-Medium', 26, GREY, 'lm')
    card_in(img, c2, 540, 1490, t, 28.0, rise=260)
    bx = 540 - w / 2 - 40 + ox + w - 60 - 75; by = 960 - h / 2 - 40 + iy + 50
    ca = prog(t, 27.15, 27.4) * (1 - prog(t, 27.85, 28.1))
    if ca > 0:
        x, y = cursor_path(t, 27.2, 27.62, (900, 1450), (bx + 8, by + 8), (840, by + 300))
        draw_cursor(img, x, y, scale=lerp(.55, 1.0, prog(t, 27.2, 27.55)), alpha=ca, press=press)
    click_ring(img, int(bx), int(by), prog(t, 27.62, 28.15))
    return crema_cam(img, t, Track([(26.3, 1.0), (27.0, 1.0, 'cine'), (29.55, 1.05)]), 540, 1000)

# ------------------------------------------------------------------ montaje
SCENES = [s_face0, s_edit, s_face2, s_tools, s_face4, s_skill, s_face7, s_cta, s_face9]
BOUNDS = [0.0, 3.4, 8.4, 11.75, 15.85, 17.1, 22.9, 26.3, 29.55, 99.0]
KINDS = ['blob', 'punch', 'blob', 'punch', 'blob', 'blob', 'blob', 'blob']
BLOB_DUR = .72
BLOB_C = [((540, 900), (500, 1000)), None, ((300, 1200), (700, 800)), None, ((800, 1100), (400, 900)), ((250, 800), (780, 1050)),
          ((860, 1250), (330, 1000)), ((520, 700), (600, 1100))]

def render_frame(i, foot):
    t = i / FPS
    k = 0
    while k < len(SCENES) - 1 and t >= BOUNDS[k + 1]: k += 1
    # ventanas de transicion
    for j, kind in enumerate(KINDS):
        b = BOUNDS[j + 1]
        if kind == 'blob' and abs(t - b) < BLOB_DUR / 2:
            p = (t - (b - BLOB_DUR / 2)) / BLOB_DUR
            A = SCENES[j](t, foot).convert('RGBA'); B = SCENES[j + 1](t, foot).convert('RGBA')
            c1, c2 = BLOB_C[j]
            return np.array(blob_transition(A, B, p, c1, c2, seed=j + 1).convert('RGB'))
        if kind == 'punch' and b <= t < b + .15:
            img = SCENES[j + 1](t, foot).convert('RGBA')
            a = [.55, .32, .16, .06][min(3, int((t - b) * FPS))]
            img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(255 * a))))
            return np.array(img.convert('RGB'))
    return np.array(SCENES[k](t, foot).convert('RGB'))

def _frame_at(t):
    buf = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.4f}', '-i', SRC, '-frames:v', '1', '-vf', f'scale={W}:{H}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(buf, np.uint8).reshape(H, W, 3)

def stills(times, out):
    tiles = []
    for t in times:
        tiles.append(Image.fromarray(render_frame(int(round(t * FPS)), _frame_at(t))).resize((324, 576), Image.LANCZOS))
    cols = 6; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 324, rows * 576), (40, 40, 40))
    for k, im in enumerate(tiles): sheet.paste(im, ((k % cols) * 324, (k // cols) * 576))
    sheet.save(out, quality=88)

def render_range(a, b, out):
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{a / FPS:.5f}', '-i', SRC, '-vf', f'fps={FPS},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', f'{FPS}', '-i', '-',
                            '-c:v', 'libx264', '-crf', '15', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    n = W * H * 3
    for i in range(a, b):
        buf = dec.stdout.read(n)
        if len(buf) < n: break
        enc.stdin.write(render_frame(i, np.frombuffer(buf, np.uint8).reshape(H, W, 3)).tobytes())
    enc.stdin.close(); enc.wait(); dec.kill()

def mux(parts_dir, out):
    parts = sorted(glob.glob(os.path.join(parts_dir, 'p*.mp4')), key=lambda p: int(os.path.basename(p)[1:-4]))
    lst = os.path.join(parts_dir, 'l.txt')
    open(lst, 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    tmp = os.path.join(parts_dir, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', tmp], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', SRC, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'stills': stills([float(x) for x in sys.argv[3].split(',')], sys.argv[2])
    elif m == 'part': render_range(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    elif m == 'mux': mux(sys.argv[2], sys.argv[3])
