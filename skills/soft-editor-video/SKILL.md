---
name: soft-editor-video
description: >-
  Edita uma gravação crua e devolve o arquivo de vídeo vertical 9:16 finalizado mais o relatório da edição: corte de pausa, gancho no começo, apoios de 2 a 3 segundos, legenda palavra por palavra, música discreta e auditoria visual com prova em mosaico. Âncora: o vídeo JÁ FOI GRAVADO. Use quando o pedido for: "edita esse vídeo", "corta as pausas", "queima a legenda nesse reel", "monta o gancho desse vídeo já gravado", "coloca b-roll aqui", "anima essa imagem", "monta o anúncio em vídeo", "deixa esse take pronto pra postar", "põe o CTA no final". NÃO use pra: escrever o roteiro, a fala ou a legenda de publicação do reel (soft-conteudo-reels); escrever o gancho como texto, antes de gravar (soft-conteudo-headlines); o reel curto renderizado do zero (soft-reel-7seg); criticar a copy da tela (soft-critico-copy); arte estática ou banner (soft-designer); o lote de criativos (soft-criativo-campeao); landing (soft-funil-landing). Leia e siga o fluxo inteiro do SKILL.md.
---

# Editor de vídeo: entra uma gravação crua, sai o arquivo finalizado

Esta skill pega a MATÉRIA-PRIMA (uma gravação de celular ou câmera, mais o que existir de apoio) e devolve DUAS coisas: o arquivo de vídeo vertical 9:16 pronto pra postar, e o relatório da edição com a prova visual do que foi conferido.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**A fala que o dono vai gravar passa pelo gate do número não confirmado.** Roteiro de gravação é copy publicada com atraso: o que está na lista de falas vira áudio no ar, e o vídeo não tem onde carregar a ressalva. `PEDIDO-DE-GRAVACAO*`, `roteiro*` e `fala*` entram no gate como qualquer peça pública. Rode `grep -n 'A CONFIRMAR' <perfil>`, extraia cada valor e rode `grep -nF '<valor>' <arquivo de falas>`, colando as duas saídas. Valor não confirmado sai da fala e vira linha de pendência pro dono confirmar antes do take, nunca marcador dentro da fala. Cole `valores não confirmados no perfil: N · presentes nas falas: 0`.

Ela entra DEPOIS que o roteiro já existe. Aqui é produção e edição, nunca escrita. É marca-neutra: não embute a cara de ninguém, no primeiro uso entrevista o dono e guarda o elenco e a identidade dele em `config/personagens.json`, e cada cliente roda com a própria marca.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício de ponta a ponta em nicho neutro: a matéria-prima que chegou, as perguntas do primeiro uso, a decisão de forma, o manifesto preenchido, o que a auditoria devolveu e o relatório final. É o arquivo que calibra o formato antes do primeiro corte.

**O perfil do dono vem do banco do agente.** Onde a skill precisar de identidade visual, paleta, logo, elenco ou voz: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista do Passo 0 e siga com o que faltar marcado `[A CONFIRMAR]`.

**Levantamento BLOQUEANTE antes de editar (roda como a ancoragem do gate, e é COMANDO, nunca de memória).** Antes de decidir a forma e antes de queimar qualquer cena ou texto, LEIA o `config/personagens.json`, o perfil e os insumos do dono e cole no processo uma linha por dado-chave, nesta forma: `<campo> | <valor encontrado> (<arquivo>:<trecho>) | ou [A CONFIRMAR] só se o ls/leitura devolveu vazio`. Os campos-chave: elenco e aparência, ambiente ou cenário, paleta, logo, destino da peça, card de encerramento. **Marcar `[A CONFIRMAR]` um dado que EXISTE no config ou no insumo reprova a entrega**, então rode a leitura antes de decidir e cole a saída. A tabela fecha com `campos-chave: N · encontrados no insumo: N · [A CONFIRMAR] com leitura vazia comprovada: N`, e a soma fecha em N.

**O exemplo é ILUSTRATIVO, é PROIBIDO parafrasear.** `references/EXEMPLO-FIM-A-FIM.md` usa um nicho fictício só pra mostrar a FORMA. É proibido reusar as frases, os números, o nicho ou a cena dele na peça real. A peça real nasce 100% do insumo e do config do dono; se você se pegar copiando uma frase ou uma cena do exemplo, pare e volte ao insumo.

---

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você manda o vídeo e me diz a marca e eu edito). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra a edição com o vídeo que o dono já mandou. Se faltar um insumo que a edição não vive sem (o arquivo do vídeo, ou a cor/marca da legenda), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz as perguntas uma de cada vez (a forma da edição, a identidade, o CTA) antes de cortar.

A pergunta do modo é UMA por vídeo. Mais duas partes entram nos passos abaixo:

