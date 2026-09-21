---
name: soft-atendimento-reclamacao
description: >-
  Resolve uma reclamação de cliente de ponta a ponta: lê o que aconteceu, levanta o histórico dessa pessoa, escreve a resposta no tom certo pra gravidade, decide o que oferecer, e diz o que mudar na operação pra não repetir. Também trata pedido de reembolso e cliente que ameaça expor publicamente. Use quando o pedido for: "esse cliente está bravo", "chegou uma reclamação", "me ajuda a responder isso aqui", "o cara quer o dinheiro de volta", "cliente ameaçou me expor", "como eu respondo sem piorar", "recebi uma avaliação ruim", "esse cliente reclama toda vez". NÃO use pra: priorizar quem atender primeiro na caixa cheia de leads (soft-atendimento-triagem); a conversa de venda e a objeção de quem ainda não comprou (soft-vendas-closer); contrato, cláusula e rescisão (soft-vendas-contratos); a régua de mensagem automática (soft-funil-nutricao); a copy de peça pública (soft-conteudo-*). Leia e siga o fluxo inteiro do SKILL.md.
---

# Reclamação: responder sem piorar, e consertar o que causou

Reclamação bem respondida devolve um cliente mais leal do que ele era antes de reclamar. Reclamação mal respondida vira avaliação pública, pedido de reembolso e a história que ele conta pros outros. A diferença quase nunca está no que foi oferecido; está em quanto tempo levou, em quem foi reconhecido antes de ser explicado, e em o dono ter respondido a mesma coisa a duas pessoas diferentes.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Leitura em voz alta, por mensagem, com o resultado colado.** Toda mensagem que o lead recebe passa pela leitura em voz alta antes de sair. Cole `molde N | lida em voz alta: passa/tropeça | onde tropeça: <trecho>` pra cada mensagem da sequência, e feche com `lida em voz alta: sim · frase junta afirmação e pergunta: 0`. Frase que emenda uma afirmação e uma pergunta direta na mesma oração tropeça por construção, e a cura é quebrar em duas: `vi que você baixou o guia e o que mais te fez baixar logo esse foi o quê?` junta as duas e tropeça na leitura em voz alta. A abertura é a única linha do agente sem segunda chance: escreva primeiro e releia por último.

**A resposta devolve à pessoa o que ela mesma trouxe de bom.** Rode `grep -niE 'melhorou|funcionou|gostei|deu certo|obrigad' <insumo>` e cole a saída. Toda linha que voltar entra na mensagem, em uma frase, ANTES da parte que falhou. Cole `pontos positivos na reclamação: N · reconhecidos na mensagem: N`, iguais.

**A mensagem promete ato, nunca processo.** Rode `grep -niE 'apurar|apurando|verificar|analisar|definição|retorno|posicionamento|alinhar' <mensagem>` e cole a saída, inclusive vazia. Troque cada ocorrência por um ato com sujeito e hora (`eu volto a responder o grupo hoje à noite`), ou tire a frase: contar à pessoa o trabalho interno da casa não é resposta. Cole `palavras de processo na mensagem: 0`.

**A promessa que consome recurso do dono sai da mensagem pronta, e o teste é por efeito, nunca por nome.** Liste tudo que a mensagem promete e marque cada item: `<promessa> | consome tempo, acesso ou dinheiro que não estava no combinado? sim/não`. Extensão de prazo, dias a mais de acesso, sessão extra e prioridade na fila respondem **sim** do mesmo jeito que mês grátis. Tudo que responde `sim` vira linha da tabela, marcada `quem aprova: o dono`. Cole a lista item a item e `promessas que consomem recurso na mensagem pronta: 0`. **A contagem sem a lista ao lado não conta como feita**, porque quem classifica sozinho classifica a favor do próprio texto.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Cada linha da mensagem curta carrega algo que a anterior não carrega.** Antes de fechar, releia as linhas e corte a que só reformula a de cima; numa mensagem de três linhas, repetição é metade da peça.

**A lei-mãe: reconhecer vem antes de explicar.** Explicação antes do reconhecimento é ouvida como desculpa, e desculpa esfria uma pessoa que já está quente. Primeiro o que aconteceu com ela, depois por que aconteceu, depois o que você vai fazer.

