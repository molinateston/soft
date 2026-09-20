# Instalar a área de membros na VPS do dono

Use o pacote oficial entregue pelo fornecedor. Ele contém o snapshot do código, as imagens do app, MongoDB e Caddy, o instalador e checksums. Esse caminho offline foi provado numa VPS Ubuntu 24.04 limpa e não depende de GitHub ou registry.

O agente executa os comandos na VPS. O dono recebe perguntas curtas e, no fim, abre a escola pelo celular.

## 1. Coletar sem expor segredo

Pergunte uma coisa por vez:

1. `Qual endereço você quer para a área de membros? Normalmente é membros.seudominio.com.br.`
2. `Qual e-mail será o dono da escola?`
3. `Qual nome, subtítulo e cor principal você quer usar?`
4. `Quais são o servidor, a porta, o usuário, o remetente e a senha SMTP?`

Guarde a senha SMTP num arquivo temporário com permissão `600`. Não ponha a senha no chat, no histórico do shell ou no argumento `--smtp-pass`.

## 2. Conferir a entrega

Na pasta que recebeu `soft-members-<versao>.tar` e o arquivo `.sha256`:

```bash
sha256sum -c soft-members-<versao>.tar.sha256
tar -xf soft-members-<versao>.tar
cd soft-members-<versao>
sha256sum -c SHA256SUMS
```

As duas conferências precisam responder `OK`. O pacote inclui:

- `soft-members-images-<versao>.tar.gz`, com as três imagens Docker;
- `soft-members-source-<versao>.tar.gz`, com o código-fonte exato da entrega;
- `deployment/install.sh` e os scripts de operação;
- `release.json`, com versão, commit e ids das imagens.

Falha de checksum encerra a instalação. Peça uma nova cópia do pacote.

## 3. Pré-voo da VPS

Instale Docker Engine e o plugin Compose pela fonte oficial da distribuição. Depois confira:

```bash
docker --version
docker compose version
ss -ltn | grep -E ':(80|443) ' || echo "portas livres"
dig +short <dominio>
curl -4 -s https://api.ipify.org; echo
```

As portas 80 e 443 precisam estar livres. O IP do `dig` precisa ser o mesmo da VPS. Se não for, pare e peça o ajuste do registro A antes de subir o serviço.

## 4. Instalar pelo pacote

O arquivo da senha SMTP deve ficar fora da pasta final e só pode ser lido pelo usuário que instala.

```bash
chmod 600 <arquivo-da-senha-smtp>
sudo ./deployment/install.sh \
  --domain <dominio> \
  --admin-email <email-do-dono> \
  --smtp-host <servidor-smtp> \
  --smtp-port <porta-smtp> \
  --smtp-user <usuario-smtp> \
  --smtp-pass-file <arquivo-da-senha-smtp> \
  --smtp-from <remetente> \
  --image soft-members:local \
  --image-archive ./soft-members-images-<versao>.tar.gz
```

O instalador:

- carrega as imagens sem rede externa;
- gera `AUTH_SECRET` e a senha do MongoDB;
- grava `/opt/soft-members/.env` com modo `600`;
- sobe app, banco e proxy;
- espera a saúde e inicializa a escola;
- cria a chave do LEON sem exigir abertura do painel;
- agenda o backup diário.

Ele recusa uma pasta que já tenha `.env`. Não apague uma instalação existente para repetir. Use `update.sh` ou diagnostique o erro.

## 5. Provar serviço, chave e e-mail

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://<dominio>/healthy
stat -c "%a %n" /opt/soft-members/.env /opt/soft-members/chave-agente-leon.env
source /opt/soft-members/chave-agente-leon.env
curl -sS -o /dev/null -w "%{http_code}\n" \
  -H "x-api-key: $MEMBERS_API_KEY" \
  "https://<dominio>/api/products?limit=1"
```

Os dois códigos precisam ser `200` e os dois arquivos precisam mostrar modo `600`. A chave nunca entra no relatório ou no chat.

Peça ao dono para entrar pelo código recebido no e-mail. Depois crie um curso descartável, publique e convide um endereço de teste. O login do dono e o convite do aluno provam caminhos diferentes do SMTP. Remova apenas os dados descartáveis identificados pelo teste.

## 6. Aplicar a marca

Guie o dono pelo painel:

1. `Settings`, depois `Branding`: nome, subtítulo e logo.
2. Ative a remoção da marca do projeto de origem.
3. `Theme`: aplique a cor principal escolhida.

Abra uma página pública e uma aula como aluno. Confirme nome, logo, cor e ausência de marca de terceiro. O envio local de imagens já faz parte da instalação. Para capa de curso por API, siga `personalizar.md`.

## 7. Provar backup e restauração

```bash
sudo /opt/soft-members/backup_mongo.sh
ls -lh /opt/soft-members/backups/
crontab -l | grep backup_mongo
```

Cada execução gera um par com a mesma marca de tempo:

- `soft-members-<data>.archive.gz`, com o banco `courselit`;
- `soft-members-<data>.media.tar.gz`, com as imagens locais.

`restore_mongo.sh` recusa banco ou pasta de mídia com conteúdo. A restauração completa numa VPS vazia usa:

```bash
sudo /opt/soft-members/restore_mongo.sh \
  --archive <arquivo-do-banco> \
  --media-archive <arquivo-de-midia>
```

As sete cópias mais novas ficam na VPS. Recomende uma segunda cópia em outro provedor para cobrir perda total da máquina.

## 8. Aceite no celular

O dono precisa confirmar, no próprio celular:

- login recebido por e-mail;
- painel abrindo sem rolagem lateral;
- `Products` abrindo o produto correto;
- configurações abrindo;
- convite de aluno chegando;
- aluno entrando, abrindo uma aula e marcando conclusão;
- vídeo utilizável em retrato e paisagem.

Só declare instalado depois da confirmação do dono e de uma resposta `200` da API autenticada.

## Relatório final

Registre sem segredos:

```text
versão do pacote: <release.json>
checksums externo e interno: OK
dns: <ip>
healthy: 200
API autenticada: 200
e-mail do dono: recebido
convite do aluno: recebido
marca aplicada: sim
produto no mobile: abriu o produto correto
conclusão da aula: registrada
backup do banco: <arquivo e tamanho>
backup da mídia: <arquivo e tamanho>
cron: <linha>
dono confirmou: "<resposta>"
```

Item sem prova aparece como `não conferido`. Nunca preencha de memória.
