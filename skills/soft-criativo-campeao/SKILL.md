---
name: soft-criativo-campeao
description: >-
  Porta de entrada da tarefa ANUNCIAR: entrega ângulo, peças (lote de arte com texto do anúncio, roteiro de vídeo com instrução de edição) e plano de teste mínimo (verba pelo ticket, fases, quando matar e escalar). Âncora: pedido de anúncio ou de criativo = aqui; verba, conta e métrica de campanha = soft-trafego-meta. Use quando o pedido for: "quero anunciar", "anúncio", "criativo", "faz meus anúncios", "anúncio pro perpétuo", "anúncio pra VSL", "faz os criativos do anúncio", "preciso de 4 artes pra campanha", "roteiro do anúncio em vídeo", "qual o ângulo das peças", "por que o criativo não vende". NÃO use pra: quanto de verba pôr, subir campanha, métrica da conta, pausar ou escalar (soft-trafego-meta); peça avulsa ou banner (soft-designer); headline isolada (soft-conteudo-headlines); reel curto (soft-reel-7seg); editar vídeo gravado (soft-editor-video); roteiro de VSL (soft-funil-vsl); espionar ou desmontar anúncio de concorrente (soft-espiao). Leia e siga o fluxo inteiro do SKILL.md.
---

# Criativo campeão: do ângulo ao pixel

Esta skill entrega um LOTE de criativos de anúncio prontos pra subir. Ela decide o ângulo de cada peça, fixa a identidade da marca num arquivo, renderiza em lote e valida antes de virar campanha.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. A mensagem ao dono segue a seção "Mensagem ao dono"; o relato de processo abre com `Pronto:`, `Abra primeiro:` e `Falta você responder:` e fecha com `Perguntas pra você`. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**O render NUNCA aplica caixa alta na headline.** `text-transform: uppercase` não alcança manchete, capa, título de slide ou de card, nem texto grande lido como a frase da peça: ênfase é por palavra. Caixa alta e versalete só em tag ou etiqueta (`.slide-label`, `.tag`), rótulo de rodapé e cabeçalho pequeno de topo, até 16px. Antes de exportar, cole `regras de caixa alta no render: N · alcançando a manchete: 0`; o `checar_titulos.py --render <arquivo.html>` e o `--conferir` reprovam com `título em caixa alta: <linha>`.

**Os arquivos que cada ação exige (`--exige`).** Conferência: `--conferir <pasta> --exige <lista>`. Lote de criativos: `--exige manifesto.json,copy-lote.md,identidade.json`; matriz: `--exige matriz-criativos.md`; identidade: `--exige identidade.json`; pacote: as três somadas; tarefa de anunciar (Ação 0): `--exige manifesto.json,copy-lote.md,identidade.json,plano-de-teste.md`, mais `roteiro-video-*.md` quando `tipo no teste: vídeo`. Em toda ação some `conferencia/mensagem-dono.txt`, e no lote e na Ação 0 some `conferencia/material-do-dono.txt`. Arquivo ausente sai com exit 1.

**O gate de conteúdo manda sobre toda regra de conversão.** Número `[A CONFIRMAR]`, nome de conversa privada, promessa proibida, ressalva e marcador (seção "Gate de qualidade") vencem a ponte com o destino, o termo-gancho, o ângulo tirado da copy do dono, a razão de agir agora e o uso completo dos dados. Material do dono (anúncio atual, VSL, página, comentário) é fonte de termo e de cena, nunca de promessa: prazo de resultado, ganho, cura ou antes e depois que já estão nele não passam pra copy nova; a mensagem aponta o risco em 1 linha e a peça sai na versão segura. Prova entra só com o que ela diz ao pé da letra ("23 depoimentos em vídeo" não vira "23 alunas conseguiram X"), e cena, cidade, idade ou frase de material sem autorização não viram gancho nem passam pra outra prova. Quando uma regra de conversão pede o que o gate barra, cole em `conferencia/` a linha `barrado pelo gate: <o quê> · regra: <qual>`.

**Pedido que nomeia evento, turma ou data: ao menos uma peça carrega a razão de agir agora.** Rode `grep -niE 'turma|vagas|come[çc]a|aula ao vivo|[0-9]{2}/[0-9]{2}' <perfil>` e cole a saída. O que voltar entra em pelo menos uma peça, com o número literal. Cole `peças no lote: N · com razão de agir agora: N`, e zero na segunda coluna, num pedido que nomeia turma ou evento, reprova o lote.

**Todo campo preenchido do JSON de identidade carrega a origem no próprio arquivo.** Some um objeto `origens` com uma entrada por campo preenchido, no formato `"<campo>": "<arquivo>:<linha>"`. Campo com valor e sem entrada em `origens` reprova, inclusive `@` de perfil, texto de selo e CTA. Cole `campos preenchidos: N · com origem apontada: N`, iguais. `null` com pendência declarada é resultado correto e dispensa origem.

**A conclusão nasce da saída do grep, e negar a saída colada reprova.** Depois de colar a saída, escreva uma linha por ocorrência: `<arquivo:linha> | ação: <verbo> | palavra: <literal> | usada? sim/não · porque: <motivo>`. **Conclusão negativa só é válida com a saída vazia**, e o `--conferir` sai com exit 1 e `conclusão contradiz a saída do grep` quando a peça diz `palavra-chave: nenhuma` com ocorrência colada na mesma checagem.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Capacidade negada no perfil é fato, nunca lacuna a interpretar.** Antes de escolher a mecânica do CTA, rode `grep -in 'automação\|automacao\|robô\|bot' <perfil do dono>` e cole a saída literal. Linha que diz `nenhuma automação` responde `não`, e ela não é omissão nem falso positivo a contornar. Cole `mecânica exige automação? sim/não · perfil declara: <a linha literal> · mecânica adaptada: <qual>`. Negação no perfil sai como CTA sem robô, e manter a mecânica por leitura funcional, herança de outra plataforma ou hábito presumido reprova a peça.

**O universo da R3 é o das unidades produzidas, nunca o dos pilares.** As `teses distintas` saem das pautas, headlines ou frames que a peça entrega, e a contagem igual ao número de pilares do dono é resultado inválido. Cole `unidades no lote: N · linhas em teses.txt: N`, os dois iguais, e só então a matriz de pares.

**`teses.txt` é arquivo obrigatório da pasta de saída**, uma tese de até 4 palavras por linha, ao lado do `conferencia/checagem-titulos.md`. Sem ele o gate não calcula a R3 e o campo do fecho sai com a instrução do script no lugar do número, o que reprova a entrega.

