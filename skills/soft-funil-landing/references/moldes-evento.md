# Moldes da página de evento: curto, longo grátis e longo pago

Abre quando o tipo é Registro de evento (aula, webinar perpétuo com horário, live, masterclass, workshop, imersão) ou o ingresso pago de um evento. Traz a regra de qual molde usar, os 3 moldes com lacunas, o hero, a página de obrigado que puxa comparecimento e a regra de escassez e de promessa de entrega. Os moldes saíram de 4 páginas de inscrição validadas pelo dono; nenhuma frase delas está aqui, só a função de cada bloco. Toda lacuna `[DO DONO: ...]` se preenche com o insumo; lacuna sem dado no insumo some da página e vira pergunta no `_notas-operador.md`.

Cada molde aponta os blocos do template `assets/landing-base.html` (o nome entre crases é o `data-bloco`). Bloco que o molde não lista sai do HTML.

---

## 1. Qual molde (regra de decisão)

| Tráfego | Evento grátis | Evento pago (ingresso) |
|---|---|---|
| Quente (lista, seguidor, remarketing, anúncio que já explicou a aula) | CURTO | LONGO PAGO |
| Morno (conhece o dono de nome, ainda não confia) | LONGO GRÁTIS | LONGO PAGO |
| Frio (anúncio pra quem nunca viu o dono) ou público cético | LONGO GRÁTIS | LONGO PAGO |
| Não declarado | assuma frio: LONGO GRÁTIS | LONGO PAGO |

**Por quê.** A página curta confia que o anúncio já vendeu a aula e só não atrapalha quem decidiu. No frio isso não existe: o formulário no topo pega quem já veio convencido, e o resto da página trabalha quem precisa de mais motivo (o que vai aprender, o filtro, a bio). No pago, a pessoa tira dinheiro do bolso, então a página é de venda: entregas, lote, garantia e perguntas frequentes, com o formulário no fim.

**Declaração, uma linha no topo do `.md` da copy:** `Tráfego <frio/morno/quente, e de onde tirei> · evento <grátis/pago, data fixa ou sessões> → molde <CURTO/LONGO GRÁTIS/LONGO PAGO>, porque <motivo em meia linha>.`

Perpétuo com horário marcado (sessões que se repetem) é evento: entra no molde pelo tráfego, com o seletor de horário como primeiro campo. Aula gravada que a pessoa assiste na hora, sem horário, é Captura (Tipo 1).

---

## 2. O hero de inscrição (vale nos 3 moldes)

**Molde:** `[DO DONO: resultado concreto da aula ou do evento] mesmo sem [DO DONO: a objeção que o insumo lista]` ou `mesmo que [DO DONO: situação de hoje do público]`. Com método nomeado no insumo: `[resultado] com [nome do método] mesmo sem [objeção]`.

**Regras, com motivo:**
- O hero promete o resultado DA AULA (o que a pessoa sai sabendo ou fazendo), nunca o do produto que vem depois. A aula é o que a pessoa está comprando com o e-mail.
- O "mesmo que / mesmo sem" entra sempre que o insumo lista objeção, crença ou "quem acha que precisa de X". Motivo: a objeção é o que segura o dedo em cima do botão; nomeada no hero, ela cai antes do primeiro rolar.
- Aqui o teste do espelho não vale. O anúncio já prometeu, e a página repete a promessa com as palavras do anúncio (Message Match, `tipos-de-landing.md`, princípio 2). Hero que foge da promessa do anúncio pra parecer original quebra o elo e perde o clique pago.
- O inimigo, a tese e o diagnóstico não são hero de inscrição. Eles vão pro corpo da aula e, se couber, pra um card.
- Nome do evento e formato vão na etiqueta acima do hero (`[DO DONO: nome e formato com a palavra do insumo]`), nunca como o hero. Gravado ou perpétuo nunca vira "ao vivo"; "gratuita" e "sem custo" só se o insumo diz do próprio evento (o diagnóstico grátis que vem depois não torna a aula grátis).
- Número de autoridade nas 5 primeiras linhas (a `prova-linha`, logo sob a sub). Prova acima da dobra é a regra; bio longa, quando existe, fica no fim.

**Contraste (nicho fictício, confeitaria):**
- Fraco: "A confeitaria caseira que ninguém te contou". Tese sem resultado e sem objeção.
- Fraco: "O mercado de doces não paga quem faz bem feito". Inimigo no lugar da promessa.
- Forte: "Venda 40 bolos de pote por semana pelo WhatsApp, mesmo sem ter loja nem seguidor". Resultado da aula, número do insumo, duas objeções que o insumo listava.

