#!/usr/bin/env python3
"""Passo 5 do ciclo de auto-melhoria: promover (ou não) um candidato em sombra.

Para cada candidato em `sombra/candidatos.json` que já está em sombra há pelo
menos `--dias-minimos` dias (padrão 7 — uma semana), decide, nesta ordem:

  1. Ganhou da produção no teste congelado (o mesmo teste de `propor_sombra.py`,
     nunca usado para gerar o candidato)? Se não, REPROVADO.
  2. Piorou durante a semana em sombra (`sombra/diario.jsonl`, só conta com
     5+ medições no período)? Se sim, REPROVADO.
  3. Piorou algum caso de `casos_estaveis.json` — casos fixos que a produção
     acerta e que ninguém quer ver quebrar (medidos de novo agora, não
     reaproveitados de um dia anterior)? Se sim, BLOQUEADO (fica registrado,
     não é descartado: pode voltar a ser avaliado na próxima rodada).
  4. Senão, ATIVO: o candidato vira a nova produção (`producao.json` é
     sobrescrito) e some da lista de sombra — na próxima rodada,
     `propor_sombra.py` volta a gerar candidatos a partir dessa nova
     produção.

Nada aqui é apagado: candidato reprovado ou bloqueado continua no arquivo,
com o motivo e um histórico de decisões, só para nunca perder o rastro do
porquê.

Simplificação assumida de propósito (documentada aqui para não confundir
com o sistema original que inspirou este kit): a checagem de "caso estável"
mede uma vez, no momento da promoção, em vez de exigir dois dias seguidos de
falha antes de bloquear. Isso é mais simples e mais conservador (bloqueia
mais fácil), ao custo de eventualmente bloquear por uma falha de sorte num
caso só; para um gabarito pequeno como o deste kit, esse é o lado seguro do
erro.

Uso: promover.py [--dir ESTADO] [--rotulo pronto_sem_prova] [--dias-minimos 7]
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import medir  # noqa: E402
from propor_sombra import caminho_sombra, caminho_diario  # noqa: E402

HOJE = dt.date.today().isoformat()
MIN_MEDICOES_SEMANA = 5


def dias_desde(data):
    try:
        return (dt.date.fromisoformat(HOJE) - dt.date.fromisoformat(data)).days
    except (ValueError, TypeError):
        return 0


def semana(d, rotulo, dias):
    ini = (dt.date.fromisoformat(HOJE) - dt.timedelta(days=dias)).isoformat()
    linhas = [l for l in medir.ler_jsonl(caminho_diario(d)) if l.get('rotulo') == rotulo and l.get('data', '') >= ini]
    n = len(linhas)
    okp = sum(1 for l in linhas if l.get('ok_producao'))
    okc = sum(1 for l in linhas if l.get('ok_candidato'))
    return n, okp, okc


def carregar_casos_estaveis(d):
    arq = d / 'casos_estaveis.json'
    if arq.exists():
        return medir.ler_json(arq, [])
    padrao = Path(__file__).resolve().parent / 'casos_estaveis.json'
    return json.loads(padrao.read_text(encoding='utf-8'))


def regressoes(producao, candidato, casos_estaveis, rotulo):
    """Casos estáveis em que a produção acerta hoje e o candidato erra hoje."""
    mp = medir.medir(producao, casos_estaveis, rotulo)
    mc = medir.medir(candidato, casos_estaveis, rotulo)
    return [cid for cid, ok in mp['por_caso'].items() if ok and not mc['por_caso'].get(cid, False)]


def decidir(d, rotulo, candidato_registro, dias_minimos):
    n, okp, okc = semana(d, rotulo, dias=7)
    if not medir.ganhou(candidato_registro['antes'], candidato_registro['depois']):
        return 'reprovada', 'não ganhou da produção no teste congelado'
    if n >= MIN_MEDICOES_SEMANA and okc < okp:
        return 'reprovada', f'piorou na semana em sombra ({okc} acerto(s) do candidato × {okp} da produção em {n} medições)'
    producao = medir.carregar_producao(d)
    casos_estaveis = carregar_casos_estaveis(d)
    estaveis_quebrados = regressoes(producao, candidato_registro['pergunta'], casos_estaveis, rotulo)
    if estaveis_quebrados:
        return 'bloqueada', f"piorou {len(estaveis_quebrados)} caso(s) estável(is) que a produção acerta: {', '.join(estaveis_quebrados[:3])}"
    return 'ativa', f"teste {candidato_registro['antes'].get('acerto')} → {candidato_registro['depois'].get('acerto')}; semana {okc}/{n} × {okp}/{n} (mín. {MIN_MEDICOES_SEMANA} medições para contar)"


def main(argv=None):
    ap = argparse.ArgumentParser(description='Promove (ou reprova/bloqueia) candidatos que já passaram tempo suficiente em sombra.')
    ap.add_argument('--dir', help='Diretório de estado do ciclo (padrão: ~/.local/share/jev-auto/auto-melhoria).')
    ap.add_argument('--rotulo', default=medir.PRODUCAO_PADRAO['id'])
    ap.add_argument('--dias-minimos', type=int, default=7, help='Dias mínimos em sombra antes de considerar promoção (padrão 7; use 0 para forçar no mesmo dia, ex.: para testar o fluxo).')
    a = ap.parse_args(argv)

    d = medir.estado_dir(a.dir)
    todos = medir.ler_json(caminho_sombra(d), {}) or {}
    candidato_registro = todos.get(a.rotulo)

    if not candidato_registro or candidato_registro.get('estado') != 'sombra':
        resultado = {'acao': 'nada_a_promover', 'rotulo': a.rotulo, 'motivo': 'nenhum candidato em sombra para este rótulo'}
        print(json.dumps(resultado, ensure_ascii=False))
        return resultado

    maturidade = dias_desde(candidato_registro.get('gerado_em', HOJE))
    if maturidade < a.dias_minimos:
        resultado = {'acao': 'ainda_nao_maduro', 'rotulo': a.rotulo, 'dias_em_sombra': maturidade, 'dias_minimos': a.dias_minimos}
        print(json.dumps(resultado, ensure_ascii=False))
        return resultado

    estado, motivo = decidir(d, a.rotulo, candidato_registro, a.dias_minimos)
    if estado == 'ativa':
        medir.gravar_json(d / 'producao.json', candidato_registro['pergunta'])
        motivo += '; producao.json atualizado com o texto do candidato'

    candidato_registro.setdefault('historico', []).append({'at': HOJE, 'para': estado, 'motivo': motivo})
    candidato_registro['estado'] = estado
    todos[a.rotulo] = candidato_registro
    medir.gravar_json(caminho_sombra(d), todos)

    resultado = {'acao': estado, 'rotulo': a.rotulo, 'candidato_id': candidato_registro['id'], 'motivo': motivo}
    print(json.dumps(resultado, ensure_ascii=False, indent=1))
    return resultado


if __name__ == '__main__':
    main()
