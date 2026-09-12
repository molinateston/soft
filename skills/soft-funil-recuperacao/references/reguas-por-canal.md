# Réguas de recuperação por canal (o arco de toques detalhado)

A régua de recuperação vai buscar a venda que parou no checkout. Ela roda em 3 canais que trabalham juntos, cada um com um ritmo e um papel. Este arquivo traz o arco de toques de cada canal, a cadência por gatilho de evento e a copy-molde de cada função. Todo número, preço, desconto, garantia e prova é do dono; os moldes usam campo `[ ]` onde o dado entra.

---

## Seção 1 · O arco de toques (o que vale nos 3 canais)

A pessoa já quis comprar. Cada toque escala a intenção sem cansar, e cada um tem uma função no arco. O e-mail é o canal mais completo (roda o arco inteiro); o SMS pega o começo e o pico de urgência; o WhatsApp roda a conversa com desconto progressivo.

| Toque | Função | O que faz | Onde brilha |
|---|---|---|---|
| 1 | neutro | "falta um passo": lembra a compra, sem pressão; formas de pagamento, garantia, acesso imediato | e-mail, SMS |
| 2 | reconhecimento | parabeniza pela decisão, tira o atrito, oferece ajuda no canal, manda o link de onde parou | e-mail, WhatsApp |
| 3 | prova | mostra que gente como ela resolveu; traz a objeção real e a resposta | e-mail |
| 4 | benefício | lista o que a pessoa desbloqueia ao concluir | e-mail, WhatsApp |
| 5 | dor | reconecta com a dor que a levou ao checkout, nas palavras dela | e-mail |
| 6 | dor perigosa | mostra o custo de deixar como está, com respeito, sem terror | e-mail |
| 7 | objeção / FAQ | responde o que segura a compra: funciona? é fácil? em quanto tempo? e se não der certo? | e-mail |

**Duas regras de arco:**
- **Um convite por toque.** Cada mensagem leva a UMA ação: concluir a compra, ou responder pra pedir ajuda. Nunca as duas.
- **A prova entra por resultado, não por tempo de casa.** "Mais de mil pessoas resolveram" só entra com o número no disco; "nove anos de mercado" mede o vendedor, não o que a pessoa ganha.

---

## Seção 2 · E-mail (o arco longo)

Cadência de 10 minutos a 72 horas, até 7 toques, escalando urgência e prova. Cada toque tem assunto, pré-cabeçalho e corpo curto, escaneável no celular, com um único botão. O link de retomada é campo (`[LINK]`, fim da linha).

### Cadência por gatilho

| Toque | Pix gerado | Checkout abandonado | Cartão recusado | Função |
|---|---|---|---|---|
| E0 | 10 min | 10 min | 10 min | neutro |
| E1 | 1 h | 1 h | 1 h | reconhecimento |
| E2 | 4 h | 4 h | 4 h | prova |
| E3 | 12 h | 12 h | 12 h | benefício |
| E4 | 24 h | 24 h | 24 h | dor |
| E5 | 48 h | 48 h | 48 h | dor perigosa |
| E6 | 72 h | 72 h | 72 h | objeção / FAQ |

### Moldes de copy (função por função)

**E0 · neutro (10 min).**
> Assunto: falta um passo pra fechar seu [PRODUTO]
> Pré-cabeçalho: conclua e receba o acesso agora mesmo
> Corpo: Olá [NOME], falta só um passo pra concluir sua compra do [PRODUTO]. É só clicar no botão e finalizar. Formas de pagamento: [FORMAS]. Acesso no mesmo minuto. Garantia de [PRAZO] dias. [BOTÃO: concluir] [LINK]

**E1 · reconhecimento (1 h).** Parabeniza pela decisão, diz que falta o último passo, oferece ajuda: "se teve dificuldade pra concluir, responde este e-mail que eu te ajudo".

**E2 · prova (4 h).** Traz 2 a 3 falas de dor reais do público (verbatim) e a virada: quem aplicou resolveu. Fecha com o convite. Número de prova só com lastro no disco.

**E3 · benefício (12 h).** Lista o que a pessoa desbloqueia ao concluir (os bullets da oferta real). Preço promocional SÓ se o dono deu.

**E4 · dor (24 h).** Reconecta com a dor: "como você se sente quando [DOR]?". Usa as falas do público. Fecha no convite.

**E5 · dor perigosa (48 h).** Mostra o custo de não resolver, com respeito. Traz bônus real, se houver. Sem terror, sem promessa inventada.

**E6 · objeção / FAQ (72 h).** Responde as perguntas que seguram a compra: o que é o [PRODUTO], é fácil de aplicar, em quanto tempo dá resultado, funciona mesmo, e a garantia. É o toque que fecha o arco.

**Assunto:** nasce da régua de títulos, com gatilho nomeado, nunca em caixa alta. Um assunto por toque.

---

## Seção 3 · SMS (o toque que chega na hora)

Agressivo no timing, curtíssimo no tamanho. **SEM acento** (o acento quebra em muito aparelho). Uma linha, nome no início, link no fim como campo. Nada de parágrafo.

