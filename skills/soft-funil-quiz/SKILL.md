---
name: soft-funil-quiz
description: >-
  Planeja, escreve e implementa funil de quiz em qualquer nicho, com perguntas, segmentação, resultados, captura, roteiro de vídeo e aplicação responsiva. Use quando o pedido for: "faz um quiz", "funil com vídeo", "quiz para checkout", "quiz para reunião", "adapta meu quiz". Entrega configuração editável, HTML executável e testes. NÃO use pra: escrever somente uma landing page (soft-funil-landing) ou definir somente a oferta (soft-plano-ofertas). Leia e siga o fluxo inteiro do SKILL.md.
---

# Funil de quiz do planejamento à aplicação

Entregue o quiz funcionando, além do método e da copy. A responsabilidade desta skill inclui página, botões, estados, lógica, resultado, mídia disponível e destino. Landing, design ou sistema podem apoiar internamente; não devolva outra skill como tarefa obrigatória ao usuário. Se o pedido for somente planejamento ou estudo, respeite esse limite.

O princípio ASK preservado é perguntar para entender e adaptar a mensagem à situação declarada. Não trate quantidade de perguntas, perfis, captura anterior ao resultado ou dois vídeos como receita fixa. O tamanho sai das decisões necessárias. Um quiz de adequação pode ter dois resultados. Uma explicação comum pode coexistir com recomendações diferentes, desde que a página descreva essa diferença com honestidade.

## Levantar o mínimo e seguir

Procure primeiro o material existente no destino, perfil, oferta, perguntas, mídia e código que já funcionaram. Leia [método e engenharia das perguntas](references/metodo-quiz.md). Reaproveite somente o que continua coerente com o pedido.

Registre em `planejamento.md`: público e situação, decisão comercial, oferta e operação real, falas literais disponíveis com origem, provas e limites, destino confirmado, critérios de adequação, mídia existente, captura e uso dos dados. Cada afirmação comercial tem origem rastreável. Faça uma pergunta curta pelo conjunto indispensável que faltar; continue o trabalho independente. Não invente perfil, conversa, preço, prazo, agenda, desconto, renda, garantia ou prova para completar um arquivo ou passar num validador.

Sem fala literal, declare a ausência e escreva opções como hipóteses editoriais, sem aspas atribuídas a clientes. Sem prova, corte a afirmação dependente e demonstre o funcionamento real. Informação não confirmada fica em notas como `[A CONFIRMAR: campo]`, nunca como promessa pública. Confronte inclusos, suporte e condições com registros da operação; falhas encontradas exigem decisão registrada, não promessa automática.

Falta de destino, backend ou vídeo bloqueia apenas a integração dependente. Entregue o protótipo funcional com estado honesto e descreva o que falta. Não declare pronto para aquisição se faltar informação essencial de oferta, consentimento ou destino.

## Decidir percurso, perguntas e resultado

Escolha a rota e justifique em uma linha:

- **Compra direta:** perguntas → resultado → vídeo de apresentação, quando necessário → oferta confirmada → checkout. Informar entrega, uso, acesso, suporte, preço e condições realmente disponíveis.
- **Reunião estratégica:** perguntas → resultado → vídeo de convite → qualificação → agendamento para elegíveis; alternativa útil e honesta para os demais. Explicar quem atende, o que acontece, preparo e eventual proposta. Custo e duração só com confirmação.

Pode existir um vídeo explicativo entre blocos de perguntas quando ele muda a compreensão necessária à próxima resposta. Leia [roteiros e rotas](references/roteiros-e-rotas.md) para escrever o vídeo e [estudo Trinca](references/estudo-trinca.md) quando a referência for útil. Observado, interpretação e adaptação são categorias separadas. Nenhuma estrutura observada comprova conversão.

