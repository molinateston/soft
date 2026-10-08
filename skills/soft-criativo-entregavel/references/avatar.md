# Avatar no FLUX 3 (Higgsfield)

O avatar fala o gancho (com o alívio) e, se a configuração pedir, o CTA. É um clipe só, gerado uma vez, que o script `montar_base.py` confere e corta.

## Conteúdo
1. Definir a pessoa e o cenário
2. Duração
3. O prompt
4. Parâmetros e geração
5. Quando sai errado
6. O que o script faz com o clipe
7. O que já deu errado (histórico)

## 1. Definir a pessoa e o cenário

Não pergunte ao usuário; decida pela oferta e pelo áudio:

- **Gênero:** o da voz do áudio (`analisar_audio.py` diz). A pessoa fala em primeira pessoa; a voz do avatar e a do áudio são diferentes, mas precisam ser do mesmo gênero. Se der "incerto", procure marcas no texto ("cansada", "obrigado") e, sem isso, pergunte.
- **Idade e perfil:** quem compraria e recomendaria esse produto a um amigo. Leia a copy: a dor, o tom, o público. Oferta de espiritualidade e calma pede alguém sereno, de 40 a 55; oferta para mães, uma mãe; oferta de produtividade, alguém de escritório em casa.
- **Cenário:** casa de verdade, arrumada, com luz de janela, condizente com o tema (estante e planta para estudo; cozinha clara para receita). Não precisa ser feio para parecer UGC; precisa parecer gravado pelo celular.
- **Nada na frente do corpo.** No gancho o avatar é recortado do fundo e posto sobre o material. Mesa, livro aberto ou caneca entre ele e a câmera escondem parte do corpo, e o recorte fica com o tronco cortado em linha reta. Braço estendido atravessando o quadro também atrapalha. Peça um selfie próximo, com o rosto grande e na metade de cima do quadro ("close selfie framing, his head in the upper half of the frame, shoulders filling the width"), com a mesa e os objetos **ao lado ou atrás** dele ("a bookshelf and a small table behind him"), nunca "on the table in front of him".
- **Roupa:** simples, cuidada, cor que conversa com a paleta da oferta sem virar uniforme.
- **Autoridade sem credencial:** postura composta, olhar atento, fala tranquila. Não invente profissão.
- **Tom: indicação.** O avatar é alguém do público contando para um conhecido uma coisa que está usando, num vídeo orgânico. Nunca vendedor, apresentador ou pessoa animada. Escreva no prompt quem ele é e para quem está falando ("a friend who is studying for the same Military Police exam"): isso dirige o tom melhor que adjetivos.
- **Linguajar do público.** As palavras do gancho têm que caber na boca dessa pessoa. Homem falando de concurso da PM: "Ô, se liga só", "olha só". "Gente" foi reprovado para avatar homem. Leia a oferta e pense em como esse público fala entre si.
- **Gancho que não é gancho.** Se a primeira frase do áudio é descritiva e não abre um vídeo ("Olha por dentro do Guia Ilustrado de Temas das Provas da PMPE."), adapte de leve o texto do avatar: uma chamada curta e a indicação ("Ô, se liga só. Olha esse guia ilustrado da prova da PMPE por dentro."). Não acrescente promessa que a copy não faz. Diga ao usuário qual foi a adaptação.

**Variedade na leva.** Planeje as cinco pessoas antes de escrever qualquer prompt. Trocar só a camisa não é variedade: mude formato de rosto, tom de pele, cabelo, idade, óculos, porte, roupa **e** cenário. Escreva a tabela e só então os prompts.

Para repetir a **mesma** pessoa em outro clipe (refação, ou gancho e CTA em clipes separados), a descrição em texto não garante: use um quadro do clipe anterior como imagem de referência (`start_image` ou `image_references`, depois de enviar a imagem com `media_upload`).

## 2. Duração

```
segundos = palavras do gancho e do CTA ÷ 2,7  +  1   (arredonde para cima; mínimo 5, máximo 20; sigla soletrada = 3 palavras)
```

