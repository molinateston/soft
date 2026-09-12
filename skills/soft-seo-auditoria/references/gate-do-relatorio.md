# O gate do relatório, check por check

O gate roda **por dentro**, antes de o dono ver qualquer coisa. A tabela nunca vai pra saída. O
veredito é o **pior item**, e uma reprovação refaz aquela seção, não a auditoria inteira.

## Os 5 checks anti-IA (inline)

**1. Travessão longo.** Zero ocorrência de U+2014 e U+2013 no arquivo inteiro, notas incluídas. Ponto
final ou hífen comum no lugar. Faixa numérica escreve "10 a 20".

**2. Verbo-freio banido.** A família que a régua anti-voz proíbe (o verbo que rima com "cravar" e todas
as flexões dele) não aparece. Substitutos: emperrar, empacar, parar, freio, amarra, prender.

**3. Antítese de espelho.** Reprova todo molde que nega um polo curto pra afirmar o outro: o par colado
numa frase só, o mesmo par quebrado em duas, a versão com a preposição "sobre", a negação pelada
seguida da virada, e duas negações paralelas empilhadas. Afirme o que é, com sujeito e cena.

**4. Verbo de transformação genérico.** Reprova a família de verbos grandiosos de folheto: os que falam
em revolução, redefinição, liberação de potencial, amplificação, ganho de escala e superação de
limites. Troque por concreto: resolve, tira, muda, corta, encurta.

**5. Abertura e fecho de robô.** Reprova a saudação de praxe, o convite a imaginar uma cena, a pergunta
retórica de introdução, a moldura de revelação que anuncia um segredo, o conectivo formal de
dissertação e o fecho que agradece a leitura.

## Os checks próprios do formato (binários)

| Check | Reprova quando |
|---|---|
| Fonte do número | volume, dificuldade, posição ou velocidade aparecem sem dizer de onde vieram |
| Gravidade | uma recomendação sai sem crítico, alto, médio ou baixo |
| Esforço | uma recomendação sai sem rápido, meio dia ou obra |
| Conserto executável | o item diz o problema e não diz o que abrir e o que escrever no lugar |
| Furo marcado | falta `[A CONFIRMAR: o quê]` onde o dado não foi verificado |
| Nada inventado | dado não medido aparece como número em vez de "não medido" |
| Intenção conferida | uma palavra é recomendada sem dizer que tipo de página ela pede |
| Plano nas duas colunas | a auditoria completa fecha sem separar conserto rápido de obra |

**A reprovação mais comum e mais grave:** número sem fonte. Auditoria de SEO é um documento que o dono
usa pra decidir onde gastar meses de trabalho; um volume de busca inventado desperdiça o trimestre
dele. Quando não houver dado, escreva "não medido" e diga onde ele consegue medir de graça.

## O lint em código

Com shell disponível, `python3 scripts/lint_copy.py <arquivo>` a partir da pasta desta skill é
**obrigatório**: é ele que decide o item anti-IA do gate. Saída diferente de zero significa reprovação
dura, e o arquivo volta pra correção antes de qualquer entrega. Sem shell, faça a busca manual pelos
dois bloqueios do check 1 e do check 2, no arquivo inteiro, notas incluídas.
