#!/usr/bin/env python3
"""Biblioteca de sons dos GIFs de meme, sintetizada localmente com numpy (sem download, sem pacote).

Obra própria, livre (CC0). Determinística (sementes fixas): rodar de novo gera os mesmos arquivos.
Uso: python3 -I sfx_gif.py pasta_saida   ->  <nome>.wav (48 kHz, estéreo, 16 bit, pico -6 dBFS) + sons.json
O nível final NÃO vem do arquivo: a mixagem aplica ganho pelo RMS (pop -12 dB, sting -1 dB do p90 da voz).
"""
import json, sys, wave
from pathlib import Path
import numpy as np

SR = 48000
R = np.random.RandomState


def _t(d): return np.arange(int(d * SR)) / SR
def _lp(x, fc):
    k = max(1, int(SR / fc)); return np.convolve(x, np.ones(k) / k, 'same')
def _bp(x, lo, hi): return _lp(x, hi) - _lp(x, lo)
def _st(a, b=None): return np.stack([a, a if b is None else b], 1)


def _env(n, a=.005, r=None):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    if r: e *= np.exp(-np.arange(n) / (r * SR))
    nf = int(.01 * SR); e[-nf:] *= np.linspace(1, 0, nf); return e


def _soma(dur, *partes):
    out = np.zeros((int(dur * SR), 2))
    for x, t0, g in partes:
        if x.ndim == 1: x = _st(x)
        a = int(t0 * SR); n = min(len(x), len(out) - a); out[a:a + n] += x[:n] * g
    return out


def pop():  # entrada do GIF: pop suave 0,11 s (mesma receita do pop suave dos sons do gancho)
    n = int(.11 * SR); t = np.arange(n) / SR; f = 650 * (1 + .45 * np.exp(-t / .015))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / .002) * np.exp(-t / .028)
    return _st(s + .05 * _bp(R(3).randn(n), 400, 2000) * np.exp(-t / .01), s + .05 * _bp(R(4).randn(n), 400, 2000) * np.exp(-t / .01))


def tontura():  # confusão: apito de desenho descendo com vibrato, girando no estéreo, 1,0 s
    t = _t(1.0); f = 950 * (330 / 950) ** t * (1 + .06 * np.sin(2 * np.pi * 7 * t)); ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + .25 * np.sin(2 * ph) + .1 * np.sin(3 * ph)) * _env(len(t), .01, .6)
    p = .5 + .35 * np.sin(2 * np.pi * 2.5 * t); return np.stack([x * (1 - p), x * p], 1) * 2


def trombone():  # dor/fracasso: trombone triste "uón uón uón uóóón" (Si-Lá#-Lá-Sol#), 1,6 s
    out = np.zeros(int(1.6 * SR))
    for t0, f0, d, vib in ((0, 246.9, .3, 0), (.32, 233.1, .3, 0), (.64, 220.0, .3, 0), (.96, 207.7, .64, 1)):
        t = _t(d); f = f0 * (1 + .012 * np.sin(2 * np.pi * 5.5 * t) * vib * np.minimum(1, t / .2)) * (1 - .015 * t / d)
        ph = 2 * np.pi * np.cumsum(f) / SR
        x = sum(np.sin(k * ph) * a for k, a in ((1, 1), (2, .7), (3, .5), (4, .3), (5, .18), (6, .1)))
        wah = .55 + .45 * np.sin(np.pi * np.clip(t / d, 0, 1)) ** .7          # "uá": abre e fecha a surdina
        x = _lp(x * wah, 1400 + 1600 * wah.mean()) * _env(len(t), .03)
        a = int(t0 * SR); out[a:a + len(x)] += x[:len(out) - a]
    return _st(out)


def dinheiro():  # dinheiro: caixa registradora = clique da gaveta + "ching" + duas moedas, 1,1 s
    rng = R(16)
    clk = _bp(rng.randn(int(.03 * SR)), 1500, 6000) * _env(int(.03 * SR), .001, .006)
    gav = _bp(rng.randn(int(.25 * SR)), 200, 1800) * _env(int(.25 * SR), .01, .06) * .5
    t = _t(.9); ching = (np.sin(2 * np.pi * 2637 * t) + .7 * np.sin(2 * np.pi * 3951 * t) + .3 * np.sin(2 * np.pi * 5274 * t)) * _env(len(t), .002, .25)
    n = int(.36 * SR); tm = np.arange(n) / SR; moeda = np.zeros(n)
    for t0, f, d in ((0, 987.8, .07), (.07, 1318.5, .29)):
        i = int(t0 * SR); tt = tm[:n - i]
        moeda[i:] += _lp(np.sign(np.sin(2 * np.pi * f * tt)) * .35 + np.sin(2 * np.pi * f * tt), 9000) * np.minimum(1, tt / .002) * np.exp(-tt / (d / 2.5))
    return _soma(1.1, (clk, 0, 4), (gav, .02, 4), (ching, .12, .45), (moeda, .14, .5), (moeda, .30, .4))


