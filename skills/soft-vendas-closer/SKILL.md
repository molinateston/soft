---
name: soft-vendas-closer
description: >-
  Conduz e FECHA o lead que já chegou quente: entrega o script das 7 fases até a coleta do sinal, a resposta de objeção, o diagnóstico da conversa que empacou, o copiloto ao vivo e o pós-venda. Use quando o pedido for: "script de venda", "como conduzo essa conversa", "o cliente disse que tá caro", "ele falou que vai pensar", "como peço o sim", "como pego o Pix", "analisa essa conversa", "me ajuda agora, tô no meio da call", "não consigo cobrar caro", "como peço indicação". NÃO use pra: o DOSSIÊ e o roteiro de temas ANTES da call, pesquisa do lead, objetivo da reunião (soft-vendas-call-prep); abrir conversa fria, qualificar, agendar, operar o CRM ou montar agente de IA (soft-vendas-sdr, que faz a metade de cima); prospecção fria em lista (soft-vendas-outreach); o kit de SDR (soft-sdr-kit); a campanha do mês (soft-vendas-estrategias); contrato (soft-vendas-contratos); proposta em site (soft-vendas-proposta); posicionamento e oferta (soft-plano-posicionamento). Leia e siga o fluxo inteiro do SKILL.md.
---

# O closer: conduzir a conversa quente até o dinheiro na conta

Esta skill transforma a conversa em cliente sem empurrar. Ela recebe o lead que já chegou quente, do funil ou do agendamento, e entrega a condução inteira: o script das 7 fases até a coleta do sinal, a objeção isolada e respondida, o diagnóstico de uma negociação que empacou, a jogada ao vivo quando o dono está no meio da conversa, e o pós-venda que vira indicação e prova. O resultado é sempre um documento nomeado, completo, pronto pra usar.

**A skill confere que é ela mesma, antes da primeira linha do fluxo.** As quatro skills de venda são vizinhas e se confundem: uma execução leu a pasta da vizinha, concluiu que esta skill não existia, rodou a outra, e entregou 2 arquivos onde o contrato pede 8, sem `conferencia/checagem-titulos.md`. A PRIMEIRA linha do fluxo é `head -3 SKILL.md` da pasta indicada, e você cola `SKILL.md lido: <caminho literal> · nome no frontmatter: <nome>`. **Nome diferente do que o dono pediu PARA tudo** e reporta que a skill pedida não está no catálogo desta sessão, em vez de rodar a vizinha: contratos de saída diferentes produzem entrega incompleta que parece completa.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Os arquivos que cada ação exige (`--exige`).** Conferência: `--conferir <pasta> --exige <lista>`. Script de sessão: `--exige script-sessao.md`; objeções: `--exige mapa-objecoes.md`; follow-up pós-call: `--exige followup-pos-call.md`; pacote: as três somadas. Arquivo ausente sai com exit 1.

**A resposta devolve à pessoa o que ela mesma trouxe de bom.** Rode `grep -niE 'melhorou|funcionou|gostei|deu certo|obrigad' <insumo>` e cole a saída. Toda linha que voltar entra na mensagem, em uma frase, ANTES da parte que falhou. Cole `pontos positivos na reclamação: N · reconhecidos na mensagem: N`, iguais.

**A mensagem promete ato, nunca processo.** Rode `grep -niE 'apurar|apurando|verificar|analisar|definição|retorno|posicionamento|alinhar' <mensagem>` e cole a saída, inclusive vazia. Troque cada ocorrência por um ato com sujeito e hora (`eu volto a responder o grupo hoje à noite`), ou tire a frase: contar à pessoa o trabalho interno da casa não é resposta. Cole `palavras de processo na mensagem: 0`.

**A promessa que consome recurso do dono sai da mensagem pronta, e o teste é por efeito, nunca por nome.** Liste tudo que a mensagem promete e marque cada item: `<promessa> | consome tempo, acesso ou dinheiro que não estava no combinado? sim/não`. Extensão de prazo, dias a mais de acesso, sessão extra e prioridade na fila respondem **sim** do mesmo jeito que mês grátis. Tudo que responde `sim` vira linha da tabela, marcada `quem aprova: o dono`. Cole a lista item a item e `promessas que consomem recurso na mensagem pronta: 0`. **A contagem sem a lista ao lado não conta como feita**, porque quem classifica sozinho classifica a favor do próprio texto.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Cada linha da mensagem curta carrega algo que a anterior não carrega.** Antes de fechar, releia as linhas e corte a que só reformula a de cima; numa mensagem de três linhas, repetição é metade da peça.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra, num caso fictício de nicho neutro, a entrada que o dono deu, as perguntas que a skill fez e a saída de cada ação, com o script das 7 fases montado por inteiro, a resposta de objeção, o laudo da conversa empacada e a mensagem de pós-venda. Ler antes economiza uma rodada inteira de retrabalho.