---

## 3. Molde CURTO (tráfego quente, uma dobra)

| # | Bloco | Template | Lacuna |
|---|---|---|---|
| 1 | Etiqueta do evento | `hero` (etiqueta) | [DO DONO: formato em 2 ou 3 palavras] |
| 2 | Headline | `hero` | molde do hero (seção 2) |
| 3 | Linha de prova | `hero` (prova-linha) | [DO DONO: 1 número conferível de quem chegou ao resultado] |
| 4 | Objeções em lista "sem" | `lista-sem` | [DO DONO: 3 a 5 coisas que o público acha que precisa e não vai precisar] |
| 5 | O que vai ver | `hero` (lista-ganhos) | [DO DONO: 3 ou 4 descobertas, o quê, nunca o como] |
| 6 | Cartão do condutor | `condutor-mini` | [DO DONO: foto, nome, papel] |
| 7 | Data e hora, ou a escolha | `cartao-form` | [DO DONO: dia e hora; ou sessões no `seletor-horario`] |
| 8 | Formulário curto | `cartao-form` | [DO DONO: campos que o insumo pede; sessão primeiro quando houver] |
| 9 | Micro-garantia | `cartao-form` (micro) | [DO DONO: uma verdade do insumo que tira o medo do clique, como a duração]. Sem dado, a linha sai (seção 9) |
| 10 | Barra fixa no celular | `barra-fixa` | mesmo texto do botão |

Um botão (mais a barra fixa, que aponta pro mesmo lugar). Sem faixa de selos, sem bio longa, sem FAQ.

---

## 4. Molde LONGO GRÁTIS (tráfego frio ou morno)

| # | Bloco | Template | Lacuna |
|---|---|---|---|
| 1 | Faixa de 3 selos | `faixa-selos` | [DO DONO: formato com a palavra do insumo · política de gravação que o dono decidiu · limite com motivo]. Selo sem dado sai |
| 2 | Foto do condutor com números na legenda | `foto-hero` | [DO DONO: foto vertical, nome, 2 ou 3 números reais] |
| 3 | Headline e sub | `hero` | molde do hero; a sub diz o que a aula mostra |
| 4 | Prova e 3 ganhos | `hero` (prova-linha, lista-ganhos) | [DO DONO: 1 número] · [DO DONO: 3 ganhos] |
| 5 | Cartão do formulário, na primeira tela | `cartao-form`, `contador`, `seletor-horario`, `numeros-form` | [DO DONO: data fixa ou sessões; sem horário no insumo, sem seletor] · nome, e-mail, WhatsApp se o insumo pede · micro-garantia com dado · [DO DONO: 3 números de autoridade] |
| 6 | O que vai descobrir | `cards` | [DO DONO: 5 ou 6 tópicos da aula, rótulo curto e 1 frase, cada um tocando uma dor, desejo ou dúvida] |
| 7 | É pra você se | `pra-voce` (lado sim) | [DO DONO: 3 a 5 cenas da rotina do público, do insumo]. Alternativa: antes e depois no mesmo componente |
| 8 | Não é pra você se | `pra-voce` (lado não) | [DO DONO: quem o insumo exclui] · [linha anti-milagre: quem procura atalho sem esforço] |
| 9 | Botão do meio | `cta-meio` | mesmo texto e destino do botão principal |
| 10 | O que vem junto e o que vem depois | `cards` | [DO DONO: material real de quem se inscreve] · [DO DONO: o objetivo de conversão declarado, como a candidatura a uma sessão], obrigatório quando o dono declara. Valor em dinheiro só se já foi vendido por esse preço |
| 11 | Bio longa | `bio` | [DO DONO: virada, feito com número conferível, credenciais] |
| 12 | Botão final e micro | `cta-final` | a mesma micro do formulário, se ela existe |
| 13 | Rodapé | rodapé | [DO DONO: razão social, privacidade] |
| 14 | Barra fixa no celular | `barra-fixa` | some quando o formulário aparece na tela |

**Seletor de horário como primeiro campo** quando o insumo dá as sessões. Motivo: escolher o horário vira compromisso antes de digitar o nome, e a pessoa escolhe o horário em que vai estar livre. Sem horário no insumo, o seletor sai inteiro e `quais sessões e horários?` vai pro `_notas-operador.md`; opção "Sessão a confirmar" ou lista vazia publicada reprova.

