---
name: soft-trafego-meta
description: Executa tráfego pago no Meta (Facebook/Instagram) de verdade, cria campanha ODAX, sobe criativo, lê métrica, escala ou pausa, e publica post + liga a automação comentário-para-DM, tudo na conta do próprio dono via MCP oficial da Meta ou Marketing API. É a MÃO que opera a plataforma; a CABEÇA que DECIDE o que turbinar, verba, 50/30/20 e régua mora na soft-conteudo-impulsionar (é o gate de entrada desta skill). Use quando o pedido for "sobe/cria/ativa a campanha", "publica o carrossel no Instagram", "liga o comment-to-DM", "puxa as métricas da conta", "pausa/escala a campanha", "conecta minha conta de anúncios", "auditar a conta de ads", "por que a campanha não entrega". NÃO use pra DECIDIR estratégia de verba, distribuição ou diagnóstico de retorno (soft-conteudo-impulsionar), nem pra a COPY/CTA do anúncio (soft-conteudo-headlines/-carrossel/-reels), nem pra a ARTE (soft-designer), nem pra lançamento com evento/ingresso (soft-lancamento-pago).
---

# Tráfego Meta, a mão que executa na plataforma (a cabeça é a impulsionar)

Esta skill NÃO decide estratégia. Ela EXECUTA na conta de anúncios do dono o que a `soft-conteudo-impulsionar` já decidiu: cria a campanha, sobe o criativo, lê a métrica, escala ou pausa. E faz o outro par de mãos: **publica o post** (carrossel/imagem/reel) no Instagram e **liga a automação comentário-para-DM**. Toda operação gasta ou pode gastar dinheiro real, então a regra-mãe é uma: **nada entra no ar sem OK explícito do dono, toda campanha nasce PAUSED.**

**Fronteira dura (decore):**
- **soft-conteudo-impulsionar = CABEÇA.** Decide o QUE turbinar (peça com ROI orgânico), quanta verba, quantos dias, qual público, a distribuição 50/30/20, a régua de custo por seguidor, o ROI. Roda no chat sem credencial nenhuma. É onde o plano nasce.
- **soft-trafego-meta (esta) = MÃO.** Pega o plano APROVADO e executa na plataforma via API. Precisa das credenciais do dono. Nunca inventa estratégia; se o plano não veio da impulsionar, PARA e manda montar lá primeiro.

## GATE DE ENTRADA (bloqueante, não pule)
Só executa se as duas condições abaixo estiverem cumpridas. Se qualquer uma falha, PARA e diz o que falta, não toca na conta:

1. **Os 5 pré-requisitos da soft-conteudo-impulsionar** (herdados inteiros): (a) posicionamento de pé (Plano); (b) perfil convertendo (visita → seguir); (c) destino no ar: Mini Carta / isca / DM com palavra, **exceção**: o ad de ATRAÇÃO/story ad é CTA-less por desenho, o filtro de destino vale só pro ad de CONVERSÃO; (d) ≥1 peça orgânica acima da média do perfil; (e) primeira venda do método já fechada.
2. **Plano de tráfego aprovado**, vindo da impulsionar: cada peça com objetivo · público · verba/dia · duração · métrica-chave, e a distribuição no 50/30/20. Sem plano, não há o que executar.

> Se o dono chegou pedindo "sobe a campanha" mas não passou pela impulsionar, sua primeira resposta é: "Antes de subir preciso do plano de verba (o que turbinar, quanto, quanto tempo, qual público). Vamos montar na impulsionar?", e para.

