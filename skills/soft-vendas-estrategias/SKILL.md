---
name: soft-vendas-estrategias
description: >-
  Decide QUAL jogada de campanha rodar agora e em que ordem no mês. Entrega o Plano de Jogadas ou a jogada montada, pronta pra passar na voz do dono. Use quando o pedido for: "o que eu vendo esse mês", "como faço caixa rápido", "plano do mês", "qual campanha eu rodo", "vou lançar minha mentoria", "como relanço", "que jogada eu rodo pra reativar minha base", "como valido um produto novo", "vou subir o preço", "monta minha reunião paga", "levantada de mão". NÃO use pra: "tô sem caixa" quando a conta é de DRE, margem ou dívida (soft-financeiro); escrever a régua de mensagens da reativação (soft-funil-nutricao); abrir, qualificar ou agendar o lead que a jogada gerou (soft-vendas-sdr); conduzir e fechar (soft-vendas-closer); a proposta em site (soft-vendas-proposta); desenhar e precificar a mentoria (soft-plano-ofertas); tráfego pago (soft-trafego-meta); o próximo passo do fundador (soft-leon); a copy da peça (soft-conteudo-*). Leia e siga o fluxo inteiro do SKILL.md.
---

# As jogadas: o que vender agora, e em que ordem

Caixa não entra de postar mais. Entra de rodar a jogada certa pro momento: a audiência que o dono tem, a oferta que ele quer mover, a meta do mês. Esta skill lê o momento e devolve qual jogada rodar, em que ordem, com que frequência, e onde o lead quente é entregue pra quem vende. O resultado é um documento nomeado: o Plano de Jogadas do mês, ou uma jogada montada pronta pra passar na voz do dono.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**O H1 do documento interno carrega o número que o documento mede.** Forma: `<número medido> <o que ele custa ou libera>`. Rótulo de tipo de documento e nome do negócio sozinho reprovam. Cole `H1: <literal> · número medido no H1: sim/não`. **`títulos de abertura: 0` num documento que tem H1 é resultado inválido**, porque o H1 entra no universo da régua, e remover o H1 não é alternativa a escrevê-lo bem: `.md` de peça sem nenhuma linha `^# ` sai com exit 1 e `peça sem H1`.

**A frase que sobrevive não pode sobreviver à troca de nicho.** A frase-tese da peça passa pelo teste do nicho trocado como qualquer outra linha, e `sobrevive? sim` nela reprova, ao contrário da tabela de checagem. Cole `frase que sobrevive | substantivo trocado: <original> → <outro mercado> | sobrevive? não`. Máxima de marketing que qualquer negócio repetiria não é a frase da dona: é a frase de ninguém.

**A linha do inventário aparece duas vezes na entrega, e só duas:** uma na peça que o dono lê e uma no `conferencia/checagem-titulos.md`. Recitar a linha dentro do RELATO não conta como prova. Cole `linhas de inventário na entrega: 2`.

**Os títulos das etapas são teses, não rótulos.** `## P3` é numeração; `## P3: cada peça existe para impedir uma desistência específica` é a etapa dizendo o que decidiu. **O prefixo enumerador vale pra qualquer nível, H2 e H3: `Jogada N:`, `Passo N`, `Etapa N`, `Bloco N` somem, e a tese fica** (`### A base reconhece o próximo passo`, nunca `### Jogada 1: a base reconhece o próximo passo`): a ordem já está na sequência do documento e não precisa de rótulo. A isenção de rótulo estrutural vale pra cabeçalho de anexo, de tabela e de fonte, **nunca pras etapas do plano**: renomear uma etapa pra caber na isenção reprova a entrega, porque troca a qualidade da peça pela facilidade do gate, e o `--conferir` imprime cada caso como `rótulo no miolo: <linha>`. Cole `etapas: N · com tese no título: N`, iguais. **E nenhum cabeçalho nomeia um requisito da régua:** `Seção de fecho`, `Frase que sobrevive`, `Checagem`, `Inventário` e `Régua` são nomes do gate. A frase que sobrevive entra no fecho sem cabeçalho próprio, ou sob um cabeçalho que seja ela mesma. Cole `cabeçalhos que nomeiam um requisito do gate: 0`.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra, num caso fictício de nicho neutro, a entrada que o dono deu, as perguntas que a skill fez e a saída de cada ação: o diagnóstico do momento, o Plano de Jogadas do mês inteiro, uma jogada montada frase a frase e a estratégia de lançamento. Ler antes economiza uma rodada inteira de retrabalho.

**Quem já sabe qual jogada quer, pula direto pra ela.** Quem não sabe é perguntado, e a pergunta é uma só. Está na tabela de roteamento logo abaixo.

> **A doutrina que rege tudo:** nenhuma jogada vende sozinha. Toda jogada filtra E convence, revela a dor real e confirma o próximo passo, nunca empurra. O script bruto de cada jogada é esqueleto: passa pela voz do dono e pelo filtro anti-IA antes de ir pra rua. Tom de robô educado ("espero que esteja bem", "agradeço a confiança") mata a jogada.

