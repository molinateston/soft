# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nomes, endereços, identificadores, saídas de comando e resultados
> foram inventados só pra mostrar a FORMA de cada fase. Nenhum endereço daqui abre, nenhum repositório
> existe. Num trabalho real, toda saída colada no pacote de prova vem de comando rodado de verdade, e
> o que não foi rodado sai marcado `[NÃO VERIFICADO]`.

**O caso fictício:** uma empresa de manutenção predial com 6 técnicos atende 40 condomínios. O dono
fictício quer um sistema onde o síndico de cada condomínio entra e vê os chamados do prédio dele, sem
enxergar os outros.

Este arquivo mostra o ciclo inteiro, **incluindo uma revisão que reprovou três vezes seguidas** e o
que a skill fez, mais o **mesmo pedido resolvido num ambiente sem infraestrutura nenhuma**.


## Índice

- Pergunta zero
- Fase 1 · Spec, uma pergunta por vez, e a parada pra aprovação
- Fase 2 · Arquitetura
- Fase 3 · Build, escopos em sequência sem delegação
- Fase 4 · Review, e a reprovação que se repetiu 3 vezes
- Fase 5 · Entrega, o pacote de prova com as saídas coladas
- O mesmo pedido, num ambiente sem infraestrutura nenhuma

---

## PERGUNTA ZERO

> Antes de mais nada: é um sistema do zero, ou uma edição de algo que já existe?
>
> *"Do zero. Hoje é tudo por grupo de mensagem e planilha."*

→ Fase 1.

---

## Fase 1 · SPEC (uma pergunta por vez)

As perguntas, na ordem em que saíram, e as respostas resumidas:

> **1.** Quem abre esse sistema, e o que essa pessoa precisa conseguir fazer?
> *"O síndico. Ele quer ver os chamados do prédio dele e abrir um novo."*

> **2.** Alguém mais entra além do síndico?
> *"Eu e a minha secretária, pra ver tudo e atualizar o status. E o técnico devia poder marcar
> concluído do celular."*

> **3.** Quais são os estados de um chamado, do começo ao fim?
> *"Aberto, agendado, em execução, concluído. E tem os que a gente recusa, quando não é serviço
> nosso."*

> **4.** O síndico pode ver alguma coisa de outro condomínio, em alguma hipótese?
> *"Nunca. Isso é o mais importante. Já teve caso de síndico querer saber quanto o vizinho paga."*

> **5.** Tem restrição de marca, prazo ou integração?
> *"A marca é verde-escuro e cinza, eu te mando o logotipo. Prazo, uns 20 dias. Integração nenhuma
> por enquanto."*

> **6.** Descreve o dia em que isso estiver funcionando: quem abre, o que faz, e o que acontece no fim.
> *"O síndico abre no celular às 7h, vê que o chamado do elevador está agendado pra quinta, e fica
> quieto. Meu telefone para de tocar."*

A pergunta 6 é a que fecha a definição de pronto, e ela veio da narrativa dele, não de um formulário.

### A spec fechada

```markdown
# specs/chamados-manutencao.md

## Objetivo
Síndico de condomínio acompanha e abre chamados do prédio dele, sem enxergar
nenhum dado de outro condomínio.

## Requisitos
1. Login por e-mail e senha, com recuperação
2. Três perfis: síndico (vê só o dele), administração (vê tudo, edita), técnico (marca concluído)
3. Síndico vê a lista de chamados do próprio condomínio, com estado e data
4. Síndico abre chamado novo: título, descrição, urgência, foto opcional
5. Estados do chamado: aberto, agendado, em execução, concluído, recusado
6. Administração muda estado e agenda data
7. Técnico marca concluído pelo celular, com foto do serviço feito
8. Isolamento por condomínio no banco, não só na tela
9. Histórico do chamado: quem mudou o quê e quando
10. Administração vê o painel consolidado de todos os condomínios
11. Foto do chamado guardada e exibida na lista
12. Interface funciona no celular, é onde o síndico usa
13. Marca do cliente: verde-escuro e cinza  [A CONFIRMAR: logotipo, o dono vai mandar]

## Restrições
- 20 dias
- Sem integração externa nesta versão
- Não fazer: orçamento, cobrança, nota fiscal (o dono disse que fica pra depois)

## Definição de pronto
Um síndico entra pelo celular, vê o chamado do elevador agendado pra quinta,
e não consegue, por nenhum caminho, ver dado de outro condomínio.
```

