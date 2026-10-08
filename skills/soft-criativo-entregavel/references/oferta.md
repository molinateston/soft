# Kit da oferta (`_kit_criativos/`)

Feito uma vez por oferta, dentro da pasta raiz que o usuário indicar. Guarda o que todos os criativos da oferta reaproveitam: páginas, paleta, fundos, mockup e takes. Exemplo completo e aprovado em `references/exemplo/oferta.json` (oferta "50 Lições Visuais de Budismo para a Vida").

## Conteúdo
1. Reconhecer a pasta
2. `oferta.json`
3. Paleta e tema dos textos
4. Regiões das páginas (para zoom e molduras)
5. Fundos
6. Takes de vídeo
7. Conferir o kit

## 1. Reconhecer a pasta

Liste a pasta raiz e olhe as imagens (monte folhas de contato com miniaturas e leia). O que procurar, com os nomes que costumam aparecer nas ofertas deste usuário:

| O que | Onde costuma estar | Como reconhecer |
|---|---|---|
| Páginas do entregável | `PREVIAS/`, `Impressão/` | imagens verticais (ex.: 1024x1536), uma página por arquivo; pode haver repetidas entre as pastas |
| Capa | dentro das páginas (ex.: `000-capa.png`) | a página com o nome do produto |
| Mockup | `PNGS MOCKUPS/` (ex.: `PRINCIPAL.png`) | PNG com fundo transparente mostrando o produto inteiro |
| Takes de vídeo | `Assets/`, `VIDEOS OUTROS/` | `.MOV`/`.mp4` do tablet, das folhas impressas, de mãos folheando |
| Áudios e avatares antigos | `Criativos/AD nn/` | `.mp3` do gancho/corpo e o áudio completo |
| Fotos de uso | `USANDO/` | fotos de pessoas usando o material (opcionais; hoje não entram nas telas) |

Use todas as páginas únicas que achar: quanto mais páginas, mais variedade na parede e no carrossel. Se a oferta não tem páginas em imagem (só PDF), converta as páginas do PDF em PNG antes (uma por página, ~1024 px de largura) e guarde em `_kit_criativos/paginas/`.

Se faltar algo essencial para a configuração pedida (nenhuma página em imagem, nenhum take para o modo takes, nenhum mockup), diga ao usuário o que falta antes de seguir. Sem mockup, troque as telas `mockup`/`cta` por `destaque` da capa.

## 2. `oferta.json`

```json
{
  "nome": "50 Lições Visuais de Budismo para a Vida",
  "raiz": "D:\\…\\11 - 50 Lições Visuais de Budismo para a Vida",
  "capa": "capa",
  "mockup": "PNGS MOCKUPS/PRINCIPAL.png",
  "dias": "STQQSSD",
  "tinta": [34, 40, 32],
  "paleta": { "a": "#7AA068", "b": "#DEA430" },
  "paginas": { "capa": "Impressão/000-capa.png", "l02": "Impressão/02-licao-02-….png", "l05": "PREVIAS/PREVIA (2).png" },
  "regioes": { "l03": { "ilustracao": [20, 290, 1010, 800], "explicacao": [36, 820, 342, 1240] } },
  "takes": { "tablet_capa": { "arquivo": "Assets/VIDEOS OUTROS/BUDISMO TABLET 01.MOV", "inicio": 0.2, "dur": 5.0 } }
}
```

- Caminhos são relativos a `raiz` (ou absolutos).
- `paginas`: dê identificadores curtos e com sentido (`capa`, `l03` para a lição 3, `p12`…). São esses nomes que o roteiro usa.
- `dias`: iniciais dos dias da semana para o cartão da tela `pilha` (português: `STQQSSD`; espanhol: `LMXJVSD`).
- `tinta`: cor do texto escuro.

## 3. Paleta e tema dos textos

Faz parte da leitura da identidade (seção 5). Duas cores de acento tiradas do próprio material, que combinem entre si: `a` (a principal, a cor que mais identifica o produto) e `b` (uma segunda, quente ou contrastante). Olhe as páginas e o mockup e escolha; não use o coral do Claude nem cores de outra oferta.

Forma curta: `"a": "#7AA068"`. O motor deriva os tons claros, escuros, o marcador e a mancha de transição. Forma completa, se quiser controlar cada tom:

```json
"a": {"a": [122,160,104], "l": [178,208,160], "d": [74,112,66], "mark": [206,228,188], "tint": [230,240,220],
      "blob0": [152,188,132], "blob1": [96,138,86], "blob2": [218,236,204], "base": [245,240,228]}
```

`dark` (o fundo escuro do mockup e do fechamento) é opcional; por padrão sai do tom escuro de `a`. Para definir: `"dark": {"base": [18,35,26], "glow": [47,90,62], "acento": [178,220,156], "texto": [242,240,226], "pill": [44,86,58]}`.

