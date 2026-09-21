---
name: soft-tweet-card
description: >-
  Renderiza um carrossel vertical 1080x1350 no formato print de tweet: cabeçalho com avatar, nome, selo e handle, corpo em fonte de tweet, uma palavra-chave em verde por card, e o arco de 5 a 8 frames. Entrega os PNGs numerados, o mosaico de conferência e o veredito do verificador. Também revisa carrossel já feito neste formato. Use quando o pedido for: "faz um card estilo tweet", "print de tweet", "carrossel no formato de tweet", "posta como se fosse um tweet meu", "aquele carrossel que parece print da timeline", "revisa esses cards de tweet", "gera as versões clara e escura". NÃO use pra: escrever a copy do carrossel (soft-conteudo-carrossel); a headline isolada (soft-conteudo-headlines); carrossel comum, banner ou capa (soft-designer); levar a peça pronta pra outra plataforma (soft-conteudo-multiplataforma); o lote de criativos (soft-criativo-campeao); deck em PPTX (soft-apresentacao); reel ou vídeo (soft-reel-7seg, soft-editor-video). Leia e siga o fluxo inteiro do SKILL.md.
---

# Cards no formato print de tweet

Esta skill veste uma copy já escrita no formato que imita um print de timeline: cabeçalho de perfil real, texto tranquilo, uma palavra em verde, sem numeração de card. A receita é fechada; nada aqui é sugestão, e a skill não inventa outro sistema visual por cima.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**O render NUNCA aplica caixa alta na headline.** `text-transform: uppercase` não entra em manchete, capa, título de slide, título de card nem em qualquer texto grande que o leitor lê como a frase da peça: ênfase é por palavra, não por tecla, e a caixa alta engorda a linha, come a área segura e derruba a leitura no celular. **O versalete (small caps) e a caixa alta continuam liberados em três lugares e só neles:** tag ou etiqueta (`.slide-label`, `.tag`), rótulo de rodapé, e cabeçalho pequeno de topo, todos até 16px. Antes de exportar, confira que nenhuma regra de caixa alta alcança a classe da manchete, e cole `regras de caixa alta no render: N · alcançando a manchete: 0`. O `checar_titulos.py --render <arquivo.html>` e o `--conferir` leem os títulos do HTML e do deck e reprovam com `título em caixa alta: <linha>`.

**Quando o pedido nomeia um evento, uma turma ou uma data, ao menos uma peça do lote carrega a razão de agir agora, escrita.** Rode `grep -niE 'turma|vagas|come[çc]a|aula ao vivo|[0-9]{2}/[0-9]{2}' <perfil>` e cole a saída. O que voltar entra em pelo menos uma peça, no gancho ou no sub, com o número literal (a data de início, a quantidade de vagas, a data da aula). Cole `peças no lote: N · com razão de agir agora: N`, e zero na segunda coluna, num pedido que nomeia turma ou evento, reprova o lote: peça atemporal responde a um pedido que não foi feito.

**O motivo da troca de capa nomeia o gatilho ganho, nunca a medida do texto.** Cole `motivo da troca: <gatilho ganho> · <o que a capa antiga não fazia>`. Contagem de caractere, "ficou mais curta" e preferência de leitura não são motivo aceito: a capa é a peça de maior custo de erro do carrossel, e trocá-la por medida de comprimento é trocá-la por acaso.

**O `titulos.txt` nasce do arquivo de copy, por comando, e vazio reprova.** Um arquivo só, `conferencia/titulos.txt`, uma linha por CARD de copy mais o H1 (10 cards + 1 = 11 numa peça de 10), extraída da copy fonte (o `.md` da copy, ou o bloco de texto do HTML de cada card). **Não existe `titulos-cards.txt` paralelo:** o universo é de copy, e a copy não dobra com o tema. **Quando a peça sai em 2 temas (claro/escuro), o universo é resolvido pela copy fonte e conta UM título por card, nunca um por PNG:** o mesmo `slide-03.png` em `claro/` e em `escuro/` é a mesma copy, e o `--conferir` já colapsa os temas e cobra `titulos.txt` com uma linha por card, não pelo dobro de PNG. `titulos.txt` vazio reprova antes da análise de arte: uma entrega saiu com 0 bytes para 10 cards em dois temas e oito telas foram publicadas sem gate. Quando a peça mora em subpasta (`<slug>/_fonte/*.html`), aponte o gate pros arquivos dela com `--peca`, nunca reduza o universo ao topo da pasta.

**Capacidade negada no perfil é fato, nunca lacuna a interpretar.** Antes de escolher a mecânica do CTA, rode `grep -in 'automação\|automacao\|robô\|bot' <perfil do dono>` e cole a saída literal. Linha que diz `nenhuma automação` responde `não`, e ela não é omissão nem falso positivo a contornar. Cole `mecânica exige automação? sim/não · perfil declara: <a linha literal> · mecânica adaptada: <qual>`. Negação no perfil sai como CTA sem robô, e manter a mecânica por leitura funcional, herança de outra plataforma ou hábito presumido reprova a peça.

