---
name: soft-edicao-simples
description: >-
  Edita a gravação vertical de quem fala pra câmera no estilo Direto: abertura em painel (imagem em cima, headline grossa numa faixa escura, a pessoa falando embaixo), depois o take ampliado a 1,2x, legenda em fonte de código com a palavra falada na cor de acento, três apoios concretos em tela cheia e o CTA com a frase da própria gravação. Entrega o MP4 1080x1920 e o relatório da edição. Use quando o pedido for: "edita no estilo simples", "edita no Direto", "abertura em painel com headline", "legenda verde de código", "põe três imagens de apoio", "edição limpa sem efeito". NÃO use pra: o reel cru de celular com prints acima da cabeça (soft-edicao-yap); o visual serifado de revista (soft-edicao-yap2); o YAP de websérie com título no quadro 0 (soft-edicao-yap3); cenas animadas grandes encadeadas (soft-edicao-motion); edição com b-roll, música e cartões (soft-editor-video); escrever o roteiro ou o gancho (soft-conteudo-reels, soft-conteudo-headlines). Leia e siga o fluxo inteiro do SKILL.md.
---

# Simples, estilo Direto: abertura em painel, legenda de código e três apoios

Esta skill pega a gravação vertical de uma pessoa falando pra câmera e devolve o reel pronto no estilo Direto. Ela entra DEPOIS da gravação: aqui é edição, nunca escrita. É marca-neutra: a cor de acento e a fonte do título vêm do `perfil.json` do dono, e cada cliente roda com a própria. Sem identidade declarada, tudo sai em branco com as fontes livres da skill.

**A regra que manda em tudo:** um acontecimento só na abertura, e depois a pessoa falando. Nada de card, música, efeito ou texto extra. Muita informação na abertura não prende ninguém; uma imagem clara com uma frase grossa prende.

**Origem e honestidade.** As medidas deste estilo (tamanhos, posições, tempos, velocidade, regra de corte) foram tiradas de uma edição aprovada pelo dono que encomendou o estilo e conferidas num render de prova feito só com esta skill. Nada aqui foi medido em desempenho de público: o que "prende" é hipótese a confirmar nas métricas do próprio dono.

## A condução: a skill te ajuda a fazer, não só te entrega

Pergunte o modo uma vez, na primeira mensagem: "Eu já edito no modo direto (você manda o vídeo e eu monto). Se preferir ser guiado passo a passo, te pergunto uma coisa de cada vez." No silêncio, é o modo direto: pergunte só o que a edição não vive sem. No modo guiado, uma pergunta por vez, dizendo o que precisa, por quê, onde conseguir e o que vem depois:

1. **O vídeo:** o arquivo da gravação. É o único bloqueio duro. Depois dele vem a transcrição.
2. **O perfil (uma vez só):** se não houver `perfil.json` na pasta de trabalho, peça numa mensagem só os campos de `references/perfil.md` e salve.
3. **A imagem da abertura:** uma cena que mostra o assunto acontecendo (não um escritório qualquer). Onde conseguir: foto do próprio dono, banco de imagens com licença de uso, ou imagem gerada pela ferramenta que o dono já usa. Imagem gerada é ilustração, nunca prova de caso. Depois disso vêm os apoios.
4. **Os três apoios:** três imagens de coisas concretas que a fala cita (o objeto, a tela, a ação), da mesma origem permitida. Sem foto ou print de terceiro sem permissão.
5. **A headline:** proponha uma, fiel à fala, em até 2 linhas, e pergunte se pode. O dono pode mandar a dele.

Ensine enquanto faz (uma linha do porquê de cada escolha) e feche oferecendo o ajuste ("quer outra imagem de abertura, outra palavra em destaque, o corte mais seco?").

## Antes de editar: ambiente pronto, instalado por você

Quem prepara a máquina é você, o agente. O dono não instala nada na mão. Esta skill precisa de node 22, ffmpeg, HyperFrames, GSAP, o Chrome do render e a transcrição local. Nos comandos, `<S>` é a pasta `scripts` desta skill e `<pasta>` é a pasta de trabalho da edição. No Windows, troque `python3` por `python`.

