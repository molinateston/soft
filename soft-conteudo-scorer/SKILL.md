---
name: soft-conteudo-scorer
description: Avalia uma peça de conteúdo ANTES de publicar em DOIS eixos que se somam. Empírico, bate com o que HISTORICAMENTE engajou no perfil do próprio dono (temas, formatos, ganchos, tamanho, CTA dos posts que mais performaram) e dá a probabilidade de repetir. Doutrinário, passa no gate Soft (ancorado, aponta pro método, C/U/B, filtra o cliente, anti-IA). Entrega scorecard com veredito e ajustes, cada correção citando um dado real do perfil, nunca conselho genérico. Sem dados reais degrada com honestidade (só o gate de qualidade + pede a coleta), jamais inventa benchmark. Use quando o pedido for "dá uma nota nesse post", "esse carrossel vai bombar", "avalia antes de eu publicar", "qual desses posta primeiro", "isso combina com meu perfil", "probabilidade de engajar". NÃO use pra ESCREVER a peça (soft-conteudo-carrossel/-reels/-stories/-headlines), pra IDEAÇÃO de pautas (soft-conteudo-matriz), pro Crivo geral de fase (soft-leon), pra arte (soft-designer) nem pra carta/funil/venda (soft-funil/soft-vendas-closer).
---

# Avaliador de Conteúdo, o duplo eixo antes de publicar

O dono terminou a peça e não sabe se aperta publicar. Duas perguntas diferentes ficam no ar: "isso está bom pelo padrão certo?" e "isso vai performar no MEU perfil?". Esta skill responde as duas de uma vez e num só scorecard. Ela **não escreve** a peça: recebe a peça pronta, mede, e devolve veredito + ajustes ancorados em dado.

**O que esta skill faz por você:** mede uma peça (post, carrossel, reel, story) contra os DADOS REAIS de engajamento do perfil do dono (o que os melhores posts dele têm em comum: temas, formatos, ganchos, tamanho, ritmo, CTA) E contra o gate de qualidade do método. Devolve nota nos dois eixos e correções onde cada uma cita um número do próprio perfil, não opinião.

**A fronteira (leia, é o que te diferencia):** existem DOIS avaliadores no sistema e eles se somam, não competem.
- O **Crivo** (dentro da **soft-leon**, doutrina em `shared-references/crivo/`) avalia **CONTRA O MÉTODO**: a peça está boa pelo padrão Soft? É qualidade, prescritiva, vale mesmo que o passado do perfil seja medíocre.
- Esta skill avalia **CONTRA O HISTÓRICO**: a peça bate com o que de fato engajou NAQUELE perfil? É probabilidade, empírica, diagnóstica.
- **As duas se somam.** Uma peça pode passar no método e mesmo assim destoar do que o público daquele perfil responde (eixo empírico pega isso). E pode bater com o histórico do perfil e ainda ser rasa pelo método (eixo doutrinário pega isso). Por isso o scorecard tem os DOIS eixos: nota de probabilidade E nota de qualidade. Você roda os dois sempre.

**As 6 leis (valem antes de tudo, detalhe em `shared-references/operacao-padrao.md` Seção 0):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil; (2) abre ensinando o que faz; (3) é consultiva, coleta o insumo antes de julgar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: sem dados reais do perfil você NÃO fabrica benchmark, você degrada pro eixo doutrinário e pede a coleta; número que você não tem vira `[A CONFIRMAR]`; (6) **scorecard enxuto pros 2 leitores**: o doc que sai serve o humano que decide publicar E a IA que pega uma correção como input pra reescrever.

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos STOPs, e roda os dois eixos por dentro antes de mostrar o scorecard.**

## Output Contract (o que você entrega)
- **UM scorecard** com os DOIS eixos separados e visíveis:
  - **Eixo empírico (probabilidade, 5 notas de 1 a 10):** força do gancho vs. histórico · aderência à voz do perfil · densidade de valor vs. os melhores · formato/estrutura vs. o que engaja · encaixe no feed. Total /50.
  - **Eixo doutrinário (qualidade, PASSA/REFAZ binário):** ancorado no verbatim real · aponta pro método (deixa lacuna que o dono fecha) · C/U/B (aumenta o motivo de comprar, não só de olhar) · filtra o cliente certo · clareza (Lei 1) · anti-IA HARD.
