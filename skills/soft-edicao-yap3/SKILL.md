---
name: soft-edicao-yap3
description: >-
  Edita um YAP, o vídeo de talking head falado direto pra câmera (episódio de websérie, vídeo solto ou spin-off), do bruto ao arquivo 1080x1920 pronto: cortes sem respiro, título no primeiro quadro, textos e listas na palavra, prova em print, câmera parada com aproximação só quando a fala pede, legenda de uma palavra quando pedida e sons marcando cada elemento. Também monta o briefing pro editor (agente ou pessoa), exporta uma versão por gancho com o mesmo corpo e confere a edição antes de entregar. Use quando o pedido for: "edita esse YAP", "edita o episódio da websérie", "monta o briefing de edição do meu vídeo falado", "exporta uma versão por gancho", "confere essa edição antes de eu postar". NÃO use pra: escrever o roteiro ou o gancho (soft-conteudo-reels, soft-conteudo-ganchos); editar gravação com b-roll e cartões (soft-editor-video); reel mudo de 7 segundos (soft-reel-7seg). Leia e siga o fluxo inteiro do SKILL.md.
---

## Preservar a aparência de cor do bruto (dono, 15/10/2026 20:51)

Ordem explícita: “Corrige ambos então, a skill não pode mexer na cor ok?” Vale para edição completa, ajuste e exportação. Preserve a aparência de cor da gravação original. Sem pedido explícito do dono, não altere brilho, exposição, contraste, saturação ou balanço de branco; não aplique LUT, filtro de cor, embelezamento, retoque de pele nem correção automática. A identidade e a cor de acento das camadas gráficas não autorizam alterar a imagem filmada. Molde aprovado ou vídeo já editado não substitui o bruto como referência de cor.

Conversão técnica de HDR, HLG ou Dolby Vision para o formato de entrega não autoriza mudar a aparência. Antes do lote, inspecione metadados e estabeleça uma reprodução confiável do original, com gerenciamento de cor compatível com o material. Registre arquivo, player ou fluxo de reprodução, espaço de cor e condições conhecidas de comparação. Não trate uma extração crua de valores HLG ou uma prévia sem gerenciamento de cor como referência visual suficiente.

Confira a cadeia inteira, incluindo intermediários, composição e exportação. Os pixels convertidos e as tags de primárias, transferência, matriz e faixa precisam corresponder ao sinal real; trocar apenas tags não corrige a imagem. Nenhum preset de tone mapping, valor de luminância ou escurecimento arbitrário serve como solução universal. A mera ausência de filtro também não prova preservação da aparência.

Antes de entregar, compare o MP4 final decodificado com a reprodução confiável do bruto nos mesmos instantes de origem, mapeados pelos cortes, incluindo início, meio e fim dos trechos usados e mudanças de iluminação. Examine rosto, parede e roupa nas áreas sem sobreposição; confira luminosidade, contraste, cor da pele e saturação. Salve comparações e registre tempos de origem/saída, transformação aplicada, tags e limites da inspeção no relatório. Se a imagem ficar mais clara, lavada, escura ou com outra cor, corrija a cadeia e repita a comparação antes de entregar. Sem referência confiável, declare a pendência e não afirme correspondência visual comprovada. Não prometa identidade matemática entre espaços de cor distintos.

## Contrato de reprodução do molde (15/10/2026)

Antes de escolher fonte ou montar texto, leia [o contrato tipográfico](references/contrato-tipografico.md) e execute `python3 scripts/reproduzir_molde.py --fontes <pasta das fontes>` (sem `--fontes`, procura em `assets/fontes`). Um perfil aprovado da mesma série tem prioridade sobre medidas genéricas desta skill. Para ajuste de texto, congele pessoa, ângulo, escala, enquadramento, cortes e áudio. Entregue amostra comparada com o molde antes do lote.



# Edição de YAP: do bruto ao vídeo que prende do início ao fim

YAP é o vídeo de uma pessoa falando direto pra câmera, sem cenário montado. Esta skill pega o bruto (e o que existir de prova: prints, telas, fotos) e devolve o MP4 vertical pronto, mais o relatório do que foi feito e conferido. Ela entra DEPOIS que o roteiro e a gravação existem: aqui é edição, nunca escrita. É marca-neutra: a identidade (cor de acento, fonte, logo) vem do perfil do dono, e cada cliente roda com a própria.

**Origem e honestidade.** O método vem de um curso de edição de YAP e da medição de 19 reels de um perfil de nicho (amostra de uma conta, estudo por quadros, retenção não medida). O que está marcado "medido" descreve aquela amostra: é referência, não meta nem cota. Tudo o que a skill afirma sobre "o que prende" é a melhor leitura conhecida, e vale como hipótese a confirmar nas métricas do próprio dono.

