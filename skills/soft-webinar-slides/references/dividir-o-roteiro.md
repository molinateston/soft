# Dividir o roteiro antes de desenhar

No modo agente, o roteiro do dono quase nunca está no tamanho de um slide da venda. Um slide do roteiro costuma carregar de 30 a 60 segundos de fala e várias ideias. O guia manda uma ideia por tela, trocando a cada 3 a 10 segundos. O passo "Dividir" reescreve o roteiro nessa medida, antes de qualquer desenho, e só depois o esqueleto é gerado.

## O que sai deste passo

- `trabalho/roteiro-original.md`: o roteiro do dono, intocado. Fica de prova.
- `trabalho/roteiro.md`: o roteiro dividido, no mesmo contrato (`### Slide N · título`, Objetivo, CONTEÚDO, FALTA, NOTAS com FALA e TRANSIÇÃO), renumerado de 01 em diante.
- Em cada slide novo, logo abaixo do `### Slide`, uma linha de comentário `<!-- Origem: slide N do original, dividido em K -->`. Ela fica fora das NOTAS e fora da tela: o `ler_roteiro.py` a ignora (só a copia pro comentário do esqueleto), então não vaza pro `notas.md` nem pro PPTX. O conferidor da divisão é outro caso: veja "Conferir a divisão".
- As perguntas ao dono que a divisão gerou, no `trabalho/slides/_operador.md`.

## Três números, um que manda

O mesmo slide tem até três números: o do roteiro do dono (SLIDE 12), o do `roteiro.md` dividido (renumerado de 01; o slide que sai do deck mantém o número dele aqui) e o do deck (os arquivos `01.html`...; slide fora do deck não gasta número). **O número do deck é a referência única** de comando (`--so N`, `slide-NN.png`, `checar_deck`, `menor fonte`) e de relato. Cite o roteiro entre parênteses: "deck 05 (roteiro 06)"; se precisar do original: "deck 05 (roteiro 06, original 14)". Slide fora do deck não tem número de deck: "roteiro 01 (original 12)". O `ler_roteiro.py --resumo` mostra o número do roteiro dividido; o `_operador.md` que o esqueleto grava traz o mapa deck, roteiro e original; o `_notas-operador.md` escreve cada pergunta como "Slide NN (nome (roteiro MM))", com NN do deck.

## Normalizar antes de dividir

O roteiro do dono vem em formatos variados. O `roteiro.md` dividido sai sempre no contrato, mesmo que o original use outro:

- `### Slide NN · título` (o original pode ter `### SLIDE 1 ·`); `**Objetivo:**`, `**CONTEÚDO:**` e `**NOTAS**` com negrito (o original pode ter `OBJETIVO:` solto).
- `FALTA:` só onde falta dado. `FALTA: nenhuma.` não é falta: apague a linha (o leitor também a ignora, mas o contrato fica limpo). Com `[A CONFIRMAR: ...]` na mesma linha, a nota leva só o colchete; o texto inteiro fica no `roteiro.md` e no comentário do esqueleto.
- Parágrafo de premissa antes do primeiro `###`: deixe lá; o leitor o ignora. Se ele traz pendência (por exemplo "[A CONFIRMAR: minuto real]"), copie a pendência pro `trabalho/slides/_operador.md`.
- Fases: um `## Fase X · Nome` antes do primeiro slide de cada fase. O X é uma letra, A, B, C na ordem das fases do roteiro (o roteiro do dono quase nunca traz letra: você a põe; um trecho de uma fase só é `## Fase A · Nome`). É isso que define o bloco (`data-bloco`) e, com ele, a troca de fundo. O nome vem do dono, inteiro, com o ponto médio interno se tiver ("FASE AÇÃO · OFERTA & FECHO" vira "## Fase A · Ação · Oferta & Fecho"); a letra do dono, como "FASE M", cede à ordem A, B, C. Mas título de fase todo em caixa alta ("FASE AÇÃO") vira Capitalizado ("Fase A · Ação"): caixa alta de grito não vai pro deck. Sigla conhecida continua em caixa alta (A PUV, A IA, CTA). Sem `##`, o deck inteiro vira um bloco só, "Aula".
- Nomes próprios do dono: liste em `trabalho/termos-do-dono.txt`, um por linha, o nome de cada módulo, bônus e marca que o roteiro traz (o nome próprio inteiro, na grafia do roteiro). Sem nome próprio, o arquivo vazio vale e não gera aviso. O lint do fecho barra alguns desses nomes (a família do verbo-freio e outras muletas); o `montar_desenho.py` os mascara só no texto que manda ao lint e avisa na primeira linha da saída. O deck e as notas ficam como o dono escreveu (`conferencia.md`).
- Marcador de desenho entre colchetes, sozinho numa linha do CONTEÚDO (`[BOTÃO]`): não é texto de tela. O esqueleto o tira da tela e o põe na nota como "Obs.: BOTÃO". O botão se desenha a partir do Objetivo ("botão visível") ou dessa linha; pra pedir botão, ponha `[BOTÃO]` numa linha do CONTEÚDO ou "botão" no Objetivo. O texto do botão é a frase do roteiro; o endereço só entra se o dono deu o link (sem ele, o botão fica sem endereço e a pergunta vai pra lista).
- NOTAS do dono com `Objetivo:` dentro: o contrato só tem Objetivo no `**Objetivo:**` do slide. Suba o texto dele pra lá (junte com o que já existe, numa frase) e deixe as NOTAS só com a fala; a nota do deck leva o Objetivo do slide. O Objetivo diz o que o slide faz, sem comparar números: nada de "número maior que o à vista" nem outro valor contra valor. No fecho, o `montar_desenho.py` já manda o Objetivo ao conferidor de fontes como campo de nota; na conferência da divisão, o comando abaixo faz o mesmo.
- Título que você dá a um slide novo (`### Slide NN · título`) entra na peça que o conferidor lê. Use palavras do roteiro (o nome do trecho, uma palavra da fala), nunca fração nem número seu: "primeira metade" vira léxico de frequência fora de nota. Se o conferidor acusar o título, troque por palavras do roteiro ("o começo da pilha", "aplicar e consultoria") e rode de novo.
- Confira que o leitor pegou todos os slides: `python3 scripts/ler_roteiro.py trabalho/roteiro-original.md --resumo` lista um por linha.

