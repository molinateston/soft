---
name: soft-espiao
description: >-
  Pesquisa o que está vendendo no nicho do dono, explica por que funciona e diz o que modelar sem copiar: puxa anúncios da biblioteca da Meta, pontua os sinais de venda (cópias, páginas, variações, views, tempo no ar), acompanha em planilha semanal, desmonta anúncio, VSL ou funil concorrente e entrega o brief de modelagem. Entrega o Radar do mercado em .md e a planilha em CSV. Use quando o pedido for: "o que está vendendo no meu nicho", "espiona esse concorrente", "acha anúncio escalado", "biblioteca de anúncios", "desmonta esse anúncio", "por que esse anúncio funciona", "quero modelar esse anúncio". NÃO use pra: headline ou gancho do zero (soft-conteudo-headlines); o lote de criativos (soft-criativo-campeao); subir, ler ou escalar a campanha do dono (soft-trafego-meta); auditar o perfil do dono (soft-consultoria-instagram); decidir sobre o que postar (soft-conteudo-planner); avaliar ou desenhar oferta, stack e preço, inclusive a do concorrente (soft-plano-ofertas). Leia e siga o fluxo inteiro do SKILL.md.
---

# Espião: o que vende no nicho, por que vende e o que modelar

Esta skill responde três perguntas do dono: o que está vendendo no meu nicho, por que funciona e o que eu modelo. Ela acha os anúncios que dão sinal de venda, desmonta o que há por trás e devolve um brief pro anúncio do dono, com o princípio e sem copiar texto, imagem ou promessa.

**Regra de ouro:** anúncio que vende deixa rastro. Quem anuncia só duplica, espalha e varia o que está dando dinheiro. Um sinal sozinho engana; os sinais somados, medidos em data, apontam o que vale modelar.

**O que é "pronto" (por ação).** Ação 1 e 2: `radar-<nicho>.md` e `planilha-<nicho>.csv`; Ação 3: `ficha-<anunciante>-<n>.md`; Ação 4: `brief-<n>.md`. Em todas: link e data em cada anúncio citado, o gate do fim passado e o lint com exit 0 em cada `.md`. Sem isso, diga o que falta em vez de "pronto".

**Mensagem ao dono (chat e Telegram).** Abre com `Pronto:` (1 linha), `Abra primeiro:` (1 arquivo) e `Falta você responder:` (`as N perguntas abaixo` ou `nada`); depois, no máximo 4 linhas do que muda a decisão (o que modelar primeiro, o que saiu e por quê); fecha com `Perguntas pra você`, no máximo 3, numeradas, cada uma escrita uma vez só. Cabe em 12 linhas. A lista de anúncios, os pontos e o brief moram nos arquivos; nome de script, gate e lint ficam fora da mensagem.

**Multimotor.** Tudo aqui roda igual no Claude e no Codex. Cada comando de shell tem o caminho sem shell ao lado; siga o que o ambiente permitir e declare em 1 linha qual caminho usou. Esta skill é a pasta que contém este arquivo e a subpasta `scripts/`; rode os comandos a partir dela.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício inteiro, do pedido ao brief, com a planilha e o gate preenchidos.

## Onde estou: os 3 ambientes (a mesma skill, entrega diferente)

| Ambiente | Tem shell? | O que pergunta, nesta ordem | O que faz | Entrega |
|---|---|---|---|---|
| só chat | não | as da ação, pela triagem da condução, numa mensagem só | conduz a busca manual passo a passo e pontua os sinais com o que o dono colar | o Radar e a planilha como texto no chat, prontos pra copiar |
| com shell | sim | as mesmas, só as que faltarem depois de ler o perfil | roda `scripts/buscar_anuncios.py`, grava o CSV, pontua e desmonta | os dois arquivos na pasta de trabalho, com o caminho na resposta |
| dentro de um agente de conversa | sim | uma mensagem só; aceita áudio, link e print | igual ao ambiente com shell; o acompanhamento semanal pode rodar agendado | a "Mensagem ao dono", com o caminho completo dos arquivos |

- **Precisa de terminal:** puxar anúncios pelo script (com `APIFY_TOKEN` no ambiente), a planilha em arquivo, o recálculo dos pontos e a conferência de distância do brief.
- **Sem terminal:** o dono abre a biblioteca de anúncios da Meta no navegador, busca os termos que a skill escreveu e cola links e prints; a skill preenche a planilha no mesmo formato de colunas e aplica a mesma régua. Sem token o script também para com erro claro e aponta esse caminho.

