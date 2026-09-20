#!/usr/bin/env bash
# Soft Members: gera a chave de API do agente direto no banco, sem painel.
#
# Por que existe: a tela /dashboard/settings/apikeys/new e o unico caminho
# oficial para criar chave, e ela exige sessao de navegador. O dono leigo
# nao abre painel. Este script faz o mesmo que a tela faz, no mesmo formato,
# lendo as credenciais do .env que ja esta ao lado.
#
# Uso:
#   bash gerar_chave_api.sh
#   bash gerar_chave_api.sh --nome agente-leon --email dono@exemplo.com
#   bash gerar_chave_api.sh --rotacionar
#
# Rodar duas vezes nao cria chave duplicada: o banco tem indice unico em
# (dominio, nome) e o script respeita o que ja existe.

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$DIR/.env"
NOME="agente-leon"
EMAIL=""
ARQUIVO=""
ROTACIONAR=0
CONTAINER="${MONGO_CONTAINER:-soft-members-mongo}"

erro() { printf 'ERRO: %s\n' "$1" >&2; exit 1; }

while [ $# -gt 0 ]; do
    case "$1" in
        --nome)   NOME="${2:-}"; shift 2 ;;
        --email)  EMAIL="${2:-}"; shift 2 ;;
        --arquivo) ARQUIVO="${2:-}"; shift 2 ;;
        --env)    ENV_FILE="${2:-}"; shift 2 ;;
        --rotacionar) ROTACIONAR=1; shift ;;
        -h|--help)
            sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
            exit 0 ;;
        *) erro "opcao desconhecida: $1. Rode com --help." ;;
    esac
done

# --- 1. O arquivo de configuracao ------------------------------------------
[ -f "$ENV_FILE" ] || erro "nao achei $ENV_FILE. Este script mora ao lado do .env da instalacao."

ler_env() {
    sed -n -E "s/^[[:space:]]*(export[[:space:]]+)?$1=//p" "$ENV_FILE" \
        | head -n1 \
        | sed -E 's/^"(.*)"$/\1/; s/^'"'"'(.*)'"'"'$/\1/' \
        | sed -E 's/[[:space:]]+$//'
}

URI="$(ler_env DB_CONNECTION_STRING)"
DOMINIO="$(ler_env DOMINIO)"
[ -n "$URI" ] || erro "DB_CONNECTION_STRING vazio em $ENV_FILE. Sem endereco de banco nao da para seguir."
[ -n "$DOMINIO" ] || erro "DOMINIO vazio em $ENV_FILE. Preencha com o dominio publico da area de membros, sem http."
printf '%s' "$DOMINIO" | grep -qE '^[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?$' \
    || erro "DOMINIO invalido em $ENV_FILE: $DOMINIO. Use o dominio publico sem http, caminho ou porta."
case "$DOMINIO" in
    localhost|*.localhost)
        erro "DOMINIO aponta para endereco local em $ENV_FILE: $DOMINIO. Use o dominio publico da area de membros." ;;
esac
[ -n "$EMAIL" ] || EMAIL="$(ler_env SUPER_ADMIN_EMAIL)"
[ -n "$EMAIL" ] || erro "faltou o e-mail do dono. Passe --email, ou preencha SUPER_ADMIN_EMAIL em $ENV_FILE."

# --- 2. Higiene de entrada --------------------------------------------------
printf '%s' "$EMAIL" | grep -qE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' \
    || erro "e-mail invalido: $EMAIL"
printf '%s' "$NOME" | grep -qE '^[A-Za-z0-9._-]{1,60}$' \
    || erro "nome de chave invalido: $NOME. Use letras, numeros, ponto, hifen ou sublinhado."

[ -n "$ARQUIVO" ] || ARQUIVO="$DIR/chave-$NOME.env"

# --- 3. Como falar com o banco ---------------------------------------------
if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx "$CONTAINER"; then
    MODO="container $CONTAINER"
    rodar_mongo() { docker exec -i "$CONTAINER" mongosh "$URI" --quiet --eval "$1"; }
elif command -v mongosh >/dev/null 2>&1; then
    MODO="mongosh desta maquina"
    rodar_mongo() { mongosh "$URI" --quiet --eval "$1"; }
