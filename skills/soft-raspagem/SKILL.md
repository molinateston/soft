---
name: soft-raspagem
description: >-
  Raspagem grátis de vídeo, transcrição e imagem, com dois programas de código aberto
  (yt-dlp e gallery-dl), sem conta e sem risco: dados e transcrição de vídeo do YouTube,
  TikTok e centenas de sites; lista de vídeos de um canal; download de vídeo ou áudio;
  imagens de galerias, posts e perfis (Pinterest, Reddit, Tumblr e outros). Instala os
  programas sozinha. Instagram sai pela reserva paga, que custa centavos por coleta, com
  aviso de custo antes e teto de US$ 1; coletar o Instagram logado é opção avançada, com
  risco para a conta. Use quando o pedido for: "transcreve esse vídeo", "lista os vídeos
  desse canal", "baixa esse vídeo", "baixa as imagens desse link", "raspa o perfil tal",
  "pega os posts do concorrente", "baixa esse reel", "coleta sem pagar". NÃO use pra:
  biblioteca de anúncios e criativo de concorrente (soft-espiao), análise do próprio
  Instagram (soft-consultoria-instagram), busca por palavra-chave, Google Maps ou volume
  grande. Leia e siga o fluxo inteiro do SKILL.md.
---

# Raspagem grátis: vídeo, transcrição e imagem sem pagar ferramenta

O dono pede em português ("transcreve esse vídeo", "baixa as imagens desse link"). Você escolhe o programa certo, coleta, confere e entrega o arquivo. O que esta skill entrega de graça, sem conta e sem risco, é **vídeo, transcrição e imagem** (yt-dlp e gallery-dl).

**Instagram é caso à parte.** Sem conta, o Instagram barra a coleta feita de servidor. Por isso o caminho padrão para Instagram é a reserva paga (Apify): custa centavos por coleta e não expõe a conta de ninguém. Coletar logado existe como opção avançada, com risco para a conta usada, e só entra se o dono pedir depois de ler o aviso.

## Regra de ouro

**Vídeo, transcrição e imagem: grátis primeiro. Instagram: reserva paga primeiro, com o custo dito antes. Em qualquer caso, teto de US$ 1 por coleta; acima disso, só com nova ordem do dono. Conta de ninguém entra na coleta sem o dono pedir depois de ler o aviso de risco.** E nunca entrega número inventado: o que não veio, você diz que não veio.

## O que é pronto

| Arquivo | Para que serve |
|---|---|
| `scripts/instalar.sh` | Confere e instala os 3 programas. Pode rodar quantas vezes quiser. |
| `scripts/coletar.py` | Faz a coleta. Um subcomando por tipo de pedido. Grava sempre em pasta. |
| `references/yt-dlp.md` | Tudo que o yt-dlp faz (vídeo e transcrição), por caso de uso. |
| `references/gallery-dl.md` | Tudo que o gallery-dl faz (imagem), por caso de uso. |
| `references/instaloader.md` | Tudo que o Instaloader faz. Só para a opção avançada do Instagram. |

A skill não carrega o código dos 3 programas: ela instala a versão oficial atual de cada um, direto do repositório público de pacotes. Endereço e licença de cada um estão nas referências.

## Tabela de decisão

| O dono pediu | O que você faz | Com o quê |
|---|---|---|
| "Transcreve esse vídeo", "me dá os dados desse vídeo" | `video-dados LINK` | yt-dlp, grátis |
| "Quais os comentários desse vídeo?" | `video-dados LINK --comentarios` | yt-dlp, grátis |
| "Lista os vídeos desse canal, playlist ou perfil do TikTok" | `video-lista LINK --max 30` | yt-dlp, grátis |
| "Baixa esse vídeo" ou "só o áudio" | `video-baixar LINK` ou `--so-audio` | yt-dlp, grátis |
| "Baixa as imagens desse link" (Pinterest, Reddit, Tumblr, galeria) | `imagens LINK --max 20` | gallery-dl, grátis |
| "Só quero a lista das imagens, sem baixar" | `imagens LINK --so-dados` | gallery-dl, grátis |
| "Pega os posts do perfil tal do Instagram" | Seção "Instagram: caminho padrão". Diga o custo antes. | Reserva paga (Apify) |
| "Pega os dados desse post ou reel" (link do Instagram) | Seção "Instagram: caminho padrão". Diga o custo antes. | Reserva paga (Apify) |
| "Usa a minha conta para coletar o Instagram" | Seção "Opção avançada". Só depois de o dono ler o aviso. | Instaloader, com risco para a conta |
| Filtro por data, arquivo incremental, opção que o subcomando não cobre | comando direto do programa | veja a referência do programa |

