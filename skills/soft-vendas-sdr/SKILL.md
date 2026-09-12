---
name: soft-vendas-sdr
description: >-
  Monta e opera o agente comercial de IA do TOPO do funil, que abre a conversa, qualifica o lead e agenda a reunião no WhatsApp ou no CRM, e escreve as peças de topo. Use quando o pedido for: "monta meu SDR de IA", "agente de WhatsApp", "atendente 24 horas", "qualificar lead", "agendar reunião", "abordagem de DM", "follow-up automático", "recuperar carrinho", "conectar o CRM", "responde o lead que chegou na DM". NÃO use pra: priorizar a caixa cheia, antes da conversa começar (soft-atendimento-triagem); reclamação de quem já comprou (soft-atendimento-reclamacao); abordar quem NUNCA ouviu falar de você, lista fria (soft-vendas-outreach); preparar a call já marcada (soft-vendas-call-prep); o pacote do kit (soft-sdr-kit); conversa quente, objeção, pedir o sim (soft-vendas-closer); a campanha do mês (soft-vendas-estrategias); a proposta em site (soft-vendas-proposta); contrato (soft-vendas-contratos); posicionamento (soft-plano-posicionamento). Leia e siga o fluxo inteiro do SKILL.md.
---

# O agente comercial de topo: abre, qualifica, agenda

Esta skill monta e opera um agente comercial de IA que atende o lead 24 horas no canal do dono, classifica o estado dele, conduz a qualificação com a voz do dono e entrega o lead quente pronto pra quem fecha. Quando o pedido é só uma peça escrita (abordagem de DM, sequência de qualificação, convite de sessão), ela entrega essa peça num documento pronto pra copiar. O resultado é sempre um arquivo nomeado: ou o agente rodando com o doc de operação ao lado, ou a peça de topo em `.md`.

**A skill confere que é ela mesma, antes da primeira linha do fluxo.** As quatro skills de venda são vizinhas e se confundem: uma execução leu a pasta da vizinha, concluiu que esta skill não existia, rodou a outra, e entregou 2 arquivos onde o contrato pede 8, sem `conferencia/checagem-titulos.md`. A PRIMEIRA linha do fluxo é `head -3 SKILL.md` da pasta indicada, e você cola `SKILL.md lido: <caminho literal> · nome no frontmatter: <nome>`. **Nome diferente do que o dono pediu PARA tudo** e reporta que a skill pedida não está no catálogo desta sessão, em vez de rodar a vizinha: contratos de saída diferentes produzem entrega incompleta que parece completa.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Toda mensagem que o lead recebe sai em bloco, uma por bloco.** O que está no bloco cercado é o que vai colado no WhatsApp, e nada mais: as instruções de fluxo (`Se ela disser que é agora:`) ficam FORA do bloco. Horário, dia e janela são chutados e avisados em uma linha, nunca `[HORÁRIO]` vazio no molde. Cabeçalho de peça de mensagem afirma o que a mensagem faz, nunca o nome do molde (`## A primeira mensagem responde a dúvida antes de perguntar`, e não `## Molde da abertura`). Cole `mensagens na peça: N · em bloco: N`, iguais.

**`--exige` por ação (a conferência cobra os arquivos daquela ação).** Rode `--conferir <pasta> --exige <lista>` com a linha da ação que você entregou. Arquivo da lista ausente na pasta sai com exit 1 e `arquivo exigido pela ação ausente: <nome>`. Entregar 2 das 7 ações num pedido de pacote é entrega incompleta, não escopo reduzido: se você achar que o dono quis menos, entregue tudo e diga em 1 linha o que achou.

| Ação | `--exige` |
|---|---|
| 1 OBJETIVO | `01-operacao-agente.md` |
| 2 ONBOARDING | `01-operacao-agente.md,precos.json,wiki/*` |
| 3 CANAL | `01-operacao-agente.md` |
| 4 MOTOR | `02-prompt-agente.md` |
| 5 GATE | `01-operacao-agente.md` |
| 6 SUBIDA | `03-relatorio-subida.md` |
| 7 PEÇA DE TOPO | `04-pecas-de-topo.md` |
| pacote (o agente inteiro) | `01-operacao-agente.md,02-prompt-agente.md,03-relatorio-subida.md,precos.json` |

**A mensagem promete ato, nunca processo.** Rode `grep -niE 'apurar|apurando|verificar|analisar|definição|retorno|posicionamento|alinhar' <mensagem>` e cole a saída, inclusive vazia. `eu ainda estou apurando` e `te dar uma definição ainda hoje` contam ao lead o trabalho interno do dono, que não é o que ele pediu pra saber. Troque cada ocorrência por um ato com sujeito e hora (`eu volto a te responder hoje à noite`), ou tire a frase. Cole `palavras de processo na mensagem: 0`.

**Leitura em voz alta, por mensagem, com o resultado colado.** Toda mensagem que o lead recebe passa pela leitura em voz alta antes de sair. Cole `molde N | lida em voz alta: passa/tropeça | onde tropeça: <trecho>` pra cada mensagem da sequência, e feche com `lida em voz alta: sim · frase junta afirmação e pergunta: 0`. Frase que emenda uma afirmação e uma pergunta direta na mesma oração tropeça por construção, e a cura é quebrar em duas: `vi que você baixou o guia e o que mais te fez baixar logo esse foi o quê?` junta as duas e tropeça na leitura em voz alta. A abertura é a única linha do agente sem segunda chance: escreva primeiro e releia por último.

**Capacidade negada no perfil é fato, nunca lacuna a interpretar.** Antes de escolher a mecânica do CTA, rode `grep -in 'automação\|automacao\|robô\|bot' <perfil do dono>` e cole a saída literal. Linha que diz `nenhuma automação` responde `não`, e ela não é omissão nem falso positivo a contornar. Cole `mecânica exige automação? sim/não · perfil declara: <a linha literal> · mecânica adaptada: <qual>`. Negação no perfil sai como CTA sem robô, e manter a mecânica por leitura funcional, herança de outra plataforma ou hábito presumido reprova a peça.