- Um **VEREDITO em 1 frase** que combina os dois eixos e cita um dado específico do perfil (ex.: "seus 10% melhores abrem com número 42% das vezes, este abre com pergunta; forte pelo método mas destoa do que engaja no seu perfil").
- **Até 3 correções**, cada uma citando um dado real do perfil (ou, sem dados, citando o critério de método que falhou, marcado como tal). Nunca "melhore o gancho": sempre "seus melhores usam X, este usa Y, troque".
- A **fonte de dados declarada** no topo (posts reais coletados / dados em cache / SEM dados: só eixo doutrinário).
- Você **para e oferece** reescrever a parte mais fraca (aciona a skill de escrita certa) ou liberar pra publicar. Você **não reescreve** aqui: mede e aponta.
- Você **nunca inventa benchmark, número de perfil nem "os seus melhores fazem X"** sem ter coletado. Sem dado, o eixo empírico sai marcado **[SEM DADOS, só qualidade]** e você pede a coleta.

## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar o scorecard em pedaços no chat)
Regra dura: o RESULTADO é **UM documento markdown consolidado** (o scorecard completo, dois eixos + veredito + correções). No **claude.ai**, um **artifact de markdown** (o dono lê, decide, copia a correção); no **Claude Code**, um arquivo `.md` na working dir; no **agente/Telegram**, um ARQUIVO cujo path completo vai na resposta + um resumo curto SEM markdown pesado. A CONDUÇÃO (pegar a peça, decidir a fonte de dados, os STOPs) acontece no chat; o SCORECARD mora no DOC. Ao parar num STOP, você mostra/atualiza o DOC e pergunta; nunca reescreve o scorecard em fatias no corpo da conversa. Sem o doc entregue, a skill não terminou.

## Os 3 ambientes (como a entrega e a COLETA mudam)
A coleta de dados reais depende de rodar a infra Apify, e isso só existe em dois dos três ambientes. Declare em qual você está e siga o ramo certo.
- **App/chat (claude.ai, SEM Bash):** você **não coleta** dado real (sem terminal pra rodar Apify). Dois caminhos: se o dono colar/já ter um export de posts, você lê e usa; senão, você roda **só o eixo doutrinário** (o gate de qualidade, que não precisa de dado) e entrega o eixo empírico marcado **[SEM DADOS]** com o pedido explícito pra rodar a coleta no Claude Code/agente. O scorecard sai como **artifact de markdown** (nunca tabela dentro de bloco de código, vira texto ilegível).
- **Claude Code (tem Write/Edit/Bash):** **pipeline completo.** Coleta os posts via Apify (Passo 2), calcula o perfil de engajamento (Passo 3), roda os dois eixos, salva `scorecard-AAAA-MM-DD.md` na working dir e roda `python3 scripts/lint_copy.py` no texto da peça como cinto anti-IA. Confirma o path pro dono.
- **Agente/Telegram (tem Bash):** **pipeline completo** igual ao Claude Code. Coleta via Apify, calcula, mede, grava o `.md` e devolve **o path completo na resposta**, mais um resumo curto SEM markdown pesado (o veredito e as 3 correções em texto corrido, sem tabela nem asteriscos, porque o Telegram não renderiza markdown pesado). O scorecard inteiro mora no arquivo.

## Passo 0, pega a peça e declara o tipo
Se o dono já colou a peça na mesma mensagem, usa ela. Senão:
> Cola a peça que você quer que eu avalie (post, carrossel, reel ou story) e me diz de qual perfil é.

Espera a peça. Identifica o **tipo** (post de texto, carrossel, roteiro de reel, sequência de story), porque o eixo empírico compara com os melhores DAQUELE formato quando dá.

