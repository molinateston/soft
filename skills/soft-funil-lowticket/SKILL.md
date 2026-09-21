---
name: soft-funil-lowticket
description: >-
  Constrói o FUNIL DE LOW-TICKET completo, a oferta de entrada paga barata (R$ 19,90 a R$ 59) pra tráfego frio que COMPRA cliente em vez de buscar lucro na primeira venda: anúncio de frio → quiz → diagnóstico → mini VSL de 3 a 6 min → mini página → checkout. É funil mais a copy do low-ticket. Use quando o pedido for: "oferta de entrada", "produto de entrada", "low ticket", "low-ticket", "tripwire", "quiz de venda", "mini VSL", "mini página de vendas", "funil de R$ 19,90", "porta de entrada paga", "produto barato pra tráfego frio", "auditar meu low-ticket". NÃO use pra: material GRÁTIS ou isca de captura (soft-funil-isca); empacotar a oferta como stack (soft-plano-ofertas); VSL longa ou carta de ticket alto (soft-funil-carta); página da isca (soft-funil-landing); mini-webinar (soft-funil-miniwebinar); posicionamento (soft-plano-posicionamento); verba, o que turbinar e operar a conta (soft-trafego-meta); headline isolada (soft-conteudo-headlines); arte, PNG (soft-designer). Siga o fluxo inteiro do SKILL.md.
---

# Low-ticket, a porta de entrada paga que compra cliente

O low-ticket não é um produto barato pra faturar. É a porta de entrada paga pra tráfego frio: um produto digital simples de R$ 19,90 a R$ 59 que transforma curioso em COMPRADOR no primeiro contato. Ele paga o anúncio (ou parte dele), monta base de gente que já passou o cartão, e abre a esteira. O lucro não mora na primeira venda; mora na rodada seguinte, quando o dono vende de novo pra quem já comprou.

