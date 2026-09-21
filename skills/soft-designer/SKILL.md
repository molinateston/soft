---
name: soft-designer
description: >-
  Desenha e entrega o ARQUIVO visual de uma peça: banner ou criativo de anúncio, carrossel em PNG 1080x1350, deck de slides 16:9, página em HTML, capa ou thumbnail. Escreve a copy curta que vai DENTRO do desenho. Âncora: o TEXTO do carrossel é da soft-conteudo-carrossel, a ARTE é daqui. Use quando o pedido for: "renderiza o carrossel em PNG", "cria o banner do anúncio", "desenha os slides", "monta o visual disso", "transforma essa copy em arte", "exporta os PNGs", "faz a capa", "monta a thumbnail", "faz a página em HTML", "me mostra como fica". NÃO use pra: "faz um carrossel" quando o dono quer o TEXTO slide a slide (soft-conteudo-carrossel); a headline de texto (soft-conteudo-headlines); a carta (soft-funil-carta); o lote de criativos com ângulo por peça (soft-criativo-campeao); o reel curto (soft-reel-7seg); o vídeo (soft-editor-video); a apostila (soft-apostila); o card print de tweet (soft-tweet-card); o deck em PPTX (soft-apresentacao). Leia e siga o fluxo inteiro do SKILL.md.
---

# Designer, a peça visual pronta pra postar

Esta skill pega uma tese ou uma copy e devolve o arquivo visual final: o banner do anúncio, os PNGs do carrossel, o deck de slides, a página em HTML ou a capa. O valor próprio é a engenharia visual (3 famílias de estilo, tipografia editorial, render HTML/CSS para PNG) somada a um trabalho de copy: a skill escreve a copy que vai NO desenho, porque texto curto de peça visual é arte própria, e passa essa copy pelo gate antes de desenhar.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**O render NUNCA aplica caixa alta na headline.** `text-transform: uppercase` não entra em manchete, capa, título de slide, título de card nem em qualquer texto grande que o leitor lê como a frase da peça: ênfase é por palavra, não por tecla, e a caixa alta engorda a linha, come a área segura e derruba a leitura no celular. **O versalete (small caps) e a caixa alta continuam liberados em três lugares e só neles:** tag ou etiqueta (`.slide-label`, `.tag`), rótulo de rodapé, e cabeçalho pequeno de topo, todos até 16px. Antes de exportar, confira que nenhuma regra de caixa alta alcança a classe da manchete, e cole `regras de caixa alta no render: N · alcançando a manchete: 0`. O `checar_titulos.py --render <arquivo.html>` e o `--conferir` leem os títulos do HTML e do deck e reprovam com `título em caixa alta: <linha>`.

**Os arquivos que cada ação exige (`--exige`).** Conferência: `--conferir <pasta> --exige <lista>`. Carrossel PNG: `--exige *.png,preview.html`; banner: `--exige *.png`; deck animado: `--exige index.html`; capa ou thumbnail: `--exige *.png`; prompt de imagem: `--exige prompt-de-imagem.md`. Arquivo ausente sai com exit 1.

**Pedido que nomeia evento, turma ou data: ao menos uma peça carrega a razão de agir agora.** Rode `grep -niE 'turma|vagas|come[çc]a|aula ao vivo|[0-9]{2}/[0-9]{2}' <perfil>` e cole a saída. O que voltar entra em pelo menos uma peça, com o número literal. Cole `peças no lote: N · com razão de agir agora: N`, e zero na segunda coluna, num pedido que nomeia turma ou evento, reprova o lote.

**Todo campo preenchido do JSON de identidade carrega a origem no próprio arquivo.** Some um objeto `origens` com uma entrada por campo preenchido, no formato `"<campo>": "<arquivo>:<linha>"`. Campo com valor e sem entrada em `origens` reprova, inclusive `@` de perfil, texto de selo e CTA. Cole `campos preenchidos: N · com origem apontada: N`, iguais. `null` com pendência declarada é resultado correto e dispensa origem.

**O HTML se confere no corpo montado, nunca no arquivo.** Rode o grep de marcador e de frase de bastidor (`entra aqui|preencher|antes de publicar|placeholder|a definir|pendente`) sobre o **texto que o HTML renderiza**: página que monta o corpo por script esconde o marcador da varredura estática, e a peça pública não carrega bastidor renderizado. Cole `marcadores no corpo renderizado: 0 · frases de bastidor renderizadas: 0`.

**A peça de render entra na lista do lint, e o conflito com a fonte tem saída escrita.** `preview.html` é o primeiro nome da lista. Quando a copy herdada reprovar, o render NÃO reescreve: cole `origem reprovada no lint: <arquivo> · falha: <a literal> · presente na fonte: sim` e devolva a linha à skill de origem como `volta pra <skill>: <a frase>`. A entrega sai; o que não pode é a peça sumir da contagem. `arquivos linteados: N` sem o arquivo da peça reprova o gate, mesmo com todos os exit 0.

**O gate de literal no gerador lê o AST, porque concatenação derrota o grep.** Rode e cole a saída:

```
python3 -c "import ast,sys; t=ast.parse(open(sys.argv[1]).read()); print(max((len(n.value) for n in ast.walk(t) if isinstance(n,ast.Constant) and isinstance(n.value,str)), default=0))" <gerador>
```

