---
name: soft-webinar-slides
description: >-
  Faz os SLIDES de uma aula que vende (webinar, masterclass, palestra com oferta) a partir do roteiro ou dos tópicos do dono, do jeito que deu certo: um modelo desenhando cada slide com juízo visual e o guia de slides provado na mão. Entrega o brief em partes pra colar no Claude Design (o guia inteiro, a identidade e os slides no contrato do roteiro) ou o deck desenhado aqui slide a slide, com prova visual de cada um: deck.html 1920x1080 com revelação por clique, deck.pptx com notas e animação, deck.pdf, mosaicos e notas do apresentador. Use quando o pedido for: "faz os slides", "monta o deck da aula", "apresentação do webinar", "slides da palestra com oferta", "transforma esse roteiro em slides", "slides da masterclass", "brief dos slides pro Claude Design". NÃO use pra: o roteiro, a oferta e a copy da aula (soft-webinar); arte de carrossel, banner ou capa (soft-designer); apresentação institucional ou palestra sem venda (soft-apresentacao). Leia e siga o fluxo inteiro do SKILL.md.
---

# Os slides da aula que vende

O dono manda o roteiro (ou só os tópicos) e recebe os slides. A qualidade vem de um modelo **desenhando** cada slide com juízo visual e o guia provado na mão (`references/guia-slides-provado.md`). Molde preenchido por script gera slide de texto puro e foi reprovado. Dois jeitos:

| modo | pedido típico | entrega |
|---|---|---|
| **Claude Design** (principal) | "faz os slides", "me dá o brief pro Claude Design" | `BRIEF-CLAUDE-DESIGN-parte-01.md`, `-02.md`... pra colar no Claude Design |
| **Agente desenha** | "quero o deck pronto aqui", "me manda o PPTX", ou o dono não usa o Claude Design | a pasta do deck (abaixo), desenhada por você slide a slide |

Pedido sem modo dito: com o dono na conversa, entregue o brief e ofereça, numa linha, o deck desenhado aqui; sem ninguém pra responder, desenhe o deck no modo agente e ofereça o brief numa linha. Pedido dos dois: faça os dois a partir do mesmo `trabalho/roteiro.md`.

Nos comandos, `scripts/` é a pasta de scripts desta skill (com o caminho dela) e `trabalho/` mora na pasta onde o dono trabalha, nunca dentro da skill instalada.

## Os três níveis de entrada

**Roteiro completo** (slide a slide, com conteúdo de tela e fala): siga. No modo agente, um slide do roteiro vira quantos slides tiver ideias (passo Dividir); no brief, o roteiro vai como está.

**Só tópicos** (a ordem da aula, sem roteiro): antes de tudo, escreva `trabalho/roteiro.md` no contrato do roteiro, um `### Slide N · título` por ideia, com `**Objetivo:**`, `**CONTEÚDO:**` só com as frases do dono e `**FALTA:**` no que não existe (fala, número, print, preço). Nada que o dono não escreveu entra no CONTEÚDO. Entregue o que dá pra fazer e pergunte o resto, sem parar a entrega.

**Nada** (só "faz meus slides"): conduza as perguntas abaixo, uma por vez, começando pelo roteiro ou pelos tópicos. Só o roteiro (ou os tópicos) para a entrega: espere. As outras seguem o padrão do passo 0 e vão pra lista de pendentes.

O contrato do roteiro, aceito pelos dois modos:
```
### Slide 07 · Título do slide
**Objetivo:** o que o slide faz
**CONTEÚDO:**
- linha de tela
- FALTA: o que o insumo não traz
**NOTAS**
FALA
  Abre com: ...
  Clique 1: ...
  Fecha com: ...
TRANSIÇÃO: ...
```

**Identidade:** cores, fonte, logo e nome vêm do perfil do agente quando existe; se o dono mandou, monte `trabalho/perfil.json` só com o que ele deu (campos em `assets/perfil-padrao.json`). Sem identidade, a neutra, declarada numa linha no relato. Cor do dono com pouco contraste: escureça no fundo claro ou clareie no escuro e avise.

## Modo Claude Design (principal)

