---
name: soft-vendas
description: A venda consultiva do método Soft, o fechamento limpo. Transforma a conversa em cliente sem empurrar, revela a dor real e pede a decisão. Cobre script de venda (WhatsApp / call / reunião), prospecção no Direct, isolamento de objeção, diagnóstico de conversa empacada, copiloto em tempo real, métricas de pipeline e pós-venda (indicações + testemunhos). Puxa a Oferta e a PUV do Plano de Posicionamento. Use SEMPRE que envolver "script de venda", "venda", "vender", "cliente objetou", "objeção", "fechamento", "fechar", "follow-up", "prospecção", "DM/Direct", "WhatsApp", "lead sumiu", "lead frio", "não consigo cobrar caro", "cabeça do vendedor", "pipeline", "win rate", "CAC", "analisa essa conversa", "pós-venda", "pedir indicação", "testemunho". NÃO use pra carta/vídeo de aquecimento ou funil (isso é soft-funil-carta/-landing), nem pra posicionamento ou conteúdo.
---

## 📦 O QUE ESTA SKILL PRODUZ

**Serve o agente:** braço-comercial do LEON (orquestrador) e cliente final direto, equipa quem vende e fecha o 1:1 high-ticket; também o copiloto que conduz a conversa ao vivo.

- **Script de venda por canal**, roteiro de fechamento para WhatsApp, call ou reunião presencial, montado pelo `script-builder` a partir da Oferta/PUV do Plano.
- **Mensagem de prospecção no Direct (DM)**, abordagem que abre conversa sem parecer spam (`prospeccao-dm`).
- **Isolamento e resposta de objeção**, uma objeção por vez, com respostas-modelo do `banco-de-objecoes`.
- **Diagnóstico de conversa empacada**, análise de print/transcrição de uma negociação que emperrou e próximo passo (`analise-de-conversa`).
- **Copiloto de venda em tempo real**, conduz uma conversa ao vivo, mensagem a mensagem (`copiloto-tempo-real`).
- **As 7 fases da conversa de venda**, o roteiro-hub do diagnóstico que desce até a dor (`processo-conversao`).
- **Trabalho de mentalidade do vendedor**, a cabeça antes da técnica: sistema de crença, confiança no preço (`mentalidade-do-vendedor`).
- **Frameworks de venda consultiva adaptados ao Soft**, perguntas em escada, checklist de qualificação, ensinar/desafiar a visão, qualificação por dor, tamanho do problema, checklist de recorrência (`frameworks-consolidados`).
- **Arquitetura do Comercial 1:1 high-ticket + Conta de Padaria**, as 4 etapas da venda, o diagnóstico pelos números do próprio comprador, jogadas de fechamento (G4) e de confiança (Mid House), e o comercial operado por IA / Sócio IA (`comercial-1a1-e-conta-de-padaria`).
- **Métricas de pipeline**, lead → reunião → venda → ticket, win rate, CAC/LTV (`funil-e-metricas`).
- **Pós-venda**, pedido de indicação, coleta de testemunho e expansão de cliente (`indicacoes-pos-venda`).
- **Contrato de mentoria/consultoria pronto pra assinar**, gerado no mesmo fluxo depois do sim, em **`.docx`** (D4Sign/Clicksign/Autentique) ou, sem `/mnt/user-data/outputs`, em **markdown inline**; com cláusulas anti-calote, de pagamento, PF/PJ e por formato, mais glossário jurídico (`processo-contratos` + `clausulas-*` + `glossario-juridico`).

**Gate externo obrigatório:** todo texto que vai pro lead (script, DM, follow-up) passa antes pelo `shared-references/crivo/`, o gate CUB bloqueante (Confusão · Inacreditável · Tédio). Mensagem genérica ou promessa sem chão é consertada antes de sair.

# Soft Vendas, a venda consultiva (fechamento limpo)

Transforma a conversa em cliente **sem empurrar**. A venda Soft não convence à força: ela **revela a dor que já existe** e pede a decisão. Quando o Plano está de pé, o lead chega quente da carta e aqui você **confirma, não convence**, mas a conversa ainda precisa ser conduzida, e é isso que esta skill faz.

**Puxa do Plano** (a Oferta, a PUV, o Mecanismo e a Voz da `soft-posicionamento`): o script é a oferta do Plano virando conversa. Sem Plano, volta.


## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a peça no chat)
Regra dura, vale mesmo pra copy curta: o RESULTADO desta skill sai como **UM documento markdown consolidado**. No **claude.ai**, um **artifact de markdown** (o dono abre, copia, baixa); no **Claude Code**, um arquivo `.md`. A CONDUÇÃO (perguntas de contexto, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA/COPY em si mora no DOC. Ao parar num STOP, você mostra ou atualiza o DOC e pergunta "ajusto?"; você NUNCA reescreve a peça em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## A fonte e a lei
- Guia: `guia/10-vendas-consultivas.md` (a mecânica). Fonte da verdade.
- `guia/CODIGO-DE-ESCRITA.md`: pegada falada, **simples e honesto, nunca fácil e mágico**, sem travessão na copy.
- **O eixo:** o lead vive o **teto** (preso, comparado por preço, refém da operação); "invisibilidade/percepção" é o teu diagnóstico, não a fala da conversa. Fala pelo teto que ele sente.
- Filtros anti-ia + cliente-primeiro (não vaza Léo nem jargão de cozinha) antes de qualquer texto sair: `shared-references/filtro-anti-ia/` e `filtro-cliente-primeiro.md`.

## A mecânica (Igor Mello + frameworks consolidados)
- **Diagnóstico que desce** do fato neutro à dor que o cliente **nomeia com a própria boca**. Não se entrega a dor pronta, se conduz até ele dizer.
- **Revela dor real, NUNCA inventa.** A mesma escada que revela a verdade pode fabricar urgência, o Soft só usa a primeira. Lead sem a dor real, solta, não empurra.
- **Isola a objeção** (uma de cada vez) antes de responder.
- **Pede o sim ou o não no fim.** Sem follow-up eterno, sem perseguir quem não decide.
- **Filtra E convence:** não trabalha com quem precisa ser arrastado. Trabalha com quem já sentiu o teto e cansou dele.
- **Cabeça antes da técnica:** a mentalidade do vendedor (sistema de crença, confiança no preço) vem antes de qualquer script.
- **Marketing qualifica, Comercial vende.** Todo funil Soft entrega o "sim do produto"; aqui você fecha o "sim da venda" no 1:1, high-ticket (3k+) nunca fecha sozinho no checkout. As 4 etapas (abertura/investigação/demonstração/obtenção de compromisso) e a **Conta de Padaria** (diagnóstico pelos números do próprio comprador) → `references/comercial-1a1-e-conta-de-padaria.md`.

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
| **7. Fechamento** | Operacionaliza a venda (preço, condição, link); quem chegou aqui já decidiu. Uma jogada de encaminhamento no máximo, depois para. | *"O investimento é R$[valor] à vista ou [Xx] de R$[parcela]. [O que inclui em 1 frase]. Faz sentido pra você?"* |

**Regras universais entre fases:** nunca apresenta antes de entender (pular F2 = pitch no vazio) · nunca revela preço com dúvida aberta (pular F6 = objeção garantida) · nunca força quem não tem perfil (encerra leve, isso é vitória) · uma oferta por vez (Principal → Condicional → Secundária) · tom de comando, nunca de súplica.

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

## Prospecção por DM (Modo A+, detalhe em `prospeccao-dm`)

**Regra-mãe: a DM leva pra Carta/vídeo, nunca vende na DM.** Abre conversa, qualifica de leve, entrega o pré-qualificador (Mini Carta ou Mini Webinar) e espera o lead voltar esquentado; só aí começa a Fase 1. DM → Carta/vídeo → Venda, nessa ordem. Uma pergunta por mensagem, referência concreta, recua na fricção.

- **Frio** (seguiu há 1-7 dias): puxa a essência, por que ele seguiu. *"Vi que chegou por aqui faz pouco. Por curiosidade, o que te fez começar a seguir?"*
- **Morno engajado** (acompanha há meses, nunca comprou): ancora num sinal concreto que ele já deu. *"Vi que você acompanha [conteúdo] e comentou [X]. Como tá sendo pra você [contexto que ele mencionou]?"*
- **Sinal ativo** (se inscreveu / baixou / mandou dúvida): confirma o interesse e entrega o pré-qualificador na janela quente (2h). *"Vi que você [ação]. O que mais te chamou atenção? ... Então isso aqui vai te ajudar: [link]. Dá uma lida e me fala o que achou."*

## ⛔ STOP antes de mandar pro lead
Mostra o script (ou o próximo passo/DM/resposta de objeção) no DOC e **PARA**: pergunta *"ajusto ou pode ir pro lead?"*. Nunca despeja a peça direto pro lead nem assume o "manda". A condução é sua; o disparo é do dono.

> **Passo 0, sempre: lê o perfil do usuário** (`shared-references/crivo/00-perfil-do-usuario.md`). Avatar, fonte de VoC, banco de provas, voz e nicho são DELE, nunca os do Léo (que são só um perfil de exemplo). Usuário sem perfil (cold start) é roteado pro onboarding (Plano na `soft-posicionamento` + mineração de VoC no `01-entrada-verbatim.md`) antes de produzir, em vez de assumir os dados do Léo.

## Como conduz (por pergunta, nunca despeja)
1. Confirma o Plano (Oferta + PUV + Mecanismo + Voz). Sem ele, volta pra `soft-posicionamento`.
2. Pergunta o estágio: prospecção no Direct? script (WhatsApp / call / reunião)? uma objeção específica? diagnóstico de uma conversa que empacou? copiloto em tempo real? pós-venda (indicação / testemunho)?
3. Puxa o reference certo (`processo-conversao` é o hub) + os densos da etapa.
4. Escreve ou conduz, mostra, ajusta, passa no filtro anti-ia e no gate `shared-references/crivo/` (CUB bloqueante), entrega.

**Consulta `references/conducao-na-pratica.md` o tempo todo**, é o jeito de conduzir que faz a venda sair excelente (diagnóstico de mudança mental, não passo a passo · a nota 0-10 ancora · expectativa honesta, promete melhorar não 100% · mostra o case sem medo · ser pequeno é a vantagem · ofertas de risco/ancoragem/custo invisível · sistema de prova · vender liberta, sem mágica).

## References (densos, sob demanda)
`processo-conversao` (o hub: as 7 fases da conversa) + `script-builder` (monta o script por canal) · `prospeccao-dm` (DM de prospecção) · `mentalidade-do-vendedor` (a cabeça antes da técnica) · `banco-de-objecoes` (objeções e respostas) · `funil-e-metricas` (pipeline, win rate, CAC/LTV) · `indicacoes-pos-venda` (indicações + testemunhos + expansão) · `analise-de-conversa` (diagnóstico de print/transcrição) · `copiloto-tempo-real` (conduz uma conversa ao vivo) · `frameworks-consolidados` (perguntas em escada · checklist de qualificação · ensinar/desafiar a visão · qualificação por dor · tamanho do problema · checklist de recorrência, adaptados ao Soft).

**O Comercial high-ticket (1:1):** `comercial-1a1-e-conta-de-padaria`, a arquitetura do "+ Comercial" de todo funil (marketing qualifica / comercial vende), as 4 etapas da venda, a **Conta de Padaria**, as jogadas de fechamento high-ticket (G4) e de confiança (Mid House), e o comercial operado por IA (Sócio IA: automação de SDR, transcrição+probabilidade, follow-up pela objeção, lead score, roleplay).

**Contratos** (depois do sim): `processo-contratos` + as cláusulas (anti-calote · pagamento · PF/PJ · por formato) + glossário jurídico. Fechou a venda → gera o contrato de mentoria/consultoria no mesmo fluxo, sem trocar de ferramenta. **Entrega:** `.docx` em `/mnt/user-data/outputs/` (pronto pra D4Sign/Clicksign/Autentique); **fallback**, se esse diretório não existir, entrega o contrato como markdown estruturado inline no chat.

**Transversal:** `conducao-na-pratica`, o jeito de conduzir a venda destilado de sessões reais (diagnóstico de mudança mental, nota 0-10, expectativa honesta, case sem medo, ser pequeno como vantagem, ofertas na conversa, sistema de prova, vender liberta); exemplos de nichos neutros, nunca o Léo.

## Princípios
- **Confirma, não convence:** se a oferta do Plano é forte e a carta aqueceu, a conversa fecha confirmando a crença, não construindo do zero.
- **Honesto sempre:** simples e real, nunca fácil e mágico. O avatar já tomou pau de promessa mágica.
- **Pede decisão e respeita o não.** Lead que precisa de empurrão não é cliente, é problema futuro.

## When NOT to use
- **Carta, VSL, mini-webinar ou landing** (aquecer/qualificar o lead antes da conversa) → `soft-funil-carta`, `soft-funil-miniwebinar`, `soft-funil-landing`.
- **Posicionamento, Oferta, PUV, Mecanismo, Voz** (a fundação de onde o script puxa) → `soft-posicionamento`. Sem Plano, a venda volta pra lá.
- **Conteúdo de feed** (carrossel, reel, stories, headline) → `soft-conteudo-*`.
- **Onde começar / próximo passo / diagnóstico da jornada** → `soft-leon` (o orquestrador invoca esta skill quando chega na venda).
- **Só o contrato depois do sim** vive aqui mesmo (fluxo de contratos), mas contrato isolado sem venda → `soft-contratos-consultoria`.

## Anti-Patterns

| Erro | Por que quebra | Faz assim |
|---|---|---|
| Deu preço antes do Isolamento (F6) | Dúvida aberta + preço = objeção garantida ("vou pensar" em 70% dos casos) | Isola primeiro, revela valor só com o caminho limpo |
| Script sem verbatim (aspas inventadas) | Reprova no Crivo de ancoragem; soa genérico, não fecha | Puxa 3-5 falas reais da fonte do cliente, a 1ª linha nasce de uma delas |
| Follow-up eterno sem pedir sim/não | Queima o aquecimento e a autoridade; lead que precisa de 7 toques não está pronto | Pede a decisão na conversa; antecipa o follow-up pra dentro da call |
| Apresentou o método inteiro (F5) | Lead desengaja; vira aula, não venda | Só o que amarra com o que ele disse + 1 reframe |
| Nome de framework vazando pro lead | "Degrau de implicação" soa manual, mata a naturalidade | O framework opera invisível; vira pergunta em linguagem do nicho |
| Vender na DM / oferecer call direto na DM | Pula o filtro, fecha gente que cancela | DM leva pro pré-qualificador; a call só depois que ele volta |

## Handoff
Venda fechada → os números (lead → reunião → venda → ticket) voltam pro LEON, que calibra a rotina. Cliente novo → o pós-venda abre indicações e testemunho (que viram prova pra `soft-posicionamento` e as `soft-conteudo-*`).
