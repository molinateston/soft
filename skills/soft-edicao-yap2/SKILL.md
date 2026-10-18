---
name: soft-edicao-yap2
description: >-
  Edita a gravação de talking head no Yap 2, estilo editorial: um reel vertical 1080x1920 polido, com uma palavra minúscula por vez no meio do quadro, as palavras-chave em serifado itálico na cor de acento do dono, frases montadas linha a linha, cortes secos entre ângulos e punch-ins, cartões arredondados flutuando com prints reais, nota manuscrita e CTA no fim. Devolve o MP4, a folha de contato conferida e o relatório. Use quando o pedido for: "edita no Yap 2", "edita no estilo editorial", "quero o reel com cara de editado", "estilo serifado", "monta esse vídeo falado com visual de revista". NÃO use pra: o visual cru de celular (soft-edicao-yap, estilo celular); o YAP de websérie com título no quadro 0 e versão por gancho (soft-edicao-yap3); escrever o roteiro ou o gancho (soft-conteudo-reels). Leia e siga o fluxo inteiro do SKILL.md.
---

## Preservar a aparência de cor do bruto (dono, 15/10/2026 20:51)

Ordem explícita: “Corrige ambos então, a skill não pode mexer na cor ok?” Vale para edição completa, ajuste e exportação. Preserve a aparência de cor da gravação original. Sem pedido explícito do dono, não altere brilho, exposição, contraste, saturação ou balanço de branco; não aplique LUT, filtro de cor, embelezamento, retoque de pele nem correção automática. A identidade e a cor de acento das camadas gráficas não autorizam alterar a imagem filmada. Molde aprovado ou vídeo já editado não substitui o bruto como referência de cor.

Conversão técnica de HDR, HLG ou Dolby Vision para o formato de entrega não autoriza mudar a aparência. Antes do lote, inspecione metadados e estabeleça uma reprodução confiável do original, com gerenciamento de cor compatível com o material. Registre arquivo, player ou fluxo de reprodução, espaço de cor e condições conhecidas de comparação. Não trate uma extração crua de valores HLG ou uma prévia sem gerenciamento de cor como referência visual suficiente.

Confira a cadeia inteira, incluindo intermediários, composição e exportação. Os pixels convertidos e as tags de primárias, transferência, matriz e faixa precisam corresponder ao sinal real; trocar apenas tags não corrige a imagem. Nenhum preset de tone mapping, valor de luminância ou escurecimento arbitrário serve como solução universal. A mera ausência de filtro também não prova preservação da aparência.

Antes de entregar, compare o MP4 final decodificado com a reprodução confiável do bruto nos mesmos instantes de origem, mapeados pelos cortes, incluindo início, meio e fim dos trechos usados e mudanças de iluminação. Examine rosto, parede e roupa nas áreas sem sobreposição; confira luminosidade, contraste, cor da pele e saturação. Salve comparações e registre tempos de origem/saída, transformação aplicada, tags e limites da inspeção no relatório. Se a imagem ficar mais clara, lavada, escura ou com outra cor, corrija a cadeia e repita a comparação antes de entregar. Sem referência confiável, declare a pendência e não afirme correspondência visual comprovada. Não prometa identidade matemática entre espaços de cor distintos.

## Contrato de reprodução do molde (15/10/2026)

Antes de escolher fonte ou montar texto, leia [o contrato tipográfico](references/contrato-tipografico.md) e execute `python3 scripts/reproduzir_molde.py <pasta do molde>` (ou com `YAP_MOLDES_DIR`). Um perfil aprovado da mesma série tem prioridade sobre medidas genéricas desta skill. Para ajuste de texto, congele pessoa, ângulo, escala, enquadramento, cortes e áudio. Entregue amostra comparada com o molde antes do lote.



# Yap 2, estilo editorial: o reel que mostra que foi editado

O Yap 2 pega a gravação de uma pessoa falando direto pra câmera e devolve um reel calmo e polido, com cara de revista. É o oposto do visual cru de celular: aqui a edição aparece, e faz parte da mensagem. Cada recurso visual ilustra a palavra exata que está sendo dita, entra nela e sai dentro da mesma frase. Enfeite sem fala por trás é defeito. A skill entra DEPOIS da gravação: aqui é edição, nunca escrita. É marca-neutra: cor de acento, fontes, nome e prints vêm do perfil do dono.

**Origem e honestidade.** O visual vem de um pacote de estilos de edição de terceiro, repassado com a declaração de direito do dono do pacote. Os números de partida (duração alvo, punch-in de 1,2 a 1,35, uma palavra em destaque por frase) são escolha de estilo do pacote, sem medição de retenção por trás: valem como hipótese a confirmar nas métricas do próprio dono.

