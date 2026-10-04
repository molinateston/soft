# Notas do apresentador

A tela fala com todo mundo; a nota ajuda quem apresenta. A fala do roteiro vai pra nota, nunca pra tela.

## A sequência de cada nota

1. **Objetivo:** o que o slide faz, em uma linha.
2. **Abre com:** a primeira frase.
3. **Clique 1, Clique 2...:** o que se diz em cada entrada, uma linha por clique da tela, na ordem.
4. **Fecha com:** a última frase, já apontando o slide seguinte.
5. **Hora-meta:** nos pontos de controle ("[hora]: começa a oferta").
6. **Pode pular:** nos slides que dão folga quando a aula atrasa.

Também moram na nota:
- **Por público:** a resposta pra quem ainda não faz, quem está começando, quem já é aluno. Sai da tela porque a tela fala com todos.
- **[A CONFIRMAR: o quê]:** o que ainda não é fato. Quem apresenta só fala o que está confirmado.
- **Histórico:** "Mudou ([data], pedido de [quem])" e "Saiu da tela: [o quê]". Ninguém desfaz uma decisão sem saber por que ela foi tomada.

## No slide desenhado

A nota mora no próprio slide, dentro do `<aside class="notes">`, uma linha por campo, nesta ordem. O `ler_roteiro.py --esqueleto` já escreve a nota de cada slide com a fala do roteiro; você ajusta os cliques ao desenho. Mudou um clique ou a repartição? Edite o `roteiro.md` e a nota do HTML do slide, nos dois (o `conferir_fala.py` lê o `roteiro.md`, o checador lê a nota), e rode o `conferir_fala.py`; regravar o esqueleto apagaria o desenho.

```html
<aside class="notes">Objetivo: [o que o slide faz]
Abre com: [primeira frase, da FALA do roteiro]
Clique 1: [fala do clique 1]
Fecha com: [última frase, apontando o slide seguinte]
Transição: [a TRANSIÇÃO do roteiro, quando existe]
Hora-meta: [hora do dono]: [marco]
[A CONFIRMAR: o dado que falta]
Saiu da tela: [o quê]</aside>
```

O número de linhas "Clique N" é o número de cliques do desenho. No rascunho de texto, os mesmos campos vão no `notas` do `deck.json` (`references/receitas-e-layouts.md`).

## De onde vem cada linha

- Roteiro com FALA, Abre com, Clique N, Fecha com e TRANSIÇÃO: copie a fala; a TRANSIÇÃO vira o "Fecha com" quando o slide não traz um (o esqueleto faz isso) e, quando traz, vai no campo `Transição:`. A conclusão que é a última frase falada e também um clique: o Clique N a diz e o "Fecha com" é "a mesma frase, sem pausa".
- Tela que traz mais que a fala, ou roteiro só com tela: "Abre com: lê a frase da tela" (assim, sem colchete); nos cliques sem fala, "Clique N: lê a frase da tela". Nada de fala nova inventada; o `conferir_fala.py` ignora essas linhas e também a TRANSIÇÃO toda entre parênteses, direção de palco como "(segue direto pra garantia)": ela vai em `Transição:` e não vira "Fecha com".
- Só tópicos: objetivo e abre com saem do tópico; o resto fica como [A CONFIRMAR: fala deste slide].
- Slide dividido (passo Dividir): a fala do original é repartida pelos slides novos, na ordem, sem mudar palavra, e a origem (`slide N do original, dividido em K`) vai num comentário `<!-- Origem: ... -->` do roteiro, nunca na nota (senão vira "Obs.: Origem" no `notas.md` e no PPTX). Slide cuja fala é uma frase só: "Abre com" é a frase inteira e "Fecha com: a mesma frase, sem pausa" (o checador só exige que os dois campos existam). Lista repartida: o Clique 1 é o primeiro item e o Abre com é a frase de abertura ou "a mesma frase, sem pausa" (`dividir-o-roteiro.md`, regra 4).
- Hora-meta, pode pular e por público só com dado do insumo (duração da aula, agenda, perfil do público).

## O que o script confere

- Toda nota tem Objetivo, Abre com e Fecha com.
- O número de "Clique N" bate com os cliques da tela.
- Nenhum travessão.
- O `notas.md` (tela e fala de cada slide) passa no `lint_copy.py` e no `conferir_fontes.py`.
