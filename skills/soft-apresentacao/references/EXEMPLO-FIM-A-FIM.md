# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, marca, números e resultados foram inventados só pra mostrar
> a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega de
> verdade. Num trabalho real, todo número e toda prova sem fonte nascem marcados `[A CONFIRMAR]` e o
> dono confirma antes de sair.

**O caso fictício:** uma nutricionista que atende esportista amador e foi convidada pra falar 25
minutos num encontro de corredores de rua. Ela não tem deck, tem as anotações da fala num documento
de 3 páginas. Identidade visual fictícia: nenhuma, então o padrão neutro B80/C20 manda.

Este arquivo mostra a Ação 1 (deck novo) inteira, de ponta a ponta, e no fim resume o que muda nas
Ações 2 e 3.

---

## 1 · O pedido

> "Fui chamada pra falar 25 minutos num evento de corrida no mês que vem. Tenho as anotações aqui.
> Consegue montar os slides? E eles querem o PDF depois pra mandar pra quem foi."

## 2 · O bloco de perguntas de alinhamento (mandado de uma vez só)

> Pra montar o deck certo de primeira, me responde essas 6 rapidinho, pode ser em uma linha cada:
> 1. Qual o objetivo da apresentação e quem está na plateia?
> 2. O conteúdo já existe em algum lugar, ou nasce agora a partir do tema?
> 3. Quantos slides, ou quanto tempo de fala?
> 4. Você vai falar por cima dos slides, ou a pessoa vai ler sozinha depois?
> 5. Tem identidade visual sua (cor, fonte, logo)? Se não tiver, eu uso o padrão neutro.
> 6. Quais arquivos você precisa no fim: HTML navegável, PDF, PNGs, PPTX fiel, PPTX editável?

**As respostas dela:**

1. Objetivo é que o corredor entenda que comer mal antes da prova custa mais tempo do que treinar
   errado. Plateia: 80 corredores amadores, a maioria acima dos 35.
2. Existe, está nas anotações que já mandei.
3. 25 minutos de fala.
4. Vou falar por cima. Mas eles vão mandar o material depois pra quem foi.
5. Não tenho. Usa o padrão.
6. HTML e PDF. PPTX não precisa.

**Premissa declarada em 1 linha:** "sem identidade sua, vou no padrão neutro (fundo escuro, texto
grande, um acento de cor); se você tiver uma cor de marca depois, eu troco em um minuto".

## 3 · A decisão de densidade

Resposta 4 diz fala, resposta 4 também diz que o material circula depois. Os dois modos aparecem no
mesmo pedido, então vale a régua do modo dominante: **guiada pela fala**, porque é ao vivo e o
material que circula depois é o PDF, não a razão de existir do deck. Uma ideia por slide, headline
grande, no máximo 3 pontos.

Consequência declarada ao dono em 1 linha: "os slides vão ficar enxutos porque você fala por cima;
se você quiser que eles se expliquem sozinhos no PDF, eu engordo o texto, mas aí eles competem com
você no palco".

## 4 · O arco, 12 slides pra 25 minutos

| # | Tela (a ideia dominante) | Tipo |
|---|---|---|
| 1 | Você treina 6 dias e come mal 7. | Headline |
| 2 | O que acontece nos 40 minutos antes da largada. | Transição |
| 3 | 3 erros aparecem em 8 de cada 10 fichas que eu leio. | Número |
| 4 | Erro 1: café preto no lugar de comida. | Headline |
| 5 | Erro 2: gel de carboidrato estreado no dia da prova. | Headline |
| 6 | Erro 3: água demais na hora errada. | Headline |
| 7 | Nenhum dos três é sobre disciplina. É sobre horário. | Transição |
| 8 | A janela de 3 horas, 1 hora e 15 minutos. | Sequência simples |
| 9 | O que comer em cada uma das três janelas. | Recurso: tabela |
| 10 | O teste que você faz no treino longo, nunca na prova. | Headline |
| 11 | Antes e depois de um corredor que ajustou só o horário. | Recurso: comparação `[A CONFIRMAR]` |
| 12 | Escolha uma janela e teste sábado. | Fechamento |

O slide 11 nasceu marcado `[A CONFIRMAR]`: ela citou o caso na fala, mas não tinha o número na mão.
Ficou marcado na tela e no aviso ao dono, e não foi preenchido com um valor plausível.

