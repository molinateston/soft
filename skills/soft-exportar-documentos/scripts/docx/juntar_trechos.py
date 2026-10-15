#!/usr/bin/env python3
"""Junta trechos (runs) vizinhos do Word que têm a mesma formatação.

O Word parte o texto em muitos pedaços (marcas de revisão, correção
ortográfica), e uma frase que aparece inteira na tela quase nunca existe
contígua no XML. Este script junta os pedaços vizinhos de formatação
idêntica, sem mudar uma letra do texto nem a aparência.

Uso:
    python3 juntar_trechos.py ENTRADA.docx -o SAIDA.docx
    python3 juntar_trechos.py PASTA_DESEMPACOTADA            (edita no lugar)
    python3 juntar_trechos.py PASTA_DESEMPACOTADA -o SAIDA.docx

O que conta como mesma formatação: as propriedades do trecho (w:rPr) iguais
depois de ignorar os atributos de ruído de revisão (rsid*) e a ordem dos
filhos. Nunca junta através de comentário, marcador, alteração rastreada,
campo, nota, quebra, desenho ou símbolo: só pedaços irmãos diretos, cujo
conteúdo é apenas texto, tabulação ou hífen.

Por padrão remove as marcas de verificação ortográfica (w:proofErr), que
não aparecem no documento e só atrapalham a junção. Use
--manter-ortografia para mantê-las.

Vale para o corpo, cabeçalhos, rodapés, notas e comentários.

Saída: 0 feito, 2 argumento errado, 3 arquivo faltando ou ilegível.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comum_docx import (  # noqa: E402
    W, XML_SPACE, SAIDA_OK, abrir_ou_sair, w, nome_local, espaco,
)

# Conteúdo de trecho que pode ser juntado sem mudar o sentido.
CONTEUDO_JUNTAVEL = {"t", "delText", "tab", "noBreakHyphen", "softHyphen", "lastRenderedPageBreak"}
TEXTO = {"t", "delText"}


def eh_ruido(nome_qualificado):
    """Atributos de identificação de sessão de edição (rsid*), que não mudam nada visível."""
    if not nome_qualificado.startswith("{%s}" % W):
        return False
    return nome_qualificado.split("}", 1)[1].startswith("rsid")


def canonico(el):
    """Assinatura estável de um elemento, sem rsid e sem espaço em branco."""
    attrs = sorted((k, v) for k, v in el.attrib.items() if not eh_ruido(k))
    filhos = "".join(canonico(c) for c in el if isinstance(c.tag, str))
    return "<%s %r>%s</>" % (el.tag, attrs, filhos)


def chave_formatacao(run):
    """Formatação normalizada do trecho, ou None se o trecho não pode ser juntado."""
    rpr = None
    for filho in run:
        if not isinstance(filho.tag, str):
            return None
        if filho.tag == w("rPr"):
            if rpr is not None:
                return None
            rpr = filho
            continue
        if espaco(filho) != W or nome_local(filho) not in CONTEUDO_JUNTAVEL:
            return None
    attrs_run = tuple(sorted((k, v) for k, v in run.attrib.items() if not eh_ruido(k)))
    if rpr is None:
        return (attrs_run, ())
    if rpr.find(w("rPrChange")) is not None:
        return None  # mudança de formatação rastreada: não mexe
    filhos = tuple(sorted(canonico(c) for c in rpr if isinstance(c.tag, str)))
    attrs_rpr = tuple(sorted((k, v) for k, v in rpr.attrib.items() if not eh_ruido(k)))
    return (attrs_run, attrs_rpr, filhos)


def texto_ambiguo(t):
    """w:t sem xml:space='preserve' com espaço na ponta: o Word descarta esse espaço.
    Juntar mudaria o que aparece na tela, então esse trecho fica como está."""
    if t.get(XML_SPACE) == "preserve":
        return False
    texto = t.text or ""
    return texto != texto.strip()


def tem_texto_ambiguo(run):
    return any(nome_local(c) in TEXTO and texto_ambiguo(c) for c in run)


def precisa_preservar(texto):
    return texto != texto.strip() or "  " in texto or "\t" in texto or "\n" in texto


def compactar_textos(run):
    """Funde w:t consecutivos dentro do mesmo trecho."""
    anterior = None
    for filho in list(run):
        nome = nome_local(filho) if espaco(filho) == W else ""
        if nome in TEXTO and anterior is not None and anterior.tag == filho.tag:
            preservar = anterior.get(XML_SPACE) == "preserve" or filho.get(XML_SPACE) == "preserve"
            anterior.text = (anterior.text or "") + (filho.text or "")
            if preservar or precisa_preservar(anterior.text):
                anterior.set(XML_SPACE, "preserve")
            run.remove(filho)
            continue
        anterior = filho if nome in TEXTO else None


def absorver(destino, origem):
    for filho in list(origem):
        if filho.tag == w("rPr"):
            continue
        filho.tail = None
        destino.append(filho)
    compactar_textos(destino)


def juntar_irmaos(pai):
    juntados = 0
    anterior = None
    chave_anterior = None
    for el in list(pai):
        if el.tag != w("r"):
            anterior = None
            continue
        chave = chave_formatacao(el)
        if chave is None or tem_texto_ambiguo(el):
            anterior = None
            continue
        if anterior is not None and chave == chave_anterior:
            absorver(anterior, el)
            pai.remove(el)
            juntados += 1
            continue
        anterior, chave_anterior = el, chave
    return juntados


def juntar_parte(raiz, tirar_ortografia=True):
    removidas = 0
    if tirar_ortografia:
        for marca in list(raiz.iter(w("proofErr"))):
            pai = marca.getparent()
            if pai is not None:
                pai.remove(marca)
                removidas += 1
    pais = []
    vistos = set()
    for run in raiz.iter(w("r")):
        pai = run.getparent()
        if pai is not None and id(pai) not in vistos:
            vistos.add(id(pai))
            pais.append(pai)
    juntados = sum(juntar_irmaos(pai) for pai in pais)
    return juntados, removidas


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Junta trechos vizinhos do Word com a mesma formatação, sem mudar o texto.")
    ap.add_argument("entrada", help="arquivo .docx ou pasta desempacotada")
    ap.add_argument("-o", "--saida", help="arquivo .docx de saída (obrigatório para entrada .docx)")
    ap.add_argument("--manter-ortografia", action="store_true",
                    help="não remove as marcas de verificação ortográfica (w:proofErr)")
    args = ap.parse_args(argv)

    pacote = abrir_ou_sair(args.entrada, args.saida)
    total_juntados = total_marcas = 0
    for nome in pacote.partes_wordml():
        juntados, marcas = juntar_parte(pacote.xml(nome), not args.manter_ortografia)
        total_juntados += juntados
        total_marcas += marcas
    pacote.gravar(args.saida)
    destino = args.saida or args.entrada
    print("Juntei %d trechos. Removi %d marcas de ortografia. Gravado em %s"
          % (total_juntados, total_marcas, destino))
    return SAIDA_OK


if __name__ == "__main__":
    sys.exit(main())
