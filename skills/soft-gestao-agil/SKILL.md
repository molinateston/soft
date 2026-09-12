---
name: soft-gestao-agil
description: >-
  Entrega a rotina da semana escrita em arquivo, com dia e horário já sugeridos: os 3 encontros
  fixos com pauta, a fila do que fazer em ordem, o quadro do que está em andamento, os objetivos
  do trimestre com o resultado que mede cada um, o briefing de uma página e as listas de
  produtividade. Serve pra quem toca sozinho e pra quem tem time. Use quando o pedido for:
  "organiza a rotina do meu time", "como planejo o trimestre", "monta meu OKR", "tudo é prioridade
  e nada anda", "não sei quem está fazendo o que", "o time entrega tudo no último dia", "esqueço
  as coisas toda semana", "começamos e ninguém sabia o que era pra entregar", "quero rodar
  sprint". NÃO use pra: publicar o plano como Google Doc (soft-google-docs); faxina de disco no
  servidor (soft-organizacao-vps); treino e dieta (soft-treino-dieta); copy e conteúdo
  (soft-conteudo-*); funil e venda (soft-funil-*, soft-vendas-*); preço e caixa (soft-financeiro);
  métrica de funil (soft-negocio-metricas).
---

# Gestão ágil: da dor ao plano executável

Esta skill pega uma frase de aperto ("nada anda", "não sei quem faz o quê", "esqueço tudo") e devolve o plano da camada que resolve aquilo, montado com o dono numa conversa de uma pergunta por vez. A entrega é sempre um arquivo `.md` com a peça pronta de usar na segunda-feira: o objetivo com seus resultados-chave, a fila reordenada, o quadro com as colunas e o limite, o roteiro dos rituais com horário, o briefing de uma página, ou as listas individuais.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

Serve qualquer negócio: agência, consultor sozinho, comércio, serviço local, produto digital, produto físico. Nada aqui exige nascer de outro processo.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra o fluxo inteiro num caso fictício: a frase de dor que o dono disse, o mapeamento para a camada, cada pergunta na ordem em que foi feita, as duas prévias preenchidas de verdade, a auditoria rodando no meio do caminho, e o plano final como ele fica no arquivo.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a dor e tudo que tem sobre o trabalho e eu monto o plano). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou. Se faltar um insumo que o plano não vive sem (o objetivo, a lista do que está na mesa, quem executa), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez, e monta o plano com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda o plano (a camada certa pra dor, a ordem da fila, o ritmo da semana, o recorte do ciclo), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a decidir sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("tá tudo urgente", "muita coisa pra fazer"), não segue com o genérico. Pede o concreto que só o dono tem: a lista real do que está aberto, o prazo que aperta de verdade, quem faz o quê hoje. Material bruto vira plano executável; resposta rasa vira plano que ninguém segue. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar o plano, fecha com UMA linha: "Quer outra ordem? Ciclo mais curto? Menos na semana? Me diz o que ajustar que eu refaço só essa parte." A oferta de refino não substitui o gate nem a auditoria.


## Roteamento por pedido: a frase de dor decide a camada

O dono nunca pede "a camada estratégica". Ele diz uma frase de aperto. Esta tabela traduz.

