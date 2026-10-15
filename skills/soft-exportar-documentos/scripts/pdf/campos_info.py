#!/usr/bin/env python3
"""Lista os campos preenchiveis (AcroForm) de um PDF.

Uso:
    campos_info.py ENTRADA.pdf [-o campos.json] [--dpi 72] [--so-verificar]

Sem -o, o JSON sai na tela. Com --so-verificar, so diz se o PDF tem campos
(e quantos) e sai 0 nos dois casos.

Para cada campo: nome completo (pai.filho), tipo (texto, caixa_selecao, radio,
lista_suspensa, lista, botao, assinatura), pagina, retangulo em pontos do PDF
(origem embaixo a esquerda) e em coordenadas de imagem (origem em cima a
esquerda, na escala do --dpi), opcoes validas e valor atual. O formato esta
descrito no LEIA-ME-pdf.md.

Saida: 0 ok, 2 argumento errado, 3 falta pypdf ou o arquivo.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comum as c  # noqa: E402


def descrever(campo, infos, escala):
    no = campo["no"]
    tipo = campo["tipo"]
    ff = campo["ff"]
    widgets = []
    for w, pag in campo["widgets"]:
        item = {"pagina": None if pag is None else pag + 1}
        rect = w.get("/Rect")
        if rect is not None:
            r = [float(v) for v in rect.get_object()]
            r = [min(r[0], r[2]), min(r[1], r[3]), max(r[0], r[2]), max(r[1], r[3])]
            item["retangulo_pdf"] = [c.r2(v) for v in r]
            if pag is not None:
                t = c.ret_pdf_para_topo(infos[pag], r)
                item["retangulo_imagem"] = [c.r2(v * escala) for v in t]
        if tipo in ("caixa_selecao", "radio"):
            estados = c.estados_ligados(w)
            item["valor_ligado"] = estados[0] if estados else None
            estado_atual = w.get("/AS")
            item["estado_atual"] = c.para_python(estado_atual)
        widgets.append(item)

    saida = {"nome": campo["nome"], "tipo": tipo}
    primeiro = widgets[0] if widgets else {}
    saida["pagina"] = primeiro.get("pagina")
    saida["retangulo_pdf"] = primeiro.get("retangulo_pdf")
    saida["retangulo_imagem"] = primeiro.get("retangulo_imagem")
    saida["valor"] = c.para_python(c.herdado(no, "/V"))

    if tipo == "caixa_selecao":
        ligados = [x["valor_ligado"] for x in widgets if x.get("valor_ligado")]
        saida["valor_ligado"] = ligados[0] if ligados else "Yes"
        saida["valor_desligado"] = "Off"
        if not ligados:
            saida["aviso"] = "campo sem aparencia; valor ligado presumido 'Yes'"
    elif tipo == "radio":
        opcoes = []
        for x in widgets:
            v = x.get("valor_ligado")
            if v and v not in opcoes:
                opcoes.append(v)
        saida["opcoes"] = opcoes
        saida["valor_desligado"] = "Off"
    elif tipo in ("lista", "lista_suspensa"):
        pares = c.opcoes_de_lista(no)
        saida["opcoes"] = [p[0] for p in pares]
        if any(p[0] != p[1] for p in pares):
            saida["textos_opcoes"] = [p[1] for p in pares]
        saida["multipla_escolha"] = bool(ff & c.BIT_MULTIPLA)
        if tipo == "lista_suspensa":
            saida["aceita_texto_livre"] = bool(ff & c.BIT_EDITAVEL)
    elif tipo == "texto":
        saida["multilinha"] = bool(ff & c.BIT_MULTILINHA)
        maxlen = c.herdado(no, "/MaxLen")
        if maxlen is not None:
            saida["tamanho_maximo"] = int(maxlen)

    da = c.herdado(no, "/DA")
    tam = c.tamanho_da_fonte_da(da)
    if tam is not None:
        saida["tamanho_fonte"] = tam  # 0 quer dizer tamanho automatico
    dica = c.herdado(no, "/TU")
    if dica is not None:
        saida["descricao"] = str(dica)
    saida["somente_leitura"] = bool(ff & c.BIT_SOMENTE_LEITURA)
    saida["obrigatorio"] = bool(ff & c.BIT_OBRIGATORIO)
    saida["widgets"] = widgets
    return saida


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Lista os campos preenchiveis (AcroForm) de um PDF.")
    ap.add_argument("entrada", help="arquivo PDF")
    ap.add_argument("-o", "--saida", help="grava o JSON neste arquivo (padrao: tela)")
    ap.add_argument("--dpi", type=float, default=72.0,
                    help="escala do retangulo_imagem (72 = pontos; padrao 72)")
    ap.add_argument("--so-verificar", action="store_true",
                    help="so diz se ha campos preenchiveis e sai 0")
    args = ap.parse_args(argv)
    if args.dpi <= 0:
        c.sair("--dpi precisa ser maior que zero.", c.ARGUMENTO)

    leitor = c.abrir_pdf(args.entrada)
    campos = c.listar_campos(leitor)

    if args.so_verificar:
        if campos:
            print(f"O PDF tem {len(campos)} campos preenchiveis. "
                  "Siga pelo caminho A (campos_info.py e preencher_campos.py).")
        else:
            print("O PDF nao tem campos preenchiveis. Siga pelo caminho B "
                  "(estrutura.py e preencher_texto.py).")
        return c.OK

    infos = [c.info_pagina(p) for p in leitor.pages]
    escala = args.dpi / 72.0
    paginas = []
    for i, inf in enumerate(infos):
        w, h = c.tamanho_exibido(inf)
        paginas.append({"pagina": i + 1, "largura": c.r2(w), "altura": c.r2(h),
                        "giro": inf["giro"]})
    dados = {
        "arquivo": os.path.basename(args.entrada),
        "tem_campos": bool(campos),
        "dpi_imagem": args.dpi,
        "paginas": paginas,
        "campos": [descrever(cp, infos, escala) for cp in campos],
    }
    c.gravar_json(dados, args.saida)
    if args.saida:
        print(f"{len(campos)} campos gravados em {args.saida}", file=sys.stderr)
    return c.OK


if __name__ == "__main__":
    sys.exit(main())