## A condução: a skill te ajuda a fazer, não só te entrega

Pergunte o modo uma vez, na primeira mensagem: "Eu já edito no modo direto (você manda o bruto e eu monto). Se preferir ser guiado passo a passo, te pergunto uma coisa de cada vez." No silêncio, é o modo direto: pergunte só o que a edição não vive sem. No modo guiado, uma pergunta por vez, dizendo o que precisa, por quê, onde conseguir e o que vem depois:

1. **O bruto:** o arquivo do vídeo e, se houver, os outros ângulos do mesmo take. É o único bloqueio duro: sem o arquivo não há edição. Depois disso vem a identidade.
2. **A identidade** (só na primeira vez, vira o `perfil.json`): cor de acento, fontes, nome, usuário, avatar, logo, seguidores e pasta de prints. Serve para o serifado e o CTA saírem com a cara do dono. Onde conseguir: a cor e as fontes no material de marca dele; o resto no próprio perfil do Instagram. Sem identidade, a edição sai só em branco.
3. **A prova:** prints, telas e capas de reels antigos que sustentam o que a fala afirma, com a origem de cada um. Sem print real, o elemento não entra e a pendência fica anotada.
4. **O CTA:** a palavra literal que o dono fala no fim ("comenta *palavra*"). Uma ação só.

Ensine enquanto faz (uma linha do porquê de cada escolha) e feche oferecendo o ajuste ("quer o corte mais seco, menos serifado, outra cor?").

## Antes de editar: ambiente pronto, instalado por você

Quem prepara a máquina é você, o agente. O dono não instala nada na mão. Esta skill precisa de node 22, ffmpeg, HyperFrames, GSAP, o Chrome do render e a transcrição local. Nos comandos, `<S>` é a pasta `scripts` desta skill e `<pasta>` é a pasta de trabalho da edição. No Windows, troque `python3` por `python`.

1. **Instale:** `python3 <S>/instalar_ambiente.py --perfil hyperframes --pasta <pasta>`. Ele confere o sistema e instala sozinho o que faltar, dentro da pasta sempre que possível. Na primeira vez leva de 3 a 5 minutos; rodar de novo é seguro. Saída 0, ambiente pronto. Saída 3, falta algo que só o dono faz: passe a ele, em uma frase, o comando exato que o instalador imprimiu e espere. Saída 1, 2 ou 4, leia o motivo, rode de novo uma vez e, se repetir, mostre ao dono o passo e o log.
2. **Prove:** `python3 <S>/prova_render.py --perfil hyperframes --pasta <pasta> --audio <vídeo do dono>`. Só a linha `PROVA DE RENDER: OK` libera a edição. Reprovou, diga ao dono qual item falhou e não edite.
3. **Carregue o ambiente em todo comando:** Linux e Mac `. <pasta>/.ambiente/ativar.sh && <comando>`; Windows `call <pasta>\.ambiente\ativar.bat && <comando>`.
4. **Regra dura:** nunca entregue uma edição simplificada por falta de ferramenta. Ou o ambiente prova que renderiza, ou você para e diz o que falta. Cole a linha da prova no relatório.

O passo a passo completo, com a tabela de estados e as saídas, está em `references/ambiente.md`.

## O perfil do dono (`perfil.json`)

Fica na pasta de trabalho e vale para todas as edições. Procure antes de perguntar. Se não existir, pergunte UMA vez, numa mensagem só, e salve a partir de `template/perfil.exemplo.json`:

| Campo | O que é | Onde este estilo usa |
|---|---|---|
| `nome`, `usuario`, `nicho`, `seguidores` | como aparecem no perfil | CTA e qualquer tela que mostre o perfil |
| `avatar`, `logo` | caminho do arquivo (relativo ao perfil.json ou absoluto) | só se o dono pedir na tela |
| `cor_acento` | `#RRGGBB` | o serifado das palavras-chave e das pilhas; vazio = branco |
| `fonte_texto` | arquivo .woff2, .woff, .ttf ou .otf da sans do dono | legenda e linhas sans; vazio = Inter (livre, vem na skill) |
| `fonte_destaque` | arquivo da serifada itálica do dono | palavras-chave; vazio = Instrument Serif Italic (livre, vem na skill) |
| `pasta_prints` | onde o dono guarda prints | `listar-prints.mjs` |

