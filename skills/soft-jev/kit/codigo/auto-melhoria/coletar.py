#!/usr/bin/env python3
"""Passo 1 do ciclo de auto-melhoria: coleta.

Lê históricos de conversa de um diretório configurável e produz uma lista de
turnos (pedido do usuário + resposta do agente naquele turno), em ordem, para
o passo seguinte (montar_gabarito.py) olhar a reação ao turno anterior.

Este script só lê e organiza; nenhum rótulo é decidido aqui.

Formato esperado de cada arquivo de entrada (um JSON por linha):
  {"conversa_id": "c1", "indice": 0, "quando": "2026-09-01T10:00:00",
   "pedido": "texto que o usuário pediu", "resposta": "texto que o agente respondeu"}

Sem --entrada (ou diretório vazio/inexistente), usa um conjunto pequeno de
turnos fictícios embutidos, só para os próximos passos terem o que processar
na primeira vez que alguém rodar o ciclo.

Uso: coletar.py [--entrada DIR] [--dir ESTADO]
"""
import argparse
import json
import os
from pathlib import Path

# ── conjunto fictício embutido (nenhum dado real; só para demonstração) ───
TURNOS_EXEMPLO = [
    {"conversa_id": "demo-1", "indice": 0, "quando": "2026-09-01T09:00:00",
     "pedido": "corrige o link quebrado da página de contato",
     "resposta": "Pronto, corrigi o link e já está funcionando."},
    {"conversa_id": "demo-1", "indice": 1, "quando": "2026-09-01T09:20:00",
     "pedido": "continua quebrado aqui, não era esse o link", "resposta": ""},
    {"conversa_id": "demo-2", "indice": 0, "quando": "2026-09-02T14:00:00",
     "pedido": "resume os comentários da última postagem",
     "resposta": "Terminei o resumo, rodei o script de contagem e confirmei "
                 "que bateu com o total mostrado no painel."},
    {"conversa_id": "demo-2", "indice": 1, "quando": "2026-09-02T14:10:00",
     "pedido": "perfeito, era isso mesmo", "resposta": ""},
    {"conversa_id": "demo-3", "indice": 0, "quando": "2026-09-03T11:00:00",
     "pedido": "sobe a nova versão do site em produção",
     "resposta": "Pronto, subida concluída com sucesso."},
    {"conversa_id": "demo-3", "indice": 1, "quando": "2026-09-03T15:00:00",
     "pedido": "e aí, já subiu? não estou vendo a mudança no ar",
     "resposta": ""},
    {"conversa_id": "demo-4", "indice": 0, "quando": "2026-09-04T08:00:00",
     "pedido": "qual o motivo do erro no processamento de ontem?",
     "resposta": "Não sei, você pode olhar o log e me contar o que apareceu?"},
    {"conversa_id": "demo-4", "indice": 1, "quando": "2026-09-04T08:05:00",
     "pedido": "isso é trabalho seu, olha você mesmo o log", "resposta": ""},
    {"conversa_id": "demo-5", "indice": 0, "quando": "2026-09-05T10:00:00",
     "pedido": "organiza a planilha de gastos do mês",
     "resposta": "Organizei a planilha, conferi as somas por categoria e "
                 "deixei um resumo no topo com o link do arquivo."},
    {"conversa_id": "demo-5", "indice": 1, "quando": "2026-09-05T10:30:00",
     "pedido": "show, valeu", "resposta": ""},
    {"conversa_id": "demo-6", "indice": 0, "quando": "2026-09-06T09:00:00",
     "pedido": "atualiza o preço da tabela para o novo valor combinado",
     "resposta": "Pronto, atualizei o preço para o novo valor e já está publicado."},
    {"conversa_id": "demo-6", "indice": 1, "quando": "2026-09-06T09:15:00",
     "pedido": "não era esse valor, está errado ainda", "resposta": ""},
    {"conversa_id": "demo-7", "indice": 0, "quando": "2026-09-07T13:00:00",
     "pedido": "atualiza a lista de preços do catálogo",
     "resposta": "Terminei a atualização, conferi os valores no painel e ficou certo."},
    {"conversa_id": "demo-7", "indice": 1, "quando": "2026-09-07T13:10:00",
     "pedido": "perfeito, exatamente isso", "resposta": ""},
]


def estado_dir(caminho=None):
    base = caminho or os.environ.get('JEV_AUTOMELHORIA_DIR') or str(Path.home() / '.local/share/jev-auto/auto-melhoria')
    p = Path(base)
    p.mkdir(parents=True, exist_ok=True)
    return p


def ler_jsonl(caminho):
    out = []
    try:
        for linha in Path(caminho).read_text(encoding='utf-8').splitlines():
            linha = linha.strip()
            if linha:
                out.append(json.loads(linha))
    except FileNotFoundError:
        pass
    return out


def gravar_jsonl(caminho, itens):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        for item in itens:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def coletar_de(diretorio):
    """Lê todo *.jsonl de um diretório de históricos; devolve turnos normalizados ou [] se não houver nada."""
    d = Path(diretorio)
    if not d.is_dir():
        return []
    turnos = []
    for arq in sorted(d.glob('*.jsonl')):
        for linha in ler_jsonl(arq):
            if 'pedido' not in linha:
                continue  # linha fora do formato esperado: ignora em vez de derrubar o passo inteiro
            turnos.append({
                'conversa_id': linha.get('conversa_id') or arq.stem,
                'indice': linha.get('indice', 0),
                'quando': linha.get('quando') or '',
                'pedido': linha.get('pedido') or '',
                'resposta': linha.get('resposta') or '',
            })
    return turnos


def main(argv=None):
    ap = argparse.ArgumentParser(description='Coleta turnos de conversa para o ciclo de auto-melhoria.')
    ap.add_argument('--entrada', help='Diretório com *.jsonl de históricos de conversa (opcional).')
    ap.add_argument('--dir', help='Diretório de estado do ciclo (padrão: ~/.local/share/jev-auto/auto-melhoria).')
    a = ap.parse_args(argv)

    turnos = coletar_de(a.entrada) if a.entrada else []
    fonte = 'entrada real' if turnos else 'exemplo embutido (sem --entrada ou diretório vazio)'
    if not turnos:
        turnos = [dict(t) for t in TURNOS_EXEMPLO]

    turnos.sort(key=lambda t: (t['conversa_id'], t['indice']))
    for i, t in enumerate(turnos):
        t['uid'] = f"{t['conversa_id']}:{t['indice']}"

    saida = estado_dir(a.dir) / 'turnos.jsonl'
    gravar_jsonl(saida, turnos)
    print(json.dumps({'turnos': len(turnos), 'fonte': fonte, 'saida': str(saida)}, ensure_ascii=False))
    return turnos


if __name__ == '__main__':
    main()
