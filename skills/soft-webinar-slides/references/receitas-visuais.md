# Receitas visuais: o agente desenha cada slide

No modo agente, você é o designer. Cada slide é um arquivo HTML que você desenha com juízo visual, seguindo o `guia-slides-provado.md`, e olha renderizado antes de seguir pro próximo. As receitas de `assets/receitas/` são pontos de partida testados: abra a que serve, entenda a composição e adapte. Elas trazem só `{{MARCADORES}}`, nunca texto de exemplo; todo texto, número e nome sai do roteiro do dono.

## O contrato de um slide

Um arquivo por slide em `trabalho/slides/` (`01.html`, `02.html`, na ordem do deck). O `ler_roteiro.py --esqueleto` já cria cada um com o roteiro num comentário e a nota escrita.

```html
<section class="slide escuro" data-nome="nome curto" data-bloco="Abertura">
<style>
.quadro { position: absolute; inset: 110px 140px; }   /* o script prefixa com o id do slide */
:scope { }                                            /* :scope é o próprio slide */
</style>
<div class="quadro"> ... HTML e SVG em 1920x1080 ... </div>
<div data-click="1" data-fx="subir"> ... entra no clique 1 ... </div>
<aside class="notes">Objetivo: ...
Abre com: ...
Clique 1: ...
Fecha com: ...</aside>
</section>
```

- **Fundo:** `claro` ou `escuro` na classe; troca quando o bloco da aula muda, nunca slide a slide.
- **Cores:** só as variáveis. `var(--bg)` o fundo do slide (halo, véu), `var(--ink)` texto, `var(--dim)` texto apagado, `var(--dest)` a cor do que importa, `var(--acao)` link e pílula, `var(--linha)`, `var(--suave)` e `var(--dest-suave)` pra formas e fundos de cartão. A `var(--reservada)` só existe nas peças `.tarja`, `.risco-linha` e `.rot-bonus`.
- **Peças com papel fixo:** `.dest` (palavra em destaque), `.risco` com `.risco-wrap > .risco-rot > .risco-linha` (preço antigo riscado), `.tarja` (bônus dos primeiros, sempre no mesmo canto), `.rot-bonus`, `.pct` (percentual), `.acao-pilula` ("Escreve no chat"), `.marca`.
- **Clique:** `data-click="N"` no bloco que entra, com `data-fx` `subir` (texto), `aparecer` (véu, pílula, link), `riscar` (preço antigo) ou `selo` (percentual). Título e imagem já estão na tela quando o slide abre. Não ponha `opacity` nem `transform` no próprio elemento que tem `data-click`: embrulhe.
- **Texto em HTML, forma em SVG.** Texto dentro de SVG com `viewBox` escalado engana a medida de fonte. Rótulo HTML posto por cima de uma forma SVG é medido contra o preenchimento liso do SVG; com gradiente ou imagem por baixo o script só avisa. O jeito sem dúvida é dar ao rótulo o seu próprio fundo HTML (`background` na caixa do texto), que ele mede sempre. SVG e bloco marcado `data-imagem` vão pro PPTX como imagem, na mesma posição. Texto dentro de `data-imagem` (célula de grade, número de pictograma) e célula repetida 6 vezes ou mais também não contam no teto de 40; o piso de fonte e a sobreposição continuam medindo tudo.
- **Imagem do dono:** `<img src="caminho relativo à pasta dos slides">`; o script copia pra `img/`.
- **Vaga (print ou cena que falta):** bloco de borda tracejada com `data-vaga` no lugar da imagem, rótulo no piso de 30px ou mais: "print ou recibo de [o quê]" ou "cena: [o quê]". O `checar_deck.py` avisa "vaga sem imagem" e não reprova. A receita `print-moldura` traz as duas formas, `<img>` ou `data-vaga`; com o print do dono, a vaga vira o `<img>`.
- **Oferta, bônus e escada** levam `data-layout="oferta"`, `"bonus"` ou `"escada"`: são os únicos que passam de 40 palavras (o teto único; vaga, legenda, tarja e `.rot-bonus` não contam). Tabela que soma: `data-geometria` no bloco que contém as linhas e o total, `data-valor` em cada valor, `data-total` no total.
- **Texto por cima de forma de propósito** (número sobre a barra): `data-sobrepoe` no texto de cima.

## O laço de cada slide (até 2 correções)

