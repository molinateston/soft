---
name: soft-conteudo-headlines
description: Escreve a HEADLINE/gancho/abertura de uma peça do método Soft, os primeiros 3 segundos que param o scroll e filtram o cliente certo. Ancora no verbatim do cliente, cruza o assunto com os teus templates testados, escreve 2-3 headlines por template, e passa cada uma pelo gate (ancoragem + clareza + as 3 perguntas do Harry + anti-IA) antes de mostrar. Use quando o pedido for "headline", "gancho", "abertura", "manchete", "título", "chamada", "capa de carrossel", "primeiros segundos", "banco de headlines". NÃO use pro CORPO da peça (o texto longo, slides do carrossel, roteiro do reel ou arco de stories vão pra soft-conteudo-carrossel/-reels/-stories), nem pro Plano/posicionamento (soft-posicionamento), nem pro visual/arte (soft-designer), nem pra abertura de VSL/webinar (soft-webinario).
---

# Headline, os primeiros 3 segundos

A decisão de ficar ou pular acontece em menos de 2 segundos. A abertura é 90% do jogo. A headline **filtra E atrai**: para o scroll de quem é cliente e instala a percepção que deixa a conversa mais quente depois. Ela não fecha venda (isso é na carta e no WhatsApp). Headline que só viraliza e atrai estranho falhou tanto quanto a que ninguém para.

**O que esta skill faz por você:** pega a fala real do teu cliente e gera headlines que param o scroll, usando os teus templates testados (2-3 por template). A headline decide se a pessoa lê o resto, por isso vem antes do corpo.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa o contexto de você antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: confere se tem a fala/o número/o case antes de montar e, se faltar, marca `[DADO: confirmar]` no lugar do furo e diz o que falta, jamais preenche com algo plausível; (6) **doc de output enxuto pros 2 leitores**: o que sai é otimizado pro humano que lê E pra IA que recebe como contexto: só as headlines limpas + `[DADO: confirmar]`, zero meta-narração. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar qualquer headline.**

## Output Contract (o que você entrega)
- Por padrão, **escolhe os templates que encaixam no assunto** (de `references/templates.md`) e escreve **2-3 headlines DENTRO de cada template**, agrupadas por template. É assim que se ensina headline: a mesma ideia rendida por várias fórmulas testadas. Nunca uma lista solta de 10 genéricas.
- A saída é **limpa, como no Claude Chat**: cada grupo traz **o template nomeado + os gatilhos que ele aciona** no topo, e as 2-3 headlines embaixo. O gate roda **por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída.
- Você **para e espera** o cliente escolher/ajustar antes de gerar mais ou passar pro corpo.
- Volume grande (banco de 50/100/200/300) só sob o comando explícito "banco de [tema]".
- Você **nunca inventa fala nem número do cliente** e **nunca mostra headline que falhou no gate**.

## Passo 0, ancora antes de escrever (NÃO PULE)
Procura a fonte de fala real do cliente, nesta ordem: **descrição do projeto** → **Plano colado na conversa** → **mensagens anteriores**. Puxa **3-5 falas de DOR + 3-5 de DESEJO** do tema, literais, contando o N (quantas vezes apareceu). A primeira linha de cada headline nasce de uma delas, quase intacta.

Três estados de entrada (declara qual é o seu antes de escrever):
- **Tem fala real (com N):** ancora nela e cita o N. Caminho ideal.
- **Tem nicho/fundação mas ZERO fala literal:** NÃO inventa fala nem N. Cada headline ancora em **prova real do autor** (resultado, case, mecanismo); qualquer número que você não confirmou entra como `[DADO: confirmar]` e **NÃO conta como Ancorada=✓**. Avisa: minerar 5-8 falas reais (ou rodar o Plano na soft-posicionamento) deixa as headlines muito mais cravadas.
- **Sem nicho e sem nada:** pergunta numa única mensagem (nicho em 1 linha + 1 dor real que o cliente fala) e segue daí.

A fundação (quando existe, do Plano): tese central · top 3 inimigos nominais · lista do "não defendo" · cliente em uma frase.

## Passo 1, escolhe o assunto que carrega a tese
Pega 1 das 3 fontes de assunto e, quando der, **cruza duas** pra multiplicar público:
- **Universal** (idade, dinheiro, tempo, medo, status) · **Nicho** (dor, desejo, crença, ferramenta do cliente) · **Momento** (algo em alta, com link claro à tese).
- A tese vai sempre por dentro. Assunto sem tese vira jornalismo que atrai estranho.
- Abre com palavra ampla (pra não expulsar), nicha do meio pro fim (onde aprofunda e filtra).

