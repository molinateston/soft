#!/usr/bin/env python3
"""
dps.py - monta, confere e lê o XML da NFS-e padrão nacional.

- montar_dps: ficha da empresa + ficha do cliente + dados da nota -> DPS (lxml)
- validar_dados: o que falta nas fichas (uma pergunta por vez) e os limites
- validar_estrutura: Id de 45 caracteres, namespace em todo nível, sem prefixo,
  ordem, formato e as regras oficiais que a skill aplica antes do envio
- ler_nfse: leitor do XML autorizado, qualificando o namespace em CADA nível

Versão do leiaute: NFSE_VERSAO_DPS (1.00 padrão, como o guia de origem; 1.01 é a
do pacote oficial vigente). O grupo IBS/CBS não é gerado em nenhuma das duas.
Os valores aceitos estão em references/fluxo-e-campos.md.
"""
import datetime as dt
import os
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from lxml import etree

NS = "http://www.sped.fazenda.gov.br/nfse"
DS = "http://www.w3.org/2000/09/xmldsig#"
NSMAP = {"n": NS}
VERSOES = ("1.00", "1.01")
VER_APLIC = "nfse-emissao-1.0"
TP_AMB = {"producao": "1", "restrita": "2"}
AMB_DE_TP = {v: k for k, v in TP_AMB.items()}
RET_ISS = {1: "não retido", 2: "retido pelo tomador", 3: "retido pelo intermediário"}
SERIE_MAX = 49999
LIMITE_DESCRICAO = 2000
ORDEM_INFDPS = ["tpAmb", "dhEmi", "verAplic", "serie", "nDPS", "dCompet", "tpEmit",
                "cLocEmi", "prest", "toma", "serv", "valores"]
FORA_DA_SKILL = "Esse caso fica fora desta skill. Encaminhe ao contador ou emita pelo portal nacional."


def versao_dps():
    v = os.environ.get("NFSE_VERSAO_DPS", "1.00").strip() or "1.00"
    if v not in VERSOES:
        raise ValueError(f"NFSE_VERSAO_DPS só aceita {' ou '.join(VERSOES)} (veio {v!r})")
    return v


def parser_seguro():
    return etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=False,
                           remove_blank_text=False)


# ------------------------------------------------------------------ documentos

def limpo(v):
    """Texto da ficha sem espaço nas pontas; marcador de modelo (<...>) conta como vazio."""
    t = str(v if v is not None else "").strip()
    return "" if re.fullmatch(r"<[^<>]*>", t) else t


def so_digitos(v):
    return re.sub(r"\D", "", limpo(v))


def doc_limpo(v):
    """CNPJ pode ter letras (CNPJ alfanumérico); tira pontuação e sobe a caixa."""
    return re.sub(r"[^0-9A-Za-z]", "", limpo(v)).upper()


def _dv_mod11(base, pesos):
    s = sum((ord(c) - 48) * p for c, p in zip(base, pesos))
    r = s % 11
    return "0" if r < 2 else str(11 - r)


def cnpj_valido(c):
    c = doc_limpo(c)
    if not re.fullmatch(r"[0-9A-Z]{12}[0-9]{2}", c) or len(set(c)) == 1:
        return False
    p1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    d1 = _dv_mod11(c[:12], p1)
    d2 = _dv_mod11(c[:12] + d1, [6] + p1)
    return c[12:] == d1 + d2


def cpf_valido(c):
    c = so_digitos(c)
    if len(c) != 11 or len(set(c)) == 1:
        return False
    for n in (9, 10):
        s = sum(int(c[i]) * (n + 1 - i) for i in range(n))
        if (s * 10) % 11 % 10 != int(c[n]):
            return False
    return True