## A condução

Modo direto por padrão, sem anunciar o modo. **Triagem antes de produzir:** leia o perfil ou o brain do dono quando existir; o que ele e o pedido respondem não vira pergunta. Falta dado que muda a entrega ou o risco (o nicho, a frase do cliente, o link do anúncio a desmontar, a prova do dono pro brief)? UMA mensagem antes de produzir, no máximo 3 itens, cada um dizendo o que muda com a resposta. O resto vira `[A CONFIRMAR: o quê]` com a premissa em 1 linha, e a pergunta vai junto da entrega. Promessa proibida (cura, prazo de resultado, ganho garantido, antes e depois em saúde ou corpo) nunca vira pergunta: o brief sai na versão segura.

- **Ensina enquanto faz:** a cada anúncio que entra no Radar, uma linha do porquê ("entrou porque tem 9 cópias e 3 páginas rodando o mesmo texto; tempo no ar sozinho não bastaria").
- **Puxa o material bruto:** pedido raso ("vê o que o mercado faz") ganha a pergunta concreta: "me manda o link de 1 concorrente que te incomoda e a frase que o teu cliente usa pra descrever o problema".
- **Oferece refinar no fim:** "quer que eu desmonte algum desses a fundo, ou que eu acompanhe os candidatos até semana que vem?"

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Ação |
|---|---|
| "o que está vendendo no meu nicho", "acha anúncio escalado", "o que os concorrentes anunciam", "espiona esse concorrente" | **1 · RADAR** |
| "acompanha esses anúncios", "planilha de espionagem", "o que mudou essa semana" | **2 · ACOMPANHAMENTO SEMANAL** |
| "desmonta esse anúncio", "por que essa VSL funciona", "o que tem por trás desse funil" | **3 · ENGENHARIA REVERSA** |
| "quero modelar esse anúncio", "como eu faço um desses pro meu produto" | **4 · MODELAGEM** (passa pela 3 antes, se o anúncio não foi desmontado) |

Pedido ambíguo ("me ajuda a ver a concorrência"): pergunte UMA coisa, "você quer o mapa do que vende agora, acompanhar alguns anúncios por dias, desmontar um específico ou já o brief pra modelar?", e siga pela resposta.

**Perguntas de entrada, pela triagem (só o que a ação usa e ainda falta):** Ação 1, o nicho em 2 a 4 palavras e a frase que o cliente usa pra descrever o problema (os dois mudam a busca), mais concorrentes conhecidos e a idade do comprador se souber; Ação 2, a planilha anterior; Ação 3, o link ou o vídeo; Ação 4, o produto, a prova e a promessa do dono. O que faltar vira `[A CONFIRMAR: o quê]`.

---

## Ação 1 · RADAR (pesquisa pontual de um nicho ou concorrente)

**Leia antes:** `references/busca-na-biblioteca.md` e `references/sinais-de-venda.md`.

**R1 · Termos.** Escreva de 4 a 6 buscas de 2 palavras soltas, sem aspas, cruzando 3 famílias: **mercado** (causa, erro, método, truque, revela), **nicho** (o tema) e **oferta** (o nome do gancho ou do mecanismo de um concorrente que já vende). A biblioteca transcreve o áudio, então a busca acha a palavra dita no vídeo em qualquer ordem. Cada palavra a mais piora a busca: 3 palavras só com motivo escrito.

**R2 · Coleta.** Confira o token sem imprimir: `test -n "$APIFY_TOKEN" && echo token: ok || echo token: ausente`. O token vem do ambiente do agente; nunca peça no chat nem escreva o valor no comando. Com `ok`:

```
python3 scripts/buscar_anuncios.py --termo "erro violao" --termo "metodo violao" --max 20 --saida planilha-<nicho>.csv
```

Concorrente nomeado: `--pagina-id <id>` traz até `--max` anúncios ativos da página (padrão 20); o script para acima de 150 itens por chamada. Sem token ou sem shell: caminho manual do bloco "Onde estou". Cole a última linha do script (`anuncios na planilha: N · vendendo: N · candidato: N · observar: N`).

**R3 · Limpa o ruído.** Busca por palavra traz anúncio de outro assunto. Marque na coluna `nota` como `fora do eixo: <motivo>`; linha marcada fica na planilha (a próxima coleta não a traz de volta como novidade) e não entra no Radar. **Black sai antes dos pontos:** link que abre página diferente da anunciada, falso especialista, cura ou prazo garantido, rede de páginas de nome genérico ganham `descartado: black: <motivo>`, e sinal de venda nenhum devolve o anúncio à modelagem. Anúncio que o dono trouxe sai com veredito em 1 linha no Radar (modelar, observar ou descartado com motivo); nenhum some.

