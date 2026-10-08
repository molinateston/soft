#!/usr/bin/env python3
"""Passo 2 do ciclo de auto-melhoria: montar o gabarito.

A partir dos turnos coletados (coletar.py), olha a reação humana no turno
SEGUINTE a cada resposta do agente e usa essa reação como rótulo verdadeiro
de um caso. Três padrões de reação viram rótulo:

  corrigiu  – a pessoa aponta que a resposta anterior estava errada/incompleta
  cobrou    – a pessoa cobra status ("e aí?", "já subiu?") porque não ficou claro
  confirmou – a pessoa segue satisfeita (elogio, "isso mesmo", assunto novo)

Este exemplo de referência usa esses três padrões para rotular UMA pergunta
candidata: "a resposta do agente afirma ter terminado o trabalho sem mostrar
nenhuma prova (comando, teste, log, link)?" — rótulo `pronto_sem_prova`. É a
mesma pergunta usada como exemplo em medir.py, propor_sombra.py e
promover.py. Para medir outra pergunta, adapte as expressões abaixo ou
adicione outra chave ao dicionário `rotulos` de cada caso.

Regra de privacidade (vale também com dados reais): se o pedido ou a
resposta trouxer segredo, token ou dado de terceiro, descarte o caso em vez
de tentar mascarar — na dúvida, descarte.

Uso: montar_gabarito.py [--dir ESTADO]
"""
import argparse
import json
import os
import re
from pathlib import Path

TERMINOU = re.compile(r'\b(pronto|conclu[ií]d?[oa]?|finalizad[oa]|resolvid[oa]|terminei|corrigi|feito|sucesso|entreguei|publiquei|organizei)\b', re.I)
CORRIGIU = re.compile(r'(n[ãa]o (era|est[aá]) (isso|assim)|errad[oa]|n[ãa]o funcion|continua (quebrad|igual)|de novo\??|faltou|n[ãa]o (foi|deu))', re.I)
COBROU = re.compile(r'(e a[ií]\??|cad[eê]|j[aá] (subiu|terminou|fez)\??|n[ãa]o estou vendo|esqueceu|ainda n[ãa]o)', re.I)
CONFIRMOU = re.compile(r'(perfeito|valeu|show|isso mesmo|obrigad[oa]|[oó]timo|blz|beleza|fechou)', re.I)

ROTULO = 'pronto_sem_prova'  # rótulo que este exemplo produz; veja o docstring acima


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


def rotulo_pronto_sem_prova(resposta, reacao_seguinte):
    """True: a resposta afirmou ter terminado e a reação seguinte mostrou que não estava pronto (corrigiu).
    False: afirmou ter terminado e a reação seguinte confirmou que estava certo. None: não afirmou ter
    terminado, ou a reação seguinte não é decisiva (cobrança de status, por exemplo, não prova nada aqui)."""
    if not TERMINOU.search(resposta or ''):
        return None
    if CORRIGIU.search(reacao_seguinte or ''):
        return True
    if CONFIRMOU.search(reacao_seguinte or ''):
        return False
    return None


def monta(turnos):
    por_conversa = {}
    for t in turnos:
        por_conversa.setdefault(t['conversa_id'], []).append(t)
    casos = []
    for lista in por_conversa.values():
        lista.sort(key=lambda t: t['indice'])
        for i, t in enumerate(lista):
            if not t.get('resposta'):
                continue
            reacao = lista[i + 1]['pedido'] if i + 1 < len(lista) else ''
            y = rotulo_pronto_sem_prova(t['resposta'], reacao)
            if y is None:
                continue  # sem sinal decisivo: não vira caso (melhor faltar caso do que rotular errado)
            casos.append({
                'id': t['uid'], 'pedido': t['pedido'], 'resposta': t['resposta'], 'reacao_seguinte': reacao,
                'rotulos': {ROTULO: y}, 'fonte_rotulo': 'reacao_humana',
            })
    return casos


def main(argv=None):
    ap = argparse.ArgumentParser(description='Monta o gabarito de casos rotulados a partir dos turnos coletados.')
    ap.add_argument('--dir', help='Diretório de estado do ciclo (padrão: ~/.local/share/jev-auto/auto-melhoria).')
    a = ap.parse_args(argv)

    d = estado_dir(a.dir)
    turnos = ler_jsonl(d / 'turnos.jsonl')
    if not turnos:
        raise SystemExit('nenhum turno em turnos.jsonl — rode coletar.py primeiro')
    casos = monta(turnos)
    saida = d / 'gabarito.jsonl'
    gravar_jsonl(saida, casos)
    positivos = sum(1 for c in casos if c['rotulos'][ROTULO])
    print(json.dumps({'casos': len(casos), 'positivos': positivos, 'negativos': len(casos) - positivos,
                      'saida': str(saida)}, ensure_ascii=False))
    return casos


if __name__ == '__main__':
    main()
