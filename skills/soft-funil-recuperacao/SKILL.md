---
name: soft-funil-recuperacao
description: >-
  Escreve a RÉGUA DE RECUPERAÇÃO DE VENDA, o resgate de quem chegou ao checkout, gerou o Pix, abandonou o carrinho ou teve o cartão recusado e NÃO comprou. Entrega a régua nos 3 canais (e-mail, SMS e WhatsApp), cada mensagem com o timing por evento e a função no arco de recuperação. Use quando o pedido for: "recuperar venda", "carrinho abandonado", "checkout abandonado", "Pix não pago", "Pix gerado", "cartão recusado", "resgatar quem não comprou", "régua de recuperação", "sequência de recuperação", "e-mail/SMS/WhatsApp de recuperação". NÃO use pra: a régua pós-isca que aquece o lead FRIO que ainda não demonstrou intenção de compra (soft-funil-nutricao); o upsell ou a oferta pós-compra APROVADA (soft-funil-upsell); a carta de vendas ou a VSL que apresenta a oferta (soft-funil-carta); a página de vendas (soft-funil-landing); o lançamento com carrinho aberto (soft-launch); carrossel, reel, headline solta (soft-conteudo-*); webinar (soft-webinar). Leia e siga o fluxo inteiro do SKILL.md.
---

# Régua de recuperação, o resgate da venda perdida no checkout

A pessoa já quis comprar. Ela gerou o Pix, digitou o cartão, chegou ao checkout e parou a um passo. Não é um lead frio que precisa ser aquecido: é um comprador quase feito que empacou por preço, por medo, por distração ou por um cartão que não passou. A régua de recuperação vai buscar essa venda de volta, nos 3 canais onde a pessoa ainda pode ser alcançada (e-mail, SMS e WhatsApp), com cada mensagem no timing certo do evento e com uma função clara no arco. Régua que dispara a mesma mensagem 7 vezes cansa e queima o contato; régua boa escala a urgência e a prova a cada toque, e para na hora certa.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Assunto de e-mail nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Cada mensagem da régua carrega, declarada, o timing e a função.** Toda mensagem que sai tem duas coisas escritas ao lado: o gatilho de disparo com o tempo desde o evento (`10 min após o Pix gerado`) e a função no arco (`reconhecimento`, `prova`, `dor perigosa`, `objeção`). Mensagem sem timing declarado ou sem função declarada reprova. Cole `mensagens na régua: N · com timing declarado: N · com função declarada: N`, os três iguais.

**Desconto e preço promocional NÃO se inventam, saem só do que o dono deu.** As fontes deste tema usam um preço promocional caindo a cada toque (de 29 pra 19 pra 9) e um cupom de última chance. Isso é uma TÁTICA, não um número: o valor do desconto, o preço de virada e o piso só entram se o dono os forneceu no perfil ou no insumo. Antes de escrever qualquer toque com preço ou cupom, rode `grep -rniE 'desconto|cupom|R\$|promo|preço|preco' <insumos> <perfil>` e cole a saída. Sem o número no disco, o toque sai na forma que dispensa o valor ("uma condição especial pra fechar hoje", com o campo `[A CONFIRMAR: valor do desconto]` no handoff) e a pergunta vai pro dono. Inventar um "de 29 por 9" plausível reprova a entrega. Cole `toques com preço ou desconto: N · com número do disco: N · inventados: 0`.

**Zero promessa que a oferta não cumpre.** A régua só repete o que a oferta real entrega: garantia, prazo de acesso, bônus, formas de pagamento. Antes de prometer garantia de 30 dias, acesso imediato, bônus ou "mais de mil pessoas", rode `grep -rniE 'garantia|bônus|bonus|acesso|reembolso|<cada número de prova>' <insumos> <perfil>` e cole a saída. Número de prova sem lastro no disco vira `[A CONFIRMAR: número]` e sai da mensagem, com ou sem ressalva ao lado. Cole `provas e promessas na régua: N · com lastro no disco: N · sem lastro: 0`.

