# ARQUIVO PARA MEMBROS: arquivo que só aluno ativo baixa

O dono quer entregar um arquivo (um programa, uma planilha, um pacote) só pra quem tem acesso ativo na área. Às vezes quer também que o programa que o aluno instalou procure versão nova sozinho. As duas coisas saem da mesma rota da área de membros, sem cadastro novo e sem registro de quem baixou.

O envio de mídia não serve pra isso: ele guarda só imagem, e aula do tipo `file` ou `pdf` não funciona nesta instalação. O arquivo mora numa pasta da própria instalação, montada só pra leitura dentro do app.

## O que perguntar ao dono

1. Qual o arquivo e qual nome curto ele ganha no endereço (só letras minúsculas, números e hífen, como `kit-planilhas`).
2. Quem pode baixar: qualquer aluno com acesso ativo, ou só quem tem um curso específico.
3. Em qual curso e em qual módulo fica a aula com o botão de baixar.

Uma pergunta por vez, em linguagem de gente.

## Como a rota decide

`GET /api/member-files/<nome>` entrega o arquivo. `GET /api/member-files/<nome>?info=1` entrega a ficha da versão (o `versao.json`).

- **Quem passa:** o aluno logado no site, pela sessão, ou quem manda o e-mail do aluno no cabeçalho `x-membro-email`. O e-mail vai no cabeçalho, nunca no endereço, pra não aparecer em log de ninguém.
- **Quem é membro:** usuário ativo com pelo menos um curso liberado. Assinatura cancelada vale até o fim do período já pago. Com a variável `MEMBER_FILES_COURSE_IDS` (ids separados por vírgula) só contam os cursos da lista.
- **Recusa:** qualquer recusa volta o mesmo 404. A resposta nunca conta se o e-mail existe.
- **Nada é gravado:** a rota não anota atividade, não cria link de download e não registra chamada. O único rastro fica na memória do processo: 10 tentativas erradas do mesmo IP em 15 minutos devolvem 429 até a janela passar. Atrás do túnel da Cloudflare o IP contado é o do `cf-connecting-ip`, e endereço IPv6 conta pela rede /64 inteira.
- **Só pelo túnel:** o `cf-connecting-ip` só merece confiança se o app recebe pedido apenas pelo túnel. Um proxy aberto na 80 ou na 443 que repasse pro app (um Caddy esquecido, por exemplo) deixa qualquer um escolher o IP e contornar o limite. Rode `ss -ltn` e feche o que escuta em `0.0.0.0` ou `[::]` sem servir ninguém.
- **Sem cópia no caminho:** toda resposta sai com `Cache-Control: private, no-store`, então a Cloudflare não guarda o arquivo pra entregar a quem não é membro.

A rota existe a partir da versão da área de 29/09. Instalação mais antiga responde 404 em qualquer pedido: rode a ação ATUALIZAR antes.

## 1 · Montar a pasta

No compose da instalação, o serviço `app` ganha uma linha em `volumes`:

```yaml
            - ./member-files:/data/member-files:ro
```

O `docker-compose.yml` que vem com a instalação desde 29/09 já traz essa linha. Em instalação mais antiga, acrescente e recrie só o app:

```bash
docker compose --env-file <pasta>/.env -f <pasta>/docker-compose.yml up -d --force-recreate --no-deps app
```

Nunca suba o compose sem a linha do volume de mídia (`media_data:/data/media`): o app volta sem logo e sem capas. Recriar só o app deixa o site uns 30 segundos fora, então combine o horário com o dono.

## 2 · Pôr o arquivo

Na VPS, uma pasta por nome, com o arquivo e a ficha:

```text
<pasta>/member-files/kit-planilhas/
    kit-planilhas-1.0.0.zip
    versao.json
```

O `versao.json`:

```json
{
  "versao": "1.0.0",
  "arquivo": "kit-planilhas-1.0.0.zip",
  "sha256": "<sha256 do arquivo>",
  "tamanho": 95321,
  "publicadoEm": "2026-09-29T03:00:00Z",
  "notas": "o que mudou nesta versão, em uma linha"
}
```

O campo `arquivo` é só o nome, sem pasta e sem `..`. Ficha fora desse formato faz a rota responder 404.

O app lê essa pasta como o usuário `nextjs` (uid 1001), que não é dono de nada ali. Pasta em `0755`, arquivo e ficha em `0644`. Arquivo que nasce `0600` (o `mktemp` e o `tempfile` do Python criam assim) fica ilegível pro app: a rota responde 404 a todos os alunos e deixa no log do app a linha `member-files: sem permissao de leitura em <nome>`. Por isso tudo entra por `install -m 0644`, nunca por `mktemp` seguido de `mv`.

