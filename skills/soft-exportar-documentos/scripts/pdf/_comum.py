"""Funcoes de apoio dos scripts da pasta pdf/ (nao e para rodar sozinho).

Junta o que os scripts dividem: abrir o PDF com pypdf, trocar coordenadas
entre o sistema do PDF (origem embaixo a esquerda) e o sistema "topo"
(origem em cima a esquerda, como a imagem da pagina e o pdftotext), medir e
quebrar texto e ler as caixas de um campos.json.

Codigos de saida usados pela pasta: 0 passou, 1 conferencia reprovou,
2 argumento errado, 3 falta dependencia ou arquivo, 4 programa externo falhou.
"""

import json
import os
import shutil
import subprocess
import sys

OK, REPROVOU, ARGUMENTO, DEPENDENCIA, EXTERNO = 0, 1, 2, 3, 4


def sair(mensagem, codigo):
    """Imprime a mensagem no erro padrao e encerra com o codigo dado."""
    print(mensagem, file=sys.stderr)
    sys.exit(codigo)


def exigir_pypdf():
    """Importa pypdf ou sai com codigo 3 dizendo o que instalar."""
    try:
        import pypdf  # noqa: F401
    except ImportError:
        sair("Falta a biblioteca pypdf. Instale com: pip install pypdf "
             "(de preferencia num venv) e rode de novo.", DEPENDENCIA)
    return pypdf


def exigir_pillow():
    """Importa Pillow ou sai com codigo 3."""
    try:
        from PIL import Image, ImageDraw, ImageFont  # noqa: F401
    except ImportError:
        sair("Falta a biblioteca Pillow. Instale com: pip install Pillow", DEPENDENCIA)
    return Image, ImageDraw, ImageFont


def exigir_programa(nome, pacote="poppler-utils"):
    """Confere se um programa externo existe no PATH; sai 3 se nao existir."""
    caminho = shutil.which(nome)
    if not caminho:
        sair(f"Falta o programa {nome}. Instale o pacote {pacote} "
             f"(por exemplo: apt install {pacote}).", DEPENDENCIA)
    return caminho


def exigir_arquivo(caminho):
    if not os.path.isfile(caminho):
        sair(f"Arquivo nao encontrado: {caminho}", DEPENDENCIA)


def rodar(cmd, tempo=300):
    """Roda programa externo; se falhar, sai com codigo 4 e mostra o erro."""
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=tempo)
    except subprocess.TimeoutExpired:
        sair(f"O programa {cmd[0]} passou do limite de {tempo} s.", EXTERNO)
    if r.returncode != 0:
        erro = r.stderr.decode("utf-8", "replace").strip()[:800]
        sair(f"O programa {cmd[0]} falhou (codigo {r.returncode}): {erro}", EXTERNO)
    return r


def abrir_pdf(caminho):
    """Abre o PDF com pypdf, tentando senha vazia se estiver protegido."""
    pypdf = exigir_pypdf()
    exigir_arquivo(caminho)
    try:
        leitor = pypdf.PdfReader(caminho)
    except Exception as e:  # arquivo corrompido ou que nao e PDF
        sair(f"Nao consegui abrir {caminho} como PDF: {e}", DEPENDENCIA)
    if leitor.is_encrypted:
        try:
            ok = leitor.decrypt("")
        except Exception:
            ok = 0
        if not ok:
            sair("O PDF tem senha. Tire a senha antes, com o dono de acordo: "
                 "qpdf --password=SENHA --decrypt entrada.pdf saida.pdf", DEPENDENCIA)
    return leitor


def ler_json(caminho):
    exigir_arquivo(caminho)
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        sair(f"JSON invalido em {caminho}: {e}", ARGUMENTO)


def gravar_json(dados, caminho):
    texto = json.dumps(dados, ensure_ascii=False, indent=2)
    if caminho in (None, "-"):
        print(texto)
    else:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(texto + "\n")


# ---------------------------------------------------------------- geometria

def r2(v):
    return round(float(v), 2)


def info_pagina(pagina):
    """Caixa de midia e giro da pagina, base de toda troca de coordenadas.

    Usa a MediaBox porque e ela que o pdftoppm e o pdftotext usam por padrao.
    """
    mb = pagina.mediabox
    x0, y0, x1, y1 = (float(mb.left), float(mb.bottom), float(mb.right), float(mb.top))
    giro = int(pagina.get("/Rotate", 0) or 0) % 360
    return {"x0": x0, "y0": y0, "x1": x1, "y1": y1, "giro": giro}


