#!/usr/bin/env bash
# md2doc.sh <arquivo.md> "<Nome do Documento>" <FOLDER_ID>
# Gera um Google Doc nativo formatado a partir de Markdown e imprime a URL.
set -euo pipefail
MD="${1:?uso: md2doc.sh <arquivo.md> \"<Nome>\" <FOLDER_ID>}"
NAME="${2:?falta o nome do documento}"
PARENT="${3:?falta o FOLDER_ID de destino}"
GOG="${GOG:-$(command -v gog || true)}"
[ -n "$GOG" ] || { echo "ERRO: gog nao encontrado no PATH. Defina GOG=/caminho/do/gog ou entregue o .md/.html e converta pelo Drive."; exit 127; }
command -v pandoc >/dev/null || { echo "ERRO: pandoc nao encontrado no PATH."; exit 127; }
HTML="$(mktemp --suffix=.html)"
# -tex_math_dollars/-tex_math_single_backslash: evita que "R$1.200 ... R$3.000" (precos)
# seja interpretado como formula TeX entre cifroes e corrompa o texto.
# -smart: nao converte '--'/'...' em travessao/reticencia unicode (travessao e banido na copy).
pandoc "$MD" -f markdown-tex_math_dollars-tex_math_single_backslash-smart -t html -o "$HTML"
OUT="$($GOG drive upload "$HTML" --name "$NAME" --convert-to doc --parent "$PARENT" -j)"
ID="$(printf '%s' "$OUT" | grep -oE '"id"[: ]*"[^"]+"' | head -1 | grep -oE '[A-Za-z0-9_-]{20,}')"
[ -n "$ID" ] || { echo "ERRO: nao consegui extrair o id. Saida do gog:"; echo "$OUT"; exit 1; }
echo "https://docs.google.com/document/d/$ID/edit"