**R4 · Pontua os sinais.** Aplique a régua de `references/sinais-de-venda.md`: cópias (7 a 10), mesmo anúncio em várias páginas, variações circulando, views subindo, tempo no ar. **Tempo no ar entra somado, nunca sozinho.** Recência pesa: começou há menos de 30 dias e já tem cópias vale mais que um anúncio antigo parado. "Vendendo" pede 3 pontos com 2 sinais distintos além do tempo. Régua de partida; a planilha do nicho do dono a substitui (`sinais-de-venda.md`, topo).

**R5 · Técnica ou personalidade.** Pra cada anunciante do topo, decida: vende por técnica (anúncio ativo há semanas, especialista pouco conhecido fora do nicho) ou por personalidade (pouca mídia paga, audiência grande). **Quem vende por personalidade sai da lista de modelagem** do dono sem a mesma audiência, com o motivo escrito. Sem o número de seguidores na conversa ou no print, marque `técnica? audiência não vista` e deixe o anunciante na modelagem com essa nota.

**R6 · Formato fora do nicho.** Rode quando o pedido é vídeo, quando 3 ou mais dos anúncios `vendendo` usam o mesmo formato, ou quando o dono trouxe anúncio de fora do nicho (esse entra sempre na leitura de formato): gaste a busca de formato do `references/modelagem.md` (viral do orgânico, comentários que elogiam um elemento). Formato de fora vale mais que o do concorrente, que o mercado já cansou de ver.

**R7 · Escreve o Radar.** Estrutura fixa em `references/radar-modelo.md`: o que vende agora (3 a 5 anúncios, cada um com sinais, link, data e o porquê em 1 linha), o padrão que se repete (ângulo, formato, oferta), a linguagem literal do público que apareceu, o que o dono modela primeiro e o que fica em observação.

## Ação 2 · ACOMPANHAMENTO SEMANAL (planilha com sinais medidos ao longo dos dias)

**Leia antes:** `references/sinais-de-venda.md`, seção "Acompanhamento".

1. Rode a coleta na mesma planilha com `--acrescentar`. O script liga a coleta nova à anterior do mesmo anúncio e preenche `copias_antes`.
2. Views: o dono (ou a skill, quando o vídeo mostra o número) anota `views` na linha do dia. Depois rode `python3 scripts/buscar_anuncios.py --recalcular planilha-<nicho>.csv` pra pontuar o sinal de views subindo. Sem shell, compare as duas colunas no olho com a mesma régua.
3. **Sinal medido vale mais que sinal visto uma vez.** Candidato só sobe pra "vendendo" com o sinal repetido em 2 coletas ou mais. Se o script marcou `vendendo` um id que tinha só uma coleta anterior como `candidato`, confira o sinal nas duas linhas antes de mover pro topo do Radar.
4. **Anúncio que some da biblioteca não prova fracasso:** cai por reprovação e por troca de metadado. Marque `sumiu em <data>` na nota e siga olhando as variações dele.
5. Guarde cada achado no arquivo de referências do dono, por nicho e por formato (link, print e, quando der, o vídeo, que é estudo interno: nunca sobe em anúncio nem sai da pasta do dono). Sem isso a pesquisa se perde em uma semana.

**Entrega:** a planilha atualizada e um trecho novo no topo do Radar: `o que mudou desde <data>`, com o que subiu, o que apareceu e o que sumiu.

## Ação 3 · ENGENHARIA REVERSA (anúncio, VSL ou funil concorrente)

**Leia antes:** `references/engenharia-reversa.md` (a ficha completa).

**Só desmonte pra modelar anúncio da classe `vendendo`.** Fora dela pode ser oferta quebrada; se o dono insistir, a ficha sai com o aviso na primeira linha. Sem o anúncio na planilha: com shell e token, rode a coleta com `--pagina-id` da página dele e cole a linha; sem shell, peça o link da biblioteca e o print com "Veiculação iniciada em" e "N anúncios usam este criativo"; sem nenhum dos dois, a ficha abre com `sinais não medidos`.

