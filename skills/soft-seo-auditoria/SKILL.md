---
name: soft-seo-auditoria
description: >-
  Audita o SEO de um site e devolve o plano de correção priorizado: palavras que valem a pena, erros de cada página com gravidade e conserto, buracos de conteúdo, checagem técnica e comparação com concorrente. Use quando o pedido for: "audita o SEO do meu site", "por que meu site não aparece no Google", "pesquisa de palavra-chave", "que palavra eu devo atacar", "meu concorrente aparece e eu não", "checagem técnica do site", "meu site está lento pro Google", "o que escrever pra ranquear", "plano de SEO". NÃO use pra: escrever o texto da página depois de escolher a palavra (soft-funil-landing); calendário e pauta de rede social (soft-conteudo-planner); anúncio pago (soft-trafego-meta); auditoria de perfil do Instagram (soft-consultoria-instagram); construir ou hospedar o site (soft-sistema); leitura geral do número do negócio (soft-negocio-metricas). Leia e siga o fluxo inteiro do SKILL.md.
---

# A auditoria de SEO que vira lista de tarefas

Esta skill olha um site como o buscador olha, e devolve o que consertar em ordem de impacto. Ela entrega quatro coisas: as palavras que valem a pena atacar, os erros de página com gravidade e conserto escrito, o que falta de conteúdo comparado a quem já ranqueia, e a checagem técnica. O resultado é sempre um arquivo nomeado, fechado por um plano dividido em conserto rápido e obra de trimestre.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**A lei-mãe:** auditoria sem plano é diagnóstico sem receita. Todo item apontado sai com o conserto escrito, a gravidade e o esforço estimado, e nada entra no relatório sem que o dono consiga agir sozinho a partir dele.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as 5 ações num caso fictício de nicho neutro: o resumo executivo, a tabela de palavras, a tabela de erros por página, a comparação com dois concorrentes, a checagem técnica e o plano em duas colunas. Ler antes da primeira pergunta economiza uma rodada de retrabalho.

**Sobre dados:** volume de busca, dificuldade e posição vêm de ferramenta de SEO quando o ambiente tiver uma conectada; se não tiver, busque na web quando o ambiente permitir; se nem isso, peça ao dono os números que ele já tem (o painel do buscador para donos de site é grátis e responde quase tudo). **Nenhum número entra no relatório sem a fonte escrita ao lado.** Estimativa sem fonte vira `[A CONFIRMAR: origem do dado]` e continua.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Como aqui o trabalho é auditar e priorizar, valem duas delas:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o site, o concorrente e o público e eu audito). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pra auditoria com o que o dono colou. Se faltar um insumo que a auditoria não vive sem (a URL do site, a página alvo), pergunta AQUELE insumo e segue, sem repetir a entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Pergunta o site, a página que o dono quer ranquear, o público e o concorrente, uma coisa de cada vez, e roda a auditoria com o que ele for dando.

A pergunta do modo é UMA por auditoria.

**Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer que eu aprofunde uma página? compare com outro concorrente? detalhe o plano do trimestre? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "audita o SEO do meu site", "por que meu site não aparece", "plano de SEO", "faz a auditoria completa" | **as 5 na ordem, com parada em cada** |
| "pesquisa de palavra-chave", "que palavra eu ataco", "que termo vale a pena" | **1 · PALAVRAS** |
| "olha essa página", "revisa os títulos", "meu texto está otimizado?" | **2 · PÁGINA POR PÁGINA** |
| "o que eu deveria escrever", "meu concorrente tem conteúdo que eu não tenho", "onde estão os buracos" | **3 · BURACOS DE CONTEÚDO** |
| "checagem técnica", "meu site está lento", "o Google não indexa", "problema de estrutura" | **4 · TÉCNICA** |
| "compara com o concorrente", "por que ele aparece e eu não", "análise de concorrente no Google" | **5 · CONCORRENTE** |

