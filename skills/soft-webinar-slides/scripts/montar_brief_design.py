#!/usr/bin/env python3
"""montar_brief_design.py: o modo Claude Design. Reproduz o processo que deu certo:
o guia provado, inteiro e sem mudança, no topo de cada parte, mais os slides daquela
parte no contrato do roteiro, mais a identidade do dono, mais o pedido explícito de
desenhar cada slide com juízo visual.

  python3 scripts/montar_brief_design.py <roteiro.md> --saida <pasta> [--perfil perfil.json] [--max-palavras 6500]

Grava BRIEF-CLAUDE-DESIGN-parte-01.md, -02.md ... Cada parte tem até 6.500 palavras
com o guia incluído e vale sozinha; a primeira diz como colar as demais. Todo slide do
roteiro aparece uma vez e na ordem; o que o roteiro tira por falta de dado aparece no
lugar dele como "fora do deck", com o que falta. Lacuna do roteiro vira [FALTA DO DONO].
No fim roda o lint_copy.py em cada parte.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
from gerar import ferramenta  # noqa: E402
from ler_roteiro import LACUNA, ler  # noqa: E402
from montar_deck import carregar_perfil  # noqa: E402

GUIA = RAIZ / "references" / "guia-slides-provado.md"
INI, FIM = "=== GUIA DE SLIDES PROVADO (início, siga à risca) ===", "=== GUIA DE SLIDES PROVADO (fim) ==="
PALAVRAS = re.compile(r"\S+")


def palavras(txt):
    return len(PALAVRAS.findall(txt))


def lacunas(txt):
    """[A CONFIRMAR: x] e afins viram [FALTA DO DONO: x]; o resto do texto fica igual."""
    def troca(m):
        miolo = re.sub(r"^(A CONFIRMAR|DO DONO|A DEFINIR|FALTA|PREENCHER)\s*:?\s*", "", m.group(0).strip("`[]"), flags=re.I)
        return f"[FALTA DO DONO: {miolo}]" if miolo else "[FALTA DO DONO]"
    return LACUNA.sub(troca, txt)


def identidade(p, com_perfil):
    c = p["cores"]
    fonte = p["fonte"].split(",")[0].strip("'\" ")
    acao = p["fonte_acao"].split(",")[0].strip("'\" ")
    origem = "a do dono" if com_perfil else "neutra (o dono não mandou cores nem fonte; troque se ele mandar)"
    ln = [f"## A identidade visual ({origem})", "",
          f"- Fonte: {fonte} no deck inteiro. Fonte de ação, só nas pílulas de comando (\"Escreve no chat\", \"O link está no chat\"): {acao}.",
          f"- Cor de destaque, a do que importa: {c['destaque_escuro']} no fundo escuro e {c['destaque_claro']} no fundo claro.",
          f"- Cor de ação e desconto (link, botão, pílula de percentual): {c['acao']}.",
          f"- Cor reservada, só na tarja do bônus dos primeiros, no risco do preço antigo e no rótulo BÔNUS da tabela: {c['reservada']}.",
          f"- Fundo escuro {c['fundo_escuro']} com texto {c['tinta_escura']}; fundo claro {c['fundo_claro']} com texto {c['tinta_clara']}. "
          f"O primeiro bloco da aula abre no fundo {p.get('fundo_inicial', 'escuro')}, e o fundo troca quando o bloco muda.",
          f"- Marca no rodapé: {p.get('marca') or 'nenhuma'}. Logo: {'o arquivo que o dono anexar' if p.get('logo') else 'nenhum'}."]
    if p.get("nome"):
        ln.append(f"- Quem apresenta: {p['nome']}.")
    return "\n".join(ln) + "\n"


PEDIDO = """## O pedido

Desenhe os slides {faixa} desta aula, na ordem e com a numeração do roteiro, em 16:9 (1920 por 1080). Desenhe cada slide com juízo visual, mostre em vez de contar, use imagem, SVG e número como imagem; não entregue slide de texto puro. O guia acima já foi provado num deck real: siga as regras, as receitas e o checklist dele.

