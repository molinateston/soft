# gallery-dl: referência completa por caso de uso

- **O que é:** programa de código aberto que baixa imagens (e os dados delas) de galerias, posts e perfis de centenas de sites: Pinterest, X, Reddit, Tumblr, Flickr, DeviantArt, ArtStation, Behance, Imgur, Bluesky, Mastodon, Wikimedia Commons e muitos outros. Também aceita link direto de arquivo.
- **Repositório oficial:** https://github.com/mikf/gallery-dl
- **Lista de sites aceitos:** https://github.com/mikf/gallery-dl/blob/master/docs/supportedsites.md (ou `gallery-dl --list-extractors`)
- **Todas as opções de configuração:** https://gdl-org.github.io/docs/configuration.html
- **Licença:** GPL-2.0.
- **Instalação:** `bash scripts/instalar.sh` (pacote `gallery-dl`). Ajuda completa na máquina: `gallery-dl --help`.

O `scripts/coletar.py imagens` cobre: baixar até N arquivos de um link com planilha dos dados, ou só a planilha (`--so-dados`). Todo o resto está aqui. Qualquer opção desta página pode ir em `--extra "..."`.

## Índice

1. Forma geral do comando
2. Só os dados e os links, sem baixar
3. Escolher o que baixar: quantidade, data, filtro
4. Onde e como gravar
5. Vários links de uma vez
6. Dados junto com os arquivos e pós-processamento
7. Login e cookies
8. Rede, pausas e bloqueio
9. Configuração e opções próprias de cada site
10. Memória do programa (cache)
11. Saída na tela e investigação de erro
12. Receitas prontas
13. Erros comuns e o que significam

## 1. Forma geral do comando

```bash
gallery-dl [opções] LINK [LINK ...]
```

Por padrão grava em `./gallery-dl/<site>/<autor ou galeria>/`. Gerais: `--version`, `-U` (confere se há versão nova; pela skill use `instalar.sh --atualizar`), `--list-extractors` (sites aceitos, com link de exemplo), `--list-modules`.

## 2. Só os dados e os links, sem baixar

| Opção | Efeito |
|---|---|
| `-j`, `--dump-json` | Imprime os dados de cada item em JSON |
| `-J`, `--resolve-json` | Igual, seguindo também os links intermediários |
| `-g`, `--get-urls` | Imprime só os links dos arquivos |
| `-G`, `--resolve-urls` | Igual, seguindo links intermediários |
| `-s`, `--simulate` | Percorre tudo sem baixar |
| `--no-download` | Não baixa arquivo, mas roda o resto (grava dados, por exemplo) |
| `-K`, `--list-keywords` | Mostra os campos disponíveis naquele link, com exemplo de valor |
| `-N`, `--print [EVENTO:]MODELO` | Imprime só os campos pedidos. Ex.: `--print "{author[name]};{date};{likes}"` |
| `--print-to-file [EVENTO:]MODELO ARQUIVO` | Igual, gravando em arquivo |
| `--Print`, `--Print-to-file` | Como os dois acima, mas baixando também |
| `-E`, `--extractor-info` | Mostra os padrões e ajustes do site daquele link |

Os campos mudam de site para site. Rode `-K` no link antes de montar filtro ou modelo.

## 3. Escolher o que baixar: quantidade, data, filtro

| Opção | Efeito |
|---|---|
| `--range FAIXA` | Quais arquivos, pela posição. Ex.: `1-20`, `5`, `1:24:3` |
| `--post-range FAIXA` | O mesmo, contando posts em vez de arquivos |
| `--child-range FAIXA` | O mesmo, para links externos e capítulos |
| `--date-after DATA` | Só posts depois da data; para ao achar um mais velho. Ex.: `2026-01-01` |
| `--date-before DATA` | Só posts antes da data |
| `--filter "EXPRESSÃO"` | Só baixa o arquivo se a expressão for verdadeira. Ex.: `"width >= 1000 and extension in ('jpg','png')"` |
| `--post-filter "EXPRESSÃO"` | O mesmo, por post |
| `--child-filter "EXPRESSÃO"` | O mesmo, para links externos |
| `--filesize-min`, `--filesize-max TAMANHO` | Por tamanho. Ex.: `200k`, `10M` |
| `--download-archive ARQUIVO` | Anota o que já baixou e pula na próxima vez |
| `-A`, `--abort N` | Para depois de N arquivos seguidos já baixados (para manter pasta em dia) |
| `-T`, `--terminate N` | Igual, parando também as coletas acima e indo ao próximo link |
| `--blacklist`, `--whitelist SITES` | Ignora ou só permite certos sites ao seguir links externos |
| `--tags-blacklist`, `--tags-whitelist ETIQUETAS` | Ignora ou só permite posts com certas etiquetas |

