---
name: soft-vendas-call-prep
description: >-
  Monta o DOSSIÊ DA CALL antes da conversa de venda: quem é o lead, quem está na sala e o papel de cada um, o histórico, o objetivo declarado, o roteiro por tipo de reunião, as perguntas de descoberta e as objeções prováveis com resposta pronta. Use quando o pedido for: "me prepara pra call com [nome]", "tenho reunião amanhã, me ajuda", "monta o dossiê desse lead", "o que eu pergunto nessa call", "quem é essa pessoa que vou atender", "que objeção esperar", "pesquisa essa empresa antes da call", "prep de call", "qual meu objetivo nessa conversa". NÃO use pra: conduzir a conversa, responder objeção ao vivo, pedir o sim (soft-vendas-closer); abrir conversa fria, qualificar e AGENDAR a call (soft-vendas-sdr); prospectar lista de contas por e-mail ou rede profissional (soft-vendas-outreach); a proposta depois da call (soft-vendas-proposta); contrato (soft-vendas-contratos). Leia e siga o fluxo inteiro do SKILL.md.
---

# O dossiê que entra na call com o dono

Esta skill entrega o documento que o dono lê nos 15 minutos antes da conversa: quem está do outro lado, o que já aconteceu entre vocês, o que ele quer sair dali levando, os temas na ordem, as perguntas que faltam responder e as objeções que vão aparecer, com a resposta já escrita. O resultado é sempre um arquivo nomeado, curto o suficiente pra ser lido de pé.

**A skill confere que é ela mesma, antes da primeira linha do fluxo.** As quatro skills de venda são vizinhas e se confundem: uma execução leu a pasta da vizinha, concluiu que esta skill não existia, rodou a outra, e entregou 2 arquivos onde o contrato pede 8, sem `conferencia/checagem-titulos.md`. A PRIMEIRA linha do fluxo é `head -3 SKILL.md` da pasta indicada, e você cola `SKILL.md lido: <caminho literal> · nome no frontmatter: <nome>`. **Nome diferente do que o dono pediu PARA tudo** e reporta que a skill pedida não está no catálogo desta sessão, em vez de rodar a vizinha: contratos de saída diferentes produzem entrega incompleta que parece completa.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**A lei-mãe:** preparação não é acumular informação, é decidir antes o que a conversa precisa produzir. Todo item do dossiê existe porque serve a um objetivo declarado; o que não serve fica de fora, porque dossiê que não cabe numa tela não é lido.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as 4 ações num caso fictício de nicho neutro: o dossiê inteiro no formato real de entrega, o roteiro por tipo de reunião, as perguntas de descoberta e a tabela de objeções. Ler antes da primeira pergunta economiza uma rodada de retrabalho.

**Sobre pesquisa:** notícia recente, mudança de comando, tamanho e histórico da conta vêm de conector de CRM, agenda, e-mail ou transcrição quando o ambiente tiver algum conectado; se não tiver, busque na web quando o ambiente permitir; se nem isso, peça ao dono o que ele tem e trabalhe com isso. **Nada entra no dossiê sem fonte.** O que não foi confirmado vira `[A CONFIRMAR: o quê]` e a call segue: melhor uma pergunta a mais na conversa que uma afirmação errada na frente do cliente.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola quem é o lead e o histórico e eu monto o dossiê). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pro dossiê com o que o dono colou. Se faltar um insumo que o dossiê não vive sem (quem está na sala, o objetivo da conversa), pergunta AQUELE insumo e segue, sem repetir a entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Pergunta quem é o lead, o que já rolou entre vocês e o objetivo da call, uma coisa de cada vez, e monta o dossiê com o que o dono for dando.

A pergunta do modo é UMA por dossiê. As outras três partes acontecem nos passos abaixo:

