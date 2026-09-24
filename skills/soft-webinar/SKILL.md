---
name: soft-webinar
description: >-
  Entrega o webinar inteiro numa esteira só, com entrada por qualquer etapa: consultiva e pesquisa, oferta em stack, roteiro da aula slide a slide, páginas de cadastro, obrigado e checkout, mensagens com tags por percentual assistido, e o chat simulado ou moderado ao vivo. Use quando o pedido for: "monta meu webinar", "webinário", "masterclass", "aula que vende", "plano do webinar", "oferta do webinar", "roteiro do webinar", "slides do webinar", "páginas do webinar", "mensagens do webinar", "chat do webinar", "perpétuo ou ao vivo". NÃO use pra: o mini-webinar de 10 minutos do funil (soft-funil-miniwebinar); o lançamento com carrinho e evento (soft-launch); a régua pós-isca fora do webinar (soft-funil-nutricao); a isca (soft-funil-isca); renderizar deck e arte (soft-designer); o deck em PPTX (soft-apresentacao); carta, VSL ou landing avulsa (soft-funil-carta, soft-funil-landing); a venda 1:1 e a objeção (soft-vendas-closer). Leia e siga o fluxo inteiro do SKILL.md.
---

# O webinar inteiro, numa esteira só

Webinar que converte é um SISTEMA: plano consultivo, oferta desenhada, aula que ensina e vende, páginas que enchem a sala, mensagens que trazem de volta, chat que faz a sala existir. Esta skill conduz as 6 etapas num POP único; cada etapa entrega uma peça pronta e alimenta a seguinte.

**Pronto nesta skill.** A pasta de saída tem o arquivo da etapa pedida, limpo, e o bastidor à parte em `_notas-operador.md`. O relato abre com `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Antes de dizer pronto, rode `python3 scripts/lint_copy.py <arquivo>` em cada arquivo gravado, o relato incluso, e cole `<arquivo>: exit N`; exit diferente de 0 volta pra correção. Headline nunca em caixa alta. Motivo: nos casos medidos a conferência de títulos custou mais que a entrega, empurrou frase de teste pra dentro da peça e deixou passar a palavra-chave inventada.

**Bastidor fica fora da peça.** Caminho e nome de arquivo, nome de script, de etapa (Etapa 3) e de regra interna (lista-mestra, Seção 0b, Faca Soft, Mastercard), marco da oferta, furos, conferências, inventário, grep, lint e gate vão pra `_notas-operador.md`, nunca pro roteiro, a oferta ou as mensagens. Motivo: o dono recebe a peça pra publicar e, nos casos medidos, teve de apagar o bastidor.

**Nome próprio só o que o dono deu.** Mecanismo, passo, condição, bônus e produto levam o nome do insumo. Sem nome do dono, o passo é descrito pelo que faz, sem nome próprio, e a pergunta vai pro `_notas-operador.md`. Anti-padrão: «as 4 condições», nome que o dono nunca disse e subiu pra tela como se fosse dele.

**Teste do nicho, numa linha.** Troque o substantivo do nicho no nome do mecanismo (sem nome, na promessa) e escreva nas notas do operador `mecanismo: <nome> | trocado: <outro mercado> | sobrevive? sim/não`. Sobreviveu, o nome ainda é genérico: leve a troca ao dono como pergunta. Título que vai ao público (slide, assunto, página) segue `shared-references/crivo/07-regua-de-titulos.md` (a régua de escrita do título; o script, a pasta `conferencia/` e o inventário que ela descreve não valem nesta skill); cabeçalho de documento interno só diz o que a seção contém. Anti-padrão: afirmar no título uma tese que o dono não deu.

**Nome de persona é como a pessoa se identifica, e inicial de sobrenome denuncia a máquina.** Personas como `Adriana V.`, `Beatriz S.` em sequência quase alfabética são fabricadas. Rode `cut -d, -f1 <csv> | sort -u | grep -c ' [A-Z]\.$'` e cole a saída: acima de zero reprova.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra a saída resumida das 6 etapas num caso fictício de nicho neutro, do doc-mãe ao chat.

**SEM PORTEIRO (lei do dono).** Qualquer pessoa usa, em qualquer estágio; nada aqui exige nascer de outro processo. A régua de maturidade é no máximo um **aviso consultivo de 1 linha** ("validar barato antes costuma render mais; dá pra seguir mesmo assim"), NUNCA um bloqueio. **Perpétuo vs ao vivo é PARÂMETRO**, não decisão dramática: pergunta, anota, calibra o que muda (pré-início, link, escassez, chat), segue.

**As 6 leis** (`shared-references/operacao-padrao.md` Seção 0), as duras: (5) **marca `[A CONFIRMAR]`, JAMAIS inventa** número, case, fala ou nome; (6) **tabelas e listas, nunca paredão de prosa**. **Processo:** etapas na ordem quando o pedido é o webinar inteiro, **uma peça por vez, STOP pro OK**, gate da etapa **por dentro** (a tabela nunca sai), saída limpa em `.md`. Anti-IA HARD em tudo: rode `python3 scripts/lint_copy.py <arquivo>` no shell quando o ambiente permitir; senão, CTRL+F do travessão e do verbo-freio banido (a família que a régua anti-voz proíbe). Conferência de voz (sim ou não): a peça usa as expressões do dono que o insumo traz (vocativo, bordão, jeito de pedir)? E alguma frase, bordão, beat ou oferta desta entrega veio de outro dono (o autor do corpus, o GA, exemplo de referência: «te vejo do outro lado», «gente pior vendendo mais», presente pra quem fica)? Sim na segunda reprova.

**Furo nunca vira frase da peça.** Marcador `[A CONFIRMAR: x]` só entra em posição de campo (link, data, valor, telefone), no fim da linha. Slide ou mensagem que depende de um dado inexistente sai da peça e vai pro `_notas-operador.md`. Anti-padrão: escrever na tela uma frase sobre o furo («o depoimento desta tela fica pendente»). Motivo: a frase sobe junto com a peça e o lead lê o bastidor.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real vinda de mensagem privada, caixa de entrada ou call só entra em copy pública com a linha `autorizado por <dono> em <data>` no próprio insumo. Sem ela: anonimiza (inicial do nome, ou "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** **A classificação vale pra FALA, não só pro nome:** frase literal de call ou caixa de entrada continua conversa privada mesmo sem nome. Nas notas do operador, liste cada fala de terceiro na forma `<fala literal> | origem: <arquivo:linha> | classe: prova declarada ou conversa privada | como aparece: <"uma aluna", "alguém que me procurou">`. Conversa privada com lead em negociação só entra como "alguém que me procurou"; "uma aluna", "uma cliente" e "antes de entrar" afirmam a compra e reprovam. Feche com `falas de terceiro na peça: N · de conversa privada apresentadas como aluna: 0`. **A checagem é COMANDO, nunca memória** (`shared-references/crivo/08-consentimento.md`): (1) extraia os primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` por nome, no arquivo INTEIRO (configuração, filtros e checklists inclusos); (3) cole a saída dos dois e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. Nome sem a linha de autorização apontada por `<arquivo:linha>` reprova; contagem sem a saída colada não conta. **Vale igual pro ELENCO SIMULADO** (a lead em negociação não pode se ver comentando): rode o grep sobre a planilha entregue e feche com `nomes nos insumos privados: N · colisões no elenco: 0`, com a saída colada.