Pedido ambíguo ("dá uma olhada no meu site", "meu site não traz cliente"): pergunte UMA coisa só, **"que página você quer que apareça, e pra quem procurando o quê?"**, mostre a tabela acima como cardápio e siga pela resposta. Sem essa resposta, a auditoria vira lista genérica de boas práticas.

## Como ler cada ação

Toda ação abaixo traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de oferta, avatar, região de atendimento ou linguagem do público: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" da ação e siga com o que faltar marcado `[A CONFIRMAR: o quê]`.

**Duas regras que valem em toda ação:** toda recomendação sai com gravidade (crítico, alto, médio, baixo) e esforço (rápido, meio dia, obra) · e nenhum item entra sem o conserto escrito de forma que o dono consiga executar sem perguntar de volta.

---

## Ação 1 · PALAVRAS (o que as pessoas digitam de verdade)

**O que faz:** levanta e classifica as palavras que valem a pena atacar, com intenção, dificuldade e o tipo de página que cada uma pede.

**Precisa de:** o **domínio ou a página** a auditar · o que o dono **vende**, em uma frase, e pra quem · a **região** de atendimento, quando o negócio for local · as palavras que ele **já ataca hoje**, se souber · os **concorrentes** que ele conhece.

**Sem o insumo:** entrevista curta de 4 perguntas: o endereço do site · o que você vende e pra quem · você atende uma região específica ou o país inteiro · quais três concorrentes aparecem quando você procura o que vende. Sem concorrente citado, busque na web quando o ambiente permitir e proponha dois ou três; se não houver acesso, peça ao dono numa pergunta só. Sem dado de volume, classifique demanda em alta, média e baixa pelo julgamento declarado e marque `[A CONFIRMAR: volume]`.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `seo-palavras.md`, com a **tabela de oportunidades** de 15 a 25 linhas, ordenada por oportunidade, mais a lista de perguntas do público. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/palavras-e-intencao.md` (as 4 intenções, os tipos de termo e como pontuar oportunidade).

**Profundidade:** `references/gate-do-relatorio.md`.

**Os passos:**
1. Levante os termos em quatro caixas: **principais** (alta intenção, colados no que o dono vende) · **secundários** (variação e apoio) · **cauda longa** (frases específicas, pouca disputa, intenção clara) · **perguntas** (o que a pessoa digita como pergunta, que é onde o buscador mostra resposta destacada).
2. Classifique a **intenção** de cada uma: informacional (quer aprender), navegacional (procura uma marca), comercial (compara antes de comprar), transacional (quer comprar agora). Página com intenção errada nunca ranqueia, por melhor que seja o texto.
3. Estime **demanda** e **dificuldade** com a fonte escrita ao lado de cada número.
4. Calcule a **oportunidade** (alta, média, baixa) cruzando demanda, dificuldade e relevância pro que o dono vende. Termo de alta demanda que não vende nada é oportunidade baixa.
5. Diga qual **tipo de página** cada termo pede: artigo, página de serviço, comparação, glossário, ferramenta, guia.
6. Monte a tabela: termo · dificuldade · oportunidade · posição atual · intenção · tipo de página recomendado. **STOP.**

---

## Ação 2 · PÁGINA POR PÁGINA (o que está errado no que já existe)

**O que faz:** revisa as páginas que importam, item por item, e devolve cada erro com gravidade e conserto.

**Precisa de:** a lista das **páginas principais** (a inicial, as de serviço ou produto, os textos mais visitados), do dono ou da navegação do site · o **conteúdo** de cada uma: peça o texto ao dono quando o ambiente não tiver acesso à web · a **palavra alvo** de cada página, da Ação 1.

**Sem o insumo:** se o dono não sabe quais páginas importam, use as três que sempre importam: a inicial, a página do que ele mais vende, e o texto mais recente. Se não houver acesso ao conteúdo, peça numa pergunta só que ele cole o texto de uma página por vez, e audite o que chegar, marcando as demais como `[A CONFIRMAR: conteúdo não auditado]`.

**Entrega:** `seo-paginas.md`, com a **tabela de erros** (página · erro · gravidade · conserto) e, quando o dono pedir, o título e a descrição reescritos de cada página. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/checklist-pagina.md` (os 8 itens, com o critério de cada um e o exemplo ruim e bom).

