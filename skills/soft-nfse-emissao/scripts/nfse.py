#!/usr/bin/env python3
"""
nfse.py - emissão de NFS-e padrão nacional em dois passos, com portões.

Rode a partir da pasta da skill. Toda chamada exige NFSE_DADOS_DIR, fora da skill.

  iniciar                               cria a pasta de dados e as fichas-modelo
  conferir [--cliente X]                o que falta nas fichas, uma pergunta por vez
  certificado                           validade do .pfx (aviso com 30 dias ou menos)
  palavra-passe --definir|--trocar|--status
  contador [--ajustar N] [--producao]   mostra ou sobe o último número de DPS usado
  preparar --cliente X --valor V --competencia AAAA-MM [--descricao T] [--producao]
  emitir --hash H [--producao] [--palavra-passe-stdin]
  consultar --dps ID | --chave C [--producao]
  resolver --dps ID --sem-nota [--producao]
  eventos --chave C [--producao]
  pdf --xml ARQ [--saida ARQ.pdf]
  ler --xml ARQ

Ambiente padrão: produção restrita (tpAmb 2). Produção só com NFSE_AMBIENTE=producao
E a flag --producao, juntas.

Saída: 0 ok | 1 erro | 2 recusa de guarda ou limite | 3 falta dado | 4 dependência
ausente | 5 rejeitada pelo servidor | 6 envio incerto ou consulta inconclusiva |
7 não enviado (conexão não abriu)
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import cofre  # noqa: E402
from cofre import Recusa  # noqa: E402

try:
    from lxml import etree  # noqa: E402
    import assinatura  # noqa: E402
    import cliente_sefin  # noqa: E402
    import danfse  # noqa: E402
    import dps  # noqa: E402
except ImportError as _e:
    print(f"DEPENDÊNCIA AUSENTE: {_e.name}. Rode: python3 scripts/checar_dependencias.py",
          file=sys.stderr)
    sys.exit(4)

VALIDADE_RASCUNHO = dt.timedelta(hours=12)
RECUO_DHEMI = dt.timedelta(seconds=60)
NOME_AMB = {"restrita": "produção restrita (teste, sem validade jurídica)",
            "producao": "PRODUÇÃO (nota com valor fiscal)"}
CODIGOS_EVENTO = {"101101": "cancelamento", "105102": "cancelamento por substituição"}
ID_DPS_RE = r"DPS\d{7}[12][0-9A-Z]{14}\d{20}"

MODELO_EMPRESA = {
    "_leia": "Ficha da empresa emissora. Troque cada <marcador> pelo dado real. Regime, "
             "código de serviço e retenção vêm do contador; a skill não adivinha.",
    "razao_social": "<razão social da empresa>",
    "cnpj": "<CNPJ da empresa, 14 caracteres>",
    "inscricao_municipal": "<inscrição municipal, se o município usar>",
    "municipio_ibge": "<código IBGE do município da empresa, 7 dígitos>",
    "simples_nacional": {"opSimpNac": "<3 para ME/EPP, confirme com o contador>",
                         "regApTribSN": "<1 quando tudo é apurado no Simples, o contador confirma>"},
    "regEspTrib": "<0 quando não há regime especial>",
    "serie_dps": "<série do DPS, de 1 a 49999>",
    "tributos_aproximados": {"pTotTribFed": "<percentual federal>",
                             "pTotTribEst": "<percentual estadual>",
                             "pTotTribMun": "<percentual municipal>"},
    "exigir_palavra_passe": True,
}
MODELO_CLIENTE = {
    "_leia": "Ficha de um cliente. Salve uma cópia como clientes/<apelido>.json (apelido em "
             "minúsculas, sem espaço). Troque cada <marcador> pelo dado real.",
    "nome": "<razão social ou nome completo do cliente>",
    "documento": {"tipo": "<CNPJ ou CPF>", "numero": "<número do documento>"},
    "endereco": {"cep": "<CEP, 8 dígitos>",
                 "municipio_ibge": "<código IBGE do município do cliente, 7 dígitos>",
                 "logradouro": "<rua ou avenida>", "numero": "<número ou S/N>",
                 "complemento": "<complemento, opcional>", "bairro": "<bairro>"},
    "servico": {"cTribNac": "<código de tributação nacional, 6 dígitos, o contador informa>",
                "cLocPrestacao": "<código IBGE do município da prestação>",
                "descricao_base": "<texto fixo da descrição, opcional>"},
    "iss": {"tribISSQN": "<1 para operação tributável, o contador confirma>",
            "tpRetISSQN": "<1 não retido, 2 retido pelo tomador, 3 retido pelo intermediário>"},
}


# ------------------------------------------------------------------ apoio

def ambiente(a):
    env = (os.environ.get("NFSE_AMBIENTE") or "restrita").strip().lower()
    if env not in ("restrita", "producao"):
        raise Recusa("NFSE_AMBIENTE só aceita restrita ou producao.")
    flag = bool(getattr(a, "producao", False))
    if env == "producao" and not flag:
        raise Recusa("NFSE_AMBIENTE=producao, mas o comando veio sem --producao. Produção "
                     "exige as duas coisas juntas; nada foi feito.")
    if flag and env != "producao":
        raise Recusa("o comando pediu --producao, mas NFSE_AMBIENTE não é producao. Produção "
                     "exige as duas coisas juntas; nada foi feito.")
    return env


def flag_amb(amb):
    return " --producao" if amb == "producao" else ""


def carregar_empresa(dados):
    arq = dados / "empresa.json"
    if not arq.is_file():
        raise Recusa("falta a ficha da empresa (empresa.json). Rode: python3 scripts/nfse.py iniciar")
    return cofre.ler_json(arq)


def carregar_cliente(dados, apelido):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,60}", apelido or ""):
        raise Recusa("apelido de cliente só com letras minúsculas, números, hífen e sublinhado.")
    arq = dados / "clientes" / f"{apelido}.json"
    if not arq.is_file():
        pasta = dados / "clientes"
        existentes = sorted(p.stem for p in pasta.glob("*.json") if not p.stem.startswith("_"))
        raise Recusa(f"não achei a ficha do cliente {apelido}. Fichas existentes: "
                     f"{', '.join(existentes) or 'nenhuma'}. Modelo em clientes/_modelo.json.")
    return cofre.ler_json(arq)


def pendencias_do(dados, amb):
    return [(p, e) for p, e in cofre.pendencias(dados) if e.get("ambiente") == amb]


def msg_pendencias(pend):
    linhas = ["há envio sem desfecho conhecido neste ambiente. Nenhuma nota nova sai antes "
              "de resolver:"]
    for _, e in pend:
        linhas.append(f"  DPS {e.get('id_dps')} | cliente {e.get('cliente')} | "
                      f"{danfse.brl(e.get('valor'))} | status {e.get('status')}")
        linhas.append(f"  rode: python3 scripts/nfse.py consultar --dps {e.get('id_dps')}"
                      f"{flag_amb(e.get('ambiente'))}")
    return "\n".join(linhas)


def conferir_cnpj_certificado(cert, empresa):
    c = cofre.cnpj_do_certificado(cert)
    e = dps.doc_limpo(empresa.get("cnpj"))
    if not c:
        cofre.aviso("não achei o CNPJ dentro do certificado. As regras oficiais pedem a "
                    "assinatura com o certificado do emitente (E0718).")
        return
    if c == e:
        return
    if c[:8] == e[:8]:
        cofre.aviso(f"o certificado é do CNPJ {danfse.fmt_doc(c)}, da mesma raiz da empresa "
                    f"({danfse.fmt_doc(e)}). Caso de matriz e filial: confirme na produção restrita.")
        return
    raise Recusa(f"o certificado é do CNPJ {danfse.fmt_doc(c)} e a ficha da empresa é "
                 f"{danfse.fmt_doc(e)}. As regras oficiais pedem a assinatura com o certificado "
                 "do emitente (E0718). Nada foi enviado.")


def pasta_da_nota(dados, r):
    return (dados / "notas" / r["ambiente"] / r["competencia"][:7] /
            f"{r['cliente']}-s{r['serie']}-dps{r['nDPS']}")


def achar_nota(dados, amb, id_dps=None, chave=None):
    for arq in sorted((dados / "notas" / amb).glob("*/*/estado.json")):
        try:
            e = cofre.ler_json(arq)
        except Exception:
            continue
        if (id_dps and e.get("id_dps") == id_dps) or (chave and e.get("chave") == chave):
            return arq.parent, e
    return None, None


def guardar_bruto(dados, amb, nome, bruto):
    carimbo = cofre.agora().strftime("%Y%m%d-%H%M%S")
    return cofre.escrever_privado(dados / "notas" / amb / "respostas" / f"{nome}-{carimbo}.txt",
                                  bruto or b"")


def situacao_de(estado):
    return {"cancelada": estado.get("cancelada"), "substituida": estado.get("substituida"),
            "conferida_em": estado.get("eventos_conferidos_em")}


def gerar_pdf_da_pasta(nota_dir, info, estado):
    saida = nota_dir / "nfse.pdf"
    try:
        danfse.gerar_pdf(info, saida, situacao_de(estado or {}))
    except danfse.FaltaDependencia as e:
        return f"não gerado ({e})"
    os.chmod(saida, 0o600)
    return str(saida)


def relato_nota(titulo, nota_dir, info, amb, pdf_txt):
    print(f"{titulo} em {NOME_AMB[amb]}.")
    print(f"  número:           {info.get('numero')}")
    print(f"  chave de acesso:  {info.get('chave')}")
    print(f"  cliente:          {info.get('tomador_nome')} | valor "
          f"{danfse.brl(info.get('valor_servico'))}")
    print(f"  XML (documento fiscal): {nota_dir / 'nfse.xml'}")
    print(f"  PDF (representação):    {pdf_txt}")
    print(f"  consulta pública: {danfse.url_consulta(info.get('chave'))}")


def interpretar_eventos(j):
    """Eventos achados na resposta: XML compactado (e101101, e105102) ou código no JSON.
    O formato da resposta não foi conferido em nota real; o leitor é tolerante."""
    achados = {}

    def do_xml(xml):
        try:
            raiz = etree.fromstring(xml, dps.parser_seguro())
        except etree.XMLSyntaxError:
            return
        for el in raiz.iter(etree.Element):
            m = re.fullmatch(r"e(\d{6})", etree.QName(el).localname)
            if m:
                desc = (el.findtext(f"{{{dps.NS}}}xDesc") or "").strip()
                achados.setdefault(m.group(1), desc or CODIGOS_EVENTO.get(m.group(1), ""))

    def visitar(o):
        if isinstance(o, dict):
            for k, v in o.items():
                kl = k.lower()
                if isinstance(v, str) and "xml" in kl and len(v) > 20:
                    try:
                        do_xml(cliente_sefin.de_gz_b64(v))
                        continue
                    except Exception:
                        if v.lstrip().startswith("<"):
                            do_xml(v.encode("utf-8"))
                            continue
                if kl in ("tipoevento", "tpevento", "codigoevento") and str(v).strip().isdigit():
                    cod = str(v).strip()
                    achados.setdefault(cod, CODIGOS_EVENTO.get(cod, ""))
                    continue
                visitar(v)
        elif isinstance(o, list):
            for x in o:
                visitar(x)

    visitar(j)
    return [{"codigo": c, "descricao": d} for c, d in achados.items()]


def _vazio(j):
    if j in (None, [], {}):
        return True
    if isinstance(j, dict):
        return all(v in (None, [], {}, "") for v in j.values())
    return False


def limpar_rascunhos_vencidos(dados):
    base = dados / "rascunhos"
    if not base.is_dir():
        return
    for pasta in base.iterdir():
        try:
            r = cofre.ler_json(pasta / "resumo.json")
            if cofre.agora() - dt.datetime.fromisoformat(r["criado_em"]) > 2 * VALIDADE_RASCUNHO:
                shutil.rmtree(pasta, ignore_errors=True)
        except Exception:
            continue


# ------------------------------------------------------------------ comandos

def cmd_iniciar(a):
    dados = cofre.dados_dir()
    for sub in ("clientes", "notas", "rascunhos"):
        (dados / sub).mkdir(mode=0o700, exist_ok=True)
    criados = []
    if not (dados / "empresa.json").exists():
        cofre.gravar_json(dados / "empresa.json", MODELO_EMPRESA)
        criados.append("empresa.json")
    if not (dados / "clientes" / "_modelo.json").exists():
        cofre.gravar_json(dados / "clientes" / "_modelo.json", MODELO_CLIENTE)
        criados.append("clientes/_modelo.json")
    cofre.registrar(dados, "iniciou")
    print(f"Pasta de dados pronta: {dados}")
    print("Criados: " + (", ".join(criados) if criados else "nada (já existia tudo)"))
    print("Próximo passo: preencher empresa.json e salvar cada cliente como "
          "clientes/<apelido>.json a partir de clientes/_modelo.json. Depois: "
          "python3 scripts/nfse.py conferir")
    return 0


def cmd_conferir(a):
    dados = cofre.dados_dir()
    empresa = carregar_empresa(dados)
    cliente = carregar_cliente(dados, a.cliente) if a.cliente else {}
    hoje = cofre.agora().date()
    nota = {"valor": "1.00", "competencia": hoje.strftime("%Y-%m"), "descricao": "conferência"}
    probs = [p for p in dps.validar_dados(empresa, cliente, nota, hoje=hoje)
             if p[0] == "LIMITE" or p[0].startswith("empresa.")
             or (a.cliente and p[0].startswith("cliente."))]
    amb_env = (os.environ.get("NFSE_AMBIENTE") or "restrita").strip().lower()
    print(f"Pasta de dados: {dados}")
    print(f"Ambiente configurado: {amb_env} | leiaute {dps.versao_dps()} | assinatura "
          f"{assinatura.algoritmo_configurado()}")
    limites = [p for p in probs if p[0] == "LIMITE"]
    faltas = [p for p in probs if p[0] != "LIMITE"]
    for p in limites:
        print(f"LIMITE: {p[1]} {p[2]}")
    if faltas:
        print(f"FALTA DADO ({len(faltas)} item(ns)). Primeira pergunta ao dono: {faltas[0][2]}")
    if not probs:
        print("Fichas completas" + (f" (empresa e cliente {a.cliente})." if a.cliente else
                                    " (empresa). Para um cliente: conferir --cliente <apelido>."))
    if os.environ.get("NFSE_PFX_PATH", "").strip():
        try:
            _, cert, _ = cofre.carregar_certificado()
            dias, fim = cofre.conferir_validade(cert)
            print(f"Certificado: válido até {fim:%d/%m/%Y} ({dias} dias).")
            conferir_cnpj_certificado(cert, empresa)
        except Recusa as e:
            print(f"Certificado: {e}")
    else:
        print("Certificado: NFSE_PFX_PATH não definida (dá pra preparar, não dá pra emitir).")
    print("Palavra-passe: " + ("definida." if cofre.palavra_passe_definida(dados)
                               else "não definida (só produção pede)."))
    pend = cofre.pendencias(dados)
    print(f"Envios sem desfecho: {len(pend)}")
    for _, e in pend:
        print(f"  DPS {e.get('id_dps')} ({e.get('ambiente')}, {e.get('status')}): rode consultar "
              f"--dps {e.get('id_dps')}{flag_amb(e.get('ambiente'))}")
    return 2 if limites else (3 if faltas else 0)


def cmd_certificado(a):
    dados = cofre.dados_dir()
    _, cert, _ = cofre.carregar_certificado()
    dias, fim = cofre.conferir_validade(cert)
    cnpj = cofre.cnpj_do_certificado(cert)
    print(f"Certificado válido até {fim:%d/%m/%Y}: faltam {dias} dia(s).")
    print(f"CNPJ no certificado: {danfse.fmt_doc(cnpj) if cnpj else 'não identificado'}")
    if (dados / "empresa.json").is_file():
        conferir_cnpj_certificado(cert, carregar_empresa(dados))
    return 1 if dias <= cofre.DIAS_AVISO_CERTIFICADO else 0


def cmd_palavra_passe(a):
    dados = cofre.dados_dir()
    if a.status:
        print("Palavra-passe definida." if cofre.palavra_passe_definida(dados)
              else "Palavra-passe ainda não definida.")
        return 0
    if a.definir:
        if cofre.palavra_passe_definida(dados):
            raise Recusa("já existe palavra-passe. Para trocar use --trocar (pede a atual).")
        cofre.definir_palavra_passe(dados, cofre.ler_segredo("nova palavra-passe"))
    else:
        if not cofre.palavra_passe_definida(dados):
            raise Recusa("não há palavra-passe para trocar. Use --definir.")
        atual = cofre.ler_segredo("palavra-passe atual")
        nova = cofre.ler_segredo("nova palavra-passe")
        cofre.definir_palavra_passe(dados, nova, atual=atual)
    cofre.registrar(dados, "palavra_passe_gravada")
    print("Palavra-passe guardada só como hash com sal. Ela é pedida em toda emissão em produção.")
    return 0


def cmd_contador(a):
    dados = cofre.dados_dir()
    amb = ambiente(a)
    empresa = carregar_empresa(dados)
    serie = dps.so_digitos(empresa.get("serie_dps"))
    if not serie:
        raise Recusa("a ficha da empresa ainda não tem serie_dps.")
    serie = str(int(serie))
    with cofre.cadeado(dados):
        ultimo = cofre.contador_ultimo(dados, amb, serie)
        if a.ajustar is not None:
            if a.ajustar < ultimo:
                raise Recusa(f"o contador só sobe (está em {ultimo}). Baixar repetiria número de DPS.")
            ultimo = cofre.contador_avancar(dados, amb, serie, a.ajustar)
            cofre.registrar(dados, "contador_ajustado", ambiente=amb, serie=serie, ultimo=ultimo)
    print(f"Último DPS usado em {NOME_AMB[amb]}, série {serie}: {ultimo}. "
          f"O próximo sai com {ultimo + 1}.")
    return 0


def cmd_preparar(a):
    dados = cofre.dados_dir()
    amb = ambiente(a)
    pend = pendencias_do(dados, amb)
    if pend:
        raise Recusa(msg_pendencias(pend))
    empresa = carregar_empresa(dados)
    cliente = carregar_cliente(dados, a.cliente)
    nota = {"valor": a.valor, "competencia": a.competencia, "descricao": a.descricao or ""}
    hoje = cofre.agora().date()
    probs = dps.validar_dados(empresa, cliente, nota, hoje=hoje)
    limites = [p for p in probs if p[0] == "LIMITE"]
    if limites:
        raise Recusa(f"LIMITE: {limites[0][1]} {limites[0][2]}")
    if probs:
        print(f"FALTA DADO: {probs[0][1]}")
        print(f"Pergunta ao dono: {probs[0][2]}")
        if len(probs) > 1:
            print(f"(faltam {len(probs)} itens; pergunte um por vez)")
        return 3
    if os.environ.get("NFSE_PFX_PATH", "").strip():
        _, cert, _ = cofre.carregar_certificado()
        cofre.conferir_validade(cert)
        conferir_cnpj_certificado(cert, empresa)
    else:
        cofre.aviso("NFSE_PFX_PATH não definida: o rascunho sai, mas emitir vai pedir o certificado.")
    versao = dps.versao_dps()
    alg = assinatura.algoritmo_configurado()
    serie = str(int(dps.so_digitos(empresa["serie_dps"])))
    ndps = cofre.contador_ultimo(dados, amb, serie) + 1
    raiz, id_dps = dps.montar_dps(empresa, cliente, nota, amb, ndps,
                                  cofre.agora() - RECUO_DHEMI, versao=versao)
    erros = dps.validar_estrutura(raiz, versao=versao)
    if erros:
        print("ERRO: o DPS montado não passou na conferência de estrutura:", file=sys.stderr)
        for e in erros:
            print(f"  - {e}", file=sys.stderr)
        return 1
    xml = dps.serializar(raiz)
    h = hashlib.sha256(xml).hexdigest()[:12]
    limpar_rascunhos_vencidos(dados)
    pasta = dados / "rascunhos" / h
    cofre.escrever_privado(pasta / "dps.xml", xml)
    resumo = {
        "hash": h, "ambiente": amb, "cliente": a.cliente,
        "cliente_nome": dps.limpo(cliente.get("nome")),
        "cliente_doc": dps.doc_limpo(cliente["documento"]["numero"]),
        "valor": f"{dps.dinheiro(a.valor):.2f}",
        "descricao": dps.descricao_final(cliente, nota),
        "competencia": dps.competencia(a.competencia, hoje).isoformat(),
        "retencao": int(dps.limpo(cliente["iss"]["tpRetISSQN"])),
        "serie": serie, "nDPS": ndps, "id_dps": id_dps, "versao": versao,
        "assinatura": alg, "criado_em": cofre.agora_iso(),
    }
    cofre.gravar_json(pasta / "resumo.json", resumo)
    cofre.registrar(dados, "preparou", ambiente=amb, cliente=a.cliente, valor=resumo["valor"],
                    id_dps=id_dps, hash=h)
    r = resumo
    print("RASCUNHO PRONTO. Nada foi enviado ao governo.")
    print(f"  ambiente:     {NOME_AMB[amb]}")
    print(f"  cliente:      {r['cliente_nome']} ({danfse.fmt_doc(r['cliente_doc'])})")
    print(f"  valor:        {danfse.brl(r['valor'])}")
    print(f"  descrição:    {r['descricao']}")
    print(f"  competência:  {r['competencia'][5:7]}/{r['competencia'][:4]} "
          f"(dCompet {r['competencia']})")
    print(f"  ISS:          {dps.RET_ISS[r['retencao']]}")
    print(f"  DPS:          série {serie}, número {ndps} (Id {id_dps})")
    print(f"  leiaute:      versão {versao}, assinatura {alg}")
    print(f"  hash:         {h}")
    print("Mostre este resumo ao dono e espere a confirmação explícita. Depois:")
    if amb == "producao":
        print(f"  python3 scripts/nfse.py emitir --hash {h} --producao --palavra-passe-stdin")
        print("  (a palavra-passe que o dono digitar entra pela entrada padrão, nunca como argumento)")
    else:
        print(f"  python3 scripts/nfse.py emitir --hash {h}")
    print(f"O rascunho vale por {int(VALIDADE_RASCUNHO.total_seconds() // 3600)} horas.")
    return 0


def exigir_palavra_passe(dados, empresa, a, h):
    if empresa.get("exigir_palavra_passe", True) is False:
        cofre.aviso("a ficha desligou a palavra-passe; a confirmação com resumo continua obrigatória.")
        return
    if not cofre.palavra_passe_definida(dados):
        raise Recusa("produção pede a palavra-passe do dono e ela ainda não foi definida. O dono "
                     "define uma vez com: python3 scripts/nfse.py palavra-passe --definir")
    if not a.palavra_passe_stdin and not (sys.stdin and sys.stdin.isatty()):
        raise Recusa("produção pede a palavra-passe do dono. Passe pela entrada padrão com "
                     "--palavra-passe-stdin.")
    pp = cofre.ler_segredo("palavra-passe")
    if not pp or not cofre.conferir_palavra_passe(dados, pp):
        cofre.registrar(dados, "palavra_passe_errada", hash=h)
        raise Recusa("palavra-passe não confere. Nada foi enviado.")


def cmd_emitir(a):
    dados = cofre.dados_dir()
    amb = ambiente(a)
    h = (a.hash or "").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{12}", h):
        raise Recusa("hash inválido. Use os 12 caracteres que o preparar imprimiu.")
    pasta = dados / "rascunhos" / h
    if not (pasta / "dps.xml").is_file() or not (pasta / "resumo.json").is_file():
        raise Recusa("o hash não confere com nenhum rascunho. Nada foi enviado. Rode preparar e "
                     "use o hash que ele imprimir.")
    xml = (pasta / "dps.xml").read_bytes()
    r = cofre.ler_json(pasta / "resumo.json")
    if hashlib.sha256(xml).hexdigest()[:12] != h or r.get("hash") != h:
        raise Recusa("o conteúdo do rascunho não bate com o hash confirmado. Nada foi enviado. "
                     "Rode preparar de novo e mostre o resumo novo ao dono.")
    tp = etree.fromstring(xml, dps.parser_seguro()).findtext(f"{{{dps.NS}}}infDPS/{{{dps.NS}}}tpAmb")
    if r["ambiente"] != amb or tp != dps.TP_AMB[amb]:
        raise Recusa(f"o rascunho é de {NOME_AMB[r['ambiente']]} e o comando pediu "
                     f"{NOME_AMB[amb]}. Nada foi enviado.")
    if cofre.agora() - dt.datetime.fromisoformat(r["criado_em"]) > VALIDADE_RASCUNHO:
        raise Recusa("rascunho vencido (mais de 12 horas). Rode preparar de novo; o resumo novo "
                     "volta ao dono.")
    empresa = carregar_empresa(dados)
    if amb == "producao":
        exigir_palavra_passe(dados, empresa, a, h)
    pend = pendencias_do(dados, amb)
    if pend:
        raise Recusa(msg_pendencias(pend))
    cliente_sefin.url_base(amb)
    chave, cert, extras = cofre.carregar_certificado()
    cofre.conferir_validade(cert)
    conferir_cnpj_certificado(cert, empresa)

    with cofre.cadeado(dados):
        ultimo = cofre.contador_ultimo(dados, amb, r["serie"])
        if int(r["nDPS"]) != ultimo + 1:
            raise Recusa(f"o número {r['nDPS']} do rascunho não é o próximo livre ({ultimo + 1}). "
                         "Nada foi enviado. Rode preparar de novo.")
        try:
            assinado = assinatura.assinar_dps(xml, chave, cert, r.get("assinatura"))
        except ValueError as e:
            raise Recusa(f"não deu para assinar: {e}. Nada foi enviado.") from None
        problemas = dps.prefixos(etree.fromstring(assinado, dps.parser_seguro()))
        if problemas:
            raise Recusa(f"o XML assinado ficou com prefixo de namespace: {problemas[0]}. "
                         "Nada foi enviado.")
        nota_dir = pasta_da_nota(dados, r)
        cofre.escrever_privado(nota_dir / "dps-rascunho.xml", xml)
        cofre.escrever_privado(nota_dir / "dps-assinado.xml", assinado)
        estado = {k: r[k] for k in ("id_dps", "ambiente", "serie", "nDPS", "cliente",
                                    "cliente_nome", "valor", "competencia", "hash", "versao",
                                    "assinatura")}
        estado.update(status="enviando", enviado_em=cofre.agora_iso())
        cofre.gravar_json(nota_dir / "estado.json", estado)
        cofre.registrar(dados, "enviando", ambiente=amb, id_dps=r["id_dps"], hash=h)
        try:
            try:
                ctx = cliente_sefin.contexto_tls(chave, cert, extras)
            except (OSError, ValueError) as e:
                raise cliente_sefin.NaoEnviado(
                    f"o certificado não entrou no TLS ({type(e).__name__}: {e})") from None
            j, xml_nfse, _ = cliente_sefin.enviar_dps(amb, ctx, assinado)
        except (cliente_sefin.NaoEnviado, Recusa) as e:
            estado.update(status="nao_enviada", motivo=str(e), fim=cofre.agora_iso())
            cofre.gravar_json(nota_dir / "estado.json", estado)
            cofre.registrar(dados, "nao_enviada", ambiente=amb, id_dps=r["id_dps"])
            print("NÃO ENVIADO: a conexão não abriu, então nada chegou ao governo e o número do "
                  "DPS segue livre.")
            print(f"  motivo: {e}")
            print(f"  Dá pra tentar o mesmo rascunho de novo: python3 scripts/nfse.py emitir "
                  f"--hash {h}{flag_amb(amb)}")
            return 7
        except cliente_sefin.Rejeitado as e:
            cofre.contador_avancar(dados, amb, r["serie"], r["nDPS"])
            estado.update(status="rejeitada", http=e.status, erros=e.erros, fim=cofre.agora_iso())
            cofre.escrever_privado(nota_dir / "resposta-bruta.txt", e.bruto)
            cofre.gravar_json(nota_dir / "estado.json", estado)
            cofre.registrar(dados, "rejeitada", ambiente=amb, id_dps=r["id_dps"], http=e.status)
            shutil.rmtree(pasta, ignore_errors=True)
            print(f"REJEITADA (HTTP {e.status}): o governo recusou o DPS e nenhuma nota foi emitida.")
            for x in e.erros:
                print(f"  - {x}")
            print(f"  resposta guardada em {nota_dir / 'resposta-bruta.txt'}")
            print("  Corrija o que o erro aponta (dado fiscal, com o contador) e rode preparar de novo.")
            return 5
        except cliente_sefin.EnvioIncerto as e:
            cofre.contador_avancar(dados, amb, r["serie"], r["nDPS"])
            estado.update(status="incerta", motivo=str(e), chave_na_resposta=e.chave,
                          fim=cofre.agora_iso())
            if e.bruto:
                cofre.escrever_privado(nota_dir / "resposta-bruta.txt", e.bruto)
            cofre.gravar_json(nota_dir / "estado.json", estado)
            cofre.registrar(dados, "incerta", ambiente=amb, id_dps=r["id_dps"])
            shutil.rmtree(pasta, ignore_errors=True)
            print("ENVIO INCERTO: o pedido saiu e a resposta não fechou. A nota PODE ter sido emitida.")
            print(f"  motivo: {e}")
            if e.bruto:
                print(f"  resposta bruta guardada em {nota_dir / 'resposta-bruta.txt'}")
            if e.chave:
                print(f"  a resposta trouxe a chave {e.chave}: python3 scripts/nfse.py consultar "
                      f"--chave {e.chave}{flag_amb(amb)}")
            print("  NÃO emita de novo. Antes de qualquer reenvio, rode:")
            print(f"  python3 scripts/nfse.py consultar --dps {r['id_dps']}{flag_amb(amb)}")
            return 6
        cofre.contador_avancar(dados, amb, r["serie"], r["nDPS"])
        try:
            info = dps.ler_nfse(xml_nfse)
        except (ValueError, etree.XMLSyntaxError) as e:
            cofre.escrever_privado(nota_dir / "nfse-devolvido-ilegivel.xml", xml_nfse)
            estado.update(status="incerta", motivo=f"XML devolvido ilegível: {e}",
                          fim=cofre.agora_iso())
            cofre.gravar_json(nota_dir / "estado.json", estado)
            cofre.registrar(dados, "incerta", ambiente=amb, id_dps=r["id_dps"])
            shutil.rmtree(pasta, ignore_errors=True)
            print("ENVIO INCERTO: o servidor devolveu um XML que o leitor não reconheceu.")
            print(f"  guardado em {nota_dir / 'nfse-devolvido-ilegivel.xml'}. NÃO emita de novo; rode:")
            print(f"  python3 scripts/nfse.py consultar --dps {r['id_dps']}{flag_amb(amb)}")
            return 6
        cofre.escrever_privado(nota_dir / "nfse.xml", xml_nfse, sobrescrever=False)
        estado.update(status="autorizada", chave=info["chave"], numero=info["numero"],
                      fim=cofre.agora_iso())
        cofre.gravar_json(nota_dir / "resposta.json",
                          {k: v for k, v in (j or {}).items() if "xmlgzipb64" not in k.lower()})
        cofre.gravar_json(nota_dir / "estado.json", estado)
        cofre.registrar(dados, "autorizada", ambiente=amb, id_dps=r["id_dps"], chave=info["chave"])
    shutil.rmtree(pasta, ignore_errors=True)
    relato_nota("NFS-e AUTORIZADA", nota_dir, info, amb, gerar_pdf_da_pasta(nota_dir, info, estado))
    return 0


def _consulta_ctx(amb):
    cliente_sefin.url_base(amb)
    chave, cert, extras = cofre.carregar_certificado()
    cofre.conferir_validade(cert)
    try:
        return cliente_sefin.contexto_tls(chave, cert, extras)
    except (OSError, ValueError) as e:
        raise Recusa(f"o certificado não entrou no TLS ({type(e).__name__}).") from None


def cmd_consultar(a):
    dados = cofre.dados_dir()
    amb = ambiente(a)
    if a.dps and not re.fullmatch(ID_DPS_RE, a.dps):
        raise Recusa("Id de DPS inválido (45 caracteres, começando por DPS).")
    if a.chave and not re.fullmatch(r"\d{50}", a.chave):
        raise Recusa("chave de acesso inválida (50 dígitos).")
    ctx = _consulta_ctx(amb)
    chave_nota = a.chave
    try:
        if a.dps:
            desfecho, chave_nota, bruto = cliente_sefin.consultar_dps(amb, ctx, a.dps)
            if desfecho == "nao_achou":
                nota_dir, estado = achar_nota(dados, amb, id_dps=a.dps)
                if estado is not None:
                    estado["consulta_sem_nota_em"] = cofre.agora_iso()
                    cofre.gravar_json(nota_dir / "estado.json", estado)
                cofre.registrar(dados, "consulta_dps_sem_nota", ambiente=amb, id_dps=a.dps)
                print(f"Nenhuma NFS-e encontrada para o DPS {a.dps} (404 com e sem o prefixo DPS).")
                print("Antes de liberar nova emissão, confira também no portal do emissor nacional.")
                print("Se lá também não houver nota com esse DPS, libere com:")
                print(f"  python3 scripts/nfse.py resolver --dps {a.dps} --sem-nota{flag_amb(amb)}")
                return 0
            if desfecho == "inconclusivo":
                arq = guardar_bruto(dados, amb, f"consulta-{a.dps}", bruto)
                print("CONSULTA INCONCLUSIVA: a resposta não trouxe a chave de acesso no formato "
                      "esperado. O envio continua pendente.")
                print(f"  resposta bruta guardada em {arq}")
                print("  Confira no portal do emissor nacional antes de qualquer reenvio.")
                return 6
        r = cliente_sefin.consultar_nfse(amb, ctx, chave_nota)
    except (cliente_sefin.NaoEnviado, cliente_sefin.EnvioIncerto) as e:
        print(f"CONSULTA NÃO CONCLUÍDA: {e}. Nada mudou; tente de novo em alguns minutos.")
        return 6
    except cliente_sefin.Rejeitado as e:
        print(f"CONSULTA RECUSADA (HTTP {e.status}):")
        for x in e.erros:
            print(f"  - {x}")
        return 5
    except cliente_sefin.RespostaIlegivel as e:
        arq = guardar_bruto(dados, amb, f"consulta-{chave_nota}", e.bruto)
        print(f"CONSULTA INCONCLUSIVA: {e}. Resposta bruta guardada em {arq}.")
        return 6
    if r is None:
        print(f"Nenhuma NFS-e com a chave {chave_nota} em {NOME_AMB[amb]}.")
        return 1
    _, xml = r
    info = dps.ler_nfse(xml)
    nota_dir, estado = achar_nota(dados, amb, id_dps=info.get("id_dps"))
    if nota_dir is None:
        nota_dir, estado = dados / "notas" / amb / "consultas" / info["chave"], None
    if not (nota_dir / "nfse.xml").exists():
        cofre.escrever_privado(nota_dir / "nfse.xml", xml, sobrescrever=False)
    if estado is not None and estado.get("status") != "autorizada":
        antes = estado.get("status")
        estado.update(status="autorizada", chave=info["chave"], numero=info["numero"],
                      resolvido_em=cofre.agora_iso(), resolvido_por="consulta")
        cofre.gravar_json(nota_dir / "estado.json", estado)
        with cofre.cadeado(dados):
            cofre.contador_avancar(dados, amb, estado["serie"], estado["nDPS"])
        print(f"O envio que estava {antes} virou nota. Ela foi guardada; não emita de novo.")
    cofre.registrar(dados, "consultou", ambiente=amb, chave=info["chave"])
    relato_nota("NFS-e ENCONTRADA", nota_dir, info, amb,
                gerar_pdf_da_pasta(nota_dir, info, estado or {}))
    return 0


def cmd_resolver(a):
    dados = cofre.dados_dir()
    amb = ambiente(a)
    nota_dir, estado = achar_nota(dados, amb, id_dps=a.dps)
    if estado is None:
        raise Recusa(f"não achei envio registrado com o DPS {a.dps} em {NOME_AMB[amb]}.")
    if estado.get("status") not in cofre.STATUS_PENDENTE:
        raise Recusa(f"o envio do DPS {a.dps} não está pendente (status {estado.get('status')}). "
                     "Nada mudou.")
    if not a.sem_nota:
        raise Recusa("resolver só libera com --sem-nota, depois de conferir que não existe nota "
                     "com esse DPS.")
    if not estado.get("consulta_sem_nota_em") and not a.sem_consulta_api:
        raise Recusa(f"rode antes: python3 scripts/nfse.py consultar --dps {a.dps}{flag_amb(amb)}. "
                     "Se a consulta pela API não funcionar e o portal mostrar que não há nota, "
                     "repita este comando com --sem-consulta-api.")
    with cofre.cadeado(dados):
        cofre.contador_avancar(dados, amb, estado["serie"], estado["nDPS"])
        estado.update(status="sem_nota", resolvido_em=cofre.agora_iso(),
                      resolvido_por="dono, depois de consultar")
        cofre.gravar_json(nota_dir / "estado.json", estado)
    cofre.registrar(dados, "resolveu_sem_nota", ambiente=amb, id_dps=a.dps)
    print(f"Envio do DPS {a.dps} marcado como sem nota. O número {estado['nDPS']} fica usado; a "
          "próxima nota sai com número novo depois de um preparar.")
    return 0


def cmd_eventos(a):
    dados = cofre.dados_dir()
    amb = ambiente(a)
    if not re.fullmatch(r"\d{50}", a.chave or ""):
        raise Recusa("chave de acesso inválida (50 dígitos).")
    ctx = _consulta_ctx(amb)
    try:
        j, bruto = cliente_sefin.consultar_eventos(amb, ctx, a.chave)
    except (cliente_sefin.NaoEnviado, cliente_sefin.EnvioIncerto) as e:
        print(f"CONSULTA NÃO CONCLUÍDA: {e}. Nada mudou.")
        return 6
    except cliente_sefin.Rejeitado as e:
        print(f"CONSULTA RECUSADA (HTTP {e.status}):")
        for x in e.erros:
            print(f"  - {x}")
        return 5
    eventos = interpretar_eventos(j)
    nota_dir, estado = achar_nota(dados, amb, chave=a.chave)
    if nota_dir is None:
        nota_dir = dados / "notas" / amb / "consultas" / a.chave
        est = nota_dir / "estado.json"
        estado = cofre.ler_json(est) if est.is_file() else {
            "chave": a.chave, "ambiente": amb, "status": "consultada"}
    cofre.escrever_privado(nota_dir / "eventos-bruto.json", bruto or b"[]")
    if not eventos and not _vazio(j):
        print("EVENTOS INCONCLUSIVOS: a resposta veio num formato que o leitor não reconheceu.")
        print(f"  resposta guardada em {nota_dir / 'eventos-bruto.json'}; confira no portal.")
        return 6
    cancelada = any(e["codigo"] == "101101" for e in eventos)
    substituida = any(e["codigo"] == "105102" for e in eventos)
    estado.update(cancelada=cancelada or substituida, substituida=substituida,
                  eventos=eventos, eventos_conferidos_em=cofre.agora_iso())
    cofre.gravar_json(nota_dir / "estado.json", estado)
    cofre.registrar(dados, "eventos", ambiente=amb, chave=a.chave, cancelada=cancelada,
                    substituida=substituida)
    print(f"Eventos da chave {a.chave}: {len(eventos)}")
    for e in eventos:
        print(f"  - {e['codigo']} {e['descricao']}")
    if cancelada or substituida:
        marca = "SUBSTITUÍDA" if substituida else "CANCELADA"
        print(f"A nota está {marca}. Gere o PDF de novo para ele mostrar a marca:")
        print(f"  python3 scripts/nfse.py pdf --xml {nota_dir / 'nfse.xml'}")
    else:
        print("Nenhum evento de cancelamento registrado para essa chave.")
    return 0


def cmd_pdf(a):
    cofre.dados_dir()
    xml_path = Path(a.xml).expanduser().resolve()
    if not xml_path.is_file():
        raise Recusa(f"não achei o XML em {xml_path}.")
    saida = Path(a.saida).expanduser().resolve() if a.saida else xml_path.with_suffix(".pdf")
    cofre.exigir_fora_da_skill(saida, "--saida")
    info = dps.ler_nfse(xml_path.read_bytes())
    est = xml_path.parent / "estado.json"
    estado = cofre.ler_json(est) if est.is_file() else {}
    try:
        danfse.gerar_pdf(info, saida, situacao_de(estado))
    except danfse.FaltaDependencia as e:
        print(f"DEPENDÊNCIA AUSENTE: {e}. O XML segue sendo o documento fiscal; o PDF fica "
              "para depois.")
        return 4
    os.chmod(saida, 0o600)
    print(f"PDF gerado: {saida}")
    print(f"Chave: {info['chave']} | consulta pública: {danfse.url_consulta(info['chave'])}")
    if estado.get("cancelada") is None:
        print(f"Situação de cancelamento não consultada. Para conferir: python3 scripts/nfse.py "
              f"eventos --chave {info['chave']}")
    return 0


def cmd_ler(a):
    cofre.dados_dir()
    info = dps.ler_nfse(Path(a.xml).expanduser().read_bytes())
    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0


def main(argv=None):
    os.umask(0o077)
    ap = argparse.ArgumentParser(prog="nfse.py", description="Emissão de NFS-e padrão nacional.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def novo(nome, func, ajuda, producao=False):
        p = sub.add_parser(nome, help=ajuda)
        p.set_defaults(func=func)
        if producao:
            p.add_argument("--producao", action="store_true", help="produção (exige NFSE_AMBIENTE=producao)")
        return p

    novo("iniciar", cmd_iniciar, "cria a pasta de dados e as fichas-modelo")
    p = novo("conferir", cmd_conferir, "o que falta nas fichas")
    p.add_argument("--cliente")
    novo("certificado", cmd_certificado, "validade do certificado")
    p = novo("palavra-passe", cmd_palavra_passe, "define, troca ou mostra a palavra-passe")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--definir", action="store_true")
    g.add_argument("--trocar", action="store_true")
    g.add_argument("--status", action="store_true")
    p = novo("contador", cmd_contador, "último número de DPS usado", producao=True)
    p.add_argument("--ajustar", type=int)
    p = novo("preparar", cmd_preparar, "monta o rascunho e imprime o resumo", producao=True)
    p.add_argument("--cliente", required=True)
    p.add_argument("--valor", required=True)
    p.add_argument("--competencia", required=True)
    p.add_argument("--descricao")
    p = novo("emitir", cmd_emitir, "assina e envia o rascunho confirmado", producao=True)
    p.add_argument("--hash", required=True)
    p.add_argument("--palavra-passe-stdin", action="store_true")
    p = novo("consultar", cmd_consultar, "consulta por Id do DPS ou por chave", producao=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--dps")
    g.add_argument("--chave")
    p = novo("resolver", cmd_resolver, "libera envio incerto confirmado sem nota", producao=True)
    p.add_argument("--dps", required=True)
    p.add_argument("--sem-nota", action="store_true")
    p.add_argument("--sem-consulta-api", action="store_true")
    p = novo("eventos", cmd_eventos, "eventos da chave (cancelamento)", producao=True)
    p.add_argument("--chave", required=True)
    p = novo("pdf", cmd_pdf, "PDF de representação a partir do XML")
    p.add_argument("--xml", required=True)
    p.add_argument("--saida")
    p = novo("ler", cmd_ler, "lê o XML autorizado")
    p.add_argument("--xml", required=True)

    a = ap.parse_args(argv)
    try:
        return a.func(a) or 0
    except Recusa as e:
        print(f"RECUSADO: {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
