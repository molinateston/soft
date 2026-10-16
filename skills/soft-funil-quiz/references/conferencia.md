# Conferência de conteúdo e aplicação

## Fontes, operação e títulos

Mantenha `conferencia/fontes.md`: afirmação pública, origem exata (arquivo e trecho ou URL consultada), limite e decisão. Sem insumo real, registrar a ausência; não criar perfil, fala ou caso. Toda oferta e bônus deve ser comparada aos registros disponíveis de entrega e reclamações. Sem acervo operacional, declare limite. Condições não confirmadas saem da copy e ficam nas notas.

Em `conferencia/checagem-titulos.md`, listar cada pergunta e título de resultado, decisão e justificativa: entende sem contexto? Responde à mesma dimensão? As opções cobrem a situação? O título conclui somente o que os dados permitem? Há afirmação adicional sem prova? Sem caixa alta e sem apelo genérico que substitua clareza. Contar produzidos e revisados com totais iguais.

`shared-references/crivo/07-regua-de-titulos.md` e `scripts/checar_titulos.py` preservam o gate legado para campanhas com perfil e insumos reais. Esse material contém exigências de relatórios e estruturas de campanha que não se tornam campos obrigatórios deste contrato. Não execute `--conferir` com perfil inventado. Quando incompatível, use a conferência explícita acima e registre por que; nunca apresente revisão manual como exit 0 do script. O autoteste do script só verifica o próprio script.

Rode `python3 scripts/lint_copy.py entrega/copy.md`; revise avisos e corrija falhas. Rode também no roteiro e em textos públicos externos ao config. Lint não verifica veracidade: faça a conferência de fontes separadamente. Transcrição literal do estudo fica preservada e identificada, sem alterações para maquiar fala original.

## Navegador

Execute em ambiente isolado com dados fictícios e rede externa bloqueada quando não houver autorização de integração. Teste escolhas reais por botões e teclado. Mantenha log legível com resultados e capturas identificadas:

1. Cada perfil alcançável, combinação mista, empate e todos zero quando possíveis. Explicação e CTA coerentes com as respostas.
2. Voltar, alterar pergunta anterior, preservar resposta válida, remover resposta de pergunta oculta. Recomeçar limpa tudo.
3. Uma e várias seleções, limites, número vazio/inválido/fronteiras, texto vazio e caracteres especiais. Sem execução de texto como HTML.
4. Mídia existente carregada/erro; sem mídia mostrar ausência e roteiro. Não afirmar que um vídeo foi produzido por haver um roteiro.
5. Captura: validação, consentimento, opção sem contato, honestidade sobre envio. Se backend existir, sucesso/erro reais em ambiente próprio, sem dados de pessoas.
6. Reunião: qualificação após convite, elegível com agenda correta, inelegível com alternativa. Checkout: destino consistente. Testar navegação sem comprar, reservar ou enviar formulários externos.
7. Mobile e desktop, sem corte lateral, campos acessíveis, foco, teclado e área de botão legíveis. Verificar imagens capturadas, não apenas gerar prints.

Para pequenas combinações discretas, enumerar todos os caminhos e comparar com regras esperadas independentes do runtime. Para números/textos, testar fronteiras e classes; registrar que não é exaustivo. Não confundir cobertura da árvore com taxa de conversão.

## Relato honesto

`conferencia/testes.md` informa comandos, ambiente, casos, resultado observado e falhas corrigidas. `conferencia/limitacoes.md` distingue aplicação local, integrações, mídias, dados e publicação. Entrega está completa no escopo local quando o quiz executa e as limitações dependentes são explícitas. Só chamar de pronto para operação quando destino, oferta, mídia necessária, captação e integração aplicáveis estiverem confirmados e testados. Nenhum resultado de teste autoriza publicar.

## Regressão reutilizável

`python3 scripts/test_contract.py` valida exemplos e rejeições do contrato com biblioteca padrão. `python3 scripts/test_example_quizzes.py --out /tmp/quiz-ensaio` constrói os dois exemplos e percorre as rotas no Chromium. Esse teste requer Python Playwright, Chromium instalado e ffmpeg disponível no PATH. A dependência ffmpeg produz somente um arquivo branco sintético curto para testar reprodução e erro de mídia, sem voz ou prova comercial. As páginas geradas precisam somente do navegador; o construtor precisa de Python 3.

O teste de navegador bloqueia requests externos e grava resultados e capturas no destino isolado. Os dados usados são fictícios. Os exemplos integram checkout e agenda locais, sem submissão. Não execute o teste sobre destinos comerciais de pessoas reais.
