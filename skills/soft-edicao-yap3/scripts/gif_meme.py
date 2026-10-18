#!/usr/bin/env python3
"""GIF de meme + som acima da cabeça, sobre um final YAP3 pronto (HEVC HLG, GOP 30 fechado, sem B-frames).

Cartão: GIF retangular (com fundo) num quadrado de cantos arredondados com borda branca, centralizado em x=540,
base fixa em y=BASE_Y (acima da 1ª linha do título), altura ALT_CARTAO, largura pelo aspecto (máx. LARG_MAX).
Pop de entrada ancorado na base (o exagero do easeOutBack cresce para CIMA, nunca para dentro da letra); saída
encolhe e some em 5 quadros. O GIF nunca é espelhado.

Só as janelas dos GIFs são recodificadas (IDR no quadro da palavra k0, fim numa keyframe k1 da base);
o resto é cópia de pacotes da base. Áudio = base + pop-gif (-12 dB) + sting (-1 dB) relativos ao p90 do RMS da voz.

Uso: python3 -I gif_meme.py plano.json [procs] [--so-audio]
plano.json: {"base", "saida", "trab", "sons" (pasta dos .wav), "p90",
             "momentos": [{"k0", "k1", "gif" (mp4), "ini", "laco", "palavra", "fala", "som", "termo", "fonte", "pagina", "titulo"}]}
"""
import sys, os, json, time, subprocess, shutil
from pathlib import Path
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cor_hlg as C

W, H, FS10 = C.W, C.H, C.FS10
CX, BASE_Y, ALT_CARTAO, LARG_MAX, BORDA, RAIO = 540, 300, 272, 500, 5, 28
DB_POP, DB_STING = -12.0, -1.0
PICO_FX = 0.5          # teto de pico por efeito (-6 dBFS): som de crista alta (moeda, ching) não estoura o true peak
PL = None   # plano carregado


def sh(args, **k): return subprocess.run(args, check=True, **k)


def keyframes(f):
    o = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'packet=flags', '-of', 'csv=p=0', str(f)], text=True)
    fl = o.split(); return [i for i, x in enumerate(fl) if x.startswith('K')], len(fl)


def gif_rgb(m, iw, ih):
    """quadros do GIF a 30 fps, escalados (cobre + corta no centro) para iw x ih, rgb24."""
    vf = f'fps=30,scale={iw}:{ih}:force_original_aspect_ratio=increase:flags=lanczos,crop={iw}:{ih}'
    o = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(m['gif']), '-an', '-vf', vf, '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'])
    return np.frombuffer(o, np.uint8).reshape(-1, ih, iw, 3)


def geometria(m):
    gw, gh = map(int, subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                                               '-of', 'csv=p=0', str(m['gif'])], text=True).strip().split(','))
    ih = ALT_CARTAO - 2 * BORDA
    iw = min(LARG_MAX - 2 * BORDA, int(round(ih * gw / gh / 2)) * 2)
    return iw, ih


def mascara(w, h, r, ss=4):
    im = Image.new('L', (w * ss, h * ss), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, fill=255)
    return np.asarray(im.resize((w, h), Image.LANCZOS), np.float32) / 255.0


def escala(i, n):
    """pop de entrada (6 quadros, easeOutBack 0,35 -> ~1,065 -> 1) e saída (5 quadros, encolhe e some)."""
    if i < 6:
        u = (i + 1) / 6; c = 1.70158; e = 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
        return 0.35 + 0.65 * e, min(1.0, (i + 1) / 3)
    j = n - 1 - i
    if j < 5: u = (j + 1) / 6; return 0.55 + 0.45 * u, u
    return 1.0, 1.0


def indice(i, nq, ini, laco):
    """quadro do GIF: começa em ini (s) e repete o trecho [laco, fim) se a janela for mais longa que o GIF."""
    q = int(round(ini * 30)) + i; ql = min(int(round(laco * 30)), nq - 1)
    return q if q < nq else ql + (q - nq) % (nq - ql)


