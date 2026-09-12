# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** O negócio, os números, os identificadores, os custos e os
> resultados foram inventados só pra mostrar a FORMA de cada saída. Nada disso é caso real e nada
> disso pode ser copiado pra uma entrega de verdade. Num trabalho real, todo número sem fonte nasce
> marcado `[DADO: confirmar]`.

**O caso fictício:** uma professora de natação infantil que dá aula em piscina alugada e quer encher
a turma do semestre. Ela vende uma avaliação presencial de 120 reais que vira matrícula de 380 por
mês. Perfil com 6 mil seguidores. Verba declarada: 900 reais no mês.

Este arquivo mostra a saída resumida das duas ações, na ordem, mais o formato exato dos dois
documentos que a skill entrega.

---

## O que o dono deu de entrada

> "Tenho 900 reais pra colocar em anúncio esse mês. Quero encher a turma. Meu reel do bebê boiando
> sozinho deu 40 mil visualizações."

---

# Ação 1 · Plano de mídia

## Passo A0 · Os 5 pré-requisitos, conferidos um por um

| Pré-requisito | Situação |
|---|---|
| Posicionamento de pé | sim, ela fala com mãe de bebê de 6 meses a 3 anos, com medo de água |
| Perfil convertendo | sim, ganha em média 90 seguidores por semana no orgânico |
| Destino no ar | sim, mensagem com a palavra AVALIAR, respondida por ela mesma |
| Peça orgânica acima da média | sim, o reel do bebê, 40 mil contra a média de 3 mil |
| Primeira venda fechada | sim, 14 matrículas ativas |

Os 5 cumpridos. O plano seguiu.

## Passo P0 · A plataforma

Meta. O motivo escrito no plano: o avatar é mãe de 28 a 42 anos, que não busca "aula de natação
para bebê" no Google com volume, e a munição dela é vídeo do próprio ambiente. Google fica de fora
até existir volume de busca. TikTok fica de fora porque a segunda plataforma só entra com a primeira
positiva.

## Os números que ela mandou, e o que faltou

| Peça | Formato | Desempenho orgânico |
|---|---|---|
| bebê boiando sozinho | reel | 40 mil visualizações, 310 envios |
| 3 sinais de que seu filho tem medo de água | carrossel | 82 salvamentos |
| a mãe que chorou na primeira aula | reel | 9 mil visualizações, 140 envios |
| como escolher a escola de natação | carrossel | 61 salvamentos |

Faltou o custo por resultado atual, porque ela nunca anunciou. Marcado `[DADO: confirmar]` na
projeção de custo por mensagem, e a régua saiu parametrizada.

## O documento entregue: `plano-trafego-natacao-infantil.md`

```
PLANO DE TRÁFEGO · natação infantil · setembro
verba do mês: 900  ·  plataforma: Meta  ·  nível: gerenciador

AS PEÇAS

| # | Peça | Função | Objetivo | Público | Verba/dia | Dias | Métrica-chave |
|---|---|---|---|---|---|---|---|
| 1 | bebê boiando sozinho | Atração | tráfego qualificado | amplo, 25-45, raio 12 km | 15 | 30 | custo por visita ao perfil |
| 2 | 3 sinais de medo de água | Lead | leads | amplo, 25-45, raio 12 km | 9 | 30 | custo por mensagem, alvo abaixo de 3 |
| 3 | a mãe que chorou | Remarketing | leads | quem interagiu 30-90 dias | 6 | 30 | conversão em avaliação marcada |

DISTRIBUIÇÃO (50/30/20)
distribuição pura 450  ·  lead 270  ·  remarketing 180  ·  total 900

RÉGUA DE DECISÃO (revê a cada 2 dias)
custo por seguidor até 0,80: aumenta 50% por mais 7 dias
de 0,80 a 0,99: troca o público
1,00 ou mais: pausa a peça e sobe a próxima da lista
custo por mensagem acima de 3 por 2 dias seguidos: pausa (teto pré-autorizado)

ROI MENSAL ABSOLUTO (projeção)
900 de verba  ·  custo por mensagem projetado 2,50 [DADO: confirmar]  ·  360 mensagens
taxa de comparecimento estimada 20% [DADO: confirmar]  ·  72 avaliações a 120 = 8.640
matrícula estimada 30% [DADO: confirmar]  ·  21 matrículas a 380 = 7.980 por mês recorrente
ROI do mês: 8.640 menos 900 = 7.740, sem contar a recorrência.

CAPA POR TERRENO
o reel do bebê tem gancho específico (bebê boiando), então entra pelo gerenciador com objetivo
de tráfego qualificado. Nenhuma peça de capa ampla recebe verba neste plano.

O QUE FALTA CONFIRMAR
custo por mensagem real, comparecimento e taxa de matrícula. Os três saem na primeira semana.
```

**STOP.** A skill parou aqui e perguntou: "aprova esse plano? Ele gasta 900 no mês, dividido em 3
peças, e a primeira revisão é em 2 dias."

> Resposta: "aprova, sobe."

---

# Ação 2 · Execução na conta

## Gate de entrada

Os 5 pré-requisitos, conferidos na Ação 1. Plano aprovado, com o OK acima. Ambiente: com shell,
motor de anúncios conectado. Seguiu.

## Passo B1 · Auditoria da conta

