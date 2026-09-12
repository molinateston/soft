# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, números, prazos e resultados foram inventados só pra mostrar
> a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega de
> verdade. Num trabalho real, todo número e toda prova sem fonte nascem marcados `[A CONFIRMAR]` e o
> dono confirma antes de sair.

**O caso fictício:** um software de controle de estoque pra lojas de material de construção de bairro.
A dona fictícia vende assinatura mensal de 380 reais, com 14 dias de teste grátis. O gatilho de entrada
da campanha é a abertura do teste. O problema que ela ouve dos clientes: a loja compra dobrado porque
ninguém sabe o que já tem no depósito.

Este arquivo mostra a saída resumida de cada ação, na ordem. A saída real é maior; aqui está só o
suficiente pra você reconhecer o formato antes de começar.

---

## O que o dono deu de entrada

> "Umas 60 lojas começam o teste por mês e só 9 viram assinante. A maioria some no terceiro dia. Eu
> mando um e-mail de boas-vindas e depois um no dia 13 avisando que o teste acaba. Só isso."

**O que faltava:** o arco não existia (dois e-mails soltos não formam escada), o momento em que o
valor aparece nunca foi medido, e não havia nenhuma fala literal de cliente anexada.

## As perguntas que a skill fez (uma por vez)

1. "O que a pessoa fez pra entrar nessa sequência?" → *"Abriu o teste grátis de 14 dias."*
2. "O que precisa acontecer pra você considerar essa campanha um sucesso?" → *"A loja cadastrar o estoque inicial e fazer a primeira baixa. Quem faz isso vira assinante quase sempre."*
3. "O que você vende e por quanto?" → *"Assinatura de 380 por mês."* `[fictício]`
4. "Qual a frase que essa pessoa fala no pior do problema?" → *"'Comprei 40 sacos de cimento e tinha 30 no fundo do depósito.' Ouço isso toda semana."*
5. "Que prova real você pode citar?" → *"Uma loja parou de comprar duplicado e economizou 4 mil no primeiro mês."* `[fictício]`
6. "Que material pronto você já tem pra linkar?" → *"Um vídeo de 6 minutos ensinando a cadastrar o estoque, e uma planilha de contagem."*

**Premissa declarada em 1 linha:** o marco de valor é o primeiro registro de saída de produto, então a
sequência inteira empurra pra esse ato e não pra assinatura, porque a assinatura vem depois dele.

---

## Ação 1 · A SEQUÊNCIA

Saída real: `sequencia-email.md`. Resumo:

### O arco declarado (antes de escrever qualquer e-mail)

A campanha conta a história de uma loja que para de comprar no escuro. Começa mostrando que o depósito
tem dinheiro parado dentro dele, faz a pessoa contar o que tem, mostra o primeiro número que ela nunca
tinha visto, e só depois pede a assinatura, com a conta já feita por ela mesma. A intensidade sobe
assim: curiosidade, primeiro ato pequeno, primeiro número, comparação com quem já faz, prazo.

### O bloco de configuração (o topo do arquivo)

```
GATILHO: abriu o teste grátis de 14 dias
OBJETIVO: a loja cadastra o estoque inicial e registra a primeira saída ate o dia 7
PUBLICO: dono de loja de material de construcao de bairro, 1 a 3 funcionarios, sem sistema
TIPO: boas-vindas / onboarding
PECAS: 6 em 14 dias: D+0, D+1, D+3, D+6, D+10, D+13
CADENCIA: densa na primeira semana, espacada na segunda
SAIDA: assinou · respondeu · pediu pra sair
SUPRESSAO: quem abriu chamado no suporte nas ultimas 48h nao recebe a peca de oferta
FUROS: [A CONFIRMAR: link do video de cadastro] · [A CONFIRMAR: autorizacao por escrito do caso dos 4 mil]
```

### A tabela de visão geral

| # | Assunto | Trabalho | Dia | CTA | Condição |
|---|---|---|---|---|---|
| 1 | Seu depósito tem dinheiro parado | recebe e sabe o que esperar | D+0 | Ver o vídeo de 6 minutos | todos |
| 2 | Comece pelo cimento | primeira vitória rápida | D+1 | Cadastrar o primeiro produto | quem não cadastrou nada |
| 3 | O número que a loja nunca viu | mostra o primeiro resultado | D+3 | Registrar a primeira saída | quem já cadastrou |
| 4 | 40 sacos comprados, 30 no fundo | prova de quem já fez | D+6 | Ver o caso completo | todos |
| 5 | Faltam 4 dias do seu teste | condição com prazo | D+10 | Assinar por 380 | quem não assinou |
| 6 | Último dia | último aviso, curto | D+13 | Assinar por 380 | quem não assinou |

**STOP.** Aqui a skill parou e perguntou: *"essa é a escada? escrevo os e-mails?"*

### Dois e-mails escritos por inteiro

```
### E-mail 2 · primeira vitória rápida

**Assunto A:** Comece pelo cimento
**Assunto B:** O produto que some primeiro
**Prévia:** Cadastre um só. Leva dois minutos e já mostra uma coisa.
**Trabalho:** fazer a pessoa cadastrar o primeiro produto hoje, porque quem cadastra um cadastra o resto.
**Dia:** D+1 (contado do gatilho) · **Recebe:** quem não cadastrou nenhum produto · **Pula:** quem já cadastrou

---
Não cadastre o depósito inteiro. Cadastre um produto.

O cimento é o melhor pra começar: sai rápido, entra sempre, e é onde a maior parte das lojas
compra duplicado sem perceber.

Abre o sistema, clica em Produtos, coloca o nome e a quantidade que tem hoje no depósito. Dois
minutos. Depois disso a próxima contagem já vem sozinha.

Cadastrar o primeiro produto -> [link do painel]

Se emperrar em alguma tela, responde este e-mail que eu vejo.
---

**Nota de configuração:** condicione ao campo "produtos cadastrados = 0". Se a ferramenta não
registrar esse campo, mande pra todo mundo e troque a primeira linha por "se você já cadastrou, pula
esse aqui".
```