**Regra de ouro:** a peça não começa no editor de imagem, começa na DOR. Quem pesa mais no custo depende da campanha: **se o público foi escolhido à mão** (interesse, semelhante), o público decide mais que a arte e o diagnóstico começa nele (Ação 3); **se o público é aberto**, a plataforma entrega pelo criativo e o diagnóstico começa na peça (Ação 4).

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um lote fictício de 4 peças, do briefing às artes, e no fim a Ação 0 inteira (as 3 listas do passo 1, a ponte com a VSL, o roteiro e o plano de teste). Ler antes economiza uma rodada de retrabalho.

**O perfil do dono vem do banco do agente.** Onde a skill precisar de voz, avatar, dor, prova, cor, fonte ou @perfil: leia do perfil/brain do agente quando existir; se não existir, passe pela triagem (seção "A condução") e siga com o que faltar marcado `[A CONFIRMAR]`. Nunca invente, nunca pare por causa disso.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz (padrão em `references/09-conducao-agente.md`). **O modo direto é o padrão e não se anuncia na mensagem**; o guiado, uma pergunta por mensagem, só roda quando o dono pede ("me guia", "passo a passo").

**Triagem antes de produzir (vale pra toda ação).** Leia primeiro o perfil, o pedido e os insumos; o que eles respondem não vira pergunta. O que falta cai em dois grupos. **(a) Muda a peça ou o risco:** o destino do clique, a dor do comprador quando nada a diz, a prova que a peça usaria e está sem número ou sem autorização registrada, a promessa que o pedido quer e não tem lastro. **(b) Não muda a peça:** caixa de teste, idade da conta, cor, fonte, selo, @, URL, evento de conversão, ordem das peças, a foto (sem ela o render espera, e a copy sai). Com item em (a): UMA mensagem antes de produzir, no máximo 3 itens numerados, cada um dizendo o que muda com a resposta, fechando com "responde o que souber, o resto eu marco"; item de (b) só entra se couber nos 3, e nessa rodada não sai lote. Sem item em (a): produza, cada item de (b) sai `[A CONFIRMAR: o quê]` com a premissa declarada em 1 linha, e as perguntas vão junto da entrega, no máximo 3 (cor, fonte, selo e @ são uma pergunta só). Promessa proibida (prazo de resultado, cura, ganho garantido, antes e depois) nunca vira pergunta: sai na versão segura, pelo gate.

- **Ensina enquanto faz:** ao escolher o ângulo de cada peça, escreve UMA linha do porquê ao lado dela no `copy-lote.md` ("ataca a objeção de preço porque é aí que o teu público empaca"), pra o dono decidir sozinho na próxima.
- **Puxa o material bruto:** dor ou prova rasa ("meus clientes querem resultado") entra na triagem como item (a): "me conta de UM cliente, o que ele te falou quando te procurou, com as palavras dele?", ou o número/print que aconteceu.
- **Oferece refinar no fim:** a última pergunta da prévia é UMA linha de ajuste ("quer outro ângulo em uma delas? refaço só a peça que você pedir").

**Mensagem ao dono (chat e Telegram): no máximo 8 linhas, regra do gate.** Grave-a em `conferencia/mensagem-dono.txt` antes de enviar e cole `linhas da mensagem: N (teto 8)` com a saída de `grep -c . conferencia/mensagem-dono.txt`. Nesta ordem: (1) o que o dono decide primeiro, em 1 pergunta, a que segura o próximo passo (ou `Pode seguir: nada depende de você`); (2) `Pronto:` o que saiu e o único arquivo pra abrir, 1 linha; (3) até 3 linhas do que muda a decisão (a conta do diagnóstico, a premissa usada, o risco que ficou fora); (4) as outras perguntas, no máximo 2, numeradas, cada uma escrita uma vez. Nunca na mensagem: lista de arquivos, o que já está no arquivo (copy, porquê do ângulo, plano), nome de regra ou de script, lint, gate, checkpoint, o modo, a pasta `conferencia/`. O `--conferir` reprova acima de 8 linhas, com mais de 1 linha citando arquivo ou com nome de script ou de gate. No STOP do passo 2 vale o mesmo teto: os ganchos, uma linha cada e sem o porquê, a pergunta do STOP e as do grupo (b).

## Onde estou (os 3 ambientes: a mesma skill, entrega diferente)

Descubra o ambiente antes da primeira pergunta: rode `ls scripts/checar_titulos.py` a partir da pasta desta skill; respondeu, tem terminal. Sem ferramenta de comando, é só chat. É agente de conversa quando a mensagem do dono chegou por Telegram ou WhatsApp, ou quando o sistema do agente declara o canal.

| Ambiente | Tem terminal? | O que perguntar, nesta ordem | O que entrega |
|---|---|---|---|
| só chat | não | as perguntas da triagem da ação roteada, uma mensagem (destino com a 1ª frase, se for VSL ou página) | os arquivos da ação como blocos de markdown no chat, um bloco por arquivo com o nome no topo; `spec-render.md` no lugar do PNG; `plano-de-teste.md` com o passo a passo à mão |
| com terminal | sim | leia antes o perfil do dono e os insumos na pasta; a triagem pergunta só o que faltar | os arquivos gravados na pasta de trabalho, PNG renderizado, lint e `checar_titulos.py` rodados, com o caminho de cada arquivo na resposta |
| dentro de um agente de conversa | sim | igual ao terminal, numa mensagem só; áudio do dono vale como resposta | igual ao terminal; a resposta é a "Mensagem ao dono", com a prévia das peças como imagem |

**Precisa de terminal:** render em PNG, lint por código, extração de frame de vídeo, `checar_titulos.py`. **Sem terminal:** a spec de render no lugar do pixel, o lint no olho pela régua escrita (seção "Nome do arquivo e lint") e o plano de teste pra fazer à mão; a entrega sai do mesmo jeito e o relato declara o que ficou sem código.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Ação |
|---|---|
| "quero anunciar", "faz meus anúncios", "anúncio pro perpétuo", "anúncio pra VSL", "quero anúncio rodando essa semana", "anuncia meu produto" | **0 · ANUNCIAR** (a tarefa inteira: ângulo, peças e plano de teste) |
| "faz os criativos", "preciso de 4 artes pra campanha", "monta o lote", "renderiza as peças" | **1 · LOTE DE CRIATIVOS** (o caminho inteiro, passos 1 a 7) |
| "roteiro do anúncio em vídeo", "criativo em vídeo pra VSL", "o script do ad", "monta o lote de vídeo" | **1**, tipo de peça VÍDEO (ver `references/playbook-video-ads.md`) |
| "quantos criativos eu faço", "quando desisto da VSL", "o que varia primeiro", "esse criativo já validou?", "por que empacou na escala" | **4 · FÁBRICA E LEITURA DE MÉTRICA** |
| "qual o ângulo das peças", "que dor cada arte ataca", "só os ganchos por enquanto" | **1**, parando no STOP do passo 2 |
| "monta o playbook de criativo desse cliente", "replica o processo pro especialista novo", "quero o método pra outro nicho" | **2 · PLAYBOOK DE 4 CAMPOS** |
| "o criativo não vende", "CPL subiu, troco a arte?" | **3 · DIAGNÓSTICO PÚBLICO ANTES DE CRIATIVO** |
| "tem clique e não vende, faz criativo novo", pedido de peça nova com número da campanha atual | **0**, abrindo pelo diagnóstico do funil |
| "quanto ponho de verba", "sobe a campanha", "puxa a métrica da conta", "pausa ou escala essa" (sem pedir peça) | fora daqui: **soft-trafego-meta** |

