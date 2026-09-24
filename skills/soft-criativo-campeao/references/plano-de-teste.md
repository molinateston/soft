# Plano de teste mínimo (Ação 0, passo final)

Este reference monta o `plano-de-teste.md` que fecha a tarefa de anunciar: quanto
gastar pra testar, em que fases, o que mata um criativo cedo e quando escalar. É o
MÍNIMO pra o dono pôr o lote no ar sem queimar caixa. O plano de mídia completo e
a operação na conta são da soft-trafego-meta; sem ela, este plano basta pra fazer
à mão.

**Toda régua daqui é ponto de partida**, relatada por operadores de resposta
direta no Brasil, sem auditoria. No plano, cada régua sai com a nota: `régua de
partida; depois de 7 dias rodando, vale o seu próprio recorde`. Número do dono
sempre ganha da régua.

---

## 1. O que fazer sem resposta

As perguntas são as da Ação 0 do SKILL.md, na mesma triagem; este reference não
abre pergunta nova. Aqui fica só o que fazer quando a resposta não veio:

- **Sem ticket:** conta aberta (`verba por corpo = 1 ticket`) com o valor em
  `[A CONFIRMAR: ticket]`.
- **Sem caixa de teste:** a conta sai por corpo, e o total fica
  `[A CONFIRMAR: caixa de teste]`.
- **Sem conta:** `Conta: [A CONFIRMAR: nova ou com histórico]` e os dois ramos
  da seção 3 escritos.

Nunca invente o ticket, o caixa nem a idade da conta.

---

## 2. Verba de teste pelo ticket

- **Objetivo de venda, no gerenciador de anúncios:** cada corpo recebe o valor de
  1 ticket do produto, espalhado em 2 a 5 dias. Com caixa curto, 50% do ticket por
  corpo. Verba abaixo disso não gera venda suficiente pra decidir, e o teste vira
  sorteio. Piso: 30 reais por dia por conjunto.
- **No lote de imagem, corpo = ângulo:** cada peça do manifesto é um corpo, e o
  2º gancho do conjunto é uma variação do `gancho` ou do `texto_anuncio` da mesma
  peça, gravada no manifesto como entrada própria (`peca-01b`). C é o número de
  peças do manifesto, nunca 5 por padrão.
- **Conta a colar no plano:** `ticket <T> · corpos <C> · verba de teste = T x C
  (ou 0,5 x T x C com caixa curto) · dias <D> · por dia por corpo = verba ÷ C ÷ D`.
  Se o valor por dia ficar abaixo do piso: encurte os dias (mínimo 2); se ainda
  ficar abaixo, a verba por corpo sobe pra piso x dias (acima de 1 ticket) e, pra
  caber no caixa, corte corpos (mínimo 2) ou rode um corpo por vez. Diga em 1
  linha que o piso mandou na conta.
- **Ticket alto demais pra essa conta** (1 ticket por corpo passa do caixa mesmo
  com 2 corpos): teste pelo evento anterior à venda (início de checkout,
  agendamento) e diga em 1 linha que trocou a régua.
- **Destino gratuito (isca, aula, cadastro):** o teste mede custo por cadastro.
  Piso de 30 reais por dia por conjunto, janela de 3 dias, e o custo por cadastro
  julgado contra o valor que o dono aceita pagar por lead (pergunte; sem resposta,
  `[A CONFIRMAR: custo por lead aceito]`).
- **Botão de impulsionar do post:** a régua é outra (a da soft-trafego-meta);
  este plano vale pro gerenciador.

---

## 3. As 3 fases e a estrutura de cada uma

