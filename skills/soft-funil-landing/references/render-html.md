# Render: a página pronta em HTML

Abre na Ação 7, depois que a copy está escrita no `.md`. Transforma a copy em `pagina.html` e `obrigado.html` a partir do template `assets/landing-base.html`: arquivo único, CSS embutido, sem dependência externa, feito primeiro pro celular, sem menu. Traz pra dentro desta skill o que a soft-designer ensina de página em HTML (identidade do dono, tipografia, contraste, quebra de linha, conferência de tela), pra a landing sair inteira daqui.

Nada é publicado. Hospedar, apontar domínio ou subir em ferramenta só com ordem nomeada do dono.

---

## 1. O que sai na pasta

| Arquivo | Quem lê | O que tem |
|---|---|---|
| `pagina.html` | o visitante | a página de inscrição ou de venda do ingresso |
| `obrigado.html` | quem se inscreveu | confirmação, data e hora, um próximo passo, compromisso, o que preparar |
| `pagina-<slug>.md` | o dono | a copy das duas páginas, bloco a bloco, com a linha do molde no topo |
| `_notas-operador.md` | o dono e o operador | o que conectar, perguntas sobre o que faltou, saída das conferências, fontes de cada número |

A página não carrega bastidor: nome de regra, de arquivo, de script, contagem, pergunta ao dono e instrução de publicação moram no `_notas-operador.md`.

---

## 2. Passo a passo

1. Copie `assets/landing-base.html` pra `pagina.html` e pra `obrigado.html`.
2. Em `pagina.html` apague do `INICIO PAGINA:obrigado` ao `FIM`; em `obrigado.html`, do `INICIO PAGINA:inscricao` ao `FIM` (o `<head>`, o CSS e o script ficam nas duas).
3. Apague os blocos (`<!-- BLOCO nome -->` até `<!-- /BLOCO nome -->`) que o molde não lista (`references/moldes-evento.md`). Fora do registro de evento, fique com hero, `cards`, `pra-voce`, `cta-final` e `barra-fixa` conforme a receita do tipo.
4. No longo pago, troque o id `inscricao-final` por `inscricao` (o `cartao-form` já saiu).
5. Troque cada `{{TOKEN}}` pela copy do `.md`, com Python (lendo o arquivo, trocando e gravando). Heredoc de shell corrompe `$`, crase e aspas.
6. Repita `<li>`, `<article class="card">`, `<details>` e `<option>` pelo número de itens da copy; apague os que sobram.
7. Preencha as variáveis de `:root` com a identidade (seção 3).
8. Rode a conferência (seção 7) e conserte até passar.

**Dado que falta.** No HTML não existe lacuna visível. A frase que depende do dado sai inteira; o dado vira pergunta no `_notas-operador.md`. Link que o dono ainda não deu fica só no atributo, marcado `#CONECTAR-...`, e o script do template segura o envio do formulário sem destino. `#CONECTAR-...` nunca aparece como texto: rodapé sem razão social sai.

**Token sem dado apaga o elemento.** Micro sob o botão, selo, formato, confirmação, rodapé e seletor são campos, não texto padrão. Sem linha do insumo, apague o elemento inteiro (o `<p>`, o `<li>`, o bloco) e ponha a pergunta no `_notas-operador.md`. "Sem custo", "dados protegidos", "pagamento protegido", "ao vivo" e "por e-mail" só com a palavra no insumo, dita do próprio evento (tabela em `moldes-evento.md`, seção 9). Sem sessões no insumo, o `seletor-horario` sai inteiro; opção "a confirmar" ou sem data reprova no script.

---

## 3. Identidade do dono (cor e fonte)

Procure nesta ordem e pare no primeiro que achar:
1. Seção `## Identidade Visual` no `soft-perfil.md` ou no brain do agente. Achou: aplica e não pergunta.
2. Referência visual que o dono anexou na conversa (print de post, página, manual). Tire fundo, destaque e estilo de fonte e declare em 1 linha no `_notas-operador.md`.
3. Nada: fica o padrão neutro do template (fundo claro, texto quase preto, um azul de destaque, fonte do sistema). Anote no `_notas-operador.md` que dá pra trocar em 2 minutos e quais variáveis mudam.

| Campo da identidade | Variável do template |
|---|---|
| Fundo | `--cor-fundo` (e `--cor-cartao` um tom acima ou abaixo) |
| Texto | `--cor-texto`, `--cor-suave` |
| Destaque (1 só) | `--cor-destaque`, `--cor-destaque-texto` (a cor do texto do botão) |
| Negativo (o X da lista "sem") | `--cor-negativo` |
| Fonte de título e peso | `--fonte-titulo`, `--peso-titulo` |
| Fonte de corpo | `--fonte-corpo` |
| Cantos | `--raio` (retos: 2px a 4px; arredondados: o da marca) |

