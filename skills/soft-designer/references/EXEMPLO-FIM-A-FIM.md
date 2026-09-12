# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, marca, cores, números e resultados foram inventados só pra
> mostrar a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega
> de verdade. Num trabalho real, todo número e toda prova sem fonte nascem marcados `[A CONFIRMAR]`
> e o dono confirma antes de sair.

**O caso fictício:** uma escola de idiomas de bairro, com 4 professores, que vende curso de inglês
pra adulto que já tentou aprender três vezes e desistiu. Dona fictícia: professora que virou
empresária. Público: adulto de 30 a 50 anos que emperra na hora de falar. Identidade visual fictícia
dela: fundo creme, texto grafite, um accent azul-petróleo, tipografia sans.

Este arquivo mostra a saída resumida das 5 ações, na ordem. Cada saída real é bem maior; aqui está
só o suficiente pra você reconhecer o formato antes de começar.

---

## Ação 1 · BANNER, o criativo do anúncio

**O que o dono deu:** "faz o banner do anúncio da turma nova, começa dia 10".

**O que a skill perguntou (3 perguntas, de uma vez):**
1. O que esse anúncio promete em uma frase?
2. Pra onde a pessoa vai quando clica?
3. Qual formato a plataforma pede?

**O que ele respondeu:** promete falar inglês em reunião sem congelar · vai pra uma página de
inscrição da turma · formato quadrado, feed.

**A copy-visual escrita aqui, depois do gate:**

- Headline: "Você entende tudo em inglês e emperra na hora de responder."
- Copy-curta de apoio: "Turma nova, 12 vagas, começa dia 10."
- CTA visual: "Ver as vagas"

O gate cortou a primeira versão da headline ("Domine o inglês de uma vez por todas") por não passar
nas 3 perguntas: não dá pra ver a cena, não é falsificável, qualquer escola diria. A versão que
ficou nasceu do verbatim "eu entendo tudo, mas na hora de falar minha cabeça apaga".

**Preview, e o STOP:** a skill mostrou o `preview.html` e perguntou "o que ajusto antes de eu
exportar?". O dono pediu o número de vagas maior.

**Conferência do render (Passo D), com leitor de imagem:**

> Abri o `banner-turma-out.png`. A headline lê limpa em duas linhas, sem palavra sozinha na última.
> O bloco de vagas estava a 60px da borda de baixo, abaixo do padding de 100px: subi. O accent
> azul-petróleo contra o creme deu contraste suficiente no texto grande, mas não no CTA pequeno:
> escureci o azul do botão. Reduzi mentalmente a peça a miniatura e a headline continua legível.
> Re-renderizei e conferi de novo: passou limpo.

**Entrega:** `banner-turma-out.png` mais `preview.html`, no diretório de saída.

---

## Ação 2 · CARROSSEL, os PNGs

**O que o dono deu:** a copy de 8 cards, já aprovada, colada em markdown.

**Funções detectadas e declaradas antes de desenhar:**

| Card | Função |
|---|---|
| 1 | hook |
| 2 | problema |
| 3 | problema (aprofunda) |
| 4 | virada |
| 5 | método |
| 6 | método (passo 2) |
| 7 | prova |
| 8 | CTA |

O dono corrigiu uma: o card 7 não era prova, era objeção. A skill trocou o layout daquele card antes
de gerar o HTML, o que teria custado uma rodada inteira de retrabalho se a lista não fosse declarada.

**Ritmo aplicado:** os cards 2, 3 e 4 vinham no mesmo molde de título mais corpo. O card 4, que é a
virada, virou afirmação pura em tela quase vazia. O card 7 virou pergunta e resposta curta.

**Conferência do render (Passo D), com leitor de imagem:**

> Abri os 8 PNGs e o mosaico. Card 3: a palavra "sozinho" ficou sozinha na última linha, puxei uma
> palavra da linha anterior. Card 5: o número 12 encostava no rótulo, abri 24px entre os dois.
> Card 8: o botão do CTA estava com texto claro sobre creme, contraste insuficiente, escureci.
> Os outros 5 passaram limpos. Seta de arraste presente nos cards 1 a 7, ausente no 8, como manda a
> régua. Re-renderizei os três corrigidos e conferi de novo.

**Entrega:** `slide_01.png` a `slide_08.png`, mais `preview.html`.

---

## Ação 3 · SLIDES, o deck 16:9

**O que o dono deu:** "monta o deck da aula aberta que eu vou dar pros pais dos alunos".

