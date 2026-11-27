---
name: soft-vendas-diagnostico
description: "Conduz diagnóstico da operação comercial e entrega decisão baseada em evidências, prioridade e recomendação de intervenção. Use quando o pedido for: diagnosticar o processo de vendas, levantar gargalos comerciais, conduzir entrevista de diagnóstico ou preparar devolutiva antes da oferta. NÃO use pra: preparar dossiê antes da reunião (soft-vendas-call-prep), negociar objeções e fechar (soft-vendas-closer) ou redigir proposta comercial (soft-vendas-proposta). Leia e siga o fluxo inteiro do SKILL.md."
---

# Diagnóstico da operação comercial

Entregue uma decisão sustentada sobre o processo comercial: investigar, corrigir internamente, contratar uma intervenção ou não contratar. Use a identidade, a oferta e a capacidade comprovada do fornecedor informado pelo usuário. Não presuma ferramenta, integração, preço ou promessa de vendas.

Leia [perguntas e evidências](references/perguntas.md) antes da entrevista. Use [registro e devolutiva](references/registro-devolutiva.md) para a saída em Markdown. Consulte [origem e limites](references/origem-limites.md) para atribuir o método corretamente.

## Preparar o recorte

1. Registre objetivo, decisão a apoiar, participantes, período, fontes disponíveis e oferta atual do fornecedor. Peça somente as informações ausentes que possam alterar a conclusão; continue o levantamento independente enquanto isso.
2. Combine um resultado observável com o prospect, como consultar responsável e próxima ação das propostas abertas. Sem critério acordado, mantenha o objetivo como declaração pendente de confirmação.
3. Use dados autorizados. Na devolutiva, substitua identificadores pessoais por referências mínimas. Não publique registros, conversas ou credenciais. Obter informação não autoriza enviar mensagem, alterar CRM ou executar a intervenção.

## Executar as seis etapas

| Etapa | Ação | Saída e condição de avanço |
| --- | --- | --- |
| 1. Definir a decisão | Pergunte o que precisa funcionar melhor, qual episódio motivou o pedido e quem executa ou decide. | Objetivo e critério observável confirmados; se ainda vagos, peça um episódio antes de classificar. |
| 2. Mapear o processo | Acompanhe um caso desde a origem até o desfecho disponível; registre responsáveis, passagens e ferramentas. Pergunte se o exemplo é típico. | Percurso compreensível, período e pontos desconhecidos; restrinja o alcance quando faltar acesso. |
| 3. Avaliar critérios | Selecione práticas relevantes ao objetivo; registre critério, situação, fonte e pendência. | Cada conclusão tem critério e evidência; ausência de prova permanece não verificada. |
| 4. Priorizar | Relacione a falha confirmada com consequência observada; investigue explicações alternativas e escolha a prioridade com o prospect. | Relevância e motivo da escolha registrados; se a dúvida altera a decisão, recomende investigação. |
| 5. Testar a intervenção | Descreva a mudança antes da ferramenta; compare execução interna, ajuste pontual e contratação. Confira capacidade, acessos e responsável. | Relação entre problema, ação e aceite; sem aderência, recomende outra saída. |
| 6. Devolver e decidir | Apresente objetivo, fatos, distância, consequência, prioridade e intervenção. Peça correções e combine próximo passo. | Decisão, divergências, responsável e prazo acordado; registre prazo não acordado quando faltar. |

Não invente confirmação do prospect para completar etapas. Em análise assíncrona, marque decisões dependentes da entrevista como propostas pendentes.

## Classificar sem nota artificial

- **Atende:** a evidência sustenta o comportamento combinado no recorte.
- **Insuficiente:** a prática existe e falha no critério combinado.
- **Inexistente:** a ausência da prática foi confirmada por fonte identificada.
- **Não se aplica:** registre a justificativa ligada ao processo.
- **Não verificado:** falta evidência para concluir, inclusive quando há somente relato ainda não confirmado.

Diferencie fato observado, declaração e hipótese. Um caso consultado não representa toda a operação. Falta de medição comprovada pode ser falha específica, mas não prova desempenho comercial ruim. Não reutilize referências numéricas de mídia paga como metas de vendas.

Informe cobertura por contagem dos estados e critérios fora do recorte, sem nota geral. Se calcular cobertura, declare a fórmula: critérios com evidência conclusiva divididos pelos critérios aplicáveis selecionados; exclua não se aplica do denominador e mantenha não verificado nele. Se o denominador for zero, escreva cobertura não calculável. Cobertura mede alcance da avaliação, não qualidade ou desempenho.

Priorize problemas confirmados que comprometem o objetivo e possam ser tratados nas condições atuais. Resolva primeiro a dependência que bloqueia os demais; se houver empate, peça escolha fundamentada ao prospect considerando a complexidade. Não some pesos arbitrários. Sem fundamento para escolher, priorize obter a evidência que muda a decisão.

## Recomendar com aderência

Complete cada recomendação: “Observamos [fato e fonte], a consequência sustentada é [efeito observado], recomendamos [ação], a verificar por [critério de aceite]”. Reduza a conclusão quando faltar um elo.

Separe consequência observada de causa provável. Não atribua perda financeira, retorno ou aumento de vendas sem dados e premissas verificáveis. O método não possui eficácia comercial validada.

Apresente uma prioridade central e guarde os demais achados no registro. Só recomende oferta quando o escopo, as dependências e a capacidade do fornecedor estiverem confirmados. Diferencie implantação de rotina contínua; a recorrência exige trabalho recorrente identificado. Sem compatibilidade comprovada, proponha validação técnica antes da proposta. Registre alternativas internas e casos sem aderência.

## Conferir a entrega

Grave o diagnóstico em arquivo .md na pasta indicada pelo usuário. Registre fontes, período e limites dentro do arquivo para permitir leitura independente. Reabra o arquivo e confira que outro operador consegue reproduzir classificação, prioridade e recomendação. Rode `python3 scripts/lint_copy.py <arquivo.md>` a partir da pasta desta skill; corrija os apontamentos antes de entregar. Use `scripts/checar_titulos.py --help` se houver títulos de campanha ou conteúdo que exijam sua régua específica.

Devolva o caminho do diagnóstico, a decisão recomendada, o que foi comprovado e a informação ainda necessária. Não envie proposta, mensagem ou documento a terceiros sem autorização específica.
