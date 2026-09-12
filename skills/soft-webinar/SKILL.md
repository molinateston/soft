---
name: soft-webinar
description: >-
  Entrega o webinar inteiro numa esteira só, com entrada por qualquer etapa: consultiva e pesquisa, oferta em stack, roteiro da aula slide a slide, páginas de cadastro, obrigado e checkout, mensagens com tags por percentual assistido, e o chat simulado ou moderado ao vivo. Use quando o pedido for: "monta meu webinar", "webinário", "masterclass", "aula que vende", "plano do webinar", "oferta do webinar", "roteiro do webinar", "slides do webinar", "páginas do webinar", "mensagens do webinar", "chat do webinar", "perpétuo ou ao vivo". NÃO use pra: o mini-webinar de 10 minutos do funil (soft-funil-miniwebinar); o lançamento com carrinho e evento (soft-launch); a régua pós-isca fora do webinar (soft-funil-nutricao); a isca (soft-funil-isca); renderizar deck e arte (soft-designer); o deck em PPTX (soft-apresentacao); carta, VSL ou landing avulsa (soft-funil-carta, soft-funil-landing); a venda 1:1 e a objeção (soft-vendas-closer). Leia e siga o fluxo inteiro do SKILL.md.
---

# O webinar inteiro, numa esteira só

Webinar que converte é um SISTEMA: plano consultivo, oferta desenhada, aula que ensina e vende, páginas que enchem a sala, mensagens que trazem de volta, chat que faz a sala existir. Esta skill conduz as 6 etapas num POP único; cada etapa entrega uma peça pronta e alimenta a seguinte.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**A linha do mecanismo é saída obrigatória.** No `conferencia/checagem-titulos.md` desta entrega saem, sempre: `mecanismo do problema: <nome> | substantivo trocado: <original> → <outro mercado> | sobrevive à troca de nicho? sim/não` · `mecanismo da solução: <nome>` · `números não confirmados no perfil: N · publicados na peça: 0`. Falta de qualquer uma invalida a entrega, e a ausência da linha do mecanismo custa mais que as outras: sem ela ninguém sabe se o problema foi batizado ou só descrito.

**O teste do nicho trocado preenchido é gate.** Linha do teste com `<preencher>` no campo do substantivo ou do veredito conta como teste NÃO FEITO, e teste não feito reprova a entrega inteira. Cole `unidades no teste: N · preenchidas: N`, iguais. O script reprova `<preencher>` em qualquer arquivo da pasta. Some: o inventário sai do comando sobre a tabela, colado ao lado, e é um só; dois totais diferentes na mesma entrega reprovam antes da análise.

**Nome de persona é como a pessoa se identifica, e inicial de sobrenome denuncia a máquina.** Personas como `Adriana V.`, `Beatriz S.` em sequência quase alfabética são fabricadas. Rode `cut -d, -f1 <csv> | sort -u | grep -c ' [A-Z]\.$'` e cole a saída: acima de zero reprova.

**O título é uma afirmação, e o nome da seção desta skill nunca é o título da peça.** Todo cabeçalho do documento entregue afirma a decisão daquela seção. É proibido usar como cabeçalho o nome do passo desta skill (`Passo N`, `Etapa N`, `Bloco N`), o prefixo `Seção:` e o nome do artefato (`PUV`, `Racional`, `Equação de Valor`): esses são o andaime da execução, e o dono abre o documento pra saber o que foi decidido, nunca onde o texto mora. Errado, porque rotula: `# Plano de Posicionamento · Studio Base 40`, `## Passo 5 · a prescrição`, `## Seção: a conta do tempo`. Certo, porque afirma: `# 3 sessões de 25 minutos vencem outro recomeço`, `# 12 semanas: o ombro escolhe a carga`, `# A sala aquece antes da oferta, sem fabricar prova`. Cole uma linha por cabeçalho, `H2: <literal> · afirma algo que o dono pode discordar: sim/não`, e feche com `cabeçalhos que afirmam: N de N`. Menos da metade volta pro passo de escrita.

**`--exige` por etapa.** Rode `--conferir <pasta> --exige <lista>` com a linha da etapa entregue; arquivo ausente sai com exit 1 e `arquivo exigido pela ação ausente: <nome>`. Entregar 2 das 6 etapas num pedido de pacote é entrega incompleta, não escopo reduzido.

| Etapa | `--exige` |
|---|---|
| 1 CONSULTIVA | `01-plano-webinar.md` |
| 2 OFERTA | `02-oferta.md` |
| 3 AULA | `03-roteiro-aula.md` |
| 4 PÁGINAS | `04a-pagina-cadastro.md,04b-pagina-obrigado.md,04c-checkout.md` |
| 5 MENSAGENS | `05-mensagens.md` |
| 6 CHAT | `06-chat-simulado.csv,06-chat-planejamento.md` |


**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra a saída resumida das 6 etapas num caso fictício de nicho neutro (consultoria de organização financeira pra clínicas): o doc-mãe em 15 linhas, a oferta em stack, 6 slides no contrato duro, uma página, 3 mensagens com tag e 8 linhas de chat com timestamp. Ler os 180 linhas de lá antes da primeira pergunta economiza uma rodada inteira de retrabalho.

