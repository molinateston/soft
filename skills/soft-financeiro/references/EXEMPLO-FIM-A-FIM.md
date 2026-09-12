# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nomes, valores, datas de contrato e situações foram inventados só
> pra mostrar a FORMA de cada saída. Nada disso é caso real, nada disso é orientação a ninguém. As
> leis citadas são reais e vêm do mapa de `02-bases-legais.md`, conferido em jun/2026; o resto é
> ilustração. Num trabalho real, número sem confirmação nasce `[A CONFIRMAR]` e regra sem fonte
> conferida é `NÃO VERIFICADO`.

**Os casos fictícios:** três pedidos que entram pela mesma porta e saem por caminhos diferentes. Um
de empresa, um pessoal, e um que a skill se recusou a atender.

---

## Caso A · Ação 1, EMPRESA (preço e margem)

### O que o dono deu

> "Cobro 180 reais na diária de organização de arquivo, faço umas 14 por mês e não sobra nada.
> Quanto eu devia cobrar?"

### A árvore percorrida, em voz alta

```
1. Há ação judicial, penhora, bloqueio ou risco patrimonial?
   Não foi mencionado nada disso. A skill perguntou mesmo assim, uma linha:
   "Antes de calcular: tem alguma cobrança na justiça, penhora ou conta bloqueada?"
   Resposta: "não, nada disso". → segue.

2. Empresa ou pessoa?
   Ele fatura, cobra cliente e emite nota. → EMPRESA, bloco Preço.
```

### A entrevista curta, uma pergunta por vez

Faltavam quatro dos cinco insumos, então a skill perguntou. Uma por vez, e parou quando deu pra
calcular:

> **1.** Quanto entrou de dinheiro no último mês fechado?
> *"2.520, foram 14 diárias."*
>
> **2.** Quais custos você paga mesmo se não vender nada no mês, e quanto somam?
> *"Aluguel de uma salinha 600, contador 180, telefone 90, e o Simples eu pago em cima do que
> faturo. Uns 870 fixos."*
>
> **3.** Quanto custa entregar uma diária?
> *"Transporte uns 25, e às vezes compro caixa e etiqueta, uns 15. Digamos 40."*
>
> **4.** Quanto você quer tirar por mês, pra você?
> *"Uns 3.000 seria bom."*

A quinta pergunta (caixa disponível) não foi feita: não é preço, é a frente de crise, e o pedido não
era esse. Perguntar o que não muda a resposta é atrito.

### A conta, com o que ficou marcado

```
PREÇO · organização de arquivo, diária · base: mês fechado informado pelo dono

  Receita atual:        14 × 180 = 2.520
  Custo variável:       14 ×  40 =   560
  Margem de contribuição:           1.960  (78% do preço)
  Custo fixo:                         870
  Sobra hoje:                       1.090  ← é isso que "não sobra nada" significa

  Ponto de equilíbrio, preço atual:
    870 ÷ (180 - 40) = 6,2 → 7 diárias só pra pagar a estrutura

  Preço necessário pra retirada de 3.000, mantendo 14 diárias:
    (870 + 3.000) ÷ 14 + 40 = 316,43  →  preço de 320

  Se o volume cair pra 10 diárias no preço novo:
    10 × (320 - 40) = 2.800 - 870 = 1.930 de sobra  (ainda quase o dobro de hoje)

  Alíquota do Simples: [A CONFIRMAR com seu contador]. Não incluí no cálculo porque
  a faixa e o anexo mudam o número, e chutar isso desloca o preço inteiro.
```

Leitura entregue em três linhas, sem enrolação: o preço atual paga a estrutura e sobra pouco para o
dono; 320 é o preço que sustenta a retirada; e mesmo perdendo 4 clientes no preço novo ele fica
melhor do que hoje.

### A tabela do gate, preenchida

| Check | Passa se (✓) | ✓/✗ |
|---|---|---|
| **Escalada checada** | perguntei sobre ação, penhora e bloqueio. Nada. Nenhum sinal disparou | ✓ |
| **Fonte datada** | não citei nenhuma regra regulada. A alíquota do Simples ficou `[A CONFIRMAR com seu contador]`, que é o profissional da matéria | ✓ |
| **Sem parecer** | não disse "seu regime é o Simples anexo III" nem "você paga imposto demais". Isso é do contador | ✓ |
| **Sem promessa** | não disse que ele vai ganhar mais. Mostrei a conta nos dois cenários de volume | ✓ |
| **Ressalva nas reguladas** | não se aplica, não houve regra regulada citada | n/a |
| **Gate regulado** | a peça não vai ao público, é uso interno dele | n/a |
| **Disclaimer fixo** | está no fim do arquivo | ✓ |
| **Anti-IA (HARD)** | busca feita: 0 travessão longo, 0 ocorrência da família do verbo-freio banida | ✓ |
| **VEREDITO** | o pior item é ✓ | **LIBERA** |

