import math, random, functools, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1080, 1920
FPS = 24000 / 1001

LIME = (210, 245, 42)
LIME2 = (226, 255, 80)
PINK = (233, 21, 113)
PINK2 = (255, 70, 150)
INK = (8, 8, 10)
PAPER = (251, 250, 252)
GRID = (205, 205, 210)
GRIDD = (42, 42, 48)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FD = os.path.join(ROOT, 'assets', 'fonts') + '/'
LG = os.path.join(ROOT, 'assets', 'logos') + '/'

# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else (1.0 if t >= a else 0.0)
def eo3(p): return 1 - (1 - p) ** 3
def eo4(p): return 1 - (1 - p) ** 4
def eio(p): return 3 * p * p - 2 * p ** 3
def eio4(p): return 8 * p ** 4 if p < .5 else 1 - 8 * (1 - p) ** 4
def eback(p, s=1.5):
    p = p - 1
    return p * p * ((s + 1) * p + s) + 1
def lerp(a, b, p): return a + (b - a) * p
def rnd(*k):
    return random.Random(hash(k) & 0xffffffff).random()

# ---------------------------------------------------------------- fonts
def HEAD(size): return font('Archivo', size, 850, 78)      # titulares bold condensados
def HEADW(size): return font('Archivo', size, 800, 100)
def SG(size, w=700): return font('SpaceGrotesk', size, w)
def UI(size, w=500): return font('Inter', size, w)

# ---------------------------------------------------------------- canvas utils
def new_canvas(color):
    return Image.new('RGBA', (W, H), color + (255,))

def paste(dst, src, xy, alpha=1.0):
    """pega RGBA src sobre dst (RGBA) en xy (esquina sup izq), recortando."""
    if alpha < 1.0:
        a = src.getchannel('A').point(lambda v: int(v * alpha))
        src = src.copy(); src.putalpha(a)
    x, y = int(xy[0]), int(xy[1])
    sx0 = max(0, -x); sy0 = max(0, -y)
    sx1 = min(src.width, dst.width - x); sy1 = min(src.height, dst.height - y)
    if sx1 <= sx0 or sy1 <= sy0: return
    dst.alpha_composite(src, (x + sx0, y + sy0), (sx0, sy0, sx1, sy1))

def ss_layer(w, h, scale=2):
    return Image.new('RGBA', (w * scale, h * scale), (0, 0, 0, 0))

