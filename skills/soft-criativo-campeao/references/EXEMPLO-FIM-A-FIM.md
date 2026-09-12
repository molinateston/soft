# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, perfil, números, custos e resultados foram inventados só
> pra mostrar a FORMA de cada saída. Nada disso é caso real e nada disso pode ser copiado pra uma
> entrega de verdade. Num trabalho real, todo número sem fonte nasce marcado `[A CONFIRMAR]` e o
> dono confirma antes de sair.

**O caso fictício:** um fisioterapeuta esportivo que atende corredores amadores e vende uma
mentoria de 8 semanas pra outros fisioterapeutas ("como parar de atender por sessão avulsa").
Avatar: fisioterapeuta autônomo, 27 a 40 anos, agenda cheia e faturamento baixo, cobra por sessão.
Pedido do dono: "preciso de 4 artes pra rodar anúncio da minha aula gratuita na semana que vem".

Este arquivo mostra a saída resumida de cada ação, na ordem em que aconteceu.

---

## O que o dono deu de entrada

> "Quero anunciar minha aula gratuita. Tenho umas fotos de estúdio que tirei ano passado. Minha cor
> é um verde escuro, uso a fonte do meu site. A aula é dia 18, o cadastro é na minha página."

Insumo faltando: as dores nomeadas, o arquivo da fonte, o evento de conversão. A skill não parou:
perguntou o que faltava e marcou o resto.

## As perguntas que a skill fez (uma por vez)

1. "Quem é a pessoa que você quer nessa aula, e o que dói nela hoje?"
   > "Fisioterapeuta que atende o dia inteiro, ganha por sessão e não sobra nada. Ele vive com medo
   > de o paciente sumir depois da terceira sessão."
2. "Me manda 2 ou 3 fotos suas em boa resolução."
   > mandou 3 arquivos de estúdio, fundo claro, meio corpo.
3. "Qual a cor e a fonte da sua marca?"
   > "Verde escuro. A fonte eu não sei o nome, é a do site."
   Resolução: verde declarado, fonte sem-serifa do sistema, marcada `[A CONFIRMAR]`.
4. "Pra onde a pessoa vai quando clica, e o que ela ganha lá?"
   > "Página de cadastro da aula. Ela ganha a aula gratuita de quinta."
5. "Qual evento de conversão dispara quando ela se cadastra?"
   > "Acho que Lead." Marcado `[A CONFIRMAR]`, o dono confere no gerenciador antes de subir.

---

## Passo 1 e 2 · Os 4 ângulos, uma dor cada (STOP)

A skill escreveu 4 ganchos, cada um mordendo UMA dor diferente do mesmo avatar, e parou pra aprovação.

| Peça | Dor que morde | Gancho (1ª linha) | Sub (2ª linha) |
|---|---|---|---|
| 01 | agenda cheia, conta vazia | "Sua agenda está cheia. E o mês, fecha?" | "O que muda quando a sessão deixa de ser o produto." |
| 02 | paciente que some | "O paciente melhora na terceira sessão e some." | "O plano de alta que faz ele ficar mais oito semanas." |
| 03 | preço por hora | "Você cobra por hora. Seu resultado dura meses." | "Quem cobra pelo resultado cobra outro número." |
| 04 | depender de indicação | "Sua agenda depende de quem indicou você." | "Como encher a semana sem esperar o telefone tocar." |

**STOP.** Pergunta ao dono: "esses 4 ângulos batem com o que dói no seu cliente? Corto algum, troco
algum?"

> Resposta do dono: "o 4 troca. Indicação eu tenho de sobra. Coloca o medo de dar desconto."

Peça 04 reescrita: **"Toda vez que ele hesita, você baixa o preço."** / sub: "O que dizer no lugar
do desconto." Aprovado.

---

## Passo 4 · `identidade.json` como ficou

```json
{
  "cor_principal": [18, 58, 44],
  "cor_texto_sobre_veu": [17, 17, 17],
  "cor_sub": [110, 110, 110],
  "fonte": "fontes/sans-sistema.ttf",
  "selo": "PARA FISIOTERAPEUTAS · AULA GRATUITA",
  "cta": "Cadastre-se",
  "assinatura": "@perfil_ficticio",
  "formato": [1080, 1350]
}
```

Nota registrada pro dono: `[A CONFIRMAR]` a fonte real da marca. Enquanto ela não vier, todas as
peças saem com a sem-serifa do sistema, e trocar depois custa um lote novo.