**Cada linha da mensagem curta carrega algo que a anterior não carrega.** Antes de fechar, releia as linhas e corte a que só reformula a de cima; numa mensagem de três linhas, repetição é metade da peça.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra, num caso fictício de nicho neutro, a entrada que o dono deu, as perguntas que a skill fez e a saída resumida de cada ação: o doc de operação, o prompt final do agente, a sequência de qualificação e a nota de handoff. Ler antes economiza uma rodada inteira de retrabalho.

> **Em ambiente só de chat, o resultado é SEMPRE um documento, nunca o agente rodando.** Sem acesso a terminal, esta skill entrega o plano de conexão escrito passo a passo, o prompt do agente e as peças de topo, tudo em `.md`, pro dono executar num ambiente com terminal. Operação viva só onde há shell. Isto vale desde a primeira resposta: não prometa agente ligado onde não dá pra ligar.

### A régua de canal por ticket (mesma régua das skills irmãs)

Até R$ 3.000 o fechamento acontece na própria conversa (DM ou WhatsApp, com áudio, doc e vídeo curto). Acima de R$ 3.000 a conversa qualifica e agenda a call 1:1, e o fechamento acontece na call. O funil de aula/webinar é a exceção: ele fecha de uma vez no checkout, dentro da própria aula. A call também entra abaixo do limiar quando o lead pede a condução ao vivo, quando a decisão é a vários ou quando o caso é complexo. Esta régua é a mesma nas skills irmãs soft-vendas-sdr, soft-vendas-closer e soft-vendas-estrategias, com o texto idêntico nas três; mudou numa, muda nas três.

### A fronteira com as duas irmãs (escrita dos dois lados)

| Quem | O que é dela | Onde para |
|---|---|---|
| **soft-vendas-sdr** (esta) | o TOPO: abre a conversa, responde o lead novo, qualifica de leve, vende a sessão como vaga, agenda e passa o bastão | para no agendamento com a nota rica; nunca responde objeção de preço nem pede o sim |
| **soft-vendas-closer** | o FUNDO: recebe o lead quente, conduz as 7 fases, isola objeção, pede a decisão e coleta o sinal | não abre conversa fria nem opera o CRM |
| **soft-vendas-estrategias** | a JOGADA: decide qual campanha rodar no mês e em que ordem, pra gerar a conversa que esta skill vai atender | não conduz conversa nem opera agente |
| **soft-vendas-outreach** | a PROSPECÇÃO FRIA: pesquisa a conta que nunca ouviu falar do dono e escreve a abordagem que abre a porta | para quando a pessoa responde; a conversa a partir daí é desta skill |
| **soft-vendas-call-prep** | o ANTES da call já agendada: o dossiê do lead, o objetivo da reunião e as objeções antecipadas | não abre conversa nem agenda; ela começa depois que a reunião já existe |

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a oferta, o canal e a voz e eu monto o SDR). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pra montagem com o que o dono colou. Se faltar um insumo que o agente não vive sem (a oferta, o critério de qualificação, o canal), pergunta AQUELE insumo e segue, sem repetir o onboarding inteiro. A subida em sombra e o gate de segurança valem em qualquer modo.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o onboarding do agente, uma pergunta de cada vez (a missão, a oferta, o canal, a voz), e monta com o que o dono for dando.

A pergunta do modo é UMA por operação. As outras três partes acontecem nos passos abaixo:

- **Ensina enquanto faz:** em cada escolha estrutural (a missão do agente, o critério de qualificação, a linha que ele não cruza) escreve UMA linha do porquê. O dono lê a razão e aprende a operar sozinho.
- **Puxa o material bruto:** quando a resposta vier rasa ("qualifica quem tem interesse", "fala como eu"), não segue com o genérico. Pede o concreto que só o dono tem: como ele mesmo abre a conversa na DM com as palavras dele, o que separa o lead que fecha do que some, a última objeção real que ouviu. Voz e critério reais viram agente que soa dono; resposta rasa vira robô genérico.
- **Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer outro critério de qualificação? o follow-up mais insistente? a abordagem em outra voz? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "monta meu SDR", "liga o agente", "quero um atendente 24 horas", "agente de WhatsApp" | **1 · OBJETIVO** e segue até a 6, e **a 7 é obrigatória dentro desta rota** (o pacote sem as mensagens de abertura não é um SDR) |
| "que perguntas o agente faz", "onboarding", "voz do agente", "wiki do produto", "onde ponho o preço" | **2 · ONBOARDING** |
| "conectar o CRM", "conectar o GHL", "Z-API", "Evolution", "webhook", "não chega mensagem" | **3 · CANAL** |
| "o prompt do agente", "o cérebro", "o agente responde errado", "o agente inventou preço" | **4 · MOTOR** |
| "o que o agente pode fazer sozinho", "gate", "killswitch", "medo de ele falar besteira" | **5 · GATE** |
| "pode ligar?", "sombra", "replay", "como sei que está funcionando", "métricas do agente" | **6 · SUBIDA E OPERAÇÃO** |
| "escreve a abordagem de DM", "mensagem de prospecção", "sequência de qualificação", "convite da sessão", "mensagem de follow-up" | **7 · PEÇA DE TOPO** (entra direto, não precisa das anteriores) |

Pedido ambíguo ("me ajuda com o SDR", "olha esse agente aqui"): pergunte UMA coisa só, "você quer o agente rodando ou a mensagem escrita?", mostre a tabela como cardápio e siga pela resposta.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · passos numerados com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de voz, oferta, avatar ou prova: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta descrita no "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR]`. Nunca invente, nunca pare por causa disso.

---

## Ação 1 · OBJETIVO (a missão do agente, sempre primeiro)

**O que faz:** crava qual das 3 missões o agente vai cumprir, porque cada uma tem fluxo, gate e métrica próprios.

**Precisa de:** a resposta do dono sobre o que ele quer que o agente resolva.

