"""Mini motor de line drawing com stroke reveal (PIL, supersampling 2x).
Cada desenho e uma lista de tracos. Traco = dict(pts=[(x,y),...], cor='w'|'a', w=largura)
ou texto = dict(txt=..., xy=(cx,cy), size=, cor=). Revelacao: os tracos aparecem em
sequencia pelo comprimento acumulado; texto entra inteiro no 1o quadro (rotulo curto segue o traco).
Coordenadas em espaco logico 1080 x 656 (a tarja de baixo). Cores e fontes vem da marca:
'w' = cores.traco, 'a' = cores.acento; fontes.desenho (L) e fontes.desenho_forte (M).
Chame configurar(M) antes de desenhar (o compor e o 05 ja chamam)."""
import math
from PIL import Image, ImageDraw, ImageFont
import comum as C

W, H = 1080, 656
SS = 2
_M = C.marca()
BRANCO = C.cor(_M, 'traco')
ACENTO = C.cor(_M, 'acento')
FONT_L = C.fonte_arq(_M, 'desenho')
FONT_M = C.fonte_arq(_M, 'desenho_forte')


def configurar(M):
    global BRANCO, ACENTO, FONT_L, FONT_M
    BRANCO, ACENTO = C.cor(M, 'traco'), C.cor(M, 'acento')
    FONT_L, FONT_M = C.fonte_arq(M, 'desenho'), C.fonte_arq(M, 'desenho_forte')
    _fc.clear()


_fc = {}


def font(size, peso='L'):
    k = (size, peso)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONT_M if peso == 'M' else FONT_L, int(size * SS))
    return _fc[k]


# ---------- primitivas que devolvem listas de pontos ----------
def arco(cx, cy, r, a0, a1, n=None, ry=None):
    ry = r if ry is None else ry
    n = n or max(8, int(abs(a1 - a0) / 360 * 64))
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def circ(cx, cy, r, ini=-90):
    return arco(cx, cy, r, ini, ini + 360)


def ret(x0, y0, x1, y1, r=0):
    if r <= 0:
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    p = []
    p += arco(x1 - r, y0 + r, r, -90, 0, 8)
    p += arco(x1 - r, y1 - r, r, 0, 90, 8)
    p += arco(x0 + r, y1 - r, r, 90, 180, 8)
    p += arco(x0 + r, y0 + r, r, 180, 270, 8)
    return [(x0 + r, y0)] + p + [(x0 + r, y0)]


def seta(x0, y0, x1, y1, cab=16):
    a = math.atan2(y1 - y0, x1 - x0)
    l = [(x1 - cab * math.cos(a - 0.5), y1 - cab * math.sin(a - 0.5)), (x1, y1),
         (x1 - cab * math.cos(a + 0.5), y1 - cab * math.sin(a + 0.5))]
    return [[(x0, y0), (x1, y1)], l]


def boneco(cx, cy, s=1.0):
    """pessoa minimal: cabeca + ombros. cy = centro da cabeca."""
    return [circ(cx, cy, 11 * s), arco(cx, cy + 40 * s, 24 * s, 200, 340)]


def T(pts, cor='w', w=3):
    return {'pts': pts, 'cor': cor, 'w': w}


def X(txt, cx, cy, size=30, cor='w', peso='L', anc='mm'):
    return {'txt': txt, 'xy': (cx, cy), 'size': size, 'cor': cor, 'peso': peso, 'anc': anc}


def comp(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


TXT_PESO = 140  # "comprimento" equivalente de um texto na fila de revelacao


def pesos(desenho):
    # v2: texto entra inteiro no 1o quadro (titulo primeiro); so os tracos entram na fila de revelacao
    # rotulos curtos (numero do degrau, A/B/C) seguem o traco a que pertencem
    return [comp(e['pts']) if 'pts' in e else (TXT_PESO if _curto(e) else 0) for e in desenho]


def _curto(e):
    return 'txt' in e and len(e['txt']) <= 2 and e['txt'] != '?'


def render(desenho, frac, base=None, alpha=1.0, fixo=None):
    """frac 0..1 da revelacao. Devolve RGBA W x H (ja reduzido do supersampling)."""
    img = base or Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    if fixo:
        _desenha(img, fixo, 1.0)
    _desenha(img, desenho, frac)
    out = img.resize((W, H), Image.LANCZOS)
    if alpha < 1:
        a = out.getchannel('A').point(lambda v: int(v * alpha))
        out.putalpha(a)
    return out


def _desenha(img, desenho, frac):
    d = ImageDraw.Draw(img)
    ps = pesos(desenho)
    tot = sum(ps) or 1
    alvo = frac * tot
    acc = 0
    for e, p in zip(desenho, ps):
        if 'pts' not in e and not _curto(e):
            f = 1.0
        elif acc >= alvo:
            continue
        else:
            f = min(1.0, (alvo - acc) / p) if p else 1
        acc += p
        cor = ACENTO if e.get('cor') == 'a' else BRANCO
        if 'pts' in e:
            pts = e['pts']
            if f < 1:
                lim = f * p
                out = [pts[0]]
                run = 0
                for i in range(len(pts) - 1):
                    seg = math.dist(pts[i], pts[i + 1])
                    if run + seg >= lim:
                        t = (lim - run) / seg if seg else 1
                        out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t,
                                    pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t))
                        break
                    run += seg
                    out.append(pts[i + 1])
                pts = out
            sp = [(x * SS, y * SS) for x, y in pts]
            wd = int(e.get('w', 3) * SS)
            if len(sp) >= 2:
                d.line(sp, fill=cor + (255,), width=wd, joint='curve')
                r = wd / 2
                for q in (sp[0], sp[-1]):
                    d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=cor + (255,))
        else:
            a = int(255 * f)
            x, y = e['xy']
            d.text((x * SS, y * SS), e['txt'], font=font(e['size'], e.get('peso', 'L')),
                   fill=cor + (a,), anchor=e.get('anc', 'mm'))
