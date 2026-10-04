---
name: soft-critico-copy
description: >-
  Recebe uma peça de texto pronta e devolve o veredito em arquivo, aprovada ou reprovada, com o
  trecho que falhou, o motivo em português e a versão reescrita pronta pra colar embaixo de cada
  falha. Use quando o pedido for: "critica essa copy", "essa headline passa?", "revisa esse
  carrossel antes de eu postar", "isso está com cara de IA?", "audita essas 10 headlines", "roda o
  gate nessa página", "por que essa copy não convence", "isso é genérico?", "valida no modo
  rigoroso", "passa no teste do concorrente?". É também o gate que toda skill de copy chama antes de entregar linha pública. NÃO use
  pra: "por que não converteu" sobre o número do funil (soft-negocio-metricas); auditar o perfil
  inteiro do Instagram (soft-consultoria-instagram); escrever copy nova (soft-conteudo-headlines,
  soft-conteudo-carrossel ou a skill do formato); revisar brief interno ou plano, que não é linha
  pública; decidir posicionamento (soft-plano-posicionamento). Leia e siga o fluxo inteiro do
  SKILL.md.
---

# Gate de copy: uma peça entra, um veredito sai

Esta skill não escreve copy. Ela AUDITA uma peça pronta e devolve um veredito em arquivo: aprovada, ou reprovada com a falha exata, o trecho que falhou, o motivo em uma linha e a reescrita sugerida. Quem chamou corrige e manda de novo, até passar.

## Primeiros passos (o que mandar, como pedir, o que volta)

O agente mostra estes passos ao dono que chega sem nada pronto e pede uma coisa de cada vez. Quatro palavras que aparecem no arquivo inteiro: **veredito** é a resposta final (aprovada ou reprovada); **filtro** é cada régua que a peça atravessa (são 6); **lastro** é a prova de onde saiu cada número, nome e caso que a peça cita; **modo rigoroso** é a régua mais dura, com nota de 0 a 10.

1. **A peça**, colada ou em arquivo, do jeito que vai pro público. É a única coisa sem a qual não existe auditoria.
2. **O tipo e o que ela vende**, uma frase cada ("anúncio do curso de bolo; promete precificar o cardápio numa tarde"). Por quê: o tipo decide o peso dos filtros e se o modo rigoroso já vem ligado, e a promessa é o lastro do filtro 5. Não sabe o tipo? A skill classifica e diz qual assumiu. Não sabe dizer a promessa? A skill faz uma pergunta e segue com a resposta. Caixinha de aceite ou rodapé de caminhos: diga qual sinal a linha capta e onde ela mora.
3. **Opcional, e melhora o veredito:** a origem de cada número, prazo e caso que a peça cita (planilha, print, conversa com cliente), a peça anterior e a próxima da campanha, e o perfil de voz. Sem eles, a skill marca `[LASTRO: confirmar com o dono]` e segue. Senha, token e dado de cliente que não vai na peça nunca entram.
4. **O rigor:** peça de venda já roda no modo rigoroso (nota X/10, só 10 aprova). Em post educativo, peça "valida no modo rigoroso" ou "isso é genérico?". Pra desligar o padrão, use a chave do dono em "Modo rigoroso".
5. **O que volta:** o arquivo `veredito-copy-<slug>.md` com APROVADA, REPROVADA ou, no rigoroso, a nota e REFAZER; cada falha com o trecho, o motivo em uma linha e a reescrita sugerida. Em lote, o topo diz quantas passaram e quais faltam. Depois: a skill que escreveu a peça (ou o dono) corrige e manda de novo, até 3 rodadas; na terceira reprovação a decisão volta pro dono.

## O que vale em toda auditoria

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --peca-externa <peça auditada> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0 (o `--peca-externa` é obrigatório aqui: a peça auditada mora fora da pasta). A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**A régua de títulos é filtro com item próprio na lista de falhas**, aberto por `filtro: Régua de títulos`, com o universo contado, os títulos reprovados e as reescritas. Ela nunca entra como sub-item do lint: um lote passa no lint e reprova na régua.

Ela existe porque copy fraca reprova por régua, nunca por opinião. São 6 filtros, e a ordem de leitura importa: se quem lê não entende, não adianta ser confiável; se não acredita, não adianta ser interessante; se a promessa é de qualquer um, não adianta estar bem escrita.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra três auditorias fictícias em nicho neutro: a headline de um anúncio reprovada no modo rigoroso, a mesma headline aprovada com nota 10 depois da correção, e um lote de 5 legendas de feed com o veredito consolidado.

**O lastro do dono vem do banco do agente.** Onde o filtro 5 precisar de tese, oferta, prova, número ou nome de mecanismo: leia do perfil/brain do agente quando existir; se não existir, use a tese e a oferta declaradas na própria conversa e marque toda afirmação grande que não apareceu ali como `[LASTRO: confirmar com o dono]`. Nunca invente fato do negócio, nunca pare por causa disso.

