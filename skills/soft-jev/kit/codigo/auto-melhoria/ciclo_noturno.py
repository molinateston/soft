#!/usr/bin/env python3
"""Passo 6 do ciclo de auto-melhoria: orquestrador.

Roda, em ordem, os passos diários (coletar → montar_gabarito → propor_sombra
→ calibrar_limiar) chamando cada script deste diretório como um processo
separado (o mesmo que rodar cada um na mão, só que em sequência e com o
resultado de cada um agregado num relatório só no final). Com `--promover`,
roda também `promover.py` no final — normalmente só 1x por semana, mesmo que
o resto rode toda noite.

Uso:
  ciclo_noturno.py [--dir ESTADO] [--entrada DIR] [--teto N] [--rotulo pronto_sem_prova]
  ciclo_noturno.py --promover [--dias-minimos 0]   # roda tudo + tenta promover

Exemplo de cron (roda 1x por noite, promovendo 1x por semana):

  0 3 * * *   /usr/bin/python3 /caminho/para/auto-melhoria/ciclo_noturno.py
  0 3 * * 0   /usr/bin/python3 /caminho/para/auto-melhoria/ciclo_noturno.py --promover
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def roda(script, args):
    cmd = [sys.executable, str(AQUI / script), *args]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    saida = r.stdout.strip()
    try:
        dado = json.loads(saida) if saida else None
    except json.JSONDecodeError:
        dado = saida
    return {'script': script, 'ok': r.returncode == 0, 'saida': dado, 'erro': r.stderr.strip() if r.returncode != 0 else None}


def main(argv=None):
    ap = argparse.ArgumentParser(description='Orquestra o ciclo diário de auto-melhoria (e, opcionalmente, a promoção semanal).')
    ap.add_argument('--dir', help='Diretório de estado do ciclo (padrão: ~/.local/share/jev-auto/auto-melhoria).')
    ap.add_argument('--entrada', help='Diretório com *.jsonl de históricos de conversa (opcional; ver coletar.py).')
    ap.add_argument('--rotulo', default='pronto_sem_prova')
    ap.add_argument('--teto', type=int, default=0, help='Teto de chamadas ao julgador por dia (0 = sem limite).')
    ap.add_argument('--promover', action='store_true', help='Depois do ciclo diário, também roda promover.py.')
    ap.add_argument('--dias-minimos', type=int, default=7, help='Repassado para promover.py.')
    a = ap.parse_args(argv)

    dir_args = ['--dir', a.dir] if a.dir else []
    passos = []

    passos.append(roda('coletar.py', dir_args + (['--entrada', a.entrada] if a.entrada else [])))
    passos.append(roda('montar_gabarito.py', dir_args))
    passos.append(roda('propor_sombra.py', dir_args + ['--rotulo', a.rotulo] + (['--teto', str(a.teto)] if a.teto else [])))
    passos.append(roda('calibrar_limiar.py', dir_args + ['--rotulo', a.rotulo]))
    if a.promover:
        passos.append(roda('promover.py', dir_args + ['--rotulo', a.rotulo, '--dias-minimos', str(a.dias_minimos)]))

    relatorio = {'passos': [p['script'] for p in passos], 'ok': all(p['ok'] for p in passos), 'detalhe': passos}
    print(json.dumps(relatorio, ensure_ascii=False, indent=1))
    if not relatorio['ok']:
        sys.exit(1)
    return relatorio


if __name__ == '__main__':
    main()