## Passo 5 · `manifesto.json` como ficou (2 das 4 entradas)

```json
{
  "pecas": [
    {
      "foto": "fotos/autoridade-01.jpg",
      "gancho": "Sua agenda está cheia. E o mês, fecha?",
      "sub": "O que muda quando a sessão deixa de ser o produto.",
      "saida": "out/peca-01-agenda.jpg"
    },
    {
      "foto": "fotos/autoridade-02.jpg",
      "gancho": "O paciente melhora na terceira sessão e some.",
      "sub": "O plano de alta que faz ele ficar mais oito semanas.",
      "saida": "out/peca-02-alta.jpg"
    }
  ]
}
```

Corte da foto conferido peça a peça: topo do cabelo a 90 px da borda superior, queixo a 380 px.
Nenhuma cabeça cortada.

## Passo 5 · O que aconteceu no lote

Primeira rodada: as peças 01 e 02 saíram. A 03 gravou no `progress.json` e não gerou arquivo.
Aplicando o critério de retentativa: a entrada da 03 foi apagada do `progress.json`, o jpg parcial
saiu, o lote rodou de novo e a 03 saiu inteira. A 04 saiu na mesma rodada. Nenhuma peça precisou de
segunda retentativa, então o lote não parou.

## Passo 6 · O lint

```
python3 scripts/lint_copy.py copy-lote.md
```

Primeira passada reprovou a peça 03: o sub estava "Quem cobra pelo resultado transforma o próprio
negócio." Verbo-clichê. Reescrito pra "Quem cobra pelo resultado cobra outro número." Segunda
passada: exit 0.

## Passo 7 · A mensagem de prévia (STOP)

> "Saíram as 4 peças, cada uma numa dor diferente: agenda cheia e conta vazia, paciente que some,
> preço por hora, medo de dar desconto. Estão em `out/`. Duas coisas ficaram marcadas pra você
> confirmar: a fonte da sua marca (usei uma sem-serifa do sistema) e o evento de conversão do
> cadastro. Aprova as 4, corto alguma, refaço alguma?"

## Passo 8 · O que ficou escrito pro dono subir

Campanha nasce PAUSADA. UTM padrão gravado no `spec-render.md`:

```
utm_campaign=aula-gratuita-fisio
utm_content={{ad.name}}
utm_term={{adset.id}}
```

---

## Gate de qualidade, como foi preenchido nesse lote

| Critério | Resultado |
|---|---|
| Anti-IA na copy | exit 0 na segunda passada |
| Ângulo por peça | 4 dores distintas, nenhuma repetida |
| Foto | rosto real, cabeça inteira nas 4 |
| Identidade | tudo do `identidade.json`, fonte `[A CONFIRMAR]` |
| Contraste | véu creme, 1ª linha escura, sub cinza médio, conferido no jpg final |
| Lastro | nenhum número na copy, nada a confirmar |
| Prévia | mandada, aguardando o OK |

---

## Ação 2 · Playbook, como ficaria pro mesmo caso

Se o pedido tivesse sido "monta o playbook pra eu repetir isso todo mês", a saída seria
`playbook-criativo-fisio.md` com os 4 campos:

- **CAMPO 1 (FOTO):** 3 fotos de estúdio, fundo claro, tratadas em preto e branco. Reposição a cada
  6 meses.
- **CAMPO 2 (IDENTIDADE):** o `identidade.json` acima, com a fonte `[A CONFIRMAR]`.
- **CAMPO 3 (4 GANCHOS):** as 4 dores da tabela do passo 1, com o gancho ao lado.
- **CAMPO 4 (DESTINO):** página de cadastro da aula, evento Lead `[A CONFIRMAR]`, UTM padrão acima.

---

## Ação 3 · Diagnóstico, como ficaria

Se duas semanas depois o dono voltasse com "o criativo 02 morreu, refaço a arte?", a skill perguntaria
em que públicos ele rodou, e a saída seria `diagnostico-criativo.md`:

| Criativo | Público | Custo por lead |
|---|---|---|
| peça 02 | aberto + semelhante de compradores | 4,10 |
| peça 02 | interesse "fisioterapia" | 19,70 |
| peça 01 | interesse "fisioterapia" | 21,30 |

**Veredito em 1 linha:** a peça 02 não morreu, ela rodou num interesse forçado; no público aberto
ela é a mais barata do lote, então a alavanca aqui é o conjunto, não a arte.
