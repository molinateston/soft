# O gate, check por check

O gate roda **por dentro**, em cada e-mail, antes de o dono ver qualquer coisa. A tabela nunca vai
pra saída: o que sai é o e-mail limpo. O veredito é o **pior item**, e uma reprovação refaz aquela
peça, não a campanha inteira.

## Os 5 checks anti-IA (inline, sem depender de arquivo externo)

**1. Travessão longo.** Zero ocorrência de U+2014 e U+2013 no arquivo inteiro, notas incluídas.
Ponto final ou hífen comum no lugar. Faixa numérica escreve "10 a 20", não usa traço.

**2. Verbo-freio banido.** A família que a régua anti-voz proíbe (o verbo que rima com "cravar" e
todas as flexões dele) não aparece em lugar nenhum. Substitutos: emperrar, empacar, parar, freio,
amarra, prender.

**3. Antítese de espelho.** Reprova todo molde que nega um polo curto pra afirmar o outro: o par
colado numa frase só, o mesmo par quebrado em duas frases, a versão com a preposição "sobre", a
negação pelada seguida da virada, e duas negações paralelas empilhadas uma atrás da outra. Afirme o
que é, com sujeito e cena.
Ruim: um par de duas palavras, uma negada e outra afirmada, com ponto no meio.
Bom: "Quando a pessoa pergunta o preço três vezes, ela ainda não viu o que recebe."

**4. Verbo de transformação genérico.** Reprova a família de verbos grandiosos de folheto: os que
falam em revolução, redefinição, liberação de potencial, amplificação, ganho de escala e superação
de limites. Troque por concreto: resolve, tira, muda, faz, corta, encurta.

**5. Abertura e fecho de robô.** Reprova a saudação de praxe que deseja que o e-mail encontre a
pessoa bem, o convite a imaginar uma cena, a pergunta retórica de introdução, a moldura de revelação
que anuncia um segredo, o conectivo formal de dissertação e o fecho que agradece a leitura. Corte a
frase e comece pela seguinte, que quase sempre é a boa.

## Os checks próprios do formato (binários)

| Check | Reprova quando |
|---|---|
| Um trabalho só | o e-mail pede duas coisas diferentes |
| Um CTA principal | há dois pedidos concorrentes, ou o destino não está escrito |
| Assunto | passa de 50 caracteres sem motivo, ou a prévia só repete o assunto |
| Ancoragem | número, caso ou fala aparece sem fonte declarada |
| Furo marcado | falta `[A CONFIRMAR: o quê]` onde o insumo não veio |
| Saída | falta o link de saída da lista |
| Personalização | o campo é genérico a ponto de servir pra qualquer pessoa da base |
| Placeholder repetido | o mesmo colchete aparece em dois e-mails: reprova a campanha inteira |

O último merece nome próprio. Placeholder repetido é o sinal de que o insumo faltou e a skill
escreveu por cima dele. Ou você tem o dado e escreve, ou você para e pergunta. Um `[A CONFIRMAR]`
isolado, num ponto onde o dono precisa mesmo decidir, continua valendo.

## O lint em código

Com shell disponível, `python3 scripts/lint_copy.py <arquivo>` a partir da pasta desta skill é
**obrigatório**: é ele que decide o item anti-IA do gate, e ele pega o que o olho perde. Saída
diferente de zero significa reprovação dura, e o arquivo volta pra correção antes de qualquer
entrega. Sem shell, faça a busca manual pelos dois bloqueios do check 1 e do check 2, no arquivo
inteiro, notas incluídas.
