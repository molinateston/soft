---
name: soft-conteudo-ganchos
description: >-
  Escolhe e preenche o GANCHO UNIVERSAL: a primeira linha (falada nos 3 primeiros segundos, na tela ou escrita) que serve a qualquer conteúdo ou encaixa no conteúdo que o dono já tem, sem lacuna ou com lacuna ampla, num banco de 260 moldes e 346 frases literais, com selo de prova. Preenche com a fala do cliente e a prova do dono, confere no gate de copy e entrega em .md. Use quando o pedido for: "me dá um gancho pronto", "banco de ganchos", "molde de gancho", "gancho pra esse conteúdo que eu já tenho", "gancho que serve pra qualquer reel", "preenche esse molde", "modela esse gancho que viralizou", "CTA pro fim do post". NÃO use pra: a linha construída a partir de uma dor, objeção ou número do dono, com o conteúdo nascendo dela (soft-conteudo-headlines); o roteiro do reel (soft-conteudo-reels); os slides (soft-conteudo-carrossel); o gancho no vídeo já gravado (soft-editor-video); abertura de story (soft-conteudo-stories); criticar copy pronta (soft-critico-copy). Leia e siga o fluxo inteiro do SKILL.md.
---

# Ganchos prontos: o molde certo, preenchido com o que só o dono tem

Esta skill acha o gancho de uma peça num banco de moldes prontos e preenche as lacunas com a fala real do cliente e a prova do dono. Gancho é a primeira coisa que o público vê: a capa (primeira lâmina) do carrossel ou os 3 primeiros segundos do reel. O banco tem 260 moldes em 17 famílias e 54 quadros alternativos, cada um com o selo de prova (medido ou sem medição), o formato onde encaixa e o teto de palavras, organizados em 21 cartões de framework (15 de família e 6 de tipo de conteúdo). A skill abre o cartão certo, confere o que ele exige do insumo, oferece 3 moldes por rodada, o dono escolhe um, ela preenche pelos passos do cartão, passa na régua de títulos e no gate de copy e entrega tudo numa pasta, com o gancho num arquivo `.md`.

Ela acelera; não substitui ninguém. A **soft-conteudo-headlines** continua sendo o método que cria a headline do zero a partir da tese. A **soft-conteudo-reels** e a **soft-conteudo-carrossel** escrevem o corpo da peça e resolvem o gancho sozinhas quando o dono não passa por aqui. Use esta skill quando o dono quer partir de um molde que já funcionou, ou não sabe por onde começar a abertura.

**O passo central: molde solto não é gancho.** O molde é ponto de partida. Ele só vale depois de preenchido com o assunto real do nicho do dono, a cena do cliente e um fato que só o dono pode afirmar (número, caso, tempo de casa). Molde preenchido com palavra vaga ("vai mudar sua vida") reprova no teste do concorrente; molde que termina em palavra-ponteiro ("use isto") reprova na régua de títulos, porque a frase não se explica sozinha. No gate real, os ganchos que passaram nomeiam o objeto do ofício e trazem um fato que só o dono afirma (número, caso ou mecanismo).

## Qual skill: headline ou gancho (a mesma primeira linha, dois caminhos)

| O dono | Skill |
|---|---|
| tem uma dor, objeção, número, cena ou prova e quer a linha construída com ela, para fazer o conteúdo DEPOIS e em cima dela ("penso 5 dores do nicho") | `soft-conteudo-headlines`: a linha tem lacunas específicas que ele preenche |
| quer uma linha que serve a qualquer conteúdo, ou que encaixa no conteúdo que já tem, sem lacuna ou com lacuna ampla ("o que eu nunca mais faço depois de 10 anos de [profissão]") | `soft-conteudo-ganchos` |
| o roteiro do reel inteiro, depois da linha | `soft-conteudo-reels` |
| os slides do carrossel, depois da capa | `soft-conteudo-carrossel` |

Falada nos 3 primeiros segundos, na tela ou escrita (capa, título, assunto, manchete) é só o formato: as duas skills servem aos três. Dúvida entre elas: o conteúdo já existe (gancho) ou vai nascer da linha (headline)? Pergunte isso ao dono em uma linha. As duas têm banco de moldes e banco de frases literais, por família e por alcance; cada uma tem o índice em `references/literais/00-indice.md`.

## O que é "pronto" nesta skill

A entrega existe quando:

1. a pasta de saída `ganchos-<slug>/` (slug curto do tema, sem espaço nem acento; sem pasta definida, dentro da pasta atual) tem o arquivo `ganchos-<slug>.md` no formato de "A entrega" e a subpasta `conferencia/` com `titulos.txt`, `checagem-titulos.md` preenchida e o veredito do gate;
2. a régua de títulos rodou em todo texto que o público lê como título (o gancho falado, o texto na tela, a capa e o CTA) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0, com a última linha colada no relato;
3. `python3 scripts/lint_copy.py <arquivo>` devolve exit 0 em cada `.md` da pasta, com uma linha `<arquivo>: exit 0` por arquivo no relato;
4. o veredito do gate de copy está colado inteiro em `conferencia/` (o da soft-critico-copy, ou o gate de bolso desta skill quando ela não está instalada, dito com todas as letras). Peça de conteúdo só sai pronta com APROVADA; peça que vende só sai pronta com nota 10, e abaixo disso a decisão é do dono (ver "O gate");
5. nenhum dado foi inventado: `python3 scripts/conferir_fontes.py --gancho <pasta de saída> --insumos <pasta de insumos do dono>` devolve exit 0 (todo número, nome próprio e aspa do gancho aparece no insumo, e nenhuma lacuna sobrou), com a saída em `conferencia/fontes.txt`. O que faltou vira pergunta ao dono antes de escrever, ou a frase sai na versão que dispensa o dado.

**A pasta de insumos.** O gate procura a origem de cada número, fala e palavra de CTA nos insumos do dono. Se ele já tem perfil salvo (posicionamento, provas, banco de falas), use a pasta que contém esse perfil, nunca uma subpasta dela. Se não tem, grave as respostas das perguntas 4 e 5 (e a palavra do CTA, quando houver) em `insumos/perfil.md`, na pasta de trabalho do dono, uma por linha começando com `- `, com a origem e a autorização ao lado de cada fala de cliente. A pasta `insumos/` é o `--insumos` e o arquivo é o `--perfil`. Nada do dono é gravado dentro da pasta da skill.

Sem isso, não diga "pronto": diga o que falta. Esta skill é a pasta que contém este arquivo e a subpasta `scripts/`; se você leu este texto de uma cópia sem `scripts/`, abra a pasta instalada.

## Primeiros passos (diga isto antes da primeira pergunta)

Fale com as suas palavras, cobrindo:

- **O que vou te pedir:** cinco coisas, uma de cada vez: o formato (reel ou carrossel), o tipo de conteúdo, o objetivo da peça, o público com uma cena dele, e a fala do cliente com a sua prova.
- **Quanto leva:** com a fala do cliente à mão, umas 6 a 8 mensagens até o gancho final.
- **O que você recebe:** uma pasta com o gancho escolhido num arquivo `.md`, já preenchido, contado no teto do formato e conferido, pronto pra colar na capa ou gravar. A conferência fica numa subpasta que você não precisa abrir.
- **O que só você pode trazer:** a frase que o cliente falou, de onde ela veio e se você pode publicar, e a sua prova (um número, um caso, o tempo de casa). Sem isso eu deixo o gancho em aberto e te pergunto; não invento.
- **Como funciona depois:** você pede "mais 3", "outra família", "versão pro reel" ou "o CTA do fim", e eu sigo de onde paramos.

Se o perfil do dono (posicionamento, banco de verbatim, provas) já estiver no contexto do agente, leia antes de perguntar: ele pode responder sozinho as perguntas 4 e 5.

## Palavras que o dono vai ouvir

Explique na primeira vez em que a palavra aparecer, com a frase da tabela. Depois, use a palavra simples.

| Palavra | Explicação em uma frase |
|---|---|
| gancho | a primeira frase ou imagem da peça, a que faz a pessoa parar de rolar |
| molde | um gancho que já funcionou, com as partes trocáveis em colchetes |
| lacuna | a parte entre colchetes, que você preenche com o seu assunto |
| família | o tipo de efeito do gancho: reconhecer o público, provocar, perguntar, abrir mistério, alertar |
| universal | molde que serve pra qualquer assunto |
| específico | molde que só prende quando a peça entrega aquele tipo de conteúdo, como uma lista ou um tutorial |
| selo de prova | se a forma do molde foi medida em posts reais (com número) ou ainda não tem medição; o seu gancho preenchido é uma variante, sem medição própria |
| cartão | o roteiro de uma família ou de um tipo de conteúdo: o que precisa existir antes, os passos, os erros que o juiz reprova e os moldes |
| quadro alternativo | outra frase pro mesmo molde (Q01 a Q54), já na forma que a conferência aceita |
| força e mediana | força é quantas vezes o post rendeu acima do normal da conta; a mediana é o resultado típico, e é ela que vale olhar |
| teto | o máximo de palavras que cabe no formato: 7 faladas no reel, 5 na tela do reel, de 8 a 15 na capa |
| verbatim | a frase do cliente, com as palavras dele |
| lastro | a prova que sustenta o que o gancho afirma: número, caso, tempo |
| palavra-ponteiro | uma palavra como isto, isso ou esse, que aponta pra uma coisa sem dizer qual; no gancho final ela dá lugar ao nome da coisa |
| teste do concorrente | cobrir o nome da sua marca e do seu método e imaginar a frase no perfil do concorrente mais próximo do seu nicho; se ela ainda funciona lá, está genérica |
| régua de títulos | a conferência de cada frase que o público lê como título: se ela afirma algo, se se explica sozinha, se tem dois gatilhos |
| gate | a conferência antes de entregar: o lint, a régua de títulos e a crítica de copy |
| falar, mostrar, texto na tela | as três frentes do gancho de reel: a frase dita, a cena, a frase escrita por cima |

