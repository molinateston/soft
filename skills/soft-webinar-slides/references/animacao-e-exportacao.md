# Animação e exportação

## O deck.html é a fonte única

Palco fixo de 1920x1080 que escala pra qualquer tela. Todo formato nasce dele.

Pra apresentar: abra o `deck.html` no navegador, em tela cheia (F11).
- Seta direita, espaço, Enter ou clique: próximo clique; no último clique, avança pro slide seguinte.
- Seta esquerda ou Backspace: volta.
- Tecla N: mostra e esconde as notas do apresentador no rodapé, com o número do clique.
- O endereço guarda o slide (`deck.html#12` abre no 12). Número e Enter pulam pro slide (4, 2, Enter vai pro 42); Home e End vão ao primeiro e ao último. Serve pra voltar à tabela no meio das perguntas.

## A revelação por clique

Cada bloco que entra por clique leva `data-click="N"` e `data-fx` (no slide desenhado, você escreve os dois; o script põe a classe `reveal`). O bloco ocupa o lugar dele desde o começo (só fica invisível), então nada pula de posição quando entra.

| efeito | função | no HTML | no PowerPoint |
|---|---|---|---|
| subir | texto | aparece subindo 36px | Flutuar para dentro (preset 42) |
| aparecer | véu, pílula, marca | aparece no lugar | Esmaecer (preset 10) |
| riscar | preço antigo | o traço cresce da esquerda | Revelar da esquerda (preset 22) |
| selo | percentual | cresce do centro | Zoom (preset 53) |

Escolha o efeito pela função, nunca pelo gosto. Máximo de 7 cliques por slide.

## As saídas

- `deck.pdf`: um slide por página, cada um no estado final (todos os cliques abertos). Sai dos PNGs que a conferência já tirou, pelo Chromium do Playwright, sem segunda renderização.
- `mosaico-1.png`, `mosaico-2.png`...: os slides em folhas de 12 (3 colunas), com o número de cada um (`make_mosaic.py`). Deck de até 12 slides sai em `mosaico.png`. No rascunho de texto, folhas de 24.
- `deck.pptx`: o PowerPoint editável (`exportar_pptx.py`).

## Como o PPTX é feito, e o que se perde

O script abre o `deck.html` no Chromium, lê a posição de cada caixa de texto, bloco de cor, borda e imagem, e recria tudo como forma nativa do PowerPoint, na mesma posição (1px vale 0,5pt; 24px viram 12pt). Todo SVG, e todo bloco marcado `data-imagem` (capa desenhada, prévia embaçada), vira imagem na mesma posição e no mesmo clique. O que entra no clique N vira um grupo com a animação do efeito da tabela acima. As notas do apresentador vão pra área de notas de cada slide.

- O texto fica editável. O preço: a quebra de linha pode mudar se a fonte do PowerPoint for outra. Por isso a fonte padrão é Arial (no Linux, a Liberation Sans tem a mesma medida) e o perfil tem `fonte_pptx` e `fonte_acao_pptx` pra apontar a fonte que existe no computador do dono.
- O fundo de cada slide vira a cor sólida do bloco. Degradê e sombra do HTML só vão quando o bloco é SVG ou `data-imagem`.
- O risco do preço vira um retângulo fino girado; o selo vira grupo com Zoom.
- Mudou o deck? Gere de novo. Editar o PPTX à mão e depois rodar o script apaga a edição.

## O que está verificado e o que não está

Verificado aqui, com LibreOffice (não há PowerPoint nesta máquina):
- O arquivo abre e converte pra PDF; a renderização bate com o HTML (mesmas posições, cores e textos).
- As animações são lidas como entrada por clique (subir, aparecer, riscar e selo reconhecidos), uma por clique, na ordem da tela.
- Todo slide tem nota.

Sem verificação (precisa de alguém abrir no PowerPoint e no Keynote):
- O efeito visual exato de cada animação no PowerPoint.
- A fonte de ação no computador do dono: Georgia é o padrão; sem ela, o PowerPoint troca e a pílula pode mudar de largura.
- O Google Slides importa o PPTX sem as animações.

## Imagens

Print e logo entram pelo `<img src>` do slide, com o caminho relativo à pasta dos slides; o `montar_desenho.py` copia pra `img/` na pasta de saída. A pasta inteira viaja junto: o `deck.html` sozinho fica sem as imagens.