**O universo da R3 é o das unidades produzidas, nunca o dos pilares.** As `teses distintas` saem das pautas, headlines ou frames que a peça entrega, e a contagem igual ao número de pilares do dono é resultado inválido. Cole `unidades no lote: N · linhas em teses.txt: N`, os dois iguais, e só então a matriz de pares.

**`teses.txt` é arquivo obrigatório da pasta de saída**, uma tese de até 4 palavras por linha, ao lado do `conferencia/checagem-titulos.md`. Sem ele o gate não calcula a R3 e o campo do fecho sai com a instrução do script no lugar do número, o que reprova a entrega.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício de nicho neutro do início ao fim: o onboarding, a copy que o dono deu, a escolha dos tipos de frame card a card, o manifesto de entrada colado no formato que o script lê, o mosaico conferido com o que foi visto, o STOP de aprovação e a lista final de arquivos.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Como aqui o trabalho é vestir uma copy já escrita no render, valem duas delas:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a copy e o perfil e eu renderizo os cards). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pro render com o que o dono colou. Se faltar um insumo que os cards não vivem sem (a copy, o cabeçalho de perfil), pergunta AQUELE insumo e segue, sem repetir o onboarding inteiro.
- **Modo guiado**: só quando o dono pede explicitamente. Pergunta a copy, o perfil (avatar, nome, selo, handle) e se quer as duas versões, uma coisa de cada vez, e renderiza com o que o dono for dando.

A pergunta do modo é UMA por carrossel.

**Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer a versão clara também? outra palavra em verde? trocar a capa? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "faz o carrossel estilo tweet", "transforma essa copy em print de tweet", "posta como se fosse um tweet meu" | **1 · CARROSSEL NOVO** |
| "revisa esses cards", "olha se esse carrossel de tweet está certo", "por que isso não parece um tweet?" | **2 · REVISÃO** |
| "gera a versão clara também", "quero as duas versões" | **1 ou 2, com o passo das duas versões** |

Pedido ambíguo ("faz um card"): pergunte UMA coisa só, se é pra parecer um print de timeline ou é carrossel visual comum, porque a segunda resposta manda o pedido pra **soft-designer**.

## Como ler cada ação

Toda ação traz o mesmo bloco fixo: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · passos numerados com **STOP**.

## Onboarding, uma vez, antes do primeiro card

O cabeçalho do card imita um perfil real, então ele precisa dos dados do dono. **Leia do perfil/brain do agente quando existir.** Se não existir, pergunte os três de uma vez e guarde num `config.local.md` na pasta de trabalho do dono (o diretório de saída desta rodada, nunca dentro da pasta desta skill, que é código versionado e compartilhado), pra não perguntar de novo. **A checagem tem que RODAR, não só existir.** Depois de gravar, rode os dois comandos abaixo e **cole a saída dos dois no relatório**, uma embaixo da outra:

```bash
realpath <caminho do config.local.md>
realpath <pasta desta skill>
```

O primeiro caminho **não pode começar** pelo segundo. Se começar, mova o arquivo com `mv` pro lugar certo, corrija a linha que você escreveu ao dono e rode a checagem de novo antes de seguir. Sem as duas linhas coladas o gate não fecha, mesmo que você tenha certeza de ter gravado no lugar certo: a proibição já foi violada por quem tinha essa certeza. Os campos são:

| O que | O que é | Vai pra |
|---|---|---|
| Nome de exibição | o nome da PESSOA que assina o perfil, como ela escreve, com acento e tudo | `PERFIL_NOME` |
| Handle | o identificador do perfil, com arroba | `PERFIL_HANDLE` |
| Avatar | caminho do PNG quadrado, que o script recorta em círculo | `PERFIL_AVATAR` |

Os scripts leem os três das variáveis de ambiente de mesmo nome.

**`PERFIL_NOME` é o nome da PESSOA, não o do negócio**, porque o formato imita um print de perfil pessoal e um card assinado por marca denuncia a montagem. Se o perfil do dono traz um campo de quem ele é com nome de pessoa, ele é a resposta e não há pergunta a fazer. Só quando não existir nome de pessoa em lugar nenhum o nome do negócio entra, e aí a linha `nome de exibição: marca (nenhum nome de pessoa no perfil)` vai colada no handoff.

**Sem avatar real:** o script desenha um círculo de placeholder com a inicial do nome, e a peça sai marcada como rascunho. Card publicado sem avatar real reprova. Diga ao dono, em 1 linha, como ele completa a peça depois: **"me manda um PNG quadrado do seu avatar, de pelo menos 400x400, e eu re-renderizo só o cabeçalho: a copy, os frames e o arco ficam iguais, é uma passada de 2 minutos"**. Nunca invente um avatar, nunca use foto de banco de imagem no lugar do rosto dele.

