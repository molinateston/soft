#!/usr/bin/env python3
"""Confere as caixas de um campos.json antes de escrever no PDF.

Uso:
    conferir_caixas.py campos.json [--tolerancia 0.5] [--json]

Aceita os dois formatos de campos.json (a entrada do preencher_texto.py e a
saida do campos_info.py; veja o LEIA-ME-pdf.md) e acusa:
  - caixas da mesma pagina que se sobrepoem, inclusive caixa de texto
    contra rotulo (retangulo_rotulo);
  - caixa baixa demais para o tamanho da fonte (altura menor que
    1,2 vez o tamanho);
  - caixa sem largura ou sem altura.
Avisa, sem reprovar, quando o texto dado nao cabe na caixa no tamanho pedido
(o preencher_texto.py reduz a fonte nesse caso).

Saida: 0 tudo certo, 1 achou problema, 2 JSON fora do formato,
3 arquivo nao encontrado.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comum as c  # noqa: E402

FATOR_ALTURA = 1.2
TIPOS_SEM_FONTE = {"rotulo", "caixa_selecao", "radio", "botao", "assinatura", "lista"}


def _norm(r):
    return [min(r[0], r[2]), min(r[1], r[3]), max(r[0], r[2]), max(r[1], r[3])]


def conferir(caixas, tolerancia=0.5, medidor=None):
    """Devolve (problemas, avisos), cada um uma lista de textos."""
    problemas, avisos = [], []
    for cx in caixas:
        r = cx["ret"]
        if r[2] - r[0] <= 0 or r[3] - r[1] <= 0:
            problemas.append(f"pagina {cx['pagina']}: {cx['nome']} tem caixa sem largura ou "
                             f"altura {[c.r2(v) for v in r]}")
    validas = [cx for cx in caixas if cx["ret"][2] > cx["ret"][0] and cx["ret"][3] > cx["ret"][1]]

    for i, a in enumerate(validas):
        for b in validas[i + 1:]:
            if a["pagina"] != b["pagina"] or a["sistema"] != b["sistema"]:
                continue
            if a["tipo"] == "rotulo" and b["tipo"] == "rotulo":
                continue
            ra, rb = _norm(a["ret"]), _norm(b["ret"])
            larg = min(ra[2], rb[2]) - max(ra[0], rb[0])
            alt = min(ra[3], rb[3]) - max(ra[1], rb[1])
            if larg > tolerancia and alt > tolerancia:
                problemas.append(f"pagina {a['pagina']}: {a['nome']} se sobrepoe a {b['nome']} "
                                 f"({larg:.1f} x {alt:.1f} pt)")

    for cx in validas:
        tam = cx["tamanho_fonte"]
        if not tam or cx["tipo"] in TIPOS_SEM_FONTE:
            continue
        r = _norm(cx["ret"])
        alt = r[3] - r[1]
        if alt < tam * FATOR_ALTURA:
            problemas.append(f"pagina {cx['pagina']}: {cx['nome']} tem {alt:.1f} pt de altura, "
                             f"baixa demais para fonte {tam:g} (minimo {tam * FATOR_ALTURA:.1f} pt)")
            continue
        if cx["texto"] and medidor is not None:
            _, linhas, cabe = c.encaixar(cx["texto"], r[2] - r[0], alt, tam, tam, medidor, False)
            if not cabe:
                avisos.append(f"pagina {cx['pagina']}: o texto de {cx['nome']} nao cabe com fonte "
                              f"{tam:g} ({len(linhas)} linhas); a fonte sera reduzida ao escrever")
    return problemas, avisos


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Acusa caixas sobrepostas ou pequenas demais num campos.json.")
    ap.add_argument("campos", help="campos.json")
    ap.add_argument("--tolerancia", type=float, default=0.5,
                    help="sobreposicao em pontos que ainda e aceita (padrao 0.5)")
    ap.add_argument("--json", action="store_true", help="resultado em JSON na tela")
    args = ap.parse_args(argv)

    dados = c.ler_json(args.campos)
    caixas, erros = c.ler_caixas(dados)
    if erros:
        c.sair("campos.json fora do formato:\n  " + "\n  ".join(erros), c.ARGUMENTO)
    medidor = c.Medidor()
    problemas, avisos = conferir(caixas, args.tolerancia, medidor)

    if args.json:
        print(json.dumps({"caixas": len(caixas), "problemas": problemas, "avisos": avisos},
                         ensure_ascii=False, indent=2))
    else:
        for p in problemas:
            print("Problema: " + p)
        for a in avisos:
            print("Aviso: " + a)
        if problemas:
            print(f"{len(problemas)} problemas em {len(caixas)} caixas. Conserte e confira de novo.")
        else:
            print(f"{len(caixas)} caixas conferidas, nenhuma sobreposta ou pequena demais.")
    return c.REPROVOU if problemas else c.OK


if __name__ == "__main__":
    sys.exit(main())