Pedido ambíguo ("me ajuda com o criativo"): pergunte UMA coisa só, "você quer pôr anúncio no ar (peças e plano de teste), as peças renderizadas agora, o playbook pra clonar o processo, entender por que o criativo atual não rende, ou o vídeo e a fábrica em volta (quantos criativos, o que varia, leitura de métrica)?", mostre a tabela como cardápio e siga pela resposta.

---

## Ação 0 · ANUNCIAR (a tarefa inteira, porta de entrada)

**O que faz:** o dono diz "quero anunciar" e recebe tudo pra pôr anúncio no ar: ângulo, peças e plano de teste mínimo. Roda sozinha; as skills de apoio só aprofundam.

**Entrada: a triagem (seção "A condução"), com a lista desta ação.** (a) Muda a peça: o que vende e por quanto, se o perfil não diz; pra onde a pessoa vai ao clicar (VSL, página, checkout, cadastro gratuito ou direct) e, se VSL ou página, a 1ª frase dela; a prova que o pedido quer usar sem número ou sem autorização. (b) Vão juntas do STOP do passo 2: caixa de teste, conta com mais ou menos de 15 dias rodando, o anúncio que mais vendeu, e a foto se ainda falta. Na Ação 0 a entrevista "Sem o insumo" da Ação 1 não roda: dor e avatar saem do perfil ou da 1ª frase do destino; cor e fonte entram no padrão com `[A CONFIRMAR]`; URL e evento vão pro plano como `[A CONFIRMAR]`. Ticket sem resposta vira `[A CONFIRMAR: ticket]`, nunca número inventado.

**Pedido com número da campanha atual: diagnóstico do funil antes dos ângulos.** Faça a conta em 1 ou 2 linhas (clique → visualização da página → início de checkout → compra) e aponte a etapa com a maior perda. Perda depois do clique: diga sem rodeio que peça nova sozinha não resolve, dê a ordem do conserto (velocidade, topo da página casando com o gancho, preço e garantia visíveis, depois oferta) e entregue no máximo 2 peças que casam com a página consertada; o plano mede depois do conserto (`references/plano-de-teste.md`, seção 4). Perda no clique ou antes: siga o lote. **Parada obrigatória:** se o anúncio "parou" ou "caiu" mas clique, custo do clique e frequência ficaram parecidos, a causa está depois do clique ou no registro da venda (página, checkout, pixel). Nesta rodada NÃO gere lote, manifesto nem roteiro: entregue só a conta, a etapa suspeita e até 3 checagens pro dono (vendas no painel do checkout, compra de teste vendo o evento de compra, página aberta no celular), numa mensagem só. O lote sai depois da resposta.

**Tipo de peça pelo destino (regra, cole a escolha no plano).** Se o destino é VSL, a peça que escala é vídeo: teste o ângulo em lote de imagem, e o ângulo que passar vira roteiro. Página de venda: com vídeo na página, igual à VSL; sem vídeo, imagem no teste e na escala. Se é checkout direto de ticket até R$ 100, fique no estático (CPM menor). Cadastro gratuito ou direct: imagem primeiro, vídeo quando um ângulo validar. Cole `destino: <qual> · tipo no teste: <imagem/vídeo> · tipo na escala: <qual> · porquê: <1 linha>`.

**O fluxo:** (1) ângulos pelos passos 1 e 2 da Ação 1, com o STOP; (2) peças pelos passos 3 a 7, com texto e título do anúncio no manifesto; quando `tipo no teste: vídeo`, escreva `roteiro-video-<n>.md` depois de ler `references/playbook-video-ads.md`, seções 1, 2 e 9, e com bruto de gravação no insumo (VSL, aula, live) o roteiro corta do bruto antes de pedir gravação nova; com `tipo no teste: imagem`, NÃO escreva roteiro agora: o plano diz em 1 linha que ele nasce do ângulo que validar, pela Ação 1 tipo vídeo; (3) plano de teste: leia `references/plano-de-teste.md` inteiro e grave `plano-de-teste.md` na pasta, na forma da seção 8 dele.

**Entrega:** os arquivos da Ação 1 · `roteiro-video-<n>.md` quando houver vídeo · `plano-de-teste.md` (verba de teste pelo ticket, fases teste, pré-escala e escala, métricas pra matar cedo, quando escalar, quem sobe).

**Apoio, se instalado (confira na lista de skills do ambiente, ou com `ls` na pasta que contém esta skill, procurando `<nome-da-skill>/SKILL.md`):** soft-designer desenha a arte avulsa; soft-editor-video edita o vídeo a partir do roteiro e da instrução de edição; soft-trafego-meta sobe o plano na conta, tudo pausado; soft-funil-vsl recebe `gancho do anúncio: <frase>` quando falta a VSL ou um ângulo novo escala. Sem a skill de apoio, a peça ou o plano sai pronto pra fazer à mão, e nada para por falta dela.

---

## Ação 1 · LOTE DE CRIATIVOS (do ângulo ao arquivo)

**O que faz:** entrega um lote de artes de anúncio, cada uma nascida de um ângulo de dor diferente do mesmo avatar, com identidade da marca aplicada e copy aprovada no lint.

**Precisa de:** o avatar e as dores dele, do perfil/brain do agente · a foto real da autoridade, sempre pedida ao dono (arquivo ou pasta) · a identidade visual (cor, fonte, selo, CTA, @perfil, formato), do perfil/brain quando existir · o destino do anúncio (o tipo, a URL e o evento de conversão), perguntado ao dono; **se o destino é VSL ou página, peça também a primeira frase dela**, porque o termo-gancho das peças sai dali (passo 5).