**Palavra-chave de CTA não se inventa, e a grafia é literal.** Antes de escrever qualquer CTA que peça uma palavra ("manda X no Direct", "comenta Y", "envia Z no WhatsApp"), procure a palavra nos insumos do dono (transcrição, peça pronta, mensagem, site) e cole `palavra-chave: <literal> | origem: <arquivo:linha>`. Use a grafia EXATA, sem espaço a mais nem a menos: uma palavra com espaço é outra palavra para quem digita e para a automação que responde, e a lead cai em lugar nenhum. **Sem origem no disco, é PROIBIDO escolher uma:** escreva o CTA na versão que dispensa a palavra ("me chama no Direct e eu te mando") e leve a pergunta ao handoff. Marcar a incerteza no relato e publicar a palavra assim mesmo reprova, porque o dono publica sem perceber. Anti-padrão: frase que garante resultado («quem aplica tem resultado», «em semanas», «a conta fecha numa venda só») sai sempre.

**Prazo, escassez, presença e replay só com o motivo no insumo.** Frase de prazo ou escassez («só hoje», «hoje, nesta sala», «vale pra quem entra nesta sessão», «até o fim desta aula», «último dia») entra na tela, na fala ou na mensagem só quando o dono declara o motivo e o prazo. Sem isso a frase não entra e vira pergunta em `_notas-operador.md`. No perpétuo gravado, nunca prometa presença ao vivo («vou ficar pra tirar dúvida», «já tem gente entrando») nem política de replay que o dono não deu. Frequência sem fonte («a maioria», «o mais comum»), presente pra quem fica e autor externo como prova seguem a mesma regra.

**Conferência de fonte, mecânica (o fecho de TODA etapa).** Antes de todo STOP, rode `python3 scripts/conferir_fontes.py --entrega <arquivos da etapa> --insumo <arquivos do dono>` (sem insumo, `--insumo` vazio; a régua de canal passa com `--aceitar 3000`). Cada linha `SEM FONTE` ou `REVISAR FORA DE NOTA` sai da peça ou vai pro `_notas-operador.md` como pergunta ao dono; rode de novo até o código 0 e cole a saída no `_notas-operador.md`. Número de pesquisa web nunca entra na peça sem o dono confirmar: vai pro plano como pergunta. Motivo: invenção é a falha número 1 medida, e regra em prosa não segurou.

**Conferência do insumo (sim ou não, no relato).** A prova, o preço, a parcela, a garantia, os bônus e os casos que o dono deu estão na peça, ou o relato diz por que ficaram fora? Caso que o dono lista como case ou prova é prova declarada e entra; a regra de autorização acima vale pra conversa privada. Motivo: nos casos medidos a garantia e os bônus sumiram das mensagens, e três cases do insumo ficaram fora da aula.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Nome de terceiro sem origem apontada (linha do insumo ou comando) reprova a entrega inteira.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a oferta e o público e eu monto a etapa). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pra construção com o que o dono colou. Se faltar um insumo que a etapa não vive sem (a promessa, a oferta, a prova externa), pergunta AQUELE insumo e segue, sem repetir a consultiva inteira. A entrada por qualquer etapa continua valendo.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a etapa consultiva com o dono, uma pergunta de cada vez, e monta o webinar com o que ele for dando.

A pergunta do modo é UMA por etapa. As outras três partes acontecem nas etapas abaixo:

- **Ensina enquanto faz:** em cada escolha estrutural (a promessa única, o nome do mecanismo, o desenho da stack, a sequência da aula) escreve UMA linha do porquê.
- **Puxa o material bruto:** quando a resposta vier rasa ("ensino o que sei", "meu público em geral"), não segue com o genérico. Pede o concreto que só o dono tem: um caso real de aluno com número e prazo, a frase que o público usa pra descrever a dor, a prova externa que sustenta a promessa.
- **Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer outra promessa? a oferta com outra ancoragem? o roteiro mais enxuto? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na etapa N

