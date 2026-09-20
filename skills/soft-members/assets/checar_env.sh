#!/usr/bin/env bash
# Soft Members: confere o .env antes de subir o compose.
# Uso: bash checar_env.sh [caminho/do/.env]
# Sai 0 quando esta tudo certo, sai 1 e lista o que falta quando nao esta.

set -u

PASTA="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARQUIVO="${1:-$PASTA/.env}"

if [ ! -f "$ARQUIVO" ]; then
    echo "ERRO: arquivo $ARQUIVO nao existe."
    echo "Copie o modelo e preencha: cp $PASTA/.env.exemplo $PASTA/.env"
    exit 1
fi

# Le o .env sem executar nada que esteja dentro dele.
valor_de() {
    local chave="$1"
    sed -n "s/^[[:space:]]*${chave}[[:space:]]*=//p" "$ARQUIVO" | tail -n 1 |
        sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/^"\(.*\)"$/\1/' -e "s/^'\(.*\)'$/\1/"
}

OBRIGATORIAS=(
    SUPER_ADMIN_EMAIL
    AUTH_SECRET
    DB_CONNECTION_STRING
    DB_TRANSACTIONS
    EMAIL_HOST
    EMAIL_PORT
    EMAIL_USER
    EMAIL_PASS
    EMAIL_FROM
    MULTITENANT
    NODE_ENV
    DOMINIO
    SOFT_MEMBERS_IMAGE
    MONGO_USER
    MONGO_PASS
)

FALTA=()
for chave in "${OBRIGATORIAS[@]}"; do
    if [ -z "$(valor_de "$chave")" ]; then
        FALTA+=("$chave")
    fi
done

PROBLEMAS=()

if [ ${#FALTA[@]} -gt 0 ]; then
    for chave in "${FALTA[@]}"; do
        PROBLEMAS+=("falta preencher $chave em $ARQUIVO")
    done
fi

MULTI="$(valor_de MULTITENANT | tr '[:upper:]' '[:lower:]')"
if [ "$MULTI" = "true" ]; then
    PROBLEMAS+=("MULTITENANT esta true: a area de membros e de um dono so, ponha MULTITENANT=false")
fi

if [ -z "$(valor_de SUPER_ADMIN_EMAIL)" ]; then
    PROBLEMAS+=("SUPER_ADMIN_EMAIL vazio derruba o app inteiro na primeira visita, preencha com o e-mail do dono")
fi

TRANS="$(valor_de DB_TRANSACTIONS | tr '[:upper:]' '[:lower:]')"
if [ -n "$TRANS" ] && [ "$TRANS" != "false" ]; then
    PROBLEMAS+=("DB_TRANSACTIONS esta $TRANS: o mongo avulso deste compose nao faz transacao, ponha DB_TRANSACTIONS=false")
fi

MONGO_USER="$(valor_de MONGO_USER)"
MONGO_PASS="$(valor_de MONGO_PASS)"
DB_URI="$(valor_de DB_CONNECTION_STRING)"
if [ -n "$MONGO_USER" ] && [ -n "$DB_URI" ] && [[ "$DB_URI" != mongodb://"$MONGO_USER":* ]]; then
    PROBLEMAS+=("DB_CONNECTION_STRING nao usa o MONGO_USER informado")
fi
if [ -n "$MONGO_PASS" ] && [ -n "$DB_URI" ] && [[ "$DB_URI" != *":$MONGO_PASS@mongo/"* ]]; then
    PROBLEMAS+=("DB_CONNECTION_STRING nao combina com MONGO_PASS ou nao aponta para o servico mongo")
fi
if [ "$MONGO_PASS" = "example" ] || [ "$MONGO_PASS" = "password" ]; then
    PROBLEMAS+=("MONGO_PASS usa uma senha de exemplo; gere uma senha exclusiva")
fi
if [ -n "$MONGO_PASS" ] && [[ ! "$MONGO_PASS" =~ ^[A-Za-z0-9._~-]{16,}$ ]]; then
    PROBLEMAS+=("MONGO_PASS deve ter ao menos 16 caracteres seguros para URI: letras, numeros, ponto, sublinhado, til ou hifen")
fi

if [ ${#PROBLEMAS[@]} -gt 0 ]; then
    echo "NAO PODE SUBIR. Conserte isto primeiro:"
    for p in "${PROBLEMAS[@]}"; do
        echo "  - $p"
    done
    exit 1
fi

echo "OK: $ARQUIVO tem todas as variaveis obrigatorias preenchidas."
echo "Pode subir: docker compose -f $PASTA/docker-compose.yml up -d"
exit 0
