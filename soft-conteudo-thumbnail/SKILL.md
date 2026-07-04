---
name: soft-conteudo-thumbnail
description: Cria a THUMBNAIL/capa de vídeo (YouTube, Shorts, aula, VSL) do método Soft, a imagem que decide o clique antes de alguém ouvir uma palavra. Usa o rosto real do dono como elemento central e cruza o título com as boas práticas de CTR (contraste, expressão, 3-5 palavras de gancho, teto contado, curiosidade sem clickbait vazio). Entrega o BRIEFING de capa + o gancho de texto (já gated, ancorado no verbatim) + o prompt de imagem pronto pro gerador com a foto do dono; a ARTE final renderizada é handoff pra soft-designer. Use quando o pedido for "thumbnail", "thumb", "capa de vídeo", "capa do YouTube", "capa da aula", "capa do Shorts", "faz a capa desse vídeo", "monta uma thumbnail", "capa antes do roteiro". NÃO use pra a HEADLINE/gancho de post de feed (soft-conteudo-headlines), nem pro ROTEIRO do vídeo (soft-conteudo-reels), nem pra arte tipográfica de carrossel/banner/deck OU a renderização final da capa (soft-designer), nem pro Plano/posicionamento (soft-posicionamento), nem pra carta/VSL em texto (soft-funil).
---

# Thumbnail, a capa que vende o vídeo antes da primeira palavra

A pessoa decide clicar no vídeo em menos de 1 segundo, olhando a capa entre dezenas de outras miniaturas. A thumbnail é a headline do vídeo: se ela não para o olho, o roteiro perfeito nunca é ouvido. Por isso a capa vem ANTES do roteiro (thumbnail-first): você desenha o clique primeiro, e o vídeo entrega a promessa da capa.

**O que esta skill faz por você:** pega o título do vídeo e o rosto do dono e devolve o BRIEFING da capa (composição + gancho de texto + paleta + elemento focal) mais o prompt de imagem pronto pro gerador. O gancho de texto (as 3-5 palavras que ficam na capa) passa pelo mesmo gate das headlines: ancorado no verbatim, sem clickbait que o vídeo não entrega. A ARTE final renderizada é handoff pra **soft-designer** (é ela que roda o gerador de imagem ou compõe a capa).

**A fronteira (não invada):** esta skill DECIDE a capa (o que compõe o clique) e escreve o GANCHO de texto. Quem RENDERIZA a arte final (chama o gerador com a foto, compõe o overlay de texto, exporta o PNG) é a **soft-designer** (branch de imagem-IA). Quem escreve o ROTEIRO do vídeo é a **soft-conteudo-reels**. Você entrega o briefing + o prompt e faz o handoff; não é o motor de render.

**As 6 leis (valem antes de tudo, detalhe em `shared-references/operacao-padrao.md` Seção 0):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil; (2) abre ensinando o que faz; (3) é consultiva, puxa a foto e o título antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: sem a foto de referência ou sem fala real do avatar, marca `[A CONFIRMAR]`, jamais inventa um gancho plausível de choque; (6) **doc de output enxuto pros 2 leitores**: o briefing que sai serve o humano que aprova E a soft-designer que recebe como contexto do render.

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos STOPs, e rode o gate por dentro antes de mostrar a capa.**

## Output Contract (o que você entrega)
- Um **BRIEFING de thumbnail** consolidado: título do vídeo · gancho de texto (3-5 palavras) · composição (posição do rosto, % do quadro, direção do olhar, expressão) · paleta (2 cores dominam) · elemento focal além do rosto · zona-limpa do selo de duração.
- Junto, o **prompt de imagem pronto pro gerador**, com a foto de referência do dono como input (a foto entra anexada, nunca o caminho dentro do prompt).
- O **gancho de texto passou pelo gate** (ancorado, curiosidade real, sem clickbait vazio, teto de palavras CONTADO, anti-IA). Só gancho que passa vai pra saída.
- **1-3 variações de capa** quando o dono pede escolha (mudam o gancho + a expressão + a composição, não só a cor).
- O **handoff explícito**: no fim, "passo o prompt pra soft-designer renderizar / rodar o imagegen, ou você cola no seu gerador".
- Você **para e espera** o dono aprovar o briefing antes de soltar o prompt e antes do handoff.
- Você **nunca inventa fala nem número** do avatar e **nunca mostra gancho que falhou no gate** (clickbait de choque falso reprova).

## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a capa no chat)
Regra dura: o RESULTADO é **UM documento markdown consolidado** (o briefing + o prompt de imagem). No **claude.ai**, um **artifact de markdown** (o dono abre, copia o prompt, cola no gerador); no **Claude Code**, um arquivo `.md`; no **agente/Telegram**, um ARQUIVO cujo path completo vai na resposta. A CONDUÇÃO (puxar foto/título, os STOPs) acontece no chat; o BRIEFING e o PROMPT moram no DOC. Ao parar num STOP, você mostra/atualiza o DOC e pergunta "ajusto?"; NUNCA reescreve o prompt em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Os 3 ambientes (como a entrega muda)
- **App/chat (claude.ai, sem Bash):** o briefing + o prompt saem como **artifact de markdown**. Você entrega o prompt pronto pra colar no gerador do dono (o dono anexa a foto lá). Não renderiza a imagem aqui; o render é da soft-designer no Code ou do próprio dono no gerador dele.
- **Claude Code (tem Write/Edit/Bash):** salva o briefing em `thumbnail-<slug>-AAAA-MM-DD.md` na working dir + roda `python3 scripts/lint_copy.py` no gancho de texto como cinto anti-IA. Faz handoff pra **soft-designer**, que pode chamar o `imagegen` local (gpt-image, aceita foto de referência) e exportar o PNG 1280x720. Confirma os paths pro dono.
- **Agente/Telegram (tem Bash):** grava o `.md` e devolve **o path completo na resposta**, mais um resumo curto SEM markdown pesado (o gancho + as 2 decisões-chave da capa em texto corrido, sem asteriscos). O briefing e o prompt inteiros moram no arquivo. Se for renderizar, o PNG exportado tem o path completo na resposta também.

## Passo 0, puxa a foto e ancora (NÃO PULE, é a fronteira)
Procura o insumo nesta ordem: **perfil do dono colado na conversa / `soft-perfil.md`** → **descrição do projeto** → **mensagens anteriores** (`shared-references/crivo/00-perfil-do-usuario.md` diz onde cada slot mora).

Precisa de duas coisas antes de desenhar:
1. **A foto de referência do dono.** O ideal é uma foto nítida do rosto, boa luz, com uma expressão que dá pra reaproveitar em vários vídeos (isso é o que mantém a marca do canal consistente). Se não houver caminho salvo, pede numa linha: *"me manda ou aponta o caminho da sua foto de referência (rosto nítido, boa luz) que eu uso na capa"*.
2. **A ancoragem do gancho.** Puxa **2-4 falas de DOR e 2-4 de DESEJO** do avatar sobre o tema do vídeo, literais, contando o N. O gancho de 3-5 palavras nasce de uma dessas falas, nunca de choque genérico inventado.

Três estados de entrada (declara qual é o seu):
- **Tem foto + tem fala real (com N):** caminho ideal. Ancora o gancho na fala e cita o N.
- **Tem foto mas ZERO fala literal:** NÃO inventa gancho de choque. Ancora em prova real do dono (resultado, case, mecanismo); número não confirmado vira `[A CONFIRMAR]`. Avisa que minerar 5-8 falas reais (ou rodar o Plano na soft-posicionamento) deixa o gancho muito mais cravado.
- **Sem foto:** pede a foto numa única mensagem antes de gerar o prompt (o prompt sem foto de referência sai genérico e perde a marca do canal). Pode adiantar o briefing de texto enquanto espera.

**Gatilho de nicho regulado (BLOQUEANTE, roda ANTES de fechar o gancho):** se o nicho do dono for regulado por conselho de classe (saúde, jurídico, finanças e correlatos, ex.: fisioterapeuta, dentista, nutri, advogado), roda o `shared-references/crivo/04-gate-regulado.md` ANTES de fechar o gancho e o briefing. Ele VETA gancho de cura, de resultado garantido, ou de prazo cravado sobre condição de saúde (ex.: "não é pra sempre" sobre um sintoma clínico = promessa implícita de cura, reprova) e manda trocar pro eixo educação/mecanismo. Na dúvida se o nicho é regulado, TRATA como regulado.

