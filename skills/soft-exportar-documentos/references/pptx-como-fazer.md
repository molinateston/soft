# PowerPoint (.pptx): as rotas, o que corrompe o arquivo e o trabalho com template

Um `.pptx` também é arquivo compactado com XML dentro, um XML por slide. As armadilhas aqui são piores que as do Word porque muitas corrompem o arquivo em silêncio: a biblioteca escreve, o validador passa, outros programas abrem, e só o PowerPoint recusa.

## Escolha da rota

| Tarefa | Rota |
|---|---|
| **Criar** deck novo, com gráfico nativo e imagem | `pptxgenjs` (Node) |
| **Criar** deck simples, ou editar em Python | `python-pptx` |
| **Preencher** um template que o dono mandou | descompactar, editar `ppt/slides/slideN.xml`, recompactar |
| **Ler** o conteúdo | `markitdown deck.pptx`, ou o mosaico com `scripts/pptx/thumbnail.py` |

## O que corrompe o arquivo (o mais importante desta página)

- **Cor sem o sinal de cerquilha e sem transparência embutida.** Cor de seis dígitos, só isso. Cerquilha na frente ou oito dígitos com transparência embutida corrompem o arquivo. Pra transparência existe propriedade própria, separada.
- **Deslocamento de sombra nunca negativo.** Pra sombra pra cima, use ângulo de 270 graus com deslocamento positivo.
- **Rótulo de valor em barra empilhada** só aceita as posições internas (centro, ponta interna, base interna). A posição externa corrompe o arquivo.
- **Gráfico com segundo eixo** precisa que os dois conjuntos de eixos estejam declarados nas opções, dois de cada. Declarar só um faz a biblioteca escrever referência a eixo que ela nunca criou, e o PowerPoint descarta o gráfico e chama o arquivo de corrompido.
- **Nunca reordene os elementos de dentro da declaração da apresentação.** A ordem em que a biblioteca escreve funciona; mover um elemento de lugar torna o mesmo deck impossível de abrir.
- **Transformando XML em script:** use um leitor de XML que preserva os prefixos de espaço de nome. O leitor padrão de Python reescreve os prefixos ao salvar, e isso quebra o deck.

## Armadilhas que não corrompem, mas estragam

- **Defina o tamanho da tela ANTES de somar slide.** O padrão é menor do que a maioria espera; coordenada fora da borda é escrita, não ajustada, e a forma simplesmente não aparece.
- **A biblioteca de Node altera o objeto de opções que você passa.** Nunca reaproveite o mesmo objeto de sombra ou de opções em duas chamadas; monte um novo a cada vez.
- **Lista:** ligue a propriedade de marcador em cada item, nunca escreva o caractere. Um item por parágrafo, nunca vários concatenados. Espaçamento entre itens pela propriedade de espaço depois do parágrafo, não pela altura de linha (que abre buracos enormes).
- **Uma instância de apresentação por arquivo de saída.** Nunca reaproveite.
- **Caixa de texto tem margem interna própria.** Zere a margem quando o texto precisa alinhar com uma forma ou linha na mesma coordenada.
- **Nota do apresentador** vai no campo de notas do slide, nunca numa caixa de texto escondida fora da área visível.
- **Gráfico nativo, não imagem de gráfico.** O que o PowerPoint sabe desenhar, desenhe com o recurso nativo; imagem só pros tipos que ele não tem.
- **Gráfico sai cru no padrão:** sem título, sem rótulo de valor, com paleta velha. Ligue título, rótulos e a sua paleta, e limpe a moldura (linha de grade discreta, legenda fora quando é uma série só).

## Template: a ordem certa de trabalhar