**A fronteira que não pode vazar:** esta régua fala com quem JÁ demonstrou intenção de compra (gerou Pix, abandonou o checkout, teve o cartão recusado). Ela não aquece o lead frio que baixou a isca e ainda não quis comprar, isso é a **soft-funil-nutricao**; e não faz o upsell de quem já pagou, isso é a **soft-funil-upsell**. Régua de recuperação que começa a educar do zero, como se a pessoa nunca tivesse ouvido falar da oferta, perdeu o ponto: ela parou NO checkout, não antes dele.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra o fluxo inteiro num caso ancorado (a Renata, do Protocolo Base 40): o briefing respondido, o gatilho de evento escolhido, a régua nos 3 canais com timing e função de cada toque, um trecho de cada canal escrito e o que o gate reprovou. `references/reguas-por-canal.md` traz o arco de toques detalhado dos 3 canais, com a cadência, o teto de tamanho e a função de cada toque.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta régua eu já faço no modo direto (você me diz a oferta, o gatilho de evento e o que a pessoa vê no checkout, e eu escrevo a sequência nos 3 canais). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou. Se faltar um insumo que a régua não vive sem (a oferta, o gatilho de evento, o canal), pergunta AQUELE insumo e segue, sem voltar pro briefing inteiro.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o briefing curto uma pergunta de cada vez, e monta a régua com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda a régua (qual gatilho de evento, quantos toques, a cadência, se entra desconto), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a calibrar sozinho na próxima. Exemplo do tom: "Pus o SMS de 5 minutos primeiro porque o Pix vence rápido e o SMS chega na hora; o e-mail entra em paralelo pra quem lê e-mail, não em vez do SMS."

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("o público de sempre", "quero recuperar a venda"), não segue com o genérico. Pede o concreto que só o dono tem: a dor literal que segura a compra, a objeção real que aparece no checkout, o número de prova documentável. Verbatim real vira a âncora dos toques de dor e prova; resposta rasa vira régua rasa. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar a régua, fecha com UMA linha: "Quer mais agressiva? Menos toques? Só um canal? Tirar o desconto? Me diz o que ajustar que eu refaço só essa parte." A oferta de refino não substitui o STOP nem o gate.

## Contrato de saída (o que sai, e onde cai)

- **Um arquivo `.md` nomeado**, salvo no disco: `regua-recuperacao-<produto>.md`. Se o ambiente renderizar markdown, mostre também.
- **A régua sai por CANAL e por GATILHO de evento.** O documento traz uma seção por canal (e-mail, SMS, WhatsApp) e, dentro de cada canal, a sequência por gatilho (Pix gerado, checkout abandonado, cartão recusado). Cada toque tem o timer, a copy e a função.
- **Preço e desconto na régua são decisão declarada, não default silencioso.** O preço da oferta entra quando o perfil traz. O desconto de recuperação só entra com o número do dono; sem ele, o toque usa a forma sem valor e leva a pergunta ao handoff.
- **Entrega etapa por etapa**, com parada pro OK a cada uma. Nunca despeja a régua inteira dos 3 canais de primeira.
- **Nunca inventa desconto, número de prova, garantia ou bônus.** Sem lastro real, o dado sai como `[A CONFIRMAR: o quê]` e a peça não sai como pronta.
- **A régua é arquivo publicável e não tem seção de bastidor, nem marcada.** Pendência, valor de desconto a confirmar, link de checkout e decisão editorial vão em `notas-confirmacao.md`, entregue ao lado. Checagem antes de fechar: `grep -nE '^#+.*(dono|não publicar|nao publicar|bastidor)' <regua>` tem que voltar vazio.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "régua de recuperação", "recuperar venda", sem dizer o canal | **1 · BRIEFING**, depois **2 · CALIBRAGEM** (os 3 canais) |
| "e-mail de carrinho abandonado", "sequência de e-mail" | **2** no ramo do e-mail, depois **3** |
| "SMS de Pix não pago", "SMS de recuperação" | **2** no ramo do SMS, depois **3** |
| "bot de WhatsApp de recuperação", "fluxo de WhatsApp" | **2** no ramo do WhatsApp, depois **3** |
| "olha essa régua aqui e diz o que está errado" | **5 · GATE** em modo auditoria, devolve o diagnóstico por toque |

Pedido ambíguo ("preciso recuperar quem não comprou"): pergunte UMA coisa só, **"qual foi o evento: a pessoa gerou o Pix, abandonou o checkout ou teve o cartão recusado?"**, porque cada gatilho tem timing próprio.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de oferta, avatar, mecanismo nomeado, voz, preço ou prova: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta do "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