**SEM PORTEIRO (lei do dono).** Qualquer pessoa usa, em qualquer estágio; nada aqui exige nascer de outro processo. A régua de maturidade é no máximo um **aviso consultivo de 1 linha** ("validar barato antes costuma render mais; dá pra seguir mesmo assim"), NUNCA um bloqueio. **Perpétuo vs ao vivo é PARÂMETRO**, não decisão dramática: pergunta, anota, calibra o que muda (pré-início, link, escassez, chat), segue.

**As 6 leis** (`shared-references/operacao-padrao.md` Seção 0), as duras: (5) **marca `[A CONFIRMAR]`, JAMAIS inventa** número, case, fala ou nome; (6) **tabelas e listas, nunca paredão de prosa**. **Processo:** etapas na ordem quando o pedido é o webinar inteiro, **uma peça por vez, STOP pro OK**, gate da etapa **por dentro** (a tabela nunca sai), saída limpa em `.md`. Anti-IA HARD em tudo: rode `python3 scripts/lint_copy.py <arquivo>` no shell quando o ambiente permitir; senão, CTRL+F do travessão e do verbo-freio banido (a família que a régua anti-voz proíbe).

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com a lista fechada de contagens, uma por linha, exatamente nesta forma:
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

**Rótulo de seção não é título, e a coluna diz qual é qual.** Classifique cada título de seção e de slide como `rótulo` ou `tese`, numa coluna própria da checagem. Rótulo nomeia o assunto e não afirma nada (`Resumo`, `Introdução`, `O método`, `Perguntas`); tese afirma alguma coisa que o leitor pode discordar (`O que sobra quando você tira a pressa`). O título de seção e de slide é a primeira coisa que o leitor lê antes de decidir se continua, e um documento de rótulos não segura ninguém. Cole a coluna inteira, um por linha, na forma `<título> | rótulo ou tese`, e **todo `rótulo` volta pro passo de escrita** antes de a peça sair. Feche com `títulos de seção: N · em tese: N · rótulos restantes: 0`.


A contagem de molde de antítese sai do lint, nunca da cabeça, e vem acompanhada da coluna sim/não de TODOS os títulos do lote; a de teses distintas vem com a lista ordenada e comparada par a par. Nenhuma das linhas pode faltar, e linha declarada sem o que a régua exige ao lado não conta como feita.

**As contagens de R3, R4 e R5 são gates, não termômetros.** Quando `com inimigo ou inversão` ficar abaixo da metade do lote, `teses distintas` abaixo de 3, ou `em molde de antítese` acima de 1, a entrega **não sai**: os títulos reprovados voltam pro passo de escrita, são reescritos, e a checagem final mostra a contagem corrigida mais a linha `reescritos por contagem: N (<contagem que reprovou>)`. Declarar a contagem que reprova e publicar assim mesmo é o pior dos dois mundos, porque produz um documento que prova o próprio defeito e não o corrige: o dono lê `0 de 4` e não tem como saber que isso significa que a régua reprovou. **Nenhuma justificativa de tipo de peça vale aqui:** se o formato dispensa a inversão, a exceção mora escrita na receita do tipo, e a entrega cita a linha dessa receita. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** **A classificação vale para a FALA, não só para o nome:** anonimizar resolve a identidade e não resolve a origem, e uma frase literal vinda de call ou de caixa de entrada continua sendo conversa privada mesmo sem nome. Liste as falas atribuídas a terceiros na peça, uma por linha, na forma `<fala literal> | origem: <arquivo:linha> | classe: prova declarada ou conversa privada | como aparece na peça: <"uma aluna", "uma seguidora", "alguém que me procurou">`. Fala de conversa privada com pessoa em negociação aberta só entra como "alguém que me procurou" ou equivalente que não afirme compra; "uma aluna", "uma cliente" e "antes de entrar" afirmam a compra e reprovam. Feche com `falas de terceiro na peça: N · de conversa privada apresentadas como aluna: 0`. Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova. **A regra vale igual para ELENCO SIMULADO**, e a lista de nomes proibidos é a que o comando devolve, nunca a que você lembra: o risco maior não é citar a aluna do caso, é sortear pro elenco o primeiro nome de uma lead em negociação aberta que vai assistir à aula e se ver comentando na sala. Rode o grep sobre o arquivo entregue (a planilha de chat inclusa) e feche com `nomes nos insumos privados: N · colisões no elenco: 0`, com a saída colada.

**Palavra-chave de CTA não se inventa, e a grafia é literal.** Antes de escrever qualquer CTA que peça uma palavra ("manda X no Direct", "comenta Y", "envia Z no WhatsApp"), procure a palavra nos insumos do dono (transcrição, peça pronta, mensagem, site) e cole `palavra-chave: <literal> | origem: <arquivo:linha>`. Use a grafia EXATA, sem espaço a mais nem a menos: uma palavra com espaço é outra palavra para quem digita e para a automação que responde, e a lead cai em lugar nenhum. **Sem origem no disco, é PROIBIDO escolher uma:** escreva o CTA na versão que dispensa a palavra ("me chama no Direct e eu te mando") e leve a pergunta ao handoff. Marcar a incerteza no relato e publicar a palavra assim mesmo reprova, porque o dono publica sem perceber.

