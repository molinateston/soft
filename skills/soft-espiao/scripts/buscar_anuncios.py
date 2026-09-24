#!/usr/bin/env python3
"""
buscar_anuncios.py: puxa anuncios ativos da biblioteca de anuncios da Meta pelo
Apify, pontua os sinais de venda e grava a planilha CSV do radar.

Token: SO pela variavel de ambiente APIFY_TOKEN, que ja vem do ambiente do
agente (carregada do arquivo de credenciais). Nunca em arquivo, nunca em
argumento, nunca digitado no comando nem pedido no chat. Sem token o script para
com erro claro e aponta o caminho manual. Confira sem imprimir o valor:
  test -n "$APIFY_TOKEN" && echo token: ok || echo token: ausente

Custo: cada 10 anuncios custam uns 5 a 9 centavos de dolar no coletor. O script
para acima de 50 por termo ou 150 no total por chamada.

USO (a partir da pasta da skill):
  # busca por palavras soltas (2 palavras, sem aspas, rendem melhor)
  python3 scripts/buscar_anuncios.py --termo "metodo violao" --saida radar.csv
  # varios termos na mesma coleta
  ... --termo "erro violao" --termo "adulto violao" --max 20 --saida radar.csv
  # ate --max anuncios ativos de uma pagina concorrente (padrao 20)
  ... --pagina-id 1234567890 --saida radar.csv
  # acompanhamento: acrescenta a coleta de hoje na planilha que ja existe
  ... --termo "metodo violao" --saida planilha.csv --acrescentar
  # recalcula os pontos depois que o dono preencheu a coluna views a mao
  python3 scripts/buscar_anuncios.py --recalcular planilha.csv
  # planilha vazia pro caminho manual (sem token)
  python3 scripts/buscar_anuncios.py --modelo planilha.csv
  # le um JSON bruto salvo antes (sem rede, sem token)
  python3 scripts/buscar_anuncios.py --de-json bruto.json --saida radar.csv

Saida: CSV com uma linha por anuncio e o resumo no terminal. Exit 0 ok,
2 sem token, 3 erro na chamada, 4 nada encontrado, 5 erro de uso.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

ATOR = "apify~facebook-ads-scraper"
API = f"https://api.apify.com/v2/acts/{ATOR}/run-sync-get-dataset-items"

COLUNAS = [
    "data_coleta", "termo", "id", "id_grupo", "pagina", "pagina_id", "inicio",
    "dias_no_ar", "ativo", "copias", "copias_antes", "paginas_mesmo_texto",
    "versoes_da_pagina", "formato", "cta", "destino", "plataformas",
    "texto_inicio", "views", "views_antes", "s1_copias", "s2_paginas",
    "s3_versoes", "s4_views", "s5_tempo", "recente", "pontos", "classe",
    "link_biblioteca", "nota",
]

# Regua de partida (explicada em references/sinais-de-venda.md).
COPIAS_MIN = 7          # 7 a 10 copias do mesmo anuncio
COPIAS_FORTE = 10       # 10 copias com pouco tempo no ar pesa dobrado
PAGINAS_MIN = 2         # mesmo texto em 2 paginas ou mais
VERSOES_MIN = 3         # 3 versoes ou mais da mesma pagina na coleta
DIAS_MIN = 7            # 1 semana no ar ja conta como sinal
RECENTE_DIAS = 30       # comecou nos ultimos 30 dias (recencia do Radar)
COPIAS_FORTE_DIAS = 14  # 10 copias em ate 14 dias no ar vale 2 (fonte: 10 com 5 dias)
VIEWS_CRESC = 0.5       # views +50% entre duas coletas de ate 7 dias


def erro(msg, code):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(code)


def norm_texto(t):
    t = unicodedata.normalize("NFKD", t or "")
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()[:200]


def url_busca(termo=None, pagina_id=None, pais="BR"):
    base = "https://www.facebook.com/ads/library/?"
    q = {"active_status": "active", "ad_type": "all", "country": pais,
         "media_type": "all"}
    if pagina_id:
        q.update({"view_all_page_id": pagina_id, "search_type": "page"})
    else:
        q.update({"q": termo, "search_type": "keyword_unordered"})
    return base + urllib.parse.urlencode(q, quote_via=urllib.parse.quote)


def puxar(urls, maximo, token):
    corpo = json.dumps({"startUrls": [{"url": u} for u in urls],
                        "resultsLimit": maximo}).encode()
    req = urllib.request.Request(
        f"{API}?maxItems={maximo * len(urls)}", data=corpo, method="POST",
        headers={"content-type": "application/json",
                 "authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=280) as r:
            bruto = r.read().decode(errors="replace").strip()
            if not bruto:
                return []
            try:
                return json.loads(bruto)
            except json.JSONDecodeError:
                erro(f"o Apify devolveu algo fora de JSON: {bruto[:200]}", 3)
    except urllib.error.HTTPError as e:
        det = e.read().decode(errors="replace")[:300]
        if e.code in (401, 403):
            erro(f"o Apify recusou o token (HTTP {e.code}). Peça ao dono pra "
                 f"conferir a credencial APIFY_TOKEN no ambiente do agente. "
                 f"Detalhe: {det}", 3)
        erro(f"o Apify respondeu HTTP {e.code}: {det}", 3)
    except (urllib.error.URLError, TimeoutError) as e:
        erro(f"sem resposta do Apify ({e}). Tente de novo com --max menor.", 3)


def dia(v):
    if v in (None, ""):
        return None
    try:
        if isinstance(v, (int, float)) or str(v).isdigit():
            return dt.datetime.fromtimestamp(int(v), dt.timezone.utc).date()
        return dt.date.fromisoformat(str(v)[:10])
    except (ValueError, OSError):
        return None


def termo_da_url(url, termo_por_url):
    if url in termo_por_url:
        return termo_por_url[url]
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    if q.get("q"):
        return q["q"][0]
    if q.get("view_all_page_id"):
        return f"pagina:{q['view_all_page_id'][0]}"
    vals = list(termo_por_url.values())
    return vals[0] if len(vals) == 1 else ""


def linhas_de(itens, hoje, termo_por_url):
    vistos, linhas = set(), []
    for x in itens:
        if not isinstance(x, dict) or x.get("error"):
            continue
        s = x.get("snapshot") or {}
        grupo = str(x.get("collationId") or x.get("collationID") or "")
        aid = str(x.get("adArchiveID") or x.get("adArchiveId") or "")
        chave = grupo or aid
        if not aid or chave in vistos:
            continue
        vistos.add(chave)
        corpo = ((s.get("body") or {}).get("text") if isinstance(
            s.get("body"), dict) else s.get("body")) or ""
        if not corpo and s.get("cards"):
            corpo = (s["cards"][0] or {}).get("body") or ""
        inicio = dia(x.get("startDateFormatted") or x.get("startDate"))
        dias = (hoje - inicio).days if inicio else ""
        linhas.append({
            "data_coleta": hoje.isoformat(),
            "termo": termo_da_url(x.get("inputUrl") or "", termo_por_url),
            "id": aid, "id_grupo": grupo,
            "pagina": x.get("pageName") or s.get("pageName") or "",
            "pagina_id": str(x.get("pageID") or x.get("pageId") or ""),
            "inicio": inicio.isoformat() if inicio else "",
            "dias_no_ar": dias,
            "ativo": "sim" if x.get("isActive") else "não",
            "copias": int(x.get("collationCount") or 1),
            "formato": s.get("displayFormat") or "",
            "cta": s.get("ctaText") or "",
            "destino": s.get("linkUrl") or "",
            "plataformas": "+".join(x.get("publisherPlatform") or []),
            "texto_inicio": re.sub(r"\s+", " ", corpo).strip()[:160],
            "_norm": norm_texto(corpo),
            "link_biblioteca": f"https://www.facebook.com/ads/library/?id={aid}",
        })
    # sinais que dependem do conjunto da coleta
    pags_por_texto, versoes = {}, {}
    for l in linhas:
        if l["_norm"]:
            pags_por_texto.setdefault(l["_norm"], set()).add(l["pagina_id"])
        versoes[l["pagina_id"]] = versoes.get(l["pagina_id"], 0) + 1
    for l in linhas:
        l["paginas_mesmo_texto"] = len(pags_por_texto.get(l.pop("_norm"), {1})) or 1
        l["versoes_da_pagina"] = versoes.get(l["pagina_id"], 1)
    return linhas


def num(v):
    try:
        return float(str(v).replace(".", "").replace(",", ".")) if str(v).strip() else None
    except ValueError:
        return None


def pontuar(l):
    copias = int(num(l.get("copias")) or 1)
    dias = num(l.get("dias_no_ar"))
    recente = dias is not None and dias <= RECENTE_DIAS
    s1 = 0
    if copias >= COPIAS_MIN:
        s1 = 2 if (copias >= COPIAS_FORTE and dias is not None
                   and dias <= COPIAS_FORTE_DIAS) else 1
    s2 = 1 if int(num(l.get("paginas_mesmo_texto")) or 1) >= PAGINAS_MIN else 0
    s3 = 1 if int(num(l.get("versoes_da_pagina")) or 1) >= VERSOES_MIN else 0
    va, vb = num(l.get("views_antes")), num(l.get("views"))
    s4 = 1 if (va and vb and vb >= va * (1 + VIEWS_CRESC)) else 0
    s5 = 1 if (dias is not None and dias >= DIAS_MIN) else 0
    pontos = s1 + s2 + s3 + s4 + s5
    # sinais DISTINTOS alem do tempo no ar (S1 vale 2 pontos, mas e 1 sinal)
    sinais_fora = sum(1 for v in (s1, s2, s3, s4) if v)
    if pontos >= 3 and sinais_fora >= 2:
        classe = "vendendo"
    elif pontos >= 2 and sinais_fora >= 1:
        classe = "candidato"
    else:
        classe = "observar"
    l.update({"s1_copias": s1, "s2_paginas": s2, "s3_versoes": s3,
              "s4_views": s4, "s5_tempo": s5,
              "recente": "sim" if recente else "não",
              "pontos": pontos, "classe": classe})
    return l


def ler_csv(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def gravar(caminho, linhas):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, extrasaction="ignore")
        w.writeheader()
        for l in linhas:
            w.writerow({c: l.get(c, "") for c in COLUNAS})


def ligar_historico(novas, antigas):
    """Preenche copias_antes e views_antes com a ultima coleta do mesmo anuncio."""
    ultimo = {}
    for a in antigas:
        for k in (a.get("id"), a.get("id_grupo")):
            if k:
                ultimo[k] = a
    for l in novas:
        a = ultimo.get(l["id"]) or ultimo.get(l.get("id_grupo") or "-")
        if a:
            l["copias_antes"] = a.get("copias", "")
            l["views_antes"] = a.get("views") or a.get("views_antes") or ""
    return novas


def recalcular(caminho):
    linhas = ler_csv(caminho)
    if not linhas:
        erro(f"planilha vazia ou ausente: {caminho}", 5)
    hist = {}
    for l in sorted(linhas, key=lambda r: r.get("data_coleta", "")):
        k = l.get("id") or l.get("id_grupo")
        ant = hist.get(k)
        if ant and not l.get("views_antes"):
            l["views_antes"] = ant.get("views", "")
        if ant and not l.get("copias_antes"):
            l["copias_antes"] = ant.get("copias", "")
        hist[k] = l
        pontuar(l)
    gravar(caminho, linhas)
    return linhas


def resumo(linhas, caminho):
    cont = {"vendendo": 0, "candidato": 0, "observar": 0}
    for l in linhas:
        cont[l["classe"]] = cont.get(l["classe"], 0) + 1
    print(f"planilha: {caminho}")
    print(f"anuncios na planilha: {len(linhas)} · vendendo: {cont['vendendo']}"
          f" · candidato: {cont['candidato']} · observar: {cont['observar']}")
    top = sorted(linhas, key=lambda r: -int(r["pontos"]))[:5]
    for l in top:
        print(f"  {l['pontos']} pts | {l['classe']} | copias {l['copias']} | "
              f"{l['dias_no_ar']} dias | {l['pagina'][:30]} | {l['link_biblioteca']}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--termo", action="append", default=[],
                   help="palavras soltas da busca (repita pra varios termos)")
    p.add_argument("--pagina-id", action="append", default=[],
                   help="id da pagina concorrente (ate --max anuncios ativos dela)")
    p.add_argument("--pais", default="BR")
    p.add_argument("--max", type=int, default=20, help="anuncios por termo (padrao 20)")
    p.add_argument("--saida", help="CSV de saida")
    p.add_argument("--acrescentar", action="store_true",
                   help="soma a coleta de hoje na planilha que ja existe")
    p.add_argument("--salvar-bruto", help="grava o JSON bruto do Apify neste caminho")
    p.add_argument("--de-json", help="le um JSON bruto salvo, sem rede e sem token")
    p.add_argument("--recalcular", metavar="CSV",
                   help="recalcula os pontos depois de preencher views a mao")
    p.add_argument("--modelo", metavar="CSV", help="grava a planilha vazia")
    a = p.parse_args()
    if a.max > 50 or a.max * (len(a.termo) + len(a.pagina_id)) > 150:
        erro("coleta acima do teto (50 por termo, 150 no total). Divida em "
             "chamadas menores.", 5)

    if a.modelo:
        gravar(a.modelo, [])
        print(f"planilha modelo gravada: {a.modelo} ({len(COLUNAS)} colunas)")
        return 0
    if a.recalcular:
        resumo(recalcular(a.recalcular), a.recalcular)
        return 0
    if not a.saida:
        erro("falta --saida <arquivo.csv>", 5)

    hoje = dt.date.today()
    if a.de_json:
        try:
            with open(a.de_json, encoding="utf-8") as f:
                itens = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            erro(f"nao li {a.de_json}: {e}", 5)
        termo_por_url = {}
    else:
        if not (a.termo or a.pagina_id):
            erro("diga o que buscar: --termo \"palavra palavra\" ou --pagina-id N", 5)
        token = os.environ.get("APIFY_TOKEN", "").strip()
        if not token:
            erro("APIFY_TOKEN nao esta no ambiente. Peça ao dono pra cadastrar a "
                 "credencial no ambiente do agente (nunca no chat nem no comando), "
                 "ou siga o caminho manual: gere a planilha com --modelo "
                 "planilha.csv e preencha com os links e prints que o dono colar.", 2)
        termo_por_url = {url_busca(t, pais=a.pais): t for t in a.termo}
        termo_por_url.update({url_busca(pagina_id=pid, pais=a.pais): f"pagina:{pid}"
                              for pid in a.pagina_id})
        print(f"itens pedidos: {a.max * len(termo_por_url)}")
        itens = puxar(list(termo_por_url), a.max, token)
        if a.salvar_bruto:
            with open(a.salvar_bruto, "w", encoding="utf-8") as f:
                json.dump(itens, f, ensure_ascii=False)

    if itens is None:
        itens = []
    if isinstance(itens, dict):
        itens = [itens]
    novas = linhas_de(itens, hoje, termo_por_url)
    if not novas:
        erro("a busca nao trouxe anuncio ativo. Troque uma das palavras "
             "(uma de mercado + uma do nicho) e rode de novo.", 4)
    antigas = ler_csv(a.saida) if a.acrescentar else []
    ligar_historico(novas, antigas)
    for l in novas:
        pontuar(l)
    todas = antigas + novas
    gravar(a.saida, todas)
    resumo(novas, a.saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
