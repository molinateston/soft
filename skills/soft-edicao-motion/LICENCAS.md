# Licenças do que vem dentro da skill

Conferido em 15/10/2026. Fonte conferida pela tabela `name` do próprio arquivo (fontTools, campos 0, 13 e 14) e por `fc-scan`; imagem conferida pela origem.

## Dentro da skill

| Item | Caminho | Origem | Licença | Texto da licença |
|---|---|---|---|---|
| Inter Black | `template/fonts/Inter-Black.otf` | pacote `fonts-inter` 4.1 do Debian, arquivo sem modificação | SIL Open Font License 1.1 ("Copyright 2016 The Inter Project Authors") | `template/fonts/OFL-Inter.txt` |
| JetBrains Mono Bold | `template/fonts/JetBrainsMono-Bold.ttf` | repositório JetBrains/JetBrainsMono, versão fixa v2.304, pasta `fonts/ttf`, arquivo sem modificação | SIL Open Font License 1.1 ("Copyright 2020 The JetBrains Mono Project Authors") | `template/fonts/OFL-JetBrainsMono.txt` |
| Exemplo neutro | `references/exemplo-neutro.jpg` | gerado para esta skill: padrão de teste do ffmpeg (`testsrc2`) no lugar do rosto, sem perfil (só branco), fala de teste escrita para a skill | feito para a skill, sem terceiro | não se aplica |
| Cenas (arquivo, trilha, rede, página, conversa, celular, anel, cabeça, mascote, degraus) | `template/motion-kit.js`, `template/index.template.html` | desenhadas em HTML, CSS e SVG para esta skill; nenhuma imagem, foto, ícone ou logo de terceiro | da casa | não se aplica |
| `lint_copy.py` e `checar_titulos.py` | `scripts/` | scripts da casa | da casa | não se aplica |
| Demais scripts | `scripts/` | escritos ou adaptados para esta skill | da casa | não se aplica |

Nenhum emoji, foto, avatar, print ou logo vem dentro da skill. As cenas não usam emoji.

## Instalado pelo dono nos Primeiros passos (não vem dentro)

| Dependência | Licença declarada pelo projeto |
|---|---|
| HyperFrames 0.8.93 (npm) | Apache 2.0 |
| GSAP 3.14.2 (npm) | licença própria do GSAP, sem custo, inclusive uso comercial |
| faster-whisper 1.2.1 (pip) e o modelo Whisper, opcionais | MIT |
| ffmpeg | LGPL ou GPL, conforme a compilação instalada |
| Chrome do render | o que o `hyperframes browser ensure` baixar, sob os termos do próprio Chrome |

## O que saiu da origem, e por quê

| Item da origem | Destino | Motivo |
|---|---|---|
| Imagem de abertura (notebook com uma linha do tempo de edição, ilustração gerada) | removida; trocada por um painel de edição desenhado em HTML | imagem ligada a uma peça e a uma pessoa; a skill não carrega imagem de terceiro |
| Fala, títulos, tempos, recortes de rosto e caminhos do vídeo de referência | removidos; viraram tipos de cena com campos, e os tempos saem da fala de cada vídeo | conteúdo de outra pessoa não vai dentro de uma skill neutra |
| Composições feitas por chamada a modelo pago, por bloco | trocadas pelo kit de cenas local, determinado só pelo tempo | o cliente edita sem custo de modelo extra e o resultado se repete igual |
| Camada transparente renderizada à parte e composta com legenda em ASS | trocada por um render único (vídeo, cenas e legenda na mesma página) | um passo e um arquivo intermediário a menos; legenda e cena no mesmo tempo |