**Uso completo do que o dono deu (vale no gate de toda etapa desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar a etapa: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **O inventário varre o perfil do dono INTEIRO, não só os campos que esta entrega consumiu:** cada campo do perfil é uma linha, e campo com vários valores (paleta com 3 cores; oferta com preço, parcela, bônus e garantia) rende uma linha por valor. **Entrega cujo `Dados fornecidos: N` for menor que o número de campos do perfil recebido reprova sem análise de conteúdo.** Qualificar a linha ("relevantes ao objeto", "considerados para esta entrega") também reprova: o total é o total. **Onde a linha mora:** no arquivo que o dono lê. Quando a entrega é uma peça de copy publicável (headline, carrossel, slide, card, chat, roteiro, deck), a peça NÃO recebe a tabela: a tabela vai num arquivo irmão de handoff (`HANDOFF-<slug>.md`) e só a linha de fechamento fica na peça, no rodapé. Inventário só no relato de processo, sem a linha na entrega nem o handoff no disco, reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a oferta e o público e eu monto a etapa). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pra construção com o que o dono colou. Se faltar um insumo que a etapa não vive sem (a promessa, a oferta, a prova externa), pergunta AQUELE insumo e segue, sem repetir a consultiva inteira. A entrada por qualquer etapa continua valendo.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a etapa consultiva com o dono, uma pergunta de cada vez, e monta o webinar com o que ele for dando.

A pergunta do modo é UMA por etapa. As outras três partes acontecem nas etapas abaixo:

- **Ensina enquanto faz:** em cada escolha estrutural (a promessa única, o nome do mecanismo, o desenho da stack, a sequência da aula) escreve UMA linha do porquê. O dono lê a razão e aprende a jogada que vende.
- **Puxa o material bruto:** quando a resposta vier rasa ("ensino o que sei", "meu público em geral"), não segue com o genérico. Pede o concreto que só o dono tem: um caso real de aluno com número e prazo, a frase que o público usa pra descrever a dor, a prova externa que sustenta a promessa. Material bruto vira aula que converte; resposta rasa vira webinar que ninguém compra.
- **Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer outra promessa? a oferta com outra ancoragem? o roteiro mais enxuto? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na etapa N

Leia o pedido, ache a linha, entre DIRETO naquela etapa. Não obrigue ninguém a passar pelas anteriores.

| O dono pediu | Entra na etapa |
|---|---|
| "o que vender", "vale a pena fazer webinar", "plano do webinar", "entender o negócio", "perpétuo ou ao vivo", "meu webinar não converte" (auditoria) | **1 · CONSULTIVA** |
| "desenha a oferta", "stack", "bônus", "quanto cobrar", "preço", "garantia", "ancoragem", "escassez dos 15 primeiros" | **2 · OFERTA** |
| "roteiro", "aula", "script", "slides", "conteúdo da aula", "objeções", "Q&A", "quantos slides", "gravar o perpétuo" | **3 · AULA** |
| "página de cadastro", "página de captura", "página de obrigado", "checkout", "as páginas do webinar" | **4 · PÁGINAS** |
| "e-mails", "WhatsApp", "sequência", "lembretes", "recuperação", "tags", "CRM", "quem não veio", "replay" | **5 · MENSAGENS** |
| "chat simulado", "comentários", "planilha de chat", "import da plataforma", "moderar o chat ao vivo" | **6 · CHAT** |
| **"webinar inteiro", "o pacote", "do zero ao ar"** | **1 a 6, na ordem, com STOP em cada** |

Pedido ambíguo ("me ajuda com o webinar", "olha esse webinar aqui"): pergunte UMA coisa só, qual peça está faltando, mostre a tabela acima como cardápio e siga pela resposta.

## Como ler cada etapa

Toda etapa abaixo traz o mesmo bloco fixo: **O que faz** · **Precisa de** (o insumo e de onde ele vem) · **Sem o insumo** (o caminho concreto quando não existe) · **Entrega** (arquivo e formato) · **Leia primeiro** (obrigatória, 1 ou 2) · **Profundidade** (o resto, opcional, só quando o caso pedir).

**O perfil do dono vem do banco do agente.** Onde qualquer etapa precisar de posicionamento, avatar, mecanismo, voz ou prova: **leia do perfil/brain do agente quando existir**; se não existir, faça a entrevista curta descrita no "Sem o insumo" da etapa e siga com o que faltar marcado `[A CONFIRMAR]`. Nunca invente, nunca pare por causa disso.

---

## Etapa 1 · CONSULTIVA (o plano nasce COM o dono)

**O que faz:** traça o plano do webinar junto com o dono e fecha o doc-mãe de onde todas as outras etapas nascem.

**Precisa de:** o posicionamento inteiro (cliente, dor, promessa, mecanismo, oferta, prova), do perfil/brain do agente quando existir · pesquisa do mercado (concorrentes, promessas do nicho, preço praticado, linguagem real do público), busque na web se o ambiente tiver acesso ou peça o material ao dono · as respostas da entrevista de 11 blocos, sempre perguntadas ao dono.