Leia o pedido, ache a linha, entre DIRETO naquela etapa. Não obrigue ninguém a passar pelas anteriores.

| O dono pediu | Entra na etapa |
|---|---|
| "o que vender", "vale a pena fazer webinar", "plano do webinar", "entender o negócio", "perpétuo ou ao vivo", "meu webinar não converte" (auditoria) | **1 · CONSULTIVA** |
| "desenha a oferta", "stack", "bônus", "quanto cobrar", "preço", "garantia", "ancoragem", "escassez" | **2 · OFERTA** |
| "roteiro", "aula", "script", "slides", "conteúdo da aula", "objeções", "Q&A", "quantos slides", "gravar o perpétuo" | **3 · AULA** |
| "pitch", "fechamento", "apresenta a oferta na aula", oferta pedida junto de roteiro ou Q&A | **3 · AULA**, só os slides da Ação (a Etapa 2 só quando o pedido é desenhar ou precificar) |
| "página de cadastro", "página de captura", "página de obrigado", "checkout", "as páginas do webinar" | **4 · PÁGINAS** |
| "e-mails", "WhatsApp", "sequência", "lembretes", "recuperação", "tags", "CRM", "quem não veio", "replay" | **5 · MENSAGENS** |
| "chat simulado", "comentários", "planilha de chat", "import da plataforma", "moderar o chat ao vivo" | **6 · CHAT** |
| **"webinar inteiro", "o pacote", "do zero ao ar", "quero fazer um webinar"** | **1 a 6, na ordem, com STOP em cada, só com o insumo mínimo** |
| **qualquer pedido SEM o insumo mínimo** (abaixo) | **só 1 · CONSULTIVA: o plano com as perguntas, e PARA** |

**Insumo mínimo, sem exceção.** É o que a Etapa 2 exige, dito pelo dono: o que a pessoa recebe, o preço, a promessa e quem compra. Sem ele, nenhuma etapa depois da 1 roda, nem quando o pedido é o webinar inteiro: a entrega é o plano da Etapa 1 com as perguntas, e a skill PARA até a resposta. Não é porteiro de maturidade, é falta de fato. Motivo: nos casos medidos, "quero fazer um webinar" sem insumo virou 8 peças com número, escassez e compra inventados.

Pedido ambíguo ("me ajuda com o webinar", "olha esse webinar aqui"): pergunte UMA coisa só, qual peça está faltando, mostre a tabela acima como cardápio e siga pela resposta.

## Como ler cada etapa

Toda etapa abaixo traz o mesmo bloco fixo: **O que faz** · **Precisa de** (o insumo e de onde ele vem) · **Sem o insumo** (o caminho concreto quando não existe) · **Entrega** (arquivo e formato) · **Leia primeiro** (obrigatória, 1 ou 2) · **Profundidade** (o resto, opcional, só quando o caso pedir).

**O perfil do dono vem do banco do agente.** Onde qualquer etapa precisar de posicionamento, avatar, mecanismo, voz ou prova: **leia do perfil/brain do agente quando existir**; se não existir, faça a entrevista curta descrita no "Sem o insumo" da etapa e siga com o que faltar marcado `[A CONFIRMAR]`. Nunca invente, nunca pare por causa disso. Sem doc-mãe, a lista-mestra sai do insumo colado ou vira a primeira pergunta da etapa.

**Minuto da oferta (vale nas Etapas 3, 5 e 6).** Sem minuto medido, use 75% da duração da aula e escreva `minuto da oferta: MM (estimativa: 75% de NN min)`. Nunca deixe o marco pendente, porque lembrete, tag e chat dependem dele.

---

## Etapa 1 · CONSULTIVA (o plano nasce COM o dono)

**O que faz:** traça o plano do webinar junto com o dono e fecha o doc-mãe de onde todas as outras etapas nascem.

**Precisa de:** o posicionamento inteiro (cliente, dor, promessa, mecanismo, oferta, prova), do perfil/brain do agente quando existir · pesquisa do mercado (concorrentes, promessas do nicho, preço praticado, linguagem real do público), busque na web se o ambiente tiver acesso ou peça o material ao dono · as respostas da entrevista de 11 blocos, sempre perguntadas ao dono.

**Sem o insumo:** entrevista curta de 6 perguntas aqui mesmo, uma por vez, sobre cliente, dor, promessa, mecanismo, oferta e prova; o que sobrar vira `[A CONFIRMAR]` no doc e o resto segue. Sem acesso à web, a pesquisa de mercado vira uma pergunta única ao dono: "me manda 3 concorrentes e o preço que eles praticam".

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `01-plano-webinar.md`, com as Seções 0 a 9 preenchidas, tabelas e listas, `[A CONFIRMAR]` em todo furo. Fecho: conferência de fonte. **STOP.** Sem insumo pra mais da metade das seções, a entrega é só a lista de perguntas ao dono, feitas uma por vez, com a das objeções entre as três primeiras. Motivo: documento feito de furo não ajuda o dono a responder.

**Leia primeiro:** `entrevista-intake.md` (INTEIRO, antes de perguntar qualquer coisa) · `montagem-secoes-0-9.md` (a forma do doc-mãe).

**Profundidade:** `intake-consultivo.md` (regras de condução) · `arsenal-vantagens-webinar.md` (o especialista que duvida) · `escolha-carta-mt-webinario.md` (a decisória Carta × MT × Webinar) · `analise-webinario-existente.md` (Modo B: audita um webinar que já existe, sem reescrever do zero) · `fundamentos-pre-roteiro.md` · `premissas-e-guarda-corpos.md` · `esqueleto-universal-e-discernimento.md`.

