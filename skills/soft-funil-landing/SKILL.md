---
name: soft-funil-landing
description: >-
  Escreve QUALQUER tipo de landing page bloco a bloco, do hero ao botão, escolhida pelo objetivo do funil: captura, entrega de isca, qualificação, vendas no texto, obrigado, replay, fila de espera, link na bio, preços, comparação, quiz, oferta pós-compra, 404. Use quando o pedido for: "faz a landing", "página de captura", "página de vendas", "página de obrigado", "squeeze", "página de aplicação", "página de preços", "link na bio", "escreve o hero", "a página do meu produto", "página de replay". NÃO use pra: auditar o SEO de uma página que já está no ar, palavra-chave, título de busca (soft-seo-auditoria); a régua pós-isca (soft-funil-nutricao); as páginas do lançamento com carrinho (soft-launch); carrossel, reel e headline solta (soft-conteudo-*); a carta ou VSL em texto corrido (soft-funil-carta); o ATIVO da isca (soft-funil-isca); as páginas do webinar (soft-webinar); página do mini-webinar (soft-funil-miniwebinar); arte (soft-designer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Landing page, a decisão inevitável pro cliente certo

A página não convence. Ela organiza o argumento pra que o cliente certo chegue ao botão pensando "seria burrice não entrar agora". O cliente errado abandona antes do botão, e isso é sucesso. Página que convence todo mundo não converte ninguém.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Cada item da oferta é conferido contra o que a operação entrega hoje.** Rode `grep -rniE '<cada item da lista de inclusos>' <insumos>` e cole a saída. Item que aparecer numa reclamação, numa cobrança ou num registro de falha entra no handoff com `prometido na peça e em falha na operação: <item> · <arquivo:linha>`, pro dono decidir antes de publicar. A peça que promete o bônus que o cliente atual não está recebendo escreve a próxima reclamação.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**A lei-mãe:** um objetivo, um botão dominante, zero menu de navegação. As três exceções deliberadas são 404, link na bio e página de comparação.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as ações num caso fictício de nicho neutro: o briefing respondido, o tipo declarado, uma página de captura escrita por inteiro (os 5 blocos, prontos pra colar), um bloco de página de vendas e o que o gate reprovou.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola tudo que tem sobre a oferta e o público e eu escrevo a página). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou. Se faltar um insumo que a página não vive sem (a oferta, o objetivo da página, o público), pergunta AQUELE insumo e segue, sem voltar pro briefing inteiro.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o briefing curto uma pergunta de cada vez, e monta a página com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda a página (o tipo pela objetivo, a ordem dos blocos do hero ao botão, a prova, o CTA), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a decidir sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("meu público quer resultado", "o de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: a frase literal de um cliente, um case com número, o print de um depoimento. Prova real vira a âncora da página; resposta rasa vira página rasa. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar a página, fecha com UMA linha: "Quer outro hero? Mais curta? Outra ordem de blocos? Me diz o que ajustar que eu refaço só esse bloco." A oferta de refino não substitui o STOP nem o gate.


## Índice rápido: já sei o tipo, quero pular a seleção

Se o dono já disse o tipo com todas as letras, vá direto pra Ação 3 e abra a receita de blocos dele em `references/tipos-de-landing.md`. A contagem média de blocos de cada tipo está aqui, e é o que você declara no contrato de saída:

**Quem manda no número de blocos é a receita do tipo, não esta tabela.** A coluna abaixo é orientação de tamanho pra escolher o tipo; o número exato e a ordem estão em `references/tipos-de-landing.md`, na seção daquele tipo, e é ela que a entrega segue. Divergência entre as duas, a receita vence, e você declara em 1 linha qual seguiu.

| Tipo | Blocos | Botão dominante aponta pra |
|---|---|---|
| Captura (squeeze/opt-in) | 4 a 5 | formulário de e-mail ou WhatsApp |
| Captura de empresa | 6 a 7 | formulário com campos de qualificação |
| Entrega de isca | 4 a 6 | o download mais o próximo passo |
| Aquecimento (advertorial) | 8 a 12 | a página seguinte |
| Registro de evento | 4 (receita do Tipo 5) | formulário de inscrição |
| Obrigado / avanço | 3 a 4 | o próximo passo (agenda, grupo, oferta) |
| Replay | 5 a 7 | o vídeo, e depois o botão |
| Fila de espera | 4 a 5 | formulário curto |
| Aplicação / qualificação | 7 a 10 | formulário longo, com botão atrasado |
| Oferta pós-compra | 5 a 7 | sim de 1 clique |
| Link na bio | 5 a 8 links | o link primeiro da hierarquia |
| Preços | 5 a 7 | o plano do meio |
| Comparação | 5 a 8 | um botão por opção, tom neutro |
| Casca de quiz | 3 a 4 | começar o quiz |
| 404 | 3 a 4 | as saídas úteis |
| **Vendas no texto** | **14 blocos universais**, com peso variando por arquitetura | checkout, formulário ou conversa |

**A regra que separa Captura de Registro de evento:** o que decide é a NATUREZA do que está sendo prometido, não a palavra que o dono usou. Se o que o lead recebe acontece numa data e hora marcadas (aula gratuita ao vivo, webinário, live, masterclass, workshop, imersão), é **Registro de evento**, mesmo que o dono tenha pedido "página de captura". Consequência dura: data, hora e formato entram na primeira dobra. Se o dono ainda não cravou data e hora, escreva a página como Registro de evento assim mesmo e marque `[A CONFIRMAR: data e hora]` no lugar exato da primeira dobra, porque a página sem essa linha não converte inscrição. **Captura** fica só pro que o lead recebe na hora, sem agenda (PDF, checklist, aula gravada, lista de espera de conteúdo).

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "faz a landing", "preciso de uma página", sem dizer qual | **1 · BRIEFING**, depois **2 · SELETOR** |
| "página de captura", "squeeze", "página de obrigado", "link na bio", nomeando o tipo | **3 · OUTLINE** (o tipo já está declarado) |
| "página de vendas", "página do meu produto", "quero vender no texto" | **2.A · ARQUITETURA**, depois **3** |
| "escreve o hero", "escreve o bloco de garantia", "refaz o FAQ" | **4 · BLOCOS**, só naquele bloco |
| "olha essa página aqui e diz o que está errado" | **5 · GATE**, em modo auditoria, e devolve o diagnóstico bloco a bloco |

Pedido ambíguo: pergunte UMA coisa só, **"o que essa página precisa fazer agora: pegar contato, qualificar, vender, ou levar pro próximo passo?"**, e a resposta cai direto no seletor.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de posicionamento, avatar, mecanismo nomeado, voz ou prova: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

**As 6 leis de operação** (detalhe em `shared-references/operacao-padrao.md`, Seção 0): (1) cria o contexto antes da afirmação, zero palavra difícil; (2) abre ensinando o que faz; (3) é consultiva, puxa o contexto antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**, confere número, caso e depoimento; (6) **doc de saída enxuto pros 2 leitores**, zero meta-narração, só o insumo denso mais `[A CONFIRMAR]` onde falta.

---

## Ação 0 · ANCORAGEM (roda antes de tudo, não pula)

**O que faz:** abre a fonte de fala real e puxa a matéria-prima do hero e da prova.

**Precisa de:** a fonte, nesta ordem: descrição do projeto → posicionamento do dono → mensagens anteriores. De lá saem **3 a 5 falas de DOR e 3 a 5 de DESEJO**, literais, com o N.

**Sem o insumo:** três estados, declare o seu em 1 linha antes de escrever.
- **Tem fala real com N:** ancora nela e cita o N. Caminho ideal.
- **Tem nicho e prova, zero fala literal:** não invente fala nem N. Cada bloco ancora em prova real do dono; número não confirmado entra como `[A CONFIRMAR: número]` e não conta como ancorado. Avise que minerar 5 a 8 falas reais deixa a página bem mais cravada.
- **Sem nada:** vá pro briefing da Ação 1 e pergunte numa mensagem só.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Fala real não quer dizer banco estruturado.** Perfil que responde solto num `.md`, print de conversa, dúvida repetida no Direct, comentário: tudo isso é fonte válida e é o caso mais comum. O protocolo, quando não existe acervo pronto: (a) peça ou puxe falas reais do público dele de onde houver; (b) separe em 3 baldes, o que ele AMA (desejo), o que ele ODEIA (inimigo) e o que ele TEME (medo, objeção); (c) fala que aparece repetida em fontes independentes é padrão, fala que apareceu uma vez é anedota e você declara isso; (d) sem nenhuma fala real, a página sai marcada "rascunho genérico, não publicar", nunca como pronta. O detalhe está em `shared-references/crivo/01-entrada-verbatim.md`, seção do protocolo sem acervo pronto.

**Entrega:** nada de arquivo. É a matéria-prima das ações 3 e 4.

**Leia primeiro:** `shared-references/crivo/01-entrada-verbatim.md`.

---

## Ação 1 · BRIEFING (pergunta só o que falta, e sabe o que pode esperar)

**O que faz:** junta o insumo mínimo pra escolher o tipo e escrever a página.

**Precisa de:** o **objetivo da página** (o insumo-raiz, conferido antes de tudo) mais os campos da tabela abaixo.

**Sem o insumo:** os críticos param o fluxo; os adiáveis viram `[A CONFIRMAR]` e a página segue.

| Campo | Crítico? | Sem ele |
|---|---|---|
| **Objetivo da página** (o que ela faz agora) | **CRÍTICO** | pare e pergunte. Sem objetivo não há tipo, e sem tipo não há receita de blocos |
| **Destino do botão** (para onde ele leva) | **CRÍTICO** | pare e pergunte. Botão sem destino é página morta |
| **Produto** (nome, formato, o que entrega) | **CRÍTICO** no ramo de venda, adiável nos outros | no ramo de venda, pare. Nos outros, `[A CONFIRMAR: produto]` |
| **Ticket** (valor ou faixa) | **CRÍTICO** no ramo de venda | decide a arquitetura e a fricção do formulário. Fora do ramo de venda, adiável |
| **Cliente ideal** (quem é, o que já tentou, a dor de terceira camada) | **CRÍTICO** | sem isso a página fala com todo mundo e não filtra ninguém |
| **Temperatura do tráfego** (frio, morno, quente) | adiável | assuma **frio** (o caso mais exigente), declare a premissa em 1 linha |
| **Método nomeado** (nome próprio mais 3 a 4 etapas) | adiável | `[A CONFIRMAR: nome do mecanismo]` no bloco onde ele entraria |
| **Prova real** (casos com nome, número e prazo) | adiável, mas caro | `[A CONFIRMAR: prova]` e a página não sai como pronta pra publicar |
| **Bônus e garantia** | adiável | só no ramo de venda. Ausência some, não vira recheio |
| **Razão de urgência** | adiável | só entra se for verdade. Sem razão real, a página fica sem urgência |

**Entrega:** nada de arquivo. É o que alimenta o seletor.

**Leia primeiro:** nada obrigatório aqui. O briefing é uma mensagem só.

**Regra:** se faltar algo crítico, pergunta **numa mensagem só**, listando o que falta. Não chuta e não pergunta em conta-gotas.

---

## Ação 2 · SELETOR POR OBJETIVO (uma linha, sem pergunta)

**O que faz:** converte o objetivo confirmado em tipo de página e framework de copy raiz.

**Precisa de:** o objetivo da Ação 1.

**Sem o insumo:** volte pra Ação 1. O seletor não roda sem objetivo.

**Entrega:** 1 linha declarada no topo do entregável: *"objetivo X → tipo Y → framework Z, por isso uso a receita Y."*

**Leia primeiro:** `references/tipos-de-landing.md`, na receita do tipo que saiu.

**Profundidade:** `references/frameworks-copy.md` (o passo a passo do framework raiz).

| Objetivo (o que a página faz agora) | Tipo de página | Framework raiz |
|---|---|---|
| Pegar e-mail ou WhatsApp | Captura (squeeze/opt-in) | PAS · 4Us |
| Capturar lead de empresa | Captura de empresa | 4Ps |
| Entregar a isca | Entrega de isca | BAB |
| Aquecer sem vender | Aquecimento (advertorial) | SSS · Star-Chain-Hook |
| Registrar em evento | Registro de evento | AIDA |
| Confirmar e avançar | Obrigado / avanço | direto |
| Recuperar quem sumiu | Replay | Slippery Slide |
| Juntar fila | Fila de espera | 4Us |
| Qualificar lead caro | Aplicação / qualificação | PASTOR · 12 passos |
| Aumentar ticket pós-compra | Oferta pós-compra | PAS · The Reverse |
| Centralizar o social | Link na bio | microcopy |
| Mostrar planos | Preços | FAB |
| Ajudar a comparar | Comparação | FAB |
| Segmentar e capturar | Casca de quiz | curiosidade |
| Resgatar quem caiu fora | 404 como landing | leve |
| **Vender no texto** | **as 4 arquiteturas** (Ação 2.A) | ADMA |

### Ação 2.A · ARQUITETURA (SÓ quando o objetivo é vender no texto)

**O que faz:** decide a arquitetura por ticket, produto e temperatura, e declara qual usa e por quê.

**Precisa de:** ticket, tipo de produto e temperatura do tráfego, da Ação 1.

**Sem o insumo:** sem ticket, assuma a **Híbrida** (é a que aguenta a faixa mais larga), marque `[A CONFIRMAR: ticket]` e declare a premissa em 1 linha.

**Entrega:** 1 linha, junto da linha do seletor.

**Leia primeiro:** `references/arquiteturas.md`.

| Cenário | Arquitetura |
|---|---|
| Produto digital de ticket baixo, qualquer tráfego | **VSL completa**, o vídeo carrega o argumento, o texto apoia |
| Produto digital de ticket médio, tráfego frio ou morno | **Híbrida**, vídeo curto mais texto robusto |
| Mentoria ou consultoria de ticket alto, tráfego morno ou quente | **Autoridade**, sem vídeo, texto cirúrgico e prova empilhada |
| Serviço recorrente, qualquer ticket | **Problema e solução**, custo de não agir mais método mais acesso |

---

## Ação 3 · OUTLINE (o esqueleto antes do corpo)

**O que faz:** entrega a lista numerada dos blocos da receita do tipo, com a headline de cada um e onde fica cada botão.

**Precisa de:** o tipo declarado na Ação 2 (ou trazido pelo dono).

**Sem o insumo:** não há outline sem tipo. Volte pra Ação 2.

**Entrega:** `outline-<tipo>.md`, os blocos numerados. **STOP. O dono vê o esqueleto antes do corpo.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/tipos-de-landing.md` (a sequência de blocos do tipo) ou `references/arquiteturas.md` (quando o objetivo é vender no texto).

---

## Ação 4 · BLOCOS (escreve um por vez, com parada)

**O que faz:** escreve a copy de cada bloco da receita, na ordem, parando a cada um.

**Precisa de:** o outline aprovado · as falas da Ação 0 · a prova real.

**Sem o insumo:** bloco que depende de prova que não existe sai com `[A CONFIRMAR: prova]` no lugar exato e não conta como pronto. Bloco que depende do nome do mecanismo sai com `[A CONFIRMAR: nome do mecanismo]`.

**Entrega:** `pagina-<tipo>.md`, bloco a bloco, na ordem em que aparecem na tela, com o destino de cada botão marcado. **STOP por bloco.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/blocos-copy.md` (a copy de cada bloco do ramo de venda) · `references/mecanicas-assinatura.md` (quando o tipo tem mecânica própria).

**Profundidade:** `references/processo-landingpage.md` (os 14 blocos universais e a auditoria de 5 movimentos) · `references/vsl-script.md` (antes do bloco do vídeo) · `references/frameworks-copy.md` · `references/conducao-na-pratica.md`.

**Os 14 blocos do ramo de venda** (o peso e a ordem mudam por arquitetura, nenhum some): hero · vídeo quando aplica · para quem é e para quem não é · o problema (dor de terceira camada) · mecanismo do problema · apresentação do método · prova social · o produto por dentro · bônus · oferta e empilhamento · garantia · sobre o autor · perguntas frequentes · botão final.

**Duas regras do bench que valem em todo tipo:**
- **A fricção do formulário casa com a temperatura e o ticket.** Um campo na captura fria, formulário longo de qualificação no ticket alto. A fricção é alavanca, não defeito.
- **Botão atrasado é assinatura de vídeo longo e de aplicação.** Ele aparece no momento do convite, não no topo.

**Antes de fechar a ação, rode a auditoria de 5 movimentos** (sonhos incentivados com cena e número · falhas justificadas sem condescendência · medos nomeados e dissolvidos com mecanismo · desconfianças confirmadas com verdade dura · inimigo-categoria nomeado sem ataque pessoal), descrita em `references/processo-landingpage.md`. É pré-filtro: movimento ausente, reforça antes do gate. O veredito final é do gate.

**Regras invioláveis enquanto escreve:** zero menu de navegação · uma promessa na página inteira · prova nunca é só elogio (nome mais nicho mais resultado com número e prazo), e uma prova real acima da dobra · bônus mata objeção nomeada, não é recheio · garantia é vendida, com headline própria · urgência real ou silêncio · cada bloco cabe em 1 tela de celular · mostra resultado e função, nunca o passo a passo executável · uma ideia por frase, número no lugar de adjetivo, vocabulário do cliente final.

---

## Ação 5 · O GATE (roda por dentro, em cada bloco, e não imprime)

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento). Palavra fora dessa lista não é gatilho e não conta**: título nomeado com "autoridade + especificidade" ou "ação + destino explícito" fica com zero gatilhos rastreáveis e volta pro passo de escrita. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Rótulo de seção não é título, e a coluna diz qual é qual.** Classifique cada título de bloco da página como `rótulo` ou `tese`, numa coluna própria da checagem. Rótulo nomeia o assunto e não afirma nada (`Benefícios`, `Sobre`, `O método`, `Depoimentos`); tese afirma alguma coisa que o leitor pode discordar (`Você já tentou, e não foi falta de esforço`). O título de bloco da página é a primeira coisa que o leitor lê antes de decidir se continua, e um documento de rótulos não segura ninguém. Cole a coluna inteira, um por linha, na forma `<título> | rótulo ou tese`, e **todo `rótulo` volta pro passo de escrita** antes de a peça sair. Feche com `títulos de seção: N · em tese: N · rótulos restantes: 0`.

