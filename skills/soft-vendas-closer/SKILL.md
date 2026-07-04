---
name: soft-vendas-closer
description: O CLOSER do método Soft, a frente que CONDUZ e FECHA o lead que já chegou quente. Faz a metade de baixo da venda e contém TUDO do tema, a espinha das 7 fases, o fechamento na DM/WhatsApp (canal default do 1:1), o banco de objeções, o script por canal, o copiloto em tempo real, a análise de conversa, a Conta de Padaria + a coleta de sinal/Pix na hora, a mentalidade do vendedor, o pós-venda (indicação, testemunho, troca bônus-por-prova). Recebe o lead qualificado do SDR (com contexto) OU direto do funil; puxa a Oferta/PUV do Plano. Use SEMPRE que envolver "script de venda", "conduzir/fechar a venda", "objeção", "tá caro/vou pensar", "pedir o sim", "coletar o Pix/sinal", "follow-up", "copiloto", "analisa essa conversa", "não consigo cobrar caro", "pós-venda", "indicação", "testemunho". NÃO use pra ABRIR/qualificar/agendar lead frio, prospecção na DM, SDR, CRM (soft-vendas-sdr); contrato (soft-contratos-consultoria); carta/VSL/landing (soft-funil); posicionamento (soft-posicionamento); conteúdo (soft-conteudo).
---

## 📦 O QUE ESTA SKILL PRODUZ

**Serve o agente:** a frente COMERCIAL DE FECHAMENTO do LEON (orquestrador) e do cliente final direto, o closer que conduz a conversa quente até o Pix. Também o copiloto que conduz a venda ao vivo, mensagem a mensagem. Faz muito bem a metade de baixo da venda; a metade de cima (abrir, qualificar, agendar) é da **soft-vendas-sdr**.

Esta skill contém TUDO do seu tema, a técnica de fechamento inteira:

- **A espinha das 7 fases da conversa de venda** (o hub do diagnóstico que desce até a dor e pede a decisão), aplicada em qualquer canal (`references/processo-conversao.md`).
- **Script de venda por canal**, o roteiro de fechamento pra DM/WhatsApp, call ou reunião, montado pelo `script-builder` a partir da Oferta/PUV do Plano, com as falas de campo fase a fase (`references/script-builder.md`).
- **Fechar high-ticket na DM/WhatsApp** sem sessão estratégica, a espinha comprimida em 5 etapas com áudio, doc e vídeo curto, o **canal DEFAULT do 1:1** (`references/dm-sem-call.md`).
- **Isolamento e resposta de objeção**, uma de cada vez, com o banco completo de 30 objeções + frases de poder (`references/banco-de-objecoes.md`).
- **A arquitetura do Comercial 1:1 high-ticket + a Conta de Padaria + a coleta de sinal/Pix na própria conversa**, as 4 etapas, o diagnóstico pelos números do próprio comprador, as jogadas de fechamento e as 6 falas de campo que pegam o Pix na hora (`references/comercial-1a1-e-conta-de-padaria.md`).
- **Copiloto de venda em tempo real**, conduz uma conversa ao vivo, mensagem a mensagem (`references/copiloto-tempo-real.md`).
- **Diagnóstico de conversa empacada**, análise de print/transcrição de uma negociação que emperrou e o próximo passo (`references/analise-de-conversa.md`).
- **Métricas de pipeline** (lead → reunião → venda → ticket, win rate, CAC/LTV) pra achar o gargalo do fechamento (`references/funil-e-metricas.md`).
- **Pós-venda**, pedido de indicação, coleta de testemunho, a troca bônus-por-prova e expansão de cliente (`references/indicacoes-pos-venda.md`).
- **A cabeça do vendedor**, o sistema de crença e a confiança no preço, antes de qualquer técnica (`references/mentalidade-do-vendedor.md`).
- **Frameworks de venda consultiva adaptados ao Soft**, perguntas em escada, ensinar/desafiar a visão, qualificação por dor, tamanho do problema (`references/frameworks-consolidados.md`).
- **A condução na prática**, o jeito de conduzir destilado de sessões reais (`references/conducao-na-pratica.md`).