**Profundidade:** `references/palavras-e-intencao.md` · `references/gate-do-relatorio.md`.

**Os 8 itens de cada página** (o detalhe de cada um está no checklist):
título da aba · descrição do resultado de busca · título principal na página · hierarquia dos subtítulos · uso da palavra alvo (aparece cedo, aparece natural, não aparece demais) · ligação interna entre páginas · texto alternativo das imagens · desenho do endereço da página.

**As gravidades:** **crítico** (impede a página de ser encontrada ou indexada) · **alto** (derruba a posição de forma clara) · **médio** (boa prática ignorada, impacto moderado) · **baixo** (ajuste fino).

---

## Ação 3 · BURACOS DE CONTEÚDO (o que falta escrever)

**O que faz:** compara o que o site cobre com o que o mercado procura, e devolve a lista do que escrever, em ordem.

**Precisa de:** o **inventário** do que já existe no site (títulos e temas), do dono ou da navegação · a tabela de palavras da Ação 1 · o que os **concorrentes** cobrem, da Ação 5 quando ela já rodou.

**Sem o insumo:** sem inventário, peça ao dono a lista dos títulos que ele já publicou, numa pergunta só. Sem dado de concorrente, use as perguntas do público levantadas na Ação 1 como fonte de buraco: pergunta muito digitada e sem resposta no site é buraco por definição.

**Entrega:** `seo-conteudo.md`, uma linha por buraco: tema · por que importa · formato recomendado · prioridade · esforço. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/buracos-de-conteudo.md` (os 6 tipos de buraco e como priorizar).

**Profundidade:** `references/palavras-e-intencao.md` · `references/gate-do-relatorio.md`.

**Os 6 tipos de buraco:** tema que o concorrente cobre e o site não · página velha que não é atualizada há mais de um ano · página rasa demais pra responder a busca · formato que falta (guia, comparação, glossário, calculadora, modelo) · etapa de decisão sem conteúdo (quem está descobrindo, quem está comparando, quem vai comprar) · grupo de temas sem página central que amarre os textos soltos.

---

## Ação 4 · TÉCNICA (o que impede o site de ser lido)

**O que faz:** roda a checagem de infraestrutura que decide se o conteúdo chega a ser lido, e devolve cada item com situação e conserto.

**Precisa de:** acesso ao site (busque na web quando o ambiente permitir) ou os **prints e dados do painel do buscador para donos de site**, pedidos ao dono · a plataforma em que o site roda, porque o conserto muda por plataforma.

**Sem o insumo:** sem acesso nenhum, entregue a checagem como **lista de verificação pro dono rodar**, item por item, com onde olhar em cada caso, e marque tudo `[A CONFIRMAR: não verificado]`. Uma lista honesta que o dono consegue rodar vale mais que um diagnóstico inventado.

**Entrega:** `seo-tecnico.md`, tabela de checagem (item · situação · detalhe · conserto), situação em passou, atenção ou falhou. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/checagem-tecnica.md` (os 9 blocos, o que olhar em cada um e o conserto padrão).

**Profundidade:** `references/gate-do-relatorio.md`.

**Os 9 blocos:** velocidade de carregamento e a causa provável · comportamento no celular · dados estruturados (a marcação que faz o resultado aparecer com estrela, pergunta ou preço) · rastreamento (o arquivo que orienta o robô, o mapa do site, o endereço canônico, as marcas de não indexar) · links quebrados e correntes de redirecionamento · conexão segura e conteúdo misto · os três sinais de experiência de carregamento · indexação e conteúdo duplicado · **declarações do cabeçalho** (`meta charset`, `viewport`, `lang`, `title`, `meta description`).

