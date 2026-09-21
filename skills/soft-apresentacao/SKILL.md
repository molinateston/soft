---
name: soft-apresentacao
description: >-
  Cria, redesenha e EXPORTA uma apresentação completa: monta o deck em HTML 1920x1080 como fonte única e devolve PDF, PNGs, mosaico de conferência e PPTX . Serve deck novo a partir de tema, roteiro, fala ou documento, e redesenho de deck que já existe. Use quando o pedido for: "monta uma apresentação", "faz o deck", "preciso de um PowerPoint", "exporta em PPTX", "transforma esse texto em slides", "gera o PDF dos slides", "redesenha essa apresentação", "slides da palestra". NÃO use pra: converter conteúdo pronto em .docx, .xlsx ou PDF, ou ler arquivo desses que chegou (soft-exportar-documentos); "material da aula pra enviar depois" quando é a apostila de uma gravação (soft-apostila); a arte de peça de feed, banner ou capa (soft-designer); o lote de criativos (soft-criativo-campeao); o card print de tweet (soft-tweet-card); o roteiro e a oferta do webinar (soft-webinar); a copy de uma página (soft-funil-landing); o vídeo (soft-editor-video). Leia e siga o fluxo inteiro do SKILL.md.
---

# A apresentação inteira, do arco ao arquivo exportado

Esta skill monta um deck de slides e devolve os arquivos que a pessoa realmente usa: o HTML navegável pra apresentar, o PDF pra enviar, os PNGs pra reaproveitar, o mosaico pra aprovar de uma olhada e o PPTX pra quem exige PowerPoint. O HTML 1920x1080 é a fonte única; todo formato nasce dele, então o deck nunca diverge entre versões.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício de nicho neutro do início ao fim: o pedido que o dono deu, o bloco de perguntas de alinhamento já montado, a decisão de densidade, o arco de 12 slides, o STOP de aprovação do master, os comandos de export, o crivo visual com o que foi visto no mosaico e a lista final de arquivos entregues.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o conteúdo e eu monto o deck). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o conteúdo que o dono já colou. Se faltar um insumo que o deck não vive sem (o material dos slides, ou pra quem ele é apresentado), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o bloco de alinhamento uma pergunta de cada vez (o objetivo do deck, o público, o conteúdo bruto) e monta a apresentação com o que o dono for dando.

A pergunta do modo é UMA por deck. Mais duas partes entram nos passos abaixo:

- **Ensina enquanto faz:** ao escolher a densidade (quantos slides, quanto por slide), escreve UMA linha do porquê ("deck enxuto porque é pra apresentar ao vivo; slide cheio compete com a sua fala"), pra o dono decidir sozinho na próxima.
- **Oferece refinar no fim:** depois de mostrar o master ou o export, fecha com UMA linha de ajuste ("quer mais slides? mais enxuto? outra ordem? refaço só a parte que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "monta uma apresentação", "faz o deck", "transforma esse texto em slides", "slides da palestra" | **1 · DECK NOVO** |
| "redesenha essa apresentação", "esse deck está feio", "arruma os slides que eu já tenho" | **2 · REDESENHO** |
| "exporta em PPTX", "gera o PDF", "me manda os PNGs", "quero o mosaico" (o deck já existe e está aprovado) | **3 · EXPORT** |

Pedido ambíguo ("preciso de uns slides"): pergunte UMA coisa só, se o conteúdo já existe em algum lugar ou se nasce agora, mostre a tabela como cardápio e siga pela resposta.

## Como ler cada ação

Toda ação traz o mesmo bloco fixo: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · passos numerados com **STOP**.

**O perfil do dono vem do banco do agente.** Identidade visual, voz, oferta e prova: leia do perfil/brain do agente quando existir; se não existir, use o bloco de perguntas de alinhamento da ação e siga com o que faltar marcado `[A CONFIRMAR]`. Sem identidade declarada, o sistema B80/C20 é o padrão neutro, e você diz isso em 1 linha. Nunca herde produto, número, copy ou prova de outra pessoa.

---

## Ação 1 · DECK NOVO

**O que faz:** monta o arco, escreve a tela de cada slide, produz o master HTML e exporta os formatos pedidos.

**Precisa de:** o objetivo da apresentação e quem assiste, do dono · o conteúdo, que pode chegar pronto (roteiro, documento, transcrição de fala, notas) ou nascer aqui a partir do tema · o tempo de fala ou a quantidade de slides, do dono · a identidade visual, do perfil/brain do agente · a lista de saídas necessárias, do dono.

**Sem o insumo:** faça o bloco de perguntas de alinhamento abaixo, todas de uma vez, e não repita nada que o dono já respondeu. O que não vier, você assume e declara: sem identidade, B80/C20; sem tempo, 12 slides; sem lista de saídas, HTML mais PDF mais mosaico.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar. Os defaults acima valem só pra escolha de formato (identidade, quantidade de slides, lista de saídas); dado do negócio do dono, como preço, data, vaga, prazo ou prova, nunca entra por default.

**Deck de aula com oferta carrega a oferta inteira.** Quando a apresentação abre turma, vende ou convida pra um próximo passo pago, os slides finais trazem preço, parcelamento, vagas, data de início e garantia, cada um que existir no perfil do dono, mais a prova que ele já tem. Dado que existe no perfil e não aparece no deck é omissão que reprova a entrega, porque a aula gratuita existe pra abrir a turma. O que não existir no perfil sai como `[A CONFIRMAR: o quê]` no doc de handoff, nunca inventado dentro do slide.

> **Bloco de perguntas de alinhamento (mande assim, junto, uma mensagem só):**
>
> Pra montar o deck certo de primeira, me responde essas 6 rapidinho, pode ser em uma linha cada:
> 1. Qual o objetivo da apresentação e quem está na plateia?
> 2. O conteúdo já existe em algum lugar, ou nasce agora a partir do tema?
> 3. Quantos slides, ou quanto tempo de fala?
> 4. Você vai falar por cima dos slides, ou a pessoa vai ler sozinha depois?
> 5. Tem identidade visual sua (cor, fonte, logo)? Se não tiver, eu uso o padrão neutro.
> 6. Quais arquivos você precisa no fim: HTML navegável, PDF, PNGs, PPTX fiel, PPTX editável?

**Entrega:** `deck.html` (a fonte, navegável) · `deck.pdf` · `deck-png/slide-01.png` em diante · `MOSAICO.png` · `PPTX-FIEL.pptx` quando pedido · `PPTX-EDITAVEL-APROXIMADO.pptx` só quando pedido E validado. Tudo no diretório de saída do ambiente (`$OUTDIR`, ou a working dir quando não houver).

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/sistema-b80-c20.md` (a direção visual e a régua de decisão, INTEIRA, antes de desenhar).

**Profundidade:** `assets/master-b80-c20.html` (o master neutro pronto pra partir dele).

**Passos:**

1. Recupere dos arquivos e da conversa tudo que já estiver definido. Pergunte só o que faltar e mudar o resultado, pelo bloco acima.
2. **Escolha a densidade** pela resposta 4 (a régua está na seção própria abaixo). Pedido misto escolhe o modo dominante: aula ao vivo e palestra usam fala; relatório assíncrono usa leitura.
3. **Monte o arco pelo MÉTODO DE ARCO abaixo** (a seção própria) e escolha uma ideia dominante por slide. Nada de dois assuntos disputando o mesmo slide.
4. Produza o master HTML, pela régua da seção "Produzir o master" abaixo.
5. **STOP: mostre o master antes de exportar.** Pergunte exatamente: **"esse é o deck; o que ajusto antes de eu gerar os arquivos?"**. Exportar 4 formatos de um deck errado custa a rodada inteira, então a aprovação vem antes do export, não depois.
6. Exporte pelos comandos da seção "Exportar".
7. Faça o **crivo visual** da seção própria abaixo, no mosaico e nos slides suspeitos.
8. Corrija o master e reexporte tudo que depende dele. Entregue pela seção "Entregar".

---

## Ação 2 · REDESENHO

**O que faz:** pega um deck que já existe e refaz a tela dele sem perder o conteúdo.

**Precisa de:** o deck atual, em qualquer forma que o dono tenha (arquivo, PDF, prints, ou o texto colado dos slides) · o que incomoda nele, perguntado ao dono · a identidade visual, do perfil/brain do agente.

**Sem o insumo:** com só os prints ou o PDF na mão, extraia o texto slide a slide e devolva ao dono a lista do que você leu, pedindo que ele corrija antes de você desenhar. Sem saber o que incomoda, pergunte UMA coisa: "o que te incomoda nesse deck hoje, o visual ou o que está escrito?". Se for o que está escrito, o arco também é refeito.

**Entrega:** os mesmos arquivos da Ação 1, mais uma tabela curta de 3 a 6 linhas dizendo o que mudou e por quê (slide fundido, slide dividido, texto que saiu da tela e virou fala).

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/sistema-b80-c20.md`.

**Passos:** extrai o conteúdo → **STOP: confirma com o dono a lista do que foi lido** → decide a densidade → **refaz o arco pelo MÉTODO DE ARCO (seção própria)**, encaixando o conteúdo lido nas 6 fases, fundindo slide repetido e dividindo slide entupido → produz o master → **STOP de aprovação do master** → exporta → crivo visual → entrega.

---

## Ação 3 · EXPORT

**O que faz:** gera os formatos a partir de um master HTML que já existe e já foi aprovado.

**Precisa de:** o caminho do HTML do deck · a lista de formatos que o dono quer.

**Sem o insumo:** sem a lista de formatos, entregue o conjunto padrão (PDF, PNGs e mosaico) e pergunte em 1 linha se ele quer também o PPTX. Sem o HTML, esta ação não existe: volte pra Ação 1 ou 2.

**Entrega:** os arquivos pedidos, mais o mosaico sempre, porque é ele que o dono olha pra aprovar.

**Passos:** confere que o HTML abre e tem o palco de 1920x1080 → exporta → crivo visual no mosaico → entrega, dizendo em 1 frase a diferença entre os dois PPTX quando os dois foram gerados.

---

## Método de arco (a espinha da aula, 6 fases)

O arco é a ESPINHA da aula. As 6 fases abaixo entram sempre nesta ORDEM, e cada uma faz um trabalho que a próxima não faz. O que varia é quantos slides cada fase ocupa: a densidade que você já decidiu no passo anterior manda, então uma fase pode ser 1 slide ou 3 (o "3 erros" da fase 2 costuma render 3 ou 4 slides; a virada quase sempre é 1). A ordem das 6 é fixa, o número de slides por fase é livre.

1. **Abertura que para.** A headline que prende antes de a fala começar. É a tela que a pessoa lê enquanto você respira, e ela sozinha tem que fazer a plateia parar de olhar o celular.
2. **Problema e inimigo.** Nomeia a dor e aponta o culpado (o modelo velho, o hábito errado, a crença que segura a pessoa), com número quando houver. O inimigo dá endereço pra dor: sem ele, a plateia acha que o problema é ela mesma.
3. **A virada.** O reenquadre que vira o jogo, o "o que você pensava não é o que está acontecendo". Aqui a plateia larga a explicação antiga e adota a sua. A virada tem que MOVER a pessoa de um lugar pra outro, não repetir a dor da fase 2 com outras palavras.
4. **O método.** O sistema nomeado, o "como" concreto: o passo a passo, a janela, a tabela, a régua. É a fase que entrega o que a pessoa leva pra casa e usa. Nomear o método faz ele virar coisa, e coisa a plateia lembra.
5. **A prova.** O caso real, o antes e depois, o teste que a pessoa faz sozinha. Prova é caso com nome, número e resultado, ou o convite pra ela mesma testar. Sem prova, o método vira alegação.
6. **A oferta e o CTA.** SÓ na aula-que-vende. Preço, parcelamento, vagas, data de início e garantia, cada um que existir no perfil do dono, mais a prova que ele já tem, e o próximo passo claro. Puxa a regra inteira de "Deck de aula com oferta carrega a oferta inteira" (Ação 1): dado que existe no perfil e não aparece aqui é omissão que reprova; o que não existir sai como `[A CONFIRMAR]` no handoff, nunca inventado no slide.

**Onde a aula para.** A aula PURA (palestra, treinamento, aula gratuita SEM abrir turma) para na fase 5 e fecha com o convite pro próximo passo grátis: o teste, o exercício, o material. A aula-QUE-VENDE segue até a fase 6. Se a plateia sai sem ter o que fazer amanhã de manhã, faltou o fecho da fase 5 ou da 6.

### Régua de corte por fase (cada fase faz o SEU trabalho)

Antes de montar a tela, passe cada fase por esta pergunta. A fase que não faz o próprio trabalho volta pra escrita, não pro slide.

- **Abertura:** para de verdade, ou só anuncia o tema? Título que descreve o nome da aula não para ninguém (a régua de títulos já reprova isso).
- **Problema e inimigo:** o culpado tem endereço, ou a dor fica solta no ar?
- **A virada:** reenquadra de verdade, ou só repete o problema da fase 2 com outras palavras? Esta é a que mais escorrega.
- **O método:** é um "como" que a pessoa executa, ou uma promessa de que existe um jeito?
- **A prova:** é caso real com nome/número/resultado (ou um teste que ela faz sozinha), ou é alegação sem caso? Esta é a segunda que mais escorrega.
- **Oferta e CTA:** o próximo passo é uma ação clara, ou termina no vácuo?

As duas fases que mais escorregam, com um exemplo curto que reprova e o conserto:

```
A VIRADA
  reprova (só repete o problema): "Comer errado antes da prova custa caro."
    isso é a dor da fase 2 de novo, não uma virada.
  passa (reenquadra, move a pessoa): "Você achava que era disciplina. O buraco
    está no HORÁRIO." A plateia troca a explicação antiga pela sua.

A PROVA
  reprova (promessa sem caso): "Ajustar o horário muda o seu resultado."
    promete sem mostrar o caso que sustenta.
  passa (caso real com número): "Um corredor mudou só o horário da refeição e
    tirou 4 minutos nos 10k." nome, mudança única, número. Sem o número na mão,
    marca [A CONFIRMAR] e não inventa.
```

## Escolher a densidade

- **Guiada pela fala:** uma ideia por slide, headline grande, 1 a 3 pontos, respiro generoso, área da câmera preservada quando houver apresentador em vídeo.
- **Feita pra leitura:** contexto suficiente no próprio slide, blocos estruturados, tabela e diagrama quando aumentarem a compreensão. Dividir o slide antes de reduzir demais a fonte.

## Produzir o master (a régua acionável)

1. Leia `references/sistema-b80-c20.md` antes de desenhar. Em resumo: **80%** é fundo preto, texto claro e grande, verde pontual numa palavra ou número, muito espaço negativo, uma área focal, composição simples, câmera fixa quando houver apresentador. **20%** é número, processo, prova, comparação ou diagrama, e só quando explicarem melhor o conteúdo. Nunca detalhe como decoração, nunca coleção de cards, nunca excesso de moldura, nunca caixa alta em headline, nunca mudança de linguagem visual entre slides.
2. Parta de `assets/master-b80-c20.html`, ou escreva um HTML equivalente.
3. Mantenha cada `.slide` num palco fixo de 1920x1080 e escale o palco inteiro pra qualquer tela, sem reflow responsivo.
4. Inclua navegação por teclado, toque e roda; respeite `prefers-reduced-motion`.
5. Mantenha CSS e JavaScript dentro do próprio HTML. Use caminho relativo pra imagem local.
6. Havendo apresentador, reserve a câmera na mesma posição em todos os slides e impeça qualquer conteúdo de invadir essa área.
7. Registre as notas de fala como comentário HTML, atributo `data-notes`, ou notas do PPTX editável quando o fluxo exigir.
8. **Precedência de cor (regra que decide sozinha).** A identidade declarada do dono vence a cor default do B80/C20. Com identidade declarada, o fundo, a cor de texto e a cor de destaque saem dela, e o que o B80/C20 continua mandando é a régua: uma área focal por slide, respiro amplo, destaque em uma palavra ou número por slide, contraste de texto sobre fundo de no mínimo 4.5:1. Sem identidade declarada, vale o default do sistema (fundo preto, texto claro, verde pontual). Nunca os dois ao mesmo tempo: é proibido misturar fundo preto default com paleta declarada do dono no mesmo deck.
9. **Checagem antes de exportar (o agente lista e prova).** Escreva no handoff estas 3 linhas, com o valor real: (a) origem da paleta: `identidade do dono` ou `default B80/C20`; (b) os valores usados: fundo `#…`, texto `#…`, destaque `#…`; (c) contraste medido texto sobre fundo: `X:1`, e ele passa de 4.5:1. Deck sem essas 3 linhas preenchidas não sai.
10. Adapte tipografia e marca à identidade do dono preservando a hierarquia e o respiro do sistema. Não copie conteúdo dos exemplos.

O PowerPoint nunca é a fonte visual. O HTML governa.

## Exportar

```bash
node scripts/export-deck.mjs CAMINHO/DECK.html --format=pdf,png,pptx --out=CAMINHO/SAIDA --pptx-mode=image
node scripts/export-deck.mjs CAMINHO/DECK.html --format=pptx --out=CAMINHO/SAIDA --pptx-mode=editable
python3 scripts/fix_editable_dark.py CAMINHO/SAIDA/DECK-editable.pptx CAMINHO/SAIDA/DECK-PPTX-EDITAVEL-APROXIMADO.pptx
python3 scripts/make_mosaic.py CAMINHO/SAIDA/DECK-png CAMINHO/SAIDA/MOSAICO.png
```

Os dois modos de PPTX têm nome explícito, e a diferença vai dita ao dono em 1 frase:

- `PPTX-FIEL.pptx`: cada slide é uma imagem, idêntico ao deck, não editável.
- `PPTX-EDITAVEL-APROXIMADO.pptx`: texto e formas editáveis, pode variar em fonte, quebra e espaçamento.

Nunca prometa fidelidade do modo editável. Se o render editável perder contraste, cortar texto ou descaracterizar o deck, corrija e valide; se não der, não entregue esse modo e diga por quê.

**O binário é lido de volta antes de fechar, e o `.html` de origem não responde por ele.** Extraia o texto de cada `.pptx` gerado (`unzip -p <deck>.pptx 'ppt/slides/slide*.xml'` e os `<a:t>`), cole `caracteres: N · linhas com acento: N` ao lado da mesma contagem sobre a fonte, e rode o lint sobre o texto extraído: **zero acento num texto em português com mais de 200 caracteres, com a origem acentuada, reprova o deck**, e o `python3 scripts/checar_titulos.py --conferir <pasta>` reprova sozinho com `deck sem acentos`.

No padrão B80/C20 o exportador pode converter transparência de CSS em branco. Rode `fix_editable_dark.py` antes do render editável: ele restaura o fundo preto e os blocos que acompanham o campo escuro. Use só em deck escuro.

## O que fazer sem shell, sem Node ou sem Python

| Falta | O que a skill faz |
|---|---|
| **Sem shell** | Entrega o `deck.html` salvo no disco e diz em 1 linha: nos ambientes que renderizam HTML ele já é apresentável; pra virar PDF, o dono abre no navegador e imprime em PDF no formato paisagem. |
| **Sem Node** | Sem `export-deck.mjs` não sai PDF, PNG nem PPTX pelo script. Entrega o HTML e o caminho de impressão pra PDF pelo navegador, e avisa que o PPTX fica pendente. |
| **Sem Python** | O mosaico e a correção do PPTX escuro não rodam. Entrega os PNGs individuais no lugar do mosaico, e não entrega o modo editável (sem `fix_editable_dark.py` ele sai com o fundo quebrado). |
| **Sem navegador headless** | O `export-deck.mjs` depende dele; a saída degradada é a mesma do "sem Node". |

Em toda linha acima, o que a skill nunca faz é dizer que não consegue. Ela nomeia a saída reduzida e entrega essa.

## Crivo visual (obrigatório, depois do export)

Deck exportado que ninguém olhou não está pronto. Existência de arquivo não é prova de qualidade.

**Quando o ambiente tem leitor de imagem:**

1. Confira a quantidade de PNGs e a dimensão 1920x1080 de cada um.
2. Confira que o PDF está em 16:9 e com o número certo de páginas.
3. Valide cada PPTX como arquivo e renderize pra inspeção.
4. **Abra o mosaico e olhe todos os slides**, procurando: corte de texto, estouro de container, sobreposição, contraste fraco, margem inconsistente, invasão da área da câmera, slide repetido e excesso decorativo.
5. Abra em tamanho cheio todo slide denso ou suspeito.
6. **Liste ao dono o que você conferiu e o que viu**, em 3 a 6 linhas. **O crivo não se declara feito, ele se escreve.** Pra cada peça aberta, registre em 1 linha o que foi OBSERVADO no ponto de risco, com o valor: quantas linhas ocupa o título mais longo, se o número principal está centrado no bloco dele ou empurrado pro rodapé, onde termina a captura, qual slide tem a margem mais apertada. **Crivo que só diz "conferido, sem problemas" não conta como feito** e a entrega volta: foi exatamente assim que um título de 6 linhas e um cartão de número quebrado passaram por um crivo declarado.

   **As três medições obrigatórias, com número ou sim/não, na largura mobile de 390px:** (1) `título principal: N linhas`, e **acima de 4 linhas reprova e o título volta pro passo de escrita**; (2) `número principal dentro do bloco? sim/não`; (3) `última seção visível sem corte lateral? sim/não`. Sem essas três linhas o crivo não conta como feito, por mais observação boa que venha junto: registrar só o que está certo é como o defeito atravessa um crivo escrito.
7. Corrija o master e reexporte tudo que depende dele. O crivo é um laço até passar, não uma passada só.

**Quando o ambiente NÃO tem leitor de imagem:** confira por medida (contagem de arquivos, dimensão, tamanho em bytes de cada PNG, contagem de páginas do PDF), e **declare em 1 linha que você não viu os slides**: "não tenho leitor de imagem aqui, conferi contagem, dimensão e tamanho dos arquivos; a conferência visual de corte e sobreposição fica com você no mosaico antes de apresentar".

## Gate de qualidade (roda antes de entregar)

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`references/regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **O inventário varre o perfil do dono INTEIRO, não só os campos que esta entrega consumiu:** cada campo do perfil é uma linha, e campo com vários valores (paleta com 3 cores; oferta com preço, parcela, bônus e garantia) rende uma linha por valor. **Entrega cujo `Dados fornecidos: N` for menor que o número de campos do perfil recebido reprova sem análise de conteúdo.** Qualificar a linha ("relevantes ao objeto", "considerados para esta entrega") também reprova: o total é o total. **Onde a linha mora:** no arquivo que o dono lê. Quando a entrega é uma peça de copy publicável (headline, carrossel, slide, card, chat, roteiro, deck), a peça NÃO recebe a tabela: a tabela vai num arquivo irmão de handoff (`HANDOFF-<slug>.md`) e só a linha de fechamento fica na peça, no rodapé. Inventário só no relato de processo, sem a linha na entrega nem o handoff no disco, reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.


| Check | Passa se |
|---|---|
| **Uma ideia por slide** | cada slide tem uma ideia dominante; dois assuntos disputando reprova |
| **Densidade coerente** | o deck inteiro segue o modo escolhido (fala ou leitura), sem alternar de slide pra slide |
| **B80/C20** | o recurso didático aparece só quando explica; se sumir e o slide continuar compreensível, ele era decoração e sai |
| **Palco fixo** | todo `.slide` mede 1920x1080 e escala inteiro, sem reflow |
| **Área da câmera** | havendo apresentador, a área está na mesma posição em todos os slides e nada invade |
| **Contraste e corte** | nenhum texto cortado, estourado ou sobreposto; contraste forte contra o fundo |
| **PPTX honesto** | o modo editável está nomeado como aproximado, e não foi entregue se descaracterizou o deck |
| **Crivo declarado com o que foi VISTO** | o crivo visual rodou e o dono recebeu, por peça aberta, 1 linha com o valor observado no ponto de risco (linhas do título mais longo, posição do número principal, fim da captura), ou o aviso de que os slides não foram vistos. "Conferido, sem problemas" não conta |
| **Régua de títulos, título a título** | cada título de slide passou pela régua de títulos (`references/regua-de-titulos.md`), e a checagem lista os N títulos com `<título> \| gatilho: <qual> \| veredito: passa` ou `\| reescrito de: <versão anterior>`. **Título de abertura que só descreve o nome da aula reprova o deck:** a tela de abertura é a que mais precisa parar a pessoa, e o nome do evento partido em dois é rótulo, não título |
| **Antítese telegráfica, cota CONTADA** | conte quantos títulos do deck usam o molde de duas orações curtas simétricas separadas por ponto ("X assim. Y assado.", ou a negação seguida da virada afirmativa na forma "não é <isto>", ponto, "<é aquilo>"). **Cota máxima: 1 a cada 4 títulos.** Acima disso o deck inteiro volta pra reescrita, mesmo com cada título passando sozinho: a repetição do molde é o tell, não a frase. Cole a contagem antes de exportar: `títulos em molde de antítese: N de NN (teto: NN dividido por 4)` |
| **`[A CONFIRMAR]`** | todo número, prova e dado sem fonte está marcado, nunca preenchido com um valor plausível. O marcador vive no doc de handoff, nunca dentro da peça exportada: na arte final, use a versão da frase sem o número ou um espaço neutro, e leve o `[A CONFIRMAR]` pro handoff. Marcador visível no arquivo que vai pro público reprova. |
| **Anti-IA** | zero travessão longo e zero da família do verbo-freio banido pela régua anti-voz no texto que vai pra tela. Com shell, rode o lint de copy das skills de conteúdo quando estiver instalado; sem shell, busca manual dos dois |
| **VEREDITO** | é o pior item acima. Uma falha corrige e reexporta |

## Entregar

Entregue o resultado utilizável, não o bastidor:

- o **mosaico PNG** primeiro, porque é ele que aprova de uma olhada;
- o **HTML navegável**;
- o **PDF**;
- a pasta de **PNGs** quando pedida;
- o **PPTX fiel**;
- o **PPTX editável aproximado** só quando pedido e validado.

Feche conduzindo o próximo passo: revisar o piloto, corrigir um slide específico, ou escalar pro restante do material.

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. Se a skill indicada não estiver instalada, faço aqui em modo reduzido e digo em 1 linha o que ficou de fora.

- A **arte de peça de feed**, banner, carrossel, capa → **soft-designer** (o deck 16:9 sem PPTX também mora lá).
- O **roteiro, a oferta e o deck do webinar** dentro da esteira → **soft-webinar**.
- A **copy de uma página** → **soft-funil-landing**.
- A **apostila navegável** de uma aula gravada → **soft-apostila**.
- O **vídeo** da apresentação, corte e legenda → **soft-editor-video**.
- A **headline** ou o gancho de texto → **soft-conteudo-headlines**.

## Recursos da pasta

- `references/regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta, leia antes de começar.
- `references/sistema-b80-c20.md`: a direção visual e a régua de decisão.
- `assets/master-b80-c20.html`: o master neutro 1920x1080.
- `scripts/export-deck.mjs`: exporta o HTML pra PDF, imagens e PPTX.
- `scripts/fix_editable_dark.py`: corrige fundo e transparência do PPTX editável escuro.
- `scripts/make_mosaic.py`: monta o mosaico dos PNGs.
- `shared-references/filtro-anti-ia/`: a mesma régua anti-IA por escrito, pro motor que não tem shell pra rodar o lint. `padroes-banidos.md` lista o que reprova; `falsos-positivos.md` roda antes de reprovar qualquer trecho.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Sem sandbox (a régua escrita, quando o lint não roda).** Motor sem shell não executa `scripts/lint_copy.py`, e isso não dispensa o anti-IA: aplique a régua no olho por `shared-references/filtro-anti-ia/padroes-banidos.md`, padrão por padrão, e passe cada reprovação por `shared-references/filtro-anti-ia/falsos-positivos.md` antes de mandar o trecho de volta pro passo de escrita, porque prosa autoral do dono cai no mesmo crivo e some se ninguém conferir. A entrega sai do mesmo jeito, no melhor que esse motor alcança, e o relato fecha com uma linha dizendo que a conferência anti-IA foi no olho, sem código: `anti-IA: conferido no olho pela régua escrita (sem shell nesta rodada)`. Calar o que ficou de fora reprova a entrega; declarar em uma linha reprova nada.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