**Números repetidos 2 ou 3 vezes** (legenda da foto, cartão, bio) são os MESMOS números, com o mesmo valor e o mesmo nome do evento em toda a página. Uma página que chama o evento de aula, curso e treinamento, ou mostra 3 contagens diferentes de alunos, perde a confiança que os números compraram.

---

## 5. Molde LONGO PAGO (ingresso, evento de data fixa)

| # | Bloco | Template | Lacuna |
|---|---|---|---|
| 1 | Faixa ou selo de data | `faixa-selos` | [DO DONO: formato, datas, horário, plataforma, com a palavra do insumo] |
| 2 | Headline e sub | `hero` | molde do hero, com o resultado do evento |
| 3 | Vídeo "assista antes de decidir" | `video-hero` | [DO DONO: embed do player]. Sem vídeo, o bloco sai |
| 4 | O que vai aprender e botão que desce | `hero` (lista-ganhos, botao-desce) | [DO DONO: 3 a 5 tópicos] |
| 5 | 3 números | `numeros-grade` | [DO DONO: participantes, anos, horas, o que o insumo tiver, com o rótulo do insumo] |
| 6 | Entregas com valor | `cards` | [DO DONO: o que o evento entrega; preço de mercado só se o insumo dá e dá pra conferir] |
| 7 | Como funciona por dentro | `cards` ou parágrafo | [DO DONO: o mecanismo] |
| 8 | É pra você / não é | `pra-voce` | como no longo grátis |
| 9 | Lotes | `lotes` | [DO DONO: preço por lote · o que faz o lote virar (número de ingressos, data) · o que inclui]. Lote ativo em destaque, os seguintes visíveis e bloqueados |
| 10 | Garantia com título vendido | `garantia` | [DO DONO: prazo e regra] |
| 11 | Formulário e o que acontece depois de pagar | `form-final` (id vira `inscricao`) | 3 campos do insumo · [DO DONO: 3 passos depois do pagamento, cada um com linha do insumo] |
| 12 | Perguntas frequentes | `faq` | [DO DONO: preço e por que sobe, pré-requisito, equipamento, acesso e gravação, garantia] |
| 13 | Rodapé com aviso legal de resultado | rodapé | [DO DONO: razão social] · aviso de que valor citado é referência e não promessa de ganho |
| 14 | Barra fixa no celular | `barra-fixa` | mesmo destino |

**Motivo da ordem.** Quem paga precisa ver o que leva antes do preço (entregas, mecanismo), depois o preço com o motivo de ele subir, depois o que tira o risco (garantia), e só então o formulário. As perguntas frequentes pegam quem rolou até o fim com uma dúvida só.

---

## 6. Escassez, prazo, preço riscado, lote e selo

A regra: urgência só com motivo que o lead consegue conferir. Motivo: o público reconhece urgência de enfeite, e uma que ele pega mentindo derruba todas as outras frases da página.

| Elemento | Entra quando | Sem o dado |
|---|---|---|
| Data e hora | o insumo dá | `[DO DONO: data]` no `.md`; o HTML não sai com a data vazia, a pergunta vai pro `_notas-operador.md` |
| Contador | data futura real (evento ou próxima sessão) | sem contador. O script do template esconde o contador quando a data passa |
| "Vagas limitadas", número de vagas | o insumo dá o número e o motivo (sala, turma, atendimento) | sai. Botão sem "vaga": "garantir meu lugar", "quero participar", "escolher meu horário" |
| "Sem replay", "não fica gravado" | o dono decidiu a política de gravação | sai; a pergunta vai pro `_notas-operador.md` |
| "Hoje", "última chance" | só em evento de data única, na véspera ou no dia | sai. Em sessão que se repete todo dia é enfeite |
| Preço riscado (inclusive "de R$ X por zero") | o insumo diz que aquele valor já foi cobrado por aquilo | sai. Âncora sem lastro é invenção |
| Lote e virada | o insumo dá preço de cada lote e o critério de virada | sem lote; preço único do insumo |
| Valor de mercado das entregas | o insumo dá o valor e ele é conferível | a entrega entra sem valor |

---

## 7. Promessa de entrega: canal, lembrete, link, bônus

Canal, prazo e forma de entrega (lembrete no WhatsApp, link por e-mail, bônus que chega depois, acesso imediato) só entram com linha do insumo. Motivo: promessa de entrega falsa vira reclamação no primeiro dia, e o dono nem sabe que prometeu.