```
python3 scripts/montar_brief_design.py trabalho/roteiro.md --saida <pasta> [--perfil trabalho/perfil.json]
```

Cada parte leva o guia inteiro, sem corte, no topo; o pedido explícito de desenhar cada slide com juízo visual, sem texto puro; a identidade do dono; e os slides daquela parte no contrato do roteiro. Até 6.500 palavras por parte, guia incluído. Todo slide aparece uma vez e na ordem; o que sai por falta de dado vira FORA DO DECK. Detalhes e relato: `references/claude-design.md`.

## Modo agente: você desenha cada slide

Obrigatórios: os passos 0 a 7, nesta ordem; o arquivo que o passo cita se lê. Você é o designer. Nenhum layout pronto: cada slide é um arquivo HTML de 1920x1080 com CSS e SVG, desenhado a partir do guia e das receitas de `assets/receitas/` (índice e contrato em `references/receitas-visuais.md`).

0. **Perguntar**, uma coisa por vez, só o que o roteiro usa e ficou sem resposta, mais a identidade (cores, fonte, logo), que vale sempre: o roteiro; os prints, só de resultado que terceiros ou o dono afirmam em venda (dívida e fato pessoal de história não pedem print); por bônus, o valor avulso, a entrega em uma linha e a dor que resolve; o prazo da oferta com o motivo real e o link (valem quando o roteiro traz preço). Cada pergunta diz o que precisa, por quê, onde conseguir e o que vem depois. Sem o dado, segue o padrão da tabela (vaga, FALTA, slide fora, identidade neutra declarada). Sem dono presente, não espere: registre cada pergunta pendente em "Falta você responder" e siga com o padrão. Detalhe: `references/perguntas-ao-dono.md`.
1. **Ler.** O `guia-slides-provado.md` inteiro, o `receitas-visuais.md`, o roteiro, `dividir-o-roteiro.md` e `esquema-principal-reusado.md`; `receita-numero-em-blocos.md` só se o roteiro trouxer número ou contagem pra virar imagem (número único de história: regra na receita). Roteiro que é só um trecho: `roteiro-parcial.md`.
2. **Normalizar.** Copie o roteiro do dono, intocado, pra `trabalho/roteiro-original.md`. O `roteiro.md` do passo 3 sai no contrato: `### Slide NN · título`, `**Objetivo:**`, `**CONTEÚDO:**`, `**NOTAS**`; `FALTA:` só onde falta dado ("FALTA: nenhuma" sai); a premissa do topo fica acima do primeiro `###`; a fase é `## Fase A · Nome` (letras A, B, C na ordem), nome do dono, com o ponto médio interno se tiver (`## Fase A · Ação · Oferta & Fecho`; caixa alta vira Capitalizado; sigla conhecida fica); os nomes próprios de módulo, bônus e marca vão, um por linha, em `trabalho/termos-do-dono.txt` (sem nome próprio, o arquivo vazio vale). Confira: `ler_roteiro.py trabalho/roteiro-original.md --resumo`.
3. **Dividir.** Um slide por ideia: o número sai da fala, não de cota; ideia só (até 25 palavras de fala) fica como está, e duas ideias dividem, mesmo num slide curto. Cada um leva uns 10 segundos de fala, a tela uma frase de até 12 palavras (indivisível, até 20) e, com o apoio visual, até 40 no total (vaga, legenda, tarja e rótulo de bônus não contam; o script reprova acima), a fala inteira nas NOTAS, sem mudar palavra nem ordem; "Fecha com" é a última fala; se ela é um clique ou a fala é uma frase só, "a mesma frase, sem pausa". Tela que traz mais que a fala: "Abre com: lê a frase da tela", sem palavra nova. Lista e conta entram uma peça por clique (teto de 7 cliques); prova que falta vira vaga de print, e cena que falta, vaga de cena (bloco tracejado com `data-vaga`; o slide fica e a pergunta vai pro `_operador.md`). Nada novo: tudo vem do roteiro, com o mesmo rótulo; trecho sem dado sai do deck e vira pergunta. O resultado é `trabalho/roteiro.md`. Regras e conferência (`python3 scripts/conferir_fala.py` tem de dizer IGUAL): `references/dividir-o-roteiro.md`.
4. **Esqueleto.** `python3 scripts/ler_roteiro.py trabalho/roteiro.md --esqueleto trabalho/slides` grava um arquivo por slide (`01.html`...) com o `<section>` vazio, o fundo por bloco, o CONTEÚDO e a FALTA do roteiro num comentário e a nota já escrita com a fala do roteiro. Slide que o roteiro tira vai pro `trabalho/slides/_operador.md` como pergunta. A TRANSIÇÃO vira "Fecha com" no slide que não traz um. Rode o esqueleto uma vez: mudar um clique depois é editar o `roteiro.md` e a nota do HTML (e rodar `conferir_fala.py`); regravar recusa se há slide desenhado, e `--forcar` descarta o desenho. O `data-bloco` vem do `## Fase X · Nome` do roteiro (sem ele, tudo é "Aula" e o fundo não troca). Numeração: o número do deck (`NN.html`) manda em comando e relato; o do roteiro vai entre parênteses ("deck 05 (roteiro 06)").
5. **Desenhar, um slide por vez, fechando o laço em cada um:**
   - passada 1, a frase: a ideia do slide numa frase completa e curta, do roteiro, lida em 3 segundos; o resto vai pra nota;
   - passada 2, mostrar em vez de contar: número vira imagem do próprio valor (blocos de escala única só pra dinheiro e contagem grandes, `references/receita-numero-em-blocos.md`; preço e razão ficam em número grande), lista vira pilha, ícone ou escada, afirmação vira print, comparação ou metáfora que bate com a fala (narrativa, emoção, future pacing e crença: a metáfora que ilustra a fala sem pessoa, cena nem número novo). O esquema principal é um desenho só, reusado no ensino, no recap, na decisão antes do pitch e como produto na oferta (módulos como degraus, sem contagem que você invente: o nome do produto como o dono escreve, "6 módulos completos", vale; em cada módulo, a escada grande na base com o degrau dele aceso); desenho que volta em dois slides é esquema, não metáfora nova (`references/esquema-principal-reusado.md`);
   - tamanho, em 1920x1080: nada abaixo de 30px (legenda, rótulo e vaga também), o que decide em 56px ou mais; o script imprime `menor fonte: Npx` e reprova abaixo do piso (`--min-fonte`);
   - escreva o HTML (receita adaptada ou desenho seu, nunca o texto de exemplo de nada);
   - renderize só ele: `python3 scripts/montar_desenho.py trabalho/slides --saida trabalho/ver/NN --so N` (uma saída por slide, senão o PNG anterior some);
   - **olhe o PNG** (Read) e passe o checklist da seção 8 do guia, mais o que o script reprovou;
   - corrija e rode de novo, no máximo duas vezes depois da primeira renderização. Ainda ruim: simplifique e anote no `_operador.md`.
   Só então desenhe o slide seguinte.