---

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a peça e eu audito na hora). Se quiser ser guiado passo a passo (te pergunto o contexto da peça antes de julgar) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): audita já com a peça que o dono colou. Se faltar um insumo que o veredito não vive sem (a peça em si, ou a tese/oferta que ela deveria sustentar), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Antes do veredito, pergunta o contexto que muda o julgamento (pra que canal é a peça, qual a oferta e a prova por trás), uma coisa de cada vez.

A pergunta do modo é UMA por auditoria. As outras três partes entram nos filtros abaixo:

- **Ensina enquanto faz:** em cada reprovação, escreve UMA linha do porquê ("reprovo essa frase porque ela se apoia em adjetivo, não em cena; o leitor não consegue ver o que você afirma"), pra o dono corrigir sozinho na próxima peça.
- **Puxa o material bruto:** quando o dono defender uma alegação grande sem lastro ("mas é verdade que transformo vidas"), não aceita o genérico. Pede o concreto: "de qual cliente real isso saiu, e que número ou frase literal prova?". Sem lastro, marca a afirmação como furo, não como aprovada.
- **Oferece refinar no fim:** depois do veredito, fecha com UMA linha de ajuste ("quer a peça de volta corrigida? aponte as falhas e a skill que escreveu a peça devolve a nova versão a partir da reescrita sugerida"). Quem reescreve é a skill de origem, nunca esta (ver "NÃO altera o texto entregue"). Com falha do filtro 6, essa linha dá lugar ao fecho de `references/validador-conversao-reescrita.md`.

## Ação única · AUDITAR UMA PEÇA (ou um lote)

**O que faz:** roda os 6 filtros numa peça de copy pronta e devolve o veredito com falha, trecho, motivo e reescrita.

**Auditoria de peça com títulos roda a régua de títulos primeiro, e ela entra no veredito.** Extraia todo título da peça auditada (capa, manchete de slide, assunto, texto na tela, primeira linha de mensagem), rode a régua de `references/regua-de-titulos.md` sobre eles e entregue `conferencia/checagem-titulos.md` na pasta do veredito, com as contagens que a régua pede. **Título reprovado é falha BLOQUEANTE, no mesmo nível da falha dura do lint:** peça com capa que só descreve não passa, por melhor que esteja o corpo, porque a capa é o que decide se o corpo é lido. O veredito cola `títulos auditados: N · reprovados: N`.

**O universo da auditoria é CONTADO por comando, nunca escolhido.** Recortar o universo pra "os títulos principais" produz um `2 · 2` sobre 10 slides, que parece checagem e não é. Conte antes de auditar: `grep -cE '^#{1,4} |^\*\*Slide|^Slide [0-9]' <peça auditada>`, e cole o número ao lado do declarado. Depois rode o `--conferir` do bloco de pronto: **a peça auditada mora FORA da pasta de saída, e o universo é contado nela pelo `--peca-externa`**, que sai com exit 1 e `títulos auditados: N menor que os M títulos da peça auditada` quando o declarado for menor. Exit diferente de 0 reprova o veredito inteiro, e um veredito que não passa no próprio gate não julga peça nenhuma.

**Precisa de:** a PEÇA, o texto exato que vai pro público, colado ou num arquivo · o TIPO DE PEÇA (a lista fechada abaixo) · a TESE e a OFERTA declaradas, que são o lastro do filtro 5 · opcionalmente, os caminhos do material canônico do dono (transcrição, documento de posicionamento, banco de verbatim) · opcionalmente, o ARCO DA CAMPANHA (a peça anterior e a próxima, ou 2 linhas do dono sobre o momento), que alimenta o encaixe narrativo do filtro 6.

