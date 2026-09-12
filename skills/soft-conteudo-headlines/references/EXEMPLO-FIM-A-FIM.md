# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, número, fala e resultado foram inventados só pra mostrar a
> FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega de
> verdade. Num trabalho real, todo número e toda fala sem fonte nascem marcados `[DADO: confirmar]` e
> o dono confirma antes de sair.

**O caso fictício:** um treinador de corrida de rua que atende corredor amador. Público: gente de 35
a 52 anos que treina 4 vezes por semana pra prova de 10 km e não melhora o tempo há dois anos.
Mecanismo do dono (fictício): o problema não é volume de treino, é a corrida lenta que ele corre
rápido demais. Nome do mecanismo: **Zona 2 Honesta**.

Este arquivo mostra a saída RESUMIDA de cada uma das 4 ações, na ordem. A saída real de cada uma é
bem maior; aqui está só o suficiente pra você reconhecer o formato antes de começar.

---

## O que o dono deu de entrada

Ele escreveu uma frase só:

> "me dá headlines sobre treino de corrida"

Sem número, sem formato, sem falas do cliente. Pedido ABERTO, então a skill entra na **Ação 1,
BANCO COMPLETO**, e antes de escrever qualquer linha roda o Passo 0.

## As perguntas que a skill fez (uma mensagem só, 4 perguntas)

> Antes de escrever, preciso de 4 coisas, pode responder em uma mensagem:
> 1. Teu nicho em 1 linha (quem você atende, não o que você faz).
> 2. Uma dor que o teu cliente fala com as palavras DELE.
> 3. Um desejo que ele fala com as palavras dele.
> 4. O que a tua audiência já conhece: um app, um método, uma prova, um nome que eles citam sozinhos.

Resposta do dono (fictícia):

1. Corredor amador de 35 a 52 que treina pra 10 km e empaca no mesmo tempo.
2. "eu treino todo dia e meu tempo não sai do lugar" (ele diz que ouve isso toda semana, N=6)
3. "queria fechar os 10 km abaixo de 50 minutos" (N=4)
4. Eles falam de relógio Garmin, de "zona 2", da São Silvestre e da planilha do treinador antigo.

Estado de entrada declarado pela skill: **tem fala real com N**. Caminho ideal. O Mapa de Munição da
Audiência veio parcial (desejos, dores e "o que já conhece"); os outros campos ficaram
`[DADO: confirmar]` e não entraram como âncora.

---

## Ação 1 · BANCO COMPLETO, um grupo renderizado

Saída real: `banco-headlines-corrida.md`, com no mínimo 50 fórmulas agrupadas por família de gatilho.
Abaixo, **um grupo inteiro no formato exato da entrega**, pra calibrar. Os outros 49 seguem a mesma
forma.

### Família Reconhecimento

**T80 · Reconhecimento · `Como [DESEJO] se você é [AVATAR]` · gatilhos: Reconhecimento + Recompensa**

- Como baixar de 50 minutos nos 10 km treinando 4 vezes por semana.
- Como voltar a melhorar o tempo depois dos 40, correndo menos.
- Como fechar os 10 km abaixo de 50 se você não tem manhã livre.

**T81 · Reconhecimento · `[X] coisas que só quem é [AVATAR] entende` · gatilhos: Reconhecimento + Mistério**

- 4 coisas que só quem treina há 2 anos sem melhorar o tempo entende.
- 3 frustrações que só o corredor de 40 anos conhece e ninguém posta.
- 5 desculpas que só quem corre de manhã cedo dá pra si mesmo.

**T86 · Reconhecimento · `Se [SITUAÇÃO] acontecer, faça isso imediatamente` · gatilhos: Reconhecimento + Recompensa**

- Se você termina o treino leve ofegante, para hoje e lê isso.
- Se o teu tempo não muda há 6 meses, o problema não é o volume.
- Se o relógio marca zona 3 no treino leve, você está treinando errado a semana inteira.

**Nota do grupo:** as 9 headlines nascem da fala "eu treino todo dia e meu tempo não sai do lugar"
(N=6) e do desejo "abaixo de 50 minutos" (N=4). Nenhuma cita número de resultado do dono, porque ele
não passou prova; assim que passar, entram 2 variações com o número real.

### Como o resto do banco fica organizado

| Família | Fórmulas no banco | Headlines geradas |
|---|---|---|
| Recompensa | 11 | 33 |
| Mistério | 9 | 27 |
| Crença | 8 | 24 |
| Disrupção | 8 | 24 |
| Popularidade / Reputação | 7 | 21 |
| Reconhecimento | 9 | 27 |
| **Total** | **52** | **156** |