## Três jeitos de entrar

**1. "Já sei o formato e a família"** ("gancho de Erro pra capa do meu carrossel de lista"). Confirme em uma linha o que entendeu, pergunte só o que falta (quase sempre a pergunta 5, a fala e a prova) e vá direto pra rodada de moldes.

**2. "Não sei, me guia"** ou pedido solto ("me dá um gancho"). Siga o roteiro abaixo, uma pergunta por vez.

**3. "Esse gancho funcionou, modela pra mim"** (o dono traz um post dele ou do mercado que já rendeu). Siga "Gancho de referência validada", mais abaixo.

Pedido ambíguo ("me ajuda com a abertura"): pergunte uma coisa só, se ele quer partir de molde pronto (aqui) ou criar do zero pela tese (soft-conteudo-headlines), e siga pela resposta.

## O roteiro, uma pergunta por vez

Abra cada pergunta com "Pergunta N de 5" e diga em uma linha o que vem depois. Grave cada resposta no rascunho antes de fazer a próxima; as respostas das perguntas 4 e 5 vão pro perfil do dono (ver "A pasta de insumos"). Resposta que já veio no pedido não se pergunta de novo.

### Pergunta 1 de 5. O formato

- **Pergunte:** "Esse gancho vai pra capa de um carrossel ou pro começo de um reel? Se for reel, você vai falar olhando pra câmera, mostrar uma cena, ou escrever a frase na tela?"
- **Por que:** cada formato tem um teto. Reel falado aguenta 7 palavras, a tela do reel 5, a capa de 8 a 15. Molde que não cabe no formato sai da lista.
- **Onde achar a resposta:** no que ele já planejou postar. Se não planejou, o carrossel é melhor pra conteúdo que a pessoa salva; o reel é melhor pra alcançar quem não conhece.
- **Se não souber:** pule pra pergunta 3 e sugira pelo objetivo, com a regra da casa: reel atrai quem não te conhece, carrossel vende e é o que a pessoa salva. Depois volte pra pergunta 2. Dá pra adaptar o gancho pro outro formato no fim.
- **Depois:** o tipo de conteúdo.

### Pergunta 2 de 5. O tipo de conteúdo

- **Pergunte:** "O conteúdo que você vai fazer tem um formato próprio (uma lista, um tutorial passo a passo, um comparativo, uma história sua, um resultado com número, uma peça de ânimo) ou é um assunto livre?"
- **Por que:** gancho específico só prende se a peça entrega aquilo. Um gancho de lista na frente de um texto corrido promete o que não tem, e o público sai. Assunto livre usa os moldes universais; formato próprio usa os específicos daquele tipo, mais os universais.
- **Onde achar a resposta:** no rascunho ou na ideia da peça. Conte os itens: se dá pra numerar, é lista; se tem passos em ordem, é tutorial.
- **Se não souber:** trate como assunto livre e avise que um formato próprio, quando aparecer, abre moldes que prendem mais.
- **Depois:** o objetivo da peça.

### Pergunta 3 de 5. O objetivo ou a emoção

- **Pergunte:** "O que você quer que a pessoa faça ou sinta com essa peça: parar e se reconhecer, salvar, comentar, mandar pra alguém, te seguir, ou comprar?"
- **Por que:** o objetivo escolhe a família do molde (tabela abaixo). E peça que vende passa num gate mais duro.
- **Onde achar a resposta:** na meta da semana. Se ele não tem, alcance (parar e se reconhecer) é o ponto de partida mais comum.
- **Se não souber:** use alcance e diga isso.
- **Depois:** o público.

### Pergunta 4 de 5. O público e uma cena dele

- **Pergunte:** "Pra quem é essa peça, e em que momento do dia essa pessoa vive o problema? Me dá uma cena: um lugar, um objeto ou um horário."
- **Por que:** a cena é o que o concorrente não tem. "Mulheres empreendedoras" qualquer um escreve; "a dona do brechó que fotografa peça no chão do quarto depois de fechar a loja" só quem conhece escreve.
- **Onde achar a resposta:** nas últimas conversas com cliente, no direct, nas perguntas que mais chegam.
- **Se não souber:** pergunte "me conta do último cliente que te procurou: o que estava acontecendo na vida dele naquele dia?"
- **Depois:** a fala do cliente e a sua prova.