## Passo 1, pega o título e o tom emocional
O título do vídeo vem do dono (ou você propõe 3 títulos fortes se ele pedir). O título e o gancho de capa são coisas diferentes: o título é a linha do YouTube (mais longa), o gancho é as 3-5 palavras GRANDES na imagem. Um complementa o outro, não repete.

Escolhe o **tom emocional** que a expressão do rosto vai carregar (casado com a dor/desejo do avatar, não escolhido por estética):
- **Choque/surpresa:** olhos arregalados, boca aberta. Serve pra revelação que quebra crença ("o que ninguém te contou").
- **Curioso/pensativo:** sobrancelha erguida, olhar fora do quadro na direção do texto. Serve pra loop aberto ("por que isso acontece").
- **Confiante/direto:** olhar na câmera, calmo, assertivo. Serve pra autoridade e método ("é assim que se faz").
- **Tensão/opinião forte:** olhar intenso, gesto de mão. Serve pra tese contrária ("para de fazer isso").

## Passo 2, aplica as boas práticas de CTR (o coração da capa)
Toda thumbnail respeita estas regras, elas são o que faz o olho parar na grade de miniaturas:

| # | Regra de CTR | Passa se |
|---|---|---|
| 1 | **Rosto ocupa 30-50% do quadro** | o rosto é grande, legível mesmo em miniatura pequena (mobile); rosto escondido/pequeno reprova |
| 2 | **Texto = 3-5 palavras, gancho, não frase** | é um estilingue de curiosidade ("demiti meu time", "não faça isso"), nunca uma sentença completa; teto de 5, ideal 3, 6 só em último caso |
| 3 | **2 cores dominam** | a cor da marca do dono + UMA cor de destaque de alto contraste (amarelo, vermelho ou ciano puxam o olho); paleta poluída reprova |
| 4 | **1 elemento focal além do rosto** | um objeto, número grande, logo de ferramenta ou seta que dá o assunto num relance. Número/dado marcado `[A CONFIRMAR]` NÃO pode virar elemento focal nem número-atrás-do-ombro até ter fonte; se o número é a espinha da capa e não tá confirmado, PARA e minera a fala antes de montar a arte |
| 5 | **Alto contraste testável** | apertando os olhos, rosto/texto/fundo ainda se separam; teste do olho semicerrado |
| 6 | **Zona-limpa do selo de duração** | nada de texto ou logo importante no canto inferior direito (o selo de tempo do YouTube cobre) |
| 7 | **Legível a 320px** | o texto se lê no tamanho mobile do YouTube; texto miúdo é texto invisível |
| 8 | **Consistência de canal** | mesma família de estilo (enquadramento, fonte, tratamento de cor) entre vídeos, pro reconhecimento da marca |

**Proporção:** 1280x720 (16:9) é o nativo do YouTube long-form e da capa de aula/VSL. Shorts/reel de capa é 1080x1920 (9:16 vertical), rosto e texto na metade de cima (a de baixo some atrás da UI). Declara qual proporção antes de montar o prompt.

## Passo 3, escreve o gancho de texto e roda o GATE por dentro (auditoria interna, NÃO imprime)
O gancho de 3-5 palavras é COPY, então passa pelo gate igual a uma headline. Escreve 2-3 candidatos ancorados na fala real do Passo 0, e roda o gate em CADA um internamente. Só gancho que passa em TODOS os critérios vai pro briefing. A tabela é teu **checklist interno**, nunca a saída.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorado** | nasce de fala real do avatar (verbatim, cita N) OU de prova real do dono; choque inventado/número plausível = ✗; sem fonte marca `[A CONFIRMAR]` | |
| **Curiosidade real (não clickbait vazio)** | abre um loop que o vídeo FECHA; a promessa da capa casa com o conteúdo; ✗ choque que o vídeo não entrega (quebra a confiança do canal) | |
| **Teto CONTADO (3-5 palavras)** | você CONTA de fato as palavras, não chuta; 5 no máximo, 3 é o melhor; estourou = comprime, não corta a curiosidade | |
| **Gancho, não frase** | é um estilingue, não uma sentença explicativa; ✗ "veja como eu consegui aumentar minhas vendas" · ✓ "vendi dormindo" | |
| **Clareza (Lei 1)** | dá pra entender num relance, sem já ser de dentro; zero palavra difícil, zero figura vazia; ✗ "reorganize sua percepção" · ✓ "cobrei o dobro" | |
| **Complementa o título** | o gancho não repete o título palavra por palavra; os dois somam curiosidade. Repetir trecho literal do título = ✗. Ex.: título *"...o que ninguém te explicou"* → ❌ gancho "Ninguém te explicou isso" (ecoa o parêntese do título) · ✓ "Não é pra sempre" (soma curiosidade nova) | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, transforma"). No chat/agente sem lint, faz CTRL+F manual de "—" e "travar" | |
| **Gate regulado (se aplicável)** | nicho regulado (saúde/jurídico/finanças) passou pelo `shared-references/crivo/04-gate-regulado.md`; VETA gancho de cura/resultado/prazo-cravado sobre condição de saúde e troca pro eixo educação/mecanismo. Fora de nicho regulado, não se aplica | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ o gancho. Repetir trecho literal do título = ✗ automático. Só tudo-✓ entra no briefing | |

