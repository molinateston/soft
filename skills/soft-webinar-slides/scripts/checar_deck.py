#!/usr/bin/env python3
"""checar_deck.py: a conferência mecânica do deck. Renderiza o deck.html em
1920x1080 no Chromium (Playwright), com todos os cliques abertos, e mede.

Reprova (código 1) quando:
  - texto sai do slide, fica cortado pela caixa ou se sobrepõe a outro texto;
  - fonte abaixo do piso (--min-fonte, padrão 30px numa tela de 1920);
  - mais de 7 cliques num slide;
  - nota sem Objetivo, Abre com ou Fecha com, ou com número de "Clique N" diferente dos cliques da tela;
  - contraste abaixo de 4,5 (texto menor que 40px) ou 3 (40px ou mais); texto HTML sobre forma SVG é medido
    contra o preenchimento liso do SVG; com gradiente ou imagem por baixo vira só AVISO (rótulo com fundo HTML próprio é medido);
  - tabela da oferta cuja soma não bate com o total;
  - o total parcelado (parcela vezes número de parcelas) aparece em algum slide;
  - travessão na tela ou na nota;
  - a cor reservada aparece fora da tarja, do risco do preço e do rótulo BÔNUS;
  - slide com mais palavras que o teto (padrão 40, o teto único; oferta, bônus e escada ficam de fora) ou bloco com mais de 20
    (não contam como palavra: texto dentro de data-imagem, rótulo de desenho em data-vaga, .legenda, .tarja e .rot-bonus,
    e célula de grade repetida 6 vezes ou mais);
  - lacuna, colchete ou marcador {{...}} visível na tela ([A CONFIRMAR], [DO DONO] e afins);
  - imagem quebrada ou imagem que entra por clique (título e imagem já estão na tela quando o slide abre).
Avisa (sem reprovar): vaga de print ou de cena (data-vaga) ainda sem imagem.
Imprime sempre a linha "menor fonte: Npx (slide NN: ...)", a menor fonte medida nos slides conferidos.

Uso:
  python3 scripts/checar_deck.py <pasta-ou-deck.html> [--png <pasta>] [--estados] [--max-palavras 40] [--min-fonte 30]
O PNG leva o número do slide (data-num do slide desenhado; senão a posição).
"""
import argparse
import re
import sys
from pathlib import Path

