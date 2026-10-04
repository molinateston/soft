# A conferência do deck

Três camadas, nesta ordem: o script mede, o insumo confirma, o olho vê. Nenhuma substitui a outra.

## 1. O script mede (checar_deck.py)

Renderiza cada slide em 1920x1080 no Chromium, com todos os cliques abertos, e reprova (código 1) quando:

| reprova | por quê |
|---|---|
| texto sai do slide, fica cortado pela caixa ou se sobrepõe a outro | o celular mostra o corte; a sala lê o que está por cima |
| fonte abaixo do piso (`--min-fonte`, padrão 30px numa tela de 1920) | leitura no celular; o script mede a menor fonte do slide e aponta o elemento |
| mais de 7 cliques | vira dois slides |
| nota sem Objetivo, Abre com ou Fecha com, ou com número de cliques diferente da tela | quem apresenta se perde |
| contraste abaixo de 4,5 (texto menor que 40px) ou 3 (40px ou mais) | leitura em tela ruim e projetor |
| soma da tabela diferente do total, ou total escrito diferente da soma | conta que não fecha derruba a oferta |
| total parcelado (parcela vezes parcelas) em qualquer slide | o número que assusta; mostre parcela e à vista |
| travessão na tela ou na nota | régua de voz |
| cor reservada fora da tarja, do risco e do rótulo BÔNUS | a cor perde o sinal |
| slide com mais de 40 palavras, o teto único (`data-layout` oferta, bônus e escada ficam de fora) ou bloco com mais de 20; não contam o texto dentro de `data-imagem`, o de `data-vaga`, `.legenda`, `.tarja` e `.rot-bonus`, nem a célula repetida 6 vezes ou mais | uma ideia por slide, lida em 3 segundos |
| colchete, lacuna ou `{{marcador}}` visível ([A CONFIRMAR], [DO DONO]) | bastidor ou receita sem adaptar na tela |
| imagem quebrada ou entrando por clique | título e imagem já estão na tela quando o slide abre |

Avisa sem reprovar: vaga (de print ou de cena) ainda sem imagem, e texto HTML sobre SVG com gradiente ou imagem (o contraste é medido contra o preenchimento liso do SVG que está atrás do texto; com gradiente o script não sabe a cor e só avisa). Contraste de texto sobre forma SVG que dê 1.0 sem motivo, ou um aviso dele, resolve-se dando ao rótulo o seu próprio fundo HTML (`background` na caixa do texto), que o script mede sempre; ou olhe o PNG e deixe o aviso. Imprime sempre `menor fonte: Npx (slide NN: ...)`, a menor fonte medida, aprovando ou não; confira essa linha contra o piso de 30px.

Quando reprovar: corrija o HTML do slide apontado em `trabalho/slides/` (encurte a tela e leve o resto pra nota, divida o slide, mude a composição) e rode o `montar_desenho.py` de novo. Nunca mexa no `deck.html` gerado. No rascunho de texto, o que se corrige é o `deck.json`.

No laço de um slide (`--so N`), o script mede só aquele slide e grava o PNG dele: é ali que a maior parte se resolve.

O teto de palavras sobe com `--max-palavras` só quando o dono pediu tela mais cheia, e isso vai escrito no `_notas-operador.md`.

O piso de fonte tem padrão 30px, o mesmo para kicker, rótulo, legenda e vaga; a frase ou o número que decide pede 56px ou mais (isso o olho confere, o script só barra abaixo do piso). O parâmetro vale nos dois comandos: `python3 scripts/checar_deck.py <pasta> --min-fonte 30` e `python3 scripts/montar_desenho.py ... --min-fonte 30`. Baixe só se o dono pediu e diga no relato. O rascunho de texto (`gerar.py`) segue com 24px, porque o molde dele tem rótulos de 24px (fora do fluxo).

## 2. O insumo confirma (conferir_fontes.py e lint_copy.py)

- `conferir_fontes.py --entrega notas.md --insumo <roteiro e perfil>`: todo número da tela e da fala tem que existir no insumo, no mesmo valor. Também reprova soma de tabela que não fecha, total parcelado e valor por dia que não é parcela dividida por 30. O total da tabela conta como número com fonte quando a soma fecha.
- `lint_copy.py` no `notas.md` e no `_notas-operador.md`: travessão, verbo-freio e clichê.
- Sem insumo em arquivo (o dono colou no chat), salve o que ele colou num `.md` e passe esse arquivo como insumo.
- Legenda de escala de pictograma ("1 bloco = [unidade]") não existe no roteiro e reprova por falta de fonte. Declare a unidade em `trabalho/escala-desenho.md` (a régua do desenho, nunca dado do dono; formato em `receita-numero-em-blocos.md`). O `montar_desenho.py` lê esse arquivo sozinho quando há `--insumo` e avisa na saída; na chamada direta do conferidor, passe os dois: `--insumo trabalho/roteiro.md trabalho/escala-desenho.md`.
- Slide dividido: antes do esqueleto, `conferir_fontes.py --entrega trabalho/roteiro.md --insumo trabalho/roteiro-original.md` mostra se a divisão inventou número, e `python3 scripts/conferir_fala.py` mostra se a fala do original e a dos slides novos têm as mesmas palavras na mesma ordem (IGUAL), ignorando "a mesma frase, sem pausa", "lê a frase da tela" e a linha toda entre parênteses, direção de palco (ver `dividir-o-roteiro.md`).

