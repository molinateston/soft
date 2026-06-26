---
name: soft-vendas-prospeccao
description: "Escreve a PROSPECÇÃO ativa no Direct do método Soft, a primeira mensagem que abre conversa com um lead e o leva ao pré-qualificador, sem vender na DM. Lê o sinal do lead (frio / morno / sinal ativo), ancora a abertura em algo REAL dele, qualifica em micro-ritmo (1 pergunta por mensagem), entrega Mini Carta ou Mini Webinar, e passa cada mensagem pelo gate (personalizada, abre conversa, qualifica, ancorada, tom de gente + as 3 perguntas do Harry + anti-IA) antes de mostrar. Use quando o pedido for \"prospecção\", \"prospeccao\", \"abordagem no Direct\", \"DM\", \"primeira mensagem\", \"puxar conversa\", \"abordar lead\", \"como falo com esse seguidor\". NÃO use pro SCRIPT de venda/call/fechamento (soft-vendas-script), pra conversa empacada/copiloto ao vivo (soft-vendas-copiloto), nem pra carta/landing/isca (soft-funil-carta/-landing/-isca)."
---

# Prospecção no Direct, abre a conversa, não vende

A prospecção Soft não vende pela DM. Ela abre uma conversa, qualifica de leve, e entrega o pré-qualificador (Mini Carta ou Mini Webinar). O pré-qualificador faz o trabalho pesado de filtrar e gerar desejo. A DM só puxa o lead pra dentro. Quem pula da DM fria pra call perde o filtro e fecha gente que cancela. Soft filtra, não convence.

**O que esta skill faz por você:** abre a PROSPECÇÃO no Direct/WhatsApp: a primeira mensagem que começa a conversa sem parecer abordagem de vendedor.

**As 4 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa o contexto de você antes de gerar; (4) contexto é rei. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar qualquer mensagem.**

## Output Contract (o que você entrega)
- **Diagnóstico do cenário** em 1 linha (frio / morno engajado / sinal ativo) antes de qualquer mensagem.
- A **abertura pronta**, bloco copiável, já personalizada pelo sinal real do lead. O gate roda **por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída.
- **Os 3 próximos passos**, como responder quando o lead abre, quando joga fricção, quando fecha a guarda.
- A **mensagem de entrega do pré-qualificador** (bloco copiável, com link ou palavra-chave), quando chegar a hora.
- Nota sobre **downsell** se houver sinal de ticket baixo.
- Você **para e espera** o usuário rodar a abertura antes de escrever a sequência inteira.
- Você **nunca inventa fala nem número do lead**, **nunca oferece call na primeira DM**, **nunca despeja um template genérico** e **nunca mostra mensagem que falhou no gate**.

## Passo 0, ancora antes de escrever (NÃO PULE)
Pega o **sinal real do lead** que o usuário descreveu: o que ele seguiu, comentou, baixou, perguntou, respondeu. Procura também fala do nicho na fonte do usuário (descrição do projeto → Plano colado → mensagens anteriores), 3-5 falas de dor e desejo, literais, com o N. A referência concreta da abertura nasce daí.

Três estados de entrada (declara qual é o seu antes de escrever):
- **Tem sinal concreto do lead:** ancora nele ("vi que você comentou X", "vi que baixou Y"). Caminho ideal.
- **Tem nicho mas o lead é genérico (recém-seguidor, zero interação):** ancora no motivo do follow ("vi que chegou recente"); a referência é o próprio ato de seguir, não uma fala inventada. Avisa que sem sinal a resposta cai.
- **Sem sinal e sem nicho:** pergunta numa única mensagem (o que o lead fez + nicho em 1 linha) e segue daí. Não chuta.

Número que você não confirmou entra como `[DADO: confirmar]` e não conta como Ancorada=✓. N inventado é ✗ automático.

## Passo 1, lê o cenário do lead
Identifica qual dos 3 cenários pelo sinal. Cada um tem abertura e ritmo próprios.

| Cenário | Quem é | Quando abordar | Objetivo da abertura |
|---|---|---|---|
| **1, Frio** | seguiu há 1-7 dias, pouca interação | até 24h depois do follow | puxar a essência: por que ele seguiu |
| **2, Morno engajado** | vê stories, comenta, responde caixinha há meses | quando vir 3+ interações em 2 semanas | conectar a um sinal específico que ele já deu |
| **3, Sinal ativo** | se inscreveu, baixou, mandou dúvida, respondeu "quero saber mais" | em até 2h (janela quente) | confirmar interesse e já entregar o pré-qualificador |

