---
name: soft-conteudo-multiplataforma
description: Adapta uma peça Soft que já existe pra OUTRA plataforma (LinkedIn, X/Threads, Substack, YouTube, newsletter, email, PDF/Notion, E o COMENTÁRIO FIXADO embaixo do post) sem diluir a tese. Engenharia reversa, extrai os 5 papéis e o núcleo da âncora e re-renderiza no idioma nativo do destino. Newsletter/email sem âncora tem modo arquétipo. O comentário fixado humaniza (1º comentário do criador, confissão que casa com a tese + imagem cômica de status baixo; arte pela soft-designer). Use pra "repurpose", "adaptar pra LinkedIn/X/YouTube/newsletter/email", "multiplataforma", "republicar a peça", "transformar esse carrossel em outro formato", "comentário fixado/fixo", "primeiro comentário", "legenda cômica do post", "humanizar esse post". NÃO use pra HEADLINE/capa do zero (soft-conteudo-headlines), arte/PNG (soft-designer; aqui sai só o briefing), posicionamento (soft-plano-posicionamento), nem carta/venda (soft-funil). Pro CORPO de carrossel/reel/stories, use as irmãs soft-conteudo-carrossel/-reels/-stories.
---

# Multiplataforma, a mesma peça em idioma nativo

Adaptar não é traduzir tom. É engenharia reversa. Você pega uma peça Soft que já funcionou, extrai os 5 papéis e o núcleo dela, e re-renderiza no formato do destino preservando a função de cada parte. Se a versão adaptada parece igual a qualquer post daquela plataforma, falhou: perdeu o filtro. O que viaja entre plataformas é a TESE e os 5 papéis; o que muda é só o tempo de exposição e a unidade de entrega.

**O que esta skill faz por você:** pega uma peça que já funcionou e a leva pra outra plataforma (LinkedIn, X, YouTube, email, newsletter) sem perder a tese, falando o idioma nativo de cada uma. É como você multiplica uma ideia boa sem reescrever do zero.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa de você a preferência (duração, formato, tom) antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: confere se tem a peça-âncora/o número/o case antes de adaptar e, se faltar, marca `[DADO: confirmar]` no lugar do furo e diz o que falta, jamais preenche com algo plausível; (6) **doc de output enxuto pros 2 leitores**: o que sai é otimizado pro humano que lê E pra IA que recebe como contexto: só a versão adaptada limpa + `[DADO: confirmar]`, zero meta-narração. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar a versão adaptada.**

## Output Contract (o que você entrega)
- **Uma versão adaptada por vez**, da peça-âncora pro destino pedido, com o **mapa dos 5 papéis no original** (o que vira o quê) impresso antes da peça.
- A versão sai no **formato e idioma nativos do destino** (subject+pre-header no email, thread numerada no X, primeira-linha-antes-do-ver-mais no LinkedIn, título+capítulos no YouTube).
- O gate roda **por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída. Versão que falha no gate não sai.
- Você **para e espera** o OK antes de adaptar pra um segundo destino ou gerar variação.
- Você **nunca inventa fala nem número do cliente** e **nunca dilui a tese pra caber no formato**.
- **Regra dura de saída (em-dash):** a copy final **nunca** contém o caractere `—` (travessão). Se contém, a skill **NÃO terminou**: volta pro Passo 5b, reescreve a linha e varre de novo. Esta regra vale acima de qualquer "ficou bonito com o travessão".


## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a peça no chat)
Regra dura, vale mesmo pra copy curta: o RESULTADO desta skill sai como **UM documento markdown consolidado**. No **claude.ai**, um **artifact de markdown** (o dono abre, copia, baixa); no **Claude Code**, um arquivo `.md`. No **agente/Telegram**: gera o doc como arquivo `.md` no disco e cita o path completo na resposta (o bridge anexa o arquivo); a condução vai em mensagens curtas, sem markdown pesado (sem `##`, sem tabela com `|` no texto ao usuário) — o doc vai como anexo. A CONDUÇÃO (perguntas de contexto, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA/COPY em si mora no DOC. Ao parar num STOP, você mostra ou atualiza o DOC e pergunta "ajusto?"; você NUNCA reescreve a peça em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Passo 0, ancora antes de adaptar (NÃO PULE)
O fluxo assume que a peça-âncora já passou pelo gate dela. Confirma duas coisas antes de mexer:
- **A headline/abertura já está escolhida?** Se a âncora ainda não tem headline aprovada, manda fazer na **soft-conteudo-headlines** primeiro e para. Você adapta a partir de uma peça pronta, não cria do zero.
- **Onde está o verbatim real?** Procura a fonte de fala do cliente nesta ordem: descrição do projeto → Plano colado → mensagens anteriores. A peça adaptada herda a mesma âncora; nenhuma fala ou número novo aparece sem fonte.

Três estados de entrada (declara qual é o seu antes de adaptar):
- **Peça-âncora colada + verbatim com N:** caminho ideal. Adapta preservando a fala literal e o N real.
- **Peça-âncora colada, mas sem a fala literal por trás:** mantém o que a âncora já tinha; qualquer número que você não confirmou entra como `[DADO: confirmar]` e **NÃO conta como Ancorada=✓**.
- **Nada colado:** pergunta numa única mensagem ("qual peça você quer adaptar, e pra qual plataforma?") e para. Sem peça-âncora não há o que adaptar.

**Exceção só pra newsletter/email (modo arquétipo):** se o destino é newsletter/email e o especialista NÃO tem peça-âncora pra adaptar NEM edições passadas pra destilar a voz dele, você não fica parado: entra no **modo arquétipo** (Passo 4a). A regra-mãe continua valendo: **com exemplos, você destila a voz do dono; sem exemplos, arquétipo + coleta**. Arquétipo é molde emprestado pra sair do cold-start, marcado como provisório, nunca a voz definitiva. Fora de newsletter/email, sem âncora não há adaptação: para e pergunta.

## Passo 1, identifica a peça-âncora e o destino
- **Âncora:** o que foi colado? Carrossel, reel, story, carta, post pronto. Anota o tipo.
- **Destino:** se não disseram, pergunta UMA vez: "Pra qual plataforma? LinkedIn, X/Threads, Substack/email, YouTube, newsletter, PDF/Notion?" e para.
- **Preferência do especialista (Lei 3, consultiva):** puxa como ELE quer a peça no destino antes de gerar. Ex.: YouTube, que duração e formato (corte curto, aula longa)? Email, mais pessoal ou mais direto? Não sai gerando sem extrair a ideia que está na cabeça dele.
- Regra de fundo: o formato não muda a arquitetura. Muda o **tempo de exposição** (3s de capa vira primeira linha do LinkedIn) e a **unidade de entrega** (slide vira parágrafo, vira tweet, vira minuto de vídeo).

## Passo 2, extrai o núcleo Soft da âncora (interno, antes de re-renderizar)
Antes de traduzir, escreve internamente os **6 componentes do núcleo** que viajam inalterados (detalhe + checklist pós-extração em `references/nucleo-soft-extracao.md`):
- **Problema Sofisticado (3ª Camada):** a dor real nomeada como inimigo-categoria, nunca defeito do cliente.
- **Método com nome próprio:** sempre nomeado, mesmo em 280 caracteres.
- **Vilão-categoria:** a prática/sistema/crença atacada, nunca pessoa ou marca.
- **CTA filtrante:** pra onde o lead vai (Direct com palavra, comentário, reply do email); nunca "curte e compartilha".
- **≥3 dos 5 movimentos Blair Warren:** incentiva sonho · justifica falha · aplaca medo · confirma desconfiança · atira pedra no inimigo. Princípio de fundo, nunca lista citada na peça.
- **Campo semântico do cliente:** vocabulário do nicho, nunca "lead/funil/conversão"; monta a tabela de tradução antes de adaptar.

A **prova específica** real da âncora (número/cena) viaja junto. Se algum dos 6 sumiu na âncora, pergunta antes de adaptar. Adaptar com núcleo incompleto produz peça fraca.

## Passo 3, mapeia os 5 papéis da Estrutura-Mãe no original
Identifica qual trecho da âncora faz cada papel. Isso é o mapa que você imprime no Passo 5.

1. **Capa** (o que parou o leitor)
2. **Capa Reserva** (o que aprofundou o loop)
3. **Contexto** (como o leitor foi aterrado)
4. **Conteúdo** (a virada + o método via contraste)
5. **CTA** (a ação filtrante)

Anti-padrão: traduzir cada slide em 1 parágrafo/tweet sem repensar os papéis. O carrossel tem N slides, mas os 5 papéis não são N unidades: alguns papéis ocupam vários slides (Conteúdo), outros colapsam (Capa + Capa Reserva num formato curto). Adaptação fiel preserva os **papéis**, não o número de unidades.

## Passo 4, re-renderiza no idioma nativo do destino
Usa a tabela como ponto de partida. Cada papel migra preservando a função, no formato do destino.

| Destino | Capa | Capa Reserva | Contexto | Conteúdo | CTA |
|---|---|---|---|---|---|
| **LinkedIn** | 1ª linha (antes do "ver mais") | parágrafo 2 | parágrafo 3 | corpo 3-5 parágrafos | última linha + P.S. |
| **X / Threads** | 1º tweet | 2º tweet | 3º tweet | tweets 4-8 | último tweet |
| **Substack / newsletter / email** | subject (≤50 char) + pre-header | 1ª linha | parágrafo 1 | parágrafos 2-4 | P.S. ou botão |
| **YouTube longo** | título + thumb | primeiros 15s | 1º minuto | corpo 3-8min | chamada de inscrição |
| **PDF / Notion** | capa do doc + título | intro de 1 parágrafo | cena/dado concreto | seções principais | CTA de fechamento |
| **TikTok / Shorts** | 0-3s | 3-6s | 6-12s | 12-40s | 40-50s |
| **Mini Webinar** | abertura 0-30s | 30s-1min | 1-2min | corpo 2-8min | fechamento com convite |
| **Comentário fixado** | a imagem cômica (a piada visual) | linha 1 legenda o fato | linha 2 (status baixo do dono) | linhas 3-4 (vitória triste + resignação) | não vende: humaniza, sem CTA de venda |

**Regras nativas por destino (o resumo; a reference tem o resto).** Cada linha: o limite que aperta a peça, a regra crítica que a maioria erra, e o formato do CTA.

| Destino | Limite duro | Regra crítica (a que erra) | Formato do CTA |
|---|---|---|---|
| **LinkedIn** | 150 char antes do "ver mais"; post 900-1200 char | zero link externo no corpo (perde 60% de reach); comentário pesa 15x mais que like | "comenta [PALAVRA] que te mando a Carta" ou DM do LinkedIn |
| **X / Threads** | 280 char por post; frase 100-240 char | frase isolada é a unidade de valor: escreve pra gerar quote-retweet, não só like | "responde aqui embaixo" ou "link no perfil" |
| **Substack / newsletter** | subject <50 char, pre-header <80 char; corpo 400-700 palavras | 1ª linha é o 2º gancho, nunca "oi tudo bem"; PS no fim é obrigatório | link pra Carta ou "assina" (Substack); nunca "curte" |
| **Email** | subject <50 char, pre-header <80 char; corpo 400-700 palavras | permite link (ao contrário do LinkedIn); PS obrigatório com urgência ou objeção | link pra Carta ou responder o email |
| **YouTube longo** | roteiro 8-12min; descrição 1000+ char; tags <500 char; capítulos 10+ | a cauda de publicação é 60% do trabalho: título+thumb são gatekeepers do CTR | Carta/WhatsApp + inscrição no canal, no fim e no 1º comentário fixado |
| **PDF / Notion** | 5-7 páginas (PDF); subpágina por capítulo (Notion) | entrega valor real mas mantém desejo: filtra a gente errada no meio, nunca resolve tudo | Mini Carta / reunião / Direct no fechamento; nunca "me segue" |
| **TikTok / Shorts** | 15-35s ideal; 9:16 vertical; legenda 1 linha | retention 70%+ no 1º 3s (gancho visual+texto+verbal) senão o algoritmo suprime; loop natural | "comenta [PALAVRA] que eu respondo" ou "link na bio" |
| **Comentário fixado** | 4 linhas exatas, ≤40 char cada, 📌 na linha 1 | a IMAGEM carrega a piada, o texto só legenda; o dono é o status mais baixo em TODA linha; morno lido sozinho = ótimo | nenhum: humaniza, não vende (CTA de venda no comentário = ✗) |

**Abre a reference da plataforma e segue as regras nativas dela** (formato, limites, exemplos, SEO/UTM). Não adapta de cabeça: a reference tem as regras que mudam a peça:
- LinkedIn → `references/plataforma-linkedin.md` · X/Threads → `references/plataforma-x-threads.md` · Substack/Email → `references/plataforma-substack-email.md` (**sem âncora nem histórico? vai pro Passo 4a + `references/newsletter-arquetipos.md`**)
- TikTok/Shorts → `references/plataforma-tiktok-shorts.md` · YouTube longo → `references/plataforma-youtube-longo.md` (traz o **pacote completo de publicação**: título, descrição, tags, capítulos, thumbnail, SEO, UTM)
- PDF/Notion → `references/plataforma-pdf-notion.md` · Mini Webinar → `references/plataforma-mini-webinar.md` (distribuição/hospedagem; a construção do roteiro é da `soft-funil-miniwebinar`)
- **Comentário fixado** (o 1º comentário do criador embaixo do post, como peça de humanização) → **vai pro Passo 4c**, que tem a mecânica inteira. É uma superfície da peça, não uma plataforma de re-render normal: em vez dos 5 papéis, ela roda a mecânica confissão + imagem cômica + 4 linhas.

**Ao re-renderizar, NÃO use travessão `—` como pausa dramática** (é o tique nº1 de IA e o furo mais comum aqui): prefira ponto curto, vírgula ou dois-pontos. Prevenir na escrita é mais barato que caçar no gate; escreve já sem `—`.

**Idioma nativo, não copia-cola do Instagram.** LinkedIn e email são armadilha pra jargão de marketing: zero "lead/funil/ticket/conversão", sempre o campo semântico do cliente final. No formato curto (tweet único, email brevíssimo), papéis podem colapsar de propósito (Manifesto = Capa+CTA · Sentença = só Capa · Único = 1 unidade faz tudo). Colapso consciente não é traição da estrutura; perder um papel sem querer, sim.

**Mini-exemplo de re-render** (exemplo ilustrativo, nicho fictício; modela a qualidade, nunca copia). O MESMO slide de capa de um carrossel migra pro limite de cada destino sem perder a tese:
- **Slide de carrossel (âncora):** "Você não tem problema de agenda. Tem problema de agenda cheia de cliente errado."
- **1ª linha de post LinkedIn** (cabe nos 150 char, polariza antes do "ver mais"): "Agenda cheia não é o objetivo. Agenda cheia de cliente errado é o que te mantém preso."
- **Subject de e-mail** (<50 char, derivado do mesmo gancho): "Sua agenda cheia é o problema". Pre-header: "Cheia do cliente errado, não do certo."

A tese ("cliente errado, não falta de cliente") viaja inteira; muda só o tempo de exposição e a unidade.

**Se o destino for YouTube longo**, entrega também o pacote de publicação: título, descrição, capítulos, tags, sugestão de thumbnail.

## Passo 4a, modo arquétipo (SÓ newsletter/email sem âncora nem histórico)
Só cai aqui se o Passo 0 marcou o estado de exceção: destino newsletter/email e o dono não tem peça-âncora pra adaptar nem edições passadas pra destilar a voz. Não inventa a voz dele; empresta uma estrutura e ancora na voz que o Plano já tem.

1. **Confirma que é cold-start real.** Se ele tem 2+ edições passadas, NÃO é modo arquétipo: pede pra colar, você destila a voz real (padrão de abertura, fluxo de seção, formatação, fechamento, sinais de ausência que se repetem) e adapta a partir dela. Modo arquétipo é só quando não há nada.
2. **Escolhe o molde COM ele, numa mensagem só** e para: *"Você não tem edição pronta pra eu adaptar. Vou montar a partir de um molde ajustado à sua voz, marcado como provisório. Qual encaixa: (0) conversão direta que vende no fim · (1) aula com método · (2) ensaio que crava posição · (3) dissecação de um caso · (4) digest com curadoria · (5) ensaio pessoal · (6) entrevista/perfil?"* O **(0) conversão Soft é o default**: se ele não escolhe, é esse (é o que vende).
3. **Puxa a voz que já existe** antes de escrever: mecanismo com nome próprio, Problema Sofisticado, campo semântico do cliente final e os "sem", do Plano/perfil. Se não há nem Plano, coleta o mínimo (nicho, mecanismo, uma prova real) e só então monta. Sem mecanismo nomeado, manda pra **soft-plano-posicionamento** primeiro.
4. **Monta pelo molde escolhido** (menu abaixo), ajustando cada campo à voz dele. As 3 trocas Soft valem em TODOS: (a) ancoragem = verbatim/prova real, nunca "todo dado com número"; número plausível de enfeite = `[DADO: confirmar]`; (b) CTA filtrante no fechamento (link pra Carta / responder com uma palavra / Direct), nunca "curte, assina e compartilha"; (c) mecanismo nomeado onde o molde diz "método".
5. **Marca como provisório** no topo do doc: *"Base: arquétipo [nome] ajustado à voz do Plano. Molde emprestado, não a voz definitiva. Revisitar depois de ~5 edições reais publicadas."*
6. **Roda o gate normal** (Passo 5) na versão montada. Molde não isenta do gate.

**Menu dos 7 moldes (faixas de palavra por seção = ritmo, não trilho; o assunto decide onde pesar):**

| Molde | Abertura | Espinha de seções | Ancoragem | Tamanho |
|---|---|---|---|---|
| **0. Conversão Soft (DEFAULT)** | subject <50 + 2º gancho na 1ª linha | Gancho → Problema (3-4 blocos) → Diagnóstico (nomeia o Problema Sofisticado) → Método (mecanismo + etapas) → Fechamento → CTA → **PS obrigatório** | verbatim na abertura/diagnóstico, prova no método | 400-700 |
| **1. Aula com método** | resultado real + autoridade 1 linha + promessa | Gancho → Problema (inimigo-categoria) → Mecanismo (nome próprio) → Passo a passo (exemplo por passo) → Exemplos reais → bônus opcional → Fecho+CTA | verbatim/cena/prova por afirmação; casos nomeados | 800-1.500 (até 2.500 guia) |
| **2. Ensaio que crava posição** | consenso → contraposição → o que está em jogo | Consenso → por que ele prende o leitor → contraposição (mecanismo) → prova → objeção+resposta → o que fazer → fecho sem meio-termo+CTA | prova pro seu lado com honestidade do contra; vilão = categoria, nunca pessoa | 700-1.200 |
| **3. Dissecação de um caso** | caso + resultado + a lição que vem | Gancho → Contexto → Dissecação → o que funcionou (numerado) → o que falhou (numerado) → 3-5 lições → fecho+CTA | métrica/linha-do-tempo real; especulação sinalizada; furo = `[DADO: confirmar]` | 800-1.500 |
| **4. Digest com curadoria** | tema do período + item mais forte | Tema → 5-7 itens (link+comentário PRÓPRIO, não resumo) → notas rápidas → fecho+CTA | atribuição real por link; comentário pela lente do mecanismo; zero link inventado | 600-1.200 |
| **5. Ensaio pessoal** | cai na cena, sem preâmbulo | Cena → tensão → exploração → virada (percepção) → fecho + CTA LEVE | detalhe específico (dá pra ver); zero número/personagem inventado | 600-1.500 |
| **6. Entrevista / perfil** | fala direta + por que importa | Quem é → origem → trabalho → visões → 3-5 lições → o que vem + CTA | fala direta, não paráfrase; marco/projeto/data reais | 800-1.500 |

**Detalhe de cada molde (o que ele nunca faz, o modelo de abertura preenchível, a nota de CTA) está em `references/newsletter-arquetipos.md`.** Abre a reference quando montar; o menu acima é o mapa, a reference é o passo a passo.

## Passo 4c, COMENTÁRIO FIXADO (a superfície de humanização embaixo do post)
Só cai aqui quando o destino é o **comentário fixado**, o 1º comentário que o próprio criador solta embaixo de um post. Ele é a superfície onde a peça vira gente: embaixo de um post técnico ou de autoridade seca, o criador tira a máscara polida e se rebaixa com graça pra o público baixar a guarda. Aqui a re-render não roda os 5 papéis; roda a mecânica própria abaixo. **Uso situacional, não é peça obrigatória do funil: humaniza, NÃO vende, zero CTA de venda.** É ouro embaixo de post de autoridade fria; se o pedido é vender, é outra skill (soft-funil / soft-vendas-closer).

**A sacada central (leia primeiro): a IMAGEM carrega a piada, o comentário só legenda a imagem.** Se o comentário é engraçado sozinho, ele está trabalhando demais e a imagem está fraca. Por isso o conceito da imagem vem PRIMEIRO, sempre. A arte final NÃO sai daqui: você entrega o briefing e o dono aciona a **soft-designer** com a ID visual dele (nunca escreve prompt de Gemini/Nano Banana nem de ferramenta externa).

**Insumos antes de escrever (não pula; herda do Passo 0):** (a) **o post** (o que ele diz/entrega) e (b) **a tese/inimigo do Plano** (o Grande Dominó, o Mecanismo do Problema, na soft-plano-posicionamento). É a tese que faz o humor reforçar o posicionamento em vez de virar piada solta. Não viu o post ou não tem o Plano? Pergunta numa linha ou marca `[DADO: confirmar]`; nunca chuta uma piada plausível.

**O Output Contract muda pra 4 blocos** (esta superfície tem contrato próprio; o doc MD continua sendo UM só):
1. **A confissão** (1 frase): a verdade meio constrangedora que o post esconde em silêncio, casada com a tese/inimigo do Plano. Ex. de forma (não copiar): "Eu cobro caro e ainda tenho medo de mandar o orçamento." / "Passei anos aprendendo o que ensino em 20 minutos." Se você não nomeia a confissão em 1 frase, o post não está pronto pro comentário fixado: avisa o dono, não força piada em cima de post que não confessa nada.
2. **O conceito da imagem** (briefing pra soft-designer, parágrafo): a piada visual clara + a postura de status baixo do dono. Formato: *"Imagem fotorrealista de [cena]. A piada visual: [quem tem o status alto e como]. O dono aparece [postura/expressão de status baixo, levada a sério]. [Luz e enquadramento]."*
3. **O comentário de 4 linhas** (começa com 📌): legenda a imagem como se noticiasse o fato.
4. **A nota de gate** (1 linha): confirma que passou nos checks + anti-IA.

**As 3 regras da imagem:** (1) **uma piada visual clara** (o olho cai nela em <1s; se precisa de mais de 5 palavras pra descrever, está cheia, simplifica; uma piada é mais afiada que três); (2) **levada totalmente a sério** (sem piscadinha, sem joinha, sem cara exagerada; o humor vem de tratar o absurdo como normal); (3) **o dono é a figura de status mais BAIXO, sempre** (quem "ganha" na cena é o oposto dele: o cliente, a planilha, a concorrência complicada, o estagiário; o dono perde com dignidade silenciosa).

**As regras das 4 linhas (inegociáveis):** exatamente 4 linhas, cada uma frase completa; cada linha ≤40 caracteres (**conte, não estime**); linha 1 começa com 📌 e legenda o fato que a imagem mostra (não monta piada separada); linha 2 vira o status do dono pra baixo; linha 3 é uma vitória triste (o menor ganho possível); linha 4 é aceitação resignada, não piada esperta (**resignado vence esperto**). Sem P.S., sem ponto-e-vírgula, sem hashtag. PT-BR com acentuação correta. Evita muleta (só, que, muito, realmente, na verdade, literalmente).

**Gate próprio desta superfície (roda por dentro, um ✗ refaz):** Confissão nomeada em 1 frase · Confissão casa com a tese (mesma briga do Grande Dominó/inimigo, não piada solta de creator) · Piada visual descritível em ≤5 palavras · Linha 1 legenda o fato · Dono é status baixo em TODA linha (se ele ganha/parece esperto em alguma, reescreve) · Linha 4 resignada · 4 linhas exatas, ≤40 char cada, 📌 na linha 1 · **Teste do tédio sozinho** (leia as 4 linhas SEM a imagem: morno sozinho = ótimo, a imagem faz o trabalho; engraçado sozinho = a imagem está fraca, reforça a imagem) · Clareza (zero palavra difícil, zero figura vazia) · Anti-IA HARD (Passo 5b). Este gate SUBSTITUI a tabela dos 5 papéis do Passo 5 (aqui não há 5 papéis); o Passo 5b (varredura anti-IA) e o Passo 6 (mostra e PARA) valem igual.

**Exemplo denso (LABEL, não copiar). Nicho: consultor que vende gestão SIMPLES pra dono de PME.** Post: carrossel provando que o dono não precisa de ERP caro, só de uma planilha de 1 aba. Tese do Plano: simplicidade radical vence a complexidade cara (inimigo = o sistema complicado que vendem pro pequeno).
- **A confissão:** "Construí um negócio inteiro numa planilha de 1 aba e ainda tenho vergonha de mostrar."
- **O conceito da imagem (briefing):** "Imagem fotorrealista de uma sala de reunião de empresa grande. Na cadeira da cabeceira, imponente, um monitor gigante rodando um ERP cheio de gráficos, tratado como o executivo-chefe. O dono está numa banquetinha no canto, de camiseta, com um notebook velho e uma única planilha aberta, olhando pro monitor com respeito tímido. Luz corporativa fria, tudo levado a sério."
- **O comentário de 4 linhas:**
```
📌 O ERP tem a cadeira da chefia.
Eu fico na banqueta do canto.
Minha planilha de 1 aba paga as contas.
Alguém tinha que segurar o rojão.
```
- **Por que passa:** a confissão casa com a tese (humildade simples vence o sistema caro); a piada visual em 5 palavras ("ERP na chefia, dono na banqueta"); a linha 1 legenda o fato; o dono perde em toda linha e só "ganha" a vitória mais triste (a planilha paga as contas); a linha 4 é resignada; lido sozinho é morno, com a imagem canta. Anti-IA limpo. Cada linha ≤40. **PASSA.**
- **Contra-exemplo (REPROVA):** "📌 Fiz um negócio de 7 dígitos numa planilha." O dono GANHA (parece esperto), não é status baixo, não casa com a humildade da tese, e é impactante sozinho (a imagem vira redundante). ✗.

## Passo 5, roda o GATE por dentro (auditoria silenciosa, NÃO imprime)
Roda o gate na versão adaptada **internamente** (auditoria silenciosa). Só versão com VEREDITO=PASSA vai pro cliente. Um ✗ refaz. A tabela abaixo é o teu **checklist interno**, nunca a saída: o usuário recebe só a versão limpa (Passo 6), jamais a tabela. A âncora já passou no gate dela; a adaptação passa de novo no idioma novo.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorada** | herda fala literal/N **real** da âncora OU prova real do autor; **N inventado/plausível = ✗ automático**; fecha em chão/número/cena, não em tese solta bonita | |
| **Tese preservada** | a percepção central da âncora chegou inteira; **não foi diluída pra caber no formato** (encurtar ≠ esvaziar) | |
| **Nativo do destino** | formato e vocabulário são da plataforma alvo (subject/thread/1ª-linha/capítulos certos), **não um copia-cola do post do Instagram** | |
| **5 papéis re-renderizados** | os 5 papéis aparecem (ou colapsam de propósito, declarado); **nenhum papel sumiu por acidente** | |
| **CTA com destino** | filtrante e direcional no idioma do destino (Direct/comentário/reply/botão), **nunca "curte e compartilha"** | |
| **Confuso? (C)** | leigo do nicho entende na 1ª passada, sem reler | |
| **Inacreditável? (U)** | promessa/número soa crível, não exagero de guru | |
| **Chato? (B)** | tem cena/tensão/opinião; não é parágrafo morno informativo | |
| **Dá pra ver?** | fecha o olho e enxerga a cena. ✗ "tenha mais clareza" · ✓ "a recepcionista diz: semana que vem enche" | |
| **Dá pra falsificar?** | é fato falsificável, não adjetivo | |
| **Só você diz?** | o concorrente direto não assina igual (cena/mecanismo proprietário, não promessa banal do nicho) | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, destrava, transforma"). **Este ✓ só fecha DEPOIS do Passo 5b abaixo, que é a varredura de verdade; aqui não confia no olho.** | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

## Passo 5b, varredura anti-IA (BLOQUEANTE, antes do Passo 6)
Marcar Anti-IA=✓ na tabela do gate não basta: aqui você VARRE de verdade, na **versão exata que vai sair**. É o passo que barra o furo mais comum (travessão que passou batido). Ordem:
1. **CTRL+F por `—` (travessão)** na versão final. Se achar **qualquer** ocorrência: **REESCREVE a linha** (troca por ponto curto, vírgula ou dois-pontos, nunca por outro travessão) e **repete a varredura do zero**. Só **zero ocorrências** de `—` libera o Passo 6.
2. **CTRL+F pela família "travar/travado/destravar"** (exceção: aspa literal do cliente). Achou fora de aspa? Reescreve e varre de novo.
3. **CTRL+F pela frase-emoldura** ("a verdade é", "o segredo", "aqui está") e **verbo-clichê** ("revoluciona", "destrava", "transforma"). Achou? Reescreve e varre de novo.

Critério de parada: só passa pro Passo 6 quando as 3 varreduras zerarem. Enquanto houver **um** `—`, a skill NÃO terminou.

## Passo 6, mostra e PARA
Mostra **só a versão que passou, LIMPO** (no DOC, nunca solto no chat): a peça adaptada no formato e idioma nativos do destino. Sem tabela de gate, sem meta. **No app/claude.ai, o doc É o artifact de markdown da própria resposta; não precisa de ferramenta de arquivo. No Claude Code, é o `.md` no disco; no agente/Telegram, é o `.md` anexado.** Pergunta "essa serve? ajusto, ou adapto pra outra plataforma?". **Espera o OK** antes de adaptar pro próximo destino ou gerar variação. Uma plataforma por vez, nunca despeja todas de uma vez.

## When NOT to use (manda pra skill certa)
- Pediu a **HEADLINE/gancho/capa/abertura** do zero → **soft-conteudo-headlines**.
- Pediu **arte/visual/PNG** da versão adaptada → **soft-designer**.
- Pediu o **Plano / posicionamento / fundação** → **soft-plano-posicionamento**.
- Pediu o **CORPO original** de carrossel/reel/stories no Instagram → **soft-conteudo-carrossel / -reels / -stories**.
- Pediu **carta / VSL** → **soft-funil-carta** · **página de vendas / captura / obrigado** → **soft-funil-landing** · **mini webinar** → **soft-funil-miniwebinar**.
- Pediu uma **LEGENDA que vende** ou um **CTA de conversão** no comentário → o comentário fixado (Passo 4c) humaniza, não fecha; a venda é **soft-funil** / **soft-vendas-closer**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Traduziu cada slide em 1 parágrafo/tweet sem repensar os papéis | Mapeia os 5 papéis primeiro; re-renderiza por função, não por unidade |
| Encurtou pra caber e a tese virou frase morna | Tese preservada = ✗; reescreve mantendo a percepção central inteira |
| Versão de LinkedIn/email com cara de post do Instagram | Idioma nativo do destino (subject, 1ª linha, thread); zero copia-cola |
| Vazou "lead/funil/conversão" no LinkedIn ou no email | Volta pro campo semântico do cliente final |
| CTA virou "curte e compartilha" | CTA filtrante com destino (Direct/comentário/reply/botão) |
| Sumiu um papel sem querer (Contexto evaporou) | 5 papéis re-renderizados = ✗; recoloca o papel ou declara o colapso |
| Inventou um número/fala "plausível" na adaptação | Só herda número/fala REAL da âncora; sem fonte, `[DADO: confirmar]` e não conta como Ancorada=✓ |
| Despejou LinkedIn + X + email de uma vez | Uma plataforma por vez, com gate, e PARA pro OK |
| Narrou o fluxo ("agora vou extrair o núcleo") | Não narra: executa em silêncio e entrega só o mapa + a versão limpa, sem a tabela do gate |
| Gerou a adaptação sem perguntar a preferência do especialista | Consultiva (Lei 3): extrai duração, formato e tom desejado antes de re-renderizar |
| Imprimiu a tabela do gate na saída | O gate é INTERNO (auditoria silenciosa); a saída é só a peça limpa |
| Newsletter sem âncora: parou e mandou o dono voltar depois | É a exceção do Passo 4a: entra no modo arquétipo (molde + voz do Plano + marca de provisório), não deixa o dono na mão |
| Modo arquétipo: inventou a voz do dono do zero | Molde dá só a estrutura; a voz vem do Plano/perfil já destilado. Sem Plano, coleta o mínimo antes; sem mecanismo nomeado, manda pra soft-plano-posicionamento |
| Entregou peça em modo arquétipo sem marcar como provisória | Toda saída de arquétipo carrega a linha "Base: arquétipo X, molde emprestado, revisitar após ~5 edições reais" |
| Tinha 2+ edições passadas e mesmo assim usou arquétipo | Com exemplos, DESTILA a voz real (não usa molde); arquétipo é só cold-start sem nada |
| Comentário fixado: o texto é engraçado sozinho (imagem vira redundante) | A piada mora na IMAGEM; enfraquece o texto e reforça a imagem; morno lido sozinho = ótimo |
| Comentário fixado: o dono ganha/parece esperto em alguma linha, ou enfiou CTA de venda | Status baixo em TODA linha (ele perde com dignidade); o comentário humaniza, não vende; tira o CTA |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `references/processo-multiplataforma.md`: a engenharia reversa completa, a tabela de mapeamento com TikTok/Shorts e Mini Webinar, e os colapsos conscientes detalhados. É o mesmo processo, com mais formato e exemplo.
- `references/nucleo-soft-extracao.md`: o protocolo de extração do núcleo do Passo 2, com os 6 componentes e o checklist pós-extração.
- `references/newsletter-arquetipos.md`: os 7 moldes de newsletter/email do Passo 4a (modo arquétipo, só quando o dono não tem âncora nem histórico), cada um com abertura preenchível, espinha de seções, ancoragem Soft, tamanho e o "nunca faz". Com exemplos, destila a voz; sem, arquétipo + coleta + marca de provisório.
- `references/conducao-na-pratica.md`: o porquê por trás (conteúdo reorganiza percepção, não dá passo a passo; estoura a bolha; polariza; aponta sempre pro método). Lê quando a adaptação está tecnicamente certa mas sem alma.
- `references/estrutura-peca.md`: a Estrutura-Mãe dos 5 papéis (Capa · Capa Reserva · Contexto · Conteúdo · CTA) com as formas de cada um. É a base da engenharia reversa do Passo 3.
- **Uma reference por plataforma (dirigidas no Passo 4):** `references/plataforma-linkedin.md` · `plataforma-x-threads.md` · `plataforma-substack-email.md` · `plataforma-tiktok-shorts.md` · `plataforma-youtube-longo.md` (com o pacote de publicação) · `plataforma-pdf-notion.md` · `plataforma-mini-webinar.md`. Cada uma traz regras de formato, exemplos e checklist nativos do destino.