## 3. O olho vê

O script não sabe se a frase é a certa, se a imagem bate com a fala, se o desenho mostra em vez de contar ou se o slide ficou feio. Ele também não vê forma por cima de texto (um X de SVG sobre um rótulo). Por isso:
1. No laço, cada slide renderizado é olhado (Read do PNG) antes do seguinte, com o checklist da seção 8 do `guia-slides-provado.md`.
2. No fecho, abra todas as folhas do mosaico (12 slides por folha) e confira a alternância de fundo por bloco, a variação de composição, slide de texto puro em série e slide vazio ou lotado.
3. Abra pelo menos 4 PNGs em tamanho real (`_conferencia/png/`): a abertura, uma escada ou lista, a oferta e o slide mais cheio.

### Aviso do lint na fala do dono

O lint que avisa na fala do dono não bloqueia. O `lint_copy.py` marca com ⚠ (aviso, não bloqueia) verbos e nomes que ele estranha, e conta como aviso padrões como "contraste invertido" ("é X, não Y") acima da cota, mesmo quando a frase é do roteiro do dono. A fala e o nome de módulo do dono não mudam: o aviso fica como está e vai anotado no `_operador.md` ("o lint avisa em: [frase], [tipo de aviso]"), com o slide. Só falha dura (código 1) barra. Isso vale também pra "molde de antítese: 2 (teto 1) ... reprova a peça" seguido de "copy passou": a mensagem é aviso, não falha (patch candidato da mensagem na nota da candidata). O lint lê também o `_operador.md`, porque ele entra no `_notas-operador.md`: ali, não cite a frase do dono nem escreva "não X, é Y" (cada citação conta de novo), e reescreva só o texto seu (Objetivo, notas do operador).

Falha dura do lint em palavra do dono (nome de bônus, módulo ou marca que casa com a família do verbo-freio ou com uma muleta de rede social que o lint barra, por exemplo): trocar na tela e manter na nota não fecha, porque o `notas.md` leva tela e nota juntas. O caminho é o arquivo `trabalho/termos-do-dono.txt`, criado no passo Normalizar: um termo por linha, só o nome próprio inteiro, na grafia do roteiro, sem a palavra solta que o lint barra. No fecho, o `montar_desenho.py` troca esses termos por uma palavra neutra SÓ no texto que envia ao lint, nunca no deck nem no `notas.md`. A primeira linha da saída ("MASCARAMENTO") conta os termos da lista; a linha do lint diz só os que apareceram e quantas vezes cada um, e a seguinte diz quais o lint barra sozinhos (o motivo do mascaramento). Termo curto e comum mascara falha de verdade: ponha só nome próprio inteiro. Falha dura em palavra que não está na lista (travessão, verbo-freio na sua redação) segue barrando: corrija o texto.

### Falsos positivos conhecidos do conferidor

- **Objetivo da nota que compara valores.** O `conferir_fontes.py` lê a nota inteira e reprova "conta de preço" em linha que compara à vista e parcela ("Objetivo: parcela como manchete, número maior que o à vista"). Escreva o Objetivo sem comparar valores ("parcela como manchete, o à vista em segundo plano"): o Objetivo diz o que o slide faz, sem comparar números. No fecho, o `montar_desenho.py` manda ao conferidor uma cópia temporária do `notas.md` com a linha Objetivo marcada como nota, então a linha não reprova; o `**Objetivo:**` do `roteiro.md` ganha o mesmo tratamento no comando de `dividir-o-roteiro.md`. O conferidor é cópia compartilhada: não se mexe nele.
- **Comentário `<!-- Origem: ... -->` na conferência da divisão.** O conferidor lê o comentário e acusa número sem fonte (a contagem "dividido em 13"). Na conferência da divisão, passe o roteiro sem essa linha, como mostra `dividir-o-roteiro.md`. No fecho do deck o `montar_desenho.py` já tira todo comentário antes de montar o `notas.md`.

## O que vai no _notas-operador.md

O `montar_desenho.py` já escreve a base (as [A CONFIRMAR] das notas viram perguntas, uma vez só por slide, com o número do deck e o do roteiro entre parênteses, e a identidade usada) e junta o `trabalho/slides/_operador.md`, onde o esqueleto já pôs os slides que o roteiro tirou. Acrescente nesse arquivo:
- cada bloco que saiu por falta de dado, com a pergunta ao dono;
- a premissa que você assumiu, em uma linha;
- o que ficou sem verificação.

Nada disso aparece no deck.

## A saída do fecho

O passo "6 pdf" imprime uma linha de resultado (`pdf: gerado (... KB, N páginas ...)` ou `pdf: NÃO gerado`). O `deck.pdf` na pasta do deck também prova. O `APROVADO` só vem depois de pdf e pptx.