Regra do frio: 1 pergunta só, sem apresentação longa. Regra do morno: referência concreta ao que ele já fez, sem ela soa spam. Regra do sinal ativo: resposta rápida, a janela dura poucas horas.

## Passo 2, escreve a abertura (1 pergunta, ancorada)
Escreve a primeira mensagem no cenário certo. Uma ideia por frase. Abre com a referência concreta, fecha com **uma** pergunta. Sem "oi tudo bem", sem "espero que esteja bem", sem se apresentar por 3 linhas. Vai direto.

Antiesqueleto por cenário (adapta, nunca cola):
- **Frio:** boas-vindas curtas + nicho em 1 linha + "o que te fez começar a seguir?"
- **Morno:** "vi que você acompanha [conteúdo específico] e [comentou X]" + "como tá sendo pra você [contexto que ele citou]?"
- **Sinal ativo:** "vi que você [ação específica]" + "o que mais te chamou atenção em [tema]?" → depois da resposta, entrega o pré-qualificador.

Quebra-gelo anti-robô (opcional, frio/morno): um áudio de 5-10s falando o nome dele e a pergunta prova na hora que é gente, não bot. Fala normal, sem locução de vendedor.

## Passo 3, qualifica em micro-ritmo (os 4 elementos)
Antes de entregar o pré-qualificador, a conversa passa por 4 elementos, **1 pergunta por mensagem**, no máximo 4 mensagens. Nunca 2 perguntas juntas, vira interrogatório.

| Elemento | Pergunta base |
|---|---|
| **Essência / Situação** | "o que te fez começar a acompanhar isso?" / "qual seu contexto hoje?" |
| **Tempo / Amarras** | "isso é pra agora ou ainda quer tentar por conta antes?" / "tem algo te prendendo?" |
| **Ações** | "o que você já fez pra tentar resolver?" / "o que não funcionou?" |
| **Resultados** | "o que conseguiu sozinho?" / "o que espera ter?" |

Regra do recuo: se o lead responder com fricção ou pressa, recua. "Tranquilo, quando fizer sentido a gente conversa. Por enquanto dá uma olhada [link]." E solta. Quem recua tem mais autoridade.

## Passo 4, entrega o pré-qualificador (o momento-chave)
Depois dos 4 elementos (ou quando entendeu o suficiente), entrega **um** pré-qualificador. Nunca dois na mesma DM.

| Pré-qualificador | Quando usar |
|---|---|
| **Mini Carta** | padrão Soft, qualquer nicho, filtra por leitura |
| **Mini Webinar** | alternativa em vídeo, quando o lead prefere vídeo ou a audiência é de vídeo |

Se o usuário não tem nenhum dos dois pronto, avisa que precisa construir antes e aponta pra **soft-funil-carta** ou **soft-webinario**. Não improvisa pré-qualificador.

Molde de entrega: conecta ao que ele disse ("pelo que você me contou") + nome do pré-qualificador + o que é em 1 linha + link ou palavra-chave + **pedido de retorno** ("me fala o que mais te pegou"). Pede resposta sempre: ativa compromisso. Nunca diz "quando tiver tempo" (vira nunca). Dá prazo real e leve se o lead aceitar bem.

**Downsell:** se o lead deu sinal financeiro empacado ("tô começando", "sem orçamento", "reinvestindo tudo") ou quer "testar antes", oferece uma entrada menor em vez da Carta principal. Uma oferta só, nunca as duas juntas.

## Passo 5, roda o GATE por dentro (auditoria silenciosa, NÃO imprime)
Roda o gate em CADA mensagem **internamente** (auditoria silenciosa). Só mensagem com a linha VEREDITO=PASSA vai pro usuário. Um ✗ refaz a mensagem. A tabela abaixo é o teu **checklist interno**, nunca a saída: o usuário recebe só a mensagem limpa (Passo 6), jamais a tabela.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Personalizada** | tem referência concreta ao lead específico; não é template que serve pra qualquer um. ✗ "oi, vi seu perfil" · ✓ "vi que você comentou na aula sobre [X]" | |
| **Abre conversa (não vende)** | termina em pergunta ou convite leve, zero pitch, zero oferta de call, zero link de checkout na 1ª mensagem | |
| **Qualifica / filtra** | a pergunta puxa essência/tempo/ação/resultado, separa quem é cliente de quem é curioso; não é papo solto | |
| **Ancorada em algo real** | nasce de sinal real do lead OU de fala literal da fonte (cita N **real**); N inventado/plausível = ✗ automático | |
| **Tom de gente** | eu mandaria isso pra um conhecido; zero jargão ("lead", "funil", "pipeline", "ticket"), zero locução de vendedor, zero "tudo bem?/espero que esteja bem" | |
| **C/U/B** | Clara (lê em 2s no celular) · Útil (o lead ganha algo em ler/responder) · Breve (1 pergunta, sem parágrafo de apresentação) | |
| **CTA com destino** | o próximo passo é explícito e único: uma pergunta a responder OU um link/palavra-chave do pré-qualificador; nunca dois destinos | |
| **Harry, dá pra ver?** | a referência é uma cena/fato concreto. ✗ "vi que você curte o tema" · ✓ "vi que você respondeu a caixinha sobre [X]" | |
| **Harry, dá pra falsificar?** | a referência é um fato verificável, não um elogio genérico | |
| **Harry, só você diz?** | a abordagem não é a DM-padrão que todo vendedor manda; o ângulo é seu | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" (exceção: aspa literal do lead) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, destrava, transforma"). **No chat (sem o lint), faz um CTRL+F manual de "—" e da família "travar" antes de marcar ✓.** | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro usuário. | |