**Sem o insumo:** pergunta única, "o agente precisa AGENDAR reunião, RESPONDER dúvida ou EMPURRAR o lead pela esteira?", e a tabela abaixo como cardápio.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** a primeira seção do `01-operacao-agente.md`, com a missão declarada, o desfecho-alvo e a métrica-mãe. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/fluxo-sdr-autonomo.md` (o turno canônico é o mesmo nas 3 missões; muda a postura e o desfecho).

**Profundidade:** `references/playbook-operacao.md` (as réguas e metas por objetivo).

| Missão | O que o agente faz | Desfecho-alvo | Métrica-mãe | Faixa de referência |
|---|---|---|---|---|
| **A. SDR clássico** | pré-qualifica pelo diagnóstico leve e vende a sessão como vaga escassa | reunião agendada + nota rica pro closer | leads → qualificados → agendados → show rate | inbound qualificado que vira reunião: mediana de mercado ~62%; show rate saudável 75% a 85%; abaixo de 70% o problema é o peso da sessão, não a agenda |
| **B. Atendente 24 horas** | responde dúvida e orienta a qualquer hora, só com fato consultado na wiki | pergunta resolvida ou escalada certa | tempo de resposta · % resolvido sem humano | resposta em minutos, madrugada inclusa por fila da manhã; escalada por motivo revisada toda semana |
| **C. Operador de funil** | conduz o lead pela esteira (isca, aula, oferta) com a mensagem do estado | lead avançando de estado até a compra | comparecimento · conversão por etapa · carrinho recuperado | janela quente: % do pós-evento tocado na primeira hora é o número que mais move o resto |

Um projeto pode ter mais de uma missão, mas **cada agente ligado tem UMA missão declarada**. Sem isso, fluxo, gate e métrica viram sopa e ninguém sabe o que é sucesso.

**Por que 24 horas e resposta rápida:** responder o lead em até 5 minutos multiplica a conversão por cerca de 4, e o contato nos primeiros 5 minutos torna a qualificação até 21 vezes mais provável que após 30 minutos ([martal.ca](https://martal.ca/speed-to-lead-lb/), [prospeo.io](https://prospeo.io/s/speed-to-lead-ai)). A média do mercado ainda é de cerca de 47 horas, e o primeiro que responde leva de 35% a 50% dos negócios ([martal.ca](https://martal.ca/speed-to-lead-lb/)). Time híbrido, IA no topo e humano no fechamento, processa de 5 a 10 vezes mais leads sem derrubar conversão ([monday.com](https://monday.com/blog/crm-and-sales/inbound-pipeline-ai-sdr/)).

---

## Ação 2 · ONBOARDING (o agente nunca liga genérico)

**O que faz:** coleta do dono a voz, a oferta, a FAQ e a tabela de preços, e coloca cada dado na morada certa.

**Precisa de:** voz e oferta do perfil/brain do agente quando existir · a FAQ do produto em páginas curtas · a tabela de preços aprovada.

**Sem o insumo:** entrevista curta de 6 perguntas, uma por vez: (1) como você fala com o cliente, manda 3 mensagens suas de verdade; (2) o que você vende, em que formato e em quanto tempo entrega; (3) por quanto, e qual é a condição de pagamento; (4) quais são as 10 perguntas que mais te fazem; (5) o que o agente NUNCA pode dizer nem prometer; (6) qual o teu limiar de ticket. O que sobrar vira `[A CONFIRMAR]` no doc e o agente liga no modo mais conservador.

**Entrega:** a seção de personalização do `01-operacao-agente.md` mais os dois arquivos de dado: `precos.json` (ou a tabela equivalente) e as páginas curtas da wiki. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Os temas obrigatórios da wiki (uma página curta por tema, no mínimo).** A wiki não é "quantas páginas der": ela cobre estes 6 temas, sempre, porque são os que o lead pergunta e o agente não pode improvisar.

| Página | Cobre |
|---|---|
| `oferta.md` | o que o dono vende, pra quem, o que a pessoa leva embora |
| `formato.md` | como é entregue: online ou presencial, duração, carga, o que o aluno faz por semana |
| `garantia.md` | prazo, condição, como se pede o reembolso, quem responde |
| `objecao-principal.md` | a objeção que mais aparece e a resposta do dono, com as palavras dele |
| `agenda.md` | turma, data de início, encerramento de inscrição, vagas e o evento gratuito quando existir |
| `escalada.md` | o que o agente NÃO responde, pra quem manda, em quanto tempo o humano volta |

**Checagem verificável antes do STOP.** Liste as páginas criadas nesta forma: `<arquivo> | tema coberto | fonte do conteúdo (fala do dono / perfil / [A CONFIRMAR])`. Fecha com `Temas obrigatórios cobertos: N de 6.` Faltando qualquer um dos 6, você não fecha a ação: pergunta ao dono o que falta ou cria a página com o conteúdo marcado `[A CONFIRMAR]` e declara isso.

**Leia primeiro:** `references/onboarding-personalizacao.md` (o que coletar e onde cada dado mora).

**Profundidade:** `references/motor-de-conhecimento.md` (como a wiki é consultada em tempo de resposta).

**O esquema do `precos.json` (mínimo obrigatório, o agente confere campo a campo).** O arquivo tem estes campos, sempre com esses nomes. Campo que o dono não informou entra como `null` e o gate barra o agente de falar sobre ele:

```json
{
  "oferta": "nome da oferta do dono",
  "valor": 0,
  "parcelas": { "quantidade": 0, "valor_parcela": 0, "condicao": "texto curto" },
  "garantia": "texto curto: prazo e condição",
  "bonus": [
    { "nome": "", "descricao": "", "valor_percebido": 0 }
  ],
  "vagas": { "total": 0, "restantes": null },
  "data": { "inicio": "AAAA-MM-DD", "encerramento_inscricao": "AAAA-MM-DD" },
  "evento_gratuito": { "nome": "", "data": "AAAA-MM-DD", "link": "" },
  "links_autorizados": ["url de checkout ou agenda que o dono aprovou"]
}
```

**Checagem verificável antes do STOP (o agente lista e prova).** Escreva no chat, uma linha por campo do esquema, nesta forma exata: `<campo> | preenchido ou null | origem (fala do dono / perfil / não informado)`. Fecha com `Campos null: N. O agente está proibido de falar sobre esses N assuntos.` Entrega de Ação 2 sem essa lista não passa.

**Data parcial vale como data, nunca como ausência.** Quando o dono informa dia e mês sem o ano, grave o valor que ele deu no campo (`"inicio": "06/10"`) e registre a dúvida numa chave irmã (`"inicio_ano_confirmado": false`), nunca `null`. `null` significa "o dono não informou" e faz o gate barrar o agente de falar do assunto: o agente perde a turma, a vaga e a data do evento inteiros por causa de quatro dígitos, e a escassez, que é o que vende a vaga, some da conversa. A mensagem que usa a data escreve a data que existe ("a próxima aula ao vivo é dia 29/09, às 20h"), e a pergunta do ano vai pro handoff. Marcador de ano nunca entra na frase que o lead lê. A mesma regra vale pra todo campo com valor parcial: valor sem condição de parcelamento, bônus sem descrição, link sem `https`.

**Preços em ARQUIVO, nunca no prompt.** Trocar preço passa a ser editar um arquivo; tabela vazia faz o gate barrar qualquer número de dinheiro. Preço no prompt vira preço velho alucinado na primeira troca de tabela. Zero identidade de terceiros: a voz é a do dono do projeto, o método entra por função, nunca por nome.

---

## Ação 3 · CANAL (conecta e testa antes de ligar)

**O que faz:** pluga o agente no canal onde o lead já fala com o dono e prova a conexão nos dois sentidos.

**Precisa de:** o canal escolhido pelo dono · as credenciais dele (token, ID da conta) · acesso a terminal pra testar de verdade.

**Sem o insumo:** sem credencial, escreva o passo a passo de coleta ("onde clicar pra gerar o token") e pare no STOP até o dono trazer. Sem terminal, a ação vira um plano de conexão escrito, numerado, pro dono rodar onde houver shell; declare isso em 1 linha e siga pras outras ações.

**Entrega:** a seção de canal do `01-operacao-agente.md` com o conector escolhido, os IDs mapeados e a **prova do teste de ida e volta**. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**A prova do teste tem 2 formas, e a segunda vale igual.** Com canal conectado e acesso de verdade, a prova é o print (ou o log da chamada) do teste. **Sem canal ligado, a prova é a transcrição do teste de ida e volta**, nesta forma exata, uma linha por passo:

```
[enviei]   texto exato que saiu, canal, horário
[chegou]   texto exato que voltou, canal, horário
[estado]   passou · falhou · não executado (motivo)
```

Passo `não executado` é resultado válido e honesto; passo inventado, não. **É proibido escrever "teste feito" ou "conexão testada" sem a transcrição ou o print no doc.** Fecha a seção com `Passos testados: N · passaram: N · não executados: N (motivo).`

**Leia primeiro:** `references/conectores.md` (os 5 canais, riscos e diferenças).

**Profundidade:** `references/conector-ghl.md` (as chamadas reais da API do GHL e os achados de campo) · `references/setup-conexao.md` (o GHL passo a passo: token, IDs, teste).

Os 5 conectores: **GHL/GoHighLevel** (o padrão, com manual completo), **Z-API**, **Evolution API** (WhatsApp não oficial: funciona, com risco real de banimento do número; o dono decide avisado), **Zernio** e **modo direto** (o bridge do próprio agente do usuário como canal). O cérebro e os gates são os mesmos em todo canal; o que muda é webhook, envio e estados. Compliance: a API oficial do WhatsApp exige opt-in e template aprovado; a não oficial tem risco de banimento, e o comportamento (spam, denúncia) pesa mais que o método de conexão ([omnichat](https://blog.omnichat.ai/unofficial-whatsapp-business-api/), [wapisimo](https://wapisimo.dev/blog/en/whatsapp-unofficial-api-ban-risk)).

---

## Ação 4 · MOTOR (o cérebro que responde)

**O que faz:** monta o prompt do agente, carrega a wiki, aponta o arquivo de preços e fecha o turno canônico.

**Precisa de:** a missão da Ação 1 · a voz, a oferta e a FAQ da Ação 2 · o canal da Ação 3.

**Sem o insumo:** com a missão e a voz na mão já dá pra montar o prompt; sem canal, monte o prompt e teste no simulador de texto, marcando o envio como pendente.

**Entrega:** `02-prompt-agente.md`, o prompt final pronto pra colar, mais a lista de páginas da wiki carregadas. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/motor-de-conhecimento.md` (wiki, preços em arquivo, proibições e lições, ports e adapters).