Na dúvida entre yt-dlp e gallery-dl: vídeo é yt-dlp, imagem é gallery-dl. Se um disser "link sem suporte", tente o outro.

## Fluxo fixo

### 1. Antes de coletar: ambiente pronto, instalado por você

```bash
bash scripts/instalar.sh
```

Prova curta: a saída termina em `RESUMO: os 3 programas estao prontos.` e mostra a versão de cada um. O instalador tenta pipx, depois pip do usuário, depois um ambiente próprio na pasta do usuário. Não pede senha de administrador. Se faltar Python no servidor, ele diz o comando exato que o dono roda uma vez.

De tempos em tempos, e sempre que um site que funcionava parar de funcionar, rode `bash scripts/instalar.sh --atualizar`. Os sites mudam e os programas correm atrás: versão velha é a causa mais comum de erro.

### 2. Coletar

Um alvo por vez. Comece pequeno (3 a 12 itens) para ver se o site deixa.

```bash
python3 scripts/coletar.py video-dados "https://www.youtube.com/watch?v=..."
python3 scripts/coletar.py video-lista "https://www.youtube.com/@canal" --max 30
python3 scripts/coletar.py imagens "https://..." --max 20
```

Pedido de Instagram não começa aqui: vá para a seção "Instagram: caminho padrão".

Cada coleta cria uma pasta `raspagem/<data>-<subcomando>-<alvo>/` (ou a que você passar em `--saida`). Para uma opção que o subcomando não cobre, use `--extra "opções do programa"` ou o comando direto que está na referência.

### 3. Conferir a saída

O script imprime `Situacao: completo | vieram: N | falharam: M` e grava `resumo.json`. Você confere três coisas antes de falar com o dono:

1. O número que veio bate com o pedido. Se veio menos, diga quanto e por quê.
2. Abra a planilha e leia duas ou três linhas: legenda, data e números fazem sentido.
3. O código de saída: `0` veio tudo, `1` veio parte ou deu erro, `2` bloqueio ou pedido de login, `3` programa não instalado.

### 4. Entregar

Entregue sempre o arquivo: a planilha (`posts.csv`, `dados.csv`, `lista.csv`, `itens.csv`), a transcrição (`transcricao-<idioma>.txt`) ou a pasta de mídia. Diga em uma linha quantos itens vieram, de onde e em que data. Se o dono pediu análise, faça em cima do arquivo e cite o arquivo.

### 5. Se o grátis for barrado

Quando o script sair com código `2`, ele já explica em português se foi bloqueio ou pedido de login. Você:

1. Mostra o erro ao dono, sem maquiar.
2. Oferece os caminhos grátis que restam: esperar algumas horas, pedir menos itens, ou o arquivo de cookies do dono (seção "Quando o YouTube ou outro site pede login").
3. Só então oferece a reserva paga (Apify), dizendo antes quanto vai custar. Teto de US$ 1 por coleta. Acima disso, só com nova ordem do dono, com o valor dito por ele.

Não insista em seguida no mesmo site depois de um bloqueio: cada tentativa aumenta o tempo de castigo.

## Instagram: caminho padrão (reserva paga)

O Instagram sem conta foi barrado no teste desta skill em servidor (erro 403 e pedido de login), e o mesmo é esperado no servidor de cada cliente. O caminho padrão é o coletor `apify/instagram-scraper`, no Apify: cobra por item coletado e usa a estrutura dele, sem tocar na conta do dono.

**1. Diga o custo antes de rodar.** O coletor cobra por item (um post, um reel ou um perfil conta como um item). Preço lido na página pública do coletor em 10/11/2026: US$ 2,70 por mil itens no plano gratuito do Apify, menos nos planos pagos. Na prática:

| Pedido | Custo aproximado |
|---|---|
| Um post ou reel | menos de 1 centavo de dólar |
| 12 posts de um perfil, mais os dados do perfil | 4 centavos de dólar |
| 100 posts de um perfil | 27 centavos de dólar |

Teto de US$ 1 por coleta: fique em até 300 itens. Acima disso, só com nova ordem do dono, com o valor dito por ele. O preço pode mudar: confira em `https://apify.com/apify/instagram-scraper` antes de citar um valor ao dono.

**2. Confira a chave, sem imprimir o valor.**

```bash
test -n "$APIFY_TOKEN" && echo token: ok || echo token: ausente
```

Com `ausente`, pare e diga ao dono em uma frase: "Para coletar Instagram eu preciso de uma chave do Apify: crie a conta em apify.com, copie o token em Settings, API & Integrations, e cadastre como `APIFY_TOKEN` nas credenciais do agente." O token nunca vai escrito em comando, em mensagem ou em memória.