- **Ensina enquanto faz:** em cada escolha estrutural (o objetivo da call, a ordem dos temas, a objeção priorizada) escreve UMA linha do porquê. O dono lê a razão e aprende a preparar a próxima sozinho.
- **Puxa o material bruto:** quando a resposta vier rasa ("é um lead interessado", "quer saber do serviço"), não segue com o genérico. Pede o concreto que só o dono tem: a última frase que o lead escreveu, onde a conversa anterior emperrou, o número que a empresa dele move. Contexto real vira dossiê afiado; resposta rasa vira roteiro genérico.
- **Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer mais objeções cobertas? outro objetivo pra call? as perguntas mais duras? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "me prepara pra call com [nome]", "tenho reunião amanhã", "monta o dossiê", "prep de call" | **as 4 na ordem, e o dossiê sai inteiro** |
| "quem é essa pessoa", "pesquisa essa empresa", "o que aconteceu com esse lead até agora" | **1 · O RETRATO** |
| "qual meu objetivo nessa call", "que temas eu levo", "como eu conduzo essa reunião" | **2 · OBJETIVO E ROTEIRO** |
| "o que eu pergunto", "que informação me falta desse lead" | **3 · AS PERGUNTAS** |
| "que objeção esperar", "ele vai falar que tá caro, o que respondo" | **4 · AS OBJEÇÕES** |

Pedido ambíguo ("tenho uma call, me ajuda"): pergunte UMA coisa só, **"que tipo de reunião é essa, e o que você quer que aconteça no fim dela?"**, mostre a tabela acima como cardápio e siga pela resposta. Tipo de reunião e objetivo são os dois insumos que mudam tudo.

## Como ler cada ação

Toda ação abaixo traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de oferta, preço, prova, casos e diferenciais: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`.

**Duas regras que valem em toda ação:** nada entra sem fonte (dado inventado na frente do cliente custa a venda inteira) · e o dossiê cabe em uma tela e meia: o que não serve ao objetivo declarado sai.

---

## Ação 1 · O RETRATO (quem é, o que já aconteceu, o que mudou)

**O que faz:** monta o retrato do lead e das pessoas que estarão na sala, com o histórico de contato e o que mudou por lá recentemente.

**Precisa de:** o **nome do lead ou da empresa** e o **tipo de reunião**, sempre perguntados ao dono · **quem participa**, nome e cargo · o **histórico**: o que já foi conversado, o que ficou combinado, o que ficou pendente (do conector de CRM, agenda, e-mail ou transcrição quando houver; do dono quando não houver) · o que mudou por lá (notícia, contratação, mudança de comando), da web quando o ambiente permitir.

**Sem o insumo:** entrevista curta de 4 perguntas, uma por vez: com quem você vai falar, nome e cargo · que tipo de reunião é · o que já rolou entre vocês até aqui, mesmo que resumido · tem alguma coisa que você já sabe que vai ser tema. Sem nome dos participantes, monte o retrato só da empresa e escreva no dossiê a primeira pergunta da call: **"quem mais participa da decisão além de você?"**. Sem acesso a pesquisa nenhuma, o retrato sai só com o que o dono contou, marcado `[A CONFIRMAR: sem pesquisa externa]`, e isso é honesto e suficiente.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**A fala primeiro, o retrato depois (esta é a primeira coisa que a Ação 1 faz, antes de escrever uma linha).** O que o dono supõe sobre o lead nunca substitui o que o lead escreveu, e a diferença entre os dois é exatamente o que a call de descoberta existe pra investigar. Antes de montar o retrato, procure a fala do lead nos insumos: com shell, `grep -rin '<primeiro nome do lead>' <pasta de insumos>`, e **cole a saída no dossiê, inclusive quando ela vier vazia**, porque a busca vazia também é informação (o lead não deixou fala registrada). Uma mensagem de duas linhas na caixa de entrada costuma carregar de onde a pessoa veio ("vi o carrossel") e a objeção literal a responder na abertura ("isso serve pra mim?"), e nenhuma das duas coisas está no enunciado do pedido. **Toda linha do retrato sai etiquetada com a origem:** `[fala dele: <arquivo>:<linha>]` quando veio da boca do lead, `[hipótese do dono]` quando veio do enunciado do pedido, `[pesquisa: <comando ou fonte>]` quando veio de busca. **Dossiê em que nenhuma linha carrega `[fala dele]` e existe insumo de conversa na pasta reprova a Ação 1.** A abertura sugerida devolve a pergunta que a pessoa fez, com as palavras dela, e não abre com o roteiro genérico da skill. Checagem colada: `linhas do retrato: N · com [fala dele]: N · com [hipótese do dono]: N · busca da fala do lead: <comando> · saída: <colada ou "vazia">`.

**Entrega:** a seção de retrato do arquivo `dossie-call.md`: o quadro da conta, um bloco por participante, e o histórico em três linhas. **STOP quando for a única ação pedida.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/dossie-formato.md` (a estrutura do arquivo, campo por campo).

