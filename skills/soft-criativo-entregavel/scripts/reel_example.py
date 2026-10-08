"""
Edicion v2: la facecam de uii.mp4 pasa intacta; solo se reemplazan los rangos de pantalla blanca.
    python3 reel_example.py stills hoja.jpg t1,t2,...
    python3 reel_example.py part A B parts/pNNN.mp4
    python3 reel_example.py mux parts/ salida.mp4
"""
import os, sys, math, subprocess, functools, glob, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))          # .../scripts
sys.path.insert(0, HERE)
WORK = os.environ.get('WORKDIR', os.getcwd())               # carpeta del proyecto: crudo_small.npy y bgs/
import coral_lib as R
from coral_lib import (F, tsp, tw, draw_txt, rrect, circle, E, W, H, CORAL, CORAL_L, CORAL_D, CORAL_K, CREAM, INK, GREY, LINE, WHITE, TINT, ROW,
                  cream_bg, asterisk, card_base, click_ring, cursor_path, FPS)
from engine import place, paste, draw_cursor, pixel_ring, shards, logo_tile, rounded_tile
from motion import Track, prog, clamp, lerp, camera, shake, wiggle, EASE, get_ease, spring

SRC = os.environ.get('CRUDO', 'crudo.mp4')
LIME = (196, 238, 52); LIME_D = (130, 186, 12); LIME_L = (226, 255, 100); MARK = (208, 246, 62)
RED_T = (240, 70, 48)
_lt = functools.lru_cache(None)(lambda kind, size: logo_tile(kind, size))

# ------------------------------------------------------------------ frames del crudo (miniaturas)
_CR = None
def crudo(i):
    global _CR
    if _CR is None: _CR = np.load(os.path.join(WORK, 'crudo_small.npy'), mmap_mode='r')
    return np.asarray(_CR[max(0, min(767, int(i)))])
def fidx(t): return int(round(t * FPS))

@functools.lru_cache(None)
def rmask(w, h, r):
    m = Image.new('L', (w * 3, h * 3), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 3 - 1, h * 3 - 1), r * 3, fill=255)
    return m.resize((w, h), Image.LANCZOS)

def round_img(im, r):
    im = im.convert('RGBA'); im.putalpha(rmask(im.width, im.height, r)); return im

def vid(fi, w, h, r=0):
    im = Image.fromarray(crudo(fi)).resize((w, h), Image.BICUBIC)
    return round_img(im, r) if r else im.convert('RGBA')

# ------------------------------------------------------------------ props 3D (3 paletas)
PAL = {'coral': ((255, 120, 92), (206, 44, 26), (190, 40, 24)), 'lime': ((228, 255, 100), (132, 192, 12), (110, 160, 10)),
       'red': ((255, 112, 86), (186, 34, 20), (110, 16, 10))}

@functools.lru_cache(None)
def prop2(kind, size, pal):
    top, bot, shc = PAL[pal]; ss = 2
    bw, bh = (size, int(size * .43)) if kind == 'pill' else (size, size)
    pad = int(size * .18); cw, ch = bw + pad * 2, bh + pad * 2
    mask = Image.new('L', (bw * ss, bh * ss), 0); md = ImageDraw.Draw(mask)
    if kind == 'pill': md.rounded_rectangle((0, 0, bw * ss - 1, bh * ss - 1), bh * ss // 2, fill=255)
    elif kind == 'check': md.ellipse((0, 0, bw * ss - 1, bh * ss - 1), fill=255)
    else:
        pts = [(0, -1), (.17, -.17), (1, 0), (.17, .17), (0, 1), (-.17, .17), (-1, 0), (-.17, -.17)]; c = bw * ss / 2
        md.polygon([(c + x * c * .98, c + y * c * .98) for x, y in pts], fill=255)
    obj = R._shaded(mask, top, bot, (.34, .24, .55, .45) if kind != 'spark' else (.4, .4, .4, .4))
    if kind == 'check':
        d = ImageDraw.Draw(obj); S = bw * ss; col = (255, 255, 255, 255) if pal != 'lime' else (34, 60, 8, 255)
        pts = [(S * .27, S * .52), (S * .43, S * .68), (S * .74, S * .34)]
        d.line(pts, fill=col, width=int(S * .11), joint='curve')
        for p in (pts[0], pts[-1]): d.ellipse((p[0] - S * .055, p[1] - S * .055, p[0] + S * .055, p[1] + S * .055), fill=col)
    L = Image.new('RGBA', (cw * ss, ch * ss), (0, 0, 0, 0)); sh = Image.new('RGBA', L.size, (0, 0, 0, 0))
    shm = Image.new('RGBA', mask.size, shc + (120,)); shm.putalpha(mask.point(lambda v: int(v * .55)))
    sh.alpha_composite(shm, (pad * ss, pad * ss + int(size * .07 * ss))); sh = sh.filter(ImageFilter.GaussianBlur(size * .06 * ss))
    L.alpha_composite(sh); L.alpha_composite(obj, (pad * ss, pad * ss))
    return L.resize((cw, ch), Image.LANCZOS)

def props2(img, t, t0, layout, pal, gain=1.0):
    for i in sorted(range(len(layout)), key=lambda i: -layout[i][5]):
        kind, size, x, y, rot, blur, ph = layout[i]
        ta = t0 + .06 * i; p = prog(t, ta, ta + .85)
        if p <= 0: continue
        e = E('expo_out', p); s = E('back_out_x', p)
        vx, vy = x - 540, y - 960; n = math.hypot(vx, vy) or 1
        ox, oy = vx / n * (1 - e) * 320, vy / n * (1 - e) * 320
        dy = 14 * gain * math.sin(2 * math.pi * (t * .45 + ph)); dx = 8 * gain * math.cos(2 * math.pi * (t * .33 + ph * 1.7))
        dr = 5 * gain * math.sin(2 * math.pi * (t * .28 + ph)); sc = max(.05, s)
        if kind == 'spark': dr = t * 38 + ph * 90; sc *= 1 + .16 * math.sin(2 * math.pi * (t * .9 + ph))
        place(img, prop2(kind, size, pal), x + ox + dx, y + oy + dy, sc, clamp(p * 4), blur=blur + 16 * (1 - e), rot=rot + dr)

P_CORAL_A = [('pill', 330, 96, 600, -24, 0, .0), ('check', 90, 996, 505, 0, 0, .3), ('pill', 560, 980, 1745, 30, 9, .55),
             ('check', 88, 92, 1712, 0, 0, .1), ('spark', 66, 150, 330, 0, 0, .5), ('spark', 58, 975, 1440, 0, 0, .8)]
P_CORAL_B = [('pill', 340, 980, 470, 28, 0, .2), ('check', 90, 80, 690, 0, 0, .4), ('pill', 540, 90, 1760, -34, 9, .7),
             ('check', 92, 1000, 1715, 0, 0, .0), ('spark', 64, 960, 330, 0, 0, .6), ('spark', 56, 110, 1480, 0, 0, .2)]
P_LIME = [('pill', 360, 110, 520, -28, 0, .0), ('check', 92, 985, 440, 0, 0, .3), ('pill', 560, 990, 1750, 28, 9, .55),
          ('check', 90, 95, 1700, 0, 0, .1), ('spark', 66, 170, 300, 0, 0, .5), ('spark', 60, 965, 1385, 0, 0, .8),
          ('check', 64, 140, 1390, 0, 0, .4), ('spark', 44, 520, 215, 0, 0, .2)]
P_RED = [('pill', 340, 920, 215, -22, 6, .0), ('pill', 560, 95, 1740, 22, 10, .4), ('check', 96, 960, 1565, 0, 0, .2),
         ('spark', 60, 110, 430, 0, 0, .5), ('spark', 64, 965, 1700, 0, 0, .9), ('spark', 40, 160, 1300, 0, 0, .3)]

# ------------------------------------------------------------------ fondos
def _bg(base, glows):
    h, w = 480, 270; yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); u, v = xx / w, yy / h
    a = np.zeros((h, w, 3), np.float32) + np.array(base, np.float32)
    for cx, cy, r, col, al in glows:
        d = np.sqrt(((u - cx) * .5625) ** 2 + (v - cy) ** 2); g = (np.exp(-(d / r) ** 2) * al)[..., None]
        a = a * (1 - g) + np.array(col, np.float32) * g
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB').resize((W, H), Image.BICUBIC).convert('RGBA')

