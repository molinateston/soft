---
name: soft-radar-tendencias
description: Radar de pauta VIVA do método Soft, o pulso semanal do nicho. Levanta o que está quente AGORA (assuntos, formatos, ganchos em alta nos últimos dias) pesquisando na web com data verificada, filtra por saliência, e devolve uma tabela de temas onde a última coluna já é o ÂNGULO Soft pronto pra virar peça, enquadrado pela tese do dono, com handoff pra soft-conteudo-headlines/-matriz. É pauta perecível e datada, o oposto da fundação. Use quando o pedido for "o que tá em alta no meu nicho", "pesquisa de tendência", "sobre o que postar essa semana", "o que tá bombando", "tendências da semana", "radar de conteúdo", "pauta viva". NÃO use pra a fundação de mercado/dor/verbatim/concorrente que se faz uma vez e usa o ano (Super Pesquisa, em soft-posicionamento), nem pra a matriz/banco de pautas do mês (soft-conteudo-matriz), nem pra a HEADLINE de uma pauta (soft-conteudo-headlines), nem pro CORPO da peça (soft-conteudo-carrossel/-reels/-stories), arte (soft-designer) ou funil/venda (soft-funil/soft-vendas-closer).
---

# Radar de Tendências, o pulso semanal do nicho

Posicionamento e matriz de conteúdo resolvem o "sobre o que eu falo sempre". Não resolvem "tem alguma coisa quente ROLANDO essa semana que eu posso surfar antes de esfriar". Essa é a lacuna que esta skill fecha: ela vasculha a web AGORA, pega o que está em alta no nicho do dono (assuntos em discussão, formatos que estão pegando, ganchos que estão viralizando), confere a **data de cada item**, e devolve uma tabela onde cada linha é um tema quente e a última coluna já é o **ângulo Soft pronto pra virar peça**.

**O que esta skill faz por você:** captura pauta PERECÍVEL e datada. Ela responde "o que posso postar HOJE pra pegar a onda", não "quem é meu cliente" nem "qual meu banco de pautas do mês". Cada linha da tabela vira input limpo pra **soft-conteudo-headlines** (escrever a headline) ou pra **soft-conteudo-matriz** (encaixar no calendário).

**A fronteira (não invada):** a **Super Pesquisa** (dentro de `soft-posicionamento`) é a FUNDAÇÃO estrutural: mercado, força da dor, concorrente por lacuna, verbatim atemporal de dor/desejo. Faz-se uma vez e usa o ano inteiro. O RADAR é o **pulso**: últimos dias, datado, descartável na semana seguinte. Misturar os dois polui o Dossiê, que precisa ser estável. Se o dono quer a fundação, isso é soft-posicionamento; aqui é só o que está quente agora.

**As 6 leis (valem antes de tudo, detalhe em `shared-references/operacao-padrao.md` Seção 0):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil; (2) abre ensinando o que faz; (3) é consultiva, puxa nicho/avatar antes de sair pesquisando; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: link, data, número ou tendência que você não verificou NÃO entra, jamais item plausível; (6) **doc de output enxuto pros 2 leitores**: a tabela que sai serve o humano que planeja E a IA que recebe a linha como contexto da peça.

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare no STOP, e rode o gate por dentro antes de mostrar o radar.** A profundidade da navegação/busca (as fontes, as buscas datadas, o fallback quando o feed não abre) está em `references/protocolo-de-busca.md`; o corpo abaixo já é executável.

## Output Contract (o que você entrega)
- **Uma tabela-radar datada.** Primeira linha antes da tabela: `Radar de [NICHO], [DD/MM/AAAA] (janela: últimos [N] dias)`. Depois a tabela com estas colunas exatas:
  `| Tema quente | Onde está pegando | Fontes/comunidades | Links representativos | Sinais de calor | O que está sendo dito/debatido | Por que importa pro [NICHO] | Ângulo Soft pra postar |`
