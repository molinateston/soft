---
name: soft-funil-quiz
description: >-
  Projeta o FUNIL DE QUIZ que segmenta e vende: as perguntas na ordem certa, a árvore de segmentação (os buckets), os resultados personalizados por perfil e a oferta conectada a cada resultado, com a captura do lead no meio do caminho. O princípio é ASK (Ryan Levesque): a copy pergunta antes de vender, em vez de adivinhar. Use quando o pedido for: "monta um quiz", "quiz que vende", "funil de quiz", "perguntas pra segmentar", "quiz de diagnóstico", "que tipo de X você é", "quero descobrir o perfil do meu lead antes de oferecer". NÃO use pra: a PÁGINA/render do quiz, o hero, os botões, o visual de cada tela (soft-funil-landing no tipo quiz, que só renderiza); a carta ou VSL de venda (soft-funil-carta); a régua de mensagens pós-captura (soft-funil-nutricao); a isca em PDF (soft-funil-isca); posicionamento, avatar e oferta do zero (soft-plano-posicionamento); carrossel, reel e headline solta (soft-conteudo-*). Leia e siga o fluxo inteiro do SKILL.md.
---

# Funil de quiz, o ativo que pergunta antes de vender

O quiz é a forma escalável de perguntar. O lead cai numa página, responde de 4 a 7 perguntas e, em vez de receber a mesma oferta que todo mundo, recebe um resultado que fala com a situação exata dele. Enquanto ele responde, o funil descobre em qual perfil ele cai (o bucket), captura o e-mail ou o WhatsApp no ponto certo, e liga o resultado à oferta que resolve o problema daquele perfil. É o oposto da oferta única pra todo mundo.

Esta skill projeta o CÉREBRO do quiz: as perguntas, a lógica de segmentação, os resultados e a conexão com a oferta. Quem desenha a página onde isso roda é a soft-funil-landing.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem o arquivo do quiz MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Título de pergunta e de resultado nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Cada pergunta do quiz é um título e passa pela régua, e o resultado de cada bucket também.** Pergunta e título de resultado são o que o lead lê antes de decidir continuar; um rótulo genérico ("Pergunta 1", "Seu resultado") não segura ninguém. A pergunta autoexplicável passa no teste do estranho: alguém que caiu na página sem contexto entende o que está sendo perguntado e por que responder. Cole `perguntas produzidas: N · passadas pela régua: N` e `resultados produzidos: N · passados pela régua: N`, iguais dois a dois.

**A oferta de cada resultado é conferida contra o que a operação entrega hoje, e essa conferência é um PASSO com saída obrigatória.** Antes de ligar um bucket a uma oferta, rode `grep -rniE '<a oferta e cada bônus ligados àquele bucket>' <insumos>` e cole a saída inteira. O resultado não promete pro perfil nada que o dono não entregue: bônus, prazo ou formato que aparecer numa reclamação, cobrança ou registro de falha recebe uma decisão escrita, e são só duas: **sai do resultado** (e a pergunta ao dono no handoff explica por quê) ou **fica no resultado** (e o handoff traz `prometido no resultado e em falha na operação: <item> · <arquivo:linha>`). Cole `ofertas por resultado: N · conferidas nos insumos: N · em falha: N · decididas: N`, com `decididas` igual a `em falha`. Resultado que promete o que a operação não cumpre escreve a próxima reclamação daquele perfil.

**Número medido do perfil entra literal no resultado.** Trocar um número medido por um vago (`dezenas`, `várias`, `muitas`) reprova, porque perde a prova sem ganhar ressalva. O vago só entra onde o perfil marca `[A CONFIRMAR`. Cole `provas nos resultados: N · com número literal do perfil: N · vagas: 0`.

**Número marcado `[A CONFIRMAR` no perfil não entra no quiz, com ou sem ressalva ao lado.** Rode `grep -nE '\[A CONFIRMAR' <perfil>` e cole a saída. Para cada número que voltar, o resultado usa a forma sem prazo (`depois de algumas semanas`, `ao longo do protocolo`) e o número fica só no arquivo de notas. A ressalva ao lado do número não conserta o número, ela documenta que ele foi publicado assim mesmo, e o lead lê o número primeiro. Cole `números não confirmados no perfil: N · publicados no quiz: 0`.

