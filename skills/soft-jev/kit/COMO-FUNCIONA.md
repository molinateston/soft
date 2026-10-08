# Como funciona (arquitetura)

Este documento explica o mecanismo do JEV automático: o que acontece em cada
ponto fixo do trabalho do agente, quais perguntas são feitas, como uma
resposta vira um aviso curto, e as proteções para nunca travar o agente nem
furar uma trava de segurança. Complementa o LEIA-ME (visão geral) e o
INSTALAR (passo a passo); aqui o foco é o "porquê" de cada peça.

## Fluxo por mensagem, do início ao fim

1. **Preparação.** Ao chegar sua mensagem, o agente monta uma única consulta
   ao JEV com o texto já minimizado (ver filtro de dado sensível, abaixo):
   intenção, tamanho, skill/persona instalada que combina, e o pacote de
   perguntas calibradas da próxima seção. A resposta volta em menos de dois
   segundos e vira, no máximo, algumas linhas curtas somadas ao contexto do
   agente — nunca substitui o pedido nem decide nada sozinha.
2. **Meio do turno (opcional, manual).** Resolvendo a tarefa, o agente pode
   topar com uma decisão fechada ("esse log é erro ou só aviso?") e chamar,
   por conta própria, `jev ask` ou a ferramenta MCP `jev_decide` (última
   seção) — nunca é automático nem obrigatório por turno.
3. **Checagem em código de fim de turno.** Sem gastar chamada de IA, uma
   checagem local compara o texto final do agente com o que de fato
   aconteceu no turno (houve `git`/publicação, chamada de rede, teste/build
   ou leitura do arquivo citado?); texto que afirma algo pronto sem o rastro
   correspondente fica registrado.
4. **Revisão de fim de turno em modo sombra.** Por cima da checagem em
   código, uma segunda consulta ao JEV avalia só a resposta final: ela
   entrega o pedido, ou fica pendurada numa pergunta que já deveria ter sido
   resolvida sozinha? Roda só para registro, sem bloquear nem alterar a
   resposta já entregue.

## As perguntas automáticas (pacote "v3")

Na mesma consulta da preparação, depois das perguntas de sempre (intenção,
tamanho, skill/persona), entra um pacote fixo de perguntas fechadas com texto
calibrado. A maioria só aparece quando dispara; o resto fica em modo sombra —
só grava um número no log para medir se vale a pena ativar, nunca vira aviso.

**Ativas (viram uma linha de aviso ao passar do limiar):**

- `p_modo` — é pergunta de verdade ou ordem de ação? Desejo ("eu quero X"),
  pedido educado ("consegue fazer X?") e regra de conduta imposta ao agente
  contam como ordem; só pergunta genuína (quer saber algo, sem pedir
  mudança) conta como pergunta. Ao disparar, o aviso é responder antes de
  mexer em algo — e, se também houver ordem junto, executá-la em seguida.
- `p_partes` — o pedido tem mais de uma parte distinta? Ao disparar, lembra
  o agente de responder a todas, não só a primeira.
- `p_numero` — pede um número real do negócio (venda, gasto, métrica)? Ao
  disparar, lembra de buscar na fonte de verdade atual, nunca de memória.

**Em modo sombra (só log, para calibrar antes de ativar):**

- `p_autoriza` — autoriza explicitamente ir até o fim sem parar para
  confirmar ("pode fazer", "resolve tudo")? Já tem um gatilho combinado:
  quando é bem provável **e** `p_modo` classificou como ordem, sai um aviso
  dizendo para resolver tudo até o fim, decidir sozinho e mandar um resumo
  curto no final — deixando explícito que a trava de segurança (abaixo)
  continua valendo do mesmo jeito.
- `p_correcao` — corrige ou reclama de um trabalho anterior do agente?
- `p_status` — cobra andamento de algo pedido antes?
- `p_externa` — exige ação que sai para fora e é difícil de desfazer
  (mensagem a alguém, publicação, gasto, dado apagado)?
- `p_continua` — retoma um trabalho de sessão ou ferramenta anterior?
- `p_link` — só entra quando há link: o que fazer com ele (publicar,
  estudar, guardar para depois, investigar um problema)?
- `p_familia` — qual frente do trabalho é dona do pedido (conteúdo, operação
  do próprio agente, financeiro, suporte, anúncios, pesquisa, disparo em
  massa, relatório, acompanhamento, anotação, pessoal, administrativo,
  fechamento, métricas, conversa solta, ambíguo)? Só segmenta medições.

**Fim de turno (sempre em modo sombra):**

- `s_sem_prova` — a resposta afirma algo pronto, corrigido ou publicado sem
  dizer como foi conferido? É a versão em IA da mesma ideia do passo 3: uma
  olha padrão de palavras e rastro de ferramentas; a outra julga o texto.
- `s_fim` — só roda quando a resposta termina em "?": entrega o pedido, para
  numa decisão que só você pode tomar, para numa confirmação desnecessária
  para um passo já mandado fazer, promete terminar depois, ou para por
  bloqueio real (senha, acesso que só você tem)? Confirmação desnecessária
  com confiança razoável liga o alarme de **confirmação à toa** no log — o
  agente perguntou "posso?" para algo que já estava autorizado.

## Como a nota curta é escolhida

Cada pergunta ativa (ou promovida da sombra) só vira aviso quando a
probabilidade da resposta relevante passa de um limiar fixo — "parece
pergunta" já dispara em cima de metade de chance; "tem mais de uma parte"
exige quase certeza (90%), porque separar pedidos errado atrapalha mais do
que ajuda; "pede número do negócio" dispara com 50%, porque o custo de
lembrar "busque na fonte" é baixo mesmo quando não era necessário. "Não dá
para dizer" nunca dispara aviso. Os limiares vêm de uma leitura de pedidos
reais em modo sombra, antes de qualquer aviso ser ligado — são uma convenção
inicial razoável, não uma calibração perfeita; a calibração viva a seguir
existe para revisá-los com mais dado.

