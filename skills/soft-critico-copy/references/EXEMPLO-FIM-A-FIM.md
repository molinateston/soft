# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** As peças, os números, o nome do método e o resultado foram
> inventados só pra mostrar a FORMA do veredito. Nada disso é caso real e nada disso pode ser
> copiado pra uma entrega de verdade.

**O caso fictício:** uma professora de canto que dá aulas online e vende um curso de 12 semanas de
técnica vocal pra quem canta em coral de igreja. Tese declarada por ela: "quem canta desafinado não
tem ouvido ruim, tem apoio de respiração errado". Método batizado por ela: Apoio em Três Tempos.
Oferta: curso de 12 semanas, 697 reais. Lastro declarado: das 11 alunas da última turma, 9 cantaram
a frase inteira do hino sem respirar no meio na semana 12, com vídeo de cada uma.

Este arquivo mostra três auditorias na ordem: a headline de um anúncio reprovada no modo rigoroso
(que já vem ligado em peça de venda), a mesma headline aprovada com nota 10 depois da correção, e um
lote de 5 legendas de feed educativo no modo padrão, com o filtro 6 rodando em cada peça.

---

## Auditoria 1 · Uma headline de anúncio, REFAZER

### O que entrou

```
peça: "Descubra o segredo que vai reinventar a sua voz e transformar a sua confiança no palco."
tipo: headline do anúncio do curso (peça de venda: modo rigoroso por padrão)
tese declarada: quem canta desafinado tem apoio de respiração errado, não ouvido ruim
oferta declarada: curso de 12 semanas, 697
material de lastro: o caso das 9 alunas, declarado na conversa
```

### O que a skill rodou

Passo 1: peça salva em `copy-em-analise.txt`.
Passo 2, filtro 3 em código:

```
python3 scripts/lint_copy.py copy-em-analise.txt
  ⚠ frase-emoldura de revelação: o segredo
  ⚠ verbo de transformação genérico: reinventar
  ⚠ verbo de transformação genérico: transformar
```

Exit 0, mas 3 avisos diferentes na mesma peça, o que reprova o filtro 3 pela régua dos 3 avisos.

Passo 3, leitura pelo sentido: CUB, depois o filtro 6. O filtro 6 reprovou em quatro critérios, a
cascata parou a leitura ali: os filtros 2 e 4 e os checkpoints não rodaram, e o 5 só fez a extração (nada sem lastro fora da promessa).

### O veredito, como saiu em `veredito-copy-headline-canto.md`

```
peça: "Descubra o segredo que vai reinventar a sua voz..."
tipo: headline (anúncio do curso, peça de venda)
modo: rigoroso
nota: 2/10
veredito: REFAZER
severidade: 4 bloqueantes (filtro 6, headline)
encaixe narrativo: não medido, sem arco informado
falhas:
  - filtro: CUB + Validador de conversão
    dimensao: B de Boring e critério 1, promessa copiável · gravidade 9
    trecho: "transformar a sua confiança no palco"
    motivo: com a marca coberta, a linha roda no anúncio de qualquer professora de canto do país, e ninguém lembra de quem era.
    sugestao: molde de promessa: "Em 12 semanas, com o Apoio em Três Tempos, você canta a frase inteira do hino sem buscar ar no meio." O prazo sai do caso das 9 alunas; sem esse lastro, a linha começaria pelo método.

  - filtro: Validador de conversão
    dimensao: critério 4, promessa sem execução, sinal vermelho do verbo de estudo · gravidade 8
    trecho: "Descubra o segredo que vai reinventar a sua voz"
    motivo: a promessa é de descobrir; quem paga quer cantar a frase inteira, e estudar o segredo não entrega isso.
    sugestao: verbo de fazer com o resultado que o caso dela mede: cantar a frase inteira sem respirar no meio.

  - filtro: Validador de conversão
    dimensao: critério 2, dor verdadeira · gravidade 8
    trecho: "a sua confiança no palco"
    motivo: estado abstrato, sem um elemento de cena; e quem canta em coral de igreja nem sobe em palco.
    sugestao: molde de dor comprimido: o ar que acaba no meio da frase do hino, na frente do coral inteiro.

  - filtro: Validador de conversão
    dimensao: critério 3, parar o scroll · gravidade 8
    trecho: a linha inteira
    motivo: sem contraste e sem quebra do esperado; desce fácil e some da cabeça no mesmo segundo.
    sugestao: abrir pelo contraste entre o que ela culpa (o ouvido) e o que falha de fato (o ar).

suspenso pela cascata: 3 avisos do lint (filtro 3 reprovado pela régua dos 3 avisos); Estrutura-mãe, filtro 4 e checkpoints não rodaram, Verbatim só na extração; voltam na rodada da reescrita
reescrita por gravidade: critério 1 (9) · critério 4 (8) · critério 2 (8) · critério 3 (8)
abaixo de 10 não sobe.
Quer a peça de volta no molde certo? Aponte as falhas e a skill de origem devolve a versão corrigida.
Copy que qualquer concorrente assinaria já está enterrada; o caixa só demora uns dias pra mandar o aviso.
```

