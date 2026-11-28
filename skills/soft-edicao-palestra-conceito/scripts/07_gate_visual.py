"""Etapa 7b. Gate visual e tecnico do final.mp4.
confere: 1080x1920, 30 fps, 1 trilha de video e 1 de audio; duracao >= duracao_min_s (dispensado com --prova) e igual
ao plano; velocidade = marca; sem cor proibida em nenhum pixel das tarjas; tarjas so com cores da paleta (e as
misturas de borda entre elas); headline, desenhos e legenda dentro da area segura; legenda fixa na faixa do video;
video sem congelar (freezedetect na faixa do palestrante); audio nao mudo.
uso: python3 07_gate_visual.py TRAB [--prova]      saida: gate-visual.json
criterio de pronto: PRONTO, exit 0."""
import json, os, re, subprocess, sys
import numpy as np
import comum as C

T = C.trab_arg()
PROVA = '--prova' in sys.argv
M, CC, RL = C.marca(T), C.lj(T, 'cortes.json'), C.lj(T, 'render-log.json')
FIN = os.path.join(T, 'final.mp4')
f, av = [], []
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', FIN]))
vs = [s for s in pr['streams'] if s['codec_type'] == 'video']; au = [s for s in pr['streams'] if s['codec_type'] == 'audio']
if len(vs) != 1 or len(au) != 1: f.append(f'{len(vs)} trilhas de video e {len(au)} de audio (esperado 1 e 1)')
v = vs[0]
if (v['width'], v['height']) != (C.W, C.H): f.append(f"tamanho {v['width']}x{v['height']}")
if abs(eval(v['r_frame_rate']) - C.FPS) > 0.01: f.append(f"fps {v['r_frame_rate']}")
dur = float(pr['format']['duration'])
mn = float(M['duracao_min_s'])
if dur < mn - 0.05: (av if PROVA else f).append(f'duracao {dur:.2f} s < {mn:.0f} s' + (' (prova)' if PROVA else ''))
alvo = RL['dur'] if RL.get('parcial') else CC['dur_saida']
if abs(dur - alvo) > 0.1: f.append(f'duracao {dur:.2f} s diferente do plano {alvo:.2f} s')
if abs(CC['velocidade'] - float(M['velocidade'])) > 1e-6: f.append(f"velocidade {CC['velocidade']} diferente da marca {M['velocidade']}")
fonte = sum(b - a for a, b in CC['keep'])
if not RL.get('parcial') and abs(fonte / CC['velocidade'] - dur) > 0.15: f.append(f'fonte usada {fonte:.2f} s / {CC["velocidade"]} nao bate com {dur:.2f} s')
if M.get('musica') is False and len(au) > 1: f.append('mais de uma trilha de audio (musica proibida)')

# ---------- cores ----------
pal = np.array([C.rgb(x) for x in M['paleta']], float)
proib = np.array([C.rgb(x) for x in M.get('cores_proibidas', [])], float).reshape(-1, 3)
seg = [(pal[i], pal[j]) for i in range(len(pal)) for j in range(i + 1, len(pal))]


def dist_paleta(px):
    d = np.full(len(px), 1e9)
    for a, b in seg:
        ab = b - a; t = np.clip(((px - a) @ ab) / (ab @ ab), 0, 1)
        d = np.minimum(d, np.linalg.norm(px - (a + t[:, None] * ab), axis=1))
    return d


n = int(dur)
raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', FIN, '-vf', 'fps=1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
frames = np.frombuffer(raw, np.uint8).reshape(-1, C.H, C.W, 3)
fora_pal, prob_t, prob_v = [], 0, 0
for k, fr in enumerate(frames):
    tar = np.concatenate([fr[:C.YV].reshape(-1, 3), fr[C.YB:].reshape(-1, 3)]).astype(float)[::7]
    vid = fr[C.YV:C.YB].reshape(-1, 3).astype(float)[::7]
    for p in proib:
        prob_t += int((np.linalg.norm(tar - p, axis=1) < 30).sum()); prob_v += int((np.linalg.norm(vid - p, axis=1) < 30).sum())
    fora_pal.append(float((dist_paleta(tar) > 45).mean()))
if prob_t: f.append(f'cor proibida {M["cores_proibidas"]} em {prob_t} pixels amostrados das tarjas')
if prob_v: av.append(f'cor parecida com a proibida em {prob_v} pixels do video (roupa/cenario? confira)')
pior = max(fora_pal) if fora_pal else 0
if pior > 0.003: f.append(f'tarjas com {pior:.2%} de pixels fora da paleta no pior quadro (s {int(np.argmax(fora_pal))})')

# ---------- area segura e legenda ----------
z = M['area_segura']; mx = z['margem_x']
hb = RL['headline']['bbox']
if hb[1] < z['topo_y_min']: f.append(f"headline comeca em y {hb[1]} (< {z['topo_y_min']}, interface do Instagram)")
if hb[0] < mx or hb[2] > C.W - mx: f.append(f'headline fora da margem lateral: x {hb[0]}-{hb[2]}')
if hb[3] > C.YV: f.append(f'headline invade o video: y {hb[3]} > {C.YV}')
for cid, b in RL['desenhos'].items():
    if b[0] < mx - 8 or b[2] > C.W - mx + 8: f.append(f'desenho {cid} fora da margem lateral: x {b[0]}-{b[2]}')
    if b[3] > z['desenho_y_max'] + 4: f.append(f"desenho {cid} desce ate y {b[3]} da tarja (max {z['desenho_y_max']})")
if RL['cap_y'] != C.CAP_Y: f.append(f"legenda em y {RL['cap_y']} (fixa em {C.CAP_Y})")
ly = RL['legenda_bbox_y']
if ly[0] < C.YV or ly[1] > C.YB: f.append(f'legenda fora da faixa do video: y {ly}')
lx = RL['legenda_x']
if lx[1] and (lx[0] < mx or lx[1] > C.W - mx): f.append(f'palavra de legenda larga demais: x {lx[0]}-{lx[1]}')

# ---------- congelamento e audio ----------
r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', FIN, '-vf', f'crop={C.WV}:{C.HV}:0:{C.YV},freezedetect=n=-55dB:d=2',
                    '-an', '-f', 'null', '-'], capture_output=True, text=True)
fz = re.findall(r'freeze_start: ([\d.]+)', r.stderr)
if fz: f.append(f'video congelado a partir de {fz} s')
r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', FIN, '-vn', '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True)
m = re.search(r'mean_volume: ([-\d.]+)', r.stderr)
if not m or float(m.group(1)) < -40: f.append(f'audio quase mudo ({m.group(1) if m else "?"} dB)')
C.gj(T, 'gate-visual.json', dict(dur=round(dur, 3), falhas=f, avisos=av, fora_paleta_pior=pior))
print(f'final {dur:.2f} s | {v["width"]}x{v["height"]} | quadros amostrados {len(frames)} | fora da paleta pior {pior:.3%}')
for x in av: print('ATENCAO', x)
for x in f: print('FALHA', x)
print('PRONTO' if not f else 'NAO PRONTO')
sys.exit(1 if f else 0)
