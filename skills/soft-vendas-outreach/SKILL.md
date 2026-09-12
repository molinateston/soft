---
name: soft-vendas-outreach
description: >-
  Escreve a PROSPECÇÃO FRIA pra contas que ainda não conhecem o dono: pesquisa cada alvo, acha o motivo real de falar agora, entrega a mensagem por e-mail ou rede profissional, mais a sequência de retomada e a régua de volume. Use quando o pedido for: "escreve um e-mail frio pra [empresa]", "prospecta essa lista de empresas", "mensagem de conexão no LinkedIn", "abordagem pra quem não me conhece", "sequência de follow-up de prospecção", "monta minha lista de prospecção", "quantos e-mails frios posso mandar por dia", "abordagem depois do evento". NÃO use pra: quem já chegou sozinho ou respondeu anúncio (soft-vendas-sdr); preparar a call já marcada (soft-vendas-call-prep); conduzir a conversa quente e fechar (soft-vendas-closer); campanha de e-mail pra base que já é sua (soft-email-sequencia); a régua pós-isca (soft-funil-nutricao); a proposta (soft-vendas-proposta). Leia e siga o fluxo inteiro do SKILL.md.
---

# Prospecção fria: pesquisa primeiro, mensagem depois

Esta skill escreve a abordagem pra quem nunca ouviu falar do dono. A ordem nunca muda: pesquisa a conta, acha o motivo real de falar com ela agora, escolhe o canal, escreve a mensagem, e monta a sequência de retomada mais a régua de volume que protege o remetente. O resultado é sempre um arquivo nomeado, com a mensagem pronta pra copiar e o raciocínio que a sustenta ao lado.

**A skill confere que é ela mesma, antes da primeira linha do fluxo.** As quatro skills de venda são vizinhas e se confundem: uma execução leu a pasta da vizinha, concluiu que esta skill não existia, rodou a outra, e entregou 2 arquivos onde o contrato pede 8, sem `conferencia/checagem-titulos.md`. A PRIMEIRA linha do fluxo é `head -3 SKILL.md` da pasta indicada, e você cola `SKILL.md lido: <caminho literal> · nome no frontmatter: <nome>`. **Nome diferente do que o dono pediu PARA tudo** e reporta que a skill pedida não está no catálogo desta sessão, em vez de rodar a vizinha: contratos de saída diferentes produzem entrega incompleta que parece completa.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Leitura em voz alta, por mensagem, com o resultado colado.** Toda mensagem que o lead recebe passa pela leitura em voz alta antes de sair. Cole `molde N | lida em voz alta: passa/tropeça | onde tropeça: <trecho>` pra cada mensagem da sequência, e feche com `lida em voz alta: sim · frase junta afirmação e pergunta: 0`. Frase que emenda uma afirmação e uma pergunta direta na mesma oração tropeça por construção, e a cura é quebrar em duas: `vi que você baixou o guia e o que mais te fez baixar logo esse foi o quê?` junta as duas e tropeça na leitura em voz alta. A abertura é a única linha do agente sem segunda chance: escreva primeiro e releia por último.

**Número medido do perfil entra literal na prova, DENTRO da mensagem que sai.** Trocar um número medido por um vago (`dezenas`, `várias`, `muitas`) reprova, porque perde a prova sem ganhar ressalva. O vago só entra onde o perfil marca `[A CONFIRMAR`. Prova que ficou no arquivo interno não é prova: o destinatário lê a mensagem, não a sua lista, e a mensagem enviável carrega pelo menos uma prova com número literal do perfil. Cole `provas na mensagem: N · com número literal do perfil: N (mínimo 1) · vagas: 0`.