6. **Fechar o deck:**
   ```
   python3 scripts/montar_desenho.py trabalho/slides --saida trabalho/deck --insumo trabalho/roteiro.md [--perfil trabalho/perfil.json] [--titulo "nome da aula"]
   ```
   Unidade de pictograma que o roteiro não traz entra em `trabalho/escala-desenho.md` (o script lê sozinho). Junta o `deck.html`, roda `checar_deck.py`, mosaicos, `conferir_fontes.py` (todo número tem fonte no insumo) e lint, e só então exporta `deck.pdf` e `deck.pptx`. Repita até `APROVADO`. Aviso do lint na fala ou no nome do dono (inclusive "molde acima do teto" seguido de "copy passou"): não bloqueia, anotado no `_operador.md`, que o lint também lê (não repita ali a frase do dono nem escreva "não X, é Y"); nome do dono que o lint barra, o script mascara só no lint (`termos-do-dono.txt`) e avisa quais. Toda saída fica dentro de `trabalho/`; rascunho e teste, na pasta temporária do sistema.
7. **Olhar o deck inteiro:** todas as folhas do mosaico (fundo por bloco, composição variada, nenhum texto puro em série) e pelo menos 4 slides em tamanho real de `_conferencia/png/`: a abertura, uma escada ou lista, a oferta e o slide mais cheio (sem oferta completa, o do preço, se houver, e os mais cheios até 4; empate: mais elementos, depois mais cliques, depois o de menor número). O que estiver ruim volta pro passo 5.

