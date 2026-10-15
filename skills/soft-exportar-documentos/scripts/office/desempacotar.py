#!/usr/bin/env python3
"""Desempacota um .docx, .pptx ou .xlsx numa pasta, com o XML recuado para editar à mão.

Uso:
    python3 desempacotar.py ARQUIVO.(docx|pptx|xlsx) PASTA [--sem-recuo]

O que faz:
- confere o zip antes de extrair qualquer coisa e recusa o arquivo inteiro se
  achar caminho perigoso (absoluto, com "..", barra invertida), link simbólico,
  entrada criptografada, nome repetido ou tamanho descompactado absurdo;
- grava cada parte dentro de PASTA (que precisa não existir ou estar vazia);
- reformata .xml e .rels com recuo de dois espaços, sem tocar no texto: elemento
  folha, xml:space="preserve" e conteúdo misto ficam como estavam;
- parte XML que não abre como XML é gravada como veio, com aviso.

Depois de editar, recompacte com empacotar.py, que tira o recuo de volta.

Saída: 0 tudo certo, 1 zip recusado, 2 argumento errado, 3 arquivo ou
dependência faltando.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import comum  # noqa: E402


def desempacotar(arquivo, pasta, recuo=True):
    """Extrai e recua. Devolve (contagem, avisos). Levanta ValueError se o zip for recusado."""
    comum.exigir_lxml()
    zf, motivo = comum.abrir_zip(arquivo)
    if zf is None:
        raise ValueError(motivo)
    with zf:
        problemas = comum.problemas_do_zip(zf)
        if problemas:
            raise ValueError("zip recusado:\n  - " + "\n  - ".join(problemas))
        raiz = os.path.realpath(pasta)
        os.makedirs(raiz, exist_ok=True)
        avisos = []
        contagem = {"partes": 0, "recuadas": 0}
        for info in zf.infolist():
            destino = os.path.realpath(os.path.join(raiz, *info.filename.rstrip("/").split("/")))
            if os.path.commonpath([raiz, destino]) != raiz or destino == raiz:
                raise ValueError("entrada %r sairia da pasta de destino" % info.filename)
            if info.is_dir():
                os.makedirs(destino, exist_ok=True)
                continue
            dados = zf.read(info)
            if recuo and comum.eh_arquivo_xml(info.filename):
                try:
                    arvore = comum.ler_xml(dados)
                    comum.recuar(arvore.getroot())
                    dados = comum.gravar_xml(arvore, dados)
                    contagem["recuadas"] += 1
                except comum.etree.XMLSyntaxError as erro:
                    avisos.append("%s não é XML bem formado, gravado como veio (%s)" % (info.filename, erro))
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            with open(destino, "xb") as saida:
                saida.write(dados)
            contagem["partes"] += 1
    return contagem, avisos


def main(argv=None):
    leitor = argparse.ArgumentParser(
        description="Desempacota docx, pptx ou xlsx numa pasta, com XML recuado.")
    leitor.add_argument("arquivo", help="o .docx, .pptx ou .xlsx")
    leitor.add_argument("pasta", help="pasta de destino (não pode ter nada dentro)")
    leitor.add_argument("--sem-recuo", action="store_true",
                        help="extrai sem reformatar o XML")
    args = leitor.parse_args(argv)

    if not os.path.isfile(args.arquivo):
        print("arquivo não encontrado: %s" % args.arquivo, file=sys.stderr)
        return comum.SAIDA_FALTA
    if os.path.exists(args.pasta):
        if not os.path.isdir(args.pasta):
            print("o destino existe e não é pasta: %s" % args.pasta, file=sys.stderr)
            return comum.SAIDA_ARGUMENTO
        if os.listdir(args.pasta):
            print("a pasta de destino já tem conteúdo, escolha uma vazia: %s" % args.pasta, file=sys.stderr)
            return comum.SAIDA_ARGUMENTO
    try:
        contagem, avisos = desempacotar(args.arquivo, args.pasta, recuo=not args.sem_recuo)
    except ValueError as erro:
        print("não desempacotei %s: %s" % (args.arquivo, erro), file=sys.stderr)
        return comum.SAIDA_REPROVOU
    except OSError as erro:
        print("não desempacotei %s: erro ao gravar (%s); a pasta pode ter ficado pela metade"
              % (args.arquivo, erro), file=sys.stderr)
        return comum.SAIDA_REPROVOU
    for aviso in avisos:
        print("aviso: %s" % aviso)
    print("desempacotado em %s: %d partes, %d com XML recuado" % (
        args.pasta, contagem["partes"], contagem["recuadas"]))
    return comum.SAIDA_OK


if __name__ == "__main__":
    sys.exit(main())
