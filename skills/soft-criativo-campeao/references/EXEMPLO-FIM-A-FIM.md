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

Insumo faltando: as dores nomeadas, as fotos, o arquivo da fonte, o evento de conversão. A triagem
separou: a dor muda a peça, então vai numa pergunta ANTES de produzir; as fotos entram na mesma
mensagem porque ela já ia sair; fonte e evento não mudam a peça e viram premissa marcada.

## A pergunta que a skill fez (uma mensagem, 2 itens)

> "Pra montar as 4 artes: (1) quem é a pessoa que você quer nessa aula, e o que dói nela hoje?
> (2) me manda 2 ou 3 fotos suas em boa resolução. A fonte eu deixo numa sem-serifa e o evento do
> cadastro como Lead, os dois marcados pra você conferir."

Resposta: "Fisioterapeuta que atende o dia inteiro, ganha por sessão e não sobra nada. Ele vive com
medo de o paciente sumir depois da terceira sessão." Mais 3 arquivos de estúdio, fundo claro, meio
corpo. Resolução: verde declarado, fonte sem-serifa do sistema marcada `[A CONFIRMAR]`, evento Lead
marcado `[A CONFIRMAR]` pro dono conferir no gerenciador antes de subir.

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

Gravada em `conferencia/mensagem-dono.txt`, 5 linhas, a decisão do dono primeiro:

> Aprova as 4 peças, ou corto ou refaço alguma?
> Pronto: 4 artes, cada uma numa dor; abra a pasta `out/`.
> Usei uma sem-serifa no lugar da fonte do site e marquei o cadastro como Lead.
> 1. Me manda o arquivo da fonte do site?
> 2. O evento do cadastro no gerenciador é Lead mesmo?

Linha colada: `linhas da mensagem: 5 (teto 8)`. A lista das dores, os arquivos e o porquê de cada
ângulo ficam no `copy-lote.md`.

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

---

## Ação 0 · Anunciar, a tarefa inteira (mesmo caso, outro pedido)

Três semanas depois, o mesmo dono volta: "quero anunciar meu curso de protocolo de alta. É R$ 197
e tem uma VSL de 12 minutos. Quero anúncio rodando essa semana." Tudo abaixo continua FICTÍCIO.

**A triagem (o perfil já tinha foto e identidade; ticket e destino vieram no pedido):** falta a 1ª
frase da VSL, que muda a peça (a ponte), então sai UMA mensagem antes de produzir, com o item que
muda a peça e um que não muda, porque a mensagem já ia sair:

> "Pra montar os anúncios da sua VSL: (1) cola a primeira frase dela; (2) quanto topa gastar pra
> testar, no total? Responde o que souber, o resto eu marco."

Resposta: "Seu paciente melhora na terceira sessão e some. Existe um plano de alta de 8 semanas que
resolve isso. Uns 600." A pergunta da conta vai junto do STOP dos ângulos, e a resposta foi: nunca
rodou, conta nova.

**Tipo de peça pelo destino:** `destino: VSL · tipo no teste: imagem · tipo na escala: vídeo ·
porquê: o lote de imagem testa o ângulo barato, e o vídeo conecta com o vídeo que vem depois`.

**Passo 1 · o material do dono, antes das listas** (`conferencia/material-do-dono.txt`):

```
terceira sessão | tipo: número | origem: pedido, 1ª frase da VSL
plano de alta de 8 semanas | tipo: objeto | origem: pedido, 1ª frase da VSL
R$ 197 | tipo: número | origem: pedido
fotos de estúdio, fundo claro, meio corpo | tipo: objeto | origem: pasta fotos/
```

Cada peça usa pelo menos 1 item: a 1 usa "terceira sessão" no gancho e "plano de alta de 8 semanas"
no sub; as outras 3 usam "plano de alta" no gancho ou no texto do anúncio.
Linha colada: `peças no lote: 4 · com material do dono: 4`.

