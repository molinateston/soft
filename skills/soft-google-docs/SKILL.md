---
name: soft-google-docs
description: >-
  Publica um documento em Markdown como Google Doc nativo e bem formatado (títulos reais, tabela nativa, listas, checklist), na conta Google do usuário, e devolve o link pronto de abrir. Âncora: o texto JÁ EXISTE em .md e só falta virar Doc. Use quando o pedido for: "joga isso no Google Docs", "quero esse doc no Drive", "manda o link do Google Doc", "transforma esse md em documento", "sobe o ebook pro Drive", "publica o relatório como Doc", "atualiza aquele Doc que você fez", "o Doc saiu com ## na tela", "em que pasta do Drive isso vai". NÃO use pra: escrever o conteúdo do documento, que é da skill do formato pedido; construir site, painel ou sistema (soft-sistema); faxina de disco no servidor (soft-organizacao-vps); a apostila de uma gravação (soft-apostila); deck ou apresentação (soft-apresentacao); gerar arquivo de Word, planilha ou PDF no disco em vez de Doc no Drive (soft-exportar-documentos). Leia e siga o fluxo inteiro do SKILL.md.
---

# Publicar um Google Doc nativo a partir de Markdown

Esta skill pega um arquivo `.md` pronto e devolve um **Google Doc nativo**, com título, cabeçalhos indexáveis, negrito, tabela de verdade e checklist, mais o link para o usuário abrir e editar. O resultado é sempre um endereço `docs.google.com` funcionando, ou, quando o ambiente não tem a ferramenta, um `.html` pronto para o usuário subir em dois cliques. Nunca um bloco com `##` e `**` aparecendo na tela.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. **Quando o `.md` que virou Doc veio de outra skill, o comando acrescenta `--fonte <arquivo de origem>`:** marcador longo, número, nome e cabeçalho idênticos à fonte saem como `achado na fonte`, fora do exit, e só o que esta conversão introduziu reprova. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício de ponta a ponta: o pedido do usuário, a pergunta que a skill fez sobre a pasta, o retorno bruto da ferramenta com o campo que interessa, a verificação e a mensagem final com o link. Ler antes economiza uma rodada.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md`. Por ser uma skill de publicação de arquivo, valem sempre a parte 1 (pergunta o modo) e a parte 4 (oferece refinar); ensinar o porquê e puxar o bruto não se aplicam aqui, o insumo já vem pronto.

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o Markdown e diz onde salvar e eu publico o Doc). Se quiser ser guiado passo a passo (te pergunto o Markdown, a pasta de destino e o título, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra publicação com o Markdown e o destino que o dono colou. Se faltar o insumo que a publicação não vive sem (o conteúdo, ou a pasta de destino), pergunta AQUELE insumo e segue.
- **Modo guiado**: só quando o dono pede explicitamente. Pergunta o Markdown, o destino e o título uma coisa de cada vez, e publica com o que o dono for dando.

**Oferece refinar no fim (parte 4):** depois de mandar o link, fecha com UMA linha: "Quer que eu ajuste o título, mova de pasta, ou atualize o mesmo Doc com uma nova versão? Me diz que eu refaço." A oferta de refino não substitui o gate de qualidade.


## Roteamento por pedido

| O usuário pediu | Ação |
|---|---|
| "sobe isso pro Drive", "quero como Google Doc", "manda o link", primeira publicação de um conteúdo | **Ação 1 · PUBLICAR** |
| "atualiza aquele Doc", "mudei o texto, sobe de novo", "regera o documento" | **Ação 2 · ATUALIZAR** |

Pedido ambíguo ("cuida desse doc aí"): pergunte uma coisa só, se é a primeira vez que esse conteúdo vai pro Drive ou se já existe um Doc dele, e siga pela resposta.

---

## Ação 1 · PUBLICAR (Markdown vira Doc nativo)

**O que faz:** converte o `.md` em HTML e sobe como Google Doc nativo na pasta certa do Drive, devolvendo o link verificado.

**Precisa de:** o arquivo `.md` com o conteúdo pronto (do pedido do usuário, ou da etapa anterior de outra skill) · o nome que o documento terá no Drive · o identificador da pasta de destino.

**Sem o insumo:** conteúdo faltando, peça o arquivo ou o texto em uma pergunta só. Nome faltando, use o título `#` do próprio Markdown e diga em uma linha que assumiu isso. **Pasta faltando, resolva assim, nesta ordem:** (1) pergunte "em que pasta do Drive?" e aceite o link da pasta que o usuário colar, o identificador é o trecho depois de `/folders/` na URL; (2) sem resposta, liste as pastas da raiz e ofereça as três mais prováveis pelo nome; (3) se nem isso, crie uma pasta com o nome do projeto e avise em uma linha qual foi. Nunca deixe subir sem pasta declarada, o arquivo cai na raiz do Drive e o usuário não acha depois.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**O `[A CONFIRMAR]` do documento NUNCA vai inline pro corpo que vira Doc.** O texto que sobe pro Drive é lido por um terceiro (a lead que baixou o guia): pendência inline aparece no meio da frase que essa pessoa lê. Antes de publicar, `grep -nE '\[A CONFIRMAR' <doc>`, e cada marcador do corpo vira uma linha da caixa **"Falta você me responder"**, no topo do `PEDIDO-PARA-QUEM-PUBLICA.md`, escrita como pergunta em português; no corpo, ou a frase é reescrita na versão que dispensa o dado, ou o campo fica no fim da linha em posição de campo (link, número, data), nunca no miolo. **H1 herdado não é rótulo:** quando o `.md` vem de outra skill, o H1 (por exemplo `# Régua de nutrição ...`) é conteúdo daquela peça, não o nome de uma etapa do gate; o `--conferir` roda com `--fonte <arquivo de origem>` e o cabeçalho idêntico à fonte sai como `achado na fonte`, fora do exit. Trocar a palavra do H1 herdado seria reescrever a peça de origem, fora do que esta skill faz.