**A segunda lei: nada sai sem o dono.** A skill escreve a resposta, calcula o que oferecer, e para. Enviar, devolver dinheiro, dar crédito, fechar ou encerrar o caso é decisão de quem paga a conta.

**A terceira lei: uma reclamação é um caso, três são um problema.** Toda vez que este processo roda, ele pergunta se já aconteceu antes. Responder bem dez vezes o mesmo defeito é fazer dez vezes o trabalho que uma mudança na operação resolveria.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as 4 ações num caso fictício: a reclamação como chegou, o histórico levantado, a resposta escrita, a decisão do que oferecer e a correção de operação que saiu no fim.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a reclamação como ela chegou e eu escrevo a resposta). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra a resposta com a reclamação que o dono já colou. Se faltar um insumo que a resposta não vive sem (o texto da reclamação, ou a gravidade real do caso), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a Ação 1 uma pergunta de cada vez (o caso, o histórico da pessoa, o que já foi tentado) antes de escrever uma linha.

A pergunta do modo é UMA por caso. As outras três partes entram nas ações abaixo:

- **Ensina enquanto faz:** ao decidir o tom e o que oferecer, escreve UMA linha do porquê ("respondo firme e curto porque o cliente já está exaltado; texto longo aqui soa desculpa"), pra o dono calibrar sozinho na próxima.
- **Puxa o material bruto:** quando o dono resumir o caso raso ("cliente reclamou do atraso"), não segue no genérico. Pede o concreto: "cola a mensagem dele com as palavras que ele usou, e me diz se já tinha acontecido antes com essa pessoa". A fala literal e o histórico mudam a resposta inteira.
- **Oferece refinar no fim:** depois de mostrar o rascunho, fecha com UMA linha de ajuste ("quer mais firme? mais acolhedor? oferecer menos? refaço só a parte que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "chegou uma reclamação", "esse cliente está bravo", "me ajuda a responder isso" | **1, 2 e 3, na ordem** (é o caminho completo) |
| "quem é esse cliente", "vale a pena segurar esse?", "ele reclama toda vez?" | **1 · ENTENDER** |
| "escreve a resposta", "como eu respondo sem piorar" | **2 · RESPONDER** |
| "eu devolvo o dinheiro?", "quanto eu ofereço", "dou desconto ou dou crédito" | **3 · O QUE OFERECER** |
| "isso já aconteceu antes", "toda semana é a mesma coisa", "o que eu mudo pra não repetir" | **4 · CONSERTAR A CAUSA** |
| "ele ameaçou me expor", "vai me avaliar mal", "postou nas redes" | **2**, na trilha de exposição pública |

Pedido ambíguo ("olha essa mensagem aqui", "esse cliente"): leia a mensagem antes de perguntar qualquer coisa. Se ela é reclamação, entre na Ação 1 direto e faça a pergunta que a Ação 1 pede. Não devolva uma pergunta de roteamento pra quem já colou o problema.

**Pedido com duas metades sai num arquivo só.** Quando o dono escreve "me ajuda a responder **e** me diz o que consertar", ele pediu duas coisas e as duas são a entrega. O VEREDITO (o que aconteceu de verdade), a MUDANÇA (o que muda no processo) e o REGISTRO (onde isso fica anotado) saem no MESMO `caso-<nome>.md`, junto da resposta pronta, com um título de seção pra cada. O handoff guarda o inventário e o raciocínio descartado, nunca a metade que o dono pediu: uma peça de 728 bytes com a segunda metade dentro de um handoff de 13 mil é o gate moldando a entrega em vez de conferi-la. Cole `metades no pedido: N · entregues no arquivo da resposta: N`, e diferença entre os dois reprova.

## Como ler cada ação

Toda ação abaixo traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de voz, política de reembolso, prazo prometido ou o que a oferta inclui: leia do perfil/brain do agente quando existir; se não existir, faça a pergunta descrita no "Sem o insumo" da ação e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente política, prazo nem promessa.

**A regra que vale em toda ação: nunca invente fato.** Se você não sabe se o pedido foi enviado, a resposta não diz que foi. O furo entra no rascunho onde o dono o veja antes de clicar em enviar, como `[CONFIRMAR ANTES DE ENVIAR: o quê]`, e nunca numa nota no fim que ninguém lê. **Mas o lugar dele é a posição de campo, no fim da linha, nunca o miolo de uma frase que a pessoa lê:** quando a frase perde o sentido sem o dado, ela sai na versão que dispensa o dado, e a pergunta vai pro bloco "Antes de enviar".

---

## Ação 1 · ENTENDER (o caso e a pessoa, antes de escrever uma linha)

**O que faz:** lê a reclamação, separa o que aconteceu do que a pessoa está pedindo, e levanta quem ela é.

**Precisa de:** o texto da reclamação, do jeito que chegou (colado, print, encaminhado) · o histórico dessa pessoa: há quanto tempo é cliente, quanto já comprou, se já reclamou antes · o que de fato aconteceu, do lado do dono.

**Sem o insumo:** sem o texto, peça o print ou o texto colado e não escreva nada antes. Sem histórico registrado em lugar nenhum, pergunte três coisas de uma vez, que é o mínimo pra calibrar o tom: **há quanto tempo ela é cliente, quanto ela já comprou no total, e é a primeira vez que ela reclama?**. Sem o lado do dono sobre o que aconteceu, pergunte uma coisa só: **"do seu lado, o que aconteceu?"**, e não escreva a explicação antes da resposta.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** o bloco de situação, 5 linhas, no topo do `caso-<nome>.md`: quem é (tempo de casa, volume, quantas reclamações antes), o que aconteceu em uma frase, o que ela está pedindo, a gravidade, e o que falta saber.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/ler-a-reclamacao.md` (a separação entre o fato, o pedido e a emoção, e a régua de gravidade).

**Profundidade:** `references/casos-dificeis.md` (repetente, ameaça de exposição, cliente sem razão, tom agressivo).

**A separação que faz o resto funcionar:**
- **O fato:** o que aconteceu, verificável. ("O produto chegou dia 12 com a caixa amassada.")
- **O pedido:** o que ela quer. Muitas vezes não está escrito, e é diferente do que parece. ("Quero o dinheiro de volta" às vezes significa "quero que alguém me responda".)
- **A emoção:** o quanto ela está brava, e com quem. Isso decide o tom, não o conteúdo.

**A gravidade decide o prazo de resposta**, e é a única coisa desta skill com hora marcada: dano em andamento responde hoje; erro já consumado responde hoje ou amanhã; insatisfação difusa responde em até dois dias, mas responde.

---

## Ação 2 · RESPONDER (o rascunho, no tom da gravidade e do histórico)

**O que faz:** escreve a resposta ao cliente, calibrada por quem ele é e pelo tamanho do problema.

**Precisa de:** o bloco de situação da Ação 1 · a voz do dono, do perfil/brain do agente · o que pode ser oferecido, da Ação 3 quando houver oferta.

**Sem o insumo:** sem a voz do dono no perfil, pergunte UMA coisa: "me manda uma resposta sua de verdade, de um caso parecido", e escreva no registro dela. Sem nenhuma referência, escreva direto e humano, frases curtas, sem formalidade de departamento, e diga em 1 linha que a voz precisa de calibragem.

**Prazo que você não sabe não vira marcador dentro da mensagem.** O marcador só entra em posição de CAMPO: um link, um valor, um telefone, no fim da linha e substituível por colagem sem reescrever a frase. Uma data de reparação está no miolo por definição, porque é ela que separa o conserto do pedido de desculpas: apague o marcador, leia a frase, e se a promessa deixar de existir, ele estava no miolo. Sem a data no insumo, o rascunho sai em DUAS versões: (1) a que dispensa a data, pronta pro dono enviar hoje ("eu te mando a data da sua call ainda hoje, e ela não vai ser remarcada"), e (2) a com a data, com o campo no fim da linha. A pergunta do prazo vai pro bloco "Antes de enviar", nunca pra dentro do texto que a pessoa lê. Cole `marcadores no rascunho: N · em posição de campo: N · no miolo de frase: 0`, e valor maior que zero na terceira posição reprova a entrega.

**O nome do destinatário é literal, e a anonimização não vale pra ele.** O crivo 08 protege TERCEIROS citados dentro de uma peça; a pessoa a quem a mensagem é endereçada usa o primeiro nome literal do insumo. Sem nome no insumo, a mensagem abre sem vocativo, nunca com inicial. Certo: `Fernanda, eu li o que você escreveu hoje de manhã.` Errado: `F., eu li o que você escreveu hoje de manhã.` Cole no `conferencia/checagem-titulos.md`, abaixo do bloco do script, a linha `mensagens escritas: N · com primeiro nome do destinatário no vocativo: N`, e diferença entre os dois números reprova (ver `references/08-consentimento.md`).

**E o papel do nome muda por ARQUIVO.** A mesma pessoa é destinatária no arquivo de mensagens e terceiro em qualquer documento que fale SOBRE ela (fila, critério, triagem, relatório), e cada arquivo segue a regra do seu papel: nome literal em vocativo lá, `contato <N>` sem identificação aqui, com o número da posição amarrando os dois. Cole as duas linhas separadas, `nomes literais no arquivo de mensagens: N (todos em vocativo)` e `nomes literais nos documentos de trabalho: 0` (ver o bloco "O papel do nome muda por ARQUIVO" em `references/08-consentimento.md`).

**A última frase é convite, nunca menu.** Peça UMA coisa que a pessoa responde em cinco segundos: um horário, um sim, uma escolha entre dois dias. Fechar com a escolha entre caminhos administrativos ("você escolhe hoje: acompanhamento reposto ou cálculo da devolução proporcional") é correto e frio, e devolve pra quem reclamou o trabalho de decidir a própria reparação. A decisão entre degraus da escada é do dono, na tabela da Ação 3. Cole `última frase: <literal> · é pergunta que se responde em 5 segundos? sim/não`, e um `não` volta pro passo de escrita.

**Compensação que custa dinheiro nunca entra na mensagem pronta.** Crédito, mês grátis, desconto, brinde e devolução mudam o caixa do dono, e nenhum insumo os autorizou: escrever "mais um mês do programa sem cobrar" dentro do texto pronto pra copiar faz o dono enviar uma conta que ele não aprovou. A mensagem pronta oferece o que já foi comprado (o conserto, a reposição do que falhou, a data). A compensação fica na tabela da Ação 3, na coluna `quem aprova: o dono`. Cole `compensações na mensagem pronta: 0`, e valor maior que zero reprova a entrega.

**Entrega:** o rascunho no `caso-<nome>.md`, pronto pro dono copiar, em duas versões quando faltar data, com todo furo em posição de campo marcado `[CONFIRMAR ANTES DE ENVIAR: o quê]`. **Nada é enviado.** **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/tom-e-resposta.md` (as 4 partes da resposta e a tabela de tom por perfil).

**Profundidade:** `references/casos-dificeis.md` (as trilhas de exposição pública, repetente e cliente sem razão).

**As 4 partes, nesta ordem:**
1. **Reconhecimento.** O que aconteceu com ela, nas palavras dela, sem "mas". Uma ou duas frases.
2. **Explicação, quando você tem uma de verdade.** Curta, sem culpar terceiro nem processo interno. Sem explicação real, pule esta parte; inventar uma é pior que não ter.
3. **O que você vai fazer**, com prazo e nome de quem faz. É esta parte que resolve, e é a que costuma faltar.
4. **O próximo passo dela**, se houver algum, e sempre uma porta aberta.

**A tabela de tom:**

| Quem é | Tom |
|---|---|
| Primeira reclamação, cliente antigo ou de volume | Caloroso e generoso. Este é o caso em que vale gastar mais do que o problema custou |
| Primeira reclamação, cliente novo | Atencioso e claro. Ele está decidindo se fica |
| Reclama sempre | Profissional, firme, focado na solução. Cordial sem ser caloroso, e sem abrir precedente novo |
| Escreveu de forma agressiva ou ofensiva | Profissional, curto, com limite escrito. Nunca no mesmo registro dele |
| Está sem razão | Respeitoso e factual. Mostre o que aconteceu sem dizer que ele mentiu |

---

## Ação 3 · O QUE OFERECER (a decisão, antes de escrever a frase)

**O que faz:** decide o que é justo oferecer neste caso, e apresenta ao dono as opções com o custo de cada uma, pra ele escolher.

**Precisa de:** o valor envolvido · de quem foi o erro, honestamente · o histórico da pessoa, da Ação 1 · a política do dono, quando existir.

**Sem o insumo:** sem política declarada, monte a recomendação pela tabela abaixo e diga em 1 linha que ela vira a política dele se ele quiser, o que poupa essa decisão nas próximas vezes. Sem saber de quem foi o erro, pergunte UMA coisa: **"isso foi falha nossa, foi coisa de fora, ou foi mal-entendido?"**. A resposta muda tudo.

**Furo de valor não vira valor suposto, nem condicionado.** Quando o valor pago não está no insumo, a opção sai como PROPORÇÃO descrita ("metade do que ela pagou", "um mês de crédito"), nunca como conta sobre um preço presumido. Marcar `[A CONFIRMAR: valor]` e calcular na linha seguinte com um número plausível é o mesmo defeito com etiqueta: o dono lê a tabela pronta e envia. Rode `grep -inE 'r\$ ?[0-9]' <insumos do caso>` e cole a saída antes de montar a tabela; sem linha na saída, nenhuma célula da tabela carrega cifra. Cole no `conferencia/checagem-titulos.md` a linha `furos no caso: N · com valor assumido: 0`, e valor maior que zero na segunda posição reprova a entrega.

**Entrega:** as opções em tabela dentro do `caso-<nome>.md` (o que oferecer, quanto custa, o que resolve, o risco), com uma recomendação marcada. **A escolha é do dono. STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/o-que-oferecer.md` (a escada de reparação e quando cada degrau vale).

**Profundidade:** `references/casos-dificeis.md` (a trilha de pedido de reembolso, e a de cliente que reclama sempre) · `references/ler-a-reclamacao.md` (a tradução do pedido literal).

**A escada, do mais barato pro mais caro:**

| Degrau | Quando vale |
|---|---|
| Consertar e avisar | O padrão. Resolve o problema em si, que é o que a maioria quer |
| Consertar rápido, na frente da fila | Quando o atraso foi o problema |
| Consertar mais um brinde pequeno | Primeira reclamação de cliente bom, ou quando o erro foi claramente seu |
| Crédito pra próxima | Quando o erro foi seu e o cliente fica. Custa menos que dinheiro e mantém o vínculo |
| Devolver parte | Quando parte do serviço foi entregue e parte falhou |
| Devolver tudo | Quando nada do que foi prometido aconteceu, ou quando o cliente não fica de jeito nenhum |
| Devolver tudo e encerrar a relação | Cliente que reclama sempre e nunca fica satisfeito. É uma decisão de negócio, e é legítima |

**As duas regras da escada:**
1. **Não pule degraus pra cima antes da hora.** Oferecer o dinheiro de volta a quem só queria o conserto ensina o cliente a pedir dinheiro de volta.
2. **Não fique embaixo quando o erro foi grande.** Brinde pequeno num erro que custou o dia da pessoa é ofensa, e ela responde à altura.

---

## Ação 4 · CONSERTAR A CAUSA (pra não fazer isso de novo)

**O que faz:** olha se esta reclamação é caso isolado ou padrão, e propõe a mudança na operação quando é padrão.

**Precisa de:** as reclamações anteriores, de onde o dono guardar (ou da memória dele) · o que causou esta.

**Sem o insumo:** sem registro nenhum, pergunte UMA coisa: **"quantas vezes você ouviu isso nos últimos três meses?"**. A memória do dono serve, e o número aproximado dele já decide entre caso isolado e padrão. Aproveite pra propor o registro mínimo (a Entrega abaixo), que é o que torna a próxima resposta mais fácil.

**Entrega:** duas linhas no fim do `caso-<nome>.md`: o veredito (isolado ou padrão) e, quando é padrão, a mudança proposta com o custo dela. Mais a linha de registro, no formato: data, quem, o que aconteceu, o que foi oferecido, resolveu.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/registro-e-padrao.md` (o registro mínimo e como um padrão aparece).

**Profundidade:** a tabela de causas comuns e a mudança de cada uma, na mesma reference.

**A régua:** uma vez é caso. Duas vezes é coincidência com aviso. **Três vezes da mesma coisa em três meses é problema de operação**, e continuar respondendo caso a caso é escolher pagar o mesmo preço toda semana.

**Cada pessoa citada na Ação 4 sai com o vínculo colado.** Ao trazer outro contato como evidência de padrão, escreva `<nome> | <aluna, cliente, lead ou desconhecido> | <arquivo>:<linha> | fala literal: "<citação>"`. **O vínculo vem de fato no insumo, nunca de inferência:** quem perguntou se o método serve é lead; aluna ou cliente é quem o insumo declara como tal, ou quem tem compra confirmada. Contato classificado errado invalida o veredito de padrão, porque a conta de "quantos casos em quantos meses" passa a somar pessoas que não são o mesmo tipo de caso, e o dono passa a tratar um lead de topo como cliente com atendimento atrasado. Checagem colada: `pessoas citadas na Ação 4: N · com vínculo apontado por arquivo e linha: N`, e os dois números batem.

**Toda afirmação de gravidade sai com a linha do insumo que a sustenta.** "A falha continua acontecendo" é uma afirmação sobre o presente e precisa de um fato em curso, não de uma impressão: escreva `gravidade <alta, média ou baixa> porque <fato> · fonte: <arquivo>:<linha>`. Sem a linha apontada, a gravidade cai um degrau, porque a conclusão pode até estar certa e a prova está de um lado só.

---

## Gate de qualidade (antes de mostrar o rascunho)

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Inventário do que o dono deu, com piso contado (vale em toda entrega desta skill).** Todo dado do perfil do dono que cabe na entrega aparece nela ou sai com o motivo da exclusão declarado, um dado por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`. **O piso é CONTADO, não estimado:** conte os dados do perfil um a um (com shell, `grep -c '^-' <perfil>`) e desdobre os campos de valor múltiplo. Cole a conta na entrega: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.**

O veredito é o PIOR item: um ✗ refaz a resposta, não o caso inteiro.

**Os 5 checks da resposta:**
1. **Reconhecer significa dizer que estava errado, e repetir o fato não basta.** A primeira frase contém, obrigatoriamente, uma das duas: "você tem razão", ou uma frase que declare que aquilo não devia ter acontecido. **Enunciar o que aconteceu é descrição, e descrição sem assunção de falha soa a defesa:** "você ficou 10 dias sem resposta e teve a call remarcada duas vezes" conta o fato com precisão e não assume nada, e a cliente lê isso como preparação pra um "mas". Numa entrega quebrada, a diferença entre relatar o fato e assumir a falha é o que decide se a pessoa fica. Resposta que abre explicando é ✗. Checagem colada, com a frase copiada: `primeira frase: "<citação literal>" · declara falha: sim ou não`, e "não" reprova a Ação 2.
2. **Zero fato inventado.** Nenhuma afirmação sobre prazo, envio, causa ou processo que não foi confirmada. Todo furo está marcado `[CONFIRMAR ANTES DE ENVIAR]` dentro do texto, na frase onde importa.
3. **Tem ação com prazo.** A resposta diz o que vai ser feito e quando. Resposta que só lamenta é ✗.
4. **Sem "mas" desmanchando o reconhecimento.** "Sinto muito pelo transtorno, mas o prazo estava no site" reprova.
5. **Sem culpar terceiro.** Transportadora, sistema, equipe, fornecedor. Do lado de fora é tudo você. Explicação pode citar a causa; a responsabilidade não se transfere.

**Os 5 checks anti-IA:**
1. **Travessão longo:** zero. Busque o caractere e troque por ponto ou hífen comum.
2. **Verbo-freio banido:** zero ocorrências da família que a régua anti-voz proíbe (o verbo que rima com "cravar" e as flexões dele). Use emperrar, empacar, parar, freio, amarra.
3. **Linguagem de departamento:** cortada. "Prezado cliente", "lamentamos o ocorrido", "sua solicitação foi encaminhada ao setor responsável", "agradecemos o contato e a compreensão". Quem escreve é uma pessoa.
4. **Antítese de espelho:** nada do molde que nega um polo curto pra afirmar o outro, em uma frase ou em duas, com ou sem a preposição "sobre", nem duas negações paralelas empilhadas. Afirme o que é, com sujeito e cena.
5. **Frase que serviria pra qualquer reclamação:** cortada. Se a resposta serve pro caso do vizinho, ela não reconheceu nada.

**Com shell disponível, rodar `python3 scripts/lint_copy.py <arquivo>` sobre o arquivo do caso é obrigatório**, não opcional: é ele que decide os checks 1, 2 e 4 acima e pega o que o olho perde. Sem shell, faça a busca manual pelos dois bloqueios duros (o travessão longo e o verbo-freio banido).

---

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Priorizar a caixa cheia de leads novos | **soft-atendimento-triagem** | trato só o caso colado, sem fila |
| Objeção de quem ainda não comprou | **soft-vendas-closer** | não faço; reclamação é de quem já é cliente |
| Cláusula, rescisão, o que o contrato permite | **soft-vendas-contratos** | digo o que está em jogo, sem opinar sobre a cláusula |
| Régua automática de mensagem | **soft-funil-nutricao** | não faço; aqui é resposta individual |
| Post público, nota oficial, resposta em rede social | **soft-conteudo-multiplataforma** | escrevo a resposta pública curta, sem estratégia de conteúdo |
| Rever o que a oferta promete, pra parar de gerar reclamação na origem | **soft-plano-ofertas** | aponto a promessa que está gerando o problema, sem redesenhar a oferta |
| A política de reembolso escrita como documento | **soft-vendas-contratos** | monto a tabela de decisão da Ação 3, que serve como política de fato |

**Duas coisas que esta skill nunca faz, mesmo com pedido:** enviar a resposta, e executar a devolução de dinheiro. As duas são do dono, sempre, mesmo depois de ele aprovar o texto.

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/ler-a-reclamacao.md` (fato, pedido, emoção e gravidade) · `references/tom-e-resposta.md` (as 4 partes e a tabela de tom) · `references/o-que-oferecer.md` (a escada de reparação) · `references/casos-dificeis.md` (repetente, exposição pública, sem razão, agressivo) · `references/registro-e-padrao.md` (o registro mínimo) · `scripts/lint_copy.py` (o anti-IA em código, rode no shell quando o ambiente permitir) · `shared-references/filtro-anti-ia/` (a régua anti-IA escrita, pro motor que não roda o lint).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** `caso-` mais o primeiro nome do cliente e a data, minúsculas, hífens, sem acento (ex.: `caso-renata-12-marco.md`). **A data é a da mensagem recebida, lida no insumo, nunca a data da sessão.** Checagem verificável antes de fechar: aponte a linha do insumo de onde a data saiu; sem data no insumo, o nome sai `caso-<nome>-sem-data.md` e o doc declara isso na primeira linha. Data de hoje no nome de um caso de ontem é fato errado carregado no nome do arquivo, e reprova.
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Sem sandbox (a régua escrita, quando o lint não roda).** Motor sem shell não executa `scripts/lint_copy.py`, e isso não dispensa o anti-IA: aplique a régua no olho por `shared-references/filtro-anti-ia/padroes-banidos.md`, padrão por padrão, e passe cada reprovação por `shared-references/filtro-anti-ia/falsos-positivos.md` antes de mandar o trecho de volta pro passo de escrita, porque prosa autoral do dono cai no mesmo crivo e some se ninguém conferir. A entrega sai do mesmo jeito, no melhor que esse motor alcança, e o relato fecha com uma linha dizendo que a conferência anti-IA foi no olho, sem código: `anti-IA: conferido no olho pela régua escrita (sem shell nesta rodada)`. Calar o que ficou de fora reprova a entrega; declarar em uma linha reprova nada.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)

**Caso único também fecha com `conferencia/checagem-titulos.md`.** Um caso só não dispensa o arquivo: a resposta ao cliente é a peça, e a primeira linha dela é título pela função. Rode `python3 scripts/checar_titulos.py --peca caso-<nome>.md --titulos titulos.txt --teses teses.txt --insumos <pasta de insumos do caso> --perfil <perfil do dono> --nomes nomes.txt` com a resposta como peça, cole a saída inteira, e confira com `ls conferencia/checagem-titulos.md`. Pasta sem esse arquivo reprova antes da análise de conteúdo, mesmo com um caso na mesa.

- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