| O dono disse alguma coisa como | Camada | Entrega |
|---|---|---|
| "aonde a gente quer chegar", "meta do trimestre", "objetivo grande", "não sei pra onde estou indo", "quero crescer mas não sei em quê", "todo ano começa igual", "meu time não sabe qual é o alvo", "quero definir os próximos 3 meses" | **ESTRATÉGICA** | Visão em 1 frase + 1 objetivo anual com 2 resultados-chave + até 3 objetivos trimestrais |
| "tudo é prioridade", "muita coisa ao mesmo tempo", "começo tudo e não termino nada", "não sei o que fazer primeiro", "minha lista só cresce", "faço o urgente e o importante fica", "toda semana muda a prioridade" | **PRIORIZAÇÃO** | Fila reordenada em Z + tipo de cada item + o item que sozinho já valeria o mês |
| "não sei quem está fazendo o que", "trabalho invisível", "perguntam o status o dia todo", "descubro que empacou quando já era", "cada um usa uma ferramenta", "o trabalho some no meio" | **QUADRO VISUAL** | Quadro de 5 colunas + limite de tarefas simultâneas + critério de pronto |
| "o time entrega no último dia", "sem ritmo", "reunião que não decide nada", "a semana passa e ninguém sabe o que rolou", "só descubro problema na sexta", "reunião demais e trabalho de menos" | **ROTINAS** | Os 3 rituais semanais com dia, hora, duração e pauta + calendário do que se repete no mês |
| "começamos e ninguém sabia o que era pra entregar", "o cliente entrou mudo", "refizemos tudo do zero", "cada um entendeu uma coisa", "não sei quando isso está pronto", "entrega grande demais pra enxergar" | **BRIEFING** | Briefing de 1 página + backlog em duas dimensões quando for entrega grande |
| "esqueço coisa toda semana", "cabeça cheia", "não durmo pensando no que falta", "anoto em 4 lugares e perco", "trabalho o dia todo e não sei no que", "sou eu sozinho e não dou conta" | **INDIVIDUAL** | As 5 listas + a regra dos 2 minutos + a revisão semanal agendada |
| "quero rodar Scrum de verdade", time de produto digital dedicado, ciclos fechados | **CICLOS FECHADOS** | Explica o que muda, e oferece o caminho de quadro visual + rotinas, que resolve na maioria |

**Ambiguidade é a parte frágil do fluxo, então trate assim, não com um chute:**

- **Frase que casa com duas linhas** (exemplo: "tudo é prioridade e ninguém sabe o que o outro faz" casa com PRIORIZAÇÃO e QUADRO VISUAL): apresente as duas, com a diferença em uma linha cada, e deixe o dono escolher. "Uma cuida de decidir a ordem, a outra de enxergar quem está com o quê. Qual aperta mais hoje?"
- **Frase que não casa com nenhuma** ("está tudo uma bagunça", "me ajuda a organizar"): não force. Pergunte uma coisa só: "me conta o que aconteceu essa semana que te fez pedir isso". A história traz a camada.
- **Frase que parece individual mas é de time** ("eu esqueço tudo" dito por quem tem 6 pessoas): pergunte se o esquecimento é dele sozinho ou se o time também perde coisa. Individual sozinho vai pra INDIVIDUAL; time perdendo coisa vai pra QUADRO VISUAL, porque lista pessoal não conserta trabalho invisível de time.
- **Dono pede a ferramenta pelo nome** ("quero um OKR", "monta um kanban"): aceite, mas confirme a dor em uma pergunta antes de rodar. Ferramenta pedida pelo nome com frequência é a errada pro problema, e uma pergunta evita montar a peça que ninguém vai usar.
- **Dono descreve várias dores de uma vez:** escolha a que ele citou primeiro, diga que vai por ela, e registre as outras como próximo passo no fim do plano. Uma camada por vez.

## Qual reference carregar, por camada

Carregue só o que a camada pede. Nunca leia tudo.

| Camada | Leia primeiro | Profundidade |
|---|---|---|
| ESTRATÉGICA | `references/_metodo-visao.md` · `references/_metodo-okr.md` | `references/_principios-gerais.md` |
| PRIORIZAÇÃO | `references/_metodo-priorizacao.md` | `references/_metodo-canva-3p.md` |
| QUADRO VISUAL | `references/_metodo-kanban.md` | `references/_metodo-kanban-review.md` |
| ROTINAS | `references/_metodo-rotinas.md` | `references/_metodo-kanban-review.md` |
| BRIEFING | `references/_metodo-briefings.md` | `references/_metodo-backlog.md` |
| INDIVIDUAL | `references/_metodo-gtd.md` | `references/_principios-gerais.md` |
| CICLOS FECHADOS | `references/_metodo-scrum.md` | `references/_metodo-rotinas.md` |

## Como ler cada camada

Toda camada abaixo traz o mesmo bloco fixo: **O que faz** · **Precisa de** (o insumo e de onde vem) · **Sem o insumo** (o caminho concreto quando falta) · **Entrega** (nome do arquivo e formato).

**O contexto do dono vem do banco do agente.** Onde a camada precisar do estágio do negócio, do tamanho do time ou dos números que ele acompanha: leia do perfil ou banco do agente quando existir; senão, use as 3 perguntas de contexto do passo F0. Nunca invente, nunca pare por causa disso.

