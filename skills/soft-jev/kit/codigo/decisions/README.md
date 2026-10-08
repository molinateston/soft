# Catálogo de decisões

Cada arquivo `decisions/<id>.json` descreve UMA decisão fechada que qualquer agente pode
consultar pelo JEV: um texto de estado com placeholders (`state`) e uma ou mais perguntas
(`noul`, `choice` ou `score`) que o serviço responde a partir desse estado. É o mesmo mecanismo
do `jev ask`, só que pré-configurado: a regra e as perguntas já ficam escritas no arquivo, e quem
chama só preenche os campos declarados em `inputs`.

Use este padrão quando a mesma decisão se repete em várias tarefas (por exemplo, toda mensagem de
suporte recebida, ou toda peça antes de publicar) e vale a pena fixar a pergunta uma vez, com
fontes citadas, em vez de escrevê-la de novo a cada chamada.

Para criar a sua própria decisão, copie `exemplo-triagem-mensagens.json` e troque: `id` (letras
minúsculas, números e hífen), `titulo`, `quando_usar`, `fontes` (de onde vêm as regras), `inputs`
(nome do campo -> descrição do que o chamador deve enviar) e `state` (o texto da regra, com
`{{nome_do_input}}` para cada campo). Em `questions`, use `type: "noul"` para sim/não com
probabilidade, `type: "choice"` com um `criteria` fixo, ou `criteria: "@nome_da_lista"` quando a
pergunta escolhe entre candidatos vindos de um input do tipo lista (o catálogo acrescenta sozinho
as opções `nenhum` e `ambiguo`). Todo pergunta recebe o aviso anti-injeção automaticamente; não
precisa escrevê-lo.

Para chamar uma decisão do catálogo pela linha de comando:

    echo '{"resumo": "...", "canal": "email", "sinais_risco": "nenhum", "filas_candidatas": ["Fila A", "Fila B"]}' \
      | node src/cli.mjs --decision exemplo-triagem-mensagens

`node src/cli.mjs --decisions` lista todas as decisões do catálogo (id, título, versão). Campos
com dado sensível (CPF, cartão, segredo) são recusados antes de qualquer chamada de rede; valores
monetários são só mascarados. Suba a `version` sempre que mudar a pergunta ou os critérios — ela
vai junto no log de telemetria.
