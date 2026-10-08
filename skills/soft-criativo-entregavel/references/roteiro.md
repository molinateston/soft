# Roteiro das telas (`roteiro.json`)

O roteiro diz ao motor quais telas aparecem em cada trecho da voz do áudio. O avatar não entra no roteiro: os trechos dele vêm de `tempo.json`.

## Conteúdo
1. Formato do arquivo
2. Regras para escolher as telas
3. Catálogo de telas de página (modo folhas)
4. Telas de take de vídeo (modos takes e mescla)
5. Telas para os trechos sem avatar (gancho e CTA)
6. Textos animados
7. Exemplo comentado: AD 05

## 1. Formato do arquivo

```json
{
  "setas_no_cta": true,
  "cenas": [
    {"tipo": "parede", "inicio": 5.9, "fundo": "a", "fala": "…", "destaque": "l02", "t_destaque": 9.4,
     "pilula": "O que o budismo realmente ensina", "t_pilula": 9.55},
    {"tipo": "carrossel", "inicio": 11.16, "fundo": "b", "paginas": ["l03", "l07", "l08"]}
  ]
}
```

- **Todos os tempos são segundos do áudio original.** O motor converte para o tempo do vídeo (pausas cortadas, aceleração).
- `inicio`: quando a tela entra. Cada tela vai até o início da próxima. A primeira tela de cada trecho de voz começa junto com o trecho, mesmo que o `inicio` esteja um pouco adiante.
- `fundo`: `a`, `b` ou `dark`. Alterne `a` e `b` entre telas vizinhas; `dark` é para o mockup e o fechamento. Se faltar, o motor alterna sozinho.
- `fala`: a frase que a tela cobre. O motor ignora; serve para você e para quem revisar.
- Páginas são citadas pelo identificador de `oferta.json` (`capa`, `l03`…). Regiões de página pelo nome em `oferta.json → regioes` ou por `[x0, y0, x1, y1]` em pixels da página com 1024 de largura.
- Precisa existir pelo menos uma tela em cada trecho de voz (`gancho`, `corpo`, `cta`) que não seja do avatar; o motor para com um aviso se faltar.

### O gancho: avatar sem fundo sobre o print do corpo (padrão)

Quando o gancho é do avatar, ele aparece **recortado, sem o quarto atrás**, por cima de um **print parado** da primeira tela do corpo (o quadro em que ela já está montada). É como se ele estivesse mostrando o que vem a seguir. Quando termina de falar, ele desce e sai, e a imagem parada começa a se mexer dali, sem mancha de transição. Não precisa de nenhuma chave no roteiro: o `montar_base.py` recorta o avatar e o motor monta.

**O corpo não muda.** Planeje e escreva o roteiro exatamente como sempre: mesmas telas, tempos e animações. Nada é criado, esticado ou adiantado para ficar atrás do avatar; o fundo do gancho é só um quadro tirado do corpo que já existe. A primeira versão deixava a primeira tela rodando atrás do avatar desde o segundo 0 e foi reprovada: a mesma parede ficou 12 s seguidos no ar e o vídeo perdeu dinâmica ("você complicou demais").

- **A primeira tela do corpo vira o cartão de visita do vídeo:** é ela que aparece atrás do avatar durante o gancho inteiro. Prefira `parede`, `destaque` ou um `take` bonito. Evite `capa` como primeira tela (1 s depois de entrar ela ainda está folheando, borrada).
- O print é a primeira tela 1 s depois de entrar, e é desse ponto que ela continua quando o corpo começa (pílulas e eventos seguem amarrados à fala, sem atraso). Para outro instante: `"gancho_sobre_material": {"quadro": 1.0}`.
- O enquadramento do avatar é automático: se ele foi gerado com a cabeça no alto do quadro, fica no tamanho original, 170 px mais baixo (as laterais continuam coladas nas bordas da tela); se veio pequeno ou baixo, é ampliado até 1,4x para a cabeça ficar perto do terço de cima. Para mandar na mão: `{"descer": 170, "escala": 1.0}` (escala menor que 1 mostra o braço cortado reto).
- Na folha de conferência, olhe os quadros do gancho com atenção: recorte limpo (sem pedaço de mesa ou parede), rosto inteiro, **braços e mãos inteiros** (braço que termina na manga é recorte falhando), material visível em cima e dos lados. Para ver só o recorte: `kit.py … stills` em três ou quatro instantes do gancho.
- Para o gancho antigo, com o cenário do avatar e a mancha de transição: `"gancho_sobre_material": false`. Só quando o usuário pedir.
- O CTA do avatar continua com o cenário dele.

## 2. Regras para escolher as telas

