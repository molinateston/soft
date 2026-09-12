# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nomes, identificadores, endereços e conteúdos foram inventados só
> pra mostrar a FORMA de cada saída. Nenhum identificador desta página existe de verdade e nenhum
> link daqui abre. Num trabalho real, todo identificador vem do retorno da ferramenta, nunca da
> memória, e o que não foi verificado sai marcado `[NÃO VERIFICADO]`.

**O caso fictício:** uma escola de idiomas de bairro montou um manual de atendimento de 14 páginas em
Markdown e quer o documento no Drive, para a coordenação editar junto. Depois de uma semana, o texto
muda e ela pede a segunda versão.

---

## Rodada 1 · Ação 1, PUBLICAR

### O que o usuário deu

> "Terminei o manual de atendimento. Joga isso no Google Docs pra mim, quero mandar o link pra
> coordenação hoje ainda."
>
> Anexo: `manual-atendimento.md`, 14 páginas, com título, 6 seções, 2 tabelas e uma checklist de
> abertura de turma.

### A pergunta que a skill fez

Uma só, porque só faltava um insumo:

> "Em que pasta do Drive esse documento deve ficar? Pode me mandar o link da pasta que eu pego o
> identificador. Se preferir, eu crio uma pasta chamada Manuais e te digo qual foi."

Resposta do usuário: colou `https://drive.google.com/drive/folders/1BcD3fG5hJ7kL9mNpQrS`.

O identificador da pasta é o trecho depois de `/folders/`: `1BcD3fG5hJ7kL9mNpQrS`.

O nome do documento não foi perguntado: a skill usou o título `#` do próprio Markdown, que era
"Manual de Atendimento", e declarou isso em uma linha na entrega.

### Passo 1, o que o ambiente tinha

```
$ command -v gog
/usr/local/bin/gog
$ command -v pandoc
/usr/bin/pandoc
```

As duas presentes, então o caminho completo rodou.

### Passo 3, a conversão e a subida

```
$ pandoc manual-atendimento.md -f markdown -t html -o manual-atendimento.html
$ $GOG drive upload manual-atendimento.html --name "Manual de Atendimento" \
    --convert-to doc --parent 1BcD3fG5hJ7kL9mNpQrS -j
```

### Passo 4, o retorno bruto e o campo que interessa

```json
{
  "id": "1aZk9QpLmN3vX7bR2sT8yUwE4cVhGjKdF",
  "name": "Manual de Atendimento",
  "mimeType": "application/vnd.google-apps.document",
  "parents": ["1BcD3fG5hJ7kL9mNpQrS"],
  "createdTime": "2026-08-07T14:22:08.311Z",
  "webViewLink": "https://docs.google.com/document/d/1aZk9QpLmN3vX7bR2sT8yUwE4cVhGjKdF/edit"
}
```

O campo a extrair é o `id`. Os outros são conferência: `mimeType` terminando em
`vnd.google-apps.document` confirma que virou Doc nativo e não ficou como arquivo HTML solto no
Drive; `parents` confirma que caiu na pasta certa. Se o `mimeType` viesse `text/html`, a conversão
falhou e o passo se refaz.

### Passo 5, a prova

```
$ $GOG drive download 1aZk9QpLmN3vX7bR2sT8yUwE4cVhGjKdF --output check.txt --format txt
$ wc -c check.txt
  21847 check.txt
```

21.847 bytes, compatível com as 14 páginas. Primeira linha do arquivo baixado: `Manual de
Atendimento`. Bate com o escrito, então a entrega está provada.

### O gate, conferido em silêncio

| Check | Resultado |
|---|---|
| Doc verificado | passou, download de volta com 21.847 bytes |
| Sem Markdown cru | passou, nenhum `##` nem `**` no texto baixado |
| Estrutura de verdade | passou, 6 cabeçalhos e 2 tabelas nativas no Doc |
| Link cru | passou |
| Pasta declarada | passou, pasta indicada pelo usuário |
| Nada inventado | passou, os dois comandos existiam no ambiente |

### A saída, como ela chega ao usuário

