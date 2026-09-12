# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, empresa, valores, datas e resultados foram inventados só pra
> mostrar a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega
> de verdade. Num trabalho real, todo dado sem fonte nasce marcado `[A CONFIRMAR]` e o dono confirma
> antes de sair.

**O caso fictício:** uma gráfica rápida que atende empresa pequena com material impresso (cartão,
banner, adesivo, papelaria, brinde). Trabalha com prazo curto, e boa parte dos pedidos tem data de
evento amarrada. O dono atende junto com duas pessoas.

Este arquivo mostra a saída resumida de cada ação, na ordem. A saída real é maior; aqui está só o
suficiente pra você reconhecer o formato antes de começar.

---

## O que chegou (colado pelo dono, sem contexto)

> **Dono:** "Olha o que a Cláudia mandou agora. Me ajuda a responder que eu não sei nem por onde
> começar."
>
> Mensagem da cliente:
>
> > "Bom dia. Os banners chegaram ontem à noite, faltando um e com o logo cortado nos outros dois.
> > O evento é sábado. Eu paguei adiantado e confiei porque vocês me atenderam bem em janeiro. Assim
> > não dá. Quero meu dinheiro de volta e vou pensar muito antes de indicar vocês pra alguém."

---

## Ação 1 · ENTENDER

**A pergunta que a skill fez ao dono, antes de qualquer coisa:** *"do seu lado, o que aconteceu?"*

> **Dono:** "O arquivo veio com o logo muito perto da margem e ninguém avisou ela. E o terceiro banner
> deu pane na impressão e a gente mandou dois achando que ia resolver o terceiro no dia seguinte. Não
> avisamos ela disso."

**A segunda pergunta, as três de uma vez:**

> **Dono:** "Cliente desde janeiro, terceiro pedido, `[fictício]` uns R$ 3.400 no total. Nunca reclamou."

Bloco de situação, no topo do `caso-claudia-14-marco.md`:

```
QUEM: cliente ha 3 meses, 3 pedidos, R$ 3.400 no total, primeira reclamacao
O FATO: 2 banners com o logo cortado + 1 nao entregue, com evento no sabado
O PEDIDO: ela pediu reembolso; pelo texto, quer os banners certos antes de sabado
GRAVIDADE: alta (o dano esta correndo, o evento e daqui a 2 dias)
FALTA SABER: se da pra reimprimir os 3 ate sexta [CONFIRMAR ANTES DE ENVIAR]
```

**A leitura que mudou a resposta:** o pedido literal é reembolso, mas o evento é sábado. Dinheiro de
volta não resolve o problema dela, deixa ela sem banner no evento. O que ela quer é banner certo até
sexta. Reembolso é o que ela pede quando acha que a primeira coisa não é possível.

**A gravidade alta disparou a regra própria:** a primeira mensagem sai antes da solução estar pronta.

---

## Ação 3 · O QUE OFERECER (rodou antes da 2, porque o pedido é reembolso)

A pergunta de calibragem: *"isso foi falha nossa, foi coisa de fora, ou foi mal-entendido?"*

> **Dono:** "Metade e metade. O arquivo dela veio ruim, mas a gente viu e não avisou. O terceiro
> banner foi nosso mesmo."

Saída real, a tabela dentro do arquivo do caso:

| Opção | Custo | O que resolve | Risco |
|---|---|---|---|
| **A. Reimprimir os 3 com o logo ajustado, entrega sexta de manhã, sem cobrar nada a mais** | `[fictício]` R$ 260 de material | Resolve o problema real: ela tem banner no evento. Reconhece o tamanho do erro | prazo apertado; se não sair sexta, piora tudo |
| B. Reimprimir os 3 e devolver 30% do pedido | R$ 260 + R$ 340 | Resolve e compensa | generoso demais pro caso; abre precedente de reembolso parcial em reimpressão |
| C. Devolver o valor integral | R$ 1.130 | Encerra o assunto | ela fica sem banner no sábado e perde o evento. Pior desfecho possível pra ela |

**Recomendação: A**, com uma condição: só prometa sexta de manhã se a impressão couber hoje. Prazo
quebrado numa resposta a reclamação transforma cliente insatisfeito em cliente perdido.

> **Dono:** "Cabe. Consigo rodar hoje à tarde."

---

## Ação 2 · RESPONDER

**A primeira mensagem, que saiu em 20 minutos** (gravidade alta responde antes de ter tudo pronto):

> Oi Cláudia, acabei de ver. Você tem razão nas duas coisas: o logo saiu cortado e o terceiro banner
> nem foi. E ninguém te avisou de nada disso.
> Estou vendo aqui agora pra te dar uma resposta com data ainda hoje de manhã.

