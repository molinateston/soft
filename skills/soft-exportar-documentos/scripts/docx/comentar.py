#!/usr/bin/env python3
"""Cria um comentário de verdade do Word, ancorado num trecho exato do texto.

Escreve o comentário em word/comments.xml, o registro de encadeamento em
word/commentsExtended.xml e o identificador durável em word/commentsIds.xml,
liga as três partes ao documento e declara os tipos de conteúdo. No corpo,
põe o início e o fim do intervalo comentado em volta do trecho e a
referência logo depois, dividindo os trechos (runs) quando o texto
procurado começa ou termina no meio de um deles. A formatação é mantida.

Uso:
    python3 comentar.py ENTRADA.docx --trecho "texto exato" --texto "comentário" -o SAIDA.docx
    python3 comentar.py ENTRADA.docx --trecho "prazo" --ocorrencia 2 --texto "..." -o SAIDA.docx
    python3 comentar.py ENTRADA.docx --resposta-a 0 --texto "Combinado" -o SAIDA.docx
    python3 comentar.py PASTA_DESEMPACOTADA --trecho "..." --texto "..."   (edita no lugar)

Opções:
    --autor NOME      autor do comentário (padrão: variável DOC_AUTOR ou "Revisor")
    --iniciais XX     iniciais (padrão: tiradas do autor)
    --resposta-a ID   cria resposta encadeada ao comentário ID; sem --trecho,
                      usa o mesmo intervalo do comentário original
    --ocorrencia N    quando o trecho aparece mais de uma vez, escolhe a N-ésima (a partir de 1)

O trecho é procurado no corpo do documento, dentro de um parágrafo (pode
atravessar trechos com formatações diferentes), fora de texto excluído.
Uma quebra de linha no --texto vira um novo parágrafo do comentário.

Imprime o número do comentário criado (use em --resposta-a).

Saída: 0 feito, 1 trecho não achado, ambíguo ou comentário-pai inexistente,
2 argumento errado, 3 arquivo faltando ou ilegível.
"""

import argparse
import copy
import datetime
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comum_docx import (  # noqa: E402
    NS, W, XML_SPACE, SAIDA_OK, SAIDA_REPROVOU,
    abrir_ou_sair, falhar, w, qn, nome_local, espaco, etree,
)

DOCUMENTO = "word/document.xml"
REL_COMENTARIOS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"
REL_ESTENDIDO = "http://schemas.microsoft.com/office/2011/relationships/commentsExtended"
REL_IDS = "http://schemas.microsoft.com/office/2016/09/relationships/commentsIds"
TIPO_COMENTARIOS = "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"
TIPO_ESTENDIDO = "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtended+xml"
TIPO_IDS = "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsIds+xml"
MC_IGNORAVEL = "{%s}Ignorable" % NS["mc"]

# Caracteres que cada filho de um trecho representa no texto lido.
def texto_do_filho(filho):
    if espaco(filho) != W:
        return ""
    nome = nome_local(filho)
    if nome == "t":
        return filho.text or ""
    if nome == "tab":
        return "\t"
    if nome in ("br", "cr"):
        return "\n"
    if nome == "noBreakHyphen":
        return "-"
    return ""


# ---------------------------------------------------------------- busca

def trechos_do_paragrafo(p):
    """Trechos (w:r) que pertencem a este parágrafo, fora de texto excluído."""
    saida = []
    for r in p.iter(w("r")):
        dono = next(r.iterancestors(w("p")), None)
        if dono is not p:
            continue
        if any(a.tag in (w("del"), w("moveFrom")) for a in r.iterancestors()):
            continue
        saida.append(r)
    return saida


def mapa_do_paragrafo(p):
    """Texto do parágrafo e, para cada trecho, a faixa [inicio, fim) que ele ocupa."""
    partes = []
    faixas = []
    pos = 0
    for r in trechos_do_paragrafo(p):
        ini = pos
        for filho in r:
            pedaco = texto_do_filho(filho)
            partes.append(pedaco)
            pos += len(pedaco)
        faixas.append((r, ini, pos))
    return "".join(partes), faixas


def paragrafos_do_corpo(raiz):
    for p in raiz.iter(w("p")):
        if any(nome_local(a) == "Fallback" and espaco(a) == NS["mc"] for a in p.iterancestors()):
            continue  # cópia de compatibilidade de caixa de texto: já contada no Choice
        yield p


