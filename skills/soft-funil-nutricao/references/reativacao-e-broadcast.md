# Reativação e broadcast (P4 e P5)

Duas seções, dois trabalhos diferentes. A Seção 1 acorda base parada há 60 dias ou mais. A Seção 2 é o toque avulso fora da régua automática.

O que as duas têm em comum: nenhuma delas vende de cara, e as duas respeitam o filtro de cliente e a checagem de colisão com régua ativa.

---

# Seção 1 · Reativação de lista fria (60 dias ou mais sem interação)

## 1.1 Por que a oferta não acorda base fria

Base parada não deixou de comprar. Ela deixou de te ver. Quem some por 60 dias esqueceu o contexto, e a primeira coisa que recebe define se volta ou se marca como spam.

Oferta de cara faz três estragos ao mesmo tempo: chega sem contexto, confirma que você só aparece pra vender, e joga um volume grande de disparo numa base de baixa interação, que é exatamente o padrão que derruba a entrega.

O caminho que funciona é o inverso: **pergunta e utilidade primeiro, oferta só pra quem reagiu.**

## 1.2 O arco de reativação, 3 a 4 toques em 10 dias

| Dia | Toque | Canal | O trabalho |
|---|---|---|---|
| **D+0** | 1 · A pergunta | e-mail | reaparece com humildade, faz UMA pergunta que dá pra responder em 1 palavra, não vende nada |
| **D+3** | 2 · A utilidade | e-mail | entrega uma coisa útil sem pedir nada em troca, e ancora na resposta mais comum do toque 1 |
| **D+6** | 3 · O convite | e-mail + WhatsApp (só quem tem opt-in vivo) | agora sim, o convite pro destino, curto, com o filtro honesto |
| **D+10** | 4 · O corte | e-mail | avisa que vai parar, e dá a escolha de ficar. Depois disso, remove |

**A pergunta de 1 palavra (toque 1), o molde:**

> Assunto: ainda faz sentido?
>
> Faz um tempo que eu não te escrevo. Antes de mandar qualquer coisa nova, queria saber uma coisa só.
>
> Hoje, o que mais atrapalha a sua agenda: **falta**, **encaixe** ou **preço**?
>
> Me responde só a palavra. Eu te mando o que fazer com ela.

Por que funciona: pergunta fechada custa 3 segundos, e a resposta segmenta a base sozinha. Cada palavra vira uma tag, e o toque 2 sai personalizado sem trabalho extra.

**O corte (toque 4), o molde:**

> Assunto: última desta lista
>
> Eu vou parar de te escrever. Você entrou aqui quando baixou o [nome da isca], e faz [N] meses que a gente não se fala.
>
> Se ainda quiser receber, me responde qualquer coisa, ou clica aqui: [link]. Se não responder, eu te tiro da lista e a gente fica bem.

Por que funciona: é honesto, dá agência ao lead, e faz a poda que a entrega precisa. Quem clica volta engajado; quem não clica não ia abrir mesmo.

## 1.3 Higiene, a parte que protege a entrega

- **Volume gradual.** Não dispare pra base fria inteira de uma vez. Comece pelos mais recentes (os que pararam há 60 a 90 dias), veja a resposta, e só então avance pros mais antigos. Disparo em massa pra base morta é o que aciona o filtro.
- **Remova o hard bounce na hora.** Endereço que não existe volta uma vez e sai.
- **Remova quem não reagiu no fim do arco.** É contraintuitivo e é o que salva a lista: manter contato morto derruba a métrica de todo mundo, inclusive de quem abre.
- **Nunca reinsira quem marcou spam.** Em nenhuma lista, por nenhum motivo.
- **Registre o que aconteceu.** Quantos responderam, quantos clicaram, quantos saíram. Sem esse número a próxima reativação repete os mesmos erros.

`[A CONFIRMAR]` as faixas de taxa de reativação por nicho. O número que circula (algo entre 5% e 15% da base fria voltando a interagir num arco bem feito) serve de calibragem de expectativa, não é dado auditado.

## 1.4 O que a reativação NÃO faz

- não abre com oferta
- não abre com desculpa longa ("desculpa o sumiço, ando muito corrido")
- não usa urgência fabricada pra forçar o retorno
- não dispara pra base inteira de uma vez
- não mantém quem não reagiu no fim do arco