### A régua de canal por ticket (mesma régua das skills irmãs)

Até R$ 3.000 o fechamento acontece na própria conversa (DM ou WhatsApp, com áudio, doc e vídeo curto). Acima de R$ 3.000 a conversa qualifica e agenda a call 1:1, e o fechamento acontece na call. O funil de aula/webinar é a exceção: ele fecha de uma vez no checkout, dentro da própria aula. A call também entra abaixo do limiar quando o lead pede a condução ao vivo, quando a decisão é a vários ou quando o caso é complexo. Esta régua é a mesma nas skills irmãs soft-vendas-sdr, soft-vendas-closer e soft-vendas-estrategias, com o texto idêntico nas três; mudou numa, muda nas três.

### A fronteira com as duas irmãs (escrita dos dois lados)

| Quem | O que é dela | Onde para |
|---|---|---|
| **soft-vendas-estrategias** (esta) | a JOGADA: decide qual campanha rodar no mês, em que ordem, e como lançar a oferta | para quando o lead esquenta; não abre conversa, não responde objeção, não fecha |
| **soft-vendas-sdr** | o TOPO: abre a conversa que a jogada gerou, qualifica de leve, vende a sessão e agenda | não escolhe campanha nem monta plano do mês |
| **soft-vendas-closer** | o FUNDO: conduz as 7 fases, isola objeção, pede a decisão e coleta o sinal | não escolhe campanha nem monta plano do mês |

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a audiência, a oferta e a meta e eu monto o plano de jogadas). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pro plano com o que o dono colou. Se faltar um insumo que a jogada não vive sem (o tamanho da base, a oferta, a meta), pergunta AQUELE insumo e segue, sem repetir o diagnóstico inteiro.
- **Modo guiado**: só quando o dono pede explicitamente. Pergunta a audiência que o dono tem, a oferta que quer mover e a meta do mês, uma coisa de cada vez, e monta o plano com o que ele for dando.

A pergunta do modo é UMA por plano. As outras três partes acontecem nos passos abaixo:

- **Ensina enquanto faz:** em cada escolha estrutural (qual jogada, por que ela e não a de maior custo, a ordem no mês) escreve UMA linha do porquê. O dono lê a razão e aprende a ler o momento sozinho.
- **Puxa o material bruto:** quando a resposta vier rasa ("quero vender mais", "minha base toda"), não segue com o genérico. Pede o concreto que só o dono tem: quantos leads quentes ele tem hoje, o que vendeu na última campanha, o número que precisa fazer esse mês. Dado real escolhe a jogada certa; resposta rasa escolhe a jogada mais cara.
- **Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer uma jogada de menor custo? outra ordem no mês? a jogada já montada na tua voz? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "tô sem caixa esse mês", "o que eu vendo agora", "plano do mês", "qual campanha eu rodo", "não sei por onde começar" | **1 · DIAGNÓSTICO DO MOMENTO**, e segue até a 2 |
| "monta minha levantada de mão", "monta a caixinha", "quero fazer a reunião paga", "monta a pré-venda", "Pix de compromisso", "reativa minha base" | **3 · JOGADA MONTADA** (entra direto, a jogada já está escolhida) |
| "vou lançar minha mentoria", "como relanço", "vou abrir turma nova", "vender antes de montar" | **4 · ESTRATÉGIA DE LANÇAMENTO** |
| "quero esquentar lead frio antes de falar com ele", "funil pra quem vende serviço" | **5 · FUNIL DE AQUECIMENTO** |

