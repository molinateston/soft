# Instalar

Este guia parte do princípio de que você já extraiu o ZIP deste kit em algum
lugar do seu computador ou servidor — chamamos essa pasta de `~/seu-projeto`
nos exemplos. Troque todo caminho de exemplo pelo caminho real onde você
colocou os arquivos.

## Antes de instalar

1. **Node 22 ou mais novo** (`node --version`). Sem isso, nada abaixo funciona.
2. **Instale as dependências dentro de `codigo/`:**

   ```sh
   cd ~/seu-projeto/codigo
   npm install
   ```

3. **Credencial.** Tudo neste kit lê a chave de acesso ao serviço TypeSafe
   (o provedor do JEV) na variável de ambiente `TYPESAFE_API_KEY`. É uma
   chave própria de cada pessoa ou empresa que usa o TypeSafe — não vem
   incluída no kit; crie sua conta no serviço, gere a chave lá e exporte-a:

   ```sh
   export TYPESAFE_API_KEY="sua-chave-aqui"
   ```

   Quem já usa um gerenciador de senhas (1Password, Keychain do macOS ou
   outro) pode configurar por conta própria uma leitura automática dessa
   chave, para não precisar exportá-la à mão toda sessão — mas isso é
   dispensável. A variável de ambiente sozinha sempre funciona.

## Testar

Antes de instalar qualquer hook, confira se o pacote está sadio:

```sh
node src/cli.mjs --check    # só confere configuração, não gasta chamada nem lê chave
node src/cli.mjs --smoke    # uma chamada real de teste; precisa da chave configurada
```

Se `--check` reportar `key_present: null` ou `false` antes de você exportar a
chave, é esperado — ele só olha o ambiente, não tenta ler nenhum cofre. Depois
de exportar `TYPESAFE_API_KEY`, rode `--smoke` de novo para confirmar que a
chave e a rede realmente funcionam.

A partir daqui, escolha a seção do seu agente de código.

## 1. Claude Code

O instalador incluído (`codigo/hooks/install.mjs`) registra os hooks direto no
`settings.json` do Claude Code, sem tocar em nada mais que já esteja lá. Rode
primeiro sem `--apply` para ver o plano:

```sh
node hooks/install.mjs \
  --config /caminho/absoluto/settings.json \
  --harness claude \
  --runtime /caminho/para/jev-auto \
  --node /caminho/para/node \
  --shell /bin/zsh
```

- `--config`: caminho absoluto do `settings.json` do Claude Code a afetar (o
  global do usuário ou o de um projeto específico).
- `--runtime`: caminho absoluto da cópia do pacote `codigo/` já com
  `npm install` feito — pode ser a própria pasta onde você extraiu o kit.
- `--node`: caminho absoluto do executável `node` (`command -v node`).
- `--shell`: `/bin/zsh` ou `/bin/bash`, o shell que deve herdar seu ambiente
  (variáveis do seu perfil, incluindo `TYPESAFE_API_KEY`).

Esse comando só imprime o plano em JSON (`status: dry_run`) e **não altera
nenhum arquivo**. Com o plano correto, repita o mesmo comando acrescentando
`--apply` no fim para gravar de verdade, e reabra o Claude Code.

Para reverter, rode o mesmo comando trocando as flags de instalação por
`--remove --apply` — remove só as entradas deste kit, preservando qualquer
outro hook que já existisse no arquivo.

## 2. Codex

Mesma ferramenta, trocando o harness e o arquivo de configuração:

```sh
node hooks/install.mjs \
  --config ~/.codex/hooks.json \
  --harness codex \
  --runtime /caminho/para/jev-auto \
  --node /caminho/para/node \
  --shell /bin/zsh
```

Rode sem `--apply` primeiro, confira o plano, depois repita com `--apply`. O
Codex mostra o hash de cada hook no próprio `hooks list` nativo — confira
contra o comando impresso antes de confiar nele. Reverter: `--remove --apply`.

## 3. Grok

```sh
node hooks/install.mjs \
  --config ~/.grok/hooks/jev-auto.json \
  --harness grok \
  --runtime /caminho/para/jev-auto \
  --node /caminho/para/node \
  --shell /bin/zsh
```

Mesmo fluxo: sem `--apply`, confira, depois com `--apply`; `--remove --apply`
reverte. **Atenção:** o Grok fixa os hooks que existiam quando a conversa foi
aberta — uma conversa já aberta antes da instalação não ganha o hook. Feche o
Grok e abra uma conversa nova depois de instalar ou atualizar.

## 4. Hermes

Se o seu agente roda dentro de um Hermes (plataforma de agente com plugins),
não use o instalador acima — copie os arquivos manualmente:

1. Copie `codigo/hermes-plugin/jev-auto/` inteira para a pasta de plugins do
   seu Hermes.
2. Copie `codigo/skill/jev-decisions/SKILL.md` para a pasta de skills do seu
   Hermes.
3. Reinicie ou recarregue o gateway conforme o procedimento da sua própria
   instalação (varia conforme como você hospeda o Hermes).

Depois de recarregar, o plugin roda os mesmos gatilhos automáticos das outras
seções, e a skill fica disponível para o agente consultar as regras de quando
chamar o JEV no meio do trabalho.

## 5. Outro agente (sem hooks nativos)

Para qualquer agente sem harness com suporte pronto acima, dois caminhos
genéricos, sem instalador:

- **MCP**, se o agente suporta servidores MCP locais via stdio: registre um
  server apontando para `node /caminho/para/jev-auto/src/cli.mjs --mcp`. Isso
  expõe a ferramenta `jev_decide` para o agente chamar sob demanda.
- **CLI direta**, em qualquer lugar que rode um comando de shell: use
  `jev ask "sua pergunta" ...` (exemplos no `codigo/README.md`) ou, sem o
  atalho `jev` no PATH, `node /caminho/para/jev-auto/src/cli.mjs --decide`
  passando o JSON da pergunta pela entrada padrão.

Nenhum dos dois cria gatilho automático — cabe às instruções do próprio
agente (prompt, equivalente a um `AGENTS.md`) dizer quando chamar `jev ask`
ou `jev_decide` no meio do trabalho.

## Desligar ou reverter

- **Hooks instalados pelo instalador (Claude Code, Codex, Grok):** rode
  `node hooks/install.mjs --config <mesmo-arquivo> --harness <mesmo-harness>
  --remove --apply`. Apaga só as entradas deste kit; outros hooks já
  existentes no arquivo continuam intactos.
- **Entrada MCP manual (seção 5):** remova a entrada `jev` do arquivo de
  configuração de servidores MCP do seu harness.
- **Hermes:** desative o plugin `jev-auto` nas configurações do seu Hermes e
  recarregue o gateway; a skill `jev-decisions` pode ficar ou ser removida da
  pasta de skills, sem efeito nos hooks.

Em nenhum caso a chave `TYPESAFE_API_KEY` precisa ser apagada — ela é só uma
variável de ambiente ou entrada de gerenciador de senhas sua; revogar o
acesso é decisão separada, feita direto no painel do provedor TypeSafe.