**Pasta de saída:** `SAIDA_DIR` é OBRIGATÓRIA. Os scripts recusam rodar sem ela, com mensagem de erro, e também recusam qualquer caminho que aponte pra dentro da pasta da skill: nada de render caindo na instalação e vazando nome e handle do dono pro próximo que usar a mesma máquina. Pergunte ao dono ou use o diretório de saída do ambiente (`$OUTDIR`, ou a working dir), e **declare em 1 linha onde os arquivos caíram**.

---

## Ação 1 · CARROSSEL NOVO

**O que faz:** veste a copy no formato, renderiza os cards nas duas versões, monta o mosaico e roda o verificador.

**Precisa de:** a copy do carrossel, já escrita, de `soft-conteudo-carrossel` ou do dono · os três dados de perfil, do brain do agente ou do onboarding · a pasta de saída · shell com Python e navegador headless, pra renderizar.

**Sem o insumo:** sem a copy, esta skill não escreve o carrossel do zero: peça a copy ao dono ou mande o pedido pra **soft-conteudo-carrossel** e volte com o texto na mão. Sem shell, veja "O que fazer sem X". Sem avatar, segue como rascunho, com o aviso acima.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Nome de terceiro nunca entra no card, e a pergunta da autorização vem ANTES do render.** Antes de renderizar, rode `grep -in 'autoriz' <perfil>` e cole a saída. Sem uma linha do perfil autorizando aquele nome em peça pública, o card sai com o papel (`uma aluna`, `uma paciente`) e a dúvida vai pro relato antes do render: perguntar num PNG já gerado não desfaz o PNG, e o dono que responde `pode` não repara que já estava lá. Rode também `python3 scripts/checar_titulos.py --render <html do card> --perfil <perfil>`, que reprova nome sem autorização no HTML antes de exportar. Cole `nomes de terceiro na arte: 0 · autorizações citadas no perfil: N`.

**Antes da primeira linha de copy que entra no card, a palavra-chave sai de comando, UMA vez.** Rode `grep -rn -iE 'manda |comenta |envia |digita |palavra ' <pasta de insumos>` e cole a saída inteira no topo do manifesto. A palavra que aparecer nessa saída é a única que pode entrar em CTA nesta entrega, com a grafia exata, e o resultado desse único comando vale pro carrossel inteiro: rodar de novo por card não vale, e escolher palavra fora da saída não vale. Saída vazia proíbe escolher uma, e o CTA sai na versão que dispensa a palavra. Cole, por card com CTA, `CTA com palavra-chave: sim/não · palavra: <literal> · origem: <arquivo:linha>`, e `sim` sem origem reprova antes do render.