**O hero passa pela régua R1 a R7 ANTES dos outros checks do bloco**, e a checagem vai na peça com a coluna da R1 preenchida: `<hero> | afirma a mais que o pedido: <o quê>`. **Quando o pedido do dono já nomeia o evento ("a página da minha aula X"), o nome do evento não pode ser o hero.** O nome vai na sub-headline, junto da data e do formato; o hero afirma o que a leitora ganha, o que ela para de fazer, ou o inimigo que ela reconhece. Prefixo na frente do nome ("Aula ao vivo:", "Aula gratuita:", "Masterclass:") não é ganho e não salva o hero. Checagem colada: `hero é o nome do evento com prefixo? sim reprova`.

**A landing é peça publicável, e o endereço de cada coisa é fixo.** A página leva os blocos, a checagem do hero e a linha de fechamento do inventário, e mais nada. Tabela de inventário, origem dos números, régua título a título e pendências vão em `HANDOFF-<slug>.md`, arquivo irmão no disco. Os dois erros são simétricos e reprovam igual: encher a página publicável de checagem, e entregar a página sem a checagem do hero que esta ação manda pôr nela. **Checagem colada antes de fechar, com as quatro saídas: (1) `ls <pasta>` mostra o handoff? (2) `wc -l <peça>` devolve menos de 60 linhas? (3) `grep -c 'afirma a mais' <peça>` devolve 1 ou mais? (4) `grep -c 'Dados fornecidos' <peça>` devolve 1?** As duas primeiras pegam a peça inchada; as duas últimas pegam a peça esvaziada, e as duas falhas reprovam igual. Qualquer uma em não, o conteúdo muda de arquivo antes da entrega: esta cláusula diz o que VAI na peça tanto quanto o que sai dela.

