# Variações de gancho (e espelho) sobre uma V3 já renderizada: troca os primeiros KG quadros por um gancho novo
# tirado de outra tomada do bruto (1.2x, título Advercase/Kalam, legenda de uma palavra) e cola o corpo da V3 sem recodificar.
# Generalizado de 2026-10-16-variacoes-ep3-ep4-yap3/scripts/variar.py. Tudo vem de um plano JSON (exemplo em assets/plano-variacao-exemplo.json).
#
# Uso:
#   python3 variar_gancho.py prefixo plano.json [--espelho] [--amostra N] [--saida arq.mp4]
#   python3 variar_gancho.py final   plano.json [--espelho] [--saida arq.mp4]
# prefixo: gancho (n_h quadros) + ponte (quadros k_p..KG-1 da V3, decodificados do arquivo pronto). --amostra N corta em N quadros.
# final: prefixo + corpo + áudio novo. Corpo normal: "corpo_normal" (V3 de KG até o fim já renderizada) ou v3_final com os trechos
#        corr trocados pelos de "correcoes". Corpo espelho: v3_espelho de KG até o fim.
# Ponte normal: "ponte_normal" se houver (V3 completa desde o quadro 0), senão v3_final. Ponte e corpo precisam estar no mesmo
# branco de gráfico do gancho ("graf_branco", padrão 1000 = letra branca; 203 só para reproduzir lotes antigos de letra cinza).
# Requer: ffmpeg/ffprobe no PATH, numpy, opencv (YuNet), Pillow, cor_hlg.py nesta pasta.
import sys, json, re, subprocess, shutil, argparse
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQUI = Path(__file__).resolve().parent; SKILL = AQUI.parent
sys.path.insert(0, str(AQUI))
import cor_hlg as N
W, H, FS10 = N.W, N.H, N.FS10; FS8 = W * H * 3
# o encoder vem de cor_hlg.X265 (mesmos parâmetros do motor que renderizou a V3: GOP fixo de 30, sem B-frames): o prefixo precisa colar no corpo com -c:v copy
YUNET_PADRAO = SKILL / 'assets/modelos/face_detection_yunet_2023mar.onnx'
SFX_PADRAO = SKILL / 'assets/sfx-gancho'


def carregar_plano(arq):
    p = json.loads(Path(arq).read_text()); base = Path(arq).resolve().parent
    def caminho(v): return None if v in (None, '') else Path(v) if Path(v).is_absolute() else base / v
    for k in ('bruto', 'v3_final', 'v3_espelho', 'correcoes', 'corpo_normal', 'ponte_normal', 'mix', 'cab_ass', 'fontes', 'sfx', 'trab', 'yunet'):
        p[k] = caminho(p.get(k))
    p['sfx'] = p['sfx'] or SFX_PADRAO; p['yunet'] = p['yunet'] or YUNET_PADRAO
    if 'corte' not in p:  # corte vindo do cortes.json do cortes_tomadas.py
        p['corte'] = json.loads(caminho(p['cortes']).read_text())[p['chave']]
    if isinstance(p.get('palavras'), str):  # palavras vindas do JSON do transcrever_tomadas.py
        p['palavras'] = json.loads(caminho(p['palavras']).read_text())[p.get('chave_palavras', p.get('chave'))]
    p.setdefault('kg', 120); p.setdefault('topo', 150); p.setdefault('estilo', 'Default'); p.setdefault('junta_curtas', False)
    p.setdefault('fix', {}); p.setdefault('drop', []); p.setdefault('corr', []); p.setdefault('prox_efeito', None)
    if not p.get('total_v3'): p['total_v3'] = contar_quadros(p['v3_final'])
    p['ponte_normal'] = p['ponte_normal'] or p['v3_final']
    p['graf_branco'] = float(p.get('graf_branco', 1000)); N.GRAF_BRANCO = p['graf_branco']   # branco dos gráficos do gancho (nits)
    p['trab'].mkdir(parents=True, exist_ok=True); p['saida_dir'] = caminho(p.get('saida_dir')) or p['trab']
    for k in ('bruto', 'v3_final', 'mix', 'cab_ass'): assert p[k] and p[k].exists(), f'falta {k}: {p[k]}'
    for f in ('Advercase-Bold.ttf', 'Kalam-Bold.ttf'): assert (p['fontes'] / f).exists(), f'falta a fonte {f} em {p["fontes"]}'
    return p


