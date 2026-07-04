---
name: soft-conteudo-matriz
description: Ideação de conteúdo EM LOTE do método Soft, o mapa de pautas do mês. Cruza os pilares do dono (do Plano/posicionamento) por 8 formatos de ataque e devolve 30+ pautas ESPECÍFICAS numa matriz-calendário, cada célula uma manchete-pauta ancorada no verbatim/tese do dono e que aponta pro método (nunca pauta genérica de creator). É o passo ANTES da headline, decide QUAIS temas atacar; cada célula vira input pronto pra soft-conteudo-headlines. Use quando o pedido for "me dá ideias de post", "matriz de conteúdo", "sobre o que eu posto", "pauta do mês", "calendário editorial", "ideação em lote", "planejamento de conteúdo", "banco de pautas", "não sei o que postar essa semana". NÃO use pra a HEADLINE/gancho de UMA pauta já escolhida (soft-conteudo-headlines), nem pro CORPO da peça (soft-conteudo-carrossel/-reels/-stories), nem pra DEFINIR os pilares/círculo temático/posicionamento (soft-posicionamento, os pilares vêm de lá), nem pra arte (soft-designer), nem pra carta/funil (soft-funil) ou venda (soft-vendas-closer).
---

# Matriz de Conteúdo, o mapa de pautas do mês

Ter posicionamento e voz não resolve o "sobre o que eu posto essa semana". O dono empaca na frente da tela com 5 pilares certos e nenhuma pauta concreta. Esta skill fecha esse buraco: pega os pilares (que a **soft-posicionamento** já definiu) e os multiplica em **30+ pautas específicas** cruzando cada pilar por 8 formatos de ataque. O resultado é o calendário de conteúdo do mês, cada linha pronta pra virar peça.

**O que esta skill faz por você:** transforma pilar (tema amplo) em pauta (manchete específica que já carrega a tese). Ela **decide QUAIS temas atacar**; ela NÃO escreve a headline nem o corpo. É o degrau anterior: cada célula da matriz é um input limpo pra soft-conteudo-headlines.

**A fronteira (não invada):** os PILARES e o círculo temático nascem na **soft-posicionamento** (é lá que se decide o universo do que o dono tem permissão de falar). Esta skill MULTIPLICA os pilares em pautas. As skills de peça (carrossel/reel/stories) ESCREVEM a pauta. Se o dono não tem pilares, você não inventa: puxa do Plano ou manda fazer o Plano primeiro.

**As 6 leis (valem antes de tudo, detalhe em `shared-references/operacao-padrao.md` Seção 0):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil; (2) abre ensinando o que faz; (3) é consultiva, puxa os pilares antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: pilar, fala ou número que você não tem vira `[A CONFIRMAR]`, jamais pauta plausível; (6) **doc de output enxuto pros 2 leitores**: a matriz que sai é otimizada pro humano que planeja E pra IA que recebe a célula como contexto da headline.

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos STOPs, e rode o gate por dentro antes de mostrar a matriz.**

## Output Contract (o que você entrega)
- Uma **matriz-calendário**: linhas = os 3-5 pilares do dono, colunas = os 8 formatos de ataque (abaixo). Cada célula = **uma manchete-pauta específica**, não um tema. Bom: "Os 3 sinais na primeira reunião de que o cliente vai pedir desconto." Ruim: "Fechamento de vendas."
- **Mínimo 30 pautas** (5 pilares × 6 formatos, ou 4 × 8). Toda célula é distinta: a mesma ideia NÃO se repete em dois pilares.
- Cada pauta **nasce de dor/desejo real do avatar** (verbatim quando existe) e **aponta pra uma lacuna que fecha no método do dono**. Pauta que qualquer creator do nicho postaria = reprovada.
- Abaixo da matriz: **as 3 pautas mais fortes** apontadas (com 1 linha de porquê cada) + a nota de qual pilar está mais raso pra pedir mais insumo.
- Você **para e espera** o dono escolher/ajustar antes de gerar volume ou passar uma célula pra headline.
- Você **nunca inventa pilar, fala nem número** e **nunca mostra pauta que falhou no gate**.

## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a matriz no chat)
Regra dura: o RESULTADO é **UM documento markdown consolidado** (a matriz-calendário). No **claude.ai**, um **artifact de markdown** (o dono abre, copia, planeja o mês); no **Claude Code**, um arquivo `.md`; no **agente/Telegram**, um ARQUIVO cujo path completo vai na resposta. A CONDUÇÃO (puxar pilares, os STOPs) acontece no chat; a MATRIZ mora no DOC. Ao parar num STOP, você mostra/atualiza o DOC e pergunta "ajusto?"; NUNCA reescreve a matriz em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Os 3 ambientes (como a entrega muda)
- **App/chat (claude.ai, sem Bash):** a matriz sai como **artifact de markdown**. Sem tabela em bloco de código (grade 5×8 vira texto monoespaçado ilegível): tabela markdown que renderiza.
- **Claude Code (tem Write/Edit):** salva em `matriz-conteudo-AAAA-MM-DD.md` na working dir + roda `scripts/lint_copy.py` na matriz como cinto anti-IA. Confirma o path pro dono.
- **Agente/Telegram (tem Bash):** grava o `.md` e devolve **o path completo na resposta**, mais um resumo curto SEM markdown pesado (as 3 pautas mais fortes em texto corrido, sem tabela nem asteriscos). A matriz inteira mora no arquivo.

## Passo 0, puxa os pilares (NÃO PULE, é a fronteira)
Procura os pilares nesta ordem: **Plano de posicionamento colado na conversa** → **descrição do projeto** → **mensagens anteriores**. Cada pilar do Plano já traz nome, tema central, valor ancorado, anti-valor/inimigo, formato preferencial (é o que a soft-posicionamento entrega).

Três estados de entrada (declara qual é o seu):
- **Tem os pilares (do Plano):** usa eles como as linhas da matriz. Caminho ideal. Puxa junto o verbatim de dor/desejo do Plano pra ancorar as células.
- **Tem nicho/fundação mas pilares não estão nomeados:** propõe **3-4 pilares** derivados da fundação (usando os 4 tipos: Método, Diagnóstico, Tese, Bastidor, em `shared-references` não; a lógica está resumida no Passo 0.1) e **PARA pra o dono confirmar** antes de montar a matriz. Não trata proposta como fato.
- **Sem nada:** pergunta numa única mensagem (nicho em 1 linha + os 3-4 assuntos que ele mais fala) e, se o pedido for maior que pauta, avisa que o Plano na **soft-posicionamento** deixa a matriz muito mais cravada.

**Regra de fronteira:** você NÃO define círculo temático nem reescreve posicionamento aqui. Se o dono quer decidir o universo de temas, isso é soft-posicionamento. Aqui os pilares entram como dados de entrada.

### Passo 0.1, os 4 tipos de pilar (só pra propor quando faltam)
Quando você precisa propor pilares (2º estado acima), use combinação destes 4, nunca "motivacional/notícias/vida pessoal" (esses falham pro Soft): **Método** (o sistema do trabalho, autoridade+venda) · **Diagnóstico** (o problema do cliente visto de perto, identificação) · **Tese/Opinião** (postura contraintuitiva sobre o mercado, diferenciação) · **Bastidor** (rotina/ferramenta/decisão, intimidade controlada). A maioria combina 2-3. Cada pilar proposto tem que ser **inconfundível com o de outro creator** (se o concorrente copia, é genérico, refaz).

## Passo 1, os 8 formatos de ataque (as colunas)
Cada formato é um ÂNGULO diferente de atacar o mesmo pilar. Reescritos na doutrina Soft: todo formato **filtra e atrai o cliente certo** e **aponta pro método**, nunca é jornalismo neutro nem frase de boteco. (Note: o formato "motivacional/inspiração" foi cortado de propósito, atrai estranho e não filtra.)