## 4. Onde e como gravar

| Opção | Efeito |
|---|---|
| `-d`, `--destination PASTA` | Pasta base (o programa ainda cria as subpastas por site) |
| `-D`, `--directory PASTA` | Pasta exata, sem subpastas |
| `-f`, `--filename MODELO` | Nome dos arquivos. Ex.: `"{date:%Y-%m-%d}_{id}.{extension}"`; `/O` usa o nome original |
| `--restrict-filenames VALOR` | Troca caracteres problemáticos (`unix`, `windows`, `ascii`) |
| `--windows-filenames` | Nomes válidos em Windows |
| `--no-part` | Não usa arquivo temporário `.part` |
| `--no-skip` | Baixa de novo e sobrescreve |
| `--no-mtime` | Não ajusta a data do arquivo |
| `-r`, `--limit-rate TAXA` | Limita a velocidade. Ex.: `500k` |
| `--chunk-size TAMANHO` | Tamanho do bloco em memória |

## 5. Vários links de uma vez

| Opção | Efeito |
|---|---|
| `-i`, `--input-file ARQUIVO` | Lê os links de um arquivo, um por linha (`-` lê da entrada padrão) |
| `-I`, `--input-file-comment ARQUIVO` | Igual, e comenta cada linha que deu certo |
| `-x`, `--input-file-delete ARQUIVO` | Igual, e apaga cada linha que deu certo |
| `-e`, `--error-file ARQUIVO` | Grava num arquivo os links que deram erro, para repetir depois |
| `--no-input` | Nunca pergunta senha ou código (obrigatório em agente) |

## 6. Dados junto com os arquivos e pós-processamento

| Opção | Efeito |
|---|---|
| `--write-metadata` | Um `.json` de dados ao lado de cada arquivo |
| `--write-info-json` | Um `info.json` com os dados da galeria |
| `--write-tags` | Um `.txt` com as etiquetas de cada imagem |
| `--zip`, `--cbz` | Guarda tudo num arquivo compactado |
| `--mtime CAMPO` | Ajusta a data do arquivo por um campo. Ex.: `date` |
| `--rename MODELO`, `--rename-to MODELO` | Renomeia arquivos já baixados de um modelo de nome para outro |
| `--ugoira FORMATO` | Converte animação do Pixiv em vídeo ou gif (usa ffmpeg) |
| `--exec "COMANDO"` | Roda um comando para cada arquivo baixado (`{}` é o caminho) |
| `--exec-after "COMANDO"` | Roda um comando no fim de tudo |
| `-P`, `--postprocessor NOME`, `-O CHAVE=VALOR` | Liga um pós-processador definido na configuração e passa ajuste |
| `--no-postprocessors` | Desliga todos |

## 7. Login e cookies

| Opção | Efeito |
|---|---|
| `-C`, `--cookies ARQUIVO` | Usa um arquivo de cookies exportado do navegador |
| `--cookies-from-browser NAVEGADOR[/DOMÍNIO]` | Lê os cookies do navegador da mesma máquina |
| `--cookies-export ARQUIVO` | Grava em arquivo os cookies da sessão atual |
| `-u USUARIO`, `-p SENHA`, `--netrc` | Login por usuário e senha. **Não use senha em linha de comando** |

Regra da casa: o dono exporta os cookies da conta dele e entrega o arquivo. No `coletar.py`: `--cookies ARQUIVO`. Sites que hoje quase sempre pedem conta: X, Instagram, Facebook, Pixiv, Patreon. Sites que costumam abrir sem conta: Pinterest, Reddit, Tumblr, Flickr, Imgur, Bluesky, Wikimedia Commons, link direto.

Alguns sites usam chave de acesso em vez de cookies (Reddit, Tumblr, Flickr, DeviantArt): `gallery-dl oauth:NOMEDOSITE` abre o passo a passo, feito pelo dono.

## 8. Rede, pausas e bloqueio

| Opção | Efeito |
|---|---|
| `--sleep SEGUNDOS` | Pausa antes de cada download. Aceita faixa: `2.0-3.5` |
| `--sleep-request SEGUNDOS` | Pausa entre consultas de dados |
| `--sleep-extractor SEGUNDOS` | Pausa antes de começar cada link |
| `--sleep-skip SEGUNDOS` | Pausa depois de pular um arquivo |
| `--sleep-429 SEGUNDOS` | Quanto esperar ao receber "429, consultas demais" |
| `--sleep-retries SEGUNDOS` | Espera antes de tentar de novo (aceita crescimento: `exp=40`) |
| `-R`, `--retries N` | Tentativas por consulta (padrão 4; `-1` sem fim) |
| `--http-timeout SEGUNDOS` | Tempo limite por consulta (padrão 30) |
| `-a`, `--user-agent TEXTO` | Identificação do navegador (`-o browser=firefox` imita um navegador inteiro) |
| `--proxy ENDEREÇO` | Sai por outro endereço de rede |
| `--xff VALOR` | Contorno de restrição por país |
| `--source-address IP`, `-4`, `-6` | Escolhe o endereço de saída |
| `--no-check-certificate` | Ignora erro de certificado (só em último caso) |