A nota sai da regra: o critério 1 (gravidade 9) põe o teto em 5, e os critérios 4, 2 e 3 (gravidade 8)
tiram 1 ponto cada. O critério 5 fica n/a, porque a headline é linha isolada e o custo de não agir é
medido no corpo do anúncio.

---

## Auditoria 2 · A mesma headline depois da correção, APROVADA

### O que entrou na segunda rodada

```
peça: "O ar acaba na metade do hino e a nota desce junto. Faça as 12 semanas do Apoio em Três Tempos e cante a frase inteira sem buscar fôlego no meio."
tipo: headline (anúncio do curso, peça de venda)
```

### O que a skill rodou

Filtro 3: exit 0, zero aviso. Filtro 1: passa nas 3 dimensões, a frase vira imagem na primeira
leitura. Filtro 6: com a marca e o método cobertos, outra professora teria de copiar o método e o caso
pra assinar a linha; a cena do ar acabando no hino é a dor de quem canta no coral; o contraste da nota
que desce segura o scroll; resultado, caminho e ação estão na segunda frase, com o prazo do caso das 9
alunas; o critério 5 fica pro corpo do anúncio. Filtro 2: headline comprime, e a peça entrega
Diagnóstico e Nova interpretação, o mínimo do formato. Filtro 5: método e prazo com lastro declarado.
Filtro 4: zero padrão.

Checkpoints: mecanismo 10 de 10 (nome dela, método de três tempos que se desenha, só funciona no coral,
entrega de processo); voz 12 de 12 (testes 5, 7, 8, 9 e 10 n/a em peça de 2 linhas, teste 11 n/a sem
perfil de voz); critérios de impacto n/a (headline sem corpo); transformação 15 de 15 (7, 8, 9 e 12
n/a); clareza, limpeza e proibições sem achado.

### O veredito

```
peça: "O ar acaba na metade do hino e a nota desce junto..."
tipo: headline (anúncio do curso, peça de venda)
modo: rigoroso
nota: 10/10
veredito: APROVADA
encaixe narrativo: não medido, sem arco informado
resumo: método com o nome dela, dor em cena no coral, contraste na primeira linha, resultado com o prazo do caso das 9 alunas. Pode subir.
```

---

## Auditoria 3 · Um lote de 5 legendas de feed educativo, em série

Entrada: 5 legendas de post pra semana, mandadas de uma vez. Feed educativo: modo padrão, filtro 6
rodando em cada peça com o peso do tipo. As 5 foram lidas UMA POR VEZ, cada uma com as duas
passadas (ou parada na cascata), e o consolidado saiu só depois da quinta.

### `veredito-copy-lote-semana-03.md`, o topo do arquivo

```
lote: legendas semana 03  ·  5 peças  ·  2 aprovadas  ·  3 reprovadas
severidade: 2 bloqueantes · 1 corrigível · 2 observações
```

### O resumo por peça, como saiu

| Peça | Tipo | Veredito | Filtro que quebrou | Severidade |
|---|---|---|---|---|
| 1, "o ar acaba antes da frase" | corpo | APROVADA | nenhum; no filtro 6, critérios 1, 2 e 3 passam e o 4, lido como ação de hoje, passa | observação, 1 padrão estrutural |
| 2, capa de lista de 3 erros da voz | capa | REPROVADA | anti-IA lexical, falha dura, e filtro 6, critério 1 (cascata) | bloqueante |
| 3, "coral inteiro afina junto" | corpo | REPROVADA | Estrutura-mãe, pulou Nomeação (filtro 6 passou) | corrigível |
| 4, "87% das pessoas cantam errado" | headline | REPROVADA | filtro 6, critérios 1 e 2 (cascata), com o número sem lastro no motivo | bloqueante (headline) |
| 5, "o que eu faço antes de cantar" | script_reel | APROVADA | nenhum; o aquecimento mostrado é o Apoio em Três Tempos, e o teste do concorrente passa | observação, hedge isolado |