**Entrega:** o link cru `https://docs.google.com/document/d/<ID>/edit` na mensagem (link cru, nunca em formato markdown de link), mais o `.md` e o `.html` salvos em disco com o mesmo nome-base. Quando a ferramenta não existir no ambiente, a entrega é o `.html` mais o caminho manual descrito abaixo.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

**Leia primeiro:** `references/formato-saida.md` (a tabela de cada elemento de Markdown e como ele cai no Doc).

**Profundidade:** `scripts/md2doc.sh` (faz os três passos numa chamada só e imprime o link).

### Passo 1. Cheque o que o ambiente tem

Rode no shell, quando o ambiente permitir:

```bash
command -v gog     # ferramenta de linha de comando do Drive/Docs, já autenticada na conta do usuário
command -v pandoc  # conversor de Markdown para HTML
```

- **As duas existem:** siga os passos 2 a 5, o caminho completo.
- **Só o conversor existe:** gere o `.html`, entregue o arquivo e explique o caminho de dois cliques: abrir o Drive, "Novo > Upload de arquivo", subir o `.html`, clicar com o botão direito e escolher "Abrir com > Google Docs". A formatação chega intacta.
- **Nenhuma das duas existe:** entregue o `.md` no formato canônico do passo 3 e explique que colar Markdown direto no Doc não funciona (sai `##` e `**` na tela). Ou o usuário instala o conversor (`pandoc arquivo.md -t html -o arquivo.html`) e sobe o HTML, ou usa um conversor de Markdown para Docs da preferência dele.

Nunca diga que subiu o Doc quando a ferramenta não existe. Entregue o arquivo e o caminho.

**Ferramenta ausente e conta desconectada são diagnósticos diferentes, e a remediação também.** Confundir os dois manda o dono reconectar uma conta quando o que falta é instalar o programa, e ele perde a tarde no lugar errado. **Cole a saída literal de `command -v gog`** no relatório, com o código de saída:

**`command -v` sozinho não basta, porque o PATH muda com o usuário.** A ferramenta costuma ser instalada no diretório pessoal de quem opera o agente, e um shell de outro usuário (root, um serviço, um runner) não enxerga esse diretório. Diagnosticar "não está instalada" a partir do PATH errado já aconteceu nos dois sentidos e manda o dono instalar o que já existe. Rode o bloco inteiro e **cole as três saídas**:

```bash
whoami                                  # declara de qual usuário o teste saiu
command -v gog; echo "exit=$?"          # o que o PATH deste usuário enxerga
ls -l ~/.local/bin/gog 2>&1             # o caminho pessoal conhecido, mesmo fora do PATH
```

- **Exit zero em qualquer uma das duas últimas linhas:** a ferramenta **existe**. Use o caminho que apareceu (chame pelo caminho completo se ele não está no PATH) e só **depois disso** é que erro de credencial vira diagnóstico de conta. Nesse caso, cole também a mensagem de erro literal que o comando devolveu.
- **Exit diferente de zero nas duas:** a ferramenta **não está instalada** para este usuário. A mensagem ao dono é "falta instalar", nunca "falta conectar a conta", e vem acompanhada do `whoami`, porque o dono pode estar operando com outro usuário. Não descreva erro de credencial, porque não houve tentativa de autenticar: não existe binário pra tentar.

**Quando as três linhas falham, falta ainda uma checagem: o PATH é por usuário, mas o binário é de alguém.** O agente pode estar rodando com um usuário administrativo enquanto a ferramenta vive no diretório pessoal do usuário que opera o ambiente. Antes de concluir ausência, rode também:

```bash
sudo -u <usuário do ambiente> bash -lc 'command -v gog'   # o PATH do dono do ambiente
ls -l "$(sudo -u <usuário do ambiente> bash -lc 'command -v gog')" 2>&1
```

e cole as duas saídas. **Concluir "ferramenta ausente" sem essa segunda checagem é diagnóstico incompleto** e manda o dono instalar o que ele já tem.

Checagem verificável antes de fechar: as três linhas (`whoami`, `command -v` com exit, e o `ls -l` do caminho pessoal) estão coladas no relatório, mais as duas linhas da checagem entre usuários quando as três primeiras falharam, e o diagnóstico que você escreveu corresponde ao que elas mostraram juntas. Concluir ausência a partir de uma linha só reprova o relatório, mesmo que o arquivo entregue esteja certo.

### Passo 2. Prepare o conteúdo no formato canônico

O documento nasce em Markdown, vira HTML, sobe como Doc. O que sempre entra num entregável:

- `#` título, `##` e `###` seções e subseções, que viram Título e Cabeçalho 1 e 2 reais, indexáveis no sumário
- `**negrito**` e `*itálico*` para ênfase (nunca caixa alta como ênfase)
- tabela em Markdown com `|` para qualquer dado comparável, que vira tabela nativa e não texto
- `-` lista e `1.` lista numerada; `- [ ]` e `- [x]` para checklist
- crase para trecho literal e bloco de código com três crases para comando
- `---` linha divisória entre grandes blocos
- densidade: cada seção com título próprio, sem "título seguido de um bloco único de texto"

A tabela completa de cada elemento está em `references/formato-saida.md`.

**Este passo é obrigatório e CONTADO, nunca pulado.** Antes de rodar o conversor, abra o `.md` de origem e converta ao canônico o que não estiver: cerca de crase que na verdade era checklist vira `- [ ]`, cerca que era dado comparável vira tabela, bloco monoespaçado que era lista vira lista. É esse passo que separa um Doc com caixinha clicável de um Doc com um bloco de código cinza no lugar da checklist. **Checagem antes de fechar: no `.html` gerado, conte `<table>`, `<li>` e `input type="checkbox"` e cole os três números no relatório**, nesta forma: `<table>: N · <li>: N · input checkbox: N`. **Zero nos três, num documento cuja fonte tem lista, tabela ou checklist, reprova a conversão** e manda voltar pra este passo.

