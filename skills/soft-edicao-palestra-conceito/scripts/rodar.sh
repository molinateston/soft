#!/usr/bin/env bash
# Roda as etapas 1 a 9 em sequencia numa pasta de trabalho e para na primeira que nao der PRONTO.
# uso: scripts/rodar.sh PASTA_DE_TRABALHO [--prova] [--de N]
#   --prova: teste curto (dispensa a duracao minima e marca a entrega como prova)
#   --de N : comeca da etapa N (ex.: --de 4 depois de ajustar a headline)
# As etapas 3, 4 e 5 dependem de escolhas no ajustes.json (blocos, headline, conceitos): preencha antes.
set -e
S="$(cd "$(dirname "$0")" && pwd)"; T="$1"; shift || true
PROVA=""; DE=1
while [ $# -gt 0 ]; do case "$1" in --prova) PROVA="--prova";; --de) DE="$2"; shift;; esac; shift; done
[ -z "$T" ] && { echo "uso: $0 PASTA_DE_TRABALHO [--prova] [--de N]"; exit 2; }
e() { echo; echo "== etapa $1: $2"; }
[ "$DE" -le 1 ] && { e 1 entrada; python3 "$S/01_entrada.py" "$T"; }
[ "$DE" -le 2 ] && { e 2 transcricao; python3 "$S/02_transcrever.py" "$T"; }
[ "$DE" -le 3 ] && { e 3 cortes; python3 "$S/03_cortes.py" "$T" $PROVA; }
[ "$DE" -le 4 ] && { e 4 headline; python3 "$S/04_headline.py" "$T"; }
[ "$DE" -le 5 ] && { e 5 conceitos; python3 "$S/05_conceitos.py" "$T"; }
[ "$DE" -le 6 ] && { e 6 render; python3 "$S/06_base.py" "$T"; python3 "$S/06_rosto.py" "$T"; python3 "$S/06_reframe.py" "$T"; python3 "$S/06_compor.py" "$T"; }
[ "$DE" -le 7 ] && { e 7 gates; python3 "$S/07_gate_fala.py" "$T"; python3 "$S/07_gate_visual.py" "$T" $PROVA; }
[ "$DE" -le 8 ] && { e 8 mosaico; python3 "$S/08_mosaico.py" "$T"; }
e 9 entrega; python3 "$S/09_entrega.py" "$T" $PROVA