- **Mire em 10-20 temas.** Menos é aceitável se o material real for limitado; nesse caso você DIZ isso, não enche com item fraco. Melhor 8 temas quentes de verdade que 20 recheados de ruído.
- Cada tema **passou pelo corte de janela** (datado, dentro dos últimos N dias, default 7) e pelo **filtro de saliência** (2+ sinais de calor). Item sem data verificável NÃO entra.
- A coluna **Ângulo Soft** é a que vale ouro: NÃO é um gancho genérico de creator. É o tema quente já **enquadrado pela tese/mecanismo do dono**, ancorado na dor do avatar, apontando pro método. É copy embrionária, então roda no gate anti-IA + cliente-primeiro.
- Abaixo da tabela: **as 3 pautas mais fortes** apontadas (1 linha de porquê cada, a que mais casa com a tese do dono) + o handoff ("quer que eu escreva a headline de alguma? passo pra soft-conteudo-headlines").
- Você **nunca inventa** link, data, número ou tendência. Sem fonte real, o item cai; furo pontual vira `[A CONFIRMAR]`.

## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar o radar solto no chat)
O RESULTADO é **UM documento markdown consolidado** (a tabela-radar). No **claude.ai**, um **artifact de markdown** (o dono abre, copia, escolhe a pauta da semana); no **Claude Code**, um arquivo `.md` na working dir; no **agente/Telegram**, um ARQUIVO cujo path completo vai na resposta. A CONDUÇÃO (puxar nicho, o STOP de escolha) acontece no chat; o RADAR mora no DOC. Ao parar, você mostra/atualiza o DOC e pergunta "qual pauta puxo?"; NUNCA reescreve a tabela em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Os 3 ambientes (a mesma skill, entrega e alcance diferentes)
| Ambiente | Tem Bash/navegação? | O que esta skill faz | Entrega |
|---|---|---|---|
| **app / chat (claude.ai)** | Sem Bash; navegação depende do que a plataforma expõe | Se NÃO tem como pesquisar ao vivo, CONDUZ: pede ao dono colar o que ele já viu quente (prints, links, o que os concorrentes postaram), e ORGANIZA isso na tabela-radar com o ângulo Soft. Não finge varredura que não fez | Doc MD (artifact) com o radar montado do que o dono trouxe; avisa que a varredura ao vivo roda no Code/agente |
| **Claude Code** | Sim (WebSearch/WebFetch + Chrome MCP) | Varredura AO VIVO: buscas datadas + leitura das fontes + verificação de data item a item. Salva `radar-[nicho]-AAAA-MM-DD.md` + roda `scripts/lint_copy.py` na coluna de ângulos como cinto anti-IA. Confirma o path | Radar completo em `.md` na working dir, path na resposta |
| **agente / Telegram** | Sim (tem Bash; WebSearch quando disponível) | Igual ao Code, com as ferramentas do ambiente. Se o feed logado (X/Instagram) não abre, cai no fallback WebSearch datado + WebFetch e DIZ o que não deu pra varrer | Radar em `.md`, **path completo na resposta** + resumo curto SEM markdown pesado (as 3 pautas quentes em texto corrido) |

> Regra de honestidade de tooling (herdada e dura): se a navegação ao vivo não está disponível ou o feed não abre, você AVISA o que faltou e trabalha com o que dá (WebSearch datado, ou o que o dono colou). Nunca simula uma varredura que não aconteceu. Radar inventado é pior que radar pequeno.

## Passo 0, puxa nicho + avatar + janela (NÃO PULE, é a fronteira)
Antes de pesquisar qualquer coisa, você precisa de três coisas. Procura nesta ordem: **Plano de posicionamento colado na conversa** → **perfil/descrição do projeto** → **mensagens anteriores**. O que faltar, pergunta numa única mensagem curta.

1. **Nicho + avatar** (obrigatório pra filtrar o ruído). Não é "marketing", é "consultor de gestão financeira pra dono de clínica odontológica". Quanto mais específico, mais afiado o filtro de saliência. Do Plano você puxa junto a **tese/mecanismo do dono e o verbatim de dor** (é o que vai enquadrar a coluna de ângulo). Se não tem Plano, você ainda roda, mas avisa que o ângulo sai mais bruto sem a tese cravada.
2. **Janela** (default **7 dias**). O dono pode pedir 3 dias (pauta muito quente) ou 14 (nicho de giro lento). Fixe o N e respeite o corte duro.
3. **Fontes prioritárias do nicho** (opcional mas ajuda): perfis/portais/subreddits que o dono já acompanha. Se ele não sabe, você descobre na varredura.

