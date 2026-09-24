#!/usr/bin/env python3
"""Caça promessa de risco na copy do anúncio, antes do render.

Uso: python3 scripts/checar_promessa.py copy-lote.md manifesto.json [roteiro-video-1.md ...]
     python3 scripts/checar_promessa.py --selftest

Lê .md e .txt linha a linha; no .json, lê todo valor de texto. Marca:
  prazo      resultado com prazo ("sair da dívida em 30 dias", "plano de 30 dias pra sair")
  garantia   resultado garantido ("garanto que você vai faturar", "resultado garantido")
  cura       cura de doença ou dor
  antes-depois  antes e depois de corpo, pele ou saúde
  atributo   afirma atributo pessoal de quem lê ("você que está acima do peso")

Prazo de evento (turma, aula, acesso, garantia de 7 dias) e trecho negado
("não promete cura") não contam.
Cada achado sai como `arquivo:linha | tipo | trecho`, e a última linha é
`promessas de risco: N`. Exit 1 com N acima de 0, exit 0 com zero, exit 2 em erro
de leitura. O achado sai da peça na versão segura (forma aberta, sem prazo nem
garantia); o material do dono que trouxe a promessa não é licença.
"""
import json
import re
import sys
from pathlib import Path

NUM = r'(?:\d+|um|uma|dois|duas|tr[êe]s|quatro|cinco|sete|dez|quinze|vinte|trinta|sessenta|noventa)'
UNID = r'(?:dias?|semanas?|m[êe]s|meses|horas?)'
VERBO = (r'(?:sai[rs]?|perd\w*|emagre\w*|ganh\w*|fatur\w*|quit\w*|cur\w*|zer\w*|dobr\w*|'
         r'tripl\w*|acab\w*|elimin\w*|resolv\w*|conquist\w*|livr\w*|sec\w*|pag\w*|mud\w*)')
EVENTO = re.compile(r'garantia|acesso|aula|turma|come[çc]a|abre|encontro|ao vivo|inscri|'
                    r'vagas?|evento|live|desafio', re.I)
NEGA = re.compile(r'\b(?:n[ãa]o|nunca|sem|nem)\b', re.I)

REGRAS = [
    ('prazo', re.compile(rf'\b(?:em|at[ée]|dentro de|daqui a)\s+{NUM}\s+{UNID}\b', re.I), True),
    ('prazo', re.compile(rf'\b{NUM}\s+{UNID}\s+(?:pra|para)\s+{VERBO}', re.I), False),
    ('garantia', re.compile(r'\bgarant\w*\s+(?:que\s+)?(?:voc[êe]\s+)?(?:vai\s+|v[aã]o\s+)?'
                            + VERBO, re.I), False),
    ('garantia', re.compile(r'resultados?\s+garantid|100\s?%\s+garantid', re.I), False),
    ('cura', re.compile(r'\bcura(?:r|do|da|m)?\b|\bcurou\b', re.I), False),
    ('antes-depois', re.compile(r'antes\s+e\s+depois', re.I), False),
    ('atributo', re.compile(r'\bvoc[êe]\s+(?:que\s+)?(?:est[áa]|[ée]|tem|anda|vive)\s+'
                            r'(?:acima do peso|gord|obes|endividad|careca|calv|diab[ée]tic|'
                            r'deprimid|ansios|velh|fei[ao])', re.I), False),
]


def textos_do_json(dado, caminho=''):
    if isinstance(dado, dict):
        for k, v in dado.items():
            yield from textos_do_json(v, f'{caminho}.{k}' if caminho else k)
    elif isinstance(dado, list):
        for i, v in enumerate(dado):
            yield from textos_do_json(v, f'{caminho}[{i}]')
    elif isinstance(dado, str):
        yield caminho, dado


def linhas_do_arquivo(p):
    p = Path(p)
    bruto = p.read_text(encoding='utf-8', errors='replace')
    if p.suffix.lower() == '.json':
        try:
            return list(textos_do_json(json.loads(bruto)))
        except json.JSONDecodeError as e:
            raise ValueError(f'JSON inválido: {e}')
    return [(str(n), l) for n, l in enumerate(bruto.splitlines(), 1)]


def achados_da_linha(texto):
    out = []
    for tipo, rx, olha_evento in REGRAS:
        for m in rx.finditer(texto):
            if NEGA.search(texto[max(0, m.start() - 60):m.start()]):
                continue
            if olha_evento:
                janela = texto[max(0, m.start() - 40):m.end() + 20]
                if EVENTO.search(janela):
                    continue
            out.append((tipo, m.group(0)))
    return out


def checar(arquivos):
    total = 0
    for a in arquivos:
        try:
            linhas = linhas_do_arquivo(a)
        except (OSError, ValueError) as e:
            print(f'não li {a}: {e}', file=sys.stderr)
            return 2
        for onde, texto in linhas:
            for tipo, trecho in achados_da_linha(texto):
                total += 1
                print(f'{Path(a).name}:{onde} | {tipo} | {trecho}')
    print(f'promessas de risco: {total}')
    return 1 if total else 0


def selftest():
    ruins = ['O passo a passo pra sair da dívida em 30 dias, mesmo ganhando pouco.',
             'Um plano de 30 dias pra sair do cheque especial.',
             'Garanto que você vai faturar o dobro.',
             'Você que está acima do peso, olha isso.',
             'O protocolo que cura a lombar.',
             'Veja o antes e depois da aluna.']
    bons = ['Garantia de 7 dias: não gostou, devolvo.',
            'A turma começa em 12 dias.',
            'Acesso de 1 ano às aulas gravadas.',
            'O salário entra dia 5, e o cartão já avisa dia 8.',
            'Aula ao vivo em 3 dias, no link.',
            'O curso não promete emagrecimento ou cura com prazo fechado.']
    for f in ruins:
        assert achados_da_linha(f), f'devia marcar: {f}'
    for f in bons:
        assert not achados_da_linha(f), f'não devia marcar: {f} -> {achados_da_linha(f)}'
    print('checar_promessa.py self-test OK')
    return 0


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0 if args else 2)
    if args[0] in ('--selftest', '--self-test', '--test'):
        sys.exit(selftest())
    sys.exit(checar(args))
