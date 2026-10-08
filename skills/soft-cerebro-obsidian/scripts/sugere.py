#!/usr/bin/env python3
"""Sugere conceitos para o mapa: as palavras que mais se repetem nas notas e ainda não são conceito.

Uso:  python3 sugere.py <config.json> [quantas]

Mostra palavras com a contagem de notas em que aparecem. O agente escolhe as que fazem sentido,
dá um nome e um núcleo (hub) a cada uma e põe no config. Palavra comum demais liga tudo com tudo:
ignore as que aparecem em mais da metade das notas.
"""
import collections
import glob
import json
import os
import re
import sys
import unicodedata


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


PARADAS = set(norm(x) for x in """
a o as os um uma uns umas de do da dos das em no na nos nas por para com sem sob sobre entre ate apos ante
e ou mas se que qual quais quando onde como porque pois ja nao sim mais menos muito pouco tambem so apenas
eu tu ele ela nos eles elas meu minha seu sua nosso nossa isso isto esse essa este esta aquele aquela
ser estar ter haver fazer ir vir poder dever ficar dar ver sao foi era tem tinha fez vai vao pode deve esta estao
todo toda todos todas cada outro outra outros outras mesmo mesma ainda sempre nunca depois antes agora hoje
sobre apos desde durante conforme segundo cerca abaixo acima dentro fora entao assim aqui ali la
nota notas mapa link links arquivo pasta md
""".split())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cfg_path = os.path.abspath(sys.argv[1])
    quantas = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    base = os.path.dirname(cfg_path)
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    raiz = os.path.normpath(os.path.join(base, cfg.get("raiz", "brain")))
    regs = []
    for c in cfg.get("conceitos", []):
        try:
            regs.append(re.compile(norm(c["regex"])))
        except re.error:
            pass
    docs = []
    for p in glob.glob(os.path.join(raiz, "**", "*.md"), recursive=True):
        partes = os.path.relpath(p, raiz).split(os.sep)
        if any(x.startswith("_") or x == "ESTADO" for x in partes):
            continue
        docs.append(norm(open(p, encoding="utf-8", errors="ignore").read()))
    if not docs:
        print("nenhuma nota encontrada em", raiz)
        sys.exit(1)
    cont = collections.Counter()
    for t in docs:
        for w in set(re.findall(r"[a-z]{5,}", t)):
            if w not in PARADAS:
                cont[w] += 1
    n = len(docs)
    print(f"{n} notas lidas. Palavra · em quantas notas aparece")
    mostradas = 0
    for w, c in cont.most_common():
        if c < 2:
            break
        if any(r.search(w) for r in regs):
            continue
        marca = "  (comum demais, evite)" if c > n / 2 else ""
        print(f"{w} · {c}{marca}")
        mostradas += 1
        if mostradas >= quantas:
            break
    if mostradas == 0:
        print("nenhuma palavra nova aparece em 2 ou mais notas. Escreva mais notas antes de definir conceitos.")


if __name__ == "__main__":
    main()