def down(img, scale=2):
    return img.resize((img.width // scale, img.height // scale), Image.LANCZOS)

def glow(layer, radius, strength=1.0):
    g = layer.filter(ImageFilter.GaussianBlur(radius))
    if strength != 1.0:
        a = g.getchannel('A').point(lambda v: min(255, int(v * strength)))
        g.putalpha(a)
    return g

def rr(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)

def vgrad(w, h, c0, c1):
    t = np.linspace(0, 1, h)[:, None, None]
    a = np.array(c0)[None, None, :] * (1 - t) + np.array(c1)[None, None, :] * t
    a = np.repeat(a, w, axis=1)
    return Image.fromarray(a.astype(np.uint8), 'RGB')

def hgrad(w, h, c0, c1):
    t = np.linspace(0, 1, w)[None, :, None]
    a = np.array(c0)[None, None, :] * (1 - t) + np.array(c1)[None, None, :] * t
    a = np.repeat(a, h, axis=0)
    return Image.fromarray(a.astype(np.uint8), 'RGB')

# ---------------------------------------------------------------- text
def text_w(s, f):
    return f.getlength(s)

def draw_text(img, xy, s, f, fill, anchor='la', track=0):
    d = ImageDraw.Draw(img)
    if track == 0:
        d.text(xy, s, font=f, fill=fill, anchor=anchor)
        return
    x, y = xy
    total = sum(f.getlength(c) + track for c in s) - track
    if anchor[0] == 'm': x -= total / 2
    elif anchor[0] == 'r': x -= total
    for c in s:
        d.text((x, y), c, font=f, fill=fill, anchor='l' + anchor[1])
        x += f.getlength(c) + track

GLITCH_CH = '#@%&$/\\<>[]{}=+*?!01'

def typewriter(img, xy, s, f, base, p, active=(PINK, LIME), anchor='l', glitch=True, seed=0, tail=3):
    """escribe s letra a letra segun p (0..1). Las ultimas `tail` letras en color activo + glitch."""
    n = len(s); k = p * n
    full = int(k)
    shown = s[:full]
    widths = [f.getlength(c) for c in s]
    total = sum(widths)
    x = xy[0]
    if anchor == 'm': x -= total / 2
    elif anchor == 'r': x -= total
    d = ImageDraw.Draw(img)
    for i, c in enumerate(s):
        if i > full: break
        col = base
        ch = c
        age = full - i
        if i == full:
            if (k - full) < .15 and p < 1: break
        if p < 1 and age < tail:
            col = active[(i + seed) % len(active)]
            if glitch and age == 0 and c != ' ':
                ch = random.Random(i * 7 + seed + int(k * 5)).choice(GLITCH_CH)
        d.text((x, xy[1]), ch, font=f, fill=col, anchor='la')
        x += widths[i]
    return total

# ---------------------------------------------------------------- backgrounds
@functools.lru_cache(None)
def halftone_block(w, h, c, direction, seed=0):
    """bloque punteado degradado (estilo referencias)."""
    cell = 7
    cw, ch = w // cell + 1, h // cell + 1
    gx = np.linspace(0, 1, cw)[None, :]
    gy = np.linspace(0, 1, ch)[:, None]
    if direction == 'tl': g = 1 - (gx * .6 + gy * .8)
    elif direction == 'br': g = (gx * .6 + gy * .8) - .2
    elif direction == 'tr': g = gx * .8 + (1 - gy) * .6 - .3
    elif direction == 'bl': g = (1 - gx) * .8 + gy * .6 - .3
    elif direction == 'r': g = gx
    elif direction == 'l': g = 1 - gx
    elif direction == 'b': g = gy
    else: g = 1 - gy
    g = np.clip(g, 0, 1)
    rng = np.random.RandomState(seed)
    g = np.clip(g + (rng.rand(ch, cw) - .5) * .25, 0, 1)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for j in range(ch):
        for i in range(cw):
            v = g[j, i]
            if v < .08: continue
            r = cell * .5 * math.sqrt(v)
            cx, cy = i * cell + cell / 2, j * cell + cell / 2
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c + (int(255 * min(1, v * 1.2)),))
    return im

@functools.lru_cache(None)
def grid_bg(dark, variant=0):
    base = INK if dark else PAPER
    im = new_canvas(base)
    d = ImageDraw.Draw(im)
    lc = GRIDD if dark else GRID
    xs = [90, 990] if variant == 0 else [90, 540, 990]
    ys = [230, 1690] if variant == 0 else [230, 960, 1690]
    for x in xs: d.line((x, 0, x, H), fill=lc, width=2)
    for y in ys: d.line((0, y, W, y), fill=lc, width=2)
    cc = (230, 230, 235) if dark else (20, 20, 24)
    for x in xs:
        for y in ys:
            d.line((x - 14, y, x + 14, y), fill=cc, width=3)
            d.line((x, y - 14, x, y + 14), fill=cc, width=3)
    # binarios chiquitos arriba a la derecha + codigo abajo a la izquierda
    f = UI(15, 400)
    tc = (90, 90, 96) if dark else (170, 170, 176)
    for r in range(8):
        s = ''.join(random.Random(r + variant * 11).choice(['0', '1', ' ', '0', '1']) for _ in range(14))
        d.text((860, 40 + r * 22), ' '.join(s), font=f, fill=tc)
    code = ['const edit = await ai()', 'POST /v1/render', 'seed = 4281', 'npm i remotion', '  fps: 24, w: 1080', '  scenes: [ ... ]', '}']
    for r, s in enumerate(code):
        d.text((110, 1730 + r * 22), s, font=f, fill=tc)
    # bloques punteados en esquinas
    c1 = LIME if True else PINK
    paste(im, halftone_block(220, 260, c1, 'br', variant + 1), (0, 0), 0)
    paste(im, halftone_block(300, 300, PINK, 'tr', variant + 2), (W - 300, 1620 if variant == 0 else 0), .0)
    return im

def bg_scene(dark, variant=0, corner_mix=0.0):
    im = grid_bg(dark, variant).copy()
    if not dark:
        paste(im, halftone_block(260, 300, LIME, 'tl', 3), (0, H - 300 if variant else 0), .85)
        paste(im, halftone_block(240, 260, PINK, 'br', 5), (W - 240, 0 if variant == 0 else H - 260), .8)
    else:
        paste(im, halftone_block(260, 300, LIME, 'tl', 3), (0, H - 300), .55)
        paste(im, halftone_block(240, 260, PINK, 'br', 5), (W - 240, 0), .55)
    return im

# ---------------------------------------------------------------- shapes
def pill(w, h, c0, c1, text=None, f=None, tcol=INK, scale=2, outline=None):
    L = ss_layer(w, h, scale)
    g = vgrad(w * scale, h * scale, c0, c1).convert('RGBA')
    m = Image.new('L', L.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, L.width - 1, L.height - 1), (h * scale) // 2, fill=255)
    L.paste(g, (0, 0), m)
    if text and f:
        ImageDraw.Draw(L).text((L.width // 2, L.height // 2), text, font=F2(f, scale), fill=tcol, anchor='mm')
    return down(L, scale)

@functools.lru_cache(None)
def font(name, size, wght=None, wdth=None):
    f = ImageFont.truetype(FD + name + '.ttf', size)
    vals = []
    try:
        axes = f.get_variation_axes()
        for a in axes:
            n = a['name']
            if n == b'Weight': vals.append(wght if wght else a['default'])
            elif n == b'Width': vals.append(wdth if wdth else a['default'])
            else: vals.append(a['default'])
        f.set_variation_by_axes(vals)
    except Exception:
        pass
    f._vals = vals
    return f

@functools.lru_cache(None)
def _fs(path, size, vals):
    f = ImageFont.truetype(path, size)
    try:
        if vals: f.set_variation_by_axes(list(vals))
    except Exception:
        pass
    f._vals = list(vals)
    return f

def F2(f, k):
    """misma fuente a k veces el tamano."""
    return _fs(f.path, f.size * k, tuple(getattr(f, '_vals', ())))

def rounded_tile(w, h, r, fill, outline=None, shadow=True, scale=2):
    pad = 40 if shadow else 0
    L = ss_layer(w + pad * 2, h + pad * 2, scale)
    if shadow:
        s = ss_layer(w + pad * 2, h + pad * 2, scale)
        ImageDraw.Draw(s).rounded_rectangle((pad * scale, (pad + 10) * scale, (pad + w) * scale, (pad + h + 10) * scale), r * scale, fill=(0, 0, 0, 55))
        s = s.filter(ImageFilter.GaussianBlur(14 * scale))
        L.alpha_composite(s)
    d = ImageDraw.Draw(L)
    d.rounded_rectangle((pad * scale, pad * scale, (pad + w) * scale, (pad + h) * scale), r * scale, fill=fill, outline=outline, width=2 * scale if outline else 0)
    return down(L, scale), pad

# ---------------------------------------------------------------- cursor
@functools.lru_cache(None)
def cursor_img(size=110):
    s = 4
    L = Image.new('RGBA', (size * s, int(size * 1.25) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    k = size * s / 20.0
    pts = [(2, 1), (2, 16.5), (6.2, 12.6), (9.2, 19.6), (12.2, 18.3), (9.3, 11.6), (14.8, 11.4)]
    pts = [(x * k, y * k) for x, y in pts]
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x + 5 * s, y + 7 * s) for x, y in pts], fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(6 * s))
    L.alpha_composite(sh)
    d.polygon(pts, fill=(255, 255, 255, 255), outline=(8, 8, 10, 255), width=int(2.4 * s))
    # borde grueso negro
    d.line(pts + [pts[0]], fill=(8, 8, 10, 255), width=int(3.4 * s), joint='curve')
    d.polygon(pts, fill=(255, 255, 255, 255))
    d.line(pts + [pts[0]], fill=(8, 8, 10, 255), width=int(3.0 * s), joint='curve')
    return L.resize((size, int(size * 1.25)), Image.LANCZOS)

def draw_cursor(img, x, y, scale=1.0, alpha=1.0, press=0.0):
    c = cursor_img(110)
    sc = scale * (1 - .12 * press)
    if sc != 1.0:
        c = c.resize((max(2, int(c.width * sc)), max(2, int(c.height * sc))), Image.LANCZOS)
    paste(img, c, (x - 4, y - 3), alpha)

# ---------------------------------------------------------------- pixel effects
def pixel_cover(img, p, color, cell=72, seed=1, edge=0.0, mode='in'):
    """tapa la pantalla con cuadrados que aparecen aleatoriamente. p 0..1 cubierto."""
    cw, ch = W // cell + 1, H // cell + 1
    rng = np.random.RandomState(seed)
    th = rng.rand(ch, cw)
    # sesgo diagonal para que se sienta barrido
    gy, gx = np.mgrid[0:ch, 0:cw]
    th = np.clip(th * .55 + (gx / cw * .25 + gy / ch * .2), 0, 1)
    m = (th < p * 1.0001).astype(np.uint8) * 255
    mask = Image.fromarray(m, 'L').resize((cw * cell, ch * cell), Image.NEAREST).crop((0, 0, W, H))
    col = Image.new('RGBA', (W, H), tuple(color) + (255,))
    img.paste(col, (0, 0), mask)

def pixel_cover_multi(img, p, colors, cell=72, seed=1):
    cw, ch = W // cell + 1, H // cell + 1
    rng = np.random.RandomState(seed)
    th = rng.rand(ch, cw)
    gy, gx = np.mgrid[0:ch, 0:cw]
    th = np.clip(th * .55 + (gx / cw * .25 + gy / ch * .2), 0, 1)
    ci = rng.randint(0, len(colors), (ch, cw))
    on = th < p
    arr = np.zeros((ch, cw, 4), np.uint8)
    for k, c in enumerate(colors):
        sel = on & (ci == k)
        arr[sel] = c + (255,)
    lay = Image.fromarray(arr, 'RGBA').resize((cw * cell, ch * cell), Image.NEAREST).crop((0, 0, W, H))
    img.alpha_composite(lay)

def pixel_ring(img, cx, cy, p, r0=110, r1=330, cell=18, color=LIME, seed=3, count=420):
    """anillo de cuadrados que explota y se desvanece (click)."""
    if p <= 0 or p >= 1: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    rng = random.Random(seed)
    rad = lerp(r0, r1, eo3(p))
    fade = 1 - p
    for i in range(count):
        a = rng.random() * math.tau
        jitter = rng.random()
        r = rad * (.78 + .38 * jitter) + rng.random() * 14
        s = cell * (.4 + rng.random() * 1.1) * (1 - .3 * p)
        x = cx + math.cos(a) * r; y = cy + math.sin(a) * r
        al = int(255 * fade * (.35 + .65 * rng.random()))
        c = color if rng.random() > .12 else (255, 255, 255)
        d.rectangle((x - s / 2, y - s / 2, x + s / 2, y + s / 2), fill=c + (al,))
    g = glow(L, 10, 1.4)
    img.alpha_composite(g)
    img.alpha_composite(L)

def glitch_slices(arr, p, seed=0, amount=60):
    """desplaza franjas horizontales (glitch). arr: ndarray HxWx3."""
    if p <= 0: return arr
    rng = np.random.RandomState(seed)
    out = arr.copy()
    for _ in range(int(8 + 14 * p)):
        y = rng.randint(0, H - 20); h = rng.randint(6, 90)
        dx = int(rng.randint(-amount, amount) * p)
        out[y:y + h] = np.roll(out[y:y + h], dx, axis=1)
    return out

def chroma(arr, shift):
    if shift == 0: return arr
    out = arr.copy()
    out[..., 0] = np.roll(arr[..., 0], shift, axis=1)
    out[..., 2] = np.roll(arr[..., 2], -shift, axis=1)
    return out

# ---------------------------------------------------------------- compound UI
def chat_bar(w=860, h=190, dark=False, text='', p=1.0, send=None, font_size=46, caret=False, seed=0, tags=True):
    """barra de chat estilo referencia. Devuelve (RGBA, send_center_offset)."""
    pad = 40
    tile, pd = rounded_tile(w, h, 44, (255, 255, 255, 255) if not dark else (30, 30, 34, 255), outline=(236, 220, 228, 255) if not dark else None)
    im = tile.copy()
    d = ImageDraw.Draw(im)
    f = UI(font_size, 500)
    typewriter(im, (pd + 40, pd + 36), text, f, (20, 20, 24), p, seed=seed)
    # selector de modelo
    f2 = UI(26, 500)
    d.text((pd + 40, pd + h - 62), '+', font=UI(40, 400), fill=(120, 120, 126))
    d.ellipse((pd + w - 470, pd + h - 56, pd + w - 456, pd + h - 42), fill=PINK)
    d.text((pd + w - 440, pd + h - 62), 'AI Studio', font=f2, fill=(30, 30, 34))
    d.text((pd + w - 300, pd + h - 62), 'Ultra', font=f2, fill=PINK)
    sx = pd + w - 78; sy = pd + h - 48
    return im, (sx, sy), pd

def send_button(r=40, rot=0.0, press=0.0, glow_p=0.0, scale=3):
    R = int(r * (1 - .1 * press))
    L = ss_layer(R * 2 + 120, R * 2 + 120, scale)
    c = (L.width // 2, L.height // 2)
    if glow_p > 0:
        g = ss_layer(R * 2 + 120, R * 2 + 120, scale)
        rad = R * scale * (1 + .6 * glow_p)
        ImageDraw.Draw(g).ellipse((c[0] - rad, c[1] - rad, c[0] + rad, c[1] + rad), fill=PINK + (int(210 * (1 - glow_p * .4)),))
        g = g.filter(ImageFilter.GaussianBlur(26 * scale))
        L.alpha_composite(g)
    d = ImageDraw.Draw(L)
    g = vgrad(R * 2 * scale, R * 2 * scale, PINK2, PINK).convert('RGBA')
    m = Image.new('L', g.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, g.width - 1, g.height - 1), fill=255)
    L.paste(g, (c[0] - R * scale, c[1] - R * scale), m)
    # flecha rotable
    a = Image.new('RGBA', L.size, (0, 0, 0, 0))
    ad = ImageDraw.Draw(a)
    k = R * scale * .5
    ad.line((c[0], c[1] + k, c[0], c[1] - k), fill=(255, 255, 255, 255), width=int(R * scale * .13))
    ad.line((c[0] - k * .7, c[1] - k * .3, c[0], c[1] - k), fill=(255, 255, 255, 255), width=int(R * scale * .13))
    ad.line((c[0] + k * .7, c[1] - k * .3, c[0], c[1] - k), fill=(255, 255, 255, 255), width=int(R * scale * .13))
    a = a.rotate(-45 * rot, resample=Image.BICUBIC, center=c)
    L.alpha_composite(a)
    return down(L, scale)

def neon_line(img, pts, p, color=LIME, width=10, gl=22, head=True):
    """polilinea que se dibuja (trim path) con glow."""
    if p <= 0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    segs = []
    tot = 0
    for a, b in zip(pts[:-1], pts[1:]):
        l = math.hypot(b[0] - a[0], b[1] - a[1]); segs.append((a, b, l)); tot += l
    target = tot * p
    acc = 0
    last = pts[0]
    for a, b, l in segs:
        if acc + l <= target:
            d.line((a, b), fill=color + (255,), width=width); last = b
        else:
            t = (target - acc) / l if l else 0
            e = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            d.line((a, e), fill=color + (255,), width=width); last = e
            break
        acc += l
    g = glow(L, gl, 1.6)
    img.alpha_composite(g)
    img.alpha_composite(L)
    if head and p < 1:
        hd = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(hd).ellipse((last[0] - 16, last[1] - 16, last[0] + 16, last[1] + 16), fill=(255, 255, 255, 255))
        img.alpha_composite(glow(hd, 14, 2))
        img.alpha_composite(hd)

def corner_brackets(img, box, color=LIME, p=1.0, size=70, width=8):
    x0, y0, x1, y1 = box
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    s = size * eo3(p)
    for (cx, cy, sx, sy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        d.line((cx, cy + sy * s, cx, cy, cx + sx * s, cy), fill=color + (255,), width=width, joint='curve')
    img.alpha_composite(glow(L, 8, 1.2))
    img.alpha_composite(L)

def logo_tile(kind, size=300, p=1.0, scale=2):
    """baldosa blanca redondeada con logo."""
    t, pd = rounded_tile(size, size, 64, (255, 255, 255, 255), outline=(232, 232, 236, 255))
    im = t.copy()
    cx = cy = pd + size // 2
    if kind == 'claude':
        lg = Image.open(LG + 'claude_black.png').convert('RGBA')
        a = np.array(lg); mask = a[..., 3] > 0
        a[mask] = (217, 119, 87, 255)[:4] if a.shape[2] == 4 else a[mask]
        a[..., 0:3] = np.where(mask[..., None], np.array([217, 119, 87]), a[..., 0:3])
        lg = Image.fromarray(a, 'RGBA')
        k = int(size * .58)
        lg = lg.resize((k, k), Image.LANCZOS)
        im.alpha_composite(lg, (cx - k // 2, cy - k // 2))
    elif kind == 'remotion':
        lg = Image.open(LG + 'remotion.png').convert('RGBA')
        k = int(size * .6)
        lg = lg.resize((k, int(k * lg.height / lg.width)), Image.LANCZOS)
        im.alpha_composite(lg, (cx - lg.width // 2, cy - lg.height // 2))
    elif kind == 'higgs':
        lg = Image.open(LG + 'hf_icon.png').convert('RGBA')
        k = int(size * .58)
        lg = lg.resize((k, int(k * lg.height / lg.width)), Image.LANCZOS)
        im.alpha_composite(lg, (cx - lg.width // 2, cy - lg.height // 2))
    return im, pd

def number_chip(n, r=44):
    L = ss_layer(r * 2, r * 2, 3)
    d = ImageDraw.Draw(L)
    d.ellipse((0, 0, L.width - 1, L.height - 1), fill=INK + (255,))
    f = font('Archivo', r * 3, 850, 78)
    d.text((L.width // 2, L.height // 2 + 4), str(n), font=f, fill=LIME + (255,), anchor='mm')
    return down(L, 3)

def blur_image(im, r):
    return im.filter(ImageFilter.GaussianBlur(r)) if r > .3 else im

def to_rgb(img):
    return np.array(img.convert('RGB'))


# ================================================================ helpers de escena
WHITE = (255, 255, 255)

def footage(foot, zoom=1.0, dx=0, dy=0):
    """ndarray HxWx3 -> RGBA con zoom/recorte (para mover el crudo sin perder resolucion)."""
    im = Image.fromarray(foot)
    if zoom > 1.0001:
        cw, ch = int(W / zoom), int(H / zoom)
        x0 = int((W - cw) / 2 + dx); y0 = int((H - ch) / 2 + dy)
        x0 = max(0, min(W - cw, x0)); y0 = max(0, min(H - ch, y0))
        im = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BICUBIC)
    return im.convert('RGBA')

def place(img, layer, cx, cy, s=1.0, a=1.0, blur=0.0, rot=0.0):
    """pega `layer` centrado en (cx,cy) con escala, alpha, blur y rotacion."""
    if a <= 0.003 or s <= 0.01: return
    L = layer
    if abs(s - 1.0) > .003:
        L = L.resize((max(2, int(L.width * s)), max(2, int(L.height * s))), Image.LANCZOS)
    if rot:
        L = L.rotate(rot, resample=Image.BICUBIC, expand=True)
    if blur > .4:
        pad = int(blur * 3)
        P = Image.new('RGBA', (L.width + pad * 2, L.height + pad * 2), (0, 0, 0, 0))
        P.alpha_composite(L, (pad, pad))
        L = P.filter(ImageFilter.GaussianBlur(blur))
    paste(img, L, (cx - L.width / 2, cy - L.height / 2), a)

def lime_pill(w, h, text, size, tcol=INK):
    return pill(w, h, LIME2, LIME, text, HEAD(size), tcol=tcol)

def pink_pill(w, h, text, size):
    return pill(w, h, PINK2, PINK, text, HEAD(size), tcol=WHITE)

def dark_panel(w, h, r=36, a=215):
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(L).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=INK + (a,))
    return L

def shards(img, box, p, seed=0, colors=(PINK, LIME, WHITE), n=170, g=900, spread=520):
    """el rectangulo `box` se desintegra en cuadrados que caen (p 0..1)."""
    if p <= 0 or p >= 1: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    for i in range(n):
        sx = rng.uniform(x0, x1); sy = rng.uniform(y0, y1)
        vx = rng.uniform(-1, 1) * spread * .5 + (sx - (x0 + x1) / 2) * .6
        vy = rng.uniform(-1.2, .3) * spread * .6
        tt = p * .9
        x = sx + vx * tt; y = sy + vy * tt + g * tt * tt * .5
        s = rng.uniform(10, 34) * (1 - .5 * p)
        al = int(255 * (1 - p) ** 1.2)
        d.rectangle((x - s / 2, y - s / 2, x + s / 2, y + s / 2), fill=rng.choice(colors) + (al,))
    img.alpha_composite(glow(L, 6, 1.0))
    img.alpha_composite(L)

def flicker_blocks(img, box, t, seed, n=5, color=LIME, rate=14):
    """bloques de color que parpadean detras de un numero o titulo."""
    rng = random.Random(seed * 1000 + int(t * rate))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    for _ in range(n):
        w = rng.randint(60, 220); h = rng.randint(40, 120)
        x = rng.randint(int(x0), int(x1 - w)); y = rng.randint(int(y0), int(y1 - h))
        d.rectangle((x, y, x + w, y + h), fill=color + (255,))
