"""Peças comuns dos scripts de docx do Soft Office.

Abre um .docx (zip) ou uma pasta já desempacotada, entrega o XML de cada
parte como árvore lxml e grava de volta, seja num .docx novo, seja na
própria pasta. Também cuida de relações e tipos de conteúdo.

Não é chamado direto pela linha de comando.
"""

import os
import sys
import tempfile
import zipfile

try:
    from lxml import etree
except ImportError:  # pragma: no cover
    sys.stderr.write("Falta a biblioteca lxml. Instale com: pip install lxml\n")
    sys.exit(3)

# Códigos de saída combinados no contrato.
SAIDA_OK = 0
SAIDA_REPROVOU = 1
SAIDA_ARGUMENTO = 2
SAIDA_FALTA = 3
SAIDA_EXTERNO = 4

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
}
W = NS["w"]
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


def w(nome):
    """Nome qualificado no espaço w: ('t' vira '{...main}t')."""
    return "{%s}%s" % (W, nome)


def qn(prefixado):
    """'w14:paraId' vira o nome qualificado lxml."""
    prefixo, nome = prefixado.split(":")
    return "{%s}%s" % (NS[prefixo], nome)


def nome_local(el):
    tag = el.tag
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1]


def espaco(el):
    tag = el.tag
    if not isinstance(tag, str) or not tag.startswith("{"):
        return ""
    return tag[1:].split("}", 1)[0]


def falhar(msg, codigo):
    sys.stderr.write(msg.rstrip("\n") + "\n")
    sys.exit(codigo)


_PARSER = etree.XMLParser(
    resolve_entities=False, no_network=True, huge_tree=True, remove_blank_text=False
)


def ler_xml(dados, nome="parte"):
    try:
        return etree.fromstring(dados, _PARSER)
    except etree.XMLSyntaxError as erro:
        falhar("XML mal formado em %s: %s" % (nome, erro), SAIDA_FALTA)


def serializar(raiz):
    return etree.tostring(raiz, xml_declaration=True, encoding="UTF-8", standalone=True)