def achar_ocorrencias(raiz, trecho):
    achados = []
    for numero, p in enumerate(paragrafos_do_corpo(raiz), start=1):
        texto, _ = mapa_do_paragrafo(p)
        inicio = texto.find(trecho)
        while inicio != -1:
            achados.append((p, numero, inicio, texto))
            inicio = texto.find(trecho, inicio + len(trecho))
    return achados


# ---------------------------------------------------------------- divisão

def dividir_trecho(r, corte):
    """Divide o trecho r no caractere 'corte'. Devolve o novo trecho da direita."""
    rpr = r.find(w("rPr"))
    direita = etree.Element(r.tag, attrib=dict(r.attrib))
    if rpr is not None:
        direita.append(copy.deepcopy(rpr))
    pos = 0
    mover = []
    for filho in list(r):
        if filho.tag == w("rPr"):
            continue
        pedaco = texto_do_filho(filho)
        fim = pos + len(pedaco)
        if fim <= corte and not (len(pedaco) == 0 and pos == corte):
            pos = fim
            continue
        if pos < corte < fim:
            # w:t atravessa o corte: parte o texto em dois.
            novo = copy.deepcopy(filho)
            novo.tail = None
            esquerda_txt = pedaco[: corte - pos]
            direita_txt = pedaco[corte - pos:]
            filho.text = esquerda_txt
            novo.text = direita_txt
            for t in (filho, novo):
                if t.text != t.text.strip():
                    t.set(XML_SPACE, "preserve")
            mover.append(("novo", novo))
        else:
            mover.append(("mover", filho))
        pos = fim
    for tipo, el in mover:
        if tipo == "mover":
            r.remove(el)
            el.tail = None
        direita.append(el)
    pai = r.getparent()
    pai.insert(pai.index(r) + 1, direita)
    direita.tail = r.tail
    r.tail = None
    return direita


def isolar(p, inicio, fim):
    """Garante bordas de trecho em inicio e fim. Devolve (primeiro, último) trecho do intervalo."""
    _, faixas = mapa_do_paragrafo(p)
    for r, a, b in faixas:
        if a < fim < b:
            dividir_trecho(r, fim - a)
            break
    _, faixas = mapa_do_paragrafo(p)
    for r, a, b in faixas:
        if a < inicio < b:
            dividir_trecho(r, inicio - a)
            break
    _, faixas = mapa_do_paragrafo(p)
    dentro = [r for r, a, b in faixas if a >= inicio and b <= fim and b > a]
    return dentro[0], dentro[-1]


# ---------------------------------------------------------------- comentários

def estilo_existe(pacote, estilo_id):
    if not pacote.existe("word/styles.xml"):
        return False
    for st in pacote.xml("word/styles.xml").iter(w("style")):
        if st.get(w("styleId")) == estilo_id:
            return True
    return False


def todos_os_ids(pacote, partes):
    usados = {-1}
    for nome in partes:
        if not pacote.existe(nome):
            continue
        for el in pacote.xml(nome).iter():
            valor = el.get(w("id")) if isinstance(el.tag, str) else None
            if valor is not None and valor.lstrip("-").isdigit():
                usados.add(int(valor))
    return usados


def todos_os_para_ids(pacote):
    usados = set()
    for nome in pacote.partes_wordml():
        for el in pacote.xml(nome).iter():
            if isinstance(el.tag, str):
                valor = el.get(qn("w14:paraId"))
                if valor:
                    usados.add(valor.upper())
    for nome in ("word/commentsExtended.xml", "word/commentsIds.xml"):
        if pacote.existe(nome):
            for el in pacote.xml(nome).iter():
                if isinstance(el.tag, str):
                    for k, v in el.attrib.items():
                        if k.endswith("}paraId"):
                            usados.add(v.upper())
    return usados


def novo_hex(usados, sorteio):
    while True:
        valor = "%08X" % sorteio.randint(1, 0x7FFFFFFE)
        if valor not in usados:
            usados.add(valor)
            return valor


def garantir_ignoravel(raiz, prefixos):
    atual = (raiz.get(MC_IGNORAVEL) or "").split()
    for prefixo in prefixos:
        if prefixo not in atual and raiz.nsmap.get(prefixo) == NS[prefixo]:
            atual.append(prefixo)
    if atual:
        raiz.set(MC_IGNORAVEL, " ".join(atual))


