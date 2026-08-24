#!/usr/bin/env python3
"""
Mede as metas de digitacao do chat simulado (soft-webinar, reference
simulador-comentarios-ao-vivo.md secao 5.3). Bloqueia a subida de um chat
em que uma mao so escreveu o elenco inteiro.

uso: python3 mede_digitacao.py <chat.csv> [--coluna message]
O CSV precisa ter uma coluna de texto (default: message) e, de preferencia,
uma coluna de autor (username/Nome) pra checar repeticao.
Sai 0 se todas as metas batem, 1 se alguma falha.
"""
import csv, re, sys, unicodedata
from collections import Counter

METAS = [
    ("comeca com maiuscula",  lambda m: m[:1].isupper(),                    0.20, 0.30),
    ("mais de 70 letras",     lambda m: len(m) > 70,                        0.08, 1.00),
    ("mais de 110 letras",    lambda m: len(m) > 110,                       0.02, 1.00),
    ("menos de 15 letras",    lambda m: len(m) < 15,                        0.10, 1.00),
    ("abreviacao/typo/risada",lambda m: bool(re.search(r'\b(tbm|pq|vc|msm|qnd|blz|vlw|tp|mt|hj)\b|kkk|rsrs|haha', m.lower())), 0.15, 0.30),
    ("emoji",                 lambda m: any(ord(c) > 0x2100 for c in m),    0.06, 0.12),
    ("sem nenhuma pontuacao", lambda m: not re.search(r'[,.!?]', m),        0.35, 0.50),
]

def norm(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', s)).strip()

def main():
    path = sys.argv[1]
    col = sys.argv[sys.argv.index('--coluna') + 1] if '--coluna' in sys.argv else 'message'
    rows = list(csv.DictReader(open(path, newline='')))
    if col not in rows[0]:
        print(f"coluna '{col}' nao existe. colunas: {list(rows[0].keys())}"); return 2
    msgs = [r[col] for r in rows]
    n = len(msgs)
    falhas = 0
    print(f"{n} comentarios em {path}\n")
    print(f"{'metrica':26} {'qtd':>5} {'%':>7}   alvo        veredito")
    for nome, teste, lo, hi in METAS:
        q = sum(1 for m in msgs if teste(m))
        pct = q / n
        ok = lo <= pct <= hi
        alvo = f"{lo:.0%}-{hi:.0%}" if hi < 1 else f">={lo:.0%}"
        if not ok: falhas += 1
        print(f"{nome:26} {q:5} {pct:6.1%}   {alvo:10}  {'OK' if ok else 'FALHA'}")

    # emoji em excesso na mesma mensagem
    mult = [m for m in msgs if sum(1 for c in m if ord(c) > 0x2100) > 1]
    print(f"\nmensagens com mais de 1 emoji: {len(mult)}  {'OK' if not mult else 'FALHA'}")
    if mult: falhas += 1

    # repeticao literal e coro de 4 seguidos
    dup = [t for t, c in Counter(norm(m) for m in msgs).items() if c > 1 and t]
    seguidas = sum(1 for i in range(len(msgs) - 3)
                   if len({norm(msgs[i+k]) for k in range(4)}) == 1)
    print(f"textos repetidos (fora do coro autorizado): {len(dup)}")
    for t in dup[:8]: print(f"   - {t}")
    print(f"blocos de 4 pessoas seguidas com o texto identico: {seguidas}  {'OK' if not seguidas else 'FALHA'}")
    if seguidas: falhas += 1

    print("\nVEREDITO DIGITACAO:", "OK" if not falhas else f"REPROVADO ({falhas} item(ns))")
    return 0 if not falhas else 1

if __name__ == '__main__':
    sys.exit(main())