**Sem o insumo:**
- Sem o texto: não existe auditoria. Devolva "sem texto pra criticar" e pare. É o único bloqueio duro.
- Sem o tipo declarado: leia a peça e classifique você mesmo pelo formato, diga em 1 linha qual tipo assumiu, e siga. Não pergunte por isso.
- **Tipo fora da lista** (um roteiro de podcast, um texto de embalagem, uma legenda de foto): não recuse. Encaixe no vizinho mais próximo pela FORMA de leitura, declare o encaixe em 1 linha no topo do veredito ("tratei como `corpo`, texto longo lido de uma vez") e rode os 6 filtros normalmente. A régua de peso do filtro segue a do tipo vizinho.
- Sem tese e oferta: pergunte UMA coisa, "o que essa peça está vendendo, e qual a promessa dela em uma frase?", e use a resposta como lastro.
- Sem nenhum material canônico: o filtro 5 não para o trabalho, ele marca `[LASTRO: confirmar com o dono]` em toda afirmação grande. Número, nome de mecanismo e história continuam reprovando quando saíram do nada.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `veredito-copy-<slug>.md` na pasta de trabalho, no formato do bloco "O veredito" abaixo. Em lote, um arquivo só, com uma seção por peça e o consolidado no topo. Se o ambiente renderizar markdown, mostre o veredito também na resposta.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/_regua-cub.md` (o filtro 1, o que mais reprova na prática) · `references/validador-conversao-mestre.md` (o filtro 6, os 5 critérios de conversão e a escala de gravidade) · `references/_padroes-estruturais-ia.md` (o filtro 4, os 12 padrões que o código não pega).

**Profundidade:** `references/_estrutura-mae.md` (os 6 movimentos, com exemplo comprimido de reel, de carrossel e de carta) · `references/_verbatim-fontes.md` (a ordem de peso das fontes de lastro) · `guia/GUIA-COPY-APLICACAO.md` (o método de copy inteiro, peça por peça) · `guia/CODIGO-DE-ESCRITA.md` (a lei por trás do guia) · `guia/03-identidade-voz.md` (os elementos de voz) · `references/validador-conversao-checkpoints.md` e `references/validador-conversao-reescrita.md` (o modo rigoroso e os moldes de reescrita do filtro 6).

### Os tipos de peça previstos

`headline` · `capa` · `corpo` · `slide` · `script_reel` · `sequencia_stories` · `carta` · `landing_bloco` · `landing_completa` · `isca_copy` · `oferta` · `whatsapp` · `email` · `script_sdr` · `script_closer` · `pos_venda` · `bio` · `cta` · `linha de serviço`

**`linha de serviço`, regra estreita.** Só texto curto (até 3 linhas) cuja função é captar um sinal do leitor (caixinha de aceite, rodapé de caminhos, "responda tal palavra"). Nunca headline, gancho, capa, anúncio nem e-mail de venda, e nunca texto com promessa de resultado, argumento de venda (por que comprar, benefício), urgência ou escassez (hoje, últimas, vagas, prazo de oferta), desconto, garantia ou prova social (depoimento entre aspas, número de alunos): com qualquer um, vale o tipo da peça de verdade, com o rigor dela. Informação neutra do caminho (preço cheio, quantidade, duração, "sem custo" que só descreve) cabe. Na dúvida, o tipo mais rigoroso; declarado fora da regra, a skill troca o tipo e avisa em 1 linha. **Efeito:** o critério 1 (teste do concorrente) e o 3 (contraste) do filtro 6, o B de Boring e o modo rigoroso não pesam nela, e a Estrutura-mãe cobra só o Movimento; anti-IA, lastro e consentimento valem inteiros. O QUÊ e PRA QUEM (C de Confusão, regra dura de frase) se leem pelo lugar onde ela mora, a página ou o e-mail em volta descrito no pedido, nunca isolados: ela só reprova ali se o lugar não os dá ou se o contradiz; sem o lugar, a skill pergunta onde ela mora. O veredito traz `tipo: linha de serviço`, o `peça:` com o texto inteiro da linha (o `--conferir` lê esse texto) e o `resumo:` dizendo qual sinal ela capta e por que nenhuma promessa é esperada.

### Os passos

**Passo 1 · Recebe e prepara.** Salve a peça num arquivo de trabalho (`copy-em-analise.txt` na pasta de trabalho). O filtro 3 roda por arquivo, então isso não é opcional quando o ambiente tem shell.

**Passo 2 · Roda o lint (filtro 3) primeiro, porque é o único que é código.** Com shell: `python3 scripts/lint_copy.py copy-em-analise.txt`. Guarde a saída inteira. Falha dura significa reprovada, não importa o resto. Aviso não bloqueia sozinho.

**Passo 3 · Lê a peça uma vez pelo SENTIDO** e aplica os filtros 1 (CUB), 6 (Validador de conversão), 2 (Estrutura-mãe) e 5 (Verbatim), nesta ordem. O 6 vem colado no CUB porque a cascata dele decide se o resto ainda vale a pena: bastou um dos 5 critérios cair, a leitura para ali: os filtros 2 e 4 não rodam nesta rodada, e o 5 só levanta o que está sem lastro, pra linha `sem lastro:`.

**Passo 4 · Lê a peça outra vez pela FORMA**, ignorando o sentido, com `references/_padroes-estruturais-ia.md` do lado, e aplica o filtro 4 (pula na cascata). Esta passada é separada de propósito: o cheiro de máquina está no desenho da frase, não no assunto dela.

**Passo 5 · Monta o veredito** no formato abaixo e salva o arquivo.

**Passo 6 · STOP.** Quem chamou corrige e manda de novo. Loop até passar, com teto de 3 rodadas. Na terceira reprovação seguida, pare de sugerir e escale ao dono: "essa peça reprovou 3 vezes no mesmo filtro, olha as falhas e decide se ajusta a copy ou se o problema é a oferta."

### Modo rigoroso (padrão em peça de venda)

**Quando liga.** Sozinho, em toda peça de venda: headline de venda, capa de peça de venda, anúncio, carta, landing, oferta, roteiro de VSL, e-mail de venda, e os afins que pedem compra (carrossel e sequência de stories que vendem, página de captura). No feed educativo e no resto, só quando o dono pede: "valida no modo rigoroso", "passa no validador?", "isso é genérico?". Skill que chama o gate não desliga o rigoroso em nome do dono. Nunca liga na `linha de serviço`, nem dentro da página de captura.

**Chave do dono:** `rigor em venda: desligado`, dito na conversa ou gravado no perfil do dono, devolve a peça de venda ao modo padrão até ele religar.

- Roda os 6 filtros e soma os checkpoints de `references/validador-conversao-checkpoints.md` (mecanismo, voz, transformação, clareza, limpeza, proibições), que só rodam quando a peça passou nos 5 critérios do filtro 6.
- Dá a nota X/10 pela regra determinística de `references/validador-conversao-mestre.md` (10 só sem nenhuma falha).
- Veredito: `APROVADA` só com 10; abaixo disso, nota 9 inclusive, `REFAZER`, com a lista de reescrita ordenada por gravidade, as perguntas, o fecho, o registro e o gume de `references/validador-conversao-reescrita.md`.

**Por que é padrão só na venda:** onde a peça pede dinheiro, copy nota 9 perde a venda pra quem tem nota 10. No feed educativo o gate roda a cada entrega das skills de conteúdo e o post não pede compra; ali o rigoroso fica a pedido, pra o loop não emperrar quem chama o gate.

---

## O veredito (o formato da saída, sempre este)

**Aprovada:**

```
peça: <nome ou primeira linha>
tipo: headline
veredito: APROVADA
resumo: em 1 linha, o que a peça cumpre, dito como fato. Pode subir.
```

**Zero elogio no veredito.** Nem na aprovada nem na reprovada: sem "quase", sem "já melhorou", sem parabéns. A aprovada diz o que a peça cumpre; a reprovada diz o que falta.

**Reprovada:**

```
peça: <nome ou primeira linha>
tipo: carta
veredito: REPROVADA
falhas:
  - filtro: CUB
    dimensao: U de Inacreditável
    trecho: "a frase exata que falhou"
    motivo: 1 linha do porquê
    sugestao: a reescrita curta, já aplicável, nunca um conselho genérico