Acima de 39 reprova, e strings adjacentes contam como uma só. Além disso, `diff` entre o texto extraído do HTML de render e o texto da fonte, colado inteiro: **qualquer linha de diferença reprova o render**, com ou sem justificativa, porque a skill de arte não tem autoridade sobre a copy. **`str.replace()`, `re.sub()`, `.upper()`, `.title()` e literal de texto do dono dentro do gerador são proibidos, com duas exceções e só duas: remoção de nome sem autorização e remoção de marcador.** O `--conferir` varre os `.py` da pasta e reprova com `gerador reescreve a copy` quando acha uma dessas chamadas; o gerador formata (quebra de linha, hierarquia, tamanho), nunca troca a palavra. Cole `linhas de diferença: N · autorizadas: N`, iguais.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício de nicho neutro passando pelas 5 ações: o briefing que o dono deu, as perguntas que a skill fez, a copy-visual de cada card, o preview, a conferência do render com o que foi visto e a lista final de arquivos. Ler aquilo antes da primeira pergunta economiza uma rodada de retrabalho.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a copy e a identidade e eu renderizo a arte). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra o render com a copy e a identidade que o dono já colou. Se faltar um insumo que a arte não vive sem (o texto que vai na peça, ou a cor/fonte da marca), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o briefing uma pergunta de cada vez (o formato, a copy-visual, a paleta/identidade) antes de renderizar.

A pergunta do modo é UMA por peça. Mais duas partes entram nas ações abaixo:

