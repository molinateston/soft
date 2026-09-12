---
name: soft-atendimento-triagem
description: >-
  Olha a caixa de entrada cheia (leads, mensagens, formulários, DMs) e devolve a fila de quem atender primeiro hoje, com a nota de cada um, o motivo da posição e a primeira frase pronta pra cada contato. Também mostra quem sair da fila e por quê. Use quando o pedido for: "chegou um monte de lead, quem eu atendo primeiro", "tenho 40 mensagens não lidas", "quem vale a pena responder hoje", "prioriza minha caixa de entrada", "monta minha lista de contatos do dia", "esse lead vale ou não vale", "meu formulário encheu de gente", "quem tá quente aí". NÃO use pra: conduzir a conversa depois que ela começou, qualificar e agendar a reunião (soft-vendas-sdr); a conversa quente, a objeção e o fechamento (soft-vendas-closer); reclamação de cliente insatisfeito (soft-atendimento-reclamacao); a régua automática pós-isca (soft-funil-nutricao); decidir qual campanha rodar no mês (soft-vendas-estrategias). Leia e siga o fluxo inteiro do SKILL.md.
---

# Triagem: quem atende primeiro, e com que frase

Caixa cheia é o mesmo que caixa vazia: quando tudo parece igualmente urgente, o dono responde na ordem de chegada, gasta a manhã inteira com quem nunca ia comprar, e o lead que estava pronto esfria esperando. Esta skill lê o que chegou, dá nota a cada contato pelo mesmo critério, e devolve uma fila curta com a primeira frase de cada um.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Leitura em voz alta, por mensagem, com o resultado colado.** Toda mensagem que o lead recebe passa pela leitura em voz alta antes de sair. Cole `molde N | lida em voz alta: passa/tropeça | onde tropeça: <trecho>` pra cada mensagem da sequência, e feche com `lida em voz alta: sim · frase junta afirmação e pergunta: 0`. Frase que emenda uma afirmação e uma pergunta direta na mesma oração tropeça por construção, e a cura é quebrar em duas: `vi que você baixou o guia e o que mais te fez baixar logo esse foi o quê?` junta as duas e tropeça na leitura em voz alta. A abertura é a única linha do agente sem segunda chance: escreva primeiro e releia por último.

**A resposta devolve à pessoa o que ela mesma trouxe de bom.** Rode `grep -niE 'melhorou|funcionou|gostei|deu certo|obrigad' <insumo>` e cole a saída. Toda linha que voltar entra na mensagem, em uma frase, ANTES da parte que falhou. Cole `pontos positivos na reclamação: N · reconhecidos na mensagem: N`, iguais.

**A mensagem promete ato, nunca processo.** Rode `grep -niE 'apurar|apurando|verificar|analisar|definição|retorno|posicionamento|alinhar' <mensagem>` e cole a saída, inclusive vazia. Troque cada ocorrência por um ato com sujeito e hora (`eu volto a responder o grupo hoje à noite`), ou tire a frase: contar à pessoa o trabalho interno da casa não é resposta. Cole `palavras de processo na mensagem: 0`.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Cada linha da mensagem curta carrega algo que a anterior não carrega.** Antes de fechar, releia as linhas e corte a que só reformula a de cima; numa mensagem de três linhas, repetição é metade da peça.

**A lei-mãe: fila curta.** A entrega é a lista de quem atender HOJE, não a planilha de todo mundo. Lista de 40 nomes ordenados é a mesma paralisia com passos extras. O tamanho da fila cresce com o volume, mas nunca vira a base inteira.

**A segunda lei: nota é argumento, não sentença.** Todo lugar na fila vem com o porquê escrito em uma linha, no dado que gerou aquele lugar. Nota sem motivo o dono não usa, porque não consegue discordar dela.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as 4 ações num caso fictício: a lista crua que chegou, o desenho do critério, a fila pronta com nota e motivo, as primeiras frases, e o que foi tirado da fila.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a lista de contatos e eu monto a fila do dia). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra a fila com a lista que o dono já colou. Se faltar um insumo que a triagem não vive sem (os contatos, ou o critério do que vale pra ele), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista uma pergunta de cada vez (quem chegou, o critério do dono, o que faz um contato valer mais) antes de ordenar a fila.