Pedido ambíguo ("me ajuda a vender", "o que eu faço"): pergunte UMA coisa só, "você já sabe qual jogada quer rodar, ou quer que eu leia o seu momento e escolha?", mostre a tabela como cardápio e siga pela resposta.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · passos numerados com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de cliente ideal, oferta, PUV, voz ou prova: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR]`. Nenhum número vira prova no documento sem estar no banco de provas do dono.

**Como o método trata número e exemplo:** onde aparece exemplo, ele vem em nicho fictício rotulado, que mostra o formato e nunca é molde pra copiar. Nenhum resultado (ticket, quantidade de vendas, taxa) é afirmação universal: ou vira princípio sem número, ou vira campo do dono, preenchido com ele e marcado `[A CONFIRMAR]` até validar. Números de mecânica (R$ 100 de filtro, 10% do sinal, 2 fundadores, 6 a 7 pessoas, 3 a 7 perguntas por dia) ficam, porque são parâmetro do processo, não prova emprestada.

---

## Ação 1 · DIAGNÓSTICO DO MOMENTO (de onde a jogada nasce)

**O que faz:** lê o momento do dono com 5 perguntas e aponta a jogada de menor custo disponível.

**Precisa de:** cliente ideal e oferta, do perfil/brain do agente · a meta do mês, se existir · as 5 respostas do momento.

**Sem o insumo:** sem posicionamento nenhum (não sabe cliente ideal nem a oferta), pare e mande pra `soft-plano-posicionamento` antes, porque jogada sem oferta clara não vende nada. Sem a meta do mês, siga assim mesmo: escolha a jogada pelo momento e chute a cadência com número (por exemplo, 2 contatos por dia, caixinha em 3 dias da semana), sempre com a frase "ajuste se não servir", dizendo em 1 linha que o número fecha melhor quando a meta existir.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar. **E o marcador só mora em posição de CAMPO:** um link, um número, uma data ou um valor, no fim da linha, substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase que alguém fala, ouve ou lê, e em qualquer peça exportada que o dono manda pra fora sem reler. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça; o furo em si vai pro handoff, nunca pra fala. Checagem: apague o marcador e leia a frase, e a pergunta é "a frase existiria sem o dado?". Com shell, `grep -n "\[A CONFIRMAR" <peça>` lista as linhas pra conferir uma a uma. Cole `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`. **Exceção: cadência é escolha operacional, não fato.** Contatos por dia, dias de caixinha por semana, horário de disparo e toques por semana SAEM SEMPRE com um número sugerido mais a frase "ajuste se não servir", nunca como `[A CONFIRMAR]`. O dono não tem esse número na cabeça, ele espera a sugestão; marcá-lo como pendência devolve pra ele uma decisão que a jogada devia ter chutado.

**Entrega:** a primeira seção do `01-plano-jogadas.md`, com o momento diagnosticado e a jogada de menor custo apontada. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/jogadas-de-campanha.md` (o cardápio rápido das 10, pra saber o que cada uma exige antes de apontar).

### As 5 perguntas que escolhem a jogada

