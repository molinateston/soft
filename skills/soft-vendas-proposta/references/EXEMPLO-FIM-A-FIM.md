# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, empresa, números, preços e falas foram inventados só pra
> mostrar a FORMA de cada saída. Nada disso é caso real. Numa proposta de verdade, todo número vem do
> dono, toda fala tem dono declarado, e o que faltar nasce marcado `[A CONFIRMAR]`.

**O caso fictício:** o dono é consultor de operação pra redes de lavanderia. O cliente fictício é a
Lavanderia Bem Passado, 4 lojas numa cidade média. A call durou 52 minutos e foi gravada.

**O pedido que o dono deu, literal:** *"acabei de sair da call com o pessoal da Bem Passado. Monta a
proposta, eles querem por escrito até sexta."*

Este arquivo mostra a saída RESUMIDA de cada ação. A saída real é bem maior.

---

## Ação 1 · EXTRAÇÃO

A skill perguntou uma coisa só antes de começar: *"você tem a call gravada ou vamos pelas suas
anotações?"*. Ele tinha a gravação, então a extração saiu da transcrição inteira, lida do começo ao
fim.

Saída, o `01-diagnostico-proposta.md`, os 12 campos:

| # | Campo | Preenchido |
|---|---|---|
| 1 | Cliente e empresa | Renato Alcântara, Lavanderia Bem Passado ME (grafia conferida no cadastro) |
| 2 | Nicho | lavanderia de bairro, público residencial mais 3 hotéis pequenos |
| 3 | Produtos hoje | lavagem por peça (ticket médio R$ 38) e contrato mensal com hotel (R$ 2.400 por hotel) |
| 4 | Faturamento | *"a gente fecha uns 120 mil no mês somando as 4"*, **fala do cliente** |
| 5 | Time | 11 pessoas, sem ninguém olhando as 4 lojas junto |
| 6 | Dor central | *"eu descubro que a loja 3 deu prejuízo dois meses depois"*, **fala do cliente** |
| 7 | Objetivo de 12 meses | abrir a quinta loja sem depender dele estar dentro |
| 8 | O que o dono sugeriu | painel semanal por loja, e **como upsell sugerido**, o treinamento do gerente de cada unidade |
| 9 | Preço oferecido | consultoria de 6 meses, R$ 3.900 por mês; implantação avulsa, R$ 12.000 |
| 10 | Reação | interessado, pediu por escrito, disse que decide com a esposa, que é sócia |
| 11 | Próximos passos | proposta até sexta, resposta na terça seguinte |
| 12 | Personalização | azul da marca (#1f5aa8), tom direto, sem juridiquês |

**A separação que o diagnóstico deixou explícita:** o cliente pediu o painel por loja. O treinamento
dos gerentes foi sugestão do dono, e entra na proposta marcado como upsell, não como escopo central.

**O número que quase virou erro:** na call o dono disse *"eu já fiz isso numa rede de 9 lojas"*. Esse
número é do DONO, não do cliente, e ficou registrado assim no diagnóstico, pra não aparecer no site
como se fosse da Bem Passado.

**STOP obrigatório.** Ele leu os 12 campos e corrigiu um: o contrato com hotel são R$ 2.400 por mês
somando os três, não por hotel. Correção feita antes de existir qualquer HTML.

---

## Ação 2 · ESTRUTURA

Saída, a seção de estrutura do mesmo documento:

| Ordem | Aba | O que carrega |
|---|---|---|
| 1 | Visão Geral | quem é a Bem Passado, a dor com a fala dele, e onde ele quer estar em 12 meses |
| 2 | O Diagnóstico das 4 Lojas | o que a call revelou, loja a loja, em duas colunas |
| 3 | Entregáveis | o painel por loja, a rotina semanal, os encontros, com marcação que persiste |
| 4 | Plano de Ação | cronograma de 6 meses, mês a mês |
| 5 | Investimento | 3 opções, validade de 7 dias |

**As 3 opções desenhadas:** consultoria de 6 meses; consultoria mais implantação; e a implantação
avulsa como caminho de entrada. O treinamento dos gerentes aparece dentro da opção do meio, marcado
como sugestão do consultor, não como pedido dele.

**STOP.** Aprovado sem ajuste.

---

## Ação 3 · GERAÇÃO

**Layout escolhido:** claro corporativo, pela tabela de decisão. Lavanderia com contrato de hotel é
cliente conservador, e ele mandou a cor da marca. O azul dele entrou no destaque.

**Prova social:** o dono tinha 2 casos com número, ambos autorizados por escrito. Entraram os dois.
Um terceiro caso, sem autorização, ficou de fora, e isso foi dito em 1 linha.

**Valor de mercado precificado:** a proposta mostra quanto custaria contratar uma empresa pra
desenvolver o painel de 4 lojas separado, o que ancora o valor da consultoria na conta que ele já
entende.

Saída, o arquivo `proposta-bem-passado.html`, arquivo único, estilo e script embutidos, abre sem
conexão.

**STOP.** Ele leu a proposta inteira e pediu pra trocar "investimento" por "valor" no botão final.

---

## Ação 4 · PUBLICAÇÃO

Antes do link, o teste no celular, os 6 itens:

| Item | Resultado |
|---|---|
| Topo cabe sem rolagem lateral | passou |
| Abas clicáveis com o polegar | reprovou na primeira, as abas ficaram estreitas demais; voltou pra Ação 3 |
| Tabela de investimento sem estourar | passou |
| Cronograma rola dentro dele mesmo | passou |
| Marcação dos entregáveis persiste | passou |
| Chamado final visível | passou |

Depois do conserto das abas, os 6 passaram e o link foi publicado em endereço privado, não
adivinhável, não listado em lugar nenhum.

**A mensagem pronta que a skill entregou junto:**

> Renato, ficou pronta. É um link só seu, não está publicado em lugar nenhum:
> [link]
>
> Tem 3 caminhos lá dentro, com o que muda em cada um. A condição vale até [data, 7 dias].
> Qualquer dúvida me chama que eu explico por áudio.

---

## O caminho sem gravação (o mesmo caso, se ele não tivesse gravado)

Se ele tivesse dito *"não gravei, mas anotei tudo"*, a skill rodaria as 8 perguntas de reconstrução,
uma por vez. A diferença na saída seria esta:

| Com gravação | Sem gravação |
|---|---|
| *"eu descubro que a loja 3 deu prejuízo dois meses depois"*, entre aspas, fala literal do cliente | ele contou que descobre o prejuízo da loja 3 só dois meses depois, **em paráfrase, sem aspas** |
| ticket médio R$ 38, dito por ele na call | ticket médio `[A CONFIRMAR]`, o dono confere no sistema antes de publicar |

O resto do fluxo é idêntico. A proposta sai; o que muda é que nenhuma fala reconstruída de memória
aparece entre aspas.

---

## O que ficou pendente no caso fictício

- O terceiro caso do dono, sem autorização por escrito: fora da proposta até virar prova usável.
- A resposta do cliente na terça: se vier o sim, o contrato é da `soft-vendas-contratos`.
- O follow-up dos 7 dias de validade é do closer, que cobra no dia 5 e fecha ou encerra no dia 7.