**Profundidade:** `references/fluxo-sdr-autonomo.md` (o turno canônico completo e os fluxos por objetivo).

**O turno canônico, a ordem que não se inverte:** killswitch → optout → estado do lead → escalada dura → prompt com a verdade do cadastro → loop de ferramentas → gate de saída → horário de silêncio → envio.

**Modelo recomendado:** o econômico da fornecedora escolhida. Pra volume 24 horas, a faixa rápida e barata do catálogo tem custo e velocidade compatíveis com centenas de conversas por dia, com qualidade suficiente pro topo do funil. O fechamento complexo é humano, ou do closer com modelo maior.

**Loop de ferramentas com teto** (padrão 4 rodadas) e 3 defesas anti-loop, com ferramentas neutras de fornecedor: leitura livre, ação com validação. **Debounce:** rajada de mensagens do lead numa janela curta vira UM turno só; sem isso o agente atropela a própria fala. **Ports e adapters:** o cérebro não importa fornecedor, trocar de CRM é escrever 1 adapter, e é isso que torna o agente replicável em qualquer cliente.

### O exemplo do prompt final (missão A, SDR clássico)

Este é o esqueleto que o `02-prompt-agente.md` entrega, com os campos do dono preenchidos. Nicho fictício, consultoria de organização financeira pra clínicas de pequeno porte:

```
Você atende o WhatsApp de uma consultoria de organização financeira pra clínicas.
Sua missão é UMA: qualificar o lead e AGENDAR a sessão de diagnóstico. Você não fecha venda.

VOZ: direta, sem saudação de call center, sem emoji além de um quando couber, frases curtas.
Fala como quem já atendeu 140 clínicas, nunca como atendente de central.

O QUE VOCÊ SABE: só o que está nas páginas da wiki que você consultou neste turno.
Não sabe = "vou confirmar isso e te respondo", e escala. Nunca afirme fato do produto de cabeça.

DINHEIRO: qualquer número de dinheiro sai do arquivo de preços consultado NESTE turno.
Arquivo sem o número = você não fala valor, você agenda.

UMA PERGUNTA POR MENSAGEM. Os 4 elementos, nesta ordem, sem metralhar:
1. Essência: "o que te fez começar a olhar pra isso agora?"
2. Tempo: "isso é pra agora ou você ainda quer tentar por conta antes?"
3. Ações: "o que você já tentou? o que não funcionou?"
4. Resultados: "o que você conseguiu sozinha até aqui? o que espera ter?"

DESFECHO: com os 4 elementos na mão, vende a SESSÃO como vaga
("tenho 2 horários essa semana pra diagnóstico, quinta 9h ou sexta 15h, qual fica melhor?"),
agenda no slot livre e grava a nota rica no CRM.

NUNCA: prometer resultado, dar desconto, fechar acima do limiar, falar de assunto fora do escopo
(jurídico, saúde, imprensa: escala), revelar que é IA se o dono vetou.

Lead sem perfil: encerra leve, marca no CRM e agradece. Filtrar cedo devolve tempo pra quem tem perfil.
```

---

## Ação 5 · GATE (a linha que o agente não cruza)

**O que faz:** monta a rede de segurança em código, mostra a tabela pro dono e pega o OK dele.

**Precisa de:** a tabela abaixo revisada com o dono · a decisão dele sobre o que o agente pode fazer sozinho.

**Sem o insumo:** sem OK do dono, liga no modo mais conservador (agente redige, ninguém envia) e diga isso em 1 linha.

**Entrega:** a seção de gate do `01-operacao-agente.md`, a tabela ajustada e assinada pelo dono. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/gate-de-seguranca.md` (as duas camadas, as regras sempre ligadas, o caminho de sombra até autônomo).

**Princípio-mãe: tudo que o prompt diz "nunca faça" tem um equivalente EM CÓDIGO conferido depois do modelo.** Prompt sozinho não é gate: o modelo esquece e ninguém confere a saída.

| Faz sozinho | NUNCA sem o dono |
|---|---|
| Responder, qualificar, conduzir o diagnóstico | Número de dinheiro sem consultar o arquivo de preços no turno |
| Vender e agendar a sessão em slot livre | Fechar acima do limiar, ou link de pagamento fora da tabela |
| Criar e atualizar contato, taguear, criar nota | Link fora da lista autorizada, ou data e hora que não batem com o cadastro |
| Mover o card, agendar follow-up | Prometer resultado, pedir dado sensível, revelar que é IA se o dono vetou |
| Encerrar lead sem perfil, com registro | Falar de assunto fora do escopo (jurídico, saúde, imprensa): escala |

**Sempre ligadas:** killswitch por arquivo de pausa · horário de silêncio das 22h às 8h no fuso local · optout imediato com tag · anti-spam · toda falha avisa alguém.

**Se o dono não tem como implementar as defesas em código** (não tem quem mexa no motor, ou o canal dele não deixa): não ligue autônomo. O caminho é o **modo rascunho permanente**, o agente redige e um humano aprova cada envio, com as 3 barreiras que se resolvem sem código: (1) tabela de preços fora do prompt, num arquivo que o humano confere antes de enviar; (2) lista curta e escrita de assuntos que forçam escalada, colada ao lado de quem aprova; (3) um teto de toques por lead por dia, contado na mão. Declare em 1 linha que esse modo custa tempo humano e que o autônomo só abre quando as defesas existirem em código.

---

## Ação 6 · SUBIDA E OPERAÇÃO (sombra, replay, números)

**O que faz:** roda o agente em sombra, prova com replay de conversas reais, sobe pra autônomo e reporta.

**Precisa de:** o agente montado das ações 1 a 5 · conversas reais anteriores pra usar no replay · a aprovação do dono.

**Sem o insumo:** sem histórico de conversa real, rode o simulador com 10 casos escritos que cubram os 7 estados do lead e trate isso como piso, não como prova; declare em 1 linha que o replay real ainda falta.

**Entrega:** `03-relatorio-subida.md`, com o resultado do replay caso a caso, a decisão de subir ou não, e a régua de reporte diário. **STOP antes de ligar o autônomo.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/playbook-operacao.md` (os 7 estados do lead, cadências, handoff, auditoria, métricas por objetivo).

**Profundidade:** `references/sales-farming.md` (o cultivo contínuo da base fria como rotina, ciclo de cerca de 30 dias, critérios de entrada e reentrada).

**Degraus: sombra → autônomo**, com replay de conversas reais como prova ANTES de ligar. Ligar autônomo no dia 1 queima lead de verdade sem histórico que justifique a confiança. **O agente nunca opera calado:** resumo diário mais auditoria legível.

**Quem comprou nunca recebe oferta.** O estado `cliente` ganha de todos os outros.

### As mensagens do agente (dentro da rota "monta meu SDR", não é opcional)

Agente sem mensagem escrita não atende ninguém. Antes de fechar a rota, escreva os 5 moldes abaixo **na voz do dono** (a voz coletada na Ação 2), com o dado real vindo do `precos.json` e das páginas da wiki. Nenhum molde sai genérico.

| Molde | O que carrega |
|---|---|
| **1. Abertura** | uma linha só, cita o que a pessoa acabou de fazer (baixou o material, respondeu o story, faltou na aula), pergunta aberta no fim, zero pitch |
| **2. As 4 perguntas da qualificação** | os 4 elementos da Ação 7 (Essência, Tempo, Ações, Resultados) vestidos na voz do dono, uma pergunta por mensagem |
| **3. Convite** | oferece o próximo passo (a sessão, a call, a aula) com dia e horário concretos, e o link autorizado do `precos.json` |
| **4. Lembrete** | dispara antes do compromisso, confirma presença, dá a saída fácil de remarcar |
| **5. Encerramento** | fecha a conversa de quem não avançou sem queimar a ponte, e diz quando o agente volta |