## Output Contract (o que você entrega)
- **No Claude Code / agente (tem Bash + credencial):** a operação EXECUTADA na conta: IDs criados (campaign_id, adset_id, ad_id, creative_id), o post publicado (media_id + permalink), a automação ligada (id + status), as métricas lidas (tabela). Tudo nasce PAUSED; a ativação é uma call separada COM OK do dono. A entrega final é um **arquivo `.md`** (o runbook do que foi feito + IDs + próximos passos) cujo **path completo vai na resposta**.
- **No app/chat (sem Bash):** você NÃO opera a plataforma. Entrega o **checklist de execução pronto pra colar** (a sequência exata de calls/campos que quem tem a credencial roda) + as **copys/legendas finais** + o mapa de campos da automação, tudo num doc MD. Deixa claro que a execução na conta acontece no Code/agente.
- Você **nunca ativa campanha nem muda budget sem OK explícito**. Você **nunca inventa uma métrica**: número vem da API real; sem leitura, marca `[LER: rodar insights]`.

## ⚠️ ENTREGA = UM doc MD, SEMPRE
O RESULTADO desta skill sai como **UM documento markdown consolidado**. No **claude.ai**, um **artifact de markdown** (o dono abre, copia, baixa); no **Claude Code / agente**, um **arquivo `.md`** salvo no disco cujo **path completo vai na resposta**. A CONDUÇÃO (perguntas, os STOPs de aprovação, "pode ativar?") acontece no chat; o RUNBOOK/checklist/IDs moram no DOC. No agente/Telegram, a resposta ao dono é sem markdown pesado (sem tabela crua, sem bloco de código gigante): frase curta + o path do arquivo. Sem o doc entregue, a skill não terminou.

## Os 3 ambientes (a mesma skill, entrega diferente)
| Ambiente | Tem Bash? | O que esta skill faz | Entrega |
|---|---|---|---|
| **app / chat (claude.ai)** | Não | Prepara tudo: monta o checklist de calls, as copys/legendas prontas, o mapa de campos da automação | Doc MD com checklist + copys; avisa que a execução na conta roda no Code/agente |
| **Claude Code** | Sim | Executa via MCP/Marketing API com as credenciais do `.env`: cria campanha/adset/ad, publica post, liga automação, lê métrica | Operação feita + arquivo `.md` (runbook + IDs + permalink) com o path na resposta |
| **agente / Telegram** | Sim | Igual ao Code, com as credenciais do dono no ambiente | Operação feita; resposta ao dono = frase curta sem markdown pesado + **path completo do arquivo** |

## PASSO 0: Confirma via de execução e credenciais
Duas vias, a skill usa a que estiver disponível:

**Via A, MCP oficial da Meta** (mais limpo, OAuth, sem credencial de dev). Endpoint único: `https://mcp.facebook.com/ads`. O dono conecta uma vez (login Meta + autoriza a conta de anúncios). Cobre Facebook + Instagram Ads. Limite ~200 chamadas/hora por conta. **Acesso de escrita TOTAL sem rascunho/undo/confirmação da Meta**, por isso a regra de ouro (nasce PAUSED, ativar só com OK).

**Via B, Marketing API direto** (o que a casa já usa). Credenciais no ambiente:
- `META_ACCESS_TOKEN` (ou `_LEO`): token da conta.
- `META_AD_ACCOUNT_*`: a conta de anúncios (`act_<id>`).
- `META_PAGE_ID`: a Página, obrigatória pro criativo.
- `META_LEOMOLINA_PIXEL` (+ CAPI token): pixel/dataset, obrigatório pra objetivo SALES + site.
- Publicação de post no IG: token do tipo Instagram Login em `graph.instagram.com`.

No **app/chat** não há credencial: você só prepara o checklist. No **Code/agente**, confere quais variáveis existem antes de operar; se faltar a que a operação precisa, PARA e pede ao dono (sem inventar).

> Detalhe completo das duas vias, os tools do MCP e os endpoints da Marketing API estão em `references/meta-api.md`. **O corpo abaixo já é executável; a reference é só profundidade.**

## PASSO 1: Auditoria da conta (antes de criar nada)
Antes de subir campanha nova, diagnostica a conta na sequência canônica (nunca pule pra "criar" numa conta que já queima verba):