### A régua de canal por ticket (mesma régua das skills irmãs)

Até R$ 3.000 o fechamento acontece na própria conversa (DM ou WhatsApp, com áudio, doc e vídeo curto). Acima de R$ 3.000 a conversa qualifica e agenda a call 1:1, e o fechamento acontece na call. O funil de aula/webinar é a exceção: ele fecha de uma vez no checkout, dentro da própria aula. A call também entra abaixo do limiar quando o lead pede a condução ao vivo, quando a decisão é a vários ou quando o caso é complexo. Esta régua é a mesma nas skills irmãs soft-vendas-sdr, soft-vendas-closer e soft-vendas-estrategias, com o texto idêntico nas três; mudou numa, muda nas três.

### A fronteira com as duas irmãs (escrita dos dois lados)

| Quem | O que é dela | Onde para |
|---|---|---|
| **soft-vendas-closer** (esta) | o FUNDO: recebe o lead quente, conduz as 7 fases, isola objeção, pede a decisão e coleta o sinal | não abre conversa fria, não prospecta, não opera o CRM nem monta agente de IA |
| **soft-vendas-sdr** | o TOPO: abre a conversa, responde o lead novo, qualifica de leve, vende a sessão como vaga e agenda | para no agendamento com a nota rica; nunca responde objeção de preço nem pede o sim |
| **soft-vendas-estrategias** | a JOGADA: decide qual campanha rodar no mês e em que ordem, pra gerar a conversa que esta skill vai fechar | não conduz conversa nem responde objeção |
| **soft-vendas-call-prep** | o ANTES da call: o dossiê do lead, o objetivo da reunião, o roteiro de temas e as objeções antecipadas por escrito | para quando a call começa; não conduz a conversa nem responde ao vivo |
| **soft-vendas-outreach** | a PROSPECÇÃO FRIA: pesquisa a conta que nunca ouviu falar do dono e escreve a abordagem que abre a porta | para quando a pessoa responde; daí em diante é sdr ou closer |

Variante registrada, não é o padrão: existe o modelo com equipe grande em que toda venda vai pra call, de qualquer ticket, com condição promocional que expira na própria call. Fica em `references/quadro-de-produtos.md`; o padrão desta skill mantém o limiar e escassez só com gatilho real.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a oferta e o lead e eu escrevo o script). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pro script com o que o dono colou. Se faltar um insumo que a condução não vive sem (a oferta, o preço, a objeção que aparece), pergunta AQUELE insumo e segue, sem repetir a entrevista inteira. No copiloto ao vivo, responde a jogada na hora, sem documento.
- **Modo guiado**: só quando o dono pede explicitamente. Pergunta a oferta, o preço e como o lead chegou, uma coisa de cada vez, e escreve a condução com o que o dono for dando.

A pergunta do modo é UMA por conversa. As outras três partes acontecem nos passos abaixo:

- **Ensina enquanto faz:** em cada escolha estrutural (a fase que resolve o empaque, o isolamento da objeção, o momento de pedir o sim) escreve UMA linha do porquê. O dono lê a razão e aprende a conduzir sozinho.
- **Puxa o material bruto:** quando a resposta vier rasa ("o cliente tá em cima do muro", "acho que é preço"), não segue com o genérico. Pede o concreto que só o dono tem: a última frase literal que o lead falou, onde a conversa esfriou, o que ele já comprou antes. Fala real do lead vira resposta certeira; resposta rasa vira script que não encaixa.
- **Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer a resposta pra outra objeção? o tom mais firme? o pós-venda também? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "script de venda", "como conduzo", "roteiro pra call", "roteiro pra DM", "monta minha conversa" | **1 · SCRIPT DAS 7 FASES** |
| "tá caro", "vou pensar", "preciso falar com meu sócio", "já tentei e não deu certo", "tem desconto", "como respondo isso" | **2 · OBJEÇÃO** |
| "analisa essa conversa", "empacou", "ele sumiu", "olha esse print", "onde eu errei" | **3 · DIAGNÓSTICO DA CONVERSA** |
| "tô no meio da call agora", "o que eu respondo", "me ajuda agora", "próxima mensagem" | **4 · COPILOTO AO VIVO** |
| "como peço o Pix", "ele disse sim e sumiu", "coleta de sinal", "fechamento" | **5 · COLETA DO SINAL** |
| "como peço indicação", "como coleto depoimento", "pós-venda", "expandir cliente" | **6 · PÓS-VENDA** |
| "não consigo cobrar caro", "empaco na hora do preço", "medo de vender" | **7 · CABEÇA DO VENDEDOR** |