O texto dos 5 moldes segue o pré-flight de copy e o gate da Ação 7. Onde falta insumo (verbatim, data, link), o molde sai com `[A CONFIRMAR: o quê]` no lugar exato, nunca com um valor plausível inventado.

**Checagem verificável antes de fechar a rota.** Liste: `<molde> | escrito? sim/não | dado real usado (campo do precos.json ou página da wiki) | [A CONFIRMAR] pendentes: N`. Rota "monta meu SDR" com qualquer molde em `não` não está terminada.

**Rode a régua de títulos sobre a PRIMEIRA LINHA de cada um dos 5 moldes.** A primeira linha da abertura, da pergunta, do convite, do lembrete e do encerramento é o que decide se o lead responde, e ela é título pela função, ainda que não pareça um. Passe cada uma pela régua `shared-references/crivo/07-regua-de-titulos.md`, R1 a R7, e cole a tabela dentro do arquivo das peças de topo, na forma `<primeira linha> | gatilho nomeado: <qual das 6 famílias> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`, com a lista fechada de contagens no fecho, uma por linha, exatamente nesta forma:

As contagens do fecho saem do script, nunca da cabeça:

```
python3 scripts/checar_titulos.py --peca <arquivo das peças de topo> \
  --titulos titulos.txt --insumos <pasta de insumos do dono> --perfil <perfil do dono>
```

`titulos.txt` traz uma primeira linha de molde por linha. Cole a saída INTEIRA e substitua só os `<preencher>`: a lista é FECHADA e nenhuma linha pode faltar. A checagem sai no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída, e entrega sem ele reprova antes da análise de conteúdo.

O lead escreve pelo canal privado, então o gate de nome vale aqui inteiro: o script imprime `nomes candidatos achados pelo script: N` com `mensagem privada: sim/não` por nome, e nome de conversa privada sem autorização no insumo reprova com exit 1. Onde falta insumo, o marcador cabe em `[A CONFIRMAR: <o dado>]`, no máximo 6 palavras: o porquê da pendência vai pro handoff, e o script conta.

**As contagens de R3, R4 e R5 são gates, não termômetros.** Quando `com inimigo ou inversão` ficar abaixo da metade do lote, `teses distintas` abaixo de 3, ou `em molde de antítese` acima de 1, a entrega **não sai**: os títulos reprovados voltam pro passo de escrita, são reescritos, e a checagem final mostra a contagem corrigida mais a linha `reescritos por contagem: N (<contagem que reprovou>)`. Declarar a contagem que reprova e publicar assim mesmo é o pior dos dois mundos, porque produz um documento que prova o próprio defeito e não o corrige: o dono lê `0 de 4` e não tem como saber que isso significa que a régua reprovou. **Nenhuma justificativa de tipo de peça vale aqui:** se o formato dispensa a inversão, a exceção mora escrita na receita do tipo, e a entrega cita a linha dessa receita.

**E nenhum molde sai com marcador no miolo da frase.** Dia, hora, link e valor são CAMPOS, e campo vive no fim da linha ou numa linha própria de configuração acima da mensagem. O convite `"tenho [dia] às [hora] ou [dia] às [hora]"` é uma frase que o dono copia e cola com o buraco no meio, e o lead recebe o buraco. Há duas saídas e nenhuma terceira: escrever o convite na versão que dispensa o dado ("me diz dois horários que funcionam pra você essa semana"), ou deixar os horários numa linha `SLOTS:` acima da mensagem, pro dono preencher antes de colar. Checagem colada: `moldes: 5 · com marcador no miolo: 0`, e qualquer valor diferente de 0 reprova a rota.

---

## Ação 7 · PEÇA DE TOPO (quando o pedido é a mensagem, não o agente)

**O que faz:** escreve a peça escrita do topo (abordagem de DM, sequência de qualificação, convite de sessão, mensagens da esteira).

**Precisa de:** a voz e a oferta do dono, do perfil/brain do agente · o verbatim real do público (a fala que ele usou de verdade).

**Sem o insumo:** entrevista curta de 4 perguntas: pra quem é a mensagem · o que essa pessoa acabou de fazer (viu um story, faltou na aula, largou o carrinho) · qual o próximo passo que você quer que ela dê · me manda 3 falas reais dela. Sem verbatim, escreva a peça marcada `[A CONFIRMAR]` no lugar de cada aspa e diga isso em 1 linha; nunca invente fala de cliente.

**O nome do destinatário é literal, e a anonimização não vale pra ele.** O crivo 08 protege TERCEIROS citados dentro de uma peça; a pessoa a quem a mensagens é endereçada usa o primeiro nome literal do insumo. Sem nome no insumo, ela abre sem vocativo, nunca com inicial. Certo: `Fernanda, eu vi que você baixou o material na terça.` Errado: `F., eu vi que você baixou o material na terça.` Cole no `conferencia/checagem-titulos.md`, abaixo do bloco do script, a linha `mensagens escritas: N · com primeiro nome do destinatário no vocativo: N`, e diferença entre os dois números reprova (ver `shared-references/crivo/08-consentimento.md`).

**E o papel do nome muda por ARQUIVO.** A mesma pessoa é destinatária no arquivo de mensagens e terceiro em qualquer documento que fale SOBRE ela (fila, critério, triagem, relatório), e cada arquivo segue a regra do seu papel: nome literal em vocativo lá, `contato <N>` sem identificação aqui, com o número da posição amarrando os dois. Cole as duas linhas separadas, `nomes literais no arquivo de mensagens: N (todos em vocativo)` e `nomes literais nos documentos de trabalho: 0` (ver o bloco "O papel do nome muda por ARQUIVO" em `shared-references/crivo/08-consentimento.md`).

**Molde endereçado a pessoa nomeada exige o insumo dela aberto:** rode `grep -n '<Nome>' <insumo>` e cole a saída antes da fala, na forma do bloco "Fala atribuída ao destinatário" de `shared-references/crivo/08-consentimento.md`. Fala atribuída sem trecho literal do insumo reprova. Cole `moldes com nome próprio: N · com fala literal do insumo: N`, os dois iguais.

