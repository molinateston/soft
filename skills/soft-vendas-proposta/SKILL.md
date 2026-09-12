---
name: soft-vendas-proposta
description: >-
  Transforma uma call de venda numa PROPOSTA COMERCIAL premium: um site HTML de arquivo único (abas, diagnóstico, entregáveis com marcação que persiste, cronograma, investimento, prova, chamado), publicado num link privado por cliente. Use quando o pedido for: "monta a proposta", "proposta comercial", "proposta em HTML", "site de proposta", "orçamento premium", "manda o plano pro cliente", "quero fugir do PDF", "o cliente pediu por escrito", "proposta com validade de 7 dias". NÃO use pra: a mensagem de prospecção e o agendamento antes da call (soft-vendas-sdr); instalar ou publicar o kit de SDR (soft-sdr-kit); a escolha da campanha do mês (soft-vendas-estrategias); página de vendas pública, landing ou VSL (soft-funil-landing); o script, a objeção e o fechamento da venda (soft-vendas-closer); o contrato que formaliza o sim (soft-vendas-contratos); posicionamento, oferta e preço (soft-plano-posicionamento). Leia e siga o fluxo inteiro do SKILL.md.
---

# A proposta comercial que o cliente reabre pra decidir

Esta skill pega a call de venda já conduzida e devolve a proposta materializada num site premium com link próprio e privado por cliente: o documento silencioso que o prospect reabre quando vai decidir. Ela entra DEPOIS que a venda foi conduzida e DEPOIS que a oferta existe. É marca-neutra: cor, fontes, logo e prova social vêm do dono, nunca da skill.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Cada item da oferta é conferido contra o que a operação entrega hoje.** Rode `grep -rniE '<cada item da lista de inclusos>' <insumos>` e cole a saída. Item que aparecer numa reclamação, numa cobrança ou num registro de falha entra no handoff com `prometido na peça e em falha na operação: <item> · <arquivo:linha>`, pro dono decidir antes de publicar. A peça que promete o bônus que o cliente atual não está recebendo escreve a próxima reclamação.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra, num caso fictício de nicho neutro, a entrada que o dono deu, as perguntas que a skill fez, o diagnóstico dos 12 campos preenchido, a estrutura de abas escolhida e o link publicado. Ler antes economiza uma rodada inteira de retrabalho.

> **A regra dura que não se negocia: NUNCA atribuir fala ou número do dono ao cliente.** Se o dono disse "eu faturei X em fevereiro", isso é do dono, não do cliente. Proposta com atribuição trocada quebra a confiança na primeira leitura e não tem conserto. Toda linha do diagnóstico declara de quem é a fala antes de entrar no HTML.

> **A segunda regra dura: separar o que o cliente QUER do que foi só SUGERIDO.** São coisas diferentes. O que ele pediu é entrega central; o que o dono propôs a mais entra como upsell sugerido, marcado como tal.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a call e a oferta e eu monto a proposta). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pra montagem com o que o dono colou. Se faltar um insumo que a proposta não vive sem (a call conduzida, a oferta com preço), pergunta AQUELE insumo e segue, sem repetir a extração inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a extração da call, uma pergunta de cada vez (o diagnóstico, os entregáveis, o investimento), e monta a proposta com o que o dono for dando.

A pergunta do modo é UMA por proposta. As outras três partes acontecem nos passos abaixo:

- **Ensina enquanto faz:** em cada escolha estrutural (a ordem das abas, o entregável que ancora, o chamado) escreve UMA linha do porquê. O dono lê a razão e aprende a montar a próxima sozinho.
- **Puxa o material bruto:** quando a resposta vier rasa ("o cliente precisa de ajuda", "o de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: a dor que o prospect falou com as palavras dele na call, o resultado que ele quer ver, a prova que o dono pode mostrar. Fala real da call vira proposta que reabre e decide; resposta rasa vira orçamento esquecido.
- **Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer outra ordem de abas? mais prova? o investimento apresentado diferente? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "monta a proposta", "tenho a call gravada", "manda o plano pro cliente" | **1 · EXTRAÇÃO**, e segue até a 4 |
| "não gravei a call, mas anotei tudo" | **1 · EXTRAÇÃO**, no caminho sem gravação |
| "muda o preço da proposta", "troca a data", "o cliente pediu outra opção" | **3 · GERAÇÃO**, direto no HTML já existente |
| "publica", "o link caiu", "manda o link pro cliente" | **4 · PUBLICAÇÃO** |
| "qual layout eu uso", "escuro ou claro" | a tabela de layout na Ação 3 |

Pedido ambíguo ("preciso mandar uma proposta"): pergunte UMA coisa só, "você tem a call gravada ou vamos pelas suas anotações?", e siga pela resposta.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · passos numerados com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Cor, fontes, logo, oferta, preço e prova social: leia do perfil/brain do agente quando existir. Se não existir, colete no onboarding abaixo, uma vez só, e guarde no perfil. Nunca invente prova, nunca use número de terceiro.

> **Onboarding, na primeira vez, 4 itens:** (a) cor principal em hexadecimal, ou "escolhe por mim"; (b) fonte de título e de texto, ou "usa o padrão"; (c) logo, arquivo ou link, ou "sem logo, usa o nome escrito"; (d) prova social real disponível: números, depoimentos, casos. Mais o destino de publicação que ele usa. Nada disso fica gravado dentro da skill: vai pro perfil do dono.

**Método completo e autossuficiente:** `references/reference.md` guarda o método inteiro. As ações abaixo dizem qual trecho ler em cada passo, pra ninguém precisar abrir 1.246 linhas de uma vez.

---

## Ação 1 · EXTRAÇÃO (a etapa que decide a qualidade da proposta)

**O que faz:** lê a call inteira e preenche os 12 campos do diagnóstico, com cada fala atribuída a quem falou.

**Precisa de:** a call gravada, ou a transcrição, ou as anotações do dono · o nome e a grafia exata do cliente e da empresa.

**Sem o insumo:** **sem gravação, a proposta não para.** Rode a entrevista de reconstrução, 8 perguntas, uma por vez, na ordem: (1) quem é o cliente e o que a empresa dele faz; (2) o que ele vende hoje e por quanto; (3) qual foi a frase dele que mais pesou, o mais literal que você lembrar; (4) o que ele disse que quer resolver; (5) onde ele quer estar em 12 meses; (6) o que você propôs; (7) que preço você falou e como ele reagiu; (8) o que ficou combinado. O que sobrar vira `[A CONFIRMAR]` no diagnóstico. **Toda fala reconstruída de memória entra marcada como paráfrase, nunca entre aspas**, porque aspa falsa na boca do cliente é o pior defeito desta entrega.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `01-diagnostico-proposta.md`, os 12 campos preenchidos, com a origem de cada fala declarada. **STOP obrigatório: o dono valida os 12 campos ANTES de qualquer HTML ser gerado.** Esta é a skill que menos pode errar, porque o resultado é um site publicado com o nome do cliente.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/reference.md`, seção 3, Etapa 2 (o que extrair, as regras de atribuição, o formato do diagnóstico).

### Os 12 campos, e o que cada um exige

| # | Campo | O que precisa estar preenchido |
|---|---|---|
| 1 | Nome do cliente e da empresa | grafia exata, conferida |
| 2 | Nicho ou segmento | mercado e público que ele atende |
| 3 | Produtos e serviços atuais | o que ele já vende, ticket, volume |
| 4 | Faturamento atual ou potencial | só os números que ele mesmo disse |
| 5 | Time e estrutura | quantas pessoas, quem faz o quê |
| 6 | Dor central | com as palavras dele, atribuídas a ele |
| 7 | Objetivo de 12 meses | onde ele quer estar no fim do contrato |
| 8 | O que foi sugerido pelo dono | separado do que o cliente pediu |
| 9 | Preço oferecido | valores exatos ditos na call |
| 10 | Reação do cliente | interessado, com objeção, fechou, pediu prazo |
| 11 | Próximos passos | o que ficou combinado no fim |
| 12 | Personalizações | cor, paleta da marca, tom pedido |

**Tangibilize tudo o que foi discutido.** Se a call mencionou um aplicativo, a proposta detalha telas, funcionalidades e valor de mercado. Se mencionou um agente, detalha papel, ferramentas e integrações. Se mencionou evento presencial, detalha formato, local sugerido e ingresso. **Onde o escopo incluir software, aplicativo ou sistema, precifique o valor de mercado**: quanto custaria contratar uma empresa de desenvolvimento pra fazer o mesmo separado. Isso justifica o investimento pela conta que o cliente já entende.

---

## Ação 2 · ESTRUTURA (as abas, antes do código)

**O que faz:** define quais abas a proposta terá e em que ordem, pelo tipo de proposta.

**Precisa de:** o diagnóstico validado da Ação 1.

**Sem o insumo:** sem os 12 campos validados, não avance. A estrutura nasce do diagnóstico.

**Entrega:** a seção de estrutura dentro do `01-diagnostico-proposta.md`, com a lista de abas na ordem. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/reference.md`, seção 5 (estrutura de conteúdo e as variações da última aba).

**As abas obrigatórias, nesta ordem:** Visão Geral (sempre a primeira) → abas intermediárias personalizadas por cliente → Entregáveis → Plano de Ação → Investimento (sempre a última, salvo as variações previstas na referência).

**A oferta aparece em 2 ou 3 opções, nunca uma só**, com validade de 7 dias e ancoragem por custo evitado ou por retorno. Os valores são do dono: a skill formata, não define preço.

---

## Ação 3 · GERAÇÃO (o HTML de arquivo único)

**O que faz:** gera o site da proposta, um HTML autocontido, com a identidade visual do dono.

**Precisa de:** a estrutura da Ação 2 · a identidade visual do dono (cor, fontes, logo) · a prova social real dele.

**Sem o insumo:** sem identidade definida, use o padrão da referência e marque em 1 linha que a paleta precisa de confirmação. Sem prova social real, **deixe a seção de prova fora do HTML** e diga isso; nunca preencha com número inventado nem com caso de terceiro.

**Entrega:** o arquivo `proposta-<cliente>.html`, único, com estilo e script embutidos, funcionando sem conexão. **STOP: o dono lê a proposta inteira antes de ela ser publicada.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/reference.md`, seção 3, Etapa 3 (a geração) e seção 4 (o layout e os componentes).

**Profundidade:** `references/reference.md`, seção 6 (regras de precificação e ancoragem) · seção 7 (as regras invioláveis, técnicas, de conteúdo e de entrega).

### Qual layout usar (a decisão em uma tabela, não em 1.246 linhas)

| Se o cliente é | Layout | Por quê |
|---|---|---|
| luxo, arte, tecnologia, bem-estar, ou qualquer nicho que pede sofisticação visual | **Escuro premium** | o fundo escuro carrega sozinho a percepção de valor alto |
| B2B, saúde, jurídico, indústria, corporativo, ou cliente mais conservador | **Claro corporativo** | o cliente conservador lê fundo escuro como enfeite, não como seriedade |
| na dúvida, ou o cliente mandou a paleta da marca dele | **Claro corporativo**, com a cor dele no destaque | erra menos, e a cor da marca faz o trabalho |

Os componentes prontos: topo com métricas de âncora, diagnóstico em duas colunas, pilares, entregáveis com marcação que persiste mais barra de progresso, cronograma, investimento em duas colunas, prova social, chamado e perguntas frequentes.

---

## Ação 4 · PUBLICAÇÃO (o link privado)

**O que faz:** publica a proposta num endereço privado e não adivinhável, e prova que ela abre no celular.

**Precisa de:** o HTML aprovado da Ação 3 · o destino de publicação e a credencial do dono.

**Sem o insumo:** sem credencial de publicação, entregue o arquivo `.html` com o caminho na resposta e o passo a passo escrito de como publicar, pro dono fazer no ambiente dele. O arquivo funciona sozinho, sem conexão, então ele já pode mandar por e-mail enquanto o link não existe.

**Entrega:** o link privado, mais a linha de mensagem pronta pro dono mandar ao cliente. **STOP: o teste no celular acontece ANTES de o link ir pro cliente.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/reference.md`, seção 3, Etapa 4 (publicação) e seção 7 (as regras de entrega).

### O teste no celular é um STOP visível, não uma nota de rodapé

A maioria dos clientes abre a proposta no telefone, no meio de outra coisa. Antes de mandar o link, confira, nesta ordem, e só siga com tudo aprovado:

1. O topo cabe na tela sem rolagem lateral.
2. As abas são clicáveis com o polegar, sem zoom.
3. A tabela de investimento não estoura a largura.
4. O cronograma rola dentro dele mesmo, e não empurra a página.
5. A marcação dos entregáveis funciona e persiste ao voltar.
6. O chamado final aparece sem precisar rolar até o fim de tudo.

Um item reprovado volta pra Ação 3.

---

## Gate de qualidade (roda antes de publicar, sempre)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.


| Check | Passa se |
|---|---|
| **Atribuição** | nenhuma fala ou número do dono aparece como do cliente; toda aspa tem dono declarado |
| **Querido x sugerido** | o que o cliente pediu está como entrega central; o que o dono propôs a mais está marcado como sugestão |
| **12 campos validados** | o dono aprovou o diagnóstico antes de existir HTML |
| **Prova real** | todo número e depoimento é do dono, verificável; sem prova real, a seção sai |
| **Preço do dono** | os valores vieram dele; a skill formatou, não definiu |
| **Opções** | a proposta oferece 2 ou 3 caminhos, com validade declarada |
| **Arquivo único** | o HTML abre sozinho, sem conexão, com estilo e script embutidos |
| **Celular** | os 6 itens do teste passaram |
| **Link privado** | o endereço não é adivinhável e não está listado em lugar nenhum |
| **Anti-IA** | com shell, roda o linter anti-IA do ambiente sobre a copy e exige saída limpa; sem shell, varre o texto atrás do travessão longo e da família do verbo-freio banida pela régua anti-voz, e reescreve cada ocorrência |
| **VEREDITO** | é o pior item; um ✗ refaz o item, não a proposta inteira |

> Regra-mãe: a proposta só é boa se a extração for boa. A maior parte do tempo é entender a call, não montar o HTML.

## O que esta skill NÃO faz

Em toda rota abaixo: se a outra skill não estiver instalada, esta faz o mínimo aqui e diz que fez, com o pedaço mais fino marcado `[A CONFIRMAR]`.

- **Conduzir a venda, responder objeção, pedir o sim, o follow-up dos 7 dias** → **soft-vendas-closer**. A proposta é a exceção da call, não a etapa padrão: quem cobra no dia 5 e fecha ou encerra no dia 7 é o closer.
- **O contrato que formaliza o sim** → **soft-vendas-contratos**.
- **Página de vendas pública, landing, VSL** → **soft-funil-landing** e **soft-funil-carta**. Aqui o link é privado, de um cliente só.
- **Escolher a campanha do mês** → **soft-vendas-estrategias**. **Abrir e agendar o lead** → **soft-vendas-sdr**.
- **Posicionamento, oferta, PUV, definição de preço** → **soft-plano-posicionamento**.
- **Arte, identidade visual do zero** → **soft-designer**. Aqui a identidade é a do dono, aplicada.

## Anti-patterns

| Erro | Por que quebra | Faz assim |
|---|---|---|
| Gerou o HTML antes de validar o diagnóstico | Erro de fato vira site publicado com o nome do cliente | STOP nos 12 campos, sempre, antes do código |
| Atribuiu fala do dono ao cliente | Quebra a confiança na primeira leitura, sem conserto | Cada fala declara de quem é, no diagnóstico |
| Misturou o que o cliente quer com o que foi sugerido | O cliente lê como se ele tivesse pedido o que não pediu | Entrega central separada de upsell sugerido |
| Escreveu aspa de memória, sem gravação | Aspa falsa na boca do cliente é o pior defeito daqui | Sem gravação, a fala entra como paráfrase, nunca entre aspas |
| Encheu a prova social pra não deixar vazio | Número inventado destrói a proposta e a marca | Sem prova real, a seção sai |
| Mandou o link sem abrir no celular | A maioria abre no telefone, e o defeito aparece pro cliente | Os 6 itens do teste, antes do link |
| Ofereceu uma opção só | Sem escolha, a decisão vira sim ou não | 2 ou 3 caminhos, com validade |
| Definiu o preço pelo cliente | O preço é do dono; a skill formata | Puxa os valores do perfil ou pergunta |
| Proposta virou rotina do funil | Sinal de que as reuniões estão sendo feitas pra gerar follow-up | Conserta a reunião, não a proposta: volta pra soft-vendas-closer |

## Handoff

- **Pra trás:** a condução da venda é da **soft-vendas-closer**; a oferta e o preço vêm do perfil do dono ou da **soft-plano-posicionamento**.
- **Pra frente:** cliente disse sim → contrato na **soft-vendas-contratos**. O follow-up dos 7 dias de validade é do closer, que cobra no dia 5 e fecha ou encerra no dia 7. O caso fechado vira prova pra `soft-plano-posicionamento` e pras `soft-conteudo-*`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
