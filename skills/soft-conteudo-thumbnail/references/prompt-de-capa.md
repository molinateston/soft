# Prompt de capa, o guia completo da imagem de thumbnail

> Profundidade do Passo 4 da skill. O fluxo no SKILL.md é autossuficiente pra 90% dos casos; leia isto quando o prompt não sai como pedido, quando for a variante vertical (Shorts), ou quando for renderizar no `imagegen` local em vez de mandar o dono colar no gerador dele. A ARTE final é da **soft-designer**; aqui está o CONTEÚDO do prompt que ela (ou o dono) usa.

## Índice

- 1. A lei-mãe: texto por overlay, nunca dentro da imagem
- 2. Anatomia do prompt de capa (as 5 seções)
- 3. O rosto: como pedir a expressão certa por tom emocional
- 4. Os moldes de prompt por tom (choque, curioso, confiante, tensão)
- 5. A variante 9:16 (Shorts / reel de capa)
- 6. Integração com o imagegen local (Claude Code / agente)
- 7. A foto de referência: o que faz e o que não faz
- 8. Consistência de canal: a família de capa
- 9. Erros de gerador e como corrigir
- 10. A fronteira com a soft-designer (quem faz o quê)

---

## 1. A lei-mãe: texto por overlay, nunca dentro da imagem

Regra dura de qualquer arte-imagem do ecossistema (vale igual pro deck animado e pro infográfico-lousa da soft-designer): **o prompt NUNCA pede o texto do gancho dentro da imagem gerada.** O gerador desenha só o cenário (rosto + fundo + elemento focal), com uma ÁREA LIMPA reservada; o gancho de 3-5 palavras entra DEPOIS, por cima, como overlay de HTML/CSS ou camada de edição.

Por quê:
- **Editável.** Trocar "Vendi sem reunião" por "Fechei sem call" não obriga a regenerar a imagem inteira (que muda o rosto, a luz, tudo). Só troca a camada de texto.
- **Legível.** Gerador de imagem escreve texto torto, com letra inventada, kerning quebrado. Overlay de fonte real (a fonte da marca do dono) sai nítido e na tipografia certa.
- **Contável.** O teto de 3-5 palavras e o teste de legibilidade a 320px só valem se o texto é uma camada controlada, não pixels chutados pelo modelo.

Consequência prática no prompt: sempre inclua *"NÃO escreva NENHUM texto na imagem"* + *"deixe uma área limpa em [lado] pra o texto entrar depois"*. Se o dono cola no gerador dele e não tem como fazer overlay, aí sim o gerador escreve o texto (2ª escolha), mas avise que a copy fica não editável e a legibilidade cai.

## 2. Anatomia do prompt de capa (as 5 seções)

Todo prompt de capa tem estas 5 seções, nesta ordem:

1. **Abertura + proporção.** "Usando a foto de referência do dono em anexo, gere uma imagem de fundo de thumbnail em 1280x720 (16:9)." A palavra "fundo" reforça a lei 1 (é cenário, não a peça final com texto).
2. **Composição (o rosto).** Posição (esquerda/direita/centro), % do quadro (30-50), expressão, direção do olhar. É a parte que mais decide o CTR.
3. **Cenário.** Fundo (hex + tratamento) e elemento focal (objeto/número/seta). O elemento focal dá o assunto num relance.
4. **Paleta.** Primária (marca do dono) + destaque de alto contraste. Duas cores dominam; o resto é ruído.
5. **Restrições.** Sem texto na imagem; área limpa reservada; rosto nítido; alto contraste; zona-limpa do selo (canto inferior direito); sem UI do YouTube, sem marca d'água.

Nunca coloque o CAMINHO da foto dentro do prompt. A foto vai ANEXADA no gerador; o prompt só a referencia como "a foto em anexo".

## 3. O rosto: como pedir a expressão certa por tom emocional

A expressão é o que carrega a emoção da capa. Peça em termos FÍSICOS concretos (olhos, boca, sobrancelha, mão), nunca em rótulo abstrato ("pareça surpreso" sai fraco; "olhos arregalados, boca entreaberta, sobrancelhas levantadas" sai forte).