A pergunta do modo é UMA por fila. As outras três partes entram nas ações abaixo:

- **Ensina enquanto faz:** ao desenhar o critério de prioridade, escreve UMA linha do porquê ("subo quem mostrou orçamento na frente de quem só curtiu; interesse dito vale mais que interesse suposto"), pra o dono decidir sozinho na próxima.
- **Puxa o material bruto:** quando o dono descrever o contato raso ("um pessoal interessado"), não segue no genérico. Pede o concreto: "o que cada um te falou, com as palavras dele, e o que você já sabe do bolso e da pressa de cada um?". O que a pessoa disse muda o lugar dela na fila.
- **Oferece refinar no fim:** depois de mostrar a fila, fecha com UMA linha de ajuste ("quer outro critério no topo? mais gente na fila? outra primeira frase? ajusto só o que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "quem eu atendo primeiro", "prioriza a caixa", "monta a lista do dia", "tenho 40 mensagens" | **1 · FILA DO DIA** (passa pela 2 se o critério ainda não existir) |
| "qual o critério", "como eu decido quem vale", "define meu cliente ideal pra triagem", "a fila veio errada" | **2 · CRITÉRIO** |
| "escreve o que eu mando pra cada um", "primeira mensagem", "abordagem desses aí" | **3 · PRIMEIRA FRASE** |
| "esse lead vale ou não vale", "vale a pena responder esse aqui", "posso descartar esses?" | **4 · UM CONTATO SÓ** |
| "organiza meu atendimento" (aberto) | **2, depois 1, depois 3, com parada em cada** |

Pedido ambíguo ("me ajuda com esses leads", "olha essa caixa aqui"): pergunte UMA coisa só, **"você quer a ordem de quem atender, ou o critério pra decidir isso sempre?"**, e siga pela resposta. Mostre a tabela acima como cardápio se não resolver.

## Como ler cada ação

Toda ação abaixo traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de cliente ideal, oferta, ticket ou voz: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" da ação e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

**Três regras que valem em toda ação:**
1. **Cliente atual sai da fila de aquisição.** Quem já comprou não é lead. Aparecer numa lista de "novos contatos pra abordar" é constrangedor e o dono paga o preço na frente do cliente.
2. **Nada é enviado por conta própria.** A skill escreve, o dono manda. Sem exceção, mesmo com a mensagem aprovada.
3. **Contato sem nada dentro não vira nota inventada.** Sem dado, o contato entra numa faixa própria, "não dá pra avaliar", com a pergunta única que resolveria isso.

---

## Ação 1 · FILA DO DIA (a lista de quem atender agora)

**O que faz:** lê o que chegou, dá nota a cada contato pelo critério da Ação 2, e devolve a fila curta com posição, nota, motivo e o que fazer com cada um.

**Precisa de:** a lista do que chegou, do jeito que o dono tiver (exportação da ferramenta, print, texto colado, lista de nomes com uma linha cada) · o critério da Ação 2 · o que aconteceu no último contato de cada um e quando.

**Sem o insumo:** sem a lista, peça numa pergunta só, e aceite o formato mais simples que ele tiver, inclusive texto colado. Sem o critério, rode a Ação 2 antes, que leva 5 perguntas. Sem data do último contato, trate todo mundo como não tocado e avise em 1 linha que a fila vai errar em quem já foi respondido ontem.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `fila-do-dia.md`, com a fila numerada (nome, de onde veio, nota, motivo em 1 linha, ação sugerida), a lista do que ficou de fora com o porquê, e os contatos que ficaram na faixa "não dá pra avaliar". **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/nota-e-criterios.md` (as 4 dimensões e como somar) · `references/armadilhas.md` (o que faz a fila mentir).

**Profundidade:** `references/o-que-perguntar.md` (as perguntas de intake, quando falta insumo).

**Os passos:**
1. **Antes de pontuar, cruze a caixa com o resto dos insumos.** A caixa de entrada raramente é o único lugar onde a pessoa aparece: uma call gravada, uma reclamação, um histórico de compra costumam estar na mesma pasta e mudam a nota. Pra cada nome da fila, rode `grep -rin '<nome>' <pasta de insumos>` e cole a saída. Contato que aparece em mais de um arquivo tem contexto que a caixa não mostra, e o caso mais caro é o lead que declarou um prazo de decisão numa call: rebaixar quem está mais perto de fechar por uma incerteza que estava a um comando de distância é o erro que esta regra existe pra matar. **É PROIBIDO descontar nota por dado ausente sem antes rodar essa busca:** `[A CONFIRMAR]` sobre um contato só vale depois do grep vazio, e o grep vazio vai colado ao lado do marcador. Checagem colada: `nomes na fila: N · buscados nos insumos: N · com contexto extra encontrado: N`.
2. **Separe o que não é lead antes de dar nota em qualquer coisa.** Cliente atual, fornecedor, currículo, propaganda, contato repetido. Isso sozinho encurta a fila e evita o erro mais caro.
3. Dê nota a cada contato pelas 4 dimensões (`nota-e-criterios.md`): interesse demonstrado, encaixe com quem o dono atende, urgência, e o desconto de quem já foi tocado hoje.
4. **Corte o tamanho da fila pelo volume:** até 10 contatos, mostre todos; de 11 a 30, os 5 primeiros; acima de 30, os 8 primeiros. O resto vai numa linha de resumo, não numa lista.
5. Escreva o motivo de cada posição em 1 linha, citando o dado (o que a pessoa fez, quando, e o que isso indica). Motivo genérico não vale.
6. Marque a faixa **"não dá pra avaliar"**: quem chegou sem dado nenhum. Cada um leva a pergunta única que resolveria.
7. **STOP.** Mostre a fila e pergunte "essa ordem faz sentido pra você? ajusto o critério, ou escrevo as mensagens?".

---

## Ação 2 · CRITÉRIO (o que faz um contato valer mais que outro)

**O que faz:** monta o critério de nota do dono, uma vez, pra que a fila de todo dia saia coerente em vez de depender do humor de quem olhou.

**Precisa de:** quem o dono atende bem de verdade (não quem ele gostaria de atender) · o que ele vende e por quanto · quais sinais a ferramenta dele registra de verdade · o que faz ele descartar um contato na hora.

**Sem o insumo:** entrevista curta de 5 perguntas, uma por vez:
1. Descreve o último cliente que deu muito certo. Quem era, que tamanho, que problema tinha?
2. E o último que deu errado. O que você teria visto antes, se tivesse olhado?
3. O que você vende pra essa pessoa, e por quanto?
4. Do que chega, o que você consegue saber sem perguntar (a pessoa respondeu, clicou, preencheu formulário, veio por indicação)?
5. O que faz você descartar um contato na hora, sem pensar?

A pergunta 2 é a que mais rende: o sinal de descarte que o dono já conhece na prática vale mais que qualquer modelo de nota. Sem resposta, use o critério de partida (`nota-e-criterios.md`, seção final) e marque `[A CONFIRMAR: critério de encaixe]`.

**Entrega:** `criterio-triagem.md`, com as 4 dimensões preenchidas pro negócio dele, os pesos, os sinais de descarte imediato, e a definição de quem sai da fila. Serve pra toda fila daí em diante. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/nota-e-criterios.md` (INTEIRO, antes de perguntar qualquer coisa).

**Profundidade:** `references/o-que-perguntar.md` · `references/armadilhas.md`.

---

## Ação 3 · PRIMEIRA FRASE (o que mandar pra cada um da fila)

**O que faz:** escreve a primeira mensagem de cada contato da fila, cada uma ancorada no que aquela pessoa fez, não num molde repetido com o nome trocado.

**Precisa de:** a fila da Ação 1 · o que cada contato fez ou disse, literal quando existir · a voz do dono, do perfil/brain do agente · o canal de cada um (é o canal por onde a pessoa chegou).

**Sem o insumo:** sem a fala literal, ancore no comportamento observável ("você baixou o material X na terça"). Sem a voz do dono no perfil, pergunte UMA coisa: "me manda uma mensagem sua de verdade que deu certo", e escreva no registro dela. Sem nenhuma das duas, escreva curto e direto, e diga em 1 linha que a voz precisa ser calibrada depois.

**Cobertura obrigatória da fila.** Toda conversa que entra na fila sai com a primeira mensagem escrita, sem exceção, e a lead mais quente é a primeira a ter mensagem, nunca a que fica de fora. Conversa sem mensagem só é aceita se estiver declarada fora da fila com o motivo escrito, e contato fora da fila não recebe nota nem posição na tabela: ou está fora, ou está na fila com mensagem. Checagem verificável antes de fechar: conte as linhas da fila e conte as mensagens escritas; os dois números batem, ou a entrega reprova. Depois confira a tabela: nenhuma linha declarada fora da fila carrega nota atribuída.

**O nome do destinatário é literal, e a anonimização não vale pra ele.** O crivo 08 protege TERCEIROS citados dentro de uma peça; a pessoa a quem a mensagem é endereçada usa o primeiro nome literal do insumo. Sem nome no insumo, a mensagem abre sem vocativo, nunca com inicial. Certo: `Fernanda, eu li o que você escreveu hoje de manhã.` Errado: `F., eu li o que você escreveu hoje de manhã.` Cole no `conferencia/checagem-titulos.md`, abaixo do bloco do script, a linha `mensagens escritas: N · com primeiro nome do destinatário no vocativo: N`, e diferença entre os dois números reprova (ver `references/08-consentimento.md`).

**O nome fica no arquivo que o dono USA, e a anonimização é só da peça pública.** A fila do dia, o dossiê da call, a lista de prospecção e o caso de reclamação são ferramenta de trabalho: o dono lê a linha e responde no aplicativo de mensagem chamando a pessoa pelo nome. Trocar por `contato 1`, `contato A` ou pela inicial obriga ele a abrir um segundo arquivo e cruzar número com nome numa manhã corrida, e é exatamente o que ele não faz. Então: nome literal na coluna, na linha e no cabeçalho do arquivo interno, sempre. A régua de consentimento continua valendo inteira na peça PÚBLICA (post, carta, landing, anúncio, stories, reel, e-mail em massa), que é onde o nome causa dano. O `checar_titulos.py` classifica o arquivo e imprime `uso interno: <arquivo>` pros que ficam de fora do gate de nome; se o arquivo interno desta rodada não aparecer nessa lista, dê a ele um nome que diga o que ele é (`fila-do-dia.md`, `dossie-call-<primeiro nome>.md`, `lista-de-prospeccao.md`).

**E o papel do nome muda por ARQUIVO.** A mesma pessoa é destinatária no arquivo de mensagens e terceiro em qualquer documento que fale SOBRE ela (fila, critério, triagem, relatório), e cada arquivo segue a regra do seu papel: nome literal em vocativo lá, `contato <N>` sem identificação aqui, com o número da posição amarrando os dois. Cole as duas linhas separadas, `nomes literais no arquivo de mensagens: N (todos em vocativo)` e `nomes literais nos documentos de trabalho: 0` (ver o bloco "O papel do nome muda por ARQUIVO" em `references/08-consentimento.md`).

**A última frase é convite, nunca menu.** Cada mensagem fecha pedindo UMA coisa que a pessoa responde em cinco segundos: um horário, um sim, uma escolha entre dois dias. Fechar oferecendo caminhos ("você prefere a call de diagnóstico, o material por escrito ou entrar na lista de espera?") é correto e frio, e devolve pra quem chegou o trabalho de escolher o próprio atendimento. A escolha entre caminhos é do dono, na fila da Ação 1. Cole `mensagens escritas: N · com última frase que se responde em 5 segundos: N`, e diferença entre os dois números volta pro passo de escrita.

**Entrega:** `primeiras-mensagens.md`, uma mensagem por contato da fila, com o canal marcado, prontas pro dono copiar. **Nada é enviado.** **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/primeira-mensagem.md` (a forma da mensagem e os 5 moldes por situação).

**Profundidade:** `references/armadilhas.md` (a seção de mensagem que denuncia automação).

**As regras da primeira frase:**
- **Mensagem que toca condição de saúde nomeada NUNCA responde sim.** Antes de escrever, marque toda conversa em que o contato cita diagnóstico, lesão, cirurgia, dor persistente, medicação, gravidez ou condição crônica. Nessas, a primeira mensagem faz três coisas e só três: reconhece a pergunta, diz que o caso precisa ser olhado antes de qualquer orientação, e faz uma pergunta que aprofunda. **É PROIBIDO afirmar que o método serve, funciona, é seguro ou "dá, sim, com ajuste" pra aquela condição**, mesmo com ressalva depois, mesmo quando é verdade, e mesmo quando a pessoa insiste: a afirmação vale como orientação clínica por escrito, sem avaliação, de quem não examinou. A acolhida sem afirmação é possível na mesma frase e não perde a lead. A mesma regra vale pra promessa de resultado financeiro e jurídico, com a ressalva do conselho que rege o nicho. Checagem colada: `mensagens com condição de saúde nomeada: N · com resposta afirmativa: 0`, e qualquer valor diferente de 0 reprova a Ação 3.
- **Uma pergunta só, e ela é fácil de responder.** Mensagem com três perguntas recebe zero.
- **Cita o que aquela pessoa fez**, com o quando. Mensagem que serviria pra qualquer contato da lista é reprovada e reescrita.
- **Não vende na primeira.** A primeira frase abre conversa; quem vende é a conversa.
- **Curta.** Se não cabe na tela do celular sem rolar, corte.
- **Contato frio há mais de 30 dias começa do zero.** Nada de "voltando ao nosso assunto" com alguém que não lembra de você.

---

## Ação 4 · UM CONTATO SÓ (vale ou não vale)

**O que faz:** avalia um contato específico que o dono colou e devolve a nota, o motivo e a recomendação: atende agora, atende depois, ou descarta.

**Precisa de:** o conteúdo do contato (a mensagem, o formulário, o print) · o critério da Ação 2, ou as 3 perguntas rápidas abaixo.

**Sem o insumo:** sem o critério pronto, pergunte três coisas de uma vez: o que você vende pra esse perfil, quanto custa, e o que te faria descartar na hora. Com essas três dá pra avaliar um contato só com honestidade.

**Entrega:** direto na resposta, em 5 linhas no máximo: nota, o dado que sustenta, a recomendação e a primeira frase se a recomendação for atender.

**Leia primeiro:** `references/nota-e-criterios.md`.

**Profundidade:** `references/armadilhas.md` (a armadilha do contato sem dado virando nota inventada) · `references/primeira-mensagem.md` (quando a recomendação for atender).

**A regra dura desta ação:** quando o dado não sustenta uma recomendação, a resposta é "não dá pra saber, pergunta isso a ele", com a pergunta escrita. Chutar aqui é pior que não responder, porque o dono age em cima do chute.

---

## Gate de qualidade (antes de mostrar a fila)

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Inventário do que o dono deu, com piso contado (vale em toda entrega desta skill).** Todo dado do perfil do dono que cabe na entrega aparece nela ou sai com o motivo da exclusão declarado, um dado por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`. **O piso é CONTADO, não estimado:** conte os dados do perfil um a um (com shell, `grep -c '^-' <perfil>`) e desdobre os campos de valor múltiplo. Cole a conta na entrega: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.**

O veredito é o PIOR item: um ✗ refaz aquele contato, não a fila inteira.

**Os 5 checks da triagem:**
1. **Cliente atual fora.** Ninguém que já comprou aparece na fila de aquisição. Este check reprova a entrega inteira, não só a linha.
2. **Motivo com dado.** Toda posição cita o que a pessoa fez e quando. Motivo que serviria pra qualquer contato é ✗.
3. **Fila curta.** O tamanho segue a régua do volume. Fila de 30 nomes é ✗.
4. **Sinal velho marcado como velho.** Contato cujos sinais têm mais de 30 dias entra com o aviso de que a nota vale pouco; entrar como quente é ✗.
5. **Furo visível.** Contato sem dado está na faixa "não dá pra avaliar", com a pergunta. Nota inventada pra preencher a coluna é ✗.

**Os 5 checks anti-IA (rodam em toda mensagem escrita na Ação 3):**
1. **Travessão longo:** zero. Busque o caractere e troque por ponto ou hífen comum.
2. **Verbo-freio banido:** zero ocorrências da família que a régua anti-voz proíbe (o verbo que rima com "cravar" e as flexões dele). Use emperrar, empacar, parar, freio, amarra.
3. **Antítese de espelho:** nada do molde que nega um polo curto pra afirmar o outro, em uma frase ou em duas, com ou sem a preposição "sobre", nem duas negações paralelas empilhadas. Afirme o que é, com sujeito e cena.
4. **Abertura de robô:** nada de "espero que esteja tudo bem", "passando pra saber", "vi que você demonstrou interesse". Comece pelo que a pessoa fez.
5. **Frase que serviria pra qualquer contato:** cortada. Se você pode trocar o nome e mandar pro próximo da fila, ela não diz nada.

**Com shell disponível, rodar `python3 scripts/lint_copy.py <arquivo>` sobre o arquivo de mensagens é obrigatório**, não opcional: é ele que decide os checks 1 a 3 acima e pega o que o olho perde. Sem shell, faça a busca manual pelos dois bloqueios duros (o travessão longo e o verbo-freio banido).

---

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Conduzir a conversa, qualificar e agendar depois que ela começou | **soft-vendas-sdr** | escrevo a primeira frase e paro; a condução do turno é dela |
| Conversa quente, objeção, pedir o sim, fechar | **soft-vendas-closer** | marco o contato como "vai pro 1:1" e não escrevo o script |
| Cliente insatisfeito, reclamação, pedido de reembolso | **soft-atendimento-reclamacao** | tiro esse contato da fila de aquisição e sinalizo que é atendimento |
| A régua automática de quem baixou a isca | **soft-funil-nutricao** | não faço; a triagem é do que chegou hoje, não da automação |
| Prospecção fria pra lista de contas que ainda não te procurou | **soft-vendas-outreach** | não faço; aqui só entra quem já deu algum sinal |
| Decidir qual campanha ou jogada rodar no mês | **soft-vendas-estrategias** | não faço |
| Cliente ideal, posicionamento, oferta | **soft-plano-posicionamento** | uso a entrevista curta de 5 perguntas da Ação 2 |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/nota-e-criterios.md` (as 4 dimensões da nota) · `references/armadilhas.md` (o que faz a fila mentir) · `references/o-que-perguntar.md` (as perguntas de intake) · `references/primeira-mensagem.md` (a forma da primeira frase) · `scripts/lint_copy.py` (o anti-IA em código, rode no shell quando o ambiente permitir).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do assunto, minúsculas, hífens, sem acento, até 6 palavras (ex.: `fila-do-dia-12-marco.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
