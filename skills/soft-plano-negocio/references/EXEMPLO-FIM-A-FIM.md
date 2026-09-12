# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: este exemplo é ILUSTRATIVO (nicho fictício).** Nome, números, taxas e resultados foram
> inventados só pra mostrar a FORMA de cada saída. É PROIBIDO parafrasear ou reusar as frases dele
> na peça real. A peça real nasce 100% do insumo do dono; se você se pegar copiando uma frase deste
> exemplo, pare e volte ao insumo. Num trabalho real, todo número sem fonte nasce marcado
> `[A CONFIRMAR]` e o dono confirma antes de sair.

**O caso fictício:** um consultor de eficiência energética que atende padarias e pequenos mercados.
Dono fictício: 5 anos de atuação, atende presencial na própria cidade, vende diagnóstico avulso.

Este arquivo mostra a saída resumida das 5 ações, na ordem. Cada saída real é maior; aqui está o
suficiente pra reconhecer o formato antes de começar.

---

## O que ele deu de entrada

> "Quero um plano. Faturo uns 12 mil por mês, quero chegar em 40 mil líquido em 6 meses. Não sei se
> é realista e não sei por onde começar."

**A skill respondeu, antes de qualquer conta:** "são 5 perguntas obrigatórias e no máximo mais 4,
dependendo do caso. Vou uma por vez."

---

## Ação 1 · DIAGNÓSTICO

**As 5 perguntas e as respostas fictícias:**

1. Faturamento médio dos últimos 3 meses: *"11.800. Somei e dividi."*
2. Mix de oferta e ticket: *"Diagnóstico energético avulso, R$1.900. Vendo 6 por mês. Mais nada."*
3. Meta de caixa em 6 meses: *"40 mil líquido."*
4. Horas reais por semana: *"30. Tenho outro trabalho meio período."*
5. Investimento mensal em tráfego: *"Zero. Tudo indicação."*

**A primeira coisa que a skill fez foi devolver o número, não aceitar a meta.**

**Saída real:** `01-diagnostico.md`. Resumo:

| Campo | Valor |
|---|---|
| Faturamento médio | R$11.800 por mês |
| Mix | 1 oferta, ticket R$1.900, 6 vendas por mês |
| Meta de caixa declarada | R$40.000 líquido no mês 6 |
| Horas disponíveis | 30 por semana |
| Tráfego | R$0 |
| **Estágio** | **Desemperrar** (faixa de R$5k a R$15k) |
| **Teto realista no mês 6** | **3x a 5x, ou seja de R$35k a R$59k de faturamento** |

**A leitura, dita em uma linha:** a meta de R$40k **líquido** exige faturamento perto de R$57k, que
está no topo do teto do estágio. Possível, e só no cenário agressivo. O plano vai mostrar isso em
vez de prometer.

**Fronteira declarada:** ele tem nicho definido e oferta única, mas nenhum mecanismo nomeado. A skill
avisou em uma linha que a `soft-plano-posicionamento` deixaria o ticket mais defensável, e seguiu.

---

## Ação 2 · A CONTA

**A pergunta condicional que apareceu aqui:** quantas horas cada cliente consome do começo ao fim,
contando deslocamento? Resposta: *"umas 9 horas. Duas visitas, o relatório e a reunião de entrega."*

**Saída real:** `02-a-conta.md`. A conta rodada:

```
Meta de caixa R$40.000 ÷ ticket R$1.900   = 21 clientes por mês
21 clientes × 9 horas                      = 189 horas por mês  = ~47 h/semana
+ produção de conteúdo                     = ~4 h/semana
+ venda, follow-up e administração         = ~6 h/semana
+ aprendizado                              = ~2 h/semana
                                           = 59 horas por semana exigidas
Disponível declarado                       = 30 horas por semana
```

**VEREDITO: não cabe.** Falta quase o dobro da semana dele.

**Os 4 ajustes mostrados, na ordem, e o que o dono escolheu:**

1. **Subir o ticket** (preferido). Com ticket de R$5.900, são 7 clientes por mês, 63 horas por mês de
   entrega, e a semana fecha em ~28 horas. **Escolhido.**
2. Refazer a esteira: concentrar em um acompanhamento de 3 meses em vez do diagnóstico avulso.
3. Baixar a meta: R$22k em 6 meses, R$40k em 12.
4. Subir as horas: recusado de saída, ele trabalha meio período em outro lugar.