```
### E-mail 5 · condição com prazo

**Assunto A:** Faltam 4 dias do seu teste
**Assunto B:** O que acontece na sexta
**Prévia:** Seus dados ficam. O acesso é que fecha.
**Trabalho:** transformar o número que a pessoa já viu em decisão, com prazo real.
**Dia:** D+10 · **Recebe:** quem não assinou · **Pula:** quem assinou, e quem abriu chamado nas últimas 48h

---
Seu teste fecha na sexta.

Você cadastrou [N] produtos e registrou [N] saídas nesses dez dias. Isso já é o histórico que mostra
o que a loja gira e o que fica parado.

Se você assinar antes de sexta, esse histórico continua de onde parou. Se não, ele fica guardado por
30 dias e depois some.

São 380 por mês, sem fidelidade, cancela pelo painel.

Assinar e continuar de onde parei -> [link do checkout]
---

**Nota de configuração:** os dois [N] são campos dinâmicos da ferramenta. Se ela não fizer isso, corte
a frase inteira em vez de mandar colchete pro cliente.
```

**STOP.** A skill mostrou os 6 e-mails limpos e o checklist de subida, e perguntou "te serve? ajusto,
ou sigo pra ramificação?".

---

## Ação 4 · LÓGICA, TESTE E META

Saída real: a seção somada ao mesmo arquivo. Resumo:

### O desenho do fluxo

```
[Gatilho: abriu o teste]
        |
    E-mail 1 (D+0)
        |
  Cadastrou produto? --sim--> E-mail 3 (D+3)
        |                            |
       nao                    Registrou saida? --sim--> E-mail 4 (D+6)
        |                            |
        v                           nao
    E-mail 2 (D+1)                   |
        |                            v
        +--------------------> E-mail 4 (D+6)
                                     |
                                     v
                               E-mail 5 (D+10)
                                     |
                               Assinou? --sim--> [SAI: converteu]
                                     |
                                    nao
                                     v
                               E-mail 6 (D+13)
                                     |
                                     v
                           [SAI: sequencia completa]
```

### As condições, em lista

- **Saída:** assinou · respondeu qualquer e-mail · pediu pra sair da lista.
- **Supressão:** chamado aberto no suporte nas últimas 48 horas bloqueia as peças 5 e 6 · máximo de um
  e-mail por dia por pessoa.
- **Reentrada:** quem deixou o teste vencer pode entrar de novo no arco de reengajamento depois de 90
  dias, uma vez só.
- `[A CONFIRMAR: sinais disponíveis]` a ferramenta registra clique e resposta; cadastro de produto e
  registro de saída dependem de integração que ainda não foi conferida.

### A tabela de metas (alvo desta campanha)

| Métrica | Alvo | Como está hoje |
|---|---|---|
| Abertura média | 50 a 70% | `[A CONFIRMAR]` |
| Clique médio | 10 a 20% | `[A CONFIRMAR]` |
| Conversão em assinante | 15 a 30% | 15% (9 de 60) `[fictício]` |
| Saída da lista | abaixo de 0,5% | `[A CONFIRMAR]` |

### Os testes propostos

1. **Assunto da peça 5**, o de maior impacto: "Faltam 4 dias do seu teste" contra "O que acontece na
   sexta". Metade da base em cada braço. Decide pela taxa de clique, não pela abertura.
2. **Texto do botão da peça 2**: "Cadastrar o primeiro produto" contra "Começar pelo cimento".
3. **Horário da peça 1**: envio na hora do cadastro contra envio às 7h do dia seguinte, porque dono de
   loja de bairro abre e-mail antes de levantar a porta.

### O checklist de subida (fecha o arquivo)

1. Criar a automação com o nome "teste de 14 dias".
2. Gatilho: abertura do teste grátis.
3. Colar as 6 peças com os atrasos D+0, 1, 3, 6, 10, 13.
4. Ligar as duas ramificações de comportamento e as três saídas.
5. Ligar a supressão de chamado aberto.
6. Ligar a medição das 4 métricas da tabela.
7. Disparar um teste pra si mesma e conferir no celular antes de abrir pra base.

---

## O que o gate reprovou no caminho (e por quê)

| Peça | O que estava escrito | Por que reprovou | Como ficou |
|---|---|---|---|
| E-mail 1 | "Espero que este e-mail te encontre bem" | abertura de robô (check 5) | cortada, o e-mail começa pela segunda frase |
| E-mail 3 | o par colado negando estoque pra afirmar caixa | antítese de espelho (check 3) | "O estoque parado é caixa parado, e agora você tem o número." |
| E-mail 4 | promessa de revolução na compra | verbo de transformação genérico (check 4) | "Isso muda o que você compra na próxima semana." |
| E-mail 5 | dois CTAs, assinar e agendar demonstração | dois pedidos concorrentes | ficou só assinar; a demonstração virou linha de texto no fim |
| E-mail 6 | `[nome do produto]` repetido em 3 peças | placeholder repetido reprova a campanha | a skill parou e perguntou o nome antes de seguir |