**Entrega:** `slide-01.png` a `slide-NN.png` (zero-padding de 2 dígitos) mais `_mosaico.png`, dentro de `$SAIDA_DIR/<slug-do-carrossel>/`, nas versões escura e clara. Quando o último card for o CTA animado, sai também `slide-NN.gif` com o `slide-NN.png` de fallback.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/receita-canonica.md` (INTEIRA, antes de escolher os frames: é lá que moram a base comum, os dois temas com os códigos de cor, **os nove tipos de frame com a função de cada um**, a régua de arco e os critérios de conferência).

**Passos:**

1. Onboarding, se ainda não rodou.
2. Leia `references/receita-canonica.md` por inteiro.
3. Leia a copy fonte **sem reescrever fato, número, CTA nem a ordem dos slides**. A copy é do dono e chega pronta.
4. **Escolha de 5 a 8 tipos de frame** pra formar o arco abrir, tensionar, provar, fechar. A régua de 5 a 8 conta TIPOS distintos, nunca cards: **a quantidade de CARDS é a da copy fonte e não se corta nem se soma**. Repetir um tipo ao longo do carrossel é permitido; usar o mesmo tipo em dois cards seguidos reprova. Os nove tipos e a função de cada um estão na receita canônica: imagem no rodapé, enquete, thread, texto puro, tópicos ou chips, citação, número, print real, conversa.
5. **Declare ao dono a lista de tipo por card antes de renderizar, e declare os dois números na forma `N cards, M tipos`.** É a chance dele corrigir sem custo, e é o mesmo que o critério de conferência vai exigir depois.
6. Monte o manifesto de entrada no formato que o script lê (a seção "O manifesto de entrada" abaixo traz um colado inteiro) e renderize com `scripts/build_tweet_cards.py`. **Nunca desenhe o card livre, fora do script:** é assim que a fonte errada e o nome errado vazam.
**Nenhum card sai com marca d'água de teste na arte.** Antes de renderizar, rode e cole a saída:

```
grep -rniE 'teste|test|placeholder|sample|lorem|sintetico' <manifesto> <pasta de assets>
```

Frame de teste prova o pipeline e **nunca entra na peça entregue**: achado na saída, o frame sai do manifesto e a peça vira PARCIAL, sem render. Sem foto real, o card sai com tratamento de fundo declarado e sem imagem. Cole `cards com texto de teste na arte: 0`.

**O número colado é copiado da saída, não redigitado.** Redirecione a saída do contador pra um arquivo e cole o arquivo: `python3 scripts/verify_tweet_cards.py <pasta> <quantidade> > contagem.txt` (ou o contador que o ambiente tiver), depois `cat contagem.txt` colado inteiro. Número redigitado que não reproduz reprova a contagem, mesmo quando o veredito é o certo.

7. Gere as versões escura e clara. Quando a tarefa pedir só uma, mantenha a outra preparada e declare a limitação.
8. Produza o mosaico e **confira visualmente** (a seção "Conferência do render" abaixo).
9. Rode o verificador: `python3 scripts/verify_tweet_cards.py <pasta> <quantidade>`. Qualquer falha reprova a entrega. **O verificador mede quantidade, dimensão, integridade e verde por card, e não mede a receita:** conte à mão os dois itens que ele não vê e cole as duas linhas no relatório, antes do STOP: `imagens fortes: N de NN cards (mínimo 4)` e `CTA final com imagem de fundo: sim/não`. **Abaixo do mínimo da receita, o carrossel volta pro passo 4** e você troca frames de texto por frames com imagem, sem mexer na copy. A contagem conta arquivo de imagem no disco: **imagem desenhada em CSS (gradiente, silhueta, forma vetorial, ruído SVG) não entra na contagem**, e cada card marcado como imagem forte leva no veredito as DUAS linhas de contagem.

   **A contagem de cores únicas roda no CARD RENDERIZADO, nunca no arquivo de origem.** A foto de origem tem dezenas de milhares de cores e o card pode achatá-las quando a imagem entra como faixa estreita, fundo escurecido ou sob camada de opacidade: o que o dono publica é o PNG final, e é ele que precisa passar dos 20.000. Cada card contado leva a linha `slide-NN | origem: <arquivo> | cores únicas do card renderizado: N (mínimo 20.000) | cores únicas da origem: N`. **Card cuja contagem renderizada fica abaixo do piso não conta como imagem forte, mesmo com foto real embutida**, e a correção é aumentar a área da foto ou reduzir o escurecimento, não trocar o número. O contador de referência, com a saída colada por card: `python3 -c "from PIL import Image; im=Image.open('<card>.png').convert('RGB'); print(len(im.getcolors(maxcolors=10**7)))"`.

   **Quando a contagem fica abaixo do mínimo, há duas saídas, só duas:** (a) gere os 4 frames do arco (capa, meio da tensão, prova, CTA final) com o gerador de imagem disponível no ambiente; (b) sem nenhum gerador disponível, entregue os cards de texto **mais** o arquivo `PEDIDO-DE-IMAGEM-<slug>.md` com as 4 cenas descritas prontas pro dono produzir (enquadramento, luz, o que aparece, o que não aparece) e marque a entrega como PARCIAL no nome do veredito. **Antes de declarar a saída (b), esgote os geradores, um por linha colada.** Teste cada caminho que o ambiente oferece (a ferramenta de geração de imagem do próprio agente, um gerador local na pasta de scripts, qualquer binário de geração no PATH) e cole `gerador: <nome> | testado: sim | resultado: <ok ou o erro literal>` para cada um. **Um único gerador falhando não autoriza a saída (b)**: só a lista completa, com no mínimo 2 caminhos testados e falha em todos, autoriza. Entrega PARCIAL sem essa lista reprova, porque um erro de crédito ou de cota é bloqueio de um caminho e não do ambiente. **Veredito que diz "reprova" e entrega assim mesmo, sem uma das duas saídas, reprova a rodada:** contar o próprio defeito com honestidade é metade do trabalho, e a outra metade é dar ao dono o que fazer com ele.

   **A saída (b) não é o pedido de imagem sozinho: é o pedido MAIS os 4 frames montados com o que existe no disco.** Antes de marcar PARCIAL, varra os insumos do dono por arquivo de imagem (`find <pasta de insumos> -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.mp4' -o -iname '*.mov'`) e cole a saída, inclusive vazia. **Vídeo conta como fonte:** havendo `.mp4` ou `.mov` do dono, extraia os frames com `ffmpeg -i <video> -vf fps=1/4 -frames:v 4 frame-%02d.png` e use nos 4 cards do arco. **Marcar PARCIAL sem a saída do find colada reprova a entrega.** **Vazio nos dois lados (gerador e disco), o card de CTA sai ainda assim com tratamento de fundo declarado** (fotografia ausente, mas superfície não chapada), e o `PEDIDO-DE-IMAGEM-<slug>.md` fecha com o bloco de reentrada pronto: os 4 slots nomeados (`capa`, `meio da tensão`, `prova`, `CTA final`), o caminho onde cada foto deve ser salva, e a linha `assim que as 4 fotos chegarem: aponte cada slot pro arquivo no manifesto do script e rode PERFIL_NOME=<nome> PERFIL_HANDLE=<handle> PERFIL_AVATAR=<avatar.png> SAIDA_DIR=<pasta> python3 scripts/build_tweet_cards.py`, seguida do `python3 scripts/verify_tweet_cards.py <pasta> <quantidade>`. A troca tem que custar um minuto, não uma conversa nova. Entrega PARCIAL sem a varredura do disco colada e sem o comando de reentrada reprova.
