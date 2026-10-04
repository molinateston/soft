#!/usr/bin/env python3
"""montar_desenho.py: o fluxo padrão do modo agente. Junta os slides que o agente
DESENHOU (um arquivo HTML por slide) no deck.html com revelação por clique,
renderiza, confere e exporta.

  Laço de um slide (renderiza só ele, confere e grava o PNG pra você olhar):
    python3 scripts/montar_desenho.py <slides/> --saida <trabalho/ver> --so 7 [--estados]
  Fecho do deck inteiro:
    python3 scripts/montar_desenho.py <slides/> --saida <pasta> --insumo <roteiro.md ...> [--perfil perfil.json] [--min-fonte 30]
  Se existir escala-desenho.md na pasta dos slides ou na pasta acima, ele entra no insumo sozinho.

Cada arquivo de <slides/> (01.html, 02.html ... na ordem do deck) é UM slide:
  <section class="slide escuro" data-nome="nome curto" data-bloco="Abertura" [data-layout="oferta"]>
    <style> CSS só deste slide (o script prefixa cada regra com o id do slide; :scope é o próprio slide) </style>
    ... HTML e SVG 1920x1080; o que entra por clique leva data-click="N" (e data-fx) ...
    <aside class="notes">Objetivo: ...
  Abre com: ...
  Clique 1: ...
  Fecha com: ...</aside>
  </section>
Imagem com caminho relativo à pasta dos slides é copiada pra <saida>/img.
<slides>/_operador.md (opcional) entra no _notas-operador.md: perguntas ao dono e premissas.

Barra (código 1) antes de renderizar: lacuna ou {{marcador}} na tela, travessão,
slide sem nota, mais de 7 cliques. Depois roda checar_deck.py, mosaico (12 por
folha), conferir_fontes.py, lint_copy.py, PDF dos PNGs e PPTX, como o gerar.py.
"""
import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
from gerar import ferramenta, pdf_dos_pngs, rodar  # noqa: E402
from montar_deck import carregar_perfil, css_vars  # noqa: E402

LACUNA = re.compile(r"\[(A CONFIRMAR|DO DONO|A DEFINIR|FALTA|PREENCHER|TODO)|\{\{|\}\}", re.I)
erros, avisos = [], []
TERMOS = []  # nomes próprios do dono (trabalho/termos-do-dono.txt); mascarados só no texto enviado ao lint
MASCARA = "Marca"


def ler_termos(pasta):
    """termos-do-dono.txt na pasta dos slides ou na de cima: um termo por linha, '#' comenta."""
    for cand in (pasta / "termos-do-dono.txt", pasta.parent / "termos-do-dono.txt"):
        if cand.is_file():
            ts = [x.strip() for x in cand.read_text(encoding="utf-8").splitlines()]
            return cand, sorted({x for x in ts if len(x) >= 3 and not x.startswith("#")}, key=len, reverse=True)
    return None, []


USADOS = {}  # termo -> quantas vezes foi mascarado de fato (só os que apareceram)


def mascarar(texto):
    """Troca cada termo do dono por uma palavra neutra. Devolve (texto, quantas trocas)."""
    total = 0
    for t in TERMOS:
        texto, k = re.subn(re.escape(t), MASCARA, texto, flags=re.I)
        total += k
        if k:
            USADOS[t] = USADOS.get(t, 0) + k
    return texto, total


def barrados_pelo_lint(termos, py):
    """Dos termos que apareceram, os que o lint reprova sozinhos (cada um numa linha)."""
    barrados = []
    with tempfile.TemporaryDirectory(prefix="termo-") as tmp:
        for t in termos:
            f = Path(tmp) / "t.md"
            f.write_text(t + "\n", encoding="utf-8")
            r = subprocess.run([py, str(ferramenta("lint_copy.py")), str(f)], capture_output=True, text=True)
            if r.returncode != 0:
                barrados.append(t)
    return barrados


