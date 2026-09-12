# O gate da abordagem, check por check

O gate roda **por dentro**, antes de o dono ver a mensagem. A tabela nunca vai pra saída. O veredito é
o **pior item**, e uma reprovação refaz aquela mensagem, não a lista inteira.

## O teste que vem antes de todos

**A troca de nome.** Troque o nome da empresa e da pessoa por outro qualquer da lista. Se a mensagem
continuar fazendo sentido, ela **reprova**. Não é personalização de superfície que se pede aqui: é a
prova de que a pesquisa aconteceu. Toda mensagem que passa nesse teste tem pelo menos uma frase que só
serve àquela conta.

## Os 5 checks anti-IA (inline)

**1. Travessão longo.** Zero ocorrência de U+2014 e U+2013 no arquivo inteiro, notas incluídas.

**2. Verbo-freio banido.** A família que a régua anti-voz proíbe (o verbo que rima com "cravar" e todas
as flexões dele) não aparece. Substitutos: emperrar, empacar, parar, freio, amarra, prender.

**3. Antítese de espelho.** Reprova todo molde que nega um polo curto pra afirmar o outro: o par colado
numa frase só, o mesmo par quebrado em duas, a versão com a preposição "sobre", a negação pelada
seguida da virada, e duas negações paralelas empilhadas.

**4. Verbo de transformação genérico.** Reprova a família de verbos grandiosos de folheto: os que falam
em revolução, redefinição, liberação de potencial, amplificação e ganho de escala. Troque por concreto:
resolve, tira, muda, corta.

**5. Abertura e fecho de robô.** Reprova a saudação de praxe que deseja que a mensagem encontre a pessoa
bem, o convite a imaginar, a pergunta retórica de introdução, a moldura de revelação e o fecho que
agradece a leitura. Numa mensagem fria, qualquer uma dessas sozinha já derruba a leitura.

## Os checks próprios do formato (binários)

| Check | Reprova quando |
|---|---|
| Motivo com fonte | a abertura afirma algo sobre a empresa e a fonte não está anotada |
| Um pedido só | há dois pedidos, ou o pedido tem fricção alta no primeiro contato |
| Tamanho | o e-mail frio passa de 120 palavras |
| Formato | há marcação de negrito ou itálico, ou lista elaborada no corpo |
| Prova | um caso ou número é citado sem autorização ou sem fonte, e sem `[A CONFIRMAR: prova]` |
| Anexo | há anexo no primeiro toque |
| Saída | falta a linha que diz como pedir pra parar |
| Volume | o plano de envio passa da régua da situação do domínio |
| Retomada | um toque repete o ângulo do anterior, ou cobra a falta de resposta |
| Encerramento | o toque 3 é irônico, passivo ou não encerra de verdade |

## A reprovação mais grave

Afirmação sobre a empresa sem fonte. Numa abordagem fria não existe segunda chance: uma frase errada
sobre o negócio da pessoa encerra a conversa antes dela começar, e ainda ensina o destinatário a
ignorar o remetente para sempre. Quando a pesquisa não confirmou, a frase sai, ou vira pergunta.

## O lint em código

Com shell disponível, `python3 scripts/lint_copy.py <arquivo>` a partir da pasta desta skill é
**obrigatório**: é ele que decide o item anti-IA do gate. Saída diferente de zero significa reprovação
dura. Sem shell, faça a busca manual pelos dois bloqueios do check 1 e do check 2, no arquivo inteiro.
