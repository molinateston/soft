# Estado de validação em 28/11/2026

Compositor portátil de monitor implementado nesta versão. Prova integral de entrada contínua com headline, CTA, legenda fixa, rosto pequeno no enquadramento original e sem música: 106,913 s planejados, 393 palavras mapeadas, render em 113,526 s. Decodificação integral sem erro; pico verdadeiro final -1,5 dBFS, medido com ebur128. Ganho uniforme +2,5 dB. O manifesto vincula fonte, configuração, compositor, fonte tipográfica, palavras e saída por SHA-256.

Essa prova comprova execução audiovisual do compositor de monitor nessa configuração. Não comprova decupagem, todas as emendas históricas, exatidão de cada legenda, semântica de todo apoio ou revisão independente. O compositor portátil de talking head também foi executado: 33,669002 s, 104 palavras, render em44,449s, duas remoções reais de pausa, três apoios visuais, manifesto com hashes. Contrato em references/COMPOSITOR-TALKING-HEAD.md. As bordas respeitam o mapa de palavras; a conferência acústica é registrada separadamente. O estado de publicação depende dos gates e da revisão de cada peça; não há certificação ponta a ponta.

A correção geométrica da palestra usa contrato próprio de tarja inferior, documentado na skill correspondente. O limite YAP4 de texto até y1400 não serve para mover desenhos da palestra para cima.

O registro anterior permanece abaixo como histórico. As reprovações antigas não foram convertidas em aprovação pela prova contínua nova.

## Histórico de 27/11/2026

Documentação e ferramentas novas revisadas por sintaxe e testes curtos. Não existe certificação ponta a ponta desta versão. Revisão independente pelo coordenador pendente. Nenhum vídeo novo foi entregue ou enviado.

Monitor: exemplo tem transcrição real e storyboard, mas o último gate integral da fonte de referência reprovou seis ocorrências. O mapa posterior não foi validado; final antigo não representa esse mapa. Cinco regressões locais e quatro testes posteriores não certificam o vídeo inteiro. Não promover o conferidor experimental.

Palestra: prova histórica de 103,40 s reprovou cobertura de fala: 95%, 17 palavras ausentes entre 456 esperadas. Artefatos posteriores de mapa/log indicam 111,333 s; não são a mesma versão nem autorizam apagar a reprovação anterior. Prova curta não satisfaz os 90 s mínimos de validação completa. A indicação antiga de conflito global y1400 foi corrigida por formato em 28/11, com precedente geométrico documentado; conferência de interface e revisão continuam necessárias.

Exemplos mantêm promessas_revisadas=false porque falta escuta integral e fechamento das demonstrações. O validador deve reprovar esses exemplos até revisão real. Um controle de teste com esse campo verdadeiro verifica apenas estrutura, não aprova o vídeo. Não trocar a flag para ocultar pendência.

Provas desta rodada: cache ASR em 4 s reais (transcrição, reuso e invalidação por configuração); wrapper com execução/reuso/invalidação/timeout; storyboard com controles de câmera, loop e intervalos; sintaxe; ffprobe e decode inicial de 4 s dos renders históricos. Nenhuma delas prova preservação de todas as emendas. Relatório da entrega registra durações medidas.


## Execução com ordem fechada, 28/11

Após fechar DECUPAGEM.json e storyboard.json/STORYBOARD.md, nova montagem talking head de 33,669002 s foi executada em38,922s com o mesmo compositor e configuração visual. Os hashes e horários dos insumos precedem a saída. Decode integral rc0; mosaico de nove tempos aberto. A prova anterior e suas limitações permanecem no histórico. A comparação acústica anterior continua aplicável ao método e não substitui escuta fonética integral. Nenhuma instalação em cliente real foi verificada.
