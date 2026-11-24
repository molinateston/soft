---
name: soft-motores-api
description: Cadastra outra IA por API no LEON (DeepSeek, GLM da Z.ai, OpenRouter, MiniMax, Kimi, Fireworks, NVIDIA, Grok da xAI ou qualquer provedor no formato Anthropic), guarda a chave sem ela passar pelo chat, testa a chave e explica como usar no /motor. Use quando o pedido for "quero usar outra IA", "cadastrar minha API", "DeepSeek", "GLM", "MiniMax", "Grok", "OpenRouter", "Kimi", "trocar o motor do LEON", "acabou meu crédito do Claude", "quero uma IA mais barata", "pôr minha chave de API". NÃO use para trocar entre Claude e Codex (é só mandar /claude ou /codex) nem para login da conta do Claude ou do Codex (/login).
---

# Motores por API: pôr outra IA no LEON

Esta skill guia você, **uma pergunta por vez**, a ligar no LEON uma IA de outra empresa paga por uso. Em cada passo, o agente diz em palavras simples: o que precisa, por que precisa, onde você consegue e o que vem depois. Ninguém precisa saber programar.

Ferramenta: `scripts/adiciona-motor.sh`, nesta pasta. Nos comandos para você colar, o agente usa SEMPRE o caminho completo dela, por exemplo `sudo bash /home/cloud/.claude/skills/soft-motores-api/scripts/adiciona-motor.sh` (o agente confere o caminho certo da sua instalação antes de mandar). Ele roda **simulado** por padrão (só mostra o que faria) e só escreve com `--aplicar`. Provedores, preços e avisos: `references/provedores.md`.

## Regras que valem o tempo todo

1. **A chave nunca passa pelo chat.** Nem pelo Telegram, nem aqui. Se você colar a chave na conversa, o agente avisa com calma: "Essa chave ficou gravada no histórico. Entre no painel do provedor, apague essa chave e gere outra." A chave colada não é usada.
2. A chave só entra pelo terminal do servidor, digitada escondida (ação `chave`). O script nunca recebe a chave por argumento e nunca mostra o valor, só quantos caracteres ela tem. **Nunca cole a chave no meio de um comando**: se ela for parar como argumento, o próprio terminal pode mostrá-la de volta numa mensagem de erro e guardá-la no histórico. Se isso acontecer, apague a chave no painel do provedor e gere outra.
3. **Simulado antes de aplicar.** O agente roda sem `--aplicar`, mostra o resultado, pede o seu "pode" e só então roda com `--aplicar`.
4. Uma pergunta por mensagem. Se algo der errado, o agente lê a mensagem do script (ela já vem em linguagem simples) e diz o próximo passo.
5. Se a instalação não for a padrão, repita em todos os comandos o `--env` e o `--cadastro` que o script mostrar.

## O caminho, passo a passo

### Passo 1. Qual IA?
Leia o `scripts/catalogo.json` desta skill e apresente a lista em poucas linhas: nome, para que serve, custo estimado e se já foi testada de verdade (tabela em `references/provedores.md`).

Pergunta: **"Qual dessas IAs você quer usar no LEON?"**
- Por quê: cada empresa tem o próprio endereço, os próprios modelos e cobra à parte.
- Se você não souber: para conversa barata, os de menor custo na estimativa de 23/11/2026 são glm-5.3-flash, deepseek-flash e o MiniMax M3.1 Flash pelo OpenRouter (confira o preço no painel).
- IA fora da lista: a página da empresa fala em "compatível com Anthropic" ou "usar com o Claude Code"? Então é a opção **outro**. Se a página só fala em formato OpenAI ou `/chat/completions`, é **outro-openai**: precisa do tradutor, e ligar o tradutor é serviço do suporte.
- Se você veio porque "acabou o crédito do Claude": o provedor por API serve para **conversar**. Trabalho na máquina (arquivos, skills, ferramentas) continua precisando do Claude ou do Codex.

### Passo 2. Já tem conta e chave?
Pergunta: **"Você já tem conta nesse provedor, com crédito, e uma chave de API?"**
- Por quê: a chave é a senha que deixa o LEON usar a sua conta; o provedor cobra no seu cartão.
- Onde conseguir: tabela "Onde pegar a chave" em `references/provedores.md`. Crie a conta, ponha crédito, gere a chave e guarde num lugar seguro, sem mandar no chat.
- Depois: escolher o modelo.

### Passo 3. Qual modelo?
Mostre os modelos do provedor (saem no catálogo) e o padrão. Pergunta: **"Fico com o modelo padrão ou você quer outro desta lista?"**
- Por quê: o modelo é o "cérebro" que responde; muda preço, rapidez e qualidade.
- Modelo fora da lista só entra pela opção **outro**.
- Na opção **outro**, uma pergunta por vez: o nome que vai aparecer, o endereço (a URL base que a página do provedor indica para o Claude Code, sem `/v1/messages` no fim) e o nome exato do modelo. O id é um apelido curto em minúsculas (vira o comando, tipo /grok). Diga com clareza: **a sua chave vai ser enviada para esse endereço**; confira o domínio na documentação oficial do provedor.