def dinheiro(v):
    """'700', '700,00', 'R$ 1.234,50', 700.0 -> Decimal('700.00'). Erro se inválido."""
    t = limpo(v).replace("R$", "").replace(" ", "")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        d = Decimal(t)
    except InvalidOperation:
        raise ValueError(f"valor inválido: {v!r}") from None
    if d != d.quantize(Decimal("0.01")):
        raise ValueError(f"valor com mais de 2 casas decimais: {v!r}")
    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def percentual(v):
    d = dinheiro(v)
    if d < 0 or d >= 100:
        raise ValueError(f"percentual fora de 0 a 99,99: {v!r}")
    return d


def competencia(v, hoje=None):
    """'2026-09' -> 2026-09-01; '2026-09-15' fica igual. Recusa data futura (E0015)."""
    t = limpo(v)
    if re.fullmatch(r"\d{4}-\d{2}", t):
        t += "-01"
    try:
        d = dt.date.fromisoformat(t)
    except ValueError:
        raise ValueError(f"competência inválida: {v!r} (use AAAA-MM ou AAAA-MM-DD)") from None
    hoje = hoje or dt.date.today()
    if d > hoje:
        raise ValueError(f"competência {d.isoformat()} está no futuro")
    return d


# ------------------------------------------------------------------ fichas

PERGUNTAS = {
    "empresa.cnpj": "Qual o CNPJ da sua empresa (14 caracteres)?",
    "empresa.municipio_ibge": "Qual o código IBGE do município da sua empresa (7 dígitos)?",
    "empresa.opSimpNac": "Qual a situação da empresa no Simples Nacional (opSimpNac), conforme "
                         "o contador? Esta skill cobre só ME/EPP, que é o código 3.",
    "empresa.regApTribSN": "Qual o regime de apuração no Simples (regApTribSN) que o contador "
                           "indica? Esta skill cobre o código 1.",
    "empresa.regEspTrib": "A empresa tem regime especial de tributação (regEspTrib)? Para ME/EPP "
                          "com apuração 1 as regras oficiais pedem 0; confirme com o contador.",
    "empresa.serie_dps": "Qual série de DPS a empresa vai usar (de 1 a 49999)?",
    "empresa.tributos_aproximados": "Quais os percentuais aproximados de tributos federais, "
                                    "estaduais e municipais que o contador indica para a nota?",
    "cliente.documento": "Qual o CNPJ ou CPF do cliente?",
    "cliente.nome": "Qual a razão social (ou nome completo) do cliente?",
    "cliente.cep": "Qual o CEP do cliente (8 dígitos)?",
    "cliente.municipio_ibge": "Qual o código IBGE do município do cliente (7 dígitos)?",
    "cliente.logradouro": "Qual o logradouro (rua, avenida) do cliente?",
    "cliente.numero": "Qual o número do endereço do cliente? Sem número, use S/N.",
    "cliente.bairro": "Qual o bairro do cliente?",
    "cliente.cTribNac": "Qual o código de tributação nacional do serviço (cTribNac, 6 dígitos)? "
                        "Esse código vem do contador.",
    "cliente.cLocPrestacao": "Qual o código IBGE do município onde o serviço foi prestado?",
    "cliente.tribISSQN": "Qual a tributação do ISS dessa nota (tribISSQN), conforme o contador? "
                         "Esta skill monta só operação tributável, código 1.",
    "cliente.tpRetISSQN": "O ISS dessa nota é retido? Use o que o contador orientou: "
                          "1 não retido, 2 retido pelo tomador, 3 retido pelo intermediário.",
    "nota.valor": "Qual o valor da nota em reais?",
    "nota.competencia": "Qual o mês de competência do serviço (AAAA-MM)?",
    "nota.descricao": "Qual a descrição do serviço que vai na nota?",
}


def _int(v):
    try:
        return int(limpo(v))
    except (TypeError, ValueError):
        return None


