#!/usr/bin/env python3
"""montar_deck.py: o RASCUNHO DE TEXTO (fora do fluxo padrão). Transforma o deck.json
(a tela de cada slide e as notas) no deck.html 1920x1080 pelos 13 layouts de molde
(assets/molde.css dentro do assets/palco.html), com revelação por clique e o notas.md.
O fluxo padrão é o agente desenhando cada slide (montar_desenho.py).

Uso:
  python3 scripts/montar_deck.py deck.json --saida <pasta> [--perfil perfil.json]

O perfil do dono sobrescreve assets/perfil-padrao.json só no que ele tiver.
O esquema de cada layout está em references/receitas-e-layouts.md.

Barreira de entrada: texto que vai pra TELA com lacuna ([A CONFIRMAR], [DO DONO],
[A DEFINIR], [FALTA) é barrado. Lacuna mora só nas notas. Sem o dado, o bloco
sai do deck e vira pergunta no _notas-operador.md.
Sai com código 1 e a lista do que barrou.
"""
import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
MAX_CLIQUES = 7
LACUNA = re.compile(r"\[(A CONFIRMAR|DO DONO|A DEFINIR|FALTA|PREENCHER|TODO)", re.I)
erros, avisos = [], []
CTX = {"base": Path("."), "saida": Path(".")}


def imagem(caminho, onde):
    """Copia a imagem pra <saida>/img e devolve o src relativo ao deck.html."""
    src = Path(caminho)
    if not src.is_absolute():
        src = CTX["base"] / src
    if not src.exists():
        erros.append(f"{onde}: imagem não encontrada ({caminho}).")
        return html.escape(caminho)
    destino = CTX["saida"] / "img"
    destino.mkdir(parents=True, exist_ok=True)
    if src.resolve() != (destino / src.name).resolve():
        shutil.copy2(src, destino / src.name)
    return "img/" + html.escape(src.name)