**Conduza a ENTREVISTA de 11 blocos** um bloco por vez, ecoando e confirmando: FILTRO (promessa=título, Grande Dominó, desejo/medo nº1) · avatar+CONSCIÊNCIA+formato · autoridade · problema/armadilhas/objeções · mecanismo com origem · as contas · módulos · oferta · prova · modelagem · logística. **A resposta de consciência do bloco 2 é a que decide o PESO das fases da aula na Etapa 3.**

**Lista-mestra de objeções (o fio do webinar).** De 5 a 8 objeções, na fala do público, cada uma com o medo por baixo e o tipo: de mecanismo (a aula derruba) ou de execução (bônus ou garantia matam). Fonte, nesta ordem: fala do público no insumo, briefing do dono, pesquisa; sem nenhuma, pergunte «quais são as desculpas que você mais ouve antes de alguém comprar?». Mais de 8: fique com as que mais aparecem. Toda etapa seguinte puxa desta lista. Motivo: lista espalhada vira três listas que não conversam. O formato da lista e a tradução objeção dita contra medo por baixo estão em `shared-references/venda-fladlien/objecoes.md`; a lista mora na Seção 0b do doc-mãe (`montagem-secoes-0-9.md`).

---

## Etapa 2 · OFERTA (o desenho, antes da encenação)

**O que faz:** monta a oferta como stack rica, com ancoragem, garantia, preço e canal de fechamento definidos.

**Precisa de:** o doc-mãe da Etapa 1 (promessa, avatar, mecanismo, módulos, prova, faixa de preço do nicho) · a lista do que o dono realmente entrega e do que ele já tem de prateleira, perguntada a ele.

**Sem o insumo:** entrevista curta de 5 perguntas: o que a pessoa recebe · quanto tempo leva pra ter o resultado · o que você já tem pronto que dá pra somar · qual o preço que o mercado pratica · quanto você já cobrou por isso. Com essas 5 dá pra montar a stack inteira; o resto vira `[A CONFIRMAR]`.

**Entrega:** `02-oferta.md`, a stack em tabela (item · o que é · tripartição · valor declarado), a soma riscada, o preço, as camadas dos N primeiros (só com o limite do dono), a garantia e o canal. Fecho: conferência de fonte. **STOP.**

**Leia primeiro:** `oferta-mapa.md` (o índice-mestre da etapa, abra ele antes de tudo) · `stack-de-oferta-e-bonus.md`.

**Profundidade:** `desenho-e-empacotamento-da-oferta.md` · `ancoragem-e-fechamento.md` · `gate-plano.md` (o gate da etapa, roda por dentro) · `exemplos-por-bloco/09-oferta-stack.md`, `10-ancoragem-preco.md`, `11-garantia.md` · `shared-references/venda-fladlien/componentes-da-oferta.md` (as 5 partes da oferta, bônus com função, risco em double bind, escassez com motivo; a ordem de preço continua a desta skill).

**O que a etapa monta:** **stack na TRIPARTIÇÃO** (módulos × cursos-prateleira com preço checável × bônus) · **bônus-âncora MAIOR que o produto** · **N primeiros em CAMADAS** (só com o limite do dono, com a REDE) · **2 moedas separadas** (desconto × bônus dos primeiros) · **soma riscada** · **garantia pelo cardápio** · **ancoragem em degraus até o valor por dia**: «R$[parcela] ÷ 30 = R$[valor] por dia, menos que [gasto de todo dia do avatar, tirado do insumo ou perguntado ao dono]», com o objeto fotografado; o objeto do exemplo da referência (Coca, iFood) nunca vai pra peça de outro dono · **régua de preço por faixa (497/997/1997/2997+)** · **canal pela régua de ~R$3.000**: até ela fecha no checkout, no próprio webinar; acima fecha na call 1:1 com INVERSÃO DE PODER (o lead é quem está sendo avaliado).

A régua de ~R$3.000 é o padrão do método (confirmado pelo dono do método em 23/09); se o dono declarou outro número no insumo, vale o dele. Conferência com a conta escrita: `preço R$X · régua R$Y (padrão ou do dono) · X até Y? sim, checkout; não, call`. Motivo: nos casos medidos uma entrega inverteu a conta e mandou o pós inteiro pra call.

O nome que o dono dá aos itens manda sobre a tripartição: se ele chama de bônus, a peça chama de bônus (o nome do item entre aspas quando o lint acusar), e classe sem item no insumo sai da tabela. Cada bônus aparece na tela com a objeção que mata ao lado («[bônus]: pra quem pensa [objeção]»), e o que mata a objeção de maior peso fica pro fechamento. Motivo: bônus sem objeção vira lista de nomes, e lista não muda decisão.

Escassez segue a regra do prazo (topo): o motivo confirmado (vagas da turma, capacidade de atendimento, prazo real de fechamento) vai na tela junto com o número. Motivo: escassez sem motivo vira objeção.

---

## Etapa 3 · AULA (o roteiro slide a slide)

> **CONTRATO DURO DO OUTPUT: a aula sai SLIDE A SLIDE, e cada slide tem TÍTULO + OBJETIVO + CONTEÚDO (a tela, em frases completas) + FALTA (fora da tela, só quando existe: o dado que o dono precisa dar) + NOTAS (fora da tela): FALA (2 ou 3 frases que o apresentador diz) e TRANSIÇÃO (a frase que leva ao slide seguinte).** Nunca parágrafo-teleprompter na tela. Onde as references falarem em "NOTA/copy falada", é o campo NOTAS deste contrato; onde disserem que a nota fica fora da entrega, vale este contrato.

