# Mineração de benchmark, registro das rodadas

> Este arquivo é o **diário da mineração de fórmulas de headline**: como se garimpa fórmula nova de fora, com que fontes, e o que a Rodada 1 produziu (metodologia, dedup, limitações, próxima rodada). É a memória que impede repetir garimpo já feito e importar fórmula fraca. Toda fórmula que entra na skill (cânone ou incubadora) passa por aqui primeiro. O comando `minera benchmark de [tema]` roda uma rodada nova com dedup e devolve veredito ANTES de propor candidato.

## Índice
- [Metodologia](#metodologia)
- [Fontes por Tier](#fontes-por-tier)
- [Rodada 1, tabela de dedup](#rodada-1-tabela-de-dedup)
- [Limitação da Ads Library](#limitacao-da-ads-library)
- [Rodada 2 pendente](#rodada-2-pendente)
- [Regra de autoria e neutralização](#regra-de-autoria-e-neutralizacao)

## Metodologia

A mineração busca **fórmula de headline com proxy de performance** (não só "headline bonita"), destila a estrutura, checa se já existe no cânone (dedup) e classifica o que sobra em: **redundante** (funde no T/C existente), **refinamento** (vira nota sob um T existente), **fora de escopo** (não é headline) ou **novo candidato** (entra na incubadora `templates-candidatos.md` com C-número, sob quarentena até bater baseline em 2 peças reais do dono).

O **dedup é obrigatório**: antes de nomear qualquer candidato novo, a fórmula minerada é confrontada com os 30 templates T e os candidatos C existentes. Se colide, não vira C novo. Esse passo é o que impede o cânone de inchar com sinônimos.

## Fontes por Tier

**Tier 1 (com proxy de performance medido):**
- **Hormozi:** 25 Video Hooks, os top-10 posts medidos, o material $100M Hooks. Proxy = engajamento/retenção real.
- **Retenção de vídeo curto (TikTok/Reels):** 71% decidem nos 3s; 85%+ de retenção = ~2,8x views; limiar prático de retenção 65-70%; 70-85% = ~2,2x.
- **Títulos de YouTube:** base SubSub de 120.703 títulos (mediana de top performers ~8 palavras, sweet spot 50-60 caracteres); Backlinko sobre ~4M de resultados (40-60 caracteres = +8,9% CTR; pronomes eu/você elevam CTR); doutrina MrBeast de título/thumb.
- **Assunto de e-mail:** Belkins sobre 5,5M de e-mails (pergunta 46% abertura, 2-4 palavras 46%); Klenty sobre 255k+ (interrogação 20% vs 12%, valor monetário 29% vs 13%; "coisa rápida" de colega +8pts; jargão/urgência genérica derruba a abertura pra baixo de 36%).

**Tier 2 (referência de estrutura, sem proxy medido, citável):**
- Copyblogger, Caples (Tested Advertising Methods), fórmula das 4U's, swipe files clássicos de estrutura (Brunson e afins como coletânea de estrutura).

**Fontes BR do insumo:** os criadores BR citados no material de origem foram **neutralizados** no produto (viram "criadores BR" sem nome). O lastro que aparece nas references é sempre o distante e citável (Hormozi, Caples, Copyblogger, Backlinko, Belkins, Klenty, SubSub, bases de estudo). Ver [regra de autoria](#regra-de-autoria-e-neutralizacao).

## Rodada 1, tabela de dedup

Confronto das fórmulas mineradas na Rodada 1 contra o cânone existente.

**Redundantes (fundem no T/C existente, NÃO viram fórmula nova):**

| Fórmula minerada | Funde em |
|---|---|
| "everyone-talks-X" (todo mundo fala de X) | T5 / T28 |
| "difference-X-Y" (a diferença entre X e Y) | T13 |
| "X-vs-Y" | T13 |
| "how-to-without" (como fazer X sem Y) | C1 |
| "MBA-em-X" | T10 |
| "how-x-used-y" (como X usou Y) | C6 |
| "one-word-changed" (mudei uma palavra) | C2 / T21 |
| "easier-than-you-think" (mais fácil do que parece) | C3 |
| "still-time" (ainda dá tempo) | T24 |
| "making-these-mistakes" (você comete estes erros) | C5 / T30 |
| "who-else-wants" (quem mais quer) | T16 / C1 |
| "warning" (alerta/aviso) | T15 |

**Refinamentos (viram nota sob um T existente, ver `templates.md` Seção de notas):**

| Fórmula minerada | Vira refinamento de |
|---|---|
| "stop-doing-X" (imperativo-negativo) | T1 (segunda face: proibição) |
| callout "isso é pra você" falado | T9 / T15 / T20 (ultraespecífico ≤7 palavras) |
| reveal-first (número cru primeiro) | C6 / C7 |
| "mudei UMA coisa e [resultado]" 1ª pessoa | C2 / T21 |
| "é mais fácil do que você imagina" | C3 (obstáculo mental) |
| urgência de janela só com deadline real | T24 |
| "quem mais quer [resultado]?" (3ª pessoa) | T16 |

**Fora de escopo (não é headline):**

| Item | Por quê fora |
|---|---|
| escada de stakes ($1 vs $1B) | é técnica de **retenção** ao longo do vídeo, não de headline de abertura |

**Novos candidatos (viram C-número na incubadora, `templates-candidatos.md`):**

| Candidato | Padrão |
|---|---|
| **C9** | promessa com prazo crível |
| **C10** | espia meu ativo privado |
| **C11** | experimento documentado |
| **C12** | credencial emprestada na frente |

> Nota de numeração: os candidatos novos começam em **C9** porque **C1-C6** já estão ocupados pelo cânone de ângulos ortogonais (Número, Contrária, Transformação, Autoridade, Confissão, Futuro), documentado no `templates.md`. C7 e C8 ficam reservados a refinamentos de ângulo da Rodada 1 (reveal-first e obstáculo-mental) que ainda vivem como nota sob T, não como ângulo nomeado autônomo.

## Limitação da Ads Library

A **Meta Ads Library não é raspável** de forma confiável (sem export estruturado, sem proxy de performance direto no anúncio). O proxy usado no lugar: um anúncio **ativo há 30+ dias com variações** é sinal de que está performando (ninguém queima verba 30 dias num criativo que não retorna). A leitura fina disso fica pra Rodada 2, por **browse manual**.

## Rodada 2 pendente

Escopo da Rodada 2 (ainda não rodada): **browse manual da Meta Ads Library BR**, filtrando por termos de campanha comum no nicho (aula gratuita, método, faturamento, vagas abertas), pegando anúncios **ativos 30+ dias com variações** como proxy de performance, e passando cada fórmula pelo mesmo dedup desta reference antes de propor candidato.

No app **sem web** (Claude no chat, sem browse): o comando `minera benchmark de [tema]` conduz com **o que o dono colar** (headlines de concorrente, prints de anúncio, títulos que ele viu performar), roda o dedup contra o cânone e devolve o **veredito** (redundante / refinamento / fora de escopo / candidato novo) antes de propor qualquer C novo. Nunca inventa dado de benchmark que não veio de fonte.

## Regra de autoria e neutralização

**Autoria Opção C:** o lastro citável nas references é **distante** (Hormozi, Caples, Copyblogger, Backlinko, Belkins, Klenty, SubSub, bases de estudo). Os **mentores e criadores BR** do material de origem **não aparecem** na skill: são neutralizados como "criadores BR" sem nome. A skill não credita o método a ninguém do insumo; credita o lastro externo distante que qualquer um pode conferir.