O `coletar.py` já usa `--sleep 0.5-1.5`. Para lista grande: `--sleep 2-4 --sleep-request 1`.

## 9. Configuração e opções próprias de cada site

| Opção | Efeito |
|---|---|
| `-o`, `--option CHAVE=VALOR` | Ajuste avulso. Ex.: `-o browser=firefox`, `-o videos=false` |
| `-c`, `--config ARQUIVO` | Arquivo de configuração extra (também `--config-json`, `--config-yaml`, `--config-toml`) |
| `--config-ignore` | Ignora a configuração padrão da máquina |
| `--config-create`, `--config-status`, `--config-open` | Cria, confere e abre o arquivo de configuração |
| `--config-type TIPO` | Formato do arquivo padrão |
| `-X`, `--extractors PASTA` | Carrega módulos de site extras |
| `--compat` | Volta aos nomes antigos de categoria |

Arquivo padrão: `~/.config/gallery-dl/config.json`. Cada site tem ajustes próprios (por exemplo, no X: incluir repostagens e respostas; no Pinterest: incluir vídeos; no Reddit: seguir links externos). A lista está na página de configuração citada no topo.

## 10. Memória do programa (cache)

`--cache-file CAMINHO`, `--cache-status`, `--cache-show MÓDULO`, `--cache-clear MÓDULO` (apaga sessões e cookies guardados; `ALL` apaga tudo), `--cache-vacuum`. Depois de erro estranho de login, `--cache-clear NOMEDOSITE` costuma resolver.

## 11. Saída na tela e investigação de erro

`-q` (quieto), `-w` (só avisos e erros), `-v` (detalhado), `--no-colors`, `--write-log ARQUIVO`, `--write-unsupported ARQUIVO` (links que nenhum módulo soube tratar), `--write-pages` (grava as páginas lidas, para investigar), `--print-traffic` (mostra o tráfego), `-S`/`--server` (modo servidor, raro).

## 12. Receitas prontas

```bash
# Até 20 imagens de um link, com planilha dos dados
python3 scripts/coletar.py imagens "LINK" --max 20

# Só a planilha com os links e os dados, sem baixar nada
python3 scripts/coletar.py imagens "LINK" --max 50 --so-dados

# Uma pasta do Pinterest
python3 scripts/coletar.py imagens "https://www.pinterest.com/usuario/nome-da-pasta/" --max 30

# Um perfil do X, com os cookies do dono
python3 scripts/coletar.py imagens "https://x.com/usuario/media" --max 30 --cookies cookies-do-dono.txt

# Só imagens grandes, publicadas em 2026
python3 scripts/coletar.py imagens "LINK" --max 40 --extra '--date-after 2026-01-01 --filter "width >= 1000"'

# Descobrir que campos aquele link oferece
gallery-dl -K "LINK"

# Lista simples: autor, data e link de cada arquivo (comando direto)
gallery-dl --range 1-50 --print "{date};{category};{filename}.{extension}" "LINK"

# Manter uma pasta em dia: só baixa o que é novo
gallery-dl --download-archive baixados.sqlite3 -A 5 --sleep 2-4 -d imagens "LINK"

# Fila de links a partir de um arquivo, anotando os que falharam
gallery-dl --no-input -i links.txt -e falharam.txt --sleep 2-4
```

## 13. Erros comuns e o que significam

| Erro do programa | Significado | O que fazer |
|---|---|---|
| `Unsupported URL` ou `No suitable extractor found` | O programa não conhece o site | Tentar `video-dados` (yt-dlp); conferir a lista de sites |
| `'429 Too many requests'` | O site limitou o endereço (comum em servidor) | Parar; repetir depois com `--sleep 3-6` e menos itens |
| `403 Forbidden` | Acesso negado | `-o browser=firefox`; cookies do dono |
| `401 Unauthorized`, `AuthRequired`, `login required` | O site pede conta | Cookies do dono |
| `NotFoundError`, `404` | Link errado ou conteúdo apagado | Conferir o link |
| `Failed to download ...` | Um arquivo falhou (os outros podem ter vindo) | Ver o aviso da linha anterior; repetir só os que faltam |
| Nenhum arquivo e nenhum erro | A galeria está vazia para visitante, ou o filtro cortou tudo | Rodar com `-v`; tirar o filtro; tentar com cookies |
