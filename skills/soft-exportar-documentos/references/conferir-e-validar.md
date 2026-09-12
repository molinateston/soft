# Conferir e validar: as 3 camadas, na ordem

Todo arquivo que sai daqui passa pelas 3 camadas. Elas pegam defeitos diferentes, e nenhuma substitui a outra. A ordem importa: conteúdo é o mais barato de consertar, visual é o mais caro.

## Camada 1 · Conteúdo (sempre)

Leia o arquivo de volta pra texto e compare com o que devia estar lá.

```bash
pandoc -t markdown documento.docx        # Word
markitdown deck.pptx                     # deck (uma seção por slide)
markitdown planilha.xlsx                 # planilha (uma seção por aba)
pdftotext -layout documento.pdf -        # PDF
```

O que essa camada pega:
- Conteúdo que sumiu na conversão (a última seção que não entrou, a tabela que virou parágrafo).
- Ordem trocada.
- **Sobra de template**, o defeito mais embaraçoso de todos. Procure sempre:

```bash
markitdown saida.pptx | grep -iEn "x{3,}|lorem|ipsum|inserir aqui|preencher|seu texto|titulo do slide|\[.*\]"
```

Achou, conserte antes de dizer que está pronto. Vale igual pro Word e pra planilha, trocando o comando de leitura.

## Camada 2 · Arquivo (quando a ferramenta existir)

Valide a estrutura interna. É a camada que pega o arquivo que abre quebrado, antes do dono descobrir.

```bash
python3 scripts/office/validate.py saida.docx
python3 scripts/office/validate.py saida.pptx --original template.pptx
python3 scripts/xlsx/recalc.py saida.xlsx
```

**Sempre passe o original quando o arquivo nasceu de um template.** O template pode ter erro próprio de esquema; sem essa base, os erros dele aparecem misturados com os seus, e o que você quebrou de verdade se esconde no meio. As conferências de estrutura (vínculos, tipos de conteúdo, gráficos) ignoram essa base e reportam de qualquer jeito, então leia essas por si.

Cada falha nomeia o próprio conserto. Conserte no gerador, não editando o XML compactado na mão: senão você conserta uma vez e reintroduz o erro na próxima geração.

**Na planilha, o recálculo é a validação.** E lembre das duas leituras da saída: JSON com chave de erro em vez de situação significa que nada foi calculado; e recálculo verde prova que a fórmula roda, não que ela está certa.

## Camada 3 · Visual (obrigatória em deck e em tudo que vai impresso)

Renderize e olhe.

```bash
python3 scripts/office/soffice.py --headless --convert-to pdf saida.pptx
rm -f pagina-*.jpg
pdftoppm -jpeg -r 150 saida.pdf pagina
ls -1 "$PWD"/pagina-*.jpg
```

Depois abra as imagens e olhe uma por uma. **Olhe com olho novo:** depois de encarar o código que gerou o arquivo, você tende a ver o que esperava em vez do que apareceu. Se o ambiente tiver delegação, peça a conferência a outra execução; senão, faça uma pausa e volte.

**Refazendo alguma coisa, rode os quatro comandos de novo.** O PDF precisa ser gerado outra vez a partir do arquivo corrigido, ou as imagens continuam mostrando a versão velha.

O que procurar, na ordem de frequência:

1. **Texto estourando a caixa ou cortado na borda.** É o defeito mais comum e sempre visível pra quem recebe. Confira este primeiro. (Numa fonte fora da lista segura, a prévia é aproximada: confie na folga que você deixou, não no encaixe aparente.)
2. Elementos sobrepostos: texto atravessando forma, linha cortando palavra, coisa empilhada.
3. Rodapé ou fonte da informação colidindo com o conteúdo de cima.
4. Elementos colados demais, ou espaço muito desigual entre um bloco e outro.
5. Margem pequena demais em relação à borda da página.
6. Colunas ou blocos que deviam alinhar e não alinham.
7. Texto de contraste fraco (cinza claro em fundo claro, escuro em fundo escuro).
8. Decoração de template fora de lugar depois da troca de texto: o sublinhado desenhado pra um título de uma linha, com o título novo ocupando duas.
9. Caixa estreita demais fazendo a palavra quebrar em toda linha.
10. Sobra de template que passou pela camada 1.

**Sua primeira geração quase sempre tem dois ou três defeitos reais.** Ache, conserte, gere de novo só o que mudou, e pare. Não fique polindo sem defeito apontado.

## Sem as ferramentas de conferência

Nenhuma camada é opcional por preguiça, mas todas são impossíveis sem ferramenta. Quando faltar:

- Sem leitor de volta (`pandoc`, `markitdown`, `pdftotext`): confira a camada 1 relendo o `.md` de origem contra a lista do que você escreveu no gerador, seção por seção, e diga ao dono em uma linha que a conferência foi feita na origem, não no arquivo final.
- Sem validador: diga em uma linha que o arquivo não passou pela validação de estrutura e peça que o dono abra uma vez antes de encaminhar.
- Sem renderizador: diga em uma linha que a conferência visual não foi possível, e liste o que você não pôde verificar (encaixe de texto e sobreposição). Nunca declare que conferiu com o olho um arquivo que você não viu.
