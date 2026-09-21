---
name: soft-funil-vsl
description: >-
  Escreve o ROTEIRO DE VÍDEO DE VENDAS (VSL) no arco de 19 blocos de Jon Benson, mas só depois de LEVANTAR toda a munição: quem é o cliente dos sonhos (Dream Buyer Avatar de Sabri Suby), em que nível de consciência ele está (Eugene Schwartz), a USP, o mecanismo, a oferta com equação de valor, as provas reais e as objeções. A VSL não escreve uma linha antes da munição estar completa. Use quando o pedido for "faz uma VSL", "roteiro de vídeo de vendas", "script do meu vídeo de vendas", "roteiro pra gravar meu vídeo que vende", "video sales letter". NÃO use pra a carta escrita em texto corrido pra ler no celular (soft-funil-carta); o mini-webinar com filtro e virada (soft-funil-miniwebinar); a página que hospeda o vídeo (soft-funil-landing); a régua de mensagens pós-isca (soft-funil-isca); o webinar completo (soft-webinar); carrossel, reel e headline solta (soft-conteudo-*); a conversa de venda ao vivo (soft-vendas-closer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Roteiro de VSL, o vídeo que vende antes da conversa

A VSL é a carta de vendas falada. Ela filtra, explica e constrói desejo em vídeo, e entrega o lead quente pro comercial. Ela nasce PERFEITA por um motivo só: a fase de levantamento vem antes da escrita, e a VSL não escreve uma linha até a munição estar completa. Vídeo que começa a roteirizar sem saber quem é o cliente dos sonhos e em que nível de consciência ele está vira discurso genérico e queima o tráfego.

**A alma desta skill é o levantamento.** Roteiro bom não é bom porque a estrutura é boa; é bom porque a munição por trás de cada bloco é real e cavada fundo. Sabri Suby chama de Halo Strategy: pesquisa obsessiva do cliente ANTES de escrever, minerando a fala real dele (dor, medo, desejo na língua dele). Schwartz decide COMO abrir pelo nível de consciência. Benson dá a estrutura. As três fontes estão confirmadas em `references/fontes-do-metodo.md`, e nenhuma fonte nova entra fora dela.

**A carta faz o TEXTO escrito, esta skill faz o ROTEIRO DE VÍDEO.** A migração da VSL pra cá é oficial: a soft-funil-carta continua com a carta em texto corrido lida em silêncio; o roteiro de vídeo de vendas mora aqui, com a fase de levantamento que a carta não tem.

**O que é "pronto" nesta skill (vale pra toda entrega).** A entrega só existe quando a pasta de saída tem os 3 arquivos de entrega (o roteiro, o dossiê de munição, a versão teleprompter) MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída>` devolve exit 0. A última linha dessa saída vai colada no relato. Todo arquivo de conferência mora em `conferencia/`; na pasta de saída o dono vê os 3 entregáveis e o handoff. O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**A regra que não se dobra: ZERO dado inventado.** Nenhuma fala, nenhum caso, nenhum número, nenhuma fonte entra sem origem no perfil do dono, nos insumos dele, ou nas 3 fontes confirmadas. Furo vira `[A CONFIRMAR: o quê]`, nunca invenção plausível. Número marcado `[A CONFIRMAR` no perfil não entra no roteiro nem com ressalva ao lado; a fala usa a forma sem prazo e o número fica só no dossiê.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra o fluxo inteiro no caso fictício da Renata (Studio Base 40): o pedido, as 3 fases de levantamento, o STOP de munição completa, o roteiro dos 19 blocos e um trecho na versão teleprompter.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Pra sair perfeita, esta VSL levanta tudo antes de escrever. Te guio passo a passo pelo levantamento (te pergunto uma coisa de cada vez), ou puxo do seu brain o que já tem e só pergunto o que faltar? Do jeito que você preferir, a escrita só começa com a munição completa.

- **Modo direto** (default, e o que roda no silêncio): puxa o avatar, a consciência, a USP, o mecanismo, as provas e as objeções do brain do dono e do que ele colou. Se faltar um insumo que a VSL não vive sem, pergunta só AQUELE e segue. Não abre entrevista inteira.
- **Modo guiado**: só quando o dono pede. Faz o levantamento das 3 fases uma pergunta de cada vez, esperando a resposta antes da próxima.

**Ensina enquanto faz (parte 2):** em cada escolha que muda o roteiro (o nível de consciência que decide a abertura, a temperatura do tráfego que decide o comprimento, a USP, o bloco de abertura), escreve UMA linha do porquê na voz de quem ensina o método, pro dono aprender a calibrar sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("meu cliente quer resultado", "o público de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: a frase literal que uma cliente falou na dor, um caso real com número, o print de uma objeção. Verbatim real vira a âncora do roteiro; resposta rasa vira roteiro raso. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar o roteiro, fecha com UMA linha: "Quer mais curto? Outra abertura? Mais suave no pitch? Me diz o que ajustar que eu refaço só esse bloco." A oferta de refino não substitui o STOP nem o gate.

## Contrato de saída (o que sai, e onde cai)

Três arquivos `.md` na pasta de saída, salvos no disco. Se o ambiente renderizar markdown, mostre também.

- **(a) O ROTEIRO completo**, `roteiro-vsl-<produto>.md`: os 19 blocos em ordem, com marcação de tempo por bloco, pronto pra gravar. Cada bloco puxa a munição da fase certa.
- **(b) O DOSSIÊ de munição**, `dossie-municao-<produto>.md`: o avatar preenchido, o nível de consciência declarado, a USP e o mecanismo nomeados, o banco de provas reais, o banco de objeções. É a prova de que a munição estava completa antes da escrita.
- **(c) A versão TELEPROMPTER**, `teleprompter-<produto>.md`: só a fala, em frases curtas, sem marcação técnica de tempo nem nome de bloco, pronta pra rolar na tela enquanto o dono grava.

Regras que valem nos 3:
- **Entrega etapa por etapa**, com parada pro OK a cada fase. Nunca despeja o roteiro inteiro de primeira.
- **Preço no roteiro é decisão declarada.** Quando o perfil traz o preço, o pitch (bloco 13) o mostra com a equação de valor ao lado. Só omite quando o dono pede ou quando o destino é qualificação por conversa, e nesses casos cola a linha `preço omitido por: <motivo>`.
- **O roteiro é arquivo que vira gravação e não tem seção de bastidor.** Pendência, decisão editorial e recado ao dono vão pro handoff, nunca pra fala que o dono lê no teleprompter.

## Roteamento: o dono pediu X, você entra na fase N

| O dono pediu | Entra na fase |
|---|---|
| "faz uma VSL", "roteiro de vídeo de vendas", "script do meu vídeo" | **FASE 0 · LEVANTAMENTO**, e segue o fluxo inteiro |
| "já tenho o avatar e a oferta, só monta o roteiro" | confirma a munição no **STOP**, e se estiver completa entra na **FASE 3** |
| "olha essa VSL e diz o que está errado" | **FASE 4 · GATE** em modo auditoria, devolve o diagnóstico por fase |

Pedido ambíguo ("preciso de um vídeo de vendas"): confirme UMA coisa, **"é um vídeo curto direto ou uma VSL completa que constrói o argumento?"**, e siga. VSL completa entra aqui; vídeo com filtro e virada é o mini-webinar.

## Como ler cada fase

Toda fase traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro**, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a fase precisar de avatar, mecanismo nomeado, voz, oferta ou prova: leia do perfil/brain do agente quando existir; se não existir, faça a pergunta curta do "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

**Levantamento BLOQUEANTE antes de escrever (o STOP de munição em forma verificável, e é COMANDO, nunca de memória).** Antes de escrever o roteiro, LEIA o perfil e os insumos do dono e cole no dossiê uma linha por dado-chave, nesta forma: `<campo> | <valor encontrado> (<arquivo>:<trecho>) | ou [A CONFIRMAR] só se o ls/leitura devolveu vazio`. Os campos-chave: avatar, nível de consciência, USP nomeada, mecanismo nomeado, oferta com preço, as 3 provas reais, as objeções. **Marcar `[A CONFIRMAR]` um dado que EXISTE no insumo reprova a entrega**, então rode a leitura antes de decidir e cole a saída. A tabela fecha com `campos-chave: N · encontrados no insumo: N · [A CONFIRMAR] com leitura vazia comprovada: N`, e a soma fecha em N. É esta tabela que o STOP de munição confere.

**O exemplo é ILUSTRATIVO, é PROIBIDO parafrasear.** `references/EXEMPLO-FIM-A-FIM.md` usa a Renata (nicho fictício) só pra mostrar a FORMA. É proibido reusar as frases, os números ou o nicho dela na peça real: parafrasear o EXEMPLO em vez de gerar do insumo do dono reprova a entrega. O roteiro real nasce 100% do insumo do dono; se você se pegar copiando uma frase do exemplo, pare e volte ao insumo.

---

## FASE 0 · LEVANTAMENTO (quem é o cliente dos sonhos)

**O que faz:** monta o Dream Buyer Avatar e minera a fala real do cliente. É a fundação. Sem ela, nada avança.

**Precisa de:** o brain do dono, os insumos dele (transcrições, caixa de entrada, reclamações, comentários) e, no modo guiado, as respostas das 9 perguntas do avatar.

**Sem o insumo:** sem nenhuma fonte de fala real, pergunte numa mensagem só (quem é o cliente em 1 linha, 1 dor real na boca dele, o que ele já tentou) e siga, marcando o que faltar.

**Entrega:** o avatar preenchido e o mapa de fala (dor, medo, desejo na língua do cliente), mostrado pro dono. É a base do dossiê.

**Leia primeiro:** `references/fase-0-2-levantamento.md` (as 9 perguntas do Dream Buyer Avatar de Suby e a Halo Strategy) · `shared-references/crivo/01-entrada-verbatim.md`.

O **Dream Buyer Avatar** (Suby) responde 9 perguntas sobre a rotina, o medo, a esperança e a linguagem exata do cliente. A **Halo Strategy** (Suby) minera onde o cliente fala de verdade (nos insumos do dono, no brain, nos comentários) e traz a dor, o medo e o desejo nas palavras dele, não nas suas. A abertura da VSL vai nascer de uma dessas falas, quase intacta.

---

## FASE 1 · BÚSSOLA (consciência, sofisticação, temperatura)

**O que faz:** decide COMO abrir e QUÃO longo o vídeo é. Este é o passo que Schwartz governa.

**Precisa de:** o avatar da Fase 0 · o nível de consciência do lead · a saturação do mercado · a temperatura do tráfego.

**Sem o insumo:** sem o dado de consciência, **PARA e pergunte só isso**: "quem vai assistir já sabe que tem esse problema, já sabe que existe solução, ou já te conhece?". Sem temperatura declarada, assuma **frio** (o caso mais exigente) e declare a premissa em 1 linha.

**Entrega:** 1 linha declarada antes de escrever: `consciência: Z → sofisticação: S → temperatura: T → abertura: <qual bloco 1 e 2 usam> → comprimento: Q`. **STOP.**

**Leia primeiro:** `references/fase-0-2-levantamento.md` (os 5 níveis de consciência de Schwartz com o que cada um muda na abertura, a sofisticação de mercado, e a temperatura de tráfego de Suby).

Os **5 níveis de consciência** (Schwartz) decidem por onde a VSL abre: quem nem sabe que tem o problema abre pela cena e pelo mecanismo do problema; quem só falta a oferta abre pela oferta na cara. A **sofisticação de mercado** decide se a promessa basta ou se precisa de mecanismo novo. A **temperatura** (Suby: frio, morno, quente) decide o comprimento: tráfego frio pede vídeo mais longo, tráfego quente pede curto.

**Duração por consciência, em minutos** (afina a régua da temperatura): super informado 5-7 · solution-aware ~10 · problem-aware 15-30 · zero-aware 30-45. Detalhe em `references/playbook-vturb-vsl.md` (2.10).

**Ticket decide o canal (destino comercial), declare aqui.** VSL de tráfego frio vende bem até R$1.000 (faixa praticada R$197-697); acima de R$1.000 o destino é lançamento/webinar OU uma VSL que só QUALIFICA pra call. Régua e o ramo call funnel em `references/playbook-vturb-vsl.md` (2.9).

---

## FASE 2 · MUNIÇÃO (a matéria-prima de cada bloco)

**O que faz:** levanta os cinco carregadores que os 19 blocos vão puxar, tudo do perfil do dono, zero inventado.

**Precisa de:** o avatar e a bússola das fases anteriores, mais o perfil e os insumos do dono.

**Sem o insumo:** cada carregador que faltar vira `[A CONFIRMAR: o quê]` e entra no STOP como furo. Nunca invente USP, mecanismo, prova ou objeção.

**Entrega:** os cinco carregadores documentados, mostrados pro dono. **STOP** no checklist da próxima seção.

**Leia primeiro:** `references/fase-0-2-levantamento.md` (o detalhe de cada carregador) · `references/banco-de-objecoes.md` (as objeções clássicas e o bloco que quebra cada uma).

Os cinco carregadores:
- **USP** (Benson): a proposta única de venda, nomeada, que aparece cedo (bloco 2).
- **Mecanismo do problema e da solução:** a causa-raiz oculta que exonera o lead, e o método nomeado que resolve. O formato deste carregador é a **One Belief** (Evaldo Albuquerque), uma crença única na frase-molde "fazer [ação] é a chave para [desejo], possível através de [mecanismo nomeado]", preenchida pelos 4 campos da Arquitetura da Esperança. Sem essa frase o STOP não passa. Molde, campos e os 3 testes em `references/playbook-vturb-vsl.md` (2.2).
- **Oferta com equação de valor** (Hormozi, já no brain): sonho vivido vezes probabilidade percebida, dividido por tempo e esforço. Quanto mais alto o de cima e mais baixo o de baixo, mais irresistível.
- **Banco de provas reais:** casos, números e depoimentos documentáveis do dono. O piso é 3.
- **Banco de objeções:** as objeções clássicas mapeadas, cada uma com o bloco que a quebra.

---

## STOP · A MUNIÇÃO ESTÁ COMPLETA?

**O que faz:** o portão bloqueante. A VSL não escreve uma linha enquanto este checklist tiver furo aberto. É a alma da skill em forma de porta fechada.

Passa só quando TODOS estes estão preenchidos com dado real:

| Munição | Passa quando |
|---|---|
| **Avatar preenchido** | as 9 perguntas do Dream Buyer respondidas com fala real, não genérico |
| **Consciência definida** | um dos 5 níveis de Schwartz declarado, mais a temperatura do tráfego |
| **USP e mecanismo nomeados** | a USP tem nome próprio; o mecanismo do problema e o da solução têm nome próprio |
| **Provas reais** | no mínimo 3 provas documentáveis do dono, com número literal do perfil |
| **Objeções mapeadas** | as objeções clássicas listadas, cada uma ligada ao bloco que a quebra |

**Furo vira `[A CONFIRMAR]`, nunca invenção.** Um carregador vazio não vira uma prova plausível nem um caso genérico: vira uma linha de pendência no dossiê e uma pergunta ao dono no handoff. Só passa completo. Munição furada gera roteiro furado, e o gate no fim reprova de qualquer jeito, então o furo custa menos aqui.

**STOP.** Mostre o checklist preenchido pro dono antes de escrever.

---

## FASE 3 · ESCREVE (o arco de 19 blocos)

**O que faz:** escreve o roteiro inteiro na voz do cliente, seguindo os 19 blocos. Benson dá a estrutura; Schwartz calibra a abertura pelo nível de consciência da Fase 1; cada bloco puxa a munição da fase certa.

**Precisa de:** a munição completa aprovada no STOP.

**Sem o insumo:** não há escrita sem STOP aprovado. Se o dono mandou pular pra cá, volte e feche a munição primeiro.

**Entrega:** o roteiro dos 19 blocos com marcação de tempo, mostrado pro dono. **STOP.**

**Leia primeiro:** `references/os-19-blocos.md` (cada bloco: o que é, o que faz, de qual fonte vem, um exemplo curto ancorado na Renata, e o erro clássico).

Os 19 blocos, na ordem:

1. **Quebra de padrão** (snap suggestion, pattern interrupt) · Benson
2. **Ponto-chave de comunicação** (escolha um, pela consciência) · Schwartz decide qual
3. **Frase de conexão** entre o bloco 2 e a promessa
4. **Quebre as primeiras objeções** (cedo)
5. **Gatilho de curiosidade mais chamada** (open loop)
6. **Apresentação do herói** (reluctant hero, nightmare story) · Benson
7. **Pivote o foco**
8. **Ponto de conexão com o cliente dos sonhos** (dream buyer) · Suby
9. **A grande descoberta** (dream story, o mecanismo) · Benson
10. **Apresente a solução**
11. **Prova social**
12. **Preparação pro pitch**
13. **Pitch** (quebra de padrão, provas, revelação de elementos, chamada, com a equação de valor de Hormozi)
14. **Garantia**
15. **Dualidade** (comprar contra não comprar, escolha seu lado)
16. **Call to action**
17. **Escassez e urgência** (só se a razão existe)
18. **Mostre como será o processo da compra**
19. **Última call to action**

**A abertura muda pela consciência.** Os blocos 1 e 2 não são fixos: o nível de Schwartz declarado na Fase 1 decide se a VSL abre pela cena do problema (baixa consciência) ou pela oferta direta (alta consciência). Escrever a mesma abertura pra todo público é o erro que a Fase 1 existe pra matar.

**Ordem de ESCRITA é o inverso da ordem de LEITURA.** Produza nesta sequência: munição (STOP) → tese/mecanismo → oferta → história → lead por último (o bloco mais sensível e o mais testado). O roteiro final continua na ordem dos 19 blocos; só a ordem de produção muda. Consenso do playbook, detalhe em `references/playbook-vturb-vsl.md` (2.1).

**Escreva 3 leads desde o dia 1 (checagem que CONTA os leads e reprova abaixo de 3).** A lead (blocos 1 a 5) é a variável que mais decide entre lucro e prejuízo: entregue 3 versões, uma clonando a estrutura do benchmark e duas variando só os elementos de prova e a ordem deles, com o resto da copy idêntico. Uma rodada entregou 1 lead onde a FASE 3 pede 3. Regra dura: **o roteiro sai com 3 leads rotuladas** (`### Lead A`, `### Lead B`, `### Lead C`, ou equivalente) e menos de 3 reprova a fase. Antes de fechar, conte e cole: `grep -ciE '^#+ *lead [ABC]|lead (a|b|c|1|2|3)\b' <roteiro>`, e escreva `leads entregues: N · exigidas: 3 · abaixo de 3? sim/não`. `sim` volta pra escrita. Tipos de lead e a fórmula de variação em `references/playbook-vturb-vsl.md` (2.7).

**Bloco 6 (história do herói): a jornada vem do insumo ou não existe (regra dura, zero invenção).** A apresentação do herói puxa a história real do dono, da transcrição, do perfil ou do brain. Uma rodada inventou biografia ("por muito tempo eu recebia a mesma pergunta") sem nenhum lastro no insumo: isso é dado inventado e reprova. Regra: cada fato da história (o que o herói vivia, o que sentiu, o ponto de virada) sai com origem apontada no insumo, ou o bloco marca `[A CONFIRMAR: história do herói]` no dossiê e a peça usa SÓ o que é real, sem preencher o vão com jornada plausível. **NUNCA invente a trajetória do herói.** Checagem antes de fechar: para cada afirmação biográfica no bloco 6, aponte ao lado a linha do insumo (`<arquivo>:<trecho>`) que a sustenta; afirmação sem origem apontada reprova a entrega inteira. Cole `afirmações biográficas no bloco 6: N · com origem apontada: N · sem lastro: 0`.

---

## FASE 4 · GATE (a régua que reprova antes de o dono ver)

**O que faz:** reprova o roteiro que não serve, antes de o dono ver. Serve também como modo auditoria, quando o dono cola uma VSL pronta.

**Precisa de:** o roteiro escrito.

**Entrega:** nada em modo normal (auditoria silenciosa, a tabela nunca vai pra saída). Em modo auditoria, entrega `diagnostico-vsl.md` com o bloco, o check que falhou e a correção.

**Leia primeiro:** `shared-references/crivo/03-gate-cub.md` · `shared-references/crivo/07-regua-de-titulos.md`.

**Verificador de lastro (obrigatório antes de pronto).** Depois de o gate passar e ANTES de dizer pronto, roda o segundo par de olhos de `shared-references/crivo/10-verificador-lastro.md`: cego ao roteiro, no papel de verificador, confere cada afirmação (aspa, número, história, fato de produto, promessa) contra o insumo do dono e conserta ou remove o que estiver sem lastro. Sem a tabela `afirmação | lastro ou REMOVIDA` no bastidor, a peça não está pronta.

Os checks, e o veredito é o PIOR item:

| Check | Passa se |
|---|---|
| **Régua de títulos** | toda abertura, promessa e nome de bloco é autoexplicável e passa no teste do estranho: alguém que caiu no vídeo por acaso entende a promessa sem contexto. Título vago reprova |
| **Slippery slide** (Sugarman) | cada linha puxa a próxima. A primeira frase existe só pra fazer ouvir a segunda. Frase que não puxa a próxima é cortada |
| **Munição completa** | o STOP passou: avatar, consciência, USP, mais de 3 provas, objeções, tudo real |
| **Zero dado inventado** | todo caso e número é verdade documentável do perfil. Sem prova, o trecho está `[A CONFIRMAR]` e a peça não sai como pronta |
| **3 leads entregues** (BLOQUEANTE) | o roteiro sai com 3 leads rotuladas. `grep -ciE '^#+ *lead [ABC]|lead (a\|b\|c\|1\|2\|3)\b' <roteiro>` maior ou igual a 3. Menos de 3 reprova a FASE 3 |
| **História do herói com lastro** (BLOQUEANTE) | cada afirmação biográfica do bloco 6 tem origem no insumo, ou o bloco está `[A CONFIRMAR: história do herói]`. Biografia inventada (jornada sem lastro) reprova a peça inteira |
| **Consciência casada** | a abertura escrita bate com o nível declarado na Fase 1 |
| **Cada objeção quebrada** | cada objeção do banco foi endereçada em algum bloco. Objeção mapeada e não quebrada reprova |
| **Equação de valor no pitch** | o bloco 13 mostra sonho e probabilidade em cima, tempo e esforço em baixo |
| **Convite único** | UM destino comercial coerente do bloco 16 ao 19 |
| **Anti-IA (duro)** | zero travessão longo · zero da família do verbo-freio banida pela régua · sem frase-emoldura · sem verbo-clichê de hype |
| **Roda nos 2 motores** | o roteiro é neutro de motor, escrito pra rodar igual no Claude e no Codex |
| **VEREDITO** | o PIOR item acima. Um item reprovado refaz o bloco. Só tudo aprovado vai pro dono |

Com shell, rode o lint em `scripts/lint_copy.py` sobre cada arquivo. Reprovou, refaz o bloco e roda de novo.

---

## FASE 5 · FECHO (mostra e para)

**O que faz:** entrega os 3 arquivos limpos e o comentário de gravação.

**Entrega:** os 3 entregáveis (roteiro, dossiê, teleprompter), sem tabela de gate, mais uma linha sobre como gravar (onde entra a marcação de tempo, como usar o teleprompter). Pergunta "esse te serve? ajusto?" e **espera o OK** antes de seguir pra variação.

**Grava lo-fi primeiro, produção só depois de validar.** No comentário de gravação, oriente a primeira versão crua (celular ou webcam, 1 luz) só pra testar se a copy converte; produção pesada vem depois de validado, nunca antes. Detalhe em `references/playbook-vturb-vsl.md` (2.13).

**Prova forte descartada se declara na própria entrega.** Se um caso ou número real do dono existia e ficou de fora, declare em 1 linha por quê, dentro do dossiê. O dono precisa ver a ausência sem abrir o relato.

---

## O que esta skill NÃO faz

Cada rota é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Carta de vendas em texto corrido pra ler no celular | **soft-funil-carta** | não faço; a fronteira é firme, aqui é roteiro de vídeo |
| Vídeo curto com filtro e virada de decisão | **soft-funil-miniwebinar** | escrevo o roteiro como VSL curta de autoridade |
| Página que hospeda o vídeo (hero, seções, botão) | **soft-funil-landing** | entrego o roteiro e, no máximo, o briefing da página |
| Webinar completo ou perpétuo | **soft-webinar-script** | não faço |
| Isca, material gratuito | **soft-funil-isca** | não faço |
| A régua de mensagens que entrega o vídeo | **soft-funil-isca** | escrevo a mensagem de passagem, e mais nada |
| Script da conversa de venda ao vivo | **soft-vendas-closer** | escrevo o convite, não a conversa |
| VSL de qualificação high ticket (o vídeo só agenda a call, o preço fica pra conversa) | escrevo a VSL com CTA de "agende", nunca "compre", e faço o **handoff pro setter em soft-vendas-sdr e o fechamento em soft-vendas-closer** | escrevo a VSL de qualificação e marco o handoff no arquivo de saída |
| Posicionamento, oferta, nomear mecanismo | **soft-plano-posicionamento** | uso a munição da Fase 2 com o que o dono já tem |
| Headline ou gancho isolado | **soft-conteudo-headlines** | escrevo a abertura dentro do bloco 1 |
| Arte, visual, PNG | **soft-designer** | entrego o `.md`, sem o visual |

## Anti-patterns (sintoma, correção)

| Sintoma | Correção |
|---|---|
| Começou a roteirizar sem levantar a munição | Volta pra Fase 0. A VSL não escreve antes do STOP passar |
| Inventou um caso ou número plausível pra encher um carregador | Só prova real. Sem fonte, `[A CONFIRMAR]` e a peça não sai |
| Abriu igual pra todo público | A abertura sai da consciência declarada na Fase 1, não do gosto |
| Despejou o roteiro inteiro de primeira | Volta: levantamento, munição, STOP, roteiro, parando a cada fase |
| Pitch sem equação de valor | O bloco 13 mostra sonho e probabilidade em cima, tempo e esforço em baixo |
| Objeção mapeada e nunca quebrada | Cada objeção do banco fecha num bloco. Sem isso, o gate reprova |
| Múltiplos convites no fim | Um destino comercial só, do bloco 16 ao 19 |
| Roteiro que só roda num motor | Escreve neutro de motor. Roda igual no Claude e no Codex |
| Narrou o fluxo ("agora vou escrever o bloco 6") | Executa em silêncio e entrega o resultado |
| Imprimiu a tabela do gate | O gate é interno |
| Escassez fabricada | Urgência só se a razão existe. Escassez falsa queima a confiança |

## Transversais

`references/fontes-do-metodo.md` (as 3 fontes confirmadas) · `references/fase-0-2-levantamento.md` (o detalhe das 3 fases) · `references/os-19-blocos.md` (cada bloco) · `references/playbook-9-blocos-tecnicas.md` (as 6 técnicas de estrutura e persuasão honesta e os 4 pilares de pré-produção, já com o tom de promessa mágica filtrado; cada técnica encaixa num bloco de `os-19-blocos.md`) · `references/playbook-vturb-vsl.md` (o playbook destilado de 6 podcasts: ordem de escrita, One Belief, estrutura invisível, pontos lógicos, 3 leads, ticket x canal, duração por consciência, call funnel, lo-fi; cada técnica diz em que fase cai, com a régua zero-inventado aplicada) · `references/banco-de-objecoes.md` (as objeções e onde quebram) · `references/EXEMPLO-FIM-A-FIM.md` (o fluxo inteiro na Renata) · `shared-references/crivo/`, `scripts/lint_copy.py`, `scripts/checar_titulos.py` · `shared-references/filtro-anti-ia/` (a régua anti-IA escrita, pro motor que não roda o lint).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras.
- **Lint:** com shell, rode `python3 scripts/lint_copy.py --ignore-code-blocks <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado na saída, o relato incluso, e só declare o gate aprovado depois de exit 0 em cada um. **Cole no relato uma linha por arquivo, no formato `<arquivo>: exit N`.** "Passou no lint" sem o exit colado, arquivo por arquivo, não conta como gate cumprido. A lista fecha com `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Sem sandbox (a régua escrita, quando o lint não roda).** Motor sem shell não executa `scripts/lint_copy.py`, e isso não dispensa o anti-IA: aplique a régua no olho por `shared-references/filtro-anti-ia/padroes-banidos.md`, padrão por padrão, e passe cada reprovação por `shared-references/filtro-anti-ia/falsos-positivos.md` antes de mandar o trecho de volta pro passo de escrita, porque prosa autoral do dono cai no mesmo crivo e some se ninguém conferir. A entrega sai do mesmo jeito, no melhor que esse motor alcança, e o relato fecha com uma linha dizendo que a conferência anti-IA foi no olho, sem código: `anti-IA: conferido no olho pela régua escrita (sem shell nesta rodada)`. Calar o que ficou de fora reprova a entrega; declarar em uma linha reprova nada.
- **Configuração do dono fora da pasta da skill.** Perfil, dossiê ou qualquer arquivo do dono vai pra pasta de trabalho do dono, com o caminho no relato, nunca dentro da pasta desta skill.
