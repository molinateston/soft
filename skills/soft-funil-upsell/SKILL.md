---
name: soft-funil-upsell
description: >-
  Projeta a MÁQUINA DE UPSELL de uma oferta, o que vende DEPOIS que a venda principal já fechou: o order bump (checkbox no checkout, antes do comprar), o upsell pós-compra (a oferta de um clique, sem novo checkout) e o downsell (a alternativa mais barata quando a pessoa recusa). Entrega a estrutura das três peças mais a copy de cada uma, pronta pra montar no checkout, sempre como continuação lógica do que a pessoa acabou de comprar. Use quando o pedido for: "monta o upsell", "order bump", "oferta pós-compra", "downsell", "aumenta o ticket médio", "one-click upsell", "add-on no checkout", "o que ofereço depois que a pessoa compra". NÃO use pra: a oferta principal, o stack, a ancoragem e a garantia da venda-mãe (soft-plano-ofertas); a régua de e-mail depois da isca (soft-funil-nutricao); a carta de vendas ou o roteiro de VSL (soft-funil-carta e soft-funil-vsl); a página de checkout em si como arquitetura visual (soft-funil-landing). Leia e siga o fluxo inteiro do SKILL.md.
---

# A máquina de upsell, o que vende depois que a venda já fechou

A venda principal fecha e a pessoa está no ponto mais quente que vai estar: cartão na mão, decisão tomada, confiança no alto. A máquina de upsell aproveita esse instante pra aumentar o valor de cada cliente sem gastar mais um centavo pra atrair ninguém. Ela vem depois da oferta principal e parte de quem já disse sim, oferecendo o próximo passo lógico sem tentar convencer de novo.

São três peças, cada uma num momento próprio do checkout:
- **Order bump:** um checkbox no checkout, ANTES do botão de comprar. A pessoa marca e o add-on entra no mesmo pagamento. Pré-compra.
- **Upsell:** a oferta que aparece DEPOIS que o pagamento passou, aceita com um clique, sem novo checkout. Pós-compra.
- **Downsell:** a alternativa mais barata que aparece SE a pessoa recusa o upsell. Uma saída sem culpa, não uma insistência.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem o arquivo da máquina de upsell MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Toda headline de peça carrega tese, nunca rótulo.** O texto do order bump, o título do upsell e o do downsell passam pela régua de títulos: cada um afirma alguma coisa que a pessoa entende de cara, jamais um rótulo fino ("Oferta especial", "Upgrade", "Não perca"). O lugar que a pessoa lê no instante da decisão recebe a frase mais concreta do material. Cole `peças de copy: N · com tese no título: N`, iguais.

**A âncora manda: quem não sabe o que a pessoa acabou de comprar não tem como desenhar a continuação lógica.** O order bump, o upsell e o downsell nascem TODOS da oferta principal (a venda-mãe, que é da soft-plano-ofertas). Cada peça é o próximo passo natural de quem comprou aquilo, nunca um produto solto. Cole `peças na máquina: N · ancoradas na oferta principal: N · aleatórias: 0`. Peça que sobrevive trocada pra outra oferta qualquer vira enchimento, e volta pro passo de desenho.

**A regra de ouro do one-click é um PASSO com saída obrigatória, e o gate a cobra.** O upsell é aceito com um clique porque o cartão já foi capturado na compra principal. No instante em que a oferta faz a pessoa digitar o cartão de novo, deixa de ser upsell e vira uma segunda venda, que converte muito pior: a fricção mata o upsell. O order bump entra no mesmo pagamento (a pessoa nem sai da tela). Cole `peças pós-compra: N · com aceite de um clique: N · que pedem cartão de novo: 0`. Qualquer peça pós-compra que exija novo checkout reprova a entrega.

**Número de mercado é referência, nunca promessa ao dono.** As `references/` trazem números reais de mercado (por exemplo, a fatia da receita da Amazon que vem de upsell e cross-sell, ou a faixa de aceite de order bump entre criadores de curso). Esses números entram no material como referência de mercado, com a fonte ao lado, e NUNCA viram promessa de resultado pro dono ("você vai faturar 35% a mais"). Cole `números de mercado citados: N · apresentados como referência: N · apresentados como promessa ao dono: 0`.