**O que faz:** escreve a aula inteira, de trás pra frente a partir da oferta, no arco atenção → problema → solução → decisão, e emite o timestamp da oferta.

**Precisa de:** a oferta fechada da Etapa 2 (é dela que o roteiro nasce de trás pra frente) · o nível de CONSCIÊNCIA do público, do doc-mãe da Etapa 1, que decide o peso de cada fase · o mecanismo nomeado e a prova, do perfil/brain do agente ou do doc-mãe.

**Sem o insumo:** entrevista curta de 4 perguntas: o que você vende e por quanto · quem assiste e o quanto essa pessoa já sabe do problema · qual é o seu mecanismo e como ele nasceu · qual prova você pode mostrar na tela. Sem a consciência declarada, assuma MÉDIA, mantenha Mecanismo e Ação perto de 70% e diga ao dono em 1 linha qual premissa você assumiu.

**Entrega:** `03-roteiro-aula.md`, slide a slide no contrato duro, e o **TIMESTAMP DA OFERTA** (minuto em que o link abre + marcos de retenção) em `_notas-operador.md`, nunca no roteiro. Esse timestamp é o elo que as Etapas 5 e 6 consomem. Fecho: conferência de fonte. **STOP.** Depois do pitch vem o Q&A, escrito: uma resposta por objeção da lista-mestra, neste molde: «Faz sentido pensar [a objeção, na fala da pessoa]. O que pesa aqui é [o resultado que ela quer]. Se [a palavra dela] estiver resolvido, o que te impede de [a ação do CTA do dono: comprar, se candidatar, agendar] agora?», com a pergunta final variando de uma resposta pra outra. Ao vivo, agrupe as perguntas parecidas do chat, comece por «o que estou ouvindo é [reformulação]» e siga até a lista acabar. Motivo: resposta que termina em encorajamento deixa a pessoa no talvez; a que termina em pergunta pede a decisão.

**Leia primeiro:** `estrutura-real-webinar.md` (fonte-da-verdade, INTEIRA) · `tela-granularidade-e-bloco.md` (1 slide = 1 assunto, e a regra da tela auto-explicativa no bloco do topo) · no Q&A e no pitch, `shared-references/venda-fladlien/objecoes.md` e `fechamentos.md` (use só o que vale pra formato de grupo) · o arquivo do caso do autor (no perfil dele, fora da skill) só quando o insumo diz que o dono é o autor do corpus; pra qualquer outro dono, nem abrir, e nenhum beat, bordão ou presente de lá vira molde.

**Profundidade:** `arco-adma-e-reguas.md` · `padroes-de-profundidade.md` (**os 12 não-negociáveis**) · `mecanismo-objecoes-e-qea.md` + `motor-3-viradas.md` + `frameworks-proprietarios.md` (mecanismo na sequência real, objeções nos 4 níveis, Q&A que força decisão) · `beats-e-arquetipos.md` + `template-72-slides.md` (beats e esqueleto) · `oferta-stack.md` + `falas-prontas-por-bloco.md` (a oferta encenada) · `estrutura-webinario-aida.md` · `fladlien-modelo.md` · `gravacao-energia-ao-vivo.md` + `gravacao-do-perpetuo.md` · `passe-adversarial.md` · `gate-aula.md` · `exemplos-por-bloco/` (00 a 14).

**Peso das fases:** Mecanismo e Ação ficam perto de 70% da aula (faixa de referência do webinar real do autor, não número rígido); a consciência do público decide quanto do resto vai pra Atenção e pra Diagnóstico (baixa puxa pro Diagnóstico, altíssima pro Mecanismo), a ordem é lei e o fechamento nunca encurta. Cada um dos 3 passos do Mecanismo derruba uma objeção da lista e segue o molde: nome · por que importa · o que fazer (o quê e o porquê, sem o passo a passo executável que o produto vende) · o que acontece (na primeira vez, com o tempo, o obstáculo provável). Contraste: fraco, «o método organiza a receita»; forte, o mesmo passo demonstrado com o Caso A contra o Caso B, em números marcados como fictícios. Motivo: mecanismo só afirmado não ensina, e aula que não ensina não prova a promessa.

Abertura: a promessa traz o resultado medido que o insumo tem (quanto, em quanto tempo, de quem) e as três desculpas nomeadas; sem número no insumo, promessa sem número e nota ao dono. O recap do Mecanismo confere a lista-mestra uma por uma («[objeção]: resolvida no passo N, sim?»). Motivo: nos casos medidos a abertura prometeu sem medida e o recap nunca conferiu a lista.

Pré-início: um case do insumo por objeção da lista, na ordem dela, e o melhor case guardado pro fechamento; case que não coube no pré-início vai pra prova do Mecanismo. Case de cliente de serviço ou consultoria conta como prova, dito como o que é. Sem case autorizado, o pré-início vira preparação (cronômetro, card de autoridade, uma pergunta na dor, o que anotar, o que ter à mão, qual número trazer), nunca um espaço vazio de depoimento nem depoimento inventado. Motivo: prova que o dono deu e ficou fora é venda perdida, e slot vazio sobe pra tela como pendência.

Conferência de tela (sim ou não): cada slide carrega uma ideia e se lê em 3 segundos, e o único slide denso é o da oferta (pilha, total, prazo, link), com um CTA só? Cada bônus diz a objeção que mata? Conferência do fio (sim ou não): alguma objeção da lista ficou sem passo, bônus, resposta ou mensagem?

