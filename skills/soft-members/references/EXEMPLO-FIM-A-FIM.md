# Exemplo fim a fim: do "quero área de membros" ao aluno assistindo

Uma conversa inteira, com um dono fictício de nicho neutro. O que o dono escreveu está em citação. O que o agente fez por baixo está em lista. O que o agente respondeu está em bloco.

O dono deste exemplo é confeiteira, vende um curso de bolo de casamento, e nunca abriu um painel na vida.

O exemplo começa no zero absoluto: nenhum endereço guardado, nenhuma chave, nada instalado. O passo da conexão é o que mais quebra na primeira vez, então ele aparece aqui inteiro, com a falha e tudo, em vez de já vir resolvido.

## Dia 1, 9h12

> quero botar meu curso num lugar que os alunos entrem com senha

O agente procura `MEMBERS_URL` e `MEMBERS_API_KEY` no `.env` do projeto da dona. Os dois estão vazios. **Ele não chama nada ainda**, porque chamar sem chave só produz 401 e uma frase errada pro dono.

Primeiro separa os dois casos possíveis, em uma pergunta:

```
Antes de começar: você já tem uma área de membros no ar em algum endereço seu,
ou a gente vai montar do zero?
```

> não tenho nada, sou eu e o Instagram

Montar a instalação numa VPS é serviço de quem cuida de máquina, e o caminho está em `references/INSTALAR.md`. Nesta história quem cuida da VPS da Rita sobe a área de membros à tarde e devolve o endereço.

## Dia 1, 16h30

O agente tem o endereço. Grava em `MEMBERS_URL` e roda a primeira chamada do teste de leitura de `setup-conexao.md`:

```
lista de cursos: 401
```

**401 com o endereço certo significa chave ausente ou inválida.** O agente para aqui e resolve a chave pelo caminho de `setup-conexao.md`, que é quem manda nesse passo. Ele não improvisa, não tenta outra rota e não diz à dona que já está operando.

Com a chave guardada, repete o teste de leitura. As duas chamadas obrigatórias voltam 200, e a listagem vem vazia: a escola existe e não tem nada dentro.

Só agora ele fala com a dona, e faz uma pergunta só.

```
Sua escola está no ar, vazia, esperando o conteúdo.
Qual o seu nome completo? É o nome que assina a escola.
```

> Rita Camargo

Por baixo, sem comentar:

- grava o nome do dono, para a publicação não falhar depois.

```
Pronto. Que nome você quer dar pro curso?
```

> Bolo de Casamento do Zero

Por baixo:

- cria o curso e guarda o identificador;
- cria o plano de acesso gratuito, que o dono nunca vê;
- confere que a escola responde por fora.

```
Curso "Bolo de Casamento do Zero" criado, ainda fechado.
Me manda o primeiro vídeo que eu monto a primeira aula.
```

## Dia 1, 17h05

> como eu chamo as partes? aqui eu penso em semana 1, semana 2

```
Então vai ser Semana 1, Semana 2 e por aí. Quantas semanas tem?
```

> 4

Por baixo: cria quatro seções e guarda os quatro identificadores no mapa da instância.

```
Quatro semanas criadas. Manda os vídeos que eu vou pondo no lugar certo.
```

## Dia 1, 17h20

> segue o link do primeiro, é o da massa base, vai na semana 1

O dono cola um endereço de YouTube.

Por baixo:

- cria a aula com tipo de incorporação, não de vídeo, porque link externo não é arquivo;
- amarra a aula à seção da Semana 1, pelo identificador guardado;
- deixa publicada e fechada para quem não é aluno.

```
Aula "Massa base" no ar, dentro da Semana 1.
Próximo?
```

Dez vídeos depois, mesma dança. O dono nunca soube que existe identificador, tipo de aula ou plano.

## Dia 2, 15h20

> tá pronto, quero liberar pra Jussara

Por baixo, antes de convidar:

- confere que o curso está publicado. Não está;
- publica. Passa, porque nome do dono e plano já existem desde ontem;
- convida a aluna por e-mail.

```
Curso publicado e a Jussara liberada. Ela vai receber um e-mail pra criar a senha dela.
Se não chegar em dez minutos, me avisa.
```

## Dia 2, 15h44

> ela diz que não chegou nada

Por baixo:

- procura o e-mail na lista de alunos do curso. Aparece, com acesso ativo;
- conclui: o convite não reenvia e-mail para quem já tem acesso.

```
Achei o problema. O acesso dela já está valendo, e por isso o sistema não manda o e-mail de novo.
O caminho é ela entrar no endereço da escola com /login no fim, clicar em esqueci a senha e usar o e-mail dela.
O link chega na hora. Quer que eu escreva essa mensagem pra você mandar pra ela?
```

> pode ser

O agente escreve a mensagem, em bloco, pronta pra copiar. Não diz "reenviei".

## Dia 5, 11h00

> quanto a Jussara já assistiu?

Por baixo: lê o progresso dela naquele curso.

```
Ela assistiu 3 das 11 aulas, a última anteontem.
```

## Dia 9, 8h30

> quero pôr minha logo e mudar a cor pro meu rosa

Antes de responder, o agente confere o armazenamento de imagem com o POST de assinatura de `personalizar.md`. Volta 500: não está configurado naquela instalação. Se ele tivesse usado GET, viria 405, que é erro dele e não prova nada.

```
Duas coisas, e vou ser direto.
A cor e o nome da escola eu não mexo daqui, só dá por dentro do painel, que é em inglês. Te passo o caminho em três linhas se quiser.
A logo eu não consigo nem por lá: sua instalação está sem a parte que guarda imagem, e quem instalou consegue ligar isso.
O que eu faço agora e muda bastante: deixo uma aula aberta de amostra e escrevo a abertura do curso com as suas palavras. Quer?
```

> quero

O agente escreve a descrição do curso na voz dela, abre a aula da massa base para quem não é aluno, e devolve o link.

## O que este exemplo mostra

1. O dono respondeu sete perguntas em nove dias, todas em linguagem de gente.
2. O agente nunca mostrou identificador, código de erro nem nome de campo.
3. Os passos escondidos, nome do dono e plano de acesso, aconteceram sem virar assunto.
4. Nos dois pontos onde o sistema não entrega, o agente disse a verdade na hora e ofereceu o que dava.
5. Nenhuma frase do agente afirmou algo que ele não tivesse conferido na resposta da chamada.
6. O passo da conexão aconteceu na frente de todo mundo, com um 401 no meio, e a dona não precisou entender nada dele.