## A condução: a skill te ajuda a fazer, não só te entrega

Pergunte o modo uma vez, na primeira mensagem: "Eu já edito no modo direto (você manda o bruto e eu monto). Se preferir ser guiado passo a passo, te pergunto uma coisa de cada vez." No silêncio, é o modo direto: pergunte só o que a edição não vive sem. No modo guiado, uma pergunta por vez, dizendo o que precisa, por quê, onde conseguir e o que vem depois:

1. **O bruto:** o arquivo do vídeo e quantos ganchos foram gravados e onde estão. É o único bloqueio duro: sem o arquivo não há edição.
2. **A identidade:** a cor de acento, a fonte e o logo do perfil do dono. Sem identidade declarada, só branco, sem cor de acento.
3. **O CTA:** a frase literal, uma ação só.
4. **A prova:** prints, telas ou números que sustentam cada afirmação forte, com a origem. Sem print real, a edição usa o número em texto e deixa a pendência anotada.

Ensine enquanto faz (uma linha do porquê de cada escolha) e feche oferecendo o ajuste ("quer o corte mais seco, o texto maior, outra cor?").

## Antes de editar: ambiente pronto, instalado por você

Quem prepara a máquina é você, o agente. O dono não instala nada na mão. Esta skill precisa de ffmpeg, ffprobe, a transcrição local (faster-whisper) e os pacotes Python dos scripts de GIF e de variação (numpy, Pillow e OpenCV), que o instalador põe no venv da pasta e prova importando. Nos comandos, `<S>` é a pasta `scripts` desta skill e `<pasta>` é a pasta de trabalho da edição. No Windows, troque `python3` por `python`.

1. **Instale:** `python3 <S>/instalar_ambiente.py --perfil ffmpeg --pasta <pasta>`. Ele confere o sistema e instala sozinho o que faltar, dentro da pasta sempre que possível. Na primeira vez leva de 3 a 5 minutos; rodar de novo é seguro. Saída 0, ambiente pronto. Saída 3, falta algo que só o dono faz: passe a ele, em uma frase, o comando exato que o instalador imprimiu e espere. Saída 1, 2 ou 4, leia o motivo, rode de novo uma vez e, se repetir, mostre ao dono o passo e o log.
2. **Prove:** `python3 <S>/prova_render.py --perfil ffmpeg --pasta <pasta> --audio <vídeo do dono>`. Só a linha `PROVA DE RENDER: OK` libera a edição. Reprovou, diga ao dono qual item falhou e não edite.
3. **Carregue o ambiente em todo comando:** Linux e Mac `. <pasta>/.ambiente/ativar.sh && <comando>`; Windows `call <pasta>\.ambiente\ativar.bat && <comando>`. Ele põe na frente um `python3` que usa o venv da pasta; sem ele, os scripts de GIF e de variação param no import.
4. **Regra dura:** nunca entregue uma edição simplificada por falta de ferramenta. Ou o ambiente prova que renderiza, ou você para e diz o que falta. Cole a linha da prova no relatório.

O passo a passo completo, com a tabela de estados e as saídas, está em `references/ambiente.md`.

## Regras de partida (o dono pode mudar qualquer uma; registre a mudança no relatório)

1. **Uma cor de acento só**, a da identidade do dono. Na legenda não há destaque colorido.
2. **Preservar a voz e a fala.** Velocidade padrão 1,1x preservando o tom (`atempo=1.1`), com o ok do dono; 1,2x só se a fala continuar clara; fala já rápida não acelera. Sem compressão, sem EQ, sem troca de take por IA. O som de efeito entra por baixo da fala, nunca no lugar dela. Única exceção: um ganho linear uniforme e pequeno (até -2 dB) no master inteiro, só para o pico ficar em -1 dBTP ou menos, anotado no relatório.
3. **O vídeo não começa com motion.** Título em texto já no quadro 0, sim. Animação de abertura, vinheta, zoom de keyframe ou texto entrando animado no primeiro plano, não.
4. **Export 1080x1920, 30 fps, menos de 300 MB, arquivo íntegro** (`ffmpeg -v error -i X -f null -` sem saída).
5. **Título e legenda literais ao que foi falado.** Não resuma o gancho. Ajuste exclusivo de posição move só a camada de texto e preserva apresentador, ângulo, escala, enquadramento, fundo, cortes, áudio, velocidade e PNG original (tamanho, palavras e quebras). Aplicar o molde aprovado em `references/texto-legenda-elementos.md`.
6. **Não publique, não envie e não use serviço pago sem pedido explícito.** Print só com origem conhecida e permissão do dono para expor. Nunca simule resultado financeiro nem invente prova.

