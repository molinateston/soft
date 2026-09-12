---
name: soft-sistema
description: >-
  Constrói qualquer coisa com código, do pedido falado até no ar com prova, no ciclo de 5 fases (spec com parada pra aprovação, arquitetura, construção, revisão contra o sistema real, entrega provada). Cinco tipos: sistema multiusuário, painel de apresentação, site, ferramenta ou dashboard, e automação ou integração. Use quando o pedido for: "constrói um sistema pra mim", "quero um painel pra apresentar pro cliente", "faz um site", "monta uma calculadora", "automatiza isso aqui", "liga essa API na outra", "mexe no sistema que você fez". NÃO use pra: publicar um .md como Google Doc (soft-google-docs); faxina de disco no servidor (soft-organizacao-vps); instalar ou publicar o kit de SDR pronto (soft-sdr-kit); rotina, OKR e ritual de time (soft-gestao-agil); copy e conteúdo (soft-conteudo-*); carta e landing (soft-funil-*); script de venda (soft-vendas-*); arte e PNG (soft-designer); edição de vídeo (soft-editor-video). Leia e siga o fluxo inteiro do SKILL.md.
---

# Do pedido falado ao sistema no ar, com prova

Esta skill é o braço técnico: sai de um pedido dito em voz alta e chega em **qualquer coisa com código pronta, no ar, com prova**, sem o dono corrigir no meio. Constrói ou edita um sistema, um painel de apresentação, um site, uma ferramenta ou uma automação. O mesmo ciclo e o mesmo rigor valem pros cinco. Marca-neutra: cor, fonte e marca vêm do cliente de quem opera. Não faz copy de venda, arte solta nem edição de vídeo.

**Nota de gestão da operação (relato de operador, sem prova; contexto, não escopo desta skill).** O bloco de gestão que sustenta uma operação de resposta direta rodando (CERP: cultura, estrutura, rotina, processos; CBS, o compromisso binário semanal de 1 a 3 dias, feito ou não feito; as 3 reuniões por nível, daily operacional, weekly tática por setor, monthly estratégica da liderança; a régua de 8 a 10 pessoas em que o dono sai do operacional) é rotina e ritual de time: mora em `soft-gestao-agil`, não aqui. Esta skill constrói o que tem código; a gestão da operação é vizinha.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Todo furo que a dona não fecha vira pedido endereçado.** Mesmo padrão `PEDIDO-PARA-QUEM-PUBLICA`: o pedido abre com as 3 linhas pro dono (`O que é este arquivo`, `Pra quem mandar`, `O que essa pessoa vai fazer`), traz o que fazer em cada furo, quem faz e onde devolver, sem linha de terminal pra dona, e o `RELATO` sai sem comando. Cole `furos que dependem de terceiro: N · endereçados no pedido: N`, iguais.

**A saída de máquina entra literal na prova, e reescrevê-la invalida a linha.** A coluna de saída lida no DOM, no shell ou na API recebe a string literal, com entidades e espaços como vieram (`R$&nbsp;2.880`). Reescrever por extenso, por arredondamento ou por qualquer gate de texto invalida a linha inteira, porque a coluna existe pra provar o que a máquina fez. Colisão com um gate de texto resolve com a linha `colisão de gate`, nunca alterando a saída. Cole `leituras coladas: N · literais: N`, iguais. Some: arquivo de prova e pasta de especificação (`specs/`, `PROVA-*`) entram em `conferencia/`; a raiz recebe o entregável, o `RELATO` e o pedido endereçado, e mais nada.

**O HTML se confere no corpo montado, nunca no arquivo.** Rode o grep de marcador e de frase de bastidor (`entra aqui|preencher|antes de publicar|placeholder|a definir|pendente`) sobre o **texto que o HTML renderiza**: página que monta o corpo por script esconde o marcador da varredura estática, e a peça pública não carrega bastidor renderizado. Cole `marcadores no corpo renderizado: 0 · frases de bastidor renderizadas: 0`.

**A peça interativa abre calculada.** O estado inicial carrega valores de partida visíveis e rotulados na tela como exemplo, com a conta já resolvida. Valor de partida cumpre papel de legibilidade e sai marcado como exemplo na interface, nunca como medição. **Estado inicial que exibe instrução no lugar do resultado reprova o gate visual.** Cole `estado inicial: <o que aparece no bloco de resultado> · é um número calculado: sim/não`.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício de ponta a ponta: a pergunta zero, a spec fechada com a parada pra aprovação, a arquitetura, a construção em escopos, uma revisão que reprovou duas vezes seguidas e o que aconteceu na terceira, o pacote de prova real com as saídas coladas, e o mesmo pedido resolvido **num ambiente sem infraestrutura nenhuma**, com o documento de saída inteiro.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Como aqui o trabalho é construir com código, valem duas delas:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o que quer e eu construo). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pra construção com o que o dono colou. Se faltar um dado que a spec não vive sem (o que o sistema faz, quem usa), pergunta AQUELE dado e segue, sem repetir a spec inteira. Na EDIÇÃO, a Pergunta Zero e o estudo do sistema real vêm antes de qualquer modo.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a spec com o dono, uma pergunta de cada vez, e constrói com o que ele for dando.

A pergunta do modo é UMA por build.

**Oferece refinar no fim:** depois de entregar provado, fecha com UMA linha: "quer que eu ajuste uma tela? adicione um campo? mude o fluxo? me diz o que mexer que eu volto no ciclo só nessa parte."

## PERGUNTA ZERO: a primeira coisa, sempre

Antes de qualquer outra pergunta: **sistema do ZERO, ou EDIÇÃO de um que JÁ EXISTE?**

- **Do zero** → siga direto pra Fase 1 (Spec).
- **Edição** → **não entreviste antes de estudar.** Primeiro localize e estude o sistema real, e só então pergunte sobre as mudanças:
  1. Pergunte **qual** sistema, o endereço, onde ele roda.
  2. **Localize o repositório e o código real** (na organização do dono, no servidor, no domínio).
  3. **Estude o sistema inteiro.** Em paralelo se o ambiente tiver delegação, em sequência se não tiver. Mapeie telas, tabelas, rotas, serviços.
  4. **Não há repositório?** Crie na hora e registre o estado atual **antes de mexer**. É o ponto de retorno.
  5. Só então **entreviste sobre as mudanças**, com perguntas **informadas** pelo que você estudou, citando telas e tabelas reais ("na tela de clientes hoje não existe a coluna de status; você quer ela na tabela principal ou numa visão separada?"), nunca perguntas genéricas.

