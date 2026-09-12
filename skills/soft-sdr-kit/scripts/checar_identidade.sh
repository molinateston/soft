#!/usr/bin/env bash
# Prova de identidade do kit de SDR.
#
# O kit e marca-neutra: ele nao pode carregar nome do dono da operacao que o
# mantem, identificador de conta de CRM, identificador de canal de mensageiro
# nem endereco proprio. Este script procura esses termos de forma mecanica e
# falha o lancamento quando acha qualquer um.
#
# USO
#   bash checar_identidade.sh <pasta-do-kit> [arquivo-de-termos]
#
# Sem o segundo argumento, o script procura o arquivo de termos nesta ordem:
#   1. $SDR_KIT_TERMOS  (variavel de ambiente)
#   2. <pasta-desta-skill>/termos-proibidos.local.txt
#
# O ARQUIVO DE TERMOS FICA FORA DO REPOSITORIO DO KIT, porque ele contem
# justamente os dados que nao podem vazar. Um termo por linha; linha vazia e
# linha comecando com # sao ignoradas. Exemplo de conteudo:
#
#   # nomes
#   NomeDoDono
#   SobrenomeDoDono
#   # identificadores
#   ABC123locationid
#   -1001234567890
#   # enderecos
#   minhaoperacao.com.br
#
# SAIDA
#   codigo 0  = limpo, pode lancar
#   codigo 1  = achou termo proibido, lancamento BLOQUEADO
#   codigo 2  = erro de uso (pasta ou arquivo de termos ausente)

set -uo pipefail

PASTA="${1:-}"
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TERMOS="${2:-${SDR_KIT_TERMOS:-$AQUI/../termos-proibidos.local.txt}}"

if [ -z "$PASTA" ] || [ ! -d "$PASTA" ]; then
  echo "uso: bash checar_identidade.sh <pasta-do-kit> [arquivo-de-termos]" >&2
  echo "pasta do kit ausente ou inexistente: '${PASTA}'" >&2
  exit 2
fi

if [ ! -f "$TERMOS" ]; then
  echo "arquivo de termos nao encontrado: $TERMOS" >&2
  echo "crie um termo por linha (nome do dono, id de CRM, id de canal, dominio)." >&2
  echo "ele fica FORA do repositorio do kit." >&2
  exit 2
fi

PADROES="$(grep -vE '^\s*(#|$)' "$TERMOS" || true)"
if [ -z "$PADROES" ]; then
  echo "arquivo de termos esta vazio: $TERMOS" >&2
  exit 2
fi

ACHOU=0
TOTAL=0

while IFS= read -r termo; do
  [ -z "$termo" ] && continue
  TOTAL=$((TOTAL + 1))
  SAIDA="$(grep -rniF --binary-files=without-match \
      --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=logs \
      --exclude='*.tar.gz' --exclude='*.log' \
      -- "$termo" "$PASTA" 2>/dev/null || true)"
  if [ -n "$SAIDA" ]; then
    ACHOU=1
    echo "TERMO PROIBIDO ENCONTRADO: $termo"
    echo "$SAIDA" | head -20 | sed 's/^/    /'
    QTD="$(printf '%s\n' "$SAIDA" | wc -l | tr -d ' ')"
    if [ "$QTD" -gt 20 ]; then
      echo "    ... e mais $((QTD - 20)) ocorrencia(s)"
    fi
    echo
  fi
done <<< "$PADROES"

if [ "$ACHOU" -eq 1 ]; then
  echo "LANCAMENTO BLOQUEADO: o kit carrega identidade da operacao."
  echo "limpe as ocorrencias acima e rode de novo."
  exit 1
fi

echo "identidade limpa: $TOTAL termo(s) conferido(s), zero ocorrencia em $PASTA"
exit 0
