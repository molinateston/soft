# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, números, prazos e resultados foram inventados só pra mostrar
> a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega de
> verdade. Num trabalho real, todo número e toda prova sem fonte nascem marcados `[A CONFIRMAR]` e o
> dono confirma antes de sair.

**O caso fictício:** consultoria de organização de agenda pra clínicas pequenas (odontologia,
fisioterapia, estética). A dona fictícia atende clínicas de 2 a 6 salas. A isca dela é o "Checklist
dos 12 Pontos da Agenda", um PDF de 4 páginas que a pessoa lê em 6 minutos. O destino é uma conversa
de 30 minutos. Ticket do programa: `[fictício]` 4.800 reais.

Este arquivo mostra a saída resumida de cada ação, na ordem. A saída real é maior; aqui está só o
suficiente pra você reconhecer o formato antes de começar.

---

## O que o dono deu de entrada

> "Tenho um checklist que umas 400 pessoas baixaram nos últimos meses. Mando o link e acabou. Ninguém
> responde nada depois. Eu queria que essas pessoas chegassem na minha agenda."

**O que faltava:** o destino estava implícito, a temperatura não estava definida, e não havia fala
literal nenhuma anexada.

## As perguntas que a skill fez (uma por vez)

1. "Depois que a pessoa baixa o checklist, pra onde você quer levar ela?" → *"Pra uma conversa minha, de meia hora."*
2. "O que você vende no fim, e por quanto?" → *"Um programa de 8 semanas, 4.800."* `[fictício]`
3. "Qual a frase que essa pessoa fala quando está no pior do problema?" → *"'Atendo o dia inteiro e não sobra nada.' Isso eu ouço direto."*
4. "Que prova real você tem?" → *"Uma clínica de fisioterapia com 3 salas subiu 18% em 6 semanas só mudando a ordem de encaixe."* `[fictício]`
5. "Você fala com essa base por WhatsApp, por e-mail, ou pelos dois?" → *"Tenho e-mail de todo mundo. WhatsApp só de quem me chamou."*

**Premissa declarada em 1 linha:** a base é fria (baixou e sumiu), então a régua sai na rota fria e o
WhatsApp entra só nos toques 2, 5 e 6, e só pros contatos com opt-in vivo.

---

## Ação 1 · RÉGUA PÓS-ISCA

Saída real: `regua-nutricao.md`. Resumo:

### O bloco de configuração (o topo do arquivo)

```
ISCA: Checklist dos 12 Pontos da Agenda · promessa: achar as 12 falhas que fazem a agenda cheia não pagar a conta
CRENÇA-PONTE: agenda cheia e agenda lucrativa não são a mesma agenda
DESTINO: call · link: [A CONFIRMAR: link da agenda]
TEMPERATURA DE ENTRADA: frio
CANAIS: e-mail (todos) + WhatsApp (só opt-in vivo)
CADÊNCIA: 6 toques em 7 dias: D+0, D+1, D+2, D+4, D+5, D+7
FILTRO DE SAÍDA: cliente sai · quem agendou sai · quem respondeu sobe pro 1:1 · sem reação até D+7 vai pro fluxo de base fria
FUROS: [A CONFIRMAR: link da agenda] · [A CONFIRMAR: prova, o caso dos 18% precisa de autorização por escrito]
```

### Os 6 toques (resumidos)

| Dia | Toque | Canal | Trabalho | Como abre |
|---|---|---|---|---|
| D+0 | Entrega | e-mail + WhatsApp | link + instrução de primeiro uso | "Aqui está o Checklist dos 12 Pontos. Abre no item 4." |
| D+1 | Consumo | WhatsApp | pergunta de 1 palavra | "Conseguiu abrir ontem? Me responde só o número do item que mais bateu." |
| D+2 | Crença | e-mail | mecanismo do problema, exonera | "Você já tentou apertar os horários. A conta não mudou." |
| D+4 | Prova | e-mail | o caso, com número e prazo | "Uma clínica com 3 salas mudou só a ordem de encaixe." |
| D+5 | Convite | WhatsApp + e-mail | o destino, com filtro honesto | "Se quiser, eu olho a sua agenda de uma semana." |
| D+7 | Última chamada | WhatsApp | ângulo novo, e o corte | "A dúvida que mais aparece é 'não tenho tempo agora'." |

### Um toque escrito por inteiro (D+2, e-mail)

> **Assunto:** por que a agenda enche e o faturamento não
>
> Você já tentou apertar os horários. Encaixou mais gente no mesmo dia, cortou o intervalo do almoço,
> atendeu mais cedo. Fez a conta no fim do mês e o número quase não mexeu.
>
> Não é falta de esforço. É que a agenda cheia e a agenda lucrativa não são a mesma agenda.
>
> Quando o encaixe segue a ordem de quem ligou primeiro, o horário de maior movimento vai pro
> procedimento mais rápido e mais barato, porque é o que mais gente pede. O de maior valor sobra pro
> fim da tarde, quando a taxa de falta é maior.
>
> O inimigo não é o volume. É a ordem de encaixe.
>
> Amanhã eu te mostro o que acontece quando uma clínica muda só isso, sem contratar ninguém e sem
> mexer no preço.

**Por que este toque passou no gate:** cita a isca por dentro (o item 4 do checklist foi o gancho do
toque 1 e volta aqui), ancora na fala literal *"atendo o dia inteiro e não sobra nada"* reescrita em
cena, exonera o lead em vez de culpar, faz UM trabalho só (crença), e fecha no gancho do próximo
toque sem pedir nada.