**Profundidade:** `references/gate-do-dossie.md`.

**Os passos:**
1. Preencha o **quadro da conta**: nome · o que a empresa ou a pessoa faz · tamanho · situação (nunca falamos antes, negociação aberta, já é cliente) · último contato, com data.
2. Um **bloco por participante**: cargo · trajetória, quando encontrada · papel na decisão (decide, defende por dentro, avalia, atrapalha) · última interação com o dono · **um ponto de conversa** real, nunca elogio genérico.
3. **O histórico em três linhas:** o que já foi conversado · o que ficou combinado e por quem · o que ficou em aberto ou virou preocupação.
4. **O que mudou por lá**, no máximo três itens, e cada um com a frase que explica por que aquilo importa pra esta conversa. Notícia sem consequência não entra.
5. Marque `[A CONFIRMAR]` em tudo que não tem fonte, e mande esses itens pro bloco de perguntas da Ação 3.

**Papel na decisão, o mapa curto:** quem assina · quem defende a compra por dentro · quem avalia tecnicamente · quem paga a conta · quem perde alguma coisa se a compra acontecer (o último é o que mais derruba negociação e o que menos aparece na sala).

---

## Ação 2 · OBJETIVO E ROTEIRO (o que a call precisa produzir)

**O que faz:** crava o objetivo da conversa em uma frase e monta a sequência de temas do tipo de reunião que ela é.

**Precisa de:** o **tipo de reunião** · o que o dono quer **sair levando**, em uma frase · o **tempo** da call · quem manda na agenda (o dono ou o cliente).

**Sem o insumo:** se o dono não consegue dizer o objetivo em uma frase, ofereça o padrão do tipo de reunião (a tabela abaixo) e peça pra ele confirmar ou corrigir. Sem tempo declarado, assuma 30 minutos e monte o roteiro nesse formato, avisando em 1 linha. Objetivo confuso é a causa número um de call que termina em "me manda um material".

