# Modo Claude Design: o brief que reproduz o processo provado

O deck aprovado nasceu assim: o guia de slides inteiro colado no Claude Design junto com o conteúdo da aula, e um modelo desenhando cada slide com juízo visual. O brief desta skill monta exatamente isso, em partes que cabem numa mensagem.

## O comando

```
python3 scripts/montar_brief_design.py trabalho/roteiro.md --saida <pasta> [--perfil trabalho/perfil.json] [--max-palavras 6500]
```

Gere o brief só quando o dono o pediu (ou, com o dono na conversa e sem modo dito, como o caminho principal). Num pedido sem modo dito e sem dono pra responder, o deck desenhado é a entrega e o brief fica oferecido numa linha, sem gerar. Grava `BRIEF-CLAUDE-DESIGN-parte-01.md`, `-02.md` e assim por diante. Cada parte, nesta ordem:
1. o cabeçalho com o "como usar" (a parte 1 diz como colar as demais; as outras dizem que continuam a mesma conversa);
2. o guia `references/guia-slides-provado.md` inteiro, idêntico, entre as linhas `=== GUIA DE SLIDES PROVADO ... ===`;
3. o pedido: desenhar os slides daquela parte com juízo visual, mostrar em vez de contar, usar imagem, SVG e número como imagem e não entregar slide de texto puro; a tela sai do CONTEÚDO, as NOTAS vão nas notas, [FALTA DO DONO] fica fora da tela;
4. a identidade visual (do perfil do dono, ou a neutra, dita como neutra);
5. os slides daquela parte no contrato do roteiro: título, bloco, objetivo, conteúdo, tabela, falta e notas (fala, cliques, fecha com, transição);
6. como entregar e exportar.

Até 6.500 palavras por parte, contando o guia (perto de 3.100). O script corta a parte entre slides, nunca no meio de um, e roda o `lint_copy.py` em cada parte (código 1 se alguma reprovar).

## A entrada

| entrada | o que fazer antes |
|---|---|
| roteiro slide a slide | copie pra `trabalho/roteiro.md` e rode |
| só tópicos | escreva `trabalho/roteiro.md` no contrato do roteiro (um `### Slide N · título` por ideia, CONTEÚDO só com as frases do dono, FALTA no resto) e rode |
| o dono colou no chat | salve o texto em `trabalho/roteiro.md` |

## O que o brief garante

- O guia aparece idêntico em todas as partes: nada condensado, nada neutralizado.
- Todo slide do roteiro aparece uma vez e na ordem, com a numeração do roteiro. Slide que o roteiro tira por falta de dado aparece no lugar dele como FORA DO DECK, com o que falta, e o pedido manda não desenhar.
- Lacuna do roteiro ([A CONFIRMAR], [DO DONO]) vira [FALTA DO DONO: o quê]. Tabela com valor faltando leva a ordem de não desenhar soma nem total.
- Nenhum caminho de arquivo, nome de script ou nota de bastidor.

## O relato ao dono

- **Pronto:** quantas partes e quantos slides, e a pasta.
- **Como usar:** cole a parte 1 no Claude Design e mande; quando aprovar os slides dela, cole a parte 2 na mesma conversa, e assim por diante.
- **Falta você responder:** as lacunas [FALTA DO DONO] que mais pesam (preço, parcela, prova, prazo), numeradas, com o slide.
- **Premissa:** a identidade usada.
- Uma linha: "quer o deck desenhado aqui também (HTML, PPTX e PDF)? Faço a partir do mesmo roteiro."

## Sem verificação

O resultado visual é do Claude Design, e os formatos de exportação e o jeito de levar as notas são dele. Se o dono devolver o PDF exportado, abra as páginas e passe o checklist da seção 8 do guia; o `checar_deck.py` só mede o `deck.html` desta skill.