9.1. **O resultado do verificador vira arquivo, não fica no relato:** grave `veredito-<slug>.md` na pasta de saída com a tabela de critérios (um por linha, com o veredito), a conferência visual card a card (o que você viu em cada um, não "conferido"), as duas contagens do passo 9 e as pendências que sobraram. É o entregável que a descrição desta skill promete, ao lado dos PNGs e do mosaico; sem ele a entrega está incompleta.
10. **STOP: mostre o mosaico e pergunte "esses são os cards; algum precisa de ajuste antes de você postar?"**. Não dê a peça por pronta por conta própria: o critério de pronto é do dono, não do agente. Ajuste pedido edita só o card mencionado e re-renderiza.

---

## Ação 2 · REVISÃO

**O que faz:** audita um carrossel que já existe neste formato e diz o que reprova e por quê.

**Precisa de:** os cards ou o mosaico · a copy fonte, pra comparar tela por tela.

**Sem o insumo:** sem a copy fonte, você audita só o que é visual (cabeçalho, cor, numeração, arco, órfã) e declara em 1 linha que a fidelidade da copy ficou por conferir.

**Entrega:** uma tabela curta, um critério por linha, com o veredito e o card que falhou; mais os cards corrigidos quando o dono pedir a correção.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/receita-canonica.md`, o bloco "Conferência visual por critério".

**Passos:** compara cada tela com a copy fonte → lista o tipo de frame de cada card e prova que não há repetição consecutiva → roda os checks do gate abaixo → entrega a tabela → **STOP: pergunta se é pra corrigir agora**.

---

## O manifesto de entrada (o que o script espera)

O script monta cada card por uma função de frame. O manifesto é uma entrada no dicionário `CARROSSEIS`, com o slug do carrossel como chave e a lista de cards em ordem. Formato real, colado:

```python
CARROSSEIS["turma-de-natacao-adulto"] = [
    slide_texto("Adulto que não sabe nadar não tem medo de água.\n\nTem medo de ser visto tentando.",
                kw="ser visto", big=True),
    slide_texto("Eu pergunto isso na primeira aula e a resposta é quase sempre a mesma: "
                "'e se eu for o pior da turma?'"),
    slide_texto("Ninguém afunda por não saber nadar. Afunda por tentar não parecer que não sabe."),
    slide_kpi("Na turma de adulto iniciante:", "9 de 10", "nunca tinham colocado o rosto na água. [A CONFIRMAR]"),
    slide_chips("A primeira aula tem três coisas, e nenhuma é nadar.",
                [("Respirar", "boca fora, rosto dentro, sem pressa."),
                 ("Boiar", "o corpo flutua sozinho, você só atrapalha."),
                 ("Soltar", "a mão sai da borda quando você decidir.")],
                "Nadar vem na terceira.", kw="terceira"),
    slide_texto("A turma de adulto é fechada. Ninguém de fora olha, ninguém compara tempo."),
    slide_cta("Comenta NADAR que eu te mando o horário da próxima turma de adulto.", kw="NADAR"),
]
```

As quatro funções de card que o `build_tweet_cards.py` já traz prontas: `slide_texto` (texto puro, com `kw` pra palavra-chave verde e `big=True` pra abertura), `slide_kpi` (número com contexto antes e depois), `slide_chips` (dois ou três pontos organizados) e `slide_cta` (o fechamento). Os outros frames do repertório (thread, citação, enquete, conversa) moram em `scripts/build_frames.py` como `frame_thread`, `frame_quote`, `frame_poll` e `frame_chat`, e recebem o tema como argumento: pra usar um deles no carrossel, importe do módulo de frames e envolva com o mesmo `wrap`. A receita canônica descreve a função de cada tipo.

O `[A CONFIRMAR]` do card de número no exemplo acima é regra, não descuido: número sem lastro na fonte sai marcado, nunca preenchido com um valor plausível.

## Regras inegociáveis do formato

- Avatar real redondo, nome grafado exatamente como o dono escreve (acento faltando reprova), selo azul `#1D9BF0` e o handle.
- **Nunca Bebas Neue.** A fonte é a de tweet (a do sistema, ou Inter), texto tranquilo, peso normal. Peso forte só na palavra-chave verde.
- Selo azul sempre, verde nunca.
- Verde só na palavra-chave. Frase inteira em verde reprova.
- **Não numerar o card.** A regra deste formato manda sobre qualquer identidade genérica que peça indicador de N sobre total.
- Nenhuma palavra sozinha na última linha, e nada de quebra entre o cifrão e o número.
- Seta de arraste pequena, em verde, no canto inferior direito de todos os cards de 1 a N-1, nunca no último.
- Não fabricar depoimento, conversa, print ou fala atribuída. Print só quando é screenshot real catalogado.
- Número só quando validado na fonte.
- Não publicar automaticamente.