**A identidade muda a tinta, nunca o piso.** Com qualquer cor:
- Contraste: corpo 4,5:1 contra o fundo; título grande e botão 3:1. Destaque claro em fundo claro (amarelo, verde-limão) vai pra borda e ícone, e o botão ganha um tom mais escuro da mesma cor.
- Um destaque só, em 5% a 15% da página (botão, check, borda do card). Duas cores de destaque dividem o olho entre dois caminhos.
- Fonte de marca do Google Fonts é a única dependência externa aceita: um `<link>` no `<head>` e a pilha de reserva do sistema depois do nome (`"Inter", system-ui, sans-serif`). No máximo 2 famílias e 3 pesos. Anote no `_notas-operador.md`.
- Sem cor neon, sem gradiente atrás de texto, sem foto atrás do hero.

---

## 4. Piso do celular (não mexa abaixo disto)

O template já vem nesses números; ao ajustar, confira contra `shared-references/filtro-mobile-first/checklist-final.md`.

- Corpo 18px, título principal 32px ou mais no celular, texto de apoio (micro, rodapé, legenda) 14px ou mais.
- Botão com 56px de altura, largura cheia no celular, texto de 2 a 5 palavras com verbo de posse.
- Margem lateral de 24px, espaço de 64px entre blocos, 1 coluna no celular, linha de até cerca de 65 caracteres no computador.
- Sem pop-up, sem menu, sem link de saída. A barra fixa do celular aponta pro mesmo lugar do botão e some quando o formulário aparece.
- Campo de formulário com 52px de altura, `type` certo (`email`, `tel`) pra abrir o teclado certo, `autocomplete` ligado.

---

## 5. Quebra de linha e imagem

**Última linha do título.** Leia a última linha do `h1` em 390px: se ficar com 1 palavra sozinha, ou 2 palavras curtas, ligue as duas últimas com `&nbsp;`. Vale pro `h1`, pros `h2` e pro texto do botão.

**Foto.** Só a foto do dono, com o caminho ou a URL que ele deu. Sem foto, o bloco de foto sai (nunca banco de imagem nem rosto gerado). Foto em `.webp` ou `.jpg` de até 200 KB, com `width` e `height` no `<img>` pra página não pular enquanto carrega. A da bio vai em preto e branco pelo CSS; a do hero, colorida.

**Vídeo.** O iframe do player do dono dentro da `div.video`; sem vídeo, o bloco sai.

---

## 6. Obrigado e agenda

O botão de agenda do template monta o evento sozinho: Google Agenda no Android e no computador, arquivo `.ics` no iPhone, com aviso 30 minutos antes. Preencha:
- `data-inicio`: data e hora em ISO com fuso (`2026-10-14T19:00:00-03:00`), do insumo. No perpétuo com seletor, deixe vazio: o script usa o horário escolhido (vem em `?sessao=` ou do próprio formulário, quando as duas páginas estão no mesmo domínio).
- `data-datas`: evento de mais de uma data (duas noites, três encontros) leva TODAS, em ISO separadas por vírgula, e o botão gera um `.ics` com um evento por data em qualquer aparelho. A agenda cobre todas as datas ou não é oferecida: agenda só da noite 1 num evento de duas noites reprova.
- `data-duracao-min`: duração do insumo; sem ela, a agenda marca 60 minutos e a página não fala em duração.
- `data-local`: o link de acesso, se o insumo tem; senão, vazio.

Sem data nem sessão, apague o botão e a micro dele (o script também esconde o botão que não achou data). A micro promete só o que o arquivo leva: sem link no insumo, nada de "o Zoom entra na sua agenda".

Grupo ou WhatsApp no lugar da agenda só com o link no insumo. Um botão só.

---

## 7. Conferência antes de entregar

1. **Fonte e estrutura, mecânica:** `python3 scripts/conferir_fontes.py --entrega <pasta de saída> --insumo <arquivos do dono>`. Lê o `.md` e os `.html` (só o texto visível). Reprova número sem fonte, termo de risco sem o mesmo termo no insumo (inclusive "ao vivo", "sem custo", "dados protegidos", "pagamento protegido", canal da confirmação), `{{` que sobrou, marcador visível, "a confirmar" ou `#CONECTAR` visível, seletor sem horário real, tag sem fechar, id repetido, âncora sem alvo, falta do viewport e mais de um destino de clique. A saída vai pro `_notas-operador.md`.
2. **Tela:** com Chromium ou Playwright no ambiente, tire a captura em 390x844 e em 1280x800 (`chromium --headless --screenshot=<saida>.png --window-size=390,844 file://<caminho>/pagina.html`) e olhe: no celular, hero e botão antes de rolar; no computador, o cartão do formulário ao lado do hero (longo grátis); nada vazando na lateral; a barra fixa não cobre o botão. Sem navegador, abra o arquivo e leia o HTML nos 3 pontos.
3. **Conexões:** liste no `_notas-operador.md`, seção `O que conectar`, cada `#CONECTAR-...` que ficou, o redirecionamento pro `obrigado.html` (com `?sessao=` no perpétuo), o pixel e onde hospedar. Uma linha por item, com o que o dono precisa colar.
