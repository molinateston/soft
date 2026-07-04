---
name: soft-conteudo-impulsionar
description: Decide o IMPULSIONAR/tráfego pago básico do método Soft, o que turbinar, com quanta verba, por quantos dias, pra qual público, e diagnostica campanha que não retorna. Parte de peças orgânicas que JÁ provaram engajamento real, aplica a régua de custo por seguidor e a distribuição 50/30/20 (Distribuição Pura/Lead/Remarketing), e separa o ROAS de palco do ROI que paga conta. Use quando o pedido for "impulsionar", "turbinar", "tráfego pago", "anúncio", "campanha", "gerenciador de anúncios", "quanto investir", "qual verba", "meu anúncio não retorna", "ROAS", "ROI", "custo por seguidor", "custo por lead", "anúncio/criativo pra encher o webinar", "tráfego pro webinar". NÃO use pra a ARTE/visual do anúncio (soft-designer), nem pro CORPO/copy ou o CTA da peça que vai ser turbinada (soft-conteudo-carrossel/-reels/-headlines), nem pra lançamento pago tático com evento/ingresso (soft-lancamento-pago), nem pro Plano/posicionamento (soft-posicionamento).
---

# Impulsionar, a alavanca de escala (só depois do orgânico validar)

Tráfego pago não substitui posicionamento, acelera o que já funciona organicamente. Ligar antes do orgânico validar é pagar pra acelerar erro. A função do impulsionar é uma: pegar a peça que JÁ provou ROI no orgânico e multiplicar o alcance dela pro público certo, medindo cada real.

**O que esta skill faz por você:** decide o que turbinar, com quanta verba, por quantos dias e pra qual público, e diagnostica a campanha que não retorna. Não escreve a copy da peça (isso é carrossel/reel/headline) nem faz a arte (soft-designer), parte de uma peça que já existe e performou.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa de você os números reais do perfil antes de decidir; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: confere se tem os números reais (engajamento das peças, custo, verba) antes de montar o plano e, se faltar, marca `[DADO: confirmar]` e diz o que falta, jamais inventa métrica plausível; (6) **doc de output enxuto pros 2 leitores**: o que sai é o plano acionável (o que turbinar · verba · dias · público · régua), zero meta-narração. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e confira os pré-requisitos antes de qualquer plano de tráfego.**

## Output Contract (o que você entrega)
- **Um plano de impulsionamento acionável:** lista de peças candidatas (priorizadas por engajamento orgânico real) + por peça o objetivo · público · verba/dia · duração · métrica-chave.
- **A distribuição mensal da verba** no 50/30/20 (Distribuição Pura · Lead · Remarketing).
- **A régua de decisão** (continuar · trocar público · pausar) por custo por seguidor, e o **ROI mensal absoluto**, não só o ROAS.
- Quando o tráfego já roda, **o diagnóstico** (sintoma → causa → fix), um gargalo + um ajuste por vez.
- Você **nunca inventa número do perfil nem do criativo** e **nunca monta plano sem os pré-requisitos cumpridos**.
- A copy/CTA do criativo é da `soft-conteudo-headlines/-carrossel/-reels`; a arte é da `soft-designer`. Aqui é a estratégia de verba e decisão.


## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a peça no chat)
Regra dura, vale mesmo pra copy curta: o RESULTADO desta skill sai como **UM documento markdown consolidado**. No **claude.ai**, um **artifact de markdown** (o dono abre, copia, baixa); no **Claude Code**, um arquivo `.md`. A CONDUÇÃO (perguntas de contexto, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA/COPY em si mora no DOC. Ao parar num STOP, você mostra ou atualiza o DOC e pergunta "ajusto?"; você NUNCA reescreve a peça em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Passo 0, confere os PRÉ-REQUISITOS (gate bloqueante, NÃO PULE)
Tráfego acelera o que já funciona. Ligar antes destes 5 itens é pagar pra acelerar erro. **Se algum falta, PARA e diz o que falta, não monta plano de verba:**

| Pré-requisito | Por quê |
|---|---|
| Posicionamento empacado (Plano de pé) | Sem isso, tráfego atrai público errado |
| Perfil convertendo (visita → seguir) | Sem isso, o lead chega e vaza |
| Destino no ar (Mini Carta / isca / DM com palavra) | Sem isso, o lead clica e não tem pra onde ir. **Exceção:** o ad de ATRAÇÃO (story ad) é CTA-less por desenho, a segmentação faz o trabalho; o filtro de destino vale só pro ad de CONVERSÃO |
| ≥1 peça orgânica acima da média do perfil | É o que diz O QUE turbinar com confiança |
| Primeira venda do método já fechada | Confirma que a oferta converte antes de escalar |

Com os pré-requisitos ok, **ancora nos números REAIS do perfil** (engajamento das últimas peças, custo atual se já roda). Sem os números, pergunta numa mensagem e marca `[DADO: confirmar]`, nunca assume.

**Pré-check do perfil (opcional, cruza com a soft-posicionamento):** o pré-requisito "perfil convertendo" tem um teste objetivo. O **Score de Autenticidade** (mora na `soft-posicionamento`, ref `references/modo-perfil.md` §3.6 + `scripts/score_perfil.py`) audita se o perfil parece real e limpo antes de virar destino de verba, foto real e não de banco, biografia e destaques de gente que faz, sinais de perfil vivo. Perfil que não passa nesse crivo não deve receber tráfego (o lead chega e desconfia). Se houver dúvida sobre a solidez do perfil, roda esse score na soft-posicionamento antes de montar o plano de verba aqui.

## Passo 1, escolhe o nível
- **Turbinar (botão nativo):** amplifica peça orgânica que já provou ROI (40+ curtidas orgânicas naturais). R$10-15/dia por peça, 3-7 dias. Simples, custo baixo, menos controle de público. É onde o solo começa.
- **Gerenciador de Anúncios:** campanhas estruturadas (públicos custom, lookalike, remarketing, pixel de conversão). R$50+/dia sustentado. Entra quando o turbinar atinge teto e o especialista quer escalar.

**Nota-fronteira, decisão aqui × execução lá:** esta skill DECIDE o tráfego (o que turbinar, quanta verba, qual público, a régua). Quem EXECUTA a campanha estruturada no Gerenciador (cria conta/campanha/ad set/ad via API, audita a conta, ativa e pausa) é a `soft-trafego-meta`. Ela nasce toda campanha PAUSADA e só liga com o OK explícito do dono, e herda ESTA skill como gate de entrada (confere os 5 pré-requisitos, aplica o 50/30/20 e a régua de custo antes de gastar). Regra: o plano de verba sai daqui; a mão que mexe na conta de anúncios é a `soft-trafego-meta`. No **claude.ai** (sem credencial) esta skill entrega o plano e o especialista executa na mão ou aciona a `soft-trafego-meta` onde ela tem acesso à conta.

## Passo 2, identifica os candidatos e a função de cada um
Olha as peças orgânicas dos últimos 30 dias (números reais). Candidato = top 3 carrosséis (swipe + saves acima da média) + top 3 reels (watch time + sends acima da média). O **Passo 2.5** (logo abaixo) refina essa lista pelos 4 quadrantes, prioriza a Estrela e a Ouro de nicho e descarta a de Alcance raso. Cada peça serve uma das **3 funções**, cada uma com criativo e métrica próprios:

| Função | O que faz | Criativo | Métrica-chave |
|---|---|---|---|
| **Atração** (público frio) | traz quem não te conhece | vídeo/carrossel longo que filtra (quem vê 90% É o cliente) | custo por visita ao perfil / por seguidor |
| **Lead** (DM ou Carta) | captura mensagem/clique | carrossel 3C com CTA forte ou reel curto com hook + CTA | custo por mensagem no DM (alvo < R$3) |
| **Remarketing** (já se envolveu) | reapresenta a quem interagiu 30-90 dias | depoimento, caso, seeding, oferta direta | conversão (3-5x a do frio) |

(A métrica-chave por formato e o duplo filtro algorítmico × financeiro estão em `references/metricas.md`.)

**Quando o criativo de Atração for um STORY AD** (o anúncio que se camufla no conteúdo do dia, "não prometa, não convide, só afirmações e coisas soltas", foto/vídeo REAL nunca banco/IA, métrica = custo por visita R$0,15-0,25), a estrutura da associação + a régua de teste/escala (testa ~15, 2-3 vencem, escala devagar) estão em `references/story-ads.md`. A verba/distribuição segue o resto desta skill; a arte é da `soft-designer`. **As 2 camadas (D2):** o ad de ATRAÇÃO é SEM CTA (a segmentação faz o trabalho) e o filtro de destino não o reprova; o ad de CONVERSÃO leva CTA com destino sem exceção.

## Passo 2.5, mapeia as peças nos 4 QUADRANTES (o que escalar, o que matar)
Antes de decidir a verba, separa as peças orgânicas dos últimos 30 dias em dois eixos, **números reais do perfil, nunca adjetivo** ("2,3% de likes/reach", não "bom engajamento"):
- **Eixo alcance:** quantas contas a peça atingiu (reach), comparado à média do perfil.
- **Eixo engajamento:** a métrica-chave do formato dividida pelo alcance (reel = watch time + sends/reach · carrossel = swipe-até-3 + saves/reach), comparada à média do perfil.

O cruzamento dá 4 quadrantes, e cada um tem um veredito de tráfego:

| Quadrante | Alcance | Engajamento | O que significa | Decisão de verba |
|---|---|---|---|---|
| **Estrela** | alto | alto | a peça prova ROI orgânico redondo | **turbina primeiro**, é a candidata número 1 (Atração ou Lead) |
| **Ouro de nicho** | baixo | alto | o algoritmo não distribuiu, mas quem viu amou | **turbina pra escalar o alcance** (a verba compra a distribuição que faltou), costuma ser a de melhor custo por seguidor |
| **Alcance raso** | alto | baixo | espalhou mas não prendeu (público errado ou promessa vazia) | **NÃO turbina como está**, o dinheiro amplifica o vazamento; volta pro gancho/público antes |
| **Abaixo do esperado** | baixo | baixo | não funcionou no orgânico | **mata**, turbinar é acelerar erro (Lei do Passo 0) |

**A leitura que decide:** a Estrela e a Ouro de nicho são as candidatas do Passo 2, nessa ordem. A Ouro de nicho é a jogada de maior alavanca do impulsionar, porque a verba faz exatamente o que faltou (dar alcance a algo que já provou que prende). A de Alcance raso é uma armadilha, o número grande de alcance engana; sem engajamento, turbinar só paga pra espalhar mais rápido o que não converte.

**Pauta orientada a dado (loop de volta pro orgânico):** o quadrante também vira pauta, não só verba. O que virou Estrela ou Ouro de nicho aponta o TEMA/ÂNGULO que o perfil deve repetir no orgânico, alimentando de volta a `soft-conteudo-carrossel/-reels/-headlines` (replica a fórmula que já provou). O Alcance raso e o Abaixo do esperado dizem o que parar de fazer. Você reporta essa leitura em 1-2 linhas no doc, pra o especialista decidir a próxima peça a partir do que os números mostraram, não do palpite.

Se faltar o número de alcance ou de engajamento de alguma peça, marca `[DADO: confirmar]` e pede numa mensagem, jamais classifica no quadrante por estimativa (Lei 5).

## Passo 3, define público, verba e duração
- **Público:** interesse do nicho (não inclui concorrente) · lookalike de seguidores (se já tem 1.000+ qualificados) · custom de quem visitou o perfil 30 dias. Mantém entre 100k-500k: amplo demais ("Brasil 18-65") queima verba, estreito demais (5k) o algoritmo não escala.
- **Verba/duração (solo iniciando):** R$10-15/dia por peça, 3-7 dias (R$30-105 por peça).

## Passo 4, distribui a verba (50/30/20)
Metade da verba é **Distribuição Pura**, não captação: aparecer com vídeo longo pra construir público customizado de qualidade (quem assiste 90% vira base de remarketing futuro muito superior).

| Função | % da verba |
|---|---|
| Distribuição Pura (atração via vídeo longo) | 50% |
| Lead (DM ou Carta) | 30% |
| Remarketing (quente, 30-90 dias) | 20% |

## Passo 5, a régua de decisão e o ROI (revê a cada 2 dias)
**Custo por seguidor (proxy de criativo + segmentação):**

| Custo por seguidor | Decisão |
|---|---|
| até R$0,80 | bom, aumenta a verba 50% por +7 dias |
| R$0,80 a R$0,99 | troca o público (fadiga ou segmentação errada) |
| R$1,00 ou mais | cara, pausa essa peça e sobe a próxima da lista |

**ROAS de palco × ROI de empresa:** ROAS muito alto sinaliza SUBINVESTIMENTO. Escalar é aceitar ROAS menor com verba maior, porque o ROI absoluto cresce (retorno de R$5.000 com ROAS 10x perde, em ROI, pra R$25.000 com ROAS 5x). **Sempre calcula o ROI mensal absoluto, não só o ROAS.**

Quando o tráfego já roda e não retorna, diagnostica **UM gargalo + UM fix por vez** (tabela completa em `references/modo-impulsionar.md` §10): custo por DM alto → CTA fraco (reescreve na `soft-conteudo-headlines`) · DMs chegam sem fechar → Carta ou público errado · tráfego roda mas o perfil não cresce → bio/destaques (volta pra `soft-posicionamento`).

## Passo 6, confere o plano (gate interno) e PARA
Antes de entregar, confere internamente (a tabela NÃO vai pra saída):

| Check | Passa se |
|---|---|
| **Pré-requisitos** | os 5 do Passo 0 cumpridos; algum faltando = PARA, não entrega plano |
| **Números reais** | toda métrica vem do perfil real; número inventado/plausível = refaz e marca `[DADO: confirmar]` |
| **Quadrante** | as candidatas são Estrela ou Ouro de nicho (Passo 2.5); nada de Alcance raso ou Abaixo do esperado na lista de turbinar |
| **Distribuição** | a verba respeita o 50/30/20 (ou justifica o desvio em 1 linha) |
| **Régua definida** | cada peça tem objetivo · público · verba/dia · duração · métrica-chave + a decisão por custo |
| **ROI calculado** | o plano mostra o ROI mensal absoluto, não só o ROAS |
| **Acionável** | o especialista sai sabendo o que turbinar, com quanto, por quanto tempo, pra qual público |

Mostra **só o plano LIMPO** e PARA pro especialista decidir antes de ligar a verba ou diagnosticar outra campanha. Não narra o fluxo.

## When NOT to use (manda pra skill certa)
- Pediu a **arte/visual/PNG do anúncio** → **soft-designer**.
- Pediu o **CORPO/copy ou o CTA** da peça a ser turbinada → **soft-conteudo-carrossel / -reels / -headlines**.
- Pediu **lançamento pago tático** (evento, ingresso pago, congresso, pico) → **soft-lancamento-pago** (degrau 3).
- Pediu o **Plano / posicionamento / perfil** → **soft-posicionamento**.
- Pediu **diagnóstico de Story pago / infiltrado** → **soft-conteudo-stories**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Montou plano sem os pré-requisitos | Passo 0 é bloqueante: para e diz o que falta antes de qualquer verba |
| Turbinou peça sem teste orgânico | Só turbina peça com 40+ curtidas orgânicas naturais (acelerar erro queima dinheiro) |
| Turbinou a peça de Alcance raso (muito reach, pouco engajamento) | O número grande de alcance engana; sem engajamento a verba só espalha o vazamento. Turbina Estrela ou Ouro de nicho (Passo 2.5), nunca Alcance raso como está |
| Classificou a peça no quadrante por estimativa | Alcance e engajamento vêm do perfil real; sem o número, marca `[DADO: confirmar]` e pergunta |
| Verba de R$5/dia | Mínimo R$10-15/dia, senão o algoritmo não aprende |
| Tudo em Lead, nada em Distribuição Pura | Aplica os 50% de Distribuição: é o público de remarketing futuro |
| Olhou só o ROAS | Calcula o ROI mensal absoluto; ROAS alto pode ser subinvestimento |
| Público amplo demais ("Brasil 18-65") | Interesse do nicho ou lookalike; mantém 100k-500k |
| Inventou um número do perfil | Só número real; sem fonte, marca `[DADO: confirmar]` e pergunta |
| Mesmo criativo 30+ dias | Refresca a cada 14 dias (a fadiga sobe o custo) |
| Entregou o plano sem o que falta declarado | Lei 5: admite o furo, marca `[DADO: confirmar]`, nunca inventa o número |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `references/modo-impulsionar.md`: a engenharia completa do impulsionar (pré-requisitos, 2 níveis, 3 funções, ROAS×ROI, Distribuição Pura, régua de custo por seguidor, workflow de turbinar em 6 passos, anti-padrões e a tabela de diagnóstico §10). É a fonte da verdade do tema. **Dirigida em todos os passos.**
- `references/metricas.md`: as métricas que importam por formato + o duplo filtro (algorítmico × financeiro, "cada post é cheque") + o princípio do comparativo interno (teu perfil é a bússola, não o benchmark de fora). **Dirigida nos Passos 2 e 5.**
- `references/ads-de-webinar.md`: a COPY do anúncio de tráfego frio que enche o WEBINAR (promessa do webinar em ADMA <15s, bateria ângulos×temperos, legenda, gate próprio). Era a skill soft-conteudo-impulsionar, fundida aqui. **Dirigida quando o tráfego pago for pra encher um webinar** (a verba/régua é o resto desta skill; a arte é da soft-designer).
- `references/story-ads.md`: o STORY AD, o anúncio que não parece anúncio (associação + curiosidade, sem promessa/CTA, foto/vídeo real, segmentação óbvia, teste/escala e diagnóstico). **Dirigida no Passo 2 quando o criativo de Atração for um story ad** (a régua de custo por seguidor e o ROI são os Passos 4-5; a arte é da soft-designer).
- `scripts/lint_copy.py`: no Claude Code, roda `python3 scripts/lint_copy.py` em qualquer CTA/copy que você reescrever pro criativo (reprova em-dash e "travar"). No chat não roda.