## Ordem de edição

1. **Briefing** (modelo no fim). Sem briefing, não monta.
2. **Transcrição com tempo por palavra**: serve de mapa para os cortes. Local com `faster-whisper`, ou serviço de transcrição só se o pedido autorizar. Some a detecção de silêncio (`silencedetect=-38dB:d=0.10`) para as bordas.
3. **Cortes.** Depois de cortar, a legenda-mapa sai e só volta no fim.
4. **Textos e título.**
5. **Elementos** (prints, emojis, figurinhas).
6. **Movimento** (zoom e posição).
7. **Legenda de uma palavra**, por último, e só se o dono pediu.
8. **Sons.**
9. **Conferência** "me prende do início ao fim" e a lista técnica.
10. **Amostra antes das variantes.** Exporte primeiro UMA versão normal completa e mostre ao dono em vídeo. Só depois da avaliação derive os demais ganchos e as versões espelhadas autorizadas.

O GIF de meme com som entra sobre o arquivo final de cada gancho, depois do export e antes da conferência (seção "GIF de meme + som").

### Ordem ponta a ponta de um episódio YAP3 (EP3 e EP4, 16/10/2026)

`<S>` é a pasta `scripts/` desta skill. Cada passo só começa com o anterior aprovado.

1. **Bruto:** cópia em `bruto/`. Transcrição geral; depois `python3 <S>/transcrever_tomadas.py` (large-v3 offline, por palavra) só nas tomadas candidatas a gancho e `python3 <S>/cortes_tomadas.py` para os limites exatos de cada tomada (`f0` e `n_h`).
2. **Edição:** a V3 normal completa (gancho principal + corpo) pela "Ordem de edição" acima, letra branca em `GRAF_BRANCO=1000`.
3. **Amostra:** UMA versão normal completa para o dono avaliar em vídeo. Sem avaliação, não deriva nada.
4. **Variantes e espelho:** `python3 <S>/variar_gancho.py prefixo|final <plano.json> [--espelho]` (seção "Variações de gancho e espelho"), depois `python3 <S>/auditar_variacao.py <plano.json> <final.mp4> [--espelho]` em cada final até APROVADO.
5. **GIF de meme + som:** escolha dos memes contra os já usados (`python3 <S>/memes_usados.py ver`), `pico_gif.py`, `ganho_uniforme.py` se preciso, `planos_gif_lote.py` e `lote_gif.sh` (seção "GIF de meme + som").
6. **Auditoria por vídeo e do lote:** `verificar_gif.py` e `auditar_gif_meme.py` em cada final (o `lote_gif.sh` já roda os dois), depois `python3 <S>/mosaico_geral.py <pasta_verif> mosaico-geral.png` e olhar o lote inteiro.
7. **Entrega:** seção "Entrega".

A prioridade é velocidade com critério: edição boa e rápida vence edição perfeita e lenta. Mesmo assim a conferência técnica do fim é obrigatória.

## Cortes

- **Sem espaço, sem brecha, sem respiro, sem erro.** Tire silêncio, respiração, erro e repetição. Do take repetido, fica o melhor, e o plano anota qual e por quê.
- **Pausa só se for intencional** (um respiro de drama). Silêncio acidental sai.
- **Medido:** mediana de 5 cortes por 30 s e plano mediano de 4,3 s. Num YAP de corte seco por respiro o número de cortes sai maior, e tudo bem.
- **Corte em fronteira de quadro:** `round(t*30)/30`. Deixe 30 a 60 ms antes da primeira sílaba e corte até 30 ms depois da última, sem comer consoante final. Escute a emenda.
- **Micro-fade de áudio de 4 ms** em cada borda de segmento (`afade=t=in:d=0.004`, `afade=t=out:st=dur-0.004:d=0.004`) contra clique. Não muda a voz.
- **Gancho regravado:** procure na transcrição todas as repetições do gancho. Havendo um take limpo inteiro, use-o em vez de remendar trechos de takes diferentes.

## Textos, elementos, legenda, câmera e sons

O detalhe de cada um mora em duas referências. Leia a certa antes de montar essa camada:

- `references/texto-legenda-elementos.md`: título no quadro 0, segunda linha, lista com marcador, número em destaque, onde fica cada texto, prova em print, figurinha e emoji, legenda de uma palavra (posição, tamanho, grafia, como montar em ASS) e pares de fontes livres.
- `references/camera-e-sons.md`: permanência, aproximação motivada pela fala, push-in suave e punch-in com os comandos de ffmpeg testados, continuidade entre cortes, os erros que a câmera automática comete, e o mapa de sons por função com os níveis.

