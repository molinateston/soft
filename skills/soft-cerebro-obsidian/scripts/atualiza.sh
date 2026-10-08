#!/usr/bin/env bash
# Monta o mapa de novo, confere se deu certo e escreve uma linha em cerebro-diario.log.
# Uso:  bash atualiza.sh /caminho/completo/config.json
# Para também publicar e conferir no ar, defina antes:
#   PUBLICAR="comando que publica a pasta do mapa"   URL="https://seu-endereco/cerebro/"
set -u
CFG="${1:?uso: bash atualiza.sh /caminho/completo/config.json}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
DIR="$(cd "$(dirname "$CFG")" && pwd)"
LOG="$DIR/cerebro-diario.log"
agora() { date '+%Y-%m-%d %H:%M'; }
fim() { echo "$(agora) $1" >> "$LOG"; echo "$1"; [ "$1" = OK ] && exit 0 || exit 1; }

SAIDA="$(python3 "$AQUI/monta.py" "$CFG" 2>&1)" || { echo "$SAIDA"; fim "FALHOU: monta.py (veja a mensagem acima)"; }
echo "$SAIDA" | head -3
CAM="$(python3 -c 'import json,os,sys;c=json.load(open(sys.argv[1]));print(os.path.normpath(os.path.join(os.path.dirname(sys.argv[1]),c.get("saida","cerebro-site"))))' "$CFG")"
[ -s "$CAM/index.html" ] || fim "FALHOU: index.html vazio ou ausente"
if [ -n "${PUBLICAR:-}" ]; then
  bash -c "$PUBLICAR" >/dev/null 2>&1 || fim "FALHOU: o comando PUBLICAR deu erro"
  if [ -n "${URL:-}" ]; then
    curl -fsS "$URL" 2>/dev/null | grep -q "<canvas" || fim "FALHOU: o endereço no ar não mostra o mapa"
  fi
fi
python3 "$AQUI/confere.py" "$CFG" --silencioso || echo "aviso: a base tem pendências (rode confere.py para ver)"
fim OK
