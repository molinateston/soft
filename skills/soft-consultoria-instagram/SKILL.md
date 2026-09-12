---
name: soft-consultoria-instagram
description: >-
  Audita um perfil do Instagram inteiro como sistema comercial e entrega a nota de 0 a 100 com cobertura declarada, o diagnóstico separando fato de hipótese, e as correções prontas de bio, link, destaques, fixados, CTA e séries editoriais, num relatório em markdown mais um HTML autônomo. Use quando o pedido for: "audita meu Instagram", "dá uma nota pro meu perfil", "por que meu perfil não converte", "analisa esse perfil", "meu Instagram tá bonito e não vende", "o que eu arrumo primeiro no perfil", "reescreve minha bio e meus destaques do que já está no ar". NÃO use pra: criticar UMA peça isolada (soft-critico-copy); diagnosticar o funil por número, CPL e meta (soft-negocio-metricas); verba e conta de anúncio (soft-trafego-meta); escrever carrossel, reel ou stories (soft-conteudo-carrossel, -reels, -stories); reconstruir posicionamento, bio e oferta do zero (soft-plano-posicionamento); arte (soft-designer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Consultoria de Instagram: o perfil inteiro, com nota e correção pronta

Esta skill audita um perfil do Instagram como sistema comercial: se ele é entendido, lembrado, acreditado e capaz de conduzir alguém ao próximo passo. Ela entrega uma nota de 0 a 100 com a cobertura de dados declarada ao lado, o diagnóstico do gargalo de maior impacto, e o texto pronto das correções.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

Ela separa sempre fato, declaração, inferência, hipótese e o que não pode ser determinado de fora. Métrica pública descreve o estado da peça, não prova venda nem causalidade.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra uma auditoria fictícia inteira em nicho neutro: o que foi coletado, o `audit-score.json` preenchido, a nota com cobertura, o diagnóstico e o texto pronto de bio e destaques. É o arquivo que calibra o formato antes da primeira pergunta.

**Anuncie o plano antes de começar.** Na primeira resposta, diga em uma frase o que vai acontecer: "vou coletar o perfil, pontuar as 10 dimensões, diagnosticar o gargalo principal e gerar o relatório em markdown e em HTML. Vou parar duas vezes pra você conferir." Quem pediu precisa saber as 4 etapas antes de responder a primeira pergunta.

**O perfil do dono vem do banco do agente.** Onde a auditoria precisar de objetivo comercial, oferta, ticket, público ou voz: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta do "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR]`. Nunca use produto, voz, número ou estética de outro cliente como padrão.

---

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o @ e os prints do perfil e eu faço a auditoria). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra a auditoria com o que o dono já colou. Se faltar um insumo que a auditoria não vive sem (o perfil em si, ou o que ele quer que o perfil faça), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez (o perfil, o objetivo comercial, a oferta, o público) antes de auditar.

A pergunta do modo é UMA por auditoria. As outras três partes entram nas etapas abaixo:

- **Ensina enquanto faz:** em cada nota que a auditoria dá (bio, destaque, grade), escreve UMA linha do porquê ("reprovo a bio porque ela diz o que você é, não o que resolve; bio que promete resultado converte visita em seguidor"), pra o dono corrigir sozinho na próxima.
- **Puxa o material bruto:** quando o dono descrever o público raso ("quem quer crescer no Instagram"), não segue no genérico. Pede o concreto: "me conta de UM seguidor que virou cliente, o que ele te falou quando te procurou, com as palavras dele?". A fala real ancora a auditoria.
- **Oferece refinar no fim:** depois de mostrar o diagnóstico, fecha com UMA linha de ajuste ("quer que eu reescreva a bio? sugira a grade? aprofunde um ponto? mexo só na parte que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Ação única · AUDITAR O PERFIL (4 etapas, 2 paradas)

**O que faz:** coleta o perfil, pontua as 10 dimensões da rubrica, diagnostica o gargalo de maior impacto e entrega o relatório com as correções escritas.

**Precisa de:** o endereço do perfil, sempre do dono · o objetivo comercial dele (o que esse perfil precisa fazer acontecer), do perfil/brain do agente ou perguntado · a data da auditoria · acesso a alguma fonte de coleta (a lista de 4 abaixo).

**Sem o insumo:**
- Sem o endereço do perfil: não existe auditoria. Peça e pare. É o único bloqueio duro.
- Sem objetivo comercial declarado: entrevista curta de 3 perguntas, uma por vez: o que você vende e por quanto · quem você quer que chegue nesse perfil · qual o próximo passo que você quer que a pessoa dê. Sem elas, a nota sai, mas o diagnóstico não tem alvo.
- Sem token e sem Node pro coletor: pule pra fonte 3 ou 4 da lista. O método da auditoria é o mesmo, muda só de onde o material entra, e a marcação `parcial` continua valendo.
- Sem NENHUM acesso ao perfil: a auditoria não roda no escuro. Peça ao dono os prints da grade, da bio, dos destaques e dos 3 fixados, e trabalhe com isso marcando cobertura `parcial`.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** quatro arquivos na pasta de trabalho.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.
1. `audit-score.json`, a pontuação por dimensão com a evidência de cada nota.
2. `relatorio.json`, o conteúdo já preparado que alimenta o montador do HTML. É insumo do pipeline, não peça de leitura do dono, mas ele existe no disco e conta como arquivo entregue: sem ele o `scripts/montar_relatorio.py` não roda.
3. `relatorio-<perfil>.md`, o relatório legível, na ordem do bloco "O corpo do relatório".
4. `relatorio-<perfil>.html`, autônomo, com o CSS embutido, que abre sem nenhum arquivo do lado.

**Checagem verificável antes de fechar.** Liste os 4 caminhos com o tamanho de cada um, nesta forma: `<arquivo> | existe? sim/não | bytes`. Arquivo faltando, a ação não terminou.

**Leia primeiro:** `references/rubrica.md` (as 10 dimensões, os pesos e a escala de 0 a 5) · `references/formato-de-entrega.md` (a ordem e os componentes do relatório).

**Profundidade:** `references/coleta-visual.md` (o que olhar em cada superfície) · `references/arquitetura-narrativa.md` (como o diagnóstico vira história única) · `references/sistema-visual.md` (a identidade fixa do relatório, que nunca é a do cliente) · `references/benchmark-metodologico.md` (só pra calibrar coerência funcional, nunca pra copiar personagem, estética, promessa ou oferta).

---

### Etapa 1 · COLETA

1. Defina o perfil, o objetivo comercial e a data da auditoria.
2. Abra o estado da auditoria com `python3 scripts/gerenciar_estado.py`, que grava o ponto de retomada. Salve o estado depois de cada peça e nunca repita item já marcado como concluído.
3. Se a auditoria for guiada, faça UMA pergunta por vez. Em decisão real, ofereça duas ou três rotas e recomende uma. Mostre um resumo do que entendeu a cada cinco respostas.
4. **Insumo declarado no perfil é fonte obrigatória, não opcional.** Antes de pontuar, liste os insumos que o perfil do dono nomeia (transcrição, caixa de entrada, reclamação, call, site, peças prontas) e, para cada um, cole `<arquivo> | lido: sim/não | o que rendeu: <dimensão ou 'nada'>`. **Auditoria de perfil que fecha com algum insumo declarado em `lido: não` sai marcada como PARCIAL, e a marca abre o relatório**, porque a voz publicada do dono e a fila de mensagens dele são evidência de rubrica e não contexto de apoio: a bio se audita contra o que ele já fala, não contra o que ele diz que fala.

Trabalhe na fonte mais direta disponível, nesta ordem:
1. dados internos que o dono autorizou;
2. coleta externa pelo script desta skill;
3. navegador conectado, quando o ambiente tiver;
4. material que o dono mandar (prints, exportação, texto colado).

O coletor roda em qualquer máquina com Node e acesso à internet:

```bash
export APIFY_TOKEN=<token de coleta>
node scripts/coletar_instagram.cjs <endereco-do-perfil> <pasta-de-saida> 30
```

O token vem da variável `APIFY_TOKEN`, de um `.env` na raiz desta skill, ou do caminho apontado por `APIFY_ENV_FILE`.

Colete bio, link, grade, fixados, até 30 posts, TODOS os slides dos carrosséis, transcrição dos reels da amostra, destaques relevantes e o destino do link.

**Marque `parcial`** quando faltar qualquer carrossel completo, transcrição de reel da amostra, destaque relevante ou o destino do link. Falta de acesso nunca equivale a ausência.

**O que acontece quando a cobertura fica abaixo do mínimo.** Cobertura ou confiança abaixo de 70% significa que a nota NÃO é definitiva, e isso não é um detalhe de rodapé, é a primeira coisa que o relatório diz. Nesse caso, três coisas mudam de uma vez: a nota sai marcada `preliminar` na abertura do relatório, cada dimensão sem prova recebe `score: null` e `evidence_quality: 0` em vez de nota baixa, e o relatório abre com a lista do que falta coletar pra fechar. O diagnóstico continua saindo, porque gargalo grande costuma aparecer com amostra pequena, mas nenhuma recomendação de prioridade se apoia em dimensão nula. **STOP:** pergunte ao dono se ele consegue liberar o que falta antes de você fechar a nota.

### Etapa 2 · EVIDÊNCIA E PONTUAÇÃO

Classifique cada conclusão relevante em uma das cinco marcas:

- `observado`: aparece diretamente na fonte;
- `declarado`: o dono informou, sem prova externa;
- `inferido`: sustentado por duas ou mais evidências observadas;
- `hipótese`: explicação plausível que precisa de validação;
- `não determinável externamente`: venda, conversão, alcance real, retenção, salvamento, mensagem direta, ou causalidade sem dados autorizados.

Monte o `audit-score.json` conforme `references/rubrica.md`. Toda dimensão pontuada exige evidência não vazia; dimensão sem prova recebe `score: null` e `evidence_quality: 0`.

```bash
python3 scripts/calcular_pontuacao.py audit-score.json
```

O programa recusa pontuação definitiva sem evidência, de propósito. Apresente nota, cobertura das dimensões, cobertura das fontes, cobertura geral, confiança e teto comercial.

**Piso de cobertura de dimensões.** `dimension_coverage_percent` abaixo de 80 reprova a auditoria antes da entrega, mesmo com `status: provisorio`. Dimensão nula por falta de dado é legítima; dimensão nula em bloco (mais de 1 em 5) significa que a rubrica não foi percorrida, e **rubrica não percorrida não dispara teto comercial, o que INFLA a nota por omissão**: um perfil sem link de captura e sem mecanismo nomeado sai com nota mais alta que um perfil pior, só porque ninguém olhou. Cole `dimensões preenchidas: N de M (mínimo 80%) · nulas com motivo declarado: N`. **Cobertura abaixo de 80 não se declara, se conserta.** Antes de entregar, percorra as dimensões nulas uma a uma e responda por escrito, pra cada uma: o dado que falta existe em algum insumo no disco (transcrição, caixa de entrada, site, peça pronta)? Se existe, preencha a dimensão com ele. Só depois de esgotar os insumos do disco a dimensão fica nula, e aí ela sai da conta do piso: recalcule a cobertura **sobre as dimensões determináveis** e cole `dimensões determináveis: N · preenchidas: N · nulas por dado inexistente no disco: N`. Entregar com cobertura abaixo de 80 sobre o universo cheio, mesmo declarando o furo, reprova: declarar o piso furado não cumpre o piso.

**A regra do `score: null` é checada pelo programa, não pela sua leitura.** O calculador sai com erro e `status: nota_invalida`, sem nota final, em três casos: cobertura abaixo de 70% com as 10 dimensões pontuadas e nenhuma em `null`; `evidence_quality: 1` uniforme em todas as dimensões com confiança abaixo de 70%; e dimensão pontuada cuja evidência é só `nao_determinavel_externamente`. Quando isso acontecer, a saída traz `invalid_reasons` e `missing_sources`: corrija o `audit-score.json` pondo `score: null` e `evidence_quality: 0` nas dimensões sem prova, e rode de novo. Não contorne o erro editando o número na mão e não apresente nota nenhuma ao dono enquanto o programa recusar, porque nota inflada por falta de prova é o pior defeito que esta skill pode entregar.

**STOP.** Mostre a nota com a cobertura ao lado e pergunte: "essa leitura bate com o que você vê? Tem alguma coisa que eu não consegui ver e você pode me mandar?"

### Etapa 3 · DIAGNÓSTICO

Priorize o gargalo de maior impacto, nesta ordem:

1. comprador, problema e tese;
2. mecanismo e diferenciação;
3. narrativa e vocabulário;
4. oferta, bio, link e próximo passo;
5. prova;
6. arquitetura editorial;
7. voz, ambiente e acabamento visual.

Cada recomendação responde três coisas: o que acontece hoje, o que fazer, e como medir. Entregue o TEXTO PRONTO da bio, do CTA, dos destaques, dos três fixados, da rota de conversão e das séries editoriais. Nunca invente preço, promessa, prova, cliente ou resultado.

**Palavra-chave de CTA não se inventa, e a grafia é literal.** Antes de prescrever qualquer CTA que peça uma palavra ("manda X no Direct", "envia Y no WhatsApp"), procure a palavra nos insumos do dono (transcrição, peça pronta, mensagem, site) e cole `palavra-chave: <literal> | origem: <arquivo:linha>`. Use a grafia EXATA, sem espaço a mais nem a menos: quem digita a palavra errada cai em lugar nenhum, e uma palavra com espaço é outra palavra para a automação que responde. **Sem origem no disco, é PROIBIDO escolher uma:** prescreva o CTA na versão que dispensa a palavra e leve a pergunta ao handoff.

**A bio passa pela régua de títulos como se fosse uma headline**, porque ela é o único bloco de copy que o dono cola sem editar e a peça mais vista do perfil. A checagem vai colada, uma linha por linha da bio: `linha N | afirma a mais: <o quê>`. **Bio cuja linha de promessa não carrega pelo menos 2 diferenciais do perfil do dono (tempo por sessão, frequência, lugar, ausência de equipamento, parte do corpo, público específico) reprova e volta pra reescrita:** a promessa genérica do nicho descreve o mercado inteiro, não este dono. Cole a contagem: `diferenciais na bio: N (mínimo 2)`. **A checagem sai no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega**, com as três contagens no fecho: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: o universo é a bio linha a linha, o CTA, cada título de post fixado e cada nome de série, contados antes de rodar. Nome fixo é achável por `ls`; seção no meio do relatório não é.

**Limite de escopo:** se a correção exigir reconstruir público, categoria, oferta ou posicionamento do zero, isso não é auditoria de perfil. Chame **soft-plano-posicionamento** e use a decisão dela como entrada. Se ela não estiver instalada, escreva o gargalo em 3 linhas, diga que ele está acima do perfil, e siga com as correções que cabem dentro do que já existe.

### Etapa 4 · ENTREGA

Gere o markdown e o HTML autônomo com o CSS embutido, a partir de `assets/report-template.html`:

```bash
python3 scripts/montar_relatorio.py --data relatorio.json --out relatorio.html
```

**O lint roda em TODA peça que o dono abre, e o HTML é a principal delas.** Antes de fechar, rode `python3 scripts/lint_copy.py` no `.md` E no `.html` gerado. O HTML precisa de uma passada extra, porque o gerador escreve o travessão como entidade HTML, e a entidade escapada passa reto por uma leitura no olho. As três formas que o gerador produz são a entidade nomeada do travessão longo, a do travessão médio e a numérica do mesmo caractere. Monte a busca pelas três a partir do próprio caractere, pra não redigitar entidade neste arquivo, e cole a saída:

```
python3 - <<'EOF'
import html, pathlib, sys
bruto = pathlib.Path('relatorio.html').read_text(encoding='utf-8')
print('entidades de travessao no HTML:', html.unescape(bruto).count(chr(8212)) + html.unescape(bruto).count(chr(8211)) - bruto.count(chr(8212)) - bruto.count(chr(8211)))
EOF
```

Cole a linha `arquivos linteados: N · exit 0: N · entidades de travessão no HTML: 0`. **Travessão em entidade conta igual a travessão literal**, e um `.md` limpo com um `.html` sujo é a peça suja: o HTML é o que o dono abre e imprime.

#### O corpo do relatório (sempre esta ordem)

1. leitura executiva;
2. a experiência de quem chega;
3. diagnóstico central;
4. sistema atual e sistema proposto;
5. os quatro trabalhos do perfil;
6. "Construa assim", o texto pronto. **Todo item desta seção sai como texto pronto pra colar, entre aspas ou em citação.** Descrição de tarefa ("refazer o post X citando o método", "gravar um reel sobre Y", "amarrar a peça ao método nomeado") NÃO é entrega: ou você escreve o título e a primeira linha, prontos, ou o item sai da seção. **Checagem verificável antes de fechar:** cada item da seção tem uma linha que o dono copia sem escrever nada, e a checagem conta `itens da seção: N · itens com texto colável: N (têm que bater)`. Parêntese de justificativa pode acompanhar o texto pronto, nunca substituir ele;
7. plano de 48 horas, 7 dias e 30 dias;
8. apêndice com a pontuação, as fontes e os limites.

Toda copy pública do relatório passa pelo crivo anti-IA antes de sair, por **soft-critico-copy** quando ela estiver instalada.

---

## Gate de qualidade (roda antes de entregar)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **O inventário varre o perfil do dono INTEIRO, não só os campos que esta entrega consumiu:** cada campo do perfil é uma linha, e campo com vários valores (paleta com 3 cores; oferta com preço, parcela, bônus e garantia) rende uma linha por valor. **Entrega cujo `Dados fornecidos: N` for menor que o número de campos do perfil recebido reprova sem análise de conteúdo.** Qualificar a linha ("relevantes ao objeto", "considerados para esta entrega") também reprova: o total é o total. **Onde a linha mora:** no arquivo que o dono lê. Quando a entrega é uma peça de copy publicável (headline, carrossel, slide, card, chat, roteiro, deck), a peça NÃO recebe a tabela: a tabela vai num arquivo irmão de handoff (`HANDOFF-<slug>.md`) e só a linha de fechamento fica na peça, no rodapé. Inventário só no relato de processo, sem a linha na entrega nem o handoff no disco, reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Fontes consultadas (esta skill pesquisa, então a seção é obrigatória).** A seção "Fontes consultadas" da entrega lista só o que foi de fato aberto neste turno, e cada linha traz o comando ou a chamada de ferramenta que abriu aquela fonte. Sem acesso à web no ambiente, a seção diz exatamente "sem acesso à web neste ambiente" e nada mais: nenhum domínio, nenhum nome de marca, nenhuma data de busca. Checagem verificável antes de fechar: conte as linhas da seção e conte os comandos registrados no relatório e escreva os dois números lado a lado, nesta forma: `fontes declaradas: N · comandos no log: N`. **Declarar 4 buscas com 1 comando no log reprova**, e o conserto é apagar as 3 linhas sem comando, nunca inventar o comando. **Cada linha de tabela sobre terceiro traz a consulta que a produziu e o trecho citado da página aberta.** Número (preço, prazo, prazo de entrega, volume, quantidade de alunos, faturamento) vindo de página de terceiro só entra com o trecho colado ao lado; sem trecho colado, o campo sai como `[A CONFIRMAR: exige abrir a página]`, e cravar o número mesmo assim reprova a entrega inteira. Memória de treino e inferência plausível não são fonte.


| Critério | Passa se |
|---|---|
| Testes da própria skill | `python3 scripts/test_calculadora.py`, `python3 scripts/test_estado.py` e `python3 scripts/test_relatorio.py` passam. São o gate automatizado desta skill e existem na pasta |
| Pontuação honesta | `python3 scripts/calcular_pontuacao.py audit-score.json` sai com código 0; se sair `nota_invalida`, nenhuma nota vai pro dono até o `audit-score.json` ser corrigido |
| Cobertura declarada | a nota aparece com cobertura e confiança ao lado, e sai marcada `preliminar` abaixo de 70% |
| Retomada | o estado preserva o ponto exato; rodar de novo não repete peça concluída |
| HTML fechado | nenhum `{{MARCADOR}}` sobrou no HTML, e o arquivo abre sem nenhum arquivo externo |
| Prova visual | os 2 arquivos `prova-desktop.png` e `prova-mobile.png` existem na pasta de trabalho, OU o relatório traz a linha literal `Prova visual: não gerada, não havia navegador no ambiente.` Ver o bloco "Como a prova visual é feita" logo abaixo |
| Crivo visual escrito, não declarado | **o crivo não se declara feito, ele se escreve.** Abra a prova mobile (390px) e escreva, obrigatoriamente, estas três linhas, cada uma com número ou com sim/não: (1) `título principal: N linhas`, e **acima de 4 linhas reprova e o título volta pro passo de escrita**; (2) `número principal da nota dentro do bloco? sim/não`; (3) `última seção visível sem corte lateral? sim/não`. **Crivo sem essas três linhas não conta como feito**, mesmo trazendo outras observações boas, e registrar só o que está certo é o jeito mais comum de um crivo escrito deixar passar o defeito que ele existia pra pegar. "Conferido, sem problemas" não conta |
| Régua de títulos na copy prescrita | bio, CTA, títulos de post fixado e nomes de série passaram pela régua de títulos (`references/regua-de-titulos.md`), listados com `<título> \| gatilho: <qual> \| veredito: passa` ou `\| reescrito de: <versão anterior>`. **O gatilho sai da lista fechada das 6 famílias, e ela é esta, sem sétima:** `Recompensa`, `Mistério`, `Crença`, `Disrupção`, `Popularidade`, `Reconhecimento`. **Formato (bastidor, lista, tutorial, print), atributo (especificidade, autoridade, clareza, urgência, concretude, utilidade) e tema (custo, tempo, dor, pausa, identificação, ação, alívio) NÃO são gatilhos:** o gatilho é a família psicológica que faz o leitor parar, e só essas seis contam. Título com dois de fora da lista fica com zero gatilhos rastreáveis e volta pro passo de escrita. A checagem fecha com `gatilhos fora da lista fechada: 0` |
| Agenda do dono usada | datas, turmas, vagas e eventos que o dono declarou aparecem no plano de 48 horas, 7 dias e 30 dias, com a instrução de retirar a urgência depois da data. **Checagem contada:** `datas e eventos que o dono deu: N · citados no plano: N`. Auditoria entregue às vésperas de um evento do dono que não trata do evento deixa de fora a decisão mais urgente dele |
| Data da auditoria | o `audited_at` do `audit-score.json` é a data de hoje, medida no ambiente (`date +%F` quando houver shell), nunca uma data lembrada |
| Cuidado clínico na prescrição | série editorial e pauta sobre saúde, corpo, dor ou dinheiro saem marcadas com a ressalva do nicho ("sem diagnóstico", "avaliação individual", o conselho profissional quando o dono declarou o registro), e caso de aluno sai com "autorizado" e "números confirmados" ao lado |
| Identidade | nenhum nome, logo, cor ou assinatura de terceiro aparece como identidade do relatório |
| Anti-IA | a copy pública do relatório passou no crivo, exit 0 quando houver lint no ambiente |
| Publicação | nada foi publicado sem autorização explícita do dono |

O veredito é o pior item da tabela.

### Como a prova visual é feita (nomes fixos, e o caminho quando não há navegador)

A prova visual mora em 2 arquivos de nome fixo, na mesma pasta de trabalho do relatório:

- `prova-desktop.png`, o HTML renderizado em largura de 1440 pixels.
- `prova-mobile.png`, o mesmo HTML em largura de 390 pixels.

**Com navegador no ambiente**, gere os dois em modo sem janela. Qualquer navegador baseado em Chromium serve, e a chamada tem esta forma:

```
<navegador> --headless --screenshot=prova-desktop.png --window-size=1440,2400 --hide-scrollbars relatorio-<perfil>.html
<navegador> --headless --screenshot=prova-mobile.png  --window-size=390,2400  --hide-scrollbars relatorio-<perfil>.html
```

Depois abra as 2 imagens e confira, item a item: corte de texto, sobreposição de bloco, contraste, legibilidade em tela pequena, imagem quebrada. Escreva o resultado no relatório nesta forma: `Prova visual: prova-desktop.png e prova-mobile.png conferidas. Problemas encontrados: N (lista).`

**Sem navegador no ambiente**, é proibido afirmar que conferiu, descrever o que "aparece" na tela ou inventar o nome de um arquivo de prova. O caminho é declarar, com esta frase literal no relatório e na mensagem ao dono:

> `Prova visual: não gerada, não havia navegador no ambiente. Abra o relatorio-<perfil>.html no computador e no celular antes de mandar pro cliente.`

Prova declarada sem os 2 arquivos no disco e sem essa frase reprova o gate.

## O agente empacotado nesta skill

`agents/openai.yaml` traz a interface pronta desta auditoria pra quando ela é publicada como agente de conversa: o nome que aparece pro usuário, a descrição de uma linha e o prompt de abertura ("audite este Instagram, separe evidência de hipótese e entregue correções prontas em ordem de prioridade"). Ele não muda nada do fluxo acima, é a mesma auditoria com uma porta de entrada diferente. Mexeu no fluxo desta skill, confira se o prompt de abertura continua verdadeiro.

## O que esta skill NÃO faz

Se a skill de destino não estiver instalada, esta faz o mínimo aqui, do jeito escrito na etapa correspondente.

- Criticar UMA peça isolada, uma headline, um carrossel: **soft-critico-copy**.
- Escrever o conteúdo em si (carrossel, reel, stories): **soft-conteudo-carrossel**, **soft-conteudo-reels**, **soft-conteudo-stories**. Aqui saem as SÉRIES editoriais e o texto de bio, destaque e CTA, nunca a peça inteira.
- Reconstruir posicionamento, público, categoria ou oferta do zero: **soft-plano-posicionamento**.
- Arte, identidade visual, template de post: **soft-designer**.
- Subir anúncio ou impulsionar o que a auditoria apontou: **soft-trafego-meta**.

## Arquivos desta skill
- `references/regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.

`references/EXEMPLO-FIM-A-FIM.md` · `references/rubrica.md` · `references/formato-de-entrega.md` · `references/coleta-visual.md` · `references/arquitetura-narrativa.md` · `references/sistema-visual.md` · `references/benchmark-metodologico.md` · `assets/report-template.html` · `assets/report.css` · `scripts/coletar_instagram.cjs` · `scripts/calcular_pontuacao.py` · `scripts/gerenciar_estado.py` · `scripts/montar_relatorio.py` · `scripts/test_calculadora.py` · `scripts/test_estado.py` · `scripts/test_relatorio.py` · `agents/openai.yaml`

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