**Entrega:** a seção de objetivo e roteiro do `dossie-call.md`: a frase do objetivo, o roteiro numerado com minutagem, e o próximo passo que o dono vai propor. **STOP quando for a única ação pedida.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/tipos-de-reuniao.md` (o foco, o roteiro e o resultado esperado de cada tipo).

**Profundidade:** `references/dossie-formato.md` · `references/gate-do-dossie.md`.

**A tabela dos 5 tipos** (o detalhe de cada um está na reference):

| Tipo | Foco | O roteiro pende pra | O que a call precisa produzir |
|---|---|---|---|
| Descoberta | entender o mundo da pessoa, a dor e a prioridade | perguntar mais que falar | sinal de qualificação e o próximo passo marcado na hora |
| Demonstração | o caso específico dela, com o exemplo dela na tela | mostrar o que ela pediu, não o catálogo | requisito técnico e prazo de decisão |
| Proposta e negociação | preocupação respondida e valor sustentado | responder objeção e fechar espaço | caminho pro acordo, com data |
| Acompanhamento de cliente | o que já foi entregue e o que abriu de novo | revisar resultado e escutar | confiança na renovação e a próxima necessidade |
| Reencontro depois do sumiço | o que mudou dos dois lados | escutar antes de propor | a conversa reaberta ou o encerramento honesto |

**Os passos:**
1. Escreva o **objetivo em uma frase**, com verbo e resultado observável. Ruim: "avançar a negociação". Bom: "sair com a data da apresentação pro comitê marcada".
2. Monte o **roteiro numerado com minutagem**, sempre nesta forma: abertura que retoma a conversa anterior · dois ou três blocos de tema · fechamento com o próximo passo proposto pelo dono.
3. A abertura **nunca** é apresentação pessoal quando já houve contato: ela retoma o que ficou em aberto, e isso sozinho muda o tom da conversa inteira.
4. O último bloco é sempre o próximo passo **com data e responsável**. Call sem próximo passo marcado dentro dela é call que vira e-mail sem resposta.

---

## Ação 3 · AS PERGUNTAS (o que ainda falta saber)

**O que faz:** escreve as perguntas de descoberta que fecham os buracos do retrato, na ordem em que elas cabem na conversa.

**Precisa de:** o retrato da Ação 1 (é dos `[A CONFIRMAR]` dele que metade das perguntas nasce) · o objetivo da Ação 2 · o que o dono precisa saber pra decidir se vale seguir com esse lead.

**Sem o insumo:** sem retrato nenhum, use as 5 perguntas que servem a qualquer conversa de venda (as cinco famílias abaixo) e adapte pelo tipo de reunião. Elas cobrem o essencial mesmo quando não se sabe nada do lead.

**Entrega:** a seção de perguntas do `dossie-call.md`, de 5 a 8 perguntas numeradas, cada uma com a razão de estar ali em meia linha. **STOP quando for a única ação pedida.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/perguntas-de-descoberta.md` (as 5 famílias, com exemplos e os erros que matam a resposta).

**Profundidade:** `references/tipos-de-reuniao.md` · `references/gate-do-dossie.md`.

**As 5 famílias de pergunta:**
1. **Situação:** como funciona hoje, o que já foi tentado, o que está em uso.
2. **Dor e prioridade:** o que incomoda, quanto custa esse incômodo, e por que isso virou assunto agora.
3. **Decisão:** quem mais participa, como decisões desse tipo costumam ser tomadas ali, que prazo existe.
4. **Sucesso:** o que precisa acontecer em três meses pra essa pessoa considerar que valeu.
5. **Concorrência e alternativa:** o que mais está sendo avaliado, incluindo a alternativa de não fazer nada.

**As regras que salvam a resposta:** uma pergunta por vez, sem emendar duas · pergunta aberta na primeira rodada e fechada só pra confirmar · silêncio depois de perguntar (a segunda parte da resposta é sempre a boa) · nunca comece pelo orçamento (isso vem depois da dor, ou o número sai defensivo).

---

## Ação 4 · AS OBJEÇÕES (o que vai vir, e o que responder)

**O que faz:** antecipa as objeções prováveis daquele lead naquele tipo de reunião, e escreve a resposta de cada uma, ancorada em prova real.

**Precisa de:** o retrato e o tipo de reunião · a **objeção que o dono já ouviu desse lead**, quando houver · as **provas reais** que ele pode citar (caso, número, garantia), do perfil/brain do agente · o preço e o que está incluso.

**Sem o insumo:** sem objeção conhecida, use as quatro que aparecem em quase toda conversa (preço, momento, confiança, autoridade) e escreva a resposta de cada uma. Sem prova real disponível, a resposta se apoia em mecanismo e garantia, e o dossiê marca `[A CONFIRMAR: prova]`, porque prova inventada na frente do cliente é o pior erro possível.