---

# Seção 2 · Broadcast (o toque avulso pra base)

## 2.1 O que autoriza um broadcast

Broadcast é a mensagem única, fora da régua automática, pra um recorte da base. Ele custa caro em confiança, então só sai com **motivo real**:

| Motivo válido | Exemplo |
|---|---|
| **Notícia real** | turma nova abrindo, mudança no produto, evento com data |
| **Conteúdo que vale sozinho** | uma coisa útil que a pessoa usaria mesmo sem comprar nada |
| **Convite com janela** | uma sessão, uma aula, uma vaga que existe de verdade e fecha de verdade |
| **Aviso de serviço** | mudança de canal, de horário, de link |

**O que não autoriza:** a meta do mês, a semana fraca, o "faz tempo que a gente não fala". Broadcast sem notícia treina a base a ignorar o próximo, e o próximo é justamente o que você vai precisar que funcione.

## 2.2 As 4 checagens antes de disparar

Roda as quatro, sempre, nesta ordem:

1. **Motivo real?** Se você não consegue dizer a notícia em 1 frase, não tem broadcast.
2. **Filtro de cliente.** Quem já comprou não recebe convite pra comprar o que já tem.
3. **Colisão com régua ativa.** Quem está no meio de uma sequência não recebe o broadcast no mesmo dia. Ou espera, ou é excluído do recorte.
4. **Recorte certo.** Broadcast pra base inteira é quase sempre broadcast pra ninguém. Corte por temperatura, por isca consumida, ou por interesse declarado.

## 2.3 O molde do broadcast

**Estrutura, 4 linhas:**
1. a notícia, na primeira linha, sem aquecimento
2. o que ela muda pra quem está lendo
3. o link, sozinho
4. a saída, ou o "se não for pra você, ignora essa"

**Exemplo fictício, WhatsApp** (nicho neutro: consultoria de organização de agenda pra clínicas pequenas):

> Abri uma sessão nova na quinta, 19h, sobre encaixe de agenda. São 20 lugares porque é ao vivo e eu respondo pergunta.
>
> Se a sua agenda enche e o faturamento não acompanha, é essa a conversa.
>
> [link]
>
> Se não for o seu momento, ignora essa que na semana que vem eu não te chateio.

**Frequência:** no máximo 1 broadcast por semana pra mesma base, e nunca dois em dias seguidos. Se você precisa de mais que isso, o que você quer não é broadcast, é uma régua.

## 2.4 Broadcast x régua, a fronteira

| | Broadcast | Régua |
|---|---|---|
| **Dispara por** | um evento que aconteceu | uma ação do lead (baixou, clicou, respondeu) |
| **Quantas mensagens** | uma | várias, encadeadas |
| **Personalização** | por recorte de lista | por comportamento individual |
| **Quando usar** | notícia real com data | sempre que existe entrada nova de lead |

Se você está pensando em mandar 3 broadcasts encadeados, você está montando uma régua sem chamar pelo nome, e sem os filtros que a régua tem. Monte a régua.

## 2.5 Anti-patterns das duas seções

| Sintoma | Correção |
|---|---|
| Reativação abriu com oferta | Abre com pergunta de 1 palavra. Oferta só pra quem reagiu |
| Disparou pra base fria inteira de uma vez | Volume gradual, do mais recente pro mais antigo |
| Manteve quem não reagiu no fim do arco | Remove. Contato morto derruba a entrega de quem está vivo |
| Reinseriu quem marcou spam | Nunca. Em nenhuma lista |
| Broadcast sem notícia real | Sem notícia não tem broadcast. Espera ter |
| Broadcast bateu em quem estava no meio da régua | Checa colisão e exclui do recorte |
| Broadcast pra base inteira sempre | Recorta por temperatura ou por isca consumida |
| Três broadcasts encadeados | Isso é uma régua. Monta como régua, com os filtros dela |
| Pediu desculpa longa pelo sumiço | Uma linha, e vai pra pergunta. A desculpa não interessa ao lead |
| Urgência fabricada pra forçar retorno | Se a vaga não fecha de verdade, não diz que fecha |