**Entrega:** `preco-organizacao-arquivo.md`, com a conta, os dois cenários, o `[A CONFIRMAR]` da
alíquota, a tabela acima e o disclaimer. E **STOP**: a skill perguntou se serve, antes de oferecer o
fluxo de caixa. Não empilhou peça.

---

## Caso B · Ação 2, PESSOAL (defesa de dívida)

### O que a pessoa deu

> "Meu cartão virou uma bola de neve. Peguei 4 mil de rotativo e hoje eles cobram 11 mil. Isso pode?
> Eu quero mandar uma reclamação."

### A árvore percorrida

```
1. Há ação judicial, penhora, bloqueio ou risco patrimonial?
   A skill perguntou explicitamente, porque nesta frente é a pergunta que muda tudo:
   "Você chegou a ser citado em algum processo, teve conta bloqueada, penhora, ou
    recebeu carta de oficial de justiça?"
   Resposta: "não, é só telefone e mensagem toda semana". → segue.

2. Empresa ou pessoa? → PESSOA, bloco Defesa.
```

### A entrevista curta, e a pergunta que decide a resposta inteira

> **1.** Quanto entra por mês, líquido? *"3.200 fixos."*
>
> **2.** Quanto sai no que não dá pra cortar? *"Aluguel 1.100, mercado 800, transporte 300, remédio
> da minha mãe 250. Uns 2.450."*
>
> **3.** Quais dívidas existem hoje? *"Só essa do cartão. E a fatura mínima que eu pago todo mês."*
>
> **4.** **Quando essa dívida foi contratada, e quanto era o valor original?**
> *"Não lembro direito, acho que 2022."*

Essa quarta pergunta é a que decide. O teto de 100% da Lei 14.690/2023 vale só para operações
**contratadas a partir de 03/01/2024**. Um "acho que 2022" não é uma data, então:

> Preciso da data exata da contratação pra saber se uma regra específica se aplica ao seu caso. Ela
> está na sua fatura ou no contrato do cartão. Sem ela, eu te explico a regra em tese, mas não digo
> que ela vale pra você, porque pode não valer.

E a marcação entrou no documento como `[A CONFIRMAR: data da contratação da operação]`.

### O diagnóstico, primeira peça

```
DIAGNÓSTICO DA DÍVIDA

  Tipo:                    rotativo de cartão de crédito
  Valor original:          4.000  [A CONFIRMAR na fatura]
  Cobrado hoje:           11.000
  Data da operação:        [A CONFIRMAR: decide se o teto de 100% se aplica]
  Renda líquida:           3.200
  Gasto essencial:         2.450
  Sobra mensal:              750   ← 23% da renda

  Sinal de superendividamento: presente em tese. A dívida de 11.000 contra uma sobra
  de 750/mês não se paga sem comprometer o essencial. Isso NÃO é um diagnóstico
  jurídico, é uma leitura de números que indica qual caminho procurar.

  Ação judicial, penhora ou bloqueio: nenhum informado. A via administrativa está
  aberta, e é por ela que a gente começa.
```

**STOP.** A skill mostrou isso, perguntou se os números estavam certos, e só depois foi ao mapa de
direitos.

### O mapa de direitos, segunda peça (o formato do Passo 1)

Um item, pra mostrar a forma:

> **Teto de 100% sobre encargos do rotativo**
>
> **O que a regra diz:** o total de juros e encargos do rotativo e do parcelamento da fatura não pode
> ultrapassar o valor original da dívida. Ela pode, no máximo, dobrar.
>
> **Fonte e data:** Lei 14.690/2023, regulamentada pela Resolução CMN 5.112/2023. Aplicável a
> operações **contratadas a partir de 03/01/2024**. Mapa conferido em jun/2026.
>
> **Veredito:** VERIFICADO COM RESSALVA.
>
> **Como isso se aplica a você:** ainda não sei, e não vou afirmar. Se a sua operação for de 2022,
> como você acha, **essa regra não alcança ela**, e a dívida segue a taxa de mercado do contrato. Por
> isso a data importa tanto. `[A CONFIRMAR: data da contratação]`
>
> **O que NÃO afirmar:** que a regra é retroativa. Ela não é, e essa é a confusão mais repetida no
> assunto. Também não se presume que juros são abusivos só por serem altos: isso depende de análise
> de contrato, que é trabalho de advogado.

Mais três itens saíram no mesmo formato (prazo de negativação de 5 anos contado do vencimento, com a
ressalva de que "10 dias antes" não é prazo legal; devolução em dobro do art. 42 do CDC com a
modulação de 30/03/2021; e o que cada canal oficial de fato resolve).

### A carta, terceira peça, e ela é ARQUIVO

A carta saiu como `carta-reclamacao-consumidor-gov-2026-08-19.md`, não como texto no chat. O motivo
está escrito na entrega:

> Salvei em arquivo porque você vai colar isso num formulário oficial e vai precisar guardar
> exatamente o que enviou, com a data. Reclamação que só existiu no chat some, e daqui a 40 dias você
> não vai lembrar o que escreveu.

Trecho da carta, pra mostrar o tom:

