#!/usr/bin/env python3
"""Passo 3 do ciclo de auto-melhoria: medir.

Mede um texto de pergunta (produção ou candidato) contra o gabarito, com as
métricas que decidem se um texto é melhor que outro: taxa de falso positivo,
acerto, precisão, cobertura e AUC — mais o custo (número de vezes que o
julgador foi chamado). `comparar` mede dois textos no MESMO conjunto de
casos, na mesma rodada (medição pareada): é assim que dá para dizer que um
texto "ganhou" do outro sem confundir com o conjunto de casos ter mudado.

Ponto de extensão: `pontuacao_texto(pergunta, caso)` decide, para um caso,
que probabilidade de "sim" o texto de pergunta dado atribuiria a ele. Aqui,
para rodar sem chave nem rede, é uma heurística de palavras determinística.
Para usar com o serviço de verdade, troque o corpo desta função por uma
chamada ao mesmo julgador usado pelo `jev ask` deste kit (a credencial é a
variável de ambiente TYPESAFE_API_KEY), mantendo a assinatura.

Uso: medir.py [--dir ESTADO] [--pergunta ARQ.json] [--candidato ARQ.json]
Sem argumentos, mede a produção sozinha e depois compara com um candidato de
exemplo, só para mostrar o formato da saída.
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
import sys
from pathlib import Path

# Vocabulário fixo de "palavras de prova": só destas o judge tira sinal negativo (nunca de texto livre do
# usuário) — é o mesmo cuidado que propor_sombra.py usa para nunca copiar texto de caso real para a pergunta.
VOCAB_PROVA = ['rodei', 'testei', 'conferi', 'confirmei', 'log', 'comando', 'script', 'print', 'saída',
               'bateu', 'painel']
VOCAB_TERMINOU = ['pronto', 'conclu', 'finalizad', 'resolvid', 'terminei', 'corrigi', 'feito', 'sucesso',
                  'entreguei', 'publiquei', 'atualizei', 'organizei']

CASOS_EXEMPLO = [
    {"id": "demo-1:0", "resposta": "Pronto, corrigi o link e já está funcionando.", "rotulos": {"pronto_sem_prova": True}},
    {"id": "demo-2:0", "resposta": "Terminei o resumo, rodei o script de contagem e confirmei que bateu com o total mostrado no painel.", "rotulos": {"pronto_sem_prova": False}},
    {"id": "demo-5:0", "resposta": "Organizei a planilha, conferi as somas por categoria e deixei um resumo no topo com o link do arquivo.", "rotulos": {"pronto_sem_prova": False}},
    {"id": "demo-6:0", "resposta": "Pronto, atualizei o preço para o novo valor e já está publicado.", "rotulos": {"pronto_sem_prova": True}},
]

PRODUCAO_PADRAO = {
    'id': 'pronto_sem_prova',
    'texto': 'A resposta afirma ter terminado o trabalho sem mostrar nenhuma prova (comando, teste, log, link)?',
    'pistas_positivas': list(VOCAB_TERMINOU),
    'pistas_negativas': ['rodei', 'testei'],  # incompleta de propósito: é o que propor_sombra.py vai melhorar
    'limiar': 0.5,
}


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


def ler_json(caminho, padrao=None):
    try:
        return json.loads(Path(caminho).read_text(encoding='utf-8'))
    except FileNotFoundError:
        return padrao


def gravar_json(caminho, obj):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def carregar_gabarito(d):
    casos = ler_jsonl(d / 'gabarito.jsonl')
    return casos if casos else [dict(c) for c in CASOS_EXEMPLO]


def carregar_producao(d):
    p = ler_json(d / 'producao.json')
    if p is None:
        p = dict(PRODUCAO_PADRAO)
        gravar_json(d / 'producao.json', p)
    return p


def _fracao_hash(semente, caso_id):
    return int(hashlib.sha256(f'{semente}:{caso_id}'.encode()).hexdigest()[:8], 16) / 2 ** 32


def dividir(d, rotulo, casos, fracao_teste=0.4, semente=42):
    """(selecao, teste): separa os casos com rótulo em treino (selecao, usado para gerar um candidato) e
    teste (congelado, só para julgar se um candidato "ganhou"). Estratifica por rótulo na 1ª vez (mesma
    fração de positivos e negativos nos dois lados, por ordem de hash); depois os ids ficam congelados em
    `divisao.json` — caso novo entra no teste se sha256(f'{semente}:id') cair abaixo da fração de teste, sem
    nunca remexer nos ids antigos. Sem essa separação, um candidato que só decorou os erros do texto de
    produção pareceria sempre "melhor" ao ser medido no mesmo conjunto que o gerou (a "cola" mais óbvia de
    avaliação): é por isso que `propor_sombra.py` gera o candidato olhando só a `selecao` e decide "ganhou
    ou não" olhando só o `teste`."""
    caminho = d / 'divisao.json'
    congelado = ler_json(caminho, None) or {'semente': semente, 'fracao_teste': fracao_teste, 'rotulos': {}}
    info = congelado['rotulos'].get(rotulo)
    ids_com_rotulo = [c['id'] for c in casos if (c.get('rotulos') or {}).get(rotulo) is not None]
    if info is None:
        teste = set()
        for y in (True, False):
            grupo = sorted((c['id'] for c in casos if (c.get('rotulos') or {}).get(rotulo) == y),
                           key=lambda cid: _fracao_hash(semente, cid))
            teste |= set(grupo[:round(len(grupo) * fracao_teste)])
        info = {'teste': sorted(teste), 'selecao': sorted(i for i in ids_com_rotulo if i not in teste)}
        mudou = True
    else:
        conhecidos = set(info['teste']) | set(info['selecao'])
        novos = [i for i in ids_com_rotulo if i not in conhecidos]
        for n in novos:
            info['teste' if _fracao_hash(semente, n) < fracao_teste else 'selecao'].append(n)
        mudou = bool(novos)
    if mudou:
        congelado['rotulos'][rotulo] = info
        gravar_json(caminho, congelado)
    ids_selecao, ids_teste = set(info['selecao']), set(info['teste'])
    return [c for c in casos if c['id'] in ids_selecao], [c for c in casos if c['id'] in ids_teste]


