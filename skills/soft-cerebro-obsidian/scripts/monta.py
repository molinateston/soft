#!/usr/bin/env python3
"""Gera o mapa visual do cérebro: uma página HTML de arquivo único (sem internet, sem bibliotecas).

Uso:  python3 monta.py <config.json>

Lê as notas em Markdown da pasta `raiz`, liga uma nota na outra pelos [[links]] e pelos
conceitos do config, e grava `<saida>/index.html`. Só usa a biblioteca padrão do Python 3.
Arquivo ou pasta que começa com "_" fica de fora, e a pasta ESTADO também.
"""
import glob
import json
import os
import re
import sys
import unicodedata
from datetime import date

CORES = ["#4ade80", "#60a5fa", "#f59e0b", "#f472b6", "#a78bfa", "#2dd4bf",
         "#fb7185", "#facc15", "#38bdf8", "#c084fc", "#34d399", "#fb923c"]


def norm(s):
    """minúsculo e sem acento, para casar 'diagnostico' com 'diagnóstico'."""
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def falha(msg):
    print("ERRO: " + msg, file=sys.stderr)
    sys.exit(1)


def rotulo(stem, acentos, por_data):
    if por_data:
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", stem)
        if m:
            return f"{m.group(3)}/{m.group(2)}/{m.group(1)}"
    palavras = re.sub(r"[-_]+", " ", stem).strip().split()
    out = []
    for p in palavras:
        fix = acentos.get(norm(p))
        out.append(fix if fix else p.capitalize() if p.isupper() or p.islower() else p)
    return " ".join(out)


def titulo_h1(cru):
    """primeiro cabeçalho '# Título' da nota (já com acento certo), ou ''."""
    t = re.sub(r"^---\n.*?\n---\n", "", cru, flags=re.S)
    m = re.search(r"^#\s+(.+?)\s*$", t, re.M)
    return m.group(1).strip() if m else ""