**Sem o insumo:** a triagem (seção "A condução"): a dor, o destino e o que a pessoa ganha lá são do grupo (a); fotos, cor e fonte (preto e uma sem-serifa do sistema, marcadas `[A CONFIRMAR]`), URL e evento são do (b). Guiado, só a pedido: as mesmas perguntas, uma por vez. Sem foto real do dono, a copy, o manifesto e a spec saem e o render para até a foto chegar.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** na pasta de trabalho do lote, `identidade.json` (a marca), `manifesto.json` (uma entrada por peça), `copy-lote.md` (as linhas de texto, o arquivo que passa no lint), `out/` com as imagens renderizadas e `out/progress.json` (o checkpoint). Sem ferramenta de imagem no ambiente: `spec-render.md` com a especificação visual peça a peça, pro dono renderizar na ferramenta dele.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**O `out/progress.json` sai sempre, mesmo quando nada renderiza.** Quando o bloqueio de foto ou a falta de ferramenta de imagem impede o render, crie a pasta `out/` de verdade e grave o `progress.json` assim mesmo, com `"concluidas": []` e o motivo em `"bloqueio"`. Ele é o comprovante de que nada foi renderizado, e é o que separa "não rodou" de "rodou e não gravou". Checagem verificável antes de fechar: liste a pasta `out/` e confirme que ela existe no disco e que o `progress.json` está lá; nunca afirme que uma pasta foi criada sem listá-la, porque essa afirmação se confere em um comando.

**Leia primeiro:** `references/metodo-4-campos.md` (os 4 campos que sustentam qualquer lote) · `references/angulos-de-cpc.md` (o arsenal de 5 ângulos de CPC baixo, com a régua de lastro; no passo 1) · `references/EXEMPLO-FIM-A-FIM.md` (a forma da entrega). Anúncio em VÍDEO: no passo de roteiro, `references/playbook-video-ads.md`, seções 1, 2 e 9. Profundidade: `references/exemplo-preenchido.md`.

### Os 7 passos

**Passo 1 · ÂNGULO ANTES DA ARTE: 1 arte = 1 combinação.** A peça nasce de um gancho por ângulo de dor específico, nunca de "uma imagem bonita".

**Antes dos ganchos, a lista do material do dono.** Grave `conferencia/material-do-dono.txt`, um item concreto por linha: `<item literal> | tipo: número, lugar, caso, objeto ou frase | origem: <arquivo:linha> | autorização: <arquivo:linha> quando for de terceiro`. Entra o que está nos insumos: valor, prazo real de entrega, bairro ou cidade atendida, foto de trabalho feito, objeto do serviço, caso com número, frase de cliente com autorização registrada. Fica fora: o que você deduziu, o número `[A CONFIRMAR]` e caso, cena ou frase de terceiro sem autorização (esse vira papel, "uma cliente", sem detalhe que identifique). **Cada peça usa pelo menos 1 item da lista**, literal, no gancho, no sub ou no `texto_anuncio`; o gate continua mandando no item (número de resultado com prazo não vira promessa). Lista vazia vira item (a) da triagem: "me manda UM caso com número, o lugar que você atende ou uma foto de trabalho feito". Cole `peças no lote: N · com material do dono: N`, iguais.

Depois, 3 listas curtas: personas possíveis (não só a óbvia), elementos de curiosidade da oferta (o nome do mecanismo, o objeto, a cena) e dores do dia a dia de cada persona. Cada peça combina um item de cada lista e morde UMA dor; combinação repetida não entra. Comece pelos ângulos que a copy do dono já tem (a abertura da VSL, o mecanismo do problema, o da solução; o termo e a cena, nunca a promessa) e só depois os arriscados. Escreva 3 ou 4 ganchos. **As personas são de quem COMPRA:** a história do dono é autoridade, nunca a dor da peça, salvo quando o comprador vive a mesma coisa. Anúncio do dono que já vendeu dá o primeiro ângulo, e o plano marca aquele corpo na pré-escala. Cole uma linha por peça em `conferencia/`: `peça <n> | persona: <x> | curiosidade: <y> | dor: <z> | material: <item>`; nenhuma linha repete as três primeiras, e a dor repete no máximo uma vez no lote, com persona diferente.

**O arsenal de ângulos (CPC baixo).** A dor é o alvo; o ângulo escolhe COMO ela vira gancho: Falar sem dizer, Segmentação reversa, Storytelling com plot twist, O Patinho Feio e Trends virais. Quando usar cada um, exemplo e régua: `references/angulos-de-cpc.md`. **Régua de lastro (dura):** Patinho Feio e Plot Twist SÓ com verdade real (o porquê verdadeiro da inversão, a história que aconteceu); sem o fato na mão do dono, o gancho vira `[A CONFIRMAR]` e para ali. Trend ou viral: seção 5 de `angulos-de-cpc.md`, com o jeito usado colado. Peça modelada de anúncio de terceiro: seção 5 de `playbook-video-ads.md`, com a linha `modelagem:` colada; frase literal, história e personagem do original nunca entram. **O gancho nunca promete o que o corpo e o produto não entregam**; clickbait só como variação de peça já validada.

**Passo 2 · STOP.** Mostre os ganchos ao dono e pergunte: "esses 4 ângulos batem com o que dói no seu cliente? Corto algum, troco algum?" Só siga com o OK. Na Ação 0, esta mensagem leva também as perguntas do grupo (b) que ficaram (caixa de teste, idade da conta, anúncio que mais vendeu, a foto), no máximo 3 além da pergunta do STOP.

**Passo 3 · FOTO REAL DA AUTORIDADE: nunca banco de imagem.** Rosto real, tratado em preto e branco, com topo do cabelo e queixo dentro do quadro (como medir: `references/metodo-4-campos.md`, "Detalhe do render"). Cabeça cortada reprova a peça, sem exceção.

**Passo 4 · IDENTIDADE FIXADA NUM JSON.** Cor, fonte, selo, CTA, assinatura e formato saem do `identidade.json` na pasta de trabalho, nunca escritos no código (campos mínimos e exemplo: `references/metodo-4-campos.md`, "Detalhe do render").

**Identificador do dono nunca é deduzido.** O `@` de `assinatura`, o `selo` e o `cta` só entram literais quando vieram do dono, do perfil/brain ou do insumo dele; deduzir do nome do negócio, do domínio ou de outro material não vale. Sem origem, `"assinatura": "[A CONFIRMAR: @ do perfil]"` e o render para nesse campo.

**Cor descrita em palavra nunca vira valor exato.** Sem RGB dado pelo dono, o campo sai `"cor_acento": "[A CONFIRMAR: RGB de verde]"` e o render para nesse campo. `cor_fundo` é obrigatório sempre que o dono nomear a cor de fundo, mesmo em palavra. Número de cor e texto literal sem origem apontada em `origens` reprovam a entrega.

**Passo 5 · RENDER EM LOTE: o manifesto manda.** Monte o `manifesto.json`, uma entrada por peça, com `foto`, `gancho` (1ª linha), `sub` (opcional), `cta`, `texto_anuncio`, `titulo_anuncio` e `saida` (exemplo em `references/metodo-4-campos.md`, "Detalhe do render"). Texto e título passam pelo mesmo lint e pela régua de títulos. **Se o dono deu a primeira frase da VSL ou da página, o termo-gancho dela (o nome do mecanismo, a cena, o expert) entra literal no gancho ou no `texto_anuncio` de cada peça**, e a linha de congruência do gate vai colada logo depois de montar o manifesto. O termo passa, a promessa não: prazo, ganho ou cura da VSL ficam fora da peça. O manifesto é a única fonte da verdade do lote; nada de gancho digitado na mão na hora de renderizar.

