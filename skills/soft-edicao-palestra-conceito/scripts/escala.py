"""Amplia (~1,3x) e centraliza cada grupo de desenhos na zona util da tarja de baixo.
Traco continua fino (largura nao escala); texto escala junto. A transformacao e a mesma
para todo o grupo (escada, agente), calculada pelo estado final do grupo, pra nada pular."""
from PIL import ImageDraw, Image
import linhas as L

ALVO = 1.30
ZX0, ZX1, ZY0, ZY1 = 66, 1014, 12, 505   # margem de 60 px (66 no eixo do traco); abaixo de ~505 a interface do Instagram cobre
_d = ImageDraw.Draw(Image.new('L', (1, 1)))


def _horizonte(e):
    p = e['pts']
    return len(p) == 2 and abs(p[0][1] - p[1][1]) < 1 and abs(p[0][0] - p[1][0]) > 800


def bbox(els):
    xs, ys = [], []
    for e in els:
        if 'pts' in e:
            if _horizonte(e):
                continue
            xs += [q[0] for q in e['pts']]; ys += [q[1] for q in e['pts']]
        else:
            f = L.font(e['size'], e.get('peso', 'L'))
            x, y = e['xy']
            b = _d.textbbox((x * L.SS, y * L.SS), e['txt'], font=f, anchor=e.get('anc', 'mm'))
            xs += [b[0] / L.SS, b[2] / L.SS]; ys += [b[1] / L.SS, b[3] / L.SS]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else (0, 0, 0, 0)


def calc(els):
    if not els: return 1.0, 0.0, 0.0  # estado sem apoio previsto no storyboard
    x0, y0, x1, y1 = bbox(els)
    s = min(ALVO, (ZX1 - ZX0) / (x1 - x0), (ZY1 - ZY0) / (y1 - y0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    tx, ty = (ZX0 + ZX1) / 2 - cx * s, (ZY0 + ZY1) / 2 - cy * s
    return s, tx, ty


def aplicar(els, tr):
    s, tx, ty = tr
    out = []
    for e in els:
        e = dict(e)
        if 'pts' in e:
            pts = [(x * s + tx, y * s + ty) for x, y in e['pts']]
            if _horizonte(e):
                pts = [(min(max(x, 66), 1014), y) for x, y in pts]
            e['pts'] = pts
        else:
            x, y = e['xy']
            e['xy'] = (x * s + tx, y * s + ty)
            e['size'] = e['size'] * s
        out.append(e)
    return out