## Passo 2, escolhe os gatilhos e os TEMPLATES que encaixam
Vê quais dos **7 gatilhos** o assunto pede e, com eles, **escolhe 3-5 templates de `references/templates.md`** que encaixam no assunto + na fala real. Os templates são o coração do passo, não profundidade opcional. O inimigo nominal entra como **ataque** ("isso te custa X"), nunca como "ensinar a fazer melhor".

| # | Gatilho | Como aparece NA FRASE (rastreável) |
|---|---|---|
| 1 | Recompensa | verbo de ação + objeto desejado ("ganha", "domina") |
| 2 | Mistério | loop aberto, "isso aqui", pergunta sem resposta |
| 3 | Reconhecimento | característica ultra específica do leitor ("você que...") |
| 4 | Popularidade | nome/figura/marca/evento conhecido |
| 5 | Crença | tese forte ("X não é Y") ou senso comum atacado |
| 6 | Autoridade | A profissão ("sou X") · B resultado ("fiz X") · C emprestada ("X disse Y") |
| 7 | Disrupção | "não é A, é B" / "para de fazer X" |

(Os 30 templates por gatilho estão em `references/templates.md`. Lê e escolhe os que encaixam: é o passo central, não opcional.)

## Passo 3, escreve 2-3 headlines DENTRO de cada template
Pra cada template escolhido, escreve **2-3 headlines**, todas ancoradas na fala real (Passo 0). Estilo Soft: uma ideia por frase, número no lugar de adjetivo, vocabulário do cliente final (nunca "lead/funil/ticket"), tom de comando, nunca morno. **Clareza acima de tudo (Lei 1): nada de palavra difícil, nada de figura de linguagem vazia ("mensagem cheia"), só o que uma pessoa real diria.** Toda headline nasce **curta e densa, reaproveitável em qualquer formato** (capa, reel, post, story). **Quando o formato-destino já é conhecido, comprime pra ele:** reel ≤7 palavras nos 3s · texto na tela ≤5 · capa de carrossel 8-15 · story 5-10 · anúncio ≤5 (tabela dos 8 formatos + protocolo de redução em `references/criterios-v2.md`). **Tempero, só se a headline estiver chapada:** injeta 1 dispositivo de `references/dispositivos-de-frase.md` (preparação+virada, antítese, dizer o não-dito, evocação sensorial), nunca no lugar da ideia. No topo de cada grupo, declara o **template (nome/fórmula) + os gatilhos** que ele aciona. **Não narra o fluxo**, só entrega limpo, organizado por template.

## Passo 4, roda o GATE por dentro (auditoria interna, NÃO imprime)
Roda o gate em CADA headline **internamente** (auditoria silenciosa). Só headline que passa em TODOS os critérios vai pro cliente. Uma falha refaz a frase (não o conceito). A tabela abaixo é o teu **checklist interno**, nunca a saída: o usuário recebe só as headlines limpas (Passo 5), jamais a tabela.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorada** | nasce de fala literal da fonte (cita N **real**) OU de prova real do autor; **N inventado/plausível = ✗ automático**; fecha em chão/número/cena, não em tese solta bonita | |
| **Gatilhos rastreáveis** | **≥2 dos 7 gatilhos rastreáveis na frase (ideal 3); 1 só = ✗**, e "no espírito" não conta | |
| **Target-leigo** | zero palavra-container sem adjetivo concreto. ✗ "um sistema que transforma" · ✓ "sistema de aquisição por indicação" | |
| **Clareza, sem contexto presumido (Lei 1)** | dá pra entender sem já ser de dentro; cria o contexto antes da afirmação; zero palavra difícil. ✗ "reorganize a percepção de valor" · ✓ "cobra o que você vale sem o cliente achar caro" | |
| **Stranger às 22h** | benefício concreto OU curiosidade real OU dor específica. ✗ "o futuro da nutrição é a personalização" · ✓ "treina 2 anos e a bioimpedância não mexe" | |
| **Mesa-sentado** | eu falaria pro cliente na cara dele. ✗ "descubra o segredo que mudou tudo" · ✓ "cobrei 3x mais e o cliente agradeceu" | |
| **Curta e densa (serve pra tudo)** | diz mais com menos; corta toda palavra que não muda o sentido; curta mas NÃO rasa; nunca encurta até virar figura vazia (Lei 1). A mesma headline serve de capa, reel, post ou story | |
| **Não-defendo** | não ensina a fazer melhor uma prática da lista do "não defendo" | |
| **Harry, dá pra ver?** | fecha o olho e enxerga a cena. ✗ "tenha mais clareza" · ✓ "a recepcionista diz: semana que vem enche" | |
| **Harry, dá pra falsificar?** | é um fato falsificável, não um adjetivo | |
| **Harry, só você diz?** | o concorrente direto não assina igual (cena/mecanismo proprietário, não promessa banal do nicho) | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, destrava, transforma"). **No chat (sem o lint), faz um CTRL+F manual de "—" e da família "travar" antes de marcar ✓.** | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