## Conferência do render (obrigatória antes do STOP)

**Com leitor de imagem:** abra o `_mosaico.png` e confira, contra o padrão do formato: nove cards verticais em grade, todos com o mesmo cabeçalho no topo (avatar redondo, nome, selo azul, handle), fundo uniforme do tema escolhido, corpo em peso normal com uma única palavra-chave verde por card, nenhum indicador de numeração em canto nenhum, e alternância visível de silhueta entre cards vizinhos, de modo que dois seguidos nunca tenham a mesma forma. Abra em tamanho cheio todo card denso ou suspeito. **Liste ao dono o que você conferiu e o que viu**, em 3 a 6 linhas.

**Sem leitor de imagem:** rode o verificador, que confere quantidade, dimensão e arquivo vazio, e **declare em 1 linha que você não viu os cards**: "não tenho leitor de imagem aqui, o verificador aprovou quantidade, dimensão e integridade dos arquivos; a conferência visual do cabeçalho, do verde e do arco fica com você no mosaico antes de postar".

## O que fazer sem X

| Falta | O que a skill faz |
|---|---|
| **Sem shell** | Não renderiza. Entrega o manifesto de entrada pronto, no formato colado acima, com os tipos de frame já escolhidos e declarados, e diz em 1 linha que basta rodar o script num ambiente com shell. |
| **Sem navegador headless** | O render depende dele. Mesma saída de cima: entrega o manifesto pronto. |
| **Sem avatar real** | Renderiza com o placeholder, marca a peça como rascunho e diz como o dono completa depois (a linha está no onboarding). |
| **Sem `SAIDA_DIR` definida** | O script recusa rodar (a variável é obrigatória, e caminho dentro da pasta da skill também é recusado). Defina a pasta de saída, use o diretório de saída do ambiente, e declare em 1 linha onde os arquivos caíram. |
| **Sem a copy fonte** | Não escreve o carrossel aqui. Pede a copy ou manda pra **soft-conteudo-carrossel**. |

## Gate de qualidade (roda antes do STOP)

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