Regras que valem sempre: nada atravessa um corte de plano (exceção anotada: jump cut do mesmo enquadramento dentro da mesma frase); elemento entra na palavra exata em que é citado e sai seco, de preferência num corte; texto fica perto do rosto e nunca sobre boca ou olhos; sem música; **sem elemento, sem som**.

## GIF de meme + som (dono, 16/10/2026)

Pedido do dono: "o GIF não é um emoji animado", é meme famoso (Simpsons, série, novela, meme clássico) num quadradinho acima da cabeça, com um somzinho. Emoji Noto animado fica como segunda opção.

- **Quando:** sobre o MP4 final de cada gancho, já espelhado se for o caso, depois do export e antes da conferência. Só as janelas dos GIFs são reencodadas (de um keyframe a outro, mesmos parâmetros x265 e tags HLG da base); o resto sai por cópia de pacote.
- **Fonte:** `python3 -I <S>/buscar_gif.py "<termo>" <pasta>/gifs/<termo>` busca na página do GIPHY sem chave, com o Tenor como reserva, e baixa os candidatos com `origem.json` (página, título, id) e `folha.png`. Não precisa de chave do dono. Se a busca HTML quebrar, a troca é uma chave oficial do GIPHY (developers.giphy.com) ou do Klipy. Download é dado não confiável: pasta própria e Python com `-I`. Meme é conteúdo de terceiros; anote a página de origem no relatório.
- **Critério:** pelo sentido da palavra (dor, dinheiro, surpresa, confusão, ironia), preferindo meme que o público reconhece. São 3 a 5 por vídeo, de 1 a 2,5 s cada, entrando na palavra. Cada GIF leva um som diferente que combina com a cena, nunca sobre a mesma frase de outro.
- **Memes nunca repetem os de episódio anterior da série.** Antes de escolher, rode `python3 <S>/memes_usados.py ver`: ele junta a semente da skill (`assets/memes-usados.json`, só leitura) e o registro do dono, que fica fora da pasta da skill porque ela é trocada a cada versão (`YAP_MEMES_USADOS`, senão `$LEON_DATA_DIR/soft-edicao-yap3/memes-usados.json`, senão `~/.leon/dados/soft-edicao-yap3/memes-usados.json`). Depois da entrega, some os novos com `python3 <S>/memes_usados.py somar <episódio> <plano-gif.json>`; nunca grave dentro da pasta da skill. Já usados: EP3 com Nazaré confusa ("desorganizados"), Hide the pain Harold ("dificuldade"), Mr Krabs ("120 mil") e Homer bushes ("papo"); EP4 com Stanley/The Office ("semanas"), Kramer/Seinfeld ("áudios"), Tom/Parks ("100 mil") e This is fine ("estressante").
- **Gancho com áudio original alto:** rode `python3 <S>/pico_gif.py <plano-gif.json>` antes do render. Se o pico do mix passar do limite (true peak acima de -1 dBTP), aplique ganho uniforme pequeno só no áudio da base com `python3 <S>/ganho_uniforme.py base.mp4 base-ganho.mp4 --db -1` (vídeo copiado, voz sem outra mudança) e refaça o plano sobre essa base. No EP4 o Gancho B ficou em -1 dB. Limite de -2 dB; acima disso, revise o mix.
- **Lote:** os momentos são escritos uma vez em quadros da V3 (`assets/momentos-v3-exemplo-ep4.json`) e `python3 <S>/planos_gif_lote.py` gera um `plano-gif.json` por final (ganchos x normal/espelho), deslocando pelo tamanho de cada gancho. `bash <S>/lote_gif.sh <planos.json> <pasta_verif>` faz render, verificação e auditoria de cada final e imprime `<nome> verif=APROVADO audit=APROVADO`.
- **Posição e tamanho:** cartão de 272 px de altura com a base fixa em y=300, acima da primeira linha de título, centrado em x e com até 500 px de largura. Borda branca de 5 px, cantos com raio 28 e GIF recortado em cover. A entrada é um pop de 6 quadros que cresce para cima, e a saída encolhe em 5. Pode cobrir de 0 a 1 px de letra, e nunca o rosto.
- **Som:** a biblioteca fica em `assets/sons-gif/`, com origem e licença em `sons.json` (sintetizada por `sfx_gif.py`, obra própria, CC0). O pop de entrada fica em -12 dB e o sting em -1 dB do p90 da voz, com teto de pico de -6 dBFS por efeito. O true peak final precisa ficar em -1 dBTP ou menos, e a voz não muda.
- **Espelho:** espelhe só o apresentador, no export. O GIF é aplicado depois e nunca é invertido (letreiro e rosto do meme ficam legíveis).
- **Render:** `python3 -I <S>/gif_meme.py <pasta>/plano-gif.json` (modelo em `assets/plano-gif-exemplo.json`; `--so-audio` refaz só a mixagem).
- **Conferência:** `python3 <S>/verificar_gif.py <pasta>/plano-gif.json <pasta>/final/conferencia` até APROVADO (decode, tags, pacotes fora das janelas iguais à base, letra coberta, rosto, null test, true peak e sincronia). Depois abra o `mosaico.png` e o `pop.png` e confira a cor, a legibilidade e a invasão de texto.
- **Auditoria por vídeo:** `python3 <S>/auditar_gif_meme.py <plano-gif.json> <pasta_verif>` até APROVADO (PTS do áudio, duração A/V, sincronia com o mix da V3 dentro e fora das janelas, rosto medido por YuNet com `rosto.py` contra a borda do cartão, letra x GIF).