**A peça não explica a própria conduta.** Frase que descreve o que a página faz ou deixa de fazer ("a aula mostra a lógica sem prescrever treino individual", "sem transformar orientação em promessa", "apresenta a lógica do método") é nota de método e vai pro handoff. No lugar dela entra a cena: o que a leitora vai conseguir fazer depois, dita em concreto. A leitora não contratou a explicação da sua conduta, ela veio pelo ganho. Checagem: `grep -nE 'sem prescrever|sem transformar|sem garantir|apresenta a lógica' <peça>` volta vazio.

**As contagens da régua não admitem justificativa.** `com inimigo ou inversão: N de N` abaixo da metade manda o lote de títulos de volta pro passo de escrita, e a linha "a baixa contagem é deliberada" é resposta inválida: se o tipo de página dispensa a inversão, a exceção está escrita na receita do tipo, não na entrega.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase. **O teste não é "a frase fica agramatical": é "a frase existiria sem o dado?".** Frase cuja única função é registrar a pendência ("Prazo exato do caso: [A CONFIRMAR: número de semanas]") está no miolo por definição e sai da peça, mesmo parecendo um campo. **Antes de marcar qualquer número, grepe os insumos (`grep -in '<termo>' <insumos>`) e cole a saída: dado que existe no disco nunca vira marcador.** Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado, e a conta vem ANTES de escrever a peça.** Monte a conta em 3 passos e cole no processo: (1) `grep -c '^-' <perfil>` = C campos; (2) percorra os campos e escreva `campo <n>: <k> valores` para todo campo com k maior que 1, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1; (3) some, e M é o piso. Cole `campos no perfil: C · valores desdobrados: M · linhas do inventário: M`. **Inventário com menos de M linhas reprova sem análise de conteúdo, e a linha que agrupa dois dados conta como UMA linha e como N dados faltando.** A ordem é o que decide: a conta feita depois da peça vira justificativa, e a conta feita antes vira o alvo. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **O universo é o arquivo de perfil inteiro, e nenhuma seção dele é 'de outra skill'.** Insumo listado no perfil conta como dado fornecido e entra no inventário, ainda que a coluna diga 'descartado porque pertence a outro funil': relevância decide a coluna usado ou descartado, nunca a existência da linha. **`Dados fornecidos` menor que o `grep -c '^- '` bruto reprova sem análise de conteúdo**, porque significa que uma parte do arquivo foi excluída do universo em vez de descartada com motivo.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Todo número da página carrega, no inventário, a linha do perfil de onde saiu.** Preço, prazo, duração, quantidade, frequência, idade, percentual: nenhum entra por dedução nem por cruzamento. **Quando a linha de origem descreve um objeto diferente do que a página vende, o número não entra:** vira `[A CONFIRMAR: <o dado>]` no lugar exato. A duração do webinar gravado não é a duração da aula ao vivo; o preço de outro produto não é o preço deste. Checagem colada, um número por linha: `<número> | origem: <perfil, linha N> | mesmo objeto da página? sim/não`. Um `não` reprova a página, e descartar o contexto e manter o número que só existia dentro dele é o erro que essa checagem existe pra pegar.

