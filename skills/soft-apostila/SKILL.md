---
name: soft-apostila
description: >-
  Transforma uma aula ou live gravada (Zoom, YouTube, MP4) numa APOSTILA navegável: extrai o áudio, transcreve, limpa as muletas de fala, segmenta em 8 a 15 capítulos, enriquece cada um e devolve em Markdown ou como site HTML de arquivo único com índice clicável. Âncora: existe uma GRAVAÇÃO e o dono quer ler o conteúdo dela. Use quando o pedido for: "transforma essa aula em material", "vira apostila", "material de apoio da live", "handout pros alunos", "quero o conteúdo dessa gravação escrito", "transcreve e organiza essa aula", "bônus do webinar a partir da gravação", "material da mentoria". NÃO use pra: deck de slides, PPTX ou PDF de apresentação (soft-apresentacao); arte e carrossel em PNG (soft-designer); publicar o .md como Google Doc (soft-google-docs); conteúdo de feed (soft-conteudo-carrossel, soft-conteudo-reels); página de captura ou venda (soft-funil-landing); a isca em si (soft-funil-isca); edição de vídeo (soft-editor-video). Leia e siga o fluxo inteiro do SKILL.md.
---

# A gravação vira material que a pessoa consegue usar

Esta skill pega algo que o dono já gravou (aula, live, webinar, call de mentoria) e devolve um material indexado, navegável e versionável, sem plataforma de ensino engessada e sem PDF que ninguém abre. O pipeline é o mesmo sempre: áudio, transcrição, limpeza, capítulos, enriquecimento, render. O destino muda com o ambiente.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Os arquivos que cada ação exige (`--exige`).** A conferência roda `--conferir <pasta> --exige <lista>`, e arquivo ausente sai com exit 1 e `arquivo exigido pela ação ausente: <nome>`.
- Ação 1 · APOSTILA COMPLETA: `--exige apostila-*.md`
- Ação 2 · RENDER E PUBLICAÇÃO: `--exige apostila-*.md,index.html`
- Pacote (1 e 2): `--exige apostila-*.md,index.html`

**Entregar o markdown num pedido que também pede o site é entrega incompleta, não escopo reduzido.**

**O último capítulo, bloco ou seção carrega tese no título, como todos os outros.** `Resumo`, `Conclusão`, `Considerações finais`, `Fechamento` e `Recapitulando` são rótulos de estrutura e reprovam a régua. O lugar que o leitor lê por último recebe a frase mais concreta do material, jamais a mais geral. Cole `capítulos: N · com tese no título: N`, iguais.

**O HTML se confere no corpo montado, nunca no arquivo.** Rode o grep de marcador e de frase de bastidor (`entra aqui|preencher|antes de publicar|placeholder|a definir|pendente`) sobre o **texto que o HTML renderiza**: página que monta o corpo por script esconde o marcador da varredura estática, e a peça pública não carrega bastidor renderizado. Cole `marcadores no corpo renderizado: 0 · frases de bastidor renderizadas: 0`.

**A voz do dono se confere no arquivo inteiro, nunca nas aberturas.** Rode `grep -nE '\b(ela|ele|<nome do dono>|a professora|a autora) (abre|traz|explica|diz|conta|é|fala|mostra)' <peça>` sobre TODO o corpo e cole a saída literal, inclusive vazia. Uma única frase em terceira pessoa dentro de um material em primeira reprova. Cole `frases em terceira pessoa sobre o dono: 0`.

**Num universo acima de 20 títulos, a R7 exige versão morta colada.** `reescritos` igual a 0 ou 1 num lote desse tamanho é a régua rodando de leve: cole a versão morta de pelo menos três títulos, mostrando que a reescrita foi tentada e a original venceu. O `--conferir` sai com exit 1 quando `reescritos` fica abaixo de 5% do universo.