**Dentro do bloco de copy só existe campo, e campo é substituível por colagem sem reescrever a frase.** Rode e cole a saída:

```
grep -oE '\[[^]]*\]' <bloco de copy> | awk '{print NF, $0}'
```

**Qualquer colchete com mais de 3 palavras dentro do bloco reprova a abordagem.** Cole `campos no bloco: N · com mais de 3 palavras: 0 · instruções movidas pro bloco de preparo: N`. O `checar_titulos.py` conta o marcador acima de 6 palavras e reprova ali; dentro do bloco de copy o teto é mais apertado, e são 3.


**A última frase é convite, nunca menu.** Cada mensagem fecha pedindo UMA coisa que o lead responde em cinco segundos: um horário, um sim, uma escolha entre dois dias. Fechar oferecendo o cardápio ("você prefere a sessão, o material por escrito ou entrar na lista?") é correto e frio, e devolve pro lead o trabalho de escolher o próprio caminho, que é justo o trabalho do SDR. A escolha entre caminhos comerciais é do dono, na tabela de opções. Cole `mensagens escritas: N · com última frase que se responde em 5 segundos: N`, e diferença entre os dois números volta pro passo de escrita.

**Entrega:** `04-pecas-de-topo.md`, um documento consolidado com a peça inteira, nunca pingada em pedaços no chat. **STOP: "ajusto ou pode ir pro lead?"**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/prospeccao-e-qualificacao.md` (os 3 cenários da DM, os 4 elementos, o pré-qualificador, o downsell).

**Profundidade:** `references/vender-a-sessao.md` (a sessão como vaga, as 5 jogadas de campo) · `references/caixa-de-ferramentas-sdr.md` (scripts por canal, árvore de qualificação, templates de agendamento e lembrete) · `references/modos-e-mentalidade.md` (os 3 modos e as cadências de reativação) · `references/prospeccao-dm.md` (banco complementar de aberturas; onde divergir, vale `prospeccao-e-qualificacao.md`).

### A ordem canônica do topo (não se pula etapa)

```
[Abordagem/resposta] → qualifica de leve → PRÉ-QUALIFICADOR
                     → volta esquentado → vende a SESSÃO → handoff pro closer
