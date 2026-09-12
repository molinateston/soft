# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, números, prazos e resultados foram inventados só pra mostrar
> a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega de
> verdade. Num trabalho real, todo número e toda prova sem fonte nascem marcados
> `[A CONFIRMAR: o quê]` e o dono confirma antes de sair.

**O caso fictício:** consultoria de precificação pra pequenas marcas de roupa que vendem por
encomenda. O dono fictício atende costureiras e ateliês que faturam de 4 a 20 mil por mês. O produto
é um programa de 6 semanas de `[fictício]` 2.900 reais. Estágio de consciência do avatar: médio (sabe
que ganha pouco, culpa o cliente que pechincha).

Este arquivo mostra a saída resumida de cada ação, na ordem. A saída real é maior; aqui está só o
suficiente pra você reconhecer o formato antes de começar.

---

## O que o dono deu de entrada

> "Quero uma isca pra pegar contato no Instagram. Não sei o que fazer. Já pensei em um ebook sobre
> precificação, mas todo mundo faz isso."

**Estado de entrada declarado:** tem nicho e produto, tem prova, não tem fala literal minerada, não
tem isca decidida. Então a skill entrou pela Ação 0 e depois pela Ação 1.

---

## Ação 0 · ANCORAGEM

A skill pediu a fonte de fala. O dono colou 40 mensagens de clientes e prints de comentários. O que
saiu:

**DOR (com o N):**
- "eu cobro e a pessoa acha caro, aí eu abaixo" (N=9)
- "no fim do mês parece que eu trabalhei de graça" (N=6)
- "não sei quanto custa a minha hora" (N=5)

**DESEJO:**
- "queria falar o preço sem tremer" (N=4)
- "queria saber se eu estou tendo lucro de verdade" (N=7)

**Prova real do dono:** um ateliê de 2 costureiras subiu a margem de 12% pra 31% em 5 semanas sem
perder cliente. `[fictício]`

**Mecanismo nomeado:** "Preço de Dentro pra Fora", começar pelo custo real da hora e só depois olhar
o que o mercado cobra.

---

## Ação 1 · IDEAÇÃO

As 3 perguntas de ordem de retorno, uma por vez:

1. **O que você vende?** → programa de 6 semanas, 2.900. `[fictício]`
2. **O que o avatar precisa acreditar pra querer isso?** → que o problema não é o cliente que pechincha, é que ela não sabe o custo real da própria hora.
3. **Brainstorm** a partir das falas acima.

Saída real: `ideias-de-isca.md`. As 5 candidatas:

| Candidata | Dor de top 3 | Ganho rápido | Formato | Destino | Nota |
|---|---|---|---|---|---|
| Calculadora do Custo da Sua Hora | "não sei quanto custa a minha hora" | número na tela em 4 min | calculadora | conversa | 9 |
| Checklist dos 9 custos que somem da peça | "trabalhei de graça" | lista conferida em 10 min | checklist | conversa | 8 |
| Quiz: o seu preço é dor de cabeça ou lucro? | "acha caro, aí eu abaixo" | diagnóstico em 3 min | quiz | conversa | 8 |
| Guia completo de precificação pra ateliê | todas, difusas | nenhum, é leitura | guia longo | conversa | 4 |
| Planilha de custo por peça | "trabalhei de graça" | preenchimento em 25 min | planilha | conversa | 6 |

**Recomendação com convicção:** a **Calculadora do Custo da Sua Hora**.

> Ela ataca a dor que aparece em quase todas as conversas, entrega um número na tela em menos de 5
> minutos, e o número que sai é justamente a evidência que faz a crença-ponte virar. A pessoa vê que
> a hora dela custa mais do que ela cobra e o problema deixa de ser o cliente pechincha. A segunda
> opção seria o quiz, que segmenta bem, mas ele diagnostica sem entregar o número, então convence
> menos.
>
> O guia longo é o que você já pensou e é o que eu tiraria da mesa. Ele é o formato que todo mundo do
> nicho faz, não entrega ganho em menos de 20 minutos, e é o que menos filtra.

**STOP.** O dono escolheu a calculadora.

---

## Ação 2 · FORMATO

A linha declarada:

> Formato: calculadora (família B, interativo e diagnóstico). Promessa: "descubra em 4 minutos quanto
> custa a sua hora de verdade, e quanto você está deixando na mesa em cada peça". Destino: conversa de
> 30 minutos. Porque o avatar está no estágio médio de consciência, e o interativo converte e segmenta
> no mesmo movimento.

**STOP pro OK.** O dono aprovou.

---

## Ação 3 · PRODUÇÃO

Saída real: `arquitetura-calculadora-custo-da-hora.md`, porque o formato é interativo e o que se
entrega é a arquitetura, não um PDF. Resumo:

### As perguntas (6, na ordem)