## Regras que valem em todas as camadas

- **Uma pergunta por vez.** Nunca despeje três juntas: o dono responde no atropelo e o plano sai furado.
- **Sugira 2 ou 3 opções em cada decisão**, nunca uma só. O dono escolhe.
- **Prévia a cada 5 respostas**, preenchida com o que ele já deu. Não é resumo, é a peça começando a existir.
- **Sem jargão.** Nunca deixe uma sigla sozinha sem a tradução ao lado, na primeira vez que ela aparecer.
- **Toda iniciativa aponta pra um objetivo.** Não aponta, sai da lista.
- **Todo número tem um dono nomeado**, uma pessoa, não uma área.
- **Comece pequeno:** 1 objetivo anual com 2 resultados-chave, no máximo 3 objetivos no trimestre com 2 resultados-chave cada.
- **O plano cabe em uma página.** Se não cabe, ninguém olha depois da primeira semana.
- **A parte tática não se pula.** Ir do objetivo direto pro quadro, sem briefing nem backlog, é o erro mais comum de quem tenta isso sozinho.

---

## Fluxo canônico

### M0 · a frase de dor (1 pergunta)

> "O que mais te aperta na gestão ou na rotina de trabalho hoje? Me conta em uma frase."

Escute a resposta livre e mapeie pela tabela de roteamento. Ambiguidade: siga o tratamento descrito lá.

### P0 · o que já existe (1 pergunta)

> "Você já tem alguma peça pronta que dê pra aproveitar? Um quadro em alguma ferramenta, uma planilha, um objetivo escrito, um calendário de reuniões. Se tiver, me manda ou cola aqui. Se não tiver nada, tudo bem, a gente monta do zero."

Trouxe peça, extraia o contexto dela e **pule as perguntas cuja resposta já está lá**. Perguntar o que ele acabou de mandar queima confiança.

### F0 · contexto do negócio (3 perguntas, uma por vez)

1. "Você toca isso sozinho ou tem time? Se tem, quantas pessoas envolvidas?"
2. "Faz quanto tempo o negócio roda, e em que estágio ele está: idealizando, primeiros clientes, crescendo, ou já rodando grande?"
3. "Você acompanha algum número hoje? Faturamento do mês, clientes ativos, ticket médio, algum. Se não acompanha nenhum, tudo bem, a gente começa por um."

**Prévia 1** (a primeira das duas obrigatórias): mostre o que já dá pra afirmar com essas respostas, no formato de prévia preenchida do bloco F2.

### F1 · execução da camada

Cada camada tem seu bloco abaixo. Rode só a que o roteamento indicou.

---

## Camada ESTRATÉGICA (visão e objetivos com resultados-chave)

**O que faz:** transforma "quero crescer" numa visão de uma frase e num objetivo com dois números que dizem se ele aconteceu.

**Precisa de:** onde o negócio está hoje, onde o dono quer chegar, e pelo menos um número que ele já acompanhe (do passo F0 ou do banco do agente).

**Sem o insumo:** número nenhum acompanhado é comum e não bloqueia. Escolha com ele **um** número que já dê pra medir a partir da semana que vem, meça a linha de base agora, e construa o resultado-chave em cima dela. Resultado-chave sem linha de base é chute; com linha de base medida hoje, é meta.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `plano-estrategico-<negocio>.md`, com a visão em uma frase, o objetivo anual com 2 resultados-chave, até 3 objetivos trimestrais com 2 cada, e as iniciativas que sustentam cada resultado-chave.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/_metodo-visao.md` e `references/_metodo-okr.md`.

1. Rode os 6 campos da visão, um por vez: situação atual · passado · perspectivas e tendências · futuro desejado · como pretende chegar lá · a visão sintetizada.
2. Feche a visão em **uma frase**. Um exemplo genérico ilustra a forma, nunca vira o padrão do dono.
3. Vá pro objetivo anual: **1 objetivo qualitativo forte** (sem número dentro dele) + **2 resultados-chave numéricos**.
4. Construa cada resultado-chave com quatro campos: métrica, linha de base, meta, prazo.
5. Desça pro trimestre: até 3 objetivos, 2 resultados-chave cada, em cascata a partir do anual.
6. Pergunte quais iniciativas sustentam cada resultado-chave. Elas alimentam a camada de priorização.

## Camada PRIORIZAÇÃO (a fila reordenada)

**O que faz:** pega a lista bagunçada e devolve a ordem de fazer, com o que não entra marcado como não-entra.

**Precisa de:** a lista do que está na fila hoje · os objetivos do trimestre, se existirem.

**Sem o insumo:** sem objetivos definidos, o filtro de "isso move algum objetivo?" não roda. Substitua por uma pergunta só: "qual resultado você quer ver diferente daqui a 90 dias?", e use a resposta como o objetivo provisório do filtro. Marque no plano que ele é provisório.

**Entrega:** `prioridades-<periodo>.md`, com a fila em ordem, o tipo de cada item, o item que sozinho já valeria o mês, e a lista do que ficou de fora com o motivo.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/_metodo-priorizacao.md`.

