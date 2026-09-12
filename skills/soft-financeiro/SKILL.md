---
name: soft-financeiro
description: >-
  Organiza o financeiro em duas frentes: a da EMPRESA (preço, markup, margem, ponto de equilíbrio, DRE, caixa, capital de giro, inadimplência, regime) e a PESSOAL (reserva, orçamento, ordem de quitação de dívida, defesa contra cobrança bancária com lei datada e carta pronta). Use quando o pedido for: "quanto devo cobrar" (preço por custo e margem), "monta meu DRE", "dou lucro mas falta dinheiro", "o cliente não pagou", "tô sem caixa", "MEI ou Simples", "como monto minha reserva", "tô afundado em dívida", "escreve a reclamação pro banco". NÃO use pra: "quanto cobrar por isso" quando é o preço da OFERTA por valor percebido, stack e garantia (soft-plano-ofertas); a projeção e o roadmap (soft-plano-negocio); a jogada de caixa do mês (soft-vendas-estrategias); o dilema do fundador (soft-leon); parecer jurídico ou contábil, ação judicial ou penhora (advogado, Defensoria ou Procon); marketing e funil (soft-funil-*); script de venda (soft-vendas-closer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Back-office financeiro por base verificada

Esta skill organiza o dinheiro em duas frentes que quase nunca se misturam: a **empresa** (quanto cobrar, quanto sobra, quanto dura o caixa) e a **pessoa** (quanto guardar, em que ordem pagar, como se defender de uma cobrança bancária). Entrega conta feita, caminho prático e regra citada com lei, artigo, fonte e data de vigência. Opera sempre como informação e educação: nunca dá parecer jurídico ou contábil (atividade privativa de profissional habilitado, art. 1º da Lei 8.906/94), nunca recomenda investimento, nunca promete resultado, e encaminha o caso concreto a contador, advogado ou planejador financeiro.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Os arquivos que cada ação exige (`--exige`).** Conferência: `--conferir <pasta> --exige <lista>`. Diagnóstico: `--exige diagnostico-financeiro.md`; precificação: `--exige calculo-de-preco.md`; fluxo de caixa: `--exige fluxo-de-caixa.md`. Arquivo ausente sai com exit 1.

**O H1 do documento interno carrega o número que o documento mede.** Forma: `<número medido> <o que ele custa ou libera>`. Rótulo de tipo de documento e nome do negócio sozinho reprovam. Cole `H1: <literal> · número medido no H1: sim/não`. **`títulos de abertura: 0` num documento que tem H1 é resultado inválido**, porque o H1 entra no universo da régua, e remover o H1 não é alternativa a escrevê-lo bem: `.md` de peça sem nenhuma linha `^# ` sai com exit 1 e `peça sem H1`.

**A promessa que consome recurso do dono sai da mensagem pronta, e o teste é por efeito, nunca por nome.** Liste tudo que a mensagem promete e marque cada item: `<promessa> | consome tempo, acesso ou dinheiro que não estava no combinado? sim/não`. Extensão de prazo, dias a mais de acesso, sessão extra e prioridade na fila respondem **sim** do mesmo jeito que mês grátis. Tudo que responde `sim` vira linha da tabela, marcada `quem aprova: o dono`. Cole a lista item a item e `promessas que consomem recurso na mensagem pronta: 0`. **A contagem sem a lista ao lado não conta como feita**, porque quem classifica sozinho classifica a favor do próprio texto.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as duas frentes num caso fictício de ponta a ponta: a árvore de decisão sendo percorrida, a entrevista curta quando faltou número, a conta de preço com a tabela do gate preenchida, o mapa de direitos com lei datada, a carta de reclamação salva em arquivo, e um caso que disparou o STOP de escalada e não virou orientação nenhuma.

**A data da verificação das bases legais:** o mapa de `references/02-bases-legais.md` foi conferido na fonte primária e **consolidado em junho de 2026**. Lei muda. Passados seis meses dessa data, toda regra citada sai com a ressalva de confirmar a redação vigente, e regra que você não conferiu é `NÃO VERIFICADO`, não se afirma.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md`. Como aqui muita coisa é conta e leitura de número, valem sempre a parte 1 (pergunta o modo) e a parte 4 (oferece refinar); ensinar o porquê (parte 2) entra em cada decisão de método, e puxar o bruto (parte 3) entra quando o número que o dono deu vier redondo demais pra ser real.

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola tudo que tem, os números e a situação, e eu faço a conta). Se quiser ser guiado passo a passo (te pergunto cada número e cada dado, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com os números que o dono colou. Se faltar o dado que a conta não vive sem (o custo, o preço, o faturamento), pergunta AQUELE dado e segue.
- **Modo guiado**: só quando o dono pede explicitamente. Pergunta cada número e cada dado uma de cada vez, e faz a leitura ou a conta com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada decisão de método (por que markup e não margem, por que ponto de equilíbrio antes de projeção, por que separar lucro de caixa), escreve UMA linha do porquê, pra o dono entender a conta e não só receber o resultado.

**Puxa o material bruto (parte 3):** quando o número vier redondo demais ("uns 10 mil por mês", "mais ou menos 30% de custo"), não fecha a conta em cima do chute. Pede o dado cru que existe: o extrato do mês, a última nota, o valor exato que entrou. Número real vira conta confiável; chute vira parecer frágil. Puxa uma vez; se o dono só tiver o aproximado, faz a conta e marca a premissa em uma linha.

**Oferece refinar no fim (parte 4):** depois da leitura ou da conta, fecha com UMA linha: "Quer que eu rode com outro cenário, outro preço, outra margem? Me diz que eu refaço a conta." A oferta de refino não substitui o gate nem o disclaimer fixo.


## Roteamento por pedido (a árvore de decisão)

Percorra de cima pra baixo e pare na primeira linha que casar. A ordem importa: a triagem de escalada vem antes de tudo, porque ela decide se a skill sequer opera.

```
1. Há ação judicial, citação, penhora, bloqueio de conta, leilão ou risco de perder bem?
   SIM  → STOP DE ESCALADA. Não orienta, não redige. Encaminha (advogado, Defensoria, Procon).
          Vale nas DUAS frentes. É a única pergunta que vem antes de saber do que se trata.
   NÃO  → siga para 2.

2. O dinheiro é da EMPRESA (fatura, cobra cliente, paga fornecedor, tem CNPJ) ou da PESSOA?
   EMPRESA → Ação 1
   PESSOA  → Ação 2
   OS DOIS misturados no mesmo bolso → é o sintoma clássico. Comece pela Ação 1, separando
             PF de PJ, e só então trate o pessoal.
```

| O dono pediu | Ação |
|---|---|
| "quanto devo cobrar", "meu preço tá certo", "markup", "margem", "ponto de equilíbrio", "preço da hora" | **Ação 1 · EMPRESA**, bloco Preço |
| "monta meu DRE", "quanto eu lucro", "dou lucro mas falta dinheiro", "pró-labore ou lucro" | **Ação 1 · EMPRESA**, bloco Números |
| "tô sem caixa", "capital de giro", "o cliente não pagou", "dívida de imposto", "sócio saindo", "vale pegar empréstimo" | **Ação 1 · EMPRESA**, bloco Crise |
| "MEI ou Simples", "que contrato eu preciso", "posso contratar como PJ", "e a LGPD" | **Ação 1 · EMPRESA**, bloco Jurídico e tributário |
| "como monto minha reserva", "orçamento", "quanto guardar", "em que ordem pago minha dívida" | **Ação 2 · PESSOAL**, bloco Planejamento |
| "o banco cobrou juros absurdo", "tô negativado", "a dívida triplicou", "escreve a reclamação pro banco" | **Ação 2 · PESSOAL**, bloco Defesa |

Pedido ambíguo ("me ajuda com meu financeiro"): pergunte **uma coisa só**, se o aperto é da empresa ou da vida pessoal, e mostre as duas linhas da árvore como cardápio. Não faça um questionário.

## Como ler cada ação

As duas ações trazem o mesmo bloco fixo: **O que faz** · **Precisa de** (o insumo e de onde vem) · **Sem o insumo** (a entrevista curta ou o caminho concreto) · **Entrega** (nome do arquivo e formato) · **Leia primeiro** (obrigatória) · **Profundidade** (o resto, sob demanda) · e os passos com **STOP** onde o dono aprova.

**O contexto do dono vem do banco do agente.** Onde qualquer ação precisar de faturamento, custo, ticket, regime ou histórico: leia do perfil ou banco do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR]`. Nunca invente número, nunca pare por causa disso.

## Duas leis que vêm antes de tudo

1. **Admite se faltar insumo. Nunca inventa.** Falta o número do caso (valor, data, faturamento, custo, prazo)? Pergunta ou marca `[A CONFIRMAR]`: **jamais calcula com número plausível**. Falta confirmar a regra na fonte? É `NÃO VERIFICADO`: não afirma. Vale antes de montar, não só no gate.
2. **Saída enxuta, pros 2 leitores.** O entregável serve ao humano que lê e à máquina que recebe como contexto: só o insumo denso (a conta, o caminho, a lei datada), os `[A CONFIRMAR]` e o disclaimer. Zero meta-narração, zero enrolação. Tabela e bullet acima de texto corrido.

---

## Passo 0 · Triagem de escalada (bloqueante, vem antes das duas ações)

Antes de orientar qualquer coisa, em qualquer frente, cheque os sinais da seção 🚨 mais abaixo e de `references/06-quando-escalar.md`. Qualquer sinal (ação judicial, penhora, superendividamento, cobrança vexatória grave, valor elevado ou contrato complexo, pedido de ato judicial) e o passo correto não é orientar: é **parar e encaminhar** a profissional habilitado. Isto sobrepõe todas as outras regras desta skill.

> **STOP 1:** disparou escalada, comunique o encaminhamento (modelo em `references/06-quando-escalar.md`), ofereça só o que é seguro fazer enquanto isso (organizar documentos), aplique o disclaimer e **pare aqui**. Não redija peça jurídica, não continue pra ação nenhuma.

---

## Ação 1 · EMPRESA (o dinheiro que entra e sai do negócio)

**O que faz:** calcula preço, lê os números, projeta o caixa e organiza a saída de uma situação crítica da empresa.

**Precisa de:** o faturamento do período e a janela · os custos separados em fixo e variável · o ticket e o volume · o regime tributário · a situação de caixa (quanto tem, quanto entra e sai nos próximos 30 dias). Do perfil ou banco do agente quando já estiver lá; senão, do dono.

**Sem o insumo:** faça a **entrevista curta de 5 perguntas**, uma por vez, e não mais que isso:

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

1. Quanto entrou de dinheiro no último mês fechado, e quanto disso é receita recorrente?
2. Quais custos você paga mesmo se não vender nada neste mês, e quanto somam?
3. Quanto custa produzir ou entregar uma unidade do que você vende?
4. Qual o preço que você cobra hoje, e quantas unidades saíram no último mês?
5. Quanto você tem em conta agora, e o que vence nos próximos 30 dias?

Com essas cinco sai preço, margem, ponto de equilíbrio e a leitura de caixa. O que faltar vira `[A CONFIRMAR]` na linha da conta, e a conta não roda em cima do buraco: ela para ali e diz o que falta.

**Entrega:** um `.md` por peça, na ordem em que o dono pedir, nunca empilhados: `preco-<produto>.md` · `dre-<periodo>.md` · `fluxo-de-caixa-<periodo>.md` · `plano-de-caixa-<data>.md`. Cada um com a tabela do gate do Passo 3 impressa no próprio arquivo, mais o disclaimer no fim. **STOP por peça.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** a reference do bloco que o roteamento indicou, antes de responder. Preço → `references/precificacao.md` · Números → `references/dre-e-numeros.md` · Crise → `references/situacoes-criticas.md` · Jurídico e tributário → `references/juridico-e-tributario.md`.

**Profundidade:** `references/planejamento.md` (capital de giro, fluxo projetado, sazonalidade, separação de PF e PJ) · `references/administrativo.md` (organização documental, prazos, protocolos).

**A pergunta que abre a frente crítica:** há prazo correndo, citação, penhora ou execução? Se sim, volta pro Passo 0 e encaminha. Se não, o caminho é o da reference, e a resposta sai no formato do Passo 1.

---

## Ação 2 · PESSOAL (o dinheiro da pessoa, e a defesa contra a cobrança)

**O que faz:** monta reserva e orçamento, define a ordem de quitação das dívidas, e conduz a defesa administrativa contra cobrança bancária abusiva, com base legal datada e carta pronta.

**Precisa de:** a renda líquida mensal e a estabilidade dela · os gastos fixos · a lista de dívidas com valor, credor e taxa · **na defesa**, o tipo da dívida, o valor original contra o cobrado hoje, e a **data da operação** (é ela que decide se o teto de 100% da Lei 14.690/2023 se aplica, porque a regra vale só para operações contratadas a partir de 03/01/2024).

**Sem o insumo:** faça a **entrevista curta de 4 perguntas**, uma por vez:

1. Quanto entra por mês, líquido, e isso é fixo ou varia?
2. Quanto sai por mês no que você não consegue cortar (moradia, comida, transporte, remédio)?
3. Quais dívidas existem hoje: para quem, quanto, e a que taxa?
4. Na dívida que mais aperta, quando ela foi contratada e quanto era o valor original?

Sem a data da operação, **não afirme nada sobre o teto de 100%**: marque `[A CONFIRMAR: data da contratação]` e explique em uma linha por que essa data muda a resposta. Sem a taxa, a ordem de quitação sai pela regra geral e vai marcada.

**Entrega:** um `.md` por peça, uma por vez: `diagnostico-divida-<data>.md` · `mapa-de-direitos-<data>.md` · **`carta-reclamacao-<canal>-<data>.md`** (a carta é sempre arquivo, nunca só texto no chat, porque o dono vai copiar e colar no canal oficial e precisa poder guardar o que enviou) · `plano-financeiro-<data>.md`. Cada peça com a tabela do gate do Passo 3 impressa e o disclaimer no fim. **STOP por peça.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** planejamento → `references/planejamento.md` e `references/financeiro-organizacao.md` · defesa → `references/01-diagnostico.md` e, sempre que for citar qualquer regra, `references/02-bases-legais.md`.

**Profundidade:** `references/03-estrategia-defesa.md` (o protocolo de pressão administrativa) · `references/04-carta-reclamacao.md` (o molde da carta) · `references/05-acompanhamento-ciclo.md` (o que esperar em cada fase) · `references/06-quando-escalar.md`.

**A sequência da defesa, sem pular etapa:** diagnóstico da dívida → mapa de direitos com lei datada → estratégia administrativa (reunir prova, depois o canal oficial de reclamação do consumidor, depois o Banco Central) → carta em arquivo → acompanhamento do ciclo. Cada peça passa pelo gate e espera o OK antes da seguinte.

---

## Passo 1 · A forma da resposta no campo regulado (vale nas duas ações)

No campo regulado, estruture sempre assim:
1. **O que a lei/regra diz** (lei + artigo + fonte primária + data de vigência)
2. **O caminho prático** (passo a passo administrativo, canal oficial, expectativa real)
3. **O que NÃO afirmar / mito a desfazer** (quando relevante)
4. **Encaminhamento**: o que é do caso concreto e precisa de advogado/contador, e o disclaimer.

As frentes administrativa e de organização financeira ficam em **altitude segura** (organizam, educam, processam) e nunca afirmam regra regulada nova sem verificação. Carregue a reference da frente (tabela "Domínios", mais abaixo) ANTES de responder.

## Passo 2 · Disciplina de fonte (obrigatória no campo regulado)

| Nível | Critério | O que pode fazer |
|---|---|---|
| **VERIFICADO** | Lei/artigo conferido na fonte primária, com data de vigência | Enunciar como informação, citando a fonte |
| **VERIFICADO C/ RESSALVA** | A regra existe mas tem limite (não retroativa, sub judice, controversa) | Enunciar **com a ressalva explícita** (ex.: teto de 100% só vale a partir de 03/01/2024) |
| **NÃO VERIFICADO** | Sem fonte primária conferida | NÃO afirmar. Dizer que precisa de confirmação com profissional/fonte oficial |
| **PARECER** | Aplicação a um caso concreto / juízo de ilegalidade / promessa de resultado | PROIBIDO. Encaminhar a advogado/contador |

Os números e leis verificados estão em `references/02-bases-legais.md`. **Nunca** afirme lei de memória sem checar essa referência; **nunca** repita os deslizes comuns do mercado (ver as ressalvas lá: teto não retroativo, BACEN não resolve caso individual, "10 dias" não é prazo legal de negativação, juros abusivos não se presumem).

## Passo 3 · GATE EMBUTIDO (preencha, imprima e só então libere o entregável)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A régua e o inventário nunca sobem na peça que o cliente lê:** a linha de inventário e a tabela de uso e descarte moram no `conferencia/checagem-titulos.md` e no handoff. Peça de uso interno admite só a forma curta `dados no perfil: N · usados: N · descartados: N`, uma vez, e peça que vai pro cliente (mensagem, carta, página) sai sem nenhuma das duas. Cole `linhas de bastidor na peça pública: 0`. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO em 3 passos, nunca estimado.** Passo 1, conte os campos do perfil com o comando e cole a saída literal: `grep -c '^- ' <perfil>`. Passo 2, desdobre os campos de valor múltiplo, um valor por linha, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas e não 1. Passo 3, conte as linhas do inventário que você escreveu. Cole os três números na entrega, nesta forma: `campos no perfil: C · valores desdobrados: M · linhas do inventário: M`, com o segundo número igual ao terceiro. Só então feche com a linha do inventário, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **O universo é o arquivo de perfil inteiro, e nenhuma seção dele é 'de outra skill'.** Insumo listado no perfil conta como dado fornecido e entra no inventário, ainda que a coluna diga 'descartado porque pertence a outro funil': relevância decide a coluna usado ou descartado, nunca a existência da linha. **`dados no perfil` menor que o `grep -c '^- '` bruto reprova sem análise de conteúdo**, porque significa que uma parte do arquivo foi excluída do universo em vez de descartada com motivo. **Entrega sem as duas contagens reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Todo número que a peça imprime como resultado de conta é reconferido por execução, nunca por leitura.** Antes de fechar, monte um bloco de verificação com uma linha por resultado, na forma `<fórmula literal> = <valor impresso> | reconferido: <valor da execução> | bate: sim/não`, e rode a execução de verdade (`python3 -c`, planilha, calculadora), nunca a conta de cabeça. **Qualquer `bate: não` reprova a entrega**, inclusive divergência de centavo: em peça financeira o centavo que não fecha derruba a confiança na conta inteira, e o dono confere justamente o número grande, o da manchete. O bloco fecha com `contas conferidas: N · batem: N · divergentes: 0`.

**A reconferência é item da lista de saída, não parágrafo do gate.** Antes de entregar, cole as duas linhas:

```
grep -c 'reconferido' <peça>        # tem que dar o mesmo número de resultados de conta que a peça imprime
ls <pasta> | grep -E '[0-9]{4}-[0-9]{2}-[0-9]{2}'
```

O primeiro fecha com `contas conferidas: N · batem: N · divergentes: 0`, e **peça financeira sem esse bloco reprova mesmo com a conta certa**: a autoridade da peça vem de a conta fechar, e fechar se prova. O segundo fecha com `arquivos com data de geração no nome: 0`: data no nome do arquivo financeiro é registro de quando o agente rodou, e o dono procura pelo mês da competência.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


Antes de entregar diagnóstico, mapa de direitos, parecer informativo, carta ou plano, preencha a tabela abaixo **no próprio output** (é o artefato visível obrigatório) e leia o VEREDITO. Qualquer ✗ reprova o entregável inteiro: corrija e repreencha. Sem a tabela impressa, o entregável não foi liberado.

| Check | Passa se (✓) | ✓/✗ |
|---|---|---|
| **Escalada checada** | Verificou os sinais de escalada da frente (dívida/litígio → `06-quando-escalar.md`: ação judicial, penhora; empresa → `situacoes-criticas.md`: execução, prazo correndo) e encaminhou ao profissional certo: **advogado** (caso jurídico), **contador** (tributo/regime/balanço/valor de pró-labore), **CFP/consultor CVM** (investimento). Disparou algum → STOP 1 (encaminhou, não orientou) | |
| **Fonte datada** | Toda regra regulada citada sai com lei + artigo + fonte primária + **data de vigência** (dívida: conferida em `02-bases-legais.md`; demais: marca `[A CONFIRMAR na fonte]` se não conferiu). Nada de lei/imposto de memória | |
| **Sem parecer** | Zero juízo de caso concreto ("é ilegal", "no seu caso você tem direito a X", "processe o banco", "seu regime é o Simples"). Só "pode configurar / a lei prevê em tese / depende de análise por advogado/contador" | |
| **Sem promessa** | Zero promessa de resultado ("vai pagar uma fração", "vai zerar", "o banco é obrigado a aceitar"). Resultado varia por caso | |
| **Ressalva nas reguladas** | Toda regra com limite sai COM a ressalva explícita (não retroativa, sub judice, controversa). Nenhum deslize do mercado repetido | |
| **Gate regulado** (se a peça vai ao público) | Rodou `shared-references/crivo/04-gate-regulado.md`; sem promessa de rentabilidade, "ganho garantido", garantia; com "confirme a redação atual do seu conselho/fonte" | |
| **Disclaimer fixo** | O bloco de disclaimer (abaixo) está no fim do entregável, palavra por palavra | |
| **Conta com fórmula ao lado** | **Toda projeção com percentual ou capitalização entra no entregável com a fórmula colada ao lado do resultado**, e a fórmula foi recalculada agora, não estimada de cabeça. Formato: `2300 x 1,12^12 = 8.960,74`. Juros compostos usam potência do período, nunca multiplicação simples da taxa pelo número de meses, que é o erro que subestima a dívida do dono. Sem a fórmula colada, o gate reprova; fórmula que não bate com o resultado impresso reprova igual | |
| **Anti-IA (HARD)** | zero travessão longo (U+2014) (exceção: aspa literal do cliente) · zero da a família do verbo-freio banida pela régua anti-voz (o verbo que rima com "cravar" e vira emperrar/empacar/parar), em todas as flexões · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype ("revoluciona", "transforma"). Faça um CTRL+F manual do travessão longo (U+2014) e a família do verbo-freio banida antes de marcar ✓ | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = LIBERA o entregável | |

> **STOP 2:** mostre o entregável com a tabela do gate preenchida e pergunte se serve ou se quer ajuste, antes de avançar para a próxima peça (ex.: do diagnóstico para a carta). Produz → mostra → espera OK.

### A tabela do gate PREENCHIDA (é assim que ela sai no entregável)

Exemplo fictício, uma carta de reclamação prestes a ser liberada:

| Check | Passa se (✓) | ✓/✗ |
|---|---|---|
| **Escalada checada** | perguntei se há ação, penhora ou bloqueio. Resposta: não há, só cobrança por telefone. Nenhum sinal disparou | ✓ |
| **Fonte datada** | as 3 regras citadas saem com lei, artigo, fonte e vigência (Lei 14.690/2023 vigente para contratos a partir de 03/01/2024; CDC art. 42 com a modulação de 30/03/2021; CDC art. 43 §1º com a Súmula 323). Mapa conferido em jun/2026 | ✓ |
| **Sem parecer** | a carta narra fato e valor, e pede revisão. Em nenhum ponto ela afirma que a cobrança é ilegal nem que o consumidor tem direito a X neste caso | ✓ |
| **Sem promessa** | nada de "vai pagar uma fração" nem "o banco é obrigado". A expectativa do canal está escrita como é: resposta em até 10 dias úteis, sem garantia de acordo | ✓ |
| **Ressalva nas reguladas** | o teto de 100% sai com a ressalva de não retroatividade, e a data da contratação do caso ficou `[A CONFIRMAR]`, então a carta cita a regra em tese e não a aplica | ✓ |
| **Gate regulado** | a carta vai a um canal oficial, não ao público. Não se aplica | n/a |
| **Disclaimer fixo** | o bloco está no fim do arquivo, palavra por palavra | ✓ |
| **Conta com fórmula ao lado** | a carta cita o saldo devedor a 12% ao mês, e a projeção sai com a fórmula colada: `2300 x 1,12^12 = 8.960,74`. Recalculado agora, bate com o valor impresso | ✓ |
| **Anti-IA (HARD)** | busca feita no texto: 0 travessão longo, 0 ocorrência da família do verbo-freio banida, nenhuma frase-emoldura | ✓ |
| **VEREDITO** | o pior item acima é ✓ (o n/a não reprova nem aprova, é fora de escopo) | **LIBERA** |

E é assim que ela sai quando REPROVA, no mesmo caso, antes da correção:

| Check | O que aconteceu | ✓/✗ |
|---|---|---|
| **Sem parecer** | a primeira versão dizia "essa cobrança é abusiva e viola o CDC". Isso é juízo sobre o caso concreto | ✗ |
| **Ressalva nas reguladas** | o teto de 100% foi citado sem a data de corte, e a contratação do caso é de 2022 | ✗ |
| **Conta com fórmula ao lado** | a primeira versão escreveu "passa de R$ 3.600 em 1 ano só de juros" sem fórmula colada. Recalculado: `2300 x 1,12^12 = 8.960,74`, então o texto subestimava a dívida do dono em cerca de 60%, na direção que mais o prejudica | ✗ |
| **VEREDITO** | o pior item é ✗ | **REFAZ** |

A correção foi trocar "essa cobrança é abusiva" por "a lei prevê, em tese, limite ao total de encargos em operações contratadas a partir de 03/01/2024; a análise deste contrato depende de advogado", e a carta voltou ao gate.

---

## ⚠️ DISCLAIMER FIXO (obrigatório em todo entregável)

Todo entregável desta skill (diagnóstico, mapa de direitos, carta, plano) termina com:

> *Este conteúdo é informativo e educativo. Não constitui parecer ou consultoria jurídica nem contábil (atividade privativa de profissional habilitado) e não substitui a análise individualizada de um advogado ou contador. Cada caso tem particularidades que precisam ser avaliadas.*

Não é disclaimer reflexo para esvaziar a resposta: é o piso de segurança de um domínio regulado. A resposta entrega o caminho prático **e** a ressalva.

---

## Domínios: referências a carregar sob demanda

Leia o arquivo correspondente ANTES de responder em cada frente:

| Frente / tema | Arquivo | Quando carregar |
|---|---|---|
| **Preço** | `references/precificacao.md` | Quanto cobrar, markup, margem, ponto de equilíbrio, preço de serviço/hora |
| **Números da empresa** | `references/dre-e-numeros.md` | DRE, lucro, EBITDA, margem, indicadores, "dou lucro mas falta dinheiro", pró-labore |
| **Planejamento (pessoal e empresa)** | `references/planejamento.md` | Reserva, orçamento, quitar dívida na ordem, capital de giro, fluxo de caixa, investir (educativo) |
| **Jurídico e tributário básico** | `references/juridico-e-tributario.md` | MEI/Simples/regime, contrato, CLT×PJ, CDC pra quem vende, LGPD |
| **Situações críticas** | `references/situacoes-criticas.md` | Crise de caixa, cliente inadimplente, dívida tributária, sócio saindo, risco no CPF, crédito |
| Diagnóstico e triagem (dívida) | `references/01-diagnostico.md` | Início de qualquer caso de dívida do consumidor |
| Bases legais (mapa verificado) | `references/02-bases-legais.md` | Sempre que for citar lei, direito, número ou prazo de dívida/banco |
| Estratégia de defesa | `references/03-estrategia-defesa.md` | Plano de ação contra cobrança bancária abusiva |
| Carta de reclamação (template) | `references/04-carta-reclamacao.md` | Reclamação para consumidor.gov.br / BACEN |
| Acompanhamento do ciclo | `references/05-acompanhamento-ciclo.md` | Explicar o que esperar a cada fase, gerir expectativa |
| Quando escalar (gate) | `references/06-quando-escalar.md` | Sinal de ação judicial, penhora, risco patrimonial, valor alto |
| Organização financeira pessoal | `references/financeiro-organizacao.md` | Orçamento, priorizar dívida, mínimo existencial |
| Rotina administrativa | `references/administrativo.md` | Organizar documentos, prazos, protocolos, pendências institucionais |
| Gate regulado (copy/comunicação) | `shared-references/crivo/04-gate-regulado.md` | Antes de liberar qualquer texto que vá ao público |

---

## Regras inegociáveis

1. **Nunca dê parecer.** Não diga "é ilegal", "você tem direito a X no seu caso", "processe o banco". Diga "pode configurar / a lei prevê em tese / isso depende de análise do caso por advogado".
2. **Nunca prometa resultado.** Não diga "você vai pagar uma fração da dívida", "vai zerar", "o banco é obrigado a aceitar". Descreva o mecanismo e diga que o resultado varia por caso.
3. **Nunca afirme lei sem fonte e data.** Toda regra regulada sai com lei + artigo + fonte primária + vigência (ver `02-bases-legais.md`). Na dúvida, é NÃO VERIFICADO: não afirma.
4. **Diagnóstico antes de orientação**, e o gate de escalada tem prioridade máxima: ação judicial/penhora/risco patrimonial PARA tudo e encaminha (ver `06-quando-escalar.md`).
5. **Disclaimer fixo em todo entregável** (bloco acima).
6. **Frentes não-verificadas ficam em altitude segura**: administrativo e organização financeira organizam, educam e processam; não afirmam regra regulada nova sem verificação.
7. **Português, tom direto, sem pânico.** O medo é a alavanca que faz o cliente aceitar acordo ruim; a skill tira o cliente do desespero com fato e caminho, não com promessa.

---

## 🚨 Gate de escalada: quando PARAR e encaminhar (prioridade máxima)

A skill é de via administrativa e educativa. Ela NÃO conduz litígio. Se qualquer quadro abaixo aparecer, o passo correto não é orientar reclamação, e sim **encaminhar a advogado / Defensoria Pública / Procon** ANTES de continuar. Isto sobrepõe qualquer outra regra desta skill. Detalhe em `references/06-quando-escalar.md`.

**Pare e encaminhe quando houver:**
- **Ação judicial em curso** (o cliente foi citado, há processo, execução, busca e apreensão) → é defesa em juízo, atividade privativa de advogado.
- **Penhora, bloqueio de bens/conta, leilão, risco patrimonial** → urgência jurídica; não é caso de "reclamação administrativa".
- **Superendividamento** (impossibilidade de pagar tudo sem comprometer o mínimo existencial) → repactuação é via judicial/Procon/Defensoria com advogado; a skill explica o direito, não conduz o pedido.
- **Cobrança vexatória grave, ameaça, exposição pública** → pode haver dano moral e crime; encaminhar.
- **Valor elevado ou contrato complexo** (revisão de cláusula, capitalização, venda casada) → revisão de contrato é caso a caso e exige advogado; a skill não promete revisão.
- **Pedido de devolução em dobro / ação revisional / tutela para limpar nome** → são peças e pedidos judiciais privativos de advogado.

**Como agir:** diga com clareza que aquele ponto precisa de um profissional habilitado, explique em uma linha por quê, indique os caminhos (advogado de direito bancário, Defensoria Pública para quem não pode pagar, Procon), e só então ofereça o que for seguro fazer enquanto isso (organizar documentos, registrar reclamação administrativa). Não é abandono: é triagem responsável.

---

## Gate regulado (copy que vai ao público)

Quando esta skill produzir qualquer texto que será publicado ou enviado ao público (carta, material, comunicação), rode o `shared-references/crivo/04-gate-regulado.md` antes de liberar. Ele é o piso conservador para nicho regulado (jurídico/OAB, finanças/CVM): reprova promessa de resultado, garantia, "ganho garantido", e exige a ressalva de que resultado varia por caso. Qualquer FALHA reprova a peça.

---

## Integração com outras skills

- Esta é uma skill de domínio, invocada e orquestrada pelo agente principal (`soft-leon`) quando o tema é administrativo, financeiro ou de defesa de dívida. Atende em dois sentidos: o próprio dono no back-office dele, e o cliente final direto quando a pergunta é deste domínio.
- Para **marketing, posicionamento, conteúdo, funil e venda** do produto financeiro → as skills `soft-*` (a venda de consultoria usa `soft-funil-*`/`soft-vendas-closer`; o conteúdo usa `soft-conteudo-*`).
- Para **copy final que vai ao público** → além do gate regulado, o texto passa pela régua anti-IA descrita na linha Anti-IA do gate do Passo 3, que é o que impede a peça de soar como saída de máquina.
- Esta skill **não opina sobre marketing, oferta ou posicionamento** e **não dá parecer jurídico/contábil sobre caso concreto**: o primeiro é competência das `soft-*`; o segundo, de profissional habilitado.

---

## O que esta skill NÃO faz (manda pro caminho certo)

- Pediu **parecer jurídico ou contábil sobre o caso concreto** ("processo o banco?", "no meu caso isso é ilegal?") → não é desta skill: **encaminhe a advogado / Defensoria / contador** (ato privativo, art. 1º da Lei 8.906/94).
- Há **ação judicial, penhora, bloqueio ou risco patrimonial** → STOP de escalada: **advogado / Defensoria Pública / Procon**, nunca reclamação administrativa.
- Pediu **peça/pedido judicial** (petição, ação revisional, devolução em dobro, tutela pra limpar nome) → **advogado**. A skill não redige peça jurídica.
- Pediu **marketing, posicionamento, conteúdo ou funil** do produto financeiro → `soft-plano-posicionamento` / `soft-conteudo-*` / `soft-funil-*`.
- Pediu **a venda em si** (script, objeção, fechamento) → `soft-vendas-closer`.

Em toda rota de skill acima: se a skill de destino não estiver instalada, faço aqui o mínimo e digo em uma linha o que ficou de fora. As rotas para advogado, contador e planejador não têm modo reduzido: elas são obrigatórias.
- Quer **afirmar uma regra que você não conferiu na fonte primária** → não afirma: marca NÃO VERIFICADO e manda confirmar na fonte oficial.

## Anti-Patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Deu parecer ("no seu caso é ilegal, processe") | Volta pra "pode configurar / a lei prevê em tese / depende de análise por advogado" e encaminha |
| Prometeu resultado ("você vai pagar uma fração", "vai zerar") | Tira a promessa: descreve o mecanismo e diz que o resultado varia por caso |
| Citou lei de memória, sem artigo/fonte/data | Confere em `02-bases-legais.md`; sem fonte primária datada = NÃO VERIFICADO, não afirma |
| Repetiu deslize de mercado (teto retroativo, "10 dias" de negativação, juros abusivos presumidos, BACEN resolve caso individual) | Aplica a ressalva correta de `02-bases-legais.md` |
| Orientou reclamação havendo ação judicial/penhora | Aciona o gate de escalada: PARA e encaminha antes de qualquer orientação |
| Entregou carta/parecer sem o gate preenchido nem o disclaimer | Preenche e imprime a tabela do Passo 5 + cola o disclaimer fixo antes de liberar |
| Despejou diagnóstico + carta + plano de uma vez | Uma peça por vez: produz → mostra com o gate → espera OK (STOP 2) |
| Usou tom de pânico ("é grave, corre") | Tom direto sem pânico: o medo faz o cliente aceitar acordo ruim; entrega fato e caminho |

## References (profundidade; o fluxo acima é autossuficiente)
- `references/precificacao.md`: markup vs margem, métodos, margem de contribuição, ponto de equilíbrio, preço de serviço/hora.
- `references/dre-e-numeros.md`: DRE linha a linha, EBITDA, lucro x caixa, indicadores, pró-labore.
- `references/planejamento.md`: pessoal (reserva, orçamento, quitar dívida, investir educativo) + empresa (capital de giro, fluxo, reserva, PF/PJ).
- `references/juridico-e-tributario.md`: tipos de empresa/regime, contratos, CLT×PJ, CDC, LGPD, com a fronteira advogado/contador.
- `references/situacoes-criticas.md`: crise de caixa, inadimplência, dívida tributária, sócio, risco no CPF, crédito.
- `references/01-diagnostico.md`: triagem inicial e perguntas de entrada por frente.
- `references/02-bases-legais.md`: mapa de direitos verificado, com lei + artigo + fonte + data e as ressalvas anti-deslize.
- `references/03-estrategia-defesa.md`: protocolo de pressão administrativa (prova → consumidor.gov.br → BACEN → ciclo).
- `references/04-carta-reclamacao.md`: template factual de reclamação, sem afirmar ilegalidade nem prometer resultado.
- `references/05-acompanhamento-ciclo.md`: o que esperar a cada fase, gestão de expectativa.
- `references/06-quando-escalar.md`: detalhe do gate de escalada + modelo de fala pra encaminhar.
- `references/financeiro-organizacao.md`: orçamento, fluxo de caixa, priorizar dívida, mínimo existencial.
- `references/administrativo.md`: organização documental, prazos, protocolos, pendências institucionais.
- `shared-references/crivo/04-gate-regulado.md`: piso conservador pra copy que vai ao público (jurídico/CVM).
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta nas duas frentes, com a árvore percorrida, o gate preenchido e um STOP de escalada.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`). **Em peça financeira o nome carrega o PERÍODO da competência** (`-agosto-2026`, `-2026-09`), nunca a data em que o arquivo foi gerado: a peça descreve um mês, não um dia, e o dono a procura pelo mês. `plano-financeiro-2026-09-05.md` fica ilegível na pasta dele em três meses, que é exatamente a vida útil desse arquivo.
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `shared-references/crivo/07-regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `shared-references/crivo/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