> **PARADA: "pode ir?"**
>
> *"Pode. Só uma coisa: o requisito 10, o painel consolidado, eu quero ver por condomínio também, não
> só o total."*

A observação entrou na spec **antes** do "pode ir" valer, como requisito 10 reescrito. Guarde esta
frase, ela volta na Fase 4.

---

## Fase 2 · ARQUITETURA

```
Contrato dos dados (decidido antes da 1ª linha):
  condominio { id, nome, endereco }
  usuario    { id, email, papel, condominio_id (nulo pra administração) }
  chamado    { id, condominio_id, titulo, descricao, urgencia, estado, criado_em }
  evento     { id, chamado_id, usuario_id, de_estado, para_estado, em }
  foto       { id, chamado_id, caminho, tipo (abertura|conclusao) }

Rotas: GET /chamados · POST /chamados · PATCH /chamados/:id/estado
       GET /painel (só administração)

Rápido x lento:
  criar chamado, mudar estado → responde na hora
  upload e redimensionamento de foto → fila e trabalhador, nunca segura a resposta

Segurança de base:
  isolamento por condomínio na CAMADA DO BANCO, com política por linha.
  Filtro só na consulta da aplicação seria suficiente pra tela, e insuficiente
  pro requisito 8. O requisito diz "não só na tela" de propósito.

Repositório criado ANTES da 1ª linha.
Tokens de cor: verde-escuro e cinza. Logotipo [A CONFIRMAR].
```

---

## Fase 3 · BUILD

Ambiente **sem delegação**, então os escopos rodaram em sequência, na ordem em que um libera o outro:

```
Escopo 1 · banco e políticas de isolamento
  precisa entregar: as 5 tabelas, e a política que impede um usuário de ler
                    linha de condomínio que não é o dele
  conferido contra:  requisitos 8 e 2

Escopo 2 · autenticação e os 3 perfis
  precisa entregar: login, recuperação de senha, e o papel gravado no usuário
  conferido contra:  requisitos 1 e 2

Escopo 3 · telas do síndico (lista e abertura)
  precisa entregar: lista com estado e data, formulário de abertura com foto
  conferido contra:  requisitos 3, 4, 11, 12

Escopo 4 · telas da administração e do técnico
  precisa entregar: mudança de estado, agendamento, conclusão pelo celular
  conferido contra:  requisitos 5, 6, 7, 9

Escopo 5 · painel consolidado
  precisa entregar: total geral E a quebra por condomínio
  conferido contra:  requisito 10
```

As três linhas de nota antes de cada escopo são a mesma informação que iria num prompt delegado. Sem
delegação, elas viram nota escrita; a disciplina não muda.

---

## Fase 4 · REVIEW, e a reprovação que se repetiu 3 vezes

Primeira passada, contra o sistema rodando:

| Req | O que foi conferido | Resultado |
|---|---|---|
| 1 | entrei com e-mail e senha, e recuperei senha de teste | passa |
| 2 | os 3 perfis entram e veem o que devem | passa |
| 3 | lista do síndico mostra 4 chamados, com estado e data | passa |
| 4 | abri chamado com foto, apareceu na lista | passa |
| 5 | os 5 estados existem e transitam | passa |
| 6 | administração mudou estado e agendou | passa |
| 7 | marquei concluído pelo celular, com foto | passa |
| 8 | **consulta direta no banco com o usuário síndico** | passa (ver prova abaixo) |
| 9 | histórico registrou as 3 mudanças que fiz | passa |
| **10** | **painel consolidado** | **não passa** |
| 11 | foto guardada e exibida | passa |
| 12 | testei em tela de 390px, tudo alcançável | passa |

### O requisito 10, tentativa por tentativa

**1ª reprovação.** O painel mostrava o total geral (128 chamados abertos), sem a quebra por
condomínio. Conserto: adicionada a tabela por condomínio abaixo do total. Volta pra revisão.

**2ª reprovação.** Agora tinha a quebra por condomínio, mas contava **todos** os chamados de cada
condomínio, e o dono, ao conferir, disse que não era isso. Aqui a regra do ciclo mandou **parar de
consertar e reler o requisito**:

```
Requisito 10 na spec: "Administração vê o painel consolidado de todos os
condomínios, com a quebra por condomínio."

Leitura A: total de chamados por condomínio (foi o que eu construí)
Leitura B: total de chamados ABERTOS por condomínio
Leitura C: os dois números lado a lado

O requisito admite as três. O problema não é o código.
```

Mesmo assim, a skill tentou a leitura mais provável (B) uma vez. Foi a terceira.

**3ª reprovação.** O dono conferiu e disse que faltava saber quantos estavam atrasados. **O ciclo
parou aqui**, e a skill chamou o dono, em vez de tentar uma quarta:

> O requisito 10 reprovou três vezes. O que eu construí funciona nas três leituras que tentei, e
> nenhuma é a que você confere quando abre o painel. A gente está entendendo "consolidado" de forma
> diferente, e mais uma tentativa minha é chute.
>
> Quando você abre esse painel de manhã, qual é a **primeira pergunta** que você quer responder?
>
> (a) quantos chamados abertos tem em cada prédio
> (b) quais prédios estão com chamado atrasado
> (c) quanto trabalho cada técnico tem pela frente
>
> Os outros 12 requisitos estão passando. Só este segura a entrega.

**Resposta:** *"(b). Eu quero saber onde vai dar problema. O resto eu vejo depois."*

O requisito 10 foi **reescrito na spec** (não remendado no código):

```
10. Administração vê o painel de risco: os condomínios com chamado aberto há mais
    de 5 dias, ordenados do mais atrasado pro menos. O total geral aparece no
    topo, como contexto, não como a informação principal.
```

Reconstruído contra o requisito novo, passou na primeira. Três reprovações consumiram meio dia; uma
quarta tentativa às cegas teria consumido o resto e ainda entregue a coisa errada.

---

## Fase 5 · ENTREGA, o pacote de prova com as saídas coladas

Este é o formato. Repare que cada linha traz a **saída**, não a afirmação.

```markdown
# PROVA · chamados-manutencao · 2026-08-22

## Endereço e repositório
  https://chamados.exemplo-fictício.com.br
  repositório privado: <organização>/chamados-manutencao, commit a3f19c2

## 1. O domínio responde e o certificado está de pé
$ curl -sSI https://chamados.exemplo-fictício.com.br | head -3
HTTP/2 200
server: nginx
content-type: text/html; charset=utf-8

$ echo | openssl s_client -connect chamados.exemplo-fictício.com.br:443 2>/dev/null \
    | openssl x509 -noout -dates
notBefore=Aug 19 00:00:00 2026 GMT
notAfter=Nov 17 23:59:59 2026 GMT

## 2. Entrei de verdade, com credencial de teste
  Usuário: sindico.teste@exemplo-fictício.com.br (perfil síndico, Condomínio Alfa)
  Captura: prova/01-login.png
  Captura: prova/02-lista-chamados.png  (4 chamados, todos do Alfa)

## 3. O isolamento existe NO BANCO, não só na tela
   O teste que importa: consultar direto, como o usuário síndico, pedindo tudo.

$ psql "$URL_COMO_SINDICO" -c "select condominio_id, count(*) from chamado group by 1"
 condominio_id | count
---------------+-------
             7 |     4
(1 row)

   O banco tem 312 chamados de 40 condomínios. Este usuário enxerga 4, de 1.
   A consulta não tinha filtro: quem filtrou foi a política do banco.

$ psql "$URL_COMO_SINDICO" -c "select count(*) from chamado where condominio_id = 12"
 count
-------
     0
(1 row)

   Pedi explicitamente o dado de outro condomínio. Voltou vazio, não erro:
   a linha simplesmente não existe para este usuário.

## 4. O dado que a tela mostra existe mesmo na tabela
$ psql "$URL_ADMIN" -c "select id, titulo, estado from chamado where condominio_id = 7"
 id  |          titulo           |   estado
-----+---------------------------+------------
 118 | Elevador social parado    | agendado
 121 | Infiltração garagem       | em execução
 126 | Lâmpada hall 3o andar     | aberto
 129 | Portão eletrônico         | concluído
(4 rows)

   Bate linha a linha com prova/02-lista-chamados.png.

## 5. O requisito 10, reescrito, conferido
  Captura: prova/03-painel-risco.png
  Mostra 6 condomínios com chamado aberto há mais de 5 dias, o mais antigo
  no topo (14 dias). Total geral no rodapé, como contexto.

## 6. Celular
  Captura: prova/04-celular-390px.png
  Testado em 390px de largura. Botão de abrir chamado alcançável com o polegar.

## O que NÃO foi verificado
  [NÃO VERIFICADO] Comportamento com mais de 500 chamados por condomínio.
  O maior hoje tem 31. Não simulei volume.
  [A CONFIRMAR] O logotipo ainda não chegou. A marca está aplicada em cor,
  e o espaço do logotipo está reservado no cabeçalho.
```

