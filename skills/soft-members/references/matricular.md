# Matricular, listar, acompanhar

Dar acesso é a ação mais pedida e a que mais decepciona quando falha em silêncio. Esta reference tem as chamadas, os dois buracos conhecidos e a frase honesta pra cada um.

## Índice

- [Dar acesso por e-mail](#dar-acesso-por-e-mail)
- [Listar os alunos de um curso](#listar-os-alunos-de-um-curso)
- [Ver o progresso de um aluno](#ver-o-progresso-de-um-aluno)
- [Tirar o acesso: não dá hoje](#tirar-o-acesso-nao-da-hoje)
- [Reenviar o acesso: responde sucesso sem enviar](#reenviar-o-acesso-responde-sucesso-sem-enviar)
- [Quando o aluno digitou o e-mail errado](#quando-o-aluno-digitou-o-e-mail-errado)
- [O que perguntar ao dono](#o-que-perguntar-ao-dono)

## Dar acesso por e-mail

```bash
curl -s -X POST "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/customers/invitations" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"email":"{{EMAIL_DO_ALUNO}}","tags":["turma-1"]}'
```

Aceita só `email` e `tags`. O `tags` é opcional e serve pra separar turma, origem ou lote.

**O curso precisa estar publicado.** Convidar para curso fechado devolve `Cannot invite customers to an unpublished product` em 422. Se cair aqui, publique primeiro, com `criar-curso.md`, e repita.

O que acontece por dentro, e vale saber porque muda o que o aluno recebe:

- **Aluno que nunca existiu naquela escola** recebe um e-mail pra criar a senha dele.
- **Aluno que já existia** recebe um e-mail avisando do curso novo, com o endereço de entrada.
- **Aluno que já tem acesso ativo àquele curso** não recebe nada. A rota responde 201 assim mesmo. Leia o bloco de reenvio.

Resposta 201 traz o cliente com `userId` e o estado do acesso. Guarde o `userId`: é por ele que o progresso é consultado.

## Listar os alunos de um curso

```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/customers?page=1&limit=50"
```

Parâmetros: `page` começa em 1, `limit` vai até 200, `search` filtra por texto.

Cada aluno da lista traz e-mail, nome, estado do acesso e `completedLessons`, que é a lista de aulas concluídas. É daí que sai a resposta pro dono quando ele pergunta "quem já assistiu".

Achar um aluno pelo e-mail:

```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/customers?search={{EMAIL}}&limit=5"
```

## Ver o progresso de um aluno

```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/customers/{{USER_ID}}/progress"
```

Devolve as aulas concluídas e as datas. 404 aqui significa que aquele aluno não tem acesso àquele curso, e é a forma mais rápida de conferir se a matrícula pegou mesmo.

Para o dono, traduza em fração: `A Maria assistiu 4 das 12 aulas.` Nunca devolva a lista de identificadores.

## Tirar o acesso: não dá hoje

**Buraco conhecido, sem contorno por API.** Não existe rota pra remover o acesso de um aluno. Não existe pela camada de navegador também: o botão de remover aluno está desligado no painel. O acesso só desaparece quando o curso inteiro é apagado, o que atinge todo mundo.

A frase honesta pro dono, sem rodeio:

> Hoje eu não consigo tirar o acesso de um aluno sozinho, e nem pelo painel dá. O acesso dele continua valendo. O que eu consigo fazer agora é marcar ele com uma etiqueta de cancelado, pra você ter a lista certa, e a gente resolve o acesso quando essa função existir. Quer que eu marque?

A etiqueta entra pelo mesmo convite, com `tags`, e serve só de registro. Ela não fecha porta nenhuma, e o agente diz isso.

Pendência para quem constrói o sistema: uma rota de remoção que mude o estado do acesso do aluno para recusado ou vencido. Enquanto ela não existir, aluno que pediu reembolso continua dentro.

## Reenviar o acesso: responde sucesso sem enviar

**Buraco conhecido, com contorno.** Quando o aluno já tem acesso ativo, a rota de convite devolve 201 com os dados do cliente e **não dispara e-mail nenhum**. Do lado de fora parece que reenviou.

Regra do agente: **nunca diga "reenviei" depois de um convite a aluno que já tinha acesso.** Confira antes. Se o aluno aparecer na lista de alunos daquele curso, o convite não vai enviar nada.

O contorno honesto, que funciona hoje:

> O acesso dele já está valendo, então o sistema não manda o e-mail de novo. O caminho é ele entrar em ENDEREÇO/login, clicar em esqueci a senha e usar o e-mail EMAIL. O link chega na hora. Quer que eu escreva essa mensagem pra você mandar pra ele?

Pendência para quem constrói o sistema: uma rota de reenvio de acesso, ou um parâmetro que force o envio mesmo com acesso ativo.

## Quando o aluno digitou o e-mail errado

Acontece toda semana. O dono matriculou `maria@` e o aluno usa `mariaa@`.

O agente faz, nesta ordem:

1. Procura o e-mail que o dono passou na lista de alunos do curso. Se não achar, o convite nunca existiu e é só convidar de novo com o e-mail certo.
2. Se achar o e-mail errado matriculado, convida o e-mail certo. O aluno certo passa a ter acesso.
3. O e-mail errado continua matriculado, porque remover não dá hoje. O agente **avisa o dono disso**, em uma linha: `Liberei o e-mail certo. O errado continua na lista, porque ainda não consigo remover ninguém.`

Nunca esconda o passo 3. Uma lista de alunos com nomes fantasmas atrapalha o dono na hora de contar quantos pagaram.

## O que perguntar ao dono

| Falta saber | Pergunta |
|---|---|
| O e-mail do aluno | `Qual o e-mail que ele usa? Tem que ser o mesmo onde ele recebe as coisas.` |
| Em qual curso | `Ele entra em qual curso? Você tem: X e Y.` |
| Se é turma | `É um aluno só, ou uma lista? Se for lista, me manda um e-mail por linha.` |
| Confirmação de lote | `São N e-mails. Libero todos agora?` |

Lista inteira de uma vez é ordem nomeada. O agente mostra quantos são e espera o dono confirmar antes da primeira chamada.

## O que dizer quando terminar

```
Pronto. FULANO já tem acesso ao curso NOME e recebeu o e-mail pra criar a senha.
Se não chegar em 10 minutos, me avisa que eu vejo o caminho alternativo.
```

Se o e-mail não podia ser enviado, por qualquer um dos motivos acima, a segunda linha muda e diz a verdade.