Dos 12 slides, 2 usam recurso didático (o 9 e o 11). Os outros 10 são base. Fica dentro da régua de
80% base e 20% recurso.

## 5 · O STOP de aprovação do master

Depois de produzir o `deck.html`, antes de qualquer export:

> "Esse é o deck, 12 slides, dá uns 2 minutos por slide nos seus 25. O que ajusto antes de eu gerar
> os arquivos?"

**O que ela pediu:** juntar os slides 4, 5 e 6 num só, porque os três erros ela fala rápido. E o
número do slide 3 estava errado, é 7 de cada 10.

Resultado: o deck foi pra 10 slides e o número foi corrigido no master, antes do export. Sem esse
STOP, os quatro formatos teriam sido gerados de um deck com um número errado e três slides a mais.

## 6 · O export

```bash
node scripts/export-deck.mjs ./deck-corrida/deck.html --format=pdf,png --out=./deck-corrida/saida
python3 scripts/make_mosaic.py ./deck-corrida/saida/deck-png ./deck-corrida/saida/MOSAICO.png
```

PPTX não foi gerado, porque a resposta 6 disse que não precisava. Gerar formato que ninguém pediu
enche a entrega e confunde quem recebe.

## 7 · O crivo visual (com leitor de imagem)

> Abri o `MOSAICO.png` e depois os slides suspeitos em tamanho cheio.
>
> - Contei 10 PNGs, todos em 1920x1080. O PDF saiu com 10 páginas em 16:9.
> - Slide 4 (os três erros fundidos): as três linhas ficaram apertadas contra o rodapé. Reduzi a
>   headline um degrau e respirei o bloco.
> - Slide 7 (a tabela das janelas): a última coluna estava cortada na borda direita. Estreitei as
>   três colunas e a tabela coube.
> - Slide 9: o marcador `[A CONFIRMAR]` está visível na tela, como tem que estar, pra ela não
>   apresentar um número que ainda não confirmou.
> - Os outros 7 passaram limpos. Nenhuma sobreposição, nenhuma margem fora do padrão.
>
> Corrigi o master e reexportei o PDF e os PNGs. Conferi o mosaico de novo: passou.

## 8 · A entrega

- `MOSAICO.png`, primeiro, pra ela aprovar de uma olhada.
- `deck.html`, navegável por teclado, é o que ela abre no palco.
- `deck.pdf`, 10 páginas, é o que o evento manda pra quem foi.
- `deck-png/slide-01.png` a `slide-10.png`.

Fechamento em uma frase: "está pronto pra apresentar. Falta só o número do caso do slide 9: me manda
que eu troco em um minuto e reexporto".

---

## O que muda nas outras duas ações

**Ação 2 · REDESENHO.** O dono manda o deck que já tem (aqui, imagine um PDF de 18 slides cheios de
caixas). A skill extrai o texto slide a slide, devolve a lista do que leu e **para**, porque ler
errado o deck antigo contamina tudo que vem depois. Depois pergunta o que incomoda. Se a resposta é
"está feio", o arco fica e a tela muda. Se a resposta é "está confuso", o arco também é refeito: 18
slides viram 11, três slides repetidos são fundidos, dois slides entupidos são divididos, e a
entrega leva uma tabela curta dizendo o que mudou e por quê.

**Ação 3 · EXPORT.** O deck já existe e já foi aprovado. A skill confere que o HTML abre com o palco
de 1920x1080, roda os comandos dos formatos pedidos, faz o crivo no mosaico e entrega. Quando os dois
PPTX foram gerados, fecha com a frase que diz a diferença: "o fiel é idêntico ao que você viu, mas
cada slide é uma imagem e não dá pra editar; o editável dá pra mexer no texto, mas fonte e quebra
podem sair um pouco diferentes".

## O que este exemplo prova sobre o fluxo

1. As 6 perguntas de uma vez só cabem numa mensagem e evitam a entrevista longa.
2. Quando o pedido mistura fala e leitura, declarar o modo dominante e a consequência em 1 linha
   evita o deck que não serve pra nenhum dos dois.
3. O STOP antes do export é o passo que mais economiza: aprovar o master custa uma mensagem, refazer
   quatro formatos custa a rodada inteira.
4. O crivo visual encontrou dois problemas de tela que o código não denunciava. Arquivo que existe
   não é arquivo que está certo.