Editar sem estudar antes é o erro mais caro desta skill, porque gera mudança que quebra o que já funcionava e o dono só descobre em produção.

## Roteamento por pedido

| O dono pediu | Tipo de build |
|---|---|
| "um sistema onde meus clientes entram", "cada cliente vê só o dele", "login, banco, cadastro" | **SISTEMA / APP** |
| "um painel pra eu apresentar na reunião", "quero mostrar o diagnóstico e a proposta" | **PAINEL DE APRESENTAÇÃO** |
| "um site", "uma página institucional", "um portal" | **SITE / PÁGINA RICA** |
| "uma calculadora", "um painel de números", "uma ferramenta interna", "um gerador" | **FERRAMENTA / DASHBOARD** |
| "automatiza isso", "liga essa API na outra", "um robô que roda todo dia", "quando chegar X faz Y" | **AUTOMAÇÃO / INTEGRAÇÃO** |
| "mexe no que você já fez", "adiciona uma tela", "está quebrado" | **qualquer um dos cinco, entrando pela PERGUNTA ZERO em modo edição** |

Pedido ambíguo ("faz um negócio pra mim aí"): pergunte **uma coisa só**, quem vai usar isso e o que essa pessoa precisa conseguir fazer. A resposta decide o tipo, e nenhuma outra pergunta é necessária antes dela.

## Como ler cada fase

Cada fase abaixo traz o mesmo bloco fixo: **O que faz** · **Precisa de** (o insumo e de onde vem) · **Sem o insumo** (o caminho concreto quando falta) · **Entrega** (o que sai, com nome de arquivo) · e a **parada** onde o dono aprova, quando houver.

## ⚠️ ENTREGA: três ambientes, um padrão de qualidade

O entregável muda com o ambiente onde a skill roda; a **qualidade não**.

- **Sem shell, só conversa:** entrega a **spec + a arquitetura + o plano visual** como **um documento markdown consolidado**; se o ambiente renderizar markdown, mostre. Não finge que subiu nada. Diz, em uma linha, o que a infraestrutura somaria. O documento inteiro está em `references/EXEMPLO-FIM-A-FIM.md`, na seção do ambiente sem infraestrutura.
- **Com shell e acesso a arquivo:** roda o ciclo inteiro (versionamento, construção, publicação, prova) e entrega o **endereço + o repositório + a prova**.
- **Com ponte de arquivo** (o ambiente anexa o que você salva): igual ao shell; o entregável vai citado por caminho completo na resposta, e a condução vai em mensagens curtas.

Doutrina **adaptável ao ambiente**: o melhor resultado com as ferramentas que o usuário tem. Com a infraestrutura, executa e entrega no ar. Sem ela, entrega a spec, a arquitetura e o plano de construção com a mesma qualidade, e nomeia o que a infraestrutura somaria. Nunca promete o que não pode provar.

## Quando não há delegação disponível

A skill fala em "escopos paralelos" e "um agente por escopo". Isso é uma otimização, não um requisito. Sem delegação, nada se perde e nada se corta:

- **Você percorre os mesmos escopos, em sequência**, na ordem em que um libera o outro: primeiro o que os outros dependem (o formato dos dados, o contrato das rotas, os tokens de cor), depois o resto.
- **Cada escopo continua isolado**: termine um, registre o estado, e só então comece o seguinte. Não abra dois ao mesmo tempo no mesmo arquivo.
- **A disciplina do prompt autossuficiente vira disciplina de nota:** antes de começar cada escopo, escreva em 3 linhas o que ele precisa entregar e contra que requisito da spec ele será conferido. É a mesma informação que iria pro agente delegado.
- **A revisão não muda em nada.** Ela roda contra o sistema real, escopo por escopo, igual.
- **O que muda é só o tempo**, e vale dizer isso ao dono em uma linha, sem transformar em desculpa.

Na fase de estudo de um sistema existente, a mesma regra: sem delegação, leia as telas, as tabelas e as rotas em sequência, começando pelo formato dos dados, que é o que explica o resto.

## Duas leis que vêm antes de tudo

1. **Constrói EXATAMENTE a spec. Nada além, nada aquém.** Faltou requisito? Pergunta ou marca `[A CONFIRMAR]` na spec. Não inventa funcionalidade "que seria legal", não corta requisito "pra simplificar". A revisão compara requisito por requisito.
2. **Só afirma o que provou.** "Está no ar" só depois do acesso real, da captura de tela e da consulta ao banco. "Passa na revisão" só depois de comparar contra o sistema real rodando, não contra o código lido. Sem prova, é `[NÃO VERIFICADO]`.

## O LOOP: 5 fases

A Fase 1 é conversada (uma pergunta por vez). Do fim da Spec em diante, **o loop roda autônomo após o "pode ir"**. Ninguém pede permissão pra iterar; só pra **mudar escopo** ou pra **ação destrutiva** (dropar tabela, apagar deploy, force-push).

### Fase 1 · SPEC (entrevista, uma pergunta por vez)

**O que faz:** fecha o contrato do que vai ser construído, e é contra ele que a revisão compara depois.

**Precisa de:** o objetivo, os requisitos tela a tela, as restrições e a definição de pronto, todos perguntados ao dono · a marca do cliente (cor, fonte, logotipo), do perfil ou banco do agente quando existir.

**Sem o insumo:** o dono não sabe descrever a definição de pronto (é o mais comum): pergunte "me descreve o dia em que isso estiver funcionando: quem abre, o que essa pessoa faz, e o que acontece no fim?". A narrativa dele vira o teste. Marca do cliente ausente: use o padrão visual da skill e marque `[A CONFIRMAR: marca do cliente]` na spec, sem parar por isso.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `specs/<nome>.md`, com objetivo, requisitos numerados, restrições, definição de pronto, e `[A CONFIRMAR]` em todo furo.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

Entrevista **uma pergunta por vez** até fechar: **objetivo** (que problema o sistema resolve, pra quem), **requisitos** (o que ele faz, tela a tela, dado a dado), **restrições** (marca do cliente, prazo, integrações, o que NÃO fazer) e **definição-de-pronto** (o teste que, passando, encerra: "o cliente loga, vê o diagnóstico, assiste o vídeo e aceita a proposta"). Uma pergunta por vez porque uma parede de 12 perguntas faz o dono responder no atropelo e a spec sai furada.

Salva em `specs/<nome>.md`. Ver `references/frente-war-room.md` e `references/frente-produto.md` pra saber **quais** requisitos cada frente costuma ter (não reinventa a anatomia a cada projeto).