## Passo 4, monta o briefing e o prompt de imagem
Monta o BRIEFING enxuto no DOC:

```
Vídeo: [título do vídeo]
Proporção: [1280x720 16:9  /  1080x1920 9:16]
Gancho de texto: "[3-5 palavras, já gated]"
Composição: [posição do rosto, % do quadro, direção do olhar, expressão/tom]
Posição do texto: [esquerda / direita / topo / contorna o rosto]  (fora da zona do selo)
Paleta: [hex marca], [hex destaque], [tratamento do fundo]
Elemento focal: [objeto / número / logo / seta]
```

Depois o **prompt de imagem** num bloco de código, seguindo a lei geral de arte-imagem do ecossistema (`references/prompt-de-capa.md` e `soft-designer` §8): **o texto NUNCA vai dentro da imagem gerada, entra por overlay por cima**, pra a copy ficar editável sem regenerar a imagem. O prompt pede só o CENÁRIO (rosto + fundo + elemento focal); a soft-designer aplica o gancho por cima.

```
Usando a foto de referência do dono em anexo, gere uma imagem de fundo de thumbnail em [1280x720 / 1080x1920].
Composição:
- Posicione o dono [à esquerda / à direita / ao centro] ocupando [30-50]% do quadro
- Expressão: [detalhe do tom, ex.: chocado, olhos arregalados, boca entreaberta]
- Olhar: [direção, ex.: direto na câmera / pra fora do quadro no lado onde o texto vai entrar]
Cenário:
- Fundo: [hex], tratamento [chapado / gradiente / cena desfocada]
- Elemento de apoio: [descrição específica: objeto, número grande, seta]
Paleta: primária [hex marca], destaque [hex de alto contraste]
Restrições:
- NÃO escreva NENHUM texto na imagem (o texto entra por overlay depois)
- Rosto nítido e bem definido, alto contraste entre rosto, elemento e fundo
- Deixe uma área limpa em [lado onde o texto vai] e no canto inferior direito (selo de duração)
- Sem marca d'água, sem elementos de interface do YouTube
```

## Passo 5, mostra, PARA e faz o handoff
Mostra o briefing + o prompt **no DOC** (nunca solta no chat). Pergunta: *"esse briefing te serve? digo 'renderiza' pra soft-designer gerar a capa (rodar o imagegen com a sua foto), ou você cola o prompt no seu gerador. Quer variação?"*. **Espera a escolha.**
- **"renderiza" no Code/agente:** handoff pra **soft-designer** (branch de imagem-IA): ela chama o `imagegen` com a foto anexada, aplica o gancho por overlay, exporta o PNG e devolve o path. O gancho gated e o briefing vão como contexto.
- **App/chat:** entrega o prompt pronto; o dono cola no gerador dele e anexa a foto.
- **Variação:** gera 1-3 capas alternativas (mudam gancho + expressão + composição), cada uma passando pelo gate.