@functools.lru_cache(None)
def bg_lime(): return _bg((239, 242, 228), [(.92, .9, .2, (212, 248, 60), .35), (.06, .2, .2, (212, 248, 60), .18), (.5, .0, .4, (250, 252, 240), .6)])
@functools.lru_cache(None)
def bg_red(): return _bg((52, 20, 14), [(.5, .5, .55, (122, 36, 26), .9), (.5, 1.0, .5, (30, 10, 8), .5), (.5, .0, .5, (30, 10, 8), .35)])

# ------------------------------------------------------------------ utilidades UI
def rr_path(x0, y0, x1, y1, r, n=10):
    pts = []
    def arc(cx, cy, a0, a1):
        for k in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * k / n); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts += [(x0 + r, y0), (x1 - r, y0)]; arc(x1 - r, y0 + r, -90, 0); pts.append((x1, y1 - r)); arc(x1 - r, y1 - r, 0, 90)
    pts.append((x0 + r, y1)); arc(x0 + r, y1 - r, 90, 180); pts.append((x0, y0 + r)); arc(x0 + r, y0 + r, 180, 270); pts.append((x0 + r, y0))
    return pts

def dashed_rr(img, box, r, col, width=3, dash=16, gap=12, a=255, progress=1.0):
    pts = rr_path(*box, r); d = ImageDraw.Draw(img)
    tot = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) * progress
    acc = 0.0; walked = 0.0; on = True
    for i in range(len(pts) - 1):
        p0, p1 = pts[i], pts[i + 1]; L = math.dist(p0, p1)
        if L < 1e-6: continue
        k = max(1, int(L // 5)); 
        for j in range(k):
            s = L / k; walked += s
            if walked > tot: return
            if on:
                a0 = (p0[0] + (p1[0] - p0[0]) * j / k, p0[1] + (p1[1] - p0[1]) * j / k)
                a1 = (p0[0] + (p1[0] - p0[0]) * (j + 1) / k, p0[1] + (p1[1] - p0[1]) * (j + 1) / k)
                d.line([a0, a1], fill=col + (a,), width=width)
            acc += s
            if acc >= (dash if on else gap): acc = 0; on = not on

def slide_text(img, txt, fname, size, color, cx, cy, t, ta, dur=.55, hl=None, hlt=.25):
    p = prog(t, ta, ta + dur)
    if p <= 0: return
    f = F(fname, size); w = int(f.getlength(txt)) + 44; h = int(size * 1.55)
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if hl:
        ph = E('expo_out', prog(t, ta + hlt, ta + hlt + .45))
        if ph > .01: rrect(L, (12, int(h * .2), 12 + max(4, int((w - 24) * ph)), int(h * .86)), 14, hl)
    off = (1 - E('expo_out', p)) * size * 1.0
    ImageDraw.Draw(L).text((w / 2, h / 2 + off), txt, font=f, fill=color + (255,), anchor='mm')
    paste(img, L, (cx - w / 2, cy - h / 2), clamp(p * 3))

def title2(img, t, t0, lines, y0, size=128, lh=150, mark=MARK):
    for li, line in enumerate(lines):
        sp = tw(' ', 'Outfit-SemiBold', size) * .9
        ws = [tw(w[0], 'Outfit-SemiBold', size) for w in line]; tot = sum(ws) + sp * (len(line) - 1); x = 540 - tot / 2
        for wi, w in enumerate(line):
            ta = t0 + (li * 2 + wi) * .09; p = prog(t, ta, ta + .55); cy = y0 + li * lh
            if p > 0:
                e = E('expo_out', p)
                if len(w) > 2 and w[2] == 'm':
                    pm = E('expo_out', prog(t, ta + .35, ta + .95))
                    if pm > .01:
                        L = Image.new('RGBA', (int(ws[wi] + 44), int(size * .72)), (0, 0, 0, 0))
                        rrect(L, (0, 0, max(4, int((ws[wi] + 44) * pm)), L.height), 22, mark); paste(img, L, (x - 22, cy - size * .34 + 44 * (1 - e)))
                place(img, tsp(w[0], 'Outfit-SemiBold', size, w[1]), x + ws[wi] / 2, cy + 44 * (1 - e), 1.0, clamp(p * 3), blur=18 * (1 - E('easy_in', p)))
            x += ws[wi] + sp

def stepper2(img, t, t_in, y, idx, t_chg, labels=('Subir', 'Prompt', 'Espera', 'Listo')):
    f = F('Jakarta-SemiBold', 31); wid = [int(f.getlength(l)) + 116 for l in labels]; gap = 20
    x = 540 - (sum(wid) + gap * (len(labels) - 1)) / 2
    for i, lab in enumerate(labels):
        pin = prog(t, t_in + i * .08, t_in + .55 + i * .08)
        active = idx == i; done = idx > i; h = 76
        L = Image.new('RGBA', (wid[i] + 40, h + 40), (0, 0, 0, 0)); sh = Image.new('RGBA', L.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((20, 26, 20 + wid[i], 26 + h), h // 2, fill=(60, 30, 20, 40)); L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
        rrect(L, (20, 20, 20 + wid[i], 20 + h), h // 2, CORAL if active else WHITE)
        cy = 20 + h // 2
        circle(L, 20 + 40, cy, 22, WHITE if active else (CORAL if done else (238, 233, 226)))
        if done: ImageDraw.Draw(L).line([(20 + 31, cy), (20 + 38, cy + 8), (20 + 50, cy - 8)], fill=WHITE + (255,), width=5, joint='curve')
        elif not active: draw_txt(L, (20 + 40, cy + 1), str(i + 1), 'Jakarta-Bold', 26, GREY, 'mm')
        draw_txt(L, (20 + 78, cy + 1), lab, 'Jakarta-Bold', 31, WHITE if active else INK, 'lm')
        pop = 1 + .08 * math.sin(math.pi * prog(t, t_chg, t_chg + .32)) if active else 1.0
        place(img, L, x + wid[i] / 2, y - 80 * (1 - E('expo_out', pin)), pop, clamp(pin * 3), blur=14 * (1 - E('easy_in', pin)))
        x += wid[i] + gap

def chat_card(w, h):
    base, pad = card_base(w, h); c = base.copy(); ox, oy = pad, pad
    c.alpha_composite(asterisk(40), (ox + 40, oy + 34)); draw_txt(c, (ox + 96, oy + 54), 'Claude', 'Jakarta-Bold', 36, INK, 'lm')
    ImageDraw.Draw(c).line([(ox + 2, oy + 100), (ox + w - 2, oy + 100)], fill=LINE + (255,), width=2)
    return c, ox, oy

def glow_disc(img, cx, cy, r, col, a):
    if a <= .01: return
    L = Image.new('RGBA', (int(r * 3), int(r * 3)), col + (0,))
    ImageDraw.Draw(L).ellipse((r * .5, r * .5, r * 2.5, r * 2.5), fill=col + (int(255 * clamp(a)),))
    paste(img, L.filter(ImageFilter.GaussianBlur(r * .35)), (cx - L.width / 2, cy - L.height / 2))

def zoom_cam(img, t, keys):
    z = Track(keys)(t); return camera(img, z) if z > 1.0005 else img

def shake_cam(img, t, hits):
    dx = dy = 0.0
    for t0, amp, dec in hits:
        if t0 <= t < t0 + dec:
            s = shake(t, amp=amp, freq=15, decay=dec, t0=t0, seed=int(t0 * 10)); dx += s[0]; dy += s[1]
    return camera(img, 1.03, dx=dx, dy=dy) if (dx or dy) else img

# ================================================================== S1: TUMBA
PADS = 60; SW, SH = 520, 760
CRACK = [(260, -20), (236, 92), (288, 172), (244, 262), (294, 352), (250, 444), (286, 534), (246, 622), (272, 704), (256, 780)]
BRANCH = [(288, 172), (352, 208), (392, 262), (432, 284)]

@functools.lru_cache(None)
def stone_base():
    ss = 2; S = Image.new('RGBA', ((SW + 2 * PADS) * ss, (SH + 2 * PADS) * ss), (0, 0, 0, 0))
    x0, y0, x1, y1 = PADS * ss, PADS * ss, (PADS + SW) * ss, (PADS + SH) * ss
    m = Image.new('L', S.size, 0); ImageDraw.Draw(m).rounded_rectangle((x0, y0, x1, y1), 260 * ss, fill=255, corners=(True, True, False, False))
    t = np.linspace(0, 1, S.height, dtype=np.float32)[:, None, None]; xs = np.linspace(0, 1, S.width, dtype=np.float32)[None, :, None]
    col = (np.array((74, 66, 64), np.float32) * (1 - t) + np.array((34, 30, 31), np.float32) * t) * (1.08 - .22 * xs)
    img = Image.fromarray(np.clip(np.repeat(col, 1, axis=1) if False else np.broadcast_to(col, (S.height, S.width, 3)), 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    S.paste(img, (0, 0), m)
    D = Image.new('RGBA', S.size, (0, 0, 0, 0)); d = ImageDraw.Draw(D)
    ins = 30 * ss
    d.rounded_rectangle((x0 + ins, y0 + ins, x1 - ins, y1 + 200 * ss), 228 * ss, outline=(104, 94, 92, 255), width=5 * ss, corners=(True, True, False, False))
    cx, cy, k = (PADS + SW // 2) * ss, (PADS + 300) * ss, 96 * ss
    d.rounded_rectangle((cx - k, cy - k, cx + k, cy + k), 44 * ss, fill=(240, 69, 47, 255))
    d.polygon([(cx - 26 * ss, cy - 44 * ss), (cx - 26 * ss, cy + 44 * ss), (cx + 50 * ss, cy)], fill=(255, 255, 255, 255))
    d.rounded_rectangle((cx - 96 * ss, cy + 150 * ss, cx + 96 * ss, cy + 166 * ss), 8 * ss, fill=(104, 94, 92, 255))
    d.rounded_rectangle((cx - 60 * ss, cy + 190 * ss, cx + 60 * ss, cy + 204 * ss), 7 * ss, fill=(90, 82, 80, 255))
    D.putalpha(ImageChops.multiply(D.getchannel('A'), m)); S.alpha_composite(D)
    return S.resize((SW + 2 * PADS, SH + 2 * PADS), Image.LANCZOS)

def crack_pts(pts_src, p):
    pts = [(x + PADS, y + PADS) for x, y in pts_src]; Ls = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    lim = sum(Ls) * p; out = [pts[0]]; acc = 0
    for i, l in enumerate(Ls):
        if acc + l <= lim: out.append(pts[i + 1]); acc += l
        else:
            f = (lim - acc) / l; out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)); break
    return out

def draw_cracks(S, p, lit=1.0):
    ss = 2; L = Image.new('RGBA', (S.width * ss, S.height * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for pts_src, pp in ((CRACK, p), (BRANCH, clamp((p - .3) / .6))):
        if pp <= 0: continue
        pts = [(x * ss, y * ss) for x, y in crack_pts(pts_src, pp)]
        if len(pts) < 2: continue
        d.line(pts, fill=(12, 9, 9, 255), width=int(9 * ss), joint='curve')
        d.line(pts, fill=(255, int(100 + 40 * lit), int(70 + 20 * lit), 255), width=int(4 * ss), joint='curve')
    g = L.filter(ImageFilter.GaussianBlur(7 * ss)); ga = g.getchannel('A').point(lambda v: int(min(255, v * 1.4 * lit)))
    gl = Image.new('RGBA', g.size, (255, 96, 66, 255)); gl.putalpha(ga)
    Sx = S.resize(L.size, Image.BILINEAR); Sx.alpha_composite(gl); Sx.alpha_composite(L)
    return Sx.resize(S.size, Image.LANCZOS)

@functools.lru_cache(None)
def half_masks():
    ss = 2; pts = [((x + PADS) * ss, (y + PADS) * ss) for x, y in CRACK]; Wd, Hd = (SW + 2 * PADS) * ss, (SH + 2 * PADS) * ss
    ml = Image.new('L', (Wd, Hd), 0); mr = Image.new('L', (Wd, Hd), 0)
    ImageDraw.Draw(ml).polygon([(-10, -10)] + pts + [(-10, Hd + 10)], fill=255)
    ImageDraw.Draw(mr).polygon([(Wd + 10, -10)] + pts + [(Wd + 10, Hd + 10)], fill=255)
    return ml.resize((SW + 2 * PADS, SH + 2 * PADS), Image.LANCZOS), mr.resize((SW + 2 * PADS, SH + 2 * PADS), Image.LANCZOS)

def place_pivot(img, layer, cx, cy, pivot, rot, dx, dy, a=1.0):
    th = math.radians(rot); vx, vy = cx - pivot[0], cy - pivot[1]
    nx = pivot[0] + vx * math.cos(th) + vy * math.sin(th); ny = pivot[1] - vx * math.sin(th) + vy * math.cos(th)
    place(img, layer, nx + dx, ny + dy, 1.0, a, rot=rot)

P_S1 = P_CORAL_A
def sc_grave(t):
    img = scene_bg('coral', t, 1.0)
    cx = 540; base_y = 1380
    # montículo
    pm = prog(t, 1.15, 1.75)
    if pm > 0:
        L = Image.new('RGBA', (900, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((110, 90, 790, 190), fill=(80, 40, 30, 90)); L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
        d.ellipse((120, 80, 780, 170), fill=(70, 62, 60, 255)); d.ellipse((150, 84, 750, 150), fill=(92, 82, 80, 255))
        place(img, L, cx, base_y + 18, E('back_out', pm), clamp(pm * 4))
    fall = prog(t, 1.38, 1.74)
    yc = Track([(1.38, -560, 'expo_in'), (1.74, 1000, 'expo_out'), (1.84, 980, 'easy'), (1.98, 1000)])(t)
    cp = E('expo_inout', prog(t, 2.02, 2.52)); lit = .6 + .4 * math.sin(max(0, t - 2.02) * 14) ** 2 if t > 2.02 else 0
    S = stone_base()
    if t >= 1.38:
        if t < 2.62:
            tremor = (wiggle(t, 30, 5, 3), wiggle(t, 26, 2, 7)) if 2.5 <= t < 2.62 else (0, 0)
            st = draw_cracks(S, cp, lit) if cp > .005 else S
            speed = abs(Track([(1.38, -560, 'expo_in'), (1.74, 1000)])(t + .02) - Track([(1.38, -560, 'expo_in'), (1.74, 1000)])(t - .02)) if t < 1.76 else 0
            place(img, st, cx + tremor[0], yc + tremor[1], 1.0, 1.0, blur=min(10, speed * .05))
        else:
            full = draw_cracks(S, 1.0, 1.0); ml, mr = half_masks()
            Lh = full.copy(); Lh.putalpha(ImageChops.multiply(full.getchannel('A'), ml)); Rh = full.copy(); Rh.putalpha(ImageChops.multiply(full.getchannel('A'), mr))
            pop = E('expo_out', prog(t, 2.62, 2.78)); s_ = max(0.0, t - 2.7); e = min(1.8, (s_ / .62) ** 2)
            pl = (cx - SW / 2, base_y); pr = (cx + SW / 2, base_y)
            place_pivot(img, Lh, cx, 1000, pl, pop * 7 + e * 26, -pop * 60 - e * 330, e * 620)
            place_pivot(img, Rh, cx, 1000, pr, -pop * 6 - e * 22, pop * 64 + e * 360, e * 560)
    # impacto
    for k, (rr0, rr1, off) in enumerate([(70, 330, -250), (60, 280, 250)]):
        pixel_ring(img, cx + off, base_y + 6, prog(t, 1.74, 2.3), r0=rr0, r1=rr1, cell=16, color=(236, 190, 168) if k else CORAL_L, seed=11 + k, count=170)
    # estallido
    glow_disc(img, cx, 840, 340, (255, 120, 90), (1 - prog(t, 2.62, 3.1)) * .55 if t >= 2.62 else 0)
    click_ring(img, cx, 840, prog(t, 2.62, 3.15), CORAL)
    shards(img, (cx - 90, 640, cx + 90, 1280), prog(t, 2.64, 3.4), seed=5, colors=(CORAL, (60, 52, 50), CORAL_L, (255, 255, 255)), n=120, g=1500, spread=800)
    return shake_cam(img, t, [(1.74, 18, .5), (2.62, 14, .45)])

# ================================================================== S2: SUBIR -> ENVIAR -> EDITAR
CW2, CH2 = 860, 900
def sc_upload(t):
    img = scene_bg('coral', t, 5.0)
    idx = 0 if t < 6.2 else (1 if t < 6.62 else 2)
    c, ox, oy = chat_card(CW2, CH2); w = CW2
    zx0, zy0, zx1, zy1 = ox + 40, oy + 130, ox + w - 40, oy + 130 + 560
    za = 1 - E('expo_in', prog(t, 6.62, 6.82))
    if za > 0.01:
        Z = Image.new('RGBA', c.size, (0, 0, 0, 0)); dashed_rr(Z, (zx0, zy0, zx1, zy1), 34, (214, 206, 196), 3, 16, 12, int(255 * za), progress=E('expo_out', prog(t, 5.2, 5.8))); c.alpha_composite(Z)
    # barra de entrada (input)
    pin = E('expo_out', prog(t, 6.2, 6.55)); iy = oy + CH2 - 238
    if pin > 0:
        Lb = Image.new('RGBA', (w - 80, 140), (0, 0, 0, 0)); rrect(Lb, (0, 0, w - 80, 140), 46, ROW)
        press = prog(t, 6.62, 6.7) * (1 - prog(t, 6.7, 6.84)); r_ = int(42 * (1 - .12 * press))
        circle(Lb, w - 80 - 70, 70, r_, CORAL); dd = ImageDraw.Draw(Lb); bx, by = w - 150, 70
        dd.line([(bx, by + 14), (bx, by - 14)], fill=WHITE + (255,), width=6); dd.line([(bx - 13, by - 2), (bx, by - 15), (bx + 13, by - 2)], fill=WHITE + (255,), width=6, joint='curve')
        paste(c, Lb, (ox + 40, iy + 80 * (1 - pin)), pin)
    # miniatura: cae en la zona -> barra -> viaja al input
    tw_, th_ = 250, 444; zc = ((zx0 + zx1) / 2, zy0 + 262)
    pd = prog(t, 5.4, 5.8); fly = E('expo_inout', prog(t, 6.22, 6.58))
    bar = E('easy', prog(t, 5.72, 6.2))
    thumb = vid(fidx(t), tw_, th_, 26)
    if t >= 5.4 and t < 6.64:
        sc = lerp(1.0, 66 / tw_, fly); px = lerp(zc[0], ox + 86, fly); py = lerp(zc[1] - 20 + (-380 * (1 - E('expo_out', pd))), oy + CH2 - 168, fly)
        a = clamp(pd * 3)
        s2 = E('back_out_x', pd) if fly == 0 else 1.0
        sh = Image.new('RGBA', (tw_ + 80, th_ + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((40, 52, 40 + tw_, 52 + th_), 26, fill=(60, 30, 20, 70))
        place(c, sh.filter(ImageFilter.GaussianBlur(14)), px, py + 4, sc * (.35 + .65 * s2), a * (1 - fly))
        place(c, thumb, px, py, sc * (.35 + .65 * s2), a)
        if pd > 0 and fly == 0:
            bx0, by = zc[0] - 170, zc[1] + th_ / 2 + 34
            rrect(c, (bx0, by, bx0 + 340, by + 14), 7, LINE)
            if bar > .02: rrect(c, (bx0, by, bx0 + max(14, int(340 * bar)), by + 14), 7, CORAL)
            R.check_badge(c, int(zc[0] + tw_ / 2 - 6), int(zc[1] - th_ / 2 + 6), 26, prog(t, 6.14, 6.5) * (1 if fly == 0 else 0))
    # enviado: burbuja con el video + Claude editando
    sent = prog(t, 6.64, 7.0)
    if sent > 0:
        bubw, bubh = 250, 300; e = E('expo_out', sent)
        Bb = Image.new('RGBA', (bubw + 20, bubh + 20), (0, 0, 0, 0)); rrect(Bb, (0, 0, bubw + 20, bubh + 20), 36, CORAL)
        Bb.alpha_composite(vid(fidx(t), bubw - 20, bubh - 20, 26), (20 - 10 + 0, 10)) if False else Bb.alpha_composite(vid(fidx(t), bubw - 10, bubh - 10, 28), (15, 15))
        place(c, Bb, ox + w - 40 - 145, oy + 270 + 60 * (1 - e), E('back_out', sent), clamp(sent * 3))
        sp = prog(t, 6.78, 7.2)
        if sp > 0:
            ya = oy + 500
            ang = (t - 6.78) * 380
            A = asterisk(58).rotate(ang, resample=Image.BICUBIC); place(c, A, ox + 90, ya + 40, E('back_out', sp), clamp(sp * 4))
            for k, wd in enumerate((470, 360, 250)):
                ps = prog(t, 6.84 + k * .05, 7.2 + k * .05)
                if ps <= 0: continue
                Ln = Image.new('RGBA', (wd, 22), (0, 0, 0, 0)); rrect(Ln, (0, 0, wd, 22), 11, (236, 230, 222))
                hx = ((t * 520 + k * 140) % (wd + 200)) - 100; Hl = Image.new('RGBA', (90, 22), (255, 255, 255, 190)); Ln.alpha_composite(Hl, (int(hx) - 45, 0)) if 0 <= hx - 45 < wd - 40 else None
                paste(c, Ln, (ox + 170 + 40 * (1 - E('expo_out', ps)), ya + 6 + k * 34), ps)
            # linea de tiempo que se arma
            ty = ya + 150; tr_ = Image.new('RGBA', (w - 80, 120), (0, 0, 0, 0)); rrect(tr_, (0, 0, w - 80, 120), 28, ROW)
            clips = [(24, 150, CORAL), (186, 110, INK), (308, 190, CORAL_L), (510, 120, TINT), (642, 144, CORAL)]
            for k, (x_, wd, col) in enumerate(clips):
                pc = E('back_out', prog(t, 6.9 + k * .05, 7.25 + k * .05))
                if pc > 0: rrect(tr_, (x_, 26, x_ + int(wd * pc), 94), 18, col)
            ph_ = E('easy', prog(t, 6.95, 7.45)); px_ = 24 + ph_ * (w - 80 - 48)
            d3 = ImageDraw.Draw(tr_); d3.line([(px_, 8), (px_, 112)], fill=INK + (255,), width=4); d3.ellipse((px_ - 9, 2, px_ + 9, 20), fill=INK + (255,))
            place(c, tr_, ox + w / 2, ty + 60, 1.0, clamp(sp * 3))
    R.card_in(img, c, 540, 1010, t, 5.0, rise=320)
    # cursor
    cx0 = 540 - c.width / 2 + ox + w - 110; cy0 = 1010 - c.height / 2 + iy + 80 + 70
    ca = prog(t, 6.12, 6.36) * (1 - prog(t, 6.86, 7.02))
    if ca > 0:
        x, y = cursor_path(t, 6.16, 6.62, (900, 1600), (cx0 + 8, cy0 + 8), (850, cy0 + 360))
        draw_cursor(img, x, y, scale=lerp(.55, 1.0, prog(t, 6.16, 6.56)), alpha=ca, press=prog(t, 6.62, 6.7) * (1 - prog(t, 6.7, 6.84)))
    click_ring(img, int(cx0), int(cy0), prog(t, 6.62, 7.1))
    return zoom_cam(img, t, [(4.96, 1.0), (5.5, 1.0, 'cine'), (7.5, 1.06)])

# ================================================================== S3a: TRES HERRAMIENTAS (lima)
def sc_tools(t):
    img = bg_lime().copy(); props2(img, t, 9.2, P_LIME, 'lime', gain=1.25)
    fade = 1 - E('expo_in', prog(t, 11.75, 12.1))
    # circulos del escenario (como la referencia) + pings
    if fade > 0.01:
        Rg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(Rg); pa = E('expo_out', prog(t, 9.1, 9.9))
        for k, cx in enumerate((400, 700)):
            r = 320 * pa * (1 + .03 * math.sin(t * 2.2 + k)); d.ellipse((cx - r, 1020 - r, cx + r, 1020 + r), outline=(190, 236, 70, int(150 * fade)), width=3)
        for k in range(2):
            q = ((t - 9.4 - k * 1.1) % 2.2) / 2.2
            if t > 9.4 + k * 1.1: rr_ = 120 + 420 * E('expo_out', q); d.ellipse((540 - rr_, 1020 - rr_, 540 + rr_, 1020 + rr_), outline=(200, 242, 80, int(130 * (1 - q) * fade)), width=3)
        img.alpha_composite(Rg)
    # carrusel: entra, se corre al costado, entra el siguiente
    xL, xR = 290, 790; tiles = ['claude', 'remotion', 'higgs']
    tr = [Track([(9.15, xL), (10.15, xL, 'expo_inout'), (10.7, xL - 500)]),
          Track([(9.5, xR), (10.15, xR, 'expo_inout'), (10.7, xL), (10.95, xL, 'expo_inout'), (11.45, xL - 500)]),
          Track([(10.15, xR + 500, 'expo_inout'), (10.7, xR), (10.95, xR, 'expo_inout'), (11.45, xL)])]
    t_in = [9.15, 9.5, 10.15]
    if fade > .01:
        # signo x entre los dos visibles
        pxm = E('expo_out', prog(t, 9.6, 10.0)) * (1 - E('expo_in', prog(t, 10.0, 10.2)) * 0) 
        for i in range(3):
            if t < t_in[i]: continue
            x = tr[i](t); pop = prog(t, t_in[i], t_in[i] + .7); rise = 1.0
            tile, pd = _lt(tiles[i], 270)
            up = E('expo_in', prog(t, 11.75, 12.15)) * 520
            place(img, tile, x, 1020 - up, max(.05, E('back_out_x', pop)) if i != 2 else 1.0 * max(.05, E('back_out', prog(t, 10.15, 10.9))), clamp(pop * 4) * fade, blur=10 * (1 - E('expo_out', pop)) + 14 * E('expo_in', prog(t, 11.75, 12.1)))
            if i < 2:
                pr = prog(t, t_in[i] + .02, t_in[i] + .6)
                if 0 < pr < 1: click_ring(img, int(x), 1020, pr, LIME_D)
        if t > 9.6:
            xm = 540; ps = prog(t, 9.6, 9.95) * (1 - prog(t, 10.1, 10.3)) + prog(t, 10.75, 11.0) * (1 - prog(t, 11.0, 11.12)) * 0
            hide = prog(t, 11.0, 11.12) if t > 10.7 else 0
            sx = prog(t, 9.6, 9.95) if t < 10.2 else (1 - prog(t, 10.2, 10.3)) if t < 10.7 else prog(t, 10.7, 11.0) * (1 - prog(t, 11.05, 11.15))
            if sx > .01: draw_txt(img, (xm, 1020), '×', 'Outfit-Medium', int(70 * (.6 + .4 * sx)), (150, 150, 140), 'mm')
    # titulo
    title2(img, t, 10.5, [[('Solo', INK), ('3', INK, 'm')], [('herramientas', INK)]], 330)
    # fase numerada: ranuras, chip, logo, nombre con marcador
    xs = [195, 540, 885]; chips = [11.8, 13.3, 14.85]; pops = [12.45, 14.2, 15.3]; names = ['Claude', 'Remotion', 'Higgsfield']
    for i in range(3):
        ps = prog(t, 11.85 + i * .1, 12.35 + i * .1)
        if ps > 0:
            Sl = Image.new('RGBA', (300, 300), (0, 0, 0, 0)); dashed_rr(Sl, (25, 25, 275, 275), 58, (150, 200, 30), 4, 16, 12, int(255 * (1 - prog(t, pops[i], pops[i] + .3))))
            place(img, Sl, xs[i], 1020, E('back_out', ps), clamp(ps * 3))
        pc = prog(t, chips[i] - .1, chips[i] + .45)
        if pc > 0:
            Cp = Image.new('RGBA', (110, 110), (0, 0, 0, 0)); circle(Cp, 55, 55, 44, INK); draw_txt(Cp, (55, 58), str(i + 1), 'Outfit-Bold', 48, LIME, 'mm')
            place(img, Cp, xs[i], 1215, E('back_out_x', pc), clamp(pc * 4))
        pp = prog(t, pops[i], pops[i] + .75)
        if pp > 0:
            tile, pd = _lt(['claude', 'remotion', 'higgs'][i], 250)
            place(img, tile, xs[i], 1020 + 140 * (1 - E('expo_out', pp)), max(.05, E('back_out_x', pp)), clamp(pp * 4), blur=16 * (1 - E('expo_out', pp)))
            click_ring(img, xs[i], 1020, prog(t, pops[i] + .03, pops[i] + .65), LIME_D)
            slide_text(img, names[i], 'Outfit-Medium', 54, INK, xs[i], 1330, t, pops[i] + .22, .5, hl=MARK, hlt=.3)
    return zoom_cam(img, t, [(8.9, 1.0), (9.6, 1.0, 'cine'), (12.0, 1.045, 'cine'), (16.7, 1.06)])

# ================================================================== S3b: ESTILOS DE EDICION
@functools.lru_cache(None)
def _grad(w, h, a0, a1):
    g = np.linspace(a0, a1, h, dtype=np.float32)[:, None] * np.ones((1, w), np.float32); return Image.fromarray(g.astype(np.uint8), 'L')

def styled_tile(style, fi, t, w=204, h=362):
    fr = Image.fromarray(crudo(fi)).resize((w, h), Image.BICUBIC).convert('RGBA'); d = ImageDraw.Draw(fr, 'RGBA'); bob = 4 * math.sin(t * 5 + style)
    if style == 0:
        g = Image.new('RGBA', (w, int(h * .4)), (0, 0, 0, 255)); g.putalpha(_grad(w, g.height, 170, 0)); fr.alpha_composite(g)
        rrect(fr, (int(w * .17), int(h * .08), int(w * .83), int(h * .08) + 14), 7, WHITE); rrect(fr, (int(w * .29), int(h * .08) + 26, int(w * .71), int(h * .08) + 40), 7, CORAL)
        fr.alpha_composite(R.prop('pill', 110) if False else prop2('pill', 110, 'coral'), (int(w * .5 - 77 + bob), int(h * .8 - 40)))
        fr.alpha_composite(prop2('check', 40, 'coral'), (int(w * .8 - 20), int(h * .66 - 20 + bob)))
    elif style == 1:
        ov = Image.new('RGBA', (w, h), (10, 14, 40, 150)); fr.alpha_composite(ov)
        gl = Image.new('RGBA', (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl); a = int(190 + 60 * math.sin(t * 6))
        gd.rounded_rectangle((7, 7, w - 8, h - 8), 22, outline=(96, 140, 255, a), width=5); gl2 = gl.filter(ImageFilter.GaussianBlur(5)); fr.alpha_composite(gl2); fr.alpha_composite(gl)
        gd2 = ImageDraw.Draw(fr); gd2.line([(int(w * .2), int(h * .93)), (int(w * .8), int(h * .93))], fill=(240, 69, 47, 255), width=5)
        rrect(fr, (int(w * .22), int(h * .08), int(w * .78), int(h * .08) + 12), 6, (230, 236, 255))
    elif style == 2:
        L = int(w * .22)
        for (x0, y0, sx, sy) in ((12, 12, 1, 1), (w - 12, 12, -1, 1), (12, h - 12, 1, -1), (w - 12, h - 12, -1, -1)):
            d.line([(x0, y0 + sy * L), (x0, y0), (x0 + sx * L, y0)], fill=LIME + (255,), width=6, joint='curve')
        for i in range(5):
            for j in range(5):
                r_ = max(0, 4.5 - (i + j) * .55)
                if r_ > .6: d.ellipse((w - 24 - i * 14 - r_, 24 + j * 14 - r_, w - 24 - i * 14 + r_, 24 + j * 14 + r_), fill=LIME + (255,))
        pl = Image.new('RGBA', (110, 44), (0, 0, 0, 0)); rrect(pl, (0, 0, 110, 44), 22, LIME); fr.alpha_composite(pl, (int(w * .5 - 55 + bob), int(h * .84)))
    else:
        fr = Image.new('RGBA', (w, h), CREAM + (255,))
        rrect(fr, (int(w * .1), int(h * .07), int(w * .8), int(h * .07) + 22), 11, CORAL); rrect(fr, (int(w * .1), int(h * .07) + 36, int(w * .56), int(h * .07) + 50), 7, (214, 206, 196))
        face = Image.fromarray(crudo(fi)).crop((10, 120, 260, 420)).resize((int(w * .84), int(h * .58)), Image.BICUBIC)
        fr.alpha_composite(round_img(face, 14), (int(w * .08), int(h * .34))); fr.alpha_composite(prop2('pill', 96, 'coral'), (int(w * .52), int(h * .27 + bob)))
    return round_img(fr, 22)

def sc_styles(t):
    img = scene_bg('coral', t, 15.0)
    done_t = [17.5, 18.4, 19.3, 20.2]; idx = 0 if t < 20.3 else (1 if t < 20.4 else (2 if t < 20.5 else 3))
    CWs, CHs = 960, 640
    c, ox, oy = chat_card(CWs, CHs)
    st = [16.9, 17.8, 18.7, 19.6]
    for k in range(4):
        x = ox + 36 + 102 + k * 228; y = oy + 130 + 181
        p = prog(t, st[k], st[k] + .5)
        if p <= 0: continue
        e = E('expo_out', p); bar = E('easy', prog(t, st[k] + .2, st[k] + .75)); fin = prog(t, st[k] + .75, st[k] + .95)
        tl = styled_tile(k, fidx(t) + k * 70, t)
        if fin < 1:
            sk = Image.new('RGBA', (204, 362), (0, 0, 0, 0)); rrect(sk, (0, 0, 204, 362), 22, (238, 233, 226))
            hx = ((t * 600 + k * 90) % 420) - 100; sd = ImageDraw.Draw(sk); sd.polygon([(hx, 0), (hx + 70, 0), (hx + 20, 362), (hx - 50, 362)], fill=(255, 255, 255, 140))
            sk.putalpha(ImageChops.multiply(sk.getchannel('A'), rmask(204, 362, 22)))
            sk.alpha_composite(asterisk(46), (79, 120)); rrect(sk, (24, 300, 24 + 156, 314), 7, (255, 255, 255, 255)); rrect(sk, (24, 300, 24 + max(14, int(156 * bar)), 314), 7, CORAL)
            body = Image.alpha_composite(sk, Image.new('RGBA', sk.size, (0, 0, 0, 0)))
            if fin > 0: tl2 = tl.copy(); tl2.putalpha(tl.getchannel('A').point(lambda v: int(v * fin))); body.alpha_composite(tl2)
        else: body = tl
        sc = (.9 + .1 * e) * (1 + .04 * math.sin(math.pi * prog(t, st[k] + .75, st[k] + 1.05)))
        place(c, body, x, y + 260 * (1 - e), sc, clamp(p * 3), blur=18 * (1 - E('easy_in', p)))
        if fin > 0: R.check_badge(c, x + 92, y - 170, 22, prog(t, st[k] + .8, st[k] + 1.2))
        # ping de remarcado cuando dice "animaciones"
        pp = prog(t, 20.3 + k * .1, 20.9 + k * .1)
        if 0 < pp < 1:
            ring = Image.new('RGBA', (260, 420), (0, 0, 0, 0)); ImageDraw.Draw(ring).rounded_rectangle((6, 6, 254, 414), 30, outline=CORAL + (int(255 * (1 - pp)),), width=5)
            place(c, ring, x, y, 1 + .12 * E('expo_out', pp), 1.0)
    R.card_in(img, c, 540, 960, t, 15.1, rise=300)
    return zoom_cam(img, t, [(15.0, 1.0), (15.8, 1.0, 'cine'), (20.5, 1.05)])

# ================================================================== S3c: PROMPT -> ENVIAR -> CARGA
PROMPT = 'Editá mi video con el estilo de la referencia.'
def sc_prompt(t):
    img = scene_bg('coral', t, 20.85)
    idx = 1 if t < 22.52 else 2
    c, ox, oy = chat_card(CW2, CH2); w = CW2
    zx0, zy0, zx1, zy1 = ox + 40, oy + 130, ox + w - 40, oy + 130 + 470
    pz = prog(t, 21.0, 21.5); zc = 1 - E('expo_in', prog(t, 22.52, 22.82))
    Z = Image.new('RGBA', c.size, (0, 0, 0, 0)); dashed_rr(Z, (zx0, zy0, zx1, zy1), 34, (214, 206, 196), 3, 16, 12, int(255 * zc), progress=E('expo_out', pz))
    c.alpha_composite(Z)
    load = prog(t, 22.52, 22.9)
    for k, (cxk, lab) in enumerate(((ox + w / 2 - 160, 'raw_footage.mp4'), (ox + w / 2 + 160, 'referencia.mp4'))):
        ta = 21.1 + k * .22; p = prog(t, ta, ta + .6)
        if p <= 0: continue
        e = E('expo_out', p); bar = E('easy', prog(t, ta + .15, ta + .55))
        if k == 0: tl = vid(fidx(t), 250, 340, 24)
        else:
            tl = Image.new('RGBA', (250, 340), (0, 0, 0, 0)); g = R.vgrad(250, 340, (255, 110, 82), (226, 50, 30)) if hasattr(R, 'vgrad') else None
            from engine import vgrad as _vg
            gg = _vg(250, 340, (255, 110, 82), (226, 50, 30)).convert('RGBA'); gg = round_img(gg, 24); tl.alpha_composite(gg)
            rrect(tl, (36, 96, 214, 124), 14, (40, 22, 20)); rrect(tl, (36, 138, 170, 156), 9, (255, 214, 204)); rrect(tl, (36, 190, 150, 230), 20, WHITE)
        sx = (1 - .55 * load * (1 if load < 1 else 1)); mv = E('expo_inout', load)
        px = lerp(cxk, ox + w / 2, mv); py = lerp(zy0 + 235 + 140 * (1 - e), zy0 + 235, 1.0)
        place(c, tl, px, py, max(.05, (.9 + .1 * e) * (1 - .55 * mv)), clamp(p * 3) * (1 - E('expo_in', prog(t, 22.7, 22.9))), blur=16 * (1 - e))
        if load < .01:
            R.check_badge(c, int(cxk + 118), int(zy0 + 235 - 160), 24, prog(t, ta + .5, ta + .9))
            if bar < 1: rrect(c, (int(cxk - 90), int(zy0 + 235 + 188), int(cxk + 90), int(zy0 + 235 + 200)), 6, LINE); rrect(c, (int(cxk - 90), int(zy0 + 235 + 188), int(cxk - 90 + max(12, 180 * bar)), int(zy0 + 235 + 200)), 6, CORAL)
            else: draw_txt(c, (cxk, zy0 + 235 + 205), lab, 'Jakarta-Medium', 23, GREY, 'mm')
    # carga: anillo con asterisco
    if load > 0:
        a = E('expo_out', load); cxr, cyr = ox + w / 2, zy0 + 235
        Rg = Image.new('RGBA', (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(Rg); d.ellipse((30, 30, 270, 270), outline=LINE + (255,), width=18)
        ang = (t - 22.5) * 520; d.arc((30, 30, 270, 270), ang, ang + 110, fill=CORAL + (255,), width=18)
        place(c, Rg, cxr, cyr, a, a); place(c, asterisk(84).rotate(-(t - 22.5) * 140, resample=Image.BICUBIC), cxr, cyr, a, a)
    # input
    iy = oy + CH2 - 190; Lb = Image.new('RGBA', (w - 80, 140), (0, 0, 0, 0)); rrect(Lb, (0, 0, w - 80, 140), 46, ROW)
    n = int(len(PROMPT) * prog(t, 21.6, 22.35)); shown = PROMPT[:n]
    if t < 22.5 and shown: draw_txt(Lb, (36, 70), shown, 'Jakarta-Medium', 31, INK, 'lm')
    elif t < 22.5: draw_txt(Lb, (36, 70), 'Escribí tu prompt...', 'Jakarta-Medium', 30, (186, 180, 172), 'lm')
    press = prog(t, 22.4, 22.48) * (1 - prog(t, 22.48, 22.62)); circle(Lb, w - 80 - 70, 70, int(42 * (1 - .12 * press)), CORAL)
    dd = ImageDraw.Draw(Lb); bx, by = w - 150, 70
    dd.line([(bx, by + 14), (bx, by - 14)], fill=WHITE + (255,), width=6); dd.line([(bx - 13, by - 2), (bx, by - 15), (bx + 13, by - 2)], fill=WHITE + (255,), width=6, joint='curve')
    paste(c, Lb, (ox + 40, iy), 1.0)
    R.card_in(img, c, 540, 1010, t, 20.85, rise=300)
    cx0 = 540 - c.width / 2 + ox + w - 110; cy0 = 1010 - c.height / 2 + iy + 70
    ca = prog(t, 21.85, 22.1) * (1 - prog(t, 22.62, 22.8))
    if ca > 0:
        x, y = cursor_path(t, 21.9, 22.4, (900, 1650), (cx0 + 8, cy0 + 8), (850, cy0 + 380))
        draw_cursor(img, x, y, scale=lerp(.55, 1.0, prog(t, 21.9, 22.35)), alpha=ca, press=press)
    click_ring(img, int(cx0), int(cy0), prog(t, 22.4, 22.95))
    pixel_ring(img, int(cx0), int(cy0), prog(t, 22.42, 22.95), r0=60, r1=260, cell=14, color=CORAL, seed=4, count=180)
    return zoom_cam(img, t, [(20.85, 1.0), (21.4, 1.0, 'cine'), (23.4, 1.06)])

# ================================================================== S4: COMENTA + CARGA (rojo oscuro)
def sc_cta(t):
    img = scene_bg('red', t, 26.5)
    cx, cy = 540, 960; r = 300
    pa = E('expo_out', prog(t, 26.65, 27.15)); prg = E('easy', prog(t, 26.9, 29.0)); done = prog(t, 29.0, 29.35)
    if pa > 0:
        Rg = Image.new('RGBA', (r * 2 + 160, r * 2 + 160), (0, 0, 0, 0)); d = ImageDraw.Draw(Rg); o = 80
        d.ellipse((o, o, o + 2 * r, o + 2 * r), outline=(96, 34, 26, 255), width=30)
        if prg > .005:
            g = Image.new('RGBA', Rg.size, (255, 84, 56, 0)); gd = ImageDraw.Draw(g); gd.arc((o, o, o + 2 * r, o + 2 * r), -90, -90 + 360 * prg, fill=(255, 84, 56, 255), width=30)
            glw = g.filter(ImageFilter.GaussianBlur(16)); Rg.alpha_composite(glw); Rg.alpha_composite(g)
            ang = math.radians(-90 + 360 * prg); ex, ey = o + r + r * math.cos(ang), o + r + r * math.sin(ang)
            d.ellipse((ex - 21, ey - 21, ex + 21, ey + 21), fill=(255, 150, 120, 255))
        place(img, Rg, cx, cy, .8 + .2 * pa, pa, blur=12 * (1 - pa))
    glow_disc(img, cx, cy, 320, (255, 70, 46), .30 * pa * (1 + .12 * math.sin(t * 4)))
    slide_text(img, 'editor', 'Outfit-Bold', 150, RED_T, cx, cy, t, 26.85, .6)
    if done > 0:
        R.check_badge(img, cx + 190, cy - 190, 62, done); glow_disc(img, cx, cy, 300, (255, 90, 60), (1 - done) * .5)
        pixel_ring(img, cx, cy, done, r0=250, r1=520, cell=18, color=(255, 110, 80), seed=21, count=300)
    return zoom_cam(img, t, [(26.3, 1.0), (27.0, 1.0, 'cine'), (29.7, 1.06)])


# ================================================================== FONDOS DEL USUARIO + OBJETOS FLOTANDO
BGD = os.path.join(WORK, 'bgs')

@functools.lru_cache(None)
def bg_clean(name): return Image.open(os.path.join(BGD, name + '_clean.png')).convert('RGBA')

@functools.lru_cache(None)
def sprite_set(name):
    import json
    meta = json.load(open(os.path.join(BGD, name + '_meta.json'))); out = []
    for k, m in enumerate(meta):
        sp = Image.open(os.path.join(BGD, f"{name}_{m['name']}.png")).convert('RGBA'); a = np.asarray(sp.getchannel('A'))
        edge = dict(l=a[:, :2].max() > 40, r=a[:, -2:].max() > 40, t=a[:2, :].max() > 40, b=a[-2:, :].max() > 40)
        out.append(dict(m=m, sp=sp, edge=edge, ph=(k * .37 + .11) % 1.0))
    return out

_BLUR = {}
def blurred(sp, key, r):
    r = max(0, int(round(r / 2.0)) * 2)
    if r == 0: return sp
    k = (key, r)
    if k not in _BLUR:
        P = Image.new('RGBA', (sp.width + r * 6, sp.height + r * 6), (0, 0, 0, 0)); P.alpha_composite(sp, (r * 3, r * 3)); _BLUR[k] = P.filter(ImageFilter.GaussianBlur(r))
    return _BLUR[k]

def scene_bg(name, t, t0, gain=1.0, enter=True):
    img = bg_clean(name).copy()
    for i, o in enumerate(sprite_set(name)):
        m, sp, ed, ph = o['m'], o['sp'], o['edge'], o['ph']; typ = m['type']
        ta = t0 + .1 + .13 * i; p = prog(t, ta, ta + 1.05) if enter else 1.0
        if p <= 0: continue
        e = E('expo_out', p); cx, cy = m['cx'], m['cy']
        cropped = ed['l'] or ed['r'] or ed['t'] or ed['b']
        ax = 0 if ed['l'] else (W if ed['r'] else cx); ay = 0 if ed['t'] else (H if ed['b'] else cy)
        sec = 2 * math.pi
        if cropped:
            s = 1.0 + .04 * (.5 + .5 * math.sin(sec * (t * .085 + ph))) * gain
            px = ax + (cx - ax) * s; py = ay + (cy - ay) * s
            if not (ed['l'] or ed['r']): px += 14 * gain * math.sin(sec * (t * .07 + ph))
            if not (ed['t'] or ed['b']): py += 14 * gain * math.sin(sec * (t * .07 + ph))
            vx, vy = (ax - cx), (ay - cy); n = math.hypot(vx, vy) or 1
            px -= vx / n * 360 * (1 - e) * 0 + (-vx / n) * 0; ox, oy = (vx / n) * 380 * (1 - e), (vy / n) * 380 * (1 - e)
            px += ox; py += oy; rot = 0.0; sc = s
        else:
            dy = (13 if typ == 'check' else 11) * gain * math.sin(sec * (t * .11 + ph)); dx = 7 * gain * math.cos(sec * (t * .08 + ph * 1.6))
            vx, vy = cx - 540, cy - 960; n = math.hypot(vx, vy) or 1
            px = cx + dx + vx / n * 300 * (1 - e); py = cy + dy + vy / n * 300 * (1 - e)
            if typ == 'spark': rot = t * 16 + ph * 90; sc = (1 + .12 * math.sin(sec * (t * .22 + ph))) * (.35 + .65 * E('back_out_x', p))
            else: rot = 4 * gain * math.sin(sec * (t * .07 + ph * 1.3)); sc = .35 + .65 * E('back_out_x', p)
        bl = 12 * (1 - e)
        spr = blurred(sp, (name, m['name']), bl) if bl > 1 else sp
        place(img, spr, px, py, max(.05, sc), clamp(p * 3.5), blur=0, rot=rot)
    return img

# ================================================================== S3a v3: TRES HERRAMIENTAS (tiempos de la voz)
# voz: "tres herramientas" 9.6-10.5 | "Numero 1" 10.66-11.35 | "Claude" 11.42-11.72 | "Numero 2" 11.82-12.36
#      "Remotion" 12.56-13.23 | "y Numero 3" 13.34-14.05 | "Higgsfield" 14.28-14.71 | "que al conectarlas" 14.97
T_QPOP = [9.72, 9.98, 10.24]; T_MERGE0, T_MERGE1 = 10.62, 11.14; T_CLAUDE = 11.14
T_C_LEFT = (11.95, 12.5); T_REMO_UP = (12.38, 12.95); T_R_RIGHT = (13.4, 13.95); T_HIGGS_UP = (14.0, 14.55)
XL, XC, XR, YT = 195, 540, 885, 880

@functools.lru_cache(None)
def qtile():
    t_, pad = rounded_tile(250, 250, 64, (255, 255, 255, 255), outline=(228, 236, 214, 255))
    d = ImageDraw.Draw(t_); d.text((pad + 125, pad + 130), '?', font=F('Outfit-Bold', 170), fill=LIME_D + (255,), anchor='mm')
    return t_

def lbl(img, txt, cx, cy, t, ta):
    slide_text(img, txt, 'Outfit-Medium', 62, INK, cx, cy, t, ta, .55, hl=MARK, hlt=.28)

def sc_tools(t):
    t0 = 8.93
    img = scene_bg('lime', t, t0, gain=1.2)
    fade = 1 - E('expo_in', prog(t, 14.78, 15.1))
    # titulo con la voz "a partir solamente de tres herramientas"
    # --- tres cuadraditos con ? : plim, plim, plim
    xs = [XL, XC, XR]
    if t < T_CLAUDE + .25:
        merge = E('expo_in', prog(t, T_MERGE0, T_MERGE1))
        for i in range(3):
            p = prog(t, T_QPOP[i], T_QPOP[i] + .62)
            if p <= 0: continue
            x = lerp(xs[i], XC, merge); s = E('back_out_x', p) * (1 - .12 * merge)
            y = YT + 190 * (1 - E('expo_out', p)); a = clamp(p * 4) * (1 - prog(t, T_CLAUDE, T_CLAUDE + .18))
            place(img, qtile(), x, y, max(.05, s), a, blur=14 * (1 - E('expo_out', p)) + 10 * merge, rot=(-5 + 5 * i) * (1 - merge))
            pr = prog(t, T_QPOP[i] + .03, T_QPOP[i] + .6)
            if 0 < pr < 1: click_ring(img, xs[i], YT, pr, LIME_D)
    # impacto de la union y nacimiento de Claude
    pm = prog(t, T_CLAUDE, T_CLAUDE + .7)
    if pm > 0:
        glow_disc(img, XC, YT, 330, (200, 244, 80), (1 - pm) * .5)
        pixel_ring(img, XC, YT, pm, r0=110, r1=370, cell=13, color=(168, 220, 40), seed=31, count=150)
    # --- carrusel: Claude izq, Remotion arriba->der, Higgsfield arriba al centro
    xc = Track([(T_C_LEFT[0], XC), (T_C_LEFT[1], XL, 'expo_inout')]) if True else None
    claude_x = Track([(T_C_LEFT[0], XC, 'expo_inout'), (T_C_LEFT[1], XL)])(t)
    remo_x = Track([(T_R_RIGHT[0], XC, 'expo_inout'), (T_R_RIGHT[1], XR)])(t)
    items = [('claude', 'Claude', T_CLAUDE, claude_x, None, 11.5), ('remotion', 'Remotion', T_REMO_UP[0], remo_x, T_REMO_UP, 12.72), ('higgs', 'Higgsfield', T_HIGGS_UP[0], XC, T_HIGGS_UP, 14.38)]
    for kind, name, ta, x, up, tl in items:
        if t < ta: continue
        tile, pd = _lt(kind, 250)
        if up is None:                                    # nace del centro
            p = prog(t, ta, ta + .75); s = max(.05, E('back_out_x', p)); y = YT; a = clamp(p * 4); bl = 12 * (1 - E('expo_out', p))
        else:                                             # slide up desde abajo
            p = prog(t, up[0], up[1]); e = E('expo_out', p); s = .92 + .08 * e; y = YT + 430 * (1 - e); a = clamp(p * 3); bl = 14 * (1 - e)
        place(img, tile, x, y, s, a * fade, blur=bl)
        lp = prog(t, tl, tl + .6)
        if lp > 0 and fade > 0.01:
            lbl(img, name, x, YT + 190, t, tl)
    # chasquido cuando Remotion y Higgsfield aterrizan
    for ta in (T_REMO_UP[1] - .12, T_HIGGS_UP[1] - .12):
        pr = prog(t, ta, ta + .55)
        if 0 < pr < 1: click_ring(img, XC, YT, pr, LIME_D)
    return zoom_cam(img, t, [(8.9, 1.0), (9.5, 1.0, 'cine'), (11.2, 1.035, 'cine'), (15.2, 1.05)])


# ================================================================== montaje
# (nombre, f0, f1, entrada(centro, dur), salida(centro, dur))
SEGS = [('grave', 25, 81, ((540, 1000), .5), ((540, 1100), .38), sc_grave),
        ('upload', 119, 179, ((540, 1000), .42), ((700, 900), .42), sc_upload),
        ('tools', 214, 561, ((540, 900), .5), ((400, 1100), .4), None),
        ('cta', 632, 711, ((540, 960), .45), ((540, 1000), .4), sc_cta)]
T34 = (15.0, .55); T23 = (20.85, .6)

def s3(t):
    if abs(t - T34[0]) < T34[1] / 2:
        p = (t - (T34[0] - T34[1] / 2)) / T34[1]; return R.blob_transition(sc_tools(t).convert('RGBA'), sc_styles(t).convert('RGBA'), p, (700, 1000), (400, 1050), 3)
    if abs(t - T23[0]) < T23[1] / 2:
        p = (t - (T23[0] - T23[1] / 2)) / T23[1]; return R.blob_transition(sc_styles(t).convert('RGBA'), sc_prompt(t).convert('RGBA'), p, (400, 1000), (700, 1000), 5)
    if t < T34[0]: return sc_tools(t)
    if t < T23[0]: return sc_styles(t)
    return sc_prompt(t)

REVEAL = .36                      # segundos de facecam sobre los que la mancha termina de abrirse

def render_screen(i):
    t = i / FPS
    for name, f0, f1, ent, ext, fn in SEGS:
        if f0 <= i < f1:
            t0, t1 = f0 / FPS, f1 / FPS; fn_ = fn or s3
            if t < t0 + ent[1]:
                q = (t - t0) / ent[1]; return R.blob_transition(None, fn_(t).convert('RGBA'), .5 + .5 * clamp(q), (500, 900), ent[0], 7).convert('RGB')
            if t > t1 - ext[1] - 1 / FPS:
                q = (t - (t1 - ext[1] - 1 / FPS)) / ext[1]; return R.blob_transition(fn_(t).convert('RGBA'), None, .5 * clamp(q), ext[0], (500, 900), 9).convert('RGB')
            return fn_(t).convert('RGB')
    return None

def render_frame(i, foot):
    r = render_screen(i)
    if r is not None: return np.array(r)
    t = i / FPS
    for name, f0, f1, ent, ext, fn in SEGS:
        t1 = f1 / FPS
        if t1 <= t < t1 + REVEAL:                         # la mancha sigue y destapa a la persona
            p = .5 + .5 * clamp((t - t1) / REVEAL)
            return np.array(R.blob_transition(None, Image.fromarray(foot).convert('RGBA'), p, ext[0], (500, 900), 9).convert('RGB'))
    return foot

def _frame_at(i):
    buf = subprocess.run(['ffmpeg', '-v', 'error', '-i', SRC, '-vf', f'select=eq(n\\,{i})', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(buf, np.uint8).reshape(H, W, 3)

def stills(times, out):
    tiles = []
    for t in times:
        i = int(round(t * FPS)); tiles.append(Image.fromarray(render_frame(i, _frame_at(i) if render_screen(i) is None else None)).resize((324, 576), Image.LANCZOS))
    cols = 6; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 324, rows * 576), (40, 40, 40))
    for k, im in enumerate(tiles): sheet.paste(im, ((k % cols) * 324, (k // cols) * 576))
    sheet.save(out, quality=88)

def render_range(a, b, out):
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{a / FPS:.5f}', '-i', SRC, '-vf', f'fps={FPS},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', f'{FPS}', '-i', '-',
                            '-c:v', 'libx264', '-crf', '13', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    n = W * H * 3
    for i in range(a, b):
        buf = dec.stdout.read(n)
        if len(buf) < n: break
        enc.stdin.write(render_frame(i, np.frombuffer(buf, np.uint8).reshape(H, W, 3)).tobytes())
    enc.stdin.close(); enc.wait(); dec.kill()

def mux(parts_dir, out):
    parts = sorted(glob.glob(os.path.join(parts_dir, 'p*.mp4')), key=lambda p: int(os.path.basename(p)[1:-4]))
    lst = os.path.join(parts_dir, 'l.txt'); open(lst, 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    tmp = os.path.join(parts_dir, 'video.mp4'); subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', tmp], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', SRC, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'stills': stills([float(x) for x in sys.argv[3].split(',')], sys.argv[2])
    elif m == 'part': render_range(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    elif m == 'mux': mux(sys.argv[2], sys.argv[3])