**Normalizar não é reescrever, e a prova é o `diff`.** A linha de fechamento do inventário **é** normalização autorizada, e é a única adição de conteúdo permitida ao documento do dono: última linha, em itálico, no máximo 2 linhas. O `diff` do Passo 3 a lista à parte, sob o rótulo `adição autorizada: rodapé de inventário`. **Documento sem essa linha reprova; documento com qualquer outra linha adicionada reprova.** Fora ela, a única alteração autorizada no `.md` de origem é a normalização de formato deste passo. **Acrescentar seção nova ao documento do dono é proibido**, inclusive seção de auditoria, de rastreabilidade, de proveniência ou de fim de documento: o dono pediu o documento, não a auditoria dele. Toda alteração entra no relatório como `linha N: <antes> → <depois>`. **Checagem verificável: rode `diff <fonte> <entrega>` e cole a saída no relatório.** Diff com linhas adicionadas que não sejam normalização de formato reprova a entrega e manda regravar a partir da fonte.

### Passo 3. Converta e suba

```bash
# carrega as variáveis de ambiente do agente, se houver (traz as credenciais da ferramenta)
set -a; . ./.env 2>/dev/null; set +a
GOG="${GOG:-$(command -v gog)}"
[ -n "$GOG" ] || echo "ferramenta ausente: entregue o .html/.md e explique a conversão manual"

# Markdown vira HTML
pandoc doc.md -f markdown -t html -o doc.html

# HTML vira Google Doc nativo, na pasta escolhida
$GOG drive upload doc.html --name "Nome do Documento" --convert-to doc --parent <ID_DA_PASTA> -j
```

Atalho: `scripts/md2doc.sh doc.md "Nome" <ID_DA_PASTA>` faz os três passos e imprime o link.

### Passo 4. Extraia o link do retorno

A opção `-j` devolve JSON. O campo que interessa é o `id`. O retorno tem esta forma:

```json
{"id":"1aZk9QpLmN3vX7bR2sT8yUwE4cVhGjKdF","name":"Nome do Documento","mimeType":"application/vnd.google-apps.document","parents":["1BcD3fG5hJ7kL9mN"],"webViewLink":"https://docs.google.com/document/d/1aZk9QpLmN3vX7bR2sT8yUwE4cVhGjKdF/edit"}
```

Pegue o `id` e monte a URL: `https://docs.google.com/document/d/<ID>/edit`. Mande o endereço cru, nunca embrulhado em sintaxe de link, porque em vários mensageiros o link embrulhado chega quebrado.

### Passo 5. Prove antes de dizer "pronto"

Baixe o conteúdo de volta e confira que não veio vazio:

```bash
$GOG drive download <ID> --output check.txt --format txt && wc -c check.txt
```

O arquivo tem que existir com tamanho maior que zero, e o texto tem que bater com o que você escreveu. "Subi o Doc" sem esse download de volta é `[NÃO VERIFICADO]`.

---

## Ação 2 · ATUALIZAR um Doc que já existe

**O que faz:** publica a versão nova do conteúdo e aposenta a anterior sem apagar nada.

**Precisa de:** o `.md` atualizado · o link ou o identificador do Doc antigo · a mesma pasta de destino.

**Sem o insumo:** identificador do Doc antigo faltando, procure pelo nome no Drive (`$GOG drive list --query "name contains 'Nome'"`) e confirme com o usuário qual dos resultados é o certo antes de mexer. Se não achar, trate como Ação 1 e avise em uma linha que criou um documento novo.

**Entrega:** o link cru do Doc novo, mais uma linha dizendo que o antigo foi renomeado e continua no Drive.

**Leia primeiro:** `references/formato-saida.md`.

Um Google Doc nativo **não troca o conteúdo mantendo o mesmo link**: a conversão só acontece na criação. Então o caminho é:

1. Gere um Doc novo pela Ação 1, na mesma pasta.
2. No Drive, renomeie o antigo para `[SUBSTITUIDO AAAA-MM-DD] <nome>`. Não apague, espere o usuário confirmar.
3. Diga ao usuário, em uma linha, qual link vale agora.

