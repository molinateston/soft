# Receita: pilha de nomes (itens sem valor)

Use quando o roteiro lista bônus, módulos ou entregas só pelo nome, sem valor avulso. As receitas `pilha-valor` e `oferta-tabela` dizem "sem o valor, não entra"; esta é a saída da linha "só os nomes, sem valor e sem total" da tabela de condição de entrada (`receitas-visuais.md`). Desenhe você mesmo, no HTML do slide, com as classes e o contrato de `receitas-visuais.md`.

## O desenho

- **Cartões que enchem.** Cada item é um cartão de uma linha com o nome do dono em 42px ou mais, num fundo `var(--suave)` com borda `var(--linha)`. Os cartões entram por clique, um por clique, na ordem da fala, e a pilha vai enchendo o quadro.
- **Sem valor e sem soma.** Nada de preço, "R$0", riscado, coluna de total, `data-valor`, `data-total` ou `data-geometria`: o checador cobra conta de quem tem esses atributos. Vale também pro item que tem valor (o produto de R$3.500, por exemplo): o valor dele mora no slide de preço, não no cartão. O que o dono não disse não aparece.
- **Tarja dos primeiros na mesma posição.** A peça `.tarja` (receita `bonus-tarja`) fica no mesmo canto e no mesmo tamanho em todos os slides da pilha. Regra de entrada abaixo.
- **Sete cliques no máximo.** Lista de 8 ou mais: divida em 2 slides, metade em cada (8: 4 e 4; 9: 5 e 4). No segundo, os itens do primeiro já estão na tela, apagados e sem clique, e os novos entram por clique: a pilha parece continuar. Passando de 40 palavras, use `data-layout="bonus"`.
- **Abre com e Fecha com** de cada metade: `dividir-o-roteiro.md`.

## A contagem

A regra do guia "nunca anuncie a contagem antes" vale para o desenho que você cria: vaga vazia contada, "Bônus 3 de 8" e "8 bônus" escritos por você ficam fora. O que o dono fala ("oito bônus") fica como está e vai nas notas. O nome de item que o dono escreve com número ("Operação SOFT, 6 módulos completos") vale inteiro no cartão: é o nome dele, não contagem sua; o que se proíbe é inventar a contagem. Na tela, a pilha sem número, a não ser que o roteiro ponha o número na tela; aí a frase é do dono e entra como ele escreveu.

## A tarja dos primeiros

| o roteiro traz | na tela | no relato |
|---|---|---|
| o número e o critério no CONTEÚDO ou na fala ("15 primeiros que entrarem hoje") sem o motivo do limite | tarja só com "15 primeiros", sem contador, sem "últimas vagas", sem prazo | o motivo vira pergunta em "Falta você responder" |
| "os primeiros" sem número, ou o número só no texto da FALTA | sem tarja | pergunta: quantos e por quê (ou se vale o número da FALTA) |
| número, critério e motivo | tarja com o número; o motivo vai na fala e na nota | nada pendente |

Razão: o guia pede a tarja nos bônus dos primeiros, e a tarja só repete o limite que o dono já falou. O que a tela inventaria sozinha (contador, vaga que acaba, prazo) segue barrado pela regra "escassez sem motivo real".

## Antes de dar por pronto

- Os nomes estão como o dono escreveu. Nome próprio que o lint barra entra em `trabalho/termos-do-dono.txt` (`conferencia.md`).
- A pergunta do valor, da dor e da entrega de cada item está em "Falta você responder": quando ele responder, a pilha troca para `pilha-valor`.
- Slide da pilha anotado no `_operador.md` como metáfora sua, com a ideia da fala que ele ilustra, em palavras suas.