**Cinco contas sem cinco motivos é uma conta repetida cinco vezes, e as duas linhas são literais.** Quando a lista não sustentar N recortes, as duas linhas são obrigatórias e literais: a abertura `a lista não sustenta N recortes: <o que falta>` na primeira linha da peça, e `motivos distintos: N · contas: N` no fecho, entregando **um** modelo com os campos a preencher em vez de N cópias. A decisão explicada em prosa no relato não conta: o dono confere o número em um segundo e a prosa em um minuto. O volume falso custa ao dono o tempo de descobrir que são iguais.

**Todo texto enviável sai em bloco cercado, com o prazo fora dele.** Do assunto à linha de descadastro, cada toque tem bloco próprio e o prazo (`Toque 1, 3 dias depois`) fica FORA do bloco: o que está fora é bastidor, e o dono nunca copia por engano. Cole `blocos de copy no arquivo: N · textos enviáveis: N`, iguais.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**A lei-mãe:** mensagem sem pesquisa não sai daqui. Não porque personalizar é bonito, mas porque a mensagem genérica ensina o destinatário a ignorar tudo que vier depois daquele remetente, e esse dano dura anos.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as 4 ações num caso fictício de nicho neutro: a lista com o critério de recorte, a pesquisa de uma conta, o motivo escolhido, a mensagem por dois canais, a sequência de retomada e a régua de volume. Ler antes da primeira pergunta economiza uma rodada de retrabalho.

**Sobre pesquisa e envio:** dado de contato, notícia e histórico vêm de conector de enriquecimento, CRM ou e-mail quando o ambiente tiver algum conectado; se não tiver, busque na web quando o ambiente permitir; se nem isso, peça ao dono o que ele já sabe de cada conta. Quando houver conector de e-mail, o rascunho pode nascer direto na caixa do dono; quando não houver, o texto sai pronto pra copiar. **Nada afirmado sobre a empresa entra sem fonte.** Sem fonte, a frase sai ou vira pergunta.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a lista de alvos e a oferta e eu escrevo a prospecção). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pra escrita com o que o dono colou. Se faltar um insumo que a abordagem não vive sem (a conta-alvo, o motivo de falar agora), pergunta AQUELE insumo e segue, sem repetir a entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Pergunta quem são os alvos, o que o dono vende e o canal, uma coisa de cada vez, e escreve a abordagem com o que ele for dando.

A pergunta do modo é UMA por lote. As outras três partes acontecem nos passos abaixo:

- **Ensina enquanto faz:** em cada escolha estrutural (o motivo real de falar agora, o canal, a régua de volume) escreve UMA linha do porquê. O dono lê a razão e aprende a prospectar sozinho.
- **Puxa o material bruto:** quando a resposta vier rasa ("empresas do meu nicho", "porque meu serviço é bom"), não segue com o genérico. Pede o concreto que só o dono tem: o gatilho real na conta-alvo (uma contratação, um post, uma mudança), um cliente parecido que ele já atendeu, o resultado que entregou. Gatilho real vira abertura que responde; resposta rasa vira spam ignorado.
- **Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer outro canal? a sequência de retomada mais longa? o tom mais direto? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "escreve um e-mail frio pra [empresa]", "abordagem pra essa conta", "mensagem de conexão" | **2 e 3, e a mensagem sai** |
| "monta minha lista de prospecção", "quem eu deveria abordar", "que critério eu uso pra escolher conta" | **1 · A LISTA** |
| "pesquisa essa empresa", "o que eu falo pra abrir com eles", "qual o gancho" | **2 · A PESQUISA E O MOTIVO** |
| "escreve a mensagem", "e-mail ou LinkedIn?", "como começo essa conversa" | **3 · A MENSAGEM** |
| "sequência de follow-up", "ele não respondeu, e agora", "quantos toques", "quantos por dia posso mandar" | **4 · RETOMADA E VOLUME** |
| "prospecta essa lista inteira" | **as 4 na ordem, com parada em cada** |

Pedido ambíguo ("quero prospectar", "preciso de cliente novo"): pergunte UMA coisa só, **"quem é a conta perfeita pra você, e por que ela precisaria falar com você esta semana?"**, mostre a tabela acima como cardápio e siga pela resposta.