## Exemplo denso (nicho: consultor de vendas B2B), LABEL, não copiar
Título do vídeo: *"Como eu fecho contrato de R$50 mil sem fazer reunião de apresentação"*. Tom: confiante/direto.
> **BRIEFING.** Gancho: **"Vendi sem reunião"** (3 palavras) · Composição: dono à direita, ~40% do quadro, olhar na câmera, braços cruzados, meio sorriso confiante · Texto à esquerda em amarelo com contorno preto grosso · Paleta: azul-marinho da marca + amarelo de destaque · Elemento focal: um "R$50K" grande atrás do ombro, meio desfocado.
- **Ancorado:** verbatim real "eu perco a venda quando marco a reunião de apresentação, o cara esfria" (N=3 nas calls). O gancho nasce dessa dor, invertida em promessa.
- **Curiosidade real:** o loop ("como fecha sem reunião?") é exatamente o que o vídeo ensina; a capa não promete nada que o roteiro não entrega.
- **Teto contado:** "Vendi sem reunião" = 3 palavras. PASSA.
- **CTR:** rosto 40% (regra 1), 2 cores (azul+amarelo, regra 3), elemento focal R$50K (regra 4), texto fora do canto do selo (regra 6). Alto contraste no teste do olho semicerrado.
- **Anti-IA:** zero travessão, zero "travar", zero frase-emoldura. VEREDITO = PASSA.

Contra-exemplo (REPROVA): gancho **"Você NÃO vai acreditar nisso"** com foto de choque e o vídeo é um tutorial calmo. Clickbait vazio: a capa promete choque que o conteúdo não entrega, queima a confiança do canal. Falha em "curiosidade real". VEREDITO = ✗, reancora na dor real.

## When NOT to use (manda pra skill certa)
- Pediu a **HEADLINE/gancho de um POST de feed** (carrossel, reel de conteúdo) → **soft-conteudo-headlines**.
- Pediu o **ROTEIRO do vídeo** (o que falar) → **soft-conteudo-reels**.
- Pediu **arte tipográfica** (carrossel PNG, banner, deck, infográfico-lousa) OU a **RENDERIZAÇÃO final da capa** (rodar o gerador, compor o overlay, exportar o PNG) → **soft-designer** (é ela que renderiza a arte desta skill).
- Pediu pra **definir posicionamento/avatar/pilares** → **soft-posicionamento** (é de lá que a fala/avatar vêm).
- Pediu **carta/VSL/página em texto** → **soft-funil**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Gancho virou frase explicativa longa | Comprime pra 3-5 palavras, estilingue de curiosidade, não sentença |
| Clickbait de choque que o vídeo não entrega | Reprova no gate; reancora na dor real do avatar, a capa casa com o conteúdo |
| Inventou um número de choque pra chamar clique | Fere a Lei 5; número sem fonte vira `[A CONFIRMAR]`, nunca vai pra capa, NEM no gancho NEM como elemento focal / número-atrás-do-ombro |
| Pôs um número `[A CONFIRMAR]` como elemento focal gigante da arte | O veto cobre o VISUAL, não só o gancho de texto; número sem fonte não vira foco da capa. Para, minera a fala, só monta a arte com o número confirmado |
| Pediu o prompt sem a foto de referência | Para e pede a foto; sem ela a capa sai genérica e perde a marca do canal |
| Pôs texto DENTRO da imagem gerada | Texto vai por overlay por cima (soft-designer), nunca dentro do prompt; senão a copy não é editável |
| Rosto pequeno ou escondido | Rosto 30-50% do quadro, ponto focal visível; refaz a composição |
| Texto/logo no canto inferior direito | Move pra área limpa; o selo de duração do YouTube cobre esse canto |
| Cada vídeo com estilo totalmente diferente | Mantém a família de estilo entre vídeos pro reconhecimento do canal |
| Tentou renderizar a arte aqui | Esta skill entrega briefing + prompt; o render é handoff pra soft-designer |
| Despejou o prompt solto no chat | O briefing + prompt saem como doc MD (artifact / arquivo / path no agente) |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `references/prompt-de-capa.md`: o guia completo do prompt de imagem de capa (a regra "texto por overlay, nunca na imagem", os moldes de prompt por tom emocional, a integração com o `imagegen` local, a variante 9:16 de Shorts, os erros de gerador). Consulta quando o prompt não sai como pedido ou pra a variante vertical.
- `shared-references/operacao-padrao.md`: as 6 leis (Seção 0) + regras de tom/economia/entrega. Consulta na 1ª invocação da sessão.
- `shared-references/crivo/00-perfil-do-usuario.md`: onde mora a foto de referência, a marca e o avatar do dono (os 5 slots do perfil).
- `shared-references/filtro-anti-ia/`: o banco de padrões banidos + falsos-positivos que alimenta o check Anti-IA do gate do gancho.
- `scripts/lint_copy.py`: no Claude Code/agente, roda `python3 scripts/lint_copy.py` no gancho de texto como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual do gate.
