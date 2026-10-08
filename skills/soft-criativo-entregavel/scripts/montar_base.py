"""Monta a base do criativo: base.mp4 (video do avatar onde ele fala, preto no resto, e toda a voz ja no tempo final) e tempo.json.
    python montar_base.py <pasta_do_criativo>
Le projeto.json:
    audio          caminho do audio completo do criativo
    avatar         "gancho+cta" | "gancho" | "nenhum"
    gancho_fim     segundo do audio em que o gancho (frase + alivio) termina
    cta_inicio     segundo do audio em que o CTA comeca
    audio_fim      (opcional) corta o audio aqui (resto de fala solto no fim)
    K              aceleracao da voz do audio (1.0 = sem acelerar)
    avatar_video   arquivo do avatar gerado (padrao avatar_raw.mp4)
    palavras       {"ultima_gancho": "...", "primeira_cta": "..."}  (so no modo gancho+cta: onde separar as duas falas do avatar)
    fim_parado     segundos de quadro parado no fim (padrao 0.7 com avatar no CTA, 1.0 sem)
    gancho_inteiro padrao true: o gancho do avatar entra inteiro, sem cortar os silencios (do comeco da fala, contando interjeicao
                   curta como "O", ate o fim). O avatar aparece recortado sobre um fundo parado, e corte seco ali viraria um salto.
                   false = corta os silencios acima de 0,35 s (modo antigo, com o fundo do quarto)
    recortar_avatar padrao true: no fim, grava gancho_alpha.npy (mascara do avatar em cada quadro do gancho; ~10 s, sem creditos)
O que faz:
  - corta as pausas da voz do audio (>= 0,28 s viram ~0,16 s) nos trechos que continuam na voz original;
  - no clipe do avatar: confere as palavras, acha a divisa gancho/CTA pela transcricao, corta os silencios que o modelo deixa
    (com leve aproximacao em trechos alternados), nivela o volume com a voz do audio e tira ruido de fundo;
  - avisa se a fala do avatar encosta no fim do clipe (ultima palavra cortada) ou se faltou alguma palavra.
"""
import sys, os, re, json, subprocess, unicodedata
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import align_voice as A, transcribe as T
from scipy.signal import butter, sosfiltfilt

FPS = 30
MIN_GAP, PRE, POST = .28, .08, .08                      # voz do audio: pausa minima para cortar; folga antes/depois da fala
LEAD_H, TAIL_H, LEAD_C, TAIL_C = .30, .22, .15, .40     # avatar: folgas antes/depois das falas
MAXGAP, KEEP_A, KEEP_B = .35, .10, .12                  # avatar: silencio maximo dentro da fala; folgas do corte

def _env(x, sr):
    y = sosfiltfilt(butter(4, [150, 3000], btype='band', fs=sr, output='sos'), x); hop = int(.005 * sr)
    env = np.array([np.sqrt(np.mean(y[i:i + hop * 4] ** 2)) for i in range(0, len(y) - hop * 4, hop)])
    env = np.convolve(env, np.ones(5) / 5, 'same'); return env / env.max(), np.arange(len(env)) * .005

def voiced(x, sr, thr=.045, join=.10, minlen=.0):
    env, t = _env(x, sr); segs = []; s = None
    for i, a in enumerate(env > thr):
        if a and s is None: s = i
        if not a and s is not None:
            if t[i] - t[s] > .05: segs.append([float(t[s]), float(t[i])])
            s = None
    if s is not None: segs.append([float(t[s]), float(t[-1])])
    m = [segs[0][:]]
    for a, b in segs[1:]:
        if a - m[-1][1] < join: m[-1][1] = b
        else: m.append([a, b])
    return ([iv for iv in m if iv[1] - iv[0] > minlen] or m), (env, t)

_REC = None
def tr(x, sr, a, b):
    global _REC
    if _REC is None:
        import sherpa_onnx
        d = T.ensure_model()
        _REC = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d + '/small-encoder.int8.onnx', decoder=d + '/small-decoder.int8.onnx', tokens=d + '/small-tokens.txt', language='pt', task='transcribe', num_threads=6)
    st = _REC.create_stream(); st.accept_waveform(sr, x[int(max(0, a) * sr):int(b * sr)]); _REC.decode_stream(st); return st.result.text.strip()