**Número marcado `[A CONFIRMAR` no perfil não entra na peça, com ou sem ressalva ao lado.** Rode `grep -nE '\[A CONFIRMAR' <perfil>` e cole a saída. Para cada número que voltar, a peça usa a forma sem prazo (`depois de algumas semanas`, `ao longo do protocolo`) e o número fica só no arquivo de notas. **A ressalva ao lado do número não conserta o número**, ela documenta que ele foi publicado assim mesmo, e o leitor lê o número primeiro; registrar a pendência num arquivo à parte também não autoriza, porque quem lê a peça não abre as notas. Cole `números não confirmados no perfil: N · publicados na peça: 0`.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício de nicho neutro do início ao fim: a gravação que o dono mandou, as perguntas que a skill fez, o aviso de tempo e custo, um trecho da transcrição crua, o mesmo trecho depois da limpeza, o índice de capítulos aprovado no STOP, um capítulo enriquecido inteiro e a lista final de arquivos.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já monto a apostila com o brain + o que você colou (o link ou o arquivo da aula). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com a gravação que o dono já mandou. Se faltar um insumo que a apostila não vive sem (a fonte da aula, ou pra quem ela é), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez (a gravação, o público da apostila, o tema/ID) e monta o material com o que o dono for dando.

A pergunta do modo é UMA por material. As outras três partes entram nos passos abaixo, marcadas onde caem:

- **Ensina enquanto faz:** ao decidir a segmentação em capítulos e o grau de enriquecimento de cada um, escreve UMA linha do porquê ("cortei aqui porque muda de assunto; capítulo curto ensina melhor que um bloco de trinta minutos"), pra o dono aprender a fatiar sozinho na próxima.
- **Puxa o material bruto:** quando o dono não souber pra quem é a apostila ou o que ela deve deixar pronto, não segue no genérico ("é sobre a aula"). Pergunta o concreto: "quem vai ler isso, e o que essa pessoa precisa saber fazer depois de ler?". Contexto raso vira apostila rasa.
- **Oferece refinar no fim:** depois de mostrar o material, fecha com UMA linha de ajuste ("quer mais enxuto? capítulo a mais? outro tom no título? mexo só na parte que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "transforma essa aula em material", "vira apostila", "aproveita essa gravação", "handout pros alunos" (só o vídeo na mão) | **1 · APOSTILA COMPLETA** (o pipeline inteiro, passos 1 a 7) |
| "eu já tenho a transcrição", "organiza esse texto que eu já transcrevi" | **1, entrando no passo 3** |
| "monta o site da apostila", "publica isso" (o markdown já está pronto e aprovado) | **2 · RENDER E PUBLICAÇÃO** |

Pedido ambíguo ("faz alguma coisa com essa gravação"): pergunte UMA coisa só, pra quem esse material vai (aluno pagante, lead que baixou uma isca, ou comprador do webinar), porque a resposta muda a profundidade e o tom de cada capítulo.

## Como ler cada ação

Toda ação traz o mesmo bloco fixo: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · passos numerados com **STOP**.

**O perfil do dono vem do banco do agente.** Voz, nicho, identidade visual e público: leia do perfil/brain do agente quando existir; se não existir, faça as 3 perguntas da ação e siga com o que faltar marcado `[A CONFIRMAR]`. A skill é marca-neutra: cor, fonte e marca vêm do dono, nunca de um padrão que a skill inventa como se fosse dele.

**Os invioláveis:** mantém a VOZ e os exemplos reais do dono, nunca inventa conteúdo que ele não falou · não resume, enriquece (a apostila é mais longa que a fala, não mais curta) · toda copy escrita aqui passa pelo filtro anti-IA · número, caso e promessa que ele citou sem fonte saem marcados `[A CONFIRMAR]`.

**A fonte é a gravação, não o perfil.** A apostila explica a AULA para quem assistiu, então toda afirmação escrita na voz do dono precisa de uma marca de tempo correspondente na transcrição. Dor, público, oferta e número que existem no perfil do dono mas não foram ditos na gravação **não entram no corpo do capítulo**: viram nota de contexto identificada como tal, ou ficam de fora. Checagem verificável antes de fechar: escolha 3 afirmações de conteúdo por capítulo e aponte, ao lado de cada uma, a marca de tempo da transcrição que a sustenta; afirmação sem marca de tempo sai do capítulo ou vira nota de contexto identificada.

**Onde a âncora mora.** A marca de tempo ou a referência de origem de cada trecho é obrigatória e **NÃO aparece no corpo que o aluno lê**. Ela vai num bloco `Origem` no fim de cada capítulo, ou num atributo do arquivo de página que só aparece ao passar o mouse. **Marca de tempo dentro do parágrafo reprova o acabamento:** rastreabilidade é pra o dono conferir contra a gravação, não pra o aluno tropeçar. Quem lê a apostila não tem o vídeo aberto ao lado, então `[02:10, 06:40]` no meio da frase interrompe a leitura sem informar nada. Checagem verificável: com shell, `grep -c "\[[0-9][0-9]:[0-9][0-9]" apostila.md` contando só as linhas de corpo; sem shell, releia os parágrafos. Cole `marcas de tempo no corpo do capítulo: 0 · em bloco Origem ou atributo: N`.

**Número que o dono marcou como incerto continua incerto na apostila.** Prazo, resultado e quantidade que o perfil ou o insumo trazem com marca de dúvida entram com a mesma ressalva, e **nunca viram base de argumento pedagógico**: escrever que o resultado apareceu em seis semanas e depois usar essas seis semanas pra provar que a ordem do método funciona é inferência sobre dado incerto apresentada como fato, e reprova. Checagem colada: `números incertos na fonte: N · usados com a ressalva: N · usados como prova de mecanismo: 0`.

**Leitura em voz alta do corpo antes de renderizar.** Releia cada capítulo procurando frase quebrada, concordância que não fecha e período que se contradiz ("os mesmos seis meses, os mesmos 12 semanas" é a família inteira: dois números de unidades diferentes na mesma enumeração). A apostila é produto que o aluno lê inteiro, então uma frase emperrada aparece. Cole `capítulos relidos em voz alta: N de N · frases reescritas: N`.

**A apostila ensina, não comenta a si mesma.** O corpo que a aluna lê explica a aula. Nota de revisão, política de anonimização, decisão editorial e pendência de prova vão para o handoff e para o relatório, nunca para o corpo. Checagem verificável antes de fechar: busque no `apostila.md` as marcas de comentário editorial (nota de revisão, decisão, anonimização, pendência) e prove que o corpo não tem nenhuma; comentário sobre a própria apostila dentro do corpo reprova a entrega.

---

## Ação 1 · APOSTILA COMPLETA

**O que faz:** roda o pipeline inteiro, da gravação ao material final.

**Precisa de:** o arquivo da gravação (MP4, MP3, ou o link do vídeo) · pra quem o material vai, perguntado ao dono · a identidade visual, do perfil/brain do agente · shell com `ffmpeg` e um transcritor instalado, pra transcrever.

**Sem o insumo:** as 3 perguntas de alinhamento abaixo cobrem tudo que muda o resultado. Sem shell ou sem transcritor, veja a seção "O que fazer sem X": a skill pede a transcrição ao dono e entra no passo 3, em vez de dizer que não consegue.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

> **As 3 perguntas (mande juntas, uma mensagem só):**
> 1. Esse material vai pra quem: aluno que já pagou, lead que está conhecendo você, ou comprador de um produto específico?
> 2. Você quer o material fiel à aula, ou quer que eu corte o que ficou datado e organize por assunto?
> 3. Tem cor, fonte ou logo seu pra eu aplicar? Se não tiver, eu entrego neutro e você me passa depois.

**Entrega, e ela muda com o ambiente:**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

| Ambiente | Entrega |
|---|---|
| **Com shell e sistema de arquivo** | `apostila.md` (o conteúdo) mais `index.html` (arquivo único, índice na lateral, navegação por teclado, leitura no celular). Publicação, quando o dono pedir, num host de site estático. |
| **Só conversa, sem arquivo** | `apostila.md` em Markdown limpo, capítulo por capítulo, mostrado na tela. Mesmo conteúdo, sem o site. |

A regra é: sem arquivo entrega Markdown, com arquivo entrega site.

**Leia primeiro:** `references/reference.md` (o método completo, com os comandos, os prompts de cada etapa, o template HTML inteiro e a tabela de erros comuns, INTEIRO antes de rodar o passo 1).

**Profundidade:** a mesma reference traz as variações (player de áudio sincronizado, embed do vídeo, quiz por capítulo, export em PDF) e a tabela de erros comuns por etapa.

### Antes do passo 1: o aviso de tempo e custo

Diga ao dono, antes de começar, em 3 linhas:

> "Uma aula de 1 a 2 horas leva de 30 a 90 minutos pra virar apostila, e a maior parte disso é a
> transcrição rodando sozinha. A transcrição local não custa dinheiro, custa tempo de máquina; o
> modelo médio é o que eu uso por padrão porque o pequeno erra nome próprio em português. Se você
> quiser mais rápido, dá pra usar o modelo pequeno, com mais erro de nome pra corrigir depois."

Esse aviso vem antes porque quem não sabe que vai esperar 40 minutos acha que a skill emperrou.

### Os 7 passos do pipeline

```
[Vídeo]
  → [1] áudio           ffmpeg extrai o MP3 em 16kHz mono
  → [2] transcrição     o transcritor devolve o texto cru, em português
  → [3] limpeza         tira muleta de fala, preserva voz e exemplo
  → [4] capítulos       8 a 15, com título e resumo de uma frase   ← STOP
  → [5] enriquecimento  cada capítulo vira texto corrido com intro e fechamento
  → [6] render          apostila.md, e o index.html quando há arquivo
  → [7] publicação      host de site estático, só quando o dono pedir  ← STOP
```

1. **Áudio.** `ffmpeg -i aula.mp4 -vn -acodec libmp3lame -ar 16000 -ac 1 aula.mp3`. O `-vn` tira o vídeo, `-ar 16000` é a taxa que o transcritor quer, `-ac 1` força mono.
2. **Transcrição.** Rode o transcritor com o idioma cravado em português e o modelo médio como padrão. Saída: um `.txt` cru, sem capítulo, sem pontuação confiável. Os comandos exatos estão em `references/reference.md`.
3. **Limpeza.** Primeiro uma passada de expressão regular tirando as muletas óbvias, depois uma passada de modelo com o prompt da reference. O prompt manda preservar a voz, a primeira pessoa e os exemplos, e proíbe resumir. O que sai: pausa verbalizada, repetição de palavra, autocorreção. O que fica: tudo que é conteúdo.
4. **Capítulos.** O modelo lê o texto limpo e propõe de 8 a 15 capítulos, cada um com título de 5 a 9 palavras, a frase em que começa e um resumo de uma frase. Sai em uma lista estruturada. **STOP: mostre o índice ao dono e pergunte "esse é o mapa da aula; algum capítulo sobra, falta ou está no lugar errado?"**. **Antes do STOP, classifique cada título de capítulo como `rótulo` ou `tese`, numa coluna.** Rótulo nomeia o assunto e não afirma nada (`07. Resumo`, `03. Introdução`, `05. Perguntas`); tese afirma alguma coisa que o aluno pode discordar (`07. O que sobra quando você tira a pressa`). O título de capítulo é a primeira coisa que o aluno lê na barra lateral, e um sumário de rótulos não dá vontade de abrir capítulo nenhum. Cole a coluna inteira, um capítulo por linha, na forma `<título> | rótulo ou tese`, e **todo `rótulo` volta pro passo de escrita do título antes do STOP**. Feche com `capítulos: N · com título em tese: N · rótulos restantes: 0`. Enriquecer 12 capítulos mal cortados custa a rodada inteira; corrigir o índice custa uma mensagem.
5. **Enriquecimento.** Capítulo por capítulo, o trecho bruto vira prosa fluida com intro de 2 a 3 frases, exemplo prático onde for natural, e um parágrafo de fechamento. Lista, comando e código viram Markdown. **O piso de palavras é condicionado ao tamanho da fonte, e a conta vem antes da régua.** Conte as palavras da transcrição e escreva `transcrição: P palavras` antes de enriquecer. Com **mais de 3.000 palavras** na fonte, cada capítulo fica entre 800 e 2000: menos que isso fica raso, mais que isso cansa. Com **3.000 palavras ou menos**, o piso de 800 não se aplica e nem é meta: o critério passa a ser **fidelidade e cobertura**, ou seja, todo bloco da gravação virou capítulo e nenhuma frase da fonte ficou de fora sem motivo escrito. Nesse caso a checagem que reprova é a de cobertura, não a de volume: cole `blocos/marcas de tempo na fonte: N · cobertos em capítulo: N · descobertos: 0` e declare em 1 linha que o piso não se aplica por tamanho de fonte. Esticar capítulo pra alcançar 800 palavras com fonte curta reprova a entrega, porque o volume só pode vir de invenção. Se a gravação não sustentar o piso, **reduza o número de capítulos** fundindo blocos correlatos, e só então reavalie o tamanho. Se ainda assim não fechar, entregue os capítulos curtos e declare o motivo em 1 linha. **Nunca preencha o piso com material do perfil do dono, do avatar ou do negócio:** o capítulo cita apenas o que foi dito na gravação, e o piso cede antes do inviolável de não inventar. Checagem verificável antes de fechar: conte as palavras de cada capítulo e cole a lista `capítulo N: P palavras`; número declarado que não bate com a contagem reprova a entrega. **A apostila fala na voz de quem deu a aula, nunca na voz de quem resenha a aula.** O aluno assistiu; o material continua a mesma conversa, na primeira pessoa do dono. Terceira pessoa sobre o próprio material ("a aula apresenta", "o material mostra", "vale olhar", "é importante notar", "o princípio aqui é") transforma o capítulo em resenha e apaga o dono do próprio conteúdo. Antes de concatenar, rode e cole a saída:

```
grep -nE 'a aula apresenta|o material|vale olhar|é importante notar|o princípio' apostila.md
```

**A saída tem que voltar vazia.** Cada linha devolvida volta pro passo de escrita e é reescrita na voz do dono. E cada capítulo carrega no mínimo uma fala literal da gravação, entre aspas, com a marca de tempo no bloco `Origem`: capítulo sem fala literal é paráfrase, não apostila. Cole `capítulos: N · com fala literal citada: N`, e **os dois números têm que ser iguais**; diferença reprova a entrega.

**A última frase de cada capítulo passa pelo teste do nicho trocado sozinha.** É a que fica com o leitor, e é onde a prosa de manual se instala, porque o motor fecha o capítulo resumindo o que já foi dito. Liste as últimas frases numa coluna própria, uma por capítulo, na forma `cap N | <a frase copiada inteira> | sobrevive à troca de nicho? sim/não`. Um `sim` significa que a frase serviria em qualquer negócio e volta pro passo de escrita: o último lugar do capítulo pede a frase mais concreta que a gravação deu, a cena ou o número, e a mais geral não serve ali. Fecho que só resume o capítulo é fecho reprovado.

Concatene tudo em `apostila.md`, numerando os capítulos no título, e feche com um capítulo de Resumo em tópicos.
6. **Render.** Sem sistema de arquivo, para aqui e entrega o Markdown. Com sistema de arquivo, injeta o Markdown no template de arquivo único da reference e gera o `index.html`: índice fixo na lateral, área de leitura central, navegação por seta do teclado, índice que acompanha o scroll, botões de anterior e próximo, âncora por capítulo, e gaveta de menu no celular. Aplique aqui a cor e a fonte do dono; sem identidade dele, entregue neutro e diga em 1 linha que é provisório.
7. **Publicação.** Só quando o dono pedir. O padrão é um host de site estático com linha de comando (o comando de exemplo está na reference); qualquer host de arquivo estático serve, porque a apostila é um arquivo único sem build e sem dependência de servidor. **STOP antes de publicar: "publico agora, ou você quer revisar o material antes de ele ganhar link?"**. Material com link é material que circula, e circular é irreversível.

---

## Ação 2 · RENDER E PUBLICAÇÃO

**O que faz:** pega um `apostila.md` já escrito e aprovado e devolve o site.

**Precisa de:** o arquivo Markdown, com os capítulos em títulos de segundo nível · o título da apostila · a identidade visual, do perfil/brain do agente.

**Sem o insumo:** sem identidade, renderiza neutro e avisa em 1 linha. Sem os títulos de segundo nível marcando os capítulos, o índice sai vazio: nesse caso, mostre ao dono como o arquivo está estruturado e proponha a divisão antes de renderizar.

**"Navegável" se mede, e nunca se declara.** O `index.html` sai com índice no topo em que **cada capítulo é um `<a href="#cap-N">`** e cada capítulo abre com o `id` correspondente. Antes de entregar, rode `grep -c '<a href="#' index.html` e `grep -c 'id="cap' index.html`: os dois números têm que ser iguais ao de capítulos, com a saída colada no relato, na forma `capítulos: N · âncoras: N · alvos id: N`. Índice sem link, ou link sem alvo, reprova a entrega: uma apostila com um link para dez capítulos cumpre a palavra do pedido no papel e não no uso.

**HTML entregue é HTML que ABRE, e são quatro comandos, não uma promessa.** Um `index.html` com o template por renderizar entrega ao dono a chave `{{titulo}}` na tela, e markdown cru no corpo entrega os `##` que deviam ter virado título. Rode os quatro e cole as quatro saídas:

```
grep -c '{{' index.html
grep -cE '^#{1,6} ' index.html
grep -c '<a href="#' index.html
python3 -c "import html.parser,sys;p=html.parser.HTMLParser();p.feed(open('index.html',encoding='utf-8').read());print('parse ok')"
```

`{{` tem que dar **0**, `^#` no corpo tem que dar **0**, as âncoras têm que bater com o número de capítulos, e o parse tem que imprimir `parse ok`. Depois abra o arquivo num navegador sem tela (`python3 -m http.server` numa porta local mais o navegador em modo headless, ou o comando de headless que o ambiente tiver) e cole a saída literal. **Declarar "navegável", "índice que acompanha o scroll" ou "navegação por teclado" sem essas saídas coladas é afirmação sem prova, e o `--conferir` reprova o HTML com `{{` ou sem `<html>` e `</html>`.** Sem navegador no ambiente, diga isso em 1 linha e cole os três `grep` mesmo assim: eles não dependem de navegador.

**Entrega:** `index.html`, arquivo único, mais o link quando a publicação foi pedida e aprovada.

**O binário é lido de volta antes de fechar, e o `.md` de origem não responde por ele.** Quando a apostila também sair em `.pdf` ou `.pptx`, extraia o texto do arquivo gerado, cole `caracteres: N · linhas com acento: N` ao lado da mesma contagem sobre o `.md` de origem (`grep -c '[áéíóúâêôãõç]' apostila.md`) e rode o lint sobre o texto extraído: **zero acento num texto em português com mais de 200 caracteres, com a origem acentuada, reprova o arquivo**, porque a origem foi escrita sem acento pra fugir de encoding e ninguém abriu o resultado. O `python3 scripts/checar_titulos.py --conferir <pasta>` refaz as duas contagens e reprova sozinho com `deck sem acentos`.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/reference.md`, o bloco do template HTML e o bloco de injeção do Markdown.

**Passos:** confere a estrutura do Markdown → injeta no template → confere o render (a seção abaixo) → **STOP antes de publicar** → publica.

## Conferência do render (obrigatória antes de entregar o site)

1. Abra o `index.html` no navegador e confira, **item a item, a barra lateral contra os títulos do `.md`**: numeração duplicada ("01. 01."), âncora morta e item fora de ordem reprovam o render. **Cole a lista dos títulos como eles aparecem na tela**, não como estão no Markdown: é a comparação entre as duas listas que pega a numeração dobrada, que passa batido em qualquer conferência por amostra. Confira também: o índice lista todos os capítulos, na ordem · cada link do índice desce pro capítulo certo · o índice acompanha o scroll · a seta do teclado navega · nenhum bloco de código escapou e quebrou a página (é o erro mais comum, causado por crase dentro do conteúdo) · a leitura funciona na largura de celular, com a gaveta do menu abrindo.
2. Confira o conteúdo por amostra: abra 2 capítulos e leia o começo e o fim. Procure trecho que ficou em linguagem de transcrição ("então, é... o que eu falei ali atrás"), que é o sinal de que a limpeza passou raso naquele pedaço.
3. **Diga ao dono o que você conferiu**, em 2 a 4 linhas. Sem leitor de imagem ou sem navegador, confira o que dá no próprio arquivo (contagem de capítulos, presença de cada âncora, tamanho do arquivo) e declare em 1 linha que a conferência visual fica com ele.

## O que fazer sem X

| Falta | O que a skill faz |
|---|---|
| **Sem shell** | Não roda a extração de áudio nem a transcrição. Pede ao dono a transcrição (o próprio player do vídeo costuma ter legenda que dá pra copiar) e entra direto no passo 3. Entrega em Markdown. |
| **Sem transcritor instalado** | Mesma saída de cima: pede o texto e entra no passo 3. Nunca fique parado esperando uma instalação que o dono não pediu. |
| **Sem `ffmpeg`** | Se o arquivo já for áudio, o passo 1 é desnecessário. Se for vídeo, peça ao dono o áudio ou a transcrição. |
| **Sem sistema de arquivo** | Entrega `apostila.md` na tela, capítulo por capítulo. O site fica pendente e você diz isso em 1 linha. |
| **Sem host de publicação** | Entrega o `index.html` no disco e diz que ele funciona aberto direto no navegador, porque é arquivo único, e que dá pra publicar depois em qualquer host de arquivo estático. |
| **Sem identidade visual do dono** | Renderiza neutro e avisa em 1 linha que a cor é provisória. Nunca invente uma marca. |

## Gate de qualidade (roda antes de entregar)

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`references/regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória**, nestes 3 passos: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A linha de fechamento e a tabela de destino moram em `conferencia/checagem-titulos.md`, nunca dentro da apostila que o aluno lê:** a apostila é material de leitura, e a contagem de dados ou a tabela de veredito no meio dela é bastidor da máquina, que o `--conferir` reprova como `bastidor na peça pública`. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta em `conferencia/`, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Checagem sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.

**Número que o dono marcou como incerto nunca vira afirmação.** Antes de escrever qualquer capítulo, rode `grep -n 'A CONFIRMAR' <perfil do dono>` e liste os valores marcados. Cada um desses números só entra na apostila de três formas: com a ressalva colada na mesma frase ("cerca de", "no caso dela", "pelo que ela contou"), como pergunta aberta, ou fora. **Escrever o número como fato porque a transcrição o disse reprova o capítulo**, ainda que a transcrição seja a fonte, e a razão é simples: o dono já declarou que não confia no próprio número, e a transcrição é a fala dele com a mesma incerteza dentro. Vale também no resumo do fim e em toda repetição: um número marcado como incerto que aparece três vezes precisa da ressalva nas três. Checagem colada: `números marcados como incertos no perfil: N · afirmados sem ressalva na apostila: 0`.

**Teste da voz, colado (a apostila é lida sozinha, então a voz é metade do produto).** Antes de fechar, escolha 3 parágrafos ao acaso e reescreva cada um na fala do dono declarada no perfil, sem termo abstrato de ensaio (interrupção, experiência, processo, dimensão, aspecto, contexto, jornada). Cole as 3 versões lado a lado no handoff e fique com a que a pessoa da aula diria em voz alta. Se a versão original vencer nas 3, a apostila passa; se perder em qualquer uma, a apostila inteira volta pro passo de escrita, e não só o parágrafo perdedor, porque o registro é do texto todo. **A transcrição é a fonte do conteúdo e também a fonte do vocabulário:** palavra que não aparece na transcrição e não é termo técnico do método entra na apostila por escolha declarada, nunca por hábito. Checagem colada: `parágrafos testados: 3 · original venceu: N de 3`, e qualquer N menor que 3 reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.


| Check | Passa se |
|---|---|
| **Voz preservada** | o capítulo soa como o dono falando, na primeira pessoa, com os exemplos que ele deu |
| **Não resumiu** | a apostila é mais longa e mais organizada que a fala, nunca um resumo dela |
| **Nada inventado** | nenhum conceito, exemplo ou número que não estava na gravação foi acrescentado |
| **Fonte por marca de tempo** | 3 afirmações de conteúdo por capítulo estão apontadas contra a marca de tempo da transcrição que as sustenta; material que só existe no perfil do dono ficou fora do corpo |
| **Corpo sem comentário editorial** | nota de revisão, anonimização, decisão e pendência ficaram no handoff; o corpo que a aluna lê só ensina a aula |
| **`[A CONFIRMAR]`** | todo número, caso ou promessa que ele citou sem fonte está marcado |
| **Capítulos aprovados** | o índice passou pelo STOP do passo 4 antes do enriquecimento |
| **Tamanho de capítulo (piso condicionado à fonte)** | a contagem `transcrição: P palavras` está colada. Com fonte acima de 3.000 palavras, a lista `capítulo N: P palavras` bate com a contagem real e cada capítulo cai entre 800 e 2000; abaixo do piso só depois de fundir capítulos, com o motivo declarado em 1 linha. Com fonte de 3.000 palavras ou menos, **o piso não se aplica** e este check passa pela cobertura: `blocos na fonte: N · cobertos: N · descobertos: 0`, com a linha declarando que o piso caiu por tamanho de fonte. Capítulo esticado além do que a gravação diz reprova nos dois casos |
| **Resumo no fim** | existe um capítulo final de resumo em tópicos |
| **Render conferido** | a lista dos títulos como aparecem na tela está colada e conferida contra os títulos do `.md`: sem numeração duplicada, sem âncora morta, sem item fora de ordem. Índice, navegação e leitura no celular conferidos, ou o dono foi avisado de que não foram |
| **Anti-IA** | zero travessão longo e zero da família do verbo-freio banido pela régua anti-voz no texto escrito aqui. Com shell, rode o lint de copy das skills de conteúdo quando estiver instalado; sem shell, busca manual dos dois. A fala literal do dono entre aspas é exceção |
| **Conteúdo sensível** | nome de aluno, valor de contrato e dado pessoal que apareceram na gravação foram procurados e tirados antes de publicar |
| **VEREDITO** | é o pior item acima. Uma falha corrige e re-roda |

## Onde este material entra na operação

- **Isca ou material de captura:** uma aula gravada vira o material navegável no lugar do PDF engessado. A isca em si, o que ela promete e como capta, é da **soft-funil-isca**.
- **Bônus de um webinar ou de uma oferta:** material complementar gerado da própria gravação.
- **Micro-aula de um funil:** o treinamento curto entregue como apostila.
- **Entrega de mentoria ou de comunidade:** cada call vira material indexado, o que reduz a pergunta repetida e o cancelamento.

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. Se a skill indicada não estiver instalada, faço aqui em modo reduzido e digo em 1 linha o que ficou de fora.

- O **roteiro ou a ideia de conteúdo de feed** → **soft-conteudo-carrossel**, **soft-conteudo-reels**, **soft-conteudo-stories**.
- A **página de captura ou de venda** → **soft-funil-landing**.
- A **isca**, o que ela promete e como capta → **soft-funil-isca**.
- A **proposta comercial** → **soft-vendas-proposta**.
- A **edição do vídeo**, corte e legenda → **soft-editor-video**.
- O **deck de slides** e o PPTX → **soft-apresentacao**.
- A **arte, a capa e a identidade visual** → **soft-designer**.

## Recursos da pasta

- `references/regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta, leia antes de começar.
- `references/reference.md`: o método completo, com os comandos de cada etapa, os prompts de limpeza, segmentação e enriquecimento, o template HTML de arquivo único, o script de injeção, o caminho de publicação, as boas práticas, as variações e a tabela de erros comuns.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