1. Lista contas (descobre `act_<id>`, confere que a conta está habilitada).
2. Opportunity score (0-100, **nível de CONTA**, nunca atribua a uma campanha).
3. Sinal de anomalia (desvio, é observação não causa).
4. Benchmarks de leilão + de indústria (competitividade, audiência sobreposta).
5. Erros de entrega (só hard-stops, não performance).

**No Code/agente:** roda as calls e lê. **No app:** entrega a sequência como checklist. Se a conta tiver problema estrutural (erro de entrega, pixel morto), PARA e reporta antes de criar campanha.

## PASSO 2: Cria a estrutura (tudo nasce PAUSED)
Hierarquia da Meta: **Campanha → Conjunto de anúncios (ad set) → Anúncio (ad) → Criativo.**

1. **Campanha**: objetivo ODAX (`OUTCOME_AWARENESS/TRAFFIC/ENGAGEMENT/LEADS/SALES/APP_PROMOTION`). Nunca objetivo legado. O objetivo vem do plano da impulsionar (a função Atração/Lead/Remarketing mapeia pro objetivo). **Otimize pra VENDA, não pra lead**: quando o destino é venda, o objetivo é `OUTCOME_SALES` e a otimização é conversão de compra, não volume de lead barato. Budget na campanha = CBO; deixe vazio pra ABO (budget no ad set). CBO e ABO são mutuamente exclusivos.
2. **Ad set**: público (do plano), posicionamentos, agenda, e o budget se ABO. Pra `OUTCOME_SALES` + site, o `promoted_object` com o **pixel** é OBRIGATÓRIO (sem ele a campanha não otimiza pra compra).
3. **Ad**: liga o ad set ao criativo. Precisa de `ad_set_id`, `ad_name`, `creative`.
4. **Criativo**: a peça (imagem/vídeo + copy). A COPY e o CTA vêm da `soft-conteudo-headlines/-carrossel/-reels`; a ARTE vem da `soft-designer`. Aqui você só monta o creative object (precisa do `page_id`).

**Story ad em 2 camadas (herdado da impulsionar, respeite na execução):**
| Camada | CTA no criativo | Objetivo típico |
|---|---|---|
| **ATRAÇÃO** (story ad) | **SEM CTA** (a segmentação faz o trabalho; não force botão) | tráfego/alcance qualificado, métrica = custo por visita ao perfil R$0,15-0,25 |
| **CONVERSÃO** (carrossel 3C, reel com hook, oferta) | **CTA com destino, sem exceção** | LEADS ou SALES, leva a destino no ar (Mini Carta, isca, DM, checkout) |

Cobrar CTA/destino de um story ad de atração quebra a camuflagem que o faz funcionar. Não faça.

**STOP**, mostra a estrutura montada (ainda PAUSED) e pergunta "pode ativar?". Não ativa por conta própria.

## PASSO 3: Publica o post + liga o comment-to-DM (quando o pedido for publicação)
Quando o pedido é publicar um post orgânico e ligar a automação (não uma campanha paga), o fluxo é:

**Publicação (Instagram, `graph.instagram.com`, NÃO facebook):**
1. Cada card do carrossel numa **URL pública própria** (Cloudflare Pages / hospedagem estática do negócio, `CLOUDFLARE_API_TOKEN` no ambiente). **NUNCA** Litterbox/Catbox/Imgur: o scraper da Meta bloqueia (erro 9004). Valida que respondem 200 antes de publicar; se a Meta rejeitar o JPEG (erro 36001), recompress `quality=92, optimize=True` e adiciona `?v=$(date +%s)` pra furar o cache.
2. Cria N containers `is_carousel_item=true` → espera cada `status_code=FINISHED` → cria container `media_type=CAROUSEL` com `children` + `caption` → `media_publish` com `creation_id`. Salva o `media_id` e pega o `permalink`.