1. "Me lista tudo que está na sua fila hoje, mesmo desorganizado. Uma coisa por linha."
2. Filtre: pra cada item, "isso move algum objetivo do trimestre?". Não move, sai da fila e vai pra uma lista separada de "não entra agora".
3. Rode a matriz de esforço e impacto, 4 quadrantes, e leia em Z: alto impacto e baixo esforço primeiro, alto impacto e alto esforço depois, baixo impacto e baixo esforço em terceiro, baixo impacto e alto esforço **não faz**.
4. Classifique cada item que sobrou: **projeto** (tem começo, meio e fim), **processo** (rotina que não acaba) ou **produto** (o que a empresa vende).
5. "Qual é o único que, se você só entregasse ele, já valeria o mês?" Esse fica destacado no topo.

## Camada QUADRO VISUAL (o trabalho na parede)

**O que faz:** tira o trabalho da cabeça e do aplicativo de mensagem e coloca num quadro onde qualquer um vê o estado de tudo em 5 segundos.

**Precisa de:** onde o trabalho vive hoje · quantas pessoas puxam trabalho ao mesmo tempo · o que significa "pronto" ali.

**Sem o insumo:** "pronto" não definido é o caso mais comum, e é o que faz o quadro falhar. Construa na hora, com uma pergunta: "quando você olha uma entrega e sabe que ela acabou, o que você conferiu?". A resposta dele vira o critério, com as palavras dele.

**Entrega:** `quadro-<negocio>.md`, com as 5 colunas, o limite da coluna de execução, o critério de pronto, a regra de bloqueio, e de 3 a 5 cartões de exemplo tirados do trabalho real dele.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/_metodo-kanban.md`.

1. "Onde vive o trabalho hoje?"
2. Monte as 5 colunas: a fazer · fazendo · validação · impedimento · feito.
3. "Quantas pessoas puxam trabalho ao mesmo tempo?" O número define o limite da coluna **fazendo**, que **sempre** tem limite.
4. Defina o critério de pronto, que é o que faz o cartão sair de validação para feito.
5. Defina quando um cartão vai para impedimento, e quem ele avisa ao ir.
6. Preencha o quadro com 3 a 5 cartões do trabalho real dele, nunca com exemplos genéricos.

## Camada ROTINAS (o ritmo da semana)

**O que faz:** instala os 3 rituais semanais com dia, hora, duração e pauta, para que a semana tenha começo, meio e fim.

**Precisa de:** quem participa · a rotina atual de reuniões · o que já se repete todo mês e todo trimestre.

**Sem o insumo:** dono sozinho, sem time, os rituais continuam valendo, com ele mesmo: o planejamento vira a meia hora de segunda que define a semana, o acompanhamento diário vira uma checagem de 5 minutos no quadro, e a revisão de sexta vira a meia hora que fecha. Não corte os três, encurte.

**Entrega:** `rotina-semanal-<negocio>.md`, com os 3 rituais em formato de agenda (dia, hora, duração, quem, pauta, o que se decide), mais o calendário do que se repete no mês e no trimestre.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/_metodo-rotinas.md`.

