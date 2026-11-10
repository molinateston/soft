# yt-dlp: referência completa por caso de uso

- **O que é:** programa de código aberto que lê dados, legendas e baixa vídeo e áudio de milhares de sites (YouTube, TikTok, Instagram, Facebook, X, Vimeo, Twitch, Kwai e outros).
- **Repositório oficial:** https://github.com/yt-dlp/yt-dlp
- **Lista de sites aceitos:** https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md (ou `yt-dlp --list-extractors`)
- **Licença:** Unlicense (domínio público).
- **Instalação:** `bash scripts/instalar.sh` (pacote `yt-dlp`). Ajuda completa na máquina: `yt-dlp --help`.

O `scripts/coletar.py` cobre: dados e transcrição (`video-dados`), lista de canal ou playlist (`video-lista`) e download (`video-baixar`). Todo o resto está aqui. Qualquer opção desta página pode ir em `--extra "..."`.

## Índice

1. Forma geral do comando
2. Só os dados, sem baixar
3. Legenda e transcrição
4. Comentários
5. Canal, playlist e perfil: listar e escolher
6. Filtros: data, duração, visualizações
7. Baixar vídeo: escolher qualidade e formato
8. Baixar só o áudio
9. Trechos, capítulos e ao vivo
10. Nome e pasta dos arquivos
11. Capa, descrição e dados dentro do arquivo
12. Login e cookies
13. Rede, pausas e bloqueio
14. Opções próprias de cada site
15. Atalhos prontos e configuração
16. Receitas prontas
17. Erros comuns e o que significam

## 1. Forma geral do comando

```bash
yt-dlp [opções] LINK [LINK ...]
```

Opções gerais úteis: `--version`, `-U` (atualiza, quando instalado como arquivo único; pela skill use `instalar.sh --atualizar`), `--list-extractors`, `--ignore-config`, `-i`/`--ignore-errors` (segue para o próximo item quando um falha), `--abort-on-error`, `--no-warnings`, `-q` (quieto), `-v` (detalhado, para investigar erro).

## 2. Só os dados, sem baixar

| Opção | Efeito |
|---|---|
| `--skip-download` | Não baixa o vídeo, mas grava os arquivos pedidos (legenda, dados, capa) |
| `-s`, `--simulate` | Não baixa nem grava nada |
| `-j`, `--dump-json` | Imprime os dados de cada vídeo em JSON, uma linha por vídeo |
| `-J`, `--dump-single-json` | Imprime um JSON só, com a playlist inteira dentro |
| `--write-info-json` | Grava os dados num arquivo `.info.json` ao lado |
| `-O`, `--print MODELO` | Imprime só os campos pedidos. Ex.: `-O "%(title)s;%(view_count)s;%(upload_date)s"` |
| `--print-to-file MODELO ARQUIVO` | Como `--print`, gravando em arquivo |
| `-F`, `--list-formats` | Lista as qualidades disponíveis |
| `--list-subs` | Lista as legendas disponíveis |
| `--list-thumbnails` | Lista as capas disponíveis |

Campos mais usados: `id`, `title`, `description`, `webpage_url`, `channel`, `channel_follower_count`, `uploader`, `upload_date`, `timestamp`, `duration`, `view_count`, `like_count`, `comment_count`, `repost_count`, `tags`, `categories`, `thumbnail`, `chapters`, `language`, `live_status`, `availability`.

## 3. Legenda e transcrição

| Opção | Efeito |
|---|---|
| `--write-subs` | Grava a legenda feita pelo autor |
| `--write-auto-subs` | Grava a legenda automática do site |
| `--sub-langs LISTA` | Idiomas. Ex.: `"pt.*,en.*"`, `all`, `"all,-live_chat"` |
| `--sub-format FORMATO` | Formato preferido. Ex.: `vtt`, `srt`, `"srt/vtt/best"` |
| `--convert-subs FORMATO` | Converte a legenda (`srt`, `vtt`, `ass`, `lrc`); usa ffmpeg |
| `--embed-subs` | Coloca a legenda dentro do arquivo de vídeo |
| `--sleep-subtitles SEGUNDOS` | Pausa antes de cada legenda |

O `coletar.py video-dados` já pede legenda do autor e automática em português e inglês, e limpa o arquivo para um `.txt` só com a fala. No YouTube, `--sub-langs "pt.*,en.*"` pode trazer também a tradução automática; para só o idioma original use `--sub-langs "pt-orig,en-orig,pt,en"`.

