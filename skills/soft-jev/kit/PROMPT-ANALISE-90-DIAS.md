# Prompt de análise dos últimos 90 dias

Este arquivo traz um prompt pronto para colar na sua própria IA de codificação
(Claude Code, Codex ou outro agente equivalente rodando na sua máquina). Ele
faz a IA reler o histórico real de trabalho dos últimos 90 dias, achar
padrões de erro e acerto, e propor perguntas fechadas novas para o JEV
automático — no mesmo formato das que já vêm no kit — mais um jeito de medir
se cada proposta realmente ajuda antes de ligá-la de vez.

Copie o bloco inteiro (do `INÍCIO DO PROMPT` até `FIM DO PROMPT`) e cole na
conversa com o agente. Depois do bloco, este arquivo explica como usar o
resultado.

---

INÍCIO DO PROMPT — copie a partir daqui

```
Você vai analisar o meu histórico real de trabalho com agentes de IA dos
últimos 90 dias para propor perguntas fechadas automáticas novas (estilo
"JEV": um juiz rápido de perguntas fechadas do tipo escolha entre opções,
sim/não, ou nota em uma escala) que me ajudem a pegar cedo os erros que mais
se repetem. Siga as instruções abaixo na ordem. Você tem acesso de leitura
aos arquivos desta máquina: use-o para achar e ler os históricos você mesmo,
não peça para eu colar nada.

AVISO ANTES DE COMEÇAR, vale para o trabalho inteiro: você vai ler conversas
minhas de verdade, que podem citar nome de cliente, aluno, lead, colega ou
parceiro; valor financeiro; senha, token, chave de API ou outro segredo;
dado de contrato ou de saúde; ou qualquer outra informação identificável de
terceiro. NUNCA copie esse texto original para o relatório final, nem como
"exemplo ilustrativo", nem parcialmente, nem mascarado só na aparência.
Sempre que for citar um padrão, troque por um exemplo curto, genérico e
inventado por você, que preserve a estrutura do problema (o tipo de pedido,
o tipo de erro) sem preservar nenhum conteúdo real. Na dúvida se um trecho é
sensível, trate como sensível e deixe de fora. Todo o trabalho de leitura e
análise acontece localmente, nesta máquina e nesta sessão: não envie o
conteúdo dos históricos para nenhum serviço externo, API, outro chat ou
pessoa; o único lugar onde o conteúdo bruto pode aparecer é no seu raciocínio
interno e, de forma já anonimizada, no arquivo de saída do passo 5.

PASSO 1 — Localizar os históricos.
Descubra onde ficam guardadas as conversas/sessões dos agentes de IA que eu
uso nesta máquina. Você não sabe de antemão quais eu realmente uso: verifique
a existência de cada um destes lugares antes de assumir que ele se aplica, e
ignore os que não existirem ou estiverem vazios.
- Claude Code costuma guardar um histórico por sessão em arquivos de projeto
  sob uma pasta pessoal do tipo "~/.claude/projects" (um subdiretório por
  projeto, um arquivo por sessão).
- Codex costuma guardar sessões sob uma pasta pessoal do tipo
  "~/.codex/sessions" (ou um arquivo de histórico consolidado equivalente).
- Se eu uso algum gateway de agente com plugins/automação rodando na minha
  própria máquina (às vezes chamado de "hermes" de conversa comigo, ou nome
  parecido), ele costuma guardar um banco de estado local (arquivo de banco
  tipo ".db") com o histórico de turnos; procure por esse tipo de arquivo nas
  pastas de configuração desses programas.
  - Também podem existir bancos rotacionados ou "snapshots" antigos desse
    mesmo estado, guardados em subpastas de backup com data no nome; use-os
    também se o histórico ativo não cobrir os 90 dias inteiros.
- Também considere exportações manuais de conversa que eu tenha feito por
  conta própria (arquivos .txt, .md, .json ou .html exportados de WhatsApp,
  Slack, e-mail ou de algum chat de navegador), se existirem em pastas óbvias
  de download ou de documentos.
Para cada fonte encontrada, anote (só para seu controle interno, não
precisa entrar no relatório) o caminho, o formato do arquivo e a faixa de
datas que ele cobre. Se não achar nenhuma fonte, pare aqui e me diga isso
antes de inventar qualquer coisa.

PASSO 2 — Recortar os últimos 90 dias, sem vazar nada para fora.
A partir de hoje, filtre cada fonte para os últimos 90 dias corridos usando a
data de cada sessão/arquivo. Leia o conteúdo direto do disco, com suas
próprias ferramentas de arquivo; não peça a nenhum serviço externo para
processar esse conteúdo. Se um histórico for grande demais para ler de uma
vez, processe em lotes (por exemplo, por semana ou por projeto) e vá
guardando só as observações já anonimizadas do passo 3 em vez do texto bruto,
para não precisar manter tudo em memória.

PASSO 3 — Achar os padrões.
Para cada fonte e cada janela de tempo, procure especificamente por:
- Pedidos repetidos: a mesma pergunta ou o mesmo tipo de tarefa voltando
  várias vezes, sinal de que algo devia ter ficado resolvido ou documentado
  da primeira vez.
- Correções que eu precisei fazer: turnos em que, logo depois de uma resposta
  do agente, eu disse algo como "não era isso", "está errado", "faltou X",
  "não funcionou", ou simplesmente refiz o pedido de outro jeito.
- Casos em que o agente tratou uma pergunta minha como se fosse uma ordem
  (saiu executando, alterando ou criando algo quando eu só queria saber algo)
  ou o contrário (ficou só respondendo/explicando quando eu já tinha pedido
  para ele agir).
- O que o agente esquece ou repete: informação que eu já dei antes e precisei
  repetir, contexto que se perdeu entre sessões, ou passos que o agente refaz
  sem necessidade.
- Qualquer outro padrão claro de atrito que apareça com frequência (por
  exemplo: o agente parar para pedir confirmação de algo que o próprio pedido
  já autorizava; o agente declarar algo pronto sem checar; o agente responder
  só parte de um pedido com várias partes).
Para cada padrão, guarde: uma descrição curta do tipo de situação, uma
contagem aproximada de quantas vezes ele apareceu nos 90 dias, e um ou dois
exemplos — já reescritos por você de forma genérica e fictícia, sem nenhum
nome, valor ou detalhe real, só preservando a estrutura do problema.

PASSO 4 — Propor perguntas novas, casos de teste e um plano de medição.
Com base nos padrões do passo 3, monte três coisas:

4a) Perguntas fechadas automáticas novas. Para cada uma, preencha:
    - id: um nome curto em snake_case.
    - momento: quando ela deveria rodar (por exemplo: antes de começar a
      atender o pedido; no fim do turno, antes de declarar algo pronto; ou
      qualquer outro ponto fixo e repetível do fluxo de trabalho).
    - tipo: "choice" (escolher uma entre opções fechadas predefinidas, cada
      uma com uma definição de uma linha, incluindo sempre uma opção para
      "não dá para saber"), "noul" (uma condição que é verdadeira ou falsa,
      com um grau de confiança entre 0 e 1), ou "score" (uma nota numa escala
      fixa de poucos níveis, por exemplo de 2 a 10, com cada nível descrito
      concretamente).
    - texto da pergunta: a pergunta exata que seria enviada ao juiz de
      perguntas fechadas, incluindo o critério de cada opção (para "choice",
      uma linha por opção; para "noul", o que conta como verdadeiro e o que
      conta como falso; para "score", o que cada nível da escala significa).
    - nota sugerida: a mensagem curta e neutra que o agente veria quando essa
      pergunta disparar (por exemplo, um lembrete de uma linha do tipo do
      erro a evitar), sem incluir nenhum dado real do caso que a originou.
    - limiar inicial: o valor de confiança/probabilidade ou de nota a partir
      do qual essa pergunta deveria disparar, marcado como um chute inicial
      a calibrar (não invente precisão que você não mediu).
    - modo de partida: recomende que toda pergunta nova comece em "modo
      sombra" — ou seja, ela roda e o resultado só é registrado num log
      local, sem aparecer para quem está trabalhando nem mudar nenhum
      comportamento — até haver medição suficiente para confiar nela.

4b) Casos de teste rotulados. Para cada padrão relevante, monte pares
    "pedido → resposta esperada" que sirvam de gabarito para testar as
    perguntas novas: um resumo curto e genérico do tipo de pedido (nunca o
    texto original), o rótulo esperado (por exemplo, qual opção a pergunta
    nova deveria escolher, ou verdadeiro/falso) e uma frase curta explicando
    por que esse é o rótulo certo. Não copie nenhum texto sensível original
    para dentro de nenhum caso; se não conseguir descrever o padrão sem
    reproduzir detalhe identificável, descarte esse caso.

4c) Plano de medição antes/depois. Descreva como comparar, de forma pareada
    (o texto atual e o texto candidato avaliados no mesmo caso, na mesma
    leva, nunca em dias diferentes, para não confundir "melhorou" com "o
    período foi mais fácil"):
    - Taxa de falso positivo: quantas vezes a pergunta nova dispara em casos
      que não deviam disparar (incomoda à toa).
    - Acerto: quantas vezes a pergunta nova bate com o rótulo esperado do
      gabarito do passo 4b.
    - Custo: quantas chamadas ao juiz de perguntas fechadas isso soma por dia
      e quanto tempo isso acrescenta ao fluxo, para não sair caro nem lento
      demais para o volume real de trabalho.
    - Critério de promoção: só mover a pergunta nova do "modo sombra" para
      ativa de verdade se, num conjunto de casos separado que não foi usado
      para desenhar a pergunta, ela empatar ou ganhar do comportamento atual
      em acerto e falso positivo, E não piorar nenhum caso que já era
      acertado de forma consistente antes. Exija um número mínimo razoável
      de casos rotulados por pergunta antes de confiar no resultado (poucas
      dezenas, não 2 ou 3 casos) — se não houver casos suficientes, registre
      isso e recomende continuar coletando em vez de promover.

PASSO 5 — Escrever a saída em arquivo, não só responder no chat.
Grave tudo isto num arquivo novo de saída (sugestão de nome:
"analise-jev-90-dias.md", na pasta atual ou em outro lugar que você ache mais
adequado nesta máquina) com estas seções: resumo em poucas linhas; onde os
históricos foram encontrados e qual janela de datas cada fonte cobriu;
padrões encontrados (com contagem aproximada e exemplos já anonimizados);
perguntas novas propostas (uma tabela ou lista com os campos do passo 4a);
casos de teste rotulados propostos (passo 4b); e o plano de medição
antes/depois (passo 4c). Ao final, me avise em poucas linhas, no chat, que o
arquivo foi escrito e onde ficou, sem repetir o conteúdo inteiro na
conversa.
```

