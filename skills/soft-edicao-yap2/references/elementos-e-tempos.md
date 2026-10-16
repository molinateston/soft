# Elementos do Yap 2 e como marcar o tempo de cada um

Leia antes do passo 5 (plano de batidas) e do passo 7 (composição). Os nomes entre crases são as funções que já existem no `src/index.template.html` de cada projeto.

## A regra que vale para todos

Cada elemento ilustra as palavras exatas que estão sendo ditas, entra na palavra (tempo tirado do `ancoras.mjs`) e sai dentro da mesma frase. Elemento sem fala por trás é defeito, por mais bonito que fique.

## Os elementos

| Elemento | Quando usar | Como montar |
|---|---|---|
| Legenda de uma palavra | O vídeo inteiro, menos onde uma pilha ou um elemento de tela cheia carrega as palavras | Sai sozinha do `montar-index.mjs`. Minúscula, centrada, altura em `ajustes.json` (`altura_legenda`, entre 1150 e 1400, padrão 1330; topo pelo menos 40 px abaixo do queixo, inclusive no punch-in). Corte seco de palavra para palavra. Sem contorno. |
| Palavra no serifado | Mais ou menos uma por frase: a palavra que carrega o sentido | `assets/destaques.json`: `palavras` marca toda ocorrência, `em` marca uma ocorrência pelo tempo. Sai no serifado itálico, na cor de acento. |
| Aparte em tamanho pequeno | Um comentário de canto, dito mais baixo | `pequeno` no `destaques.json`, com o trecho em segundos. |
| Pilha de frase | Gancho e afirmações grandes | `<div class="stack">` com uma `<span class="ln sans">` ou `ln serif` por linha. Cada linha entra com `line(seletor, tempo)` na sua palavra; a pilha sai com `fadeOut`. Enquanto ela fala, a legenda fica em `ocultar`. |
| Câmera | A cada uma ou duas frases | Com mais de um ângulo gravado, corte entre eles (um `<video class="ang">` por trecho). Com um ângulo só, `punch(1.2 a 1.35, tempo)` e `punch(1, tempo)`, sempre na fronteira de frase. Nunca zoom animado. |
| Cartão | A fala cita algo que existe e tem print | `<div class="card">` com o print real, ao lado ou acima da cabeça. `cardIn` e `cardOut`. No máximo 2 na tela ao mesmo tempo. |
| Explosão de miniaturas | A fala fala de volume ("uma semana inteira de vídeos") | De 10 a 14 `<div class="thumb sc">` com `--x`, `--y` e `--r`; `scatter(".sc", tempo)`. As miniaturas são capas de reels do próprio dono. |
| Faixa de filme | "em lote", "material de apoio", sequência | `<div class="strip">` com quadros; `strip(seletor, tempo, duração)`. |
| Parede de grade | Momento de prova (o que o dono já publicou) | Duas metades `#wt` e `#wb` com capas do dono; `wallIn(tempo)` e `wallOut(tempo)`. |
| Nota manuscrita | Uma confissão pessoal por vídeo | `<div class="note">` com a frase e a seta em SVG; `noteIn` desenha a seta. |
| Momento de interface | A fala descreve a ação de editar | Barra de texto `restyle(barra, frase sans, frase serif, tempo)` ou uma janela simples de linha do tempo. No máximo 2 por vídeo. Mostre só interface honesta, nunca tela inventada de ferramenta real. |
| CTA | Últimos 4 a 6 segundos | Enquadramento mais fechado; "comenta *palavra*" com a palavra no serifado. A palavra sai literal da fala do dono. |

## O plano de batidas (`assets/batidas.md`)

Uma linha por frase da transcrição limpa, com:

1. o tempo de início (do `ancoras.mjs`);
2. UM recurso: só legenda, pilha, cartão, explosão, faixa, parede, nota ou interface;
3. a câmera (aberto, punch-in ou outro ângulo);
4. a palavra no serifado.

Alterne frase cheia e frase vazia. Nunca dois elementos de tela cheia seguidos.

## Exemplo de bloco de tempos

```js
line("#st1 .ln:nth-child(1)", 0.40); line("#st1 .ln:nth-child(2)", 0.72); fadeOut("#st1", 3.95);
punch(1.25, 4.03); punch(1, 7.10);
cardIn("#c1", 4.21); cardOut("#c1", 5.45);
noteIn("#n1", 9.60); fadeOut("#n1", 12.00);
```

Os tempos são da linha do tempo do `limpo.mp4`, a mesma da legenda.

## O que conferir quadro a quadro

Puxe quadros em cada batida com `mosaico.mjs --tempos` e olhe:

- o rosto nunca coberto (boca e olhos livres);
- o serifado legível sobre o fundo do vídeo, na cor de acento certa;
- cartão inteiro dentro do quadro, sem corte na borda;
- a pilha saindo antes da próxima frase;
- borda direita sem faixa preta (o `renderizar.mjs` já mede).