**A chave `cta` é obrigatória em cada peça, com texto literal, e nunca é apagada pra passar no gate.** Com destino informado, o CTA leva a ele (checkout: comprar pelo link; VSL: assistir o vídeo; cadastro: garantir a vaga) e nunca manda pra outro canal. Sem destino, o texto vem, nesta ordem: (1) da ação que o dono já usa nos insumos, achada por `grep -rniE 'manda |chama |responde |comenta |envia ' <insumos>` com a saída colada; (2) da ação nativa da plataforma do anúncio; (3) do convite ao evento datado. Sem as três, sai a frase falada que dispensa botão (`me chama no Direct e eu te mando o link`), nunca um marcador e nunca a chave ausente. Antes de renderizar, rode e cole as duas saídas:

```
python3 -c "import json;d=json.load(open('manifesto.json'));print(len(d['pecas']))"
grep -c '"cta"' manifesto.json
```

Os dois números têm que ser iguais. Cole `CTAs no lote: N · com texto escrito: N · em marcador: 0 · ausentes: 0`, e qualquer linha diferente de zero nas duas últimas volta pro passo de escrita.

**Todo CTA diz O QUE o lead recebe ao agir, nunca só a palavra-chave (checagem que reprova).** A palavra-chave vem com o próximo passo concreto que o dono de fato entrega (aula, PDF, diagnóstico, link da turma); sem esse insumo, pergunte AQUELE dado, nunca invente o brinde. Antes de renderizar, escreva `peça <n> | palavra-chave: <literal> | recebe: <o que o lead ganha>`; peça com palavra-chave e sem `recebe` reprova o lote.

**A ressalva de resultado (o range clínico, o "resultados variam") entra UMA vez, no fim da ÚLTIMA peça do lote, depois do CTA dela.** Rode `grep -niE 'resultado.{0,20}(varia|individual|não.{0,3}garant)|resultados podem variar|cada caso' copy-lote.md` e confira que toda ocorrência cai no bloco da última peça. Cole `ressalvas no lote: N · na última peça: N · em peça do meio: 0`; a última coluna diferente de zero volta pro passo de escrita.

**Nome de terceiro nunca entra em pixel, e a pergunta da autorização vem antes do render.** Antes de renderizar, rode `grep -in 'autoriz' <perfil>`; sem uma linha do perfil autorizando o nome em peça pública, a arte sai com o papel (`uma aluna`) e a dúvida vai pro relato antes do render, porque perguntar num PNG já gerado não desfaz o PNG. `python3 scripts/checar_titulos.py --render <html> --perfil <perfil>` reprova nome sem autorização no HTML antes de exportar. Cole `nomes de terceiro na arte: 0 · autorizações citadas no perfil: N`.

**Nenhum card sai com marca d'água de teste na arte.** Antes de renderizar, rode e cole a saída:

```
grep -rniE 'teste|test|placeholder|sample|lorem|sintetico' <manifesto> <pasta de assets>
```

Frame de teste prova o pipeline e **nunca entra na peça entregue**: achado na saída, o frame sai do manifesto e a peça vira PARCIAL, sem render. Sem foto real, o card sai com tratamento de fundo declarado e sem imagem. Cole `cards com texto de teste na arte: 0`.

**O número colado é copiado da saída, não redigitado.** Redirecione a saída do contador pra um arquivo e cole o arquivo: `<comando do contador> > contagem.txt`, depois `cat contagem.txt` colado inteiro. Número redigitado que não reproduz reprova a contagem, mesmo quando o veredito é o certo.

**A varredura de imagem no disco roda antes de marcar PARCIAL.** Rode e cole a saída, inclusive vazia:

```
find <pasta de insumos> -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.mp4' -o -iname '*.mov'
```

**Vídeo conta como fonte:** havendo `.mp4` ou `.mov`, extraia os frames com `ffmpeg -i <video> -vf fps=1/4 -frames:v 4 frame-%02d.png` e use na peça. **Marcar PARCIAL sem a saída do find colada reprova a entrega.**

O render (foto tratada, véu, texto, selo e CTA, no formato do `identidade.json`) usa a ferramenta de imagem do ambiente na ordem de `references/metodo-4-campos.md`, "Detalhe do render"; sem shell nem biblioteca de imagem, a skill não inventa pixel e entrega `spec-render.md`. O lote roda com checkpoint em `out/progress.json`, e a falha no meio do lote segue o mesmo detalhe (duas falhas seguidas na mesma peça param o lote).

**Passo 6 · LINT ANTI-IA: obrigatório ANTES de virar pixel.** Toda linha de copy passa no gate antes de renderizar. Depois de renderizado, corrigir texto custa o lote inteiro.

Com shell: `python3 scripts/lint_copy.py copy-lote.md` (o script vem dentro desta skill). Só segue com exit 0.

Sem shell, o gate roda no olho, linha por linha, e reprova (falha dura): travessão longo, o verbo-freio banido (a forma verbal, o particípio e a forma com "des-"), frase-emoldura que promete revelação ("a verdade é que", "o segredo"), verbo-clichê (revoluciona, transforma, potencializa, alavanca), tricolon só pelo ritmo, "não é X, é Y" repetido, e qualquer número ou prova sem lastro no material do dono.

**Passo 7 · PRÉVIA PRO DONO, e STOP.** Renderize as prévias e mande pro dono aprovar ANTES de existir campanha. Nunca sobe criativo sem o dono ver. A ordem que evita refação: o dono aprova as PEÇAS primeiro, e só depois as campanhas e as copys. Pergunta literal: "essas são as 4 peças. Aprova todas, corto alguma, refaço alguma?"

**Passo 8 · SOBE PAUSADO + UTM PADRÃO.** A campanha nasce PAUSADA, com o UTM padrão pra casar lead com anúncio e conjunto:
`utm_campaign=<FUNIL-FIXO>` · `utm_content={{ad.name}}` · `utm_term={{adset.id}}`
Subir e segmentar de verdade é com **soft-trafego-meta**; se ela não estiver instalada, este passo sai como especificação escrita pro dono subir na mão (na Ação 0, é a seção 8 de `references/plano-de-teste.md`).

---

## Ação 2 · PLAYBOOK DE 4 CAMPOS (clonar o processo pra outro especialista)

**O que faz:** monta o playbook de criativo de um cliente novo, pra qualquer pessoa rodar a Ação 1 nesse nicho sem redecidir nada.