## Como ler cada ação

Toda ação abaixo traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de oferta, proposta de valor em uma frase, casos e assinatura: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`.

**Três regras que valem em toda ação:** pesquisa antes de escrever, sempre · um pedido só por mensagem · e a lista fria nunca entra em ferramenta de disparo em massa, porque isso queima o domínio de e-mail do dono e o estrago é permanente.

---

## Ação 1 · A LISTA (quem vale a pena abordar)

**O que faz:** define o recorte da lista e organiza as contas em ordem de prioridade, com o motivo de cada uma estar ali.

**Precisa de:** o **cliente perfeito** descrito por características observáveis (setor, tamanho, região, o que a empresa faz, sinal de que ela tem o problema) · a **capacidade real** de atendimento do dono (quantas conversas por semana ele aguenta) · as contas que ele **já tem em mente** · o que ele **já vendeu** e pra quem, porque o melhor recorte costuma ser parecido com quem já comprou.

**Sem o insumo:** entrevista curta de 4 perguntas: descreva o cliente que você mais gostou de atender · o que ele tinha em comum com os outros bons · quantas conversas por semana você consegue atender de verdade · quais empresas você já quis atender e nunca abordou. Sem capacidade declarada, assuma 5 conversas por semana e dimensione a lista por isso, avisando em 1 linha. Lista grande demais pra capacidade vira prospecção mal feita em todas.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar. **E o marcador só mora em posição de CAMPO:** um link, um número, uma data ou um valor, no fim da linha, substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase que alguém fala, ouve ou lê, e em qualquer peça exportada que o dono manda pra fora sem reler. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça; o furo em si vai pro handoff, nunca pra fala. Checagem: apague o marcador e leia a frase, e a pergunta é "a frase existiria sem o dado?". Com shell, `grep -n "\[A CONFIRMAR" <peça>` lista as linhas pra conferir uma a uma. Cole `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Sem lista e sem cidade dadas pelo dono.** Esta skill nunca gera nome de negócio, domínio, telefone ou e-mail. Faltando a lista de contas ou a região, a Ação 1 entrega o recorte escrito e a tabela em placeholder marcado (`Conta 1 [A CONFIRMAR: nome]`, `[A CONFIRMAR: cidade]`), com a coluna de critério preenchida em cada linha, e a mensagem da Ação 3 é escrita sobre o placeholder. Diga ao dono, em 1 linha, que ele preenche os nomes antes de enviar. Checagem verificável antes de fechar: todo nome próprio da tabela ou veio de linha do insumo do dono, e você aponta qual, ou está entre colchetes como `[A CONFIRMAR]`. Nome inventado, ainda que plausível, reprova a entrega inteira.

