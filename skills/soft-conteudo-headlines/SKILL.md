---
name: soft-conteudo-headlines
description: >-
  Encontra a HEADLINE (gancho, abertura, manchete, capa, título, assunto) e entrega o banco de headlines por família de gatilho, num arquivo .md. Use quando o pedido for: "me dá headlines sobre X", "banco de headlines", "escreve o gancho falado desse reel", "qual a capa desse carrossel", "escreve a chamada", "título pro YouTube", "assunto do e-mail", "primeiros 3 segundos", "abertura do story", "manchete". NÃO use pra: "faz o gancho desse vídeo" quando é montar o cold open no vídeo já gravado (soft-editor-video); os slides do carrossel (soft-conteudo-carrossel); o roteiro do reel depois do gancho (soft-conteudo-reels); frames de story (soft-conteudo-stories); adaptar peça pronta pra outra plataforma (soft-conteudo-multiplataforma); decidir SOBRE O QUE postar (soft-conteudo-planner); posicionamento e pilares (soft-plano-posicionamento); arte e PNG (soft-designer); abertura de carta (soft-funil-carta); abertura da aula (soft-webinar). Leia e siga o fluxo inteiro do SKILL.md.
---

# Headline: a linha que já existe na cabeça do leitor

Esta skill encontra a primeira linha de qualquer peça (a capa do carrossel, os 3 primeiros segundos do reel, a abertura do story, o título do YouTube, o assunto do e-mail) e entrega um banco de headlines agrupado por família de gatilho, num arquivo `.md` que o dono guarda e reusa. Ela ancora na fala real do cliente, escreve dentro do cânone de fórmulas, e reprova sozinha tudo que não passa no gate. O resultado é um documento de headlines prontas pra escolher, nunca uma lista solta no meio da conversa.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**As cenas saem listadas antes de escrever, e lote sem cena reprova** (a régua já cobra isto em `crivo/07-regua-de-titulos.md`, no bloco do nicho trocado; aqui ela é passo de trabalho). No Passo 0, liste as CENAS dos insumos, uma por linha, `<cena em até 8 palavras> | origem: <arquivo:linha>`. Cena tem lugar, objeto ou data (a escada do prédio, o dia 12, o aplicativo instalado sem abrir), nunca sentimento nem diagnóstico. Depois de escrever, cole `cenas disponíveis: N · usadas no lote: N`. **Lote acima de 4 unidades com `usadas: 0` volta pro passo de escrita**, porque o banco de fórmulas dá a forma e a cena é a única coisa que o concorrente não tem.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Capacidade negada no perfil é fato, nunca lacuna a interpretar.** Antes de escolher a mecânica do CTA, rode `grep -in 'automação\|automacao\|robô\|bot' <perfil do dono>` e cole a saída literal. Linha que diz `nenhuma automação` responde `não`, e ela não é omissão nem falso positivo a contornar. Cole `mecânica exige automação? sim/não · perfil declara: <a linha literal> · mecânica adaptada: <qual>`. Negação no perfil sai como CTA sem robô, e manter a mecânica por leitura funcional, herança de outra plataforma ou hábito presumido reprova a peça.

**O universo da R3 é o das unidades produzidas, nunca o dos pilares.** As `teses distintas` saem das pautas, headlines ou frames que a peça entrega, e a contagem igual ao número de pilares do dono é resultado inválido. Cole `unidades no lote: N · linhas em teses.txt: N`, os dois iguais, e só então a matriz de pares.

**`teses.txt` é arquivo obrigatório da pasta de saída**, uma tese de até 4 palavras por linha, ao lado do `conferencia/checagem-titulos.md`. Sem ele o gate não calcula a R3 e o campo do fecho sai com a instrução do script no lugar do número, o que reprova a entrega.

**A primeira decisão, em uma linha:** pedido ABERTO ("me dá headlines sobre X", "banco de headlines", sem número nem formato) entrega o **BANCO COMPLETO** (Ação 1, mínimo 50 fórmulas, 3+ headlines cada). Pedido ESPECÍFICO ("headline pra ESTE carrossel", "6 ganchos", formato ou quantidade dita) entrega **3 a 5 fórmulas com 2 a 3 headlines cada** (Ação 2).

**A regra que decide sem inferência: nomeou o formato-destino = peça única (Ação 2), sempre.** Se o pedido tem a palavra carrossel, capa, reel, story, anúncio, e-mail, assunto, YouTube ou título, o destino está dito e você cai na Ação 2, mesmo que o pedido pareça aberto no resto. "Headlines pra um carrossel sobre X" é Ação 2, não banco. Ação 1 só quando o pedido não nomeia nenhum formato E não dá quantidade. Na dúvida que sobrar, pergunta uma coisa só e mostra a tabela de roteamento abaixo como cardápio.

**Ordem de leitura, quando existe perfil do dono:** o perfil/brain do agente vem PRIMEIRO, antes do exemplo e antes de qualquer pergunta (o perfil pode responder sozinho o que você ia perguntar). Sem perfil, começa pelo exemplo.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra, num caso fictício de nicho neutro, a entrada que o dono deu, as perguntas que a skill fez e a saída real de cada ação: um grupo inteiro de banco renderizado, o pedido específico com os tetos contados, e a compressão da mesma fórmula em 4 formatos. Ler antes da primeira pergunta economiza uma rodada de retrabalho.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o tema e o que tem de dor e prova, e eu escrevo as headlines). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra a escrita com o que o dono já colou. Se faltar um insumo que a headline não vive sem (o assunto, ou a dor/verbatim que ela ancora), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez (o tema, a dor com as palavras do cliente, o formato/plataforma) e escreve com o que o dono for dando.

A pergunta do modo é UMA por pedido. As outras três partes entram nos passos abaixo:

- **Ensina enquanto faz:** ao escolher o gatilho e a família da fórmula, escreve UMA linha do porquê ("puxo pela família Mistério porque o tema tem uma virada que dá pra segurar; Recompensa entrega o benefício de cara, mas abre menos loop"), pra o dono aprender a decidir sozinho na próxima.
- **Puxa o material bruto:** quando a dor vier rasa ("meus clientes querem crescer"), não segue no genérico. Pede o concreto que só o dono tem: "me conta de UM cliente, o que ele te falou quando te procurou, com as palavras dele?", ou um número que aconteceu. Verbatim vira headline com âncora; resposta rasa vira headline rasa.
- **Oferece refinar no fim:** depois de mostrar as headlines, fecha com UMA linha de ajuste ("quer mais direto? outro gatilho? mais curto pro teto da plataforma? reescrevo só as que você marcar"), pra o dono saber que dá pra ajustar sem começar do zero.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "me dá headlines sobre X", "banco de headlines", "gera headlines pro meu nicho", "preciso de ideias de gancho" (sem número, sem formato) | **1 · BANCO COMPLETO** |
| "headline pra ESTE carrossel", "o gancho desse reel", "a capa dessa peça", "6 aberturas", "3 chamadas", qualquer quantidade ou formato dito | **2 · PEÇA ÚNICA** |
| "encurta essa headline pro reel", "cabe no assunto do e-mail?", "faz caber no título do YouTube", "comprime pra capa" | **3 · COMPRESSÃO POR FORMATO** |
| "minera benchmark de [tema]", "olha essas headlines que eu vi", "modela esse viral" | **4 · MINERAÇÃO** |

Pedido ambíguo ("me ajuda com a headline", "olha essa frase aqui"): pergunta UMA coisa só, o que a headline vai vestir (uma peça específica ou um banco pra escolher depois), mostra a tabela como cardápio e segue pela resposta.

## Os TETOS por formato (o alvo que o gate CONTA, fica no topo de propósito)