def validar_dados(empresa, cliente, nota, hoje=None):
    """Lista de (campo, problema, pergunta). Vazia quando dá pra montar o DPS.
    Item com campo 'LIMITE' manda parar: o caso fica fora da skill."""
    p = []

    def falta(campo, problema):
        p.append((campo, problema, PERGUNTAS.get(campo, problema)))

    def limite(problema):
        p.append(("LIMITE", problema, FORA_DA_SKILL))

    if not cnpj_valido(empresa.get("cnpj")):
        falta("empresa.cnpj", "CNPJ da empresa ausente ou com dígito inválido")
    if not re.fullmatch(r"\d{7}", so_digitos(empresa.get("municipio_ibge"))):
        falta("empresa.municipio_ibge", "código IBGE do município da empresa ausente")
    sn = empresa.get("simples_nacional") or {}
    op = _int(sn.get("opSimpNac"))
    if op is None:
        falta("empresa.opSimpNac", "opSimpNac ausente")
    elif op != 3:
        limite(f"opSimpNac={op}: esta skill cobre só Simples Nacional ME/EPP (opSimpNac 3). "
               "MEI, não optante e outros regimes ficam fora.")
    reg = _int(sn.get("regApTribSN"))
    if reg is None:
        falta("empresa.regApTribSN", "regApTribSN ausente")
    elif reg != 1:
        limite(f"regApTribSN={reg}: com ISS ou tributos federais apurados fora do Simples a nota "
               "pede alíquota e outros campos que esta skill não monta.")
    esp = _int(empresa.get("regEspTrib"))
    if esp is None:
        falta("empresa.regEspTrib", "regEspTrib ausente")
    elif esp != 0:
        limite(f"regEspTrib={esp}: para ME/EPP com regApTribSN 1 as regras oficiais pedem "
               "regime especial 0 (erro E0175).")
    serie = so_digitos(empresa.get("serie_dps"))
    if not serie or not (1 <= int(serie) <= SERIE_MAX):
        falta("empresa.serie_dps", "série do DPS ausente ou fora de 1 a 49999")
    tt = empresa.get("tributos_aproximados") or {}
    try:
        for k in ("pTotTribFed", "pTotTribEst", "pTotTribMun"):
            percentual(tt[k])
    except (KeyError, ValueError):
        falta("empresa.tributos_aproximados", "percentuais pTotTrib ausentes ou inválidos")

    doc = cliente.get("documento") or {}
    tipo = limpo(doc.get("tipo")).upper()
    num = doc.get("numero")
    if not ((tipo == "CNPJ" and cnpj_valido(num)) or (tipo == "CPF" and cpf_valido(num))):
        falta("cliente.documento", "CNPJ ou CPF do cliente ausente ou inválido")
    if not limpo(cliente.get("nome")):
        falta("cliente.nome", "nome do cliente ausente")
    end = cliente.get("endereco") or {}
    if not re.fullmatch(r"\d{8}", so_digitos(end.get("cep"))):
        falta("cliente.cep", "CEP do cliente ausente")
    if not re.fullmatch(r"\d{7}", so_digitos(end.get("municipio_ibge"))):
        falta("cliente.municipio_ibge", "código IBGE do município do cliente ausente")
    for k in ("logradouro", "numero", "bairro"):
        if not limpo(end.get(k)):
            falta(f"cliente.{k}", f"{k} do cliente ausente")
    serv = cliente.get("servico") or {}
    if not re.fullmatch(r"\d{6}", so_digitos(serv.get("cTribNac"))):
        falta("cliente.cTribNac", "cTribNac ausente (6 dígitos)")
    if not re.fullmatch(r"\d{7}", so_digitos(serv.get("cLocPrestacao"))):
        falta("cliente.cLocPrestacao", "código IBGE do local da prestação ausente")
    iss = cliente.get("iss") or {}
    trib = _int(iss.get("tribISSQN"))
    if trib is None:
        falta("cliente.tribISSQN", "tribISSQN ausente (o contador informa)")
    elif trib != 1:
        limite(f"tribISSQN={trib}: esta skill monta só operação tributável (1). Os códigos 2 a 4 "
               "mudam de significado entre as versões 1.00 e 1.01 do leiaute e pedem campos extras.")
    ret = _int(iss.get("tpRetISSQN"))
    if ret not in RET_ISS:
        falta("cliente.tpRetISSQN", "tpRetISSQN ausente (o contador informa)")
    elif ret != 1:
        limite(f"tpRetISSQN={ret}: com ISS retido as regras oficiais exigem a alíquota (pAliq), "
               "campo que esta skill não monta.")

    try:
        if dinheiro(nota.get("valor")) <= 0:
            raise ValueError("valor zero")
    except (ValueError, TypeError):
        falta("nota.valor", "valor ausente ou inválido")
    try:
        competencia(nota.get("competencia"), hoje)
    except ValueError as e:
        falta("nota.competencia", str(e))
    desc = descricao_final(cliente, nota)
    if not desc:
        falta("nota.descricao", "descrição do serviço ausente")
    elif len(desc) > LIMITE_DESCRICAO:
        falta("nota.descricao", f"descrição com {len(desc)} caracteres (limite da casa: "
              f"{LIMITE_DESCRICAO})")
    return p