**Regra de fronteira:** você NÃO faz pesquisa de fundação aqui (força da dor, mapa de concorrente, verbatim atemporal). Se o pedido é esse, é soft-posicionamento (Super Pesquisa). Aqui nicho/avatar entram como FILTRO de entrada, não como objeto de pesquisa.

## Passo 1, varre as fontes com data verificada
Vasculha a web como um pesquisador humano faria, na sequência abaixo. **A regra-mãe: confere a data de publicação de cada item e descarta sem exceção o que passa da janela.** Detalhe das fontes, das queries e do fallback em `references/protocolo-de-busca.md`; o essencial:

- **Buscas datadas (base, sempre roda):** para cada eixo, uma query filtrada pela janela. Os 5 eixos que capturam pauta quente: `[nicho] novidade/lançamento`, `[nicho] polêmica/debate`, `[nicho] dado/pesquisa`, `[nicho] mudança/regra nova`, `[nicho] o que está bombando/viralizou`. No Code/agente, WebSearch + WebFetch pra abrir e ler a data no corpo da página. Adapte as queries pro idioma e jargão real do nicho (PT-BR quando o público é BR).
- **Feed social (quando a navegação abre):** rola o feed relevante ao nicho (Reddit home/r/popular + subreddits do nicho; X/Para Você; perfis de concorrente no Instagram) e abre os posts em alta. Confere o carimbo de data em cada um. O feed LOGADO (X/Instagram) é o ponto frágil: se não abre, cai no fallback e diz.
- **Verificação de data (sem atalho):** abre a página, localiza a data visível, confirma que está dentro da janela. Data faltando, confusa ou fora da janela = item descartado. Nunca deduz data pelo "parece recente".

## Passo 2, filtra por saliência (o que é calor de verdade)
Junta o conjunto amplo de itens datados e agrupa os relacionados em **temas** (um tema pode combinar discussão social + cobertura de portal). Um tema só entra no radar se mostra **pelo menos 2** destes sinais de calor:

- **Volume/atenção forte** (muita gente falando, engajamento acima do normal do nicho).
- **Debate/discordância clara** (o nicho está dividido, tem os dois lados).
- **Informação nova ou virada** (dado inédito, lançamento, mudança de regra que altera como o avatar trabalha).
- **Implicação real pro avatar do dono** (mexe com a vida/o bolso/o trabalho de quem ele atende).

Tema com 1 sinal só é ruído, não entra. É o filtro que separa "assunto quente que rende peça" de "notícia qualquer".

## Passo 3, escreve a coluna Ângulo Soft (o coração da skill)
Aqui o radar deixa de ser clipping e vira munição. Pra cada tema que passou, a coluna **Ângulo Soft** enquadra o tema quente pela lente do dono. NÃO é um gancho genérico de creator ("aproveite essa tendência!"). É:

- **Ancorado na dor/desejo real do avatar** (verbatim do Plano quando existe). O ângulo nasce de como o cliente do dono vive esse assunto quente, não de como o mercado geral vê.
- **Enquadrado pela tese/mecanismo do dono.** O tema quente é a ISCA; o método do dono é a resposta. Ex.: sai uma polêmica sobre ferramenta X no nicho → o ângulo não é "opine sobre a ferramenta X", é "por que a ferramenta X não resolve o problema real (que é [o que o método do dono ataca])".
- **Aponta pro método e filtra o cliente certo.** Deixa a lacuna que fecha no que o dono vende. Ângulo que qualquer creator do nicho postaria = reprovado.
- **Vocabulário do cliente final** (nunca "lead/funil/ticket" no ângulo), tom de comando, número em algarismo.
- **Curto:** uma manchete-ângulo, não um parágrafo. Ela vira o INPUT da soft-conteudo-headlines.