### Tema dos textos (`"texto"` em `oferta.json`)

As pílulas, faixas e textos grandes usam a fonte e as cores da oferta, para parecerem etiquetas do próprio material:

```json
"texto": {"fonte": "CrimsonText-Bold", "fundo": [249, 241, 218], "borda": [176, 140, 62], "tinta": [8, 36, 62],
          "destaque": [122, 31, 43], "marca": [240, 208, 122], "dor": [140, 38, 40]}
```

| Campo | O que é | Como escolher |
|---|---|---|
| `fonte` | arquivo em `assets/fonts/` (sem `.ttf`) | a que mais lembra os títulos do material: `CrimsonText-Bold` (serifada clássica), `Jakarta-Bold` ou `Outfit-Bold` (modernas), `Handlee` (manuscrita), `Archivo`, `SpaceGrotesk` |
| `fundo` | cor da placa do texto | a cor do papel ou das etiquetas do material |
| `borda` | borda dupla fina da placa (opcional) | a cor das molduras do material; sem ela a placa sai lisa |
| `tinta` | cor do texto | a cor dos títulos |
| `destaque` | cor das palavras de destaque | a segunda cor forte do material |
| `marca` | cor do marca-texto e dos sublinhados | um tom claro e quente da paleta |
| `dor` | cor dos selos de dor ("?", "x") | um vermelho ou vinho do material |

Se nenhuma fonte da skill combina, baixe uma fonte de licença livre (Google Fonts) para `assets/fonts/` e use o nome do arquivo. Sem o bloco `"texto"`, vale o padrão antigo: placa branca, Jakarta Bold.

## 4. Regiões das páginas

As telas `lista` e `destaque` apontam pedaços da página (a ilustração, a caixa de explicação, a caixa de prática, o espaço de anotação). Para isso, marque em 2 a 4 páginas bem representativas os retângulos `[x0, y0, x1, y1]`, **em pixels da página com 1024 de largura**.

Como marcar: abra a imagem da página (leia o arquivo), localize cada bloco e anote os cantos. Confira renderizando a folha de conferência de uma tela `destaque` com marcas: a moldura tem que abraçar o bloco. Nomes sugeridos: `ilustracao`, `explicacao`, `exemplo`, `pratica`, `anotacao`. Use os mesmos nomes em todas as páginas para o roteiro ficar previsível.

Regiões muito largas e baixas ficam pequenas no zoom; prefira blocos mais ou menos quadrados ou verticais.

## 5. Fundos

**Os fundos seguem a identidade visual do próprio material.** O usuário reprovou o padrão antigo ("é sempre o mesmo 3D") e aprovou o teste da Jornada de Jesus em Mapas, em que fundo, elementos e textos parecem ter saído das páginas do produto. O objetivo é que tudo no vídeo pareça a mesma peça.

**1. Leia a identidade do material** olhando as páginas e o mockup:

| Pergunta | Exemplo (Jornada de Jesus em Mapas) |
|---|---|
| De que é feito o "papel"? | pergaminho envelhecido, com grão suave |
| Como é o traço? | aquarela e nanquim, ilustração plana, nada de 3D |
| Que molduras e ornamentos aparecem? | moldura dourada dupla com arabescos nos cantos, faixas de título |
| Quais cores mandam? | dourado, azul-marinho, vinho, verde-oliva |
| Que objetos se repetem nas páginas? | bússola, pergaminho enrolado, pino de mapa, lupa, ramo de oliveira, barco |
| Existe uma versão "noite" ou um tom escuro no material? | azul-marinho das faixas e do mapa noturno |

Material desenhado à mão em caderno pede papel pautado e rabiscos; material de receita, papel kraft e ingredientes em aquarela; material com cara de app, aí sim formas limpas. O 3D de "argila brilhante" só entra se o material for assim ou se o usuário pedir.

**2. Gere quatro imagens** (Higgsfield, `gpt_image_2_5`, variant `sunburst`, quality `high`, resolution `2k`; ~2,75 créditos cada; avise o custo): três fundos **limpos, sem nenhum objeto**, em 9:16, e uma folha de elementos em 1:1. Modelos de prompt (troque o que está entre colchetes pela identidade lida):

