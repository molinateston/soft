# Planilha (.xlsx e .csv): fórmula viva, recálculo e o que sobrevive

A diferença entre uma planilha e uma tabela impressa é que a planilha recalcula. Quem recebe uma planilha espera mexer num número e ver os outros mudarem. Uma planilha com resultados fixos digitados por dentro parece igual e é inútil.

## Escolha da rota

| Tarefa | Rota |
|---|---|
| **Criar** ou **editar** com fórmula e formatação | `openpyxl` |
| **Despejar** muito dado de uma vez | `pandas` |
| **Espiar** o que tem dentro | `markitdown arquivo.xlsx` (uma seção por aba, sem coordenada de célula, então não planeje edição por ele) |
| **Ler** um modelo com fórmula E valor | duas leituras separadas, veja abaixo |

## As exigências de toda planilha que sai daqui

- **Fonte profissional** (Arial ou Times New Roman) no arquivo todo, salvo pedido em contrário.
- **Zero erro de fórmula.** Nunca entregue enquanto o recálculo apontar erro. Se você acha que o erro já existia antes de você, prove: abra o arquivo original lendo os valores guardados e olhe aquela célula. Erro que você criou é idêntico a erro que você herdou.
- **Fórmula, nunca resultado digitado.** Escreva a soma como fórmula, não o total que você calculou por fora.
- **Siga a especificação do dono ao pé da letra.** Nome exato de aba, cabeçalho exato de coluna, a fórmula que ele soletrou. Redesenho que calcula outra coisa falha, por mais elegante que seja.
- **Documente toda premissa e todo número fixo** onde o leitor vê: um comentário na célula, ou uma célula ao lado no fim da tabela. Cite a fonte real quando existir; quando o número veio do dono, escreva isso.
- **Planilha pra alguém preencher** leva uma legenda curta dizendo quais células editar, e uma linha de exemplo com valores realistas mostrando o formato esperado. Nunca acrescente essa linha de exemplo num arquivo que você foi chamado pra editar.
- **Editando arquivo que já existe: as convenções dele mandam**, acima de qualquer regra desta página. Ache primeiro as células de entrada (marcadas por cor de fonte, preenchimento ou sombreado diferente), escreva só nelas, e não encoste em nenhuma fórmula existente.

## Recálculo (obrigatório sempre que houver fórmula)

A biblioteca escreve fórmula como texto, sem valor guardado. Até recalcular, toda célula de fórmula é lida como vazia por qualquer coisa que leia valores guardados: outras bibliotecas, o próprio leitor de valores, e a maioria dos visualizadores.

```bash
python3 scripts/xlsx/recalc.py saida.xlsx [segundos_de_limite]   # padrão 30
```

O LibreOffice calcula tudo, o arquivo é reescrito no lugar, e você recebe um JSON: situação (sucesso ou erros encontrados), total de fórmulas, total de erros, e um resumo nomeando até 100 células por tipo de erro (um campo diz quantas ficaram de fora da lista; confie no total, não no tamanho da lista). Conserte o que ele nomear e rode de novo.

**Duas leituras importantes da saída:**
1. **JSON com chave de erro em vez de situação significa que nada foi recalculado.** Só esse caso sai com código diferente de zero. "Erros encontrados" sai com código zero, então saída limpa do comando nunca prova planilha limpa: leia o JSON.
2. **Recálculo verde prova que a fórmula roda, não que ela está certa.** Um intervalo com uma linha a mais ou a menos gera arquivo limpo com número errado. Escreva 2 ou 3 fórmulas primeiro e confira que elas puxam o valor que você esperava, antes de estender pra grade inteira.

**Planilha que puxa dado de outro arquivo perde esses vínculos** se você reescrever e recalcular. A fórmula desse tipo aponta pra um arquivo separado no disco, que quase nunca está aqui; o valor guardado é a única coisa segurando aquele dado. A biblioteca apaga o valor guardado ao salvar, o LibreOffice tenta resolver o vínculo de verdade, falha, escreve erro de nome e apaga todos os vínculos. O script se recusa a rodar nesse estado: copie os valores dessas células pra fora do original antes de salvar por cima (existe uma opção de forçar, que aceita a perda).

