# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Números, datas, taxas e resultados foram inventados só pra mostrar
> a FORMA de cada saída. Nada disso é caso real e nenhum número daqui serve de referência pra um
> diagnóstico de verdade. Num trabalho real, todo número tem fonte e data ditas pelo dono, e o que
> não tiver nasce marcado.

**O caso fictício:** uma consultoria de organização de estoque para lojas de material de construção.
Dona fictícia: consultora que atende lojas de bairro com 5 a 30 funcionários. Ticket do serviço:
R$2.800. Ela publica no Instagram, atende por mensagem direta e fecha em reunião por vídeo.

Este arquivo mostra as três ações, na ordem, mais um caso em que a skill se recusou a diagnosticar.

---

## Ação 1 · DIAGNÓSTICO

### Passo 0, o que a dona mandou

Pedido dela:

> "Semana passada foi horrível, não vendi nada. O que tá errado no meu funil?"

A skill não opinou. Pediu tudo que faltava numa mensagem só:

> Pra dizer o que quebrou eu preciso de 8 números da semana, com a fonte e o período de cada um.
> Manda tudo de uma vez, na ordem que der:
>
> 1. quantas peças você publicou · 2. alcance somado · 3. salvamentos e compartilhamentos ·
> 4. cliques no link · 5. mensagens diretas qualificadas · 6. conversas que evoluíram ·
> 7. reuniões realizadas · 8. vendas e receita
>
> E mais três: qual era a meta da semana, qual o seu ticket, e o que a projeção previa.

Resposta dela, colada como veio:

> "12 a 18/03, tudo do painel do Instagram: 5 peças (2 reels, 3 carrosséis), alcance 9.400,
> salvamentos+compartilhamentos 210, cliques 64, DM qualificada 23, conversas 9, reuniões 2, vendas 0.
> Meta era 3 vendas. Ticket 2.800. A projeção falava em 40 DMs pra chegar em 3 vendas."

### Passo 1, confiabilidade (rodado antes de qualquer taxa)

| Teste | Resultado | Consequência |
|---|---|---|
| **Amostra** | DMs 23 (piso 10, passa) · conversas 9 (piso 10, **reprova por 1**) · reuniões 2 (piso 10, **reprova**) | as duas últimas etapas não viram recomendação |
| **Janela** | ticket R$2.800, faixa de 1.500 a 5.000, janela mínima 4 semanas. A leitura é de 1 semana | venda da semana não se julga sozinha; declarado |
| **Rastreio** | 64 cliques no painel, e a dona confirma 61 no encurtador. Diferença de 5%, dentro do normal | passa |
| **Atribuição** | ninguém comprou, então não há venda pra atribuir | não se aplica |

Saída deste passo, escrita na entrega:

> Dois avisos antes da leitura. Primeiro: com 2 reuniões realizadas eu **não** consigo dizer nada
> sobre o seu fechamento. A diferença entre um script bom e um ruim nesse volume é uma reunião.
> Segundo: seu ciclo de venda pede 4 semanas de janela, então "zero venda em 7 dias" ainda não é um
> resultado, é meio caminho. O que dá pra ler com confiança é tudo até a mensagem direta.

### Passo 2, a conta etapa a etapa

```
peças → alcance:        9.400 ÷ 5 = 1.880 por peça  · faixa 800-5.000 (carrossel) · VERDE
alcance → engajamento:  210 ÷ 9.400 = 2,2%          · faixa 1,5-4%               · VERDE
engajamento → clique:   64 ÷ 210 = 30%              · faixa 20-40%               · VERDE
clique → DM:            23 ÷ 64 = 36%               · faixa 25-50%               · VERDE
DM → conversa:          9 ÷ 23 = 39%                · faixa 45-65%               · VERMELHO
conversa → reunião:     2 ÷ 9 = 22%                 · [AMOSTRA INSUFICIENTE, piso 10]
reunião → venda:        0 ÷ 2 = 0%                  · [AMOSTRA INSUFICIENTE, piso 10]
```

Detalhe que importa: a etapa `DM → conversa` está em 39% contra uma faixa baixa de 45%. Isso é 87% da
referência, o que cairia em amarelo. Mas a dona tem histórico próprio de três meses nessa etapa,
média de 58%, e **quando o histórico próprio e a referência genérica discordam, vence o histórico**.
Contra os 58% dela, 39% é 67% da própria média, e aí é vermelho.