```

**Falha do filtro 6 (e do modo rigoroso):** o mesmo formato de 5 linhas, com o critério e a gravidade na `dimensao` e o molde de reescrita na `sugestao`:

```
  - filtro: Validador de conversão
    dimensao: critério 1, promessa copiável · gravidade 9
    trecho: "a frase exata que falhou"
    motivo: 1 linha do porquê
    sugestao: molde de promessa aplicado: "a reescrita pronta"
```

Com o filtro 6 rodando, o veredito também traz a linha `encaixe narrativo:` (medido contra o arco, ou `não medido, sem arco informado`). No modo rigoroso, soma `modo: rigoroso` e `nota: X/10` logo abaixo do `tipo`. Na cascata, soma a linha `suspenso pela cascata:`. O veredito reprovado fecha com a pergunta e o bordão de `references/validador-conversao-reescrita.md`.

Em lote, o arquivo abre com o consolidado e depois traz uma seção por peça:

```
lote: <nome do lote>  ·  5 peças  ·  2 aprovadas  ·  3 reprovadas
severidade: 1 bloqueante (falha dura de anti-IA) · 2 corrigíveis (CUB e Estrutura-mãe)
```

**Severidade, as 3 faixas:** *bloqueante* (falha dura do lint, ou fato do negócio inventado: não sai do jeito que está, sem discussão) · *corrigível* (falha de CUB, Estrutura-mãe ou anti-IA estrutural: a reescrita sugerida resolve) · *observação* (aviso do lint isolado, ou 1 padrão estrutural sozinho: aponta e segue, o dono decide). **No filtro 6 a faixa sai da gravidade:** 7 ou mais é bloqueante, 4 a 6 é corrigível, 3 ou menos é observação, com o teto do tipo de peça (tabela de peso abaixo). Gravidade 9 ou 10 (promessa genérica, custo de não agir ausente) reprova sozinha nas peças de venda.

**Lote roda em SÉRIE, peça por peça, nunca em paralelo.** O motivo é o filtro 4: dois padrões estruturais que aparecem na mesma peça reprovam, e a contagem se perde quando as peças são lidas juntas. Se o ambiente tiver delegação e o lote passar de 10 peças, delegue blocos de 5 peças, mas cada bloco continua lido em série por dentro. O consolidado do topo é montado só no fim, depois do último veredito.

---

## Os 6 filtros (a ordem de leitura está nos Passos)

### Filtro 1 · CUB (Confusão, Inacreditável, Boring)

Toda copy morre por um destes 3 motivos. Não tem um quarto.

- **C, Confusão.** Exige reler? Tem 2 ideias na mesma frase? Jargão ou rótulo solto? Abstração que não vira imagem?
- **U, Inacreditável.** Promessa grande sem chão do lado? Cheira a infoproduto? Um estranho acreditaria?
- **B, Boring.** Já ouviu mil vezes? Amplifica o problema óbvio no lugar da virada? Frase-ponte no lugar de tensão? (n/a na `linha de serviço`)

Exemplos fraco contra forte e o teste das 3 perguntas (visualizo, provo, só eu diria) em `references/_regua-cub.md`; na `linha de serviço`, o só eu diria é o critério 1 e fica n/a.

### Filtro 2 · Estrutura-mãe

A espinha de toda peça, do reel de 30 segundos à carta de 3 páginas. O que muda entre formatos é o tamanho de cada parte, nunca a ordem.

> Diagnóstico · Nomeação · Polaridade · Nova interpretação · Consequência · Movimento

**Diagnóstico** olha de cima e nomeia o que o leitor vive. **Nomeação** batiza o que ele sente e nunca soube dizer. **Polaridade** põe dois lados e uma tensão. **Nova interpretação** renomeia a causa e derruba o que ele já tentou. **Consequência** mostra que ficar como está custa caro. **Movimento** convida como continuação lógica, nunca como pedido.

Peça curta comprime, não pula; a `linha de serviço` é a exceção e cobra só o Movimento, porque as outras 5 partes são argumento. Furo mais comum: pular Nomeação (a peça vira aula) ou pular Polaridade (vira monólogo). Exemplos por formato em `references/_estrutura-mae.md`.

### Filtro 3 · Anti-IA lexical (em código)

`python3 scripts/lint_copy.py <arquivo>` (o script vem dentro desta skill).

Três camadas:
- **Falha dura (exit 1, zero tolerância):** travessão longo e a família do verbo-freio banido (use emperrar, empacar, prender).
- **Aviso (não bloqueia):** conectivo formal de IA (outrossim, ademais, vale ressaltar), frase-emoldura de revelação (a verdade é, o segredo, o que ninguém te conta), verbo genérico (alavancar, potencializar, transcender), clichê (pulo do gato, muda o jogo), abertura banida (imagine só, já se perguntou), fechamento que implora engajamento (comenta aí, marca aquele amigo), emoji decorativo, antítese nominal telegráfica, molde de negação-sobre.
- **Contagem (avisa quando excede):** literalmente (1 por peça), absolutamente (1), verdadeiro (1), antítese em espelho em série (2).

Zero falha dura é obrigatório pra passar. Aviso é log pro dono revisar, mas 3 ou mais avisos DIFERENTES na mesma peça reprovam o filtro: é o sinal de copy de máquina disfarçada.

**Sem shell no ambiente:** o filtro roda no olho com a lista acima, procurando item por item. Declare em 1 linha no veredito que o lint rodou na leitura e não em código.

**Como citar o trecho reprovado sem o próprio veredito reprovar.** O veredito precisa mostrar o trecho, e o trecho carrega o termo banido, então o lint do veredito pega a citação. A saída é sempre uma das duas: cite o trecho dentro de bloco de código cercado por três crases e linte o veredito com `python3 scripts/lint_copy.py <veredito> --ignore-code-blocks`, ou descreva a falha em prosa indireta ("a frase abre com o verbo-freio banido, terceira palavra"). A peça do dono é sempre lintada sem a opção; ela vale só pro arquivo do veredito. O que nunca se faz é reescrever a peça do dono pra o veredito passar no próprio lint, nem omitir o trecho pra fugir do bloqueio: a citação é a prova do achado. Checagem verificável antes de fechar: rode o lint no arquivo do veredito e confirme exit 0; reprovou pela citação, ela vai pro bloco de código.

### Filtro 4 · Anti-IA estrutural (no olho, o código não pega)

O filtro 3 é lexical: pega palavra e símbolo. A peça pode sair com exit 0 e mesmo assim cheirar a máquina, porque o problema está na FORMA da frase.

Os 12 padrões:

1. Simetria de frase (frases vizinhas do mesmo tamanho e do mesmo ritmo)
2. Tripla (item, item e item, com o terceiro sem fato novo)
3. Paralelismo mecânico (3 ou mais frases abrindo com a mesma palavra)
4. Adjetivo em par (dois sinônimos onde um bastava)
5. Abertura por definição (começa explicando o conceito no lugar de mostrar a cena)
6. Fechamento que resume (o último parágrafo repete o texto e não entrega fato novo)
7. Transição genérica (frase-ponte que só anuncia a próxima)
8. Escalada de três tempos (curta, média, longa, mais a frase de efeito sozinha na linha)
9. Número redondo sem fonte (90%, 3x, decorativo, ninguém contou)
10. Hedge (pode ajudar a, tende a, em geral: copy que se protege perde autoridade)
11. Cena sem corpo (sentimento e estado, sem hora, objeto ou pessoa, nada filmável)
12. Densidade uniforme (todo parágrafo com o mesmo peso, sem uma frase que carrega a peça)

**Régua:** 1 padrão aponta e sugere, não reprova sozinho. 2 ou mais REPROVAM mesmo com exit 0 no filtro 3, porque cheiro de máquina vem do conjunto. Exceção: o padrão 5 em headline ou capa reprova sozinho, o primeiro segundo não tem margem.

Cada padrão com exemplo ruim curto, versão consertada e teste de reconhecimento em `references/_padroes-estruturais-ia.md`.

### Filtro 5 · Verbatim (o lastro)

A copy NÃO inventa fato do negócio. Toda tese, prova, nome de mecanismo, número e história tem lastro em fonte que o DONO forneceu. Sem lastro, é chute que evapora.

As fontes são ENTRADA desta skill, nunca arquivo que ela sai procurando na máquina. Ordem de peso:
1. transcrição literal do dono falando (aula, live, call gravada), a fonte de maior peso, porque é a voz dele;
2. a tese-mãe escrita (narrativa canônica, documento de posicionamento, manifesto);
3. bancos derivados (desejos, promessas, verbatim de cliente, comentário e mensagem real);
4. o plano de posicionamento do dono, quando ele já tiver um.

Onde procurar, nesta ordem: os caminhos que quem chamou informou · a variável de ambiente `FONTES_LASTRO`, quando o ambiente tem shell e ela está definida · a pasta que o dono apontar na conversa.

**Como o filtro roda:** extraia os 2 ou 3 termos carregados da peça (nome de mecanismo, número, prova) e busque só esses nas fontes. Falhou algum, reprova, e a sugestão é uma de duas: trocar por afirmação ancorada, ou buscar o lastro antes de manter. Detalhe em `references/_verbatim-fontes.md`.

### Filtro 6 · Validador de conversão (o filtro-mestre)

Roda logo depois do CUB e pergunta se a peça MERECE ir pro público. Promessa que qualquer outro do mercado poderia dizer reprova. Os 5 critérios, com a gravidade de cada falha:

1. **Promessa copiável** (9): qualquer concorrente assinaria igual? Inclui o teste do concorrente (marca e método cobertos, promessa no perfil do outro), bloqueante em toda peça de venda.
2. **Dor verdadeira** (8): a dor escondida, em cena, ou a dor apresentável?
3. **Parar o scroll** (8): tem contraste ou quebra do esperado, ou é gostosa de ler e esquecível?
4. **Promessa executável** (8): resultado concreto, caminho visível, ação simples. Aprender, descobrir e dominar como promessa são sinal vermelho, sem exceção: a skill pede ao dono número, prazo e métrica reais e, sem lastro, manda reescrever pro que dá pra verificar.
5. **Risco de não agir** (10): o fantasma do ciclo que se repete, usado como arma; quem ignora paga, em silêncio, no próximo ciclo. Sem risco, sem urgência: reprova.

Também roda o **encaixe narrativo** (com o arco informado: ruptura ou contradição é bloqueante, ponte fraca é corrigível; sem arco, observação, porque a skill não inventa contexto) e o **registro da peça** (o tom combina com o estado do público: urgência, dúvida ou ação?).

**Por cima, só verdade e lei:** fato, número e data citados precisam de lastro (`references/10-verificador-lastro.md`); urgência e escassez só com janela real, porque prazo ou vaga inventados são publicidade enganosa; nicho regulado sem prazo de resultado nem antes e depois; anúncio em vídeo em forma aberta. **Cascata:** bastou um dos 5 critérios cair, para tudo e refaz do zero; critério n/a não aciona. O que o veredito traz na cascata, onde cada critério se aplica (peça de uma linha, peça sem oferta, `linha de serviço`), a escala inteira e o que já está coberto pelos filtros 1 a 5 em `references/validador-conversao-mestre.md`.

---

## Onde cada tipo de peça mais falha (o peso por tipo)

Todas as peças passam em todos os filtros. Estes são os pesos, pra a leitura focar onde a prática mostra que a peça quebra:

| Tipo | Filtro que pesa dobrado | Filtro 6 |
|---|---|---|
| headline, capa | CUB (B de Boring, é o teste do dedo no feed) + Verbatim | bloqueante |
| corpo de carrossel | Estrutura-mãe (arco de 7 a 10 slides com os 6 movimentos) + anti-IA lexical | corrigível no feed educativo; bloqueante no carrossel que vende |
| script de reel | CUB (C de Confusão, ele não pausa pra reler) + Estrutura-mãe comprimida | corrigível; bloqueante em anúncio |
| sequência de stories | Estrutura-mãe (observação, interpretação, tese) + CUB (B, ele fura em 1 toque) | corrigível na rotina; bloqueante na sequência de venda |
| carta, landing | Estrutura-mãe COMPLETA + CUB (U de Inacreditável em dobro) + Verbatim | bloqueante |
| oferta | CUB (U, cada entregável mata uma objeção) + Verbatim (garantia real, preço ancorado) | bloqueante |
| WhatsApp, e-mail | CUB (C, a mensagem se lê em 3 segundos no celular) + anti-IA (frase-ponte destrói intimidade) | bloqueante no e-mail de venda; corrigível no resto |
| script de SDR | CUB (C, ele responde em 30 segundos ou não responde) + Estrutura-mãe na primeira mensagem | corrigível |
| script de closer | Estrutura-mãe (Diagnóstico, Consequência, Movimento) + CUB (U na garantia) | bloqueante |

Fora da tabela, no filtro 6: `isca_copy` e `cta` bloqueante; `slide` herda o da peça-mãe; `pos_venda` e `bio` corrigível; anúncio e roteiro de VSL encaixam em `headline` e `carta` e herdam o bloqueante. **Por quê:** onde a peça pede compra, cadastro ou dinheiro, promessa genérica não converte e não sai; onde a peça ensina ou acompanha, a falta de tensão de venda é escolha do formato e vira ajuste, nunca bloqueio.

---

## Gate de qualidade (o gate passa no próprio gate)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


| Critério | Passa se |
|---|---|
| Lint em código | `python3 scripts/lint_copy.py copy-em-analise.txt` rodou nesta auditoria e a saída está citada no veredito |
| Teste do próprio gate | `python3 scripts/lint_copy.py SKILL.md` sai com exit 0; este arquivo obedece a régua que ele cobra |
| Duas passadas | a leitura pelo sentido e a leitura pela forma aconteceram separadas, não juntas |
| Trecho citado | toda falha traz o TRECHO exato, nunca só o nome do filtro |
| Sugestão aplicável | toda falha traz uma reescrita pronta, nunca "melhore a clareza" |
| Filtro 6 com gravidade | toda falha do filtro 6 traz critério, gravidade e molde; no modo rigoroso, a nota bate com a regra do `references/validador-conversao-mestre.md`; nenhum veredito traz elogio nem consolo |
| Saída em arquivo | o veredito está salvo em `veredito-copy-<slug>.md`, não só no chat |
| Teto de rodadas | na 3ª reprovação seguida, a skill escalou ao dono no lugar de insistir |

O veredito da auditoria é o pior item da tabela.

**O teste mínimo, quando o ambiente tem shell.** Rode o lint em dois arquivos que você mesmo escreve na pasta de trabalho: um com uma linha contendo um travessão longo, que precisa sair com exit 1, e um com uma linha limpa, que precisa sair com exit 0. Se o primeiro sair com exit 0, o script não está funcionando e a auditoria segue no olho, declarando isso no veredito.

## Quem chama esta skill

Toda skill que produz linha pública passa por aqui antes de entregar: as de conteúdo (soft-conteudo-headlines, soft-conteudo-carrossel, soft-conteudo-reels, soft-conteudo-stories, soft-conteudo-planner, soft-conteudo-multiplataforma), as de funil (soft-funil-carta, soft-funil-landing, soft-funil-isca, soft-funil-miniwebinar), soft-webinar, as de venda (soft-vendas-sdr, soft-vendas-closer), soft-plano-posicionamento, soft-apostila e soft-editor-video (o texto que vai na tela).

O dono também chama direto, e nesse caso a peça é o que ele colou.

## O que esta skill NÃO faz

- **NÃO escreve copy nova.** Recebeu texto vazio, devolve "sem texto pra criticar" e para. Pra escrever, a skill do formato: **soft-conteudo-headlines**, **soft-conteudo-carrossel**, **soft-conteudo-reels**, **soft-conteudo-stories**, **soft-funil-carta**, **soft-funil-landing**.
- **NÃO roda em brief interno**, plano de ação, documento de estudo ou nota do agente. Roda só em linha que o público vai ler.
- **NÃO substitui o julgamento do dono.** Ele pode aprovar uma peça com aviso de clichê quando for escolha de voz. A falha dura do lint sempre bloqueia.
- **NÃO faz pesquisa nem consulta fonte externa.** Todo o lastro vem do material que o dono forneceu.
- **NÃO altera o texto entregue.** Devolve o veredito. Aplicar a sugestão é de quem chamou, ou do dono. **Se quem chamou pedir a correção**, esta skill entrega o veredito e passa a peça pra skill de origem reescrever (**soft-conteudo-headlines**, **soft-conteudo-carrossel**, **soft-conteudo-reels**, **soft-conteudo-stories**, **soft-funil-carta**, **soft-funil-landing**), dizendo em 1 linha qual é. Ela nunca grava versão corrigida da peça, nunca roda uma segunda rodada sobre o texto que ela mesma mudou, e nunca se reaprova. Checagem verificável antes de fechar: a saída desta skill tem o veredito e a cópia de trabalho, e nenhum arquivo de peça reescrita; se existir um, apague o passo e devolva só o veredito.
- **NÃO decide posicionamento, tese ou oferta.** Isso é **soft-plano-posicionamento**. Se ela não estiver instalada, use a tese declarada na conversa como lastro e siga.

## Regras transversais

1. **Zero identidade de terceiro.** Nome de programa, de mesa ou de consultoria de outro negócio só entra nas references marcado "(exemplo, não copia)". A copy usa o naming do próprio dono.
2. **Lastro configurável.** Quem chama passa o caminho do material canônico. Sem ele, vale a ordem do filtro 5.
3. **Saída curta e estruturada.** O feedback não vira ensaio. Cada falha em 5 linhas: filtro, dimensão, trecho, motivo, sugestão.
4. **Anti-IA em dobro.** Este arquivo também passa no próprio lint. Zero falha dura, zero travessão, zero verbo-freio banido.

## Regra dura de frase, "toda frase se explica sozinha"

Vale em tudo que esta skill aprovar pro público.

Copy boa é frase que gera IMAGEM na cabeça de quem lê frio. Ela não pode assumir que o leitor já sabe o assunto, o produto, a categoria, o método, o mecanismo ou o antes e depois. Toda frase precisa se sustentar sozinha, sem depender do slide anterior, da bio, do título ou do que "obviamente é". Frase curta que soa afiada e deixa o entendimento pro contexto está reprovada.

**Teste antes de aprovar CADA frase:** se essa frase caísse solta no scroll de uma pessoa que nunca ouviu falar do produto, ela entenderia O QUÊ, PRA QUEM e O RESULTADO CONCRETO? Se não, reescreve nomeando explícito: qual é o objeto ("conta de calorias", não só "conta"), qual é o público ("mulher que já tentou emagrecer de todas as formas", não só "mulher que já tentou de tudo"), qual é o resultado concreto ("para de recomeçar a dieta", não só "para de recomeçar"). Na `linha de serviço` O QUÊ e PRA QUEM vêm do lugar em volta (regra no tipo), e resultado concreto não entra.

- Reprovado: *"Você come o que ama, um agente faz a conta do seu dia e você para de recomeçar."*
- Aprovado: *"Você passa a comer o que ama, um agente faz a conta de calorias do seu dia inteiro e não te deixa escorregar, e você para de recomeçar a dieta toda vez do zero."*

Somar 3 a 5 palavras que ancoram o contexto é melhor que a frase curta ambígua. Copy boa se mede por ser inequívoca e imagética; o tamanho vem depois.

### Regra irmã, "nenhum verbo órfão"

O leitor tem cérebro preguiçoso e NÃO vai completar sua frase. Todo verbo precisa vir com o OBJETO NOMEADO na mesma frase, senão a peça vira média. Verbos-armadilha que exigem complemento explícito: cortar (cortar o quê?), recomeçar, parar, mudar, melhorar, escapar, largar, controlar, ajustar, resolver, virar. Nomeie sempre o objeto concreto (arroz, pão, doce, dieta, treino, agenda, cliente, valor), nunca deixe aberto.

- Boa: *"Você come arroz, pão e o que ama, e uma ferramenta minha conta as calorias de tudo por você todo dia, pra você emagrecer sem viver de dieta."* Cada verbo com objeto.
- Média: *"...pra você emagrecer comendo o que gosta em vez de cortar."* Cortar o quê? O leitor não completa, desiste. Correto: *"...em vez de cortar arroz, pão e doce."*

Antes de aprovar a frase, sublinhe cada verbo e confira: cada um tem objeto nomeado?

## Arquivos desta skill

`references/_regua-cub.md` · `references/_estrutura-mae.md` · `references/_padroes-estruturais-ia.md` · `references/_verbatim-fontes.md` · `references/validador-conversao-mestre.md` · `references/validador-conversao-checkpoints.md` · `references/validador-conversao-reescrita.md` · `references/EXEMPLO-FIM-A-FIM.md` · `guia/GUIA-COPY-APLICACAO.md` · `guia/CODIGO-DE-ESCRITA.md` · `guia/03-identidade-voz.md` · `scripts/lint_copy.py`

O material de LASTRO (transcrição, tese-mãe, bancos de verbatim) não mora aqui: é entrada do dono, pelos caminhos que quem chama informar.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