def _ledger_path(d):
    return d / 'ledger.jsonl'


def gasto_hoje(d, rotulo, hoje=None):
    """Chamadas já gastas hoje para este rótulo, somando todas as rodadas de todos os scripts do ciclo (o
    ledger é compartilhado: `medir.py`, `propor_sombra.py` e `promover.py` gravam nele)."""
    hoje = hoje or dt.date.today().isoformat()
    return sum(l.get('chamadas', 0) for l in ler_jsonl(_ledger_path(d)) if l.get('data') == hoje and l.get('rotulo') == rotulo)


def registra_gasto(d, rotulo, chamadas, hoje=None):
    if chamadas <= 0:
        return
    caminho = _ledger_path(d)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'data': hoje or dt.date.today().isoformat(), 'rotulo': rotulo, 'chamadas': chamadas}, ensure_ascii=False) + '\n')


class Orcamento:
    """Teto de chamadas ao julgador por dia, por rótulo. Enquanto `pontuacao_texto` é a heurística local
    grátis deste kit, o teto não muda nada na prática — mas ele já fica ativo e compartilhado (mesmo ledger
    entre os scripts do ciclo) desde já, então, no dia em que você trocar `pontuacao_texto` por uma chamada
    paga de verdade ao julgador, o ciclo já para sozinho ao bater o teto do dia, sem precisar mexer em mais
    nada. Sem teto (`--teto 0` ou omitido = sem limite), `pode()` sempre devolve True."""

    def __init__(self, d, rotulo, teto):
        self.d, self.rotulo, self.teto = d, rotulo, (teto or None)
        self.hoje = dt.date.today().isoformat()
        self.gastas_no_inicio = gasto_hoje(d, rotulo, self.hoje)
        self.gastas_agora = 0

    def pode(self, n=1):
        return self.teto is None or (self.gastas_no_inicio + self.gastas_agora + n) <= self.teto

    def gasta(self, n=1):
        self.gastas_agora += n
        registra_gasto(self.d, self.rotulo, n, self.hoje)

    def restante(self):
        return None if self.teto is None else max(0, self.teto - self.gastas_no_inicio - self.gastas_agora)


def pontuacao_texto(pergunta, caso):
    """Probabilidade (0 a 1) de que o rótulo seja "sim" para este caso, segundo o texto de pergunta dado.
    Substitua por uma chamada real ao julgador (ver docstring do módulo); a assinatura deve continuar
    (pergunta, caso) -> float."""
    texto = (caso.get('resposta') or '').lower()
    positivas = sum(1 for p in pergunta['pistas_positivas'] if p in texto)
    negativas = sum(1 for p in pergunta['pistas_negativas'] if p in texto)
    bruto = positivas - 2 * negativas  # cada pista de prova pesa o dobro: "mostrou prova" deve dominar
    return 1 / (1 + math.exp(-bruto))


def auc(pos, neg):
    """Probabilidade de um caso positivo tirar nota maior que um negativo (empate conta meio ponto)."""
    if not pos or not neg:
        return None
    ganho = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return ganho / (len(pos) * len(neg))