### Cadência por gatilho

| Gatilho | Toque | Timer | Molde (sem acento) |
|---|---|---|---|
| **Pix gerado** | S1 | 5 min | `[NOME]; seu PIX do [PRODUTO] foi gerado. Conclua pelo link: [LINK_PIX]` |
| | S2 | 10 min | `[NOME]; seu PIX do [PRODUTO] vence em 15 min. Codigo aqui: [LINK_PIX]` |
| | S3 | 40 min | `[NOME]; [CONDICAO ESPECIAL, se o dono deu] acesse o [PRODUTO]: [LINK]` |
| **Checkout abandonado** | S1 | 7 min | `[NOME]; falta um passo pra concluir seu [PRODUTO]. Termine aqui: [LINK]` |
| | S2 | 30 min | `[NOME]; [CONDICAO ESPECIAL, se o dono deu] garanta seu [PRODUTO]: [LINK]` |
| **Cartão recusado** | S1 | 2 min | `[NOME]; seu cartao nao passou. Conclua a compra por aqui: [LINK]` |
| | S2 | 20 min | `[NOME]; ainda da tempo de garantir o [PRODUTO]. Termine aqui: [LINK]` |
| | S3 | 40 min | `[NOME]; [CONDICAO ESPECIAL, se o dono deu] pegue seu [PRODUTO]: [LINK]` |

**Por que o Pix abre em 5 min:** o Pix copia-e-cola vence em minutos. O SMS chega na hora e é o único canal rápido o bastante pra pegar a janela antes do vencimento.

**Por que o cartão recusado abre em 2 min:** quase sempre é limite ou dado digitado errado, não desistência. O toque tira o atrito enquanto a pessoa ainda está no celular.

**O `[CONDICAO ESPECIAL]` só existe se o dono deu o desconto.** Sem número no disco, esse toque de SMS vira lembrete de urgência ("ultima chance de garantir hoje") sem valor, e a pergunta do desconto vai pro handoff. Preço inventado reprova.

---

## Seção 4 · WhatsApp (a conversa com botões)

Mensagem de corpo médio, com botão de aceitar e botão de recusar, e footer que oferece cancelar. Cada botão respeita o teto de caracteres da ferramenta (em geral 20 a 25). **O core são as 2 a 3 primeiras mensagens.** As demais só entram se as primeiras performarem; diga isso em 1 linha ao dono.

### Cadência

| Toque | Timer | Função | Botão aceitar / recusar |
|---|---|---|---|
| W1 | 15 min após o evento | reconhecimento + reduzir atrito | "Quero concluir" / "Agora não" |
| W2 | 48 h | benefício (os bullets do que desbloqueia) | "Quero garantir" / "Agora não" |
| W3 | 48 h | desconto ou última condição (SÓ se o dono deu) | "Quero a condição" / "Agora não" |
| W4 | 48 h | última chamada, com respeito | "Quero garantir" / "Pode encerrar" |

### Molde do core (W1)

> Olá [NOME], tudo bem? Aqui é [NOME DO DONO], do [PRODUTO]. Vi que você chegou pertinho de concluir. Se ficou alguma dúvida sobre o [PRODUTO] e os bônus, eu te ajudo por aqui. Pra facilitar, deixo o link de onde você parou. [Garantia e segurança do checkout, se o dono confirmou.]
>
> Botão: `Quero concluir` · `Agora não`
> Footer: Respeitamos sua decisão. É só pedir pra encerrar as mensagens.

**W1 traz o link de retomada e a oferta de ajuda, não a venda inteira.** A pessoa já viu a oferta; aqui você tira o atrito e abre a conversa.

**O desconto de W3 é do dono.** As fontes deste tema fazem o preço cair a cada mensagem. Isso é tática: o valor, o preço de virada e o piso só entram com o número do dono, e a queda vai declarada no handoff. Sem desconto, W3 vira uma nova prova ou um novo benefício, e você diz isso em 1 linha.

**Segurança e garantia no rodapé** entram só quando o dono confirma o prazo de garantia e as formas de pagamento reais. Nada de "seus dados 100% protegidos" sem o dono ter isso no checkout.

---

## Seção 5 · A régua rodando junto (o quadro de um gatilho)

Exemplo de como os 3 canais se cruzam num Pix gerado (timers a partir do evento):

| Tempo | Canal | Toque | Função |
|---|---|---|---|
| 5 min | SMS | S1 | urgência (Pix vence) |
| 10 min | E-mail | E0 | neutro |
| 15 min | WhatsApp | W1 | reconhecimento |
| 40 min | SMS | S2 | urgência |
| 1 h | E-mail | E1 | reconhecimento |
| 4 h | E-mail | E2 | prova |
| 12 h | E-mail | E3 | benefício |
| 24 h | E-mail | E4 | dor |
| 48 h | E-mail + WhatsApp | E5 + W2 | dor perigosa / benefício |
| 72 h | E-mail | E6 | objeção / FAQ |

O dono liga os canais que usa. A régua sai completa; ele desativa o que não tem.