Abaixo da tabela, na entrega real, vem a nota de honestidade: quais fórmulas ficaram de fora e por
quê. Neste caso fictício: "3 fórmulas da família Popularidade dependem de citar um nome que o dono
não confirmou que pode usar. Ficaram fora, não inventei o nome."

**STOP.** A pergunta que fecha a entrega: "quais te servem? ajusto, troco de família, ou gero mais?"

---

## Ação 2 · PEÇA ÚNICA, com os tetos contados

Segunda rodada. O dono voltou e disse:

> "quero a capa do carrossel sobre a zona 2"

Formato-destino declarado: **capa de carrossel** (8 a 15 palavras E ≤ 65 caracteres na linha-título).
A skill escolheu 3 fórmulas e contou os dois eixos em cada linha antes de mostrar.

**T5 · Crença · `Crença popular que você quer confrontar`**

| Headline | Palavras | Caracteres |
|---|---|---|
| Correr devagar não te deixa mais lento. Te deixa mais rápido. | 11 | 61 |
| O teu treino leve está rápido demais, e é por isso que empaca. | 11 | 62 |

**T29 · Mistério · `O [melhor/pior] pra [situação] não é X, não é Y, não é Z`**

| Headline | Palavras | Caracteres |
|---|---|---|
| O que segura o teu tempo não é idade, não é peso, não é volume. | 14 | 62 |

**T67 · Crença · `[CONHECIDO], você está fazendo isso errado`**

| Headline | Palavras | Caracteres |
|---|---|---|
| Zona 2: você está correndo ela errado desde o primeiro dia. | 11 | 58 |

Uma quarta headline foi gerada e **reprovada por dentro**, sem ir pro dono: "Descubra o segredo que
vai revolucionar a sua corrida e finalmente soltar o seu tempo." Falhou em quatro checks de uma
vez (frase-emoldura, verbo-clichê de hype, o verbo-freio banido, e zero ancoragem). Regenerada do
zero, virou a linha do T67 acima.

**STOP.** O dono escolhe UMA antes de qualquer corpo de carrossel ser escrito, e a peça segue pra
soft-conteudo-carrossel com essa capa na mão.

---

## Ação 3 · COMPRESSÃO POR FORMATO, a mesma fórmula em 4 tetos

O dono escolheu a linha do T5 e pediu: "essa serve pro reel e pro e-mail também?". A skill não
reescreve o gatilho, aperta a mesma fórmula:

| Formato | Teto | A linha | Contagem |
|---|---|---|---|
| Capa de carrossel | 8 a 15 palavras, ≤ 65 car. | Correr devagar não te deixa mais lento. Te deixa mais rápido. | 11 p · 61 c |
| Reel, 3s falados | ≤ 7 palavras | Correr devagar te deixa mais rápido. | 6 p |
| Reel, texto na tela | ≤ 5 palavras, ≤ 40 car. | Devagar é o atalho. | 4 p · 20 c |
| Assunto de e-mail | 4 a 9 palavras, ≤ 45 car. | Você corre devagar rápido demais | 5 p · 32 c |

O gatilho (Crença atacada) é o mesmo nas quatro. O que mudou foi só quanto texto coube.

---

## Ação 4 · MINERAÇÃO, o veredito de duplicidade

Terceira rodada, semanas depois. O dono colou 12 headlines de perfis de corrida de fora do país e
pediu "olha essas aqui". Sem acesso à web, a skill trabalhou só com o que ele colou e disse isso em
uma linha.

Resultado resumido da rodada:

- 12 headlines analisadas.
- 7 caíram na dedup: já eram T31, T43, T61 e T80 com outra roupa. Nenhuma virou fórmula nova.
- 3 viraram variação de fórmula existente (entraram como exemplo em `templates.md`, não como número novo).
- 2 viraram fórmula nova, somadas ao fim da numeração e marcadas **EXTERNO**, com a origem
  rastreada e a nota de que só viram CASA depois de bater o baseline em 2 peças reais do dono.

**STOP** antes de somar qualquer uma ao banco. O dono aprovou as 2 e reprovou uma das variações; a
reprovada foi pro cemitério de conceitos e não volta de roupa nova.

---

## O que este exemplo prova

1. A skill nunca inventou fala nem número. O que faltou saiu marcado.
2. A entrega foi sempre um documento nomeado, nunca uma lista solta no chat.
3. O gate rodou por dentro: a headline reprovada da Ação 2 não chegou ao dono, e a tabela do gate
   não apareceu na saída.
4. Cada ação parou num STOP e esperou o dono, em vez de emendar na próxima.
