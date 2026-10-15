#!/usr/bin/env python3
"""Escreve texto em retangulos de um PDF sem campos (formulario chapado).

Uso:
    preencher_texto.py ENTRADA.pdf campos.json SAIDA.pdf
                       [--fonte-minima 6] [--sem-reduzir] [--fonte-metrica ARQ.ttf]

Cada item de campos.json traz pagina, retangulo e texto (e, se quiser,
tamanho_fonte, cor, alinhamento e retangulo_rotulo). O retangulo esta no
sistema "topo" (origem em cima a esquerda, em pontos, o mesmo do
estrutura.py) a menos que o arquivo diga "sistema": "pdf". Com
"escala_dpi": N, os numeros sao pixels de uma imagem feita naquele dpi.
Formato completo no LEIA-ME-pdf.md.

O texto vira uma anotacao de texto livre (FreeText) sem borda e sem fundo,
com aparencia propria, quebrada em linhas para caber na caixa. Se nao couber,
a fonte diminui ate o minimo; se nem assim couber, o texto e gravado no
minimo, cortado na borda da caixa, e o item e relatado.

Saida: 0 tudo coube, 1 algum texto nao coube ou item invalido,
2 argumento errado, 3 falta pypdf ou arquivo.
"""

import argparse
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comum as c  # noqa: E402

MATRIZ_GIRO = {0: [1, 0, 0, 1, 0, 0], 90: [0, 1, -1, 0, 0, 0],
               180: [-1, 0, 0, -1, 0, 0], 270: [0, -1, 1, 0, 0, 0]}
Q_ALINHAMENTO = {"esquerda": 0, "centro": 1, "direita": 2}


