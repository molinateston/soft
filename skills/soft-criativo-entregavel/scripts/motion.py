"""
MOTION EDITS PRO - motion.py
Curvas de velocidad estilo After Effects (Graph Editor), keyframes con easing por
segmento, resortes, wiggle, motion blur por sub-frames, camara y speed ramp.

Modelo de AE:  cada keyframe tiene "influence" (que tan largo es el mango, 0-1) y
"speed" (pendiente). Un segmento entre dos keys es una bezier cubica con
P1 = (out_influence, out_speed * out_influence)
P2 = (1 - in_influence, 1 - in_speed * in_influence)
en coordenadas normalizadas (tiempo 0-1, valor 0-1), donde speed 1 = velocidad promedio.
Easy Ease de AE = influence 33.3% y speed 0 en ambos lados = ae(.333, .333).
"""
import math
import numpy as np

# ------------------------------------------------------------------ bezier
def cubic_bezier(x1, y1, x2, y2):
    """Devuelve f(p) para p en [0,1]. Igual que cubic-bezier() de CSS / mango de AE.
    y1,y2 pueden salirse de [0,1] (overshoot / anticipacion)."""
    cx, bx = 3 * x1, 3 * (x2 - x1) - 3 * x1
    ax = 1 - cx - bx
    cy, by = 3 * y1, 3 * (y2 - y1) - 3 * y1
    ay = 1 - cy - by

    def sx(t): return ((ax * t + bx) * t + cx) * t
    def sy(t): return ((ay * t + by) * t + cy) * t
    def dx(t): return (3 * ax * t + 2 * bx) * t + cx

    def solve(x):
        t = x
        for _ in range(8):                      # Newton
            e = sx(t) - x
            if abs(e) < 1e-6: return t
            d = dx(t)
            if abs(d) < 1e-6: break
            t -= e / d
        lo, hi = 0.0, 1.0                       # biseccion de respaldo
        t = x
        for _ in range(40):
            e = sx(t)
            if abs(e - x) < 1e-6: break
            if e < x: lo = t
            else: hi = t
            t = (lo + hi) / 2
        return t

    def f(p):
        if p <= 0: return 0.0
        if p >= 1: return 1.0
        return sy(solve(p))
    f.params = (x1, y1, x2, y2)
    return f


def ae(out_inf=.333, in_inf=.333, out_speed=0.0, in_speed=0.0):
    """Curva en el vocabulario del Graph Editor de AE."""
    return cubic_bezier(out_inf, out_speed * out_inf, 1 - in_inf, 1 - in_speed * in_inf)


# Presets. Nombre -> funcion. Los nombres dicen para que sirven.
EASE = {
    'linear':      lambda p: min(1.0, max(0.0, p)),
    'easy':        ae(.333, .333),                    # F9 de AE
    'easy_in':     ae(.1, .75),                       # Easy Ease In de AE: sale rapido, llega frenando (ENTRADAS)
    'easy_out':    ae(.75, .1),                       # arranca lento y se va acelerando (SALIDAS)
    'expo_out':    cubic_bezier(.16, 1, .3, 1),       # entrada "caliente": 90% en el primer tercio
    'expo_in':     cubic_bezier(.7, 0, .84, 0),       # salida que acelera hasta irse
    'expo_inout':  cubic_bezier(.87, 0, .13, 1),      # movimientos de camara caros
    'quart_inout': cubic_bezier(.76, 0, .24, 1),
    'cine':        ae(.62, .62),                      # lento-rapido-lento suave, pico a mitad (camara)
    'whip':        ae(.9, .9),                        # pico de velocidad muy alto (whip pan)
    'snap':        cubic_bezier(.7, 0, .15, 1),
    'back_out':    cubic_bezier(.34, 1.56, .64, 1),   # overshoot ~8%
    'back_out_x':  cubic_bezier(.2, 2.1, .4, 1),      # overshoot fuerte (pop de sello)
    'back_in':     cubic_bezier(.36, 0, .66, -.56),   # anticipacion (se hunde antes de salir)
    'anticip':     cubic_bezier(.5, -.9, .25, 1),     # anticipacion + salida rapida
    'hold':        lambda p: 0.0 if p < 1 else 1.0,   # keyframe "hold" (escalon)
}

