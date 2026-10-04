# Exemplo fim a fim: dois casos completos

**EXEMPLO:** os dois casos são inventados, com dado fictício e nicho neutro. Não copie o dado, use o seu: os números, as falas e as credenciais abaixo existem só no insumo de mentira de cada caso. Do primeiro "oi" ao gancho final. O primeiro é um reel falado de conteúdo (gate no modo padrão). O segundo é a capa de um carrossel que vende (gate no modo rigoroso). Todo veredito abaixo é o do gate de verdade, com o lint e a régua de títulos rodados por script e a crítica aplicada linha por linha; nenhum foi montado de cabeça. Leia antes da primeira rodada.

## Caso 1: reel falado, professora de inglês pra adultos

**Pedido:** "Me guia num gancho pro reel de amanhã."

**Abertura da skill (resumida):** "Vou te pedir 5 coisas, uma de cada vez: formato, tipo de conteúdo, objetivo, público com uma cena, e a fala de um aluno com a sua prova. Leva umas 6 a 8 mensagens. No fim você recebe uma pasta com o gancho escolhido, preenchido e conferido. O que só você tem é a fala do aluno, de onde ela veio, e os seus números; sem eles eu te pergunto e não invento."

| Pergunta | Resposta da dona |
|---|---|
| 1 de 5, formato | Reel falado, olhando pra câmera. |
| 2 de 5, tipo de conteúdo | Assunto livre: por que o adulto entende inglês e não consegue responder. |
| 3 de 5, objetivo | Alcance. Quero que a pessoa pense "sou eu". |
| 4 de 5, público e cena | Adulto de 30 a 45 anos que estudou anos e fica mudo na reunião em inglês, com a câmera ligada. |
| 5 de 5, parte 1, a fala | Aluna: "Eu entendo tudo, mas na hora de responder some tudo da cabeça." Veio de um depoimento escrito no grupo da turma, e a aluna autorizou o uso em 01/10. |
| 5 de 5, parte 2, a prova | 9 anos de aula, 140 alunos adultos, e o método de respostas prontas de 3 palavras desde o primeiro mês. A skill avisa: na fala de 7 palavras cabe o método ou o número, não os dois; o outro vai pra legenda. A dona escolhe o método. |

As respostas das perguntas 4 e 5 vão pro `insumos/perfil.md` da dona, uma por linha, com a origem e a autorização da fala.

**Os 3 moldes oferecidos** (assunto livre, então universais; objetivo alcance, então o cartão `frameworks/01-reconhecimento.md`, cuja condição de entrada pede cena, recorte do público e fato da dona, todos no insumo; reel falado, então coluna Reel com falar; 2 famílias):

```
1. G001 · Reconhecimento · universal
   [Público], [ganho específico pra ele]
   por que pra você: chama o adulto na primeira palavra e já promete a saída
   prova: medido, mediana 12,8x, 7 aberturas; a sua versão é variante sem medição · teto: falado até 7 palavras
2. G004 · Reconhecimento · universal
   Deixa eu adivinhar: você [3 hábitos do público]
   por que pra você: você conhece os hábitos do aluno de cor
   prova: medido, mediana 6,0x, 1 abertura; a sua versão é variante sem medição · teto: falado até 7 palavras
3. G094 · Reconhecimento por estado emocional · universal
   Pra você que sente [sensação no corpo] toda vez que [cena]
   por que pra você: a fala da aluna é uma sensação ("some tudo")
   prova: sem medição (novo) · teto: falado até 7 palavras
```

A dona escolhe o G001.

**Preenchimento, primeira versão:** "Adulto, isso vai mudar o seu inglês." (7 palavras, 36 caracteres.)

A régua de títulos para essa versão antes da crítica: "isso" é palavra-ponteiro sem o objeto na frase, e a pergunta natural de um estranho é "isso o quê?". Título reprovado é falha bloqueante. O teste do concorrente do gate também cai: com a marca coberta, qualquer professora de inglês publica a mesma frase, e não sobra nenhum fato da dona. O veredito real desta versão:

```
peça: Adulto, isso vai mudar o seu inglês.
tipo: headline (gancho falado de reel)
modo: padrão
veredito: REPROVADA
títulos auditados: 1 · reprovados: 1
encaixe narrativo: não medido, sem arco informado
falhas:
  - filtro: Régua de títulos (título que se explica sozinho)
    dimensao: palavra abstrata órfã · bloqueante
    trecho: "isso vai mudar"
    motivo: "isso" não tem antecedente na frase; o estranho pergunta "isso o quê?"
    sugestao: nomeie a ação: "Adulto, responde em inglês com 3 palavras."
  - filtro: Validador de conversão
    dimensao: critério 1, promessa copiável · gravidade 9
    trecho: "mudar o seu inglês"
    motivo: com a marca coberta, qualquer perfil de idioma assina igual
    sugestao: molde de promessa aplicado: a ação do método dito em palavras simples, "responde com 3 palavras"
suspenso pela cascata: CUB com 1 achado (B, promessa batida); filtros 2 e 4 não rodaram
Quer a peça de volta no molde certo? Aponte as falhas e a skill de origem devolve a versão corrigida.
Copy que qualquer concorrente assinaria já está enterrada; o caixa só demora uns dias pra mandar o aviso.
```

**Preenchimento, segunda versão:** "Adulto, responde em inglês com 3 palavras." (7 palavras, 42 caracteres, teto falado até 7: passa.)

Teste do concorrente do gate: com a marca coberta, sobra o método das respostas de 3 palavras dito em palavras simples, que é da dona. O pré-filtro também passa: trocando inglês por violão, a frase perde o sentido.

No reel, as frentes ficam assim: FALAR "Adulto, responde em inglês com 3 palavras." · TEXTO NA TELA o trecho literal da aluna, "some tudo da cabeça" (4 palavras, 19 caracteres, teto de tela: passa) · MOSTRAR a dona com o notebook aberto numa chamada de vídeo. A tela entra porque a aluna autorizou; sem autorização, a cena iria com as palavras da dona.

O arquivo `ganchos-ingles-reuniao.md` traz a frase dita no título, a tabela das três frentes e a ficha (formato e contagem, molde, selo, fala com origem, prova, os outros 2 moldes, próximo passo). A régua de títulos sai em `conferencia/checagem-titulos.md` e o `--conferir` da definição de pronto devolve exit 0. O veredito real:

```
peça: Adulto, responde em inglês com 3 palavras.
tipo: headline (gancho falado de reel, com texto na tela)
modo: padrão
veredito: APROVADA
resumo: a fala dá a ação (responder), o caminho (3 palavras) e chama o público na primeira palavra, e a tela traz o trecho literal da aluna; régua de títulos, CUB, critérios 1 a 4 e lastro sem falha. Pode subir.
títulos auditados: 2 · reprovados: 0
encaixe narrativo: não medido, sem arco informado
observacoes:
  - critério 1 pela leitura que cobre marca e método e procura o fato que só a dona tem; se o dono do gate ler o teste ao pé da letra (a mesma promessa no perfil da concorrente mais próxima), outra professora publica a mesma técnica e a peça reprova com gravidade 9
  - o vocativo "Adulto" é público largo (gravidade 3, observação)
  - teste do nicho trocado: a tela não tem substantivo do nicho e sobrevive em qualquer mercado (1 sim, teto 1)
```

Lint: `✓ copy passou no anti-IA em código (0 falhas duras, 0 aviso(s) pra revisar no olho).`

**Relato no chat:**

```
Pronto: "Adulto, responde em inglês com 3 palavras." (falado), com "some tudo da cabeça" na tela.
Abra primeiro: ganchos-ingles-reuniao/ganchos-ingles-reuniao.md
Falta você responder: nada.
ganchos-ingles-reuniao.md: exit 0 · conferencia/checagem-titulos.md: exit 0 · conferencia/veredito-copy-ingles-reuniao.md: exit 0
conferência ok: a entrega sai.
conferir_fontes: exit 0 · todo número, nome e aspa do gancho tem fonte no insumo
Quer mais 3, outra família ou a versão pra capa de carrossel?
```

Próximo passo: o roteiro do reel na soft-conteudo-reels, com o gancho já cravado.

## Caso 2: capa de carrossel que vende, marcenaria de móveis planejados