def anotacao(escritor, ret_pdf, giro, texto, tamanho, linhas, cor, alinhamento, medidor):
    """Cria o dicionario da anotacao FreeText com fluxo de aparencia."""
    from pypdf.generic import (ArrayObject, DecodedStreamObject, DictionaryObject,
                               FloatObject, NameObject, NumberObject, TextStringObject)
    larg_u, alt_u = ret_pdf[2] - ret_pdf[0], ret_pdf[3] - ret_pdf[1]
    # tamanho da caixa como ela aparece na pagina girada
    larg, alt = (alt_u, larg_u) if giro in (90, 270) else (larg_u, alt_u)
    corpo, trocados = c.conteudo_texto(linhas, tamanho, larg, alt, medidor, cor, alinhamento)
    fluxo = DecodedStreamObject()
    fluxo.set_data(corpo)
    fluxo.update({
        NameObject("/Type"): NameObject("/XObject"),
        NameObject("/Subtype"): NameObject("/Form"),
        NameObject("/BBox"): ArrayObject([FloatObject(0), FloatObject(0),
                                          FloatObject(round(larg, 3)), FloatObject(round(alt, 3))]),
        NameObject("/Matrix"): ArrayObject([NumberObject(v) for v in MATRIZ_GIRO[giro]]),
        NameObject("/Resources"): DictionaryObject({
            NameObject("/Font"): DictionaryObject({NameObject("/F1"): c.fonte_helvetica(escritor)})}),
    })
    r, g, b = cor
    hexa = "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))
    anot = DictionaryObject({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/FreeText"),
        NameObject("/Rect"): ArrayObject([FloatObject(round(v, 3)) for v in ret_pdf]),
        NameObject("/Contents"): TextStringObject(texto),
        NameObject("/NM"): TextStringObject("soft-" + uuid.uuid4().hex[:12]),
        NameObject("/F"): NumberObject(4),
        NameObject("/Q"): NumberObject(Q_ALINHAMENTO[alinhamento]),
        NameObject("/DA"): TextStringObject("/Helv %.2f Tf %.3f %.3f %.3f rg" % (tamanho, r, g, b)),
        NameObject("/DS"): TextStringObject(f"font: Helvetica {tamanho:g}pt; color:{hexa}"),
        NameObject("/Border"): ArrayObject([NumberObject(0)] * 3),
        NameObject("/BS"): DictionaryObject({NameObject("/W"): NumberObject(0)}),
        NameObject("/AP"): DictionaryObject({NameObject("/N"): escritor._add_object(fluxo)}),
    })
    if giro:
        anot[NameObject("/Rotate")] = NumberObject(giro)
    return anot, trocados


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Escreve texto em retangulos de um PDF sem campos.")
    ap.add_argument("entrada", help="PDF de entrada")
    ap.add_argument("campos", help="campos.json com pagina, retangulo e texto")
    ap.add_argument("saida", help="PDF de saida")
    ap.add_argument("--fonte-minima", type=float, default=6.0,
                    help="menor tamanho de fonte aceito ao reduzir (padrao 6)")
    ap.add_argument("--sem-reduzir", action="store_true",
                    help="nunca diminui a fonte; so relata o que nao coube")
    ap.add_argument("--fonte-metrica",
                    help="arquivo .ttf com larguras da Helvetica (padrao: Liberation Sans)")
    args = ap.parse_args(argv)
    if args.fonte_minima <= 0:
        c.sair("--fonte-minima precisa ser maior que zero.", c.ARGUMENTO)

    pypdf = c.exigir_pypdf()
    from pypdf.generic import ArrayObject, NameObject
    leitor = c.abrir_pdf(args.entrada)
    dados = c.ler_json(args.campos)
    if isinstance(dados, list):
        dados = {"campos": dados}
    if not isinstance(dados, dict) or not isinstance(dados.get("campos"), list):
        c.sair("campos.json precisa ter a lista 'campos'.", c.ARGUMENTO)
    _, erros = c.ler_caixas(dados)
    if erros:
        c.sair("campos.json com problema:\n  " + "\n  ".join(erros), c.ARGUMENTO)

    topo = {k: v for k, v in dados.items() if k != "campos"}
    escritor = pypdf.PdfWriter(clone_from=leitor)
    medidor = c.Medidor(args.fonte_metrica)
    total = len(escritor.pages)
    escritos, nao_couberam, invalidos, vazios, fora, trocados = 0, [], [], [], [], []

    for original in dados["campos"]:
        if isinstance(original, dict) and "widgets" in original:
            invalidos.append(f"{original.get('nome')}: item da saida do campos_info.py; "
                             "para PDF com campos use preencher_campos.py")
            continue
        uma, _ = c.ler_caixas(dict(topo, campos=[original]))
        uma = [cx for cx in uma if cx["tipo"] != "rotulo"]
        if not uma:
            continue
        cx = uma[0]
        nome = cx["nome"]
        if not cx["texto"]:
            vazios.append(nome)
            continue
        if cx["pagina"] > total:
            invalidos.append(f"{nome}: pagina {cx['pagina']} nao existe (o PDF tem {total})")
            continue
        alin = str(original.get("alinhamento", "esquerda"))
        if alin not in Q_ALINHAMENTO:
            invalidos.append(f"{nome}: alinhamento '{alin}' invalido (esquerda, centro, direita)")
            continue
        try:
            cor = c.cor_hex(original.get("cor"))
        except ValueError as e:
            invalidos.append(f"{nome}: {e}")
            continue
        pagina = escritor.pages[cx["pagina"] - 1]
        info = c.info_pagina(pagina)
        ret = cx["ret"]
        ret_pdf = (c.ret_topo_para_pdf(info, ret) if cx["sistema"] == "topo"
                   else [min(ret[0], ret[2]), min(ret[1], ret[3]),
                         max(ret[0], ret[2]), max(ret[1], ret[3])])
        larg_u, alt_u = ret_pdf[2] - ret_pdf[0], ret_pdf[3] - ret_pdf[1]
        if larg_u <= 0 or alt_u <= 0:
            invalidos.append(f"{nome}: retangulo sem largura ou altura")
            continue
        if (ret_pdf[0] < info["x0"] - 0.5 or ret_pdf[1] < info["y0"] - 0.5
                or ret_pdf[2] > info["x1"] + 0.5 or ret_pdf[3] > info["y1"] + 0.5):
            fora.append(nome)
        larg, alt = (alt_u, larg_u) if info["giro"] in (90, 270) else (larg_u, alt_u)
        tam_pedido = cx["tamanho_fonte"] or 10.0
        tam, linhas, cabe = c.encaixar(cx["texto"], larg, alt, tam_pedido,
                                       args.fonte_minima, medidor, not args.sem_reduzir)
        anot, tr = anotacao(escritor, ret_pdf, info["giro"], cx["texto"], tam, linhas,
                            cor, alin, medidor)
        trocados += tr
        ref = escritor._add_object(anot)
        anot[NameObject("/P")] = pagina.indirect_reference
        if "/Annots" in pagina:
            pagina["/Annots"].get_object().append(ref)
        else:
            pagina[NameObject("/Annots")] = ArrayObject([ref])
        escritos += 1
        if not cabe:
            nao_couberam.append(f"{nome}: nao coube nem com fonte {tam:g} "
                                f"(caixa {larg:.1f} x {alt:.1f} pt, {len(linhas)} linhas)")
        elif tam < tam_pedido:
            print(f"{nome}: fonte reduzida de {tam_pedido:g} para {tam:g} para caber.")

    try:
        with open(args.saida, "wb") as f:
            escritor.write(f)
    except OSError as e:
        c.sair(f"Nao consegui gravar {args.saida}: {e}", c.DEPENDENCIA)

    print(f"{escritos} textos escritos em {args.saida}.")
    for linha in nao_couberam:
        print("Texto nao coube: " + linha)
    for linha in invalidos:
        print("Item ignorado: " + linha)
    if fora:
        print("Aviso: caixa saindo da pagina: " + ", ".join(fora))
    if vazios:
        print("Ficaram vazios (sem texto no campos.json): " + ", ".join(vazios))
    if trocados:
        print("Aviso: caracteres sem desenho na Helvetica viraram '?': "
              + "".join(sorted(set(trocados))))
    return c.REPROVOU if (nao_couberam or invalidos) else c.OK


if __name__ == "__main__":
    sys.exit(main())
