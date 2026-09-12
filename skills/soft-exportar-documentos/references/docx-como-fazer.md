# Word (.docx): as rotas, as armadilhas e a edição

Um `.docx` é um arquivo compactado com XML dentro. Isso explica quase tudo que dá errado: o programa que gerou o arquivo escreveu XML, e o Word é exigente com esse XML de um jeito que nenhum outro leitor é.

## Escolha da rota

| Tarefa | Rota |
|---|---|
| **Criar** documento novo, com controle fino | biblioteca `docx` de Node, ou `python-docx` |
| **Criar** rápido, sem exigência de estilo | `pandoc -f markdown -t docx entrada.md -o saida.docx` |
| **Editar** documento que já existe | descompactar, editar `word/document.xml`, recompactar |
| **Ler** o conteúdo | `pandoc -t markdown arquivo.docx` |

A biblioteca de criação não abre arquivo existente. Editar é sempre o caminho do XML.

## Armadilhas ao criar do zero

Valem nas duas bibliotecas, com nomes diferentes de propriedade:

- **Tamanho de página.** O padrão costuma ser A4. Carta (padrão dos EUA) tem outra medida; declare o tamanho em vez de torcer.
- **Tabela precisa de largura nas duas pontas.** Largura declarada na tabela E em cada célula, na mesma unidade absoluta. Largura em porcentagem quebra quando o arquivo é aberto em outro editor. A soma das colunas tem que bater com a largura da tabela.
- **Fundo de célula:** use o preenchimento sólido claro, não o tipo que renderiza preto em alguns leitores.
- **Lista:** nunca escreva o caractere de marcador na mão. Use a numeração nativa, com o nível configurado como marcador. Marcador digitado vira marcador duplo.
- **Imagem** precisa do tipo declarado (png, jpg).
- **Quebra de página** mora dentro de um parágrafo, não solta.
- **Nunca use quebra de linha dentro de um parágrafo** pra separar ideias. Um parágrafo por ideia.
- **Sumário automático** só enxerga títulos com o estilo nativo de título. Estilo de título inventado por você precisa do nível de tópico declarado, ou não aparece no sumário.
- **Linha horizontal:** use borda inferior de parágrafo, nunca uma tabela de uma linha fingindo ser régua.
- **Texto alinhado à direita na mesma linha** (número de página, valor de item): use a tabulação posicional com preenchimento de pontos, nunca pontos ou espaços digitados.

## Editar um arquivo que chegou

```bash
unzip -q documento.docx -d desempacotado/
find desempacotado -type l -delete          # arquivo de fora nunca é confiável
python3 scripts/docx/merge_runs.py desempacotado/
# edite desempacotado/word/document.xml, sem reformatar nem indentar
(cd desempacotado && rm -f ../saida.docx && zip -Xr ../saida.docx .)
python3 scripts/office/validate.py saida.docx --original documento.docx
```

**Por que o `merge_runs.py` vem antes de tudo:** o Word parte o texto em muitos pedaços (marcas de revisão, correção ortográfica), então a frase que você lê na tela quase nunca existe inteira e contígua no XML. Procurar por ela sem juntar os pedaços não acha nada, e você conclui errado que o texto não está lá. O script junta pedaços vizinhos de mesma formatação, sem mudar uma vírgula do conteúdo nem do desenho. Ele também aceita o `.docx` direto: `python3 scripts/docx/merge_runs.py documento.docx -o juntado.docx`.

**Recompacte de dentro da pasta**, e apague o arquivo de saída antes, ou pedaço que você removeu sobrevive dentro do novo arquivo.

**Arquivo `.doc` antigo** (formato anterior) precisa ser convertido primeiro: `python3 scripts/office/soffice.py --headless --convert-to docx arquivo.doc`.

## Marcação de revisão (o "controle de alterações")

Quando o dono pede sugestão marcada, e não texto substituído:

- Envolva o que entra na marca de inserção e o que sai na marca de exclusão, cada uma com identificador, autor e data.
- Dentro da marca de exclusão, o elemento de texto tem nome próprio, diferente do texto normal. Trocar um pelo outro faz o Word ignorar a marca.
- Apagar um parágrafo inteiro é duas coisas: marcar a exclusão de cada pedaço de texto, e marcar a exclusão da própria marca de fim de parágrafo (que significa "junta este parágrafo com o de baixo"). Faltando a segunda, sobra um parágrafo vazio na versão aceita, que aparece como marcador solto numa lista.
- A ordem dos elementos dentro das propriedades é exigida pelo esquema. A marca de exclusão vem antes dos irmãos dela.
- Valide com `python3 scripts/office/validate.py saida.docx --original entrada.docx --author "<o nome que você usou>"`. Ele aponta todo texto que você mudou sem marcar, que é fácil de fazer sem perceber e invisível na visualização final.
- Pra entregar uma cópia limpa com tudo aceito: `python3 scripts/docx/accept_changes.py entrada.docx saida.docx`.

## Comentários

Comentário no Word é seis arquivos internos cruzados. Use o utilitário:

```bash
python3 scripts/docx/comment.py desempacotado/ "Este prazo está curto pro escopo"
python3 scripts/docx/comment.py desempacotado/ "Combinado" --parent 0
python3 scripts/docx/comment.py contrato.docx "Revisar a cláusula 4" -o comentado.docx
```

O autor sai como "Revisor" por padrão, e muda pela variável de ambiente `DOC_AUTOR`. O script escreve todos os arquivos internos e as ligações, e imprime o trecho de marcação que você precisa colar no `word/document.xml` pra ancorar o comentário num texto específico. Enquanto você não colar esse trecho, o comentário existe no arquivo mas ninguém vê.

## Sem nenhuma biblioteca de Word na máquina

Entregue o `.md` completo e diga ao dono, em uma linha: falta `python-docx` ou `pandoc` pra gerar o Word; o texto está pronto e a conversão roda com um comando assim que a ferramenta existir. Ofereça o comando exato. Não instale nada por conta própria.
