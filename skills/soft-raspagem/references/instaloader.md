# Instaloader: referência completa por caso de uso

> **AVISO DE RISCO. Leia para o dono antes de qualquer coisa.**
> **Conta usada para coleta automática pode ser limitada ou bloqueada pelo Instagram.**
> **Só conta secundária. Nunca a conta principal, nunca a conta que vende.**
> **Você só usa o Instaloader com conta se o dono pedir, depois de ler este aviso.**
>
> Sem conta, o Instagram barra a coleta feita de servidor (erro 403 e pedido de login). Por isso o caminho padrão para Instagram nesta skill é a reserva paga, descrita no SKILL.md, seção "Instagram: caminho padrão". Este arquivo serve à seção "Opção avançada".

- **O que é:** programa de código aberto que baixa posts, legendas e dados do Instagram.
- **Repositório oficial:** https://github.com/instaloader/instaloader
- **Documentação:** https://instaloader.github.io/
- **Licença:** MIT.
- **Instalação:** `bash scripts/instalar.sh` (pacote `instaloader`). Ajuda completa na máquina: `instaloader --help`.

O `scripts/coletar.py` cobre o caso mais pedido (posts de um perfil em planilha, e um post pelo link), com a conta entrando por `--cookies ARQUIVO`. Todo o resto está aqui, com o comando direto.

## Índice

1. Forma geral do comando
2. Alvos: o que dá para coletar
3. O que baixar de cada post
4. O que baixar de cada perfil
5. Quais posts: quantidade, filtro, atualização
6. Login e sessão
7. Onde e como gravar
8. Rede, tentativas e bloqueio
9. Receitas prontas
10. Uso como biblioteca (o que o coletar.py faz por dentro)
11. Erros comuns e o que significam

## 1. Forma geral do comando

```bash
instaloader [opções] alvo [alvo ...]
```

Para cada alvo o programa cria uma pasta e grava, por post: a mídia (foto ou vídeo), um `.txt` com a legenda e um `.json.xz` com os dados completos (curtidas, comentários, data, tipo).

## 2. Alvos: o que dá para coletar

| Alvo | O que traz | Precisa de login |
|---|---|---|
| `perfil` | Todos os posts do perfil | Não, se o perfil for público (o site pode pedir mesmo assim) |
| `@perfil` | Todos os perfis que aquele perfil segue | Sim |
| `"#hashtag"` | Posts da hashtag (entre aspas, por causa do `#`) | Na prática, sim |
| `%id_do_local` | Posts marcados num local | Sim |
| `:feed` | O feed da conta logada | Sim |
| `:stories` | Stories de quem a conta logada segue | Sim |
| `:saved` | Posts salvos da conta logada | Sim |
| `-- -CODIGO` | Um post só, pelo código do link (`/p/CODIGO/`) | Não, se for público |
| `arquivo.json` ou `arquivo.json.xz` | Baixa de novo um item já salvo | Depende do item |
| `+lista.txt` | Lê alvos e opções de um arquivo de texto | Depende |

## 3. O que baixar de cada post

| Opção | Efeito |
|---|---|
| `--no-pictures` | Não baixa fotos (não combina com `--fast-update`) |
| `-V`, `--no-videos` | Não baixa vídeos |
| `--no-video-thumbnails` | Não baixa a capa dos vídeos |
| `--slide N` ou `--slide N-M` | Em carrossel, baixa só a imagem N ou o intervalo |
| `-C`, `--comments` | Baixa os comentários de cada post (uma consulta a mais por post; pede login) |
| `-G`, `--geotags` | Grava o local do post com link de mapa (uma consulta a mais; pede login) |
| `--no-captions` | Não cria o `.txt` da legenda |
| `--post-metadata-txt "MODELO"` | Define o texto do `.txt` de cada post. Ex.: `"{likes} curtidas, {comments} comentarios\n{caption}"` |
| `--storyitem-metadata-txt "MODELO"` | O mesmo, para stories |
| `--no-metadata-json` | Não grava o `.json` de dados |
| `--no-compress-json` | Grava o `.json` legível, sem compactar |

**Só os dados, sem mídia:** `--no-pictures --no-videos --no-video-thumbnails --no-compress-json`.

## 4. O que baixar de cada perfil

| Opção | Efeito |
|---|---|
| `--no-posts` | Não baixa os posts comuns (útil para pegar só stories ou destaques) |
| `--no-profile-pic` | Não baixa a foto do perfil |
| `-s`, `--stories` | Baixa também os stories do perfil (login) |
| `--highlights` | Baixa também os destaques (login) |
| `--tagged` | Baixa também os posts em que o perfil foi marcado |
| `--reels` | Baixa também os Reels |
| `--igtv` | Baixa também os vídeos longos antigos (IGTV) |

## 5. Quais posts: quantidade, filtro, atualização

