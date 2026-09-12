# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Empresa, nome, números e falas foram inventados só pra mostrar a
> FORMA da saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega de verdade. Num
> trabalho real, toda afirmação sobre a conta nasce com a fonte anotada, e o que não foi confirmado sai
> da mensagem ou vira pergunta.

**O caso fictício:** o dono vende um serviço de tradução técnica de manual de equipamento industrial,
do inglês pro português, com revisão por engenheiro. Ticket médio de 9 mil reais por manual. Ele nunca
prospectou: os clientes sempre vieram por indicação, e as indicações pararam.

Este arquivo mostra a saída resumida das 4 ações, na ordem. A saída real é maior; aqui está o
suficiente pra você reconhecer o formato.

---

## O que o dono deu de entrada

> "Eu quero atender importadora de máquina industrial. Já traduzi manual pra três delas e foi ótimo,
> mas as indicações secaram. Tenho uma planilha com 60 empresas que eu peguei de uma lista de
> associação e não sei por onde começar."

**O que faltava:** o recorte nunca tinha sido escrito, a capacidade de atendimento não estava
declarada, e a planilha de 60 nomes não tinha nenhuma pesquisa individual.

## As perguntas que a skill fez (uma por vez)

1. "Descreve o cliente que você mais gostou de atender." → *"Uma importadora de máquina de embalagem, média, que trouxe uma linha nova da Itália e precisava do manual em português pra treinar operador."*
2. "O que os três bons tinham em comum?" → *"Todos tinham acabado de trazer equipamento novo. E todos tinham problema com operador que não entendia o manual em inglês."*
3. "Quantas conversas por semana você atende de verdade?" → *"Três, no máximo. Eu mesmo faço a tradução."*
4. "Quais empresas você já quis atender e nunca abordou?" → *"Umas quatro que eu vi em feira do setor."*

**Premissa declarada em 1 linha:** o sinal de momento é a chegada de equipamento novo, então a lista A
sai só de empresas com evidência pública de importação ou linha nova nos últimos 90 dias, e as outras
esperam.

---

## Ação 1 · A LISTA

Saída real: `lista-prospeccao.md`. Resumo:

**O recorte, em uma frase:** importadora ou indústria de médio porte que trouxe equipamento de linha
nova nos últimos 90 dias, com operação própria de produção e operador que precisa de manual em
português.

**O tamanho:** o dono atende 3 conversas por semana. Com taxa de resposta de 10% e metade delas virando
conversa, uma lista A de 24 contas por mês já enche a agenda. Das 60 da planilha, 9 entraram em A.

| Prioridade | Conta | Pessoa e cargo | Por que entra no recorte | Sinal de momento | Canal |
|---|---|---|---|---|---|
| **A** | [importadora fictícia 1] | [nome], gerente industrial | importa linha de embalagem, produção própria | anunciou nova linha italiana há 6 semanas, fonte: site da empresa | e-mail encontrado no site |
| **A** | [importadora fictícia 2] | [nome], diretor de operações | importa máquina de corte | 3 vagas abertas de operador de máquina, fonte: página de carreiras | rede profissional |
| **A** | [indústria fictícia 3] | [nome], gerente de produção | fábrica com linha importada | nota na imprensa do setor sobre expansão, fonte: revista do setor | rede profissional |
| **B** | [importadora fictícia 4] | [nome], sócio | recorte cheio | nenhum sinal encontrado | e-mail |
| **C** | [empresa fictícia 5] | não identificada | só distribui, não opera | nenhum | nenhum |

**A decisão declarada:** as 9 contas A recebem pesquisa individual e mensagem escrita uma a uma. As de
B esperam o fim de A. As de C saem da planilha até um sinal aparecer.

**STOP.** A skill mostrou a lista e perguntou "começo a pesquisa pela primeira?".

---

## Ação 2 · A PESQUISA E O MOTIVO (conta 1)

Saída real: a seção de pesquisa de `abordagem-importadora-1.md`. Resumo:

```
## Pesquisa

**Quem é:** [nome], gerente industrial na [importadora fictícia 1]
**O que a empresa faz:** importa e instala linhas de embalagem pra indústria de alimentos, e faz a
manutenção depois.
**O que foi encontrado:**
- anunciou uma linha italiana nova há 6 semanas · fonte: página de notícias do site
- abriu 2 vagas de técnico de instalação no mesmo período · fonte: página de carreiras
- o gerente publicou um texto curto sobre o tempo de treinamento de operador · fonte: perfil dele na
  rede profissional
**O motivo escolhido (degrau 1, fato recente):** a linha italiana chegou e o time de instalação está
sendo montado agora, que é exatamente quando o manual em inglês vira problema de treinamento.
**Buracos:** [A CONFIRMAR: se o fabricante italiano já entrega manual em português]
```

**A observação que a skill escreveu pro dono:** o degrau 3 também existia (o texto do gerente sobre
tempo de treinamento), e ele entra como segunda frase da mensagem, o que é mais forte que usar só o
degrau 1.

---

## Ação 3 · A MENSAGEM

Saída real: o resto de `abordagem-importadora-1.md`. Resumo:

### E-mail

