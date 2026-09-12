# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, empresa, números e falas foram inventados só pra mostrar a
> FORMA da saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega de verdade. Num
> trabalho real, todo dado nasce com a fonte escrita ao lado, e o que não foi confirmado vira
> `[A CONFIRMAR]` e depois pergunta na call.

**O caso fictício:** o dono vende um serviço de manutenção preventiva de máquinas de café pra redes de
padaria. Ticket médio de 2.400 reais por mês por rede. A call é com uma rede fictícia de 9 padarias que
pediu uma conversa depois de duas máquinas quebrarem no mesmo mês. É a segunda conversa: a primeira foi
uma descoberta de 20 minutos por telefone, há 12 dias.

Este arquivo mostra a saída das 4 ações reunidas no formato real de entrega. A saída real é do mesmo
tamanho: dossiê é um documento curto por definição.

---

## O que o dono deu de entrada

> "Amanhã às 10 tenho call com a rede de padarias que me chamou. Vai o dono e a gerente de operações
> que eu não conheço. Eles pediram proposta mas eu ainda não passei preço. Não sei bem o que levar."

**O que faltava:** o objetivo não estava declarado, o papel da gerente de operações era desconhecido, e
o dono não sabia dizer o que tinha ficado combinado na primeira conversa.

## As perguntas que a skill fez (uma por vez)

1. "Com quem você vai falar, nome e cargo?" → *"O dono, [nome fictício], e a gerente de operações, [nome fictício]. A gerente não estava na primeira conversa."*
2. "Que tipo de reunião é essa?" → *"Eles pediram proposta. Acho que é de proposta e negociação."*
3. "O que já rolou entre vocês até aqui?" → *"Uma call de 20 minutos, eles contaram das duas máquinas que quebraram, eu falei do plano de visita mensal. Ficou de eu mandar uma proposta e eu não mandei ainda."*
4. "Tem alguma coisa que você já sabe que vai ser tema?" → *"Preço. E eles têm um técnico que vem quando quebra, então vão comparar com isso."*

**Premissa declarada em 1 linha:** a call foi tratada como reunião de proposta, mas o dono nunca
levantou o custo real da quebra pra essa rede, então o roteiro reserva 8 minutos de descoberta antes do
preço, porque sem esse número a proposta não tem contra o que ser comparada.

**Sobre pesquisa:** o ambiente não tinha CRM nem acesso à web nesta sessão. O retrato saiu com o que o
dono contou, marcado `[A CONFIRMAR: sem pesquisa externa]`, e os buracos viraram perguntas da call.

---

## A saída: `dossie-call.md`