## Passo 4, roda o GATE por dentro (auditoria interna, NÃO imprime)
Roda o gate em CADA linha antes de ela entrar no radar. A tabela abaixo é teu **checklist interno**, nunca a saída. Uma falha refaz a linha (ou derruba o tema), não o radar inteiro.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Datado e na janela** | tem data verificada, dentro dos N dias; data faltando/fora = ✗ (item cai) | |
| **Saliente (2+ sinais)** | tem ao menos 2 sinais de calor reais; 1 só = ruído, ✗ | |
| **Link real** | link representativo existe e foi aberto; link inventado/deduzido = ✗ | |
| **Ângulo ancorado** | nasce da dor real do avatar (verbatim) OU da tese do dono; genérico de creator = ✗ | |
| **Ângulo aponta pro método** | deixa lacuna que fecha no que o dono vende; NÃO é "surfe a tendência" solto | |
| **Filtra o cliente certo** | atrai quem compra do dono, não curioso do nicho; pauta viral genérica = ✗ | |
| **Clareza (Lei 1)** | dá pra entender sem já ser de dentro; zero palavra difícil, zero figura vazia | |
| **Sem invenção (Lei 5)** | zero link/data/número/tendência inventado; furo pontual = `[A CONFIRMAR]`, não item plausível | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, destrava, transforma"). No chat sem lint, faz CTRL+F manual de "—" e "travar" na coluna de ângulos | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ na data/link/invenção derruba o TEMA. Um ✗ no ângulo REFAZ o ângulo. Só tudo-✓ entra. | |

## Passo 5, monta o radar e PARA
Renderiza a tabela-radar no DOC (tabela markdown que renderiza, nunca dentro de bloco de código, que vira grade ilegível). Abaixo dela: **as 3 pautas mais quentes** com 1 linha de porquê cada (a que mais casa com a tese, a mais debatida, a com implicação mais direta pro avatar) + a nota de "isso foi o que verifiquei dentro da janela; [X] itens caíram por falta de data". Se a varredura ao vivo falhou em parte, DIZ o que não deu pra varrer.

Mostra o radar **no DOC** e PARA. Pergunta: "qual dessas pautas você quer transformar em peça? Passo pra **soft-conteudo-headlines** pra escrever a headline, ou encaixo no calendário na **soft-conteudo-matriz**." **Espera a escolha** antes de escrever qualquer peça. O radar entrega a munição; quem dispara é a skill de peça.

## Exemplo denso (inline): nicho = nutricionista esportivo pra corredor amador. LABEL, não copiar.
> Nicho/avatar (do Plano): nutri esportivo, avatar = corredor amador 35-50 que treina pra prova de rua e "come certo mas não rende". Tese do dono: o problema não é dieta restritiva, é **timing de carboidrato em torno do treino** (o mecanismo dele). Janela: 7 dias. Ambiente: Claude Code.

1. **Passo 0:** puxo nicho, avatar e tese do Plano colado. Janela 7 dias. Fontes que o dono segue: 2 perfis de treino + r/running.
2. **Passo 1:** rodo as buscas datadas (`corrida de rua novidade`, `suplemento corredor polêmica`, `nutrição esportiva pesquisa`, etc.) via WebSearch, abro os resultados com WebFetch, leio a data no corpo. Rolo r/running e os 2 perfis. Descarto 6 itens sem data clara.
3. **Passo 2 (saliência):** um tema quente sobrevive: "estudo novo dessa semana questionando o gel de carboidrato durante a prova". Sinais: debate claro (corredores divididos) + informação nova (o estudo) + implicação real pro avatar (ele usa gel e não sabe se serve). 3 sinais, passa. Um segundo tema ("tênis de placa de carbono na moda") tem só volume, 1 sinal: cai.
4. **Passo 3 (ângulo Soft):** o ângulo NÃO é "opine sobre o estudo do gel". Enquadro pela tese: **"O corredor que toma 3 géis na prova e continua quebrando no km 30, porque o problema nunca foi o gel na corrida, foi o carboidrato que faltou nas 48h antes."** Ancorado no verbatim "como certo mas não rendo", aponta pro mecanismo (timing de carbo), filtra o corredor que treina sério (o cliente), não o curioso.
5. **Passo 4 (gate):** datado ✓, 3 sinais ✓, link do estudo aberto ✓, ângulo ancorado na tese ✓, aponta pro método ✓, filtra ✓, clareza ✓, sem invenção ✓, anti-IA (rodei `lint_copy.py` na coluna, zero em-dash, zero "travar") ✓. VEREDITO ✓, entra.
6. **Passo 5:** salvo `radar-nutri-corrida-2026-07-04.md` com a tabela, aponto essa como a pauta #1, respondo com o path completo e pergunto "escrevo a headline dela? (soft-conteudo-headlines)".