**A premissa desta skill, dita de cara.** O método aqui foi destilado de um curso de 8 aulas de low-ticket. Ele é uma HIPÓTESE de trabalho: o curso não mostra nenhuma métrica de conversão, CPA ou retorno. A skill entrega o funil inteiro montado, mas cada peça sai marcada pra ser provada em casa real antes de servir a cliente. Nenhum número de resultado nasce aqui; todo número é do dono, com prova, ou entra como `[A CONFIRMAR: o quê]`.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela.** O passo a passo da régua de títulos está em `shared-references/crivo/07-regua-de-titulos.md`.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o posicionamento, o público e o que vende, e eu monto o funil de low-ticket inteiro). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou. Se faltar um insumo que o funil não vive sem (a promessa, o público, o mecanismo), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez, e monta o funil com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda o funil (o pilar do nicho, o formato do quiz, o vilão da mini VSL, a ancoragem do preço, o ângulo do criativo), escreve UMA linha do porquê na voz de quem ensina, pra o dono aprender a decidir sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("meu público quer emagrecer", "os clientes de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: a frase literal que um cliente falou, a dor que ele viu de perto, um resultado real com prova. Material bruto vira a âncora do funil; resposta rasa vira funil raso. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar cada peça, fecha com UMA linha: "Quer outro ângulo no criativo? Vilão mais forte na VSL? Preço ancorado diferente? Me diz o que ajustar que eu refaço só essa parte." A oferta de refino não substitui o STOP nem o gate.

## A régua zero-inventado (guarda dura, roda antes de tudo e reprova a peça)

O curso-fonte é cheio de promessa mágica que NÃO pode entrar na skill. Esta seção lista o que barrar. Toda promessa no funil precisa de lastro real do dono. Sem lastro, o trecho sai como `[A CONFIRMAR: o quê]`, nunca preenchido com o palpite mais convincente.

| O que o curso faz | Por que barra | O que entra no lugar |
|---|---|---|
| Promessa com número e prazo inventados ("R$ 3.000 por mês", "5 kg em 1 semana", "6 kg em 17 dias") | número de resultado sem prova é renda mágica | só número do dono com prova; sem prova, `[A CONFIRMAR: número]` |
| Prova científica gerada por chat de IA dentro da VSL | prova precisa existir e ser rastreável | prova real do dono, ou nenhuma prova naquele ponto |
| Números soltos sem fonte ("97% das dietas falham", "90% já viu low carb") | estatística sem fonte é invenção | corta, ou `[A CONFIRMAR: fonte]` |
| Faturamento do autor do curso ("mais de R$ 1 milhão no produto") | afirmação sem prova exibida | não entra como benchmark; nunca vira promessa da casa |
| Prova importada de nicho vizinho (print de views de vídeo alheio como credibilidade) | não prova resultado do produto | aceitável só como prova de INTERESSE do mercado, nunca de resultado |
| Hook de risco ("Monjaro de pobre", "gorda não merece casar", "truque das lésbicas") | brinca com remédio (política da Meta, ANVISA) e humilha o leitor | ângulo que não cita medicamento nem rebaixa quem lê |
| Autoridade genérica ("Universidade de Harvard" sem estudo nomeado) | apelo vazio, não rastreável | estudo nomeado do insumo do dono, ou corta |

**A checagem é COMANDO, não de cabeça.** Antes de fechar qualquer peça, rode sobre o arquivo: `grep -niE 'R\$ ?3.?000|5 ?kg|6 ?kg|17 dias|97%|90%|monjaro|harvard' <peça>`. Qualquer casamento que não seja um número do dono com prova reprova a peça e manda reescrever o trecho. Cole a saída do grep na conferência.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "vale a pena um low-ticket pro meu caso", "que produto de entrada eu faço", "escolhe o nicho" | **1 · NICHO E VALIDAÇÃO** |
| "constrói o mecanismo", "qual é o 'como' que eu vendo", "meu mecanismo serve pra frio" | **2 · MECANISMO** |
| "monta o quiz", "quiz que vende", "as perguntas do diagnóstico" | **3 · QUIZ E DIAGNÓSTICO** |
| "escreve a mini VSL", "o vídeo de 5 minutos", "o roteiro do vídeo do funil" | **4 · MINI VSL** |
| "monta a mini página", "a página de vendas curta", "o checkout" | **5 · MINI PÁGINA** |
| "os criativos de anúncio", "o hook do anúncio de frio", "o ângulo do anúncio" | **6 · CRIATIVO DE FRIO** |
| "o funil inteiro, do zero" | **1 a 6, na ordem, com parada em cada** |
| "auditar meu low-ticket que já roda" | **7 · GATE**, aplicado à peça que o dono colou |

Pedido ambíguo ("me ajuda com o low-ticket"): pergunta UMA coisa só, **"você já tem o produto e o público decididos, ou quer ajuda pra escolher?"**, mostra a tabela como cardápio e segue pela resposta.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de posicionamento, avatar, mecanismo nomeado, voz ou prova: leia do perfil do agente quando existir; se não existir, faça a entrevista curta do "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

**Marcação única de furo em toda a entrega:** `[A CONFIRMAR: o quê]`. Uma grafia só, do começo ao fim.

**Levantamento BLOQUEANTE antes de escrever (roda como a Ação 0 de ancoragem, e é COMANDO, nunca de memória).** Antes de escrever qualquer peça, LEIA o perfil e os insumos do dono e cole no processo uma linha por dado-chave, nesta forma: `<campo> | <valor encontrado> (<arquivo>:<trecho>) | ou [A CONFIRMAR] só se o ls/leitura devolveu vazio`. Os campos-chave desta skill: promessa, público, mecanismo nomeado, oferta principal e ticket, prova real, preço do produto de entrada. **Marcar `[A CONFIRMAR]` um dado que EXISTE no insumo reprova a entrega**, então rode a leitura antes de decidir e cole a saída. A tabela fecha com `campos-chave: N · encontrados no insumo: N · [A CONFIRMAR] com leitura vazia comprovada: N`, e a soma fecha em N. Só depois desta tabela a peça começa.

**O exemplo é ILUSTRATIVO, é PROIBIDO parafrasear.** `references/EXEMPLO-FIM-A-FIM.md` usa um nicho fictício só pra mostrar a FORMA. É proibido reusar as frases, os números ou o nicho dele na peça real. A peça real nasce 100% do insumo do dono; se você se pegar copiando uma frase do exemplo, pare e volte ao insumo.

**Fronteira com as skills irmãs (standalone).** Esta skill faz a oferta de ENTRADA PAGA barata e seu funil. A soft-funil-isca faz o material GRÁTIS. A soft-plano-ofertas empacota qualquer oferta como stack. Se a skill precisa de posicionamento ou de oferta e a irmã não está instalada, faz o mínimo aqui (nunca "vá fazer lá primeiro"): puxa o essencial pela entrevista curta e marca o que ficou reduzido.

---

## Ação 0 · ANCORAGEM (roda antes de qualquer ação, não pula)

**O que faz:** abre a fonte de fala real do público e puxa a matéria-prima de todo o funil.

**Precisa de:** a fonte de fala, nesta ordem: descrição do projeto → posicionamento do dono → mensagens de cliente. De lá saem **3 a 5 falas de DOR e 3 a 5 de DESEJO**, literais, com o N (quantas vezes cada uma apareceu). A ordem é manual antes de qualquer IA: fala humana primeiro cria o senso do mercado que filtra o genérico.

**Sem o insumo:** sem nenhuma fala real, **não invente**. Ancore em prova real do dono (resultado, caso, mecanismo) e avise em 1 linha que minerar 5 a 8 falas reais deixa o funil bem mais cravado. Número que não veio do briefing entra como `[A CONFIRMAR: número]`. **PARA e confirma a fonte antes de seguir.**

**A régua zero-inventado vale desde aqui.** Fala do público é substring literal da fonte. Nada de dor inventada, nada de desejo plausível. As 5 categorias pra minerar em cada fonte: (1) problema nas palavras do lead; (2) vocabulário e jargão dele; (3) o que já tentou e falhou; (4) do que reclama, inclusive a vergonha que não diria alto; (5) o que mais quer, separando o desejo dito ("emagrecer") do desejo real ("se sentir bem de novo").

**Entrega:** nada de arquivo. É a matéria-prima das ações seguintes.

**Leia primeiro:** `shared-references/crivo/01-entrada-verbatim.md` (o protocolo de ancoragem) e `references/metodo-lowticket.md`, seção 1 (as 5 categorias e a ordem manual antes de IA).

---

## Ação 1 · NICHO E VALIDAÇÃO (o produto de entrada tem demanda?)

**O que faz:** decide se o low-ticket cabe no caso do dono, escolhe o produto de entrada e valida a demanda por sinal de mercado, antes de qualquer copy.

**Precisa de:** as falas da Ação 0 · o que o dono vende de principal (o low-ticket é o degrau, o topo da esteira vem depois) · a evidência de demanda (concorrente anunciando o tema hoje).

**Sem o insumo:** sem oferta principal definida, o low-ticket não tem pra onde levar. Marque `[A CONFIRMAR: oferta principal]`, siga pela dor de top 3, e diga em 1 linha que o destino final depende disso. Sem evidência de concorrente, deixe a validação de demanda como `[A CONFIRMAR: anúncio ativo do tema]` e siga.

**Entrega:** `nicho-e-validacao.md`, com o produto de entrada proposto, os 3 pilares avaliados, o sinal de demanda e o papel dele na esteira do dono. **STOP pro OK.**

**Arquivos obrigatórios: o arquivo acima, e `conferencia/checagem-titulos.md` por último.**

**Leia primeiro:** `references/metodo-lowticket.md`, seções 1 e 2.

**Os 3 pilares do nicho (não precisa dos 3; quanto mais, mais escala):**
1. **Dor urgente e específica:** sentida todo dia. Escala mais.
2. **Conveniência ou curiosidade:** facilita a vida ou desperta curiosidade.
3. **Demanda comprovada:** já tem gente anunciando o tema, o que é atalho pra saber qual promessa funciona.

**Os passos:**
1. Confere se o caso é de low-ticket: público frio, produto simples, promessa que cabe numa ação rápida. Serviço consultivo e ticket alto não fazem low-ticket direto; aí o low-ticket vira só o degrau de entrada da esteira. Uma linha do porquê.
2. Propõe o produto de entrada (o que ele resolve, num pedaço só) e avalia os 3 pilares com as falas da Ação 0.
3. Registra o sinal de demanda: concorrente anunciando o tema, com o tema visível. Sinal fraco vira `[A CONFIRMAR]`.
4. Declara o papel na esteira: frio → low-ticket → base de compradores → aquecimento → oferta principal.
5. **STOP.**

---

## Ação 2 · MECANISMO (o "como" novo pra quem nunca te viu)

**O que faz:** constrói ou adapta o Mecanismo da Solução, o "como" que carrega a promessa, na versão que funciona pra público frio.

**Precisa de:** o mecanismo nomeado do dono, do perfil do agente · a promessa do produto de entrada (da Ação 1) · as falas da Ação 0 (o que o público já tentou).

**Sem o insumo:** sem mecanismo nomeado, escreva o "como" pelo que o dono ensina de fato e marque `[A CONFIRMAR: nome do mecanismo]`. Nunca nomeie um mecanismo que o dono não pratica.

**Entrega:** `mecanismo-lowticket.md`, com o mecanismo nomeado, os 4 fatores respondidos e o teste do "já tentou e falhou". **STOP pro OK.**

**Arquivos obrigatórios: o arquivo acima, e `conferencia/checagem-titulos.md` por último.**

**Leia primeiro:** `references/metodo-lowticket.md`, seção 3.

**O teste de filtro, antes de tudo:** o mecanismo precisa ser NOVO pra quem lê. Se o público já tentou aquilo e falhou, o funil morre na primeira objeção "como?". Dois caminhos de novidade: algo que ele não conhece, ou a mesma ideia com nome e roupagem mais palpável.

**Os 4 fatores do mecanismo (atribuição a Alex Hormozi):** resultado que ele quer + probabilidade percebida de dar certo + tempo até o resultado + esforço reduzido. Respondidos com o que o dono entrega de verdade, sem inflar prazo nem resultado.

---

## Ação 3 · QUIZ E DIAGNÓSTICO (o compromisso antes da venda)

**O que faz:** monta o quiz por SPIN e o diagnóstico que entrega ao fim, a etapa que cria identificação e compromisso antes do vídeo de venda.

**Precisa de:** as falas da Ação 0 · o mecanismo da Ação 2 · a promessa do produto de entrada.

**Sem o insumo:** sem falas reais, monte pela prova e pelo mecanismo do dono e marque as perguntas que dependeriam do verbatim.

**Entrega:** `quiz-e-diagnostico.md`, com as perguntas em SPIN, as opções de cada uma, a lógica de resultado e a copy do diagnóstico. **STOP pro OK.**

**Arquivos obrigatórios: o arquivo acima, e `conferencia/checagem-titulos.md` por último.**

**Leia primeiro:** `references/metodo-lowticket.md`, seção 4.

**Quiz por SPIN (venda por perguntas):**
- **Situação:** perguntas fáceis (idade, há quanto tempo tem o problema).
- **Implicação:** faz admitir o problema, ver como ele afeta outras áreas, o que já tentou.
- **Necessidade:** urgência, tempo disponível, "como seria se você conseguisse X".

**Regra dura do quiz: nenhuma opção de fuga.** Cada resposta é um microcompromisso; não existe "não quero mudar". Os 4 objetivos: cutucar a dor, canalizar o desejo, gerar identificação, criar compromisso.

---

## Ação 4 · MINI VSL (o vídeo curto que cria a necessidade)

**O que faz:** escreve a mini VSL de 3 a 6 minutos (cerca de 1000 palavras), a peça entre o diagnóstico e a página que cria a necessidade e empurra pro produto.

**Precisa de:** o mecanismo da Ação 2 · a promessa · a prova real do dono · as falas da Ação 0.

**Sem o insumo:** sem prova, o trecho de prova sai como `[A CONFIRMAR: prova]` e a VSL não sai como pronta. Prova gerada por IA não entra (régua zero-inventado).

**Entrega:** `mini-vsl.md`, com a Única Crença numa frase, os 3 a 5 pontos lógicos e os 5 blocos escritos, na voz do dono. **STOP a cada bloco quando fica longo.**

**Arquivos obrigatórios: o arquivo acima, e `conferencia/checagem-titulos.md` por último.**

**Leia primeiro:** `references/metodo-lowticket.md`, seções 5 e 6.

**Começa pela Única Crença, antes de qualquer linha.** Template: "Fazer [AÇÃO ACREDITÁVEL] é a chave pra alcançar [DESEJO]. E a melhor forma de fazer isso é com [SOLUÇÃO ACREDITÁVEL]." A copy nasce de trás pra frente a partir dela.

**Os 5 blocos fixos:**
1. Boas-vindas e ponte: liga à promessa do quiz, vende o vídeo ("assista até o fim").
2. Conceito universal: uma verdade nova que reenquadra o problema.
3. Vilão oculto e quebra de crença: o problema tem culpado externo. Nunca deixa a culpa cair no leitor.
4. Solução: o mecanismo em passos simples.
5. Decisão: pergunta binária e o botão.

**Os 3 gatilhos obrigatórios:** vilão oculto, absolvição (a culpa é do desenho, nunca do caráter de quem lê), mecanismo em 3 passos.

**Prova dosada ao ceticismo.** Afirmação óbvia não leva prova; afirmação forte leva prova forte. Prova em excesso entedia e derruba a conversão de um produto barato. Toda prova é rastreável ao insumo do dono.

**Piso de palavras da mini VSL (checagem do gate, reprova abaixo do piso).** O alvo é 3 a 6 min de fala, cerca de 1000 palavras. Fala corre a ~150 a 170 palavras por minuto, então 3 min já pedem ~500 palavras e o corpo cheio dos 5 blocos fica perto de 1000. Uma rodada entregou a VSL com ~400 palavras: os 5 blocos viraram tópicos, o vilão não teve espaço pra virar necessidade e a peça não sustentou 3 min. Regra dura: **abaixo de ~800 palavras a mini VSL reprova** e volta pra escrita, com os blocos rasos preenchidos até o corpo. Antes de fechar, conte e cole: `wc -w mini-vsl.md`, e escreva `palavras: N · alvo: 3-6 min (~1000) · piso: 800 · abaixo do piso? sim/não`. `sim` reprova a Ação 4.

---

## Ação 5 · MINI PÁGINA (a página curta e o preço ancorado)

**O que faz:** monta a mini página de vendas e a ancoragem do preço, o fecho depois da VSL.

**Precisa de:** a mini VSL da Ação 4 · o preço do produto de entrada (R$ 19,90 a R$ 59) · a prova real · a garantia que o dono oferece.

**Sem o insumo:** sem preço, deixe `[A CONFIRMAR: preço]` dentro da faixa e siga. Sem garantia declarada pelo dono, use a incondicional de 30 dias como sugestão marcada, nunca como fato dele.

**Entrega:** `mini-pagina.md`, com os blocos da página, a ancoragem com motivo lógico, a garantia e o CTA. **STOP pro OK.**

**Arquivos obrigatórios: o arquivo acima, e `conferencia/checagem-titulos.md` por último.**

**Leia primeiro:** `references/metodo-lowticket.md`, seção 7.

**A página abre com HEADLINE, não com rótulo.** O H1 é a headline que para o scroll e vende o clique, nunca o nome da peça: "Mini página: X" ou "Semana de Partida" é rótulo de seção e reprova no gate. Aplique o teste do estranho antes de fechar: quem cai na página por acaso entende a promessa sem contexto.

**A inversão do low-ticket:** MENOS stack, não mais. Empilhar valor percebido demais num produto barato faz ele vender menos. A página é curta: antes e depois, prova social, benefícios, o que a pessoa recebe, garantia, FAQ, CTA.

**Ancoragem com motivo lógico:** o preço barato tem uma razão que o leitor aceita ("na clínica custaria R$ 397; online, sem a estrutura, R$ 29,90"). O motivo é real, do dono, nunca inventado.

---

## Ação 6 · CRIATIVO DE FRIO (o anúncio que vende o clique, não o produto)

**O que faz:** escreve os criativos de anúncio pra tráfego frio no funil de quiz. O anúncio vende a crença de que o mecanismo funciona e o clique no quiz; a venda do produto fica pra mini VSL.

**Precisa de:** o mecanismo da Ação 2 · as falas da Ação 0 · a promessa.

**Sem o insumo:** sem verbatim, monte o ângulo pela prova e pelo mecanismo do dono.

**Entrega:** `criativos-frio.md`, com 6 criativos, cada um com ângulo, hook e formato declarados, e o CTA pro quiz. **STOP pro OK.**

**Arquivos obrigatórios: o arquivo acima, e `conferencia/checagem-titulos.md` por último.**

**Leia primeiro:** `references/metodo-lowticket.md`, seção 8.

**As 3 variáveis independentes do criativo:**
- **Ângulo** (a ideia central): promessa, problema mais mecanismo, história, descoberta, demonstração, quebra de expectativa, depoimento.
- **Hook:** os 3 primeiros segundos, sem enrolar.
- **Formato:** podcast, caixinha, reação, entrevista, tela dividida, imagem com texto.

**Regra de escala:** anúncio parou de vender? Mantém o ângulo, troca o FORMATO. O ângulo validado se guarda; o formato se recria.

**As 3 leis do anúncio:** todo anúncio abre uma venda disfarçada; não pode parecer venda (cara de conteúdo nativo); atenção qualificada (indireto e diferente pra não ser ignorado). CTA literal: "clique em saiba mais, faça o teste". Nenhum criativo com número inventado (régua zero-inventado).

**O ritual de teste (o que fica FORA daqui):** a estrutura de campanha (1 campanha, 3 conjuntos, 2 anúncios, o piso de R$ 90) e a leitura de métrica são de outra skill. A DECISÃO de verba, o que turbinar e OPERAR a conta de anúncio ficam na soft-trafego-meta. Aqui saem os criativos e a expectativa registrada: a rodada 1 busca a primeira venda e o primeiro dado; lucro é a rodada 2.

---

## Ação 7 · O GATE (roda por dentro, em toda peça, e não imprime)

**O que faz:** reprova a peça que não serve, antes de o dono ver. Também é a ação de auditar um low-ticket que o dono colou.

**Precisa de:** a peça escrita.

**Entrega:** nada. O gate é auditoria silenciosa; a tabela nunca vai pra saída. O que sai é a peça limpa.

**Leia primeiro:** `shared-references/crivo/03-gate-cub.md` e `shared-references/crivo/04-gate-regulado.md`.

**Verificador de lastro (obrigatório antes de pronto).** Depois de o gate passar e ANTES de dizer pronto, roda o segundo par de olhos de `shared-references/crivo/10-verificador-lastro.md`: cego à peça, no papel de verificador, confere cada afirmação (aspa, número, história, fato de produto, promessa) contra o insumo do dono e conserta ou remove o que estiver sem lastro. Sem a tabela `afirmação | lastro ou REMOVIDA` no bastidor, a peça não está pronta.

**O veredito é o PIOR item.** Um ✗ qualquer refaz a peça e re-roda o gate.

| Check | Passa se |
|---|---|
| **Ancorada na dor real** | nasce de fala literal da fonte (cita o N real) ou de prova real do dono. N inventado reprova na hora |
| **Zero promessa mágica** | roda o grep da régua zero-inventado. Número de resultado sem prova, prova de IA, estatística sem fonte, hook de risco: reprova |
| **Mecanismo novo pra frio** | passa no teste "já tentou e falhou?"; se o público já falhou nisso, morre na objeção "como?" |
| **Quiz sem opção de fuga** | nenhuma resposta deixa o leitor escapar do compromisso; cumpre os 4 objetivos |
| **Mini VSL completa** | Única Crença numa frase, os 5 blocos, os 3 gatilhos, 3 a 5 pontos lógicos, prova dosada ao ceticismo |
| **Headline de verdade, não rótulo** (BLOQUEANTE) | a mini página e a mini VSL abrem com HEADLINE que para o scroll, nunca com rótulo ou nome de seção. H1 que só nomeia a peça (ex. "Mini página: X", "Semana de Partida") reprova na hora. Aplique o teste do estranho ao H1: quem cai ali por acaso entende a promessa sem contexto; se o H1 só rotula a peça, reescreve |
| **Preço ancorado com motivo real** | ticket entre R$ 19,90 e R$ 59, ancoragem com motivo lógico do dono, garantia declarada |
| **Criativo vende o clique** | ângulo, hook e formato declarados; vende o quiz, não o produto; nenhum número inventado |
| **Culpa no desenho, não no leitor** | absolvição: a culpa é do timing ou da informação errada, nunca do caráter de quem lê |
| **C/U/B** | não é Confuso (1 leitura), não é Inacreditável (promessa do tamanho da prova), não é Boring (tem tensão) |
| **Coerência de fato repetido** (BLOQUEANTE) | o mesmo dado (frequência, duração, preço, prazo, número) bate em toda a peça e com o `dono.md`. Uma rodada disse "25 minutos por dia" num bloco e "25 minutos, 3 vezes na semana" no outro, com o `dono.md` dando só 3x na semana: contradizer a si mesma ou o insumo reprova. Liste cada fato repetido e o valor em cada aparição; qualquer divergência refaz |
| **Mini VSL no piso de palavras** | `wc -w mini-vsl.md` maior ou igual a 800 (alvo ~1000, 3 a 6 min). Abaixo de 800 reprova: os blocos estão rasos |
| **Anti-IA (duro)** | zero travessão longo · zero da família do verbo-freio banido · sem frase-emoldura · sem verbo-clichê de hype |
| **VEREDITO** | = o PIOR item acima. Um ✗ refaz. Só tudo ✓ vai pro dono |

**Como rodar o check de coerência de fato repetido.** Antes de fechar qualquer peça, faça a lista dos fatos que a peça repete (a frequência do hábito, a duração, o preço, o prazo, o número de passos) e cole o valor de cada aparição, uma linha por fato: `<fato> | bloco A: <valor> | bloco B: <valor> | dono.md: <valor> | bate? sim/não`. Puxe o valor do insumo com `grep -niE '[0-9]+ *(min|minuto|dia|semana|x|vez|reais|R\$)' <dono.md>` e confira contra a peça. Qualquer `não` reprova e refaz. Cole `fatos repetidos conferidos: N · divergências: 0`.

Com shell disponível, rode o lint de copy em `scripts/lint_copy.py` sobre o arquivo. Sem shell, faça a busca manual pelos dois bloqueios duros antes de marcar o anti-IA.

---

## O que esta skill NÃO faz

Cada rota é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Material GRÁTIS, isca de captura | **soft-funil-isca** | não faço. O low-ticket é oferta PAGA; a isca troca material por contato |
| Empacotar a oferta como stack, régua 10x, garantia | **soft-plano-ofertas** | monto só a mini oferta de entrada aqui, sem a stack completa |
| Posicionamento, nomear o mecanismo | **soft-plano-posicionamento** | uso a entrevista curta das Ações 1 e 2 |
| VSL longa, carta de ticket alto | **soft-funil-carta** | não faço. Aqui é mini VSL de 3 a 6 min, o oposto |
| Página de captura ou de entrega da isca | **soft-funil-landing** | escrevo só a mini página de vendas do low-ticket |
| Mini-webinar | **soft-funil-miniwebinar** | não faço |
| Headline ou gancho isolado | **soft-conteudo-headlines** | escrevo o hook do criativo dentro da Ação 6 |
| DECIDIR verba, o que turbinar, OPERAR a conta de anúncio | **soft-trafego-meta** | registro só a expectativa de rodada 1 e 2, e entrego os criativos prontos sem subir na conta |
| Arte, visual, PNG | **soft-designer** | entrego o `.md` com a estrutura, sem o visual |

## Anti-patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Despejou o funil inteiro de uma vez | Volta: produz, mostra, PARA pro OK a cada ação |
| Inventou número de resultado ("R$ 3.000 por mês") | Só o real do dono com prova. Sem prova, `[A CONFIRMAR: número]` |
| Colou prova gerada por IA na VSL | Corta. Prova precisa existir e ser rastreável ao insumo do dono |
| Hook que cita remédio ou humilha o leitor | Troca o ângulo. A casa não assina hook de risco |
| Empilhou stack gigante no produto barato | Encolhe. Mais valor percebido num produto barato faz vender menos |
| Quiz com opção de fuga ("não quero mudar") | Tira. Cada resposta é um microcompromisso |
| Mecanismo que o público já tentou e falhou | Reescreve pra algo novo, ou dá roupagem nova e mais palpável |
| Culpou o leitor na VSL | Absolvição: culpa no desenho, no timing, na informação errada |
| Anúncio que tenta vender o produto | O anúncio vende o clique no quiz; o produto é vendido na VSL |
| Preço ancorado com motivo inventado | Motivo real do dono, ou corta a ancoragem |
| Prometeu lucro na primeira venda | Registra a expectativa: rodada 1 busca a primeira venda e o dado; lucro é rodada 2 |
| Narrou o fluxo ("agora vou auditar") | Executa em silêncio e entrega só o resultado |
| Usou duas grafias pra marcar furo | Uma só, em todo o arquivo: `[A CONFIRMAR: o quê]` |

## Transversais

`references/metodo-lowticket.md` (o método em etapas) · `references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/playbook-fonte.md` (a fonte destilada, o lastro do método) · `shared-references/crivo/` · `scripts/lint_copy.py` · `scripts/checar_titulos.py` · `shared-references/filtro-anti-ia/` (a régua anti-IA escrita, pro motor que não roda o lint).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras.
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado, o relato incluso, e só declare o gate aprovado depois de exit 0 em cada um. Cole no relato uma linha por arquivo, no formato `<arquivo>: exit N`, e feche com `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Sem sandbox (a régua escrita, quando o lint não roda).** Motor sem shell não executa `scripts/lint_copy.py`, e isso não dispensa o anti-IA: aplique a régua no olho por `shared-references/filtro-anti-ia/padroes-banidos.md`, padrão por padrão, e passe cada reprovação por `shared-references/filtro-anti-ia/falsos-positivos.md` antes de mandar o trecho de volta pro passo de escrita, porque prosa autoral do dono cai no mesmo crivo e some se ninguém conferir. A entrega sai do mesmo jeito, no melhor que esse motor alcança, e o relato fecha com uma linha dizendo que a conferência anti-IA foi no olho, sem código: `anti-IA: conferido no olho pela régua escrita (sem shell nesta rodada)`. Calar o que ficou de fora reprova a entrega; declarar em uma linha reprova nada.
- **Configuração do dono fora da pasta da skill.** Perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill; vai pra pasta de trabalho do dono, com o caminho declarado no relato.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos:** todo título, capa e nome de bloco que vai ao público passa pela régua (`shared-references/crivo/07-regua-de-titulos.md`), e a checagem sai em `conferencia/checagem-titulos.md`, com gatilho e veredito por título, fechando com as três contagens.
- **Consentimento de nome real:** toda peça passa pelos 3 passos de `shared-references/crivo/08-consentimento.md`. Nome de pessoa vindo de conversa privada sem autorização registrada reprova. Lead em negociação nunca é chamada de aluna nem de cliente.