> Contratei operação de crédito rotativo junto à instituição, com valor original de R$ 4.000,00. O
> valor atualmente cobrado é de R$ 11.000,00. Solicito o extrato detalhado da evolução do débito, com
> a discriminação de encargos, juros e tarifas aplicados mês a mês, bem como a data de contratação da
> operação. Solicito ainda proposta de renegociação compatível com minha capacidade de pagamento.

Repare no que a carta **não** diz: não diz que a cobrança é ilegal, não cita a lei como se ela
valesse ali, não exige valor nenhum, não promete processo. Ela pede documento e proposta. É isso que
a via administrativa faz bem.

### A tabela do gate desta peça, preenchida, e a versão que REPROVOU antes

Primeira versão, reprovada:

| Check | O que aconteceu | ✓/✗ |
|---|---|---|
| **Sem parecer** | a carta dizia "essa cobrança é abusiva e viola o CDC" | ✗ |
| **Ressalva nas reguladas** | citava o teto de 100% como se valesse, sem a data de corte, num caso cuja data é desconhecida | ✗ |
| **VEREDITO** | o pior item é ✗ | **REFAZ** |

Depois da correção:

| Check | Passa se (✓) | ✓/✗ |
|---|---|---|
| **Escalada checada** | perguntei sobre ação, penhora e bloqueio. Nada. Superendividamento em tese está anotado como caminho a considerar, não como diagnóstico | ✓ |
| **Fonte datada** | as 3 regras citadas no mapa saem com lei, artigo, fonte e vigência. Mapa conferido em jun/2026 | ✓ |
| **Sem parecer** | a carta narra fato e valor e pede documento. Nenhuma afirmação de ilegalidade | ✓ |
| **Sem promessa** | expectativa do canal escrita como é: resposta em prazo, sem garantia de acordo. Nada de "vai pagar uma fração" | ✓ |
| **Ressalva nas reguladas** | o teto sai com a ressalva de não retroatividade, e a data do caso ficou `[A CONFIRMAR]` | ✓ |
| **Gate regulado** | a carta vai a canal oficial, não ao público | n/a |
| **Disclaimer fixo** | no fim do arquivo, palavra por palavra | ✓ |
| **Anti-IA (HARD)** | busca feita: 0 travessão longo, 0 ocorrência da família banida | ✓ |
| **VEREDITO** | o pior item é ✓ | **LIBERA** |

**STOP.** A skill parou aqui e perguntou se a carta servia, antes de escrever o acompanhamento do
ciclo. Uma peça por vez.

---

## Caso C · o pedido que a skill NÃO atendeu

Vale mostrar, porque é o comportamento que separa esta skill de um chute com aparência de ajuda.

### O que a pessoa deu

> "Recebi uma carta do oficial de justiça sobre uma dívida de financiamento do carro. Me escreve uma
> defesa pra eu apresentar, você entende disso."

### O que aconteceu na árvore

```
1. Há ação judicial, citação, penhora, bloqueio ou risco de perder bem?
   SIM. "Carta do oficial de justiça" é citação. → STOP DE ESCALADA.
```

A skill não passou da linha 1. Não perguntou valor, não perguntou renda, não abriu reference de
dívida. A resposta:

> Não vou escrever isso, e é importante você entender por quê.
>
> Carta de oficial de justiça significa que já existe um processo e que corre um prazo contra você.
> Defesa em processo é ato privativo de advogado (art. 1º da Lei 8.906/94), e uma peça escrita por
> quem não é advogado não vale nada no processo. Pior: enquanto você tenta resolver por fora, o prazo
> passa, e prazo perdido não volta.
>
> O que fazer agora, nesta ordem:
>
> 1. **Olhe a data na carta.** O prazo começa a contar dela, e costuma ser curto.
> 2. **Procure um advogado hoje.** Se não puder pagar, a Defensoria Pública da sua cidade atende de
>    graça e é exatamente pra isso que ela existe.
> 3. Leve a carta inteira, o contrato do financiamento e os comprovantes de pagamento que tiver.
>
> O que eu **posso** fazer com você enquanto isso, e é seguro: organizar essa documentação numa lista
> ordenada, pra você chegar no atendimento com tudo na mão e não perder a consulta juntando papel.
> Quer que eu monte essa lista?
>
> *Este conteúdo é informativo e educativo. Não constitui parecer ou consultoria jurídica nem contábil
> (atividade privativa de profissional habilitado) e não substitui a análise individualizada de um
> advogado ou contador. Cada caso tem particularidades que precisam ser avaliadas.*

Três coisas dessa resposta merecem atenção:

- **A recusa veio com caminho.** Não é "não posso ajudar", é "não é comigo, é com quem, e é hoje".
- **A urgência foi dita sem pânico.** O medo é a alavanca que faz a pessoa aceitar acordo ruim. Fato e
  prazo bastam.
- **Sobrou algo seguro de fazer.** Organizar documento não é ato privativo de ninguém, e ajuda de
  verdade.
