---
name: soft-conteudo-headlines
description: Escreve a HEADLINE/gancho/abertura de qualquer peça do método Soft, da capa de carrossel ao título, gancho FALADO do reel (3 primeiros segundos), título de YouTube e assunto de e-mail. Ancora no verbatim e escreve DENTRO do CÂNONE POR GATILHO (6 famílias, Recompensa/Mistério/Crença/Disrupção/Popularidade/Reconhecimento) com gramática de SLOTS que puxam do Mapa de Munição da Audiência, cada uma pelo gate (standalone + CUB + as 3 perguntas + anti-IA + teto CONTADO). Plataforma não é família, é teto de renderização. Pedido aberto = BANCO COMPLETO, mínimo 50 fórmulas com 3+ headlines. Use quando o pedido for "headline", "gancho", "abertura", "manchete", "título", "chamada", "capa de carrossel", "título do YouTube", "assunto de e-mail", "primeiros segundos", "banco de headlines". NÃO use pro CORPO da peça (soft-conteudo-carrossel/-reels/-stories), nem pro Plano (soft-plano-posicionamento), nem pra arte (soft-designer), nem pra abertura de VSL (soft-funil-carta) ou da aula do webinar (soft-webinar-script).
---

# Headline, os primeiros 3 segundos

A decisão de ficar ou pular acontece em menos de 2 segundos. A abertura é 90% do jogo. A headline **filtra E atrai**: para o scroll de quem é cliente e instala a percepção que deixa a conversa mais quente depois. Ela não fecha venda (isso é na carta e no WhatsApp). Headline que só viraliza e atrai estranho falhou tanto quanto a que ninguém para.

**O que esta skill faz por você:** pega a fala real do teu cliente e gera headlines que param o scroll, usando os teus templates testados (2-3 por template). A headline decide se a pessoa lê o resto, por isso vem antes do corpo.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa o contexto de você antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: confere se tem a fala/o número/o case antes de montar e, se faltar, marca `[DADO: confirmar]` no lugar do furo e diz o que falta, jamais preenche com algo plausível; (6) **doc de output enxuto pros 2 leitores**: o que sai é otimizado pro humano que lê E pra IA que recebe como contexto: só as headlines limpas + `[DADO: confirmar]`, zero meta-narração. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar qualquer headline.**

## Output Contract (o que você entrega)
**O cânone VALIDADO é O CÂNONE POR GATILHO: 86 fórmulas T em 6 famílias de gatilho (Recompensa · Mistério · Crença · Disrupção · Popularidade/Reputação · Reconhecimento) + C1-C6 (ângulos ortogonais).** Numeração única e estável: T1-T30 mantêm o número histórico (com a família onde moram); T31-T86 são as fórmulas da Rodada 2. O cânone inteiro, com todas as fórmulas e variações, mora em `references/templates.md`, e é o que o banco completo usa. C9-C12 são INCUBADORA (`references/templates-candidatos.md`): só entram sob o comando "usa os candidatos", sempre marcados com o C-número; candidato sem métrica não vira cânone.
- **Pedido ABERTO, sem orientação específica** ("me dá headlines sobre X", "banco de headlines"): entrega o **BANCO COMPLETO no doc: no mínimo 50 fórmulas validadas, com PELO MENOS 3 headlines cada**, organizado **por família de gatilho** (nunca por plataforma). Cada grupo com **o T-número + a família + a fórmula (notação de slots) + os gatilhos** no topo. Se a ancoragem real só sustenta menos fórmulas com honestidade, entrega o que sustenta e DIZ quais faltaram e por quê (nunca inventa pra completar).
- **Pedido ESPECÍFICO** (formato, quantidade, "headline pra ESTE carrossel/reel"): obedece a orientação, escolhe 3-5 templates que encaixam, 2-3 headlines cada, com a mesma marcação de origem.
- A saída é **limpa, no doc (artifact)**. O gate roda **por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída.
- No pedido específico, você **para e espera** o cliente escolher antes de gerar mais. No banco completo, entrega o doc inteiro de uma vez e pergunta o que ajustar.
- Você **nunca inventa fala nem número do cliente** e **nunca mostra headline que falhou no gate**.


## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a peça no chat)
Regra dura, vale mesmo pra copy curta: o RESULTADO desta skill sai como **UM documento markdown consolidado**. No **claude.ai**, um **artifact de markdown** (o dono abre, copia, baixa); no **Claude Code**, um arquivo `.md`. A CONDUÇÃO (perguntas de contexto, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA/COPY em si mora no DOC. Ao parar num STOP, você mostra ou atualiza o DOC e pergunta "ajusto?"; você NUNCA reescreve a peça em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Passo 0, ancora antes de escrever (NÃO PULE)
Procura a fonte de fala real do cliente, nesta ordem: **descrição do projeto** → **Plano colado na conversa** → **mensagens anteriores**. Puxa **3-5 falas de DOR + 3-5 de DESEJO** do tema, literais, contando o N (quantas vezes apareceu). A primeira linha de cada headline nasce de uma delas, quase intacta.

Três estados de entrada (declara qual é o seu antes de escrever):
- **Tem fala real (com N):** ancora nela e cita o N. Caminho ideal.
- **Tem nicho/fundação mas ZERO fala literal:** NÃO inventa fala nem N. Cada headline ancora em **prova real do autor** (resultado, case, mecanismo); qualquer número que você não confirmou entra como `[DADO: confirmar]` e **NÃO conta como Ancorada=✓**. Avisa: minerar 5-8 falas reais (ou rodar o Plano na soft-plano-posicionamento) deixa as headlines muito mais cravadas.
- **Sem nicho e sem nada:** pergunta numa única mensagem (nicho em 1 linha + 1 dor real que o cliente fala) e segue daí.

A fundação (quando existe, do Plano): tese central · top 3 inimigos nominais · lista do "não defendo" · cliente em uma frase.

**A munição dos SLOTS vem do MAPA DE MUNIÇÃO DA AUDIÊNCIA** (os 12 campos do público, coletados pela `soft-plano-posicionamento` e salvos no Plano: desejos, dores, medos, hábitos comuns, filmes/séries/músicas, técnicas, pessoas/personagens, instituições, objetos/ferramentas, crenças, violações de expectativa, características do avatar). Cada slot das fórmulas (`references/templates.md`, gramática de slots) puxa de um desses campos. **Sem o Mapa no contexto**, NÃO inventa: pergunta numa única mensagem os **3-4 campos mais críticos pro tema** (desejos · dores · o que a audiência já conhece · características do avatar) e segue daí.

## Passo 1, escolhe o assunto que carrega a tese
Pega 1 das 3 fontes de assunto e, quando der, **cruza duas** pra multiplicar público:
- **Universal** (idade, dinheiro, tempo, medo, status) · **Nicho** (dor, desejo, crença, ferramenta do cliente) · **Momento** (algo em alta, com link claro à tese).
- A tese vai sempre por dentro. Assunto sem tese vira jornalismo que atrai estranho.
- Abre com palavra ampla (pra não expulsar), nicha do meio pro fim (onde aprofunda e filtra).

## Passo 2, escolhe a família de gatilho e as FÓRMULAS que encaixam
O cânone se organiza por **GATILHO**, não por plataforma (gancho é gancho, headline é headline). Escolhe a **família de gatilho** que o assunto pede e, dentro dela, **escolhe 3-5 fórmulas de `references/templates.md`** que encaixam no assunto + na fala real. As fórmulas são o coração do passo, não profundidade opcional. O inimigo nominal entra como **ataque** ("isso te custa X"), nunca como "ensinar a fazer melhor".

**Família ≠ gatilho rastreável.** As **6 FAMÍLIAS** organizam o cânone (onde a fórmula mora): Recompensa · Mistério · Crença · Disrupção · Popularidade/Reputação · Reconhecimento. Os **7 GATILHOS** abaixo são o que se **rastreia NA FRASE** (o que o gate conta). Autoridade **própria** e Valor prático não são família (temperam fórmulas das 6; Autoridade **emprestada** = a família Popularidade/Reputação), mas seguem rastreáveis na frase:

| # | Gatilho | Como aparece NA FRASE (rastreável) |
|---|---|---|
| 1 | Recompensa | verbo de ação + objeto desejado ("ganha", "domina") |
| 2 | Mistério | loop aberto, "isso aqui", pergunta sem resposta |
| 3 | Reconhecimento | característica ultra específica do leitor ("você que...") |
| 4 | Popularidade | nome/figura/marca/evento conhecido |
| 5 | Crença | tese forte ("X não é Y") ou senso comum atacado |
| 6 | Autoridade | A profissão ("sou X") · B resultado ("fiz X") · C emprestada ("X disse Y") |
| 7 | Disrupção | "não é A, é B" / "para de fazer X" |

**AS FÓRMULAS-ÂNCORA POR GATILHO (usa ESTAS, NUNCA invente uma fórmula genérica).** As 30 âncoras históricas (T1-T30) abaixo, seguidas das âncoras novas mais fortes da Rodada 2. Escolhe 3-5 que encaixam no assunto + na fala real; preenche com elementos concretos e reais do cliente (adapta ao nicho, nunca copia o exemplo). **O cânone COMPLETO, com todas as 86 fórmulas e as variações, mora em `references/templates.md`, e é o que o banco completo usa.**

**Âncoras históricas T1-T30** (a coluna Gatilho é o que se rastreia na frase; a família de cada uma está em `templates.md`):

| # | Template (fórmula) | Exemplo | Gatilho |
|---|---|---|---|
| 1 | Faça algo muito específico (ordem direta + razão no corpo) | "Seja chato em 2026." | Autoridade + Disrupção |
| 2 | Coisas que eu [faço/deixei de fazer] sendo [autoridade] | "Cremes que eu não passo no rosto sendo dermatologista." | Autoridade |
| 3 | Coisas que parecem normais mas geram [dano] | "Alimentos que parecem saudáveis mas emperram seu intestino." | Disrupção |
| 4 | Esse é o maior motivo disso acontecer | "Esse é o maior motivo do seu carrossel não viralizar." | Mistério |
| 5 | Crença popular que você quer confrontar | "Comer ovo todo dia faz mal. É isso que falam, mas..." | Crença + Disrupção |
| 6 | O inimigo pôs a mão em tal coisa e ela mudou | "A indústria pôs a mão no sorvete e ele mudou." | Disrupção + Crença |
| 7 | O inimigo do meu público adora quando você faz isso | "O banco adora cliente que faz essas 4 coisas." | Reconhecimento + Disrupção |
| 8 | Demorei X anos pra aprender, te explico em X segundos | "Levei 8 anos de psicanálise pra descobrir isso. Resumo em 1 minuto." | Recompensa + Autoridade |
| 9 | Toda pessoa com [característica ultra específica] precisa saber disso | "Toda pessoa que tem casa de aluguel precisa saber disso." | Reconhecimento |
| 10 | Coisas que são uma verdadeira [autoridade] em [área] | "3 livros que são um MBA em finanças." | Popularidade + Recompensa |
| 11 | Na próxima vez que você for [situação], faça isso | "Da próxima vez que for fechar um cliente, não faça reunião." | Recompensa + Valor prático |
| 12 | Coisas que transformam X em Y | "4 hábitos que transformam sua insônia no sono mais restaurador." | Recompensa |
| 13 | X é assim, Y é assim (contraste visual) | "O coração de um diabético é assim. O de uma pessoa normal é assim." | Disrupção |
| 14 | O que fazer quando [algo cotidiano acontece] | "O que fazer quando o cliente pede desconto na hora do fechamento." | Valor prático + Reconhecimento |
| 15 | Esse vídeo é um alerta para [pessoas com essa característica] | "Alerta para quem toma anticoncepcional há mais de 10 anos." | Reconhecimento + Mistério |
| 16 | O item mais subestimado tem esses benefícios | "A vitamina mais subestimada do Brasil custa R$12 e resolve insônia." | Mistério + Recompensa |
| 17 | Fazer isso gera essas consequências | "Pedir desculpa demais gera essas 3 consequências no casamento." | Recompensa + Reconhecimento |
| 18 | Situações onde você tem permissão pra quebrar regras | "3 situações onde você tem permissão para demitir um cliente." | Disrupção + Autoridade |
| 19 | Enquanto pessoas com X, é isso que pessoas com Y fazem | "Enquanto empresários vivem em reunião, é isso que CEOs fazem." | Reconhecimento + Disrupção |
| 20 | Se você tem [características], isso aqui é obrigatório | "Faturando acima de 50 mil/mês? Esse software é obrigatório." | Reconhecimento + Autoridade |
| 21 | O que acontece quando você faz [ação ultra específica] | "O que acontece quando você dorme após as 23 horas." | Mistério + Reconhecimento |
| 22 | Sinais que você é uma pessoa com [características] | "Sinais que você está burnout e ainda não sabe." | Reconhecimento + Mistério |
| 23 | É assim que [situação dolorosa] está acontecendo | "É assim que empresas familiares estão sumindo no Brasil." | Mistério + Disrupção |
| 24 | Antes que [situação específica] aconteça, faça isso | "Antes de assinar com a empreiteira, exija esses 4 itens." | Recompensa + Autoridade |
| 25 | X coisas que trazem esses [benefícios/malefícios] | "5 hábitos que aumentam testosterona em homens acima de 35." | Recompensa |
| 26 | [Assunto quente] não aconteceu pelo que você acredita | "O Banco Master não quebrou por má gestão, é por algo que vai te assustar." | Disrupção + Mistério |
| 27 | [Situação dolorosa] acontece porque você faz isso | "O Instagram não entrega porque você tenta parecer inteligente demais." | Reconhecimento + Disrupção |
| 28 | Isso não é o que você pensa (sempre com imagem) | "Isso não é estiloso, isso não é estiloso, isso não é se vestir bem." | Disrupção |
| 29 | O [melhor/pior] pra [situação] não é X, não é Y, não é Z | "O exame mais importante pro coração não é colesterol, não é glicose, e o médico não pede." | Mistério |
| 30 | Erros que você comete ao [ação comum] e como evitar | "4 erros que você comete na primeira reunião com um cliente." | Reconhecimento + Recompensa |

**Âncoras novas da Rodada 2** (as mais fortes; 1 por linha, com T-número e família. O cânone inteiro está em `templates.md`):

| T# | Família | Fórmula (slots) | Exemplo |
|---|---|---|---|
| T31 | Recompensa | Como [DESEJO] | "Como acabar com manchas na pele" |
| T36 | Recompensa | [X] que substitui [OBJEÇÃO] | "Treino de 4 min que substitui 1 hora de academia" |
| T40 | Recompensa | De [PROBLEMA/DOR] a [DESEJO] | "De agenda vazia a aula vendendo sozinha" |
| T42 | Recompensa | Fiz [X] fazendo isso (prova crua) | "5 vendas saíram de uma aula só" |
| T43 | Mistério | [X] coisas piores do que [CONHECIDO] | "5 carboidratos piores que o açúcar" |
| T53 | Mistério | A ciência por trás de [PROBLEMA/HÁBITO] | "A ciência por trás da procrastinação" |
| T58 | Mistério | [X] coisas que [INSTITUIÇÃO] esconde de você | "5 investimentos que o banco esconde de você" |
| T61 | Mistério | [PERGUNTA LITERAL DA AUDIÊNCIA] | "Quanto eu ganho com 1 milhão de views?" |
| T62 | Mistério | [AÇÃO JÁ ACONTECENDO] (in media res) | "Ontem às 22h, três vendas caíram" |
| T64 | Crença | Eu estava errado sobre [CONHECIDO] (confissão) | "Vendi do jeito errado por anos, olha o que mudou" |
| T66 | Crença | Como eu [DESEJO] fazendo [ALGO CONTRA A CRENÇA] | "Como fiquei rico comprando imóvel financiado" |
| T67 | Crença | [CONHECIDO], você está fazendo isso errado | "Agachamento, você está fazendo errado" |
| T70 | Disrupção | Fazendo [COMPORTAMENTO QUE VIOLA A EXPECTATIVA] pela 1ª vez | "Comprando seguidores pela primeira vez" |
| T71 | Disrupção | Não abre esse [X] (negação) | "Não abre esse e-mail se você vende no direct" |
| T75 | Popularidade | Vivi como [PERSONAGEM/ESTILO] por [TEMPO] | "Copiei a carteira do Warren Buffett por 30 dias" |
| T78 | Popularidade | A [TÉCNICA] de [PERSONAGEM/CULTURA] para [DESEJO] | "A técnica japonesa para superar a preguiça" |
| T80 | Reconhecimento | Como [DESEJO] se você é [AVATAR] | "Como ganhar massa muscular depois dos 40" |
| T81 | Reconhecimento | [X] coisas que só quem é [AVATAR] entende | "10 coisas que só quem é diabético passa" |
| T86 | Reconhecimento | Se [SITUAÇÃO] acontecer, faça isso imediatamente | "Se ver esses 3 sinais nas campanhas, pause já" |

> **Regra dura:** as fórmulas do cânone são as 86 de `references/templates.md` (T1-T86, nas 6 famílias). Se você escreveu um "template" fora do cânone, você INVENTOU (é o erro a não cometer). No máximo adapta/combina ao nicho do cliente. `templates.md` traz todas com slots, exemplos, variações e a família de cada uma.

**Plataforma NÃO é família: é teto de RENDERIZAÇÃO.** A mesma fórmula serve pra qualquer formato; o que muda é quanto texto cabe. A tabela de tetos por formato está no gate (Passo 4); o protocolo de compressão (a mesma fórmula apertada pro teto de reel/YouTube/e-mail/capa) está em `references/subcanones-formato.md`. Não existe fórmula exclusiva de plataforma.

**Comandos rápidos:** "**usa os candidatos**" libera C9-C12 da incubadora (sempre marcados com o C-número na saída). "**minera benchmark de [tema]**" roda nova rodada de mineração com veredito de dedup contra o cânone ANTES de propor candidato (no app sem web, conduz com o material que o dono colar); registro em `references/mineracao-benchmark.md`.

### Régua de cobertura de ângulo (camada de VARIAÇÃO, roda POR CIMA das fórmulas do cânone)
Fórmula diz a ESTRUTURA da frase. Ângulo diz de que LADO psicológico você ataca o mesmo tema. Duas fórmulas diferentes podem cair no mesmo ângulo (dois jeitos de "confessar") e aí o cliente recebe 6 headlines que soam iguais por dentro. Esta régua garante DIVERSIDADE de ataque: quando o pedido é solto ("me dá 6 aberturas", "gera uns ganchos rápido", "headlines sobre X" sem número), o conjunto entregue cobre **pelo menos 4 dos 6 ângulos abaixo**, cada um mapeado a uma fórmula do cânone. Ela NÃO substitui os 7 gatilhos nem as fórmulas T: é um checklist de cobertura por cima deles.

| Ângulo | O lado que ataca | Templates que costumam servir |
|---|---|---|
| **Número** | abre com um número/métrica que o leitor calcula (algarismo, não extenso) | T8, T10, T16, T17, T25, T30 |
| **Contrária** | declara uma crença aceita e vira ela do avesso | T5, T6, T13, T26, T27, T29 |
| **Transformação** | antes vs depois, com o número que prova a virada | T12, T13, T19 |
| **Autoridade** | ancora em quem fala (profissão, resultado real, nome citado) | T1, T2, T8, T18 |
| **Confissão** | assume um erro, uma perda, um "eu deixei de" | T2, T22, T30 |
| **Futuro** | previsão ou alerta do que está prestes a mudar | T15, T23, T24, T26 |

**Como usar (não é passo novo, é lente do Passo 2-3):**
- Pedido de VOLUME solto (6 aberturas, "uns ganchos", banco): antes de fechar, confere quantos ângulos distintos o conjunto cobre. **Menos de 4 ângulos = repetitivo, troca 1-2 templates por outros de ângulo faltante** e regenera essas headlines.
- Pedido de CENA única (Comando 3, "headline pra esse reel"): cobertura não obrigatória, mas as 3-5 opções devem variar o ângulo pra dar escolha real ao cliente.
- **A ancoragem manda sobre a cobertura.** Se a fala real do cliente só dá base honesta pra 3 ângulos, entrega 3 bem ancorados e diz que faltam falas pra cobrir os outros. NUNCA inventa número/fala só pra fechar um ângulo (fere a Lei 5 e o gate).
- Todo template escolhido continua passando pelo gate normal do Passo 4; a régua só decide QUAIS templates entram no conjunto, não afrouxa nenhum critério.

## ✍️ PRÉ-FLIGHT DE COPY (relê IMEDIATAMENTE antes de escrever a 1ª linha)
Escreve JÁ dentro do gate, nunca pra ser corrigido por ele depois:
1. **Munição na mão:** verbatim/prova real do dono na frente (sem munição = pergunta, jamais inventa).
2. **Uma ideia por frase.** Número em algarismo no lugar de adjetivo.
3. **Voz do cliente final:** zero jargão de marketing (lead, funil, ticket, copy).
4. **Standalone:** cada frase entendida sem contexto e sem explicação.
5. **Anti-IA:** zero travessão, zero família banida, zero frase-emoldura, zero clichê de robô.
6. **Promessa do tamanho da prova:** menor com chão ganha de grande sem chão.
7. **Teto do formato conhecido ANTES de escrever** (conta durante, não conserta depois).
Depois de escrita, a auditoria do gate confere DE FATO (busca e contagem). Reprovou, reescreve ANTES de mostrar.

## Passo 3, escreve 2-3 headlines DENTRO de cada template
Pra cada template escolhido, escreve **2-3 headlines**, todas ancoradas na fala real (Passo 0). Estilo Soft: uma ideia por frase, número no lugar de adjetivo, vocabulário do cliente final (nunca "lead/funil/ticket"), tom de comando, nunca morno. **Clareza acima de tudo (Lei 1): nada de palavra difícil, nada de figura de linguagem vazia ("mensagem cheia"), só o que uma pessoa real diria.** Toda headline nasce **curta e densa, reaproveitável em qualquer formato** (capa, reel, post, story). **Quando o formato-destino já é conhecido, comprime pra ele, respeitando OS DOIS eixos (palavras E caracteres com espaço):** reel falado ≤7 palavras nos 3s · reel texto na tela ≤5 palavras E ≤40 caracteres/linha · capa de carrossel 8-15 palavras E ≤65 caracteres na linha-título · story 5-10 palavras E ≤50 caracteres no topo · anúncio ≤5 palavras · email 8-12 palavras E ≤45 caracteres no assunto · YouTube 50-70 caracteres. A tabela completa dos 8 formatos vai INLINE no Passo 4 (é o alvo que o gate conta); o protocolo de redução detalhado está em `references/criterios-v2.md`. **Tempero, só se a headline estiver chapada:** injeta 1 dispositivo de `references/dispositivos-de-frase.md` (preparação+virada, antítese, dizer o não-dito, evocação sensorial), nunca no lugar da ideia. No topo de cada grupo, declara o **template (nome/fórmula) + os gatilhos** que ele aciona. **Não narra o fluxo**, só entrega limpo, organizado por template.

## Passo 4, roda o GATE por dentro (auditoria interna, NÃO imprime)
Roda o gate em CADA headline **internamente** (auditoria silenciosa). Só headline que passa em TODOS os critérios vai pro cliente. Uma falha refaz a frase (não o conceito). A tabela abaixo é o teu **checklist interno**, nunca a saída: o usuário recebe só as headlines limpas (Passo 5), jamais a tabela.

### Os TETOS que o gate conta (números inline, não deixa pra reference)
O check "Teto físico do formato" manda CONTAR contra um alvo. O alvo mora AQUI, no corpo, pra você não contar contra número de memória-vaga. Onde os DOIS eixos aparecem, os DOIS têm que passar (uma capa de 12 palavras que dá 80 caracteres **estoura** e falha).

| Formato-destino | Teto em palavras | Teto em caracteres (com espaço) |
|---|---|---|
| Reel, 3s falados | ≤ 7 | n/a (é falado) |
| Reel, texto na tela | ≤ 5 | ≤ 40 por linha |
| **Carrossel, capa** | **8 a 15** | **≤ 65 na linha-título (frase de maior peso)** |
| Stories, abertura | 5 a 10 | ≤ 50 na linha de topo |
| Anúncio, 1.7s falados | ≤ 5 | n/a (é falado) |
| Anúncio, 5s falados | ≤ 10 | n/a (é falado) |
| Email/Substack, assunto | 8 a 12 | ≤ 45 no assunto |
| Título de YouTube | n/a | 50 a 70 |

**Contagem:** número em algarismo conta 1 palavra ("40 anos" = 2); caractere = letra + espaço + pontuação (espaço conta). Número sempre em algarismo ("3", nunca "três"): ocupa menos e lê mais rápido.

**MARGEM DE SEGURANÇA no app/chat (sem Bash):** contar caractere de cabeça é impreciso e o erro típico é 15-30 caracteres pro lado do PASSA. Então trate o teto com FOLGA, não no fio: se a frase-título passa visivelmente de ~8-10 palavras OU tem 2 orações longas ("...na academia, mesmo sendo personal"), **presuma ESTOURO e comprime, nunca arredonde pra baixo pra caber**. Duas orações longas quase sempre quebram JUNTO o teto de caractere E o check "Curta e densa" (uma ideia por frase). No Claude Code/agente (com Bash), conta de fato: `echo -n "a headline" | wc -m` (caracteres) e `| wc -w` (palavras) antes de marcar ✓.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorada** | nasce de fala literal da fonte (cita N **real**) OU de prova real do autor; **N inventado/plausível = ✗ automático**; fecha em chão/número/cena, não em tese solta bonita | |
| **Gatilhos rastreáveis** | **≥2 dos 7 gatilhos rastreáveis na frase (ideal 3); 1 só = ✗**, e "no espírito" não conta | |
| **Target-leigo** | zero palavra-container sem adjetivo concreto. ✗ "um sistema que transforma" · ✓ "sistema de aquisição por indicação" | |
| **STANDALONE, sem contexto e sem explicação (Lei 1)** | a headline se sustenta SOZINHA: num print isolado, quem nunca te viu entende e para. Se precisa da linha de cima, de "ou seja" ou de um rodapé explicando, REPROVA. Zero palavra difícil, cria o contexto dentro da própria frase. ✗ "reorganize a percepção de valor" · ✓ "cobra o que você vale sem o cliente achar caro" | |
| **CUB** | a frase carrega com força pelo menos 1 dos três: Curiosidade real (loop que o cérebro quer fechar) · Utilidade/valor prático · Benefício concreto. Nenhum dos três = frase morta, refaz | |
| **Stranger às 22h** | benefício concreto OU curiosidade real OU dor específica. ✗ "o futuro da nutrição é a personalização" · ✓ "treina 2 anos e a bioimpedância não mexe" | |
| **Mesa-sentado** | eu falaria pro cliente na cara dele. ✗ "descubra o segredo que mudou tudo" · ✓ "cobrei 3x mais e o cliente agradeceu" | |
| **Curta e densa (serve pra tudo)** | diz mais com menos; corta toda palavra que não muda o sentido; curta mas NÃO rasa; nunca encurta até virar figura vazia (Lei 1). **Uma ideia por frase: headline que virou 2 orações longas encadeadas ("...na academia, mesmo sendo personal") já falha aqui E no Teto; comprime pra uma oração.** A mesma headline serve de capa, reel, post ou story | |
| **Teto físico do formato (CONTA, não estima)** | quando o formato-destino é conhecido, a headline respeita **os dois eixos da tabela de tetos acima** (palavras E caracteres com espaço) e você **CONTA de fato**, não chuta no olho. Estourou 1 unidade em qualquer eixo = ✗ e comprime (não corta o gatilho). No app/chat sem Bash, vale a MARGEM DE SEGURANÇA acima: 2 orações longas ou muito acima de ~10 palavras = presume estouro. Ex.: capa "8-15 palavras" que só cabe se a linha-título ≤ 65 caracteres, senão vira parágrafo e não lê como capa. Número em algarismo, nunca por extenso | |
| **Não-defendo** | não ensina a fazer melhor uma prática da lista do "não defendo" | |
| **Dá pra ver?** | fecha o olho e enxerga a cena. ✗ "tenha mais clareza" · ✓ "a recepcionista diz: semana que vem enche" | |
| **Dá pra falsificar?** | é um fato falsificável, não um adjetivo | |
| **Só você diz?** | o concorrente direto não assina igual (cena/mecanismo proprietário, não promessa banal do nicho) | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, destrava, transforma") · **repetição paralela idêntica em série (a mesma casca sintática 2-3x seguidas, tipo "...é assim. Com Y é assim.") também é tell**; em T13/T28 varia a estrutura, não copia a moldura. **No chat (sem o lint), faz um CTRL+F manual de "—" e da família "travar" antes de marcar ✓.** | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

## Passo 5, mostra e PARA
Mostra **só as que passaram, agrupadas por template, LIMPO** (no DOC, nunca solto no chat): cada grupo com o **template nomeado + os gatilhos** no topo e as 2-3 headlines embaixo. Sem tabela de gate, sem meta. Pergunta "quais te servem? ajusto, troco de template, ou gero mais?". **Espera a escolha** antes de gerar volume ou passar pro corpo (soft-conteudo-carrossel / -reels / -stories).

## COMO ENTREGAR (o banco de headlines vira doc MD)
O resultado (as headlines agrupadas por template) é o entregável, e o cliente quer GUARDAR ele. Entrega como **documento markdown**: no **claude.ai** como um **artifact de markdown** (o banco que ele abre, copia e reusa), no **Claude Code** como arquivo `.md`. No **agente/Telegram**: gera o banco como arquivo `.md` e cita o path completo na resposta (o bridge anexa), com a condução em mensagens curtas, sem markdown pesado (sem `##`, sem tabela). A condução (perguntas, escolha de template, o gate por dentro) acontece no chat; o **banco de headlines sai como doc**, agrupado por template, não só solto no meio da conversa. Volume (banco de 50/100/200/300) é SEMPRE doc.

## When NOT to use (manda pra skill certa)
- Pediu o **CORPO** da peça → **soft-conteudo-carrossel** (slides do carrossel) · **soft-conteudo-reels** (roteiro do reel) · **soft-conteudo-stories** (arco de stories).
- Pediu o **Plano / posicionamento / fundação** → **soft-plano-posicionamento**.
- Pediu **arte/visual/PNG** → **soft-designer**.
- Pediu **abertura de VSL** → **soft-funil-carta** · **abertura da aula do webinar** → **soft-webinar-script** (a headline de palco é operada lá).

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Despejou 10 headlines soltas, sem template | Volta: 2-3 DENTRO de cada template escolhido, agrupadas, com gate, e PARA pra escolher |
| Inventou um número/fala "plausível" | Só número/fala REAL; sem fonte, marca `[DADO: confirmar]` e não conta como Ancorada=✓ |
| Palavra-container solta ("um sistema que transforma") | Troca por imagem concreta com adjetivo + número |
| Inimigo virou "5 erros ao fazer X" | Ataca como erro estrutural, não como prática a melhorar |
| Mistério vácuo ("tem algo que ninguém conta") | Dá a textura/pista concreta do que está em jogo |
| Headline bonita mas genérica (concorrente assina) | Falha no gate "só você diz"; reescreve com cena/mecanismo proprietário |
| Narrou o fluxo ("agora vou auditar") | Não narra: executa em silêncio e entrega só as headlines limpas, sem a tabela do gate |
| Headline que só quem já é de dentro entende | Falha na Clareza (Lei 1): reescreve criando o contexto e troca a palavra difícil pela simples |
| Figura de linguagem vazia ("mensagem cheia") | Curto nunca acima de claro: reescreve concreto, como uma pessoa real diria ("muitas mensagens pra responder e zero contratos") |
| Imprimiu a tabela do gate na saída | O gate é INTERNO (auditoria silenciosa); a saída é só template + gatilhos + as headlines limpas |
| Inventou uma fórmula genérica (não é uma fórmula do cânone) | Usa as fórmulas T do cânone por gatilho (`templates.md`); adapta ao nicho, nunca cria fórmula do zero |
| Organizou o banco por plataforma (reel/YouTube/e-mail) | Organiza por FAMÍLIA de gatilho; plataforma é só teto de renderização (comprime a mesma fórmula) |
| Entregou as headlines só soltas no chat, sem doc | O banco sai como doc MD (artifact no claude.ai / arquivo no Code); o chat é a condução |
| Promoveu candidato sem métrica | C9-C12 são incubadora: só sob "usa os candidatos", sempre com o C-número; viram cânone SÓ com baseline batido em 2+ peças reais do dono |
| Alegou "todas dentro do teto" sem contar | O teto é CONTADO (palavras E caracteres); declarar conformidade sem contagem é gate falso, o erro mais grave |
| Banco "completo" com menos de 50 templates, calado | Ou entrega os 50+ validados, ou DIZ quais faltaram e por quê (ancoragem insuficiente); nunca entrega menos em silêncio |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `references/templates.md`: **O CÂNONE POR GATILHO completo** (as 86 fórmulas T nas 6 famílias, com a gramática de slots no topo, os exemplos multi-nicho, as variações fundidas e as notas de refinamento) + a numeração C1-C6 dos ângulos. **Central nos Passos 2-3.**
- `references/subcanones-formato.md`: **renderização por formato** (a MESMA fórmula comprimida pro teto de cada formato, com o exemplo de uma fórmula renderizada nos 4 formatos e a evidência de cada teto). Plataforma não é família, é camada de renderização. A tabela de tetos está inline no gate (Passo 4).
- `references/templates-candidatos.md`: a INCUBADORA (C9-C12) com fichas completas e a regra de promoção por métrica. Só via "usa os candidatos".
- `references/mineracao-benchmark.md`: o registro das rodadas de mineração (metodologia, fontes, dedup) e o protocolo do comando "minera benchmark de [tema]".
- `references/criterios-v2.md`: o detalhamento do gate do Passo 4 (rastreabilidade física dos 7 gatilhos + exemplos passa/falha por nicho + comprimento por 8 formatos). É o mesmo gate, com mais exemplo, não um segundo sistema.
- `references/comandos-rapidos.md`: lógica de volume (50/100/200/300) e protocolo de lotes do "banco de [tema]".
- `references/modo-input-livre.md`: decodar um viral de outro nicho pra modelar.
- `references/amplificadores.md`: as frases curtas que precedem a headline no reel falado/story.
- `references/dispositivos-de-frase.md`: o repertório de tempero (preparação+virada, âncora do cotidiano, dizer o não-dito, evocação sensorial, antítese) que realça a headline na revisão, depois da ideia de pé. **Dirigido no Passo 3.**
- `scripts/lint_copy.py`: no Claude Code, roda `python3 scripts/lint_copy.py` na headline como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual do gate.