JS = r"""
(i) => {
  const s = document.querySelectorAll('.slide')[i];
  const R = s.getBoundingClientRect();
  const out = {layout: s.dataset.layout, num: s.dataset.num || String(i + 1).padStart(2, '0'), texts: [], clip: [], imgs: [], cor: [], vagas: 0, tabelas: [], cliques: 0, nota: ''};
  const parse = (c) => { const m = (c||'').match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(parseFloat); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; };
  const bgOf = (el) => { for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0.5) return c; if (e === s) break; } return parse(getComputedStyle(s).backgroundColor); };
  // texto HTML sobre forma SVG: o fundo que o texto vê é o preenchimento do SVG, que bgOf não enxerga
  const temBgHtml = (el) => { for (let e = el; e && e !== s; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0.5) return true; } return false; };
  const sobreSvg = (el, rects) => {  // null: sem SVG por baixo; {fill: cor}: preenchimento liso; {fill: null}: gradiente ou imagem
    if (!rects.length || temBgHtml(el)) return null;
    const r = rects[0]; const x = R.x + r.x + r.w / 2, y = R.y + r.y + r.h / 2;
    for (const e of document.elementsFromPoint(x, y)) {
      if (e === el || el.contains(e) || e.contains(el)) continue;
      if (e === s) return null;
      if (e instanceof SVGElement) {
        if (e instanceof SVGSVGElement) continue;
        const cs = getComputedStyle(e); const f = parse(cs.fill);
        if (!f) { if ((cs.fill || '').startsWith('url')) return {fill: null}; continue; }
        if (f.a * (parseFloat(cs.fillOpacity) || 0) > 0.5) return {fill: {r: f.r, g: f.g, b: f.b, a: 1}};
        continue;
      }
      const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0.5) return null;
    }
    return null;
  };
  const path = (el) => { const p = []; for (let e = el; e && e !== s; e = e.parentElement) p.unshift(e.tagName.toLowerCase() + (e.classList.length ? '.' + [...e.classList].filter(c=>!['reveal','on'].includes(c)).join('.') : '')); return p.slice(-3).join('>'); };
  const reserv = getComputedStyle(document.documentElement).getPropertyValue('--reservada').trim();
  const RES = (() => { const d = document.createElement('div'); d.style.color = reserv; document.body.appendChild(d); const c = parse(getComputedStyle(d).color); d.remove(); return c; })();
  out.cliques = Math.max(0, ...[...s.querySelectorAll('[data-click]')].map(e => +e.dataset.click));
  const n = s.querySelector('aside.notes'); out.nota = n ? n.textContent : '';
  const walk = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
  let t; let idx = 0;
  while ((t = walk.nextNode())) {
    const txt = t.nodeValue.replace(/\s+/g, ' ').trim(); if (!txt) continue;
    const el = t.parentElement; if (el.closest('aside.notes')) continue;
    const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const rg = document.createRange(); rg.selectNodeContents(t);
    const rects = [...rg.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5).map(r => ({x:r.x-R.x, y:r.y-R.y, w:r.width, h:r.height}));
    const bloco = el.closest('li, .tl, .degrau, .linha, .aprende, .col, [data-click], .principal, .promessa, .frase, div') ;
    out.texts.push({txt, size: parseFloat(cs.fontSize), color: parse(cs.color), bg: bgOf(el), svg: el.closest('svg') ? null : sobreSvg(el, rects), rects, path: path(el), id: idx++,
      bloco: bloco ? (bloco.dataset.bid || (bloco.dataset.bid = 'b' + Math.random().toString(36).slice(2,8))) : 'x',
      sobrepoe: !!el.closest('[data-sobrepoe]'), linhaTabela: !!el.closest('.tl'), imagem: !!el.closest('[data-imagem]'), rotulo: !!el.closest('[data-vaga], .legenda, .tarja, .rot-bonus')});
  }
  s.querySelectorAll('*').forEach(el => {
    if (el.closest('aside.notes')) return;
    const cs = getComputedStyle(el);
    if (['hidden','clip','auto','scroll'].includes(cs.overflowX) || ['hidden','clip','auto','scroll'].includes(cs.overflowY)) {
      if (el.textContent.trim() && (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2)) out.clip.push(path(el) + ` (${el.scrollWidth}x${el.scrollHeight} em ${el.clientWidth}x${el.clientHeight})`);
    }
    const papel = el.closest('.tarja, .risco-linha, .rot-bonus');
    for (const prop of ['color','backgroundColor','borderTopColor','borderLeftColor']) {
      const v = cs[prop];
      if (prop.startsWith('border') && parseFloat(cs[prop.replace('Color','Width')]) === 0) continue;
      if (!v || !reserv) continue;
      const a = parse(v); const b = RES;
      if (a && b && a.a > 0 && Math.abs(a.r-b.r)+Math.abs(a.g-b.g)+Math.abs(a.b-b.b) < 6 && !papel && !(prop==='color' && el.closest('.tarja,.rot-bonus'))) {
        if (prop === 'color' && !el.textContent.trim()) continue;
        out.cor.push(path(el) + ' ' + prop);
      }
    }
  });
  s.querySelectorAll('img').forEach(im => out.imgs.push({ok: im.complete && im.naturalWidth > 0, src: im.getAttribute('src'), porClique: !!im.closest('[data-click]')}));
  out.vagas = s.querySelectorAll('[data-vaga]').length;
  s.querySelectorAll('[data-geometria]').forEach(tb => {
    const vals = [...tb.querySelectorAll('[data-valor]')].map(e => parseFloat(e.dataset.valor));
    const tot = tb.parentElement.querySelector('[data-total]') || tb.querySelector('[data-total]');
    out.tabelas.push({soma: vals.reduce((a,b)=>a+(isNaN(b)?NaN:b),0), total: tot ? parseFloat(tot.dataset.total) : null, mostrado: tot ? tot.textContent.trim() : '', linhas: vals.length});
  });
  return out;
}
"""

LACUNA = re.compile(r"\[|\]|\{\{|\}\}|A CONFIRMAR|DO DONO|A DEFINIR|PREENCHER|lorem", re.I)
DINHEIRO = re.compile(r"R\$\s?([\d.]+(?:,\d{1,2})?)")


def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c["r"]) + 0.7152 * ch(c["g"]) + 0.0722 * ch(c["b"])