- **Ensina enquanto faz:** ao decidir a hierarquia visual (o que domina o card, o que é apoio), escreve UMA linha do porquê ("dou o maior peso à promessa e encolho o selo porque no feed a primeira leitura é a headline; selo grande rouba o olho do que converte"), pra o dono decidir sozinho na próxima.
- **Oferece refinar no fim:** depois de mostrar o preview, fecha com UMA linha de ajuste ("quer outra cor de fundo? a headline maior? outro corte? refaço só o card que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "faz o banner", "cria o criativo", "arte do anúncio", "imagem pro tráfego", "peça pra impulsionar" | **1 · BANNER** |
| "faz o carrossel", "monta os slides do post", "exporta os PNGs", "transforma essa copy em carrossel" | **2 · CARROSSEL** |
| "desenha os slides", "monta o deck", "apresentação", "slides da aula", "16:9" | **3 · SLIDES** |
| "faz a página", "monta em HTML", "página de evento", "veste essa copy de página" | **4 · PÁGINA** |
| "faz a capa", "monta a thumbnail", "a imagem de abertura", "capa do vídeo", "capa do carrossel sozinha" | **5 · CAPA** |

Pedido ambíguo ("faz o visual disso", "deixa bonito"): pergunte UMA coisa só, onde essa peça vai ser publicada, mostre a tabela acima como cardápio e siga pela resposta.

## Como ler cada ação

Toda ação abaixo traz o mesmo bloco fixo: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · passos numerados com **STOP**.

**O perfil do dono vem do banco do agente.** Onde qualquer ação precisar de identidade visual, avatar, voz, prova ou nicho: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" da ação e siga com o que faltar marcado `[A CONFIRMAR]`. Nunca invente cor de marca, nunca invente número, nunca pare por causa disso.

**As 6 leis (valem antes de tudo):** (1) a copy que vai no visual nunca assume que o cliente já sabe o contexto, zero palavra difícil; (2) abre ensinando o que faz; (3) é consultiva, puxa do dono a família, a cor e o formato antes de desenhar; (4) contexto é rei, o layout flutua pela função da peça; (5) admite se faltar insumo, nunca inventa: sem prova, número ou cor de marca, pergunta ou marca `[A CONFIRMAR]`; (6) saída enxuta, só a peça, zero meta-narração, zero tabela de gate impressa. Detalhe em `shared-references/operacao-padrao.md`, Seção 0.

**Os 4 passos comuns a TODAS as ações** (cada ação abaixo diz o que muda neles):

**A · Ancora a copy-visual.** Puxa o verbatim real do público (`shared-references/crivo/01-entrada-verbatim.md`), escreve uma frase por peça na espinha, cada uma com UMA ideia comprimida (`shared-references/crivo/05-premissas-mestras.md`), e passa pelo gate de copy `shared-references/crivo/03-gate-cub.md` (CUB por peça, as 3 perguntas na capa: dá pra ver a cena? é falsificável? só este cliente diria?). Nicho regulado roda também `04-gate-regulado.md`. Anti-IA por `shared-references/filtro-anti-ia/`; quando o ambiente rodar shell, `python3 scripts/lint_copy.py <arquivo>`.

**B · Aplica a identidade do cliente OU escolhe família.** Leia `references/identidade-visual-cliente.md`. Se o dono já tem identidade (no perfil, ou anexou referência, ou disse "igual ao último"), aplica a marca dele e pula as perguntas. Se não tem, escolhe entre as 3 famílias:

| Família | Quando usar |
|---|---|
| **Editorial Preto** | Posicionamento, manifesto, oferta premium, autoridade. Vibe revista de negócios. |
| **Clínico Branco** | Listas, comparativos, ofertas diretas, prova de números. Vibe bula bem desenhada. (default mais seguro) |
| **Manuscrito Cru** | Storytelling pessoal, confissão, antes e depois. Vibe print de rede social. |

Sem família indicada, PARE e pergunte seguindo `references/perguntas-design.md` (3 perguntas no máximo, opções nomeadas, nunca exige hex). Fallback "decide você": Clínico Branco com um accent neutro, avisa que é neutro e oferece salvar como a identidade dele.

**A identidade do dono é lei, e vence a cor default da família.** Cor de fundo e de acento vêm do perfil do dono ou do onboarding, nunca do gosto da família: dono que declarou fundo off-white recebe off-white, mesmo que a família escolhida peça branco puro ou preto, e a adaptação preserva a régua de contraste e de área focal. Nenhuma cor nova entra na peça sem o dono pedir, o que inclui uma segunda cor de destaque pra marcar erro, negativo ou alerta: a peça tem UMA cor de acento e ponto. Copy aprovada não se reescreve no render: quando o texto chega pronto, ele é imutável, ajuste só quebra de linha e hierarquia, e todo corte precisa ser declarado ao dono.

**C · Escreve o HTML.** Sempre gera o HTML por um script em Python, nunca por heredoc de shell (`$` e crase corrompem strings). `scripts/build_carousel.py` é o esqueleto, `assets/template-base.html` o template. Regras inegociáveis do desenho: fundo chapado (sem gradiente nem textura) · hierarquia de 2 níveis no máximo · espaço negativo de 30 a 50% · UMA cor de destaque por peça, teto de 4 palavras · negrito é acento, nunca parágrafo inteiro · tipografia mista é assinatura, nunca serif e sans no mesmo título · zero sombra, zero ícone colorido, cantos retos. Antes de gerar, leia a reference da família escolhida mais `references/escala-densidade.md`, `references/tipografia-quebra-linhas.md` e, no carrossel, `references/setinha-arraste.md`. Padding de 100px nos 4 lados. **Quebra de linha se mede no PNG, e nunca se decide no HTML.** É proibido `<br>` dentro de parágrafo de corpo: a quebra é da caixa (`max-width` em `ch`), e o `<br>` só entra em headline curta escrita pra quebrar naquele ponto. Antes de exportar, olhe o texto renderizado de cada slide: nenhuma linha pode ficar com menos de 4 palavras, exceto a última do parágrafo. Cole `slides: N · linhas órfãs (menos de 4 palavras fora da última): 0`, e qualquer valor maior manda o slide de volta pro ajuste de caixa, nunca pro corte do texto.

**Nome de terceiro nunca entra em pixel, e a pergunta da autorização vem antes do render.** Antes de renderizar, rode `grep -in 'autoriz' <perfil>`; sem uma linha do perfil autorizando o nome em peça pública, a arte sai com o papel (`uma aluna`) e a dúvida vai pro relato antes do render. `python3 scripts/checar_titulos.py --render <html> --perfil <perfil>` reprova nome sem autorização no HTML antes de exportar. Cole `nomes de terceiro na arte: 0 · autorizações citadas no perfil: N`.

**Nenhum card sai com marca d'água de teste na arte.** Antes de renderizar, rode e cole a saída:

```
grep -rniE 'teste|test|placeholder|sample|lorem|sintetico' <manifesto> <pasta de assets>
```

Frame de teste prova o pipeline e **nunca entra na peça entregue**: achado na saída, o frame sai do manifesto e a peça vira PARCIAL, sem render. Sem foto real, o card sai com tratamento de fundo declarado e sem imagem. Cole `cards com texto de teste na arte: 0`.

**O número colado é copiado da saída, não redigitado.** Redirecione a saída do contador pra um arquivo e cole o arquivo: `<comando do contador> > contagem.txt`, depois `cat contagem.txt` colado inteiro. Número redigitado que não reproduz reprova a contagem, mesmo quando o veredito é o certo.

**A varredura de imagem no disco roda antes de marcar PARCIAL.** Rode e cole a saída, inclusive vazia:

```
find <pasta de insumos> -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.mp4' -o -iname '*.mov'
```

**Vídeo conta como fonte:** havendo `.mp4` ou `.mov`, extraia os frames com `ffmpeg -i <video> -vf fps=1/4 -frames:v 4 frame-%02d.png` e use na peça. **Marcar PARCIAL sem a saída do find colada reprova a entrega.**

**As duas regras do render se conferem por comando, antes de exportar.** Cole as duas saídas:

```
grep -c '<br>' <html de render>          # não pode passar do número de headlines declaradas
python3 scripts/checar_titulos.py --render <html de render>; echo exit=$?   # tem que dar 0
```

`<br>` acima do número de headlines significa quebra à mão dentro de corpo, e reprova: a primeira troca de copy reabre as órfãs, porque a quebra não é da caixa. O `--render` reprova marcador de pendência antes do PNG, porque marcador no HTML vira tinta e PNG não se corrige por colagem. **E o `--render` mede o PNG, além do HTML:** quando existir PNG com o mesmo nome-base do HTML na pasta, ele imprime `slide <n> | altura da manchete: P% da arte` e marca acima de 45% como alerta ao dono, jamais como falha. Sem a medição, uma manchete de 5 linhas passa igual a uma de 2, porque ninguém confere o pixel final. Cole a linha por slide junto do `exit=0`.

**A headline renderizada é idêntica à declarada, e isso se mede no PNG.** Depois de exportar, abra cada PNG e leia a manchete que aparece na imagem, palavra por palavra, contra a que a checagem declarou. Cole `manchetes renderizadas: N · conferidas no PNG: N · diferentes da declarada: 0`. **Cada PNG se abre UMA vez por volta, e só o que mudou.** Na primeira volta você abre os PNGs da peça; na segunda, abre só os que foram re-renderizados depois da correção. PNG que já passou nunca se reabre, e PNG que ninguém tocou nunca se relê: imagem aberta é o item mais caro do turno, e reler o lote inteiro a cada volta já queimou a cota de 5 horas de um dono num logo só. **Qualquer diferença reprova o slide**, inclusive pontuação e caixa: o que o dono publica é o pixel, e a checagem que confere só o HTML valida um arquivo que ninguém vê.

**D · Confere o render com o olho, roda o gate e entrega.** É o Passo de CONFERÊNCIA descrito na seção própria abaixo, e ele é obrigatório em toda ação. Sem ele a skill trabalha cega.

---

## Ação 1 · BANNER (criativo de anúncio)

**O que faz:** desenha o criativo estático de tráfego, uma mensagem só, com o CTA visual que o destino do clique exige.

**Precisa de:** a tese ou a promessa do anúncio, do pedido do dono ou de uma skill de conteúdo · o destino do clique (o que a pessoa encontra depois de clicar), perguntado ao dono · a identidade visual, do perfil/brain do agente.

**Sem o insumo:** entrevista curta de 3 perguntas: o que esse anúncio promete em uma frase · pra onde a pessoa vai quando clica · qual formato a plataforma pede (quadrado, vertical, feed). Sem identidade declarada, use o fallback neutro do Passo B e diga em 1 linha que a cor é provisória.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `banner-<nome>.png` no diretório de saída do ambiente (`$OUTDIR`, ou a working dir quando não houver), mais o `preview.html` que gerou. Nos ambientes que renderizam HTML, o HTML renderizado já é a entrega visível.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/processo-banner.md` (a anatomia e a biblioteca de modelos).

**Profundidade:** `references/layouts.md` · `references/tipografia.md` · `references/layout-utilitario.md`.

**Passos:** A (a copy-visual do banner são 3 elementos só: a headline que para, a copy-curta de apoio que se corta quando não soma, e o CTA) → B → C (um ponto focal só: hook OU número OU imagem, nunca dois) → **STOP: mostra o preview e pergunta "o que ajusto antes de eu exportar?"** → D (conferência + gate) → exporta.

---

## Ação 2 · CARROSSEL (PNG 1080x1350)

**O que faz:** transforma a copy aprovada do carrossel nos PNGs numerados, prontos pra postar.

**Precisa de:** a copy do carrossel já escrita, de `soft-conteudo-carrossel` ou do dono (pode vir numerada, em markdown, ou texto solto) · a identidade visual, do perfil/brain do agente.

**Sem o insumo:** com só o tema na mão, escreva você a copy-visual dos cards no Passo A, uma frase por card, e avise em 1 linha que a copy nasceu aqui e precisa do OK do dono antes do desenho. Sem identidade, fallback neutro do Passo B.

**Entrega:** `slide_01.png`, `slide_02.png` em diante (zero-padding de 2 dígitos) no diretório de saída, mais `preview.html`. Estrutura recomendada: 7 a 10 slides. Se vier fora disso, desenha o que veio e avisa.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/processo-design.md` (o pipeline completo) · `references/deteccao-automatica.md` (inferir a função de cada card).

**Profundidade:** `references/carrossel-embalagens.md` · `references/setinha-arraste.md` · `references/layout-tweet-avatar.md` · `references/layout-diagrama-manuscrito.md` · `references/elementos-manuscritos.md`.

**Passos:** A → identifica a função de cada card (hook, problema, virada, método, prova, oferta, CTA) e **declara a lista de funções detectadas ao dono antes de desenhar**, que é a única chance dele corrigir → B → C, com a régua de ritmo abaixo → **STOP: "quais slides precisam de ajuste antes de eu exportar os PNGs?"** → D → exporta.

**Régua de ritmo do carrossel:** a hierarquia de 2 níveis é teto, não obrigação. Se 3 ou mais cards seguidos repetem o mesmo molde, mude a forma pela função: afirmação pura na virada, tópicos quando a enumeração pede escaneabilidade, prosa para narrativa, número dominante na prova. Caixa ou chip só quando agrupa uma unidade real. Não converta tudo em card, nem reduza tudo a parágrafo plano. Seta de arraste e handle nos slides 1 a N-1. Ajuste pedido edita SÓ o slide mencionado, nunca regenera o carrossel inteiro.

---

## Ação 3 · SLIDES (deck 16:9)

**O que faz:** veste um roteiro ou uma lista de teses de deck 16:9, um assunto por slide, lido em 3 segundos.

**Precisa de:** o roteiro ou a lista de teses por slide, do dono ou de uma skill de roteiro · a identidade visual, do perfil/brain do agente · se há apresentador em cena e onde fica a câmera, perguntado ao dono.

**Sem o insumo:** entrevista curta de 3 perguntas: qual o argumento da apresentação em uma frase · quantos slides ou quanto tempo de fala · é guiada pela fala ou feita pra ler sozinha. Guiada pela fala vai densidade baixa (uma ideia, headline grande, 1 a 3 pontos); feita pra ler vai densidade alta (contexto suficiente no próprio slide).

**Entrega:** `deck.html` navegável mais `slide_01.png` em diante no diretório de saída.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/processo-slides.md` (a espinha de tensão do deck e os tipos de slide).

**Profundidade:** `references/escala-densidade.md` · `references/layouts.md` · `references/tipografia.md`.

**Passos:** A (a copy-visual aqui é o título e o conteúdo de cada slide; a fala chega pronta e não entra na tela) → B → C, palco fixo de 16:9, câmera reservada na mesma posição em todos os slides quando houver apresentador → **STOP: mostra o preview do deck e pergunta o que ajustar** → D → exporta.

Quando o pedido for PPTX, PDF paginado ou o deck com notas de fala exportadas, essa é a **soft-apresentacao**; esta ação para no HTML e nos PNGs.

---

## Ação 4 · PÁGINA (HTML)

**O que faz:** veste uma copy de página já escrita com a pele visual do método, em HTML de arquivo único.

**Precisa de:** a copy da página bloco a bloco, de `soft-funil-landing` ou do dono · a identidade visual, do perfil/brain do agente · o destino do botão (link do checkout, do formulário ou do WhatsApp), perguntado ao dono.

**Sem o insumo:** sem a copy bloco a bloco, pergunte UMA coisa: "me manda a copy da página, na ordem em que ela aparece na tela". Sem o destino do botão, deixe o `href` marcado `[A CONFIRMAR]` no HTML e avise em 1 linha, nunca invente um link.

**Entrega:** `pagina-<nome>.html`, arquivo único (CSS embutido, sem build, sem framework), no diretório de saída. Nos ambientes que renderizam HTML, a página renderizada é a entrega visível.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/identidade-visual-cliente.md` · a reference da família escolhida.

**Profundidade:** `references/tipografia.md` · `references/tipografia-quebra-linhas.md` · `shared-references/filtro-mobile-first/`.

**Passos:** A (a copy chega pronta; aqui você só afia o que vai virar título de bloco) → B → C, fundo chapado, um accent, tipografia editorial, cantos retos, e a página tem que ler bem no celular antes de ler bem no monitor → **STOP: mostra a página e pergunta o que ajustar** → D (a conferência aqui olha a página em largura de celular e em largura de monitor) → entrega.

---

## Ação 5 · CAPA (capa ou thumbnail)

**O que faz:** desenha a peça única que interrompe o scroll: capa de carrossel isolada, thumbnail de vídeo, imagem de abertura.

**Precisa de:** a promessa da peça em uma frase, do dono · onde a capa vai aparecer (feed, thumbnail de vídeo, topo de página), perguntado ao dono · a identidade visual, do perfil/brain do agente.

**Sem o insumo:** pergunta única: "qual a frase que essa capa precisa entregar, e onde ela vai aparecer?". Com essas duas informações a capa sai inteira.

**Entrega:** `capa-<nome>.png` no formato que o destino pede (1080x1350 no feed, 1280x720 no thumbnail de vídeo), mais o `preview.html`.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/processo-design.md` (o bloco da capa) · `references/tipografia-quebra-linhas.md`.

**Profundidade:** `references/layouts.md` · `references/familia-editorial-preto.md` e as outras duas famílias.

**Passos:** A (a capa é a peça que mais precisa das 3 perguntas do gate: dá pra ver a cena? é falsificável? só este cliente diria?) → B → C → **STOP: mostra a capa e pergunta o que ajustar** → D → exporta.

**Licença da imagem de capa:** quando a capa tiver imagem, ela é a única peça autorizada a liberar absurdo controlado. A cena pode ser impossível, mas precisa comunicar a tese de imediato e nunca virar enfeite desconectado. Isso não torna imagem obrigatória em toda capa.

---

## Passo D · CONFERÊNCIA do render (obrigatório, é o que tira a skill da cegueira)

Peça renderizada que ninguém olhou é peça não entregue. Antes de dar qualquer arte por pronta, você CONFERE o arquivo que saiu, não o código que você escreveu.

**Orçamento declarado, antes e depois (o custo aparece no chat, nunca só na fatura).** Antes de abrir o primeiro PNG, escreva ao dono uma linha: `Orçamento: N peças · até 2 voltas de conferência cada`. No fecho da entrega, cole `PNGs abertos: N`, contado, nunca estimado. **O teto duro do pedido é N peças vezes 2 voltas, mais N** (a passada de fechamento). Bateu o teto com peça ainda reprovada, você para na hora e avisa: `teto de PNGs atingido: N · falta conferir: <lista>`. Entrega com `PNGs abertos` acima do teto reprova, mesmo com toda peça bonita.

**Quando o ambiente tem leitor de imagem** (a capacidade de abrir e ver um PNG ou um JPG):

1. Abra a imagem gerada, uma por uma. No carrossel e no deck, abra também o mosaico quando houver, e depois abra em tamanho cheio todo card que parecer denso ou suspeito.
2. Olhe cada peça procurando, nesta ordem: **texto cortado** (frase que some na borda, palavra que sai do quadro, bloco que estourou o container) · **safe area** (nada de texto encostando na borda nem invadindo a área da câmera, do rosto ou do chrome da plataforma; padding de 100px preservado) · **contraste** (o texto se lê contra o fundo imediato atrás dele, sem "eu sei que está lá mas mal enxergo") · **órfã** (palavra sozinha na última linha de um bloco) · **sobreposição** (elemento por cima de outro) · **legibilidade em miniatura** (reduza mentalmente a peça a um thumbnail: a mensagem principal ainda chega?).
3. **Liste ao dono o que você conferiu e o que viu**, em 3 a 6 linhas, peça por peça quando forem poucas ou por lote quando forem muitas. Exemplo do formato: "abri os 9 PNGs; slide 4 tinha a palavra 'agora' sozinha na última linha, corrigi; slide 7 tinha o número encostando na borda de baixo, subi 40px; os outros 7 passaram limpos".
4. **Confira a identidade contra o declarado, sempre, mesmo sem enxergar a peça.** Extraia do HTML a lista de cores que entraram no render (com shell: `grep -oiE '#[0-9a-f]{3,8}' <caminho>/preview.html | sort -u`) e confronte uma a uma com o fundo e o acento que o dono declarou. Cor que não estiver no perfil do dono não pode aparecer, e a peça tem um acento só: um segundo tom de destaque, mesmo pra marcar erro ou negativo, reprova e volta pro Passo C. Quando a copy chegou pronta, compare também o texto renderizado contra a fonte, palavra por palavra.
5. Achou problema, corrige o HTML, re-renderiza e **confere de novo**. **O teto é de 2 voltas por peça**: renderiza, confere, corrige, renderiza de novo, confere de novo, e acabou. Reprovou na segunda volta, você PARA e entrega ao dono o que saiu, com a lista do que ficou reprovado, peça por peça, na forma `<arquivo> · reprovado em: <o quê>`. Quem decide pagar uma terceira volta é o dono, nunca a skill: cada volta reabre PNG, e PNG aberto por conta própria gasta a cota dele sem ele saber.

**Quando o ambiente NÃO tem leitor de imagem** (você não consegue abrir o PNG):

1. Confira por medida, no código e pelo script. Rode, quando houver shell, `python3 scripts/craft.py audit <caminho>/preview.html`: ele reprova em código o contraste insuficiente (luminância WCAG) e sinaliza órfã provável. O `export_pngs.py` já chama esse gate sozinho e recusa exportar peça com falha dura.
2. Confira os números que dá pra conferir sem ver: contagem de caracteres por bloco contra a escala de `references/escala-densidade.md`, padding declarado no CSS, dimensão do viewport, quantidade de arquivos gerados e tamanho de cada um (arquivo de poucos bytes é render vazio).
3. **Declare ao dono, em 1 linha, que você não viu a peça**: "não tenho leitor de imagem aqui, conferi por medida (contraste pelo craft.py, contagem de caracteres, padding e dimensão); a conferência visual de corte e sobreposição fica com você antes de postar".

Nunca diga que conferiu o visual quando não abriu a imagem. Peça exportada sem conferência declarada é entrega incompleta.

## Gate de qualidade (roda por dentro, a tabela nunca vai pra saída)

**Número não confirmado nunca vira pixel (a arte publicada não carrega ressalva).** Antes de renderizar, rode `grep -n 'A CONFIRMAR' <perfil do dono>`, extraia cada valor marcado, e rode `grep -nF '<valor>' <copy da peça>` por valor, colando as duas saídas. Valor marcado sai da frase e entra a forma sem número ("algumas semanas", "depois de um tempo"), nunca o marcador e nunca o número cru: o card sai no feed sozinho, e quem lê não vê a ressalva que ficou no bastidor. Cole `valores não confirmados no perfil: N · renderizados na arte: 0`, e qualquer número acima de zero na segunda coluna reprova o render antes de exportar.

**Capa que chega pronta na copy fonte não se troca por outra pior.** Quando a peça nasce de uma copy que já tem capa ou headline escolhida, a capa da fonte é a linha a bater, nunca a linha a descartar por hábito. Cole `capa da fonte: <literal> · capa publicada: <literal> · motivo da troca: <escrito>`, passe a publicada pela régua com o gatilho nomeado, e feche com `manchetes idênticas à fonte: N de N`. **Capa publicada em molde `Como <resultado> sem <obstáculo>` reprova a troca**: é o molde mais batido do mercado, e é o que a régua existe pra superar. Sem motivo escrito, a capa da fonte volta.

**Os gates de arte saem em linha de saída, cada um com o comando literal ao lado.** Prosa não conta como contagem, e foi por isso que três exigências passaram sem número em duas entregas seguidas. O passo de render fecha com estas linhas, uma por linha, na forma `<gate>: <valor> | comando: <literal>`, cada uma com a saída crua colada acima dela:

```
realpath config: <saída> | comando: realpath <caminho do config do dono>
realpath skill: <saída> | comando: realpath <pasta desta skill>
a primeira começa pela segunda: não | comando: a comparação das duas saídas acima
cores medidas no PNG: <lista hex> | comando: python3 -c "from PIL import Image; ..." ou o medidor da skill
imagens fortes no PNG: N de N exigidas | comando: a contagem sobre os arquivos renderizados
cards com GIF: N de N exigidos | comando: ls *.gif
geradores testados: N (mínimo 2) · falharam: N | comando: um por linha na forma `gerador: X | testado: sim | resultado: Y`
```

Qualquer uma dessas linhas ausente reprova antes da análise de arte, e declarar sem a saída colada não conta como feito.


**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.


Roda depois da conferência, lendo CADA peça. Só peça com VEREDITO PASSA sai. Uma falha corrige o desenho daquela peça e re-roda.

| Check | Passa se |
|---|---|
| **Título** | é o único bloco com peso forte por padrão, cria entrada clara sem disputar com corpo e imagem |
| **Corpo** | peso normal 400 ou 500; parágrafo inteiro em negrito reprova |
| **Destaque** | a cor de accent marca só a palavra ou o trecho decisivo, teto de 4 palavras; destaque espalhado reprova |
| **Quebra útil** | traço, linha, caixa ou diagrama explica relação, separa virada ou agrupa unidade; ornamento sem função reprova |
| **Contraste** | cada bloco tem contraste forte contra o fundo imediato (mira 3:1, corpo em 4.5:1). Pele clara pede texto escuro e accent escuro; pele escura pede texto claro. Texto claro em fundo claro reprova automático |
| **Anti-órfã** | nenhuma palavra sozinha na última linha de um bloco; termo composto quebrado entre linhas reprova. Com shell, `nw()` de `scripts/craft.py` envolve todo texto de peça; sem shell, quebra manual com `<br>` |
| **Diagrama forte** | se a peça tem diagrama: traço de 5 a 6px, marcador semântico e rótulo do que cada parte é. Sem diagrama, não se aplica |
| **1 ideia por peça** | o card ou slide carrega UMA ideia fechando numa frase; duas mensagens competindo reprova |
| **Legível no celular** | o título se lê sem esforço numa tela de 6cm, escala bate com `references/escala-densidade.md` |
| **Fundo chapado e 1 accent** | cor sólida sem gradiente, um accent só, zero sombra, cantos retos; carrossel com seta e handle nos slides 1 a N-1 |
| **Handle uma vez por slide, e na capa só no rodapé** | conte as ocorrências do handle em cada slide: `slide N: handle Nx`. Passa só com 1 em cada. **O slide 1 é o que erra:** a capa costuma receber o handle do cabeçalho da arte e de novo o do rodapé de arraste. Na capa o handle vive **só no rodapé**, junto da seta; cabeçalho da capa não leva handle. Duas ocorrências no mesmo slide reprovam |
| **Nada vazio** | todo elemento estrutural está preenchido; caixa vazia com baixa opacidade parece bug de carregamento e reprova |
| **Anti-IA** | zero travessão longo na copy-visual, zero da família do verbo-freio banido pela régua anti-voz, zero frase-emoldura. Com shell, `python3 scripts/lint_copy.py <arquivo>`; sem shell, busca manual dos dois |
| **Render não mudou palavra (prova colada, slide a slide)** | o texto desenhado é exatamente o que passou no gate de copy do Passo A. Quando a copy chegou pronta do dono, **renderizar não é editar**: monte uma tabela com uma linha por slide, colando a linha da fonte e o texto que foi pro render lado a lado, e conte as orações das duas. Passa só com as duas colunas idênticas fora quebra de linha. **Reprova automático:** oração cortada, enumeração condensada, prosa da fonte virando lista ou tabela, e lista da fonte virando prosa. Copy que não cabe no card não se resume: reduz o corpo da fonte, ou pede ao dono a versão curta, e o que foi feito vai declarado em 1 linha |
| **Identidade do dono respeitada** | as cores usadas no render batem com as declaradas pelo dono. Liste os hex que saíram na peça e confronte com o perfil: fundo e acento fora do declarado reprova, e qualquer cor de acento além da primeira reprova mesmo que combine |
| **Conferência declarada** | o Passo D rodou e o dono recebeu a lista do que foi conferido, ou o aviso de que a peça não foi vista |
| **`[A CONFIRMAR]` em todo furo** | todo número, prova, cor de marca e link sem fonte está marcado, nunca preenchido com um valor plausível. O marcador vive no doc de handoff, nunca dentro da peça exportada: na arte final, use a versão da frase sem o número ou um espaço neutro, e leve o `[A CONFIRMAR]` pro handoff. Marcador visível no arquivo que vai pro público reprova. |
| **VEREDITO** | é o pior item acima. Uma falha corrige e re-roda. Só tudo aprovado exporta |

## Exportar

Com o gate aprovado e o "pode exportar" do dono, quando há shell:

```bash
python3 scripts/export_pngs.py --html <caminho>/preview.html --output <caminho>/slides
```

O script depende de Playwright e o instala sozinho na primeira execução. **Sem shell ou sem Playwright**, a entrega é o HTML renderizado (nos ambientes que renderizam) ou o arquivo `preview.html` salvo no disco, com 1 linha dizendo ao dono que o PNG precisa ser exportado por ele abrindo o HTML e capturando a tela em 1080x1350. Nunca fique esperando um export que o ambiente não faz.

Entregue só as peças limpas, na ordem, sem tabela de gate e sem meta. Pra leigo, fecha em 1 frase: "pronto, seus 9 slides estão aí na ordem, é só baixar e postar".

## Anti-patterns (sintoma, correção)

| Sintoma | Correção |
|---|---|
| Exportou sem mostrar preview | Volta: mostra preview, pergunta o ajuste, espera o OK |
| Deu por pronto sem abrir a imagem | Roda o Passo D; sem leitor de imagem, confere por medida e declara que não viu |
| Texto claro sobre fundo claro | Cada pele define as próprias cores; re-roda o gate |
| Palavra sozinha na última linha | Aplica `nw()` ou puxa 1 palavra da linha anterior |
| Diagrama com linha fina sem marcador | Traço de 5 a 6px mais marcador mais rótulo |
| 3 ou mais cards seguidos com o mesmo molde | Quebra o ritmo pela função do card |
| Tudo virou caixa, chip ou quadrado | Volta ao texto editorial; mantém só o recurso que explica, agrupa ou prova |
| Corpo inteiro em negrito | Forte só no título e no trecho decisivo |
| Inventou um número plausível | Só prova com lastro; sem fonte, `[A CONFIRMAR]` |
| Render reescreveu a copy | Texto desenhado é o que passou no gate; mexeu, re-passa |
| Regenerou o carrossel inteiro por 1 ajuste | Edita só o slide mencionado |
| Imprimiu a tabela do gate na saída | O gate é interno; a saída é só a peça |

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. Se a skill indicada não estiver instalada, faço aqui em modo reduzido e digo em 1 linha o que ficou de fora.

- A **headline ou o gancho de texto** (não a arte) → **soft-conteudo-headlines**.
- O **corpo de texto longo, caption, roteiro, carta, e-mail** → **soft-conteudo-carrossel**, **soft-conteudo-reels**, **soft-conteudo-stories**, **soft-funil-carta**.
- O **posicionamento, o avatar, o mecanismo** → **soft-plano-posicionamento**.
- A **copy da landing** bloco a bloco → **soft-funil-landing** (a pele visual dela volta pra Ação 4 daqui).
- O **deck do webinar** dentro da esteira → **soft-webinar**.
- O deck **exportado em PPTX, PDF paginado e mosaico**, com notas de fala → **soft-apresentacao**.
- O card em formato **print de tweet**, com cabeçalho de perfil e avatar → **soft-tweet-card**.
- O **vídeo**, o reel, o corte e a legenda → **soft-editor-video** (reel curto de 7 segundos: **soft-reel-7seg**).
- Os **anúncios como sistema** (verba, campanha, métrica) → **soft-trafego-meta** (a arte volta pra Ação 1 daqui).

## Recursos da pasta

- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta, leia antes de começar.
- `references/processo-design.md` · `processo-banner.md` · `processo-slides.md`: o pipeline de cada superfície.
- `references/perguntas-design.md`: o formato exato das 3 perguntas de design.
- `references/identidade-visual-cliente.md`: como ler, aplicar e salvar a marca de cada cliente.
- `references/familia-editorial-preto.md` · `familia-clinico-branco.md` · `familia-manuscrito-cru.md`: cor, tipografia e layout por família.
- `references/escala-densidade.md` · `tipografia.md` · `tipografia-quebra-linhas.md`: escala de fonte, combinações tipográficas, quebra de linha e controle de órfã.
- `references/auditoria-pre-preview.md`: as perguntas detalhadas do gate visual, cada uma com exemplo de render que queimou.
- `references/layouts.md` · `layout-utilitario.md` · `layout-tweet-avatar.md` · `layout-diagrama-manuscrito.md` · `setinha-arraste.md` · `elementos-manuscritos.md` · `deteccao-automatica.md` · `carrossel-embalagens.md`: repertório de layouts e elementos.
- `scripts/build_carousel.py` (esqueleto de geração) · `scripts/export_pngs.py` (export por Playwright) · `scripts/craft.py` (gate de craft em código: anti-órfã e contraste) · `scripts/lint_copy.py` (anti-IA na copy-visual).
- `assets/template-base.html`: o template do render.
- `shared-references/`: operação-padrão, crivo, filtro anti-IA, filtro mobile-first.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **A régua aqui é de CONFERÊNCIA, e ela roda sobre o que foi RENDERIZADO.** O render entrega `conferencia/checagem-titulos.md` com a régua passada nas manchetes que aparecem nos PNG, uma por slide, porque o que foi renderizado é o que o público lê. Quando a copy vem pronta de outra skill, cada manchete sai com `passa` ou `alerta ao dono: <o quê>`, e o alerta não bloqueia o render: vai pro handoff, pra quem escreveu decidir. Cole `manchetes renderizadas: N · conferidas: N · com alerta: N`.
- **O render não reescreve a copy, nem para consertar o que a régua reprova.** Quando a manchete da fonte fere uma regra, o render sai com a manchete DA FONTE e a linha `alerta ao dono: <o quê> · sugestão: <literal>` na checagem. Cole `manchetes idênticas à fonte: N de N`; número menor obriga `alterada porque <motivo> · autorizado por <quem>` naquela manchete. **Texto de slide como string literal dentro do script gerador é proibido, e a proibição virou contagem:** o texto vem por leitura do arquivo-fonte, e a conferência é o comando `grep -c '<manchete>' <arquivo-fonte>` ao lado de cada manchete renderizada. **Grave o gerador na própria pasta de saída** e cole as duas saídas:

```
grep -c 'read_text\|open(.*\.md)' <gerador>     # maior que zero
grep -cE '"[A-Za-zÀ-ú ,.]{40,}"' <gerador>     # igual a zero
```

**Sem o gerador na pasta, a entrega reprova mesmo com as PNGs certas**, porque o render não se reproduz: o dono recebe imagens que ninguém consegue gerar de novo. Cole também o comando que reproduz o render inteiro, na forma `python3 <gerador> <arquivo-fonte> <pasta de saída>`, e ele tem que rodar da pasta sem editar nada. Decidir certo pelo caminho errado deixa a fonte e o PNG dizendo coisas diferentes, e é o PNG que vai ao público.
- **Marcador de pendência nunca vira tinta.** O `scripts/export_pngs.py` conta `[A CONFIRMAR`, `[DADO` e `[CONFIRMAR` no HTML de render e sai com exit 1 antes de exportar, e esse gate não aceita `--force`. Resolva o dado com o dono ou reescreva a frase sem ele. Cole a saída (`marcadores no html de render: 0`) na checagem.
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `shared-references/crivo/07-regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `shared-references/crivo/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**

## Passo 2 da checagem (fecho, roda por comando)

Depois de gravar todos os entregáveis, rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída. Ele exige o `conferencia/checagem-titulos.md` na pasta, confere o inventário (os 4 inteiros, o piso e o `inventário duplicado`), o universo dos títulos, o marcador acima de 6 palavras, o nome de conversa privada, a `saída do script reescrita` e o lint de todo `.md`, RELATO incluso. **`exit` diferente de 0 reprova a entrega inteira, antes da análise de conteúdo.**