## Passo 5, mostra e PARA
Mostra **só as que passaram, agrupadas por template, LIMPO** (como no Claude Chat): cada grupo com o **template nomeado + os gatilhos** no topo e as 2-3 headlines embaixo. Sem tabela de gate, sem meta. Pergunta "quais te servem? ajusto, troco de template, ou gero mais?". **Espera a escolha** antes de gerar volume ou passar pro corpo (soft-conteudo-carrossel / -reels / -stories).

## When NOT to use (manda pra skill certa)
- Pediu o **CORPO** da peça → **soft-conteudo-carrossel** (slides do carrossel) · **soft-conteudo-reels** (roteiro do reel) · **soft-conteudo-stories** (arco de stories).
- Pediu o **Plano / posicionamento / fundação** → **soft-posicionamento**.
- Pediu **arte/visual/PNG** → **soft-designer**.
- Pediu **abertura de VSL / webinar** → **soft-webinario** (a headline de webinar é operada lá).

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Despejou 10 headlines soltas, sem template | Volta: 2-3 DENTRO de cada template escolhido, agrupadas, com gate, e PARA pra escolher |
| Inventou um número/fala "plausível" | Só número/fala REAL; sem fonte, marca `[DADO: confirmar]` e não conta como Ancorada=✓ |
| Palavra-container solta ("um sistema que transforma") | Troca por imagem concreta com adjetivo + número |
| Inimigo virou "5 erros ao fazer X" | Ataca como erro estrutural, não como prática a melhorar |
| Mistério vácuo ("tem algo que ninguém conta") | Dá a textura/pista concreta do que está em jogo |
| Headline bonita mas genérica (concorrente assina) | Falha no Harry "só você diz"; reescreve com cena/mecanismo proprietário |
| Narrou o fluxo ("agora vou auditar") | Não narra: executa em silêncio e entrega só as headlines limpas, sem a tabela do gate |
| Headline que só quem já é de dentro entende | Falha na Clareza (Lei 1): reescreve criando o contexto e troca a palavra difícil pela simples |
| Figura de linguagem vazia ("mensagem cheia") | Curto nunca acima de claro: reescreve concreto, como uma pessoa real diria ("muitas mensagens pra responder e zero contratos") |
| Imprimiu a tabela do gate na saída | O gate é INTERNO (auditoria silenciosa); a saída é só template + gatilhos + as headlines limpas |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `references/templates.md`: banco de 30 templates por gatilho. **Central nos Passos 2-3** (escolhe os que encaixam, 2-3 headlines por template). Adapta ao nicho, nunca copia a frase pronta.
- `references/criterios-v2.md`: o detalhamento do gate do Passo 4 (rastreabilidade física dos 7 gatilhos + exemplos passa/falha por nicho + comprimento por 8 formatos). É o mesmo gate, com mais exemplo, não um segundo sistema.
- `references/comandos-rapidos.md`: lógica de volume (50/100/200/300) e protocolo de lotes do "banco de [tema]".
- `references/modo-input-livre.md`: decodar um viral de outro nicho pra modelar.
- `references/amplificadores.md`: as frases curtas que precedem a headline no reel falado/story.
- `references/dispositivos-de-frase.md`: o repertório de tempero (preparação+virada, âncora do cotidiano, dizer o não-dito, evocação sensorial, antítese) que realça a headline na revisão, depois da ideia de pé. **Dirigido no Passo 3.**
- `scripts/lint_copy.py`: no Claude Code, roda `python3 scripts/lint_copy.py` na headline como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual do gate.
