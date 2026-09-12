# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, números, preços, falas e resultados foram inventados só pra
> mostrar a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega
> de verdade. Num trabalho real, todo número e toda prova sem fonte nascem marcados `[A CONFIRMAR]`
> e o dono confirma antes de sair.

**O caso fictício:** consultoria de organização financeira pra clínicas de pequeno porte. A dona
fictícia atende clínicas de 3 a 15 funcionários. O público são donos de clínica que faturam bem e
mesmo assim terminam o mês no vermelho. Ela vende uma sessão de diagnóstico paga e, a partir dela,
um programa de 8 semanas por R$ 4.900, acima do limiar de ticket.

**O pedido que o dono deu, literal:** *"tenho 40 mensagens paradas no WhatsApp e não dou conta.
Queria um agente que responde, entende se a pessoa serve, e marca o diagnóstico comigo."*

Este arquivo mostra a saída RESUMIDA de cada ação, na ordem. A saída real é bem maior; aqui está o
suficiente pra reconhecer o formato antes de começar.

---

## Ação 1 · OBJETIVO

**A pergunta que a skill fez:** *"o agente precisa AGENDAR reunião, RESPONDER dúvida ou EMPURRAR o
lead pela esteira?"*
**Resposta dela:** *"agendar. Responder dúvida eu até queria, mas o problema é a agenda vazia."*

Saída no `01-operacao-agente.md`:

| Campo | Cravado |
|---|---|
| Missão | **A. SDR clássico** |
| Desfecho-alvo | sessão de diagnóstico agendada, com nota rica pra ela abrir a call já sabendo o caso |
| Métrica-mãe | leads → qualificados → agendados → show rate |
| Faixa de referência | inbound qualificado que vira reunião, mediana ~62%; show rate 75% a 85% |
| Número de partida dela | `[A CONFIRMAR]`, ela nunca mediu |

**STOP.** Ela aprovou.

---

## Ação 2 · ONBOARDING

**As 6 perguntas, uma por vez.** As respostas que mudaram o agente:

- **Voz:** ela mandou 3 mensagens reais. Padrão: começa pelo problema, sem "olá, tudo bem?", usa
  "a gente" e chama a cliente pelo primeiro nome. Frases de 1 linha.
- **Oferta:** sessão de diagnóstico de 90 minutos por R$ 400, e o programa de 8 semanas por R$ 4.900.
- **FAQ:** 10 páginas curtas escritas, entre elas "preciso de contador?", "e se eu não tiver
  planilha nenhuma?" e "atende clínica de 2 pessoas?".
- **O que o agente NUNCA diz:** que ela garante lucro, que ela resolve problema com a Receita, e
  qualquer valor de parcelamento fora da tabela.
- **Limiar:** R$ 3.000. O programa está acima, então o agente agenda e ela fecha na call.

Saída, o `precos.json` fictício:

```json
{
  "sessao_diagnostico": { "valor": 400, "condicao": "à vista, no Pix ou cartão" },
  "programa_8_semanas": { "valor": 4900, "condicao": "à vista ou 12x de 449", "acima_do_limiar": true }
}
```

**STOP.** Ela aprovou, e pediu pra tirar a palavra "investimento" das mensagens.

---

## Ação 3 · CANAL

Canal escolhido: GHL, que ela já usava pro cadastro. O que a skill fez: pediu o token de integração
privada e o ID da conta, mapeou o pipeline (4 etapas) e os campos, e rodou o teste de ida e volta.

| Teste | Resultado |
|---|---|
| Mensagem de entrada chega no webhook | passou, 1,2s |
| Resposta do agente sai pelo canal | passou |
| Contato criado com tag | passou |
| Slot de agenda lido | passou, 2 horários livres na semana |

**STOP.** Conexão provada antes de qualquer lead real ver o agente.

---

## Ação 4 · MOTOR

