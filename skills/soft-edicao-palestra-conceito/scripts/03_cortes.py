"""Etapa 3. Cortes: planeja as pecas (tira so silencio comprovado, longe das palavras) e confere a escolha do trecho.
Le ajustes.json: blocos [[ini,fim],...] (tempo absoluto da fonte), cold_open [ini,fim] opcional,
substituir (corrige palavra da transcricao), cortar (tira de proposito: gaguejo, recomeco), loops.
uso: python3 03_cortes.py TRAB [--prova]   (--prova dispensa a duracao minima, so para teste curto)
saidas: silencios.json, cortes.json, palavras-saida.json
criterio de pronto: imprime PRONTO e sai com 0. Falha (exit 1) se:
  - duracao final < duracao_min_s da marca;
  - alguma borda de bloco corta uma palavra no meio;
  - algum corte de pausa cai fora de silencio do silencedetect ou a menos de MARGEM de palavra com timestamp;
  - frase de loop aberto ("vou mostrar...") sem entrada em loops com o fechamento dentro do corte."""
import json, math, os, re, subprocess, sys
import comum as C

T = C.trab_arg()
PROVA = '--prova' in sys.argv
M = C.marca(T)
A = C.ajustes(T)
E = C.lj(T, 'entrada.json')
SPD, FPS = float(M['velocidade']), C.FPS
PAUSA, PAD, MARGEM = 0.35, 0.08, 0.15   # pausa minima (silencedetect), folga dentro do silencio, folga de cada palavra
Q = SPD / FPS

# ---------- silencios (fonte16.wav comeca em E['offset']) ----------
sp = os.path.join(T, 'silencios.json')
if not os.path.exists(sp):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', os.path.join(T, 'fonte16.wav'), '-af', 'silencedetect=n=-35dB:d=0.3',
                        '-f', 'null', '-'], capture_output=True, text=True)
    st, sil = None, []
    for ln in r.stderr.splitlines():
        m = re.search(r'silence_start: ([\d.]+)', ln)
        if m: st = float(m.group(1))
        m = re.search(r'silence_end: ([\d.]+)', ln)
        if m and st is not None:
            sil.append([round(st + E['offset'], 3), round(float(m.group(1)) + E['offset'], 3)]); st = None
    json.dump(sil, open(sp, 'w'))
sil = json.load(open(sp))

# ---------- palavras ----------
ws = C.palavras_bruto(T)
for de, ate, novas in A.get('substituir', []):
    ws = [w for w in ws if not (de <= w['t0'] < ate)] + [dict(w=x[0], t0=x[1], t1=x[2]) for x in novas]
ws.sort(key=lambda w: w['t0'])
dd = []
for w in ws:   # palavra repetida na borda de segmento do whisper
    if dd and w['w'].lower().strip('.,?!') == dd[-1]['w'].lower().strip('.,?!') and w['t0'] < dd[-1]['t1'] + 0.05:
        continue
    dd.append(w)
REM = A.get('cortar', [])
ws = [w for w in dd if not any(a <= (w['t0'] + w['t1']) / 2 <= b for a, b in REM)]


