# Receita: o número vira imagem mostrando o próprio valor (blocos)

Serve pra dinheiro e pra contagem grande que o roteiro traz e que, escrito sozinho, não entra na cabeça (regra 6 do guia). O pictograma de blocos mostra quanto vale o número, com uma régua que a sala lê de uma vez. Ponto de partida: `assets/receitas/numero-pictograma.html`; troque a figura pelo bloco.

## A régua

1. **Escala única, declarada na tela.** Um bloco vale uma unidade redonda, escrita na legenda: `1 bloco = R$1 milhão` pra dinheiro, `1 bloco = 1.000 vendas` pra contagem. Escolha a unidade que deixa o maior número do deck em até 50 blocos. A mesma unidade vale pra todos os slides do mesmo tipo de número.
   Contagem unitária de vários itens (por exemplo, 27 skills inclusas): `1 bloco = 1 [item]` vale, com um bloco por item e no máximo 50. Declare no `escala-desenho.md` como qualquer unidade.
2. **Mesmo tamanho de bloco em todos os slides da escala.** O lado do bloco (por exemplo 76px) é o mesmo no slide com 1 bloco e no slide com 46. Número maior ganha mais blocos, nunca um bloco maior. Slide com bloco único não pode usar um bloco gigante: ele mentiria a escala.
3. **A fração vem pintada dentro do bloco.** Metade do valor é um bloco meio pintado, com contorno de 4px no bloco inteiro pra se ver o que falta. O resto vem em blocos cheios, em fileiras de dez.
4. **O número continua escrito, grande, como rótulo ao lado.** A imagem mostra o tamanho; o rótulo diz o valor exato, com o rótulo do roteiro (gerenciou, faturou).
5. **A legenda da escala tem 30px ou mais** (o piso único), na cor de texto, nunca apagada.
6. **Um valor por slide; dois só quando o roteiro os junta.** Dois dados que o roteiro põe lado a lado na mesma fala (gerenciou e faturou; pessoas e reais) ficam no mesmo slide, cada um na sua fileira, com o rótulo do roteiro, a unidade na legenda e no `escala-desenho.md` (uma legenda por escala) e o mesmo lado de bloco nas duas (a regra 2 vale por escala e entre elas); a mesma unidade em dois cases (R$10,6 milhões e R$3 milhões) vale igual. Dados que o roteiro separa (um case por fala) ficam cada um no seu slide. Em nenhum caso entra proporção entre eles, na fala ou na tela. Se o dono encadeia os números (funil), a sequência dele vale, etapa por etapa; a relação que você calcularia (quantos compram, o ticket) nunca vai à tela. Preço (R$3.500, R$154,62) e razão (ROAS 2,2) não viram bloco: a escala é de dinheiro e contagem grandes, e R$3.500 na escala de R$1 milhão seria 0,0035 bloco. Ficam em número grande, com o rótulo do roteiro.
7. **Sem o número no roteiro, não tem bloco.** Vale a condição de entrada de `receitas-visuais.md`.
8. **Cor:** as duas cores de destaque e o neutro. Dívida e perda não ganham uma cor própria (a cor reservada não é pra isso); a legenda diz o que é.
9. **Percentual:** pinte a fração dentro de um bloco ou de uma fileira inteira (40% é 4 de 10 células), com o % escrito ao lado. A base é a que o roteiro diz ("dos inscritos"); se ele não diz, a fração vai sem base escrita e a base vira pergunta no `_operador.md`.
10. **Número único de história** (sem comparação nem escala entre slides): vira bloco só se o roteiro traz o número e a unidade o deixa em mais de um bloco. A legenda da escala é permitida só se estiver declarada em `escala-desenho.md`, e conta como rótulo do desenho, não como número novo. Se só um slide usa a escala, o texto simples (o número grande com o rótulo do roteiro) basta; havendo bloco, o lado é o de sempre (76px), nunca gigante.

## O arquivo da escala: `trabalho/escala-desenho.md`

A legenda "1 bloco = R$1 milhão" não existe no roteiro do dono. O `conferir_fontes.py` procura todo número da tela no insumo e reprova essa legenda por falta de fonte. A unidade é regra do desenho, como a régua de um gráfico, e não dado do dono. Declare num arquivo à parte, sem afirmar nada sobre o negócio:

```
# Escala do desenho (régua do designer, não é dado do dono)

Estes valores são a unidade dos pictogramas de blocos. Não afirmam nada sobre o negócio do dono.

- Dinheiro, slides [lista]: 1 bloco = [unidade] (EXEMPLO: R$1 milhão)
- Contagem, slides [lista]: 1 bloco = [unidade] (EXEMPLO: 1.000 vendas)
- Contagem unitária, slides [lista]: 1 bloco = 1 [item] (EXEMPLO: 1 bloco = 1 skill)
- Tamanho na tela: o bloco tem [N]px de lado em todos os slides da escala.
```

Pode ficar em `trabalho/escala-desenho.md` (ou na pasta dos slides). O `montar_desenho.py` lê esse arquivo sozinho quando há `--insumo` e avisa na primeira linha da saída. Para rodar a conferência de fontes à mão, passe os dois arquivos:

```
python3 scripts/conferir_fontes.py --entrega trabalho/deck/notas.md --insumo trabalho/roteiro.md trabalho/escala-desenho.md
```

O arquivo só aceita unidades. Valor do negócio nunca entra nele: o número do dono sempre vem do roteiro. Sem o arquivo, o deck reprova só nas linhas da legenda, e mais nada.

## O que olhar no PNG

- O bloco tem o mesmo tamanho aqui e nos outros slides da escala?
- A fração pintada bate com o número (um terço pintado vale um terço)?
- A legenda se lê no celular, sem esforço?
- O olho entende o tamanho antes de ler o rótulo?
- Alguma barra, forma ou foto do slide é maior que o bloco da escala e pode confundir? Se sim, tire ou reduza.

## Limite conhecido

Bloco pequeno lê como ícone antes de ler como imagem. Número pequeno (uma fração de um bloco): só o número em fonte grande, como na regra 10, e diga isso no `_operador.md`.
