---
name: soft-edicao-yap4
description: Edita gravações talking head pelo método YAP4 ou capturas de monitor preservando o formato gravado, com decupagem, storyboard temporizado, legenda fixa, materiais literais e conferências distintas de fala, visual e arquivo. Use quando pedirem edição YAP4, briefing, storyboard ou conferência desses formatos. Não use para palestra com desenho de conceito. Leia o fluxo completo e o estado das ferramentas antes de executar.
---

# Edição YAP4 e captura de monitor

Leia `references/PROCESSO.md` inteiro antes de cortar. Ele define entradas, saídas, pronto e retomada de cada etapa. Leia `ORQUESTRACAO.md` para fila e revisão independente. `references/FERRAMENTAS.md` distingue utilitários prontos de moldes históricos que precisam de configuração; não execute um plano antigo sobre vídeo novo.

## Escolha do formato na entrada

| Formato | Base visual | Regra de composição |
|---|---|---|
| talking_head_yap4 | pessoa na câmera | YAP4, abertura dividida e apoios literais |
| monitor_preservado | captura gravada com rosto pequeno | preservar tela inteira e janelinha na posição/tamanho originais; apenas cortes, legenda, headline, cold open e CTA autorizados |

Na captura de monitor, a demonstração já é o apoio. Não aplicar abertura dividida, quotas de apoio, zoom, reframe de selfie, blur no monitor ou novo layout. Não ampliar rosto para atender detector. Sobreposição não cobre rosto nem conteúdo demonstrado. Se a legenda fixa entrar na demonstração, registrar conflito na prévia e resolver a camada de texto sem alterar a captura; mudança de posição aprovada exige parâmetro de formato, nunca exceção por código de vídeo. Sem prévia legível, não renderizar final.

## Método vigente para talking head

Base histórica: V121 v3; referência atual de letra/legenda: V179. Não refazer esses vídeos. Correções de 26 e 27/11 prevalecem sobre registros antigos preservados no histórico.

Tela cheia mantém a cor do bruto, sem retoque. Topo: Advercase Bold 92 e apoio Kalam 50, destaque laranja #D4541C. Cards até y490 e textos até y600, respeitando safe area e rosto.

Divisão: linha y790, apoio 1080x790 em cima; apresentador abaixo, deslocado à esquerda, cabeça inteira. Parâmetros do molde aprovado: PES_Y0=380, DIV_ESCALA=1.2, DIV_X0=180. Boca ao menos 120 px abaixo da linha; topo da cabeça com folga de 20 px no bruto. Não subir recorte para fugir da legenda. Se a geometria de uma fonte diferente não serve ao molde, parar na prévia e registrar conflito em vez de cortar a cabeça.

Abertura cerca de 6 s, sempre vídeo em cima: clipe real ou foto de impacto animada. Preferir foto real da notícia; print só quando foto forte é dominante, nunca página de texto/documento como abertura. Headline Modelo 3: Advercase Bold branca com contorno/sombra e palavra em bloco inclinado 2 graus; usar laranja vigente. Centrada na emenda, sem cobrir olhos. O antigo gerador temporário não é dependência de execução; exportar overlay transparente para materiais, registrar parâmetros e conferir na prévia. Não recriar método por indisponibilidade do gerador.

Meio: 2 a 4 divisões com motivo concreto, não consecutivas, mais de 5 s entre elas; até 12 s cada. Diagrama também conta como divisão. Apoios em palavra âncora com tolerância de 0,3 s. Conceito em etapas alterna desenho que se preenche (1,5 a 3 s) e foto/vídeo correspondente (2 a 4 s), com volta ao desenho. Nenhum apoio parado por mais de 4 s sem mudança ligada à fala.

Foto real/manchete com foto é o apoio principal para fatos, pessoas e casos. Motion só explica conceito/mecanismo sem foto, nunca para cumprir variedade. Manter variedade quando a fala permite, sem quota cega de imagens nem exigir 3 tipos da captura de monitor. Toda imagem ilustra exatamente a fala, com palavra que prova e crédito no storyboard. X nega, seta aponta dado real, GIF reage à fala de julgamento. Um elemento por vez; apoios de topo só após 7 s, fora das divisões. Topo útil começa em y195, não na antiga indicação y60. Sem cobrir rosto, legenda ou prova.

Paleta gráfica: tinta #141413, marfim #faf9f5, linha #e6e3da, laranja #D4541C, preto e branco. Sem verde ou ícone multicolorido genérico. Cores naturais da fonte/foto não são recoloridas.

## Legenda e áudio, fonte única

Legenda de uma palavra, mesma letra da referência V179: Advercase72, sombra preta leve, fixa em `\an6\pos(940,1250)`, inclusive divisão. Máximo de 0,7 s por palavra. Quando palavra comprida tocar rosto, reduzir apenas aquela palavra até mínimo aprovado52. Se ainda tocar, reprovar prévia. Não mover legenda a cada palavra nem reenquadrar captura de monitor. Marca portátil declara arquivo/licença da fonte; não substituir silenciosamente por outra letra.

Sem música. SFX só ligado a elemento, baixo e sem ocultar voz; alternar sons/marcadores quando presentes. Voz e vídeo a1,15x com mapa único; fades nas emendas de4ms, sem compressor/EQ, ganho uniforme para true peak alvo -1,5dBTP, limite -1dBTP. Cor igual ao bruto, bt709 limitada; comparar amostra de pessoa/bruto, diferenças médias Y/U/V abaixo de1 no método vigente.

CTA apenas quando fala permite: cartão de seguir entra em “segue”, fica legível antes do toque Seguir para Seguindo durante a identificação falada. Foto/nome/perfil e selo vêm da marca, fora do método portátil. Curtir breve no meio só em espaço livre, com plim baixo. Não antecipar CTA nem cortar sílabas para acomodar animação. Sem ganchos alternativos por padrão.

## Áreas seguras parametrizadas

`marca.json > formatos` declara geometria por formato, não por vídeo. Base1080x1920: texto x65..1015, y195..1400; na faixa y1005..1400 a borda direita é940. A legenda tem borda direita940. Excluir também caixas de rosto e conteúdo demonstrado. Perfil monitor mantém câmera original e acrescenta regiões demonstradas do plano; regiões temporais são evidência do conteúdo, nunca dispensa da safe area. Sobreposição de informação precisa passar tanto na zona da plataforma quanto na região livre da demonstração. Gabarito local: `assets/safe-zone-reels-1080x1920.png`.

## Comandos e entrega

Preencher modelos em `modelos/`. Validar storyboard com `python3 scripts/validar_storyboard.py TRAB/storyboard.json`. Usar `executar_etapa.py` para prazo/cache e a fila local quando disponível. Os comandos específicos e limites dos moldes estão em `references/FERRAMENTAS.md`.

Conferir fala antes da montagem; após render, laudos separados e revisão independente. Arquivo final1080x1920,30fps, menos de300MB, decode sem erro, áudio dentro do limite. Mosaico aberto e conferido, master/leve/manifesto e checklist completos. Upload04 e bruto03 só na tarefa de vídeo autorizada. Esta skill não declara concluída uma entrega com gate reprovado.

Exemplo de monitor em `exemplos/monitor/`: preenchido a partir de material real, com proveniência e estado reprovado/desatualizado. Exemplo não é aprovação. Ver `VALIDACAO.md` para limites atuais.

## Compositor portátil de talking head

Use [contrato executável](references/COMPOSITOR-TALKING-HEAD.md) para montar os segmentos decididos na decupagem. A prova de monitor não valida este formato.