## Passo 1, puxa o contexto de voz (a base do eixo doutrinário e da aderência)
Procura, nesta ordem: **Plano de posicionamento colado** → **soft-perfil do cliente** → **descrição do projeto** → **mensagens anteriores**. Extrai:
- O **avatar e o verbatim** (dor/desejo real, com N quando existe): é contra isso que o critério "ancorado" mede.
- O **método/tese do dono** (pra medir "aponta pro método").
- Os **padrões de ausência da voz** quando existirem (o que aquela voz NUNCA faz: palavras, muletas, estruturas). Se a skill de voz do cliente traz essa lista, puxa 5-8 itens e usa como filtro extra na aderência e no anti-IA.
Se faltar contexto de voz, anota e mede a aderência só contra os padrões que os dados de posts revelarem (Passo 3). Nunca inventa a voz.

## Passo 2, decide a FONTE DE DADOS do eixo empírico (o ramo que separa medir de degradar)
O eixo empírico precisa dos dados reais de engajamento do perfil. Três estados, declara qual é o seu:

**(A) Já tem dado em cache.** Procura na working dir / pasta do projeto por arquivos tipo `*-posts.json`, `*-all-posts.json`, export de posts do perfil. Se achar e estiver recente (menos de ~14 dias), usa. Se estiver velho, avisa e oferece atualizar.

**(B) Não tem, e o ambiente TEM Bash (Claude Code/agente).** Oferece coletar, **avisando que custa** (a coleta Apify consome crédito). Se o dono topar:
1. Pega o @ do perfil (nome de usuário do Instagram).
2. Roda a coleta pela nossa infra Apify (actor `apify~instagram-scraper`, `resultsType:"posts"`), a mesma que já usamos pra puxar perfil. Comando de referência (ajusta o @ e o limite):
   ```bash
   cd /home/cloud/insta-transcricoes && ./scrape.sh <@perfil>/posts.json https://www.instagram.com/<@perfil>/ '{"resultsLimit":150}'
   ```
   O JSON de saída traz, por post, `likesCount`, `commentsCount`, `type` (Image/Sidecar/Video), `caption`, `timestamp`. É tudo que o Passo 3 precisa. **NÃO** passa filtro de campos que derrube o engajamento.
3. Segue pro Passo 3.

**(C) Não tem, e o ambiente NÃO tem Bash (app/chat), ou o dono recusa a coleta.** Você **degrada com honestidade**: NÃO inventa "os seus melhores fazem X". Roda **só o eixo doutrinário** (Passo 4B, que não precisa de dado), entrega o eixo empírico marcado **[SEM DADOS, só qualidade]**, e no fim pede a coleta pra completar. Jamais preenche o buraco com benchmark plausível: um scorecard empírico sem dado é mentira, e mentira falha na Lei 5.

## Passo 3, calcula o PERFIL DE ENGAJAMENTO (só quando há dado real)
Com os posts em mãos, extrai o padrão do que performa NAQUELE perfil. Isso é o "benchmark do próprio dono", a régua do eixo empírico.
1. **Nota de engajamento por post** = `likesCount + (commentsCount × 3)` (comentário pesa mais: custa mais que a curtida e move mais o alcance).
2. Ordena e separa os **10% melhores** por essa nota. Se o perfil tem poucos posts (menos de ~20), usa os **3 melhores** e AVISA que a amostra é pequena (baixa confiança, não trata como lei).
3. Dos melhores, extrai o perfil:
   - **Tipos de gancho que mais aparecem** (contrário, puxado-por-número, afirmação-ousada, história-pessoal, pergunta, confissão) e a % de cada.
   - **Tamanho médio** (contagem de palavras / nº de slides no carrossel).
   - **Formato dominante** (texto, imagem única, carrossel, reel/vídeo).
   - **Padrão de CTA** (comenta-palavra, salva, manda no direct, pergunta aberta, nenhum).
   - **Temas que puxam acima da média** (agrupa por assunto).
   - **Ritmo** (tamanho médio de frase, quebras de parágrafo).
