---
name: soft-funil-landing
description: >-
  Escreve e entrega PRONTA qualquer landing page: a copy bloco a bloco e a página em HTML de arquivo único (inscrição ou venda mais a página de obrigado), com o tipo e o tamanho escolhidos pelo objetivo do funil e pelo tráfego: captura, inscrição em aula, live ou webinar (curta, longa grátis, longa paga com lotes), entrega de isca, qualificação, vendas no texto, obrigado, replay, fila de espera, link na bio, preços, comparação, quiz, oferta pós-compra, 404. Use quando o pedido for: "faz a landing", "página de captura", "página de inscrição da minha aula", "página de vendas", "página do ingresso", "página de obrigado", "squeeze", "página de aplicação", "página de preços", "link na bio", "escreve o hero", "a página do meu produto", "página de replay". NÃO use pra: auditar o SEO de uma página que já está no ar, palavra-chave, título de busca (soft-seo-auditoria); a régua pós-isca (soft-funil-nutricao); as páginas do lançamento com carrinho (soft-launch); carrossel, reel e headline solta (soft-conteudo-*); a carta ou VSL em texto corrido (soft-funil-carta); o ATIVO da isca (soft-funil-isca); o webinar inteiro, com aula, oferta e mensagens (soft-webinar); página do mini-webinar (soft-funil-miniwebinar); arte de anúncio, carrossel ou PNG (soft-designer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Landing page, a decisão inevitável pro cliente certo

A página não convence. Ela organiza o argumento pra que o cliente certo chegue ao botão pensando "seria burrice não entrar agora". O cliente errado abandona antes do botão, e isso é sucesso. Página que convence todo mundo não converte ninguém.

**O que é "pronto" nesta skill (vale pra toda ação).** A pasta de saída tem `pagina.html`, `obrigado.html` (quando o pedido ou o tipo pede obrigado), `pagina-<slug>.md` com a copy das duas e `_notas-operador.md`. Pronto é: `python3 scripts/conferir_fontes.py --entrega <pasta de saída> --insumo <arquivos do dono>` com exit 0, a conferência de estrutura da Ação 5 toda em sim e o lint com exit 0 em cada `.md`. A saída das conferências vai pro `_notas-operador.md`, nunca pra página. O relato no chat abre com `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `O que conectar` (formulário, WhatsApp ou grupo, checkout, pixel). Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **Publicar, hospedar ou subir a página em qualquer ferramenta só com ordem nomeada do dono.**

**Cada item da oferta é conferido contra o que a operação entrega hoje.** Rode `grep -rniE '<cada item da lista de inclusos>' <insumos>` e cole a saída. Item que aparecer numa reclamação, numa cobrança ou num registro de falha entra no `_notas-operador.md` com `prometido na peça e em falha na operação: <item> · <arquivo:linha>`, pro dono decidir antes de publicar. A peça que promete o bônus que o cliente atual não está recebendo escreve a próxima reclamação.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** Cada linha `SEM FONTE`, `REVISAR FORA DE NOTA` ou `REPROVA` sai da página ou vira pergunta no `_notas-operador.md`. Depois de corrigir, rode de novo.

**A lei-mãe:** um objetivo, um botão dominante, zero menu de navegação. As três exceções deliberadas são 404, link na bio e página de comparação.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as ações num caso fictício de nicho neutro: o briefing respondido, o tipo declarado, uma página de captura escrita por inteiro (os 5 blocos, prontos pra colar), um bloco de página de vendas e o que o gate reprovou.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola tudo que tem sobre a oferta e o público e eu escrevo a página). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): entrega a tarefa inteira de uma vez, as páginas em HTML, a copy e as notas, sem parada no meio. Se faltar um insumo que a página não vive sem (a oferta, o objetivo da página, o público), pergunta AQUELE insumo e segue, sem voltar pro briefing inteiro.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o briefing curto uma pergunta de cada vez, mostra o outline e escreve um bloco por vez, com parada, antes do render.

**Ensina enquanto faz (parte 2):** em cada escolha que muda a página (o tipo pela objetivo, a ordem dos blocos do hero ao botão, a prova, o CTA), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a decidir sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("meu público quer resultado", "o de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: a frase literal de um cliente, um case com número, o print de um depoimento. Prova real vira a âncora da página; resposta rasa vira página rasa. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar a página, fecha com UMA linha: "Quer outro hero? Mais curta? Outra ordem de blocos? Me diz o que ajustar que eu refaço só esse bloco." A oferta de refino não substitui a conferência.


## Índice rápido: já sei o tipo, quero pular a seleção

Se o dono já disse o tipo com todas as letras, vá direto pra Ação 3 e abra a receita dele em `references/tipos-de-landing.md` (ou o molde do evento em `references/moldes-evento.md`). A contagem de blocos de cada tipo está aqui:

**O tamanho sai do tráfego e do evento; a receita dá a ordem.** No registro de evento, a Ação 2.B escolhe curto, longo grátis ou longo pago pela temperatura e pelo preço do evento, e o molde escolhido manda. Nos outros tipos, a receita em `references/tipos-de-landing.md` dá os blocos e a ordem. A escolha vai numa linha, com o motivo.

| Tipo | Blocos | Botão dominante aponta pra |
|---|---|---|
| Captura (squeeze/opt-in) | 4 a 5 | formulário de e-mail ou WhatsApp |
| Captura de empresa | 6 a 7 | formulário com campos de qualificação |
| Entrega de isca | 4 a 6 | o download mais o próximo passo |
| Aquecimento (advertorial) | 8 a 12 | a página seguinte |
| Registro de evento | curto 10 · longo grátis 14 · longo pago 14 (Ação 2.B) | formulário de inscrição, ou checkout do ingresso |
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

**A regra que separa Captura de Registro de evento:** o que decide é a NATUREZA do que está sendo prometido, não a palavra que o dono usou. Se o que o lead recebe acontece numa data e hora marcadas (aula ao vivo, webinário, webinar perpétuo com sessões, live, masterclass, workshop, imersão), é **Registro de evento**, mesmo que o dono tenha pedido "página de captura". Consequência dura: data e hora (ou o seletor de horário), duração e formato entram na primeira tela, com o dado do insumo. Sem data no insumo, a copy leva `[DO DONO: data e hora]`, a pergunta vai pro `_notas-operador.md` e o HTML não sai com data inventada. **Captura** fica só pro que o lead recebe na hora, sem agenda (PDF, checklist, aula gravada que se assiste na hora, lista de espera de conteúdo).

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "faz a landing", "preciso de uma página", sem dizer qual | **1 · BRIEFING**, depois **2 · SELETOR** |
| "página de captura", "squeeze", "página de obrigado", "link na bio", nomeando o tipo | **3 · OUTLINE** (o tipo já está declarado) |
| "página de inscrição da minha aula", "do webinar", "da live", "venda do ingresso da imersão" | **2 · SELETOR** → **2.B · TAMANHO** → **3** a **7** |
| "página de vendas", "página do meu produto", "quero vender no texto" | **2.A · ARQUITETURA**, depois **3** |
| "faz a página em HTML", "monta a página pronta" com a copy já escrita | **7 · RENDER** |
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
| **Destino do botão** (formulário, checkout ou conversa) | **CRÍTICO** o tipo de destino; o link é adiável | sem o link, o atributo do HTML fica `#CONECTAR-...` e o item entra em `O que conectar` |
| **Produto** (nome, formato, o que entrega) | **CRÍTICO** no ramo de venda, adiável nos outros | no ramo de venda, pare. Nos outros, `[A CONFIRMAR: produto]` |
| **Ticket** (valor ou faixa) | **CRÍTICO** no ramo de venda | decide a arquitetura e a fricção do formulário. Fora do ramo de venda, adiável |
| **Cliente ideal** (quem é, o que já tentou, a dor de terceira camada) | **CRÍTICO** | sem isso a página fala com todo mundo e não filtra ninguém |
| **Temperatura do tráfego** (frio, morno, quente) | adiável | assuma **frio** (o caso mais exigente) e declare a premissa em 1 linha. No registro de evento ela decide o tamanho (Ação 2.B) |
| **Evento** (grátis ou pago, data fixa ou sessões, duração, formato, política de gravação) | adiável | só do insumo, com a palavra dele: gravado ou perpétuo nunca vira "ao vivo"; "grátis" e "sem custo" só se o insumo diz do próprio evento. O que faltar some da página (sem horário, o seletor sai) e vira pergunta no `_notas-operador.md` |
| **Canal de lembrete e de acesso** (WhatsApp, e-mail, grupo, link) | adiável | só com linha do insumo. Sem ela, a página não promete canal nem prazo, e a pergunta vai pro `_notas-operador.md` |
| **Método nomeado** (nome próprio mais 3 a 4 etapas) | adiável | `[A CONFIRMAR: nome do mecanismo]` no bloco onde ele entraria |
| **Prova real** (casos com nome, número e prazo) | adiável, mas caro | `[A CONFIRMAR: prova]` e a página não sai como pronta pra publicar |
| **Bônus e garantia** | adiável | só no ramo de venda. Ausência some, não vira recheio |
| **Razão de urgência** | adiável | só entra se for verdade e tiver motivo no insumo (data, número de vagas, virada de lote). Sem isso, a página fica sem urgência |

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
| Registrar em evento | Registro de evento (tamanho pela Ação 2.B) | AIDA |
| Vender o ingresso de um evento | Registro de evento, molde longo pago | AIDA com oferta |
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

### Ação 2.B · TAMANHO (registro de evento: curto, longo grátis ou longo pago)

**O que faz:** escolhe o molde pelo tráfego e pelo preço do evento. **Precisa de:** temperatura (sem ela, frio) e se o evento é grátis ou pago. **Entrega:** 1 linha no topo do `.md`: `Tráfego <X, e de onde tirei> · evento <grátis ou pago> → molde <Y>, porque <motivo>.` **Leia primeiro:** `references/moldes-evento.md` (a regra, os 3 moldes, o hero, o obrigado, a escassez).

| Tráfego | Grátis | Pago |
|---|---|---|
| Quente | CURTO | LONGO PAGO |
| Morno, frio ou cético | LONGO GRÁTIS | LONGO PAGO |

Motivo: a curta confia que o anúncio já vendeu a aula; no frio, o formulário no topo pega quem decidiu e o resto da página trabalha quem precisa de mais motivo. Pago é página de venda, com formulário no fim.

---

## Ação 3 · OUTLINE (o esqueleto antes do corpo)

**O que faz:** entrega a lista numerada dos blocos da receita do tipo, com a headline de cada um e onde fica cada botão.

**Precisa de:** o tipo declarado na Ação 2 (ou trazido pelo dono).

**Sem o insumo:** não há outline sem tipo. Volte pra Ação 2.

**Entrega:** o topo de `pagina-<slug>.md`: a linha do molde e os blocos numerados, com a headline de cada um e onde fica cada botão. No modo guiado, **STOP: o dono vê o esqueleto antes do corpo**; no direto, segue.

**Leia primeiro:** `references/moldes-evento.md` (registro de evento) · `references/tipos-de-landing.md` (os outros tipos) · `references/arquiteturas.md` (vender no texto).

---

## Ação 4 · BLOCOS (a copy, bloco a bloco)

**O que faz:** escreve a copy de cada bloco da receita, na ordem (no modo guiado, com parada a cada um).

**Precisa de:** o outline · as falas da Ação 0 · a prova real.

**Sem o insumo:** bloco que depende de prova que não existe sai com `[A CONFIRMAR: prova]` no lugar exato e não conta como pronto. Bloco que depende do nome do mecanismo sai com `[A CONFIRMAR: nome do mecanismo]`.

**Entrega:** `pagina-<slug>.md`, bloco a bloco, na ordem da tela, com o destino de cada botão marcado, mais a copy do obrigado. Parada por bloco só no modo guiado.

**Hero de inscrição.** Promete o resultado DA AULA ou do evento, com o "mesmo que / mesmo sem" sempre que o insumo lista objeção. O teste do espelho não vale aqui: o anúncio já prometeu e a página repete (Message Match). Tese, inimigo e diagnóstico ficam pro corpo; nome e formato do evento vão na etiqueta. Número de autoridade nas 5 primeiras linhas. Molde e contraste em `references/moldes-evento.md`, seção 2.

**Obrigado que puxa comparecimento.** Confirma, repete data e hora (ou o horário escolhido), UM próximo passo (agenda por padrão; grupo ou WhatsApp só com o link no insumo), um pequeno compromisso e o que preparar. Canal ou lembrete que o insumo não traz vira pergunta no `_notas-operador.md`. Molde em `references/moldes-evento.md`, seção 8.

**Leia primeiro:** `references/moldes-evento.md` (registro de evento e obrigado) · `references/blocos-copy.md` (a copy de cada bloco do ramo de venda) · `references/mecanicas-assinatura.md` (quando o tipo tem mecânica própria).

**Profundidade:** `references/processo-landingpage.md` (os 14 blocos universais e a auditoria de 5 movimentos) · `references/vsl-script.md` (antes do bloco do vídeo) · `references/frameworks-copy.md` · `references/conducao-na-pratica.md`.

**Os 14 blocos do ramo de venda** (o peso e a ordem mudam por arquitetura, nenhum some): hero · vídeo quando aplica · para quem é e para quem não é · o problema (dor de terceira camada) · mecanismo do problema · apresentação do método · prova social · o produto por dentro · bônus · oferta e empilhamento · garantia · sobre o autor · perguntas frequentes · botão final.

**Duas regras do bench que valem em todo tipo:**
- **A fricção do formulário casa com a temperatura e o ticket.** Um campo na captura fria, formulário longo de qualificação no ticket alto. A fricção é alavanca, não defeito.
- **Botão atrasado é assinatura de vídeo longo e de aplicação.** Ele aparece no momento do convite, não no topo.

**Antes de fechar a ação, rode a auditoria de 5 movimentos** (sonhos incentivados com cena e número · falhas justificadas sem condescendência · medos nomeados e dissolvidos com mecanismo · desconfianças confirmadas com verdade dura · inimigo-categoria nomeado sem ataque pessoal), descrita em `references/processo-landingpage.md`. É pré-filtro: movimento ausente, reforça antes do gate. O veredito final é do gate.

**Regras invioláveis enquanto escreve:** zero menu de navegação · uma promessa na página inteira · prova nunca é só elogio (nome mais nicho mais resultado com número e prazo), e uma prova real acima da dobra · botão com verbo de posse e, embaixo, micro-garantia só com dado do insumo (sem dado, a linha sai) · um destino de clique · bônus mata objeção nomeada, não é recheio · garantia é vendida, com headline própria · escassez, vagas, prazo, lote e preço riscado só com motivo e dado do insumo, e preço riscado só se o insumo diz que aquele valor já foi cobrado · cada bloco cabe em 1 tela de celular · mostra resultado e função, nunca o passo a passo executável · uma ideia por frase, número no lugar de adjetivo, vocabulário do cliente final.

---

## Ação 5 · O GATE (roda por dentro, em cada bloco, e não imprime)

**Títulos da página.** Escreva pela régua de escrita (`shared-references/crivo/06-regua-de-escrita.md`). Título de bloco pode ser rótulo de função ("o que você vai descobrir", "é pra você se", "quem conduz"): as páginas validadas usam assim e o leitor acha o bloco pelo rótulo. A régua de títulos 07, o `checar_titulos.py` e a pasta `conferencia/` não valem nesta skill.

**Hero, conferido:** `hero tem o resultado da aula? sim/não · tem "mesmo que/sem" quando o insumo lista objeção? sim/não · é o nome do evento com prefixo ("Aula ao vivo:")? sim reprova`.

**Bastidor fica fora da página.** A página e o obrigado levam só o que o visitante lê. Nome de regra, de arquivo, de script, contagem, inventário, origem de número, instrução ao dono ("confirme", "valide", "antes de publicar"), pergunta e pendência vão pro `_notas-operador.md`. No HTML não existe marcador visível: a frase que depende de dado que falta sai inteira, e o link que falta fica só no atributo, marcado `#CONECTAR-...`. O `conferir_fontes.py` reprova `{{` que sobrou e `[DO DONO` ou `[A CONFIRMAR` visível.

**A peça não explica a própria conduta.** Frase que descreve o que a página faz ou deixa de fazer ("a aula mostra a lógica sem prescrever treino individual", "sem transformar orientação em promessa", "apresenta a lógica do método") é nota de método e vai pro `_notas-operador.md`. No lugar dela entra a cena: o que a leitora vai conseguir fazer depois, dita em concreto. A leitora não contratou a explicação da sua conduta, ela veio pelo ganho. Checagem: `grep -nE 'sem prescrever|sem transformar|sem garantir|apresenta a lógica' <peça>` volta vazio.

**Marcador no `.md` só em posição de campo.** `[DO DONO: x]` e `[A CONFIRMAR: x]` entram na copy só onde a frase existiria sem o dado (um link, uma data, um valor no fim da linha). No miolo de uma frase, reescreva a frase sem o dado ou pergunte antes. Antes de marcar qualquer número, grepe os insumos (`grep -in '<termo>' <insumos>`): dado que existe no disco nunca vira marcador.

**Nome de pessoa real em copy pública.** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Conferência do insumo, sim ou não (no `_notas-operador.md`).** `o dono declarou o objetivo de conversão (no pedido ou no insumo)? aparece na página e no obrigado? · o insumo lista objeções? entraram no hero ou no "é/não é"? · lista quem não é o público? entrou? · traz prova com número? está nas 5 primeiras linhas? · traz data, sessões, duração, formato? estão na primeira tela? · traz preço, lote, garantia, bônus? entraram com o valor do insumo?` Cada `não` entra na página ou ganha o motivo da exclusão em meia linha.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no `_notas-operador.md`. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Número com o mesmo rótulo e a mesma causa.** O `conferir_fontes.py` acha o número no insumo, mas não o rótulo. Confira um por linha no `_notas-operador.md`: `<número> | origem: <arquivo, linha> | mesmo rótulo (verbo, objeto, "mais de")? sim/não | liga a uma causa que o insumo não liga? sim/não`. "Gerenciou" não vira "em anúncio"; "420 alunos" não vira "420 dentistas"; faturamento não ganha "num único webinário". Um `não` no rótulo ou um `sim` na causa reescreve a frase com a palavra do insumo.


**O que faz:** reprova o bloco que não serve, antes de o dono ver. Serve também como modo auditoria, quando o dono cola uma página pronta e pede diagnóstico.

**Precisa de:** o bloco escrito.

**Sem o insumo:** o gate sempre tem o que precisa.

**Entrega:** em modo normal, a tabela **nunca** vai pra página; o `_notas-operador.md` leva 3 a 6 linhas do que o gate conferiu (a fala real que sustentou a promessa, o pior bloco e por quê, o que foi reescrito, o que ficou pendente). Em modo auditoria de página existente, entrega `diagnostico-pagina.md` com o bloco, o check que falhou e a correção.

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

Com shell disponível, rode o lint de copy em `scripts/lint_copy.py` sobre cada `.md`. Sem shell, faça a busca manual pelos dois bloqueios duros antes de marcar o anti-IA. O lint lê o arquivo inteiro, inclusive o `_notas-operador.md`: escreva as notas com o mesmo cuidado da copy.

**Conferência de estrutura (sim ou não, colada no `_notas-operador.md`; qualquer não volta pro bloco):**
1. Hero com o resultado da aula, e "mesmo que/sem" quando o insumo tem objeção?
2. Data e hora, ou o seletor como primeiro campo com horário do insumo (sem horário, sem seletor), na primeira tela?
3. Número de autoridade nas 5 primeiras linhas?
4. Página longa: formulário na primeira tela (grátis) ou no fim depois da oferta (pago)?
5. Micro-garantia, selo, formato, confirmação e rodapé só com dado do insumo, e sem dado o elemento sumiu? Cada número com o rótulo do insumo?
6. Um destino de clique só, botão com verbo de posse, barra fixa no celular apontando pro mesmo lugar?
7. Longa: "é pra você / não é" com o que o insumo traz?
8. Cada promessa de entrega (canal, lembrete, link, bônus, prazo) com linha do insumo?
9. Obrigado: data repetida, um botão só (agenda com todas as datas do evento, ou sem agenda), compromisso, o que preparar e o objetivo de conversão do dono?
10. Celular: captura em 390px (ou leitura do HTML) com hero e botão antes de rolar, nada vazando na lateral?

---

## Ação 6 · FECHO (congruência e entrega)

**O que faz:** confere a congruência da página inteira e fecha a entrega.

**Entrega:** no modo direto, a pasta completa (Ação 7) e o relato do "pronto". No modo guiado, só o bloco, sem tabela de gate, com a pergunta "esse bloco te serve? sigo pro próximo?", e **espera o OK**.

No fim da página, confira: ela repete UMA promessa e aponta pra UM destino, do primeiro bloco ao último.

---

## Ação 7 · RENDER (a página pronta em HTML)

**O que faz:** transforma a copy em `pagina.html` e `obrigado.html` a partir do template `assets/landing-base.html` (arquivo único, CSS embutido, sem dependência externa, feito primeiro pro celular, sem menu) e diz o que conectar.

**Precisa de:** a copy aprovada no `.md` · o molde · a identidade visual do perfil/brain do dono (sem ela, o padrão neutro do template).

**Sem o insumo:** sem identidade, padrão neutro e uma linha no `_notas-operador.md`. Sem link de formulário, checkout ou grupo, o atributo fica `#CONECTAR-...` e o script do template segura o envio. Sem foto, o bloco de foto sai. Token sem dado do insumo: o elemento sai inteiro (o `<p>`, o `<li>`, o bloco) e vira pergunta; nunca frase padrão.

**Entrega:** `pagina.html` · `obrigado.html` · `pagina-<slug>.md` · `_notas-operador.md` com `O que conectar` (formulário e redirecionamento pro obrigado, WhatsApp ou grupo, checkout, pixel, onde hospedar). Nada é publicado.

**Leia primeiro:** `references/render-html.md` (passo a passo, identidade, piso do celular, quebra de linha, agenda, conferência de tela).

**Profundidade:** `shared-references/filtro-mobile-first/` (`checklist-final.md`, `ctas.md`, `contraste-e-cor.md`).

**Passos:** copia o template duas vezes → apaga a página que não é e os blocos que o molde não pede → troca cada `{{TOKEN}}` com Python → variáveis de cor e fonte → `conferir_fontes.py` com exit 0 → captura em 390px e 1280px quando houver navegador → conferência de estrutura → relato.

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
| O webinar inteiro (aula, oferta, mensagens, chat) | **soft-webinar** | a página de inscrição, o obrigado e a venda do ingresso eu faço inteiros aqui |
| A página do mini-webinar | **soft-funil-miniwebinar** | monto pela receita de entrega de isca com vídeo |
| Posicionamento, oferta, nomear mecanismo | **soft-plano-posicionamento** | uso o briefing crítico da Ação 1 |
| Script de venda, objeção, prospecção | **soft-vendas-closer** / **soft-vendas-sdr** | não faço |
| Arte de anúncio, carrossel, PNG | **soft-designer** | a página em HTML é daqui (Ação 7); arte de anúncio e carrossel não faço |

## Anti-patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| No modo guiado, despejou a página inteira de uma vez | Volta: tipo, outline, um bloco por vez com gate |
| Entregou só o `.md` quando o dono pediu a página | Ação 7: `pagina.html` e `obrigado.html` prontos, mais o que conectar |
| Página curta pra tráfego frio, ou tamanho justificado pela receita | Ação 2.B: o tráfego e o evento decidem |
| Hero com tese ou inimigo no lugar do resultado da aula | Molde do hero em `references/moldes-evento.md` |
| Prova de autoridade só no terceiro bloco | Número nas 5 primeiras linhas, logo sob a headline |
| Canal, lembrete, micro-garantia, selo ou formato completados por padrão ou pelo exemplo | Só com linha do insumo; sem ela, o elemento sai e vira pergunta no `_notas-operador.md` |
| Bastidor (contagem, nome de regra, pergunta ao dono) dentro da página | Tudo pro `_notas-operador.md` |
| Aplicou os 14 blocos de venda numa página de captura | Usa a receita enxuta DO TIPO (captura tem 4 a 5 blocos) |
| Duas promessas competindo | Corta a segunda |
| Vários botões pra destinos diferentes | Um botão dominante, um destino, repetido nos picos |
| Pôs depoimento antes da promessa | Prova sempre depois da promessa |
| Inventou depoimento ou número plausível | Só prova real. Sem fonte, `[A CONFIRMAR: prova]` |
| Copy tentando agradar todo mundo | Filtra na entrada: para quem é e para quem não é |
| Promessa redonda ("dobre seu faturamento") | Número específico e calculável da prova real |
| Cronômetro falso em replay | Escassez real com janela que expira, ou silêncio |
| Página de obrigado sem saída, ou com dois botões | Um próximo passo, com data repetida, compromisso e o que preparar |
| Quiz que pede o contato depois do resultado | Contato antes do resultado, senão não captura |
| Link na bio com 12 links iguais | Máximo 8, hierarquia de intenção em 3 camadas |
| Oferta pós-compra sem o "não, obrigado" discreto | Sim de 1 clique em destaque, recusa pequena embaixo |
| Solução genérica sem mecanismo nomeado | Nomeia o mecanismo |
| Narrou o fluxo ("agora vou auditar") | Executa em silêncio e entrega o bloco limpo |
| Imprimiu a tabela do gate | O gate é interno |

## Transversais

`references/moldes-evento.md` (os 3 moldes do evento, o hero, o obrigado e a escassez) · `references/render-html.md` (a página em HTML) · `assets/landing-base.html` (o template) · `references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/tipos-de-landing.md` (tipos e receitas) · `references/frameworks-copy.md` · `references/mecanicas-assinatura.md` (mecânica de cada tipo) · `references/arquiteturas.md` (as 4 do ramo de venda) · `references/processo-landingpage.md` (14 blocos e auditoria) · `references/blocos-copy.md` · `references/vsl-script.md` (o roteiro do vídeo na página) · `references/conducao-na-pratica.md` · `shared-references/operacao-padrao.md`, `crivo/`, `filtro-anti-ia/`, `filtro-mobile-first/` · `scripts/conferir_fontes.py` · `scripts/lint_copy.py`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** `pagina.html` e `obrigado.html` pras páginas; a copy em slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `pagina-aula-bolo-de-pote.md`); o bastidor em `_notas-operador.md`.
- **Lint:** `python3 scripts/lint_copy.py <arquivo>` em cada `.md` gravado, o `_notas-operador.md` incluso, e só declare o gate aprovado com exit 0 em cada um. Cole no `_notas-operador.md` uma linha por arquivo, `<arquivo>: exit N`, e feche com `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`. O `_notas-operador.md` é escrito por último e é o que mais reprova: rode o lint nele depois de terminar. O texto do HTML é o mesmo do `.md`; confira nele o travessão longo com `grep -cP '\x{2014}' pagina.html obrigado.html` (tem que dar 0).
- **Arquivo aberto de volta:** abra cada `.md` gravado e confira a primeira linha, a última e uma do meio (cabeçalho, tabela e lista válidos).
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