Nunca invente número, logo, capa ou print. Se faltar algo, peça ao dono o arquivo exato. Fonte do dono só entra se ele tiver a licença dela.

## Regras de partida (o dono pode mudar qualquer uma; registre a mudança no relatório)

1. **Uma cor de acento só**, a do perfil, e só no serifado. Sem identidade declarada, tudo em branco.
2. **Mais ou menos uma palavra no serifado por frase.** Mais que isso e o destaque perde o sentido.
3. **Corte sem pausa e sem erro.** Toda pausa medida sai (-30 dB, 0,15 s) e todo take repetido sai. Alvo de 35 a 60 s, teto de 90 s.
4. **Câmera só em corte seco**, a cada uma ou duas frases. Zoom animado, nunca.
5. **Nada cobre o rosto.** Cartões ao lado ou acima da cabeça, no máximo 2 ao mesmo tempo.
6. **Texto literal ao que foi falado.** Pilha, nota e CTA repetem a fala, não resumem.
7. **Export 1080x1920, 30 fps, com áudio, menos de 300 MB, arquivo íntegro.**
8. **Não publique, não envie e não use serviço pago sem pedido explícito.** Print só com origem conhecida e permissão do dono para expor. Nunca simule resultado nem tela de ferramenta.

## O visual em resumo

Legenda de uma palavra minúscula no meio do quadro (sans 92 px, sombra suave, sem contorno) · palavra-chave em serifado itálico 124 px na cor de acento · pilhas de frase montadas linha a linha no terço de cima · cortes secos entre ângulos e punch-ins · cartões arredondados (34 px de raio) com print real · explosão de miniaturas, faixa de filme e parede de grade com capas do dono · uma nota manuscrita com seta desenhada por vídeo · até 2 momentos de interface · CTA no enquadramento mais fechado. Cores, tamanhos e o que não fazer: `template/DESIGN.md` (vai para cada projeto). Cada elemento, quando usar e como montar: `references/elementos-e-tempos.md`.

## Fluxo (rode na pasta de trabalho do dono)

`S=<pasta desta skill>/scripts`. Os comandos são iguais no terminal do Linux, do Mac e no PowerShell.

1. **Projeto e transcrição:** `node $S/novo-reel.mjs "<video>" <slug> ["<angulo2>" ...]`. Cria `projetos-video/<slug>/` com o bruto em 1080x1920 a 30 fps, a transcrição e `assets/palavras.txt` (as palavras com tempo e as pausas).
2. **Enquadramento** (deste passo em diante, na pasta do projeto): `node $S/mosaico.mjs assets/bruto.mp4`; escolha a altura da legenda (entre 1150 e 1400, padrão 1330, no peito; o topo da legenda fica pelo menos 40 px abaixo do queixo, inclusive no punch-in) e grave `ajustes.json` com `{"altura_legenda": <px>}`.
3. **Corte:** escreva `assets/trechos.json` com os trechos que ficam (o melhor take de cada frase) e, dentro de `assets/`, rode `node $S/cortar.mjs`. Sai `limpo.mp4` e `cortes.json`. Outros ângulos: sincronize com o bruto, apare no mesmo início e rode `node $S/cortar.mjs --angulo angulo2.mp4`.
4. **Conferência do corte:** transcreva o limpo (`"$WHISPER_PYTHON" $S/transcrever.py limpo.mp4 transcricao.json --model medium` dentro de `assets/`) e leia de ponta a ponta. Sobrou pausa ou repetição, volte ao passo 3. Palavra mal ouvida vai para `assets/correcoes.json`.
5. **Plano de batidas** em `assets/batidas.md`: por frase, um recurso, a câmera e a palavra no serifado. Regras em `references/elementos-e-tempos.md`.
6. **Material:** prints com `node $S/listar-prints.mjs "<termo>"` (abra cada candidato) para `assets/prints/`; capas de reels antigos do dono para `assets/thumbs/`. Origem de cada arquivo em `assets/prints/ORIGEM.md`.
7. **Composição:** em `src/index.template.html`, adapte os elementos e escreva o bloco de tempos com as funções do template. Tempos com `node $S/ancoras.mjs "frase" ...`. Escreva `assets/destaques.json`.
8. **Montagem e rascunho:** `node $S/montar-index.mjs` e depois `node $S/renderizar.mjs --rascunho`. Puxe quadros em cada batida com `node $S/mosaico.mjs renders/<slug>-rascunho.mp4 --tempos <lista>` e OLHE (lista no fim da referência).
9. **Textos na tela:** `conferencia/textos-na-tela.md` com tempo, elemento, texto literal e a fala de origem; rode a régua (seção abaixo).
10. **Final:** `node $S/renderizar.mjs --final`. Sai `renders/<slug>-final.mp4` já conferido.