Monte o mapa por estado com id, tipo, texto, alternativas, propósito, variável, condição de entrada, regra de avanço e efeito no resultado. Cada pergunta precisa alterar uma decisão ou trazer informação usada de forma explícita. Declare por que aparece naquele ponto. Opções devem cobrir situações plausíveis sem forçar concordância. Múltipla escolha exige instrução e limites claros. Perguntas dependentes desaparecem quando a resposta anterior muda; respostas ocultas deixam de contar.

Defina perfis por diferença de recomendação, prioridade ou próximo passo. Cubra respostas mistas, empates, dados insuficientes e inelegibilidade. Nenhum perfil sem caminho; nenhuma combinação válida sem saída. Resultado reconhece respostas reais, apresenta conclusão proporcional e indica próximo passo adequado. Orientação comercial não vira diagnóstico clínico, técnico ou garantia.

## Construir ali mesmo

Leia [contrato e execução](references/contrato-aplicacao.md). Use `assets/quiz-template.html` e `scripts/build_quiz.py` como base reutilizável, ou implemente alternativa que preserve os mesmos comportamentos. O contrato aceita perguntas de escolha única/múltipla, número, texto, intersticiais e vídeo, com condições e pontuação. Os exemplos em `examples/` são inteiramente fictícios, para testar mecânica, sem autoridade comercial.

```bash
python3 scripts/build_quiz.py caminho/config.json --out caminho/entrega
python3 scripts/validate_quiz.py caminho/entrega/config.json
```

O HTML gerado abre localmente e funciona sem serviço externo. Instale mídia local no pacote ou indique fonte autorizada e teste carregamento. Roteiro não equivale a vídeo produzido. Sem mídia, mostrar ausência e roteiro em texto, sem player falso. Sem backend, contato opcional fica apenas em memória da página, não persistido nem transmitido; a interface diz isso. Com backend solicitado, implemente e teste contrato, consentimento, resposta de sucesso/erro e proteção de credenciais. Esta base não implementa backend: não basta ativar um campo na configuração.

Use interface enxuta, Inter quando disponível com fallback legível, responsiva, com foco e teclado, progresso verdadeiro, voltar e preservação das respostas ainda válidas. Não simule análise, carregamento, prova ou personalização. Não use contador ou retenção artificial para liberar CTA. O destino precisa corresponder ao perfil e à rota. Contato nunca vai em URL. Regras no navegador servem à orientação; agenda restrita exige controle no servidor se essa restrição for uma exigência operacional.

## Conferir e entregar

Leia [conferência](references/conferencia.md). Entregue na mesma pasta `planejamento.md`, `copy.md`, `roteiro-video.md`, `config.json`, `index.html`, mídia usada e `conferencia/` com regras, fontes, títulos, lint, testes e limitações. A configuração é a fonte da aplicação; a copy deve corresponder ao render. Registre cada alteração de ordem ou perfil com seu motivo, em vez de exigir aprovação a cada fase. Revisões internas não são autorização para publicar.

Execute o lint em toda copy pública e revise todas as perguntas e títulos de resultado: clareza fora de contexto, benefício proporcional, ausência de caixa alta e origem das afirmações. Preserve os scripts legados; use `checar_titulos.py` quando houver perfil e insumos reais compatíveis. Não fabrique esses arquivos para obter exit 0. A revisão explícita da conferência substitui o gate legado quando ele exigir materiais inexistentes ou aplicar regras de anúncio às perguntas funcionais. Pergunta factual pode ser direta, sem sensacionalismo. Não dispense o lint nem a revisão de evidências.

Teste caminhos no navegador, inclusive desktop/celular, mistos/empates, voltar/alterar, condições, captura, mídia e CTA. Teste integrações externas com simulação ou ambiente próprio sem enviar dados reais, comprar ou agendar. Resultado de teste local não comprova recebimento de lead, entrega pós-compra ou conversão.

O relato informa o que funciona, arquivo a abrir, como executar, testes efetivamente feitos e dependências restantes. Se estiver incompleto, use o estado exato: protótipo local funcional, integração pendente ou pronto para revisão. Publicação, mensagens, compra e agendamento dependem da autorização aplicável. Não publique por inferência.