**O corpo da página contém só o que a leitora lê.** Instrução dirigida ao dono ("confirme", "valide", "ajuste antes de publicar", "cheque as regras do conselho") vai no handoff, nunca dentro de um bloco: briefing impresso dentro do produto é o dono falando sozinho na cara do cliente. A ressalva de nicho que a leitora precisa ler fica; a ordem de serviço para o dono sai. Checagem verificável: `grep -niE 'antes de publicar|confirme|valide|verifique as regras' <arquivo da página>` tem que voltar vazio.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.


**O que faz:** reprova o bloco que não serve, antes de o dono ver. Serve também como modo auditoria, quando o dono cola uma página pronta e pede diagnóstico.

**Precisa de:** o bloco escrito.

**Sem o insumo:** o gate sempre tem o que precisa.

**Entrega:** em modo normal, a tabela **nunca** vai pra saída; o que acompanha a peça é um **relato de 3 a 6 linhas** do que o gate conferiu (a fala real que sustentou a promessa, o pior bloco e por quê, o que foi reescrito, o que ficou pendente). Em modo auditoria de página existente, entrega `diagnostico-pagina.md` com o bloco, o check que falhou e a correção.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `shared-references/crivo/03-gate-cub.md`.

**Profundidade:** `references/mecanicas-assinatura.md` (o gate lê dela) · `shared-references/filtro-anti-ia/padroes-banidos.md` e `falsos-positivos.md` · `shared-references/filtro-mobile-first/escaneabilidade-texto.md`.