def tamanho_exibido(info):
    """Largura e altura da pagina como ela aparece (ja girada), em pontos."""
    w, h = info["x1"] - info["x0"], info["y1"] - info["y0"]
    return (h, w) if info["giro"] in (90, 270) else (w, h)


def _ponto_pdf_para_topo(info, ux, uy):
    x0, y0, x1, y1, g = info["x0"], info["y0"], info["x1"], info["y1"], info["giro"]
    if g == 90:
        return uy - y0, ux - x0
    if g == 180:
        return x1 - ux, uy - y0
    if g == 270:
        return y1 - uy, x1 - ux
    return ux - x0, y1 - uy


def _ponto_topo_para_pdf(info, dx, dy):
    x0, y0, x1, y1, g = info["x0"], info["y0"], info["x1"], info["y1"], info["giro"]
    if g == 90:
        return x0 + dy, y0 + dx
    if g == 180:
        return x1 - dx, y0 + dy
    if g == 270:
        return x1 - dy, y1 - dx
    return x0 + dx, y1 - dy


def _normalizar(a, b, c, d):
    return [min(a, c), min(b, d), max(a, c), max(b, d)]


def ret_pdf_para_topo(info, ret):
    """[x0, y0, x1, y1] do PDF para [esq, topo, dir, base] da pagina exibida."""
    a = _ponto_pdf_para_topo(info, ret[0], ret[1])
    b = _ponto_pdf_para_topo(info, ret[2], ret[3])
    return _normalizar(a[0], a[1], b[0], b[1])


def ret_topo_para_pdf(info, ret):
    a = _ponto_topo_para_pdf(info, ret[0], ret[1])
    b = _ponto_topo_para_pdf(info, ret[2], ret[3])
    return _normalizar(a[0], a[1], b[0], b[1])


def ret_valido(ret):
    return (isinstance(ret, (list, tuple)) and len(ret) == 4
            and all(isinstance(v, (int, float)) for v in ret))


# ---------------------------------------------------------- medida de texto

class Medidor:
    """Mede largura de texto em Helvetica.

    Usa a Liberation Sans (mesmas larguras da Helvetica), achada pelo fc-match
    ou passada por caminho. Sem ela, estima 0,55 do tamanho por caractere,
    que erra para mais e por isso nao deixa texto estourar a caixa.
    """

    def __init__(self, caminho_fonte=None):
        self.fonte = None
        caminho = caminho_fonte or self._achar()
        if caminho:
            try:
                from PIL import ImageFont
                self.fonte = ImageFont.truetype(caminho, 100)
            except Exception:
                self.fonte = None

    @staticmethod
    def _achar():
        if not shutil.which("fc-match"):
            return None
        try:
            r = subprocess.run(["fc-match", "Liberation Sans:style=Regular",
                                "--format=%{file}"], capture_output=True, timeout=20)
            caminho = r.stdout.decode("utf-8", "replace").strip()
        except Exception:
            return None
        if caminho and "liberation" in caminho.lower() and os.path.isfile(caminho):
            return caminho
        return None

    def largura(self, texto, tamanho):
        if not texto:
            return 0.0
        if self.fonte is not None:
            return self.fonte.getlength(texto) * tamanho / 100.0
        return len(texto) * tamanho * 0.55


def quebrar_linhas(texto, largura_max, tamanho, medidor):
    """Quebra o texto em linhas que cabem na largura. Respeita quebras do texto."""
    linhas = []
    for paragrafo in str(texto).split("\n"):
        palavras = paragrafo.split(" ")
        atual = ""
        for palavra in palavras:
            tentativa = palavra if not atual else atual + " " + palavra
            if medidor.largura(tentativa, tamanho) <= largura_max:
                atual = tentativa
                continue
            if atual:
                linhas.append(atual)
            # palavra sozinha maior que a linha: corta por caractere
            while medidor.largura(palavra, tamanho) > largura_max and len(palavra) > 1:
                corte = len(palavra) - 1
                while corte > 1 and medidor.largura(palavra[:corte], tamanho) > largura_max:
                    corte -= 1
                linhas.append(palavra[:corte])
                palavra = palavra[corte:]
            atual = palavra
        linhas.append(atual)
    return linhas