**A pergunta que a skill fez antes de seguir:** *"olhando essas 59 horas e essa meta, você ainda quer
isso?"* Resposta: *"quero, mas com ticket maior. Não vou virar escravo de padaria."*

**O que ficou registrado no doc:** o ajuste escolhido foi ticket, e o desenho do produto de R$5.900
não é desta skill, é da `soft-plano-ofertas`. A rota foi declarada.

**Nenhum ajuste proposto mexeu no outro trabalho dele nem na família.**

---

## Ação 3 · PROJEÇÃO

**A pergunta condicional que apareceu:** que canal de venda você usa hoje? Resposta: *"indicação e
visita porta a porta. Nunca vendi pela internet."*

Sem histórico de canal digital, a skill usou a **faixa baixa** do Benchmark e declarou a premissa.

**Saída real:** `03-projecao.md`. Os 3 cenários, com ticket já ajustado pra R$5.900:

| Cenário | Premissa escrita | Faturamento no mês 6 | Anual projetado |
|---|---|---|---|
| **Conservador** | ~60% de execução, zero tráfego pago, só indicação, faixa baixa do benchmark | R$23.600 (4 vendas) | ~R$212.000 |
| **Realista** | ~80% de execução, conteúdo semanal rodando a partir do mês 2, 2 indicações por mês continuando | R$41.300 (7 vendas) | ~R$355.000 |
| **Agressivo** | execução plena, R$1.500 por mês em tráfego a partir do mês 3, 1 contrato grande por trimestre | R$59.000 (10 vendas) | ~R$490.000 |

**A curva mês a mês do realista:** M1 R$11.800 · M2 R$17.700 · M3 R$23.600 · M4 R$29.500 · M5
R$35.400 · M6 R$41.300.

**A régua de realismo aplicada, e o que ela cortou:** a primeira rodada do agressivo deu R$88.500
(15 vendas por mês). Estourou o teto de 5x do estágio Desemperrar e a capacidade de entrega dele
(15 clientes × 9 horas passa de 30 horas por semana de novo). Cortado em 33% pra R$59.000, com a
premissa reescrita. O corte está registrado no doc.

**Um número intermediário que acendeu alerta e foi resolvido:** o conservador pedia 340 pessoas
alcançadas por mês pra 4 vendas, o que é plausível pra indicação local. Passou sem correção.

**A meta oficial do roadmap:** o realista, R$41.300 no mês 6. Costura com A Conta ajustada.

---

## Ação 4 · SCORE DE NICHO

**Rodou?** Sim, e por gatilho objetivo, não por sensação: **na Ação 1 ele nomeou dois candidatos**
("padaria e pequeno mercado, e às vezes me chamam de posto de gasolina"). Isso é o gatilho 1.

**Saída real:** `04-score-de-nicho.md`.

| Critério | Padaria e mercado | Posto de gasolina |
|---|---|---|
| Dor latente | 7 (conta de luz dói, mas convivem com ela) | 9 (a conta é o segundo maior custo deles) |
| Disposição a pagar | 6 (margem apertada) | 9 (já contratam consultoria técnica) |
| Recorrência | 7 (revisão anual) | 8 (auditoria periódica é norma) |
| **Conexão pessoal** | **9** (5 anos, 40 clientes, ele conhece o chão) | **2** (nunca atendeu um de verdade) |
| Tamanho e concorrência | 8 (muitos, pouca concorrência local) | 5 (poucos, e já atendidos por rede grande) |
| **Total** | **37 (bom)** | **33 (bom)** |

**A recomendação, com o freio aplicado:** posto de gasolina pontuou perto, e **reprovou no freio do
critério 4**. Conexão 2 não vira posicionamento, vira ficção. Fica fora.

**O afunilamento sugerido pra sair de "bom" e chegar em "ouro":** sair de "padaria e mercado" pra
**padaria com forno elétrico e câmara fria**, onde a dor é mais aguda e a disposição a pagar sobe,
porque o desperdício é mensurável e visível na conta.

---

## Ação 5 · ROADMAP

**Saída real:** `05-roadmap-90-dias.md`.

### Mês 1 · Montar e vender