## Passo 6, mostra e PARA
Mostra **só a peça LIMPA** (como no Claude Chat): o diagnóstico do cenário (1 linha), a abertura que passou (bloco copiável) e os 3 próximos passos (como responder a cada resposta provável). Sem tabela de gate, sem meta. Pergunta "essa abertura te serve? rodo e te mando a sequência?". **Espera o OK** antes de escrever a entrega do pré-qualificador, o downsell ou os follow-ups.

Follow-up: 72h depois, **1 vez só**, leve ("só passando pra saber se conseguiu dar uma olhada; se não fez sentido, me fala que eu sumo"). Sem resposta = encerra com leveza. Não persegue.

## When NOT to use (manda pra skill certa)
- Pediu o **SCRIPT de venda / call / reunião / fechamento** → **soft-vendas-script**.
- Pediu pra **isolar/quebrar uma objeção** específica → **soft-vendas-objecao**.
- Pediu **conversa empacada / copiloto em tempo real / lead sumiu no meio da venda** → **soft-vendas-copiloto**.
- Pediu **indicação / testemunho / pós-fechamento** → **soft-vendas-posvenda**.
- Pediu **headline/gancho de feed** → **soft-conteudo-headlines**. Pediu a **carta/landing/isca** em si → **soft-funil-carta / -landing / -isca**. Pediu **posicionamento/oferta** → **soft-posicionamento**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Mandou um template genérico ("oi, vi seu perfil") | Volta: referência concreta ao sinal real do lead, senão é spam |
| Tentou vender ou marcar call na 1ª DM | A DM só abre conversa e entrega o pré-qualificador; call só depois que o lead consome e volta |
| Juntou 2-3 perguntas na mesma mensagem | 1 pergunta por mensagem, micro-ritmo, máximo 4 |
| Ofereceu Carta E downsell juntos | Uma oferta só por DM; escolhe principal OU downsell |
| Vazou jargão ("manda seu lead pro funil") | Vocabulário de gente; zero "lead/funil/pipeline/ticket" no texto |
| Abriu com "oi tudo bem?" / "espero que esteja bem" | Corta a saudação-clichê, vai direto na referência concreta |
| Inventou um número/fala "plausível" do lead | Só sinal/fala REAL; sem fonte marca `[DADO: confirmar]` e não conta como Ancorada=✓ |
| Perseguiu o lead com vários follow-ups | Follow-up 72h, 1 vez só; sem resposta, encerra e solta |
| Despejou a sequência inteira de uma vez | Mostra a abertura + 3 passos e PARA; só escreve o resto após o OK |
| Imprimiu a tabela do gate na saída | O gate é INTERNO (auditoria silenciosa); a saída é só a peça limpa |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `references/prospeccao-dm.md`: os 3 cenários completos, os 4 elementos, downsell, formulário pré-call, confirmação pré-reunião e as regras universais da DM Soft. É o mesmo fluxo acima, com mais exemplo, não um segundo sistema.
- `references/conducao-na-pratica.md`: o porquê e o como da venda consultiva Soft (vender libertando, ancorar no número, ser pequeno como vantagem), o espírito que rege a prospecção.
- `shared-references/crivo/`: o Crivo de saída detalhado (ancoragem no verbatim → simulação na pele do lead → gate CUB + 3 perguntas do Harry). É a versão longa do gate do Passo 5.
- `shared-references/adaptacao-semantica.md` e `dicionario-conversacional.md`: como tirar o jargão de marketing e falar a língua do lead.
- `scripts/lint_copy.py`: no Claude Code, roda `python3 scripts/lint_copy.py` na mensagem como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual do gate.