1. Leia o comentário do esqueleto: objetivo, conteúdo, falta e cliques daquele slide.
2. Pergunte, como o guia manda na passada 2: dá pra mostrar em vez de contar? Número vira imagem; lista vira pilha, grade de ícones ou escada; afirmação vira print, antes e depois ou metáfora que bate com a fala. Escolha a receita pela tabela abaixo ou desenhe a sua.
3. Escreva a tela na versão curta do roteiro: uma frase completa de até 12 palavras, lida em 3 segundos. O que não cabe vai pra nota. Roteiro com slide longo passa antes pelo passo Dividir (`dividir-o-roteiro.md`).
4. Rode só aquele slide e olhe:
   ```
   python3 scripts/montar_desenho.py trabalho/slides --saida trabalho/ver/07 --so 7
   ```
   Abra `trabalho/ver/07/png/slide-07.png` (Read). Use uma `--saida` por slide (`trabalho/ver/NN`): a rodada apaga os PNGs da anterior na mesma saída. Com `--estados`, sai um PNG por clique.
5. Confira o checklist do guia (seção 8) olhando a imagem: uma ideia, o maior é o que importa, número virou imagem, nada vazio ou lotado, nada encostado na borda, a imagem diz o mesmo que a fala. Some o que o script reprovou.
6. Corrija e rode de novo, no máximo duas vezes. Se ainda estiver ruim, simplifique (uma frase grande e um elemento visual) e anote no `_operador.md` o que ficou devendo.

Só depois desenhe o slide seguinte. Ao fim, o deck inteiro: `montar_desenho.py trabalho/slides --saida trabalho/deck --insumo trabalho/roteiro.md`. A pasta do deck é sempre `trabalho/deck`, dentro da pasta de trabalho, nunca `../deck`.

## O que o slide diz, e a receita que mostra

| o roteiro traz | receita | o visual |
|---|---|---|
| frase de impacto, combinado, pergunta pro chat, PUV | `letra-grande` | a frase enorme, rótulo pequeno, pílula de ação por clique |
| custo que se repete por mês ou por dia | `numero-calendario` | grade de meses ou dias, X por clique |
| proporção, concorrência, "1 contra muitos" | `numero-radar` | pontinhos e o ponto grande em destaque |
| dois a seis números que se comparam | `numero-barras` | barras proporcionais, a que importa em destaque |
| "1 em cada N", contagem de gente | `numero-pictograma` | figuras, as que importam pintadas |
| dinheiro ou contagem grande, um valor por slide | blocos com escala única (`receita-numero-em-blocos.md`) | "1 bloco = [unidade]", mesmo bloco em todos os slides, fração pintada dentro |
| prova (resultado, conversa, painel) | `print-moldura` | o print grande, borda fina, círculo no número; sem o print, a vaga com `data-vaga` |
| narrativa, emoção, future pacing, crença | metáfora (desenho seu) | a que ilustra a fala sem pessoa, cena nem número novo; entre duas, a mais simples (uma forma, uma ação). Cena que a fala não descreve: vaga de cena |
| o que a pessoa leva, somando | `pilha-valor` | a pilha cresce por clique e a coluna do total sobe |
| cada bônus | `bonus-tarja` | capa, dor, promessa, o que aprende, valor riscado, R$0 |
| dois caminhos, antes e depois, responsabilidade | `antes-depois` | dois lados, o da fala em destaque; lados com números de itens diferentes (4 e 3): variante "colunas desiguais" no cabeçalho da receita |
| o passo atual do método | `bussola` | trilho com o passo feito riscado e o atual enorme |
| níveis, módulos, "você está aqui", a decisão, o produto | `escada` | degraus que sobem com nome e promessa; a mesma escada em todas as voltas (`esquema-principal-reusado.md`) |
| o esquema na abertura, antes de ensinar | `previa-cortada` | o esquema de canto, cortado e embaçado |
| desculpas, loops, "o que você vai ver" | `grade-icones` | ícone grande por item, de cima pra baixo |
| preço cheio que cai pro valor da oferta, em degraus | `receita-preco-em-degraus.md` (desenho seu) | valor riscado por clique, seta, parcela manchete, à vista menor; o valor por dia fecha |
| garantia em etapas, sem esquema principal na aula | `receita-trilho-de-garantia.md` (desenho seu) | trilho de 3 cartões ligados, um por clique |
| o carrinho e a tela fixa das perguntas | `oferta-tabela` | tabela que soma, total riscado, parcela manchete, link |
| a chamada | `cta-faixa` | o link numa faixa de ponta a ponta |

Fora da tabela, desenhe: um chat com o balão que a pessoa vai escrever, uma linha do tempo, um iceberg quando a fala é "isso é só a ponta", um relógio, a barra de abas do navegador. A regra 7 do guia vale pra tudo: a imagem diz o mesmo que a fala, senão sai.

## Proporção e ritmo

