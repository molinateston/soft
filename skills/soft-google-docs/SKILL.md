---
name: soft-google-docs
description: Gerar ou atualizar um Google Doc NATIVO e bem formatado a partir de conteudo em Markdown, na conta Google do dono, via gog. Use SEMPRE que a tarefa for entregar um documento como Google Doc (ebook, plano, proposta, relatorio, manual, dossie, roteiro) que o dono abre e edita no Drive. Ensina o formato de saida canonico e o pipeline seguro (markdown para pandoc para gog --convert-to doc), sem chave nova nem escopo de Gmail/contatos. NAO use para PDF, para site publicado, nem para .md que fica so no disco.
---

# soft-google-docs

Entrega canonica de Google Doc do LEON. Todo Google Doc que qualquer LEON gerar passa por aqui,
pra sair sempre no mesmo formato limpo e editavel: titulo, cabecalhos reais, negrito/italico,
tabela nativa, listas, checklist e linha divisoria — nao um bloco de texto corrido.

## Regra de ouro

O documento nasce em **Markdown**, vira **HTML com pandoc**, e sobe como **Google Doc nativo com
`gog ... --convert-to doc`**. Nunca cole markdown cru dentro do Doc (sai `##` e `**` literais na
tela). Nunca reconstrua por bbox/PDF. Nunca peca chave nova nem escopo de Gmail/Drive-total: o
`gog` ja usa a conta do dono (leomolina@raizonline.com.br).

## O pipeline (3 passos)

```bash
# 0. carrega o .env do agente (traz as credenciais do gog) — rode de dentro do dir do agente
set -a; . ./.env 2>/dev/null; set +a
GOG=/home/cloud/.local/bin/gog

# 1. Markdown -> HTML (pandoc ja instalado em /usr/bin/pandoc)
pandoc /tmp/doc.md -f markdown -t html -o /tmp/doc.html

# 2. HTML -> Google Doc nativo, na pasta certa do Drive
$GOG drive upload /tmp/doc.html --name "Nome do Documento" --convert-to doc --parent <FOLDER_ID> -j
```

O `-j` devolve JSON com o `id` do Doc criado. A URL pro dono e sempre:
`https://docs.google.com/document/d/<ID>/edit`  (mandar CRUA, nunca em markdown `[nome](url)`).

Atalho: `scripts/md2doc.sh /tmp/doc.md "Nome" <FOLDER_ID>` faz os 3 passos e imprime a URL.

## Formato de saida canonico (o que usar no Markdown)

Ver `references/formato-saida.md` pra tabela completa de cada elemento e como ele cai no Doc.
Resumo do que SEMPRE entra num entregavel:

- `#` titulo / `##` `###` secoes e subsecoes (viram Titulo/Cabecalho 1/2 reais, indexaveis)
- `**negrito**` e `*italico*` pra enfase (nunca CAIXA ALTA como enfase)
- tabela markdown com `|` pra qualquer dado comparavel (vira tabela nativa, nao texto)
- `-` lista e `1.` lista numerada; `- [ ]` / `- [x]` pra checklist
- `` `code` `` e bloco ``` pra comando/trecho literal
- `---` linha divisoria entre grandes blocos
- Densidade: cada secao com titulo proprio; sem "titulo + blocao de texto" (reprovado 13/08)

## Atualizar um Doc que ja existe

Google Doc nativo NAO troca o conteudo mantendo o mesmo link (`--convert` so vale na criacao).
Entao: gera um Doc NOVO, e no Drive RENOMEIA o antigo pra `[SUBSTITUIDO AAAA-MM-DD] <nome>`
(nao apaga — aguarda OK do dono pra remover). Avisa o dono qual link usar agora.

## Provar antes de dizer "pronto"

Baixa o conteudo de volta e confere que nao veio vazio:

```bash
$GOG drive download <ID> --output /tmp/check.txt --format txt && wc -c /tmp/check.txt
```

`test -s /tmp/check.txt` tem que passar e o texto tem que bater com o que voce escreveu.
"Subi o Doc" sem esse download de volta e `[NAO VERIFICADO]`.

## O que NAO fazer

- Nao importar scripts Ruby/gems de terceiro que pedem escopo de Gmail/contatos/Drive-total:
  o `gog` ja resolve tudo com a conta do dono, sem essa superficie de risco.
- Nao mandar PDF nem site publicado como "preview" de doc (bagunca o Telegram — regra do dono).
- Nao deixar markdown cru no Doc. Sempre passar pelo pandoc.