**Pedido:** "Gancho pra capa de um carrossel que vende o meu projeto de cozinha."

O pedido já diz o formato (capa de carrossel), então a skill pula a pergunta 1 e confirma em uma linha: "Capa de carrossel, peça de venda: a crítica vai rodar no modo rigoroso, nota de 0 a 10, só 10 sobe."

| Pergunta | Resposta do dono |
|---|---|
| 2 de 5, tipo de conteúdo | Lista: 3 números que eu meço na parede antes de desenhar a cozinha. |
| 3 de 5, objetivo | Converter: quero que comentem e peçam a visita. |
| 4 de 5, público e cena | Casal que comprou apartamento na planta e recebe as chaves em 3 meses, com o projeto da cozinha aberto no celular. |
| 5 de 5, parte 1, a fala | Cliente: "A gente quer fazer tudo de uma vez, mas tem medo do móvel estufar." Veio da conversa na visita técnica com um casal que já fechou, que autorizou o uso em 01/10. |
| 5 de 5, parte 2, a prova | 14 anos, 380 cozinhas entregues, a medição dos 3 pontos em toda visita (umidade da parede, prumo e distância do ponto de água) e 5 anos de garantia. A skill avisa: na capa de até 15 palavras e 65 caracteres cabe um número e o método, e a fala do casal vai pro slide 2. O dono escolhe as 380 cozinhas. |

**Os 3 moldes oferecidos** (conteúdo em lista, então o cartão `frameworks/16-tipo-lista.md` mais os universais; objetivo converter, então os cartões 12 e 14, Erro e alerta e Número e lista; capa, então Formato carrossel ou ambos; 2 famílias):

```
1. G129 · Erro e alerta · específico: só se a peça é lista
   [N] erros que custam [o recurso, com número] a quem quer [resultado]
   prova: medido na forma original, mediana 10,0x, 1 abertura; a sua versão é variante sem medição · teto: capa de 8 a 15 palavras
2. G112 · Número e lista · específico: só se a peça é lista
   [N] [coisas] [o resultado que você viu, com prazo ou número]
   prova: medido na forma original, mediana 5,0x, 34 aberturas; a sua versão é variante sem medição · teto: capa de 8 a 15 palavras
3. G115 · Número e lista · específico: só se a peça é lista
   Não [tome a decisão] antes de ver estes [N] números de [onde]
   por que pra você: segura o casal na hora de fechar e o conteúdo já são 3 números
   prova: sem medição (casa) · teto: capa de 8 a 15 palavras
```

O dono escolhe o G115, mesmo sem medição, porque o conteúdo já são 3 números e o casal está a 3 meses de fechar.

**Preenchimento, primeira versão:** "Não feche móveis planejados antes de ver estes números" (9 palavras, 54 caracteres). A régua de títulos para a versão: sem o lugar dos números, "estes números" fica órfão ("que números?"). O veredito real:

```
peça: Não feche móveis planejados antes de ver estes números
tipo: capa
modo: rigoroso
nota: 4/10
veredito: REFAZER
títulos auditados: 1 · reprovados: 1
encaixe narrativo: não medido, sem arco informado
reescrita por gravidade:
  1. régua de títulos · bloqueante · "estes números" sem o lugar de onde saem; o estranho pergunta "que números?"
  2. critério 1, promessa copiável · gravidade 9 · qualquer marcenaria publica a mesma frase; ponha o número que só o dono tem e o lugar da medição
  3. critério 2, dor verdadeira · gravidade 8 · nenhum elemento de cena nem de público; a parede do apartamento novo é a cena do casal
suspenso pela cascata: CUB, filtros 2 e 4 e checkpoints não rodaram
abaixo de 10 não sobe.
Quer a peça de volta no molde certo? Aponte as falhas e a skill de origem devolve a versão corrigida.
Copy que qualquer concorrente assinaria já está enterrada; o caixa só demora uns dias pra mandar o aviso.
```

A nota sai da regra: a falha de gravidade 9 limita a 5, e a segunda falha de gravidade 7 ou mais tira 1 ponto.

**Preenchimento, segunda versão:** "380 cozinhas: não feche o planejado antes dos 3 números da parede" (12 palavras, 65 caracteres, capa de 8 a 15 e até 65: passa). Palavra em destaque: parede. A frase traz o que o leitor vive (a hora de fechar o planejado) e a causa que ele não via (a parede decide), numa linha só.