Caso real de referência: o usuário pediu a segunda versão de um plano de 12 páginas. O antigo virou `[SUBSTITUIDO 2026-08-14] Plano Trimestral`, o novo subiu com o mesmo nome limpo, e a mensagem final trouxe só o link novo mais a frase "o anterior continua no Drive, renomeado, caso queira comparar".

---

## Gate de qualidade (antes de mandar o link)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **O inventário varre o perfil do dono INTEIRO, não só os campos que esta entrega consumiu:** cada campo do perfil é uma linha, e campo com vários valores (paleta com 3 cores; oferta com preço, parcela, bônus e garantia) rende uma linha por valor. **Entrega cujo `Dados fornecidos: N` for menor que o número de campos do perfil recebido reprova sem análise de conteúdo.** Qualificar a linha ("relevantes ao objeto", "considerados para esta entrega") também reprova: o total é o total. **Onde a linha mora:** no arquivo que o dono lê. Quando a entrega é uma peça de copy publicável (headline, carrossel, slide, card, chat, roteiro, deck), a peça NÃO recebe a tabela: a tabela vai num arquivo irmão de handoff (`HANDOFF-<slug>.md`) e só a linha de fechamento fica na peça, no rodapé. Inventário só no relato de processo, sem a linha na entrega nem o handoff no disco, reprova.

**Onde a linha mora NESTA skill (regra específica, vence a geral acima).** Esta skill publica documento do dono, então o documento publicado recebe **apenas a linha de fechamento**, em nota de rodapé de no máximo 2 linhas. **A tabela item a item fica no RELATO, nunca no documento.** Anexar a tabela ao documento do dono infla o entregável e reprova: o dono pediu a régua, não a auditoria dela. Checagem colada: `bytes da fonte: N · bytes da entrega: N · linhas adicionadas pelo inventário: 1 a 2 (a linha de fechamento, autorizada)`. Zero linhas também reprova: o documento tem que sair com a linha.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


Confira em silêncio, e só então entregue:

1. **Doc verificado.** O download de volta rodou e o arquivo veio com conteúdo. Sem isso, a entrega sai marcada `[NÃO VERIFICADO]`.
2. **Sem Markdown cru na tela.** Abriu o Doc (ou o texto baixado) e não tem `##` nem `**` literais.
3. **Estrutura de verdade.** Cabeçalhos viraram Título e Cabeçalho, tabelas viraram tabela nativa, listas viraram lista.
4. **Link cru.** O endereço vai puro na mensagem, sem sintaxe de link em volta.
5. **Pasta declarada.** O documento está na pasta que o usuário indicou, ou na que você criou e nomeou para ele.
6. **Nada inventado.** Se algum passo não rodou no ambiente, isso está dito, não maquiado.
7. **`diff` colado.** A saída de `diff <fonte> <entrega>` está no relatório, e as únicas linhas alteradas são normalização de formato do Passo 2 mais a linha de fechamento do inventário, listada à parte sob o rótulo `adição autorizada: rodapé de inventário`. Diff com seção nova reprova.
8. **Contagem da conversão colada.** As três linhas `<table>: N · <li>: N · input checkbox: N` estão no relatório, medidas no `.html` gerado, e não são zero quando a fonte tem lista, tabela ou checklist.
9. **Inventário no lugar certo.** Só a linha de fechamento no documento, em nota de rodapé de até 2 linhas, e ela é obrigatória: documento sem ela reprova. A tabela item a item fica no relato. `bytes da fonte` e `bytes da entrega` colados lado a lado.
10. **Pasta de saída limpa.** Nenhum log do motor, arquivo temporário ou sobra de execução ficou na pasta de entrega junto do documento.

## O que esta skill NÃO faz

- **Escrever o conteúdo do documento.** Esta skill publica o que já existe. Quem produz o texto é a skill do assunto (copy, plano, relatório). Se nenhuma outra estiver disponível, escreva aqui o mínimo necessário e diga em uma linha que a versão completa pede a skill do assunto.
- **PDF.** Converta o Doc para PDF pelo próprio Drive depois de publicado.
- **Site ou página publicada** → `soft-sistema`. Se não estiver instalada, entregue o `.html` e explique onde hospedar.
- **Planilha e apresentação.** O caminho é outro, esta skill trata documento de texto.
- **Importar ferramentas de terceiro que pedem escopo de e-mail, contatos ou Drive inteiro.** A ferramenta padrão já resolve com a conta que o usuário configurou, sem essa superfície de risco.

