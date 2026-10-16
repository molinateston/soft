# Visual editorial do reel

Esta folha é copiada para cada projeto. Ela diz como o reel deve parecer; o SKILL.md diz como montar.

## O visual em uma frase

Vídeo falado direto pra câmera que se mostra editado: calmo, polido, com cara de revista. Uma palavra minúscula por vez numa sans neogrotesca no meio do quadro; as palavras que carregam o sentido trocam para um serifado itálico na cor de acento do dono. Cortes secos entre ângulos e punch-ins a cada frase ou duas. Cartões arredondados flutuando, explosão de miniaturas, faixa de filme, parede de grade, nota manuscrita com seta desenhada e pequenos momentos de interface (uma barra de texto que muda o estilo de uma frase). Cada visual ilustra as palavras exatas que estão sendo ditas e sai dentro da mesma frase.

## Cores

| Uso | Cor |
|---|---|
| Texto sans, notas manuscritas | `#ffffff` |
| Palavras no serifado (a voz do destaque) | `var(--acento)`, a `cor_acento` do `perfil.json`; sem perfil, `#ffffff` |
| Cartão escuro | `#0d0d0d` |
| Papel da parede de grade, atrás das miniaturas | `#f2ede6` |
| Sombra do texto | `0 3px 22px rgba(0,0,0,.30)` |
| Sombra do cartão | `0 24px 60px rgba(0,0,0,.38)` |

Se a cor de acento do dono for muito saturada, o serifado grande pesa. Ofereça ao dono um tom mais pálido da mesma cor e registre a escolha dele no relatório.

## Tipografia

- **Sans:** Inter SemiBold (ou a `fonte_texto` do dono), minúscula, espaçamento `-0.035em`. Legenda 92 px, linhas de pilha 84 px (as em serifado, 112 px), apartes 42 px.
- **Serifado do destaque:** Instrument Serif Italic (ou a `fonte_destaque` do dono), 124 a 132 px.
- **Manuscrita:** Caveat Bold, notas em 86 px.

## O que não fazer

- Contorno preto na legenda, caixa ou faixa escura atrás das palavras.
- Mais de uma palavra no serifado por frase, mais ou menos: o destaque perde o sentido.
- Elemento cobrindo o rosto. Cartões ficam ao lado ou acima da cabeça.
- Quique no texto. Só as miniaturas entram com `back.out`.
- Cor fora da identidade do dono.
