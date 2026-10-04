# Receita: trilho de garantia (três cartões ligados)

Use quando o roteiro traz uma garantia em etapas e a aula não tem esquema principal (nenhuma escada nem bússola) pra mostrar a volta. Com esquema principal, a garantia usa o dele (`esquema-principal-reusado.md`). Desenhe você mesmo no HTML do slide, com o contrato de `receitas-visuais.md`.

## O desenho

- **Três cartões em fileira, ligados por um trilho.** Cada cartão é uma etapa da garantia, na ordem da fala, com a frase curta do roteiro em 42px ou mais. O trilho é uma linha grossa (8 a 10px) na cor `var(--linha)` que passa atrás dos cartões; o nó de cada etapa fica no encontro do trilho com o cartão.
- **Um cartão por clique**, na ordem da fala. O primeiro nó é cheio e o seguinte pode ser vazado (borda na cor de destaque) quando a etapa só vale se a anterior falhar: a forma mostra a relação que a fala já diz.
- **Prazo como barra, só se o roteiro traz.** Uma barra de largura proporcional ao prazo do roteiro, com o mesmo comprimento por unidade em todos os cartões. Sem prazo escrito, sem barra.
- **Menos de três etapas no roteiro**: faça dois cartões e pare aí. **Mais de três**: dois slides, com a fileira continuando (os cartões anteriores ficam na tela, apagados e sem clique).

## Só o que o roteiro traz

- Nome, prazo e condição de cada etapa são do roteiro, com o mesmo rótulo. Nada de selo, percentual ou "garantia total" que ele não disse.
- A frase de risco ("eu assumo o risco") vai na fala e na nota; na tela só entra se o roteiro a pôs na tela.
- Condição que o roteiro não traz (o que o aluno precisa cumprir) vira pergunta em "Falta você responder", nunca texto de tela.

## Antes de dar por pronto

- Cliques batem com as linhas "Clique N" da nota, até 7.
- Cartões com 42px ou mais; nada encostado na borda; o trilho não cobre o texto.
- Slide anotado no `_operador.md` como metáfora sua (o trilho), com a ideia da fala que ele ilustra, em palavras suas.
