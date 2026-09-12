# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** As peças, os números, o nome do método e o resultado foram
> inventados só pra mostrar a FORMA do veredito. Nada disso é caso real e nada disso pode ser
> copiado pra uma entrega de verdade.

**O caso fictício:** uma professora de canto que dá aulas online e vende um curso de 12 semanas de
técnica vocal pra quem canta em coral de igreja. Tese declarada por ela: "quem canta desafinado não
tem ouvido ruim, tem apoio de respiração errado". Oferta: curso de 12 semanas, 697 reais.

Este arquivo mostra três auditorias na ordem: uma headline reprovada, a mesma headline aprovada
depois da correção, e um lote de 5 peças com o consolidado no topo.

---

## Auditoria 1 · Uma headline, REPROVADA

### O que entrou

```
peça: "Descubra o segredo que vai reinventar a sua voz e transformar a sua confiança no palco."
tipo: headline
tese declarada: quem canta desafinado tem apoio de respiração errado, não ouvido ruim
oferta declarada: curso de 12 semanas, 697
material de lastro: nenhum caminho informado
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

Passo 3, leitura pelo sentido. Passo 4, leitura pela forma.

### O veredito, como saiu em `veredito-copy-headline-canto.md`

```
peça: "Descubra o segredo que vai reinventar a sua voz..."
tipo: headline
veredito: REPROVADA
severidade: 2 corrigíveis, 1 observação
falhas:
  - filtro: anti-IA lexical
    dimensao: 3 avisos diferentes na mesma peça
    trecho: "o segredo que vai reinventar ... e transformar"
    motivo: frase-emoldura de revelação somada a dois verbos genéricos é o desenho padrão de copy de máquina.
    sugestao: tirar os três e nomear o que acontece de concreto com a voz da pessoa.

  - filtro: CUB
    dimensao: B de Boring
    trecho: "transformar a sua confiança no palco"
    motivo: promessa que qualquer curso de canto do país já fez, não separa esta professora de nenhuma outra.
    sugestao: "Você não canta desafinado por causa do ouvido. É o ar que acaba antes da frase."

  - filtro: Verbatim
    dimensao: afirmação grande sem lastro
    trecho: "reinventar a sua voz"
    motivo: nenhuma fonte informada sustenta mudança de voz, e a tese declarada fala de respiração.
    sugestao: ancorar na tese que a dona já declarou, ou marcar [LASTRO: confirmar com o dono].
```

Observação registrada no rodapé: o filtro 4 achou 1 padrão só (o 4, adjetivo em par não, na verdade
o 8, escalada de três tempos), e 1 padrão sozinho aponta sem reprovar.

---

## Auditoria 2 · A mesma headline depois da correção, APROVADA

### O que entrou na segunda rodada

```
peça: "Você não canta desafinado por causa do ouvido. É o ar que acaba antes da frase terminar."
tipo: headline
```

### O que a skill rodou

Filtro 3: exit 0, zero aviso. Filtro 1: passa nas 3 dimensões, a frase vira imagem na primeira
leitura e ninguém do nicho já ouviu essa. Filtro 2: headline comprime, e a peça entrega Diagnóstico
e Nova interpretação na mesma linha, que é o mínimo pro formato. Filtro 4: zero padrão. Filtro 5:
ancorada na tese que a dona declarou.

### O veredito

```
peça: "Você não canta desafinado por causa do ouvido..."
tipo: headline
veredito: APROVADA
resumo: renomeia a causa em uma linha, e a promessa nasce da tese que a dona já sustenta.
```

---

## Auditoria 3 · Um lote de 5 peças, em série

Entrada: 5 legendas de post pra semana, mandadas de uma vez. As 5 foram lidas UMA POR VEZ, cada uma
com as duas passadas, e o consolidado saiu só depois da quinta.

### `veredito-copy-lote-semana-03.md`, o topo do arquivo

```
lote: legendas semana 03  ·  5 peças  ·  2 aprovadas  ·  3 reprovadas
severidade: 1 bloqueante · 2 corrigíveis · 2 observações
```

### O resumo por peça, como saiu

| Peça | Tipo | Veredito | Filtro que quebrou | Severidade |
|---|---|---|---|---|
| 1, "o ar acaba antes da frase" | corpo | APROVADA | nenhum | observação, 1 padrão estrutural |
| 2, "3 erros que prendem sua voz" | capa | REPROVADA | anti-IA lexical, falha dura | bloqueante |
| 3, "coral inteiro afina junto" | corpo | REPROVADA | Estrutura-mãe, pulou Nomeação | corrigível |
| 4, "87% das pessoas cantam errado" | headline | REPROVADA | Verbatim, número sem fonte | corrigível |
| 5, "o que eu faço antes de cantar" | script_reel | APROVADA | nenhum | observação, hedge isolado |

### A falha bloqueante, por extenso

```
peça 2: "3 erros que prendem a sua voz"
tipo: capa
veredito: REPROVADA
severidade: bloqueante
falhas:
  - filtro: anti-IA lexical
    dimensao: falha dura, o verbo-freio banido no meio da frase
    trecho: o verbo que a régua anti-voz proíbe, na terceira palavra da capa
    motivo: o lint saiu com exit 1. Falha dura não sai do jeito que está, sem discussão.
    sugestao: "3 erros que fazem o ar acabar no meio da frase."
```

### A falha de lastro, por extenso

```
peça 4: "87% das pessoas cantam errado e nem sabem"
tipo: headline
veredito: REPROVADA
severidade: corrigível
falhas:
  - filtro: Verbatim
    dimensao: número redondo sem fonte
    trecho: "87%"
    motivo: nenhuma fonte do material da dona traz esse número, e o filtro 4 marca o mesmo trecho no padrão 9.
    sugestao: trocar pelo que ela pode provar: "de cada 10 alunas que chegam aqui, 8 respiram pelo peito." Se ela não tiver contado, marcar [LASTRO: confirmar com o dono] e não publicar até confirmar.
```

---

## Um tipo fora da lista, como a skill encaixou

Pedido fictício: "critica o texto que vai atrás da embalagem do meu método impresso".

`embalagem` não está na lista fechada de tipos. A skill não recusou. Encaixe declarado no topo do
veredito:

```
tipo: tratado como `corpo` (texto longo, lido de uma vez, sem rolagem)
```

E os 5 filtros rodaram com o peso do `corpo`: Estrutura-mãe e anti-IA lexical dobrados.

---

## Quando o teto de 3 rodadas estourou

Numa quarta peça do mesmo lote fictício, a legenda reprovou 3 vezes seguidas no mesmo filtro (CUB,
dimensão U). A skill parou de sugerir reescrita e escalou:

> "Essa peça reprovou 3 vezes no U de Inacreditável. As três versões prometem afinação em 30 dias e
> nenhuma traz prova do lado. Olha as falhas e decide: você tem um caso com número que possa entrar
> aqui, ou a promessa precisa descer pra o que você consegue provar hoje?"
