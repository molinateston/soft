#!/usr/bin/env python3
"""Verificação + auditoria do GIF de meme + som (lê o mesmo plano.json do gif_meme.py e o render.json dele).

Checa: decode limpo, tags HLG/perfil iguais à base, nº de quadros e duração, VPS/SPS/PPS iguais, PTS constante,
pacotes fora das janelas = base (bit a bit), quadros decodificados fora = base, dentro das janelas só a caixa do
cartão muda (PSNR do resto >= 40), letra coberta <= 1 px (máscara de letra branca da base: Y>=880 e croma <=40, nas
colunas do cartão), folga cartão->letra, rosto (YuNet) abaixo do cartão, null test de áudio fora das janelas
<= -30 dB, true peak <= -1 dBTP, sincronia A/V contra a base. Gera mosaico.png (meio de cada GIF, com termo e
fonte) e pop.png (6 quadros da entrada do 1º GIF). Prévia = conferência de layout e cor pelo motor da letra.

Uso: python3 verificar_gif.py   (sem -I: o YuNet usa o cv2 do usuário; o script só lê a base e a saída, não os downloads)
     plano.json pasta_verif [--yunet modelo.onnx]
Grava pasta_verif/verificacao.json com veredito APROVADO/REPROVADO.
"""
import os, sys, json, re, subprocess, argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cor_hlg as C

YUNET = os.environ.get('YUNET') or str(Path(__file__).resolve().parents[1] / 'assets/modelos/face_detection_yunet_2023mar.onnx')
W, H, FS10, YS, CS = C.W, C.H, C.FS10, C.YS, C.CS
ap = argparse.ArgumentParser(); ap.add_argument('plano'); ap.add_argument('verif'); ap.add_argument('--yunet', default=YUNET)
A = ap.parse_args()
PL = json.loads(Path(A.plano).read_text()); RJ = json.loads((Path(PL['trab']) / 'render.json').read_text())
BASE, OUT, T, VF = PL['base'], PL['saida'], Path(PL['trab']), Path(A.verif); VF.mkdir(parents=True, exist_ok=True)
MOM = PL['momentos']; JAN = [(m['k0'], m['k1']) for m in MOM]
CAIXA = {s['k0']: s['caixa'] for s in RJ['segmentos']}          # união das caixas do cartão (x0,y0,x1,y1) por janela
dentro = lambda k: any(a <= k < b for a, b in JAN)


def sh(a): return subprocess.run(a, capture_output=True, text=True)


def pkts(f):
    o = sh(['ffmpeg', '-v', 'error', '-i', str(f), '-map', '0:v', '-c', 'copy', '-f', 'framemd5', '-']).stdout
    return [l.split(',')[-1].strip() for l in o.splitlines() if l and not l.startswith('#')]


def quadros(f, ks):
    ks = sorted(set(ks))
    sel = '+'.join(f'eq(n\\,{k})' for k in ks)
    o = subprocess.run(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-threads', '2', '-i', str(f), '-vf', f"select='{sel}'", '-fps_mode', 'passthrough',
                        '-pix_fmt', 'yuv420p10le', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    assert len(o) == FS10 * len(ks); return {k: o[i * FS10:(i + 1) * FS10] for i, k in enumerate(ks)}


def planos(b):
    Y, U, V = C.yuv_planos(b); return Y.astype(np.int32), C.up_croma(U).astype(np.int32), C.up_croma(V).astype(np.int32)


def dec(args):
    o = subprocess.check_output(['nice', '-n', '10', 'ffmpeg', '-v', 'error'] + args + ['-f', 'f32le', '-ar', '48000', '-ac', '2', '-'])
    return np.frombuffer(o, '<f4').reshape(-1, 2).copy()


def rms(x): return float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))