def get_ease(e):
    if e is None: return EASE['easy']
    if callable(e): return e
    if isinstance(e, str): return EASE[e]
    if isinstance(e, (tuple, list)):
        if len(e) == 4: return cubic_bezier(*e)
        raise ValueError('ease tuple = (x1,y1,x2,y2)')
    raise ValueError(e)


# ------------------------------------------------------------------ utilidades
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else (1.0 if t >= a else 0.0)
def lerp(a, b, p): return a + (b - a) * p
def remap(x, a, b, c, d): return lerp(c, d, clamp((x - a) / (b - a)))

def tween(t, a, b, v0, v1, ease='expo_out'):
    """valor entre v0 y v1 durante [a,b] con la curva dada (escalar o vector)."""
    p = get_ease(ease)(prog(t, a, b)) if True else 0
    if isinstance(v0, (tuple, list, np.ndarray)):
        return tuple(lerp(x, y, p) for x, y in zip(v0, v1))
    return lerp(v0, v1, p)


# ------------------------------------------------------------------ keyframes
class Track:
    """Propiedad animada con keyframes. keys = [(t, valor, ease_saliente), ...]
    El ease de cada key define el segmento que EMPIEZA en esa key (como en AE donde el
    mango de salida manda). Valores escalares o tuplas.
        pos = Track([(1.0,(540,2200),'expo_out'), (1.7,(540,960),'easy'), (3.0,(540,900))])
        x, y = pos(t)
    """
    def __init__(self, keys):
        self.keys = sorted(keys, key=lambda k: k[0])

    def __call__(self, t):
        ks = self.keys
        if t <= ks[0][0]: return ks[0][1]
        if t >= ks[-1][0]: return ks[-1][1]
        for i in range(len(ks) - 1):
            t0, v0 = ks[i][0], ks[i][1]
            t1, v1 = ks[i + 1][0], ks[i + 1][1]
            if t0 <= t < t1:
                e = get_ease(ks[i][2] if len(ks[i]) > 2 else 'easy')
                p = e((t - t0) / (t1 - t0))
                if isinstance(v0, (tuple, list, np.ndarray)):
                    return tuple(lerp(a, b, p) for a, b in zip(v0, v1))
                return lerp(v0, v1, p)
        return ks[-1][1]


def stagger(i, t, start, step=.08, dur=.6):
    """progreso 0-1 del elemento i de una lista que entra en cascada."""
    return prog(t, start + i * step, start + i * step + dur)


# ------------------------------------------------------------------ resortes y ruido
def spring(t, freq=3.2, damping=.42):
    """Respuesta de un resorte amortiguado a un escalon en t=0. t en segundos.
    Sube a 1, rebasa y se asienta. damping 0.3 = muy rebotador, 0.7 = suave."""
    if t <= 0: return 0.0
    w = 2 * math.pi * freq
    z = damping
    wd = w * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w * t) * (math.cos(wd * t) + z / math.sqrt(1 - z * z) * math.sin(wd * t))


def wiggle(t, freq=2.0, amp=1.0, seed=0, octaves=2):
    """Ruido suave determinista (como wiggle() de AE). Devuelve valor en [-amp, amp]."""
    v, a, f, norm = 0.0, 1.0, freq, 0.0
    for o in range(octaves):
        ph = (seed * 7919 + o * 104729) % 628 / 100.0
        ph2 = (seed * 15485 + o * 32452) % 628 / 100.0
        v += a * (math.sin(t * f * 2 * math.pi + ph) * .6 + math.sin(t * f * 2.7 * math.pi + ph2) * .4)
        norm += a; a *= .5; f *= 2
    return amp * v / norm