Saída, o `02-prompt-agente.md`, no formato do exemplo que está no SKILL.md, com os campos dela
preenchidos: voz sem saudação, os 4 elementos na ordem, dinheiro só do `precos.json`, desfecho na
sessão de diagnóstico, escalada em assunto fiscal.

Um turno real do simulador, pra mostrar a forma:

> **Lead:** *"oi, vi seu story do caixa. quanto custa?"*
> **Agente:** *"Oi Camila. Antes do valor eu preciso entender uma coisa: o que te fez olhar pra isso agora?"*
> **Lead:** *"tô faturando mais que ano passado e não sobra nada, é desesperador"*
> **Agente:** *"Entendi. Isso é pra resolver agora ou você ainda quer tentar por conta mais um pouco?"*
> **Lead:** *"agora. não aguento mais"*
> **Agente:** *"O que você já tentou? O que não funcionou?"*
> **Lead:** *"planilha, contratei um gerente, larguei as duas"*
> **Agente:** *"Isso eu vejo muito. Tenho 2 horários de diagnóstico essa semana, quinta 9h ou sexta 15h. Qual fica melhor?"*

Repare: nenhum valor apareceu, uma pergunta por mensagem, e a sessão foi oferecida como vaga, não
como pedido.

**STOP.** Ela aprovou depois de trocar uma frase.

---

## Ação 5 · GATE

A tabela do SKILL.md foi mostrada pra ela com 2 ajustes que ela pediu:

| Ajuste dela | Virou |
|---|---|
| "não quero que ele fale de imposto nem por acidente" | assunto fiscal entra na lista de escalada dura |
| "pode marcar sozinho, confio" | agendamento em slot livre fica no "faz sozinho" |

Ela tem quem mexa no motor, então as defesas ficaram em código de verdade. Se não tivesse, o
caminho seria o modo rascunho permanente, com ela aprovando cada envio.

**STOP.** Gate assinado.

---

## Ação 6 · SUBIDA E OPERAÇÃO

Replay com 22 conversas reais antigas dela. Saída, o `03-relatorio-subida.md`:

| Caso | O que o agente faria | Veredito |
|---|---|---|
| 14 conversas | mesma condução, agendou nos mesmos casos | passa |
| 5 conversas | agendou onde ela tinha encerrado (lead sem porte) | ajuste: porte da clínica entra na qualificação |
| 2 conversas | escalou certo (dúvida fiscal) | passa |
| 1 conversa | falou "a gente resolve isso" perto demais de promessa | ajuste: frase entra na lista do nunca |

Depois dos 2 ajustes, rodou 6 dias em sombra e subiu pra autônomo. Reporte diário ligado.

**STOP antes do autônomo.** Ela leu o relatório e liberou.

---

## Ação 7 · PEÇA DE TOPO

Pedido separado, semanas depois: *"escreve a mensagem pra quem se inscreveu na aula e não apareceu."*

A skill perguntou as 4: pra quem, o que a pessoa acabou de fazer, qual o próximo passo, e as 3 falas
reais. Ela mandou o verbatim: *"eu esqueci completamente, o dia na clínica me engole"*.

Saída no `04-pecas-de-topo.md`, o toque 1 de 3:

> Camila, você se inscreveu na aula de ontem e não apareceu. Sem problema, o dia na clínica engole
> mesmo.
>
> Gravei o pedaço que interessa pra você: os 12 minutos onde eu mostro por que o dinheiro some
> mesmo com o faturamento subindo.
>
> Quer que eu te mande?

Toque 2 em 24 horas, com a resposta ou sem. Toque 3 em 48 horas, só o nome. Teto de 4 toques, depois
para.

**STOP:** *"ajusto ou pode ir pro lead?"*

---

## O que ficou pendente no caso fictício

- Show rate real dela: `[A CONFIRMAR]`, primeira medição só depois de 30 dias.
- Prova social pra usar no convite da sessão: ela tem 3 casos, nenhum autorizado por escrito ainda.
- Missão B (atendente de dúvida) fica pra depois, com a mesma wiki já carregada.
