---
name: soft-conteudo-comentario-fixado
description: 'Escreve o COMENTÁRIO FIXADO do método Soft (o 1º comentário do próprio criador embaixo de um post) como peça de humanização e confiança, MAIS o conceito de imagem cômica de status baixo que vai junto. Mecânica fixa: a imagem carrega a piada e o comentário só legenda, o dono é sempre a figura de status mais baixo, 4 linhas de até 40 caracteres cada, e a confissão do post casa com a tese/inimigo do Plano do dono (humor que reforça o posicionamento, não piada solta). A arte sai pela soft-designer. Use quando o pedido for "comentário fixado", "comentário fixo", "primeiro comentário", "comment fixado", "legenda cômica do post", "humanizar esse post", "imagem de status baixo pro post". NÃO use pro CORPO do post/carrossel/reel/stories (soft-conteudo-carrossel/-reels/-stories), pra HEADLINE/gancho (soft-conteudo-headlines), pra LEGENDA de venda ou CTA (humaniza, não fecha), pra ARTE/PNG em si (soft-designer gera), nem pra tese/posicionamento (soft-posicionamento) ou funil/venda (soft-funil/soft-vendas-closer).'
---

# Comentário Fixado, a peça que humaniza a autoridade

O post entrega o valor. O comentário fixado, o primeiro comentário que o próprio criador solta embaixo do post, faz outra coisa: constrói personalidade e confiança. É onde o dono tira a máscara polida e aparece como gente. Embaixo de um post técnico ou de autoridade dura, um comentário fixado que se rebaixa com graça faz o público baixar a guarda e seguir.

Engraçado é subjetivo e fácil de errar. Esta skill torna o comentário fixado **repetível**: uma mecânica fixa que qualquer pessoa do time produz no mesmo padrão, sem depender de "veia cômica".

**O que esta skill faz por você:** escreve o comentário fixado de 4 linhas MAIS o conceito da imagem cômica que vai com ele (a arte final sai pela **soft-designer**). Ela NÃO escreve o post, nem a headline, nem gera o PNG.

**A sacada central (leia isto primeiro):** a imagem carrega a piada, o comentário só legenda a imagem. Se o comentário é engraçado sozinho, ele está trabalhando demais e a imagem está fraca. Se a imagem precisa do comentário pra ter graça, a imagem está fraca. Por isso o **conceito de imagem vem primeiro, sempre**.

**Uso situacional (não é peça obrigatória do funil):** isto humaniza, não vende. É ouro embaixo de post de autoridade seca (o especialista técnico que soa distante), pra derreter a barreira. NÃO é fechamento, não carrega CTA de venda, não substitui a legenda que converte. Se o pedido é vender, é outra skill. Use quando o objetivo é conexão e confiança.

## As 6 leis (valem antes de tudo, detalhe em `shared-references/operacao-padrao.md` Seção 0)
(1) nunca escreve como se o dono já soubesse o contexto, zero palavra difícil; (2) abre ensinando o que faz; (3) é consultiva, entende o post e o Plano antes de escrever; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: post que você não viu, tese do dono que você não tem, viram pergunta ou `[A CONFIRMAR]`, jamais piada plausível chutada; (6) **doc de output enxuto** pros 2 leitores (o dono que copia e cola, e a soft-designer que recebe o conceito da imagem).

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare no STOP, rode o gate por dentro antes de mostrar.**

## Output Contract (o que você entrega)
Um doc MD com estes 4 blocos, nesta ordem:
1. **A confissão** (uma frase): o que o post está confessando em silêncio, casada com a tese/inimigo do Plano do dono.
2. **O conceito da imagem** (parágrafo): a piada visual clara + a postura de status baixo do dono, escrito como briefing pra **soft-designer** gerar (nunca prompt de outra ferramenta).
3. **O comentário de 4 linhas** (começa com 📌): 4 linhas, cada uma ≤40 caracteres, cada uma frase completa.
4. **A nota de gate** (uma linha): confirma que passou nos 5 testes + no anti-IA.
- Opcional: 2-3 variações se a 1ª ficar no limite.
- Você **nunca inventa a confissão nem a tese do dono** (se não tem o post ou o Plano, pergunta) e **nunca mostra comentário que falhou no gate**.