**O cabeçalho é linha obrigatória na tabela, mesmo lendo só o arquivo.** `meta charset` ausente é falha de gravidade alta, é a mais barata de checar (basta procurar no HTML) e é a que mais escapa, porque ninguém procura o que não está numa lista. A tabela de entrega traz uma linha para cada uma das cinco declarações, com situação preenchida ou `[A CONFIRMAR: não verificado]`. Tabela sem essas cinco linhas reprova a auditoria.

---

## Ação 5 · CONCORRENTE (por que ele aparece e o dono não)

**O que faz:** compara o site do dono com dois ou três concorrentes, dimensão por dimensão, e nomeia o que explica a diferença.

**Precisa de:** os **concorrentes**, do dono ou identificados por busca na web quando o ambiente permitir · o que cada um cobre de tema e com que profundidade · a tabela de palavras da Ação 1.

**Sem o insumo:** se o dono não sabe quem são, pergunte o que ele digitaria pra achar o próprio serviço e use os três primeiros resultados que não sejam anúncio. Sem acesso à web, peça ao dono que cole o endereço de dois concorrentes e os títulos das páginas principais deles.

**Gate de proveniência da tabela de concorrente.** Nome de marca, de pessoa ou domínio de concorrente só entra na tabela com a chamada de busca que o produziu citada na mesma linha. Sem ferramenta de busca no ambiente e sem o endereço colado pelo dono, a tabela sai como categoria sem nome (`Concorrente A [A CONFIRMAR: exige busca]`) e as dimensões que dependem de abrir a página ficam vazias com o mesmo marcador. Nunca descreva conteúdo de página que você não abriu, e nunca date uma busca que não rodou. Inventar concorrente reprova a entrega inteira, não só a linha.

