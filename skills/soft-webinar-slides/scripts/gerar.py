#!/usr/bin/env python3
"""gerar.py: a esteira inteira do deck numa chamada só.

  python3 scripts/gerar.py deck.json --saida <pasta> [--perfil perfil.json] [--insumo roteiro.md ...]

Passos (para no primeiro que barrar, e diz qual):
  1. montar_deck.py   -> deck.html e notas.md (barra lacuna e travessão na tela)
  2. checar_deck.py   -> conferência mecânica; PNG de cada slide em _conferencia/png
  3. make_mosaic.py   -> mosaico.png (sai mesmo se o passo 2 reprovar, pra você olhar)
  4. conferir_fontes.py -> todo número do notas.md (tela e fala) tem fonte no insumo
  5. lint_copy.py     -> notas.md e _notas-operador.md sem travessão, verbo-freio e clichê
  6. deck.pdf         -> dos PNGs da conferência, um slide por página (só com 2, 4 e 5 aprovados)
  7. exportar_pptx.py -> deck.pptx editável, notas e animação por clique
Sai com código 0 só com tudo aprovado.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def ferramenta(nome):
    """lint_copy.py e conferir_fontes.py: a cópia de scripts/ na raiz da skill (a que o
    sync mantém igual à fonte); sem ela, a desta pasta. Assim o motor roda igual
    dentro desta skill e copiado em shared-references/ de outra."""
    for d in [AQUI, *AQUI.parents]:
        if (d / "SKILL.md").exists():
            if (d / "scripts" / nome).exists():
                return d / "scripts" / nome
            break
    return AQUI / nome


def rodar(nome, cmd, timeout=600):
    print(f"\n== {nome}")
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    saida = (r.stdout + r.stderr).strip().splitlines()
    corte = [ln for ln in saida if ln.startswith(("REPROVOU", "BARRADO", "AVISO"))]
    for ln in (corte + [x for x in saida[-12:] if x not in corte]) if len(saida) > 25 else saida:
        print("  " + ln)
    print(f"  ({time.time() - t0:.0f} s)")
    return r.returncode


def pdf_dos_pngs(conf, destino):
    """O PDF sai dos PNGs que a conferência já tirou (estado final de cada slide):
    nenhuma segunda renderização do deck, e a página aponta pros arquivos em vez
    de carregar tudo na memória."""
    from playwright.sync_api import sync_playwright
    pngs = sorted((conf / "png").glob("slide-*.png"))
    pags = "".join(f'<div class="p"><img src="png/{x.name}"></div>' for x in pngs)
    pagina = conf / "pdf.html"
    pagina.write_text("<html><head><style>*{margin:0;padding:0}@page{size:1920px 1080px;margin:0}"
                      ".p{width:1920px;height:1080px;page-break-after:always;overflow:hidden}.p:last-child{page-break-after:auto}"
                      "img{width:1920px;height:1080px;display:block}</style></head><body>" + pags + "</body></html>", encoding="utf-8")
    with sync_playwright() as p:
        try:
            br = p.chromium.launch()
        except Exception:
            br = p.chromium.launch(executable_path="/snap/bin/chromium")
        pg = br.new_page()
        pg.goto(pagina.resolve().as_uri(), wait_until="load", timeout=300000)
        pg.pdf(path=str(destino), width="1920px", height="1080px", print_background=True)
        br.close()
    pagina.unlink()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--perfil")
    ap.add_argument("--insumo", nargs="*", default=[])
    ap.add_argument("--max-palavras", default="40")
    a = ap.parse_args()
    out = Path(a.saida)
    conf = out / "_conferencia"
    py = sys.executable
    cmd = [py, str(AQUI / "montar_deck.py"), a.deck, "--saida", str(out)] + (["--perfil", a.perfil] if a.perfil else [])
    if rodar("1 montar", cmd):
        sys.exit("BARRADO no passo 1: corrija o deck.json (lacuna ou campo na tela) e rode de novo.")
    ok_checar = rodar("2 checar", [py, str(AQUI / "checar_deck.py"), str(out), "--png", str(conf / "png"),
                                   "--max-palavras", a.max_palavras, "--min-fonte", "24"]) == 0
    rodar("3 mosaico", [py, str(AQUI / "make_mosaic.py"), str(conf / "png"), str(out / "mosaico.png")])
    ok_fontes = True
    if a.insumo:
        ok_fontes = rodar("4 fontes", [py, str(ferramenta("conferir_fontes.py")), "--entrega", str(out / "notas.md"),
                                       "--insumo"] + a.insumo) == 0
    else:
        print("\n== 4 fontes: sem --insumo, a conferência de número não rodou (diga isso no relato).")
    ok_lint = all([rodar(f"5 lint {nome}", [py, str(ferramenta("lint_copy.py")), str(out / nome)]) == 0
                   for nome in ("notas.md", "_notas-operador.md")])
    if not (ok_checar and ok_fontes and ok_lint):
        falhou = [n for n, ok in (("checar", ok_checar), ("fontes", ok_fontes), ("lint", ok_lint)) if not ok]
        sys.exit(f"\nREPROVADO em: {', '.join(falhou)}. Corrija o deck.json e rode de novo. Mosaico pra olhar: {', '.join(str(x) for x in sorted(out.glob('mosaico*.png')))}")
    print("\n== 6 pdf")
    t0 = time.time()
    pdf_dos_pngs(conf, out / "deck.pdf")
    print(f"  {out / 'deck.pdf'} ({time.time() - t0:.0f} s)")
    if rodar("7 pptx", [py, str(AQUI / "exportar_pptx.py"), str(out)]):
        sys.exit("BARRADO no passo 7 (PPTX).")
    mos = ", ".join(x.name for x in sorted(out.glob("mosaico*.png")))
    print(f"\nAPROVADO. Pasta: {out} (deck.html, deck.pptx, deck.pdf, {mos}, notas.md)")


if __name__ == "__main__":
    main()