**Entrega:** a seção de objeções do `dossie-call.md`, em tabela: objeção · o que ela quer dizer de verdade · a resposta · a prova que sustenta. **STOP quando for a única ação pedida.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/objecoes-antecipadas.md` (as 4 famílias, o que cada uma esconde e o molde de resposta).

**Profundidade:** `references/gate-do-dossie.md`.

**As 4 famílias e o que cada uma costuma esconder:**

| A pessoa diz | Costuma querer dizer | A resposta começa por |
|---|---|---|
| "está caro" | não vi o retorno, ou comparei com uma coisa mais barata que faz outra coisa | devolver a conta, com o número dela |
| "agora não é o momento" | isso não é prioridade contra outras três coisas | achar o custo de esperar, em número |
| "preciso pensar" | falta uma informação, ou falta uma pessoa | perguntar qual das duas, sem constrangimento |
| "preciso falar com fulano" | não é a pessoa que decide, ou não quer defender sozinho | ajudar a defender por dentro, com material pronto |

**A regra de ouro da resposta:** responde-se à objeção real, não à frase. Por isso a coluna do meio da tabela existe: sem ela, o dono responde a frase, e a frase quase nunca é o problema.

---

## O gate do dossiê (roda por dentro, e não imprime)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Fontes consultadas (esta skill pesquisa, então a seção é obrigatória).** A seção "Fontes consultadas" da entrega lista só o que foi de fato aberto neste turno, e cada linha traz o comando ou a chamada de ferramenta que abriu aquela fonte. Sem acesso à web no ambiente, a seção diz exatamente "sem acesso à web neste ambiente" e nada mais: nenhum domínio, nenhum nome de marca, nenhuma data de busca. Checagem verificável antes de fechar: conte as linhas da seção e conte os comandos registrados no relatório e escreva os dois números lado a lado, nesta forma: `fontes declaradas: N · comandos no log: N`. **Declarar 4 buscas com 1 comando no log reprova**, e o conserto é apagar as 3 linhas sem comando, nunca inventar o comando. **Cada linha de tabela sobre terceiro traz a consulta que a produziu e o trecho citado da página aberta.** Número (preço, prazo, prazo de entrega, volume, quantidade de alunos, faturamento) vindo de página de terceiro só entra com o trecho colado ao lado; sem trecho colado, o campo sai como `[A CONFIRMAR: exige abrir a página]`, e cravar o número mesmo assim reprova a entrega inteira. Memória de treino e inferência plausível não são fonte.


**O que faz:** reprova o dossiê que não serve na hora da call. O veredito é o pior item, e uma reprovação refaz aquela seção.

**Leia primeiro:** `references/gate-do-dossie.md`.

Os 5 checks anti-IA, inline:
1. **Travessão longo:** zero ocorrência de U+2014 e U+2013 no arquivo inteiro, notas incluídas.
2. **Verbo-freio banido:** a família que a régua anti-voz proíbe (o verbo que rima com "cravar" e todas as flexões) não aparece. Use emperrar, empacar, parar, freio, amarra.
3. **Antítese de espelho:** nada do molde que nega um polo curto pra afirmar o outro, em uma frase ou em duas, com ou sem a preposição "sobre", nem duas negações paralelas empilhadas.
4. **Verbo de transformação genérico:** a família de verbos grandiosos de folheto. Troque por concreto: resolve, tira, muda, corta.
5. **Abertura e fecho de robô:** a saudação de praxe, o convite a imaginar, a pergunta retórica de introdução, a moldura que anuncia um segredo, o fecho que agradece a leitura.

Mais os checks próprios do formato, binários: **objetivo em uma frase** com resultado observável · **tudo com fonte**, e o que não tem vira `[A CONFIRMAR]` · **ponto de conversa real** (elogio genérico ao cargo ou à empresa reprova) · **próximo passo com data** no roteiro · **prova declarada** em cada resposta de objeção · **cabe numa tela e meia** (dossiê longo demais não é lido antes da call, e dossiê não lido não existe).

**Com shell disponível, rodar `python3 scripts/lint_copy.py <arquivo>` sobre a entrega é obrigatório, não opcional.** Sem shell, faça a busca manual pelos dois bloqueios duros do check 1 e do check 2.

---

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Conduzir a conversa, responder objeção ao vivo, pedir o sim, coletar o sinal | **soft-vendas-closer** | deixo a resposta escrita no dossiê, sem a condução da conversa |
| Abrir conversa fria, qualificar e AGENDAR essa call | **soft-vendas-sdr** | não faço. Esta skill começa depois que a call já existe na agenda |
| Prospectar uma lista de contas por e-mail ou rede profissional | **soft-vendas-outreach** | não faço |
| A proposta comercial em site depois da call | **soft-vendas-proposta** | listo o que a proposta precisa cobrir, sem montá-la |
| Contrato | **soft-vendas-contratos** | não faço |
| Resumo e tarefas depois da call | **soft-vendas-closer** | deixo no dossiê o campo de anotação do que precisa ser capturado |
| Posicionamento, oferta, preço, prova | **soft-plano-posicionamento** | uso a entrevista curta de 4 perguntas da Ação 1 |
| Campanha de e-mail de acompanhamento | **soft-email-sequencia** | escrevo só a mensagem única de retomada |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/dossie-formato.md` · `references/tipos-de-reuniao.md` · `references/perguntas-de-descoberta.md` · `references/objecoes-antecipadas.md` · `references/gate-do-dossie.md` · `scripts/lint_copy.py` (o anti-IA em código, rode no shell quando o ambiente permitir).