| Tom | Descrição física pro prompt | Direção do olhar |
|---|---|---|
| **Choque/surpresa** | olhos arregalados, boca entreaberta, sobrancelhas levantadas, mão perto do rosto | direto na câmera (o choque é com o espectador) |
| **Curioso/pensativo** | uma sobrancelha erguida, meio sorriso de canto, queixo levemente pra cima | fora do quadro, na direção do texto (guia o olho pro gancho) |
| **Confiante/direto** | queixo firme, meio sorriso fechado, ombros pra trás, braços cruzados | direto na câmera (autoridade) |
| **Tensão/opinião forte** | testa levemente franzida, olhar intenso, gesto de mão apontando ou palma aberta | direto na câmera (confronto) |

O tom não é escolha de estética: casa com a dor/desejo do avatar. Vídeo que quebra crença pede choque; vídeo de método pede confiança.

## 4. Os moldes de prompt por tom

Preencha os `[...]` com o que saiu do briefing. Os 4 moldes são o esqueleto; adapte ao cenário do vídeo.

**Choque/surpresa:**
```
Usando a foto de referência do dono em anexo, gere uma imagem de fundo de thumbnail em 1280x720 (16:9).
Composição: dono à direita ocupando ~45% do quadro, olhos arregalados, boca entreaberta, sobrancelhas levantadas, olhar direto na câmera.
Cenário: fundo [hex] com gradiente radial mais claro atrás do rosto; elemento focal [objeto/número] grande e desfocado no lado esquerdo.
Paleta: primária [hex marca], destaque vermelho de alto contraste.
Restrições: NÃO escreva texto na imagem; deixe o terço esquerdo limpo pro texto entrar depois; rosto nítido; alto contraste; canto inferior direito limpo; sem UI do YouTube, sem marca d'água.
```

**Curioso/pensativo:**
```
[...] Composição: dono à esquerda ~40% do quadro, uma sobrancelha erguida, meio sorriso de canto, olhar pra fora do quadro no lado direito (na direção do texto).
Cenário: fundo [hex] chapado ou cena desfocada; elemento focal [seta/objeto] apontando pra onde o olhar vai.
Paleta: primária [hex marca], destaque ciano.
Restrições: [...] deixe o terço direito limpo pro texto; [...]
```

**Confiante/direto:**
```
[...] Composição: dono ao centro-direita ~40% do quadro, braços cruzados, meio sorriso fechado, olhar firme na câmera.
Cenário: fundo [hex] escuro com leve gradiente; elemento focal [número/logo] atrás do ombro.
Paleta: primária [hex marca], destaque amarelo.
Restrições: [...] deixe o lado esquerdo limpo pro texto; [...]
```

**Tensão/opinião forte:**
```
[...] Composição: dono ao centro ~45% do quadro, testa levemente franzida, olhar intenso na câmera, mão aberta apontando pra frente.
Cenário: fundo [hex] com vinheta escura nas bordas; elemento focal [objeto do tema].
Paleta: primária [hex marca], destaque vermelho ou laranja.
Restrições: [...] deixe o topo limpo pro texto; [...]
```

## 5. A variante 9:16 (Shorts / reel de capa)

Shorts e reels usam capa vertical 1080x1920. As diferenças no prompt:
- **Proporção:** 1080x1920 (9:16).
- **Zona útil:** o terço de baixo some atrás da UI (título, botões, legenda). Rosto e texto vão na METADE DE CIMA. O elemento focal pode ocupar o meio.
- **Rosto:** pode ocupar mais do quadro (40-55%), o vertical dá menos largura.
- **Texto:** ainda 3-5 palavras, mas empilhado em 2-3 linhas curtas cabe melhor no vertical.
- **Área limpa:** reserve o topo (pra o texto) e conte que a UI come a base; nada importante nos últimos ~25% de baixo.

Tudo mais (lei do overlay, expressão física, paleta de 2 cores) é igual.

## 6. Integração com o imagegen local (Claude Code / agente)

No Claude Code e no agente/Telegram (que têm Bash), a **soft-designer** pode renderizar a capa chamando o `imagegen` local (gpt-image, aceita foto de referência) em vez de mandar o dono colar no gerador dele. O fluxo:

1. Esta skill entrega o briefing + o prompt (com a lei do overlay) e faz o handoff.
2. A soft-designer chama o `imagegen` com a foto de referência anexada como input e o prompt do cenário (sem texto).
3. A soft-designer aplica o gancho de 3-5 palavras por overlay (HTML/CSS na fonte da marca, exportado por cima da imagem, ou camada de composição).
4. Exporta o PNG final e devolve **o path completo na resposta** (regra do ambiente agente/Telegram).

Não amarre em nenhum gerador de marca específica no prompt: ele é neutro ("cole no seu gerador de imagem"). No Code, o motor é o `imagegen` local. O prompt funciona igual nos dois porque a lei do overlay tira a dependência de o gerador saber escrever texto.

## 7. A foto de referência: o que faz e o que não faz

**Faz:** dá ao gerador o rosto real do dono pra a capa parecer ele (reconhecimento). Uma foto boa (rosto nítido, luz frontal, expressão neutra-forte) rende dezenas de capas com expressões variadas.

**Não faz:** não é a capa pronta. O gerador usa a foto como referência de identidade, mas recompõe a expressão, a luz e o fundo conforme o prompt. Por isso a foto ideal é neutra e nítida (matéria-prima), não uma foto já muito estilizada.

Regras:
- Nunca coloque o CAMINHO da foto dentro do texto do prompt. Ela vai anexada no gerador.
- Sem foto, o prompt sai genérico (rosto inventado) e perde a marca do canal. Peça a foto no Passo 0 antes de gerar.
- Uma única foto de referência boa mantém a consistência: reuse a mesma entre vídeos, variando só a expressão pedida no prompt.

## 8. Consistência de canal: a família de capa

O reconhecimento do canal vem de a capa ser SEMPRE da mesma família: mesmo enquadramento aproximado, mesma fonte do overlay (a da marca), mesmo tratamento de cor (a paleta da marca + 1 destaque), mesma posição típica do rosto. O espectador reconhece o canal na grade de miniaturas antes de ler o título.

Quando o dono já tem capas anteriores, olhe o padrão e MANTENHA a família (mesma fonte, mesma zona de cor). Uma capa que foge da família confunde e perde o reconhecimento. Isso NÃO significa capa igual: o gancho e a expressão mudam a cada vídeo; a MOLDURA (fonte, cor, enquadramento) é que se mantém.

## 9. Erros de gerador e como corrigir

| Sintoma da imagem | Correção no prompt |
|---|---|
| Gerou texto torto/inventado na imagem | Reforce "NÃO escreva NENHUM texto na imagem, nem uma letra"; o texto é overlay |
| Rosto não parece o dono | Foto de referência melhor (mais nítida, frontal); reforce "mantenha os traços da foto em anexo" |
| Rosto pequeno demais | Peça "% do quadro" explícito (35-50%) e "close no rosto e ombros" |
| Fundo poluído, muitas cores | Reforce "apenas 2 cores dominantes: [marca] e [destaque]; fundo simples" |
| Baixo contraste (some na miniatura) | Peça "alto contraste entre rosto e fundo; borda/glow sutil separando o rosto do fundo" |
| Elemento focal roubou a cena do rosto | Peça o elemento "desfocado, secundário, menor que o rosto" |
| Área do texto não ficou limpa | Reforce "deixe o [terço/lado] completamente limpo, sem elementos, pro texto entrar depois" |

## 10. A fronteira com a soft-designer (quem faz o quê)

- **Esta skill (soft-conteudo-thumbnail):** decide a capa, escreve o gancho gated, monta o briefing + o prompt do cenário. É o CÉREBRO da capa.
- **soft-designer (branch de imagem-IA, §8):** RENDERIZA. Chama o `imagegen`, aplica o overlay de texto, exporta o PNG, devolve o path. É o MOTOR do render.
- **soft-conteudo-reels:** escreve o ROTEIRO do vídeo (depois da capa, thumbnail-first).

O handoff é explícito: esta skill termina entregando o prompt e dizendo "passo pra soft-designer renderizar / você cola no seu gerador". Nunca tente renderizar a arte final aqui; nunca deixe a soft-designer decidir o gancho (ela recebe o gancho já gated).
