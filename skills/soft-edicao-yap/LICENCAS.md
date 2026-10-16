# Licenças do que vem dentro da skill

Conferido em 15/10/2026. Fonte conferida pela tabela `name` do próprio arquivo (fontTools) e por `fc-scan`; imagem conferida pela origem.

## Dentro da skill

| Item | Caminho | Origem | Licença | Texto da licença |
|---|---|---|---|---|
| DM Serif Display Regular | `template/fonts/DMSerifDisplay-Regular.ttf` | repositório google/fonts, pasta `ofl/dmserifdisplay`, arquivo sem modificação | SIL Open Font License 1.1 (nome reservado "Source", da Adobe; o arquivo não foi alterado nem renomeado) | `template/fonts/OFL-DMSerifDisplay.txt` |
| Inter Bold | `template/fonts/Inter-Bold.otf` | pacote `fonts-inter` 4.1 do Debian, arquivo sem modificação | SIL Open Font License 1.1 | `template/fonts/OFL-Inter.txt` |
| Noto Emoji, 32 PNG de 128 px | `template/emoji/emoji_u*.png` | repositório googlefonts/noto-emoji, versão fixa v2.047, pasta `png/128` | O README do projeto declara as imagens sob Apache 2.0; o arquivo LICENSE da raiz traz a OFL 1.1. As duas permitem redistribuir; os dois textos vão juntos | `template/emoji/LICENSE-Apache-2.0.txt` e `template/emoji/LICENSE-noto-emoji.txt` |
| Exemplo neutro | `references/exemplo-neutro.jpg` | gerado para esta skill: padrão de teste do ffmpeg (`testsrc2`), um print fictício desenhado com Inter (números inventados de propósito, sem dado real) e os textos da skill | feito para a skill, sem terceiro | não se aplica |
| `lint_copy.py` e `checar_titulos.py` | `scripts/` | scripts da casa | da casa | não se aplica |
| Demais scripts e o template | `scripts/`, `template/index.template.html` | escritos ou adaptados para esta skill | da casa | não se aplica |

## Baixado sob demanda, nunca guardado na skill

| Item | Quando | Licença |
|---|---|---|
| Arte de emoji que não está em `template/emoji/` | o `montar-index.mjs` baixa da mesma versão fixa do Noto Emoji (v2.047) para `assets/emoji/` do projeto | a mesma do Noto Emoji acima |

## Instalado pelo dono nos Primeiros passos (não vem dentro)

| Dependência | Licença declarada pelo projeto |
|---|---|
| HyperFrames 0.8.93 (npm) | Apache 2.0 |
| GSAP 3.14.2 (npm) | licença própria do GSAP, sem custo, inclusive uso comercial |
| faster-whisper 1.2.1 (pip) e o modelo Whisper | MIT |
| ffmpeg | LGPL ou GPL, conforme a compilação instalada |
| tesseract (opcional) | Apache 2.0 |
| Chrome do render | o que o `hyperframes browser ensure` baixar, sob os termos do próprio Chrome |

## O que saiu do pacote de origem, e por quê

| Item da origem | Destino | Motivo |
|---|---|---|
| Fonte display do pacote de origem (Regular e Bold) | removida; a padrão virou DM Serif Display, e o dono pode declarar a dele em `fonte_titulo` | a tabela `name` do arquivo não traz copyright nem licença: licença desconhecida não vai dentro |
| Arte de emoji de um fabricante de celular, baixada de um serviço de terceiro | removida; trocada pelo Noto Emoji | essa arte não pode ser redistribuída |
| Quadros de reels de terceiro e folhas de referência com foto de pessoa | removidos; trocados pelo exemplo neutro | imagem de terceiro não vai dentro |
