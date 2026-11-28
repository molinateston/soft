"""Tarja de cima (headline + sub, estatica) e legenda (1 palavra por vez). Cores e fontes da marca."""
from PIL import Image, ImageDraw, ImageFont
import comum as C


def quebra(d, txt, f, wmax):
    out, cur = [], ''
    for w in txt.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= wmax: cur = t
        else: out.append(cur); cur = w
    return [x for x in out + [cur] if x]


def topo(M, HL):
    """devolve (imagem 1080 x YV, log com linhas, larguras e bbox)"""
    tz = M['tamanhos']
    img = Image.new('RGB', (C.W, C.YV), C.cor(M, 'tarja'))
    d = ImageDraw.Draw(img)
    fh = ImageFont.truetype(C.fonte_arq(M, 'headline'), int(HL.get('size', tz['headline'])))
    fs = ImageFont.truetype(C.fonte_arq(M, 'sub'), int(HL.get('sub_size', tz['sub'])))
    wmax = tz['largura_max_linha']
    hl = HL.get('linhas') or quebra(d, HL['headline'], fh, wmax)
    sl = HL.get('sub_linhas') or quebra(d, HL['sub'], fs, wmax - 40)
    lh, ls = int(fh.size * 1.12), int(fs.size * 1.3)
    bloco = len(hl) * lh + 34 + len(sl) * ls
    y = 190 + (C.YV - 190 - 40 - bloco) // 2    # abaixo da interface do Instagram no topo
    dest = {x.strip('.,?!') for x in HL.get('destaque', [])}
    txt_cor, ac = C.cor(M, 'texto'), C.cor(M, 'acento')
    bb = [9999, 9999, 0, 0]
    larg = []
    for ln in hl:
        wtot = d.textlength(ln, font=fh); larg.append(round(wtot))
        x = (C.W - wtot) / 2
        for w in ln.split(' '):
            d.text((x, y), w, font=fh, fill=ac if w.strip('.,?!') in dest else txt_cor, anchor='la')
            b = d.textbbox((x, y), w, font=fh, anchor='la'); bb = [min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3])]
            x += d.textlength(w + ' ', font=fh)
        y += lh
    y += 34
    for ln in sl:
        d.text((C.W / 2, y), ln, font=fs, fill=C.cor(M, 'sub'), anchor='ma')
        b = d.textbbox((C.W / 2, y), ln, font=fs, anchor='ma'); bb = [min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3])]
        larg.append(round(d.textlength(ln, font=fs)))
        y += ls
    return img, dict(linhas=hl, sub_linhas=sl, larguras=larg, bbox=[round(v) for v in bb], size=fh.size, sub_size=fs.size)


class Legenda:
    def __init__(self, M, words, corte=0.0):
        self.f = ImageFont.truetype(C.fonte_arq(M, 'legenda'), int(M['tamanhos']['legenda']))
        self.fill, self.stroke = C.cor(M, 'legenda') + (255,), C.cor(M, 'legenda_contorno') + (255,)
        MIN_W = float(M['legenda'].get('min_s', 0.12))
        self.disp, last = [], -1
        for i, w in enumerate(words):
            s = w['t0'] if last < 0 else max(w['t0'], last + MIN_W)
            nxt = words[i + 1]['t0'] if i + 1 < len(words) else w['t1'] + 0.5
            e = nxt if nxt - w['t1'] <= 0.5 else w['t1'] + 0.3
            e = max(e, s + MIN_W)
            if corte and s < corte < e: e = corte     # legenda do cold open nao atravessa a emenda
            self.disp.append((s, e, w['w']))
            last = s
        self._c = {}

    def img(self, txt):
        if txt not in self._c:
            tw = int(ImageDraw.Draw(Image.new('L', (1, 1))).textlength(txt, font=self.f)) + 40
            im = Image.new('RGBA', (tw, 110), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((tw / 2, 55), txt, font=self.f, fill=self.fill, anchor='mm', stroke_width=7, stroke_fill=self.stroke)
            self._c[txt] = im
        return self._c[txt]

    def em(self, t):
        cur = [x for x in self.disp if x[0] <= t < x[1]]
        return cur[-1][2] if cur else None


def modulo_desenhos(trab, nome):
    """carrega o modulo de desenhos: primeiro da pasta de trabalho, depois de scripts/"""
    import importlib, sys
    for p in (trab, C.SCRIPTS):
        if p not in sys.path: sys.path.insert(0, p) if p == trab else sys.path.append(p)
    return importlib.import_module(nome or 'desenhos_exemplo')


class Baixo:
    """tarja de baixo: line drawing do conceito vigente com stroke reveal. Troca entre conceitos = corte seco."""
    REVEAL = 1.4

    def __init__(self, M, conceitos, D):
        import linhas as L, escala as E
        L.configurar(M)
        self.L, self.C, self.bg = L, conceitos, C.cor(M, 'tarja')
        des = {c['id']: D.montar(c['id']) for c in conceitos}
        self.TR = {}
        for g in dict.fromkeys(c['grupo'] for c in conceitos):   # 1 escala por grupo, pelo estado final do grupo
            els = [e for c in conceitos if c['grupo'] == g for e in des[c['id']][0] + des[c['id']][1]]
            self.TR[g] = E.calc(els)
        self.DES = {c['id']: (E.aplicar(des[c['id']][0], self.TR[c['grupo']]), E.aplicar(des[c['id']][1], self.TR[c['grupo']])) for c in conceitos}
        self._st = {}
        self.D = D

    def bbox_final(self, cid):
        import escala as E
        fx, nv = self.DES[cid]
        return E.bbox(fx + nv)

    def final(self, cid):
        if cid not in self._st:
            fx, nv = self.DES[cid]
            self._st[cid] = self.L.render(nv, 1.0, fixo=fx)
        return self._st[cid]

    def em(self, t):
        idx = max([i for i, c in enumerate(self.C) if c['t'] <= t] or [0])
        c = self.C[idx]
        frac = min(1.0, max(0.0, (t - c['t']) / c.get('reveal', self.REVEAL)))
        if idx == 0: frac = 1.0    # o 1o desenho ja entra inteiro: o quadro 0 e a capa e precisa funcionar sozinho
        din = self.D.montar_tempo(c['id'], t-c['t']) if hasattr(self.D, 'montar_tempo') else None
        if din is not None:
            import escala as E
            fx, nv = [E.aplicar(els, self.TR[c['grupo']]) for els in din]
            img = self.L.render(nv, 1., fixo=fx)
        elif frac >= 1.0: img = self.final(c['id'])
        else:
            fx, nv = self.DES[c['id']]
            img = self.L.render(nv, frac, fixo=fx)
        out = Image.new('RGBA', (C.W, C.HB), self.bg + (255,))
        out.alpha_composite(img)
        return out.convert('RGB')