### Pergunta 5 de 5. A fala do cliente e a sua prova (em duas partes)

Faça em duas mensagens, uma parte de cada vez.

**Parte 1, a fala e de onde ela veio.**

- **Pergunte:** "Me passa uma frase que um cliente te disse sobre esse problema, com as palavras dele. De onde ela veio (comentário público, depoimento que ele te mandou pra usar, conversa no direct ou no WhatsApp) e ele autorizou você a publicar?"
- **Por que:** a fala vira a lacuna do molde quase intacta e faz o público se reconhecer. Mas fala de conversa privada sem autorização não vai pro público, nem sem o nome, e quem ainda não comprou nunca vira "uma aluna" ou "uma cliente" na peça.
- **Onde achar a resposta:** print de conversa, áudio transcrito, comentário, avaliação. A autorização é uma mensagem da pessoa dizendo que pode, com a data.
- **Se não souber a origem ou não tiver autorização:** a fala serve pra você entender a dor, e o gancho usa a cena com as suas palavras, sem aspas e sem atribuir a ninguém. Se a pessoa tem assunto em aberto com o dono (reclamação, cobrança, negociação), a fala fica fora desta rodada.
- **Como gravar no perfil:** `- Fala de cliente: "<as palavras dele>" · origem: <onde> · autorizado por <dono> em <data>`, ou `· sem autorização: só como cena`.

**Parte 2, a prova que vai na linha.**

- **Pergunte:** "Agora a sua prova: um número ou uma credencial que só você pode afirmar (clientes atendidos, anos de casa, um resultado com registro, um teste que você fez). Qual deles pode ir na frase do gancho?"
- **Por que:** o gate cobre o nome da sua marca e do seu método e pergunta se a frase ainda funcionaria no perfil do concorrente mais próximo. A fala do cliente mostra a dor; o que prova que a frase é sua é o número ou o caso que só você tem. **Avise o efeito nos tetos:** reel falado aguenta 7 palavras, a tela 5, a capa até 15 palavras e 65 caracteres. Quase nunca cabem a fala e o número na mesma frase: um vai na linha principal, o outro numa frente vizinha (a tela, a fala, o slide 2), e nenhum dos dois some.
- **Onde achar a resposta:** nos seus números: planilha, relatório, print do caixa, contagem de clientes. Resultado de cliente só com registro e autorização.
- **Se não souber:** siga com o que tem e diga que a frase vai ficar mais fraca no teste do concorrente. Nunca preencha com algo que parece real.
- **Depois:** a rodada de 3 moldes.

## Do objetivo ao cartão (índice de frameworks)

Cada família e cada tipo de conteúdo tem um cartão em `references/frameworks/<cartão>.md`: a condição de entrada (o que precisa existir no insumo e a pergunta exata quando falta), a estrutura obrigatória do gancho, os passos, os erros que o juiz reprova com a forma que passa, um exemplo bom e um ruim, os tetos e os moldes do cartão. Mapa de uso da casa, sem medição por trás. O índice do banco é `references/banco-moldes.md`, e os moldes moram em `references/banco/`.

| Cartão | Família ou tipo de conteúdo | Objetivo que costuma servir |
|---|---|---|
| `01-reconhecimento` | Reconhecimento | parar e se reconhecer (alcance) |
| `02-disrupcao-e-troca` | Disrupção e troca | parar e se reconhecer, salvar |
| `03-pergunta-e-comentario` | Pergunta e convite ao comentário | comentar |
| `04-irresistiveis` | Irresistíveis | parar, mandar pra alguém |
| `05-humor-e-pauta` | Humor e pauta do momento | parar (alcance) |
| `06-urgencia-e-retencao` | Urgência e retenção | comprar com prazo real, medo de errar |
| `07-popularidade-e-autoridade` | Popularidade e autoridade | seguir |
| `08-recompensa` | Recompensa | salvar |
| `09-misterio-e-segredo` | Mistério e segredo | curiosidade |
| `10-crenca` | Crença | comentar, seguir |
| `11-historia` | História | seguir |
| `12-erro-e-alerta` | Erro e alerta | salvar, comprar, medo de errar |
| `13-estado-emocional` | Reconhecimento por estado emocional | mandar pra alguém |
| `14-numero-e-lista` | Número e lista | salvar |
| `15-prova-e-resultado` | Prova e resultado | comprar |
| `16-tipo-lista` | tipo lista | a peça entrega itens contados |
| `17-tipo-tutorial` | tipo tutorial | a peça ensina passos ou um modelo |
| `18-tipo-comparativo` | tipo comparativo, com a família Comparativos | a peça compara A e B |
| `19-tipo-historia` | tipo história | a peça conta um caso vivido |
| `20-tipo-resultado` | tipo resultado | a peça mostra um número com registro |
| `21-tipo-motivacao` | tipo motivação, com a família Motivação e mentalidade | a peça dá ânimo |

