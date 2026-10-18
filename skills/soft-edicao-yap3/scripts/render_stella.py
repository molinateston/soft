import json,re,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
def render(source,out,top=315,title_px=85,secondary_px=54):
 global P,FONTES,VERDE,W,H,_fc
 source=Path(source);out=Path(out);out.mkdir(parents=True,exist_ok=True)
 P=json.loads((source/'plano.json').read_text());P['titulo']=dict(P['titulo'],l1_px=title_px,l2_px=secondary_px);W,H=1080,1920;VERDE=P['verde'];_fc={}
 FONTES={'black':str(source/'fontes/InterDisplay-BlackItalic.otf'),'kalam':str(source/'fontes/Kalam-Bold.ttf'),'advb':str(source/'fontes/Advercase-Bold.ttf'),'adv':str(source/'fontes/Advercase-Regular.ttf')}
 boxes=[]
 for i in (0,1):
  im=estado_titulo(P['ganchos'][0],bool(i));im.save(out/f'original{i}.png')
  box=im.getbbox();shift=top-box[1];new=Image.new('RGBA',im.size);new.alpha_composite(im,(0,shift));new.save(out/f'estado{i}.png');boxes.append(new.getbbox())
  assert new.getbbox()[3]<=1605,'Texto fora do recorte central'
 (out/'caixas.json').write_text(json.dumps(boxes))

def fonte(k, px):
    if (k, px) not in _fc:
        _fc[k, px] = ImageFont.truetype(FONTES[k], px)
    return _fc[k, px]

def tokens(txt):
    pecas = [(m.group(1) or m.group(2), m.group(1) is not None) for m in re.finditer('\\[([^\\]]+)\\]|([^\\[\\]]+)', txt)]
    palavras, cur = ([], [])
    for t, v in pecas:
        for i, parte in enumerate(re.split('(\\s+)', t)):
            if not parte:
                continue
            if parte.isspace():
                if cur:
                    palavras.append(cur)
                    cur = []
            else:
                cur.append((parte, v))
    if cur:
        palavras.append(cur)
    return palavras

def larg(f, w):
    return sum((f.getlength(x) for x, _ in w))

def linhas(txt, f, maxw):
    if '\n' in txt:
        return [ln for part in txt.split('\n') for ln in linhas(part, f, maxw)]
    sp = f.getlength(' ')
    ws = tokens(txt)

    def lw(ln):
        return sum((larg(f, w) for w in ln)) + sp * (len(ln) - 1)
    ls, cur = ([], [])
    for w in ws:
        if cur and lw(cur + [w]) > maxw:
            ls.append(cur)
            cur = []
        cur.append(w)
    if cur:
        ls.append(cur)
    while len(ls) > 1 and len(ls[-2]) > 2 and (len(ls[-1]) == 1 or lw(ls[-2]) - lw(ls[-1]) > maxw * 0.45) and (lw([ls[-2][-1]] + ls[-1]) <= maxw) and (lw([ls[-2][-1]] + ls[-1]) < lw(ls[-2])):
        ls[-1].insert(0, ls[-2].pop())
    return ls

def desenha_texto(cv, txt, k, px, y, maxw=960, cor='#ffffff', lh=1.12):
    f = fonte(k, px)
    sp = f.getlength(' ')
    d = ImageDraw.Draw(cv)
    for ln in linhas(txt, f, maxw):
        lw = sum((larg(f, w) for w in ln)) + sp * (len(ln) - 1)
        x = (W - lw) / 2
        for w in ln:
            for t, v in w:
                d.text((x, y), t, font=f, fill=VERDE if v else cor)
                x += f.getlength(t)
            x += sp
        y += round(px * lh)
    return y

def com_sombra(cv):
    a = cv.split()[3]
    sh = Image.new('RGBA', cv.size, (0, 0, 0, 0))
    for blur, op, dy in ((10, 0.55, 5), (3, 0.45, 2)):
        m = a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op))
        lay = Image.new('RGBA', cv.size, (0, 0, 0, 0))
        lay.putalpha(m)
        sh.alpha_composite(lay, (0, dy))
    sh.alpha_composite(cv)
    return sh

def estado_titulo(g, com_l2):
    t = P['titulo']
    cv = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    p1, p2 = (t['l1_px'], t['l2_px'])
    y0 = round(t['y0'] * H)
    if y0 + len(linhas(g['l1'], fonte(t['l1_fonte'], p1), 960)) * round(p1 * 1.08) + 10 + len(linhas(g['l2'], fonte(t['l2_fonte'], p2), 960)) * round(p2 * 1.05) > 390:
        raise ValueError("Texto excede o molde. Resolver quebras com direcao antes de mudar tamanho.")
    y = desenha_texto(cv, g['l1'], t['l1_fonte'], p1, y0, lh=1.08)
    if com_l2:
        desenha_texto(cv, g['l2'], t['l2_fonte'], p2, y + 10, lh=1.05)
    return com_sombra(cv)

if __name__=="__main__":render(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 315)
