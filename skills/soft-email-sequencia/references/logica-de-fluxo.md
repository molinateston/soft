# Lógica de fluxo: ramificação, saída, supressão, reentrada

A sequência escrita é metade do trabalho. A outra metade é o que decide quem recebe o quê, e quando
a pessoa para de receber. Sem isso, a campanha manda oferta pra quem já comprou e cobra quem
acabou de abrir chamado no suporte.

## 1. Ramificação

Um desvio nasce de um **comportamento observável**, nunca de palpite. Os três que qualquer
ferramenta registra: clicou, respondeu, comprou. Abertura é sinal fraco (bloqueio de imagem e
pré-carregamento distorcem), então use abertura só como reforço, nunca como única condição.

Os desvios que mais pagam:

| Comportamento | Desvio |
|---|---|
| Clicou o CTA da peça 1 | pula a peça 2 (que era pra convencer) e vai direto pra 3 |
| Abriu a 2 e não clicou | recebe a 2b, o mesmo pedido com menos fricção |
| Não abriu nada até a peça 3 | recebe a 3 com assunto novo, e a cadência afrouxa |
| Respondeu qualquer coisa | sai da automação no mesmo dia e vira conversa humana |

## 2. Saída

**O que conta como conversão** desta campanha, escrito em uma frase, e a pessoa sai no instante em
que faz isso. Sequência que continua depois da compra é o jeito mais rápido de irritar cliente novo.

Saídas obrigatórias em toda campanha: comprou · agendou · respondeu · pediu pra sair da lista.

## 3. Supressão

O e-mail está na fila, o dia chegou, e mesmo assim ele não sai:

- a pessoa já está em outra sequência ativa (colisão);
- ela abriu chamado de suporte nas últimas 48 horas (oferta em cima de problema aberto queima);
- ela já recebeu um e-mail hoje;
- ela pediu pra não receber comunicação comercial, mesmo continuando cliente.

## 4. Reentrada

Pode a mesma pessoa entrar de novo? Em que condição, e quantas vezes? Sem essa regra escrita, a base
antiga fica em loop de reengajamento e a taxa de saída sobe. O padrão seguro: reentrada uma vez só,
e com no mínimo 90 dias de intervalo.

## 5. O desenho em bloco

O fluxo vai no arquivo como diagrama de texto, porque é ele que o dono usa pra montar a automação na
ferramenta. Formato:

```
[Gatilho: baixou o material]
        |
    E-mail 1 (D+0)
        |
   Clicou? --sim--> E-mail 3 (D+3)
        |                  |
       nao            Comprou? --sim--> [SAI: converteu]
        |                  |
        v                 nao
   E-mail 2 (D+2)          |
        |                  v
        +------------> E-mail 4 (D+7)
                           |
                           v
                   [SAI: sequencia completa]
```

## 6. O checklist de subida

Fecha todo arquivo de entrega:

1. Criar a automação com o nome da campanha.
2. Configurar o gatilho de entrada exatamente como está no bloco de configuração.
3. Colar cada peça com o atraso declarado.
4. Ligar as ramificações e as saídas.
5. Ligar as supressões.
6. Ligar a medição das métricas da tabela de metas.
7. Disparar um teste pra você mesmo antes de abrir pra base, e conferir no celular.