**Entrega:** `lista-prospeccao.md`, com o critério de recorte escrito no topo e a tabela de contas em ordem de prioridade. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/recorte-e-lista.md` (os 5 sinais que definem um bom recorte e como priorizar).

**Profundidade:** `references/gate-da-abordagem.md`.

**Os passos:**
1. Escreva o **recorte em uma frase**, com característica observável. Ruim: "empresas que querem crescer". Bom: "rede de 5 a 20 lojas físicas, com estoque próprio e sem sistema de gestão".
2. Cruze com o que já vendeu: os três melhores clientes têm alguma coisa em comum que o recorte precisa capturar.
3. Adicione o **sinal de momento**: o que faz a conta ter o problema agora (abriu unidade nova, contratou pra uma função específica, mudou de comando, apareceu numa lista de crescimento, teve um problema público).
4. Priorize em três degraus: **A** (recorte cheio mais sinal de momento), **B** (recorte cheio, sem sinal), **C** (recorte parcial). Ataque A inteiro antes de tocar em B.
5. Dimensione pela capacidade: se o dono atende 5 conversas por semana, uma lista A de 40 contas é um mês de trabalho, e é o suficiente.

---

## Ação 2 · A PESQUISA E O MOTIVO (por que falar com ela agora)

**O que faz:** pesquisa a conta e escolhe o motivo que vai abrir a mensagem, com a fonte anotada.

**Precisa de:** o **nome da pessoa e da empresa**, ou o cargo e a empresa · o que a empresa faz e para quem · o que mudou por lá nos últimos 90 dias · o que a pessoa publicou ou disse, quando existir · se já houve algum contato antes.

**Sem o insumo:** sem acesso a pesquisa nenhuma, pergunte ao dono numa mensagem só: o que você já sabe dessa empresa, e por que você quer atender ela. Se ele não souber nada, **a conta sai da lista A e volta pra B**, porque abordagem sem motivo tem retorno perto de zero e queima o contato. Isso é um resultado legítimo da ação, não uma falha.

**Entrega:** a seção de pesquisa do `abordagem-[conta].md`: quem é a pessoa, o que a empresa faz, os fatos encontrados com fonte, e o **motivo escolhido** em uma frase. **STOP quando for a única ação pedida.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/motivos-e-pesquisa.md` (a escada de 5 motivos, do mais forte ao mais fraco, e onde procurar cada um).

**Profundidade:** `references/recorte-e-lista.md` · `references/gate-da-abordagem.md`.

**A escada dos 5 motivos, do mais forte pro mais fraco:**

| Motivo | Por que funciona | Onde procurar |
|---|---|---|
| **1. Fato recente** (abriu unidade, mudou de comando, contratou pra uma função, anunciou expansão) | é o mais oportuno: o problema acabou de nascer | site da empresa, imprensa local, vagas abertas, rede profissional |
| **2. Conexão em comum** | prova social emprestada, e a taxa de resposta multiplica | rede profissional, cliente atual, associação do setor |
| **3. Algo que a pessoa publicou** (texto, entrevista, palestra) | mostra que houve leitura de verdade | perfil da pessoa, blog da empresa, vídeo de evento |
| **4. Iniciativa declarada da empresa** (projeto, meta pública, novo produto) | conecta com a prioridade dela | site, comunicado, relatório |
| **5. Dor típica do cargo** | o mais fraco, mas ainda melhor que nada | conhecimento do setor |

**A regra:** só desça um degrau quando o de cima não existir. E se só o degrau 5 existir, escreva a mensagem mais curta possível e não finja pesquisa que não houve.

**O que nunca conta como motivo:** "vi que você trabalha na [empresa]" · "parabéns pela sua trajetória" · "acompanho o trabalho de vocês". São frases que anunciam que ninguém pesquisou nada.

---

## Ação 3 · A MENSAGEM (o canal e o texto)

**O que faz:** escolhe o canal e escreve a mensagem, com o raciocínio de cada escolha ao lado.

**Precisa de:** o motivo da Ação 2 · o **contato disponível** (e-mail confirmado, perfil na rede profissional, mensagem direta) · a **proposta de valor do dono** em uma frase · um **caso próximo** pra citar, quando existir · o **pedido**: o que ele quer que a pessoa faça.

**Sem o insumo:** sem contato de e-mail confirmado, escreva pela rede profissional, que não depende de endereço. Sem caso pra citar, apoie no mecanismo e marque `[A CONFIRMAR: prova]`, porque caso inventado numa abordagem fria é o pior começo possível de relacionamento. Sem pedido declarado, use o de menor fricção: uma conversa de 15 minutos.