- **A tela ilustra a frase com material.** Pergunte "que parte do produto prova ou mostra o que está sendo dito?". Fala sobre a variedade do conteúdo → `parede` ou `carrossel`. Fala que enumera qualidades → `lista`. Fala que apresenta o produto pelo nome → `capa`. Fala de rotina ou frequência → `pilha`. Fala sobre um benefício ou um tema → `destaque` com a página daquele tema.
- **Combine a página com o tema.** Leia os títulos das páginas (olhe as imagens) e escolha a que fala do assunto: "equilíbrio" pede a página do Caminho do Meio; "silêncio interno", a do Silêncio Interior.
- **Duração.** Mínimo de ~3,5 s por tela; o melhor fica entre 5 e 9 s. Frase curta se junta à tela vizinha usando os recursos de evolução (`t_crescer`, pílulas com `t_sai`, mais `marcas`).
- **Dinâmica dentro da tela.** Em telas longas, coloque um evento a cada 1 a 2 s amarrado a uma palavra: pílula, check, moldura, selo, página que cresce.
- **Variedade.** Não repita o mesmo tipo em telas vizinhas, e ao longo da leva varie as páginas em destaque.
- **A abertura do corpo** é a tela mais importante: é onde o material aparece pela primeira vez, logo depois do avatar. Prefira `parede` (mostra volume), `capa` ou um `take` bonito.
- **Antes do CTA** funciona bem um `mockup`: o produto inteiro, para a pessoa saber o que vai receber.

## 3. Catálogo de telas de página

### `parede`
Parede de páginas correndo em três colunas, inclinada. Opcionalmente uma página salta para a frente.

| Campo | Para quê |
|---|---|
| `paginas` | lista de páginas (padrão: todas menos a capa) |
| `colunas` | três listas de 6 páginas, se quiser controlar a ordem |
| `destaque`, `t_destaque` | página que salta para a frente e quando |
| `pilula`, `t_pilula` | texto embaixo |

Boa para: volume, "muito conteúdo", abertura do corpo.

### `carrossel`
Uma página grande no centro e as vizinhas menores; passa uma por vez.

| Campo | Para quê |
|---|---|
| `paginas` | 3 a 6 páginas, na ordem |
| `passo` | segundos de cada página no centro (padrão: divide o tempo da tela; não use menos de 1,1 s) |
| `pilula`, `t_pilula` | texto embaixo |

Boa para: frases mais longas sobre o conteúdo, em que dá tempo de ver várias lições.

### `destaque`
Uma página grande. Cada marca leva uma moldura a uma região da página e soma uma pílula embaixo.

| Campo | Para quê |
|---|---|
| `pagina` | a página |
| `marcas` | `[{"t": 19.1, "regiao": "ilustracao", "texto": "Observar"}, …]` (até 3 com texto) |
| `pilula`, `t_pilula` ou `pilulas` | alternativa às marcas, quando não há regiões |

Boa para: enumerações curtas ("observar, refletir e tirar suas conclusões") e para falas sobre um tema específico. Sem marcas, vira uma página grande com zoom lento e pílula.

### `capa`
Folheia várias páginas rápido até parar na capa; depois entra um selo e as páginas abrem em leque atrás dela.

| Campo | Para quê |
|---|---|
| `tira` | páginas que passam; a última é a capa |
| `t_capa` | quando a capa para (na palavra "encontrei", "conheci", "esse material") |
| `selo`, `t_selo` | texto curto do selo (ex.: "50") e quando aparece (quando o número é dito) |
| `leque`, `t_leque` | 4 páginas que abrem atrás da capa e quando |

Boa para: a frase em que o produto é apresentado pelo nome. Use uma vez por criativo.

### `lista`
Página em cima, checklist embaixo. A cada item, um pedaço da página salta ampliado; no fim o checklist sai e a página cresce.

| Campo | Para quê |
|---|---|
| `pagina` | a página (precisa ter regiões marcadas para o zoom) |
| `itens` | `[{"rotulo": "Lições ilustradas", "t_inicio": 31.95, "t_check": 32.75, "regiao": "ilustracao"}, …]`, 2 a 4 itens |
| `t_crescer` | quando o checklist sai e a página cresce (opcional) |
| `pilula`, `t_pilula` | texto que entra depois de crescer |

`t_inicio` é quando o item começa a ser dito; `t_check` é quando termina. O primeiro item ganha só uma moldura na região (para a página inteira continuar visível); os seguintes saltam em zoom. Rótulos curtos, com as palavras da fala.

Boa para: a frase que lista o que o material tem.

### `pilha`
Folhas caindo uma a uma numa pilha, com a semana se enchendo de checks; depois a folha de cima sai da pilha e cresce.