---

## A régua de títulos sobre o que o lead OUVE

O dossiê é documento interno e por isso marcador e nome real cabem nele sem falta. **Mas nem toda linha do dossiê é interna:** a abertura sugerida, a frase de transição e a pergunta de fechamento são falas que o lead ouve na call, e fala que o lead ouve é título pela função, mesmo sem parecer um. Passe cada uma dessas linhas pela régua de títulos (`references/08-consentimento.md` cuida do nome; a régua de títulos cuida do gancho falado) e cole a tabela em `conferencia/checagem-titulos.md`, arquivo de nome fixo na raiz da pasta de saída, com uma cópia no fim do dossiê para quem lê só o dossiê na hora da call. **A pasta sem `conferencia/checagem-titulos.md` reprova a Ação antes da análise de conteúdo.** A tabela sai na forma `<linha que o lead ouve> | gatilho nomeado: <qual das 6 famílias> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. **Nenhuma dessas linhas sai com marcador no miolo**, porque o dono vai falar a frase e não dá pra falar um colchete: dia, hora e número vivem numa linha `DADOS:` acima da fala, ou a frase se escreve na versão que dispensa o valor. Checagem colada: `falas que o lead ouve: N · passadas pela régua: N · com marcador no miolo: 0`, mais as contagens de fecho do crivo de títulos no mesmo arquivo. **O nome do lead é literal na fala, e a anonimização não vale pra ele.** O crivo 08 protege TERCEIROS citados dentro do dossiê; a pessoa com quem o dono vai falar é chamada pelo primeiro nome literal do insumo, na abertura e nas transições. Sem nome no insumo, a abertura sai sem vocativo, nunca com inicial. Certo: `Fernanda, obrigado pelo tempo de hoje.` Errado: `F., obrigado pelo tempo de hoje.` Cole no `conferencia/checagem-titulos.md`, abaixo do bloco do script, a linha `mensagens escritas: N · com primeiro nome do destinatário no vocativo: N`, contando cada fala endereçada ao lead, e diferença entre os dois números reprova (ver `references/08-consentimento.md`).

**O nome fica no arquivo que o dono USA, e a anonimização é só da peça pública.** A fila do dia, o dossiê da call, a lista de prospecção e o caso de reclamação são ferramenta de trabalho: o dono lê a linha e responde no aplicativo de mensagem chamando a pessoa pelo nome. Trocar por `contato 1`, `contato A` ou pela inicial obriga ele a abrir um segundo arquivo e cruzar número com nome numa manhã corrida, e é exatamente o que ele não faz. Então: nome literal na coluna, na linha e no cabeçalho do arquivo interno, sempre. A régua de consentimento continua valendo inteira na peça PÚBLICA (post, carta, landing, anúncio, stories, reel, e-mail em massa), que é onde o nome causa dano. O `checar_titulos.py` classifica o arquivo e imprime `uso interno: <arquivo>` pros que ficam de fora do gate de nome; se o arquivo interno desta rodada não aparecer nessa lista, dê a ele um nome que diga o que ele é (`fila-do-dia.md`, `dossie-call-<primeiro nome>.md`, `lista-de-prospeccao.md`).

**E o papel do nome muda por ARQUIVO.** A mesma pessoa é destinatária no arquivo de mensagens e terceiro em qualquer documento que fale SOBRE ela (fila, critério, triagem, relatório), e cada arquivo segue a regra do seu papel: nome literal em vocativo lá, `contato <N>` sem identificação aqui, com o número da posição amarrando os dois. Cole as duas linhas separadas, `nomes literais no arquivo de mensagens: N (todos em vocativo)` e `nomes literais nos documentos de trabalho: 0` (ver o bloco "O papel do nome muda por ARQUIVO" em `references/08-consentimento.md`).

**Molde endereçado a pessoa nomeada exige o insumo dela aberto:** rode `grep -n '<Nome>' <insumo>` e cole a saída antes da fala, na forma do bloco "Fala atribuída ao destinatário" de `references/08-consentimento.md`. Fala atribuída sem trecho literal do insumo reprova.

**As falas que entram na conta são todas as que o dono vai pronunciar:** abertura, transições, apresentação de preço, pergunta de fechamento e a resposta a cada objeção prevista, não só a abertura.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `dossie-call-transportadora-norte.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com a lista fechada de contagens, uma por linha, exatamente nesta forma:

```
títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N
em molde de antítese (títulos): N (teto 1)
em molde de antítese (fala ou narração que o público ouve): N (teto 1)
com inimigo ou inversão: N de N
teses distintas: N
títulos de serviço: N · de abertura: N · de abertura reescritos: N
rótulos de seção fora da régua: N
gatilhos fora da lista fechada: 0
```

A contagem de molde de antítese sai do lint, nunca da cabeça, e vem acompanhada da coluna sim/não de TODOS os títulos do lote; a de teses distintas vem com a lista ordenada e comparada par a par. Nenhuma das linhas pode faltar, e linha declarada sem o que a régua exige ao lado não conta como feita.

**As contagens de R3, R4 e R5 são gates, não termômetros.** Quando `com inimigo ou inversão` ficar abaixo da metade do lote, `teses distintas` abaixo de 3, ou `em molde de antítese` acima de 1, a entrega **não sai**: os títulos reprovados voltam pro passo de escrita, são reescritos, e a checagem final mostra a contagem corrigida mais a linha `reescritos por contagem: N (<contagem que reprovou>)`. Declarar a contagem que reprova e publicar assim mesmo é o pior dos dois mundos, porque produz um documento que prova o próprio defeito e não o corrige: o dono lê `0 de 4` e não tem como saber que isso significa que a régua reprovou. **Nenhuma justificativa de tipo de peça vale aqui:** se o formato dispensa a inversão, a exceção mora escrita na receita do tipo, e a entrega cita a linha dessa receita. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.

- **Passo 2 da checagem:** rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída; `exit` diferente de 0 reprova a entrega inteira.