Teste do concorrente do gate: com a marca e a medição cobertas, sobram as 380 cozinhas, que só o dono afirma.

**CTA do fim:** antes de escrever, a skill pergunta qual palavra a automação dele já responde, onde ela está e se a ficha prometida existe. O dono responde: a palavra PAREDE manda a ficha da medição no direct, ligada desde março, e a ficha é um PDF de 1 página. As duas respostas vão pro perfil, e o CTA sai "Comenta PAREDE que eu te mando a ficha da medição dos 3 pontos." Sem palavra registrada, o CTA sairia "Me chama no direct e eu te mando a ficha da medição dos 3 pontos."

O `--conferir` devolve exit 0, com `palavra-chave: PAREDE` achada no perfil e a automação declarada. O veredito real:

```
peça: 380 cozinhas: não feche o planejado antes dos 3 números da parede
tipo: capa (carrossel que vende o projeto de cozinha, com CTA)
modo: rigoroso
nota: 9/10
veredito: REFAZER
títulos auditados: 2 · reprovados: 0
encaixe narrativo: não medido, sem arco informado
filtro 6: critérios 1 a 3 passam; o 4 fica pro corpo (headline de proibição); o 5 é n/a na linha
checkpoints:
  - mecanismo: 7 de 10 sim; não no 1 (a oferta não tem nome próprio na peça), no 3 (a medição é prática conhecida do ramo) e no 8 (sem metáfora dele); faixa do meio, gravidade 6
  - voz: 12 de 12 sim (os itens de arco ficam n/a em peça de 2 linhas)
  - transformação: 11 de 15 sim; não no 2 (prazo), no 3 (métrica do resultado), no 4 (o leitor com o resultado na mão) e no 5 (antes e depois); faixa do meio, gravidade 6
reescrita por gravidade:
  1. checkpoint 1, mecanismo único · gravidade 6 · a capa traz a medição e a credencial e não traz nome próprio da oferta, processo exclusivo nem metáfora do dono
  2. checkpoint 3, transformação · gravidade 6 · a capa proíbe e não mostra o resultado: falta o que muda na cozinha do casal e em quanto tempo
observacoes:
  - se o dono do gate ler o teste do concorrente ao pé da letra, a cascata para a leitura e a nota cai a 5/10
  - a distância do ponto de água não é número da parede no sentido estrito
abaixo de 10 não sobe.
Quer a peça de volta no molde certo? Aponte as falhas e a skill de origem devolve a versão corrigida.
Copy que qualquer concorrente assinaria já está enterrada; o caixa só demora uns dias pra mandar o aviso.
```

O veredito traz também as perguntas dos checkpoints 1 e 3, que o dono responde pra soltar a próxima rodada. A skill não chama a capa de aprovada. Leva ao dono a nota, as duas falhas e as perguntas, e ele decide: responde as perguntas pra uma terceira rodada (por exemplo, dando nome à medição ou trazendo o prazo de um caso entregue), ou publica a capa com 9 sabendo que o gate pede 10.

**Relato no chat:**

```
Pronto: não, o gate deu 9/10 (faltam nome próprio da oferta e o resultado na capa).
Abra primeiro: ganchos-cozinha-planejada/ganchos-cozinha-planejada.md
Falta você responder: 2 perguntas (nome da medição, prazo de um caso).
ganchos-cozinha-planejada.md: exit 0 · conferencia/checagem-titulos.md: exit 0 · conferencia/veredito-copy-cozinha-planejada.md: exit 0
conferência ok: a entrega sai.
conferir_fontes: exit 0 · todo número, nome e aspa do gancho tem fonte no insumo
Quer a terceira rodada com as suas respostas, ou a versão pro reel (até 7 palavras)?

Perguntas pra você
A medição dos 3 pontos tem um nome que só você usa?
Em quanto tempo, depois da entrega, um móvel estufado apareceria numa parede sem medição?
```

Próximo passo, se o dono publicar: o corpo na soft-conteudo-carrossel, com a capa já cravada; a arte da capa na soft-designer.
