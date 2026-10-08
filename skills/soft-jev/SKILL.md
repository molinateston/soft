---
name: soft-jev
description: >-
  Liga o Jev, um modelo rápido e barato que só DECIDE (escolhe uma opção, responde sim ou não, ou dá uma nota), para o agente parar de gastar o modelo caro em decisão simples: qual skill usar, se um trecho de memória importa, se a mensagem é da mesma tarefa, se uma resposta que diz "feito" tem prova. Guia a criação da chave no OpenRouter, faz o teste de aceite e, se o usuário quiser, liga o Jev automático nos pontos fixos do trabalho do agente. Use quando o pedido for: "liga o jev", "instala o jev", "decisão barata", "economizar token em decisão simples", "conferir se a resposta tem prova", "escolher a skill certa antes do modelo", "classificar sem gastar o modelo". NÃO use pra: escrever, planejar, pesquisar, fazer conta ou executar (o Jev não faz nada disso); autorizar ou aprovar ação; decidir o próximo passo do negócio (soft-leon). Leia e siga o fluxo inteiro do SKILL.md.
---

# Jev: o juiz rápido de decisões fechadas

## O que é, em palavras simples

O Jev é um modelo pequeno que responde só perguntas fechadas, até 32 numa chamada:

- **escolher** uma opção entre as que você dá (devolve a chance de cada uma e a confiança);
- **sim ou não** (devolve a chance de ser sim);
- **nota** numa régua de 2 a 10 níveis.

Ele não escreve texto, não planeja, não pesquisa e não faz conta. A resposta dele é uma sugestão: **nunca autoriza** executar, enviar, cobrar ou apagar. Confiança alta continua sendo estimativa.

Para que serve: tirar do modelo principal as decisões repetitivas, que são caras para o que valem. Exemplos: qual skill combina com o pedido, se uma memória é relevante agora, se a mensagem nova é da mesma tarefa, se uma resposta que diz "pronto" tem prova de que foi feito. Custa na ordem de US$ 0,04 por milhão de tokens de entrada (a saída é grátis) e cada chamada leva de 0,3 a 0,9 segundo. O modelo é o `typesafe/jev-1.13`, usado pelo serviço OpenRouter.

## Como conduzir (regras de conversa)

- **Uma pergunta por vez.** Cada uma diz o que o agente precisa, por quê, onde o usuário acha e o que vem depois.
- **Linguagem de gente.** Quem usa esta skill pode não ser programador. Explique "chave de API" como "a senha que deixa o seu agente usar o serviço".
- **A chave nunca aparece em mensagem.** Nem inteira, nem pela metade. Se o usuário colar a chave no chat, o agente responde "chave guardada" e pede que ele apague aquela mensagem.
- **Toda falha segue sem o Jev.** Sem chave, fora do ar, prazo estourado ou resposta ruim: o agente continua como antes e não tenta de novo sozinho.

## Etapa 0. Entender o que o usuário quer

Pergunte, uma coisa por vez:

1. **"Você quer o Jev só quando eu pedir (sob demanda), ou ligado sozinho nos pontos fixos do trabalho (automático)?"** Sob demanda é a escolha segura para começar: não mexe em configuração nenhuma. Automático liga ganchos no seu agente e vale depois que o sob demanda funcionar.
2. **"Qual agente você usa: Claude Code, Codex, Grok ou outro?"** (Só importa para o automático.)

## Etapa 1. Criar a chave no OpenRouter

O OpenRouter é um serviço que dá acesso a muitos modelos com uma conta só. O Jev roda lá, e o uso é cobrado por consumo.

1. Criar a conta em `openrouter.ai` e pôr crédito (US$ 5 já duram muito, porque cada decisão custa frações de centavo).
2. No painel, em "Keys", criar uma chave nova e dar um nome, por exemplo "jev".
3. Guardar a chave num arquivo só do usuário, por exemplo `~/.config/jev/openrouter.env`, com uma linha `OPENROUTER_API_KEY=<a chave>`, e restringir a permissão (`chmod 600`). O agente cria a pasta e o arquivo vazio, o usuário cola a chave dentro por conta própria, num editor, nunca no chat.

Explique o porquê: com a chave num arquivo fora de qualquer pasta de projeto, ela não vai parar em commit, log nem mensagem.

## Etapa 2. Teste de aceite (um comando)