ALTURA_LINHA = 1.15  # entrelinha em multiplos do tamanho da fonte
FOLGA = 1.0          # margem interna da caixa, em pontos


def encaixar(texto, largura, altura, tamanho, minimo, medidor, reduzir=True):
    """Acha o tamanho de fonte em que o texto cabe na caixa.

    Devolve (tamanho_usado, linhas, cabe). Se nao couber nem no minimo,
    devolve o minimo (ou o pedido, sem reduzir) com cabe=False.
    """
    util_w = max(largura - 2 * FOLGA, 1.0)
    util_h = max(altura - 2 * FOLGA, 1.0)
    t = float(tamanho)
    piso = min(float(minimo), t) if reduzir else t
    while True:
        linhas = quebrar_linhas(texto, util_w, t, medidor)
        alto = t + (len(linhas) - 1) * t * ALTURA_LINHA
        largo = max((medidor.largura(l, t) for l in linhas), default=0)
        if alto <= util_h + 0.01 and largo <= util_w + 0.01:
            return t, linhas, True
        if t - 0.5 < piso - 1e-9:
            return t, linhas, False
        t = round(t - 0.5, 2)


# ------------------------------------------------------- texto em stream PDF

def literal_pdf(texto):
    """Codifica texto como string literal do PDF em WinAnsi (cp1252).

    Devolve (bytes com parenteses, lista de caracteres trocados por '?').
    """
    trocados = []
    saida = bytearray(b"(")
    for ch in texto:
        try:
            b = ch.encode("cp1252")
        except UnicodeEncodeError:
            trocados.append(ch)
            b = b"?"
        for byte in b:
            if byte in (0x28, 0x29, 0x5C):  # ( ) \
                saida += b"\\" + bytes([byte])
            elif byte < 32 or byte > 126:
                saida += b"\\%03o" % byte
            else:
                saida.append(byte)
    saida += b")"
    return bytes(saida), trocados


def fonte_helvetica(escritor):
    """Cria (uma vez por escritor) a fonte Helvetica WinAnsi como objeto indireto."""
    from pypdf.generic import DictionaryObject, NameObject
    cache = getattr(escritor, "_soft_helvetica", None)
    if cache is not None:
        return cache
    fonte = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
        NameObject("/Encoding"): NameObject("/WinAnsiEncoding"),
    })
    ref = escritor._add_object(fonte)
    escritor._soft_helvetica = ref
    return ref


