# Receita: preço em degraus (o valor cheio cai até o da oferta)

Use quando o roteiro derruba o preço por etapas: um valor cheio, a parcela, o à vista e, às vezes, o valor por dia. Vale pra um slide só ou pra uma sequência curta. Desenhe você mesmo no HTML do slide, com o contrato de `receitas-visuais.md`; a regra de oferta do guia (parcela manchete, à vista menor, total parcelado fora) vale inteira.

## Só o que o roteiro traz

- Cada degrau é um valor que o roteiro escreveu, com o rótulo dele. **Nenhum valor intermediário que o roteiro não traga.** Dois valores no roteiro, dois degraus: o riscado e o de chegada. Não crie degrau pra a queda parecer maior.
- O motivo da queda é do dono. Sem a frase do motivo, o slide não ganha uma: o motivo vira pergunta em "Falta você responder" e a nota marca [A CONFIRMAR: motivo].
- Sem o valor cheio ou sem a parcela no roteiro, a receita não entra: só os nomes (`receita-pilha-de-nomes.md`) e a pergunta do preço.

## O desenho, de cima pra baixo

1. **O valor cheio**, médio (até uns 130px), com o rótulo do roteiro ao lado ("De"). Ele já está na tela quando o slide abre.
2. **O risco por clique.** O traço inclinado na cor reservada entra no clique e não esconde o número.
3. **A seta** pro degrau seguinte, que entra junto com a parcela.
4. **A parcela, manchete** (150 a 220px), com o rótulo do roteiro ("Por"). O à vista vem logo abaixo, bem menor (uns 90px). O total parcelado nunca aparece.
5. **O valor por dia**, se o roteiro o traz, no slide seguinte (abaixo).

Um elemento domina: a parcela. O valor cheio fica menor que ela, mesmo riscado.

## Risco por clique: o wrapper sobreposto

A receita `.risco` comum põe o texto dentro do elemento que revela, e o preço antigo some até o clique. Pra riscar só a linha, o texto fica fora do elemento com `data-click`, e o wrapper do traço vai por cima, em posição absoluta:

```html
<span class="risco">
  <span class="velho">{{VALOR_CHEIO}}</span>
  <span class="risco-over" data-click="1" data-fx="riscar">
    <span class="risco-wrap"><span class="risco-rot"><span class="risco-linha"></span></span></span>
  </span>
</span>
```

```css
.risco-over { position: absolute; inset: 0; }   /* cobre o número; .risco já é relative e inline-block */
```

Regras que fizeram funcionar: o `data-click` fica no wrapper, nunca no número; o wrapper não leva `opacity` nem `transform` próprios (o traço é o que gira, dentro de `.risco-rot`); o clique do risco pode ser o mesmo da parcela, e a seta e a parcela entram em outros elementos com o mesmo número de clique.

## O valor por dia (divisão por 30)

Quando o roteiro divide a parcela por 30 ("por dia"), o slide é próprio, com o `numero-calendario`: 30 casas sem numeral dentro e uma acesa, o valor por dia em número grande com o rótulo do roteiro. Vale o 30 que o roteiro traz; sem ele, calendário sem contagem de casas (`receitas-visuais.md`, "Proporção e ritmo"). A conta do valor por dia é a do roteiro; o conferidor de fontes reprova um "por dia" que não bata com a parcela dividida por 30.

## Antes de dar por pronto

- Todo valor da tela está no roteiro, com o rótulo dele; à vista menor que a parcela.
- O risco entra no clique e o número fica legível depois dele.
- Slide anotado no `_operador.md` como metáfora sua se a seta ou o calendário não vieram do roteiro.
