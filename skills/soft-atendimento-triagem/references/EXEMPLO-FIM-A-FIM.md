# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, empresa, números, datas e resultados foram inventados só pra
> mostrar a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega
> de verdade. Num trabalho real, todo dado sem fonte nasce marcado `[A CONFIRMAR]` e o dono confirma
> antes de sair.

**O caso fictício:** uma empresa que faz manutenção de equipamento de cozinha industrial (forno
combinado, fritadeira, câmara fria) pra restaurante, padaria e refeitório de empresa. O dono atende
sozinho com dois técnicos. Ele vende contrato mensal de manutenção preventiva `[fictício]` a partir
de R$ 890 por mês, e faz chamado avulso.

Ele voltou de uma semana fora e tem 43 contatos acumulados entre formulário do site, mensagem direta
e telefone.

Este arquivo mostra a saída resumida de cada ação, na ordem. A saída real é maior; aqui está só o
suficiente pra você reconhecer o formato antes de começar.

---

## O que o dono deu de entrada

> "Fiquei uma semana fora e tem 43 coisas pra responder. Metade deve ser besteira mas eu não sei
> qual metade. Não consigo olhar isso hoje inteiro, tenho dois atendimentos de manhã."

**O que faltava:** ele não tinha critério nenhum escrito, e a lista veio como um print da tela do
sistema mais um bloco de texto colado da caixa de mensagens.

## Ação 2 · CRITÉRIO (rodou primeiro, porque não existia)

As 5 perguntas, uma por vez:

1. *"Descreve o último cliente que deu muito certo."* → **"Uma rede de três padarias. Trocaram quatro fornos em dois anos porque ninguém fazia preventiva. Contrataram os três pontos de uma vez."**
2. *"E o último que deu errado? O que você teria visto antes?"* → **"Um restaurante que abriu fazia dois meses. Chamou pra três coisas em três semanas, pediu desconto em tudo, e fechou o restaurante antes de pagar a segunda. Eu teria visto se tivesse perguntado há quanto tempo eles abriram."**
3. *"O que você vende, e por quanto?"* → **"Contrato mensal a partir de 890. Avulso, 280 a visita mais peça."** `[fictício]`
4. *"O que você consegue saber sem perguntar?"* → **"O formulário do site pergunta o tipo de estabelecimento e quantos equipamentos. Na mensagem direta não vem nada, só o texto da pessoa."**
5. *"O que faz você descartar na hora?"* → **"Quem pergunta preço antes de dizer o que tem. E quem quer que eu vá ver de graça."**

Saída real: `criterio-triagem.md`. Resumo:

| Dimensão | Como ficou pra este negócio |
|---|---|
| **Encaixe cheio (25)** | Estabelecimento com 3 ou mais equipamentos, aberto há mais de 1 ano, ou mais de uma unidade |
| **Encaixe parcial (12 a 15)** | Um dos dois desconhecido (comum na mensagem direta, que não traz nada) |
| **Interesse** | Tabela padrão. Peso extra pra quem descreveu o equipamento e o defeito |
| **Urgência** | Palavra de prazo, mais o sinal próprio deste negócio: equipamento parado agora é urgência máxima |
| **Descarte imediato** | Cliente atual · pergunta preço sem dizer o que tem · pede visita de avaliação gratuita · aberto há menos de 6 meses (`[A CONFIRMAR]`: o dono achou duro, ficou como alerta em vez de descarte) |

**A decisão que a pergunta 2 gerou:** "aberto há menos de 6 meses" entrou como alerta amarelo, não
como corte, porque o dono relutou. Fica escrito assim no critério, pra ele decidir depois de duas ou
três filas.

---

## Ação 1 · FILA DO DIA

Saída real: `fila-do-dia.md`. Resumo:

### O que saiu da fila antes de qualquer nota

| Motivo | Quantos |
|---|---|
| Cliente atual (era chamado de contrato, não lead) | 7 |
| Contato repetido (mesma pessoa por formulário e mensagem) | 5 |
| Fornecedor, currículo e propaganda | 6 |
| Pediu visita de avaliação gratuita (descarte declarado pelo dono) | 3 |
| **Total fora antes da nota** | **21** |

**Só isso já cortou metade.** Os 7 clientes atuais eram chamados de manutenção esperando resposta há
uma semana, e viraram a primeira urgência do dia, fora da fila de aquisição.

### A fila (22 contatos avaliados, 8 mostrados pela régua de volume)