```
Assunto: a linha italiana e o treinamento de operador

[Nome],

Vi que vocês trouxeram a linha italiana há algumas semanas e estão montando o time de instalação
agora. Você mesmo escreveu que o tempo de treinamento de operador é o gargalo dessas entradas.

Na maior parte das vezes o manual chega em inglês, ou numa tradução automática que o operador não
consegue seguir, e o técnico acaba treinando de boca em boca. Isso costuma custar semanas de linha
rodando devagar.

Traduzi o manual de uma linha de embalagem parecida no ano passado, com revisão feita por engenheiro
mecânico, e o treinamento saiu em 9 dias em vez de [N] semanas. [A CONFIRMAR: prova, preciso da
autorização do cliente pra citar]

Vale uma conversa de 15 minutos pra ver se o manual de vocês tem esse problema?

[assinatura simples: nome, o que faz, telefone]

Se preferir não receber mais nada meu, é só responder pedindo pra parar.
```

**Contagem:** 118 palavras. Assunto com 44 caracteres. Texto puro, sem marcação, sem anexo.

### Opções extras de assunto

1. "manual da linha nova em português"
2. "sobre o treinamento de operador que você comentou"

### Versão pra rede profissional

**Pedido de conexão (198 caracteres):**
```
[Nome], li seu texto sobre tempo de treinamento de operador em entrada de linha nova. Trabalho com
manual técnico traduzido pra esse cenário. Bom te conhecer.
```

**Mensagem depois de aceito:**
```
Obrigado por aceitar.

Sobre o ponto do treinamento: nas linhas importadas que passaram por mim, o que mais atrasa é o
operador tentando seguir manual em inglês com o técnico traduzindo na hora. O erro que aparece é
sempre nos procedimentos de parada de emergência, que é onde tradução literal engana.

Como vocês estão resolvendo isso na linha italiana?
```

### A tabela do porquê

| Elemento | Baseado em |
|---|---|
| Abertura | a linha italiana anunciada há 6 semanas, fonte: site da empresa |
| Segunda frase | o texto dele sobre tempo de treinamento, fonte: perfil na rede profissional |
| Ponte | manual em inglês em entrada de linha nova, dor observada nos 3 clientes anteriores |
| Prova | o caso da linha de embalagem, ainda sem autorização de citação |
| Pedido | conversa de 15 minutos, a menor fricção possível pra um contato que nunca ouviu falar dele |

**O teste da troca de nome:** trocando a empresa por outra qualquer, a mensagem para de fazer sentido
nas duas primeiras frases. Passou.

---

## Ação 4 · RETOMADA E VOLUME

Saída real: a seção de retomada do mesmo arquivo, mais `regua-volume.md`. Resumo:

### Os 3 toques

**Toque 1 (3 dias depois), ângulo novo:**
```
[Nome], uma coisa que eu não falei: o pedaço que mais dá problema em manual traduzido por máquina é o
procedimento de parada de emergência, porque a tradução literal muda o sentido da instrução.

Se quiser, eu olho as duas páginas de segurança do manual de vocês e te digo o que eu veria. Sem
compromisso.
```

**Toque 2 (7 dias depois), entrega sem pedir nada:**
```
[Nome], montei uma lista de 6 pontos que costumam sair errados em manual de linha importada traduzido
por máquina. Está aqui embaixo, é curta.

[os 6 pontos, em texto puro]

Se algum deles bater com o que vocês estão vendo, me fala.
```

**Toque 3 (14 dias depois), encerramento:**
```
[Nome], não quero ocupar mais sua caixa de entrada com isso.

Se em algum momento o manual da linha italiana virar problema de treinamento aí, é só responder este
e-mail que eu retomo de onde paramos.

Boa sorte com a entrada da linha nova.
```

### A régua de volume

O dono nunca prospectou por e-mail e o domínio dele só recebe e responde. Situação: **domínio sem
aquecimento**.

| Semana | E-mails frios por dia | Total na semana |
|---|---|---|
| 1 | 5 | 25 |
| 2 | 10 | 50 |
| 3 | 15 | 75 |
| 4 | 20 | 100 |

**As decisões escritas no arquivo:**
- prospecção sai de um domínio secundário, nunca do endereço que fala com cliente atual;
- envio individual, um a um, nunca ferramenta de campanha em massa;
- a lista A de 9 contas cabe inteira na semana 1, sem forçar nada;
- reclamação de spam acima de 0,1% para a campanha no mesmo dia;
- quem pedir pra parar sai de tudo, para sempre.

---

## O que o gate reprovou no caminho (e por quê)

| Peça | O que estava escrito | Por que reprovou | Como ficou |
|---|---|---|---|
| E-mail | abertura desejando que o e-mail encontrasse a pessoa bem | abertura de robô (check 5) | cortada, o e-mail começa pelo fato |
| E-mail | "acompanho o trabalho de vocês há um tempo" | não é motivo, e o teste da troca de nome derrubaria | virou a linha italiana, com a fonte anotada |
| E-mail | o caso citado com número de economia sem autorização | prova sem fonte | virou `[A CONFIRMAR: prova]` com a tarefa de pedir autorização |
| E-mail | 190 palavras, com parágrafo apresentando o serviço | passa de 120, e o parágrafo de apresentação não entra | cortado pra 118 palavras |
| E-mail | dois pedidos, conversa e envio do manual pra análise | dois pedidos concorrentes | ficou só a conversa; a análise virou o toque 1 |
| Toque 1 | "só passando pra saber se você viu meu e-mail" | retomada sem ângulo novo | virou o ponto da parada de emergência |
| Volume | plano de 40 e-mails por dia na primeira semana | fora da régua pro domínio sem aquecimento | virou a escada de 5, 10, 15, 20 |