def descricao_final(cliente, nota):
    base = limpo((cliente.get("servico") or {}).get("descricao_base"))
    mes = limpo(nota.get("descricao"))
    if mes and base:
        return f"{base} {mes}"
    return mes or base


# ------------------------------------------------------------------ montagem

def montar_id(cmun, tp_insc, inscricao, serie, ndps):
    i = (f"DPS{so_digitos(cmun).zfill(7)}{int(tp_insc)}{doc_limpo(inscricao).zfill(14)}"
         f"{so_digitos(serie).zfill(5)}{str(int(ndps)).zfill(15)}")
    if len(i) != 45:
        raise ValueError(f"Id do DPS com {len(i)} caracteres (precisa de 45)")
    return i


def _sub(pai, nome, texto=None):
    el = etree.SubElement(pai, f"{{{NS}}}{nome}")
    if texto is not None:
        el.text = str(texto)
    return el


def montar_dps(empresa, cliente, nota, amb, ndps, dh_emi, versao=None):
    """Devolve (raiz DPS, Id). Sem assinatura. dh_emi: datetime com fuso."""
    versao = versao or versao_dps()
    cmun = so_digitos(empresa["municipio_ibge"])
    cnpj = doc_limpo(empresa["cnpj"])
    serie = str(int(so_digitos(empresa["serie_dps"])))
    id_dps = montar_id(cmun, 2, cnpj, serie, ndps)

    raiz = etree.Element(f"{{{NS}}}DPS", nsmap={None: NS})
    raiz.set("versao", versao)
    inf = _sub(raiz, "infDPS")
    inf.set("Id", id_dps)
    _sub(inf, "tpAmb", TP_AMB[amb])
    _sub(inf, "dhEmi", dh_emi.isoformat(timespec="seconds"))
    _sub(inf, "verAplic", VER_APLIC)
    _sub(inf, "serie", serie)
    _sub(inf, "nDPS", str(int(ndps)))
    _sub(inf, "dCompet", competencia(nota["competencia"], dh_emi.date()).isoformat())
    _sub(inf, "tpEmit", "1")
    _sub(inf, "cLocEmi", cmun)

    prest = _sub(inf, "prest")
    _sub(prest, "CNPJ", cnpj)
    im = limpo(empresa.get("inscricao_municipal"))
    if im:
        _sub(prest, "IM", im)
    reg = _sub(prest, "regTrib")
    sn = empresa["simples_nacional"]
    _sub(reg, "opSimpNac", int(limpo(sn["opSimpNac"])))
    _sub(reg, "regApTribSN", int(limpo(sn["regApTribSN"])))
    _sub(reg, "regEspTrib", int(limpo(empresa["regEspTrib"])))

    toma = _sub(inf, "toma")
    doc = cliente["documento"]
    tipo = limpo(doc["tipo"]).upper()
    _sub(toma, tipo, doc_limpo(doc["numero"]) if tipo == "CNPJ" else so_digitos(doc["numero"]))
    _sub(toma, "xNome", limpo(cliente["nome"]))
    e = cliente["endereco"]
    end = _sub(toma, "end")
    en = _sub(end, "endNac")
    _sub(en, "cMun", so_digitos(e["municipio_ibge"]))
    _sub(en, "CEP", so_digitos(e["cep"]))
    _sub(end, "xLgr", limpo(e["logradouro"]))
    _sub(end, "nro", limpo(e["numero"]))
    if limpo(e.get("complemento")):
        _sub(end, "xCpl", limpo(e["complemento"]))
    _sub(end, "xBairro", limpo(e["bairro"]))

    serv = _sub(inf, "serv")
    loc = _sub(serv, "locPrest")
    s = cliente["servico"]
    _sub(loc, "cLocPrestacao", so_digitos(s["cLocPrestacao"]))
    cserv = _sub(serv, "cServ")
    _sub(cserv, "cTribNac", so_digitos(s["cTribNac"]))
    _sub(cserv, "xDescServ", descricao_final(cliente, nota))

    val = _sub(inf, "valores")
    vsp = _sub(val, "vServPrest")
    _sub(vsp, "vServ", f"{dinheiro(nota['valor']):.2f}")
    trib = _sub(val, "trib")
    tm = _sub(trib, "tribMun")
    iss = cliente["iss"]
    _sub(tm, "tribISSQN", int(limpo(iss["tribISSQN"])))
    _sub(tm, "tpRetISSQN", int(limpo(iss["tpRetISSQN"])))
    tot = _sub(trib, "totTrib")
    pt = _sub(tot, "pTotTrib")
    tt = empresa["tributos_aproximados"]
    for k in ("pTotTribFed", "pTotTribEst", "pTotTribMun"):
        _sub(pt, k, f"{percentual(tt[k]):.2f}")
    return raiz, id_dps