### A peça 2, por extenso

```
peça 2: capa "3 erros que [o verbo-freio banido] a sua voz"
tipo: capa
veredito: REPROVADA
severidade: 2 bloqueantes
encaixe narrativo: não medido, sem arco informado
falhas:
  - filtro: anti-IA lexical
    dimensao: falha dura, o verbo-freio banido no meio da frase
    trecho: o verbo que a régua anti-voz proíbe, na terceira palavra da capa
    motivo: o lint saiu com exit 1. Falha dura não sai do jeito que está, sem discussão.
    sugestao: trocar o verbo e, junto, a promessa (falha abaixo).

  - filtro: Validador de conversão
    dimensao: critério 1, promessa copiável · gravidade 9
    trecho: a capa inteira
    motivo: lista de erros sobre "a sua voz" roda no perfil de qualquer professora de canto; com a marca coberta, ninguém sabe de quem é.
    sugestao: amarrar a lista na tese dela: "Os 3 erros de respiração que fazem o ar acabar no meio do hino."

suspenso pela cascata: Estrutura-mãe e filtro 4 não rodaram, Verbatim só na extração; voltam na rodada da reescrita
```

### A peça 4, por extenso

```
peça 4: "87% das pessoas cantam errado e nem sabem"
tipo: headline
veredito: REPROVADA
severidade: 2 bloqueantes (filtro 6, headline)
encaixe narrativo: não medido, sem arco informado
falhas:
  - filtro: Validador de conversão
    dimensao: critério 1, promessa copiável · gravidade 9
    trecho: "87% das pessoas cantam errado"
    motivo: qualquer perfil de canto publica essa linha igual; e o 87% não aparece em nenhuma fonte da dona, então o número sai da reescrita.
    sugestao: trocar pelo que ela pode provar: "de cada 10 alunas que chegam aqui, 8 respiram pelo peito e culpam o ouvido." Se ela não tiver contado, marcar [LASTRO: confirmar com o dono] e não publicar até confirmar.

  - filtro: Validador de conversão
    dimensao: critério 2, dor verdadeira · gravidade 8
    trecho: "cantam errado e nem sabem"
    motivo: dor anônima, sem cena; ninguém se reconhece em "errado".
    sugestao: molde de dor comprimido: a nota que cai no fim da frase do hino, com o coral inteiro ouvindo.

suspenso pela cascata: Estrutura-mãe e filtro 4 não rodaram, Verbatim só na extração; o padrão 9, número redondo, volta na reescrita
```

O arquivo do lote fecha uma vez, depois da última peça, com a pergunta e o bordão de
`validador-conversao-reescrita.md`.

**O que mudou neste lote com o filtro 6.** Na versão sem ele, a peça 2 reprovava só pelo lint e a
peça 4 só pelo número sem fonte (corrigível). Com ele, as duas caem no critério 1: a capa e a headline
eram genéricas, e trocar só o verbo ou só o número deixaria as duas genéricas. A peça 4 sobe pra
bloqueante porque headline carrega o filtro 6 bloqueante na tabela de peso. As peças 1, 3 e 5 passaram
no filtro 6 sem mudança de veredito.

---

## Um tipo fora da lista, como a skill encaixou

Pedido fictício: "critica o texto que vai atrás da embalagem do meu método impresso".

`embalagem` não está na lista fechada de tipos. A skill não recusou. Encaixe declarado no topo do
veredito:

```
tipo: tratado como `corpo` (texto longo, lido de uma vez, sem rolagem)
```

E os 6 filtros rodaram com o peso do `corpo`: Estrutura-mãe e anti-IA lexical dobrados, e o filtro 6
como corrigível, porque texto de embalagem acompanha um produto já comprado e não pede compra.

---

## Quando o teto de 3 rodadas estourou

Numa legenda de outra semana do mesmo caso fictício, a peça reprovou 3 vezes seguidas no mesmo ponto
(U de Inacreditável no CUB e, no filtro 6, critério 4 com prazo sem lastro). A skill parou de sugerir
reescrita e escalou:

> "Essa peça reprovou 3 vezes no mesmo ponto. As três versões prometem afinação em 30 dias e
> nenhuma traz prova do lado. Olha as falhas e decide: você tem um caso com número que possa entrar
> aqui, ou a promessa precisa descer pra o que você consegue provar hoje?"
