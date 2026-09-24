#!/usr/bin/env python3
"""
conferir_fontes.py, a conferência de fonte da entrega (cópia da soft-webinar,
adaptada pra landing em 24/09: lê HTML, léxico de entrega e lote, termo que o
insumo também traz não reprova, e confere a estrutura do HTML entregue).

A falha medida número 1 da skill é afirmar o que o insumo não traz: número,
prazo, escassez, presença ao vivo, replay, frequência sem fonte. Regra em prosa
não segurou; este script confere na mão do código.

O que ele faz:
  1. NÚMEROS. Extrai da entrega todo número (R$, %, dias, minutos, x, mil, k,
     milhões, e número por extenso seguido de unidade) e procura o MESMO VALOR
     no insumo, em qualquer formato (R$1.497 = 1497 = 1.497,00; 3 mil = 3.000
     = 3k). Número estrutural fica de fora: posição de slide, etapa, minuto do
     roteiro ("min 42"), carimbo de tempo, numeração de lista, código entre
     crases, lacuna entre colchetes e inteiro até 10 sem unidade.
  2. LÉXICO. Toda linha com termo do léxico de risco (escassez, prazo,
     presença ao vivo, replay, frequência sem fonte, promessa com prazo,
     presente, autor externo, formato "ao vivo", custo, dados, pagamento
     protegido, canal da confirmação) sai marcada pra revisão, sempre.
  3. NOMES. Todo nome próprio entre aspas é procurado no insumo (só aviso).
  4. HTML. Arquivo .html é lido só no texto visível (sem comentário, CSS,
     script e atributo). Reprova: {{ que sobrou, marcador [DO DONO ou
     [A CONFIRMAR visível, "a confirmar" ou #CONECTAR visível, seletor de
     sessões sem horário em ISO, tag sem fechar, id repetido, âncora #x sem
     alvo, falta do meta viewport, mais de um destino de clique fora da página.
     Avisa: recurso externo (fonte de marca pode), preço riscado (<s>, <del>).

Campo de nota: linha dentro de um bloco **NOTAS** que não seja FALA, TELA ou
TRANSIÇÃO; linha que abre com FALTA, NOTA ou PERGUNTA; linha de seção cujo
título fala de perguntas, notas, furos, o que ficou fora ou pendências; linha
com [A CONFIRMAR ou [DO DONO. Ali mora a pergunta ao dono, e ali o item
não reprova.

Sai com código 1 quando existe número sem fonte ou linha de léxico FORA de
campo de nota. Arquivo cujo nome começa com "_" é bastidor e fica de fora
(use --incluir-bastidor pra conferir também).

USO:
    python3 scripts/conferir_fontes.py --entrega <pasta ou arquivos> \\
        --insumo <arquivos do dono>
    python3 scripts/conferir_fontes.py --entrega saida/ --insumo   # sem insumo:
        todo número fica sem fonte
    python3 scripts/conferir_fontes.py --selftest

Sem dependência externa. Python 3.
"""
import argparse
import csv
import html
import io
import os
import re
import sys
import unicodedata
from html.parser import HTMLParser