Exemplos reais: 14 palavras com uma sigla → 6 s (aprovado, sobrou 0,4 s). 40 palavras → 16 s (AD 05, aprovado). 

**O modelo espalha a fala pelo clipe inteiro.** Em quatro clipes medidos (12, 6, 5 e 6 s) a fala terminou sempre nos últimos 0,4 s, qualquer que fosse a duração, e pedir "about 3 seconds" no prompt não mudou nada. Quem manda no ritmo é a conta palavras ÷ duração:

| Clipe | Palavras | Ritmo | Resultado |
|---|---|---|---|
| 12 s, gancho + CTA | 25 | 2,1 no gancho | reprovado: "falando muito lentamente, texto solto" |
| 5 s, só gancho | 12 + sigla | 2,5 | última palavra colada no fim do clipe |
| 6 s, só gancho | 14 + sigla | 2,8 | aprovado |

Por isso a duração é justa: folga grande dá fala arrastada, folga nenhuma corta a última palavra. Se o gancho sozinho for curto demais para 5 s (menos de ~11 palavras), alongue o texto com uma chamada de conversa em vez de deixar sobra. `montar_base.py` mostra o "ritmo do gancho" e marca LENTO abaixo de 2,3 palavras por segundo.

Se passar de 20 s, separe em dois clipes (gancho e CTA), o segundo com um quadro do primeiro como referência.

## 3. O prompt

Descrição visual e direção em **inglês**; a fala exata em **português**, entre aspas. Modelo:

```text
[PESSOA: nacionalidade, idade, pele, cabelo, rosto, óculos/barba se houver, roupa]. [CENÁRIO: onde está sentada, o que
aparece atrás, luz de janela]. Vertical smartphone selfie video, slight natural handheld movement.

A casual [N]-second vertical phone recording, as if [she/he] is sending a spontaneous video message to a friend
[QUEM É O AMIGO, ex.: who is studying for the same Military Police exam]. Relaxed shoulders, natural blinks and small
unplanned head movements.

[INTENÇÃO DA 1ª FRASE, ex.: He first calls his friend's attention, offhand, the way guys do / She quotes, in a flat
matter-of-fact way, a phrase she heard from someone]:
"[1ª FRASE]"

[INTENÇÃO DA 2ª FRASE, ex.: Then, right away, he passes along a tip about something he has been using / Right after,
as her own amused, slightly incredulous comment], in natural connected Brazilian Portuguese:
"[2ª FRASE]"

Then, in the same light conversational voice and volume, as if casually sharing something useful, clearly pointing
straight down with [her/his] index finger toward the bottom edge of the frame while [she/he] says "aqui embaixo":
"[CTA]"

Let the rhythm be organic and the words flow together, with understated expression and ordinary pitch variation.
Preserve the complete first word and finish the entire line, with a short breath after the last word.

No formal presenter delivery, exaggerated articulation, theatrical pauses or advertising tone.

Quiet room ambience, synchronized on-camera speech, ordinary window daylight and smartphone look. One continuous shot
without music, captions or text.
```

Como preencher:

- **Fala exata.** Copie as frases do áudio como foram ditas ("pro", "pra"). Não reescreva a copy. Se uma construção falhar duas vezes, ofereça ao usuário uma alternativa que preserve o sentido e use a que ele aprovar.
- **Intenção por frase, só o necessário.** A frase absurda costuma ser citação de outra pessoa ou provocação; o alívio é o comentário da própria pessoa; o CTA é uma dica entre amigos. Uma linha por frase basta. Empilhar instruções de pausa, sílaba e ênfase deixa a fala mais artificial, não menos.
- **Prompt curto.** O modelo acima é o que foi aprovado. Não acrescente tempos ("takes about 3 seconds", "mouth at rest for 0.3 seconds"), nem listas de proibições, nem direção de rosto ("neutral face", "steady eye contact", "eyebrows up", "excited"). Cada uma dessas já produziu uma reprovação: fala dura de teleprompter ou fala forçada de propaganda.
- **Sigla.** Uma linha entre parênteses basta: `("PMPE" is said as letters, "pê-eme-pê-é")`. Evite a sigla como última palavra do clipe.
- **Refação com a mesma pessoa.** Comece o prompt com "Use the man/woman in the reference frame, preserving [rosto, cabelo, roupa, cenário]." e passe o quadro como `start_image`.
- **Sem pedir silêncio.** Nunca escreva "stays silent for…" nem "pauses for…": o modelo estica. O ponto de corte entre gancho e CTA é achado pela transcrição.
- **CTA no mesmo tom.** Sem aumentar o volume, sem dar ordem, sem virar locutor. O gesto de apontar para baixo tem que estar escrito, ligado às palavras "aqui embaixo".
- **Só gancho** (sem CTA do avatar): tire o bloco "Then…" e ajuste a contagem.
- **Em espanhol:** fala em espanhol, persona correspondente; o CTA "Mira esto" vem sempre com o dedo apontando.

## 4. Parâmetros e geração

`generate_video` (ou `generate_video_batch` para a leva) com:

```json
{"model": "flux_3_video", "duration": 16, "aspect_ratio": "9:16", "resolution": "720p", "generate_audio": true,
 "use_unlim": false, "count": 1, "prompt": "…"}
```

- Antes: `get_cost: true` com os mesmos parâmetros, e diga o custo ao usuário.
- Se a ferramenta devolver uma sugestão de preset ("preset_recommendation"), repita a chamada com o `declined_preset_id` indicado: o pedido é geração literal.
- Acompanhe com `jobs_wait` (leva 3 a 5 minutos). Baixe o `result_url` com `curl -sS -o "$PJ/avatar_raw.mp4" "<url>"`.
- 720p basta: o motor amplia para 1080x1920.

## 5. Quando sai errado

`montar_base.py` mostra a fala reconhecida. Compare com o texto:

| Problema | O que fazer |
|---|---|
| Palavra trocada, repetida ou frase faltando | Regenerar. Avise o usuário do custo antes. Na segunda falha na mesma construção, proponha outra redação. |
| Última palavra cortada no fim do clipe | Regenerar com 1 s a mais de duração (não mais: clipe longo deixa a fala lenta). |
| Começou a falar tarde ou deixou pausas | Nada: o script corta (a não ser que o projeto use `gancho_inteiro`). |
| "Ritmo do gancho" marcado como LENTO, ou o usuário diz que está arrastado, "texto solto" | Regenerar só o gancho com duração justa (seção 2) e, se preciso, texto um pouco mais longo. Acelerar na edição não resolve o jeito. |
| O usuário diz que está forçado, animado, com cara de propaganda | Regenerar com o modelo curto da seção 3, tom de indicação, e rever as palavras pelo público (seção 1). |
| Pronúncia duvidosa (o reconhecedor alterna entre duas palavras) | Não regenere por conta própria; peça para o usuário ouvir. |
| Tom de teleprompter, CTA forçado | Só o usuário percebe. Se ele reclamar, refaça com prompt **mais curto**, focado no problema, e com um quadro de referência para manter a pessoa. |

Corrija o erro específico. Não reescreva o prompt inteiro nem acrescente uma coreografia.

## 6. O que o script faz com o clipe