**Precisa de:** quem é o especialista e o que ele vende · o avatar dele · a marca dele (cor, fonte, selo, CTA) · o destino do anúncio.

**Sem o insumo:** uma mensagem com o que falta dos 4 campos abaixo, até 3 itens (o que sobrar vira premissa marcada). Campo sem resposta vira `[A CONFIRMAR]` no playbook e não impede a entrega.

**Entrega:** `playbook-criativo-<especialista>.md` na pasta de trabalho, com os 4 campos preenchidos e o `identidade.json` já montado dentro. **Arquivos obrigatórios: os acima e `conferencia/checagem-titulos.md` por último** (saída de `scripts/checar_titulos.py`); confira com `ls` antes de dizer que entregou.

**Leia primeiro:** `references/metodo-4-campos.md` (o template completo). Profundidade: `references/exemplo-preenchido.md`.

Os 4 campos:
- **CAMPO 1 (FOTO):** banco de foto própria da autoridade, tratada em preto e branco.
- **CAMPO 2 (IDENTIDADE):** o `identidade.json` (cor, fonte, selo, CTA, assinatura, formato).
- **CAMPO 3 (4 GANCHOS):** 4 combinações distintas (persona, curiosidade, dor), cada peça com UMA dor, 1 gancho por peça.
- **CAMPO 4 (DESTINO):** URL de inscrição, evento de conversão e o UTM padrão.

Preencheu os 4, roda a Ação 1 a partir do passo 4. **STOP:** o dono confirma os 4 campos antes de qualquer render.

---

## Ação 3 · DIAGNÓSTICO: público antes de criativo

**O que faz:** responde se a arte é mesmo o problema, antes do dono gastar um lote novo.

**Precisa de:** em que público cada criativo rodou, e o custo por lead de cada combinação, perguntados ao dono ou lidos do relatório da conta.

**Sem o insumo:** pergunte primeiro "o público foi escolhido à mão (interesse, semelhante) ou é aberto?". **Se é aberto, pule pra Ação 4**: ali a plataforma entrega pelo criativo e o diagnóstico começa na peça. Se foi escolhido à mão, pergunte UMA coisa: "esse criativo rodou em quantos públicos diferentes, e qual foi o custo por lead em cada um?" Sem essa resposta, não existe diagnóstico, só chute.

**Entrega:** `diagnostico-criativo.md`, com a tabela criativo × público × custo por lead e o veredito em 1 linha. **Arquivos obrigatórios: os acima e `conferencia/checagem-titulos.md` por último** (saída de `scripts/checar_titulos.py`); confira com `ls` antes de dizer que entregou.

**A regra-mãe (público escolhido à mão).** Antes de trocar ou matar um criativo, verifique o PÚBLICO: a mesma arte muda de custo por lead em ordem de grandeza só trocando o público. [prova do dono: custo por lead nos dois públicos, período e conta]. Custo alto não manda refazer a arte antes de olhar em que público ela rodou; só se troca criativo ruim NO PÚBLICO BOM.

---

## Ação 4 · FÁBRICA E LEITURA DE MÉTRICA (a peça em vídeo e o que decide se vira dinheiro)

**O que faz:** responde as perguntas que ficam depois da peça pronta. Quantos criativos, de que tipo, em que cadência; o que varia primeiro quando um já vendeu; o que a métrica ruim manda reescrever; e quando um criativo conta como validado. É a camada de VÍDEO e de fábrica por cima do lote de imagem. **Antes de responder, leia em `references/playbook-video-ads.md` a seção que a pergunta pede:** roteiro (1, 2 e 9), quantos e em que cadência (3), o que varia (4 e 5), métrica e validado (6 e 7), pesquisa, espionagem e banco de ativos (8). As réguas de corte (hook rate, hold rate, CTR) estão em `references/plano-de-teste.md`, seção 4. Aqui ficam só as costuras.

**O que decide, em 1 linha por tema (o detalhe está na seção citada do playbook).** Anatomia e duração do vídeo: hook de 3 a 5 segundos, aterrissagem, corpo com mecanismo e prova, 1º CTA pela régua de canal, instrução de edição anexa (1, 2 e 9). Os 3 lotes e a proporção da leva; piso de 50 criativos antes de condenar uma VSL (3). Hierarquia de variação: 2 a 3 ganchos por criativo no primeiro teste, 5 a 10 depois que o corpo validar; empilhamento é anúncio novo (4). Mapa métrica → causa: CPM alto é formato, hook rate baixo é ângulo, hook alto sem venda é corpo, CTR baixo é a CTA, hold baixo é edição, sempre contra o próprio recorde (6). **Validado = 3 a 4 vendas dentro do CPA esperado**, e a régua é o lucro do funil (7). O roteiro passa pelo mesmo lint e pela mesma régua de lastro do lote estático.

**Fronteira fechada:** o critério de validado e o mapa métrica → copy são desta skill; a **soft-trafego-meta** cria, sobe, lê a métrica bruta, pausa e escala com o critério que sai daqui, e a separação teste vs escala é dela. A edição é da **soft-editor-video**.

**Entrega:** quando o pedido é análise, `analise-criativos.md` na pasta de trabalho, com o mapa métrica → causa aplicado aos criativos do dono, o veredito de validado por peça, a proporção da leva e, no fim, o banco de ativos (gancho, hook visual, avatar, corpo e CTA que já venderam) e a lista negra (elemento que falhou em 5 anúncios seguidos), de onde o próximo lote parte. Quando é peça de vídeo, os mesmos arquivos da Ação 1 com o roteiro no lugar do manifesto de imagem. **Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último.**

---

**Número de terceiro sai com a tripla completa.** Preço de concorrente, média de mercado e qualquer número que não seja do dono entram na forma:

```
<número> | trecho: "<literal>" | url: https://... | consultado em: <dd/mm/aaaa>
```

**Linha sem URL completa reprova o número**: a referência interna da ferramenta de busca não abre no navegador do dono. Feche com `números de terceiro: N · com trecho literal: N · com URL completa: N`, os três iguais. O `checar_titulos.py` conta e reprova quando divergem.

## Gate de qualidade (roda antes de toda entrega)

**Número não confirmado nunca vira pixel (a arte publicada não carrega ressalva).** Antes de renderizar, rode `grep -n 'A CONFIRMAR' <perfil do dono>`, extraia cada valor marcado, e rode `grep -nF '<valor>' <copy da peça>` por valor, colando as duas saídas. Valor marcado sai da frase e entra a forma sem número ("algumas semanas", "depois de um tempo"), nunca o marcador e nunca o número cru: o card sai no feed sozinho, e quem lê não vê a ressalva que ficou no bastidor. Cole `valores não confirmados no perfil: N · renderizados na arte: 0`, e qualquer número acima de zero na segunda coluna reprova o render antes de exportar.