def contar_quadros(f):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', str(f)],
                       capture_output=True, text=True, check=True).stdout
    return int(o.strip().split(',')[0])


def camera_bruto(bruto, raws):
    """raws: quadros crescentes do bruto -> gera (b, buf) em 10 bits lanczos, como o motor da V3."""
    need = sorted(set(raws)); rng = []
    for b in need:
        if rng and rng[-1][1] == b - 1: rng[-1][1] = b
        else: rng.append([b, b])
    sel = '+'.join(f'between(n,{a},{b})' for a, b in rng)
    p = subprocess.Popen(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-threads', '3', '-filter_threads', '2', '-i', str(bruto), '-vf',
                          f"select='{sel}',setpts=N/30/TB,scale={W}:{H}:flags=lanczos,format=yuv420p10le", '-fps_mode', 'passthrough',
                          '-frames:v', str(len(need)), '-f', 'rawvideo', '-pix_fmt', 'yuv420p10le', '-'], stdout=subprocess.PIPE)
    for b in need:
        buf = p.stdout.read(FS10); assert len(buf) == FS10, f'câmera curta no quadro {b}'
        yield b, buf
    p.kill()


def ponte(v3, k0, k1):
    """quadros k0..k1-1 do arquivo da V3 já renderizado (câmera + gráficos), em 10 bits."""
    p = subprocess.Popen(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-threads', '3', '-i', str(v3), '-vf', f"select='between(n,{k0},{k1 - 1})',setpts=N/30/TB",
                          '-fps_mode', 'passthrough', '-frames:v', str(k1 - k0), '-f', 'rawvideo', '-pix_fmt', 'yuv420p10le', '-'], stdout=subprocess.PIPE)
    for k in range(k0, k1):
        buf = p.stdout.read(FS10); assert len(buf) == FS10, f'V3 curta no quadro {k}'
        yield k, buf
    p.kill()


def espelhar(buf):
    Y, U, V = N.yuv_planos(buf)
    return np.ascontiguousarray(Y[:, ::-1]).tobytes() + np.ascontiguousarray(U[:, ::-1]).tobytes() + np.ascontiguousarray(V[:, ::-1]).tobytes()


def matte(rgb_preto, rgb_branco):  # igual ao motor da V3: alfa pela diferença entre render sobre branco e sobre preto
    bp = rgb_preto.astype(np.float32); bw = rgb_branco.astype(np.float32)
    return np.clip(1 - (bw - bp).mean(-1) / 255.0, 0, 1), bp


def encoder(saida, n):
    ent = ['-f', 'rawvideo', '-pix_fmt', 'yuv420p10le', '-s', f'{W}x{H}', '-r', '30', '-color_range', 'tv', '-colorspace', 'bt2020nc',
           '-color_primaries', 'bt2020', '-color_trc', 'arib-std-b67', '-i', '-']
    return subprocess.Popen(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-y'] + ent + ['-map', '0:v', '-an', '-frames:v', str(n)] + N.X265 +
                            ['-r', '30', '-fps_mode', 'cfr', '-movflags', '+faststart', str(saida)], stdin=subprocess.PIPE)


# ---------------- título e legenda do gancho ----------------
def tokens(txt):
    pecas = [(m.group(1) or m.group(2), m.group(1) is not None) for m in re.finditer(r'\[([^\]]+)\]|([^\[\]]+)', txt)]
    pal, cur = [], []
    for t, v in pecas:
        for parte in re.split(r'(\s+)', t):
            if not parte: continue
            if parte.isspace():
                if cur: pal.append(cur); cur = []
            else: cur.append((parte, v))
    if cur: pal.append(cur)
    return pal


