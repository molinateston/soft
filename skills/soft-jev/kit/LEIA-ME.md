# JEV automático — leia isto primeiro

## O que é isto

JEV é um juiz rápido de perguntas fechadas: você (ou o próprio agente de código)
faz uma pergunta com opções definidas de antemão — sim/não, escolha entre A/B/C,
ou uma nota de 2 a 10 níveis — e um serviço de IA especializado (chamado
TypeSafe, também citado aqui como "JEV") devolve a resposta mais provável junto
com um nível de confiança. Ele não conversa, não escreve texto livre e não
substitui o seu agente: só responde perguntas fechadas, em menos de dois
segundos.

Este kit pluga o JEV nos "gatilhos" automáticos do seu agente de código
(Claude Code, Codex, Grok ou um agente rodando em Hermes) — os pontos em que o
agente já para naturalmente para ler o seu pedido, escolher uma ferramenta ou
fechar a resposta. Em cada um desses pontos, o agente manda uma ou mais
perguntas fechadas para o JEV, recebe a resposta e segue o trabalho sozinho. O
JEV nunca trava a tarefa nem decide por conta própria: ele só dá uma opinião
rápida, calibrada, para o agente principal usar como quiser.

Fora desses pontos automáticos, o próprio agente também pode chamar o JEV a
qualquer momento no meio da tarefa, sempre que topar com uma decisão fechada —
isso é o comando manual `jev ask` (linha de comando) ou a ferramenta `jev_decide`
(MCP), explicados mais abaixo.

## O que acontece em cada mensagem sua, em ordem

1. **Checagem de preparação.** Antes de começar a trabalhar no seu pedido, o
   agente manda uma única consulta agrupada ao JEV perguntando: isto é uma
   pergunta ou uma ordem? o pedido é curto, médio ou longo? existe alguma
   skill/persona instalada que combina claramente com o pedido? Essa consulta
   já vem com um pacote de perguntas calibradas (chamado aqui de "v3") que só
   aparecem para você quando disparam — ou seja, na maioria das mensagens você
   não vê nada, e só um aviso curto some some quando algo relevante é
   detectado:
   - **"É pergunta, não ordem"** — quando o texto parece uma pergunta genuína
     (não um pedido de ação), o agente é avisado para responder antes de
     alterar qualquer coisa.
   - **"A mensagem tem mais de um pedido"** — quando dá para perceber que você
     fez dois ou mais pedidos na mesma mensagem, o agente é avisado a
     responder todos, não só o primeiro.
   - **"Está pedindo um número do negócio"** — quando o pedido parece pedir um
     valor real (um total, um preço, uma métrica), o agente é avisado a buscar
     esse número numa fonte de verdade, nunca a inventar ou chutar de memória.
2. **Checagem em código de "disse sem provar".** Sem chamar o JEV, uma
   checagem local olha o texto final do agente: se ele afirma ter publicado,
   commitado, testado ou concluído algo, mas o turno não teve o comando
   correspondente rodando de fato (por exemplo, `git log`/`push`, uma
   chamada HTTP real, um teste/build, ou a leitura do arquivo citado), isso
   fica registrado como aviso — a mentira acidental de "dei como pronto sem
   provar" fica visível, mesmo sem gastar uma chamada de IA.
3. **Revisão de fim de turno.** Depois que o agente termina de responder, uma
   checagem final avalia a própria resposta (por exemplo, se ela termina numa
   pergunta desnecessária depois de já ter feito tudo o que foi pedido).
4. **Chamada manual no meio da tarefa.** A qualquer momento, o próprio agente
   pode chamar o comando `jev ask` (ou a ferramenta `jev_decide`, quando
   disponível) para resolver uma decisão fechada sozinho — por exemplo "esse
   log mostra erro ou só aviso?" ou "esse resultado de teste passou?". Isso
   não é automático: é o agente decidindo, no meio do trabalho, que vale a
   pena perguntar antes de seguir.

## Como ler a confiança da resposta

Toda resposta do JEV vem com uma faixa de confiança:

- **Alta** (a resposta parece bem certa): o agente segue direto pela resposta.
- **Média** (a resposta é razoável, mas não muito segura): o agente confirma
  de outro jeito antes de seguir (lendo mais contexto, rodando um comando).
- **Baixa**, ou **"não dá pra dizer"** (o JEV não conseguiu decidir com
  segurança): o agente ignora a resposta do JEV e decide sozinho, com o
  próprio julgamento.

## Custo

Cada chamada custa uma fração de centavo e leva entre 0,25 e 1,4 segundo. Isso
é barato o bastante para rodar em toda mensagem, mas o kit também define um
limite prático de cerca de dez chamadas manuais por tarefa — o JEV é um
auxiliar rápido para decisões pontuais, não um substituto do raciocínio do
agente.

## Próximo passo

Para instalar, veja `INSTALAR.md` — em resumo:

1. Consiga uma chave de acesso ao serviço TypeSafe e coloque-a na variável de
   ambiente `TYPESAFE_API_KEY` (um gerenciador de senhas é só um atalho
   opcional para guardar essa chave, não é obrigatório).
2. Instale o pacote de código deste kit (pasta `codigo/`).
3. Registre os gatilhos no seu agente de código com o instalador incluído.
4. Reabra o agente para os gatilhos entrarem em vigor.
5. Rode o teste de fumaça incluído para confirmar que a chave e a rede estão
   funcionando.
6. Leia `COMO-FUNCIONA.md` se quiser entender os detalhes técnicos por trás
   de cada checagem.

Além desses dois documentos, o kit traz mais dois, opcionais:

- `AUTO-MELHORIA.md` — como calibrar sozinho, com o tempo, o texto e o
  limiar de cada pergunta automática, usando a reação das próprias pessoas
  no dia a dia (com uma implementação de referência rodável em
  `codigo/auto-melhoria/`).
- `PROMPT-ANALISE-90-DIAS.md` — um prompt pronto para colar na sua IA e
  descobrir, a partir do seu próprio histórico de conversas dos últimos 90
  dias, que perguntas automáticas novas valeriam a pena para o seu caso.
