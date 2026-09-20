# Setup de conexão: ligar o agente na área de membros

Leia primeiro, antes de qualquer outra ação. Regra dura: **conexão testada antes de operar.** Chave errada produz uma fila de falhas que parecem defeito do sistema e não são.

## O que o agente precisa ter

Duas coisas, e só duas:

| Nome | O que é |
|---|---|
| `MEMBERS_URL` | O endereço da área de membros do dono, com https e sem barra no fim |
| `MEMBERS_API_KEY` | A chave de API daquela instalação |

Ambas ficam no `.env` do projeto do dono, junto com as outras credenciais dele. Nunca dentro da pasta desta skill. O molde está em `assets/env.exemplo`, bloco "conexão do agente".

## De onde vem a chave

A chave nasce na instalação, não no painel. O instalador inicializa a escola e chama o script na pasta final:

```bash
bash gerar_chave_api.sh --nome agente-leon
```

O script lê o `.env` da instalação, acha a escola pelo e-mail do dono e grava a chave no banco no mesmo formato que a tela de administração gravaria: 21 caracteres, sem hash, amarrada ao domínio e ao usuário dono. Ele imprime a chave uma vez e guarda em `chave-agente-leon.env`, com permissão 600. Rodar duas vezes não duplica nada. O comando manual serve para recuperação ou rotação, não como etapa normal da instalação.

Daí saem as duas linhas que o agente precisa:

```
MEMBERS_URL=https://membros.dominiododono.com.br
MEMBERS_API_KEY=<o valor do arquivo>
```

O agente copia esse par para o `.env` do projeto do dono. **O dono não vê painel nenhum neste passo, e não precisa colar chave em mensagem.**

Se a chave vazar, sumir ou parar de funcionar, o conserto é uma linha na VPS, e a chave velha morre na hora:

```bash
bash gerar_chave_api.sh --nome agente-leon --rotacionar
```

**O agente nunca repete a chave em nenhuma mensagem.** Nem inteira, nem os quatro últimos caracteres, nem mascarada. Confirma pelo nome, não pelo valor. Se o dono colar a chave no chat, o agente responde `chave da sua área de membros guardada` e pede pra ele apagar aquela mensagem.

## Como o cabeçalho vai em toda chamada

```
Base:    {{MEMBERS_URL}}
Header:  x-api-key: {{MEMBERS_API_KEY}}
Header:  Content-Type: application/json
```

Duas observações que economizam uma hora de depuração:

- **Não existe cabeçalho de domínio pra mandar.** A camada da frente resolve o domínio sozinha e sobrescreve o que vier. Mandar não atrapalha e não ajuda.
- **A chave é sempre dona de tudo.** Não existe chave de poder reduzido. Quem tem a chave faz tudo que o dono faz. Por isso ela mora no `.env` e em nenhum outro lugar.

## Teste de leitura obrigatório

Três chamadas. As três têm que voltar 200. Enquanto não voltarem, o agente não opera.

**1. Listar os cursos que existem**
```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/products?limit=1"
```

**2. Ler os cursos com o conteúdo, pra descobrir os ids**
```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/products?limit=50"
```
Guarde de cada curso: `productId`, `title`, `published`. O agente guarda `productId` no placeholder interno `COURSE_ID` e opera por ele, nunca por nome.

**3. Ler as seções e aulas de um curso que já exista**
```bash
curl -s -H "x-api-key: {{MEMBERS_API_KEY}}" \
  "{{MEMBERS_URL}}/api/products/{{COURSE_ID}}/lessons"
```
Se a escola estiver vazia, esta terceira vale como 404 em curso inexistente e o agente pula: o que importa é 200 nas duas primeiras.

O script `assets/checar_conexao.sh` roda as duas primeiras e devolve exit 0 quando está tudo certo.

## O que cada código de resposta significa aqui

| Código | Causa | Conserto |
|---|---|---|
| 400 sem chave | O cabeçalho `x-api-key` não foi mandado | Confere se o `.env` foi lido |
| 401 | A chave não existe naquela instalação | Rodar `gerar_chave_api.sh --rotacionar` na VPS |
| 404 domínio não encontrado | O endereço em `MEMBERS_URL` não bate com o domínio cadastrado | Confere o endereço com o dono |
| Sem resposta, tempo esgotado | A instalação está fora do ar | `diagnostico.md`, bloco "A página está fora do ar" |

## O mapa da instância, guardado uma vez

Depois do teste passar, o agente monta e guarda uma nota do projeto com:

- o `productId` de cada curso existente, guardado internamente como `COURSE_ID`, e se está publicado;
- o `sectionId` de cada seção de cada curso;
- o `planId` do plano gratuito de cada curso, se existir;
- o e-mail do dono, que é o dono da escola e o único usuário com poder total.

Sem esse mapa, toda conversa começa com uma varredura de chamadas que podia não acontecer. Com ele, "sobe essa aula no módulo 2" vira uma chamada só.

## O que ainda obriga painel

Criar chave não obriga mais: o script da instalação faz isso. O que sobrou de painel nesta versão é o nome da escola, o subtítulo e o tema de cores, que a API não expõe. A frase exata pro dono está em `personalizar.md`.

O instalador já gera a chave sem intervenção do dono. Nome da escola, subtítulo, tema e logo continuam no painel porque a API pública não expõe a configuração global. O envio de capa e imagem de aula usa a API local descrita em `personalizar.md`.