**As 6 leis de operação** (detalhe em `shared-references/operacao-padrao.md`, Seção 0): (1) cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**; (6) **doc de saída enxuto pros 2 leitores**, zero meta-narração.

---

## Ação 0 · ANCORAGEM (roda antes de tudo, não pula)

**O que faz:** abre a fonte de fala real e puxa a matéria-prima da dor que segura a compra e da prova que a solta.

**Precisa de:** a fonte, nesta ordem: descrição do projeto → posicionamento do dono → mensagens anteriores. De lá saem **3 a 5 falas de DOR** (o que faz a pessoa hesitar no checkout) e **3 a 5 de PROVA/DESEJO** (o que a solta), literais, com o N. Os toques de dor e de prova nascem delas.

**Sem o insumo:** três estados, declare o seu em 1 linha.
- **Tem fala real com N:** ancora nela e cita o N.
- **Tem nicho e prova, zero fala literal:** não invente. Ancore em prova real do dono. Número não confirmado vira `[A CONFIRMAR: número]`.
- **Sem nada:** pergunte numa mensagem só (nicho em 1 linha, 1 dor real que segura a compra, o preço da oferta) e siga.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data, preço ou desconto e etiquetar.

**Entrega:** nada de arquivo. É a matéria-prima das ações 3 e 4.

**Leia primeiro:** `shared-references/crivo/01-entrada-verbatim.md`.

---

## Ação 1 · BRIEFING (num bloco só, e espera resposta)

**O que faz:** junta o insumo que sustenta a régua.

**Precisa de:** os campos base. Se veio do posicionamento com os dados, confirme em 1 linha e pule.

**Os campos base:**
- **(a)** a oferta e o preço (o produto que a pessoa ia comprar, com o valor do checkout)
- **(b)** o gatilho de evento: **Pix gerado**, **checkout abandonado** ou **cartão recusado** (cada um tem timing próprio; o dono pode querer os três)
- **(c)** o que a pessoa vê no checkout (formas de pagamento, garantia, prazo de acesso, bônus) e o link/canal de retomada
- **(d)** a dor avançada que segura a compra, nas palavras do cliente, e a objeção real (preço, medo, dúvida)
- **(e)** 1 a 3 provas reais (número, caso, prazo, só verdade documentável)
- **(f)** o desconto de recuperação, SE o dono topa dar um: o valor, o preço de virada e o piso (sem isso a régua não usa desconto, e diz isso)

**Sem o insumo:** sem (a), (b) e (c) a régua não avança. **PARA e espera.** Faltando (d) ou (e), os toques de dor e prova saem mais fracos e você diz isso em 1 linha. Faltando (f), a régua roda SEM desconto, só com urgência e prova; nunca invente um desconto plausível.

**Entrega:** nada de arquivo. É o que alimenta a calibragem.

**Leia primeiro:** `references/reguas-por-canal.md`, Seção 1 (o arco de toques por canal).

---

## Ação 2 · CALIBRAGEM (canais, gatilhos, cadência)

**O que faz:** declara, numa linha só, tudo que decide a régua.

**Precisa de:** o briefing da Ação 1 · quais canais o dono tem ligados (e-mail, SMS, WhatsApp) · qual gatilho de evento cobrir.

**Sem o insumo:** sem saber os canais ligados, **assuma os 3** e declare a premissa em 1 linha (a régua sai completa e o dono liga só os que usa). Sem o gatilho declarado, **PARA e pergunte só isso**: "a pessoa gerou o Pix, abandonou o checkout ou teve o cartão recusado?".

**Entrega:** 1 linha declarada antes de escrever: `canais X → gatilho(s) Y → nº de toques por canal Z → desconto: sim/não`. **STOP.**

**Leia primeiro:** `references/reguas-por-canal.md`, Seções 2, 3 e 4 (o detalhe de cada canal).

### 2.1 · Os 3 canais, cada um com uma lógica

Não são fases, são canais paralelos que rodam juntos. A pessoa pode estar em todos ao mesmo tempo.