**O que a skill perguntou (3 perguntas):** qual o argumento em uma frase · quantos slides ou quanto
tempo de fala · é guiada pela fala ou feita pra ler sozinha.

**Resposta:** argumento é que criança que aprende com adulto que emperra herda o freio · 20
minutos de fala · guiada pela fala, com ela em cena.

**Decisão de densidade:** guiada pela fala, então uma ideia por slide, headline grande, no máximo 3
pontos, e a área da câmera reservada no canto inferior direito em todos os slides.

**Amostra de 3 slides:**

| Slide | Título na tela | Conteúdo na tela |
|---|---|---|
| 1 | Seu filho aprende o que você faz, não o que você paga. | (tela quase vazia, só a frase) |
| 6 | O freio tem três causas, e nenhuma é falta de vocabulário. | 3 linhas, uma por causa |
| 11 | A turma de sábado abre com 12 vagas. | número 12 dominante, uma linha embaixo |

**Conferência do render (Passo D), com leitor de imagem:**

> Abri o mosaico dos 14 PNGs. A área da câmera está reservada e vazia nos 14, nenhum texto invade.
> Slide 6 tinha as 3 linhas apertadas contra o rodapé: reduzi a headline em um degrau da escala e
> respirei o bloco. Slide 11: o número 12 estava com o mesmo peso do texto embaixo, engrossei o
> número. Abri em tamanho cheio os slides 6 e 9, que pareciam densos: passaram depois do ajuste.

**Entrega:** `deck.html` navegável mais `slide_01.png` a `slide_14.png`.

---

## Ação 4 · PÁGINA, o HTML

**O que o dono deu:** a copy da página de inscrição, bloco a bloco, escrita antes.

**O que a skill perguntou:** o destino do botão. Ele ainda não tinha o link do formulário, então o
`href` saiu marcado `[A CONFIRMAR]` no HTML e a skill avisou em 1 linha.

**Blocos vestidos:** hero com a promessa e o botão · três blocos de objeção · bloco de como funciona
em 3 passos · bloco de vagas e data · botão final.

**Conferência do render (Passo D), com leitor de imagem:**

> Abri a página em largura de celular (390px) e em largura de monitor (1440px). No celular o hero
> empurrava o botão pra fora da primeira dobra: reduzi a headline e o botão subiu. Nos três blocos
> de objeção o texto passou de 75 caracteres por linha no monitor, o que cansa: limitei a largura
> do container. Contraste do grafite sobre o creme passou nos dois tamanhos. Nenhuma sobreposição.

**Entrega:** `pagina-turma-out.html`, arquivo único, CSS embutido, sem build.

---

## Ação 5 · CAPA, a thumbnail

**O que o dono deu:** "faz a capa do vídeo que eu gravei sobre o medo de falar".

**Pergunta única:** qual a frase que essa capa precisa entregar, e onde ela aparece? Resposta: "o
medo não é de errar, é de ser corrigido na frente dos outros", e é thumbnail de vídeo.

**Copy-visual da capa:** "O medo não é de errar." (a segunda metade da tese fica pro vídeo, porque
capa carrega UMA ideia)

**Formato:** 1280x720, porque o destino é thumbnail de vídeo.

**Conferência do render (Passo D), SEM leitor de imagem** (aqui o exemplo mostra o outro caminho):

> Não tenho leitor de imagem neste ambiente. Conferi por medida: rodei o `craft.py audit` no
> preview, que aprovou o contraste (grafite sobre creme, muito acima do mínimo) e não sinalizou
> órfã. A headline tem 24 caracteres, dentro da faixa da escala de densidade pra título dominante.
> O padding de 100px está declarado nos 4 lados. O PNG saiu com 1280x720 e 214 KB, ou seja, não é
> render vazio. A conferência visual de corte e sobreposição fica com você antes de publicar.

**Entrega:** `capa-medo-falar.png` mais `preview.html`.

---

## O que este exemplo prova sobre o fluxo

1. As 3 perguntas da ação substituem uma entrevista longa e não emperram nada: quem responde em uma
   linha já libera o desenho.
2. Declarar a lista de funções antes de desenhar o carrossel foi o que evitou refazer 8 cards.
3. A conferência do render encontrou problema em TODAS as 5 ações. Peça que ninguém olhou é peça que
   ninguém sabe se está certa.
4. Quando não dá pra ver a imagem, a skill não finge que viu: confere o que dá por medida e declara
   em 1 linha o que ficou por conferir.