| # | Formato de ataque | O que a pauta faz | Camada de consciência que serve |
|---|---|---|---|
| 1 | **Acionável** | passo a passo ultra específico que ensina UMA coisa e mostra a lacuna que só o método fecha | quem já sente a dor (C2) |
| 2 | **Diagnóstico** | mostra o problema do avatar visto de perto, nomeia a dor que ele ainda não nomeou | quem não sabe que tem o problema (C1) |
| 3 | **Analítico** | destrincha POR QUE algo funciona/quebra do jeito que funciona (o mecanismo por trás) | quem desconfia mas não entende (C2) |
| 4 | **Contrário** | vira do avesso um conselho aceito do nicho e sustenta o ponto com prova | quem já tentou o caminho comum e empacou (C3) |
| 5 | **Observação** | uma tendência silenciosa/escondida que o dono notou e ninguém comenta | quem está dentro do universo (C2/C3) |
| 6 | **X vs Y** | compara dois caminhos (método antigo vs o seu, ferramenta vs ferramenta) e mostra o custo do lado errado | quem está decidindo (C3) |
| 7 | **Antes vs Depois** | o estado atual doloroso vs o estado com o método, com o número que prova a virada | quem quer o resultado (C3) |
| 8 | **Lista** | X erros/sinais/passos/itens, cada um uma pauta-semente que rende peça própria | qualquer camada, alto salvamento |

**Como escolher quantas colunas:** 5 pilares × 6 formatos = 30 pautas (corta os 2 formatos que menos servem ao nicho). 4 pilares × 8 = 32. 3 pilares × 8 = 24, então gera 2 pautas em alguns formatos pra fechar 30+. Sempre **mínimo 30**.

## Passo 2, preenche cada célula com uma manchete-pauta específica
Pra cada cruzamento pilar × formato, escreve **uma manchete-pauta** (não um tema). Regras:
- **Ancora no verbatim** (dor/desejo real do avatar, do Plano). A pauta nasce de uma fala do cliente, quase intacta. Sem fala real: ancora em prova/mecanismo do dono e marca o número não confirmado como `[A CONFIRMAR]`.
- **Aponta pro método:** cada pauta deixa uma lacuna que fecha no que o dono vende. Pauta que resolve tudo de graça e não puxa pro método = jornalismo, reprova.
- **Específica, não tema:** ✓ "O que fazer quando o cliente some depois do orçamento (o roteiro de 2 mensagens)" · ✗ "Follow-up".
- **Distinta entre pilares:** a mesma ideia NÃO aparece em duas células. Se dois pilares puxam a mesma pauta, um dos dois muda de ângulo.
- **Vocabulário do cliente final** (nunca "lead/funil/ticket" na manchete), tom de comando, número em algarismo.
- A célula é curta (uma manchete, não um parágrafo): ela vira o INPUT da soft-conteudo-headlines, que aí escreve 2-3 headlines dentro dela.

## Passo 3, roda o GATE por dentro (auditoria interna, NÃO imprime)
Roda o gate em CADA célula internamente. Só pauta que passa em TODOS os critérios entra na matriz. Uma falha refaz a célula (não a matriz). A tabela é teu **checklist interno**, nunca a saída.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Específica (manchete, não tema)** | dá pra ver a cena/o número; NÃO é rótulo amplo ("vendas", "mindset") | |
| **Ancorada** | nasce de fala real do avatar (verbatim) OU de prova real do dono; número inventado/plausível = ✗; sem fonte, marca `[A CONFIRMAR]` | |
| **Aponta pro método** | deixa lacuna que fecha no que o dono vende; NÃO é conselho neutro que resolve tudo de graça | |
| **Distinta** | essa ideia não aparece em outra célula da matriz | |
| **Cabe no pilar** | responde "por que me seguir / por que comprar de mim" dentro do universo do dono; tema fora do círculo = ✗ (é da soft-posicionamento decidir isso) | |
| **Filtra o cliente certo** | atrai quem compra, não estranho; ✗ pauta viral genérica ("5 hábitos de gente de sucesso") | |
| **Clareza (Lei 1)** | dá pra entender sem já ser de dentro; zero palavra difícil, zero figura vazia | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, destrava, transforma"). No chat/agente sem lint, faz CTRL+F manual de "—" e "travar" | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ a célula. Só tudo-✓ entra na matriz. | |