1. **Instale:** `python3 <S>/instalar_ambiente.py --perfil hyperframes --pasta <pasta>`. Ele confere o sistema e instala sozinho o que faltar, dentro da pasta sempre que possível. Na primeira vez leva de 3 a 5 minutos; rodar de novo é seguro. Saída 0, ambiente pronto. Saída 3, falta algo que só o dono faz: passe a ele, em uma frase, o comando exato que o instalador imprimiu e espere. Saída 1, 2 ou 4, leia o motivo, rode de novo uma vez e, se repetir, mostre ao dono o passo e o log.
2. **Prove:** `python3 <S>/prova_render.py --perfil hyperframes --pasta <pasta> --audio <vídeo do dono>`. Só a linha `PROVA DE RENDER: OK` libera a edição. Reprovou, diga ao dono qual item falhou e não edite.
3. **Carregue o ambiente em todo comando:** Linux e Mac `. <pasta>/.ambiente/ativar.sh && <comando>`; Windows `call <pasta>\.ambiente\ativar.bat && <comando>`.
4. **Regra dura:** nunca entregue uma edição simplificada por falta de ferramenta. Ou o ambiente prova que renderiza, ou você para e diz o que falta. Cole a linha da prova no relatório.

O passo a passo completo, com a tabela de estados e as saídas, está em `references/ambiente.md`.

## Regras de partida (o dono pode mudar qualquer uma; registre a mudança no relatório)

1. **Velocidade 1,2x no corpo inteiro** (`velocidade` no `reel.json`).
2. **Só sai o que é inequívoco:** começo e fim mortos, take repetido, começo em falso, e pausa entre frases de 0,7 s ou mais (`pausa_max`). Pausa menor fica: a 1,2x ela vira o respiro natural do estilo. A frase de abertura sai inteira.
3. **Abertura de 5 s**, sem legenda por cima: a headline é o texto dela.
4. **Três apoios**, cada um de 2 a 3 s, em tela cheia, entrando na palavra que a fala cita.
5. **Uma cor de acento só, a do perfil.** Sem identidade, tudo branco.
6. **Não publique, não envie, não use serviço pago sem pedido explícito.** Nunca invente número, logo, caso nem imagem que pareça prova.

## O visual (inegociável, medido no quadro de 1080x1920)

| Elemento | Regra |
|---|---|
| Abertura | Painel por 5 s: imagem 1080x700 no topo, faixa `#101010` de y700 a y986, a pessoa falando embaixo (janela 1080x934 do take sem ampliar). Corte seco para o corpo. |
| Headline | Fonte do título (padrão Inter Black), **89 px fixos**, 2 linhas no máximo, centralizada na faixa, tinta das linhas em y739 e y852, largura até 944 px. Branca, com UMA palavra na cor de acento (`*palavra*` no `reel.json`). Não coube? Encurte o texto, nunca a fonte (até uns 21 caracteres por linha). |
| Corpo | O take ampliado 1,5x (recorte 720x1280 do quadro), cabeça inteira no terço de cima, peito livre para a legenda. |
| Legenda | JetBrains Mono em negrito, maiúsculas, grupos de até 4 palavras em até 2 linhas de 23 caracteres, contorno quase preto e sombra curta. A palavra falada acende na cor de acento. Centro do bloco em x500, y1490. Contínua por cima dos apoios. |
| Apoios | Três, tela cheia, 2 a 3 s, zoom lento de 1 a 1,04 e nenhum outro movimento. Coisa concreta que a fala cita; teclado ou escritório genérico não serve. |
| CTA | A frase do pedido como foi falada (fonte do título, padrão Inter Bold, 76 px de corpo), topo do texto em y1600, entra no verbo do pedido e fica até o fim, junto com a legenda. |
| Fora | Música, card, emoji, transição, tarja, logo e moldura. |

## Fluxo (rode na pasta de trabalho)