Dependências: Python 3 com `playwright` (Chromium), `python-pptx`, `lxml` e `Pillow`. Sem navegador, o modo agente não fecha o laço: entregue o brief e diga por quê.

### O que é "pronto" no modo agente
1. `montar_desenho.py` termina com `APROVADO` e código 0.
2. Cada slide foi renderizado e olhado no laço, e o deck inteiro no passo 6.
3. O relato segue o formato do fim deste arquivo.
Sem os três, não diga "pronto": diga o que falta.

## O que nunca entra no deck (nos dois modos)

- Número, prazo, vaga, preço, parcela, percentual, desconto, resultado, depoimento, print, logo, nome de passo ou relação entre dois dados que o insumo não traz. O rótulo do número é o do insumo ("gerenciou" não vira "faturou").
- Escassez e prazo sem motivo real; em aula gravada, promessa de presença ao vivo ou de replay.
- [A CONFIRMAR], [DO DONO], pergunta ao dono, nome de arquivo, nome de regra ou qualquer bastidor. Tudo isso mora na nota ou no `_notas-operador.md`.
- Dado pessoal de cliente do dono sem autorização; print com dado de terceiro sem recorte.
- Pessoa, personagem, foto do dono, cena inventada, banco de imagem e imagem de IA: o que falta vira vaga tracejada (de print ou de cena), nunca ilustração.
- A oferta fora das regras do guia: a parcela é a manchete, o à vista vem menor, o total parcelado nunca aparece, o percentual fica ao lado do número a que se refere, a soma da tabela confere, e sem o valor de algum item a tabela não entra (só nomes, sem nenhum valor, nem o do item que tem: `receita-pilha-de-nomes.md`).

## As notas do apresentador

Formato em `references/notas-do-apresentador.md`. A fala vem do roteiro, palavra por palavra. Sem fala no roteiro, "Abre com: lê a frase da tela"; só tópicos, [A CONFIRMAR: fala]. O `checar_deck.py` reprova nota sem Objetivo, Abre com ou Fecha com, ou com cliques diferentes da tela.

## O relato ao dono

Curto, nesta ordem:
- **Pronto:** a pasta `trabalho/deck` (ou as partes do brief) e quantos slides.
- **Abra primeiro:** no brief, "cole a parte 1 no Claude Design; aprovada, cole a parte 2 na mesma conversa"; no deck, `deck.html` ou `deck.pptx`, e os mosaicos.
- **Premissa:** uma linha (por exemplo, identidade neutra).
- **Fora do deck:** os slides que saíram e o dado que falta em cada um. **Vagas de print e de cena:** quantas, em quais slides, o que cada uma pede.
- **Metáforas que você criou:** cada desenho que o roteiro não pediu, com o slide e a ideia da fala em palavras suas, sem copiar a frase do dono (lista no `_operador.md`).
- **Falta você responder:** as perguntas pendentes numeradas, com o slide (preço, parcela, prova, prazo, link, valor de bônus).
- **Conferência:** a última linha do script e o que ficou sem verificação (PowerPoint real, fonte do dono, Claude Design de verdade); roteiro parcial, o que não se aplica.
- Uma linha de ajuste: "quer outra ordem, mais respiro ou outra cor?"

## Rascunho de texto (fora do fluxo padrão)

`scripts/gerar.py` com o `deck.json` (`ler_roteiro.py --rascunho`) monta o deck pelos 13 layouts de molde (`references/receitas-e-layouts.md`), só pra ver o texto. Nunca é a entrega.

## Arquivos desta skill

`references/` (cada passo cita a sua), `assets/` (`receitas/`, `palco.html`, `perfil-padrao.json`; o `molde.css` é do rascunho) e `scripts/` (`gerar.py` e `montar_deck.py` são do rascunho).