**O veredito é o PIOR item.** Um ✗ refaz o bloco.

| Check | Passa se |
|---|---|
| **Ancorada** | nasce de fala literal da fonte (cita o N **real**) ou de prova real do dono. N inventado ou plausível reprova na hora |
| **Uma promessa** | a página inteira sustenta UMA promessa. O bloco não abre uma segunda concorrente |
| **Um botão dominante** | um objetivo e um botão. O botão deste bloco aponta pro mesmo lugar dos outros. Exceção só em 404, link na bio e comparação, e só quando a multiplicidade é hierarquizada |
| **Botão com destino** | destino explícito (conversa, checkout, formulário), nunca "saiba mais" vago |
| **Prova real acima da dobra** | ao menos uma prova real (nome, número, prazo) visível antes do primeiro rolar |
| **Tempo de leitura do bloco** | o bloco lê em **até 20 segundos** em voz alta (aproximadamente 45 a 60 palavras). O hero lê em até 8 segundos. Bloco acima disso quebra em dois ou corta |
| **Cabe em 1 tela de celular** | o bloco cabe e fica legível numa tela de celular, sem rolagem lateral, sem parágrafo-bloco |
| **Zero fricção** | nenhuma distração, link de saída ou segundo caminho que tire o olho do botão |
| **Filtra o cliente certo** | a copy exclui o cliente errado de propósito. Não maximiza volume |
| **Promessa não-redonda** | específica e calculável, não arredondada pra soar grande |
| **C/U/B** | não é **C**onfuso (entende de primeira), não é **I**nacreditável (a afirmação tem prova ou mecanismo do lado), não é **B**oring (tem tensão e cena real) |
| **Dá pra ver** | fecha o olho e enxerga a cena. Reprova "mais clareza". Passa "a agenda lota 3 semanas antes" |
| **Dá pra falsificar** | é fato falsificável, não adjetivo |
| **Só você diz** | o concorrente direto não assina igual |
| **Formulário casa com a temperatura** | a fricção é proporcional ao ticket e deliberada: um campo no frio, vários no qualificado |
| **Mecânica-assinatura presente** | quando o tipo tem mecânica própria, ela está implementada de fato: contato antes do resultado no quiz · sim e não na oferta pós-compra · três planos com isca de decisão nos preços · próximo passo no obrigado e no replay · janela de escassez real |
| **Anti-IA (duro)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz (o verbo que rima com "cravar" e as flexões dele; exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ refaz. Só tudo ✓ vai pro dono |

Com shell disponível, rode o lint de copy em `scripts/lint_copy.py` sobre o arquivo. Sem shell, faça a busca manual pelos dois bloqueios duros antes de marcar o anti-IA. **O lint lê o arquivo inteiro, e as notas `[A CONFIRMAR]` estão dentro dele:** um travessão longo ou um verbo-freio escrito na sua própria nota de bastidor reprova a página igual. Escreva as notas com o mesmo cuidado da copy.

---

## Ação 6 · FECHO (mostra e para)

**O que faz:** entrega o bloco limpo e confere a congruência da página inteira.

**Entrega:** só o bloco, sem tabela de gate, sem meta. Pergunta "esse bloco te serve? sigo pro próximo?" e **espera o OK**.

No fim da página, confira: ela repete UMA promessa e aponta pra UM destino, do primeiro bloco ao último.

---

## O que esta skill NÃO faz

Cada rota é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Carrossel, reel, stories | **soft-conteudo-*** | não faço |
| Headline isolada | **soft-conteudo-headlines** | escrevo a headline do hero dentro da Ação 4 |
| A carta ou o roteiro de VSL em texto corrido | **soft-funil-carta** | escrevo o bloco do vídeo com hook, corpo e fecho, sem o roteiro longo |
| O ATIVO da isca (o PDF, o quiz por dentro) | **soft-funil-isca** | monto só a casca da página, não o material |
| A régua de mensagens depois da captura | **soft-funil-nutricao** | escrevo a mensagem de entrega, e mais nada |
| As 3 páginas do webinar | **soft-webinar** | escrevo as 3 pela receita de captura, obrigado e checkout daqui |
| A página do mini-webinar | **soft-funil-miniwebinar** | monto pela receita de entrega de isca com vídeo |
| Posicionamento, oferta, nomear mecanismo | **soft-plano-posicionamento** | uso o briefing crítico da Ação 1 |
| Script de venda, objeção, prospecção | **soft-vendas-closer** / **soft-vendas-sdr** | não faço |
| Arte, visual, PNG | **soft-designer** | entrego o `.md` bloco a bloco, sem o visual |

## Anti-patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Despejou a página inteira de uma vez | Volta: tipo, outline, um bloco por vez com gate |
| Aplicou os 14 blocos de venda numa página de captura | Usa a receita enxuta DO TIPO (captura tem 4 a 5 blocos) |
| Duas promessas competindo | Corta a segunda |
| Vários botões pra destinos diferentes | Um botão dominante, um destino, repetido nos picos |
| Botão "saiba mais" | Destino explícito |
| Pôs depoimento antes da promessa | Prova sempre depois da promessa |
| Prova só elogio, sem número | Nome, nicho, resultado com número e prazo |
| Inventou depoimento ou número plausível | Só prova real. Sem fonte, `[A CONFIRMAR: prova]` |
| Copy tentando agradar todo mundo | Filtra na entrada: para quem é e para quem não é |
| Promessa redonda ("dobre seu faturamento") | Número específico e calculável da prova real |
| Cronômetro falso em replay | Escassez real com janela que expira, ou silêncio |
| Página de obrigado sem saída | Sempre um próximo passo |
| Quiz que pede o contato depois do resultado | Contato antes do resultado, senão não captura |
| Link na bio com 12 links iguais | Máximo 8, hierarquia de intenção em 3 camadas |
| Oferta pós-compra sem o "não, obrigado" discreto | Sim de 1 clique em destaque, recusa pequena embaixo |
| Solução genérica sem mecanismo nomeado | Nomeia o mecanismo |
| Bloco com menu ou link de saída | A única saída é o botão |
| Parágrafo-bloco que não cabe no celular | Quebra em frases curtas, uma tela por bloco |
| Bloco que leva 40 segundos pra ler | Quebra em dois ou corta. O teto é 20 segundos por bloco |
| Narrou o fluxo ("agora vou auditar") | Executa em silêncio e entrega o bloco limpo |
| Imprimiu a tabela do gate | O gate é interno |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/tipos-de-landing.md` (o catálogo de tipos e a receita de blocos de cada um) · `references/frameworks-copy.md` (a biblioteca de frameworks) · `references/mecanicas-assinatura.md` (as regras transversais e a mecânica própria de cada tipo) · `references/arquiteturas.md` (as 4 arquiteturas do ramo de venda) · `references/processo-landingpage.md` (os 14 blocos e a auditoria de 5 movimentos) · `references/blocos-copy.md` (a copy de cada bloco) · `references/vsl-script.md` (o roteiro do vídeo na página) · `references/conducao-na-pratica.md` · `shared-references/operacao-padrao.md`, `crivo/`, `filtro-anti-ia/`, `filtro-mobile-first/` · `scripts/lint_copy.py`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
