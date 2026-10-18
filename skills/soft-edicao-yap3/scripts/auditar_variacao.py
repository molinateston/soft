# Auditoria de uma variação de gancho (normal ou espelho) gerada pelo variar_gancho.py, lendo o mesmo plano JSON.
# Generalizado de 2026-10-16-variacoes-ep3-ep4-yap3/scripts/auditar.py (e da cópia letra branca). Segue "Conferências técnicas antes de entregar".
#
# Uso:
#   python3 auditar_variacao.py plano.json arquivo.mp4 [--espelho] [--verif pasta]
# Gera <verif>/<arquivo>.json e <verif>/<arquivo>-mosaico.png e imprime o veredito (APROVADO/REPROVADO). Sai com código 1 se reprovar.
# Checagens: ffprobe (HEVC 1080x1920 30 fps, cor igual à fonte do corpo, áudio presente, <= 300 MB), decode sem erro, contagem de quadros,
# PTS em passo constante, durações A/V, sincronia do corpo (0.15/0.5/0.85) contra o "mix" da V3, true peak <= -1 dBTP,
# pacotes do corpo idênticos à fonte copiada (framemd5), cor/PSNR contra a fonte do corpo e da ponte, rosto x legenda e título x olhos no gancho,
# nível da letra (graf_branco 1000 => miolo da letra perto de Y 940 em 10 bits), mosaico com quadros-chave e recortes 4:5 e 3:4.
import sys, json, re, subprocess, hashlib, argparse
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import cor_hlg as N
from variar_gancho import carregar_plano, sufixo
W, H = N.W, N.H; YS = W * H; FS10 = N.FS10


def sh(a, **k): return subprocess.run(a, capture_output=True, text=True, **k)


def probe(f):
    j = json.loads(sh(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(f)]).stdout)
    return {s['codec_type']: s for s in j['streams']}, j['format']


def pts(f, sel):
    o = sh(['ffprobe', '-v', 'error', '-select_streams', sel, '-show_entries', 'packet=pts', '-of', 'csv=p=0', str(f)]).stdout.split()
    return np.array(sorted(int(x.split(',')[0]) for x in o if x.split(',')[0] not in ('', 'N/A')))


def pkt_md5(f):
    o = sh(['ffmpeg', '-v', 'error', '-i', str(f), '-map', '0:v', '-c', 'copy', '-f', 'framemd5', '-']).stdout
    return [l.split(',')[-1].strip() for l in o.splitlines() if l and not l.startswith('#')]