Sem legenda no vídeo, não há transcrição grátis por aqui: baixe o áudio e transcreva por outro meio.

## 4. Comentários

| Opção | Efeito |
|---|---|
| `--write-comments` (ou `--get-comments`) | Traz os comentários para dentro do `.info.json` |
| `--extractor-args "youtube:max_comments=200,all,50,10;comment_sort=top"` | Limita a quantidade no YouTube (total, principais, respostas, respostas por comentário) e ordena por mais relevantes (`top`) ou mais novos (`new`) |

No `coletar.py`: `video-dados LINK --comentarios` grava `comentarios.csv`. Sem limite, um vídeo popular demora muito: passe o limite em `--extra`.

## 5. Canal, playlist e perfil: listar e escolher

| Opção | Efeito |
|---|---|
| `--flat-playlist` | Lista os itens sem abrir cada um (rápido; traz título, link, visualizações e duração, sem data) |
| `-I`, `--playlist-items ITENS` | Quais itens. Ex.: `1:10` (dez primeiros), `1,3,5`, `-5:` (cinco últimos), `::2` (um sim, um não) |
| `--no-playlist` / `--yes-playlist` | Quando o link é de vídeo dentro de playlist: baixa só o vídeo, ou a playlist |
| `--playlist-random` | Ordem aleatória |
| `--lazy-playlist` | Processa conforme vai recebendo, sem esperar a lista toda |
| `--max-downloads N` | Para depois de N downloads |
| `--download-archive ARQUIVO` | Anota o que já baixou e pula na próxima vez |
| `--break-on-existing` | Para ao chegar num item já anotado |
| `-a`, `--batch-file ARQUIVO` | Lê os links de um arquivo, um por linha |

Endereços de canal do YouTube: `/@canal/videos`, `/@canal/shorts`, `/@canal/streams`, `/@canal/playlists`. Busca dentro do programa: `"ytsearch10:texto"` traz os 10 primeiros resultados da busca do YouTube; `"ytsearchdate10:texto"` traz os mais recentes.

## 6. Filtros: data, duração, visualizações

| Opção | Efeito |
|---|---|
| `--date DATA`, `--datebefore DATA`, `--dateafter DATA` | Por data de publicação. Aceita `20260101` ou relativo: `today-30days`, `now-1week` |
| `--match-filters FILTRO` | Filtro por campo. Ex.: `"duration<60"`, `"view_count>=100000 & like_count>1000"`, `"!is_live"`, `"title~='(?i)marketing'"` |
| `--break-match-filters FILTRO` | Igual, mas para a coleta no primeiro que não passar |
| `--min-filesize`, `--max-filesize TAMANHO` | Por tamanho do arquivo. Ex.: `50M` |
| `--age-limit ANOS` | Só vídeos adequados à idade |

Filtro por data ou por curtidas não funciona junto com `--flat-playlist`, porque a lista rápida não traz esses campos.

## 7. Baixar vídeo: escolher qualidade e formato

| Opção | Efeito |
|---|---|
| `-f`, `--format SELETOR` | Escolhe o formato. Ex.: `"bv*+ba/b"` (melhor vídeo mais melhor áudio), `"b[height<=720]"`, `"bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"` |
| `-S`, `--format-sort ORDEM` | Ordena a preferência. Ex.: `"res:720,ext:mp4:m4a"`, `"+size"` (menor arquivo) |
| `--merge-output-format FORMATO` | Formato final ao juntar vídeo e áudio (`mp4`, `mkv`, `webm`) |
| `--remux-video FORMATO` | Troca a embalagem sem recodificar |
| `--recode-video FORMATO` | Recodifica (lento) |
| `--check-formats` | Só escolhe formato que de fato baixa |
| `-N`, `--concurrent-fragments N` | Baixa N pedaços ao mesmo tempo |
| `-r`, `--limit-rate TAXA` | Limita a velocidade. Ex.: `2M` |
| `-R`, `--retries N`, `--fragment-retries N` | Tentativas |
| `-c`, `--continue` / `-w`, `--no-overwrites` | Retoma arquivo parcial / não sobrescreve |

Juntar vídeo e áudio de alta qualidade e converter formato exigem o ffmpeg instalado.

