---
name: soft-tweet-card
description: Criar e revisar carrosséis verticais no formato print de tweet aprovado do Leo Molina, com repertório de frames, identidade dark/light e travas visuais. Usar em qualquer pedido de card, post ou carrossel “estilo tweet”, “print de tweet” ou comparação de motores nesse formato.
---

# Cards estilo tweet

Aplicar a receita aprovada em 13/08/2026 sem inventar outro sistema visual.

## Fluxo

1. Ler `references/receita-canonica.md` por inteiro antes de escolher frames.
2. Ler a copy fonte sem reescrever fatos, números, CTA ou ordem dos slides.
3. Escolher de 5 a 8 tipos de frame para formar o arco abrir → tensionar → provar → fechar. Repetir tipos ao longo de 9 slides é permitido; nunca usar o mesmo tipo em sequência.
4. Montar cada card em 1080×1350, preservando a anatomia de tweet.
5. Gerar as versões escura e clara da peça. Quando a tarefa pedir uma comparação isolada em apenas uma versão, manter a outra preparada e declarar a limitação.
6. Produzir mosaico e conferir visualmente antes de aceitar os cards individuais.
7. Rodar o verificador executável. Qualquer falha reprova a entrega.

## Travas inegociáveis

- Usar avatar real redondo, nome `Léo Molina` (com acento, sempre — `Leo` sem acento reprova), selo azul `#1D9BF0` e `@instadoleomolina`.
- NUNCA Bebas Neue. A fonte é a de tweet (`-apple-system`/Inter), texto tranquilo. Renderizar pelo `build_tweet_cards.py`, nunca soltar o motor pra desenhar o card livre — foi assim que o Bebas e o nome errado vazaram.
- Manter o selo azul; nunca verde.
- Aplicar verde apenas à palavra-chave; frase inteira verde reprova.
- Não numerar o card. A regra específica do formato tweet prevalece sobre qualquer identidade genérica que peça indicador N/total.
- Evitar palavra órfã na última linha e impedir quebra entre `R$` e o número.
- Não fabricar depoimento, conversa, print ou fala atribuída.
- Usar número apenas quando validado na fonte.
- Não publicar automaticamente.

## Recursos

- Ler `references/receita-canonica.md` para cores, frames e critérios.
- Usar `scripts/build_tweet_cards.py` como implementação de referência para carrosséis.
- Usar `scripts/build_frames.py` como biblioteca de frames escuros e claros.
- Rodar `scripts/verify_tweet_cards.py PASTA 9` para conferir quantidade, dimensões e arquivos vazios.
- Comparar com `/home/cloud/trabalho/conteudo/2026-08/2026-08-13-carrosseis-banco-modelagem/render-tweet/01-imobiliaria-24h/_mosaico.png` como exemplo aprovado.

## Critério de pronto

Aceitar somente quando houver todos os cards esperados e o mosaico, cada card medir exatamente 1080×1350, o verificador terminar sem falhas e a inspeção do mosaico provar: anatomia de tweet, selo azul, verde seletivo, ausência de numeração, variação de frames e copy fiel.
