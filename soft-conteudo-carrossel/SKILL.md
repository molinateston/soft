---
name: soft-conteudo-carrossel
description: Escreve o CORPO de um carrossel de feed do método Soft, da capa ao CTA, a peça que mais converte no feed. Parte da headline já escolhida, abre o loop, conduz pela Fórmula 7 (arco ADMA) em 7 a 10 slides com uma tese por slide, e passa o carrossel inteiro pelo gate (densidade + as 3 perguntas do gate + C/U/B + CTA + anti-IA) antes de mostrar. Use quando o pedido for "carrossel", "post de feed", "slides do carrossel", "corpo do carrossel", "escreve um carrossel", "monta um carrossel". NÃO use pra HEADLINE/gancho/capa/abertura isolada (soft-conteudo-headlines), nem pra arte/PNG/visual/design dos slides (soft-designer), nem pra reel (soft-conteudo-reels), stories (soft-conteudo-stories) ou multiplataforma (soft-conteudo-multiplataforma), nem pro Plano/posicionamento (soft-posicionamento), nem pra carta/VSL/venda (soft-funil-carta/-landing).
---

# Carrossel, a peça que move a decisão

Reel atrai, carrossel vende. Quem desliza o primeiro slide já decidiu que vai aprofundar. O carrossel não fecha a venda (isso é a carta e o WhatsApp). Ele instala a crença que faz o leitor chegar na carta já tendo comprado a ideia. A peça não convence, ela reorganiza a percepção: o leitor chega sozinho na conclusão e a venda vira consequência. Carrossel que vira mini-aula falhou, o leitor já tem informação demais.

**O que esta skill faz por você:** pega a headline escolhida e monta o carrossel que instala a crença e move a decisão (reel atrai, carrossel vende). É o passo que esquenta o leitor antes da carta.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa o contexto de você antes de gerar; (4) contexto é rei: a estrutura abaixo é guia, não trilho (ver Passo 2); (5) **admite se faltar insumo, nunca inventa**: confere se tem a fala/o número/o case antes de montar e, se faltar, marca `[DADO: confirmar]` no lugar do furo e diz o que falta, jamais preenche com algo plausível; (6) **doc de output enxuto pros 2 leitores**: o que sai é otimizado pro humano que lê E pra IA que recebe como contexto: só o carrossel limpo + `[DADO: confirmar]`, zero meta-narração. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar o carrossel.**

## Output Contract (o que você entrega)
- **A capa + 7 a 10 slides na Fórmula 7**, copy slide a slide, uma ideia por slide, na voz do cliente final do especialista.
- **O mapa de densidade** (a tese de cada slide em 1 frase). O gate roda **por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída. Nada do gate entra no doc: nem a tabela, nem veredito, nem "nota de gate", nem auto-avaliação em prosa. A ÚNICA marca permitida dentro do doc é `[DADO: confirmar]` no lugar de um furo.
- Você entrega **um carrossel por vez** e **para** pra ajuste antes de gerar outro ou passar pro design.
- Você **nunca inventa fala nem número do cliente** e **nunca mostra um carrossel que falhou no gate**.
- A copy sai daqui. **A arte/PNG e a embalagem visual da capa são da `soft-designer`**, você define a tese e o texto e aciona ela.


## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a peça no chat)
Regra dura, vale mesmo pra copy curta: o RESULTADO desta skill sai como **UM documento markdown consolidado**. No **claude.ai**, um **artifact de markdown** (o dono abre, copia, baixa); no **Claude Code**, um arquivo `.md`; no **agente/Telegram**, gera o doc como arquivo `.md` e cita o path completo na resposta (o bridge anexa), com a condução em mensagens curtas sem markdown pesado (sem `##`, sem tabela). A CONDUÇÃO (perguntas de contexto, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA/COPY em si mora no DOC. Ao parar num STOP, você mostra ou atualiza o DOC e pergunta "ajusto?"; você NUNCA reescreve a peça em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Passo 0, exige a headline e ancora (NÃO PULE)
O fluxo assume que a **headline/capa já foi escolhida** (veio da `soft-conteudo-headlines`). **Regra dura, vem antes de tudo:** se não tiver headline definida, **não comece o corpo** em hipótese nenhuma. Manda fazer a capa na `soft-conteudo-headlines` primeiro e para. A capa é 90% do jogo, o corpo se constrói a partir dela. (Os três estados de entrada abaixo só valem DEPOIS que a headline existe, eles tratam da fonte de fala, não da headline.)

Com a headline na mão, procura a fonte de fala real do cliente, nesta ordem: **descrição do projeto** → **Plano colado na conversa** → **mensagens anteriores**. Puxa **3-5 falas de DOR + 3-5 de DESEJO** do tema, literais, contando o N (quantas vezes apareceu). O diagnóstico e a prova do carrossel nascem dessas falas, quase intactas.

Três estados de entrada (já com a headline na mão, declara qual é o seu antes de escrever):
- **Tem fala real (com N):** ancora nela e cita o N. Caminho ideal.
- **Tem nicho/fundação mas ZERO fala literal:** NÃO inventa fala nem N. O diagnóstico ancora em **prova real do autor** (resultado, case, mecanismo); qualquer número que você não confirmou entra como `[DADO: confirmar]` e **NÃO conta como Ancorado=✓**. Avisa: minerar 5-8 falas reais deixa o carrossel muito mais cravado.
- **Sem nenhuma fonte de fala:** pergunta numa única mensagem (nicho em 1 linha + 1 dor real que o cliente fala) e segue daí.

A fundação (quando existe, do Plano): tese central · top 3 inimigos nominais · mecanismo nomeado · lista do "não defendo" · cliente em uma frase. A base não se inventa aqui, vem do Plano. Sem ela, a peça vira jornalismo que atrai estranho.

**Os padrões de ausência da voz (puxa ANTES de escrever, é o que impede o carrossel de soar genérico).** Uma voz se reconhece tanto pelo que ela faz quanto pelo que ela NUNCA faz. Se existe skill de voz destilada do cliente (ex.: `soft-voz-leo-molina`), abre ela e extrai, numa lista curta de **5-8 itens**, as coisas que aquela voz jamais faz: palavras que ele não usa, muletas que ele evita, estruturas de frase que soam falsas na boca dele, o tom que ele nunca adota (ex.: "nunca usa 'jornada', 'destravar' nem 'mindset'; nunca abre com pergunta retórica; nunca termina com emoji; nunca fala em 1ª pessoa do plural corporativo; nunca promete sem número"). Anota essa lista de ausência agora, no Passo 0, e carrega ela até o gate (Passo 4): cada slide é conferido contra ela, e um item da lista violado reprova igual a um travessão. Se **não existe** skill de voz do cliente, você não inventa a lista: escreve na voz neutra do cliente final e marca no doc que a voz específica ainda não foi destilada (a peça fica mais cravada quando ela existe). A lista de ausência é POR CLIENTE, nunca uma lista genérica sua, e nunca vira exemplo dentro do carrossel.

## Passo 0.5, enriquecimento factual (só quando o tema pede prova, NÃO é storytelling puro)
Casa direto com a Lei 5 (nunca inventa): o carrossel que afirma resultado, cita "estudo", compara mercado × método ou promete número precisa de **matéria-prima verificada**, não de um dado plausível que a IA chuta. Antes de montar o mapa (Passo 1), decide: **este tema apoia a tese num fato/número/case?** Se é puro storytelling ou opinião do autor, **pula este passo**. Se apoia, minera **1 insumo real** de uma destas quatro fontes, nesta ordem de preferência:
- **Um dado/número do próprio autor** (resultado dele, do aluno, do case). É o mais forte, tem CPF e ninguém contesta.
- **Uma visão contrária ou fato surpreendente** do nicho que sustenta o ângulo da capa.
- **Um estudo de caso real** (nome + contexto + número + prazo) que vira a prova do slide de Mecanismo.
- **Uma crença equivocada comum** do mercado, pra o Diagnóstico contestar com o fato.

Regra dura: o insumo tem que ser **verificado**, não inventado. Fato que você não confirmou entra como `[DADO: confirmar]` no lugar do furo e **não conta como Ancorado=✓** no gate. Número de terceiro nunca vira fato do método (segue a Lei 5). Um insumo verificado basta pra dar corpo ao carrossel; não transforma a peça numa mini-aula (Lei do "dá o tijolo, não a planta").

**Ramo por ambiente (onde a mineração acontece muda o que você entrega):**
- **App / chat (claude.ai, sem Bash):** você não roda pesquisa nem script. Puxa o insumo do que já está na conversa (Plano, descrição do projeto, falas coladas) ou **pergunta ao dono** em 1 mensagem ("tem 1 número/case real desse tema? senão marco `[DADO: confirmar]`"). Nada de dado da web sem fonte na mão.
- **Claude Code (tem Bash/pesquisa):** pode rodar a pesquisa real (busca, leitura de fonte) pra levantar o dado/contraponto/case, sempre guardando de onde veio; o que não fechar vira `[DADO: confirmar]`.
- **Agente / Telegram (tem Bash):** minera pela infra disponível, mas a entrega final é o **arquivo do carrossel** (o path completo do `.md` vai na resposta) e as mensagens no chat vão **sem markdown pesado**; qualquer dado não confirmado fica marcado `[DADO: confirmar]` no arquivo.

O insumo verificado alimenta o Diagnóstico e o slide de prova/Mecanismo do Passo 2. Sem tema-que-pede-prova, ignora tudo isto e vai pro Passo 1.

## Passo 1, declara a camada e monta o mapa de densidade (ANTES de escrever frase)
**Primeiro a camada (atração é funil, não bloco).** Decide a que camada este carrossel serve: muda a capa e o nível de filtro:
- **C1 Alcance:** capa que o leigo entende em 1s, não filtra; o técnico densifica nos cards 4-7. Volume (3-5/sem).
- **C2 Convicção:** capa que FILTRA (o cliente certo para, o resto passa); abre lacuna que só fecha no método. É o carrossel que mais vende (2-4/sem).
- **C3 Prova viva:** capa sobre o ALUNO transformado (nome + contexto + número + prazo); você é o mediador, não o herói (1-2/sem).

Declara a camada em 1 linha no topo do mapa. Detalhe + a **regra do "fragmento do produto"** (cada módulo do método vira 3-5 carrosséis C2 que abrem lacuna que só fecha no produto) em `references/camadas-conciencia.md`.

**Depois o mapa de densidade.** Densidade vence comprimento. Antes de redigir, lista **a tese de cada slide em 1 frase**, da capa ao CTA. Regra dura: **carrossel de ~10 slides exige ≥6 teses DISTINTAS.** Duas teses iguais com roupa nova se fundem (corta um slide). Cada slide AVANÇA a espinha, nunca repete o anterior com outras palavras.

Esse mapa é o esqueleto que o gate vai conferir. Se não fecha 6 teses distintas, o tema não tem corpo pra carrossel: ou aprofunda o ângulo, ou vira reel.

## Passo 2, distribui pela Fórmula 7 (arco ADMA, alta polaridade)
A Fórmula 7 são **7 movimentos** distribuídos nos **7 a 10 slides**. Movimento não é slide: alguns ocupam um card, outros se esticam por dois. A espinha é o arco ADMA (Atenção · Diagnóstico · Mecanismo · Ação). Começa em **alta polaridade** (a capa já confronta uma crença real do mercado) e termina instalando a crença nova. Sem tensão não há movimento, sem crença nova não há ação.

| # | Movimento | Slide | Função |
|---|---|---|---|
| 1 | **Hook** | 1 (a capa escolhida) | Confronta o status quo. Alta polaridade. Para o scroll. |
| 2 | **Quebra de Crença** | 2 | **Abre o loop**, vai MAIS FUNDO que a capa ("tem uma coisa pior"). Nunca responde nem reembala a capa. |
| 3 | **Diagnóstico** | 3 e 4 | Nomeia o problema com a cena que o leitor vive. Ele se reconhece. |
| 4 | **Vilão** | 5 | Nomeia o inimigo (o sistema/a prática), nunca o leitor. Tira a culpa dele. |
| 5 | **Nova Oportunidade** | 6 | Mostra que existe um caminho diferente. A virada. |
| 6 | **Mecanismo** | 7 e 8 | O método como veículo. Mostra a **FUNÇÃO**, nunca o passo a passo executável. |
| 7 | **Convite** | 9 e 10 | Caso/prova concreta + CTA que convida, não empurra. |

Os dois pontos onde o carrossel morre:
- **Slide 2 que responde a capa.** Não responde. O slide 2 aprofunda o loop, é onde a maioria mata a peça reembalando a capa com sinônimo. Vai mais fundo.
- **Slides 7-8 que ensinam o passo a passo.** Mostra a função (o que o método faz, que resultado entrega, por que muda o jogo), nunca o procedimento executável. O leitor sai sabendo que existe um caminho e quem o domina, não sabendo andar nele sozinho.

Menos de 7 slides não desenvolve a tensão. Mais de 10 cansa e derruba o CTA.

**Contexto é rei (a estrutura flutua).** A Fórmula 7 é o guia, não um trilho rígido. O assunto manda: um carrossel pode pesar mais no Mecanismo (2-3 slides só pra ele) e enxugar o Diagnóstico; outro pode ser quase inteiro sobre o Problema, quando a dor ainda não doeu o suficiente; outro corta a Nova Oportunidade porque a virada já está na capa. Mantém os 7 a 10 slides e o arco ADMA de pé, mas distribui o peso pelo que ESTE assunto pede. Decide o peso no mapa de densidade (Passo 1) e justifica em 1 linha.

## Passo 3, escreve slide a slide (na voz do cliente)
Escreve cada slide, **uma ideia por slide**, muito espaço, cada slide fechando numa frase-conclusão ancorada (nunca um slide que só prepara o próximo). Estilo Soft: uma ideia por frase, número no lugar de adjetivo, vocabulário do cliente final (nunca "lead/funil/ticket"), toma lado, nunca morno. Trabalha dor e desejo (o estado preso × o estado solto) e, quando der, ancora o contraste num número.

**Repertório tático por papel (puxa de `references/estrutura-peca.md`).** O arco da Fórmula 7 dá a ordem; a `estrutura-peca` dá as FORMAS de aterrar cada papel: escolhe **1 por papel**, nunca despeja todas:
- **Contexto (slide 3):** 1 das 7 formas: Cena Filmada · Dia Padrão · Conselho Falido · Número Próprio · Diálogo Interno · Paradoxo Observável · Contraste com Personagem. Nunca preâmbulo didático ("antes de entrar no método...") nem currículo.
- **Conteúdo (slides 7-8):** 1 das 7 formas: Contraste Emparelhado · Reframe · Casos Empilhados · Linha do Tempo Numérica · Nome-Número-Condição · Bastidor Crítico · Declaração+Sustentação. Sempre em contraste mercado×método.
- **CTA (slide final):** 1 das 7 formas: Direct com palavra-senha · Comentário · Siga com razão · Batida Emocional · Filtro Duro · Convite Específico · P.S. Ticket R$3k+ pede Filtro Duro. **Casa o rótulo com a execução:** "Envia X no Direct" É a forma **Direct com palavra-senha**; "Comenta X que eu te mando" É a forma **Comentário** (não troque o nome da forma que você declarou; ver `references/estrutura-peca.md` Seção 3, formas 1 e 2).

**As 21 formas em 1 linha (pra saber o que É cada uma sem abrir a ref; detalhe, templates e tabelas de decisão em `references/estrutura-peca.md`):**

| Papel | Forma | O que é |
|---|---|---|
| Contexto | Cena Filmada | Um instante sensorial no presente: o leitor se vê na cena antes do argumento. |
| Contexto | Dia Padrão | A rotina em 4-5 beats (seg/ter/sex/dom): mostra o padrão, não um evento. |
| Contexto | Conselho Falido | A frase exata que o mercado repete, entre aspas, seguida do resultado que a contradiz. |
| Contexto | Número Próprio | Um dado com CPF do especialista/caso dele, nunca média. |
| Contexto | Diálogo Interno | A frase que o leitor fala pra si mesmo, na voz mental dele. |
| Contexto | Paradoxo Observável | Fato aceito + fato observável que o contradiz + conclusão seca. |
| Contexto | Contraste com Personagem | Dois casos iguais em tudo, divergentes num fator: um deu certo, o outro não. |
| Conteúdo | Contraste Emparelhado | Mercado x método lado a lado, formato binário fechado num bordão. |
| Conteúdo | Reframe | "Não é X, é Y": o leitor tentava resolver o problema errado. |
| Conteúdo | Casos Empilhados | 3+ mini-casos com condição inusitada cada, que viram padrão, não anedota. |
| Conteúdo | Linha do Tempo Numérica | Evolução só em números, sem adjetivo, nomeando o ponto de virada. |
| Conteúdo | Nome-Número-Condição (NNC) | Cada linha é um micro-caso denso (nome + número + condição), 5-10 em sequência. |
| Conteúdo | Bastidor Crítico | Um momento de execução que mostra o mecanismo funcionando, sem a receita reprodutível. |
| Conteúdo | Declaração + Sustentação | Declaração forte e curta + 2-4 blocos de sustentação (cena, número, caso). |
| CTA | Direct com palavra-senha | Razão concreta + envia uma PALAVRA no Direct (padrão Soft). |
| CTA | Comentário | Razão + comenta uma PALAVRA que eu te mando. |
| CTA | Siga com razão | Tipo de conteúdo recorrente + segue pra continuar recebendo. |
| CTA | Batida Emocional | Você decide: continuar o conselho falido OU o que o método propõe + CTA direto. |
| CTA | Filtro Duro | Não é pra quem X, não é pra quem Y, é pra quem Z + CTA (ticket alto). |
| CTA | Convite Específico | Evento/conteúdo nomeado + data/formato + pra quem + ação de inscrição. |
| CTA | P.S. que vira CTA | CTA principal suave + P.S. com informação específica + ação com palavra-senha. |

**Faca Soft (teste antes de fechar cada slide de método):** *"se eu publicar isso, aumenta ou diminui o motivo de comprar o produto?"* Aumenta → fica. Diminui → corta. Dá o tijolo, nunca a planta da casa. (O exemplo card-a-card completo está em `references/06-carrossel.md` 6.7; modela, não copia.)

**Tempero, só na revisão (`references/dispositivos-de-frase.md`).** Com a estrutura de pé, pergunta "tá chapado?" e injeta 1-2 dispositivos (preparação+virada, antítese, evocação sensorial, dizer o não-dito) onde a peça está morna, nunca os 6 de uma vez, nunca no lugar da estrutura.

A **capa abre largo** (palavra do imaginário coletivo, pra não expulsar) e o corpo **nicha do meio pro fim** (onde aprofunda e filtra). O slide do CTA é **obrigatório e muito bem feito** (é o que vira o carrossel em mensagem no direct): de preferência uma **palavra-chave pra comentar** que entrega algo concreto, com os bullets do que a pessoa recebe. Ex.: comenta TRÁFEGO que eu te mando (1) o modelo de anúncio, (2) o passo do atendimento, (3) o painel. Liga a palavra-chave ao próximo passo real do funil (direct → carta/isca). Nunca termina só na consequência. Nunca CTA cafona. **Não narra o fluxo** ("agora vou o slide 5"), só entrega a copy limpa.

> Se existe skill de voz destilada do cliente (ex.: `soft-voz-leo-molina`), ela é a fonte do tom: pilares, bordões e anti-valores. Você já leu ela no Passo 0 pra tirar os **padrões de ausência**; aqui usa o lado positivo (pilares, bordões, ritmo) pra escrever COMO ele fala, enquanto a lista de ausência guarda o que ele nunca faz.

## Exemplo card-a-card (modela a QUALIDADE, nunca copia; nicho fictício)
Tema "Por que sua reunião gratuita não converte", 8 cards (o Diagnóstico ocupou 2). Repara: nenhum card ensina a executar, todos mostram função, cena ou prova.
1. **Capa (Hook):** "Sua reunião gratuita não converte porque ela treina o cliente a pedir mais sem pagar." (manifesto que polariza · frase firme)
2. **Quebra de Crença:** "Mas tem uma coisa pior. Você não tá só perdendo cliente, tá ensinando ele que teu trabalho não vale." (NÃO responde a capa, aprofunda o loop)
3. **Diagnóstico, a cena:** "Call de 1h 'sem compromisso'. Ouve o cliente 40 min. Proposta nos últimos 20. Ele diz 'vou pensar'. 3 dias depois fecha com o concorrente que cobrou metade. Por quê?" (a cena que ele vive, fecha em pergunta)
4. **Diagnóstico, a virada:** "Porque você deu de graça o que o concorrente cobrou. Diagnóstico grátis não vira valor percebido, vira acessibilidade. Acessibilidade barateia." (reframe)
5. **Vilão:** "Não é o que você fala. É como o cliente percebe teu tempo. Tempo grátis = commodity. Tempo cobrado = autoridade." (aponta o mecanismo, tira a culpa do leitor)
6. **Nova Oportunidade:** "No [método do cliente] a venda acontece antes da conversa. O cliente lê a carta, entende, chega decidido. A reunião vira confirmação." (o método como contraste; função, não execução)
7. **Mecanismo/Prova:** "Marina, advogada, implementou há 14 dias. Primeiro cliente R$8.500 sem reunião. Segundo, R$5.500. Sem call grátis, sem 'vou pensar'." (prova ancorada: nome + nicho + número + prazo)
8. **Convite/CTA:** "Se bateu, o caminho é [a oferta]: 3 sessões, sistema em 60 dias. Comenta MÉTODO que te mando a carta pra ler antes." (pede comentário, entrega valor antes, CTA único)

## COMO ENTREGAR (o carrossel vira doc MD)
O carrossel montado (capa + slides na ordem, uma ideia por slide) é o entregável, e o cliente quer guardar. Entrega como **documento markdown**: no **claude.ai** como **artifact de markdown** (o carrossel slide a slide, que ele abre, copia e manda pro designer), no **Claude Code** como arquivo `.md`, no **agente/Telegram** como arquivo `.md` cujo path completo vai citado na resposta (vira anexo), com a condução em mensagens curtas sem markdown pesado. A condução (mapa de densidade, escolha das formas, gate por dentro) acontece no chat; o **carrossel final sai como doc**, slide a slide rotulado, nunca despejado solto no meio da conversa.

**Formato do rótulo de slide (obrigatório, decalca o do exemplo card-a-card acima):** cada slide sai como `N. **Papel:** copy`, ou seja, número do slide + ponto + o papel em negrito + dois-pontos + a copy. Ex.: `7. **Mecanismo/Prova:** "..."`. **É PROIBIDO usar o travessão (em-dash) como separador de rótulo** (nada de "Slide 7" seguido de travessão e o papel): o em-dash é o char que a própria skill bane no gate e reprova a peça inteira no `lint_copy.py`. Sem número disponível, usa só `**Papel:** copy`. O separador é sempre dois-pontos, nunca em-dash.

## Passo 4, roda o GATE por dentro (auditoria silenciosa, NÃO imprime)
Roda o gate no carrossel inteiro **internamente** (auditoria silenciosa). Só carrossel com a linha VEREDITO=PASSA vai pro cliente. Uma falha refaz o ponto (não a peça inteira). A tabela abaixo é o teu **checklist interno**, nunca a saída: o usuário recebe só o carrossel limpo (Passo 5), jamais a tabela.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorado** | diagnóstico/prova nascem de fala literal da fonte (cita N **real**) OU de prova real do autor; **N inventado/plausível = ✗ automático**; aspas só pra substring literal da fonte | |
| **Densidade** | o mapa do Passo 1 fecha **≥6 teses DISTINTAS** em ~10 slides; duas teses iguais com roupa nova = ✗ (funde e corta) | |
| **Slide 2 abre loop** | o slide 2 vai MAIS FUNDO que a capa ("tem uma coisa pior"); **não responde nem reembala a capa = ✗** | |
| **Mecanismo = função** | slides 7-8 mostram a FUNÇÃO do método; **qualquer passo a passo executável = ✗** | |
| **Espinha Fórmula 7 / ADMA** | os 7 movimentos estão na ordem; começa em alta polaridade; cada slide fecha numa conclusão ancorada (nenhum só prepara o próximo) | |
| **Confuso (C)** | dá pra ler cada slide sem reler; uma ideia por slide; zero abstração que não vira imagem | |
| **Inacreditável (U)** | nenhuma promessa que o leitor não engole; prova ancorada onde afirma resultado | |
| **Chato (B)** | nenhum slide morno/educativo neutro; polariza, mexe na crença ou na cena, não só informa | |
| **Dá pra ver?** | o diagnóstico fecha o olho e vira cena. ✗ "tenha mais clareza" · ✓ "a call de 1h vira 40 min de desabafo e um 'vou pensar'" | |
| **Dá pra falsificar?** | as afirmações são fatos falsificáveis, não adjetivos | |
| **Só você diz?** | o concorrente direto não assina igual (cena/mecanismo proprietário, não promessa banal do nicho) | |
| **CTA forte com palavra-chave** | slide final tem CTA único e muito bem feito: palavra-chave pra comentar + o que a pessoa recebe (bullets/benefício) + próximo passo real do funil (direct/carta/isca); CTA fraco ou **sem destino = ✗** | |
| **Aponta pro método** | a peça aponta pro método ou faz seeding da tese; **jornalismo neutro ("5 fatos sobre X") = ✗** | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, destrava, transforma") · sem tricolon nem contraste "não é X, é Y" repetido. **No chat (sem o lint), faz um CTRL+F manual de "—" e da família "travar" em TODOS os slides antes de marcar ✓.** O em-dash "—" é ✗ em QUALQUER lugar do `.md`, não só nas frases de copy: rótulos de slide, cabeçalhos, marcadores `[DADO: confirmar]` e notas TAMBÉM são texto do doc e contam; um "—" em qualquer um deles reprova a peça igual ao `lint_copy.py` (exit 1). | |
| **Voz do cliente (padrões de ausência)** | quando a lista de ausência do Passo 0 existe: **nenhum slide viola nenhum item dela** (palavra proibida, muleta, estrutura, tom que aquela voz nunca usa); um item da lista quebrado = ✗ igual a um travessão. Sem lista destilada, marca N/A e segue. | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

## Passo 5, mostra e PARA
Mostra **só o carrossel LIMPO** (no DOC, nunca solto no chat), slide a slide no formato `N. **Papel:** copy`: a copy de cada slide, sem tabela de gate, sem meta. **É PROIBIDO** colar dentro do doc qualquer traço do gate. Não só a tabela, mas TAMBÉM qualquer nota/prosa de gate, veredito, "nota de gate (interna)", auto-avaliação ou "fiz o CTRL+F". Entregar o gate em prosa viola a Lei 6 igual à tabela; o gate mora só na tua cabeça (Passo 4), nunca no doc. A única marca permitida no doc é `[DADO: confirmar]` no lugar do furo. Pergunta "esse carrossel te serve? ajusto algum slide ou parto pro design?". **Espera a escolha** antes de gerar outro carrossel ou acionar a `soft-designer` pra arte.

## When NOT to use (manda pra skill certa)
- Pediu **headline / capa / gancho / abertura** isolada → **soft-conteudo-headlines**.
- Pediu **arte / visual / PNG / design dos slides** → **soft-designer**.
- Pediu **reel** → **soft-conteudo-reels** · **stories** → **soft-conteudo-stories** · **adaptação multiplataforma** → **soft-conteudo-multiplataforma**.
- Pediu **Plano / posicionamento / fundação / mecanismo** → **soft-posicionamento**.
- Pediu **carta / VSL / página / a venda em si** → **soft-funil-carta / soft-funil-landing**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Começou o corpo sem headline definida | Para: manda escolher a capa na `soft-conteudo-headlines` primeiro |
| Slide 2 reembala a capa com sinônimo | Reescreve aprofundando o loop ("tem uma coisa pior"/paradoxo), nunca responde a capa |
| 10 slides mas 3 teses repetidas | Funde as iguais e corta slide; carrossel é densidade, não comprimento |
| Mecanismo virou tutorial executável | Mostra resultado e função do método, esconde o procedimento |
| Slide que só prepara o próximo | Cada slide fecha numa frase-conclusão ancorada |
| Carrossel jornalístico ("5 fatos sobre X") | Costura o final apontando pro método ou faz seeding da tese |
| Terminou sem CTA ou com CTA cafona | Slide final: CTA único, firme, palavra-chave + próximo passo real do funil |
| Inventou um número/fala "plausível" | Só número/fala REAL; sem fonte, marca `[DADO: confirmar]` e não conta como Ancorado=✓ |
| Despejou a peça inteira sem mapa nem gate | Volta: mapa de densidade + gate impressos, e PARA pra escolha |
| Narrou o fluxo ("agora o slide 5") | Não narra: produz a copy em silêncio e entrega só o carrossel limpo, sem as tabelas do gate |
| Engessou a Fórmula 7 ignorando o assunto | Contexto é rei (Lei 4): redistribui o peso, mais no problema OU no mecanismo, mantendo o arco ADMA e os 7-10 slides |
| Imprimiu a tabela do gate na saída | O gate é INTERNO (auditoria silenciosa); a saída é só a peça limpa |
| Escreveu na voz certa mas usou palavra/muleta que aquele cliente nunca usa | Puxa a lista de ausência da voz no Passo 0 e confere cada slide contra ela no gate; item violado reprova |
| Afirmou resultado/estudo/número com dado "plausível" que ninguém verificou | Passo 0.5: minera 1 insumo REAL (do autor/case/fonte) ou marca `[DADO: confirmar]`; nunca chuta número |
| Virou mini-aula ao empilhar todo dado pesquisado | 1 insumo verificado basta; dá o tijolo, não a planta (Faca Soft) |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `references/06-carrossel.md`: a engenharia completa do carrossel (Alta Polaridade, a Fórmula 7 nos 10 slides, Embalagem A+B da capa, exemplo card a card, métricas e diagnóstico por sintoma). É a fonte da verdade do formato.
- `references/conducao-na-pratica.md`: os reframes da condução (palatável não raso, cada peça é um cheque, estourar a bolha, polarizar, dar o ouro). O porquê e o como por trás da peça.
- `references/modo-construcao.md`: o loop de escrever-e-auto-criticar (ancoragem antes da pele, gera 7 ângulos e descarta os 2 óbvios, teste de densidade, auto-gate). É o mesmo gate do Passo 4, com mais detalhe.
- `references/camadas-conciencia.md`: as 3 camadas de atração (C1 Alcance · C2 Convicção · C3 Prova viva), o critério de capa por camada e a regra do "fragmento do produto". **Dirigida no Passo 1.**
- `references/estrutura-peca.md`: a Estrutura-Mãe dos 5 papéis com as 21 formas nomeadas (7 de Contexto + 7 de Conteúdo + 7 de CTA), tabelas de decisão por papel, a Faca Soft e os anti-padrões de cada papel. **Dirigida no Passo 3.**
- `references/dispositivos-de-frase.md`: o repertório de tempero (preparação+virada, âncora do cotidiano, dizer o não-dito, evocação sensorial, antítese) que entra na revisão, depois da estrutura de pé. **Dirigida no Passo 3.**
- `scripts/lint_copy.py`: no Claude Code, roda `python3 scripts/lint_copy.py` no carrossel como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual do gate.
