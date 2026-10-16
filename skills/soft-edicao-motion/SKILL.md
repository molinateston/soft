---
name: soft-edicao-motion
description: >-
  Edita a gravação vertical de quem fala pra câmera no estilo Motion: cenas animadas grandes que nascem da fala e se encadeiam, tomadas de tela inteira em fundo preto com volta ao rosto, cartões no peito, legenda curta com a palavra falada na cor de acento e abertura com headline. Entrega o MP4 1080x1920 e o relatório da edição. Use quando o pedido for: "edita no estilo motion", "quero um reel animado com motion", "põe animação grande em cima da fala", "edição rebuscada com cenas", "reel com tela preta e objetos animados", "edita com motion graphics". NÃO use pra: reel cru com cara de editado no celular (soft-edicao-yap); visual desenhado com serifa de revista (soft-edicao-yap2); YAP de websérie com uma versão por gancho (soft-edicao-yap3); abertura em painel e três apoios simples (soft-edicao-simples); edição com b-roll e cartões gerados (soft-editor-video); escrever o roteiro ou o gancho (soft-conteudo-reels, soft-conteudo-headlines). Leia e siga o fluxo inteiro do SKILL.md.
---

# Motion: a fala vira cena animada, e a cena volta pro rosto

Esta skill pega a gravação vertical de uma pessoa falando pra câmera e devolve o reel com motion: cada objeto concreto que a fala cita vira uma cena desenhada e animada, as cenas se encadeiam em causa e ação, tomam a tela inteira em fundo preto nos momentos fortes e devolvem o rosto logo depois. Ela entra DEPOIS da gravação: aqui é edição, nunca escrita. É marca-neutra: a identidade (cor de acento, fonte do título, fonte da legenda) vem do `perfil.json` do dono, e cada cliente roda com a própria.

**A regra que manda em tudo:** a cena nasce da palavra dita, na hora em que ela é dita, e o rosto continua sendo metade do vídeo. Cena sem palavra que a sustente sai. Tela preta comprida demais vira apresentação de slides; figurinha pequena demais vira vídeo comum. As cenas são ilustrações de ideia, nunca prova: sem número, print, perfil nem resultado inventado.

## A condução: a skill te ajuda a fazer, não só te entrega

Pergunte o modo uma vez, na primeira mensagem: "Eu já edito no modo direto (você manda o vídeo e eu monto). Se preferir ser guiado passo a passo, te pergunto uma coisa de cada vez." No silêncio, é o modo direto: pergunte só o que a edição não vive sem. No modo guiado, uma pergunta por vez, dizendo o que precisa, por quê, onde conseguir e o que vem depois:

1. **O vídeo:** o arquivo da gravação. É o único bloqueio duro: sem ele não há edição. Se já existir transcrição com tempo por palavra, peça junto (economiza a transcrição). Depois disso vem o perfil.
2. **O perfil (uma vez só):** se não houver `perfil.json` na pasta de trabalho, peça numa mensagem só os campos de `references/perfil.md` e salve. Sem identidade declarada, só branco, com as fontes livres da skill. Depois vem a headline.
3. **A headline da abertura:** uma ou duas linhas curtas com a ideia dos primeiros segundos. Proponha uma a partir da primeira frase da fala e deixe o dono trocar. Sem abertura, o vídeo começa direto no rosto.
4. **O limite e a chamada final:** a duração máxima, o que não pode sair do corte e a frase do fim na tela (padrão: nenhuma).

Ensine enquanto faz (uma linha do porquê de cada cena) e feche oferecendo o ajuste ("quer menos tela preta, outra cena nesse trecho, a legenda maior?").

## Antes de editar: ambiente pronto, instalado por você

Quem prepara a máquina é você, o agente. O dono não instala nada na mão. Esta skill precisa de node 22, ffmpeg, HyperFrames, GSAP, o Chrome do render e a transcrição local. Nos comandos, `<S>` é a pasta `scripts` desta skill e `<pasta>` é a pasta de trabalho da edição. No Windows, troque `python3` por `python`.

