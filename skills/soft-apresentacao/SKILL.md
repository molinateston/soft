---
name: soft-apresentacao
description: "Cria, redesenha, renderiza e exporta apresentações, decks, aulas, palestras e slides a partir de roteiro, fala, documento, notas ou tema. Use quando o usuário pedir apresentação, PowerPoint, PPTX, PDF de slides, deck navegável, mosaico, slides guiados por fala ou material para leitura. Produz HTML 1920x1080 como fonte e exporta PDF, PNG/JPG e PPTX fiel; pode gerar PPTX editável identificado como aproximado."
---

# Criar apresentações utilizáveis

Tratar o HTML 1920×1080 como fonte única. Criar primeiro o deck navegável; exportar os demais formatos somente depois do crivo visual. Usar o sistema B80/C20 como direção padrão do LEON sem herdar produto, voz, números ou copy de outra pessoa.

## Alinhar o mínimo útil

Recuperar dos arquivos e da conversa tudo o que já estiver definido. Perguntar apenas o que faltar e mudar o resultado:

1. Qual é o objetivo e quem assiste?
2. O conteúdo já existe ou precisa ser estruturado?
3. Quantos slides ou quanto tempo de fala?
4. É uma apresentação guiada pela fala ou feita para leitura?
5. Há identidade visual própria? Se não houver, usar B80/C20.
6. Quais saídas são necessárias: HTML, PDF, imagens, PPTX fiel, PPTX editável?

Fazer as perguntas juntas quando mais de uma estiver faltando. Não perguntar novamente o que o usuário já informou.

## Escolher densidade

- **Guiada pela fala:** uma ideia por slide, headline grande, 1–3 pontos, respiro generoso, câmera ou área focal preservada.
- **Feita para leitura:** contexto suficiente no próprio slide, blocos estruturados, tabelas e diagramas quando aumentarem compreensão; dividir antes de reduzir demais a fonte.

Se o pedido misturar os dois, escolher o modo dominante. Aula ao vivo e palestra usam fala; relatório assíncrono usa leitura.

## Aplicar B80/C20

Ler `references/sistema-b80-c20.md` antes de desenhar. Resumo:

- 80%: fundo preto, texto claro grande, verde pontual, muito espaço negativo, uma área focal, composição simples e câmera fixa quando houver apresentador.
- 20%: número, processo, prova, comparação ou diagrama somente quando explicarem melhor o conteúdo.
- Nunca usar detalhe como decoração, coleção de cards, excesso de molduras, caixa alta em headlines, estética genérica ou mudança de linguagem entre slides.

Adaptar cores, tipografia e marca quando o usuário fornecer identidade própria, preservando a hierarquia e o respiro do sistema. Não copiar conteúdo dos exemplos.

## Produzir o master

1. Montar o arco e escolher uma ideia dominante por slide.
2. Partir de `assets/master-b80-c20.html` ou criar HTML equivalente.
3. Manter cada `.slide` em palco fixo de 1920×1080; escalar o palco inteiro para qualquer tela, sem reflow responsivo.
4. Incluir navegação por teclado, toque e roda; respeitar `prefers-reduced-motion`.
5. Manter CSS e JavaScript no próprio HTML. Usar caminhos relativos para imagens locais.
6. Se houver apresentador, reservar a câmera em posição idêntica em todos os slides e impedir qualquer conteúdo de invadir essa área.
7. Registrar notas de fala como comentários HTML, atributo `data-notes` ou notas no PPTX editável quando o fluxo exigir.

Não usar o PowerPoint como fonte visual. O HTML governa.

## Exportar

Executar:

```bash
node scripts/export-deck.mjs CAMINHO/DECK.html --format=pdf,png,pptx --out=CAMINHO/SAIDA --pptx-mode=image
node scripts/export-deck.mjs CAMINHO/DECK.html --format=pptx --out=CAMINHO/SAIDA --pptx-mode=editable
python3 scripts/fix_editable_dark.py CAMINHO/SAIDA/DECK-editable.pptx CAMINHO/SAIDA/DECK-PPTX-EDITAVEL-APROXIMADO.pptx
python3 scripts/make_mosaic.py CAMINHO/SAIDA/DECK-png CAMINHO/SAIDA/MOSAICO.png
```

Entregar os modos com nomes explícitos:

- `PPTX-FIEL.pptx`: cada slide é uma imagem; pixel-idêntico, não editável.
- `PPTX-EDITAVEL-APROXIMADO.pptx`: texto e formas editáveis; pode variar em fonte, quebra e espaçamento.

Não prometer fidelidade do modo editável. Se o render editável perder contraste, cortar texto ou descaracterizar o deck, corrigir e validar; se não for possível, não entregar esse modo.

No padrão B80/C20, o exportador pode converter transparências CSS em branco. Executar `fix_editable_dark.py` antes do render do modo editável; o script restaura o fundo preto e os blocos que deveriam acompanhar o campo escuro. Usar apenas em decks escuros.

## Fazer crivo visual real

Depois do primeiro export:

1. Conferir a quantidade de PNGs e as dimensões 1920×1080.
2. Conferir PDF 16:9 e número de páginas.
3. Validar cada PPTX como arquivo e renderizá-lo para inspeção.
4. Abrir o mosaico e inspecionar todos os slides: corte, overflow, sobreposição, contraste, margens, câmera, repetição e excesso decorativo.
5. Abrir em tamanho cheio os slides densos ou suspeitos.
6. Corrigir o master e reexportar tudo que depende dele.

Não declarar pronto com base só no código ou na existência dos arquivos.

## Entregar

Entregar o resultado utilizável, não o bastidor:

- mosaico PNG para aprovação rápida;
- HTML navegável;
- PDF;
- pasta de PNGs quando pedida;
- PPTX fiel;
- PPTX editável aproximado somente se validado.

Informar em uma frase a diferença entre os dois PPTX e conduzir o próximo passo: revisar o piloto, corrigir ou escalar o restante.

## Recursos

- `assets/master-b80-c20.html`: master neutro 1920×1080.
- `references/sistema-b80-c20.md`: direção visual e régua de decisão.
- `scripts/export-deck.mjs`: exporta HTML para PDF, imagens e PPTX.
- `scripts/fix_editable_dark.py`: corrige fundo e transparências do PPTX editável escuro.
- `scripts/make_mosaic.py`: monta o mosaico dos PNGs.
