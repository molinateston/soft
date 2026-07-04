# reference: execução Meta Ads (duas vias: MCP oficial × Marketing API)

> Memória operacional de quem opera a conta de anúncios de verdade. As duas vias de execução, a estrutura oficial da campanha, os workflows canônicos e os anti-patterns da API. O corpo da SKILL.md já é executável; aqui mora a profundidade que o app não abre.

## Índice
- 0. As duas vias (quando usar cada)
- 1. Estrutura oficial de uma campanha
- 2. Via A: MCP oficial da Meta (mapa dos tools)
- 3. Via B: Marketing API direta (endpoints + credenciais da casa)
- 4. Otimizar pra VENDA, não pra lead
- 5. Workflows canônicos
- 6. Anti-patterns técnicos da API
- 7. Regra de ouro de segurança

---

## 0. As duas vias (quando usar cada)

A skill executa pela via que estiver disponível no ambiente. As duas fazem a mesma coisa; muda a autenticação.

| | Via A, MCP oficial | Via B, Marketing API direta |
|---|---|---|
| Autenticação | OAuth da própria Meta, sem credencial de dev | token de acesso da conta (`META_ACCESS_TOKEN`) |
| Setup | o dono conecta 1x (login + autoriza a conta) | credenciais já no ambiente da casa |
| Endpoint | `https://mcp.facebook.com/ads` | `https://graph.facebook.com/<versão>/...` |
| Cobre | Facebook + Instagram Ads | Facebook + Instagram Ads |
| Limite | ~200 chamadas/hora por conta de anúncios | limite de rate do app/token |
| Escrita | TOTAL, sem rascunho/undo/confirmação da Meta | TOTAL, idem |
| Quando usar | quando o dono conectou o conector oficial | quando a casa opera por token (default hoje) |

Regra: **prefira a Via A quando o conector estiver plugado** (mais limpa, sem gerir token). Se não estiver, roda pela **Via B** com os tokens da casa. Nenhuma das duas tem undo, a segurança está na regra de ouro (Seção 7), não na plataforma.

---

## 1. Estrutura oficial de uma campanha

Hierarquia: **Campanha → Conjunto de anúncios (ad set) → Anúncio (ad) → Criativo.**

- **Campanha:** define o objetivo (ODAX) e, se CBO, o orçamento. Objetivos ODAX válidos: `OUTCOME_AWARENESS`, `OUTCOME_TRAFFIC`, `OUTCOME_ENGAGEMENT`, `OUTCOME_LEADS`, `OUTCOME_SALES`, `OUTCOME_APP_PROMOTION`. Nunca objetivo legado (`LINK_CLICKS`, `BRAND_AWARENESS`, `CONVERSIONS` antigo, etc.).
- **Ad set:** público (targeting), posicionamentos, agenda e o orçamento se ABO. O `promoted_object` com `pixel_id` (+ evento, ex. `PURCHASE`) é OBRIGATÓRIO pra `OUTCOME_SALES` + site. **CBO (budget na campanha) e budget no ad set são mutuamente exclusivos**: escolhe um.
- **Ad:** liga o ad set ao criativo. Campos obrigatórios: `ad_set_id`, `ad_name`, `creative`.
- **Criativo:** a peça (imagem/vídeo + copy + CTA). Precisa de `page_id` (a Página do Facebook/Instagram). A COPY vem da soft-conteudo-*; a ARTE da soft-designer; aqui só se monta o objeto.
- **IDs envolvidos:** conta de anúncios (`act_<id>`), Página (`page_id` / `META_PAGE_ID`), Pixel/Dataset (`META_LEOMOLINA_PIXEL` e afins). Descobertos pelos tools/endpoints de descoberta.

**Todo nível nasce PAUSED.** A entrega só acontece com a hierarquia inteira ativa; ativa de cima pra baixo (campanha → ad set → ad), sempre com OK do dono.

---

## 2. Via A: MCP oficial da Meta (mapa dos tools)

Endpoint único: `https://mcp.facebook.com/ads`. Os tools por categoria:

**Descoberta:**
- `ads_get_ad_accounts`: lista contas; cada item traz `is_ads_mcp_enabled` (se `false`, NÃO usar essa conta).
- `ads_get_pages_for_business`: pega o `page_id` pra montar o criativo.

