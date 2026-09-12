---
name: soft-funil-nutricao
description: >-
  Escreve a RÉGUA DE NUTRIÇÃO pronta pra subir: a sequência de mensagens que pega o lead depois que ele baixou a isca e o aquece até o convite, com o dia, o canal e o trabalho de cada toque. Use quando o pedido for: "régua de nutrição", "o que mandar depois que a pessoa baixou", "sequência pós-isca", "aquecer o lead", "minha lista está parada", "escreve as mensagens de reativação da base fria", "e-mails de aquecimento", "sequência de WhatsApp", "o lead sumiu depois da isca", "quantas mensagens mandar". NÃO use pra: campanha de e-mail puro, boas-vindas, pós-venda ou win-back (soft-email-sequencia); DECIDIR a jogada do mês (soft-vendas-estrategias); régua de DENTRO do webinar, pós por percentual assistido (soft-webinar); sequência de carrinho (soft-launch); régua do mini-webinar (soft-funil-miniwebinar); o ATIVO da isca (soft-funil-isca); página de captura ou obrigado (soft-funil-landing); carta ou VSL (soft-funil-carta); calendário de feed (soft-conteudo-planner). Leia e siga o fluxo inteiro do SKILL.md.
---

# Nutrição, a ponte entre a isca e o convite