- Transcreve e mostra a fala completa.
- Acha a divisa gancho/CTA: o primeiro instante em que a última palavra do gancho já foi dita, depois o primeiro em que a primeira palavra do CTA aparece, e corta no ponto de menor volume entre os dois.
- No CTA, corta silêncios acima de 0,35 s dentro da fala (corte seco, com leve aproximação de 6% em trechos alternados para o salto parecer intencional). O gancho entra inteiro, sem cortes (`gancho_inteiro`).
- Deixa 0,3 s de rosto parado antes da primeira palavra.
- Iguala o volume ao da voz do áudio (o FLUX costuma vir 10 a 18 dB mais baixo) e reduz o ruído de fundo.
- No fim do CTA, segura o último quadro por 0,7 s com as setas.
- Recorta o avatar do fundo em cada quadro do gancho (`gancho_alpha.npy`): no vídeo ele aparece sem o cenário, sobre um print da primeira tela do corpo (ver `references/roteiro.md`). O cenário descrito no prompt continua valendo: ele aparece no CTA e dá a luz e o jeito de gravação caseira.

## 7. O que já deu errado

- **Pedir pausa de 1,5 s entre gancho e CTA:** veio 2,25 s, a fala começou aos 2,6 s e a última palavra foi cortada. Geração perdida.
- **Fala colada no fim do clipe:** 40 palavras em 15 s terminaram a 0,03 s do fim. Na época a conclusão foi pedir 4 s de folga; depois se viu que o modelo sempre termina a fala no fim do clipe e que a folga só deixava a fala lenta (seção 2).
- **Divisa pelo maior silêncio:** o maior silêncio estava no meio do gancho, não entre gancho e CTA. Por isso a divisa é pela transcrição.
- **Gancho sem o alívio:** o avatar dizia a frase absurda e a outra voz explicava. O usuário reprovou: o alívio é parte do gancho.
- **Gesto vago:** "naturally pointing down" deu um aceno. "Clearly pointing straight down with her index finger toward the bottom edge of the frame while she says 'aqui embaixo'" funcionou.
- **Rostos parecidos na leva** (histórico do Codex): planejar a variedade antes, com vários traços, não só roupa.
- **Fala cortada no começo** (histórico do Codex): por isso o quadro de referência com a boca em repouso e o "Preserve the complete first word".
- **AD 01 da PMPE, quatro ganchos até aprovar (2026-10-03; as três refações custaram 93,5 créditos):**
  1. 12 s com 4 s de folga, "light inviting tone": fala a 2,1 palavras/s. Reprovado: "muito lento, não parece gancho, texto solto".
  2. "Gente, olha só…", "excited", "eyebrows up": reprovado como forçado, com cara de propaganda, e "gente" não serve para homem.
  3. "Sober, neutral face, steady eye contact" e uma lista de proibições: reprovado como teleprompter.
  4. Prompt curto de mensagem para um amigo, duas frases com intenção ("Ô, se liga só." / "Olha esse guia ilustrado da prova da PMPE por dentro."), 6 s: aprovado. Ele gesticulou e olhou para a mesa por conta própria; não foi pedido.
- **Braço cortado no recorte (AD 01 de Jesus).** O avatar foi gerado com uma Bíblia aberta na mesa à frente e o braço estendido sobre ela. O recorte rápido perdeu o antebraço (sobrou a manga, como um toco) e o usuário viu. O `recortar_avatar.py` passou a usar o modelo maior em resolução cheia, que manteve o braço; a mesa na frente continua cortando o tronco em diagonal, e isso só se evita no prompt (seção 1).
- **Avatar pequeno e baixo no quadro (segundo avatar do AD 01 de Jesus).** Pedir só "framed from the chest up, centered, nothing in front" deu um homem sentado longe, com a cabeça na metade de baixo do quadro e muita parede em cima. Recortado, ele sumia no pé da tela. O motor agora amplia sozinho (até 1,4x) quando a cabeça vem baixa, mas a imagem perde nitidez: peça o rosto grande e no alto já no prompt.
- **Interjeição curta no começo.** O "Ô" inicial (0,3 s) foi tratado como ruído e o corte de silêncios comeu metade dele. Use `"gancho_inteiro": true` no `projeto.json`.
- **Juntar gancho novo com CTA antigo.** Concatene os dois clipes num arquivo (mesmo tamanho e fps), iguale o volume da fala dos dois e aponte `avatar_video` para ele; a divisa continua sendo achada pelas palavras.