LEXICO = [
    ("escassez", r"lugar(es)? (limitado|fixo)s?"),
    ("escassez", r"\bvagas?\b"),
    ("escassez", r"\bassentos?\b"),
    ("escassez", r"\blimitad[oa]s?\b"),
    ("escassez", r"[úu]ltim[oa]s? (vaga|lugar|unidade)s?"),
    ("prazo", r"s[óo] hoje"),
    ("prazo", r"at[ée] o fim d(esta|essa) aula"),
    ("prazo", r"n[ãa]o volta"),
    ("prazo", r"s[óo] n(essa|esta) (sess[ãa]o|aula)"),
    ("prazo", r"tempo limitado"),
    ("prazo", r"termina (amanh[ãa]|hoje)"),
    ("prazo", r"[úu]ltimo dia"),
    ("prazo", r"(janela|condi[çc][ãa]o) (fecha|acaba)"),
    ("presenca", r"\blei?o (os |alguns )?nomes"),
    ("presenca", r"\bl[êe] (alguns |os |2 ou 3 |uns )?(coment[áa]rios|nomes|respostas)"),
    ("presenca", r"fico aqui|vou ficar (mais|aqui|pra)"),
    ("presenca", r"j[áa] tem gente"),
    ("presenca", r"n[ãa]o consigo me ouvir"),
    ("presenca", r"t[ôo] vendo (aqui|que)"),
    ("replay", r"replay|reprise"),
    ("replay", r"n[ãa]o recome[çc]a"),
    ("replay", r"sem material depois"),
    ("replay", r"s[óo] quem (fica|ficar|assistir) at[ée] o (fim|final)"),
    ("frequencia", r"a (grande )?maioria"),
    ("frequencia", r"\bmetade\b"),
    ("frequencia", r"mais comum"),
    ("frequencia", r"quase todo"),
    ("frequencia", r"tem gente fazendo"),
    ("promessa", r"em [0-9]+ (dias|semanas|meses)"),
    ("promessa", r"em (poucas )?semanas"),
    ("promessa", r"(caminho|m[ée]todo)[^.]{0,20}testado"),
    ("desconto", r"(mais|um) desconto"),
    ("presente", r"\bpresente\b|presentinho"),
    ("autor", r"\bSchwartz\b"),
    ("entrega", r"\blembretes?\b"),
    ("entrega", r"(link|acesso|b[ôo]nus)[^.]{0,40}(chega|vai chegar|enviad|mandamos|te mando|receber[áa])"),
    ("lote", r"\blotes?\b"),
    ("prazo", r"[úu]ltima (chance|oportunidade)"),
    ("escassez", r"esgot"),
    ("replay", r"fica gravad"),
    ("formato", r"\bao vivo\b"),
    ("custo", r"gratuit|\bgr[áa]tis\b|sem custo|de gra[çc]a"),
    ("dados", r"dados (ficam|protegid|seguros?|guardad)|sem spam"),
    ("pagamento", r"pagamento (protegido|seguro)|compra (segura|protegida)|ambiente seguro"),
    ("entrega", r"\bpor (e-?mail|whats\s?app|sms)\b"),
]
LEX_RE = [(t, re.compile(p, re.I)) for t, p in LEXICO]

MULT = {"mil": 1e3, "k": 1e3, "m": 1e6, "mi": 1e6, "milhao": 1e6, "milhoes": 1e6,
        "bi": 1e9, "bilhao": 1e9, "bilhoes": 1e9}
UNIDADES = (r"%|x\b|vezes|dias?|anos?|meses|m[êe]s|semanas?|horas?|h\b|minutos?|"
            r"min\b|segundos?|pessoas|clientes|alunos|alunas|vagas?|lugares|"
            r"lan[çc]amentos|nichos|cl[íi]nicas|parcelas|reais")
EXTENSO = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "quatro": 4,
           "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10,
           "onze": 11, "doze": 12, "quinze": 15, "vinte": 20, "trinta": 30,
           "quarenta": 40, "cinquenta": 50, "sessenta": 60, "noventa": 90,
           "cem": 100, "mil": 1000}

NUM_RE = re.compile(
    r"(?P<moeda>R\$|US\$)?\s?~?"
    r"(?P<num>\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)"
    r"(?P<mult>\s?(?:mil\b|milh(?:[õo]es|[ãa]o)\b|mi\b|bi(?:lh(?:[õo]es|[ãa]o))?\b|[kK]\b|M\b))?"
    r"(?P<un>\s?(?:" + UNIDADES + r"))?", re.I)
EXT_RE = re.compile(r"\b(?P<w>" + "|".join(EXTENSO) + r")\s(?P<un>" + UNIDADES + r")", re.I)
MAIS_DE_MIL = re.compile(r"\bmais de mil\b", re.I)
RANGE_RE = re.compile(r"^\s?(?:-|–|a|e|até|ate|to)\s?(?:R\$\s?)?\d[\d.,]*\s?(mil\b|milh\w+|k\b|M\b|mi\b)", re.I)

ESTRUTURAL_ANTES = re.compile(
    r"\b(?:slides?|s|tela|bloco|passo|etapa|fase|parte|se[çc][ãa]o|item|mensagem|"
    r"e-?mail|whatsapp|obje[çc][ãa]o|min|minuto|linha|cap|cap[íi]tulo|lei|regra|dia|"
    r"onda|toque|pergunta|beat|camada|n[íi]vel|virada|op[çc][ãa]o|vers[ãa]o|caso|"
    r"ato|prova|p|q|c|r|n|n[ºo])\s?\.?\s?#?$", re.I)
