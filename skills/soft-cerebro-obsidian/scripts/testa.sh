#!/usr/bin/env bash
# Abre o mapa num navegador sem tela, confere erros de JavaScript e tira 4 prints.
# Uso: bash testa.sh <caminho/index.html> <prefixo-dos-prints> [nota-para-abrir] [termo-de-busca]
# Se não achar o navegador:  CHROME_BIN=/caminho/do/chrome bash testa.sh ...
set -u
HTML="${1:?uso: bash testa.sh <index.html> <prefixo> [nota] [busca]}"
PREF="${2:-teste-mapa}"
NOTA="${3:-}"
BUSCA="${4:-}"
[ -f "$HTML" ] || { echo "ERRO: não achei $HTML"; exit 2; }
ABS="$(cd "$(dirname "$HTML")" && pwd)/$(basename "$HTML")"

CH="${CHROME_BIN:-}"
if [ -z "$CH" ]; then
  for c in google-chrome google-chrome-stable chromium chromium-browser chrome \
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
    if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then CH="$c"; break; fi
  done
fi
if [ -z "$CH" ]; then
  CH="$(find "$HOME/.cache" -type f \( -name chrome-headless-shell -o -name chrome \) 2>/dev/null | head -1)"
fi
[ -n "$CH" ] || { echo "ERRO: não achei Chrome ou Chromium. Instale um, ou abra o index.html à mão. Use CHROME_BIN=/caminho se ele estiver fora do PATH."; exit 3; }

PERFIL="$(mktemp -d)"; trap 'rm -rf "$PERFIL"' EXIT
case "$CH" in /snap/*) echo "aviso: Chromium em snap às vezes não abre arquivos fora do seu home. Se falhar, use CHROME_BIN=/caminho/de/outro/chrome";; esac
FLAGS=(--headless --no-sandbox --disable-gpu --disable-vulkan --use-angle=swiftshader --hide-scrollbars --allow-file-access-from-files --user-data-dir="$PERFIL" --virtual-time-budget=4000)
[ -z "$NOTA" ]  && NOTA="$(python3 - "$ABS" <<'PY'
import re,sys
t=open(sys.argv[1],encoding="utf-8").read()
m=re.search(r'"tipo": "nota"',t)
n=re.findall(r'"nome": "([^"]+)", "hub": "[^"]+", "tipo": "nota"',t)
print(n[0] if n else "")
PY
)"
[ -z "$BUSCA" ] && BUSCA="${NOTA%% *}"

shot() { # nome  largura  altura  hash
  "$CH" "${FLAGS[@]}" --window-size="$2,$3" --screenshot="$1" "file://$ABS$4" >/dev/null 2>&1
  [ -s "$1" ] && echo "print: $1" || echo "FALHOU: $1"
}
DOM="$("$CH" "${FLAGS[@]}" --window-size=1280,800 --dump-dom "file://$ABS" 2>/dev/null)"
STATUS="$(printf '%s' "$DOM" | grep -o 'id="status">[^<]*' | sed 's/id="status">//')"
echo "${STATUS:-sem resposta do mapa (a página não carregou)}"
shot "${PREF}-1-visao-geral.png" 1280 800 ""
shot "${PREF}-2-nota-aberta.png" 1280 800 "#abre=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$NOTA")"
shot "${PREF}-3-busca.png" 1280 800 "#busca=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$BUSCA")"
shot "${PREF}-4-celular.png" 390 844 ""
echo "$STATUS" | grep -q "erros JS: 0" && echo "PASSOU: abra os 4 prints e olhe antes de dar por pronto" || { echo "REPROVOU: há erro de JavaScript ou a página não carregou"; exit 1; }