A ficha tem 8 campos, todos com o que se viu e onde: ângulo · gancho (os primeiros 3 a 5 segundos, transcritos pra estudo) · formato · estrutura invisível (frase a frase, a função de cada uma: credibilidade, história, prova, mecanismo, chamada) · mecanismo · oferta (preço, bônus, garantia, parcelamento) · página e funil (VSL, quiz, carta, checkout, o que aparece depois da compra) · técnica ou personalidade. O que não dá pra ver (margem, verba, upsell escondido) sai como `não visível`, nunca como palpite. O campo oferta é leitura do que se vê; comparar ou desenhar oferta vai pra **soft-plano-ofertas** no próximo passo.

## Ação 4 · MODELAGEM (vira brief pro anúncio do dono)

**Leia antes:** `references/modelagem.md` (os 3 níveis, o que pode e o que nunca vem de fora, o molde do brief).

1. **Escolha o nível e escreva o motivo:** rasa (troca gancho e formato de um validado), estudiosa (esqueleto frase a frase com as palavras do dono) ou de nicho vizinho (outro nicho com a mesma estrutura de crença). Nicho sem vizinho de crença só se modela dentro dele.
2. **Separe o que se leva do que é do dono.** Leva: estrutura, ângulo, tipo de prova, ordem dos argumentos, formato. Do dono, com origem apontada: história, prova, número, nome do produto, promessa e toda frase.
3. **Escreva o brief** no molde da reference: o princípio em 1 frase, o nível, o que se leva, 3 ganchos na voz do dono, o corpo em tópicos, a prova do dono, o CTA, o destino e o que medir nos primeiros dias.
4. **Confira a distância.** Com shell, salve o texto do anúncio de referência em `ref-<n>.txt` e rode `python3 scripts/checar_distancia.py --referencia ref-<n>.txt --brief brief-<n>.md`. Exit 1 lista as sequências repetidas: reescreva e rode de novo. Sem shell, compare frase a frase e cole `frases iguais à referência: 0`.

**O próximo passo depois do brief.** Confira se a skill irmã está instalada (a lista de skills do agente, ou `ls` na pasta que contém esta skill, procurando `soft-criativo-campeao/SKILL.md`). Instalada, aponte: lote de anúncios pela **soft-criativo-campeao**, roteiro de VSL pela **soft-funil-vsl**, oferta como stack e preço pela **soft-plano-ofertas**. Sem elas, o brief já basta pro dono gravar ou mandar pro editor, e o relato diz isso em 1 linha.

---

## Gate (roda antes de toda entrega; só `não` volta a peça)

Cole cada linha com `sim`, `não` ou `n/a: <ação sem esse arquivo>`. Linhas 1 a 6 valem pro Radar, 7 a 9 pro brief, 10 a 12 pra toda entrega.

1. (Radar) Todo anúncio citado tem link da biblioteca (ou print identificado) e data da coleta, e todo anúncio que o dono trouxe tem veredito?
2. (Radar) Todo anúncio marcado "vendendo" tem 3 pontos ou mais, com 2 sinais distintos além do tempo no ar, e nenhum black ficou na modelagem?
3. (Radar) Nenhum anúncio entrou no topo só por tempo no ar?
4. (Radar) A data da coleta aparece no Radar e na planilha, e o Radar avisa que a biblioteca mostra só o que está no ar hoje?
5. (Radar) Todo anunciante do topo foi marcado técnica ou personalidade, e os de personalidade saíram da modelagem com motivo?
6. (Radar) A planilha CSV tem as colunas do modelo (`--modelo`) e todo anúncio citado no Radar está nela com os mesmos pontos?
7. (brief) O brief tem o princípio escrito em 1 frase e o nível de modelagem com motivo?
7b. (brief) Com 3 briefs ou mais, ao menos um é de formato de fora do nicho?
8a. (brief) `checar_distancia.py` exit 0 sobre o brief inteiro, ou a comparação frase a frase colada?
8b. (brief) Nome de produto, mecanismo ou personagem do concorrente no brief: 0, com `grep -niF '<nome>' brief-<n>.md` por nome anotado na ficha?
9. (brief) Toda promessa, número e prova do brief tem origem no material do dono, ou sai `[A CONFIRMAR]`, e nenhum tipo de prova barrado no nicho (antes e depois de corpo ou saúde, cura) foi levado?
10. Número de concorrente (cópias, dias, views, preço) aparece como sinal, sem nenhuma frase que prometa venda ao dono por causa dele?
11. Nenhuma sugestão de cloaker, conta falsa, compra de conta, link de exibição trocado ou contorno de reprovação?
12. Lint anti-IA com exit 0 em cada `.md` entregue, com a linha `<arquivo>: exit 0` colada?