Versão nova não pede imagem nova nem reinício. A ordem protege quem baixa no meio da troca:

```bash
install -d -m 0755 <pasta>/member-files/kit-planilhas
install -m 0644 kit-planilhas-1.1.0.zip <pasta>/member-files/kit-planilhas/
sha256sum <pasta>/member-files/kit-planilhas/kit-planilhas-1.1.0.zip
# a ficha nova entra já em 0644, com nome provisório na mesma pasta, e troca de uma vez
install -m 0644 versao.json <pasta>/member-files/kit-planilhas/versao.json.novo
mv <pasta>/member-files/kit-planilhas/versao.json.novo <pasta>/member-files/kit-planilhas/versao.json
# o app enxerga? (o docker exec roda como o usuário do app)
docker exec <container do app> sh -c 'cd /data/member-files/kit-planilhas && test -r versao.json && test -r kit-planilhas-1.1.0.zip' && echo legivel
```

O arquivo novo entra primeiro e a ficha por último. Apague a versão velha só depois que a ficha nova estiver no lugar e o `legivel` aparecer.

## 3 · A aula com o botão

A aula é de **texto**, criada como em `criar-curso.md` (seção "Aula de texto"), com `requiresEnrollment: true` e um link pro endereço completo:

```json
{"type":"text","text":"Baixar o arquivo","marks":[{"type":"link","attrs":{"href":"https://<dominio>/api/member-files/kit-planilhas"}}]}
```

Aula `embed` não serve: ela roda num quadro isolado que o navegador proíbe de baixar arquivo. Pra aula aparecer no menu do aluno, grave o caminho dela nos links extras do menu (`personalizar.md`).

Crie o módulo e a aula só depois que o arquivo estiver na pasta e o `legivel` da seção 2 aparecer, e crie a aula já publicada (`published: true`). Módulo sem aula publicada aparece na trilha de todos os alunos como "em breve", com o título à vista, até alguém publicar. Se a aula falhar depois do módulo criado, apague o módulo vazio (`DELETE /api/products/<curso>/sections/<id do módulo>`).

## 4 · Programa do aluno que se atualiza sozinho

O programa guarda o e-mail do aluno e o endereço da área. De tempos em tempos:

```bash
curl -fsS -H "x-membro-email: <e-mail do aluno>" "https://<dominio>/api/member-files/kit-planilhas?info=1"
```

Se a `versao` mudou, baixa o arquivo pelo mesmo endereço sem o `?info=1`, confere tamanho e `sha256` com a ficha e só então troca. 404, 429 ou falta de rede contam como "sem atualização": o programa segue rodando com a versão que tem. Quem perde o acesso na área deixa de receber versão nova e continua com a última que baixou.

O e-mail é a única chave desse caminho. Quem souber o e-mail de um aluno baixa o arquivo. Guarde ali só o que o dono aceita entregar nessa condição.

## 5 · Prova antes de dizer pronto

```bash
# o app lê a ficha e o arquivo: legivel
docker exec <container do app> sh -c 'cd /data/member-files/kit-planilhas && test -r versao.json && test -r <arquivo da ficha>' && echo legivel
# sem nada: 404
curl -s -o /dev/null -w "%{http_code}\n" "https://<dominio>/api/member-files/kit-planilhas?info=1"
# e-mail de aluno ativo que o dono escolheu: 200, e só o código aparece
curl -s -o /dev/null -w "%{http_code}\n" -H "x-membro-email: <e-mail>" "https://<dominio>/api/member-files/kit-planilhas?info=1"
# cabeçalho de cache: private, no-store
curl -sI -H "x-membro-email: <e-mail>" "https://<dominio>/api/member-files/kit-planilhas" | grep -i cache-control
# logo depois, sem e-mail: 404 e cf-cache-status diferente de HIT (a borda não guardou a cópia do aluno)
curl -sI "https://<dominio>/api/member-files/kit-planilhas" | grep -i '^HTTP\|cf-cache-status'
```

Depois o dono abre a aula no celular e baixa. Esse clique é a prova que vale.

## Relato

```text
nome no endereço: <nome>
versão na ficha: <versao>
app lê ficha e arquivo: <legivel ou não>
sem e-mail: <código>
com e-mail de aluno: <código>
cache-control: <valor>
aula: <link da aula>
```

Nenhuma linha se preenche de cabeça. E-mail de aluno nunca vai pro relato nem pro chat.
