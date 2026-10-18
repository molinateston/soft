# Mede o rosto (caixa, olhos, nariz, cantos da boca) com YuNet local, sem rede, em coordenadas 1080x1920.
# Uso: python3 rosto.py video.mp4 saida.json [--passo 3] [--espelho] [--yunet modelo.onnx]
# Saída: lista de {k, rosto:[x,y,w,h] ou None, olho_d, olho_e, nariz, boca_d, boca_e, conf}, um item a cada <passo> quadros.
import json, os, subprocess, argparse
from pathlib import Path
import numpy as np, cv2
YUNET = os.environ.get('YUNET') or str(Path(__file__).resolve().parents[1] / 'assets/modelos/face_detection_yunet_2023mar.onnx')
ap = argparse.ArgumentParser(description='rosto por quadro com YuNet (1080x1920)')
ap.add_argument('video'); ap.add_argument('saida'); ap.add_argument('--passo', type=int, default=3)
ap.add_argument('--espelho', action='store_true', help='espelha a imagem antes de medir (para o corpo espelhado)')
ap.add_argument('--yunet', default=YUNET)
A = ap.parse_args()
w, h = 540, 960
det = cv2.FaceDetectorYN.create(A.yunet, '', (w, h), 0.6, 0.3, 5000)
vf = f"select='not(mod(n,{A.passo}))',scale={w}:{h}:flags=area" + (',hflip' if A.espelho else '') + ',format=bgr24'
p = subprocess.Popen(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-threads', '2', '-i', A.video, '-vf', vf, '-fps_mode', 'passthrough',
                      '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
res = []; k = 0
while True:
    b = p.stdout.read(w * h * 3)
    if len(b) < w * h * 3: break
    _, f = det.detect(np.frombuffer(b, np.uint8).reshape(h, w, 3))
    if f is None or len(f) == 0: res.append(dict(k=k, rosto=None))
    else:
        f = max(f, key=lambda r: r[2] * r[3]) * 2
        pts = f[4:14].reshape(5, 2)
        res.append(dict(k=k, rosto=[round(float(v)) for v in f[:4]], olho_d=pts[0].round().tolist(), olho_e=pts[1].round().tolist(),
                        nariz=pts[2].round().tolist(), boca_d=pts[3].round().tolist(), boca_e=pts[4].round().tolist(), conf=round(float(f[14] / 2), 3)))
    k += A.passo
p.wait()
Path(A.saida).write_text(json.dumps(res))
print(A.saida, len(res), sum(r['rosto'] is None for r in res), 'sem rosto')