| Fase | A pergunta | Verba | Duração | Passa quando |
|---|---|---|---|---|
| Teste | a mensagem vende? | 1 ticket por corpo (seção 2) | 2 a 5 dias, nunca julgar antes de 3 | sai venda, ou o sinal verde precoce da seção 4; ROI não é exigido |
| Pré-escala | vende com lucro quando a verba sobe? | 2x a 3x a verba do teste | ciclo de 3 a 5 dias | o critério de validado (3 a 4 vendas no CPA esperado) e o lucro do funil acima da meta do dono |
| Escala | até onde aguenta? | degraus (seção 5) | contínua | o lucro absoluto do mês segue crescendo |

Nunca pule da fase de teste pra escala. Criativo que passou no teste ainda não
validou a oferta; quem valida a oferta é a pré-escala.

**Estrutura pela fase (regra condicional):**

- **Se é teste:** um conjunto por corpo, com os 2 a 3 ganchos daquele corpo
  dentro, orçamento no conjunto. Assim a plataforma não concentra o gasto num
  anúncio só e deixa os outros sem avaliação. Lote padrão: 5 corpos x 2 a 3
  ganchos, 10 a 15 anúncios, só no lote de vídeo; no de imagem, C é o número de
  peças (seção 2).
- **Se é escala:** consolide os validados em poucos conjuntos, porque fragmentar
  divide o sinal.

**Se a conta é nova** (menos de 15 dias rodando): rode a fase de teste mesmo com
criativo que já validou em outra conta, e só depois replique a estrutura de
escala. Caixa sobrando não acelera essa fase.

---

## 4. Métricas pra matar cedo (régua de partida)

A régua de custo por seguidor mede atração. Pro criativo de conversão, as
métricas abaixo descartam antes de queimar a verba de teste inteira.

| Métrica | Vale pra | Como calcula | Régua de partida | O que fazer |
|---|---|---|---|---|
| Hook rate (só vídeo) | vídeo | visualização de 3 s ÷ impressões | abaixo de 50% fraco; 55% a 60% bom; 70% ou mais top | abaixo: reescreva os 3 a 5 s ou o hook visual. Acima de 70% com conversão baixa: o gancho pode estar atraindo curioso |
| Hold rate (só vídeo) | vídeo | visualização de 75% ÷ impressões | abaixo de 8% descarta | corpo ou edição (playbook, seção 6) |
| CTR de link | imagem e vídeo | cliques no link ÷ impressões | abaixo de 3,5% depois de 2 dias sem venda mata o criativo | troque o criativo, não a página |
| Custo de início de checkout | imagem e vídeo | verba ÷ inícios de checkout | 10% a 20% do ticket | acima: criativo trazendo gente errada ou página fraca |
| Primeira venda | imagem e vídeo | gasto até a 1ª venda | sai gastando até 40% do CPA-alvo | sinal verde precoce: siga pra pré-escala quando fechar a janela |

No lote de imagem, a tabela do plano leva só as linhas `imagem e vídeo`.

**Árvore curta de leitura:**

- Clique bom e venda zero: olhe a página e a oferta antes de trocar o criativo;
  o plano abre com a ordem do conserto e o teste das peças novas começa depois
  dele, medindo visualização da página ÷ clique e início de checkout.
- Hook rate alto e venda zero: o corpo sai, o gancho vai pro banco de ativos e é
  empilhado noutro corpo.
- Verba pequena por dia: o retorno sobre anúncio engana (uma venda isolada mostra
  retorno 2 que não se repete). Decida pelo custo do evento anterior à venda.
  Criativo com retenção muito abaixo dos outros e nenhum início de checkout pode
  sair antes dos 3 dias.
- Destino VSL: leia a retenção do 1º minuto da VSL separada por criativo de
  origem; a queda ali aponta ponte fraca entre anúncio e lead.

---

## 5. Quando escalar e até onde

- **Só validado vai pra escala** (critério: playbook, seção 7).
- **Vertical primeiro:** mais verba na mesma campanha, em degraus. Com a
  soft-trafego-meta instalada, siga a régua de salto dela; sem ela, suba de 20% a
  30% por vez, com 2 a 3 dias entre um degrau e outro, sempre de um dia pro outro
  e nunca no meio do dia.
