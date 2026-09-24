# Personalizar a escola

A instalação padrão guarda imagens na própria VPS. Logo, capa de curso e imagem em aula não dependem de uma conta de mídia externa. Nome, subtítulo, cor e logo da escola continuam no painel porque a API pública não expõe a configuração global.

## O que dá por cada caminho

| Pedido | Caminho |
|---|---|
| Nome e subtítulo da escola | Painel, na aba Configurações |
| Cor do tema | Painel, na aba de tema |
| Logo da escola | Painel, usando o envio local de imagem |
| Capa de curso | API de mídia e atualização do curso |
| Capa e linha de promessa do módulo | API de mídia e atualização da seção, em `criar-curso.md` |
| Imagens padrão da tela de entrada | Arquivos da instalação, fora da API |
| Imagem dentro de aula de texto | API de mídia e documento da aula |
| Título, descrição, módulos e privacidade | API do curso |
| Link da comunidade e link do suporte (menu do aluno) | Painel, em Configurações, campos "Link da comunidade" e "Link do suporte". Aceita `https://` (abre em outra aba) ou caminho interno como `/course/...` (abre na mesma aba, por exemplo a aula que explica a comunidade) |
| Links extras do menu do aluno (até 6, como "Instalação") | Painel, em Configurações, lista de rótulo e endereço; ou a mutação `updateSiteInfo(siteData: { navLinks: [{ label, url }] })`. Cada chamada troca a lista inteira |
| Destaque da semana (banner grande do início) | `PATCH /api/products/<id>` com `{"highlightLessonIds":["<lessonId>", ...]}`, até 5 aulas do curso, na ordem de exibição; `[]` volta ao automático |
| Capa de cada aula (imagem da aula nas faixas) | API de mídia e `PATCH` da aula com `{"cover":{"mediaId":"..."}}`, em `criar-curso.md` |
| Produto trancado com botão de compra | `PATCH /api/products/<id>` com `{"saleUrl":"https://checkout.exemplo.com/oferta"}`, em `vender-pelo-checkout.md` |

Quando o dono pedir nome, cor ou logo, diga:

> Essa parte fica na configuração visual da escola. Eu te guio por três cliques no painel e o restante do curso continuo fazendo por aqui.

O caminho curto é:

1. Abra `{{MEMBERS_URL}}/dashboard/settings`.
2. Entre em Configurações para nome, subtítulo, logo e cores.
3. Salve e abra uma página de aluno para conferir o resultado.

## O que o aluno vê

Desde 23/09 a escola tem visual novo:

- **Entrada dividida.** De um lado a imagem, do outro o cartão de login. O título grande é o nome do site e a linha de promessa é o subtítulo, os dois de Configurações. Trocar o texto da entrada é trocar nome e subtítulo no painel.
- **Início do curso, estilo streaming (desde 24/09).** Banner grande no topo, no molde da Netflix: imagem da capa da aula de ponta a ponta, título grande, resumo tirado da descrição da aula e os botões Assistir e Mais informações. Ele gira entre os destaques da semana escolhidos pelo dono a cada 8 segundos; sem escolha, entra a aula que o aluno tem pela frente. Em aula de vídeo próprio convertido, depois de 2,5 segundos entra um trecho mudo do vídeo, como um trailer (nunca com som, e nunca em celular, economia de dados ou movimento reduzido). Abaixo, cartão "Primeiros passos" (primeira aula, entrar na comunidade, concluir o primeiro módulo, marcados sozinhos e que o aluno pode ocultar) e cada módulo numa faixa horizontal, com uma imagem por aula e o título por cima dela; no computador a faixa também é arrastada com o mouse. A imagem da aula é, nesta ordem: a capa da aula, a capa do vídeo próprio, a miniatura do YouTube, a capa do módulo. Módulo sem aula publicada aparece com o selo "Em breve".
- **Aluno com um curso só entra direto no início desse curso**, sem passar pela lista "Meu conteúdo".
- **Tela da aula larga.** O vídeo ocupa a largura disponível até 1680 px, com o menu do curso ao lado, sem passar da altura da tela. Em aula de vídeo próprio, o botão "Janela flutuante" solta o vídeo por cima das outras janelas, e no Chrome ele pode flutuar sozinho quando o aluno troca de aba.
- **Menu do aluno** com Início, Comunidade e Suporte. Comunidade e Suporte só aparecem se os links estiverem gravados em Configurações, e também ficam no topo da página do curso (no celular, como ícones).
- **Faixas trancadas no fim:** todo curso publicado da escola que o aluno não tem e que tem link de venda aparece em preto e branco com cadeado e o botão "Quero acesso".
- **Tela da aula.** Menu por blocos, um por módulo, com a duração de cada aula, capítulos clicáveis embaixo do vídeo e painel com a descrição.

As imagens padrão da entrada ficam na instalação em `apps/web/public/membros/entrada-retrato.webp` e `apps/web/public/membros/entrada-rede.webp`. A troca é por arquivo com esses mesmos nomes, no servidor. A API não mexe nelas.

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

Aceita JPEG, PNG, WebP, GIF e AVIF, até 10 MB por padrão. Não defina o `Content-Type` do cabeçalho à mão, porque o `curl` monta o limite do formulário.

**Declare o tipo da imagem no próprio campo do arquivo**, com `;type=`. O servidor confere o tipo que o `curl` declara, e o `curl` nem sempre reconhece a extensão. Com `.webp` sem `;type=image/webp`, a resposta é 415 `Unsupported image type` (medido em 23/09). Use sempre o par certo:

| Extensão | Campo |
|---|---|
| `.webp` | `-F "file=@capa.webp;type=image/webp"` |
| `.png` | `-F "file=@capa.png;type=image/png"` |
| `.jpg` ou `.jpeg` | `-F "file=@capa.jpg;type=image/jpeg"` |
| `.gif` | `-F "file=@capa.gif;type=image/gif"` |
| `.avif` | `-F "file=@capa.avif;type=image/avif"` |

```bash
curl -sS -X POST \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -F "file=@<arquivo>;type=<tipo da tabela>" \
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
| 415 `Unsupported image type` | tipo não declarado ou fora da lista. Confira o `;type=` do campo e repita uma vez |
| 415 `Invalid image file` | o conteúdo do arquivo não bate com o tipo declarado |

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

O mesmo `mediaId` serve de capa do módulo, no campo `cover` da seção. O passo a passo está em `criar-curso.md`, bloco "Capa e descrição do módulo".

## Perguntas ao dono

Pergunte uma coisa por vez:

- `Qual nome e subtítulo você quer no topo da escola?`
- `Qual é a cor principal da sua marca?`
- `Me manda a logo em PNG ou WebP, de preferência com fundo transparente.`
- `Me manda a capa do curso e o texto curto que descreve a imagem.`

O agente não escolhe identidade visual sem autorização. Ele recebe a escolha, aplica pelo caminho disponível e confere na tela do aluno.