### Passo 4. Cadastrar
Simulado: `sudo bash <caminho completo>/adiciona-motor.sh adiciona --provedor <escolha> [--modelo <modelo>]`
(opção outro: `--provedor outro --id <apelido> --nome "<nome>" --url <endereço> --modelo <modelo>`).

Mostre o bloco e pergunte: **"Posso gravar esse provedor no cadastro do LEON?"** Com o sim, o mesmo comando com `--aplicar`. O script guarda uma cópia do cadastro de antes, troca o arquivo de uma vez só, mantém dono e modo, e pede ao validador do próprio LEON para conferir; se ele recusar, a cópia de antes volta.

Se o script recusar (id repetido, endereço sem https, modelo vazio ou fora da lista), explique o motivo e pergunte o dado que falta.

### Passo 5. Guardar a chave
A chave é digitada no **terminal do servidor**: a tela de texto onde se digitam comandos. Se você nunca abriu um, peça ao suporte ou ao Léo que abra o terminal com você. Entre como root (o comando começa com `sudo`) ou como o usuário dono do LEON (normalmente `cloud`, e aí sem `sudo`). Se aparecer que o node não foi achado, é porque o `sudo` às vezes não enxerga o node: rode como o usuário dono do LEON, sem `sudo`. Se aí aparecer que a máquina não deixa rodar a conferência isolada sem root, peça ajuda ao suporte.

Pergunta: **"Você está com o terminal do servidor aberto?"** Com o sim, peça para rodar:
`sudo bash <caminho completo>/adiciona-motor.sh chave --provedor <id> --aplicar`
- O script desliga o eco do terminal antes de tudo e depois pede a chave. **Só cole depois que aparecer "Cole a chave"** (o que for colado antes é jogado fora). Cole e aperte Enter. **Nada aparece na tela; é de propósito.**
- Por quê: assim a chave vai direto para o arquivo de configuração do LEON (o `.env`), sem passar pela conversa, sem ficar no histórico de comandos e sem aparecer na tela.
- Se a sessão do terminal estiver sendo gravada ou compartilhada: a chave não aparece, mas o gerenciador de área de transferência pode guardar o que você copiou. Depois de colar, copie outra coisa qualquer por cima. Se tiver dúvida, gere uma chave nova no painel.
- Sem terminal (por exemplo, só pelo celular): peça ajuda ao suporte para esta parte.

### Passo 6. Testar
Pergunta: **"Posso fazer um teste rápido com a sua chave? Costuma custar centavos; confira o seu painel."** Rode primeiro `sudo bash <caminho completo>/adiciona-motor.sh testa --provedor <id>` e mostre a linha "A CHAVE SERÁ ENVIADA PARA". Com o sim, rode com `--aplicar`. Se o destino (esquema, endereço, porta e caminho) não for exatamente o de um provedor do catálogo, o script ainda pede `--confirmo-destino <destino>`: só confirme depois de conferir na documentação oficial do provedor.

Leia o resultado: funcionou; o modelo só pensou (a chave está boa); chave recusada; sem saldo; passou do limite; modelo inexistente; redirecionou (confira a URL); não respondeu a tempo; tradutor desligado. Cada resposta já diz o que fazer. Depois de consertar, teste de novo.

### Passo 7. Começar a usar
- No Telegram, mande /motor: o provedor novo aparece na lista. O LEON costuma pegar a chave nova no próximo pedido; se o provedor não aparecer em /motor em 1 minuto, peça ajuda ao suporte.
- Para usar: /motor e escolha, ou mande o atalho (ex.: /deepseek).
- No provedor o LEON **só conversa**: sem ferramentas, sem mexer em arquivos, sem skills. Para trabalho de verdade, volte com /claude ou /codex.
- Se o provedor falhar (saldo, chave, fora do ar), o LEON **não troca de motor sozinho**: você troca com /claude, /codex ou o atalho de outro provedor.
- O provedor cobra por uso, no seu cartão. Acompanhe o gasto no painel dele.

Feche dizendo o que ficou pronto e o único passo que falta, se faltar algum.

## Caminhos

Padrão: `.env` em `/home/cloud/lean-bridge/.env` e cadastro em `/home/cloud/.leon/motores-api.json` (o cadastro também sai do `.env`, por LEON_MOTORES_API ou LEON_DATA_DIR). Em outra instalação, o suporte informa o caminho e você usa `--env <arquivo>`. **Ao usar `--env` fora do padrão, passe também `--cadastro <arquivo>`**: sem ele, o script usa o cadastro da pasta home do dono do `.env` (na casa padrão, `/home/cloud/.leon/motores-api.json`) e, com `--aplicar`, grava nele. O script precisa do LEON instalado ao lado desse `.env`: ele pede ao validador do próprio LEON (`leon2/lib/motores-api.cjs`) para conferir o cadastro, e só aceita esse arquivo (e o node) se ele e todas as pastas acima forem do root ou do dono do LEON, sem atalho e sem permissão de escrita para o grupo nem para outros. Se o script disser que os arquivos do LEON podem ser alterados por outro usuário, peça ao suporte para tirar a escrita de grupo dessas pastas. A conferência roda como o dono do LEON, sem rede e com ambiente limpo. O teste da chave nunca passa por proxy e nunca segue redirecionamento.