## Conferência "me prende do início ao fim"

Assista do início ao fim como espectador. Perguntas:

- O gancho prende antes de 1 s? Título no quadro 0, sem motion?
- Sobrou respiro, brecha, erro ou repetição? Alguma palavra comida na emenda?
- Cada afirmação forte tem prova (ou pendência anotada)?
- A fala sustenta os trechos de permanência? Duração acima de 8 s sem recurso não obriga zoom, texto ou elemento.
- Cada movimento tem motivo na fala? Há aproximação seguida de recuo automático, ou direção invertida em todo corte? Se houver, refaça o mapa de câmera.
- Algum elemento atravessa corte? Algum som sem elemento?
- O CTA é uma ação só (por exemplo, "me segue para o episódio 2")?

## Conferências técnicas antes de entregar

- `ffprobe`: 1080x1920, 30 fps, áudio presente, duração e tamanho abaixo de 300 MB. E `ffmpeg -v error -i X -f null -` sem saída.
- **Folha de contato por versão** (quadros em 0, 1, 3 s e a cada 5 s): título no quadro 0, nenhuma animação de abertura (quadros 0 e 1 iguais no fundo), legenda legível, só a cor de acento da identidade, nada cortado na borda.
- **Recortes do feed:** aplicar a área de texto e a conferência integral em `references/texto-legenda-elementos.md`, com mosaico 9:16, 4:5 e 3:4 dos maiores estados de texto e CTA. Texto cortado reprova a entrega.
- **Câmera:** confira a trajetória de escala e posição no arquivo final. Examine pares antes e depois dos cortes e a sequência em tempo real: quadro isolado não valida conforto de movimento. Anote se só foi possível examinar quadros.
- **Emenda gancho → corpo:** quadros n-1 e n e escuta de 2 s em volta (sem respiro, sem palavra comida).
- **Entrada de cada elemento:** quadros n-1 e n.
- **Sincronia do som:** atraso do efeito em relação ao elemento de 0 a 2 quadros.
- **Voz intacta:** diferença entre o áudio editado e o mesmo mix sem efeitos, fora das janelas dos efeitos, perto do ruído do reencode.
- **Loudness e pico:** `ebur128=peak=true`, true peak -1,0 dBTP ou menos.
- **Corpo idêntico entre versões:** o hash dos quadros do corpo (`framemd5` no trecho) é igual nas N versões, ou o intermediário concatenado é o mesmo.
- **Texto literal à fala.** Rode o lint de copy desta skill sobre o arquivo com os textos (`python3 scripts/lint_copy.py <arquivo>`). Aviso de lint em fala literal não muda a fala: só anota.
- **Auditoria do lote inteiro antes de entregar:** com todos os finais aprovados um a um, `python3 <S>/mosaico_geral.py <pasta_verif> mosaico-geral.png` junta o mosaico de cada final num PNG só. Abra e olhe todos lado a lado: cor igual entre versões, espelho só no apresentador, GIF legível e nunca invertido, título e legenda no lugar. Um final fora do padrão reprova o lote até ser refeito.

## Export de uma versão por gancho

Quando o dono grava N ganchos (no início e/ou no fim do bruto), sai **um MP4 por gancho, com um único gancho cada**, e o **corpo é idêntico** em todos.