def serializar(raiz):
    return etree.tostring(raiz, xml_declaration=True, encoding="UTF-8")


# ------------------------------------------------------------------ estrutura

FORMATOS = {
    "n:tpAmb": r"[12]",
    "n:dhEmi": r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}",
    "n:verAplic": r".{1,20}",
    "n:serie": r"[1-9]\d{0,4}",
    "n:nDPS": r"[1-9]\d{0,14}",
    "n:dCompet": r"\d{4}-\d{2}-\d{2}",
    "n:tpEmit": r"1",
    "n:cLocEmi": r"\d{7}",
    "n:prest/n:CNPJ": r"[0-9A-Z]{12}\d{2}",
    "n:prest/n:regTrib/n:opSimpNac": r"[123]",
    "n:prest/n:regTrib/n:regEspTrib": r"[0-69]",
    "n:serv/n:locPrest/n:cLocPrestacao": r"\d{7}",
    "n:serv/n:cServ/n:cTribNac": r"\d{6}",
    "n:serv/n:cServ/n:xDescServ": r"(?s).{1,2000}",
    "n:valores/n:vServPrest/n:vServ": r"\d{1,13}\.\d{2}",
    "n:valores/n:trib/n:tribMun/n:tribISSQN": r"[1-4]",
    "n:valores/n:trib/n:tribMun/n:tpRetISSQN": r"[1-3]",
    "n:valores/n:trib/n:totTrib/n:pTotTrib/n:pTotTribFed": r"\d{1,2}\.\d{2}",
    "n:valores/n:trib/n:totTrib/n:pTotTrib/n:pTotTribEst": r"\d{1,2}\.\d{2}",
    "n:valores/n:trib/n:totTrib/n:pTotTrib/n:pTotTribMun": r"\d{1,2}\.\d{2}",
}
FORMATOS_TOMADOR = {
    "n:toma/n:xNome": r".+",
    "n:toma/n:end/n:endNac/n:cMun": r"\d{7}",
    "n:toma/n:end/n:endNac/n:CEP": r"\d{8}",
    "n:toma/n:end/n:xLgr": r".+",
    "n:toma/n:end/n:nro": r".+",
    "n:toma/n:end/n:xBairro": r".+",
}