| Opção | Efeito |
|---|---|
| `-c N`, `--count N` | No máximo N posts. Vale para hashtag, local, `:feed` e `:saved`. **Não limita perfil.** |
| `--post-filter "EXPRESSÃO"` (ou `--only-if`) | Só baixa o post se a expressão for verdadeira. A expressão usa os campos do post |
| `--storyitem-filter "EXPRESSÃO"` | O mesmo, para stories |
| `-F`, `--fast-update` | Para ao achar o primeiro post já baixado. É o modo de manter um arquivo em dia |
| `--latest-stamps [ARQUIVO]` | Guarda a data do último post coletado de cada perfil; atualiza mesmo se a pasta foi apagada |

Para limitar a quantidade num perfil, use o `scripts/coletar.py instagram-perfil --max N`, ou um filtro por data.

Exemplos de filtro:

```bash
--post-filter "date_utc >= datetime(2026, 1, 1)"          # só de 2026 em diante
--post-filter "likes > 1000"                               # só os com mais de mil curtidas
--post-filter "is_video"                                   # só vídeos
--post-filter "not is_video and 'promo' in caption_hashtags"
```

Campos usáveis no filtro: `date_utc`, `date_local`, `likes`, `comments`, `caption`, `caption_hashtags`, `caption_mentions`, `is_video`, `video_view_count`, `typename`, `owner_username`, `tagged_users`, `viewer_has_liked`, `is_sponsored`, `is_pinned`.

## 6. Login e sessão

| Opção | Efeito |
|---|---|
| `-l USUARIO`, `--login USUARIO` | Entra com a conta. Pede a senha no terminal e grava um arquivo de sessão (a sessão, não a senha) |
| `-f ARQUIVO`, `--sessionfile ARQUIVO` | Caminho do arquivo de sessão (padrão: `~/.config/instaloader/session-USUARIO`) |
| `-b NAVEGADOR`, `--load-cookies NAVEGADOR` | Importa a sessão de um navegador instalado na mesma máquina, onde a conta já está aberta. Pede o pacote extra `browser_cookie3`. Em servidor não há navegador, então não serve |
| `-B ARQUIVO`, `--cookiefile ARQUIVO` | Complemento do `--load-cookies`: aponta o banco de cookies do próprio navegador. Não lê o `cookies.txt` exportado por extensão |
| `-p SENHA`, `--password SENHA` | Senha na linha de comando. **Não use:** fica gravada no histórico |

Regra da casa: o dono não usa terminal e a senha nunca passa pelo agente. O dono entra no instagram.com pelo navegador com a conta secundária, exporta os cookies com uma extensão (formato `cookies.txt`) e manda o arquivo. O agente guarda em `~/.config/soft-raspagem/`, fora da pasta da skill, sem copiar o conteúdo para memória ou mensagem, e coleta com `python3 scripts/coletar.py instagram-perfil PERFIL --cookies ARQUIVO`. Quem lê o `cookies.txt` é o `coletar.py`; a linha de comando do `instaloader` não tem opção para esse arquivo.

Os comandos diretos deste arquivo que levam `--login USUARIO` dependem de um arquivo de sessão já gravado nesta máquina (o `coletar.py` aceita o mesmo arquivo com `--sessao USUARIO`). Criar esse arquivo pede a senha digitada no terminal, o que o dono não faz. Sem ele, fique no que o `coletar.py --cookies` cobre.

## 7. Onde e como gravar

| Opção | Efeito |
|---|---|
| `--dirname-pattern MODELO` | Pasta de destino. Aceita `{profile}` e `{target}`. Padrão: `{target}` |
| `--filename-pattern MODELO` | Nome dos arquivos. Padrão: `{date_utc}_UTC`. Aceita `{shortcode}`, `{profile}`, `{mediaid}`, `{date_utc:%Y-%m-%d}` |
| `--title-pattern MODELO` | Nome da foto de perfil e das capas de destaque |
| `--sanitize-paths` | Nomes válidos também em Windows |
| `--resume-prefix PREFIXO` | Prefixo do arquivo que guarda o ponto de retomada |
| `--no-resume` | Não retoma coleta interrompida |

## 8. Rede, tentativas e bloqueio

| Opção | Efeito |
|---|---|
| `--user-agent TEXTO` | Identificação do navegador enviada ao site |
| `--max-connection-attempts N` | Tentativas por consulta (padrão 3; `0` tenta sem fim) |
| `--request-timeout N` | Segundos até desistir de uma consulta (padrão 300) |
| `--abort-on CODIGOS` | Para na hora ao receber esses códigos. Ex.: `--abort-on=302,400,429` |
| `--no-iphone` | Não pede a versão de celular das mídias (menos consultas) |
| `-q`, `--quiet` | Não pergunta nada e só mostra erros. É o modo para tarefa agendada |

Em servidor, use sempre `--abort-on=302,400,401,403,429 --max-connection-attempts 1 --quiet`. Sem isso, ao ser barrado o programa dorme até meia hora e tenta de novo, em silêncio.

## 9. Receitas prontas

