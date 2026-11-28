# Orquestração vigente

Um vídeo por vez na fila pesada. Não iniciar lotes concorrentes de render ou ASR. Um executor por etapa; revisão independente por coordenador ou executor separado, que recebe insumos e critérios sem assumir o veredito do autor. Nesta finalização documental, revisão fica com o coordenador.

Ordem: inventário/briefing, transcrição em cache, decupagem e conferência pré-montagem, headline, storyboard e crítica, materiais, prévia, composição, conferências finais e pacote. Os contratos estão em references/PROCESSO.md. Pesquisa/material e revisão textual podem ocorrer em paralelo desde que não disputem a fila pesada nem alterem plano em render.

Render por peças é opcional quando o compositor implementa intervalo de quadros. Não ordenar alteração de compositor durante edição para cumprir divisão em metades. Renderizar peças sequencialmente; concat somente com parâmetros idênticos e bordas verificadas. Sem versões A/B/C por padrão.

Falha volta apenas à etapa causadora e invalida dependentes efetivos. Etapa fixa tem teto de1h contando fila, causa e checkpoint. Auditor em desenvolvimento não bloqueia toda a fila; bloqueia entrega do vídeo reprovado. Não abrir sucessivas tentativas silenciosas.
