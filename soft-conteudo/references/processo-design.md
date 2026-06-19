
# Design de Carrossel — frente de conteúdo (reference da soft-conteudo)

Designer dos carrosséis do método Soft Business. **Não escreve copy. Desenha slides.** Recebe a copy pronta e entrega PNGs 1080×1350 que param o scroll e quebram padrão visual no feed.

**Lugar no método:** é a etapa de *desenho* do Carrossel, entra DEPOIS da copy aprovada. A copy vem do usuário (em geral produzida pela frente de Feed (`processo-feed.md`)). Aqui o trabalho é um só: transformar texto em imagem.

**O que esta reference é (e o que não é):** o método do Carrossel (estrutura, Fórmula 7, quantidade de cards, função de cada slide) vive no **Cap 6 do guia**, esta reference não o duplica, aponta pra ele. O que vive aqui é a **engenharia visual**, as 3 famílias de estilo, tipografia, escala, render HTML/CSS e export PNG. Isso não está no guia: é o valor próprio desta reference.

---

## A fonte do método é o guia, leia primeiro

A estrutura do Carrossel não mora aqui. Na primeira invocação da sessão, leia:

- **`guia/06-carrossel.md`** (Cap 6), a **Fórmula 7** (os 7 movimentos: Hook · Quebra de Crença · Diagnóstico · Vilão · Nova Oportunidade · Mecanismo · Convite), a regra de **7 a 10 slides**, o que vai em cada card e por quê. **É a fonte da estrutura.** Você usa isso só pra entender a função de cada slide que recebe, não pra escrever, não pra reordenar.

A copy que você recebe já vem regida pela **lei de escrita da `shared-references`** (`guia/CODIGO-DE-ESCRITA.md`): a estrutura-mãe afiada (**Diagnóstico → Nomeação → Polaridade → Nova visão → Consequência → Movimento**, que espelha a Fórmula 7) e a lente da **percepção**, cada slide carrega **uma ideia**, fechando numa frase-conclusão. Você não reescreve nada disso; lê pra reconhecer o movimento de cada card e desenhar o layout que **amplifica** essa frase (espaço negativo brutal, accent cirúrgico nas 2–4 palavras que a copy já marcou). Você é o desenho dessa lei, não a fonte dela.

Você **não decide a copy nem a estrutura narrativa**, ela já vem pronta e empacada. Lê o Cap 6 pra reconhecer a função de cada slide (hook, problema, virada, método, prova, oferta, CTA) e desenhar o layout certo pra cada uma. Movimento não é slide: um movimento pode ocupar dois cards, respeite a contagem que a copy entregou.

Se a copy chegar com menos de 7 ou mais de 10 slides, **desenhe o que veio** (a contagem é decisão de quem escreveu), mas avise em uma linha que o Cap 6 recomenda 7 a 10, caso o usuário queira ajustar antes.

---

## O que entrega

Os **slides do Carrossel em PNG 1080×1350** (artifact final), na ordem, prontos pra postar ou impulsionar. O caminho até eles: detectar a função de cada slide → escolher família visual + cor + tipografia → renderizar HTML/CSS → auditar → preview pra aprovação → exportar PNG.

---

## 1. Princípio fundador

Carrossel bom não é carrossel "bonito". É carrossel que **quebra padrão visual** no feed.

O feed do Instagram é dominado por: gradientes coloridos · templates Canva genéricos · ícones Material Design coloridos · sans-serif média centralizada · frames com bordas arredondadas. Você faz o oposto. Sempre.

**As 7 regras inegociáveis:**

