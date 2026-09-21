# SOCORRO: sintoma, causa, conserto

Comece pelo sintoma na fala de quem reclamou. Rode o comando da coluna do meio antes de concluir qualquer coisa. **Sem a saída na mão, não diga a causa.**

Nesta página, `<pasta>` é a pasta da instalação, padrão `/opt/soft-members`, e `<dominio>` é o endereço da área de membros.

Atalho que serve para quase tudo:

```bash
docker compose -f <pasta>/docker-compose.yml ps
docker compose -f <pasta>/docker-compose.yml logs --tail=60 app
docker compose -f <pasta>/docker-compose.yml logs --tail=60 caddy
```

---

## Tabela rápida

| Sintoma | Onde olhar | Conserto |
|---|---|---|
| O endereço não abre de jeito nenhum | `dig +short <dominio>` e `curl -4 -s https://api.ipify.org` | os dois precisam bater. Diferente, o DNS é a causa, ver abaixo |
| Abre com aviso de site perigoso | `docker compose -f <pasta>/docker-compose.yml logs --tail=40 caddy` | certificado não emitido, ver abaixo |
| O programa sobe e cai sozinho | `docker compose -f <pasta>/docker-compose.yml logs --tail=40 app` | quase sempre variável faltando, rode `bash <pasta>/checar_env.sh` |
| Erro logo na primeira visita, falando em buscar o endereço | registros do app, procure por `verify-domain` ou `fetch failed` | o programa chama ele mesmo pelo endereço público, ver abaixo |
| Não chega e-mail nenhum | `docker compose -f <pasta>/docker-compose.yml logs --tail=60 app \| grep -i mail` | dados de envio errados, ver abaixo |
| Aluno diz que não consegue entrar | pergunte primeiro: erro de senha, link vencido, ou nada chegou | ver a seção do aluno |
| O dono entra e o painel devolve para o login | o endereço do navegador começa com `http://` | HTTP puro não autentica. Use sempre HTTPS |
| Botão de publicar recusa | o aviso em inglês na tela | falta nome no perfil ou plano Free, ver `references/ORGANIZAR.md` |
| Envio de imagem responde erro | o código que voltou na resposta | 400, 401, 403, 413 ou 415, cada um com conserto próprio em `references/personalizar.md` |
| O curso sumiu depois de mexer no docker | `docker volume ls \| grep mongo` | o volume guarda o banco. Se o volume foi apagado, reponha pela cópia de segurança |

---

## O endereço não abre

```bash
dig +short <dominio>
curl -4 -s https://api.ipify.org; echo
```

Saídas diferentes significam que o endereço não aponta para esta máquina. Frase para o dono:

> No painel onde você comprou o domínio, o registro do tipo A precisa ter o IP que eu te mando. Se tiver uma opção de proxy ou de nuvem ligada nesse registro, ela precisa ficar desligada. Me avisa quando ajustar.

Mudança de DNS leva de minutos a horas. Confira de novo com o mesmo comando antes de mexer em qualquer outra coisa.

---

## Porta 80 ou 443 ocupada ou fechada

```bash
ss -ltn | grep -E ':(80|443) '
```

**Ocupada por outro programa** (nginx, apache, outro container): dois programas não dividem a mesma porta. Ou o outro sai, ou a área de membros não sobe. Isso é decisão do dono, pergunte antes de parar qualquer coisa que já esteja servindo o negócio dele.

**Fechada por fora** (firewall do provedor, ou da própria máquina): de outra máquina, `curl -I http://<dominio>` fica sem resposta. O certificado precisa da porta 80 aberta para ser emitido, e o site precisa da 443. Peça ao dono para liberar as duas no painel do provedor dele. Sem isso, não existe caminho por aqui.

---

## Certificado não emitido

```bash
docker compose -f <pasta>/docker-compose.yml logs --tail=60 caddy
```

Causas, em ordem de frequência: DNS ainda não aponta para esta máquina, porta 80 fechada por fora, ou domínio digitado com diferença no `.env`.

Confira a linha do endereço:

```bash
grep '^DOMINIO=' <pasta>/.env
```

Sem `https://`, sem barra no fim, exatamente igual ao que o DNS resolve. Depois de corrigir, `docker compose -f <pasta>/docker-compose.yml restart caddy` e espere um minuto.

---

## O programa chama ele mesmo e falha

Sintoma: erro na primeira visita, e nos registros aparece `verify-domain` ou `fetch failed`.