def prefixos(raiz):
    """Problemas de prefixo de namespace no XML inteiro (o leiaute pede nenhum, E1228)."""
    out = []
    for el in raiz.iter(etree.Element):
        if el.prefix is not None:
            out.append(f"elemento com prefixo de namespace: {el.prefix}:{etree.QName(el).localname}")
        if any(k is not None for k in (el.nsmap or {})):
            decl = [k for k in el.nsmap if k is not None]
            out.append(f"declaração de prefixo em {etree.QName(el).localname}: {decl}")
        for nome in el.attrib:
            if nome.startswith("{"):
                out.append(f"atributo com namespace em {etree.QName(el).localname}: {nome}")
    return sorted(set(out))


def validar_estrutura(raiz, versao=None):
    """Lista de problemas do DPS montado. Vazia = estrutura conferida."""
    erros = []
    versao = versao or versao_dps()
    if raiz.tag != f"{{{NS}}}DPS":
        return [f"raiz {raiz.tag} (esperado DPS no namespace {NS})"]
    if raiz.get("versao") != versao:
        erros.append(f"versao do DPS {raiz.get('versao')!r} (configurada {versao})")
    erros += prefixos(raiz)
    for el in raiz.iter(etree.Element):
        dentro_ds = etree.QName(el).namespace == DS or any(
            etree.QName(a).namespace == DS for a in el.iterancestors())
        if not dentro_ds and etree.QName(el).namespace != NS:
            erros.append(f"elemento fora do namespace da NFS-e: {el.tag}")
    inf = raiz.find(f"{{{NS}}}infDPS")
    if inf is None:
        return erros + ["infDPS ausente"]
    formatos = dict(FORMATOS)
    if inf.find(f"{{{NS}}}toma") is not None:
        formatos.update(FORMATOS_TOMADOR)
        if len(inf.xpath("n:toma/n:CNPJ|n:toma/n:CPF", namespaces=NSMAP)) != 1:
            erros.append("tomador presente precisa de exatamente um CNPJ ou CPF")
    for caminho, rx in formatos.items():
        r = inf.xpath(caminho, namespaces=NSMAP)
        if not r:
            erros.append(f"campo obrigatório ausente: {caminho.replace('n:', '')}")
        elif not re.fullmatch(rx, (r[0].text or "")):
            erros.append(f"formato inválido em {caminho.replace('n:', '')}: {r[0].text!r}")
    serie = _txt(inf, "n:serie")
    if serie and serie.isdigit() and int(serie) > SERIE_MAX:
        erros.append(f"série {serie} acima de {SERIE_MAX} (E0010)")
    if _txt(inf, "n:prest/n:regTrib/n:opSimpNac") == "3" and \
            not inf.xpath("n:prest/n:regTrib/n:regApTribSN", namespaces=NSMAP):
        erros.append("ME/EPP sem regApTribSN (E0166)")
    if versao == "1.00" and inf.find(f"{{{NS}}}IBSCBS") is not None:
        erros.append("grupo IBSCBS só existe na versão 1.01 (E0854)")
    filhos = [etree.QName(c).localname for c in inf]
    if filhos != [n for n in ORDEM_INFDPS if n in filhos] or set(filhos) - set(ORDEM_INFDPS):
        erros.append(f"ordem ou bloco de infDPS fora do leiaute montado: {filhos}")
    i = inf.get("Id") or ""
    if len(i) != 45 or not re.fullmatch(r"DPS\d{7}[12][0-9A-Z]{14}\d{20}", i):
        erros.append(f"Id do DPS inválido ({len(i)} caracteres): {i!r}")
    else:
        try:
            esperado = montar_id(_txt(inf, "n:cLocEmi"), 2, _txt(inf, "n:prest/n:CNPJ"),
                                 _txt(inf, "n:serie"), _txt(inf, "n:nDPS"))
            if esperado != i:
                erros.append(f"Id não bate com os campos: {i} x {esperado}")
        except (TypeError, ValueError):
            erros.append("Id não pôde ser recomposto a partir dos campos")
    return erros