def limpa_md(t):
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)  # frontmatter
    t = re.sub(r"^\s*#\s+.*\n", "", t, count=1)  # o título já aparece no painel
    t = re.sub(r"\[\[([^\]|]+)\|?([^\]]*)\]\]", lambda m: m.group(2) or m.group(1), t)
    t = re.sub(r"[#>*`_]+", "", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def main():
    if len(sys.argv) != 2:
        falha("uso: python3 monta.py <config.json>")
    cfg_path = os.path.abspath(sys.argv[1])
    base = os.path.dirname(cfg_path)
    try:
        cfg = json.load(open(cfg_path, encoding="utf-8"))
    except Exception as e:
        falha(f"não consegui ler o config: {e}")

    raiz = os.path.normpath(os.path.join(base, cfg.get("raiz", "brain")))
    if not os.path.isdir(raiz):
        falha(f"a pasta raiz não existe: {raiz}")
    saida = os.path.normpath(os.path.join(base, cfg.get("saida", "cerebro-site")))
    acentos = {norm(k): v for k, v in cfg.get("acentos", {}).items()}
    modo_texto = cfg.get("texto", "resumo")  # nenhum | resumo | completo

    hubs = cfg.get("hubs", [])
    if not hubs:
        falha("o config precisa de pelo menos 1 hub (núcleo)")
    hub_ids = set()
    for i, h in enumerate(hubs):
        h.setdefault("cor", CORES[i % len(CORES)])
        hub_ids.add(h["id"])
    conceitos = cfg.get("conceitos", [])
    for c in conceitos:
        if c["hub"] not in hub_ids:
            falha(f'o conceito "{c["id"]}" aponta para o hub "{c["hub"]}", que não existe em "hubs"')
        try:
            c["_re"] = re.compile(norm(c["regex"]))
        except re.error as e:
            falha(f'regex inválida no conceito "{c["id"]}": {e}')

    nos, ligacoes, vistos = [], [], {}
    especiais = {norm(x) for x in cfg.get("notas_especiais", [])}

    def add_no(id_, nome, hub, tipo, texto="", caminho="", grande=False):
        nos.append({"id": id_, "nome": nome, "hub": hub, "tipo": tipo, "texto": texto,
                    "caminho": caminho, "grande": grande})
        vistos[id_] = len(nos) - 1

    add_no("centro", cfg.get("titulo", "Cérebro"), hubs[0]["id"], "centro", grande=True)
    for h in hubs:
        add_no("hub:" + h["id"], h["nome"], h["id"], "hub", grande=True)
        ligacoes.append(["centro", "hub:" + h["id"], "hub"])
    for c in conceitos:
        add_no("c:" + c["id"], c["nome"], c["hub"], "conceito")
        ligacoes.append(["hub:" + c["hub"], "c:" + c["id"], "hub"])

    # --- notas ---
    notas = []  # (id, stem_norm, texto_norm, texto_cru, pasta_cfg, caminho_rel)
    for pasta in cfg.get("pastas", [{"caminho": "*.md", "hub": hubs[0]["id"]}]):
        if pasta["hub"] not in hub_ids:
            falha(f'a pasta "{pasta["caminho"]}" aponta para o hub "{pasta["hub"]}", que não existe em "hubs"')
        padrao = os.path.join(raiz, pasta["caminho"])
        achados = sorted(glob.glob(padrao, recursive=True))
        for p in achados:
            partes = os.path.relpath(p, raiz).split(os.sep)
            if any(x.startswith("_") or x == "ESTADO" for x in partes):
                continue
            if pasta.get("tipo") == "pastas":
                if not os.path.isdir(p):
                    continue
                leitura = os.path.join(p, "README.md")
                cru = open(leitura, encoding="utf-8", errors="ignore").read() if os.path.isfile(leitura) else ""
                stem = os.path.basename(p.rstrip(os.sep))
            else:
                if not os.path.isfile(p) or not p.endswith(".md"):
                    continue
                cru = open(p, encoding="utf-8", errors="ignore").read()
                stem = os.path.splitext(os.path.basename(p))[0]
            nid = "n:" + os.path.relpath(p, raiz)
            if nid in vistos:
                continue
            especial = norm(os.path.basename(p)) in especiais
            nome = rotulo(stem, acentos, pasta.get("rotulo_por_data", False))
            h1 = titulo_h1(cru)
            if h1 and not especial and not pasta.get("rotulo_por_data") and len(h1) <= 40 and ":" not in h1:
                nome = h1
            if modo_texto == "nenhum":
                texto = ""
            else:
                limpo = limpa_md(cru)
                texto = limpo if modo_texto == "completo" else limpo[:700]
            add_no(nid, nome, pasta["hub"], "nota", texto, os.path.relpath(p, raiz), especial)
            notas.append((nid, norm(stem), norm(cru + " " + stem), cru, pasta, os.path.basename(p)))
            ligacoes.append(["hub:" + pasta["hub"], nid, "hub"])
            if especial:
                ligacoes.append(["centro", nid, "centro"])

    if not notas:
        falha("não achei nenhuma nota. Confira 'raiz' e 'pastas' no config")

    por_stem = {}
    for nid, stem_n, *_ in notas:
        por_stem.setdefault(stem_n, nid)
    por_arq = {norm(os.path.splitext(a)[0]): nid for nid, _, _, _, _, a in notas}

    n_links = 0
    pares = set()
    for nid, stem_n, texto_n, cru, pasta, arq in notas:
        for alvo in re.findall(r"\[\[([^\]|#]+)", cru):
            a = norm(alvo.strip())
            dest = por_stem.get(a) or por_arq.get(a)
            if dest and dest != nid and (nid, dest) not in pares and (dest, nid) not in pares:
                pares.add((nid, dest))
                ligacoes.append([nid, dest, "link"])
                n_links += 1
        for c in conceitos:
            if c["_re"].search(texto_n):
                ligacoes.append([nid, "c:" + c["id"], "conceito"])
        for alvo in pasta.get("liga_a", []):
            dest = por_arq.get(norm(os.path.splitext(alvo)[0]))
            if dest and dest != nid:
                ligacoes.append([nid, dest, "pasta"])

    for pe in cfg.get("pessoas", []):
        pid = "p:" + pe["id"]
        add_no(pid, pe["nome"], pe.get("hub", hubs[0]["id"]), "pessoa")
        ligacoes.append(["hub:" + pe.get("hub", hubs[0]["id"]), pid, "hub"])
        for cid in pe.get("conceitos", []):
            if "c:" + cid in vistos:
                ligacoes.append([pid, "c:" + cid, "conceito"])

    # grau para o tamanho; nota sem nenhuma ligação além do hub é órfã
    grau = {n["id"]: 0 for n in nos}
    for a, b, _ in ligacoes:
        if a in grau and b in grau:
            grau[a] += 1
            grau[b] += 1
    orfas = [n["nome"] for n in nos if n["tipo"] == "nota" and grau[n["id"]] <= 1]

    dados = {
        "titulo": cfg.get("titulo", "Cérebro"),
        "subtitulo": (cfg.get("subtitulo", "") + " · " + date.today().strftime("%d/%m/%Y")).strip(" ·"),
        "logo": cfg.get("logo", ""),
        "hubs": [{"id": h["id"], "nome": h["nome"], "cor": h["cor"]} for h in hubs],
        "nos": [{**n, "grau": grau[n["id"]]} for n in nos],
        "ligacoes": [l for l in ligacoes if l[0] in vistos and l[1] in vistos],
    }
    os.makedirs(saida, exist_ok=True)
    logo_html = ""
    if dados["logo"]:
        lp = os.path.join(base, dados["logo"])
        if os.path.isfile(lp):
            import base64
            ext = os.path.splitext(lp)[1].lstrip(".").lower().replace("jpg", "jpeg")
            dados["logo"] = f"data:image/{ext};base64," + base64.b64encode(open(lp, "rb").read()).decode()
        else:
            dados["logo"] = ""
    modelo = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelo.html"), encoding="utf-8").read()
    html = modelo.replace("/*__DADOS__*/null", json.dumps(dados, ensure_ascii=False).replace("</", "<\\/"))
    html = html.replace("__TITULO__", dados["titulo"].replace("<", "&lt;"))
    destino = os.path.join(saida, "index.html")
    open(destino, "w", encoding="utf-8").write(html)

    pontos = len(dados["nos"])
    print(f"ok: {pontos} pontos, {len(dados['ligacoes'])} ligações, {n_links} vieram dos [[links]]")
    print(f"notas: {len(notas)} · conceitos: {len(conceitos)} · núcleos: {len(hubs)}")
    if orfas:
        print(f"aviso: {len(orfas)} nota(s) sem ligação além do núcleo (faltam conceitos ou [[links]]): "
              + ", ".join(orfas[:8]) + (" ..." if len(orfas) > 8 else ""))
    print("gravado em " + destino)


if __name__ == "__main__":
    main()