## 8. Baixar só o áudio

| Opção | Efeito |
|---|---|
| `-x`, `--extract-audio` | Extrai o áudio (usa ffmpeg) |
| `--audio-format FORMATO` | `mp3`, `m4a`, `wav`, `flac`, `best` e outros (lista em `yt-dlp --help`) |
| `--audio-quality QUALIDADE` | De `0` (melhor) a `10`, ou taxa como `128K` |
| `-f "ba"` | Baixa só a faixa de áudio, sem converter |

## 9. Trechos, capítulos e ao vivo

| Opção | Efeito |
|---|---|
| `--download-sections "*INICIO-FIM"` | Baixa só um trecho. Ex.: `"*00:01:00-00:02:30"`, ou pelo nome do capítulo |
| `--split-chapters` | Um arquivo por capítulo |
| `--sponsorblock-remove CATEGORIAS` | Corta trechos marcados pela comunidade (ex.: `sponsor,intro`), no YouTube |
| `--sponsorblock-mark CATEGORIAS` | Só marca esses trechos como capítulos |
| `--live-from-start` | Baixa uma transmissão ao vivo desde o começo |
| `--wait-for-video SEGUNDOS` | Espera uma transmissão agendada começar |

## 10. Nome e pasta dos arquivos

| Opção | Efeito |
|---|---|
| `-o`, `--output MODELO` | Nome do arquivo. Ex.: `"%(upload_date)s-%(title).80s-%(id)s.%(ext)s"` |
| `-P`, `--paths PASTA` | Pasta de destino |
| `--restrict-filenames` | Só letras simples, sem espaço nem acento |
| `--windows-filenames` | Nomes válidos em Windows |
| `--trim-filenames N` | Limita o tamanho do nome |

## 11. Capa, descrição e dados dentro do arquivo

`--write-thumbnail` (capa), `--write-description` (descrição em `.description`), `--write-link` (atalho para a página), `--embed-thumbnail`, `--embed-metadata`, `--embed-chapters`, `--convert-thumbnails jpg`, `--load-info-json ARQUIVO` (reaproveita dados já coletados para baixar depois).

## 12. Login e cookies

| Opção | Efeito |
|---|---|
| `--cookies ARQUIVO` | Usa um arquivo de cookies exportado do navegador (formato Netscape) |
| `--cookies-from-browser NAVEGADOR` | Lê os cookies direto do navegador da mesma máquina (`chrome`, `firefox`, `edge`, `brave`, `safari`) |
| `-u USUARIO`, `-p SENHA`, `--netrc` | Login por usuário e senha. **Não use senha em linha de comando** |
| `--video-password SENHA` | Senha de um vídeo protegido (Vimeo, por exemplo) |

Regra da casa: o dono não usa terminal. Ele exporta os cookies pelo navegador, com uma extensão que gera o `cookies.txt`, e manda o arquivo. O agente guarda fora da pasta da skill (`~/.config/soft-raspagem/`), sem copiar o conteúdo para memória ou mensagem, e usa `--cookies ARQUIVO` (no `coletar.py`, a mesma opção). Em servidor não há navegador, então `--cookies-from-browser` não serve. Conta usada para coleta em volume pode ser limitada pelo site: prefira conta secundária.

## 13. Rede, pausas e bloqueio

| Opção | Efeito |
|---|---|
| `--sleep-requests SEGUNDOS` | Pausa entre consultas de dados |
| `--sleep-interval N`, `--max-sleep-interval M` | Pausa aleatória entre N e M segundos antes de cada download |
| `--proxy ENDEREÇO` | Sai por outro endereço de rede |
| `--xff VALOR`, `--geo-verification-proxy` | Contorno de restrição por país |
| `-4`, `-6` | Força o tipo de endereço de rede |
| `--impersonate CLIENTE` | Imita um navegador real (pede o pacote extra `curl_cffi`); `--list-impersonate-targets` mostra as opções |
| `--js-runtimes MOTOR` | Motor de JavaScript para o YouTube (`deno`, `node`). O `coletar.py` já passa `node` quando não há `deno` |
| `--remote-components` | Permite baixar componentes auxiliares do YouTube |
| `--throttled-rate TAXA` | Reinicia o download se a velocidade cair abaixo disso |

Para lista grande: `--sleep-requests 1 --sleep-interval 5 --max-sleep-interval 15`.

