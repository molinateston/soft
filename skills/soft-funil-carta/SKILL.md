---
name: soft-funil-carta
description: "Escreve a CARTA DE VENDAS do método Soft que aquece e qualifica o lead antes da conversa, o degrau 1 do funil. ESCALA da mini-carta (4-7min) até a CARTA LONGA de resposta direta (sales letter: duplo mecanismo, value stack, garantia, bônus, FAQ, P.S.), no MESMO arco ADMA (Atenção-Diagnóstico-Mecanismo-Ação, nunca AIDA). Diagnostica a consciência (Schwartz) pra calibrar comprimento e lead, ancora no verbatim real, constrói desejo antes da oferta, fecha em UM convite pro 1:1, roda o gate embutido (ancoragem, duplo mecanismo, prova maior que alegação, anti-IA HARD). Também faz roteiro de VSL. Use pra \"carta\", \"carta de vendas\", \"carta longa\", \"sales letter\", \"mini-carta\", \"VSL\", \"vídeo de vendas\", \"escreve a carta\", \"deixa a carta mais completa\". NÃO use pro corpo de feed (slides, reel, stories: soft-conteudo-*; headline: soft-conteudo-headlines), landing/sales page hero-ao-botão (soft-funil-landing), mini-webinar (soft-funil-miniwebinar), nem o fechamento (objeção, follow-up: soft-vendas-closer)."
---

# Carta de vendas, o ativo que aquece antes da conversa

A carta faz o trabalho que a reunião fazia. Lida em silêncio, no celular. Ela **filtra, explica e constrói desejo**, entrega o lead quente pro Comercial 1:1. Ela NÃO fecha a venda: high-ticket (3k+) fecha na conversa, a carta é o degrau 1 que aquece e qualifica. Carta que tenta fechar sozinha vira pitch e esfria o lead certo.

**Esta peça ESCALA de comprimento.** O mesmo arco ADMA vai da **Mini-Carta** (4-7min de leitura, 4 blocos enxutos, o modo default e mais usado) até a **Carta Longa** de resposta direta (15-25min, sales letter completa, com os blocos clássicos da DR: duplo mecanismo, value stack, garantia, bônus, FAQ, P.S.). Mesma espinha, mesma função em qualquer tamanho: filtra, explica, constrói desejo, entrega quente pro 1:1. O Passo 2-bis decide o comprimento; ninguém infla a carta por gosto.

**Carta Longa não é landing page (a fronteira que não pode vazar).** A carta, curta ou longa, é **texto corrido lido em silêncio**: uma promessa, um CTA pro 1:1, leitura de cima a baixo. A landing é **arquitetura-de-página** (hero, seções com título, vídeo embed, CTA repetido em botão), e quem monta isso é a `soft-funil-landing`. Carta Longa que ganha hero, blocos titulados e botão repetido deixou de ser carta. Aqui a peça é uma fala só, do começo ao fim.