Pedido ambíguo ("me ajuda com a venda", "olha essa conversa aqui"): pergunte UMA coisa só, "você quer o script pronto ou a próxima jogada de uma conversa que já está rolando?", mostre a tabela como cardápio e siga pela resposta.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · passos numerados com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de oferta, PUV, mecanismo, voz, avatar ou prova: leia do perfil/brain do agente quando existir; se não existir, rode a entrevista rápida abaixo e siga com o que faltar marcado `[A CONFIRMAR]`. Nunca invente, nunca pare por causa disso.

**Não existe Plano de Posicionamento pronto? O caminho é a entrevista rápida de 5 perguntas logo abaixo, e mais nada.** Isso vale em toda ação, e vale igual quando a `soft-plano-posicionamento` não está instalada. Você não para, não manda o dono buscar o Plano e não inventa oferta: faz as 5 perguntas num bloco só, escreve com o que voltar, e o que faltar sai marcado `[A CONFIRMAR]` no lugar exato.

> **Entrevista rápida (5 perguntas, num bloco só, quando não há perfil):**
> 1. Qual é a oferta: o que você entrega, em que formato, em quanto tempo?
> 2. Qual o preço e a condição de pagamento?
> 3. Qual a promessa concreta, com número e prazo quando der?
> 4. Qual a objeção que mais aparece nas suas conversas?
> 5. Que prova você tem na mão: case, número, depoimento?
>
> Com essas 5 respostas o script sai completo.

**Quando a pergunta 4 fica sem resposta (o perfil não cobre a objeção).** Pergunte UMA vez, direta: "qual é a frase que mais aparece quando o lead não fecha?". Se o dono não responder ou não souber, **não pare e não invente uma objeção exótica**: assuma a mais comum do nicho dele, escreva a resposta pra ela no script, e marque no lugar exato `[A CONFIRMAR: objeção assumida por ser a mais comum do nicho, o dono não confirmou]`. Declare a premissa em 1 linha no chat, no STOP. As mais comuns por natureza de decisão, pra quando você precisa escolher: compra pessoal de ticket médio puxa "preciso falar com meu marido / minha esposa" e "vou pensar"; compra pessoal de ticket baixo puxa "tá caro" e "agora não é o momento"; compra de empresa puxa "preciso levar pro sócio" e "vou ver o orçamento"; nicho onde o lead já tentou de tudo puxa "já tentei e não deu certo". Uma objeção assumida, nunca três: o script responde a que você assumiu e o dono corrige no STOP.

### De onde vem o lead

O closer recebe o lead de dois jeitos. **Direto do funil:** o lead veio quente da carta, da jogada ou da aula e cai na conversa querendo resolver; você começa na Fase 1. **Do agendamento, com contexto:** quem abriu deixou uma nota rica (a dor nomeada, o problema avançado, a temperatura, o BANT, as objeções já ditas, o que ainda falta cair); você abre lendo a nota, ecoa a qualificação e entra direto no diagnóstico, nunca faz o lead repetir tudo. Nota rasa ("tá quente") faz o closer entrar perdendo: cobre o contexto de quem abriu.

---

## Ação 1 · SCRIPT DAS 7 FASES (a entrega principal)

**O que faz:** monta o roteiro de fechamento inteiro, da abertura até a coleta do sinal, no canal escolhido.

**Precisa de:** a oferta, o preço e a promessa, do perfil/brain do agente · o canal (DM/WhatsApp ou call) e o ticket · o verbatim real do avatar, pra as falas nascerem da boca dele.

**Sem o insumo:** rode a entrevista rápida de 5 perguntas acima. Sem verbatim, escreva o script com `[A CONFIRMAR]` no lugar de cada aspa que se declararia real e diga isso em 1 linha; nunca invente fala de cliente.

