#!/usr/bin/env python3
"""Passo 4 do ciclo de auto-melhoria: propor um candidato e rodar em sombra.

Olha os erros do texto de produção no gabarito (falso positivo e falso
negativo) e propõe um texto candidato. Aqui a "reflexão" é uma regra simples
e determinística — troca por palavras de um vocabulário fixo e curado, nunca
por trechos do texto real do usuário — só para não depender de chamar um
modelo de linguagem nesta implementação de referência; num sistema real,
esta etapa normalmente pede pra um LLM reescrever o texto olhando os erros
(é o que o próprio agente de codificação pode fazer, lendo os casos errados
e reescrevendo a pergunta).

O gabarito é sempre dividido em `selecao` (treino) e `teste` (congelado) por
`medir.dividir` — ver o docstring de lá. O candidato é proposto olhando só os
erros da `selecao`; "ganhou ou não" é decidido só no `teste`, que o candidato
nunca viu. É essa separação que evita o candidato parecer bom só por ter
decorado os erros do mesmo conjunto que o gerou.

O candidato só é gravado se ganhar da produção no teste, e sempre em modo
sombra (`sombra/candidatos.json`, estado "sombra"): nada aqui muda
producao.json. Se já existe um candidato em sombra para o mesmo rótulo, este
passo não gera outro — em vez disso, mede de novo o candidato existente
contra a produção nos casos de hoje e acrescenta ao diário de sombra
(`sombra/diario.jsonl`), que é o log que promover.py usa para julgar a
"semana em sombra".

Uso: propor_sombra.py [--dir ESTADO] [--rotulo pronto_sem_prova] [--teto N]
"""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import medir  # noqa: E402  (mesma pasta: reaproveita pontuacao_texto/medir/comparar/ganhou/estado_dir)

HOJE = dt.date.today().isoformat()


def caminho_sombra(d):
    return d / 'sombra' / 'candidatos.json'


def caminho_diario(d):
    return d / 'sombra' / 'diario.jsonl'


def erros(pergunta, casos, rotulo):
    """(falsos_positivos, falsos_negativos): casos em que a nota do texto atual erra o rótulo."""
    fp, fn = [], []
    for c in casos:
        y = (c.get('rotulos') or {}).get(rotulo)
        if y is None:
            continue
        pred = medir.pontuacao_texto(pergunta, c) >= pergunta['limiar']
        if pred and not y:
            fp.append(c)
        elif not pred and y:
            fn.append(c)
    return fp, fn


def gera_candidato(producao, falsos_positivos, falsos_negativos):
    """Só acrescenta palavras do vocabulário fixo encontradas nos casos errados; nunca copia texto livre."""
    candidato = json.loads(json.dumps(producao))  # cópia profunda simples
    novas_negativas, novas_positivas = [], []
    for c in falsos_positivos:
        texto = (c.get('resposta') or '').lower()
        for palavra in medir.VOCAB_PROVA:
            if palavra in texto and palavra not in candidato['pistas_negativas'] and palavra not in novas_negativas:
                novas_negativas.append(palavra)
    for c in falsos_negativos:
        texto = (c.get('resposta') or '').lower()
        for palavra in medir.VOCAB_TERMINOU:
            if palavra in texto and palavra not in candidato['pistas_positivas'] and palavra not in novas_positivas:
                novas_positivas.append(palavra)
    candidato['pistas_negativas'] = candidato['pistas_negativas'] + novas_negativas[:3]
    candidato['pistas_positivas'] = candidato['pistas_positivas'] + novas_positivas[:3]
    mudou = bool(novas_negativas[:3] or novas_positivas[:3])
    return candidato, mudou