**Sem o insumo:** entrevista curta de 6 perguntas aqui mesmo, uma por vez, sobre cliente, dor, promessa, mecanismo, oferta e prova; o que sobrar vira `[A CONFIRMAR]` no doc e o resto segue. Sem acesso à web, a pesquisa de mercado vira uma pergunta única ao dono: "me manda 3 concorrentes e o preço que eles praticam".

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `01-plano-webinar.md`, com as Seções 0 a 9 preenchidas, tabelas e listas, `[A CONFIRMAR]` em todo furo. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `entrevista-intake.md` (INTEIRO, antes de perguntar qualquer coisa) · `montagem-secoes-0-9.md` (a forma do doc-mãe).

**Profundidade:** `intake-consultivo.md` (regras de condução) · `arsenal-vantagens-webinar.md` (o especialista que duvida) · `escolha-carta-mt-webinario.md` (a decisória Carta × MT × Webinar) · `analise-webinario-existente.md` (Modo B: audita um webinar que já existe, sem reescrever do zero) · `fundamentos-pre-roteiro.md` · `premissas-e-guarda-corpos.md` · `esqueleto-universal-e-discernimento.md`.

**Conduza a ENTREVISTA de 11 blocos** um bloco por vez, ecoando e confirmando: FILTRO (promessa=título, Grande Dominó, desejo/medo nº1) · avatar+CONSCIÊNCIA+formato · autoridade · problema/armadilhas · mecanismo com origem · as contas · módulos · oferta · prova · modelagem · logística. **A resposta de consciência do bloco 2 é a que decide o PESO das fases da aula na Etapa 3.**

---

## Etapa 2 · OFERTA (o desenho, antes da encenação)

**O que faz:** monta a oferta como stack rica, com ancoragem, garantia, preço e canal de fechamento definidos.

**Precisa de:** o doc-mãe da Etapa 1 (promessa, avatar, mecanismo, módulos, prova, faixa de preço do nicho) · a lista do que o dono realmente entrega e do que ele já tem de prateleira, perguntada a ele.

**Sem o insumo:** entrevista curta de 5 perguntas: o que a pessoa recebe · quanto tempo leva pra ter o resultado · o que você já tem pronto que dá pra somar · qual o preço que o mercado pratica · quanto você já cobrou por isso. Com essas 5 dá pra montar a stack inteira; o resto vira `[A CONFIRMAR]`.

**Entrega:** `02-oferta.md`, a stack em tabela (item · o que é · tripartição · valor declarado), a soma riscada, o preço, as camadas dos 15 primeiros, a garantia e o canal. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `oferta-mapa.md` (o índice-mestre da etapa, abra ele antes de tudo) · `stack-de-oferta-e-bonus.md`.

**Profundidade:** `desenho-e-empacotamento-da-oferta.md` · `ancoragem-e-fechamento.md` · `gate-plano.md` (o gate da etapa, roda por dentro) · `exemplos-por-bloco/09-oferta-stack.md`, `10-ancoragem-preco.md`, `11-garantia.md`.

**O que a etapa monta:** **stack na TRIPARTIÇÃO** (módulos × cursos-prateleira com preço checável × bônus) · **bônus-âncora MAIOR que o produto** · **15-primeiros em CAMADAS** (turma/15/10, com a REDE) · **2 moedas separadas** (desconto × bônus dos primeiros) · **soma riscada** · **garantia pelo cardápio** · **ancoragem com re-ancoragem progressiva** · **régua de preço por faixa (497/997/1997/2997+)** · **canal: até ~3k fecha no checkout, acima de ~3k fecha na call 1:1 com INVERSÃO DE PODER** (o lead é quem está sendo avaliado).

---

## Etapa 3 · AULA (o roteiro slide a slide)

> **CONTRATO DURO DO OUTPUT: a aula sai SLIDE A SLIDE, e cada slide tem exatamente TÍTULO + OBJETIVO (qual beat do arco cumpre) + CONTEÚDO (o que o slide carrega: a lista, o número, a frase, a cena).** Nunca roteiro falado corrido, nunca texto pra ler em voz alta, nunca parágrafo-teleprompter. **Esta skill NÃO renderiza slides**: ela entrega o roteiro slide-a-slide pronto pra QUALQUER renderizador agir em cima. Onde as references falarem em "NOTA/copy falada", leia como material do apresentador/renderizador, fora do contrato desta entrega.

**O que faz:** escreve a aula inteira, de trás pra frente a partir da oferta, no arco atenção → problema → solução → decisão, e emite o timestamp da oferta.

**Precisa de:** a oferta fechada da Etapa 2 (é dela que o roteiro nasce de trás pra frente) · o nível de CONSCIÊNCIA do público, do doc-mãe da Etapa 1, que decide o peso de cada fase · o mecanismo nomeado e a prova, do perfil/brain do agente ou do doc-mãe.

**Sem o insumo:** entrevista curta de 4 perguntas: o que você vende e por quanto · quem assiste e o quanto essa pessoa já sabe do problema · qual é o seu mecanismo e como ele nasceu · qual prova você pode mostrar na tela. Sem a consciência declarada, assuma MÉDIA, escreva com o peso equilibrado e diga ao dono em 1 linha qual premissa você assumiu.

**Entrega:** `03-roteiro-aula.md`, slide a slide no contrato duro, com o **TIMESTAMP DA OFERTA** no fim (minuto do roteiro em que o link/carrinho abre + marcos de retenção). Esse timestamp é o elo que as Etapas 5 e 6 consomem. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `estrutura-real-webinar.md` (fonte-da-verdade, INTEIRA) · `tela-granularidade-e-bloco.md` (1 slide = 1 assunto, e a regra da tela auto-explicativa no bloco do topo).