- **Objetivo:** vender 2 acompanhamentos de R$5.900 pra base de indicação que já existe.
- **Semana 1:** listar os 40 clientes antigos e classificar por conta de luz.
- **Semana 2:** desenhar o acompanhamento de 3 meses (rota declarada: `soft-plano-ofertas`).
- **Semana 3:** falar com os 12 melhores da lista, um por dia.
- **Semana 4:** fechar os 2 primeiros e documentar o antes com número.
- **Métrica:** conversas iniciadas por semana. **Checkpoint:** 2 vendas fechadas até o dia 30.

### Mês 2 · Validar e repetir

- **Objetivo:** repetir a venda com os primeiros resultados na mão, e ligar o conteúdo semanal.
- **Semana 5 e 6:** entregar os 2 primeiros e colher número de economia real.
- **Semana 7:** 1 peça por semana mostrando o número colhido, com autorização por escrito.
- **Semana 8:** mais 3 conversas com a base, agora com prova.
- **Métrica:** economia média por cliente. **Checkpoint:** 4 vendas acumuladas e 1 caso documentado.

### Mês 3 · Escalar e subir ticket

- **Objetivo:** chegar a 7 vendas por mês e testar o afunilamento pra padaria com forno e câmara.
- **Semana 9 e 10:** ligar R$1.500 por mês de tráfego local, se o caixa do mês 2 permitir.
- **Semana 11:** revisar o ticket com o caso documentado na mão.
- **Semana 12:** checkpoint de 90 dias e recalibragem da projeção.
- **Métrica:** vendas por mês. **Checkpoint:** 7 vendas no mês, ou a projeção volta pra mesa.

### Os 3 próximos passos, datados, pra ESSA semana

1. **Até quarta:** exportar a lista dos 40 clientes antigos e marcar quem tem forno elétrico.
2. **Até sexta:** escrever a primeira versão do acompanhamento de 3 meses (o que entra, quanto dura).
3. **Até domingo:** mandar mensagem pros 5 primeiros da lista, um texto só, sem preço.

Nenhum passo é "estudar mais" ou "pensar melhor".

---

## A tabela do gate, preenchida (o artefato visível obrigatório)

| Check | ✓/✗ | Evidência |
|---|---|---|
| Número real, não inventado | ✓ | os 5 números vieram dele; nada preenchido com média de mercado |
| 3 cenários com premissa | ✓ | conservador, realista e agressivo, cada um com a premissa escrita |
| Régua de realismo aplicada | ✓ | agressivo cortado de R$88.500 pra R$59.000 (33%), premissa reescrita |
| A Conta fecha (ou tem ajuste) | ✓ | não fechou (59h contra 30h); ajuste 1 escolhido, ticket de R$1.900 pra R$5.900 |
| Nicho com conexão | ✓ | posto de gasolina descartado pelo freio do critério 4 (conexão 2) |
| Roadmap fecha com próximos passos | ✓ | 3 ações datadas pra essa semana, todas com verbo e objeto |
| Marca-neutra | ✓ | zero número de terceiro, zero inventado como prova |
| Contrato de formato | ✓ | doc `.md` em mapa-mental, tabela e número acima de prosa |
| Anti-IA (HARD), com prova | ✓ | travessão longo U+2014: 0 · verbo-freio banido e flexões: 0 |
| **VEREDITO** | **PASSA** | libera o plano |

---

## O caso alternativo: quando o dono se recusa a dar número

Vale registrar a outra saída, porque ela acontece. Se ele responde *"não sei, dá uma estimativa aí"*,
o plano **não sai**. O que sai é isto, em 5 linhas:

> Sem os números o plano vira chute com casa decimal, então prefiro não entregar isso. Faltam três:
> o faturamento médio dos 3 últimos meses, o ticket do que você vende hoje, e as horas reais que você
> tem por semana. Sem o faturamento eu não sei seu estágio nem seu teto. Sem o ticket eu não faço A
> Conta. Sem as horas eu não sei se a meta cabe na sua vida. Junta esses três e a gente fecha o plano
> na mesma conversa.

Se ele der só os três primeiros e não os cinco, sai um **plano parcial**: diagnóstico, A Conta e
roadmap, sem a projeção em 3 cenários, com o doc declarando no topo que é parcial e o que falta.
