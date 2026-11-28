# Ferramentas e limites de execução

Comuns: `python3 scripts/validar_storyboard.py trabalho/storyboard.json` confere estrutura; `python3 scripts/executar_etapa.py trabalho etapa --input entrada --output saida --timeout 3600 -- COMANDO` executa uma etapa com cache por hashes, lock e prazo. Declarar scripts, marca, materiais e fontes como entradas. Não omitir dependências para obter cache. Saídas parciais após falha não são finais.

Dependências: Python 3, ffmpeg/ffprobe. Instalar em ambiente isolado antes da tarefa; modelos ASR devem estar disponíveis antes da fila. Modelos MD são preenchidos com material real da tarefa. Não executar exemplos históricos sobre outro bruto. Conferência humana das emendas e revisão independente continuam obrigatórias.

Pipeline local/portátil: `bash scripts/rodar.sh TRAB [--prova] [--de N]`. Antes: preencher entrada, ajustes, marca, mapa e storyboard. Etapas: 01_entrada, 02_transcrever, 03_cortes, 04_headline, 05_conceitos, 06_base/rosto/reframe/compor, 07_gate_fala/visual, 08_mosaico, 09_entrega. Execute cada chamada pesada pelo wrapper, com todas as dependências; o shell sequencial sozinho não impõe prazo/cache de render. `--de` só muda início, não prova coerência dos artefatos existentes. `--prova` dispensa duração mínima e nunca certifica corte longo.

Dependências adicionais em requirements.txt. `instalar.sh` é opção explícita, não ação automática desta skill. Whisper baixa modelo na primeira execução se não estiver preparado. 02_transcrever agora valida áudio/configuração/motor e hash da transcrição antes do reuso. Não confundir cache do bruto com cache da auditoria de saída. Desenhos de exemplo e defaults não substituem storyboard nem materiais da tarefa.


Complemento de 28/11: `desenhos_storyboard.py` implementa estados VPS de exemplo na tarja inferior, inclusive estados sem apoio e manutenção do último desenho. É módulo de material, não detector de assunto nem aprovador de storyboard. `03_cortes.py` aceita `preservar_fala_continua: true` para manter pausas internas dos blocos; cortes explícitos continuam declarados. Use na prova contínua de compositor e confira as bordas no áudio. `escala.py` aceita grupo vazio, que produz tarja sem desenho; o teste de área útil ignora somente a caixa de área nula. Conceito desenhado continua sujeito à zona local x66..1014/y12..505.

Na prova nova, o trecho começa na pergunta sobre onde mora o agente e termina antes da nova promessa de ferramentas. O cold open relativo à segurança e a promessa anterior de cinco camadas foram retirados do plano. A sequência contínua de 108,100 s foi planejada com 29 cenas e 28 estados gráficos; a última cena mantém o estado anterior. Essa escolha não certifica outros cortes. Diagramas e âncoras ainda exigem conferência semântica e auditiva independente, incluindo troca de modelos e execução por auxiliares.


`preservar_painel: true` mantém o painel 16:9 integral na faixa do palestrante, sem zoom ou recorte. Use quando o detector segue rosto da plateia ou quando o telão contém informação demonstrada. A prévia da prova mostrou o detector priorizando a plateia e cortando a cabeça do palestrante; o painel integral mantém cabeça e telão. O layout das tarjas permanece o mesmo. Não confundir pane preservado com rosto sempre presente: cortes de câmera existentes na fonte permanecem.