```bash
# Posts de um perfil em planilha (legenda, data, curtidas, comentários, link)
python3 scripts/coletar.py instagram-perfil nomedoperfil --max 12

# Um post ou reel pelo link, com a mídia
python3 scripts/coletar.py instagram-post "https://www.instagram.com/reel/CODIGO/" --baixar-midia

# Perfil inteiro, só dados, sem mídia
instaloader --no-pictures --no-videos --no-video-thumbnails --no-compress-json --quiet nomedoperfil

# Só os posts de 2026, com comentários (pede sessão)
instaloader --login USUARIO_DA_CONTA_SECUNDARIA --comments --post-filter "date_utc >= datetime(2026,1,1)" nomedoperfil

# Stories e destaques de um perfil, sem os posts (pede sessão)
instaloader --login USUARIO_DA_CONTA_SECUNDARIA --stories --highlights --no-posts nomedoperfil

# Reels de um perfil
instaloader --reels --no-posts nomedoperfil

# 50 posts de uma hashtag (pede sessão)
instaloader --login USUARIO_DA_CONTA_SECUNDARIA --count 50 "#nomedahashtag"

# Posts em que o perfil foi marcado
instaloader --tagged --no-posts nomedoperfil

# Manter o arquivo do próprio perfil em dia (roda de novo e só traz o que é novo)
instaloader --login USUARIO_DA_CONTA_SECUNDARIA --fast-update --latest-stamps -- nomedoperfil

# Vários perfis em fila, a partir de um arquivo com um nome por linha
instaloader --quiet +perfis.txt
```

## 10. Uso como biblioteca (o que o coletar.py faz por dentro)

O Instaloader também é uma biblioteca Python. É por ela que o `coletar.py` limita a quantidade de posts e monta a planilha.

```python
import instaloader
L = instaloader.Instaloader(quiet=True, max_connection_attempts=1)
# L.load_session_from_file("USUARIO_DO_DONO")      # se o dono criou a sessão
perfil = instaloader.Profile.from_username(L.context, "nomedoperfil")
print(perfil.followers, perfil.mediacount, perfil.biography)
for post in perfil.get_posts():
    print(post.shortcode, post.date_local, post.likes, post.comments, post.caption)
```

O que a biblioteca entrega além do comando:

| Chamada | O que traz | Login |
|---|---|---|
| `Profile.from_username(ctx, nome)` | Seguidores, seguindo, bio, link da bio, total de posts, privado, verificado, conta comercial e categoria | Não |
| `perfil.get_posts()`, `get_reels()`, `get_tagged_posts()`, `get_igtv_posts()` | Posts, um a um | Não |
| `perfil.get_followers()`, `perfil.get_followees()` | Lista de seguidores e de quem segue | Sim |
| `perfil.get_similar_accounts()` | Contas parecidas sugeridas pelo site | Sim |
| `Post.from_shortcode(ctx, codigo)` | Um post pelo código do link | Não |
| `post.get_comments()`, `post.get_likes()` | Comentários e quem curtiu | Sim |
| `Hashtag.from_name(ctx, nome).get_posts()` | Posts de uma hashtag | Na prática, sim |
| `TopSearchResults(ctx, "texto")` | Busca de perfis, hashtags e locais por texto | Sim |
| `L.get_stories()`, `L.get_highlights(perfil)` | Stories e destaques | Sim |

Campos de cada post: `shortcode`, `date_utc`, `date_local`, `typename` (foto, vídeo, carrossel), `caption`, `caption_hashtags`, `caption_mentions`, `likes`, `comments`, `is_video`, `video_view_count`, `video_duration`, `url`, `video_url`, `owner_username`, `tagged_users`, `location`, `is_sponsored`, `is_pinned`, `get_sidecar_nodes()`.

## 11. Erros comuns e o que significam

| Erro do programa | Significado | O que fazer |
|---|---|---|
| `403 Forbidden when accessing` (endereço terminado em `graphql/query`) | O site recusou acesso anônimo deste endereço | Reserva paga (padrão). Opção avançada só se o dono pedir |
| `Redirected to login page. Use --login or --load-cookies.` | O site só responde para conta logada | Reserva paga (padrão). Opção avançada só se o dono pedir |
| `401 Unauthorized` com "Please wait a few minutes" | Bloqueio temporário por volume | Parar; voltar em algumas horas |
| `429 Too Many Requests` | Consultas demais | Parar; voltar depois com menos itens e mais pausa |
| `Profile ... does not exist` | Nome errado, conta apagada, ou o site escondendo o perfil de anônimo | Conferir o nome; se persistir, reserva paga |
| `LoginRequiredException` | A função pedida exige conta | Opção avançada, com o aviso de risco lido pelo dono |
| `Checkpoint required` ou `challenge_required` | O site pediu confirmação de identidade para a conta | O dono abre o aplicativo e confirma |
| `BadCredentialsException`, `TwoFactorAuthRequiredException` | Senha errada ou verificação em duas etapas | O dono exporta os cookies de novo pelo navegador e manda o arquivo |