**A primeira linha da spec repete o objeto, com as palavras do dono.** Antes de qualquer requisito, a spec abre dizendo **o que o sistema calcula ou faz, e quem abre a tela**, nas palavras que o dono usou. Se o pedido nomeia a coisa ("uma calculadora de quanto custa parar de treinar", "um painel de entregas atrasadas"), **esse nome é o objeto e não se troca por um mais útil**: construir uma ferramenta melhor pra uma pergunta que ninguém fez é a falha mais cara desta skill, porque obriga a refazer a peça inteira. Achou que outro objeto serviria mais? Diga isso em 1 linha no STOP e deixe o dono decidir; não decida por ele.

**A checagem de objeto NÃO compara títulos, compara SAÍDAS.** Título igual com fórmula diferente é o jeito mais comum de trocar o objeto sem perceber. Escreva uma linha embaixo da outra, no relatório: (a) **o substantivo que o pedido pede como resultado** ("custo", "prazo", "quantas vagas", "quanto sobra"); (b) **a unidade que a fórmula devolve** ("R$", "sessões", "dias", "minutos"). **Se as duas não forem a mesma coisa, você trocou o objeto: pare no STOP e pergunte, não construa a versão que você acha melhor.** Uma calculadora cujo H1 diz "quanto custa" e cuja fórmula devolve "sessões não realizadas" reprova, por mais bem feita que esteja. Cole as duas linhas antes de seguir, junto da comparação de público entre a frase do pedido e a primeira linha da spec.

**Checagem de sujeito, ao lado da checagem de objeto.** Escreva quem está na tela quando a página abre: `visitante que ainda não comprou` ou `cliente que já comprou`. Embaixo, escreva as entradas que a fórmula exige, uma por linha. **Se alguma entrada só existe pro outro sujeito** (o preço de um produto que o visitante ainda vai conhecer, um dado de dentro da área de membros, o número do pedido dele), **a fórmula está escrita pra pessoa errada e reprova**: pare no STOP e pergunte. Uma calculadora de aquisição que pede à visitante assumir já ter pago o programa pra então mostrar quanto ela desperdiça acertou a unidade e trocou a pergunta. Cole as duas linhas no relatório, junto das da checagem de objeto.

**Varredura de faixa, obrigatória em toda fórmula com entrada do usuário, e ela roda na SPEC, antes do HTML.** Rode a varredura contra os limites PROPOSTOS na spec (o mínimo, o máximo e o passo de cada campo) e cole a tabela ali, ainda na Fase 1. **Teto de campo que produz saída absurda é erro de spec, e corrigir spec custa uma linha; corrigir HTML custa uma rodada** (um teto de 20 tentativas por 24 semanas devolve 480 semanas, mais de nove anos, e só aparece quando alguém roda os extremos). Refaça a varredura no fim, sobre o HTML pronto, para provar que a implementação bate com a spec. Nos dois momentos, rode a fórmula em 5 pontos: os defaults que a tela já vem preenchida, o placeholder de cada campo, o mínimo de cada campo, o máximo de cada campo, e um caso médio realista. Cole a tabela `entrada | saída | a saída defende o objetivo da página?`, com a conta escrita ao lado de cada linha, não só o resultado. **Saída que fica em zero, em valor irrisório, ou que argumenta contra a oferta em qualquer um dos 5 pontos reprova a fórmula, não a copy: reescreva a conta.** O teste com os defaults da tela tem que produzir resultado plausível; uma tela que imprime "R$ 3" de economia sob um programa de mil e quinhentos é um argumento contra a oferta em corpo grande, na página de conversão. **Número de destaque nunca nasce de subtração cujo minuendo o usuário controla e cujo subtraendo é o preço.** **A coluna de veredito é bloqueante, não descritiva.** Para cada um dos 5 pontos responda `a saída defende o objetivo da página? sim/não`, e **um único `não` reprova a fórmula e manda reescrever**, nunca anotar e seguir. Numa página de aquisição, defender significa uma coisa exata: a saída não entrega à visitante um argumento contra o próximo passo em nenhum ponto da faixa de entrada, nem no mínimo, que é onde mora quem começou e parou. **O preço da oferta nunca entra na conta:** compare o custo do problema consigo mesmo ao longo do tempo, porque toda subtração que tem o preço como subtraendo vira desconto disfarçado nas entradas baixas e faz a página dizer à visitante que sair sem comprar sai mais barato. Convidar a aumentar os números até a conta inverter não conserta: o ponto já foi lido. Cole a tabela com a coluna e a linha `pontos com veredito não: 0`; qualquer valor diferente de zero reprova a entrega. **E esta regra mora aqui, no arquivo da skill, não na conversa da rodada:** conserto que fica só na entrega volta como regressão na próxima. **Os 5 pontos rodam um a um, e a linearidade da fórmula não dispensa nenhum:** o que a varredura mede não é a aritmética, é a FRASE que acompanha o número em cada ponto, e uma conta linear pode trocar de moldura no meio da faixa. Cole uma linha por ponto, nesta forma exata: `entrada | saída lida no DOM | frase que acompanha | a saída defende o objetivo da página? sim/não`. A saída sai LIDA NO DOM da tela renderizada, nunca recalculada de cabeça. São 5 linhas obrigatórias, mais `pontos varridos: 5 de 5` e `pontos com veredito não: 0`. **Menos de 5 linhas reprova a Ação**, e a justificativa de que a fórmula é linear não substitui nenhuma delas.

**Campo de contato sem valor real do dono sai inerte.** Botão, link ou formulário que depende de um dado que o dono ainda não deu (número de mensagem, e-mail, URL de checkout) sai como botão inerte com a etiqueta do que falta, nunca como link vivo apontando pra número de exemplo ou pra endereço vazio. Placeholder de teste de outro insumo não é valor funcional. Um botão que parece funcionar e leva a lugar nenhum é pior que um que avisa que falta o número, porque só quebra depois do clique, com a pessoa mais quente da página. **As três saídas do CTA, nesta ordem, e não há uma quarta.** (1) Com o valor real do dono no perfil, o CTA é vivo e aponta pra ele. (2) Sem o valor real, o CTA CONTINUA na tela e **sai funcional com o destino em campo de 1 palavra**, `[LINK]`: mesmo texto, mesma aparência, `href="[LINK]"`, e nada mais. **A pendência não aparece na tela, nem em vermelho embaixo do botão, nem em cinza ao lado: ela vai inteira pro handoff**, com o seletor do elemento ao lado, porque frase de bastidor renderizada no lugar mais visível da conversão é a mesma pendência com outra roupa. Rode `grep -niE 'entra aqui|preencher|antes de publicar|placeholder|a definir|pendente' <peça pública>` e cole a saída, inclusive vazia, com `frases de bastidor renderizadas: 0`. (3) Nunca, em nenhum caso, a página de conversão sai SEM o bloco de próximo passo: **retirar o CTA é pior que qualquer uma das duas anteriores**, porque a peça deixa de ser de conversão, e uma calculadora que mostra à visitante quanto ela desperdiçou e não oferece passo nenhum gasta o melhor momento da página. Checagem colada: `bloco de próximo passo na tela: sim · destino real: sim/não · CTAs na tela: N · com destino real do dono: N · vivos apontando pra placeholder: 0`. `bloco de próximo passo: não` reprova a entrega, e qualquer número diferente de zero no último campo reprova também.