**Automação comment-to-DM** (liga o comentário com a palavra-chave ao DM, entregando o lead pro fluxo de vendas):
- Campos: `media_id` do post · `keywords` (a palavra-chave do CTA, ex. "QUERO") · `reply_public_variants` (5 variações da resposta pública, pra não soar bot) · `dm_text` (no tom do dono, sem link cru) · `dm_buttons` com **`quick_reply`** (payload único e descritivo) · `delay_seconds: 3`.
- **Regra dura:** o botão é `quick_reply`, NÃO `web_url`. `quick_reply` entrega o lead pro fluxo do SDR (a conversa chega no DM e o vendedor assume); `web_url` abre link externo mas NÃO entrega pro fluxo. Pra handover, sempre `quick_reply`.
- A Private Reply leva o botão anexado JUNTO no mesmo payload, nunca numa 2ª chamada.

**STOP**, publicação e automação também são ações no ar. Mostra a legenda + os campos da automação e pergunta "publico e ligo?". No app, entrega tudo como checklist (você não tem como publicar sem credencial).

## PASSO 4: Ativa (só com OK) e depois lê as métricas
- **Ativar:** a hierarquia inteira precisa estar ativa pra entregar; ativa de cima pra baixo (campanha → ad set → ad). É uma call separada, SEMPRE com o "pode ativar?" respondido pelo dono.
- **Ler métrica:** a leitura principal puxa por nível (`campaign/adset/ad`), com os campos (inclui id+name), filtro, ordenação, breakdowns e janela de tempo. Pra ver topo E fundo, duas leituras com ordenação invertida.
- A DECISÃO sobre o que a métrica significa (continuar/trocar público/pausar/escalar, ROI absoluto) é da **soft-conteudo-impulsionar**: esta skill LÊ e ENTREGA o número; a leitura da régua volta pra cabeça. Você executa o que a régua mandar (pausar a peça cara, escalar a vencedora devagar: R$50→R$70, não pula de 30 pra 300).

## PASSO 5: Gate interno e PARA
Antes de entregar, confere (a tabela NÃO vai pra saída):

| Check | Passa se |
|---|---|
| **Gate de entrada** | os 5 pré-requisitos + plano aprovado da impulsionar; algum faltando = PARA, não toca na conta |
| **Nasce PAUSED** | nada foi ativado sem o "pode ativar?" respondido pelo dono |
| **Objetivo certo** | ODAX (nunca legado); SALES+site tem pixel no `promoted_object`; otimiza pra venda não pra lead barato |
| **Métrica real** | todo número vem da API; sem leitura, marca `[LER: rodar insights]`, nunca inventa |
| **quick_reply** | a automação usa `quick_reply` (entrega o lead), não `web_url` |
| **Doc + path** | a entrega é UM doc MD; no Code/agente o path completo do arquivo vai na resposta |

Mostra só o resultado LIMPO (IDs, permalink, métricas ou checklist) e PARA. Não narra o fluxo.

## Exemplo denso (inline): subir uma campanha SALES de conversão via Marketing API
> Plano aprovado na impulsionar: turbinar o carrossel "3 erros que enterram a agenda" (28 saves orgânicos, acima da média), função LEAD→venda, R$40/dia, 7 dias, público lookalike 1% dos compradores, destino = Mini Carta no ar. Gate de entrada: 5 pré-requisitos ok, plano aprovado. Ambiente: Claude Code, Via B (Marketing API).