Sem a linha no insumo, a página diz só o que é certo ("depois de enviar, você cai na página de confirmação"; data e agenda só quando o insumo dá a data) e o canal vai pro `_notas-operador.md` como pergunta: `canal do lembrete? · link de acesso chega por onde e quando? · bônus chega quando?`.

Anti-padrão: completar canal, horário de lembrete ou prazo de bônus a partir de um exemplo de receita. Exemplo ilustra a forma e nunca é dado.

---

## 8. Obrigado que puxa comparecimento

| # | Bloco | Lacuna | Regra |
|---|---|---|---|
| 1 | Confirmação | [curta: inscrição feita] | uma linha |
| 2 | Data e hora de novo | [DO DONO: data e hora] ou o horário escolhido | no perpétuo o template lê o horário de `?sessao=` ou do formulário. Sem data nem sessão no insumo, a linha sai; nunca "você recebe o horário por e-mail" sem linha do insumo |
| 3 | Um próximo passo | agenda (padrão) · grupo ou WhatsApp só com o link no insumo | UM botão. A agenda cobre TODAS as datas do evento (duas noites, dois eventos na agenda) ou não é oferecida; sem data, sem agenda. A micro do botão promete só o que o arquivo de agenda leva |
| 4 | Pequeno compromisso | [uma ação de 10 segundos ligada ao botão, ou uma decisão: bloquear o horário, avisar quem mora junto] | nada que peça canal que o insumo não tem |
| 5 | O que preparar | [DO DONO: 1 a 3 itens que o insumo cita] | sem item no insumo, pergunte; "leve uma dúvida" serve quando a aula é ao vivo |
| 6 | O que vem depois | [DO DONO: o objetivo de conversão declarado] | uma linha de texto, nunca segundo botão; obrigatório quando o dono declara |

**Por quê.** A pessoa acabou de dizer sim e está com a atenção mais alta do funil. O que ela faz nos 20 segundos seguintes (pôr na agenda, se comprometer com uma coisa pequena, saber o que levar) decide se aparece. Dois botões dividem essa atenção; nenhum a desperdiça.

Evento pago: o obrigado confirma o pagamento, repete data e hora, e o próximo passo é o que o insumo diz (grupo da turma, e-mail de acesso). Sem o dado, agenda.

---

## 9. Texto fixo da página: cada linha é um campo

Todo texto que parece padrão (micro sob o botão, selo, formato, confirmação, rodapé, rótulo de número) é campo. Entra com dado do insumo; sem dado, o elemento sai da página e vira pergunta no `_notas-operador.md`. Motivo: frase padrão é afirmação sem dono, e o visitante lê como promessa.

| Elemento | Entra quando | Sem o dado |
|---|---|---|
| "Sem custo", "gratuita", "grátis" | o insumo diz que ESTE evento é grátis | sai |
| "Seus dados ficam só comigo", "dados protegidos", "sem spam" | o insumo traz a política de dados | sai; o link da política vai no rodapé quando existe |
| "Pagamento protegido", "compra segura" | o insumo nomeia o checkout e o que ele garante | sai |
| Formato ("ao vivo", "online", "gravada") | o insumo diz o formato, com essa palavra | sai; perpétuo e gravado nunca levam "ao vivo" |
| Confirmação "por e-mail" ou "no WhatsApp" | o insumo diz o canal | a confirmação fica "inscrição feita", sem canal |
| Seletor de sessões | o insumo dá dia e hora de cada sessão | sai; pergunta a grade |
| Razão social e privacidade no rodapé | o insumo dá | sai; nunca `#CONECTAR-...` visível |
| Objetivo de conversão (diagnóstico, candidatura, sessão) | o dono declara no pedido ou no insumo | não se aplica: quando declarado, aparece na página e no obrigado |

**Número com o rótulo do insumo (contraste, nicho fictício):**
- Fraco: insumo "gerenciei R$ 20 milhões", página "R$ 20 milhões em anúncio". Acrescentou objeto.
- Fraco: insumo "mais de 300 alunas", página "300 confeiteiras". Trocou o rótulo e tirou o "mais de".
- Fraco: insumo "R$ 80 mil no ano" e, noutra linha, "fez 12 lançamentos", página "R$ 80 mil num único lançamento". Ligou resultado a uma causa que o insumo não liga.
- Forte: "Gerenciou mais de R$ 20 milhões", "mais de 300 alunas". Verbo, objeto e "mais de" do insumo.