### Passo 3, o gargalo

Primeira etapa vermelha de cima pra baixo: **DM para conversa**.

> Seu gargalo é a primeira resposta na mensagem direta. Chegaram 23 pessoas qualificadas e só 9
> viraram conversa de verdade. Todo o topo do funil está saudável, você não tem problema de alcance
> nem de gancho nesta semana.

### Passo 4, projetado contra realizado

```
projetado 40 DMs · real 23 · delta -43%    (delta de VOLUME)
projetado 58% de DM→conversa · real 39% · delta -33%  (delta de TAXA)
projetado 3 vendas · real 0 · janela ainda aberta, não conclusivo
```

Leitura em uma linha: dois problemas somados, entrou menos gente **e** a que entrou avançou menos. O
delta de taxa é o que se conserta esta semana, porque o de volume depende de mais publicação e leva
mais tempo pra mostrar efeito.

### Passo 5, o que decide e o que é vaidade

O reel de terça teve o maior alcance da semana, 4.100, quase o dobro da média dela. E trouxe 2 DMs,
das quais nenhuma virou conversa. O carrossel de quinta teve 1.200 de alcance, o menor, e trouxe 7
DMs, das quais 4 viraram conversa.

> O reel de terça é a peça de vaidade da semana: alcance alto, filtro nenhum. O carrossel de quinta é
> a peça que decide. Se você for repetir alguma coisa, repete o de quinta, não o de terça.

### Passo 6 e 7, a entrega como ela chega à dona

```
DIAGNÓSTICO · 12 a 18/03 · fonte: painel do Instagram

O funil está saudável até a mensagem direta. Ele vaza na primeira resposta.

  peças → alcance        1.880/peça   VERDE
  alcance → engajamento  2,2%         VERDE
  engajamento → clique   30%          VERDE
  clique → DM            36%          VERDE
  DM → conversa          39%          VERMELHO (sua média é 58%)
  conversa → reunião     22%          [AMOSTRA INSUFICIENTE, piso 10]
  reunião → venda        0%           [AMOSTRA INSUFICIENTE, piso 10]

  projetado 40 DMs · real 23 · delta -43%   (volume)
  projetado 58% DM→conversa · real 39% · delta -33%   (taxa)

Gargalo: a primeira resposta na mensagem direta. 23 chegaram, 9 avançaram.

AÇÃO ÚNICA DO CICLO
  o quê:     reescrever a primeira resposta da mensagem direta, as próximas 25
  por quê:   DM→conversa em 39% contra sua média própria de 58%, primeira etapa vermelha
  alvo:      DM→conversa acima de 50% nas próximas 25 mensagens
  quando medir: próxima leitura, 7 dias, mesma fonte

REPASSE
  skill:     soft-vendas-sdr
  leve isto: taxa atual 39% · média própria 58% · alvo 50% · as 9 conversas que
             avançaram e as 14 que morreram, pra ver o que separa as duas
  o que NÃO peça lá: mudança de oferta, de preço ou de público. Não é o gargalo
             desta semana, e mexer nisso agora suja a medição da ação acima.

Não recomendo nada sobre o seu fechamento nem sobre o script de reunião: com 2 reuniões
não dá pra separar problema real de variação normal. Precisa de 10. No seu ritmo atual,
isso são umas 5 semanas.
```

Repare no que **não** foi entregue: nenhuma opinião sobre o closer, nenhuma sugestão de mudar oferta,
nenhuma lista de cinco melhorias. Uma ação, um alvo, um destino.

---

## Ação 2 · COMPARAÇÃO ENTRE PERÍODOS

Duas semanas depois, a dona voltou:

> "Melhorou ou piorou em relação à semana retrasada?"

Os dois períodos, mesma fonte, mesma duração:

| Número | 12 a 18/03 | 26/03 a 01/04 |
|---|---|---|
| DMs qualificadas | 23 | 31 |
| DM → conversa | 39% | 55% |
| conversa → reunião | 22% | 29% |
| reuniões | 2 | 5 |
| reunião → venda | [amostra insuficiente] | [amostra insuficiente] |
| receita | 0 | 2.800 |

Decomposição, só das etapas que passaram no teste de amostra nos **dois** períodos:

