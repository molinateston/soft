#!/usr/bin/env python3
# Confere as fontes do molde tipográfico aprovado (references/perfil-tipografico.json) pelo SHA256 e imprime o perfil.
# Os caminhos do JSON são relativos à pasta do lote aprovado, só registro de origem (perfil Manuscrito); aqui cada arquivo é procurado pelo NOME
# nas pastas dadas em --fontes (padrão: assets/fontes desta skill). Falha se faltar fonte ou se o hash não bater.
# Uso: python3 reproduzir_molde.py [--fontes <pasta> ...] [--so <nome.ttf> ...] [--origem <pasta do lote aprovado>]
#   --so limita a conferência às fontes citadas (ex.: --so Advercase-Bold.ttf --so Kalam-Bold.ttf).
#   --origem também confere plano.json e scripts/montar_ep.py do lote aprovado, se você tiver essa pasta.
import argparse, hashlib, json, sys
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--fontes', action='append', help='pasta com as fontes (pode repetir); padrão assets/fontes')
ap.add_argument('--so', action='append', help='conferir só estes arquivos de fonte (nome do arquivo)')
ap.add_argument('--origem', help='pasta do lote aprovado, para conferir os arquivos de origem')
a = ap.parse_args()

p = json.loads((SK / 'references/perfil-tipografico.json').read_text())
pastas = [Path(x).expanduser() for x in (a.fontes or [SK / 'assets/fontes'])]
falhas = []
for nome, esperado in p['font_files'].items():
    base = Path(nome).name
    if a.so and base not in a.so: continue
    achado = next((d / base for d in pastas if (d / base).is_file()), None)
    if not achado: falhas.append(f'fonte ausente: {base} (procurei em {", ".join(map(str, pastas))})'); continue
    h = hashlib.sha256(achado.read_bytes()).hexdigest()
    if h != esperado: falhas.append(f'fonte alterada: {achado} ({h} != {esperado})')
    else: print(f'ok {achado}')
if a.origem:
    o = Path(a.origem).expanduser(); src = Path(p['source'])
    for nome, esperado in p.get('source_files', {}).items():
        f = o / Path(nome).relative_to(src)
        if not f.is_file(): falhas.append(f'origem ausente: {f}'); continue
        if hashlib.sha256(f.read_bytes()).hexdigest() != esperado: falhas.append(f'origem alterada: {f}')
        else: print(f'ok {f}')
if falhas:
    print('\n'.join(falhas), file=sys.stderr); sys.exit(1)
print(json.dumps(p, ensure_ascii=False, indent=2))