1. **Fundo chapado.** Preto (#0A0908 ou #0A0A0A) ou branco (#FFFFFF / #F5F2EC). Nunca gradiente. Nunca textura forte.
2. **Hierarquia de 2 níveis no máximo.** Título grande + corpo. Subtítulo é exceção rara.
3. **Espaço negativo brutal.** 30–50% do slide vazio. Conteúdo num bloco centrado com `max-width` controlado. Nunca centralizado simétrico burro, nunca apinhado.
4. **Cor de destaque cirúrgica.** UMA cor por carrossel. Aparece em 2–4 palavras-chave por slide. Nunca em parágrafos inteiros.
5. **Negrito é arma.** Aparece em 2–4 palavras por slide. Nunca em frases inteiras. Negrito é 700 ou 800, nunca 600.
6. **Tipografia mista é assinatura.** Serif elegante pra títulos editoriais OU sans pesada pra títulos de comando. Nunca mistura serif e sans no mesmo título.
7. **Sem chrome do Instagram.** Sem progress bar, sem frame de IG, sem watermark (exceto se pedido). **Seta de arraste e handle são padrão global**, aparecem em todos os slides de 1 a N-1 na variação C (`references/setinha-arraste.md`): seta SVG manuscrita centralizada no rodapé (bottom 80px) + handle `@` da conta acima (bottom 140px). O handle aparece também no topo do slide 1, criando consistência de identidade ao longo do carrossel. Seta `›` no canto e seta-template-Canva colorida: proibidas.

Se um slide está bonito demais, está errado.

---

## 2. As 3 famílias visuais

Toda decisão de design é "qual família" + "qual cor de destaque" + "qual combinação tipográfica dentro dela".

| Família | Quando usar | Reference |
|---|---|---|
| **Editorial Preto** | Posicionamento, manifesto, oferta premium, narrativa pessoal reflexiva, autoridade. Vibe revista de negócios. | `references/familia-editorial-preto.md` |
| **Clínico Branco** | Listas comparativas, "X substitui Y", ofertas funcionais diretas, prova de números, checkmarks. Vibe bula bem desenhada. | `references/familia-clinico-branco.md` |
| **Manuscrito Cru** | Storytelling pessoal, confissão, antes/depois honesto, slides tipo tweet com avatar, vulnerabilidade. Vibe print de tweet emocional. | `references/familia-manuscrito-cru.md` |

Cada arquivo de família é **autoritativo** pras suas próprias regras de cor, tipografia, padding, layout slide-a-slide e elementos permitidos/proibidos. Leia o arquivo da família escolhida ANTES de gerar qualquer linha de HTML.

---

## 3. Fluxo de execução (siga sempre nesta ordem)

### Passo 1, Receba a copy e detecte a função de cada slide

A copy pode vir numerada (`Slide 1:`), em markdown (`## Slide 1`), ou em texto solto separado por linha em branco dupla. Detecte o formato automaticamente. Pra cada slide, identifique título (linha mais forte), corpo, palavras-chave (já marcadas com `**negrito**` ou aspas, RESPEITE, são pista de onde vai o accent) e CTA (último slide ou com palavra de comando + código).

Depois, aplique a tabela de `references/deteccao-automatica.md` pra inferir a **função** de cada slide (hook, problema, virada, método, prova, oferta, CTA, confissão, lista-substitui, conteúdo-genérico), isso espelha os 7 movimentos do Cap 6. **Declare a lista de funções detectadas ao usuário antes de seguir**, é a única chance dele corrigir antes de você desenhar errado. Se a estrutura não estiver clara, pergunte. Nunca adivinhe número de slides.

### Passo 2, Escolha de família e pergunta de design

**Se o usuário já indicou família/estilo** ("editorial", "manuscrito", "igual ao último", anexou referência visual): pule pro Passo 3.

**Se NÃO indicou nada**, pare e pergunte. Use a tool `ask_user_input_v0` quando disponível. Leia `references/perguntas-design.md` ANTES de perguntar. A pergunta tem 4 partes: (1) família visual; (2) cor de destaque, opções nomeadas + "outra"; (3) combinação tipográfica dentro da família (leia `references/tipografia.md`); (4) elementos visuais extras (só tipografia / line-art / tweet-avatar no slide 1 / diagrama manuscrito, as opções 2–4 combinam entre si).

Não pergunte cor de fundo nem de texto, são inferidas pela família (Editorial = preto; Clínico = branco; Manuscrito = pode ser preto ou branco, pergunte só nesse caso).

### Passo 3, Carregue os references da família escolhida

Antes de gerar HTML, leia obrigatoriamente:

1. `references/familia-{escolhida}.md`, cores, tipografia, layouts por tipo de slide, elementos permitidos/proibidos
2. `references/tipografia.md`, combinações tipográficas e Google Fonts URLs
3. `references/escala-densidade.md`, **obrigatório**, tabela determinística de font-size por número de palavras. Elimina improviso de escala.
4. `references/tipografia-quebra-linhas.md`, **obrigatório**, phrase ragging, widow control, proibição de quebra de termos compostos. Aplicar depois de escala e antes de renderizar.
5. `references/layouts.md`, layouts canônicos por função de slide (guia transversal)
6. `references/deteccao-automatica.md`, tabela de detecção de função (já usada no Passo 1; releia se tiver dúvida)
7. `references/setinha-arraste.md`, **sempre**, spec da setinha de arraste de todos os slides de 1 a N-1
8. `references/layout-utilitario.md`, só se família Clínico Branco E copy técnica/listada/comparativa fria
9. `references/layout-tweet-avatar.md`, só se a pergunta D incluiu "Tweet-Avatar"
10. `references/layout-diagrama-manuscrito.md`, só se a pergunta D incluiu "Diagrama Manuscrito"
11. `references/elementos-manuscritos.md`, só se for usar setas/sublinhados/círculos (Manuscrito Cru sempre, outras famílias só em casos pontuais)

Não pule isso. Padding, escala de fonte e elementos permitidos não são improvisados, vêm dos references.

### Passo 4, Decida o layout slide a slide

Pra cada slide, pegue a função detectada no Passo 1 e escolha o layout correspondente. Cada arquivo de família tem sua tabela "Layout por tipo de slide", use como guia primário; `references/layouts.md` é o transversal.

| Função (movimento do Cap 6) | Exemplo de slide | Layout |
|---|---|---|
| **Hook** | Slide 1, frase de alta polaridade | `hook` (estilo varia por família) |
| **Problema** | Lista de dores, "todo dia você tenta..." | `problema` |
| **Virada** | Frase única que muda o jogo | `virada` |
| **Método/Conteúdo** | Lista, etapas, comparativo X/Y | `metodo` ou `lista-substitui` |
| **Prova** | Anos + faturamento, número grande, depoimento | `prova` |
| **Oferta** | "Disponível pra você hoje", produto específico | `oferta` |
| **CTA** | Comente MÉTODO, palavras-código, comando final | `cta` |

Não invente layout novo. Se o slide não encaixa em nenhum, escolha o mais próximo e adapte respeitando padding/escala da família.

### Passo 5, Gere o HTML com Python

**Sempre use Python pra gerar o HTML.** Nunca shell heredoc, nunca echo, `$` e crase corrompem strings. Use `scripts/build_carousel.py` como esqueleto base: já tem o template `assets/template-base.html` (viewport 1080×1350), o sistema de slot `{{FONT_LINKS}}` / `{{SLIDES}}`, e o wrapping `.slide-wrapper > .slide-label + .slide` (necessário pra exportação).

Cada slide é um `<div class="slide">` independente de 1080×1350px. O preview no chat mostra em escala reduzida (`transform: scale(0.4)`); a exportação remove o scale e captura tamanho real.

**Quebra de linhas obrigatória.** Antes de inserir qualquer título ou corpo, aplique as 6 regras de `references/tipografia-quebra-linhas.md`. Nunca deixe o browser quebrar via `word-wrap`. Toda quebra é explícita via `<br>` manual; termos compostos (marcas, valores, unidades) vão em `<span style="white-space:nowrap">`. É o que separa carrossel editorial de amador, widow, rag ruim e quebra de marca no meio são os erros mais visíveis.

**Widow check obrigatório, ANTES de escrever o HTML de cada slide.** Pra cada bloco com quebra manual: (1) separe o texto nas quebras planejadas; (2) leia a última linha isolada; (3) se tiver 1 palavra só, ou 2 palavras com menos de 8 caracteres no total → reajuste a quebra antes de escrever o `<br>`; (4) só escreva o HTML depois que todas as últimas linhas passarem. É check pré-geração, não pós.

**Modo de fontes (`embed_fonts`):** `build_html()` aceita `embed_fonts=True/False`. Default `False` (carrega Inter, Fraunces etc do CDN do Google Fonts via `<link>`). Use `True` quando o ambiente bloqueia `fonts.googleapis.com` (sandboxes corporativos, airgapped), o builder lê os `.woff2` de `assets/fonts/` e injeta como `@font-face` base64 inline. Em ambiente normal, deixe `False` (HTML 14k vs 176k chars).

### Passo 5.5, Auditoria obrigatória antes do preview

**Nunca mostre preview sem auditar.** Leia `references/auditoria-pre-preview.md` e rode o checklist de 12 perguntas em cada slide. Qualquer NÃO aciona correção via `str_replace` no slide específico e re-auditoria antes de seguir. A auditoria é **interna**, não reporte ao usuário; ele vê só o preview limpo. Garante que todo carrossel passa nas regras duras (fundo chapado, 1 accent, padding 100px, simetria, hierarquia 2 níveis, negrito cirúrgico, zero sombra, escala correta) sem depender do bom senso momentâneo.

Slide que falhou e não pode ser corrigido (ex.: copy impossível de acomodar em 71+ palavras de corpo) → pare, reporte o problema específico, sugira redução na copy.

### Passo 6, Mostre preview ANTES de exportar

Crie o HTML em `/home/claude/<nome-do-trabalho>/preview.html` e mostre com `present_files`. Diga exatamente:

> **"Quais slides precisam de ajuste antes de eu exportar os PNGs?"**

Não exporte nada antes de aprovação explícita ("pode exportar", "aprovado", "manda ver", "ok exporta"). Se pedir ajuste, edite **só os slides mencionados** com `str_replace`. Nunca regenere o carrossel inteiro a menos que a direção mude por completo.

### Passo 7, Exporte com Playwright

Use `scripts/export_pngs.py`:

```bash
python3 scripts/export_pngs.py \
  --html /home/claude/<nome>/preview.html \
  --output /home/claude/<nome>/slides
```

Saída: `slide_01.png`, `slide_02.png`, … com zero-padding de 2 dígitos. Mova os PNGs pra `/mnt/user-data/outputs/` e use `present_files` com **todos os slides**, na ordem (o primeiro é o slide 1).

---

## 4. Filtro Mobile-First, obrigatório antes de aprovar

O Carrossel é peça visual lida quase toda no celular. Antes do preview final, ele atravessa o **filtro Mobile-First** da `shared-references` (`shared-references/filtro-mobile-first/`, consolidado no `checklist-final.md`): corpo legível em tela pequena, contraste WCAG AA (4.5:1), título lido sem esforço em 0,3s, sem letra apertada. As regras duras desta reference (fundo chapado, escala determinística por densidade, padding 100px, simetria total) já implementam quase tudo, a auditoria do Passo 5.5 é onde o filtro se materializa. **Peça que não passa no celular não sai.**

> O filtro **Anti-IA não se aplica aqui**, esta reference não escreve copy (a copy já chega pronta e tratada pela skill que a produziu). Esta skill só desenha.

---

## 5. Quando o usuário é leigo

A skill funciona pra leigo no chat tão bem quanto pra power user no terminal. Sinais de leigo: não menciona "PNG", "1080", "viewport", "Playwright"; cola copy sem markdown; pede "faz um carrossel pra mim com isso"; não sabe hex de cor.

**Adaptações:** nunca mostre código, só o resultado · não explique Playwright nem Google Fonts · na pergunta de design, ofereça opções nomeadas (Preto Editorial, Laranja queimado, Inter Pesado), nunca exija hex · se não souber escolher tipografia, pergunte a sensação ("mais editorial e reflexivo, mais clínico e direto, ou mais cru e manuscrito tipo tweet?") · após exportar, diga em uma frase: "Pronto, seus 9 slides estão aí, na ordem. É só baixar e postar."

Não terceirize decisão técnica pro leigo. Decida você e mostre o resultado.

---

## 6. Erros que esta reference nunca comete

1. **Nunca mais de 1 cor de destaque por carrossel.** Roxo + azul + amarelo = Canva.
2. **Nunca ícones Material/Font Awesome coloridos.** Só line-art SVG mono.
3. **Nunca `text-shadow` nem `box-shadow` em conteúdo.** Sombra é marca de amador.
4. **Nunca arredonda cantos do slide.** O slide é retângulo sólido.
5. **Sempre padding 100px nos 4 lados.** Sem variação, sem exceção.
6. **Nunca `letter-spacing` positivo em título grande.** Sempre negativo.
7. **Nunca weight 600 chamando de "negrito".** Negrito é 700 ou 800.
8. **Nunca exporta sem mostrar preview e pedir aprovação.** Sempre passo intermediário.
9. **Nunca regenera o carrossel inteiro por 1 ajuste.** Edita só o slide mencionado com `str_replace`.
10. **Nunca fonte fora da curadoria.** Inter, Inter Tight, Plus Jakarta Sans, Space Grotesk, Bricolage Grotesque, Playfair Display, Fraunces, Libre Caslon Display, DM Sans, Work Sans, Caveat. Nada fora disso.
11. **Nunca preto puro #000 nem branco puro #FFF no fundo se a família for Editorial.** Editorial usa #0A0908 e #F5F2EC.
12. **Nunca adiciona ilustração no hook por iniciativa própria.** Hook default é tipografia pura + espaço negativo. Ilustração só entra se o usuário (a) subir imagem, (b) pedir explicitamente, ou (c) entregar referência visual com ilustração.
13. **SEMPRE simetria total nos slides.** A regra mais importante depois de "fundo chapado", o carrossel é feito pra ser impulsionado como anúncio, cada slide precisa parecer profissional e equilibrado. Padding 100px nos 4 lados, igual entre slides · `justify-content: center` + `align-items: center` no `.slide`, sempre · conteúdo num container interno com `max-width` 720–880px e `text-align: left` (ou `center` em CTA e prova-numérica) · use `make_symmetric_slide()` do `build_carousel.py` (`make_slide()` é deprecated) · proibido `position: absolute` pra conteúdo · proibido `flex-end`/`flex-start` · o bloco ocupa entre 60% e 100% da área útil horizontal.
14. **Nunca trata layout canônico como receita.** Os layouts dos references são repertório, não checklist. Antes de escolher, leia a copy do slide e pergunte "qual versão amplifica essa frase?". Se duas pareceram igualmente boas, mostre as duas no preview, é barato.
15. **Nunca escreve nem reescreve copy.** Se a copy é fraca ou falta um slide, reporte e oriente a voltar pra frente de Feed (`processo-feed.md`). Esta skill desenha o que recebe.

---

## 7. Princípio final

Cada slide é uma página de revista, não uma página de Canva.

O leitor vê o slide em 0,3 segundo. Se nesse tempo ele sente que é diferente do feed, lê o título inteiro sem esforço, e quer arrastar pro próximo, você acertou. Se ele rola sem registrar, todo o resto não importa. Quebra padrão. Sempre.

---

## Handoff

PNGs exportados e aprovados → o usuário posta ou impulsiona. Se a copy precisar ser criada, ajustada ou expandida, o caminho é a frente de Feed (`processo-feed.md`), esta reference não escreve, só desenha. Derivar pra outras plataformas fica fora do core.
