---
name: soft-conteudo-reels
description: >-
  Escreve o ROTEIRO de um reel em arquivo .md, do gancho ao CTA: o que falar, o que mostrar e o que vai escrito na tela. Âncora: ESCREVER o que dizer = reels; EDITAR o vídeo já gravado = soft-editor-video. Use quando o pedido for: "faz um reel sobre X", "roteiro de reel", "o que eu falo nesse vídeo", "script de vídeo curto", "reel de 30 segundos", "vídeo lo-fi", "reel falado", "escreve a legenda de publicação desse reel", "lote de reels". NÃO use pra: PRODUZIR o reel curto de 7 segundos, com cena, render e headline sobre o vídeo (soft-reel-7seg); cortar, queimar legenda ou editar o vídeo já gravado (soft-editor-video); a headline isolada, que vem ANTES (soft-conteudo-headlines); os slides do carrossel (soft-conteudo-carrossel); frames de story (soft-conteudo-stories); adaptar o reel pronto pra outra plataforma (soft-conteudo-multiplataforma); decidir o tema (soft-conteudo-planner); arte e PNG (soft-designer); carta e VSL (soft-funil-carta). Leia e siga o fluxo inteiro do SKILL.md.
---

# Reel, o vídeo curto que atrai

Esta skill escreve o roteiro de um reel inteiro, do gancho ao CTA, e entrega num arquivo `.md` que a pessoa lê e grava. O roteiro sai nas 3 frentes (o que falar, o que mostrar, o que vai escrito na tela), com a espinha marcada frase a frase.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**O universo de títulos do reel inclui o que aparece na tela.** O título é o valor de TEXTO NA TELA de cada bloco, mais o gancho falado dos 3 primeiros segundos e a legenda de publicação. Cole `textos na tela: N · linhas em titulos.txt: pelo menos N`, e o `--conferir` reprova quando o `titulos.txt` tiver menos linhas que os textos de tela da tabela.

**O TEXTO NA TELA é rótulo de leitura rápida, não headline, e a régua de caixa alta da headline não alcança ele.** O que a régua proíbe é maquiar: o `conferencia/titulos.txt` copia a forma literal que está na peça, caractere por caractere, inclusive a caixa alta. Monte o arquivo por comando sobre a coluna da tabela e cole a saída. Reescrever a forma no arquivo de conferência pra passar no gate reprova a entrega, mesmo com o motivo declarado no relato. E a palavra de CTA que o dono já usa na boca dele não é automação: é a forma de ele saber de onde veio a conversa. `nenhuma automação` no perfil descreve a ferramenta, nunca a palavra.

**A conclusão nasce da saída do grep, e negar a saída colada reprova.** Depois de colar a saída, escreva uma linha por ocorrência: `<arquivo:linha> | ação: <verbo> | palavra: <literal> | usada? sim/não · porque: <motivo>`. **Conclusão negativa só é válida com a saída vazia**, e o `--conferir` sai com exit 1 e `conclusão contradiz a saída do grep` quando a peça diz `palavra-chave: nenhuma` com ocorrência colada na mesma checagem.

**O inventário tem um universo só, e o arquivo à parte não cria um segundo.** Quando os valores desdobrados não couberem no `conferencia/checagem-titulos.md`, a tabela vai pra arquivo próprio e a **linha de fecho continua sendo uma só**, com os quatro inteiros, repetida idêntica nos dois arquivos. O piso sozinho (`campos no perfil: 29`) **nunca aparece em linha própria**. Antes de fechar, rode `grep -rn 'campos no perfil' <pasta>` e confira que toda linha que volta traz os quatro números, e os mesmos quatro. Cole a saída.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Capacidade negada no perfil é fato, nunca lacuna a interpretar.** Antes de escolher a mecânica do CTA, rode `grep -in 'automação\|automacao\|robô\|bot' <perfil do dono>` e cole a saída literal. Linha que diz `nenhuma automação` responde `não`, e ela não é omissão nem falso positivo a contornar. Cole `mecânica exige automação? sim/não · perfil declara: <a linha literal> · mecânica adaptada: <qual>`. Negação no perfil sai como CTA sem robô, e manter a mecânica por leitura funcional, herança de outra plataforma ou hábito presumido reprova a peça.

**A fronteira, na primeira linha:** ESCREVER o que dizer é desta skill. **EDITAR o vídeo já gravado (corte, legenda, b-roll, ritmo, cold open) é da soft-editor-video.** Se o dono já gravou e quer mexer no vídeo, esta skill não é a certa.

