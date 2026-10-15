#!/usr/bin/env python3
"""Preenche os campos (AcroForm) de um PDF a partir de um valores.json.

Uso:
    preencher_campos.py ENTRADA.pdf valores.json SAIDA.pdf [--parcial]

valores.json pode ser um objeto simples {"nome.do.campo": valor} ou uma
lista de objetos {"nome": ..., "valor": ..., "descricao": ..., "pagina": ...}
(tambem aceito dentro de {"campos": [...]}). Veja o LEIA-ME-pdf.md.

Antes de gravar, confere cada campo:
  texto           qualquer texto (respeita o tamanho maximo do campo)
  caixa_selecao   o valor ligado do proprio campo (ou true), "Off" (ou false)
  radio           uma das opcoes do grupo, ou "Off"
  lista_suspensa  uma das opcoes (aceita o texto exibido; texto livre so se
                  o campo permitir)
  lista           uma opcao, ou uma lista delas se o campo aceitar varias
Campo de botao, de assinatura e somente leitura nao se preenche.

Se houver campo nao encontrado ou valor recusado, nada e gravado e a saida e 1.
Com --parcial, grava os campos certos mesmo assim (saida continua 1).
Os campos ganham aparencia nova e o formulario fica com NeedAppearances
ligado, para o leitor de PDF redesenhar o que precisar.

Saida: 0 tudo preenchido, 1 algum campo com problema, 2 argumento errado,
3 falta pypdf ou arquivo.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comum as c  # noqa: E402


def ler_valores(dados):
    """Normaliza os formatos aceitos em lista de (nome, valor)."""
    if isinstance(dados, dict) and isinstance(dados.get("campos"), list):
        dados = dados["campos"]
    if isinstance(dados, dict):
        return list(dados.items()), []
    if isinstance(dados, list):
        pares, erros = [], []
        for i, item in enumerate(dados):
            if not isinstance(item, dict) or "nome" not in item or "valor" not in item:
                erros.append(f"item {i + 1}: precisa de 'nome' e 'valor'")
                continue
            pares.append((str(item["nome"]), item["valor"]))
        return pares, erros
    return [], ["valores.json precisa ser um objeto {nome: valor} ou uma lista"]


def _sem_barra(v):
    return v[1:] if isinstance(v, str) and v.startswith("/") else v


def validar(campo, valor):
    """Devolve (valor_normalizado, erro). erro None quando o valor serve."""
    tipo, ff, no = campo["tipo"], campo["ff"], campo["no"]
    if tipo in ("botao", "assinatura", "desconhecido"):
        return None, f"campo do tipo {tipo} nao se preenche por aqui"
    if ff & c.BIT_SOMENTE_LEITURA:
        return None, "campo somente leitura"

    if tipo == "texto":
        if isinstance(valor, bool) or not isinstance(valor, (str, int, float)):
            return None, "campo de texto pede texto ou numero"
        s = str(valor)
        maxlen = c.herdado(no, "/MaxLen")
        if maxlen is not None and len(s) > int(maxlen):
            return None, f"texto com {len(s)} caracteres; o campo aceita {int(maxlen)}"
        return s, None

    if tipo == "caixa_selecao":
        ligados = []
        for w, _ in campo["widgets"]:
            for e in c.estados_ligados(w):
                if e not in ligados:
                    ligados.append(e)
        if not ligados:
            ligados = ["Yes"]
        if valor is True:
            return ligados[0], None
        if valor is False or valor is None or _sem_barra(valor) == "Off":
            return "Off", None
        if _sem_barra(valor) in ligados:
            return _sem_barra(valor), None
        return None, (f"caixa de selecao aceita {ligados[0]!r} (ligada) ou 'Off'; "
                      f"recebeu {valor!r}")

    if tipo == "radio":
        opcoes = []
        for w, _ in campo["widgets"]:
            for e in c.estados_ligados(w):
                if e not in opcoes:
                    opcoes.append(e)
        if valor is None or _sem_barra(valor) == "Off":
            return "Off", None
        if _sem_barra(valor) in opcoes:
            return _sem_barra(valor), None
        return None, f"opcao {valor!r} nao existe; opcoes validas: {opcoes}"

    if tipo in ("lista", "lista_suspensa"):
        pares = c.opcoes_de_lista(no)
        exportados = [p[0] for p in pares]
        exibidos = {p[1]: p[0] for p in pares}

        def um(v):
            if not isinstance(v, (str, int, float)) or isinstance(v, bool):
                return None
            v = str(v)
            if v in exportados:
                return v
            if v in exibidos:
                return exibidos[v]
            if tipo == "lista_suspensa" and ff & c.BIT_EDITAVEL:
                return v
            return None

        if isinstance(valor, list):
            if tipo == "lista_suspensa" or not ff & c.BIT_MULTIPLA:
                return None, "este campo aceita uma opcao so, nao uma lista"
            saida = []
            for v in valor:
                n = um(v)
                if n is None:
                    return None, f"opcao {v!r} nao existe; opcoes validas: {exportados}"
                saida.append(n)
            return saida, None
        n = um(valor)
        if n is None:
            return None, f"opcao {valor!r} nao existe; opcoes validas: {exportados}"
        return n, None
    return None, f"tipo {tipo} desconhecido"


def cor_da(da):
    """Cor de preenchimento do texto lida do /DA (padrao preto)."""
    s = str(da or "")
    m = re.search(r"([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+rg", s)
    if m:
        return tuple(float(x) for x in m.groups())
    m = re.search(r"([\d.]+)\s+g(?:\s|$)", s)
    if m:
        g = float(m.group(1))
        return (g, g, g)
    return (0.0, 0.0, 0.0)


def fluxo_form(escritor, conteudo, largura, altura):
    from pypdf.generic import (ArrayObject, DecodedStreamObject, DictionaryObject,
                               FloatObject, NameObject)
    s = DecodedStreamObject()
    s.set_data(conteudo)
    s.update({
        NameObject("/Type"): NameObject("/XObject"),
        NameObject("/Subtype"): NameObject("/Form"),
        NameObject("/BBox"): ArrayObject([FloatObject(0), FloatObject(0),
                                          FloatObject(round(largura, 3)),
                                          FloatObject(round(altura, 3))]),
        NameObject("/Resources"): DictionaryObject({
            NameObject("/Font"): DictionaryObject({
                NameObject("/F1"): c.fonte_helvetica(escritor)})}),
    })
    return escritor._add_object(s)


def medida_widget(w):
    r = [float(v) for v in w["/Rect"].get_object()]
    return abs(r[2] - r[0]), abs(r[3] - r[1])


def aparencia_texto(escritor, campo, w, texto, medidor):
    """Desenha o texto dentro do widget (texto ou lista suspensa)."""
    from pypdf.generic import DictionaryObject, NameObject
    if "/Rect" not in w:
        return []
    largura, altura = medida_widget(w)
    da = c.herdado(campo["no"], "/DA")
    tam = c.tamanho_da_fonte_da(da)
    multilinha = bool(campo["ff"] & c.BIT_MULTILINHA)
    if not tam:  # tamanho automatico
        tam, linhas, _ = c.encaixar(texto, largura, altura, 12, 4, medidor)
    elif multilinha:
        linhas = c.quebrar_linhas(texto, max(largura - 2 * c.FOLGA, 1), tam, medidor)
    else:
        linhas = [texto.replace("\n", " ")]
    if not multilinha:
        linhas = [" ".join(linhas)]
    q = int(c.herdado(campo["no"], "/Q") or 0)
    alin = {1: "centro", 2: "direita"}.get(q, "esquerda")
    corpo, trocados = c.conteudo_texto(linhas, tam, largura, altura, medidor,
                                       cor_da(da), alin, centralizar_uma_linha=not multilinha)
    conteudo = b"/Tx BMC\n" + corpo + b"\nEMC"
    w[NameObject("/AP")] = DictionaryObject({NameObject("/N"): fluxo_form(escritor, conteudo, largura, altura)})
    return trocados


def aparencia_lista(escritor, campo, w, escolhidos, medidor):
    """Desenha a caixa de lista com as opcoes escolhidas realcadas."""
    from pypdf.generic import DictionaryObject, NameObject
    if "/Rect" not in w:
        return []
    largura, altura = medida_widget(w)
    da = c.herdado(campo["no"], "/DA")
    tam = c.tamanho_da_fonte_da(da) or 10
    entre = tam * c.ALTURA_LINHA
    pares = c.opcoes_de_lista(campo["no"])
    partes = [b"/Tx BMC", b"q", b"0 0 %.2f %.2f re W n" % (largura, altura)]
    y = altura - c.FOLGA
    for exp, _ in pares:
        if exp in escolhidos:
            partes.append(b"0.60 0.75 0.90 rg 0 %.2f %.2f %.2f re f" % (y - entre, largura, entre))
        y -= entre
    trocados = []
    y = altura - c.FOLGA
    partes += [b"BT", b"/F1 %.2f Tf" % tam, b"%.3f %.3f %.3f rg" % cor_da(da)]
    for _, texto in pares:
        lit, tr = c.literal_pdf(texto)
        trocados += tr
        partes.append(b"1 0 0 1 %.2f %.2f Tm %s Tj" % (c.FOLGA + 1, y - tam * 0.95, lit))
        y -= entre
    partes += [b"ET", b"Q", b"EMC"]
    w[NameObject("/AP")] = DictionaryObject({NameObject("/N"): fluxo_form(escritor, b"\n".join(partes), largura, altura)})
    return trocados


def aplicar(escritor, campo, valor, medidor):
    from pypdf.generic import ArrayObject, NameObject, NumberObject, TextStringObject
    no, tipo = campo["no"], campo["tipo"]
    trocados = []
    if tipo == "texto":
        no[NameObject("/V")] = TextStringObject(valor)
        for w, _ in campo["widgets"]:
            trocados += aparencia_texto(escritor, campo, w, valor, medidor)
    elif tipo in ("caixa_selecao", "radio"):
        nome = NameObject("/" + valor)
        no[NameObject("/V")] = nome
        for w, _ in campo["widgets"]:
            estado = nome if valor in c.estados_ligados(w) else NameObject("/Off")
            w[NameObject("/AS")] = estado
    elif tipo == "lista_suspensa":
        no[NameObject("/V")] = TextStringObject(valor)
        if "/I" in no:
            del no["/I"]
        exibido = {p[0]: p[1] for p in c.opcoes_de_lista(no)}.get(valor, valor)
        for w, _ in campo["widgets"]:
            trocados += aparencia_texto(escritor, campo, w, exibido, medidor)
    elif tipo == "lista":
        lista = valor if isinstance(valor, list) else [valor]
        if isinstance(valor, list):
            no[NameObject("/V")] = ArrayObject([TextStringObject(v) for v in valor])
        else:
            no[NameObject("/V")] = TextStringObject(valor)
        exportados = [p[0] for p in c.opcoes_de_lista(no)]
        indices = sorted(exportados.index(v) for v in lista if v in exportados)
        no[NameObject("/I")] = ArrayObject([NumberObject(i) for i in indices])
        for w, _ in campo["widgets"]:
            trocados += aparencia_lista(escritor, campo, w, lista, medidor)
    return trocados


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Preenche campos de formulario de um PDF a partir de um JSON.")
    ap.add_argument("entrada", help="PDF com campos")
    ap.add_argument("valores", help="valores.json (nome do campo para valor)")
    ap.add_argument("saida", help="PDF de saida")
    ap.add_argument("--parcial", action="store_true",
                    help="grava os campos certos mesmo com problema em outros")
    args = ap.parse_args(argv)

    pypdf = c.exigir_pypdf()
    from pypdf.generic import BooleanObject, NameObject
    leitor = c.abrir_pdf(args.entrada)
    pares, erros_formato = ler_valores(c.ler_json(args.valores))
    if erros_formato:
        c.sair("valores.json com problema:\n  " + "\n  ".join(erros_formato), c.ARGUMENTO)

    escritor = pypdf.PdfWriter(clone_from=leitor)
    campos = {cp["nome"]: cp for cp in c.listar_campos(escritor)}
    if not campos:
        c.sair("O PDF nao tem campos preenchiveis. Use estrutura.py e "
               "preencher_texto.py (formulario chapado).", c.REPROVOU)

    nao_achados, recusados, prontos = [], [], []
    for nome, valor in pares:
        campo = campos.get(nome)
        if campo is None:
            nao_achados.append(nome)
            continue
        normal, erro = validar(campo, valor)
        if erro:
            recusados.append((nome, erro))
        else:
            prontos.append((campo, normal))

    problema = bool(nao_achados or recusados)
    for nome in nao_achados:
        print(f"Campo nao encontrado: {nome}")
    for nome, erro in recusados:
        print(f"Valor recusado em {nome}: {erro}")
    if nao_achados:
        print("Campos que existem: " + ", ".join(sorted(campos)))
    if problema and not args.parcial:
        print("Nada foi gravado. Corrija o valores.json e rode de novo "
              "(ou use --parcial).")
        return c.REPROVOU

    medidor = c.Medidor()
    trocados = []
    for campo, valor in prontos:
        trocados += aplicar(escritor, campo, valor, medidor)
    acro = escritor.root_object["/AcroForm"].get_object()
    acro[NameObject("/NeedAppearances")] = BooleanObject(True)
    try:
        with open(args.saida, "wb") as f:
            escritor.write(f)
    except OSError as e:
        c.sair(f"Nao consegui gravar {args.saida}: {e}", c.DEPENDENCIA)

    preenchidos = {cp["nome"] for cp, _ in prontos}
    vazios = sorted(n for n in campos if n not in preenchidos
                    and campos[n]["tipo"] not in ("botao", "assinatura"))
    print(f"{len(prontos)} campos preenchidos em {args.saida}.")
    if vazios:
        print("Ficaram sem valor neste preenchimento: " + ", ".join(vazios))
    if trocados:
        print("Aviso: caracteres sem desenho na fonte padrao viraram '?' na aparencia "
              "(o valor do campo ficou certo): " + "".join(sorted(set(trocados))))
    return c.REPROVOU if problema else c.OK


if __name__ == "__main__":
    sys.exit(main())