**Toda constante numérica da fórmula precisa de origem apontada.** Liste cada constante que entra no cálculo com a linha do insumo que a produziu (dado do dono, insumo dele, ou busca deste turno com o comando colado). **Constante sem origem NÃO vai pra tela do público:** ou ela vira input que a própria pessoa preenche, ou a peça sai com o campo `[A CONFIRMAR]` visível e o cálculo desabilitado até o dono responder. **Marcar `[A CONFIRMAR]` só na spec, com o número limpo impresso na tela, reprova**, porque é a tela que a pessoa lê: um "partimos de uma base de R$ 180 por mês" que não existe em lugar nenhum do perfil do dono vira âncora inventada do cálculo inteiro. Checagem colada: `constantes na fórmula: N · com origem apontada: N · sem origem impressas na tela: 0`.

> **STOP (o único obstáculo do loop):** mostra a spec fechada e pergunta **"pode ir?"**. Só com o "pode ir" o loop roda sozinho até a Entrega. Antes disso, não escreve uma linha de código nem cria repo.

### Fase 2 · ARQUITETURA (contrato primeiro, decisões antes do código)

**O que faz:** decide a forma do sistema antes da primeira linha, e registra as decisões no documento.

**Precisa de:** a spec aprovada · o ambiente disponível (repositório, hospedagem, servidor, banco).

**Sem o insumo:** sem infraestrutura nenhuma, a arquitetura se escreve igual, e o entregável vira o documento consolidado (ver "três ambientes"). O que muda é a última linha: em vez de "criado", ela diz "a criar, quando houver repositório".

**Entrega:** a seção de arquitetura dentro do mesmo `specs/<nome>.md`, com o contrato dos dados, o que é rápido e o que é lento, a segurança de base, e o repositório criado.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

Antes da 1ª linha, decide e registra no doc:
- **Contrato primeiro**: as rotas/endpoints e o shape dos dados, antes da implementação.
- **Síncrono vs assíncrono**: o que é rápido responde na hora; o que é **lento** (gerar vídeo, processar upload, chamar IA em lote) vai pra **fila + worker**, nunca segura a request.
- **Segurança de base**: auth, **RLS por tenant** (no produto), rate-limit, logs.
- **Checklist antes de construir** (ver `references/entrega-e-infra.md`): repo criado, tokens no cofre, tema/tokens de cor definidos, dados demo desenhados.
- **Cria o repo AGORA**, antes da 1ª linha: `git init` + `gh repo create <org-do-dono>/<nome> --private`. Repo = produção.

### Fase 3 · BUILD (constrói exatamente a spec)

**O que faz:** escreve o código dos escopos, cada um conferido contra o requisito que o originou.

**Precisa de:** a spec aprovada e a arquitetura fechada · o repositório criado.

**Sem o insumo:** sem delegação no ambiente, veja o bloco "Quando não há delegação disponível": os escopos rodam em sequência, sem perda de qualidade. Sem repositório possível, registre o estado em arquivo local versionado à mão e diga isso ao dono em uma linha.

**Entrega:** o código de cada escopo registrado, e cada tela já passada pelo gate visual.

Constrói em **escopos paralelos**: se o ambiente tiver delegação, um agente por escopo; se não tiver, você percorre os mesmos escopos em sequência, com a mesma disciplina. Cada escopo é **isolado** (worktree próprio, ou uma região do código com lock, pra dois agentes não escreverem no mesmo arquivo) e **prompt autossuficiente** (o agente recebe a spec + o contrato + o gate visual, não depende de perguntar de volta). Cada agente **commita** seu escopo. Constrói **exatamente** a spec, e a Lei 1 vale aqui.

**Todo componente de UI passa pelo GATE VISUAL** (tabela abaixo) enquanto é construído, não só no fim.

### Fase 4 · REVIEW (compara com a spec, requisito por requisito, contra o REAL)

**O que faz:** confere o construído contra a spec, requisito por requisito, rodando o sistema de verdade.

**Precisa de:** a spec com os requisitos numerados · o sistema rodando, de preferência num ambiente igual ao de produção.

**Sem o insumo:** sem conseguir rodar o sistema, a revisão **não acontece**. Ler o código e concluir que "deve funcionar" é a coisa mais perigosa desta fase. Nesse caso, a entrega sai marcada `[NÃO VERIFICADO]`, com a lista do que precisaria ser conferido, e o dono decide.

**Entrega:** a tabela requisito por requisito, com passa ou não passa e a prova de cada um.

Compara o que foi construído com a spec, **requisito por requisito**, rodando **o sistema real** (não lendo o código e concluindo que "deve funcionar"). Requisito que não passou **volta pro Build**. Repete construção e revisão até **100%** dos requisitos da spec baterem. A revisão também roda o gate visual em cada tela.

#### O teto do ciclo: quando parar de tentar e chamar o dono

O ciclo entre construção e revisão não é infinito. **Três tentativas no mesmo requisito e você para.** Isso não é fracasso: é o sinal de que o problema deixou de estar no código.

| Tentativa | O que fazer |
|---|---|
| **1ª reprovação** | conserta e roda de novo. Comportamento normal do ciclo |
| **2ª reprovação no MESMO requisito** | pare de consertar e **releia o requisito na spec**. Duas falhas no mesmo ponto quase sempre significam requisito ambíguo, não código ruim. Se ele admite duas leituras, esse é o problema |
| **3ª reprovação no MESMO requisito** | **para o ciclo e chama o dono.** Não tente uma quarta |

O que dizer ao dono no recuo, e o que **não** dizer:

> O requisito 7 ("o gestor vê o relatório consolidado") reprovou três vezes. O que eu construí funciona
> nas três leituras que tentei, e nenhuma é o que você conferiu. Acho que a gente está entendendo
> "consolidado" de forma diferente.
>
> Consolidado é: (a) a soma de todas as unidades numa linha só, (b) uma linha por unidade na mesma
> tela, ou (c) as duas coisas, com a soma no topo?
>
> Os outros 12 requisitos estão passando. Só este segura a entrega.