## Régua do texto na tela

Todo texto que aparece escrito (linhas de pilha, nota, cartão escuro, CTA) vai para `conferencia/textos-na-tela.md` e passa por:

- `python3 <pasta desta skill>/scripts/lint_copy.py conferencia/textos-na-tela.md` (exit 0). Aviso em fala literal não muda a fala: só anota no relatório.
- As linhas de abertura e o CTA vão, uma por linha, para `conferencia/titulos.txt`, e a transcrição limpa em texto vai para uma pasta de insumos. Rode `python3 <pasta desta skill>/scripts/checar_titulos.py --peca conferencia/textos-na-tela.md --titulos conferencia/titulos.txt --insumos <pasta com a transcrição>` e cole o bloco que sai em `conferencia/checagem-titulos.md`, preenchendo cada `<preencher>`. Ele confere caixa alta, nome de pessoa e a palavra do CTA contra a fala real.

## O que é "pronto"

- `renderizar.mjs --final` saiu com todas as linhas `ok`: 1080x1920, 30 fps, áudio, menos de 300 MB, arquivo íntegro, borda direita sem faixa preta.
- Folha de contato do final (0, 1, 3 s e a cada 5 s, mais um quadro em cada batida) olhada: rosto livre, serifado legível na cor certa, nada cortado na borda.
- Assistido do início ao fim como espectador: nenhuma pausa sobrando, nenhuma palavra comida na emenda, cada elemento entrando na palavra e saindo na frase.
- Lint dos textos com exit 0 e checagem de títulos preenchida.
- Relatório entregue.

## Entrega

A pasta do projeto com `renders/<slug>-final.mp4`, `conferencia/` (mosaicos, textos na tela, checagem) e `relatorio.md`: o que foi cortado, o plano de batidas, o material usado com a origem, as regras de partida que o dono mudou, o que ficou incerto e o que depende dele. No chat: o caminho do MP4, a duração, o tamanho e as pendências. Cada caminho em linha isolada. Feche oferecendo o ajuste.

## O que esta skill NÃO faz

- O visual cru de celular, sem serifado: **soft-edicao-yap** (estilo celular).
- O YAP de websérie com título no quadro 0 e uma versão por gancho: **soft-edicao-yap3**.
- Escrever ou corrigir o roteiro e o gancho: **soft-conteudo-reels**.
- Publicar, agendar ou enviar o vídeo.
- Criar print, número ou depoimento que o dono não tem.

## Arquivos desta skill

- `references/elementos-e-tempos.md`: cada elemento, quando usar, como montar, o plano de batidas e o que olhar nos quadros.
- `template/index.template.html`: a composição com as funções de tempo; `template/DESIGN.md`: cores, tipos e o que não fazer; `template/perfil.exemplo.json`: o esquema do perfil.
- `template/fonts/`: Inter, Instrument Serif Italic e Caveat, todas OFL, com as licenças ao lado.
- `scripts/instalar_ambiente.py`: instala sozinho o ambiente da edição e grava `ambiente.json`.
- `scripts/prova_render.py`: prova que a máquina renderiza e transcreve antes de editar.
- `references/ambiente.md`: o passo a passo do ambiente, com saídas e regra dura.
- `scripts/conferir.mjs`: confere as dependências e o perfil.
- `scripts/novo-reel.mjs`, `cortar.mjs`, `transcrever.py`, `ancoras.mjs`, `montar-index.mjs`, `renderizar.mjs`, `mosaico.mjs`, `listar-prints.mjs`, `ferramentas.mjs`: o fluxo acima.
- `scripts/lint_copy.py` e `scripts/checar_titulos.py`: a régua da casa para o texto na tela.
- `LICENCAS.md`: o que vem dentro e a licença de cada item.

## Nome do arquivo e lint

