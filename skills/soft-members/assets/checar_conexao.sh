#!/usr/bin/env bash
# Soft Members: confere a conexao do agente com a area de membros.
# Uso: bash checar_conexao.sh [caminho/do/.env]
# Sai 0 quando o agente pode operar, sai 1 e diz o que falta quando nao pode.
#
# Roda as duas chamadas de LEITURA obrigatorias de references/setup-conexao.md.
# Nao escreve nada na area de membros. Nao imprime a chave, nunca.

set -u

PASTA="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ $# -lt 1 ]; then
    echo "ERRO: diga onde esta o .env do dono."
    echo "Uso: bash checar_conexao.sh /caminho/do/.env"
    echo
    echo "O .env mora na pasta de trabalho do dono, NUNCA dentro desta skill,"
    echo "porque atualizacao da skill sobrescreve o que estiver aqui dentro."
    exit 1
fi

ARQUIVO="$1"

case "$ARQUIVO" in
    "$PASTA"/*)
        echo "ERRO: esse .env esta dentro da pasta da skill ($ARQUIVO)."
        echo "Atualizacao da skill apaga esse arquivo. Mova para a pasta de trabalho do dono."
        exit 1
        ;;
esac

if [ ! -f "$ARQUIVO" ]; then
    echo "ERRO: arquivo $ARQUIVO nao existe."
    echo "Copie o modelo para a pasta de trabalho do dono e preencha:"
    echo "  cp $PASTA/env.exemplo <pasta-do-dono>/.env"
    exit 1
fi

valor_de() {
    local chave="$1"
    sed -n "s/^[[:space:]]*${chave}[[:space:]]*=//p" "$ARQUIVO" | tail -n 1 |
        sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/^"\(.*\)"$/\1/' -e "s/^'\(.*\)'$/\1/"
}

URL="$(valor_de MEMBERS_URL)"
CHAVE="$(valor_de MEMBERS_API_KEY)"

FALTA=()
[ -z "$URL" ] && FALTA+=("MEMBERS_URL")
[ -z "$CHAVE" ] && FALTA+=("MEMBERS_API_KEY")

if [ ${#FALTA[@]} -gt 0 ]; then
    echo "NAO PODE OPERAR. Preencha em $ARQUIVO:"
    for c in "${FALTA[@]}"; do echo "  - $c"; done
    echo
    echo "A chave nasce na instalacao, em /opt/soft-members/chave-agente-leon.env"
    exit 1
fi

URL="${URL%/}"

case "$URL" in
    https://*) ;;
    *) echo "AVISO: MEMBERS_URL nao comeca com https. Sessao de aluno nao funciona fora do https." ;;
esac

echo "Escola: $URL"
echo "Chave: guardada (nao sera impressa)"
echo

# 1. A pagina publica responde?
COD_PAGINA="$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 "$URL/" || echo "000")"
echo "pagina publica: $COD_PAGINA"

# 2. A API aceita a chave?
COD_API="$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 \
    -H "x-api-key: $CHAVE" "$URL/api/products?limit=1" || echo "000")"
echo "api de cursos:  $COD_API"
echo

PROBLEMAS=()

if [ "$COD_PAGINA" = "000" ]; then
    PROBLEMAS+=("a escola nao respondeu: instalacao fora do ar, ou endereco errado")
elif [ "$COD_PAGINA" -ge 500 ] 2>/dev/null; then
    PROBLEMAS+=("a escola respondeu $COD_PAGINA: o programa caiu, veja references/SOCORRO.md")
fi

case "$COD_API" in
    200) ;;
    400) PROBLEMAS+=("a api recusou sem chave: o cabecalho x-api-key nao chegou") ;;
    401) PROBLEMAS+=("a chave nao vale nesta instalacao: rotacione com gerar_chave_api.sh na VPS") ;;
    404) PROBLEMAS+=("dominio nao encontrado: MEMBERS_URL nao bate com o dominio cadastrado") ;;
    000) PROBLEMAS+=("a api nao respondeu: instalacao fora do ar") ;;
    *)   PROBLEMAS+=("a api respondeu $COD_API, que nao e sucesso") ;;
esac

if [ ${#PROBLEMAS[@]} -gt 0 ]; then
    echo "NAO PODE OPERAR. Conserte isto primeiro:"
    for p in "${PROBLEMAS[@]}"; do echo "  - $p"; done
    exit 1
fi

echo "OK: o agente pode operar esta area de membros."
echo "Proximo passo: montar o mapa da instancia (references/setup-conexao.md, ultimo bloco)."
exit 0