O que **não** se faz: escolher a leitura mais provável e seguir, ou entregar dizendo que passou. As duas quebram a Lei 1.

**Sinal de que o problema é ambiente, não requisito:** três requisitos diferentes reprovando por causas parecidas (tudo que toca o banco falha, tudo que carrega imagem falha). Aí não é o ciclo, é a infraestrutura. Pare igual, e diga isso, em vez de consertar sintoma um por um.

### Fase 5 · ENTREGA (verificação adversarial de fora + pacote com prova)

**O que faz:** ataca o próprio trabalho de fora, como um usuário hostil, e fecha o pacote de prova.

**Precisa de:** o sistema no ar · uma credencial de teste · acesso ao banco.

**Sem o insumo:** sem poder acessar de fora, a entrega sai como `[NÃO VERIFICADO]`, com a lista exata do que falta provar. Nunca diga "está no ar" sem ter entrado.

**Entrega:** `PROVA-<nome>-<data>.md`, com o endereço, o repositório, as capturas e cada verificação com a saída colada. O molde completo, com saídas reais, está em `references/EXEMPLO-FIM-A-FIM.md`.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

Verificação final **adversarial, de fora**, como um usuário hostil que quer achar o furo: **login real** (com credencial de teste), **navegação com screenshots** das telas principais, **query no banco** (o dado que a UI mostra existe mesmo na tabela?), **probe no domínio** (o subdomínio responde 200, o TLS está de pé?). Sincroniza repo = produção. Fecha o **pacote com prova**: link, repo, screenshots, o que foi verificado. Ver `references/entrega-e-infra.md` pro checklist de pronto.

## POLÍTICA DE MODELOS (recomendação, o ambiente decide)

Recomendação de alocação, não regra de motor: o ambiente escolhe os modelos que tem. O trabalho que decide a forma do sistema roda no modelo mais capaz disponível; escrever código também pede o mais capaz; ler código já escrito cabe no econômico. Isso protege a qualidade onde ela é irreversível (arquitetura, merge, verificação) sem gastar o modelo caro em leitura. Se o ambiente só oferecer um modelo, tudo roda nele e a régua de qualidade continua a mesma.

- **Planejar / merge / verificar** → o modelo mais capaz disponível.
- **Construir e revisar (Build, Review)** → o modelo mais capaz disponível. Evite o econômico no build; código ruim gerado barato custa mais no review.
- **Exploração / leitura de código pré-existente** → cabe no modelo econômico disponível. É só ler o que já existe.

## OS TIPOS DE BUILD (o que a skill constrói)

O mesmo loop e o mesmo padrão servem a qualquer build. Os cinco tipos:

- **SISTEMA / APP** (o mais pesado): app multi-tenant com **RLS por tenant**, banco próprio (Supabase), **IA sempre atrás de proxy server-side com JWT** (chave nunca no client), login, LMS, onboarding, dados demo. Deploy na VPS. Detalhe em `references/frente-produto.md`.
- **WAR ROOM**: o painel com que o **dono apresenta ao cliente dele**. SPA leve trancada por login split, seções de apresentação (visão geral, diagnóstico, vídeo com capítulos, plano numerado, proposta). Deploy Cloudflare Pages. Detalhe em `references/frente-war-room.md`.
- **SITE / PÁGINA RICA**: institucional, portal público, one-pager, landing técnica (não a landing de venda, que é `soft-funil-landing`). Estático ou backend leve. Deploy Cloudflare Pages. Passa pelo gate visual inteiro.
- **FERRAMENTA / DASHBOARD**: calculadora, painel de métricas, gerador, ferramenta interna. Tela funcional + a lógica. Gate visual no que tem UI.
- **AUTOMAÇÃO / INTEGRAÇÃO**: WhatsApp/API/webhook, fluxo n8n, script, robô, cron, sincronização entre sistemas. **Sem UI** na maioria: aqui o gate NÃO é visual, é de **ROBUSTEZ** (ver o Gate de Robustez abaixo). Deploy = serviço na VPS (systemd) ou worker.

Todo build com **tela** segue o mesmo padrão visual e engenharia estrutural (`references/padrao-visual-default.md`) e passa pelo Gate Visual. Todo build **sem tela** passa pelo Gate de Robustez.

## 🎨 GATE VISUAL (preencha, imprima e só então libere a tela)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **O inventário varre o perfil do dono INTEIRO, não só os campos que esta entrega consumiu:** cada campo do perfil é uma linha, e campo com vários valores (paleta com 3 cores; oferta com preço, parcela, bônus e garantia) rende uma linha por valor. **Entrega cujo `Dados fornecidos: N` for menor que o número de campos do perfil recebido reprova sem análise de conteúdo.** Qualificar a linha ("relevantes ao objeto", "considerados para esta entrega") também reprova: o total é o total. **Onde a linha mora:** no arquivo que o dono lê. Quando a entrega é uma peça de copy publicável (headline, carrossel, slide, card, chat, roteiro, deck), a peça NÃO recebe a tabela: a tabela vai num arquivo irmão de handoff (`HANDOFF-<slug>.md`) e só a linha de fechamento fica na peça, no rodapé. Inventário só no relato de processo, sem a linha na entrega nem o handoff no disco, reprova.

**O piso do inventário é contável e a conta vai colada.** Rode `grep -c '^- ' <perfil>` e cole a saída do comando: esse número é o PISO BRUTO. Depois desdobre toda linha que carrega mais de um valor (a oferta com preço, parcela, 3 bônus e garantia conta 6, não 1) e cole `piso bruto: N · desdobrados: M · Dados fornecidos: N+M`. **`Dados fornecidos` menor que o piso bruto reprova a entrega**, porque significa que a peça descartou campo sem registrar o motivo. Não qualifique a linha com recorte de escopo: o total é o total, e o filtro de relevância mora na coluna de destino de cada dado, nunca no total.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


Toda tela/componente passa por aqui, no Build e no Review. Qualquer ✗ reprova a tela inteira: corrige e repreenche. As três primeiras linhas exigem o **resultado do grep colado como número**, não um "ok" qualitativo, igual ao anti-IA da copy, prova por CTRL+F.