## A rodada: o cartão e os 3 moldes

1. **Escolha o alcance:** assunto livre fica nos universais. Formato próprio soma o cartão do tipo (16 a 21) ao cartão da família.
2. **Abra o cartão** da família do objetivo e, se houver, o do tipo. Leia só esses cartões e os arquivos do banco que eles apontam.
3. **Confira a condição de entrada do cartão** contra as respostas e o perfil. Faltou um dado: faça a pergunta do cartão, uma por vez, e não ofereça molde que depende dele.
4. **Filtre pelo formato e pelo teto:** colunas Formato, Reel e Teto da linha do banco.
5a. **Mais opções ou a frase como o mercado escreve:** se o dono pede mais do que os 3 moldes, abra `references/literais/00-indice.md` e ofereça 3 frases de padrões diferentes do mesmo cartão e alcance. Frase literal é ponto de partida: a lacuna se preenche com a cena e a prova do dono, e o gate vale igual.
5. **Ordene pela mediana**, não pela força média: a força de 2024 está inflada por picos. Molde com 1 abertura medida é aposta; sem medição entra quando encaixa melhor, dito assim. Quadro alternativo conta como opção do molde pai.
6. **Varie e reserve:** os 3 vêm de pelo menos 2 famílias, e com formato próprio pelo menos 1 vem do cartão do tipo. Se sobrarem menos de 3 que cabem no teto, abra outra família antes de oferecer molde acima do teto, e diga ao dono que o objetivo pedido fica com o CTA do fim.
7. **Diga o selo como ele é:** a medição é da forma do molde; o gancho preenchido será variante sem medição própria. "Medido na forma original" teve o texto mudado depois da medição, e a nota diz o quê.

Mostre cada um assim, e pare pra o dono escolher:

```
1. G010 · Disrupção e troca · universal
   Em vez de [o que todo mundo usa], [use ou faça o substituto, nomeado]
   por que pra você: <uma linha ligada à cena ou à fala dele>
   prova: medido na forma original, mediana 27,3x, 11 aberturas; a sua versão é variante sem medição · teto: falado até 7 palavras
```

Feche com: "Qual dos 3? Se nenhum servir, peço mais 3 de outra família." As visões por formato (`references/visao-reel.md` e `references/visao-carrossel.md`) dão a ordem de escolha e o que mais rendeu em cada um.

## O preenchimento

1. **Siga os passos do cartão, e cada lacuna recebe dado do dono:** a fala do cliente, a cena (lugar, objeto, horário), o número com fonte. O exemplo do banco é inventado e mostra a forma: não copie o dado, use o seu.
2. **Lacuna sem dado não vira marcador no gancho.** Pergunte ao dono antes de escrever, ou escreva a versão da frase que dispensa o dado. É proibido inventar número, nome, prazo ou resultado.
3. **Toda frase se explica sozinha.** Leia cada frase como se ela caísse solta no feed de quem nunca te viu: ela diz o quê, pra quem e o que muda? Palavra-ponteiro (isto, isso, esse, assim) e palavra abstrata sem o nome ao lado ("a ordem", "o método", "essa virada") dão lugar ao objeto: "use isto" vira "use azeite". O nome do método do dono só entra explicado na mesma frase. O antecedente vale quando está na mesma frase: "estes números da parede" passa, "estes números" sozinho não.
4. **Nenhum verbo órfão.** Todo verbo leva o objeto dito na mesma frase: "testei" vira "testei as plantas do banheiro", "use" vira "use azeite", "cobre" vira "cobre pelo custo da fatia". Sublinhe cada verbo antes de entregar e confira.
5. **Teste do concorrente, o mesmo do gate, antes da crítica:** cubra o nome da marca e do método e imagine a frase publicada no perfil do concorrente mais próximo, do mesmo nicho: tem que sobrar um fato, número, caso ou mecanismo dito em palavras simples que só o dono tem. Se não sobra, volte pra prova da pergunta 5. Trocar o nicho na cabeça (inglês por violão) é só o pré-filtro: se a frase serve igual em outro nicho, já reprovou; se não serve, ainda falta o teste do concorrente.
6. **Conte o teto, de fato:** `echo -n "a frase" | wc -w` pras palavras e `| wc -m` pros caracteres; número em algarismo conta 1 palavra. Estourou: corte o enfeite, depois a palavra de ligação, e preserve o fato do dono, um elemento concreto de cena ou de público e o gatilho. Abaixo do mínimo da capa (8 palavras): acrescente a cena, o público ou a prova, nunca enfeite. Se cortar mata o gatilho, leve o molde pra outro formato ou volte pra rodada; molde marcado acima do teto pede conversa com o dono.
7. **Uma frase só por linha.** Duas frases separadas por ponto, a segunda corrigindo ou completando a primeira, gastam a cota de 1 antítese por lote da régua de títulos (o lote é o gancho com o CTA). Junte numa frase quando der; os moldes que só funcionam em duas frases trazem o aviso na nota.
8. **Capa ou gancho de peça que vende traz a estrutura-mãe do gate:** o Diagnóstico (o que o leitor vive, de preferência na fala do cliente) e a Nova interpretação (a causa que ele não via) comprimidos numa frase. Molde de lista, de curiosidade ou de experimento que não carrega os dois ganha a causa na própria linha, ou a capa troca de molde e o experimento vai pro slide 2.
9. **Duas versões quando der,** com cenas ou provas diferentes, pra o dono escolher.
10. **No reel, diga a frente, e a imagem não salva a frase:** o que é FALAR, o que é TEXTO NA TELA, o que é MOSTRAR. Uma frente já segura; duas em conflito multiplicam. Quando o teto de uma frente não comporta a prova, ela vai pra outra frente e nunca some. O MOSTRAR e a arte da capa só contam como prova ou explicação quando a fala, a tela ou a legenda dizem o que aparece.