```markdown
# Dossiê de call: Rede de padarias [nome fictício]

**Reunião:** proposta e negociação · amanhã, 10h · 30 minutos
**Quem está na sala:** [dono] · [gerente de operações]
**O objetivo desta call:** sair com a data de início do primeiro contrato de 3 meses acordada, ou
com a objeção real nomeada por escrito.

---

## O quadro da conta

| Campo | Valor |
|---|---|
| Quem é | rede de 9 padarias de bairro, mesma cidade `[A CONFIRMAR: número de unidades]` |
| Tamanho | não confirmado `[A CONFIRMAR: sem pesquisa externa]` |
| Situação | negociação aberta, proposta pedida e não entregue |
| Último contato | há 12 dias, call de 20 minutos por telefone |

## Quem você vai encontrar

### [dono] · proprietário
- **Trajetória:** desconhecida `[A CONFIRMAR]`
- **Papel na decisão:** decide e paga
- **Última interação:** contou das duas quebras do mês passado, pediu proposta
- **Ponto de conversa:** ele mencionou que a segunda quebra foi num sábado de manhã, o dia de maior
  movimento. Retomar por esse fato, não por elogio à rede.

### [gerente de operações] · gerente de operações
- **Trajetória:** desconhecida `[A CONFIRMAR]`
- **Papel na decisão:** provavelmente avalia, e é quem vive o problema no dia a dia. Pode ser a maior
  aliada ou a maior resistência, porque hoje é ela quem chama o técnico avulso.
- **Última interação:** nenhuma, primeira conversa
- **Ponto de conversa:** perguntar como ela resolve hoje quando uma máquina para, e escutar até o fim.
  A resposta dela é a fonte do número que sustenta a proposta.

## O que já aconteceu

- **Conversado:** duas máquinas quebraram no mesmo mês, uma delas num sábado de manhã.
- **Combinado, e por quem:** o dono mandaria a proposta. Não mandou.
- **Em aberto ou preocupando:** eles têm um técnico avulso que atende quando quebra, e vão comparar o
  preço da manutenção mensal com o custo desse técnico.

## O que mudou por lá

- Duas quebras em 30 dias · **por que importa nesta call:** é o que abriu a conversa, e a memória
  disso é o que sustenta o valor. Vai esfriando a cada semana que passa.
- `[A CONFIRMAR]` nada mais foi confirmado, sem pesquisa externa nesta sessão.

## O roteiro (30 minutos)

1. **Abertura (3 min)** · retomar o sábado de manhã: "você comentou que a segunda parada foi num
   sábado. Quanto tempo a máquina ficou fora naquele dia?"
2. **O custo real da parada (8 min)** · perguntar pra gerente como funciona hoje e chegar a um número:
   quantas paradas por ano, quanto tempo cada uma, quanto se deixa de vender.
3. **A proposta, valor antes de preço (10 min)** · o plano de visita mensal, o que ele previne, o
   tempo de resposta quando quebra mesmo assim. O preço só depois do número da etapa anterior.
4. **Preocupações (5 min)** · abrir espaço: "o que ainda não fecha pra vocês?"
5. **Próximo passo (4 min)** · propor início no dia 1 do mês seguinte, contrato de 3 meses,
   confirmação por escrito até sexta. Responsável: o dono da rede confirma, e eu mando o contrato.

## As perguntas

1. Quantas paradas de máquina vocês tiveram nos últimos 12 meses? · *por que:* é o número que
   sustenta a proposta inteira, e ninguém nunca contou.
2. Quando uma máquina para no sábado, o que acontece na prática? · *por que:* a resposta da gerente
   é o custo real, e ela é quem vive isso.
3. Quanto tempo leva pro técnico chegar hoje, e quanto ele cobra por chamado? · *por que:* é a
   comparação que eles já vão fazer; melhor ser eu a colocar o número na mesa.
4. Vocês já perderam venda por causa de uma máquina parada? Quanto, mais ou menos? · *por que:*
   transforma o problema técnico em dinheiro.
5. Além de vocês dois, mais alguém precisa aprovar isso? · *por que:* não foi confirmado, e é o que
   mais atrasa fechamento.
6. Existe alguma data em que isso precisa estar resolvido? · *por que:* revela se existe urgência
   real ou se a conversa pode esfriar por três meses.

## As objeções prováveis

| A pessoa diz | O que ela quer dizer | A resposta | A prova |
|---|---|---|---|
| "sai mais barato chamar o técnico quando quebra" | não vi o retorno, comparei com uma coisa que resolve outro problema | "Vamos somar: [N] chamados por ano vezes [valor] do chamado, mais as horas de máquina parada no sábado. O plano custa [valor] e inclui a visita e o atendimento urgente." | `[A CONFIRMAR: prova]` o dono precisa me passar o caso da outra rede antes da call |
| "está caro" | o valor mensal parece grande sem o número anual do lado | "Por unidade dá [valor] por mês. Uma parada de sábado sozinha custa mais que isso." | o número que sair da pergunta 4, dito por eles mesmos |
| "deixa eu pensar" | falta informação, ou falta alguém | "Faz sentido. Só pra eu mandar a coisa certa: falta uma informação, ou falta alguém olhar junto?" | não precisa de prova, precisa da pergunta |
| "vamos começar com duas lojas" | quer testar antes de assumir a rede | aceitar, com condição: 3 meses nas duas lojas de maior movimento, e revisão com número na mesa no fim | o próprio piloto vira a prova para as outras 7 |

## Notas internas

A gerente de operações é a pessoa que hoje chama o técnico avulso. O plano mensal muda a rotina dela,
e pode soar como crítica ao jeito que ela resolve. Perguntar antes de propor, e nunca comparar o
serviço com o técnico dela na frente dos dois.

O dono já pediu a proposta há 12 dias e ela não foi entregue. Se ele mencionar isso, assumir em uma
frase, sem desculpa longa, e seguir.

## Pra anotar durante

- [ ] número de paradas nos últimos 12 meses
- [ ] custo do chamado avulso
- [ ] quem mais aprova
- [ ] data de início acordada
```

---

## O que o gate reprovou no caminho (e por quê)

| Seção | O que estava escrito | Por que reprovou | Como ficou |
|---|---|---|---|
| Objetivo | "avançar a negociação e apresentar a proposta" | sem resultado observável | virou "sair com a data de início acordada, ou com a objeção real nomeada" |
| Retrato | "rede consolidada com forte presença no bairro" | ponto de conversa genérico | virou o fato do sábado de manhã, que o dono realmente disse |
| Retrato | "empresa com 9 unidades e faturamento de 400 mil" | dado sem fonte, nada foi pesquisado | virou `[A CONFIRMAR]` e depois pergunta na call |
| Roteiro | fechava com "mandar a proposta por e-mail depois" | próximo passo sem data e sem responsável | virou início no dia 1, confirmação até sexta, responsável nomeado |
| Objeções | a primeira resposta citava um caso de outra rede sem autorização | prova não confirmada | virou `[A CONFIRMAR: prova]` com a tarefa de conferir antes da call |
| Dossiê inteiro | tinha 4 telas com histórico do setor de panificação | passa do tamanho, não seria lido | cortado pra uma tela e meia, só o que serve ao objetivo |