## As regras da divisão

1. **Um slide por ideia: o número de slides sai da fala, não de uma cota.** Slide curto é o que já tem uma ideia só e até 25 palavras de fala: fica como está, sem forçar divisão. A ideia manda, não a conta: dois fatos ou duas ideias dividem mesmo num slide de 20 palavras. Fala de 3 frases sobre uma ideia só pode ficar num slide com 3 cliques. Slide com cinco ou mais ideias volta pra mesa: junte o que for da mesma ideia.
2. **Uma ideia por tela, cerca de 10 segundos de fala cada.** Conte cerca de 25 palavras faladas por slide. A conta é só referência de ritmo; passar um pouco não reprova.
3. **A tela é uma frase de até 12 palavras.** Frase completa, que se entende sem a fala. O resto vai pra nota. Exceção: frase que não se divide (uma PUV, uma promessa nomeada) pode ocupar a tela inteira até 20 palavras, que é o teto de bloco do `checar_deck.py`; acima disso, corte em cláusulas (regra 4). Diga a exceção no `_operador.md`. A tela inteira, com o apoio visual, tem um teto só, 40 palavras (`checar_deck.py`; vaga, legenda, tarja e rótulo de bônus não contam).
4. **A fala vai inteira e sem mudar uma palavra para as NOTAS.** Reparta as frases do original pelos slides novos, na ordem. Pode cortar no meio da frase, em fronteira de cláusula (vírgula, ponto e vírgula, "e", "que"), sem mudar palavra nem ordem: a conta de palavras do original e dos slides novos tem que ser igual. Cada slide novo ganha Abre com e Fecha com tirados dessa fala. Três marcas valem como o campo e não contam como palavra (o `conferir_fala.py` as ignora): **"a mesma frase, sem pausa"** (Fecha com quando a última fala é um clique; slide de uma frase só, em que o Abre com é a frase inteira; Abre com que repete o Clique 1) e **"lê a frase da tela"** (Abre com do slide cuja tela traz mais que a fala, ou que só tem tela; escreva assim, sem colchete nem "lê a caixinha") e **linha toda entre parênteses**, como "(segue direto pra garantia)": direção de palco, não fala. Ela fica em `Transição:` na nota e nunca vira Fecha com. Lista repartida em vários slides (8 itens em 2 de 4, 9 em 5 e 4): cada item é a fala de um Clique N e não se escreve duas vezes; o Abre com é a frase de abertura (a da lista no primeiro slide, a do primeiro item nos seguintes) ou "a mesma frase, sem pausa". O slide seguinte abre no item novo; a frase de fecho e a TRANSIÇÃO ficam no último.
5. **Lista e conta entram uma peça por slide, ou uma peça por clique.** Nunca a lista aberta de uma vez. Conta (soma, passo a passo, funil) mostra uma etapa por vez e termina na conclusão. "Peça" é a unidade que entra de uma vez, inteira: um item, uma cláusula, uma etapa. É a mesma coisa que o guia chama de "bloco" em "um bloco por clique, inteiro de uma vez": nunca meia peça, nem vários itens num clique. No modo agente vale "uma peça por clique", com teto de 7 cliques por slide (o `checar_deck.py` reprova acima). Fala de uns 10 segundos pode ter até esse teto quando as peças são curtas (6 cliques numa frase repartida em cláusulas passaram nos testes); se passar de 7, divida o slide: lista de mais de 7 peças vai em 2 slides, metade em cada (9: 5 e 4), e no segundo as do primeiro já estão na tela, apagadas e sem clique.
6. **Resultado afirmado vira vaga de print.** Vale pro resultado de terceiros ou do dono em venda (faturamento, alunos, painel, depoimento), não pra dívida, quebra ou outro fato pessoal contado em história. Sem o print, o slide ganha na CONTEÚDO a linha `FALTA: print ou recibo de <o que>` e, no desenho, uma vaga tracejada com `data-vaga` (receita `print-moldura`). Painel de funil (inscritos, comparecimento, conversão): uma vaga só, no slide do resultado principal, e as outras cifras na mesma pergunta. Slide do roteiro com dois cases, cada um com o seu resultado: uma vaga por case. Sem print, o número fica sem prova visível e isso vai pro relato.
7. **NADA NOVO.** Todo número, nome, preço, prazo, resultado e depoimento da divisão vem do roteiro, com o mesmo rótulo ("gerenciou" continua "gerenciou"). Nenhum exemplo seu, nenhum dado de mercado, nenhuma cena inventada.
8. **Trecho cujo dado não existe sai do deck e vira pergunta.** Dado de mercado sem fonte, número sem origem: o slide fica no roteiro sem CONTEÚDO, só com `**FALTA:** <o que falta>`. O esqueleto o tira do deck e o põe no `_operador.md` como pergunta, e ela entra na lista final do relato. Exceção, a cena: se o slide tem tela própria e a cena concreta é que falta, ele fica, com uma vaga de cena (`cena: [o que falta]`, `data-vaga`), a nota leva [A CONFIRMAR] e a pergunta vai pro `_operador.md`; é a vaga de print, só que de cena, e conta nas vagas do relato.
9. **Renumere as transições.** "Corta pro slide 02" do original vira o número novo.

