# Dois exercícios fictícios executáveis

Os arquivos em `examples/` substituem o exemplo antigo de fitness para evitar alegações de saúde sem fonte e falsos envios por WhatsApp. Todos os nomes, ofertas e escolhas são fictícios e só verificam mecânica.

- `organizacao-checkout.json`: pessoas que organizam documentos pessoais. Prioridade entre localizar e separar, restrição de espaço, seleção múltipla de materiais. Resultado com vídeo ausente explicitamente indicado e roteiro em texto; CTA abre checkout de demonstração local, sem compra.
- `biblioteca-reuniao.json`: biblioteca comunitária que avalia organização de catálogo. Situação, ferramenta atual, pergunta dependente, número de títulos e texto livre, qualificação após vídeo de convite. Critério fictício de adequação, agenda de demonstração para elegíveis e orientação alternativa aos demais.

Para gerar: `python3 scripts/build_quiz.py examples/organizacao-checkout.json --out /tmp/exercicio-quiz`. Abra `/tmp/exercicio-quiz/index.html`. Os destinos locais são telas de ensaio, nunca serviço externo. As regras e a copy estão na configuração. Para qualquer uso real, substituir por oferta, fontes, critério e destinos válidos; revisar roteiro e aplicar mídia autorizada.
