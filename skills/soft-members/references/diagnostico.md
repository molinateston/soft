# Diagnóstico por sintoma: o agente confere antes de responder

Este é o socorro do lado do agente, o que se resolve por chamada de API. O socorro do lado da máquina, que exige acesso à VPS (registros do programa, porta, certificado, envio de e-mail), mora em `SOCORRO.md`, na mesma pasta. Dois arquivos, dois leitores: aqui quem lê é o agente do dono, lá quem lê é quem cuida da instalação.

O dono nunca chega dizendo o que quebrou. Ele diz "o aluno não entra" ou "o vídeo não aparece". Esta reference é a ordem de diagnóstico por sintoma, com a chamada que prova cada hipótese e a frase de volta.

Regra dura: **o agente confere antes de responder.** Palpite dito com confiança é o que faz o dono perder a manhã.

## Índice

- [Primeira coisa, sempre: a escola está no ar?](#primeira-coisa-sempre-a-escola-esta-no-ar)
- [O aluno não recebeu o e-mail](#o-aluno-nao-recebeu-o-e-mail)
- [O aluno não consegue entrar](#o-aluno-nao-consegue-entrar)
- [O vídeo não aparece](#o-video-nao-aparece)
- [A página está fora do ar](#a-pagina-esta-fora-do-ar)
- [A chave parou de funcionar](#a-chave-parou-de-funcionar)
- [Pendências que o agente declara em vez de contornar](#pendencias-que-o-agente-declara-em-vez-de-contornar)

## Primeira coisa, sempre: a escola está no ar?

Duas chamadas, dez segundos, antes de qualquer diagnóstico fino.

```bash
curl -s -o /dev/null -w "pagina %{http_code}\n" "{{MEMBERS_URL}}/"
curl -s -o /dev/null -w "api %{http_code}\n" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" "{{MEMBERS_URL}}/api/products?limit=1"
```

| Resultado | Significa | Vá para |
|---|---|---|
| página 200, api 200 | A escola está inteira. O problema é de um aluno só | O sintoma específico, abaixo |
| página 200, api 401 | A escola funciona, a chave do agente morreu | "A chave parou de funcionar" |
| página 502, 503, ou sem resposta | A instalação caiu | "A página está fora do ar" |
| página 200, api 404 domínio | O endereço guardado não bate com o da escola | `setup-conexao.md` |

## O aluno não recebeu o e-mail

Três causas, e a ordem de conferir importa porque a primeira é a mais comum e a mais chata.

**Passo 1. O aluno já tinha acesso?**

```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/customers?search={{EMAIL}}&limit=5"
```

Se o e-mail aparecer na lista com acesso ativo, **o e-mail não foi enviado e não vai ser**. A rota de convite responde sucesso e não dispara nada para quem já está dentro. É defeito conhecido, está em `matricular.md`. A saída é a recuperação de senha, e a frase está lá.

**Passo 2. O e-mail que o dono passou está certo?**

Confira letra por letra com o dono, em voz de gente: `O e-mail que eu liberei foi ESTE. É esse mesmo que ele usa?`

**Passo 3. O envio da escola está funcionando?**

Isto não se vê por API. Quem tem acesso à máquina da instalação confere os registros do programa e as variáveis de envio. O caminho está em `SOCORRO.md`, bloco `E-mail não chega`. O que o agente diz ao dono nesse meio tempo:

> O convite saiu do meu lado. Se não chegou nem no spam, o problema é no envio da escola, e eu preciso de quem cuida da máquina pra olhar. Enquanto isso, ele entra por ENDEREÇO/login, clica em esqueci a senha e recebe o acesso por lá.

## O aluno não consegue entrar

Pergunte qual das quatro frases é a dele. Cada uma tem conserto diferente, e perguntar economiza meia hora.

| O aluno diz | Causa | O que o agente faz |
|---|---|---|
| `não recebi nada` | Envio, ou acesso já ativo | Bloco de cima |
| `cliquei no link e deu erro` | O link de criar senha tem validade curta | Manda ele usar esqueci a senha na tela de entrada |
| `minha senha não funciona` | Senha errada, ou conta sem senha criada | Mesma coisa: esqueci a senha resolve os dois |
| `entro e não vejo o curso` | A matrícula não existe naquele curso | Confere o progresso dele. 404 confirma. Convida de novo |

A conferência de matrícula:

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/customers/{{USER_ID}}/progress"
```

200 significa matriculado. 404 significa que não tem acesso àquele curso, e o convite precisa ser refeito.

Aluno sem matrícula ver a mensagem de conteúdo fechado é o comportamento certo, não é defeito.

## O vídeo não aparece

Quase sempre é uma das três, nesta ordem de frequência.

**1. A aula nasceu com o tipo errado.** Link de YouTube posto como tipo de vídeo cria uma aula que não toca. Confira o tipo:

```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/lessons/{{LESSON_ID}}"
```

Se o tipo vier como vídeo e o conteúdo for um endereço externo, a aula precisa nascer de novo como incorporação. **O tipo não muda por atualização.** Apagar e recriar é ordem nomeada: `Apaga a aula NOME e faz de novo?`

**2. A aula não está publicada.** Aula com publicação desligada não aparece pro aluno, mesmo em curso publicado. Conserto:

```bash
curl -s -X PATCH "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/lessons/{{LESSON_ID}}" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"published":true}'
```

**3. O link do vídeo está restrito na origem.** Vídeo marcado como privado no site de origem não toca dentro de página nenhuma. Pergunte ao dono: `Esse vídeo está como não listado ou público lá no YouTube? Privado não toca aqui.`

## A página está fora do ar

O agente confere e relata, e só mexe na máquina se a máquina for do escopo dele.

```bash
curl -s -o /dev/null -w "%{http_code} em %{time_total}s\n" "{{MEMBERS_URL}}/"
```

| O que volta | Causa provável |
|---|---|
| Sem resposta, tempo esgotado | A máquina caiu, ou o nome do site não aponta mais pra ela |
| 502 ou 503 | O programa da escola parou, a camada da frente continua de pé |
| 404 em tudo | A configuração do site perdeu o domínio |
| Erro de certificado | O certificado venceu ou não foi emitido |

O caminho de conserto na máquina está em `SOCORRO.md`, blocos `Tabela rápida` e `O endereço não abre`. A frase pro dono, imediata, sem enfeite:

> Sua área de membros está fora do ar agora. Seus alunos não conseguem entrar. Já estou olhando e volto aqui com o que achei.

Nunca deixe o dono descobrir isso por um aluno.

## A chave parou de funcionar

Sintoma: tudo que o agente tenta volta 401, inclusive leitura.

Causa quase sempre: a chave foi apagada, a escola foi reinstalada ou o agente está lendo o arquivo de outra instalação.

Quem opera a VPS roda `gerar_chave_api.sh --nome agente-leon --rotacionar`. O script guarda a nova chave em `chave-agente-leon.env` com modo `600`. Atualize o segredo do agente sem mostrar o valor no chat e rode o teste de leitura de `setup-conexao.md` antes de voltar a operar.

## Pendências que o agente declara em vez de contornar

Três. Nenhuma tem truque, e inventar um é pior que a falta.

| Pendência | O que o dono sente | O que o agente diz |
|---|---|---|
| Não dá pra tirar acesso de aluno | Quem cancelou continua dentro | `Ainda não consigo tirar acesso de ninguém, nem pelo painel. Marco ele como cancelado na lista?` |
| Reenvio de acesso responde sucesso sem enviar | O aluno jura que não recebeu | `O acesso dele já vale, então o sistema não reenvia. Ele recupera a senha na tela de entrada.` |
| Nome, subtítulo e cor da escola sem caminho por API | A escola fica com cara padrão | `Isso eu não mexo daqui. Só pelo painel, e eu te passo o caminho em três linhas.` |

O armazenamento local já recebe logo, capa e imagens. Se um envio falhar, use os códigos de `personalizar.md`: tamanho, formato, permissão, chave ou volume. O agente do dono não inventa contorno para as três pendências da tabela: declara, oferece o caminho disponível e segue.