**Passo 0, obrigatório antes de escrever a Fase 1: varredura de conversa em curso.** Antes de montar o script, procure nos insumos do dono uma conversa já aberta sobre esta oferta: transcrição de call, caixa de entrada, histórico de chat, nota de agendamento. **Se existir, o script é pra ELA**, e abre na fase em que a conversa parou, nunca na fase 1. Cole a linha `conversa em curso encontrada: <arquivo:item> · fase em que parou: <N>` ou `conversa em curso: nenhuma nos insumos (varridos: <lista de arquivos>)`. **Script que abre em descoberta com uma lead que já ouviu o preço reprova**: pedir três perguntas de diagnóstico a quem acabou de escrever "ainda tem vaga?" recomeça do zero uma conversa que estava na hora de fechar. O script reusa o que ela já contou, com as palavras dela, e não a faz repetir nada.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `01-script-venda.md`, as **7 fases inteiras num só documento**, cada fase com a fala pronta em bloco copiável, mais a nota final de condução. **Um único STOP, sobre o script completo: "ajusto ou pode ir pro lead?"**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/script-builder.md`, o roteiro fase a fase com as falas de campo e a seção "Como entregar o script final". **É por ele que você começa, e na maioria dos casos ele basta pra escrever o script.**

**Sobre a sobreposição com `references/processo-conversao.md`, pra você não ler duas vezes a mesma coisa:** as duas trazem a espinha das 7 fases, e isso é de propósito, cada uma serve um momento. **`script-builder.md` é o "leia primeiro"**: a espinha com a fala pronta pra copiar, é dele que o script sai. **`processo-conversao.md` é a profundidade**: o porquê de cada fase, o roteamento entre os modos da skill e o catálogo de objeções. Abra ele quando precisar do catálogo de objeções, quando o dono perguntar por que a ordem das fases é essa, ou quando a conversa fugiu do roteiro. Se você já leu a espinha no script-builder, não releia no processo-conversao: pule pro catálogo.

**Profundidade:** `references/dm-sem-call.md` (fechar na DM, a espinha comprimida em 5 etapas) · `references/frameworks-consolidados.md` (perguntas em escada, ensinar e desafiar a visão, tamanho do problema) · `references/conducao-na-pratica.md` (o jeito de conduzir, destilado de sessões reais) · `references/quadro-de-produtos.md` (as concessões pré-autorizadas por produto, pra operação com equipe) · `guia/10-vendas-consultivas.md` (a fonte da mecânica, leitura dirigida).

> **Anti-pattern grave: pingar fase a fase no chat.** Entregar as fases 1 a 3 e deixar "o resto pro próximo passo" não é um passo por vez, é entrega incompleta, e corta justo a fase 7, que é o núcleo desta skill. O STOP é sobre o documento pronto, não sobre liberar fase por fase.

### A espinha de 7 fases

A ordem é fixa. O que muda por canal e ticket é ritmo e comprimento, nunca a sequência.

| Fase | O que faz | Fala-âncora de campo |
|---|---|---|
| **1. Recuo estratégico** | Abre consultivo, mostra que não veio empurrar; pede permissão pra perguntar antes de falar do programa. | *"Primeiro eu faço um diagnóstico do seu [problema] e te falo na cara se consigo ajudar. Se não, sou o primeiro a dizer. Só se fizer sentido nos dois lados é que a gente fala de plano e valor."* |
| **2. Descoberta** | Lead fala 70%; desce em escada da situação à dor, acha o problema avançado (o que as tentativas antigas criaram de pior). | *"Antes de te responder: quando você diz [palavra dele], o que isso significa pra você?"* / *"Já tentou resolver antes? O que não funcionou?"* |
| **3. Implicação** | Amplia a consciência do custo de ficar como está e qualifica a intenção; o lead verbaliza o custo, você só pergunta. | *"De 0 a 10, quanto você quer resolver isso hoje?"* |
| **4. Conexão (espelho)** | Mostra que entendeu antes de apresentar; devolve a situação nas palavras dele e confirma. | *"Deixa eu ver se entendi: você tá em [situação], tentou [X], deu [efeito colateral], e o que quer de verdade é [desejo]. É isso?"* |
| **5. Apresentação + reframe** | Conecta só o que amarra com o que ele disse e vira a crença dele em camadas até ele concluir sozinho que precisa. | *"Isso que você me diz, você já sabe. O problema não é informação. Se você sabe e o número ainda é [resultado ruim], a falta é aplicar do jeito certo."* |
| **6. Isolamento** | Confirma que, com valor e ajuste claros, falta só investir; separa objeção real de decorativa, ANTES do preço. | *"Antes de eu te passar o investimento: se a gente resolver [as dores] em [prazo], com [formato], e o valor fizer sentido, faz sentido trabalhar junto?"* |
| **7. Fechamento** | Operacionaliza a venda (preço, condição, coleta do sinal); quem chegou aqui já decidiu. Uma jogada de encaminhamento no máximo, depois para. | *"O investimento é R$[valor] à vista ou [Xx] de R$[parcela]. [O que inclui em 1 frase]. E a gente já garante sua entrada pra começar."* |

### As 3 falas-assinatura (o piso que não sai raso)

Estas três carregam a assinatura da condução. Adapte ao nicho, mantenha o miolo. Genérico do tipo "me conta como tá sua rotina" ou "de 0 a 10 quanto quer resolver" sem o corte é a versão rasa e perde a assinatura. O repertório denso vive em `references/script-builder.md` e `references/conducao-na-pratica.md`.

> **A conta da padaria** (quando o lead pede preço cedo, na fase 2):
> *"Você já foi num restaurante? Trazem a conta antes ou primeiro perguntam o tamanho da sua fome? Aqui é igual, não consigo te passar valor sem entender o que você precisa. Hoje, qual é a maior dificuldade no seu [problema]?"*

> **O reframe "saber não é aplicar"** (fase 5, movimento 1):
> *"Isso que você me diz, você já sabe. O problema não é informação. Quem mais sabe de [tema] muitas vezes é justo quem não colhe [resultado]. Se você sabe e o número ainda é [resultado ruim], a falta não é saber, é aplicar do jeito certo."*

> **O termômetro que qualifica** (fase 3):
> *"De 0 a 10, quanto você quer resolver isso hoje? ... 7? Nota ruim, hein. Você me disse que [o que importa] importa muito. Eu não arranco com um 7."*

### Regras universais entre fases

- Nunca apresenta antes de entender: pular a fase 2 é pitch no vazio.
- **Nunca apresenta sem saber quanto o lead tem.** A leitura de capacidade é pré-condição da fase 5.
- Nunca revela preço com dúvida aberta: pular a fase 6 é objeção garantida.
- **Antecipa as objeções clássicas ANTES do preço** (decisor, financeiro, "vou pensar", concorrente); enquanto são hipotéticas, morrem baratas.
- Nunca força quem não tem perfil: encerra leve, e isso é vitória.
- Uma oferta por vez: principal, condicional, secundária.
- Tom de comando, nunca de súplica. A régua 7-38-55: a palavra é cerca de 7% do impacto, o tom cerca de 38%, o corpo cerca de 55%. Incisivo com semblante leve, nunca agressivo.
- Nunca cala depois do preço: ancoragem negativa. Diz o número com leveza e emenda no próximo passo.
- **"Faz sentido pra você?" é banido do fechamento.** Pergunta de validação devolve o bastão; engaje com "o que você entendeu disso?".
- **Conversão é PAGAMENTO**, dinheiro ou sinal na conta, medido sobre os aprovados no diagnóstico: até 20% é péssimo, 30% é sinal de vida, 40% está no jogo, 50% é bom.

---

## Ação 2 · OBJEÇÃO (isola primeiro, responde depois)

**O que faz:** entrega a resposta pronta pra objeção que o lead acabou de dizer, isolada antes de respondida.

**Precisa de:** a objeção literal, como o lead escreveu ou falou · a oferta e o preço · onde na conversa ela apareceu.

**Sem o insumo:** pergunta única, "me cola a frase exata que ele mandou", porque a resposta muda inteira conforme a palavra que ele usou.

**Entrega:** `02-resposta-objecao.md`, com o isolamento, a resposta em bloco copiável e os 2 caminhos esperados depois dela. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/banco-de-objecoes.md` (as 30 objeções e as frases de poder).