**O nome do destinatário é literal, e a anonimização não vale pra ele.** O crivo 08 protege TERCEIROS citados dentro de uma peça; a pessoa a quem a mensagem é endereçada usa o primeiro nome literal do insumo. Sem nome no insumo, a mensagem abre sem vocativo, nunca com inicial. Certo: `Fernanda, eu li o que você escreveu hoje de manhã.` Errado: `F., eu li o que você escreveu hoje de manhã.` Cole no `conferencia/checagem-titulos.md`, abaixo do bloco do script, a linha `mensagens escritas: N · com primeiro nome do destinatário no vocativo: N`, e diferença entre os dois números reprova (ver `references/08-consentimento.md`).

**O nome fica no arquivo que o dono USA, e a anonimização é só da peça pública.** A fila do dia, o dossiê da call, a lista de prospecção e o caso de reclamação são ferramenta de trabalho: o dono lê a linha e responde no aplicativo de mensagem chamando a pessoa pelo nome. Trocar por `contato 1`, `contato A` ou pela inicial obriga ele a abrir um segundo arquivo e cruzar número com nome numa manhã corrida, e é exatamente o que ele não faz. Então: nome literal na coluna, na linha e no cabeçalho do arquivo interno, sempre. A régua de consentimento continua valendo inteira na peça PÚBLICA (post, carta, landing, anúncio, stories, reel, e-mail em massa), que é onde o nome causa dano. O `checar_titulos.py` classifica o arquivo e imprime `uso interno: <arquivo>` pros que ficam de fora do gate de nome; se o arquivo interno desta rodada não aparecer nessa lista, dê a ele um nome que diga o que ele é (`fila-do-dia.md`, `dossie-call-<primeiro nome>.md`, `lista-de-prospeccao.md`).

**E o papel do nome muda por ARQUIVO.** A mesma pessoa é destinatária no arquivo de mensagens e terceiro em qualquer documento que fale SOBRE ela (fila, critério, triagem, relatório), e cada arquivo segue a regra do seu papel: nome literal em vocativo lá, `contato <N>` sem identificação aqui, com o número da posição amarrando os dois. Cole as duas linhas separadas, `nomes literais no arquivo de mensagens: N (todos em vocativo)` e `nomes literais nos documentos de trabalho: 0` (ver o bloco "O papel do nome muda por ARQUIVO" em `references/08-consentimento.md`).

**Molde endereçado a pessoa nomeada exige o insumo dela aberto:** rode `grep -n '<Nome>' <insumo>` e cole a saída antes da fala, na forma do bloco "Fala atribuída ao destinatário" de `references/08-consentimento.md`. Fala atribuída sem trecho literal do insumo reprova. Cole `moldes com nome próprio: N · com fala literal do insumo: N`, os dois iguais.

**Entrega:** `abordagem-[conta].md`, com o e-mail (assunto, 2 opções extras de assunto, corpo), a versão pra rede profissional (pedido de conexão e mensagem depois de aceito), e a tabela que explica cada escolha. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/mensagem-e-canal.md` (a estrutura da mensagem, os moldes por cenário e as regras de formato).

**Profundidade:** `references/motivos-e-pesquisa.md` · `references/gate-da-abordagem.md`.

**A estrutura da mensagem fria (4 movimentos, nesta ordem):**
1. **Abertura pelo motivo.** A primeira frase é sobre a pessoa ou a empresa, nunca sobre o dono. E é específica o bastante pra não servir a mais ninguém.
2. **A ponte.** Uma ou duas frases ligando aquele fato ao problema que o dono resolve. Sem enumerar solução.
3. **A prova, curta.** Um resultado de alguém parecido, com número quando houver. Uma frase, não um parágrafo.
4. **O pedido, um só, de baixa fricção.** Pergunta que se responde com sim ou não.

**As regras de formato que valem em todo canal:** texto puro, sem marcação de negrito ou itálico que não renderiza · parágrafos de duas a três linhas · abaixo de 120 palavras no e-mail frio · assunto abaixo de 50 caracteres, sem promessa exagerada · assinatura simples · nada de anexo no primeiro toque.

**A escolha de canal:**

| Situação | Canal |
|---|---|
| e-mail confirmado | e-mail primeiro, rede profissional como reforço dias depois |
| sem e-mail | pedido de conexão na rede profissional, e a mensagem só depois de aceito |
| conexão em comum disponível | pedir a apresentação primeiro, sempre; é o caminho de maior retorno e ninguém usa |
| a pessoa publica com frequência | comentar de verdade num texto dela antes, e só então abordar |

**O que nunca entra:** abertura desejando que a mensagem encontre a pessoa bem · o parágrafo de apresentação da empresa do dono · lista de funcionalidades · dois pedidos na mesma mensagem · elogio genérico · marcação de negrito no corpo do e-mail.

---

## Ação 4 · RETOMADA E VOLUME (o que fazer depois do silêncio)

**O que faz:** escreve a sequência de retomada e a régua de volume que protege o remetente.

**Precisa de:** a mensagem da Ação 3 · quantas contas o dono vai abordar por semana · o canal usado · se o domínio de e-mail dele é novo ou antigo.

**Sem o insumo:** sem histórico de domínio declarado, assuma domínio sem aquecimento e use a régua conservadora (a tabela abaixo). É a premissa segura: errar pra cima aqui custa o domínio.

**Entrega:** a seção de retomada do `abordagem-[conta].md` mais `regua-volume.md` quando a prospecção for em lista. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/retomada-e-volume.md` (os 3 toques, o que cada um muda, e a régua de volume por situação de domínio).

