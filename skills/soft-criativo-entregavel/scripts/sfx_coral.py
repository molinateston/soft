"""Efectos de sonido suaves y graves, sintetizados. Sin agudos molestos."""
import sys, json, wave
import numpy as np
SR = 44100
def _t(n): return np.arange(n) / SR
def _rng(seed): return np.random.RandomState(seed)

def lp(x, fc):
    k = max(1, int(SR / fc)); return np.convolve(x, np.ones(k) / k, 'same')

def sub_hit(g=1.0, f0=58):
    n = int(.9 * SR); t = _t(n); f = f0 * (1 + 1.3 * np.exp(-t / .05))
    return g * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / .002) * np.exp(-t / .26)

def boom(g=1.0):
    n = int(1.7 * SR); t = _t(n)
    return g * .8 * (np.sin(2 * np.pi * 44 * t) * np.exp(-t / .6) + .35 * lp(_rng(1).randn(n), 900) * np.exp(-t / .22))

def swoosh(g=1.0, dur=.6, seed=2, fc=520):
    n = int(dur * SR); t = _t(n); env = np.sin(np.pi * t / dur) ** 2
    return g * 2.6 * lp(_rng(seed).randn(n), fc) * env

def riser(g=1.0, dur=1.0):
    n = int(dur * SR); t = _t(n); f = 90 + 520 * (t / dur) ** 2
    return g * .45 * np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / dur) ** 1.6

def plim(g=1.0, f=780):
    n = int(.34 * SR); t = _t(n)
    return g * .5 * (np.sin(2 * np.pi * f * t) + .28 * np.sin(2 * np.pi * f * 2 * t)) * np.minimum(1, t / .004) * np.exp(-t / .075)

def pop(g=1.0):
    n = int(.22 * SR); t = _t(n); f = 190 * (1 + 1.6 * np.exp(-t / .03))
    return g * .55 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .05)

def tick(g=1.0):
    n = int(.05 * SR); t = _t(n)
    return g * .3 * lp(_rng(int(g * 100) + 5).randn(n), 3200) * np.exp(-t / .008)

def click(g=1.0):
    n = int(.1 * SR); t = _t(n)
    return g * (.5 * np.sin(2 * np.pi * 210 * t) * np.exp(-t / .02) + .18 * lp(_rng(9).randn(n), 2600) * np.exp(-t / .006))

def chime(g=1.0):
    n = int(1.1 * SR); t = _t(n)
    a = np.sin(2 * np.pi * 523 * t) * np.exp(-t / .35)
    b = np.sin(2 * np.pi * 784 * t) * np.exp(-(t - .09).clip(0) / .4) * (t > .09)
    return g * .3 * (a + .8 * b)

def crack(g=1.0, seed=3):
    n = int(.16 * SR); t = _t(n)
    return g * .6 * lp(_rng(seed).randn(n), 2200) * np.exp(-t / .03)

def debris(g=1.0):
    n = int(1.0 * SR); t = _t(n); r = lp(_rng(11).randn(n), 1400)
    gate = (_rng(12).rand(n // 400 + 1).repeat(400)[:n] > .55)
    return g * 1.3 * r * np.exp(-t / .3) * (.35 + .65 * gate)

KINDS = dict(sub_hit=sub_hit, boom=boom, swoosh=swoosh, riser=riser, plim=plim, pop=pop, tick=tick, click=click, chime=chime, crack=crack, debris=debris)

def build(cues, dur, out):
    buf = np.zeros(int((dur + 2) * SR))
    for c in cues:
        kw = {k: v for k, v in c.items() if k not in ('t', 'kind')}
        s = KINDS[c['kind']](**kw); i = int(c['t'] * SR)
        buf[i:i + len(s)] += s[:len(buf) - i]
    buf = np.clip(buf / max(1e-6, np.abs(buf).max()) * .9, -1, 1)
    with wave.open(out, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 32767).astype(np.int16).tobytes())

def cue_list():
    C = []; add = lambda t, k, **kw: C.append(dict(t=round(t, 3), kind=k, **kw))
    # transiciones de mancha
    for t in (1.04, 4.96, 8.93, 14.74, 20.56, 26.36): add(t, 'swoosh', g=.55, dur=.6, seed=int(t * 10))
    for t, d in ((3.02, .55), (7.05, .55), (23.0, .55), (29.26, .55)): add(t, 'swoosh', g=.6, dur=d, seed=int(t * 10) + 1); add(t + d + .02, 'sub_hit', g=.35)
    for t in (3.4, 7.5, 23.4, 29.65): add(t, 'swoosh', g=.4, dur=.5, seed=int(t * 10) + 2, fc=700)
    # tumba
    add(1.72, 'sub_hit', g=1.0); add(1.74, 'debris', g=.4)
    for t in (2.06, 2.16, 2.27, 2.38, 2.47): add(t, 'crack', g=.7, seed=int(t * 100))
    add(2.62, 'boom', g=1.0); add(2.64, 'debris', g=.9); add(2.78, 'swoosh', g=.5, dur=.5, seed=7, fc=420)
    # subida del video
    add(5.4, 'pop', g=.8); add(6.62, 'click', g=.8); add(6.64, 'plim', g=.5, f=988); add(6.75, 'swoosh', g=.4, dur=.4, seed=21)
    for k, t in enumerate((6.9, 6.95, 7.0, 7.05, 7.1)): add(t, 'pop', g=.35)
    # herramientas
    for t, f in zip((9.72, 9.98, 10.24), (660, 784, 988)): add(t, 'plim', g=.85, f=f)
    add(10.55, 'riser', g=.6, dur=.6); add(11.14, 'sub_hit', g=.8); add(11.14, 'plim', g=.7, f=1175)
    for t in (11.95, 12.38, 13.4, 14.0): add(t, 'swoosh', g=.5, dur=.5, seed=int(t * 10) + 5, fc=620)
    for t in (12.9, 14.5): add(t, 'pop', g=.7); add(t, 'plim', g=.5, f=880)
    # estilos
    for t in (16.9, 17.8, 18.7, 19.6): add(t, 'pop', g=.7); add(t + .75, 'plim', g=.45, f=880)
    for k, t in enumerate((20.3, 20.4, 20.5, 20.6)): add(t, 'plim', g=.35, f=660 + 120 * k)
    # prompt
    add(21.1, 'pop', g=.6); add(21.32, 'pop', g=.6)
    t = 21.65
    while t < 22.35: add(t, 'tick', g=.55 + .2 * ((int(t * 100)) % 3) / 2); t += .065
    add(22.4, 'click', g=.9); add(22.52, 'swoosh', g=.5, dur=.7, seed=31, fc=600)
    # cierre
    add(26.62, 'pop', g=.7); add(26.85, 'plim', g=.5, f=660); add(26.9, 'riser', g=.7, dur=2.1)
    add(29.0, 'chime', g=.9); add(29.0, 'boom', g=.55)
    return C

if __name__ == '__main__':
    build(cue_list(), 32.032, sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav'); print('ok', len(cue_list()), 'cues')
