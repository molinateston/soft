"""Etapa 6d. Composicao final 1080x1920 (ordem das camadas: tarja de cima, video, tarja de baixo, legenda por ultimo).
Le base.mkv, audio.wav, reframe.json, conceitos.json, palavras-saida.json, cortes.json e ajustes.json
(hold_ini: repete o 1o quadro do corpo por N quadros quando a fonte ainda mostra o plano anterior; padrao 0).
uso: python3 06_compor.py TRAB [--ate SEGUNDOS]      saidas: final.mp4, render-log.json
criterio de pronto: imprime PRONTO; final.mp4 existe com 1 trilha de video e 1 de audio."""
import json, os, subprocess, sys
from PIL import Image, ImageFilter
import comum as C
import tarjas

T = C.trab_arg()
M, A = C.marca(T), C.ajustes(T)
CC, CO = C.lj(T, 'cortes.json'), C.lj(T, 'conceitos.json')
PAL = C.lj(T, 'palavras-saida.json')
BOX = json.load(open(os.path.join(T, 'reframe.json')))
FPS = C.FPS
BASE, AUD, OUT = (os.path.join(T, x) for x in ('base.mkv', 'audio.wav', 'final.mp4'))
dur = C.duracao(BASE)
if '--ate' in sys.argv: dur = min(dur, float(sys.argv[sys.argv.index('--ate') + 1]))
NF = int(round(dur * FPS))
SW, SH = C.tamanho(BASE)
fsz = SW * SH * 3

topo, hl_log = tarjas.topo(M, CO['headline'])
HOLD_AT = int(round(CC.get('cold_saida', 0) * FPS))
leg = tarjas.Legenda(M, PAL, corte=CC.get('cold_saida', 0))
D = tarjas.modulo_desenhos(T, A.get('desenhos'))
BX = tarjas.Baixo(M, CO['conceitos'], D)
HOLD = int(A.get('hold_ini', 0))

dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', BASE, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['nice', '-n', '15', 'ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{C.W}x{C.H}',
                        '-r', str(FPS), '-i', '-', '-i', AUD, '-map', '0:v', '-map', '1:a', '-t', f'{dur:.3f}',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
                        '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
pre, leg_x = [], []
for n in range(NF):
    t = n / FPS
    if HOLD and n == HOLD_AT: pre = [dec.stdout.read(fsz) for _ in range(HOLD + 1)]
    no_hold = HOLD and HOLD_AT <= n <= HOLD_AT + HOLD
    raw = pre[HOLD] if no_hold else dec.stdout.read(fsz)
    if len(raw) < fsz: NF = n; break
    fr = Image.new('RGB', (C.W, C.H), C.cor(M, 'tarja'))
    fr.paste(topo, (0, 0))
    x0, y0, bw, bh = BOX[min(HOLD_AT + HOLD if no_hold else n, len(BOX) - 1)]
    vid = Image.frombytes('RGB', (SW, SH), raw).resize((C.WV, C.HV), Image.LANCZOS, box=(x0, y0, x0 + bw, y0 + bh))
    fr.paste(vid.filter(ImageFilter.UnsharpMask(radius=1.5, percent=45, threshold=2)), (0, C.YV))
    fr.paste(BX.em(t), (0, C.YB))
    w = leg.em(t)
    if w:
        im = leg.img(w)
        fr.paste(im, (C.W // 2 - im.width // 2, C.CAP_Y - 55), im)
        leg_x.append([C.W // 2 - im.width // 2, C.W // 2 - im.width // 2 + im.width])
    enc.stdin.write(fr.tobytes())
    if n % 300 == 0: print(f'quadro {n}/{NF}', flush=True)
enc.stdin.close(); enc.wait(); dec.kill()
C.gj(T, 'render-log.json', dict(
    dur=round(NF / FPS, 3), quadros=NF, cap_y=C.CAP_Y, legenda_bbox_y=[C.CAP_Y - 55, C.CAP_Y + 55],
    legenda_x=[min([a for a, b in leg_x] or [0]), max([b for a, b in leg_x] or [0])],
    headline=hl_log, desenhos={c['id']: [round(v) for v in BX.bbox_final(c['id'])] for c in CO['conceitos']},
    hold_ini=HOLD, hold_em=HOLD_AT, parcial='--ate' in sys.argv))
ok = enc.returncode == 0 and os.path.exists(OUT)
print(OUT, f'{NF} quadros', 'PRONTO' if ok else 'NAO PRONTO')
sys.exit(0 if ok else 1)