**Isola antes de responder, sempre que der:** *"É só isso ou tem mais coisa emperrando?"*

| Objeção | Resposta de cor |
|---|---|
| **"Tá caro"** | *"Caro comparado com quê? Com continuar [problema] por mais [tempo]? Se não cabe à vista, tenho condicional: parte agora, parte quando [resultado]. Facilita?"* |
| **"Preciso pensar"** | *"Claro. Pensar sobre o quê, o método ou o investimento? Às vezes é uma pergunta que eu respondo agora."* |
| **"Preciso falar com [sócio/cônjuge]"** | *"Faz sentido. Quando vocês conversam? Se quiser, faço uma call com vocês dois, ou te mando um resumo pra levar."* |
| **"Já tentei e não deu certo"** | *"Por isso faz sentido. O que você tentou ensinava [a solução errada]. Aqui é o oposto. Você não falhou, tentou o método errado."* |
| **"Não tenho tempo"** | *"Por isso o formato é esse. Separa [X] por semana. Consegue ou não?"* |
| **"Funciona mesmo?"** | *"Funciona pra quem aplica como foi pensado. Se é pra você, eu descubro nas perguntas. O que você já tentou antes?"* |
| **"Tem desconto?"** | *"Esse já é o menor valor. Não abaixo porque não quero te filtrar pelo desconto."* |

Se a mesma objeção volta duas vezes, é outra coisa: *"Acho que tem algo além disso. O que é?"*. Não nomeou, é curiosidade e não comprador: encerra com leveza.

---

## Ação 3 · DIAGNÓSTICO DA CONVERSA (o laudo do que empacou)

**O que faz:** lê a conversa que emperrou e devolve onde a condução saiu do trilho, mais o próximo passo concreto.

**Precisa de:** a conversa colada, o print ou a transcrição · o ticket e o que foi oferecido.

**Sem o insumo:** sem a conversa, não há laudo. Pergunta única: "cola a conversa, do começo ou do ponto em que virou".

**Entrega:** `03-laudo-conversa.md`, com a fase em que emperrou, o erro nomeado, o que fazer agora e a mensagem de retomada pronta. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/analise-de-conversa.md`.

**Profundidade:** `references/caixa-de-ferramentas-closer.md` (a régua de autoavaliação de call e o modelo de laudo) · `references/funil-e-metricas.md` (quando o problema não é a conversa e sim o funil: lead, reunião, venda, ticket, taxa de ganho).

---

## Ação 4 · COPILOTO AO VIVO (a exceção ao documento)

**O que faz:** dá a próxima jogada agora, enquanto o dono está no meio da conversa real.

**Precisa de:** a última mensagem do lead · onde a conversa está.

**Sem o insumo:** pergunta única e curta, sem interromper o ritmo: "o que ele disse por último?".

**Entrega:** aqui, e só aqui, a resposta não é um documento. O formato é: **diagnóstico em 1 linha → mensagem pronta em bloco copiável → 1 linha com os 2 caminhos esperados.** UMA jogada por vez, nunca um roteiro inteiro. O STOP é implícito, porque o dono está na conversa e decide na hora.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/copiloto-tempo-real.md`.

