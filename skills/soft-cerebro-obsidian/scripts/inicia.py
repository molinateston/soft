#!/usr/bin/env python3
"""Cria a estrutura do cérebro numa pasta de projeto. Nunca sobrescreve nada que já existe.

Uso:  python3 inicia.py <pasta-do-projeto> [--nome "Nome do negócio"] [--grava-claude-md]

Cria brain/ (MAPA, MEMORIA-VIVA, agentes, arquivo, ideias, ESTADO), trabalho/ e config.json.
Com --grava-claude-md, acrescenta a regra "gravar na hora" ao CLAUDE.md do projeto (ou cria o arquivo).
"""
import json
import os
import sys
from datetime import datetime

MAPA = """# MAPA: índice da memória do negócio

> Antes de responder sobre histórico, decisões, números ou pessoas, abra a nota certa daqui.
> Toda nota nova ganha uma linha neste arquivo.

## Negócio

## Método

## Pessoas

## Números

## Preferências do dono
"""

VIVA = """# MEMORIA-VIVA: o que está valendo agora

> Uma linha por fato, a mais nova no topo. Sempre com data, hora e onde está a prova.
> Pendência começa com PENDENTE:. Passou de 150 linhas? Mova as antigas para arquivo/AAAA-MM-DD.md.

- [{agora}] Cérebro criado. brain/MAPA.md
"""

BLOCO = """## Memória do negócio (brain/)
- Antes de responder sobre histórico, decisões, números, pessoas ou preferências: abra brain/MAPA.md, ache a nota certa e responda a partir dela.
- Aprendeu algo novo? Grave NA HORA:
  - decisão do dia: linha no topo de brain/MEMORIA-VIVA.md com [data hora] e o caminho da prova;
  - fato permanente: nota em brain/ e linha no brain/MAPA.md, com [[links]];
  - correção numa área: linha em brain/agentes/<area>/licoes.md.
- Toda entrega vai para trabalho/<area>/<AAAA-MM>/<AAAA-MM-DD-nome>/
- Nunca guarde senha, chave de API ou dado sensível de cliente nessas notas.
"""

CONFIG = {
    "titulo": "{nome}",
    "subtitulo": "Mapa da memória do negócio",
    "raiz": "brain",
    "saida": "cerebro-site",
    "logo": "",
    "texto": "resumo",
    "hubs": [
        {"id": "negocio", "nome": "Negócio"},
        {"id": "metodo", "nome": "Método"},
        {"id": "pessoas", "nome": "Pessoas"},
        {"id": "numeros", "nome": "Números"},
        {"id": "memoria", "nome": "Memória"},
        {"id": "entregas", "nome": "Entregas"},
    ],
    "conceitos": [
        {"id": "cliente", "nome": "Cliente ideal", "hub": "negocio", "regex": "cliente|publico|avatar"},
        {"id": "oferta", "nome": "Oferta", "hub": "negocio", "regex": "oferta|programa|produto"},
        {"id": "preco", "nome": "Preço", "hub": "numeros", "regex": "preco|valor|ticket|desconto"},
        {"id": "metodo", "nome": "Método", "hub": "metodo", "regex": "metodo|passo a passo|processo"},
    ],
    "pastas": [
        {"caminho": "*.md", "hub": "negocio"},
        {"caminho": "arquivo/*.md", "hub": "memoria", "rotulo_por_data": True, "liga_a": ["MEMORIA-VIVA.md"]},
        {"caminho": "ideias/*.md", "hub": "memoria", "rotulo_por_data": True},
        {"caminho": "agentes/*/*.md", "hub": "metodo"},
        {"caminho": "../trabalho/*/*/*/", "hub": "entregas", "tipo": "pastas"},
    ],
    "notas_especiais": ["MAPA.md", "MEMORIA-VIVA.md"],
    "pessoas": [],
    "acentos": {"memoria": "Memória", "preco": "Preço", "metodo": "Método", "negocio": "Negócio"},
}


def grava(caminho, conteudo, criados, pulados):
    if os.path.exists(caminho):
        pulados.append(caminho)
        return
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    criados.append(caminho)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)
    proj = os.path.abspath(args[0])
    nome = "Meu negócio"
    if "--nome" in sys.argv:
        nome = sys.argv[sys.argv.index("--nome") + 1]
        args = [a for a in args if a != nome]
    criados, pulados = [], []
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    for d in ["brain/agentes", "brain/arquivo", "brain/ideias", "brain/ESTADO", "trabalho"]:
        os.makedirs(os.path.join(proj, d), exist_ok=True)
    grava(os.path.join(proj, "brain/MAPA.md"), MAPA, criados, pulados)
    grava(os.path.join(proj, "brain/MEMORIA-VIVA.md"), VIVA.format(agora=agora), criados, pulados)
    cfg = json.loads(json.dumps(CONFIG).replace("{nome}", nome))
    grava(os.path.join(proj, "config.json"), json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", criados, pulados)
    if "--grava-claude-md" in sys.argv:
        cm = os.path.join(proj, "CLAUDE.md")
        atual = open(cm, encoding="utf-8").read() if os.path.exists(cm) else ""
        if "Memória do negócio (brain/)" in atual:
            pulados.append(cm + " (a regra já estava lá)")
        else:
            with open(cm, "a", encoding="utf-8") as f:
                f.write(("\n\n" if atual.strip() else "") + BLOCO)
            criados.append(cm + " (regra de gravar na hora acrescentada)")
    print(f"projeto: {proj}")
    for c in criados:
        print("criado:", os.path.relpath(c, proj) if c.startswith(proj) else c)
    for p in pulados:
        print("já existia, não mexi:", os.path.relpath(p, proj) if p.startswith(proj) else p)
    if "--grava-claude-md" not in sys.argv:
        print("\nFalta a regra de gravar na hora. Cole este bloco no CLAUDE.md do projeto:\n")
        print(BLOCO)


if __name__ == "__main__":
    main()