**Profundidade:** `arco-adma-e-reguas.md` · `padroes-de-profundidade.md` (**os 12 não-negociáveis**) · `mecanismo-objecoes-e-qea.md` + `motor-3-viradas.md` + `frameworks-proprietarios.md` + `objection-annihilation.md` (mecanismo na sequência real, objeções nos 4 níveis, Q&A que força decisão) · `beats-e-arquetipos.md` + `template-72-slides.md` (beats e esqueleto) · `oferta-stack.md` + `falas-prontas-por-bloco.md` (a oferta encenada) · `estrutura-webinario-aida.md` · `fladlien-modelo.md` · `gravacao-energia-ao-vivo.md` + `gravacao-do-perpetuo.md` · `passe-adversarial.md` · `gate-aula.md` · `exemplos-por-bloco/` (00 a 14).

**SEM PROPORÇÃO FIXA: o peso de cada fase segue a CONSCIÊNCIA do público** (baixa = mais diagnóstico/problema; altíssima = mais solução/mecanismo); a ordem é lei, o fechamento nunca encurta. Pré-início de prova é obrigatório. Antes de entregar, **PASSE ADVERSARIAL obrigatório** (`passe-adversarial.md`): o crivo do FILTRO slide a slide, o leigo cético, o checklist duro.

**Nota de perpétuo (relato de operador, sem prova).** Antes de gravar o perpétuo, roda ao vivo de verdade algumas rodadas e documenta as objeções reais, que viram slide a cada rodada; grava só quando o ciclo esgotou. O conteúdo é espelho da oferta: cada "segredo" ensinado é, disfarçado, uma peça da oferta que vem no fim. E o Q&A é pré-arquitetado, com perguntas que quebram objeções específicas, tratado como peça de venda com o mesmo cuidado do pitch.

**Quando o script e o gerador de deck entram:** a skill entrega o roteiro em texto e para aí; ela não desenha nem exporta arte. Quando o dono quiser sair do roteiro pra um deck, `scripts/deck_gen.py` lê o roteiro slide a slide e gera a BASE do deck (um slide por entrada, título e conteúdo no lugar), e `SLIDE-MODELO-SCRIPT.md` mais `geracao-de-slides.md` dizem em que forma o roteiro precisa estar pro script conseguir ler. O script é marca-neutro: cor, fonte e marca vêm da config do dono (variáveis de ambiente `DECK_*`). O acabamento visual (paleta, arte, animação) sai daqui e vai pra **soft-designer**.

---

## Etapa 4 · PÁGINAS (cadastro · obrigado · checkout)

**O que faz:** escreve as 3 páginas do webinar, uma por vez, cada uma com UMA função e UM objetivo.

**Precisa de:** a promessa e o título do webinar, do doc-mãe da Etapa 1 · a oferta e o preço, da Etapa 2 (o checkout precisa dos dois) · a data/horário e o modo (perpétuo ou ao vivo), perguntados ao dono · a prova e a bio, do perfil/brain do agente.

**Sem o insumo:** entrevista curta de 4 perguntas: qual a promessa da aula em uma frase · quem você quer na sala · o que você vende no fim e por quanto · quando ela acontece. Sem a oferta fechada, escreva cadastro e obrigado agora e deixe o checkout pra depois, avisando em 1 linha.

**Entrega:** um `.md` por página (`04a-pagina-cadastro.md`, `04b-pagina-obrigado.md`, `04c-checkout.md`), bloco a bloco, na ordem em que aparecem na tela. **STOP por página.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `regua-leis-e-contrato.md` (na 1ª invocação da etapa, sempre) · `blocos-das-3-paginas.md`.

**Profundidade:** `intake-e-extracao.md` (P0/P0.5) · `principios-e-numeros.md` (P4 princípios · P5 espinha do perpétuo · P6 variante crua de link direto) · `gate-linha-a-linha.md` (P7, o gate) · `anti-patterns.md` · `_PAGINAS-BENCH.md` (bench real, marca-neutro: modela a premissa, nunca a paleta) · `paginas-cadastro-obrigado-checkout.md` (moldes verbatim).

**A função de cada página:** **Cadastro** captura e qualifica · **Obrigado** faz aparecer (o toque no WhatsApp aumenta muito o comparecimento; a ficha fecha no WhatsApp) · **Checkout ENXUTO** (cronômetro de 5min + 15-primeiros + garantia + provas + bônus, NADA mais; acima de ~3k o CTA vira call 1:1, nunca preço seco).

---

## Etapa 5 · MENSAGENS + a máquina de tags

**O que faz:** escreve as 3 réguas de mensagem (antes, durante, pós) e monta a máquina de tags por % assistido.

**Precisa de:** o **timestamp da oferta emitido na Etapa 3** (é ele que define os marcos de % assistido) · a promessa e a data, da Etapa 1 · a oferta e o prazo de fechamento, da Etapa 2 · o canal que o dono usa de verdade (WhatsApp oficial, e-mail, ou os dois), perguntado a ele.