O lead baixou a isca e some. Esta skill escreve o que vem depois: a régua de mensagens que aquece esse lead até ele aceitar o convite, com o dia de cada toque, o canal, o trabalho que cada mensagem faz e o gate que reprova a que não passa.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**A lei-mãe:** nutrição **não vende, aquece até o convite**. Ponte curta, uma isca, uma promessa, um destino. Quem vende é o webinar, a carta ou a conversa; a nutrição entrega o lead quente lá. Newsletter sem destino envelhece a lista.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as 4 ações numa régua completa de caso fictício: o bloco de configuração, os 6 toques com dia e canal, o desvio de temperatura, o arco de reativação e o checklist de subida. Ler antes da primeira pergunta economiza uma rodada de retrabalho.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola tudo que tem sobre a base e o convite e eu escrevo a régua). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou. Se faltar um insumo que a régua não vive sem (a isca que veio antes, o convite pra onde ela leva, quem é a base), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez, e monta a nutrição com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda a régua (a rota por temperatura, o número de toques, o ritmo, o convite), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a decidir sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("minha lista", "os leads de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: a frase literal que um lead respondeu, o que mais segura a base antes de comprar, um número da última régua. Material bruto vira a âncora dos toques; resposta rasa vira nutrição rasa. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar a régua, fecha com UMA linha: "Quer mais toques? Outro ritmo? Convite mais suave? Me diz o que ajustar que eu refaço só essa parte." A oferta de refino não substitui o STOP nem o gate.


## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "régua de nutrição", "o que mandar depois que baixou", "sequência pós-isca", "aquecer o lead", "como levar quem baixou pro webinar" | **1 · RÉGUA PÓS-ISCA** |
| "esse lead já foi na call e não fechou", "tem gente quente e gente fria na mesma lista", "o que mandar pra quem respondeu" | **2 · ROTAS POR TEMPERATURA** |
| "minha lista está parada", "base fria", "reativar", "faz meses que não mando nada" | **3 · REATIVAÇÃO** |
| "manda um aviso pra base", "broadcast", "abri turma nova, avisa todo mundo" | **4 · BROADCAST** |
| "monta o funil de nutrição inteiro" | **1, depois 2, depois 3 se houver base velha, com parada em cada** |

Pedido ambíguo ("me ajuda com a nutrição", "o lead some depois da isca"): pergunta UMA coisa só, **"pra onde você quer levar essa pessoa depois?"**, mostra a tabela acima como cardápio e segue pela resposta.

## Como ler cada ação

Toda ação abaixo traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de posicionamento, avatar, voz, oferta ou prova: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" da ação e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

**Duas regras que valem em toda ação:** cliente sai de toda régua de aquisição (o filtro "já comprou?" roda na entrada de todo disparo), e nenhum número, caso ou fala entra sem fonte.

---

## Ação 1 · RÉGUA PÓS-ISCA (a sequência que aquece até o convite)

**O que faz:** escreve a sequência completa que pega o lead no download e o entrega no destino, mensagem a mensagem, com dia, canal e trabalho de cada toque.

**Precisa de:** o **destino** (webinar, call ou oferta direta), perguntado ao dono · o **nome e a promessa da isca** que o lead consumiu, do material da isca ou do dono · a **crença-ponte** que ela instalou · **3 a 5 falas de dor e 3 a 5 de desejo**, literais, com o N, do perfil/brain do agente · a **prova real** e o **ticket** · o **canal** que o dono usa de verdade (WhatsApp, e-mail, Instagram Direct, ou a combinação; Direct é canal de régua, não substituto informal, e tem régua própria em `canais-e-cadencia.md`).

**Sem o insumo:** entrevista curta de 7 perguntas, uma por vez (o que a pessoa baixou e o que você prometeu · pra onde você quer levar ela · o que você vende e por quanto · a frase que ela fala no pior do problema · que prova real você tem · WhatsApp, e-mail, Direct do Instagram ou mais de um · **se o destino for call, quantas conversas por semana ele atende de verdade e como a pessoa agenda hoje**). Sem destino declarado, assuma **call/conversa** (é o destino que aceita o lead mais frio sem queimar a base), marque `[A CONFIRMAR: destino]` e faça a pergunta 7 mesmo assim: destino call sem capacidade de atender vira oferta direta ou webinar gravado. **E a régua pós-isca é ativo perpétuo: ela roda todo mês, e o destino datado tem que declarar a sucessão.** Quando o destino for evento datado (aula, turma, live), cole `destino datado: <data> · o que a régua vira depois dessa data: <literal>`. Sem essa linha, o destino sai permanente (call, conversa, página) e o evento datado entra como colisão no checklist de subida: régua que aponta pra 29/09 fica sem destino no dia 30, e ninguém percebe até o lead cair numa página morta. Diga em 1 linha qual premissa assumiu. Sem fala literal, ancore em prova real do dono e avise que minerar 5 a 8 falas deixa a régua bem mais afiada; com 1 fala só, encolha a régua pra 4 toques em vez de reciclar a mesma fala (Seção 6 de `intake-e-destino.md`).

**Antes de escrever qualquer cena com pessoa, rode o passo de nomes.** A pessoa citada costuma ser justamente quem vai ler a peça. Rode antes da primeira linha da abertura:

```
python3 scripts/checar_titulos.py --peca <cada entregável> \
  --insumos <pasta de insumos do dono> --perfil <perfil do dono>
```

Ele imprime `nomes candidatos achados pelo script: N` e, por nome, `autorização no insumo: sim/não` e `mensagem privada: sim/não`. **Nome com `mensagem privada: sim` e `autorização: não` sai da peça** e vira a forma por faixa ("uma aluna na casa dos 50"). Lead com pergunta sem resposta nunca vira cena de abertura. Cole `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada: 0`.

**O marcador é campo, e campo tem tamanho.** Na peça pública ele cabe em `[A CONFIRMAR: <o dado>]`, no máximo 6 palavras, depois de um rótulo e no fim da linha. **O porquê da pendência nunca entra na peça**, vai pro handoff com o número da linha ao lado. O script conta e reprova acima do teto, em `marcadores acima de 6 palavras: N (teto 0)`.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**O convite e a entrega da isca nunca saem em marcador, e são a linha que cada toque serve.** A entrega da isca no D+0 é o único trabalho daquela mensagem: marcador no lugar do link a esvazia inteira. O texto do convite vem, nesta ordem: (1) da ação que o dono já usa nos insumos, achada por `grep -rniE 'manda |chama |responde |comenta |envia ' <insumos>` com a saída colada; (2) da ação nativa do canal principal do perfil; (3) do convite ao evento datado. Sem nenhuma das três, sai na forma que dispensa o link (`me chama no WhatsApp e eu te mando o link`), nunca em marcador. **Campo de template e marcador de pendência são coisas diferentes:** `[LINK]`, campo de uma palavra no FIM da linha e substituível por colagem, fica na frase; `[A CONFIRMAR: link]` é pendência, mora no bloco de configuração e no handoff, nunca no meio da linha que o lead lê. Cole `convites na peça: N · com ação escrita: N · em marcador: 0` e `toques com marcador ocupando linha do corpo: 0`.

**O nome do mecanismo do problema passa pelo teste do nicho trocado, como qualquer título.** Cole `mecanismo do problema: <nome> | substantivo trocado: <original> → <outro mercado> | sobrevive à troca de nicho? sim/não`. **`sim` volta pro passo de nomear**, porque um mecanismo que serve pra qualquer mercado não explica este: "recomeço acelerado" sobrevive trocando treino por dieta, por estudo e por carreira, e por isso não é mecanismo, é rótulo. O nome sai do substantivo concreto do caso (o dia 12, o joelho que decide, os 78 que sumiram), nunca do adjetivo do comportamento.

**Sem o NOME da isca, pergunte antes de escrever a primeira mensagem, e não escreva sem resposta.** Toda mensagem da régua cita a isca pelo nome, então nome ausente contamina a régua inteira. Pergunte numa única mensagem duas coisas: **(a) qual o nome exato da isca**, como o lead viu na página e no arquivo, e **(b) 3 seções, capítulos ou passos reais do material**, com o título de cada uma. Com isso cada toque referencia um pedaço concreto do que ele consumiu, em vez de falar do material no genérico. Se o dono responder o nome mas não as seções, escreva com o nome e marque `[A CONFIRMAR: seções do material]` no toque que dependia delas.

**Entrega:** `regua-nutricao.md`, com o bloco de configuração no topo (isca, crença-ponte, destino, temperatura, canais, cadência, filtro de saída, furos), as mensagens uma a uma com dia e canal, e o checklist de subida no fim. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/intake-e-destino.md` (INTEIRO, antes de perguntar qualquer coisa) · `references/sequencia-pos-isca.md` (a grade D+0 a D+7 e os 6 moldes).

**Profundidade:** `references/canais-e-cadencia.md` (quando o dono usa os dois canais) · `references/gate-linha-a-linha.md` (o critério de cada check).

**Os passos:**
1. Declare o estado de entrada e crave o **destino** e a **temperatura** (`intake-e-destino.md`, Seções 1 a 4). Sem destino, não escreve.
2. Monte o **bloco de configuração** (Seção 7 da mesma ref). Ele é a configuração da régua, não enfeite.
3. Escolha a grade: 6 toques em 7 dias é o padrão; webinar com data encolhe pra 4 ou 5 em 3 a 5 dias; oferta direta estica pra 5 a 7 em 7 a 10 dias.
4. Escreva **um toque por vez**, pelo molde da Seção 4 de `sequencia-pos-isca.md`. Cada toque faz UM trabalho e cita a isca pelo nome.
5. Rode o **gate por dentro** em cada mensagem (Ação 5). Mensagem reprovada é refeita, não a régua inteira.
6. **STOP.** Mostre a régua limpa mais o checklist de subida, pergunte "te serve? ajusto, ou sigo?" e espere o OK.

---

## Ação 2 · ROTAS POR TEMPERATURA (frio, morno, quente)

**O que faz:** desenha a ramificação que manda cada lead pro caminho certo, pelo comportamento que ele teve, e escreve as mensagens de cada rota.

**Precisa de:** a régua base da Ação 1 (ou o destino declarado, no mínimo) · os **sinais que o dono consegue registrar** de verdade na ferramenta dele (abriu, clicou, respondeu, foi na call), perguntados a ele · nas rotas morna e quente, a **objeção real** que o dono ouve dos leads que não fecham.

**Sem o insumo:** se o dono não sabe quais sinais a ferramenta dele registra, use os três que qualquer ferramenta pega (respondeu, clicou, comprou) e monte a ramificação só com eles, marcando `[A CONFIRMAR: sinais disponíveis]`. Se ele não sabe nomear a objeção da rota quente, use as três que aparecem quase sempre (preço, tempo, confiança) e faça o toque 4 ser a pergunta de 1 palavra que devolve a objeção na voz do lead.

**Entrega:** `rotas-temperatura.md`, com o desenho da ramificação em bloco (a árvore de entrada, trilhas e saídas) mais as mensagens de cada rota. **STOP por rota.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/rotas-por-temperatura.md` (as 3 rotas, os sinais e a ramificação da Seção 6).

**Profundidade:** `references/sequencia-pos-isca.md` (a rota fria reusa a grade padrão) · `references/canais-e-cadencia.md` (a rota quente é 1:1 manual, não automação).

**Os passos:**
1. Defina cada temperatura por **comportamento observável** (Seção 1 da ref). Palpite não vale.
2. Escreva a **rota fria** como padrão, a **morna** curta (3 a 4 toques em 4 a 5 dias) e a **quente** manual, com uma objeção por mensagem.
3. Monte a tabela de **sinais de subida e descida** (Seção 5). Lead que responde sai da automação, sempre, no mesmo dia.
4. Desenhe tudo como **UMA ramificação** (Seção 6), não como três sequências soltas que ninguém configura.
5. Rode o gate por dentro. **STOP** por rota.

---

## Ação 3 · REATIVAÇÃO de base fria (60 dias ou mais)

**O que faz:** escreve o arco que acorda a lista parada por pergunta e utilidade, e faz a poda que protege a entrega.

**Precisa de:** há quanto tempo a base está parada e **de que isca ou origem** ela veio, perguntado ao dono · o **tamanho da base** e se houve algum disparo recente · o destino atual (pode ser diferente do que existia quando ela entrou).

**Sem o insumo:** se o dono não sabe a origem da base, abra o toque 1 pela pergunta de 1 palavra mesmo assim, sem citar isca nenhuma, e use a resposta pra segmentar. Se ele não sabe o tamanho, escreva o arco e coloque no checklist a instrução de **volume gradual** (começa pelos que pararam há 60 a 90 dias, vê a resposta, só então avança).

**Entrega:** `reativacao.md`, com os 3 a 4 toques em 10 dias, a pergunta de 1 palavra, o toque de corte e as regras de higiene. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/reativacao-e-broadcast.md`, Seção 1 (o arco, os moldes e a higiene).

**Profundidade:** `references/canais-e-cadencia.md` (a cadência da base fria é mais espaçada e o WhatsApp só entra com opt-in vivo) · `references/gate-linha-a-linha.md`.

**Os passos:**
1. Abra pela **pergunta de 1 palavra**, nunca por oferta. Oferta de cara na base fria é o caminho pro spam.
2. Toque 2 entrega utilidade sem pedir nada. Toque 3 convida. Toque 4 corta.
3. Escreva as regras de higiene junto: volume gradual, remoção de quem não reagiu, hard bounce fora, e quem marcou spam nunca volta.
4. Rode o gate. **STOP.**

---

## Ação 4 · BROADCAST (o toque avulso pra base)

**O que faz:** escreve a mensagem única fora da régua automática, depois de checar que ela tem motivo real pra existir.

**Precisa de:** a **notícia**, em 1 frase, do dono · o **recorte** de quem recebe · o link do destino.

**Sem o insumo:** se o dono não consegue dizer a notícia em 1 frase, ele não tem broadcast. Diga isso em 1 linha e ofereça a Ação 1 no lugar (o que ele quer costuma ser uma régua). Se ele não sabe o recorte, corte por isca consumida ou por temperatura, nunca a base inteira.

**Entrega:** `broadcast.md`, a mensagem única mais as 4 checagens registradas. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/reativacao-e-broadcast.md`, Seção 2 (o que autoriza, as 4 checagens, o molde de 4 linhas).

**Profundidade:** `references/canais-e-cadencia.md` (frequência e colisão).

**Os passos:**
1. Rode as **4 checagens** antes de escrever: motivo real, filtro de cliente, colisão com régua ativa, recorte certo.
2. Escreva pelo molde de 4 linhas: a notícia primeiro, o que ela muda, o link sozinho, a saída.
3. Confira a frequência: no máximo 1 por semana pra mesma base, nunca dois em dias seguidos. Se precisa de mais, é régua.
4. Rode o gate. **STOP.**

---

## Ação 5 · O GATE (roda por dentro, em toda ação, e não imprime)

**Régua de títulos (roda antes do resto do gate).** Todo título que sai desta skill passa pela régua `shared-references/crivo/07-regua-de-titulos.md`, R1 a R7. Rode a régua sobre a primeira linha de cada toque da régua de nutrição, que é o assunto funcional da mensagem, o que decide se ela é lida ou ignorada. A checagem sai colada num arquivo do disco que o dono abre, uma linha por título, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a entrega antes da análise de conteúdo. **O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento). Palavra fora dessa lista não é gatilho e não conta**: o assunto com dois desses fica com zero gatilhos rastreáveis e volta pro passo de escrita. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase. **O teste não é "a frase fica agramatical": é "a frase existiria sem o dado?".** Frase cuja única função é registrar a pendência ("Prazo exato do caso: [A CONFIRMAR: número de semanas]") está no miolo por definição e sai da peça, mesmo parecendo um campo. **Antes de marcar qualquer número, grepe os insumos (`grep -in '<termo>' <insumos>`) e cole a saída: dado que existe no disco nunca vira marcador.** Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`. **A busca vira contagem, não promessa:** cole `marcadores na peça: N · com grep colado: N · com grep vazio: N`, e marcador sem a saída do grep ao lado reprova a peça, porque o dado que a transcrição responde não pode virar pendência no WhatsApp de ninguém.

**O corpo da peça contém só o que o destinatário lê.** Instrução dirigida ao dono ("confirme", "valide", "ajuste antes de publicar", "verifique com o conselho") vai no handoff ou no bloco de configuração, **nunca dentro de mensagem, slide, frame, bloco de página ou fala**: briefing impresso dentro do produto é o dono falando sozinho na cara do cliente. A ressalva de nicho que o destinatário precisa ler fica; a ordem de serviço pro dono sai. Checagem verificável, restrita às seções públicas: `grep -nE 'antes de publicar|confirme|valide|verifique com' <peça>` tem que voltar vazio.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Molde endereçado a pessoa nomeada exige o insumo dela aberto:** rode `grep -n '<Nome>' <insumo>` e cole a saída antes da fala, na forma do bloco "Fala atribuída ao destinatário" de `shared-references/crivo/08-consentimento.md`. Fala atribuída sem trecho literal do insumo reprova. Cole `moldes com nome próprio: N · com fala literal do insumo: N`, os dois iguais.

**Dentro do bloco de copy só existe campo, e campo é substituível por colagem sem reescrever a frase.** Rode e cole a saída:

```
grep -oE '\[[^]]*\]' <bloco de copy> | awk '{print NF, $0}'
```

**Qualquer colchete com mais de 3 palavras dentro do bloco reprova a abordagem.** Cole `campos no bloco: N · com mais de 3 palavras: 0 · instruções movidas pro bloco de preparo: N`. O `checar_titulos.py` conta o marcador acima de 6 palavras e reprova ali; dentro do bloco de copy o teto é mais apertado, e são 3.


**A régua é escrita na primeira pessoa do dono, sempre.** A mensagem sai do número dele e é lida como conversa: "eu", "te", "você". **Terceira pessoa sobre o dono dentro do corpo de um toque reprova o toque** ("a Renata trabalha há 9 anos" vira "eu trabalho há 9 anos"), porque assinar em terceira pessoa transforma conversa em anúncio e o lead percebe na primeira linha. Antes de fechar, rode `grep -n '<nome do dono>' <peça>` e classifique cada ocorrência: nome do dono dentro do corpo de um toque só passa em assinatura ou no primeiro toque, quando o lead ainda não sabe com quem fala. Cole `toques: N · em primeira pessoa: N · com o dono em terceira pessoa no corpo: 0`.

**Verbatim do perfil não é o que ESTE destinatário escreveu.** A mensagem 1:1 chega a alguém que talvez só tenha baixado um PDF, e a fala que mora no perfil do dono é a descrição que ele faz das clientes dele, não uma frase desta pessoa. **Fórmula proibida: "você escreveu", "como você me disse", "você mesma falou"** sobre fala vinda do perfil e não da conversa com esta pessoa. Use a forma de grupo ("é o que eu mais escuto") ou descreva a cena sem atribuir. Checagem colada: para cada fala entre aspas na mensagem, `<fala> | origem: <arquivo:linha> | atribuída a: <quem> | esta pessoa disse isso? sim/não`; **um "não" com atribuição direta reprova a mensagem.**

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado, e a conta vem ANTES de escrever a peça.** Monte a conta em 3 passos e cole no processo: (1) `grep -c '^-' <perfil>` = C campos; (2) percorra os campos e escreva `campo <n>: <k> valores` para todo campo com k maior que 1, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1; (3) some, e M é o piso. Cole `campos no perfil: C · valores desdobrados: M · linhas do inventário: M`. **Inventário com menos de M linhas reprova sem análise de conteúdo, e a linha que agrupa dois dados conta como UMA linha e como N dados faltando.** A ordem é o que decide: a conta feita depois da peça vira justificativa, e a conta feita antes vira o alvo. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**O piso do inventário é contável e a conta vai colada.** Rode `grep -c '^- ' <perfil>` e cole a saída do comando: esse número é o PISO BRUTO. Depois desdobre toda linha que carrega mais de um valor (a oferta com preço, parcela, 3 bônus e garantia conta 6, não 1) e cole `piso bruto: N · desdobrados: M · Dados fornecidos: N+M`. **`Dados fornecidos` menor que o piso bruto reprova a entrega**, porque significa que a peça descartou campo sem registrar o motivo. Não qualifique a linha com recorte de escopo: o total é o total, e o filtro de relevância mora na coluna de destino de cada dado, nunca no total.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


**O que faz:** reprova a mensagem que não serve, antes de o dono ver.

**Precisa de:** a mensagem escrita (assunto e corpo) e o bloco de configuração da régua.

**Sem o insumo:** o gate sempre tem o que precisa, porque ele lê o que você acabou de escrever.

**Entrega:** nada. O gate é auditoria silenciosa; a tabela **nunca** vai pra saída. O que sai é a mensagem limpa.

**Leia primeiro:** `references/gate-linha-a-linha.md` (o critério de cada check, com exemplo ruim e bom).

**Profundidade:** `shared-references/filtro-anti-ia/padroes-banidos.md` e `shared-references/filtro-anti-ia/falsos-positivos.md` · `shared-references/crivo/03-gate-cub.md`.

**Como roda:** em **cada** mensagem, assunto e corpo. **O veredito é o PIOR item**, e um ✗ refaz a mensagem, não a régua.

Os 3 checks próprios, que mais reprovam:
1. **UM destino:** a régua inteira empurra pra um destino declarado. Dois destinos reprova.
2. **Referencia o ativo:** toda mensagem cita pelo nome a isca que ELE consumiu ou o sinal que ELE deu. Mensagem que serviria pra qualquer lista reprova.
3. **Frequência declarada:** a cadência está escrita no bloco de configuração e a régua cumpre.
4. **Placeholder repetido na copy final:** proibido. O mesmo `[nome da isca]`, `[seção do material]` ou colchete equivalente aparecendo em mais de uma mensagem reprova a régua inteira: é o sinal de que o insumo faltou e a skill escreveu por cima dele. Ou você tem o nome e o escreve, ou você para e pergunta (o "Sem o insumo" da Ação 1). Um `[A CONFIRMAR: o quê]` isolado, num ponto onde o dono precisa mesmo decidir, continua valendo; o que reprova é o mesmo furo repetido como se fosse texto.

Mais os herdados, binários: **um trabalho só** · **temperatura certa** · **canal certo** · **não vende, aquece** · **ancorada** em fala literal com N ou prova real · **furo marcado** em `[A CONFIRMAR: o quê]` · **C/U/B** · **CTA com destino** · **anti-IA**.

**Com shell disponível, rodar `python3 scripts/lint_copy.py` sobre o arquivo de entrega é obrigatório, não opcional:** é ele que decide o item anti-IA do gate, e ele pega o que o olho perde. Sem shell, faça a busca manual pelos dois bloqueios duros: o travessão longo (U+2014 e U+2013) e a família do verbo-freio banida pela régua anti-voz (o verbo que rima com "cravar" e as flexões dele). Vale pro arquivo inteiro, inclusive as notas `[A CONFIRMAR]`.

---

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Régua de DENTRO do webinar (24h antes, link da sala, pós por percentual assistido) | **soft-webinar** | escrevo os 3 lembretes de comparecimento com o marco parametrizado |
| O ATIVO da isca (o PDF, o checklist, o quiz) | **soft-funil-isca** | descrevo a promessa e o sumário, não produzo o material |
| Página de captura, de obrigado, de entrega | **soft-funil-landing** | escrevo só o texto do bloco, sem a arquitetura de página |
| Carta de vendas ou roteiro de VSL | **soft-funil-carta** | não faço. O convite da régua aponta pra ela |
| Script de venda, objeção ao vivo, fechamento | **soft-vendas-closer** | escrevo a mensagem de passagem pro 1:1, não o script da conversa |
| Calendário e peças de feed | **soft-conteudo-planner** | não faço |
| Headline ou gancho isolado | **soft-conteudo-headlines** | escrevo o assunto do e-mail dentro da régua |
| Posicionamento, avatar, mecanismo nomeado | **soft-plano-posicionamento** | uso a entrevista curta de 6 perguntas da Ação 1 |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `shared-references/operacao-padrao.md` (as leis de operação) · `shared-references/crivo/` (ancoragem no verbatim, simulação do cliente, gate C/U/B) · `shared-references/filtro-anti-ia/` (os padrões banidos e os falsos positivos) · `scripts/lint_copy.py` (o anti-IA em código, rode no shell quando o ambiente permitir).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **O lint é gate com código de saída, não relatório.** Rode `python3 scripts/lint_copy.py <todos os .md da entrega>; echo "exit=$?"` e cole a linha `exit=` no relatório. **`exit` diferente de 0 proíbe a entrega:** volte pro passo de escrita, conserte e rode de novo, até sair 0. Declarar que rodou o lint sem colar o veredito não conta como gate cumprido. E a frase de fecho entra na varredura junto com o resto: o CTA é o texto que mais se repete no pacote, então um molde banido ali se multiplica por todos os arquivos e pelos dados que alimentam qualquer gerador. Cole `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Passo 2 da checagem (fecho, roda por comando)

Depois de gravar todos os entregáveis, rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída. Ele exige o `conferencia/checagem-titulos.md` na pasta, confere o inventário (os 4 inteiros, o piso e o `inventário duplicado`), o universo dos títulos, o marcador acima de 6 palavras, o nome de conversa privada, a `saída do script reescrita` e o lint de todo `.md`, RELATO incluso. **`exit` diferente de 0 reprova a entrega inteira, antes da análise de conteúdo.**
