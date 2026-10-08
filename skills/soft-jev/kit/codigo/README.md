# jev-auto

Pacote Node (ESM, Node >= 22) com o "encanamento" que fala com o TypeSafe Jev: um serviço de IA que
julga perguntas fechadas (`choice`, `noul`, `score`) sobre um pedaço de estado que você manda, e devolve
resposta, probabilidades e confiança. É sempre consultivo (`advisory_only`), nunca trava o trabalho, e
se a rede ou a chave falharem devolve um resultado "indisponível" para o chamador seguir por conta própria.

Três portas de entrada: a **CLI** (`bin/jev`, aponta para `src/cli.mjs`), pensada para hooks e scripts;
um **servidor MCP stdio** (`src/server.mjs`), que expõe a tool `jev_decide` para qualquer agente que fale
MCP; e um **catálogo de decisões prontas** (`src/decisions.mjs` + pasta `decisions/`), perguntas já
desenhadas para tarefas recorrentes, chamáveis por id.

## Comandos da CLI

- `jev --check` — mostra a configuração ativa, sem chamar a rede.
- `jev --smoke` — faz uma chamada real mínima, para confirmar chave e rede.
- `jev --mcp` (ou sem argumento nenhum) — sobe o servidor MCP por stdio.
- `jev --decide` — lê um JSON `{state, questions}` do stdin, devolve a resposta com faixa de confiança.
- `jev --decisions` — lista as decisões do catálogo.
- `jev --decision <id>` — roda uma decisão do catálogo; inputs vêm como JSON pelo stdin.
- `jev --rerank` — reordena uma lista curta de trechos de busca por relevância a uma pergunta.
- `jev ask "<pergunta>" ...` — pergunta fechada avulsa direto da linha de comando.

A credencial vem sempre de `TYPESAFE_API_KEY`; um gerenciador de senhas, se você usar um, é só um atalho
opcional para preenchê-la.

Veja, uma pasta acima, `LEIA-ME.md`, `INSTALAR.md` e `COMO-FUNCIONA.md`.