class Cartao:
    def __init__(self, m):
        self.m = m; self.iw, self.ih = geometria(m); self.q = gif_rgb(m, self.iw, self.ih)
        self.cw, self.ch = self.iw + 2 * BORDA, self.ih + 2 * BORDA
        self.a_ext = mascara(self.cw, self.ch, RAIO); self.a_int = mascara(self.iw, self.ih, RAIO - BORDA)

    def rgba(self, i):
        g = self.q[indice(i, len(self.q), self.m.get('ini', 0.0), self.m.get('laco', 0.0))].astype(np.float32)
        cor = np.full((self.ch, self.cw, 3), 255.0, np.float32)             # borda branca (= branco da letra)
        ai = self.a_int[..., None]; sl = (slice(BORDA, BORDA + self.ih), slice(BORDA, BORDA + self.iw))
        cor[sl] = g * ai + cor[sl] * (1 - ai)
        return np.dstack([cor * self.a_ext[..., None], self.a_ext * 255]).clip(0, 255).astype(np.uint8)   # pré-multiplicado

    def camada(self, i, n):
        s, op = escala(i, n)
        w = max(8, int(round(self.cw * s / 2)) * 2); h = max(8, int(round(self.ch * s)))
        p = np.asarray(Image.fromarray(self.rgba(i), 'RGBA').resize((w, h), Image.LANCZOS), np.float32).clip(0, 255)
        x0, y0 = CX - w // 2, BASE_Y - h                                      # ancorado na base: cresce para cima
        a = np.zeros((H, W), np.float32); bp = np.zeros((H, W, 3), np.float32)
        a[y0:BASE_Y, x0:x0 + w] = p[..., 3] / 255.0 * op; bp[y0:BASE_Y, x0:x0 + w] = np.minimum(p[..., :3], p[..., 3:4]) * op
        return a, bp, (x0, y0, x0 + w, BASE_Y)


def segmento(m):
    os.nice(10); t0 = time.time(); k0, k1 = m['k0'], m['k1']; n = k1 - k0; T = Path(PL['trab'])
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-threads', '2', '-ss', f'{k0 / 30:.6f}', '-i', PL['base'], '-frames:v', str(n), '-an',
                          '-pix_fmt', 'yuv420p10le', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    assert len(raw) == n * FS10, (len(raw) / FS10, n)
    ct = Cartao(m); out = T / f'seg-{k0}.mp4'; caixa = [W, H, 0, 0]
    ent = ['-f', 'rawvideo', '-pix_fmt', 'yuv420p10le', '-s', f'{W}x{H}', '-r', '30', '-color_range', 'tv', '-colorspace', 'bt2020nc',
           '-color_primaries', 'bt2020', '-color_trc', 'arib-std-b67', '-i', '-']
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y'] + ent + ['-map', '0:v', '-an', '-frames:v', str(n)] + C.X265 +
                         ['-r', '30', '-fps_mode', 'cfr', '-video_track_timescale', '15360', str(out)], stdin=subprocess.PIPE)
    for i in range(n):
        a, bp, bx = ct.camada(i, n); caixa = [min(caixa[0], bx[0]), min(caixa[1], bx[1]), max(caixa[2], bx[2]), max(caixa[3], bx[3])]
        p.stdin.write(C.compor(raw[i * FS10:(i + 1) * FS10], a, bp))
    p.stdin.close(); assert p.wait() == 0
    return dict(k0=k0, seg=str(out), caixa=caixa, cartao=[ct.cw, ct.ch], quadros_gif=len(ct.q), s=round(time.time() - t0, 1))


def video(procs):
    T = Path(PL['trab']); mom = PL['momentos']
    cortes = sorted(x for m in mom for x in (m['k0'], m['k1']))
    pb = T / 'base-partes'; shutil.rmtree(pb, ignore_errors=True); pb.mkdir(parents=True)
    t0 = time.time()
    with Pool(procs) as pool:
        r = pool.map_async(segmento, mom)
        sh(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-y', '-i', PL['base'], '-map', '0:v', '-c', 'copy', '-f', 'segment',
            '-segment_frames', ','.join(map(str, cortes)), '-break_non_keyframes', '1', '-reset_timestamps', '1', str(pb / 'p%02d.mp4')])
        segs = r.get()
    lista = [pb / f'p{i:02d}.mp4' if i % 2 == 0 else T / f'seg-{mom[i // 2]["k0"]}.mp4' for i in range(len(cortes) + 1)]
    (T / 'concat.txt').write_text(''.join(f"file '{f}'\n" for f in lista))
    sh(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(T / 'concat.txt'), '-c', 'copy',
        '-video_track_timescale', '15360', str(T / 'video.mp4')])
    return dict(segmentos=segs, t_video=round(time.time() - t0, 1), procs=procs)


