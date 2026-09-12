# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, números, preços, falas e resultados foram inventados só pra
> mostrar a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega
> de verdade. Num trabalho real, todo resultado e todo número sem fonte nascem marcados
> `[A CONFIRMAR]` e o dono confirma antes de sair.

**O caso fictício:** consultoria de gestão pra donos de restaurante de bairro. O dono fictício tem
15 clientes de consultoria avulsa, audiência de cerca de 1.200 no perfil com cerca de 250
visualizações qualificadas por story, quer abrir uma mentoria em grupo e nunca lançou nada.

**O pedido que o dono deu, literal:** *"esse mês tá fraco e eu quero abrir a mentoria. Só que eu não
sei se anuncio, se faço live, se mando mensagem. Me diz o que eu faço."*

Este arquivo mostra a saída RESUMIDA de cada ação. A saída real é bem maior; aqui está o suficiente
pra reconhecer o formato.

---

## Ação 1 · DIAGNÓSTICO DO MOMENTO

**As 5 perguntas e as respostas dele:**

| Sinal | Resposta |
|---|---|
| Tem base de clientes ou ex-clientes? | SIM, 15 clientes de consultoria avulsa |
| Tem audiência ativa? | SIM, cerca de 250 visualizações qualificadas por story |
| Tem produto novo pra testar antes de criar? | SIM, a mentoria em grupo, que ainda não existe |
| Vai subir preço, ou tem demanda represada? | Não agora |
| Tem volume de DM cansando o manual? | Não, volume baixo |

**A meta do mês:** ele não sabe. Ficou `[A CONFIRMAR]`, e a skill avisou em 1 linha que a frequência
de cada jogada só fecha quando a meta existir.