ADJACENTE = re.compile(r"(?:[A-Za-z#_/]|\d[:.])$")


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def valor(num, mult):
    s = num
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "." in s:
        partes = s.split(".")
        if all(len(p) == 3 for p in partes[1:]):
            s = s.replace(".", "")
    elif "," in s:
        partes = s.split(",")
        s = s.replace(",", "", len(partes) - 2).replace(",", ".")
    try:
        v = float(s)
    except ValueError:
        return None
    if mult:
        m = sem_acento(mult.strip())
        v *= MULT.get(m, MULT.get(m.rstrip("s"), 1))
    return round(v, 2)


def numeros(linha, estrutural=True):
    """Devolve [(trecho, [valores candidatos], tem_unidade)] da linha."""
    out = []
    limpa = re.sub(r"`[^`]*(?:tag|roteamento|\.md|\.py|\.csv|/|_)[^`]*`", lambda m: " " * len(m.group(0)), linha)
    if estrutural:
        limpa = re.sub(r"\[[^\]]*\]", lambda m: " " * len(m.group(0)), limpa)
        limpa = re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\b", lambda m: " " * len(m.group(0)), limpa)
        limpa = re.sub(r"^\s*(?:[-*>|]\s*)*\**\d+[.)º°ª]\**\s", lambda m: " " * len(m.group(0)), limpa)
        limpa = re.sub(r"\d+[ºª°]", lambda m: " " * len(m.group(0)), limpa)
    for m in NUM_RE.finditer(limpa):
        pos = m.start("moeda") if m.group("moeda") else m.start("num")
        antes = limpa[max(0, pos - 14):pos].rstrip("~")
        if estrutural and not m.group("moeda") and (ESTRUTURAL_ANTES.search(antes) or ADJACENTE.search(antes)):
            continue
        v = valor(m.group("num"), m.group("mult"))
        if v is None:
            continue
        un = (m.group("un") or "").strip()
        tem_un = bool(un or m.group("moeda") or m.group("mult"))
        if estrutural and not tem_un and v <= 10:
            continue
        cands = [v]
        rg = RANGE_RE.match(limpa[m.end():m.end() + 16])
        if rg and not m.group("mult"):
            cands.append(valor(m.group("num"), rg.group(1)))
        out.append((m.group(0).strip(), cands, tem_un))
    for m in EXT_RE.finditer(limpa):
        out.append((m.group(0), [float(EXTENSO[sem_acento(m.group("w"))])], True))
    for m in MAIS_DE_MIL.finditer(limpa):
        out.append((m.group(0), [1000.0], True))
    return out


def valores_insumo(textos):
    vals = set()
    for t in textos:
        for linha in t.splitlines():
            for _, cands, _ in numeros(linha, estrutural=False):
                for c in cands:
                    if c is not None:
                        vals.add(c)
    return vals


NOME_RE = re.compile(r"[\"“«]([^\"”»\n]{2,60})[\"”»]")


def nomes(linha):
    out = []
    for m in NOME_RE.finditer(linha):
        s = m.group(1).strip()
        pal = s.split()
        if not (1 <= len(pal) <= 5) or re.search(r"[.!?;:,]", s):
            continue
        if all(p[0].isupper() or p.lower() in ("de", "da", "do", "dos", "das", "e") for p in pal) and pal[0][0].isupper():
            out.append(s)
    return out


LABEL_PECA = re.compile(r"^\s*[-*>]*\s*\**\s*(FALA|TELA|TRANSI[ÇC][ÃA]O|CONTE[ÚU]DO|T[ÍI]TULO|VISUAL)\b", re.I)
NOTAS_ABRE = re.compile(r"^\s*\**\s*NOTAS\b", re.I)
SECAO = re.compile(r"^\s*#{1,6}\s")
SECAO_PERG = re.compile(r"perguntas|notas|furos|fica(ram)? fora|pend[êe]ncias|a confirmar", re.I)
NOTA_LINHA = re.compile(r"^\s*[-*>]*\s*\**\s*(FALTA|NOTA|PERGUNTA|PERGUNTA AO DONO|A CONFIRMAR)\b", re.I)
CAMPO_ABRE = re.compile(r"^\s*\*\*[^*]+\*\*\s*:?\s*$|^\s*\*\*[A-ZÇÃÕÉÍ ]{3,}\*\*")