**Sem o insumo:** se o roteiro não existir e o timestamp não tiver sido emitido, pergunte UMA coisa: **"em que minuto entra a oferta?"**. Com esse número só, os marcos de % assistido saem inteiros. Se nem isso o dono souber, use a proporção padrão (oferta a 75% da aula), escreva as réguas com o marco parametrizado e avise em 1 linha que o número precisa ser confirmado.

**Entrega:** `05-mensagens.md`, as 3 réguas peça por peça, cada mensagem com a tag e o roteamento colados embaixo, mais o **checklist técnico de subida** no fim. **STOP por régua.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `sequencias-email-whatsapp-pre-pos.md` (o molde de cada peça) · `perpetuo-vs-aovivo.md` (o que muda por modo).

**Profundidade:** `perpetuo-mecanica.md` (a mecânica fina do perpétuo, sessões, offset, escassez por sessão).

**As 3 réguas:** **ANTES** (cadastro · 24h · 1h · link 5min) · **DURANTE** (2 toques, só WhatsApp) · **PÓS** (resumo · prova · objeção · last call · fechamento · downsell/pergunta de 1 palavra + esteira semanal). **A MÁQUINA DE TAGS é DESTA etapa** (nada de skill externa): define os marcos (não veio · 0-25 · 25-75 · viu a oferta · ficou até o fim · comprou), cria as tags e o roteamento (quente fecha, morno nutre, frio reconvida, cliente sai de tudo). **SEM replay é o padrão** (quem faltou vai pra próxima sessão); nota consultiva de 1 linha: abrir replay 24-48h é opção consciente, mais views a uma conversão menor. Lead que responde = quente, vai pro 1:1 (**soft-vendas-closer**).

---

## Etapa 6 · CHAT (a sala viva)

**O que faz:** gera o chat simulado do perpétuo (planilha de import) ou o guia de moderação do chat ao vivo.

**Precisa de:** o roteiro e o **timestamp da oferta da Etapa 3** (o elo fecha aqui: eco↔respaldo, comando↔rajada, compra só DEPOIS do link) · o offset da sala de espera e o formato de colunas da plataforma do dono, perguntados a ele · os nomes e comandos que o apresentador ecoa na fala, do roteiro.

**Sem o insumo:** sem o roteiro, pergunte UMA coisa: **"em que minuto entra a oferta?"**, e mais o tamanho da aula. Com esses dois números a curva de densidade sai inteira e nenhuma compra cai antes do link. Sem o formato da plataforma declarado, use o default `username,message,minutes,seconds` e avise em 1 linha que ele precisa ser confirmado antes de subir.

**Entrega:** perpétuo, `06-chat-simulado.csv` no formato de import da plataforma, mais `06-chat-planejamento.md` com a tabela rica de auditoria. Ao vivo, `06-moderacao-chat.md`. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Exemplo numérico obrigatório no planejamento (a conta que os dois erros do campo produziram).** A primeira seção do `06-chat-planejamento.md` é a conta do tempo, escrita com os números deste pedido, no formato do exemplo abaixo. Sem essa conta escrita, com os quatro números, a etapa não fecha.

> Oferta no **minuto 42** do roteiro + sala de espera de **5 min** = link em **47:00 da sala** (o relógio que a plataforma toca). Preço, parcela, garantia e bônus só entram depois de 47:00. Aula declarada de 60 min de roteiro + offset de 5 min = teto de **65:00**: qualquer linha além disso não dispara e reprova.

**Como não errar o lado da conta.** O minuto que o dono dá é sempre do **roteiro** (o relógio do host falando), a não ser que ele diga "no vídeo" com todas as letras. Vídeo = roteiro + offset, e as três grandezas saem do mesmo lado: link, teto e todos os timestamps do CSV são tempo de **vídeo**. Antes de escrever uma linha, declare qual lado o dono deu, nesta forma: `O minuto 42 é do ROTEIRO (padrão) · offset 5:00 · link no vídeo em 47:00 · duração 60:00 de roteiro · teto no vídeo 65:00.` Se o dono disse "60 minutos de vídeo", a conta inverte e vai escrita igual: `duração 60:00 de VÍDEO · roteiro termina em 55:00 · teto no vídeo 60:00.` Adotar a premissa sem escrever a conta reprova a etapa, mesmo que a planilha saia coerente por dentro.

**Conflito de eixo temporal, quando o disco e o dono discordam.** Quando existe roteiro ou transcrição real no disco E o dono declara outro tamanho de aula ou outro minuto de oferta, os dois eixos valem, cada um mandando numa coisa. **O roteiro real manda no POSICIONAMENTO das reações de conteúdo:** cada reação casa com o beat que realmente passou, porque é o vídeo real que a plataforma vai tocar. **O número declarado manda na CONTA do link e do teto**, que é o que o dono controla no painel. Entregue os dois eixos lado a lado na tabela de auditoria, nesta forma: `eixo do disco: duração <MM:SS> · oferta em <MM:SS> (fonte: <arquivo>) · eixo declarado: duração <MM:SS> · oferta em <MM:SS>`, e **pergunte ao dono qual vídeo vai subir antes de fechar**. Replotar os beats reais num eixo declarado que não existe põe toda reação de conteúdo no minuto errado se o vídeo real for o que sobe: a sala reage ao mecanismo dez minutos antes de ele ser nomeado, e o lead vê isso.

