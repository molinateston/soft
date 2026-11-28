"""Biblioteca de desenhos de EXEMPLO (espaco logico 1080x656 da tarja de baixo).
Para outra cliente: copie este arquivo para a pasta de trabalho (ou para scripts/) com outro nome,
troque os desenhos e aponte "desenhos" no ajustes.json para o nome do modulo.
Registro: CONCEITOS[id] = funcao que devolve lista de elementos (tudo novo)
ou (fixo, novo) quando o conceito acumula sobre o anterior do mesmo grupo (escada, hub).
Ids com parametro: 'nivel3' chama c_nivel(3); 'hub:skills' chama c_hub('skills').
Cores: 'w' = traco da marca, 'a' = acento (uma ideia por desenho em acento)."""
import math
from linhas import T, X, arco, circ, ret, seta, boneco


def bolha(x0, y0, x1, y1, cor='w', w=3):
    p = ret(x0, y0, x1, y1, 22)
    rabo = [(x0 + 50, y1), (x0 + 36, y1 + 30), (x0 + 80, y1)]
    return [T(p, cor, w), T(rabo, cor, w)]


def lupa(cx, cy, r, cor='w'):
    return [T(circ(cx, cy, r), cor), T([(cx + r * .7, cy + r * .7), (cx + r * 1.6, cy + r * 1.6)], cor, 4)]


def casa(cx, cy, s=1.0, cor='w'):
    w, h = 120 * s, 90 * s
    return [T([(cx - w / 2, cy), (cx - w / 2, cy + h), (cx + w / 2, cy + h), (cx + w / 2, cy)], cor),
            T([(cx - w / 2 - 16 * s, cy + 8 * s), (cx, cy - 60 * s), (cx + w / 2 + 16 * s, cy + 8 * s)], cor),
            T(ret(cx - 16 * s, cy + h - 44 * s, cx + 16 * s, cy + h), cor, 2)]


def computador(cx, cy, s=1.0, cor='w'):
    return [T(ret(cx - 60 * s, cy - 40 * s, cx + 60 * s, cy + 34 * s, 6), cor),
            T([(cx, cy + 34 * s), (cx, cy + 54 * s)], cor), T([(cx - 34 * s, cy + 56 * s), (cx + 34 * s, cy + 56 * s)], cor)]


def servidor(cx, cy, s=1.0, cor='w'):
    d = []
    for k in range(3):
        y = cy - 66 * s + k * 46 * s
        d += [T(ret(cx - 70 * s, y, cx + 70 * s, y + 36 * s, 6), cor), T(circ(cx + 48 * s, y + 18 * s, 5 * s), cor, 2),
              T([(cx - 50 * s, y + 18 * s), (cx + 10 * s, y + 18 * s)], cor, 2)]
    return d


# ---------- conceitos ----------
def c_perguntar():
    """IA usada so para perguntar (busca -> bolha com ?)"""
    d = [T(ret(90, 150, 430, 230, 40))] + lupa(140, 186, 18)
    d += [T([(190, 190), (380, 190)], 'w', 2), X('busca', 260, 285, 30)]
    d += [T(p, 'w', 3) for p in seta(455, 190, 560, 190)]
    d += bolha(595, 110, 905, 260, 'a')
    d += [X('?', 750, 182, 84, 'a', 'M'), X('IA só para perguntar', 750, 340, 34)]
    return d


def c_iceberg():
    """o que se ve (ponta) x o potencial (corpo submerso)"""
    agua = [(80, 150), (1000, 150)]
    ponta = [(450, 150), (500, 85), (540, 105), (580, 70), (630, 150)]
    corpo = [(450, 150), (380, 230), (330, 330), (360, 420), (480, 455), (640, 445), (740, 380), (760, 270), (700, 190), (630, 150)]
    return [T(agua, 'w', 2), T(ponta), X('perguntar', 290, 100, 30),
            T(corpo, 'a', 3), X('o potencial', 540, 300, 40, 'a', 'M'), X('muito maior', 540, 350, 34, 'a')]


def c_servidor():
    """seu computador desliga; o servidor (VPS) fica ligado 24 h"""
    d = computador(260, 230, 1.3) + [X('seu computador', 260, 360, 32), X('desliga', 260, 400, 30)]
    d += [T(p, 'w', 3) for p in seta(410, 230, 640, 230)]
    d += servidor(810, 230, 1.3, 'a') + [X('servidor (VPS)', 810, 360, 34, 'a', 'M'), X('ligado 24 h', 810, 400, 30, 'a')]
    return d