def _txt(no, caminho):
    r = no.xpath(caminho, namespaces=NSMAP)
    if not r:
        return None
    v = r[0]
    return (v.text or "").strip() if hasattr(v, "text") else str(v).strip()


def decompor_id(i):
    return {"prefixo": i[:3], "municipio": i[3:10], "tipo_inscricao": i[10],
            "inscricao": i[11:25], "serie": i[25:30], "numero": i[30:45]}


# ------------------------------------------------------------------ leitura

def ler_nfse(xml):
    """Lê o XML autorizado com o namespace qualificado em TODOS os níveis.
    Devolve dict com os campos que o relato e o PDF usam."""
    raiz = etree.fromstring(xml, parser_seguro())
    infs = raiz.xpath("//n:infNFSe", namespaces=NSMAP)
    if not infs:
        raise ValueError("o XML não traz infNFSe no namespace da NFS-e")
    inf = infs[0]
    dps = inf.xpath("n:DPS/n:infDPS", namespaces=NSMAP)
    dps = dps[0] if dps else None
    ident = inf.get("Id") or ""
    chave = ident[3:] if ident.startswith("NFS") else ident

    def d(caminho):
        return _txt(dps, caminho) if dps is not None else None

    return {
        "chave": chave,
        "numero": _txt(inf, "n:nNFSe"),
        "municipio_emissor": _txt(inf, "n:xLocEmi"),
        "local_prestacao": _txt(inf, "n:xLocPrestacao"),
        "trib_nacional_desc": _txt(inf, "n:xTribNac"),
        "processada_em": _txt(inf, "n:dhProc"),
        "ambiente_gerador": _txt(inf, "n:ambGer"),
        "situacao": _txt(inf, "n:cStat"),
        "prestador_cnpj": _txt(inf, "n:emit/n:CNPJ") or d("n:prest/n:CNPJ"),
        "prestador_nome": _txt(inf, "n:emit/n:xNome"),
        "prestador_im": _txt(inf, "n:emit/n:IM") or d("n:prest/n:IM"),
        "tomador_doc": d("n:toma/n:CNPJ") or d("n:toma/n:CPF"),
        "tomador_nome": d("n:toma/n:xNome"),
        "valor_servico": d("n:valores/n:vServPrest/n:vServ"),
        "valor_liquido": _txt(inf, "n:valores/n:vLiq"),
        "valor_iss": _txt(inf, "n:valores/n:vISSQN"),
        "retencao_iss": d("n:valores/n:trib/n:tribMun/n:tpRetISSQN"),
        "descricao": d("n:serv/n:cServ/n:xDescServ"),
        "cTribNac": d("n:serv/n:cServ/n:cTribNac"),
        "competencia": d("n:dCompet"),
        "tpAmb": d("n:tpAmb"),
        "id_dps": dps.get("Id") if dps is not None else None,
    }


def ler_ingenuo(xml):
    """O erro da lição do namespace, de propósito: qualifica só o primeiro nível.
    Existe para o autoteste mostrar que este caminho devolve vazio."""
    raiz = etree.fromstring(xml, parser_seguro())
    inf = raiz.find(f"{{{NS}}}infNFSe")
    if inf is None:
        return {"prestador_cnpj": None, "tomador_nome": None, "valor_servico": None}

    def t(c):
        el = inf.find(c)
        return el.text if el is not None else None
    return {"prestador_cnpj": t("emit/CNPJ"),
            "tomador_nome": t("DPS/infDPS/toma/xNome"),
            "valor_servico": t("DPS/infDPS/valores/vServPrest/vServ")}