def pecas(INI, FIM):
    # So corta silencio comprovado no audio (silencedetect), nunca o vao entre timestamps do whisper:
    # o whisper erra o fim/inicio da palavra e o vao "vazio" dele pode ter fala (foi o que comeu 'VPS', 'e', 'que').
    # Cada palavra com timestamp fica protegida com MARGEM nas duas pontas; do silencio que sobra ainda sai PAD de cada lado.
    wb = [w for w in ws if w['t1'] >= INI - 0.5 and w['t0'] <= FIM + 0.5]
    prot = sorted([w['t0'] - MARGEM, max(w['t0'] + 0.3, w['t1']) + MARGEM] for w in wb)
    fora = []
    for a, b in sil:
        segs = [[a + PAD, b - PAD]]
        for p0, p1 in prot:
            nov = []
            for x0, x1 in segs:
                if p1 <= x0 or p0 >= x1: nov.append([x0, x1]); continue
                if p0 > x0: nov.append([x0, p0])
                if p1 < x1: nov.append([p1, x1])
            segs = nov
        fora += [s for s in segs if s[1] - s[0] > PAUSA - 2 * PAD]
    if A.get("preservar_fala_continua", False):
        fora = []  # manter pausas: prova contínua, sem emendas internas
    fora += [list(r) for r in REM]
    fora = sorted(f for f in fora if f[1] - f[0] > 0.08)
    mg = []
    for f in fora:
        if mg and f[0] <= mg[-1][1] + 0.05: mg[-1][1] = max(mg[-1][1], f[1])
        else: mg.append(list(f))
    keep, a = [], INI
    for f0, f1 in mg:
        if f1 <= INI or f0 >= FIM: continue
        if f0 - a > 0.05: keep.append([a, f0])
        a = max(a, f1)
    if FIM - a > 0.05: keep.append([a, FIM])
    # quadro de 1/30 s arredondado para fora: a peca so cresce, o corte nunca encosta mais na palavra
    keep = [[round(math.floor(a * 30 + 1e-6) / 30, 4), round(math.ceil(b * 30 - 1e-6) / 30, 4)] for a, b in keep]
    keep = [k for k in keep if k[1] - k[0] > 0.1]
    D = sum(b - a for a, b in keep)
    nq = int(-(-D // Q))
    keep[-1][1] = round(keep[-1][1] + (nq * Q - D), 4)   # bloco = numero inteiro de quadros de saida
    return keep, nq


CO = A.get('cold_open')
blocos = ([dict(ini=CO[0], fim=CO[1], cold=True)] if CO else []) + [dict(ini=a, fim=b, cold=False) for a, b in A['blocos']]
B, cut_map, pal, tl = [], [], [], 0.0
for bi, b in enumerate(blocos):
    INI, FIM = b['ini'], b['fim']
    if b['cold']:   # cold open: trecho continuo, sem corte de pausa
        nq = int(-(-(FIM - INI) // Q)); keep = [[INI, round(INI + nq * Q, 4)]]
    else:
        keep, nq = pecas(INI, FIM)
    t0b, acc = tl, 0.0
    for a, c in keep:
        cut_map.append(dict(id=f'cut-{len(cut_map) + 1:03d}', bloco=bi, source_start=round(a, 3), source_end=round(c, 3),
                            timeline_start=round(tl + acc / SPD, 3), timeline_end=round(tl + (acc + c - a) / SPD, 3),
                            audio_fade_in_ms=30, audio_fade_out_ms=30))
        for w in ws:
            if a - 0.04 <= w['t0'] < c - 0.04:   # pelo inicio: o fim da palavra no whisper invade a pausa
                pal.append(dict(t0=round(tl + (acc + max(w['t0'], a) - a) / SPD, 3), t1=round(tl + (acc + min(w['t1'], c) - a) / SPD, 3), w=w['w']))
        acc += c - a
    B.append(dict(ini=INI, fim=FIM, cold=b['cold'], keep=keep, nq=nq, t0=round(t0b, 4)))
    tl = t0b + nq / FPS
for i, w in enumerate(pal):
    if w['t1'] - w['t0'] < 0.04:
        w['t1'] = round(w['t0'] + 0.06, 3)
        if i + 1 < len(pal) and pal[i + 1]['t0'] < w['t1']:
            pal[i + 1]['t0'] = w['t1']; pal[i + 1]['t1'] = max(pal[i + 1]['t1'], round(w['t1'] + 0.06, 3))
keep_all = [k for b in B for k in b['keep']]
C.gj(T, 'cortes.json', dict(velocidade=SPD, fps=FPS, keep=keep_all, cut_map=cut_map, blocos=B, dur_saida=round(tl, 4),
                            cold_open=CO, cold_saida=round(B[0]['nq'] / FPS, 4) if CO else 0.0))
C.gj(T, 'palavras-saida.json', pal)

# ---------- conferencias ----------
falhas, avisos = [], []
todas = C.palavras_bruto(T)
print(f'pecas {len(keep_all)} | saida {tl:.2f} s | palavras {len(pal)}')
for i, b in enumerate(B):
    print(f"bloco {i}{' (cold open)' if b['cold'] else ''} fonte {b['ini']:.2f}-{b['fim']:.2f} pecas {len(b['keep'])} saida {b['t0']:.2f}+{b['nq'] / FPS:.2f}")
    for borda in (b['ini'], b['fim']):
        x = [w['w'] for w in todas if w['t0'] + 0.03 < borda < w['t1'] - 0.03]
        if x: falhas.append(f'borda {borda:.2f} do bloco {i} corta a palavra {x}')
    if not b['cold']:
        dentro = [w for w in ws if b['ini'] - 0.05 <= w['t0'] < b['fim']]
        antes = [w for w in todas if w['t1'] <= b['ini'] + 0.03]
        if dentro and not re.search(r'[.?!]$', dentro[-1]['w']):
            avisos.append(f"bloco {i} termina em '{dentro[-1]['w']}' sem ponto final: confira se a frase acabou")
        if antes and not re.search(r'[.?!]$', antes[-1]['w']) and dentro and dentro[0]['t0'] - antes[-1]['t1'] < 0.6:
            avisos.append(f"bloco {i} comeca em '{dentro[0]['w']}' logo depois de '{antes[-1]['w']}' sem pausa: confira se a frase comeca ali")
for i, b in enumerate(B):   # nenhum corte fora de silencio comprovado nem perto de palavra (fora 'cortar')
    for (a0, a1), (b0, b1) in zip(b['keep'], b['keep'][1:]):
        if any(r0 - 0.04 <= a1 and b0 <= r1 + 0.04 for r0, r1 in REM): continue
        if not any(s0 - 0.02 <= a1 and b0 <= s1 + 0.02 for s0, s1 in sil):
            falhas.append(f'corte {a1:.2f}-{b0:.2f} do bloco {i} fora de silencio comprovado')
        x = [w['w'] for w in ws if w['t0'] - MARGEM + 0.005 < b0 and max(w['t0'] + 0.3, w['t1']) + MARGEM - 0.005 > a1]
        if x: falhas.append(f'corte {a1:.2f}-{b0:.2f} do bloco {i} a menos de {MARGEM:.2f} s da palavra {x}')
mn = float(M['duracao_min_s'])
if tl < mn:
    (avisos if PROVA else falhas).append(f'duracao {tl:.2f} s abaixo do minimo {mn:.0f} s' + (' (dispensado: --prova)' if PROVA else ''))
corpo = [b for b in B if not b['cold']]
dentro_corpo = lambda t: any(b['ini'] <= t <= b['fim'] for b in corpo)
kw = [w for w in ws if dentro_corpo(w['t0'])]
txt, pos = '', []
for w in kw:
    pos.append((len(txt), w['t0'])); txt += w['w'].lower() + ' '
LO = A.get('loops', [])
for rx in M.get('loops_abertos', []):
    for m in re.finditer(rx, txt):
        t = max(p[1] for p in pos if p[0] <= m.start())
        ok = [l for l in LO if abs(l['abre'] - t) < 3 and l.get('fecha') is not None and dentro_corpo(l['fecha']) and l['fecha'] > l['abre']]
        if not ok:
            falhas.append(f"loop aberto em {t:.2f} ('{txt[max(0, m.start() - 30):m.end() + 30].strip()}') sem fechamento: inclua o trecho que fecha e registre em loops")
for a in avisos: print('ATENCAO', a)
for f in falhas: print('FALHA', f)
print('PRONTO' if not falhas else 'NAO PRONTO')
sys.exit(1 if falhas else 0)