## Passo 4, monta a matriz e aponta as mais fortes
Renderiza a matriz-calendário (tabela markdown: pilares nas linhas, formatos nas colunas, célula = manchete-pauta). Abaixo dela: **as 3 pautas mais fortes de toda a matriz** com 1 linha de porquê cada (a que mais fecha no método, a mais ancorada em dor, a mais contrária), e a **nota de qual pilar ficou mais raso** (pra pedir insumo). Não narra o fluxo, entrega limpo.

## Passo 5, mostra e PARA
Mostra a matriz **no DOC** (nunca solta no chat). Pergunta: "quais pautas te servem? quer que eu escreva a headline de alguma (passo pra soft-conteudo-headlines) ou gero mais numa linha?". **Espera a escolha** antes de gerar volume ou passar pra headline.

## Exemplo denso (nicho: consultor de gestão pra dono de PME), LABEL, não copiar
Pilar 2 (Diagnóstico) × Formato 2 (Diagnóstico de dor):
> **"O dono de PME que aprova cada compra de R$50 e não vê o rombo de R$8 mil por mês no processo que ninguém revisa."**
- **Ancorada:** verbatim real "eu controlo tudo mas o dinheiro some" (N=4 na super-pesquisa). Nasce quase intacta dessa fala.
- **Aponta pro método:** a lacuna (não é gastar menos, é o processo cego) fecha no "sistema mínimo de gestão" que o consultor vende.
- **Específica:** dá pra ver (R$50 aprovado, R$8 mil somem), não é "gestão financeira".
- **Filtra:** fala com dono que decide tudo sozinho (o cliente), não com quem quer dica de app de finanças.
- **Anti-IA:** zero travessão, zero "travar", zero frase-emoldura. PASSA.

Contra-exemplo (REPROVA): "5 dicas de produtividade pra empreendedor." Genérica (qualquer creator posta), não aponta pro método, não filtra, não ancora em fala real. VEREDITO = ✗.

## When NOT to use (manda pra skill certa)
- Pediu a **HEADLINE/gancho** de uma pauta já escolhida → **soft-conteudo-headlines** (é o passo seguinte; cada célula da matriz é o input dela).
- Pediu o **CORPO** da peça → **soft-conteudo-carrossel** / **-reels** / **-stories**.
- Pediu pra **definir pilares / círculo temático / posicionamento** → **soft-posicionamento** (é de lá que os pilares vêm).
- Pediu **arte/visual/PNG** → **soft-designer**.
- Pediu **carta/página/venda** → **soft-funil** / **soft-vendas-closer**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Célula virou tema amplo ("Vendas", "Mindset") | Reescreve como manchete específica com cena/número que dá pra ver |
| Mesma ideia em dois pilares | Uma das células muda de ângulo; toda célula é distinta |
| Pauta genérica que qualquer creator postaria | Falha em "aponta pro método" e "filtra": reancora na dor do avatar e na lacuna do método |
| Inventou um pilar que o dono não tem | Puxa do Plano; se faltam, PROPÕE e PARA pra confirmar, nunca fixa como fato |
| Definiu círculo temático / reescreveu posicionamento | Fora do escopo: isso é soft-posicionamento; aqui pilar é dado de entrada |
| Frase motivacional / viral de boteco na célula | Cortado de propósito: atrai estranho, não filtra cliente; reescreve ancorado |
| Despejou a matriz solta no chat | A matriz sai como doc MD (artifact / arquivo / path no agente); o chat é a condução |
| Jogou a tabela dentro de bloco de código | Tabela markdown que renderiza; bloco de código vira grade ilegível |
| Menos de 30 pautas | Fecha 30+ (5×6 ou 4×8); gera 2 por formato em alguns cruzamentos se faltar |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `shared-references/operacao-padrao.md`: as 6 leis (Seção 0) + regras de tom/economia/entrega. Consulta na 1ª invocação da sessão.
- `shared-references/filtro-anti-ia/`: o banco de padrões banidos + falsos-positivos que alimenta o check Anti-IA do gate.
- `scripts/lint_copy.py`: no Claude Code/agente, roda `python3 scripts/lint_copy.py` na matriz como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual do gate.