---

## Ação 5 · COLETA DO SINAL (entre o sim e o dinheiro)

**O que faz:** fecha o buraco entre o "sim" e o dinheiro na conta, com o sinal coletado na própria conversa.

**Precisa de:** o sim já dado, ou o lead na fase 7 · a condição de pagamento e o valor do sinal.

**Sem o insumo:** sem a condição definida, pergunta única: "qual entrada você aceita pra começar hoje?". **Se o dono não respondeu ou não definiu valor de sinal, o roteiro NÃO inventa entrada parcial: ele coleta o pagamento integral da condição que o lead escolheu** (à vista ou a primeira parcela do parcelamento já ofertado), e deixa marcado `[valor de sinal a definir pelo dono]` para quando ele quiser abrir essa porta.

**Entrega:** `05-coleta-sinal.md`, as jogadas escolhidas pro caso, cada uma com a fala pronta. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/comercial-1a1-e-conta-de-padaria.md` (as 4 etapas, o diagnóstico pelos números do próprio comprador e as 6 falas de campo que pegam o sinal na hora).

"Manda o link" não é coleta. Pegar o sinal na própria reunião é uma habilidade separada de vender. As 6 jogadas: a energia leve e o silêncio que resolve · a condição única da call gravada · o sinal como prova de comprometimento · negociar o sinal possível · plano A, B e C de pagamento · o "faço depois" convertido na hora. Tudo segue a lei: escassez real nunca inventada, o sinal é prova de comprometimento e não armadilha, e o não se respeita.

---

## Ação 6 · PÓS-VENDA (a venda que gera as próximas)

**O que faz:** transforma o cliente novo em indicação, depoimento e prova pra próxima venda.

**Precisa de:** o cliente que fechou e há quanto tempo · o resultado que ele já teve, mesmo parcial.

**Sem o insumo:** entrevista curta de 3 perguntas: quando ele fechou · o que já mudou pra ele · ele já falou de você pra alguém.

**Entrega:** `06-pos-venda.md`, com o pedido de indicação, o roteiro de coleta de depoimento e a troca bônus por prova. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/indicacoes-pos-venda.md`.

---

## Ação 7 · CABEÇA DO VENDEDOR (antes de qualquer técnica)

**O que faz:** trata o que emperra o dono antes do script: o sistema de crença e a confiança no preço.

**Precisa de:** onde ele sente que perde a firmeza (na hora do valor, no silêncio depois do preço, no "vou pensar").

**Sem o insumo:** pergunta única: "em que ponto exato da conversa você sente que perde o chão?".

