# Padrão visual e engenharia estrutural

O que faz uma tela parecer construída por alguém que se importa, não cuspida por IA barata. Duas camadas: a **estética** (paleta, tipo, forma: a do cliente por cima, o padrão visual da skill como default) e a **engenharia estrutural** (componentes ricos, tokens, temas, login, nav, i18n, **universal**, vale pra qualquer marca). O dono vai apresentar isso na frente do cliente dele: a tela é parte da venda.

## Índice
- [Regra-mãe: marca do cliente por cima, o padrão visual por baixo](#regra-mae)
- [A estética default](#estetica-default)
- [Tokens de cor e os 2 temas (sem flash)](#tokens-temas)
- [Os 3 inegociáveis (com grep de prova)](#inegociaveis)
- [Componentes ricos (o catálogo)](#componentes-ricos)
- [Login split de 2 colunas](#login-split)
- [Nav numerada e menus de dados](#nav-numerada)
- [i18n motor próprio](#i18n)
- [As 14 regras novas (catalogos abertos, agosto/2026)](#regras-catalogo)
- [Onde o catalogo discorda da casa (e quem ganha)](#conflitos-catalogo)
- [Checklist visual antes de liberar](#checklist)

<a id="regra-mae"></a>
## Regra-mãe: marca do cliente por cima, o padrão visual por baixo

Esta skill é **marca-neutra**. A ESTRUTURA (componentes ricos, tema duplo, login split, nav numerada, tokens, zero gradiente/emoji/travessão) é **universal**, vale pra toda tela, toda marca. A **paleta e o tipo** vêm da marca do CLIENTE: leia a identidade dele (site, material, o que o dono passar) e aplique nos tokens. Na ausência de marca definida, o **default é o padrão visual da skill** abaixo. Nunca decida a paleta sozinho quando o cliente tem uma; nunca deixe sem paleta quando ele não tem (cai no default).

<a id="estetica-default"></a>
## A estética default

Editorial brutalista-técnico. Sofisticação pela subtração. O contraste vem de branco-sobre-preto e hairlines de 1px, **não** de blocos de cor.

**Paleta (dark):** fundo `#000`; superfícies `#0a0a0a` / `#101010` / `#0d0d0d` (nunca clareia pro branco). Texto `#fff` (primário), `#b8b8b8` (corpo dim), `#6a6a6a` (faint). Hairlines `#1e1e1e` (padrão) / `#2f2f2f` (realce). Acento ÚNICO verde-neon `[COR-DE-ACAO do dono via config]` (CTA, ✓, índices, kicker, números, links); hover `#3ec96f`. Vermelho-negativo `#c0392b` (× / atenção). Verde-WhatsApp `#25D366` SÓ no botão literal de WhatsApp.

**Fontes (3 papéis fixos):** **Bebas Neue** = todos os títulos h1 a h4 + números de seção, sempre CAIXA ALTA, line-height apertado. **Inter** (400/500/600/700) = corpo. **JetBrains Mono** = kickers, labels, badges, números, header de tabela, footer, uppercase, tracking alto (.14–.26em). Nunca Bebas em parágrafo nem Inter em título grande.

**Forma:** radius quase reto (2–4px); pílula 999px só em nav-cta. Sem sombra estrutural, **sem gradiente**, sem glow (exceção: backdrop-blur da nav e o glow do CTA). CTA = fundo do acento, texto preto, Bebas uppercase, radius 2–4px. Callout = border-left 3px, fundo `#0a0a0a`, radius 0. Kicker = mono com tracinho antes.

```css
/* Google Fonts (única exceção de rede externa que o padrão usa) */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
```

<a id="tokens-temas"></a>
## Tokens de cor e os 2 temas (sem flash)

**Toda** cor é `var(--token)`. Nada de hex solto no meio do CSS de componente, e assim a marca do cliente entra num lugar só e os 2 temas funcionam.

```css
:root, [data-theme="dark"] {
  --bg: #000; --surface: #0a0a0a; --surface-2: #101010;
  --text: #fff; --text-dim: #b8b8b8; --text-faint: #6a6a6a;
  --line: #1e1e1e; --line-strong: #2f2f2f;
  --accent: [COR-DE-ACAO do dono via config]; --accent-hover: #3ec96f; --neg: #c0392b;
  --font-display: 'Bebas Neue', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
[data-theme="light"] {
  --bg: #fff; --surface: #f6f6f6; --surface-2: #efefef;
  --text: #0a0a0a; --text-dim: #444; --text-faint: #888;
  --line: #e2e2e2; --line-strong: #cfcfcf;
  /* --accent permanece o da marca; contraste re-checado no claro */
}
```

**Sem flash de tema (FOUC):** o tema é setado **antes do paint**, no `<head>`, síncrono, não depois de renderizar (senão pisca branco→preto e o dono percebe na apresentação).

```html
<!-- primeiro script do <head>, antes de qualquer CSS de conteúdo -->
<script>
  (function () {
    var t = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', t);
  })();
</script>
```

<a id="inegociaveis"></a>
## Os 3 inegociáveis (com grep de prova)

Provados por grep no gate visual do SKILL.md. Aqui está o porquê e o certo-em-vez-de.

1. **Zero gradiente decorativo.** A riqueza vem de **2 tons sólidos em blocos** (um bloco `--bg`, o vizinho `--surface`), não de degradê. Gradiente decorativo é a assinatura nº 1 de template de IA. `grep -rniE "linear-gradient|radial-gradient|conic-gradient"` = 0.
2. **Zero emoji na UI.** Todo ícone é **SVG de linha** (stroke, `currentColor`, 1.5px). Emoji na interface grita "protótipo". Ex.: em vez de ✅ num card, um `<svg>` de check de linha herdando `--accent`.
3. **Zero travessão** (`—`) em UI **e** em docs novos. Usa vírgula, parênteses ou `·` (middot). Vale também pro texto que a skill escreve.

<a id="componentes-ricos"></a>
## Componentes ricos (o catálogo)

O anti-padrão que o gate mata é a **"caixinha título + descrição"**: um retângulo com um `<h3>` e um `<p>` cinza embaixo, repetido em grid. É o visual de "gerei rápido". Em vez dela, use um destes, escolhido pela função do conteúdo:

- **Hero de 2 colunas**: narrativa/kicker/título à esquerda, prova (device, número, imagem) à direita. Abre war room e landing do produto.
- **KPI número-gigante**: o número em Bebas grande (3–5rem), o label em mono uppercase pequeno embaixo. Para métrica única que precisa impactar (faturamento, nº de unidades, % de gargalo).
- **Escada de valor**: 3 níveis lado a lado (ex.: 3 faixas da proposta), o do meio destacado com border no acento. Nunca 3 caixinhas iguais.
- **Acordeão numerado**: plano de ação/FAQ; cada item com índice mono (`01`, `02`) e corpo que expande. Persiste qual está aberto.
- **Vídeo com capítulos**: player + lista de capítulos clicáveis à direita que dão seek (ver `frente-war-room.md`).
- **Mockup device**: a tela do produto dentro de um frame de notebook/celular, pra apresentar sem sair da tela.
- **Vitrine / grid de cards ricos**: card = kicker (mono) + título (Bebas) + corpo curto + chips (tags mono). Nunca só título+descrição.
- **Timeline**: fases/etapas com linha vertical e marcos; para roadmap ou histórico.
- **Modal**: conteúdo longo (um protocolo inteiro, um contrato) abre em modal, não estoura o card.
- **Lightbox**: imagem/infográfico amplia ao clicar.

Regra de decisão rápida: **um número que impacta → KPI gigante; três opções → escada de valor; uma sequência → acordeão numerado ou timeline; conteúdo longo → modal.** Se você se pegou fazendo grid de retângulos iguais com h3+p, parou no anti-padrão.

Exemplo de card rico (não-caixinha):

```html
<article class="card">
  <span class="kicker">Gargalo 02</span>
  <h3 class="card-title">Retorno de vacina não agendado</h3>
  <p class="card-body">38% dos tutores não remarcam o reforço. Perda estimada de 6 consultas/semana por unidade.</p>
  <div class="chips"><span class="chip">Retenção</span><span class="chip">3 unidades</span></div>
</article>
```
```css
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 3px; padding: 24px; }
.kicker { font-family: var(--font-mono); text-transform: uppercase; letter-spacing: .18em;
          font-size: 11px; color: var(--accent); }
.card-title { font-family: var(--font-display); font-size: 1.6rem; letter-spacing: .02em; margin: 10px 0 8px; }
.card-body { font-family: var(--font-body); color: var(--text-dim); line-height: 1.5; }
.chips { display: flex; gap: 8px; margin-top: 14px; }
.chip { font-family: var(--font-mono); font-size: 10px; text-transform: uppercase; letter-spacing: .12em;
        border: 1px solid var(--line-strong); border-radius: 2px; padding: 4px 8px; color: var(--text-faint); }
```

<a id="login-split"></a>
## Login split de 2 colunas

A entrada é sempre um **login split**: coluna esquerda = narrativa da marca (nome, uma frase de posicionamento, fundo `--surface`); coluna direita = card do form (~392px de largura), fundo `--bg`. Tudo além do login fica **atrás do gate**. Motivo: a primeira tela já vende, e um form solto no meio da página parece inacabado.

```css
.login { display: grid; grid-template-columns: 1fr minmax(360px, 480px); min-height: 100vh; }
.login__brand { background: var(--surface); padding: 64px; display: flex; flex-direction: column; justify-content: center; }
.login__form { display: flex; align-items: center; justify-content: center; }
.login__card { width: 392px; max-width: 100%; padding: 40px; border: 1px solid var(--line); border-radius: 4px; }
@media (max-width: 720px) { .login { grid-template-columns: 1fr; } .login__brand { display: none; } }
```

<a id="nav-numerada"></a>
## Nav numerada e menus de dados

- **Nav numerada**: cada item com índice mono (`01 Visão geral`, `02 Diagnóstico`), na ordem da apresentação/uso.
- **Grupos colapsáveis persistidos**: seções que agrupam itens colapsam, e o estado (aberto/fechado) persiste em `localStorage` por grupo, e o dono não reabre tudo a cada visita.
- **Menus de array de dados**: a nav e os menus são renderizados de um **array** (`const nav = [{ id, label, icon, children }]`), nunca item a item no HTML. Assim adicionar seção é adicionar um objeto, e a numeração é automática.

```js
const nav = [
  { id: 'overview',  label: 'Visão geral',  icon: iconGrid },
  { id: 'diagnosis', label: 'Diagnóstico',  icon: iconPulse },
  { id: 'plan',      label: 'Plano de ação', icon: iconList, children: [/* ... */] },
];
// render: nav.map((item, i) => `<a>${String(i+1).padStart(2,'0')} ${item.label}</a>`)
```

<a id="i18n"></a>
## i18n motor próprio

pt/en/es com **motor próprio** e chaves **namespaced** (`warroom.overview.title`, `product.lms.startModule`). Nenhuma string de UI solta no meio do JSX/HTML: toda string passa por `t('chave')`. Motivo: o cliente pode operar em mais de um idioma, e string hard-coded impede tradução e vira dívida. Um objeto de dicionário por idioma, um `t()` que resolve a chave e cai no pt se faltar.

```js
const dict = {
  pt: { 'warroom.overview.title': 'Visão geral da rede' },
  en: { 'warroom.overview.title': 'Network overview' },
  es: { 'warroom.overview.title': 'Visión general de la red' },
};
const lang = localStorage.getItem('lang') || 'pt';
const t = (k) => (dict[lang] && dict[lang][k]) || dict.pt[k] || k;
```

<a id="regras-catalogo"></a>
## As 14 regras novas (catálogos abertos, agosto/2026)

Vieram de dois registros públicos de antipadrão lidos direto do código-fonte: `github.com/pbakaus/impeccable` (59 regras, `scripts/detector/registry/antipatterns.mjs`) e `github.com/Leonxlnx/taste-skill` (SKILL.md, seções 4.7, 4.8, 6 e 9). Entrou **só o que não estava escrito acima**. Cada uma diz o defeito, por que ele custa dinheiro e como se prova.

**1. Caixa dentro de caixa é proibida.** Card aninhado dentro de outro card empilha borda sobre borda e vira ruído. Separe por espaço, tipo e hairline, nunca por mais um retângulo. Prova: nenhum bloco com `border`/`background` de superfície dentro de outro que já tem os dois.

**2. Barra colorida grossa na lateral do card é o tell nº 1 de tela feita por IA.** O callout com `border-left: 3px` continua permitido **só** com radius 0 e uma única vez por seção. Proibido em elemento arredondado (a borda briga com o canto) e proibido repetido num grid de cards. Prova: `grep -c "border-left: *[3-9]px"` menor que 2 por seção, e nenhum deles num elemento com `border-radius` acima de 4px.

**3. Texto funcional nunca desce de 11px.** Link, botão, item de nav, label, célula de tabela, chip e rodapé abaixo de 11px falham em tela de alta densidade e no celular. Vale mesmo se o valor estiver na escala de tamanhos: pôr 10px na escala legaliza o token, não a leitura. Exceção só pra letra miúda legal não clicável (piso 10px). Prova: nenhum `font-size` abaixo de 11px fora de `sup`, `sub` e texto de leitor de tela.

**4. Linha de texto entre 65 e 75 caracteres.** Passando de ~80 o olho perde o ponto de retorno e a pessoa para de ler. Todo container de corpo leva `max-width: 65ch` a `75ch`. Prova: medir a largura da coluna de texto na tela real, não no CSS.

**5. Entrelinha do corpo entre 1.5 e 1.7.** Abaixo de 1.3 o parágrafo empasta. Título pode ser apertado, corpo não. Prova: `line-height` declarado em todo seletor de corpo.

**6. Contraste WCAG AA obrigatório: 4.5:1 no corpo, 3:1 no texto grande.** Cinza sobre cor é o caso que mais escapa. `#6a6a6a` sobre `#000` dá cerca de 4.0:1 e **reprova** pra corpo: esse tom só serve pra rótulo grande ou texto decorativo. Prova: medidor de contraste em cada par texto/fundo, com o número anotado.

**7. Espaço acima do título tem que ser maior que o espaço abaixo dele.** O título pertence ao que vem depois. Quando o espaço é igual dos dois lados, cada seção parece legenda da anterior. E espaçamento não pode ser o mesmo valor em toda a página: junto o que é do mesmo assunto, afasta o que muda de assunto. Prova: comparar a margem de cima e a de baixo dos títulos.

**8. A primeira tela cabe na primeira tela.** Título com no máximo 2 linhas, linha de apoio com no máximo 20 palavras e 4 linhas, botão visível sem rolar. Teto de **4 elementos de texto** na abertura: rótulo (zero ou um), título, apoio, botões. Proibido na abertura: tarja de confiança, prévia de preço, lista de itens, fileira de rostos. Tudo isso desce pra seção própria. Se a promessa não cabe em 20 palavras, o problema é a promessa. Prova: screenshot da primeira tela no celular e no computador com o botão dentro do quadro.

**9. Rótulo minúsculo em caixa alta acima de título é racionado: no máximo 1 a cada 3 seções.** É o item mais violado em teste de produção. Página com 9 seções aceita 3 no total, e a abertura já conta como um. Se a seção A tem, as duas seguintes não têm. E ele nunca enumera capítulo (`01 / ÍNDICE`, `002 · Recursos`): a posição na página já ordena. Prova: contar os rótulos e dividir pelo número de seções.

**10. Nenhuma família de layout se repete.** Usou grid de 3 colunas iguais numa seção, não usa de novo. Teto de 2 seções seguidas no padrão imagem-de-um-lado-texto-do-outro; a terceira seguida reprova. Página de 8 seções usa pelo menos 4 arranjos diferentes. Grid de 3 cards idênticos lado a lado é proibido como padrão. Prova: listar o arranjo de cada seção e conferir que nenhum aparece duas vezes.

**11. Conteúdo tem que estar visível parado.** Bloco que nasce com `opacity: 0` esperando o script revelar some inteiro se o script falhar, e a página vai ao ar em branco pra quem entrou. O conteúdo nasce visível; a animação só melhora a entrada, nunca decide a existência. Junto: nenhum erro de script na carga, nenhuma imagem com `src` vazio ou de exemplo. Prova: abrir a página com o script desligado e ver o texto, mais o console limpo.

**12. Nada de tela falsa montada com retângulos.** Painel, lista de tarefas, terminal ou celular desenhados com `div` pra simular o produto é o tell mais reconhecível de todos. Use captura real, imagem gerada, o componente de verdade, ou nenhuma prévia. Vale igual pra ilustração grande feita de formas soltas.

**13. Nada colado na borda no celular, e nada estourando pro lado.** Parágrafo precisa de pelo menos 16px (ideal 24 a 32px) de folga lateral, e caixa com borda ou fundo precisa de pelo menos 12px por dentro. Barra de rolagem horizontal na página inteira é defeito, nunca escolha. Prova: largura do documento igual à largura da janela no celular, e folga medida na tela.

**14. Movimento é opcional pra quem pediu menos movimento.** Todo bloco animado respeita `prefers-reduced-motion`. Proibido por padrão: rolagem automática infinita, mola no easing (`bounce`, `elastic`), cursor piscando decorativo, ponto colorido pulsando antes de item de lista ou de nav, imagem que cresce ou gira ao passar o mouse. Ponto de estado só vale quando carrega estado de verdade. Prova: bloco `@media (prefers-reduced-motion: reduce)` presente e nenhum dos padrões acima no CSS.

**Bônus de conteúdo, não de forma:** nome genérico (`João da Silva`), número redondo demais (`99,99%`, `50%`), avatar de ovo e verbo de folheto (`impulsionar`, `potencializar`, `revolucionar`) denunciam dado inventado. Número quebrado e nome plausível são mais críveis que número redondo.

<a id="conflitos-catalogo"></a>
## Onde o catálogo discorda da casa (e quem ganha)

Os catálogos são régua genérica contra tela sem dono. A casa **tem** sistema declarado, e o próprio registro do `impeccable` trata como defeito o desvio do sistema declarado, não o sistema em si. Quatro pontos ficam decididos aqui pra ninguém "consertar" o que é escolha:

- **Inter é chamada de fonte batida.** Fica. É o corpo do sistema há meses, a personalidade da casa vem do par Bebas + JetBrains Mono, e trocar a fonte de corpo mexeria em toda peça aprovada. Decisão: mantida, e é a única concessão de fonte.
- **Preto puro `#000` é desaconselhado.** Fica. A estética é contraste branco-sobre-preto com hairline de 1px, e clarear o fundo mata o efeito. Decisão: mantido como fundo, com a ressalva da regra 6 sobre contraste do texto cinza.
- **Nav numerada é apontada como enumeração desnecessária.** Fica **só na navegação**, onde o número é endereço e ajuda a apresentar na ordem. Morre no corpo da página: nenhuma seção enumera o próprio capítulo (regra 9).
- **Kicker mono em todo card** vira excesso pela regra 9. Decisão: o kicker do card rico deixa de ser obrigatório e passa a ser exceção, dentro do teto de 1 a cada 3 seções. O exemplo de card acima continua válido como forma, não como obrigação de todo card ter kicker.


<a id="checklist"></a>
## Checklist visual antes de liberar

Espelha o GATE VISUAL do SKILL.md. Antes de dar uma tela por pronta:
- grep de gradiente / emoji / travessão = **0** (colar os números).
- nenhuma caixinha título+descrição; cada bloco é um componente rico do catálogo.
- toda cor é `var(--token)`; 2 temas; tema setado no `<head>` sem flash.
- entrada por login split; resto atrás do gate.
- nav numerada, grupos persistidos, menus de array.
- i18n com chaves namespaced; nenhuma string solta.
- paleta = a do cliente (ou o default da skill, se ele não tem marca).
- as 14 regras novas: caixa dentro de caixa = 0; barra lateral grossa so em callout de canto reto; nenhum texto funcional abaixo de 11px; coluna de corpo entre 65ch e 75ch; entrelinha de corpo 1.5 a 1.7; contraste medido em 4.5:1 no corpo; espaco acima do titulo maior que abaixo; primeira tela com botao dentro do quadro e no maximo 4 elementos de texto; rotulo em caixa alta no teto de 1 a cada 3 secoes; nenhuma familia de layout repetida; conteudo visivel com o script desligado; zero tela falsa feita de div; folga lateral de 16px no celular e zero rolagem horizontal; bloco de movimento reduzido presente.