## Conferir a divisão (2 minutos)

Antes do esqueleto, confirme que nada entrou que o dono não escreveu:

```
D=$(mktemp -d); grep -v '^<!-- Origem' trabalho/roteiro.md | sed 's/^\*\*Objetivo:\*\*/NOTA: Objetivo:/' > $D/roteiro-sem-origem.md
python3 scripts/conferir_fontes.py --entrega $D/roteiro-sem-origem.md --insumo trabalho/roteiro-original.md
```

A primeira linha tira o comentário `<!-- Origem: ... -->` da cópia que vai ao conferidor (ele o leria como número sem fonte, a contagem "dividido em 13") e marca o `**Objetivo:**` como nota (diz o que o slide faz, não é peça de tela). O `roteiro.md` não muda. Rascunhos e cópias de teste ficam na pasta temporária do sistema, nunca em `trabalho/`.

A fala não mudou? `python3 scripts/conferir_fala.py` (sem argumentos, compara `trabalho/roteiro-original.md` com `trabalho/roteiro.md`) junta a fala de todos os slides (Abre com, Clique N, fala solta, Fecha com, TRANSIÇÃO), tira pontuação, maiúscula, espaço e o que vai entre colchetes, e compara a sequência de palavras. Diz IGUAL, ou DIFERENTE com as primeiras diferenças (código 1). Ele ignora "a mesma frase, sem pausa" (em Abre com, Clique ou Fecha com), "lê a frase da tela", a linha toda entre parênteses (direção de palco) e o número depois de "slide" na TRANSIÇÃO (a divisão renumera). Também avisa palavra de CONTEÚDO que o original não traz. Repita até IGUAL.

Leia a linha `sem fonte fora de nota`: tem que ser 0. Uma linha de léxico por causa da palavra "vaga" (de print) não reprova a divisão. Número com fonte ausente volta pro roteiro original ou sai.

Depois o fluxo segue: `ler_roteiro.py trabalho/roteiro.md --esqueleto trabalho/slides`. No fecho do deck, o insumo da conferência de números é o `trabalho/roteiro.md` dividido.

## Perguntas de verificação, slide por slide

- Sobrou frase da fala sem slide? Todo trecho de fala do original está em alguma nota?
- Algum slide novo tem duas ideias? Divida de novo.
- Algum slide novo ficou sem fala própria só porque a ideia veio da tela? Marque na nota.
- A ordem do original foi mantida? Dividir não reordena.
