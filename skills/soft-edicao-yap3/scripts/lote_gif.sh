#!/bin/bash
# GIF em lote: para cada plano de <trab>/planos.json roda render (gif_meme.py) -> verificação (verificar_gif.py) -> auditoria (auditar_gif_meme.py).
# Uso: bash lote_gif.sh <planos.json> <pasta_verif> [<pasta_logs>]
#   Cada final ganha <pasta_verif>/<nome>/{verificacao.json, auditoria.json, mosaico.png}. No fim, rode mosaico_geral.py <pasta_verif> mosaico-geral.png
#   e olhe o lote inteiro antes de entregar. Saída por final: "<nome> verif=APROVADO audit=APROVADO".
set -u
S="$(cd "$(dirname "$0")" && pwd)"; PL="$1"; VF="$2"; LG="${3:-$VF/logs}"; mkdir -p "$VF" "$LG"
for p in $(python3 -c "import json,sys;print('\n'.join(json.load(open(sys.argv[1]))))" "$PL"); do
  n=$(basename "$(dirname "$p")")
  ( cd /tmp && nice -n 10 python3 -I "$S/gif_meme.py" "$p" 2 > "$LG/render-$n.log" 2>&1 ) || { echo "$n RENDER FALHOU (ver $LG/render-$n.log)"; continue; }
  nice -n 10 python3 "$S/verificar_gif.py" "$p" "$VF/$n" > "$LG/verif-$n.log" 2>&1
  nice -n 10 python3 "$S/auditar_gif_meme.py" "$p" "$VF/$n" > "$LG/audit-$n.log" 2>&1
  v=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['veredito'])" "$VF/$n/verificacao.json" 2>/dev/null || echo ERRO)
  a=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['veredito'])" "$VF/$n/auditoria.json" 2>/dev/null || echo ERRO)
  echo "$n verif=$v audit=$a"
done