def partir_seletores(sel):
    out, d, cur = [], 0, ""
    for ch in sel:
        d += ch in "(["
        d -= ch in ")]"
        if ch == "," and d == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    return [x.strip() for x in out + [cur] if x.strip()]


def escopo(css, sid):
    """Prefixa cada regra com #sid; ':scope' e '&' viram o próprio slide."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        cab = css[i:j].strip()
        if ";" in cab:
            cab = cab.rsplit(";", 1)[1].strip()
        k, d = j + 1, 1
        while k < n and d:
            d += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        corpo = css[j + 1:k - 1]
        i = k
        if cab.startswith(("@media", "@supports", "@container")):
            out.append(f"{cab} {{\n{escopo(corpo, sid)}\n}}")
        elif cab.startswith("@"):
            out.append(f"{cab} {{{corpo}}}")
        else:
            sels = []
            for s in partir_seletores(cab):
                if s.startswith((":scope", "&")):
                    sels.append("#" + sid + s.split(":scope", 1)[-1] if s.startswith(":scope") else "#" + sid + s[1:])
                else:
                    sels.append(f"#{sid} {s}")
            out.append(f"{', '.join(sels)} {{{corpo}}}")
    return "\n".join(out)


def texto_tela(sec):
    sem = re.sub(r"<(aside|style|script)\b.*?</\1>", " ", sec, flags=re.S | re.I)
    sem = re.sub(r"<[^>]+>", " ", sem)
    return re.sub(r"\s+", " ", html.unescape(sem)).strip()


def num_arquivo(p):
    m = re.match(r"(\d+)", p.stem)
    return int(m.group(1)) if m else None


def montar(pasta, saida, perfil, so=None, titulo="Aula"):
    arqs = sorted([p for p in pasta.glob("*.html") if num_arquivo(p) is not None], key=lambda p: (num_arquivo(p), p.name))
    if not arqs:
        sys.exit(f"Nenhum slide em {pasta}: um arquivo por slide, 01.html, 02.html ...")
    if so:
        arqs = [p for p in arqs if num_arquivo(p) in so]
    saida.mkdir(parents=True, exist_ok=True)
    estilos, secoes, notas_md, perguntas = [], [], [f"# Notas do apresentador: {titulo}", ""], []
    fundo_bloco = {}
    for p in arqs:
        num = num_arquivo(p)
        sid, tag = f"s{num:02d}", f"slide {num:02d} ({p.name})"
        bruto = p.read_text(encoding="utf-8")
        m = re.search(r"<section\b[^>]*>.*</section>", bruto, re.S | re.I)
        if not m:
            erros.append(f"{tag}: falta o <section class=\"slide ...\"> ... </section>.")
            continue
        sec = re.sub(r"<!--.*?-->", "", m.group(0), flags=re.S)
        abre = re.match(r"<section\b[^>]*>", sec).group(0)
        classes = re.search(r'class="([^"]*)"', abre)
        cl = classes.group(1).split() if classes else []
        if "slide" not in cl:
            cl.insert(0, "slide")
        if not ({"claro", "escuro"} & set(cl)):
            erros.append(f"{tag}: diga o fundo na classe do section (claro ou escuro).")
        nome = (re.search(r'data-nome="([^"]*)"', abre) or [None, f"slide {num}"])[1]
        bloco = (re.search(r'data-bloco="([^"]*)"', abre) or [None, ""])[1]
        fundo = "claro" if "claro" in cl else "escuro"
        if bloco and fundo_bloco.setdefault(bloco, fundo) != fundo:
            avisos.append(f"{tag}: o bloco '{bloco}' já vinha com fundo {fundo_bloco[bloco]}; o fundo troca por bloco, nunca slide a slide.")
        resto = re.sub(r'\s(class|id|data-num)="[^"]*"', "", abre[len("<section"):-1])
        novo = f'<section id="{sid}" data-num="{num:02d}" class="{" ".join(cl)}"{resto}>'
        sec = novo + sec[len(abre):]
        for st in re.findall(r"<style\b[^>]*>(.*?)</style>", sec, re.S | re.I):
            estilos.append(f"/* {p.name} */\n" + escopo(st, sid))
        sec = re.sub(r"<style\b[^>]*>.*?</style>", "", sec, flags=re.S | re.I)

        def reveal(mt):  # todo data-click ganha a classe reveal e o efeito padrão subir
            el = mt.group(0)
            if 'data-fx="' not in el:
                el = el.replace("data-click=", 'data-fx="subir" data-click=', 1)
            if re.search(r'class="[^"]*\breveal\b', el):
                return el
            if 'class="' in el:
                return re.sub(r'class="', 'class="reveal ', el, count=1)
            return el.replace("data-click=", 'class="reveal" data-click=', 1)
        sec = re.sub(r"<[a-zA-Z][^>]*\bdata-click=\"\d+\"[^>]*>", reveal, sec)

        def img(mt):
            src = mt.group(2)
            if re.match(r"^(data:|https?:|img/)", src):
                return mt.group(0)
            orig = (pasta / src)
            if not orig.exists():
                erros.append(f"{tag}: imagem não encontrada ({src}).")
                return mt.group(0)
            (saida / "img").mkdir(exist_ok=True)
            shutil.copy2(orig, saida / "img" / orig.name)
            return f'{mt.group(1)}img/{orig.name}"'
        sec = re.sub(r'(<img\b[^>]*\bsrc=")([^"]+)"', img, sec)

        nota_m = re.search(r'<aside class="notes">(.*?)</aside>', sec, re.S)
        nota = html.unescape(nota_m.group(1)).strip() if nota_m else ""
        nota = "\n".join(x.strip() for x in nota.splitlines())
        tela = texto_tela(sec)
        if not nota:
            erros.append(f"{tag}: slide sem <aside class=\"notes\"> (Objetivo, Abre com, Clique N, Fecha com).")
        if LACUNA.search(tela):
            erros.append(f"{tag}: lacuna ou marcador na tela ({LACUNA.search(tela).group(0)}). Lacuna mora na nota; sem o dado, o bloco sai.")
        if "—" in tela or "–" in tela:
            erros.append(f"{tag}: travessão na tela.")
        if "—" in nota or "–" in nota:
            erros.append(f"{tag}: travessão na nota.")
        cliques = [int(x) for x in re.findall(r'data-click="(\d+)"', sec)]
        n = max(cliques, default=0)
        if n > 7:
            erros.append(f"{tag}: {n} cliques; o máximo é 7. Divida em dois slides.")
        if cliques and sorted(set(cliques)) != list(range(1, n + 1)):
            avisos.append(f"{tag}: os cliques pulam número ({sorted(set(cliques))}).")
        secoes.append(sec)
        notas_md += [f"## Slide {num:02d} · {nome}", "", f"Tela: {tela}", ""] + nota.splitlines() + [""]
        # a mesma pergunta pode aparecer em mais de um campo da nota (Fecha com e rodapé): uma vez só por slide
        perguntas += [f"- Slide {num:02d} ({nome}): {x}" for x in dict.fromkeys(
            y.strip() for y in re.findall(r"\[A CONFIRMAR:\s*([^\]]+)\]", nota))]
    base = (RAIZ / "assets" / "palco.html").read_text(encoding="utf-8")
    out = (base.replace("{{TITULO}}", html.escape(titulo)).replace("/*{{VARS}}*/", css_vars(perfil))
           .replace("/*{{CSS}}*/", "\n\n".join(estilos)).replace("<!--{{SLIDES}}-->", "\n".join(secoes)))
    (saida / "deck.html").write_text(out, encoding="utf-8")
    (saida / "notas.md").write_text("\n".join(notas_md).rstrip() + "\n", encoding="utf-8")
    (saida / ".perfil-usado.json").write_text(json.dumps(perfil, ensure_ascii=False, indent=2), encoding="utf-8")
    extra = (pasta / "_operador.md").read_text(encoding="utf-8").strip() if (pasta / "_operador.md").exists() else ""
    op = ["# Notas do operador (bastidor, fica fora do deck)", "", "## Perguntas tiradas das notas", ""]
    op += perguntas or ["- Nenhuma [A CONFIRMAR] nas notas."]
    op += ["", "## Bastidor", "", f"- Slides desenhados: {len(secoes)}.", f"- Identidade: {perfil.get('_origem', 'perfil do dono')}.",
           "- Numeração: \"Slide NN\" é o número do deck (o do arquivo NN.html); \"(roteiro NN)\" é o do roteiro.md dividido."]
    op += [f"- {x}" for x in avisos]
    if TERMOS:
        op += [f"- {len(TERMOS)} termo(s) do dono mascarado(s) só no texto enviado ao lint; o aviso do fechamento diz quais apareceram e quais o lint barra."]
    if extra:
        op += ["", re.sub(r"^# ", "## ", extra, flags=re.M)]
    (saida / "_notas-operador.md").write_text("\n".join(op).rstrip() + "\n", encoding="utf-8")
    return len(secoes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slides", help="pasta com um HTML por slide (01.html, 02.html ...)")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--perfil")
    ap.add_argument("--insumo", nargs="*", default=[])
    ap.add_argument("--titulo", default="Aula")
    ap.add_argument("--so", help="números dos slides pro laço (ex.: 7 ou 7,8): renderiza e confere só eles")
    ap.add_argument("--estados", action="store_true", help="no laço, grava também um PNG por clique")
    ap.add_argument("--max-palavras", default="40")
    ap.add_argument("--min-fonte", default="30", help="piso de fonte em px numa tela de 1920 (padrão 30)")
    a = ap.parse_args()
    pasta, out = Path(a.slides), Path(a.saida)
    cand_t, termos = ler_termos(pasta)
    if termos and not a.so:
        TERMOS.extend(termos)
        print(f"== MASCARAMENTO: {len(termos)} termo(s) em {cand_t}; no fim, o aviso diz quais apareceram, quantas vezes e quais o lint barra. O mascaramento vale SÓ no lint; o deck e as notas não mudam.")
    # escala-desenho.md (unidade do pictograma, regra do desenho e não dado do dono) entra sozinha no insumo
    if a.insumo:
        for cand in (pasta / "escala-desenho.md", pasta.parent / "escala-desenho.md"):
            if cand.is_file() and cand.resolve() not in [Path(x).resolve() for x in a.insumo]:
                a.insumo = list(a.insumo) + [str(cand)]
                print(f"== escala do desenho lida de {cand}: entra no insumo só como unidade do pictograma.")
                break
    perfil = carregar_perfil(a.perfil)
    perfil["_origem"] = "perfil do dono" if a.perfil else "padrão neutro da skill (o dono não mandou perfil)"
    so = {int(x) for x in a.so.split(",")} if a.so else None
    if so and out.resolve() == pasta.resolve():
        sys.exit("No laço, a saída precisa ser outra pasta (ex.: trabalho/ver).")
    if so:
        for velho in (out / "png").glob("slide-*.png"):
            velho.unlink()
    n = montar(pasta, out, perfil, so, a.titulo)
    for x in avisos:
        print("AVISO", x)
    for x in erros:
        print("BARRADO", x)
    if erros:
        sys.exit(f"BARRADO: corrija o HTML do slide e rode de novo ({len(erros)} item(ns)).")
    py = sys.executable
    if so:
        cmd = [py, str(AQUI / "checar_deck.py"), str(out), "--png", str(out / "png"), "--max-palavras", a.max_palavras,
               "--min-fonte", a.min_fonte]
        rc = rodar("checar (laço)", cmd + (["--estados"] if a.estados else []))
        print("\nOlhe agora (Read):", ", ".join(str(x) for x in sorted((out / "png").glob("slide-*.png"))))
        sys.exit(rc)
    conf = out / "_conferencia"
    ok_checar = rodar("2 checar", [py, str(AQUI / "checar_deck.py"), str(out), "--png", str(conf / "png"),
                                   "--max-palavras", a.max_palavras, "--min-fonte", a.min_fonte]) == 0
    for velho in out.glob("mosaico*.png"):
        velho.unlink()
    rodar("3 mosaico", [py, str(AQUI / "make_mosaic.py"), str(conf / "png"), str(out / "mosaico.png"),
                        "--por-folha", "12", "--columns", "3", "--width", "640"])
    ok_fontes = True
    if a.insumo:
        # o Objetivo diz o que o slide faz: na cópia enviada ao conferidor ele é campo de nota (não vira conta de preço)
        with tempfile.TemporaryDirectory(prefix="fontes-") as tmpf:
            ent = Path(tmpf) / "notas.md"
            ent.write_text(re.sub(r"^(\s*)Objetivo:", r"\1NOTA: Objetivo:", (out / "notas.md").read_text(encoding="utf-8"),
                                  flags=re.M | re.I), encoding="utf-8")
            ok_fontes = rodar("4 fontes (Objetivo lido como nota)", [py, str(ferramenta("conferir_fontes.py")), "--entrega",
                                                                    str(ent), "--insumo"] + a.insumo) == 0
    else:
        print("\n== 4 fontes: sem --insumo, a conferência de número não rodou (diga isso no relato).")
    oks, trocas = [], 0
    with tempfile.TemporaryDirectory(prefix="lint-") as tmp:
        for nome in ("notas.md", "_notas-operador.md"):
            alvo = out / nome
            if TERMOS:
                txt, k = mascarar(alvo.read_text(encoding="utf-8"))
                trocas += k
                alvo = Path(tmp) / nome
                alvo.write_text(txt, encoding="utf-8")
            oks.append(rodar(f"5 lint {nome}", [py, str(ferramenta("lint_copy.py")), str(alvo)]) == 0)
    ok_lint = all(oks)
    if TERMOS:
        quais = ", ".join(f"{t} (x{k})" for t, k in sorted(USADOS.items(), key=lambda x: -x[1])) or "nenhum apareceu"
        print(f"\n== lint: {trocas} ocorrência(s) mascarada(s) só na cópia lintada. Termos que apareceram: {quais}.")
        if USADOS:
            bar = barrados_pelo_lint(list(USADOS), py)
            print("   Barrados pelo lint (o motivo do mascaramento): " + (", ".join(bar) if bar else "nenhum; o mascaramento não era necessário."))
    if not (ok_checar and ok_fontes and ok_lint):
        falhou = [x for x, ok in (("checar", ok_checar), ("fontes", ok_fontes), ("lint", ok_lint)) if not ok]
        sys.exit(f"\nREPROVADO em: {', '.join(falhou)}. Corrija o HTML do slide apontado e rode de novo.")
    print("\n== 6 pdf")
    pdf_dos_pngs(conf, out / "deck.pdf")
    pdf = out / "deck.pdf"
    if pdf.is_file() and pdf.stat().st_size > 0:
        print(f"pdf: gerado ({pdf.stat().st_size // 1024} KB, {len(list((conf / 'png').glob('slide-*.png')))} páginas, dos PNGs da conferência).")
    else:
        print("pdf: NÃO gerado (deck.pdf ausente ou vazio).")
    if rodar("7 pptx", [py, str(AQUI / "exportar_pptx.py"), str(out)]):
        sys.exit("BARRADO no passo 7 (PPTX).")
    mos = ", ".join(x.name for x in sorted(out.glob("mosaico*.png")))
    print(f"\nAPROVADO. {n} slides. Pasta: {out} (deck.html, deck.pptx, deck.pdf, {mos}, notas.md)")


if __name__ == "__main__":
    main()