## ⚠️ ENTREGA = UM doc MD consolidado e COMPLETO, SEMPRE (nunca pingar a peça no chat)
Regra dura, vale mesmo pra copy curta: o RESULTADO desta skill sai como **UM documento markdown consolidado**. No **claude.ai**, um **artifact de markdown** (o dono abre, copia, baixa); no **Claude Code**, um arquivo `.md`. No **agente/Telegram**, gera o doc como arquivo e cita o path completo na resposta (vira anexo no Telegram); a condução vai em mensagens curtas, sem markdown pesado (nada de `##` nem tabela `|` no texto ao usuário, isso mora só dentro do doc). A CONDUÇÃO (perguntas de contexto, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA/COPY em si mora no DOC. Ao parar no STOP, você mostra ou atualiza o DOC INTEIRO e pergunta "ajusto?"; você NUNCA reescreve a peça em pedaços no corpo da conversa.

**"Script de venda" pedido = as 7 fases inteiras ATÉ a coleta do Pix, num só doc.** O script-builder (`references/script-builder.md`, §5 "Como entregar o script final") manda entregar as 7 fases juntas em blocos copiáveis + a nota final. **Anti-pattern grave: pingar fase-a-fase no chat, entregar F1–F3 e deferir "F4–F7 + objeções + Pix pro próximo passo".** Isso NÃO é "um passo por vez", é entrega incompleta, corta justo a Fase 7 (Isolamento → Fechamento → Pix) que é o núcleo desta skill (está no nome: o CLOSER que pega o sinal/Pix na hora). Um único STOP, sobre o SCRIPT INTEIRO já montado. Sem o doc completo entregue, a skill não terminou.

**A exceção é o modo copiloto ao vivo:** quando o dono está NO MEIO de uma conversa real e precisa da próxima jogada agora, a resposta é a mensagem operacional na hora (bloco copiável), não um doc. Aí o formato é `diagnóstico em 1 linha → mensagem pronta em bloco → 1 linha com os 2 caminhos esperados`.

# Soft Vendas Closer, conduzir e fechar (fechamento limpo)

Transforma a conversa em cliente **sem empurrar**. A venda Soft não convence à força: ela **revela a dor que já existe** e pede a decisão. O lead chega quente (veio do funil ou o SDR entregou o lead qualificado com contexto). Aqui você **confirma, não convence**, mas a conversa ainda precisa ser conduzida, e é isso que esta skill faz.

**Puxa do Plano** (a Oferta, a PUV, o Mecanismo e a Voz da `soft-posicionamento`): o script é a oferta do Plano virando conversa. Sem Plano, volta.

## De onde vem o lead (a fronteira com a soft-vendas-sdr)

Esta é a linha que faz as duas skills fazerem muito bem cada uma a sua metade da venda:

- **A metade de cima (abrir, qualificar, agendar) é da `soft-vendas-sdr`.** O SDR prospecta na DM fria, qualifica de leve, entrega o pré-qualificador (Mini Carta / Mini Webinar), vende a SESSÃO como vaga e agenda. Ele NÃO fecha.
- **A metade de baixo (conduzir e fechar) é esta skill.** O closer recebe o lead de dois jeitos:
  1. **Direto do funil:** o lead veio quente da carta/jogada/mini-webinar e cai na DM ou na sessão querendo resolver. Você começa na Fase 1.
  2. **Do SDR, com contexto:** o SDR agendou e deixou uma **nota rica no CRM** (a dor nomeada, o Problema Avançado, o score/temperatura, o BANT, as objeções que ele já disse, o que ainda falta cair). Você **abre lendo o CRM**, ecoa a qualificação e entra direto no flow do diagnóstico, nunca faz o lead repetir tudo (o recebimento do bastão, em `conducao-na-pratica.md`).
- **Handoff quente é o combustível.** Se a nota do SDR veio rasa ("tá quente"), o closer entra perdendo. Cobre o contexto upstream; o bastão bem enviado é o que faz a sessão converter.

## A doutrina do canal (é do FUNIL, não do ticket)
- **O Funil de Aula Agendada fecha de uma vez no checkout, na própria aula (one-step).** A esteira 1:1 vem DEPOIS como ascensão, e é AÍ que esta skill entra, não no fechamento do produto da aula.
- **Nos funis comerciais (carta, jogadas de campanha, mentoria), o 1:1 fecha via de regra na DM/WhatsApp** (chat com áudio, doc e vídeo curto, o modo `dm-sem-call`), mesmo high-ticket. **A call/reunião é exceção de contexto**, não o degrau seguinte do preço: entra quando o lead pede a condução ao vivo, o caso é complexo (B2B, decisão a vários), ou o especialista prefere.
- **SDR+Closer só com equipe e volume.** Volume baixo e ticket alto, uma pessoa faz as duas pontas na DM. Não confunda: aula = one-step no checkout; carta/jogada/mentoria = DM por padrão.

## A fonte e a lei
- Guia: `guia/10-vendas-consultivas.md` (a mecânica). Fonte da verdade, leia na 1ª invocação da sessão. Lá vivem a cabeça do vendedor (10.3), os 4 princípios (10.4), as premissas dos grandes (10.5), a espinha de 7 fases (10.6), o Filtro Soft (10.7), o mapa de canal (10.8), a mecânica do diagnóstico que revela sem inflar (10.10-A), o roteiro fase a fase com as falas prontas (10.10), o Isolamento (Fase 6), o catálogo de objeções no tom Soft (10.11), as frases de poder (10.12) e os 3 níveis no fechamento (10.13).
- `guia/CODIGO-DE-ESCRITA.md`: pegada falada, **simples e honesto, nunca fácil e mágico**, sem travessão na copy.
- **O eixo:** o lead vive o **teto** (preso, comparado por preço, refém da operação); "invisibilidade/percepção" é o teu diagnóstico, não a fala da conversa. Fala pelo teto que ele sente.
- Filtros anti-ia + cliente-primeiro (não vaza Léo nem jargão de cozinha) antes de qualquer texto sair: `shared-references/filtro-anti-ia/` e `filtro-cliente-primeiro.md`.

## A mecânica (frameworks consolidados)
- **Diagnóstico que desce** do fato neutro à dor que o cliente **nomeia com a própria boca**. Não se entrega a dor pronta, se conduz até ele dizer.
- **Revela dor real, NUNCA inventa.** A mesma escada que revela a verdade pode fabricar urgência, o Soft só usa a primeira. Lead sem a dor real, solta, não empurra.
- **Isola a objeção** (uma de cada vez) antes de responder.
- **Pede o sim ou o não no fim.** Sem follow-up eterno, sem perseguir quem não decide.
- **Filtra E convence:** não trabalha com quem precisa ser arrastado. Trabalha com quem já sentiu o teto e cansou dele.
- **Cabeça antes da técnica:** a mentalidade do vendedor (sistema de crença, confiança no preço) vem antes de qualquer script.
- **Coleta o sinal/Pix na própria conversa, com a temperatura no pico.** O que se empurra pra "depois" esfria e vira cobrança por mensagem (as 6 falas de campo em `comercial-1a1-e-conta-de-padaria.md`).

## A espinha de 7 fases (a venda consultiva Soft)

A ordem é fixa. O que muda por canal e ticket é ritmo e comprimento, nunca a sequência. Detalhe fase a fase com falas de campo em `references/script-builder.md`; a mecânica e o catálogo de objeções em `references/processo-conversao.md`.

| Fase | O que faz | Fala-âncora de campo |
|---|---|---|
| **1. Recuo Estratégico** | Abre consultivo, mostra que não veio empurrar; pede permissão pra perguntar antes de falar do programa. | *"Primeiro eu faço um diagnóstico do seu [problema] e te falo na cara se consigo ajudar. Se não, sou o primeiro a dizer. Só se fizer sentido nos dois lados é que a gente fala de plano e valor."* |
| **2. Descoberta** | Lead fala 70%; desce em escada da situação à dor, acha o Problema Avançado (o que as tentativas antigas criaram de pior). | *"Antes de te responder: quando você diz [palavra dele], o que isso significa pra você?"* / *"Já tentou resolver antes? O que não funcionou?"* |
| **3. Implicação** | Amplia a consciência do custo de ficar como está e qualifica a intenção; o lead verbaliza o custo, você só pergunta. | *"De 0 a 10, quanto você quer resolver isso hoje? ... 7? Mas você me disse que [o que importa] importa muito. Como isso é 7?"* |
| **4. Conexão (espelho)** | Mostra que entendeu antes de apresentar; devolve a situação nas palavras dele e confirma. | *"Deixa eu ver se entendi: você tá em [situação], tentou [X], deu [efeito colateral], e o que quer de verdade é [desejo]. É isso?"* |
| **5. Apresentação + Reframe** | Conecta só o que amarra com o que ele disse e vira a crença dele em camadas até ele concluir sozinho que precisa. | *"Isso que você me diz, você já sabe. O problema não é informação. Se você sabe e o número ainda é [resultado ruim], a falta é aplicar do jeito certo."* |
| **6. Isolamento** | Confirma que, com valor e ajuste claros, falta só investir; separa objeção real de decorativa, ANTES do preço. | *"Antes de eu te passar o investimento: se a gente resolver [as dores] em [prazo], com [formato], e o valor fizer sentido, faz sentido trabalhar junto?"* |
| **7. Fechamento** | Operacionaliza a venda (preço, condição, coleta do sinal/Pix); quem chegou aqui já decidiu. Uma jogada de encaminhamento no máximo, depois para. | *"O investimento é R$[valor] à vista ou [Xx] de R$[parcela]. [O que inclui em 1 frase]. E a gente já garante sua entrada pra começar."* |

**Regras universais entre fases:** nunca apresenta antes de entender (pular F2 = pitch no vazio) · nunca revela preço com dúvida aberta (pular F6 = objeção garantida) · nunca força quem não tem perfil (encerra leve, isso é vitória) · uma oferta por vez (Principal → Condicional → Secundária) · tom de comando, nunca de súplica · nunca cala depois do preço (ancoragem negativa; diz o número com leveza e emenda no próximo passo).

**Falas-assinatura irredutíveis (a assinatura Soft, não "qualquer LLM").** O repertório denso vive em `references/script-builder.md` (§"Falas de campo") e `conducao-na-pratica.md`; estas três são o piso que NÃO pode sair raso, porque no app o corpo é tudo que carrega. Adapta ao nicho, mantém o miolo:
- **A Conta de Padaria** (quando o lead pede preço cedo, F2): *"Você já foi num restaurante? Trazem a conta antes ou primeiro perguntam o tamanho da sua fome? Aqui é igual, não consigo te passar valor sem entender o que você precisa. Hoje, qual é a maior dificuldade no seu [problema]?"*
- **O reframe "saber ≠ aplicar"** (F5, movimento 1): *"Isso que você me diz, você já sabe. O problema não é informação. Quem mais sabe de [tema] muitas vezes é justo quem não colhe [resultado]. Se você sabe e o número ainda é [resultado ruim], a falta não é saber, é aplicar do jeito certo."*
- **O termômetro que qualifica** (F3): *"De 0 a 10, quanto você quer resolver isso hoje? ... 7? Nota ruim, hein. Você me disse que [o que importa] importa muito. Eu não arranco com um 7."*
Genérico do tipo "me conta como tá sua rotina" / "de 0 a 10 quanto quer resolver" sem o corte é a versão rasa: perde a assinatura.

## Top 7 objeções (resposta de cor, banco completo em `banco-de-objecoes`)

Isola antes de responder quando der: *"É só isso ou tem mais coisa emperrando?"*

- **"Tá caro"** → *"Caro comparado com quê? Com continuar [problema] por mais [tempo]? Se não cabe à vista, tenho condicional: parte agora, parte quando [resultado]. Facilita?"*
- **"Preciso pensar"** → *"Claro. Pensar sobre o quê, o método ou o investimento? Às vezes é uma pergunta que eu respondo agora."*
- **"Preciso falar com [sócio/cônjuge]"** → *"Faz sentido. Quando vocês conversam? Se quiser, faço uma call com vocês dois, ou te mando um resumo pra levar."*
- **"Já tentei e não deu certo"** → *"Por isso faz sentido. O que você tentou ensinava [a solução errada]. Aqui é o oposto. Você não falhou, tentou o método errado."*
- **"Não tenho tempo"** → *"Por isso o formato é esse. Separa [X] por semana. Consegue ou não?"*
- **"Funciona mesmo?"** → *"Funciona pra quem aplica como foi pensado. Se é pra você, eu descubro nas perguntas. O que você já tentou antes?"*
- **"Tem desconto?"** → *"Esse já é o menor valor. Não abaixo porque não quero te filtrar pelo desconto."*

Se a mesma objeção volta duas vezes, é outra coisa: *"Acho que tem algo além disso. O que é?"* Não nomeou, é curiosidade, não comprador, encerra com leveza.

## Fechar high-ticket na DM (o canal DEFAULT, detalhe em `dm-sem-call`)
Quando o lead já chega quente (viu o perfil, consumiu um material, veio do SDR) e quer **resolver agora** sem marcar call, você fecha 100% na DM/WhatsApp com áudio, doc e vídeo curto. Comprime a espinha de 7 fases em **5 etapas** (Conexão → Qualificação com 3-4 perguntas que filtram → Autoridade em áudio que normaliza a dor + pede permissão "posso te mostrar como funciona?" → Oferta com doc/vídeo de 3min + "já libero seu acesso" → Follow-up 10min/24h/24h). Doutrina: **venda fácil = entrega fácil**, não mata objeção à força; e **só flexibiliza o preço quando a própria pessoa abre a brecha** ("só teria metade agora" → ajusta a forma de pagamento, nunca baixa o valor cheio). O doc/vídeo da oferta puxa o bloco Oferta da `soft-posicionamento`. A abordagem fria que TRAZ o lead até aqui é da `soft-vendas-sdr`.

## Coletar o sinal/Pix na hora (detalhe em `comercial-1a1-e-conta-de-padaria`)
"Manda o link" não é coleta. Pegar o Pix na própria reunião é uma habilidade separada de vender. As 6 jogadas de campo (a energia leve e o silêncio que mata · a condição única da call gravada · o sinal é prova de comprometimento · negociar o sinal possível · plano A/B/C do pagamento · o "faço depois" que se converte na hora) preenchem o buraco entre o "sim" e o dinheiro na conta. Tudo segue a lei Soft: escassez real nunca inventada, o sinal é prova de comprometimento (não armadilha), respeita-se o não.

## ⛔ STOP antes de mandar pro lead
Um único STOP, sobre a PEÇA INTEIRA já montada no DOC (o script COMPLETO das 7 fases até o Pix, ou o próximo passo/resposta de objeção completo). Mostra no DOC, imprime a tabela do Crivo ANTES dele (ver o gate abaixo) e **PARA**: pergunta *"ajusto ou pode ir pro lead?"*. Nunca despeja a peça direto pro lead nem assume o "manda". A condução é sua; o disparo é do dono. **Não confunda "peça consolidada" com "liberação incremental de fases":** parar na F3 e prometer o resto pro próximo passo QUEBRA a regra `ENTREGA = UM doc completo` (é o anti-pattern do bloco de entrega acima). O STOP é sobre o doc pronto, não sobre liberar fase por fase. **No copiloto ao vivo** o STOP é implícito (o dono está na conversa e decide na hora), mas mesmo lá você entrega UMA jogada por vez, nunca um roteiro inteiro de uma vez.

> **Passo 0, sempre: lê o perfil do usuário** (`shared-references/crivo/00-perfil-do-usuario.md`). Avatar, fonte de VoC, banco de provas, voz e nicho são DELE, nunca os do Léo (que são só um perfil de exemplo). Usuário sem perfil (cold start) é roteado pro onboarding (Plano na `soft-posicionamento` + mineração de VoC no `01-entrada-verbatim.md`) antes de produzir, em vez de assumir os dados do Léo.
>
> **Aspa de cliente exige GREP visível na fonte real do usuário.** Toda fala entre aspas que se declara verbatim tem que ser substring literal que você grepou e mostrou na fonte de VoC DELE (a tabela de ancoragem, `01-entrada-verbatim.md` passo 6). **Persona fictícia SEM perfil de VoC real não tem fonte, logo NÃO pode ter aspa "real":** aí a peça sai marcada `RASCUNHO-COM-PENDÊNCIA` / `[A CONFIRMAR]` e roteia pro onboarding. É PROIBIDO afirmar "verbatim-âncora, fonte real da [persona]" ou "nenhuma aspa é inventada, todas batem na fonte" sem o grep à mostra na fonte do usuário. Sem fonte, não se ASSUME nem se DECLARA verbatim, marca-se rascunho. Encenar a ancoragem (afirmar que bateu sem grepar) é a fraude que o gate existe pra matar.

## Como conduz (por pergunta, nunca despeja)
1. Confirma o Plano (Oferta + PUV + Mecanismo + Voz). Sem ele, volta pra `soft-posicionamento`.
2. Confirma de onde vem o lead: veio do funil quente? veio do SDR com nota no CRM (então lê a nota e ecoa)? Nunca faz o lead repetir o que já contou.
3. Pergunta o estágio: conduzir/gerar o script (DM / call / reunião)? uma objeção específica? diagnóstico de uma conversa que empacou? copiloto em tempo real? pós-venda (indicação / testemunho)?
4. Puxa o reference certo (`processo-conversao` é o hub) + os densos da etapa.
5. Escreve ou conduz, mostra, ajusta, passa no filtro anti-ia e no gate `shared-references/crivo/` (CUB bloqueante), entrega.

**Consulta `references/conducao-na-pratica.md` o tempo todo**, é o jeito de conduzir que faz a venda sair excelente (recebe o bastão do SDR lendo o CRM · diagnóstico de mudança mental, não passo a passo · a nota 0-10 ancora · expectativa honesta, promete melhorar não 100% · mostra o case sem medo · ser pequeno é a vantagem · ofertas de risco/ancoragem/custo invisível · sistema de prova · vender liberta, sem mágica).

## Os 3 ambientes onde o closer roda
- **App (claude.ai):** o dono pede a peça de fechamento (um script, uma resposta de objeção, um diagnóstico de conversa) → entrega no **artifact de markdown**. O copiloto ao vivo aqui responde a jogada na hora, no chat.
- **Claude Code:** mesma coisa, a peça sai como arquivo `.md`.
- **Agente / Telegram (LEON e frota):** o dono cola a conversa real ("cliente disse X, o que respondo?") e recebe a próxima jogada na hora; ou pede o script pra uma oferta nova. É o ambiente do copiloto ao vivo e da análise de conversa colada.

## O gate de saída obrigatório (o Crivo, bloqueante)
Antes de mostrar a peça, ela passa pelo Crivo embutido em `shared-references/crivo/`, nesta ordem. **O gate é ARTEFATO IMPRESSO ANTES do doc no STOP, não promessa de texto.** Narrar "passei no Crivo, como a skill exige" sem a tabela na tela é encenação e não conta como entrega.
1. **Ancoragem** (`crivo/01-entrada-verbatim.md`): toda fala entre aspas é verbatim literal grepado na fonte real do usuário. Aspa que não bate na fonte reprova. **Persona sem fonte de VoC → nenhuma aspa "real": marca `RASCUNHO-COM-PENDÊNCIA`/`[A CONFIRMAR]`, nunca declara verbatim** (ver o Passo 0).
2. **Simulação na pele do avatar** (`crivo/02-simulacao-cliente.md`): onde ele larga, onde se reconhece, o teste dos 2 segundos.
3. **Gate CUB bloqueante** (`crivo/03-gate-cub.md`): **imprime a tabela de fato**, o VEREDITO é o pior bloco (Confusão · Inacreditável · Tédio); peça que falha não sai, volta pra reescrita. Fala-mecânica de venda (descoberta, isolamento, termômetro) roda a régua reduzida; o bloco que carrega prova/promessa (o case, a oferta) roda a tabela cheia. Formato mínimo a colar:

```
BLOCO: [o slide/parágrafo/fala, entre aspas]
0. Ancorado ........ PASSA/FALHA (grep na fonte do usuário, N do sub-padrão)
1. Confuso ......... PASSA/FALHA
2. Inacreditável ... PASSA/FALHA
3. Boring .......... PASSA/FALHA
=> VEREDITO DA PEÇA: [pior bloco manda]
```

**O linter é passo BLOQUEANTE, não nota solta.** Roda a copy no `scripts/lint_copy.py` (anti-IA + anti-voz Soft): `python3 scripts/lint_copy.py peca.txt` ou `echo "..." | python3 scripts/lint_copy.py -`. **`exit 1` = COPY REPROVADA = não entrega, reescreve e re-roda.** Ele derruba por 2 falhas duras: **o em-dash (o travessão longo U+2014)** e a **família da palavra banida "tr-a-v-a-r"** (todas as flexões e o antônimo "des-tr-a-v-a-r"). **Valem em QUALQUER lugar do `.md`, inclusive TÍTULOS, cabeçalhos e rótulos de fase**, não só nas aspas de copy: um título "Script [travessão] WhatsApp" ou um header "FASE 3 [travessão]" ou a palavra banida na narração ("a intimidade tr-a-v-o-u", "(des-tr-a-v-a-d-a)") reprova igual. Troca o travessão por ponto ou hífen comum; troca a palavra banida por emperrar/empacar/parar/freio/amarra. No chat (sem rodar o script), faz CTRL+F manual do travessão e da palavra banida em todo o doc antes de marcar ✓. O anti-IA limpa o robô; o Crivo dá a força. **Sem a tabela do Crivo impressa junto E o linter em exit 0, a peça não foi entregue.**

## Princípios
- **Confirma, não convence:** se a oferta do Plano é forte e a carta aqueceu, a conversa fecha confirmando a crença, não construindo do zero.
- **Honesto sempre:** simples e real, nunca fácil e mágico. O avatar já tomou pau de promessa mágica.
- **Pede decisão e respeita o não.** Lead que precisa de empurrão não é cliente, é problema futuro.

## When NOT to use
- **Abrir conversa fria, prospectar no Direct, qualificar de leve, vender/agendar a sessão, operar o CRM (GHL/GoHighLevel), o SDR de IA** → **soft-vendas-sdr**. Esta skill começa quando o lead já chega quente.
- **Contrato de mentoria/consultoria** (depois do sim) → **soft-contratos-consultoria** (cláusulas anti-calote/pagamento/PF-PJ/por formato, glossário jurídico, modo enxuto vs robusto). Fechou a venda → gera o contrato lá, sem trocar de método.
- **Carta, VSL, mini-webinar ou landing** (aquecer/qualificar o lead antes da conversa) → `soft-funil-carta`, `soft-funil-miniwebinar`, `soft-funil-landing`.
- **Posicionamento, Oferta, PUV, Mecanismo, Voz** (a fundação de onde o script puxa) → `soft-posicionamento`. Sem Plano, a venda volta pra lá.
- **Conteúdo de feed** (carrossel, reel, stories, headline) → `soft-conteudo-*`.
- **Onde começar / próximo passo / diagnóstico da jornada** → `soft-leon` (o orquestrador invoca esta skill quando chega no fechamento).

## Anti-Patterns

| Erro | Por que quebra | Faz assim |
|---|---|---|
| Deu preço antes do Isolamento (F6) | Dúvida aberta + preço = objeção garantida ("vou pensar" em 70% dos casos) | Isola primeiro, revela valor só com o caminho limpo |
| Faz o lead do SDR repetir tudo | Queima a 1ª impressão, expõe que o time não conversa | Abre lendo a nota do CRM, ecoa a qualificação, entra direto no diagnóstico |
| Cala depois de dizer o preço | Ancoragem negativa: o cérebro ecoa só o custo, apaga o valor | Diz o número com leveza e emenda no próximo passo, sem pausa dramática |
| "Faço o Pix depois" aceito de boa | Sai da conversa quente, esfria, vira cobrança por mensagem | Resolve na hora: ou faz agora, ou o "mas..." vira objeção pra tratar ali |
| Script sem verbatim (aspas inventadas) | Reprova no Crivo de ancoragem; soa genérico, não fecha | Puxa 3-5 falas reais da fonte do cliente, a 1ª linha nasce de uma delas |
| Follow-up eterno sem pedir sim/não | Queima o aquecimento e a autoridade; lead que precisa de 7 toques não está pronto | Pede a decisão na conversa; antecipa o follow-up pra dentro da conversa |
| Apresentou o método inteiro (F5) | Lead desengaja; vira aula, não venda | Só o que amarra com o que ele disse + 1 reframe |
| Nome de framework vazando pro lead | "Degrau de implicação" soa manual, mata a naturalidade | O framework opera invisível; vira pergunta em linguagem do nicho |

## Handoff
- **Pra trás:** lead frio, prospecção, qualificação, agendamento → **soft-vendas-sdr** (o closer não abre conversa fria). Pré-qualificador que falta → `soft-funil-carta`/`soft-funil-miniwebinar`. Oferta/PUV indefinida → `soft-posicionamento`.
- **Pra frente:** venda fechada → contrato na **soft-contratos-consultoria**; os números (lead → reunião → venda → ticket) voltam pro **LEON**, que calibra a rotina; cliente novo → o pós-venda abre indicações e testemunho (a troca bônus-por-prova), que viram prova pra `soft-posicionamento` e as `soft-conteudo-*`.