4. Anota também o padrão dos **10% piores** pra saber o que fracassa naquele perfil (é correção de ouro: "seus posts que morrem fazem Y, este faz Y").
Guarda isso como o "perfil de avaliação" que cada critério do eixo empírico consulta. **Se um dado não sai limpo dos posts, marca `[A CONFIRMAR]`, não estima.**

## Passo 4, roda os DOIS eixos por dentro (auditoria interna, NÃO imprime a mecânica)

### 4A, Eixo empírico (probabilidade), 5 notas de 1 a 10
Cada nota compara a peça com o perfil de engajamento do Passo 3. **Regra dura: nota 8+ só se o traço da peça BATER com um padrão dos 10% melhores dele.** Sem dado (estado C), este eixo inteiro sai **[SEM DADOS]**.

| Critério | Nota alta (8+) quando | Cita o dado |
|---|---|---|
| **Gancho vs. histórico** | a 1ª linha usa um tipo de gancho que está no topo dos 10% melhores dele | "seu gancho campeão é número (42%); este é [tipo]" |
| **Aderência à voz** | tom, ritmo e tamanho de frase batem com os melhores; não viola padrão de ausência | "seus melhores têm frase de ~X palavras; esta tem Y" |
| **Densidade vs. os melhores** | ensina/prova/conta no mesmo nível dos que engajaram; tamanho na faixa dos melhores | "seus 10% melhores têm ~X palavras; este tem Y ([acima/abaixo])" |
| **Formato/estrutura** | o formato é o que mais engaja pra ele; ritmo de quebra bate; CTA no padrão | "carrossel engaja Z% mais que texto no seu perfil; este é [tipo]" |
| **Encaixe no feed** | some naturalmente no feed dele; não parece corpo estranho vs. o histórico | "isto se mistura / destoa do seu feed porque [dado]" |

### 4B, Eixo doutrinário (qualidade), binário PASSA/REFAZ por check
Este eixo **sempre roda** (não precisa de dado do perfil, precisa do método e do contexto de voz). Um ✗ qualquer = REFAZ naquele ponto.

| Check | PASSA se | ✓/✗ |
|---|---|---|
| **Ancorado** | nasce de fala real do avatar (verbatim) ou de prova real do dono; número inventado = ✗; sem fonte, `[A CONFIRMAR]` | |
| **Aponta pro método** | deixa lacuna que fecha no que o dono vende; NÃO é conselho neutro que resolve tudo de graça (jornalismo) | |
| **C/U/B (a Faca Soft)** | aumenta o motivo de COMPRAR (clareza/urgência/crença), não só o motivo de olhar; curtida vazia que não aproxima da venda = ✗ | |
| **Filtra o cliente certo** | atrai quem compra, não estranho; viral genérico ("5 hábitos de gente de sucesso") = ✗ | |
| **Clareza (Lei 1)** | dá pra entender sem já ser de dentro; zero palavra difícil, zero figura vazia | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" · sem frase-emoldura ("a verdade é", "o segredo") · sem paralelismo negativo ("não só X, mas Y") · sem verbo-clichê. Ambiente com Bash roda `lint_copy.py`; no chat, CTRL+F manual de "—" e "travar" | |

### A regra de ouro dos dois eixos
**Toda correção cita um dado.** No eixo empírico, o dado é do perfil ("seus melhores usam X"). No eixo doutrinário, o dado é o critério de método que falhou ("não ancora: número sem fonte no slide 3"). Nunca sai correção subjetiva ("ficou fraco", "podia ser melhor"). Se você não tem o dado pra sustentar a correção, você não faz a correção, você pede o insumo.

## Passo 5, monta o scorecard e o VEREDITO combinado
Renderiza o scorecard no DOC (tabela markdown, não bloco de código). Estrutura fixa:

```
SCORECARD · [tipo de peça] · perfil @[dono]

FONTE DE DADOS: [posts coletados: N / cache / SEM DADOS: só qualidade]
Posts analisados: [N]  ·  amostra: [ampla / pequena, baixa confiança]
Engajamento médio dos 10% melhores: [nota]

EIXO EMPÍRICO (probabilidade de performar no seu perfil)
  Gancho vs. histórico     [X]/10   [tipo detectado vs. campeão]
  Aderência à voz          [X]/10
  Densidade vs. melhores   [X]/10
  Formato/estrutura        [X]/10   [formato]
  Encaixe no feed          [X]/10
  --------------------------------
  SUBTOTAL                 [XX]/50   → [alta / média / baixa] chance

EIXO DOUTRINÁRIO (qualidade pelo método Soft)
  Ancorado          [PASSA/REFAZ]
  Aponta pro método [PASSA/REFAZ]
  C/U/B             [PASSA/REFAZ]
  Filtra o cliente  [PASSA/REFAZ]
  Clareza           [PASSA/REFAZ]
  Anti-IA           [PASSA/REFAZ]
  --------------------------------
  GATE: [PASSA / REFAZ em N pontos]

VEREDITO: [1 frase combinando os dois eixos + 1 dado específico]

CORREÇÕES (cada uma com o dado):
1. [correção ancorada em dado do perfil ou critério de método]
2. [...]
3. [...]
```

O VEREDITO combina os dois eixos com honestidade:
- **Passa nos dois** → "manda ver, forte pelo método e no padrão do que engaja no seu perfil".
- **Passa no método, fraco no empírico** → "sólida pelo método, mas destoa do que performa aqui: [dado]. Ajusta [X] ou aceita que é aposta fora do padrão."
- **Bate com o histórico, falha no método** → "combina com seu feed, mas [critério de método] falhou: [qual]. Corrige antes, senão é engajamento que não vira venda."
- **Falha nos dois** → "não publica ainda: [pior do empírico] + [pior do doutrinário]."
- **Sem dados** → veredito só do eixo doutrinário, com a nota "eixo empírico pendente da coleta".

## Passo 6, oferece o próximo passo (NÃO reescreve aqui)
Depois do scorecard, PARA e oferece:
> Quer que eu reescreva a parte mais fraca com os padrões dos seus melhores posts, ou já publica? (a reescrita vai pra soft-conteudo-[carrossel/reels/stories/headlines], que é quem escreve.)

Se o dono pedir a reescrita, **você aciona a skill de escrita certa** passando as correções como contexto. Esta skill mede e aponta; quem escreve é a skill de peça. Não vira máquina de reescrever.

## Exemplo denso (peça: post de texto · perfil de consultor de gestão pra PME), LABEL, não copiar
Peça colada (1ª linha): *"Você já pensou em organizar melhor as finanças da sua empresa?"*
Dado do perfil (Passo 3, N=112 posts): os 10% melhores abrem com **número** 42% das vezes e com **afirmação-contrária** 27%; **pergunta aberta** aparece só 9% e cai no terço pior. Tamanho médio dos melhores: 180 palavras. Formato campeão: carrossel (engaja 2,3× o texto simples). CTA campeão: "comenta a palavra X".

- **Eixo empírico:** Gancho 3/10 (pergunta aberta é o padrão dos PIORES dele, não dos melhores). Aderência 6/10. Densidade 5/10 (o post tem 90 palavras, metade da faixa dos melhores). Formato 5/10 (é texto; carrossel engaja 2,3× mais). Encaixe 5/10. Subtotal 24/50 → **baixa chance**.
- **Eixo doutrinário:** Ancorado ✗ (não nasce de fala do avatar, é pergunta genérica). Aponta pro método ✗ (não deixa lacuna, é conselho vago). C/U/B ✗ (não aumenta motivo de comprar). Filtra ✗ (atrai qualquer um). Clareza ✓. Anti-IA ✓. **GATE: REFAZ em 4 pontos.**
- **VEREDITO:** "Não publica ainda: seu gancho campeão é número (42% dos melhores), este é pergunta aberta (o padrão dos seus piores); e pelo método não ancora nem aponta pro que você vende."
- **CORREÇÃO 1:** "Troca a abertura por número: teus 10% melhores abrem com número 42% das vezes; ex.: 'O dono de PME que aprova cada compra de R$50 e não vê o rombo de R$8 mil/mês.'" **CORREÇÃO 2:** "Vira carrossel: no teu perfil carrossel engaja 2,3× o texto." **CORREÇÃO 3:** "Ancora na dor real ('eu controlo tudo mas o dinheiro some') e aponta pro teu sistema de gestão, senão é conselho que não vira cliente."