- Margem de 120 a 150px dos lados e de 90 a 120px em cima e embaixo. Nada encostado na borda, a não ser de propósito (faixa de ponta a ponta, prévia cortada).
- Tamanho de letra, num slide de 1920x1080: nenhum texto abaixo de 30px, nem legenda nem rodapé. Kicker, rótulo e legenda no mesmo piso, 30px ou mais; apoio de 40 a 48px; frase ou número que decide em 56px ou mais (frase principal de 64 a 120px, número-imagem de 150 a 220px). O `checar_deck.py` imprime a menor fonte medida (`menor fonte: Npx`) e reprova abaixo do piso (`--min-fonte`, padrão 30): corrija até passar. Rótulo e legenda cinza apagados encolhem no celular: prefira a cor de texto.
- Preço: a parcela é a manchete, grande (número-imagem de 150 a 220px); o à vista vem menor. O que o guia proíbe em fonte gigante e isolada é o preço cheio (tamanho de título, com o rótulo do roteiro e o que ele cobre). "[valor] por dia" é a parcela dividida, não o preço cheio: pode ser o número com o rótulo. Calendário de 30 casas só se o roteiro trouxer o 30: "30 dias", "dividido por 30" ou "por 30" valem, o 30 do roteiro basta, mesmo sem a palavra "dias". Nesse caso são 30 casas sem numeral dentro e uma acesa (a de hoje, o valor por dia). Se o roteiro só diz "por dia", sem o 30, o calendário vai sem contagem de casas (uma folha, ou uma fileira que segue além da borda) e sem numeral dentro.
- Botão: o roteiro marca `[BOTÃO]` (vira "Obs.: BOTÃO" na nota, fora da tela) ou o Objetivo diz "botão visível"; desenhe o botão com a frase do roteiro e use `cta-faixa` quando há link (`dividir-o-roteiro.md`).
- Um elemento dominante por slide. Se dois disputam, um fica menor ou vai pro clique seguinte.
- Varie a composição: frase sozinha, frase com imagem do lado, imagem cheia, duas colunas, grade. Dois slides seguidos com a mesma composição pedem motivo.
- Slide de texto puro (só linhas de texto, sem forma, número-imagem, ícone, print ou diagrama) é exceção: a frase de impacto que o roteiro pede assim. Dois seguidos, nunca.

## Condição de entrada de cada bloco

O bloco só entra quando o dado está no insumo. Sem o dado, ele sai e vira pergunta no `_operador.md`:

| bloco | entra com | sem o dado |
|---|---|---|
| número vira imagem | o número e a unidade do insumo | a frase com a ideia, sem número |
| print e depoimento | o print autorizado | o slide sai ou fica só com a frase; o pedido vai pro dono |
| tabela da oferta e pilha | item e valor de cada linha | só os nomes, sem valor e sem total (`receita-pilha-de-nomes.md`), ou o preço em degraus |
| preço em degraus | valor cheio e parcela | sai; pergunta o preço |
| tarja dos primeiros | o número e o critério no CONTEÚDO ou na fala (o que só está no texto da FALTA não vale: vira pergunta, sem tarja); sem o motivo, a tarja leva só "N primeiros" e o motivo vira pergunta | sem número, sem tarja (`receita-pilha-de-nomes.md`) |
| percentual, prazo | o número, o critério e o motivo do dono | sai |
| hora no cronograma | a hora do dono | linha sem hora |
| objeto do dia a dia | o objeto que o dono indicou, com foto | vaga de cena (`dividir-o-roteiro.md`, regra 8) se o slide tem tela própria; se a conta já é a tela, só a conta |

## O que nunca entra

- Número, proporção, contagem de células ou de figuras, nome, depoimento, logo ou print que o roteiro não traz. O visual nasce do dado; sem o dado, outra receita.
- Texto de exemplo de receita. Se um texto de tela não está no roteiro do dono, ele não vai pro slide.
- Pessoa, personagem, foto do dono, cena inventada, banco de imagem e imagem de IA: sem o real, vaga tracejada.
- Enfeite sem função: ícone que não bate com a fala, animação sem papel, cor fora das duas de destaque e da reservada.
- Lacuna, colchete ou `{{MARCADOR}}` na tela. O script barra.

## Onde está o resto

- Dividir o roteiro antes de desenhar: `dividir-o-roteiro.md`.
- Número que vira imagem com escala única: `receita-numero-em-blocos.md`.
- Itens sem valor (bônus só com nome), a contagem e a tarja dos primeiros: `receita-pilha-de-nomes.md`.
- Preço que cai em degraus, com o risco por clique e o valor por dia: `receita-preco-em-degraus.md`.
- Garantia em etapas quando não há esquema principal: `receita-trilho-de-garantia.md`.
- A mesma escada no ensino, no recap, na decisão e como produto: `esquema-principal-reusado.md`.
- Perguntas ao dono e o relato final: `perguntas-ao-dono.md`.
- Evidência medida: `evidencia-v4.md`.