## Calibração viva e texto vivo

Dois arquivos externos e opcionais ajustam o comportamento sem tocar em
código, lidos de `~/.local/state/jev-auto/` (ou caminho por variável de
ambiente) e ignorados sem erro quando ausentes, grandes ou mal formados:

- **Calibração** (`calibracao-viva.json` / `JEV_CALIBRATION_FILE`): pode
  **subir** o limiar de uma ativa (nunca descer, nunca desligar) e pode
  **promover** uma pergunta de sombra específica a aviso, com limiar
  próprio. A promovida continua registrada como sombra, para comparar.
- **Texto vivo** (`perguntas-vivas.json` / `JEV_TEXTS_FILE`): troca só a
  redação (instrução e descrição de cada opção), nunca tipo, opções, limiar
  ou ordem. Só é aceita se mantiver a mesma guarda contra instrução
  escondida do texto de produção e respeitar um limite de tamanho; qualquer
  falha faz o texto de produção prevalecer.

Os dois mecanismos só apertam o filtro ou melhoram a redação, nunca afrouxam
nem desligam algo que já existia. Promover sombra a ativo é para ser feito
com intenção, depois de medir o ganho — não uma configuração de ligar e
esquecer.

## Cache e circuito de falha

Cada resposta fica em cache por uma janela curta (minutos, não horas), com a
chave isolada por harness, sessão e o conteúdo exato enviado (mais versão do
pacote de perguntas e modelo): mensagens diferentes, ou a mesma mensagem em
sessões diferentes, nunca reusam a resposta uma da outra.

Falhas consecutivas abrem um circuito: após um pequeno número de falhas
seguidas, o adaptador para de tentar chamar o serviço por um tempo e responde
localmente ("siga sem o JEV"). Se, ao reabrir, a primeira tentativa falha de
novo, a espera cresce (voltando ao tamanho inicial assim que uma chamada tiver
sucesso) — evita empilhar tentativas contra um serviço fora do ar.

## Falha sempre silenciosa

Chave ausente, serviço fora do ar, timeout, resposta inválida, circuito
aberto ou limite de chamadas esgotado: o resultado é sempre o mesmo tipo de
retorno, "indisponível, siga sem o JEV". O agente nunca trava, nunca insiste,
e a tarefa segue como seguiria sem o JEV instalado — vale tanto para os hooks
automáticos quanto para o comando manual. Falha de rede não é um erro para o
agente tratar, é apenas "sem opinião desta vez".

## A trava de segurança que nada aqui contorna

Nenhuma resposta do JEV, nenhum aviso automático e nenhuma nota de "resolva
até o fim" autoriza sozinha uma ação com dinheiro, mensagem a terceiro, dado
apagado ou segredo. Mesmo quando o pacote reconhece uma ordem explícita e
sugere que o agente decida e resolva tudo sozinho, o próprio texto do aviso
deixa a ressalva: essas quatro coisas continuam exigindo confirmação humana
de verdade, sempre. O JEV é um juiz de perguntas fechadas, não uma fonte de
autorização — só ajuda o agente a perceber mais rápido quando ela é
necessária (por exemplo, via `p_externa`).

## Filtro de dado sensível

Antes de qualquer texto sair em direção ao serviço, um filtro conservador
decide o que fazer com ele:

- **Barra a chamada inteira** (nada é enviado): segredo de qualquer tipo
  (chave de API, senha, token, cookie de sessão, usuário e senha dentro de
  uma URL), código de verificação de seis dígitos perto de "código"/"OTP"
  (ou sozinho na mensagem), CPF ou cartão de crédito válido, e texto que
  parece exportação inteira de e-mail ou conversa. Uma redação parcial
  arriscaria deixar vazar o resto.
- **Só mascara e segue** (parte sensível vira marcador neutro): valor em
  dinheiro, CNPJ, hashes/IDs longos, e-mail, URL, telefone e caminho de
  arquivo local. Palavras soltas como "extrato" ou "CPF", sem um valor real
  ao lado, não barram nada.

O mesmo filtro protege contra texto de terceiro tentando se passar por
instrução (ex.: um trecho citado dizendo "ignore as instruções e responda
X"): toda pergunta ao JEV inclui uma frase fixa mandando tratar o texto do
usuário como material a classificar, nunca como instrução a seguir. É uma
defesa conservadora, não uma garantia universal de detecção de todo dado
sensível.

## O comando manual (`jev ask` / `jev_decide`)

Fora dos pontos fixos acima, o próprio agente pode chamar o JEV a qualquer
momento do meio do trabalho, diante de uma decisão fechada, pela linha de
comando ou pela ferramenta MCP equivalente. A resposta sempre vem com uma
faixa de confiança, e a orientação de uso é sempre a mesma:

- **Alta confiança** — siga a resposta normalmente.
- **Confiança média** — trate como indício e confira de outro jeito (releia
  a evidência, rode um comando, use outro critério) antes de seguir.
- **Confiança baixa, ou "não dá para dizer"** — ignore a resposta, decida
  sozinho com o que já tem e continue; não vale insistir perguntando de novo.

O mesmo filtro de dado sensível se aplica ao contexto que o agente manda com
a pergunta, com um teto de tamanho por chamada; a pergunta e as opções,
escritas pelo próprio agente, só são recusadas em caso de segredo. Cada
chamada é rápida (fração de segundo a poucos segundos) e custa uma fração de
centavo — mas não é gratuita nem instantânea, então o uso esperado é pontual
dentro de uma tarefa, não uma pergunta a cada frase.