**Profundidade:** `references/gate-da-abordagem.md`.

**Os 3 toques da retomada** (e a regra que os torna suportáveis: **cada toque traz um ângulo novo**, nunca "só passando pra saber se você viu"):

| Toque | Quando | O que muda |
|---|---|---|
| 1 | 3 dias depois | ângulo diferente do mesmo problema, mais curto que o primeiro |
| 2 | 7 dias depois do toque 1 | uma prova concreta, ou um material útil sem pedir nada |
| 3 | 14 dias depois do toque 2 | o encerramento honesto: diz que para de escrever e deixa a porta aberta |

O terceiro toque é o que mais recebe resposta de toda a sequência, e por isso ele nunca é irônico nem
passivo. Ele encerra de verdade: sem resposta, a conta sai por 6 meses.

**A régua de volume:**

| Situação do domínio | E-mails frios por dia | Cuidado |
|---|---|---|
| domínio novo, sem aquecimento | 5 a 10 | subir 5 por semana, e só se ninguém marcar como spam |
| domínio com 3 meses ou mais de envio normal | 20 a 30 | acompanhar retorno de erro e reclamação |
| domínio antigo e com histórico limpo | 40 a 50 | teto prático de prospecção manual honesta |

**As quatro regras que protegem o remetente:** nunca use a caixa principal do negócio pra prospecção em volume (use um domínio secundário) · nada de disparo em massa com a mesma mensagem · saída fácil oferecida em texto simples, mesmo em mensagem individual · e quem pediu pra não receber sai para sempre, de toda lista, sem exceção.

---

## O gate da abordagem (roda por dentro, e não imprime)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Fontes consultadas (esta skill pesquisa, então a seção é obrigatória).** A seção "Fontes consultadas" da entrega lista só o que foi de fato aberto neste turno, e cada linha traz o comando ou a chamada de ferramenta que abriu aquela fonte. Sem acesso à web no ambiente, a seção diz exatamente "sem acesso à web neste ambiente" e nada mais: nenhum domínio, nenhum nome de marca, nenhuma data de busca. Checagem verificável antes de fechar: conte as linhas da seção e conte os comandos registrados no relatório e escreva os dois números lado a lado, nesta forma: `fontes declaradas: N · comandos no log: N`. **Declarar 4 buscas com 1 comando no log reprova**, e o conserto é apagar as 3 linhas sem comando, nunca inventar o comando. **Cada linha de tabela sobre terceiro traz a consulta que a produziu e o trecho citado da página aberta.** Número (preço, prazo, prazo de entrega, volume, quantidade de alunos, faturamento) vindo de página de terceiro só entra com o trecho colado ao lado; sem trecho colado, o campo sai como `[A CONFIRMAR: exige abrir a página]`, e cravar o número mesmo assim reprova a entrega inteira. Memória de treino e inferência plausível não são fonte.


