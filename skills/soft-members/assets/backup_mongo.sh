#!/usr/bin/env bash
# Soft Members: copia de seguranca do banco e da midia local.
# Uso: bash backup_mongo.sh
# Cron diario as 03:00:
#   0 3 * * * /bin/bash /opt/soft-members/backup_mongo.sh >> /opt/soft-members/backups/backup.log 2>&1
#
# Para restaurar, use as credenciais do .env por um arquivo --config temporario.
# Nao ponha a senha na linha de comando: ela fica visivel para outros processos.
#
# Guarda as 7 copias mais novas e apaga o resto.

set -euo pipefail

PASTA="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINO="$PASTA/backups"
CONTAINER="${MONGO_CONTAINER:-soft-members-mongo}"
APP_CONTAINER="${APP_CONTAINER:-soft-members-app}"
MANTER=7

# Usuario e senha saem do .env quando estiverem la.
USUARIO=""
SENHA=""
if [ -f "$PASTA/.env" ]; then
    LIDO_USER="$(sed -n 's/^[[:space:]]*MONGO_USER[[:space:]]*=//p' "$PASTA/.env" | tail -n 1 | tr -d '"'"'"' ')"
    LIDO_PASS="$(sed -n 's/^[[:space:]]*MONGO_PASS[[:space:]]*=//p' "$PASTA/.env" | tail -n 1 | tr -d '"'"'"' ')"
    [ -n "$LIDO_USER" ] && USUARIO="$LIDO_USER"
    [ -n "$LIDO_PASS" ] && SENHA="$LIDO_PASS"
fi

[ -n "$USUARIO" ] || { echo "ERRO: MONGO_USER ausente no .env"; exit 1; }
[ -n "$SENHA" ] || { echo "ERRO: MONGO_PASS ausente no .env"; exit 1; }

mkdir -p "$DESTINO"
MARCA="$(date +%Y-%m-%d-%H%M%S)"
ARQUIVO="$DESTINO/soft-members-$MARCA.archive.gz"
ARQUIVO_MIDIA="$DESTINO/soft-members-$MARCA.media.tar.gz"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] gerando copia em $ARQUIVO"

CONFIG_CONTAINER="/tmp/soft-members-mongodump-$$.yml"
cleanup() { docker exec "$CONTAINER" rm -f "$CONFIG_CONTAINER" >/dev/null 2>&1 || true; }
trap cleanup EXIT

# O segredo segue por stdin e nao aparece nos argumentos de mongodump nem no ps.
printf 'password: "%s"\n' "$SENHA" |
    docker exec -i "$CONTAINER" sh -c 'umask 077; cat > "$1"' sh "$CONFIG_CONTAINER"

docker exec "$CONTAINER" mongodump \
    --config "$CONFIG_CONTAINER" \
    --username "$USUARIO" \
    --authenticationDatabase admin \
    --db courselit \
    --archive \
    --gzip > "$ARQUIVO"

docker exec "$APP_CONTAINER" tar -C /data/media -czf - . > "$ARQUIVO_MIDIA"

if [ ! -s "$ARQUIVO" ] || [ ! -s "$ARQUIVO_MIDIA" ]; then
    echo "ERRO: uma copia saiu vazia. Apagando o par e parando."
    rm -f "$ARQUIVO" "$ARQUIVO_MIDIA"
    exit 1
fi

# Os nomes sao gerados por este script e nao contem espacos nem caracteres livres.
# shellcheck disable=SC2012
ls -1t "$DESTINO"/soft-members-*.archive.gz 2>/dev/null | tail -n +$((MANTER + 1)) | while read -r velho; do
    echo "apagando copia antiga: $velho"
    rm -f "$velho" "${velho%.archive.gz}.media.tar.gz"
done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] banco: $(du -h "$ARQUIVO" | cut -f1) em $ARQUIVO"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] midia: $(du -h "$ARQUIVO_MIDIA" | cut -f1) em $ARQUIVO_MIDIA"