1. **Preparação:** segmentos pela regra de silêncio (fim = `ceil((s+0.04)*30)`, início = `floor((e-0.04)*30)`), mapa de tempo bruto → saída, áudio a 48 kHz com 1600 amostras por quadro e fade de 4 ms, efeitos calibrados pelo p90 da voz, ganho uniforme do master para true peak -1,5 dBTP.
2. **Corpo:** renderizado **uma vez**, numa passada (`select` dos quadros dos segmentos, `setpts=N/30/TB`, conversão de faixa de cor para limitada, câmera por partes, overlay dos textos e legenda).
3. **Ganchos:** um clipe por gancho com os mesmos parâmetros de codec (plano estático, título literal no quadro 0, legenda, som do quadro 0).
4. **Final:** concatene gancho e corpo com `-c:v copy` (o corpo sai bit a bit igual nas versões) e junte o áudio da versão em AAC 192k 48 kHz, `+faststart`.

Nome: `ep<N>-v<k>-<tipo-ou-3-palavras-do-gancho>.mp4` (v1 = gancho do início do bruto). A apresentação do corpo ("Meu nome é...") entra colada no gancho, sem respiro. **Variantes espelhadas** (quando pedidas): espelhe só a imagem do apresentador antes de inserir título, legenda, números e apoios; o áudio fica igual. Rode a renderização em segundo plano, com prioridade baixa (`nice`).

### Variações de gancho e espelho (YAP3, a partir da V3 aprovada)

- **Plano:** um JSON por gancho, modelo em `assets/plano-variacao-exemplo.json` (caminhos relativos ao próprio plano). Campos de origem: o bruto, `f0` e `n_h` do `cortes_tomadas.py`, o texto literal do título e da legenda, `k_p` (quadro da V3 onde a ponte começa), `KG=120` e o mix da V3. Fórmulas: `P = n_h + KG - k_p` quadros de gancho novo antes do corpo; total = `P + TV - KG` (EP4: `k_p=117`, `TV=2104`; EP3: `k_p=91`, `TV=2336`).
- **Ponte e corpo:** três formas, explicadas no `_ponte_e_corpo` do exemplo: (a) `v3_final` com letra branca completa e `corr` vazio; (b) `v3_final` + `correcoes` + `corr`; (c) `corpo_normal` (corpo de KG até o fim) + `ponte_normal`. O corpo entra por cópia de pacote, então sai bit a bit igual em todas as versões.
- **Render:** `python3 <S>/variar_gancho.py prefixo <plano.json>` monta só o gancho novo com a ponte (confira `trab/prev` e os títulos), depois `final` concatena com o corpo. `--espelho` gera a versão espelhada, com ponte e corpo vindos de `v3_espelho` (o espelho original da V3, câmera espelhada e texto legível). Saída: `<saida_dir>/<nome>-gancho-normal-hlg.mp4` e `-espelho-hlg.mp4`.
- **Letra branca:** o lote entregue usa `graf_branco: 1000` (letra a 1000 nits HLG, Y perto de 940). No EP4, o retângulo da demonstração (716, 1140, 336, 464) ficou em 203 no corpo da V3 para não estourar a tela gravada; isso vem pronto no corpo, o `variar_gancho.py` não mexe. Lote antigo em 203 só serve de referência.
- **Auditoria:** `python3 <S>/auditar_variacao.py <plano.json> <final.mp4> [--espelho]` confere ffprobe e cor contra o corpo, decode e contagem de quadros, PTS, sincronia com o mix, true peak de -1 dBTP ou menos, framemd5 do corpo, PSNR da ponte e do corpo (40 dB ou mais), emenda, nível da letra, boca x legenda e título x olhos (YuNet) e mosaico 4:5 e 3:4. Sai com código 1 se reprovar.

## Modelo de briefing por vídeo

```
Vídeo: <tema>  Série/ep: <...>  Take: <caminho do bruto>  Ganchos: <N, onde estão no bruto>
Gancho k (fala literal): "<...>"  2ª linha a partir de "<palavra>"  número em destaque: <...>
Corpo: início "<...>" fim "<...>"  takes repetidos: <qual fica>
Textos do topo (na palavra): "<palavra>" → "<texto literal>" | fonte <...> | som clique|moeda|whoosh
Lista com marcador: itens <...> na palavra de cada um
Prova: <print> | origem | permissão do dono <sim/não>   (sem print: pendência)
Câmera: 1º plano estático; permanência em <trechos>; por movimento: <início/fim> | <fala/motivo> | <escala e posição inicial/final> | <fim do movimento e permanência>; recuo só com <motivo próprio>; emendas de continuidade herdam escala e posição
Legenda (só se pedida): posição <x,y no lado livre do rosto>  fonte <...>  tamanho <...>  sem contorno
CTA (literal, uma ação): "<...>"
Não fazer: música, cor fora da identidade, motion na abertura, mudar a voz
```

## Entrega