```

O **pré-qualificador é etapa obrigatória**, em duas formas: **A. aula/webinar** (a aula é o pré-qualificador; o agente entra depois dela, com a postura do estado do lead) ou **B. mini carta / mini webinar** (a peça curta faz o filtro; entregar na janela quente, até 2 horas). É proibido saltar da qualificação direto pra sessão sem pré-qualificador, com a exceção do lead que já chega pedindo a sessão. Se nenhum existe no projeto, avise o dono que precisa construir primeiro e não improvise.

### Os 4 elementos da qualificação (o framework, não invente outros)

São exatamente estes quatro. **Dor não é um dos elementos**, ela sai por dentro de Ações e Resultados. O BANT é lido por dentro, nunca perguntado a seco.

| Elemento | Pergunta base |
|---|---|
| **Essência / Situação** | *"O que te fez começar a olhar pra isso?"* |
| **Tempo / Amarras** | *"Isso é pra agora ou ainda quer tentar por conta antes?"* |
| **Ações** | *"O que você já fez pra resolver? O que não funcionou?"* |
| **Resultados** | *"O que você conseguiu sozinho? O que espera ter?"* |

Uma pergunta por mensagem. A abertura do cenário de sinal ativo é UMA linha que confirma o interesse; o áudio de abertura tem de 5 a 10 segundos, só nome e pergunta, sem pitch.

### Pré-flight de copy (releia imediatamente antes da primeira linha)

**Antes da primeira linha de copy da entrega, a palavra-chave sai de comando, UMA vez.** Rode `grep -rn -iE 'manda |comenta |envia |digita |palavra ' <pasta de insumos>` e cole a saída inteira no topo da peça (ou do handoff, quando a peça for pública). A palavra que aparecer nessa saída é a única que pode entrar em CTA nesta entrega, com a grafia exata, e o resultado desse único comando é reaproveitado em cada jogada: rodar de novo por jogada não vale, e escolher palavra que não está na saída não vale. Saída vazia proíbe escolher uma, e o CTA sai na versão que dispensa a palavra. Cole, por peça, `CTA com palavra-chave: sim/não · palavra: <literal> · origem: <arquivo:linha>`, e `sim` sem origem reprova antes da análise de conteúdo.

A copy nasce da terça-feira à noite DO LEITOR. A regra é checagem, nunca geradora: escreva a partir da cena e da emoção dela, com voz de mesa; a regra confere depois. Reprovou, regenera do zero, porque frase editada herda o esqueleto do defeito.

1. **Munição na mão:** verbatim e prova real do dono na frente; sem munição, pergunta, jamais inventa.
2. **Leitura única:** uma leitura em voz alta, sem reler; valência única; sintaxe linear; 1 operação mental por frase.
3. **Mundo do leitor:** componente do método vira dia, hora, lugar e fala do cliente.
4. **Compressão gramatical: cota zero.** Verbo da relação por extenso; a força é do fato.
5. **Voz de mesa, não palco:** a colocação inteira é fala real; metáfora morta entra, figura de escritor não.
6. **Prova com atribuição exata**, do banco de provas do dono, nunca fundida.
7. **Anti-IA:** zero travessão, zero da família banida, zero verbo genérico de transformação, zero frase de moldura.
8. **Teto do formato conhecido ANTES**, contado durante, não consertado depois.

---

## Gate de qualidade (roda antes de entregar, sempre)

**As cinco primeiras linhas da sequência entram na régua de títulos, e nenhuma sai por ser operacional.** Lembrete, confirmação e encerramento são as duas mensagens de maior taxa de leitura da sequência: classificá-las como serviço tira da régua justamente o que mais gente lê. A coluna `serviço` deixa de ser resposta aceita nesta lista, e `títulos de abertura: N` menor que o número de moldes da sequência reprova a checagem. Conte os moldes antes de escrever a tabela, e cole `moldes na sequência: N · títulos de abertura na régua: N`, com os dois números iguais.


**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


| Check | Passa se |
|---|---|
| **Missão declarada** | o doc diz qual das 3 missões, com desfecho-alvo e métrica-mãe |
| **Personalizado** | voz, oferta e FAQ vieram do dono; nada de bot genérico; zero identidade de terceiro |
| **Preço em arquivo** | nenhum valor de dinheiro dentro do prompt; a tabela é arquivo consultado no turno |
| **Gate em código** | toda proibição do prompt tem conferência depois do modelo, ou o modo rascunho permanente está declarado |
| **Sombra antes do autônomo** | o replay de conversas reais aconteceu e está no relatório, ou a pendência está escrita |
| **Fronteira respeitada** | não conduziu objeção nem pediu o sim (é da soft-vendas-closer), não decidiu campanha do mês (é da soft-vendas-estrategias), não empacotou nem instalou kit (é da soft-sdr-kit) |
| **Handoff rico** | a nota do CRM traz dor, problema avançado, BANT, o que falta, e tem dedup de 30 minutos |
| **Furo marcado** | todo dado que faltou está `[A CONFIRMAR]` no lugar exato; nada foi inventado |
| **Saída em arquivo** | a peça está num `.md` nomeado, com o caminho citado na resposta, nunca pingada no chat |
| **Anti-IA** | com shell, roda o linter anti-IA do ambiente sobre o arquivo e exige saída limpa; sem shell, varre o texto atrás do travessão longo e da família do verbo-freio banida pela régua anti-voz, e reescreve cada ocorrência |
| **VEREDITO** | é o pior item; um ✗ refaz o item, não o doc inteiro |

Onde a pasta trouxer `shared-references/filtro-anti-ia/`, ele é a régua completa e roda por último na copy.

## O que esta skill NÃO faz

Em toda rota abaixo: se a outra skill não estiver instalada, esta faz o mínimo aqui e diz que fez, com o pedaço mais fino marcado `[A CONFIRMAR]`.

- **Conduzir a conversa quente, responder objeção, pedir o sim, coletar o Pix, pós-venda** → **soft-vendas-closer**. Esta skill para no agendamento.
- **Decidir qual campanha rodar no mês, plano de jogadas, estratégia de lançamento** → **soft-vendas-estrategias**. Ela gera a conversa; esta atende.
- **Instalar, atualizar ou publicar o pacote do kit de SDR num cliente** → **soft-sdr-kit**. Lá é o pacote e a instalação; aqui é o método comercial.
- **Contrato depois do sim** → **soft-vendas-contratos**. **Proposta em site premium** → **soft-vendas-proposta**.
- **Carta, VSL, mini webinar, landing** que traz o lead → `soft-funil-*`. **O webinar em si** → `soft-webinar`.
- **Posicionamento, oferta, PUV, voz** → `soft-plano-posicionamento`. **Conteúdo de feed** → `soft-conteudo-*`.

## Anti-patterns

| Erro | Por que quebra | Faz assim |
|---|---|---|
| Ligar o agente sem missão declarada | Fluxo, gate e métrica viram sopa | Ação 1: escolhe A, B ou C e declara no prompt |
| Preço no prompt | O modelo alucina número velho na primeira troca de tabela | Preço em arquivo; sem arquivo, o gate barra dinheiro |
| Gate só no prompt | O modelo esquece e ninguém confere a saída | Toda proibição tem conferência em código depois do modelo |
| Ligar autônomo no dia 1 | Erro queima lead real sem histórico que justifique | Sombra, replay de conversa real, depois autônomo |
| Responder rajada mensagem a mensagem | O agente atropela a própria fala e vira spam | Debounce: a rajada vira um turno |
| Afirmar fato do produto de cabeça | Alucinação em cima do produto do dono | Só responde o que consultou na wiki; achou nada, escala |
| Oferta pra quem já comprou | Queima o cliente e a marca | O estado `cliente` ganha de tudo |
| Handoff raso ("tá quente") | O closer entra perdendo | Nota rica com dor, problema avançado, BANT e o que falta |
| O agente fecha acima do limiar | Invade o closer e fecha sem condução | Vende a sessão, agenda, passa o bastão |
| Metralha perguntas, cara de call center | O lead sente o robô e esfria | Uma pergunta por mensagem, crivo anti-IA em toda saída |
| Persegue quem não respondeu | Queima o lead e a marca | Cadência com teto de 4 toques, depois para |
| Prometer agente rodando em ambiente só de chat | Entrega que não existe | Sem shell, entrega o plano escrito e diz isso na primeira resposta |

## Handoff

- **Pra frente:** lead qualificado e agendado → **soft-vendas-closer**, com a nota rica no CRM, dedup de 30 minutos e frase de espera pro lead.
- **Pra trás:** os números do agente por objetivo voltam pro orquestrador, que calibra a rotina; pré-qualificador que falta → `soft-funil-carta` ou `soft-funil-miniwebinar`; oferta ou tabela indefinida → `soft-plano-posicionamento`; campanha do mês → `soft-vendas-estrategias`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `shared-references/crivo/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## A frase que a dona repetiria (fecho, uma por entrega)

Escolha a UMA frase da entrega que a dona repetiria de cor numa conversa, cole ela sozinha e responda por escrito por que ela sobrevive fora do contexto: sem a peça em volta, sem o nome do produto, sem a explicação que vem antes. Cole `frase que sobrevive fora do contexto: <literal>`. Correta e morna é o defeito comum aqui: a abertura que serve pra qualquer serviço do mesmo tipo não é a frase, é o preenchimento. Nenhuma frase significa que a peça está correta e não está viva, e a entrega volta pro passo de escrita.

## Passo 2 da checagem (fecho, roda por comando)

Depois de gravar todos os entregáveis, rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída. Ele exige o `conferencia/checagem-titulos.md` na pasta, confere o inventário (os 4 inteiros, o piso e o `inventário duplicado`), o universo dos títulos, o marcador acima de 6 palavras, o nome de conversa privada, a `saída do script reescrita` e o lint de todo `.md`, RELATO incluso. **`exit` diferente de 0 reprova a entrega inteira, antes da análise de conteúdo.**