**Checagem verificável do tempo (releia o CSV, imprima os números).** Antes do STOP, reabra o `06-chat-simulado.csv` salvo e escreva no planejamento, nesta ordem:
1. `Link no ar em: MM:SS` (a conta acima, oferta + offset).
2. `3 primeiros timestamps que citam preço, parcela, garantia ou bônus: MM:SS, MM:SS, MM:SS` (relidos do arquivo; se houver menos de 3, escreva quantos existem). O primeiro deles tem que ser **maior** que o do link; se for menor, reprova e a linha volta pra depois do link.
3. `Teto: MM:SS (duração + offset) · maior timestamp do arquivo: MM:SS · linhas acima do teto: N.` **N maior que 0 reprova**, e a contagem vai escrita mesmo quando é zero: linha agendada além do fim do vídeo nunca dispara no import.

**A ordem preço-depois-do-link é checagem executável, não promessa.** Antes do STOP, releia o CSV salvo (nunca a memória do que você escreveu) e escreva no `06-chat-planejamento.md`, com número medido: o timestamp do vídeo em que o link abre, que é (minuto da oferta no roteiro + offset da sala de espera); a lista de TODOS os timestamps de comentário que citam preço, parcela, garantia ou bônus; e a prova da ordem, ou seja, o menor desses timestamps comparado com o do link. Qualquer um deles antes do link reprova a entrega e volta pra correção. Confira junto o teto: nenhum timestamp do CSV passa de (duração declarada da aula + offset), porque linha além do fim do vídeo nunca dispara no import. Auditoria que afirma a ordem sem citar os dois números medidos não vale como auditoria.

**As outras 4 checagens executáveis do chat (mesma régua da ordem preço-depois-do-link: relidas no CSV, escritas com número).** Antes do STOP, o `06-chat-planejamento.md` traz estas 4 linhas, cada uma com o valor medido no arquivo salvo:

1. **Sala de espera povoada:** `Entradas de vídeo entre 00:30 e <offset>: N` (piso 8, ou 4 quando o offset é menor que 2 minutos). Sala de espera vazia reprova.
2. **Rajada da transição pro pitch:** com roteiro, toda rajada nasce de um comando do roteiro. **Sem roteiro, você segue a espinha padrão de comandos do `_CHAT-MODELO.md` §5** e declara: `Modo sem roteiro. Comandos assumidos: <lista com timestamp>.` A rajada da transição pro pitch é obrigatória nos dois modos.
3. **Nada de rodízio determinístico, e sala com escada de micro-compromissos:** `Nomes com 3+ falas: N (mínimo 8, e piso de 20% do elenco) · com intervalo fixo: 0 · sequências de 3 nomes repetidas: 0 · nomes distintos: N (entre 15% e 40% das linhas).` Zero nome com 3 falas reprova a planilha mesmo com os outros números limpos: sem gente voltando ao chat não existe escada de micro-compromissos, e é ela que prepara a sala pro pitch. A ficha de digitação por persona sai em `personas-digitacao.csv`, entregue junto. **Esses números saem do script, nunca da leitura:** rode `python3 scripts/auditar_chat.py 06-chat-simulado.csv --link MM:SS --teto MM:SS --offset MM:SS` e **cole a saída literal dele** no `06-chat-planejamento.md`, com o comando acima dela. O script mede as três contagens, a régua de elenco, a sala de espera, o teto, a ordem e a prova de preço-depois-do-link, e imprime o veredito. **Ele mede mais duas coisas que o rodízio de nome não pega, e as duas reprovam:** `linhas com texto repetido de outra linha: N (teto 10% das linhas)` e `linhas com acento: N de M`. Uma planilha passou com veredito limpo tendo 51 de 117 linhas repetindo texto de outra linha e zero acento em 4.553 caracteres: quem lê a tela vê as duas. Repetição acima de 10% das linhas reprova, com exceção declarada só pro comando que o host pediu em coro. Zero acento em mais de 500 caracteres reprova como `chat sem acentos`: chat brasileiro sem um acento não foi escrito em português. **Auditoria escrita à mão reprova**, mesmo com o número certo: o olho não pega rodízio, e uma trinca de nomes repetida oito vezes já passou debaixo de uma linha que declarava zero. Sem shell, escreva `não medido (sem shell)` em cada uma das três e marque a planilha como não auditada; o que não vale é declarar `0` sem a saída colada.
4. **Elenco não toca a prova do dono:** `Nomes na prova do dono: <lista> · nomes do elenco: <lista> · coincidências de nome, primeiro nome, ou nome mais idade: 0.` Persona com nome, idade ou caso que tangencie pessoa real citada na prova é proibida, mesmo com o sobrenome trocado. **A colisão se testa por nome CONTIDO, nunca por string inteira**, e o nome composto é testado também pela primeira palavra: `Paula J.` no elenco colide com `Ana Paula, 40` na caixa de entrada, e uma entrega declarou `coincidências: 0` com as duas no mesmo arquivo. Rode `for n in $(cat nomes.txt); do grep -inE "(^|[^a-zà-ú])$n([^a-zà-ú]|$)" <peça>; done` e cole a saída literal. `colisões por nome contido: 0` sem essa saída colada não conta como feito.
5. **A sala É o avatar:** `Avatar declarado: <faixa etária, gênero predominante, dor de entrada, em 1 linha> · nomes coerentes com o gênero predominante: N de N · perfis derivados do avatar: N de N · perfis vindos de lista de exemplo: 0.` Sala majoritariamente masculina num webinar cujo avatar é feminino reprova, e perfil de profissão copiado de exemplo de referência reprova: os perfis saem da dor de entrada do avatar do dono, nunca de uma lista pronta.
6. **Coerência entre `username` e texto:** `linhas com nome no texto divergente do username: 0 · linhas com gênero gramatical divergente do nome: 0 · personas com o primeiro nome do host ou do dono: 0.` Persona que se apresenta com outro nome ("Anderson Reis" escrevendo "Camila aqui de SP") e nome masculino escrevendo no feminino aparecem na tela do lead e reprovam a planilha.

