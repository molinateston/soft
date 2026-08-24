# FORMA "TOPO-FIXO" - talking-head em cima, apoio embaixo (aprovada 18/08/2026)

É a segunda forma desta skill, ao lado do b-roll IA de rodapé. Nasceu do reel
IMG_4133 e foi APROVADA pelo Léo em 18/08 (forma na amostra das 15h36, filme
completo entregue às 18h05). Use esta forma quando o vídeo cru é o Léo falando à
câmera e o apoio são SLIDES de texto + TELAS reais (print/gravação de produto),
não cenas geradas por IA. Motor: React/Remotion, não os scripts Python de b-roll.

## A regra de ouro da forma

O quadro 9:16 (1080x1920) é partido em duas faixas horizontais:

- CIMA (0 → 1070px): rosto do apresentador, `clean_top.mp4`, FIXO o vídeo
  inteiro, NUNCA coberto por nada. É o take limpo, sem legenda queimada.
- BAIXO (1070 → 1920px): a faixa de apoio. Tudo mora aqui - slide de texto,
  tela de produto, barra de progresso. Nada sobe pra cima da divisão.
- LEGENDA da fala: branca, fina, fundo preto translúcido, centralizada, rente à
  divisão (logo ACIMA da linha, sobre o rosto). Nunca no meio, nunca embaixo.

## As 4 correções que o Léo aprovou (cravadas - reproduza sempre)

- A · LEGENDA branca fina rente à divisão (não caixa grossa, não centro da tela).
- B · FALA TRATADA: corta respiração/pausa/silêncio e acelera 1.2x; o vídeo
  começa JÁ na fala. No IMG_4133 isso levou 518s → 384s (6min24s) sem perder
  sentido. Enxuga o morto, não o conteúdo.
- C · ENQUADRAMENTO do rosto INTOCADO: o crop/zoom do `clean_top.mp4` que já
  ficou bom não se mexe (top:-700 left:-135 width:1350 height:2400 no IMG_4133;
  recalibrar só se o cru for outro).
- D · TROCA slide → TELA → slide: no ponto em que a fala cita algo que dá pra
  MOSTRAR (um app, um print, uma tela de produto), a faixa de baixo exibe o
  slide ~1,4s e então a TELA real assume a faixa; ao fim volta pro slide
  seguinte. No IMG_4133: tela "SOFT IA TEAM" em ~82s e o print `ops.png` no
  trecho do Resultado.

## Anatomia da composição (`templates/topo-fixo/src/Director.tsx`)

Identidade cravada: verde `#4ade80`, branco `#f7f7f3`, cinza `#b8b8b8`, fonte
Inter (Black/ExtraBold/Regular em `public/`). Componentes:

- `Lower` - SLIDE de texto: eyebrow (verde, caixa-alta) + título (branco com
  linha de acento verde) + bullets que aparecem UM POR VEZ + barra de progresso
  verde no rodapé. Bullets vêm de `body` separado por `→` ou `·`.
- `LowerScreen` - a TELA: mostra o slide ~42 frames, o slide sai e a tela
  (`video` em loop ou `img`) toma a faixa de baixo, com moldura verde fina.
- `Caption` - legenda da fala, lê `captions.json` (startMs/endMs/text) e
  desenha rente à divisão.
- A METADE DE CIMA é um `<Video clean_top.mp4>` fixo o filme inteiro.

O ROTEIRO da faixa de baixo (quando cada slide/tela entra, com que texto) mora
em `beats.json` - veja `beats.sample.json` como molde. A legenda mora em
`captions.json` (gerada da transcrição Whisper, revisada: a transcrição
automática erra nome de produto/termo, ex "relatórios de ares" = Ads; corrige à
mão antes de renderizar).

## Como rodar (gasto zero, só CPU local)

1. Copie `templates/topo-fixo/` pra pasta de trabalho do vídeo. `npm install`
   (Remotion + @remotion/media).
2. Ponha em `public/`: `clean_top.mp4` (o take limpo sem legenda, na resolução
   cheia) e os assets de tela (mp4/png dos produtos).
3. Escreva `beats.json` (o roteiro da faixa) e `captions.json` (a legenda).
4. Ajuste `durationInFrames` do Director ao tamanho do `clean_top` (30fps).
5. Render resiliente em blocos + concat, com `render_blocos.sh` (idempotente,
   pula bloco já pronto - vídeo longo não recomeça do zero se cair):
   `--codec=h264 --crf=18 --pixel-format=yuv420p`.
6. Versão leve pro Telegram (o chat corta em 50MB; master vai pro Drive):
   `ffmpeg -i FILME_COMPLETO.mp4 -vf scale=-2:1280 -c:v libx264 -crf 30 FILME_web.mp4`.

## Auditoria (mesma regra da skill)

Rode a visão real sobre o mosaico do FINAL antes de dizer "conferido"; sem
mosaico anexo, sem selo. O `06_audit.py` heurístico foi feito pra a forma de
b-roll e REPROVA a topo-fixo por regra do formato antigo (falso negativo) - aqui
a prova é o mosaico olhado, não a nota do script. Visão só na conta OAuth do
motor ativo, gasto zero; sem saldo, entrega com o aviso e sem selo.

## Molde visual aprovado IMG_4361 (22/08/2026)

O IMG_4361 é a referência intocável para os demais vídeos desta família.

- Começar na primeira palavra falada, sem a respiração inicial.
- Acelerar a fala e todas as camadas sincronizadas para 1.2x.
- Manter o apresentador centralizado, com enquadramento aberto e proporções naturais.
- Redimensionar sempre de forma uniforme, sem deformar rosto ou corpo.
- Usar imagens, slides e animações na faixa inferior de acordo com a fala.
- Usar legenda branca simples, rente à divisão das duas áreas.
- Não colocar "Sócio IA" no topo.
- Não criar tarjas laterais artificiais.
- Quando a fonte já tiver faixas laterais, reduzir a presença delas sem aproximar demais o rosto.
- Preservar o IMG_4361 sem regenerar ou alterar.

Em uma nova família visual, produzir e aprovar uma amostra antes de aplicar o
molde ao lote. Depois de uma reprovação, corrigir somente a classe de defeito
citada pelo Léo e conferir essa mesma classe no vídeo inteiro. Elemento aprovado
não volta para edição.