def dec(args):
    o = subprocess.check_output(['nice', '-n', '10', 'ffmpeg', '-v', 'error'] + args + ['-f', 'f32le', '-ar', '48000', '-ac', '2', '-'])
    return np.frombuffer(o, '<f4').reshape(-1, 2).copy()


def rms(x): return float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))


def audio():
    T = Path(PL['trab']); S = Path(PL['sons']); P90 = PL['p90']
    base = dec(['-i', PL['base'], '-vn']); fx = np.zeros_like(base); ef = []
    for m in PL['momentos']:
        a = round(m['k0'] / 30 * 48000)
        for nome, db in (('pop-gif', DB_POP), (m['som'], DB_STING)):
            s = dec(['-i', str(S / f'{nome}.wav')]); g = min(P90 * 10 ** (db / 20) / rms(s), PICO_FX / float(np.abs(s).max())); n = min(len(s), len(fx) - a)
            fx[a:a + n] += s[:n] * g
            ef.append(dict(k0=m['k0'], t=round(m['k0'] / 30, 3), som=nome, db=db, ganho=round(g, 4), dur=round(len(s) / 48000, 2),
                           pico=round(float(np.max(np.abs(s * g))), 3)))
    mix = base + fx; pk = float(np.max(np.abs(mix))); assert pk < .8, pk
    np.save(T / 'fx.npy', fx.astype('<f4'))
    return mix.astype('<f4'), dict(efeitos=ef, pico_mix=round(pk, 4), amostras=len(mix))


def validar():
    kf, tot = keyframes(PL['base'])
    hb = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=has_b_frames', '-of', 'csv=p=0', PL['base']], text=True).strip()
    assert hb == '0', 'base com B-frames: a cópia de pacotes não fecha'
    ult = -1
    for m in sorted(PL['momentos'], key=lambda m: m['k0']):
        assert m['k1'] in kf, f"k1={m['k1']} não é keyframe da base"
        assert m['k0'] > ult and 30 <= m['k1'] - m['k0'] <= 75, (m['k0'], m['k1'], 'janela fora de 1-2,5 s ou sobreposta')
        assert Path(m['gif']).is_file() and (Path(PL['sons']) / f"{m['som']}.wav").is_file(), m
        ult = m['k1']
    assert len({m['som'] for m in PL['momentos']}) == len(PL['momentos']), 'cada GIF leva um som diferente'
    return tot


def main():
    global PL
    if sys.argv[1:2] in (['-h'], ['--help']): print(__doc__); return
    PL = json.loads(Path(sys.argv[1]).read_text()); procs = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 4
    Path(PL['trab']).mkdir(parents=True, exist_ok=True); tot = validar(); dur = tot / 30
    t0 = time.time()
    if '--so-audio' in sys.argv:   # refaz só a mixagem/mux, reaproveitando trab/video.mp4 já renderizado
        R = {k: v for k, v in json.loads((Path(PL['trab']) / 'render.json').read_text()).items() if k in ('segmentos', 't_video', 'procs')}
    else:
        R = video(procs)
    mix, RA = audio()
    Path(PL['saida']).parent.mkdir(parents=True, exist_ok=True)
    sh(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-y', '-i', str(Path(PL['trab']) / 'video.mp4'), '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', '-',
        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', f'{dur:.6f}', '-movflags', '+faststart', PL['saida']],
       input=mix.tobytes())
    R.update(audio=RA, quadros=tot, t_total=round(time.time() - t0, 1), saida=PL['saida'], momentos=PL['momentos'])
    (Path(PL['trab']) / 'render.json').write_text(json.dumps(R, ensure_ascii=False, indent=1))
    print(json.dumps({k: R[k] for k in ('t_video', 't_total', 'procs')}), json.dumps([(s['k0'], s['caixa'], s['s']) for s in R['segmentos']]))


if __name__ == '__main__':
    main()