**3. Rode a coleta.** Se a skill `soft-consultoria-instagram` estiver instalada, use o coletor dela, que já grava perfil, posts e o recibo com o custo real:

```bash
node ~/.claude/skills/soft-consultoria-instagram/scripts/coletar_instagram.cjs "https://www.instagram.com/nomedoperfil/" PASTA_DE_SAIDA 12
```

Sem ela, a chamada direta é esta. O `maxTotalChargeUsd=1` é o teto de custo aplicado pelo próprio Apify.

```bash
# Posts de um perfil (troque o link e o resultsLimit)
curl -sS -X POST "https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?clean=true&format=json&maxTotalChargeUsd=1" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"directUrls":["https://www.instagram.com/nomedoperfil/"],"resultsType":"posts","resultsLimit":12,"addParentData":false}' \
  -o PASTA_DE_SAIDA/posts-raw.json

# Dados do perfil (bio, seguidores, link): "resultsType":"details","resultsLimit":1
# Um post ou reel: o link do post em directUrls, "resultsType":"posts","resultsLimit":1
```

Campos de cada post na resposta: `url`, `shortCode`, `type`, `timestamp`, `caption`, `likesCount`, `commentsCount`, `videoViewCount`, `videoUrl`, `displayUrl`, `childPosts` (os slides do carrossel). A chamada espera até 5 minutos; se passar disso, peça menos itens.

**4. Confira e entregue** como no fluxo fixo: conte os itens, leia duas ou três linhas, monte a planilha a partir do arquivo e diga ao dono quantos vieram e quanto custou.

De onde vem este passo a passo: o coletor e os campos de entrada são os mesmos que a `soft-consultoria-instagram` usa no catálogo; a forma da chamada e a variável `APIFY_TOKEN` seguem a `soft-espiao`. Provado em 10/11/2026 com 1 post de um perfil público: a chamada respondeu certo e devolveu legenda, data, curtidas e comentários. Em perfil novo, comece com um item só.

## Opção avançada: Instagram logado (Instaloader)

> **AVISO DE RISCO. Leia para o dono antes de qualquer coisa.**
> **Conta usada para coleta automática pode ser limitada ou bloqueada pelo Instagram.**
> **Só conta secundária. Nunca a conta principal, nunca a conta que vende.**
> **Você só usa este caminho se o dono pedir, depois de ler este aviso.** Sem esse pedido, o caminho é a reserva paga.

O que este caminho dá a mais: coleta sem custo por item, e itens que só aparecem para conta logada (stories, destaques, hashtag, marcados). Os subcomandos `instagram-perfil` e `instagram-post` do `coletar.py` continuam existindo para isso, e o resto está em `references/instaloader.md`.

**Como o dono libera, sem terminal.** A senha nunca passa por você.

1. No navegador do computador, o dono entra no instagram.com com a conta secundária.
2. Ele instala uma extensão que exporta cookies no formato `cookies.txt` (no Chrome, "Get cookies.txt LOCALLY"; no Firefox, "cookies.txt"), abre o instagram.com e exporta.
3. Ele manda o arquivo para você pelo Telegram.
4. Você guarda o arquivo fora da pasta da skill, com acesso só do usuário, e não copia o conteúdo para memória, nota ou mensagem:

```bash
mkdir -p ~/.config/soft-raspagem && chmod 700 ~/.config/soft-raspagem
mv ARQUIVO_RECEBIDO ~/.config/soft-raspagem/instagram-cookies.txt && chmod 600 ~/.config/soft-raspagem/instagram-cookies.txt
```

5. Você coleta com `--cookies`:

```bash
python3 scripts/coletar.py instagram-perfil nomedoperfil --max 12 --cookies ~/.config/soft-raspagem/instagram-cookies.txt
python3 scripts/coletar.py instagram-post "https://www.instagram.com/p/CODIGO/" --cookies ~/.config/soft-raspagem/instagram-cookies.txt
```

O `--cookies` é do `coletar.py`, que lê o arquivo e entrega a sessão ao Instaloader. O programa `instaloader` sozinho não lê esse tipo de arquivo: o `--load-cookies` dele pede um navegador instalado na mesma máquina, o que servidor não tem. O `coletar.py` recusa arquivo de cookies guardado dentro da pasta da skill.

Sem `--cookies`, os dois subcomandos tentam o acesso anônimo uma vez. É grátis e não arrisca conta nenhuma, mas a skill não promete que funciona: em servidor o comum é ser barrado, e aí o script aponta a reserva paga.