Antes de entregar, **PASSE ADVERSARIAL obrigatório** (`passe-adversarial.md`): o crivo do FILTRO slide a slide, o leigo cético, o checklist duro.

**Deck:** a skill entrega o roteiro em texto e não renderiza. Pedido de deck: `scripts/deck_gen.py` gera a BASE (um slide por entrada, cor e marca da config `DECK_*`). **`references/design-persuasivo-slides.md` é a régua de DESIGN de todo slide**, com as 4 checagens no `gate-aula.md`. Acabamento visual vai pra **soft-designer**.

---

## Etapa 4 · PÁGINAS (cadastro · obrigado · checkout)

**O que faz:** escreve as 3 páginas do webinar, uma por vez, cada uma com UMA função e UM objetivo.

**Precisa de:** a promessa e o título do webinar, do doc-mãe da Etapa 1 · a oferta e o preço, da Etapa 2 (o checkout precisa dos dois) · a data/horário e o modo (perpétuo ou ao vivo), perguntados ao dono · a prova e a bio, do perfil/brain do agente.

**Sem o insumo:** entrevista curta de 4 perguntas: qual a promessa da aula em uma frase · quem você quer na sala · o que você vende no fim e por quanto · quando ela acontece. Com o insumo mínimo e sem a stack fechada, escreva cadastro e obrigado agora e deixe o checkout pra depois, avisando em 1 linha.

**Entrega:** um `.md` por página (`04a-pagina-cadastro.md`, `04b-pagina-obrigado.md`, `04c-checkout.md`), bloco a bloco, na ordem em que aparecem na tela. Fecho: conferência de fonte. **STOP por página.**

**Leia primeiro:** `regua-leis-e-contrato.md` (na 1ª invocação da etapa, sempre) · `blocos-das-3-paginas.md`.

**Profundidade:** `intake-e-extracao.md` (P0/P0.5) · `principios-e-numeros.md` (P4 princípios · P5 espinha do perpétuo · P6 variante crua de link direto) · `gate-linha-a-linha.md` (P7, o gate) · `anti-patterns.md` · `_PAGINAS-BENCH.md` (bench real, marca-neutro: modela a premissa, nunca a paleta) · `paginas-cadastro-obrigado-checkout.md` (moldes verbatim).

**A função de cada página:** **Cadastro** captura e qualifica · **Obrigado** faz aparecer (o toque no WhatsApp aumenta muito o comparecimento; a ficha fecha no WhatsApp) · **Checkout ENXUTO** (cronômetro e N primeiros só com prazo e limite do dono + garantia + provas + bônus, NADA mais; acima da régua de canal (Etapa 2) o CTA vira call 1:1, nunca preço seco).

---

## Etapa 5 · MENSAGENS + a máquina de tags

**O que faz:** escreve as 3 réguas de mensagem (antes, durante, pós) e monta a máquina de tags por % assistido.

**Precisa de:** o **timestamp da oferta emitido na Etapa 3** (é ele que define os marcos de % assistido) · a promessa e a data, da Etapa 1 · a oferta, o prazo de fechamento e o canal (com a conta preço contra régua), da Etapa 2 · o canal que o dono usa de verdade (WhatsApp oficial, e-mail, ou os dois), perguntado a ele.

**Sem o insumo:** se o roteiro não existir e o timestamp não tiver sido emitido, pergunte UMA coisa: **"em que minuto entra a oferta?"**. Com esse número só, os marcos de % assistido saem inteiros. Se nem isso o dono souber, vale a regra do minuto da oferta (75%, em "Como ler cada etapa").

**Entrega:** `05-mensagens.md`, as 3 réguas peça por peça, cada mensagem com a tag e o roteamento colados embaixo, mais o **checklist técnico de subida** no fim. Fecho: conferência de fonte. **STOP por régua.**

**Leia primeiro:** `sequencias-email-whatsapp-pre-pos.md` (o molde de cada peça) · `perpetuo-vs-aovivo.md` (o que muda por modo) · no pós, `shared-references/venda-fladlien/follow-up.md` (motivo novo por mensagem, uma objeção por mensagem, a sessão só de dúvidas).

**Profundidade:** `perpetuo-mecanica.md` (a mecânica fina do perpétuo, sessões, offset, escassez por sessão).

**As 3 réguas:** **ANTES** (cadastro · 24h · 1h · link 5min) · **DURANTE** (2 toques, só WhatsApp) · **PÓS** (reconvite de quem não veio ou saiu cedo, sem pitch · nutrição de quem saiu antes da oferta, com o que faltou e a sessão nova · pra quem viu a oferta: resumo · prova · uma mensagem por objeção da lista-mestra, com o preço e a garantia do insumo e um motivo que as anteriores não trouxeram · a garantia, com o nome que o dono deu, pelo menos uma vez · preço e parcela · convite pra uma sessão ao vivo só de dúvidas, com as objeções no assunto · last call com o motivo real do prazo · fechamento · pergunta de 1 palavra + esteira semanal). Conferência: as três faixas (não veio, saiu antes da oferta, viu e não comprou) têm mensagem escrita por inteiro, não só a tag; cada mensagem traz motivo novo, e a garantia aparece? **A MÁQUINA DE TAGS é DESTA etapa** (nada de skill externa): define os marcos (não veio · 0-25 · 25-75 · viu a oferta · ficou até o fim · comprou), cria as tags e o roteamento (quente fecha, morno nutre, frio reconvida, cliente sai de tudo). **SEM replay é a recomendação padrão ao dono** (quem faltou vai pra próxima sessão), e a copy só fala de replay com a decisão dele no insumo; nota consultiva de 1 linha: abrir replay 24-48h é opção consciente, mais views a uma conversão menor. Lead que responde = quente, vai pro 1:1 (**soft-vendas-closer**). Conferência do fio (sim ou não): alguma objeção da lista ficou sem passo, bônus, resposta ou mensagem?