1. Instale os 3: **planejamento** (segunda de manhã, 1 a 2 horas), **acompanhamento diário** (terça a sexta, no máximo 15 minutos, em pé), **revisão** (sexta no fim do dia, 30 a 60 minutos).
2. Para cada um, defina horário, participantes, duração e a pauta. **Ritual sem decisão sendo tomada dentro dele não se cria.**
3. Planejamento: puxa tarefa do backlog pra coluna a fazer.
4. Acompanhamento diário: 3 perguntas por pessoa, o que fiz, o que vou fazer, o que me impede.
5. Revisão: fecha o quadro, o pendente volta pra fila, o que falhou vira aprendizado de 2 minutos.
6. "O que você refaz todo mês ou todo trimestre?" Isso vira rotina fixa fora da semana.

## Camada BRIEFING (uma página antes de começar)

**O que faz:** escreve, antes de a equipe começar, o que exatamente vai ser entregue e como se sabe que acabou.

**Precisa de:** qual é a entrega · quem pediu · qual resultado ela precisa produzir · o que está fora do escopo.

**Sem o insumo:** o dono não sabe descrever o resultado esperado (acontece muito com pedido de cliente): pergunte "o que vai estar diferente na vida de quem recebe isso, depois que estiver pronto?". A resposta é o resultado, mesmo que ele não use essa palavra.

**Entrega:** `briefing-<entrega>.md`, uma página, com o campo de aprovação no fim. Entrega grande, mais o backlog em duas dimensões.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/_metodo-briefings.md`.

1. Classifique primeiro: **projeto**, **processo** ou **produto**. Cada um tem um molde diferente.
2. Rode os campos do molde certo, um por vez.
3. Feche em **uma página**. Documento de 30 páginas ninguém lê, e briefing que ninguém lê é o mesmo que briefing que não existe.
4. Entrega grande: quebre em backlog de duas dimensões, a narrativa horizontal (as fases em sequência) e o detalhamento vertical (as tarefas dentro de cada fase), com cada item marcado como essencial, desejável, opcional ou questionável.
5. Termine com o campo de aprovação: quem assina que o briefing está certo, antes de a equipe começar.

## Camada INDIVIDUAL (a cabeça vazia)

**O que faz:** tira tudo da cabeça, organiza em 5 listas, e agenda a revisão que mantém o sistema vivo.

**Precisa de:** onde as coisas chegam pra ele hoje (as entradas) · quanto tempo ele consegue reservar por semana pra revisar.

**Sem o insumo:** dono que não consegue listar as entradas: pergunte "por onde alguém te pede alguma coisa?". Aplicativo de mensagem, e-mail, ligação, papel na mesa, a própria cabeça às 3 da manhã. Tudo isso é entrada.

**Entrega:** `sistema-pessoal-<nome>.md`, com as 5 listas já povoadas com itens reais da vida dele, a regra dos 2 minutos, e a revisão semanal com dia e hora marcados.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/_metodo-gtd.md`.

1. "Por onde chegam as coisas pra você hoje?"
2. Rode os 5 passos: capturar, esclarecer, organizar, refletir, executar.
3. Aplique a regra dos 2 minutos: o que leva menos que isso, faz agora, não anota.
4. Monte as 5 listas com itens reais dele: próximas ações por contexto, projetos, aguardando resposta, algum dia, referência.
5. Agende a revisão semanal com dia e hora fixos, cerca de 1 hora. **Sem a revisão, o sistema morre em 3 semanas**, e vale dizer isso a ele.

## Camada CICLOS FECHADOS

**O que faz:** explica o que muda num método de ciclos fechados formal e oferece o caminho mais curto quando ele não é necessário.

**Precisa de:** saber se é time de produto digital dedicado, com ciclos e papéis definidos, ou negócio pequeno querendo ritmo.

**Sem o insumo:** pergunte uma coisa só: "esse time trabalha em um produto só, em tempo integral?". Não, o caminho é quadro visual mais rotinas.