## ⚠️ ENTREGA = UM doc MD, SEMPRE (nunca pingar solto no chat)
Regra dura: o RESULTADO é **UM documento markdown consolidado** com os 4 blocos acima. No **claude.ai**, um **artifact de markdown**; no **Claude Code**, um arquivo `.md`; no **agente/Telegram**, um ARQUIVO cujo path completo vai na resposta. A CONDUÇÃO (entender o post, o STOP) acontece no chat; a PEÇA mora no DOC. Ao parar no STOP, você mostra/atualiza o DOC e pergunta "ajusto?"; NUNCA reescreve a peça em pedaços na conversa. Sem o doc entregue, a skill não terminou.

## Os 3 ambientes (como a entrega muda)
- **App/chat (claude.ai, sem Bash):** a peça sai como **artifact de markdown**. Você entrega o texto do comentário e o briefing da imagem; a arte em si o dono gera acionando a **soft-designer** depois.
- **Claude Code (tem Write/Edit):** salva em `comentario-fixado-AAAA-MM-DD.md` na working dir + roda `python3 scripts/lint_copy.py` no arquivo como cinto anti-IA (reprova em-dash e "travar"). Confirma o path pro dono.
- **Agente/Telegram (tem Bash):** grava o `.md`, devolve **o path completo na resposta**, mais o comentário de 4 linhas em texto corrido SEM markdown pesado (sem asterisco, sem tabela). O briefing da imagem mora no arquivo.

## Passo 0, entende o post e puxa a tese do dono (NÃO PULE)
Você precisa de duas coisas antes de escrever:
- **O post** (o que ele diz, o que ele entrega). Procura nesta ordem: post colado na conversa → descrição do que o dono acabou de publicar → pergunta em 1 linha se não tem. Sem saber o que o post diz, você não acha a confissão.
- **A tese/inimigo do Plano** do dono (o Grande Dominó, o inimigo, o Mecanismo do Problema, na **soft-posicionamento**). É isto que faz o humor reforçar o posicionamento em vez de virar piada aleatória. Sem Plano na conversa, pergunta "qual a tese central que você defende / contra o que você luta" numa linha, ou marca `[A CONFIRMAR]`.

**Regra de fronteira:** você NÃO reescreve o post nem define a tese aqui. O post vem pronto (outra skill o escreveu), a tese vem do Plano. Aqui os dois entram como dados de entrada.

## Passo 1, acha A confissão (e casa com a tese)
Todo post bom esconde uma confissão silenciosa, a verdade meio constrangedora que ele não diz em voz alta. Exemplos de forma (não copiar):
- "Eu cobro caro e ainda fico com medo de mandar o orçamento."
- "Meu processo é simples demais pro tanto que eu cobro."
- "Passei anos aprendendo o que ensino em 20 minutos."

Escreve a confissão em **uma frase** antes de qualquer coisa. E casa com a tese do dono: a confissão tem que ser o lado humano da MESMA briga que o Plano defende (se a tese é "simplicidade vence complexidade", a confissão brinca com o quanto isso incomoda quem aposta no complicado). Humor que reforça o posicionamento, não piada de creator genérico.

**STOP interno:** se você não consegue nomear a confissão em uma frase, o post ainda não está pronto pra comentário fixado. Fala isso pro dono, não force uma piada em cima de post que não confessa nada.

## Passo 2, monta o conceito da imagem PRIMEIRO (pra soft-designer)
Três regras pra imagem:
1. **Uma piada visual clara.** O olho cai nela em menos de um segundo. Se você precisa de mais de 5 palavras pra descrever a piada, está cheia demais, simplifica. Uma piada por imagem, uma é mais afiada que três.
2. **Levada totalmente a sério.** Sem piscadinha pra câmera, sem joinha, sem cara exagerada. O humor vem de tratar o absurdo como se fosse normal.
3. **O dono é a figura de status mais baixo.** Sempre. Quem "ganha" na cena é o oposto dele (o cliente, a planilha, a concorrência complicada, o estagiário). O dono perde com dignidade silenciosa.