Os 5 checks anti-IA, inline:
1. **Travessão longo:** zero ocorrência de U+2014 e U+2013 no arquivo inteiro, notas incluídas.
2. **Verbo-freio banido:** a família que a régua anti-voz proíbe (o verbo que rima com "cravar" e todas as flexões) não aparece. Use emperrar, empacar, parar, freio, amarra.
3. **Antítese de espelho:** nada do molde que nega um polo curto pra afirmar o outro, em uma frase ou em duas, com ou sem a preposição "sobre", nem duas negações paralelas empilhadas.
4. **Verbo de transformação genérico:** a família de verbos grandiosos de folheto. Troque por concreto: resolve, tira, muda, corta.
5. **Abertura e fecho de robô:** a saudação de praxe que deseja que a mensagem encontre a pessoa bem, o convite a imaginar, a pergunta retórica de introdução, a moldura que anuncia um segredo, o fecho que agradece a leitura.

Mais os checks próprios do formato, binários, com **o teste da troca de nome** na frente: **trocando o nome da empresa por outro, a mensagem continua fazendo sentido? Se continuar, ela reprova**, porque não foi pesquisada. Depois: **motivo com fonte** · **um pedido só** · **abaixo de 120 palavras** no e-mail frio · **texto puro**, sem marcação · **prova declarada** ou marcada `[A CONFIRMAR: prova]` · **sem anexo** no primeiro toque · **saída oferecida** · **volume dentro da régua**.

**A mensagem é o que o destinatário lê, e só isso.** Antes de fechar cada abordagem, isole o bloco de copy (do "Assunto:" à assinatura) e rode duas checagens sobre ele isolado: `grep -nE "\[A CONFIRMAR|\[a preencher|confirme|valide|antes de enviar|usar somente se"` tem que voltar VAZIO, e o grep de nomes do consentimento tem que voltar vazio ou com a autorização apontada por `<arquivo:linha>`. Todo furo, toda pendência e toda condição de uso vivem numa seção `ANTES DE ENVIAR` acima do bloco, nunca dentro dele. Campo que o dono cola (o nome da pessoa, o nome da clínica) fica como `[Nome]` no início da linha; **pendência de autorização e condição de pesquisa NUNCA entram, porque não são campos, são decisões.** Cole `bloco de copy: <arquivo>:<linha inicial>-<linha final> · marcadores dentro dele: 0 · nomes de terceiro dentro dele: 0`.

**Dentro do bloco de copy só existe campo, e campo é substituível por colagem sem reescrever a frase.** Rode e cole a saída:

```
grep -oE '\[[^]]*\]' <bloco de copy> | awk '{print NF, $0}'
```

**Qualquer colchete com mais de 3 palavras dentro do bloco reprova a abordagem.** Cole `campos no bloco: N · com mais de 3 palavras: 0 · instruções movidas pro ANTES DE ENVIAR: N`. O `checar_titulos.py` conta o marcador acima de 6 palavras e reprova ali; dentro do bloco de copy o teto é mais apertado, e são 3.

**Prova de terceiro em mensagem fria sai sempre anonimizada, sem exceção e sem marcador.** "Uma aluna de 52 anos voltou a subir escada sem dor" é publicável; "Márcia, 52" não é, e a diferença não é o marcador ao lado, é o nome. Marcar `[A CONFIRMAR: autorização]` e enviar assim mesmo reprova: o marcador registra a dúvida e não resolve o risco. **E a anonimização é de reidentificação, não só de nome:** num destinatário da área de saúde, idade exata mais condição mais resultado mais prazo identificam a pessoa mesmo sem o nome, então a faixa etária substitui a idade exata ("mulher na casa dos 50") e o prazo não confirmado sai da frase em vez de virar marcador.

