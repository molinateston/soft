---
name: soft-conteudo-reels
description: Escreve o ROTEIRO de um reel do método Soft, o vídeo curto lo-fi que para o scroll e atrai o cliente certo. Parte da headline já escolhida, constrói o corpo pela espinha ADMA comprimida em 1 a 2 minutos, escreve nos 3 tipos quando útil (falar, mostrar, texto na tela), e passa o roteiro pelo gate (verbatim real + as 3 perguntas do gate + C/U/B + tensão que não relaxa + CTA com destino + anti-IA) antes de mostrar. Use quando o pedido for "reel", "roteiro de reel", "vídeo curto", "vídeo lo-fi", "reels", "script de vídeo", "o que falar no vídeo". NÃO use pra HEADLINE/gancho/capa/abertura isolada (soft-conteudo-headlines, faz a headline primeiro), nem pro carrossel (soft-conteudo-carrossel), stories (soft-conteudo-stories) ou adaptação multiplataforma (soft-conteudo-multiplataforma), nem pro Plano/posicionamento (soft-plano-posicionamento), arte/PNG/visual (soft-designer), ou carta/VSL/venda (soft-funil-carta).
---

# Reel, o vídeo curto que atrai

Reel atrai. Carrossel vende. A função do reel é uma só: fazer o cliente certo parar de rolar e te enxergar diferente. Ele não fecha venda (isso é na carta e no WhatsApp), não entrega passo a passo, não vira aula. Reel é story: peça diária, leve, gravada em minutos. Volume é o que faz o método rodar, e produção cara mata volume. O que performa é o gancho e a ideia, nunca a câmera.

**O que esta skill faz por você:** transforma a headline escolhida no roteiro do reel que para o scroll e atrai o cliente certo (reel atrai, carrossel vende). O roteiro é o que importa; a câmera, não.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa o contexto de você antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: confere se tem a fala/o número/o case antes de montar e, se faltar, marca `[DADO: confirmar]` no lugar do furo e diz o que falta, jamais preenche com algo plausível; (6) **doc de output enxuto pros 2 leitores**: o que sai é otimizado pro humano que lê E pra IA que recebe como contexto: só o roteiro limpo + `[DADO: confirmar]`, zero meta-narração. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar qualquer roteiro.**

## Output Contract (o que você entrega)
- Por padrão, **1 roteiro de reel completo** pro pedido: headline nos 3 primeiros segundos (nos 3 tipos quando útil) + corpo pela espinha ADMA + CTA com destino real. Escrito como fala/cena, não como ensaio literário.
- O gate roda **por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída. O roteiro vem com a marcação da espinha (qual frase é qual movimento).
- Você **para e espera** o cliente aprovar/ajustar antes de gerar outro ou escalar pra lote.
- Lote (5 reels numa tarde, banco de pautas) só sob comando explícito "lote de [tema]".
- Você **nunca inventa fala nem número do cliente** e **nunca mostra roteiro que falhou no gate**.


## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a peça no chat)
Regra dura, vale mesmo pra copy curta: o RESULTADO desta skill sai como **UM documento markdown consolidado**. No **claude.ai**, um **artifact de markdown** (o dono abre, copia, baixa); no **Claude Code**, um arquivo `.md`. No **agente/Telegram**, gera o doc como arquivo e cita o **caminho completo** na resposta (ex.: `/home/cloud/reels/reel-x.md`), que vira anexo; a condução fica em mensagens curtas, sem markdown pesado (sem `##`, sem tabela). A CONDUÇÃO (perguntas de contexto, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA/COPY em si mora no DOC. Ao parar num STOP, você mostra ou atualiza o DOC e pergunta "ajusto?"; você NUNCA reescreve a peça em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Passo 0, parte da headline e ancora (NÃO PULE)
O reel começa de uma **headline já escolhida**. Se o usuário ainda não tem a headline (a frase que para o scroll nos 3 primeiros segundos), você **não escreve o corpo**: manda fazer a headline antes na **soft-conteudo-headlines** e volta com ela. Corpo sem gancho é vídeo que ninguém assiste.

Com a headline na mão, procura a fonte de fala real do cliente, nesta ordem: **descrição do projeto** → **Plano colado na conversa** → **mensagens anteriores**. Puxa **3-5 falas de DOR + 3-5 de DESEJO** do tema, literais, contando o N (quantas vezes apareceu). O corpo do reel nasce dessas falas, na voz do cliente final, nunca no jargão de marketing.

Três estados de entrada (declara qual é o seu antes de escrever):
- **Tem fala real (com N):** ancora nela e cita o N. Caminho ideal.
- **Tem nicho/fundação mas ZERO fala literal:** NÃO inventa fala nem N. O roteiro ancora em **prova real do autor** (resultado, case, mecanismo); qualquer número que você não confirmou entra como `[DADO: confirmar]` e **NÃO conta como Ancorado=✓**. Avisa: minerar 5-8 falas reais (ou rodar o Plano na soft-plano-posicionamento) deixa o roteiro muito mais cravado.
- **Sem nicho e sem nada:** pergunta numa única mensagem (nicho em 1 linha + 1 dor real que o cliente fala + a headline) e segue daí.

A fundação (quando existe, do Plano): tese central · top 3 inimigos nominais · mecanismo nomeado · cliente em uma frase.

**Puxa os padrões de ausência da voz (o que essa voz NUNCA faz).** Se existir voz do cliente (na descrição do projeto, no Plano, ou numa skill de voz dele), tira de lá uma lista curta, de 5 a 8 itens, do que aquela voz NÃO faz: palavras que ele não usa, muletas que ele evita, estruturas que soam falsas na boca dele, o termo que ele detesta. Isso vira um **filtro extra** que roda junto do anti-IA no gate (Passo 5): antes de marcar ✓, confere que o roteiro não caiu em nenhum item da ausência. É o que faz o reel soar COMO ele, não só "não-IA". Se não houver voz mapeada, segue sem, e anota que definir a voz (na soft-plano-posicionamento) deixaria o roteiro mais fiel. Nunca inventa uma "ausência" que o cliente não declarou.

**Enriquecimento factual (mini-passo opcional, só quando o tema pede prova).** Se o ponto do reel se apoia em dado, contraponto ou caso (não é puro relato pessoal), minera ANTES de roteirizar: 1 dado/estatística que sustenta o ângulo, ou 1 crença comum do nicho pra contestar, ou 1 caso real. Puxa isso da fonte do cliente (Plano, prova real dele) ou de pesquisa quando for fato público verificável. Regra dura: o dado só entra se for REAL e verificável; número que você não confirmou vira `[DADO: confirmar]` e **não conta como Ancorado=✓**. Nunca fabrica estatística "plausível". Reel de puro storytelling pula esse passo.

## Passo 1, confirma o ÚNICO ponto do reel
O reel carrega **um insight, uma virada, uma frase**, nunca a tese inteira. Quem tenta cuspir tudo numa peça produz vídeo pesado que ninguém assiste. Define em uma linha qual pedaço do quebra-cabeça esta peça materializa, e o que ela reorganiza na cabeça do leitor. A peça não precisa estar completa: ela é uma pecinha que o mercado monta ao longo do tempo. Se o ponto não cabe numa frase, ainda está grande demais, corta antes de roteirizar.

**Declara a camada (atração é funil, não bloco):** C1 = reel curto com gancho que o leigo entende (alcance) · C2 = reel longo opinativo, técnica entremeada com opinião pessoal (convicção, ótimo pra dark post) · C3 = reel-visita ao cliente no contexto real dele (prova viva). A camada muda o gancho e o comprimento. (Detalhe em `references/camadas-conciencia.md`.)

## Passo 2, escreve o gancho nos 3 tipos (os 3 primeiros segundos)
A headline do Passo 0 entra nos 3 primeiros segundos, trabalhada em **até 3 frentes ao mesmo tempo**. Uma já segura. As três em conflito multiplicam (o texto contradiz a imagem, a fala abre o loop, a pessoa precisa descobrir o que vem). Escreve as que servirem ao reel:

| Tipo | O que é | Como aparece |
|---|---|---|
| **FALAR** | a frase dita na boca nos primeiros segundos | a headline falada, direta |
| **MOSTRAR** | a cena/imagem que prende: exagero, movimento, contraste | print circulado · objeto inesperado · antes/depois |
| **TEXTO NA TELA** | a frase sobreposta, grande, lida em silêncio | aparece enquanto a boca fala outra coisa relacionada |

Não força os três se um só já cria o conflito. Mas marca no roteiro qual entra em cada frente.

**Confirma qual dos 7 gatilhos a abertura aciona** (Recompensa · Mistério · Reconhecimento · Popularidade · Crença · Autoridade · Disrupção): toda abertura forte aciona ≥1. A headline já vem da `soft-conteudo-headlines` com o gatilho escolhido; aqui você confirma qual está ativo no corpo. **Disrupção exige defesa com argumento sólido logo depois**, senão vira clickbait e queima reputação. (Tabela dos 7 + os 3 tipos detalhados em `references/metodo-reel.md` 7.4.)

**Amplificador (opcional, 0-2s antes da headline falada):** uma frase curta que precede a headline e carrega 2s a mais de atenção (ex.: "Por que ninguém tá falando sobre isso?"). Os 10 canônicos + a afinidade por template em `references/amplificadores.md`. Um por peça, nunca se a headline já está cravada ou o tempo dos 3s estourou.

**Como aparecer no vídeo é só sugestão, nunca obrigação.** A pessoa grava do jeito dela; o que a skill garante e entrega é o ROTEIRO. Quando sugerir cena, gesto ou edição, deixa explícito que é opcional, um caminho possível, não uma regra.

## Passo 3, desenvolve pela espinha ADMA (comprimida em 1-2 min)
A mesma espinha do carrossel, comprimida no tempo do vídeo. Cada frase abre a próxima. **A tensão não relaxa.** Se o leitor consegue prever a próxima frase, ele pula. A tensão é o que segura, não a informação. Mostra o **diagnóstico**, nunca o passo a passo executável (passo a passo vira aula grátis e não vira venda).

| Trecho | Movimento | Função |
|---|---|---|
| **3s** | Atenção (Hook) | interrupção, a frase que para o scroll (a headline do Passo 2) |
| **Abertura** | Quebra de crença | conflito, mostra a tensão vivida, não resolve ainda |
| **Meio** | Diagnóstico + Vilão | nomeia a causa real, o culpado é o modelo velho, não o leitor |
| **Virada** | Nova oportunidade | a virada de interpretação, existe um caminho diferente |
| **Fechamento** | Mecanismo + Convite | aponta pro método (função, não execução) + CTA com destino |

Duração: 1 a 2 minutos, em torno de 1:30 quando for impulsionar. Polariza (toma lado, gancho que polariza exige corpo que sustenta). Carrega **moeda social** (≥2 de: valor prático, identificação, opinião forte, argumentação, notícia, história, prova, fato curioso). Sempre aponta pro método ou faz seeding da tese.

**Depois do gancho, o conteúdo precisa ser NOTÁVEL** (`references/metodo-reel.md` 7.5): (1) algo NOVO, um ângulo que quase ninguém falou (se a pessoa prevê a próxima frase, ela pula); (2) baixo carregamento cognitivo, explica como pra criança, termo técnico só com tradução fácil em seguida; (3) sem encher linguiça, curto não raso, zero introdução antes de entrar no conteúdo.

Os 6 roteiros-modelo (decisão contraintuitiva · erro que custou caro · bastidor · contraste de resultado · crença errada · caso real) estão em `references/roteiros-modelo.md`, profundidade opcional, clona e adapta, nunca copia cru.

**Roteiro-modelo inline (Bastidor Invisível, ~50s, nicho Consultoria de gestão), modela a qualidade, nunca copia.** Repara como cada marca de tempo carrega um movimento da espinha ADMA:
- **[0:00-0:03] GANCHO (Atenção).** Texto na tela: "O que acontece antes da reunião". Fala: "Eu cobro R$4.500 por consultoria. E 80% do trabalho acontece antes da primeira reunião."
- **[0:03-0:10] TENSÃO (quebra de crença).** "O cliente acha que o valor está na reunião. Não está." Abre o loop, não resolve.
- **[0:10-0:18] DIAGNÓSTICO (Diagnóstico + vilão).** "Antes de sentar com ele, eu já analisei o financeiro, os processos, as margens. Levo entre 6 e 8 horas nisso." O modelo velho (achar que o valor mora na hora do encontro) é o culpado, não o cliente.
- **[0:18-0:25] REVELAÇÃO (nova oportunidade).** "Quando começa a reunião, eu já sei o problema. Ele não." Existe um caminho diferente de enxergar o serviço.
- **[0:25-0:30] MECANISMO (função, não execução).** "A reunião é só a hora que eu mostro o que encontrei." Aponta pro método sem entregar o passo a passo.
- **[0:30-0:35] FRASE DE IMPACTO.** "O diagnóstico vale mais que a solução. Sem ele, qualquer conselho é chute."
- **[0:35-0:40] CTA (Ação, destino real).** "Me conta o que você faz que te dou uma ideia." (comentar = próximo passo do funil)
- **Edição (sugestão, não regra):** cortes secos entre as frases; se der, 2-3s de B-roll da análise na tela durante "analisei o financeiro". Grava do jeito que for possível, o roteiro é o que a skill garante.

**Repara: o modelo acima não tem NENHUM travessão nem abertura-muleta, de propósito.** O reflexo de LLM é escrever com `—` e com frase-emoldura; caça e troca ANTES de entregar (é o Checkpoint do Passo 5):
- Travessão: ✗ `O modelo velho — a dieta de restrição — te programou pra isso` → ✓ `O modelo velho, a dieta de restrição, te programou pra isso.`
- Frase-emoldura: ✗ `O que ninguém te contou: a dieta te programou` → ✓ abre direto no conteúdo, `A dieta te programou.`

## Passo 4, fecha com CTA de próximo passo real
O reel não fecha venda, mas aponta pra onde. O CTA convida, não empurra, e tem **destino concreto do funil**: salvar, comentar uma palavra, mandar pra alguém, ir pro carrossel que aprofunda, ir pra isca/carta. CTA sem destino é peça órfã, o leitor para e não tem pra onde ir. Escreve o CTA na voz do cliente, ligado ao ponto único do reel.

**O CTA vem IMEDIATAMENTE depois da virada de interpretação, nunca depois de um bloco neutro** (`anti-padroes.md §3`). Se o parágrafo colado antes do CTA não reposiciona a crença (é mecanismo, recap ou frase de impacto), o CTA vira mendigo de interação. Confere: a frase logo acima do CTA é a revelação/virada? Se a virada real ficou 15-20s atrás, separada por mecanismo, ou re-ancora a virada numa linha curta antes do CTA, ou move o CTA pra logo depois dela.

## Passo 5, roda o GATE por dentro (auditoria interna, NÃO imprime)
Roda o gate no roteiro **internamente** (auditoria silenciosa). Só roteiro com a linha VEREDITO=PASSA vai pro cliente. Um ✗ refaz o ponto que falhou (não o conceito inteiro). A tabela abaixo é o teu **checklist interno**, nunca a saída: o usuário recebe só o roteiro limpo (Passo 6), jamais a tabela.

**CHECKPOINT ANTI-IA (obrigatório, roda ANTES de escrever a linha VEREDITO, sem exceção):** o modelo do app NÃO tem o `lint_copy.py`, então esta varredura manual é o ÚNICO cinto; se pular, entrega peça com assinatura de IA e o follow-test REPROVA. Varra o roteiro inteiro, caractere-a-caractere:
1. **Travessão `—`:** achou 1 que seja = **VEREDITO=REFAZ**. Reescreve com vírgula, ponto ou parênteses. (✗ `O modelo velho — a dieta — te programou` → ✓ `O modelo velho, a dieta de restrição, te programou`.)
2. **Família `trav*`** (travar/travado/destravar/destrava): achou 1 fora de aspa literal do cliente = **VEREDITO=REFAZ**.
3. **Frase-emoldura** (`padroes-banidos.md §4`): abre o parágrafo com "O que ninguém te conta/contou", "A verdade é que", "O segredo", "Vou te contar uma coisa"? = **VEREDITO=REFAZ**. Abre DIRETO no conteúdo. (✗ `O que ninguém te contou: a dieta te programou` → ✓ `A dieta te programou`.)
4. **Figura abstrata que vira promessa** (teste "dá pra ver?", check abaixo): moldura vazia tipo "a conta muda quando...", "a chave é...", "o jogo vira"? Troca por número, cena ou mecanismo concreto. Achou = REFAZ o trecho.

Achou QUALQUER um dos 4 = o VEREDITO já é REFAZ, não importa o resto. Só passa pro checklist da tabela depois que a varredura zerou.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorado** | nasce de fala literal da fonte (cita N **real**) OU de prova real do autor; **N inventado/plausível = ✗ automático**; fecha em chão (número, avatar, cena, mecanismo), não em tese solta bonita | |
| **Um ponto só** | a peça carrega UMA virada, não a tese inteira; cabe numa frase | |
| **3 tipos de gancho** | usa Falar/Mostrar/Texto na tela quando útil (ao menos 1 marcado; ideal os 3 em conflito) | |
| **Tensão contínua** | a tensão NÃO relaxa no meio; em nenhum ponto o leitor prevê a próxima frase (se prevê, ele pula) | |
| **Lo-fi** | gancho + ideia carregam a peça, sem depender de câmera/edição cara; gravável em minutos | |
| **Espinha ADMA** | Atenção → Diagnóstico → Mecanismo → Ação visível e comprimida em 1-2 min; mostra função, nunca passo a passo | |
| **CTA com destino** | termina com próximo passo real do funil (salvar/comentar/manda/carrossel/isca), não solto | |
| **Dá pra ver?** | fecha o olho e enxerga a cena. ✗ "tenha mais clareza" · ✓ "a recepcionista diz: semana que vem enche" | |
| **Dá pra falsificar?** | é fato falsificável, não adjetivo | |
| **Só você diz?** | o concorrente direto não assina igual (cena/mecanismo proprietário, não promessa banal do nicho) | |
| **C/U/B** | não é **C**onfuso (carregamento cognitivo baixo, explica como pra criança), não é inacreditável (**U**nbelievable, promessa que o leitor não compra), não é **B**oring (chato, encheção de linguiça, introdução antes do conteúdo) | |
| **Anti-IA (HARD)** | rodou o **CHECKPOINT ANTI-IA** de 4 varreduras acima e zerou: zero travessão "—" · zero "travar/travado/destravar" (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo", "o que ninguém te conta/contou", "vou te contar") · sem verbo-clichê ("revoluciona, destrava, transforma"). **1 achado = ✗ automático, VEREDITO=REFAZ; sem exceção, sem "quase passou".** | |
| **Voz do cliente** | (só quando há voz mapeada) o roteiro não cai em NENHUM item da lista de ausência puxada no Passo 0 (palavra/muleta/estrutura que essa voz nunca faz); soa como ele, não genérico. Sem voz mapeada = N/A, não bloqueia | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

## Passo 6, mostra e PARA
Mostra **só o roteiro que passou, LIMPO** (no DOC, nunca solto no chat), com a espinha marcada (qual frase é qual movimento). Sem tabela de gate, sem meta. Pergunta "esse te serve? ajusto ou faço outro?". **Espera a escolha** antes de gerar outro ou montar lote. **Não narra o fluxo** ("agora vou auditar"), só entrega limpo.

**Quando um reel performa, escala (regra do "faz mais", `references/metodo-reel.md` 7.7):** faz mais do mesmo ASSUNTO em outros ângulos, OU troca o tema mantendo a ESTRUTURA da headline que funcionou. Mede comparando com o típico do TEU perfil (skip rate · tempo médio · tempo total · interações), nunca com benchmark de fora: a métrica é diagnóstico, não troféu (`references/metodo-reel.md` 7.9).

## MODO Modelar um viral (opcional, quando há reel de referência)
Dispara quando o dono cola a **URL de um reel** ou aponta uma base de referências e pede "modela esse", "faz um parecido", "um reel na estrutura desse". É um **atalho de estrutura**: em vez de partir do zero, parte de uma espinha de atenção já provada, extrai a PREMISSA dela, e enche com o TEU conteúdo. Modelar aqui é a doutrina Soft, extrai o porquê aquilo prende, nunca decalca. Depois o roteiro volta pro trilho normal e passa pelo MESMO gate do Passo 5. (Fluxo completo, protocolo de dissecação, infra e exemplo denso em `references/modelar-viral.md`.)

**Os 3 ambientes (declara qual é o teu antes de prometer captura):**
- **app / claude.ai (sem Bash):** você NÃO baixa nem transcreve sozinho. Pede a **transcrição colada** + os números (print de views/curtidas/comentários) e disseca o texto; ou conduz pela estrutura que o dono descreve, avisando que sem a transcrição a leitura fica mais rasa. Nunca finge que assistiu.
- **Claude Code (tem Bash):** roda o pipeline inteiro (Apify pega o `videoUrl` → ffmpeg extrai áudio → Groq Whisper transcreve) e entrega o roteiro como arquivo `.md`. **Sem Gemini/análise de vídeo por LLM:** transcreve o ÁUDIO e disseca o TEXTO (a perda é o visual, pega pela legenda ou pergunta ao dono).
- **agente / Telegram (tem Bash):** mesmo pipeline; a ENTREGA é **arquivo**, e a resposta traz o **caminho completo** (ex.: `/home/cloud/reels-modelados/reel-x.md`) com mensagens em texto limpo, sem tabela nem bloco gigante no chat.

**STOP após a dissecação:** mostra a sacada-chave e a estrutura extraída ANTES de escrever o roteiro novo, e confirma o tema/nicho pra onde vai modelar. Não sai escrevendo em cima da premissa sem o dono ver o que você leu do viral.

**O protocolo de dissecação (o checklist do que extrair, `references/modelar-viral.md` §3):** transcrição por timestamp aproximado · gancho (palavras exatas, quantas palavras contadas de fato, qual gatilho, abre com "Eu"?) · linguagem (frase média, proporção você/eu, transições, minimizadores) · estrutura (duração, seções com tempos, antes/depois, CTA, quantos pontos-chave) · a ÚNICA sacada-chave (a premissa que você importa).

**O que importa e o que NÃO importa (§5):** importa a FORMA do gancho, o ritmo, a arquitetura de seções (é a nossa ADMA), o tipo de CTA. NÃO importa o conteúdo dele, e **número/case/fala de terceiro NUNCA vira fato do teu método** (usa o teu número real ou `[DADO: confirmar]`, jamais o dele reaproveitado), nem o traço-assinatura que denunciaria cópia.

**Se a captura/transcrição falhar: relata e PARA.** Nunca inventa a análise (Lei 5). E **descarta a nota 95/100**: o veredito continua binário e honesto (PASSA/REFAZ), o REFAZ aponta o item que falhou. Os dois ✗ mais comuns no modo modelar: **Ancorado ✗** (herdou o número do viral, troca por prova tua) e **Só você diz ✗** (ficou parecido demais, reescreve até a estrutura sumir na tua voz).

## When NOT to use (manda pra skill certa)
- Pediu só a **headline / gancho / capa / abertura** isolada → **soft-conteudo-headlines** (e faz a headline ANTES deste reel).
- Pediu **carrossel** → **soft-conteudo-carrossel**. Pediu **stories** → **soft-conteudo-stories**. Pediu **adaptar pra LinkedIn/X/YouTube** → **soft-conteudo-multiplataforma**.
- Pediu o **Plano / posicionamento / fundação** → **soft-plano-posicionamento**.
- Pediu **arte/visual/PNG/edição** → **soft-designer**.
- Pediu **carta / VSL / página / venda** → **soft-funil-carta**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Escreveu o corpo sem ter headline | Volta: a headline é o Passo 0; sem ela, manda pra soft-conteudo-headlines primeiro |
| Tentou meter a tese inteira no reel | Um ponto só por peça; o resto é outra peça do quebra-cabeça |
| Roteiro relaxa no meio (dá pra prever a frase) | Reescreve pra tensão contínua; cada frase abre a próxima |
| Entregou o passo a passo executável | Mostra função e diagnóstico, nunca o como; passo a passo vira aula grátis |
| Pediu câmera/edição cara | Lo-fi: gancho e ideia carregam; gravável em minutos |
| Impôs como gravar ou aparecer | Sugestão, não obrigação; a pessoa grava do jeito dela, a skill garante o roteiro |
| CTA solto ("siga pra mais") | CTA com destino real do funil (salvar/comentar/manda/carrossel/isca) |
| Inventou um número/fala "plausível" | Só número/fala REAL; sem fonte, marca `[DADO: confirmar]` e não conta como Ancorado=✓ |
| Despejou 5 reels de uma vez | 1 por vez com gate; lote só sob comando "lote de [tema]" |
| Narrou o fluxo ("agora vou pro passo X") | Não narra: executa em silêncio e entrega só o roteiro limpo, sem a tabela do gate |
| Imprimiu a tabela do gate na saída | O gate é INTERNO (auditoria silenciosa); a saída é só a peça limpa |
| Modelou um viral e trouxe o número/case DELE | Número/fala de terceiro nunca vira fato teu; usa o teu real ou `[DADO: confirmar]`, não conta como Ancorado=✓ |
| Roteiro modelado ficou parecido demais com o original | Importa a premissa, não o roteiro; reescreve até a estrutura sumir dentro da tua voz (gate: Só você diz) |
| Deu nota 95/100 ao roteiro modelado | Veredito é binário e honesto (PASSA/REFAZ) e aponta o item que falhou; nota inflada é teatro |
| No app prometeu "baixar e transcrever o viral" | Sem Bash não baixa: pede transcrição colada + números, ou conduz pela estrutura descrita; nunca finge que assistiu |
| Escreveu como se a voz do cliente fosse genérica | Puxa a lista de ausência da voz no Passo 0 e roda como filtro no gate; soa como ele, não só não-IA |
| Deixou um travessão "—" ou frase-emoldura passar pro roteiro | Roda o CHECKPOINT ANTI-IA do Passo 5 (varredura caractere-a-caractere); 1 achado = REFAZ, é o único cinto no app sem lint |
| Fechou com figura abstrata ("a conta muda quando…", "a chave é…") | Não passa no "dá pra ver?"; troca moldura vazia por número, cena ou mecanismo concreto |
| Colou o CTA depois de um bloco neutro (mecanismo/recap) | O CTA vem logo após a virada de interpretação (anti-padroes.md §3); re-ancora a virada antes do CTA ou o CTA vira mendigo de interação |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `references/roteiros-modelo.md`: os 6 roteiros de reel escritos por inteiro (fala + marcação de tempo + edição) pra clonar e adaptar ao nicho.
- `references/modelar-viral.md`: o **modo modelar um viral** por inteiro (dissecação por timestamp, o checklist do que extrair, a infra Apify + Whisper pros 3 ambientes, importar premissa sem decalcar, e o exemplo denso do link ao roteiro). **Dirigida no MODO Modelar um viral.**
- `references/producao-em-lote.md`: template de sessão, rotinas por tipo de reel, calendário por objetivo, sessão-modelo completa (pro comando "lote de [tema]").
- `references/anti-padroes.md`: os anti-padrões do reel com pares errado→certo escritos por extenso.
- `references/metodo-reel.md`: o capítulo-método completo do reel (Lo-fi vence Hi-fi, a Fórmula 7 comprimida, os 3 tipos + os 7 gatilhos da atenção 7.4, conteúdo notável 7.5, a regra do "faz mais"/escalar 7.7, e as 4 métricas como diagnóstico 7.9). É a fonte da verdade do formato. **Dirigida nos Passos 2, 3 e 6.**
- `references/amplificadores.md`: os 10 amplificadores canônicos (frase de 0-2s antes da headline falada) + a tabela de afinidade por template + as regras de uso. **Dirigida no Passo 2.**
- `references/camadas-conciencia.md`: as 3 camadas de atração (C1 reel curto · C2 reel longo opinativo · C3 reel-visita). **Dirigida no Passo 1.**
- `references/estrutura-peca.md`: a Estrutura-Mãe dos 5 papéis com as formas de aterrar Contexto/Conteúdo/CTA, pra quando o reel precisa de repertório tático no corpo.
- `references/dispositivos-de-frase.md`: o repertório de tempero (virada, antítese, evocação sensorial) que entra na revisão, depois da estrutura de pé.
- `scripts/lint_copy.py`: no Claude Code, roda `python3 scripts/lint_copy.py` no roteiro como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual do gate.
