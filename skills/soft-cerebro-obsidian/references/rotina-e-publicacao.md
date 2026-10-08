# Atualização diária e publicação

## Atualizar à mão

```bash
bash scripts/atualiza.sh /caminho/completo/config.json
```

Monta o mapa de novo, confere a base e escreve uma linha em `cerebro-diario.log`, ao lado do config. A última linha precisa ser `OK`.

## Atualizar todo dia sozinho

Mac ou Linux: rode `crontab -e` e cole (todo dia às 23h):

```
0 23 * * * bash /caminho/scripts/atualiza.sh /caminho/config.json
```

Windows: use o Agendador de Tarefas e chame o mesmo script pelo Git Bash ou pelo WSL.

No dia seguinte, abra `cerebro-diario.log`: a última linha precisa ser `OK`.

## Publicar para ver no celular (opcional)

A página é um arquivo só. No computador, basta abrir o `index.html`. Para ver no celular de qualquer lugar, suba a pasta `cerebro-site/` numa hospedagem de site estático (GitHub Pages, Netlify ou um servidor seu).

Para o `atualiza.sh` publicar e conferir sozinho, defina antes:

```
PUBLICAR="comando que publica a pasta do mapa"
URL="https://seu-endereco/cerebro/"
```

Ele roda o comando e depois confere se o endereço responde com o mapa.

## Cuidado com a privacidade

O mapa mostra o nome de todas as notas, e por padrão um resumo do texto. Antes de publicar:

1. Ponha senha no endereço (a hospedagem costuma ter essa opção), ou deixe o mapa só no computador.
2. Se o endereço for aberto, use `"texto": "nenhum"` no config para a página não levar o conteúdo.
3. Rode `python3 scripts/confere.py config.json` e zere os erros de segredo.