FIM DO PROMPT — copie até aqui

---

## Como usar

1. Cole o prompt acima no mesmo agente que já roda o seu dia a dia (o que tem
   acesso de leitura aos arquivos e pastas de histórico da sua própria
   máquina) — não em um chat separado sem esse acesso, e não em um serviço
   de terceiro.
2. Rode e espere o arquivo de saída ser escrito; não é para virar só uma
   resposta longa no chat.
3. Leia o arquivo gerado com atenção antes de aplicar qualquer coisa. Confira
   em especial se os "exemplos anonimizados" realmente não sobrou nenhum
   nome, valor ou detalhe identificável — a IA pode errar nisso, a checagem
   final é sua.
4. Trate o arquivo de saída com o mesmo cuidado que os seus outros arquivos
   de trabalho: mesmo anonimizado, ele descreve como você trabalha, então não
   é para postar num grupo público nem mandar para terceiros sem revisar.
5. Cada pergunta nova proposta deve nascer em modo sombra (só log, sem
   aparecer nem mudar nada) — nunca ligue uma pergunta nova direto em
   produção.
6. Deixe rodando em modo sombra por um período (por exemplo, uma a duas
   semanas de uso real, ou o tempo que levar para juntar algumas dezenas de
   casos) antes de olhar os números.
7. Só ative de vez a pergunta se ela cumprir o critério de promoção descrito
   no plano de medição (empatar ou ganhar em acerto e falso positivo num
   conjunto de teste separado, sem piorar nenhum caso que já ia bem, com
   casos suficientes para confiar no número).
8. Se não cumprir o critério, não é para descartar sem mais: ajuste o texto
   da pergunta ou o limiar e teste de novo em sombra, ou deixe coletando mais
   casos antes de decidir.
9. Repita este prompt de tempos em tempos (por exemplo, a cada 90 dias) — o
   seu jeito de trabalhar muda, e perguntas que faziam sentido antes podem
   deixar de ser úteis, além de aparecerem padrões novos.
10. Este prompt não depende de nenhuma ferramenta ou empresa específica além
    do próprio agente de codificação que você já usa; adapte os nomes de
    pasta do passo 1 se o seu agente guardar histórico em outro lugar.