## Fórmula que sobrevive à conferência

O LibreOffice implementa menos funções que o Excel, e uma que ele não consegue calcular vira um erro de nome gravado dentro do arquivo que você entrega.

- **Prefira as funções clássicas**, que não precisam de prefixo nenhum: soma condicional com vários critérios, índice, correspondência, tratamento de erro, soma de produtos.
- **Seis funções mais novas funcionam, mas só com o prefixo interno**, porque a biblioteca grava sua fórmula no XML exatamente como você escreveu, e o Excel guarda os nomes novos com prefixo (a interface esconde isso): junção de texto, concatenação nova, condicional múltipla, seleção por caso, máximo e mínimo condicionais. Escritas sem o prefixo, cada uma vira erro de nome.
- **Nunca use as funções de matriz derramada** (busca nova, correspondência nova, ordenação, filtro, valores únicos, sequência). O LibreOffice daqui não avalia nenhuma delas sob prefixo algum. Onde avalia, elas derramam por várias células, e um arquivo escrito por biblioteca não tem a marcação de derrame, então só a célula de cima recebe valor, e o recálculo relata zero erro sobre um resultado truncado. Use índice com correspondência pra busca, e ordene, filtre e tire duplicata em Python antes de escrever as células.
- Fórmula que o LibreOffice não conseguiu interpretar é regravada em minúsculas: é a pista rápida ao lado de um erro de nome.

## Armadilhas da biblioteca

- **Ler um modelo exige duas leituras.** Uma opção devolve os valores guardados sem as fórmulas; o padrão devolve as fórmulas sem os valores. Uma leitura só não dá as duas coisas.
- **A leitura de valores é destrutiva se você salvar.** Aquela versão do arquivo não tem mais fórmula nenhuma, então salvar troca cada fórmula por um número fixo, pra sempre.
- **Ler valores de um arquivo recém-escrito devolve vazio em tudo:** recalcule primeiro. (Fórmula cujo resultado é texto vazio também é lida como vazia.)
- **Célula mesclada: escreva só na do canto superior esquerdo.** As outras são somente leitura.
- **Planilha com macro perde as macros** se você não pedir explicitamente pra preservá-las na abertura.
- **Nome de aba com espaço precisa de aspas** na referência entre abas, ou a fórmula vira erro de valor.

## Modelo financeiro (quando o dono não pedir outra coisa)

**Cor:** texto azul para número digitado e alavanca de cenário · preto para fórmula · verde para vínculo com outra aba · vermelho para vínculo com outro arquivo · preenchimento amarelo para premissa importante e célula que o usuário deve preencher.

**Números:** moeda com separador de milhar e a unidade nomeada no cabeçalho da coluna · zero renderizado como traço, inclusive em porcentagem · negativo entre parênteses · porcentagem guardada como fração (quinze centésimos rendem quinze por cento; guardar quinze rende mil e quinhentos) · múltiplo com o "x" no formato · ano como texto, nunca com separador de milhar.

**Estrutura:** cada premissa na própria célula rotulada, referenciada pelas fórmulas que a usam, nunca o número solto dentro da conta · fórmula idêntica ao longo de todos os períodos projetados, porque uma célula editada sozinha no meio da linha é o erro silencioso mais comum · proteja todo denominador que pode chegar a zero.

## Sem `openpyxl` na máquina

Entregue `.csv`, que sai de qualquer lugar com a biblioteca padrão de Python, e diga em uma linha: sem `openpyxl` a planilha vai como texto separado por vírgula; fórmula, formatação e aba múltipla ficaram de fora, e o arquivo vira `.xlsx` completo assim que a biblioteca existir. Escreva o `.csv` com o separador que o programa de planilha do dono espera (no Brasil o ponto e vírgula costuma abrir melhor) e diga qual você usou.