Uma pasta de projeto com `bruto/` (cópia), `plano.json`, `final/` (os MP4s), `final/conferencia/` (folhas e medidas) e `relatorio.md` (takes escolhidos, cortes, mapa de sons e de câmera, conferências, incertezas e pendências do dono). No chat: os caminhos, a duração e o tamanho de cada arquivo, o que ficou incerto e o que depende do dono. Cada caminho vai em linha isolada.

**Entrega no Drive (YAP3):** os finais aprovados, com GIF, vão para a pasta `04 APROVAÇÃO` do Drive do projeto, um arquivo por gancho e versão (normal e espelho), com o nome do final. Só sobe com o pedido explícito de quem coordena; a skill não sobe sozinha e não publica. Depois de subir, atualize `assets/memes-usados.json` com os memes do episódio.

## O que esta skill NÃO faz

- Escrever ou corrigir o roteiro e o gancho: **soft-conteudo-reels** e **soft-conteudo-ganchos**.
- Editar uma gravação com b-roll, cartões e apoio gerado: **soft-editor-video**.
- Reel mudo curto de 7 segundos com legenda longa: **soft-reel-7seg**.
- Criticar a copy dos textos antes de queimar: **soft-critico-copy** (se não estiver instalada, o lint desta skill e a regra de literalidade seguram o mínimo).

## Arquivos desta skill

- `references/texto-legenda-elementos.md`: título, textos, elementos, prova, legenda e fontes.
- `references/camera-e-sons.md`: câmera, receitas de ffmpeg e mapa de sons.
- `scripts/instalar_ambiente.py`: instala sozinho o ambiente da edição e grava `ambiente.json`.
- `scripts/prova_render.py`: prova que a máquina renderiza e transcreve antes de editar.
- `references/ambiente.md`: o passo a passo do ambiente, com saídas e regra dura.
- `scripts/lint_copy.py`: o lint de copy da casa, para o arquivo de textos.
- `scripts/buscar_gif.py`, `gif_meme.py`, `cor_hlg.py`, `verificar_gif.py`, `sfx_gif.py`: busca, render HLG, conferência e sons do GIF de meme.
- `assets/sons-gif/`: sons dos GIFs (CC0, origem em `sons.json`); `assets/plano-gif-exemplo.json`: plano de exemplo.
- `scripts/transcrever_tomadas.py`, `cortes_tomadas.py`: palavras das tomadas de gancho (large-v3 offline) e limites exatos de cada tomada.
- `scripts/variar_gancho.py`, `auditar_variacao.py`: variações de gancho e espelho sobre a V3 e a auditoria de cada final; `assets/plano-variacao-exemplo.json`: plano de exemplo.
- `scripts/rosto.py`: rosto, olhos e boca com YuNet local (`assets/modelos/face_detection_yunet_2023mar.onnx`).
- `scripts/pico_gif.py`, `ganho_uniforme.py`: diagnóstico de pico do mix com GIF e ganho uniforme pequeno no áudio.
- `scripts/planos_gif_lote.py`, `lote_gif.sh`, `auditar_gif_meme.py`, `mosaico_geral.py`: GIF em lote, auditoria por vídeo e mosaico do lote.
- `assets/memes-usados.json`: semente, só leitura, dos memes já usados na série (não repetir); `scripts/memes_usados.py`: lê a semente e o registro do dono e grava os novos fora da skill; `assets/momentos-v3-exemplo-ep4.json`: momentos de GIF do EP4 em quadros da V3.
- `assets/sfx-gancho/`: impacto e clique do gancho (sintetizados, obra própria); `assets/fontes/`: Kalam Bold com a licença OFL (a Advercase não vem junto, ver `references/ambiente.md`).
- `scripts/reproduzir_molde.py`, `render_overlay.cjs`: confere as fontes do molde pelo SHA256 e desenha o overlay HTML aprovado em PNG (puppeteer-core e Chrome por `YAP_PUPPETEER` e `YAP_CHROME`).
- `references/revisao-fluidez-elementos-camera-2026-10-15.md`: resumo do curso para o refinamento de fluidez, elementos e câmera.

## Nome do arquivo e lint