## Regras duras

1. **Nunca copiar texto, imagem ou promessa.** Da referência vem o princípio; as palavras, a prova e a promessa são do dono. Anúncio clonado também perde no leilão pra quem tem mais verba.
2. **Nunca black, cloaker, conta persona falsa, compra de conta, link de exibição diferente do destino ou contorno de reprovação.** Pedido nessa linha recebe a recusa em 1 frase e a alternativa limpa.
3. **Número de concorrente é sinal, nunca garantia.** O Radar diz "dá sinal de venda", nunca "vai vender pra você". Faturamento de terceiro não vira projeção do dono.
4. **Tempo no ar nunca decide sozinho.** Anúncio bom cai por reprovação; anúncio velho pode seguir no ar esquecido.
5. **Sem data, não é dado.** A biblioteca muda todo dia; achado sem data da coleta sai do Radar.
6. **Nome de concorrente fica no Radar e na planilha, nunca na copy pública do dono.**
7. **Pesquisa na rede do comprador.** A rede muda com a idade do avatar; buscar só onde o dono gosta de estar dá o mercado errado.

## Anti-padrões (sintoma, correção)

| Sintoma | Correção |
|---|---|
| "esse anunciante tem 40 anúncios ativos, está escalando" | quantidade de anúncios do anunciante não prova escala; pontue cada anúncio pelos sinais |
| busca de 5 palavras entre aspas voltou vazia | 2 palavras soltas, uma de mercado e uma do nicho |
| Radar lista o concorrente famoso do nicho como modelo | confira técnica ou personalidade; audiência grande vende até copy fraca |
| brief repete o gancho do concorrente trocando uma palavra | volta pro passo 2 da Ação 4 e escreve o gancho a partir da dor do dono |
| só o concorrente direto entrou na pesquisa de formato | busque formato fora do nicho no orgânico viral |

## O que esta skill NÃO faz

Se a skill de destino não estiver instalada, esta entrega o brief e para ali.

- Escrever o banco de headlines: **soft-conteudo-headlines**. Sem ela, os 3 ganchos do brief bastam.
- Produzir e renderizar o lote de anúncios: **soft-criativo-campeao**.
- Avaliar, comparar ou desenhar oferta, stack e preço, inclusive a do concorrente: **soft-plano-ofertas**. Sem ela, o campo oferta da ficha fica como leitura do que se vê.
- Subir, ler, pausar ou escalar a campanha do próprio dono: **soft-trafego-meta**.
- Auditar o perfil do próprio dono no Instagram: **soft-consultoria-instagram**.
- Decidir a pauta do mês de conteúdo: **soft-conteudo-planner**.

## Arquivos

`references/busca-na-biblioteca.md` (termos, coleta pelo script e manual, outras bibliotecas) · `references/sinais-de-venda.md` (a régua dos 5 sinais e o acompanhamento) · `references/engenharia-reversa.md` (a ficha de 8 campos) · `references/modelagem.md` (os 3 níveis, o viral do orgânico, o molde do brief) · `references/radar-modelo.md` (a estrutura do Radar) · `references/EXEMPLO-FIM-A-FIM.md` (caso fictício inteiro) · `references/fontes-do-metodo.md` (a origem de cada regra) · `scripts/buscar_anuncios.py` (coleta e pontuação) · `scripts/checar_distancia.py` (distância entre brief e referência) · `scripts/lint_copy.py` (gate anti-IA).

## Nome do arquivo e lint (vale em toda entrega)

- **Nome:** slug curto, minúsculas, hífens, sem acento: `radar-<nicho>.md`, `planilha-<nicho>.csv`, `ficha-<anunciante>-<n>.md`, `brief-<n>.md`.
- **Lint:** com shell, `python3 scripts/lint_copy.py <arquivo>` em cada `.md` gravado, o relato incluso, e cole `<arquivo>: exit N` por arquivo mais `arquivos linteados: N · exit 0: N`. Citação literal do concorrente, quando precisa entrar numa ficha, vai dentro de bloco de código cercado. Sem shell, confira no olho: zero travessão longo, zero verbo-freio banido, zero clichê de revelação; e feche com `anti-IA: conferido no olho (sem shell nesta rodada)`.
- **Arquivo do dono fora da pasta da skill.** Planilha, Radar e brief vão pra pasta de trabalho do dono, nunca pra dentro desta pasta.