**Criação (tudo nasce PAUSED; ativar é call separada COM OK do dono):**
- `ads_create_campaign`: objetivos ODAX. CBO se setar budget aqui; ABO se deixar vazio e setar no ad set.
- `ads_create_ad_set`: `promoted_object` com pixel obrigatório pra `OUTCOME_SALES` + `WEBSITE`.
- `ads_create_ad`: required: `ad_set_id`, `ad_name`, `creative`.
- `ads_update_entity`: modifica campaign/ad_set/ad. Pra pausar: `fields={"status":"PAUSED"}`.
- `ads_activate_entity`: PAUSED→ACTIVE. Ativar a hierarquia inteira, de cima pra baixo. SEMPRE com confirmação do dono.

**Reporting:**
- `ads_get_ad_entities`: leitura principal. Setar `level` (campaign/adset/ad), `fields` (incluir id+name), `filtering`, `sort`, `breakdowns`, `time_range`. Pra topo+fundo, 2 calls com `sort` invertido.

**Insights analíticos:**
- `ads_insights_advertiser_context`: overview business+funil (usar no início da auditoria).
- `ads_insights_performance_trend`: série temporal (CPC/CPM/CPR/ROAS/CTR/CVR).
- `ads_insights_anomaly_signal`: desvios (observação, não causa).
- `ads_insights_auction_ranking_benchmarks`: competitividade de leilão + audiência sobreposta.
- `ads_insights_industry_benchmark`: vs indústria.
- `ads_get_opportunity_score`: score 0-100 da CONTA. Recomendações por `opportunity_score_lift` (pontos). NUNCA atribuir a campanha/ad set/ad.

**Diagnóstico:**
- `ads_get_errors`: só hard-stops de entrega (não performance/pacing).
- `ads_get_help_article`: help center da Meta pra conceitos/políticas.

**Catalog** (precisa permissão `catalog_management`): `ads_catalog_get_catalogs` (listar antes de criar, regra "one catalog"), `ads_catalog_create` (`feed_url` XOR `items` XOR `feed_file_content` base64), `ads_catalog_get_details`, `ads_catalog_get_diagnostics` (MUST_FIX vs OPPORTUNITY), `ads_catalog_get_feed_rules`, `ads_catalog_get_products` (filtro `retailer_id` = SKU alfanumérico), `ads_catalog_get_product_details` (só FBID numérico), `ads_catalog_get_product_sets`, `ads_catalog_get_product_set_products`, `ads_catalog_get_product_feed_details`.

**Datasets / Pixel / CAPI:** `ads_get_dataset_details` (config + status; sinaliza `last_fired_time` velho = pixel morto), `ads_get_dataset_quality` (EMQ + match keys + freshness), `ads_get_dataset_stats` (lookback MÁX 28 dias; timestamps em Unix string, não ISO).

---

## 3. Via B: Marketing API direta (endpoints + credenciais da casa)

Base: `https://graph.facebook.com/<versão>/`. Credenciais no ambiente:
- `META_ACCESS_TOKEN` (ou `META_ACCESS_TOKEN_LEO`): o token.
- `META_AD_ACCOUNT_*` (`_DEFAULT`, `_LEO`, `_LEVIN`, `_ID`): a conta `act_<id>`.
- `META_PAGE_ID`: a Página.
- `META_LEOMOLINA_PIXEL` (+ `META_LEOMOLINA_CAPI_TOKEN`): pixel/dataset e o CAPI (conversões server-side). Outros pixels da casa: `META_MINIMAL_PIXEL`, `META_RECANTO_PIXEL_ID`.

Endpoints principais (o `<versão>` segue a atual da conta):
- **Descoberta:** `GET /me/adaccounts`, `GET /<ad_account_id>/` (campos `name,account_status`), `GET /<business_id>/owned_pages` ou `GET /me/accounts` (pega `page_id`).
- **Campanha:** `POST /act_<id>/campaigns`: body: `name`, `objective` (ODAX), `status=PAUSED`, `special_ad_categories=[]` (ou a categoria se for regulado), e `daily_budget` só se CBO.
- **Ad set:** `POST /act_<id>/adsets`: `name`, `campaign_id`, `daily_budget` (se ABO), `billing_event`, `optimization_goal` (ex. `OFFSITE_CONVERSIONS` pra SALES), `promoted_object` (`{pixel_id, custom_event_type:"PURCHASE"}` pra SALES+site), `targeting`, `status=PAUSED`.
- **Criativo:** `POST /act_<id>/adcreatives`: `name`, `object_story_spec` (com `page_id`, `instagram_actor_id`/`instagram_user_id`, e o `link_data`/`video_data` com imagem+copy+CTA).
- **Ad:** `POST /act_<id>/ads`: `name`, `adset_id`, `creative={creative_id}`, `status=PAUSED`.
- **Ativar/pausar:** `POST /<entity_id>` com `status=ACTIVE` ou `PAUSED`.
- **Insights:** `GET /<entity_id>/insights`: `level`, `fields` (`spend,impressions,clicks,cpc,cpm,ctr,actions,cost_per_action_type,purchase_roas`), `time_range`, `breakdowns`, `filtering`.