| Sinal | Se SIM, a jogada de menor custo |
|---|---|
| **Tem base de clientes ou ex-clientes?** | **Lembrei de Você** (#10), o caixa mais barato, sempre a primeira ao abrir produto novo |
| **Tem audiência ativa, mesmo pequena?** | **Levantada de Mão** (#1) mais **Caixinha** (#2) rodando em fundo |
| **Tem produto novo pra testar antes de criar?** | **Pré-venda** (#6), valida com dinheiro na mesa |
| **Vai subir preço, ou tem demanda represada?** | **Pix de Compromisso** (#7), congela quem quer mas não tem o valor cheio |
| **Tem volume de DM cansando o manual?** | **Vendas Automáticas** (#9) mais **Destaques** (#8), piloto automático |

**Regra do menor custo:** sempre começa pela jogada de menor custo de aquisição disponível no momento. Base quente antes de audiência, audiência antes de tráfego. A Reunião de R$ 100 (#5) entra como pico do mês quando ele tem audiência semente, e cerca de 200 visualizações qualificadas já sustentam.

---

## Ação 2 · PLANO DO MÊS (a ordem, não uma jogada solta)

**O que faz:** monta a combinação de jogadas na ordem e na frequência que fecham o volume de conversa que a meta exige.

**Precisa de:** o diagnóstico da Ação 1 · a meta do mês, quando existir.

**Sem o insumo:** sem meta, monte a ordem mesmo assim e chute a cadência com número (contatos por dia, dias de caixinha por semana) mais a frase "ajuste se não servir": cadência é escolha operacional, não fato do dono, e nunca sai como `[A CONFIRMAR]`. Diga em 1 linha que o número de toques por semana fecha melhor quando a meta existir.

**Entrega:** `01-plano-jogadas.md` completo, com o diagnóstico, as jogadas escolhidas e o porquê, a ordem no mês, a frequência e o ponto de handoff comercial. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**A jogada escolhida sai com a PRIMEIRA MENSAGEM ESCRITA, sempre, e isso é parte da Ação 2.** Plano do mês sem uma linha que o dono copia e cola é meia entrega: quem pergunta "qual a melhor jogada" está perguntando também "o que eu digo", e devolver só o plano deixa com o dono exatamente o trabalho que ele queria terceirizar. Ao fechar a Ação 2, escreva o esqueleto da abertura da jogada nº 1, na voz do dono, marcado como esqueleto a revisar, e rode a régua de títulos sobre a primeira linha dele. A Ação 3 continua sendo a jogada inteira frase a frase, com as variantes e as respostas às objeções; o que a Ação 2 deve é a abertura da primeira. Ler o pedido como "ele não pediu a jogada linha a linha" e parar no plano é a leitura que reprova, porque a abertura escrita custa cinco linhas e é o que faz o plano virar ação na segunda-feira. **Toda jogada que entra na lista de escolhidas sai com a abertura escrita, não só a primeira.** Se o plano recomenda 5 jogadas, saem 5 aberturas; se você não tem munição pra escrever a quinta, ela não deveria estar na lista de escolhidas, e a saída certa é reduzir a lista, não reduzir a copy. Checagem colada: `jogadas escolhidas: N · com abertura escrita: N`, e **os dois números têm que ser IGUAIS**, com qualquer diferença reprovando a Ação 2. Uma lista longa sem copy transfere pro dono o trabalho de escrever cinco mensagens; uma lista curta com tudo escrito é a entrega. **Toda abertura sai em bloco cercado, pronta pra enviar, e citação markdown não conta.** O dono copia o bloco; o que está fora do bloco ele nunca copia por engano. Entregar a abertura em `>` com o rótulo "esqueleto pra revisar" faz ele não saber onde o texto começa e sugere reescrever antes de usar; o bloco sai pronto, e quando faltar um dado ele é campo curto (até 3 palavras) dentro do bloco, com a instrução de preencher fora dele. Cole `aberturas pro dono enviar: N · em bloco cercado: N`, iguais.

**Toda abertura que peça uma palavra passa pelo grep antes de ser escrita, e o resultado vai colado.** Antes de escrever o CTA, rode `grep -rniE '<candidata>' <pasta de insumos> <perfil>` e cole `palavra-chave: <literal> | origem: <arquivo:linha>`. Quando o grep voltar vazio, **é PROIBIDO escolher uma palavra**: reescreva o CTA na versão que dispensa a palavra ("me chama no Direct que eu te conto") e leve a pergunta ao handoff. Quando existir uma palavra já usada pelo dono em qualquer insumo, **ela é a resposta e não há escolha a fazer**: duas palavras-chave concorrentes na mesma conta dividem a automação e a memória da audiência. Checagem colada por jogada: `CTA com palavra-chave: sim/não · palavra: <literal> · origem: <arquivo:linha>`, e "sim" sem origem reprova a Ação 2.

**Leia primeiro:** `references/jogadas-de-campanha.md` (as 10 no formato completo, e os fios que costuram uma na outra).

**Ordem típica num mês de partida:** Lembrei de Você (base quente primeiro) → Levantada de Mão mais Caixinha em fundo → Oferta Direta uma vez por semana → Reunião de R$ 100 como pico → Pré-venda quando for testar produto novo → Pix de Compromisso pra fechar o quente que emperrou só no preço. Destaques e Automáticas entram quando o fluxo de seguidor novo e o volume de DM crescem.

**Como as jogadas se encadeiam:**

1. **Motor diário sempre ligado:** Caixinha (#2) e Oferta Direta (#3) rodam todo dia ou toda semana, subindo autoridade ou carregando oferta, sem depender de evento.
2. **Entrada de lead quente:** Levantada de Mão (#1) enche o direct e qualifica um a um.
3. **Vender com história:** Storytelling mais Oferta (#4), ideal pra lançar e relançar.
4. **Micro-lançamento com caixa:** Reunião de R$ 100 (#5), filtra curioso, entrega valor, oferta no fim.
5. **Validar antes de criar:** Pré-venda (#6), vende o produto antes de ele existir.
6. **Fechar quem emperrou só no preço:** Pix de Compromisso (#7).
7. **Escalar sem repetir esforço:** Destaques (#8) deixam as ofertas organizadas no perfil.
8. **Piloto automático:** Vendas Automáticas (#9) plugam o atendimento no direct.
9. **Reativar a base:** Lembrei de Você (#10), o caixa mais barato.
10. **A esteira que costura tudo:** entrada barata sobe pra grupo e mentoria. Quem desenha a mentoria é a `soft-plano-ofertas`.

---

## Ação 3 · JOGADA MONTADA (o esqueleto na voz do dono)

**O que faz:** monta uma jogada específica passo a passo, pronta pra passar na voz do dono.

**Precisa de:** a jogada escolhida · a oferta e o preço · a voz do dono e o verbatim real do público.

**Sem o insumo:** entrevista curta de 4 perguntas: qual oferta essa jogada move · por quanto · pra quem exatamente · me manda 3 falas reais dessa pessoa. Sem verbatim, monte o esqueleto com `[A CONFIRMAR]` no lugar de cada aspa que se declararia real e diga isso em 1 linha.

**Entrega:** `02-jogada-montada.md`, com o que é, quem pode rodar, o resultado esperado como campo do dono, o passo a passo com as falas, onde encaixa no mês, quem executa e o ajuste de tom. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/jogadas-de-campanha.md` (a jogada escolhida, no formato completo com os roteiros).

### As 10 jogadas, em resumo executável

| # | Jogada | O núcleo dela |
|---|---|---|
| **1** | **Levantada de Mão** (funil de stories) | Story com os 5 elementos: escassez real, público nomeado, resultado, urgência e UM chamado. Fala-âncora: *"Procuro [2 a 3] [público] que querem [resultado] nos próximos [X dias]. Vou te mostrar como [mecanismo]. Se você quer [resultado], responde [palavra]."* Posta como primeiro story do dia, 24 horas qualificando com 3 perguntas, oferta na DM com vídeo curto personalizado. Follow-up em 24 horas ("viu?") e 48 horas (só o nome) |
| **2** | **Caixinha de Perguntas** (o coringa diário) | 3 a 7 perguntas por dia mais 1 ou 2 ofertas no meio. Reformula pergunta mal feita, manda pergunta a si mesmo pra ativar o comprador silencioso. Alterna tipo autoridade (resposta que dá vontade de printar) com tipo oferta. Padrão visual fixo. Não responde caixinha à toa |
| **3** | **Oferta Direta** (comunicar claro, por público) | Escolhe 1 público específico ("é pra você que..."), o modelo de copy e a rota: com preço quando já validada ou pra ancorar; sem preço, só DM, quando ainda valida demanda; checkout direto quando validada. Ancoragem: oferta cara antes da barata |
| **4** | **Storytelling mais Oferta** | Base quente primeiro. Sequência: chamada, micro-história real de mudança, ponte, oferta, ação rápida com condição de quem é de casa. Duas horas depois, caixinha de dúvidas. Depois replica pro público aberto mudando o contexto final |
| **5** | **Reunião de R$ 100** (micro-lançamento, o pico) | O R$ 100 é FILTRO, reembolsável, não é o produto. Dois formatos: turma pequena de 10 a 15 com sabatina, ou temática com 20 ou mais sem sabatina. Sequência de stories: gancho que qualifica, oferta forte, urgência, prova social, quebra de objeção. Roteiro de 1h a 1h30: agenda, conteúdo útil de verdade, oferta do próximo passo em 5 a 10 minutos com vantagem exclusiva e não desconto, oferta ativa por 24 horas, feedback individual no dia seguinte que vira depoimento |
| **6** | **Pré-venda** (validar antes de criar) | Descobre a demanda antes, nunca inventa. Sequência: curiosidade, segredo, apresentação, conteúdo e pra quem é, preço cheio com prova, condição especial de pré-venda, bônus que a pessoa já consome na hora. Vira destaque e repete mudando só o prazo |
| **7** | **Pix de Compromisso** (congela o preço com 10%) | Ancorado em aumento de preço real. Mostra o grupo e o número de membros, avisa que o preço sobe ao bater [N], qualifica de forma explícita ("só pra quem já decidiu"), oferece 10% agora que congela por 6 meses, com a diferença parcelável, mais bônus que ajudam a juntar o resto. NUNCA esconde o valor cheio |
| **8** | **Vendas com Destaques** (esteira no perfil) | Primeiro os destaques de prova e de quebra de dúvida. 1 destaque por produto. Dentro: o que é, como funciona, mostra por dentro, casos, chamado. Mantém atualizado, porque número desatualizado reprova |
| **9** | **Vendas Automáticas** (atendimento no direct mais downsell) | Stories com afastamento honesto ("é pago, se não vai executar não envie"). A primeira mensagem assume que é automação e revela o preço cedo. Quem não fecha vai pra opções mais acessíveis. Downsell: quem não se qualifica pro principal pega a sessão menor como primeiro passo. Quem OPERA o atendimento no canal é a `soft-vendas-sdr` |
| **10** | **Lembrei de Você** (reativar a base) | Segmenta em regulares, ex-clientes e alto valor. Conexão de verdade primeiro, nunca abre com pitch. Apresenta a novidade como evolução natural, pra ele se sentir parte e não alvo. **Atenção:** o esqueleto padrão engana com tom de robô educado, e isso não passa no anti-IA. Reescreve na voz do dono e fala pelo teto que aquele cliente sente, nunca por "estou lançando" |

---

## Ação 4 · ESTRATÉGIA DE LANÇAMENTO (vender antes de montar)

**O que faz:** define como lançar a oferta sem montar a estrutura inteira antes de vender.

**Precisa de:** a oferta a lançar e o ticket · a data em que ele consegue começar a entregar.

**Sem o insumo:** entrevista curta de 3 perguntas: o que você vai lançar · quando você consegue começar a entregar de verdade · quantas pessoas você aguenta atender no primeiro mês. Com essas 3 a estratégia sai inteira.

**Entrega:** `03-estrategia-lancamento.md`, com a data futura, os 2 fundadores alternados, o critério de consumo, o teto individual, a porta de entrada e o canal de fechamento. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/lancamento-e-esteira.md` (vender antes com data, fundadores alternados, critério de consumo, micro-oferta como porta, downsell com cashback, a esteira de 3 públicos e a matemática da meta).

**Profundidade:** `references/time-comercial.md` (a jogada de escala do time comercial: quando montar equipe, a triagem por pré-treinamento, a remuneração de referência, o ritmo de gestão por cargo).

A regra-mãe: **não monta a estrutura inteira antes de vender**, porque a pessoa compra pelo fim, não pelo meio.

- **Vende ANTES, com data futura.** Lança com uma data lá na frente pra começar, vende, organiza enquanto os primeiros entram.
- **2 fundadores em dias ou semanas ALTERNADOS.** O primeiro na segunda, você vê a evolução na semana, leva o aprendizado pro segundo na quinta. Itera o método de um pro outro e ganha velocidade.
- **Fundador em troca de caso documentado:** os primeiros entram por condição especial em troca do caso, com formulário de saída e depoimento. Sem caso, não escala.
- **Critério de consumo:** só libera o próximo nível quem consumiu o atual. Isso puxa quem estava parado.
- **Individual até 6 ou 7 pessoas.** Passou disso, é hora de pensar em grupo, e isso é desenho de produto, da `soft-plano-ofertas`.
- **A micro-oferta como PORTA de entrada** (sessão paga única de 60 a 90 minutos sobre UM problema): capta quem quer só um direcionamento. Vira grupo por cashback, pagando só a diferença, ou vira downsell de quem não fechou o principal. NÃO dá acesso ao grupo na sessão, senão mata a subida.

---

## Ação 5 · FUNIL DE AQUECIMENTO (o lead frio antes do contato humano)

**O que faz:** monta o funil que esquenta o lead frio em minutos, antes de qualquer contato humano, pra quem vende procedimento ou serviço.

**Precisa de:** o serviço vendido · a dúvida número 1 de quem contrata esse serviço.

**Sem o insumo:** pergunta única: "qual é a pergunta que todo mundo te faz antes de fechar?". A aula inteira nasce dela.

**Entrega:** `04-funil-aquecimento.md`, com a peça de entrada, a automação de comentário e mensagem, o roteiro da aula curta e o ponto onde o lead cai no canal humano. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/lancamento-e-esteira.md`, seção do funil de aquecimento.

A arquitetura: peça curta que fisga a dor, automação de comentário e mensagem ("digita [palavra]"), página com aula de cerca de 15 minutos que aquece (o especialista tira a dúvida do antes, do durante e do depois do serviço), botão de contato só no fim. Quem chega no canal humano já assistiu e chega quente pro fechamento 1:1, nunca frio. É tática, e convive com a escada de funis; a regra do menor custo continua valendo, base quente e audiência antes de tráfego frio.

---

## Contrato de entrega (vale em todas as ações)

O resultado sai como **UM documento markdown consolidado**. Se o ambiente renderizar markdown, mostre o documento inteiro ali; senão salve um arquivo `.md` no disco e cite o caminho completo na resposta. Num ambiente que não renderiza markdown, o documento vai num único bloco de código fechado, separado da condução. A condução vai em mensagens curtas, sem markdown pesado. Ao parar no STOP, você mostra ou atualiza o documento inteiro e pergunta "ajusto?".

**Uma resposta é no máximo UM passo novo.** Proibido rodar 2 ações no mesmo turno, mesmo com OK. O OK de uma libera só a seguinte. E o raciocínio de processo é interno: nunca narre qual ação detectou, nem explique o que o OK autoriza, nem anuncie que leu o SKILL. Conduz com a próxima pergunta, entrega o documento, ponto.

## Pré-flight de copy (releia imediatamente antes da primeira linha)

**Antes da primeira linha de copy da entrega, a palavra-chave sai de comando, UMA vez.** Rode `grep -rn -iE 'manda |comenta |envia |digita |palavra ' <pasta de insumos>` e cole a saída inteira em `conferencia/checagem-titulos.md`, **nunca no topo da peça nem do handoff**: a linha `Pré-flight de CTA, saída literal: ...` é diário de trabalho, e o `--conferir` reprova quando ela vaza pro corpo da peça (`bastidor na peça pública`). A palavra que aparecer nessa saída é a única que pode entrar em CTA nesta entrega, com a grafia exata, e o resultado desse único comando é reaproveitado em cada jogada: rodar de novo por jogada não vale, e escolher palavra que não está na saída não vale. Saída vazia proíbe escolher uma, e o CTA sai na versão que dispensa a palavra. Cole em `conferencia/`, por peça, `CTA com palavra-chave: sim/não · palavra: <literal> · origem: <arquivo:linha>`, e `sim` sem origem reprova antes da análise de conteúdo.

A copy nasce da terça-feira à noite DO LEITOR. A regra é checagem, nunca geradora: escreva a partir da cena e da emoção dela, com voz de mesa; a regra confere depois. Reprovou, regenera do zero, porque frase editada herda o esqueleto do defeito.

1. **Munição na mão:** verbatim e prova real do dono na frente; sem munição, pergunta, jamais inventa.
2. **Leitura única:** uma leitura em voz alta, sem reler; valência única; sintaxe linear; 1 operação mental por frase.
3. **Mundo do leitor:** componente do método vira dia, hora, lugar e fala do cliente.
4. **Compressão gramatical: cota zero.** Verbo da relação por extenso; a força é do fato.
5. **Voz de mesa, não palco:** a colocação inteira é fala real; metáfora morta entra, figura de escritor não.
6. **Prova com atribuição exata**, do banco de provas do dono, nunca fundida.
7. **Anti-IA:** zero travessão, zero da família banida, zero verbo genérico de transformação, zero frase de moldura.
8. **Teto do formato conhecido ANTES**, contado durante, não consertado depois.

## Gate de qualidade (roda por dentro, antes de entregar, e não sai no documento)

**O H1 do documento de decisão carrega o número da rodada e a decisão, nunca o rótulo.** O dono abre este plano pra escolher a jogada do mês, e rótulo não dá no que discordar. Errado: `Plano de Jogadas · setembro`. Certo: `Setembro começa por quem já confiou`. Cole `H1: <literal> · afirma algo que o dono pode discordar: sim/não · número medido no H1: sim/não`, e `não` na segunda coluna volta o documento pro passo de escrita.

**Todo tamanho de arquivo declarado no relato sai de comando, com tolerância zero.** O relato é a única parte da entrega que o dono confere sem abrir o terminal, e uma entrega declarou `conferencia/checagem-titulos.md: 8014 bytes` num arquivo de 7.464, mais `nomes.txt (0 bytes, lista vazia)` num arquivo de 68 bytes com 8 nomes. Rode `wc -c <cada entregável>` e `wc -l nomes.txt`, e cole a saída literal ACIMA da lista. Tamanho ou contagem que o `wc` contradiz reprova o relato, e o `--conferir` acusa como `bytes redigitados`.


**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


| Check | Passa se |
|---|---|
| **Ancoragem** | herdou cliente ideal e oferta do dono; sem posicionamento, mandou pra soft-plano-posicionamento |
| **Momento diagnosticado** | rodou as 5 perguntas antes de escolher a jogada |
| **Menor custo primeiro** | escolheu a jogada de menor custo disponível: base quente antes de audiência, audiência antes de tráfego |
| **Ordem no mês** | não entregou jogada solta; deu a combinação, a ordem e a frequência |
| **Filtra E convence** | cada jogada afasta quem não é cliente e convence quem se reconhece; nada de empurrar nem prometer milagre |
| **Prova real** | toda prova social é verdadeira, coletada por design; número de membros e caso atualizados |
| **Afastamento honesto** | onde a jogada usa afastamento, é filtro honesto e não manipulação |
| **Lançamento na ordem certa** | vende antes com data; 2 fundadores alternados; individual até 6 ou 7; critério de consumo; fundador em troca de caso; micro-oferta não dá acesso ao grupo |
| **Canal de fechamento certo** | seguiu a régua de ticket sem confundir com o funil de aula |
| **Fronteira respeitada** | não abriu nem qualificou lead (é da soft-vendas-sdr), não conduziu nem respondeu objeção (é da soft-vendas-closer), não desenhou nem precificou a mentoria (é da soft-plano-ofertas) |
| **Esqueleto vai na voz do dono** | todo script bruto sai marcado como esqueleto pra passar na voz do dono antes da rua; tom de robô educado reprova |
| **Números são do dono** | todo resultado, ticket ou taxa é do dono ou `[A CONFIRMAR]`; número de exemplo nunca virou promessa; números de mecânica ficam |
| **Saída densa e em arquivo** | tabelas e listas, não prosa; zero bastidor; a peça está num `.md` nomeado com o caminho citado |
| **Anti-IA** | com shell, roda o linter anti-IA do ambiente sobre o arquivo e exige saída limpa; sem shell, varre o texto inteiro atrás do travessão longo e da família do verbo-freio banida pela régua anti-voz, e **reescreve de fato** cada ocorrência |
| **VEREDITO** | é o pior item; um ✗ refaz o item, não o documento inteiro |

**A reescrita do travessão longo é o furo mais provável**, porque o modelo o usa por reflexo em prosa densa. Não basta procurar: reescreva cada ocorrência. Travessão de aposto no meio da frase vira vírgula; travessão que anuncia consequência ou lista vira dois-pontos; travessão que separa duas ideias inteiras vira ponto. Faça isso antes de marcar o item como aprovado, porque declarar aprovado sem procurar é o erro mais grave do gate.

Onde a pasta trouxer `shared-references/crivo/`, ele é a régua completa da copy e roda na última checagem.

## O que esta skill NÃO faz

Em toda rota abaixo: se a outra skill não estiver instalada, esta faz o mínimo aqui e diz que fez, com o pedaço mais fino marcado `[A CONFIRMAR]`.

- **Abrir, qualificar, agendar o lead, prospecção, CRM, agente de IA** → **soft-vendas-sdr**.
- **Conduzir, responder objeção, pedir o sim, coletar o sinal, follow-up de venda, analisar conversa, pós-venda** → **soft-vendas-closer**.
- **Desenhar, estruturar e precificar a mentoria em si** → **soft-plano-ofertas**.
- **Posicionamento, nomear método, PUV, oferta do zero** → **soft-plano-posicionamento**.
- **Tráfego pago, quanto investir, retorno do anúncio** → **soft-trafego-meta**.
- **A copy da peça** (headline, carrossel, reel, stories, carta, landing) → `soft-conteudo-*` e `soft-funil-*`.
- **Webinar, oferta de palco, o perpétuo** → `soft-webinar`.

## Anti-patterns

| Sintoma | Correção |
|---|---|
| Mandou postar mais ou produzir mais conteúdo | Escolhe a jogada certa pro momento, na ordem certa; conteúdo solto não é estratégia |
| Escolheu a jogada sem diagnosticar o momento | Roda as 5 perguntas antes de escolher |
| Começou por tráfego frio com a base quente parada | Menor custo primeiro: base quente antes de tudo |
| Entregou uma jogada solta | Dá a combinação, a ordem no mês e a frequência |
| Montou a estrutura da mentoria inteira antes de vender | Vende antes com data futura e monta com os fundadores |
| Começou o lançamento com 1 fundador só | 2 em dias alternados, pra iterar de um pro outro |
| Deu acesso ao grupo dentro da micro-oferta | Não dá acesso na sessão, senão mata a subida |
| Fabricou escassez ou prova pra apressar | Prova real, coletada por design; escassez só com gatilho real |
| Escondeu o valor cheio no Pix de Compromisso | Fala o preço desde o começo; os 10% congelam, não escondem |
| Escreveu o Lembrei de Você com tom de robô educado | Reescreve na voz do dono, pelo teto que aquele cliente sente |
| Foi conduzir a conversa ou responder objeção aqui | Isso é da soft-vendas-closer; esta entrega a estratégia e aponta |
| Foi desenhar ou precificar a mentoria aqui | Isso é da soft-plano-ofertas; aqui é como e quando lançar |
| Usou um número de exemplo como promessa do dono | Número de exemplo é só formato; o do dono é campo `[A CONFIRMAR]` |
| Documento com prosa e bastidor | Tabelas e listas; corta o "isto serve para" |

## Handoff

O Plano de Jogadas aprovado alimenta:

- **soft-conteudo-stories** (a sequência de stories da jogada) · **soft-conteudo-headlines** (a chamada da oferta) · **soft-conteudo-carrossel** e **soft-conteudo-reels** (o corpo da peça).
- **soft-funil-miniwebinar** e **soft-webinar** (o conteúdo da Reunião de R$ 100, se ela virar aula).
- **soft-vendas-sdr** (abrir, qualificar e agendar o lead que a jogada gerou).
- **soft-vendas-closer** (conduzir e fechar, pela régua de canal por ticket).
- **soft-plano-ofertas** (desenhar e precificar a oferta que a jogada lança).

Posicionamento ou PUV pendente volta pra **soft-plano-posicionamento**. Meta do mês pendente volta pro orquestrador.

## References

- `references/jogadas-de-campanha.md`: as 10 jogadas no formato completo (o que é, quem pode rodar, resultado esperado como campo do dono, o passo a passo com as falas-âncora, onde encaixa no mês, quem executa, o ajuste de tom), o cardápio rápido e os fios que costuram uma na outra. Lida nas ações 1, 2 e 3.
- `references/lancamento-e-esteira.md`: o lado lançamento da oferta e os funis de entrada de baixa fricção, incluindo o funil de aquecimento. Lida nas ações 4 e 5.
- `references/time-comercial.md`: a jogada de escala do time comercial, contexto de operação com equipe. Convive com o modo individual.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `shared-references/crivo/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `shared-references/crivo/07-regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com a lista fechada de contagens, uma por linha, exatamente nesta forma:

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

## A frase que a dona repetiria (fecho, uma por entrega)

Escolha a UMA frase da entrega que a dona repetiria de cor numa conversa, cole ela sozinha e responda por escrito por que ela sobrevive fora do contexto: sem a peça em volta, sem o nome do produto, sem a explicação que vem antes. Cole `frase que sobrevive fora do contexto: <literal>`. Correta e morna é o defeito comum aqui: a abertura que serve pra qualquer serviço do mesmo tipo não é a frase, é o preenchimento. Nenhuma frase significa que a peça está correta e não está viva, e a entrega volta pro passo de escrita.

## Passo 2 da checagem (fecho, roda por comando)

Depois de gravar todos os entregáveis, rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída. Ele exige o `conferencia/checagem-titulos.md` na pasta, confere o inventário (os 4 inteiros, o piso e o `inventário duplicado`), o universo dos títulos, o marcador acima de 6 palavras, o nome de conversa privada, a `saída do script reescrita` e o lint de todo `.md`, RELATO incluso. **`exit` diferente de 0 reprova a entrega inteira, antes da análise de conteúdo.**