> Manual de Atendimento no ar, 14 páginas, na pasta que você mandou.
>
> https://docs.google.com/document/d/1aZk9QpLmN3vX7bR2sT8yUwE4cVhGjKdF/edit
>
> Nome tirado do título do arquivo. Conferi baixando o texto de volta: as 6 seções, as 2 tabelas e a
> checklist chegaram como elementos nativos, dá pra editar direto e o sumário automático funciona.
> O `.md` e o `.html` ficaram salvos ao lado, caso queira gerar de novo.

---

## Rodada 2 · Ação 2, ATUALIZAR (uma semana depois)

### O que o usuário deu

> "Mudei a parte de reclamação e adicionei uma seção de matrícula. Sobe de novo."

### A pergunta que a skill fez

Nenhuma. O identificador do Doc anterior e a pasta já estavam na conversa, então a skill seguiu
direto e só declarou o que ia fazer:

> "Vou gerar um Doc novo e renomear o antigo, porque Doc nativo não troca conteúdo mantendo o mesmo
> link. Nada é apagado."

### O que rodou

```
$ pandoc manual-atendimento.md -f markdown -t html -o manual-atendimento.html
$ $GOG drive rename 1aZk9QpLmN3vX7bR2sT8yUwE4cVhGjKdF "[SUBSTITUIDO 2026-08-14] Manual de Atendimento"
$ $GOG drive upload manual-atendimento.html --name "Manual de Atendimento" \
    --convert-to doc --parent 1BcD3fG5hJ7kL9mNpQrS -j
```

Retorno do novo, só o campo que importa:

```json
{"id":"1TgH5jK7lM9nP2qR4sV6xY8zA1bC3dE5f","name":"Manual de Atendimento","parents":["1BcD3fG5hJ7kL9mNpQrS"]}
```

Prova: download de volta com 24.109 bytes, seção "Matrícula" presente no texto baixado.

### A saída, como ela chega ao usuário

> Versão nova no ar, com a seção de Matrícula:
>
> https://docs.google.com/document/d/1TgH5jK7lM9nP2qR4sV6xY8zA1bC3dE5f/edit
>
> O anterior continua no Drive, renomeado para `[SUBSTITUIDO 2026-08-14] Manual de Atendimento`,
> caso queira comparar. Me diga quando puder apagar, que eu não removo nada por conta.

---

## Rodada 3 · o mesmo pedido, num ambiente sem as ferramentas

Vale mostrar porque é o caso mais comum fora de um servidor preparado.

```
$ command -v gog
$ command -v pandoc
/usr/bin/pandoc
```

Só o conversor existe. A skill não fingiu que subiu nada:

> Gerei o documento formatado, mas neste ambiente não tenho a ferramenta do Drive conectada, então
> não consigo subir por aqui.
>
> Arquivo: `manual-atendimento.html`
>
> Dois cliques pra virar Doc nativo com a formatação intacta: abra o Drive, "Novo > Upload de
> arquivo", suba esse `.html`, clique com o botão direito nele e escolha "Abrir com > Google Docs".
> As 6 seções, as tabelas e a checklist chegam prontas.

Se nem o conversor existisse, a entrega seria o `.md` no formato canônico mais a mesma explicação,
com o comando de conversão para o usuário rodar depois.

---

## Uma falha real, e como ela foi tratada

Numa das rodadas fictícias, a subida devolveu isto:

```
error: token expired or revoked for the configured account
```

O que a skill NÃO fez: pedir chave nova, tentar outra ferramenta, ou dizer que subiu.

O que a skill fez:

> A conta do Drive configurada aqui está com a autenticação vencida, então a subida não passou. Isso
> se resolve reconectando a conta no seu ambiente, não é coisa que eu consiga contornar por dentro.
>
> Enquanto isso, o `manual-atendimento.html` já está pronto e sobe em dois cliques pelo Drive
> (Novo > Upload de arquivo, depois Abrir com > Google Docs).

Nada foi marcado como entregue, e a mensagem separou o que a skill fez do que depende do usuário.
