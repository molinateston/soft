#!/usr/bin/env python3
"""ler_roteiro.py: lê o roteiro da aula (slide a slide) ou só os tópicos e
devolve a lista de slides com tela, falta, notas e transição. É a base do
rascunho do deck.json e do brief do Claude Design.

Uso:
  python3 scripts/ler_roteiro.py roteiro.md --resumo
      uma linha por slide (fase, título, linhas de tela, cliques da fala, faltas)
  python3 scripts/ler_roteiro.py roteiro.md --esqueleto trabalho/slides
      o ponto de partida do modo agente: um arquivo por slide (01.html ...) com
      o <section> vazio, o fundo por bloco, o CONTEÚDO e a FALTA do roteiro num
      comentário (some no deck) e a nota já escrita com a fala do roteiro.
      Slide que o roteiro tira vai pro _operador.md como pergunta.
      Rodar de novo REGRAVA os NN.html e o _operador.md; por isso o script recusa quando
      algum NN.html já foi desenhado (tem <style> ou HTML além do esqueleto), a não ser com
      --forcar (que apaga o desenho).
  python3 scripts/ler_roteiro.py roteiro.md --rascunho trabalho/deck.json
      rascunho de texto (fora do fluxo padrão): o deck.json dos layouts de molde.

Formatos aceitos (os dois que a aula slide a slide costuma ter):
  ### Slide 07 · Título            ### Slide 07 · Título
  **Objetivo:** ...                - Objetivo: ...
  **CONTEÚDO:**                    - Conteúdo:
  - linha da tela                    - linha da tela
  **NOTAS**                        - FALTA: ...
  FALA                             - NOTAS:
    Abre com: ...                    - FALA: ...
    Clique 1: ...                    - TRANSIÇÃO: ...
    Fecha com: ...
  TRANSIÇÃO: ...
Linhas que o parser ignora: "FALTA: nenhuma." (não é falta), comentário HTML de uma linha,
como "<!-- Origem: slide 3 do original, dividido em 4 -->" (a origem da divisão, que vai
só pro comentário do esqueleto). "## Fase X · Nome" define o bloco (fundo), nome como escrito.
Sem nenhum "###", cada item de lista (ou cada título "##") vira um slide: é o
caso de quem mandou só os tópicos.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROTULO = re.compile(
    r"^(?:[-*]\s+)?(?:\*\*)?\s*(objetivo|conte[úu]do|tela|falta|notas|fala|transi[çc][ãa]o|abre com|fecha com|"
    r"clique\s*\d+|hora(?:-meta)?|pode pular|mostrar)\b\s*(\([^)]*\))?\s*:?\s*(?:\*\*)?\s*:?\s*(.*)$", re.I)
LACUNA = re.compile(r"`?\[(?:A CONFIRMAR|DO DONO|A DEFINIR|FALTA|PREENCHER)[^\]]*\]`?", re.I)
COLCHETE = re.compile(r"`?\[[^\]]*\]`?")
TITULO = re.compile(r"^(?:slide\s+)?([\w&]+(?:\s*\d+)?)\s*[·:\-.]\s*(.+)$", re.I)
PALAVRA = re.compile(r"\w+")
SEM_FALTA = re.compile(r"^(?:nenhuma|nada|sem falta|n[ãa]o h[áa])\.?$", re.I)
ORIGEM = re.compile(r"^<!--\s*origem\s*:\s*(.*?)\s*-->$", re.I)


def limpa(s):
    s = re.sub(r"\*\*|__", "", s or "").strip()
    return s.strip("`").strip()


def nome_fase(h):
    h = limpa(h)
    h = re.sub(r"^fase\s+(?:\d+|[a-z&])\b\s*[·:\-]\s*", "", h, flags=re.I)  # só a letra (ou número) sai; o nome fica inteiro, com "·" dentro
    h = re.sub(r"^fase\s+", "", h, flags=re.I)
    if re.match(r"^(q\s*&\s*a|perguntas)", h, re.I):
        return "Perguntas e respostas"
    h = re.sub(r"\s*\(.*\)$", "", h).strip()
    return h


def novo(num, titulo, fase):
    return {"num": num, "titulo": titulo, "fase": fase, "objetivo": "", "tela": [], "tabela": [],
            "falta": [], "sai": False, "nota_objetivo": "", "abre": "", "cliques": [], "fecha": "",
            "fala": [], "notas_livres": [], "transicao": "", "hora": "", "pode_pular": False, "mostrar": [], "marcados": 0,
            "origem": ""}


def tirar_lacunas(txt, sl):
    """Separa a lacuna do texto de tela. A lacuna vira falta; o resto volta."""
    for m in LACUNA.findall(txt):
        miolo = re.sub(r"^(A CONFIRMAR|DO DONO|A DEFINIR|FALTA|PREENCHER)\s*:?\s*", "", limpa(m).strip("[]"), flags=re.I)
        if miolo:
            sl["falta"].append(miolo)
    resto = LACUNA.sub("", txt).strip()
    return re.sub(r"\s{2,}", " ", resto)


CLIQUE = re.compile(r"^`?\[clique\]\s*([^`]*)`\s*(.*)$", re.I)
FONTE = re.compile(r"\s*\((P\d+|fonte[^)]*)\)", re.I)


def linha_tela(txt, sl):
    m = CLIQUE.match(txt.strip())
    if m:  # `[clique] RÓTULO` texto: o roteiro marcou a revelação por clique
        sl["marcados"] += 1
        rot = re.sub(r"^\d+\s*·\s*", "", m.group(1)).strip(" ·.:")
        rot = rot.capitalize() if rot.isupper() else rot
        txt = f"{rot}: {m.group(2)}" if rot else m.group(2)
    for f in FONTE.findall(txt):  # marca de fonte da pesquisa é bastidor: vai pra nota
        sl["notas_livres"].append(f"Fonte do dado na tela: {f}")
    txt = limpa(FONTE.sub("", txt))
    if not txt:
        return
    if LACUNA.fullmatch(txt):
        tirar_lacunas(txt, sl)
        return
    if re.match(r"^\[.*\]\.?$", txt):  # instrução entre colchetes, nunca tela
        if re.search(r"\bsai\b|sem o print|sem a cena|n[ãa]o entra", txt, re.I):
            sl["sai"] = True
        sl["notas_livres"].append(txt.strip("[]"))
        return
    if re.match(r"^falta\b", txt, re.I):
        resto = re.sub(r"^falta\s*:?\s*", "", txt, flags=re.I)
        if not SEM_FALTA.match(resto.strip()):
            sl["falta"].append(resto)
        return
    txt = tirar_lacunas(txt, sl)
    if txt:
        sl["tela"].append(txt)


def ler(caminho):
    linhas = Path(caminho).read_text(encoding="utf-8").splitlines()
    titulo_aula = ""
    for ln in linhas:
        if ln.startswith("# "):
            titulo_aula = limpa(ln[2:])
            break
    if not any(ln.startswith("### ") for ln in linhas):
        return {"titulo": titulo_aula, "slides": ler_topicos(linhas), "topicos": True}
    slides, sl, fase, secao = [], None, "", None
    for bruta in linhas:
        ln = bruta.rstrip()
        if ln.startswith("## ") and not ln.startswith("### "):
            fase, sl, secao = nome_fase(ln[3:]), None, None
            continue
        if ln.startswith("### "):
            cab = limpa(ln[4:])
            m = TITULO.match(cab)
            num, tit = (m.group(1), m.group(2)) if m else (str(len(slides) + 1), cab)
            if re.match(r"^q\s*&\s*a", cab, re.I):
                num = "Q" + re.sub(r"\D", "", num or "") if re.sub(r"\D", "", num or "") else num
            sl = novo(num.replace("Q&A", "Q").strip(), "", fase)
            sl["titulo"] = tirar_lacunas(tit, sl)
            slides.append(sl)
            secao = None
            continue
        if ln.strip() == "---":
            sl, secao = None, None
            continue
        if sl is None or not ln.strip():
            continue
        txt = ln.strip()
        mo = ORIGEM.match(txt)
        if mo:  # <!-- Origem: slide N do original, dividido em K -->: bastidor, nunca nota nem tela
            sl["origem"] = mo.group(1)
            continue
        if txt.startswith("<!--") and txt.endswith("-->"):  # outro comentário HTML: ignora
            continue
        m = ROTULO.match(txt)
        if m and not (secao == "conteudo" and txt.startswith(("- ", "* ")) and m.group(1).lower() in ("tela", "mostrar")):
            rot, resto = m.group(1).lower(), limpa(m.group(3))
            if rot == "objetivo":
                if secao in ("notas", "fala"):
                    sl["nota_objetivo"] = resto
                else:
                    sl["objetivo"] = resto
            elif rot.startswith("conte") or rot == "tela":
                secao = "conteudo"
                if resto:
                    linha_tela(resto, sl)
            elif rot == "falta":
                if resto and not SEM_FALTA.match(resto):
                    antes = len(sl["falta"])
                    texto = tirar_lacunas(resto, sl)
                    if len(sl["falta"]) == antes:  # sem [A CONFIRMAR]: a própria linha é a falta
                        sl["falta"].append(texto or resto)
                    # com [A CONFIRMAR]: ele já é a pergunta; o texto em volta não vira uma segunda falta
                if not txt.startswith(("- ", "* ")):
                    secao = None if secao == "conteudo" else secao
            elif rot == "notas":
                secao = "notas"
                if resto:
                    sl["notas_livres"].append(resto)
            elif rot == "fala":
                secao = "fala"
                if resto:
                    sl["fala"].append(resto)
            elif rot.startswith("transi"):
                sl["transicao"] = resto
            elif rot == "abre com":
                sl["abre"] = resto
                secao = "fala"
            elif rot == "fecha com":
                sl["fecha"] = resto
            elif rot.startswith("clique"):
                sl["cliques"].append(resto)
            elif rot.startswith("hora"):
                sl["hora"] = resto
            elif rot == "pode pular":
                sl["pode_pular"] = not re.match(r"^n[ãa]o", resto, re.I)
            elif rot == "mostrar":
                sl["mostrar"].append(resto)
            continue
        if secao == "conteudo":
            if txt.startswith("|"):
                cel = [limpa(c) for c in txt.strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cel if c):
                    sl["tabela"].append(cel)
            else:
                linha_tela(re.sub(r"^(?:[-*]|\d+[.)])\s+", "", txt), sl)
        else:  # fala ou nota livre; a lacuna vira falta (pergunta ao dono), nunca nota solta
            resto = tirar_lacunas(limpa(re.sub(r"^[-*]\s+", "", txt)), sl)
            if resto:
                sl["fala" if secao == "fala" else "notas_livres"].append(resto)
    bastidor = re.compile(r"[;:,.]?\s*\(?(ver|veja|pergunta ao dono (em|no)|vai pro)\s*`?_notas-operador\.md`?\)?\.?", re.I)
    for s in slides:  # a lacuna fala com o dono; o nome do arquivo de bastidor sai dela
        s["falta"] = list(dict.fromkeys(bastidor.sub("", x).strip() for x in s["falta"] if x))
    return {"titulo": titulo_aula, "slides": slides}


def ler_topicos(linhas):
    """Só tópicos: cada item de lista (ou cada título sem itens) vira um slide."""
    slides, fase, pendente = [], "", None
    for ln in linhas:
        t = ln.strip()
        if not t or t.startswith("# "):
            continue
        if re.match(r"^#{2,}\s", t):
            if pendente:
                slides.append(pendente)
            nome = limpa(t.lstrip("#"))
            fase, pendente = nome_fase(nome), None
            sl = novo(str(len(slides) + 1), nome, fase)
            linha_tela(nome, sl)
            pendente = sl
            continue
        m = re.match(r"^(?:[-*]|\d+[.)])\s+(.*)$", t)
        if m and not ln.startswith(("  ", "\t")):
            pendente = None
            sl = novo(str(len(slides) + 1), LACUNA.sub("", limpa(m.group(1))).strip()[:60], fase)
            linha_tela(m.group(1), sl)
            slides.append(sl)
        elif slides and not pendente:
            linha_tela(re.sub(r"^(?:[-*]|\d+[.)])\s+", "", t), slides[-1])
    if pendente:
        slides.append(pendente)
    for i, s in enumerate(slides, 1):
        s["num"] = str(i)
    return slides


# ---------------------------------------------------------------- rascunho

PRECO = re.compile(r"R\$\s?\d|\d+\s*x\s*(de\s*)?R\$|parcela|à vista|a vista", re.I)


def rascunho(dados):
    deck = {"titulo": dados["titulo"] or "Aula", "perguntas": [], "bastidor": [
        "Deck de partida gerado pelo ler_roteiro.py: notas do roteiro, tela com as frases do roteiro. "
        "Cada slide com 'revisar' pede decisão do operador antes do gerar.py."], "slides": []}
    for s in dados["slides"]:
        rot = f"Slide {s['num']} do roteiro ({s['titulo'][:50]})"
        if s["sai"] or (not s["tela"] and not s["tabela"] and s["falta"]):
            motivo = "; ".join(s["falta"][:2]) or "o roteiro tira este slide"
            deck["perguntas"].append(f"{rot} ficou fora do deck: {motivo[:300]}")
            continue
        tela, revisar = list(s["tela"]), []
        n_fala = len(s["cliques"])
        if s["tabela"]:
            revisar.append("tabela no roteiro: monte o layout oferta só com os valores do insumo; sem valor de algum item, use o layout preco")
        if not tela:
            revisar.append("o roteiro não traz tela: escreva a frase a partir do roteiro, sem acrescentar ideia")
            tela = [s["titulo"]]
        if len(tela) > 7:
            revisar.append(f"{len(tela)} linhas de tela: divida em dois slides (máximo de 7 cliques)")
            tela = tela[:7]
        palavras = sum(len(PALAVRA.findall(x)) for x in tela)
        longas = [x for x in tela if len(PALAVRA.findall(x)) > 20]
        if palavras > 40 or longas:
            revisar.append(f"tela longa ({palavras} palavras): deixe a versão curta que diz o mesmo; a frase inteira já está na fala")
        if any(PRECO.search(x) for x in tela):
            revisar.append("preço na tela: use o layout preco (valor cheio e parcela) ou oferta (tabela que soma)")
        if any(re.search(r"print|depoimento|foto|imagem", x, re.I) for x in s["falta"]):
            revisar.append("o roteiro pede print: layout print com a legenda; sem o print, a vaga fica e o pedido vai pro dono")
        if len(tela) == 1:
            slide = {"layout": "frase", "frase": tela[0]}
            cliques_tela = 0
        elif n_fala == len(tela) - 1 or len(tela) == 2:
            slide = {"layout": "frase", "frase": tela[0], "depois": tela[1:]}
            cliques_tela = len(tela) - 1
        else:
            slide = {"layout": "lista", "itens": tela}
            cliques_tela = len(tela)
        itens_clique = tela[-cliques_tela:] if cliques_tela else []
        cliques = list(s["cliques"][:cliques_tela])
        confirmar = list(s["falta"])
        if len(cliques) < cliques_tela:
            cliques += [f"(a tela) {x}" for x in itens_clique[len(cliques):]]
            confirmar.append("fala dos cliques que o roteiro não traz")
        elif len(s["cliques"]) > cliques_tela:
            revisar.append(f"a fala tem {len(s['cliques'])} cliques e a tela {cliques_tela}: ajuste a tela ou junte as falas")
        abre = s["abre"] or (s["fala"][0] if s["fala"] else "")
        if not abre:
            abre = tela[0]
            confirmar.append("fala de abertura")
        direcao = bool(re.match(r"^\s*\(.*\)\s*$", s["transicao"] or ""))  # direção de palco entre parênteses não é fala de saída
        fecha = s["fecha"] or ("" if direcao else s["transicao"]) or (s["fala"][-1] if len(s["fala"]) > 1 else "")
        if not fecha:
            fecha = "(o roteiro não traz a fala de saída)"
            confirmar.append("fala de saída")
        notas = {"objetivo": s["nota_objetivo"] or s["objetivo"] or s["titulo"], "abre": abre,
                 "cliques": cliques, "fecha": fecha}
        if s["transicao"] and s["transicao"] != fecha:
            notas["transicao"] = s["transicao"]
        meio = s["fala"][1:-1] if (not s["abre"] and len(s["fala"]) > 2) else ([] if not s["abre"] else s["fala"])
        if meio:
            notas["fala"] = " ".join(meio)
        if s["notas_livres"]:
            notas["obs"] = s["notas_livres"]
        if s["hora"]:
            notas["hora"] = s["hora"]
        if s["pode_pular"]:
            notas["pode_pular"] = True
        if confirmar:
            notas["confirmar"] = [x[:300] for x in dict.fromkeys(confirmar)]
        slide = {"nome": f"{s['titulo'][:56]} (roteiro {s['num']})", "bloco": s["fase"] or "Aula", **slide, "notas": notas}
        if revisar:
            slide["revisar"] = revisar
        deck["slides"].append(slide)
    return deck


def slide_desenhado(p):
    """True se o HTML tem desenho: algo além do section vazio, do comentário e da nota do esqueleto."""
    t = p.read_text(encoding="utf-8", errors="replace")
    if any(x.strip() for x in re.findall(r"<style\b[^>]*>(.*?)</style>", t, re.S | re.I)):
        return True
    t = re.sub(r"<!--.*?-->|<style\b.*?</style>|<aside\b.*?</aside>|</?section\b[^>]*>", "", t, flags=re.S | re.I)
    return bool(t.strip())


def esqueleto(dados, pasta, fundo="escuro", forcar=False):
    """Um HTML por slide que fica: o section vazio, o roteiro num comentário e a nota pronta."""
    import html as H
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from montar_deck import texto_nota
    deck = rascunho(dados)
    orig = {s["num"]: s for s in dados["slides"]}
    pasta.mkdir(parents=True, exist_ok=True)
    feitos = sorted(p.name for p in pasta.glob("[0-9]*.html") if slide_desenhado(p))
    if feitos and not forcar:
        sys.exit(f"RECUSADO: {len(feitos)} slide(s) já desenhado(s) em {pasta} ({', '.join(feitos)}). "
                 "O esqueleto apaga e regrava os NN.html e o _operador.md. Para refazer o esqueleto mesmo assim "
                 "(o desenho se perde), rode de novo com --forcar; para só atualizar uma nota, edite o HTML do slide.")
    for velho in pasta.glob("[0-9]*.html"):
        velho.unlink()
    limpo = lambda x: re.sub(r"-{2,}", "-", str(x))
    ant = None
    mapa, no_deck = [], set()
    orig_de = lambda o: (re.search(r"slide\s+(\S+?),?\s+do original", o["origem"], re.I) or [None, ""])[1]
    for i, sl in enumerate(deck["slides"], 1):
        num = re.search(r"\(roteiro (\w+)\)$", sl["nome"]).group(1)
        o = orig[num]
        no_deck.add(num)
        mapa.append(f"- deck {i:02d} = roteiro {num}" + (f" = original {orig_de(o)}" if orig_de(o) else "") + f": {o['titulo'][:50]}")
        if ant is not None and sl["bloco"] != ant:
            fundo = "claro" if fundo == "escuro" else "escuro"
        ant = sl["bloco"]
        nt = dict(sl["notas"])
        nt["cliques"] = list(o["cliques"])
        extra = [x for x in nt.get("confirmar", []) if x in ("fala de abertura", "fala de saída")]
        nt["confirmar"] = list(dict.fromkeys(o["falta"] + extra))
        if not nt["confirmar"]:
            nt.pop("confirmar")
        conteudo = o["tela"] + [" | ".join(c for c in row if c) for row in o["tabela"]]
        com = [f"DESENHE AQUI o slide {num} do roteiro: {o['titulo']}",
               f"OBJETIVO: {o['objetivo'] or o['nota_objetivo'] or o['titulo']}",
               "CONTEÚDO do roteiro (a tela sai daqui, na versão curta, sem nada a mais):"] + [f"- {x}" for x in conteudo]
        if o["origem"]:
            com.insert(1, f"ORIGEM (bastidor, não vai pra nota): {o['origem']}")
        if o["falta"]:
            com += ["FALTA (fora da tela; a nota já leva como [A CONFIRMAR]):"] + [f"- {x}" for x in o["falta"]]
        com += [f"Cliques: a fala do roteiro tem {len(o['cliques'])}. Um data-click por bloco que entra; o número de linhas 'Clique N' da nota tem que bater."]
        nome = H.escape(f"{o['titulo'][:56]} (roteiro {num})", quote=True)
        corpo = (f'<section class="slide {fundo}" data-nome="{nome}" data-bloco="{H.escape(sl["bloco"], quote=True)}">\n'
                 f'<style>\n</style>\n<!--\n{limpo(chr(10).join(com))}\n-->\n'
                 f'<aside class="notes">{H.escape(texto_nota(nt, len(nt["cliques"])), quote=False)}</aside>\n</section>\n')
        (pasta / f"{i:02d}.html").write_text(corpo, encoding="utf-8")
    for o in dados["slides"]:
        if o["num"] not in no_deck:
            mapa.append(f"- fora do deck: roteiro {o['num']}" + (f" = original {orig_de(o)}" if orig_de(o) else "") + f": {o['titulo'][:50]}")
    op = ["# Operador", "", "## Numeração (o número do deck é a referência de comando e de relato)", "",
          "Cite sempre \"deck NN (roteiro MM)\": NN é o arquivo NN.html (usado por --so, pelos PNGs e pelo checar_deck); MM é o do roteiro.md dividido.", ""]
    op += mapa + ["", "## Perguntas ao dono (slides que ficaram fora do deck)", ""]
    op += [f"- {x}" for x in deck["perguntas"]] or ["- Nenhum slide ficou fora."]
    op += ["", "## Decisões de desenho (preencha: fundo por bloco, exceções de tela, aviso do lint na fala do dono)", "",
           "## Metáforas e esquemas (preencha: cada desenho com o slide e a ideia da fala que ele ilustra, em palavras suas; o que volta em 2 slides é esquema)", ""]
    (pasta / "_operador.md").write_text("\n".join(op) + "\n", encoding="utf-8")
    return len(deck["slides"]), len(deck["perguntas"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro")
    ap.add_argument("--resumo", action="store_true")
    ap.add_argument("--rascunho")
    ap.add_argument("--json", help="grava a leitura completa em JSON")
    ap.add_argument("--esqueleto", help="pasta dos slides do modo agente (um HTML por slide)")
    ap.add_argument("--fundo", default="escuro", help="fundo do primeiro bloco no esqueleto")
    ap.add_argument("--forcar", action="store_true", help="esqueleto: regrava mesmo com slide já desenhado (o desenho se perde)")
    a = ap.parse_args()
    dados = ler(a.roteiro)
    if a.json:
        Path(a.json).write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    if a.esqueleto:
        n, fora = esqueleto(dados, Path(a.esqueleto), a.fundo, a.forcar)
        print(f"esqueleto: {n} slides em {a.esqueleto} (cada um com o roteiro num comentário e a nota pronta); {fora} fora do deck, no _operador.md")
    if a.resumo or not (a.rascunho or a.json or a.esqueleto):
        for s in dados["slides"]:
            print(f"[{s['num']}] {s['fase'][:40]} | {s['titulo'][:50]} | tela {len(s['tela'])}"
                  f"{' tabela ' + str(len(s['tabela'])) if s['tabela'] else ''} | cliques {len(s['cliques'])}"
                  f" | falta {len(s['falta'])}{' | SAI' if s['sai'] else ''}")
        print(f"{len(dados['slides'])} slides lidos de {a.roteiro}")
    if a.rascunho:
        deck = rascunho(dados)
        Path(a.rascunho).parent.mkdir(parents=True, exist_ok=True)
        Path(a.rascunho).write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding="utf-8")
        rev = sum(1 for s in deck["slides"] if s.get("revisar"))
        print(f"rascunho: {len(deck['slides'])} slides ({rev} com 'revisar'), "
              f"{len(deck['perguntas'])} fora do deck -> {a.rascunho}")
    if not dados["slides"]:
        sys.exit("Nenhum slide lido: o roteiro precisa de '### Slide N · título' ou de uma lista de tópicos.")


if __name__ == "__main__":
    main()
