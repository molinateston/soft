# O gate do dossiê, check por check

O gate roda **por dentro**, antes de o dono ver o arquivo. A tabela nunca vai pra saída. O veredito é
o **pior item**, e uma reprovação refaz aquela seção, não o dossiê inteiro.

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

**5. Abertura e fecho de robô.** Reprova a saudação de praxe, o convite a imaginar uma cena, a pergunta
retórica de introdução, a moldura de revelação e o fecho que agradece a leitura. Vale principalmente
pros pontos de conversa e pra frase de abertura do roteiro, que são os pedaços que o dono vai falar.

## Os checks próprios do formato (binários)

| Check | Reprova quando |
|---|---|
| Objetivo | não está em uma frase, ou não tem resultado observável ("avançar" reprova) |
| Fonte | um dado do retrato aparece sem dizer de onde veio e sem `[A CONFIRMAR]` |
| Ponto de conversa | é elogio genérico ao cargo, à empresa ou ao "crescimento impressionante" |
| Próximo passo | o roteiro fecha sem ação, data e responsável |
| Prova da objeção | uma resposta de objeção sai sem a coluna de prova preenchida ou marcada |
| Tamanho | o dossiê não cabe em uma tela e meia |
| Notas internas | contexto de bastidor está misturado com o que pode ser dito na call |
| Perguntas | passa de 8, ou pergunta coisa que estava disponível na pesquisa |

**A reprovação mais grave:** dado sem fonte. Uma afirmação errada sobre a empresa dita na abertura
derruba a credibilidade da conversa inteira, e não há recuperação dentro daquela call. Quando a
pesquisa não confirmou, o item vira pergunta na Ação 3, e a pergunta é sempre melhor que o palpite.

## O lint em código

Com shell disponível, `python3 scripts/lint_copy.py <arquivo>` a partir da pasta desta skill é
**obrigatório**: é ele que decide o item anti-IA do gate. Saída diferente de zero significa reprovação
dura. Sem shell, faça a busca manual pelos dois bloqueios do check 1 e do check 2, no arquivo inteiro.