| Campo | Para quê |
|---|---|
| `paginas` | 5 a 8 páginas; **a última é a que cresce**, escolha-a pelo tema do fim da frase |
| `t_inicio`, `passo` | quando a primeira folha cai e o intervalo entre elas (0,13 a 0,25 s) |
| `titulo`, `t_titulo` | pílula do alto (ex.: "Alguns minutos por dia") |
| `semana` | `false` tira o cartão dos dias da semana |
| `t_crescer` | quando a folha de cima cresce (opcional) |
| `pilulas` | pílulas de baixo, uma por vez (`t_sai` na anterior) |

Boa para: rotina, frequência ("uma lição por dia"), seguida dos benefícios.

### `mockup`
O mockup do produto em fundo escuro, com uma pílula. Boa para a última frase antes do CTA.

## 4. Telas de take de vídeo

Os takes são definidos em `oferta.json → takes` e recortados com `preparar_takes.py`.

### `take`
O take quase em tela cheia, dentro de um cartão.

| Campo | Para quê |
|---|---|
| `take` | nome do take |
| `velocidade` | 1.0 normal; até ~1.6 para folhas sendo viradas. O take precisa durar `tempo da tela × velocidade` |
| `foco_y` | 0 a 1, altura do enquadramento (0.5 = centro) |
| `selo` | `{"texto": "50", "t": 26.75}` |
| `titulo`, `t_titulo` | pílula do alto |
| `semana` | `{"t_inicio": 38.5, "passo": 0.13}` põe o cartão da semana por cima do pé do take |
| `pilula`/`pilulas` | texto no pé |

### `take_lista`
Take em cima e checklist embaixo: `take`, `velocidade`, `foco_y`, `itens` (sem `regiao`), `pilula`.

No modo **mescla**, alterne: take para apresentar e dar realidade (mãos, mesa, tablet), páginas para os detalhes (zoom, checklist). No modo **takes**, use só `take` e `take_lista`, variando os takes e as pílulas.

## 5. Telas para os trechos sem avatar

Só entram quando a configuração não tem avatar naquele trecho.

### `frase` (gancho sem avatar)
A parede de páginas no fundo (material já em cena) e a frase do gancho em cartões grandes, linha a linha.

```json
{"tipo": "frase", "inicio": 0.0, "fundo": "b",
 "linhas": [{"texto": "“Se você acredita no budismo,", "t": 0.2}, {"texto": "está sendo enganado.”", "t": 1.6},
            {"texto": "Uma das frases mais absurdas que ouvi", "t": 2.95}]}
```

Até 3 linhas de até ~30 caracteres; `t` é quando a linha começa a ser dita. É o único lugar em que o texto da fala aparece por inteiro, porque sem avatar o gancho ficaria só no áudio.

### `cta` (fechamento sem avatar)
Mockup + texto + setas para baixo.

```json
{"tipo": "cta", "inicio": 52.04, "texto": "Link aqui embaixo", "t_texto": 52.4, "t_setas": 53.0}
```

## 6. Textos animados

Os textos continuam curtos e feitos com as **palavras da fala** (até ~32 caracteres, entrando no segundo em que a expressão começa a ser dita). O que mudou em 2026-10-04: cada texto tem um **estilo de animação**, e o estilo varia ao longo do vídeo. O usuário reprovou "sempre o mesmo padrão" de pílula branca e aprovou o conjunto abaixo ("agora sim, perfeito esse padrão"). A fonte e as cores vêm do tema da oferta (`references/oferta.md`).

Os textos vão em `pilulas`, cada um com `estilo`:

```json
"pilulas": [
  {"texto": "Mais clareza nos Evangelhos", "estilo": "palavras", "destaque": "clareza", "t": 32.25, "t_fim": 33.8, "t_sai": 35.3},
  {"texto": "Para ensinar ou estudar a Bíblia", "estilo": "icone", "icone": "livro", "destaque": "ensinar estudar", "t": 35.5}
]
```

| Estilo | O que acontece | Use para | Campos próprios |
|---|---|---|---|
| `palavras` | as palavras entram uma a uma, no ritmo da fala; as de destaque ganham cor e um sublinhado que se desenha | benefício dito com calma, frase em que uma palavra carrega o sentido | `t_fim` (quando a expressão termina de ser dita), `destaque` |
| `marca` | o texto entra inteiro e um marca-texto passa por trás do destaque | o trecho que é o "problema" ou a "virada" da frase | `destaque`, `t_marca` (quando o trecho é dito), `cor_marca` |
| `soltas` | cada palavra cai na sua plaquinha e fica levemente torta | bagunça, confusão, coisas soltas ou espalhadas (até 5 palavras) | `destaque` |
| `faixa` | uma faixa se desenrola do centro, com brilho de estrelinhas | nome ou promessa curta em tela limpa (capa, parede); até ~20 caracteres | |
| `icone` | um selo com ícone animado surge e a placa se abre a partir dele | dor (`interrogacao`, `x`), prova social (`pessoas`), tempo (`relogio`), estudo ou leitura (`livro`), confirmação (`check`), novidade (`brilho`) | `icone`, `cor_icone`, `destaque` |
| `grande` | texto grande sem placa, linha por linha subindo; o destaque muda de cor e ganha um traço | a frase final antes do CTA, em fundo escuro ou limpo. Linhas separadas por uma barra vertical: `"Visualize\|em minutos"` na tabela, `"Visualize|em minutos"` no arquivo | `escuro: true` em fundo escuro, `tam` |