```
Leads no funil: 23 → 31 · delta +8 (+35%)
Conversas geradas: 9 → 17 · delta +8 (+89%)

Decomposição do ganho de 8 conversas, um fator por vez:
  1. volume de DMs (23→31, taxa fixa em 39%):        +3,1 conversas
  2. taxa DM→conversa (39%→55%, volume fixo em 23):  +3,7 conversas
                                    soma dos efeitos: +6,8
  resíduo (os dois fatores subindo juntos):          +1,2
                                    total conferido: +8,0 ✓

Leitura: a ação do ciclo passado funcionou. A taxa saiu de 39% pra 55%, acima do
alvo de 50%, e responde por 46% do ganho. O volume subiu junto e responde por 39%.
```

O que a skill disse sobre o resto:

> A receita saiu de 0 pra 2.800, mas isso é **uma venda**. Não decomponho receita com esse volume, e
> não digo que seu fechamento melhorou: continua sem amostra. O que eu posso afirmar com confiança é
> que a etapa que estava vermelha voltou pra faixa e passou do alvo.
>
> A soma da decomposição fecha com o delta real, então os números batem entre si.

E o repasse mudou de destino, porque o gargalo mudou:

```
Novo gargalo: conversa → reunião, 29% contra sua média própria de 41%.
Mas atenção: 17 conversas passa do piso, então esta etapa agora É legível.
Era a primeira vermelha do ciclo anterior que virou verde; esta é a nova primeira.
```

---

## Ação 3 · ESCALA

Três meses depois, com volume:

> "Vale colocar dinheiro em anúncio?"

```
FUNIL EM REAIS · março · fonte: painel de anúncios + planilha da dona

  investimento no mês:            4.200
  leads gerados:                    140
  custo por lead:                 30,00
  agendamentos:                      38
  custo por agendamento:         110,53
  comparecimentos:                   29
  custo por comparecimento:      144,83
  calls realizadas:                  29
  custo por call realizada:      144,83
  faturamento por call realizada: 386,21  (11.200 ÷ 29)

  Leitura: cada call custa 144,83 e devolve 386,21. Sobra 241,38 por call,
  margem de 62% sobre o custo de aquisição. Escalar faz sentido.

  Limite: sua capacidade hoje é de 3 a 4 calls por dia. Em 29 calls no mês você
  está usando cerca de 40% da capacidade de uma agenda. Dá pra dobrar a verba
  antes de a agenda ser o gargalo, e o próximo número a vigiar não é o custo,
  é a taxa de comparecimento (29 de 38 = 76%).
```

Sobre o retorno sobre anúncio, a leitura própria desta skill:

> Seu retorno sobre o anúncio deu 2,67. Isso não é ruim, é sinal de que você está investindo pouco.
> Retorno muito alto costuma significar subinvestimento: você está colhendo só o público mais barato
> e deixando volume na mesa.

---

## O caso em que a skill se RECUSOU a diagnosticar

Vale mostrar, porque é o comportamento mais difícil de sustentar.

Pedido:

> "Rodei um anúncio novo por 3 dias, gastei 180 reais, deu 4 cliques e nenhuma venda. O criativo tá
> ruim, né? Já mudo?"

Resposta:

```
Não dá pra dizer isso, e mudar agora custa caro.

  cliques: 4 · piso pra comparar com faixa: 30 · [AMOSTRA INSUFICIENTE]
  janela: 3 dias · seu ticket pede 4 semanas · [JANELA CURTA]

Com 4 cliques, a diferença entre um criativo bom e um ruim é indistinguível de
sorte. Se você trocar o criativo agora, perde os 180 reais que já rodaram e
recomeça a contagem do zero, sem ter aprendido nada.

O que dá pra fazer:
  o quê: deixar rodar até 1.000 impressões na variante, ou até 30 cliques
  alvo:  o que vier primeiro
  estimativa: no ritmo atual (60 reais/dia, ~340 impressões/dia), são uns 3 dias
  aí sim: a gente lê e decide com número

Não estou dizendo que o criativo é bom. Estou dizendo que ninguém sabe ainda,
e que decidir agora é chute com cara de análise.
```

Nenhuma recomendação foi dada, nenhuma skill foi acionada, e a saída foi uma instrução de medição
com prazo. É este o comportamento quando o dado não sustenta a conclusão.