def medir(pergunta, casos, rotulo, orcamento=None):
    """Métricas de `pergunta` no conjunto `casos`, mais o custo (nº de casos efetivamente pontuados). Se um
    `orcamento` (Orcamento) for passado e o teto do dia já tiver sido atingido, os casos restantes são
    ignorados (contam em `ignorados_por_teto`, não em `n`) em vez de estourar o teto."""
    pontos, custo, ignorados = [], 0, 0
    for c in casos:
        y = (c.get('rotulos') or {}).get(rotulo)
        if y is None:
            continue
        if orcamento is not None and not orcamento.pode(1):
            ignorados += 1
            continue
        pontos.append((pontuacao_texto(pergunta, c), bool(y), c['id']))
        custo += 1
        if orcamento is not None:
            orcamento.gasta(1)
    lim = pergunta['limiar']
    tp = sum(1 for s, y, _ in pontos if s >= lim and y)
    fp = sum(1 for s, y, _ in pontos if s >= lim and not y)
    fn = sum(1 for s, y, _ in pontos if s < lim and y)
    tn = sum(1 for s, y, _ in pontos if s < lim and not y)
    n = len(pontos)
    m = {
        'n': n, 'custo': custo,
        'acerto': round((tp + tn) / n, 4) if n else None,
        'precisao': round(tp / (tp + fp), 4) if (tp + fp) else None,
        'cobertura': round(tp / (tp + fn), 4) if (tp + fn) else None,
        'falso_positivo': round(fp / (fp + tn), 4) if (fp + tn) else None,
        'auc': (lambda v: round(v, 4) if v is not None else None)(auc([s for s, y, _ in pontos if y], [s for s, y, _ in pontos if not y])),
    }
    if ignorados:
        m['ignorados_por_teto'] = ignorados
    m['por_caso'] = {cid: (s >= lim) == y for s, y, cid in pontos}
    return m


def comparar(producao, candidato, casos, rotulo, orcamento=None):
    """Mede os dois textos no MESMO conjunto de casos (medição pareada) e devolve os dois resultados. Os
    dois lados compartilham o mesmo `orcamento`, se houver um."""
    return {'producao': medir(producao, casos, rotulo, orcamento), 'candidato': medir(candidato, casos, rotulo, orcamento)}


def ganhou(antes, depois):
    """Candidato só "ganha" se acerta mais; em empate de acerto, desempata por AUC (separa melhor os dois lados)."""
    if depois.get('acerto') is None or antes.get('acerto') is None:
        return False
    if depois['acerto'] > antes['acerto']:
        return True
    return depois['acerto'] >= antes['acerto'] and (depois.get('auc') or 0) > (antes.get('auc') or 0)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Mede um texto de pergunta (ou dois, pareado) contra o gabarito.')
    ap.add_argument('--dir', help='Diretório de estado do ciclo (padrão: ~/.local/share/jev-auto/auto-melhoria).')
    ap.add_argument('--pergunta', help='Arquivo JSON com o texto a medir (padrão: producao.json do diretório de estado).')
    ap.add_argument('--candidato', help='Arquivo JSON com um segundo texto, para comparar pareado com o primeiro.')
    ap.add_argument('--rotulo', default=PRODUCAO_PADRAO['id'], help='Chave de rótulo dentro de cada caso (padrão: pronto_sem_prova).')
    ap.add_argument('--teto', type=int, default=0, help='Teto de chamadas ao julgador por dia (0 = sem limite). Só importa depois que pontuacao_texto vira uma chamada paga.')
    a = ap.parse_args(argv)

    d = estado_dir(a.dir)
    casos = carregar_gabarito(d)
    pergunta = ler_json(a.pergunta) if a.pergunta else carregar_producao(d)
    orc = Orcamento(d, a.rotulo, a.teto) if a.teto else None
    candidato_arq = a.candidato
    if candidato_arq is None and a.pergunta is None and (argv is None and len(sys.argv) == 1):
        # sem nenhum argumento: além de medir a produção, mostra a comparação pareada com um candidato de
        # exemplo (mesma ideia do passo 4), só para ilustrar o formato de saída de um "ganhou ou não".
        candidato = {**pergunta, 'pistas_negativas': pergunta['pistas_negativas'] + ['conferi', 'painel', 'link']}
    elif candidato_arq:
        candidato = ler_json(candidato_arq)
    else:
        candidato = None

    if candidato is not None:
        saida = comparar(pergunta, candidato, casos, a.rotulo, orc)
        saida['ganhou'] = ganhou(saida['producao'], saida['candidato'])
    else:
        saida = medir(pergunta, casos, a.rotulo, orc)
        saida.pop('por_caso', None)
    print(json.dumps(saida, ensure_ascii=False, indent=1))
    return saida


if __name__ == '__main__':
    main()