def com_prefixos(pacote, nome, raiz, prefixos):
    """Garante os prefixos declarados na raiz (lxml não muda nsmap no lugar: refaz a raiz)."""
    faltam = [x for x in prefixos if raiz.nsmap.get(x) != NS[x]]
    if not faltam:
        return raiz
    mapa = dict(raiz.nsmap)
    for x in faltam:
        if x in mapa:  # prefixo usado para outra coisa: deixa o lxml escolher
            continue
        mapa[x] = NS[x]
    nova = etree.Element(raiz.tag, attrib=dict(raiz.attrib), nsmap=mapa)
    nova.text = raiz.text
    for filho in list(raiz):
        nova.append(filho)
    pacote.novo_xml(nome, nova)
    return nova


def parte_de_comentarios(pacote):
    nome = pacote.alvo_por_tipo(DOCUMENTO, REL_COMENTARIOS)
    if nome and pacote.existe(nome):
        raiz = com_prefixos(pacote, nome, pacote.xml(nome), ["w14", "mc"])
        garantir_ignoravel(raiz, ["w14"])
        return nome, raiz
    nome = "word/comments.xml"
    if pacote.existe(nome):
        raiz = com_prefixos(pacote, nome, pacote.xml(nome), ["w14", "mc"])
        garantir_ignoravel(raiz, ["w14"])
    else:
        raiz = etree.Element(w("comments"), nsmap={
            "w": W, "w14": NS["w14"], "mc": NS["mc"], "r": NS["r"]})
        garantir_ignoravel(raiz, ["w14"])
        pacote.novo_xml(nome, raiz)
    pacote.ligar(DOCUMENTO, REL_COMENTARIOS, "comments.xml")
    pacote.declarar_tipo(nome, TIPO_COMENTARIOS)
    return nome, raiz


def parte_auxiliar(pacote, rel, tipo_ct, arquivo, raiz_tag, prefixo):
    nome = pacote.alvo_por_tipo(DOCUMENTO, rel)
    if nome and pacote.existe(nome):
        return pacote.xml(nome)
    nome = "word/" + arquivo
    if pacote.existe(nome):
        raiz = pacote.xml(nome)
    else:
        raiz = etree.Element(qn(prefixo + ":" + raiz_tag), nsmap={
            prefixo: NS[prefixo], "mc": NS["mc"], "w": W})
        garantir_ignoravel(raiz, [prefixo])
        pacote.novo_xml(nome, raiz)
    pacote.ligar(DOCUMENTO, rel, arquivo)
    pacote.declarar_tipo(nome, tipo_ct)
    return raiz


def montar_comentario(id_novo, autor, iniciais, data, texto, para_ids, usar_estilos):
    com = etree.Element(w("comment"))
    com.set(w("id"), str(id_novo))
    com.set(w("author"), autor)
    com.set(w("date"), data)
    if iniciais:
        com.set(w("initials"), iniciais)
    linhas = texto.split("\n")
    for i, linha in enumerate(linhas):
        p = etree.SubElement(com, w("p"))
        p.set(qn("w14:paraId"), para_ids[i])
        p.set(qn("w14:textId"), "77777777")
        if usar_estilos[0]:
            ppr = etree.SubElement(p, w("pPr"))
            etree.SubElement(ppr, w("pStyle")).set(w("val"), usar_estilos[0])
        if i == 0:
            r = etree.SubElement(p, w("r"))
            if usar_estilos[1]:
                rpr = etree.SubElement(r, w("rPr"))
                etree.SubElement(rpr, w("rStyle")).set(w("val"), usar_estilos[1])
            etree.SubElement(r, w("annotationRef"))
        if linha:
            r = etree.SubElement(p, w("r"))
            t = etree.SubElement(r, w("t"))
            t.text = linha
            t.set(XML_SPACE, "preserve")
    return com


def trecho_de_referencia(id_novo, estilo_ref):
    r = etree.Element(w("r"))
    if estilo_ref:
        rpr = etree.SubElement(r, w("rPr"))
        etree.SubElement(rpr, w("rStyle")).set(w("val"), estilo_ref)
    etree.SubElement(r, w("commentReference")).set(w("id"), str(id_novo))
    return r


def inserir_depois(ancora, novo):
    pai = ancora.getparent()
    pai.insert(pai.index(ancora) + 1, novo)