def classifica(linhas):
    """Devolve lista de bools: True se a linha é campo de nota."""
    res = []
    em_notas = False
    em_perg = False
    for ln in linhas:
        if SECAO.match(ln):
            em_perg = bool(SECAO_PERG.search(ln))
            em_notas = False
        elif NOTAS_ABRE.match(ln):
            em_notas = True
            res.append(True)
            continue
        elif CAMPO_ABRE.match(ln) and not NOTAS_ABRE.match(ln):
            em_notas = False
        nota = (em_perg or (em_notas and not LABEL_PECA.match(ln)) or bool(NOTA_LINHA.match(ln))
                or bool(re.search(r"\[(A CONFIRMAR|DO DONO)", ln, re.I)))
        res.append(nota)
    return res


def ler(caminhos, bastidor):
    arquivos = []
    for c in caminhos:
        if os.path.isdir(c):
            for raiz, _, fs in os.walk(c):
                for f in sorted(fs):
                    if f.endswith((".md", ".csv", ".txt", ".html")):
                        arquivos.append(os.path.join(raiz, f))
        elif os.path.isfile(c):
            arquivos.append(c)
    if not bastidor:
        arquivos = [a for a in arquivos if not os.path.basename(a).startswith("_")]
    return arquivos


def _apaga(m):
    return "\n" * m.group(0).count("\n")


