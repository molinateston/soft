#!/usr/bin/env python3
"""Aceita todas as alterações rastreadas de um .docx, direto no XML.

Não usa LibreOffice. O resultado é o documento como ficaria clicando em
"Aceitar todas as alterações" no Word:

- inserção (w:ins) vira texto normal; exclusão (w:del) some com o conteúdo;
- movimento: a origem (w:moveFrom) some e o destino (w:moveTo) vira normal,
  e as marcas de intervalo de movimento somem;
- mudança de formatação (w:rPrChange, w:pPrChange, w:sectPrChange,
  w:tblPrChange, w:tblPrExChange, w:trPrChange, w:tcPrChange,
  w:tblGridChange, w:numberingChange) some e fica o estado novo;
- marca de parágrafo excluída junta o parágrafo com o seguinte;
- linha de tabela excluída some, linha inserida vira normal; célula
  excluída some, célula inserida vira normal;
- nenhum w:delText nem w:delInstrText sobra.

Vale para o corpo, cabeçalhos, rodapés, notas de rodapé e de fim,
comentários, estilos e numeração.

Uso:
    python3 aceitar_alteracoes.py ENTRADA.docx -o SAIDA.docx
    python3 aceitar_alteracoes.py PASTA_DESEMPACOTADA            (edita no lugar)
    python3 aceitar_alteracoes.py ENTRADA.docx -o SAIDA.docx --desligar-rastreio

Saída: 0 feito, 1 sobrou marca de alteração depois de aceitar,
2 argumento errado, 3 arquivo faltando ou ilegível.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comum_docx import (  # noqa: E402
    NS, SAIDA_OK, SAIDA_REPROVOU, abrir_ou_sair, w, nome_local, espaco, W,
)

MUDANCAS_DE_PROPRIEDADE = [
    "rPrChange", "pPrChange", "sectPrChange", "tblPrChange", "tblPrExChange",
    "trPrChange", "tcPrChange", "tblGridChange", "numberingChange",
]
MARCAS_DE_INTERVALO = [
    "moveFromRangeStart", "moveFromRangeEnd", "moveToRangeStart", "moveToRangeEnd",
    "customXmlInsRangeStart", "customXmlInsRangeEnd",
    "customXmlDelRangeStart", "customXmlDelRangeEnd",
    "customXmlMoveFromRangeStart", "customXmlMoveFromRangeEnd",
    "customXmlMoveToRangeStart", "customXmlMoveToRangeEnd",
]
# Tudo que não pode existir depois de aceitar.
PROIBIDOS = (["ins", "del", "moveFrom", "moveTo", "delText", "delInstrText",
              "cellIns", "cellDel", "cellMerge"]
             + MUDANCAS_DE_PROPRIEDADE + MARCAS_DE_INTERVALO)

M_R = "{%s}r" % NS["m"]


def tirar(el):
    """Remove o elemento (e a cauda dele, que em WordprocessingML é só recuo)."""
    pai = el.getparent()
    if pai is not None:
        pai.remove(el)


def desembrulhar(el):
    """Põe os filhos no lugar do elemento."""
    pai = el.getparent()
    if pai is None:
        return
    pos = pai.index(el)
    for filho in reversed(list(el)):
        pai.insert(pos, filho)
    pai.remove(el)


def dentro_de_propriedades(el):
    """Marca solta (w:pPr/w:rPr/w:del, w:trPr/w:ins...) em vez de embrulho de conteúdo."""
    pai = el.getparent()
    return pai is not None and nome_local(pai).endswith("Pr") and espaco(pai) == W


def paragrafo_vazio(p):
    return all(c.tag == w("pPr") for c in p if isinstance(c.tag, str))


def juntar_com_seguinte(p, contagem):
    """Aceita a exclusão da marca de parágrafo de p."""
    seguinte = p.getnext()
    while seguinte is not None and not isinstance(seguinte.tag, str):
        seguinte = seguinte.getnext()
    if seguinte is not None and seguinte.tag == w("p"):
        alvo_pos = 0
        ppr = seguinte.find(w("pPr"))
        if ppr is not None:
            alvo_pos = seguinte.index(ppr) + 1
        conteudo = [c for c in p if c.tag != w("pPr")]
        for filho in reversed(conteudo):
            seguinte.insert(alvo_pos, filho)
        p.getparent().remove(p)
        contagem["parágrafos juntados"] += 1
        return
    # Sem parágrafo logo abaixo (tabela, fim de célula, fim do corpo).
    if seguinte is not None and seguinte.tag == w("tbl") and paragrafo_vazio(p):
        p.getparent().remove(p)
        contagem["parágrafos juntados"] += 1
        return
    contagem["marcas de parágrafo sem vizinho"] += 1


def aceitar_parte(raiz, contagem):
    # 1. Mudanças de formatação: fica o estado novo, que já é o elemento pai.
    for nome in MUDANCAS_DE_PROPRIEDADE:
        for el in list(raiz.iter(w(nome))):
            tirar(el)
            contagem["mudanças de formatação"] += 1

    # 2. Marcas de intervalo (movimento, XML personalizado).
    for nome in MARCAS_DE_INTERVALO:
        for el in list(raiz.iter(w(nome))):
            tirar(el)

    # 3. Linhas e células de tabela.
    tabelas_mexidas = []
    for trpr in list(raiz.iter(w("trPr"))):
        for marca in trpr.findall(w("ins")):
            trpr.remove(marca)
            contagem["linhas inseridas"] += 1
        if trpr.find(w("del")) is not None:
            tr = trpr.getparent()
            tbl = tr.getparent() if tr is not None else None
            if tr is not None and tbl is not None:
                tbl.remove(tr)
                tabelas_mexidas.append(tbl)
                contagem["linhas excluídas"] += 1
    for tcpr in list(raiz.iter(w("tcPr"))):
        for nome in ("cellIns", "cellMerge"):
            for marca in tcpr.findall(w(nome)):
                tcpr.remove(marca)
                contagem["marcas de célula"] += 1
        if tcpr.find(w("cellDel")) is not None:
            tc = tcpr.getparent()
            if tc is not None and tc.getparent() is not None:
                tc.getparent().remove(tc)
                contagem["células excluídas"] += 1
    for tbl in tabelas_mexidas:
        if tbl.find(w("tr")) is None and tbl.getparent() is not None:
            tbl.getparent().remove(tbl)
            contagem["tabelas que ficaram vazias"] += 1

    # 4. Exclusões e origens de movimento.
    marcas_de_paragrafo = []
    for nome in ("del", "moveFrom"):
        for el in list(raiz.iter(w(nome))):
            if dentro_de_propriedades(el):
                rpr = el.getparent()
                dono = rpr.getparent()
                if rpr.tag == w("rPr") and dono is not None and dono.tag == w("pPr"):
                    p = dono.getparent()
                    if p is not None and p.tag == w("p"):
                        marcas_de_paragrafo.append(p)
                    rpr.remove(el)
                elif rpr.tag == w("rPr") and dono is not None and dono.tag == M_R:
                    if dono.getparent() is not None:
                        dono.getparent().remove(dono)
                    contagem["exclusões"] += 1
                else:
                    rpr.remove(el)
                continue
            tirar(el)
            contagem["exclusões" if nome == "del" else "movimentos"] += 1

    # 5. Inserções e destinos de movimento.
    for nome in ("ins", "moveTo"):
        for el in list(raiz.iter(w(nome))):
            if dentro_de_propriedades(el):
                el.getparent().remove(el)
                if nome == "ins":
                    contagem["marcas de inserção soltas"] += 1
                continue
            desembrulhar(el)
            if nome == "ins":
                contagem["inserções"] += 1

    # 6. Texto excluído fora de exclusão (arquivo torto): sai também.
    for nome in ("delText", "delInstrText"):
        for el in list(raiz.iter(w(nome))):
            tirar(el)
            contagem["texto excluído solto"] += 1

    # 7. Marcas de parágrafo excluídas, de baixo para cima.
    ordem = {id(p): i for i, p in enumerate(raiz.iter(w("p")))}
    unicos = {id(p): p for p in marcas_de_paragrafo}.values()
    for p in sorted(unicos, key=lambda x: ordem.get(id(x), -1), reverse=True):
        if p.getparent() is None:
            continue
        juntar_com_seguinte(p, contagem)


def sobras(raiz):
    achados = {}
    for nome in PROIBIDOS:
        n = sum(1 for _ in raiz.iter(w(nome)))
        if n:
            achados[nome] = n
    return achados


class Contagem(dict):
    def __missing__(self, chave):
        return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Aceita todas as alterações rastreadas de um .docx, direto no XML.")
    ap.add_argument("entrada", help="arquivo .docx ou pasta desempacotada")
    ap.add_argument("-o", "--saida", help="arquivo .docx de saída (obrigatório para entrada .docx)")
    ap.add_argument("--desligar-rastreio", action="store_true",
                    help="também desliga o controle de alterações nas configurações do documento")
    args = ap.parse_args(argv)

    pacote = abrir_ou_sair(args.entrada, args.saida)
    contagem = Contagem()
    restos = {}
    for nome in pacote.partes_wordml():
        raiz = pacote.xml(nome)
        aceitar_parte(raiz, contagem)
        achados = sobras(raiz)
        if achados:
            restos[nome] = achados

    if args.desligar_rastreio and pacote.existe("word/settings.xml"):
        ajustes = pacote.xml("word/settings.xml")
        for el in list(ajustes.iter(w("trackRevisions"))):
            el.getparent().remove(el)
            contagem["rastreio desligado"] += 1

    pacote.gravar(args.saida)
    destino = args.saida or args.entrada
    resumo = ", ".join("%s: %d" % (k, v) for k, v in sorted(contagem.items()) if v)
    print("Aceitei as alterações. %s" % (resumo or "Não havia alteração rastreada."))
    print("Gravado em %s" % destino)
    if restos:
        for nome, achados in restos.items():
            lista = ", ".join("w:%s (%d)" % (k, v) for k, v in achados.items())
            sys.stderr.write("Sobrou marca de alteração em %s: %s\n" % (nome, lista))
        return SAIDA_REPROVOU
    return SAIDA_OK


if __name__ == "__main__":
    sys.exit(main())