Plataforma não é família de gatilho: é teto de renderização. A mesma fórmula serve pra tudo, o que muda é quanto texto cabe. Onde os DOIS eixos aparecem, os DOIS têm que passar (uma capa de 12 palavras que dá 80 caracteres estoura e falha).

| Formato-destino | Teto em palavras | Teto em caracteres (com espaço) |
|---|---|---|
| Reel, 3s falados | ≤ 7 | n/a (é falado) |
| Reel, texto na tela | ≤ 5 | ≤ 40 por linha |
| **Carrossel, capa** (pedido que diz só "headline pra um carrossel", sem outro formato, cai AQUI: headline de carrossel é a capa) | **8 a 15** | **≤ 65 na linha-título (frase de maior peso)** |
| Stories, abertura | 5 a 10 | ≤ 50 na linha de topo |
| Anúncio, 1.7s falados | ≤ 5 | n/a (é falado) |
| Anúncio, 5s falados | ≤ 10 | n/a (é falado) |
| Email/Substack, assunto | 8 a 12 | ≤ 45 no assunto |
| Título de YouTube | n/a | 40 a 60 (mobile trunca em ~50) |

**Contagem:** número em algarismo conta 1 palavra ("40 anos" = 2); caractere = letra + espaço + pontuação. Quando o ambiente tiver shell, conta de fato: `echo -n "a headline" | wc -m` (caracteres) e `| wc -w` (palavras). Sem shell, vale a margem de segurança do gate (Passo 4).

## O perfil do dono vem do banco do agente

Onde esta skill precisa de voz, avatar, prova, mecanismo ou oferta: **leia do perfil/brain do agente quando existir**; se não existir, faça a entrevista curta descrita no "Sem o insumo" da ação e siga com o que faltar marcado `[DADO: confirmar]`. Nunca invente, nunca crie um arquivo de perfil, nunca pare por causa disso.

---

## Ação 1 · BANCO COMPLETO (o pedido aberto)

**O que faz:** entrega um banco de headlines organizado por família de gatilho, pro dono escolher e reusar o ano inteiro.

**Precisa de:** o tema/nicho, dito pelo dono · 3 a 5 falas de DOR e 3 a 5 de DESEJO do cliente, do perfil/brain do agente quando existir · o Mapa de Munição da Audiência (os 12 campos que alimentam os slots das fórmulas), do perfil/brain quando existir.

**Sem o insumo:** entrevista curta de 4 perguntas numa mensagem só: o nicho em 1 linha · 1 dor que o cliente fala com as palavras dele · 1 desejo que ele fala · o que a audiência dele já conhece (pessoa, ferramenta, instituição, técnica). Sem o Mapa, pergunta os 3 ou 4 campos mais críticos pro tema e segue; o que faltar vira `[DADO: confirmar]` e não conta como Ancorada.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `banco-headlines-[tema].md`, agrupado por família de gatilho, **mínimo 50 fórmulas com 3+ headlines cada**, cada grupo com T-número + família + fórmula em slots + gatilhos no topo. Se a ancoragem real só sustenta menos, entrega o que sustenta e DIZ quais faltaram e por quê. **STOP** pra escolha.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/templates.md` (o banco único, INTEIRO antes de escolher fórmula) · `references/comandos-rapidos.md` (a lógica de volume 50/100/200/300 e o protocolo de lotes).

**Profundidade:** `references/regua-final.md` (a régua integral e o cemitério) · `references/criterios-v2.md` (o gate com mais exemplo) · `references/dispositivos-de-frase.md` (o tempero da revisão) · `references/subcanones-formato.md` (a mesma fórmula em cada formato).

Passos: 0 (ancora) → 1 (assunto) → 2 (famílias e fórmulas) → 3 (2 a 3 headlines por fórmula) → 4 (gate por dentro) → 5 (mostra e PARA). Em banco grande, mostra uma amostra por seção no MEIO do caminho, não só no fim.

---

## Ação 2 · PEÇA ÚNICA (o pedido específico)

**O que faz:** entrega 3 a 5 fórmulas com 2 a 3 headlines cada, já comprimidas no teto do formato-destino, pra UMA peça.

**Precisa de:** a peça e o formato-destino (capa de carrossel, 3s de reel, topo de story, assunto de e-mail, título de YouTube), ditos pelo dono · a fala real do cliente sobre o tema, do perfil/brain do agente.

**Sem o insumo:** se o formato não foi dito, pergunta UMA coisa: "essa headline vai virar o quê, capa, reel, story, e-mail ou título?". Sem fala real, ancora em prova real do dono e marca todo número não confirmado como `[DADO: confirmar]`.

**Entrega:** `headlines-<slug>.md` (slug curto do tema ou da peça, sem espaço, ex.: `headlines-primeiro-cliente.md`), as 3 a 5 fórmulas agrupadas, cada uma com as 2 a 3 headlines já dentro do teto (palavras E caracteres CONTADOS). **STOP:** o dono escolhe UMA antes de qualquer corpo de peça ser escrito.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/templates.md` (escolhe as fórmulas por família e nota) · `references/subcanones-formato.md` (a renderização no teto do destino).

**Profundidade:** `references/amplificadores.md` (a frase de 0 a 2s antes da headline falada, no reel e no story) · `references/dispositivos-de-frase.md` · `references/regua-final.md`.

Quando o pedido é de VOLUME solto ("6 aberturas", "uns ganchos"), o conjunto cobre **pelo menos 4 dos 6 ângulos de ataque** (régua de cobertura, mais abaixo).

---

## Ação 3 · COMPRESSÃO POR FORMATO

**O que faz:** pega uma headline que já existe e a comprime pro teto de outro formato, sem perder o gatilho.

**Precisa de:** a headline atual, colada pelo dono · o formato-destino.

**Sem o insumo:** se o dono colou a headline mas não disse o destino, pergunta UMA coisa: "pra qual formato?". Se colou o destino mas não a headline, pede a frase.

**Entrega:** `headline-[formato].md` com a versão comprimida + a contagem dos dois eixos declarada + 1 alternativa. Comprimir é apertar a mesma fórmula, nunca trocar de gatilho nem cortar a ancoragem. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/subcanones-formato.md` (o protocolo de compressão, com a mesma fórmula renderizada nos 4 formatos).

**Profundidade:** `references/criterios-v2.md` (comprimento por formato com exemplos passa/falha).

---

## Ação 4 · MINERAÇÃO DE BENCHMARK

**O que faz:** transforma headlines que performaram lá fora em fórmulas novas do banco, com veredito de duplicidade contra o banco inteiro antes de aceitar qualquer uma.

**Precisa de:** o material bruto (as headlines que o dono viu, ou o tema pra buscar) · acesso à web quando a busca for ao vivo.

**Sem o insumo:** sem acesso à web, conduz com o que o dono colar; pede 10 a 20 headlines que ele viu funcionando e roda a dedup em cima delas. Nunca finge varredura que não aconteceu.

**Entrega:** o registro da rodada anexado a `references/mineracao-benchmark.md` e as fórmulas aprovadas somadas ao banco como EXTERNO, no fim da numeração, com a origem rastreada. **STOP** antes de somar qualquer fórmula ao banco.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/mineracao-benchmark.md` (metodologia, fontes, protocolo de dedup) · `references/modo-input-livre.md` (decodar um viral de outro nicho pra modelar).

---

## O fluxo (os passos que as 4 ações compartilham)

A decisão de ficar ou pular acontece em menos de 2 segundos. A abertura é 90% do jogo. A headline **filtra E atrai**: para o scroll de quem é cliente e instala a percepção que deixa a conversa mais quente depois. Ela não fecha venda (isso é na carta e no WhatsApp). Headline que só viraliza e atrai estranho falhou tanto quanto a que ninguém para.

