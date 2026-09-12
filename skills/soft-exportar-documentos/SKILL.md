---
name: soft-exportar-documentos
description: >-
  Converte um conteúdo que já existe (markdown, HTML, tabela, texto colado) em arquivo de escritório pronto pra enviar: Word .docx, PowerPoint .pptx, planilha .xlsx ou .csv, e PDF. Também lê, edita e confere arquivo desses formatos que o dono mandou. Use quando o pedido for: "exporta em Word", "transforma esse md em docx", "me manda em PDF", "gera a planilha disso", "joga essa tabela num xlsx", "converte esse arquivo", "abre esse docx e me diz o que tem dentro", "preenche esse formulário em PDF", "junta esses PDFs", "esse arquivo abriu quebrado". NÃO use pra: criar o deck de apresentação desenhado do zero em HTML (soft-apresentacao, que exporta o próprio deck); publicar como Google Doc nativo com link (soft-google-docs); escrever o conteúdo, que é da skill do formato pedido; a apostila navegável de uma gravação (soft-apostila); arte, banner ou PNG de peça (soft-designer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Exportar documentos: o conteúdo pronto vira arquivo que o cliente abre

O texto já está escrito. Falta ele chegar na mão de alguém no formato que essa pessoa consegue abrir, imprimir, assinar ou editar. Esta skill faz essa passagem nos 4 formatos de escritório (Word, PowerPoint, planilha, PDF), nas duas direções: gera o arquivo a partir do conteúdo, e lê o arquivo que chegou pra devolver o conteúdo.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --fonte <o .md de origem> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. **O `--fonte` é obrigatório aqui e resolve a contradição que travava esta skill:** sem ele, o script reprova pelo marcador herdado que a lei desta skill proíbe consertar, e a única saída correta da conversão vira exit 1. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Os arquivos que cada ação exige (`--exige`).** Conferência: `--conferir <pasta> --exige <lista>`. DOCX: `--exige *.docx`; PDF: `--exige *.pdf`; deck: `--exige *.pptx`; planilha: `--exige *.xlsx`. Arquivo ausente sai com exit 1.

**O HTML se confere no corpo montado, nunca no arquivo.** Rode o grep de marcador e de frase de bastidor (`entra aqui|preencher|antes de publicar|placeholder|a definir|pendente`) sobre o **texto que o HTML renderiza**: página que monta o corpo por script esconde o marcador da varredura estática, e a peça pública não carrega bastidor renderizado. Cole `marcadores no corpo renderizado: 0 · frases de bastidor renderizadas: 0`.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**A lei-mãe:** a skill não inventa conteúdo. Ela transporta. Se o conteúdo tem furo, o furo atravessa a conversão e vira `[A CONFIRMAR: o quê]` dentro do arquivo, visível na página, nunca uma frase inventada pra tapar o buraco.

**Furo aberto por outra etapa atravessa esta skill intacto**, mesmo que o dado exista em outro lugar do perfil do dono, e mesmo que você tenha certeza de qual é. Quem resolve o furo é quem pediu aquela etapa: fechar aqui um `[A CONFIRMAR]` que veio de fora ultrapassa o escopo de uma conversão e esconde do dono que a etapa anterior ficou pela metade. Checagem verificável antes de fechar: **conte os marcadores do arquivo-fonte e os do arquivo exportado e cole os dois números** na forma `marcadores na fonte: N · no exportado: N`; se diferirem, a exportação reprova e volta pro transporte fiel.

**Defeito que veio da FONTE não conta como reprovação da conversão.** Marcador, nome sem autorização e título fora da régua que já existiam no `.md` de origem são achados SOBRE A FONTE, e vão pro handoff na forma `achado na fonte: <o quê> · <arquivo:linha> · pergunta ao dono: <literal>`. Nunca entram nas contagens desta skill, e nunca são consertados aqui. **As contagens desta skill medem o que a CONVERSÃO introduziu, e saem zeradas:** `marcadores introduzidos: 0 · travessões introduzidos: 0 · linhas alteradas: 0`, com o `diff` colado. Contar o marcador da fonte como falha da conversão faz o relato culpar a etapa errada e esconde o furo real de quem tinha que fechá-lo. **E quem separa os dois é o script, com `--fonte <o .md de origem>`:** marcador, nome de terceiro e número que já existem literalmente na fonte saem impressos como `achado na fonte: <o quê> · <arquivo:linha>` e não contam pro exit; só o que a conversão introduziu reprova. Cole a linha `herdados da fonte (fora do exit): N · introduzidos por esta conversão: 0` junto do `exit=0`. Rode o `--conferir` sempre, inclusive quando reprovar, e cole a última linha e o exit.

```bash
grep -c 'A CONFIRMAR' <arquivo-fonte.md>
grep -c 'A CONFIRMAR' <arquivo exportado ou o .md que virou o exportado>
```

**A segunda lei: entrega sempre sai.** Biblioteca que falta não cancela o trabalho. Sem a biblioteca do formato pedido, a entrega é o `.md` completo mais uma linha dizendo o que faltou instalar e o comando exato de conversão pra quando existir. Ninguém fica sem nada.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as 4 ações num caso fictício de nicho neutro (uma empresa de manutenção predial que precisa mandar proposta, apresentação, planilha de custos e o PDF assinável): o que o dono deu de entrada, as perguntas que a skill fez, e a saída resumida de cada formato.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md`. Aqui, por ser uma skill de conversão de arquivo, valem sempre a parte 1 (pergunta o modo) e a parte 4 (oferece refinar); as outras duas entram só quando o formato de saída pede uma decisão de estrutura.

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o conteúdo e diz o formato e eu gero o arquivo). Se quiser ser guiado passo a passo (te pergunto o formato de saída e as opções, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra geração com o conteúdo e o formato que o dono colou. Se faltar o insumo que o arquivo não vive sem (o formato de saída, ou o conteúdo-fonte), pergunta AQUELE insumo e segue.
- **Modo guiado**: só quando o dono pede explicitamente. Pergunta o formato de destino e as opções (capa, sumário, orientação) uma de cada vez, e gera o arquivo com o que o dono for dando.

**Oferece refinar no fim (parte 4):** depois de gerar o arquivo, fecha com UMA linha: "Quer outra orientação, capa, ou o mesmo conteúdo em outro formato? Me diz que eu regero." A oferta de refino não substitui o gate de qualidade nem o "mostra e para".


## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "exporta em Word", "manda em .docx", "vira documento", "faz o relatório em Word", "preciso mandar pra assinatura em Word" | **1 · WORD** |
| "faz o PowerPoint", "exporta em .pptx", "quero editar os slides no PowerPoint", "abre esse pptx e tira o texto" | **2 · POWERPOINT** |
| "joga isso numa planilha", "exporta em .xlsx", "monta a planilha de custos", "quero as fórmulas vivas", "me manda em csv" | **3 · PLANILHA** |
| "manda em PDF", "junta esses PDFs", "separa as páginas", "preenche esse formulário", "tira o texto desse PDF", "põe marca d'água" | **4 · PDF** |
| "converte esse arquivo", "abre esse arquivo e me diz o que tem", "esse arquivo abriu quebrado" | **5 · LER E CONFERIR** |
| "manda em Word e em PDF", "os dois formatos" | **a ação do formato-fonte, depois a 4** |

Pedido ambíguo ("me manda esse documento", "exporta isso aí"): pergunte UMA coisa só, **"quem vai abrir esse arquivo, e pra quê?"**, e decida pela resposta. Quem vai editar quer Word ou planilha; quem vai só ler, assinar ou imprimir quer PDF; quem vai apresentar quer PowerPoint. Mostre a tabela acima como cardápio se a resposta não resolver.

## Como ler cada ação

Toda ação abaixo traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**Antes da primeira conversão, meça a máquina.** Rode `python3 scripts/checar_dependencias.py` (a partir da pasta desta skill). Ele imprime, por formato, qual rota existe aqui e qual não existe, e escreve a frase que você devolve ao dono quando nenhuma rota do formato existe. Sem shell, siga a tabela de dependências no fim deste arquivo e teste importando a biblioteca antes de escrever o gerador inteiro.

**A identidade visual vem do perfil do dono.** Cor, fonte e logo: leia do perfil/brain do agente quando existir; se não existir, use o padrão sóbrio (fonte Arial ou Calibri, preto no branco, sem cor de acento) e diga em 1 linha que assumiu isso. Nunca invente uma paleta e apresente como se fosse a marca dele.

---

## Ação 1 · WORD (.docx)

**O que faz:** transforma o conteúdo num arquivo Word com títulos reais, tabela nativa, lista e sumário, ou edita um .docx que já existe sem estragar o resto.

**Precisa de:** o conteúdo pronto, em markdown, HTML ou texto colado, do pedido do dono ou da etapa anterior de outra skill · a decisão entre criar do zero ou editar um arquivo existente · o tamanho da página (A4 ou carta) e a identidade visual.

**Sem o insumo:** conteúdo faltando, peça o arquivo ou o texto numa pergunta só e não escreva antes da resposta. Tamanho de página faltando, use A4, o padrão do Brasil, e diga numa linha. Identidade faltando, use o padrão sóbrio da regra acima.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** o `.docx` no disco, com nome em slug curto, mais o `.md` de origem preservado ao lado. **STOP** antes de considerar entregue: mostre o arquivo renderizado ou o resumo do que entrou.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

**Leia primeiro:** `references/docx-como-fazer.md` (as rotas, as armadilhas de cada uma e o passo a passo de edição).

**Profundidade:** `references/conferir-e-validar.md` (a conferência que pega o erro antes do dono) · `scripts/docx/merge_runs.py`, `scripts/docx/comment.py`, `scripts/docx/accept_changes.py` (os utilitários de edição fina).

**Os passos:**
1. Meça a máquina (`scripts/checar_dependencias.py --formato docx`) e escolha a rota pela ordem de preferência que ele imprime.
2. Criando do zero: escreva o gerador, um bloco de conteúdo por vez, títulos com o estilo nativo de título (é o que faz o sumário existir), tabela com largura declarada nas duas pontas.
3. Editando um arquivo que chegou: descompacte, rode `scripts/docx/merge_runs.py` antes de procurar qualquer frase (o Word quebra o texto em pedaços e a frase que você lê não existe inteira no XML), edite, recompacte, valide.
4. Confira (Ação 5) antes de dizer que está pronto.
5. **STOP.** Mostre o arquivo e pergunte "te serve? ajusto, ou sigo?".

---

## Ação 2 · POWERPOINT (.pptx)

**O que faz:** monta o arquivo .pptx a partir de um roteiro de slides já escrito, ou preenche um template que o dono mandou, ou lê um deck existente e devolve o conteúdo.

**Precisa de:** o roteiro slide a slide, com título e conteúdo de cada tela, do dono ou da etapa anterior · o template, quando existir · a proporção (16:9 é o padrão) e a identidade visual.

**Sem o insumo:** sem roteiro, esta skill NÃO escreve o deck: pergunte se o conteúdo já existe em algum lugar e, se não existir, diga em 1 linha que quem escreve o arco e a tela de cada slide é a skill de apresentação, e ofereça converter assim que o roteiro chegar. Sem template, gere do zero no padrão sóbrio. Sem proporção declarada, use 16:9.

**Entrega:** o `.pptx` no disco, mais o mosaico de miniaturas pra conferência quando as ferramentas de apoio existirem. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

**Leia primeiro:** `references/pptx-como-fazer.md` (rotas, as armadilhas que corrompem o arquivo, e o trabalho com template).

**Profundidade:** `references/conferir-e-validar.md` · `scripts/pptx/thumbnail.py` (o mosaico que mostra os slides do template) · `scripts/pptx/add_slide.py` (duplica slide com toda a papelada) · `scripts/pptx/clean.py` (limpa slide, mídia e vínculo órfão depois de apagar).

**Os passos:**
1. Meça a máquina e escolha a rota.
2. Com template: gere o mosaico primeiro, escolha o layout de cada seção, varie os layouts. Faça todo o trabalho de estrutura (somar, apagar, reordenar slide) ANTES de editar conteúdo de qualquer slide.
3. Sem template: monte do zero, uma ideia por slide, título grande e corpo pequeno, cada slide com um elemento visual.
4. Confira (Ação 5): valide o arquivo, leia o texto de volta e olhe as imagens dos slides procurando texto que estourou a caixa, que é o defeito mais comum.
5. **STOP.**

---

## Ação 3 · PLANILHA (.xlsx e .csv)

**O que faz:** transforma tabela, lista de números ou dado colado numa planilha com fórmula viva e formato de célula, ou lê e conserta uma planilha que chegou bagunçada.

**Precisa de:** os dados (tabela em markdown, csv, texto colado, ou a descrição do cálculo) · o que cada coluna significa e qual é a unidade · quais números são premissa que o dono muda depois, e quais são resultado de conta.

**Sem o insumo:** sem saber o que é premissa e o que é conta, pergunte UMA coisa: **"quais desses números você vai querer mudar depois pra ver o resultado mudar?"**. Esses viram célula de entrada, destacada, e todo o resto vira fórmula que aponta pra elas. Sem unidade declarada, escreva a unidade no cabeçalho da coluna e marque `[A CONFIRMAR: unidade]`.

**Entrega:** o `.xlsx` com as fórmulas recalculadas, ou o `.csv` quando a rota da planilha não existir na máquina. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

**Leia primeiro:** `references/xlsx-como-fazer.md` (a regra da fórmula viva, o recálculo obrigatório e quais funções sobrevivem).

**Profundidade:** `references/conferir-e-validar.md` · `scripts/xlsx/recalc.py` (o recálculo que prova que nenhuma fórmula quebrou).

**Os passos:**
1. Meça a máquina e escolha a rota.
2. Separe o que é entrada do que é conta. Toda premissa mora na própria célula, rotulada, e as fórmulas apontam pra ela; número solto dentro de fórmula é erro.
3. Escreva fórmula, nunca o resultado calculado por fora. A planilha tem que recalcular quando o dono mexe numa premissa.
4. Recalcule com `scripts/xlsx/recalc.py` e conserte cada erro que ele nomear. Recálculo limpo prova que as fórmulas rodam, não que estão certas: confira 2 ou 3 à mão contra o número que você esperava.
5. Documente toda premissa e todo número fixo onde o leitor vê, ao lado da célula ou no rodapé da tabela.
6. **STOP.**

---

## Ação 4 · PDF (gerar, juntar, separar, preencher, extrair)

**O que faz:** gera o PDF a partir de qualquer um dos formatos acima ou do markdown, e faz o trabalho de manipulação: juntar, separar, girar, marca d'água, senha, extrair texto e tabela, preencher formulário.

**Precisa de:** o arquivo-fonte ou o conteúdo · o que exatamente fazer com ele (gerar, juntar, separar, preencher, extrair) · nos formulários, o valor de cada campo.

**Sem o insumo:** sem saber se o PDF é pra ler, imprimir ou assinar, assuma leitura em tela, gere a partir do formato-fonte e diga a premissa em 1 linha. Num formulário com campo que o dono não preencheu, deixe o campo vazio e liste os campos vazios na entrega; nunca preencha por conta própria.

**Entrega:** o `.pdf` no disco, mais a lista do que foi feito (páginas juntadas, campos preenchidos, campos que ficaram vazios). **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

**Leia primeiro:** `references/pdf-como-fazer.md` (as rotas de geração e a receita de cada manipulação).

**Profundidade:** `references/conferir-e-validar.md` · `scripts/pdf/` (os utilitários de formulário: descobrir os campos, preencher os que são de verdade preenchíveis, e desenhar por cima quando não são).

**Os passos:**
1. Meça a máquina e escolha a rota.
2. Gerando: prefira converter a partir do formato-fonte já pronto (Word ou deck), porque a conversão preserva o desenho; montar o PDF do zero só quando não houver fonte.
3. Manipulando: identifique primeiro o que o arquivo é (com campo de formulário de verdade, ou uma imagem escaneada sem texto nenhum), porque a rota muda completamente.
4. Confira (Ação 5): abra o PDF gerado e leia o texto de volta; num formulário, confira campo a campo contra o valor que o dono deu.
5. **STOP.**

---

## Ação 5 · LER E CONFERIR (o arquivo que chegou, e o que você gerou)

**O que faz:** abre um arquivo de escritório e devolve o conteúdo em texto, e roda a conferência obrigatória sobre todo arquivo que a skill gerou.

**Precisa de:** o arquivo · o que o dono quer dele (o texto todo, uma tabela específica, ou o diagnóstico de por que abriu quebrado).

**Sem o insumo:** sem saber o que ele quer, devolva o sumário do que tem dentro (quantas páginas ou slides ou abas, os títulos) e pergunte o que interessa. Não despeje o arquivo inteiro na conversa.

**Entrega:** o conteúdo em `.md` no disco quando é longo, ou direto na resposta quando cabe em poucas linhas.

**Leia primeiro:** `references/conferir-e-validar.md` (as 3 camadas de conferência e o que cada uma pega).

**Profundidade:** `scripts/office/validate.py` (a validação de estrutura de Word e deck) · a reference do formato que chegou (`docx-`, `pptx-`, `xlsx-` ou `pdf-como-fazer.md`), na seção de leitura.

**As 3 camadas, nesta ordem:**
1. **Conteúdo:** leia o arquivo de volta pra texto e confira contra o que devia estar lá. Pega conteúdo faltando, ordem errada, e o pior de todos, o texto de exemplo do template que ficou pra trás.
2. **Arquivo:** valide a estrutura interna quando a ferramenta existir. Pega o arquivo que abre quebrado antes do dono descobrir.
3. **Visual:** renderize e olhe. Pega o que só o olho pega: texto estourando a caixa, elemento sobreposto, margem errada. Obrigatório em deck e em qualquer coisa que vai impressa.

---

## Gate de qualidade (antes de dizer que está pronto)

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Inventário do que o dono deu, com piso contado (vale em toda entrega desta skill).** Todo dado do perfil do dono que cabe na entrega aparece nela ou sai com o motivo da exclusão declarado, um dado por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`. **O piso é CONTADO, não estimado:** conte os dados do perfil um a um (com shell, `grep -c '^-' <perfil>`) e desdobre os campos de valor múltiplo. Cole a conta na entrega: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo.**

O veredito é o PIOR item: um ✗ refaz a peça, não o trabalho inteiro.

**Os 6 checks do formato:**
1. **Abre.** O arquivo foi aberto de volta depois de gerado, nem que seja lendo o texto. Arquivo nunca reaberto não se entrega.
2. **Conteúdo completo.** Tudo que estava no `.md` de origem está no arquivo final, na mesma ordem. Nada de tabela que virou parágrafo nem lista que virou texto corrido.
3. **Sem sobra de template.** Nenhum texto de exemplo, nenhum "inserir aqui", nenhum campo de preenchimento esquecido. Busque por esses termos antes de entregar.
4. **Furo visível.** Todo dado que faltou está marcado `[A CONFIRMAR: o quê]` dentro do arquivo, na página, não numa nota de rodapé que ninguém lê.
5. **Marcador contado dos dois lados.** Os dois números estão colados, na forma `marcadores na fonte: N · no exportado: N`, e são iguais. Furo fechado por aqui, com dado achado em outro lugar do perfil, reprova a exportação: o transporte é fiel, e quem fecha o furo é quem pediu a etapa que o abriu.
6. **Nome e destino.** O arquivo tem nome que o dono entende sem abrir, e você disse onde ele está.

**Os 5 checks anti-IA (rode em todo texto que a skill escreveu, inclusive legenda de tabela e nota de rodapé):**
1. **Travessão longo:** zero. Busque o caractere e troque por ponto ou hífen comum.
2. **Verbo-freio banido:** zero ocorrências da família que a régua anti-voz proíbe (o verbo que rima com "cravar" e as flexões dele). Use emperrar, empacar, parar, freio, amarra.
3. **Antítese de espelho:** nada do molde que nega um polo curto pra afirmar o outro, em uma frase ou em duas, com ou sem a preposição "sobre", nem duas negações paralelas empilhadas. Afirme o que é, com sujeito e cena.
4. **Adjetivo sem lastro:** nada de "robusto", "poderoso", "completo" descrevendo o próprio arquivo. Diga o que ele tem: quantas páginas, quais abas, quais fórmulas.
5. **Frase que serviria pra qualquer documento:** cortada. Se a legenda cabe em qualquer planilha do mundo, ela não diz nada; ou nomeia o que aquele número é, ou sai.

**Com shell disponível, rodar `python3 scripts/lint_copy.py <arquivo>` sobre o `.md` de origem é obrigatório**, não opcional: é ele que decide os checks 1 a 3 acima e pega o que o olho perde. Sem shell, faça a busca manual pelos dois bloqueios duros (o travessão longo e o verbo-freio banido).

**O lint roda no TEXTO EXTRAÍDO de cada binário gerado, nunca no `.md` como procuração.** O `.md` limpo não prova nada sobre o `.docx`: a sujeira entra na conversão, e o arquivo que chega na mão do dono é o binário. Antes de declarar pronto, rode sobre cada binário gravado:

```
python3 scripts/lint_binario.py <saída>.docx <saída>.pdf <saída>.pptx
```

Ele extrai o texto por formato (zip interno em `word/document.xml` e `ppt/slides/*.xml` para Word e deck, `pdftotext` para PDF), roda o `lint_copy.py` no que saiu e imprime a linha exigida, `<arquivo> (texto extraído): exit N`, fechando em `binários linteados: N · exit 0: N · exit diferente de 0: 0`. **Cole essas linhas no relatório, ao lado das linhas dos `.md`. Exit diferente de 0 em qualquer binário reprova a entrega, mesmo com o `.md` limpo.** Sem shell, abra o arquivo gerado e faça a busca do travessão longo dentro dele mesmo.

**A contagem de acento entra junto do lint do texto extraído.** Ao lado de `<arquivo> (texto extraído): exit N`, cole `caracteres: N · linhas com acento: N` do binário e a mesma contagem sobre o `.md` de origem (`grep -c '[áéíóúâêôãõç]'`): **zero acento num texto em português com mais de 200 caracteres, com a origem acentuada, reprova o arquivo**, porque exit 0 no lint não vê o português perdido entre o `.md` e o binário, e o `checar_titulos.py --conferir <pasta>` reprova sozinho com `deck sem acentos`.

**E é PROIBIDO redigitar o conteúdo dentro do script gerador.** O texto vai do `.md` para o binário por LEITURA do arquivo (`open(...).read()`, `pandoc`, `markitdown`), nunca por string literal digitada no código: conteúdo redigitado à mão é conteúdo reescrito, e esta skill transporta. A checagem que pega isso na origem, antes de gerar: `python3 -c "import sys;print(open(sys.argv[1],encoding='utf-8').read().count(chr(8212)))" <script gerador>` tem que voltar `0`. Quando o gerador precisa de uma pausa no meio da frase, ela sai por vírgula ou por ponto, do jeito que a régua de escrita manda, nunca por travessão.

---

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Criar a apresentação desenhada do zero (arco, tela de cada slide, deck em HTML) | **soft-apresentacao** | monto o .pptx simples a partir de um roteiro que o dono me der, sem projeto visual |
| Publicar como Google Doc nativo, com link de abrir | **soft-google-docs** | entrego o .docx e digo que subir pro Drive é manual |
| Escrever o CONTEÚDO (a copy, o roteiro, o relatório) | a skill do formato pedido | converto o que existir; não escrevo o texto |
| A apostila navegável de uma aula gravada | **soft-apostila** | converto o material que já estiver escrito |
| Arte, banner, PNG de peça, identidade visual | **soft-designer** | uso o padrão sóbrio e digo que assumi isso |
| Planilha como sistema de gestão financeira, com método | **soft-financeiro** | monto a planilha que o dono descrever, sem o método por trás |

## Dependências (o que precisa existir na máquina, e o que fazer sem)

`python3` é a única exigência absoluta. Todo o resto é rota: o que existe, decide como a skill trabalha; o que falta, vira uma linha honesta pro dono. **Rode `python3 scripts/checar_dependencias.py` e siga o que ele imprimir**, em vez de decorar esta tabela.

| Formato | Rota preferida | Rotas alternativas | Sem nenhuma delas |
|---|---|---|---|
| Word | biblioteca `docx` de Node | `python-docx`, depois `pandoc`, depois editar o XML na mão | entrego o `.md` e digo: falta `python-docx` ou `pandoc` pra gerar o Word |
| PowerPoint | `pptxgenjs` de Node | `python-pptx`, depois editar o XML de um template | entrego o `.md` do roteiro e digo: falta `python-pptx` pra gerar o deck |
| Planilha | `openpyxl` | `pandas` pra despejo de dado sem fórmula | entrego `.csv`, que sempre sai, e aviso que fórmula e formatação ficaram de fora |
| PDF | LibreOffice (`soffice`) convertendo o formato-fonte | `reportlab` pra montar do zero, `pypdf` ou `qpdf` pra manipular | entrego o `.md` ou o `.docx` e digo qual comando roda a conversão quando a ferramenta existir |

**Ferramentas de apoio** (conferência, não geração): `soffice` renderiza pra conferir e converte entre formatos · `pdftoppm` vira PDF em imagem por página · `pdftotext` e `pandoc` puxam texto de volta · `markitdown` lê deck e planilha · `lxml` e `defusedxml` validam o XML interno · `PIL` monta o mosaico de miniaturas.

**Regra de instalação:** não rode instalador por conta própria. Se uma biblioteca resolveria o pedido, diga ao dono qual é e o comando exato, e espere o OK. Ambiente de cliente costuma ter restrição de rede, e instalação silenciosa que falha no meio deixa a máquina pior do que estava.

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/conferir-e-validar.md` (a conferência das 3 camadas, vale nas 4 ações) · `scripts/checar_dependencias.py` (mede a máquina antes de converter) · `scripts/office/validate.py` (valida a estrutura interna de Word e deck) · `scripts/lint_copy.py` (o anti-IA em código, rode no shell quando o ambiente permitir) · `scripts/lint_binario.py` (o mesmo anti-IA sobre o texto extraído do `.docx`, `.pptx` e `.pdf` gerados).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do assunto, minúsculas, hífens, sem acento, até 6 palavras, com a extensão do formato (ex.: `proposta-manutencao-predial.docx`). O `.md` de origem fica ao lado com o mesmo nome-base.
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo.md>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`. **Binário gerado entra nessa lista pelo texto extraído**, com `python3 scripts/lint_binario.py <arquivo>`, e a linha dele é `<arquivo> (texto extraído): exit N`: o `.docx` e o `.pdf` são os arquivos que o dono abre, e o lint só vale quando lê o que eles carregam de verdade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