def desenha(cv, txt, f, px, y, lh, avisos):
    d = ImageDraw.Draw(cv); sp = f.getlength(' ')
    for part in txt.split('\n'):
        ln = tokens(part); lw = sum(f.getlength(t) for w in ln for t, _ in w) + sp * (len(ln) - 1)
        if lw > 960: avisos.append(f'largura {lw:.0f} > 960: {part}')
        x = (W - lw) / 2
        for w in ln:
            for t, v in w: d.text((x, y), t, font=f, fill='#4ade80' if v else '#ffffff'); x += f.getlength(t)
            x += sp
        y += round(px * lh)
    return y


def com_sombra(cv):
    a = cv.split()[3]; sh = Image.new('RGBA', cv.size, (0, 0, 0, 0))
    for blur, op, dy in ((10, .55, 5), (3, .45, 2)):
        m = a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op))
        lay = Image.new('RGBA', cv.size, (0, 0, 0, 0)); lay.putalpha(m); sh.alpha_composite(lay, (0, dy))
    sh.alpha_composite(cv); return sh


def titulos(pl, pasta):
    F = pl['fontes']; f1 = ImageFont.truetype(str(F / 'Advercase-Bold.ttf'), 85); f2 = ImageFont.truetype(str(F / 'Kalam-Bold.ttf'), 54)
    av, out = [], []
    for com_l2 in (True, False):
        cv = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        y = desenha(cv, pl['l1'], f1, 85, 35, 1.08, av)
        if com_l2: desenha(cv, pl['l2'], f2, 54, y + 10, 1.05, av)
        im = com_sombra(cv); bb = im.getbbox()
        if com_l2: ref = bb[1]; fundo_titulo = bb[3] + pl['topo'] - ref
        o = Image.new('RGBA', im.size, (0, 0, 0, 0)); o.alpha_composite(im, (0, pl['topo'] - ref)); out.append(o)
    p2, p1 = pasta / 'titulo-l1l2.png', pasta / 'titulo-l1.png'; out[0].save(p2); out[1].save(p1)
    return p1, p2, fundo_titulo, sorted(set(av))


def palavras(pl):
    ini = pl['corte']['ini']; ws = []
    for a, b, w in pl['palavras']:
        w = w.strip()
        if w in pl['drop']: continue
        w0 = w.strip('.,?!')
        if w0 in pl['fix']:
            if pl['fix'][w0] is None: ws[-1][1] += '%'; continue   # fix {"%": null} cola o % na palavra anterior
            w = w.replace(w0, pl['fix'][w0])
        ws.append([a, w.strip('.,!') if not w.endswith('?') else w[:-1]])
    ws[0][0] = ini
    return [(max(0, round((a - ini) * 25)), w) for a, w in ws]   # 25 = 30 fps / 1.2


