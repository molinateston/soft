# Processo, retomada e critérios

Este documento é vigente. Histórico e exemplos não substituem as regras. Uma tarefa interna não pede aprovação a cada passagem; decisões de marca já dadas continuam válidas. Revisão independente permanece obrigatória antes de entrega. Na execução sem revisor, registrar REVISÃO INDEPENDENTE PENDENTE e encaminhar ao coordenador.

## Registro obrigatório

Criar `STATUS.md`, `BRIEFING.md`, `MAPA-CORTE.md`, `STORYBOARD.md`, `storyboard.json`, `materiais.json` e `conferencia/`. Registrar código, fonte, autorização, objetivo, formato, versão dos scripts e hashes. Conferir inventário de códigos e pastas locais/03/04 disponíveis antes de editar; arquivo já entregue não vira nova edição sem pedido. Registrar o que foi realmente consultado; ausência de acesso não equivale a ausência de duplicata.

Formato é decisão de entrada: `talking_head_yap4`, `monitor_preservado` ou `palestra_conceito`. Nunca escolher pelo tamanho do rosto. Captura de monitor preserva o enquadramento completo, rosto pequeno, legibilidade e demonstração; sem crop, zoom no rosto, blur, nova divisão ou cobertura da interface relevante. Talking head segue o layout próprio. Palestra segue tarjas e desenhos. Não transformar um formato em outro silenciosamente.

## Etapas com contrato

| Etapa | Entrada | Saída | Pronto | Retomar e invalidação |
|---|---|---|---|---|
| 0 Inventário e briefing | pedido, código, brutos, entregas e marca | BRIEFING e inventário com provas | formato, objetivo, destino e fonte identificados; duplicata resolvida | atualizar somente entrada alterada |
| 1 Transcrição | áudio extraído, hash, motor/modelo, idioma, prompt, beam, offset | palavras por tempo e chave de cache | texto conferido no bruto, termos incertos marcados | cache só vale com áudio/configuração/motor iguais; correção editorial separada do ASR |
| 2 Decupagem | transcrição, áudio e objetivo | MAPA-CORTE e mapa de palavras da saída | ideia completa, abertura compreensível, conclusão dentro do corte, cada remoção justificada e cada emenda ouvida | fala errada volta aqui; não transcrever tudo novamente |
| 3 Headline | corte fechado e método de headline da marca | candidatas internas e escolhida com justificativa | assunto inteiro, promessa entregue, texto contextual e lint 0 | alterar só texto e camadas dependentes; sem ganchos alternativos por padrão |
| 4 Storyboard | mapa fechado e headline | STORYBOARD e storyboard.json | todas as cenas têm fala/fonte, tempos de origem/saída, âncora, material, composição, legenda, transição e fechamento | não produzir apoio antes de fechar a relação fala/imagem |
| 5 Materiais | storyboard fechado | materiais.json e arquivos por ID | origem, licença/permissão, hash e transformação registrados; IA identificada | substituir só material afetado; nenhum token em manifesto |
| 6 Prévia | plano e materiais | quadros de abertura, emenda, palavra longa, CTA e amostra curta | cabeça, rosto, monitor e texto legíveis; nenhuma sobreposição cobre demonstração | falha de caixa volta ao layout; fala volta à etapa 2 |
| 7 Montagem/render | plano, mapa por palavra e prévia conferida | render, log e manifesto de versões | duração do plano confere; fila sequencial; saída vinculada ao hash do plano | reutilizar peças só com mesmas entradas/config/codificação; não juntar peças antigas e novas incompatíveis |
| 8 Conferências | render e plano | laudos separados fala/visual/arquivo e revisão independente | todos os critérios aplicáveis passam; divergências resolvidas por áudio e quadro real | falha retorna só à causa; nada de baixar limiar para passar |
| 9 Pacote | render conferido e autorização | master, leve, mosaico, manifesto e checklist | arquivos abrem, hashes e relatório presentes; revisão independente encerrada | upload 04 e bruto 03 só em tarefa de vídeo autorizada; esta finalização de skill não envia |

## Fala e tempo

Transcrever a fonte uma vez por configuração coerente. Auditoria da saída é uma transcrição distinta e necessária; reaproveitar seu cache apenas para o mesmo áudio/configuração. ASR não prova fonema sozinho. Antes da montagem, ouvir cada emenda com contexto antes/depois e comparar as palavras/sílabas no bruto e na saída. Timestamp entre palavras não é silêncio comprovado. Pausa, respiração, falso começo e gaguejo podem sair apenas sem danificar fala válida. Repetição intencional, ênfase e paralelismo ficam; uma declaração não pode dispensar evidência acústica. Não esconder erro no áudio corrigindo só legenda. Nome incerto exige contraprova, não substituição por palpite.