```text
[a] Vertical 9:16 background for a motion-graphics video, in the style of [ESTILO DO MATERIAL, ex.: an antique hand-illustrated
biblical map page]. [PAPEL/BASE com cor em hex], soft, even, subtle texture. [MOLDURA E ORNAMENTOS do material], close to the
edges. Extremely faint [TRAÇOS TÍPICOS do material] only near the edges and corners, almost invisible. The whole center area
stays completely empty and clean for content. [TÉCNICA: flat illustrated look, watercolor and ink, not 3D, no glossy objects].
No text, no letters, no labels, no people, no logos, no objects.

[b] O mesmo de [a], trocando os traços dos cantos por [SEGUNDO MOTIVO do material, ex.: soft watercolor washes of muted sea
blue in the top left and bottom right corners]. Mesma moldura, mesmo papel.

[dark] Vertical 9:16 dark background ... Deep [COR ESCURA do material, hex] ... a slightly lighter glow in the center and darker
edges. A mesma moldura, em [COR DE ACENTO]. Very faint [MOTIVO] only near the edges. The whole center area stays completely
empty and dark for content. Mesma técnica. No text, no letters, no labels, no people, no logos, no objects.

[objetos] A sprite sheet of eight separate [TÉCNICA] objects in the style of [ESTILO DO MATERIAL], arranged in a clean grid of 3
rows with wide empty gaps between objects, none touching or overlapping, each fully visible: (1) [objeto grande e marcante];
(2) ...; (7) a small [ESTRELINHA/BRILHO do estilo]; (8) ... The background is a completely flat, uniform, solid pure magenta
(#FF00FF), with no shadows, no gradients and no texture. No text, no letters, no labels, no people.
```

Escolha objetos que **aparecem no material** ou no universo dele, um deles pequeno e simétrico para servir de brilho. Nenhum pode ter magenta.

Baixe para `_kit_criativos/bgs/originais/` como `a.png`, `b.png`, `dark.png` e `objetos.png`.

**3. Recorte e posicione os elementos.**

```bash
$PY "$S/fundos_identidade.py" "<kit>" recortar     # corta a folha e numera: bgs/elementos/01.png… e bgs/elementos.jpg
```

Olhe `bgs/elementos.jpg` e escreva `bgs/layout.json`, dizendo quais elementos vão em cada fundo e onde (centro e largura em pixels da tela 1080x1920):

```json
{"a":    [["01", "pill", 905, 1650, 400], ["02", "check", 875, 255, 300], ["07", "spark", 125, 330, 86]],
 "b":    [["04", "pill", 195, 1630, 330], ["06", "check", 905, 1725, 235]],
 "dark": [["01", "pill", 885, 300, 350], ["08", "pill", 205, 1650, 330], ["07", "spark", 150, 390, 76]]}
```

- 5 ou 6 elementos por fundo, nos cantos e nas bordas; o centro fica livre para as páginas.
- Um grande (300 a 400 px) num canto de baixo, um médio no canto oposto de cima, um pequeno, e duas ou três estrelinhas (`spark`, 50 a 90 px).
- Combine o elemento com o fundo quando fizer sentido (o barco em cima do mar, a bússola no fundo escuro).
- Varie entre os três fundos: não repita o mesmo elemento grande em `a` e `b`.

```bash
$PY "$S/fundos_identidade.py" "<kit>" montar       # grava os fundos limpos, os elementos e <nome>_recon.png
```

Confira `bgs/a_recon.png`, `b_recon.png` e `dark_recon.png`: elementos inteiros, sem resto de magenta nas bordas, centro livre. Exemplo completo em `references/exemplo-identidade/layout.json`.

**Sem Higgsfield:** sem os arquivos em `bgs/`, o motor usa um degradê da paleta, sem elementos. Funciona, fica mais simples; diga isso ao usuário.

**Modo antigo (3D).** O script `fundos.py` continua na skill: ele separa objetos de um fundo já gerado com eles (`bgs/caixas.json`). Só use se o usuário pedir o visual 3D das ofertas antigas (Budismo, PMPE); o preenchimento que ele faz atrás dos objetos não fica bom em fundo com textura.

## 6. Takes de vídeo

Só para as configurações com takes. Para cada vídeo gravado, monte uma folha de quadros (1 por segundo) e escolha trechos de 3 a 7 s que mostrem bem o material: a capa, uma página inteira, folhas sendo viradas, várias folhas na mesa, o tablet rolando.

```bash
ffmpeg -v error -y -i "<video>" -vf "fps=1,scale=135:240,tile=16x3" -frames:v 1 folha_take.jpg
```

Registre em `oferta.json → takes` com nomes que descrevam o conteúdo (`tablet_capa`, `folhas_virando`, `folha_licao18`) e rode:

```bash
$PY "$S/preparar_takes.py" "<kit>"
```

Cada segundo de take ocupa ~83 MB em disco; confira o espaço livre. O take precisa durar pelo menos `tempo da tela × velocidade`; se acabar antes, o último quadro fica parado. Vídeos gravados deitados com marca de rotação são endireitados sozinhos pelo ffmpeg.

## 7. Conferir o kit

Antes do primeiro criativo, faça um roteiro mínimo de teste (uma `parede`, um `destaque` com marcas e um `mockup`) ou vá direto ao primeiro criativo e olhe a folha de conferência com atenção redobrada: cores da paleta, fundos e textos com a cara do material, páginas nítidas, molduras nas regiões certas.
