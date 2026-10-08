#!/usr/bin/env python3
"""jev_decide.py: uma decisao do Jev (TypeSafe) pelo OpenRouter, em qualquer harness.

Uso:  python3 jev_decide.py '{"state": {...}, "questions": {...}}'
  ou: echo '{"state": {...}, "questions": {...}}' | python3 jev_decide.py

Chave: OPENROUTER_API_KEY no ambiente, ou o arquivo apontado por JEV_KEY_FILE (linha OPENROUTER_API_KEY=...).
Saida: JSON {"available": true, "answers": ..., "usage": ..., "ms": ...} ou {"available": false, "reason": ...}.
Nunca imprime a chave, nunca repete sozinho, prazo de 2 s (socket). So biblioteca padrao, Python 3.8+.
"""
import json
import math
import os
import re
import sys
import time
import urllib.request

URL = os.environ.get('JEV_URL', 'https://openrouter.ai/api/alpha/decisions')
MODEL = os.environ.get('JEV_MODEL', 'typesafe/jev-1.13')
TIMEOUT = float(os.environ.get('JEV_TIMEOUT', '2'))
LIMITE_BYTES = 48000
CAMPO_SEGREDO = re.compile(r'(?i)(password|senha|api[_-]?key|access[_-]?token|authorization|secret|private[_-]?key)')
CREDENCIAL = re.compile(r'(?i)(-----BEGIN .{0,30}PRIVATE KEY|\b(?:sk-|ghp_|github_pat_|xox[baprs]-)[A-Za-z0-9_-]{12,}|\beyJ[A-Za-z0-9_-]{20,}\.)')


def chave():
    k = os.environ.get('OPENROUTER_API_KEY', '')
    if k:
        return k
    arquivo = os.environ.get('JEV_KEY_FILE', '')
    if arquivo:
        try:
            with open(arquivo, encoding='utf-8') as f:
                for linha in f:
                    if linha.startswith('OPENROUTER_API_KEY='):
                        return linha.split('=', 1)[1].strip().strip('"').strip("'")
        except OSError:
            pass
    return ''


def tem_campo_segredo(valor):
    if isinstance(valor, dict):
        return any(CAMPO_SEGREDO.search(str(k)) or tem_campo_segredo(v) for k, v in valor.items())
    if isinstance(valor, list):
        return any(tem_campo_segredo(v) for v in valor)
    return False


def numero(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def valida(data, perguntas):
    if not isinstance(data, dict) or not str(data.get('model') or '').startswith(MODEL):
        raise ValueError('model')
    respostas = data.get('answers')
    if not isinstance(respostas, dict) or set(respostas) != set(perguntas):
        raise ValueError('questions')
    for nome, p in perguntas.items():
        r = respostas[nome]
        tipo = p.get('type')
        if not isinstance(r, dict) or r.get('type') != tipo:
            raise ValueError('type')
        if tipo == 'noul':
            if not numero(r.get('noul')) or not 0 <= r['noul'] <= 1:
                raise ValueError('noul')
        elif tipo == 'choice':
            probs = r.get('probabilities')
            if r.get('choice') not in p['criteria'] or not isinstance(probs, dict) or set(probs) != set(p['criteria']):
                raise ValueError('choice')
            if not numero(r.get('confidence')) or not 0 <= r['confidence'] <= 1:
                raise ValueError('confidence')
        elif tipo == 'score':
            if not numero(r.get('score')) or not numero(r.get('confidence')):
                raise ValueError('score')
        else:
            raise ValueError('type')
    return respostas


def confere_pedido(bruto):
    pedido = json.loads(bruto)
    if not isinstance(pedido, dict) or set(pedido) != {'state', 'questions'}:
        raise ValueError('formato esperado: {"state": ..., "questions": ...}')
    perguntas = pedido['questions']
    if not isinstance(perguntas, dict) or not 1 <= len(perguntas) <= 32:
        raise ValueError('de 1 a 32 perguntas')
    for nome, p in perguntas.items():
        if not re.fullmatch(r'[a-z][a-z0-9_]{0,47}', nome) or not isinstance(p, dict) or p.get('type') not in ('choice', 'noul', 'score'):
            raise ValueError('pergunta mal formada: ' + str(nome)[:40])
        if p['type'] == 'choice' and (not isinstance(p.get('criteria'), dict) or not 2 <= len(p['criteria']) <= 100):
            raise ValueError('choice precisa de 2 a 100 opcoes')
        if p['type'] == 'score' and (not isinstance(p.get('criteria'), list) or not 2 <= len(p['criteria']) <= 10):
            raise ValueError('score precisa de 2 a 10 niveis')
    if tem_campo_segredo(pedido['state']) or CREDENCIAL.search(bruto):
        raise ValueError('segredo no estado')
    if len(bruto.encode()) > LIMITE_BYTES:
        raise ValueError('acima de 48 KB')
    return pedido


def main():
    bruto = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    try:
        pedido = confere_pedido(bruto)
    except Exception as e:
        print(json.dumps({'available': False, 'reason': 'pedido_invalido', 'detail': str(e)[:80]}))
        return
    k = chave()
    if not k:
        print(json.dumps({'available': False, 'reason': 'missing_key'}))
        return
    corpo = json.dumps({'model': MODEL, 'state': pedido['state'], 'questions': pedido['questions']}, ensure_ascii=False).encode()
    req = urllib.request.Request(URL, data=corpo, headers={'Authorization': 'Bearer ' + k, 'Content-Type': 'application/json'})
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read(200001))
        respostas = valida(data, pedido['questions'])
    except Exception as e:
        texto = str(e).lower()
        motivo = 'timeout' if 'timed out' in texto else ('api_error' if hasattr(e, 'code') else 'invalid_response')
        print(json.dumps({'available': False, 'reason': motivo, 'ms': round((time.monotonic() - t0) * 1000)}))
        return
    print(json.dumps({'available': True, 'model': data.get('model'), 'answers': respostas, 'usage': data.get('usage'),
                      'ms': round((time.monotonic() - t0) * 1000), 'advisory_only': True}, ensure_ascii=False))


if __name__ == '__main__':
    main()
