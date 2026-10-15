---
name: soft-edicao-yap
description: >-
  Edita um YAP, o vídeo de talking head falado direto pra câmera (episódio de websérie, vídeo solto ou spin-off), do bruto ao arquivo 1080x1920 pronto: cortes sem respiro, título no primeiro quadro, textos e listas na palavra, prova em print, câmera parada com aproximação só quando a fala pede, legenda de uma palavra quando pedida e sons marcando cada elemento. Também monta o briefing pro editor (agente ou pessoa), exporta uma versão por gancho com o mesmo corpo e confere a edição antes de entregar. Use quando o pedido for: "edita esse YAP", "edita o episódio da websérie", "monta o briefing de edição do meu vídeo falado", "exporta uma versão por gancho", "confere essa edição antes de eu postar". NÃO use pra: escrever o roteiro ou o gancho (soft-conteudo-reels, soft-conteudo-ganchos); editar gravação com b-roll e cartões (soft-editor-video); reel mudo de 7 segundos (soft-reel-7seg). Leia e siga o fluxo inteiro do SKILL.md.
---

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

## Regras de partida (o dono pode mudar qualquer uma; registre a mudança no relatório)

1. **Uma cor de acento só**, a da identidade do dono. Na legenda não há destaque colorido.
2. **Preservar a voz e a fala.** Velocidade padrão 1,1x preservando o tom (`atempo=1.1`), com o ok do dono; 1,2x só se a fala continuar clara; fala já rápida não acelera. Sem compressão, sem EQ, sem troca de take por IA. O som de efeito entra por baixo da fala, nunca no lugar dela. Única exceção: um ganho linear uniforme e pequeno (até -2 dB) no master inteiro, só para o pico ficar em -1 dBTP ou menos, anotado no relatório.
3. **O vídeo não começa com motion.** Título em texto já no quadro 0, sim. Animação de abertura, vinheta, zoom de keyframe ou texto entrando animado no primeiro plano, não.
4. **Export 1080x1920, 30 fps, menos de 300 MB, arquivo íntegro** (`ffmpeg -v error -i X -f null -` sem saída).
5. **Título e legenda literais ao que foi falado.** Não resuma o gancho.
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
- **Câmera:** confira a trajetória de escala e posição no arquivo final. Examine pares antes e depois dos cortes e a sequência em tempo real: quadro isolado não valida conforto de movimento. Anote se só foi possível examinar quadros.
- **Emenda gancho → corpo:** quadros n-1 e n e escuta de 2 s em volta (sem respiro, sem palavra comida).
- **Entrada de cada elemento:** quadros n-1 e n.
- **Sincronia do som:** atraso do efeito em relação ao elemento de 0 a 2 quadros.
- **Voz intacta:** diferença entre o áudio editado e o mesmo mix sem efeitos, fora das janelas dos efeitos, perto do ruído do reencode.
- **Loudness e pico:** `ebur128=peak=true`, true peak -1,0 dBTP ou menos.
- **Corpo idêntico entre versões:** o hash dos quadros do corpo (`framemd5` no trecho) é igual nas N versões, ou o intermediário concatenado é o mesmo.
- **Texto literal à fala.** Rode o lint de copy desta skill sobre o arquivo com os textos (`python3 scripts/lint_copy.py <arquivo>`). Aviso de lint em fala literal não muda a fala: só anota.

## Export de uma versão por gancho

Quando o dono grava N ganchos (no início e/ou no fim do bruto), sai **um MP4 por gancho, com um único gancho cada**, e o **corpo é idêntico** em todos.

1. **Preparação:** segmentos pela regra de silêncio (fim = `ceil((s+0.04)*30)`, início = `floor((e-0.04)*30)`), mapa de tempo bruto → saída, áudio a 48 kHz com 1600 amostras por quadro e fade de 4 ms, efeitos calibrados pelo p90 da voz, ganho uniforme do master para true peak -1,5 dBTP.
2. **Corpo:** renderizado **uma vez**, numa passada (`select` dos quadros dos segmentos, `setpts=N/30/TB`, conversão de faixa de cor para limitada, câmera por partes, overlay dos textos e legenda).
3. **Ganchos:** um clipe por gancho com os mesmos parâmetros de codec (plano estático, título literal no quadro 0, legenda, som do quadro 0).
4. **Final:** concatene gancho e corpo com `-c:v copy` (o corpo sai bit a bit igual nas versões) e junte o áudio da versão em AAC 192k 48 kHz, `+faststart`.

Nome: `ep<N>-v<k>-<tipo-ou-3-palavras-do-gancho>.mp4` (v1 = gancho do início do bruto). A apresentação do corpo ("Meu nome é...") entra colada no gancho, sem respiro. **Variantes espelhadas** (quando pedidas): espelhe só a imagem do apresentador antes de inserir título, legenda, números e apoios; o áudio fica igual. Rode a renderização em segundo plano, com prioridade baixa (`nice`).

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

## O que esta skill NÃO faz

- Escrever ou corrigir o roteiro e o gancho: **soft-conteudo-reels** e **soft-conteudo-ganchos**.
- Editar uma gravação com b-roll, cartões e apoio gerado: **soft-editor-video**.
- Reel mudo curto de 7 segundos com legenda longa: **soft-reel-7seg**.
- Criticar a copy dos textos antes de queimar: **soft-critico-copy** (se não estiver instalada, o lint desta skill e a regra de literalidade seguram o mínimo).

## Arquivos desta skill

- `references/texto-legenda-elementos.md`: título, textos, elementos, prova, legenda e fontes.
- `references/camera-e-sons.md`: câmera, receitas de ffmpeg e mapa de sons.
- `scripts/lint_copy.py`: o lint de copy da casa, para o arquivo de textos.

## Nome do arquivo e lint

Nome de arquivo em minúsculas, sem acento, com hífens. Todo `.md` que a skill entregar passa por `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) antes de ser dado como pronto.