**A resposta completa, 40 minutos depois:**

> Cláudia, resolvido do meu lado:
>
> Os três banners voltam pra impressão hoje à tarde, com o logo ajustado pra dentro da margem, e
> ficam prontos sexta de manhã. Eu mesmo levo aí, sem custo nenhum a mais pra você.
>
> O que aconteceu: o arquivo veio com o logo bem na borda, a gente viu na hora de imprimir e devia
> ter te ligado antes de rodar. Não ligamos. E o terceiro banner deu problema na máquina, mandamos
> dois achando que resolveríamos no dia seguinte, e também não te avisamos. Os dois erros são meus.
>
> Sobre o reembolso: se sexta de manhã os banners não estiverem na sua mão do jeito certo, eu
> devolvo o valor integral no mesmo dia, sem você precisar pedir de novo.
>
> Vou te mandar a foto do primeiro banner assim que sair da máquina, hoje à tarde, pra você aprovar
> antes de eu rodar os outros dois.

**O que o gate pegou no primeiro rascunho:**

| Check | Primeiro rascunho | Correção |
|---|---|---|
| Reconhecimento antes de explicação | ✗ abria com "o arquivo que você mandou veio com o logo na margem" | Reordenado: reconhecimento primeiro, explicação na terceira parte |
| Sem "mas" | ✗ "sinto muito, mas o arquivo veio fora do padrão" | Cortado o "mas"; a informação do arquivo foi pra parte 2, em frase própria |
| Sem culpar terceiro | ✗ "a máquina deu pane" como justificativa | Virou "deu problema na máquina, e não te avisamos", que é a parte que é responsabilidade dele |
| Tem ação com prazo e nome | ✓ | |
| Zero fato inventado | ✓ (o prazo de sexta foi confirmado com o dono antes de entrar) | |
| Linguagem de departamento | ✗ fechava com "agradecemos a compreensão" | Cortado |

```
$ python3 scripts/lint_copy.py caso-claudia-14-marco.md
OK (0 HARD, 1 WARN)
```

O aviso apontou a palavra "resolver" três vezes. Duas foram trocadas por "sair certo" e "estar na sua mão".

**A resposta não foi enviada pela skill.** Ficou no arquivo, e o dono copiou e mandou.

---

## Ação 4 · CONSERTAR A CAUSA

A pergunta: *"quantas vezes você ouviu isso nos últimos três meses?"*

> **Dono:** "De logo cortado? Umas três, quatro. Sempre arquivo do cliente. A gente refaz e pronto."

Duas linhas no fim do arquivo:

```
VEREDITO: padrão. É a quarta vez em 3 meses de arte cortada por arquivo fora de margem.
MUDANÇA: conferir margem antes de rodar e ligar pro cliente quando o arquivo estiver na borda.
Custa 2 minutos por pedido e uma ligação. [A CONFIRMAR: quem confere hoje, e se dá pra
mandar a orientação de margem junto com o orçamento]
```

**A conversa que isso abriu, e que é o valor real da ação 4:**

> **Dono:** "Se eu ligar pra todo mundo eu não faço mais nada."
>
> "Não é pra ligar pra todo mundo. É pra ligar quando o arquivo está na borda, que aconteceu 4 vezes
> em 3 meses. São 4 ligações em 3 meses, contra 4 reimpressões e uma reclamação de gravidade alta.
> E tem uma versão mais barata: mandar a orientação de margem junto com o orçamento. Aí quase todo
> mundo já manda certo, e a ligação vira exceção."

Registro proposto, que não existia:

```
data | quem | o que aconteceu | gravidade | o que foi oferecido | resolveu?
14/03 | Claudia, evento | logo cortado + 1 banner nao entregue | alta | reimpressao 3 + entrega + garantia de reembolso | [aguardando sexta]
```

---

## O resumo que foi pro dono

> A resposta está pronta no arquivo, é você quem manda. Duas coisas:
>
> 1. Ela pediu reembolso, mas o que ela quer é banner no sábado. A resposta oferece isso, com
>    reembolso automático se sexta não sair. Isso costuma segurar o cliente e ainda resolve o
>    problema dele.
> 2. É a quarta arte cortada em três meses. Mandar a orientação de margem junto com o orçamento
>    custa nada e mata quase todos os casos. Fica com você.
>
> Uma coisa pra confirmar antes de mandar: você disse que a impressão cabe hoje à tarde. Se tiver
> qualquer dúvida disso, mude o prazo pra sexta à tarde agora, não depois.