**Entrega:** `07-cabeca-vendedor.md`, o diagnóstico e o treino da semana. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/mentalidade-do-vendedor.md`.

**Profundidade:** `references/perfis-de-closer.md` (os 5 perfis, a autoavaliação e os 4 pilares que se treinam; no estudo com cerca de 6.000 vendedores, o perfil desafiador aparece em 39% dos de alta performance contra 7% do perfil amigão).

---

## Contrato de entrega (vale em todas as ações, menos a 4)

O resultado sai como **UM documento markdown consolidado e completo**. Se o ambiente renderizar markdown, mostre o documento inteiro ali; senão salve um arquivo `.md` no disco e cite o caminho completo na resposta. A condução vai em mensagens curtas, sem markdown pesado. A peça e a copy moram no documento; as perguntas, as escolhas e os STOP moram no chat. Ao parar no STOP, você mostra ou atualiza o documento inteiro e pergunta "ajusto?", nunca reescreve a peça em pedaços no corpo da conversa. Sem o documento completo entregue, a skill não terminou.

## Pré-flight de copy (releia imediatamente antes da primeira linha)

A copy nasce da terça-feira à noite DO LEITOR. A regra é checagem, nunca geradora: escreva a partir da cena e da emoção dela, com voz de mesa; a regra confere depois. Reprovou, regenera do zero, porque frase editada herda o esqueleto do defeito.

1. **Munição na mão:** verbatim e prova real do dono na frente; sem munição, pergunta, jamais inventa.
2. **Leitura única:** uma leitura em voz alta, sem reler; valência única; sintaxe linear; 1 operação mental por frase.
3. **Mundo do leitor:** componente do método vira dia, hora, lugar e fala do cliente; rótulo abstrato só entre aspas, como palavra do inimigo.
4. **Compressão gramatical: cota zero.** Verbo da relação por extenso; a força é do fato.
5. **Voz de mesa, não palco:** a colocação inteira é fala real; metáfora morta entra, figura de escritor não.
6. **Prova com atribuição exata**, do banco de provas do dono, nunca fundida; renda do leitor só em terceira pessoa.
7. **Anti-IA:** zero travessão, zero da família banida, zero verbo genérico de transformação, zero frase de moldura.
8. **Teto do formato conhecido ANTES**, contado durante, não consertado depois.

## Gate de qualidade (roda antes de entregar, sempre)

**Régua de títulos (roda antes do resto do gate).** Todo título que sai desta skill passa pela régua `shared-references/crivo/07-regua-de-titulos.md`, R1 a R7. Rode a régua sobre a primeira linha de cada mensagem de abertura e de cada retomada do script, que é o que decide se a pessoa responde. A checagem sai colada num arquivo do disco que o dono abre, uma linha por título, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a entrega antes da análise de conteúdo.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Molde endereçado a pessoa nomeada exige o insumo dela aberto:** rode `grep -n '<Nome>' <insumo>` e cole a saída antes da fala, na forma do bloco "Fala atribuída ao destinatário" de `shared-references/crivo/08-consentimento.md`. Fala atribuída sem trecho literal do insumo reprova.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


| Check | Passa se |
|---|---|
| **Ancoragem do verbatim** | toda fala entre aspas que se declara real foi encontrada literalmente na fonte do dono e mostrada; sem fonte, a peça sai marcada `[A CONFIRMAR]` e nunca se declara verbatim |
| **Documento completo** | as 7 fases inteiras num só documento, até a coleta do sinal; nada foi deferido pro próximo passo |
| **Ordem das fases** | ninguém apresentou antes de entender, nem revelou preço com dúvida aberta |
| **Capacidade lida** | a leitura de quanto o lead tem aconteceu antes da fase 5 |
| **Fronteira respeitada** | não abriu conversa fria nem qualificou lead frio (é da soft-vendas-sdr), não escolheu campanha do mês (é da soft-vendas-estrategias), não redigiu contrato (é da soft-vendas-contratos) |
| **Frase banida fora** | "faz sentido pra você?" não aparece no fechamento |
| **Nicho regulado** | quando a profissão do dono é regulada por conselho, o roteiro roda o gate regulado antes de sair. **Personal trainer e educação física entram como saúde regulada, inclusive em conversa privada de venda:** o script pode falar de processo, método e experiência, e **nunca promete resultado garantido, prazo cravado de resultado nem cura**; projeção vira faixa com "pode", e a peça sai com o aviso de confirmar a regra atual no conselho. Conversa privada não é exceção: o que o conselho proíbe em anúncio, esta skill também não escreve na DM |
| **Prova real** | nenhum case, número ou depoimento inventado; furo vira `[A CONFIRMAR]` no lugar exato |
| **Saída em arquivo** | a peça está num `.md` nomeado, com o caminho citado na resposta |
| **Anti-IA** | com shell, roda o linter anti-IA do ambiente sobre o arquivo e exige saída limpa; sem shell, varre o texto inteiro atrás do travessão longo e da família do verbo-freio banida pela régua anti-voz, inclusive em títulos e rótulos, e reescreve cada ocorrência |
| **VEREDITO** | é o pior item; um ✗ refaz o item, não o documento inteiro |

Onde a pasta trouxer `shared-references/crivo/` e `shared-references/filtro-anti-ia/`, eles são a régua completa: o crivo roda antes de mostrar (ancoragem, simulação na pele do avatar, veredito pelo pior bloco) e o artefato dele sai junto do documento no STOP. Narrar que passou no crivo, sem artefato nenhum na tela, não conta como entrega.

**Qual artefato, e por quê, porque script de venda é o caso especial.** O gate CUB cheio foi escrito pra copy que o leitor lê (case, promessa, oferta), e a maior parte de um script é **fala-mecânica**: descoberta, isolamento, termômetro, transição. Fala-mecânica não roda a tabela cheia, roda a régua curta (soa natural lido em voz alta, não é pomposo, não vaza framework), e isso está em `shared-references/crivo/03-gate-cub.md`. Então **o artefato de um script é um relato de régua, não uma tabela cheia**: 3 a 6 linhas dizendo quais blocos são fala-mecânica e que passaram na régua curta, quais blocos carregam prova ou promessa (o case, a oferta, a fase 5, a fase 7) e a tabela CUB SÓ desses blocos, mais o veredito pelo pior item. Tabela cheia num script inteiro é over-engineering e reprova por rigor errado; relato de régua sem nomear os blocos que rodaram a tabela cheia é entrega incompleta. Nas ações de copy pura (a mensagem de pós-venda da Ação 6, por exemplo) vale a tabela cheia normal.

## O que esta skill NÃO faz

Em toda rota abaixo: se a outra skill não estiver instalada, esta faz o mínimo aqui e diz que fez, com o pedaço mais fino marcado `[A CONFIRMAR]`.

- **Abrir conversa fria, prospectar na DM, qualificar de leve, agendar, operar o CRM, montar agente de IA** → **soft-vendas-sdr**. Esta skill começa quando o lead já chega quente.
- **Escolher a campanha do mês, plano de jogadas, estratégia de lançamento** → **soft-vendas-estrategias**.
- **Contrato depois do sim** → **soft-vendas-contratos**. **Proposta em site premium com validade** → **soft-vendas-proposta**.
- **Carta, VSL, mini webinar, landing** que aquece antes da conversa → `soft-funil-*`. **O webinar** → `soft-webinar`.
- **Posicionamento, oferta, PUV, mecanismo, voz** → `soft-plano-posicionamento`. Sem ele, a entrevista rápida de 5 perguntas cobre o mínimo e a venda segue.
- **Conteúdo de feed** → `soft-conteudo-*`.

## Anti-patterns

| Erro | Por que quebra | Faz assim |
|---|---|---|
| Deu preço antes do isolamento (fase 6) | Dúvida aberta mais preço é objeção garantida | Isola primeiro, revela valor só com o caminho limpo |
| Faz o lead repetir o que já contou | Queima a primeira impressão e expõe que ninguém conversa | Abre lendo a nota, ecoa a qualificação, entra direto no diagnóstico |
| Cala depois de dizer o preço | Ancoragem negativa: o cérebro ecoa o custo e apaga o valor | Diz o número com leveza e emenda no próximo passo |
| Aceita "faço o Pix depois" | Sai da conversa quente, esfria, vira cobrança por mensagem | Resolve na hora, ou o "mas" vira objeção pra tratar ali |
| Script com aspas inventadas | Reprova na ancoragem, soa genérico e não fecha | Puxa falas reais da fonte do cliente; a primeira linha nasce de uma delas |
| Follow-up eterno sem pedir sim ou não | Queima o aquecimento e a autoridade | Pede a decisão na conversa |
| Apresentou o método inteiro na fase 5 | O lead desengaja: virou aula, não venda | Só o que amarra com o que ele disse, mais 1 reframe |
| Apresentou sem saber quanto o lead tem | Pitch no escuro, e a melhor munição foi gasta à toa | Leitura de capacidade antes da fase 5 |
| "Faz sentido pra você?" na hora de fechar | Pede aprovação, devolve o bastão, abre porta de fuga | "O que você entendeu disso?", com o número dele na escada de fechamento |
| Mede conversão sobre "call feita" | Mistura filtro com perda, e o número mente | Conversão é pagamento sobre aprovados no diagnóstico |
| Nome de framework vazando pro lead | Soa manual e mata a naturalidade | O framework opera invisível, vira pergunta na linguagem do nicho |
| Entrega as fases 1 a 3 e defere o resto | Corta justo o núcleo da skill | Documento completo, um STOP só |

## Handoff

**Pra trás:**
- Lead frio, prospecção, qualificação, agendamento → **soft-vendas-sdr**.
- Pré-qualificador que falta → `soft-funil-carta` ou `soft-funil-miniwebinar`.
- Oferta ou PUV indefinida → `soft-plano-posicionamento`.

**Call que terminou sem o sinal**, os 3 desfechos possíveis, nesta hierarquia:
1. **Fecha na própria call**, lapidando cada pendência dentro dela: "vou ver o cartão" vira "abre o app agora"; "falo com o sócio" vira "liga pra ele, eu espero". Esta é a rota padrão.
2. **Encerra com dignidade e libera**, quando não fechou e não há justificativa. A pergunta que decide é *"o que muda de hoje pra amanhã?"*; sem resposta, encerra.
3. **Proposta de 7 dias, exceção e não etapa.** Só pra call que sobreviveu ao método com motivo real (processo formal de empresa, rito de decisão a vários com sinceridade demonstrada), e sempre com compromisso amarrado na própria call: dia e hora do retorno mais condição que expira. A **soft-vendas-proposta** materializa a oferta; o follow-up desses 7 dias é do closer, que cobra no dia 5 e fecha ou encerra no dia 7. Proposta virada rotina significa que as reuniões estão sendo feitas pra gerar follow-up: conserta a reunião, não a proposta.

**Pra frente:**
- Venda fechada → contrato na **soft-vendas-contratos**.
- Os números (lead, reunião, venda, ticket) voltam pro orquestrador, que calibra a rotina.
- Cliente novo → o pós-venda abre indicação e depoimento, que viram prova pra `soft-plano-posicionamento` e pras `soft-conteudo-*`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

- **Passo 2 da checagem:** rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída; `exit` diferente de 0 reprova a entrega inteira.