| Canal | Ritmo | Tamanho | Função no conjunto |
|---|---|---|---|
| **E-mail** | cadência de 10 min a 72 h, até 7 toques | corpo completo, com prova e FAQ | o arco longo que escala urgência e prova |
| **SMS** | agressivo, de minutos a horas | curtíssimo, SEM acento, 1 linha | o toque que chega na hora, pro Pix que vence |
| **WhatsApp (bot)** | core de 2 a 3 mensagens, escala se performar | médio, com botões (aceitar/recusar) | a conversa com resposta e desconto progressivo |

### 2.2 · Cada gatilho de evento tem timing próprio

| Gatilho | Urgência | Primeiro toque | Por quê |
|---|---|---|---|
| **Pix gerado** | máxima | SMS em 5 min | o Pix vence rápido (minutos); o resgate tem que chegar antes do vencimento |
| **Checkout abandonado** | alta | SMS em 7 min, e-mail em 10 min | a pessoa saiu com a intenção fresca; quanto antes, maior a chance |
| **Cartão recusado** | alta | SMS em 2 min | quase sempre é um problema técnico (limite, dado errado), não uma desistência; o toque tira o atrito |

**Regra da cadência:** o SMS abre porque chega na hora; o e-mail roda em paralelo pra quem lê e-mail; o WhatsApp entra com a conversa e os botões. Nenhum canal substitui o outro, e o mesmo toque não sai idêntico nos três.

---

## Ação 3 · ESPINHA (o arco de toques, ainda em bastidor)

**O que faz:** monta o arco de cada canal, toque a toque, com o timer e a função, antes de escrever a copy.

**Precisa de:** o briefing, a linha declarada da Ação 2 e as falas da Ação 0.

**Sem o insumo:** sem o desconto (item f), a espinha marca os toques de desconto como toques de urgência e prova, e você diz isso em 1 linha.

**Entrega:** a espinha por canal, uma tabela de toques com timer e função, mostrada pro dono. **STOP.**

**Leia primeiro:** `references/reguas-por-canal.md` (o arco completo dos 3 canais).

**O arco de funções (vale nos 3 canais, o e-mail é o mais completo):**

| Toque | Função | O que faz |
|---|---|---|
| **1** | neutro | avisa que falta um passo, sem pressão; lembra as formas de pagamento e a garantia |
| **2** | reconhecimento | parabeniza pela decisão, reduz o atrito, oferece ajuda no canal |
| **3** | prova | mostra que outros como ela resolveram; traz a objeção real e a resposta |
| **4** | benefício | lista o que a pessoa desbloqueia ao concluir |
| **5** | dor | reconecta com a dor que fez ela chegar ao checkout |
| **6** | dor perigosa | mostra o custo de não resolver, com respeito, sem terror |
| **7** | objeção / FAQ | responde as perguntas que seguram a compra (funciona? é fácil? em quanto tempo? e se não der certo?) |

**A prova entra por resultado, não por tempo de casa.** Cada toque de prova carrega o resultado concreto de alguém (o que mudou, em quanto tempo), nunca um "anos de mercado". Número sem lastro vira `[A CONFIRMAR: prova]`.

**O desconto, quando existe, escala com respeito.** Nas fontes o preço cai a cada toque. Isso só entra com o número do dono, e a queda é declarada no handoff, nunca inventada. Sem desconto, esses toques viram urgência honesta e prova nova.

---

## Ação 4 · REDAÇÃO (a régua final)

**O que faz:** transforma a espinha na régua pronta pra colar na ferramenta de disparo.

**Precisa de:** a espinha aprovada na Ação 3.

**Sem o insumo:** não há redação sem espinha aprovada.

**Entrega:** `regua-recuperacao-<produto>.md`, salvo no disco, com uma seção por canal e, dentro, a sequência por gatilho. Se o ambiente renderizar markdown, mostre também. **STOP.**