**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`references/regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com a lista fechada de contagens, uma por linha, exatamente nesta forma:

```
títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N
em molde de antítese (títulos): N (teto 1)
em molde de antítese (fala ou narração que o público ouve): N (teto 1)
com inimigo ou inversão: N de N
teses distintas: N
títulos de serviço: N · de abertura: N · de abertura reescritos: N
rótulos de seção fora da régua: N
gatilhos fora da lista fechada: 0
```

A contagem de molde de antítese sai do lint, nunca da cabeça, e vem acompanhada da coluna sim/não de TODOS os títulos do lote; a de teses distintas vem com a lista ordenada e comparada par a par. Nenhuma das linhas pode faltar, e linha declarada sem o que a régua exige ao lado não conta como feita.

**As contagens de R3, R4 e R5 são gates, não termômetros.** Quando `com inimigo ou inversão` ficar abaixo da metade do lote, `teses distintas` abaixo de 3, ou `em molde de antítese` acima de 1, a entrega **não sai**: os títulos reprovados voltam pro passo de escrita, são reescritos, e a checagem final mostra a contagem corrigida mais a linha `reescritos por contagem: N (<contagem que reprovou>)`. Declarar a contagem que reprova e publicar assim mesmo é o pior dos dois mundos, porque produz um documento que prova o próprio defeito e não o corrige: o dono lê `0 de 4` e não tem como saber que isso significa que a régua reprovou. **Nenhuma justificativa de tipo de peça vale aqui:** se o formato dispensa a inversão, a exceção mora escrita na receita do tipo, e a entrega cita a linha dessa receita. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** **A classificação vale para a FALA, não só para o nome:** anonimizar resolve a identidade e não resolve a origem, e uma frase literal vinda de call ou de caixa de entrada continua sendo conversa privada mesmo sem nome. Liste as falas atribuídas a terceiros na peça, uma por linha, na forma `<fala literal> | origem: <arquivo:linha> | classe: prova declarada ou conversa privada | como aparece na peça: <"uma aluna", "uma seguidora", "alguém que me procurou">`. Fala de conversa privada com pessoa em negociação aberta só entra como "alguém que me procurou" ou equivalente que não afirme compra; "uma aluna", "uma cliente" e "antes de entrar" afirmam a compra e reprovam. Feche com `falas de terceiro na peça: N · de conversa privada apresentadas como aluna: 0`. Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória**, nestes 3 passos: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Palavra-chave de CTA não se inventa, e a grafia é literal.** Antes de escrever qualquer CTA que peça uma palavra ("manda X no Direct", "comenta Y", "envia Z no WhatsApp"), procure a palavra nos insumos do dono (transcrição, peça pronta, mensagem, site) e cole `palavra-chave: <literal> | origem: <arquivo:linha>`. Use a grafia EXATA, sem espaço a mais nem a menos: uma palavra com espaço é outra palavra para quem digita e para a automação que responde, e a lead cai em lugar nenhum. **Sem origem no disco, é PROIBIDO escolher uma:** escreva o CTA na versão que dispensa a palavra ("me chama no Direct e eu te mando") e leve a pergunta ao handoff. Marcar a incerteza no relato e publicar a palavra assim mesmo reprova, porque o dono publica sem perceber.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **O inventário varre o perfil do dono INTEIRO, não só os campos que esta entrega consumiu:** cada campo do perfil é uma linha, e campo com vários valores (paleta com 3 cores; oferta com preço, parcela, bônus e garantia) rende uma linha por valor. **Entrega cujo `Dados fornecidos: N` for menor que o número de campos do perfil recebido reprova sem análise de conteúdo.** Qualificar a linha ("relevantes ao objeto", "considerados para esta entrega") também reprova: o total é o total. **Onde a linha mora:** no arquivo que o dono lê. Quando a entrega é uma peça de copy publicável (headline, carrossel, slide, card, chat, roteiro, deck), a peça NÃO recebe a tabela: a tabela vai num arquivo irmão de handoff (`HANDOFF-<slug>.md`) e só a linha de fechamento fica na peça, no rodapé. Inventário só no relato de processo, sem a linha na entrega nem o handoff no disco, reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.

**Marcador no cabeçalho reprova o render (checagem mecânica, roda antes do STOP).** O cabeçalho imita perfil real, então marcador queimado ali perde o carrossel inteiro. Antes do STOP, rode `grep -i 'A CONFIRMAR' <manifesto de entrada>` e confira campo a campo os três valores de cabeçalho (`PERFIL_NOME`, `PERFIL_HANDLE`, `PERFIL_AVATAR`). Cole a saída do grep no relatório. Marcador em nome, handle ou headline reprova o render e manda refazer o card; nome que falta sai do render inteiro e vira pergunta ao dono, nunca vira string impressa no card.

**O tema claro herda a cor do dono.** O tema claro usa a cor de fundo declarada pelo dono; sem cor declarada, use o off-white padrão da receita canônica. Branco puro só quando o dono pedir branco puro. Prova verificável antes de fechar: cole o hex do pixel do canto superior esquerdo do `slide-01.png` ao lado do hex declarado pelo dono; hex diferente do declarado reprova o render.

| Check | Passa se |
|---|---|
| **Cabeçalho** | avatar redondo, nome com a grafia exata, selo azul e handle em todos os cards |
| **Fonte** | é a fonte de tweet, peso normal; Bebas Neue em qualquer lugar reprova |
| **Verde seletivo** | o verificador contou o verde de acento por card e nenhum card passou de 1. A linha `verde por card: N (máximo 1)` está colada no relatório |
| **Sem numeração** | nenhum indicador de card em canto nenhum |
| **Arco** | de 5 a 8 TIPOS de frame, sem dois iguais em sequência, com a contagem de cards igual à da copy fonte, e os dois números declarados ao dono na forma `N cards, M tipos` antes do render |
| **Cabeçalho sem marcador** | o `grep -i 'A CONFIRMAR'` no manifesto saiu colado no relatório e nenhum campo de cabeçalho carrega marcador |
| **Fundo do tema claro** | o hex do canto superior esquerdo do `slide-01.png` bate com a cor declarada pelo dono, ou com o off-white padrão quando não há cor declarada |
| **Copy fiel** | cada tela bate com o slide correspondente da fonte, sem fato, número, CTA nem ordem alterados |
| **Órfã e cifrão** | nenhuma palavra sozinha na última linha, nenhuma quebra entre o cifrão e o número |
| **Seta de arraste** | presente nos cards de 1 a N-1, ausente no último |
| **Lastro** | todo número, print e fala atribuída tem fonte citada; sem fonte, `[A CONFIRMAR]` |
| **Verificador** | `verify_tweet_cards.py` terminou sem falha (quantidade, dimensão 1080x1350, nenhum arquivo vazio) |
| **Imagem forte, CONTADA e de NATUREZA certa** | a linha `imagens fortes: N de NN cards (mínimo 4)` está colada no relatório e N é 4 ou mais, com as imagens distribuídas no arco (capa, meio da tensão, prova, CTA final), e cada card contado tem a linha `slide-NN \| origem: <arquivo> \| cores únicas do card renderizado: N (mínimo 20.000) \| cores únicas da origem: N`, com a contagem do PNG final e não a do arquivo de origem. **Desenho em CSS não conta como imagem forte.** Carrossel só de tipografia sobre fundo liso reprova a receita, por mais que o verificador aprove: ele mede dimensão e verde, não imagem. Abaixo do mínimo, a entrega só sai por uma das duas saídas do passo 9 (gerar, ou `PEDIDO-DE-IMAGEM-<slug>.md` com entrega marcada PARCIAL) |
| **CTA final com imagem** | a linha `CTA final com imagem de fundo: sim/não` está colada e diz `sim`; o último card é o GIF com imagem forte de fundo mais o PNG de fallback, nunca tipografia sobre fundo chapado |
| **Arquivo de veredito no disco** | `veredito-<slug>.md` existe na pasta de saída, com a tabela de critérios, a conferência card a card e as pendências. Checagem colada no relatório com o caminho absoluto do arquivo; veredito só no relato de processo reprova |
| **Imagem ilustrativa declarada** | quando um card usa foto que não é do dono nem de aluno dele, o veredito registra `imagem ilustrativa, não é prova` naquele card. Num card que imita o print do perfil do dono, foto de banco de imagem pode ser lida como prova, e o dono precisa saber disso antes de postar |
| **Conferência declarada** | o mosaico foi conferido e o dono recebeu a lista, ou o aviso de que os cards não foram vistos |
| **STOP do dono** | o dono viu o mosaico e disse que pode. O critério de pronto é dele |
| **VEREDITO** | é o pior item acima. Uma falha corrige o card e re-renderiza |

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. Se a skill indicada não estiver instalada, faço aqui em modo reduzido e digo em 1 linha o que ficou de fora.

- **Escrever a copy** do carrossel → **soft-conteudo-carrossel**.
- A **headline isolada** ou o gancho → **soft-conteudo-headlines**.
- **Carrossel visual comum**, banner, capa, página → **soft-designer**.
- **Deck de slides** e PPTX → **soft-apresentacao**.
- **Reel** e vídeo → **soft-reel-7seg**, **soft-editor-video**.
- **Publicar** e impulsionar → **soft-trafego-meta**.

## Recursos da pasta

- `references/regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta, leia antes de começar.
- `references/receita-canonica.md`: a receita fechada do formato, com a base comum, os dois temas e seus códigos de cor, **os nove tipos de frame e a função de cada um**, a régua de arco, os critérios de conferência e os ajustes de movimento e imagem.
- `scripts/build_tweet_cards.py`: a implementação de referência do carrossel, e o lugar onde o manifesto de entrada mora.
- `scripts/build_frames.py`: a biblioteca de frames escuros e claros.
- `scripts/verify_tweet_cards.py`: o verificador de quantidade, dimensão e arquivo vazio.
- `shared-references/filtro-anti-ia/`: a mesma régua anti-IA por escrito, pro motor que não tem shell pra rodar o lint. `padroes-banidos.md` lista o que reprova; `falsos-positivos.md` roda antes de reprovar qualquer trecho.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Sem sandbox (a régua escrita, quando o lint não roda).** Motor sem shell não executa `scripts/lint_copy.py`, e isso não dispensa o anti-IA: aplique a régua no olho por `shared-references/filtro-anti-ia/padroes-banidos.md`, padrão por padrão, e passe cada reprovação por `shared-references/filtro-anti-ia/falsos-positivos.md` antes de mandar o trecho de volta pro passo de escrita, porque prosa autoral do dono cai no mesmo crivo e some se ninguém conferir. A entrega sai do mesmo jeito, no melhor que esse motor alcança, e o relato fecha com uma linha dizendo que a conferência anti-IA foi no olho, sem código: `anti-IA: conferido no olho pela régua escrita (sem shell nesta rodada)`. Calar o que ficou de fora reprova a entrega; declarar em uma linha reprova nada.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill, provada por `realpath`.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono. **Item de gate reprovável:** o relatório traz as duas saídas de `realpath` coladas lado a lado (a do `config.local.md` e a da pasta desta skill) e a primeira não começa pela segunda. Sem as duas linhas coladas, o gate reprova, mesmo que o arquivo esteja no lugar certo: declarar não conta, só a saída colada conta.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**

## Passo 2 da checagem (fecho, roda por comando)

Depois de gravar todos os entregáveis, rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída. Ele exige o `conferencia/checagem-titulos.md` na pasta, confere o inventário (os 4 inteiros, o piso e o `inventário duplicado`), o universo dos títulos, o marcador acima de 6 palavras, o nome de conversa privada, a `saída do script reescrita` e o lint de todo `.md`, RELATO incluso. **`exit` diferente de 0 reprova a entrega inteira, antes da análise de conteúdo.**