Conta encontrada e habilitada. Pontuação de oportunidade em 62, de nível de conta, anotada como
observação e não atribuída a nenhuma campanha. Nenhum erro de entrega. Evento de conversão
respondendo. Seguiu.

## Passo B2 · Estrutura criada, tudo PAUSADO

Campanha de tráfego qualificado pra peça 1, orçamento por conjunto, público amplo com raio de 12 km,
posicionamento no feed e nos stories. Criativo montado com o identificador da página, legenda já
aprovada. Nenhuma marcação de conteúdo gerado por IA, porque o reel é gravação real da piscina dela.

**STOP.** A skill mostrou os identificadores e perguntou: "pode ativar? Vai gastar 15 por dia por 30
dias na peça 1, 450 no total."

> "Pode."

## Passo B3 · Publicação e automação

O carrossel da peça 2 foi publicado, com os cards hospedados na página estática dela, todos
respondendo 200. A automação de comentário para mensagem foi ligada com a palavra AVALIAR, 5
variações de resposta pública, e o botão de **resposta rápida**, não link externo.

**STOP** antes de publicar. Aprovado.

## O documento entregue: `runbook-natacao-2026-09-04.md`

Este é o teto de tamanho do runbook, não o piso.

```
RUNBOOK · natação infantil · 04/09/2026

O QUE FOI FEITO
3 campanhas criadas e ativadas com OK do dono, na distribuição 50/30/20 do plano aprovado.
1 carrossel publicado com a automação de comentário para mensagem ligada na palavra AVALIAR.
Nada foi ativado sem pergunta; tudo nasceu pausado.

IDENTIFICADORES
| Item | Identificador | Situação |
|---|---|---|
| campanha atração | cmp_8841 | ativa |
| conjunto atração | set_9930 | ativo, 15/dia |
| anúncio atração | ad_5521 | ativo |
| campanha lead | cmp_8842 | ativa |
| campanha remarketing | cmp_8843 | ativa |
| post publicado | media_71204 | no ar |
| automação | auto_3390 | ligada, resposta rápida |

REGRAS DE PROTEÇÃO AGENDADAS
freio de perda: custo por mensagem acima de 3 por 2 dias, pausa (teto pré-autorizado no plano)
escalar: custo no alvo por 3 dias, propõe mais 20 a 50% e espera OK
fadiga: frequência acima de 3,5 em 7 dias, alerta pra trocar o criativo

PRÓXIMOS PASSOS
06/09: primeira leitura de desempenho, e a régua do plano decide continuar, trocar público ou pausar.
```

---

## A leitura do dia 2, e a decisão que ela produziu

```
LEITURA · 06/09 · 2 dias de veiculação

| Peça | Gasto | Resultado | Custo por resultado | Régua diz |
|---|---|---|---|---|
| 1 atração | 30 | 214 visitas ao perfil | 0,14 por visita | dentro do alvo, mantém |
| 2 lead | 18 | 4 mensagens | 4,50 por mensagem | acima do teto de 3, atenção |
| 3 remarketing | 12 | 2 avaliações marcadas | 6,00 por avaliação | dentro, mantém |
```

A Ação 2 leu o número. A régua da Ação 1 decidiu: a peça 2 está a 4,50, acima do teto de 3, mas com
1 dia só de custo alto. O freio de perda pede 2 dias seguidos, então nada foi pausado ainda. O
diagnóstico apontou UM gargalo e UM ajuste: a chamada do carrossel pede a palavra AVALIAR no último
slide, e o slide está sem contraste. Ajuste único proposto, e a reescrita da chamada foi devolvida
pra **soft-conteudo-headlines**, não escrita aqui.

**STOP.** "A peça 2 está a 4,50 por mensagem, acima do teto de 3. Se amanhã continuar, a regra pausa
sozinha, como você autorizou. O que eu vejo é a chamada no último slide, que está sem contraste.
Quer que eu peça a reescrita da chamada antes de deixar pausar?"

---

## O que teria mudado sem motor conectado

Nada do método muda, só a mão. Em vez dos identificadores, o mesmo `runbook-natacao-2026-09-04.md`
carregaria:

```
PLANO PRONTO PRA COLAR NO GERENCIADOR

CAMPANHA 1 · atração
objetivo: tráfego  ·  nome: ATR · reel-bebe · amplo · 2026-09
orçamento: por conjunto  ·  status ao criar: pausado

CONJUNTO
verba 15/dia  ·  30 dias  ·  público amplo, 25-45, raio 12 km da piscina
sem caixinha de interesse (o criativo segmenta)
posicionamento: feed e stories do Instagram

ANÚNCIO
criativo: reel-bebe-boiando.mp4
legenda: (a copy aprovada, transcrita inteira no campo de texto)
chamada: Saiba mais  ·  destino: mensagem com a palavra AVALIAR

ONDE CLICAR
1. Gerenciador, botão Criar, objetivo Tráfego.
2. No nível do conjunto, verba diária 15, e desmarcar a expansão de público.
3. No nível do anúncio, subir o vídeo e colar a legenda no campo de texto principal.
4. PARE aqui e mostre ao dono antes de publicar. A ativação é decisão dele.

Conectar o motor faz a skill subir isso sozinha, sem você tocar no gerenciador.
```
