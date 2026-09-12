#!/bin/bash
# Render resiliente em 3 blocos + concat. Idempotente: pula bloco ja pronto.
set -e
# PROJETO: pasta do projeto Remotion (a copia deste template na pasta de trabalho do video).
#          Default: o diretorio deste script.
# OUT:     pasta de saida dos blocos e do filme final. Default: PROJETO/out.
PROJETO="${PROJETO:-$(cd "$(dirname "$0")" && pwd)}"
OUT="${OUT:-$PROJETO/out}"
cd "$PROJETO"
mkdir -p "$OUT"

BIN=node_modules/.bin/remotion
render_bloco () {
  local nome=$1 ini=$2 fim=$3
  if [ -s "$OUT/$nome.mp4" ]; then echo "$nome ja existe, pulando"; return; fi
  $BIN render src/index.ts Director "$OUT/$nome.mp4" \
    --frames=$ini-$fim --codec=h264 --crf=18 --pixel-format=yuv420p --concurrency=2 \
    >> "$OUT/blocos.log" 2>&1
  echo "$nome OK ($ini-$fim)" >> "$OUT/blocos.log"
}
render_bloco b1 0 3844
render_bloco b2 3845 7689
render_bloco b3 7690 11534
# concat
printf "file '%s'\n" "$OUT/b1.mp4" "$OUT/b2.mp4" "$OUT/b3.mp4" > "$OUT/concat.txt"
ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i "$OUT/concat.txt" -c copy "$OUT/FILME_COMPLETO.mp4"
echo "FULL_OK dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/FILME_COMPLETO.mp4") size=$(ls -la "$OUT/FILME_COMPLETO.mp4"|awk '{print $5}')" > "$OUT/full_done.txt"
