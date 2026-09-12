# Verbatim · toda copy ancora em fonte que o dono forneceu

A copy NAO inventa fato do negocio. Tese, prova, nome de mecanismo, numero, historia, transformacao tem lastro em fonte real do dono.

As fontes de lastro sao ENTRADA desta skill. Ela nunca sai lendo arquivo fora da propria pasta: quem chama informa os caminhos, ou o dono informa na conversa.

## Fontes na ordem de peso

1. Transcricao literal do dono falando (aula, webinar, live, call gravada). Maior peso: e a voz dele, palavra por palavra.
2. A tese-mae escrita: narrativa canonica, documento de posicionamento, manifesto, o que o dono chamar de fonte da verdade do negocio.
3. Bancos derivados: desejos, promessas, materia-prima, verbatim de cliente, comentario e mensagem real.
4. Plano de posicionamento do dono, se ja existir.

## Onde procurar (nesta ordem)

1. Os caminhos que a skill chamadora informou.
2. A variavel de ambiente `FONTES_LASTRO`, se o ambiente tiver shell e ela estiver definida (lista de caminhos separados por dois-pontos).
3. A pasta que o dono apontar na conversa.

## Se nao houver fonte nenhuma

O filtro nao para o trabalho. Usa a tese e a oferta declaradas na propria conversa como lastro e marca toda afirmacao grande que nao apareceu ali como `[LASTRO: confirmar com o dono]`. Numero, nome de mecanismo e historia continuam reprovando se sairam do nada.

## Como checar

Para cada afirmacao grande da copy, extrai 2-3 termos-chave (nome de mecanismo, numero, prova, historia) e procura nas fontes informadas.

Com shell:

    grep -ril "TERMO" "$FONTES_LASTRO"

Sem shell: pede o trecho ao dono e confere no olho. Se nenhum material retorna o termo, e chute. Reprova.

## Formato da prova (exemplos inventados, nao copia)

Exemplos ilustrativos, no formato dos fatos verbatim que costumam aparecer numa aula gravada. Ilustram o padrao "afirmacao grande + prova ao lado":

- alguns milhoes gerados em dez anos (na agencia).
- Escola de nicho: 7 digitos em 2 anos, com 5 pessoas, 1 funil so.
- 1 ano sem postar e seguiu vendendo.

Nao use estes numeros pra dono nenhum: sao inventados. Cada dono tem os seus. Estao aqui so como MODELO da estrutura "numero + contexto + peso".

## Como o dono declara as provas dele

Quando a skill chamadora trabalha pra um dono novo, ela precisa apontar o material de lastro. Padrao esperado, dentro da pasta que o dono escolher:

- a transcricao da aula ou live, se ja tiver alguma gravada;
- o documento da tese-mae dele;
- o plano de posicionamento, se ja rodou `soft-plano-posicionamento`.

Se o dono nao tem nada disso ainda, o filtro reprova promessa grande sem prova e sugere: rode `soft-plano-posicionamento` antes, ou declare a tese e a oferta aqui na conversa pra virarem o lastro minimo.

## O criterio duro

- Numero solto sem prova ao lado: reprova.
- Nome de mecanismo que nao existe na fonte: reprova.
- Historia inventada: reprova.
- Promessa generica sem dono: reprova.

O que passa: afirmacao com nome, numero, mecanismo ou historia que a fonte confirma.