def registra_diario(d, rotulo, producao, candidato, casos, orcamento=None):
    comparacao = medir.comparar(producao, candidato, casos, rotulo, orcamento)
    linhas = []
    for c in casos:
        y = (c.get('rotulos') or {}).get(rotulo)
        if y is None:
            continue
        linhas.append({
            'data': HOJE, 'rotulo': rotulo, 'caso_id': c['id'], 'y': y,
            'ok_producao': comparacao['producao']['por_caso'].get(c['id']),
            'ok_candidato': comparacao['candidato']['por_caso'].get(c['id']),
        })
    caminho = caminho_diario(d)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, 'a', encoding='utf-8') as f:
        for l in linhas:
            f.write(json.dumps(l, ensure_ascii=False) + '\n')
    return len(linhas)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Propõe um candidato a partir dos erros da produção e o roda em sombra.')
    ap.add_argument('--dir', help='Diretório de estado do ciclo (padrão: ~/.local/share/jev-auto/auto-melhoria).')
    ap.add_argument('--rotulo', default=medir.PRODUCAO_PADRAO['id'])
    ap.add_argument('--teto', type=int, default=0, help='Teto de chamadas ao julgador por dia (0 = sem limite). Só importa depois que pontuacao_texto vira uma chamada paga.')
    a = ap.parse_args(argv)

    d = medir.estado_dir(a.dir)
    casos = medir.carregar_gabarito(d)
    selecao, teste = medir.dividir(d, a.rotulo, casos)
    producao = medir.carregar_producao(d)
    orc = medir.Orcamento(d, a.rotulo, a.teto) if a.teto else None
    todos = medir.ler_json(caminho_sombra(d), {}) or {}
    existente = todos.get(a.rotulo)

    if existente and existente.get('estado') == 'sombra':
        candidato = existente['pergunta']
        n_dia = registra_diario(d, a.rotulo, producao, candidato, teste, orc)
        print(json.dumps({'acao': 'medido_em_sombra', 'rotulo': a.rotulo, 'candidato_id': existente['id'],
                          'casos_do_dia': n_dia, 'gerado_em': existente['gerado_em']}, ensure_ascii=False))
        return

    fp, fn = erros(producao, selecao, a.rotulo)
    if not fp and not fn:
        print(json.dumps({'acao': 'nada_a_propor', 'rotulo': a.rotulo, 'motivo': 'produção não errou nenhum caso da seleção (treino) atual'}, ensure_ascii=False))
        return
    candidato, mudou = gera_candidato(producao, fp, fn)
    if not mudou:
        print(json.dumps({'acao': 'nada_a_propor', 'rotulo': a.rotulo,
                          'motivo': 'os casos errados não trazem nenhuma palavra do vocabulário fixo ainda não usada'}, ensure_ascii=False))
        return
    if not teste:
        print(json.dumps({'acao': 'sem_teste', 'rotulo': a.rotulo,
                          'motivo': 'gabarito pequeno demais: nenhum caso caiu no lado de teste ainda; rode montar_gabarito.py com mais casos'}, ensure_ascii=False))
        return
    comparacao = medir.comparar(producao, candidato, teste, a.rotulo, orc)
    if not medir.ganhou(comparacao['producao'], comparacao['candidato']):
        print(json.dumps({'acao': 'candidato_pior_ou_igual', 'rotulo': a.rotulo,
                          'antes': comparacao['producao'], 'depois': comparacao['candidato']}, ensure_ascii=False, indent=1))
        return

    registro = {
        'id': f'cand-{a.rotulo}-{HOJE}', 'pergunta': candidato,
        'antes': {k: v for k, v in comparacao['producao'].items() if k != 'por_caso'},
        'depois': {k: v for k, v in comparacao['candidato'].items() if k != 'por_caso'},
        'gerado_em': HOJE, 'estado': 'sombra',
        'historico': [{'at': HOJE, 'para': 'sombra', 'motivo': 'ganhou da produção no teste congelado'}],
    }
    todos[a.rotulo] = registro
    medir.gravar_json(caminho_sombra(d), todos)
    registra_diario(d, a.rotulo, producao, candidato, teste, orc)
    print(json.dumps({'acao': 'gravado_em_sombra', 'rotulo': a.rotulo, 'candidato_id': registro['id'],
                      'antes': registro['antes'], 'depois': registro['depois']}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