Contra-exemplo (REPROVA): tema "tênis de placa de carbono está na moda" com ângulo "aproveite a hype dos tênis de carbono pra falar de performance". Um sinal só (volume), ângulo genérico que qualquer creator posta, não aponta pro mecanismo do dono, não filtra o cliente. VEREDITO = ✗, tema cai.

## When NOT to use (manda pra skill certa)
- Pediu a **fundação** (mercado, força da dor, verbatim atemporal, mapa de concorrente por lacuna) que se faz uma vez e usa o ano → **soft-posicionamento** (Super Pesquisa). O radar é pulso perecível, não fundação estável.
- Pediu a **ideação em lote/matriz do mês** a partir dos pilares (banco de pautas, calendário editorial) → **soft-conteudo-matriz**. O radar alimenta a matriz com pauta quente, mas não é a matriz.
- Pediu a **HEADLINE** de uma pauta já escolhida → **soft-conteudo-headlines** (é o passo seguinte; cada linha do radar é o input dela).
- Pediu o **CORPO** da peça → **soft-conteudo-carrossel** / **-reels** / **-stories**.
- Pediu **arte/visual/PNG** → **soft-designer**.
- Pediu **carta/página/venda** → **soft-funil** / **soft-vendas-closer**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Incluiu item sem data ou fora da janela | Corte duro: data verificada dentro dos N dias, senão o item cai. Nunca deduz "parece recente" |
| Inventou um link, uma data ou uma tendência | Lei 5: só o que você abriu e verificou entra; furo vira `[A CONFIRMAR]`, nunca item plausível |
| Tema com 1 sinal de calor entrou no radar | Filtro de saliência: mínimo 2 sinais; 1 só é ruído, não pauta |
| Ângulo genérico ("aproveite essa tendência!") | Enquadra pela tese/mecanismo do dono e ancora na dor do avatar; tema quente é isca, método é resposta |
| Ângulo que qualquer creator do nicho postaria | Falha em "aponta pro método" e "filtra": reancora na lacuna do método do dono |
| Simulou a varredura quando o feed não abriu | Honestidade de tooling: avisa o que não deu pra varrer, trabalha com WebSearch datado ou o que o dono colou |
| Virou pesquisa de fundação (dor, concorrente, verbatim atemporal) | Fora do escopo: isso é a Super Pesquisa (soft-posicionamento); aqui é pauta da semana |
| Encheu 20 linhas com item fraco pra bater meta | Melhor 8 temas quentes de verdade; diz que o material foi limitado, não recheia com ruído |
| Despejou a tabela solta no chat | O radar sai como doc MD (artifact / arquivo / path no agente); o chat é a condução |
| Jogou a tabela dentro de bloco de código | Tabela markdown que renderiza; bloco de código vira grade ilegível |
| Escreveu a headline/peça sem parar | O radar entrega munição e PARA; quem escreve é soft-conteudo-headlines/-carrossel após a escolha |

## References (só pra profundidade, o corpo acima é autossuficiente)
- `references/protocolo-de-busca.md`: as fontes por tipo, as buscas datadas por eixo, a rolagem de feed, a verificação de data sem atalho, o fallback quando o feed logado não abre, e a régua de saliência detalhada. **Fonte da verdade da varredura.** Consulta no Passo 1.
- `shared-references/operacao-padrao.md`: as 6 leis (Seção 0) + regras de tom/economia/entrega. Consulta na 1ª invocação da sessão.
- `shared-references/filtro-anti-ia/`: o banco de padrões banidos + falsos-positivos que alimenta o check Anti-IA do gate (roda na coluna de ângulos).
- `shared-references/filtro-cliente-primeiro.md`: a régua de "isto atrai o cliente certo ou o curioso do nicho?", aplicada na coluna de ângulos.
- `scripts/lint_copy.py`: no Claude Code/agente, roda `python3 scripts/lint_copy.py radar.md` (ou na coluna de ângulos) como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual do gate.