---

## Etapa 6 · CHAT (a sala viva)

**O que faz:** gera o chat simulado do perpétuo (planilha de import) ou o guia de moderação do chat ao vivo.

**Precisa de:** o roteiro e o **timestamp da oferta da Etapa 3** (o elo fecha aqui: eco↔respaldo, comando↔rajada, compra só DEPOIS do link) · o offset da sala de espera e o formato de colunas da plataforma do dono, perguntados a ele · os nomes e comandos que o apresentador ecoa na fala, do roteiro.

**Sem o insumo:** sem o roteiro, pergunte UMA coisa: **"em que minuto entra a oferta?"**, e mais o tamanho da aula. Com esses dois números a curva de densidade sai inteira e nenhuma compra cai antes do link. Sem o formato da plataforma declarado, use o default `username,message,minutes,seconds` e avise em 1 linha que ele precisa ser confirmado antes de subir.

**Entrega:** perpétuo, `06-chat-simulado.csv` no formato de import da plataforma, mais `06-chat-planejamento.md` com a tabela rica de auditoria. Ao vivo, `06-moderacao-chat.md`. Fecho: conferência de fonte. **STOP.**

**Exemplo numérico obrigatório no planejamento (a conta que os dois erros do campo produziram).** A primeira seção do `06-chat-planejamento.md` é a conta do tempo, escrita com os números deste pedido, no formato do exemplo abaixo. Sem essa conta escrita, com os quatro números, a etapa não fecha.

> Oferta no **minuto 42** do roteiro + sala de espera de **5 min** = link em **47:00 da sala** (o relógio que a plataforma toca). Preço, parcela, garantia e bônus só entram depois de 47:00. Aula declarada de 60 min de roteiro + offset de 5 min = teto de **65:00**: qualquer linha além disso não dispara e reprova.

**Como não errar o lado da conta.** O minuto que o dono dá é sempre do **roteiro** (o relógio do host falando), a não ser que ele diga "no vídeo" com todas as letras. Vídeo = roteiro + offset, e as três grandezas saem do mesmo lado: link, teto e todos os timestamps do CSV são tempo de **vídeo**. Antes da primeira linha, declare o lado: `O minuto 42 é do ROTEIRO (padrão) · offset 5:00 · link no vídeo em 47:00 · duração 60:00 de roteiro · teto no vídeo 65:00.` Se o dono disse "60 minutos de vídeo", a conta inverte e vai escrita igual: `duração 60:00 de VÍDEO · roteiro termina em 55:00 · teto no vídeo 60:00.` Premissa sem a conta escrita reprova a etapa.

**Conflito de eixo temporal, quando o disco e o dono discordam.** Com roteiro ou transcrição real no disco E outro tamanho de aula ou minuto de oferta declarado, os dois eixos valem: **o roteiro real manda no POSICIONAMENTO das reações** (cada reação casa com o beat que passou no vídeo que sobe) e **o número declarado manda na CONTA do link e do teto** (o que o dono controla no painel). Entregue lado a lado: `eixo do disco: duração <MM:SS> · oferta em <MM:SS> (fonte: <arquivo>) · eixo declarado: duração <MM:SS> · oferta em <MM:SS>`, e **pergunte ao dono qual vídeo vai subir antes de fechar**.

**Checagem verificável do tempo (releia o CSV, imprima os números).** Antes do STOP, reabra o `06-chat-simulado.csv` salvo e escreva no planejamento, nesta ordem:
1. `Link no ar em: MM:SS` (a conta acima, oferta + offset).
2. `3 primeiros timestamps que citam preço, parcela, garantia ou bônus: MM:SS, MM:SS, MM:SS` (relidos do arquivo; se houver menos de 3, escreva quantos existem). O primeiro deles tem que ser **maior** que o do link; se for menor, reprova e a linha volta pra depois do link.
3. `Teto: MM:SS (duração + offset) · maior timestamp do arquivo: MM:SS · linhas acima do teto: N.` **N maior que 0 reprova**, e a contagem vai escrita mesmo quando é zero: linha agendada além do fim do vídeo nunca dispara no import.

**As outras checagens executáveis do chat (relidas no CSV, escritas com número).** Antes do STOP, o `06-chat-planejamento.md` traz estas 4 linhas, cada uma com o valor medido no arquivo salvo:

1. **Sala de espera povoada:** `Entradas de vídeo entre 00:30 e <offset>: N` (piso 8, ou 4 quando o offset é menor que 2 minutos). Sala de espera vazia reprova.
2. **Rajada da transição pro pitch:** com roteiro, toda rajada nasce de um comando do roteiro. **Sem roteiro, você segue a espinha padrão de comandos do `_CHAT-MODELO.md` §5** e declara: `Modo sem roteiro. Comandos assumidos: <lista com timestamp>.` A rajada da transição pro pitch é obrigatória nos dois modos.
3. **Nada de rodízio determinístico, e sala com escada de micro-compromissos:** `Nomes com 3+ falas: N (mínimo 8, e piso de 20% do elenco) · com intervalo fixo: 0 · sequências de 3 nomes repetidas: 0 · nomes distintos: N (entre 15% e 40% das linhas).` Zero nome com 3 falas reprova: sem gente voltando ao chat não há escada de micro-compromissos, e é ela que prepara a sala pro pitch. A ficha de digitação por persona sai em `personas-digitacao.csv`. **Esses números saem do script, nunca da leitura:** rode `python3 scripts/auditar_chat.py 06-chat-simulado.csv --link MM:SS --teto MM:SS --offset MM:SS` e cole o comando e a saída literal no `06-chat-planejamento.md`. O script mede as contagens, a régua de elenco, a sala de espera, o teto e a ordem preço-depois-do-link, e mais duas que reprovam: `linhas com texto repetido de outra linha: N` (teto 10% das linhas, exceção declarada só pro coro que o host pediu) e `linhas com acento: N de M` (zero acento em mais de 500 caracteres reprova como `chat sem acentos`). Sem shell, escreva `não medido (sem shell)` em cada uma e marque a planilha como não auditada; declarar `0` sem a saída colada não vale.
4. **Elenco não toca a prova do dono:** `Nomes na prova do dono: <lista> · nomes do elenco: <lista> · coincidências de nome, primeiro nome, ou nome mais idade: 0.` Persona com nome, idade ou caso que tangencie pessoa real citada na prova é proibida, mesmo com o sobrenome trocado. **A colisão se testa por nome CONTIDO, nunca por string inteira**, e o nome composto é testado também pela primeira palavra: `Paula J.` no elenco colide com `Ana Paula, 40` na caixa de entrada. Rode `for n in $(cat nomes.txt); do grep -inE "(^|[^a-zà-ú])$n([^a-zà-ú]|$)" <peça>; done` e cole a saída literal. `colisões por nome contido: 0` sem essa saída colada não conta como feito.
5. **A sala É o avatar:** `Avatar declarado: <faixa etária, gênero predominante, dor de entrada, em 1 linha> · nomes coerentes com o gênero predominante: N de N · perfis derivados do avatar: N de N · perfis vindos de lista de exemplo: 0.` Sala majoritariamente masculina num webinar cujo avatar é feminino reprova, e perfil de profissão copiado de exemplo de referência reprova: os perfis saem da dor de entrada do avatar do dono, nunca de uma lista pronta.
6. **Coerência entre `username` e texto:** `linhas com nome no texto divergente do username: 0 · linhas com gênero gramatical divergente do nome: 0 · personas com o primeiro nome do host ou do dono: 0.` Persona que se apresenta com outro nome ("Anderson Reis" escrevendo "Camila aqui de SP") e nome masculino escrevendo no feminino aparecem na tela do lead e reprovam a planilha.

**A auditoria só existe relida**, e fecha com `Ordem conferida: as N linhas estão em ordem crescente de (minutes, seconds), sem duas no mesmo segundo.`

**Leia primeiro:** `_CHAT-MODELO.md` (a spec canônica, INTEIRO antes de gerar uma linha) · no modo ao vivo, `interacao-chat-ao-vivo.md`.

**Profundidade:** `simulador-comentarios-ao-vivo.md` (a doutrina longa: curva, honestidade, consistência) · `exemplos-por-bloco/14-interacao-chat.md`.

**Regra-mãe: simula a SALA, nunca a PROVA.** Comentário reproduz chegada, dúvida, reação, "eu quero", "comprei agora". Nunca inventa resultado de produto, número de vaga falso, preço, garantia, bônus ou meio de pagamento; sem oferta confirmada no insumo, nenhuma linha de compra. Tempo do vídeo = minuto do roteiro + offset da sala de espera. Gate do Crivo por dentro: todo comentário é copy que o lead LÊ. As dúvidas do chat simulado saem da lista-mestra, na fala do público.

---

## When NOT to use

Em toda rota abaixo: se a skill não estiver instalada, faço aqui em modo reduzido.

Render fino do deck / arte / PNG / paleta → **soft-designer**. Carta / VSL / landing fora do webinar → **soft-funil-carta** / **soft-funil-landing**. Micro-aula / mini-webinar de funil → **soft-funil-miniwebinar**. Posicionamento / nomear método → **soft-plano-posicionamento**. Venda 1:1 / objeção ao vivo / fechamento → **soft-vendas-closer** (prospecção: **soft-vendas-sdr**). Anúncios → **soft-trafego-meta**. Headline isolada → **soft-conteudo-headlines**. Conteúdo de feed → **soft-conteudo-***. "Por onde começo" → **soft-leon**.

## Transversais

`shared-references/` (operação-padrão, crivo/, filtro-anti-ia/, filtro-mobile-first/, adaptação semântica, dicionário conversacional, venda-fladlien/) · `scripts/lint_copy.py` (anti-IA em código, rode no shell quando o ambiente permitir) · `references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta).

---

## ⛔ REGRA DA TELA (02/09/2026, vale na Etapa 3 · AULA e manda sobre as references)

**O slide é auto-explicativo.** Quem lê só os slides, do primeiro ao último, entende o argumento inteiro da aula, na ordem, sem a fala; e quem vai apresentar olha o slide e já sabe o que falar, mesmo sem ensaio.

No campo CONTEÚDO: **toda linha da tela é frase completa, com verbo conjugado, terminando em ponto, interrogação ou exclamação, e entendida sem depender do slide anterior nem da fala.** Rótulo curto (nome de fase, etapa de fluxo, nome de campo) só existe colado a uma frase completa na mesma linha. Continua proibido o outro extremo, o parágrafo falado inteiro na tela.

Por extenso, com exemplo ruim e bom: `references/tela-granularidade-e-bloco.md`, bloco do topo. Onde `references/geracao-de-slides.md` pregar "slide mínimo", leia poucas frases completas, nunca palavras soltas.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