**Passo 1 · as 3 listas antes dos ganchos:**

| Personas | Curiosidade da oferta | Dores |
|---|---|---|
| fisio recém-formado | o plano de alta de 8 semanas | paciente some na 3ª sessão |
| fisio com agenda cheia | a consulta de alta | agenda cheia e conta vazia |
| fisio que atende atleta | a planilha de retorno | dá desconto quando o paciente hesita |

Combinações escolhidas, sem repetir: (1) recém-formado · plano de alta · paciente some; (2) agenda
cheia · consulta de alta · conta vazia; (3) atleta · planilha de retorno · paciente some depois da
prova; (4) agenda cheia · plano de alta · desconto. Todas começam por ângulos que a VSL já tem.

**Congruência:** o termo-gancho da VSL é "plano de alta". As peças 1 e 4 usam o termo literal no
gancho; a 2 e a 3 usam no `texto_anuncio`. Linha colada: `peça 1 | termo-gancho: plano de alta |
está em: gancho`, e assim nas 4, com a contagem do comando do gate: `4 4`.

**Entrada do manifesto com texto e título do anúncio (peça 1):**

```json
{
  "foto": "fotos/autoridade-01.jpg",
  "gancho": "Seu paciente melhora na terceira sessão e some.",
  "sub": "O plano de alta de 8 semanas que faz ele ficar.",
  "cta": "Assiste a aula de 12 minutos na página",
  "texto_anuncio": "O paciente some quando melhora. O plano de alta muda o que ele compra de você.",
  "titulo_anuncio": "O plano de alta que segura o paciente",
  "saida": "out/peca-01-alta.jpg"
}
```

**Roteiro de vídeo: NÃO sai nesta rodada** (`tipo no teste: imagem`); o plano diz em 1 linha que ele nasce do ângulo que validar, pela Ação 1 tipo vídeo. Trecho de como ele sairia depois:

```
formato: expert em ação (atendendo, mãos no joelho do paciente) · canal: Reels · duração alvo: 1:15
0:00 | hook: "Seu paciente melhora na terceira sessão e some." | na tela: "3ª sessão" | apoio: a ficha do paciente
0:04 | aterrissagem: "E o pior é que ele sumiu porque você fez o trabalho certo." | ...
0:30 | prova: demonstração (o plano de alta aberto na tela) · nicho confia em colega de profissão
0:55 | CTA 1 em 0:55: "A aula de 12 minutos mostra o plano inteiro."
```

Instrução de edição anexa: take 2 do atendimento; referência de estilo com link e minuto
`[A CONFIRMAR: link de referência]`; na frase "o plano de alta aberto" entra a tela do plano.

**Plano de teste (resumo do `plano-de-teste.md`):**

```
Ticket: 197 · Caixa de teste: 600 · Destino: VSL · Conta: nova
Verba: 1 ticket x 4 ângulos = 788, acima do caixa. Caixa curto: 0,5 x 197 x 4 = 394 em 3 dias
= 32,83 por dia por conjunto (acima do piso de 30).
Fases: teste 3 dias · pré-escala a 2x a verba do teste, ciclo de 3 a 5 dias · escala só com validado.
Estrutura: 4 conjuntos, 1 por ângulo, 2 ganchos em cada (a peça do lote e uma variação escrita no
passo 1): 8 anúncios.
Matar cedo: CTR de link abaixo de 3,5% depois de 2 dias sem venda; custo de início de checkout acima de 20% do ticket.
Régua de partida; depois de 7 dias rodando, vale o seu próprio recorde.
Escalar: degraus de 20% a 30% com 2 a 3 dias entre eles; teto no degrau em que o lucro do mês cai.
Quem sobe: soft-trafego-meta não instalada, passo a passo à mão anexo.
```

Conta nova: o plano avisa que os 10 a 15 primeiros dias rendem pior, e que caixa sobrando não
acelera essa fase. Conferência colada: `plano de teste: 6 de 6 blocos`.