def disco():  # ironia/"fica pra outra": disco arranhado (vai-e-volta) + whoosh de saída, 0,9 s
    rng = R(21); n = int(.9 * SR); t = np.arange(n) / SR; x = rng.randn(n)
    # dois arranhões: frequência central acompanha a "velocidade" do disco
    out = np.zeros(n); blk = 240
    for i in range(0, n - blk, blk):
        u = t[i]
        if u < .38:
            v = np.sin(np.pi * u / .19) ** 2          # vai e volta duas vezes
            fc = 500 + 3500 * v; g = .3 + v
        else:
            v = max(0, 1 - (u - .38) / .5); fc = 600 + 4000 * (1 - v); g = np.sin(np.pi * min(1, (u - .38) / .5)) * .8
        seg = _bp(x[max(0, i - 1024):i + blk], fc * .5, fc * 1.5)[-blk:]
        out[i:i + blk] = seg * g
    ton = np.sin(2 * np.pi * np.cumsum(300 + 900 * np.abs(np.sin(np.pi * t / .19))) / SR) * (t < .38) * .25
    y = (out + ton) * _env(n, .003)
    return np.stack([y, np.roll(y, 30)], 1)


def surpresa():  # surpresa/choque: apito subindo rápido + pop brilhante no topo, 0,7 s
    t = _t(.45); f = 400 * (2000 / 400) ** (t / .45) ** 1.6; ph = 2 * np.pi * np.cumsum(f) / SR
    ap = (np.sin(ph) + .2 * np.sin(2 * ph)) * _env(len(t), .01)
    n = int(.12 * SR); tb = np.arange(n) / SR
    br = np.sin(2 * np.pi * 2400 * tb) * np.exp(-tb / .018) + .6 * _bp(R(5).randn(n), 2500, 7000) * np.exp(-tb / .008)
    return _soma(.7, (ap, 0, 1), (br, .43, 1.2))


def boing():  # bobeira/queda: mola "bóóing" com vibrato largo, 0,8 s
    t = _t(.8); f = 180 * (1 + .9 * np.exp(-t / .08)) * (1 + .18 * np.sin(2 * np.pi * 14 * t) * np.exp(-t / .5))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return _st((np.sin(ph) + .4 * np.sin(2 * ph) + .15 * np.sin(3 * ph)) * _env(len(t), .003, .3))


SONS = {
    'pop-gif': (pop, 'entrada de todo GIF (pop suave)', 'entrada'),
    'sting-tontura': (tontura, 'apito de desenho descendo com vibrato, gira no estéreo', 'confusão, bagunça, "não entendi"'),
    'sting-trombone': (trombone, 'trombone triste de 4 notas descendo (wah-wah)', 'dor, fracasso, dificuldade, "deu ruim"'),
    'sting-dinheiro': (dinheiro, 'caixa registradora: gaveta + ching + moedas', 'dinheiro, economia, faturamento'),
    'sting-disco': (disco, 'disco arranhado vai-e-volta + whoosh de saída', 'ironia, mudança de assunto, "fica pra outro vídeo", saída de fininho'),
    'sting-surpresa': (surpresa, 'apito subindo + pop brilhante', 'surpresa, choque, número absurdo'),
    'sting-boing': (boing, 'mola bóóing', 'bobeira, tombo, ideia ruim'),
}


def main():
    if sys.argv[1:2] in (['-h'], ['--help']): print(__doc__); return
    out = Path(sys.argv[1] if len(sys.argv) > 1 else '.'); out.mkdir(parents=True, exist_ok=True); meta = {}
    for nome, (fn, desc, uso) in SONS.items():
        s = fn().astype(np.float64); s = s / np.abs(s).max() * .5
        with wave.open(str(out / f'{nome}.wav'), 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((s * 32767).astype('<i2').tobytes())
        meta[nome] = dict(arquivo=f'{nome}.wav', descricao=desc, usar_em=uso, duracao_s=round(len(s) / SR, 2),
                          origem='sintetizado localmente com numpy por sfx_gif.py (função ' + fn.__name__ + ')',
                          licenca='obra própria, CC0 (uso livre, sem atribuição)')
        print(nome, meta[nome]['duracao_s'], 's')
    (out / 'sons.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