1. **Veja os layouts primeiro.** `python3 scripts/pptx/thumbnail.py template.pptx template-mosaico` monta um mosaico numerado de todos os slides. **Sempre passe o segundo argumento com o nome do deck**: sem ele o nome padrão se repete, e dois templates na mesma pasta apagam o mosaico um do outro sem avisar.
2. **Todo o trabalho de estrutura vem antes de todo o trabalho de conteúdo.** Somar, apagar e reordenar slide primeiro; escrever o texto depois. `scripts/pptx/add_slide.py` copia o slide como está, então duplicar depois de editar clona o conteúdo editado; e `scripts/pptx/clean.py` apaga qualquer slide que não esteja na lista oficial, inclusive um que você acabou de escrever.
3. **Nunca copie um arquivo de slide na mão.** `scripts/pptx/add_slide.py desempacotado/ slide2.xml --after slide5.xml` faz todo o registro que um slide novo precisa e imprime o que criou. Rodando direto sobre o arquivo, passe a saída explícita ou ele reescreve o deck de entrada por cima.
4. **Slide duplicado aponta pro mesmo gráfico do original**, não faz uma cópia. Editar o gráfico de um muda o do outro.
5. **Vaga do template não é item do seu conteúdo.** Se o template mostra 4 caixas e você tem 3, apague o grupo inteiro da quarta (imagem e texto), não só o texto dela. Depois procure o que ficou órfão na conferência visual.
6. Depois de apagar slide, rode `python3 scripts/pptx/clean.py desempacotado/` pra remover slide, mídia e vínculo que ninguém mais usa.
7. Valide sempre com o original como base: `python3 scripts/office/validate.py saida.pptx --original template.pptx`. O template pode ter erro próprio de esquema, e sem essa base os erros dele aparecem como se fossem seus, escondendo o que você quebrou de verdade.

**Se você usar `python-pptx`**, três coisas ela não faz: duplicar slide (só cria a partir de layout), preservar formatação quando você troca o texto do quadro inteiro de uma vez (isso achata tudo num pedaço sem estilo; troque pedaço por pedaço), e ler os desenhos vetoriais que a maior parte dos templates usa.

**Arquivo `.ppt` antigo** precisa ser convertido primeiro: `python3 scripts/office/soffice.py --headless --convert-to pptx arquivo.ppt`.

## Fonte e a conferência que mente

A fonte que você escreve no arquivo é desenhada pelo programa de quem abre, não por aqui. A conferência local substitui a fonte que não tem, e algumas substitutas têm largura diferente, então o texto que parece caber na conferência pode estourar no computador do cliente, e o contrário também.

- **Fontes seguras** (largura fiel na conferência e presentes em qualquer instalação de escritório): Arial, Calibri, Cambria, Times New Roman, Courier New. Use essas no corpo e em tudo que depende de caber.
- **Fonte com personalidade sem risco:** um título em serifada da lista segura com corpo em sem-serifa da lista segura.
- **Fonte que o dono pediu e está fora da lista:** use onde ele pediu, deixe uns 10 por cento de folga na caixa, e não confie na conferência de encaixe daquele elemento.
- **Nunca use a fonte padrão nova do pacote de escritório** como escolha automática: não tem substituta de mesma largura aqui, e falta nas instalações mais antigas, então falha nas duas pontas.

| Elemento | Tamanho |
|---|---|
| Título do slide | 36 a 44, negrito |
| Título de seção | 20 a 24, negrito |
| Corpo | 14 a 16 |
| Legenda | 10 a 12, cinza |

## Desenho: o que evitar porque tem cara de gerado por máquina

- Linha de acento embaixo do título. Use espaço em branco ou fundo de cor.
- Barra ou faixa de cor decorativa: no topo, na lateral, na borda de um cartão. Pra destacar um cartão, use fundo levemente tingido, sombra ou ícone.
- Todo slide com o mesmo layout. Varie coluna, cartão e destaque.
- Slide só de texto. Todo slide leva imagem, ícone, gráfico ou forma.
- Corpo de texto centralizado. Centralize título; alinhe parágrafo e lista à esquerda.
- Fundo bege ou creme por padrão. Sem instrução, use branco ou a paleta do dono.
- Texto estourando a caixa. Diminua a fonte, divida em dois slides ou aumente a caixa; nunca entregue cortado.

## Sem nenhuma biblioteca de deck na máquina

Entregue o roteiro em `.md`, slide a slide, com título e conteúdo de cada tela, e diga em uma linha: falta `python-pptx` pra gerar o arquivo; o roteiro está pronto e vira deck com um comando assim que a biblioteca existir.
