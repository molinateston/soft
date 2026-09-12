---
name: soft-conteudo-planner
description: >-
  Decide SOBRE O QUE postar e entrega o plano de pautas num arquivo .md, em 2 ações: a matriz-calendário do mês (30+ pautas fixas) e o radar da semana (o que está quente agora, datado). Âncora: plano de CONTEÚDO aqui; plano de NEGÓCIO em soft-plano-negocio. Use quando o pedido for: "sobre o que eu posto", "ideias de post", "planeja meu mês de conteúdo", "matriz de conteúdo", "banco de pautas", "calendário de conteúdo", "o que tá em alta no meu nicho", "tendências da semana", "o que tá bombando", "não sei o que postar". NÃO use pra: "não sei o que oferecer de graça" e a escolha da isca (soft-funil-isca); a headline da pauta escolhida (soft-conteudo-headlines); o corpo da peça (soft-conteudo-carrossel, -reels, -stories); adaptar peça pronta (soft-conteudo-multiplataforma); pilares e posicionamento (soft-plano-posicionamento); meta e roadmap (soft-plano-negocio); arte (soft-designer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Planejamento de Conteúdo, o mapa de pautas (matriz + radar)

Esta skill decide SOBRE O QUE postar e entrega o plano num arquivo `.md`. Ela não escreve headline nem peça: entrega pauta pronta pra virar peça. São duas ações, cada uma com uma cadência própria.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**O universo da R3 é o das unidades produzidas, nunca o dos pilares.** As `teses distintas` saem das pautas, headlines ou frames que a peça entrega, e a contagem igual ao número de pilares do dono é resultado inválido. Cole `unidades no lote: N · linhas em teses.txt: N`, os dois iguais, e só então a matriz de pares.

**`teses.txt` é arquivo obrigatório da pasta de saída**, uma tese de até 4 palavras por linha, ao lado do `conferencia/checagem-titulos.md`. Sem ele o gate não calcula a R3 e o campo do fecho sai com a instrução do script no lugar do número, o que reprova a entrega.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra, num caso fictício de nicho neutro, a entrada que o dono deu, as perguntas que a skill fez, uma matriz preenchida de verdade e um radar datado, nos formatos reais da entrega.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola teus pilares e o nicho e eu monto o plano de conteúdo). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra o plano com os pilares que o dono já colou. Se faltar um insumo que o planner não vive sem (os pilares do dono, ou o nicho pro radar varrer), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez (os pilares, o público, o nicho pro radar) antes de montar a matriz ou o radar.

A pergunta do modo é UMA por plano. As outras três partes entram nos passos abaixo:

- **Ensina enquanto faz:** ao cruzar pilar por formato (MATRIZ) ou escolher o ângulo Soft de uma tendência (RADAR), escreve UMA linha do porquê ("puxo esse pilar pro formato Lista porque ele tem muitos exemplos soltos; um pilar de tese única renderia melhor em Problema Solução"), pra o dono planejar sozinho na próxima.
- **Puxa o material bruto:** quando os pilares vierem rasos ("falo de marketing, de vendas"), não segue no genérico. Pede o concreto: "de qual dor real do teu cliente cada pilar nasce, e que frase ele usa pra falar dela?". Pilar ancorado em dor real vira pauta específica; pilar genérico vira pauta genérica.
- **Oferece refinar no fim:** depois de mostrar a matriz ou o radar, fecha com UMA linha de ajuste ("quer mais pautas de um pilar? outro formato dominando o mês? aprofundar uma célula? ajusto só o que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação | Cadência |
|---|---|---|
| "matriz de conteúdo", "planeja meu mês", "banco de pautas", "sobre o que eu posto sempre", "calendário de conteúdo", "não sei o que postar" | **1 · MATRIZ** (o mapa do mês) | **1 vez por mês** |
| "o que tá em alta", "tendências da semana", "o que tá bombando", "sobre o que postar essa semana", "pauta quente", "tem alguma coisa rolando no meu nicho?" | **2 · RADAR** (o pulso da semana) | **1 vez por semana** |

Na dúvida entre os dois, pergunta em 1 linha: "quer o mapa de pautas do mês (fixo) ou o radar do que tá quente essa semana?". **Os dois se complementam:** o radar alimenta a matriz com pauta quente da semana; a matriz é o chão que não depende de tendência. Quem só tem tempo pra uma coisa por mês, faz a matriz.

**Como a marcação de furo funciona nas duas ações:** dado que falta sai como `[A CONFIRMAR]`, sempre com essa grafia, nas duas ações e no doc inteiro. Não existe segunda sintaxe pra isso aqui.

## O perfil do dono vem do banco do agente

Onde esta skill precisa de pilares, avatar, verbatim, tese ou mecanismo: **leia do perfil/brain do agente quando existir**; se não existir, faça a entrevista curta do "Sem o insumo" da ação e siga com o que faltar marcado `[A CONFIRMAR]`. Nunca invente, nunca crie um arquivo de perfil.

---

## Ação 1 · MATRIZ (o mapa de pautas do mês)

**O que faz:** multiplica os pilares do dono em 30 ou mais pautas específicas, cruzando cada pilar por 8 formatos de ataque, e entrega uma matriz-calendário pronta pra escolher.

**Precisa de:** os **3 a 5 pilares** do dono (nome, tema central, valor ancorado, inimigo, formato preferencial), do perfil/brain do agente · o **verbatim de dor e desejo** do avatar, do perfil/brain.

**Sem o insumo:**
- **Pilares não nomeados, mas tem fundação:** propõe 3 ou 4 pilares combinando os 4 tipos (Método, Diagnóstico, Tese, Bastidor) e **PARA pro dono confirmar** antes de montar a matriz. Proposta não é fato.
- **Sem nada:** entrevista curta de 3 perguntas, numa mensagem só. (1) Teu nicho em 1 linha, quem você atende. (2) Os 3 ou 4 assuntos que você mais fala. (3) Uma dor que o teu cliente te fala com as palavras dele. Com isso a matriz sai; o que faltar vira `[A CONFIRMAR]`.
- **Sem verbatim:** ancora em prova ou mecanismo do dono e marca todo número não confirmado como `[A CONFIRMAR]`.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Dia que já passou não recebe pauta.** Antes de montar a matriz, compare a data de hoje com o primeiro dia da janela pedida e escreva `hoje: <dd/mm> · janela pedida: <dd/mm a dd/mm> · dias já vencidos: N`. Os dias vencidos saem da matriz, e a linha que os substitui diz o que fazer com eles em uma frase (repor no fim da janela, ou começar em <dd/mm>). Matriz que abre num dia no passado, sem essa linha, entrega ao dono um calendário que ele não tem como executar.

**Entrega:** `matriz-conteudo-AAAA-MM-DD.md`, com a matriz-calendário em lista por semana e por dia (cada linha: dia, pilar, formato, manchete-pauta), **mínimo 30 pautas**, mais as 3 mais fortes apontadas com 1 linha de porquê cada e a nota de qual pilar ficou raso. **STOP** pra escolha.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Toda pauta da matriz tem dia da semana e data, sem exceção.** Célula sem data reprova a matriz: pauta sem dia não entra em agenda nenhuma e volta pra decisão do dono, que é justamente o que a skill existe pra resolver. Nada de "Extra 1" e "Extra 2" pendurados no fim de uma semana curta pra fechar a conta do mínimo. **Se o mês não comporta o número de pautas que o cruzamento pilares × formatos gerou**, declare a conta e parqueie o resto: `pautas geradas: N · dias disponíveis no mês: M · excedente parqueado pro mês seguinte: N-M`, com o excedente numa seção própria intitulada como excedente, nunca dentro do calendário. Semana curta no fim do mês é semana curta, e sai declarada assim em 1 linha. Checagem colada: `pautas na matriz: N · com dia e data: N · sem data: 0`.

**Leia primeiro:** os Passos 0 a 5 do MODO MATRIZ abaixo (o fluxo é autossuficiente, não precisa de reference pra rodar).

**Profundidade:** `shared-references/filtro-cliente-primeiro.md` (a régua de "isto atrai o cliente certo ou o curioso?") · `shared-references/filtro-anti-ia/` (os padrões banidos que alimentam o check anti-IA).

---

## Ação 2 · RADAR (o pulso da semana no nicho)

**O que faz:** varre a web dentro de uma janela de dias, verifica a data de cada item, e devolve os temas quentes já enquadrados pela tese do dono, prontos pra postar.

**Precisa de:** **nicho + avatar** (obrigatório pra filtrar ruído), do perfil/brain do agente · a **tese e o mecanismo** do dono, do perfil/brain (é o que enquadra a coluna de ângulo) · a **janela** em dias (default 7) · acesso à web, quando a varredura for ao vivo · fontes prioritárias do nicho, opcional.

**Sem o insumo:**
- **Sem acesso à web:** você NÃO finge varredura. Conduz: pede ao dono colar o que ele já viu quente (prints, links, o que os concorrentes postaram) e ORGANIZA na tabela-radar com o ângulo, avisando em 1 linha que a varredura ao vivo roda em ambiente com acesso à web. Radar inventado é pior que radar pequeno.
- **Sem Plano/tese cravada:** roda mesmo assim, e avisa em 1 linha que o ângulo sai mais bruto sem a tese.
- **Sem nicho declarado:** pergunta UMA coisa, e pede específico ("consultor de gestão financeira pra dono de clínica odontológica", não "marketing").
- **Se o feed logado não abre:** cai no fallback de busca web datada, e DIZ o que não deu pra varrer.

**Entrega:** `radar-[nicho]-AAAA-MM-DD.md`, com a linha de cabeçalho datada, a tabela-radar de 10 a 20 temas (menos se o material real for limitado, e você DIZ isso), mais as 3 pautas mais quentes e a nota de quantos itens caíram por falta de data. **STOP** pra escolha.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/protocolo-de-busca.md` (a fonte da verdade da varredura: fontes por tipo, buscas datadas por eixo, verificação de data sem atalho, fallback, régua de saliência).

**Profundidade:** `shared-references/filtro-cliente-primeiro.md` · `shared-references/filtro-anti-ia/`.

---

## As duas ações, por dentro

Ter posicionamento e voz não resolve o "sobre o que eu posto". Essa skill é o PLANEJAMENTO de conteúdo, e ela decide QUAIS temas atacar em **dois modos** que respondem duas perguntas diferentes:

- **MODO MATRIZ (o mapa do mês):** "quais são os temas que EU tenho pra falar sempre?" Pega os pilares do dono (que a **soft-plano-posicionamento** já definiu) e os multiplica em **30+ pautas específicas** cruzando cada pilar por 8 formatos de ataque. É o banco de pautas estável, o calendário do mês, cada célula pronta pra virar peça. É pauta ESTRUTURAL, dura o mês.
- **MODO RADAR (a pauta viva da semana):** "tem alguma coisa quente ROLANDO essa semana que eu posso surfar antes de esfriar?" Varre a web AGORA, pega o que está em alta no nicho (assunto em discussão, formato pegando, gancho viralizando), confere a **data de cada item**, e devolve uma tabela onde a última coluna é o **ângulo do método pronto pra postar**. É pauta PERECÍVEL e datada, descartável na semana seguinte.

**Como escolher o modo (leia o pedido):** "matriz / mapa do mês / banco de pautas / sobre o que eu posto sempre" = MODO MATRIZ. "o que tá em alta / tendências da semana / o que tá bombando / sobre o que postar ESSA semana / pauta quente" = MODO RADAR. Na dúvida entre os dois, pergunta em 1 linha: "quer o mapa de pautas do mês (fixo) ou o radar do que tá quente essa semana?". Os dois se complementam: o radar alimenta a matriz com pauta quente da semana; a matriz é o chão que não depende de tendência.

**O que os dois fazem por você:** transformam tema em pauta específica (manchete que já carrega a tese) e **decidem QUAIS temas atacar**; NENHUM escreve a headline nem o corpo. Cada célula da matriz e cada linha do radar é um input limpo pra soft-conteudo-headlines.

**A fronteira (não invada):** os PILARES e o círculo temático nascem na **soft-plano-posicionamento** (é lá que se decide o universo do que o dono tem permissão de falar). A **Super Pesquisa** (também na soft-plano-posicionamento) é a FUNDAÇÃO estrutural: mercado, força da dor, concorrente por lacuna, verbatim atemporal, feita uma vez, usada o ano. Esta skill MULTIPLICA os pilares em pautas (matriz) e capta o PULSO da semana (radar), nunca refaz a fundação. As skills de peça (carrossel/reel/stories) ESCREVEM a pauta. Se o dono não tem pilares, você não inventa: puxa do Plano ou manda fazer o Plano primeiro.

**As 6 leis (valem nos DOIS modos, detalhe em `shared-references/operacao-padrao.md` Seção 0):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil; (2) abre ensinando o que faz; (3) é consultiva, puxa os pilares (matriz) ou o nicho/janela (radar) antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: no MATRIZ, pilar/fala/número que você não tem vira `[A CONFIRMAR]`, jamais pauta plausível; no RADAR, link/data/número/tendência que você não verificou NÃO entra, item sem data cai; (6) **doc de output enxuto pros 2 leitores**: o que sai (matriz ou radar) serve o humano que planeja E a IA que recebe a célula/linha como contexto da headline.

**Este SKILL.md é o processo inteiro dos dois modos. Identifique o modo primeiro, siga os passos DELE na ordem, pare nos STOPs, e rode o gate por dentro antes de mostrar o doc.**

## Output Contract (o que você entrega, por modo)
**MODO MATRIZ:**
- Uma **matriz-calendário entregue em lista por semana e por dia** (nunca grade de 8 colunas): cada linha traz dia, pilar, formato de ataque e **uma manchete-pauta específica**, não um tema. O cruzamento dos 3-5 pilares pelos 8 formatos de ataque é o método de GERAÇÃO das pautas, não o formato da entrega. Bom: "Os 3 sinais na primeira reunião de que o cliente vai pedir desconto." Ruim: "Fechamento de vendas."
- **Mínimo 30 pautas** (5 pilares × 6 formatos, ou 4 × 8). Toda célula é distinta: a mesma ideia NÃO se repete em dois pilares.
- Cada pauta **nasce de dor/desejo real do avatar** (verbatim quando existe) e **aponta pra uma lacuna que fecha no método do dono**. Pauta que qualquer creator do nicho postaria = reprovada.
- Abaixo da matriz: **as 3 pautas mais fortes** apontadas (com 1 linha de porquê cada) + a nota de qual pilar está mais raso pra pedir mais insumo.
- Você **para e espera** o dono escolher/ajustar antes de gerar volume ou passar uma célula pra headline.
- Você **nunca inventa pilar, fala nem número** e **nunca mostra pauta que falhou no gate**.

**MODO RADAR:**
- **Uma tabela-radar datada.** Primeira linha antes da tabela: `Radar de [NICHO], [DD/MM/AAAA] (janela: últimos [N] dias)`. Depois a tabela com estas colunas exatas: `| Tema quente | Onde está pegando | Fontes/comunidades | Links representativos | Sinais de calor | O que está sendo dito/debatido | Por que importa pro [NICHO] | Ângulo do Método pra postar |`
- **Mire em 10-20 temas.** Menos é aceitável se o material real for limitado; nesse caso você DIZ isso, não enche com item fraco. Melhor 8 temas quentes de verdade que 20 recheados de ruído.
- Cada tema **passou pelo corte de janela** (datado, dentro dos N dias, default 7) e pelo **filtro de saliência** (2+ sinais de calor). Item sem data verificável NÃO entra.
- A coluna **Ângulo do Método** é a que vale ouro: NÃO é gancho genérico de creator, é o tema quente já **enquadrado pela tese/mecanismo do dono**, ancorado na dor do avatar, apontando pro método. É copy embrionária, roda no gate.
- Abaixo da tabela: **as 3 pautas mais fortes** (1 linha de porquê cada) + a nota "[X] itens caíram por falta de data" e o que não deu pra varrer.
- Você **nunca inventa** link, data, número ou tendência. Sem fonte real, o item cai; furo pontual vira `[A CONFIRMAR]`.

## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar o doc no chat)
Regra dura: o RESULTADO é **UM documento markdown consolidado** (a matriz-calendário, ou a tabela-radar). Em ambiente que renderiza markdown, mostre o doc renderizado (o dono abre, copia, planeja/escolhe a pauta); em ambiente com sistema de arquivo, salve um arquivo `.md`; num agente de mensageria, um ARQUIVO cujo path completo vai na resposta. A CONDUÇÃO (puxar pilares ou nicho/janela, os STOPs) acontece no chat; o DOC (matriz ou radar) mora no arquivo. Ao parar num STOP, você mostra/atualiza o DOC e pergunta "ajusto?" (matriz) ou "qual pauta puxo?" (radar); NUNCA reescreve a tabela em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Os 3 ambientes (como a entrega muda, e o alcance do radar)
- **Sem shell (só conversa):** o doc sai como markdown renderizado. Sem tabela em bloco de código (a grade vira texto monoespaçado ilegível): tabela markdown que renderiza. **No RADAR sem navegação ao vivo:** você NÃO finge varredura, CONDUZ: pede ao dono colar o que ele já viu quente (prints, links, o que os concorrentes postaram) e ORGANIZA na tabela-radar com o ângulo do método, avisando que a varredura ao vivo roda em ambiente com shell e acesso à web.
- **Com shell e acesso à web:** salva em `matriz-conteudo-AAAA-MM-DD.md` (matriz) ou `radar-[nicho]-AAAA-MM-DD.md` (radar) na working dir + roda `scripts/lint_copy.py` no doc como cinto anti-IA. **No RADAR:** varredura AO VIVO (buscas datadas + leitura das fontes + verificação de data item a item). Confirma o path.
- **Agente de mensageria (tem shell; busca web quando disponível):** grava o `.md` e devolve **o path completo na resposta**, mais um resumo curto SEM markdown pesado (as 3 pautas mais fortes em texto corrido, sem tabela nem asteriscos). **No RADAR:** igual ao caso acima; se o feed logado (X/Instagram) não abre, cai no fallback de busca web datada + leitura da página e DIZ o que não deu pra varrer.

> Regra de honestidade de tooling (RADAR): se a navegação ao vivo não está disponível ou o feed não abre, você AVISA o que faltou e trabalha com o que dá (busca web datada, ou o que o dono colou). Nunca simula uma varredura que não aconteceu. Radar inventado é pior que radar pequeno.

# MODO MATRIZ, o mapa de pautas do mês
> Escolha este modo quando o pedido é o banco de pautas estável (mês/pilares). Passos 0 a 5 abaixo. Pro pulso da semana, pule pro **MODO RADAR** mais abaixo.

## Passo 0 (MATRIZ), puxa os pilares (NÃO PULE, é a fronteira)
Procura os pilares nesta ordem: **Plano de posicionamento colado na conversa** → **descrição do projeto** → **mensagens anteriores**. Cada pilar do Plano já traz nome, tema central, valor ancorado, anti-valor/inimigo, formato preferencial (é o que a soft-plano-posicionamento entrega).

Três estados de entrada (declara qual é o seu):
- **Tem os pilares (do Plano):** usa eles como as linhas da matriz. Caminho ideal. Puxa junto o verbatim de dor/desejo do Plano pra ancorar as células.
- **Tem nicho/fundação mas pilares não estão nomeados:** propõe **3-4 pilares** derivados da fundação (usando os 4 tipos: Método, Diagnóstico, Tese, Bastidor, descritos no Passo 0.1 logo abaixo) e **PARA pra o dono confirmar** antes de montar a matriz. Não trata proposta como fato.
- **Sem nada:** pergunta numa única mensagem (nicho em 1 linha + os 3-4 assuntos que ele mais fala) e, se o pedido for maior que pauta, avisa que o Plano na **soft-plano-posicionamento** deixa a matriz muito mais cravada.

**Regra de fronteira:** você NÃO define círculo temático nem reescreve posicionamento aqui. Se o dono quer decidir o universo de temas, isso é soft-plano-posicionamento. Aqui os pilares entram como dados de entrada.

### Passo 0.1, os 4 tipos de pilar (só pra propor quando faltam)
Quando você precisa propor pilares (2º estado acima), use combinação destes 4, nunca "motivacional/notícias/vida pessoal" (esses atraem estranho e não filtram): **Método** (o sistema do trabalho, autoridade+venda) · **Diagnóstico** (o problema do cliente visto de perto, identificação) · **Tese/Opinião** (postura contraintuitiva sobre o mercado, diferenciação) · **Bastidor** (rotina/ferramenta/decisão, intimidade controlada). A maioria combina 2-3. Cada pilar proposto tem que ser **inconfundível com o de outro creator** (se o concorrente copia, é genérico, refaz).

**Régua de standalone do Bastidor (o pilar que mais escorrega pro genérico).** Bastidor produz célula vaga com facilidade, porque "mostrar a rotina" convida frase que serve pra qualquer creator. A régua de corte: uma célula de Bastidor só passa se for **inconfundível**, o teste do estranho aplicado ao bastidor. Se a mesma frase, trocado o nicho, serviria pra qualquer outro creator, ela reprova e refaz. O que torna inconfundível: **nomear a ferramenta, a decisão ou o número real** da cena, não a categoria dela.
- ✗ REPROVA (vago, qualquer um assina): "A pergunta que eu faço na primeira reunião e que já muda a resposta do cliente." Qual pergunta? Some a pauta e não muda nada.
- ✓ PASSA (específico, só o dono assina): "A primeira pergunta que eu faço na reunião: 'me mostra o extrato dos últimos 3 meses antes de falar de meta'. Quem empaca aí é quem eu não pego." Nomeia a decisão real e o filtro.

## Passo 1 (MATRIZ), os 8 formatos de ataque (as colunas)
Cada formato é um ÂNGULO diferente de atacar o mesmo pilar. Reescritos na doutrina deste método: todo formato **filtra e atrai o cliente certo** e **aponta pro método**, nunca é jornalismo neutro nem frase de boteco. (Note: o formato "motivacional/inspiração" foi cortado de propósito, atrai estranho e não filtra.)

| # | Formato de ataque | O que a pauta faz | Camada de consciência que serve |
|---|---|---|---|
| 1 | **Acionável** | passo a passo ultra específico que ensina UMA coisa e mostra a lacuna que só o método fecha | quem já sente a dor (C2) |
| 2 | **Diagnóstico** | mostra o problema do avatar visto de perto, nomeia a dor que ele ainda não nomeou | quem não sabe que tem o problema (C1) |
| 3 | **Analítico** | destrincha POR QUE algo funciona/quebra do jeito que funciona (o mecanismo por trás) | quem desconfia mas não entende (C2) |
| 4 | **Contrário** | vira do avesso um conselho aceito do nicho e sustenta o ponto com prova. **Varie a mecânica do contraste:** nem toda célula Contrária usa a forma "não é X, é Y" (vira tique quando concentrado numa coluna só, e o lint conta a estrutura). Alterne com afirmação invertida direta, com pergunta que fura o consenso, com o custo escondido do conselho aceito | quem já tentou o caminho comum e empacou (C3) |
| 5 | **Observação** | uma tendência silenciosa/escondida que o dono notou e ninguém comenta | quem está dentro do universo (C2/C3) |
| 6 | **X vs Y** | compara dois caminhos (método antigo vs o seu, ferramenta vs ferramenta) e mostra o custo do lado errado | quem está decidindo (C3) |
| 7 | **Antes vs Depois** | o estado atual doloroso vs o estado com o método, com o número que prova a virada | quem quer o resultado (C3) |
| 8 | **Lista** | X erros/sinais/passos/itens, cada um uma pauta-semente que rende peça própria | qualquer camada, alto salvamento |

**Como escolher quantas colunas:** 5 pilares × 6 formatos = 30 pautas (corta os 2 formatos que menos servem ao nicho). 4 pilares × 8 = 32. 3 pilares × 8 = 24, então gera 2 pautas em alguns formatos pra fechar 30+. Sempre **mínimo 30**.

## ✍️ PRÉ-FLIGHT DE COPY (relê IMEDIATAMENTE antes de escrever a 1ª linha)
A copy nasce da terça-feira à noite DO LEITOR. Regra é CHECAGEM, nunca geradora: escreve a partir da CENA (a emoção dela: raiva, medo, absurdo, cobiça), com voz de mesa; a regra confere depois. Reprovou, REGENERA do zero (frase editada herda o esqueleto do defeito):
1. **Munição na mão:** verbatim/prova real do dono na frente (sem munição = pergunta, jamais inventa).
2. **Leitura única:** uma leitura em voz alta, sem re-parse; valência única (bom ou ruim na 1ª leitura); sintaxe linear; 1 operação mental por frase.
3. **Mundo do leitor, não o mapa do autor:** componentes do método viram dias, horas, lugares e falas do cliente; rótulo abstrato só entre aspas, como palavra do inimigo.
4. **Compressão gramatical: cota zero.** Verbo da relação por extenso; a força é do fato, nunca do aperto da frase.
5. **Voz de mesa, não palco:** a colocação inteira é fala real; metáfora morta entra, personificação e figura de escritor não.
6. **Prova com atribuição exata** (do banco de provas do dono, nunca fundir); conta apresentada como conta; renda do leitor só em 3ª pessoa.
7. **Anti-IA:** zero travessão longo (U+2014), zero da família do verbo-freio banida, zero verbo genérico de transformação, zero frase-emoldura.
8. **Teto do formato conhecido ANTES** (conta durante, não conserta depois).
Depois de escrita, a auditoria roda TODOS os filtros em cada linha (régua cumulativa, checklist mecânico). Reprovou, regenera ANTES de mostrar.

## Passo 2 (MATRIZ), preenche cada célula com uma manchete-pauta específica
Pra cada cruzamento pilar × formato, escreve **uma manchete-pauta** (não um tema). Regras:
- **Ancora no verbatim** (dor/desejo real do avatar, do Plano). A pauta nasce de uma fala do cliente, quase intacta. Sem fala real: ancora em prova/mecanismo do dono e marca o número não confirmado como `[A CONFIRMAR]`.
- **Aponta pro método:** cada pauta deixa uma lacuna que fecha no que o dono vende. Pauta que resolve tudo de graça e não puxa pro método = jornalismo, reprova.
- **Específica, não tema:** ✓ "O que fazer quando o cliente some depois do orçamento (o roteiro de 2 mensagens)" · ✗ "Follow-up".
- **Distinta entre pilares:** a mesma ideia NÃO aparece em duas células. Se dois pilares puxam a mesma pauta, um dos dois muda de ângulo.
- **Vocabulário do cliente final** (nunca "lead/funil/ticket" na manchete), tom de comando, número em algarismo.
- A célula é curta (uma manchete, não um parágrafo): ela vira o INPUT da soft-conteudo-headlines, que aí escreve 2-3 headlines dentro dela.

## Passo 3 (MATRIZ), roda o GATE por dentro (auditoria interna, NÃO imprime)

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo. **A tabela da régua fecha com três linhas, obrigatórias:** `em molde de antítese: N (teto 1)`, precedida da coluna sim/não com TODOS os títulos listados, inclusive os que dizem não; `com inimigo ou inversão: N de N`; e `teses distintas: N`, com a lista ordenada e comparada. Rode `python3 scripts/lint_copy.py <matriz>` e cole a saída do contador de molde ao lado do número declarado: **o script é a autoridade, e divergência entre o número dele e o declarado reprova o lote.** O contador conta o arquivo inteiro e não separa título de prosa nem de citação da própria checagem, então escreva a triagem ao lado (`saída do lint: N · em manchete: N · repetições de citação: N`). Marque também as 3 melhores com ★ e uma linha de porquê cada.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** **A classificação vale para a FALA, não só para o nome:** anonimizar resolve a identidade e não resolve a origem, e uma frase literal vinda de call ou de caixa de entrada continua sendo conversa privada mesmo sem nome. Liste as falas atribuídas a terceiros na peça, uma por linha, na forma `<fala literal> | origem: <arquivo:linha> | classe: prova declarada ou conversa privada | como aparece na peça: <"uma aluna", "uma seguidora", "alguém que me procurou">`. Fala de conversa privada com pessoa em negociação aberta só entra como "alguém que me procurou" ou equivalente que não afirme compra; "uma aluna", "uma cliente" e "antes de entrar" afirmam a compra e reprovam. Feche com `falas de terceiro na peça: N · de conversa privada apresentadas como aluna: 0`. Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Palavra-chave de CTA não se inventa, e a grafia é literal.** Antes de escrever qualquer CTA que peça uma palavra ("manda X no Direct", "comenta Y", "envia Z no WhatsApp"), procure a palavra nos insumos do dono (transcrição, peça pronta, mensagem, site) e cole `palavra-chave: <literal> | origem: <arquivo:linha>`. Use a grafia EXATA, sem espaço a mais nem a menos: uma palavra com espaço é outra palavra para quem digita e para a automação que responde, e a lead cai em lugar nenhum. **Sem origem no disco, é PROIBIDO escolher uma:** escreva o CTA na versão que dispensa a palavra ("me chama no Direct e eu te mando") e leve a pergunta ao handoff. Marcar a incerteza no relato e publicar a palavra assim mesmo reprova, porque o dono publica sem perceber.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Fontes consultadas (esta skill pesquisa, então a seção é obrigatória).** A seção "Fontes consultadas" da entrega lista só o que foi de fato aberto neste turno, e cada linha traz o comando ou a chamada de ferramenta que abriu aquela fonte. Sem acesso à web no ambiente, a seção diz exatamente "sem acesso à web neste ambiente" e nada mais: nenhum domínio, nenhum nome de marca, nenhuma data de busca. Checagem verificável antes de fechar: conte as linhas da seção e conte os comandos registrados no relatório e escreva os dois números lado a lado, nesta forma: `fontes declaradas: N · comandos no log: N`. **Declarar 4 buscas com 1 comando no log reprova**, e o conserto é apagar as 3 linhas sem comando, nunca inventar o comando. **Cada linha de tabela sobre terceiro traz a consulta que a produziu e o trecho citado da página aberta.** Número (preço, prazo, prazo de entrega, volume, quantidade de alunos, faturamento) vindo de página de terceiro só entra com o trecho colado ao lado; sem trecho colado, o campo sai como `[A CONFIRMAR: exige abrir a página]`, e cravar o número mesmo assim reprova a entrega inteira. Memória de treino e inferência plausível não são fonte.

Roda o gate em CADA célula internamente. Só pauta que passa em TODOS os critérios entra na matriz. Uma falha refaz a célula (não a matriz). A tabela é teu **checklist interno**, nunca a saída.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Específica (manchete, não tema)** | dá pra ver a cena/o número; NÃO é rótulo amplo ("vendas", "mindset") | |
| **Ancorada** | nasce de fala real do avatar (verbatim) OU de prova real do dono; sem fonte, marca `[A CONFIRMAR]` conforme a regra dos 2 tipos de número logo abaixo | |
| **Número classificado** | todo número da célula foi classificado como CENA ou NEGÓCIO, e o de NEGÓCIO sem fonte está marcado `[A CONFIRMAR]` | |
| **Aponta pro método** | deixa lacuna que fecha no que o dono vende; NÃO é conselho neutro que resolve tudo de graça | |
| **Distinta** | essa ideia não aparece em outra célula da matriz | |
| **Cabe no pilar** | responde "por que me seguir / por que comprar de mim" dentro do universo do dono; tema fora do círculo = ✗ (é da soft-plano-posicionamento decidir isso) | |
| **Filtra o cliente certo** | atrai quem compra, não estranho; ✗ pauta viral genérica ("5 hábitos de gente de sucesso") | |
| **Bastidor inconfundível (só pra célula de pilar Bastidor)** | nomeia a ferramenta, a decisão ou o número REAL da cena; a frase, trocado o nicho, NÃO serviria pra qualquer outro creator. ✗ "A pergunta que eu faço na primeira reunião e que muda a resposta do cliente" (some a pauta e nada muda). Célula de Método/Diagnóstico/Tese não roda este check | |
| **Clareza (Lei 1)** | dá pra entender sem já ser de dentro; zero palavra difícil, zero figura vazia | |
| **Anti-IA (HARD)** | zero travessão longo (U+2014) · zero da a família do verbo-freio banida pela régua anti-voz (o verbo que rima com "cravar" e vira emperrar/empacar/parar), em todas as flexões · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype (o "revoluciona/transforma" e o próprio verbo-freio banido) | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ a célula. Só tudo-✓ entra na matriz. | |

**Os 2 tipos de número, e só um deles é marcado.** Antes de fechar cada célula, todo número que aparece nela entra em uma das duas caixas:

- **Número de CENA (ilustrativo).** Serve pra desenhar a situação e não afirma nada sobre o negócio do dono. Idade de personagem, quantidade de itens numa lista de sintomas, "as 3 primeiras semanas", "a segunda reunião", "às 6 da manhã". Este NÃO leva `[A CONFIRMAR]` quando é claramente cena. Leva `[A CONFIRMAR]` só num caso: quando a frase o apresenta como fato do dono ou do cliente dele ("os 48 anos da minha aluna", "as 3 academias que ela abriu"), porque aí ele deixou de ser cena e virou número de negócio.
- **Número de NEGÓCIO (factual).** Qualquer número que descreve a realidade do dono, do cliente dele ou do resultado: alunas atendidas, faturamento, preço, prazo do método, taxa, quantidade de turmas, tempo de mercado, número de casos. Este só entra se veio do perfil do dono ou de fala que ele deu. Sem fonte, entra `[A CONFIRMAR: o quê]` **sem valor**, nunca um número plausível com etiqueta.

**Checagem verificável (o agente lista e prova, não afirma).** Antes de renderizar a matriz, escreva no chat a lista de todos os números que aparecem nas células, um por linha, nesta forma exata:
> `Números da matriz: <número> | CENA ou NEGÓCIO | fonte (perfil do dono / fala do dono / cena inventada) | marcado? sim/não`

Fecha a lista com: `Números de NEGÓCIO sem fonte: N (todos marcados [A CONFIRMAR]).` Se algum número de negócio sem fonte estiver sem marca, corrija e rode a lista de novo. Matriz sem essa lista escrita não passa no gate.

**Varredura anti-IA OBRIGATÓRIA e VISÍVEL (não é checkbox implícito).** Antes de renderizar a matriz no doc, o alvo do check NÃO é só as células: é o doc INTEIRO, e o travessão mora justamente onde o modelo esquece de olhar (TÍTULO H1, HEADERS H2/H3, prosa fora da tabela). Sem shell (onde o `lint_copy.py` não roda), você NÃO declara "fiz CTRL+F" e segue: você **escreve no chat, como etapa do gate, o resultado literal da varredura** sobre o texto do doc, nesta forma exata:
> `Varredura anti-IA do doc: travessao U+2014 encontrados: N em [onde]; verbo-freio banido encontrados: N em [onde].`

Se N maior que 0 em qualquer um, você **corrige antes de mostrar o doc** (troca travessão por ponto, dois-pontos, vírgula ou hífen comum; troca o verbo-freio banido e suas flexões por emperrar/empacar/parar/freio/amarra) e roda a varredura de novo até dar `0 em nada`. Só depois renderiza. Zona proibida de esquecer: título, headers, legendas e frases de ligação, NÃO só as células. Com shell disponível, `python3 scripts/lint_copy.py` no doc confirma o zero (exit 0); sem shell, a varredura escrita acima é o gate.

## Passo 4 (MATRIZ), monta a matriz e aponta as mais fortes
Renderiza a matriz **em lista por semana e por dia**, nunca numa grade de 8 colunas (grade larga não fica legível em markdown nem no celular do dono). O formato da entrega é este:

```
## Semana 1
- **Seg | [pilar] | [formato]:** manchete-pauta
- **Ter | [pilar] | [formato]:** manchete-pauta
...
## Semana 2
...
```

Uma linha por pauta, com o dia, o pilar e o formato de ataque visíveis na própria linha. Distribua as 30 ou mais pautas pelas 4 ou 5 semanas do mês, variando pilar e formato dentro de cada semana pra nenhuma semana ficar só de um tipo. O cruzamento pilar por formato continua sendo como você GERA as pautas (Passo 1 e 2); ele não é como você ENTREGA. Abaixo dela: **as 3 pautas mais fortes de toda a matriz** com 1 linha de porquê cada (a que mais fecha no método, a mais ancorada em dor, a mais contrária), e a **nota de qual pilar ficou mais raso** (pra pedir insumo). Não narra o fluxo, entrega limpo.

**Título e subtítulo do doc também passam pelo anti-IA HARD.** O H1 e todo header (H2/H3) do documento seguem a mesma regra das células: use vírgula, ponto ou dois-pontos como separador, NUNCA travessão. Certo: "Matriz de Conteúdo, Nutrição Esportiva" ou "Matriz-Calendário: 4 pilares por 8 formatos". Errado: qualquer título com travessão entre as partes. Isso é o que a varredura visível do Passo 3 pega no título e nos headers.

**O doc carrega SÓ o conteúdo, zero bastidor da conversa (Lei 6, corta meta-narração).** Dentro do arquivo entra APENAS: a matriz + os pilares + as 3 mais fortes + os `[A CONFIRMAR]`. Fica FORA do doc, e mora só no chat: qualquer eco de fala do dono ("você respondeu...", "perfeito, pode seguir"), qualquer narração do STOP, qualquer frase de condução ("matriz montada abaixo", "conforme você pediu"). A confirmação do dono acontece no chat e não vira carimbo no documento. Se você se pegar escrevendo no doc uma frase que só faz sentido pra quem viu a conversa, ela é meta-narração: corta.

## Passo 5 (MATRIZ), mostra e PARA
**Antes de mostrar, rode o Passo 6 (o gate executável) e cole a saída.** Mostra a matriz **no DOC** (nunca solta no chat). Pergunta: "quais pautas te servem? quer que eu escreva a headline de alguma (passo pra soft-conteudo-headlines) ou gero mais numa linha?". **Espera a escolha** antes de gerar volume ou passar pra headline.

## Passo 6 (MATRIZ), o gate executável (último passo, saída colada, BLOQUEANTE)

**A tabela de pilares por formatos morre no rascunho.** O cruzamento 4x8 é o método de GERAÇÃO das pautas, e o dono não executa uma grade: a entrega é a lista por semana e por dia, uma pauta por linha, com `<Dia> <dd/mm>` no COMEÇO de cada linha de pauta. Entrega em grade de 8 colunas está entregando o rascunho no lugar do plano, e reprova antes do gate. Se você montou a matriz 4x8 pra gerar, ela fica no `conferencia/checagem-titulos.md` como seção de rascunho, nunca no arquivo que o dono abre pra planejar o mês.

**Este gate é bloqueante: sem a saída dos quatro comandos colada, a matriz não é mostrada.** As regras de contrato desta skill que mais são ignoradas viram comando aqui, e a saída de cada um vai colada no `conferencia/checagem-titulos.md`. Rode os quatro, nesta ordem, com a matriz já gravada:

```
grep -cE '^\|' matriz-conteudo-AAAA-MM-DD.md
grep -cE '^\| *[A-ZÀ-Ú][a-zà-ú]+ [0-9]{2}/[0-9]{2}' matriz-conteudo-AAAA-MM-DD.md
grep -c 'dias já vencidos' matriz-conteudo-AAAA-MM-DD.md
ls conferencia/checagem-titulos.md
```

O que cada saída decide:

- **A regra "toda pauta tem data" é contagem, não promessa.** Cole `pautas: N · com <Dia> <dd/mm> no começo da linha: N`, com N tirado da contagem de linhas de pauta e o segundo número da segunda contagem. **Diferença entre os dois números reprova a matriz** e as linhas sem dia e data voltam pro Passo 2. O segundo comando conta a data NO COMEÇO da linha de propósito: data solta no meio da célula não diz ao dono em que dia ele posta. Escrever "todas as pautas têm data" sem as duas contagens coladas não conta como feito.
- **A linha de dias vencidos existe ou a matriz não sai.** `grep -c 'dias já vencidos'` tem que voltar 1. Saída 0 reprova: a matriz abriu num dia que o dono não tem como executar, e a linha `hoje: <dd/mm> · janela pedida: <dd/mm a dd/mm> · dias já vencidos: N` do Passo 0 nunca foi escrita.
- **`ls conferencia/checagem-titulos.md` tem que listar o arquivo.** Saída de erro reprova antes da análise de conteúdo, e nenhuma seção dentro de outro documento substitui o arquivo de nome fixo.

Cole a saída literal dos quatro comandos, sem reescrever nada, e só então mostre a matriz.

## Uma matriz PREENCHIDA, no formato exato da entrega (caso FICTÍCIO, não copiar)

Nicho fictício: consultor de gestão pra dono de pequena empresa de 5 a 40 funcionários. Avatar: o
dono que aprova cada compra pequena e não vê o rombo grande. Mecanismo dele (fictício): **Sistema
Mínimo de Gestão**. As pautas nasceram do cruzamento de 4 pilares por 8 formatos (32 pautas), e a
entrega sai em lista por semana e por dia. É esta a densidade que a entrega real tem.

### Semana 1
- **Seg | Método | Acionável:** Os 3 números que você precisa olhar toda segunda antes de abrir o e-mail.
- **Ter | Diagnóstico | Diagnóstico:** O dono que aprova cada compra de 50 reais e não vê o rombo de 8 mil por mês.
- **Qua | Tese | Contrário:** Contratar um gerente antes de existir número compra um problema mais caro que o original.
- **Qui | Bastidor | Bastidor:** A primeira coisa que eu peço na reunião é o extrato dos últimos 3 meses, antes de falar de meta. Quem empaca aí não é meu cliente.
- **Sex | Método | Antes vs Depois:** Da segunda-feira de susto ao número na tela antes do café.
- **Sáb | Diagnóstico | Lista:** 6 sinais de que o teu processo de compra está furado.
- **Dom | Tese | Observação:** Quase todo dono que me procura já contratou alguém pra resolver o que era decisão dele.
- **Extra | Bastidor | X vs Y:** Diagnóstico de 1 dia vs acompanhamento de 3 meses: quando cada um serve.

### Semana 2
- **Seg | Diagnóstico | Acionável:** Como descobrir em 20 minutos quanto do teu lucro some no processo de compra.
- **Ter | Método | Diagnóstico:** O dono que tem 14 planilhas e nenhuma resposta na hora que o contador pergunta.
- **Qua | Bastidor | Contrário:** Na primeira reunião eu peço a lista de quem tem poder de assinar um pagamento, e o faturamento pode esperar.
- **Qui | Tese | Analítico:** Por que o dono virou o gargalo da própria empresa sem nenhuma decisão errada.
- **Sex | Diagnóstico | Antes vs Depois:** De "eu acho que dá lucro" a "eu sei quanto sobrou", em 30 dias.
- **Sáb | Método | Lista:** 5 controles que cabem numa folha e substituem 14 planilhas.
- **Dom | Bastidor | Observação:** Nas últimas 12 empresas que eu abri a pasta, o mesmo erro apareceu em 9. `[A CONFIRMAR: número real de casos]`
- **Extra | Tese | X vs Y:** Sócio operacional vs gerente contratado: quem resolve o que, e a que preço.

### Semana 3
- **Seg | Tese | Acionável:** O que perguntar ao teu contador na próxima reunião, e o que não aceitar como resposta.
- **Ter | Bastidor | Diagnóstico:** O que eu vejo em toda empresa que me chama dizendo "está tudo sob controle".
- **Qua | Método | Contrário:** Quanto do teu ERP você abriu esse mês? A folha que o teu concorrente usa custa zero.
- **Qui | Diagnóstico | Analítico:** O que acontece com a margem quando ninguém revisa o processo há 2 anos.
- **Sex | Tese | Antes vs Depois:** Do dono que aprova tudo ao dono que decide o que importa.
- **Sáb | Bastidor | Lista:** 3 coisas que eu peço antes de aceitar um cliente novo.
- **Dom | Método | Observação:** Toda empresa que cresce rápido perde primeiro o controle de compra, não o de venda.
- **Extra | Diagnóstico | X vs Y:** Cortar 10% do custo vs consertar 1 processo: qual devolve mais no mesmo mês.

### Semana 4
- **Seg | Bastidor | Acionável:** Antes de olhar qualquer número, eu pergunto quem aprova uma compra de 50 reais na empresa. A resposta já mostra onde o dinheiro vaza.
- **Ter | Tese | Diagnóstico:** O empresário que se chama de estrategista e passa o dia aprovando compra de material.
- **Qua | Diagnóstico | Contrário:** Cortar custo em empresa que não sabe onde o dinheiro entra só deixa o buraco mais difícil de achar.
- **Qui | Método | Analítico:** Por que o controle que funciona com 5 pessoas quebra exatamente aos 12 funcionários.
- **Sex | Bastidor | Antes vs Depois:** O que muda no primeiro mês depois que a compra passa a ter uma regra.
- **Sáb | Tese | Lista:** 4 decisões que só o dono pode tomar, e 4 que ele nunca deveria tomar.
- **Dom | Diagnóstico | Observação:** Empresa que reclama de margem quase sempre tem 3 fornecedores fazendo o mesmo item.
- **Extra | Método | X vs Y:** Planilha do contador vs painel do dono: os dois existem, só um decide alguma coisa.

**Lista de números desta matriz (a checagem do Passo 3, escrita):**
`50 reais | CENA | cena inventada | não` · `8 mil por mês | NEGÓCIO | fala do dono | não` · `20 minutos | CENA | cena inventada | não` · `14 planilhas | CENA | cena inventada | não` · `12 empresas e 9 casos | NEGÓCIO | sem fonte | sim, marcado [A CONFIRMAR]` · `30 dias | NEGÓCIO | perfil do dono | não` · `12 funcionários | CENA | cena inventada | não` · `10% do custo | CENA | cena inventada | não`
`Números de NEGÓCIO sem fonte: 1 (todos marcados [A CONFIRMAR]).`

**As 3 pautas mais fortes desta matriz:**
1. Pilar 2 × Diagnóstico ("aprova 50 e não vê o rombo de 8 mil"), porque nasce quase intacta do verbatim e a lacuna fecha direto no que ele vende.
2. Pilar 3 × Contrário ("contratar gerente antes de existir número"), porque ataca a decisão mais cara que o avatar está prestes a tomar.
3. Pilar 1 × Antes vs Depois ("da segunda-feira de susto ao número antes do café"), porque é a única que mostra o estado depois com cena.

**Pilar mais raso: o 4 (Bastidor).** As células saíram genéricas porque não há verbatim nem número
real do dia a dia dele. Pedir 3 histórias concretas de atendimento resolve.

**Contagem: 32 pautas, 32 ideias distintas.** Nenhuma se repete entre pilares.

### A célula, destrinchada (por que esta passa no gate)
Pilar 2 (Diagnóstico) × Formato 2 (Diagnóstico de dor):
> **"O dono de PME que aprova cada compra de R$50 e não vê o rombo de R$8 mil por mês no processo que ninguém revisa."**
- **Ancorada:** verbatim real "eu controlo tudo mas o dinheiro some" (N=4 na super-pesquisa). Nasce quase intacta dessa fala.
- **Aponta pro método:** a lacuna (não é gastar menos, é o processo cego) fecha no "sistema mínimo de gestão" que o consultor vende.
- **Específica:** dá pra ver (R$50 aprovado, R$8 mil somem), não é "gestão financeira".
- **Filtra:** fala com dono que decide tudo sozinho (o cliente), não com quem quer dica de app de finanças.
- **Anti-IA:** zero travessão longo (U+2014), zero do verbo-freio banido, zero frase-emoldura, no doc inteiro (célula, título e headers). PASSA.

Contra-exemplo (REPROVA): "5 dicas de produtividade pra empreendedor." Genérica (qualquer creator posta), não aponta pro método, não filtra, não ancora em fala real. VEREDITO = ✗.

# MODO RADAR, o pulso da semana no nicho
> Escolha este modo quando o pedido é a pauta quente da semana ("o que tá em alta", "tendências", "o que tá bombando", "sobre o que postar essa semana"). É pauta perecível e datada, o oposto do banco fixo da matriz. A profundidade da varredura (fontes, buscas datadas, verificação de data, fallback quando o feed não abre, régua de saliência item a item) está em `references/protocolo-de-busca.md`; os passos abaixo já são executáveis.

## Passo 0 (RADAR), puxa nicho + avatar + janela (NÃO PULE, é a fronteira)
Antes de pesquisar, você precisa de três coisas. Procura nesta ordem: **Plano de posicionamento colado** → **perfil/descrição do projeto** → **mensagens anteriores**. O que faltar, pergunta numa mensagem curta.
1. **Nicho + avatar** (obrigatório pra filtrar o ruído). Não é "marketing", é "consultor de gestão financeira pra dono de clínica odontológica". Do Plano você puxa junto a **tese/mecanismo do dono e o verbatim de dor** (é o que enquadra a coluna de ângulo). Sem Plano, você ainda roda, mas avisa que o ângulo sai mais bruto sem a tese cravada.
2. **Janela** (default **7 dias**). O dono pode pedir 3 (pauta muito quente) ou 14 (nicho de giro lento). Fixe o N e respeite o corte duro.
3. **Fontes prioritárias do nicho** (opcional): perfis/portais/subreddits que o dono já acompanha. Se ele não sabe, você descobre na varredura.

**Regra de fronteira:** você NÃO faz pesquisa de fundação aqui (força da dor, mapa de concorrente, verbatim atemporal). Isso é a Super Pesquisa da soft-plano-posicionamento. Aqui nicho/avatar entram como FILTRO de entrada, não como objeto de pesquisa.

## Passo 1 (RADAR), varre as fontes com data verificada
Vasculha a web como um pesquisador humano faria. **A regra-mãe: confere a data de publicação de cada item e descarta sem exceção o que passa da janela.** Detalhe em `references/protocolo-de-busca.md`; o essencial:
- **Buscas datadas (base, sempre roda):** para cada eixo, uma query filtrada pela janela. Os 5 eixos que capturam pauta quente: `[nicho] novidade/lançamento`, `[nicho] polêmica/debate`, `[nicho] dado/pesquisa`, `[nicho] mudança/regra nova`, `[nicho] o que está bombando/viralizou`. Com acesso à web, busque e abra cada resultado pra ler a data no corpo da página. Adapte as queries pro idioma e jargão real do nicho (PT-BR quando o público é BR).
- **Feed social (quando a navegação abre):** rola o feed relevante (Reddit home/r/popular + subreddits do nicho; X/Para Você; perfis de concorrente no Instagram) e abre os posts em alta. Confere o carimbo de data em cada um. O feed LOGADO (X/Instagram) é o ponto frágil: se não abre, cai no fallback e diz.
- **Verificação de data (sem atalho):** abre a página, localiza a data visível, confirma que está dentro da janela. Data faltando, confusa ou fora = item descartado. Nunca deduz data pelo "parece recente".

## Passo 2 (RADAR), filtra por saliência (o que é calor de verdade)
Junta o conjunto amplo de itens datados e agrupa os relacionados em **temas** (um tema pode combinar discussão social + cobertura de portal). Um tema só entra no radar se mostra **pelo menos 2** destes sinais de calor:
- **Volume/atenção forte** (muita gente falando, engajamento acima do normal do nicho).
- **Debate/discordância clara** (o nicho está dividido, tem os dois lados).
- **Informação nova ou virada** (dado inédito, lançamento, mudança de regra que altera como o avatar trabalha).
- **Implicação real pro avatar do dono** (mexe com a vida/o bolso/o trabalho de quem ele atende). É o sinal mais valioso aqui: em dúvida entre dois temas, fica com o que toca o avatar.

Tema com 1 sinal só é ruído, não entra. É o filtro que separa "assunto quente que rende peça" de "notícia qualquer". Anota QUAIS sinais o tema tem (vira a coluna "Sinais de calor"): se você não consegue nomear 2 sinais concretos, o tema não passa.

## Passo 3 (RADAR), escreve a coluna Ângulo do Método (o coração do modo)
Aqui o radar deixa de ser clipping e vira munição. Pra cada tema que passou, a coluna **Ângulo do Método** enquadra o tema quente pela lente do dono. NÃO é gancho genérico de creator ("aproveite essa tendência!"). É:
- **Ancorado na dor/desejo real do avatar** (verbatim do Plano quando existe). O ângulo nasce de como o cliente do dono vive esse assunto quente, não de como o mercado geral vê.
- **Enquadrado pela tese/mecanismo do dono.** O tema quente é a ISCA; o método do dono é a resposta. Ex.: sai uma polêmica sobre a ferramenta X → o ângulo não é "opine sobre a ferramenta X", é "por que a ferramenta X não resolve o problema real (que é [o que o método do dono ataca])".
- **Aponta pro método e filtra o cliente certo.** Deixa a lacuna que fecha no que o dono vende. Ângulo que qualquer creator do nicho postaria = reprovado.
- **Vocabulário do cliente final** (nunca "lead/funil/ticket" no ângulo), tom de comando, número em algarismo.
- **Curto:** uma manchete-ângulo, não um parágrafo. Ela vira o INPUT da soft-conteudo-headlines.

## Passo 4 (RADAR), roda o GATE por dentro (auditoria interna, NÃO imprime)
Roda o gate em CADA linha antes de ela entrar no radar. A tabela é teu **checklist interno**, nunca a saída. Uma falha refaz a linha (ou derruba o tema), não o radar inteiro.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Datado e na janela** | tem data verificada, dentro dos N dias; data faltando/fora = ✗ (item cai) | |
| **Saliente (2+ sinais)** | tem ao menos 2 sinais de calor reais; 1 só = ruído, ✗ | |
| **Link real** | link representativo existe e foi aberto; link inventado/deduzido = ✗ | |
| **Ângulo ancorado** | nasce da dor real do avatar (verbatim) OU da tese do dono; genérico de creator = ✗ | |
| **Ângulo aponta pro método** | deixa lacuna que fecha no que o dono vende; NÃO é "surfe a tendência" solto | |
| **Filtra o cliente certo** | atrai quem compra do dono, não curioso do nicho; pauta viral genérica = ✗ | |
| **Clareza (Lei 1)** | dá pra entender sem já ser de dentro; zero palavra difícil, zero figura vazia | |
| **Sem invenção (Lei 5)** | zero link/data/número/tendência inventado; furo pontual = `[A CONFIRMAR]`, não item plausível | |
| **Anti-IA (HARD)** | zero travessão longo (U+2014) · zero da a família do verbo-freio banida pela régua anti-voz (o verbo que rima com "cravar" e vira emperrar/empacar/parar), em todas as flexões · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype (o "revoluciona/transforma" e o próprio verbo-freio banido) | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ na data/link/invenção derruba o TEMA. Um ✗ no ângulo REFAZ o ângulo. Só tudo-✓ entra. | |

**Varredura anti-IA OBRIGATÓRIA e VISÍVEL na coluna de ângulos (a mesma do MATRIZ Passo 3):** o alvo do check é o doc INTEIRO, título e headers inclusos, não só as células. No chat/agente sem Bash, você **escreve no chat, como etapa do gate, o resultado literal da varredura**, na forma exata: `Varredura anti-IA do doc: travessao U+2014 encontrados: N em [onde]; verbo-freio banido encontrados: N em [onde].` Se N maior que 0, corrige antes de mostrar e roda de novo até dar `0 em nada`. No Code/agente com Bash, `python3 scripts/lint_copy.py` no doc confirma o zero (exit 0).

## Passo 5 (RADAR), monta o radar e PARA
Renderiza a tabela-radar no DOC (tabela markdown que renderiza, nunca dentro de bloco de código, que vira grade ilegível). Abaixo dela: **as 3 pautas mais quentes** com 1 linha de porquê cada (a que mais casa com a tese, a mais debatida, a com implicação mais direta pro avatar) + a nota "isso foi o que verifiquei dentro da janela; [X] itens caíram por falta de data". Se a varredura ao vivo falhou em parte, DIZ o que não deu pra varrer.

Mostra o radar **no DOC** e PARA. Pergunta: "qual dessas pautas você quer transformar em peça? Passo pra **soft-conteudo-headlines** pra escrever a headline, ou encaixo no calendário do MODO MATRIZ." **Espera a escolha** antes de escrever qualquer peça. O radar entrega a munição; quem dispara é a skill de peça.

## Exemplo denso RADAR (nicho: nutricionista esportivo pra corredor amador), LABEL, não copiar
> Nicho/avatar (do Plano): nutri esportivo, avatar = corredor amador 35-50 que treina pra prova de rua e "come certo mas não rende". Tese do dono: o problema não é dieta restritiva, é **timing de carboidrato em torno do treino** (o mecanismo dele). Janela: 7 dias. Ambiente: com shell e acesso à web.

1. **Passo 0:** puxo nicho, avatar e tese do Plano colado. Janela 7 dias. Fontes que o dono segue: 2 perfis de treino + r/running.
2. **Passo 1:** rodo as buscas datadas (`corrida de rua novidade`, `suplemento corredor polêmica`, `nutrição esportiva pesquisa`) pela busca web, abro os resultados e leio a data no corpo. Rolo r/running e os 2 perfis. Descarto 6 itens sem data clara.
3. **Passo 2 (saliência):** um tema quente sobrevive: "estudo novo dessa semana questionando o gel de carboidrato durante a prova". Sinais: debate claro (corredores divididos) + informação nova (o estudo) + implicação real pro avatar (ele usa gel e não sabe se serve). 3 sinais, passa. Um segundo tema ("tênis de placa de carbono na moda") tem só volume, 1 sinal: cai.
4. **Passo 3 (ângulo do método):** o ângulo NÃO é "opine sobre o estudo do gel". Enquadro pela tese: **"O corredor que toma 3 géis na prova e continua quebrando no km 30, porque o problema nunca foi o gel na corrida, foi o carboidrato que faltou nas 48h antes."** Ancorado no verbatim "como certo mas não rendo", aponta pro mecanismo (timing de carbo), filtra o corredor que treina sério (o cliente), não o curioso.
5. **Passo 4 (gate):** datado ✓, 3 sinais ✓, link do estudo aberto ✓, ângulo ancorado na tese ✓, aponta pro método ✓, filtra ✓, clareza ✓, sem invenção ✓, anti-IA (rodei `lint_copy.py` na coluna, zero travessão longo, zero do verbo-freio banido) ✓. VEREDITO ✓, entra.
6. **Passo 5:** salvo `radar-nutri-corrida-2026-07-04.md` com a tabela, aponto essa como a pauta #1, respondo com o path completo e pergunto "escrevo a headline dela? (soft-conteudo-headlines)".

Contra-exemplo RADAR (REPROVA): tema "tênis de placa de carbono está na moda" com ângulo "aproveite a hype dos tênis de carbono pra falar de performance". Um sinal só (volume), ângulo genérico que qualquer creator posta, não aponta pro mecanismo do dono, não filtra o cliente. VEREDITO = ✗, tema cai.

## O que esta skill NÃO faz (e pra onde vai)

Esta skill decide SOBRE O QUE postar e para aí. Ela não escreve headline nem peça. Em toda rota abaixo, se a skill de destino não estiver instalada, esta faz o mínimo aqui e diz o que fez.

| O pedido é | Vai pra | Se não estiver instalada |
|---|---|---|
| A **headline/gancho** de uma pauta já escolhida | **soft-conteudo-headlines** | escreve 3 headlines a partir da célula e avisa que o banco completo mora lá |
| O **corpo do carrossel** | **soft-conteudo-carrossel** | entrega só a pauta e diz que a peça é outra etapa |
| O **roteiro do reel** | **soft-conteudo-reels** | idem |
| A **sequência de stories** | **soft-conteudo-stories** | idem |
| **Adaptar** uma peça pronta pra outra plataforma | **soft-conteudo-multiplataforma** | entrega só a pauta |
| Definir **pilares, círculo temático, posicionamento**, ou a pesquisa de **fundação** (mercado, força da dor, concorrente, verbatim atemporal) que se faz uma vez e usa o ano | **soft-plano-posicionamento** | propõe 3 ou 4 pilares e PARA pro dono confirmar; nunca fixa como fato |
| **Meta, projeção, roadmap de 90 dias do NEGÓCIO** | **soft-plano-negocio** | diz que aqui o plano é de conteúdo, não de negócio, e pergunta se é isso mesmo |
| **Arte, visual, PNG** | **soft-designer** | entrega só o texto da pauta |
| **Carta, página, venda** | **soft-funil-carta** / **soft-funil-landing** / **soft-vendas-closer** | entrega só a pauta |

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Célula virou tema amplo ("Vendas", "Mindset") | Reescreve como manchete específica com cena/número que dá pra ver |
| Mesma ideia em dois pilares | Uma das células muda de ângulo; toda célula é distinta |
| Pauta genérica que qualquer creator postaria | Falha em "aponta pro método" e "filtra": reancora na dor do avatar e na lacuna do método |
| Inventou um pilar que o dono não tem | Puxa do Plano; se faltam, PROPÕE e PARA pra confirmar, nunca fixa como fato |
| Definiu círculo temático / reescreveu posicionamento | Fora do escopo: isso é soft-plano-posicionamento; aqui pilar é dado de entrada |
| Frase motivacional / viral de boteco na célula | Cortado de propósito: atrai estranho, não filtra cliente; reescreve ancorado |
| Despejou a matriz/radar solto no chat | O doc sai como MD (renderizado, arquivo ou path no agente, conforme o ambiente); o chat é a condução |
| Jogou a tabela dentro de bloco de código | Tabela markdown que renderiza; bloco de código vira grade ilegível |
| Menos de 30 pautas (matriz) | Fecha 30+ (5×6 ou 4×8); gera 2 por formato em alguns cruzamentos se faltar |
| (RADAR) Incluiu item sem data ou fora da janela | Corte duro: data verificada dentro dos N dias, senão o item cai. Nunca deduz "parece recente" |
| (RADAR) Inventou um link, uma data ou uma tendência | Lei 5: só o que você abriu e verificou entra; furo vira `[A CONFIRMAR]`, nunca item plausível |
| (RADAR) Tema com 1 sinal de calor entrou | Filtro de saliência: mínimo 2 sinais; 1 só é ruído, não pauta |
| (RADAR) Ângulo genérico ("aproveite essa tendência!") | Enquadra pela tese/mecanismo do dono e ancora na dor do avatar; tema quente é isca, método é resposta |
| (RADAR) Simulou a varredura quando o feed não abriu | Honestidade de tooling: avisa o que não deu pra varrer, trabalha com busca web datada ou o que o dono colou |
| (RADAR) Virou pesquisa de fundação (dor, concorrente, verbatim atemporal) | Fora do escopo: isso é a Super Pesquisa (soft-plano-posicionamento); aqui é pauta da semana |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `shared-references/crivo/07-regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta (a entrada do dono, as perguntas feitas e a saída real de cada ação). **Leia antes da primeira pergunta.**
- `references/protocolo-de-busca.md`: **fonte da verdade da varredura do MODO RADAR** (fontes por tipo, buscas datadas por eixo, rolagem de feed, verificação de data sem atalho, fallback quando o feed logado não abre, régua de saliência detalhada). Consulta no Passo 1/2 do RADAR.
- `shared-references/operacao-padrao.md`: as 6 leis (Seção 0) + regras de tom/economia/entrega. Consulta na 1ª invocação da sessão.
- `shared-references/filtro-anti-ia/`: o banco de padrões banidos + falsos-positivos que alimenta o check Anti-IA do gate.
- `shared-references/filtro-cliente-primeiro.md`: a régua de "isto atrai o cliente certo ou o curioso do nicho?", aplicada nas células (matriz) e na coluna de ângulos (radar).
- `scripts/lint_copy.py`: quando há shell disponível (terminal ou agente), roda `python3 scripts/lint_copy.py` no doc INTEIRO como cinto extra do anti-IA (reprova o travessão longo U+2014 e o verbo-freio banido com exit 1, inclusive em título/headers). Sem shell não roda, por isso a varredura anti-IA escrita e visível é o gate.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
