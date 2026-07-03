# Saídas obrigatórias do plano: páginas (captura + obrigado) + ângulos de anúncio

> **Regra:** todo Plano de Webinar termina com a **proposta de página de captura**, a **proposta de página de obrigado** e os **ângulos de anúncio (com headlines)**. Não é o código nem a arte (isso é `soft-webinar-paginas` / `soft-conteudo-headlines` / `soft-designer`): é a **copy-base derivada do plano**, pronta pra virar página e ad sem reabrir a estratégia. O funil inteiro nasce coerente porque nasce do mesmo doc.

> **Tudo DERIVA do plano, nada se inventa:** a página puxa a promessa (S2), os bullets/fascinations (S2b/S9), o mundo ideal e a voz (S0/S9); os ângulos puxam os pilares (inimigo, dor, mecanismo, prova, desejo). Furo de insumo = `[A CONFIRMAR]`, nunca preenchido com plausível (Lei 5).

---

## 1. A PÁGINA DE CAPTURA (proposta de copy)

Função: **uma só** (inscrever). Mobile-first, attention ratio 1:1. O molde que o plano cospe:

| Bloco | De onde vem | Molde |
|---|---|---|
| **Headline** | a Promessa (S2) | "Como [resultado que ele quer] sem [o que ele teme/odeia]" |
| **Sub-headline** | a categoria + o mecanismo (S0) | "Numa aula de [duração], o [nome da categoria]: [a tese em 1 linha]" |
| **3-5 bullets** | as fascinations (S2b/S9) | cada um um loop aberto ("por que X", "o único lugar onde Y", "como Z sem W") |
| **Prova rápida** | a autoridade calibrada (S0) | 1 número crível + quem fala ("[N] feito com [como], por [quem]") |
| **CTA (botão)** | o formato | verbo de posse + o que ganha ("Reservar meu horário" / "Quero minha vaga") |
| **Contra-filtro** | o avatar (S4) | "Não é pra você se [quem a aula NÃO serve]" (qualifica e eleva) |
| **Data/horário** | o webinar | o seletor de sessão (perpétuo) ou a data (ao vivo) |

Regras: prova DEPOIS da promessa · 1 objetivo, 1 CTA · o contra-filtro qualifica (não afasta). O código/layout final é `soft-webinar-paginas` (ou `soft-funil-landing`); aqui sai a **copy pronta pra colar**.

---

## 2. A PÁGINA DE OBRIGADO (proposta de copy)

Função: **subir o comparecimento** (não é "valeu, até logo"). O molde:

| Bloco | Função | Molde |
|---|---|---|
| **Confirmação + horário** | reforça o compromisso | "Tá confirmado. Você marcou um horário comigo: [data/hora]. Igual um Zoom: bota na agenda." |
| **O timer / countdown** | ancora a urgência da sessão | "A aula começa em: [contador]" |
| **O que fazer AGORA** | anti-fuga, opt-in | "1) Salva na agenda. 2) Entra no [WhatsApp/grupo] pra receber o link e o lembrete." |
| **Por que valer a pena ficar** | retenção plantada | "Quem fica até o fim leva [o presente real]." |
| **Mini-prova / bio** | mantém o calor | 1 depoimento curto ou 1 linha de autoridade |

Regras: reforça que ele **marcou um horário** (gatilho de compromisso) · opt-in de WhatsApp explícito · sem replay completo (anti-fuga) · botão de calendário. Variante ao vivo x perpétuo: no perpétuo o timer é da sessão escolhida, sem data fixa.

---

## 3. OS ÂNGULOS DE ANÚNCIO (com headlines)

Não um ad só: **5-8 ângulos**, cada um pescando um tipo de pessoa por uma porta diferente. Cada ângulo nasce de um **pilar do plano** e sai com a **headline pronta** + o público que pesca:

| # | Ângulo (pilar) | Porta de entrada | Headline (molde) |
|---|---|---|---|
| 1 | **Dor / mundo atual** | quem vive o problema agora | "[a cena ruim de hoje, na fala dele]. Tem um jeito de [virar]." |
| 2 | **Desejo / mundo ideal** | quem quer o resultado | "[a cena boa do depois, com número]." |
| 3 | **Inimigo** | quem tá cansado da cultura dominante | "Você não precisa de [o que o mercado vende]. Precisa de [a virada]." |
| 4 | **Mecanismo / curiosidade** | quem quer entender o "como" | "[a sacada contraintuitiva do mecanismo]." |
| 5 | **Prova / autoridade** | o cético que quer número | "[N] com [como]. Sem [o ônus]." |
| 6 | **A objeção invertida** | quem "já tentou e desistiu" | "Já tentou [X] e não deu? O problema não foi você, foi [o mapa]." |
| 7 | **Filtro / identidade** | o avatar exato | "Pra [quem é], que [faz X] e [sente Y]." |
| 8 | **Number-forward** (se houver número calculável) | o pragmático | "[número] que [resultado], sem [esforço]." |

Regras: cada headline ancora num **verbatim real** do plano (a dor/desejo na fala do avatar), passa nas 3 perguntas do gate (dá pra VER, dá pra FALSIFICAR, SÓ ele assina) e no anti-IA (zero em-dash, zero clichê). O banco completo e as variações finas são `soft-conteudo-headlines`; aqui o plano entrega **a semente de cada ângulo**, pronta pra testar.

> **Por que ângulos diferentes (não 1 ad melhor):** iscas diferentes pegam peixes diferentes, todos pro mesmo aquário. Um pega quem se move por dor, outro por desejo, outro por curiosidade do mecanismo. Testa-se vários; o que escala, escala.

---

## 4. Como isso sai no doc
Três blocos no fim do plano (depois da Seção 9 Insumos), cada um em tabela/lista densa:
- **Página de captura:** o molde preenchido com a copy do cliente (headline + sub + bullets + CTA + contra-filtro).
- **Página de obrigado:** o molde preenchido (confirmação + timer + o que fazer agora + retenção).
- **Ângulos de anúncio:** a tabela de 5-8 ângulos com a headline de cada, etiquetada pelo pilar e pelo público que pesca.

Insumo faltando (ex.: o presente da retenção, o objeto da prova) = `[A CONFIRMAR]`. O handoff: páginas vão pra `soft-webinar-paginas` (código), ângulos vão pra `soft-conteudo-headlines` (banco) e `soft-designer` (arte).