def c_casa_servidor():
    """sua casa (PC) x um servidor que trabalha por voce"""
    d = casa(250, 200, 1.3) + computador(250, 300, 0.5) + [X('na sua casa', 250, 420, 32)]
    d += [T([(540, 120), (540, 440)], 'w', 2)]
    d += servidor(810, 260, 1.2, 'a') + [X('no servidor', 810, 420, 34, 'a', 'M')]
    return d


# escada de N degraus que acumula (grupo continuo)
STEP_W, STEP_H, SX0, SY0 = 150, 54, 140, 430
NIVEIS = {1: ('Nível 1', 'o começo'), 2: ('Nível 2', 'o segundo passo'), 3: ('Nível 3', 'o terceiro passo'),
          4: ('Nível 4', 'quase lá'), 5: ('Nível 5', 'o topo')}


def degrau_top(i):
    x0 = SX0 + (i - 1) * STEP_W
    return x0, x0 + STEP_W, SY0 - i * STEP_H


def escada():
    p = [(SX0 - 60, SY0)]
    for i in range(1, 6):
        x0, x1, y = degrau_top(i)
        p += [(x0, SY0 - (i - 1) * STEP_H), (x0, y), (x1, y)]
    p += [(SX0 + 5 * STEP_W, SY0)]
    return [T(p, 'w', 3)] + [X(str(i), (degrau_top(i)[0] + degrau_top(i)[1]) / 2, degrau_top(i)[2] + 32, 30) for i in range(1, 6)]


def c_escada():
    return [X('5 níveis', 300, 70, 46, 'a', 'M')] + escada()


def c_nivel(n):
    fixo = escada()
    for k in range(1, n):
        x0, x1, y = degrau_top(k)
        fixo.append(T(circ((x0 + x1) / 2, y - 40, 14), 'w', 3))
    x0, x1, y = degrau_top(n)
    novo = [T(ret(x0 + 4, y + 4, x1 - 4, y + 54), 'a', 2), T(circ((x0 + x1) / 2, y - 40, 14), 'a', 3)]
    t, sub = NIVEIS[n]
    novo += [X(t, 90, 60, 40, 'a', 'M', 'lm'), X(sub, 90, 110, 32, 'w', 'L', 'lm')]
    return fixo, novo


# hub que acumula partes (grupo continuo)
HUB = (540, 250)
POS = {'memoria': (250, 170), 'regras': (250, 360), 'ferramentas': (830, 360), 'rotina': (830, 170)}
ROT = {'memoria': 'memória', 'regras': 'regras', 'ferramentas': 'ferramentas', 'rotina': 'rotina'}
ORDEM = list(POS)


def _parte(k, cor):
    hx, hy = HUB
    cx, cy = POS[k]
    a = math.atan2(cy - hy, cx - hx)
    p0 = (hx + 74 * math.cos(a), hy + 74 * math.sin(a))
    p1 = (cx - 50 * math.cos(a), cy - 50 * math.sin(a))
    return [T([p0, p1], cor, 2), T(circ(cx, cy, 40), cor), X(ROT[k], cx, cy + 74, 28, cor, 'M' if cor == 'a' else 'L')]


def c_hub(k=None):
    hx, hy = HUB
    hub = [T(circ(hx, hy, 70), 'w', 3), X('agente', hx, hy - 12, 34, 'w', 'M'), X('de IA', hx, hy + 24, 30)]
    if k is None:
        return [], hub
    fixo = list(hub)
    for kk in ORDEM[:ORDEM.index(k)]:
        fixo += _parte(kk, 'w')
    return fixo, _parte(k, 'a')


CONCEITOS = {'perguntar': c_perguntar, 'iceberg': c_iceberg, 'servidor': c_servidor, 'casa_servidor': c_casa_servidor,
             'escada': c_escada, 'nivel': c_nivel, 'hub': c_hub}


def montar(cid):
    """devolve (fixo, novo). 'cold:ID' desenha tudo do zero (sem parte fixa)."""
    if cid.startswith('cold:'):
        fx, nv = montar(cid[5:])
        return [], fx + nv
    if ':' in cid:
        base, arg = cid.split(':', 1)
        r = CONCEITOS[base](arg)
    elif cid.startswith('nivel') and cid[5:].isdigit():
        r = CONCEITOS['nivel'](int(cid[5:]))
    else:
        r = CONCEITOS[cid]()
    return r if isinstance(r, tuple) else ([], r)


def existe(cid):
    cid = cid[5:] if cid.startswith('cold:') else cid
    base = cid.split(':', 1)[0]
    if base.startswith('nivel') and base[5:].isdigit():
        return int(base[5:]) in NIVEIS
    return base in CONCEITOS
