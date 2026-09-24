# ATUALIZAR: trocar a versão com volta automática

Atualização mexe no que está no ar. Ela só começa com ordem nomeada do dono para atualizar a área de membros.

O `update.sh` confere o ambiente, faz a cópia do banco, carrega ou baixa a imagem, troca `SOFT_MEMBERS_IMAGE`, sobe os serviços, testa a saúde e volta sozinho para a imagem anterior se o teste falhar.

## 1 · Conferir a imagem atual

```bash
grep '^SOFT_MEMBERS_IMAGE=' <pasta>/.env
docker image ls soft-members
```

Guarde a saída no relato. O script também lê essa etiqueta e a usa na volta automática.

## 2 · Preparar e instalar a versão nova

Não reaproveite a etiqueta anterior. Para construir na VPS:

```bash
docker build -f services/app/Dockerfile -t soft-members:2026-09-20 .
bash <pasta>/update.sh --image soft-members:2026-09-20
```

Para carregar um arquivo trazido de outra máquina:

```bash
bash <pasta>/update.sh --image soft-members:2026-09-20 --image-archive <caminho>/<arquivo-da-imagem>.tar.gz
```

Para baixar de um repositório acessível pela VPS:

```bash
bash <pasta>/update.sh --image <repositorio>/soft-members:2026-09-20 --pull-image
```

O comando só termina com sucesso depois do backup e da resposta 200 em `https://<dominio>/healthy`. Se a versão nova falhar, o script restaura a etiqueta anterior no `.env`, sobe os serviços antigos e retorna erro.

Teste as ações sem trocar nada:

```bash
bash <pasta>/update.sh --image soft-members:2026-09-20 --dry-run
```

## 3 · Conferir o resultado

```bash
grep '^SOFT_MEMBERS_IMAGE=' <pasta>/.env
curl -s -o /dev/null -w "%{http_code}\n" https://<dominio>/healthy
docker compose --env-file <pasta>/.env -f <pasta>/docker-compose.yml ps
```

O fechamento exige a etiqueta nova, resposta `200` e os três serviços da instalação (`app`, `mongo` e `caddy`) de pé na saída do `ps`.

Se houve volta automática, avise:

> A versão nova não respondeu, então a volta automática recolocou a versão anterior. A área está funcionando como antes. Vou conferir o motivo antes de tentar de novo.

Leia o registro sem derrubar o serviço:

```bash
docker compose --env-file <pasta>/.env -f <pasta>/docker-compose.yml logs --tail=80 app
```

## Quando o banco precisa voltar junto

Só restaure quando a versão nova estragou dados e o dono confirmou, pelo nome da cópia, que tudo criado depois dela pode ser perdido. O restaurador recusa banco que contenha documentos.

```bash
bash <pasta>/restore_mongo.sh --archive <pasta>/backups/<arquivo>.archive.gz
```

As credenciais vêm do `.env` e a senha não entra na linha de comando. Sem banco vazio, o script para.

## Relato

```text
cópia antes: <arquivo e tamanho>
versão anterior: <etiqueta>
versão nova: <etiqueta>
healthy depois: <código>
volta automática: sim ou não, e por quê
```

Nenhuma linha se preenche de cabeça.