**Arquivos obrigatórios: o arquivo acima, e `conferencia/checagem-titulos.md` por último** (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`). Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/reguas-por-canal.md` (a copy de cada toque, por canal) · `references/EXEMPLO-FIM-A-FIM.md` (o caso completo).

### No ramo do E-MAIL

Cada toque tem assunto, pré-cabeçalho e corpo. O assunto nasce da régua de títulos, com gatilho nomeado, nunca em caixa alta. O corpo é curto, escaneável no celular, com um único botão e o link de retomada como campo (`[LINK]` no fim da linha, substituível por colagem). O toque final é o FAQ que responde as objeções.

### No ramo do SMS

Curtíssimo, **SEM acento** (o SMS quebra acento em muito aparelho), uma linha, com o nome no início e o link no fim como campo. Nada de parágrafo. O timing é o mais apertado dos três, porque o Pix vence.

### No ramo do WhatsApp (bot)

Mensagem com corpo médio, botão de aceitar e botão de recusar (cada botão respeita o teto de caracteres da ferramenta), footer que oferece cancelar. O core são as 2 a 3 primeiras mensagens; as demais só entram se as primeiras performarem, e você diz isso em 1 linha. O rodapé de segurança e garantia entra quando o dono os confirma.

**Densidade nos 3 canais:** cada linha carrega função. Corta o que não empurra pra concluir a compra.

---

## Ação 5 · O GATE (roda por dentro, e não imprime)

**Régua de títulos (vale em todo assunto de e-mail, headline de WhatsApp e nome de toque que vai ao público).** Todo assunto e toda headline passam pela régua de títulos (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`.** Fecha com `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`, os dois primeiros iguais. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Cada mensagem tem timing e função declarados.** Cole `mensagens na régua: N · com timing declarado: N · com função declarada: N`, os três iguais. Mensagem sem uma das duas reprova.

**Desconto e preço só do que o dono deu.** Rode `grep -rniE 'desconto|cupom|R\$|promo|preço|preco' <insumos> <perfil>` e cole a saída. Todo valor na régua tem que aparecer nela. Valor sem origem no disco reprova. Cole `toques com preço ou desconto: N · com número do disco: N · inventados: 0`.

**Zero promessa inventada.** Garantia, prazo, bônus e número de prova só entram com lastro no disco. Cole `provas e promessas na régua: N · com lastro no disco: N · sem lastro: 0`.

**Marcador nunca no miolo da fala.** `[A CONFIRMAR: x]` só entra em posição de CAMPO (link, valor, data, no fim da linha, substituível por colagem). No miolo de uma frase que perde o sentido sem o valor, reprova: escreva a versão que dispensa o dado ou pergunte ao dono antes. Cole `marcadores na régua: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública.** Nome, caso ou frase vindos de mensagem privada, caixa de entrada ou call NUNCA entram sem autorização registrada pelo dono (`autorizado por <dono> em <data>` no insumo). Sem isso, anonimiza ou não usa. A checagem é COMANDO (`shared-references/crivo/08-consentimento.md`): rode `grep -nwF '<nome>' <regua>` por nome e cole a saída. Feche com `nomes de pessoa na régua: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`.

**Uso completo do que o dono deu.** Todo dado que o dono forneceu e cabe na régua aparece nela ou tem o motivo da exclusão declarado. Liste um por linha, `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0`. O piso é CONTADO: `grep -c '^- ' <perfil>` e a saída literal ao lado.

**Proveniência de terceiro.** Nome de empresa, pessoa, domínio, telefone ou endereço de terceiro só entra se veio do dono, do insumo dele, ou de busca executada neste turno com o comando registrado. Sem isso, sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte.

**O que faz:** reprova a régua que não serve, antes de o dono ver. Serve também como modo auditoria, quando o dono cola uma régua pronta.

**Precisa de:** a régua escrita.

**Entrega:** nada em modo normal (auditoria silenciosa, a tabela nunca vai pra saída). Em modo auditoria, entrega `diagnostico-regua.md` com o canal, o toque, o check que falhou e a correção.

**Leia primeiro:** `shared-references/crivo/03-gate-cub.md`.

| Check | Passa se |
|---|---|
| **Ancorada** | os toques de dor e prova nascem de fala literal da fonte (cita o N real) ou de prova real do dono. N inventado reprova na hora |
| **Timing por evento** | cada toque tem o gatilho e o tempo desde o evento; o SMS de Pix abre em minutos, não em horas |
| **Função declarada** | cada toque tem uma função clara no arco (neutro, reconhecimento, prova, benefício, dor, dor perigosa, objeção); dois toques idênticos reprovam |
| **Intenção respeitada** | a régua fala com quem já quis comprar; ela não educa do zero como pra lead frio |
| **Desconto real** | todo preço e desconto tem origem no disco. Valor inventado reprova |
| **Promessa real** | garantia, bônus, prazo e número de prova têm lastro no disco. Sem lastro, `[A CONFIRMAR]` e sai da mensagem |
| **Um convite por toque** | cada toque leva a UMA ação (concluir a compra, ou responder), nunca a duas |
| **SMS sem acento** | os toques de SMS não têm acento e cabem em 1 linha |
| **C/U/B** | não Confuso, não Inacreditável (promessa menor mais prova), não Boring (cada linha empurra pra concluir) |
| **Anti-IA (duro)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz · sem frase-emoldura · sem antítese-molde de IA |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ refaz. Só tudo ✓ vai pro dono |

Com shell disponível, rode o lint de copy em `scripts/lint_copy.py` sobre o arquivo. Sem shell, faça a busca manual pelos dois bloqueios duros antes de marcar o anti-IA.

---

## Ação 6 · FECHO (mostra e para)

**O que faz:** entrega a régua limpa e o comentário de configuração.

**Entrega:** só a régua (ou a etapa pronta), sem tabela de gate, sem meta, mais uma linha sobre como configurar (em que ferramenta de disparo colar cada canal, onde ligar o link de retomada). Pergunta "essa te serve? ajusto?" e **espera o OK** antes de seguir pra próxima etapa ou variação.

**Prova ou desconto descartado se declara na própria régua.** Se um caso, número ou desconto REAL do dono existia e ficou de fora, declare em 1 linha na própria entrega por quê. Cautela sua, não pedida pelo dono, é motivo válido, e é exatamente o que ele precisa ler pra discordar.

---

## O que esta skill NÃO faz

Cada rota é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Aquecer o lead FRIO pós-isca, que ainda não quis comprar | **soft-funil-nutricao** | não faço: aqui a pessoa já demonstrou intenção no checkout |
| Upsell ou oferta pós-compra APROVADA | **soft-funil-upsell** | não faço: aqui a pessoa NÃO comprou ainda |
| A carta de vendas ou a VSL que apresenta a oferta | **soft-funil-carta** | não faço: a régua resgata quem já viu a oferta, não a escreve |
| Página de vendas com hero, seções e botão | **soft-funil-landing** | não faço |
| Lançamento com carrinho aberto e fechamento | **soft-launch** | não faço |
| Carrossel, reel, stories, headline solta | **soft-conteudo-*** | escrevo o assunto e a headline dos toques, e mais nada |
| Arte, visual, PNG | **soft-designer** | entrego o `.md` da régua, sem o visual |

## Anti-patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Despejou os 3 canais de primeira | Volta: briefing, espinha, régua, parando a cada etapa |
| Educou do zero, como pra lead frio | Reescreve: a pessoa parou NO checkout, ela já conhece a oferta |
| Inventou um "de 29 por 9" que o dono não deu | Só desconto real. Sem número no disco, usa a forma sem valor e pergunta |
| Prometeu garantia ou bônus que a oferta não tem | Só o que a oferta entrega. Sem lastro, `[A CONFIRMAR]` e sai |
| SMS de Pix disparando em horas | O Pix vence em minutos; o SMS abre em 5 min |
| SMS com acento e 3 linhas | Sem acento, 1 linha, nome no início e link no fim |
| Mesmo texto nos 7 toques | Cada toque tem função própria: neutro, prova, dor, objeção |
| Dois convites num toque | Um convite por toque: concluir a compra, ou responder |
| Imprimiu a tabela do gate | O gate é interno |
| Narrou o fluxo ("agora vou escrever o SMS") | Executa em silêncio e entrega o resultado |

## Transversais

`references/reguas-por-canal.md` (o arco de toques dos 3 canais, com cadência e função) · `references/EXEMPLO-FIM-A-FIM.md` (o caso da Renata, do começo ao fim) · `shared-references/operacao-padrao.md`, `crivo/` · `scripts/lint_copy.py` · `scripts/checar_titulos.py`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `regua-recuperacao-protocolo-base-40.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas inclusos, e só declare o gate aprovado depois de exit 0 em cada um. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** A lista fecha com o total: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`. O `RELATO.md` entra na varredura como qualquer outro arquivo; rode o lint nele por último, depois de escrevê-lo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill; vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
