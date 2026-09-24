# Vender pelo checkout: venda vira acesso sozinha

Com a integração ligada, quem compra no checkout do dono entra na área de membros sem ninguém mexer. Serve para qualquer checkout que avise a venda por webhook: a instalação traz um adaptador pronto e aceita adaptador novo para o checkout que faltar. Esta reference liga a integração, cadastra os produtos, lê o histórico, conserta o que dá errado e ensina a escrever o adaptador de um checkout novo.

## Índice

- [Como funciona](#como-funciona)
- [O que acontece em cada aviso de venda](#o-que-acontece-em-cada-aviso-de-venda)
- [Vitrine: produto trancado com botão de compra](#vitrine-produto-trancado-com-botao-de-compra)
- [O que o agente NÃO faz](#o-que-o-agente-nao-faz)
- [Ligar a venda automática, em 5 passos](#ligar-a-venda-automatica-em-5-passos)
- [Cadastrar, listar e apagar produto](#cadastrar-listar-e-apagar-produto)
- [Ler o histórico de avisos](#ler-o-historico-de-avisos)
- [O que cada resultado quer dizer](#o-que-cada-resultado-quer-dizer)
- [Sintoma, causa, conserto](#sintoma-causa-conserto)
- [Checkout sem adaptador](#checkout-sem-adaptador)
- [O que perguntar ao dono](#o-que-perguntar-ao-dono)

## Como funciona

Três peças, todas na instalação:

1. **O webhook de venda**, um endereço por checkout: `https://<dominio>/api/integrations/checkout/<provedor>/webhook`. O `<provedor>` é o id do adaptador daquele checkout, em minúsculas. O adaptador lê o aviso no formato do checkout, confere o segredo e traduz para o formato único da área de membros.
2. **O mapa de produto**, em `/api/integrations/checkout/products`: diz qual produto do checkout libera qual curso. Vale para todo checkout.
3. **O histórico de avisos**, em `/api/integrations/checkout/events`: cada aviso recebido, o que o sistema fez com ele e por quê.

Para saber quais checkouts a instalação já entende, o agente lê a lista `webhook.providers` na listagem de produtos (passo 2). Id que não está na lista responde 404 com a lista dos instalados. Checkout do dono fora da lista pede um adaptador novo: seção [Checkout sem adaptador](#checkout-sem-adaptador).

Instalação anterior a 24/09 não tem essas rotas: o `GET` do webhook devolve a página de erro em vez de JSON. Atualize antes (`ATUALIZAR.md`). A atualização não mexe no que já vende: cadastros, histórico e o endereço de webhook antigo seguem valendo.

## O que acontece em cada aviso de venda

Em linguagem do dono, que é como o agente explica:

- **Compra aprovada:** o comprador ganha acesso aos cursos ligados àquele produto e recebe o e-mail de acesso. Quem nunca entrou na escola recebe o e-mail para criar a senha. Quem já era aluno recebe o aviso do curso novo.
- **Reembolso ou chargeback:** o acesso sai na hora. O progresso do aluno fica guardado.
- **Recompra depois do reembolso:** o acesso volta e o aluno continua de onde parou.
- **Cancelamento de assinatura:** o acesso continua até o fim do período já pago. Depois dessa data, na primeira vez que o aluno abre a aula, o acesso sai, com o progresso guardado. Se o checkout não mandar a data do fim do período, nada muda no acesso e o histórico marca o aviso.
- **Curso ainda não publicado:** a venda matricula assim mesmo e o histórico marca o aviso. No minuto em que o dono publica, o aluno entra.
- **Aviso repetido:** checkout reenvia o mesmo aviso às vezes. O segundo não duplica matrícula nem e-mail.
- **Pagamento recusado:** nada acontece.
- **Aluno com duas compras do mesmo produto:** reembolso de uma não tira o acesso que a outra ainda paga.
- **Aviso de teste:** nada muda na escola. O histórico registra e responde 200.

Diferença do convite manual de `matricular.md`: o convite manual exige curso publicado. A venda pelo checkout não exige.

O histórico guarda um resumo do e-mail do comprador, nunca o endereço. Cada aviso some do histórico depois de 180 dias.

## Vitrine: produto trancado com botão de compra

Desde 24/09, um curso publicado com link de venda aparece trancado para quem ainda não o tem: faixa em preto e branco com cadeado no início do curso do aluno e o botão "Quero acesso" levando ao checkout. A página do curso, para quem não é aluno, usa o mesmo link no botão de compra.

```bash
curl -s -X PATCH "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" -H "Content-Type: application/json" \
  -d '{"saleUrl":"https://checkout.exemplo.com/oferta"}'
```

Troque o endereço de exemplo pelo link da página de pagamento que o dono passar. Só `https://`, até 500 caracteres; vazio ou `null` tira. Com a venda automática ligada para esse produto, quem compra entra sozinho e a faixa ganha cor. Só faz sentido para produto cujas aulas já estão dentro da área de membros: senão o aluno compra e não tem o que assistir. Confirme isso com o dono antes de gravar o link.

## O que o agente NÃO faz

- **Não configura nada dentro do checkout.** Só o dono acessa o painel do checkout. O agente dita o que o dono cola lá, uma instrução por vez.
- **Não inventa segredo.** O segredo vem do dono: o que ele digitou no campo de segredo do webhook no checkout, ou o que o checkout gerou ali. O agente grava exatamente esse valor.
- **Não mostra o segredo ao dono depois de gravado.** Nem inteiro, nem pela metade. A API também não devolve: a leitura dos produtos diz só se há segredo (`webhookSecretSet`). Se o dono colar o segredo no chat, o agente grava, responde "segredo do checkout guardado" e pede para ele apagar aquela mensagem.
- **Não promete acesso sem ler o histórico.** "Liguei a venda automática" só sai depois do passo 5 com resposta boa.

## Ligar a venda automática, em 5 passos

Nesta seção, `<pasta>` é a pasta da instalação, padrão `/opt/soft-members`, `<dominio>` é o endereço da área de membros e `<provedor>` é o id do adaptador do checkout do dono, lido em `webhook.providers`.

### Passo 1. O segredo

O dono passa o segredo do webhook. Há dois lugares para gravar, e o agente escolhe um.

**No `.env` da instalação**, quando o dono usa o mesmo segredo em todos os produtos. É a linha:

```bash
CHECKOUT_WEBHOOK_SECRET=o-segredo-que-o-dono-passou
```

Ela vale para todo adaptador. Instalação antiga pode ter, em vez dela, a variável própria do adaptador que já vem pronto: as duas funcionam juntas, e a antiga não precisa sair. Sem a linha, acrescente no fim do `<pasta>/.env`. Para trocar de segredo sem derrubar venda nenhuma, a linha aceita mais de um valor, separados por vírgula, e o antigo sai depois que o checkout já estiver com o novo.

O app só lê o `.env` quando sobe de novo:

```bash
bash <pasta>/checar_env.sh && docker compose -f <pasta>/docker-compose.yml up -d
```

O `restart` não relê o `.env`. Use `up -d`.

**No cadastro do produto**, quando o checkout gera um segredo diferente para cada webhook. Vai no campo `webhookSecret` do passo 2, entre 8 e 256 caracteres, sem reiniciar nada.

Conferência, sem chave de API:

```bash
curl -s "https://<dominio>/api/integrations/checkout/<provedor>/webhook"
```

Resposta boa: `{"ok":true,"secretConfigured":true}`. Com `false`, o segredo não entrou: o `.env` não foi relido, ou a linha está vazia. Sem segredo nenhum, o checkout leva 503 em toda venda. Com 404 e `unknown_provider`, o id está errado: a resposta traz a lista certa em `providers`.

### Passo 2. Cadastrar o produto

O agente precisa do id do produto no checkout. O dono acha no painel do checkout, em geral na URL da página do produto ou nos detalhes dele. O agente pede o link da página do produto e tira o id de lá. Se não der para achar, há um atalho: com o webhook já apontado (passo 3), a primeira venda de um produto sem cadastro aparece em `unmappedRecent`, com o `productId` exato. Essa venda fica vermelha no checkout até o cadastro, e o reenvio matricula depois.

E precisa do `courseId` de cada curso que aquele produto libera, lido na lista de cursos da escola.

```bash
curl -s -X PUT "{{MEMBERS_URL}}/api/integrations/checkout/products" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"productId":"{{ID_DO_PRODUTO_NO_CHECKOUT}}","courseIds":["{{COURSE_ID}}"],"note":"Método X, venda única"}'
```

Detalhe no bloco de cadastro abaixo. Resposta 200 com `data.courses[].courseExists: true` em todos os cursos.

### Passo 3. O dono aponta o webhook no checkout

**Em alguns checkouts o webhook é por produto.** Produto sem webhook vinculado vende normalmente e não libera ninguém, e o painel mostra taxa de sucesso 0% nesse webhook. Pergunte ao dono se o painel dele liga webhook por produto ou para a conta inteira. Se for por produto, cada produto novo pede este passo de novo.

O agente dita ao dono, uma coisa por mensagem:

1. No painel do checkout, abra a área de webhooks (ou o produto, quando o webhook é por produto) e crie o webhook, ou vincule a este produto o que já existe.
2. Endereço: `https://<dominio>/api/integrations/checkout/<provedor>/webhook`
3. Segredo: o mesmo do passo 1.
4. Se o painel pedir para escolher eventos: compra aprovada, reembolso, chargeback e, se o produto for assinatura, cancelamento.

O agente não sabe o nome exato de cada botão no painel de cada checkout. Se o dono não achar, o agente pede um print da tela e guia pelo que aparece nele.

**Escola que já vendia antes de 24/09** tem um endereço de webhook antigo, cadastrado no painel na época. Ele segue funcionando igual e não precisa ser trocado. Webhook novo pode usar o endereço genérico.

### Passo 4. O dono aperta "testar" no checkout

No webhook recém-apontado, o dono aperta o botão de teste do checkout e diz quando apertou.

O botão de teste de alguns checkouts não manda marcador de teste. Ele manda um pedido de exemplo, com um produto que não existe na conta do dono e um link de pagamento de exemplo. O adaptador que já vem na instalação reconhece o pedido de exemplo do checkout dele e responde 200 com `test_mode`. Checkout cujo adaptador não reconhece o exemplo devolve 422 `product_not_mapped` com um `productId` estranho, e isso já prova que o aviso chegou e o segredo bateu. Nunca cadastre esse produto de exemplo.

O dono vê o código de cada envio na lista de envios do webhook, no painel do checkout. A mensagem genérica de erro do botão de teste não diz o motivo, a lista diz.

### Passo 5. O agente confere no histórico

```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/integrations/checkout/events?provedor=<provedor>&limit=5"
```

| O que aparece no aviso mais novo | Leitura |
|---|---|
| `isTest: true`, `outcome: "test_mode"` | O aviso chegou e o segredo bateu. Nada foi alterado. Pronto |
| `outcome: "product_not_mapped"` | Chegou e o segredo bateu. Se o aviso tem cara de pedido de exemplo (produto que o dono não reconhece, link de pagamento de exemplo em `includePayload=true`), é o teste do checkout, e está tudo certo. Senão, o id do produto não bate com o cadastro. Compare o `productId` do aviso com o do passo 2 |
| outro `outcome` | O teste veio como venda comum. Leia a tabela de resultados abaixo |
| nada novo na lista | O aviso não passou da porta. Segredo diferente, endereço errado, ou webhook vinculado a outro produto. Ver a tabela de sintomas |

Recusa por segredo errado não entra no histórico: ela é barrada antes do registro. Lista vazia depois do teste aponta para segredo ou endereço. Cada recusa deixa uma linha no registro do app terminada em `webhook recusado`, com o motivo e onde havia candidato a segredo (nunca o segredo):

```bash
docker compose -f <pasta>/docker-compose.yml logs --tail=200 app | grep -i "webhook recusado"
```

Um 401 seguido de 422 na lista de envios do checkout quer dizer que o segredo foi salvo no meio do caminho: o primeiro envio saiu antes e o segundo já bateu.

Só depois disso o agente fala ao dono: `Venda automática ligada no produto X. Quem comprar entra no curso Y e recebe o e-mail de acesso.`

## Cadastrar, listar e apagar produto

### Cadastrar ou mudar (`PUT`)

Campos aceitos, lista fechada. Campo fora dela volta 400.

| Campo | O que é |
|---|---|
| `productId` | Obrigatório. Id do produto no checkout |
| `offerId` | Opcional. Id de uma oferta do produto. Cadastro da oferta vence o cadastro do produto inteiro. Serve para uma oferta liberar cursos diferentes |
| `courseIds` | Lista de `courseId` desta escola, de 1 a 50. Curso que não existe volta 422 `course_not_found` com a lista `missing` |
| `ignore` | `true` para produto que não libera curso nenhum (order bump, e-book). Não vai junto com `courseIds` |
| `note` | Opcional. Texto livre até 500 caracteres. `null` apaga |
| `webhookSecret` | Opcional. Segredo daquele produto. Omitido mantém o atual, `null` ou vazio apaga |

A chave do cadastro é o par produto e oferta. Repetir a chamada com o mesmo par atualiza, não duplica. `created: true` na resposta quer dizer que era novo.

Para trocar os cursos de um produto já cadastrado, mande o `PUT` de novo com a lista completa. A lista nova substitui a antiga.

### Listar (`GET`)

```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/integrations/checkout/products"
```

A resposta traz três partes:

- `data`: cada produto cadastrado, com `mappingId`, `productId`, `offerId`, os cursos (`title`, `published`, `courseExists`), `webhookSecretSet` e `lastEvent`, o último aviso daquele produto.
- `unmappedRecent`: produtos que venderam nos últimos 30 dias e não têm cadastro, com `productId`, quantas vendas e a data da última. **É a lista de quem pagou e ficou de fora.** Cada item aqui vira um `PUT`.
- `webhook`: o caminho do webhook, `providers` (os ids dos adaptadores instalados) e `secretConfigured`. Com `?provedor=<id>` no fim do endereço, o caminho sai pronto para aquele checkout.

Curso com `courseExists: false` foi apagado depois do cadastro: a próxima venda volta 422. Curso com `published: false` matricula e o aluno só vê quando publicar.

### Apagar (`DELETE`)

```bash
curl -s -X DELETE -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/integrations/checkout/products/{{MAPPING_ID}}"
```

Usa o `mappingId` da listagem. Depois de apagar, venda aprovada daquele produto volta a ser recusada com `product_not_mapped`. Apagar exige ordem nomeada do dono, como apagar curso.

## Ler o histórico de avisos

```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/integrations/checkout/events?email={{EMAIL_DO_ALUNO}}&limit=20"
```

Filtros, todos opcionais e combináveis: `provedor`, `email`, `status`, `action`, `outcome`, `orderId`, `productId`, `since` (data ISO, como `2026-09-01`), `limit` (padrão 50, até 200) e `includePayload=true`, que traz o aviso original com os dados pessoais cobertos.

O filtro `email` funciona mesmo o histórico não guardando o endereço: o sistema faz o mesmo resumo do e-mail e compara. O e-mail precisa ser o que o comprador digitou no checkout.

Campos de cada aviso que o agente lê:

| Campo | Leitura |
|---|---|
| `provider` | o id do adaptador que recebeu o aviso |
| `action` | `approve` (compra), `revoke` (reembolso, chargeback), `expire_at_period_end` (cancelamento), `ignore` (evento sem efeito) |
| `status` | `done` terminou bem. `rejected` recusado, o reenvio do checkout tenta de novo. `failed` erro do sistema, o reenvio tenta de novo. `processing` em andamento |
| `outcome` | o que aconteceu, tabela abaixo |
| `warnings` | avisos com `code`, tabela abaixo |
| `productId`, `offerId`, `orderId` | produto, oferta e pedido, como o checkout mandou |
| `courseIds`, `userId` | cursos e aluno afetados |
| `periodEndsAt` | fim do período pago, nos cancelamentos |
| `isTest` | aviso de teste do checkout |
| `rawEvent`, `rawStatus` | o nome do evento e o status como o checkout mandou |

Aviso `rejected` ou `failed` volta a ser processado quando o checkout reenviar. Por isso cadastrar o produto que faltava resolve as vendas que já ficaram vermelhas.

## O que cada resultado quer dizer

| `outcome` | Resposta ao checkout | Leitura |
|---|---|---|
| `enrolled` | 200 | Matriculou e mandou o e-mail |
| `already_active` | 200 | O aluno já tinha acesso. Nada mudou |
| `superseded_by_refund` | 200 | A aprovação chegou depois do reembolso do mesmo pedido. Não matriculou |
| `revoked` | 200 | Acesso tirado, progresso guardado |
| `nothing_to_revoke` | 200 | Reembolso de quem não tinha acesso |
| `kept_other_order` | 200 | Reembolso de um pedido, e outro pedido do mesmo aluno segue pago. Acesso mantido |
| `access_ends_at_set` | 200 | Cancelamento: o acesso vai até `periodEndsAt` |
| `nothing_to_expire` | 200 | Cancelamento de quem não tinha acesso ativo |
| `period_end_unknown` | 200 | Cancelamento sem data do fim do período. Acesso intacto |
| `product_ignored` | 200 | Produto cadastrado com `ignore: true` |
| `ignored_event` | 200 | Evento que não mexe em acesso, como pagamento recusado |
| `test_mode` | 200 | Teste do checkout. Nada alterado |
| `product_not_mapped` | 422 na compra, 200 no resto | Produto sem cadastro. Só a compra aprovada fica vermelha no checkout |
| `missing_email` | 422 | O aviso veio sem e-mail válido do comprador |
| `course_not_found` | 422 | O cadastro aponta para curso que não existe mais |
| `in_progress` | 409 | O mesmo aviso está sendo tratado agora. O reenvio resolve |
| `internal_error` | 500 | Erro do sistema. O reenvio tenta de novo |

| `warnings[].code` | Leitura |
|---|---|
| `course_unpublished` | Matriculou em curso não publicado. O aluno vê quando o dono publicar |
| `progress_restored` | Recompra: o progresso guardado voltou |
| `no_prior_approval` | Reembolso de acesso que não veio desta integração (convite manual ou sistema antigo). Tirou assim mesmo |
| `period_end_unknown` | Cancelamento sem data. Acesso intacto |
| `course_not_found` | O curso do cadastro sumiu |

Respostas do próprio webhook, antes do histórico:

| Código | Leitura |
|---|---|
| 400 `invalid_json` | o corpo não é JSON |
| 401 | segredo não confere. Não entra no histórico |
| 404 `domain_not_found` | o endereço chegou por um domínio que a escola não conhece |
| 404 `unknown_provider` | não há adaptador com esse id. A resposta lista os instalados |
| 413 | corpo maior que 1 MB |
| 503 `secret_not_configured` | nenhum segredo gravado |

## Sintoma, causa, conserto

| Sintoma | Onde olhar | Conserto |
|---|---|---|
| Painel do checkout vermelho com 422 | `GET products`, parte `unmappedRecent` | produto não cadastrado. `PUT products` com o id que aparece ali. O reenvio do checkout matricula |
| Painel do checkout vermelho com 401 | nada no histórico, é o esperado; no registro do app, a linha `webhook recusado` | segredo diferente entre o checkout e a instalação. O dono confere o segredo no webhook do checkout e passa de novo. Grave no `.env` ou no produto e refaça o teste |
| Painel do checkout vermelho com 503 | `GET` no webhook: `secretConfigured: false` | nenhum segredo gravado, ou o `.env` não foi relido. Passo 1 |
| Painel do checkout vermelho com 404 | `GET` no webhook: `unknown_provider` | o id do endereço está errado, ou o checkout não tem adaptador. Corrija o id pela lista `providers`, ou veja [Checkout sem adaptador](#checkout-sem-adaptador) |
| Botão de teste dá erro e a venda de verdade funciona | lista de envios do checkout: 422 com produto estranho | o teste mandou um pedido de exemplo que o adaptador não reconhece. Segredo e endereço estão certos. Nunca cadastre o produto de exemplo |
| Painel do checkout com taxa de sucesso 0% e nenhum aviso no histórico | com o dono: o webhook está vinculado a ESTE produto? | vincular o webhook ao produto no checkout. Passo 3 |
| Aluno pagou e não entrou | `GET events?email=<e-mail da compra>` | ver o `outcome` do aviso. Sem aviso nenhum com esse e-mail: webhook não vinculado ao produto, ou o aluno digitou outro e-mail na compra |
| Aluno entrou e diz que o e-mail não chegou | `outcome` do aviso: `enrolled` ou `already_active` | `already_active` não manda e-mail. Com `enrolled`, é entrega de e-mail, `SOCORRO.md` |
| Aluno reembolsou e ainda assiste | `GET events?email=...&action=revoke` | sem aviso: o checkout não mandou o reembolso ou o webhook não tem esse evento marcado. `kept_other_order`: outro pedido dele segue pago |
| Aluno cancelou a assinatura e perdeu o acesso antes do fim | aviso de cancelamento dele | cancelamento só marca a data. Perda antes da data vem de reembolso ou chargeback, veja se há `revoke` |
| Aviso com `course_not_found` | `GET products`, curso com `courseExists: false` | `PUT products` com o curso certo. O reenvio do checkout matricula |
| Tudo `ignored_event` numa venda que foi paga | `GET events?includePayload=true` do aviso | o adaptador não reconheceu o nome do evento ou do status desse checkout. Leia `rawEvent` e `rawStatus` e ajuste a classificação no adaptador (seção abaixo) |

## Checkout sem adaptador

Quando o checkout do dono não está em `webhook.providers`, a venda automática pede um adaptador novo no código da área de membros. É uma mudança de código com imagem nova: o agente faz com o dono sabendo, na cópia do código-fonte que veio na entrega (`soft-members-source-<versao>.tar.gz`, ver `INSTALAR.md`), e publica pelo caminho de `ATUALIZAR.md`. Se o dono não tem onde compilar a imagem, o trabalho de código vai para a skill `soft-sistema`.

O modelo é o adaptador que já vem na instalação, na pasta `apps/web/lib/checkout/adapters/`. O contrato completo, com o passo a passo, está no comentário do topo de `apps/web/lib/checkout/adapter.ts`. Em resumo:

1. **Pegar um aviso de verdade.** O agente precisa do JSON que o checkout manda: a documentação de webhooks do checkout, ou o corpo que aparece na lista de envios do painel. Um aviso de cada tipo: compra aprovada, reembolso, chargeback, cancelamento de assinatura e o do botão de teste. Tire e-mail e nome reais antes de guardar.
2. **Criar a pasta do adaptador.** `apps/web/lib/checkout/adapters/<id>/index.ts`, copiando o que já vem pronto. O `<id>` é minúsculo, com letras, números e hífen, e nunca muda depois da primeira venda: vai no endereço do webhook, na etiqueta do aluno e no histórico.
3. **Mapear os campos** do aviso para o formato único, pela tabela abaixo. A leitura nunca pode dar erro: corpo que o adaptador não entende sai como `ignore`.

| Campo do formato único | O que o adaptador põe ali |
|---|---|
| `action` | `approve` para compra paga, `revoke` para reembolso e chargeback, `expire_at_period_end` para assinatura cancelada, `ignore` para o resto. Reembolso e chargeback vencem aprovação: há checkout que reenvia o evento de compra com o status já estornado |
| `orderId` | id do pedido. É a chave que impede matrícula em dobro no reenvio |
| `productId`, `offerId` | os ids que o dono cadastra no mapa de produto |
| `email`, `name` | do comprador. E-mail inválido vira vazio |
| `periodEndsAt` | fim do período pago, nos cancelamentos, quando o checkout manda |
| `isTest` | `true` no aviso do botão de teste. Se o teste manda pedido de exemplo, reconheça o exemplo aqui (produto ou link de pagamento de exemplo) |
| `rawEvent`, `rawStatus` | evento e status crus, para o histórico |

4. **Conferir o segredo.** Checkout que manda o segredo puro (num cabeçalho ou no corpo): junte os lugares possíveis e use a comparação pronta de `apps/web/lib/checkout/shared-secret.ts`. Checkout que assina o corpo (HMAC): calcule a assinatura sobre o corpo cru com cada segredo aceito e compare em tempo constante. Se o checkout tem variável de ambiente própria para o segredo, liste em `envSecretNames`; `CHECKOUT_WEBHOOK_SECRET` e o segredo por produto já valem para todo adaptador.
5. **Registrar** o adaptador na lista de `apps/web/lib/checkout/registry.ts`.
6. **Testar com o aviso de exemplo.** Um teste em `apps/web/lib/checkout/adapters/<id>/__tests__/` que chama a leitura com cada JSON do item 1 e confere `action`, `orderId`, `productId`, `email` e `isTest`. Rode `pnpm test -- --testPathPattern checkout` e só siga com tudo verde.
7. **Publicar e provar.** Imagem nova pelo `ATUALIZAR.md`. Depois, `curl -s "https://<dominio>/api/integrations/checkout/<id>/webhook"` responde `ok: true`, e o `<id>` aparece em `webhook.providers`. Daí em diante, os 5 passos de cima, com o botão de teste do checkout como prova final.

O resto (mapa de produto, matrícula, reembolso com progresso guardado, cancelamento até o fim do período, histórico, reenvio sem duplicar) é comum a todo checkout e não se mexe.

## O que perguntar ao dono

Uma pergunta por mensagem, nesta ordem, só o que faltar:

1. `Qual checkout você usa para vender esse produto?` (para achar o `<provedor>` na lista, ou saber que falta adaptador)
2. `Qual o segredo que está no webhook do checkout?` (se ainda não há segredo gravado)
3. `Me manda o link da página desse produto no checkout?` (para tirar o id)
4. `Quem compra esse produto entra em qual curso?`
5. `Já apontou o webhook para a área de membros nesse produto?`
6. `Pode apertar o teste do webhook no checkout e me avisar?`