R = {}; falhas = []
# 1) decode, tags, quadros, duração, extradata, PTS
e = sh(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-threads', '2', '-i', OUT, '-f', 'null', '-'])
R['decode_erros'] = e.stderr.strip()[:300]
if R['decode_erros']: falhas.append('decode com erro: ' + R['decode_erros'])
j = json.loads(sh(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', OUT]).stdout)
jb = json.loads(sh(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', BASE]).stdout)
st = lambda jj, t: [s for s in jj['streams'] if s['codec_type'] == t][0]
v, a, vb = st(j, 'video'), st(j, 'audio'), st(jb, 'video'); TOT = int(vb['nb_read_frames'])
R['video'] = {k: v.get(k) for k in ('codec_name', 'profile', 'pix_fmt', 'width', 'height', 'r_frame_rate', 'color_range', 'color_space', 'color_transfer', 'color_primaries', 'chroma_location', 'nb_read_frames')}
R['audio'] = {k: a.get(k) for k in ('codec_name', 'sample_rate', 'channels', 'bit_rate', 'duration')}
R['duracao'] = dict(final=float(j['format']['duration']), base=float(jb['format']['duration']))
for k in ('color_range', 'color_space', 'color_transfer', 'color_primaries', 'chroma_location', 'profile', 'pix_fmt'):
    if v.get(k) != vb.get(k): falhas.append(f'{k} {v.get(k)} != base {vb.get(k)}')
if v['color_transfer'] != 'arib-std-b67' or v['color_primaries'] != 'bt2020': falhas.append('tags HLG ausentes')
if int(v['nb_read_frames']) != TOT: falhas.append(f"quadros {v['nb_read_frames']} != {TOT}")
if abs(R['duracao']['final'] - R['duracao']['base']) > 1e-3: falhas.append(f"duração {R['duracao']}")
xd = lambda f: sh(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=extradata', '-show_data', '-of', 'json', str(f)]).stdout
xb = xd(BASE); R['extradata_igual_base'] = xd(OUT) == xb
R['extradata_segmentos_igual_base'] = all(xd(T / f'seg-{k0}.mp4') == xb for k0, _ in JAN)
if not R['extradata_igual_base']: falhas.append('extradata (VPS/SPS/PPS) diferente da base')
o = sh(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'packet=pts', '-of', 'csv=p=0', OUT]).stdout.split()
R['pts_passos_video'] = sorted(set(np.diff(sorted(int(x) for x in o)).tolist()))
if len(R['pts_passos_video']) != 1: falhas.append(f"PTS irregular {R['pts_passos_video']}")
o = sh(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'packet=pts', '-of', 'csv=p=0', OUT]).stdout.split()
R['pts_passos_audio'] = sorted(set(np.diff(sorted(int(x) for x in o if x.lstrip('-').isdigit())).tolist()))[:5]
if len(R['pts_passos_audio']) != 1: falhas.append(f"salto de PTS no áudio {R['pts_passos_audio']}")
R['dif_dur_av_ms'] = round((float(a['duration']) - float(v['duration'])) * 1000, 1)
if abs(R['dif_dur_av_ms']) > 34: falhas.append('áudio e vídeo com durações diferentes')
# 2) fora das janelas: pacotes e decodificado iguais à base
pf, pbs = pkts(OUT), pkts(BASE); fora = [k for k in range(TOT) if not dentro(k)]
dif = [k for k in fora if pf[k] != pbs[k]]
R['pacotes'] = dict(fora_das_janelas=len(fora), diferentes=len(dif), primeiros_dif=dif[:10])
if dif: falhas.append(f'{len(dif)} quadros fora das janelas diferentes da base')
amost = sorted({x for a0, b0 in JAN for x in (a0 - 1, b0, b0 + 1)} | {0, TOT // 2, TOT - 1} - {k for k in range(TOT) if dentro(k)})
qa, qb = quadros(OUT, amost), quadros(BASE, amost)
R['decodificado_fora_igual'] = all(qa[k] == qb[k] for k in amost)
if not R['decodificado_fora_igual']: falhas.append('quadro decodificado fora da janela diferente da base')
# 3) dentro das janelas: só o cartão muda; letra da base fica de fora
jan = []
for m in MOM:
    a0, b0 = m['k0'], m['k1']; x0, y0, x1, y1 = CAIXA[a0]; ks = sorted(set(range(a0, b0, 3)) | {b0 - 1})
    qa2, qb2 = quadros(OUT, ks), quadros(BASE, ks); pior = dict(fora=0, letra=0, psnr=99.0, folga=9999)
    for k in ks:
        ya, _, _ = planos(qa2[k]); yb, ub, vb_ = planos(qb2[k]); d = np.abs(ya - yb); mud = d > 120   # mudança estrutural (vazamento do cartão); ruído do reencode crf16 fica < ~80/1023
        cx = np.zeros_like(mud); cx[max(0, y0 - 2):y1 + 2, max(0, x0 - 2):x1 + 2] = True
        letra = (yb >= 880) & (np.abs(ub - 512) <= 40) & (np.abs(vb_ - 512) <= 40); letra[:, :x0] = False; letra[:, x1:] = False; letra[:max(0, y1 - 10)] = False   # letra só existe abaixo do cartão; claro do fundo dentro do cartão não conta
        alt = np.zeros_like(mud); alt[max(0, y0 - 2):y1 + 2, max(0, x0 - 2):x1 + 2] = d[max(0, y0 - 2):y1 + 2, max(0, x0 - 2):x1 + 2] > 8
        lt = np.nonzero(letra[y1:y1 + 400].any(1))[0]; folga = int(lt[0]) if len(lt) else 9999   # 1ª linha de letra abaixo do cartão
        mse = float(np.mean(d[~cx].astype(np.float64) ** 2)); ps = 99.0 if mse == 0 else 10 * np.log10(1023 ** 2 / mse)
        pior = dict(fora=max(pior['fora'], int((mud & ~cx).sum())), letra=max(pior['letra'], int((letra & alt).sum())),
                    psnr=round(min(pior['psnr'], ps), 1), folga=min(pior['folga'], folga))
    jan.append(dict(janela=[a0, b0], dur_s=round((b0 - a0) / 30, 2), caixa=CAIXA[a0], px_mudados_fora_da_caixa=pior['fora'],
                    letra_coberta_px=pior['letra'], psnr_y_resto_min=pior['psnr'], folga_cartao_letra_px=pior['folga']))
R['janelas'] = jan
if any(x['px_mudados_fora_da_caixa'] > 50 for x in jan): falhas.append('mudança fora da caixa do cartão')
if any(x['letra_coberta_px'] > 1 for x in jan): falhas.append('cartão sobre a letra (> 1 px)')
if any(x['psnr_y_resto_min'] < 40 for x in jan): falhas.append('PSNR fora do cartão baixo')
if not 3 <= len(MOM) <= 5: falhas.append(f'{len(MOM)} GIFs (o padrão é 3 a 5)')
if any(not 1 <= x['dur_s'] <= 2.5 for x in jan): falhas.append('GIF fora de 1 a 2,5 s')
# 4) rosto (YuNet) abaixo do cartão
try:
    import cv2
    if not Path(A.yunet).is_file(): raise ImportError('modelo YuNet ausente: passe --yunet ou YUNET=')
    det = cv2.FaceDetectorYN.create(A.yunet, '', (540, 960), 0.6, 0.3, 5000); rost = []
    for m in MOM:
        a0, b0 = m['k0'], m['k1']; yb1 = CAIXA[a0][3]
        o = subprocess.run(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-threads', '2', '-ss', f'{a0 / 30:.6f}', '-i', OUT, '-frames:v', str(b0 - a0),
                            '-vf', 'select=not(mod(n\\,3)),scale=540:960:flags=area,format=bgr24', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-'],
                           capture_output=True, check=True).stdout
        tops = []
        for i in range(len(o) // (540 * 960 * 3)):
            _, fc = det.detect(np.frombuffer(o, np.uint8, 540 * 960 * 3, i * 540 * 960 * 3).reshape(960, 540, 3))
            if fc is not None and len(fc): tops.append(float(max(fc, key=lambda q: q[2] * q[3])[1] * 2))
        rost.append(dict(janela=[a0, b0], quadros_com_rosto=len(tops), topo_rosto_min_px=round(min(tops)) if tops else None, base_cartao_px=yb1))
        if not tops: falhas.append(f'rosto não detectado na janela {a0}-{b0}')
        elif min(tops) <= yb1: falhas.append(f'cartão sobre o rosto na janela {a0}-{b0}')
    R['rosto_x_cartao'] = rost
except ImportError:
    R['rosto_x_cartao'] = 'cv2 ou modelo YuNet indisponível; conferir rosto x cartão no mosaico'
# 5) áudio: null test, true peak, sincronia com a base
fin = dec(['-i', OUT, '-vn']); base = dec(['-i', BASE, '-vn']); fx = np.load(T / 'fx.npy'); n = min(len(fin), len(base))
if len(fin) != len(base): falhas.append(f'áudio com {len(fin)} amostras != base {len(base)}')
res = fin[:n] - base[:n]; mj = np.zeros(n, bool)
for a0, _ in JAN:
    s = round(a0 / 30 * 48000); mj[max(0, s - 2400):s + round(1.7 * 48000) + 2400] = True
db = lambda x: 20 * np.log10(max(rms(x), 1e-12))
R['null_test'] = dict(fora_rel_voz_db=round(db(res[~mj]) - db(base[:n][~mj]), 1), corr_res_sfx_dentro=round(float(np.corrcoef(res[mj].ravel(), fx[:n][mj].ravel())[0, 1]), 4))
if R['null_test']['fora_rel_voz_db'] > -30: falhas.append(f"null test fora das janelas {R['null_test']['fora_rel_voz_db']} dB")
if R['null_test']['corr_res_sfx_dentro'] < 0.9: falhas.append('sons dos GIFs não batem com o esperado')
lo = sh(['ffmpeg', '-hide_banner', '-nostats', '-i', OUT, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-']).stderr
lb = sh(['ffmpeg', '-hide_banner', '-nostats', '-i', BASE, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-']).stderr
tp = lambda s: float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', s)[-1]); il = lambda s: float(re.findall(r'I:\s+(-?[\d.]+) LUFS', s)[-1])
R['loudness'] = dict(final_lufs=il(lo), base_lufs=il(lb), final_tp=tp(lo), base_tp=tp(lb))
if R['loudness']['final_tp'] > -1.0: falhas.append(f"true peak {R['loudness']['final_tp']} dBTP")
sinc = []
perto = lambda t: any(a0 * 1600 < round(t / 30 * 48000) + 144000 and round(t / 30 * 48000) < round(a0 / 30 * 48000) + round(1.7 * 48000) + 2400 for a0, _ in JAN)
for t in sorted({TOT // 5, TOT // 2, 4 * TOT // 5} | {a0 for a0, _ in JAN}):
    s = round(t / 30 * 48000); x = fin[s:s + 144000].mean(1); y = base[s:s + 144000].mean(1); m_ = min(len(x), len(y))
    x, y = x[:m_] - x[:m_].mean(), y[:m_] - y[:m_].mean(); L = 4800
    c = np.fft.irfft(np.fft.rfft(x, 2 * m_) * np.conj(np.fft.rfft(y, 2 * m_))); c = np.concatenate([c[-L:], c[:L + 1]])
    lag = int(np.argmax(c)) - L; cc = float(c.max() / (np.sqrt((x ** 2).sum() * (y ** 2).sum()) + 1e-12))
    sinc.append(dict(quadro=t, janela=perto(t), atraso_amostras=lag, corr=round(cc, 3)))
    if abs(lag) > 480 or cc < (0.5 if perto(t) else 0.95): falhas.append(f'sincronia no quadro {t}: atraso {lag}, corr {cc:.2f}')
R['sincronia_vs_base'] = sinc
# 6) mosaico (meio de cada GIF) e pop.png (entrada do 1º GIF, recorte 1:1 do topo)
try: fo = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 19); fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
except Exception: fo = fb = ImageFont.load_default()
prev = lambda b: Image.fromarray(C.preview_de_buf(b)).crop((0, 0, 1080, 1000)).resize((540, 500), Image.LANCZOS)
meio = [(a0 + b0) // 2 for a0, b0 in JAN]; qm = quadros(OUT, meio)
mos = Image.new('RGB', (540 * len(MOM), 590), (20, 20, 20)); dr = ImageDraw.Draw(mos)
for i, (m, k) in enumerate(zip(MOM, meio)):
    mos.paste(prev(qm[k]), (540 * i, 90)); x = 540 * i + 8
    dr.text((x, 4), f"{k / 30:.2f}s  \"{m['palavra']}\" ({m.get('sentido', '')})", fill=(240, 240, 240), font=fb)
    dr.text((x, 34), f"{m['fonte']}: \"{m['termo']}\"  som: {m['som']}", fill=(200, 200, 200), font=fo)
    dr.text((x, 58), m['titulo'][:46], fill=(170, 170, 170), font=fo)
mos.save(VF / 'mosaico.png')
m0 = MOM[0]; kt = [m0['k0'] + i for i in range(6)]; qt = quadros(OUT, kt); x0, y0, x1, y1 = CAIXA[m0['k0']]
cw = x1 - x0 + 40; pop = Image.new('RGB', (cw * 3, 2 * 400), (20, 20, 20)); dr = ImageDraw.Draw(pop)
for i, k in enumerate(kt):
    pop.paste(Image.fromarray(C.preview_de_buf(qt[k])).crop((x0 - 20, 0, x1 + 20, 380)), (cw * (i % 3), 400 * (i // 3) + 20))
    dr.text((cw * (i % 3) + 6, 400 * (i // 3)), f'q{k}', fill=(255, 255, 0), font=fo)
pop.save(VF / 'pop.png')
R.update(falhas=falhas, veredito='APROVADO' if not falhas else 'REPROVADO')
(VF / 'verificacao.json').write_text(json.dumps(R, ensure_ascii=False, indent=1, default=str))
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
