# PDF: gerar, manipular, extrair e preencher formulário

PDF é o formato de quem vai só ler, imprimir ou assinar. Ele congela o desenho, e essa é a virtude e a limitação: ninguém edita depois sem trabalho.

## Índice

- Escolha da rota
- Gerar PDF
- Manipular (juntar, separar, girar, marca d'água, senha)
- Extrair (texto, tabela, imagem, PDF escaneado)
- Preencher formulário: o caminho A (campos de verdade) e o caminho B (formulário chapado)
- Sem biblioteca de PDF na máquina

## Escolha da rota

| Tarefa | Rota |
|---|---|
| **Gerar** a partir de Word, deck ou planilha | LibreOffice: `python3 scripts/office/soffice_seguro.py --converter-para pdf arquivo.docx --saida .` |
| **Gerar** a partir de markdown | `pandoc entrada.md -o saida.pdf` (precisa de um motor de composição instalado junto) |
| **Gerar** do zero, com controle de página | `reportlab` |
| **Manipular** PDF que já existe | `pypdf` em Python, ou `qpdf` na linha de comando |
| **Extrair** texto e tabela | `pdfplumber`; texto simples também sai com `pdftotext -layout` |
| **Virar imagem** pra conferência | `pdftoppm -jpeg -r 150 arquivo.pdf pagina` |

**Regra de preferência:** converter a partir do formato-fonte preserva o desenho que alguém já fez. Montar o PDF do zero é a rota de quando não existe fonte nenhuma.

## Gerar

Converter de Word ou deck:

```bash
python3 scripts/office/soffice_seguro.py --converter-para pdf documento.docx --saida .
pdftoppm -jpeg -r 100 documento.pdf pagina
ls pagina-*.jpg     # depois olhe as imagens
```

A numeração das imagens é preenchida com zeros conforme o total de páginas: uma página vira `pagina-1.jpg`, doze páginas viram `pagina-01.jpg` a `pagina-12.jpg`, e assim por diante.

**Montando do zero com `reportlab`:** para documento de texto corrido, use o construtor de documento com fluxo de parágrafos, não o desenho por coordenada, que obriga você a calcular quebra de página na mão.

**Nunca use os caracteres unicode de sobrescrito e subscrito** (os dígitos pequenos elevados ou rebaixados) num PDF gerado por `reportlab`: as fontes internas não têm esses desenhos e cada um vira um quadrado preto na página. Use as marcações próprias da biblioteca dentro do parágrafo. Em texto desenhado por coordenada, ajuste tamanho e posição na mão.

## Manipular

**Juntar:** leia cada arquivo, acrescente cada página num escritor único, salve. Na linha de comando: `qpdf --empty --pages a.pdf b.pdf -- juntado.pdf`.

**Separar:** um escritor por página, ou `qpdf entrada.pdf --pages . 1-5 -- paginas1a5.pdf`.

**Girar:** gire a página no escritor, ou `qpdf entrada.pdf saida.pdf --rotate=+90:1` pra girar a página 1.

**Marca d'água:** carregue a página de marca d'água de um PDF de uma página só e funda ela em cada página do documento.

**Senha:** o escritor aceita senha de usuário (pra abrir) e de dono (pra editar). Guarde a senha com o dono; ela não fica no histórico da conversa.

**Tirar a senha:** `qpdf --password=<a senha> --decrypt entrada.pdf saida.pdf`, e só com o dono confirmando que o arquivo é dele.

## Extrair

**Texto com o desenho preservado:** `pdftotext -layout entrada.pdf saida.txt`, ou `pdfplumber` página a página.

**Tabela:** `pdfplumber` devolve cada tabela como lista de linhas. Tabela de PDF quase sempre sai suja: célula partida, cabeçalho repetido em cada página, linha vazia entre grupos. Limpe antes de escrever a planilha, e mostre ao dono duas ou três linhas do resultado antes de processar o arquivo inteiro.

**Imagem:** `pdfimages -j entrada.pdf prefixo`.

**PDF escaneado** (a página é uma foto, não tem texto nenhum dentro): nenhuma extração funciona. Precisa de reconhecimento óptico, que é outra biblioteca. Sem ela na máquina, diga isso ao dono em uma linha, com o nome da ferramenta, e ofereça a alternativa de ele mandar o texto. Nunca "leia" um escaneado adivinhando o conteúdo pela aparência.

## Preencher formulário

Os scripts de formulário usam a biblioteca `pypdf`; sem ela, saem com 3 e dizem `pip install pypdf`. O `preencher_texto.py` aceita as coordenadas em pontos do PDF (`"sistema": "pdf"`, origem embaixo) ou medidas na imagem (`"sistema": "topo"`, origem no alto, com `escala_dpi`); o `campos_info.py` e o `estrutura.py` já trazem as medidas prontas.

**Primeiro descubra que tipo de formulário é**, porque as duas rotas não se parecem:

```bash
python3 scripts/pdf/campos_info.py formulario.pdf --so-verificar
```

### Caminho A: o PDF tem campos de verdade

1. `python3 scripts/pdf/campos_info.py entrada.pdf -o campos.json` lista cada campo com nome completo, página, retângulo e tipo (texto, caixa de marcação, grupo de opção, lista de escolha). Caixa de marcação traz o valor que marca e o que desmarca; grupo de opção traz as opções válidas.
2. `python3 scripts/pdf/para_imagens.py entrada.pdf imagens/` gera a imagem de cada página. Olhe as imagens pra descobrir o que cada campo significa de verdade, porque o nome interno costuma ser um texto sem sentido.
3. Monte um `valores.json` que liga o nome de cada campo ao valor (o formato em lista, com descrição e página, também é aceito). Em caixa de marcação, use exatamente o valor que marca; em grupo de opção, uma das opções listadas.
4. `python3 scripts/pdf/preencher_campos.py entrada.pdf valores.json saida.pdf`. O script confere nome e valor; se algum campo não existir ou o valor for recusado, ele não grava nada, lista os nomes que existem e sai com 1 (`--parcial` grava só os certos). Conserte e rode de novo.

### Caminho B: o formulário é chapado (linhas desenhadas, sem campo)

Aqui você escreve texto por cima, na coordenada certa. Duas abordagens, nesta ordem:

**Pela estrutura (preferida).** `python3 scripts/pdf/estrutura.py entrada.pdf -o estrutura.json` devolve cada rótulo de texto com coordenada exata, as linhas horizontais que separam as fileiras, e os quadradinhos que são caixa de marcação. Com isso você calcula onde cada resposta entra: a área de escrita começa logo depois do rótulo e vai até o próximo rótulo ou até a borda da fileira. A coordenada de caixa de marcação vem pronta.

**Pela imagem (reserva).** Só quando a estrutura não devolve rótulo nenhum, que é o caso do escaneado. Gere as imagens e estime as posições olhando.

Em qualquer das duas, antes de escrever: `python3 scripts/pdf/conferir_caixas.py campos.json` confere se as áreas se sobrepõem e se alguma ficou pequena demais pro tamanho de fonte. Conserte o que ele apontar. Depois `python3 scripts/pdf/preencher_texto.py entrada.pdf campos.json saida.pdf` escreve (texto que não cabe na caixa é relatado e sai com 1), e `python3 scripts/pdf/imagem_de_conferencia.py entrada.pdf campos.json --pagina 1 -o imagem.png` desenha as áreas por cima da página pra você conferir com o olho que nada caiu fora do lugar.

**O que a estrutura costuma não achar:** caixa de marcação redonda (só quadrado é detectado), controle gráfico fora do padrão, e elemento de cor muito clara. Onde a imagem mostra um campo que a estrutura não trouxe, resolva aquele campo pelo olho e deixe o resto pela estrutura.

**Campo que o dono não preencheu fica vazio**, e a entrega lista quais ficaram. Preencher formulário por conta própria é inventar declaração no nome de outra pessoa, e isso não se faz nem com dado que parece óbvio.

## Sem biblioteca de PDF na máquina

Se existir LibreOffice, a geração sai de qualquer formato de escritório e você não precisa de mais nada. Sem ele e sem `reportlab`, entregue o `.docx` ou o `.md` e diga em uma linha qual comando gera o PDF quando a ferramenta existir. Para manipulação, `qpdf` na linha de comando resolve juntar, separar e girar sem biblioteca de Python nenhuma; teste se ele existe antes de dizer que não dá.