## A régua de títulos (roda antes da crítica)

O gate de copy roda primeiro a régua de títulos sobre todo texto que o público lê como título; aqui, o gancho falado, o texto na tela, a capa e o CTA. A régua inteira mora na soft-critico-copy, no arquivo da régua de títulos dentro das referências daquela skill. Estas são as regras que mais derrubam gancho, e cada uma ganha resposta escrita em `conferencia/checagem-titulos.md`, uma linha por título:

- **Afirma algo a mais que o pedido:** cole o pedido do dono e o título, um embaixo do outro, e escreva o que o título afirma a mais (inimigo nomeado, ordem invertida, custo, troca ou um resultado). Célula vazia reprova.
- **Não é item de sumário:** reescreva o título como item de índice de aula ("5 plantas pra banheiro escuro", "Como cobrar o bolo"); se ficou igual ou quase igual, ele só descreve e reprova.
- **Se explica sozinho:** se a pergunta natural de um estranho é "usar o quê?" ou "que números?", reprova.
- **Um copywriter de ponta assinaria?** "Não" ou "não sei" obriga a reescrita, e é a reescrita que vai pro arquivo, com a versão anterior colada ao lado em `reescrito de:`.
- **Dois gatilhos da lista fechada** em cada título: Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento. Formato, atributo e tema não contam.

O fecho sai de script, em 3 passos, rodados da pasta da skill:

1. `python3 scripts/checar_titulos.py --peca <pasta de saída>/ganchos-<slug>.md --titulos <pasta de saída>/conferencia/titulos.txt --insumos <pasta de insumos do dono> --perfil <perfil do dono>` (um título por linha em `titulos.txt`, copiado da peça caractere por caractere; o script conta o molde de antítese do lote, teto 1), com a saída inteira colada em `checagem-titulos.md`;
2. troque cada `<preencher>` pela resposta, e nada mais;
3. rode o `--conferir` da definição de pronto. Exit diferente de 0 não é entrega: corrija a linha que o script apontou e rode de novo.

## O gate

1. **Lint em código:** `python3 scripts/lint_copy.py <pasta de saída>/ganchos-<slug>.md`, exit 0. Ele reprova travessão longo, a família de verbo banida pela régua da casa e a antítese em espelho (negar uma coisa e afirmar a outra no mesmo fôlego). Reprovou: reescreva a partir da cena, sem remendar a frase.
2. **Régua de títulos:** a seção acima, antes da crítica. Título reprovado é falha bloqueante, no mesmo nível da falha dura do lint.
3. **Crítica de copy:** chame a **soft-critico-copy** com o gancho final, o CTA e os insumos (a pasta e o perfil do dono). Peça de conteúdo roda no modo padrão (veredito APROVADA ou REPROVADA). **Peça que vende roda no modo rigoroso** (nota de 0 a 10, só 10 aprova). Cole o veredito INTEIRO em `conferencia/veredito-copy-<slug>.md`, com as linhas que o gate exige: `títulos auditados: N · reprovados: N`, `encaixe narrativo:` (ou `não medido, sem arco informado`), `suspenso pela cascata:` quando a cascata parou a leitura, e, na reprovação, o fecho com a pergunta e o bordão. Veredito resumido, simulado ou montado de cabeça não conta.
4. **Onde o gate é mais duro, dito ao dono.** Na capa que vende, o modo rigoroso soma os checkpoints de mecanismo, voz e transformação, e o de mecanismo pede itens (nome próprio da oferta, processo exclusivo, metáfora do dono) que uma linha de até 15 palavras raramente comporta juntos (o caso 2 do exemplo parou em 9). Abaixo de 10, a skill não chama de aprovado: o relato abre com `Pronto: não, o gate deu <nota>/10`, entrega o veredito REFAZER com as versões e o que faltou, e o dono decide se publica assim ou leva o nome do método pro corpo. O gate não muda por causa disso.
5. **Sem a soft-critico-copy instalada,** rode o gate de bolso e diga ao dono que o gate completo não rodou: o lint, a régua de títulos com os scripts desta pasta, o teste do concorrente do gate e as 3 perguntas, cada uma com sim ou não escrito em `conferencia/`: dá pra visualizar? dá pra provar com o lastro dele? só ele diria isso?
6. **Até 3 rodadas, cada uma com o gate inteiro.** A versão corrigida pelo veredito passa por uma rodada nova; nunca cole o veredito da versão anterior. Na terceira reprovação seguida, pare e leve a decisão ao dono com as versões e os motivos.