- A tela sai do CONTEÚDO de cada slide, na versão curta que se lê em 3 segundos. Nunca acrescente ideia, número, nome ou promessa.
- As NOTAS vão nas notas do apresentador, nunca na tela, no formato da seção 5 do guia.
- O que aparece como [FALTA DO DONO] fica fora da tela. Não desenhe dado, print, logo ou depoimento no lugar: o bloco sai e a lacuna vai pras notas.
- Slide marcado FORA DO DECK não se desenha; ele está aqui só pra numeração bater com o roteiro.
- Antes de passar pro slide seguinte, olhe o slide pronto e passe o checklist da seção 8 do guia; o que der "não", refaça.
"""

ENTREGA = """## Como entregar

1. Um slide por vez, na ordem; mostre cada um pronto antes do seguinte.
2. A animação por clique segue a seção 6 do guia: o que já está na tela quando o slide abre, e um bloco por clique.
3. No fim desta parte, exporte no formato que o Claude Design oferecer (PDF, PPTX ou link de apresentação), com as notas junto quando o formato permitir.
"""


def bloco_slide(s, topicos):
    ref = f"Tópico {s['num']}" if topicos else f"Slide {s['num']}"
    ln = [f"### {ref} · {lacunas(s['titulo'])}", ""]
    fora = s["sai"] or (not s["tela"] and not s["tabela"] and s["falta"])
    if fora:
        ln.append("FORA DO DECK: não desenhe este slide até o dono mandar o que falta.")
        ln += [f"- [FALTA DO DONO: {x}]" for x in s["falta"]] or ["- [FALTA DO DONO: o conteúdo deste slide]"]
        return "\n".join(ln) + "\n"
    ln.append(f"TÍTULO: {lacunas(s['titulo'])}")
    if s["fase"]:
        ln.append(f"BLOCO: {s['fase']}")
    if s["objetivo"] or s["nota_objetivo"]:
        ln.append(f"OBJETIVO: {lacunas(s['objetivo'] or s['nota_objetivo'])}")
    ln.append("CONTEÚDO (a tela):")
    ln += [f"- {lacunas(x)}" for x in s["tela"]] or ["- (o roteiro não traz linha de tela: a tela é o título, dito como frase)"]
    if s["tabela"]:
        ln.append("Tabela do roteiro:")
        for row in s["tabela"]:
            ln.append("| " + " | ".join(lacunas(c) for c in row) + " |")
        if any(LACUNA.search(c) for row in s["tabela"] for c in row):
            ln.append("Falta valor em item da tabela: não desenhe soma nem total. Mostre só os itens, sem valor, e a lacuna vai pras notas.")
    longas = [x for x in s["tela"] if palavras(x) > 20]
    if longas:
        ln.append(f"Linha longa ({len(longas)}): a tela leva a versão curta que diz o mesmo; a frase inteira vai pras notas.")
    if s["mostrar"]:
        ln += [f"MOSTRAR: {lacunas(x)}" for x in s["mostrar"]]
    if s["falta"]:
        ln.append("FALTA DO DONO (fora da tela, vai pras notas):")
        ln += [f"- [FALTA DO DONO: {x}]" for x in s["falta"]]
    ln.append("NOTAS:")
    fala = []
    if s["abre"]:
        fala.append(f"- FALA, abre com: {lacunas(s['abre'])}")
    fala += [f"- Clique {i}: {lacunas(c)}" for i, c in enumerate(s["cliques"], 1)]
    fala += [f"- FALA: {lacunas(x)}" for x in s["fala"]]
    if s["fecha"]:
        fala.append(f"- Fecha com: {lacunas(s['fecha'])}")
    ln += fala or ["- FALA: [FALTA DO DONO: a fala deste slide]"]
    if s["transicao"]:
        ln.append(f"- TRANSIÇÃO: {lacunas(s['transicao'])}")
    if s["hora"]:
        ln.append(f"- Hora-meta: {lacunas(s['hora'])}")
    if s["pode_pular"]:
        ln.append("- Pode pular, se a aula atrasar.")
    ln += [f"- Obs.: {lacunas(x)}" for x in s["notas_livres"]]
    return "\n".join(ln) + "\n"


def cabecalho(titulo, k, total, faixa):
    t = f"# Brief dos slides: {titulo}, parte {k} de {total}\n\n"
    if total == 1:
        return t + ("Como usar: abra o Claude Design (ou uma conversa nova no Claude), cole este brief inteiro e mande. "
                    "Ele traz o guia de slides, a identidade, o pedido e todos os slides da aula.\n\n")
    if k == 1:
        return t + (f"Como usar: este brief tem {total} partes, pra caber numa mensagem. Abra o Claude Design (ou uma conversa nova no Claude), "
                    f"cole esta parte 1 inteira e mande. Quando os slides dela estiverem prontos e conferidos, cole a parte 2 na mesma conversa, "
                    "e assim por diante, sempre na ordem. Cada parte traz o guia inteiro e a identidade e vale sozinha: se a conversa ficar longa, "
                    "abra outra e cole a parte seguinte. No fim, junte os arquivos exportados na ordem das partes.\n\n")
    return t + (f"Esta é a parte {k} de {total}, com os slides {faixa}. Ela vale sozinha. Na mesma conversa das partes anteriores, "
                "mantenha o mesmo visual e siga a numeração do roteiro.\n\n")


def montar(titulo, slides, topicos, perfil, com_perfil, limite):
    guia = GUIA.read_text(encoding="utf-8")
    blocos = [bloco_slide(s, topicos) for s in slides]
    fixo = palavras(guia) + palavras(PEDIDO) + palavras(ENTREGA) + palavras(identidade(perfil, com_perfil)) + 160
    if fixo >= limite:
        sys.exit(f"O guia e o texto fixo já somam {fixo} palavras; o teto de {limite} não deixa espaço pros slides.")
    grupos, atual, conta = [], [], fixo
    for i, b in enumerate(blocos):
        w = palavras(b)
        if atual and conta + w > limite:
            grupos.append(atual)
            atual, conta = [], fixo
        atual.append(i)
        conta += w
    if atual:
        grupos.append(atual)
    partes = []
    for k, g in enumerate(grupos, 1):
        rot = "tópicos" if topicos else "slides"
        faixa = f"{slides[g[0]]['num']} a {slides[g[-1]]['num']}" if len(g) > 1 else slides[g[0]]["num"]
        txt = cabecalho(titulo, k, len(grupos), f"{rot} {faixa}")
        txt += f"{INI}\n\n{guia.rstrip()}\n\n{FIM}\n\n"
        txt += PEDIDO.format(faixa=f"{rot.rstrip('s') if len(g) == 1 else rot} {faixa}") + "\n"
        txt += identidade(perfil, com_perfil) + "\n"
        txt += f"## Os {rot} desta parte\n\n" + "\n".join(blocos[i] for i in g) + "\n"
        txt += ENTREGA
        partes.append(txt)
    return partes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro", help="roteiro.md: slide a slide (### Slide N · título) ou só tópicos")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--perfil")
    ap.add_argument("--max-palavras", type=int, default=6500)
    a = ap.parse_args()
    perfil = carregar_perfil(a.perfil)
    dados = ler(a.roteiro)
    if not dados["slides"]:
        sys.exit("Nenhum slide lido. O roteiro precisa de '### Slide N · título' ou de uma lista de tópicos.")
    titulo = re.sub(r"\s*\(.*?\)\s*$", "", lacunas(dados["titulo"] or "Aula")).strip() or "Aula"
    partes = montar(titulo, dados["slides"], bool(dados.get("topicos")), perfil, bool(a.perfil), a.max_palavras)
    out = Path(a.saida)
    out.mkdir(parents=True, exist_ok=True)
    for velho in out.glob("BRIEF-CLAUDE-DESIGN-parte-*.md"):
        velho.unlink()
    rc = 0
    for k, txt in enumerate(partes, 1):
        arq = out / f"BRIEF-CLAUDE-DESIGN-parte-{k:02d}.md"
        arq.write_text(txt, encoding="utf-8")
        r = subprocess.run([sys.executable, str(ferramenta("lint_copy.py")), str(arq)], capture_output=True, text=True)
        rc = rc or r.returncode
        dura = [x.strip() for x in (r.stdout + r.stderr).splitlines() if x.strip().startswith("✗")]
        print(f"{arq.name}: {palavras(txt)} palavras, lint exit {r.returncode}" + (f" ({'; '.join(dura)[:300]})" if dura else ""))
    ident = "perfil do dono" if a.perfil else "identidade neutra da skill (sem perfil do dono)"
    print(f"{len(dados['slides'])} slides do roteiro em {len(partes)} parte(s) -> {out} · identidade: {ident}")
    if rc:
        print("Lint reprovou alguma parte: reescreva a frase apontada no roteiro e rode de novo.")
    sys.exit(1 if rc else 0)


if __name__ == "__main__":
    main()