else
    erro "nao achei o container $CONTAINER rodando nem mongosh nesta maquina. Suba o compose ou aponte MONGO_CONTAINER para o nome certo."
fi

# --- 4. Chave no formato exato que a tela gera ------------------------------
# O modelo (apps/web/models/ApiKey.ts) usa generateUniqueId, que e nanoid():
# 21 caracteres do alfabeto de 64 abaixo, um byte aleatorio por caractere
# mascarado com 63. Sem hash, sem sal: o campo key guarda o valor cru, e a
# validacao (apps/web/app/api/public-api.ts) compara o valor cru do header.
ALFABETO='useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict'
gerar_id() {
    local saida='' b
    for b in $(od -An -v -tu1 -N21 /dev/urandom); do
        saida="$saida${ALFABETO:$((b & 63)):1}"
    done
    printf '%s' "$saida"
}
CHAVE_NOVA="$(gerar_id)"
KEYID_NOVO="$(gerar_id)"
[ ${#CHAVE_NOVA} -eq 21 ] || erro "a geracao da chave saiu com ${#CHAVE_NOVA} caracteres em vez de 21. Nao gravei nada."

# --- 5. O trabalho no banco -------------------------------------------------
JS=$(cat <<'FIMJS'
(function () {
    const nome = "__NOME__";
    const email = "__EMAIL__";
    const chaveNova = "__CHAVE__";
    const keyIdNovo = "__KEYID__";
    const rotacionar = __ROTACIONAR__;
    const dica = "__DOMINIO__";

    const dominios = db.domains
        .find({ email: email, deleted: { $ne: true } })
        .toArray();

    if (dominios.length === 0) {
        print("RESULTADO_ESTADO=sem_dominio");
        print(
            "RESULTADO_MENSAGEM=nenhuma escola neste banco tem " +
                email +
                " como dono. Confira SUPER_ADMIN_EMAIL e a inicializacao da escola.",
        );
        quit(3);
    }

    let dominio = dominios[0];
    if (dominios.length > 1) {
        const casados = dominios.filter(
            (d) => d.name === dica || d.customDomain === dica,
        );
        if (casados.length !== 1) {
            print("RESULTADO_ESTADO=dominio_ambiguo");
            print(
                "RESULTADO_MENSAGEM=este banco tem " +
                    dominios.length +
                    " escolas com o mesmo dono. Rode de novo com DOMINIO certo no .env.",
            );
            quit(4);
        }
        dominio = casados[0];
    }

    // A validacao da API mapeia a chave para o usuario cujo e-mail e igual ao
    // e-mail do dominio. Sem esse usuario, toda chamada volta 403.
    const dono = db.users.findOne({ domain: dominio._id, email: email });
    if (!dono) {
        print("RESULTADO_ESTADO=sem_dono");
        print(
            "RESULTADO_MENSAGEM=a escola existe mas ninguem com o e-mail " +
                email +
                " foi criado nela. Inicialize a escola pela pagina local e rode de novo.",
        );
        quit(5);
    }

    const features = dominio.features || [];
    let feature = "ja_ligada";
    if (features.indexOf("api") === -1) {
        db.domains.updateOne(
            { _id: dominio._id },
            { $addToSet: { features: "api" } },
        );
        feature = "ligada_agora";
    }

    let doc = db.apikeys.findOne({ domain: dominio._id, name: nome });
    let estado = "";

    if (doc && rotacionar) {
        db.apikeys.deleteOne({ _id: doc._id });
        doc = null;
        estado = "rotacionada";
    }

    if (!doc) {
        const agora = new Date();
        db.apikeys.insertOne({
            domain: dominio._id,
            keyId: keyIdNovo,
            name: nome,
            key: chaveNova,
            createdAt: agora,
            updatedAt: agora,
            __v: 0,
        });
        doc = db.apikeys.findOne({ domain: dominio._id, name: nome });
        if (!estado) estado = "criada";
    } else {
        estado = "existente";
    }

    print("RESULTADO_ESTADO=" + estado);
    print("RESULTADO_CHAVE=" + doc.key);
    print("RESULTADO_KEYID=" + doc.keyId);
    print("RESULTADO_DOMINIO_NOME=" + dominio.name);
    print("RESULTADO_FEATURE=" + feature);
    print("RESULTADO_DONO_NOME=" + (dono.name || ""));
})();
FIMJS
)
JS="${JS//__NOME__/$NOME}"
JS="${JS//__EMAIL__/$EMAIL}"
JS="${JS//__CHAVE__/$CHAVE_NOVA}"
JS="${JS//__KEYID__/$KEYID_NOVO}"
JS="${JS//__ROTACIONAR__/$ROTACIONAR}"
JS="${JS//__DOMINIO__/$DOMINIO}"

SAIDA="$(rodar_mongo "$JS" 2>&1)" || true

pegar() { printf '%s\n' "$SAIDA" | sed -n -E "s/^$1=//p" | head -n1; }

ESTADO="$(pegar RESULTADO_ESTADO)"
if [ -z "$ESTADO" ]; then
    printf 'ERRO: o banco nao respondeu o que eu esperava (%s). Saida crua:\n%s\n' "$MODO" "$SAIDA" >&2
    exit 1
fi

case "$ESTADO" in
    sem_dominio|dominio_ambiguo|sem_dono)
        erro "$(pegar RESULTADO_MENSAGEM)" ;;
esac

CHAVE="$(pegar RESULTADO_CHAVE)"
KEYID="$(pegar RESULTADO_KEYID)"
DOMINIO_NOME="$(pegar RESULTADO_DOMINIO_NOME)"
FEATURE="$(pegar RESULTADO_FEATURE)"
DONO_NOME="$(pegar RESULTADO_DONO_NOME)"
[ -n "$CHAVE" ] || erro "o banco nao devolveu a chave. Nada foi gravado em arquivo."

# --- 6. O arquivo que o agente le ------------------------------------------
BASE_URL="https://$DOMINIO"
if [ "$ESTADO" != "existente" ]; then
    umask 077
    cat > "$ARQUIVO" <<FIMENV
# Soft Members: conexao do agente. Nao versione, nao mande por mensagem.
# Gerado por gerar_chave_api.sh em $(date -u '+%Y-%m-%d %H:%M UTC').
MEMBERS_URL=$BASE_URL
MEMBERS_API_KEY=$CHAVE
MEMBERS_API_KEY_NOME=$NOME
MEMBERS_API_KEY_ID=$KEYID
MEMBERS_DONO=$EMAIL
FIMENV
    chmod 600 "$ARQUIVO"
fi

# --- 7. O relato ------------------------------------------------------------
echo
case "$ESTADO" in
    criada)      echo "Chave criada agora, no nome $NOME." ;;
    rotacionada) echo "Chave trocada, no nome $NOME. A antiga foi apagada e para de funcionar." ;;
    existente)   echo "A chave $NOME ja existia. Nao criei outra." ;;
