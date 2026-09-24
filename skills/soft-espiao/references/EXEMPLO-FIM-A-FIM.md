# EXEMPLO FIM A FIM (caso inventado)

**Tudo aqui é fictício:** o dono, o nicho, as páginas, os números e os links. Serve pra mostrar a forma da entrega, do pedido ao brief. Nenhum dado deste arquivo vale como régua.

## 1. O pedido

> "Dou aula de violão online pra adulto que nunca tocou. Quero saber o que está vendendo nesse nicho e o que eu faço de anúncio."

Roteamento: "o que está vendendo" + "o que eu faço" = Ação 1 (Radar) seguida da Ação 4 (Modelagem).

## 2. A pergunta (uma mensagem, 3 itens)

> "Pra achar o que vende no teu nicho: (1) qual o teu produto e o preço? (2) que frase o teu aluno usa quando te procura? (3) onde ele passa o tempo, e que idade tem? Responde o que souber, o resto eu marco."

Resposta: curso gravado de 8 semanas, R$ 297; "acho que meus dedos já não aprendem mais"; 35 a 55 anos, Facebook e Instagram.

O dono não conhecia concorrentes pelo nome, então a busca começa por palavra.

## 3. Termos (R1)

| Busca | Famílias |
|---|---|
| `erro violao` | mercado + nicho |
| `metodo violao` | mercado + nicho |
| `adulto violao` | nicho + nicho (a palavra do público) |
| `dedos violao` | a frase do aluno + nicho |

## 4. Coleta (R2)

```
test -n "$APIFY_TOKEN" && echo token: ok || echo token: ausente
python3 scripts/buscar_anuncios.py --termo "erro violao" --termo "metodo violao" --termo "adulto violao" --termo "dedos violao" --max 20 --saida planilha-violao.csv
```

Última linha colada: `anuncios na planilha: 52 · vendendo: 3 · candidato: 6 · observar: 43`

## 5. Ruído e pontos (R3 e R4)

Sete anúncios de loja de instrumento vieram pela palavra "violão" e ganharam `fora do eixo: venda de instrumento` na nota.

Trecho da planilha (colunas principais):

| data_coleta | pagina | dias_no_ar | copias | paginas_mesmo_texto | versoes_da_pagina | pontos | classe |
|---|---|---|---|---|---|---|---|
| 2026-03-10 | Página A (fictícia) | 22 | 11 | 1 | 4 | 3 | vendendo |
| 2026-03-10 | Página B (fictícia) | 64 | 8 | 2 | 3 | 4 | vendendo |
| 2026-03-10 | Página C (fictícia) | 15 | 7 | 1 | 3 | 3 | vendendo |
| 2026-03-10 | Página D (fictícia) | 210 | 1 | 1 | 1 | 1 | observar |

A Página D está no ar há 7 meses com 1 cópia só: tempo no ar sozinho, fica em observação.

## 6. Técnica ou personalidade (R5)

- Página A: professor sem audiência fora do nicho, 4 versões rodando. Técnica.
- Página B: canal com 900 mil inscritos e pouca mídia paga no resto do ano. Personalidade: sai da modelagem, fica como estudo.
- Página C: técnica.

## 7. Trecho do Radar (R7)

> **O que está vendendo agora**
> **Página A (fictícia)** · https://www.facebook.com/ads/library/?id=0000000000000001 · início 16/02 · 22 dias
> 11 cópias · 4 versões · 22 dias · 3 pontos · técnica
> Por que funciona: abre culpando o método e tira a culpa da idade do aluno, que é a objeção que ele traz pronta.
>
> **O padrão que se repete:** A e C abrem com a mão do professor em close e uma afirmação que contraria a crença da idade; os dois levam pra aula gratuita, não direto pro checkout.
>
> **A linguagem do público:** "dedo duro", "comecei tarde", "empaquei no F" (comentários da Página C; entra aqui como citação do público, e o dono escreve a frase dele a partir disso).

## 8. Ficha de engenharia reversa da Página A (Ação 3, resumida)

```
Gancho citado para estudo: "Se você tem mais de 40 e acha que seus dedos não aprendem..."
```

- Ângulo: medo de ter passado da idade.
- Gancho: close da mão, afirmação que contraria a crença.
- Formato: professor falando pra câmera, 58 segundos.
- Estrutura invisível: identificação · culpa transferida pro método · mecanismo da solução com nome · prova com aluno · chamada pra aula.
- Oferta: aula gratuita, depois curso. Preço `não visível`.
- Página e funil: página de captura, aula gravada, checkout.
- Princípio: tirar a culpa do aluno e pôr no método abre espaço pra um método novo.

## 9. Brief de modelagem (Ação 4)

- Referência: Página A · coletado em 10/03 · 3 pontos (cópias 1, versões 1, tempo 1).
- Princípio: tirar a culpa da idade e pôr no jeito de ensinar.
- Nível: estudiosa, porque a estrutura é o que rende e o gancho dele não serve na boca do dono.
- Leva: a ordem identificação, culpa no método, mecanismo, prova, chamada. O formato de close da mão.
- Fica de fora: a frase de abertura, o nome do método dele, o aluno dele.
- Ganchos na voz do dono:
  1. "Dedo duro aos 50 tem conserto, e começa pela mão esquerda parada."
  2. "Você não começou tarde. Te ensinaram na ordem de quem tinha 12 anos."
  3. "Três acordes bastam pra tua primeira música inteira. O resto vem depois."
- Prova do dono: [A CONFIRMAR: depoimento de aluno acima de 40, com autorização]
- CTA: "clica e vê como funcionam as 8 semanas do curso" (produto informado pelo dono na pergunta 1).
- Distância, com o script: `sequencias de 5 palavras iguais a referencia: 0` (exit 0).
- Próximo passo: soft-criativo-campeao instalada, então o lote de anúncios sai por ela com este brief.

## 10. Gate colado

```
1 sim · 2 sim · 3 sim · 4 sim · 5 sim · 6 sim · 7 sim · 8 sim · 9 sim (1 campo em [A CONFIRMAR]) · 10 sim · 11 sim · 12 sim
radar-violao.md: exit 0
brief-1.md: exit 0
arquivos linteados: 2 · exit 0: 2
```

## 11. O relato ao dono

```
Pronto: Radar do violão com 3 anúncios que dão sinal de venda e 1 brief pra modelar.
Abra primeiro: radar-violao.md
Falta você responder: a pergunta abaixo
O brief usa só a sua história de aluno adulto; o depoimento entra quando houver autorização.

Perguntas pra você
1. Tem aluno acima de 40 que autoriza depoimento com nome?
```