def rosto_bruto(pl, f0, nraw):
    det = cv2.FaceDetectorYN.create(str(pl['yunet']), '', (540, 960), 0.6, 0.3, 5000)
    o = subprocess.run(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-threads', '2', '-ss', f'{f0 / 30:.4f}', '-i', str(pl['bruto']), '-frames:v', str(nraw),
                        '-vf', 'select=not(mod(n\\,6)),scale=540:960:flags=area,format=bgr24', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-'],
                       capture_output=True, check=True).stdout
    res = []
    for i in range(len(o) // (540 * 960 * 3)):
        _, f = det.detect(np.frombuffer(o, np.uint8, 540 * 960 * 3, i * 540 * 960 * 3).reshape(960, 540, 3))
        if f is None or not len(f): continue
        f = max(f, key=lambda r: r[2] * r[3]) * 2
        res.append(dict(kr=i * 6, olho=float(min(f[5], f[7])), boca=float(max(f[11], f[13]))))
    return res


def ass_gancho(pl, ws, n_h, rosto, saida):
    cab = pl['cab_ass'].read_text().split('[Events]')[0]; grupos = []
    for k, w in ws:
        g = grupos[-1] if grupos else None
        if pl['junta_curtas'] and g and len(g[1].split()) == 1 and (len(w) <= 3 or len(g[1]) <= 3) and len(g[1]) + len(w) < 12: g[1] += ' ' + w
        else: grupos.append([k, w])
    cs = lambda t: f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'
    ev = []
    for i, (k, w) in enumerate(grupos):
        k1 = grupos[i + 1][0] if i + 1 < len(grupos) else n_h
        bocas = [r['boca'] for r in rosto if k - 3 <= r['kr'] / 1.2 <= k1 + 3]
        ev.append(dict(k0=k, k1=k1, txt=w, y=1540 if bocas and max(bocas) > 1250 else 1330))
    L = [f'Dialogue: 0,{cs(int(e["k0"] / 30 * 100) / 100)},{cs(int(e["k1"] / 30 * 100) / 100)},{pl["estilo"]},,0,0,0,,{{\\pos(650,{e["y"]})}}{e["txt"]}' for e in ev]
    Path(saida).write_text(cab + '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n' + '\n'.join(L) + '\n')
    return ev


def esc_filtro(p): return str(p).replace('\\', '/').replace(':', '\\:').replace("'", "\\'")


def graf_gancho(pl, n_h, p1, p2, k2, ass, fundo):
    fc = (f"[0:v]format=rgb24[b];[b][1:v]overlay=0:0:format=rgb:enable='lt(n,{k2})'[x];[x][2:v]overlay=0:0:format=rgb:enable='gte(n,{k2})',"
          f"subtitles={esc_filtro(ass)}:fontsdir={esc_filtro(pl['fontes'])},format=rgb24[v]")
    p = subprocess.Popen(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-threads', '2', '-f', 'lavfi', '-i', f'color=c={fundo}:s={W}x{H}:r=30',
                          '-loop', '1', '-framerate', '30', '-i', str(p1), '-loop', '1', '-framerate', '30', '-i', str(p2),
                          '-filter_complex', fc, '-map', '[v]', '-frames:v', str(n_h), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    for k in range(n_h):
        b = p.stdout.read(FS8); assert len(b) == FS8
        yield k, np.frombuffer(b, np.uint8).reshape(H, W, 3)
    p.wait()


# ---------------- áudio ----------------
def dec(args):
    return np.frombuffer(subprocess.check_output(['nice', '-n', '10', 'ffmpeg', '-v', 'error'] + args + ['-f', 'f32le', '-ar', '48000', '-ac', '2', '-']), '<f4').reshape(-1, 2).copy()


def sfx_ganho(pl, som, voz, a):
    s = dec(['-i', str(pl['sfx'] / f'sfx-{som}.wav')]); db = {'impacto': -10, 'clique': -15}[som]
    g = pl['p90'] * 10 ** (db / 20) / max(float(np.sqrt(np.mean(s ** 2))), 1e-8)
    lp = max(.08, float(np.max(abs(voz[max(0, a - 4800):a + 24000]))))
    return s, min(g, lp * .20 / max(float(np.max(abs(s))), 1e-8))


def audio_variacao(pl, n_h, t2, total_out):
    c = pl['corte']
    voz = dec(['-ss', f"{c['ini']:.5f}", '-t', f'{n_h * 1.2 / 30 + 1:.3f}', '-i', str(pl['bruto']), '-vn', '-af', 'aresample=48000,atempo=1.2'])[:n_h * 1600]
    assert len(voz) == n_h * 1600
    r = 240; voz[-r:] *= np.linspace(1, 0, r)[:, None]
    v3 = dec(['-i', str(pl['mix'])])[pl['k_p'] * 1600:]
    v3[:r] *= np.linspace(0, 1, r)[:, None]
    mix = np.concatenate([voz, v3])[:total_out * 1600]
    mix = np.pad(mix, ((0, total_out * 1600 - len(mix)), (0, 0)))
    efe = []
    for som, t in (('impacto', 0.0), ('clique', t2)):
        if t is None: continue
        a = round(t * 48000); s, g = sfx_ganho(pl, som, mix, a); n = min(len(s), len(mix) - a)
        mix[a:a + n] += s[:n] * g; efe.append(dict(som=som, t=round(t, 3), ganho=round(g, 4)))
    pk = float(np.max(abs(mix))); assert pk < .90, f'pico {pk:.3f} >= 0.90: baixe o ganho dos efeitos'
    return mix.astype('<f4'), dict(efeitos=efe, pico=round(pk, 4))


def sufixo(esp): return 'm' if esp else 'n'


# ---------------- prefixo (gancho + ponte k_p..KG-1) ----------------
def prefixo(pl, espelho, saida, n_lim=None):
    c = pl['corte']; n_h, f0, KG, k_p = c['n_h'], c['f0'], pl['kg'], pl['k_p']
    pasta = pl['trab'] / pl['nome']; pasta.mkdir(exist_ok=True)
    p1, p2, fundo_tit, av = titulos(pl, pasta)
    ws = palavras(pl)
    k2 = next(k for k, w in ws if w == pl['entra'] and k > 0)
    ros = rosto_bruto(pl, f0, round(n_h * 1.2))
    ev = ass_gancho(pl, ws, n_h, ros, pasta / 'gancho.ass')
    olho = min(r['olho'] for r in ros) if ros else None
    P = n_h + KG - k_p; n = P if n_lim is None else min(P, n_lim)
    hook_raw = [f0 + (k * 6) // 5 for k in range(n_h)]
    if espelho: assert pl['v3_espelho'] and pl['v3_espelho'].exists(), 'falta v3_espelho (espelho original da V3) no plano'
    fonte_ponte = pl['v3_espelho'] if espelho else pl['ponte_normal']   # o espelho original já vem com câmera espelhada e texto legível
    enc = encoder(saida, n)
    hb = camera_bruto(pl['bruto'], hook_raw[:min(n, n_h)]); cur_b, cur = -1, None
    for (k, rp), (_, rw) in zip(graf_gancho(pl, min(n, n_h), p1, p2, k2, pasta / 'gancho.ass', 'black'),
                                graf_gancho(pl, min(n, n_h), p1, p2, k2, pasta / 'gancho.ass', 'white')):
        while cur_b < hook_raw[k]: cur_b, cur = next(hb)
        a, bp = matte(rp, rw); cbuf = espelhar(cur) if espelho else cur
        q = N.compor(cbuf, a, bp)
        if k in (0, k2): Image.fromarray(N.preview_de_buf(q)).save(pasta / f'prev-{sufixo(espelho)}-{k}.png')
        enc.stdin.write(q)
    if n > n_h:
        for k, buf in ponte(fonte_ponte, k_p, k_p + n - n_h): enc.stdin.write(buf)
    enc.stdin.close(); assert enc.wait() == 0
    info = dict(tomada=pl['nome'], f0=f0, n_h=n_h, k2=k2, t_l2=round(k2 / 30, 3), quadros_prefixo=P, quadros_gravados=n, titulo_fundo_y=fundo_tit,
                olho_min_y=olho, avisos_titulo=av, legendas=ev, espelho=espelho, saida=str(saida))
    if n_lim is None: (pasta / f'info-{sufixo(espelho)}.json').write_text(json.dumps(info, ensure_ascii=False, indent=1))
    return info


def final(pl, esp, saida):
    c = pl['corte']; n_h, KG, k_p, TV = c['n_h'], pl['kg'], pl['k_p'], pl['total_v3']; P = n_h + KG - k_p; tot = P + TV - KG
    info = json.loads((pl['trab'] / pl['nome'] / f'info-{sufixo(esp)}.json').read_text())
    pre = Path(info['saida']); assert pre.exists() and contar_quadros(pre) == P, f'prefixo ausente ou incompleto: {pre} (rode o comando prefixo sem --amostra)'
    if esp: partes = [(pl['v3_espelho'], KG, TV)]
    elif pl['corpo_normal']:
        assert pl['corpo_normal'].exists() and contar_quadros(pl['corpo_normal']) >= TV - KG, f'corpo_normal ausente ou curto: {pl["corpo_normal"]}'
        partes = [(pl['corpo_normal'], 0, TV - KG)]
    else:
        partes, k, off = [], KG, 0
        for a, b in pl['corr']:
            assert pl['correcoes'] and pl['correcoes'].exists(), 'corr no plano pede o arquivo correcoes'
            if a > k: partes.append((pl['v3_final'], k, a))
            partes.append((pl['correcoes'], off, off + b - a)); off += b - a; k = b
        if k < TV: partes.append((pl['v3_final'], k, TV))
    lst = pl['trab'] / f'concat-{pl["nome"]}-{sufixo(esp)}.txt'
    L = [f"file '{pre}'"]
    for f, a, b in partes: L += [f"file '{f}'", f'inpoint {a / 30:.6f}', f'outpoint {b / 30:.6f}']
    lst.write_text('\n'.join(L) + '\n')
    t2 = info['t_l2']; prox = pl['prox_efeito']   # próximo efeito sonoro da V3 (s); clique só se ficar a mais de 1.7 s de outro efeito
    if t2 < 1.7 or (prox is not None and abs(prox + (P - KG) / 30 - t2) < 1.7): t2 = None
    mix, aud = audio_variacao(pl, n_h, t2, tot)
    est = pl['v3_final'].stat().st_size * tot / TV; livre = shutil.disk_usage(Path(saida).resolve().parent).free
    assert livre > est + 600e6, f'disco: livre {livre / 1e9:.2f} GB < estimativa {est / 1e9:.2f} GB + 0.6 GB'
    p = subprocess.Popen(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', '-',
                          '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', f'{tot / 30:.6f}', '-movflags', '+faststart', str(saida)], stdin=subprocess.PIPE)
    p.stdin.write(mix.tobytes()); p.stdin.close(); assert p.wait() == 0
    return dict(saida=str(saida), quadros=tot, prefixo=P, **aud)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Variação de gancho (normal ou espelho) sobre uma V3 pronta, guiada por plano JSON.')
    ap.add_argument('comando', choices=['prefixo', 'final']); ap.add_argument('plano')
    ap.add_argument('--espelho', action='store_true', help='câmera espelhada (texto continua legível); corpo vem de v3_espelho')
    ap.add_argument('--amostra', type=int, help='só prefixo: grava apenas os N primeiros quadros, para conferir título e legenda')
    ap.add_argument('--saida', help='arquivo de saída (padrão: trab/prefixo-<nome>-n|m.mp4 ou saida_dir/<nome>-gancho-normal|espelho-hlg.mp4)')
    a = ap.parse_args(); pl = carregar_plano(a.plano); s = sufixo(a.espelho)
    if a.comando == 'prefixo':
        saida = Path(a.saida) if a.saida else pl['trab'] / (f'amostra-{pl["nome"]}-{s}.mp4' if a.amostra else f'prefixo-{pl["nome"]}-{s}.mp4')
        r = prefixo(pl, a.espelho, saida, a.amostra)
        print(json.dumps({k: v for k, v in r.items() if k != 'legendas'}, ensure_ascii=False, indent=1))
    else:
        sd = pl['saida_dir']; sd.mkdir(parents=True, exist_ok=True)
        saida = Path(a.saida) if a.saida else sd / f'{pl["nome"]}-gancho-{"espelho" if a.espelho else "normal"}-hlg.mp4'
        print(json.dumps(final(pl, a.espelho, saida), ensure_ascii=False, indent=1))