**A fronteira que não pode vazar:** o quiz aqui é **conteúdo e lógica**, as perguntas, os buckets, os resultados, a ligação com a oferta e o ponto de captura. A PÁGINA/render do quiz (o hero, cada tela, os botões, a barra de progresso, o visual) é da **soft-funil-landing** no tipo quiz. Aqui é o que o quiz diz e como ele segmenta; lá é como ele aparece na tela.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra o fluxo inteiro num caso fictício de nicho neutro: o objetivo declarado, os buckets, as perguntas com o propósito de cada uma, os resultados por perfil, a oferta ligada a cada um e onde o lead é capturado. A mecânica ASK, a lógica de perguntas e a árvore de segmentação estão em `references/metodo-quiz.md`.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você me diz o que o quiz precisa vender e quem é o público, e eu monto as perguntas, os perfis e os resultados). Se quiser ser guiado passo a passo (te pergunto uma coisa de cada vez, do objetivo aos resultados) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou e com o brain dele. Se faltar um insumo que o quiz não vive sem (a oferta-destino, quem é o público, os perfis de cliente), pergunta AQUELE insumo e segue, sem voltar pro briefing inteiro.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o levantamento curto uma pergunta de cada vez, e monta o quiz com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda o quiz (quantos buckets, a ordem das perguntas, o ponto de captura, o ângulo de cada resultado), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a calibrar sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("meu cliente quer resultado", "o público de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: a frase literal que um cliente falou na dor, os perfis reais que ele já percebe na base, um caso com número. Verbatim real vira a âncora das perguntas e dos resultados; resposta rasa vira quiz raso. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar o quiz, fecha com UMA linha: "Quer menos perguntas? Outro perfil? Captura mais cedo? Me diz o que ajustar que eu refaço só essa parte." A oferta de refino não substitui o STOP nem o gate.

## Contrato de saída (o que sai, e onde cai)

- **Um arquivo `.md` nomeado**, salvo no disco: `quiz-<tema>.md`, com o quiz completo: as perguntas na ordem, a árvore de segmentação (que resposta leva a que bucket), os resultados por perfil, a oferta ligada a cada resultado e o ponto de captura do lead. Se o ambiente renderizar markdown, mostre também.
- **De 3 a 5 buckets**, nem menos nem mais. Menos de 3 não segmenta (vira oferta única disfarçada); mais de 5 pulveriza e o dono não consegue escrever oferta pra cada um. O número sai do avatar do dono, não do gosto.
- **De 4 a 7 perguntas.** Cada uma serve pra (a) segmentar OU (b) gerar identificação, nunca pra decorar. Pergunta sem propósito sai.
- **A captura do lead tem um ponto declarado**, não um default silencioso. O padrão é capturar ANTES de mostrar o resultado (o lead responde, deixa o contato, e aí recebe o diagnóstico), porque o resultado é a recompensa que paga o contato. O dono pode mover, e o motivo entra numa linha.
- **Entrega etapa por etapa**, com parada pro OK a cada uma. Nunca despeja o quiz inteiro de primeira.
- **Nunca inventa fala, caso, número ou perfil.** Sem prova real, o trecho sai como `[A CONFIRMAR: prova]` e a peça não sai como pronta. Perfil de cliente que o dono não confirmou vira `[A CONFIRMAR: perfil]`.
- **O quiz é arquivo publicável e não tem seção de bastidor, nem marcada.** Pendência, substituição de link, decisão editorial e a nota do conselho profissional vão em `notas-confirmacao.md`, entregue ao lado. Checagem: `grep -nE '^#+.*(dono|não publicar|nao publicar|bastidor)' <quiz>` tem que voltar vazio.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "monta um quiz", "quiz que vende", "funil de quiz", sem mais detalhe | **1 · OBJETIVO**, depois **2**, **3** e **4** |
| "quiz de diagnóstico", "que tipo de X você é" | **1** com o tema já dado, depois **2**, **3** e **4** |
| "já sei os perfis, só quero as perguntas" | **2 · SEGMENTOS** pra confirmar os buckets, depois **3 · PERGUNTAS** |
| "já tenho o quiz, faz os resultados" | **4 · RESULTADOS**, com os buckets confirmados na entrada |
| "olha esse quiz aqui e diz o que está errado" | **5 · GATE** em modo auditoria, devolve o diagnóstico por fase |

Pedido ambíguo ("preciso de um quiz"): pergunte UMA coisa só, **"o quiz vai levar o lead pra qual oferta no fim?"**, e a resposta ancora tudo.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de posicionamento, avatar, mecanismo nomeado, voz, oferta ou prova: leia do perfil/brain do agente quando existir; se não existir, faça o levantamento curto do "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

**As 6 leis de operação** (detalhe em `shared-references/operacao-padrao.md`, Seção 0): (1) cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**; (6) **doc de saída enxuto pros 2 leitores**, zero meta-narração, só o insumo denso mais `[A CONFIRMAR]` onde falta.

---

## Ação 0 · ANCORAGEM (roda antes de tudo, não pula)

**O que faz:** abre a fonte de fala real e puxa a matéria-prima das perguntas e dos resultados.

**Precisa de:** a fonte, nesta ordem: descrição do projeto → posicionamento do dono → mensagens anteriores. De lá saem **3 a 5 falas de DOR e 3 a 5 de DESEJO**, literais, com o N. As perguntas de identificação nascem dessas falas, quase intactas: uma pergunta que ecoa a dor na voz do próprio cliente é a que ele responde.

**Sem o insumo:** três estados, declare o seu em 1 linha.
- **Tem fala real com N:** ancora nela e cita o N.
- **Tem nicho e prova, zero fala literal:** não invente. Ancore em prova real do dono. Número não confirmado vira `[A CONFIRMAR: número]`; perfil que o dono não confirmou vira `[A CONFIRMAR: perfil]`.
- **Sem nada:** pergunte numa mensagem só (nicho em 1 linha, 1 dor real, a oferta-destino) e siga.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data, nome ou perfil e etiquetar.

**A captura do lead nunca sai em marcador, e o campo do formulário vem da ação nativa do canal do dono.** O ponto de captura (e-mail, WhatsApp) vem, nesta ordem: (1) do canal que o dono já usa nos insumos, achado por `grep -rniE 'whatsapp|e-mail|email|direct|telefone' <insumos>` com a saída colada; (2) do canal principal do perfil. Sem nenhum dos dois, sai na forma que dispensa o link (`deixa seu WhatsApp e eu te mando o resultado`), nunca em marcador. Campo de template (`[LINK]`, no fim da linha, substituível por colagem) fica na frase; `[A CONFIRMAR: link]` é pendência, mora no bloco de configuração e no handoff. Cole `pontos de captura no quiz: N · com canal escrito: N · em marcador: 0`.

**Entrega:** nada de arquivo. É a matéria-prima das ações 3 e 4.

**Leia primeiro:** `shared-references/crivo/01-entrada-verbatim.md`.

---

## Ação 1 · OBJETIVO (num bloco só, e espera resposta)

**O que faz:** crava pra que serve o quiz. Sem saber a oferta-destino, o quiz não tem pra onde levar o lead, e vira entretenimento que não vende.

**Precisa de:** a oferta que o quiz vai vender no fim (o produto, o ticket), e o que o dono quer descobrir sobre o lead pra vender melhor. Se veio do posicionamento com esses dados, confirme em 1 linha e pule.

**Os 3 campos base:**
- **(a)** a **oferta-destino**: o que o lead compra depois do quiz, com o ticket. Uma oferta só, ou uma oferta com variações por perfil.
- **(b)** o **que muda a venda por perfil**: o que o dono precisa saber sobre o lead pra oferecer o ângulo certo (o nível de experiência, a dor dominante, a situação, o momento). É isso que o quiz vai medir.
- **(c)** a **dor central** nas palavras do cliente, não em jargão. É dela que nascem as perguntas de identificação.

**Sem o insumo:** sem (a) o quiz não avança. **PARA e espera.** Sem (b) ou (c), faça o levantamento curto e siga com o que faltar marcado.

**Entrega:** 1 linha declarada: `objetivo: segmentar por <o quê de (b)> pra vender <oferta de (a)>`. **STOP.**

**Leia primeiro:** `references/metodo-quiz.md`, a seção da mecânica ASK.

---

## Ação 2 · SEGMENTOS (os buckets, a árvore)

**O que faz:** define os 3 a 5 perfis de cliente que o quiz separa, e o que muda na oferta ou na mensagem pra cada um.

**Precisa de:** o objetivo da Ação 1, o avatar do dono, e a lógica ASK (perguntar pra descobrir o bucket).

**Sem o insumo:** sem os perfis do avatar, **PARA e pergunte só isso**: "quais 3 a 5 tipos de cliente você já percebe na sua base, e o que muda no que você oferece pra cada um?". Perfil que o dono não confirma vira `[A CONFIRMAR: perfil]`, nunca inventado.

**Entrega:** a lista de buckets, cada um com nome, o cliente que cai nele e o ângulo de oferta que resolve o problema dele. **STOP.**

**Leia primeiro:** `references/metodo-quiz.md`, a seção dos buckets e da árvore de segmentação.

**Cada bucket tem oferta ou ângulo distinto, senão não é bucket.** Dois perfis que recebem a mesma oferta pelo mesmo ângulo são um perfil só com dois nomes: junta. O bucket existe porque a venda muda pra ele. Cole `buckets: N · com ângulo de oferta distinto: N`, iguais.

**O nome do bucket passa pelo teste do estranho e do nicho trocado.** O perfil sai da situação concreta do cliente (a experiente que parou, a iniciante com medo, a que já tentou tudo), nunca do adjetivo vazio ("a determinada", "a guerreira"). Um nome que serve pra qualquer mercado não descreve este cliente. Cole `buckets: N | por nome: sobrevive à troca de nicho? sim/não`, e `sim` volta pro passo de nomear.

---

## Ação 3 · PERGUNTAS (a ordem, o propósito de cada uma)

**O que faz:** escreve as 4 a 7 perguntas na ordem certa, cada uma com o propósito declarado.

**Precisa de:** os buckets da Ação 2, as falas da Ação 0.

**Sem o insumo:** sem os buckets não há como saber o que cada pergunta precisa medir. Volta pra Ação 2.

**Entrega:** as perguntas na ordem, cada uma com as opções de resposta e o propósito (segmenta pra qual bucket, ou gera identificação). **STOP.**

**Leia primeiro:** `references/metodo-quiz.md`, a seção da lógica de perguntas.

**Cada pergunta serve pra segmentar OU pra identificar, e o propósito é declarado.** Pergunta que não empurra o lead pra um bucket nem cria o "ela me entende" é decorativa e sai. Cole, por pergunta, `pergunta N | propósito: segmenta pra <bucket> ou identificação`. Pergunta sem propósito reprova.

**A ordem começa fácil e afunila.** A primeira pergunta é a mais fácil e a mais de identificação (o lead se reconhece e continua); as de segmentação mais fina vêm depois, quando ele já está dentro. Abrir com a pergunta que exige o lead se classificar num perfil espanta quem ainda não confia. Cole `perguntas: N · de identificação no início: sim/não`.

**Cada opção de resposta leva a um bucket, e a árvore fecha.** Toda combinação de respostas cai em exatamente um perfil, sem beco sem saída. Cole a árvore: que resposta (ou combinação) leva a que bucket, e confirme que todo bucket tem pelo menos um caminho que chega nele. Cole `buckets: N · com caminho de resposta que chega: N`, iguais.

---

## Ação 4 · RESULTADOS (o diagnóstico por perfil, a oferta ligada)

**O que faz:** escreve o resultado personalizado de cada bucket: nomeia a dor dele, aponta o caminho e liga na oferta certa pra ele.

**Precisa de:** os buckets da Ação 2, as perguntas da Ação 3, a oferta da Ação 1.

**Sem o insumo:** não há resultado sem bucket e sem oferta ligada.

**Entrega:** `quiz-<tema>.md`, salvo no disco, com o quiz completo: perguntas, árvore, um resultado por perfil e a oferta ligada a cada um, mais o ponto de captura. Se o ambiente renderizar markdown, mostre também. **STOP.**

**Arquivos obrigatórios: o arquivo acima, e `conferencia/checagem-titulos.md` por último** (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`). Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/EXEMPLO-FIM-A-FIM.md` (o quiz completo do caso Renata, a peça de referência pra calibrar densidade e tom).

**Cada resultado nomeia a dor daquele perfil e aponta o caminho, não elogia.** O resultado que só diz "você é a Guerreira, parabéns" não vende. O bom resultado espelha a situação concreta do lead ("você é a que já tentou academia e dieta e parou pela dor no joelho"), diz por que as tentativas anteriores não pegaram, e aponta a oferta como o próximo passo pra aquele perfil. Cole `resultados: N · que nomeiam a dor concreta: N`, iguais.

**A oferta ligada ao resultado é a mesma da operação, pelo ângulo daquele perfil.** Cada resultado leva à oferta-destino, mas pela porta que fala com aquele bucket: o mesmo Protocolo entra pela dor da experiente por um ângulo, pela da iniciante por outro. Ângulos diferentes, oferta real única (ou as variações que o dono confirmou que existem). Cole `resultados: N · com oferta da operação ligada: N · com oferta inventada: 0`.

**A captura do lead está no ponto declarado.** Confirme onde o lead deixou o contato (antes do resultado, por padrão) e que o resultado é a recompensa que paga esse contato. Cole `ponto de captura: <antes/depois do resultado> · motivo: <1 linha>`.

---

## Ação 5 · O GATE (roda por dentro, e não imprime)

**Régua de títulos (vale em toda pergunta, título de resultado e nome de bucket que vai ao público).** Todo título passa pela régua (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega**, e fecha com as contagens: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais; o universo são TODOS os textos que o lead lê como título (as perguntas, os nomes de bucket, os títulos de resultado), não só a primeira tela. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Teste do estranho em toda pergunta e resultado.** Alguém que caiu na página sem contexto lê a pergunta e entende o que se pergunta e por quê; lê o título do resultado e sabe o que ele diz. Pergunta que só faz sentido pra quem já leu a anterior, ou título de resultado que é rótulo vazio (`Resultado A`, `Perfil 2`), reprova. Cole, por linha, `<pergunta ou título de resultado> | passa no teste do estranho: sim/não`, e todo `não` volta pro passo de escrita.

**O marcador é campo, e campo tem tamanho.** O marcador cabe em `[A CONFIRMAR: <o dado>]`, no máximo 6 palavras, depois de um rótulo e no fim da linha. O porquê da pendência nunca entra na peça, vai pro handoff com o número da linha ao lado. O script conta e reprova acima do teto.

**Marcador nunca no miolo da fala.** `[A CONFIRMAR: x]` só entra em posição de CAMPO: um link, um telefone, uma data, um valor, no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma pergunta ou de um resultado, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo: escreve a versão que dispensa o dado, ou pergunta ao dono ANTES de escrever. Checagem: `grep -n "\[A CONFIRMAR" <quiz>`; pra cada marcador, apague-o e releia a frase; se virar agramatical, está no miolo e reprova. Cole `marcadores no quiz: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública.** Nome, caso, frase ou perfil de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono (uma linha `autorizado por <dono> em <data>` no próprio insumo). Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna") ou não usa. **Lead em negociação aberta nunca vira exemplo de bucket nem é chamada de aluna.** A checagem é COMANDO, nunca de memória (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`; (2) rode `grep -nwF '<nome>' <quiz>` para cada nome, sobre o arquivo INTEIRO; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa no quiz: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. Nome presente na saída sem a linha de autorização reprova.

**O bucket nunca leva nome real de lead da base.** O perfil de cliente é peça pública: é dele que nasce a segmentação. Rode `grep -rn 'autorizado por' <insumos>`; saída vazia proíbe nome próprio de pessoa real no nome ou na descrição do bucket. O perfil sai por idade, situação e comportamento (`45 a 55, já tentou academia, parou pela dor`). Quando o texto precisar de um nome pra ilustrar, use um nome inventado e diga na mesma linha que é inventado. Cole `buckets ilustrados com nome: N · com nome inventado declarado: N · com nome real dos insumos: 0`.

**Palavra-chave de captura não se inventa, e a grafia é literal.** Se a captura pede uma palavra ("manda X no WhatsApp", "responde Y"), procure a palavra nos insumos do dono e cole `palavra-chave: <literal> | origem: <arquivo:linha>`. Grafia EXATA, sem espaço a mais. Sem origem no disco, escreva a versão que dispensa a palavra e leve a pergunta ao handoff.

**Uso completo do que o dono deu.** Todo dado que o dono forneceu e cabe na entrega aparece nela ou tem o motivo da exclusão declarado. Liste um por linha, `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0`. Qualquer dado em `sem destino` reprova. **O piso é CONTADO:** conte os campos do perfil com `grep -c '^- ' <perfil>`, desdobre os de valor múltiplo, cole a conta: `Piso do inventário: N (campos: X + valores compostos: Y)`. `Dados fornecidos` menor que o piso reprova.

**Proveniência de terceiro.** Nome de empresa, pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra se veio do dono, do insumo dele, ou de uma busca deste turno com o comando e o resultado registrados. Sem isso, sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte.

**O que faz:** reprova a peça que não serve, antes de o dono ver. Serve também como modo auditoria, quando o dono cola um quiz pronto.

**Precisa de:** o quiz escrito.

**Entrega:** nada em modo normal (auditoria silenciosa, a tabela **nunca** vai pra saída). Em modo auditoria, entrega `diagnostico-quiz.md` com a fase, o check que falhou e a correção.

**Leia primeiro:** `shared-references/crivo/03-gate-cub.md`.

**O veredito é o PIOR item.** Um ✗ refaz o trecho que falhou.

| Check | Passa se |
|---|---|
| **Ancorado** | as perguntas de identificação nascem de fala literal da fonte (cita o N real); zero fala inventada |
| **Cada pergunta tem propósito** | toda pergunta segmenta pra um bucket ou gera identificação, e o propósito está declarado. Pergunta decorativa reprova |
| **A árvore fecha** | toda combinação de respostas cai em um bucket, todo bucket tem caminho que chega nele, zero beco sem saída |
| **Buckets distintos** | de 3 a 5 perfis, cada um com ângulo de oferta próprio. Dois perfis com a mesma oferta reprova |
| **Ordem certa** | começa fácil e de identificação, afunila pra segmentar depois |
| **Resultado nomeia a dor** | cada resultado espelha a situação concreta do perfil e aponta o caminho, não elogia em vazio |
| **Oferta real ligada** | cada resultado leva à oferta da operação pelo ângulo do perfil; oferta inventada reprova |
| **Não promete o que não entrega** | nenhum resultado promete bônus, prazo ou formato que a operação não cumpre; item em falha tem decisão escrita |
| **Captura no ponto certo** | o lead deixa o contato antes do resultado (por padrão), e o resultado paga esse contato |
| **Prova real do dono** | todo caso e número é verdade documentável. Sem prova, `[A CONFIRMAR: prova]` e a peça não sai como pronta |
| **Teste do estranho** | toda pergunta e todo título de resultado se explicam a quem chega sem contexto |
| **C/U/B** | não **C**onfuso (uma ideia por pergunta), não **I**nacreditável (resultado com prova à altura), não **B**oring (a pergunta puxa a resposta) |
| **Anti-IA (duro)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz (o verbo que rima com "cravar" e as flexões dele; exceção: aspa literal do cliente) · sem antítese telegráfica ("não é X, é Y") · sem frase-emoldura · sem verbo-clichê de hype |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ refaz. Só tudo ✓ vai pro dono |

Com shell disponível, rode o lint de copy em `scripts/lint_copy.py` sobre o arquivo. Sem shell, faça a busca manual pelos dois bloqueios duros antes de marcar o anti-IA.

---

## Ação 6 · FECHO (mostra e para)

**O que faz:** entrega o quiz limpo e o comentário de publicação.

**Entrega:** só o quiz, sem tabela de gate, sem meta, mais uma linha sobre como levar isso pra página (o handoff pra soft-funil-landing render a página do quiz, com o mapa de que resposta leva a que tela). Pergunta "esse te serve? ajusto?" e **espera o OK** antes de seguir pra próxima etapa ou variação.

**Prova forte descartada se declara na própria peça.** Se um caso, depoimento ou número REAL do dono existia e ficou de fora de um resultado, declare em 1 linha na própria entrega por quê. O dono precisa ver a ausência sem abrir o relato de processo.

---

## O que esta skill NÃO faz

Cada rota é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| A PÁGINA/render do quiz, o hero, cada tela, os botões, o visual | **soft-funil-landing (tipo quiz)** | aqui é o conteúdo e a lógica do quiz; entrego o mapa de telas pra render |
| A carta de vendas ou VSL que vende no fim | **soft-funil-carta** | ligo o resultado à oferta, não escrevo a carta |
| A régua de mensagens depois da captura | **soft-funil-nutricao** | marco o ponto de captura, não escrevo a régua |
| A isca em PDF, o material gratuito | **soft-funil-isca** | não faço |
| Posicionamento, avatar, oferta, nomear mecanismo | **soft-plano-posicionamento** | uso os 3 campos base do objetivo |
| Carrossel, reel, stories, headline solta | **soft-conteudo-*** | não faço |
| Arte, visual, PNG das telas | **soft-designer** | entrego o `.md` do quiz, sem o visual |

## Anti-patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Despejou o quiz inteiro de primeira | Volta: objetivo, buckets, perguntas, resultados, parando a cada etapa |
| Montou o quiz sem saber a oferta-destino | Volta pra Ação 1: sem destino, o quiz não vende, entretém |
| Pergunta decorativa sem propósito | Toda pergunta segmenta ou identifica; a que não faz nenhum dos dois sai |
| Buckets que recebem a mesma oferta | Junta os perfis; bucket existe porque a venda muda pra ele |
| Resultado que só elogia ("você é a Guerreira") | Nomeia a dor concreta do perfil e aponta o caminho pra oferta |
| Resultado promete o que a operação não entrega | Confere cada oferta nos insumos; item em falha tem decisão escrita |
| Árvore com beco sem saída | Toda combinação de respostas cai num bucket, todo bucket tem caminho |
| Captura depois do resultado, sem motivo | O padrão é capturar antes; o resultado é a recompensa que paga o contato |
| Abriu com a pergunta que exige o lead se classificar | Começa fácil e de identificação, afunila depois |
| Inventou um perfil ou número plausível | Só prova real. Sem fonte, `[A CONFIRMAR: perfil/prova]` |
| Narrou o fluxo ("agora vou fazer os buckets") | Executa em silêncio e entrega o resultado |
| Imprimiu a tabela do gate | O gate é interno |
| Foi pra página, o hero, os botões | Isso é da soft-funil-landing; aqui é o conteúdo e a lógica |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o quiz inteiro do caso Renata) · `references/metodo-quiz.md` (a mecânica ASK, os buckets, a lógica de perguntas) · `references/fontes-do-metodo.md` (a fonte confirmada) · `shared-references/operacao-padrao.md`, `crivo/`, `filtro-anti-ia/` · `scripts/lint_copy.py` · `scripts/checar_titulos.py`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `quiz-corpo-depois-dos-40.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` em todo arquivo gravado no diretório de saída, o relato e as notas inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** A lista fecha com `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`. O `RELATO.md` entra na varredura como qualquer outro arquivo; rode o lint nele por último, depois de escrever.
- **Sem sandbox (a régua escrita, quando o lint não roda).** Motor sem shell não executa `scripts/lint_copy.py`, e isso não dispensa o anti-IA: aplique a régua no olho por `shared-references/filtro-anti-ia/padroes-banidos.md`, padrão por padrão, e passe cada reprovação por `shared-references/filtro-anti-ia/falsos-positivos.md` antes de mandar o trecho de volta pro passo de escrita, porque prosa autoral do dono cai no mesmo crivo e some se ninguém conferir. A entrega sai do mesmo jeito, no melhor que esse motor alcança, e o relato fecha com uma linha dizendo que a conferência anti-IA foi no olho, sem código: `anti-IA: conferido no olho pela régua escrita (sem shell nesta rodada)`. Calar o que ficou de fora reprova a entrega; declarar em uma linha reprova nada.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato. Antes de declarar o gate aprovado, abra cada arquivo e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou arquivo do dono nunca é gravado dentro da pasta desta skill; vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