1. **Instale:** `python3 <S>/instalar_ambiente.py --perfil hyperframes --pasta <pasta>`. Ele confere o sistema e instala sozinho o que faltar, dentro da pasta sempre que possível. Na primeira vez leva de 3 a 5 minutos; rodar de novo é seguro. Saída 0, ambiente pronto. Saída 3, falta algo que só o dono faz: passe a ele, em uma frase, o comando exato que o instalador imprimiu e espere. Saída 1, 2 ou 4, leia o motivo, rode de novo uma vez e, se repetir, mostre ao dono o passo e o log.
2. **Prove:** `python3 <S>/prova_render.py --perfil hyperframes --pasta <pasta> --audio <vídeo do dono>`. Só a linha `PROVA DE RENDER: OK` libera a edição. Reprovou, diga ao dono qual item falhou e não edite.
3. **Carregue o ambiente em todo comando:** Linux e Mac `. <pasta>/.ambiente/ativar.sh && <comando>`; Windows `call <pasta>\.ambiente\ativar.bat && <comando>`.
4. **Regra dura:** nunca entregue uma edição simplificada por falta de ferramenta. Ou o ambiente prova que renderiza, ou você para e diz o que falta. Cole a linha da prova no relatório.

O passo a passo completo, com a tabela de estados e as saídas, está em `references/ambiente.md`.

## Regras de partida (o dono pode mudar qualquer uma; registre a mudança no relatório)

1. **Pausa sai, respiro fica.** Silêncio de 0,4 s ou mais (abaixo de -30 dB) sai; o respiro curto da fala fica, porque o motion precisa do ritmo natural (`cortar.mjs --pausa`).
2. **Fala acelerada em 1,2x** (`--velocidade 1.2`; a voz mantém o tom). Use 1 se o dono já fala rápido.
3. **Todo take repetido, começo em falso e frase dita duas vezes sai.** Fica o último take, o mais limpo.
4. **Cortes J/L ligados** (`--jl 6` mais suave, `--no-jl` desliga).
5. **Uma cor de acento só, a do perfil.** Sem identidade, tudo branco.
6. **Takeover entre 30% e 45% do vídeo, rosto livre por pelo menos 1,5 s entre dois blocos de tela preta.**
7. **Não publique, não envie, não use serviço pago sem pedido explícito.** Cena é ilustração: nunca número, logo, print nem resultado inventado.

## O visual (inegociável)

| Elemento | Regra |
|---|---|
| Fundo | Preto absoluto nos takeovers. Objetos brancos; o que está em ação (play, barra, anel, mascote, degrau de destino) na cor de acento, com brilho suave. |
| Títulos e palavras grandes | Fonte do título (padrão Inter Black), caixa alta, 84 a 110 px, entrando letra por letra. Só palavra dita. |
| Cenas | Grandes e encadeadas: o objeto ocupa a tela, se transforma no próximo e sai com desfoque de 0,3 s. Nunca uma coleção de cartõezinhos iguais. Tipos e campos em `references/cenas.md`. |
| Sobre o rosto | Só cenas que respeitam o rosto (`rede`, `timeline`, `cartao`): ficam no peito ou em volta da cabeça, nunca na boca nem nos olhos. |
| Legenda | Grupos de até 4 palavras e 23 letras, caixa alta, fonte da legenda (padrão JetBrains Mono Bold) em 41 px, branca com contorno preto; a palavra falada na cor de acento. Centrada em `capY` (no peito, abaixo do queixo). Continua por cima também nos takeovers. Some durante a abertura. |
| Abertura | Painel de edição desenhado em cima (0 a 700 px), faixa escura com a headline em 89 px (700 a 986 px), rosto embaixo. Corte seco para a primeira cena. |
| Chamada final | Fonte do título, 62 px, abaixo da legenda, do momento em que é dita até o fim. |
| Câmera | Zoom no corpo pelo `reel.json` (`camZoom`, `camOrigemY`) para o rosto encher a parte de cima, medido no enquadramento de cada vídeo. |

`references/exemplo-neutro.jpg` mostra o visual num vídeo de teste neutro (barras de cor no lugar do rosto, sem identidade, só branco): olhe antes de compor.

## Fluxo (rode na pasta de trabalho)