## Quem chama esta skill

Qualquer skill que produza um `.md` de entrega e o usuário queira o resultado no Drive. As mais frequentes: `soft-plano-negocio`, `soft-negocio-metricas`, `soft-gestao-agil`, `soft-financeiro`, `soft-apostila`. O circuito é sempre o mesmo: a outra skill gera o `.md` e para, esta skill recebe o caminho do arquivo e publica.

## O dono nunca recebe comando (regra dura desta skill)

Quando a publicação ou a instalação não sair, a PRIMEIRA linha do relato diz o que aconteceu e o que pedir, em português, sem nome de comando: "não consegui publicar porque a conta do Drive não está conectada; me manda o acesso que eu publico" vale, e "rode `gog drive upload`" não vale. O dono opera pelo aplicativo de mensagem e não abre terminal.

Nesse caso a entrega sai com duas coisas, sempre as duas:
1. **O arquivo pronto**, no formato final, do jeito que ele seria publicado.
2. **`PEDIDO-PARA-QUEM-PUBLICA.md`**, o passo a passo escrito pra TERCEIRO (quem cuida do site, do Drive ou do servidor): o que abrir, onde colar, o que conferir depois, e a quem devolver o link. Escrito pra pessoa, não pro terminal: o comando, quando existir, mora dentro de bloco de código nesse arquivo, com uma linha em português dizendo o que ele faz.

**O arquivo pra quem publica não tem terminal, e abre pelo cabeçalho de 3 linhas.** O `PEDIDO-PARA-QUEM-PUBLICA.md` abre com as 3 linhas pro dono, nesta ordem, ANTES de qualquer outra coisa: `O que é este arquivo:` · `Pra quem mandar:` · `O que essa pessoa vai fazer:`. Só depois vem `Não publiquei porque <motivo em português>` e os passos de mouse: abrir a pasta, arrastar o arquivo, clicar. Nenhuma linha de comando (`pandoc`, `gog`, `npx`, `python3`, bloco cercado). **As pendências de conteúdo viram a caixa "Falta você me responder", logo depois do cabeçalho:** cada `[A CONFIRMAR]` do documento vira uma pergunta em português aqui, e sai do corpo que vira Doc. Cole a checagem: rode `grep -nE '```|gog |pandoc |npx |python3 ' <arquivo pra quem publica>` e cole a saída; qualquer linha encontrada reprova.

**O arquivo pra quem publica abre com 3 linhas pro dono.** As 3 linhas endereçam o dono antes de tudo: `O que é este arquivo`, `Pra quem mandar`, `O que essa pessoa vai fazer`. Só com esse cabeçalho os passos DENTRO dele ficam isentos do gate de comando ao dono, porque o script já trata assim. O `RELATO` nunca carrega comando.

O relato fecha com a seção `Perguntas pra você`, e a pergunta do acesso entra ali escrita como pergunta.

---

## Falhas comuns

| Sintoma | Causa | Ação |
|---|---|---|
| O Doc abriu com `##` e `**` na tela | Markdown colado direto, sem passar pelo conversor | Refaça pelo passo 3, sempre via HTML |
| A ferramenta respondeu erro de credencial ou pediu login | Autenticação expirada ou ausente na conta configurada | Não tente contornar nem peça chave nova. Diga ao usuário que a conta do Drive precisa ser reconectada no ambiente dele, e entregue o `.html` enquanto isso |
| O Doc subiu mas ninguém acha no Drive | Faltou a pasta de destino, caiu na raiz | Mova para a pasta certa e mande o link de novo |
| O link chegou quebrado no mensageiro | Endereço embrulhado em sintaxe de link | Reenvie o endereço cru |
| O download de volta veio vazio | A conversão falhou em silêncio | Refaça a subida e verifique de novo antes de anunciar |

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