Escreve como **briefing pra soft-designer** (não como prompt de ferramenta externa), neste formato:
> "Imagem fotorrealista de [cena]. A piada visual: [descrita em detalhe, quem tem o status alto e como]. O dono aparece [postura e expressão de status baixo, levadas a sério]. [Luz e enquadramento]."

A imagem final NÃO sai daqui: você entrega o briefing e o dono aciona a **soft-designer** com a ID visual dele. Não invente prompt de Gemini/Nano Banana nem de outra ferramenta.

## Passo 3, legenda a imagem com o comentário de 4 linhas
O comentário nomeia o que a imagem mostra, como se estivesse noticiando o fato. Estrutura:
```
📌 [Linha 1: descreve a coisa absurda como fato normal, legenda a imagem]
[Linha 2: vira o status do dono pra baixo]
[Linha 3: uma vitória triste, o menor ganho possível]
[Linha 4: aceitação resignada, sem forçar a piada]
```

**As regras das 4 linhas (inegociáveis):**
- Exatamente 4 linhas, nem mais nem menos. Cada uma é frase completa.
- Cada linha tem no máximo 40 caracteres (**conte, não estime**).
- Linha 1 começa com 📌.
- Sem P.S., a linha 4 é o fecho. Sem ponto e vírgula, sem hashtag.
- PT-BR do começo ao fim, acentuação correta.
- Evita muleta e encheção (só, que, muito, realmente, na verdade, literalmente).
- Resignado vence esperto: a linha 4 aceita, não faz graça inteligente.

## Passo 4, roda o GATE por dentro (auditoria interna, NÃO imprime)
Roda os checks internamente. Uma falha refaz a peça (não pula o gate). A tabela é teu **checklist interno**, nunca a saída.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Confissão nomeada** | dá pra dizer em 1 frase o que o post confessa; se não dá, o post não está pronto (avisa o dono) | |
| **Casa com a tese** | a confissão é o lado humano da MESMA briga do Plano (Grande Dominó/inimigo); não é piada solta de creator | |
| **Piada visual em 5 palavras** | dá pra descrever a piada da imagem em ≤5 palavras; se não, a imagem está cheia, simplifica | |
| **Linha 1 legenda o fato** | a linha 1 nomeia o que a imagem mostra como fato; se ela monta uma piada separada, reescreve | |
| **Dono é status baixo em TODA linha** | o dono perde em toda linha; se ele ganha, parece esperto ou descolado em alguma, reescreve | |
| **Linha 4 resignada** | aceitação seca, não piada forçada; se força pra ser esperta, deixa menor e mais triste | |
| **4 linhas, ≤40 chars cada** | conta de fato os caracteres de cada linha; 4 linhas exatas; 📌 na linha 1 | |
| **Teste do tédio sozinho** | leia as 4 linhas SEM a imagem: sem graça sozinho = ótimo (a imagem faz o trabalho). Se engraçado sozinho, a imagem está fraca, reforça a imagem | |
| **Clareza (Lei 1)** | dá pra entender sem já ser de dentro; zero palavra difícil, zero figura vazia | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, destrava, transforma"). No chat/agente sem lint, faz CTRL+F manual de "—" e "travar" | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ é mostrado. | |

## Passo 5, monta o doc e PARA
Monta o doc MD com os 4 blocos do Output Contract. Mostra **no DOC** (nunca solta no chat). Pergunta: "esse comentário te representa? quer que eu ajuste o tom, gere 2-3 variações, ou você já leva o briefing pra soft-designer gerar a imagem?". **Espera a escolha** antes de gerar variações ou fechar.

## Exemplo denso (nicho: consultor que vende gestão SIMPLES pra dono de PME), LABEL, não copiar
Post: um carrossel provando que o dono não precisa de ERP caro, só de uma planilha de 1 aba bem feita.
Tese do Plano: **simplicidade radical vence a complexidade cara** (inimigo = o sistema complicado que vendem pro pequeno).