Campos comuns: `texto`, `t`, `t_sai` (some um pouco antes do próximo), `y` (altura; padrão perto do pé da tela), `tam`, `destaque` (palavras que mudam de cor, separadas por espaço), `dor: true` (o destaque usa a cor de dor).

O selo da tela `capa` conta de 0 até o número sozinho quando é número (`"selo": "50"`).

**Como escolher (a regra é variar com sentido):**

- Leia o tipo da frase: **dor** → `icone` com `interrogacao`/`x`, `soltas` ou `marca` com `dor`; **número** → selo que conta; **nome ou promessa** → `faixa`; **benefício** → `palavras` ou `icone`; **prova social** → `icone` com `pessoas`; **tempo ou rapidez** → `icone` com `relogio` ou `grande`; **frase final** → `grande`.
- Não repita o mesmo estilo em dois textos seguidos, e use pelo menos quatro estilos diferentes num vídeo de 40 a 60 s.
- Quando a animação puder **mostrar** o que a frase diz, prefira essa ("milagres soltos" com as palavras soltas; "em minutos" com o relógio).
- `grande` não tem placa: só em fundo escuro (`mockup`) ou em tela limpa. Em cima de take ou de página ele fica ilegível.
- Texto sem `estilo` ainda funciona e sai como pílula simples, já com a fonte e as cores do tema. As `marcas` da tela `destaque`, o `titulo` da `pilha` e o checklist da `lista` também seguem o tema.
- Na folha de conferência os textos aparecem em meio de animação; para ver um texto pronto, peça um quadro 1 s depois do `t` dele (`kit.py … stills`).

Exemplo completo: `references/exemplo-identidade/roteiro.json` (AD 01 da Jornada de Jesus: nove textos, seis estilos).

## 7. Exemplo comentado: AD 05

Arquivo completo em `references/exemplo/roteiro.json`. A fala e a escolha de cada tela:

| Fala (áudio) | Tela | Por quê |
|---|---|---|
| "O mais curioso é que ela veio de alguém que nunca tinha parado pra estudar o que o budismo realmente ensina." (5,9–11,1 s) | `parede`, salta a Lição 02 em 9,4 s, pílula "O que o budismo realmente ensina" | abertura: mostra o volume do material; a página que salta é a do ensinamento central |
| "Muita gente cria opiniões… não pede que você acredite cegamente em nada." (11,2–17,4 s) | `carrossel` de 5 lições, pílula em 15,3 s | frase longa sobre o conteúdo: dá tempo de ver várias lições |
| "…incentiva a observar, refletir e tirar suas próprias conclusões…" (17,5–22,8 s) | `destaque` da Lição 05 com 3 marcas | enumeração de três verbos: cada um aponta uma parte da página (ilustração, explicação, espaço de anotação) |
| "…encontrei essas 50 Lições Visuais de Budismo para a Vida." (22,9–28,8 s) | `capa`, para em 26,0 s, selo "50" em 26,75 s, leque em 27,9 s | apresentação do produto pelo nome |
| "O material apresenta… lições ilustradas, explicações fáceis de entender e exercícios práticos que ajudam a aplicar cada conceito na rotina." (28,9–37,7 s) | `lista` com a Lição 03, três itens, cresce em 35,6 s, pílula "Para aplicar na rotina" | lista do que o material tem; o fim da frase aproveita a mesma tela |
| "Com apenas alguns minutos por dia… mais equilíbrio… clareza…" (37,8–47,4 s) | `pilha` terminando na Lição 08 (Caminho do Meio), cresce em 41,75 s, pílulas "Mais equilíbrio" e "Mais clareza" | rotina e depois benefícios; a página que cresce é a do equilíbrio |
| "…vale a pena conhecer o assunto por você mesmo." (47,5–52,0 s) | `mockup`, pílula "Conheça por você mesmo" | o produto inteiro antes do CTA |

Resultado: 7 telas em 46 s (média de 6,6 s), 13 s de avatar, material na tela dos 6,8 s aos 53 s.