def shake(t, amp=8, freq=14, decay=None, t0=0.0, seed=1):
    """Sacudida de camara 2D (dx, dy) en pixeles. decay=segundos hasta apagarse (None = sin decay)."""
    k = 1.0
    if decay: k = max(0.0, 1 - (t - t0) / decay) ** 2
    return (wiggle(t, freq, amp * k, seed), wiggle(t, freq, amp * k, seed + 17))


def drift(t, secs=9.0, pct=.04):
    """Zoom lento constante ("nunca estatica"). ~4% cada 9 s."""
    return 1.0 + pct * (t / secs)


# ------------------------------------------------------------------ camara 2D
def camera(img, zoom=1.0, cx=None, cy=None, rot=0.0, dx=0, dy=0, resample=None):
    """Aplica zoom/rotacion/desplazamiento de camara a un PIL.Image completo.
    cx,cy = punto de foco (por defecto el centro). zoom>1 acerca hacia ese punto."""
    from PIL import Image
    W, H = img.size
    cx = W / 2 if cx is None else cx
    cy = H / 2 if cy is None else cy
    th = math.radians(rot)
    c, s = math.cos(th), math.sin(th)
    # transform PIL: salida -> entrada. out(x,y) = in(a x + b y + c, d x + e y + f)
    inv = 1.0 / zoom
    a, b = c * inv, s * inv
    d, e = -s * inv, c * inv
    ox = cx - (a * (W / 2 - dx) + b * (H / 2 - dy))
    oy = cy - (d * (W / 2 - dx) + e * (H / 2 - dy))
    return img.transform((W, H), Image.AFFINE, (a, b, ox, d, e, oy), resample=resample or Image.BICUBIC)


# ------------------------------------------------------------------ motion blur
def dir_blur(img, length, angle=0.0, samples=9):
    """Blur direccional (acumula copias desplazadas). length en px, angle en grados."""
    from PIL import Image, ImageChops
    if length < 1.5: return img
    ax, ay = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    acc = None
    for i in range(samples):
        k = (i / (samples - 1) - .5) * length
        sh = ImageChops.offset(img, int(round(ax * k)), int(round(ay * k)))
        a = np.asarray(sh, dtype=np.float32)
        acc = a if acc is None else acc + a
    return Image.fromarray((acc / samples).astype(np.uint8), img.mode)


def mblur(render, t, fps, shutter=.5, samples=4):
    """Motion blur real por sub-frames: promedia render(t') en la ventana del obturador.
    shutter=.5 equivale a 180 grados. Cuesta `samples` veces mas. Usar solo en cortes rapidos."""
    from PIL import Image
    if samples <= 1: return render(t)
    dt = shutter / fps
    acc = None
    for i in range(samples):
        tt = t + (i / (samples - 1) - .5) * dt
        a = np.asarray(render(tt).convert('RGB'), dtype=np.float32)
        acc = a if acc is None else acc + a
    return Image.fromarray((acc / samples).astype(np.uint8), 'RGB').convert('RGBA')


def speed_blur_amount(track, t, fps, k=.35, maxlen=120):
    """Blur proporcional a la velocidad de un Track de posicion: longitud en px."""
    a, b = track(t - .5 / fps), track(t + .5 / fps)
    if isinstance(a, (tuple, list)):
        v = math.hypot(b[0] - a[0], b[1] - a[1])
    else:
        v = abs(b - a)
    return min(maxlen, v * k)


