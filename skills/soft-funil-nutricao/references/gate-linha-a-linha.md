# Gate linha a linha (P6)

O que este arquivo resolve: o critério exato de cada check do gate, o que faz passar e o que faz reprovar, com exemplo ruim e exemplo bom. O gate roda **por dentro**, em cada mensagem (assunto e corpo), e a tabela **nunca** vai pra saída.

Duas leis do gate:
1. **O veredito é o PIOR item.** Um ✗ qualquer reprova a mensagem.
2. **Um ✗ refaz a MENSAGEM, não a régua.** Você conserta o toque que falhou e re-roda o gate nele. Não joga fora a sequência inteira.

Ordem de execução: os 3 checks próprios primeiro (são os que mais reprovam), depois os herdados, e o anti-IA por último, porque ele é mecânico.

---

## Parte 1 · Os 3 checks próprios da nutrição

### 1. UM destino

**Passa se:** a régua inteira empurra pra um único destino declarado no bloco de abertura, e toda mensagem que carrega link carrega o mesmo destino.

**Reprova se:** duas mensagens da mesma régua apontam pra lugares diferentes, ou uma mensagem oferece duas saídas ("clica aqui pra ver a aula, ou me chama no direct pra conversar").

❌ Toque 4 manda pro webinar, toque 5 manda pra call.
✅ Todos os toques com link mandam pra call. O webinar, se existir, é outra régua, com outra entrada.

**Por que importa:** dois destinos dividem o clique e não fecham nenhum dos dois. O lead que precisa escolher entre duas ações não faz nenhuma.

### 2. Referencia o ativo

**Passa se:** a mensagem cita, pelo nome, a isca que **aquele lead** consumiu, ou o sinal específico que ele deu.

**Reprova se:** a mensagem serviria, sem trocar uma palavra, pra qualquer lista de qualquer nicho.

❌ "Espero que o material tenha sido útil. Hoje quero falar sobre um erro comum."
✅ "Você baixou o Checklist dos 12 Pontos. O item 4 é o que mais aparece nas agendas que eu olho, e é sobre ele que eu quero falar hoje."

**Teste rápido:** cubra o nome do dono e o nicho. Se a mensagem continua fazendo sentido pra qualquer negócio, ela reprova.

### 3. Frequência declarada

**Passa se:** o bloco de abertura da entrega traz a cadência escrita (quantos toques, em quantos dias, com que espaçamento) e a régua cumpre exatamente isso.

**Reprova se:** a cadência não está escrita, ou a régua entregue tem mais/menos toques do que o bloco declara.

❌ Bloco diz "6 toques em 7 dias" e a régua tem 8 mensagens.
✅ Bloco diz "6 toques em 7 dias: D+0, D+1, D+2, D+4, D+5, D+7" e as 6 mensagens estão lá, nesses dias.

**Por que importa:** cadência não declarada é lista queimada, porque ninguém consegue auditar, reproduzir, nem detectar quando o volume subiu.

---

## Parte 2 · Os checks herdados (binários)

### 4. Um trabalho só

**Passa se:** a mensagem faz UMA coisa. Entrega, ou pergunta, ou instala crença, ou prova, ou convida.

❌ Uma mensagem que entrega o link, explica o mecanismo, mostra um caso e convida pra call.
✅ Quatro mensagens, uma pra cada.

### 5. Temperatura certa

**Passa se:** o conteúdo da mensagem bate com o estado do lead que vai recebê-la.

❌ Mensagem de quebra de objeção de preço indo pro lead frio que baixou a isca ontem.
✅ Objeção de preço só na rota quente, pra quem já viu o preço.

### 6. Canal certo

**Passa se:** o formato respeita o canal. WhatsApp de 50 a 150 palavras, até 5 linhas, conclusão no topo. E-mail de 200 a 400, com assunto que abre loop.

❌ E-mail de 350 palavras colado no WhatsApp.
✅ A versão de WhatsApp reescrita, com a conclusão na primeira linha.

Marca obrigatória no WhatsApp: `[TEMPLATE]` fora da janela de 24h, `[livre]` dentro.

### 7. Não vende, aquece

**Passa se:** a mensagem move o lead um degrau, sem tentar fechar. O fechamento é do destino.

❌ "Últimas vagas do programa, garanta a sua por 12x de X."
✅ "Se quiser, eu olho a sua agenda de uma semana e te digo onde está o dinheiro parado."

Exceção única: quando o destino declarado é oferta direta, o último toque pode carregar o link do checkout. Ainda assim, a régua não é a página de vendas.

### 8. Ancorada

**Passa se:** a mensagem nasce de fala literal do lead (com o N de quantas vezes apareceu) ou de prova real do dono.

**Reprova automaticamente se:** tem número, caso ou fala que soa plausível e não veio da fonte.