Nome de arquivo em minúsculas, sem acento, com hífens. Todo `.md` que a skill entregar passa por `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) antes de ser dado como pronto.


## Nova edição completa e correção de fluidez, 15/10/2026 16:02

A ordem de congelar pessoa, ângulo e áudio aplica-se a ajuste restrito de posição de texto. Uma nova edição completa autorizada volta ao bruto e decide cortes, aproximações, recuos, sons e apoios pela fala; não herda o corpo rejeitado como pronto. Preserve a identidade deste estilo e a prioridade do perfil aprovado da série.

Antes de renderizar, salve mapa por fala com: intervalo do bruto, frase literal, tentativa descartada e retomada escolhida, tempo de saída, função tipográfica, arquivo de fonte, câmera inicial/final e motivo, apoio e sua origem, som e instante de entrada. Detecte repetições, gagueiras, início abortado e autocorreção na transcrição com palavras temporizadas. Compare as tentativas no áudio; mantenha a retomada mais fluida e remova a primeira tentativa quando ela for erro. Não corte uma repetição intencional só porque a palavra repete. Transcrição automática sozinha não prova emenda fonética: confira bordas, consoantes, respiração e continuidade; documente tempos antes/depois e incerteza real. Guarde bordas de áudio suficientes para preservar a sílaba, em vez de cortar exatamente no timestamp estimado de palavra.

Varie a tipografia por função dentro dos pares comprovados do estilo: título, complemento/contraponto e legenda não são uma camada indiferenciada. Leia o perfil e referências locais; registre caminho e hash das fontes e falhe se o arquivo não carregar. Não invente fonte nem use fallback silencioso. No perfil Manuscrito (ep2), a referência local é Advercase Bold85 para título, Kalam Bold54 para complemento e Advercase72 para legenda; topo315 e folga de30px do recorte4:5. Esse perfil não substitui a identidade celular ou editorial de outro pedido.

Planeje sons nas entradas motivadas de texto, lista, demonstração, comparação ou ênfase; sincronize o som ao evento e mantenha a voz dominante. A reclamação de poucos sons exige rever oportunidades concretas, não preencher uma cota. Aproximação gradual pode sustentar uma fala que cresce em importância; recuo precisa de motivo próprio, como abrir área para lista ou iniciar etapa. Registre escala e duração, preserve continuidade em cortes de limpeza e permita permanência. Não alternar zoom in/out por índice, por intervalo fixo nem por obrigação de variar.

Escolha elementos pertinentes aos substantivos, ações e relações da fala: lista progressiva, número, contraste, seta ou demonstração real quando houver fonte. Não invente prova ou resultado. Audite cada estado no feed9:16 e recortes4:5/3:4, olhos e boca livres, título e complemento com hierarquia e sem palavra órfã. Confira duração final até90s, CTA literal completo, cortes, áudio/canais/truepeak e decodificação integral. Declare exatamente o que foi executado; não alegue escuta humana ou revisão independente inexistente. Sem música, EQ, compressor ou limiter nesta correção do dono.


## Refinamento de fluidez, elementos e câmera, 15/10/2026 17:11

O dono elogiou a direção visual da v1 e pediu outra edição completa: ainda havia erros/gaguejos e faltavam GIFs pertinentes e jogo de câmera perceptível. Elogio com ressalva não representa aprovação integral. Leia a fonte de curso em `references/revisao-fluidez-elementos-camera-2026-10-15.md` ao executar esse refinamento. Respeite a identidade própria desta skill.

ASR é mapa, não revisão fonética: pode normalizar sílabas repetidas, falsos começos e muletas. Faça varredura de todas as frases selecionadas, incluindo respirações e as emendas internas, em vez de conferir apenas os erros já apontados. Examine áudio quando a ferramenta permitir; na ausência de escuta, combine janelas curtas sobrepostas, análise acústica e margem de fonema, registre a limitação e nunca declare todos os gaguejos removidos só porque a transcrição está limpa. Compare candidatos por fluidez, preserve a retomada literal mais completa e mantenha o CTA até o último fonema. Acelerar não corrige gaguejo; esta nova tentativa do EP2 usa velocidade natural.

GIF/figurinha animada é recurso opcional, escolhido pelo substantivo, ação ou reação da fala. Demonstre que o arquivo anima no render, entra na palavra e sai com a troca do assunto. Identifique ilustração criada como ilustração; não use animação ou imagem genérica como prova de resultado. Falta de fonte real para contrato ou valor permanece limite, nunca vira print inventado.

Para câmera, a prova é o MP4 decodificado: compare começo/meio/fim de cada trajetória com a imagem fonte, além das duas bordas de cada emenda. Meça ou mostre escala/posição realmente realizadas; registre inversão, tremor, reset ou ausência de progressão. Trocar algoritmo exige repetir a prova curta do movimento. Push-in lento deve ser perceptível e terminar antes da fala para permitir permanência; recuo e punch precisam de motivo próprio. Preserve escala e posição em cortes de limpeza. Não alternar automaticamente por corte. Abertura estática permanece. Nova edição completa autoriza esses movimentos; take fixo de um ajuste de texto não congela uma edição posterior autorizada.