# ------------------------------------------------------------------ speed ramp (b-roll)
class RemapReader:
    """Lee un video como si el tiempo de origen siguiera una curva (speed ramp / time remap).
    Pide tiempos de origen NO decrecientes. Hace frame-blending en camara lenta.
        rr = RemapReader('b-roll.mp4', fps=24000/1001, w=1080, h=1920)
        frame = rr.at(src_time)           # ndarray HxWx3
    Para el crudo con voz NO usar: el audio quedaria desfasado (usar zoom/escala en su lugar)."""
    def __init__(self, path, fps, w=1080, h=1920):
        import subprocess
        self.fps, self.w, self.h = fps, w, h
        self.n = w * h * 3
        self.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'fps={fps},scale={w}:{h}',
                                   '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        self.idx = -1
        self.cur = None
        self.nxt = self._read()
        self.idx = 0
        self.cur = self.nxt
        self.nxt = self._read()

    def _read(self):
        b = self.p.stdout.read(self.n)
        if len(b) < self.n: return None
        return np.frombuffer(b, np.uint8).reshape(self.h, self.w, 3)

    def at(self, s):
        f = s * self.fps
        i = int(f)
        while self.idx < i:
            self.cur, self.nxt = self.nxt, self._read()
            self.idx += 1
            if self.cur is None: break
        if self.cur is None: return np.zeros((self.h, self.w, 3), np.uint8)
        fr = f - i
        if self.nxt is None or fr < .05: return self.cur
        return ((1 - fr) * self.cur + fr * self.nxt).astype(np.uint8)

    def close(self):
        try: self.p.kill()
        except Exception: pass


def ramp(t, points):
    """Tiempo de origen para un speed ramp. points = [(t_salida, t_origen, ease_saliente), ...]
    Ej: [(0,0,'linear'), (2,2,'expo_inout'), (2.6,2.9,'linear'), (5,5.6)] acelera entre 2 y 2.6 s."""
    return Track([(a, b, c if len(p) > 2 else 'linear') for p in points for (a, b, c) in [(p + ('linear',))[:3]]])(t)


# ------------------------------------------------------------------ vista de curvas
def plot_curves(names=None, path='curves.png', cols=4, cell=300):
    """Guarda una hoja con el grafico de velocidad de cada preset (para elegir de un vistazo)."""
    from PIL import Image, ImageDraw, ImageFont
    names = names or [k for k in EASE if k != 'hold']
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * cell, rows * cell), (14, 14, 18))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.load_default()
    for n, name in enumerate(names):
        ox, oy = (n % cols) * cell, (n // cols) * cell
        pad = 38
        x0, y0, x1, y1 = ox + pad, oy + pad + 20, ox + cell - pad, oy + cell - pad
        d.rectangle((x0, y0, x1, y1), outline=(60, 60, 70))
        d.text((ox + pad, oy + 12), name, fill=(210, 245, 42), font=f)
        e = EASE[name]
        top, bot = 1.6, -.7
        def Y(v): return y1 - (v - bot) / (top - bot) * (y1 - y0)
        d.line((x0, Y(0), x1, Y(0)), fill=(50, 50, 58)); d.line((x0, Y(1), x1, Y(1)), fill=(50, 50, 58))
        pts = [(x0 + (x1 - x0) * i / 100, Y(e(i / 100))) for i in range(101)]
        d.line(pts, fill=(233, 21, 113), width=3)
        # velocidad (derivada) en lima
        vs = []
        for i in range(100):
            v = (e((i + 1) / 100) - e(i / 100)) * 100
            vs.append((x0 + (x1 - x0) * i / 100, y1 - clamp((v / 4 + .02), 0, 1) * (y1 - y0) * .55))
        d.line(vs, fill=(210, 245, 42), width=1)
    sheet.save(path)
    return path


if __name__ == '__main__':
    # autotest
    e = ae(.333, .333)
    assert abs(e(.5) - .5) < 1e-3
    assert abs(EASE['expo_out'](.3) - 0.9) < .12, EASE['expo_out'](.3)
    assert EASE['back_out'](.7) > 1.0
    tr = Track([(0, 0, 'expo_out'), (1, 100, 'easy'), (2, 50)])
    assert abs(tr(1.0) - 100) < 1e-6 and abs(tr(2.0) - 50) < 1e-6 and 50 < tr(1.5) < 100
    tr2 = Track([(0, (0, 0), 'cine'), (1, (100, 200))])
    assert tr2(.5)[0] > 40
    assert spring(.5) > .9 and max(spring(i / 100) for i in range(100)) > 1.05
    print('motion.py OK')