def quadros(f, ks):
    ks = sorted(set(ks)); sel = '+'.join(f'eq(n\\,{k})' for k in ks)
    o = subprocess.run(['ffmpeg', '-v', 'error', '-threads', '2', '-i', str(f), '-vf', f"select='{sel}'", '-fps_mode', 'passthrough',
                        '-pix_fmt', 'yuv420p10le', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    assert len(o) == FS10 * len(ks), (f, len(o) / FS10, len(ks))
    return {k: o[i * FS10:(i + 1) * FS10] for i, k in enumerate(ks)}


def planos(b):
    a = np.frombuffer(b, '<u2'); return a[:YS].reshape(H, W), a[YS:YS + YS // 4].reshape(H // 2, W // 2), a[YS + YS // 4:].reshape(H // 2, W // 2)


def medias(b): return [float(p.mean()) for p in planos(b)]


def psnr_y(a, b):
    m = np.mean((planos(a)[0].astype(np.float64) - planos(b)[0].astype(np.float64)) ** 2)
    return 99.0 if m == 0 else float(10 * np.log10(1023 ** 2 / m))


def audio(f, ss=None, t=None):
    a = ['ffmpeg', '-v', 'error'] + (['-ss', f'{ss:.4f}'] if ss is not None else []) + (['-t', f'{t:.4f}'] if t else []) + ['-i', str(f), '-vn', '-ac', '1', '-ar', '48000', '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(a, capture_output=True, check=True).stdout, '<f4')


def atraso(x, y, maxlag=4800):
    n = min(len(x), len(y)); x = x[:n] - x[:n].mean(); y = y[:n] - y[:n].mean()
    c = np.fft.irfft(np.fft.rfft(x, 2 * n) * np.conj(np.fft.rfft(y, 2 * n)))
    c = np.concatenate([c[-maxlag:], c[:maxlag + 1]]); lag = int(np.argmax(c)) - maxlag
    return -lag, float(c.max() / (np.sqrt((x ** 2).sum() * (y ** 2).sum()) + 1e-12))


def bocas(f, n_h, yunet):
    det = cv2.FaceDetectorYN.create(str(yunet), '', (540, 960), 0.6, 0.3, 5000)
    o = subprocess.run(['ffmpeg', '-v', 'error', '-threads', '2', '-i', str(f), '-frames:v', str(n_h), '-vf', 'select=not(mod(n\\,3)),scale=540:960:flags=area,format=bgr24',
                        '-fps_mode', 'passthrough', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    r = {}
    for i in range(len(o) // (540 * 960 * 3)):
        _, fc = det.detect(np.frombuffer(o, np.uint8, 540 * 960 * 3, i * 540 * 960 * 3).reshape(960, 540, 3))
        if fc is not None and len(fc):
            fc = max(fc, key=lambda q: q[2] * q[3]) * 2; r[i * 3] = dict(boca=float(max(fc[11], fc[13])), olho=float(min(fc[5], fc[7])), cx=float(fc[0] + fc[2] / 2))
    return r


def prev(b, w=270):
    return Image.fromarray(N.preview_de_buf(b)).resize((w, w * 16 // 9), Image.LANCZOS)


def fonte_ui(tam, negrito=False):
    for f in (['DejaVuSans-Bold.ttf'] if negrito else ['DejaVuSans.ttf']):
        for d in ('/usr/share/fonts/truetype/dejavu', '/usr/share/fonts/dejavu', '/Library/Fonts', 'C:/Windows/Fonts'):
            if Path(d, f).exists(): return ImageFont.truetype(str(Path(d, f)), tam)
    return ImageFont.load_default()


def auditar(pl, arq, esp, verif):
    arq = Path(arq); verif = Path(verif); verif.mkdir(parents=True, exist_ok=True)
    c = pl['corte']; n_h, KG, k_p, TV = c['n_h'], pl['kg'], pl['k_p'], pl['total_v3']; P = n_h + KG - k_p; tot = P + TV - KG
    info = json.loads((pl['trab'] / pl['nome'] / f'info-{sufixo(esp)}.json').read_text())
    R = dict(arquivo=str(arq), tomada=pl['nome'], espelho=esp, graf_branco=pl['graf_branco']); falhas = []
    # fontes de referência: ponte (quadros k_p..KG-1) e corpo (KG..fim), as mesmas que o variar_gancho.py usou
    if esp: ponte_ref, corpo_ref = pl['v3_espelho'], [(pl['v3_espelho'], KG, TV)]
    elif pl['corpo_normal']: ponte_ref, corpo_ref = pl['ponte_normal'], [(pl['corpo_normal'], 0, TV - KG)]
    else:
        ponte_ref, corpo_ref, k, off = pl['ponte_normal'], [], KG, 0
        for a, b in pl['corr']:
            if a > k: corpo_ref.append((pl['v3_final'], k, a))
            corpo_ref.append((pl['correcoes'], off, off + b - a)); off += b - a; k = b
        if k < TV: corpo_ref.append((pl['v3_final'], k, TV))
    st, fm = probe(arq); v, a = st.get('video'), st.get('audio'); rv = probe(corpo_ref[0][0])[0]['video']
    R['ffprobe'] = dict(codec=v['codec_name'], perfil=v.get('profile'), tam=f"{v['width']}x{v['height']}", fps=v['r_frame_rate'], pix=v['pix_fmt'],
                        cor=[v.get(k) for k in ('color_range', 'color_space', 'color_primaries', 'color_transfer')],
                        audio=a and dict(codec=a['codec_name'], hz=a['sample_rate'], canais=a['channels'], kbps=round(int(a.get('bit_rate', 0)) / 1000)),
                        dur_v=float(v['duration']), dur_a=a and float(a['duration']), mb=round(int(fm['size']) / 1e6, 1))
    corref = [rv.get(k) for k in ('color_range', 'color_space', 'color_primaries', 'color_transfer')]
    if R['ffprobe']['cor'] != corref: falhas.append(f'metadado de cor {R["ffprobe"]["cor"]} != fonte {corref}')
    if v['codec_name'] != 'hevc' or (v['width'], v['height'], v['r_frame_rate']) != (1080, 1920, '30/1'): falhas.append('codec/resolução/fps')
    if not a: falhas.append('sem áudio')
    if int(fm['size']) > 300e6: falhas.append('acima de 300 MB')
    err = sh(['ffmpeg', '-v', 'error', '-threads', '2', '-i', str(arq), '-f', 'null', '-'])
    nfr = int(sh(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', str(arq)]).stdout.strip())
    R['decode'] = dict(erros=err.stderr.strip()[:300], quadros=nfr, plano=tot)
    if err.stderr.strip(): falhas.append('decode com erro')
    if nfr != tot: falhas.append(f'quadros {nfr} != plano {tot}')
    vp = pts(arq, 'v'); ap_ = pts(arq, 'a'); dv = np.diff(vp); da = np.diff(ap_)
    R['pts'] = dict(video_passos=sorted(set(dv.tolist()))[:5], audio_passos=sorted(set(da.tolist()))[:5],
                    dif_dur_ms=round(((R['ffprobe']['dur_a'] or 0) - R['ffprobe']['dur_v']) * 1000, 1))
    if len(set(dv.tolist())) != 1: falhas.append('salto de PTS no vídeo')
    if len(set(da.tolist())) != 1: falhas.append('salto de PTS no áudio')
    if abs(R['pts']['dif_dur_ms']) > 34: falhas.append('áudio e vídeo com durações diferentes')
    # sincronia do corpo: áudio de saída no quadro t (>= P) = mix da V3 no quadro t-P+KG
    sinc = []
    for frac in (0.15, 0.5, 0.85):
        t = int(P + (tot - P) * frac); lag, cc = atraso(audio(arq, t / 30, 3.0), audio(pl['mix'], (t - P + KG) / 30, 3.0))
        sinc.append(dict(quadro=t, atraso_amostras=lag, corr=round(cc, 3)))
        if abs(lag) > 480 or cc < 0.8: falhas.append(f'sincronia no quadro {t}: atraso {lag} amostras, corr {cc:.2f}')
    R['sincronia_corpo'] = sinc
    lo = sh(['ffmpeg', '-hide_banner', '-nostats', '-i', str(arq), '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-']).stderr
    tp = re.findall(r'Peak:\s+(-?[\d.]+|-inf) dBFS', lo); il = re.findall(r'I:\s+(-?[\d.]+) LUFS', lo)
    R['loudness'] = dict(lufs=float(il[-1]) if il else None, true_peak=float(tp[-1]) if tp and tp[-1] != '-inf' else None)
    if R['loudness']['true_peak'] is not None and R['loudness']['true_peak'] > -1.0: falhas.append(f'true peak {R["loudness"]["true_peak"]} > -1,0 dBTP')
    # corpo: pacotes idênticos à fonte copiada (prova de que não houve recodificação)
    corpo = pkt_md5(arq)[P:]; ref = []; cache = {}
    for f, x, y in corpo_ref:
        if f not in cache: cache[f] = pkt_md5(f)
        ref += cache[f][x:y]
    R['corpo_md5'] = hashlib.md5(''.join(corpo).encode()).hexdigest()
    if corpo != ref: falhas.append(f'corpo diferente da fonte copiada ({len(corpo)} x {len(ref)} pacotes)')
    # cor e PSNR: ponte contra ponte_ref (recodificada, PSNR >= 40) e corpo contra a fonte (cópia, PSNR 99)
    ks_out = sorted(set([0, 1, 30, 90] + list(range(150, tot, 150)) + [P - 1, P, n_h - 1, n_h, info['k2'] - 1, info['k2']]))
    ks_out = [k for k in ks_out if 0 <= k < tot]
    qo = quadros(arq, ks_out)
    kp_ = {k: k - n_h + k_p for k in ks_out if n_h <= k < P}; qp = quadros(ponte_ref, kp_.values()) if kp_ else {}
    kc = {}
    for k in ks_out:
        if k < P: continue
        kv = k - P + KG; off = 0
        for f, x, y in corpo_ref:
            if off <= kv - KG < off + (y - x): kc[k] = (f, x + kv - KG - off); break
            off += y - x
    qc = {}
    for f in {f for f, _ in kc.values()}:
        qq = quadros(f, [i for g, i in kc.values() if g == f]); qc.update({(f, i): b for i, b in qq.items()})
    cor = []
    for k in ks_out:
        if k < n_h: continue
        r = qp[kp_[k]] if k in kp_ else qc[kc[k]]
        mo, mr = medias(qo[k]), medias(r)
        cor.append(dict(quadro=k, trecho='ponte' if k in kp_ else 'corpo', dYUV=[round(x - y, 2) for x, y in zip(mo, mr)], psnr_y=round(psnr_y(qo[k], r), 1)))
    R['cor_vs_fonte'] = cor
    R['cor_resumo'] = dict(max_dUV=round(max(max(abs(x) for x in q['dYUV'][1:]) for q in cor), 2), max_dY=round(max(abs(q['dYUV'][0]) for q in cor), 2),
                           min_psnr=min(q['psnr_y'] for q in cor))
    if R['cor_resumo']['max_dUV'] > 3 or R['cor_resumo']['max_dY'] > 3: falhas.append(f'cor fora da fonte {R["cor_resumo"]}')
    if R['cor_resumo']['min_psnr'] < 40: falhas.append(f'PSNR baixo contra a fonte ({R["cor_resumo"]["min_psnr"]})')
    # emenda: último quadro do gancho x primeiro da ponte (mesma luz)
    R['cor_emenda_gancho'] = [round(x - y, 2) for x, y in zip(medias(qo[n_h - 1]), medias(qo[n_h]))]
    if abs(R['cor_emenda_gancho'][0]) > 40: falhas.append(f'salto de luz na emenda do gancho {R["cor_emenda_gancho"]}')
    # nível da letra no título do quadro 0: com graf_branco 1000 o miolo branco fica perto de Y 940 (10 bits); com 203, perto de 720
    y0 = planos(qo[0])[0][pl['topo']:max(pl['topo'] + 10, info['titulo_fundo_y'] or pl['topo'] + 400)]
    alvo = 940 if pl['graf_branco'] >= 999 else None
    p995 = float(np.percentile(y0, 99.5)); R['letra'] = dict(y_p995_titulo=p995, alvo=alvo)
    if alvo and not (alvo - 25 <= p995 <= alvo + 25): falhas.append(f'letra branca fora de ~{alvo} (p99.5 {p995:.0f}): confira graf_branco')
    # rosto x legenda e título x olhos no arquivo final
    bb = bocas(arq, n_h, pl['yunet']); prob = []
    for e in info['legendas']:
        m = [r for k, r in bb.items() if e['k0'] - 2 <= k <= e['k1'] + 2]
        if m and max(r['boca'] for r in m) + 15 > e['y'] - 36: prob.append(dict(palavra=e['txt'], y=e['y'], boca=round(max(r['boca'] for r in m))))
    R['boca_legenda'] = dict(quadros_com_rosto=len(bb), boca_max=round(max([r['boca'] for r in bb.values()], default=0)),
                             olho_min=round(min([r['olho'] for r in bb.values()], default=0)), conflitos=prob[:5],
                             rosto_cx_medio=round(float(np.mean([r['cx'] for r in bb.values()]))) if bb else None)
    if prob: falhas.append(f'legenda sobre a boca em {len(prob)} palavra(s)')
    if not bb: falhas.append('rosto não detectado no gancho')
    ya, yb = planos(qo[0])[0].astype(int), planos(qo[1])[0].astype(int)
    R['abertura'] = dict(dif_q0_q1=round(float(np.abs(ya - yb).mean()), 2), titulo_fundo_y=info['titulo_fundo_y'], olho_min_bruto=info['olho_min_y'])
    if info['titulo_fundo_y'] and bb and info['titulo_fundo_y'] > R['boca_legenda']['olho_min']: falhas.append('título sobre os olhos')
    # mosaico
    tiles = [(f'q{k} {k / 30:.1f}s', prev(qo[k])) for k in sorted(set([0, 1, 30, 90] + list(range(150, tot, 150)))) if k in qo]
    for r, k in ((f'emenda q{n_h - 1}', n_h - 1), (f'emenda q{n_h}', n_h), (f'l2 q{info["k2"] - 1}', info['k2'] - 1), (f'l2 q{info["k2"]}', info['k2']),
                 (f'prefixo|corpo q{P - 1}', P - 1), (f'q{P}', P)):
        tiles.append((r, prev(qo[k])))
    big = Image.fromarray(N.preview_de_buf(qo[info['k2']]))
    for nm, (a0, a1) in (('4:5', (285, 1635)), ('3:4', (240, 1680))):
        cr = big.crop((0, a0, 1080, a1)); tiles.append((f'recorte {nm}', cr.resize((270, round(270 * cr.height / 1080)), Image.LANCZOS)))
    veredito = 'APROVADO' if not falhas else 'REPROVADO'
    cols = 8; tw, th = 270, 480 + 22; rows = (len(tiles) + cols - 1) // cols
    mos = Image.new('RGB', (cols * tw, rows * th + 120), (20, 20, 20)); dr = ImageDraw.Draw(mos); fo, fb = fonte_ui(16), fonte_ui(30, True)
    dr.text((10, 8), f'{arq.name}  {veredito}', fill=(74, 222, 128) if not falhas else (255, 80, 80), font=fb)
    dr.text((10, 50), f'{nfr}/{tot} quadros  dUV<={R["cor_resumo"]["max_dUV"]}  PSNR>={R["cor_resumo"]["min_psnr"]}  TP {R["loudness"]["true_peak"]} dBTP  '
                      f'letra p99.5 {p995:.0f}  sinc {[s["atraso_amostras"] for s in sinc]} amostras', fill=(230, 230, 230), font=fo)
    dr.text((10, 76), ('; '.join(falhas) or 'sem falhas automáticas') + '  (prévia HLG: layout, não prova de cor)', fill=(230, 230, 230), font=fo)
    for i, (r, im) in enumerate(tiles):
        x, y = (i % cols) * tw, 120 + (i // cols) * th; mos.paste(im, (x, y + 22)); dr.text((x + 4, y + 2), r, fill=(230, 230, 230), font=fo)
    mp = verif / f'{arq.stem}-mosaico.png'; mos.save(mp)
    R.update(veredito=veredito, falhas=falhas, mosaico=str(mp))
    (verif / f'{arq.stem}.json').write_text(json.dumps(R, ensure_ascii=False, indent=1))
    return R


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Audita uma variação de gancho (normal ou espelho) contra o plano JSON do variar_gancho.py.')
    ap.add_argument('plano'); ap.add_argument('arquivo')
    ap.add_argument('--espelho', action='store_true', help='o arquivo é a versão espelho (corpo vem de v3_espelho)')
    ap.add_argument('--verif', help='pasta dos relatórios (padrão: <trab>/verif)')
    a = ap.parse_args(); pl = carregar_plano(a.plano)
    r = auditar(pl, a.arquivo, a.espelho, a.verif or pl['trab'] / 'verif')
    print(json.dumps({k: r[k] for k in ('arquivo', 'veredito', 'falhas', 'mosaico')}, ensure_ascii=False))
    sys.exit(0 if r['veredito'] == 'APROVADO' else 1)
