#!/usr/bin/env python3
"""Confere a saúde da base de notas do cérebro.

Uso:  python3 confere.py <config.json> [--silencioso]

ERRO (sai 1): MAPA.md ausente, [[link]] quebrado, segredo escrito numa nota.
AVISO (sai 0): nota permanente fora do MAPA, nota sem nenhum [[link]], MEMORIA-VIVA grande ou linha sem data.
"""
import json
import os
import re
import sys
import unicodedata


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


SEGREDOS = [
    (r"\bsk-[A-Za-z0-9_-]{20,}", "chave de API (sk-...)"),
    (r"\bAIza[0-9A-Za-z_-]{30,}", "chave do Google"),
    (r"\bghp_[A-Za-z0-9]{30,}", "token do GitHub"),
    (r"\b(senha|password|passwd|token|secret)\s*[:=]\s*\S{4,}", "senha ou token escrito"),
    (r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", "CPF"),
    (r"\b(?:\d[ -]?){15}\d\b", "possível número de cartão"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "chave privada"),
]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    silencio = "--silencioso" in sys.argv
    cfg_path = os.path.abspath(sys.argv[1])
    base = os.path.dirname(cfg_path)
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    raiz = os.path.normpath(os.path.join(base, cfg.get("raiz", "brain")))
    erros, avisos = [], []
    arquivos = {}
    for dp, dn, fn in os.walk(raiz):
        dn[:] = [d for d in dn if not d.startswith("_") and d != "ESTADO"]
        for f in fn:
            if f.endswith(".md") and not f.startswith("_"):
                p = os.path.join(dp, f)
                arquivos[p] = open(p, encoding="utf-8", errors="ignore").read()
    stems = {norm(os.path.splitext(os.path.basename(p))[0]) for p in arquivos}
    mapa_p = os.path.join(raiz, "MAPA.md")
    if not os.path.isfile(mapa_p):
        erros.append("falta brain/MAPA.md (é a porta de entrada)")
    mapa = norm(arquivos.get(mapa_p, ""))
    for p, t in arquivos.items():
        rel = os.path.relpath(p, raiz)
        for alvo in re.findall(r"\[\[([^\]|#]+)", t):
            if norm(alvo.strip()) not in stems:
                erros.append(f"{rel}: link quebrado [[{alvo.strip()}]]")
        for rx, nome in SEGREDOS:
            if re.search(rx, t, re.I):
                erros.append(f"{rel}: parece ter {nome}. Tire da nota")
        permanente = os.path.dirname(p) == raiz and os.path.basename(p) not in ("MAPA.md", "MEMORIA-VIVA.md")
        if permanente:
            stem = os.path.splitext(os.path.basename(p))[0]
            if norm("[[" + stem + "]]") not in mapa:
                avisos.append(f"{rel}: nota permanente sem linha no MAPA.md")
            if not re.search(r"\[\[", t):
                avisos.append(f"{rel}: nenhum [[link]] para outra nota")
    viva_p = os.path.join(raiz, "MEMORIA-VIVA.md")
    if os.path.isfile(viva_p):
        linhas = [l for l in arquivos[viva_p].splitlines() if l.startswith("- ")]
        if len(linhas) > 150:
            avisos.append(f"MEMORIA-VIVA.md tem {len(linhas)} linhas: mova as antigas para arquivo/")
        sem = [l for l in linhas if not re.match(r"- \[\d{4}-\d{2}-\d{2}", l)]
        if sem:
            avisos.append(f"MEMORIA-VIVA.md: {len(sem)} linha(s) sem [data hora]")
    resumo = f"{len(arquivos)} notas · {len(erros)} erro(s) · {len(avisos)} aviso(s)"
    if silencio:
        print("base: " + resumo)
    else:
        for e in erros:
            print("ERRO:", e)
        for a in avisos:
            print("aviso:", a)
        print("base: " + resumo)
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