Repare no item 3: a prova do isolamento não é "eu implementei a política". É a consulta rodada **como
o usuário restrito**, pedindo o que ele não pode ver, e voltando vazio. Prova é o que alguém hostil
não consegue derrubar.

---

## O MESMO pedido, num ambiente sem infraestrutura nenhuma

Sem shell, sem repositório, sem hospedagem. A skill **não fingiu** e **não baixou a qualidade**. Rodou
a pergunta zero e a Fase 1 igual, e entregou este documento consolidado:

```markdown
# Sistema de chamados de manutenção · spec, arquitetura e plano de construção

> Este documento é a entrega completa do que dá pra fazer neste ambiente. Ele não
> foi construído nem publicado, porque aqui não tenho repositório, servidor nem
> banco. O que está aqui é o suficiente pra qualquer pessoa técnica construir sem
> voltar pra perguntar.

## 1. Objetivo
Síndico de condomínio acompanha e abre chamados do prédio dele, sem enxergar
nenhum dado de outro condomínio.

## 2. Requisitos
[os 13 requisitos, iguais aos da spec acima, numerados]

## 3. Definição de pronto
Um síndico entra pelo celular, vê o chamado do elevador agendado pra quinta, e
não consegue, por nenhum caminho, ver dado de outro condomínio.

## 4. Arquitetura
### 4.1 Contrato dos dados
[as 5 tabelas com seus campos, como na Fase 2 acima]

### 4.2 Rotas
GET /chamados · POST /chamados · PATCH /chamados/:id/estado · GET /painel

### 4.3 O que é rápido e o que é lento
Criar chamado e mudar estado respondem na hora.
Upload e redimensionamento de foto vão pra fila com trabalhador separado.

### 4.4 A decisão que não pode ser negociada na hora da pressa
O isolamento por condomínio fica na CAMADA DO BANCO, com política por linha,
não no filtro da consulta da aplicação. Filtro na aplicação atende a tela e
falha no requisito 8: basta uma rota nova esquecer o filtro pra vazar. A
política por linha vale mesmo pra código que ainda não existe.

## 5. Plano de construção, na ordem em que um escopo libera o outro
1. Banco e políticas de isolamento (requisitos 8, 2)
2. Autenticação e os 3 perfis (1, 2)
3. Telas do síndico (3, 4, 11, 12)
4. Telas de administração e técnico (5, 6, 7, 9)
5. Painel de risco (10)

## 6. Plano visual
Marca: verde-escuro e cinza. Logotipo [A CONFIRMAR].
Sem degradê decorativo, sem emoji na interface, ícone é desenho de linha.
Componentes: cabeçalho de 2 colunas, número grande com rótulo pra cada estado,
lista com etiqueta de urgência, acordeão pro histórico do chamado.
Dois temas, claro e escuro, aplicados antes do primeiro desenho da tela.
Entrada por tela de login de 2 colunas.

## 7. Como se prova que ficou pronto, quando alguém construir
- entrar de verdade com um usuário síndico
- consultar o banco COMO esse usuário, pedindo dado de outro condomínio,
  e receber vazio
- comparar a lista da tela linha a linha com a tabela
- abrir em 390px de largura

## 8. O que a infraestrutura somaria
Com repositório, hospedagem e banco, eu levaria isto até o ar e entregaria o
endereço mais o pacote de prova do item 7 preenchido, com as saídas coladas.
Sem eles, este documento é a entrega, e ela é completa até onde pode ir.
```

A última seção é obrigatória: ela separa o que foi feito do que ficou fora, sem transformar a falta de
ferramenta em desculpa e sem fingir que o sistema existe.
