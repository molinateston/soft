# Criar curso, seção e aula

O trabalho do dia a dia. O dono fala "sobe esse vídeo no módulo 2" e o agente resolve em uma ou duas chamadas, porque o mapa da instância já tem os ids.

Todas as chamadas levam o mesmo cabeçalho de `setup-conexao.md`.

## Índice

- [Criar o curso](#criar-o-curso)
- [Pôr a descrição](#por-a-descricao)
- [Criar a seção](#criar-a-secao)
- [Aula de vídeo por link](#aula-de-video-por-link)
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

Aceita só `name`. A resposta traz `sectionId`. **Esse valor é o que vai no campo `groupId` da aula.** Guardar agora evita uma varredura depois.

Renomear: `PATCH /api/products/{{COURSE_ID}}/sections/{{SECTION_ID}}` com `{"name":"..."}`. Aceita `name` e `drip`.

## Aula de vídeo por link

O caminho do YouTube, do Vimeo e de qualquer incorporação. **Não use o tipo `video`**: aquele exige arquivo hospedado dentro do sistema e uma referência de mídia selada, que o agente não consegue produzir sozinho.

```bash
curl -s -X POST "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/lessons" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"title":"{{TITULO_DA_AULA}}","type":"embed","groupId":"{{SECTION_ID}}","content":{"value":"{{LINK_DO_VIDEO}}"},"published":true,"requiresEnrollment":true}'
```

Campos aceitos na criação: `title`, `type`, `content`, `media`, `downloadable`, `groupId`, `requiresEnrollment`, `published`.

Valores de `type`: `text`, `video`, `audio`, `pdf`, `file`, `embed`, `quiz`, `scorm`. Para link externo é sempre `embed`.

Sobre `content.value`: aceita o endereço do vídeo ou o bloco de incorporação inteiro que o site de vídeo oferece. O que estiver ali é o que o aluno vê no lugar do player. Valor vazio devolve erro de conteúdo nulo.

Sobre `requiresEnrollment`: `true` significa que só aluno matriculado vê. `false` deixa a aula aberta pra quem abrir o link, útil pra aula de amostra.

Sobre `published`: aula não publicada não aparece pro aluno mesmo em curso publicado. O dono quase sempre quer `true`.

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

Antes disso, confira os dois passos escondidos de `montar-escola.md`: nome do dono gravado e plano criado. Sem o nome, volta `Complete your profile to perform this action`. Sem plano, volta `Add a payment plan before performing this action`. As duas mensagens vêm em 422 e nenhuma delas explica ao dono o que fazer.

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

**Editar a aula:** `PATCH /api/products/{{COURSE_ID}}/lessons/{{LESSON_ID}}`, aceita `title`, `content`, `media`, `downloadable`, `requiresEnrollment`, `published`.

**O tipo não muda depois de criado.** Mandar `type` no PATCH é ignorado em silêncio, sem erro. Transformar aula de texto em aula de vídeo obriga apagar e criar de novo, e isso é ordem nomeada.

**Mover a aula de seção ou de posição:** `POST /api/products/{{COURSE_ID}}/lessons/{{LESSON_ID}}/move` com `{"destinationSectionId":"{{SECTION_ID}}","destinationIndex":0}`. O índice começa em zero.

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
| 422 seção não encontrada | O `groupId` não é de uma seção daquele curso | `Não achei esse módulo. Em qual deles você quer a aula?` |
| 422 perfil incompleto | Falta o nome do dono | Resolve por baixo com `montar-escola.md`, passo 1, e repete |
| 422 plano obrigatório | Falta o plano | Resolve por baixo com `montar-escola.md`, passo 3, e repete |
| 404 | O curso ou a aula não existe mais | `Esse curso sumiu do ar. Quer que eu crie de novo?` |

Erro que repete duas vezes vira aviso ao dono, com o que o agente tentou. Não existe terceira tentativa cega.