## Gancho de referência validada

Quando o dono traz um post que já funcionou (dele ou do mercado):

1. **Peça o post e o número:** o print ou o texto da abertura, e o que ele rendeu (visualizações, salvamentos ou comentários). Sem número, trate como referência sem medição.
2. **Extraia a mecânica, nunca o texto:** em que família ele cai e qual molde do banco é o mais parecido; sem molde com a mesma mecânica, escreva o molde novo com lacunas. Do texto de terceiro só fica frase genérica que qualquer pessoa diria; nome, bordão e construção própria do autor saem.
3. **Registre o molde novo** no arquivo do dono `meus-moldes.md`, na pasta de trabalho dele (nunca dentro da pasta da skill), com código D001 em diante, família, alcance, formato, teto e o selo "sem medição (referência)", mais de onde veio a mecânica. Lacuna que nomeia o objeto, como no banco: nada de palavra-ponteiro solta. Depois, preencha e siga a régua e o gate normais.

## A entrega

A pasta `ganchos-<slug>/` tem só isto:

```
ganchos-<slug>/
  ganchos-<slug>.md          o gancho, que o dono abre
  conferencia/
    titulos.txt              um título por linha, copiado da peça
    checagem-titulos.md      a régua preenchida, com o fecho do script
    veredito-copy-<slug>.md  o veredito do gate, inteiro
    conferir.txt             a saída do --conferir
    fontes.txt               a saída do conferir_fontes.py
```

No arquivo do gancho, toda frase que o público lê aparece uma vez como título, e o resto vai numa ficha em tabela:

```
# <o gancho: a capa, ou a frase dita do reel; reel sem fala usa a frase da tela>

| FALAR | MOSTRAR | TEXTO NA TELA |
|---|---|---|
| <a frase dita> | <a cena> | <a frase escrita, ou (nada)> |

## <o CTA, quando o dono pediu>

| Ficha do gancho | |
|---|---|
| Formato | <reel falado, reel com texto na tela ou capa>, <N palavras, N caracteres>, teto <...>: passa |
| Molde | G___ · <família> · <alcance> |
| Selo | <medido ... ou sem medição>; a sua versão é variante sem medição própria |
| Fala do cliente | "<as palavras dele>" · <origem> · <autorização> |
| Prova na linha | <o número ou a credencial> |
| Outros moldes oferecidos | G___ e G___ |
| Próximo passo | <a skill do corpo da peça> |
```

A tabela de frentes só existe no reel com fala; reel sem fala leva a cena na ficha, numa linha MOSTRAR. Contagem, resultado do gate e comando moram em `conferencia/`, nunca no arquivo do gancho.

No chat, o relato abre com três linhas: `Pronto:` (o gancho final, ou `não` com o motivo), `Abra primeiro:` (o caminho do arquivo) e `Falta você responder:` (o número de perguntas e o assunto, ou "nada"). Depois vêm uma linha `<arquivo>: exit N` por arquivo linteado, a última linha do `--conferir`, a do `conferir_fontes.py` e uma linha oferecendo ajuste ("quer mais 3, outra família ou a versão pro outro formato?"). Por último, `Perguntas pra você`, uma pergunta por linha, terminada em "?", quando houver.

**O que vem depois do gancho:** o corpo da peça. Reel vai pra soft-conteudo-reels com o gancho já cravado; carrossel vai pra soft-conteudo-carrossel com a capa já cravada. A arte da capa é da soft-designer.

## Atalhos (sem processo rígido: o dono pode pular direto pra qualquer um destes)