Causa: em toda requisição, o programa faz uma chamada para ele mesmo pelo endereço público. O container precisa conseguir resolver o próprio domínio e alcançar o próprio IP de dentro da rede da máquina. Em rede que não devolve o próprio IP para dentro, essa chamada falha e derruba a página, e a mensagem de erro não conta nada disso.

Conferência de dentro do container:

```bash
docker compose -f <pasta>/docker-compose.yml exec app sh -lc "getent hosts <dominio>; curl -s -o /dev/null -w '%{http_code}\n' https://<dominio>/healthy"
```

Falhando ali dentro, o caminho é dar ao container um jeito de resolver o próprio nome, apontando o domínio para o serviço interno do proxy. **Este ponto nunca foi provado numa VPS de cliente**, só numa bancada local com apelido de rede. Se cair aqui, diga ao dono que emperrou nisto, registre a saída do comando, e não prometa prazo.

---

## E-mail não chega

```bash
docker compose -f <pasta>/docker-compose.yml logs --tail=80 app | grep -i mail
grep -E '^EMAIL_' <pasta>/.env
```

| O que aparece | Causa | Conserto |
|---|---|---|
| erro de autenticação | usuário ou senha do envio errados | muitos provedores exigem senha de aplicativo, e não a senha da conta. Peça a senha de aplicativo ao dono |
| conexão recusada, ou tempo esgotado | porta errada, ou saída bloqueada pelo provedor da VPS | tente 587 com TLS e 465 com SSL. Continuando bloqueado, o provedor da VPS barra a saída de e-mail, e a saída é um serviço de disparo por e-mail |
| remetente recusado | o remetente não pertence ao domínio autorizado | o campo de remetente precisa ser um endereço da conta de envio |
| nada nos registros | o e-mail saiu, e parou antes de chegar | procure no spam, confira o endereço do destinatário letra por letra |

Depois de corrigir o `.env`:

```bash
bash <pasta>/checar_env.sh && docker compose -f <pasta>/docker-compose.yml up -d
```

Prove com gente de verdade: peça ao dono para pedir um código na tela de login e dizer se chegou.

**O código de acesso nunca aparece nos registros nesta versão**, e isso foi conferido. Se alguém achar um código escrito no registro, a instalação está fora de produção e isso precisa ser resolvido na hora.

---

## O aluno não consegue entrar

Pergunte primeiro qual dos três é. Cada um tem conserto diferente.

| O aluno diz | Causa | Conserto |
|---|---|---|
| "não recebi nada" | e-mail no spam, endereço errado, ou envio parado | siga `references/diagnostico.md`, bloco `O aluno não recebeu o e-mail` |
| "cliquei no link e deu erro" | o link de criar senha vale 60 minutos | ele usa esqueci minha senha na tela de login e recebe outro |
| "minha senha não funciona" | senha errada mesmo, ou conta sem senha criada | esqueci minha senha resolve os dois |
| "entro e não vejo o curso" | matrícula faltando | convide ele no curso certo pela Ação 3. Aluno sem matrícula vê "Conteúdo bloqueado", e isso é o certo |
| "não consigo criar minha conta" | criar conta por senha é recusado de propósito | quem dá acesso é o dono, pelo convite. Explique isso ao aluno |

---

## O painel não autentica

Se o dono entra e volta para a tela de login em círculo, olhe o endereço do navegador. Começando com `http://`, essa é a causa: fora do HTTPS o navegador e o programa discordam sobre o dado da sessão, e ninguém fica logado. Defeito herdado, sem conserto nesta versão.

Nunca sirva a área de membros em endereço sem HTTPS, nem "só para testar".

---

## Sem logo e sem capa

A instalação guarda imagem no disco da própria máquina, num volume do docker. Envio de logo e de capa funciona, e não depende de serviço de fora nenhum.

Se o envio responder erro, o código diz o motivo: 401 e 403 são chave de API errada ou sem permissão, 413 é arquivo acima do teto, 415 é formato que não entra, 400 é pedido malformado. O conserto de cada um está em `references/personalizar.md`.

Antes de procurar defeito no envio, confira se o volume de imagem existe: `docker volume ls | grep media`. Volume apagado leva junto toda imagem já enviada.

---

## Espaço em disco acabando

```bash
df -h /
docker system df
```

Imagens antigas acumulam a cada atualização. Com a versão atual provada e funcionando, limpe o que sobrou:

```bash
docker image ls soft-members
docker image rm <etiqueta antiga>
```

Apague uma etiqueta por vez, e nunca a que está escrita no `SOFT_MEMBERS_IMAGE=` do `.env`.
