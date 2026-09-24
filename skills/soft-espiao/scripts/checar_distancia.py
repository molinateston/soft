#!/usr/bin/env python3
"""
checar_distancia.py: confere se o brief de modelagem ficou longe o bastante do
anuncio de referencia. Conta as sequencias de N palavras seguidas (padrao 5)
que aparecem nos dois textos, sem acento e sem pontuacao.

USO:
  python3 scripts/checar_distancia.py --referencia ref.txt --brief brief.md
  python3 scripts/checar_distancia.py --referencia ref.txt --brief brief.md --n 4
  python3 scripts/checar_distancia.py --referencia ref.txt --brief ficha-x-1.md --ignorar-cerca

O texto de referencia e a copy ou a transcricao do anuncio concorrente, colada
num .txt. O brief e lido INTEIRO, bloco cercado incluso: copia escondida numa
cerca tambem reprova. So a ficha da engenharia reversa, onde mora a citacao de
estudo dentro de bloco cercado (```), roda com --ignorar-cerca.

Exit 0: nenhuma sequencia repetida. Exit 1: ha repeticao (reescreva na voz do
dono). Exit 5: erro de uso.
"""
import argparse
import re
import sys
import unicodedata

FENCE = re.compile(r"^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$", re.M | re.S)


def palavras(t):
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.findall(r"[a-z0-9]+", t)


def ngramas(ws, n):
    return {" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--referencia", required=True)
    p.add_argument("--brief", required=True)
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--ignorar-cerca", action="store_true",
                   help="tira os blocos cercados da conta (so pra ficha, nunca pro brief)")
    a = p.parse_args()
    if a.n < 3:
        print("ERRO: --n minimo e 3", file=sys.stderr)
        return 5
    try:
        ref = open(a.referencia, encoding="utf-8").read()
        brief = open(a.brief, encoding="utf-8").read()
        if a.ignorar_cerca:
            brief = FENCE.sub("", brief)
    except OSError as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 5
    comuns = sorted(ngramas(palavras(ref), a.n) & ngramas(palavras(brief), a.n))
    for s in comuns[:30]:
        print(f"repetido: {s}")
    print(f"sequencias de {a.n} palavras iguais a referencia: {len(comuns)}")
    return 1 if comuns else 0


if __name__ == "__main__":
    sys.exit(main())