def cor_hex(cor):
    """'#1a2b3c' ou '1a2b3c' para (r, g, b) entre 0 e 1. Padrao preto."""
    if not cor:
        return (0.0, 0.0, 0.0)
    c = str(cor).lstrip("#")
    if len(c) != 6:
        raise ValueError(f"cor invalida: {cor}")
    return tuple(int(c[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def conteudo_texto(linhas, tamanho, largura, altura, medidor, cor=(0, 0, 0),
                   alinhamento="esquerda", centralizar_uma_linha=True):
    """Monta o fluxo de desenho do texto numa caixa [0 0 largura altura].

    Devolve (bytes do fluxo, caracteres trocados).
    """
    trocados = []
    partes = [b"q", b"0 0 %.2f %.2f re W n" % (largura, altura), b"BT",
              b"/F1 %.2f Tf" % tamanho, b"%.3f %.3f %.3f rg" % tuple(cor)]
    entre = tamanho * ALTURA_LINHA
    if len(linhas) == 1 and centralizar_uma_linha:
        # centro vertical aproximado: a base fica 0,28 do tamanho abaixo do meio
        y = (altura - tamanho) / 2.0 + tamanho * 0.22
    else:
        y = altura - FOLGA - tamanho * 0.8
    for linha in linhas:
        w = medidor.largura(linha, tamanho)
        if alinhamento == "centro":
            x = (largura - w) / 2.0
        elif alinhamento == "direita":
            x = largura - FOLGA - w
        else:
            x = FOLGA
        lit, tr = literal_pdf(linha)
        trocados += tr
        partes.append(b"1 0 0 1 %.2f %.2f Tm %s Tj" % (x, y, lit))
        y -= entre
    partes += [b"ET", b"Q"]
    return b"\n".join(partes), trocados


# ------------------------------------------------------ leitura de caixas

def ler_caixas(dados):
    """Normaliza um campos.json (dos dois formatos) em lista de caixas.

    Cada caixa: pagina, nome, tipo, sistema ('pdf' ou 'topo'), ret em pontos,
    tamanho_fonte (ou None), texto (ou None). Devolve (caixas, erros).

    Formato 1 (saida do campos_info.py): campos com lista "widgets".
    Formato 2 (entrada do preencher_texto.py): campos com "retangulo".
    """
    erros = []
    caixas = []
    if isinstance(dados, list):
        dados = {"campos": dados}
    if not isinstance(dados, dict) or not isinstance(dados.get("campos"), list):
        return [], ["o JSON precisa ter a lista 'campos'"]
    sistema = dados.get("sistema", "topo")
    if sistema not in ("topo", "pdf"):
        erros.append(f"sistema '{sistema}' invalido; use 'topo' ou 'pdf'")
        sistema = "topo"
    escala = 72.0 / float(dados.get("escala_dpi", 72) or 72)
    padrao_fonte = dados.get("tamanho_fonte_padrao", 10)
    for i, c in enumerate(dados["campos"]):
        if not isinstance(c, dict):
            erros.append(f"campo {i + 1}: nao e um objeto")
            continue
        nome = str(c.get("nome") or c.get("descricao") or f"campo {i + 1}")
        if "widgets" in c:  # formato 1
            for j, w in enumerate(c.get("widgets") or []):
                ret = w.get("retangulo_pdf")
                if not ret_valido(ret) or not isinstance(w.get("pagina"), int):
                    erros.append(f"{nome}: widget {j + 1} sem pagina ou retangulo_pdf valido")
                    continue
                rotulo = nome
                if c.get("tipo") == "radio" and w.get("valor_ligado"):
                    rotulo = f"{nome}={w['valor_ligado']}"
                caixas.append({"pagina": w["pagina"], "nome": rotulo,
                               "tipo": c.get("tipo", "campo"), "sistema": "pdf",
                               "ret": [float(v) for v in ret],
                               "tamanho_fonte": c.get("tamanho_fonte") or None,
                               "texto": None})
            continue
        ret = c.get("retangulo")
        pag = c.get("pagina")
        if not isinstance(pag, int) or pag < 1:
            erros.append(f"{nome}: falta 'pagina' (numero a partir de 1)")
            continue
        if not ret_valido(ret):
            erros.append(f"{nome}: 'retangulo' precisa ser [x0, y0, x1, y1]")
            continue
        texto = c.get("texto")
        tam = c.get("tamanho_fonte", padrao_fonte)
        caixas.append({"pagina": pag, "nome": nome, "tipo": c.get("tipo", "texto"),
                       "sistema": sistema, "ret": [float(v) * escala for v in ret],
                       "tamanho_fonte": float(tam) if tam else None,
                       "texto": None if texto is None else str(texto)})
        rot = c.get("retangulo_rotulo")
        if rot is not None:
            if ret_valido(rot):
                caixas.append({"pagina": pag, "nome": f"{nome} (rotulo)", "tipo": "rotulo",
                               "sistema": sistema, "ret": [float(v) * escala for v in rot],
                               "tamanho_fonte": None, "texto": None})
            else:
                erros.append(f"{nome}: 'retangulo_rotulo' precisa ser [x0, y0, x1, y1]")
    return caixas, erros


# ------------------------------------------------- campos AcroForm (pypdf)

BIT_SOMENTE_LEITURA = 1
BIT_OBRIGATORIO = 1 << 1
BIT_MULTILINHA = 1 << 12
BIT_RADIO = 1 << 15
BIT_BOTAO = 1 << 16
BIT_SUSPENSA = 1 << 17
BIT_EDITAVEL = 1 << 18
BIT_MULTIPLA = 1 << 21


def herdado(no, chave, limite=50):
    """Busca a chave no campo e, se faltar, nos pais (atributos herdaveis)."""
    atual = no
    for _ in range(limite):
        if atual is None:
            return None
        if chave in atual:
            return atual[chave].get_object() if hasattr(atual[chave], "get_object") else atual[chave]
        pai = atual.get("/Parent")
        atual = pai.get_object() if pai is not None else None
    return None


def para_python(valor):
    """Converte valor do pypdf (nome, texto, lista) em tipo simples do Python."""
    from pypdf.generic import ArrayObject, NameObject
    if valor is None:
        return None
    if hasattr(valor, "get_object"):
        valor = valor.get_object()
    if isinstance(valor, NameObject):
        return str(valor)[1:]
    if isinstance(valor, ArrayObject):
        return [para_python(v) for v in valor]
    if isinstance(valor, (int, float)):
        return valor
    return str(valor)


def tipo_do_campo(ft, ff):
    if ft == "/Tx":
        return "texto"
    if ft == "/Btn":
        if ff & BIT_BOTAO:
            return "botao"
        if ff & BIT_RADIO:
            return "radio"
        return "caixa_selecao"
    if ft == "/Ch":
        return "lista_suspensa" if ff & BIT_SUSPENSA else "lista"
    if ft == "/Sig":
        return "assinatura"
    return "desconhecido"


def estados_ligados(widget):
    """Nomes de aparencia de um widget de botao, sem o 'Off'."""
    ap = widget.get("/AP")
    if ap is None:
        return []
    n = ap.get_object().get("/N")
    if n is None:
        return []
    n = n.get_object()
    if not hasattr(n, "keys"):
        return []
    return [str(k)[1:] for k in n.keys() if str(k) != "/Off"]


def opcoes_de_lista(no):
    """Lista de (valor_exportado, texto_exibido) do /Opt de um campo de opcao."""
    opt = herdado(no, "/Opt")
    saida = []
    for item in (opt or []):
        item = item.get_object() if hasattr(item, "get_object") else item
        if isinstance(item, list) and len(item) >= 2:
            saida.append((str(item[0].get_object()), str(item[1].get_object())))
        else:
            saida.append((str(item), str(item)))
    return saida


def tamanho_da_fonte_da(da):
    import re
    if not da:
        return None
    m = re.search(r"/\S+\s+([\d.]+)\s+Tf", str(da))
    return float(m.group(1)) if m else None


def listar_campos(doc):
    """Percorre o AcroForm (leitor ou escritor do pypdf) e devolve os campos.

    Cada item: nome completo, tipo, no (dicionario do campo terminal), ff,
    widgets [(dicionario do widget, indice da pagina ou None)].
    """
    raiz = doc.root_object
    acro = raiz.get("/AcroForm")
    if acro is None:
        return []
    acro = acro.get_object()
    paginas = list(doc.pages)
    por_id = {}
    ref_pagina = {}
    for i, p in enumerate(paginas):
        if p.indirect_reference is not None:
            ref_pagina[p.indirect_reference.idnum] = i
        for a in (p.get("/Annots") or []):
            if hasattr(a, "idnum"):
                por_id[a.idnum] = i
            else:
                por_id[("direto", id(a))] = i

    def pagina_do_widget(ref, w):
        chave = ref.idnum if hasattr(ref, "idnum") else ("direto", id(ref))
        if chave in por_id:
            return por_id[chave]
        p = w.get("/P")
        if p is not None and hasattr(p, "idnum"):
            return ref_pagina.get(p.idnum)
        return None

    campos = []
    vistos = set()

    def visitar(ref, prefixo):
        chave = ref.idnum if hasattr(ref, "idnum") else ("direto", id(ref))
        if chave in vistos:
            return
        vistos.add(chave)
        no = ref.get_object()
        t = no.get("/T")
        nome = (f"{prefixo}.{t}" if prefixo and t is not None
                else (str(t) if t is not None else prefixo))
        filhos = [k for k in (no.get("/Kids") or []) if "/T" in k.get_object()]
        so_widgets = [k for k in (no.get("/Kids") or []) if "/T" not in k.get_object()]
        for f in filhos:
            visitar(f, nome)
        if filhos and not so_widgets:
            return
        if so_widgets:
            widgets = so_widgets
        elif no.get("/Subtype") == "/Widget" or "/Rect" in no:
            widgets = [ref]
        else:
            widgets = []
        ft = herdado(no, "/FT")
        ff = int(herdado(no, "/Ff") or 0)
        campos.append({
            "nome": nome or "(sem nome)",
            "tipo": tipo_do_campo(str(ft) if ft is not None else None, ff),
            "no": no, "ff": ff,
            "widgets": [(w.get_object(), pagina_do_widget(w, w.get_object())) for w in widgets],
        })

    for ref in (acro.get("/Fields") or []):
        visitar(ref, "")
    return campos
