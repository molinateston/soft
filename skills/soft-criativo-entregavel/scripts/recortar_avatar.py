"""Recorta o avatar do fundo no trecho do gancho (para o modo 'gancho_sobre_material': avatar por cima da primeira tela do corpo).
    python recortar_avatar.py <pasta_do_criativo>
Le base.mp4 e tempo.json (rodar depois de montar_base.py) e grava gancho_alpha.npy: uma mascara por quadro do gancho, em 540x960.
Usa o Robust Video Matting (modelo feito para video de pessoa), na versao maior (resnet50) e em resolucao cheia: ~5 quadros por
segundo no processador, uns 40 a 50 s para um gancho de 7 s. O modelo (107 MB) baixa sozinho na primeira vez para
~/.cache/soft-criativo-entregavel/modelos. A versao pequena (mobilenet em 540x960) era 5x mais rapida, mas cortava o antebraco
quando o braco aparecia estendido na frente de uma mesa: o usuario viu ("o braco dele cortou").
Precisa de:  uv pip install onnxruntime
Nao use modelos de recorte de foto quadro a quadro (birefnet, u2net via rembg): o birefnet levou 4 a 8 s por quadro e ~12 GB de
memoria (mais de 10 min por gancho, reprovado pelo usuario), e o u2net deixa pedacos da mesa colados no corpo.
"""
import sys, os, json, time, subprocess, urllib.request
import numpy as np
AW, AH = 540, 960                                           # tamanho em que a mascara e guardada
PW, PH, DR, AQUECE = 1080, 1920, .4, 12                     # tamanho em que o modelo trabalha; passadas de aquecimento no 1o quadro
URL = 'https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_resnet50_fp32.onnx'
MODELO = os.path.join(os.path.expanduser('~/.cache/soft-criativo-entregavel/modelos'), 'rvm_resnet50_fp32.onnx')

def modelo():
    if not os.path.exists(MODELO):
        os.makedirs(os.path.dirname(MODELO), exist_ok=True); print('baixando o modelo de recorte (107 MB)...', flush=True)
        urllib.request.urlretrieve(URL, MODELO + '.part'); os.replace(MODELO + '.part', MODELO)
    return MODELO

def recortar(video, nf, fps=30.0, inicio=0.0):
    """mascaras (nf, 960, 540) uint8 dos quadros de 'video' a partir de 'inicio' (s)."""
    import onnxruntime as ort; from PIL import Image
    ses = ort.InferenceSession(modelo(), providers=['CPUExecutionProvider']); rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
    dr = np.array([DR], np.float32); n = PW * PH * 3; out = np.zeros((nf, AH, AW), np.uint8)
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{inicio:.5f}', '-i', video, '-frames:v', str(nf), '-vf', f'fps={fps},scale={PW}:{PH}',
                            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    for i in range(nf):
        buf = dec.stdout.read(n)
        if len(buf) < n: out[i:] = out[i - 1] if i else 0; break
        src = (np.frombuffer(buf, np.uint8).reshape(PH, PW, 3).astype(np.float32) / 255).transpose(2, 0, 1)[None]
        for _ in range(AQUECE if i == 0 else 1):                   # o modelo tem memoria: sem aquecer, os primeiros quadros saem piores
            _, pha, *rec = ses.run(None, {'src': src, 'r1i': rec[0], 'r2i': rec[1], 'r3i': rec[2], 'r4i': rec[3], 'downsample_ratio': dr})
        out[i] = np.asarray(Image.fromarray((pha[0, 0] * 255).clip(0, 255).astype(np.uint8)).resize((AW, AH), Image.LANCZOS))
    dec.kill(); return out

if __name__ == '__main__':
    proj = os.path.abspath(sys.argv[1]); T = json.load(open(os.path.join(proj, 'tempo.json'), encoding='utf-8')); fps = float(T.get('fps', 30)); r = T['regioes'][0]
    if r['tipo'] != 'avatar': raise SystemExit('o gancho deste criativo nao e do avatar: nada para recortar')
    nf = int(round(r['vdur'] * fps)); t0 = time.time(); alpha = recortar(os.path.join(proj, 'base.mp4'), nf, fps)
    cob = float((alpha > 128).mean())
    np.save(os.path.join(proj, 'gancho_alpha.npy'), alpha); print('ok: gancho_alpha.npy, %d quadros em %.0f s | o avatar ocupa %.0f%% do quadro' % (nf, time.time() - t0, cob * 100))
    if cob < .12 or cob > .75: print('ATENCAO: recorte suspeito (pessoa pequena demais ou fundo nao removido): confira nos quadros antes de renderizar')