**Você não precisa ter a headline pronta pra começar.** O caminho principal é escrever a headline AQUI, pela régua de título que esta skill carrega (`shared-references/crivo/07-regua-de-titulos.md`): sem headline escolhida, ela escreve 3 aberturas a partir da dor mais forte que ancorou e pede pro dono cravar UMA (o "Sem o insumo" abaixo). Quer um banco maior de variações? Existe a soft-conteudo-headlines, mas é opção, o gancho se resolve aqui. O reel nunca para por falta de gancho.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra, num caso fictício de nicho neutro, a entrada que o dono deu, as perguntas que a skill fez e um roteiro completo escrito no formato real da entrega, com a espinha marcada e o gate explicado.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o tema e a dor mais forte e eu escrevo o roteiro). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra o roteiro com o que o dono já colou. Se faltar um insumo que o reel não vive sem (o assunto, ou a dor que o gancho ataca), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez (o ponto único do reel, a dor, a headline se houver) e escreve com o que o dono for dando.

A pergunta do modo é UMA por reel. As outras três partes entram nos passos abaixo:

- **Ensina enquanto faz:** ao escolher o tipo de gancho e a duração da espinha, escreve UMA linha do porquê ("abro pelo gancho de erro comum porque o tema tem um mito forte pra derrubar; gancho de promessa entrega mais rápido, mas segura menos"), pra o dono decidir sozinho na próxima.
- **Puxa o material bruto:** quando a dor vier rasa ("as pessoas não sabem disso"), não segue no genérico. Pede o concreto: "me conta de UM cliente, o que ele te falou quando errava isso, com as palavras dele?". A fala real vira o gancho falado dos 3 primeiros segundos.
- **Oferece refinar no fim:** depois de mostrar o roteiro, fecha com UMA linha de ajuste ("quer outro gancho? mais curto? outro CTA no fim? reescrevo só a parte que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## A estrutura do reel, numa visão só (espinha + duração + formato)

Uma tabela, três decisões: qual movimento vai em qual trecho, quanto tempo o reel tem, e qual variante de formato.

| Trecho | Movimento da espinha | O que ele faz | Topo (alcance, 15 a 40s) | Fundo (aquecer, 60 a 90s) |
|---|---|---|---|---|
| 3s | **Atenção** (gancho) | a frase que para o scroll | 3s, gancho AMPLO | 3s, gancho que já filtra |
| Abertura | **Quebra de crença** | mostra a tensão, não resolve | 3 a 8s | 8 a 20s |
| Meio | **Diagnóstico + Vilão** | nomeia a causa, culpa o modelo velho | 8 a 20s | 20 a 55s |
| Virada | **Nova oportunidade** | existe outro caminho | 20 a 30s | 55 a 75s |
| Fechamento | **Mecanismo + Convite** | função do método + CTA com destino | 30 a 40s | 75 a 90s |

**As 3 variantes de formato**, escolhidas antes de escrever: **falado normal** (o default, câmera na mão, corte simples) · **YAP** (talking-head cru, sem corte seco, fala de mesa, planejado com cara de improviso) · **7 segundos** (vídeo mudo de cena cotidiana, título de curiosidade na tela, o conteúdo inteiro na legenda de 1000 a 1500 caracteres). As três usam a MESMA espinha; o que muda é a casca.

**Regra de duração:** faixa ótima 30 a 60s. Passar de 90s só quando a tese exigir e cada bloco segurar sozinho.

## O perfil do dono vem do banco do agente

Onde esta skill precisa de voz, avatar, mecanismo, inimigos ou prova: **leia do perfil/brain do agente quando existir**; se não existir, faça a entrevista curta do "Sem o insumo" e siga com o que faltar marcado `[DADO: confirmar]`. Nunca invente, nunca crie um arquivo de perfil.

## O bloco da ação (esta skill tem uma ação só: escrever o roteiro)

**O que faz:** transforma um gancho e uma fala real de cliente no roteiro de um reel, comprimido na duração da camada.

**Precisa de:** a **headline/gancho** (você escreve aqui pela régua desta skill, ou puxa de um banco pronto) · 3 a 5 falas de DOR e 3 a 5 de DESEJO sobre o tema, do perfil/brain do agente · a fundação (tese, inimigos, mecanismo nomeado, cliente em uma frase), do perfil/brain · o destino do CTA (o que o dono quer que a pessoa faça depois).

**Sem o insumo:**
- **Sem headline:** escreva aqui mesmo **3 opções de abertura** partindo da fala de dor mais forte que você ancorou (frase curta, uma ideia, sem rótulo abstrato, dentro do teto de 7 palavras faladas), peça ao dono escolher UMA, e siga com a escolhida. Corpo sem gancho é vídeo que ninguém assiste.
- **Sem fundação nenhuma:** entrevista curta de 4 perguntas, numa mensagem só. (1) Quem é o teu cliente, em uma frase. (2) Uma dor que ele te fala com as palavras dele. (3) Contra qual prática do teu mercado você é. (4) O que o teu método faz de diferente, e como ele se chama. O que faltar vira `[DADO: confirmar]`.
- **Sem destino de CTA:** pergunta UMA coisa, "depois desse reel, pra onde você quer mandar a pessoa?", e oferece as opções reais (salvar, comentar uma palavra, mandar pra alguém, ir pro carrossel, ir pra isca).

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `reel-[tema].md`, com um H1 (o título do reel) e nada mais de cabeçalho, a variante de formato e a camada declaradas no topo, o roteiro escrito nas 3 frentes (FALAR, MOSTRAR, TEXTO NA TELA) e a espinha marcada frase a frase. A tabela de destino de dados, a contagem e qualquer outro cabeçalho de trabalho ficam em `conferencia/`, fora do arquivo do reel. No formato de 7 segundos, o doc traz também a legenda inteira. Em ambiente que renderiza markdown, mostre o doc renderizado; com sistema de arquivo, salve o `.md`; num agente de mensageria, grave o arquivo e cite o path completo. A condução acontece no chat; o ROTEIRO mora no doc. **STOP** por reel.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/metodo-reel.md` (o capítulo-método completo, é a fonte da verdade do formato) · `references/roteiros-modelo.md` (os 6 roteiros escritos por inteiro, pra clonar a estrutura).

**Profundidade:** `references/amplificadores.md` (a frase de 0 a 2s antes do gancho, dirigida no Passo 2) · `references/camadas-conciencia.md` (as 3 camadas, dirigida no Passo 1) · `references/roteiros-modelo-gringos.md` (49 estruturas modeladas de material externo) · `references/producao-em-lote.md` (só pro comando "lote de [tema]") · `references/anti-padroes.md` · `references/estrutura-peca.md` · `references/dispositivos-de-frase.md`.

Passos: 0 (parte da headline e ancora) → 1 (o único ponto + camada) → 2 (gancho nos 3 tipos) → 3 (espinha na duração) → 4 (CTA com destino) → 5 (gate por dentro) → 6 (mostra e PARA).

---

## Por que o reel funciona (a doutrina, em 4 linhas)

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

## Passo 0, parte da headline e ancora (NÃO PULE)
O reel começa de uma **headline definida**. Se o usuário ainda não tem a headline (a frase que para o scroll nos 3 primeiros segundos), você **não escreve o corpo** sem ela, mas resolve AQUI mesmo pela régua de título desta skill: escreve 3 opções de abertura partindo da fala de dor mais forte que você ancorou (frase curta, uma ideia, sem rótulo abstrato), peça ao dono escolher uma, e siga com a escolhida. Quem quer um banco maior de variações pode passar pela soft-conteudo-headlines, mas isso é opção, a headline se resolve aqui. Corpo sem gancho é vídeo que ninguém assiste.

Com a headline na mão, procura a fonte de fala real do cliente, nesta ordem: **descrição do projeto** → **Plano colado na conversa** → **mensagens anteriores**. Puxa **3-5 falas de DOR + 3-5 de DESEJO** do tema, literais, contando o N (quantas vezes apareceu). O corpo do reel nasce dessas falas, na voz do cliente final, nunca no jargão de marketing.

Três estados de entrada (declara qual é o seu antes de escrever):
- **Tem fala real (com N):** ancora nela e cita o N. Caminho ideal.
- **Tem nicho/fundação mas ZERO fala literal:** NÃO inventa fala nem N. O roteiro ancora em **prova real do autor** (resultado, case, mecanismo); qualquer número que você não confirmou entra como `[DADO: confirmar]` e **NÃO conta como Ancorado=✓**. Avisa: minerar 5-8 falas reais (ou rodar o Plano na soft-plano-posicionamento) deixa o roteiro muito mais cravado.
- **Sem nicho e sem nada:** pergunta numa única mensagem (nicho em 1 linha + 1 dor real que o cliente fala + a headline) e segue daí.

A fundação (quando existe, do Plano): tese central · top 3 inimigos nominais · mecanismo nomeado · cliente em uma frase.

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

**Confirma qual dos 7 gatilhos a abertura aciona** (Recompensa · Mistério · Reconhecimento · Popularidade · Crença · Autoridade · Disrupção): toda abertura forte aciona ≥1. A headline (escrita aqui pela régua desta skill, ou vinda de um banco) já traz um gatilho; aqui você confirma qual está ativo no corpo. **Disrupção exige defesa com argumento sólido logo depois**, senão vira clickbait e queima reputação. (Tabela dos 7 + os 3 tipos detalhados em `references/metodo-reel.md` 7.4.)

**Amplificador (opcional, 0-2s antes da headline falada):** uma frase curta que precede a headline e carrega 2s a mais de atenção (ex.: "Por que ninguém tá falando sobre isso?"). Os 10 canônicos + a afinidade por template em `references/amplificadores.md`. Um por peça, nunca se a headline já está cravada ou o tempo dos 3s estourou.

**Como aparecer no vídeo é só sugestão, nunca obrigação.** A pessoa grava do jeito dela; o que a skill garante e entrega é o ROTEIRO. Quando sugerir cena, gesto ou edição, deixa explícito que é opcional, um caminho possível, não uma regra.

### MODO ALCANCE vs MODO FILTRO (declara o modo ANTES de escrever o gancho)
- **Reel de TOPO (objetivo alcance): capa/gancho AMPLO**, o filtro entra do meio pro fim do reel. Motivo com número: ~50% da audiência cai nos 3 primeiros segundos; reel com hold acima de 60% nos 3s alcança 5 a 10x mais que reel com hold abaixo de 40%. Gancho que filtra cedo derruba o hold e mata a distribuição.
- **Reel de FUNDO (aquecer quem já segue): filtro cedo**, doutrina deste método normal.
- A escolha do modo é declarada antes de escrever. **Em anúncio, SEMPRE modo filtro** (regra da capa por terreno da `soft-trafego-meta`: em anúncio o criativo é a segmentação, gancho amplo entrega lead ruim).

### FORMATO YAP (talking-head cru)
Variante lo-fi levada ao limite: vídeo falado direto pra câmera, zero edição polida, cenário real (sofá, carro, rua). Benchmark 2026: especialista falando direto pra câmera supera criativo polido em alcance e engajamento; o cérebro processa rosto mais forte que qualquer outro estímulo visual; confiança em pessoa vale mais que confiança em anúncio. **REGRA-CHAVE: o yap viral é PLANEJADO com cara de improviso.** A espinha ADMA continua obrigatória por baixo; o que muda é a casca: sem corte seco, sem legenda de estúdio, fala corrida de mesa. Compatível com MODO ALCANCE.

### FORMATO REEL DE 7 SEGUNDOS (vídeo mudo, conteúdo na legenda)
Variante que inverte onde mora a informação: o vídeo (até 7s, sem fala, cena cotidiana comum, tomando café, mexendo com o cachorro, trabalhando, embalando pedido, sem olhar pra câmera) é só o gancho visual, e o conteúdo inteiro vai pra legenda (1000-1500 caracteres, escrita por esta skill e passando pelo gate normal do Passo 5, mesmo sem fala no vídeo). Por cima do vídeo entra um título de curiosidade que empurra pra legenda (modelo: "e eu que descobri o método para alcançar X objetivo"), o TEXTO NA TELA do Passo 2 fazendo esse trabalho sozinho, já que aqui não há FALAR nem MOSTRAR carregando gancho. Ritmo: 1-2 posts por dia. Compatível com MODO ALCANCE (gancho amplo, o filtro mora na legenda). **Nota de automação:** o formato é esteira: biblioteca de cenas cotidianas reaproveitável + títulos de curiosidade do banco de headlines + legenda gerada por esta skill formam um pipeline automatizável (cena + título + legenda), sem depender de roteiro falado novo a cada peça.
Lastro (benchmark 2026, tecnica conhecida como "Read Caption"): o intervalo de decisao do viewer e exatamente 5-7s; reel curto tem 68% de completion vs 48% do longo, e completion e o sinal que o algoritmo mais premia; 75% assistem no mudo. Legenda com pergunta/CTA puxa comentario e amplia distribuicao.

## Passo 3, desenvolve pela espinha ADMA (na duração da camada)
A mesma espinha do carrossel, comprimida no tempo do vídeo. Cada frase abre a próxima. **A tensão não relaxa.** Se o leitor consegue prever a próxima frase, ele pula. A tensão é o que segura, não a informação. Mostra o **diagnóstico**, nunca o passo a passo executável (passo a passo vira aula grátis e não vira venda).

| Trecho | Movimento | Função |
|---|---|---|
| **3s** | Atenção (Hook) | interrupção, a frase que para o scroll (a headline do Passo 2) |
| **Abertura** | Quebra de crença | conflito, mostra a tensão vivida, não resolve ainda |
| **Meio** | Diagnóstico + Vilão | nomeia a causa real, o culpado é o modelo velho, não o leitor |
| **Virada** | Nova oportunidade | a virada de interpretação, existe um caminho diferente |
| **Fechamento** | Mecanismo + Convite | aponta pro método (função, não execução) + CTA com destino |

Duração POR CAMADA (benchmark de retenção 2026: faixa ótima 30-60s; abaixo de 30s tem o maior engajamento): TOPO/alcance 15-40s · FUNDO/aquecer 60-90s. Passar de 90s só quando a tese exigir e cada bloco segurar sozinho. Quando for impulsionar, testa o corte 30-45s contra a versão longa antes de escalar. Polariza (toma lado, gancho que polariza exige corpo que sustenta). Carrega **moeda social** (≥2 de: valor prático, identificação, opinião forte, argumentação, notícia, história, prova, fato curioso). Sempre aponta pro método ou faz seeding da tese.

**Depois do gancho, o conteúdo precisa ser NOTÁVEL** (`references/metodo-reel.md` 7.5): (1) algo NOVO, um ângulo que quase ninguém falou (se a pessoa prevê a próxima frase, ela pula); (2) baixo carregamento cognitivo, explica como pra criança, termo técnico só com tradução fácil em seguida; (3) sem encher linguiça, curto não raso, zero introdução antes de entrar no conteúdo.

Os 6 roteiros-modelo (decisão contraintuitiva · erro que custou caro · bastidor · contraste de resultado · crença errada · caso real) estão em `references/roteiros-modelo.md`, profundidade opcional, clona e adapta, nunca copia cru.

**A coluna MOSTRAR é instrução, não sugestão.** Cada célula abre com substantivo concreto e verbo executável ("caneta circulando o número 12 no calendário"), nunca com hedge ("sugestão de cena", "talvez um close", "algo como um gráfico", "se possível, mostrar"). Quem lê a célula tem que saber o que apontar a câmera pra fazer, sem decidir nada. **Checagem colada antes de fechar: `grep -c 'ugest\|talvez\|algo como\|se possível' <peça>` tem que devolver 0.** Saída diferente de zero manda a célula de volta pra reescrita.

## Passo 4, fecha com CTA de próximo passo real
O reel não fecha venda, mas aponta pra onde. O CTA convida, não empurra, e tem **destino concreto do funil**: salvar, comentar uma palavra, mandar pra alguém, ir pro carrossel que aprofunda, ir pra isca/carta. CTA sem destino é peça órfã, o leitor para e não tem pra onde ir. Escreve o CTA na voz do cliente, ligado ao ponto único do reel.

**A palavra-chave do CTA sai de COMANDO, e o comando é sobre os INSUMOS, não sobre o perfil.** Antes de escrever o CTA, rode e cole a saída:

```
grep -rn 'manda \|comenta \|envia \|digita ' <pasta de insumos>
```

A pasta é a de insumos inteira (transcrição, call, caixa de entrada, site), nunca só o arquivo de perfil. A palavra vem dali com a grafia EXATA, sem espaço a mais nem a menos: "BASE", "BASE 40" e "BASE40" são três palavras diferentes pra quem digita e pra automação que responde. A linha `palavra-chave: <literal> | origem: <arquivo:linha>` é obrigatória na peça. **Sem saída no grep, o CTA sai SEM palavra** ("me chama no Direct e eu te mando"), nunca com uma escolhida pelo tema, e a pergunta vai pro handoff. Dado que existe no disco nunca vira marcador nem palavra inventada.

## Passo 5, roda o GATE por dentro (auditoria interna, NÃO imprime)

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento). Palavra fora dessa lista não é gatilho e não conta**: título nomeado com "autoridade + especificidade" ou "ação + destino explícito" fica com zero gatilhos rastreáveis e volta pro passo de escrita. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo. **O lote da régua é o que está NA PEÇA, e os dois números batem.** Variação escrita durante o processo e jogada fora não entra na contagem: declarar 7 títulos com 4 no roteiro é contar o rascunho. Toda variação que você quiser mostrar sai marcada `descartada, não publicada` na própria linha, e ela cai fora dos dois lados da conta. A linha `títulos na peça: N · na checagem: N` traz os dois números iguais, e o `--conferir` reprova quando não trazem. **E ele tem FORMA obrigatória:** a `conferencia/checagem-titulos.md` do reel é reprovada se não trouxer, nesta ordem, (1) o universo declarado (o gancho FALAR dos 3 primeiros segundos, cada TEXTO NA TELA e a legenda), com o critério de exclusão escrito ao lado de cada item deixado de fora; (2) uma seção por regra, de R1 a R7, nomeadas por extenso; (3) **dois gatilhos da lista fechada por título**, e a linha com menos de dois volta pro passo de escrita; (4) o bloco de fecho com as contagens; (5) as 3 melhores marcadas com ★ e uma linha de porquê cada. Antes de fechar, rode `python3 scripts/lint_copy.py <roteiro>` (o script está na pasta desta skill) e cole a saída do contador de molde: o número dele manda sobre qualquer contagem escrita de cabeça.

**R3, as 3 teses mínimas, e a comparação vai par a par.** O lote de títulos do reel (o gancho FALAR, cada TEXTO NA TELA, a legenda) carrega no mínimo 3 teses distintas, e contar linhas não é contar teses. Salve uma tese de 4 palavras por linha em `teses.txt`, rode `sort teses.txt | uniq -c` pra achar a repetição literal, e cole a saída. Depois cole a comparação de TODOS os pares vizinhos da lista ordenada, nesta forma, uma linha por par:

```
<tese A> vs <tese B> | sujeito igual? s/n | predicado igual? s/n | conta como 1? s/n
```

**Duas teses que compartilham sujeito E predicado contam como UMA**, ainda que a fórmula mude. `teses distintas: N` sem esse bloco colado não conta como feita, e `N` abaixo de 3 reprova o lote inteiro, não o título: os repetidos voltam pro passo de escrita. `N` igual ao total do lote num lote acima de 8 é resultado inválido.

**A ressalva clínica mora FORA da fala, sempre.** Quando a R6 pede a nota de saúde (gancho com número em cima de sintoma nomeado, promessa de corpo, emagrecimento ou cura), ela sai numa linha própria da peça, nota de saúde ou rodapé, **nunca dentro do gancho, do bloco de quebra de crença ou dos primeiros 10 segundos**: ressalva falada em cima do gancho gasta o tempo mais caro do reel e desativa a frase que o dono pediu. Checagem colada: `a ressalva está dentro de alguma célula FALAR? sim reprova` e `ressalva na peça: linha <N>`.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase. **O teste não é "a frase fica agramatical": é "a frase existiria sem o dado?".** Frase cuja única função é registrar a pendência ("Prazo exato do caso: [A CONFIRMAR: número de semanas]") está no miolo por definição e sai da peça, mesmo parecendo um campo. **Antes de marcar qualquer número, grepe os insumos (`grep -in '<termo>' <insumos>`) e cole a saída: dado que existe no disco nunca vira marcador.** Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**O corpo da peça contém só o que o destinatário lê.** Instrução dirigida ao dono ("confirme", "valide", "ajuste antes de publicar", "verifique com o conselho") vai no handoff ou no bloco de configuração, **nunca dentro de mensagem, slide, frame, bloco de página ou fala**: briefing impresso dentro do produto é o dono falando sozinho na cara do cliente. A ressalva de nicho que o destinatário precisa ler fica; a ordem de serviço pro dono sai. Checagem verificável, restrita às seções públicas: `grep -nE 'antes de publicar|confirme|valide|verifique com' <peça>` tem que voltar vazio.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A tabela de destino de cada dado e a linha de fechamento moram em `conferencia/checagem-titulos.md`, nunca no arquivo do reel que o dono abre.** O reel que ele lê tem só o H1 do título e o roteiro nas 3 frentes; a tabela `<dado> | usado ou descartado` é auto-avaliação da máquina e o `--conferir` reprova quando ela vaza pra peça (`bastidor na peça pública`). **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado, e a conta vem ANTES de escrever a peça.** Monte a conta em 3 passos e cole em `conferencia/`: (1) `grep -c '^-' <perfil>` = C campos; (2) percorra os campos e escreva `campo <n>: <k> valores` para todo campo com k maior que 1, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1; (3) some, e M é o piso. Cole `campos no perfil: C · valores desdobrados: M · linhas do inventário: M`. **Inventário com menos de M linhas reprova sem análise de conteúdo, e a linha que agrupa dois dados conta como UMA linha e como N dados faltando.** A ordem é o que decide: a conta feita depois da peça vira justificativa, e a conta feita antes vira o alvo. A conta fica em `conferencia/checagem-titulos.md`, na forma `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Checagem sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

Roda o gate no roteiro **internamente** (auditoria silenciosa). Só roteiro com a linha VEREDITO=PASSA vai pro cliente. Um ✗ refaz o ponto que falhou (não o conceito inteiro). A tabela abaixo é o teu **checklist interno**, nunca a saída: o usuário recebe só o roteiro limpo (Passo 6), jamais a tabela.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorado** | nasce de fala literal da fonte (cita N **real**) OU de prova real do autor; **N inventado/plausível = ✗ automático**; fecha em chão (número, avatar, cena, mecanismo), não em tese solta bonita | |
| **Um ponto só** | a peça carrega UMA virada, não a tese inteira; cabe numa frase | |
| **3 tipos de gancho** | usa Falar/Mostrar/Texto na tela quando útil (ao menos 1 marcado; ideal os 3 em conflito) | |
| **Tensão contínua** | a tensão NÃO relaxa no meio; em nenhum ponto o leitor prevê a próxima frase (se prevê, ele pula) | |
| **Lo-fi** | gancho + ideia carregam a peça, sem depender de câmera/edição cara; gravável em minutos | |
| **Espinha ADMA** | Atenção → Diagnóstico → Mecanismo → Ação visível e comprimida na duração da camada (topo 15-40s, fundo 60-90s); mostra função, nunca passo a passo | |
| **CTA com destino** | termina com próximo passo real do funil (salvar/comentar/manda/carrossel/isca), não solto | |
| **As 3 perguntas, dá pra ver?** | fecha o olho e enxerga a cena. ✗ "tenha mais clareza" · ✓ "a recepcionista diz: semana que vem enche" | |
| **As 3 perguntas, dá pra falsificar?** | é fato falsificável, não adjetivo | |
| **As 3 perguntas, só você diz?** | o concorrente direto não assina igual (cena/mecanismo proprietário, não promessa banal do nicho) | |
| **C/U/B** | não é **C**onfuso (carregamento cognitivo baixo, explica como pra criança), não é inacreditável (**U**nbelievable, promessa que o leitor não compra), não é **B**oring (chato, encheção de linguiça, introdução antes do conteúdo) | |
| **Anti-IA (HARD)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz, o verbo que rima com "cravar" e suas flexões (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype (o "revoluciona/transforma" e o próprio verbo-freio banido). **No chat (sem o lint), faz um CTRL+F manual do travessão longo (U+2014) e a família do verbo-freio banida antes de marcar ✓.** | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

## Passo 6, mostra e PARA

**Antes de mostrar, rode e cole as duas checagens de disco:** (1) `grep -c 'Dados fornecidos' <peça>` devolve 0? A tabela de destino mora em `conferencia/`, e um 1 aqui é bastidor vazando pro arquivo do dono; (2) `grep -cE '^#{2,}' <peça>` devolve 0? O reel tem só o H1 do título; um cabeçalho `##` a mais é fragmento de trabalho no roteiro. Qualquer um fora do zero, volta pro gate do Passo 5 e mova o excesso pra `conferencia/`: o roteiro é a peça que costuma sair com bastidor no arquivo que o dono abre. Cole a saída literal dos dois comandos. A contagem de dados e o gatilho de cada título ficam em `conferencia/checagem-titulos.md`, conferidos lá.

Mostra **só o roteiro que passou, LIMPO**, no doc, com a espinha marcada (qual frase é qual movimento). Sem tabela de gate, sem meta. Pergunta "esse te serve? ajusto ou faço outro?". **Espera a escolha** antes de gerar outro ou montar lote. **Não narra o fluxo** ("agora vou auditar"), só entrega limpo.

**Quando um reel performa, escala (regra do "faz mais", `references/metodo-reel.md` 7.7):** faz mais do mesmo ASSUNTO em outros ângulos, OU troca o tema mantendo a ESTRUTURA da headline que funcionou. Mede comparando com o típico do TEU perfil (skip rate · tempo médio · tempo total · interações), nunca com benchmark de fora: a métrica é diagnóstico, não troféu (`references/metodo-reel.md` 7.9).

## Um roteiro fechado, no formato exato da entrega

Caso fictício, nicho neutro: um treinador de corrida de rua que atende corredor amador de 35 a 52
anos. Mecanismo dele (fictício): **Zona 2 Honesta**, a corrida lenta corrida no ritmo certo. Formato:
falado normal. Camada: C1 (alcance). Modo: ALCANCE, gancho amplo. Duração: 35s.

**Ponto único da peça:** o treino leve corrido rápido demais é o que segura o tempo.

| Tempo | Espinha | FALAR | MOSTRAR | TEXTO NA TELA |
|---|---|---|---|---|
| 0 a 3s | Atenção | "Correr devagar te deixa mais rápido." | ele correndo devagar, relógio no pulso em close | DEVAGAR |
| 3 a 9s | Quebra de crença | "E a maioria não consegue. Não por preguiça. Porque devagar é chato, e o corpo pede pra acelerar." | ele acelerando sem perceber | (nada) |
| 9 a 20s | Diagnóstico + Vilão | "Você sai pra correr leve, o relógio marca zona 3, e você acha que foi um bom treino. Foi um treino médio. Fez você cansar sem melhorar nada. A planilha que te deram nunca disse em qual ritmo, só disse o quanto." | print do relógio marcando zona 3 num treino chamado leve | ZONA 3 NO TREINO LEVE |
| 20 a 28s | Nova oportunidade | "Existe um jeito de saber se o teu leve é leve de verdade, e não é o relógio que responde." | ele parando e falando pra câmera | (nada) |
| 28 a 35s | Mecanismo + Convite | "É conseguir falar uma frase inteira correndo. Se você não consegue, não é treino leve. Eu chamo isso de Zona 2 Honesta. Salva esse aqui e testa no próximo treino leve." | ele falando enquanto corre | SALVA E TESTA |

**Legenda (quando o formato for o de 7 segundos, o conteúdo inteiro vai aqui, 1000 a 1500 caracteres).**
No formato falado, a legenda é curta e repete o CTA: "Testa no próximo leve e me conta se conseguiu
falar a frase inteira."

**O que rodou por dentro e não apareceu:** a primeira versão do trecho de 9 a 20s entregava o passo a
passo ("corra 6 semanas a 70% da FC máxima, use a fórmula 220 menos a idade"). Isso é aula grátis e
falha no check de mecanismo. Reescrito pra mostrar o diagnóstico e a FUNÇÃO, guardando o como.

## O que esta skill NÃO faz (e pra onde vai)

Esta skill escreve o ROTEIRO e para aí. Em toda rota abaixo, se a skill de destino não estiver instalada, esta faz o mínimo aqui e diz o que fez.

| O pedido é | Vai pra | Se não estiver instalada |
|---|---|---|
| **Cortar, legendar, editar** o vídeo já gravado, b-roll, ritmo, cold open | **soft-editor-video** | descreve em texto o corte pretendido e avisa que a edição em si fica pendente |
| A **headline/gancho** isolada, que vem ANTES | **soft-conteudo-headlines** | escreve 3 aberturas a partir da dor ancorada e pede pro dono cravar UMA |
| Os **slides do carrossel** | **soft-conteudo-carrossel** | entrega só o roteiro e diz que os slides são outra peça |
| A **sequência de frames** de story | **soft-conteudo-stories** | quebra o roteiro em frames de texto na tela e avisa |
| Levar este reel pra **LinkedIn, X, YouTube, TikTok, e-mail** | **soft-conteudo-multiplataforma** | entrega só a versão de reel e diz que a adaptação fica pendente |
| Decidir **sobre o que postar** (tema da semana ou do mês) | **soft-conteudo-planner** | pergunta o tema ao dono e segue com o que ele disser |
| **Arte, PNG, visual** | **soft-designer** | entrega só o texto |
| **Posicionamento, mecanismo, pilares** | **soft-plano-posicionamento** | roda a entrevista curta de 4 perguntas acima e marca `[DADO: confirmar]` |
| **Carta, VSL, página, venda** | **soft-funil-carta** / **soft-funil-landing** | escreve só a peça de feed e aponta o que falta |

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Escreveu o corpo sem ter headline | Volta: a headline é o Passo 0; sem ela, escreva a headline AQUI pela régua desta skill antes de seguir |
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

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `shared-references/crivo/07-regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta (a entrada do dono, as perguntas feitas e a saída real de cada ação). **Leia antes da primeira pergunta.**
- `references/roteiros-modelo.md`: os 6 roteiros de reel escritos por inteiro (fala + marcação de tempo + edição) pra clonar e adaptar ao nicho.
- `references/roteiros-modelo-gringos.md`: 49 estruturas de roteiro modeladas de material externo (04/08/2026, marca-neutra), rodízio de forma pra clonar a ESTRUTURA e preencher com o território do avatar; nunca copia o exemplo, todo roteiro gerado passa pelo gate do Passo 5.
- `references/producao-em-lote.md`: template de sessão, rotinas por tipo de reel, calendário por objetivo, sessão-modelo completa (pro comando "lote de [tema]").
- `references/anti-padroes.md`: os anti-padrões do reel com pares errado→certo escritos por extenso.
- `references/metodo-reel.md`: o capítulo-método completo do reel (Lo-fi vence Hi-fi, a Fórmula 7 comprimida, os 3 tipos + os 7 gatilhos da atenção 7.4, conteúdo notável 7.5, a regra do "faz mais"/escalar 7.7, e as 4 métricas como diagnóstico 7.9). É a fonte da verdade do formato. **Dirigida nos Passos 2, 3 e 6.**
- `references/amplificadores.md`: os 10 amplificadores canônicos (frase de 0-2s antes da headline falada) + a tabela de afinidade por template + as regras de uso. **Dirigida no Passo 2.**
- `references/camadas-conciencia.md`: as 3 camadas de atração (C1 reel curto · C2 reel longo opinativo · C3 reel-visita). **Dirigida no Passo 1.**
- `references/estrutura-peca.md`: a Estrutura-Mãe dos 5 papéis com as formas de aterrar Contexto/Conteúdo/CTA, pra quando o reel precisa de repertório tático no corpo.
- `references/dispositivos-de-frase.md`: o repertório de tempero (virada, antítese, evocação sensorial) que entra na revisão, depois da estrutura de pé.
- `scripts/lint_copy.py`: quando há shell disponível, roda `python3 scripts/lint_copy.py` no roteiro como cinto extra do anti-IA (reprova o travessão longo U+2014 e o verbo-freio banido). No chat não roda, por isso o CTRL+F manual do gate.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