1. **Projeto e transcrição:** `node <S>/novo-reel.mjs "<video>" <slug>` cria `video-projects/<slug>/` com `assets/raw.mp4`, `raw.json`, `words.txt`, as fontes, o `reel.json` (identidade vinda do perfil), `src/index.template.html` e `src/cenas.json` (exemplo neutro). Com transcrição pronta no tempo do bruto: `--transcricao <arquivo.json>`. Sem transcrição nenhuma, ele monta o projeto e diz o que instalar.
2. **Enquadramento:** folha de contato do `raw.mp4` (`ffmpeg -i assets/raw.mp4 -vf fps=1/8,scale=180:-1,tile=12x1 -frames:v 1 conferencia/enquadramento.jpg`). Ache o topo da cabeça e o queixo e acerte no `reel.json`: `camZoom` (1,3 a 1,6 quando o rosto está pequeno), `camOrigemY` (o ponto que fica parado no zoom, perto do peito), `rosto` (x, y, largura e altura do rosto já com o zoom), `capY` (abaixo do queixo) e `aberturaCamY` (de onde a caixa de rosto da abertura recorta).
3. **Escolha do corte:** leia `words.txt` e escreva `assets/keeps.json` (`{"fps":30,"keeps":[{"from":1.3,"to":62.4,"why":"take limpo"}]}`).
4. **Corte:** dentro de `assets/`: `node <S>/cortar.mjs --velocidade 1.2` gera `clean.mp4` e `edit-decisions.json`. Volte para a raiz do projeto e rode `node <S>/palavras-limpo.mjs`: leva as palavras para o tempo do `clean.mp4` (`assets/transcript.json`) e lista as que o corte tirou.
5. **Conferência do corte:** leia o `transcript.json` do começo ao fim e confira a lista de palavras tiradas: palavra comida pelo corte volta para o passo 3. Com faster-whisper instalado, transcreva o `clean.mp4` de novo (`python <S>/transcrever.py assets/clean.mp4 conferencia/clean.json`) e procure frase dobrada e verbo faltando. Palavra ouvida errado vai em `assets/caption-fixes.json` (troca de uma palavra, ou `"frases"` para uma sequência). Depois: `ffmpeg -i assets/clean.mp4 -af silencedetect=noise=-30dB:d=0.35 -f null -` sem nenhum `silence_start`.
6. **Mapa de cenas:** marque os objetos concretos da fala, ache o tempo de cada um com `node <S>/ancoras.mjs "frase" ...` e escreva `src/cenas.json` pelo `references/cenas.md` (tipo, `de`, `ate`, textos, `batidas`). Cena de takeover seguida de outra começa no `ate` da anterior.
7. **Texto da tela pela régua da casa** (abaixo).
8. **Montagem e conferência:** `node <S>/montar-index.mjs` (ele recusa mapa com tipo errado, tempo fora do vídeo ou takeover sobreposto e diz quanto do vídeo é takeover), depois `npx hyperframes lint`. Antes de renderizar o vídeo inteiro, tire quadros soltos, que saem em segundos: `npx hyperframes snapshot . --at 1,5.5,12 --no-end --describe false` (um quadro no meio de cada cena e um em cada volta ao rosto). OLHE: rosto livre fora dos takeovers, legenda legível e fora das cenas, nada cortado na borda.
9. **Render:** `node <S>/renderizar.mjs` gera `renders/<slug>-final.mp4`. Os quadros da câmera passam pelo disco: um vídeo de 70 s pede uns 3 GB livres. Com pouco disco, `--quadros jpg` usa cerca de 6 vezes menos, e só vale com `camZoom` de 1,02 ou mais. Em máquina dividida com outros serviços, rode com prioridade baixa (`nice -n 10` no Linux e no Mac) e `--workers 3`. Tire o mosaico com `node <S>/mosaico.mjs renders/<slug>-final.mp4` (entrada, meio e saída de cada cena) e OLHE de novo. Se o dono tem um vídeo aprovado como modelo, `--contra <modelo.mp4>` põe os dois lado a lado no mesmo tempo.
10. **Entrega** (em português, curta): caminho do arquivo final, duração, o que foi cortado, a lista de cenas com o tempo de cada uma, o que ficou incerto. Nunca publique nem envie nada.

O `renderizar.mjs` existe por um defeito medido: renderizado direto em 1080 px, o vídeo da câmera sai com uma faixa preta de 8 px na borda direita. O template usa janela de 1096 px, o render extrai os quadros em png e o script recorta de volta para 1080x1920. O vídeo, as cenas e a legenda saem num render só, sem camada transparente nem composição à parte.

## Texto da tela pela régua da casa

Título de cena, cartão, headline e chamada repetem o que foi falado, sem resumo e sem reescrita (a headline pode condensar a primeira frase, com aceite do dono).

1. Junte todo texto que vai queimado na tela em `textos-tela.md` (na raiz do projeto) e rode `python3 <S>/lint_copy.py textos-tela.md` até sair 0. Aviso de lint em fala literal não muda a fala: só anota no relatório.
2. Ponha os títulos, um por linha, em `conferencia/titulos.txt` e rode `python3 <S>/checar_titulos.py --peca textos-tela.md --titulos conferencia/titulos.txt --insumos assets > conferencia/checagem-titulos.md`. Preencha cada `<preencher>` do bloco. Linha que reprovaria por causa de fala literal vira nota ao dono, nunca reescrita.