Cuidados com a conta: dezenas de posts por perfil, poucos perfis por hora, um minuto de pausa entre perfis. Se o script disser que o Instagram barrou mesmo com a conta, pare de usar essa conta para coleta e avise o dono. Quando o dono pedir, apague o arquivo de cookies; para encerrar de vez, ele sai da conta no navegador.

Nota de teste: a leitura do arquivo de cookies foi conferida com um arquivo de exemplo, sem rede. A coleta logada de ponta a ponta não foi provada, porque o teste desta skill não usou conta de ninguém.

## Quando o YouTube ou outro site pede login

Vale para vídeo e imagem. O dono não usa terminal e a senha nunca passa por você.

1. No navegador do computador, com o site aberto e logado, o dono exporta os cookies com a mesma extensão (formato `cookies.txt`) e manda o arquivo pelo Telegram.
2. Você guarda em `~/.config/soft-raspagem/`, fora da pasta da skill, sem copiar o conteúdo para memória ou mensagem.
3. Você repete a coleta com `--cookies ARQUIVO`, que existe nos subcomandos de vídeo e de imagem e é repassado ao `--cookies` do yt-dlp e do gallery-dl.

Avise o dono antes: conta usada para coleta em volume pode ser limitada pelo site. Prefira conta secundária, peça pouco e não repita em seguida.

## Limites honestos

- **Um perfil ou link por vez.** Lista de alvos se faz em fila, com pausa entre um e outro.
- **Servidor é mais barrado do que computador de casa.** Instagram, YouTube e TikTok desconfiam de endereço de servidor. Isso vem do site, e a skill não tem como contornar.
- **Instagram sem conta não funciona em servidor.** No teste veio "403" e "pedido de login" logo na primeira consulta. Por isso o padrão é a reserva paga.
- **Em servidor, o YouTube às vezes pede confirmação de robô.** O erro é `Sign in to confirm you're not a bot` ou, no download, `HTTP Error 403: Forbidden`. No teste desta skill, dados e transcrição de um vídeo e a lista de um canal vieram; o download do áudio do mesmo vídeo foi barrado nas duas tentativas, uma com cada erro. Acontece em algumas tentativas e em outras não, e mais em download do que em dados. O que fazer, nesta ordem: (1) rodar `bash scripts/instalar.sh --atualizar` e tentar de novo uma vez, mais tarde; (2) se o pedido era a fala do vídeo, usar `video-dados`, que traz a transcrição sem baixar nada; (3) pedir ao dono o arquivo de cookies (seção acima); (4) oferecer a reserva paga, com o custo dito antes. Não repita em seguida: piora.
- **Instagram bloqueia por volume.** Mesmo logado, fique em dezenas de posts por perfil e poucas contas por hora.
- **Perfil privado** só com a conta que segue aquele perfil, pela opção avançada. A reserva paga só enxerga perfil público.
- **Transcrição** depende de o vídeo ter legenda (feita pelo autor ou automática). Sem legenda, baixe o áudio e transcreva por outro meio.
- **O que só a reserva paga faz:** Instagram sem expor conta, busca por palavra-chave ou por assunto, Google Maps, biblioteca de anúncios (para isso existe a soft-espiao), volume grande e coleta agendada de muitos perfis.

## Regras de respeito

1. Só dado público, ou a conta do próprio dono. Nada de perfil privado de terceiro, nada de burlar bloqueio.
2. Pausa entre coletas. O script já espera de 2 a 4 segundos entre posts do Instagram; entre um perfil e outro, espere pelo menos um minuto.
3. Senha nunca guardada, nem pedida. Arquivo de cookies fica fora da pasta da skill, com acesso só do usuário, e o conteúdo dele nunca vai para memória, nota ou mensagem.
4. Conteúdo baixado tem dono. Serve para estudo e referência; republicar foto ou vídeo de terceiro é decisão e responsabilidade do dono.
5. Dado pessoal de pessoa comum (seguidores, quem comentou) só se o dono tiver motivo claro, e nunca para disparo de mensagem.

## Conferência final

- [ ] `bash scripts/instalar.sh` terminou com os 3 prontos.
- [ ] A coleta gravou a pasta e o `resumo.json`.
- [ ] Li a planilha e os números fazem sentido.
- [ ] Disse ao dono quantos itens vieram e quantos falharam.
- [ ] Se houve bloqueio, mostrei o erro e avisei o custo antes de qualquer ferramenta paga.
- [ ] Se o pedido era Instagram, fui pela reserva paga, com o custo dito antes e abaixo de US$ 1.
- [ ] Conta do dono só entrou porque ele pediu depois de ler o aviso de risco, e era conta secundária.