Cada promessa ou demonstração tem `abre`, `fecha` e evidência visível/verbal dentro do corte; tabela vazia exige revisão explícita de que não houve promessa. Palestra longa: 90 a 300 s. Teste curto se chama prova de componentes. Se a aceleração é 1,15, tempo de saída deriva do mapa de quadros, inclusive cold open e repetições, nunca de uma subtração aproximada global.

## Storyboard executável

Uma linha por estado visual, inclusive rosto/monitor sem apoio. Cobertura contínua de 0 até o último quadro, sem buraco nem sobreposição entre cenas-base. Cada linha aponta intervalo da fonte e do render, IDs de palavras, transcrição literal de apoio, palavra âncora e fonte do material. Separar descrição de intenção da medição. O campo `criterio` diz o que o revisor deve enxergar/ouvir. CTA entra na palavra de CTA realmente dita. Registrar o fechamento da promessa; não inventar CTA falado.

O modelo MD é a pauta de leitura; `storyboard.json` é o contrato de produção. Validar antes de render: `python3 scripts/validar_storyboard.py TRAB/storyboard.json`. O validador confere estrutura e intervalos; não ouve nem aprova semântica. Cada cena precisa referenciar os IDs do mapa real; o executor confere conteúdo e caixas na prévia.

## Fila, limite e cache

Um vídeo pesado de cada vez. Pesquisa e revisão textual podem ocorrer durante render, mas não iniciar segundo render/ASR pesado. Use o agendador local quando existir; para execução portátil, `executar_etapa.py` usa lock configurável compartilhado e timeout de até 3600 s por etapa. A espera de lock conta no limite. A revisão independente não deve disputar GPU/CPU com render. Não repetir teste integral após apenas texto documental.

Exemplo: `python3 scripts/executar_etapa.py TRAB render --input TRAB/ajustes.json --input TRAB/storyboard.json --output TRAB/final.mp4 --timeout 3600 -- python3 scripts/06_compor.py TRAB`. Listar TODAS as dependências efetivas, inclusive scripts, fontes e marca; comando, hashes de entradas e hashes de saídas formam o cache. Nunca usar só existência como pronto. O wrapper não decide dependências sozinho. Em render por peças, cada peça tem identidade própria, parâmetros idênticos e emenda na borda de segmento; concat sem recompressão só após conferência.

STATUS contém início UTC, fim, duração medida, comando sem segredo, hashes, saída, causa e próximo comando. Ao atingir 1 h, parar apenas o grupo de processos próprio, registrar etapa bloqueada e preservar saídas parciais como incompletas. Não tentar variantes por horas. Auditor em desenvolvimento não bloqueia a organização nem outros vídeos leves; sua reprovação bloqueia a entrega daquele vídeo. Revisão manual não transforma laudo reprovado em PASSA.

## Conferências separadas

Fala: cobertura literal, palavras/sílabas das emendas, respirações e repetições, loops completos. Divergência de ASR requer escuta e evidência de janela, sem exceção nominal por vídeo.
Visual: abrir prévia e mosaico do começo/meio/fim e de todas as mudanças de layout; imagem ilustra exatamente a fala, marca vigente, sem verde gráfico, rosto inteiro, legenda fixa e demonstração livre. Foto real pode conter cores naturais; restrição de paleta vale à camada gráfica.
Arquivo: ffprobe (resolução/fps/duração/trilhas), decode integral sem erro, tamanho e áudio medidos; resultado automático não substitui escuta. Relatório distingue PASSA, REPROVA, NÃO EXECUTADO e NÃO APLICÁVEL com motivo por formato. Auditor de talking head não pode reprovar monitor por rosto pequeno, nem dispensar falhas reais: precisa perfil de formato implementado e regressão antes de declarar cobertura automática.

## Dependências e portabilidade

Python 3, ffmpeg/ffprobe e dependências listadas no pacote. Modelos Whisper podem baixar na primeira execução; preparar ambiente antes da fila. Fontes e identidade vêm de `marca.json` ou parâmetros do trabalho, com licença. Não instalar automaticamente ao editar vídeo. Segredos ficam no ambiente, fora de ZIP/log. Caminhos de trabalho e fontes são relativos ou parâmetros explícitos. Scripts históricos não são um CLI genérico: o índice declara quais exigem adaptação e quais são executáveis. Não confundir pacote documental com validação ponta a ponta.