**Capa que chega pronta na copy fonte não se troca por outra pior.** Quando a peça nasce de uma copy que já tem capa ou headline escolhida, a capa da fonte é a linha a bater, nunca a linha a descartar por hábito. Cole `capa da fonte: <literal> · capa publicada: <literal> · motivo da troca: <escrito>`, passe a publicada pela régua com o gatilho nomeado, e feche com `manchetes idênticas à fonte: N de N`. **Capa publicada em molde `Como <resultado> sem <obstáculo>` reprova a troca**: é o molde mais batido do mercado, e é o que a régua existe pra superar. Sem motivo escrito, a capa da fonte volta.

**Os gates de arte saem em linha de saída, cada um com o comando literal ao lado.** Prosa não conta como contagem, e foi por isso que três exigências passaram sem número em duas entregas seguidas. O passo de render fecha com estas linhas, uma por linha, na forma `<gate>: <valor> | comando: <literal>`, cada uma com a saída crua colada acima dela:

```
realpath config: <saída> | comando: realpath <caminho do config do dono>
realpath skill: <saída> | comando: realpath <pasta desta skill>
a primeira começa pela segunda: não | comando: a comparação das duas saídas acima
cores medidas no PNG: <lista hex> | comando: python3 -c "from PIL import Image; ..." ou o medidor da skill
imagens fortes no PNG: N de N exigidas | comando: a contagem sobre os arquivos renderizados
cards com GIF: N de N exigidos | comando: ls *.gif
geradores testados: N (mínimo 2) · falharam: N | comando: um por linha na forma `gerador: X | testado: sim | resultado: Y`
```

