---
name: soft-webinar-slides
description: "Renderiza o DECK/slides do webinar Soft a partir de um roteiro ADMA já pronto: projeta o roteiro nos beats do deck, escolhe o arquétipo de cada slide, joga TODA a copy falada pras notas e deixa na tela só o reforço (1 ideia, 1 número ou 1 imagem por slide), com mecanismo e oferta em slides próprios e respiro em toda virada. Não reescreve o roteiro nem reordena os blocos, só veste de tela. Roda o gate antes de exportar e faz o handoff do visual fino. Use quando o pedido for slides do webinar, deck do webinar, apresentação do webinar, gerar os slides, montar o deck, template de slides, copy na nota, ritmo do deck. NÃO use pra escrever o roteiro/falas do webinar inteiro → soft-webinar-script; nem pro PLANO/esqueleto ADMA → soft-webinar-plano; nem pra OFERTA/stack/preço → soft-webinar-plano; nem pro visual fino/arte/PNG → soft-designer; nem pra carta/VSL/landing → soft-funil-carta/soft-funil-landing."
---

# Slides do webinar, o deck que constrói crença slide a slide

O deck não é o conteúdo. É o amplificador visual de um roteiro que já funciona. A fala constrói a crença; o slide só devolve o olho pra voz e ancora 1 ideia. Slide que rouba a leitura mata a venda tanto quanto slide morto.

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de exportar qualquer deck.**

## Output Contract (o que você entrega)
- Um **deck descrito slide a slide** projetado sobre o roteiro ADMA: por slide, o **arquétipo/tipo**, o **reforço visível** (1 frase OU 1 número OU 1 imagem-conceito) e **a copy falada na NOTA**.
- A entrega vem **por fase do roteiro, uma de cada vez** (Atenção → Diagnóstico → Mecanismo → Ação), nunca o deck inteiro despejado.
- Cada fase mostrada vem com **a tabela do gate preenchida** (o artefato visível).
- Você **para e espera OK** antes de seguir pra próxima fase.
- Você **nunca reescreve o roteiro nem reordena os blocos**, só veste de tela. Se o texto de tela condensa a fala, re-passa pelo gate antes de exportar.
- Você **nunca inventa número, prova, bônus ou preço** e **nunca exporta deck cuja fase falhou no gate**.
- **ZERO travessão "—" em QUALQUER caractere do arquivo .md entregue** (títulos, rótulos de slide, nomes de fase, bullets, moldura do markdown, tela E nota, não só a copy falada). Use hífen "-" ou dois-pontos. O lint varre o arquivo inteiro; a moldura conta.
- A entrega tem **veredito duplo**: **ESTRUTURA** (o esqueleto converte quando o lastro entrar?) e **PRONTA-PRO-AR** (todo `[DADO]`/`[FALA]`/`(a definir)` preenchido com lastro real?). Enquanto houver **um** placeholder aberto, o VEREDITO da fase é **RASCUNHO-COM-PENDÊNCIA**, nunca PASSA seco.


## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a peça no chat)
Regra dura, vale mesmo pra copy curta: o RESULTADO desta skill sai como **UM documento markdown consolidado**. No **claude.ai**, um **artifact de markdown** (o dono abre, copia, baixa); no **Claude Code**, um arquivo `.md`; no **agente/Telegram**, gera o doc como arquivo `.md` e cita o path completo na resposta (o bridge anexa), com a condução em mensagens curtas, sem markdown pesado (nada de `##` nem tabela `|` no texto ao usuário; o gate e o deck vão dentro do arquivo). A CONDUÇÃO (perguntas de contexto, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA/COPY em si mora no DOC. Ao parar num STOP, você mostra ou atualiza o DOC e pergunta "ajusto?"; você NUNCA reescreve a peça em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Passo 0, exige o roteiro pronto (NÃO PULE)
O deck nasce do script, nunca do zero. Procura o roteiro ADMA, nesta ordem: **roteiro colado na conversa** → **descrição do projeto** → **mensagens anteriores**. Três estados de entrada (declara qual é o seu):
- **Tem roteiro ADMA completo:** caminho ideal. Projeta direto.
- **Tem só esqueleto/blocos, sem fala fechada:** projeta os beats, mas marca cada nota como `[FALA: do roteiro, a fechar]` e avisa que o deck só fecha com o roteiro pronto (vai pra **soft-webinar-script** escrever, ou **soft-webinar-plano** pro esqueleto).
- **Não tem roteiro:** PARA. Não inventa fala de palco. Manda fechar o roteiro primeiro (**soft-webinar-script**) e volta.

Puxa do roteiro: a UMA promessa central · o mecanismo nomeado · as provas reais (caso + número + prazo) · a oferta (stack/preço, se já existe). Número sem prova no roteiro entra como `[DADO: confirmar]`, nunca inventado.

## Passo 1, projeta o roteiro nos beats do deck (ordem-lei)
Cada bloco do roteiro vira uma faixa de slides. A ordem é lei: cada slide deixa o lead num estado que é pré-condição do próximo. Pode **expandir** um beat em mais slides; **não pode suprimir nem reordenar**. Proporção-alvo: **~55% ensino / ~45% oferta** (o fechamento pesa quase tanto quanto o conteúdo, nunca encurta).

| Fase ADMA | Faz na tela | Arquétipos típicos |
|---|---|---|
| **Pré-início** | sala "começa" antes de começar: pergunta de dor fixa + prova social passiva | capa · respiro |
| **Atenção** | promessa-mãe → autoridade (empresa antes da pessoa) → origem (fracasso primeiro) → manifesto-tese → dicotomia (medo primeiro) → contrato com loops → presente pra quem ficar | capa · respiro · prova · dicotomia |
| **Diagnóstico** | dor batizada com lastro → causa raiz (inimigo nomeado) → demolição empática das saídas falsas → consequência → "a culpa não é sua" | prova · storytelling de dor (1 cena/slide) · respiro |
| **Mecanismo** | reveal progressivo do método SIMPLES → ensino visual → prova/documento empilhada → recap yes-ladder → transição pedida pela plateia | reveal peça-a-peça · mecanismo · prova · respiro |
| **Ação** | proposição de valor → âncora alta → stack-nota-fiscal → queda riscada em degraus → bônus com reason-why → redução ao ridículo → FAQ matador → CTA com destino | oferta · investimento · prova · fechamento |

## Passo 2, escolhe o arquétipo de cada slide (a função manda)
A função psicológica do beat decide o arquétipo. Os mais transferíveis:
- **Respiro** (tela preta, 1 frase): em TODA virada de fase. O mais barato e o mais frequente.
- **Capa/Big-Idea:** promessa = transformação do avatar, nunca a ferramenta.
- **Prova/número-gigante:** o número vira a manchete; legenda embaixo. Só número REAL.
- **Dicotomia semafórica:** 2 caminhos, vermelho=medo (primeiro), verde=desejo.
- **Storytelling de dor:** 2ª pessoa, 1 cena por slide, escala até o clímax.
- **Reveal progressivo:** o mesmo diagrama entra peça por peça (clique-a-clique).
- **Stack/ancoragem:** âncora externa alta → soma item a item → queda riscada → preço ÷ dias vs. objeto trivial.

Mecanismo e oferta **têm slides próprios** (não dividem palco com outra ideia). A ferramenta, quando aparece, é **motor subordinado dentro do ensino, nunca o título/tese**.

## Passo 3, aplica a regra de ouro (copy na nota, tela mínima)
Esta é a espinha do deck:
1. A **copy falada mora na NOTA** (Speaker Notes). A tela recebe só o reforço.
2. **Pergunta-teste por slide:** "dá pra narrar lendo o que está na tela?" Se **sim → está errado**. Joga o texto pra nota.
3. **1 ideia por slide.** Emoção/virada → tela quase vazia. Prova/referência → pode ser densa (o documento É a mensagem).
4. **Densidade baixa:** framework SIMPLES (ilusão de simplicidade), nunca mega-diagrama de consultoria. Soft vende baixa complexidade.
5. **Toda lista/stack/recap → animada item por clique** (anota na nota "revelar por clique"). Lista aberta de cara mata a curiosidade.
6. **Imagem literal do conceito:** ao dizer uma palavra concreta, mostra a imagem dela (dupla codificação). Uma por ideia.
7. **Slide-mestre da oferta fixo na tela** durante FAQ/fechamento.

> EXEMPLO de nicho FICTÍCIO (dentista, ilustrativo). A fala é "o dentista que só atende convênio vira refém da tabela; quem cria demanda própria escolhe o paciente". Slide RUIM: o parágrafo inteiro digitado na tela (a plateia lê em 3s e abandona a voz). Slide BOM: fundo preto, uma frase só, "Refém da tabela?", e o parágrafo mora na nota. Números como "agenda cheia em 90 dias" ou "R$ 40/dia" são ilustrativos e marcados como tal, jamais atribuídos como verdade.

## Passo 4, monta os slots e o ritmo
- **Slots `(nome a definir com o usuário)`:** título/Big-Idea, nome do mecanismo, bordões-tese, polos da dicotomia, nome do inimigo. Marca, nunca inventa nem decalca de outra marca.
- **Ritmo casado com o roteiro:** troca frequente de estímulo + respiro preto em toda virada de fase. Persegue o RITMO, não uma contagem-alvo de slides.
- **Reserva a zona da câmera** (quando ao vivo/gravado com rosto no canto): anota na nota "reservar zona da câmera no canto".
- **Mobile/tela legível:** fonte grande, alto contraste, nada de bloco de texto miúdo. Se não lê no celular, não serve.

## Passo 5, roda o GATE antes de exportar (artefato visível obrigatório)
Preenche a tabela **por fase**. Só fase com VEREDITO=PASSA é mostrada/exportada. Uma falha refaz a fase (não o roteiro). Sem a tabela impressa, a fase não foi entregue.

**Regra dura de contagem (o furo que reprovou o teste):** o Anti-IA (HARD) NÃO é "CTRL+F que eu fiz de cabeça". No app (sem o lint) esse "confere de cabeça" é o auto-carimbo que o `03-gate-cub.md` diz que invalida a passada. Cola a contagem por caractere proibido, varrendo o TEXTO DO ARQUIVO INTEIRO (tela + nota + títulos + rótulos + bullets + moldura), não a memória. `— : 0` obrigatório em todo o .md, não só na copy falada.

**A versão proibida NÃO fica no doc entregue**, nem como before, riscado, ou comentário "corrigido abaixo". Substitui no lugar e apaga a original. Placeholder de correção não conta como corrigido: o lint varre o arquivo inteiro e reprova a string proibida onde quer que esteja. Se "travou" aparece na copy de tela, a copy de tela vira "parou"/"emperrou"/"empacou" ali mesmo, e a palavra proibida some do arquivo.

**Veredito duplo (não colapsa esqueleto com peça pronta):** cada fase recebe DOIS vereditos. **ESTRUTURA** = o esqueleto converte quando o lastro entrar? **PRONTA-PRO-AR** = todo `[DADO: confirmar]`/`[FALA: do roteiro]`/`(a definir)` está preenchido com lastro real? Enquanto houver um placeholder aberto, o VEREDITO da fase é **RASCUNHO-COM-PENDÊNCIA** (estrutura ok, não-pronta-pro-ar), nunca PASSA seco. Diz exatamente qual insumo do cliente falta (prova, número, fala, WhatsApp). Prova ainda-pendente = pendência, não aprovação.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorada no verbatim** | toda prova/número/aspa nasce da fonte REAL do roteiro (caso + N real); **inventado/plausível = ✗ automático**; **sem fonte real na tela, esta passada sai NÃO-VERIFICADO = ✗** (não ✓ bonzinho), o slide vira `[DADO: confirmar]`/`[FALA: do roteiro]` e a FASE cai em RASCUNHO-COM-PENDÊNCIA. Prova ainda-pendente NÃO é PASSA | |
| **3 perguntas do gate** | no título/frase de cada slide-chave: **dá pra ver?** (cena concreta, não adjetivo) · **dá pra falsificar?** (fato, não promessa vazia) · **só você diz?** (concorrente direto não assina igual) | |
| **C/U/B** | a copy de tela é **Clara** (1 ideia legível) · **Útil** (serve à fala) · **Boa** (na voz do usuário, não genérica) | |
| **CTA com destino** | o fechamento aponta destino real (link/canal humano) que captura indeciso pro comercial 1:1; sem "saiba mais" vago | |
| **1 ideia por slide** | passa a pergunta-teste: NÃO dá pra narrar lendo a tela; toda a copy falada na nota | |
| **Slide serve a fala** | o reforço amplifica a fala, não compete com ela; nada de teleprompter público | |
| **Densidade baixa** | framework SIMPLES; só prova/documento pode ser denso; zero mega-diagrama de consultoria | |
| **Mecanismo e oferta próprios** | mecanismo tem slide(s) só dele; stack e preço nos slides de oferta; nada dividindo palco | |
| **Ritmo ADMA** | respiro preto em TODA virada de fase; proporção ~55/45; fechamento não encurtado; ordem dos beats preservada | |
| **Mobile/legível** | lê no celular (fonte grande, contraste, sem bloco miúdo) | |
| **Slots e prova reais** | slots `(a definir)` marcados não inventados; stack/bônus/preço/escassez REAIS; Big-Idea não fabricada | |
| **Anti-IA (HARD) — CONTAGEM COLADA, não declaração** | zero travessão "—" e zero família "travar" (trava/travou/destrava...) em **QUALQUER** caractere do arquivo (títulos, rótulos, bullets, moldura, tela E nota), · reticências unicode "…" trocadas por "..." · sem "Não é X. É Y." em série · sem frase-emoldura · sem verbo-clichê. **Esta passada NÃO passa por declaração: cola aqui a evidência, uma sub-linha por caractere proibido, com a contagem varrendo o TEXTO DO DOC INTEIRO (não a memória):** `— : 0 ocorrências` · `trav* : 0 ocorrências` · `… : 0 ocorrências`. **Contagem >0 = ✗ (a fase NÃO passa).** Sem a contagem colada, a passada sai NÃO-VERIFICADO = ✗ (espelha `03-gate-cub.md`: grep à mostra, não confere de cabeça). No Code, roda `python3 scripts/lint_copy.py` no arquivo inteiro e cola o exit code. | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA. **Mas se houver placeholder aberto (`[DADO]`/`[FALA]`/`(a definir)`), o veredito é RASCUNHO-COM-PENDÊNCIA** (estrutura ok, não-pronta-pro-ar), nunca PASSA seco: diz qual insumo real falta. | |

> **Re-gate ao condensar:** o texto VISÍVEL do slide é uma condensação NOVA que o lead LÊ, não a fala original. Se condensar/reescrever o texto de tela, re-passa a ancoragem e a headline pelo `shared-references/crivo/03-gate-cub.md` (+ `lint_copy.py`) ANTES de exportar. Depois de aprovado, o render não muda palavra.

## Passo 6, mostra a fase, PARA, e faz o handoff
Mostra **só a fase que passou**, com a tabela do gate, e pergunta "essa fase te serve? sigo pra próxima?". **Espera o OK** antes de seguir. **Um OK = uma fase; nunca adiante 2 fases num STOP.** O gate roda por fase, não no fim: mostrou a Atenção, para; só com o OK vai pro Diagnóstico, e assim por diante. Ao fim das 4 fases, faz o **handoff do visual fino** (paleta, tipografia, arte, mockups, animação clique-a-clique no player) pra **soft-designer**. Esta skill entrega o deck conceitual certo; o acabamento visual é lá.

## When NOT to use (manda pra skill certa)
- Pediu o **roteiro/falas do webinar inteiro** → **soft-webinar-script**.
- Pediu o **PLANO/esqueleto ADMA / perpétuo vs ao vivo** → **soft-webinar-plano**.
- Pediu a **OFERTA / stack / preço / garantia** → **soft-webinar-plano**.
- Pediu **arte/visual fino/PNG/paleta** → **soft-designer**.
- Pediu **carta/VSL/landing** → **soft-funil-carta** / **soft-funil-landing**.
- Pediu **posicionamento / nomear método** → **soft-posicionamento**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Despejou o deck inteiro de uma vez | Volta: uma fase por vez, com gate, e PARA pro OK |
| Pôs o parágrafo da fala na tela | Joga a copy pra nota; na tela só o reforço (1 ideia) |
| Montou o deck sem roteiro pronto | PARA: o deck nasce do script; manda fechar o roteiro (soft-webinar-script) |
| Mega-diagrama de consultoria no mecanismo | Simplifica: ilusão de simplicidade, reveal peça-a-peça |
| Inventou número/bônus/preço "plausível" | Só o que tem prova no roteiro; sem fonte = `[DADO: confirmar]` |
| Ferramenta virou o título/herói do deck | Ferramenta é motor subordinado no ensino; título = transformação do avatar |
| Encurtou a oferta "pra não cansar" | Mantém ~45% do deck no fechamento; ordem dos beats é lei |
| Reescreveu/reordenou o roteiro | Não: só veste de tela; se condensou texto, re-passa o gate antes de exportar |
| Slide morto, sem troca | Respiro preto em toda virada; troca de estímulo casada com a fala |
| Marcou Anti-IA ✓ "de cabeça" sem contar | Cola a contagem por caractere (`— : 0`, `trav* : 0`, `… : 0`) varrendo o arquivo inteiro; sem contagem = NÃO-VERIFICADO = ✗ |
| Pôs travessão só na copy e deixou na moldura/rótulos/títulos | Zero "—" em QUALQUER caractere do .md; use hífen ou dois-pontos, o lint reprova o arquivo todo |
| "Corrigiu" a palavra proibida num comentário mas manteve a versão errada na peça | A versão proibida sai do arquivo: substitui no lugar e apaga a original; before/riscado ainda reprova no lint |
| Marcou PASSA com `[DADO]`/`[FALA]` aberto | Veredito é RASCUNHO-COM-PENDÊNCIA enquanto houver placeholder; diz qual insumo real falta |

## References (o fluxo acima é autossuficiente)
- `shared-references/crivo/03-gate-cub.md`: detalhamento do gate (barreira de ancoragem, CUB em camadas, 3 perguntas do gate, anti-vazamento). Mesma régua, com mais exemplo.
- `shared-references/filtro-anti-ia/`: os padrões banidos que o anti-IA HARD aplica.
- `shared-references/filtro-mobile-first/`: regra de legibilidade na tela do celular.
- `scripts/lint_copy.py`: no Code, roda `python3 scripts/lint_copy.py` no ARQUIVO INTEIRO (não só tela+nota: ele varre toda string, moldura e rótulos inclusive) e reprova em-dash e a família "travar" com exit 1. No chat não roda, por isso a CONTAGEM COLADA do gate (não o "confere de cabeça").