| Check | Passa se (✓) | Prova / ✓✗ |
|---|---|---|
| **Zero gradiente decorativo** | `grep -rniE "linear-gradient|radial-gradient|conic-gradient" <dir>` = **0** (a riqueza vem de 2 tons SÓLIDOS em blocos, não de degradê). Exceção única: glow do CTA e backdrop-blur de nav, contados à parte | `gradiente: N` |
| **Zero emoji na UI** | Nenhum emoji renderizado na interface; todo ícone é **SVG de linha**. Rode o grep de emoji (bloco abaixo) = **0** | `emoji: N` |
| **Zero travessão** | `grep -rnP "\x{2014}" <dir de UI e docs>` = **0**, o padrão escapado casa o travessão longo U+2014 sem escrever o caractere aqui (usa vírgula, parênteses ou `·`). Vale pra UI E docs novos | `travessão: N` |
| **Zero marcador na tela** | `grep -c 'A CONFIRMAR' <arquivo entregue>` = **0** em todo texto que é renderizado. Pendência vai pra spec e pro handoff, e o elemento que depende dela **sai desabilitado com rótulo neutro**, nunca com o marcador impresso pro público ler | `A CONFIRMAR: N` |
| **Número não quebra no meio** | Valor monetário e KPI numérico usam `white-space: nowrap` e reduzem por `clamp`, nunca quebram em duas linhas. `overflow-wrap: anywhere` num container de KPI reprova, porque parte "R$ 29.940" em "R$ 29.94 / 0". Confira **no render em 375px** e cole o que apareceu na tela, o número inteiro como ele saiu | `KPI em 375px: <o que apareceu>` |
| **Zero estouro lateral em 375px** | **Medição, não grep.** Abra a tela num navegador com viewport de largura 375 e leia `document.documentElement.scrollWidth`. Passa só com `scrollWidth <= 375`, ou seja `scrollWidth - clientWidth` = **0**. Qualquer número maior que 0 reprova a tela: liste os elementos que estouram (percorra os nós e compare `getBoundingClientRect().right` com 375) e conserte antes de reentregar. Sem navegador no ambiente, tire um screenshot em 375 de largura e meça a largura do conteúdo na imagem; conteúdo mais largo que o quadro reprova igual. Declarar "responsivo" sem o número medido não passa: grep não vê geometria, e foi exatamente por isso que peça com 44px de estouro passou no gate | `estouro 375px: scrollWidth=<N> clientWidth=<N> delta=<N>` |
| **Componentes ricos** | Nenhuma "caixinha título+descrição". Usa os componentes ricos (hero 2 colunas, KPI número gigante + label mono, escada de valor, acordeão numerado, vídeo com capítulos, mockup device, vitrine, timeline, card kicker+título+chips, modal pra conteúdo longo, lightbox). Ver `padrao-visual-default.md` | ✓/✗ |
| **Tokens de cor + 2 temas** | Toda cor é `var(--token)`; 2 temas (claro/escuro) aplicados **antes do paint, sem flash** (o tema é setado no `<head>`, não depois de renderizar) | ✓/✗ |
| **Login split** | Entrada por login split de 2 colunas (narrativa da marca + card do form ~392px); o resto atrás do gate | ✓/✗ |
| **Nav numerada + menus de dados** | Nav numerada, grupos colapsáveis **persistidos**, menus renderizados de **array de dados** (não hard-coded item a item) | ✓/✗ |
| **i18n motor próprio, condicionado ao público** | **i18n próprio só entra quando o dono declara mais de um idioma de público.** Público de um idioma só: o item **não se aplica**, e o relatório escreve `i18n: não se aplica, público declarado em 1 idioma`. Marcar "passa" num sistema de um idioma só infla o gate, e ignorar o item sem declarar a omissão também reprova. Quando se aplica: pt/en/es com chaves **namespaced**, motor próprio (sem string solta no meio do JSX) | ✓/✗ ou `não se aplica` |
| **Identidade vem do PERFIL, não do site** | **Antes de escolher paleta e tipografia, grepe o perfil do dono por identidade visual** (fundo, texto, acento, fonte, logo). O default da skill só entra quando o grep no perfil volta vazio: site sem paleta declarada NÃO autoriza o default se o perfil declara. Tema escuro num dono que declarou fundo off-white reprova a peça. Cole no relatório a linha do perfil que produziu cada valor, ou a saída vazia do grep | `identidade: <linha do perfil> ou <grep vazio>` |
| **Marca do cliente aplicada** | A paleta/tipo é a do CLIENTE (leu a marca dele); na ausência, o **default é o padrão visual da skill** (preto, Bebas/Inter/JetBrains Mono, acento `[COR-DE-ACAO do dono via config]`, hairlines, cantos retos) | ✓/✗ |
| **Bloco de próximo passo em peça de conversão** | **Peça com objetivo de conversão nunca sai sem o bloco de próximo passo**, e as três saídas da Fase 1 valem na ordem: com o destino real, CTA vivo; sem ele, CTA funcional na tela com `href="[LINK]"` e a pendência inteira no handoff, nunca na tela nem em vermelho embaixo do botão; retirar o CTA da página, nunca. Um link vivo apontando pra número de exemplo reprova igual, porque só quebra depois do clique, com a pessoa mais quente da página. Colada: `bloco de próximo passo na tela: sim · destino real: sim/não · vivos apontando pra placeholder: 0 · frases de bastidor renderizadas: 0` | ✓/✗ |
| **Copy da tela, com a régua de títulos** | H1, kicker, títulos de seção e rótulo de resultado passaram pela régua de títulos (`references/regua-de-titulos.md`), listados com gatilho e veredito num arquivo de nome fixo, `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, que fecha com `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N` (os dois primeiros iguais, qualquer diferença reprova). Kicker genérico do nicho e rótulo de seção que serviria em qualquer produto ("faça a sua conta", "o tamanho da pausa") reprovam: a tela usa o verbatim e o vocabulário do dono, não o do gênero. **O H1 de página que o público abre é sempre `abertura`, nunca `serviço`, e entra na régua mesmo quando repete o nome que o dono pediu:** nesse caso o nome vira rótulo interno e a régua produz a headline da tela, com as duas coladas lado a lado. `passados pela régua: 0` numa peça com público reprova a checagem | ✓/✗ |
| **Ressalva do nicho na tela** | tela que produz número sobre saúde, corpo, dinheiro ou resultado sai com a ressalva que o nicho pede visível ao lado do resultado (o que o número É e o que ele NÃO é), nunca só na spec | ✓/✗ |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ = REFAZ a tela. Só tudo-✓ = LIBERA | |

**Grep de prova (rode e cole o número):**
```bash
# gradiente decorativo
grep -rniE "linear-gradient|radial-gradient|conic-gradient" <dir> | wc -l
# travessão longo (U+2014) em UI/docs; o padrão vai escapado de propósito,
# pra este arquivo de regra não conter o caractere que ele proíbe
grep -rnP "\x{2014}" <dir> | wc -l
# emoji na UI (faixas comuns de emoji)
grep -rnP "[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}\x{2190}-\x{21FF}\x{2B00}-\x{2BFF}]" <dir> | wc -l
# marcador de pendência em texto que o público final lê
grep -c 'A CONFIRMAR' <arquivo entregue>
# quebra de número: procure overflow-wrap/word-break em container de KPI ou valor
grep -rnE "overflow-wrap: *anywhere|word-break: *break-all" <dir> | wc -l
```

**Medição de estouro em 375px (a única que o grep não faz).** No console do navegador com a janela em 375 de largura, ou no runner headless do ambiente:

```javascript
// cole os 3 números no relatório: passa só com delta = 0
const d = document.documentElement;
console.log('scrollWidth=', d.scrollWidth, 'clientWidth=', d.clientWidth, 'delta=', d.scrollWidth - d.clientWidth);
// quem estoura (só rode se delta > 0)
[...document.querySelectorAll('*')]
  .filter(e => e.getBoundingClientRect().right > 375)
  .forEach(e => console.log(e.className, Math.round(e.getBoundingClientRect().right)));