def contraste(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def valor(txt):
    return float(txt.replace(".", "").replace(",", "."))


def inter(a, b):
    x = max(0, min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]))
    y = max(0, min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"]))
    return x * y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alvo")
    ap.add_argument("--png")
    ap.add_argument("--max-palavras", type=int, default=40)
    ap.add_argument("--max-bloco", type=int, default=20)
    ap.add_argument("--min-fonte", type=float, default=30.0,
                    help="piso de fonte em px numa tela de 1920 (padrão 30; o rascunho de texto usa 24)")
    ap.add_argument("--estados", action="store_true", help="com --png, grava também um PNG por clique (slide-NN-c0.png ...)")
    a = ap.parse_args()
    alvo = Path(a.alvo)
    html = alvo / "deck.html" if alvo.is_dir() else alvo
    from playwright.sync_api import sync_playwright

    falhas, avisos, dados = [], [], []
    with sync_playwright() as p:
        try:
            br = p.chromium.launch()
        except Exception:
            br = p.chromium.launch(executable_path="/snap/bin/chromium")
        pg = br.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        pg.goto(html.resolve().as_uri())
        pg.wait_for_function("window.deckPronto === true", timeout=20000)
        pg.add_style_tag(content="*{transition:none!important;animation:none!important}#painel-notas{display:none!important}")
        n = pg.evaluate("window.deck.count")
        if a.png:
            Path(a.png).mkdir(parents=True, exist_ok=True)
        for i in range(n):
            pg.evaluate(f"window.deck.show({i})")
            pg.wait_for_timeout(60)
            dados.append(pg.evaluate(JS, i))
            if a.png:
                num = dados[-1]["num"]
                pg.screenshot(path=str(Path(a.png) / f"slide-{num}.png"))
                if a.estados:
                    for k in range(pg.evaluate(f"window.deck.cliques({i})") + 1):
                        pg.evaluate(f"window.deck.show({i}, {k})")
                        pg.wait_for_timeout(40)
                        pg.screenshot(path=str(Path(a.png) / f"slide-{num}-c{k}.png"))
        br.close()

    parcelados = set()
    for d in dados:
        for tx in d["texts"]:
            m = re.search(r"(\d+)\s*x\s*(?:de\s*)?R\$\s?([\d.]+,\d{2}|[\d.]+)", tx["txt"], re.I)
            if m:
                parcelados.add(round(int(m.group(1)) * valor(m.group(2)), 2))

    for i, d in enumerate(dados, 1):
        tag = f"slide {d['num']} ({d['layout'] or 'desenho'})"
        # não contam como palavra de tela: texto de data-imagem (pictograma, grade), rótulo de desenho (vaga, legenda, tarja,
        # rótulo de bônus) e célula repetida 6 vezes ou mais
        rep = {}
        for x in d["texts"]:
            rep[x["txt"]] = rep.get(x["txt"], 0) + 1
        visto = set()
        lidos = []
        for x in d["texts"]:
            if x.get("imagem") or x.get("rotulo"):
                continue
            if rep[x["txt"]] >= 6:
                if x["txt"] in visto:
                    continue
                visto.add(x["txt"])
            lidos.append(x)
        tela = " ".join(x["txt"] for x in lidos)
        svg_sem_medida = []
        for x in d["texts"]:
            if x["size"] < a.min_fonte - 0.5:
                falhas.append(f"{tag}: fonte {x['size']:.0f}px abaixo do piso de {a.min_fonte:g}px em {x['path']}: \"{x['txt'][:40]}\"")
            for r in x["rects"]:
                if r["x"] < -1 or r["y"] < -1 or r["x"] + r["w"] > 1921 or r["y"] + r["h"] > 1081:
                    falhas.append(f"{tag}: texto sai do slide em {x['path']}: \"{x['txt'][:40]}\"")
                    break
            svg = x.get("svg")
            if svg and not svg.get("fill"):
                svg_sem_medida.append(x["txt"][:30])
            elif x["color"] and x["bg"]:
                cr = contraste(x["color"], svg["fill"] if svg else x["bg"])
                piso = 3.0 if x["size"] >= 40 else 4.5
                if cr < piso:
                    falhas.append(f"{tag}: contraste {cr:.1f} abaixo de {piso} em {x['path']}: \"{x['txt'][:40]}\"")
            if LACUNA.search(x["txt"]):
                falhas.append(f"{tag}: lacuna ou colchete visível na tela: \"{x['txt'][:50]}\"")
            if "—" in x["txt"] or "–" in x["txt"]:
                falhas.append(f"{tag}: travessão na tela: \"{x['txt'][:50]}\"")
            for m in ([] if x.get("linhaTabela") else DINHEIRO.finditer(x["txt"])):
                if round(valor(m.group(1)), 2) in parcelados:
                    falhas.append(f"{tag}: o total parcelado aparece na tela ({m.group(0)}). Mostre só a parcela e o à vista.")
        if svg_sem_medida:
            avisos.append(f"{tag}: contraste não medido em texto HTML sobre SVG com gradiente ou imagem ({'; '.join(svg_sem_medida[:3])}): "
                          "olhe o PNG, ou dê ao rótulo um fundo HTML próprio (o script passa a medir).")
        ts = [x for x in d["texts"] if not x["sobrepoe"]]
        for j in range(len(ts)):
            for k in range(j + 1, len(ts)):
                if ts[j]["bloco"] == ts[k]["bloco"] and ts[j]["path"] == ts[k]["path"]:
                    continue
                for ra in ts[j]["rects"]:
                    for rb in ts[k]["rects"]:
                        ar = inter(ra, rb)
                        if ar > 0.15 * min(ra["w"] * ra["h"], rb["w"] * rb["h"]):
                            falhas.append(f"{tag}: texto sobreposto: \"{ts[j]['txt'][:30]}\" e \"{ts[k]['txt'][:30]}\"")
                            break
                    else:
                        continue
                    break
        for c in d["clip"]:
            falhas.append(f"{tag}: texto cortado pela caixa em {c}")
        if d["cliques"] > 7:
            falhas.append(f"{tag}: {d['cliques']} cliques; o máximo é 7.")
        nota = d["nota"]
        if not nota.strip():
            falhas.append(f"{tag}: slide sem nota do apresentador.")
        else:
            for campo in ("Objetivo:", "Abre com:", "Fecha com:"):
                if campo not in nota:
                    falhas.append(f"{tag}: nota sem \"{campo}\".")
            nc = len(re.findall(r"^Clique \d+:", nota, re.M))
            if nc != d["cliques"]:
                falhas.append(f"{tag}: a tela tem {d['cliques']} cliques e a nota descreve {nc}.")
            if "—" in nota or "–" in nota:
                falhas.append(f"{tag}: travessão na nota.")
        for c in d["cor"]:
            falhas.append(f"{tag}: cor reservada fora do papel (tarja, risco, BÔNUS) em {c}")
        for im in d["imgs"]:
            if not im["ok"]:
                falhas.append(f"{tag}: imagem quebrada ({im['src']}).")
            if im["porClique"]:
                falhas.append(f"{tag}: imagem entrando por clique; imagem já está na tela quando o slide abre.")
        if d["vagas"]:
            avisos.append(f"{tag}: vaga de print ou de cena sem imagem. Peça o print ou a cena ao dono antes de apresentar.")
        for tb in d["tabelas"]:
            if tb["total"] is None or tb["soma"] != tb["soma"] or abs(tb["soma"] - tb["total"]) > 0.005:
                falhas.append(f"{tag}: a soma da tabela ({tb['soma']}) não bate com o total ({tb['total']}).")
            else:
                mostrado = DINHEIRO.search(tb["mostrado"])
                if not mostrado or abs(valor(mostrado.group(1)) - tb["total"]) > 0.005:
                    falhas.append(f"{tag}: o total escrito na tela ({tb['mostrado']}) não bate com a soma ({tb['soma']}).")
        palavras = len(re.findall(r"\w+", tela))
        if d["layout"] not in ("oferta", "bonus", "escada") and palavras > a.max_palavras:
            falhas.append(f"{tag}: {palavras} palavras na tela; o teto é {a.max_palavras}. Encurte a tela e leve o resto pra nota, ou divida.")
        blocos = {}
        for x in lidos:
            blocos.setdefault(x["bloco"], []).append(x["txt"])
        for b in blocos.values():
            pb = len(re.findall(r"\w+", " ".join(b)))
            if pb > a.max_bloco and d["layout"] not in ("oferta",):
                falhas.append(f"{tag}: bloco com {pb} palavras (teto {a.max_bloco}): \"{' '.join(b)[:50]}\"")

    menor = min(((x["size"], d["num"], x["txt"]) for d in dados for x in d["texts"]), default=None)
    if menor:
        print(f"menor fonte: {menor[0]:g}px (slide {menor[1]}: \"{menor[2][:40]}\"); piso {a.min_fonte:g}px")
    for x in avisos:
        print("AVISO", x)
    for x in falhas:
        print("REPROVOU", x)
    print(f"checar_deck: {len(dados)} slides, {len(falhas)} reprovações, {len(avisos)} avisos -> {'REPROVADO' if falhas else 'APROVADO'}")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
