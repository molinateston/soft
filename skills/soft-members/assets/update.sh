#!/usr/bin/env bash
# Atualiza a imagem com backup, verificacao de saude e rollback automatico.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ENV_FILE="$DIR/.env"
IMAGE=""; ARCHIVE=""; PULL=false; DRY_RUN=false; TIMEOUT=60; HEALTH_URL=""
usage() { echo "Uso: update.sh --image REF [--image-archive ARQ|--pull-image] [--health-url URL] [--dry-run]"; }
fail() { echo "ERRO: $*" >&2; exit 1; }
run() { if $DRY_RUN; then printf 'DRY-RUN:'; printf ' %q' "$@"; printf '\n'; else "$@"; fi; }
while [ $# -gt 0 ]; do case "$1" in
    --image) IMAGE="${2:-}"; shift 2;; --image-archive) ARCHIVE="${2:-}"; shift 2;; --pull-image) PULL=true; shift;;
    --health-url) HEALTH_URL="${2:-}"; shift 2;; --health-timeout) TIMEOUT="${2:-}"; shift 2;;
    --dry-run) DRY_RUN=true; shift;; -h|--help) usage; exit 0;; *) fail "opcao desconhecida: $1";; esac; done
[ -f "$ENV_FILE" ] || fail ".env ausente"; [ -n "$IMAGE" ] || fail "informe --image"
[[ "$IMAGE" =~ ^[A-Za-z0-9._/:@-]+$ ]] || fail "imagem invalida"; [[ "$TIMEOUT" =~ ^[1-9][0-9]*$ ]] || fail "timeout invalido"
[ -z "$ARCHIVE" ] || [ -f "$ARCHIVE" ] || fail "archive ausente: $ARCHIVE"
old_image="$(sed -n 's/^SOFT_MEMBERS_IMAGE=//p' "$ENV_FILE" | tail -n1)"; [ -n "$old_image" ] || fail "imagem anterior ausente no .env"
domain="$(sed -n 's/^DOMINIO=//p' "$ENV_FILE" | tail -n1)"; [ -n "$HEALTH_URL" ] || HEALTH_URL="https://$domain/healthy"
run "$DIR/checar_env.sh"; run "$DIR/backup_mongo.sh"
[ -z "$ARCHIVE" ] || run docker load --input "$ARCHIVE"; $PULL && run docker pull "$IMAGE"
if $DRY_RUN; then run docker image inspect "$IMAGE"; else docker image inspect "$IMAGE" >/dev/null || fail "imagem $IMAGE indisponivel"; fi
if $DRY_RUN; then echo "DRY-RUN: trocaria SOFT_MEMBERS_IMAGE de $old_image para $IMAGE"; else
    tmp="$(mktemp "$DIR/.env.update.XXXXXX")"; trap 'rm -f "$tmp"' EXIT
    sed "s|^SOFT_MEMBERS_IMAGE=.*|SOFT_MEMBERS_IMAGE=$IMAGE|" "$ENV_FILE" > "$tmp"; chmod 600 "$tmp"; mv "$tmp" "$ENV_FILE"; trap - EXIT
fi
run docker compose --env-file "$ENV_FILE" -f "$DIR/docker-compose.yml" up -d
if $DRY_RUN; then echo "DRY-RUN: esperaria ${TIMEOUT}s por $HEALTH_URL; em falha voltaria para $old_image"; exit 0; fi
deadline=$((SECONDS + TIMEOUT)); healthy=false
until [ $SECONDS -ge $deadline ]; do [ "$(curl -sS -o /dev/null -w '%{http_code}' --max-time 5 "$HEALTH_URL" || true)" = 200 ] && { healthy=true; break; }; sleep 2; done
if ! $healthy; then
    tmp="$(mktemp "$DIR/.env.rollback.XXXXXX")"; sed "s|^SOFT_MEMBERS_IMAGE=.*|SOFT_MEMBERS_IMAGE=$old_image|" "$ENV_FILE" > "$tmp"; chmod 600 "$tmp"; mv "$tmp" "$ENV_FILE"
    docker compose --env-file "$ENV_FILE" -f "$DIR/docker-compose.yml" up -d
    fail "imagem nova falhou na saude; tag anterior restaurada: $old_image"
fi
echo "Atualizado para $IMAGE; backup feito e saude confirmada."
