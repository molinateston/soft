# Contrato de configuração e execução

## Fonte única e estrutura

`config.json` é a fonte do render. Contrato `version: 1`, UTF-8. Consulte os dois arquivos completos em `examples/` antes de montar uma configuração; não invente chaves que o runtime não usa.

| Campo | Contrato |
|---|---|
| `route` | `checkout` ou `meeting` |
| `title`, `brand`, `offer` | Texto público confirmado; oferta sem promessa inexistente |
| `profiles` | Lista de `{id,title,body,recommendation,media?,destination?}`; diferenças reais de orientação |
| `tieOrder`, `tieText` | Todos os ids uma vez, na ordem de prioridade do empate, com explicação pública proporcional |
| `steps` | Sequência de estados; cada um tem `id,type,title,purpose` e os campos do tipo |
| `qualification` | Perguntas single posteriores ao resultado/vídeo, para adequação; sem pontuação de perfil |
| `eligibility.all` | Lista de condições combinadas por E; obrigatória na rota reunião |
| `ineligible` | `{message,destination}` obrigatório se houver adequação |
| `capture` | `{mode:"none"}` ou modo `local` com `field: email/phone`, `title,purpose,label,consent` |
| `destination` | `{label,url}` ou `{label,pendingText}`; perfil pode sobrescrever; sem URL de contato ou credenciais |
| `resultMedia` | Mídia comum; perfil pode sobrescrever com `media` |

Ids são únicos. `purpose` é nota do operador. Textos públicos saem via `textContent`, não HTML arbitrário. URLs aceitas: HTTPS ou arquivo relativo dentro do pacote; rejeitar javascript, data, protocolo implícito e caminhos que escapem do pacote. Recursos locais usados devem existir ao gerar. Remotos precisam de teste real de disponibilidade e permissão de uso; o validador não os acessa.

## Estados

- `single`: `options` com `{id,label,scores?}`. `scores` mapeia id de perfil a número. Escolha e confirmação por Continuar.
- `multi`: mesmas opções, com `minSelect` e `maxSelect`. Pontos somam uma vez por alternativa escolhida. Indique limites ao visitante.
- `number`: `min,max,unit`, `step` opcional. Campo começa vazio; número é mostrado no resumo. A base só usa número em elegibilidade ou condição, não inventa fórmula para pontuar; adapte o runtime e teste se for necessário outro cálculo.
- `text`: `maxLength` opcional, `required` padrão verdadeiro. Texto aparece no resumo, sem interpretação semântica implícita.
- `info`: `body` com explicação curta e fonte nas notas.
- `video`: `media` com `title,transcript` e `src` opcional. Sem src, usa `absentText` ou mensagem honesta. `poster` e `captions` são opcionais. Falha de carregamento mostra alternativa textual. Não há bloqueio de CTA pelo tempo do vídeo.

Todos os estados aceitam `when: {question,op,value?}` referindo-se somente a pergunta anterior. Operadores: `eq/ne` para single/text/number; `includes` para multi; `gte/lte` para number; `answered` para resposta preenchida. Condições de adequação também podem referir perguntas de qualificação. A base aceita uma condição por tela e conjunção na elegibilidade; condições compostas adicionais exigem implementação e teste explícitos.

A ordem da lista é a ordem de avanço; a condição pula telas sem criar salto por id. O progresso descreve o caminho ativo atual e se recalcula. Ao voltar, preserva respostas que continuam aplicáveis. Ao mudar uma resposta, descarta respostas de telas que ficam ocultas, inclusive seu efeito na pontuação. Não há persistência após recarregar: documente isso. Se o produto exigir retomada, implemente armazenamento consentido apropriado sem expor contato.

## Resolução e captura

Pontuação soma opções dos estados ativos. Maior total define perfil; empate segue `tieOrder` e informa `tieText`. Todos zero também é empate. Justifique prioridade nas notas. Adequação é independente: todas as condições devem ser verdadeiras. Durante qualificação ainda incompleta não há CTA de agenda. Inelegível recebe mensagem e destino próprios.

No modo local o formulário é opcional, antes do resultado, valida e-mail ou solicita telefone, exige ciência do teste e guarda valor só em memória até sair/recomeçar/alterar percurso. Não faz request, não alega envio e não grava em disco. Não confundir esse teste com captação pronta. O botão Continuar sem contato preserva acesso ao resultado.

A base não recebe leads, não envia mensagem, não paga nem agenda. O link leva ao destino confirmado. Para produção com formulário remoto, implemente endpoint próprio, validação no servidor, finalidade, consentimento, resposta de sucesso/erro, retenção e exclusão definidas. Agendamento externo só é validado como navegação até o teste autorizado; não submeta. Se apenas elegíveis puderem reservar de fato, valide o critério no servidor, porque esconder link no cliente não é controle de acesso.

## Geração e entrega

`python3 scripts/build_quiz.py config.json --out entrega` valida contrato, gera HTML, copia configuração e recursos relativos, e extrai `copy.md`. Usa apenas biblioteca padrão Python. Não sobrescreva personalizações em arquivo existente sem inspecionar antes; regenere em pasta isolada e compare quando houver alterações manuais.

O HTML é autônomo e pode abrir por arquivo. Inter variável e licença OFL estão em `assets/fonts/` e são copiadas para `fonts/` no destino. A página usa `@font-face` local sem CDN. O fallback Arial mantém a leitura se o arquivo não carregar; confira a fonte no navegador.

Aplicações com backend ou lógica fora do contrato podem usar outro código, preservando estados, honestidade, revisão de fontes e testes. Entregue instruções exatas de execução, configuração e dependências; a skill continua responsável pelo conjunto.