class Pacote:
    """Um .docx aberto, vindo de zip ou de pasta desempacotada."""

    def __init__(self, caminho):
        self.caminho = caminho
        self.eh_pasta = os.path.isdir(caminho)
        self.ordem = []
        self.dados = {}
        self.infos = {}
        self._arvores = {}
        self._retrato = {}
        if not os.path.exists(caminho):
            falhar("Arquivo não encontrado: %s" % caminho, SAIDA_FALTA)
        if self.eh_pasta:
            self._ler_pasta()
        else:
            self._ler_zip()
        if "[Content_Types].xml" not in self.dados:
            falhar("%s não parece um documento do Word: falta [Content_Types].xml" % caminho, SAIDA_FALTA)
        if "word/document.xml" not in self.dados:
            falhar("%s não parece um documento do Word: falta word/document.xml" % caminho, SAIDA_FALTA)

    def _ler_zip(self):
        if not zipfile.is_zipfile(self.caminho):
            falhar("%s não é um .docx válido (não abre como zip)" % self.caminho, SAIDA_FALTA)
        try:
            with zipfile.ZipFile(self.caminho) as z:
                for info in z.infolist():
                    nome = info.filename
                    if nome in self.dados:
                        continue
                    self.ordem.append(nome)
                    self.infos[nome] = info
                    self.dados[nome] = z.read(info)
        except (zipfile.BadZipFile, OSError) as erro:
            falhar("Não consegui ler %s: %s" % (self.caminho, erro), SAIDA_FALTA)

    def _ler_pasta(self):
        base = os.path.abspath(self.caminho)
        for raiz, pastas, arquivos in os.walk(base, followlinks=False):
            pastas[:] = sorted(p for p in pastas if not os.path.islink(os.path.join(raiz, p)))
            for arq in sorted(arquivos):
                completo = os.path.join(raiz, arq)
                if os.path.islink(completo):
                    continue
                rel = os.path.relpath(completo, base).replace(os.sep, "/")
                with open(completo, "rb") as f:
                    self.dados[rel] = f.read()
                self.ordem.append(rel)

    # partes ---------------------------------------------------------------

    def existe(self, nome):
        return nome in self.dados or nome in self._arvores

    def xml(self, nome):
        """Árvore da parte (lida uma vez só; volta para o pacote ao gravar)."""
        if nome not in self._arvores:
            if nome not in self.dados:
                raise KeyError(nome)
            raiz = ler_xml(self.dados[nome], nome)
            self._arvores[nome] = raiz
            self._retrato[nome] = serializar(raiz)
        return self._arvores[nome]

    def novo_xml(self, nome, raiz):
        if nome not in self.dados and nome not in self.ordem:
            self.ordem.append(nome)
        self.dados.setdefault(nome, b"")
        self._arvores[nome] = raiz

    def partes_wordml(self):
        """Partes XML dentro de word/ cuja raiz está no espaço w (texto, cabeçalho, notas...)."""
        saida = []
        for nome in self.ordem:
            if not nome.startswith("word/") or not nome.endswith(".xml") or "/_rels/" in nome:
                continue
            raiz = self.xml(nome)
            if espaco(raiz) == W:
                saida.append(nome)
        return saida

    # relações e tipos -------------------------------------------------------

    @staticmethod
    def caminho_rels(parte):
        pasta, arq = parte.rsplit("/", 1) if "/" in parte else ("", parte)
        return (pasta + "/" if pasta else "") + "_rels/" + arq + ".rels"

    def relacoes(self, parte):
        nome = self.caminho_rels(parte)
        if not self.existe(nome):
            raiz = etree.Element("{%s}Relationships" % NS["pr"], nsmap={None: NS["pr"]})
            self.novo_xml(nome, raiz)
        return self.xml(nome)

    def alvo_por_tipo(self, parte, tipo):
        """Caminho da parte ligada a 'parte' pela relação 'tipo', ou None."""
        nome = self.caminho_rels(parte)
        if not self.existe(nome):
            return None
        pasta = parte.rsplit("/", 1)[0] if "/" in parte else ""
        for rel in self.xml(nome):
            if rel.get("Type") == tipo and rel.get("TargetMode") != "External":
                alvo = rel.get("Target", "")
                if alvo.startswith("/"):
                    return alvo.lstrip("/")
                return os.path.normpath(os.path.join(pasta, alvo)).replace(os.sep, "/")
        return None

    def ligar(self, parte, tipo, alvo_relativo):
        raiz = self.relacoes(parte)
        usados = {rel.get("Id") for rel in raiz}
        n = 1
        while "rId%d" % n in usados:
            n += 1
        rel = etree.SubElement(raiz, "{%s}Relationship" % NS["pr"])
        rel.set("Id", "rId%d" % n)
        rel.set("Type", tipo)
        rel.set("Target", alvo_relativo)
        return "rId%d" % n

    def declarar_tipo(self, parte, tipo):
        raiz = self.xml("[Content_Types].xml")
        nome = "/" + parte
        for el in raiz:
            if el.get("PartName") == nome:
                el.set("ContentType", tipo)
                return
        el = etree.SubElement(raiz, "{%s}Override" % NS["ct"])
        el.set("PartName", nome)
        el.set("ContentType", tipo)

    # gravação -----------------------------------------------------------------

    def _bytes_finais(self):
        self.alteradas = []
        for nome, raiz in self._arvores.items():
            novo = serializar(raiz)
            if self._retrato.get(nome) == novo:
                continue  # parte lida e não mexida: fica com os bytes originais
            self.dados[nome] = novo
            self.alteradas.append(nome)
        nomes = list(self.ordem)
        if "[Content_Types].xml" in nomes:
            nomes.remove("[Content_Types].xml")
            nomes.insert(0, "[Content_Types].xml")
        return nomes

    def gravar(self, destino=None):
        """Grava num .docx (destino) ou, sem destino e vindo de pasta, na própria pasta."""
        nomes = self._bytes_finais()
        if destino is None:
            if not self.eh_pasta:
                raise ValueError("destino obrigatório para entrada .docx")
            base = os.path.abspath(self.caminho)
            for nome in self.alteradas:
                completo = os.path.normpath(os.path.join(base, nome))
                if not completo.startswith(base + os.sep):
                    falhar("Caminho de parte fora da pasta: %s" % nome, SAIDA_FALTA)
                os.makedirs(os.path.dirname(completo), exist_ok=True)
                with open(completo, "wb") as f:
                    f.write(self.dados[nome])
            return
        pasta_destino = os.path.dirname(os.path.abspath(destino)) or "."
        if not os.path.isdir(pasta_destino):
            falhar("Pasta de saída não existe: %s" % pasta_destino, SAIDA_FALTA)
        fd, temporario = tempfile.mkstemp(suffix=".docx", dir=pasta_destino)
        os.close(fd)
        try:
            with zipfile.ZipFile(temporario, "w", zipfile.ZIP_DEFLATED) as z:
                for nome in nomes:
                    if nome.endswith("/"):
                        continue
                    info = zipfile.ZipInfo(nome, date_time=(1980, 1, 1, 0, 0, 0))
                    original = self.infos.get(nome)
                    if original is not None:
                        info.date_time = original.date_time
                    info.compress_type = zipfile.ZIP_DEFLATED
                    z.writestr(info, self.dados[nome])
            os.replace(temporario, destino)
        finally:
            if os.path.exists(temporario):
                os.remove(temporario)


def abrir_ou_sair(entrada, saida):
    """Valida a combinação entrada/saída do contrato e abre o pacote."""
    if not os.path.exists(entrada):
        falhar("Arquivo não encontrado: %s" % entrada, SAIDA_FALTA)
    if not os.path.isdir(entrada) and not saida:
        falhar("Informe a saída com -o SAIDA.docx", SAIDA_ARGUMENTO)
    if saida and os.path.isdir(saida):
        falhar("A saída precisa ser um arquivo .docx, não uma pasta: %s" % saida, SAIDA_ARGUMENTO)
    return Pacote(entrada)


def texto_visivel(raiz):
    """Texto de uma parte como o leitor vê: w:t e w:delText em ordem, sem marcação."""
    pedacos = []
    for el in raiz.iter(w("t"), w("delText")):
        pedacos.append(el.text or "")
    return "".join(pedacos)