## Conferências antes de entregar

- `ffprobe`: 1080x1920, 30 fps, áudio presente, duração combinada. `ffmpeg -v error -i <final> -f null -` sem saída (o `renderizar.mjs` já imprime).
- Nenhum `silence_start` no `clean.mp4` com `silencedetect=noise=-30dB:d=0.35`.
- Nenhuma palavra perdida no corte sem motivo (a lista do `palavras-limpo.mjs`).
- Mosaico olhado: cada cena no meio da palavra que a nomeia, rosto livre fora dos takeovers, legenda por cima de tudo e legível, só a cor de acento do perfil, nada cortado na borda, borda direita sem faixa preta.
- Takeover entre 30% e 45% (o `montar-index.mjs` imprime) e rosto livre por 1,5 s ou mais entre blocos.

## O que é "pronto"

O MP4 final em `renders/<slug>-final.mp4` passou nas conferências acima, o `textos-tela.md` saiu com lint 0, o `conferencia/checagem-titulos.md` está preenchido sem `<preencher>`, e o relatório no chat diz o caminho, a duração, o que foi cortado, as cenas, o que ficou incerto e o que depende do dono.

## O que esta skill NÃO faz

- O reel cru com cara de editado no celular, com prints acima da cabeça: **soft-edicao-yap**.
- O visual desenhado com serifa e acabamento de revista: **soft-edicao-yap2**.
- O YAP de websérie com título no quadro 0 e uma versão por gancho: **soft-edicao-yap3**.
- A abertura em painel com três apoios simples, sem motion: **soft-edicao-simples**.
- A edição com b-roll, cartões e apoio gerado: **soft-editor-video**.
- Escrever ou corrigir o roteiro e o gancho: **soft-conteudo-reels** e **soft-conteudo-headlines**.
- Publicar, agendar ou enviar o vídeo.

## Arquivos desta skill

- `references/perfil.md`: o esquema do `perfil.json` (o mesmo das outras skills de edição, mais a fonte da legenda).
- `references/cenas.md`: como escolher as cenas, os tipos, os campos e as áreas protegidas.
- `references/exemplo-neutro.jpg`: quadros de um teste neutro com o visual da skill.
- `scripts/instalar_ambiente.py`: instala sozinho o ambiente da edição e grava `ambiente.json`.
- `scripts/prova_render.py`: prova que a máquina renderiza e transcreve antes de editar.
- `references/ambiente.md`: o passo a passo do ambiente, com saídas e regra dura.
- `scripts/conferir-ambiente.mjs`: confere as dependências e diz como instalar o que faltar.
- `scripts/novo-reel.mjs`: cria o projeto, aplica a identidade do perfil e transcreve ou importa a transcrição.
- `scripts/transcrever.py`: transcrição local com tempo por palavra (faster-whisper).
- `scripts/cortar.mjs`: corte das pausas, aceleração e cortes J/L.
- `scripts/palavras-limpo.mjs`: as palavras do bruto no tempo do vídeo limpo.
- `scripts/ancoras.mjs`: tempo de cada frase falada no vídeo limpo.
- `scripts/montar-index.mjs`: legenda em grupos, mapa de cenas conferido e identidade no `index.html`.
- `scripts/renderizar.mjs`: render sem faixa preta, recortado em 1080x1920.
- `scripts/mosaico.mjs`: quadros de cada cena num mosaico, sozinho ou contra um vídeo modelo.
- `scripts/lint_copy.py` e `scripts/checar_titulos.py`: o lint de copy e a régua de títulos da casa.
- `template/index.template.html`: a página do vídeo, com a cor de acento e as fontes como variáveis.
- `template/motion-kit.js`: os tipos de cena e suas animações (vai embutido no `index.html`).
- `template/cenas.exemplo.json`: um mapa de cenas neutro para começar.
- `template/fonts/`: Inter Black (título padrão) e JetBrains Mono Bold (legenda padrão), ambas OFL 1.1.
- `LICENCAS.md`: o que vem dentro da skill e a licença de cada item.

## Nome do arquivo e lint

Nome de arquivo em minúsculas, sem acento, com hífens. Todo `.md` que a skill entregar passa por `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) antes de ser dado como pronto.