1. **Projeto e transcrição:** `node <S>/novo-reel.mjs "<video>" <slug>` cria `video-projects/<slug>/` com `assets/raw.mp4`, `raw.json`, `words.txt`, as fontes, o template e o `reel.json` (identidade do perfil mais o plano do vídeo para preencher). Já tem a transcrição? `--transcricao <arquivo.json>`.
2. **Enquadramento:** `ffmpeg -i assets/raw.mp4 -vf fps=1/6,scale=270:-1,tile=6x2 -frames:v 1 enquadramento.jpg` e olhe. Em `corpo_recorte` (`[720, 1280, x, y]`): `x` = centro médio do rosto menos 360; `y` = topo mais alto da cabeça no take menos uns 40 px. A janela da abertura usa o mesmo `y` (troque em `abertura.janela_y` se a cabeça sair cortada).
3. **Escolha do corte:** leia `words.txt` e escreva `assets/keeps.json` (`{"keeps":[{"from":1.2,"to":48.7,"why":"fala inteira"}]}`): começo 0,1 s antes da primeira palavra, fim 0,1 s depois da última, take repetido fora.
4. **Corte:** dentro de `assets/`: `node <S>/cortar.mjs` gera `clean.mp4` já a 1,2x, `edit-decisions.json` e `transcript.json` (as palavras na linha do tempo do vídeo limpo, pela mesma conta do corte).
5. **Conferência do corte:** com o faster-whisper, transcreva o `clean.mp4` (`"$WHISPER_PYTHON" <S>/transcrever.py clean.mp4 conferencia.json`) e leia do começo ao fim: frase dobrada, palavra comida, verbo faltando. Achou, volte ao passo 3. Palavra ouvida errado vai em `assets/caption-fixes.json`.
6. **Plano no `reel.json`:** `abertura.imagem` e `abertura.linhas`; cada apoio com `imagem`, `fala` (o trecho literal; o tempo sai sozinho da transcrição) e `duracao`; `cta.texto` (a frase falada) e `cta.fala` (o verbo do pedido, como "comenta aqui"). Imagens em `assets/`, origem de cada uma em `assets/apoios/ORIGENS.md`. Para achar um tempo à mão: `node <S>/ancoras.mjs "frase"` na raiz do projeto.
7. **Montagem:** `node <S>/montar-index.mjs` na raiz do projeto. Ele para com erro quando o plano quebra o estilo (apoio fora de 2 a 3 s, imagem faltando, fala não achada) e avisa palavra sem duração na transcrição: confira essas na escuta. Também escreve `textos-tela.md`.
8. **Texto da tela pela régua da casa** (abaixo).
9. **Olhar antes do render:** `npx hyperframes lint`, depois `npx hyperframes snapshot . --at 2,<meio de cada apoio>,<CTA> --no-end` e OLHE os PNG em `snapshots/`: headline em 2 linhas dentro da faixa, rosto inteiro, legenda fora da boca. Depois `node <S>/renderizar.mjs --rascunho`, `node <S>/mosaico.mjs renders/draft.mp4` e olhe de novo. Por fim `node <S>/renderizar.mjs` gera `renders/<slug>-final.mp4`. Máquina compartilhada: `--workers 2` ou `3`.
10. **Entrega** (em português, curta): caminho do arquivo final, duração, o que foi cortado, imagens usadas e a origem de cada uma, palavras conferidas na escuta e o que ficou incerto. Nunca publique nem envie nada.

O `renderizar.mjs` existe por um defeito medido: renderizado direto em 1080 px, o vídeo da câmera sai com uma faixa preta de 8 px na borda direita. O template usa janela de 1096 px e o script recorta de volta para 1080x1920.

## Texto da tela pela régua da casa

A headline condensa a fala sem trocar o sentido; o CTA repete a fala palavra por palavra.

