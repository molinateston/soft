---
name: soft-funil-isca
description: >-
  Constrói a ISCA, o material gratuito que captura o lead certo, entrega valor de verdade e aponta pro método, em qualquer formato (checklist, template, quiz, calculadora, mini-curso, guia, artigo-isca), e ajuda a ESCOLHER qual isca fazer. Use quando o pedido for: "faz uma isca", "lead magnet", "material gratuito", "o que eu ofereço de graça", "que isca eu faço", "não sei o que oferecer de graça", "monta um checklist pra captura", "quiz que captura lead", "calculadora pra pegar contato", "PDF de captura", "artigo isca". NÃO use pra: "não sei o que postar" e a pauta do feed (soft-conteudo-planner); o evento de entrada do lançamento (soft-launch); carrossel, reel ou post de feed (soft-conteudo-*); página de captura ou entrega (soft-funil-landing); a régua DEPOIS do download (soft-funil-nutricao); carta ou VSL (soft-funil-carta); mini-webinar (soft-funil-miniwebinar); webinar (soft-webinar); arte (soft-designer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Isca, a amostra que prova a tese e captura o lead certo

A isca não é conteúdo de graça. É a proposta de valor em formato gratuito: um material que entrega um pedaço de verdade real e faz o leitor reposicionar o que ele acha que precisa. A isca certa FILTRA. Quem não é cliente desiste no meio. Quem é, se reconhece linha a linha e pede a continuação.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

Ela sai em qualquer formato. O formato muda, a lei não: toda isca entrega **o quê** e **o porquê**, e guarda **o como**. Quem dá o como de graça não tem o que vender.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as ações num caso fictício de nicho neutro: as 5 candidatas da ideação com a recomendação, o formato escolhido, a isca produzida por inteiro, a captura desenhada e o que o gate reprovou pelo caminho.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola tudo que tem sobre a tese e o público e eu monto a isca). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou. Se faltar um insumo que a isca não vive sem (a tese que ela prova, o público, o destino da captura), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez, e monta a isca com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda a isca (o formato, a promessa única, a semente do método, o destino), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a decidir sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("o pessoal quer aprender", "os clientes de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: a pergunta literal que um cliente faz sempre, um erro real que ele vê no mercado, um número do próprio resultado. Material bruto vira a âncora da isca; resposta rasa vira isca rasa. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar a isca, fecha com UMA linha: "Quer outro formato? Promessa mais afiada? Menos fricção na captura? Me diz o que ajustar que eu refaço só essa parte." A oferta de refino não substitui o STOP nem o gate.


## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "que isca eu faço", "não sei o que oferecer de graça", "o que ofereço", "me ajuda a escolher" | **1 · IDEAÇÃO** (opcional, só quando ele não decidiu) |
| "faz um checklist", "monta um template", "quero um quiz", "um PDF de captura", "artigo isca", já com o tema decidido | **2 · FORMATO**, depois **3 · PRODUÇÃO** |
| "como eu troco isso por contato", "quantos campos no formulário", "pra onde mando quem baixou" | **4 · CAPTURA E DESTINO** |
| "como o feed entrega a isca", "comentário vira DM", "palavra-chave no post" | **5 · PONTE DO FEED** (opcional) |
| "a isca inteira, do zero" | **1 a 4, na ordem, com parada em cada** |

Pedido ambíguo ("me ajuda com a isca"): pergunta UMA coisa só, **"você já sabe qual isca quer fazer, ou quer ajuda pra escolher?"**, mostra a tabela como cardápio e segue pela resposta.

**Duas ações são OPCIONAIS e só entram sob pedido:** a **1 · IDEAÇÃO** (pula se o dono já chegou com a isca decidida) e a **5 · PONTE DO FEED** (só quando ele pergunta como o feed entrega a isca).

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de posicionamento, avatar, mecanismo nomeado, voz ou prova: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

**As 6 leis de operação** (detalhe em `shared-references/operacao-padrao.md`, Seção 0): (1) nunca escreve como se o cliente já soubesse o contexto, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa o contexto antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**, confere número, caso e fala na fonte; (6) **doc de saída enxuto pros 2 leitores**, zero meta-narração, zero bastidor, só o insumo denso mais `[A CONFIRMAR]` onde falta.

**Marcação única de furo em toda a entrega:** `[A CONFIRMAR: o quê]`. Uma grafia só, do começo ao fim do arquivo.

---

## Ação 0 · ANCORAGEM (roda antes de qualquer ação, não pula)

**O que faz:** abre a fonte de fala real do cliente e puxa a matéria-prima de toda a isca.

**Precisa de:** a fonte de fala, nesta ordem: descrição do projeto → posicionamento do dono → mensagens anteriores. De lá saem **3 a 5 falas de DOR e 3 a 5 de DESEJO**, literais, com o N (quantas vezes cada uma apareceu).

**Sem o insumo:** sem nenhuma fala real, **não invente**. Ancore em prova real do dono (resultado, caso, mecanismo) e avise em 1 linha que minerar 5 a 8 falas reais deixa a isca bem mais cravada. Número que não veio do briefing entra como `[A CONFIRMAR: número]` e não conta como ancorado. **PARA e confirma a fonte antes de seguir.**

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** nada de arquivo. É a matéria-prima que alimenta as ações 1 e 3.

**Leia primeiro:** `references/entrada-verbatim.md` (o protocolo de ancoragem).

**Profundidade:** `shared-references/crivo/01-entrada-verbatim.md`.

Aspas na copy são substring literal da fonte. A fundação que vem do posicionamento, quando existe: tese central, mecanismo nomeado, inimigo nominal, cliente em uma frase. A isca é uma amostra desse mecanismo, nunca um tema solto.

---

## Ação 1 · IDEAÇÃO (OPCIONAL, só quando o dono não decidiu a isca)

**O que faz:** gera as candidatas de isca, pontua cada uma e recomenda uma ou duas com convicção.

**Precisa de:** as falas da Ação 0 (a isca certa resolve a dor de top 3, não a sétima) · **o que o dono vende ou vai vender**, perguntado a ele, porque o destino vem antes da isca · a **crença-ponte** que a isca precisa instalar.

**Sem o insumo:** se o dono não tem oferta definida, não há próximo dólar e a ideação não fecha. Marque `[A CONFIRMAR: oferta]`, gere as candidatas mesmo assim pela dor de top 3, e diga em 1 linha que a recomendação final depende da oferta. Sem falas reais, gere as candidatas a partir da prova e do mecanismo do dono.

**Entrega:** `ideias-de-isca.md`, as 5 a 8 candidatas em tabela (dor de top 3 atacada · ganho rápido em menos de 20 minutos · formato sugerido · destino pra onde leva · nota do crivo) mais a recomendação de 1 ou 2, com o porquê. **STOP pro dono escolher.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/ideacao-isca.md` (os 4 critérios-núcleo, as 3 perguntas de retorno, os prompts de brainstorm e a lógica do próximo dólar).

**Profundidade:** `references/catalogo-iscas.md` (pra sugerir o formato de cada candidata).

**Os passos:**
1. Pergunta, na ordem de retorno (destino primeiro, isca por último): **o que você vende** → **o que o avatar precisa acreditar pra querer isso** → brainstorm do tópico a partir das falas.
2. Gera 5 a 8 candidatas. Cada uma com a dor de top 3, o ganho rápido, o formato e o destino.
3. Pontua pelo crivo: específico ganha de amplo · ataca a top 3 · traz informação nova · prova a autoridade do dono · não satura o lead.
4. **Recomenda 1 ou 2 com convicção**, postura de consultor, não menu neutro. Na ordem de recomendação, o formato interativo (quiz, template, calculadora) é o default sugerido, porque converte bem acima do material só de leitura; o guia longo entra quando o avatar pede profundidade. `[A CONFIRMAR]` as taxas exatas por nicho.
5. **STOP.**

---

## Ação 2 · FORMATO (uma isca, uma promessa, um destino)

**O que faz:** escolhe o formato da isca pela função psicológica e pelo estágio de consciência do avatar, e declara a promessa única.

**Precisa de:** a isca-alvo (da Ação 1 ou trazida pelo dono) · o **estágio de consciência do avatar**, do perfil/brain do agente · o destino pra onde a isca leva.

**Sem o insumo:** sem o estágio de consciência declarado, assuma **médio** (sabe que tem o problema, não sabe a saída), escolha pela função e diga em 1 linha qual premissa assumiu. Sem destino, pergunte só isso, numa frase, antes de escolher o formato.

**Entrega:** 1 linha declarada, no topo do que vier depois: *"formato X, promessa Y, destino Z, porque o avatar está no estágio W."* **STOP pro OK.**

**Leia primeiro:** `references/catalogo-iscas.md` (o universo de formatos por função e a matriz por estágio de consciência).

**Profundidade:** `references/conducao-na-pratica.md`, seções 1 a 4 (congruência, minimalismo, por que a posição é mais difícil que o funil; a seção 5 fica fora de escopo aqui) · `references/artigo-isca.md`, quando o formato escolhido for o artigo-isca.

**As 5 famílias por função:**
- **A · Execução e ferramenta** (checklist, cheat sheet, template, script, banco de exemplos, planner, planilha, kit): faz AGIR e vencer agora. Melhor conversão lá na frente.
- **B · Interativo e diagnóstico** (quiz, avaliação, calculadora, gerador): maior conversor absoluto e segmenta o lead no mesmo movimento. A segmentação É qualificação.
- **C · Educação e autoridade** (mini-curso por e-mail, vídeo-treino, tutorial passo a passo, guia longo só quando não cabe ganho rápido, workshop de 1h, artigo-isca).
- **D · Prova e fundo de funil** (estudo de caso, auditoria grátis, amostra, sessão, desafio, livro com frete).
- **E · Curadoria** (lista de recursos, cofre de materiais, template de organização, mapa mental, relatório do setor).

**Heurística rápida:** converter e segmentar no topo → quiz ou avaliação · agir já → checklist, template, script · ticket alto ou serviço → auditoria, sessão, estudo de caso · pré-venda de produto → mini-curso, desafio, workshop · decisor de empresa → relatório, calculadora, template.

**Regra dura:** uma isca, uma promessa específica, um destino. A promessa nomeia o pedaço que ela resolve, nunca "tudo sobre X".

---

## Ação 3 · PRODUÇÃO (a isca ancorada, com a semente do método)

**O que faz:** escreve a isca no formato escolhido, a partir do verbatim da Ação 0.

**Precisa de:** as falas da Ação 0 · o formato e a promessa da Ação 2 · o **mecanismo nomeado** do dono, do perfil/brain do agente · a **prova real**.

**Sem o insumo:** sem mecanismo nomeado, escreva a isca ensinando o quê e o porquê, e marque `[A CONFIRMAR: nome do mecanismo]` no ponto onde a semente entraria. Sem prova, o trecho sai como `[A CONFIRMAR: prova]` e a peça não sai como pronta.

**Entrega:** um arquivo por isca. Material de leitura sai em `isca-<nome>.md`. Formato interativo (quiz, avaliação, calculadora) sai em `arquitetura-<nome>.md`, com as perguntas, os ramos de resultado, a lógica de segmentação e a copy de cada resultado, mais uma tabela de roteamento `resultado → destino`, porque o que se entrega aqui é a arquitetura, não o arquivo renderizado. Script, template e banco de exemplos saem no `.md` preenchível, com os `[campos]` marcados. **STOP a cada bloco quando a peça é longa.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**O formato pedido é parte do contrato.** Se o pedido nomeia um formato de saída (PDF, `.docx`, imagem, slide), **o ativo naquele formato é entregável obrigatório**, não opcional: o `.md` sozinho não fecha o pedido, porque é o arquivo renderizado que o dono distribui a quem baixa. Com a ferramenta de render disponível, produza o arquivo (a rota está em "Como renderizar o formato pedido", abaixo). Sem a ferramenta, diga em 1 linha exatamente o que falta instalar e entregue o `.md` **marcado como rascunho**, nunca como isca pronta. Checagem verificável antes de fechar: liste o formato que o pedido nomeou e o caminho do arquivo entregue naquele formato, lado a lado; formato pedido sem arquivo correspondente reprova a entrega e sai declarado como item faltante em destaque, não diluído no relato.

**Leia primeiro:** `references/catalogo-iscas.md` (a mecânica do formato escolhido) · `references/artigo-isca.md` quando o formato for o artigo-isca (os 13 movimentos e os 5 princípios).

**Profundidade:** `references/processo-isca.md` (a mecânica dos 4 passos, isca, captura, nutrição, filtro) · `references/conducao-na-pratica.md`.

**Os dois eixos não-negociáveis:**
- **Entrega valor real.** Resolve de verdade um pedaço do problema. O leitor sai com uma coisa que dá pra usar hoje, não com um anúncio disfarçado.
- **Aponta pro método.** Deixa claro, sem pressão, que isso é uma fração. O quê e o porquê estão aqui; o como completo é o produto. A curiosidade mora no como, nunca no resultado.

**Estilo:** uma ideia por frase, número no lugar de adjetivo, vocabulário do cliente final (nunca "lead", "funil", "ticket" dentro da peça). Não narra o fluxo. A isca FILTRA: quem não é o avatar certo larga no meio, e isso é sucesso.

**Como renderizar o formato pedido.** A isca nasce em `.md`; o arquivo que o dono distribui sai desse `.md`. Teste a ferramenta antes de dizer que não dá, e cole a saída do teste no relatório.

| Formato pedido | Rota, na ordem | Sem nenhuma delas |
|---|---|---|
| **PDF** | `pandoc isca-<nome>.md -o isca-<nome>.pdf` · sem motor de composição, gere o `.docx` primeiro e converta com o LibreOffice em modo headless · sem os dois, monte com `reportlab`, em fluxo de parágrafos | entrega o `.md` marcado como rascunho e diz em 1 linha qual comando gera o PDF quando a ferramenta existir |
| **`.docx`** | `pandoc isca-<nome>.md -o isca-<nome>.docx` · ou a biblioteca `python-docx` | mesma regra: `.md` como rascunho, com o que falta nomeado |
| **Imagem ou slide** | com a **soft-designer** instalada, mande a peça pra ela · sem ela, entregue o `.md` e diga que o visual ficou de fora | mesma regra |

Se a **soft-exportar-documentos** estiver instalada, ela é a casa da conversão e vale mandar o `.md` por ela. A rota acima é o piso, porque não depende de nada instalado além do que o ambiente já tiver.

---

## Ação 4 · CAPTURA E DESTINO (fricção mínima, saída marcada)

**O que faz:** desenha a troca (o que o lead dá pra receber a isca) e crava pra onde ele vai depois.

**Precisa de:** a isca pronta da Ação 3 · o destino (carta, mini-webinar, webinar ou conversa) · o canal de contato que o dono usa de verdade.

**Sem o insumo:** sem destino declarado, **pare aqui**. Captura sem destino é lead morto, e é o erro número um da frente de funil. Pergunte só isso, numa frase: "depois que a pessoa baixar, pra onde você quer levar ela?".

**Entrega:** `captura-e-destino.md`, com o formulário (campos exatos), a promessa da troca, o destino nomeado e o link. **STOP pro OK.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/pagina-hospedagem.md` (os 6 elementos), só quando a isca tem página própria.

**Profundidade:** `references/processo-isca.md`.

**As regras:**
- **Captura.** Uma promessa específica. E-mail OU WhatsApp, não os dois. Zero campo que não serve a nada, porque cada campo a mais derruba conversão sem pagar por si. Formato interativo captura no resultado (o contato antes de revelar o resultado personalizado), e a fricção fica baixa porque a pessoa já quer o resultado.
- **Destino.** O próximo dólar manda: o destino é o problema que a isca ABRE, não o que ela fecha. Quem amou a isca quer naturalmente o próximo degrau.
- **A ponte até o destino** (o que mandar nos dias seguintes) é da **soft-funil-nutricao**. Se ela não estiver instalada, escreva aqui a régua mínima de 3 toques: entrega com instrução de uso, crença com prova colada, convite com o link.

---

## Ação 5 · PONTE DO FEED (OPCIONAL, só quando ele pergunta)

**O que faz:** liga o post do feed à entrega automática da isca.

**Precisa de:** a isca pronta e o link dela · a ferramenta de automação que o dono usa · a palavra-chave.

**Sem o insumo:** sem ferramenta de automação, a ponte vira manual: o dono responde o comentário pedindo o direct e manda o link à mão. Diga isso em 1 linha e siga.

**Entrega:** `ponte-feed.md`, com a palavra-chave, o texto do disparo e o texto do acompanhamento.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/processo-isca.md` (o passo do filtro).

**A configuração mínima:** 1 palavra-chave → 1 disparo (a mensagem com o link) → 1 acompanhamento em 24 a 48 horas ("conseguiu ver? alguma dúvida?") apontando pro destino da Ação 4. Só isso. Sequência complexa só infla.

**Dois modos:** o material de alto valor que resolve uma dúvida específica e atrai seguidor qualificado; ou o atalho, que em vez de entregar o material leva direto pro destino. O comentário vira ponto de entrada no funil.

---

## Ação 6 · O GATE (roda por dentro, em toda peça, e não imprime)

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.


**O que faz:** reprova a peça que não serve, antes de o dono ver.

**Precisa de:** a peça escrita (isca, captura, ponte).

**Sem o insumo:** o gate sempre tem o que precisa.

**Entrega:** nada. O gate é auditoria silenciosa; a tabela **nunca** vai pra saída. O que sai é a peça limpa.

**Leia primeiro:** `shared-references/crivo/03-gate-cub.md`.

**Profundidade:** `shared-references/filtro-anti-ia/padroes-banidos.md` e `falsos-positivos.md`.

**O veredito é o PIOR item.** Um ✗ qualquer refaz a peça e re-roda o gate do zero.

| Check | Passa se |
|---|---|
| **Ancorada na dor real** | nasce de fala literal da fonte (cita o N **real**) ou de prova real do dono. N inventado ou plausível reprova na hora. A aspa é substring literal e afirma a MESMA dor do avatar |
| **Entrega valor real** | resolve um pedaço de verdade, dá pra usar hoje. Reprova o anúncio disfarçado de guia. Passa quando o leitor sai sabendo fazer UMA coisa concreta |
| **Aponta pro método** | deixa claro que isso é fração. Reprova quem entrega o como inteiro (não sobra produto) e quem não conecta com o método (vira só dica) |
| **Top 3 do avatar** | ataca a prioridade 1 a 3, não a sétima. Isca brilhante sobre problema que ninguém prioriza reprova |
| **Valor óbvio no título** | o benefício fica claro só pelo NOME, sem ler o conteúdo. Reprova "guia definitivo sobre vendas". Passa "os 3 e-mails que reativam cliente parado há 6 meses" |
| **Próximo dólar, sem saturar** | resolve um sub-problema que LEVA ao produto e não mata o problema central. Existe um degrau intermediário entre a isca e o ticket alto |
| **Filtra o avatar certo** | repele quem não é cliente. Reprova "7 dicas que qualquer concorrente daria" |
| **Captura com fricção mínima** | uma promessa, um canal de contato, zero campo supérfluo, destino real marcado |
| **Formato pedido entregue** | o formato que o pedido nomeou está ao lado do caminho do arquivo naquele formato. Sem a ferramenta de render, o `.md` está marcado como rascunho e o que falta instalar está nomeado em destaque. `.md` sozinho contra um pedido que nomeava PDF, `.docx` ou imagem reprova |
| **C/U/B** | não é **C**onfuso (entende em 1 leitura), não é **I**nacreditável (promessa do tamanho da prova), não é **B**oring (tem tensão real, não é morno) |
| **CTA com destino** | a ação leva a um destino que existe e está nomeado, não "saiba mais" no vácuo |
| **Dá pra ver** | fecha o olho e enxerga a cena ou o resultado concreto, não "tenha mais clareza" |
| **Dá pra falsificar** | a promessa é um fato falsificável, não um adjetivo bonito |
| **Só você diz** | o concorrente direto não assina igual. Mecanismo ou cena proprietária, não promessa banal do nicho |
| **Anti-IA (duro)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz (o verbo que rima com "cravar" e as flexões dele; exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ refaz. Só tudo ✓ vai pro dono |

Com shell disponível, rode o lint de copy em `scripts/lint_copy.py` sobre o arquivo. Sem shell, faça a busca manual pelos dois bloqueios duros antes de marcar o anti-IA.

---

## O que esta skill NÃO faz

Cada rota é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Carrossel, reel, stories, post de feed | **soft-conteudo-*** | não faço. A isca troca material por contato; peça de alcance não |
| Headline ou gancho isolado | **soft-conteudo-headlines** | escrevo o título da isca dentro da Ação 2 |
| Página de captura ou de entrega | **soft-funil-landing** | escrevo os 6 elementos da página de hospedagem, sem a arquitetura completa |
| A régua que vem DEPOIS do download | **soft-funil-nutricao** | escrevo a régua mínima de 3 toques na Ação 4 |
| Carta de vendas ou VSL | **soft-funil-carta** | não faço. A isca aponta pra ela como destino |
| Mini-webinar | **soft-funil-miniwebinar** | não faço |
| Webinar completo ou perpétuo | **soft-webinar** | não faço. Aqui é a isca que LEVA a ele |
| Script de venda, objeção, fechamento | **soft-vendas-closer** | não faço |
| Posicionamento, nomear mecanismo | **soft-plano-posicionamento** | uso a entrevista curta da Ação 1 |
| Arte, visual, PNG | **soft-designer** | entrego o `.md` com a estrutura, sem o visual |

## Anti-patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Despejou a isca inteira de uma vez | Volta: produz, mostra, PARA pro OK a cada etapa |
| Isca genérica ("7 dicas de...") | Reescreve como amostra do mecanismo, que filtra, não dica que qualquer um daria |
| Entregou o COMO de graça | Guarda o como, é o produto. Dá o quê e o porquê |
| Guia de 80 páginas que ninguém consome | Encolhe pro mínimo consumível. Valor real é o que dá pra usar, não o volume |
| Captura com formulário longo | Corta pro essencial: uma promessa, um campo de contato, um destino |
| Pegou o contato e não tem destino | Marca o destino real antes de publicar a captura |
| Inventou número ou fala plausível | Só o real. Sem fonte, marca `[A CONFIRMAR: o quê]` e não conta como ancorado |
| Atrai todo mundo | Aperta a tese até o avatar errado largar no meio |
| Narrou o fluxo ("agora vou auditar") | Executa em silêncio e entrega só o resultado |
| Imprimiu a tabela do gate | O gate é interno. A saída é só a peça limpa |
| Inflou o formato em vez de mudar o tópico | Se o tópico não cabe num ganho rápido de menos de 20 minutos, troca o TÓPICO |
| Isca que mata o problema central | Reduz pra um sub-problema que ABRE a porta do próximo dólar |
| Pulou da isca grátis direto pro ticket alto | Garante o degrau intermediário antes |
| Escolheu o formato pelo que é fácil de produzir | Decide pela matriz de consciência e função (Ação 2) |
| Começou pela isca, não pela oferta | Ordem de retorno: destino primeiro, crença depois, isca por último |
| Usou duas grafias pra marcar furo | Uma só, em todo o arquivo: `[A CONFIRMAR: o quê]` |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/entrada-verbatim.md` (a ancoragem) · `references/ideacao-isca.md` (a ideação) · `references/catalogo-iscas.md` (os formatos) · `references/artigo-isca.md` (os 13 movimentos do artigo-isca) · `references/processo-isca.md` (isca, captura, nutrição, filtro) · `references/conducao-na-pratica.md` (o porquê das decisões) · `references/pagina-hospedagem.md` (os 6 elementos) · `shared-references/operacao-padrao.md`, `crivo/`, `filtro-anti-ia/` · `scripts/lint_copy.py`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `shared-references/crivo/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
