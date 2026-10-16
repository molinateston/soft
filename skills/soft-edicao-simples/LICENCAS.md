# Licenças do que vem dentro da skill

Conferido em 15/10/2026. Fonte conferida pela tabela `name` do próprio arquivo (fontTools, campos 0, 13 e 14) e por `fc-scan`; imagem conferida pela origem.

## Dentro da skill

| Item | Caminho | Origem | Licença | Texto da licença |
|---|---|---|---|---|
| Inter Black | `template/fonts/Inter-Black.otf` | pacote `fonts-inter` 4.1 do Debian, arquivo sem modificação (versão 4.001) | SIL Open Font License 1.1, declarada no campo 13 da tabela `name` | `template/fonts/OFL-Inter.txt` |
| Inter Bold | `template/fonts/Inter-Bold.otf` | o mesmo pacote, arquivo sem modificação | SIL Open Font License 1.1 | `template/fonts/OFL-Inter.txt` |
| JetBrains Mono Regular | `template/fonts/JetBrainsMono-Regular.ttf` | arquivo oficial do projeto JetBrains Mono, versão 2.305, sem modificação | SIL Open Font License 1.1, declarada no campo 13 da tabela `name` ("Copyright 2020 The JetBrains Mono Project Authors") | `template/fonts/OFL-JetBrainsMono.txt` |
| `lint_copy.py` e `checar_titulos.py` | `scripts/` | scripts da casa | da casa | não se aplica |
| Demais scripts e o template | `scripts/`, `template/index.template.html` | escritos ou adaptados para esta skill | da casa | não se aplica |

Nenhuma fonte foi renomeada nem alterada, então a cláusula de nome reservado da OFL não se aplica. A skill não traz emoji, foto, avatar, print nem imagem de terceiro.

## Instalado pelo dono nos Primeiros passos (não vem dentro)

| Dependência | Licença declarada pelo projeto |
|---|---|
| HyperFrames 0.8.93 (npm) | Apache 2.0 |
| GSAP 3.14.2 (npm) | licença própria do GSAP, sem custo, inclusive uso comercial |
| faster-whisper 1.2.1 (pip) e o modelo Whisper | MIT |
| ffmpeg | LGPL ou GPL, conforme a compilação instalada |
| Chrome do render | o que o `hyperframes browser ensure` baixar, sob os termos do próprio Chrome |

## Trazido pelo dono a cada vídeo

A imagem da abertura e os três apoios são do dono: foto própria, banco de imagens com licença de uso, ou imagem gerada pela ferramenta que ele já usa. A origem de cada uma vai em `assets/apoios/ORIGENS.md` do projeto. Imagem gerada é ilustração e nunca aparece como prova de caso.

## O que saiu do material de origem, e por quê

| Item da origem | Destino | Motivo |
|---|---|---|
| A fala, a headline, o CTA, os tempos, o recorte e os cortes do vídeo de referência | removidos; viraram regras gerais e campos do `reel.json` | pertencem a um vídeo de uma pessoa real |
| A imagem de abertura e as três imagens de apoio da referência | removidas; o dono traz as dele | imagem de um caso real não vai dentro |
| Caminhos de máquina, nomes de pessoa e a cor fixa de uma marca | removidos; a cor e a fonte vêm do `perfil.json` | a skill é marca-neutra |
| Render por legenda ASS e painel desenhado em imagem | trocados pela cadeia do HyperFrames das outras skills de edição da casa | a mesma cadeia roda em Linux, Mac e Windows sem depender das fontes instaladas no sistema |
