---
name: soft-email-sequencia
description: >-
  Escreve a CAMPANHA DE E-MAIL pronta pra subir na ferramenta: cada e-mail com assunto, prévia, corpo, CTA, dia de envio e condição, mais a ramificação por comportamento, a saída e as metas. Use quando o pedido for: "monta uma campanha de e-mail", "sequência de e-mails de venda", "e-mails de boas-vindas", "onboarding por e-mail", "e-mail de pós-venda", "recuperação de carrinho", "e-mail de reengajamento", "win-back", "sequência de lançamento por e-mail", "drip de e-mail", "quantos e-mails mandar", "teste A/B de assunto". NÃO use pra: a régua pós-isca que aquece o lead até o convite em WhatsApp, Direct ou e-mail (soft-funil-nutricao); a sequência de carrinho de lançamento com evento (soft-launch); mensagem de dentro do webinar por percentual assistido (soft-webinar); prospecção fria pra quem nunca ouviu falar de você (soft-vendas-outreach); carta ou VSL (soft-funil-carta); página (soft-funil-landing). Leia e siga o fluxo inteiro do SKILL.md.
---

# A campanha de e-mail, do arco à ferramenta

Esta skill escreve a sequência de e-mail inteira e pronta pra configurar: o arco narrativo que liga o primeiro ao último e-mail, cada peça com assunto, prévia, corpo, CTA e dia, a ramificação por comportamento, as condições de saída e as metas que dizem se a campanha funcionou. O resultado é sempre um arquivo nomeado, com a tabela de visão geral no topo e o checklist de subida no fim.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Leitura em voz alta, por mensagem, com o resultado colado.** Toda mensagem que o lead recebe passa pela leitura em voz alta antes de sair. Cole `molde N | lida em voz alta: passa/tropeça | onde tropeça: <trecho>` pra cada mensagem da sequência, e feche com `lida em voz alta: sim · frase junta afirmação e pergunta: 0`. Frase que emenda uma afirmação e uma pergunta direta na mesma oração tropeça por construção, e a cura é quebrar em duas: `vi que você baixou o guia e o que mais te fez baixar logo esse foi o quê?` junta as duas e tropeça na leitura em voz alta. A abertura é a única linha do agente sem segunda chance: escreva primeiro e releia por último.

**Todo texto enviável sai em bloco cercado, com o prazo fora dele.** Do assunto à linha de descadastro, cada toque tem bloco próprio e o prazo (`Toque 1, 3 dias depois`) fica FORA do bloco: o que está fora é bastidor, e o dono nunca copia por engano. Cole `blocos de copy no arquivo: N · textos enviáveis: N`, iguais.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**O universo da R3 é o das unidades produzidas, nunca o dos pilares.** As `teses distintas` saem das pautas, headlines ou frames que a peça entrega, e a contagem igual ao número de pilares do dono é resultado inválido. Cole `unidades no lote: N · linhas em teses.txt: N`, os dois iguais, e só então a matriz de pares.

**`teses.txt` é arquivo obrigatório da pasta de saída**, uma tese de até 4 palavras por linha, ao lado do `conferencia/checagem-titulos.md`. Sem ele o gate não calcula a R3 e o campo do fecho sai com a instrução do script no lugar do número, o que reprova a entrega.