**Zero dado inventado.** Nome de produto, preço, bônus e prova só entram se vierem do perfil do dono ou do que ele colou. O que falta vira `[A CONFIRMAR: o quê]`, sem valor assumido, e a peça não sai como pronta. É proibido inventar preço, número ou nome de produto e etiquetar.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra o fluxo inteiro num caso fictício de nicho neutro: a oferta principal, a escada de continuação, e o bump, o upsell e o downsell montados com a copy de cada um. `references/estrutura-upsell.md` é a referência de método (bump contra upsell contra downsell, one-click, a escada de continuação).

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você me diz qual oferta a pessoa acabou de comprar e eu monto o order bump, o upsell e o downsell). Se quiser ser guiado passo a passo (te pergunto o que preciso pra máquina, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o brain do dono mais o que ele colou. Se faltar o insumo que a máquina não vive sem (qual é a oferta principal já vendida), pergunta AQUELE insumo e segue, sem abrir briefing inteiro.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o levantamento curto uma pergunta de cada vez, e monta a máquina com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda a máquina (qual é o próximo passo lógico, o que vira upsell e o que vira bump, o preço do downsell), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a montar sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("qualquer coisa a mais serve de upsell", "põe um desconto"), não segue com o genérico. Pede o concreto que só o dono tem: o que o cliente que comprou aquele produto pede logo depois, a dúvida que sempre aparece no pós-venda, o add-on que a pessoa já perguntou se existe. Isso vira a âncora da escada; resposta rasa vira produto aleatório.

**Oferece refinar no fim (parte 4):** depois de mostrar a máquina, fecha com UMA linha: "Quer outro upsell? Um downsell mais barato? Um bump diferente? Me diz o que ajustar que eu refaço só essa peça." A oferta de refino não substitui o STOP nem o gate.

## Contrato de saída (o que sai, e onde cai)

- **Um arquivo `.md` nomeado**, salvo no disco: `maquina-upsell-<produto>.md`, com a estrutura das três peças, a copy de cada uma e onde cada uma entra no checkout. Se o ambiente renderizar markdown, mostre também.
- **A máquina sai com as três peças na ordem do checkout:** order bump (antes do comprar), upsell (pós-compra, um clique), downsell (se recusa). O dono pode pedir só uma; nesse caso as outras saem como "não incluído nesta rodada" com o motivo em 1 linha.
- **Preço de cada peça é decisão declarada, jamais um default silencioso.** Quando o perfil traz o preço da oferta principal, a máquina ancora os preços do bump, do upsell e do downsell nele, e mostra a conta. Preço que o perfil não traz vira `[A CONFIRMAR: preço]`, nunca um número plausível.
- **Entrega etapa por etapa**, com parada pro OK a cada uma. Nunca despeja a máquina inteira de primeira.
- **Nunca inventa produto, prova ou número.** Sem insumo real, o campo sai como `[A CONFIRMAR: o quê]` e a peça não sai como pronta.
- **O arquivo é publicável e não tem seção de bastidor, nem marcada.** Pendência, decisão de preço e nota de configuração vão em `notas-confirmacao.md`, entregue ao lado.

## Roteamento: o dono pediu X, você entra na fase N

| O dono pediu | Entra na fase |
|---|---|
| "monta o upsell", "o que ofereço depois que a pessoa compra", sem detalhe | **0 · A ÂNCORA**, depois **1 · A ESCADA** |
| "faz um order bump", "add-on no checkout" | **1** focada no bump, depois **2** |
| "faz um downsell", "uma versão mais barata pra quem recusa" | **1** focada no downsell, depois **2** |
| "aumenta o ticket médio dessa oferta" | **0**, depois **1** e **2** com as três peças |
| "olha esse upsell aqui e diz o que está errado" | **GATE** em modo auditoria, devolve o diagnóstico por peça |

Pedido ambíguo ("quero vender mais pra quem já comprou"): pergunte UMA coisa só, **"qual oferta a pessoa acabou de comprar?"**, e a resposta abre a máquina.

## Como ler cada fase

Toda fase traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro**, com os passos numerados e **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a fase precisar da oferta principal, do avatar, do ticket, dos bônus ou da prova: leia do perfil/brain do agente quando existir; se não existir, faça o levantamento curto do "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

---

## Fase 0 · A ÂNCORA (roda antes de tudo, não pula)

**O que faz:** descobre a oferta PRINCIPAL que a pessoa acabou de comprar. É a base de continuação lógica de tudo que vem depois.

**Precisa de:** a oferta-mãe (do perfil do dono ou da soft-plano-ofertas): o nome do produto, o que ele entrega, o ticket, os bônus e a promessa. Sem saber o que a pessoa comprou, não dá pra saber o que ela naturalmente quer a seguir.

**Sem o insumo:** três estados, declare o seu em 1 linha.
- **Tem a oferta principal completa no perfil:** ancora nela e segue.
- **Tem o produto e o ticket, faltam os bônus ou a promessa:** ancora no que há, marca o resto `[A CONFIRMAR: o quê]`.
- **Não sabe qual é a oferta principal:** pergunte numa mensagem só (qual produto, quanto custa, o que promete) e siga. A máquina de upsell não avança sem a âncora.

**Entrega:** nada de arquivo. É a base das fases 1 e 2.

**Leia primeiro:** `references/estrutura-upsell.md` (a seção da escada de continuação).

---

## Fase 1 · A ESCADA (o próximo passo lógico depois da compra)

**O que faz:** monta a escada de continuação: qual o próximo passo lógico de quem comprou a oferta principal (isso vira o upsell), qual a versão mais barata do mesmo desejo (o downsell) e qual o add-on que combina com o carrinho (o order bump).

**Precisa de:** a âncora da Fase 0, mais o que o dono sabe do comportamento pós-compra do cliente (o que ele pede depois, a dúvida que sempre volta).

**Sem o insumo:** sem o comportamento pós-compra, use a lógica da continuação a partir da própria oferta (comprou o programa, o próximo passo é o acompanhamento; comprou o protocolo, o add-on que combina é o material que apoia a execução) e diga isso em 1 linha. Nunca invente um produto que o dono não tem: se o upsell natural não existe no catálogo, marque `[A CONFIRMAR: existe esse produto?]` e leve ao handoff.

**A escada, as três peças:**

| Peça | O que é | Nasce de |
|---|---|---|
| **Order bump** | add-on pequeno que combina com o carrinho, marcado num checkbox antes do comprar | o complemento natural do que está sendo comprado, barato o bastante pra ser decisão de impulso |
| **Upsell** | o próximo passo lógico, uma oferta maior ou mais completa, aceita com um clique depois da compra | o desejo que a compra principal acabou de abrir (comprou a entrada, quer o aprofundamento) |
| **Downsell** | a versão mais barata ou parcial do upsell, oferecida só a quem recusa | o mesmo desejo do upsell, num tamanho que cabe em quem disse não ao preço cheio |

**A continuação é sempre LÓGICA (o princípio de Brunson).** O order bump e o upsell vendem quando são a continuação natural do que a pessoa já colocou no carrinho, jamais um produto solto. O teste: se a peça faz sentido depois de QUALQUER compra, ela virou enchimento e sai. Quem comprou um curso recebe como upsell o acompanhamento daquele curso, jamais um segundo curso de outro assunto.

**Entrega:** a escada mostrada pro dono, as três peças nomeadas com o motivo da continuação. **STOP.**

**Leia primeiro:** `references/estrutura-upsell.md`.

---

## Fase 2 · A COPY DE CADA PEÇA (o que a pessoa lê no checkout)

**O que faz:** escreve a copy das três peças, cada uma pela régua Soft, e diz onde cada uma entra no checkout.

**Precisa de:** a escada aprovada na Fase 1.

**Sem o insumo:** não há copy sem a escada aprovada.

**A copy de cada peça:**

| Peça | A copy | Onde entra no checkout |
|---|---|---|
| **Order bump** | UMA frase no checkbox, com o benefício concreto e o preço do add-on ("adiciona o cardápio da semana por mais R$ X") | no checkout, logo acima do botão de comprar, antes do pagamento |
| **Upsell** | a oferta pós-compra com o MOTIVO da continuação ("você acabou de garantir X, e quem faz X empaca em Y; o acompanhamento resolve Y"), o preço, e o aceite de um clique | na tela que aparece DEPOIS que o pagamento passa, com um botão de aceitar e um de recusar |
| **Downsell** | a alternativa sem culpa ("não quer o completo agora? leva a versão essencial por menos"), sem insistir nem envergonhar | na tela que aparece SE a pessoa recusa o upsell |

**A régua Soft vale em cada peça:** zero dado inventado, headline autoexplicável, uma ideia por frase, sem frase-emoldura, sem hype. O order bump é a peça mais curta do funil e cada palavra conta: benefício e preço, nada mais.

**O downsell não humilha.** A alternativa barata é uma saída digna, uma porta de tamanho menor pra quem disse não ao preço cheio. Downsell que trata a recusa como erro queima a confiança que a compra acabou de construir.

**Entrega:** `maquina-upsell-<produto>.md`, com as três peças, a copy de cada e onde cada uma entra. **STOP.**

**Arquivos obrigatórios: o arquivo acima, e `conferencia/checagem-titulos.md` por último** (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`). Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/EXEMPLO-FIM-A-FIM.md` (a máquina montada de ponta a ponta) e `references/copy-e-taticas-upsell.md` (a sequência emocional de 5 passos da página de upsell, o valor percebido, as regras táticas e os canais e-mail e WhatsApp).

---

## O GATE (roda por dentro, e não imprime)

**O que faz:** reprova a máquina que não serve, antes de o dono ver. Serve também como modo auditoria, quando o dono cola um upsell pronto.

**Precisa de:** as peças escritas.

**Régua de títulos (vale em todo título de peça).** O texto do order bump, o título do upsell e o do downsell passam pela régua (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega.** Ele fecha com `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`, os dois primeiros iguais.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega aparece nela ou tem o motivo da exclusão declarado. Liste os dados, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0`. Qualquer dado em `sem destino` reprova. O piso é CONTADO (`grep -c '^- ' <perfil>`), com a saída colada.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de produto, número ou prova só entra se veio do dono, do insumo dele, ou de uma busca deste turno com o comando registrado. Memória de treino não é fonte. Sem isso, o campo sai como `[A CONFIRMAR: o quê]`.

**O veredito é o PIOR item.** Um ✗ refaz a peça que falhou.

| Check | Passa se |
|---|---|
| **Ancorada na oferta principal** | cada peça é continuação lógica do que a pessoa comprou, não um produto aleatório; peça que serve pra qualquer compra reprova |
| **One-click respeitado** | o upsell é aceito com um clique, sem novo checkout; peça pós-compra que pede cartão de novo reprova na hora |
| **Continuação, não catálogo** | o upsell é o próximo passo do desejo aberto pela compra, não uma oferta de outro assunto |
| **Downsell sem culpa** | a alternativa barata é uma saída digna, longe de uma insistência que envergonha |
| **Número de mercado é referência** | todo número de mercado entra com a fonte ao lado e como referência, nunca como promessa de resultado ao dono |
| **Zero inventado** | nome de produto, preço e prova vêm do perfil ou do insumo; o que falta é `[A CONFIRMAR]`, nunca um plausível |
| **Headline autoexplicável** | o texto do bump, do upsell e do downsell afirma o benefício de cara, sem rótulo fino |
| **Preço coerente** | o preço de cada peça é ancorado no da oferta principal, ou marcado `[A CONFIRMAR: preço]` |
| **Anti-IA (duro)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype |
| **Roda nos 2 motores** | a máquina não depende de recurso de um motor só; a lógica vale em Claude e em Codex |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ refaz. Só tudo ✓ vai pro dono |

Com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` sobre cada arquivo gravado. Sem shell, faça a busca manual pelos dois bloqueios duros antes de marcar o anti-IA.

**Entrega:** nada em modo normal (auditoria silenciosa, a tabela **nunca** vai pra saída). Em modo auditoria, entrega `diagnostico-upsell.md` com a peça, o check que falhou e a correção.

---

## O FECHO (mostra e para)

**O que faz:** entrega a máquina limpa e o comentário de configuração.

**Entrega:** só o arquivo (ou a etapa pronta), sem tabela de gate, sem meta, mais uma linha sobre como montar cada peça no checkout (onde colar o bump, como configurar a tela de upsell de um clique, onde entra o downsell). Pergunta "essa te serve? ajusto?" e **espera o OK** antes de seguir pra próxima etapa ou variação.

---

## O que esta skill NÃO faz

Cada rota é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| A oferta principal, o stack, a ancoragem, a garantia da venda-mãe | **soft-plano-ofertas** | uso a oferta principal como âncora, não a desenho |
| A régua de e-mail depois da isca | **soft-funil-nutricao** | não faço |
| A carta de vendas ou o roteiro de VSL | **soft-funil-carta / soft-funil-vsl** | não faço |
| A página de checkout como arquitetura visual | **soft-funil-landing** | digo onde cada peça entra, não desenho a página |
| A arte, o visual, o PNG da tela de upsell | **soft-designer** | entrego o `.md` com a copy, sem o visual |
| A conversa de venda, a objeção ao vivo | **soft-vendas-closer** | não faço |

## Anti-patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Despejou a máquina inteira de primeira | Volta: âncora, escada, copy, parando a cada etapa |
| O upsell é um produto de outro assunto | Reescreve a partir do desejo que a compra principal abriu |
| O upsell pede o cartão de novo | Vira aceite de um clique; senão é segunda venda e converte pior |
| Inventou um produto que o dono não tem | Marca `[A CONFIRMAR: existe esse produto?]` e leva ao handoff |
| Usou o número de mercado como promessa ao dono | Volta a ser referência, com a fonte ao lado |
| O downsell insiste ou envergonha | Vira saída digna, sem tratar a recusa como erro |
| Order bump com rótulo fino ("Oferta especial") | Reescreve com benefício e preço concretos |
| Narrou o fluxo ("agora vou montar o downsell") | Executa em silêncio e entrega o resultado |
| Imprimiu a tabela do gate | O gate é interno |

## Transversais

`references/estrutura-upsell.md` (bump contra upsell contra downsell, one-click, a escada de continuação) · `references/copy-e-taticas-upsell.md` (a sequência emocional de 5 passos da página, o framework de valor percebido, as regras táticas testadas, os 3 tipos de oferta e os canais e-mail e WhatsApp de recuperação pós-PIX) · `references/EXEMPLO-FIM-A-FIM.md` (a máquina inteira num caso fictício) · `references/fontes-do-metodo.md` (as fontes confirmadas) · `shared-references/crivo/` · `scripts/lint_copy.py` · `scripts/checar_titulos.py` · `shared-references/filtro-anti-ia/` (a régua anti-IA escrita, pro motor que não roda o lint).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `maquina-upsell-protocolo.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`**, e feche com `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`. Como o relatório é escrito por último, rode o lint nele depois de terminar de escrevê-lo.
- **Sem sandbox (a régua escrita, quando o lint não roda).** Motor sem shell não executa `scripts/lint_copy.py`, e isso não dispensa o anti-IA: aplique a régua no olho por `shared-references/filtro-anti-ia/padroes-banidos.md`, padrão por padrão, e passe cada reprovação por `shared-references/filtro-anti-ia/falsos-positivos.md` antes de mandar o trecho de volta pro passo de escrita, porque prosa autoral do dono cai no mesmo crivo e some se ninguém conferir. A entrega sai do mesmo jeito, no melhor que esse motor alcança, e o relato fecha com uma linha dizendo que a conferência anti-IA foi no olho, sem código: `anti-IA: conferido no olho pela régua escrita (sem shell nesta rodada)`. Calar o que ficou de fora reprova a entrega; declarar em uma linha reprova nada.
- **Configuração do dono fora da pasta da skill.** Perfil ou arquivo do dono nunca é gravado dentro da pasta desta skill; vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
