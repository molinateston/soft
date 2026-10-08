#!/usr/bin/env python3
"""Passo do ciclo de auto-melhoria: calibrar o limiar.

`propor_sombra.py` só mexe no TEXTO da pergunta. Este script mexe no LIMIAR:
se o texto de produção está acertando pouco no gabarito, sobe o limiar aos
poucos (nunca desce sozinho) até o acerto voltar a um nível aceitável, ou até
um teto de segurança. Nunca muda o texto, só o número em `producao.json`.

Só mexe se houver casos suficientes (`--min-casos`, padrão 12 — baixo de
propósito para o gabarito de exemplo deste kit; num gabarito real, prefira
algo como 30+, como no sistema original). Com poucos casos, qualquer limiar
parece bom ou ruim por acaso; subir o limiar nesse regime só adicionaria
ruído.

Cada rodada grava uma linha em `calibracao-historico.jsonl`, mudando ou não o
limiar, para dar para acompanhar a métrica ao longo do tempo mesmo nos dias
em que nada mudou.

Uso: calibrar_limiar.py [--dir ESTADO] [--rotulo pronto_sem_prova]
                        [--alvo-acerto 0.70] [--min-casos 12] [--teto-limiar 0.95]
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import medir  # noqa: E402

HOJE = dt.date.today().isoformat()


def calibrar(d, rotulo, alvo_acerto=0.70, min_casos=12, teto_limiar=0.95, passo=0.05):
    casos = medir.carregar_gabarito(d)
    producao = medir.carregar_producao(d)
    m = medir.medir(producao, casos, rotulo)
    resultado = {'rotulo': rotulo, 'limiar_antes': producao['limiar'], 'metricas': {k: v for k, v in m.items() if k != 'por_caso'}}

    if m['n'] < min_casos:
        resultado['mudou'] = False
        resultado['motivo'] = f"só {m['n']} caso(s) rotulado(s) (mínimo {min_casos}) — não mexe no limiar com tão pouco dado"
        return resultado

    if m['acerto'] is not None and m['acerto'] >= alvo_acerto:
        resultado['mudou'] = False
        resultado['motivo'] = f"acerto {m['acerto']:.0%} já está em ou acima do alvo ({alvo_acerto:.0%})"
        return resultado

    novo_limiar = None
    limiar_atual = producao['limiar']
    passos = int(round((teto_limiar - limiar_atual) / passo)) + 1
    for k in range(1, max(passos, 1) + 1):
        candidato_limiar = round(min(teto_limiar, limiar_atual + passo * k), 4)
        candidato = {**producao, 'limiar': candidato_limiar}
        mm = medir.medir(candidato, casos, rotulo)
        if (mm['acerto'] or 0) >= alvo_acerto:
            novo_limiar = candidato_limiar
            break
        if candidato_limiar >= teto_limiar:
            novo_limiar = candidato_limiar
            break

    if novo_limiar is None or novo_limiar == limiar_atual:
        resultado['mudou'] = False
        resultado['motivo'] = f"acerto {m['acerto']:.0%} abaixo do alvo, mas já está no teto de limiar ({teto_limiar})"
        return resultado

    producao['limiar'] = novo_limiar
    medir.gravar_json(d / 'producao.json', producao)
    resultado['mudou'] = True
    resultado['limiar_depois'] = novo_limiar
    resultado['motivo'] = f"acerto {m['acerto']:.0%} abaixo do alvo ({alvo_acerto:.0%}): limiar {limiar_atual} → {novo_limiar}"
    return resultado


def main(argv=None):
    ap = argparse.ArgumentParser(description='Sobe o limiar da pergunta de produção quando o acerto cai abaixo do alvo.')
    ap.add_argument('--dir', help='Diretório de estado do ciclo (padrão: ~/.local/share/jev-auto/auto-melhoria).')
    ap.add_argument('--rotulo', default=medir.PRODUCAO_PADRAO['id'])
    ap.add_argument('--alvo-acerto', type=float, default=0.70)
    ap.add_argument('--min-casos', type=int, default=12)
    ap.add_argument('--teto-limiar', type=float, default=0.95)
    a = ap.parse_args(argv)

    d = medir.estado_dir(a.dir)
    resultado = calibrar(d, a.rotulo, a.alvo_acerto, a.min_casos, a.teto_limiar)

    caminho_historico = d / 'calibracao-historico.jsonl'
    caminho_historico.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho_historico, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'data': HOJE, **resultado}, ensure_ascii=False) + '\n')

    print(json.dumps(resultado, ensure_ascii=False, indent=1))
    return resultado


if __name__ == '__main__':
    main()
