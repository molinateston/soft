# O mapa de cenas (src/cenas.json)

Lido no passo 6 do fluxo do `SKILL.md`. O mapa diz, para cada cena, o tipo, o começo e o fim (segundos do `clean.mp4`, tirados do `ancoras.mjs` na palavra falada) e os textos. O `motion-kit.js` desenha e anima. Texto de cena é sempre palavra dita no vídeo, em caixa alta, curta. `*palavra*` sai na cor de acento.

## Como escolher a cena

1. Leia a fala inteira e marque os **objetos concretos** que ela cita (arquivo, pasta, computador, página, conversa, celular, cabeça, lista, degrau). Cada objeto forte vira uma cena; ideia abstrata sem objeto vira cartão no peito ou fica no rosto.
2. **Encadeie causa e ação:** o arquivo nasce, vira pedido, cai na trilha de edição; a mente se desenha e dela saem os processos. Cenas de takeover seguidas dividem o fundo preto (a próxima começa no `ate` da anterior) e o vídeo não pisca para o rosto no meio.
3. **Respiro de apresentador:** entre dois blocos de takeover, deixe o rosto livre por pelo menos 1,5 s. O rosto falando é metade do estilo.
4. **Proporção que funcionou no estilo:** num vídeo de 70 s, cerca de 5 a 6 blocos de takeover (de 3 a 7 s cada), 1 ou 2 cenas sobre o rosto (rede, trilha) e 3 a 5 cartões no peito. Takeover somando entre 30% e 45% do vídeo. Mais que isso vira apresentação de slides; menos vira vídeo com figurinha.
5. **Entrada na palavra:** a cena entra no começo da palavra que nomeia o objeto (ou até 0,2 s antes). As `batidas` marcam as viradas internas na palavra seguinte.
6. Nenhuma cena nos 0,3 s finais de uma frase que termina a ideia: deixe a saída acontecer no fim da fala.

## Tipos

Campos comuns: `tipo`, `de`, `ate`, `takeover` (força ligado ou desligado), `batidas` (lista de tempos das viradas internas), `tam` (tamanho do título em px).

| Tipo | Takeover padrão | Para quê | Campos |
|---|---|---|---|
| `abertura` | não | Primeiros segundos: painel de edição desenhado em cima, headline numa faixa, rosto embaixo | `linhas` (1 ou 2 linhas da headline, com `*destaque*`), `tam` (padrão 89), `painelAltura` (700), `faixaAltura` (286), `legenda` (padrão false) |
| `arquivo` | sim | Um arquivo de vídeo nasce e dá lugar a um segundo cartão (pedido, roteiro, briefing) | `rotulo`, `segundo`, `batidas[0]` = quando o segundo cartão entra |
| `timeline` | não | Pedaços caem numa trilha de edição e a agulha corre, no peito | `y` (topo da trilha; padrão capY menos 370), `rotulo` |
| `rede` | não | Um objeto no peito liga caminhos até 4 mascotes em volta do rosto, sem cobrir rosto nem legenda | `centro` (texto da tela do objeto), `rotulo` (embaixo), `batidas[0]` = quando o rótulo entra |
| `destino` | sim | O arquivo viaja por um caminho tracejado até um destino | `rotulo` (o destino), `arquivo` (texto do arquivo), `batidas[0]` = quando ele parte |
| `cartao` | não | Cartão de vidro no peito com ícone e a palavra falada | `texto`, `sub` (linha pequena acima), `icone` (`arquivo`, `agente`, `doc`, `nenhum`), `y`, `largura` |
| `tela` | sim | Uma página desenhada se monta bloco a bloco | `titulo` |
| `chat` | sim | Janela de conversa enche com balões alternados | `titulo` |
| `celular` | sim | Mensagens chegam de fora para dentro de um celular | `titulo`, `sub`, `batidas[0]` = quando o `sub` entra |
| `anel` | sim | Anel de luz em perspectiva liga ideias em volta | `titulo`, `batidas[0]` = quando o título entra |
| `mente` | sim | Uma cabeça se desenha, ganha conexões, e dela saem ramos | `titulo`, `sub`, `destaque`, `ramos`, `marca` (palavra ao lado da cabeça), `batidas` = [cartão do meio, ramos, marca] |
| `agente` | sim | O mascote nasce grande, ganha órbita, e uma lista se marca | `titulo`, `sub`, `tarefa`, `rotuloTarefa`, `batidas[0]` = quando a lista entra |
| `niveis` | sim | Degraus sobem e o mascote pula para o degrau de destino | `titulo`, `niveis` (padrão 3), `alvo`, `batidas` = [o pulo, a entrada do título] |
| `palavra` | sim | Uma palavra ou frase curta grande, letra por letra | `texto`, `y`, `tam`, `acento` (true pinta tudo) |

Fora de `cenas`: `"cta": {"de": 65.2, "texto": "Te mando o link", "y": 1570}` põe a chamada final abaixo da legenda até o fim.

## Áreas protegidas

- **Rosto:** `rosto` no `reel.json` (x, y, largura e altura do rosto já com o zoom). A cena `rede` recorta seus caminhos fora dele; `cartao` e `timeline` ficam no peito, abaixo do queixo. Medir no enquadramento de cada vídeo; o padrão é um ponto de partida.
- **Legenda:** faixa de 150 px centrada em `capY`. Fora dos takeovers nada passa nela. Dentro do takeover a legenda continua por cima de tudo (ela é a última camada).
- **Abertura:** enquanto a headline está na tela não há legenda (a headline já diz a ideia). Para manter a legenda também ali, ponha `"legenda": true` na cena `abertura`.

## Quando nenhum tipo serve

Escreva a cena à mão: copie a função mais parecida do `assets/motion-kit.js` do projeto para um bloco `<script>` no fim do `src/index.template.html`, depois do kit, usando a mesma linha do tempo (`window.__timelines.reel`). Não edite o kit da skill dentro do projeto: o `montar-index.mjs` copia a versão da skill de novo a cada montagem.