esac
echo "Escola: $DOMINIO_NOME  ·  Endereco: $BASE_URL  ·  Dono: $EMAIL"
[ "$ESTADO" = "existente" ] || echo "Arquivo com a chave (permissao 600): $ARQUIVO"
[ "$FEATURE" = "ligada_agora" ] && echo "Liguei o recurso de API nesta escola, que estava desligado."

if [ "$ESTADO" = "existente" ]; then
    echo
    echo "Nao alterei $ARQUIVO. A chave existente continua no cofre em que foi guardada."
    echo "Para trocar por uma nova: bash $(basename "${BASH_SOURCE[0]}") --nome $NOME --rotacionar"
else
    echo
    echo "A chave aparece UMA vez, agora. Nao vou mostrar de novo:"
    echo
    echo "    $CHAVE"
    echo
    echo "Guarde no cofre do agente. Depois disso, leia sempre do arquivo."
fi

if [ -z "$DONO_NOME" ]; then
    echo
    echo "Aviso: o dono ainda nao tem nome gravado. Publicar curso vai falhar ate isso ser preenchido."
fi

echo
echo "Teste de leitura, que so passa com chave valida:"
printf '%s\n' "    curl -s -o /dev/null -w '%{http_code}\\n' -H \"x-api-key: \$MEMBERS_API_KEY\" \"$BASE_URL/api/products?limit=1\""