def html_visivel(bruto):
    """Texto que o visitante lê, linha a linha, com a numeração do arquivo."""
    t = re.sub(r"<!--.*?-->", _apaga, bruto, flags=re.S)
    t = re.sub(r"<(style|script)\b.*?</\1>", _apaga, t, flags=re.S | re.I)
    t = re.sub(r"<(s|del)\b[^>]*>", " RISCADO:", t, flags=re.I)
    t = re.sub(r"<[^>]*>", lambda m: " " * 1 + "\n" * m.group(0).count("\n"), t)
    return [html.unescape(re.sub(r"\s+", " ", ln)).strip() for ln in t.split("\n")]


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class _Estrutura(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pilha, self.erros, self.ids, self.ancoras, self.destinos = [], [], {}, set(), set()
        self.viewport = False
        self.externos = 0
        self.em_sessao = False
        self.sessoes = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids[a["id"]] = self.ids.get(a["id"], 0) + 1
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        for k in ("src", "href"):
            v = a.get(k) or ""
            if v.startswith("http") and tag in ("script", "link", "img", "iframe"):
                self.externos += 1
        alvo = a.get("action") if tag == "form" else (a.get("href") if tag == "a" and "botao" in (a.get("class") or "") else None)
        if alvo is not None:
            if alvo.startswith("#") and not alvo.startswith("#CONECTAR"):
                self.ancoras.add(alvo[1:])
            elif alvo:
                self.destinos.add(alvo)
        if tag == "select" and a.get("name") == "sessao":
            self.em_sessao, self.sessoes = True, []
        if tag == "option" and self.em_sessao:
            self.sessoes.append(a.get("value") or "")
        if tag not in VOID:
            self.pilha.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag == "select":
            self.em_sessao = False
        if self.pilha and self.pilha[-1] == tag:
            self.pilha.pop()
        else:
            self.erros.append(f"</{tag}> na linha {self.getpos()[0]}")
            if tag in self.pilha:
                del self.pilha[len(self.pilha) - 1 - self.pilha[::-1].index(tag):]


def estrutura_html(arq):
    """Devolve [(onde, problema, veredito)] da estrutura do HTML entregue."""
    bruto = open(arq, encoding="utf-8", errors="replace").read()
    nome = os.path.basename(arq)
    sem_coment = re.sub(r"<!--.*?-->", _apaga, bruto, flags=re.S)
    out = []
    for i, ln in enumerate(sem_coment.splitlines(), 1):
        if "{{" in ln:
            out.append((f"{nome}:{i}", "token {{ sem preencher", "REPROVA"))
    for i, ln in enumerate(html_visivel(bruto), 1):
        if re.search(r"\[(DO DONO|A CONFIRMAR)", ln, re.I):
            out.append((f"{nome}:{i}", "marcador visível na página", "REPROVA"))
        elif re.search(r"\ba (confirmar|definir)\b|#CONECTAR", ln, re.I):
            out.append((f"{nome}:{i}", "pendência visível (\"a confirmar\" ou #CONECTAR): o elemento sai e vira pergunta", "REPROVA"))
    p = _Estrutura()
    p.feed(bruto)
    p.close()
    for e in p.erros:
        out.append((nome, "tag fechada fora de ordem: " + e, "REPROVA"))
    for t in p.pilha:
        if t not in ("html", "body", "head", "p", "li"):
            out.append((nome, f"<{t}> sem fechar", "REPROVA"))
    for k, v in p.ids.items():
        if v > 1:
            out.append((nome, f"id repetido: {k} ({v}x)", "REPROVA"))
    for a in p.ancoras:
        if a and a not in p.ids:
            out.append((nome, f"botão aponta pra #{a}, que não existe", "REPROVA"))
    if p.sessoes is not None and not any(re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", v) for v in p.sessoes):
        out.append((nome, "seletor de sessões sem horário real (value em ISO): sem horário no insumo, o seletor sai", "REPROVA"))
    if not p.viewport:
        out.append((nome, "falta <meta name=viewport>", "REPROVA"))
    if len(p.destinos) > 1:
        out.append((nome, "mais de um destino de clique: " + ", ".join(sorted(p.destinos)), "REPROVA"))
    if p.externos:
        out.append((nome, f"recurso externo: {p.externos} (foto, player, pixel e fonte do dono podem; biblioteca e CSS de terceiro saem)", "aviso"))
    return out


COL_TEXTO = re.compile(r"message|mensagem|texto|text|coment|comment|fala", re.I)


def texto_linhas(arq):
    """Linhas a conferir. No CSV, só as colunas de texto (o resto é tempo e nome)."""
    bruto = open(arq, encoding="utf-8", errors="replace").read()
    if arq.endswith(".html"):
        return html_visivel(bruto)
    if not arq.endswith(".csv"):
        return bruto.splitlines()
    linhas = []
    rows = list(csv.reader(io.StringIO(bruto)))
    if not rows:
        return linhas
    cols = [i for i, h in enumerate(rows[0]) if COL_TEXTO.search(h)]
    linhas.append("")
    for r in rows[1:]:
        linhas.append(" · ".join(r[i] for i in cols if i < len(r)) if cols else " · ".join(r))
    return linhas


def conferir(entrega, insumo, bastidor=False, largura=90, aceitar=()):
    textos_ins = [open(f, encoding="utf-8", errors="replace").read() for f in ler(insumo, True)]
    vals = valores_insumo(textos_ins) | {round(float(a), 2) for a in aceitar}
    ins_norm = sem_acento("\n".join(textos_ins))
    linhas_tab = []
    n_num_falha = n_lex_falha = n_num = n_lex = n_nome_aviso = 0
    for arq in ler(entrega, bastidor):
        linhas = texto_linhas(arq)
        eh_html = arq.endswith(".html")
        notas = [False] * len(linhas) if eh_html else classifica(linhas)
        nome_arq = os.path.basename(arq)
        for i, ln in enumerate(linhas, 1):
            nota = notas[i - 1]
            campo = "NOTA" if nota else "peça"
            for trecho, cands, _ in numeros(ln):
                n_num += 1
                ok = any(c in vals for c in cands if c is not None)
                if ok:
                    continue
                ver = "pergunta ao dono" if nota else "SEM FONTE"
                if not nota:
                    n_num_falha += 1
                linhas_tab.append((f"{nome_arq}:{i}", "número", trecho, "não", campo, ver))
            for tipo, rx in LEX_RE:
                m = rx.search(ln)
                if m:
                    n_lex += 1
                    a = max(0, m.start() - 35)
                    tre = ln[a:m.end() + 35].strip()
                    no_ins = sem_acento(m.group(0)) in ins_norm
                    if no_ins:
                        ver = "no insumo"
                    elif nota:
                        ver = "revisar (nota)"
                    else:
                        ver = "REVISAR FORA DE NOTA"
                        n_lex_falha += 1
                    linhas_tab.append((f"{nome_arq}:{i}", "léxico:" + tipo, tre, "sim" if no_ins else "não", campo, ver))
                    break
            for nm in nomes(ln):
                if sem_acento(nm) not in ins_norm:
                    n_nome_aviso += 1
                    linhas_tab.append((f"{nome_arq}:{i}", "nome", nm, "não", campo, "aviso"))
    n_estr = 0
    for arq in ler(entrega, bastidor):
        if arq.endswith(".html"):
            for onde, prob, ver in estrutura_html(arq):
                if ver == "REPROVA":
                    n_estr += 1
                linhas_tab.append((onde, "estrutura", prob, "-", "página", ver))
    print("| onde | tipo | trecho | no insumo | campo | veredito |")
    print("|---|---|---|---|---|---|")
    for r in linhas_tab:
        tre = r[2].replace("|", "/")
        if len(tre) > largura:
            tre = tre[:largura] + "…"
        print(f"| {r[0]} | {r[1]} | {tre} | {r[3]} | {r[4]} | {r[5]} |")
    print()
    print(f"números conferidos: {n_num} · sem fonte fora de nota: {n_num_falha}")
    print(f"linhas de léxico: {n_lex} · fora de nota: {n_lex_falha}")
    print(f"nomes entre aspas sem fonte (aviso): {n_nome_aviso}")
    print(f"estrutura do HTML reprovada: {n_estr}")
    print(f"insumos lidos: {len(textos_ins)} · valores no insumo: {len(vals)}")
    falhou = n_num_falha > 0 or n_lex_falha > 0 or n_estr > 0
    print("RESULTADO: " + ("REPROVA, tire da peça ou mova pra NOTAS como pergunta ao dono" if falhou else "PASSA"))
    return 1 if falhou else 0


def selftest():
    ins = "Preço R$1.497 à vista, 12x R$154,62. Âncora R$3.500. 30-100k/mês. Bônus (15 primeiros)."
    vals = valores_insumo([ins])
    casos = [("Custa 1497 reais", True), ("R$ 3.500,00 de âncora", True), ("R$ 3,5 mil", True),
             ("faz 30 mil por mês", True), ("100 mil", True), ("R$2.000 no botão", False),
             ("em 180 dias", False), ("seis anos atrás", False), ("~95% de abertura", False)]
    ok = True
    for frase, esperado in casos:
        achou = all(any(c in vals for c in cands) for _, cands, _ in numeros(frase)) and bool(numeros(frase))
        if achou != esperado:
            ok = False
            print("FALHA selftest:", frase, numeros(frase))
    estr = ["### Slide 12 · Abertura", "- min 42: link no ar", "1. primeiro item", "`tag: 25-75`", "[A CONFIRMAR: 3 casos]"]
    for e in estr:
        if numeros(e):
            ok = False
            print("FALHA estrutural:", e, numeros(e))
    lin = ["**NOTAS**", "- FALA: só hoje, galera", "- Pergunta ao dono: existe prazo? só hoje?", "### Slide 2", "Só hoje."]
    cl = classifica(lin)
    if cl != [True, False, True, False, False]:
        ok = False
        print("FALHA classifica:", cl)
    vis = html_visivel('<p class="a">Custa <s>R$ 197</s> hoje</p>\n<!-- 999 dias -->\n<style>b{x:12px}</style>')
    if "R$ 197" not in vis[0] or "999" in " ".join(vis) or "12px" in " ".join(vis):
        ok = False
        print("FALHA html_visivel:", vis)
    print("selftest:", "ok" if ok else "FALHOU")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Confere número, léxico de risco e nome da entrega contra o insumo do dono.")
    ap.add_argument("--entrega", nargs="*", default=[], help="pasta ou arquivos da entrega")
    ap.add_argument("--insumo", nargs="*", default=[], help="arquivos do dono (vazio: todo número fica sem fonte)")
    ap.add_argument("--incluir-bastidor", action="store_true", help="confere também arquivos que começam com _")
    ap.add_argument("--aceitar", nargs="*", default=[],
                    help="valores que a própria skill fixa e podem aparecer sem insumo (ex.: 3000, a régua de canal)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.entrega:
        ap.error("--entrega é obrigatório")
    sys.exit(conferir(a.entrega, a.insumo, a.incluir_bastidor, aceitar=a.aceitar))


if __name__ == "__main__":
    main()