### O checklist de subida (o rodapé do arquivo)

```
[ ] filtro "já comprou?" na entrada, removendo cliente de toda régua
[ ] tags: respondeu → 1:1 · clicou no destino → morno · sem reação D+7 → base fria
[ ] saída declarada: "me responde 'para' que eu tiro", executada no mesmo dia
[ ] higiene: quem não abre há 90 dias sai da lista ativa
[ ] colisão: nenhum broadcast agendado nesses 7 dias
[ ] links com parâmetro de origem, pra medir qual toque converte
[ ] disparo de teste feito pra um contato próprio antes de subir
[ ] WhatsApp: opt-in registrado, [TEMPLATE] nos toques fora da janela de 24h, API oficial
```

**STOP.** A skill mostrou isso, perguntou "te serve? ajusto, ou sigo?", e esperou.

---

## Ação 2 · ROTAS POR TEMPERATURA

Saída real: `rotas-temperatura.md`. O dono respondeu que a ferramenta dele registra abertura, clique
e resposta. Resumo da ramificação entregue:

```
ENTRADA: baixou o Checklist dos 12 Pontos
  └─ já é cliente? → SAI
  └─ TRILHA FRIA (os 6 toques acima)
       ├─ respondeu OU clicou → pula pra TRILHA MORNA
       ├─ perguntou preço ou "como funciona" → SAI da automação, vai pro 1:1
       └─ D+7 sem reagir → SAI pro fluxo de base fria

  TRILHA MORNA (3 toques em 4 dias)
       1. reconhece o sinal + mecanismo da solução nomeado
       2. prova no mesmo recorte do sinal que ele deu
       3. convite direto, com o link
       ├─ respondeu → SAI pro 1:1
       └─ terminou sem reagir → base fria

  TRILHA QUENTE (manual, 1:1, prioridade máxima)
       1. reconhece sem cobrar + UMA objeção nomeada
       2. prova que ataca aquela objeção
       3. pergunta de sim ou não
       4. "me responde uma palavra: preço, tempo ou confiança?"
       5. corte honesto
```

**Uma mensagem da trilha quente (toque 4, WhatsApp):**

> A gente conversou há duas semanas e você ficou de ver a agenda com calma. Sem pressa mesmo.
>
> Só pra eu parar de te chamar no escuro: me responde uma palavra. **Preço**, **tempo** ou
> **confiança**? Eu te mando a resposta pra essa e paro por aí.

**STOP** por rota.

---

## Ação 3 · REATIVAÇÃO

O dono lembrou que tinha 900 contatos de uma isca antiga, parados há 8 meses. Saída real:
`reativacao.md`. Resumo dos 4 toques em 10 dias:

| Dia | Toque | O trabalho |
|---|---|---|
| D+0 | A pergunta | "Hoje, o que mais atrapalha a sua agenda: falta, encaixe ou preço? Me responde só a palavra." |
| D+3 | A utilidade | entrega uma coisa útil sobre a resposta mais comum, sem pedir nada |
| D+6 | O convite | a conversa de 30 minutos, curta, com filtro honesto |
| D+10 | O corte | "Eu vou parar de te escrever. Se ainda quiser receber, me responde qualquer coisa." |

**Regra de higiene registrada na entrega:** dispara primeiro pros 300 mais recentes (pararam há 60 a
120 dias), mede a resposta, e só então avança pros 600 restantes. Quem não reagiu até D+10 é removido
da lista ativa.

---

## Ação 4 · BROADCAST

Duas semanas depois o dono pediu: *"abri uma sessão ao vivo na quinta, avisa todo mundo."*

**As 4 checagens rodaram antes de escrever:**
1. Motivo real? Sim, sessão ao vivo com data e 20 lugares. `[fictício]`
2. Filtro de cliente? Os 11 clientes ativos saíram do recorte.
3. Colisão? 34 contatos estavam no meio da régua pós-isca. Foram excluídos deste disparo.
4. Recorte? Só quem consumiu o checklist nos últimos 90 dias, não a base inteira.

**A mensagem (WhatsApp, 4 linhas):**

> Abri uma sessão nova na quinta, 19h, sobre encaixe de agenda. São 20 lugares porque é ao vivo e eu
> respondo pergunta.
>
> Se a sua agenda enche e o faturamento não acompanha, é essa a conversa.
>
> [link]
>
> Se não for o seu momento, ignora essa que na semana que vem eu não te chateio.

---

## O que o gate reprovou pelo caminho (e por quê)

| Mensagem que caiu | Check que reprovou | O que foi feito |
|---|---|---|
| Primeira versão do D+0, só o link | (molde) | reescrita com instrução de primeiro uso e gancho do próximo |
| Primeira versão do D+1, "o que achou do material?" | C/U/B, era boring e pedia esforço | virou pergunta de 1 palavra |
| Primeira versão do D+4, "vários clientes melhoraram muito" | Ancorada | trocada pelo caso com número e prazo, marcado `[A CONFIRMAR: prova]` |
| Primeira versão do D+7, "últimas vagas" | Não vende, aquece + urgência fabricada | virou ângulo novo sobre a objeção de tempo |
| Um toque extra em D+3 que o rascunho tinha | Frequência declarada | cortado, porque o bloco de configuração dizia 6 toques |