**A lei-mãe:** e-mail que vende faz UM trabalho por peça e UMA pergunta por CTA. Sequência não é um monte de e-mails no mesmo assunto, é uma escada: cada degrau só existe porque o anterior deixou uma coisa em aberto.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra as 4 ações num caso fictício de nicho neutro: o arco declarado, a tabela de visão geral, dois e-mails escritos por inteiro, o desenho da ramificação, a tabela de metas e o checklist de subida. Ler antes da primeira pergunta economiza uma rodada de retrabalho.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola tudo que tem sobre a oferta e a base e eu escrevo a sequência). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou. Se faltar um insumo que a sequência não vive sem (a oferta, o destino do CTA, quem é a base), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez, e monta a campanha com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda a campanha (o arco, quantos e-mails, a ramificação por comportamento, o CTA), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a decidir sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("meus leads", "a de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: uma frase literal que um cliente respondeu, um número que aconteceu na última campanha, a história de um lead real que abriu e não comprou. Material bruto vira a âncora dos e-mails; resposta rasa vira sequência rasa. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar a sequência, fecha com UMA linha: "Quer mais curto? Outro tom no assunto? Mais e-mails no meio? Me diz o que ajustar que eu refaço só essa parte." A oferta de refino não substitui o STOP nem o gate.


## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "monta uma campanha de e-mail", "sequência de e-mails", "e-mails de boas-vindas", "onboarding por e-mail", "sequência de lançamento por e-mail", "drip" | **1 · A SEQUÊNCIA** |
| "e-mail de pós-venda", "depois que comprou", "recuperação de carrinho", "upgrade", "quero vender de novo pra quem já comprou" | **2 · PÓS-VENDA E EXPANSÃO** |
| "reengajamento", "win-back", "quem parou de abrir", "cliente que cancelou", "e-mail pra base que sumiu" | **3 · REENGAJAMENTO E RESGATE** |
| "monta a ramificação", "quem recebe o quê", "quando a pessoa sai da sequência", "teste A/B de assunto", "que número eu persigo" | **4 · LÓGICA, TESTE E META** |
| "a campanha inteira, do zero ao configurado" | **1 ou 2 ou 3 conforme o tipo, depois 4, com parada em cada** |

Pedido ambíguo ("me ajuda com os e-mails", "minha lista não responde"): pergunte UMA coisa só, **"o que essa pessoa fez pra entrar nessa sequência?"**, mostre a tabela acima como cardápio e siga pela resposta. É o comportamento de entrada que decide o tipo, não o produto.

## Como ler cada ação

Toda ação abaixo traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de voz, oferta, avatar ou prova: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" da ação e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente número, caso, nome ou fala.

**Três regras que valem em toda ação:** cliente sai de toda sequência de aquisição no mesmo dia em que compra · nenhum e-mail sai sem link de saída da lista · e ninguém recebe dois e-mails de duas sequências diferentes no mesmo dia (a checagem de colisão é do passo final de toda ação).

---

## Ação 1 · A SEQUÊNCIA (o arco e as peças)

**O que faz:** desenha o arco da campanha e escreve cada e-mail por inteiro, com dia, condição e CTA.

**Precisa de:** o **gatilho de entrada** (o que a pessoa fez pra receber o primeiro e-mail), perguntado ao dono · o **objetivo** da campanha em uma frase (o que precisa acontecer pra ela ter funcionado) · **quem recebe** e em que estágio essa pessoa está · a **oferta** e o preço, do perfil/brain do agente · **3 a 5 falas literais** de dor e desejo do público · o **material que já existe** pra citar (aula, artigo, caso, vídeo).

**Sem o insumo:** entrevista curta de 6 perguntas, uma por vez: o que a pessoa fez pra entrar nessa lista · o que precisa acontecer pra você considerar essa campanha um sucesso · o que você vende e por quanto · a frase que essa pessoa fala no pior do problema · que prova real você pode citar · que material pronto você já tem pra linkar. Sem o número de e-mails declarado, use o padrão do tipo (a tabela de tipos abaixo) e diga em 1 linha qual premissa assumiu. Sem cadência declarada, use denso na primeira semana e espaçado depois.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `sequencia-email.md`, com o bloco de configuração no topo (gatilho, objetivo, público, tipo, número de peças, cadência, saída, furos), a **tabela de visão geral**, cada e-mail por inteiro, e o checklist de subida no fim. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/tipos-e-cadencias.md` (o tipo certo, o número de peças e o espaçamento de cada um) · `references/anatomia-do-email.md` (o que cada peça carrega, campo por campo).

**Profundidade:** `references/logica-de-fluxo.md` (ramificação, saída, supressão) · `references/gate-linha-a-linha.md` (o critério de cada check do gate).

**Os passos:**
1. Declare o **arco** antes de escrever a primeira linha: que história a campanha inteira conta, do primeiro ao último e-mail, e como a intensidade sobe. Arco não declarado vira sete e-mails repetidos.
2. Mapeie cada e-mail a **um estágio** da jornada (não conhece o problema, conhece e compara, decide, usa, expande) e a **um trabalho só**.
3. Monte o **bloco de configuração** e a **tabela de visão geral** (`#` · assunto · trabalho · dia · CTA · condição). Ela é o mapa que o dono aprova antes de você escrever o corpo.
4. **STOP.** Mostre só o arco mais a tabela e pergunte "essa é a escada? escrevo os e-mails?".
5. Depois do OK, escreva **um e-mail por vez** pelo molde de `anatomia-do-email.md`: 2 a 3 opções de assunto · prévia que complementa o assunto sem repetir · o trabalho da peça em 1 frase · corpo em parágrafos de 2 a 3 linhas · **um CTA principal** com destino · o dia · quem recebe e quem pula.
6. Rode o **gate por dentro** (Ação 4) em cada e-mail. E-mail reprovado é refeito, não a campanha inteira.
7. Feche com o **checklist de subida**: criar a automação, configurar o gatilho, colar cada peça com o atraso certo, ligar ramificação e saída, ligar a medição.

**Os tipos e a grade padrão de cada um** (adapte pelo objetivo, nunca corte o fechamento):

| Tipo | Peças e janela | A escada |
|---|---|---|
| Boas-vindas / onboarding | 5 a 7 em 14 a 21 dias | recebe e sabe o que esperar · primeira vitória rápida · o recurso central por dentro · o uso avançado · prova de quem já fez · pergunta de acompanhamento · próximo passo |
| Nutrição de lista | 4 a 6 em 3 a 4 semanas | conteúdo que serve sozinho · o problema nomeado · a solução posicionada com prova · resultado de quem aplicou · convite leve · convite direto |
| Lançamento | 4 a 6 em 2 a 3 semanas | aviso de que vem coisa · abertura com tudo · um uso por dentro · prova e primeiros resultados · condição com prazo · último aviso |
| Pós-evento | 3 a 4 em 7 a 10 dias | obrigado com o resumo do que passou · os materiais reunidos · o próximo passo · a pergunta de retorno |
| Educacional | 5 a 8 em 4 a 6 semanas | o que a pessoa vai aprender · fundamento · intermediário · avançado · exercício de aplicação · materiais · fecho e próximo passo |

---

## Ação 2 · PÓS-VENDA E EXPANSÃO (quem já comprou)

**O que faz:** escreve a sequência que recebe o cliente novo, garante o primeiro uso, e depois abre a próxima compra pela conta que ele mesmo já viu.

**Precisa de:** o que a pessoa **acabou de comprar** e o que ela recebe na prática · o **momento em que o valor aparece** (quantos dias até ela ter o primeiro resultado), perguntado ao dono · o que existe **acima** na esteira (o produto seguinte, o plano maior, o serviço) e o preço · o **motivo real** de quem cancela ou some, que o dono ouve.

**Sem o insumo:** entrevista curta de 5 perguntas: o que ela comprou · o que ela recebe no primeiro dia · quanto tempo até o primeiro resultado · o que você vende depois disso · por que as pessoas param. Sem o momento do valor declarado, assuma 7 dias, escreva a peça de acompanhamento com o marco parametrizado e avise em 1 linha que o número precisa ser confirmado.

**Entrega:** `pos-venda-email.md`, com a sequência de recepção e a de expansão separadas, cada uma com o gatilho próprio, e a regra que impede as duas de colidirem. **STOP por sequência.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/tipos-e-cadencias.md`, seção de pós-venda · `references/anatomia-do-email.md`.

**Profundidade:** `references/logica-de-fluxo.md` (a supressão que impede oferta em cima de quem abriu chamado de suporte) · `references/gate-linha-a-linha.md`.

**Os passos:**
1. Separe as duas coisas: **recepção** (garante o primeiro uso e reduz arrependimento) e **expansão** (abre a próxima compra). Misturar as duas na mesma sequência é o erro que mais gera cancelamento.
2. A recepção nunca vende nada nos primeiros toques. Ela confirma, orienta e mostra a primeira vitória.
3. A expansão entra por **marco alcançado**, não por dia no calendário: a pessoa fez o que o produto prometia, e o próximo degrau nasce disso.
4. **Recuperação de carrinho** é caso à parte, 3 peças em 48 horas: o lembrete sem cobrança · a dúvida antecipada (a objeção que emperra a compra, respondida) · o último aviso com prazo real.
5. Escreva a **supressão** junto: quem abriu chamado de suporte nas últimas 48 horas não recebe oferta.
6. Rode o gate. **STOP.**

---

## Ação 3 · REENGAJAMENTO E RESGATE (quem parou de abrir ou já foi embora)

**O que faz:** escreve o arco curto que acorda quem parou de responder e o arco de resgate de quem cancelou, com a poda que protege a entrega dos próximos disparos.

**Precisa de:** há quanto tempo essa base está sem reagir e de **que origem** ela veio · o **tamanho** e se houve disparo recente · o **motivo declarado** de saída, quando existir · o que **mudou** desde que a pessoa foi embora (é o único argumento honesto de resgate).

**Sem o insumo:** se o dono não sabe a origem, abra pela pergunta de uma palavra sem citar produto nenhum e use a resposta pra segmentar. Se ele não sabe o tamanho, escreva o arco e coloque no checklist a instrução de **volume gradual**: comece pelos que pararam há 60 a 90 dias, veja o retorno, só então avance. Se ele não sabe o que mudou, o resgate não tem argumento: diga isso em 1 linha e escreva só o reengajamento.

**Entrega:** `reengajamento-email.md`, com o arco de reengajamento (3 a 4 peças em 10 a 14 dias), o de resgate (3 a 5 peças em 30 dias) quando houver o que contar, o e-mail de corte e as regras de higiene. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/tipos-e-cadencias.md`, seção de base parada · `references/anatomia-do-email.md`.

**Profundidade:** `references/logica-de-fluxo.md` · `references/gate-linha-a-linha.md`.

**Os passos:**
1. Abra por **pergunta**, nunca por oferta. Desconto de cara em base parada é o caminho mais rápido pra caixa de spam.
2. Peça 2 entrega utilidade sem pedir nada. Peça 3 traz a condição com prazo real. Peça 4 corta e diz que corta.
3. No resgate, a peça 1 pergunta o que deu errado e escuta. A peça 2 conta o que mudou. A peça 3 abre a condição. A última fecha a porta sem drama, deixando a volta possível.
4. Escreva as **regras de higiene** junto: volume gradual, remoção de quem não reagiu ao arco inteiro, endereço que devolve erro permanente sai na hora, e quem marcou como spam nunca volta.
5. Rode o gate. **STOP.**

---

## Ação 4 · LÓGICA, TESTE E META (o que faz a campanha rodar sozinha)

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`references/regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo. **E a tabela de assuntos fecha com as três contagens mecânicas da régua, coladas, nunca só com o veredito:** `teses distintas: N` (com a lista de teses ordenada e comparada, uma tese de 4 palavras por assunto), `com inimigo ou inversão: N de N`, e `em molde de antítese: N (teto 1)` com a coluna sim/não ao lado de CADA assunto, inclusive os que dizem não. A contagem do molde não sai da leitura: com shell, `python3 scripts/lint_copy.py <arquivo dos e-mails>` conta o molde na peça inteira, com arquivo e linha de cada ocorrência, e **o número do lint é a autoridade**. A cota vale sobre o corpo dos e-mails, não só sobre a lista de assuntos: uma campanha pode declarar `em molde de antítese: 0` sobre os assuntos e carregar quatro no corpo, e é o lint que decide. Divergência entre o número do lint e o declarado, ou número acima do teto, manda o lote de volta pro passo de escrita antes de qualquer análise de conteúdo.

**Veredito `passa` em 100% dos assuntos reprova o lote.** Uma sequência de recepção tem dois tipos de assunto e eles não competem pela mesma coisa: o de **serviço** descreve por função e o leitor abre porque esperava (a confirmação da compra, o lembrete da call marcada, o recibo), e o de **abertura** disputa o clique numa caixa cheia. Marque cada assunto como `serviço` ou `abertura` na tabela. Os de serviço saem da conta de R2 e não precisam de reescrita. Cada um dos de abertura responde por escrito à pergunta de R7 ("um copywriter de ponta assinaria?"), e toda resposta que não for um sim inequívoco leva a versão reescrita ao lado, que é a versão que vai pro doc. Assunto que já é item de sumário de aula ("O que vem na fase 2", "Sua primeira call individual", "Suas 12 semanas terminaram") reprova direto em R2, porque a reescrita de sumário sai igual ao original. Checagem colada: `assuntos de serviço: N · de abertura: N · de abertura reescritos: N`, e a última coluna zero num lote com mais de 3 assuntos de abertura reprova o lote: uma coluna de N aprovações e zero reescritas é a marca da tabela preenchida depois da escrita, como validação, e não durante, como crivo.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória**, nestes 3 passos: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


**O que faz:** escreve a ramificação por comportamento, as condições de entrada e saída, os testes que valem a pena e as metas de cada métrica.

**Precisa de:** a sequência escrita (de qualquer ação anterior) · os **sinais que a ferramenta do dono registra de verdade** (abriu, clicou, respondeu, comprou), perguntados a ele · o que conta como **conversão** desta campanha, em uma frase.

**Sem o insumo:** se o dono não sabe quais sinais a ferramenta registra, monte a ramificação com os três que qualquer ferramenta pega (clicou, respondeu, comprou) e marque `[A CONFIRMAR: sinais disponíveis]`. Sem conversão declarada, use o CTA do último e-mail como definição e confirme em 1 linha.

**Entrega:** a seção de lógica somada ao arquivo da ação anterior, com o **desenho do fluxo em bloco**, a lista de condições, a tabela de metas e os testes propostos. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/logica-de-fluxo.md` (ramificação, saída, supressão, reentrada, e o desenho em bloco).

**Profundidade:** `references/gate-linha-a-linha.md`.

**Os quatro controles, e o que cada um responde:**

| Controle | A pergunta que ele responde | Exemplo |
|---|---|---|
| Ramificação | quem recebe um caminho diferente, e por qual comportamento | abriu a peça 2 e não clicou, recebe a 2b (o mesmo pedido, mais leve) no lugar da 3 |
| Saída | o que faz a pessoa sair na hora | comprou, agendou, respondeu, ou pediu pra sair |
| Supressão | quando o e-mail não sai mesmo estando na fila | já está em outra sequência ativa, abriu chamado nas últimas 48 horas, ou já recebeu e-mail hoje |
| Reentrada | se a pessoa volta pro início, e em que condição | quem sumiu de novo depois de 90 dias volta pro arco de reengajamento uma vez só |

**As metas por tipo** (ponto de partida pro dono cravar o alvo; ajuste pelo histórico dele quando existir):

| Métrica | Boas-vindas | Nutrição | Reengajamento | Resgate |
|---|---|---|---|---|
| Abertura | 50 a 70% | 20 a 30% | 15 a 25% | 15 a 20% |
| Clique | 10 a 20% | 3 a 7% | 2 a 5% | 2 a 4% |
| Conversão | 15 a 30% | 2 a 5% | 3 a 8% | 1 a 3% |
| Saída da lista | abaixo de 0,5% | abaixo de 0,5% | 1 a 2% | 1 a 3% |

**Os testes que valem a pena**, nesta ordem: assunto (o que mais move a abertura) · texto do botão · dia e horário de envio · tamanho do corpo. Um teste por vez, metade da lista em cada braço, e só declare vencedor com volume suficiente pra diferença não ser sorte. Escreva no arquivo o que está sendo testado, como a divisão foi feita, e qual número decide.

**O gate (roda por dentro, em toda ação, e não imprime):** ele lê o que você acabou de escrever e reprova antes de o dono ver. O veredito é o pior item, e uma reprovação refaz o e-mail, não a campanha.

Os 5 checks anti-IA, inline:
1. **Travessão longo:** zero ocorrência de U+2014 e U+2013 no arquivo inteiro, incluindo notas. Ponto ou hífen comum no lugar.
2. **Verbo-freio banido:** a família que a régua anti-voz proíbe (o verbo que rima com "cravar" e todas as flexões) não aparece. Use emperrar, empacar, parar, freio, amarra.
3. **Antítese de espelho:** nada do molde que nega um polo pra afirmar o outro (o par curto de negação e afirmação colado, com ou sem a preposição "sobre"), nem duas negações paralelas seguidas. Afirme o que é, com sujeito e cena.
4. **Verbo de transformação genérico:** revolucionar, potencializar, alavancar, maximizar, desbloquear. Troque por concreto: resolve, tira, muda, faz.
5. **Abertura e fecho de robô:** a saudação de praxe que deseja que o e-mail encontre a pessoa bem, o convite a imaginar, a moldura de revelação ("o segredo está em", "o que ninguém te conta"), e o fecho que agradece a leitura. Corte e comece pela frase seguinte.

Mais os checks próprios do formato, binários: **um trabalho só** por e-mail · **um CTA principal** com destino escrito · **assunto abaixo de 50 caracteres** quando der, e a prévia complementando em vez de repetir · **ancorado** em fala literal ou prova real com fonte · **furo marcado** em `[A CONFIRMAR: o quê]` · **link de saída** presente · **placeholder repetido reprova a campanha inteira** (o mesmo colchete aparecendo em dois e-mails é sinal de que o insumo faltou e a skill escreveu por cima dele: pare e pergunte).

**Colchete dentro do bloco de copy só como campo substituível:** rode `grep -oE '\[[^]]*\]' <bloco de copy> | awk '{print NF, $0}'` e cole a saída; colchete com mais de 3 palavras reprova, e a instrução volta pro bloco de preparo acima da copy.

**Com shell disponível, rodar `python3 scripts/lint_copy.py <arquivo>` sobre a entrega é obrigatório, não opcional:** é ele que decide o item anti-IA do gate e pega o que o olho perde. Sem shell, faça a busca manual pelos dois bloqueios duros do check 1 e do check 2, no arquivo inteiro.

---

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| A régua pós-isca que aquece o lead até o convite, com WhatsApp e Direct no meio | **soft-funil-nutricao** | escrevo só o braço de e-mail, sem a ramificação por canal |
| A sequência de carrinho de um lançamento com evento e data | **soft-launch** | escrevo os e-mails de abertura e fechamento sem a mecânica do evento |
| Mensagem de dentro do webinar, lembrete de sala, pós por percentual assistido | **soft-webinar** | escrevo os 3 lembretes com o marco parametrizado |
| Prospecção fria pra quem nunca ouviu falar do dono | **soft-vendas-outreach** | não faço. E-mail frio pra lista comprada queima o domínio |
| Carta de vendas ou roteiro de VSL | **soft-funil-carta** | não faço. O CTA do e-mail aponta pra ela |
| Página de captura, de obrigado, de vendas | **soft-funil-landing** | escrevo só o texto do bloco, sem a arquitetura de página |
| Só o assunto, o gancho isolado | **soft-conteudo-headlines** | escrevo as 2 a 3 opções de assunto dentro da sequência |
| Posicionamento, avatar, oferta, prova | **soft-plano-posicionamento** | uso a entrevista curta de 6 perguntas da Ação 1 |
| A leitura do número depois que a campanha rodou | **soft-negocio-metricas** | comparo o resultado com a tabela de metas da Ação 4 |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/tipos-e-cadencias.md` · `references/anatomia-do-email.md` · `references/logica-de-fluxo.md` · `references/gate-linha-a-linha.md` · `scripts/lint_copy.py` (o anti-IA em código, rode no shell quando o ambiente permitir).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `sequencia-boas-vindas-assinatura.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

- **Passo 2 da checagem:** rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída; `exit` diferente de 0 reprova a entrega inteira.
