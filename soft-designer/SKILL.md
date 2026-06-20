---
name: soft-designer
description: A skill ÚNICA de design visual do método Soft. Produz banner, carrossel e slides de apresentação ponta a ponta, o VISUAL e a COPY-VISUAL juntos (a headline do banner, o texto de cada card, o texto de cada slide), passando essa copy pelo Crivo antes de renderizar. Recebe a tese ou briefing das skills de conteúdo (soft-conteudo), webinário (soft-webinario) e lançamento (soft-lancamento-pago), ou direto do usuário, e entrega o arquivo final (PNG 1080x1350 do carrossel, banner, deck de slides) que quebra padrão no feed. Engenharia visual própria, 3 famílias de estilo, tipografia editorial, render HTML/CSS, export PNG. Use SEMPRE que envolver banner, carrossel, slides, design, PNG, criativo visual, capa, "faz o carrossel", "cria o banner", "desenha os slides", "monta o visual", "exporta os slides", "transforma essa copy em carrossel". NÃO use pra escrever conteúdo de texto longo (caption, carta, roteiro), isso é das skills de conteúdo.
---

## 📦 O QUE ESTA SKILL PRODUZ

**Carrossel** (PNG 1080x1350 pronto pra postar ou impulsionar)
- Copy-visual de cada card (escrita aqui, pelo Crivo) + render nas 3 famílias visuais.
- Capa que para o scroll, embalagem A+B, setinha de arraste, slides finais com função.

**Banner / criativo** (estático, pra tráfego ou orgânico)
- Headline e copy-curta do banner (escrita aqui, pelo Crivo) + composição visual.

**Slides de apresentação** (deck 16:9, ex.: webinário, palco, aula)
- Copy-visual de cada slide (escrita aqui, pelo Crivo) + layout do deck pela espinha de tensão. O roteiro da fala e a oferta chegam prontos; o render de deck ainda é semi-manual (ver `references/processo-slides.md`).

**Serve o agente:** as skills de conteúdo, webinário e lançamento escrevem a TESE e passam pra cá; o usuário também aciona direto. O design não volta pra elas, sai pronto.

---

# Soft Designer, a única skill de visual

O design do método num lugar só. Antes, banner, carrossel e slide viviam espalhados em três skills; aqui viram uma capacidade só, que todas chamam. O valor próprio desta skill é a **engenharia visual** (as famílias de estilo, a tipografia, o render HTML/CSS para PNG) somada a um trabalho de copy: **ela escreve a copy que vai NO visual** (a headline, o texto do card, o título do slide), porque texto curto de peça visual é uma arte própria, e a passa pelo mesmo Crivo das outras skills antes de desenhar.

> **Passo 0, sempre: lê o perfil do usuário** (`shared-references/crivo/00-perfil-do-usuario.md`). Avatar, fonte de VoC, banco de provas, voz e nicho são DELE. Usuário sem perfil é roteado pro onboarding antes de produzir. O designer nunca assume os dados de outra pessoa, nem deixa o perfil-de-referência vazar pra peça (passada anti-vazamento do `03-gate-cub.md`).

## O que entra e o que sai

- **Entra:** a TESE ou briefing da peça (de `soft-conteudo`, `soft-webinario`, `soft-lancamento-pago`, ou do usuário direto). Pode vir só o tema, pode vir a copy longa de apoio. O que NÃO vem pronto é a copy-visual: isso é trabalho daqui.
- **Sai:** o arquivo final (PNG do carrossel, banner, deck), com a copy-visual já aprovada no Crivo e o visual renderizado.

## As 3 superfícies

- **Carrossel** (a frente mais madura) → `references/processo-design.md` (o pipeline: detecta a função de cada card, escolhe família + cor + tipografia, renderiza, audita, exporta) + `references/carrossel-embalagens.md` (capa A+B, embalagem) + `references/perguntas-design.md` (o briefing visual) + `references/auditoria-pre-preview.md` (o gate visual antes de exportar).
- **Banner / criativo** → `references/processo-banner.md` (a anatomia do banner: a headline que para, a composição, o CTA visual).
- **Slides de apresentação** → `references/processo-slides.md` (a espinha de tensão do deck, os 15 tipos de slide, a regra "1 ideia por slide / lido em 3s", o slide de oferta, a dimensão 16:9). O ROTEIRO da fala e a OFERTA chegam prontos da skill de funil/webinário ou do usuário; aqui é a engenharia visual + a copy-visual de cada slide. O render de deck ainda é semi-manual (os scripts estão cravados em 1080×1350; ver "Gaps de engenharia" no fim do processo).

## A lei: copy-visual passa pelo Crivo, render não muda palavra

O designer escreve a copy-visual, então ela obedece o Crivo como qualquer peça:

1. **Ancora e escreve** a copy-visual (headline, card, título de slide) puxando o verbatim e a tese do perfil do usuário (`shared-references/crivo/01-entrada-verbatim.md`), no ângulo de ponto cego, com mecanismo nomeado.
2. **Passa pelo gate** (`shared-references/crivo/03-gate-cub.md`): CUB, as 3 perguntas do Harry na headline e na capa, a passada de Consciência, prova no CTA, anti-vazamento. Copy-visual que não passa, reescreve antes de desenhar.
3. **Anti-IA + mobile-first** (`shared-references/filtro-anti-ia/`, `shared-references/filtro-mobile-first/`): sem travessão, sem frase de robô, e legível no celular (a peça vai ser vista em 6cm de tela).
4. **Renderiza** o visual em cima da copy aprovada.

**Regra de ouro do render (fecha um furo conhecido):** depois que a copy passou no gate, o desenho **não muda palavra**. Diagrama, quebra linha, escolhe accent, mas o texto é o que foi aprovado. Se o layout EXIGIR mexer numa palavra (cabe melhor, quebra feia), a copy mexida **re-passa a passada de ancoragem e a headline do gate** antes de exportar. Render que reescreve copy às escondidas é o erro que a auditoria já pegou.

## A engenharia visual (o valor que só vive aqui)

Carrossel bom não é bonito, é o que **quebra padrão** no feed (o oposto de gradiente, ícone colorido, template Canva, sans-serif centralizada). As 3 famílias, a tipografia, os layouts e o render moram nas references de design e nos `scripts/` (`build_carousel.py`, `export_pngs.py`, render HTML/CSS com as fontes em `assets/fonts/`, export PNG). O método da peça (Fórmula 7, função de cada card) vem do guia e da tese que chega; a engenharia de transformar isso em imagem é o que esta skill domina.

## O que ela NÃO faz

- Não escreve conteúdo de texto longo (caption, carta, roteiro, e-mail). Isso é das skills de conteúdo; aqui é só a copy que vai DENTRO do visual.
- Não inventa prova nem número. Sem banco de provas no perfil, a peça sai com o placeholder marcado, igual ao Crivo manda.
- Não decalca os exemplos das references (são de outro nicho de propósito). A peça nasce do perfil do usuário da vez.