> **Headline não se escreve: se encontra.** Ela é a linha que já está na cabeça do leitor quando ele reconhece uma dor, um desejo ou um absurdo que vive. O criativo é a headline de hoje: os 3 primeiros segundos precisam fazer essa linha aparecer na cabeça dele. Esta skill extrai essa linha da fala real, da cena e da tensão do leitor; o CORPO do criativo (o roteiro, o resto do anúncio) vive em `soft-conteudo-reels` e `soft-trafego-meta`.

**O que esta skill faz por você:** pega a fala real do teu cliente e encontra as linhas que ele já pensa, usando os teus templates testados (2-3 por template). A headline decide se a pessoa lê o resto, por isso vem antes do corpo.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa o contexto de você antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: confere se tem a fala/o número/o case antes de montar e, se faltar, marca `[DADO: confirmar]` no lugar do furo e diz o que falta, jamais preenche com algo plausível; (6) **doc de output enxuto pros 2 leitores**: o que sai é otimizado pro humano que lê E pra IA que recebe como contexto: só as headlines limpas + `[DADO: confirmar]`, zero meta-narração. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar qualquer headline.**

## Output Contract (o que você entrega)
**O banco VALIDADO é O BANCO ÚNICO POR GATILHO: 225 fórmulas T em 6 famílias de gatilho (Recompensa · Mistério · Crença · Disrupção · Popularidade/Reputação · Reconhecimento) + C1-C6 (ângulos ortogonais).** Numeração única e estável: T1-T30 mantêm o número histórico (com a família onde moram); T31-T86 são as fórmulas da Rodada 2; T87-T225 são as fórmulas de origem externa absorvidas (a antiga incubadora C9-C18 e o antigo banco secundário, marca-neutra), com a origem rastreada e o lastro marcado (CASA/EXTERNO). O banco inteiro, com nota FORTE/OK por fórmula, mora em `references/templates.md`, e é o que o banco completo usa. **A escolha é pela família e pela nota, FORTE primeiro** (peso igual entre CASA e EXTERNO; fórmula EXTERNO sai marcada com a origem na saída).
- **Pedido ABERTO, sem orientação específica** ("me dá headlines sobre X", "banco de headlines"): entrega o **BANCO COMPLETO no doc: no mínimo 50 fórmulas validadas, com PELO MENOS 3 headlines cada**, organizado **por família de gatilho** (nunca por plataforma). Cada grupo com **o T-número + a família + a fórmula (notação de slots) + os gatilhos** no topo. Se a ancoragem real só sustenta menos fórmulas com honestidade, entrega o que sustenta e DIZ quais faltaram e por quê (nunca inventa pra completar).
- **Pedido ESPECÍFICO** (formato, quantidade, "headline pra ESTE carrossel/reel"): obedece a orientação, escolhe 3-5 templates que encaixam, 2-3 headlines cada, com a mesma marcação de origem.
- **Toda entrega sai com as 3 melhores marcadas** (`★` na linha) e o bloco `As 3 melhores` no fim do doc, com 1 linha de porquê cada. Sem isso a entrega está incompleta.
- A saída é **limpa, no doc**. O gate roda **por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída.
- No pedido específico, você **para e espera** o cliente escolher antes de gerar mais. No banco completo, entrega o doc inteiro de uma vez e pergunta o que ajustar.
- Você **nunca inventa fala nem número do cliente** e **nunca mostra headline que falhou no gate**.


## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a peça no chat)
Regra dura, vale mesmo pra copy curta: o RESULTADO desta skill sai como **UM documento markdown consolidado**. Em ambiente que renderiza markdown, mostre o doc renderizado (o dono abre, copia, baixa); em ambiente com sistema de arquivo, salve como arquivo `.md`. A CONDUÇÃO (perguntas de contexto, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA/COPY em si mora no DOC. Ao parar num STOP, você mostra ou atualiza o DOC e pergunta "ajusto?"; você NUNCA reescreve a peça em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Passo 0, ancora antes de escrever (NÃO PULE)
Procura a fonte de fala real do cliente, nesta ordem: **descrição do projeto** → **Plano colado na conversa** → **mensagens anteriores**. Puxa **3-5 falas de DOR + 3-5 de DESEJO** do tema, literais, contando o N (quantas vezes apareceu). A primeira linha de cada headline nasce de uma delas, quase intacta.

Três estados de entrada (declara qual é o seu antes de escrever):
- **Tem fala real (com N):** ancora nela e cita o N. Caminho ideal.
- **Tem fala literal mas SEM contagem N:** estado válido, ACEITA e segue. Ancora na fala literal normalmente, conta como Ancorada=✓, e marca a contagem como `[N A CONFIRMAR]` ao lado da fala. Falta de N **não bloqueia** a entrega e não reprova a headline no gate; só o número inventado reprova.
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

**AS FÓRMULAS-ÂNCORA POR GATILHO (usa ESTAS, NUNCA invente uma fórmula genérica).** As 30 âncoras históricas (T1-T30) abaixo, seguidas das âncoras novas mais fortes da Rodada 2. Escolhe 3-5 que encaixam no assunto + na fala real, FORTE primeiro; preenche com elementos concretos e reais do cliente (adapta ao nicho, nunca copia o exemplo). **O BANCO ÚNICO completo, com as 225 fórmulas, a nota (FORTE/OK) e o lastro (CASA/EXTERNO) de cada uma, mora em `references/templates.md`, e é o que o banco completo usa.**

**Âncoras históricas T1-T30** (a coluna Gatilho é o que se rastreia na frase; a família de cada uma está em `templates.md`):

| # | Template (fórmula) | Exemplo | Gatilho |
|---|---|---|---|
| 1 | Faça algo muito específico (ordem direta + razão no corpo) | "Seja chato em 2026." | Autoridade + Disrupção |
| 2 | Coisas que eu [faço/deixei de fazer] sendo [autoridade] | "Cremes que eu não passo no rosto sendo dermatologista." | Autoridade |
| 3 | Coisas que parecem normais mas geram [dano] | "Alimentos que parecem saudáveis mas emperram seu intestino." | Disrupção |
| 4 | Esse é o maior motivo disso acontecer | "Esse é o maior motivo do seu carrossel não viralizar." | Mistério |
| 5 | Crença popular que você quer confrontar | "Comer ovo todo dia faz mal. É isso que falam, mas..." | Crença + Disrupção |
| 6 | O inimigo NOMEADO do nicho pôs a mão em tal coisa e ela mudou (inimigo sem nome é figura vazia: plataforma, banca, guru, algoritmo) | "A indústria pôs a mão no sorvete e ele mudou." | Disrupção + Crença |
| 7 | O inimigo NOMEADO adora quando você faz [ação concreta] | "O banco adora cliente que faz essas 4 coisas." | Reconhecimento + Disrupção |
| 8 | Demorei X anos pra aprender, te explico em X segundos | "Levei 8 anos de psicanálise pra descobrir isso. Resumo em 1 minuto." | Recompensa + Autoridade |
| 9 | Toda pessoa com [característica ultra específica] precisa saber disso | "Toda pessoa que tem casa de aluguel precisa saber disso." | Reconhecimento |
| 10 | [X] [coisas] que valem [medida concreta de valor] em [área] (a moldura "MBA" desgastou; medida com número real) | "3 livros que valem R$ 20 mil de consultoria em finanças." | Popularidade + Recompensa |
| 11 | Na próxima vez que você for [situação], faça isso | "Da próxima vez que for fechar um cliente, não faça reunião." | Recompensa + Valor prático |
| 12 | Coisas que transformam X em Y | "4 hábitos que transformam sua insônia no sono mais restaurador." | Recompensa |
| 13 | X é assim, Y é assim (contraste visual) | "O coração de um diabético é assim. O de uma pessoa normal é assim." | Disrupção |
| 14 | O que fazer quando [algo cotidiano acontece] | "O que fazer quando o cliente pede desconto na hora do fechamento." | Valor prático + Reconhecimento |
| 15 | Esse vídeo é um alerta para [pessoas com essa característica] | "Alerta para quem toma anticoncepcional há mais de 10 anos." | Reconhecimento + Mistério |
| 16 | O item mais subestimado tem esses benefícios | "A vitamina mais subestimada do Brasil custa R$12 e resolve insônia." | Mistério + Recompensa |
| 17 | Fazer [ação nomeada] gera essas consequências (a ação aparece na frase; só a consequência fica em loop) | "Pedir desculpa demais gera essas 3 consequências no casamento." | Recompensa + Reconhecimento |
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

**Âncoras novas da Rodada 2** (as mais fortes; 1 por linha, com T-número e família. O banco inteiro está em `templates.md`):

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

> **Regra dura:** as fórmulas do banco são as 225 de `references/templates.md` (T1-T225, nas 6 famílias). Se você escreveu um "template" fora do banco, você INVENTOU (é o erro a não cometer). No máximo adapta/combina ao nicho do cliente. `templates.md` traz todas com slots, exemplos, variações, a família, a nota (FORTE/OK) e o lastro (CASA/EXTERNO) de cada uma; escolhe pela família e pela nota, FORTE primeiro.

**Plataforma NÃO é família: é teto de RENDERIZAÇÃO.** A mesma fórmula serve pra qualquer formato; o que muda é quanto texto cabe. A tabela de tetos por formato está no gate (Passo 4); o protocolo de compressão (a mesma fórmula apertada pro teto de reel/YouTube/e-mail/capa) está em `references/subcanones-formato.md`. Não existe fórmula exclusiva de plataforma.

**Comandos rápidos:** "**minera benchmark de [tema]**" roda nova rodada de mineração com veredito de dedup contra o banco inteiro ANTES de propor fórmula nova (no app sem web, conduz com o material que o dono colar); o que passa entra no banco único como EXTERNO, no fim da numeração; registro em `references/mineracao-benchmark.md`. (A antiga incubadora C9-C18 foi absorvida no banco único como T87+; o comando "usa os candidatos" não existe mais, a nota e a marcação EXTERNO fazem o serviço.)

### Régua de cobertura de ângulo (camada de VARIAÇÃO, roda POR CIMA das fórmulas do cânone)
**Ângulo vs Gancho (a distinção limpa).** Ângulo = o TEMA central, sobre O QUE você fala. Gancho/hook = os primeiros segundos. O gancho é a EXPANSÃO do ângulo, não uma coisa curiosa caçada à parte: ângulo bom → o gancho sai dele (você não fica procurando hook; ele nasce do ângulo forte). Por isso o trabalho começa no ângulo. Existem DUAS camadas de ângulo, e elas não competem, empilham: o **ângulo de ABORDAGEM** (o tema, sobre O QUE a peça fala: descoberta científica, causa-raiz, contrária, pergunta paradoxal...) e o **ângulo de ATAQUE da frase** (C1-C6 abaixo, de que LADO psicológico a frase bate). Primeiro escolhe a abordagem, depois a fórmula T que veste, depois checa a cobertura de C-ângulos. A lista dos ~7 ângulos de abordagem validados de resposta direta, com exemplo e as T que servem, mora em `references/templates.md` (seção "Ângulos de ABORDAGEM"), e reforça o Cânone sem substituí-lo.

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
A copy nasce da terça-feira à noite DO LEITOR. Regra é CHECAGEM, nunca geradora: escreve a partir da CENA (a emoção dela: raiva, medo, absurdo, cobiça), com voz de mesa; a regra confere depois. Reprovou, REGENERA do zero (frase editada herda o esqueleto do defeito):
1. **Munição na mão:** verbatim/prova real do dono na frente (sem munição = pergunta, jamais inventa).
2. **Leitura única:** uma leitura em voz alta, sem re-parse; valência única (bom ou ruim na 1ª leitura); sintaxe linear; 1 operação mental por frase.
3. **Mundo do leitor, não o mapa do autor:** componentes do método viram dias, horas, lugares e falas do cliente; rótulo abstrato só entre aspas, como palavra do inimigo.
4. **Compressão gramatical: cota zero.** Verbo da relação por extenso; a força é do fato, nunca do aperto da frase.
5. **Voz de mesa, não palco:** a colocação inteira é fala real; metáfora morta entra, personificação e figura de escritor não.
6. **Prova com atribuição exata** (do banco de provas do dono, nunca fundir); conta apresentada como conta; renda do leitor só em 3ª pessoa.
7. **Anti-IA:** zero travessão longo (U+2014), zero da família do verbo-freio banida, zero verbo genérico de transformação, zero frase-emoldura.
8. **Teto do formato conhecido ANTES** (conta durante, não conserta depois).
Depois de escrita, a auditoria roda TODOS os filtros em cada linha (régua cumulativa, checklist mecânico). Reprovou, regenera ANTES de mostrar.

### PRINCÍPIO-MÃE + ordem de operação (a headline NASCE da cena; a régua só confere)
A headline nasce da terça-feira à noite DO LEITOR. Regra é CHECAGEM, nunca geradora: frase gerada de regra nasce limpa e morta. Frase reprovada NÃO se remenda, REGENERA do zero, cena primeiro (frase editada herda o esqueleto do defeito). **Ordem:** (1) cena com a emoção (raiva, medo, absurdo, cobiça) → (2) frase de mesa, com atitude → (3) template como esqueleto que arruma a cena → (4) checklist completo, mecânico, TODOS os filtros. A régua INTEGRAL (8 seções + cemitério + calibradores) mora em `references/regua-final.md`; a doutrina marca-neutra, em `shared-references/crivo/06-regua-de-escrita.md`.

**Calibradores (reprovada → aprovada; o padrão do defeito):**
- "Coisas que parecem dia rendendo..." (composto de laboratório) → "Coisas que enchem o teu dia mas não pagam o teu mês: responder direct é a primeira."
- "Demite 3 das tuas 4 estratégias" (verbo concreto, objeto abstrato) → "Cancela o lançamento do segundo semestre."
- "O 'vou pensar' morre no domingo" (personificação, figura de escritor) → "Quem te fala 'vou pensar' na sexta, na segunda já esqueceu teu nome."
- "Você tem permissão... desde que" (template pela casca; contrato, não alforria) → "A regra dos '6 meses gerando valor' foi inventada por quem vive do teu conteúdo grátis."

## Passo 3, encontra 2-3 headlines DENTRO de cada template
Pra cada template escolhido, encontra **2-3 headlines** que o leitor reconheceria como pensamento próprio, todas ancoradas na fala real (Passo 0). Estilo Soft: uma ideia por frase, número no lugar de adjetivo, vocabulário do cliente final (nunca "lead/funil/ticket"), tom de comando, nunca morno. **Clareza acima de tudo (Lei 1): nada de palavra difícil, nada de figura de linguagem vazia ("mensagem cheia"), só o que uma pessoa real diria.** A linha encontrada fica **curta e densa, reaproveitável em qualquer formato** (capa, reel, post, story). **Quando o formato-destino já é conhecido, comprime pra ele, respeitando OS DOIS eixos (palavras E caracteres com espaço):** reel falado ≤7 palavras nos 3s · reel texto na tela ≤5 palavras E ≤40 caracteres/linha · capa de carrossel 8-15 palavras E ≤65 caracteres na linha-título · story 5-10 palavras E ≤50 caracteres no topo · anúncio ≤5 palavras · email 8-12 palavras E ≤45 caracteres no assunto · YouTube 40-60 caracteres (mobile trunca em ~50). A tabela completa dos 8 formatos vai INLINE no Passo 4 (é o alvo que o gate conta); o protocolo de redução detalhado está em `references/criterios-v2.md`. **Tempero, só se a headline estiver chapada:** injeta 1 dispositivo de `references/dispositivos-de-frase.md` (preparação+virada, antítese, dizer o não-dito, evocação sensorial), nunca no lugar da ideia. No topo de cada grupo, declara o **template (nome/fórmula) + os gatilhos** que ele aciona. **Não narra o fluxo**, só entrega limpo, organizado por template.

## Passo 4, roda o GATE por dentro e IMPRIME a régua de títulos

**A régua de títulos R1 a R7 é entregável, não auditoria silenciosa.** O resto do gate (a tabela de checks) roda por dentro e não vai pro doc. A régua R1 a R7, não: ela sai **impressa no documento que o dono recebe**, num bloco próprio de título `## Régua de títulos (R1 a R7)`, colado depois das headlines. É a prova de que cada linha foi medida, e é o que deixa o dono conferir sozinho por que uma headline entrou e outra foi reescrita.

**A forma do bloco, sem exceção:** uma tabela com uma linha por headline e estas colunas, nesta ordem, `headline | R1 afirma a mais | R2 sumário? | R3 tese (4 palavras) | R4 inimigo ou inversão | R5 antítese | R6 ressalva | R7 assinaria | veredito`. O veredito é `passa` ou `reescrito de: <versão anterior>`. Célula vazia não existe: quando a regra não se aplica àquela headline, escreva `n/a` e o motivo em 2 palavras.

**As quatro contagens fecham o bloco, coladas:** `com inimigo ou inversão: N de N (mínimo metade)` · `em molde de antítese: N (teto 1)` · `teses distintas: N (mínimo 3)` · `assinaria: N · reescritas: N · sem resposta: 0`. **Além do bloco no documento, a checagem sai também no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega**, com as três contagens no fecho: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros têm que ser iguais, e qualquer diferença reprova: a régua não é amostra, e nome fixo é achável por `ls` enquanto seção no meio de outro documento não é.

**Checagem verificável antes de mostrar:** `grep -c 'afirma a mais' <doc>` devolve pelo menos 1 e `grep -c 'teses distintas' <doc>` devolve 1. **Entrega sem o bloco `## Régua de títulos (R1 a R7)` no documento reprova antes de qualquer análise de conteúdo**, por mais que as headlines estejam boas. Sem shell, confira a olho que o bloco existe, que ele tem uma linha por headline e que as quatro contagens estão escritas.


**Frase genérica se corrige com CENA, nunca com adjetivo.** Quando uma frase sobrevive à troca de nicho, a correção não é somar um adjetivo forte nem trocar o verbo: é **substituir o substantivo abstrato** (obstáculo, desculpa, consistência, movimento, plano, jornada, transformação) por uma cena que só existe neste negócio. As cenas estão nos insumos e não na sua cabeça: **liste as disponíveis ANTES de escrever**, rodando o grep abaixo sobre a pasta de insumos e colando a saída.

```
grep -rniE 'quando eu|toda vez que|no dia|a hora que|eu vi|eu percebi|me disse|escreveu' <pasta de insumos>
```

Cole a lista na forma `cena: <descrição em 6 palavras> | origem: <arquivo:linha>`, uma por linha, e marque quais foram usadas na peça. Feche com `cenas disponíveis: N · usadas na peça: N`. Peça com `usadas: 0` e insumos com cena disponível volta pro passo de escrita: a frase morna não é falta de talento, é a cena que estava no disco e ninguém abriu.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase. **O teste não é "a frase fica agramatical": é "a frase existiria sem o dado?".** Frase cuja única função é registrar a pendência ("Prazo exato do caso: [A CONFIRMAR: número de semanas]") está no miolo por definição e sai da peça, mesmo parecendo um campo. **Antes de marcar qualquer número, grepe os insumos (`grep -in '<termo>' <insumos>`) e cole a saída: dado que existe no disco nunca vira marcador.** Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**O corpo da peça contém só o que o destinatário lê.** Instrução dirigida ao dono ("confirme", "valide", "ajuste antes de publicar", "verifique com o conselho") vai no handoff ou no bloco de configuração, **nunca dentro de mensagem, slide, frame, bloco de página ou fala**: briefing impresso dentro do produto é o dono falando sozinho na cara do cliente. A ressalva de nicho que o destinatário precisa ler fica; a ordem de serviço pro dono sai. Checagem verificável, restrita às seções públicas: `grep -nE 'antes de publicar|confirme|valide|verifique com' <peça>` tem que voltar vazio.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova. **Divergência reprova a headline, não só o relato: o título sai do lote e a versão anonimizada ("uma aluna de 52 anos") toma o lugar dele.** Marcador de pendência ao lado do nome não é saída: ele registra a dúvida e não resolve o risco.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado, e a conta vem ANTES de escrever a peça.** Monte a conta em 3 passos e cole no processo: (1) `grep -c '^-' <perfil>` = C campos; (2) percorra os campos e escreva `campo <n>: <k> valores` para todo campo com k maior que 1, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1; (3) some, e M é o piso. Cole `campos no perfil: C · valores desdobrados: M · linhas do inventário: M`. **Inventário com menos de M linhas reprova sem análise de conteúdo, e a linha que agrupa dois dados conta como UMA linha e como N dados faltando.** A ordem é o que decide: a conta feita depois da peça vira justificativa, e a conta feita antes vira o alvo. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **O inventário varre o perfil do dono INTEIRO, não só os campos que esta entrega consumiu:** cada campo do perfil é uma linha, e campo com vários valores (paleta com 3 cores; oferta com preço, parcela, bônus e garantia) rende uma linha por valor. **Entrega cujo `Dados fornecidos: N` for menor que o número de campos do perfil recebido reprova sem análise de conteúdo.** Qualificar a linha ("relevantes ao objeto", "considerados para esta entrega") também reprova: o total é o total. **Onde a linha mora:** no arquivo que o dono lê. Quando a entrega é uma peça de copy publicável (headline, carrossel, slide, card, chat, roteiro, deck), a peça NÃO recebe a tabela: a tabela vai num arquivo irmão de handoff (`HANDOFF-<slug>.md`) e só a linha de fechamento fica na peça, no rodapé. Inventário só no relato de processo, sem a linha na entrega nem o handoff no disco, reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

Roda o gate em CADA headline. Só headline que passa em TODOS os critérios vai pro cliente. Uma falha refaz a frase (não o conceito). A tabela de checks abaixo é o teu **checklist interno**: o dono não recebe ela. O que ele recebe, além das headlines limpas, é o bloco `## Régua de títulos (R1 a R7)` descrito acima, que é obrigatório no doc.

### Os TETOS que o gate conta (a tabela está no TOPO desta skill)
O check "Teto físico do formato" manda CONTAR contra um alvo, e o alvo é a tabela "Os TETOS por formato" logo no topo deste arquivo. Onde os DOIS eixos aparecem, os DOIS têm que passar (uma capa de 12 palavras que dá 80 caracteres **estoura** e falha). Número sempre em algarismo ("3", nunca "três"): ocupa menos e lê mais rápido.

**MARGEM DE SEGURANÇA sem shell:** contar caractere de cabeça é impreciso e o erro típico é 15-30 caracteres pro lado do PASSA. Então trate o teto com FOLGA, não no fio: se a frase-título passa visivelmente de ~8-10 palavras OU tem 2 orações longas ("...na academia, mesmo sendo personal"), **presuma ESTOURO e comprime, nunca arredonde pra baixo pra caber**. Duas orações longas quase sempre quebram JUNTO o teto de caractere E o check "Curta e densa" (uma ideia por frase). Quando há shell (terminal ou agente), conta de fato: `echo -n "a headline" | wc -m` (caracteres) e `| wc -w` (palavras) antes de marcar ✓.

### A RÉGUA DE TÍTULOS (as 7 regras de excelência, rodam ANTES do resto do gate)

Estas 7 regras vêm antes dos checks da tabela, porque elas decidem se a headline existe. Todas são mecânicas: contagem, comparação colada ou pergunta com resposta escrita. Nenhuma depende de bom gosto. **As sete saem impressas no doc do dono**, na tabela do bloco `## Régua de títulos (R1 a R7)`; onde cada regra abaixo diz "no processo", leia "na coluna dela dessa tabela".

**R1 · Teste do enunciado (a primeira, sempre).** Cole o pedido do dono e a headline uma embaixo da outra e escreva, ao lado da headline, **o que ela afirma a mais que o pedido**. Prefixo genérico ("Como", "Por que", "5 formas de", "O guia de") sobre o enunciado do pedido NÃO é ganho. O ganho tem que ser um destes quatro: um inimigo nomeado, uma ordem invertida, um custo, uma troca. **Sem esse ganho escrito por extenso, a headline não entra no doc.** Checagem verificável: no processo, cada headline tem a linha `<headline> | afirma a mais: <o quê>`; headline com essa célula vazia reprova sozinha, por mais que passe em todos os outros checks.

**R2 · Proibido o título que só descreve o tema.** Checagem física: se a headline cabe como **título de índice, de sumário ou de aula** (rotula o assunto e para aí), ela reprova. Teste de 1 linha, colado no processo: "essa frase funcionaria como item de um sumário?" Se sim, reprova. "Voltar a treinar depois dos 40 sem dor no joelho" é sumário. "A academia esconde a ordem que protege joelho depois dos 40" não é.

Teste mecânico, uma linha por headline, colado na coluna R2: reescreva a headline como item de sumário de aula ("O que fazer quando X", "Como fazer Y", "Os N erros de Z"). **Se a reescrita ficar igual ou quase igual à headline, ela já era sumário e reprova.** Cole a reescrita ao lado, na mesma célula. Isso tira a decisão do gosto: o que decide é as duas frases ficarem parecidas.

**Headline que é o nome do método, a lista dos componentes do método, ou a promessa do perfil com um verbo na frente cai na R2** mesmo quando a reescrita de sumário parecer diferente. "Troque a pressa por força, mobilidade e progressão lenta" é a ficha do produto com um imperativo na frente. **Teste também apagando o verbo inicial, e se o que sobrar for a ficha do produto, reprova.** Cole na mesma célula: `sem o verbo inicial sobra: <o quê> · é a ficha do produto? sim/não`.

**R3 · Uma tese por headline, teses contadas por lote.** Escreva a tese de cada headline do lote **em no máximo 4 palavras**, numa lista. Duas teses iguais = as duas viram uma, e a segunda sai com log. **Lote de 4 fórmulas com menos de 3 teses distintas reprova o LOTE inteiro, não a headline.** Variar a fórmula não é variar o ângulo. **Contar linhas não é contar teses:** depois de escrever a tese de cada headline em 4 palavras, ordene a lista e compare cada tese com a seguinte, escrevendo `distinta de <anterior>: sim/não` e o porquê em 3 palavras. **Duas teses que compartilham sujeito E predicado (pressa cobra joelho / peso cobra joelho) contam como UMA**, ainda que a fórmula mude. `teses distintas: N` sem a lista ordenada não conta como feita.

**R4 · Inimigo nomeado ou ordem invertida, em pelo menos metade do lote.** As headlines fortes nomeiam um inimigo externo (instituição, prática, conselho comum, ferramenta) ou invertem uma ordem que o leitor toma como dada. As fracas nomeiam o tema. **Tema não é inimigo.** Checagem contada, colada no processo: `headlines com inimigo nomeado ou ordem invertida: N de N (mínimo: metade)`.

**R5 · Antítese telegráfica, cota contada.** Conte quantas headlines do lote usam o molde da negação seguida da virada afirmativa em duas orações curtas separadas por ponto (a forma "não é <isto>", ponto, "<é aquilo>"), ou duas orações curtas simétricas separadas por ponto. **Cota máxima: 1 por banco, e nunca duas em sequência.** Acima disso o lote volta pra reescrita mesmo com cada headline passando sozinha: a repetição do molde é o tell, não a frase.

**A coluna é obrigatória e entregável.** O bloco sai com uma linha por headline do lote no formato `<headline> | duas orações separadas por ponto? sim/não`, TODAS listadas, inclusive as que dizem não. Cole a contagem: `em molde de antítese: N (teto 1)`. Contagem sem essa coluna não conta como feita e reprova antes da análise de conteúdo. **Não existe "quase-antítese" nem cota transferida:** duas orações separadas por ponto em que a segunda contradiz, corrige ou completa a primeira contam 1, e variar a tese não isenta o molde.

**Com shell, a contagem NÃO é escrita de cabeça:** rode `python3 scripts/lint_copy.py <peça>`, leia a linha `molde de antítese: N (teto 1)` com o `<arquivo>:<linha>` de cada ocorrência, e cole a saída literal ao lado do seu número. **Divergência entre o número do lint e o declarado reprova o lote e manda de volta pro passo de escrita: o script é a autoridade.** **Mas rode o lint sobre os TÍTULOS, nunca sobre o documento inteiro:** a tabela da régua manda repetir cada headline na coluna R1, e o documento carrega ainda a saída do próprio lint, então lintar o arquivo inteiro conta a mesma headline três vezes e infla o número a cada rodada de conformidade. Salve as headlines num arquivo só delas (`grep '^- ' <peça> > /tmp/titulos.txt`) e rode `python3 scripts/lint_copy.py /tmp/titulos.txt`: é esse número que vale, e ele sai na forma `em molde de antítese (títulos): N (teto 1)`. **Nunca cole a saída do lint dentro do arquivo publicável:** ela vira ocorrência na contagem seguinte, e o lugar dela é o `conferencia/checagem-titulos.md` ou o relato. Quando o arquivo precisar mesmo citar a saída, ponha a citação dentro de bloco de código cercado e linte com `python3 scripts/lint_copy.py <arquivo> --ignore-code-blocks`, que apaga só o conteúdo do bloco e continua lintando o resto.

**R6 · Crivo clínico e regulado (saúde, dinheiro, corpo).** Headline que responda "sim / não / pode" sobre condição de saúde nomeada (hérnia, artrose, lesão, gravidez, cirurgia, diabetes, depressão) ou que prometa resultado de saúde, emagrecimento, cura ou ganho financeiro **só passa com a ressalva que o nicho pede DENTRO da própria frase ou na linha imediatamente abaixo dela no doc**, e só quando o dono tem prova daquela condição específica no banco de provas dele. A ressalva é a do conselho profissional que rege o nicho (CREF pra treino, CRN pra nutrição, CRM pra saúde, CRP pra psicologia, CFC e CVM pra finanças, OAB pra jurídico): quando o dono declarou o registro, a ressalva cita o registro; quando não declarou, a ressalva é de avaliação individual ("avaliação individual antes", "resultado varia por pessoa", "não substitui consulta"). **Sem prova da condição no banco do dono, a headline não é escrita: a pergunta do cliente vira convite pra conversa, nunca resposta afirmativa.** Pergunta real do cliente é ótima matéria-prima e não autoriza a resposta. Checagem: `headlines com afirmação de saúde ou dinheiro: N · com ressalva do nicho na peça: N (têm que bater)`.

**R7 · Assinatura de copywriter, com reescrita colada.** Pra cada headline, responda por escrito no processo: **"um copywriter de ponta assinaria esta linha?"**. Resposta "não" ou "não sei" **obriga a versão reescrita ao lado**, e é a reescrita que vai pro doc. Antes de responder, **leia a headline em voz alta**: frase que precisa de entonação de locutor pra funcionar não passa. Checagem: `assinaria: N · não assinaria (reescritas): N · sem resposta: 0`. **`reescritos: 0` num lote de abertura maior que 3 é proibido sem a linha do título mais fraco.** Escreva as headlines, rode a régua, e reescreva as que não forem um sim inequívoco ANTES de montar a tabela, com a versão morta colada em `reescrito de: <anterior>`. Se depois de reescrever a coluna ainda for zero, escreva em uma linha por que nenhuma precisou, **nomeando a headline mais fraca do lote e por que ela sobreviveu**; sem essa linha o lote volta pro passo de escrita (`shared-references/crivo/07-regua-de-titulos.md`, R7).

**Nome de caso em capa só com autorização registrada.** Antes de pôr nome de pessoa ou prazo de caso numa capa, rode `grep -n 'autorizado por' <insumo>` e `grep -n 'A CONFIRMAR' <insumo>` e cole as duas saídas. **Sem a primeira, o nome sai da headline** e entra a forma por faixa ("uma aluna na casa dos 50"), nunca a inicial solta. Com a segunda apontando o número, o número vira "algumas semanas". Marcar a pendência e publicar a capa com o nome mesmo assim reprova (`shared-references/crivo/08-consentimento.md`).

**Gatilho nomeado, obrigatório em toda headline.** Nenhuma headline sai sem o gatilho escrito ao lado dela no processo e a família declarada no topo do grupo, no doc. T-número e família não bastam: o grupo declara **quais dos 7 gatilhos a frase aciona** e o gate exige mínimo 3 dos 7 gatilhos rastreáveis na própria frase. Declarar o gatilho obriga a escrever para ele.

**Contagem física obrigatória, nos dois eixos, colada.** Com shell, `wc -w` e `wc -m` em cada headline, com o resultado ao lado da linha no doc. Sem shell, vale a margem de segurança do gate: duas orações longas presumem estouro.

**As 3 melhores marcadas no doc.** Toda entrega desta skill fecha com as **3 melhores headlines do lote marcadas** (uma marca visível, tipo `★`, na linha da headline) e, no fim do doc, o bloco `As 3 melhores` com **1 linha de porquê cada uma**, nesta forma: `★ <headline> | por que: <o motivo: o gatilho que ela aciona e o que ela afirma a mais>`. Uma linha, não um parágrafo. Entrega sem as 3 marcadas e sem os 3 porquês está incompleta. Quando o lote tem menos de 3 headlines aprovadas, marca as que houver e diz por que não deu 3.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Régua de títulos (R1 a R7)** | as 7 regras acima passaram E o bloco `## Régua de títulos (R1 a R7)` está impresso no doc do dono, com uma linha por headline e as quatro contagens. **Qualquer uma delas em falha, ou o bloco ausente do doc, reprova antes de qualquer outro check** | |
| **Ancorada** | nasce de fala literal da fonte (cita N **real**) OU de prova real do autor; **fala literal sem contagem passa: marca `[N A CONFIRMAR]` e vale ✓**; **N inventado/plausível = ✗ automático**; fecha em chão/número/cena, não em tese solta bonita | |
| **Gatilhos rastreáveis** | **mínimo 3 dos 7 gatilhos rastreáveis na frase; menos de 3 = ✗**, e "no espírito" não conta | |
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
| **Anti-IA (HARD)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz, o verbo que rima com "cravar" e suas flexões (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype (o "revoluciona/transforma" e o próprio verbo-freio banido) · **repetição paralela idêntica em série (a mesma casca sintática 2-3x seguidas, tipo "...é assim. Com Y é assim.") também é tell**; em T13/T28 varia a estrutura, não copia a moldura. **Com shell disponível, roda `python3 scripts/lint_copy.py` no arquivo de headlines e é ELE que decide este item: ele pega o que o olho perde, como o travessão longo colado e flexões do verbo-freio que não são a forma mais óbvia. Sem shell, faz o CTRL+F manual do travessão longo (U+2014 e U+2013) e da família do verbo-freio antes de marcar ✓.** | |
| **VIDA (tensão/absurdo)** | tem tensão, absurdo, força ou visceralidade; dá pra sentir no corpo; algo em jogo DENTRO da frase (custo, medo ou desejo com nome). **Frase limpa mas MORTA = ✗ mesmo passando em todo o resto** | |
| **Valência única + 1 operação** | leitura única sem re-parse; o leitor sabe na 1ª leitura se é bom ou ruim (valência única); sintaxe linear (sujeito-verbo-objeto, zero oração encaixada); 1 operação mental só (uma cena OU um contraste OU uma conta já resolvida, nunca duas) | |
| **Compressão cota ZERO** | verbo da relação por extenso ("gente que te segue há 2 anos", nunca "seguidor de 2 anos"); todo pronome com dono óbvio; corte de cinema diz quem fala. Aperto de frase NÃO é fonte de força, a força é do fato | |
| **Concretude (mundo do leitor)** | componentes do método viram dias/horas/lugares/falas do cliente; rótulo abstrato só entre aspas, como palavra do inimigo; **verbo concreto + objeto abstrato ("demite a estratégia") = concretude falsa, ✗**; ordem executável só sobre objeto que o leitor POSSUI hoje | |
| **Voz de mesa** | a colocação inteira é fala real numa mesa; metáfora morta entra ("a venda morre", "ficou no vácuo"), personificação e figura de escritor não ("o 'vou pensar' morre no domingo"); licença poética cota 1-2 por lote de 30, sinalizada | |
| **Template = movimento** | template é movimento psicológico, não casca; a instrução do molde nunca vaza literal pra frase ("pôs a mão em X"); culpa no desenho ou no timing, nunca no caráter do leitor | |
| **Densidade (CONTADA, R3)** | escreva a tese de cada headline em 4 palavras, numa lista colada no processo; duas teses iguais = a segunda sai com log. **Lote de 4 fórmulas com menos de 3 teses distintas reprova o lote inteiro**, não a headline | |
| **Prova (atribuição exata)** | número do banco de provas do dono com atribuição exata, nunca fundir (o número de A jamais aparece como de B); [CONTA] apresentada sempre como conta, nunca faturamento realizado; renda do leitor só em 3ª pessoa; camada do dono: zero preço/garantia/oferta em conteúdo | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

### META-REGRAS do processo (valem no lote inteiro, não só na frase)
- **Régua CUMULATIVA:** filtro novo nunca substitui os velhos. A passada FINAL roda TODOS os filtros em cada linha, em modo checklist, nunca só os frescos. (O pêndulo, otimizar o feedback novo quebrando a conquista anterior, foi o erro mais repetido.)
- **Cemitério de conceitos:** ideia reprovada pelo dono não ressuscita de roupa nova. A lista de mortos vive na seção "Cemitério" de `references/regua-final.md`; quando o dono reprova, a entrada É ADICIONADA lá e passa a fazer parte do gate.
- **Auto-lupa antes do dono:** aponta as próprias dúvidas do lote ANTES da auditoria dele (a whitelist mental deixa passar o próprio vício).
- **Dono no loop no MEIO:** em varredura grande (banco de 50/100/200), amostra por seção no meio do caminho, não só no fim. A régua garante o piso; o olho do dono constrói a régua.

## Passo 5, lê em voz alta, marca as 3 melhores, mostra e PARA
**Antes de mostrar, leia cada headline em voz alta** e marque a que você não diria numa mesa: frase que só funciona com entonação de locutor volta pro Passo 3 e regenera do zero. Esse é passo do fluxo, não conselho.

Depois, **marque as 3 melhores do lote** com `★` na linha delas e escreva, no fim do doc, o bloco `As 3 melhores` com 1 linha de porquê cada (o gatilho que aciona + o que afirma a mais que o pedido). É o que dá ao dono uma recomendação, não só uma lista.

Mostra **só as que passaram, agrupadas por template, LIMPO** (no DOC, nunca solto no chat): cada grupo com o **template nomeado + os gatilhos** no topo e as 2-3 headlines embaixo, com a contagem dos dois eixos ao lado de cada uma. Depois dos grupos, o doc leva o bloco `## Régua de títulos (R1 a R7)` do Passo 4, com a tabela e as quatro contagens. Nada da tabela de checks do gate, nada de meta sobre o processo: o que entra é a régua, e ela entra porque é prova, não porque é bastidor.

**As duas checagens de disco antes de mostrar, com as saídas coladas no processo:** (1) `grep -c 'Régua de títulos' <doc>` devolve pelo menos 1; (2) numa Ação 2 (peça única de copy publicável), `ls <pasta>` mostra o `HANDOFF-<slug>.md` e `grep -c 'Dados fornecidos' <peça>` devolve 1. Qualquer uma das duas vazia, a entrega volta pro Passo 4 antes de chegar ao dono. Pergunta "quais te servem? ajusto, troco de template, ou gero mais?". **Espera a escolha** antes de gerar volume ou passar pro corpo (soft-conteudo-carrossel / -reels / -stories).

## COMO ENTREGAR (o banco de headlines vira doc MD)
O resultado (as headlines agrupadas por template) é o entregável, e o cliente quer GUARDAR ele. Entrega como **documento markdown**: em ambiente que renderiza markdown, mostre o doc renderizado (o banco que ele abre, copia e reusa); em ambiente com sistema de arquivo, salve como arquivo `.md`. Num agente de mensageria: gera o banco como arquivo `.md` e cita o path completo na resposta (o canal anexa), com a condução em mensagens curtas, sem markdown pesado (sem `##`, sem tabela). A condução (perguntas, escolha de template, o gate por dentro) acontece no chat; o **banco de headlines sai como doc**, agrupado por template, não só solto no meio da conversa. Volume (banco de 50/100/200/300) é SEMPRE doc.

## O que esta skill NÃO faz (e pra onde vai)

Esta skill entrega a PRIMEIRA LINHA e para aí. Em toda rota abaixo, se a skill de destino não estiver instalada, esta faz o mínimo aqui e diz o que fez.

| O pedido é | Vai pra | Se não estiver instalada |
|---|---|---|
| Os **slides/corpo do carrossel** depois da capa | **soft-conteudo-carrossel** | escreve aqui 5 linhas-tese, uma por slide, e avisa que o arco completo mora lá |
| O **roteiro do reel** depois do gancho | **soft-conteudo-reels** | escreve aqui a espinha em 4 marcações e avisa |
| A **sequência de frames de story** | **soft-conteudo-stories** | escreve aqui 3 frames em texto na tela e avisa |
| **Adaptar** uma peça pronta pra outra plataforma | **soft-conteudo-multiplataforma** | comprime só a headline pro teto do destino (Ação 3) |
| Decidir **sobre o que postar** (tema, pauta, matriz do mês) | **soft-conteudo-planner** | pergunta o tema ao dono e segue com o que ele disser |
| **Posicionamento, pilares, mecanismo, avatar** | **soft-plano-posicionamento** | roda a entrevista curta de 4 perguntas da Ação 1 e marca `[DADO: confirmar]` |
| **Arte, PNG, visual** da capa | **soft-designer** | entrega só o texto e diz que a arte fica pendente |
| **Abertura de VSL ou carta** | **soft-funil-carta** | escreve a linha e avisa que o corpo da carta é outra peça |
| **Abertura da aula do webinar** | **soft-webinar** | escreve a linha e avisa |

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
| Inventou uma fórmula genérica (não é uma fórmula do banco) | Usa as fórmulas T do banco único por gatilho (`templates.md`); adapta ao nicho, nunca cria fórmula do zero |
| Organizou o banco por plataforma (reel/YouTube/e-mail) | Organiza por FAMÍLIA de gatilho; plataforma é só teto de renderização (comprime a mesma fórmula) |
| Entregou as headlines só soltas no chat, sem doc | O banco sai como doc MD (renderizado ou arquivo `.md`, conforme o ambiente); o chat é a condução |
| Apresentou fórmula EXTERNO como testada da casa | Fórmula EXTERNO (T87-T225) sai sempre marcada com a origem; vira CASA SÓ com baseline batido em 2+ peças reais do dono (a promoção troca o campo, não o número) |
| Alegou "todas dentro do teto" sem contar | O teto é CONTADO (palavras E caracteres); declarar conformidade sem contagem é gate falso, o erro mais grave |
| Banco "completo" com menos de 50 templates, calado | Ou entrega os 50+ validados, ou DIZ quais faltaram e por quê (ancoragem insuficiente); nunca entrega menos em silêncio |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `shared-references/crivo/07-regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta (a entrada do dono, as perguntas feitas e a saída real de cada ação). **Leia antes da primeira pergunta.**
- `references/regua-final.md`: **A RÉGUA INTEGRAL** (as 8 seções calibradas em 6 rodadas: Vida · Clareza · Concretude · Voz · Template · Prova · Anti-IA · Meta-regras) + o **Cemitério de conceitos** (vivo: entra aqui quando o dono reprova) + os **calibradores completos** (pares reprovada → aprovada). É o miolo do gate do Passo 4, com toda a evidência. A doutrina marca-neutra da qual ela deriva está em `shared-references/crivo/06-regua-de-escrita.md`.
- `references/templates.md`: **O BANCO ÚNICO POR GATILHO completo** (as 225 fórmulas T nas 6 famílias, cada uma com nota FORTE/OK e lastro CASA/EXTERNO, com a gramática de slots no topo, os exemplos multi-nicho, as variações fundidas, as notas de refinamento e a regra de promoção EXTERNO a CASA) + a numeração C1-C6 dos ângulos de ataque de frase + os **ângulos de ABORDAGEM** (a camada de tema/grande-ideia que roda por cima, com causa-raiz na frente em saúde). **Central nos Passos 2-3.**
- `references/subcanones-formato.md`: **renderização por formato** (a MESMA fórmula comprimida pro teto de cada formato, com o exemplo de uma fórmula renderizada nos 4 formatos e a evidência de cada teto). Plataforma não é família, é camada de renderização. A tabela de tetos está inline no gate (Passo 4).
- `references/mineracao-benchmark.md`: o registro das rodadas de mineração (metodologia, fontes, dedup) e o protocolo do comando "minera benchmark de [tema]".
- `references/criterios-v2.md`: o detalhamento do gate do Passo 4 (rastreabilidade física dos 7 gatilhos + exemplos passa/falha por nicho + comprimento por 8 formatos). É o mesmo gate, com mais exemplo, não um segundo sistema.
- `references/comandos-rapidos.md`: lógica de volume (50/100/200/300) e protocolo de lotes do "banco de [tema]".
- `references/modo-input-livre.md`: decodar um viral de outro nicho pra modelar.
- `references/amplificadores.md`: as frases curtas que precedem a headline no reel falado/story.
- `references/dispositivos-de-frase.md`: o repertório de tempero (preparação+virada, âncora do cotidiano, dizer o não-dito, evocação sensorial, antítese) que realça a headline na revisão, depois da ideia de pé. **Dirigido no Passo 3.**
- `scripts/lint_copy.py`: com shell disponível, roda `python3 scripts/lint_copy.py` no arquivo de headlines e ele substitui o CTRL+F, não é só cinto extra (reprova o travessão longo e a família do verbo-freio). Sem shell, aí sim vale o CTRL+F manual do gate.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
