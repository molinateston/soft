# Fichas-modelo

Modelos das fichas que moram em `NFSE_DADOS_DIR`. Tudo aqui é marcador: troque cada `<...>` pelo dado real. Marcador que sobrar conta como dado faltando e o `conferir` faz a pergunta. O comando `iniciar` grava estes mesmos modelos na pasta de dados.

## A pasta de dados

```text
NFSE_DADOS_DIR/
  empresa.json              ficha da empresa emissora
  clientes/
    _modelo.json            modelo, ignorado na emissão
    <apelido>.json          uma ficha por cliente
  contador-dps.json         último número de DPS usado, por ambiente e série
  palavra-passe.json        hash com sal da palavra-passe de produção
  registro.jsonl            auditoria, uma linha por ação
  rascunhos/<hash>/         dps.xml e resumo.json de cada preparar
  notas/<ambiente>/<AAAA-MM>/<apelido>-s<série>-dps<número>/
                            dps-rascunho.xml, dps-assinado.xml, nfse.xml, nfse.pdf,
                            estado.json, resposta.json
```

## Ficha da empresa (`empresa.json`)

```json
{
  "razao_social": "<razão social da empresa>",
  "cnpj": "<CNPJ da empresa, 14 caracteres>",
  "inscricao_municipal": "<inscrição municipal, se o município usar>",
  "municipio_ibge": "<código IBGE do município da empresa, 7 dígitos>",
  "simples_nacional": {
    "opSimpNac": "<3 para ME/EPP, confirme com o contador>",
    "regApTribSN": "<1 quando tudo é apurado no Simples, o contador confirma>"
  },
  "regEspTrib": "<0 quando não há regime especial>",
  "serie_dps": "<série do DPS, de 1 a 49999>",
  "tributos_aproximados": {
    "pTotTribFed": "<percentual federal>",
    "pTotTribEst": "<percentual estadual>",
    "pTotTribMun": "<percentual municipal>"
  },
  "exigir_palavra_passe": true
}
```

Notas da ficha:

- `cnpj` aceita pontuação; o script tira. O cálculo do dígito aceita o CNPJ alfanumérico (letras nas 12 primeiras posições), mas a aceitação dele pelo leiaute nacional não foi conferida.
- `serie_dps`: escolha uma série só para esta skill, para o contador de números não cruzar com outro emissor. Se a série já foi usada antes, ajuste o contador com `contador --ajustar <último número usado>`.
- `tributos_aproximados`: percentuais com ponto ou vírgula, até 2 casas. Quem informa é o contador.
- `exigir_palavra_passe`: `true` por padrão. Com `false`, produção não pede a palavra-passe, e o resumo com confirmação continua obrigatório.

## Ficha de cliente (`clientes/<apelido>.json`)

O apelido é o nome do arquivo, em minúsculas, com letras, números, hífen e sublinhado. É ele que vai no `--cliente`.

```json
{
  "nome": "<razão social ou nome completo do cliente>",
  "documento": {"tipo": "<CNPJ ou CPF>", "numero": "<número do documento>"},
  "endereco": {
    "cep": "<CEP, 8 dígitos>",
    "municipio_ibge": "<código IBGE do município do cliente, 7 dígitos>",
    "logradouro": "<rua ou avenida>",
    "numero": "<número ou S/N>",
    "complemento": "<complemento, opcional>",
    "bairro": "<bairro>"
  },
  "servico": {
    "cTribNac": "<código de tributação nacional, 6 dígitos, o contador informa>",
    "cLocPrestacao": "<código IBGE do município da prestação>",
    "descricao_base": "<texto fixo da descrição, opcional>"
  },
  "iss": {
    "tribISSQN": "<1 para operação tributável, o contador confirma>",
    "tpRetISSQN": "<1 não retido, 2 retido pelo tomador, 3 retido pelo intermediário>"
  }
}
```

Notas da ficha:

- A descrição da nota é `descricao_base` mais o `--descricao` do pedido. Sem base, vale só o texto do pedido; sem os dois, o `preparar` pergunta.
- `tpRetISSQN` diferente de 1 e `tribISSQN` diferente de 1 saem como LIMITE: esses casos pedem campos que a skill não monta.

## Exemplo fictício preenchido

Dados inventados, só para mostrar o formato. O CNPJ é o número de exemplo usado em material didático.

```json
{
  "nome": "CLIENTE FICTICIO TOMADOR LTDA",
  "documento": {"tipo": "CNPJ", "numero": "99.888.777/0001-00"},
  "endereco": {"cep": "99999-999", "municipio_ibge": "9999999", "logradouro": "Rua Ficticia",
               "numero": "100", "complemento": "", "bairro": "Bairro Ficticio"},
  "servico": {"cTribNac": "010101", "cLocPrestacao": "9999999",
              "descricao_base": "Servico ficticio de teste"},
  "iss": {"tribISSQN": 1, "tpRetISSQN": 1}
}
```

## Do pedido ao comando

Pedido do dono: "emite a nota de setembro do cliente fictício, R$ 700, referente a setembro".

```bash
export NFSE_DADOS_DIR="$HOME/nfse-dados"
python3 scripts/nfse.py conferir --cliente cliente-ficticio
python3 scripts/nfse.py preparar --cliente cliente-ficticio --valor 700 --competencia 2026-09 --descricao "referente a setembro"
python3 scripts/nfse.py emitir --hash <hash que o preparar imprimiu>
```

Entre o `preparar` e o `emitir` fica o resumo mostrado ao dono e o sim explícito dele.