1. Rode `python3 <S>/lint_copy.py textos-tela.md` (na raiz do projeto) até sair 0. Aviso de lint em fala literal não muda a fala: só anota no relatório.
2. Ponha a headline numa linha só em `conferencia/titulos.txt` e rode `python3 <S>/checar_titulos.py --peca textos-tela.md --titulos conferencia/titulos.txt --insumos assets > conferencia/checagem-titulos.md`. Preencha cada `<preencher>`. Linha que reprovaria por causa de fala literal vira nota ao dono, nunca reescrita.

## Conferências antes de entregar

- `ffprobe`: 1080x1920, 30 fps, áudio presente, duração igual à do `clean.mp4`. O `renderizar.mjs` já imprime e confere a decodificação inteira.
- Snapshot ou mosaico olhado: abertura com uma cena só e headline em 2 linhas na faixa, rosto inteiro no corpo, legenda no peito, três apoios inteiros, CTA legível, só a cor de acento do perfil, borda direita sem faixa preta.
- Cada imagem tem origem anotada em `assets/apoios/ORIGENS.md`, e imagem gerada não é apresentada como prova.
- Toda palavra avisada pelo `montar-index.mjs` foi conferida na escuta, ou ficou como incerta no relatório.

## O que é "pronto"

O MP4 final em `renders/<slug>-final.mp4` passou nas conferências acima, o `textos-tela.md` saiu com lint 0, o `conferencia/checagem-titulos.md` está preenchido sem `<preencher>`, e o relatório no chat diz o caminho, a duração, o que foi cortado, as imagens e a origem delas, o que ficou incerto e o que depende do dono.

## O que esta skill NÃO faz

- O reel cru de celular com prints acima da cabeça: **soft-edicao-yap**.
- O visual serifado de revista: **soft-edicao-yap2**.
- O YAP de websérie com título no quadro 0 e uma versão por gancho: **soft-edicao-yap3**.
- Cenas animadas grandes, encadeadas, que tomam a tela: **soft-edicao-motion**.
- Edição com b-roll, música, cartões e gancho remontado: **soft-editor-video**.
- Escrever o roteiro ou o gancho: **soft-conteudo-reels** e **soft-conteudo-headlines**.
- Publicar, agendar ou enviar o vídeo.

## Arquivos desta skill

- `references/perfil.md`: o esquema do `perfil.json` e onde cada campo aparece neste estilo.
- `scripts/instalar_ambiente.py`: instala sozinho o ambiente da edição e grava `ambiente.json`.
- `scripts/prova_render.py`: prova que a máquina renderiza e transcreve antes de editar.
- `references/ambiente.md`: o passo a passo do ambiente, com saídas e regra dura.
- `scripts/conferir-ambiente.mjs`: confere as dependências e diz como instalar o que faltar.
- `scripts/novo-reel.mjs`: cria o projeto, aplica a identidade do perfil e transcreve (ou importa a transcrição).
- `scripts/transcrever.py`: transcrição local com tempo por palavra (faster-whisper).
- `scripts/cortar.mjs`: corte pelos trechos escolhidos, pausa longa fora, 1,2x, e as palavras na nova linha do tempo.
- `scripts/ancoras.mjs`: tempo de cada frase falada no vídeo limpo.
- `scripts/montar-index.mjs`: abertura, apoios, legenda em grupos e CTA a partir do `reel.json`, com as regras do estilo.
- `scripts/renderizar.mjs`: render sem faixa preta, recortado em 1080x1920.
- `scripts/mosaico.mjs`: um quadro por troca (abertura e apoios), para olhar.
- `scripts/lint_copy.py` e `scripts/checar_titulos.py`: o lint de copy e a régua de títulos da casa.
- `template/index.template.html`: o visual, com cor de acento, fontes e medidas como variáveis.
- `template/fonts/`: Inter Black, Inter Bold e JetBrains Mono, todas OFL 1.1.
- `LICENCAS.md`: o que vem dentro da skill e a licença de cada item.

## Nome do arquivo e lint

Nome de arquivo em minúsculas, sem acento, com hífens. Todo `.md` que a skill entregar passa por `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) antes de ser dado como pronto.