**A auditoria só existe relida.** Toda linha acima é medida reabrindo o `06-chat-simulado.csv` salvo, nunca de memória, e fecha com `Ordem conferida: as N linhas estão em ordem crescente de (minutes, seconds), sem duas no mesmo segundo.` Auditoria sem número medido em cada linha não conta como auditoria e a entrega volta.

**Leia primeiro:** `_CHAT-MODELO.md` (a spec canônica, INTEIRO antes de gerar uma linha) · no modo ao vivo, `interacao-chat-ao-vivo.md`.

**Profundidade:** `simulador-comentarios-ao-vivo.md` (a doutrina longa: curva, honestidade, consistência) · `exemplos-por-bloco/14-interacao-chat.md`.

**Regra-mãe: simula a SALA, nunca a PROVA.** Comentário reproduz chegada, dúvida, reação, "eu quero", "comprei agora". Nunca inventa resultado de produto, número de vaga falso, preço, garantia ou bônus que o apresentador ainda não abriu. Tempo do vídeo = minuto do roteiro + offset da sala de espera. Gate do Crivo por dentro: todo comentário é copy que o lead LÊ.

---

## When NOT to use

Em toda rota abaixo: se a skill não estiver instalada, faço aqui em modo reduzido.

Render fino do deck / arte / PNG / paleta → **soft-designer**. Carta / VSL / landing fora do webinar → **soft-funil-carta** / **soft-funil-landing**. Micro-aula / mini-webinar de funil → **soft-funil-miniwebinar**. Posicionamento / nomear método → **soft-plano-posicionamento**. Venda 1:1 / objeção ao vivo / fechamento → **soft-vendas-closer** (prospecção: **soft-vendas-sdr**). Anúncios → **soft-trafego-meta**. Headline isolada → **soft-conteudo-headlines**. Conteúdo de feed → **soft-conteudo-***. "Por onde começo" → **soft-leon**.

## Transversais

`shared-references/` (operação-padrão, crivo/, filtro-anti-ia/, filtro-mobile-first/, adaptação semântica, dicionário conversacional) · `scripts/lint_copy.py` (anti-IA em código, rode no shell quando o ambiente permitir) · `references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta).

---

## ⛔ REGRA DA TELA, ACRESCENTADA EM 02/09/2026 (vale na Etapa 3 · AULA, e manda sobre as references)

**O slide é auto-explicativo.** Quem lê só os slides, do primeiro ao último, entende o argumento
inteiro da aula, na ordem, sem a fala do lado. E quem vai apresentar olha o slide e já sabe o que
falar, mesmo sem ensaio.

Na prática, dentro do campo CONTEÚDO de cada slide: **toda linha que vai para a tela é uma frase
completa, com verbo conjugado, terminando em ponto, interrogação ou exclamação, e entendida sem
depender do slide anterior nem da fala.** Rótulo curto (nome de fase, etapa de fluxo, nome de campo)
está proibido em linha própria: ele só existe como etiqueta colada a uma frase completa na mesma
linha. Continua proibido o outro extremo, o parágrafo falado inteiro na tela.

Duas leituras provam a tela, e as duas precisam passar: alguém que nunca viu a aula reconstrói o
argumento lendo só as telas, e alguém que nunca leu a fala sabe o que falar olhando só para o slide.

A regra escrita por extenso, com exemplo ruim e exemplo bom, está em
`references/tela-granularidade-e-bloco.md`, no bloco do topo. Onde `references/geracao-de-slides.md`
pregar "slide mínimo", leia mínimo como poucas frases completas, nunca palavras soltas.

Ordem de origem: decisão do dono do método, registrada em 02/09/2026.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## A saída do script entra uma vez (fecho, vale em toda entrega)

**A saída do script entra uma vez e não se reescreve em prosa.** Recorte mais amplo que o do script sai com **rótulo diferente** e com o comando que o produziu ao lado, nunca com a mesma frase que o script usa. Duas listas com o mesmo rótulo e conteúdo diferente reprovam a entrega. Confira por comando antes de fechar: `python3 scripts/checar_titulos.py --conferir <pasta de saída>; echo exit=$?`, que reprova com `saída do script reescrita` quando o mesmo rótulo aparece com duas listas, e com `inventário duplicado` quando a entrega traz dois números de inventário diferentes. **`exit` diferente de 0 proíbe a entrega.**