- **Horizontal quando o degrau quebrar o custo duas vezes:** uma campanha nova por
  criativo validado, cada uma com verba pequena. Nunca duplique a mesma campanha:
  a cópia disputa o próprio leilão.
- **O teto é o lucro absoluto.** Escalar sempre baixa a margem, porque a verba
  nova alcança gente menos consciente. Enquanto o lucro absoluto do mês cresce,
  siga. No degrau em que ele cai em relação ao anterior, volte ao orçamento
  anterior, deixe estabilizar 2 a 3 dias e escale por outro criativo ou pelo
  caminho horizontal.

---

## 6. Quem sobe o plano

- **soft-trafego-meta instalada:** o plano vira o handoff dela, com as peças, o
  UTM padrão e a fase. Ela cria tudo PAUSADO e pede o OK do dono antes de ativar.
- **Sem ela:** o plano sai com o passo a passo à mão (seção 8).
- **Sem terminal nem conector:** igual, o dono executa.

---

## 7. Reprovação sem contorno

- Anúncio reprovado: desative, nunca exclua. Suba no lugar uma versão com a
  promessa em forma aberta e peça revisão do reprovado.
- Anote cada reprovação numa planilha com a hipótese da frase ou imagem que
  causou; em poucas semanas o dono sabe onde a copy dele esbarra.
- Nunca troque a página de destino de um anúncio já aprovado por outra coisa:
  suba anúncio novo.
- A agressividade de copy mora depois do clique, dentro da lei e da verdade; o
  anúncio fica dentro da política, porque a revisão aperta conforme a verba sobe.
  A página também passa pela revisão da plataforma e segue a mesma política.
- Fora sempre: compra de conta, cloaker, contorno da revisão, prática black e
  promessa que a política proíbe.

---

## 8. A forma do `plano-de-teste.md`

```
# Plano de teste: <produto>

Ticket: <valor ou [A CONFIRMAR: ticket]> · Caixa de teste: <valor> · Destino: <qual> · Conta: <nova/histórico>
Tipo de peça: teste em <imagem/vídeo> · escala em <imagem/vídeo> · porquê: <1 linha>

## Verba de teste
<a conta da seção 2, com os números>

## Fases
<a tabela da seção 3, com a verba e os dias do dono>

## Estrutura
Teste: <N> conjuntos, 1 por corpo, <n> ganchos em cada · Escala: <como consolida>

## Quando matar cedo
<a tabela da seção 4, com a nota: régua de partida; depois de 7 dias rodando, vale o seu próprio recorde>

## Quando escalar
<os degraus e o teto da seção 5>

## Quem sobe
<soft-trafego-meta, ou o passo a passo à mão abaixo>
```

**Passo a passo à mão (sem a soft-trafego-meta):**

1. No gerenciador de anúncios, crie a campanha com objetivo Vendas (ou Cadastros,
   no destino gratuito), e deixe PAUSADA.
2. Um conjunto por corpo, orçamento no conjunto igual à verba por dia por corpo
   da seção 2. Público amplo no país e na faixa de idade do avatar.
3. Dentro de cada conjunto, um anúncio por gancho, nomeado em sequência (V1, V2,
   V3), com o texto e o título do anúncio do manifesto.
4. Em cada anúncio, o destino com o UTM padrão da skill e o evento de conversão
   confirmado pelo dono.
5. Confira a prévia no celular, e ative só com o OK do dono.
6. Anote as métricas da seção 4 uma vez por dia, de um dia pro outro, e decida
   pela tabela.

**Conferência do plano (entra no gate):** ticket preenchido ou marcado · conta
da verba aberta com os números · as 3 fases · a estrutura pela fase · a régua de
corte com a nota dos 7 dias · a linha de quem sobe. Cole `plano de teste: 6 de 6
blocos`.
