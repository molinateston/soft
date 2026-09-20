#!/usr/bin/env bash
# Restaura um archive somente quando o banco de destino esta vazio.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ENV_FILE="$DIR/.env"; ARCHIVE=""; MEDIA_ARCHIVE=""; DRY_RUN=false
CONTAINER="${MONGO_CONTAINER:-soft-members-mongo}"
APP_CONTAINER="${APP_CONTAINER:-soft-members-app}"
usage() { echo "Uso: restore_mongo.sh --archive ARQUIVO [--media-archive ARQUIVO] [--dry-run]"; }
fail() { echo "ERRO: $*" >&2; exit 1; }
while [ $# -gt 0 ]; do case "$1" in --archive) ARCHIVE="${2:-}"; shift 2;; --media-archive) MEDIA_ARCHIVE="${2:-}"; shift 2;; --dry-run) DRY_RUN=true; shift;; -h|--help) usage; exit 0;; *) fail "opcao desconhecida: $1";; esac; done
[ -f "$ENV_FILE" ] || fail ".env ausente"; [ -f "$ARCHIVE" ] || fail "archive ausente: $ARCHIVE"
[ -z "$MEDIA_ARCHIVE" ] || [ -f "$MEDIA_ARCHIVE" ] || fail "archive de midia ausente: $MEDIA_ARCHIVE"
user="$(sed -n 's/^MONGO_USER=//p' "$ENV_FILE" | tail -n1)"; pass="$(sed -n 's/^MONGO_PASS=//p' "$ENV_FILE" | tail -n1)"
if [ -z "$user" ] || [ -z "$pass" ]; then fail "credenciais Mongo ausentes"; fi
if $DRY_RUN; then echo "DRY-RUN: conferiria destinos vazios e restauraria banco e midia sem senha em argv"; exit 0; fi
docker ps --format '{{.Names}}' | grep -qx "$CONTAINER" || fail "container $CONTAINER nao esta rodando"
if [ -n "$MEDIA_ARCHIVE" ]; then
    docker ps --format '{{.Names}}' | grep -qx "$APP_CONTAINER" || fail "container $APP_CONTAINER nao esta rodando"
    tar -tzf "$MEDIA_ARCHIVE" >/dev/null || fail "archive de midia invalido"
    if tar -tzf "$MEDIA_ARCHIVE" | grep -Eq '(^/|(^|/)\.\.(/|$))'; then fail "archive de midia contem caminho inseguro"; fi
    media_count="$(docker exec "$APP_CONTAINER" find /data/media -mindepth 1 -maxdepth 1 -print -quit)"
    [ -z "$media_count" ] || fail "diretorio de midia nao esta vazio; restauracao recusada"
fi
# --password sem valor le a senha de stdin; o segredo nao aparece em argv.
count="$(printf '%s\n' "$pass" | docker exec -i "$CONTAINER" mongosh --quiet --username "$user" --password --authenticationDatabase admin courselit --eval 'print(db.getCollectionNames().reduce((n,c)=>n+db.getCollection(c).estimatedDocumentCount(),0))' | tail -n1)"
[[ "$count" =~ ^[0-9]+$ ]] || fail "nao consegui conferir se o banco esta limpo"
[ "$count" -eq 0 ] || fail "banco nao esta limpo ($count documentos); restauracao recusada"
config="/tmp/soft-members-restore-$$.yml"; cleanup() { docker exec "$CONTAINER" rm -f "$config" >/dev/null 2>&1 || true; }; trap cleanup EXIT
printf 'password: "%s"\n' "$pass" | docker exec -i "$CONTAINER" sh -c 'umask 077; cat > "$1"' sh "$config"
docker exec -i "$CONTAINER" mongorestore --config "$config" --username "$user" --authenticationDatabase admin --archive --gzip < "$ARCHIVE"
if [ -n "$MEDIA_ARCHIVE" ]; then
    docker exec -i "$APP_CONTAINER" tar -C /data/media -xzf - < "$MEDIA_ARCHIVE"
fi
echo "Restauracao concluida em destinos limpos: $ARCHIVE ${MEDIA_ARCHIVE:-sem midia}"