CAPI (conversão server-side, opcional mas melhora a otimização): `POST /<pixel_id>/events` com o `META_LEOMOLINA_CAPI_TOKEN`, enviando o evento `Purchase` com os dados hasheados do comprador.

---

## 4. Otimizar pra VENDA, não pra lead

Princípio herdado: uma campanha de venda otimiza pra **conversão de compra**, não pra volume de lead barato.
- Objetivo `OUTCOME_SALES`, `optimization_goal=OFFSITE_CONVERSIONS`, `promoted_object` com o pixel e `custom_event_type="PURCHASE"`.
- Lead barato enche a base de curioso que nunca compra; o algoritmo entrega pra quem clica fácil, não pra quem paga. A campanha de venda tem que ver o evento de compra pra aprender quem é comprador.
- Exceção legítima: a função **Lead** do plano (captura de DM/mensagem) usa `OUTCOME_LEADS` de propósito, porque ali o objetivo REAL é a conversa, não a compra imediata: mas isso é decisão da impulsionar, não default seu.
- A função **Atração** (story ad) usa tráfego/alcance; a métrica é custo por visita ao perfil (R$0,15-0,25), não conversão.

---

## 5. Workflows canônicos

**Auditoria de conta** (antes de criar qualquer coisa):
`get_ad_accounts` → `get_opportunity_score` → `anomaly_signal` → `auction_ranking_benchmarks` → `industry_benchmark` → `get_errors`. Se aparecer hard-stop de entrega ou pixel morto, PARA e reporta antes de criar campanha.

**Criar campanha SALES com pixel:**
`get_ad_accounts` → `get_pages_for_business` → `create_campaign` (ABO, sem budget na campanha) → `create_ad_set` (`promoted_object` com pixel + `PURCHASE`) → `create_ad` → revisar → **STOP, pede OK** → `activate_entity` (campanha → ad set → ad, em ordem).

**Campanha não entrega:**
`get_ad_entities` (acha os filhos com 0 impressões) → `get_errors` → `auction_ranking_benchmarks` → se for conversão, `dataset_quality` + `dataset_stats` (pixel disparando? EMQ ok?). Reporta o gargalo; a DECISÃO de fix (trocar público, refrescar criativo) volta pra impulsionar.

**Catálogo** (só se o negócio vende produto físico com feed): `get_catalogs` → `get_details` → `get_diagnostics(MUST_FIX)` → `get_diagnostics(OPPORTUNITY)` → `product_feed_details` + `feed_rules`.

---

## 6. Anti-patterns técnicos da API

- Ativar/mudar budget sem confirmação do dono (gasta dinheiro real, sem undo).
- Objetivo legado (só ODAX).
- CBO + budget no ad set ao mesmo tempo (mutuamente exclusivo).
- `OUTCOME_SALES` + site sem pixel no `promoted_object` (não otimiza pra compra).
- Otimizar campanha de venda pra lead/clique barato (enche de curioso).
- Atribuir Opportunity Score a campaign/ad set/ad (é nível de CONTA).
- Criar catálogo sem listar primeiro (perde signal; regra "one catalog").
- Confundir `retailer_id` (SKU alfanumérico) com FBID (numérico longo).
- Lookback > 28 dias em `dataset_stats`; timestamp em ISO 8601 (é Unix string).
- Usar uma conta com `is_ads_mcp_enabled=false` (não está habilitada; usa outra ou habilita no Business Manager).

---

## 7. Regra de ouro de segurança

O acesso (por qualquer via) é de **escrita total, sem rascunho, sem undo, sem tela de confirmação da Meta**. A segurança inteira está no protocolo, não na plataforma:

1. **Toda entidade nasce PAUSED.** Criar não gasta; ativar gasta.
2. **Ativar ou mudar budget é sempre uma call separada, COM o "pode ativar?" respondido pelo dono.** Mostra o plano (verba/dia × dias = total), pede o OK, só então ativa.
3. **Avisa 1x sobre risco** (custo, conta não habilitada, pixel morto) e, se o dono decidir seguir, segue sem insistir.
4. **Nunca inventa métrica.** Número vem da leitura real; sem leitura, marca `[LER: rodar insights]`.
