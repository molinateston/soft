---
name: soft-conteudo-stories
description: >-
  Escreve a SEQUÊNCIA de stories em arquivo .md, frame a frame, com tipo, texto na tela, áudio, sticker e visual em cada um. Use quando o pedido for: "monta os stories de hoje", "sequência de stories", "story de venda", "campanha de 5 dias nos stories", "faz uma caixinha", "rotina de stories", "story pra abrir vaga", "meus stories não convertem" (diagnóstico), "story infiltrado", "arco de stories". NÃO use pra: "quero um desafio de 5 dias" e o evento de lançamento com carrinho (soft-launch); a headline ou abertura isolada, que vem ANTES (soft-conteudo-headlines); os slides do carrossel (soft-conteudo-carrossel); o roteiro falado de reel (soft-conteudo-reels); levar a peça pronta pra outra plataforma (soft-conteudo-multiplataforma); decidir o tema (soft-conteudo-planner); arte e PNG dos frames (soft-designer); bio e destaques (soft-plano-posicionamento); a conversa no direct (soft-vendas-closer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Stories, o arco de conversão diária

Esta skill escreve a sequência de stories inteira, frame a frame, e entrega num arquivo `.md` que a pessoa lê e posta na ordem. Cada frame sai com o tipo marcado, o texto na tela, o áudio, o sticker e o visual sugerido. Ela decide junto com o dono qual dos 4 sistemas o objetivo pede, e reprova sozinha todo frame que não passa no gate.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Pedido que nomeia evento, turma ou data: ao menos uma peça carrega a razão de agir agora.** Rode `grep -niE 'turma|vagas|come[çc]a|aula ao vivo|[0-9]{2}/[0-9]{2}' <perfil>` e cole a saída. O que voltar entra em pelo menos uma peça, com o número literal. Cole `peças no lote: N · com razão de agir agora: N`, e zero na segunda coluna, num pedido que nomeia turma ou evento, reprova o lote.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Capacidade negada no perfil é fato, nunca lacuna a interpretar.** Antes de escolher a mecânica do CTA, rode `grep -in 'automação\|automacao\|robô\|bot' <perfil do dono>` e cole a saída literal. Linha que diz `nenhuma automação` responde `não`, e ela não é omissão nem falso positivo a contornar. Cole `mecânica exige automação? sim/não · perfil declara: <a linha literal> · mecânica adaptada: <qual>`. Negação no perfil sai como CTA sem robô, e manter a mecânica por leitura funcional, herança de outra plataforma ou hábito presumido reprova a peça.

**No story, a cena vence a máxima.** Frame que abre com máxima ou definição volta pro passo de escrita, e a checagem marca quais frames abrem por cena e quais por tese, com a segunda coluna nunca acima de um terço.

**O universo da R3 é o das unidades produzidas, nunca o dos pilares.** As `teses distintas` saem das pautas, headlines ou frames que a peça entrega, e a contagem igual ao número de pilares do dono é resultado inválido. Cole `unidades no lote: N · linhas em teses.txt: N`, os dois iguais, e só então a matriz de pares.

**`teses.txt` é arquivo obrigatório da pasta de saída**, uma tese de até 4 palavras por linha, ao lado do `conferencia/checagem-titulos.md`. Sem ele o gate não calcula a R3 e o campo do fecho sai com a instrução do script no lugar do número, o que reprova a entrega.

**As 3 perguntas do gate, o apelido explicado.** Onde esta skill (e as irmãs de conteúdo) diz "as 3 perguntas", são estas, sempre nesta ordem: **dá pra ver?** (o frame vira cena quando você fecha o olho, ou é adjetivo) · **dá pra falsificar?** (é um fato que alguém poderia contestar, ou é opinião de adorno) · **só você diz?** (o concorrente direto assinaria a mesma frase, ou tem cena e mecanismo que só o dono tem). Frame que não passa nas três não vai pro público.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra, num caso fictício de nicho neutro, a entrada que o dono deu, as perguntas que a skill fez, uma rotina CARO completa e um dia inteiro da Sequência de Venda frame a frame, no formato real da entrega.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o tema e o que quer que o story faça e eu escrevo os frames). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra os frames com o que o dono já colou. Se faltar um insumo que o story não vive sem (o assunto, ou o que ele deve levar o seguidor a fazer), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez (a headline, o tipo de pedido, a dor) e escreve com o que o dono for dando.

A pergunta do modo é UMA por sequência. As outras três partes entram nos passos abaixo:

- **Ensina enquanto faz:** ao escolher o arco do sistema (rotina CARO, Sequência de Venda), escreve UMA linha do porquê ("monto a Sequência de Venda porque você quer converter essa semana; a rotina CARO aquece, mas não pede a ação hoje"), pra o dono decidir sozinho na próxima.
- **Puxa o material bruto:** quando a intenção vier rasa ("quero engajar mais"), não segue no genérico. Pede o concreto: "o que você quer que o seguidor faça no fim, e de qual dor real dele isso parte, com as palavras dele?". A intenção concreta muda o arco inteiro.
- **Oferece refinar no fim:** depois de mostrar os frames, fecha com UMA linha de ajuste ("quer mais frames? outra abertura? enxotar a caixinha de pergunta? refaço só o frame que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "os stories de hoje", "rotina de stories", "o que eu posto hoje no story" | **1 · CARO** (o default) |
| "faz uma caixinha", "quero saber o que eles querem", "pergunta pra base" | **2 · CAIXINHA ESTRATÉGICA** |
| "campanha de 5 dias", "sequência pra vender X", "vou abrir vaga", "story de venda" | **3 · SEQUÊNCIA DE VENDA** |
| "quero atrair gente nova pelo story", "story pra tráfego frio", "story infiltrado" | **4 · STORY INFILTRADO** (pede verba) |
| "meus stories não convertem", "as métricas caíram", "ninguém responde a caixinha" | **5 · DIAGNÓSTICO** |

Pedido ambíguo ("me ajuda com os stories"): pergunta UMA coisa só, o que ele quer que aconteça (vender uma oferta, aquecer a base, ler quem quer comprar, atrair gente nova, ou entender por que não converte), mostra a tabela como cardápio e segue pela resposta.

**Os 4 sistemas são camadas, não estilos.** O CARO é o chão: sem ele rodando há semanas, os outros três viram spam. A Sequência de Venda é campanha pontual, a Caixinha entra 2 a 3 vezes por semana, e o Infiltrado é o único que mira público frio.

> **O Story Infiltrado depende de verba de tráfego pago.** Não é onde se começa. Ele exige teste pago, iteração e decisão em 3 dias com número na mão. Se o dono não tem verba pra iterar, a skill diz isso em uma linha e recomenda a Ação 1 ou a 3 no lugar.

## O perfil do dono vem do banco do agente

Onde esta skill precisa de voz, avatar, mecanismo, inimigos, prova ou a palavra-chave do direct: **leia do perfil/brain do agente quando existir**; se não existir, faça a entrevista curta do "Sem o insumo" e siga com o que faltar marcado `[DADO: confirmar]`. Nunca invente, nunca crie um arquivo de perfil.

---

## Ações 1 a 4 · CONSTRUIR (o bloco vale pras quatro)

**O que faz:** monta a sequência de stories do sistema escolhido, frame a frame, cada frame com uma função única.

**Precisa de:** o **objetivo** do dono (é ele que decide o sistema) · a **headline/eixo do dia** (você escreve aqui pela régua de título desta skill, ou puxa de um banco pronto) · 3 a 5 falas de DOR e 3 a 5 de DESEJO, do perfil/brain do agente · a prova disponível (print, áudio de cliente, bastidor) · a palavra-chave única do direct.

**Sem o insumo:**
- **Sem objetivo declarado:** pergunta UMA vez, com as 5 opções da tabela de roteamento como cardápio. Se o dono só disser "stories de hoje", o default é CARO.
- **Sem headline/eixo:** você escreve o eixo AQUI, pela régua de título que esta skill carrega (`shared-references/crivo/07-regua-de-titulos.md`): 3 aberturas a partir da dor mais forte que você ancorou (cada uma no teto de 5 a 10 palavras e 50 caracteres da linha de topo) e peça pro dono cravar UMA. Quer um banco maior de variações? Existe a soft-conteudo-headlines, mas é opção, o eixo se resolve aqui. Nunca invente um eixo morno.
- **Sem fundação nenhuma:** entrevista curta de 4 perguntas, numa mensagem só. (1) Quem é o teu cliente, em uma frase. (2) Uma dor que ele te fala com as palavras dele. (3) O que o teu método faz de diferente, e como ele se chama. (4) Que prova você tem pra mostrar hoje (print, áudio, número). O que faltar vira `[DADO: confirmar]`.
- **Sem palavra-chave:** propõe 2 ou 3 curtas, tiradas do nome do método ou do resultado, e pede pro dono cravar UMA. Todas as peças apontam pra mesma.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Evento datado do perfil que cai DENTRO da janela da sequência vira conteúdo obrigatório do dia, acima do papel de âncora de calendário.** Antes de escrever o Dia 1, liste todo evento com data no perfil do dono (aula, live, abertura, início de turma, encerramento) e escreva, pra cada um, `evento: <qual> · data: <dd/mm> · cai na janela? sim/não · em qual dia da sequência · como aparece nos frames desse dia: <literal>`. Evento que cai na janela e não aparece em nenhum frame reprova a sequência: no dia do evento, o CTA do dia é o evento, e o Direct só entra depois dele. Cole a tabela no arco, antes dos frames, com estas quatro colunas e nesta ordem:

```
| evento | data | cai na janela? | frame |
```

**A regra tem duas metades e as duas se conferem por comando.** Antes de fechar, rode e cole:

```
grep -oE '[0-9]{2}/[0-9]{2}' <perfil do dono> | sort -u
grep -n 'cai na janela?' <arquivo do arco>
grep -n '<a data literal>' <arquivo do dia do evento>
```

O primeiro lista as datas do perfil, o segundo prova que a tabela existe, e o terceiro mostra em que frame o evento entrou. **Evento que cai na janela e não aparece em nenhum frame reprova a sequência**, e evento que aparece só depois da metade dos frames do dia dele volta pro passo de escrita: no dia do evento, o CTA do dia é o evento, e o Direct só entra depois dele. Feche com `eventos datados no perfil: N · dentro da janela: N · com frame apontado: N`, os dois últimos iguais.

**Entrega:** `stories-[sistema]-[data].md`, frame a frame numerado, cada frame com tipo CARO (C/A/R/O) ou dia da Sequência (1 a 5), mais texto na tela, áudio, sticker e visual. Em ambiente que renderiza markdown, mostre o doc renderizado; com sistema de arquivo, salve o `.md`; num agente de mensageria, grave o arquivo e cite o path completo. **STOP por bloco:** a rotina do dia OU um dia da Sequência, nunca os 5 dias de uma vez.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro (por ação):** Ação 1 → `references/sistema-caro.md` · Ação 2 → `references/caixinha-estrategica.md` · Ação 3 → `references/sequencias-de-venda.md` · Ação 4 → `references/story-infiltrado.md`.

**Profundidade:** `references/camadas-conciencia.md` (a função do arco no funil) · `references/algoritmo-e-metricas.md` (os benchmarks, quando o dono perguntar número).

---

## Ação 5 · DIAGNÓSTICO (quando os stories não convertem)

**O que faz:** nomeia UM gargalo e propõe UM experimento de 7 dias, em vez de mexer em cinco coisas ao mesmo tempo.

**Precisa de:** os números do perfil do dono (completion, saída por frame, story-to-direct), que só ele tem · o que ele vem postando nas últimas 2 semanas.

**Sem o insumo:** se ele não tem os números, pede 3 prints (a tela de métricas do último story, a lista de saídas por frame, e o total de respostas no direct na semana). Sem nenhum número, a skill diz que o diagnóstico fica cego e propõe medir por 7 dias antes de mudar qualquer coisa. Nunca inventa métrica.

**Entrega:** `diagnostico-stories-[data].md`, com o gargalo nomeado, a causa provável, o experimento de 7 dias e o número que decide se funcionou. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/algoritmo-e-metricas.md` (o protocolo de diagnóstico, INTEIRO antes de opinar; é exatamente a reference que resolve este pedido).

**A régua que manda:** mede comparando com o típico do PERFIL DELE, nunca com benchmark de fora. Um gargalo por vez, um experimento por vez.

---

## Por que o story funciona (a doutrina, em 4 linhas)

Carrossel e Reel atraem público novo. O Story trabalha quem já está dentro: aquece, qualifica e fecha. Não é placeholder nem vlog. É sistema de conversão, e cada frame tem função única. O arco do dia reorganiza uma percepção e termina apontando pro método, mesmo quando um frame isolado é leve. Story que só "engaja" sem filtrar nem aquecer falhou tanto quanto a oferta crua jogada às 8h da manhã.

**O que esta skill faz por você:** monta a sequência de stories que aquece e converte quem já te segue. Ela tem 4 sistemas e escolhe com você o certo pro teu objetivo: **CARO** (a rotina diária que sustenta tudo), **Caixinha Estratégica** (planta pergunta e lê quem quer comprar), **Sequência de Venda de 5 dias** (campanha pra vender uma oferta), **Story Infiltrado** (atrair gente nova). Story é canal de venda diária, não enfeite.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa de você o objetivo e o contexto antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: confere se tem a fala/o número/o case antes de montar e, se faltar, marca `[DADO: confirmar]` no lugar do furo e diz o que falta, jamais preenche com algo plausível; (6) **doc de output enxuto pros 2 leitores**: o que sai é otimizado pro humano que lê E pra IA que recebe como contexto: só os stories limpos + `[DADO: confirmar]`, zero meta-narração. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar qualquer frame que vá pro público.**

## Output Contract (o que você entrega)
- A **sessão de stories** pedida, **frame a frame numerado**, cada frame com **tipo CARO marcado** (C/A/R/O) ou **dia da Sequência (1-5)**, e indicação de **texto na tela · áudio · sticker · visual**.
- Você entrega **um bloco por vez** (a rotina CARO do dia, OU um dia da Sequência, OU a campanha dividida por dia), **mostra, e PARA** pro cliente aprovar antes do próximo.
- Cada frame que afirma tese ou que tem CTA passa pelo gate, mas **o gate roda por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída.
- Você **nunca inventa fala nem número do cliente** e **nunca mostra frame que falhou no gate**.

## Passo 0, ancora antes de escrever (NÃO PULE)
Procura a fonte de fala real do cliente, nesta ordem: **descrição do projeto** → **Plano colado na conversa** → **mensagens anteriores**. Puxa **3-5 falas de DOR + 3-5 de DESEJO** do tema, literais, contando o N. A primeira linha do arco (e a pergunta da Caixinha) nasce de uma delas, quase intacta.

Três estados de entrada (declara qual é o seu antes de escrever):
- **Tem fala real (com N):** ancora nela e cita o N. Caminho ideal.
- **Tem nicho/fundação mas ZERO fala literal:** NÃO inventa fala nem N. Cada frame ancora em **prova real do autor** (print, case, mecanismo); qualquer número não confirmado entra como `[DADO: confirmar]` e **NÃO conta como Ancorada=✓**. Avisa: minerar 5-8 falas reais (ou rodar o Plano na soft-plano-posicionamento) deixa o arco muito mais cravado.
- **Sem nicho e sem nada:** pergunta numa única mensagem (nicho em 1 linha + 1 dor real que o cliente fala) e segue daí.

A fundação (quando existe, do Plano): tese central · top 3 inimigos nominais · lista do "não defendo" · cliente em uma frase.

## Passo 1, confirma a headline e o tipo de pedido
**Antes de tudo, o pedido é CONSTRUIR ou DIAGNOSTICAR?** Se é diagnóstico (os stories não convertem, as métricas caíram), pula a construção: vai pra `references/algoritmo-e-metricas.md` (protocolo de diagnóstico), nomeia **UM gargalo** (completion, exit por frame, story-to-DM) + **UM experimento de 7 dias**, nunca 5 fixes de uma vez. Mede comparando com o típico do TEU perfil, não com benchmark de fora. Se é construir (o caso normal), segue abaixo.

O arco do dia precisa de um eixo. Se a HEADLINE/abertura já foi escolhida, constrói os frames a partir dela. Se não tem eixo do dia, você escreve AQUI mesmo, pela régua de título que esta skill carrega (3 aberturas da dor ancorada, o dono crava UMA), não inventa um eixo morno. Quem quer um banco maior de variações pode passar pela soft-conteudo-headlines, mas isso é opção.

**Puxa o objetivo de quem pediu antes de escolher o sistema** (Lei 3, consultiva): o que você quer com esses stories, vender uma oferta, demonstrar hoje uma consultoria, aquecer a base, abrir vaga, ou ler quem quer comprar? O objetivo decide o sistema. Se a pessoa já trouxe o contexto ("quero uma sequência pra vender X"), usa direto; se veio vago, pergunta UMA vez. Decide qual sistema o pedido pede (são camadas, não estilos):

| Sistema | Função | Quando entra |
|---|---|---|
| **CARO** | Rotina diária, o chão | Sempre. Sem ele rodando há semanas, o resto vira spam |
| **Caixinha Estratégica** | Planta pergunta + lê intenção de compra | 2-3x/semana |
| **Sequência de Venda (5 dias)** | Campanha pontual de conversão | Vagas abertas, lançamento, push |
| **Story Infiltrado** | Tráfego frio (gente que não te segue) | Só quando tem verba pra iterar |

Ordem: primeiro garante o eixo (sem eixo do dia, você escreve AQUI pela régua desta skill, como diz o início deste passo). Com o eixo na mão, se o pedido for ambíguo pergunta UMA vez; CARO é o default quando o cliente só diz "stories de hoje".

## Passo 2, monta o arco do sistema certo

**Régua de teto por bloco (benchmark Storrito 2026):** arco com 1-3 frames por movimento fecha com completion de 75%; bloco com 7+ frames seguidos derruba pra 50%. Regra: bloco enxuto, 1-3 frames por movimento do arco, e nunca 7 ou mais frames em sequência sem uma virada (novo movimento, pergunta, prova ou CTA).

**CARO, a rotina do dia (3-7 frames).** Quatro tipos, cada um com função. A Oferta só entra se couber na regra (não abre o dia, máx 2-3x/semana).
- **C, Caixinha.** Pergunta plantada, ligada ao método ou à dor real do cliente, nunca genérica ("me conta de você"). A resposta vira pauta amanhã e revela intenção de compra. Tipo mais importante: prova competência E abre CTA natural.
- **A, Alinhamento.** Visual real do especialista vivendo o que prega. Subtexto, nunca promessa. Mantém a tese viva nos dias sem oferta. Sem CTA. Aceita sticker discreto (poll/emoji/slider).
- **R, Resultado.** Prova: print de pagamento, áudio de cliente, bastidor de entrega. Print + 1 frase de contexto basta. Sobe pro destaque "Resultados".
- **O, Oferta.** CTA direto, 3 linhas: problema → entrega → *"Direct 'PALAVRA'"*. Nunca o primeiro do dia, máx 2-3x/semana. **Hierarquia na correria: C > A > O > R.**

**Sequência de Venda (5 dias).** A Fórmula 7 esticada em 5 dias, cada dia um objetivo, na ordem que leva o lead de frio a decidido. A progressão é a regra: cada dia avança, não repete o apelo do anterior.

| Dia | Tipo | Objetivo |
|---|---|---|
| 1 | Resultado forte | Prova social, cria desejo |
| 2 | Diagnóstico do problema | O lead se reconhece |
| 3 | Método em ação | Mostra a FUNÇÃO, nunca a execução |
| 4 | Objeção antecipada | Derruba a dúvida que segura a compra |
| 5 | Urgência + CTA | Fecha a janela |

Urgência no Dia 1 é desespero (ninguém tem desejo ainda); urgência no Dia 5 é fechamento. Palavra-chave única apontando sempre pro mesmo Direct.

**Caixinha Estratégica.** A versão deliberada do C: planta 1 pergunta que o cliente certo responde (Problema · Objeção · Detalhamento), e a resposta volta como conteúdo qualificado E sinal de compra. A resposta certa não é pitch: é continuar a conversa no DM, no ritmo da pessoa.

**Story Infiltrado.** Único que mira público frio. Parece orgânico: roda lógica de Resultado/Alinhamento sem cara de anúncio (sem "saiba mais", sem CTA, foto real). Cobra teste pra valer, não é onde se começa sem verba.

## Passo 3, escreve frame a frame (cada um com função)
Cada frame: **observação → interpretação → tese curta ancorada**. Parte do que se vê (o print, a cena real), interpreta sob a lente da percepção, fecha numa tese ancorada em chão (print, número, cena), nunca opinião solta. Estilo Soft: uma ideia por frame, número no lugar de adjetivo, vocabulário do cliente final (nunca "lead/funil/ticket" no texto), tom de comando nunca de súplica (*"Direct 'MÉTODO'"*, nunca *"você gostaria de…"*). Front-load: o primeiro frame decide se a pessoa continua, é o print ou a tese, não enrolação. **CTA é DM com palavra-chave, nunca link externo** (o algoritmo penaliza link). **Não narra o fluxo** ("agora vou montar a oferta"), só entrega limpo.

Formato de entrega (copiável):
```
### Frame N, [tipo CARO: C/A/R/O  ou  Dia N da Sequência]
**Texto na tela:** [o que aparece]
**Áudio/narração:** [se tiver]
**Sticker:** [poll/quiz/slider/emoji/question box, ou nenhum]
**Visual:** [foto real/vídeo/print/fundo]
```

## Passo 4, roda o GATE por dentro (auditoria silenciosa, NÃO imprime)

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Em stories, o título é o valor de `Texto na tela`, e só ele.** Rótulo de frame (`Frame 1`), nome de dia (`Dia 2`) e cabeçalho de arquivo nunca entram: eles não aparecem na tela pra quem assiste, e incluí-los infla a contagem com linhas que nunca competiram por atenção. Monte o `titulos.txt` por comando, nunca a olho:

```
grep -h '^\*\*Texto na tela:\*\*' <arquivos da sequência> | sed 's/^\*\*Texto na tela:\*\* //'
```

Cole a saída e cole `frames na sequência: N · linhas em titulos.txt: N`, os dois iguais. O script reprova com exit 1 quando mais de um terço das linhas do `titulos.txt` casar com `^(Frame|Slide|Dia|Peça|Bloco) *[0-9]`: isso é rótulo de estrutura entrando no lugar do texto que o público lê.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** **A classificação vale para a FALA, não só para o nome:** anonimizar resolve a identidade e não resolve a origem, e uma frase literal vinda de call ou de caixa de entrada continua sendo conversa privada mesmo sem nome. Liste as falas atribuídas a terceiros na peça, uma por linha, na forma `<fala literal> | origem: <arquivo:linha> | classe: prova declarada ou conversa privada | como aparece na peça: <"uma aluna", "uma seguidora", "alguém que me procurou">`. Fala de conversa privada com pessoa em negociação aberta só entra como "alguém que me procurou" ou equivalente que não afirme compra; "uma aluna", "uma cliente" e "antes de entrar" afirmam a compra e reprovam. Feche com `falas de terceiro na peça: N · de conversa privada apresentadas como aluna: 0`. Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Palavra-chave de CTA não se inventa, e a grafia é literal.** Antes de escrever qualquer CTA que peça uma palavra ("manda X no Direct", "comenta Y", "envia Z no WhatsApp"), procure a palavra nos insumos do dono (transcrição, peça pronta, mensagem, site) e cole `palavra-chave: <literal> | origem: <arquivo:linha>`. Use a grafia EXATA, sem espaço a mais nem a menos: uma palavra com espaço é outra palavra para quem digita e para a automação que responde, e a lead cai em lugar nenhum. **Sem origem no disco, é PROIBIDO escolher uma:** escreva o CTA na versão que dispensa a palavra ("me chama no Direct e eu te mando") e leve a pergunta ao handoff. Marcar a incerteza no relato e publicar a palavra assim mesmo reprova, porque o dono publica sem perceber. **Quem confere é o script, não a memória:** `python3 scripts/checar_titulos.py --peca <todos os arquivos da sequência> --insumos <pasta de insumos do dono> --perfil <perfil>` extrai as palavras em caixa alta dos CTAs, cruza com o grep nos insumos e sai com exit 1 em `palavra-chave inventada: <X>`. Cole a linha `palavra-chave: <literal> | origem: <arquivo:linha>`, ou `palavra-chave: nenhuma (CTA sem palavra)`.

**A ressalva entra UMA vez na SEQUÊNCIA, nunca uma por dia.** A peça é a sequência inteira, nunca o arquivo do dia: a seguidora que vê a mesma frase em cinco dias seguidos para de lê-la, e é exatamente quem precisa dela que deixa de ver. A ressalva clínica ou regulada sai no ÚLTIMO frame do ÚLTIMO dia. Passe todos os arquivos da sequência em `--peca` com `--ressalva "<a frase>"`, e a soma impressa tem que dar 1; cole a linha ao lado da contagem.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

Roda o gate em CADA frame que afirma tese ou tem CTA **internamente** (Alinhamento leve sem tese e foto-bastidor não precisam). Só bloco com VEREDITO=PASSA vai pro cliente. Uma falha refaz aquele frame (não o arco). A tabela abaixo é o teu **checklist interno**, nunca a saída: o cliente recebe só os frames limpos (Passo 5), jamais a tabela.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorada** | a fala/print nasce da fonte real (cita N **real**) OU de prova real do autor; **N inventado/plausível = ✗ automático**; toda aspa é verbatim literal do cliente | |
| **Sistema CARO** | o arco do dia tem C/A/R e a Oferta só se couber (NÃO abre o dia, máx 2-3x/semana); hierarquia C > A > O > R respeitada; se nenhum frame planta/posiciona/prova/converte, é vlog de creator = ✗ | |
| **Caixinha filtra** | a pergunta plantada é ligada ao método/dor real e a resposta revela intenção de compra; pergunta genérica que só "engaja" = ✗ | |
| **Sequência progride** | cada dia AVANÇA o lead (prova → diagnóstico → método → objeção → urgência); dia que repete o mesmo apelo do anterior = ✗; urgência só no Dia 5 | |
| **Oferta não-crua** | o story de oferta vem aquecido por C+A+R (ou pelos dias anteriores), 3 linhas com contexto; "vaga aberta, me chama" sem contexto = ✗ | |
| **CTA com destino** | DM com palavra-chave ÚNICA apontando pro mesmo Direct; link externo = ✗ | |
| **Front-load** | o primeiro frame é o print/tese, não enrolação; abre direto | |
| **C/U/B** | não é **C**onfuso (uma ideia por frame), não é ina**U**creditável (promessa que o leitor não engole; o frame fecha em chão real), não é **B**oring/chato (tem tensão ou cena, não é morno) | |
| **As 3 perguntas, dá pra ver?** | fecha o olho e enxerga a cena/print. ✗ "tenha mais clareza" · ✓ "o print da agenda lotada na segunda" | |
| **As 3 perguntas, dá pra falsificar?** | é fato falsificável, não adjetivo | |
| **As 3 perguntas, só você diz?** | o concorrente direto não assina igual (cena/mecanismo proprietário, não promessa banal do nicho) | |
| **Anti-IA (HARD)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz, o verbo que rima com "cravar" e suas flexões (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype (o "revoluciona/transforma" e o próprio verbo-freio banido). **No chat (sem o lint), faz um CTRL+F manual do travessão longo (U+2014) e a família do verbo-freio banida antes de marcar ✓.** | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

## Passo 5, mostra e PARA
Mostra **só os frames que passaram, LIMPO**, no doc, em bloco (a rotina do dia, OU um dia da Sequência). Sem tabela de gate, sem meta. Pergunta "esse arco te serve? ajusto, sigo pro próximo dia, ou paro?". **Espera a aprovação** antes de gerar o próximo bloco ou a campanha inteira. Não despeja os 5 dias de uma vez.

## Um dia completo da Sequência de Venda, no formato exato da entrega

Caso fictício, nicho neutro: uma consultora de organização financeira pra clínicas pequenas.
Mecanismo dela (fictício): **Método dos 3 Envelopes**. Oferta: programa de 8 semanas, 12 vagas.
Palavra-chave: **ENVELOPES**. Abaixo, o **Dia 4 (objeção antecipada)**, que é o dia que mais se erra.

### Frame 1, Dia 4 da Sequência
**Texto na tela:** "Eu não tenho tempo pra mais um sistema."
**Áudio/narração:** "Essa foi a primeira coisa que a última pessoa que entrou me falou. E ela tinha razão de falar."
**Sticker:** nenhum
**Visual:** print de uma mensagem real recebida `[DADO: confirmar: autorização de uso do print]`

### Frame 2, Dia 4 da Sequência
**Texto na tela:** "Quanto tempo você gasta hoje procurando quanto sobrou?"
**Áudio/narração:** "Ela me disse: umas duas horas por semana, entre extrato, planilha e o WhatsApp do contador. Todo mês a mesma coisa, e no fim ela ainda não sabia o número."
**Sticker:** enquete, "2 horas" ou "mais que isso"
**Visual:** fundo liso, texto grande

### Frame 3, Dia 4 da Sequência
**Texto na tela:** "A separação leva 40 minutos. Uma vez."
**Áudio/narração:** "Os três envelopes se montam uma vez. Depois disso a pergunta 'quanto sobrou' tem resposta no dia 5, sem procurar nada."
**Sticker:** nenhum
**Visual:** ela na mesa, papel e caneta, sem tela

### Frame 4, Dia 4 da Sequência
**Texto na tela:** "Não é mais um sistema. É o fim da procura."
**Áudio/narração:** "Se o que você tem hoje já te dá o número no dia 5, não entra. Sério. Isso aqui é pra quem gasta duas horas por semana pra não descobrir."
**Sticker:** nenhum
**Visual:** ela falando direto pra câmera

### Frame 5, Dia 4 da Sequência
**Texto na tela:** "Restam 5 das 12 vagas."
**Áudio/narração:** "Direct ENVELOPES que eu te explico como fica no teu caso."
**Sticker:** nenhum
**Visual:** print do quadro de vagas `[DADO: confirmar: número real de vagas no dia da postagem]`

**O que rodou por dentro:** a primeira versão do Frame 4 dizia "não perde essa chance, as vagas estão
acabando". Urgência no Dia 4 é desespero, a urgência é do Dia 5. Reescrita como filtro ("se o que
você tem já resolve, não entra"), que qualifica em vez de empurrar. A tabela do gate não foi impressa.

## O que esta skill NÃO faz (e pra onde vai)

Esta skill escreve os FRAMES e para aí. Em toda rota abaixo, se a skill de destino não estiver instalada, esta faz o mínimo aqui e diz o que fez.

| O pedido é | Vai pra | Se não estiver instalada |
|---|---|---|
| A **headline/gancho/abertura** isolada, que vem ANTES | **soft-conteudo-headlines** | escreve 3 aberturas no teto do topo de story e pede pro dono cravar UMA |
| Os **slides do carrossel** | **soft-conteudo-carrossel** | entrega só os frames e diz que o carrossel é outra peça |
| O **roteiro falado** de reel | **soft-conteudo-reels** | entrega só os frames e avisa |
| Levar a peça pra **LinkedIn, X, YouTube, e-mail** | **soft-conteudo-multiplataforma** | entrega só a versão de story e diz que a adaptação fica pendente |
| Decidir **sobre o que postar** (tema da semana ou do mês) | **soft-conteudo-planner** | pergunta o tema ao dono e segue com o que ele disser |
| **Arte, PNG, visual** dos frames | **soft-designer** | entrega só o texto e a sugestão de visual em palavras |
| **Posicionamento, bio, destaques, mecanismo** | **soft-plano-posicionamento** | roda a entrevista curta de 4 perguntas acima e marca `[DADO: confirmar]` |
| A **conversa de venda** depois que o lead chega no direct | **soft-vendas-closer** | entrega o frame de CTA e diz onde a conversa começa |
| **Carta, VSL, página** | **soft-funil-carta** / **soft-funil-landing** | escreve só os frames e aponta o que falta |

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Oferta abrindo o dia ou todo dia | Oferta nunca é o primeiro frame; máx 2-3x/semana; aquece com C+A+R antes |
| Caixinha genérica ("me conta de você") | Pergunta ligada ao método/dor real, que filtra e revela intenção de compra |
| Sequência repetindo o mesmo apelo todo dia | Cada dia avança: prova → diagnóstico → método → objeção → urgência; urgência só no Dia 5 |
| Story de oferta cru ("vaga aberta, chama") | 3 linhas com contexto (problema → entrega → Direct 'PALAVRA'), aquecido pelos dias/frames anteriores |
| CTA em link externo | DM com palavra-chave única; o algoritmo penaliza link |
| Arco que não aponta pro método (virou vlog) | Cada frame planta, posiciona, prova ou converte; senão corta |
| Inventou um número/fala "plausível" | Só número/fala REAL; sem fonte, marca `[DADO: confirmar]` e não conta como Ancorada=✓ |
| Despejou os 5 dias de uma vez | Um bloco por vez, com gate, e PARA pra aprovar |
| Narrou o fluxo ("agora vou montar a oferta") | Não narra: executa em silêncio e entrega só o frame limpo |
| Entregou só CARO quando o objetivo era vender | Puxa o objetivo (Lei 3) e escolhe o sistema certo: Sequência de 5 dias pra campanha, Caixinha pra ler intenção |
| Imprimiu a tabela do gate na saída | O gate é INTERNO (auditoria silenciosa); a saída é só a peça limpa |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `shared-references/crivo/07-regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta (a entrada do dono, as perguntas feitas e a saída real de cada ação). **Leia antes da primeira pergunta.**
- `references/sistema-caro.md`: CARO frame a frame, 5 ângulos de Alinhamento, 4 tipos de Resultado, 4 modelos de Oferta, banco de fotos, rotina semanal baseline.
- `references/caixinha-estrategica.md`: 3 tipos de pergunta plantável, estrutura da resposta em 3-4 frames, banco por nicho, frequência.
- `references/sequencias-de-venda.md`: variações da Sequência de 5 dias por ticket e formato (auditoria, evento, alto ticket, remarketing, híbrido), roteiros preenchidos, erros fatais.
- `references/story-infiltrado.md`: tráfego frio, 5 ângulos canônicos, régua de verba e decisão em 3 dias, métricas-âncora.
- `references/algoritmo-e-metricas.md`: benchmarks 2026 (completion >60%, exit por frame, story-to-DM), Highlights como ativo permanente, protocolo de diagnóstico. **Dirigida no ramo de diagnóstico do Passo 1.**
- `references/camadas-conciencia.md`: as 3 camadas de atração aplicadas ao story (Caixinha aberta serve C1 alcance · Caixinha respondida densifica C2 convicção · Resultado serve C3 prova viva). Lê quando precisar decidir a função do arco no funil.
- `scripts/lint_copy.py`: quando há shell disponível, roda `python3 scripts/lint_copy.py` nos frames como cinto extra do anti-IA (reprova o travessão longo U+2014 e o verbo-freio banido). No chat não roda, por isso o CTRL+F manual do gate.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** a sequência sai em **um arquivo por dia**, `stories-<slug>-<AAAA-MM-DD>.md`, mais **um** `stories-<slug>-arco.md` com a visão da semana inteira (o arco, o papel de cada dia e a virada entre eles). Slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras. Os dois formatos saem sempre juntos: o arquivo do dia é o que se abre na hora de postar, e o arco é o que mostra pra onde a semana caminha. Checagem verificável antes de fechar: conte os arquivos gravados; são os dias da sequência mais 1. Sequência inteira num arquivo só, ou dias sem o arco, reprova a entrega.
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
