# Criar curso, seção e aula

O trabalho do dia a dia. O dono fala "sobe esse vídeo no módulo 2" e o agente resolve em uma ou duas chamadas, porque o mapa da instância já tem os ids.

Todas as chamadas levam o mesmo cabeçalho de `setup-conexao.md`.

## Índice

- [Criar o curso](#criar-o-curso)
- [Pôr a descrição](#por-a-descricao)
- [Criar a seção](#criar-a-secao)
- [Capa e descrição do módulo](#capa-e-descricao-do-modulo)
- [Aula de vídeo por link](#aula-de-video-por-link)
- [Descrição, capítulos e duração da aula](#descricao-capitulos-e-duracao-da-aula)
- [Aula de texto](#aula-de-texto)
- [Publicar e tirar da vitrine](#publicar-e-tirar-da-vitrine)
- [Mudar de lugar, renomear, apagar](#mudar-de-lugar-renomear-apagar)
- [O que perguntar ao dono](#o-que-perguntar-ao-dono)
- [Quando der errado](#quando-der-errado)

## Criar o curso

```bash
curl -s -X POST "{{MEMBERS_URL}}/api/products" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"title":"{{TITULO}}","type":"course"}'
```

Aceita **só** `title` e `type`. Descrição, imagem e etiqueta são uma segunda chamada. A resposta traz `productId`: guarde esse valor no placeholder interno `COURSE_ID`.

## Pôr a descrição

A descrição não é texto solto. É um documento em JSON, e o sistema tenta interpretar o valor. Texto puro quebra e volta 422.

```bash
curl -s -X PATCH "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"description":"{\"type\":\"doc\",\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"O TEXTO DO DONO AQUI\"}]}]}"}'
```

Cada parágrafo novo é outro objeto `paragraph` dentro de `content`. Quebra de linha simples não existe nesse formato: parágrafo é a unidade.

Campos aceitos nesta rota: `title`, `slug`, `description`, `published`, `privacy`, `tags`, `featuredImage`.

## Criar a seção

Seção é o que o dono chama de módulo.

```bash
curl -s -X POST "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/sections" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"name":"{{NOME_DO_MODULO}}"}'
```

Aceita `name`, `description` e `cover`. A resposta traz `sectionId`. **Esse valor é o que vai no campo `groupId` da aula.** Guardar agora evita uma varredura depois.

Renomear: `PATCH /api/products/{{COURSE_ID}}/sections/{{SECTION_ID}}` com `{"name":"..."}`. Aceita `name`, `drip`, `description` e `cover`.

Ler as seções do curso, com nome, `sectionId` e `lessonsOrder` de cada uma:

```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/sections"
```

**O módulo se reconhece pelo `sectionId`, nunca pelo nome.** O dono renomeia módulo pelo painel sem avisar o agente. Quem procura a seção pelo nome antigo, não acha e cria outra, duplica o módulo inteiro. Em 23/09 isso gerou 13 seções duplicadas numa escola. Antes de criar seção, leia a lista acima e compare pelo `sectionId` guardado no mapa da instância. Nome diferente com o mesmo id é renomeação: o módulo continua lá. Na dúvida, pergunte ao dono: `O módulo X virou Y, ou é um módulo novo?`

## Capa e descrição do módulo

No início do curso, o aluno vê cada módulo como um cartão, com capa e uma linha de promessa. Os dois campos entram na criação da seção ou num PATCH depois.

- `description`: texto de até 300 caracteres. Uma frase do que o aluno sai sabendo do módulo.
- `cover`: `{"mediaId":"..."}`, o mesmo esquema do `featuredImage` do curso. Primeiro envie a imagem pela rota de mídia (`personalizar.md`, bloco "Enviar imagem no modo local") e use o `mediaId` que voltou. URL no lugar do `mediaId` não serve.

```bash
curl -s -X PATCH "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/sections/{{SECTION_ID}}" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"description":"{{PROMESSA_DO_MODULO}}","cover":{"mediaId":"{{MEDIA_ID}}"}}'
```

`null` em qualquer um dos dois apaga o valor guardado. Texto acima de 300 caracteres ou `cover` sem `mediaId` volta 422 com o motivo. A capa está pronta quando a leitura das seções devolve `cover.mediaId` igual ao enviado.

## Aula de vídeo por link

O caminho do YouTube, do Vimeo e de qualquer incorporação. **Não use o tipo `video`**: aquele exige arquivo hospedado dentro do sistema e uma referência de mídia selada, que o agente não consegue produzir sozinho.

```bash
curl -s -X POST "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/lessons" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"title":"{{TITULO_DA_AULA}}","type":"embed","groupId":"{{SECTION_ID}}","content":{"value":"{{LINK_DO_VIDEO}}"},"published":true,"requiresEnrollment":true}'
```

Campos aceitos na criação: `title`, `type`, `content`, `media`, `downloadable`, `groupId`, `requiresEnrollment`, `published`, `description`, `chapters`, `durationSeconds`. Os três últimos estão em [Descrição, capítulos e duração da aula](#descricao-capitulos-e-duracao-da-aula).

Valores de `type` que o agente usa: `embed`, `text` e `quiz`. São os três que a tela de criar aula mostra ao dono, como Vídeo, Texto e Quiz. Para vídeo é sempre `embed`.

Os valores `video`, `audio`, `pdf`, `file` e `scorm` saíram da tela. Eles pedem envio de arquivo, e esta instalação guarda só imagem, até 10 MB. A API ainda aceita esses valores, e a aula criada com eles não funciona pro aluno. O agente não usa nenhum deles.

Sobre `content.value`: aceita o endereço do vídeo ou o bloco de incorporação inteiro que o site de vídeo oferece. O que estiver ali é o que o aluno vê no lugar do player. Aula de vídeo não aceita `content.value` vazio: volta 422 com `O conteúdo não pode ficar vazio`. Sem o link na mão, não crie a aula ainda. Crie quando o link chegar.

**Para YouTube, grave sempre o link puro**, no formato `https://www.youtube.com/watch?v=ID` ou `https://youtu.be/ID`. O link puro cai no player próprio e limpo, em instalação nova e em instalação antiga. O código de incorporação do YouTube também funciona depois da atualização de 21/09, e antes dela ele escapava para um quadro cru com a marca do YouTube à mostra. Por isso o link puro é a forma segura. O vídeo do YouTube precisa estar como não listado.

Bloco de incorporação inteiro só para as outras hospedagens: Panda, Vimeo, Bunny.

**Página inteira dentro de uma aula, desde a versão de 24/09.** Para embutir um guia ou página externa (como a página de instalação do produto do dono), crie uma aula `embed` com um iframe marcado com `data-altura="tela"`: `<iframe src="https://..." data-altura="tela" title="..."></iframe>`. Ela aparece na largura toda, na altura da tela, rolando por dentro, sem moldura de vídeo. Confira antes que a página aceita ser embutida: `curl -sI <endereço>` não pode trazer `X-Frame-Options` nem `frame-ancestors` que barrem. Para pôr essa aula no menu, grave o caminho dela nos links extras do menu.

**Capa de cada aula, desde a versão de 24/09.** Suba a imagem pela API de mídia (16:9, até 1280x720 em `.webp` fica leve) e ligue na aula com `PATCH /api/products/{{COURSE_ID}}/lessons/{{LESSON_ID}}` e o corpo `{"cover":{"mediaId":"<mediaId>"}}`. `{"cover":null}` tira. A imagem precisa ser da própria escola, senão volta 422. Sem capa, a aula usa a imagem do vídeo. Capa gerada por IA sai melhor sem texto dentro da imagem: o título da aula já aparece embaixo dela.

**Vídeo sem YouTube, desde a versão de 23/09.** Se o dono hospeda o vídeo como arquivo, grave no `content.value` o endereço direto do arquivo, `https://` terminando em `.mp4` ou `.webm`. A aula toca no mesmo player limpo, sem marca de ninguém por cima. Servem hospedagens que entregam o arquivo com pulo de ponto (resposta 206 a um pedido com `Range`), o que se confere com `curl -s -o /dev/null -w '%{http_code}' -r 0-99 <endereço>`. A mídia do HighLevel e das plataformas feitas sobre ele já converte o vídeo em 360p a 1080p: grave o endereço `transcoded_videos/cts-<código>_1080p.mp4`, e o player usa sozinho a capa `<código>.jpg` e o 720p no celular. Quem tiver o endereço direto abre o vídeo, do mesmo jeito que um vídeo não listado do YouTube. Diga isso ao dono antes de trocar.

**Teste de "o vídeo toca" feito da VPS não prova nada** para vídeo do YouTube. O YouTube bloqueia a reprodução pedida de IP de servidor e devolve o erro 150 do player. Medido em 23/09 com qualquer vídeo, inclusive o de demonstração do próprio YouTube. Quando o YouTube devolve erro, o player limpo cai num quadro cru do YouTube. Quem prova a aula é o dono, abrindo no aparelho dele. O agente confere pela API que a aula existe, está publicada e tem o link certo, e pede ao dono: `Abre a aula no seu celular e me diz se o vídeo toca?`

Sobre `requiresEnrollment`: `true` significa que só aluno matriculado vê. `false` deixa a aula aberta pra quem abrir o link, útil pra aula de amostra.

Sobre `published`: aula não publicada não aparece pro aluno mesmo em curso publicado. O dono quase sempre quer `true`.

## Descrição, capítulos e duração da aula

Três campos opcionais que mudam a tela do aluno. Entram no POST de criação ou num PATCH depois.

| Campo | Formato | Limite | O que o aluno vê |
|---|---|---|---|
| `description` | texto em markdown | até 20.000 caracteres | painel ao lado do vídeo com a descrição da aula |
| `chapters` | lista de `{start, title, summary}` | até 60 capítulos | capítulos clicáveis que pulam o vídeo pro ponto marcado |
| `durationSeconds` | inteiro de segundos, zero ou mais | sem teto | duração da aula no menu do curso |

Regras de cada capítulo:

- `start`: segundo do vídeo onde o capítulo começa, zero ou mais. `754` é 12min34s.
- `title`: texto não vazio, até 120 caracteres.
- `summary`: opcional, até 400 caracteres.
- Nenhum outro campo dentro do capítulo. Campo a mais volta 422.
- A ordem da lista não importa. O servidor guarda por `start`.

Exemplo de PATCH completo:

```bash
curl -s -X PATCH "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/lessons/{{LESSON_ID}}" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"durationSeconds":1265,"description":"Nesta aula você monta a massa base.\n\n**Material:** farinha, água e sal.","chapters":[{"start":0,"title":"Abertura","summary":"O que sai pronto desta aula."},{"start":95,"title":"Ponto da massa"},{"start":754,"title":"Descanso e corte","summary":"Quanto tempo esperar e como cortar sem rasgar."}]}'
```

`null` em qualquer um dos três apaga o valor guardado. Valor fora do formato volta 422 com o motivo em texto, por exemplo `Capitulo 2: title precisa ser um texto nao vazio.` O agente conserta pelo motivo e repete uma vez.

**Passo recomendado depois de cada vídeo.** Com a aula de vídeo criada, preencha `durationSeconds`, `description` e `chapters`. A aula com capítulos e descrição fica navegável, e o aluno acha o trecho que procura sem arrastar a barra. De onde vêm os dados:

- Duração: pergunte ao dono ou leia da página do vídeo, se ele mandar. Não chute.
- Capítulos: se o dono tiver a transcrição do vídeo, ou se a máquina do agente tiver ferramenta de transcrição, o agente propõe os capítulos a partir dela, com minuto e título, e mostra ao dono antes de gravar. Sem transcrição, pergunte: `Quer que eu marque os capítulos dessa aula? Me manda os minutos e o assunto de cada trecho.`
- Descrição: um resumo curto do que a aula entrega, no texto do dono ou aprovado por ele.

A instalação da área de membros não transcreve vídeo. O agente não promete capítulo automático.

## Aula de texto

```bash
curl -s -X POST "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/lessons" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"title":"{{TITULO}}","type":"text","groupId":"{{SECTION_ID}}","content":{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"O TEXTO AQUI"}]}]},"published":true,"requiresEnrollment":true}'
```

Aqui o `content` é o objeto de documento direto, não a string do curso. As duas formas convivem no sistema e trocar uma pela outra devolve erro de conteúdo.

## Publicar e tirar da vitrine

Publicar é o que faz o curso existir pro aluno.

```bash
curl -s -X PATCH "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"published":true}'
```

Antes disso, confira os dois passos escondidos de `montar-escola.md`: nome do dono gravado e plano criado. Sem o nome, volta `Preencha seu nome no perfil antes de publicar`. Sem plano, volta `Crie um plano para o curso antes de publicar (pode ser gratuito)`. As duas vêm em 422 e já dizem o conserto.

Em instalação anterior à atualização de 21/09 as mesmas falhas voltam em inglês, como `Complete your profile to perform this action` e `Add a payment plan before performing this action`. O agente reconhece o 422 no momento de publicar e não depende do texto para saber o que fazer.

Tirar da vitrine sem fechar pra quem já tem acesso:

```bash
curl -s -X PATCH "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"privacy":"unlisted"}'
```

Valores de `privacy`: `public` aparece na vitrine da escola, `unlisted` só entra por link direto. Curso de turma fechada costuma ser `unlisted`.

Despublicar de vez, com `{"published":false}`, fecha o curso pra todo mundo, inclusive pra quem já pagou. É ordem nomeada: o dono precisa dizer o nome do curso.

## Mudar de lugar, renomear, apagar

**Editar a aula:** `PATCH /api/products/{{COURSE_ID}}/lessons/{{LESSON_ID}}`, aceita `title`, `content`, `media`, `downloadable`, `requiresEnrollment`, `published`, `description`, `chapters`, `durationSeconds`.

**O tipo não muda depois de criado.** O PATCH recusa `type` com 400 (`Unsupported lesson field: type`). Aula de vídeo nasce `embed`. Errou o tipo, apaga e recria, e apagar é ordem nomeada.

**Mover a aula de seção ou de posição:** `POST /api/products/{{COURSE_ID}}/lessons/{{LESSON_ID}}/move` com `{"destinationSectionId":"{{SECTION_ID}}","destinationIndex":0}`. O índice começa em zero.

**A posição conta aulas fantasmas.** A lista `lessonsOrder` da seção pode guardar ids de aulas já apagadas, e `destinationIndex` é contado sobre essa lista. Para pôr a aula no fim, leia as seções do curso e use o tamanho de `lessonsOrder` da seção de destino como índice. A contagem de aulas vivas dá posição errada. Para uma posição no meio, ache na `lessonsOrder` o índice da aula vizinha e use esse número.

**Apagar aula, seção ou curso:** existe `DELETE` nas três rotas. Nenhuma roda sem ordem nomeada do dono. Apagar curso apaga junto o acesso de todos os alunos dele, e não tem volta.

## O que perguntar ao dono

Uma pergunta por vez, sempre em linguagem de gente.

| Falta saber | Pergunta |
|---|---|
| O título da aula | `Que nome você quer nessa aula?` |
| Em qual módulo | `Essa aula entra em qual módulo? Hoje você tem: A, B e C.` |
| O link do vídeo | `Me manda o link do vídeo, do jeito que aparece na barra do navegador.` |
| Se libera já | `Solto essa aula pros alunos agora, ou deixo guardada?` |
| Qual curso, quando há vários | `Em qual curso? Você tem: X e Y.` |

Nunca pergunte por id, por tipo, por campo. Ofereça a lista de nomes e traduza para id por dentro.

## Quando der errado

| Resposta | O que é de verdade | Frase pro dono |
|---|---|---|
| 400 com nome de campo | O agente mandou campo fora da lista | (não fala com o dono, conserta o corpo e repete uma vez) |
| 422 conteúdo nulo | O `content` veio vazio ou no formato da outra família | `O vídeo não entrou. Me manda o link de novo?` |
| 422 conteúdo vazio na aula de vídeo | `content.value` foi vazio | `Me manda o link do vídeo que eu crio a aula.` |
| 400 `Unsupported lesson field: type` | Tentou trocar o tipo no PATCH | (não fala com o dono, o tipo não muda: apaga e recria com ordem nomeada) |
| 422 em capítulo, descrição ou duração | Valor fora do formato ou acima do limite | (não fala com o dono, conserta pelo motivo e repete uma vez) |
| 422 seção não encontrada | O `groupId` não é de uma seção daquele curso | `Não achei esse módulo. Em qual deles você quer a aula?` |
| 422 perfil incompleto | Falta o nome do dono | Resolve por baixo com `montar-escola.md`, passo 1, e repete |
| 422 plano obrigatório | Falta o plano | Resolve por baixo com `montar-escola.md`, passo 3, e repete |
| 404 | O curso ou a aula não existe mais | `Esse curso sumiu do ar. Quer que eu crie de novo?` |

Erro que repete duas vezes vira aviso ao dono, com o que o agente tentou. Não existe terceira tentativa cega.
