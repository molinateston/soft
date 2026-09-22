# Montar a escola: o primeiro uso

O que o agente faz na primeira conversa, antes de existir curso nenhum. São passos que o dono não pede e não vê, e sem eles a publicação do primeiro curso falha com um 422 que o dono não sabe consertar sozinho.

## O que perguntar ao dono

Uma pergunta por vez, nesta ordem. Pare assim que tiver a resposta e siga.

1. `Qual o seu nome completo? É o nome que vai assinar a escola.`
2. `Que nome você quer dar pro primeiro curso?`

Só isso. Nome da escola, cores e logo ficam pra depois, e o caminho deles está em `personalizar.md`.

## Passo 1: gravar o nome do dono

Sem nome gravado no usuário do dono, publicar qualquer curso devolve 422 com `Preencha seu nome no perfil antes de publicar`. Em instalação anterior à atualização de 21/09 a mesma falha volta como `Complete your profile to perform this action`. É o erro mais comum do primeiro dia e o mais difícil de adivinhar.

```bash
curl -s -X PATCH "{{MEMBERS_URL}}/api/user" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"email":"{{EMAIL_DO_DONO}}","name":"{{NOME_DO_DONO}}"}'
```

Campos aceitos: `email`, `name`, `permissions`, `subscribedToUpdates`.

**Nunca mande `permissions` junto com o e-mail do dono.** A rota responde 403 quando o e-mail do corpo é o do dono da escola e o campo `permissions` aparece, mesmo que o valor esteja certo. Mande só `email` e `name`.

O `{{EMAIL_DO_DONO}}` é o mesmo e-mail que administra a escola. Se o agente não souber qual é, pergunte: `Com qual e-mail você entra na sua área de membros?`

Resposta esperada: 200 com o usuário. Se vier 404, o e-mail informado não existe naquela instalação, e a pergunta ao dono se repete.

## Passo 2: criar o primeiro curso

```bash
curl -s -X POST "{{MEMBERS_URL}}/api/products" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"title":"{{TITULO}}","type":"course"}'
```

Aceita só `title` e `type`. Qualquer outro campo volta 400 com o nome do campo recusado. A resposta traz `productId`: guarde esse valor no placeholder interno `COURSE_ID`, usado em toda chamada daqui pra frente.

Valores de `type`: `course` para curso com aulas, `download` para entrega de arquivo único.

## Passo 3: criar o plano gratuito

Passo escondido. O dono nunca pede isso e nunca vê. Sem pelo menos um plano, publicar devolve 422 com `Crie um plano para o curso antes de publicar (pode ser gratuito)`. Em instalação anterior à atualização de 21/09 a mesma falha volta como `Add a payment plan before performing this action`. O agente se guia pelo 422 no momento de publicar, não pelo texto.

```bash
curl -s -X POST "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/payment-plans" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"name":"Acesso","type":"free"}'
```

O primeiro plano criado vira o plano padrão do curso sozinho. Não precisa de chamada extra pra marcar padrão.

Campos aceitos: `name`, `type`, `oneTimeAmount`, `emiAmount`, `emiTotalInstallments`, `subscriptionMonthlyAmount`, `subscriptionYearlyAmount`, `description`.

Valores de `type`: `free`, `onetime`, `emi`, `subscription`. Para área de membros que o dono libera na mão, é sempre `free`: a cobrança acontece fora, e aqui só existe o acesso.

Guarde o `planId` da resposta na nota da instância.

## Passo 4: conferir que a escola responde por fora

Antes de dizer ao dono que está pronto, o agente abre o endereço público e confere que volta página:

```bash
curl -s -o /dev/null -w "%{http_code}\n" "{{MEMBERS_URL}}/"
```

200 significa escola no ar. Qualquer outra coisa vai pra `diagnostico.md`.

## O que dizer ao dono quando terminar

```
Sua escola está no ar e o curso "NOME" já existe lá dentro, ainda fechado.
Me manda o primeiro vídeo que eu ponho a aula.
```

Não liste os passos escondidos. Eles não são notícia pro dono, são trabalho do agente.

## O que dizer quando der errado

| O que aconteceu | Frase pro dono |
|---|---|
| 403 no passo 1 | `Não consegui gravar seu nome na escola. Você consegue confirmar qual e-mail administra ela?` |
| 400 no passo 2 | `O nome do curso não passou. Me manda de novo, sem símbolo estranho?` |
| 422 no passo 3 | `O curso foi criado, mas o plano de acesso não. Vou tentar de novo agora.` |
| Sem resposta em qualquer passo | `Sua área de membros não respondeu agora. Vou conferir se ela está no ar.` |

Nunca invente que deu certo. Um curso criado sem plano parece pronto e falha só na hora de publicar, dias depois, quando o dono já contou pros alunos.

## Ordem que não pode ser invertida

Nome do dono, curso, plano. Depois vêm seções e aulas, em `criar-curso.md`. Publicar só quando os três primeiros existirem. Matricular só depois de publicar.