Contra-exemplo de correção proibida (nunca faça): "o gancho ficou fraco, melhore." Sem dado, sem critério. REPROVA a própria correção.

## When NOT to use (manda pra skill certa)
- Pediu pra **ESCREVER** a peça (headline, corpo, roteiro, arco) → **soft-conteudo-headlines / -carrossel / -reels / -stories**. Esta skill só MEDE o que já existe.
- Pediu **ideias/pautas do que postar** → **soft-conteudo-matriz** (é o passo lá atrás).
- Pediu o **Crivo geral de fase** ("que fase tô", "valida meu funil inteiro", diagnóstico amplo) → **soft-leon** (o Crivo dele avalia contra o método em qualquer ativo; esta skill é o recorte empírico+doutrinário de UMA peça de conteúdo).
- Pediu **arte/visual/PNG** → **soft-designer**.
- Pediu pra medir **carta/página/VSL/anúncio pago** → **soft-funil** / **soft-vendas-closer** / **soft-conteudo-impulsionar** (esta skill é pra conteúdo orgânico de feed).

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Inventou "os seus melhores fazem X" sem ter coletado | Proibido (Lei 5). Sem dado, eixo empírico sai **[SEM DADOS]** e pede a coleta; nunca fabrica número de perfil |
| Só rodou um eixo | Rode SEMPRE os dois; se falta dado, o empírico degrada com honestidade, o doutrinário sempre roda |
| Correção subjetiva ("ficou fraco", "melhore o gancho") | Toda correção cita um dado: do perfil (empírico) ou do critério de método que falhou (doutrinário) |
| Deu 8+ no empírico sem o traço bater com os 10% melhores | Nota 8+ só quando o traço da peça casa com um padrão dos melhores dele; senão desce |
| Começou a REESCREVER a peça | Esta skill mede e aponta; a reescrita vai pra skill de escrita certa no Passo 6 |
| Amostra minúscula tratada como lei | Menos de ~20 posts = baixa confiança; avisa e não crava padrão como certeza |
| Rodou coleta sem avisar do custo | Sempre avisa que a coleta Apify consome crédito antes de rodar |
| Despejou o scorecard solto no chat / dentro de bloco de código | Scorecard sai como doc MD (artifact / arquivo / path no agente); tabela markdown que renderiza, nunca grade em bloco de código |
| Confundiu com o Crivo do método | Crivo (soft-leon) = qualidade vs. método; esta = probabilidade vs. histórico + qualidade; as duas se somam |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `shared-references/operacao-padrao.md`: as 6 leis (Seção 0) + regras de tom/economia/entrega. Consulta na 1ª invocação da sessão.
- `shared-references/crivo/05-premissas-mestras.md`: a doutrina de copy que sustenta o eixo doutrinário (C/U/B, aponta pro método, a espinha da percepção). É o mesmo padrão que o Crivo do soft-leon usa.
- `shared-references/filtro-anti-ia/`: o banco de padrões banidos + a seção de falsos-positivos que alimenta o check Anti-IA (pra não reprovar prosa autoral legítima).
- `references/mecanica-avaliacao.md`: o detalhe operacional do eixo empírico (fórmula de engajamento, extração do perfil dos 10% melhores, coleta Apify passo a passo, como degradar sem dado). Índice no topo. Consulta quando a peça exige o cálculo fino.
- `scripts/lint_copy.py`: no Claude Code/agente, roda `python3 scripts/lint_copy.py peca.txt` no texto da peça como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual.