```

Por que inegociável: o dono vai **apresentar isso na frente do cliente dele**. Gradiente, emoji e travessão são a assinatura de "saiu de IA barata"; caixinha de título+descrição é a de "template genérico". A tela tem que parecer construída por alguém que se importa. Detalhe de cada componente e do CSS/HTML em `references/padrao-visual-default.md`.

## 🔧 GATE DE ROBUSTEZ (pro que NÃO tem tela: automação, integração, script, robô)

Build sem UI não passa no Gate Visual, passa aqui. Todo ✗ reprova: corrige e re-roda.

| Check | Passa se (✓) |
|---|---|
| **Idempotente** | rodar 2x não duplica nem corrompe (mesma entrada → mesmo estado final); usa chave de deduplicação onde precisa |
| **Erro tratado + retry** | toda chamada externa (API, banco, webhook) tem timeout, trata a falha e re-tenta com backoff; nunca engole erro em silêncio |
| **Log observável** | loga início, fim e erro de cada execução (o dono vê por que falhou sem abrir o código) |
| **Sem segredo no código** | credencial em `.env`/cofre, nunca hard-coded; caçado antes do push |
| **Provado nos 2 caminhos** | testado no caminho feliz E em 1 de falha (a API caiu, o dado veio torto). Lei 2 vale igual: sem prova é `[NÃO VERIFICADO]` |
| **VEREDITO** | o pior item acima. Um ✗ = corrige e re-roda |

---

## Exemplo curto (do pedido até as seções)

**Pedido (falado):** "Fechei uma consultoria com uma rede de 3 clínicas veterinárias. Preciso levar na reunião de segunda um painel que mostre o diagnóstico que fiz e a proposta. E depois quero entregar pra eles um portalzinho onde a equipe acompanha os protocolos."

**Pergunta Zero:** do zero. → Fase 1.

**Fase 1 (Spec, uma pergunta por vez, resumida):**
- Objetivo: um WAR ROOM pra reunião de segunda + um PRODUTO (portal de protocolos) pra entregar depois.
- Requisitos WAR ROOM: visão geral da rede (3 unidades, KPI de faturamento/unidade), diagnóstico (3 gargalos achados, cada um com o dado que prova), vídeo de 8 min gravado com capítulos por gargalo, plano de ação em 4 fases numeradas, proposta (3 níveis de investimento).
- Requisitos PRODUTO: multi-tenant (cada clínica é um tenant, RLS separando os dados), login por equipe, LMS com os protocolos em módulos, onboarding guiado no 1º acesso, dados demo de uma clínica-exemplo.
- Restrições: a marca da rede é azul-petróleo e branco (não o preto do default); prazo do war room = segunda.
- Definição-de-pronto: (war room) o dono loga, apresenta as 5 seções e mostra a proposta; (produto) uma clínica loga, vê só os dados dela, e a equipe abre um protocolo no LMS.

→ **STOP: "pode ir?"** → "pode ir".

**Fase 2 (Arquitetura):** repo `<org-do-dono>/vet-rede-painel` criado. War room = SPA + Express/sessão no Cloudflare Pages. Produto = Node na VPS (Caddy → `127.0.0.1:8412`, systemd), Supabase com RLS por `tenant_id`, subdomínio `vetrede.seudominio.com.br`. Vídeo (lento) → o upload/transcode vai pra fila + worker. Tokens de cor da marca azul-petróleo definidos; tema claro/escuro.

**Fase 3 (Build, paralelo):** um agente no war room (as 5 seções como componentes ricos: hero 2 colunas, KPIs número-gigante, acordeão numerado do plano, player com capítulos, escada de 3 níveis na proposta), outro no schema + RLS do produto, outro no LMS + onboarding. Cada tela passa pelo gate visual (grep de gradiente/emoji/travessão = 0).

**Fase 4 (Review):** roda os dois sistemas, confere requisito por requisito. Faltou o KPI por unidade no war room → volta pro build → refaz → 100%.

**Fase 5 (Entrega):** login real nos dois; screenshots das 5 seções e do LMS; query confirmando que a clínica A não enxerga o dado da clínica B (RLS de pé); probe no subdomínio (200 + TLS). Pacote: link do war room, link do produto, repo, screenshots. Entregue.

---

## O que esta skill NÃO faz (manda pro caminho certo)

- Pediu **copy / headline / carrossel / reel / stories / conteúdo** → `soft-conteudo-*` (esta skill constrói o sistema, não escreve a copy dele).
- Pediu **carta / VSL / landing de venda / isca / funil** → `soft-funil-*`.
- Pediu **webinar** (roteiro, páginas, oferta, chat) → `soft-webinar`.
- Pediu **script de venda / objeção / fechamento** → `soft-vendas-*`.
- Pediu **arte / PNG / carrossel visual / banner solto** (imagem, não sistema) → `soft-designer`.
- Pediu **edição de vídeo / corte / legenda** solta → `soft-editor-video`.
- Pediu **posicionamento / plano de marca / mecanismo** → `soft-plano-posicionamento`.
- Pediu **proposta comercial** em documento (não como seção de um painel) → `soft-vendas-proposta`.
- Pediu **faxina de disco, liberar espaço no servidor** → `soft-organizacao-vps`.

Em toda rota acima: se a skill não estiver instalada, faço aqui em modo reduzido.

A régua: se o entregável é **código que roda** (sistema, site, ferramenta, automação, integração, script, robô), é aqui. Se é **peça de comunicação** (texto, arte, vídeo), é das `soft-*` acima.

## Anti-Patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Fez "caixinha título+descrição" em vez de componente rico | Reprova no gate visual: troca por hero 2 colunas / KPI número-gigante / acordeão numerado / vídeo com capítulos (ver `padrao-visual-default.md`) |
| Usou gradiente decorativo | Grep > 0 = ✗ automático. Riqueza vem de 2 tons sólidos em blocos, não de degradê |
| Estourou lateral em 375px | `scrollWidth - clientWidth` > 0 = ✗ automático. Gate de grep não vê geometria: a medição é obrigatória e o número vai colado |
| Emoji na UI ou travessão na UI/doc | Grep > 0 = ✗ automático. Ícone = SVG de linha; travessão vira vírgula/parênteses/`·` |
| Fez deploy sem repo | Cria o repo na Fase 2, ANTES da 1ª linha. Repo = produção; sem repo não há ponto de retorno |
| Editou sistema existente sem estudar antes | Pergunta Zero: localiza o código real, estuda inteiro em paralelo, commita o estado atual ANTES de mexer, e só então entrevista com perguntas informadas |
| Começou a codar antes do "pode ir" | O STOP do fim da Spec é o único obstáculo. Sem "pode ir", não escreve código nem cria repo |
| Inventou feature fora da spec, ou cortou requisito | Lei 1: constrói exatamente a spec. Falta virou `[A CONFIRMAR]`, não invenção nem corte |
| Disse "está no ar" sem provar | Lei 2: login real + screenshot + query/probe. Sem prova é `[NÃO VERIFICADO]` |
| Review leu o código e concluiu que "deve funcionar" | Review roda o sistema REAL e compara requisito por requisito. Ler ≠ verificar |
| Chave de IA no client | IA sempre atrás de proxy server-side com JWT. Chave nunca vai pro browser (ver `frente-produto.md`) |
| Colocou tudo síncrono e a request parou no vídeo/IA | O lento vai pra fila + worker; o síncrono responde na hora (ver `frente-produto.md`) |
| Construiu no modelo econômico pra economizar | Build e Review pedem o modelo mais capaz disponível. Leitura de código pré-existente cabe no econômico; escrever código, não |
| Pediu permissão a cada passo do loop | Após "pode ir", itera sozinho. Só para pra mudar escopo ou pra ação destrutiva |
| Segredo em texto puro commitado | Cofre do dono (`.env` cifrado na VPS); caça segredo antes de cada push (ver `entrega-e-infra.md`) |

## References (profundidade; o fluxo acima é autossuficiente)

- `references/regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.
- `references/padrao-visual-default.md`: o design system (paleta, 3 fontes, forma) + a engenharia estrutural (componentes ricos, tokens, 2 temas sem flash, login split, nav numerada, i18n) com exemplos de CSS/HTML. Leia antes de construir qualquer tela.
- `references/frente-war-room.md`: anatomia dos menus do war room, vídeo com capítulos, infográficos, backend Express + sessão. Leia na Fase 1/3 do war room.
- `references/frente-produto.md`: multi-tenant com RLS, IA atrás de proxy com JWT, LMS, onboarding, dados demo, segurança. Leia na Fase 1/3 do produto.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta, com o pacote de prova real, uma revisão que reprovou 3 vezes, e o mesmo pedido resolvido sem infraestrutura nenhuma.
- `references/entrega-e-infra.md`: GitHub sempre, Cloudflare Pages (war room) / VPS Caddy + systemd (produto), subdomínio, cofre de credenciais, checklist de pronto. Leia nas Fases 2 e 5.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **O lint é gate com código de saída, não relatório.** Rode `python3 scripts/lint_copy.py <todos os .md da entrega>; echo "exit=$?"` e cole a linha `exit=` no relatório. **`exit` diferente de 0 proíbe a entrega:** volte pro passo de escrita, conserte e rode de novo, até sair 0. Declarar que rodou o lint sem colar o veredito não conta como gate cumprido. E a frase de fecho entra na varredura junto com o resto: o CTA é o texto que mais se repete no pacote, então um molde banido ali se multiplica por todos os arquivos e pelos dados que alimentam qualquer gerador. Cole `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## O dono nunca recebe comando (regra dura desta skill)

Quando a publicação ou a instalação não sair, a PRIMEIRA linha do relato diz o que aconteceu e o que pedir, em português, sem nome de comando: "não consegui publicar porque a conta do Drive não está conectada; me manda o acesso que eu publico" vale, e "rode `gog drive upload`" não vale. O dono opera pelo aplicativo de mensagem e não abre terminal.

Nesse caso a entrega sai com duas coisas, sempre as duas:
1. **O arquivo pronto**, no formato final, do jeito que ele seria publicado.
2. **`PEDIDO-PARA-QUEM-PUBLICA.md`**, o passo a passo escrito pra TERCEIRO (quem cuida do site, do Drive ou do servidor): o que abrir, onde colar, o que conferir depois, e a quem devolver o link. Escrito pra pessoa, não pro terminal: o comando, quando existir, mora dentro de bloco de código nesse arquivo, com uma linha em português dizendo o que ele faz.

O relato fecha com a seção `Perguntas pra você`, e a pergunta do acesso entra ali escrita como pergunta.

---

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**

## A frase que a dona repetiria (fecho, uma por entrega)

Escolha a UMA frase da entrega que a dona repetiria de cor numa conversa, cole ela sozinha e responda por escrito por que ela sobrevive fora do contexto: sem a peça em volta, sem o nome do produto, sem a explicação que vem antes. Cole `frase que sobrevive fora do contexto: <literal>`. Correta e morna é o defeito comum aqui: a abertura que serve pra qualquer serviço do mesmo tipo não é a frase, é o preenchimento. Nenhuma frase significa que a peça está correta e não está viva, e a entrega volta pro passo de escrita.

## A saída do script entra uma vez (fecho, vale em toda entrega)

**A saída do script entra uma vez e não se reescreve em prosa.** Recorte mais amplo que o do script sai com **rótulo diferente** e com o comando que o produziu ao lado, nunca com a mesma frase que o script usa. Duas listas com o mesmo rótulo e conteúdo diferente reprovam a entrega. Confira por comando antes de fechar: `python3 scripts/checar_titulos.py --conferir <pasta de saída>; echo exit=$?`, que reprova com `saída do script reescrita` quando o mesmo rótulo aparece com duas listas, e com `inventário duplicado` quando a entrega traz dois números de inventário diferentes. **`exit` diferente de 0 proíbe a entrega.**
