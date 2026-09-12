# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome de empresa, valores, prazos e resultados foram inventados só
> pra mostrar a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma
> entrega de verdade. Num trabalho real, todo número sem fonte nasce marcado `[A CONFIRMAR]` e o dono
> confirma antes de sair.

**O caso fictício:** uma empresa de manutenção predial de condomínios (elevador, bomba d'água,
gerador, parte elétrica). Fechou uma reunião com um síndico e precisa mandar no mesmo dia quatro
arquivos: a proposta em Word (o síndico edita e leva pra assembleia), a apresentação em PowerPoint,
a planilha de custo mensal com as premissas abertas, e o contrato em PDF pra assinatura.

Este arquivo mostra a saída resumida de cada ação, na ordem. A saída real é maior; aqui está só o
suficiente pra você reconhecer o formato antes de começar.

---

## O que o dono deu de entrada

> "Fechei a reunião com o síndico do Edifício Aroeira. Tenho a proposta escrita em markdown, o
> roteiro dos slides que eu usei na conversa, e uma tabela de custo que eu montei no bloco de notas.
> Preciso mandar tudo hoje, num formato que ele consiga abrir no computador dele e levar pra
> assembleia."

**O que faltava:** o formato de cada arquivo, e na tabela de custo o que era premissa e o que era conta.

## As perguntas que a skill fez (uma por vez)

1. "Quem vai abrir cada arquivo, e pra quê?" → *"O síndico edita a proposta pra levar pra
   assembleia. Os slides ele só apresenta. A planilha ele vai querer mexer nos números. O contrato é
   pra assinar."*
   → decidiu sozinho: proposta em Word, slides em PowerPoint, planilha em xlsx, contrato em PDF.
2. "Na tabela de custo, quais desses números você vai querer mudar depois pra ver o resultado mudar?"
   → *"O valor da hora técnica, a quantidade de visitas por mês e o percentual de peça."*
   → esses três viram célula de entrada destacada, e todo o resto vira fórmula que aponta pra eles.
3. "Tem identidade visual (cor, fonte, logo) ou uso o padrão sóbrio?" → *"Não tenho nada pronto."*

**Premissa declarada em 1 linha:** sem identidade visual, os quatro saem em padrão sóbrio (Arial,
preto no branco), e trocar isso depois é uma passada só.

## A medição da máquina (antes de qualquer conversão)

```
$ python3 scripts/checar_dependencias.py
== DOCX ==
  [nao ] docx-js      (falta: docx)
  [OK  ] python-docx  cria e edita Word em Python
  [OK  ] pandoc       converte markdown em Word direto
  -> use a rota: python-docx
== PPTX ==
  [nao ] pptxgenjs    (falta: pptxgenjs)
  [OK  ] python-pptx  cria e edita deck em Python
  -> use a rota: python-pptx
== XLSX ==
  [OK  ] openpyxl     cria e edita planilha com formula viva
  -> use a rota: openpyxl
== PDF ==
  [OK  ] libreoffice  converte docx, pptx, xlsx ou html em PDF fiel
  -> use a rota: libreoffice
```

**O que isso mudou no trabalho:** os quatro formatos saem. O deck vai pela rota de Python, que não
faz gráfico nativo, então o único gráfico do roteiro vira tabela, e isso foi dito ao dono.

---

## Ação 1 · WORD

Saída real: `proposta-manutencao-edificio-aroeira.docx`. Resumo do que entrou:

| Bloco | O que virou no arquivo |
|---|---|
| Título e subtítulo | Título nível 1, com o nome do condomínio e a data |
| Sumário | Automático, montado a partir dos títulos nativos |
| 1. O que foi conversado | Parágrafos corridos, 3 deles |
| 2. Escopo do atendimento | Lista com marcador nativo, 7 itens |
| 3. O que não está incluído | Lista com marcador nativo, 4 itens |
| 4. Investimento | Tabela de 3 colunas (item, periodicidade, valor), largura declarada em cada célula |
| 5. Prazo e vigência | Parágrafos, com `[A CONFIRMAR: data de início]` visível na página |
| 6. Próximo passo | Parágrafo, com o contato |

**Trecho, como saiu na página:**

> **4. Investimento**
>
> | Item | Periodicidade | Valor |
> |---|---|---|
> | Visita técnica preventiva | 2 por mês | `[fictício]` R$ 1.480 |
> | Plantão para chamado urgente | sob demanda | `[fictício]` R$ 220 por hora |
> | Relatório mensal de condição | mensal | incluso |
>
> Peça de reposição entra à parte, pelo custo mais 15 por cento de administração.
> `[A CONFIRMAR: se a assembleia aprova o percentual ou prefere teto fixo por mês]`

**O que a conferência pegou:** a terceira coluna saiu estreita demais e o valor quebrou em duas
linhas. Corrigido no gerador, redistribuindo a largura das colunas.

---

## Ação 2 · POWERPOINT

Saída real: `apresentacao-aroeira.pptx`, 9 slides. Resumo:

| Slide | Título | O que carrega |
|---|---|---|
| 1 | Manutenção predial do Edifício Aroeira | Capa, fundo escuro, data |
| 2 | O que a gente viu no prédio | 4 itens, ícone em círculo em cada um |
| 3 | O custo de esperar quebrar | Tabela de 3 linhas (era pra ser gráfico, virou tabela pela rota disponível) |
| 4 a 6 | Como funciona · O que está incluso · Quem atende | Passos numerados, duas colunas comparando incluso e não incluso, uma pessoa por linha |
| 7 a 9 | Investimento · Prazo · Próximo passo | Número grande no centro, linha do tempo de 4 marcos, um pedido só com o contato |