1. **Auditoria** (Passo 1): leio opportunity score da conta (`act_...`), anomalia, erros. Conta limpa, sem hard-stop. Sigo.
2. **Campanha** (Passo 2): crio `OUTCOME_SALES`, ABO (budget vazio na campanha), status `PAUSED`. Nome: `SALES · carrossel-agenda · lookalike1 · 2026-07`.
3. **Ad set**: budget R$40/dia, público lookalike 1% dos compradores (100k-500k), posicionamento Instagram feed+stories, `promoted_object` com o `META_LEOMOLINA_PIXEL` e evento `PURCHASE` (obrigatório pra SALES+site). Otimização = conversão de compra, **não** cliques nem leads.
4. **Criativo**: monto o creative com o `META_PAGE_ID`, os cards já hospedados no Cloudflare Pages (respondendo 200), a legenda aprovada (veio da soft-conteudo-carrossel, passou no anti-ia), CTA "Saiba mais" → link da Mini Carta.
5. **Ad**: ligo ad set + creative. Tudo `PAUSED`.
6. **STOP**: mostro os IDs criados (campaign/adset/ad) e a estrutura, pergunto "pode ativar? Vai gastar R$40/dia por 7 dias (R$280)."
7. Com o OK: ativo de cima pra baixo (campanha → ad set → ad).
8. **Entrega**: salvo `runbook-campanha-agenda-2026-07-04.md` com os IDs, a verba, a janela e "revisar métrica em 2 dias e voltar pra impulsionar decidir continuar/pausar". Respondo com o path completo do arquivo.

## When NOT to use (manda pra skill certa)
- Pediu pra **DECIDIR** o que turbinar, quanta verba, distribuição 50/30/20, ou diagnóstico "não retorna" → **soft-conteudo-impulsionar** (a cabeça; esta skill é só a mão).
- Pediu a **COPY/CTA** do anúncio ou da legenda → **soft-conteudo-headlines / -carrossel / -reels**.
- Pediu a **ARTE/PNG/visual** do criativo ou dos cards → **soft-designer**.
- Pediu **lançamento pago tático** (evento, ingresso, congresso, pico de data) → **soft-lancamento-pago**.
- Pediu o **Plano / posicionamento / perfil** → **soft-posicionamento**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Ativou campanha ou mudou budget sem OK | Regra de ouro: nasce PAUSED, ativar é call separada COM o "pode ativar?" respondido |
| Executou sem o plano da impulsionar | Gate de entrada: sem plano aprovado, PARA e manda montar na impulsionar |
| Objetivo legado (LINK_CLICKS, BRAND_AWARENESS) | Só ODAX (`OUTCOME_*`) |
| Otimizou pra lead barato numa campanha de venda | Otimiza pra VENDA (conversão de compra); lead barato enche de curioso, não de comprador |
| CBO + budget no ad set ao mesmo tempo | Mutuamente exclusivo: escolhe um |
| SALES + site sem pixel no `promoted_object` | Pixel obrigatório, senão não otimiza pra compra |
| Atribuiu opportunity score a uma campanha | É nível de CONTA, nunca de campaign/adset/ad |
| Automação com botão `web_url` | Usa `quick_reply` (entrega o lead pro fluxo); `web_url` não entrega |
| Hospedou os cards em Litterbox/Catbox/Imgur | O scraper da Meta bloqueia (9004); usa Cloudflare Pages / hospedagem própria, valida 200 |
| Publicou post pelo `graph.facebook.com` | Post IG roda em `graph.instagram.com`, token Instagram Login |
| Inventou uma métrica de campanha | Só número da API; sem leitura, marca `[LER: rodar insights]` |
| Forçou CTA num story ad de atração | Atração é CTA-less por desenho; CTA quebra a camuflagem, vale só no ad de conversão |
| Escalou a peça vencedora de 30 pra 300 | Escala devagar (R$50→R$70); salto queima o aprendizado do algoritmo |

## References (só pra profundidade, o corpo acima é autossuficiente)
- `references/meta-api.md`: as duas vias de execução (MCP oficial `mcp.facebook.com/ads` com o mapa dos tools × Marketing API direta com os endpoints e credenciais da casa), a estrutura oficial da campanha, os workflows canônicos (auditoria, criar SALES, não-entrega) e os anti-patterns técnicos da API. **Fonte da verdade da execução.**
- `references/publicacao-e-automacao.md`: a publicação de post no `graph.instagram.com` (containers → carrossel → publish) e a automação comment-to-DM (campos, `quick_reply` vs `web_url`, Private Reply, os gotchas de hospedagem/cache/token). **Dirigida no Passo 3.**
