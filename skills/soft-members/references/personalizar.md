# Personalizar a escola

A instalação padrão guarda imagens na própria VPS. Logo, capa de curso e imagem em aula não dependem de uma conta de mídia externa. Nome, subtítulo, cor e logo da escola continuam no painel porque a API pública não expõe a configuração global.

## O que dá por cada caminho

| Pedido | Caminho |
|---|---|
| Nome e subtítulo da escola | Painel, em `Settings` |
| Cor do tema | Painel, na aba de tema |
| Logo da escola | Painel, usando o envio local de imagem |
| Capa de curso | API de mídia e atualização do curso |
| Imagem dentro de aula de texto | API de mídia e documento da aula |
| Título, descrição, módulos e privacidade | API do curso |

Quando o dono pedir nome, cor ou logo, diga:

> Essa parte fica na configuração visual da escola. Eu te guio por três cliques no painel e o restante do curso continuo fazendo por aqui.

O caminho curto é:

1. Abra `{{MEMBERS_URL}}/dashboard/settings`.
2. Entre em `Branding` para nome, subtítulo e logo, ou em `Theme` para as cores.
3. Salve e abra uma página de aluno para conferir o resultado.

## Conferir o armazenamento antes de receber arquivo

```bash
curl -sS -X POST \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/media/presigned"
```

Na instalação padrão, a resposta é `200` com:

```json
{"mode":"local","uploadUrl":"/api/media/upload"}
```

Uma instalação ligada ao MediaLit responde com `signature` e `endpoint`. Os dois modos são válidos. `401` pede correção da chave. `403` significa que o dono ligado à chave não tem permissão de mídia. `405` significa que o agente usou GET no lugar de POST.

## Enviar imagem no modo local

Aceita JPEG, PNG, WebP, GIF e AVIF, até 10 MB por padrão. Não defina `Content-Type` à mão, porque o `curl` monta o limite do formulário.

```bash
curl -sS -X POST \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -F "file=@<arquivo>" \
  -F "access=public" \
  -F "caption=<texto alternativo>" \
  "{{MEMBERS_URL}}/api/media/upload"
```

Só confirme o envio quando a resposta vier `201`. Guarde o objeto devolvido, principalmente `mediaId`, `file`, `mimeType` e `originalFileName`. O arquivo fica no volume `media_data`, que precisa entrar na política de cópia da VPS junto com o banco.

Respostas que encerram a tentativa:

| Código | Leitura |
|---|---|
| 400 | formulário sem arquivo válido |
| 401 | chave inválida |
| 403 | dono sem permissão de mídia |
| 413 | arquivo acima do limite |
| 415 | formato ou assinatura do arquivo inválida |

## Usar a imagem como capa do curso

Depois do envio, atualize o curso com o `mediaId` devolvido:

```bash
curl -sS -X PATCH \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"featuredImage":{"mediaId":"<mediaId>"}}' \
  "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}"
```

A capa só está pronta quando o PATCH voltar `200` e a leitura do curso devolver `featuredImage.mediaId` igual ao enviado. Não passe uma URL no campo de capa.

## Perguntas ao dono

Pergunte uma coisa por vez:

- `Qual nome e subtítulo você quer no topo da escola?`
- `Qual é a cor principal da sua marca?`
- `Me manda a logo em PNG ou WebP, de preferência com fundo transparente.`
- `Me manda a capa do curso e o texto curto que descreve a imagem.`

O agente não escolhe identidade visual sem autorização. Ele recebe a escolha, aplica pelo caminho disponível e confere na tela do aluno.