- **A confissão:** "Eu construí um negócio inteiro numa planilha de 1 aba e ainda tenho vergonha de mostrar."
- **O conceito da imagem (briefing pra soft-designer):** "Imagem fotorrealista de uma sala de reunião de empresa grande. Na cadeira da cabeceira, imponente, um monitor gigante rodando um ERP cheio de gráficos, tratado como o executivo-chefe. O dono está numa banquetinha no canto, de camiseta, segurando um notebook velho com uma única planilha aberta, olhando pro monitor com respeito tímido. Luz corporativa fria, tudo levado a sério."
- **O comentário de 4 linhas:**
```
📌 O ERP tem a cadeira da chefia.
Eu fico na banqueta do canto.
Minha planilha de 1 aba paga as contas.
Alguém tinha que segurar o rojão.
```
- **Por que passa:** a confissão casa com a tese (simplicidade humilde vence o sistema caro). A piada visual em 5 palavras: "ERP na chefia, dono na banqueta". A linha 1 legenda o fato. O dono perde em toda linha (banqueta, notebook velho, respeito tímido) e só "ganha" a vitória mais triste possível (a planilha paga as contas). A linha 4 é resignada, não esperta. Lido sozinho, o comentário é morno; com a imagem, canta. Anti-IA: zero travessão, zero "travar", zero frase-emoldura. Contagem: cada linha ≤40. **VEREDITO: PASSA.**

Contra-exemplo (REPROVA): "📌 Fiz um negócio de 7 dígitos numa planilha." O dono GANHA (7 dígitos, parece esperto), não é status baixo, não casa com a humildade da tese, e é engraçado/impactante sozinho (a imagem vira redundante). VEREDITO = ✗.

## When NOT to use (manda pra skill certa)
- Pediu o **CORPO** do post/carrossel/reel/stories → **soft-conteudo-carrossel** / **-reels** / **-stories**.
- Pediu a **HEADLINE/gancho/capa** → **soft-conteudo-headlines**.
- Pediu a **LEGENDA que vende** ou um **CTA de conversão** → isto aqui humaniza, não fecha; a venda é **soft-funil** / **soft-vendas-closer**.
- Pediu a **ARTE/PNG** em si (gerar a imagem) → **soft-designer** (esta skill entrega o briefing, a designer gera).
- Pediu pra **definir a tese/posicionamento** → **soft-posicionamento** (é de lá que a tese vem).

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| O comentário explica a imagem em vez de legendar | Linha 1 nomeia o fato que a imagem mostra, não descreve a cena |
| O comentário é engraçado sozinho (imagem vira redundante) | A piada tem que morar na imagem; enfraquece o texto, reforça a imagem |
| O dono ganha, parece esperto ou descolado em alguma linha | Status baixo em TODA linha; ele perde com dignidade, o outro ganha |
| Linha 4 forçando uma piada inteligente | Deixa menor e mais triste; resignado vence esperto |
| Piada visual que precisa de mais de 5 palavras | Simplifica; uma piada por imagem, uma é mais afiada que três |
| Piada solta que não tem a ver com a tese do dono | Casa a confissão com o Grande Dominó/inimigo do Plano; humor reforça posicionamento |
| Enfiou marca patrocinada ou CTA de venda no comentário | Isto humaniza, não vende; tira o CTA, o post já faz o resto |
| Inventou o que o post diz ou a tese do dono | Não viu o post / não tem o Plano: pergunta ou marca `[A CONFIRMAR]`, nunca chuta |
| Escreveu prompt de Gemini/ferramenta externa pra imagem | Escreve briefing pra soft-designer; a arte sai por lá com a ID do cliente |
| Despejou a peça solta no chat | Sai como doc MD (artifact / arquivo / path no agente); o chat é a condução |
| Linha passou de 40 caracteres | Conta de fato, não estima; corta até caber |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `shared-references/operacao-padrao.md`: as 6 leis (Seção 0) + regras de tom/economia/entrega. Consulta na 1ª invocação da sessão.
- `shared-references/filtro-anti-ia/`: o banco de padrões banidos + falsos-positivos que alimenta o check Anti-IA do gate.
- `scripts/lint_copy.py`: no Claude Code/agente, roda `python3 scripts/lint_copy.py` no doc como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual do gate.
