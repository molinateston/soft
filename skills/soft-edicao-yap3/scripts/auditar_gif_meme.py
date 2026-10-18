# Auditoria por vídeo do GIF de meme, depois do verificar_gif.py: PTS do áudio, duração A/V, sincronia do áudio do final
# com o mix da V3 (fora e dentro das janelas de GIF), rosto (YuNet) x borda de baixo do cartão e letra x GIF.
# Uso: python3 auditar_gif_meme.py <plano-gif.json> <pasta_verif> [--mix voz-sfx-v3.wav] [--kg 120] [--yunet modelo.onnx]
#   O mix pode vir do plano (campo "mix", gravado pelo planos_gif_lote.py --mix). Sem mix, a sincronia é pulada e marcada.
# Saída: <pasta_verif>/auditoria.json com veredito APROVADO/REPROVADO.
import os, json, subprocess, argparse
from pathlib import Path
import numpy as np, cv2
YUNET = os.environ.get('YUNET') or str(Path(__file__).resolve().parents[1] / 'assets/modelos/face_detection_yunet_2023mar.onnx')
ap = argparse.ArgumentParser(description='auditoria do final com GIF de meme'); ap.add_argument('plano'); ap.add_argument('verif')
ap.add_argument('--mix'); ap.add_argument('--kg', type=int); ap.add_argument('--yunet', default=YUNET)
ap.add_argument('--caixa-baixo', type=int, default=300, help='BASE_Y do gif_meme.py: borda de baixo do cartão')
A = ap.parse_args()
PL = json.loads(Path(A.plano).read_text()); VF = Path(A.verif)
ARQ, BASE = Path(PL['saida']), Path(PL['base'])
MIX = A.mix or PL.get('mix'); KG = A.kg or PL.get('kg', 120)
TOT = PL.get('quadros') or int(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v', '-count_packets', '-show_entries',
                                                         'stream=nb_read_packets', '-of', 'csv=p=0', str(ARQ)], text=True).strip())
P = PL.get('P')
JAN = [(m['k0'], m['k1']) for m in PL['momentos']]; CAIXA_BAIXO = A.caixa_baixo


def sh(a): return subprocess.run(a, capture_output=True, text=True)


def pts(f, sel):
    o = sh(['ffprobe', '-v', 'error', '-select_streams', sel, '-show_entries', 'packet=pts', '-of', 'csv=p=0', str(f)]).stdout.split()
    return np.array(sorted(int(x) for x in o if x.strip().lstrip('-').isdigit()))


def audio(f, ss, t):
    a = ['ffmpeg', '-v', 'error', '-ss', f'{ss:.4f}', '-t', f'{t:.4f}', '-i', str(f), '-vn', '-ac', '1', '-ar', '48000', '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(a, capture_output=True, check=True).stdout, '<f4')


def atraso(x, y, maxlag=4800):
    n = min(len(x), len(y)); x = x[:n] - x[:n].mean(); y = y[:n] - y[:n].mean()
    c = np.fft.irfft(np.fft.rfft(x, 2 * n) * np.conj(np.fft.rfft(y, 2 * n)))
    c = np.concatenate([c[-maxlag:], c[:maxlag + 1]]); lag = int(np.argmax(c)) - maxlag
    return -lag, float(c.max() / (np.sqrt((x ** 2).sum() * (y ** 2).sum()) + 1e-12))


V = json.loads((VF / 'verificacao.json').read_text())
assert (VF / 'verificacao.json').stat().st_mtime > ARQ.stat().st_mtime, 'verificacao.json é mais antiga que o final: rode verificar_gif.py'
R = dict(arquivo=str(ARQ), base=str(BASE), verificacao=dict(veredito=V['veredito'], falhas=V['falhas'])); falhas = list(V['falhas'])
ap_ = pts(ARQ, 'a'); da = sorted(set(np.diff(ap_).tolist()))
pr = json.loads(sh(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(ARQ)]).stdout)['streams']
dv = float([s for s in pr if s['codec_type'] == 'video'][0]['duration']); dau = float([s for s in pr if s['codec_type'] == 'audio'][0]['duration'])
R['pts'] = dict(video_passos=V.get('pts_passos_video'), audio_passos=da[:5], dif_dur_ms=round((dau - dv) * 1000, 1))
if len(da) != 1: falhas.append(f'salto de PTS no áudio {da[:5]}')
if abs(R['pts']['dif_dur_ms']) > 34: falhas.append('áudio e vídeo com durações diferentes')
# sincronia: o áudio do final no quadro t (>= P) é o mix da V3 no quadro t - P + KG. Dentro de janela de GIF o sting soma, por isso corr >= 0,5.
if MIX and P is not None:
    sinc = []
    for t in sorted({t for t in (400, 1100, 1650, TOT - 120) + tuple(a for a, _ in JAN) if P <= t <= TOT - 90}):
        x = audio(ARQ, t / 30, 3.0); y = audio(MIX, (t - P + KG) / 30, 3.0); lag, cc = atraso(x, y)
        dentro = any(a < t + 90 and t < b for a, b in JAN); sinc.append(dict(quadro=t, janela_gif=dentro, atraso_amostras=lag, corr=round(cc, 3)))
        if abs(lag) > 480 or cc < (0.5 if dentro else 0.8): falhas.append(f'sincronia no quadro {t}: atraso {lag}, corr {cc:.2f}')
    R['sincronia'] = sinc
else:
    R['sincronia'] = 'pulada: sem --mix (ou sem P no plano)'
# rosto x GIF: em cada janela (de 3 em 3 quadros) o topo do rosto tem que ficar abaixo da borda de baixo do cartão
det = cv2.FaceDetectorYN.create(str(A.yunet), '', (540, 960), 0.6, 0.3, 5000); rost = []
for a, b in JAN:
    o = subprocess.run(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-threads', '2', '-ss', f'{a / 30:.6f}', '-i', str(ARQ), '-frames:v', str(b - a),
                        '-vf', 'select=not(mod(n\\,3)),scale=540:960:flags=area,format=bgr24', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-'],
                       capture_output=True, check=True).stdout
    tops = []
    for i in range(len(o) // (540 * 960 * 3)):
        _, fc = det.detect(np.frombuffer(o, np.uint8, 540 * 960 * 3, i * 540 * 960 * 3).reshape(960, 540, 3))
        if fc is not None and len(fc): fc = max(fc, key=lambda q: q[2] * q[3]) * 2; tops.append(float(fc[1]))
    m = dict(janela=[a, b], quadros_com_rosto=len(tops), topo_rosto_min_px=round(min(tops)) if tops else None, borda_gif_px=CAIXA_BAIXO)
    m['folga_px'] = None if not tops else round(min(tops) - CAIXA_BAIXO); rost.append(m)
    if not tops: falhas.append(f'rosto não detectado na janela {a}-{b}')
    elif min(tops) <= CAIXA_BAIXO: falhas.append(f'GIF sobre o rosto na janela {a}-{b} (topo do rosto {min(tops):.0f} px)')
R['rosto_x_gif'] = rost
R['letra_x_gif'] = [dict(janela=j['janela'], letra_coberta_px=j['letra_coberta_px'], folga_cartao_letra_px=j.get('folga_cartao_letra_px')) for j in V['janelas']]
R.update(falhas=falhas, veredito='APROVADO' if not falhas else 'REPROVADO')
(VF / 'auditoria.json').write_text(json.dumps(R, ensure_ascii=False, indent=1))
print(json.dumps(R, ensure_ascii=False, indent=1))