Nome de arquivo e slug em minúsculas, sem acento, com hífens. Todo `.md` que a skill entregar passa por `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) antes de ser dado como pronto.


## Nova edição completa e correção de fluidez, 15/10/2026 16:02

A ordem de congelar pessoa, ângulo e áudio aplica-se a ajuste restrito de posição de texto. Uma nova edição completa autorizada volta ao bruto e decide cortes, aproximações, recuos, sons e apoios pela fala; não herda o corpo rejeitado como pronto. Preserve a identidade deste estilo e a prioridade do perfil aprovado da série.

Antes de renderizar, salve mapa por fala com: intervalo do bruto, frase literal, tentativa descartada e retomada escolhida, tempo de saída, função tipográfica, arquivo de fonte, câmera inicial/final e motivo, apoio e sua origem, som e instante de entrada. Detecte repetições, gagueiras, início abortado e autocorreção na transcrição com palavras temporizadas. Compare as tentativas no áudio; mantenha a retomada mais fluida e remova a primeira tentativa quando ela for erro. Não corte uma repetição intencional só porque a palavra repete. Transcrição automática sozinha não prova emenda fonética: confira bordas, consoantes, respiração e continuidade; documente tempos antes/depois e incerteza real. Guarde bordas de áudio suficientes para preservar a sílaba, em vez de cortar exatamente no timestamp estimado de palavra.

Varie a tipografia por função dentro dos pares comprovados do estilo: título, complemento/contraponto e legenda não são uma camada indiferenciada. Leia o perfil e referências locais; registre caminho e hash das fontes e falhe se o arquivo não carregar. Não invente fonte nem use fallback silencioso. No perfil Manuscrito (ep2), a referência local é Advercase Bold85 para título, Kalam Bold54 para complemento e Advercase72 para legenda; topo315 e folga de30px do recorte4:5. Esse perfil não substitui a identidade celular ou editorial de outro pedido.

Planeje sons nas entradas motivadas de texto, lista, demonstração, comparação ou ênfase; sincronize o som ao evento e mantenha a voz dominante. A reclamação de poucos sons exige rever oportunidades concretas, não preencher uma cota. Aproximação gradual pode sustentar uma fala que cresce em importância; recuo precisa de motivo próprio, como abrir área para lista ou iniciar etapa. Registre escala e duração, preserve continuidade em cortes de limpeza e permita permanência. Não alternar zoom in/out por índice, por intervalo fixo nem por obrigação de variar.

Escolha elementos pertinentes aos substantivos, ações e relações da fala: lista progressiva, número, contraste, seta ou demonstração real quando houver fonte. Não invente prova ou resultado. Audite cada estado no feed9:16 e recortes4:5/3:4, olhos e boca livres, título e complemento com hierarquia e sem palavra órfã. Confira duração final até90s, CTA literal completo, cortes, áudio/canais/truepeak e decodificação integral. Declare exatamente o que foi executado; não alegue escuta humana ou revisão independente inexistente. Sem música, EQ, compressor ou limiter nesta correção do dono.


## Refinamento de fluidez, elementos e câmera, 15/10/2026 17:11

O dono elogiou a direção visual da v1 e pediu outra edição completa: ainda havia erros/gaguejos e faltavam GIFs pertinentes e jogo de câmera perceptível. Elogio com ressalva não representa aprovação integral. Leia `references/revisao-fluidez-elementos-camera-2026-10-15.md` ao executar esse refinamento. Respeite a identidade própria desta skill.

ASR é mapa, não revisão fonética: pode normalizar sílabas repetidas, falsos começos e muletas. Faça varredura de todas as frases selecionadas, incluindo respirações e as emendas internas, em vez de conferir apenas os erros já apontados. Examine áudio quando a ferramenta permitir; na ausência de escuta, combine janelas curtas sobrepostas, análise acústica e margem de fonema, registre a limitação e nunca declare todos os gaguejos removidos só porque a transcrição está limpa. Compare candidatos por fluidez, preserve a retomada literal mais completa e mantenha o CTA até o último fonema. Acelerar não corrige gaguejo; esta nova tentativa do EP2 usa velocidade natural.

GIF/figurinha animada é recurso opcional, escolhido pelo substantivo, ação ou reação da fala. Demonstre que o arquivo anima no render, entra na palavra e sai com a troca do assunto. Identifique ilustração criada como ilustração; não use animação ou imagem genérica como prova de resultado. Falta de fonte real para contrato ou valor permanece limite, nunca vira print inventado.

Para câmera, a prova é o MP4 decodificado: compare começo/meio/fim de cada trajetória com a imagem fonte, além das duas bordas de cada emenda. Meça ou mostre escala/posição realmente realizadas; registre inversão, tremor, reset ou ausência de progressão. Trocar algoritmo exige repetir a prova curta do movimento. Push-in lento deve ser perceptível e terminar antes da fala para permitir permanência; recuo e punch precisam de motivo próprio. Preserve escala e posição em cortes de limpeza. Não alternar automaticamente por corte. Abertura estática permanece. Nova edição completa autoriza esses movimentos; take fixo de um ajuste de texto não congela uma edição posterior autorizada.
