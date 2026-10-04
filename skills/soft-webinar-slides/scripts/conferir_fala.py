#!/usr/bin/env python3
"""conferir_fala.py: confere que a divisão do roteiro não mudou uma palavra da fala do dono.

Uso (a partir da pasta da skill):
  python3 scripts/conferir_fala.py [trabalho/roteiro-original.md] [trabalho/roteiro.md]

Sem argumentos, lê trabalho/roteiro-original.md (o roteiro do dono, intocado) contra
trabalho/roteiro.md (o dividido). Só biblioteca padrão.

O que compara (as duas leituras usam o mesmo leitor da skill, então aceitam os mesmos formatos):
  1. FALA: a sequência de palavras de Abre com, Clique N, a fala solta, Fecha com e TRANSIÇÃO,
     slide a slide, juntando tudo na ordem. Tem de ser igual nos dois arquivos. Pontuação, maiúscula,
     espaço e quebra de linha não contam; texto entre colchetes ([A CONFIRMAR ...], [BOTÃO]) não conta;
     "a mesma frase, sem pausa" (em Abre com, Clique N ou Fecha com) e "lê a frase da tela" não são
     fala do dono e não contam: em lista repartida o Abre com pode repetir o Clique 1 assim;
     o número depois de "slide" na TRANSIÇÃO não conta (a divisão renumera); linha toda entre
     parênteses, como "(segue direto pra garantia)", é direção de palco e não conta.
  2. TELA: palavra de CONTEÚDO do roteiro dividido que não existe em lugar nenhum do original
     (aviso: nada novo na tela).
Saída: IGUAL, ou DIFERENTE com as primeiras diferenças (palavras do original e do dividido, com um
pedaço de contexto). Código 0 quando a fala é igual, 1 quando difere. Aviso de tela não muda o código.
"""
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ler_roteiro import ler  # noqa: E402

PALAVRA = re.compile(r"\w+", re.UNICODE)
COLCHETE = re.compile(r"`?\[[^\]]*\]`?")
NAO_E_FALA = re.compile(r"^\s*((a\s+)?mesma\s+frase\b|l[eê] a frase da tela\b)", re.I)
DIRECAO = re.compile(r"^\s*\(.*\)\s*$", re.S)  # linha toda entre parênteses: direção de palco, não fala


def palavras(txt):
    txt = COLCHETE.sub(" ", txt or "")
    return [w.lower() for w in PALAVRA.findall(txt)]


def peca_de_fala(s):
    """As peças de fala de um slide, na ordem em que o roteiro as escreve."""
    pecas = []  # o filtro final tira "a mesma frase, sem pausa" de qualquer peça (Abre com, Clique N, Fecha com)
    if s["abre"]:
        pecas.append(s["abre"])
    pecas += s["fala"]
    pecas += s["cliques"]
    if s["fecha"] and not NAO_E_FALA.match(s["fecha"]):
        pecas.append(s["fecha"])
    if s["transicao"]:
        pecas.append(re.sub(r"\bslide\s*\d+", "slide", s["transicao"], flags=re.I))
    return [p for p in pecas if not NAO_E_FALA.match(p or "") and not DIRECAO.match(p or "")]


def fala_do_arquivo(caminho):
    ws = []
    for s in ler(caminho)["slides"]:
        for p in peca_de_fala(s):
            ws += palavras(p)
    return ws


def tela_do_arquivo(caminho):
    ws = []
    for s in ler(caminho)["slides"]:
        for t in s["tela"]:
            ws += palavras(t)
        for linha in s["tabela"]:
            for c in linha:
                ws += palavras(c)
    return ws


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__)
        return 0
    orig = Path(args[0] if args else "trabalho/roteiro-original.md")
    novo = Path(args[1] if len(args) > 1 else "trabalho/roteiro.md")
    for p in (orig, novo):
        if not p.is_file():
            sys.exit(f"Arquivo não encontrado: {p}")
    a, b = fala_do_arquivo(orig), fala_do_arquivo(novo)
    rc = 0
    if a == b:
        print(f"IGUAL: a fala tem {len(a)} palavras nos dois arquivos, na mesma ordem.")
    else:
        rc = 1
        print(f"DIFERENTE: o original tem {len(a)} palavras de fala e o dividido, {len(b)}. Primeiras diferenças:")
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        n = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            ctx = " ".join(a[max(0, i1 - 4):i1])
            print(f"  depois de '...{ctx}': original [{' '.join(a[i1:i2]) or '(nada)'}] / dividido [{' '.join(b[j1:j2]) or '(nada)'}]")
            n += 1
            if n >= 5:
                print("  (há mais diferenças)")
                break
    vocab = set(palavras(orig.read_text(encoding="utf-8")))
    novas = []
    for w in tela_do_arquivo(novo):
        if w not in vocab and w not in novas:
            novas.append(w)
    if novas:
        print(f"AVISO tela: palavra de CONTEÚDO que o original não traz: {', '.join(novas[:15])}. Nada novo na tela: confira.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
