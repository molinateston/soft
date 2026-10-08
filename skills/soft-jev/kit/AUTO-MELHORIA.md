Auto-melhoria do JEV automático (ciclo noturno de self-learning)
=================================================================

Implementação de referência, rodável sem nenhuma configuração, em
`codigo/auto-melhoria/` — leia `codigo/auto-melhoria/README.md` para a lista
de scripts, como rodar cada um e o mapeamento exato entre eles e os passos
descritos abaixo. Este documento explica o método; o código mostra o método
funcionando.

Por que isto existe
--------------------

Cada pergunta fechada que o JEV faz (choice, noul ou score) é, na prática, um
classificador escrito em linguagem natural: um texto de pergunta, um critério
do que conta como "sim" e do que conta como "não", e um limiar de confiança a
partir do qual ela dispara. Como todo classificador, ele erra dos dois lados:
dispara quando não devia (falso positivo, incomoda quem está trabalhando) ou
fica calado quando devia ter avisado (falso negativo, deixa passar o problema
que ela existe para pegar). Ajustar o texto e o limiar só "no olho", à mão,
não escala: quanto mais gente usa o hook, mais casos aparecem, e ninguém vai
reler tudo todo dia para sentir se a pergunta está calibrada.

O ciclo de auto-melhoria automatiza esse ajuste usando uma fonte de dado que
já existe de graça: a reação da própria pessoa no turno seguinte. Quando
alguém corrige o agente, cobra "e aí, terminou?" ou confirma satisfeito e
segue para outro assunto, isso já é um rótulo — só não está organizado como
tal. O ciclo junta essas reações, monta um conjunto de casos rotulados, e usa
esse conjunto para comparar o texto antigo da pergunta contra um texto novo
candidato antes de deixar o candidato virar produção.

Os cinco passos
---------------

**1. Coletar.** Ler as conversas/turnos que o próprio agente já teve — pedido
da pessoa, o que o agente respondeu, o pedido seguinte — de onde quer que
esse histórico já esteja guardado. Este passo é só leitura e só organização:
nenhum rótulo é decidido aqui.

**2. Montar o gabarito.** Para cada turno em que o agente respondeu algo,
olhar a reação humana no turno seguinte e classificar o padrão: corrigiu
("não era isso", "está errado", "não funcionou"), cobrou ("cadê", "e o
outro pedido?", "ficou faltando") ou confirmou (seguiu satisfeito, elogiou,
mudou de assunto sem reclamar). Essa reação vira o rótulo verdadeiro/falso de
um caso: por exemplo, se o agente disse "pronto, terminei" sem mostrar prova
nenhuma e a pessoa corrigiu dizendo que não estava pronto, esse é um caso
positivo para a pergunta "a resposta afirma ter terminado sem provar isso?".
Se a pessoa confirmou satisfeita, é um caso negativo. O gabarito cresce todo
dia, sozinho, sem ninguém precisar rotular manualmente caso por caso.

**3. Medir de forma pareada.** Para saber se um texto novo é melhor que o
texto atual, os dois são avaliados no MESMO caso, na mesma rodada — nunca em
dias ou lotes diferentes, porque isso confundiria "o texto melhorou" com "o
dia estava mais fácil". As métricas de cada texto são: taxa de falso
positivo, acerto geral, precisão e cobertura (quantos casos positivos reais
ele realmente pega) e AUC (o quão bem ele separa os casos positivos dos
negativos, para qualquer limiar). Tudo isso acontece sob um teto fixo de
chamadas/custo por rodada — o ciclo nunca gasta sem limite para se
autoavaliar.

**4. Propor e testar em sombra.** Um texto (ou limiar) candidato é gerado a
partir dos erros que o texto atual comete no gabarito. Esse candidato nunca
entra em produção direto: ele fica em "modo sombra" por um período — é
medido todo dia lado a lado com o texto de produção, mas o resultado só vai
para um log; nenhuma pergunta real do dia a dia usa o texto candidato ainda.

**5. Promover só com trava tripla.** Ao final do período em sombra, o
candidato só substitui o texto de produção se (a) ele ganhou do texto atual
num teste reservado desde o início — nunca visto durante a geração do
candidato —, (b) ele não piorou durante os dias em sombra (compara acerto do
candidato × acerto da produção, dia a dia, no mesmo log) e (c) ele não
piorou nenhum caso "estável", ou seja, nenhum caso que o texto atual já
acertava de forma consistente passa a errar com o candidato. Se qualquer uma
das três condições falhar, o candidato fica registrado como reprovado ou
bloqueado, com o motivo escrito — nunca é apagado, só não substitui o que
está no ar.

Sempre acrescentar, nunca desligar
----------------------------------

A regra de ouro do ciclo: ele só tem permissão para trocar o TEXTO e o
LIMIAR de uma pergunta que já existe, ou propor uma pergunta nova. Ele nunca
apaga uma pergunta, nunca desliga uma checagem, e nunca reduz a sensibilidade
de um alarme só porque ele "incomodou" em algum caso isolado — a trava de
regressão do passo 5 existe exatamente para impedir que uma melhoria em um
lugar vire um retrocesso em outro. Candidato reprovado não desaparece: fica
no histórico, com o motivo, para quem for revisar mais tarde.

Como medir antes/depois
------------------------

Antes de qualquer troca, congele um recorte de casos (o "teste") que nunca é
usado para gerar o candidato, só para julgar. Compare sempre acerto, falso
positivo, precisão/cobertura e AUC do texto novo contra o texto antigo nesse
mesmo recorte, e acompanhe também o log de sombra por alguns dias de uso real
antes de decidir. Se o número de casos rotulados naquele recorte for pequeno,
desconfie do resultado — ganho de "2 casos a mais" não é evidência.

Limites honestos
----------------

O método depende inteiramente da qualidade do gabarito: se a reação humana
for ambígua, atrasada ou vier de uma pessoa diferente de quem definiu o
critério original, o rótulo pode estar errado. Ele mede tendência estatística
em cima de poucos casos por pergunta — não é prova formal de que o texto novo
é sempre melhor, só que foi melhor no que já foi visto. E ele não substitui
revisão humana ocasional: de tempos em tempos vale reler os casos e o
histórico de promoções para conferir se a definição do que conta como "sim"
não derivou para algo que ninguém pediu.

A implementação de referência deixa de fora, de propósito, duas partes que só
fazem sentido com várias perguntas automáticas rodando ao mesmo tempo e
acesso a mais de um provedor de LLM: promoção automática de uma pergunta
inteiramente nova (ainda não ativa) para ativa por precisão acumulada, e uma
segunda opinião de outro provedor de LLM como checagem extra antes de
promover uma reescrita. Veja o final de
`codigo/auto-melhoria/README.md` para o porquê de cada uma.