Qualquer uma dessas linhas ausente reprova antes da análise de arte, e declarar sem a saída colada não conta como feito.

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`references/regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE em `conferencia/checagem-titulos.md`**, mesmo quando a entrega já tem crivo, handoff ou relato. Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros iguais, ou reprova: o universo são TODOS os textos que o público lê como título. Sem esse arquivo, reprova antes da análise de conteúdo. **O gatilho sai da lista fechada, e a checagem imprime a lista antes da tabela:** `famílias válidas: Recompensa · Mistério · Crença · Disrupção · Popularidade · Reconhecimento`. Palavra fora da lista não é gatilho, nem o critério de R4 (inimigo nomeado, ordem invertida). Cole `gatilhos fora da lista fechada: 0`, e qualquer número maior reprova o lote.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real vinda de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem a linha `autorizado por <dono> em <data>` no insumo. Sem ela: anonimiza (a inicial ou "uma aluna", sem detalhe que devolva a identidade) ou não usa; marcar `[A CONFIRMAR: autorização]` e publicar reprova. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** **A checagem é COMANDO, nunca de memória:** os 3 passos de `references/08-consentimento.md` (a lista de nomes dos insumos privados, o `grep -nwF` de cada nome sobre o arquivo INTEIRO da peça, as duas saídas coladas), fechando com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. Nome na saída sem a autorização apontada por `<arquivo:linha>` reprova; contagem sem a saída colada não conta, e declarar zero onde o grep devolveu nome reprova.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono deu e cabe na entrega aparece nela ou tem o motivo da exclusão. Liste em `conferencia/checagem-titulos.md`, um dado por linha (agrupar reprova), `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` O piso é CONTADO: `grep -c '^-' <perfil>` dá os campos, e campo de valor múltiplo desdobra (como, em `references/08-consentimento.md`, "O piso do inventário sai de comando"). Cole `dados no perfil: N · usados: N · descartados com motivo: N`, somando N. **Sem essa contagem, ou com menos linhas que N, reprova sem análise de conteúdo.**

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.

| Critério | Passa se |
|---|---|
| Anti-IA na copy | o gate roda em TODO arquivo entregue, não só nos `.md`: `for f in $(find <pasta> -type f \( -name '*.md' -o -name '*.json' -o -name '*.txt' \)); do python3 scripts/lint_copy.py "$f"; done`, com a saída colada no relato e a contagem `arquivos linteados: N · exit 0: N`. Campo de texto livre dentro de JSON (motivo de bloqueio, descrição, nota) é copy e obedece às mesmas regras duras. Sem shell, a leitura linha a linha do passo 6 não acha nenhum item da lista dura |
| Ângulo por peça | as linhas `peça <n> \| persona \| curiosidade \| dor \| material` estão coladas, nenhuma repete as três primeiras, nenhuma dor aparece mais de 2 vezes; nenhum gancho promete o que o corpo e o produto não entregam |
| Material do dono | `conferencia/material-do-dono.txt` com origem por item e nenhum item deduzido ou de terceiro sem autorização; `peças no lote: N · com material do dono: N`, iguais |
| Mensagem ao dono | `conferencia/mensagem-dono.txt` com `grep -c .` até 8, a decisão do dono na 1ª linha, no máximo 1 linha citando arquivo, sem nome de regra ou de script |
| Congruência com o destino | com a 1ª frase da VSL ou da página informada: `peça <n> \| termo-gancho: <literal> \| está em: gancho ou texto_anuncio`, mais a saída de `python3 -c "import json;d=json.load(open('manifesto.json'));t='<termo>'.lower();print(sum(t in (p['gancho']+' '+p.get('texto_anuncio','')).lower() for p in d['pecas']), len(d['pecas']))"`, os dois números iguais. Sem destino informado, 1 linha declara `sem ponte` |
| Texto e título do anúncio | toda entrada do manifesto tem `texto_anuncio` e `titulo_anuncio` com texto escrito, e os dois passaram no lint e na régua de títulos |
| Política da plataforma | `python3 scripts/checar_promessa.py copy-lote.md manifesto.json` (mais os roteiros) com `promessas de risco: 0` colado; sem shell, leia cada linha atrás de prazo de resultado, garantia de resultado, cura, antes e depois, e gancho que afirma ou insinua atributo pessoal de quem lê (saúde, peso, dívida, idade como defeito). A promessa vinda do material do dono conta igual. Mais `visuais proibidos no manifesto: 0` (zoom em parte do corpo, pessoa triste, balança ou fita métrica em emagrecimento, carteira vazia em finanças) |
| Roteiro de vídeo | quando há vídeo: formato nomeado, duração pela régua de canal, linhas `aterrissagem:` e `prova: <tipo>`, o segundo do 1º CTA marcado, e a instrução de edição anexa |
| Plano de teste (Ação 0) | `plano de teste: 6 de 6 blocos`, pela conferência da seção 8 de `references/plano-de-teste.md` |
| Foto | rosto real do dono, topo do cabelo e queixo dentro do quadro em toda peça |
| Identidade | cor, fonte, selo e CTA vieram do `identidade.json`, nenhum valor escrito dentro do código |
| Contraste | com véu claro, o texto da 1ª linha é escuro e o sub é cinza médio, conferido no arquivo final e não no preview |
| Lastro | todo número e toda prova na copy têm origem no material do dono e dizem só o que a fonte diz, ou saem marcados `[A CONFIRMAR]`; nenhum detalhe de material sem autorização vira gancho |
| CTA escrito | **o texto do botão nunca sai em marcador.** Ele vem, nesta ordem, da ação que o dono já usa nos insumos, da ação nativa da plataforma, ou do convite ao evento datado do perfil. Sem nenhuma das três, o CTA sai na versão que dispensa o botão. Cole `CTAs no lote: N · com texto escrito: N · em marcador: 0` |
| Ressalva no lote | a peça é o LOTE, nunca o arquivo: a ressalva clínica ou regulada entra UMA vez no conjunto, no fim da última peça. Cole a soma de `grep -c '<a frase da ressalva>'` sobre TODOS os arquivos da entrega, e ela tem que dar 1 |
| Prévia | o dono viu e aprovou as peças antes de existir campanha |

O veredito é o pior item da tabela. Falhou um, o lote não sai.

## Regras duras (cada uma nasceu de um erro que custou um lote)

1. **VÉU CLAREIA A BASE.** Quando o véu clareia a base pra um tom creme, o texto da 1ª linha tem que ser ESCURO, senão some. O sub usa cinza médio, não claro. Confira no arquivo final.
2. **REFAZER PEÇA SOLO É LIMPAR O CHECKPOINT.** Apague a entrada dela no `progress.json` e os jpgs daquela peça antes de rodar de novo, senão o checkpoint acha que ela já saiu e pula o item.
3. **MANTER ACENTOS NO MANIFESTO.** Escreva o texto com acento correto e teste UMA peça antes do lote. Se faltar glifo, troque a fonte, nunca tire o acento do texto.
4. **PUBLICAR NÃO É COMMITAR.** Guardar a imagem no repositório não coloca ela no ar. Abra a URL final da imagem no navegador antes de apontar o anúncio pra ela.
5. **PÁGINA E PERFIL SÃO FIXADOS NO CRIATIVO.** Ficam imutáveis dentro do criativo; errar significa refazer todos. Confirme a página certa ANTES, lendo o identificador de um anúncio ATIVO da própria conta, nunca chutando.
6. **LINT ANTES DE RENDERIZAR.** Copy passa no lint antes de virar pixel.
7. **PRÉVIA ANTES DE SUBIR.** O dono vê a prévia antes de existir campanha. Sempre.

## O que esta skill NÃO faz

Se a skill de destino não estiver instalada, esta faz o mínimo aqui, do jeito que está escrito no passo correspondente.

- Escrever a headline ou o gancho do zero como peça própria, com banco de fórmulas: **soft-conteudo-headlines**. Sem ela, os ganchos nascem aqui no passo 1.
- Peça editorial única com diagrama, tabela ou layout complexo: **soft-designer**. Sem ela, vale a ordem de preferência do passo 5.
- Pesquisar o que vende no nicho, espionar ou desmontar anúncio de concorrente: **soft-espiao**. Sem ela, a régua mínima está em `references/playbook-video-ads.md`, seção 8.
- Criar campanha, segmentar, ler métrica bruta, escalar ou pausar na conta, e o plano de mídia de campanha que já roda (o que turbinar, distribuição): **soft-trafego-meta**. Sem ela, o passo 8 e o `plano-de-teste.md` da Ação 0 saem com o passo a passo à mão.
- Editar o vídeo gravado: **soft-editor-video**. Sem ela, o roteiro sai com a instrução de edição pra quem editar. Escrever a VSL: **soft-funil-vsl**. Sem ela, o handoff leva `gancho do anúncio: <frase>`.

## Arquivos

`references/regua-de-titulos.md` (régua de títulos) · `references/metodo-4-campos.md` (os 4 campos e o detalhe do render: foto, JSONs, ferramenta, checkpoint) · `references/exemplo-preenchido.md` (os 4 campos de pé) · `references/EXEMPLO-FIM-A-FIM.md` (o lote e a Ação 0 inteiros) · `references/angulos-de-cpc.md` (os 5 ângulos) · `references/playbook-video-ads.md` (vídeo e fábrica) · `references/plano-de-teste.md` (verba, fases, corte, escala, passo a passo à mão) · `references/08-consentimento.md` (nomes e inventário por comando) · `references/fontes-do-metodo.md` (origem de cada regra) · `scripts/lint_copy.py` (anti-IA) · `scripts/checar_promessa.py` (promessa de risco) · `scripts/checar_titulos.py` (a conferência) · `shared-references/filtro-anti-ia/` (a régua anti-IA por escrito, pro motor sem shell). Produzidos na PASTA DE TRABALHO, não aqui: `identidade.json` · `manifesto.json` · `copy-lote.md` · `out/` com as imagens e o `progress.json` · `plano-de-teste.md` · `roteiro-video-<n>.md` · `conferencia/`.

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado na saída, relato e notas de confirmação inclusos, e cole uma linha por arquivo, `<arquivo>: exit N`; "passou no lint" sem essa linha não conta. **O relato conta:** `RELATO.md: exit 0` é obrigatória, rodada depois de terminar de escrevê-lo, e relato com travessão longo reprova igual a peça de cliente. Feche com `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Sem sandbox (a régua escrita, quando o lint não roda).** Aplique no olho `shared-references/filtro-anti-ia/padroes-banidos.md`, padrão por padrão, e passe cada reprovação por `shared-references/filtro-anti-ia/falsos-positivos.md` antes de reescrever, porque prosa autoral do dono cai no mesmo crivo. O relato fecha com `anti-IA: conferido no olho pela régua escrita (sem shell nesta rodada)`; calar o que ficou de fora reprova.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato. Abra cada arquivo gravado e confira a primeira linha, a última e uma do meio; prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam e mandam regravar.
- **Configuração do dono fora da pasta da skill.** Perfil ou arquivo do dono nunca é gravado dentro da pasta desta skill; vai pra pasta de trabalho do dono, com o caminho no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Consentimento de nome real (roda antes de entregar, por comando):** os 3 passos de `references/08-consentimento.md`, os mesmos da regra "Nome de pessoa real em copy pública" do gate, com a linha `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0` colada. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**

## Passo 2 da checagem (fecho, roda por comando)

Depois de gravar todos os entregáveis, rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída. Ele exige o `conferencia/checagem-titulos.md` na pasta, confere o inventário (os 4 inteiros, o piso e o `inventário duplicado`), o universo dos títulos, o marcador acima de 6 palavras, o nome de conversa privada, a `saída do script reescrita` e o lint de todo `.md`, RELATO incluso. **`exit` diferente de 0 reprova a entrega inteira, antes da análise de conteúdo.**