def mix(c1, c2, t):
    a = [int(c1.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(c2.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x * (1 - t) + y * t):02X}" for x, y in zip(a, b))


def carregar_perfil(caminho):
    base = json.loads((AQUI / "assets" / "perfil-padrao.json").read_text(encoding="utf-8"))
    if caminho:
        dono = json.loads(Path(caminho).read_text(encoding="utf-8"))
        cores = {**base["cores"], **dono.get("cores", {})}
        base.update({k: v for k, v in dono.items() if k != "cores" and v not in (None, "")})
        base["cores"] = cores
    return base


def css_vars(p):
    c = p["cores"]
    v = {k.replace("_", "-"): val for k, val in c.items()}
    v["suave-claro"] = mix(c["fundo_claro"], c["tinta_clara"], .06)
    v["suave-escuro"] = mix(c["fundo_escuro"], c["tinta_escura"], .07)
    v["dest-suave-claro"] = mix(c["fundo_claro"], c["destaque_claro"], .12)
    v["dest-suave-escuro"] = mix(c["fundo_escuro"], c["destaque_escuro"], .16)
    linhas = [f"  --{k}: {val};" for k, val in v.items()]
    linhas.append(f"  --fonte: {p['fonte']};")
    linhas.append(f"  --fonte-acao: {p['fonte_acao']};")
    return "\n".join(linhas)


def moeda(valor):
    """1997 -> R$1.997 ; 1234.5 -> R$1.234,50"""
    if isinstance(valor, str):
        return valor
    inteiro = int(round(valor * 100)) // 100
    cent = int(round(valor * 100)) % 100
    txt = f"{inteiro:,}".replace(",", ".")
    return f"R${txt}" + (f",{cent:02d}" if cent else "")


def t(texto, onde):
    """Escapa o texto da tela, barra lacuna e converte *ênfase* na cor de destaque."""
    texto = "" if texto is None else str(texto)
    if LACUNA.search(texto):
        erros.append(f"{onde}: lacuna na tela ({texto[:60]}). Lacuna vai pra nota; o bloco sai e vira pergunta.")
    if "—" in texto or "–" in texto:
        erros.append(f"{onde}: travessão na tela ({texto[:60]}).")
    esc = html.escape(texto)
    return re.sub(r"\*([^*]+)\*", r'<span class="dest">\1</span>', esc)


class Clique:
    def __init__(self):
        self.n = 0

    def __call__(self, fx="subir", cls=""):
        self.n += 1
        return self.mesmo(fx, cls)

    def mesmo(self, fx="subir", cls=""):
        """Atributos do clique atual, pra várias peças que entram juntas."""
        classes = ("reveal " + cls).strip()
        return f'class="{classes}" data-click="{self.n}" data-fx="{fx}"'


def rotulo(s, onde):
    return f'<p class="rotulo">{t(s["rotulo"], onde)}</p>' if s.get("rotulo") else ""


def lay_capa(s, c, o, p):
    nome = s.get("apresentador", p.get("nome", ""))
    h = f'<div class="area"><div class="promessa fit" data-min="56">{t(s["promessa"], o)}</div>'
    if s.get("apoio"):
        h += f'<div class="apoio">{t(s["apoio"], o)}</div>'
    if nome:
        h += f'<div class="nome">{t(nome, o)}</div>'
    return h + "</div>"


def lay_frase(s, c, o, p):
    h = f'{rotulo(s, o)}<div class="area"><div class="principal fit" data-min="48">{t(s["frase"], o)}</div>'
    for d in s.get("depois", []):
        h += f'<div {c()}><div class="depois">{t(d, o)}</div></div>'
    if s.get("pilula"):
        h += f'<div {c("aparecer")} style="align-self:flex-start"><div class="pilula">{t(s["pilula"], o)}</div></div>'
    return h + "</div>"


def lay_lista(s, c, o, p):
    h = f'{rotulo(s, o)}<div class="area">'
    if s.get("frase"):
        h += f'<div class="principal" style="font-size:60px;font-weight:800;line-height:1.1;margin-bottom:40px">{t(s["frase"], o)}</div>'
    h += "<ul>" + "".join(f'<li {c()}>{t(i, o)}</li>' for i in s["itens"]) + "</ul>"
    if s.get("conclusao"):
        h += f'<div {c()}><div class="conclusao">{t(s["conclusao"], o)}</div></div>'
    return h + "</div>"


def lay_cronograma(s, c, o, p):
    maior = max((len(str(ln.get("hora", ""))) for ln in s["linhas"]), default=0)
    larg = f' style="--hora-w:{max(4.5, round(0.62 * maior, 1))}em"' if maior else ""  # a coluna da hora com a mesma largura em toda linha
    h = f'{rotulo(s, o)}<div class="area"><div class="linhas"{larg}>'
    for ln in s["linhas"]:
        cls = "txt oferta-linha" if ln.get("oferta") else "txt"
        hora = f'<div class="hora">{t(ln["hora"], o)}</div>' if ln.get("hora") else ""
        h += f'<div {c()}><div class="linha">{hora}<div class="{cls}">{t(ln["texto"], o)}</div></div></div>'
    return h + "</div></div>"


def lay_escada(s, c, o, p):
    degraus = s["degraus"]
    if len(degraus) > 7:
        erros.append(f"{o}: escada com {len(degraus)} degraus; o máximo é 7, divida em dois slides.")
    atual = s.get("atual")
    revelar = s.get("revelar", True)
    perg_clique = s.get("pergunta_clique", False)
    h = rotulo(s, o) + '<div class="area">'
    perg = ""
    if s.get("pergunta"):
        perg = f'<div class="pergunta">{t(s["pergunta"], o)}</div>'
    pos = len(h)  # a pergunta fica no alto; quando entra por clique, o clique vem depois dos degraus
    so_nome = "" if any(d.get("promessa") for d in degraus) else " so-nome"  # sem promessa: degrau maior
    h += f'<div class="degraus{so_nome}">'
    for i, d in enumerate(degraus):
        cls = "degrau atual" if atual == i + 1 else "degrau"
        aqui = f'<span class="aqui">{t(s.get("aqui", "você está aqui"), o)}</span>' if atual == i + 1 else ""
        larg = "" if so_nome else f";width:{min(1500, 1680 - (len(degraus) - 1) * 70)}px"  # promessa longa: degrau mais largo
        inner = (f'<div class="{cls}" style="margin-left:{i * 70}px{larg}"><span class="n">{i + 1}</span>'
                 f'<div><div class="nm">{t(d["nome"], o)}</div>'
                 + (f'<div class="pr">{t(d["promessa"], o)}</div>' if d.get("promessa") else "")
                 + f'</div>{aqui}</div>')
        h += f'<div {c()}>{inner}</div>' if revelar else inner
    h += "</div>"
    if perg:
        h = h[:pos] + (f'<div {c()}>{perg}</div>' if perg_clique else perg) + h[pos:]
    return h + "</div>"


def lay_bussola(s, c, o, p):
    atual = s["atual"]
    h = f'{rotulo(s, o)}<div class="area"><div class="passos">'
    for i, ps in enumerate(s["passos"]):
        cls = "passo feito" if i + 1 < atual else ("passo atual" if i + 1 == atual else "passo")
        h += f'<div class="{cls}">{t(ps, o)}</div>'
    return h + "</div></div>"


def lay_numero(s, c, o, p):
    v = s["visual"]
    h = f'{rotulo(s, o)}<div class="area">'
    if s.get("frase"):
        h += f'<div class="principal">{t(s["frase"], o)}</div>'
    tipo = v["tipo"]
    if tipo == "calendario":
        total, marc = int(v["total"]), int(v["marcados"])
        cols = v.get("colunas", 6 if total <= 12 else 10)
        rots = v.get("rotulos") or [str(i + 1) for i in range(total)]
        alt = 110 if total <= 12 else 70
        h += f'<div class="cal" style="grid-template-columns:repeat({cols},1fr)">'
        marcar = v.get("marcar_no_clique", True)
        if marcar and marc:
            c.n += 1
        for i in range(total):
            x = ""
            if i < marc:
                x = (f'<div class="x reveal" data-sobrepoe="ok" data-click="{c.n}" data-fx="aparecer">X</div>' if marcar
                     else '<div class="x" data-sobrepoe="ok">X</div>')
            h += f'<div class="cel" style="height:{alt}px">{t(rots[i], o)}{x}</div>'
        h += "</div>"
    elif tipo == "por_dia":
        h += f'<div class="grande">{t(v["grande"], o)}</div><div class="unidade">{t(v["unidade"], o)}</div>'
        if v.get("conta"):
            h += f'<div {c()}><div class="conta">{t(v["conta"], o)}</div></div>'
    elif tipo == "comparacao":
        barras = v["barras"]
        mx = max(float(b["valor"]) for b in barras) or 1
        h += '<div class="barras">'
        for i, b in enumerate(barras):
            w = max(120, int(1240 * float(b["valor"]) / mx))  # a barra nunca fica menor que o próprio texto (CSS)
            forte = " forte" if b.get("forte") else ""
            h += (f'<div {c()}><div class="barra-linha"><div class="rot">{t(b["rotulo"], o)}</div>'
                  f'<div class="barra{forte}" style="width:{w}px">{t(b["texto"], o)}</div></div></div>')
        h += "</div>"
    else:
        erros.append(f"{o}: visual desconhecido {tipo}.")
    return h + "</div>"


def lay_print(s, c, o, p):
    h = f'{rotulo(s, o)}<div class="area"><div class="quadro">'
    img = s.get("imagem")
    if img:
        h += f'<img src="{imagem(img, o)}" alt="{html.escape(s["legenda"])}">'
    else:
        avisos.append(f"{o}: print ainda sem imagem (vaga na tela). Peça o print ao dono no _notas-operador.md.")
        h += '<div class="vaga" data-vaga="print"></div>'
    return h + f'</div><div class="legenda">{t(s["legenda"], o)}</div></div>'


def lay_duas(s, c, o, p):
    h = f'{rotulo(s, o)}<div class="area">'
    if s.get("frase"):
        h += f'<div class="principal">{t(s["frase"], o)}</div>'
    h += '<div class="cols">'
    for lado, cls in (("esquerda", "col a"), ("direita", "col b")):
        col = s[lado]
        itens = "".join(f"<p>{t(i, o)}</p>" for i in col.get("itens", []))
        h += f'<div {c()} style="flex:1;display:flex"><div class="{cls}"><h3>{t(col["titulo"], o)}</h3>{itens}</div></div>'
    h += "</div>"
    if s.get("fecho"):
        h += f'<div {c()}><div class="fecho">{t(s["fecho"], o)}</div></div>'
    return h + "</div>"


def risco(c):
    return f'<div {c("riscar")} style="position:absolute;inset:0"><div class="risco-wrap"><div class="risco-rot"><div class="risco-linha"></div></div></div></div>'


def lay_preco(s, c, o, p):
    h = f'{rotulo(s, o)}<div class="area">'
    if s.get("frase"):
        h += f'<div class="principal">{t(s["frase"], o)}</div>'
    h += f'<div class="linha-preco"><div class="antigo"><span class="v">{t(moeda(s["de"]), o)}</span>{risco(c)}'
    if s.get("percentual"):
        h += f'<div class="pct-wrap" data-sobrepoe="ok"><div {c("selo")}><span class="pct">{t(s["percentual"], o)}</span></div></div>'
    h += '</div><div class="seta">→</div>'
    h += (f'<div {c()}><div class="novo"><div class="parcela">{t(s["parcela"], o)}</div>'
          + (f'<div class="avista">{t(s["avista"], o)}</div>' if s.get("avista") else "")
          + "</div></div></div>")
    return h + "</div>"


GEOMETRIA = [(8, 84, 36), (11, 66, 32), (12, 60, 30), (14, 52, 28)]


def lay_oferta(s, c, o, p):
    linhas = s["linhas"]
    n = len(linhas)
    geo = next((g for g in GEOMETRIA if n <= g[0]), None)
    if not geo:
        erros.append(f"{o}: tabela com {n} linhas; o máximo é 14. Divida a pilha em duas telas.")
        geo = GEOMETRIA[-1]
    for i, ln in enumerate(linhas):
        if not isinstance(ln.get("valor"), (int, float)):
            erros.append(f"{o}: linha {i + 1} ({ln.get('item')}) sem valor numérico do insumo. Sem valor a soma não fecha: a tabela sai e vira pergunta.")
    soma = sum(ln["valor"] for ln in linhas if isinstance(ln.get("valor"), (int, float)))
    if s.get("total_declarado") is not None and abs(float(s["total_declarado"]) - soma) > 0.005:
        erros.append(f"{o}: a soma das linhas dá {moeda(soma)} e o total declarado é {moeda(s['total_declarado'])}.")
    if s.get("prazo") and not s["prazo"].get("motivo"):
        erros.append(f"{o}: prazo sem motivo. Prazo só entra com o motivo real do insumo.")
    animar = s.get("animar", True)
    novas = set(s.get("novas", [])) if animar else set()
    cc = (lambda fx="subir": c(fx)) if animar else (lambda fx="subir": "")
    painel = any(s.get(k) for k in ("parcela", "avista", "link"))  # sem preço: a tabela que cresce, sem risco
    h = (f'{rotulo(s, o)}<div class="corpo{"" if painel else " so-tabela"}"><div class="tabela" '
         f'style="--alt-linha:{geo[1]}px;--fs-linha:{geo[2]}px" data-geometria="{geo[0]}">')
    for i, ln in enumerate(linhas):
        bon = '<span class="rot-bonus">BÔNUS</span>' if ln.get("bonus") else ""
        inner = (f'<div class="tl">{bon}<span class="it fit" data-min="24">{t(ln["item"], o)}</span>'
                 f'<span class="vl" data-valor="{ln.get("valor", "")}">{t(moeda(ln.get("valor", "")), o)}</span></div>')
        h += f'<div {c()}>{inner}</div>' if (i + 1) in novas else inner
    riscado = (risco(cc) if animar else risco(lambda fx: 'class=""')) if painel else ""
    h += (f'<div {cc()}><div class="total"><span class="tt">{t(s.get("rotulo_total", "Total"), o)}</span>'
          f'<span class="tv" data-total="{soma}">{t(moeda(soma), o)}{riscado}</span>')
    if s.get("percentual"):
        h += f'<div {cc("selo")}><span class="pct">{t(s["percentual"], o)}</span></div>'
    h += "</div></div></div>"
    if not painel:
        return h + "</div>"
    h += f'<div {cc()} style="flex:1;display:flex"><div class="painel">'
    if s.get("chamada"):
        h += f'<div class="hoje">{t(s["chamada"], o)}</div>'
    if s.get("parcela"):
        h += f'<div class="parcela" data-parcela="1">{t(s["parcela"], o)}</div>'
    if s.get("avista"):
        h += f'<div class="avista">{t(s["avista"], o)}</div>'
    if s.get("link"):
        h += f'<div class="link">{t(s["link"], o)}</div>'
    if s.get("prazo"):
        h += f'<div class="prazo">{t(s["prazo"]["texto"], o)}. {t(s["prazo"]["motivo"], o)}</div>'
    h += "</div></div></div>"
    return h


def lay_bonus(s, c, o, p):
    h = ""
    if s.get("tarja"):
        h += f'<div class="tarja">{t(s["tarja"], o)}</div>'
    h += '<div class="topo"><div class="logo">'
    if s.get("logo"):
        h += f'<img src="{imagem(s["logo"], o)}" alt="{html.escape(s.get("nome", ""))}">'
    else:
        h += f'<span class="logo-txt">{t(s["nome"], o)}</span>'
    h += '</div></div><div class="corpo"><div class="esq">'
    h += f'<div class="dor">{t(s["dor"], o)}</div><div class="promessa fit" data-min="40">{t(s["promessa"], o)}</div>'
    if s.get("aprende"):
        h += f'<div class="aprende-rot">{t(s.get("rotulo_aprende", "O que você aprende"), o)}</div>'
        for a in s["aprende"]:
            h += f'<div {c()}><div class="aprende">{t(a, o)}</div></div>'
    h += '</div><div class="dir">'
    if s.get("valor") is not None:
        h += f'<div {c()} style="align-self:flex-start"><div class="vale"><span class="v">Vale {t(moeda(s["valor"]), o)}</span>{risco(c)}</div></div>'
        h += (f'<div {c()}><div class="zero">{t(s.get("zero", "R$0 pra você"), o)}</div>'
              f'<div class="oficial">{t(moeda(s["valor"]), o)} é o valor oficial do curso</div></div>')
    h += "</div></div>"
    return h


def lay_cta(s, c, o, p):
    h = f'{rotulo(s, o)}<div class="area"><div class="principal">{t(s["frase"], o)}</div>'
    h += f'<div {c("aparecer")}><div class="link">{t(s["link"], o)}</div></div>'
    if s.get("apoio"):
        h += f'<div {c()}><div class="apoio">{t(s["apoio"], o)}</div></div>'
    return h + "</div>"


LAYOUTS = {"capa": lay_capa, "frase": lay_frase, "lista": lay_lista, "cronograma": lay_cronograma,
           "escada": lay_escada, "bussola": lay_bussola, "numero": lay_numero, "print": lay_print,
           "duas_colunas": lay_duas, "preco": lay_preco, "oferta": lay_oferta, "bonus": lay_bonus, "cta": lay_cta}


def texto_nota(nt, cliques):
    linhas = []
    if nt.get("objetivo"):
        linhas.append(f"Objetivo: {nt['objetivo']}")
    if nt.get("abre"):
        linhas.append(f"Abre com: {nt['abre']}")
    for i, cl in enumerate(nt.get("cliques", []), 1):
        linhas.append(f"Clique {i}: {cl}")
    if nt.get("fala"):
        linhas.append(f"Fala: {nt['fala']}")
    if nt.get("fecha"):
        linhas.append(f"Fecha com: {nt['fecha']}")
    if nt.get("transicao"):
        linhas.append(f"Transição: {nt['transicao']}")
    if nt.get("hora"):
        linhas.append(f"Hora-meta: {nt['hora']}")
    if nt.get("pode_pular"):
        linhas.append("Pode pular: sim, se a aula atrasar.")
    if nt.get("publicos"):
        linhas.append("Por público:")
        for k, v in nt["publicos"].items():
            linhas.append(f"- {k}: {v}")
    for x in nt.get("confirmar", []):
        linhas.append(f"[A CONFIRMAR: {x}]")
    for x in nt.get("historico", []):
        linhas.append(x)
    for x in nt.get("obs", []):
        linhas.append(f"Obs.: {x}")
    return "\n".join(linhas)


def texto_tela(sec_html):
    sem = re.sub(r"<aside.*?</aside>", " ", sec_html, flags=re.S)
    sem = re.sub(r"<[^>]+>", " ", sem)
    return re.sub(r"\s+", " ", html.unescape(sem)).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--perfil")
    a = ap.parse_args()
    spec = json.loads(Path(a.deck).read_text(encoding="utf-8"))
    perfil = carregar_perfil(a.perfil or spec.get("perfil"))
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    CTX["base"], CTX["saida"] = Path(a.deck).resolve().parent, saida

    fundo = perfil.get("fundo_inicial", "escuro")
    bloco_ant = None
    secoes, notas_md = [], [f"# Notas do apresentador: {spec.get('titulo', 'aula')}", ""]
    for i, s in enumerate(spec["slides"], 1):
        o = f"slide {i:02d} ({s.get('nome', s.get('layout'))})"
        lay = s.get("layout")
        if lay not in LAYOUTS:
            erros.append(f"{o}: layout desconhecido '{lay}'. Use um de: {', '.join(LAYOUTS)}.")
            continue
        bloco = s.get("bloco", bloco_ant)
        if bloco_ant is not None and bloco != bloco_ant:
            fundo = "claro" if fundo == "escuro" else "escuro"
        bloco_ant = bloco
        c = Clique()
        try:
            corpo = LAYOUTS[lay](s, c, o, perfil)
        except KeyError as e:
            erros.append(f"{o}: falta o campo {e} do layout {lay}.")
            continue
        if c.n > MAX_CLIQUES:
            erros.append(f"{o}: {c.n} cliques; o máximo é {MAX_CLIQUES}. Divida em dois slides.")
        nt = s.get("notas", {})
        if len(nt.get("cliques", [])) != c.n:
            avisos.append(f"{o}: a tela tem {c.n} cliques e a nota descreve {len(nt.get('cliques', []))}.")
        nota = texto_nota(nt, c.n)
        if "—" in nota or "–" in nota:
            erros.append(f"{o}: travessão na nota.")
        marca = f'<div class="marca">{t(perfil["marca"], o)}</div>' if perfil.get("marca") and lay != "capa" else ""
        sec = (f'<section class="slide {lay.replace("duas_colunas", "duas")} {fundo}" data-layout="{lay}" '
               f'data-bloco="{html.escape(str(bloco or ""))}" data-cliques="{c.n}">\n{corpo}{marca}\n'
               f'<aside class="notes">{html.escape(nota)}</aside>\n</section>')
        secoes.append(sec)
        notas_md += [f"## Slide {i:02d} · {s.get('nome', lay)}", ""]
        if lay == "oferta":  # a tabela vai como tabela, pra soma ser conferida também no notas.md
            notas_md += ["Tela:", "", "| Item | Valor |", "|---|---|"]
            notas_md += [f"| {'BÔNUS ' if ln.get('bonus') else ''}{ln['item']} | {moeda(ln.get('valor', ''))} |" for ln in s["linhas"]]
            soma = sum(ln["valor"] for ln in s["linhas"] if isinstance(ln.get("valor"), (int, float)))
            notas_md += [f"| Total | {moeda(soma)} |", ""]
            resto = " · ".join(x for x in (s.get("parcela"), s.get("avista"), s.get("link")) if x)
            notas_md += [f"Painel: {resto}", ""] if resto else []
        else:
            notas_md += [f"Tela: {texto_tela(sec)}", ""]
        notas_md += [ln if not ln.startswith("- ") else ln for ln in nota.split("\n")] + [""]

    base = (AQUI / "assets" / "palco.html").read_text(encoding="utf-8")
    out = (base.replace("{{TITULO}}", html.escape(spec.get("titulo", "Aula")))
           .replace("/*{{VARS}}*/", css_vars(perfil))
           .replace("/*{{CSS}}*/", (AQUI / "assets" / "molde.css").read_text(encoding="utf-8"))
           .replace("<!--{{SLIDES}}-->", "\n".join(secoes)))
    (saida / "deck.html").write_text(out, encoding="utf-8")
    (saida / "notas.md").write_text("\n".join(notas_md).rstrip() + "\n", encoding="utf-8")
    (saida / ".perfil-usado.json").write_text(json.dumps(perfil, ensure_ascii=False, indent=2), encoding="utf-8")
    perguntas = []
    for i, sd in enumerate(spec["slides"], 1):
        for x in sd.get("notas", {}).get("confirmar", []):
            perguntas.append(f"- Slide {i:02d} ({sd.get('nome', sd.get('layout'))}): {x}")
    perguntas += [f"- {x}" for x in avisos]
    for x in spec.get("perguntas", []):
        perguntas.append(f"- {x}")
    neutro = "padrão neutro da skill (o dono não mandou perfil)" if not (a.perfil or spec.get("perfil")) else "perfil do dono"
    op = ["# Notas do operador (bastidor, fica fora do deck)", "",
          "## Perguntas ao dono", ""] + (perguntas or ["- Nenhuma pendência registrada."]) + ["",
          "## Bastidor", "",
          f"- Identidade usada: {neutro}.",
          f"- Slides: {len(secoes)}. Fundo inicial: {perfil.get('fundo_inicial', 'escuro')}, alternando a cada bloco.",
          ""] + [f"- {x}" for x in spec.get("bastidor", [])]
    (saida / "_notas-operador.md").write_text("\n".join(op).rstrip() + "\n", encoding="utf-8")
    for x in avisos:
        print("AVISO", x)
    for x in erros:
        print("BARRADO", x)
    print(f"{len(secoes)} slides -> {saida / 'deck.html'} e notas.md")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