**Entrega:** `seo-concorrente.md`, a tabela comparativa mais as três conclusões que explicam a diferença. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/comparacao-concorrente.md` (as 7 dimensões e como ler cada uma).

**Profundidade:** `references/buracos-de-conteudo.md` · `references/gate-do-relatorio.md`.

**As 7 dimensões:** termos em comum e quem aparece melhor em cada · termos que só o concorrente tem · sinais de força do domínio · profundidade de conteúdo (tamanho médio, cobertura, frequência de publicação) · perfil de quem aponta link pra ele · quem ocupa os espaços destacados do resultado de busca · vantagem técnica.

---

## O gate do relatório (roda por dentro, em toda ação, e não imprime)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Fontes consultadas (esta skill pesquisa, então a seção é obrigatória).** A seção "Fontes consultadas" da entrega lista só o que foi de fato aberto neste turno, e cada linha traz o comando ou a chamada de ferramenta que abriu aquela fonte. Sem acesso à web no ambiente, a seção diz exatamente "sem acesso à web neste ambiente" e nada mais: nenhum domínio, nenhum nome de marca, nenhuma data de busca. Checagem verificável antes de fechar: conte as linhas da seção e conte os comandos registrados no relatório e escreva os dois números lado a lado, nesta forma: `fontes declaradas: N · comandos no log: N`. **Declarar 4 buscas com 1 comando no log reprova**, e o conserto é apagar as 3 linhas sem comando, nunca inventar o comando. **Cada linha de tabela sobre terceiro traz a consulta que a produziu e o trecho citado da página aberta.** Número (preço, prazo, prazo de entrega, volume, quantidade de alunos, faturamento) vindo de página de terceiro só entra com o trecho colado ao lado; sem trecho colado, o campo sai como `[A CONFIRMAR: exige abrir a página]`, e cravar o número mesmo assim reprova a entrega inteira. Memória de treino e inferência plausível não são fonte.


**O que faz:** reprova o relatório que o dono não consegue executar. O veredito é o pior item, e uma reprovação refaz aquela seção, não a auditoria inteira.

**Leia primeiro:** `references/gate-do-relatorio.md`.

Os 5 checks anti-IA, inline:
1. **Travessão longo:** zero ocorrência de U+2014 e U+2013 no arquivo inteiro, notas incluídas. Ponto ou hífen comum no lugar; faixa numérica escreve "10 a 20".
2. **Verbo-freio banido:** a família que a régua anti-voz proíbe (o verbo que rima com "cravar" e todas as flexões) não aparece. Use emperrar, empacar, parar, freio, amarra.
3. **Antítese de espelho:** nada do molde que nega um polo curto pra afirmar o outro, em uma frase ou em duas, com ou sem a preposição "sobre", nem duas negações paralelas empilhadas. Afirme o que é, com sujeito e cena.
4. **Verbo de transformação genérico:** a família de verbos grandiosos de folheto (revolução, redefinição, liberação de potencial, ganho de escala). Troque por concreto: resolve, tira, muda, corta.
5. **Abertura e fecho de robô:** a saudação de praxe, o convite a imaginar, a pergunta retórica de introdução, a moldura que anuncia um segredo, o conectivo formal de dissertação, o fecho que agradece a leitura.

Mais os checks próprios do formato, binários: **fonte do número** escrita ao lado de todo dado · **gravidade e esforço** em toda recomendação · **conserto executável** (o dono sabe o que abrir e o que mudar) · **furo marcado** em `[A CONFIRMAR: o quê]` · **nada inventado**: posição, volume e velocidade que não foram medidos aparecem como não verificados, nunca como estimativa disfarçada de dado.

**Com shell disponível, rodar `python3 scripts/lint_copy.py <arquivo>` sobre a entrega é obrigatório, não opcional:** é ele que decide o item anti-IA do gate. Sem shell, faça a busca manual pelos dois bloqueios duros do check 1 e do check 2, no arquivo inteiro.

---

## O plano final (fecha toda auditoria completa)

Toda auditoria que rodou mais de uma ação fecha com `seo-plano.md`, em duas colunas:

**Conserto rápido (esta semana):** o que leva menos de 2 horas e tem efeito imediato. Título e descrição refeitos, link quebrado consertado, texto alternativo de imagem, subtítulo fora de ordem.

**Obra do trimestre:** o que precisa de projeto. Grupo de temas com página central, série de textos pra cobrir um buraco, reforma da estrutura de navegação, campanha pra ganhar links.

Cada item das duas colunas carrega: o que fazer (concreto), o efeito esperado (alto, médio, baixo), o esforço e a dependência, quando houver.

E o **resumo executivo** abre o arquivo: 3 a 5 frases com a maior força do site, as 3 prioridades de maior efeito, e o veredito em uma palavra (base sólida, precisa de trabalho, ou problema grave).

---

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Escrever o texto da página depois de escolher a palavra | **soft-funil-landing** | entrego o esqueleto de seções e o título, sem a copy de venda |
| Calendário e pauta de conteúdo de rede social | **soft-conteudo-planner** | entrego a lista de temas por prioridade, sem calendário |
| Anúncio pago, campanha, leitura de conta | **soft-trafego-meta** | não faço. Busca orgânica e mídia paga são jogos diferentes |
| Auditoria de perfil do Instagram | **soft-consultoria-instagram** | não faço |
| Construir, hospedar ou consertar o site no código | **soft-sistema** | escrevo o conserto em linguagem que o desenvolvedor executa |
| Leitura geral do número do negócio | **soft-negocio-metricas** | leio só o número de busca orgânica |
| Título e gancho isolado pra rede social | **soft-conteudo-headlines** | escrevo o título da aba e a descrição de busca, que são outra coisa |
| Posicionamento, oferta, avatar | **soft-plano-posicionamento** | uso a entrevista curta de 4 perguntas da Ação 1 |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/palavras-e-intencao.md` · `references/checklist-pagina.md` · `references/buracos-de-conteudo.md` · `references/checagem-tecnica.md` · `references/comparacao-concorrente.md` · `references/gate-do-relatorio.md` · `scripts/lint_copy.py` (o anti-IA em código, rode no shell quando o ambiente permitir).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `seo-palavras-loja-tintas.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