**O que a conferência visual pegou:** no slide 5 o título da coluna da direita ficou colado no
primeiro item, e no slide 7 o número grande estourava a caixa por 3 caracteres. Os dois foram
corrigidos e o deck foi renderizado de novo.

**A linha honesta que foi pro dono:** "o slide 3 era pra ser gráfico de barras; a biblioteca de
gráfico nativo não está nesta máquina, então saiu como tabela. Vira barra assim que ela existir."

---

## Ação 3 · PLANILHA

Saída real: `custo-mensal-aroeira.xlsx`, uma aba. Resumo da estrutura:

```
Aba "Custo mensal"

  A                                   B            C
1 PREMISSAS (mexa só aqui)
2 Valor da hora técnica               R$ 185       <- entrada, fundo amarelo, texto azul
3 Visitas preventivas por mês         2            <- entrada
4 Horas por visita                    4            <- entrada
5 Administração sobre peça            15,0%        <- entrada, guardada como fração
7 CONTA
8 Horas preventivas no mês            =B3*B4
9 Custo de mão de obra preventiva     =B8*B2
10 Média histórica de peça no mês     R$ 640       <- entrada, com a origem ao lado
11 Administração sobre peça           =B10*B5
12 CUSTO MENSAL                       =B9+B10+B11
```

Ao lado da célula B10, na coluna C: *"Média das notas de peça dos últimos 6 meses informada pelo
síndico na reunião. `[A CONFIRMAR: as notas em si, que não foram enviadas]`"*

**O recálculo:**

```
$ python3 scripts/xlsx/recalc.py custo-mensal-aroeira.xlsx
{"status": "success", "total_formulas": 5, "total_errors": 0}
```

**A conferência que o recálculo não faz:** as 5 fórmulas foram lidas à mão contra o valor esperado.
A B8 estava como `=B3*B5` em vez de `=B3*B4`. Recálculo limpo, número errado, exatamente o caso que
a régua avisa. Corrigido.

---

## Ação 4 · PDF

Saída real: `contrato-aroeira.pdf`, gerado a partir do `.docx` do contrato pela rota do LibreOffice.

```
$ python3 scripts/office/soffice.py --headless --convert-to pdf contrato-aroeira.docx
$ pdftoppm -jpeg -r 100 contrato-aroeira.pdf pagina
$ ls pagina-*.jpg
pagina-1.jpg  pagina-2.jpg  pagina-3.jpg
```

**O que a conferência visual pegou:** a linha de assinatura da página 3 caiu sozinha no alto de uma
página nova, separada do fecho. Resolvido no `.docx` de origem, juntando os dois num bloco que não
se separa, e o PDF foi gerado outra vez.

**Os campos vazios**, listados na entrega: data de assinatura, segundo testemunho, CNPJ.

---

## Ação 5 · LER E CONFERIR

O síndico devolveu a proposta com alterações e pediu "me diz o que ele mudou".

```
$ python3 scripts/docx/merge_runs.py proposta-devolvida.docx -o juntada.docx
$ pandoc -t markdown juntada.docx | diff - proposta-original.md
```

**O que apareceu:** três mudanças. Prazo de chamado urgente de 4 para 2 horas, percentual de
administração cortado de 15 para 10, e uma frase nova pedindo relatório fotográfico em toda visita.

**Como foi entregue:** as três em lista, com o texto antes e depois de cada uma, mais uma linha
dizendo que a do percentual mexe no preço e precisa de decisão do dono. Nenhuma foi aceita nem
recusada pela skill.

---

## O gate, no fim de tudo

| Check | Proposta | Deck | Planilha | Contrato |
|---|---|---|---|---|
| Abre · conteúdo completo · nome e destino · anti-IA | ✓ | ✓ | ✓ | ✓ |
| Sem sobra de template | ✓ | ✓ corrigido: slide 6 tinha "nome do técnico" | ✓ | ✓ |
| Furo visível como `[A CONFIRMAR]` | ✓ data de início | n/a | ✓ notas de peça | ✓ 3 campos |

```
$ python3 scripts/lint_copy.py proposta-manutencao-edificio-aroeira.md
OK (0 HARD, 1 WARN)
```

O aviso apontava "solução" três vezes na seção 2. Reescrita nomeando cada uma: "visita preventiva",
"plantão", "relatório".

## A mensagem final ao dono (a forma da entrega)

> Os quatro arquivos estão prontos, na pasta do projeto:
>
> - `proposta-manutencao-edificio-aroeira.docx` (o síndico edita e leva pra assembleia)
> - `apresentacao-aroeira.pptx` (9 slides; o slide 3 saiu como tabela, veja abaixo)
> - `custo-mensal-aroeira.xlsx` (as 4 premissas estão em amarelo, mexa só nelas)
> - `contrato-aroeira.pdf` (3 campos ficaram vazios: data, segundo testemunho, CNPJ)
>
> Duas coisas pra você decidir: o percentual de administração (a proposta está com 15, ele marcou
> 10) e a data de início. Uma técnica: o gráfico do slide 3 virou tabela por falta de biblioteca.