**O que esta skill faz por você:** escreve a carta de vendas, o discurso-base do teu produto. Ela faz o que a reunião fazia: filtra, explica e constrói desejo, e entrega o lead quente pro 1:1. É feita pra virar uma PÁGINA de carta (com quebra de padrão e quebra visual, sem virar landing), e dela derivam depois o mini-webinar e o webinar.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa o briefing de você antes de escrever; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa** (confere se tem o número/case/fala; se falta, admite e pergunta ou marca `[A CONFIRMAR]`, jamais preenche com algo plausível); (6) **doc de output enxuto pros 2 leitores** (o .md de entrega é o mais otimizado possível pro humano que lê E pra IA que recebe como contexto: zero meta-narração, zero bastidor, zero explicação-do-método-pro-leitor; só o insumo denso e os `[A CONFIRMAR]`). (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar qualquer trecho.**

## Output Contract (o que você entrega)
- A **carta completa** (texto em markdown Notion-compatível) OU o **roteiro de VSL/vídeo de vendas** (falado, com timings), nunca os dois sem o cliente escolher.
- A carta sai num de **3 comprimentos (Mini / Média / Longa)**, declarado no **Passo 2-bis** pelo nível de consciência × ticket × temperatura do tráfego, todos no MESMO arco ADMA. A Longa carrega os blocos clássicos da DR (duplo mecanismo, value stack, garantia, bônus, FAQ, P.S.), mas continua carta: texto corrido, uma promessa, um convite pro 1:1, preço fora salvo ticket baixo. A Longa **ancora valor** (empilha componentes, custo de não agir), nunca crava o **número do preço** dentro da peça salvo ticket baixo.
- Estruturada no **arco ADMA** (Atenção · Diagnóstico · Mecanismo · Ação). O gate roda **por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída.
- Entregue **etapa por etapa** (briefing, espinha, carta diagramada, auditoria), parando pro OK a cada uma. Nunca despeja a carta inteira de primeira.
- **Preço fora da peça** por padrão (vai pro WhatsApp). Exceção: ticket baixo (até ~R$1.500).
- Você **nunca inventa fala, case ou número** do cliente. Sem prova real do autor, o trecho sai como `[CASE: confirmar]` e **não vai como pronta**.


## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar a peça no chat)
Regra dura, vale mesmo pra copy curta: o RESULTADO desta skill sai como **UM documento markdown consolidado**. No **claude.ai**, um **artifact de markdown** (o dono abre, copia, baixa); no **Claude Code**, um arquivo `.md`. No **agente/Telegram**, gera o doc como arquivo e cita o path completo na resposta (vira anexo); a condução vai em mensagens curtas, sem markdown pesado (sem `##`, sem tabela `|` no texto ao usuário; o doc vai como arquivo). A CONDUÇÃO (perguntas de contexto, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA/COPY em si mora no DOC. Ao parar num STOP, você mostra ou atualiza o DOC e pergunta "ajusto?"; você NUNCA reescreve a peça em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Passo 0, ancora antes de escrever (NÃO PULE)
Procura a fonte de fala real, nesta ordem: **descrição do projeto** → **Plano colado na conversa** → **mensagens anteriores**. Puxa **3-5 falas de DOR + 3-5 de DESEJO** do tema, literais, contando o N (quantas vezes apareceu). A Atenção (primeira linha) nasce de uma delas, quase intacta, citando o N.

Três estados de entrada (declara qual é o seu antes de escrever):
- **Tem fala real (com N):** ancora nela e cita o N. Caminho ideal.
- **Tem nicho/fundação mas ZERO fala literal:** NÃO inventa fala nem N. Ancora em **prova real do autor** (resultado, case, mecanismo). Número não confirmado entra como `[DADO: confirmar]` e **não conta como Ancorada=✓**. Case que não existe entra como `[CASE: confirmar]`. Avisa: minerar 5-8 falas reais (ou rodar o Plano na soft-plano-posicionamento) deixa a carta muito mais cravada.
- **Sem nicho e sem nada:** pergunta numa única mensagem (nicho em 1 linha + 1 dor real + o ticket) e segue daí.

Confirma o que vem do Plano (`soft-plano-posicionamento`): Oferta + PUV + Mecanismo nomeado + Voz. Sem Plano, a carta sai genérica, volta pra `soft-plano-posicionamento`.

## Passo 1, briefing num bloco só (espera resposta)
Se veio do Plano com os dados, confirma em 1 linha e pula. Senão, coleta de uma vez:
- **(a)** cliente ideal específico (nicho + faturamento + situação + maturidade)
- **(b)** Problema Avançado nomeado (palavras do cliente, não jargão)
- **(c)** 3-5 soluções comuns que ele já tentou + o efeito colateral de cada
- **(d)** o mecanismo nomeado e suas 3-4 etapas
- **(e)** 1-3 cases reais (nome + nicho + número + prazo, só verdade documentável)
- **(f)** a oferta + o ticket (o ticket decide se o preço entra na peça)

**Só a Carta Longa exige estes 3 (opcionais, alimentam os blocos da DR, sem virar receita):**
- **(g)** o **mecanismo do PROBLEMA**, a causa-raiz oculta que exonera o leitor ("não é falta de X, é Y"), distinta do mecanismo da solução do item (d). Exemplo de nicho fictício (consultoria de gestão): o item (d) é o método "Mapa de Margem"; o item (g) é a causa-raiz, "o seu lucro some porque a precificação segue a planilha do contador, não a percepção de valor do cliente".
- **(h)** elementos de **reversão de risco** (a garantia condicional ou incondicional que o autor topa dar de verdade) + os **bônus reais** que matam objeção nominal (cada bônus mira UMA objeção: tempo, dúvida técnica, medo de não conseguir sozinho).
- **(i)** a **razão honesta de urgência**, se existir (vagas da turma, preço que sobe, janela de início), só se for verdade.

Sem (a)(b)(d)(f), não avança. PARA e espera. **Faltando (g)(h)(i), a peça DESCE pra Média/Mini, nunca inventa garantia, bônus ou urgência plausível** (lei admite-se-faltar: o que não tem entra como `[A CONFIRMAR]` ou some, jamais é preenchido com algo verossímil).

## Passo 2, escolhe o formato (carta-texto OU VSL)
Decide com o cliente, pela tabela. Carta e Vídeo **não são fases**, são formatos paralelos, mesma espinha ADMA, mesma função.

| Ticket | Formato | Preço na peça? |
|---|---|---|
| até ~R$1.500 | Carta-texto, pode fechar na própria peça | Sim, pode entrar |
| R$1.500-3k | Carta-texto + WhatsApp | Fora |
| 3k+ | Carta-texto (ou página de autoridade) OU VSL ≤25min + WhatsApp | Fora |

**Critérios da escolha (carta ou vídeo).** O vídeo entrega presença e profundidade (quanto mais alto o ticket, mais profundidade o lead precisa pra decidir), mas custa mais pra produzir (gravação, edição, regravação cara). A carta tem menos atrito de produção (edita texto) e se lê em qualquer lugar, no silêncio, sem fone. Quem comunica melhor escrevendo vai de carta, quem brilha falando vai de vídeo.

**Acima de ~R$2k com tráfego frio:** a carta-texto (ou uma página de autoridade sem vídeo) costuma superar o VSL longo. O VSL ≤25min só compensa se o autor comunica muito melhor falando do que escrevendo. VSL acima de 35min com tráfego frio raramente converte mais que a versão curta. O Vídeo só muda o formato: tom falado, transições orais, timings.

Pra a grade de durações do VSL por ticket, consulta `references/vsl-script.md`.

## Passo 2-bis, diagnostica a consciência e calibra o COMPRIMENTO + o LEAD
Antes de escrever a espinha, lê o leitor. O nível de consciência (Schwartz) decide **onde a carta abre** e **quanto ela mede**. Abre `references/anatomia-carta-longa.md` (seções 2 e 3) pra escolher o lead e o comprimento com profundidade. **PARA só se faltar o dado de consciência** (não dá pra inferir do briefing); senão, declara e segue.

**Tabela 1, consciência → abertura + comprimento:**

| Consciência do leitor | A carta abre por | Comprimento que pede |
|---|---|---|
| **Inconsciente** (nem sabe que tem o problema) | a CENA / o mecanismo do problema (mostra a dor que ele ainda não nomeou) | Longa |
| **Consciente-do-Problema** (sente a dor, não sabe a saída) | a cena + o mecanismo que exonera | Longa |
| **Consciente-da-Solução** (sabe que existe saída, compara) | a diferença + a prova (por que a sua, não a do vizinho) | Média |
| **Consciente-do-Produto** (já te conhece, hesita) | a promessa direta + o diferencial nomeado | Média / Mini |
| **Mais-Consciente** (só falta a oferta) | a oferta + a promessa direta | Mini basta |

**Tabela 2, qual lead de Masterson casar com a consciência:**

| Consciência | Lead que casa |
|---|---|
| Inconsciente | **Story** ou **Proclamation** (entra por narrativa ou declaração ousada) |
| Consciente-do-Problema | **Big-Secret** ou **Problem-Solution** (a causa oculta, a virada) |
| Consciente-da-Solução | **Problem-Solution** ou **Promise** |
| Consciente-do-Produto | **Promise** (a promessa, direta) |
| Mais-Consciente | **Offer** (a oferta na cara) |

**Regra do comprimento:** quanto MENOS consciente o leitor, MAIOR o ticket e MAIS frio o tráfego, mais longa a carta. Leitor mais-consciente em ticket conhecido quer Mini; leitor inconsciente em tráfego frio com ticket alto pede Longa. Exemplo de nicho fictício (nutrição esportiva): tráfego frio de anúncio + ticket de R$6k de acompanhamento + público que acha que "é só comer menos" (inconsciente do mecanismo real) = Carta Longa com lead Story. Já a base de e-mail quente que já fez consulta avulsa (mais-consciente) = Mini com lead Offer.

**Declara em uma linha antes de escrever:** `Consciência X → Lead Y → Comprimento Z`. Mantém a **Rule of One** em qualquer comprimento: uma ideia central, uma emoção dominante, um benefício-promessa, uma ação no fim.

## ✍️ PRÉ-FLIGHT DE COPY (relê IMEDIATAMENTE antes de escrever a 1ª linha)
Escreve JÁ dentro do gate, nunca pra ser corrigido por ele depois:
1. **Munição na mão:** verbatim/prova real do dono na frente (sem munição = pergunta, jamais inventa).
2. **Uma ideia por frase.** Número em algarismo no lugar de adjetivo.
3. **Voz do cliente final:** zero jargão de marketing (lead, funil, ticket, copy).
4. **Standalone:** cada frase entendida sem contexto e sem explicação.
5. **Anti-IA:** zero travessão, zero família banida, zero frase-emoldura, zero clichê de robô.
6. **Promessa do tamanho da prova:** menor com chão ganha de grande sem chão.
7. **Teto do formato conhecido ANTES de escrever** (conta durante, não conserta depois).
Depois de escrita, a auditoria do gate confere DE FATO (busca e contagem). Reprovou, reescreve ANTES de mostrar.

## Passo 3, escreve a espinha no arco ADMA (bastidor, texto corrido)
Escreve a peça inteira como **uma fala corrida** na voz do cliente, seguindo o arco. **ADMA, nunca AIDA.** AIDA empurra desejo→ação por gatilho; ADMA reorganiza a percepção, constrói desejo pelo diagnóstico, e só então convida.

| Fase ADMA | O que faz | Fecha em |
|---|---|---|
| **A · Atenção** | espelha o cliente certo na situação concreta dele, promete o que vai entender, filtra quem não é | reconhecimento ("isso fala comigo") |
| **D · Diagnóstico** | nomeia o Problema Avançado, lista as soluções tentadas e o efeito colateral, exonera ("não é falta de esforço, é arquitetura") | o inimigo-categoria nomeado (sistema/prática, nunca pessoa) |
| **M · Mecanismo** | a virada por contraste ("o mercado faz X, isto faz Y, porque Z"), o método nomeado com função de cada etapa, a prova real | um número/case concreto |
| **A · Ação** | a oferta sem virar pitch, o filtro ("pra quem não é"), UM convite firme pro Comercial 1:1 | o CTA único pro WhatsApp |

**Desejo antes da oferta:** a Ação só funciona se o Diagnóstico e o Mecanismo já construíram o desejo. Oferta colada logo na abertura (pulando D e M) é AIDA disfarçada, refaz.

**Explora o Problema a fundo (é onde a carta ganha ou perde).** O Diagnóstico é a fase mais longa: traz tudo que o Plano de posicionamento alinhou (o Problema Avançado, as soluções já tentadas e o efeito de cada uma, o inimigo nomeado) bem organizado, com cena e número, até o leitor pensar "é exatamente isso que eu vivo". Carta que corre o problema pra chegar logo na oferta não constrói desejo.

**Faca aparada:** mostra o mecanismo e a **função** de cada etapa, nunca o passo a passo executável. Entregar o "como fazer" mata a venda.

**Quando o comprimento é Longo, cada fase ADMA ganha músculo (sem virar AIDA, sem virar landing).** Os blocos clássicos da DR não são blocos novos fora do arco: cada um mora dentro de uma das 4 fases, na ordem psicológica em que abre a objeção que o próximo bloco precisa aberta. **A Carta Longa é a ADMA com mais músculo em cada fase, não um arco diferente.** O mapa:

| Fase ADMA | Na Longa carrega |
|---|---|
| **A · Atenção** | o Lead escolhido no Passo 2-bis + headline + pre-head + sub-head |
| **D · Diagnóstico** | a agitação da dor + a história de origem + o **mecanismo do PROBLEMA** (a causa-raiz oculta que exonera, item (g) do briefing) |
| **M · Mecanismo** | o **mecanismo da SOLUÇÃO** nomeado + o produto como encarnação desse mecanismo + o empilhamento de prova + o benefit stacking |
| **A · Ação** | a oferta + o value stack ancorado + a reversão de risco + os bônus + a urgência honesta + o FAQ + o fecho + o P.S. triplo |

**O duplo mecanismo é a marca da Longa:** o mecanismo do PROBLEMA (em D, exonera, "não é culpa sua, é Y") vem ANTES do mecanismo da SOLUÇÃO (em M, a chave proprietária nomeada). Sem o mecanismo-problema, a promessa nova colide com a decepção que o leitor já carrega das tentativas passadas. **Abre `references/blocos-copy.md` na hora de escrever a copy de cada bloco e `references/anatomia-carta-longa.md` pra a ordem dos blocos, o porquê de cada um e como ele se aninha na fase.**

### As fórmulas dos blocos (a matéria-prima)
A fórmula-raiz de cada bloco, em 1 linha, pra escrever direto sem sair da skill. Condensado de `references/blocos-copy.md` e `references/anatomia-carta-longa.md`; abre a ref quando precisa da variação, do anti-exemplo ou da ordem completa. Cada `[colchete]` é insumo real do briefing (nunca inventado).

| Bloco (fase ADMA) | Fórmula-raiz em 1 linha |
|---|---|
| **Hero / Headline** (A) | "Como [resultado desejado] sem [objeção principal], para [perfil específico]." 6 a 14 palavras, zero adjetivo vazio, zero exclamação. |
| **Sub-head** (A) | 1 a 2 frases que ampliam a promessa OU definem melhor o público; nunca repete a headline. |
| **Para quem é** (A) | "Este [produto] é pra você se: você já [situação que qualifica] · você tentou [X] e [efeito frustrante]. Não é pra você se: [exclusão]." Filtra na entrada. |
| **O Problema** (D) | Cena-âncora sensorial do dia com a dor + as tentativas e o efeito colateral de cada uma + o diagnóstico ("não é você, é [inimigo-categoria]"). Inimigo é sempre um sistema ou prática nomeada, nunca pessoa. Respira: 20 a 30% do texto. |
| **Mecanismo do Problema** (D) | Cadeia causal A->B->C: "[solução A] resolve [sintoma X], não [causa-raiz Y]; quando você faz A, B acontece; quando B acontece, C é inevitável. Não é falta de esforço, é arquitetura." 3 a 5 itens, exonera. |
| **Método / Mecanismo da Solução** (M) | Declaração do nome ("[Nome]: [síntese de 1 linha]") + contraste ("enquanto o mercado faz X, o [método] faz Y, porque Z") + etapas (nome + função + objeção que quebra, faca aparada, sem passo executável) + frase-síntese isolada. |
| **Prova social** (M) | "[Nome], [nicho]. Vinha de [situação inicial]. [Resultado concreto com número + prazo]. Sem [objeção que o resultado derruba]." Só verdade documentável; sem prova real, entra como `[CASE: confirmar]`. |
| **O Produto por dentro** (M) | Por item: "[Nome que remete a vitória] · o que você conquista: [resultado] · o que você usa: [entregável] · onde você chega: [cena]." Benefício, nunca funcionalidade. |
| **Bônus** (A) | Por bônus: nome com verbo de resultado + o que é (1 linha) + a UMA objeção que mata (tempo / dúvida técnica / medo de não conseguir) + valor unitário pra ancoragem. 2 a 4 no máximo. |
| **Empilhamento + Oferta / Value stack** (A) | Lista cada componente com sua âncora individual de valor, mata tempo e esforço percebidos, ancora o valor ANTES do preço (custo de não agir); no Soft o NÚMERO do preço fica fora salvo ticket baixo, o fecho é convite pro 1:1. |
| **Garantia / reversão de risco** (A) | "Se em [prazo] você [fez X e não obteve Y], [o que acontece]. Porque [o que diz da confiança no método]." Condicional (reverte E filtra quem não vai aplicar) é a preferida no Soft; específica e ousada, nunca "satisfação garantida". |
| **FAQ (as 7 objeções)** (A) | Uma pergunta por objeção, resposta = mini-copy conversacional: "é pra mim?" (perfil preciso) · "funciona mesmo?" (case similar) · "e se não der certo?" (garantia) · "não tenho tempo" (tempo real de implementação) · "é caro" (custo de oportunidade) · "já tentei parecido" (o que muda no mecanismo) · "quero pensar" (nomeia o que não está claro). |
| **CTA Final** (A) | Headline de decisão ("se você leu até aqui, sabe que é pra você") + resumo em 1 frase + urgência só se real + UM convite firme pro 1:1 pré-explicando o que acontece no WhatsApp. |
| **P.S. triplo** (A) | P.S. recapitula a oferta e a promessa (2 linhas) · P.P.S. reforça a garantia · P.P.P.S. a urgência honesta (só se existe). É o 2º texto mais lido; comprime o essencial pra quem pulou pro fim. |

### Exemplo-modelo, uma mini-carta inteira (nicho fictício)
Consultoria de gestão pra dono de restaurante, ticket ~R$3k, método "Mapa de Margem" (exemplo ilustrativo, nicho fictício; modela a qualidade, nunca copia). Os quatro blocos ADMA em prosa condensada:

> **[A] O restaurante lota e o mês fecha no zero.**
> Você fatura pela casa cheia no fim de semana e ainda assim, todo dia 30, sobra pouco. Nesta carta eu te mostro por que, em 5 minutos de leitura. Pra dono de restaurante que vende bem e não entende onde o lucro some.
>
> **[D] Você já cortou porção, trocou fornecedor, apertou o salgado.** E o lucro continua sumido. Cada corte resolveu um pedaço e nenhum resolveu a conta. Porque a conta que sangra não está na cozinha: está no cardápio. Você precifica pelo custo do prato mais uma margem fixa, do jeito que a planilha do contador manda. Só que o cliente não paga pelo custo, paga pela percepção, e os pratos que mais deixam margem estão escondidos no fim do cardápio. Não é falha sua. É um jeito de montar cardápio que ninguém te ensinou.
>
> **[M] O Mapa de Margem reorganiza o cardápio por margem de contribuição, não por custo.** A gente mede prato a prato quanto cada um deixa depois de tudo e reposiciona os campeões pra onde o olho do cliente cai primeiro. Em três restaurantes que aplicaram, o ticket médio subiu sem trocar fornecedor nem mexer no preço de tabela `[CASE: confirmar]`. Você passa a saber, olhando o cardápio, quais pratos defender e quais aposentar.
>
> **[A] Se você se reconheceu, o próximo passo é único.** Me chama no WhatsApp: eu primeiro entendo se o seu caso é dos que esse método resolve, e a gente acerta o investimento na conversa. Dois tipos de dono leem até aqui. Um fecha a aba pensando "interessante" e daqui seis meses ainda fecha o mês no escuro. O outro manda mensagem agora. Os dois são legítimos, só um vira a conta.

## Passo 4, diagrama a carta OU monta o roteiro do VSL
- **Carta-texto (feita pra virar PÁGINA):** fica entre a carta pura e a página de vendas. Quebra a espinha nas 4 fases pra **leitura solitária**, com **quebra de padrão** (uma virada de ritmo ou de ângulo que tira o leitor do automático) e **quebra visual** (callout, frase isolada, separador, número grande, espaço em branco) a cada bloco, pra a página respirar e segurar a leitura no celular. Parágrafos de 1-3 linhas. Frase isolada só em alto impacto. Pergunta retórica curta a cada 3-5 parágrafos ("Familiar?"). Zero subtítulo dentro de fase. Diagrama caso a caso (callouts, separadores, espaço em branco), o conteúdo decide o visual, sem template fixo. Tom escrito coloquial, não oral transcrito.
  - **Leitura solitária não perdoa:** a carta é lida sozinha, no silêncio, no celular. No vídeo a narração carrega o leitor de uma frase pra outra; na carta o leitor está só com o texto e fecha a aba na primeira frase fraca, genérica ou longa demais. Por isso cada frase tem que puxar a próxima, sem folga.
  - **Carta-texto LONGA (sales letter):** mantém texto corrido e leitura solitária, mas com a **slippery slide** de Sugarman ponta a ponta. A primeira frase é curtíssima e existe só pra puxar a segunda. No fim de cada bloco planta uma semente de curiosidade que força o próximo ("mas tem um detalhe", "deixa eu mostrar de onde isso vem"), tirada sempre da CENA concreta, nunca de fórmula vazia. Os primeiros parágrafos criam o ambiente de leitura (o leitor concorda com coisas pequenas e óbvias antes de discordar de nada). Os elementos visuais (callout, pull-quote, separador, tabela, toggle) já vivem em `references/modo-mini-carta.md`; na Longa eles aparecem com mais frequência, mas a regra "o conteúdo decide o visual, sem template fixo" continua. **Densidade na Longa:** o alvo NÃO é cortar pra 950 palavras, é cortar gordura mantendo cada bloco da DR que faz trabalho de objeção. Corta a frase que não puxa a próxima, nunca o bloco que abre uma objeção real. O **P.S. é o 2º texto mais lido** da carta: carrega oferta, garantia e urgência comprimidas, pra quem rolou direto pro fim.
- **VSL/Vídeo Minimalista (7-12min):** quebra nas 4 fases com os timings certos: Bloco 1 (Atenção) no ~1min30, Bloco 2 (Diagnóstico) até ~4min, Bloco 3 (Mecanismo) até ~10min, Bloco 4 (Ação) nos ~2min finais. Tom falado, transições orais. Entrega o roteiro pronto pra gravar e a página de hospedagem.
  - **Alta Polaridade:** a abertura do vídeo desafia o que o lead acredita; abertura que não instala tensão faz o lead desengajar nos primeiros 90 segundos.
  - **6 elementos mínimos da página de hospedagem:** Headline (promessa em 1 linha) · Subheadline (pra quem é e o filtro) · Pra quem é (3-5 bullets) · Vídeo (embed) · Provas (prints com contexto) · Botão único (CTA pro WhatsApp). A página não argumenta, o argumento está no vídeo; ela só apresenta a promessa, filtra na entrada, mostra prova e redireciona.

Densidade: cada frase carrega ideia ou função. Corta 30-40% na revisão. Carta de 15 páginas é erro.

## Passo 5, roda o GATE por dentro (auditoria silenciosa, NÃO imprime)
Roda o gate na peça inteira **internamente** (auditoria silenciosa). Só peça com a linha VEREDITO=PASSA vai pro cliente. Um ✗ qualquer = REFAZ o trecho que falhou. A tabela abaixo é o teu **checklist interno**, nunca a saída: o cliente recebe só a peça limpa (Passo 6), jamais a tabela.

Antes do gate, confere os 5 movimentos de Blair Warren (Sonhos · Falhas · Medos · Desconfianças · Inimigo) como pré-filtro; se algum estiver ausente, reforça antes de auditar. Detalhe em `references/vsl-script.md`. O veredito final é do gate, não dos 5 movimentos.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorada** | nasce de fala literal da fonte (cita N **real**) OU de prova real do autor; **N inventado/plausível = ✗ automático**; cada fase fecha em chão (número/case/mecanismo), não em tese solta bonita | |
| **Arco ADMA (não AIDA)** | as 4 fases na ordem A→D→M→A, identificáveis; **oferta colada na abertura pulando Diagnóstico/Mecanismo = ✗** (isso é AIDA) | |
| **Desejo antes da oferta** | o Mecanismo construiu o desejo antes do convite; o leitor quer a saída ANTES de ver a oferta. Oferta antes do desejo = ✗ | |
| **Prova real do autor** | todo case/número é verdade documentável; **sem prova, o trecho está como `[CASE: confirmar]`/`[DADO: confirmar]` e a peça NÃO sai como pronta** | |
| **Consciência casada** (Médio/Longo) | a peça declara o nível de consciência do Passo 2-bis e a ABERTURA bate com ele (inconsciente abre por cena, mais-consciente abre por oferta); abertura desalinhada da consciência = ✗. *n/a na Mini* | |
| **Duplo mecanismo** (Médio/Longo) | existe o mecanismo do PROBLEMA (exonera, "não é culpa sua, é Y") ANTES do mecanismo da SOLUÇÃO; mecanismo-solução só rotulado (não batizado) ou ausência do mecanismo-problema = ✗. *n/a na Mini* | |
| **Prova ≥ alegação** (Médio/Longo) | toda alegação grande tem prova do lado, e a Longa empilha prova variada (demonstração, dado, case com dono, reason-why); alegação maior que a prova = ✗. *n/a na Mini* | |
| **C/U/B** | não Confuso (1 ideia por frase, leitor não relê), não Inacreditável (promessa menor + prova, não mágica), não Boring (cada frase puxa a próxima) | |
| **Faca aparada** | mostra função das etapas, zero passo a passo executável que dispensa o autor | |
| **Convite 1:1 único** | UM CTA firme pro Comercial 1:1 (WhatsApp/conversa), pré-explica o que acontece lá; **múltiplos CTAs ou "saiba mais/agende call" genérico = ✗** | |
| **Degrau 1 da escada** | a carta filtra e aquece, não tenta fechar sozinha (salvo ticket baixo); preço fora da peça salvo ticket baixo | |
| **Dá pra ver?** | fecha o olho e enxerga a cena. ✗ "tenha mais clareza" · ✓ "a recepcionista diz: semana que vem enche" | |
| **Dá pra falsificar?** | é fato falsificável, não adjetivo | |
| **Só você diz?** | o concorrente direto não assina igual (cena/mecanismo proprietário, não promessa banal do nicho) | |
| **Teste único** | o cliente certo pensa "isso fala comigo" na primeira linha e "finalmente alguém que entende" no fim | |
| **CTA com destino** | o convite aponta pra um lugar real (link do WhatsApp/conversa), não pro vácuo | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, destrava, transforma"). **No chat (sem o lint), faz CTRL+F manual de "—" e da família "travar" antes de marcar ✓.** | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

No Claude Code, roda `python3 scripts/lint_copy.py` na peça como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual.

## Passo 6, mostra e PARA
Mostra **só a peça LIMPA** (ou a etapa pronta), no doc (artifact): sem tabela de gate, sem meta. Adiciona o comentário de publicação (como colar no Notion e configurar o link). Pergunta "essa te serve? ajusto?". **Espera o OK** antes de seguir pra próxima etapa ou variação. Não narra o fluxo ("agora vou diagramar"), só entrega limpo.

## When NOT to use (manda pra skill certa)
- Pediu **conteúdo de feed** (slides, reel, stories, multiplataforma) → **soft-conteudo-carrossel/-reels/-stories/-multiplataforma**; só a **headline/gancho** → **soft-conteudo-headlines**.
- Pediu **landing page completa / sales page** (hero ao botão, 4 arquiteturas, blocos de copy) → **soft-funil-landing**.
- Pediu **mini-webinar do funil** (vídeo de ~10min em blocos) → **soft-funil-miniwebinar**.
- Pediu **isca / lead magnet / artigo-isca / captura** → **soft-funil-isca**.
- Pediu **webinar perpétuo ou ao vivo** → **soft-webinar-plano** (porta de entrada do pacote; o roteiro é **soft-webinar-script**).
- Pediu **Plano / posicionamento / oferta / PUV** → **soft-plano-posicionamento**.
- Pediu **arte / visual / PNG** → **soft-designer**.
- Pediu o **fechamento da venda** (script, objeção, follow-up, pós-venda) → **soft-vendas-closer**; a **prospecção/abertura de lead frio** → **soft-vendas-sdr**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Despejou a carta inteira de primeira | Volta: briefing → espinha → carta → auditoria, parando pro OK a cada etapa |
| Montou no arco AIDA (atenção→interesse→desejo→ação por gatilho) | Reescreve no ADMA: o Diagnóstico nomeia o inimigo, o Mecanismo constrói o desejo, só então a Ação convida |
| Oferta colada logo na abertura | Falha "desejo antes da oferta": insere Diagnóstico + Mecanismo antes do convite |
| Inventou um case/número "plausível" | Só prova REAL; sem fonte, marca `[CASE: confirmar]`/`[DADO: confirmar]` e a peça não sai como pronta |
| Carta tenta fechar a venda sozinha | É degrau 1: aquece e filtra. O fechamento é o Comercial 1:1 (soft-vendas-closer). Preço fora da peça (salvo ticket baixo) |
| Múltiplos CTAs ("clica · agenda call · saiba mais") | UM convite firme pro WhatsApp, pré-explicando o que acontece lá |
| Entregou o passo a passo executável do método | Faca aparada: mostra função das etapas, não o "como fazer" que dispensa o autor |
| Carta bonita mas genérica (concorrente assina) | Falha no gate "só você diz"; reescreve com cena/mecanismo proprietário |
| Narrou o fluxo ("agora vou diagramar") | Não narra: executa em silêncio e entrega só o resultado |
| Imprimiu a tabela do gate na saída | O gate é INTERNO (auditoria silenciosa); a saída é só a peça limpa |
| Carta Longa virou landing page (hero, seções com título, VSL embed, CTA repetido em botão) | É carta: texto corrido, leitura solitária, UM convite pro 1:1. Arquitetura-de-página é soft-funil-landing |
| Inflou pra Longa sem ter consciência fria nem ticket que justifique | O comprimento sai do Passo 2-bis (consciência × ticket × temperatura), não do gosto; leitor mais-consciente quer Mini |
| Pôs o mecanismo-solução mas pulou o mecanismo-problema | Na Longa, exonera primeiro (a causa-raiz oculta) e só então entrega a chave; sem isso a promessa nova bate na decepção passada do leitor |
| Garantia genérica ou urgência fabricada | Garantia específica e ousada (a condicional move o risco e ainda filtra); urgência só se a razão existe de fato. Escassez falsa queima a confiança construída |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `references/discurso-base-7-passos.md`: os 7 passos nomeados do Discurso Base, o andaime entre o briefing e as 4 fases ADMA (os 7 passos colapsam nas 4 fases).
- `references/modo-mini-carta.md`: exemplo de carta completa diagramada (Notion) + tabela de quando usar cada elemento visual + diagnóstico por sintoma.
- `references/anatomia-carta-longa.md`: a espinha da carta de vendas longa de resposta direta mapeada SOBRE o arco ADMA (consciência, leads, os 17 blocos da DR, duplo mecanismo, value stack ancorado, P.S. triplo, a fronteira com a landing). **Abre no Passo 2-bis** (pra escolher o lead + o comprimento) e **no Passo 3 ao escrever a Longa** (pra a ordem dos blocos, o duplo mecanismo, o value stack ancorado e o P.S. triplo). Carrega a ESTRUTURA; a copy de cada bloco está em `blocos-copy.md`.
- `references/vsl-script.md`: o roteiro do VSL em blocos com timings, fórmulas de hook e anatomia de case.
- `references/blocos-copy.md`: a copy bloco a bloco da DR longa que a `anatomia-carta-longa.md` ordena (hero, problema, mecanismo, prova, oferta, CTA) com fórmulas e anti-exemplos. É a fonte de copy de cada bloco, não a estrutura.
- `references/tom-e-ritmo-desejo.md`: as 7 categorias de corte e a tabela-síntese de tom (auditoria frase a frase).
- `references/conducao-na-pratica.md`: o jeito de conduzir (sem-call é posicionamento, minimalismo, carta-virou-site, congruência repete a tese, o feed é a entrada).
- `scripts/lint_copy.py`: no Claude Code, roda `python3 scripts/lint_copy.py` na peça como cinto extra do anti-IA. No chat não roda, por isso o CTRL+F manual do gate.