| # | Quem | De onde | Nota | Por quê | O que fazer |
|---|---|---|---|---|---|
| 1 | Refeitório da Metalúrgica Sertã | Formulário, 9 dias | 82 | Marcou 6 equipamentos e escreveu "câmara fria oscilando temperatura". Empresa grande, dentro do encaixe cheio. Está na janela de decisão (9 dias) e o problema descrito é o que vira parada de operação | Responder hoje, pessoalmente |
| 2 | Padaria Vila Nova (2 unidades) | Mensagem direta, 4 dias | 79 | Duas unidades, encaixe cheio. Escreveu "o forno da unidade nova apagou duas vezes essa semana". Equipamento intermitente é urgência que ela ainda não sabe que tem | Responder hoje |
| 3 | Restaurante Casa do Porto | Formulário, 12 dias | 71 | 4 equipamentos, aberto há 6 anos. Não descreveu defeito, marcou "quero conhecer o contrato mensal". Pediu o que você vende, sozinho | Responder hoje |
| 4 | Bruno (sem empresa identificada) | Mensagem direta, 3 dias | 58 | Descreveu bem o defeito da fritadeira, mas não disse onde nem quantos equipamentos. Interesse alto, encaixe desconhecido | Uma pergunta: qual o estabelecimento e quantos equipamentos |
| 5 | Cantina do Colégio Ribeira | Formulário, 18 dias | 54 | 3 equipamentos, encaixe cheio, mas nenhum sinal desde o cadastro e já passou da janela | Uma mensagem, sem esforço grande |
| 6 | Hamburgueria Fogo Alto | Formulário, 5 dias | 47 | 2 equipamentos (abaixo do encaixe) e aberta há 4 meses. Alerta amarelo do critério | Responder, com condição de pagamento à vista |
| 7 | Marcela (rede de cafeterias) | Indicação, 21 dias | 45 | Indicação de cliente atual, o que vale muito, mas 21 dias sem retorno e nenhum detalhe do que ela precisa | Retomada honesta, com saída fácil |
| 8 | Buffet Sant'Ana | Formulário, 27 dias | 41 | 5 equipamentos, encaixe cheio, mas quase um mês parado e sem sinal nenhum desde então | Última tentativa, curta |

**Os outros 14 numa linha:** 6 com mais de 60 dias e nenhum sinal, 5 fora do encaixe (residencial ou
1 equipamento), 3 pediram preço sem dizer o que têm (descarte declarado).

### Não dá pra avaliar (3 contatos)

Chegaram por mensagem direta com uma frase só, sem nome de estabelecimento e sem defeito descrito.

> "A pergunta que resolve os três é a mesma: 'que equipamento é, e ele está parado agora?'"

---

## Ação 3 · PRIMEIRA FRASE

Saída real: `primeiras-mensagens.md`. Três exemplos:

**1 · Refeitório da Metalúrgica Sertã** (canal: e-mail, foi por onde veio)

> Oi [nome], você preencheu o formulário há nove dias falando que a câmara fria está oscilando
> temperatura.
> Oscilação em câmara costuma ser uma de duas coisas, e uma delas é barata: ou é o degelo, ou é o
> pressostato. Dá pra saber pelo padrão do horário.
> Ela oscila mais em algum turno específico?

**2 · Padaria Vila Nova** (canal: mensagem direta)

> Oi [nome], você me falou que o forno da unidade nova apagou duas vezes essa semana.
> Apagar duas vezes em uma semana quase sempre vira apagar de vez num sábado de manhã, que é o dia
> que dói.
> Ele apaga durante o ciclo, ou na hora de ligar?

**7 · Marcela, indicação de 21 dias atrás** (canal: mensagem direta)

> Oi Marcela, o [nome do cliente que indicou] passou seu contato faz umas três semanas e eu demorei
> pra escrever.
> Já pode nem fazer sentido mais, mas se ainda estiver de pé: você tinha comentado com ele sobre a
> manutenção das máquinas das cafeterias?
> Se já resolveu, me avisa que eu não te encho.

**Nenhuma foi enviada.** As oito ficaram no arquivo, com o canal marcado em cada uma.

---

## Ação 4 · UM CONTATO SÓ (o dono colou um depois)

> **Dono:** "Chegou esse agora: 'Bom dia, quanto custa a manutenção?'. Vale?"

Resposta, em 5 linhas:

> Nota 22. O único dado é a pergunta de preço, sem estabelecimento, sem equipamento, sem defeito.
> Isso bate no seu descarte declarado ("pergunta preço antes de dizer o que tem").
> Recomendação: não descarte ainda, responda uma vez com uma pergunta e deixe o preço pra depois.
> A frase: "Bom dia! Depende do equipamento e de quantos são. Que máquinas você tem aí?"
> Se não responder em dois dias, aí sim descarte.

---

## O gate, no fim

| Check | Resultado |
|---|---|
| Cliente atual fora da fila de aquisição | ✓ 7 separados e virados em urgência de atendimento |
| Motivo com dado em toda posição | ✓ (a posição 5 foi reescrita: dizia "lead morno", virou "18 dias sem sinal desde o cadastro") |
| Fila curta | ✓ 8 de 43, pela régua de volume |
| Sinal velho marcado | ✓ posições 7 e 8 entraram com a marca |
| Furo visível | ✓ 3 contatos na faixa "não dá pra avaliar", com a pergunta |
| Anti-IA nas mensagens | ✓ (a mensagem 3 abria com "espero que esteja tudo bem", foi reescrita) |

```
$ python3 scripts/lint_copy.py primeiras-mensagens.md
OK (0 HARD, 0 WARN)
```

## A mensagem final ao dono

> Dos 43, 21 nem eram lead (7 são chamado de cliente seu esperando há uma semana, e esses vêm antes
> de tudo). Dos 22 que sobraram, 8 valem hoje, na ordem do arquivo, com a mensagem de cada um pronta
> pra você mandar.
>
> Uma coisa pra você decidir: você relutou em cortar quem abriu há menos de 6 meses. Deixei como
> alerta, não como corte, e a Hamburgueria Fogo Alto entrou por causa disso na posição 6. Roda duas
> ou três filas e você vai saber se corta ou não.