def norm(s): return re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode())

def boundary(x, sr, env_t, h0, c1, last_hook, first_cta):
    """divisa gancho/CTA na fala do avatar: primeiro instante em que a ultima palavra do gancho ja foi dita e depois o primeiro
    em que a primeira palavra do CTA aparece; o corte fica no ponto de menor energia entre os dois."""
    env, t = env_t; lh, fc = norm(last_hook), norm(first_cta)
    def has(e, both):
        w = norm(tr(x, sr, h0 - .2, e)).split(); return lh in w and (not both or fc in w[w.index(lh) + 1:])
    def first(e, both):
        while e <= c1 + .05 and not has(e, both): e += .15
        if e > c1 + .05: return None
        f = e - .15
        while f < e and not has(f, both): f += .05
        return f
    e1 = first(h0 + 1.0, False)
    if e1 is None: raise SystemExit('nao achei a ultima palavra do gancho ("%s") na fala do avatar: conferir a transcricao acima' % last_hook)
    e2 = first(e1, True) or min(c1, e1 + .5); e2 = max(e2, e1 + .1); a, b = int((e1 - .05) / .005), int(e2 / .005)
    return float(t[a + int(np.argmin(env[a:b]))])

def meanvol(path):
    o = subprocess.run(['ffmpeg', '-i', path, '-af', 'volumedetect', '-vn', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float([l for l in o.splitlines() if 'mean_volume' in l][0].split('mean_volume:')[1].split('dB')[0])

def keep_voice(fine, a, b):
    """trechos da voz do audio mantidos entre a e b (pausas >= MIN_GAP cortadas)."""
    sp = [[max(s, a), min(e, b)] for s, e in fine if e > a + .02 and s < b - .02]
    if not sp: return [[a, b]]
    m = [sp[0][:]]
    for s, e in sp[1:]:
        if s - m[-1][1] < MIN_GAP: m[-1][1] = e
        else: m.append([s, e])
    out = []
    for s, e in m:
        s = max(a, s - PRE); e = min(b, e + POST)
        if out and s <= out[-1][1]: out[-1][1] = e
        else: out.append([round(s, 3), round(e, 3)])
    return out

def pieces(fine, a, b, lead):
    """trechos mantidos da fala do avatar entre a e b: silencios maiores que MAXGAP viram um respiro curto (corte seco)."""
    sp = [[max(s, a), min(e, b)] for s, e in fine if e > a + .02 and s < b - .02]; out = [[max(0.0, sp[0][0] - lead), sp[0][1]]]
    for s, e in sp[1:]:
        if s - out[-1][1] > MAXGAP: out[-1][1] += KEEP_A; out.append([s - KEEP_B, e])
        else: out[-1][1] = e
    return out

if __name__ == '__main__':
    proj = os.path.abspath(sys.argv[1]); P = json.load(open(os.path.join(proj, 'projeto.json'), encoding='utf-8')); os.chdir(proj)
    audio = P['audio']; K = float(P.get('K', 1.0)); mode = P.get('avatar', 'gancho+cta')
    x, sr = A.load(audio); x = x.copy(); adur = min(len(x) / sr, P.get('audio_fim') or 1e9); gf = float(P['gancho_fim']); ci = float(P['cta_inicio'])
    fine, _ = voiced(x, sr)
    av_hook = mode in ('gancho+cta', 'gancho'); av_cta = mode == 'gancho+cta'
    # ---- avatar
    hp = cp = None; gain = 0.0
    if av_hook:
        av = P.get('avatar_video', 'avatar_raw.mp4'); afine, env_t = voiced(*A.load(av), minlen=.35); ax, _ = A.load(av); ax = ax.copy(); adur_v = len(ax) / sr
        h0, c1 = afine[0][0], afine[-1][1]
        print('AVATAR | trechos de fala:', [[round(a, 2), round(b, 2)] for a, b in afine], '| clipe %.2f s' % adur_v)
        print('AVATAR | fala completa:', tr(ax, sr, 0, adur_v))
        sil = [round(afine[i + 1][0] - afine[i][1], 2) for i in range(len(afine) - 1)]
        print('AVATAR | comeca a falar aos %.2f s | silencios internos %s | sobra no fim %.2f s' % (h0, sil, adur_v - c1))
        if adur_v - c1 < .12 and np.sqrt((ax[-int(.12 * sr):] ** 2).mean()) > .01:
            print('ATENCAO: a fala do avatar encosta no fim do clipe: a ultima palavra pode ter sido cortada (ouvir; se cortou, gerar de novo com mais folga)')
        if av_cta:
            cut = boundary(ax, sr, env_t, h0, c1, P['palavras']['ultima_gancho'], P['palavras']['primeira_cta'])
            print('AVATAR | gancho ate %.2f s: %s' % (cut, tr(ax, sr, h0 - .2, cut))); print('AVATAR | CTA de %.2f s:    %s' % (cut, tr(ax, sr, cut, adur_v)))
            hend = max(e for s_, e in afine if s_ < cut); cst = min([s_ for s_, e in afine if e > cut and s_ >= cut - .05] or [cut])
            hp = pieces(afine, 0, cut, LEAD_H); hp[-1][1] = min(cut, hend + TAIL_H)
            cp = pieces(afine, cut, adur_v, 0); cp[0][0] = max(cut, cst - LEAD_C); cp[-1][1] = min(adur_v, c1 + TAIL_C); lead = round(max(.2, cst - cp[0][0]) + .25, 3)
        else:
            hp = pieces(afine, 0, adur_v, LEAD_H); hp[-1][1] = min(adur_v, c1 + TAIL_H)
        w = norm(tr(ax, sr, 0, adur_v)).split(); lh = norm(P['palavras']['ultima_gancho']) if av_cta else None   # palavras do gancho, pela fala completa
        nw = len(w) if not av_cta else (w.index(lh) + 1 if lh in w else len(norm(tr(ax, sr, 0, cut)).split()))
        wps = nw / max(.1, (hend if av_cta else c1) - h0)
        print('AVATAR | ritmo do gancho: %.1f palavras/s%s' % (wps, '  <- LENTO: abaixo de 2,3 o gancho soa arrastado (clipe longo demais para a fala)' if wps < 2.3 else ''))
        if P.get('gancho_inteiro', True): hp = [[max(0.0, voiced(ax, sr)[0][0][0] - LEAD_H), hp[-1][1]]]   # gancho sem cortes: do comeco da fala (qualquer som) ao fim
        sp = np.concatenate([ax[int(a * sr):int(b * sr)] for a, b in afine])
    # ---- regioes
    fr = lambda iv: int(round((iv[1] - iv[0]) * FPS))
    hold = float(P.get('fim_parado', .7 if av_cta else 1.0)); holdf = int(round(hold * FPS)); regs = []; v = 0
    def voz(nome, a, b, extra=0):
        global v
        man = keep_voice(fine, a, b); n = int(round(sum(e - s for s, e in man) / K * FPS)) + extra
        regs.append(dict(nome=nome, tipo='voz', c0=a, c1=b, v0=v / FPS, vdur=n / FPS, manter=man, quadros=n)); v += n
    def avatar(nome, a, b, pcs, extra=0, lead=None):
        global v
        n = sum(fr(iv) for iv in pcs) + extra; r = dict(nome=nome, tipo='avatar', c0=a, c1=b, v0=v / FPS, vdur=n / FPS, manter=[], quadros=n, pedacos=pcs)
        if lead is not None: r['lead'] = lead
        regs.append(r); v += n
    if av_hook: avatar('gancho', 0.0, gf, hp)
    else: voz('gancho', 0.0, gf)
    if av_cta: voz('corpo', gf, ci); avatar('cta', ci, adur, cp, holdf, lead)
    else: voz('corpo', gf, ci); voz('cta', ci, adur, holdf)
    # ---- nivel do avatar pela voz do audio
    if av_hook:
        body = [r for r in regs if r['tipo'] == 'voz']; bx = np.concatenate([x[int(a * sr):int(b * sr)] for r in body for a, b in r['manter']])
        gain = float(20 * np.log10(np.sqrt((bx ** 2).mean())) - 20 * np.log10(np.sqrt((sp ** 2).mean())))
        print('AVATAR | ganho aplicado no audio dele: %+.1f dB (para igualar a voz do audio)' % gain)
    # ---- ffmpeg: um trecho por pedaco, concatenados
    f = []; lab = []; n = 0; avin = 1
    for r in regs:
        last = r is regs[-1]
        if r['tipo'] == 'avatar':
            for i, (a, b) in enumerate(r['pedacos']):
                nf_ = fr((a, b)) + (holdf if (last and i == len(r['pedacos']) - 1) else 0)
                z = ',crop=iw/1.06:ih/1.06:(iw-iw/1.06)/2:(ih-ih/1.06)*0.35' if i % 2 else ''
                f.append(f'[{avin}:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS,fps={FPS}{z},scale=1080:1920:flags=lanczos,setsar=1,tpad=stop_mode=clone:stop_duration=2,trim=end_frame={nf_}[v{n}];'
                         f'[{avin}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={max(0, b - a - .03):.3f}:d=0.03,'
                         f'afftdn=nr=10:nf=-48,volume={gain:.2f}dB,alimiter=limit=0.95,apad,atrim=end={nf_ / FPS:.5f}[a{n}]')
                lab.append(f'[v{n}][a{n}]'); n += 1
        else:
            parts = ''.join(f'[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS[k{n}_{j}];' for j, (a, b) in enumerate(r['manter']))
            cat = ''.join(f'[k{n}_{j}]' for j in range(len(r['manter'])))
            f.append(parts + f'{cat}concat=n={len(r["manter"])}:v=0:a=1,atempo={K},apad,atrim=end={r["quadros"] / FPS:.5f}[a{n}];color=c=black:s=1080x1920:r={FPS},trim=end_frame={r["quadros"]},setsar=1[v{n}]')
            lab.append(f'[v{n}][a{n}]'); n += 1
    open('base_filtro.txt', 'w').write(';'.join(f) + ';' + ''.join(lab) + f'concat=n={n}:v=1:a=1[v][a]')
    ins = ['-i', audio] + (['-i', P.get('avatar_video', 'avatar_raw.mp4')] if av_hook else [])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-/filter_complex', 'base_filtro.txt', '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', 'base.mp4'], check=True)
    for r in regs: r.pop('quadros', None)
    json.dump(dict(fps=FPS, K=K, dur=v / FPS, modo=mode, ganho_avatar=gain, regioes=regs), open('tempo.json', 'w', encoding='utf-8'), indent=1)
    print('\nLINHA DO TEMPO (video %.2f s):' % (v / FPS))
    for r in regs: print('  %-7s %-6s audio %6.2f-%6.2f s -> video %6.2f-%6.2f s' % (r['nome'], r['tipo'], r['c0'], r['c1'], r['v0'], r['v0'] + r['vdur']))
    # ---- conferencia do que ficou na base
    bx_, _ = A.load('base.mp4'); bx_ = bx_.copy()
    for r in regs:
        if r['tipo'] == 'avatar': print('CONFERENCIA | %s (avatar) na base: %s' % (r['nome'], tr(bx_, sr, r['v0'], r['v0'] + r['vdur'])))
    body = [r for r in regs if r['nome'] == 'corpo'][0]
    print('CONFERENCIA | comeco do corpo: %s' % tr(bx_, sr, body['v0'], body['v0'] + 4)); print('CONFERENCIA | fim do corpo:    %s' % tr(bx_, sr, body['v0'] + body['vdur'] - 4, body['v0'] + body['vdur']))
    # ---- recorte do avatar no gancho: ele aparece sem o fundo, sobre o print da 1a tela do corpo (kit.py, gancho_sobre_material)
    if av_hook and P.get('recortar_avatar', True):
        try:
            import recortar_avatar as RA
            nfg = int(round(regs[0]['vdur'] * FPS)); al = RA.recortar('base.mp4', nfg, FPS); np.save('gancho_alpha.npy', al); cob = 100 * float((al > 128).mean())
            print('RECORTE | gancho_alpha.npy: %d quadros, o avatar ocupa %.0f%% do quadro%s' % (nfg, cob, '  <- SUSPEITO: confira nos quadros' if cob < 12 or cob > 75 else ''))
        except Exception as e:
            print('ATENCAO: nao consegui recortar o avatar (%s). Instale com "uv pip install onnxruntime" e rode recortar_avatar.py, ou use "gancho_sobre_material": false no roteiro.' % e)
