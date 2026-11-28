"""Etapa 1. Entrada: confere o bruto e extrai o audio 16 kHz mono (para transcricao e gates).
Le ajustes.json: "fonte" (caminho do bruto) e "janela" opcional [ini, fim] em segundos da fonte.
uso: python3 01_entrada.py TRAB
saidas: TRAB/entrada.json, TRAB/fonte16.wav (comeca em janela[0]; o offset fica em entrada.json)"""
import json, os, subprocess, sys
import comum as C

T = C.trab_arg()
A = C.ajustes(T)
F = os.path.abspath(os.path.join(T, A['fonte']))
if not os.path.exists(F):
    sys.exit(f'bruto nao encontrado: {F}')
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', F]))
v = [s for s in pr['streams'] if s['codec_type'] == 'video']
a = [s for s in pr['streams'] if s['codec_type'] == 'audio']
if not v or not a:
    sys.exit('o bruto precisa ter video e audio')
dur = float(pr['format']['duration'])
ini, fim = A.get('janela', [0, dur])
fim = min(fim, dur)
w, h = int(v[0]['width']), int(v[0]['height'])
num, den = v[0]['avg_frame_rate'].split('/')
fps = float(num) / float(den or 1)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{ini:.3f}', '-t', f'{fim - ini:.3f}', '-i', F, '-vn', '-ac', '1', '-ar', '16000',
                '-c:a', 'pcm_s16le', os.path.join(T, 'fonte16.wav')], check=True)
E = dict(fonte=F, largura=w, altura=h, fps=round(fps, 3), duracao=round(dur, 3), offset=ini, fim=fim)
C.gj(T, 'entrada.json', E)
print(json.dumps(E, ensure_ascii=False))
ok = abs(w / h - 16 / 9) < 0.02
print('PRONTO' if ok else 'ATENCAO: bruto nao e 16:9; defina "painel" no ajustes.json', f'{w}x{h} {fps:.2f} fps, audio {fim - ini:.1f} s extraido')