**A jogada de menor custo apontada:** Lembrei de Você (#10), porque ele tem 15 clientes quentes
parados e ainda não falou com nenhum sobre a mentoria.

**STOP.** Ele aprovou e perguntou se dava pra fazer tudo na mesma semana. A resposta foi não: a ordem
é o que faz o mês fechar.

---

## Ação 2 · PLANO DO MÊS

Saída, o `01-plano-jogadas.md`:

| Bloco | Preenchido |
|---|---|
| **Momento** | base de 15 clientes · audiência de 250 visualizações qualificadas · produto novo pra validar · sem aumento de preço · DM em volume baixo |
| **Jogada 1, a de menor custo** | **Lembrei de Você** com os 15 clientes. Apresenta a mentoria como evolução natural do que ele já faz com cada um, convite leve. Na voz dele, pelo teto que aquele dono sente: trabalhar 14 horas e não conseguir sair do salão |
| **Jogada 2, o motor de fundo** | **Caixinha** diária, 3 a 5 perguntas com 1 oferta no meio, mais **Levantada de Mão** 2 vezes por semana pra encher o direct |
| **Jogada 3, o pico** | **Reunião de R$ 100** temática sobre a virada que emperra, tema que a caixinha acusou como o mais perguntado. Formato de 20 ou mais pessoas, sem sabatina, com a oferta da mentoria no fim |
| **Ordem no mês** | Lembrei de Você na semana 1 → Caixinha e Levantada em fundo o mês todo → Reunião de R$ 100 na semana 3, o pico → fechamento correndo ao longo do mês |
| **Frequência** | `[A CONFIRMAR]`, fecha quando a meta do mês existir |
| **Handoff comercial** | lead quente da Levantada e da Reunião vai pra **soft-vendas-sdr** abrir e agendar, quando houver volume; **soft-vendas-closer** conduz e fecha. Desenho e preço da mentoria vão pra **soft-plano-ofertas** |

Repare na lógica: começa pela base quente, que é o menor custo, mantém motor diário em fundo, usa
um evento como pico, e aponta cada ponta comercial pra skill certa.

**STOP.** Ele aprovou, e pediu pra trocar a Reunião de R$ 100 de semana.

---

## Ação 3 · JOGADA MONTADA

Ele escolheu montar a Lembrei de Você primeiro.

**As 4 perguntas e as respostas dele:**

1. Qual oferta essa jogada move? A mentoria em grupo, que abre em 30 dias.
2. Por quanto? R$ 4.200, acima do limiar.
3. Pra quem exatamente? Os 15 clientes, começando pelos 6 que já contrataram duas vezes.
4. Me manda 3 falas reais dessa pessoa. Ele mandou: *"eu não consigo sair do salão nem pra ir no
   banco"*, *"todo mês eu acho que vai sobrar e nunca sobra"* e *"meu gerente não decide nada sem mim"*.

Saída, o `02-jogada-montada.md`. O esqueleto na voz dele, mensagem 1 de 3:

> **Mensagem 1, conexão de verdade, sem pitch:**
> "Marcelo, tava olhando aqui o que a gente ajustou no seu salão em março. Aquele negócio da escala
> do almoço ficou de pé ou voltou pro que era?"
>
> [espera a resposta, responde de verdade, e só então:]
>
> **Mensagem 2, a novidade como evolução natural:**
> "Te falo por que eu lembrei de você. Eu vou abrir em 30 dias uma coisa que é o passo seguinte do
> que a gente fez: em vez de eu entrar pontual e sumir, eu fico junto por 6 meses, com um grupo
> pequeno de dono de restaurante que tá exatamente onde você tá. O que eu quero resolver com esse
> grupo é o que você me disse na última: você não consegue sair do salão nem pra ir no banco."
>
> **Mensagem 3, convite leve:**
> "Não é pra todo mundo e nem vou empurrar. Se você quiser entender como funciona, eu te ligo 15
> minutos essa semana. Se não for a hora, sem problema nenhum, a gente segue como tá."

**O ajuste de tom que a jogada exigiu:** o esqueleto padrão dessa jogada engana com "espero que
esteja bem" e "agradeço a confiança", e isso não passa no anti-IA. Foi reescrito pelo teto que aquele
cliente sente, com o verbatim dele na mensagem 2.

**Resultado esperado:** campo do dono, `[A CONFIRMAR]`. Ele nunca rodou isso antes.

**STOP.**

---

## Ação 4 · ESTRATÉGIA DE LANÇAMENTO

**As 3 perguntas:**

1. O que vai lançar? A mentoria em grupo de 6 meses.
2. Quando consegue começar a entregar de verdade? Em 30 dias.
3. Quantas pessoas aguenta no primeiro mês? Umas 6.

Saída, o `03-estrategia-lancamento.md`:

| Decisão | Cravado |
|---|---|
| Data | vende agora, turma começa em 30 dias. Ele não monta a estrutura antes de vender |
| Fundadores | 2, em semanas alternadas: o primeiro na semana 1, o segundo na semana 2, pra ele levar o aprendizado de um pro outro |
| Contrapartida do fundador | condição especial em troca do caso documentado: formulário de saída mais depoimento |
| Critério de consumo | só libera o módulo seguinte quem cumpriu o anterior |
| Teto individual | 6 pessoas. Passou disso, vira desenho de produto e vai pra **soft-plano-ofertas** |
| Porta de entrada | sessão paga única de 90 minutos sobre a escala do salão. Vira mentoria por cashback, pagando a diferença. NÃO dá acesso ao grupo |
| Canal de fechamento | R$ 4.200 está acima do limiar, então a conversa qualifica e agenda a call 1:1, e o fechamento acontece na call |

**STOP.**

---

## Ação 5 · FUNIL DE AQUECIMENTO

Pedido separado, um mês depois: *"quero que o cara já chegue sabendo o que eu faço, cansei de
explicar tudo do zero no WhatsApp"*.

**A pergunta única:** "qual é a pergunta que todo mundo te faz antes de fechar?"
**Resposta dele:** *"todo mundo pergunta se eu vou mexer no cardápio e demitir gente"*.

Saída, o `04-funil-aquecimento.md`:

| Peça | O que é |
|---|---|
| Entrada | reel curto que fisga a dor do dono preso no salão |
| Automação | comentário com a palavra combinada dispara a mensagem com o link |
| Aula | 14 minutos, respondendo a dúvida número 1: o que muda e o que NÃO muda no restaurante quando ele entra |
| Botão | contato só no fim da aula, nunca antes |

Quem chega no canal humano já assistiu e chega quente. A copy do reel vai pras `soft-conteudo-*`, a
condução da conversa vai pra **soft-vendas-closer**.

**STOP.**

---

## O que ficou pendente no caso fictício

- Meta do mês: `[A CONFIRMAR]`, e sem ela a frequência de cada jogada fica em aberto.
- Prova social pra usar na Reunião de R$ 100: ele tem 15 clientes e nenhum caso documentado ainda.
- Preço e formato final da mentoria: vai pra `soft-plano-ofertas` antes da turma abrir.
