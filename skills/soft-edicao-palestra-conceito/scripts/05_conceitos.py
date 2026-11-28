"""Etapa 5. Conceitos da tarja de baixo: um line drawing por ideia, entrando quando a fala diz a ideia.
Le ajustes.json > conceitos [{id, grupo, ts (tempo ABSOLUTO da fonte em que a fala diz a ideia), prova
(palavra que tem que estar na fala perto de ts), fala, mostra, reveal?}], cold_conceito (id do desenho do
cold open), desenhos (modulo, padrao desenhos_exemplo; um .py na pasta de trabalho tem prioridade).
uso: python3 05_conceitos.py TRAB
saidas: conceitos.json (tempo de saida), conceitos-tabela.txt, conceitos-previa.jpg
criterio de pronto (PRONTO, exit 0): todo id existe no modulo, todo ts cai dentro de um bloco do corpo,
a palavra de prova aparece na transcricao a ate 3 s de ts, todo desenho cabe na zona util,
nenhum slot menor que reveal + 1 s. Slot acima de 20 s gera ATENCAO (conceito parado)."""
import sys, unicodedata, re
from PIL import Image, ImageDraw
import comum as C
import tarjas

T = C.trab_arg()
M, A = C.marca(T), C.ajustes(T)
CC = C.lj(T, 'cortes.json')
SPD, B = CC['velocidade'], CC['blocos']
D = tarjas.modulo_desenhos(T, A.get('desenhos'))
corpo = [b for b in B if not b['cold']]


def mapear(ts):
    """tempo absoluto da fonte -> tempo de saida, no 1o bloco do corpo que contem ts"""
    for b in corpo:
        acc = 0.0
        for a, c in b['keep']:
            if ts < a and b['ini'] - 0.01 <= ts: return b['t0'] + acc / SPD
            if a <= ts <= c: return b['t0'] + (acc + ts - a) / SPD
            acc += c - a
    return None


norm = lambda s: re.sub(r'[^a-z0-9%]', '', ''.join(ch for ch in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(ch) != 'Mn'))
ws = C.palavras_bruto(T)
f, av, cs = [], [], []
if CC.get('cold_open'):
    if not A.get('cold_conceito'): f.append('tem cold_open mas falta cold_conceito')
    else: cs.append(dict(id='cold:' + A['cold_conceito'], grupo='cold', ts=CC['cold_open'][0], t=0.0, fala='(cold open)', mostra=A['cold_conceito']))
for c in A.get('conceitos', []):
    t = mapear(c['ts'])
    if t is None: f.append(f"{c['id']}: ts {c['ts']} fora dos blocos do corpo"); continue
    p = norm(c.get('prova', ''))
    perto = [norm(w['w']) for w in ws if abs(w['t0'] - c['ts']) <= 3]
    if not p: f.append(f"{c['id']}: falta a palavra de prova (o que a fala diz quando o desenho entra)")
    elif not any(p in x or x in p and len(x) > 3 for x in perto):
        f.append(f"{c['id']}: '{c['prova']}' nao aparece na fala a 3 s de {c['ts']} (perto: {' '.join(w['w'] for w in ws if abs(w['t0'] - c['ts']) <= 3)})")
    cs.append(dict(c, t=round(t, 3)))
for c in cs:
    if not D.existe(c['id']): f.append(f"id {c['id']} nao existe no modulo {D.__name__}")
if f:
    for x in f: print('FALHA', x)
    print('NAO PRONTO'); sys.exit(1)
cs.sort(key=lambda c: c['t'])
C.gj(T, 'conceitos.json', dict(headline=A['headline'], conceitos=cs))
BX = tarjas.Baixo(M, cs, D)
z = M['area_segura']
lin = []
for i, c in enumerate(cs):
    fim = cs[i + 1]['t'] if i + 1 < len(cs) else CC['dur_saida']
    slot = fim - c['t']
    x0, y0, x1, y1 = BX.bbox_final(c['id'])
    if (x1 > x0 or y1 > y0) and (x0 < z['margem_x'] - 1 or x1 > C.W - z['margem_x'] + 1 or y1 > z['desenho_y_max'] + 1):
        f.append(f"{c['id']}: desenho fora da zona util ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
    rv = c.get('reveal', BX.REVEAL)
    if slot < rv + 1: f.append(f"{c['id']}: slot {slot:.2f} s menor que reveal + 1 s")
    if slot > 20: av.append(f"{c['id']}: {slot:.1f} s no ar; veja se a fala troca de ideia no meio")
    lin.append(f"{c['id']:18s} {c['grupo']:8s} entra {c['t']:7.2f} sai {fim:7.2f} slot {slot:5.2f} | fala: {c.get('fala', '')} | mostra: {c.get('mostra', '')}")
open(f'{T}/conceitos-tabela.txt', 'w').write('\n'.join(lin) + '\n')
print('\n'.join(lin))
cols = 2; rows = -(-len(cs) // cols)
pv = Image.new('RGB', (cols * 540, rows * 360), (90, 90, 90))
for i, c in enumerate(cs):
    im = Image.new('RGBA', (C.W, C.HB), BX.bg + (255,)); im.alpha_composite(BX.final(c['id'])); im = im.convert('RGB').resize((540, 328))
    pv.paste(im, ((i % cols) * 540, (i // cols) * 360))
    ImageDraw.Draw(pv).text(((i % cols) * 540 + 8, (i // cols) * 360 + 332), f"{c['id']} @ {c['t']:.1f}s", fill=(255, 255, 255))
pv.save(f'{T}/conceitos-previa.jpg', quality=88)
for x in av: print('ATENCAO', x)
for x in f: print('FALHA', x)
print('PRONTO' if not f else 'NAO PRONTO', '-> conceitos.json, conceitos-previa.jpg')
sys.exit(1 if f else 0)