| O dono diz | Você faz |
|---|---|
| "mais 3" | nova rodada, sem repetir moldes já mostrados |
| "outra família" | rodada só com a família pedida, ou com as duas que ainda não apareceram |
| "só medidos" | rodada só com selo medido, ordenada pela mediana |
| "só universais" ou "só de lista" | filtra pela parte ou pelo tipo |
| "o que é o G045?" ou "e o Q12?" | mostra a linha inteira do banco (ou o quadro e o molde pai) e explica a nota |
| "versão pro reel" ou "versão pra capa" | comprime ou estica o gancho pro outro teto, sem trocar o gatilho, e roda a régua de novo |
| "lote de 5 ganchos pra [tema]" | 5 moldes de famílias diferentes, cada um preenchido, gate em cada um |
| "CTA pro fim" | pergunta a palavra e a origem dela (ver "CTA do fim da peça") e mostra 3 opções de `shared-references/cta/cta-03-textos-base.md` pelo objetivo |
| "por que esse molde?" | uma linha ligando o molde à cena, à fala e ao objetivo |
| "modela este post" | caminho do gancho de referência validada |

## CTA do fim da peça

O tipo de CTA, o lugar dele e o banco por objetivo estão na referência única de CTA, `shared-references/cta/`: comece por `cta-01-tipos-e-lugar.md`. A palavra que o público comenta aparece no banco como `[PALAVRA]`, e **nenhum CTA entregue sai com `[PALAVRA]`.** Antes de escrever CTA de comentário ou de direct, faça ao dono as perguntas de `shared-references/cta/cta-02-palavra-do-comentario.md`, uma por vez (a palavra que a automação já responde, onde ela está, se está ligada, o que a pessoa recebe), e grave a resposta no perfil: o gate procura a palavra literal nos insumos. Sem palavra com origem, o CTA sai sem palavra ("Me chama no direct e eu te mando [o recurso]"), porque escolher uma palavra aqui é inventar. Isca prometida tem que existir, confirmada pelo dono. O CTA entra no `titulos.txt` e passa na régua como o gancho.

## Como ler o selo de prova

O selo mede a forma do molde, nunca o seu gancho: diga isso ao dono sempre que mostrar o número. Olhe a mediana (a força de 2024 está inflada por picos), lembre que o pico de comentário de carrossel mede o pedido junto com o gancho, e diga "sem medição" quando oferecer molde da casa. A legenda completa e as ressalvas estão em `references/banco-moldes.md`.

## O que esta skill não faz

| Pedido | Vai pra |
|---|---|
| criar a headline do zero a partir da tese, banco de headlines por gatilho, título de YouTube, assunto de e-mail | soft-conteudo-headlines |
| o roteiro do reel depois do gancho | soft-conteudo-reels |
| os slides do carrossel depois da capa | soft-conteudo-carrossel |
| montar o gancho no vídeo já gravado | soft-editor-video |
| o reel curto renderizado do zero | soft-reel-7seg |
| a abertura e a sequência de stories | soft-conteudo-stories |
| decidir sobre o que postar | soft-conteudo-planner |
| a arte da capa em PNG | soft-designer |
| auditar uma copy pronta | soft-critico-copy |
| levar a peça pronta pra outra plataforma | soft-conteudo-multiplataforma |

## Arquivos desta skill

- `references/banco-moldes.md`: o índice do banco (onde está cada molde, legenda, ressalvas dos números, quadros alternativos e contagem). Os moldes moram em `references/banco/`: Parte A, universais, um arquivo por família; Parte B, específicos, um por tipo de conteúdo.
- `references/literais/`: o banco literal, 346 frases de gancho universal (sem lacuna ou com lacuna ampla), em padrões, por família e por alcance. Índice em `references/literais/00-indice.md`; abra só o arquivo da família.
- `references/frameworks/`: os 21 cartões de framework, 15 de família e 6 de tipo de conteúdo (índice em "Do objetivo ao cartão").
- `references/visao-reel.md` e `references/visao-carrossel.md`: o gancho em cada formato, tetos, o que mais rendeu e a ordem de escolha.
- `references/ctas.md`: o que muda no CTA quando ele sai junto com o gancho.
- `shared-references/cta/`: a referência única de CTA (tipos e lugar, palavra do comentário, textos-base por objetivo), igual em todas as skills que escrevem CTA.
- `references/exemplo-fim-a-fim.md`: dois casos completos (um reel falado e uma capa de carrossel que vende), com o veredito real do gate. Leia antes da primeira rodada.
- `scripts/lint_copy.py` e `scripts/checar_titulos.py`: o lint de copy e o fecho da régua de títulos; o `--conferir` faz parte da definição de pronto.
- `scripts/conferir_fontes.py`: confere que todo número, nome e aspa do gancho tem fonte no insumo do dono (`--selftest` testa o script).

## Nome do arquivo e lint (vale em toda entrega)

O arquivo entregue se chama `ganchos-<slug>.md`, dentro da pasta `ganchos-<slug>/`, sem espaço e sem acento no nome. Antes de dizer pronto, rode `python3 scripts/lint_copy.py <arquivo>` em cada `.md` da pasta e cole uma linha por arquivo, `<arquivo>: exit N`. Exit diferente de 0 não é entrega.