Com a chave no arquivo, rode a partir da pasta desta skill:

```bash
JEV_KEY_FILE=~/.config/jev/openrouter.env python3 scripts/jev_decide.py '{"state":{"pedido":"Preciso do manual de deploy do site"},"questions":{"q1":{"type":"choice","instructions":"Qual candidato atende ao pedido?","criteria":{"manual":"Manual de deploy","estilo":"Guia de estilo","none":"Nenhum"}},"q2":{"type":"noul","instructions":"O pedido exige mudança em produção?"}}}'
```

Certo: `"available": true` e `"choice": "manual"` na `q1`. Se vier `available: false`, o campo `reason` diz o motivo: `missing_key` (a chave não foi achada no arquivo), `api_error`, `timeout`, `invalid_response` ou `pedido_invalido`. Também existe a versão em Node: `node scripts/jev_decide.mjs '<o mesmo JSON>'`.

## Etapa 3. Uso sob demanda

Quando surgir uma escolha fechada no meio de uma tarefa, o agente monta a pergunta no formato acima e chama o script. Como ler a resposta:

- **Confiança alta:** segue a sugestão.
- **Confiança média:** confere por outro caminho antes de seguir.
- **Confiança baixa:** ignora e decide sozinho.
- **Sempre** que a decisão mexer em dinheiro, em mensagem para terceiro, em dado apagado ou em segredo, quem decide é o usuário, qualquer que seja a confiança.
- Para conferência exata (soma, contagem, igualdade de identificador, status), usa-se a conta direta, não o Jev.

Mande estado mínimo: a mensagem cortada e só os campos que a pergunta precisa. Os scripts recusam campos com nome de segredo (senha, chave, token).

## Etapa 4 (opcional). Ligar o automático

Só depois que a etapa 2 deu certo, e só se o usuário pediu. Precisa de Node 22 ou mais novo. Os pontos fixos em que o Jev entra:

1. **Preparação do turno:** quando chega a mensagem, o Jev classifica a intenção, o tamanho e a skill candidata, e vira um aviso curto no contexto. Nunca troca o pedido.
2. **Conferência final:** se a resposta diz "feito", "publicado" ou "corrigido" e o rastro do trabalho não sustenta, o agente revisa a redação uma vez.
3. **Curadoria de memória:** antes de gravar memória por conta própria, barra o que é passageiro e sem base.

O passo a passo completo, com os comandos para cada agente e para desfazer, está em `kit/INSTALAR.md`. Em resumo: copiar `kit/codigo/` para uma pasta fixa, rodar `npm install`, conferir com `node src/cli.mjs --check` (sem rede) e `--smoke` (uma chamada real), e ligar no agente com `node hooks/install.mjs ... ` **primeiro sem `--apply`**, que só mostra o plano. Repetir com `--apply` depois de o usuário conferir. Para desfazer: o mesmo comando com `--remove --apply`.

Antes de filtrar qualquer texto, o kit barra a chamada inteira se achar chave, senha, token, CPF ou cartão, e mascara valor em dinheiro, e-mail, telefone e caminho de arquivo.

## Etapa 5. Medir antes e depois

Antes de deixar o automático ligado, rode a mesma tarefa com e sem o Jev e compare tokens, tempo e acerto. Só fica ligado o que melhora sem piorar. O registro dos hooks fica em `~/.local/state/jev-auto/`.

## Se algo der errado

| Sintoma | O que fazer |
|---|---|
| `missing_key` | A chave não está no arquivo, ou `JEV_KEY_FILE` aponta para outro lugar. Confira o caminho e a linha `OPENROUTER_API_KEY=`. |
| `api_error` (401 ou 402) | Chave errada ou sem crédito no OpenRouter. |
| `timeout` | O Jev demorou mais de 2 segundos. O agente segue sem ele. |
| `invalid_response` | Resposta fora do formato. O agente segue sem ele e não repete. |
| O hook não aparece no agente | Reabra o agente depois da instalação. No Grok, só conversas abertas depois. |
| Quero desligar tudo | `node hooks/install.mjs ... --remove --apply` e apague a linha da chave se quiser. |

## O que esta skill não faz

- Não guarda a chave em lugar nenhum além do arquivo que o usuário criou.
- Não liga hook sem mostrar o plano e receber o sim.
- Não trata a resposta do Jev como ordem.
