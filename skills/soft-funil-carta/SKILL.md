---
name: soft-funil-carta
description: >-
  Escreve a CARTA DE VENDAS em texto corrido, lida em silêncio, no arco atenção, diagnóstico, mecanismo e ação. Escala a carta de mini a longa, decidindo o comprimento pela consciência do leitor, pelo ticket e pela temperatura do tráfego. Use quando o pedido for: "escreve a carta", "carta de vendas", "carta longa", "mini-carta", "deixa a carta mais completa", "o texto que vende meu programa", "um texto pra mandar pro lead antes da call", "sales letter". NÃO use pra: o roteiro do vídeo de vendas, a VSL que o dono grava (soft-funil-vsl); "um vídeo de 10 minutos que vende" com filtro e virada (soft-funil-miniwebinar); página com hero, seções e botão repetido (soft-funil-landing); a régua pós-isca (soft-funil-nutricao); o lançamento com carrinho (soft-launch); carrossel, reel e headline solta (soft-conteudo-*); webinar (soft-webinar); isca (soft-funil-isca); a conversa de venda (soft-vendas-closer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Carta de vendas, o ativo que aquece antes da conversa

A carta faz o trabalho que a reunião fazia. Lida em silêncio, no celular. Ela filtra, explica e constrói desejo, e entrega o lead quente pro comercial. Ela não fecha a venda sozinha: ticket alto fecha na conversa, e a carta é o degrau que aquece e qualifica. Carta que tenta fechar sozinha vira discurso de vendedor e esfria o lead certo.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**O último capítulo, bloco ou seção carrega tese no título, como todos os outros.** `Resumo`, `Conclusão`, `Considerações finais`, `Fechamento` e `Recapitulando` são rótulos de estrutura e reprovam a régua. O lugar que o leitor lê por último recebe a frase mais concreta do material, jamais a mais geral. Cole `capítulos: N · com tese no título: N`, iguais.

**Saídas obrigatórias desta ação, no bloco de entrega** (linha por linha, e a ausência de qualquer uma reprova):
`mecanismo do problema: <nome> | substantivo trocado: <original> → <outro mercado> | sobrevive à troca de nicho? sim/não`
`mecanismo da solução: <nome>`
`convites na peça: N · com ação escrita: N · em marcador: 0`
`números não confirmados no perfil: N · publicados na peça: 0`

**Cada item da oferta é conferido contra o que a operação entrega hoje, e essa conferência é um PASSO com saída obrigatória, não uma recomendação.** Antes de escrever a lista do que está incluído, rode `grep -rniE '<cada item da lista de inclusos>' <insumos>` e cole a saída inteira. Todo item que aparecer numa reclamação, numa cobrança ou num registro de falha recebe uma decisão escrita, e são só duas: **sai da carta** (e a pergunta ao dono no handoff explica por quê) ou **fica na carta** (e o handoff traz `prometido na carta e em falha na operação: <item> · <arquivo:linha>`). Cole `itens da oferta: N · conferidos nos insumos: N · em falha: N · decididos: N`, com `decididos` igual a `em falha`. Carta que promete um item em falha sem nenhuma das duas decisões escritas reprova: a peça que promete o bônus que o cliente atual não está recebendo escreve a próxima reclamação.

**Número medido do perfil entra literal na prova.** Trocar um número medido por um vago (`dezenas`, `várias`, `muitas`) reprova, porque perde a prova sem ganhar ressalva. O vago só entra onde o perfil marca `[A CONFIRMAR`. Cole `provas na mensagem: N · com número literal do perfil: N · vagas: 0`.

**Número marcado `[A CONFIRMAR` no perfil não entra na peça, com ou sem ressalva ao lado.** Rode `grep -nE '\[A CONFIRMAR' <perfil>` e cole a saída. Para cada número que voltar, a peça usa a forma sem prazo (`depois de algumas semanas`, `ao longo do protocolo`) e o número fica só no arquivo de notas. **A ressalva ao lado do número não conserta o número**, ela documenta que ele foi publicado assim mesmo, e o leitor lê o número primeiro; registrar a pendência num arquivo à parte também não autoriza, porque quem lê a peça não abre as notas. Cole `números não confirmados no perfil: N · publicados na peça: 0`.

**O P.S. é UM, e traz um argumento que ainda não foi dito.** P.P.S. e P.P.P.S. que repetem preço, duração e data já ditos no corpo diluem o fecho e saem. E nenhum recado ao dono entra na carta: frase no imperativo dirigida a quem encomendou a peça (`confirme`, `verifique`, `ajuste antes de publicar`) mora no arquivo de notas, nunca no corpo que a leitora lê. Rode `grep -nE '^\*\*?P\.(P\.)*S' <a carta>` e cole a saída: mais de uma linha reprova.

**A prova sai inteira ou não sai, e o bastidor da decisão fica fora dela.** Frase do tipo `o nome e o prazo exato ficaram fora desta carta até serem confirmados` explica à leitora uma decisão editorial e enfraquece a prova que acabou de ser dada. A forma correta é a prova sem o dado incerto (`ao longo do protocolo`, `depois de algumas semanas`), e a pendência vive no arquivo de notas.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**A peça escala de comprimento.** O mesmo arco vai da mini-carta (4 a 7 minutos de leitura, 4 blocos enxutos, o modo mais usado) até a carta longa de resposta direta (15 a 25 minutos, com duplo mecanismo, empilhamento de valor, garantia, bônus, perguntas frequentes e o fecho). Mesma espinha, mesma função em qualquer tamanho.

**A fronteira que não pode vazar:** a carta é **texto corrido lido em silêncio**, uma promessa, um convite. A landing é arquitetura de página (hero, seções tituladas, vídeo embutido, botão repetido), e quem monta isso é a **soft-funil-landing**. Carta longa que ganha hero e botão repetido deixou de ser carta.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra o fluxo inteiro num caso fictício de nicho neutro: o briefing respondido, o diagnóstico de consciência com a linha declarada, a espinha nas 4 fases, um trecho da peça escrita e o que o gate reprovou. A **mini-carta completa e diagramada**, do começo ao fim, já está em `references/modo-mini-carta.md`, Seção 5, e é a peça de referência pra calibrar densidade e tom.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola tudo que tem sobre a oferta e o público e eu escrevo a carta). Se quiser ser guiado passo a passo (te pergunto o que preciso pra carta, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou. Se faltar um insumo que a carta não vive sem (a oferta, quem é o público, o convite pro 1:1), pergunta AQUELE insumo e segue, sem voltar pro briefing inteiro.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o briefing curto uma pergunta de cada vez, e monta a carta com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda a carta (o comprimento pela consciência, o lead, o duplo mecanismo, a garantia, o CTA único), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a calibrar sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("meu cliente quer resultado", "o público de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: a frase literal que um cliente falou na dor, um case real com número, o print de uma objeção. Verbatim real vira a âncora da carta; resposta rasa vira carta rasa. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar a carta, fecha com UMA linha: "Quer mais curta? Outro lead? Mais suave no fecho? Me diz o que ajustar que eu refaço só essa parte." A oferta de refino não substitui o STOP nem o gate.


## Contrato de saída (o que sai, e onde cai)

- **Um arquivo `.md` nomeado**, salvo no disco: `carta-<produto>.md` pra carta em texto, `roteiro-vsl-<produto>.md` pro vídeo. Se o ambiente renderizar markdown, mostre também. Nunca as duas peças sem o dono escolher.
- **A carta sai num de 3 comprimentos** (mini, média, longa), declarado na Ação 2 pela consciência, pelo ticket e pela temperatura. A longa carrega os blocos clássicos da resposta direta, mas continua carta: texto corrido, uma promessa, um convite.
- **O vídeo sai num de 3 modos** (curto, médio, profundo), com o destino comercial declarado antes da escrita: venda direta, aplicação/conversa, ou autoridade.
- **Preço na carta é decisão declarada, não default silencioso.** Quando o perfil traz o preço, a carta o imprime, com a ancoragem ao lado. A carta só omite o preço quando o dono pede, ou quando o destino é qualificação por conversa E o ticket passa do limiar de call 1:1; nesses dois casos a peça cola a linha `preço omitido por: <motivo> · origem da regra: <arquivo:linha>`. **Omissão sem essa linha reprova**: carta de vendas que constrói valor por dez blocos e manda perguntar o preço na conversa transfere para o canal manual do dono o trabalho que a carta existe pra fazer, e o dono que tem fila parada no WhatsApp paga essa transferência duas vezes. No vídeo, preço e convite obedecem ao destino comercial declarado.
- **Entrega etapa por etapa**, com parada pro OK a cada uma. Nunca despeja a carta inteira de primeira.
- **Nunca inventa fala, caso ou número.** Sem prova real, o trecho sai como `[A CONFIRMAR: prova]` e a peça não sai como pronta.
- **A carta é arquivo publicável e não tem seção de bastidor, nem marcada.** Pendência, substituição de link, decisão editorial e a nota do conselho profissional vão em `notas-confirmacao.md`, que já é entregue ao lado. Checagem antes de fechar: `grep -nE '^#+.*(dono|não publicar|nao publicar|bastidor)' <carta>` tem que voltar vazio, porque quem copia a carta pro editor copia o arquivo inteiro, e uma seção marcada como não publicável viaja junto.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "escreve a carta", "quero um texto que venda", sem dizer o formato | **1 · BRIEFING**, depois **2 · CALIBRAGEM** |
| "faz uma VSL", "roteiro de vídeo de vendas", "vídeo que vende" | **soft-funil-vsl**, que tem a fase de levantamento antes da escrita. Aqui o ramo do vídeo fica só como fallback, quando ela não está instalada |
| "mini-carta", "uma carta curta pra mandar antes da call" | **2** com comprimento já dado, depois **3** |
| "carta longa", "sales letter completa" | **1** com os 3 campos extras, depois **2** e **3** |
| "olha essa carta aqui e diz o que está errado" | **5 · GATE** em modo auditoria, devolve o diagnóstico por fase |

Pedido ambíguo ("preciso de um texto de vendas"): pergunte UMA coisa só, **"a pessoa vai ler ou vai assistir?"**, e a resposta separa os dois ramos.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de posicionamento, avatar, mecanismo nomeado, voz, oferta ou prova: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta do "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

**As 6 leis de operação** (detalhe em `shared-references/operacao-padrao.md`, Seção 0): (1) cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**; (6) **doc de saída enxuto pros 2 leitores**, zero meta-narração, só o insumo denso mais `[A CONFIRMAR]` onde falta.

---

## Ação 0 · ANCORAGEM (roda antes de tudo, não pula)

**O que faz:** abre a fonte de fala real e puxa a matéria-prima da primeira linha e da prova.

**Precisa de:** a fonte, nesta ordem: descrição do projeto → posicionamento do dono → mensagens anteriores. De lá saem **3 a 5 falas de DOR e 3 a 5 de DESEJO**, literais, com o N. A atenção (a primeira linha) nasce de uma delas, quase intacta.

**Sem o insumo:** três estados, declare o seu em 1 linha.
- **Tem fala real com N:** ancora nela e cita o N.
- **Tem nicho e prova, zero fala literal:** não invente. Ancore em prova real do dono. Número não confirmado vira `[A CONFIRMAR: número]`; caso que não existe vira `[A CONFIRMAR: caso]`.
- **Sem nada:** pergunte numa mensagem só (nicho em 1 linha, 1 dor real, o ticket) e siga.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**O convite nunca sai em marcador, e ele é a linha que a peça inteira serve.** O texto do convite vem, nesta ordem: (1) da ação que o dono já usa nos insumos, achada por `grep -rniE 'manda |chama |responde |comenta |envia ' <insumos>` com a saída colada; (2) da ação nativa do canal principal do perfil; (3) do convite ao evento datado. Sem nenhuma das três, sai na forma que dispensa o link (`me chama no WhatsApp e eu te mando o link`), nunca em marcador. **Campo de template e marcador de pendência são coisas diferentes:** `[LINK]`, campo de uma palavra no FIM da linha e substituível por colagem, fica na frase; `[A CONFIRMAR: link]` é pendência, mora no bloco de configuração e no handoff, nunca no meio da linha que o lead lê. Cole `convites na peça: N · com ação escrita: N · em marcador: 0` e `toques com marcador ocupando linha do corpo: 0`.

**Entrega:** nada de arquivo. É a matéria-prima das ações 3 e 4.

**Leia primeiro:** `shared-references/crivo/01-entrada-verbatim.md`.

---

## Ação 1 · BRIEFING (num bloco só, e espera resposta)

**O que faz:** junta o insumo que sustenta a carta.

**Precisa de:** os 6 campos base. Se veio do posicionamento com os dados, confirme em 1 linha e pule.

**Os 6 campos base (valem pra QUALQUER comprimento):**
- **(a)** cliente ideal específico (nicho, porte, situação, maturidade)
- **(b)** o problema avançado nomeado, nas palavras do cliente, não em jargão
- **(c)** 3 a 5 soluções comuns que ele já tentou, mais o efeito colateral de cada uma
- **(d)** o mecanismo nomeado e suas 3 ou 4 etapas
- **(e)** 1 a 3 casos reais (nome ou perfil, nicho, número, prazo, só verdade documentável)
- **(f)** a oferta e o ticket (com o preço do perfil na mão: ele entra na peça, e a omissão é que precisa de motivo declarado)

**Os 3 campos EXTRAS, que SÓ a carta longa usa.** Não pergunte estes numa mini-carta; eles alimentam os blocos de resposta direta e a ausência deles **desce** a peça pra média ou mini.
- **(g)** o **mecanismo do problema**, a causa-raiz oculta que exonera o leitor ("não é falta de X, é Y"), distinta do mecanismo da solução do item (d). Exemplo fictício, consultoria de gestão: o item (d) é o método "Mapa de Margem"; o item (g) é a causa-raiz, "o seu lucro some porque a precificação segue a planilha do contador, não a percepção de valor do cliente".

**O nome do mecanismo do problema passa pelo teste do nicho trocado, como qualquer título.** Cole `mecanismo do problema: <nome> | substantivo trocado: <original> → <outro mercado> | sobrevive à troca de nicho? sim/não`. **`sim` volta pro passo de nomear**, porque um mecanismo que serve pra qualquer mercado não explica este: "recomeço acelerado" sobrevive trocando treino por dieta, por estudo e por carreira, e por isso não é mecanismo, é rótulo. O nome sai do substantivo concreto do caso (o dia 12, o joelho que decide, os 78 que sumiram), nunca do adjetivo do comportamento.
- **(h)** os elementos de **reversão de risco** (a garantia que o dono topa dar de verdade) mais os **bônus reais**, cada um mirando UMA objeção nominal (tempo, dúvida técnica, medo de não conseguir sozinho).
- **(i)** a **razão honesta de urgência**, se existir (vagas da turma, preço que sobe, janela de início), só se for verdade.

**Sem o insumo:** sem (a), (b), (d) e (f) a carta não avança. **PARA e espera.** Faltando (g), (h) ou (i), a peça **desce** de comprimento; nunca invente garantia, bônus ou urgência plausível: o que não existe vira `[A CONFIRMAR]` ou some.

**Entrega:** nada de arquivo. É o que alimenta a calibragem.

**Leia primeiro:** `references/discurso-base-7-passos.md` (o andaime entre o briefing e as 4 fases).

---

## Ação 2 · CALIBRAGEM (formato, destino, consciência, comprimento)

**O que faz:** lê o leitor e declara, numa linha só, tudo que decide a escrita.

**Precisa de:** o briefing da Ação 1 · o nível de consciência do leitor · a temperatura do tráfego.

**Sem o insumo:** sem o dado de consciência, **PARA e pergunte só isso**: "quem vai ler isso já sabe que tem esse problema, já sabe que existe solução, ou já te conhece?". Sem temperatura declarada, assuma **frio** (o caso mais exigente) e declare a premissa em 1 linha.

**Entrega:** 1 linha declarada antes de escrever: `formato X → destino Y → consciência Z → lead W → comprimento Q`. **STOP.**

**Leia primeiro:** `references/anatomia-carta-longa.md`, Seções 2 e 3 (consciência e leads) pro ramo da carta · `references/vsl-script.md` pro ramo do vídeo.

**Profundidade:** `references/blocos-copy.md`.

### 2.1 · Carta ou vídeo

**O roteiro de vídeo de vendas migrou pra `soft-funil-vsl`.** Ela levanta a munição (avatar, consciência, USP, mecanismo, oferta, provas, objeções) antes de escrever a primeira linha, e esta skill não faz isso. Pedido de VSL vai pra lá. O ramo do vídeo que segue abaixo continua aqui como fallback, pra quando a `soft-funil-vsl` não estiver instalada; nesse caso, diga em 1 linha que a fase de levantamento ficou de fora.

Não são fases, são formatos paralelos na mesma espinha. Texto favorece leitura silenciosa e edição rápida; vídeo favorece presença, demonstração e argumento falado. Escolha pelo comportamento de consumo e pela força do dono na câmera.

### 2.2 · No ramo do VÍDEO, declare o destino comercial

| Destino comercial | Preço e oferta | Convite único |
|---|---|---|
| **Venda direta** | oferta completa, preço, condição e garantia reais entram | checkout |
| **Aplicação ou conversa** | oferta entra; o preço do perfil entra também, e só sai com a linha `preço omitido por: <motivo> · origem da regra: <arquivo:linha>` | formulário, agenda ou conversa |
| **Autoridade** | explica problema, mecanismo e prova; não simula fechamento | aplicação ou conversa |

E a profundidade. **Ticket sozinho não decide duração.**

| Modo | Duração-alvo | Use quando |
|---|---:|---|
| **Curto** | 7 a 12 min | público quente ou consciente, mecanismo simples, pouca crença a mudar |
| **Médio** | 12 a 25 min | tráfego frio, diagnóstico necessário, mecanismo novo, prova moderada |
| **Profundo** | 25 a 35 min | baixa consciência, mecanismo complexo, várias crenças e objeções, prova robusta |

**Acima de 35 minutos, a régua exige uma referência vencedora.** Referência vencedora é uma peça do mesmo nicho, na mesma faixa de ticket, que **rodou com verba e converteu**, e que o dono consegue mostrar. Como validar, na ordem: (1) o dono manda o link ou a gravação; (2) ele diz por quanto tempo ela rodou e com que verba; (3) ele diz o número que ela devolveu (custo por lead ou por venda). Sem essas três respostas, não é referência vencedora, é uma peça longa que alguém viu. Nesse caso a peça desce pro modo profundo de 35 minutos e você diz isso em 1 linha. Nunca alongue por prestígio.

### 2.3 · No ramo da CARTA, cruze consciência com comprimento

| Consciência do leitor | A carta abre por | Comprimento |
|---|---|---|
| **Inconsciente** (nem sabe que tem o problema) | a cena e o mecanismo do problema | longa |
| **Consciente do problema** (sente a dor, não sabe a saída) | a cena mais o mecanismo que exonera | longa |
| **Consciente da solução** (sabe que existe saída, compara) | a diferença e a prova | média |
| **Consciente do produto** (já te conhece, hesita) | a promessa direta e o diferencial nomeado | média ou mini |
| **Mais consciente** (só falta a oferta) | a oferta e a promessa direta | mini basta |

E o lead que casa com cada uma:

| Consciência | Lead |
|---|---|
| Inconsciente | história ou proclamação |
| Consciente do problema | grande segredo ou problema e solução |
| Consciente da solução | problema e solução, ou promessa |
| Consciente do produto | promessa direta |
| Mais consciente | a oferta na cara |

**Regra do comprimento:** quanto menos consciente o leitor, maior o ticket e mais frio o tráfego, mais longa a carta. Exemplo fictício (nutrição esportiva): tráfego frio de anúncio, ticket de 6 mil de acompanhamento, público que acha que "é só comer menos" (inconsciente do mecanismo) resulta em carta longa com lead de história. Já a base quente que já fez consulta avulsa resulta em mini com lead de oferta.

Mantenha **uma coisa só** em qualquer comprimento: uma ideia central, uma emoção dominante, um benefício-promessa, uma ação no fim.

---

## Ação 3 · ESPINHA (o arco, em texto corrido, ainda em bastidor)

**O que faz:** escreve a peça inteira como uma fala corrida na voz do cliente, seguindo o arco.

**Precisa de:** o briefing, a linha declarada da Ação 2 e as falas da Ação 0.

**Sem o insumo:** sem o mecanismo do problema, a peça desce pra média e você escreve só o mecanismo da solução, dizendo isso em 1 linha.

**Entrega:** a espinha nas 4 fases, mostrada pro dono. **STOP.**

**Leia primeiro:** `references/anatomia-carta-longa.md` (a ordem dos blocos e como cada um se aninha na fase) · `references/blocos-copy.md` (a copy de cada bloco).

**Profundidade:** `references/discurso-base-7-passos.md` · `references/conducao-na-pratica.md`.

| Fase | O que faz | Fecha em |
|---|---|---|
| **Atenção** | espelha o cliente certo na situação concreta dele, promete o que ele vai entender, filtra quem não é | reconhecimento ("isso fala comigo") |
| **Diagnóstico** | nomeia o problema avançado, lista as soluções tentadas e o efeito de cada uma, exonera ("não é falta de esforço, é arquitetura") | o inimigo-categoria nomeado, que é sistema ou prática, nunca pessoa |
| **Mecanismo** | a virada por contraste ("o mercado faz X, isto faz Y, porque Z"), o método nomeado com a função de cada etapa, a prova real | um número ou caso concreto |
| **Ação** | a oferta sem virar discurso de vendedor, o filtro de para quem não é, e o destino comercial declarado | um convite único |

**Desejo antes da oferta.** A ação só funciona se o diagnóstico e o mecanismo já construíram o desejo. Oferta colada na abertura, pulando as duas fases do meio, é outro arco disfarçado. Refaz.

**Explore o problema a fundo.** O diagnóstico é a fase mais longa e é onde a carta ganha ou perde: traz o problema avançado, as soluções já tentadas e o efeito de cada uma, com cena e número, até o leitor pensar "é exatamente isso que eu vivo". Carta que corre o problema pra chegar logo na oferta não constrói desejo.

**Mostra a função, nunca a receita.** Entregar o passo a passo executável mata a venda.

**Quando o comprimento é longo**, cada fase ganha músculo, sem virar landing. Os blocos de resposta direta não são blocos novos fora do arco: cada um mora dentro de uma fase.

| Fase | Na longa carrega |
|---|---|
| **Atenção** | o lead escolhido na Ação 2, mais headline, pré-headline e sub-headline |
| **Diagnóstico** | a agitação da dor, a história de origem e o **mecanismo do problema** (o item (g) do briefing) |
| **Mecanismo** | o **mecanismo da solução** nomeado, o produto como encarnação dele, o empilhamento de prova e o empilhamento de benefício |
| **Ação** | a oferta, o empilhamento de valor ancorado, a reversão de risco, os bônus, a urgência honesta, as perguntas frequentes, o fecho e o pós-escrito |

**Antes de escrever a cena de abertura, rode o passo de nomes.** A abertura é onde a pessoa citada se reconhece, e o pior leitor possível é ela mesma. Rode antes de escrever a primeira linha:

```
python3 scripts/checar_titulos.py --peca <a carta> \
  --insumos <pasta de insumos do dono> --perfil <perfil do dono>
```

Ele imprime `nomes candidatos achados pelo script: N` e, por nome, `autorização no insumo: sim/não` e `mensagem privada: sim/não`. **Nome com `mensagem privada: sim` e `autorização: não` sai da carta**, e a forma por faixa toma o lugar ("uma aluna na casa dos 50"). Lead que escreveu uma pergunta e ainda não teve resposta nunca vira cena de abertura: ela leria a própria pergunta virada em copy. Cole `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada: 0`.

**A prova entra por resultado, nunca por tempo de casa.** "Nove anos de atendimento online" mede o vendedor, não o que a leitora ganha. Cada bloco de prova carrega o resultado concreto de uma aluna (o que mudou, em quanto tempo, medido em coisa que ela faz). Cole `blocos de prova: N · com resultado concreto de aluna: N · com atributo do dono: N`, e **a terceira coluna maior que a segunda volta pro passo de escrita**.

**O duplo mecanismo é a marca da longa:** o do problema (no diagnóstico, exonera) vem antes do da solução (no mecanismo, a chave proprietária nomeada). Sem o primeiro, a promessa nova colide com a decepção que o leitor já carrega das tentativas passadas.

---

## Ação 4 · DIAGRAMAÇÃO ou ROTEIRO (a peça final)

**O que faz:** transforma a espinha na peça pronta pra publicar ou pra gravar.

**Precisa de:** a espinha aprovada na Ação 3.

**Sem o insumo:** não há diagramação sem espinha aprovada.

**Entrega:** `carta-<produto>.md` ou `roteiro-vsl-<produto>.md`, salvo no disco. Se o ambiente renderizar markdown, mostre também. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/modo-mini-carta.md` (a diagramação, a tabela de quando usar cada elemento visual e o exemplo completo da Seção 5) pro ramo da carta · `references/vsl-script.md` (os 8 blocos, a distribuição de tempo, as fórmulas de gancho) pro ramo do vídeo.

**Profundidade:** `references/tom-e-ritmo-desejo.md` (as 7 categorias de corte, na revisão de densidade).

### No ramo da CARTA

Fica entre a carta pura e a página de vendas. Quebra a espinha nas 4 fases pra **leitura solitária**, com uma virada de ritmo ou de ângulo a cada bloco, e uma quebra visual (destaque, frase isolada, separador, número grande, espaço em branco) pra a página respirar no celular. Parágrafos de 1 a 3 linhas. Frase isolada só em alto impacto. Pergunta retórica curta a cada 3 a 5 parágrafos. Zero subtítulo dentro de fase. Tom escrito coloquial, não fala transcrita.

**Leitura solitária não perdoa.** No vídeo a narração puxa o espectador de uma frase pra outra; na carta o leitor está só com o texto e fecha a aba na primeira frase fraca. Cada frase puxa a próxima, sem folga.

**Na carta LONGA**, o mesmo texto corrido, com a descida escorregadia ponta a ponta: a primeira frase é curtíssima e existe só pra puxar a segunda; no fim de cada bloco planta uma semente de curiosidade tirada da cena concreta, nunca de fórmula vazia; os primeiros parágrafos criam o ambiente de leitura (o leitor concorda com coisas pequenas e óbvias antes de discordar de nada). **Densidade na longa:** o alvo não é cortar até um número de palavras, é cortar gordura mantendo cada bloco que faz trabalho de objeção. Corta a frase que não puxa a próxima, nunca o bloco que abre uma objeção real. **O pós-escrito é o segundo texto mais lido da carta:** carrega oferta, garantia e urgência comprimidas, pra quem rolou direto pro fim.

### No ramo do VÍDEO

Monta os 8 blocos: gancho, empatia e justificativa da falha, inimigo-categoria, procedência, método, prova, oferta e convite. O curto comprime cada bloco; o médio desenvolve diagnóstico, mecanismo e prova; o profundo aprofunda mudanças de crença, objeções e demonstrações sem repetir argumento.
- **Polaridade alta:** a abertura desafia uma crença específica nos primeiros 30 segundos.
- **O destino comercial manda no fecho:** venda direta inclui preço e termina em checkout; aplicação termina no canal escolhido; autoridade não finge venda direta.
- **A página que hospeda o vídeo é outro entregável.** Aqui sai o roteiro e, no máximo, o briefing da página. A arquitetura é da **soft-funil-landing**.

**Densidade nos dois ramos:** cada frase carrega ideia ou função. Corta de 30% a 40% na revisão.

---

## Ação 5 · O GATE (roda por dentro, e não imprime)

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Rótulo de seção não é título, e a coluna diz qual é qual.** Classifique cada título de seção da carta como `rótulo` ou `tese`, numa coluna própria da checagem. Rótulo nomeia o assunto e não afirma nada (`Resumo`, `A oferta`, `O método`, `Perguntas frequentes`); tese afirma alguma coisa que o leitor pode discordar (`O que você paga hoje sem perceber`). O título de seção da carta é a primeira coisa que o leitor lê antes de decidir se continua, e um documento de rótulos não segura ninguém. Cole a coluna inteira, um por linha, na forma `<título> | rótulo ou tese`, e **todo `rótulo` volta pro passo de escrita** antes de a peça sair. Feche com `títulos de seção: N · em tese: N · rótulos restantes: 0`.

**O marcador é campo, e campo tem tamanho.** Na carta o marcador cabe em `[A CONFIRMAR: <o dado>]`, no máximo 6 palavras, depois de um rótulo e no fim da linha. **O porquê da pendência nunca entra na peça**, vai pro handoff com o número da linha ao lado. O script conta e reprova acima do teto, na linha `marcadores acima de 6 palavras: N (teto 0)`.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** **A classificação vale para a FALA, não só para o nome:** anonimizar resolve a identidade e não resolve a origem, e uma frase literal vinda de call ou de caixa de entrada continua sendo conversa privada mesmo sem nome. Liste as falas atribuídas a terceiros na peça, uma por linha, na forma `<fala literal> | origem: <arquivo:linha> | classe: prova declarada ou conversa privada | como aparece na peça: <"uma aluna", "uma seguidora", "alguém que me procurou">`. Fala de conversa privada com pessoa em negociação aberta só entra como "alguém que me procurou" ou equivalente que não afirme compra; "uma aluna", "uma cliente" e "antes de entrar" afirmam a compra e reprovam. Feche com `falas de terceiro na peça: N · de conversa privada apresentadas como aluna: 0`. Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**A chamada da persona nunca leva nome real.** Persona, avatar, persona-âncora, cena-assinatura e célula do Mapa de Munição são peça pública, mesmo dentro de um documento de estratégia: é deles que nascem as capas dos meses seguintes. Rode `grep -rn 'autorizado por' <insumos>`; **saída vazia proíbe nome próprio de pessoa real em qualquer um desses cinco lugares.** A persona sai por idade, profissão e situação (`55, contadora, operou o menisco`). Quando o texto precisar mesmo de um nome pra chamar a pessoa, **use um nome inventado e diga na mesma linha que é inventado**: `Marta (nome inventado), 55, contadora`. **Lead com negociação em aberto na caixa de entrada nunca vira persona-âncora**: ela é a primeira a ler a peça e vai encontrar a própria transcrição virada em avatar. Feche com `personas na peça: N · com nome inventado declarado: N · com nome real dos insumos: 0`.

**Palavra-chave de CTA não se inventa, e a grafia é literal.** Antes de escrever qualquer CTA que peça uma palavra ("manda X no Direct", "comenta Y", "envia Z no WhatsApp"), procure a palavra nos insumos do dono (transcrição, peça pronta, mensagem, site) e cole `palavra-chave: <literal> | origem: <arquivo:linha>`. Use a grafia EXATA, sem espaço a mais nem a menos: uma palavra com espaço é outra palavra para quem digita e para a automação que responde, e a lead cai em lugar nenhum. **Sem origem no disco, é PROIBIDO escolher uma:** escreva o CTA na versão que dispensa a palavra ("me chama no Direct e eu te mando") e leve a pergunta ao handoff. Marcar a incerteza no relato e publicar a palavra assim mesmo reprova, porque o dono publica sem perceber.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **A linha de fechamento tem forma fixa e não admite qualificador entre parênteses:** `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0`. Escrever `Dados fornecidos (relevantes à carta)`, `(considerados para esta peça)` ou qualquer recorte equivalente reprova a entrega, **porque o universo é o perfil inteiro e a relevância decide a coluna `usado` ou `descartado`, nunca a existência da linha.** Cole antes dela o piso: `Piso do inventário: N (campos: X + valores compostos: Y)`, com o comando `grep -c '^- ' <perfil>` e a saída literal ao lado. `Dados fornecidos` menor que o piso reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


**O que faz:** reprova a peça que não serve, antes de o dono ver. Serve também como modo auditoria, quando o dono cola uma carta pronta.

**Precisa de:** a peça escrita.

**Entrega:** nada em modo normal (auditoria silenciosa, a tabela **nunca** vai pra saída). Em modo auditoria, entrega `diagnostico-carta.md` com a fase, o check que falhou e a correção.

**Checagem de pessoa gramatical.** A carta é escrita na voz do dono, em primeira pessoa, falando com a leitora em segunda. Conte as menções ao dono em terceira pessoa no corpo da carta (o nome dele, o nome do negócio como sujeito, "ela vai te explicar") e cole `menções ao dono em terceira pessoa: N (teto 2, e nenhuma no CTA)`. Acima do teto, ou uma que seja no bloco do próximo passo, reprova: **quem convida para uma conversa não fala de si como de outra pessoa**, e a carta é a peça mais pessoal do funil. Carta correta, legível e institucional faz a leitora ler sobre um serviço em vez de ouvir alguém.

**Leia primeiro:** `shared-references/crivo/03-gate-cub.md`.

**Profundidade:** `references/tom-e-ritmo-desejo.md` · `shared-references/filtro-anti-ia/padroes-banidos.md` e `falsos-positivos.md`.

Antes do gate, confira os 5 movimentos (sonhos, falhas, medos, desconfianças, inimigo) como pré-filtro; se algum estiver ausente, reforça antes de auditar. Detalhe em `references/vsl-script.md`. O veredito final é do gate.

**O veredito é o PIOR item.** Um ✗ refaz o trecho que falhou.

| Check | Passa se |
|---|---|
| **Ancorada** | nasce de fala literal da fonte (cita o N **real**) ou de prova real do dono. N inventado reprova na hora. Cada fase fecha em chão (número, caso, mecanismo), não em tese solta |
| **O arco certo** | as 4 fases na ordem, identificáveis. Oferta colada na abertura, pulando diagnóstico e mecanismo, reprova |
| **Desejo antes da oferta** | o mecanismo construiu o desejo antes do convite |
| **Prova real do dono** | todo caso e número é verdade documentável. Sem prova, o trecho está como `[A CONFIRMAR: prova]` e a peça não sai como pronta |
| **Consciência casada** (média e longa) | a peça declara o nível da Ação 2 e a abertura bate com ele. *Não se aplica na mini* |
| **Duplo mecanismo** (média e longa) | existe o mecanismo do problema antes do da solução; mecanismo só rotulado, sem nome próprio, reprova. *Não se aplica na mini* |
| **Prova à altura da alegação** (média e longa) | toda alegação grande tem prova do lado, e a longa empilha prova variada. *Não se aplica na mini* |
| **C/U/B** | não **C**onfuso (uma ideia por frase, o leitor não relê), não **I**nacreditável (promessa menor mais prova), não **B**oring (cada frase puxa a próxima) |
| **Mostra função, não receita** | mostra a função das etapas, zero passo a passo executável que dispensa o dono |
| **Convite único e coerente** | UM convite compatível com o destino declarado. Múltiplos destinos reprova |
| **Preço coerente** | o preço que o perfil traz aparece na carta, ou a peça cola `preço omitido por: <motivo> · origem da regra: <arquivo:linha>`, e regra citada que não exista no SKILL.md reprova; o vídeo de venda direta mostra preço e condições reais; o de aplicação só mostra se a decisão foi dada; o de autoridade não inventa oferta |
| **Dá pra ver** | fecha o olho e enxerga a cena. Reprova "tenha mais clareza". Passa "a recepcionista diz: semana que vem enche" |
| **Dá pra falsificar** | é fato falsificável, não adjetivo |
| **Só você diz** | o concorrente direto não assina igual |
| **Teste único** | o cliente certo pensa "isso fala comigo" na primeira linha e "finalmente alguém que entende" no fim |
| **Convite com destino** | aponta pra um destino real e nomeado, não pro vácuo |
| **Anti-IA (duro)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz (o verbo que rima com "cravar" e as flexões dele; exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ refaz. Só tudo ✓ vai pro dono |

Com shell disponível, rode o lint de copy em `scripts/lint_copy.py` sobre o arquivo. Sem shell, faça a busca manual pelos dois bloqueios duros antes de marcar o anti-IA.

---

## Ação 6 · FECHO (mostra e para)

**O que faz:** entrega a peça limpa e o comentário de publicação.

**Entrega:** só a peça (ou a etapa pronta), sem tabela de gate, sem meta, mais uma linha sobre como publicar (onde colar e como configurar o link). Pergunta "essa te serve? ajusto?" e **espera o OK** antes de seguir pra próxima etapa ou variação.

**Prova forte descartada se declara na própria peça.** Se um caso, depoimento ou número de prova REAL do dono existia e ficou de fora, declare em 1 linha na própria entrega por quê. O dono precisa ver a ausência sem abrir o relato de processo: prova omitida em silêncio vira carta fria sem que ele saiba o motivo. Checagem verificável antes de fechar: liste as provas reais disponíveis, uma por linha, na forma `<prova> | usada em <bloco> ou descartada porque <motivo>`, e confirme que todo descarte tem a linha correspondente dentro da entrega, não só no relato. Cautela sua, não pedida pelo dono, é motivo válido, e é exatamente o que ele precisa ler pra discordar.

---

## O que esta skill NÃO faz

Cada rota é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Página de vendas com hero, seções e botão repetido | **soft-funil-landing** | entrego a carta em texto corrido e o briefing da página |
| Carrossel, reel, stories | **soft-conteudo-*** | não faço |
| Headline ou gancho isolado | **soft-conteudo-headlines** | escrevo a primeira linha dentro da fase de atenção |
| Roteiro de VSL, o vídeo de vendas que o dono grava | **soft-funil-vsl** | rodo o ramo do vídeo desta skill, sem a fase de levantamento que ela tem, e digo isso em 1 linha |
| Mini-webinar em vídeo | **soft-funil-miniwebinar** | escrevo o roteiro como vídeo curto de autoridade |
| Webinar completo ou perpétuo | **soft-webinar** | não faço |
| Isca, material gratuito, artigo-isca | **soft-funil-isca** | não faço |
| A régua de mensagens que entrega a carta | **soft-funil-nutricao** | escrevo a mensagem de passagem, e mais nada |
| Script da conversa de venda, objeção ao vivo | **soft-vendas-closer** | escrevo o convite, não a conversa |
| Posicionamento, oferta, nomear mecanismo | **soft-plano-posicionamento** | uso os 6 campos base do briefing |
| Arte, visual, PNG | **soft-designer** | entrego o `.md` diagramado, sem o visual |

## Anti-patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Despejou a carta inteira de primeira | Volta: briefing, espinha, carta, auditoria, parando a cada etapa |
| Montou no arco de gatilho, não no de diagnóstico | Reescreve: o diagnóstico nomeia o inimigo, o mecanismo constrói o desejo, só então o convite |
| Oferta colada na abertura | Insere diagnóstico e mecanismo antes do convite |
| Inventou um caso ou número plausível | Só prova real. Sem fonte, `[A CONFIRMAR: prova]` e a peça não sai como pronta |
| Carta tenta fechar a venda sozinha | É o degrau que aquece e filtra. O fechamento é a conversa. Preço fora da peça, salvo ticket baixo |
| Múltiplos convites | Escolhe UM destino comercial e fecha nele |
| Vídeo profundo sem razão pra ser longo | A profundidade vem de consciência, complexidade, objeções e prova, nunca do desejo de parecer completo |
| Passou de 35 minutos sem referência vencedora validada | Sem link, verba e número, não é referência. Desce pro teto de 35 |
| Preço e convite contradizem o destino | Venda direta leva a checkout; aplicação leva ao canal; autoridade não simula fechamento |
| Entregou o passo a passo executável | Mostra a função das etapas, não o como que dispensa o dono |
| Carta bonita mas genérica | Falha em "só você diz". Reescreve com cena ou mecanismo proprietário |
| Narrou o fluxo ("agora vou diagramar") | Executa em silêncio e entrega o resultado |
| Imprimiu a tabela do gate | O gate é interno |
| Carta longa virou página de vendas | É carta: texto corrido, leitura solitária, um convite. Arquitetura de página é a soft-funil-landing |
| Inflou pra longa sem consciência fria nem ticket que justifique | O comprimento sai da Ação 2, não do gosto |
| Pôs o mecanismo da solução e pulou o do problema | Na longa, exonera primeiro e só então entrega a chave |
| Garantia genérica ou urgência fabricada | Garantia específica e ousada; urgência só se a razão existe. Escassez falsa queima a confiança construída |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o fluxo inteiro num caso fictício) · `references/modo-mini-carta.md` (a diagramação e a **mini-carta completa da Seção 5**, a peça de referência) · `references/anatomia-carta-longa.md` (a estrutura da longa sobre o arco) · `references/blocos-copy.md` (a copy de cada bloco) · `references/vsl-script.md` (os 3 modos de vídeo, os 8 blocos, o tempo) · `references/discurso-base-7-passos.md` (o andaime do briefing pras 4 fases) · `references/tom-e-ritmo-desejo.md` (as 7 categorias de corte) · `references/conducao-na-pratica.md` · `shared-references/operacao-padrao.md`, `crivo/`, `filtro-anti-ia/` · `scripts/lint_copy.py`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
