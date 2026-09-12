# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nicho, pilares, falas, links, datas e temas quentes foram
> inventados só pra mostrar a FORMA da entrega. Nada disso é caso real, nada disso pode ser copiado
> pra um trabalho de verdade. Num radar real, nenhum item entra sem data verificada numa página que
> você abriu, e todo furo sai marcado `[A CONFIRMAR]`.

**O caso fictício:** uma veterinária que atende tutor de cachorro idoso (8 anos ou mais) em consulta
domiciliar. Público: dono que já ouviu "é da idade" e não aceitou. Mecanismo dela (fictício):
**Rotina dos 4 Sinais**, a checagem semanal em casa que antecipa a consulta em vez de reagir a ela.

Este arquivo mostra as DUAS ações, na ordem em que ela pediu: a matriz do mês (Ação 1) e, três
semanas depois, o radar da semana (Ação 2).

---

# Ação 1 · MATRIZ

## O que o dono deu de entrada

> "não sei o que postar, me ajuda a planejar o mês"

Pedido de mês, cadência mensal, entra na Ação 1.

## As perguntas que a skill fez

O perfil do agente tinha o nicho e a tese dela, mas os pilares nunca foram nomeados. Segundo estado
de entrada: a skill **propôs** 3 pilares e **parou** pra confirmar, em vez de tratar proposta como
fato.

> "Não achei os teus pilares nomeados em lugar nenhum, então eu proponho 3 e você confirma antes de
> eu montar a matriz:
> 1. **Rotina dos 4 Sinais** (Método): a checagem semanal em casa.
> 2. **O que 'é da idade' esconde** (Tese): a postura contra o diagnóstico preguiçoso.
> 3. **Consulta em casa** (Bastidor): o que eu vejo na casa que não aparece no consultório.
> Serve, ou você tira ou troca algum?"

A veterinária confirmou os 3 e acrescentou um quarto: **Fim de vida com dignidade** (Diagnóstico).
Quatro pilares × 8 formatos = 32 pautas.

Verbatim que veio do perfil:

- Dor literal (N=8): "me falaram que é da idade e eu aceitei".
- Dor literal (N=5): "ele parou de subir no sofá e eu só percebi meses depois".
- Desejo literal (N=4): "eu queria ter percebido antes".

## A matriz entregue (recorte de 2 pilares × 4 formatos, pra calibrar)

Saída real: `matriz-conteudo-2026-09-04.md`, com as 32 células. Aqui, 8 delas:

| Pilar ↓ / Formato → | Acionável | Diagnóstico | Contrário | Antes vs Depois |
|---|---|---|---|---|
| **Rotina dos 4 Sinais** | Os 4 sinais que você checa em casa no domingo, em 6 minutos. | O tutor que só percebe a dor do cachorro quando ele já parou de fazer o que gostava. | Cachorro idoso não precisa de mais exame. Precisa de mais observação. | Do "ele está velhinho" ao "ele tem artrose no cotovelo esquerdo". |
| **O que "é da idade" esconde** | O que perguntar ao veterinário quando ele disser que é da idade. | O tutor que aceitou "é da idade" e voltou 8 meses depois com um caso que dobrou de tamanho. | "É da idade" quase nunca é diagnóstico. É o fim da conversa. | Do sofá abandonado por meses ao cachorro subindo sozinho de novo. |

**As 3 pautas mais fortes desta matriz:**
1. "O tutor que aceitou 'é da idade' e voltou 8 meses depois", porque nasce intacta do verbatim de N=8.
2. "Ele parou de subir no sofá e eu só percebi meses depois", porque é a cena que o tutor reconhece.
3. "Os 4 sinais que você checa no domingo em 6 minutos", porque é a única que já vira peça sem mais insumo.

**Pilar mais raso: Fim de vida com dignidade.** As células saíram sem cena, porque não há verbatim
sobre esse momento no perfil. `[A CONFIRMAR]` em 3 células. Pedir 2 relatos concretos resolve.

**STOP.** "Quais pautas te servem? Quer que eu escreva a headline de alguma (passo pra
soft-conteudo-headlines) ou gero mais numa linha?"

---

# Ação 2 · RADAR (três semanas depois, outro pedido)

## O que o dono deu de entrada

> "tem alguma coisa rolando no meu nicho essa semana?"

Pedido de semana, cadência semanal, entra na Ação 2. Janela default: 7 dias.

## A honestidade de tooling, declarada antes de qualquer varredura

O ambiente daquela sessão não tinha acesso à web. A skill não fingiu varredura:

> "Nesse ambiente eu não consigo varrer a web ao vivo, então a gente faz assim: me cola o que você já
> viu quente essa semana (prints, links, o que os colegas postaram) e eu organizo com o ângulo. A
> varredura ao vivo, com verificação de data item a item, roda em ambiente com acesso à web."

A veterinária colou 9 itens. Três não tinham data visível e **caíram**, sem exceção. Dos 6 restantes,
4 tinham 1 sinal de calor só (ruído) e caíram no filtro de saliência. Sobraram **2 temas**.

A skill disse isso em uma linha, e não encheu a tabela pra chegar a 10.

## O radar entregue

Saída real: `radar-vet-domiciliar-2026-09-25.md`.

`Radar de veterinária domiciliar para cão idoso, 25/09/2026 (janela: últimos 7 dias)`

| Tema quente | Onde está pegando | Fontes/comunidades | Links representativos | Sinais de calor | O que está sendo dito | Por que importa pro nicho | Ângulo do Método pra postar |
|---|---|---|---|---|---|---|---|
| Ração premium para cão sênior teve o preço reajustado de novo | grupos de tutores | 2 grupos de tutor de cão idoso | `[A CONFIRMAR]` (print sem link) | debate claro (tutores divididos entre trocar e cortar) + implicação real (mexe no bolso do avatar toda semana) | uns dizem que ração sênior é marketing, outros que trocar piorou o cachorro | o tutor está prestes a trocar a comida do cão idoso por preço, sem olhar o resto | O tutor que troca a ração do cachorro de 12 anos pra economizar 80 reais, e paga 900 na consulta de emergência 3 meses depois. |
| Vídeo de um tutor mostrando o cão idoso voltando a subir escada viralizou | vídeo curto | perfil de tutor com alcance no nicho | `[A CONFIRMAR]` (print sem link) | volume forte (muita gente compartilhando) + informação nova pro nicho (o caso mostra reversão, não só cuidado paliativo) | comentários divididos entre "milagre" e "isso não é normal" | é a prova pública de que "é da idade" não fecha o assunto, que é exatamente a tese dela | O que o vídeo do cachorro subindo escada de novo não mostra: os 4 sinais que o tutor ignorou nos 8 meses anteriores. |

**As 2 pautas mais quentes:**
1. A da ração, porque toca o bolso do avatar essa semana e o ângulo mostra a conta que ele não fez.
2. A do vídeo, porque é a tese dela acontecendo em público, com plateia já reunida.

**Nota de honestidade:** 3 itens caíram por falta de data e 4 por terem um sinal de calor só. Os
links dos 2 temas que entraram estão marcados `[A CONFIRMAR]`, porque vieram de print, não de página
aberta. Sem acesso à web, isso é o teto do que dá pra afirmar.

**STOP.** "Qual dessas você quer transformar em peça? Passo pra soft-conteudo-headlines pra escrever
a headline, ou encaixo no calendário da matriz?"

---

## O que rodou por dentro e não apareceu na saída

O gate rodou em cada célula da matriz e em cada linha do radar. Três coisas foram refeitas:

1. **Uma célula virou tema amplo.** "Saúde do cão idoso" não é manchete, é rótulo. Reescrita como a
   cena dos 6 minutos de domingo.
2. **Duas células repetiam a mesma ideia** em pilares diferentes (ambas sobre "é da idade"). Uma
   mudou de ângulo pra virar a versão Antes vs Depois.
3. **Um ângulo do radar era genérico.** A primeira versão do tema do vídeo dizia "aproveite a onda
   do vídeo viral pra falar de cão idoso". Qualquer creator posta isso. Reescrito pra enquadrar pela
   tese dela: o que o vídeo não mostra.

**A varredura anti-IA foi escrita no chat**, como etapa do gate, antes de o doc ser mostrado:

> `Varredura anti-IA do doc: travessao U+2014 encontrados: 0 em nada; verbo-freio banido encontrados: 0 em nada.`

**A tabela do gate não foi impressa.** A veterinária recebeu só os docs.

---

## O que este exemplo prova

1. Os pilares não foram inventados: foram propostos e confirmados pelo dono antes da matriz existir.
2. A matriz fechou 32 pautas distintas, todas manchetes específicas, nunca temas amplos.
3. O radar não fingiu varredura: sem web, conduziu com o que o dono colou e disse o teto disso.
4. Item sem data caiu. Tema com um sinal só caiu. A tabela ficou pequena e honesta.
5. As duas ações pararam num STOP e mandaram a pauta escolhida pra soft-conteudo-headlines, nunca
   escreveram a peça aqui.