## 14. Opções próprias de cada site

`--extractor-args "SITE:CHAVE=VALOR"`. As mais úteis:

- YouTube: `youtube:player_client=...` (troca o tipo de aplicativo imitado), `youtube:lang=pt` (títulos em português), `youtube:max_comments=...`, `youtube:comment_sort=top`.
- TikTok: `tiktok:app_info=...` e `tiktok:device_id=...` (quando o site recusa o acesso padrão).
- Lista completa por site: https://github.com/yt-dlp/yt-dlp#extractor-arguments

## 15. Atalhos prontos e configuração

`-t`, `--preset-alias NOME`: conjuntos prontos de opções. `-t mp3` (áudio em mp3), `-t aac`, `-t mp4` (vídeo em mp4), `-t mkv`, `-t sleep` (pausas seguras para coleta longa).

Configuração fixa: arquivo `~/.config/yt-dlp/config`, uma opção por linha. `--ignore-config` desliga (o `coletar.py` usa, para o resultado não depender da máquina).

## 16. Receitas prontas

```bash
# Dados e transcrição de um vídeo, sem baixar
python3 scripts/coletar.py video-dados "LINK"

# Os 30 vídeos mais recentes de um canal, em planilha
python3 scripts/coletar.py video-lista "https://www.youtube.com/@canal/videos" --max 30

# Shorts de um canal
python3 scripts/coletar.py video-lista "https://www.youtube.com/@canal/shorts" --max 30

# Vídeos de um perfil do TikTok
python3 scripts/coletar.py video-lista "https://www.tiktok.com/@perfil" --max 30

# 200 comentários mais relevantes de um vídeo
python3 scripts/coletar.py video-dados "LINK" --comentarios --extra '--extractor-args "youtube:max_comments=200;comment_sort=top"'

# Só o áudio em mp3 (para transcrever por outro meio)
python3 scripts/coletar.py video-baixar "LINK" --so-audio

# Vídeo em até 1080 de altura
python3 scripts/coletar.py video-baixar "LINK" --altura 1080

# Só um trecho do vídeo
python3 scripts/coletar.py video-baixar "LINK" --extra '--download-sections "*00:01:00-00:02:30"'

# Título, visualizações e data dos vídeos do último mês de um canal (comando direto)
yt-dlp --skip-download --dateafter today-30days --break-match-filters "upload_date>=20260101" \
  -I 1:40 -O "%(upload_date)s;%(view_count)s;%(like_count)s;%(title)s;%(webpage_url)s" "https://www.youtube.com/@canal/videos"

# Os 10 primeiros resultados de uma busca no YouTube, em lista
yt-dlp --flat-playlist -O "%(title)s;%(view_count)s;%(url)s" "ytsearch10:assunto"

# Baixar uma playlist inteira sem repetir o que já veio
yt-dlp --download-archive baixados.txt -t sleep -o "%(playlist_index)03d-%(title).80s.%(ext)s" "LINK_DA_PLAYLIST"
```

## 17. Erros comuns e o que significam

| Erro do programa | Significado | O que fazer |
|---|---|---|
| `Sign in to confirm you're not a bot` | Em servidor, o YouTube às vezes pede confirmação de robô, mais em download do que em dados | `instalar.sh --atualizar` e uma nova tentativa mais tarde; `video-dados` se o pedido era a fala; arquivo de cookies do dono; reserva paga |
| `Your IP address is blocked` (TikTok) | O site barrou o endereço do servidor | Cookies do dono, outra rede ou reserva paga |
| `HTTP Error 403: Forbidden` | Acesso negado ao arquivo | Atualizar o programa; tentar de novo |
| `HTTP Error 429: Too Many Requests` | Consultas demais | Parar; voltar depois com pausas |
| `Video unavailable`, `Private video` | Vídeo apagado, privado ou restrito ao país | Conferir o link; cookies do dono se ele tem acesso |
| `Unsupported URL` | O programa não conhece o site | Tentar `imagens` (gallery-dl) |
| `Requested format is not available` | A qualidade pedida não existe | `-F` para ver as que existem |
| `ffmpeg not found` | Falta o ffmpeg para juntar ou converter | O dono instala: `sudo apt install -y ffmpeg` |
| Aviso de versão antiga (mais de 90 dias) | Programa desatualizado | `bash scripts/instalar.sh --atualizar` |