def inserir_antes(ancora, novo):
    pai = ancora.getparent()
    pai.insert(pai.index(ancora), novo)


def ultimo_paragrafo_do_pai(pacote, raiz_com, id_pai, usados_para):
    """paraId do último parágrafo do comentário-pai (cria se faltar)."""
    for com in raiz_com.iter(w("comment")):
        if com.get(w("id")) == str(id_pai):
            ps = com.findall(w("p"))
            if not ps:
                p = etree.SubElement(com, w("p"))
                ps = [p]
            ultimo = ps[-1]
            valor = ultimo.get(qn("w14:paraId"))
            if not valor:
                valor = novo_hex(usados_para, random.SystemRandom())
                ultimo.set(qn("w14:paraId"), valor)
            return valor
    return None


def iniciais_de(autor):
    letras = [parte[0] for parte in autor.split() if parte]
    return "".join(letras[:3]).upper()


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Cria um comentário do Word ancorado num trecho exato do texto.")
    ap.add_argument("entrada", help="arquivo .docx ou pasta desempacotada")
    ap.add_argument("--trecho", help="texto exato a comentar, como aparece no documento")
    ap.add_argument("--texto", required=True, help="texto do comentário")
    ap.add_argument("--autor", default=None, help='autor (padrão: DOC_AUTOR ou "Revisor")')
    ap.add_argument("--iniciais", default=None, help="iniciais do autor")
    ap.add_argument("--resposta-a", type=int, default=None, metavar="ID",
                    help="responde ao comentário de número ID (resposta encadeada)")
    ap.add_argument("--ocorrencia", type=int, default=None, metavar="N",
                    help="qual ocorrência do trecho usar, a partir de 1")
    ap.add_argument("-o", "--saida", help="arquivo .docx de saída (obrigatório para entrada .docx)")
    args = ap.parse_args(argv)

    if args.trecho is None and args.resposta_a is None:
        ap.error("informe --trecho, ou --resposta-a para responder no mesmo intervalo")
    if args.trecho == "":
        ap.error("--trecho não pode ser vazio")
    if args.ocorrencia is not None and args.ocorrencia < 1:
        ap.error("--ocorrencia começa em 1")
    if not args.texto.strip():
        ap.error("--texto não pode ser vazio")

    autor = args.autor or os.environ.get("DOC_AUTOR") or "Revisor"
    iniciais = args.iniciais if args.iniciais is not None else iniciais_de(autor)

    pacote = abrir_ou_sair(args.entrada, args.saida)
    doc = pacote.xml(DOCUMENTO)

    # Comentário-pai, se for resposta.
    nome_com_existente = pacote.alvo_por_tipo(DOCUMENTO, REL_COMENTARIOS)
    if args.resposta_a is not None:
        existe_pai = False
        if nome_com_existente and pacote.existe(nome_com_existente):
            for com in pacote.xml(nome_com_existente).iter(w("comment")):
                if com.get(w("id")) == str(args.resposta_a):
                    existe_pai = True
        if not existe_pai:
            falhar("Não existe comentário com número %d para responder." % args.resposta_a,
                   SAIDA_REPROVOU)

    # Onde ancorar.
    alvo = None
    if args.trecho is not None:
        achados = achar_ocorrencias(doc, args.trecho)
        if not achados:
            falhar('Trecho não encontrado no corpo do documento: "%s". Confira maiúsculas, '
                   "acentos e espaços; o trecho precisa estar dentro de um parágrafo só."
                   % args.trecho, SAIDA_REPROVOU)
        if args.ocorrencia is not None:
            if args.ocorrencia > len(achados):
                falhar("Pedi a ocorrência %d, mas o trecho aparece %d vez(es)."
                       % (args.ocorrencia, len(achados)), SAIDA_REPROVOU)
            alvo = achados[args.ocorrencia - 1]
        elif len(achados) > 1:
            linhas = []
            for i, (_, numero, ini, texto) in enumerate(achados[:10], start=1):
                a = max(0, ini - 25)
                b = min(len(texto), ini + len(args.trecho) + 25)
                linhas.append("  %d) parágrafo %d: ...%s..." % (i, numero, texto[a:b].replace("\n", " ")))
            falhar('O trecho "%s" aparece %d vezes. Escolha uma com --ocorrencia N:\n%s'
                   % (args.trecho, len(achados), "\n".join(linhas)), SAIDA_REPROVOU)
        else:
            alvo = achados[0]

    # Identificadores.
    nome_com, raiz_com = parte_de_comentarios(pacote)
    ids = todos_os_ids(pacote, [DOCUMENTO, nome_com])
    id_novo = max(ids) + 1
    usados_para = todos_os_para_ids(pacote)
    sorteio = random.SystemRandom()
    n_paragrafos = len(args.texto.split("\n"))
    para_ids = [novo_hex(usados_para, sorteio) for _ in range(n_paragrafos)]

    estilo_texto = "CommentText" if estilo_existe(pacote, "CommentText") else None
    estilo_ref = "CommentReference" if estilo_existe(pacote, "CommentReference") else None

    # Âncora no corpo.
    inicio_marca = etree.Element(w("commentRangeStart"))
    inicio_marca.set(w("id"), str(id_novo))
    fim_marca = etree.Element(w("commentRangeEnd"))
    fim_marca.set(w("id"), str(id_novo))
    referencia = trecho_de_referencia(id_novo, estilo_ref)

    if alvo is not None:
        p, _, ini, _ = alvo
        primeiro, ultimo = isolar(p, ini, ini + len(args.trecho))
        inserir_antes(primeiro, inicio_marca)
        inserir_depois(ultimo, fim_marca)
        inserir_depois(fim_marca, referencia)
    else:
        pai_id = str(args.resposta_a)
        ini_pai = next((e for e in doc.iter(w("commentRangeStart")) if e.get(w("id")) == pai_id), None)
        fim_pai = next((e for e in doc.iter(w("commentRangeEnd")) if e.get(w("id")) == pai_id), None)
        ref_pai = None
        for e in doc.iter(w("commentReference")):
            if e.get(w("id")) == pai_id:
                ref_pai = e.getparent()
                break
        if ini_pai is None and fim_pai is None and ref_pai is None:
            falhar("O comentário %s não está ancorado no corpo; indique --trecho para a resposta."
                   % pai_id, SAIDA_REPROVOU)
        if ini_pai is not None and fim_pai is not None:
            inserir_depois(ini_pai, inicio_marca)
            inserir_depois(fim_pai, fim_marca)
            ancora_ref = ref_pai if ref_pai is not None and ref_pai.getparent() is fim_marca.getparent() else fim_marca
            inserir_depois(ancora_ref, referencia)
        else:
            inserir_depois(ref_pai if ref_pai is not None else (fim_pai if fim_pai is not None else ini_pai),
                           referencia)

    # Comentário em si.
    data = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    raiz_com.append(montar_comentario(id_novo, autor, iniciais, data, args.texto,
                                      para_ids, (estilo_texto, estilo_ref)))

    # Encadeamento e identificador durável.
    estendido = parte_auxiliar(pacote, REL_ESTENDIDO, TIPO_ESTENDIDO,
                               "commentsExtended.xml", "commentsEx", "w15")
    ids_parte = parte_auxiliar(pacote, REL_IDS, TIPO_IDS, "commentsIds.xml", "commentsIds", "w16cid")
    entrada = etree.SubElement(estendido, qn("w15:commentEx"))
    entrada.set(qn("w15:paraId"), para_ids[-1])
    if args.resposta_a is not None:
        pai_para = ultimo_paragrafo_do_pai(pacote, raiz_com, args.resposta_a, usados_para)
        if pai_para:
            ja_listado = any(e.get(qn("w15:paraId"), "").upper() == pai_para.upper()
                             for e in estendido.iter(qn("w15:commentEx")))
            if not ja_listado:
                pai_ex = etree.Element(qn("w15:commentEx"))
                pai_ex.set(qn("w15:paraId"), pai_para)
                pai_ex.set(qn("w15:done"), "0")
                estendido.insert(estendido.index(entrada), pai_ex)
            entrada.set(qn("w15:paraIdParent"), pai_para)
    entrada.set(qn("w15:done"), "0")
    duravel = etree.SubElement(ids_parte, qn("w16cid:commentId"))
    duravel.set(qn("w16cid:paraId"), para_ids[-1])
    duravel.set(qn("w16cid:durableId"), novo_hex(usados_para, sorteio))

    pacote.gravar(args.saida)
    print("Comentário %d criado por %s. Gravado em %s" % (id_novo, autor, args.saida or args.entrada))
    return SAIDA_OK


if __name__ == "__main__":
    sys.exit(main())