- **Ensina enquanto faz:** ao escolher a forma da edição (com b-roll de IA, ou só corte e legenda), escreve UMA linha do porquê ("vou de corte seco com legenda karaokê porque o teu vídeo já é forte na câmera; b-roll aqui distrairia da tua fala"), pra o dono decidir sozinho na próxima.
- **Oferece refinar no fim:** depois de entregar o vídeo, fecha com UMA linha de ajuste ("quer o corte mais rápido? outra cor na legenda? mais b-roll? refaço só a parte que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Ação única · EDITAR UM VÍDEO

**O que faz:** transforma uma gravação crua num vídeo vertical 9:16 finalizado, com corte, gancho, apoios, legenda, música e auditoria visual.

**Precisa de (a matéria-prima):**
1. **O arquivo de vídeo cru**, sempre do dono. É o único insumo sem substituto.
2. **O destino da peça** (reel de atração, anúncio, conteúdo puro), perguntado ao dono em 1 linha.
3. **A identidade dele** (elenco, ambiente, paleta, logo), do perfil/brain do agente ou do `config/personagens.json`.
4. **O material de apoio que já existe**, quando existir: gravação de tela, print de conversa real, foto de produto, resultado na tela. Pergunta em 1 linha: "você tem alguma tela, print ou gravação que MOSTRE o que você fala?"
5. **O card de encerramento**, quando o dono usa um.

**Sem o insumo:**
- Sem o arquivo de vídeo: não existe edição. Peça o arquivo e pare. É o único bloqueio duro.
- Sem destino declarado: assuma reel de atração, escreva isso em 1 linha na resposta e siga.
- Sem `config/personagens.json`: rode o Passo 0, que é a entrevista de 6 perguntas.
- Sem material de apoio nenhum: a Forma D (conteúdo puro) resolve o vídeo inteiro sem apoio gerado. Não invente prova pra preencher tela.
- Sem card de encerramento: entregue sem CTA e diga em 1 linha que ele pode ser somado depois sem refazer o vídeo.
- Sem gerador de imagem ou de movimento no ambiente: caia pra Forma D ou pra cartela de texto sobre a própria imagem. A skill nunca para por falta de recurso pago.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega (as duas peças, sempre):**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.
1. `final-<slug>-1080x1920.mp4` na pasta de saída do dono.
2. `relatorio-edicao-<slug>.md`, com a forma escolhida e o porquê, o mapa de cortes, a decisão de cada apoio, o que a auditoria devolveu e o caminho do `audit/mosaico.jpg`.

Os dois caminhos saem na resposta, cada um em linha isolada, pra a ponte de entrega subir os dois.

**Leia primeiro:** `references/regua-adaptativa.md` (governa enquadramento, ritmo, legenda, virada e escolha de composição) · `references/metodo.md` (o método detalhado).

**Profundidade:** `references/recursos-geracao.md` (quando há cena nova, animação externa, upscale ou troca de provedor) · `references/direcao-visual-longa.md` (vídeo longo e VSL) · `references/forma-topo-fixo.md` mais `templates/topo-fixo/` (a receita completa da forma mais pesada, e só ela).

---

## Passo 1 · ESCOLHE A FORMA (a primeira decisão, antes de qualquer corte)

A forma sai da MATÉRIA-PRIMA, nunca do vídeo anterior. Leia a linha certa e decida antes de produzir. Esta decisão é interna e não vira pergunta pro dono, mas o motivo dela entra no relatório final.

| A matéria-prima tem | Forma | O que ela é |
|---|---|---|
| uma conversa real, página, produto ou demonstração que É a prova central | **A · Tela cheia de prova** | a prova ocupa a tela inteira, nunca cabe numa faixa pequena |
| um talking-head que explica, com apoio que ilustra a fala | **B · Composição adaptativa** | apresentador e apoio trocam de importância ao longo da fala, com virada de layout |
| um talking-head que cita muitas telas e listas, e o apoio precisa MOSTRAR o que a fala nomeia | **C · Topo-fixo com slides e telas** | rosto fixo em cima, faixa de baixo com slides e telas reais |
| só a fala, sem apoio disponível, ou uma direção aprovada de manter o quadro cru | **D · Conteúdo puro** | vídeo original em tela cheia, com headline curta nos 3 primeiros segundos |

**O padrão quando a matéria-prima é ambígua é a FORMA B.** Talking-head com apoio rápido é a que mais serve, é a que a `references/regua-adaptativa.md` governa por inteiro e é a que aceita degradação: sem gerador de imagem, os apoios da B viram cartela e tela real, e o vídeo sai igual. Só saia da B quando a matéria-prima gritar outra coisa: prova que precisa ser lida inteira leva pra A, muitas telas citadas levam pra C, ausência total de apoio leva pra D.

**A Forma C é a mais pesada e mora fora deste arquivo.** Ela usa motor React e template próprio, tem 4 correções cravadas e um gate de amostra. Receita completa em `references/forma-topo-fixo.md` e `templates/topo-fixo/`. Nela, o primeiro vídeo aprovado pelo dono vira o molde visual intocável da família: os seguintes copiam o mesmo tratamento sem redecidir nada, e o vídeo-molde aprovado não se regenera nem se altera.

---

## Passo 0 · PRIMEIRO USO (rode só se ainda não estiver configurado)

Se `config/personagens.json` já existir, NÃO pergunte de novo, siga direto pro Passo 2.

### 0.1 · A ordem de grandeza do custo, ANTES de pedir qualquer aprovação de gasto

O dono precisa saber em que faixa ele está pisando antes de dizer sim. As três faixas, do mais barato pro mais caro:

| Recurso | Faixa de custo | Quando entra |
|---|---|---|
| transcrição local, corte, legenda, cartela, música, montagem | **zero**, roda na máquina | sempre, é o padrão |
| geração de imagem pela conta que o ambiente já tem | **centavos por imagem**, e um vídeo usa entre 3 e 10 | quando a Forma B ou C pede apoio ilustrado |
| animação de imagem por serviço de crédito | **da ordem de dezenas de centavos a alguns reais POR CLIPE de poucos segundos**, e um vídeo pode pedir 5 a 10 clipes | só quando o movimento gerado muda a peça |

A terceira faixa é a que estoura orçamento sem avisar, porque o preço é por clipe curto e o vídeo pede vários. Regra: antes de gastar crédito, consulte o saldo e o preço REAL no provedor, mostre o número exato ao dono e espere o sim. Abrir chave paga nova por conta própria está proibido.

Movimento local é o padrão. Serviço de crédito é sempre opcional.

Nunca peça chave que já existe: confira primeiro `config/`, as variáveis de ambiente e o que o ambiente já traz. Leia `references/recursos-geracao.md` quando houver cena nova, animação externa, upscale ou troca de provedor.

### 0.2 · O elenco do dono (a marca dele nas cenas)

Se `config/personagens.json` não existir, entreviste o dono, uma pergunta por vez:

1. "Quem é o apresentador principal? Descreve aparência: etnia, cabelo, barba, roupa, vibe."
2. "Quer um mascote? Como ele é?"
3. "Tem mais alguém fixo na marca? Sócio, co-apresentador, assistente?"
4. "Qual o ambiente ou cenário padrão?"
5. "Qual a paleta de cores da marca?"
6. "Tem um logo que aparece nas cenas?"

**Todo campo preenchido do JSON de identidade carrega a origem no próprio arquivo.** Some ao `config/personagens.json` um objeto `origens` com uma entrada por campo preenchido, no formato `"<campo>": "<arquivo>:<linha>"`. Campo com valor e sem entrada em `origens` reprova, inclusive quando o valor parece óbvio: `@` de perfil, texto de selo, CTA e qualquer número de cor. Cole `campos preenchidos: N · com origem apontada: N`, iguais. `null` com a pendência declarada é resultado correto e dispensa origem; número inventado num arquivo cujos vizinhos ficaram `null` por falta de origem é o pior dos dois mundos.

Se o dono já tem identidade visual definida em **soft-designer**, puxe de lá em vez de perguntar do zero, pra manter a mesma cara entre carrossel, banner e vídeo.

Monte `config/personagens.json` no formato de `config/personagens.example.md`, cada personagem com descrição detalhada em inglês pro gerador de imagem, e defina `trio_sempre`, quem aparece em TODA cena.

**STOP.** Gere 1 imagem de teste de cada personagem e mostre ao dono antes de produzir vídeo. Pergunta literal: "é essa a sua cara nas cenas? Aprova, ou ajusto alguma coisa?"

### 0.3 · Card de encerramento (opcional)

Pergunte se o dono quer um card fixo no fim de todo vídeo. Se sim, ajude a criar: gere a imagem 9:16 com os personagens mais o texto da oferta dele, anime, e salve em `config/cta_take.mp4`. Reuse em todos os vídeos. A copy do card passa pelo crivo anti-IA das Regras Invioláveis.

---

## Passo 2 ao 14 · O pipeline

2. **Ingestão:** rode `ffprobe`; extraia o áudio; confira se o vídeo já tem legenda (extraia frames) e onde ela está.
3. **Leitura da fala e da imagem:** transcreva com palavras e tempos e grave `speech_words` no manifesto. Separe fala, prova real, listas, nomes próprios e CTA. Confirme aqui a forma escolhida no Passo 1 contra o que a transcrição revelou. **A transcrição local já dá timestamp POR PALAVRA de graça** (`faster-whisper` ou `whisper-timestamped`, não o Whisper cru que devolve por segmento), e é isso que a legenda karaokê usa. Transcrição paga só ganha em PRECISÃO DE ALINHAMENTO, não em existência do dado por palavra: antes de pagar, MEÇA o desvio do alinhamento local numa amostra e só troque se a legenda atrasar de forma visível (`references/playbook-edicao.md` seção 6).
4. **Corte:** comece na primeira fala completa, remova respiração e pausa longa, aplique 1,2x quando essa família já estiver aprovada nessa velocidade. Preserve toda a mensagem. Corte semântico só entra depois de aprovação nominal do dono. Rode `python3 scripts/00_silence_cut.py ... --manifest edit-manifest.json`; o script grava o mapa explícito de cortes e aplica fade de áudio de 30 ms na entrada e na saída de cada trecho. **Todo corte que remove FALA (não só silêncio) nasce de uma tabela em disco decidida por TEMPO, nunca no olho.** Escreva `cortes-propostos.md` na pasta do dono (`início · fim · o que sai · por quê`, cobrindo claquete, silêncio longo, gancho gravado em duplicata, CTA falado errado), o dono aprova ou ajusta linha a linha, e só então o script aplica. Corte de fala sem a tabela aprovada reprova. Cole `trechos propostos: N · aprovados: N · ajustados: N` (detalhe em `references/playbook-edicao.md` seção 1).
5. **Planejar apoios:** mapeie a fala pra cenas de 2 a 3 segundos. **Toda instrução de inserção aponta PALAVRA e TEMPO, nunca sensação:** `apoio entra na palavra "resultado" em 00:12,4` ou `entre 00:12,4 e 00:15,0`, porque o agente não assiste, ele lê a transcrição temporizada e extrai quadros. Instrução por estado ("quando ele fica sério", "no momento mais emocionante") reprova e volta pro dono apontar o segundo (`references/playbook-edicao.md` seção 3). Cada trecho registra intenção, trecho da fala, estratégia visual, frase de apoio (ou o motivo de não usar texto), frame inicial, frame final, movimento e transições de entrada e saída. A frase de apoio destaca tese, número, contraste ou conclusão, e nunca repete a legenda. A transição nasce da virada narrativa, não de efeito decorativo. Prioridade: prova real, depois imagem gerada e animada, depois cartela. Imagem não fica parada por 8 ou 10 segundos. Lista entra item por item no instante da fala. Vídeo longo e VSL seguem `references/direcao-visual-longa.md`.
6. **Gerar imagens** (`python3 scripts/01_gen_images.py`): 1536x1024 alta qualidade, corte 16:9 `crop=1536:864:0:80`, área segura declarada no prompt. **STOP:** abra as imagens pro dono e espere ele aprovar antes de animar.
7. **Animar:** movimento local é o padrão. Pra clipe gerado, siga `references/recursos-geracao.md`: imagem-pra-vídeo, uma geração por vez, imagem já aprovada, custo confirmado e prompt negativo obrigatório.
8. **Montar animações e overlays:** siga `references/regua-adaptativa.md`. No talking-head com apoio, mantenha o rosto fechado e centralizado e vire o layout por flash no terço inicial. Prova real importante pode assumir a tela inteira. Feche todas as animações, apoios, faixas e overlays ANTES da legenda.
9. **Gancho, o começo do vídeo** (`python3 scripts/05_hook.py`): copie a FRASE COMPLETA mais forte pro comecinho, só o apresentador, sem apoio, com um efeito (preto e branco, VHS, fantasma ou tv velha) E a mesma frase numa faixa na tela. Depois, transição pro corpo. A frase continua no lugar original dela. Ordem final: gancho, corpo, card, música.
   - Frase COMPLETA, nunca cortada na metade, mesmo passando um pouco de 5 segundos.
   - Faixa de no máximo 2 linhas, fonte cerca de metade do tamanho cheio, no terço inferior.
   - A escolha da frase é sua, pelos critérios: gera expectativa, é forte, é a que a pessoa repetiria. A frase passa pelo crivo anti-IA antes de queimar.
10. **Legenda por último:** aplique a legenda palavra por palavra somente depois de todas as animações e overlays; destaque a palavra-chave do trecho e mantenha a legenda na altura do peito quando houver apresentador. Registre `render_order` no manifesto. Legenda de bloco está reprovada nesta família.
11. **Card de encerramento** (se configurado): anexe `config/cta_take.mp4` com transição suave, sem corte seco. `python3 scripts/04_build_final.py` faz card e música.
12. **Música de fundo discreta:** normalizada e baixa, com fade de entrada e saída, e NUNCA por cima da fala.
13. **Inspeção de cada corte:** renderize o candidato e rode `python3 scripts/06_inspect_cuts.py candidato.mp4 edit-manifest.json pasta/cortes`. O script abre os três quadros de cada emenda com a capacidade de visão do ambiente e grava a prova. Ausência ou reprovação bloqueia o gate.
14. **Gate antes do export:** salve `edit-manifest.json` e rode `python3 scripts/07_gate_edit.py edit-manifest.json`. Falha bloqueia o export final.
15. **Export 1080x1920**, salve na pasta de saída do dono, e rode a auditoria visual.

---

## Gate de qualidade (bloqueante, roda antes de toda entrega)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado, e a conta vem ANTES de escrever a peça.** Monte a conta em 3 passos e cole no processo: (1) `grep -c '^-' <perfil>` = C campos; (2) percorra os campos e escreva `campo <n>: <k> valores` para todo campo com k maior que 1, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1; (3) some, e M é o piso. Cole `campos no perfil: C · valores desdobrados: M · linhas do inventário: M`. **Inventário com menos de M linhas reprova sem análise de conteúdo, e a linha que agrupa dois dados conta como UMA linha e como N dados faltando.** A ordem é o que decide: a conta feita depois da peça vira justificativa, e a conta feita antes vira o alvo. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **O inventário varre o perfil do dono INTEIRO, não só os campos que esta entrega consumiu:** cada campo do perfil é uma linha, e campo com vários valores (paleta com 3 cores; oferta com preço, parcela, bônus e garantia) rende uma linha por valor. **Entrega cujo `Dados fornecidos: N` for menor que o número de campos do perfil recebido reprova sem análise de conteúdo.** Qualificar a linha ("relevantes ao objeto", "considerados para esta entrega") também reprova: o total é o total. **Onde a linha mora:** no arquivo que o dono lê. Quando a entrega é uma peça de copy publicável (headline, carrossel, slide, card, chat, roteiro, deck), a peça NÃO recebe a tabela: a tabela vai num arquivo irmão de handoff (`HANDOFF-<slug>.md`) e só a linha de fechamento fica na peça, no rodapé. Inventário só no relato de processo, sem a linha na entrega nem o handoff no disco, reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.


**Critérios de auto-aprovação, e o teto de 3 tentativas.** O agente aprova sozinho o que é MEDÍVEL e escala pro dono o que é gosto. **Auto-aprova sem chamar o dono quando as QUATRO batem:** (a) nenhum elemento de tela cobre rosto ou corpo do apresentador; (b) o tempo de entrada e saída de cada elemento bate com o manifesto; (c) quando há PIP ou bolha, nenhum elemento de design fica por cima dela; (d) áudio sincronizado com a legenda karaokê, sem atraso perceptível. **SEMPRE escala pro dono, nunca decide sozinho:** se o RITMO funciona ou arrasta, e se a composição tem a CARA da marca. **Teto de 3 correções automáticas:** critério medível que falha, o agente corrige e refaz até 3 vezes; na 4ª falha para e chama o dono. O teto vive no `edit-manifest.json` no campo `tentativas_auto` (`{"teto": 3, "usadas": N, "escalou_ao_dono": bool, "motivo_escala": ...}`), e `usadas` maior que `teto` reprova no `07_gate_edit.py`. Isso não substitui o gate nem a auditoria, formaliza o loop de correção dentro deles (`references/playbook-edicao.md` seção 2).

**Memória de estilo em `config/estilos.md`.** O primeiro tratamento aprovado de uma forma ou personagem vira molde declarado (nome do estilo, legenda, cor, posição, transições, música, CTA), pra a próxima edição pular a exploração. "Edita no estilo `<nome>`" carrega o bloco em vez de redecidir tudo. Estende pras Formas A, B e D o hábito que hoje só a Forma C tem, e economiza token (`references/playbook-edicao.md` seção 4). É configuração do dono, segue a regra de não versionar dado do dono junto do código.

**Comparação entre motores (quando dois rodam o mesmo ativo).** O vencedor é o que passa a TABELA DE VERBOS DO PEDIDO inteira, a mesma régua do gate. **"Motor mais rápido" NÃO é regra:** um output rápido com qualquer verbo em `não feito` (por exemplo, exportou sem legenda) perde. O cronômetro só desempata entre dois outputs que passaram a tabela inteira, e nunca se escreve preferência fixa por motor (`references/playbook-edicao.md` seção 5).

| Critério | Passa se |
|---|---|
| Gate da edição | `python3 scripts/07_gate_edit.py edit-manifest.json` sai com exit 0 (exige fala temporizada, mapa de cortes, fades de 30 ms, ordem da legenda, direção visual completa, decisão de frase de apoio, transições e prova visual de cada corte). **Insumo sem fala é caminho previsto, não falha:** quando a medição mostrar que não há fala no material, grave `speech_words: []` junto de `no_speech_reason: "<motivo medido, com o comando que mediu>"`, e os critérios de legenda e de gancho ficam fora do gate por não se aplicarem. **É proibido gravar texto falso em `speech_words` só pra satisfazer o formato** (`[sem_fala_no_material]` e afins reprovam), e é proibido exportar com o gate em falha. O relatório declara em 1 linha que a peça saiu sem legenda por falta de fala |
| Verbos do pedido, um a um | **O veredito lista os verbos do pedido (cortar, legendar, verticalizar, musicar, ganchar) e marca cada um como `feito`, `não aplicável porque <motivo medido>` ou `não feito`.** Veredito `PASSA` com qualquer verbo em `não feito` é proibido: o status vira `PASSA COM PENDÊNCIA` e as pendências vão na PRIMEIRA linha do relatório, não no rodapé. Corte de pausas que removeu 0 quadro conta como `não feito`, e a duração medida antes e depois vai colada (`duração fonte: Xs · duração final: Ys`). **Um verbo é `feito` quando o comando alterou o arquivo E a medição do antes e do depois difere.** Quando as duas medições são iguais (bruto que já chegou em 9:16 e "verticalizar" não mexeu em nada), o estado é `nao_aplicavel`, e o motivo cola as duas lado a lado: `fonte: <medida> · final: <medida> · diferença: nenhuma`. **Verbo em `feito` com diferença nenhuma reprova o veredito**, porque infla o placar da entrega: conformidade medida não é efeito medido. **A linha de cada verbo sai nesta forma, colada:** `<verbo> | fonte: <medida> · final: <medida> · diferença: <o quê>`, com duração, resolução, número de cortes ou palavras de legenda como medida, e `diferença: nenhuma` obriga `nao_aplicavel`. **"Editar" não é verbo próprio: é a soma dos outros**, e marcá-lo como `feito` infla o placar sozinho. O `checar_entrega.py` conta em `feito` só o verbo cuja linha traga `diferença:` com valor diferente de `nenhuma`, e é dessa contagem que sai a exigência do `PEDIDO-DE-GRAVACAO`: um reencode 1080x1920 → 1080x1920 marcado como editado deixou a entrega tecnicamente conforme, materialmente vazia, e sem o pedido que ela precisava |
| Prova de cada emenda | `python3 scripts/06_inspect_cuts.py` rodou e gravou os quadros; sem prova individual, reprova |
| Auditoria visual | `python3 scripts/06_audit.py <final.mp4> <pasta>/audit 12 "<marcos>"` rodou AGORA sobre o arquivo entregue |
| Perfil de auditoria pela forma | a auditoria rodou no perfil da forma escolhida, e o relatório declara em 1 linha qual perfil rodou e qual critério se aplica a ela (a tabela "Perfil de auditoria por forma" abaixo) |
| Gancho com lastro de fala | a frase do gancho tem, ao lado dela, o segundo da gravação em que o dono a diz; texto que já vinha queimado no vídeo bruto nunca vira gancho |
| Cor da tarja e da legenda | o hex usado está colado ao lado do hex da identidade do dono, e pertence à paleta declarada; sem identidade declarada, é preto e branco |
| Texto na tela | gancho, faixa e card passaram pelo crivo anti-IA (por **soft-critico-copy** quando instalada, senão pelo crivo curto das Regras Invioláveis) |
| Plano visual | `python3 scripts/08_gate_visual_plan.py` aceita o plano de apoios. **Insumo mais curto que o recorte mínimo do gate é caminho previsto, não falha:** grave `short_input_reason: "<duração medida e o comando que mediu>"` no plano e o gate pula os critérios de recorte e de blocos semânticos e **baixa a cota de decisões de 8 para 1**, cobrando só os que se aplicam: um bruto de 20 segundos não comporta 8 decisões visuais, e cobrar as 8 assim mesmo só premia quem inventa decisão pra passar. Com o recorte cheio a cota de 8 a 12 continua valendo inteira. Exportar com esse gate em falha continua proibido, e a razão do insumo curto vai colada no relatório |
| Testes da própria skill | `python3 tests/test_mechanisms.py` e `python3 tests/test_visual_plan_gate.py` passam, quando você mexeu em script desta pasta |
| Entrega dupla | o MP4 e o `relatorio-edicao-<slug>.md` existem, com o caminho dos dois na resposta |

**Perfil de auditoria por forma.** O `06_audit.py` cobra critérios diferentes conforme a composição, e cobrar faixa de b-roll numa forma que não tem b-roll reprova entrega legítima. Escolha o perfil pela variável `SOFT_EDITOR_AUDIT_MODE` ANTES de rodar, e declare no relatório qual perfil rodou.

| Forma | Perfil (`SOFT_EDITOR_AUDIT_MODE`) | O que a auditoria cobra, e o que ela NÃO cobra |
|---|---|---|
| **A · Tela cheia de prova** | `screen_captioned` | cobra a prova legível em tela cheia e a posição da legenda. Não cobra faixa de b-roll, apresentador nem gancho |
| **B · Composição adaptativa** | `standard` (o default) | cobra apresentador, faixa de b-roll no rodapé e faixa de gancho. É a única forma em que os três valem |
| **C · Topo-fixo com slides e telas** | `split_no_hook` | cobra o split estável com apresentador em cima e slide embaixo. Não cobra gancho separado nem CTA |
| **D · Conteúdo puro** | `forma_d` | cobra só a tela cheia e a headline dos 3 primeiros segundos. **Não cobra faixa de b-roll nem apresentador visível: a Forma D não tem os dois por definição** |

Rodar a Forma D no perfil `standard` reprova a peça por faltar o que ela nunca deveria ter. Perfil errado no relatório reprova o gate.

**Os 3 resultados da auditoria visual, e o que cada um autoriza:**
- **PASSA (exit 0):** entregue o MP4 mais `audit/mosaico.jpg`, os dois caminhos em linhas isoladas. Selo permitido, exato: "Auditoria visual: PASSA (N frames). Prova: `<mosaico>`". Nada de "sync 0,000 ms", isso não foi medido. **A auditoria visual mede enquadramento, não o pedido:** antes de usar o selo, confira a tabela de verbos do pedido do gate acima. **Verbo do pedido em `não feito` proíbe o selo `PASSA`**, mesmo com exit 0: o selo vira "Auditoria visual: PASSA COM PENDÊNCIA (N frames). Pendências: `<verbo> não feito porque <motivo medido>`", e a mesma linha abre o relatório. `"problemas": []` numa peça que não cumpriu um verbo do pedido é veredito falso e reprova a entrega.
  - **O selo do relatório e o `audit/veredito.json` são a mesma afirmação em dois formatos, e divergir entre os dois reprova a entrega.** Verbo do pedido em `não feito` obriga `"status": "PASSA_COM_PENDENCIA"` no JSON e uma entrada por verbo em `"problemas"`, na forma `{"verbo": "<verbo>", "motivo_medido": "<comando e saída>"}`. Quem grava isso é o script, não a memória: rode `python3 scripts/06_audit.py <mp4> <pasta-audit> <n> "" <verbos.json>`, passando o arquivo de verbos do gate (uma lista de `{"verbo": ..., "estado": "feito|nao_aplicavel|nao_feito", "motivo_medido": ...}`), e ele reconcilia o status sozinho antes de escrever o arquivo.
  - **Checagem colada no relatório, antes de entregar:** `python3 -c "import json;d=json.load(open('audit/veredito.json'));print(d['status'], len(d['problemas']))"`. Saída `PASSA 0` com qualquer verbo em `não feito` reprova. E o status impresso nessa saída tem que ser a mesma palavra que abre o relatório: relatório dizendo `PASSA COM PENDÊNCIA` sobre um JSON dizendo `PASSA` é o veredito falso que esta regra existe pra matar.
- **REPROVA (exit 1):** NÃO está pronto. Corrija o problema apontado em `veredito.json` e rode a auditoria de novo, um ciclo. Persistiu ou ficou ambíguo, mande o mosaico e os motivos pro dono decidir.
- **INDISPONÍVEL (exit 2, visão fora do ar ou ausente):** entregue o MP4 e o mosaico com o aviso literal "não consegui auditar visualmente (visão indisponível), confere no mosaico". SEM selo.

Custo da auditoria: zero em API paga, roda na conta que o ambiente já tem. Soma 40 a 100 segundos ao pipeline. Detalhe: amostre 0,8 segundo DEPOIS de cada transição; frame no meio de uma fusão parece dupla exposição e reprova à toa (o `06_audit.py` já trata isso pelos marcos).

**Quando os verbos saem TODOS em `nao_feito` ou `nao_aplicavel`, a entrega não termina no MP4.** O bruto reencodado é caminho previsto e pode estar correto, e ainda assim o dono não publica nenhum dos dois arquivos: falta matéria-prima, não falta edição. Nesse caso a entrega leva junto `PEDIDO-DE-GRAVACAO-<slug>.md`, com as 3 a 5 falas (tiradas da fala real do dono no perfil ou nos insumos, nunca escritas do zero), o enquadramento, o que aparece e o que não aparece em cena, e a duração alvo. **Entrega com zero verbos em `feito` e sem esse arquivo sai marcada como PARCIAL**, e a marca abre o relatório.

**As falas do roteiro saem na ORDEM NATURAL de um take (checagem que reprova a ordem trocada).** As 3 a 5 falas do `PEDIDO-DE-GRAVACAO` são gravadas em sequência, então a ordem no arquivo é a ordem em que o dono fala na câmera: abertura ou gancho primeiro, corpo no meio, chamada no fim. Uma rodada listou a saudação ("Oi gente") no fim da lista, e a lista não formava um take: o dono gravaria a abertura depois do fecho. Regra: a fala de abertura (saudação, gancho, quebra de padrão) é sempre a fala 1; o CTA ou fecho é sempre a última. Checagem antes de fechar: numere as falas e escreva `fala 1: <tipo> · última fala: <tipo>`; fala 1 que não seja abertura ou gancho, ou saudação em posição diferente da 1, reprova e reordena. Cole `falas na ordem do take? sim/não`.

**Checagem mecânica antes de mostrar, com as duas saídas literais coladas no relatório:**

```
python3 -c "import json,glob;f=(glob.glob('verbos-pedido.json')+glob.glob('audit/verbos*.json')+glob.glob('audit/veredito.json'))[0];d=json.load(open(f));v=d if isinstance(d,list) else d.get('verbos',[]);print('verbos em feito:', sum(1 for x in v if x.get('estado')=='feito'))"
ls <pasta> | grep PEDIDO-DE-GRAVACAO
```

**As duas saídas acima viram uma só, e ela tem exit:** `python3 scripts/checar_entrega.py <pasta>`. O script conta os verbos em `feito`, procura o `PEDIDO-DE-GRAVACAO` e compara as palavras da transcrição com as da legenda queimada, e sai com exit 1 quando qualquer uma das três reprova. Cole a saída no relatório. Em prosa estas duas linhas já foram puladas duas rodadas seguidas.

**Saída (1) igual a zero com saída (2) vazia é entrega incompleta:** o relatório não abre em `PASSA` nem em `PASSA COM PENDÊNCIA`, abre em `PARCIAL`, e o `PEDIDO-DE-GRAVACAO-<slug>.md` é escrito ANTES de mostrar. As duas saídas vão coladas no relatório mesmo quando o resultado é o esperado, porque é a saída vazia que prova que ninguém pulou o passo. Regra sem as duas linhas viradas em comando vira recomendação, e recomendação não segura entrega.

**E o `PEDIDO-DE-GRAVACAO` leva a headline pronta.** Junto das falas vai a headline aprovada pela régua R1 a R7 pro take futuro, escrita agora e colada no arquivo com a checagem ao lado (`gatilhos: <2 das 6 famílias> · veredito: passa`). O dono grava com a headline na mão, e a rodada seguinte entra com texto aprovado em vez de recomeçar pela escrita. **A headline não pode mudar a TESE do dono:** ela é recorte fiel do que ele diz, nunca uma versão que troca o sentido (ver a régua de fidelidade nas Regras Invioláveis).

## Regras invioláveis

- Apoio nasce da imagem, primeiro a imagem aprovada e só depois a animação. Nunca texto direto pra vídeo.
- A composição segue a matéria-prima. Nunca imponha divisão de tela, gancho, card ou apoio porque o vídeo anterior usou.
- Talking-head com apoio: enquadramento fechado, sem sobra acima da cabeça, legenda na altura do peito, apoio mudando a cada 2 a 3 segundos, virada de layout por flash no terço inicial.
- Lista aparece item por item. Legenda acende palavra por palavra. Os dois entram no manifesto e no gate.
- Cada apoio tem direção completa no manifesto. Campo ausente reprova no gate.
- Frase de apoio não duplica a legenda e não entra por obrigação. Sem frase, o manifesto registra o motivo. Transição decorativa é reprovada editorialmente.
- Fala compactada preserva palavras e tempos no manifesto. Toda edição grava um mapa explícito de cortes, com fade de 30 ms na entrada e na saída de cada trecho. Corte seco de áudio reprova.
- Legenda é a última camada visual.
- Imagem aprovada é verdade absoluta: o motor de animação só ANIMA, não recria. Prompt negativo obrigatório.
- Personagens sempre consistentes com `config/personagens.json`. O elenco fixo aparece em toda cena; extras entram conforme a fala.
- **A cena e o enquadramento de gravação só entram se vierem do `config/personagens.json` ou dos personagens do dono.** É PROIBIDO inventar a cena, o cenário ou o enquadramento e atribuir a uma fonte (config, perfil, insumo) que não diz aquilo: cena inventada com fonte alegada é o veredito falso que esta regra existe pra matar. Quando o campo do config está `[A CONFIRMAR]` ou vazio, a peça NÃO inventa a cena: usa o default DECLARANDO em 1 linha no relatório que é default (`cena: default, config sem cenário declarado`), ou marca a pendência pro dono. Checagem verificável antes de queimar: ao lado de cada cena ou enquadramento, aponte `config/personagens.json:<campo>` que o produziu, ou a palavra `default` com o motivo; cena com fonte apontada que o arquivo não contém reprova o render.
- **Texto que já está queimado no vídeo bruto nunca vira gancho.** A frase do gancho vem da FALA do dono ou do material dele. Texto que já aparece impresso no vídeo bruto (marca d'água, cartela de teste, identificação de arquivo, nome do arquivo, carimbo de câmera) nunca vira gancho, faixa nem legenda. Sem fala real no material, o vídeo sai sem gancho e o relatório declara o motivo em 1 linha. Checagem verificável antes de queimar: aponte, ao lado da frase do gancho, o segundo da gravação em que o dono a diz; gancho sem marca de tempo de fala correspondente reprova o render.
- **Headline e fala na tela são recorte FIEL do insumo: mudar o sentido reprova.** A headline, o gancho e a faixa de texto saem da fala real do dono, e o texto é substring do que ele diz, sem trocar o sentido. Uma rodada pegou "o joelho avisa no dia 12" e queimou "o joelho avisa ANTES do dia 12": a headline mudou a tese do dono, virou outra afirmação. É PROIBIDO editar o sentido pra ganhar gancho: cortar palavra pra encurtar vale, inverter o significado (um prazo exato virar "antes de", um número virar "mais de", uma condição virar outra) reprova. Checagem antes de queimar: ao lado da headline, cole a fala de origem literal (`<arquivo>:<trecho>`) e confirme que a headline é substring dela ou um corte que preserva o sentido; rode `grep -nF '<núcleo da headline>' <insumo>` pra provar o lastro. Headline cujo sentido diverge da fala de origem reprova o render. Cole `headline é recorte fiel da fala? sim/não · fala de origem: <trecho>`.
- **Palavra que entra na legenda sai da transcrição, e de mais lugar nenhum.** Quando a transcrição devolve menos de 5 palavras de fala, ou devolve só marcador (`[Música]`, `[Aplausos]`, silêncio), o verbo `legendar` fica `nao_aplicavel` com o motivo medido, e **nenhuma legenda é queimada**. É PROIBIDO escrever um `words.json` à mão, mesmo declarando que é demonstração: o arquivo entregue não carrega o relato junto, e o dono publica o pixel. Checagem antes de queimar, colada no relatório: `palavras na transcrição: N · palavras na legenda queimada: N`, e o segundo número maior que o primeiro reprova a entrega. Demonstração de mecanismo, quando ela for útil, sai em arquivo separado com sufixo `-DEMO` no nome e a palavra DEMO queimada no primeiro quadro. Quem confere é o script: `python3 scripts/checar_entrega.py <pasta>` sai com exit 1 e a entrega não sai.
- **Texto de tela também não é a descrição do serviço, nem o campo de promessa do perfil copiado cru.** "Treino em casa, 3x por semana" ou "consultoria financeira para médicos" é a linha de catálogo do produto, e ela rotula o serviço sem afirmar nada. **Antes de queimar qualquer texto na tela, rode a régua de títulos R1 a R7 sobre ele e cole as respostas no relatório**, uma linha por regra; a R2 (título que só descreve) e a R7 (um copywriter assinaria) decidem sozinhas. Sem fala no material e sem texto aprovado pela régua, a peça sai **sem texto na tela** e o relatório declara em 1 linha por quê: esse é caminho previsto, não falha. Texto queimado sem as respostas da régua no relatório reprova o render. **Na R2, teste também apagando o verbo inicial: se o que sobrar for a ficha do produto, reprova.** E o gatilho nomeado sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não é gatilho e não conta.
- **A cor da tarja e da legenda sai da identidade do dono.** Sem identidade declarada, use preto e branco. Vermelho, ou qualquer cor fora da paleta declarada, só quando o dono pede. Checagem verificável antes de queimar: cole o hex usado na tarja e na legenda ao lado do hex da identidade do dono; hex fora da paleta declarada reprova o render.
- **Texto na tela passa pelo crivo anti-IA antes de queimar** (gancho, faixa, card). Com **soft-critico-copy** instalada, mande o texto por ela. Sem ela, o crivo curto roda aqui: leia a frase em voz alta e reprove se tiver travessão, palavra de folheto que ninguém fala em conversa, abertura de manual ("neste vídeo você vai aprender"), três adjetivos em sequência, ou promessa sem número nem prova. Reescreva na fala do dono, com as palavras que ele usou na gravação.
- **Mostrar, não afirmar.** "Conferido" ou "auditado" só existe se o `06_audit.py` rodou AGORA sobre o arquivo entregue e devolveu PASSA, com o mosaico anexo na mesma mensagem. Selo sem mosaico é mentira, mesmo com o vídeo bom.
- **Você não tem olhos.** Nunca descreva o conteúdo de um frame que nenhuma ferramenta de visão devolveu. Proibido alegar sincronia, milissegundos, frames conferidos ou qualidade visual de qualquer coisa que não passou pelo `06_audit.py`.
- **Conclusão honesta.** Auditoria reprovada ou não rodada significa entrega sem selo. Reprovada: corrija, ou vá pro dono com o mosaico e os motivos. Indisponível: entregue com o aviso. "Concluída" por cima de reprovação não existe.

## O que esta skill NÃO faz

Se a skill de destino não estiver instalada, esta faz o mínimo aqui, do jeito escrito no passo correspondente.

- Escrever ou corrigir o roteiro, o que falar, a ideia do vídeo: **soft-conteudo-reels**. Nunca reescreva roteiro aqui dentro.
- Criticar headline, gancho, card ou qualquer texto público antes de queimar: **soft-critico-copy**. Sem ela, o crivo curto das Regras Invioláveis roda aqui.
- Identidade visual, paleta, tipografia, personagens, direção das imagens: **soft-designer**. Sem ela, o Passo 0.2 monta o elenco por entrevista.
- Arte estática, carrossel, banner: **soft-designer**.
- Página, landing, checkout: **soft-funil-landing**.

## Arquivos desta skill
- `references/regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.

`references/EXEMPLO-FIM-A-FIM.md` · `references/regua-adaptativa.md` · `references/metodo.md` · `references/playbook-edicao.md` (tabela de cortes por tempo, critérios de auto-aprovação e teto 3, instrução por tempo, memória de estilo, régua entre motores, correção do timestamp por palavra) · `references/recursos-geracao.md` · `references/direcao-visual-longa.md` · `references/forma-topo-fixo.md` · `templates/topo-fixo/` · `config/personagens.example.md` · `config/estilos.md` (memória de estilo por forma e personagem) · `config/keys.example.env` · `scripts/` (00 corte de silêncio, 01 imagens, 02 animação, 03 montagem, 04 final, 05 gancho, 06 auditoria e inspeção de cortes, 07 gate da edição, 08 gate do plano visual) · `tests/test_mechanisms.py` · `tests/test_visual_plan_gate.py`

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