❌ "Como muitos clientes me dizem, o dia não rende."
✅ "Uma frase que apareceu 7 vezes nas conversas: 'atendo o dia inteiro e não sobra nada'."

### 9. Insumo faltante marcado

**Passa se:** todo furo aparece como `[A CONFIRMAR: o quê]`, no lugar exato onde falta, visível.

❌ Deixou o link do destino em branco e seguiu.
✅ `[A CONFIRMAR: link da agenda]` na linha do CTA.

Grafia única em toda a entrega: `[A CONFIRMAR: o quê]`. Duas grafias diferentes no mesmo arquivo reprovam por inconsistência.

### 10. C/U/B

**Passa se:**
- não é **C**onfuso: entende em uma leitura, uma ideia por frase
- não é **I**nacreditável: a promessa tem o tamanho da prova que está do lado
- não é **B**oring: tem tensão ou cena real, não é morno nem motivacional

❌ "Otimize seus processos para alcançar resultados extraordinários."
✅ "O melhor horário da sua agenda está indo pro procedimento mais barato."

### 11. CTA com destino

**Passa se:** a ação é clara e o destino existe e está nomeado.

❌ "Saiba mais."
✅ "[link da agenda] escolhe um horário de 30 minutos."

Mensagem sem CTA passa, quando o trabalho dela não é mover (o toque de crença, por exemplo). O que reprova é o CTA vago.

### 12. Anti-IA (mecânico, HARD)

**Passa se:** zero travessão longo (U+2014), zero da família do verbo-freio banida pela régua anti-voz (o verbo que rima com "cravar" e todas as flexões dele, incluindo o particípio e os derivados de "des-"), zero frase-emoldura ("a verdade é", "o segredo é"), zero verbo-clichê de hype.

Exceção única: aspa literal do cliente. Se ele falou assim, fica, entre aspas, marcado como fala dele.

**Como conferir:** com shell disponível, roda o lint de copy em `scripts/lint_copy.py` sobre o arquivo de entrega. Sem shell, faz a busca manual pelos dois bloqueios duros: o travessão longo e a família do verbo banido. O detalhe dos padrões está em `shared-references/filtro-anti-ia/padroes-banidos.md`, e o que NÃO corrigir em `shared-references/filtro-anti-ia/falsos-positivos.md`.

---

## Parte 3 · O checklist de subida (roda uma vez, na régua inteira)

Não é por mensagem, é por régua. Vai junto da entrega, no fim do arquivo.

| Item | Passa se |
|---|---|
| **Filtro de cliente** | existe a condição "já comprou?" na entrada, e ela remove o cliente de toda régua de aquisição |
| **Tags de temperatura** | os sinais de subida e descida estão escritos, e cada um aponta pra onde o lead vai |
| **Saída da régua** | existe corte declarado (quem não reagiu até o dia N sai) e existe o jeito de o lead pedir pra parar |
| **Higiene** | quem não abre há 90 dias sai da lista ativa |
| **Colisão** | a régua não bate em cima de outra régua ou broadcast no mesmo dia |
| **Link com rastreio** | os links do destino carregam o parâmetro de origem, pra medir qual toque converte |
| **Teste de disparo** | a régua foi disparada pra um contato de teste antes de subir, e chegou como devia |
| **Conformidade do WhatsApp** | opt-in real registrado, template aprovado pra fora da janela de 24h, API oficial |

---

## Parte 4 · Anti-patterns que o gate pega

| Sintoma | O check que reprova | Correção |
|---|---|---|
| Régua manda pro webinar e pra call | UM destino | escolhe um. O outro vira outra régua |
| "Espero que o material tenha sido útil" | Referencia o ativo | cita a isca pelo nome e o item específico |
| Entrega escrita sem cadência no topo | Frequência declarada | escreve o bloco de abertura antes de tudo |
| Mensagem que entrega, prova e convida | Um trabalho só | quebra em três |
| Objeção de preço no lead que baixou ontem | Temperatura certa | move pra rota quente |
| E-mail longo colado no WhatsApp | Canal certo | reescreve com a conclusão no topo |
| "Últimas vagas" numa régua de aquecimento | Não vende, aquece | tira. Quem vende é o destino |
| Número que soa plausível | Ancorada | `[A CONFIRMAR: número]` ou tira |
| Duas grafias de marcação de furo | Insumo marcado | padroniza em `[A CONFIRMAR: o quê]` |
| "Saiba mais" | CTA com destino | link nomeado e ação concreta |
| Travessão longo em qualquer lugar | Anti-IA | ponto ou vírgula |
| Régua sem fim, o lead nunca sai | Checklist de subida | corte declarado em dia fixo |
| Régua entregue com a tabela do gate colada | (processo) | o gate é interno. A saída é só a régua limpa |