**Entrega:** a explicação em uma página, mais o plano da camada escolhida.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/_metodo-scrum.md`.

Negócio pequeno ou médio: ofereça quadro visual mais rotinas, que resolve na maioria dos casos, e diga por quê em uma linha.

---

### F2 · a prévia (a cada 5 respostas, obrigatória)

Prévia não é resumo do que foi dito. É a peça começando a existir, com os campos que já dá pra preencher e os buracos visíveis. Assim:

```
======================================
PLANO DE GESTÃO · Ateliê de Costura Sob Medida     [PRÉVIA 1 de 2]
======================================
Camada: ROTINAS
Contexto: 4 pessoas · 3 anos rodando · acompanha faturamento e peças entregues

------ O QUE JÁ ESTÁ DE PÉ ------
Dor declarada: tudo fica pronto na sexta à tarde, sempre correndo
Quem participa dos rituais: você + as 3 costureiras
Onde o trabalho vive hoje: caderno na bancada + mensagens no celular

------ O QUE AINDA FALTA ------
[ ] horário que funciona pra reunião de segunda (a oficina abre 8h?)
[ ] o que significa "pronto" numa peça (prova? acabamento? entrega?)
[ ] o que se repete todo mês (fechamento? compra de tecido?)

------ COMO ESTÁ FICANDO ------
Segunda 08h15, 40min: planejamento da semana, as 4, em pé na bancada
Terça a sexta 08h05, 10min: o que fiz, o que faço, o que me impede
Sexta [horário a definir]: revisão, fecha o quadro
======================================
Faltam 3 respostas pra fechar. Vamos pela primeira: a oficina abre 8h mesmo?
```

Duas coisas que a prévia sempre faz: mostra o que **já está de pé** com as palavras do próprio dono, e mostra o que **falta** como lista de campos vazios, não como pergunta escondida no meio do texto.

### F3 · gate final

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


> "Esse plano encaixa? Se sim, eu salvo o arquivo. Se quer ajustar alguma coisa, me diz o que muda."

Aprovado: salve o `.md` no disco e devolva o caminho. Se o ambiente tiver conector de documento, exporte por ele e devolva o endereço cru, sem sintaxe de link. Sem conector, o `.md` é a entrega.

---

## Auditoria: quando ela roda (não é só no fim)

A auditoria roda em **três momentos**, e não uma vez só no fim, porque erro pego no fim custa a conversa inteira.

**1. Na prévia (a cada 5 respostas), rode os checks de forma:**

- [ ] Alguma sigla apareceu sem tradução do lado?
- [ ] Alguma decisão foi apresentada com opção única, em vez de 2 ou 3?
- [ ] Alguma pergunta saiu junto com outra?

Reprovou, conserte **na próxima mensagem**, não no fim. O dono ainda está na conversa e a correção é barata.

**2. Ao fechar cada bloco da camada, rode os checks de conteúdo daquele bloco:**

- Objetivo fechado sem número dentro dele, e cada resultado-chave com métrica, linha de base, meta e prazo?
- Fila fechada com todo item apontando pra um objetivo, e o que não aponta na lista de fora?
- Quadro fechado com limite na coluna de execução e critério de pronto escrito?
- Rituais fechados com uma decisão acontecendo dentro de cada um?
- Briefing fechado em uma página, com campo de aprovação?

Reprovou, volte ao ponto do bloco, não recomece a camada.

**3. Antes de entregar o plano, rode o crivo inteiro:**

- [ ] Toda iniciativa aponta pra um objetivo?
- [ ] Todo número tem uma pessoa nomeada como dona?
- [ ] Começou pequeno (no máximo 1 objetivo anual com 2 resultados-chave, até 3 trimestrais com 2 cada)?
- [ ] Cada cartão ou iniciativa tem dono único e critério de pronto?
- [ ] Nenhum ritual foi criado sem uma decisão sendo tomada dentro dele?
- [ ] O plano cabe em uma página ou numa tela?
- [ ] Zero jargão sem tradução ao lado?
- [ ] A parte tática não foi pulada (briefing e backlog, quando a entrega é grande)?
- [ ] Zero travessão, zero verbo da família banida pela régua anti-voz, sem caixa alta em texto corrido?

Qualquer resposta negativa, conserte antes de entregar.

**Anti-IA em código:** rode `python3 scripts/lint_copy.py <arquivo>` no shell quando o ambiente permitir. Sem shell, faça a busca manual dos dois padrões duros (travessão e a família do verbo-freio banida) no texto. Vale pro `.md` do plano e pra qualquer peça exportada.

## Teste do mapeamento inicial (rode antes de confiar na tabela)

A tabela de roteamento é o ponto onde a skill mais erra, então ela tem teste. Passe estas 10 frases pela tabela e confira o destino. Acertar 9 é o piso; errar 2 ou mais significa que a tabela precisa de mais exemplos na linha que falhou.

| # | Frase de entrada | Destino correto | Por quê |
|---|---|---|---|
| 1 | "meu time entrega tudo na sexta correndo" | ROTINAS | é falta de ritmo, não de prioridade |
| 2 | "tenho 40 coisas na lista e não sei por onde pego" | PRIORIZAÇÃO | é ordem, não visibilidade |
| 3 | "perguntam o status o dia inteiro e eu não sei responder" | QUADRO VISUAL | é trabalho invisível |
| 4 | "não durmo pensando no que esqueci" e trabalha sozinho | INDIVIDUAL | é carga mental de uma pessoa |
| 5 | "não durmo pensando no que esqueci" e tem 8 pessoas | pergunta primeiro | pode ser individual ou quadro; a pergunta desempata |
| 6 | "a gente refez o site inteiro porque o cliente queria outra coisa" | BRIEFING | é escopo não acordado antes |
| 7 | "quero saber onde quero estar em dezembro" | ESTRATÉGICA | é destino, não execução |
| 8 | "quero um OKR" | ESTRATÉGICA, com confirmação | ferramenta pedida pelo nome, confirme a dor antes |
| 9 | "tá tudo uma bagunça" | pergunta aberta | não casa com nenhuma linha; peça a história da semana |
| 10 | "meu time de 5 devs quer rodar sprint de 2 semanas em produto próprio" | CICLOS FECHADOS | é o caso legítimo do método formal |

Os casos 5, 9 e 10 são os que separam um roteamento bom de um chute. Se a sua leitura mandou o 5 direto pra INDIVIDUAL sem perguntar, ou o 9 pra qualquer camada, o mapeamento falhou.

## Retomabilidade

Estado salvo a cada resposta, num arquivo de trabalho `estado-<slug>-<data>.json`, no diretório temporário do ambiente:

```json
{
  "slug": "ateliê-costura-2026-08",
  "camada": "ROTINAS",
  "respostas": { "M0": "...", "F0.1": "..." },
  "previa_ultima": 1,
  "criado_em": "...",
  "atualizado_em": "..."
}
```

Ao iniciar, se houver estado salvo: "achei um plano que você começou em [data]. Retoma daqui ou começa de novo?"

## O que esta skill NÃO faz

Em toda rota abaixo: se a skill de destino não estiver instalada, faço aqui o mínimo e digo o que ficou de fora.

- **Copy, conteúdo, carrossel, reel** → `soft-conteudo-*`.
- **Funil, página, carta, venda** → `soft-funil-*`, `soft-vendas-*`.
- **Preço, margem, DRE, caixa** → `soft-financeiro`. Aqui o número entra só como resultado-chave, não como conta.
- **Ler métrica de funil e diagnosticar queda de resultado** → `soft-negocio-metricas`.
- **Webinar** → `soft-webinar`.
- **Construir o sistema, o quadro digital ou a automação** → `soft-sistema`. Esta skill desenha o quadro e as regras; ela não codifica a ferramenta.
- **Contratar, demitir, avaliar pessoa.** Fora de escopo. Esta skill organiza o trabalho, não gerencia gente.
- **Decidir a estratégia do negócio pelo dono.** Ela conduz a conversa e organiza a resposta dele.

## O que não fazer, dentro do escopo

- Não empurrar objetivos e resultados-chave quando a dor é individual.
- Não empurrar método de ciclos fechados formal em negócio pequeno ou médio.
- Não criar quadro nem ritual sem o dono participar do desenho, senão ninguém usa.
- Não usar nome de método ou de ferramenta de terceiro como padrão. Exemplo ilustra a forma, nunca vira o default.
- Não pular a parte tática (briefing e backlog) quando a entrega é grande.
- Não deixar a coluna de execução sem limite.
- Não rodar o quadro sem a revisão de sexta.
- Não fechar plano sem passar o crivo dos três momentos.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