| # | Pergunta | Campo | Por que ela existe |
|---|---|---|---|
| 1 | Quantas horas por semana você trabalha de verdade, contando acabamento e ida à loja de aviamento? | número | a maioria subestima, e é aqui que a conta vira |
| 2 | Quanto você quer tirar por mês pra você? | número | separa retirada de faturamento |
| 3 | Quanto você paga de aluguel, luz, internet e ferramenta por mês? | número | custo fixo, que quase ninguém rateia |
| 4 | Quantas peças você entrega por mês, em média? | número | denominador |
| 5 | Quanto você cobra hoje pela peça mais comum? | número | é o que vira o contraste do resultado |
| 6 | Quanto tempo leva pra fazer essa peça, do corte à entrega? | número | fecha a conta por peça |

### A lógica de resultado (3 ramos)

| Ramo | Condição | O que a tela mostra |
|---|---|---|
| **No vermelho** | preço cobrado abaixo do custo real por peça | o valor exato que ela perde por peça e por mês, com a frase "cada peça que você entrega custa X reais do seu bolso" |
| **No zero** | preço entre o custo real e o custo mais 20% | "você está trabalhando, mas não está lucrando. A margem que sobra não paga uma máquina nova nem uma semana de folga" |
| **Com margem** | acima do custo mais 20% | "a sua conta fecha. O que segura o crescimento aqui é outra coisa, e a gente pode olhar isso na conversa" |

### A copy de um resultado por inteiro (ramo "no vermelho")

> **O seu custo por hora é R$ 34. Você cobra o equivalente a R$ 19.**
>
> Cada peça que você entrega tira R$ 71 do seu bolso. Em 22 peças por mês, isso dá R$ 1.562.
>
> Não é que o seu cliente pechincha. É que o preço nasceu de fora pra dentro: você olhou o que a
> concorrente cobra e chegou nele por aproximação. O custo da sua hora nunca entrou na conta, então
> não tem preço que feche.
>
> O caminho é o inverso. Começa pelo custo real da sua hora, monta o preço a partir dele, e só no fim
> olha o mercado, pra saber quanto do valor você ainda não está comunicando. É o **Preço de Dentro pra
> Fora**.
>
> A calculadora te deu o número. O que fazer com ele em cada peça, e como falar esse preço sem
> tremer, é o que eu faço com as pessoas na conversa.

**Por que passou no gate:** entrega valor real (o número sai na tela e dá pra usar hoje), aponta pro
método sem entregar o como completo, ancora na fala literal *"eu cobro e a pessoa acha caro, aí eu
abaixo"* (N=9) reescrita em cena, e o título diz o benefício sem precisar abrir.

### A tabela de roteamento

| Resultado | Destino | Marcação |
|---|---|---|
| No vermelho | conversa, prioridade | tag `vermelho`, entra na régua com o convite em D+2 |
| No zero | conversa | tag `zero`, régua padrão de 6 toques |
| Com margem | conversa, mas com outra abertura | tag `margem`, a régua fala de crescimento, não de preço |

---

## Ação 4 · CAPTURA E DESTINO

Saída real: `captura-e-destino.md`.

- **A troca:** o contato entra **antes de revelar o resultado**, não antes das perguntas. A pessoa responde as 6, vê "calculando", e aí o campo aparece. Fricção baixa porque ela já quer o número.
- **Campos:** nome e WhatsApp. Só. E-mail foi cortado porque o dono só usa WhatsApp de verdade.
- **Promessa da troca:** "seu resultado completo, com o número por peça e por mês".
- **Destino:** conversa de 30 minutos. `[A CONFIRMAR: link da agenda]`
- **A ponte até o destino:** a régua fica na soft-funil-nutricao. Como ela não estava instalada nesta sessão fictícia, a skill escreveu a régua mínima de 3 toques aqui: D+0 entrega o resultado com a instrução de por onde começar · D+2 a crença com a prova do ateliê colada · D+4 o convite com o link.

**STOP pro OK.**

---

## Ação 5 · PONTE DO FEED

O dono pediu. Saída real: `ponte-feed.md`.

- **Palavra-chave:** HORA
- **Disparo:** "Aqui está a calculadora: [link]. São 6 perguntas, leva 4 minutos, e no fim aparece quanto custa a sua hora de verdade."
- **Acompanhamento (36h):** "Conseguiu ver o seu número? Me responde só se deu vermelho, zero ou margem, que eu te digo o que fazer com ele."

---

## O que o gate reprovou pelo caminho

| Peça que caiu | Check que reprovou | O que foi feito |
|---|---|---|
| Primeira versão do título, "Calculadora de Precificação" | Valor óbvio no título | virou "Calculadora do Custo da Sua Hora", que diz o benefício sozinho |
| O guia longo, na ideação | Top 3 + filtra o avatar certo | ficou com nota 4 e saiu da recomendação |
| Primeira versão do resultado "no vermelho", que trazia os 5 passos do método | Aponta pro método | os passos saíram. Ficaram o quê e o porquê; o como voltou pro produto |
| Formulário com nome, e-mail, WhatsApp, faturamento e cidade | Captura com fricção mínima | ficaram nome e WhatsApp |
| Frase "essa calculadora vai transformar o seu negócio" | Anti-IA (verbo-clichê de hype) | cortada. O resultado fala por número, não por adjetivo |
| Prova escrita como "vários ateliês melhoraram" | Ancorada | trocada pelo caso com número e prazo, marcado `[A CONFIRMAR: prova]` |