**Com shell disponível, rodar `python3 scripts/lint_copy.py <arquivo>` sobre a entrega é obrigatório, não opcional.** Sem shell, faça a busca manual pelos dois bloqueios duros do check 1 e do check 2.

---

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Quem já chegou sozinho, respondeu anúncio, caiu na lista, mandou mensagem primeiro | **soft-vendas-sdr** | não faço. Lead que chegou sozinho pede outro tom, e usar abordagem fria nele custa a conversa |
| Preparar a call que já está marcada | **soft-vendas-call-prep** | listo os fatos da pesquisa, sem o roteiro da conversa |
| Conduzir a conversa quente, objeção ao vivo, fechar | **soft-vendas-closer** | não faço |
| Campanha de e-mail pra base que já é do dono | **soft-email-sequencia** | não faço. Base própria e lista fria têm réguas opostas |
| A régua pós-isca de quem baixou material | **soft-funil-nutricao** | não faço |
| A proposta comercial depois da conversa | **soft-vendas-proposta** | não faço |
| Contrato | **soft-vendas-contratos** | não faço |
| Posicionamento, oferta, proposta de valor em uma frase | **soft-plano-posicionamento** | uso a entrevista curta de 4 perguntas da Ação 1 |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/recorte-e-lista.md` · `references/motivos-e-pesquisa.md` · `references/mensagem-e-canal.md` · `references/retomada-e-volume.md` · `references/gate-da-abordagem.md` · `scripts/lint_copy.py` (o anti-IA em código, rode no shell quando o ambiente permitir).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `abordagem-rede-oficinas-sul.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com a lista fechada de contagens, uma por linha, exatamente nesta forma:

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

**As contagens de R3, R4 e R5 são gates, não termômetros.** Quando `com inimigo ou inversão` ficar abaixo da metade do lote, `teses distintas` abaixo de 3, ou `em molde de antítese` acima de 1, a entrega **não sai**: os títulos reprovados voltam pro passo de escrita, são reescritos, e a checagem final mostra a contagem corrigida mais a linha `reescritos por contagem: N (<contagem que reprovou>)`. Declarar a contagem que reprova e publicar assim mesmo é o pior dos dois mundos, porque produz um documento que prova o próprio defeito e não o corrige: o dono lê `0 de 4` e não tem como saber que isso significa que a régua reprovou. **Nenhuma justificativa de tipo de peça vale aqui:** se o formato dispensa a inversão, a exceção mora escrita na receita do tipo, e a entrega cita a linha dessa receita. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**

## A frase que a dona repetiria (fecho, uma por entrega)

Escolha a UMA frase da entrega que a dona repetiria de cor numa conversa, cole ela sozinha e responda por escrito por que ela sobrevive fora do contexto: sem a peça em volta, sem o nome do produto, sem a explicação que vem antes. Cole `frase que sobrevive fora do contexto: <literal>`. Correta e morna é o defeito comum aqui: a abertura que serve pra qualquer serviço do mesmo tipo não é a frase, é o preenchimento. Nenhuma frase significa que a peça está correta e não está viva, e a entrega volta pro passo de escrita.

## Passo 2 da checagem (fecho, roda por comando)

Depois de gravar todos os entregáveis, rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída. Ele exige o `conferencia/checagem-titulos.md` na pasta, confere o inventário (os 4 inteiros, o piso e o `inventário duplicado`), o universo dos títulos, o marcador acima de 6 palavras, o nome de conversa privada, a `saída do script reescrita` e o lint de todo `.md`, RELATO incluso. **`exit` diferente de 0 reprova a entrega inteira, antes da análise de conteúdo.**
