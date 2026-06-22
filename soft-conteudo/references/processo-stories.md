# Stories - frente de conteúdo (reference da soft-conteudo)

> **Passo 0, antes de escrever a primeira linha (entrada ancorada).** Abre a fonte de fala real do cliente da vez (`shared-references/crivo/01-entrada-verbatim.md`, passo 0: identifica a fonte do usuário) e puxa 3-5 falas de dor e 3-5 de desejo do tema, literais. A primeira linha da peça nasce de uma delas, quase intacta, citando o N. Assim a peça nasce ancorada, não só é reprovada no gate do fim.

# Soft Stories, Cap 8 do Guia

Stories é o canal de conversão diária com quem já te segue. Enquanto Carrossel e Reel atraem público novo, o Story trabalha quem já está dentro: aquece, qualifica e fecha. Esta skill é o **processo de produzir Stories**, os 4 sistemas vivem no guia; aqui está como rodá-los todo dia, montar a campanha e corrigir quando não converte.

## A fonte é o guia, leia primeiro

O método vive no guia, não nesta reference. **Na primeira invocação da sessão, leia:**

- **`guia/08-stories.md`** (Cap 8), **a fonte da verdade dos 4 sistemas.** Define CARO, Caixinha Estratégica, Sequência de Venda de 5 dias e Story Infiltrado: o que cada um é, quando entra, a regra da Oferta (máx 2-3x/semana, nunca o primeiro do dia) e a ordem dos 5 dias. **Não duplica aqui, consulta lá.**
- `guia/01-filosofia.md`, a régua: *"o cliente certo entende e confia mais rápido"*. O arco do dia inteiro precisa apontar pro método, mesmo quando um story isolado é leve.

Esta skill carrega o **como executar**, roteiros prontos, perguntas por nicho, variações de Oferta, benchmarks de diagnóstico. Tudo que é definição de sistema está no Cap 8.

## Antes de entregar, passa pela shared-references

Toda peça atravessa a `shared-references` antes de sair:
- `guia/CODIGO-DE-ESCRITA.md`: **a lei de escrita que rege todo output**. As **8 leis** (revele não ensine · cada frase é conclusão · deixe respirar · polarize · nomeie o fenômeno · repita a tese · ancore), a **estrutura-mãe** (Diagnóstico → Nomeação → Polaridade → Nova visão → Consequência → Movimento) e a **regra-zero**: *"que percepção estou reorganizando?"* + *"onde está o chão?"*. Em Stories a estrutura-mãe vira o ritmo curto **observação → interpretação → tese**: o frame parte do que se vê (o print, a cena real), interpreta sob a lente da percepção e fecha numa tese curta ancorada, nunca opinião solta. Cada frame que afirma uma tese fecha em chão (um print, um número, uma cena), não em frase bonita no ar. **O eixo na peça:** o cliente fala o **teto** que ele vive na pele (preso, comparado por preço, refém da operação), nunca o rótulo "você é invisível"; a percepção é o mecanismo por baixo, não a frase do story.
- `shared-references/dicionario-conversacional.md` + `adaptacao-semantica.md`, tom de comando, vocabulário do cliente final (nunca "lead/funil/ticket" no texto do story).
- `shared-references/filtro-anti-ia/`, Stories é curto e vulnerável a frase-emoldura e tricolon de IA. Roda `python3 scripts/lint_copy.py` no texto dos frames: ele reprova em-dash e o verbo banido da anti-voz Soft (ver `shared-references/filtro-anti-ia/padroes-banidos.md`), falha dura re-roda.
- `shared-references/filtro-mobile-first/`, Stories é mobile por natureza; confere tipografia só se houver slide com texto.

Os 5 movimentos já estão absorvidos pela Fórmula 7 e pela régua da percepção, ficam no fundo, **não se citam como checklist** na peça. Quem segue a estrutura do Cap 8 já entrega os cinco.

---

## Os 4 sistemas, quando aciona cada um

Não são estilos a escolher: são camadas que operam em momentos diferentes (Cap 8.1). Um roda todo dia, outro entra na semana, outro só em campanha, o último só quando há verba.

| Sistema | Função | Quando | Onde está o detalhe de execução |
|---|---|---|---|
| **CARO** | Rotina diária | Sempre, o chão | `references/sistema-caro.md` |
| **Caixinha Estratégica** | Plantar pergunta + ler intenção | 2-3x/semana | `references/caixinha-estrategica.md` |
| **Sequência de Venda** | Campanha pontual de 5 dias | Lançamento, vagas abertas | `references/sequencias-de-venda.md` |
| **Story Infiltrado** | Tráfego frio | Quando tem verba | `references/story-infiltrado.md` |

Os três primeiros trabalham quem já está dentro; o quarto vai buscar quem está fora. **CARO é a base**, Sequência e Caixinha entram em cima dele. Sem CARO rodando há semanas, Sequência vira spam.

**Ponto de entrada:** `references/modo-stories.md` decide qual sistema acionar pelo que o cliente precisa hoje, e traz a tabela de decisão e o checklist diário.

---

## CARO e a Fórmula 7, como convivem

CARO é o arco do dia (Cap 8.2): quatro tipos, cada um com função. A **Fórmula 7** (Hook · Quebra de Crença · Diagnóstico · Vilão · Virada · Mecanismo · Convite, Cap 5-7) é a mesma espinha de toda peça Soft, **distribuída ao longo da sequência de Stories** em vez de comprimida numa peça só. A própria estrutura CARO já a entrega:

| Fórmula 7 | Como aparece em CARO |
|---|---|
| Hook / Diagnóstico | **C, Caixinha** abre o ciclo e nomeia a dor |
| Quebra de Crença / Vilão | **A, Alinhamento** marca a tese contra o status quo |
| Virada / Mecanismo | **R, Resultado** prova que o método funciona |
| Convite | **O, Oferta** fecha |

Numa **Sequência de Venda**, a Fórmula 7 não some, ela se estica nos 5 dias (Cap 8.4): prova (dia 1) → diagnóstico (dia 2) → método em ação (dia 3) → objeção (dia 4) → urgência + convite (dia 5). Quando precisar de mais repertório de aterramento ou de forma de Convite, a fonte é o Cap 5-7 do guia.

---

## Princípios raiz

**Do Soft Business (Cap 1, 8):**
- **Associação repetida > volume isolado.** Não é o que você diz uma vez, é o que repete de forma natural.
- **CARO não é FAQ nem vlog.** É sistema de conversão, cada tipo tem função única.
- **Oferta sem contexto é spam; oferta com contexto é convite.** Por isso C + A + R vêm antes do O. A Oferta é fechamento de sequência, nunca o primeiro story do dia, nunca mais de 2-3x/semana.
- Tom de comando, nunca de súplica: *"Direct 'MÉTODO'"*, nunca *"Você gostaria de…"*.

**Do algoritmo 2026** (detalhe em `references/algoritmo-e-metricas.md`):
- **DM > link sticker.** O Instagram penaliza o que tira o viewer da plataforma. CTA é *"Direct 'PALAVRA'"*, não link externo.
- **Front-load.** O primeiro frame decide se a pessoa continua. Story 1 da Caixinha é o print, não enrolação.
- **Sticker = sinal algorítmico.** Poll, quiz, slider, emoji e question box empurram pro topo da fila. Usar em A (Alinhamento).
- **3-7 frames por sessão** é o baseline saudável; acima de 10 sem interação gera fadiga.
- **Completion rate > 60%** é a meta. Exit consistente no mesmo frame = erro nesse ponto.

---

## CARO, mapa rápido (detalhe em `references/sistema-caro.md`)

**C, Caixinha.** Pergunta plantada que gera resposta. A resposta vira conteúdo no dia seguinte e revela intenção de compra. Sempre ligada ao método ou ao problema do cliente, nunca genérica. É o tipo mais importante, único que prova competência **e** abre CTA natural.

**A, Alinhamento.** Visual real do especialista vivendo o que prega. Subtexto, nunca promessa. Mantém a tese viva mesmo nos dias sem oferta. Sem CTA. Aceita sticker discreto.

**R, Resultado.** Prova: print de pagamento, depoimento, bastidor de entrega, transformação documentada. Print + frase de contexto já basta. Sempre sobe pro destaque "Resultados" antes de sumir.

**O, Oferta.** CTA direto, 3 linhas (problema → entrega → *"Direct 'PALAVRA'"*). Pode repetir a mesma oferta com ângulo novo cada dia. Máximo 2-3x/semana, nunca o primeiro do dia.

**Hierarquia na correria:** C > A > O > R. Se só der pra fazer 1 story, faz Caixinha.

---

## Como produzir, por tipo de pedido

### Rotina CARO do dia
1. Pergunta o tema/tese do dia.
2. Consulta `references/sistema-caro.md`.
3. Escreve 3-7 frames seguindo o arco C → A → R → O (a Oferta só se couber na regra de frequência).
4. Entrega em artifact numerado por frame, com indicação de sticker/foto/print.

### Caixinha Estratégica
1. Pergunta o tema do método e o tipo de público a filtrar.
2. Consulta `references/caixinha-estrategica.md`.
3. Entrega perguntas plantáveis (Problema · Objeção · Detalhamento) + estrutura da resposta em 3-4 frames quando o cliente trouxer uma resposta real.

### Sequência de Venda
1. Pergunta numa frase só: oferta (nome + entrega principal), ticket, formato, datas, palavra-chave, objetivo (leads ou venda direta).
2. A espinha é sempre a **Sequência de 5 dias do Cap 8.4**, prova → diagnóstico → método → objeção → urgência. Os templates de `references/sequencias-de-venda.md` são variações de execução dessa lógica, ajustadas por ticket e formato (auditoria, evento/workshop, alto ticket com filtro, remarketing, híbrido com CARO).
3. Identifica a variação adequada; se ambíguo, pergunta UMA vez.
4. Escreve a campanha dia a dia, frame a frame, palavra-chave única apontando sempre pro mesmo Direct.
5. Fecha com nota de produção (visual por tipo de story) + checklist antes de publicar.

### Story Infiltrado
1. Pergunta quem é o público frio (interesses óbvios) e a tese central a associar.
2. Consulta `references/story-infiltrado.md`.
3. Escreve a cena solta que parece orgânica (sem CTA, sem sticker, foto real) + régua de tráfego (verba de teste, métricas-âncora, decisão em 3 dias).

### Diagnóstico (story que não converte)
1. O cliente cola os números (completion, exit por frame, DMs por story).
2. Consulta `references/algoritmo-e-metricas.md` pros benchmarks 2026.
3. Nomeia **um** gargalo (front-load fraco? texto longo? CTA em link? CARO só com O?), propõe **um** experimento de 7 dias. Nunca cinco fixes ao mesmo tempo.

---

## Formato de entrega

Específico de Stories (geral em `shared-references/operacao-padrao.md`):

```
## Sessão: [tema]
## Sistema: [CARO / Sequência dia N / Caixinha / Infiltrado]

### Frame 1, [tipo CARO: C/A/R/O]
**Texto na tela:** [o que aparece]
**Áudio/narração:** [se tiver]
**Sticker:** [poll/quiz/slider/emoji/question box, ou nenhum]
**Visual:** [foto/vídeo/print/fundo]

### Frame 2, [...]
```

Sempre nomeia o tipo CARO de cada frame. Entrega copiável.

---

## Auditoria antes de entregar

1. Cada frame tem função clara dentro do CARO (ou do dia certo da Sequência)?
2. Há pelo menos 1 sticker de interação em A?
3. CTA é DM com palavra-chave única, não link externo?
4. O primeiro frame faz front-load (sem enrolação)?
5. A Oferta respeita a regra (não é o primeiro do dia; não passa de 2-3x/semana)?
6. **Teste do dia inteiro:** olhando os 3-7 stories, o arco aponta pro método? Se nenhum frame planta, posiciona ou converte, é sequência de creator, não é Soft.
7. **Regra-zero:** que percepção o arco do dia reorganiza? Onde está o chão (print, número, cena)? Frame que afirma tese sem chão, corta ou ancora.
8. Passou pela **lei de escrita** (`guia/CODIGO-DE-ESCRITA.md`) e pelos filtros **anti-ia** e **mobile-first** (este só se houver slide com texto).

---

## References de execução desta reference

- **`references/modo-stories.md`**, ponto de entrada: decisão de qual sistema, princípios universais, tabela de decisão, checklist diário, diagnóstico rápido.
- **`references/sistema-caro.md`**, CARO frame a frame: 5 ângulos de Alinhamento, 4 tipos de Resultado, 4 modelos de Oferta, protocolo de geração ativa de prova, Story Único com palavra-chave, rotina semanal baseline.
- **`references/caixinha-estrategica.md`**, 3 tipos de pergunta, como plantar nos primeiros 7 dias, estrutura da resposta, banco de respostas e de perguntas plantáveis por nicho, frequência.
- **`references/sequencias-de-venda.md`**, variações de execução da Sequência de 5 dias por ticket e formato, roteiros preenchidos, regras universais, erros fatais.
- **`references/story-infiltrado.md`**, tráfego frio: 5 ângulos canônicos, régua de verba e decisão, métricas-âncora, relação com o tipo A.
- **`references/algoritmo-e-metricas.md`**, benchmarks 2026 (completion, exit, story-to-DM, custo/visita), Highlights como ativo permanente, protocolo de diagnóstico.

---

## Cross-skill, quando passar pra outra

| Cliente pediu | Skill |
|---|---|
| Carrossel · Reel · Turbinar | `processo-feed.md` |
| Capa/headline forte pra Story ou Caixinha | `processo-headlines.md` |
| Lead chegou no Direct via Sequência, fechamento | `soft-funil` |
| Bio, destaques estruturais, Nome-SEO | `soft-posicionamento` |
| Adaptar Infiltrado pra outras plataformas | fora do core |
| Carta / Vídeo Minimalista (destino das DMs) | `soft-funil` |

**Pré-requisitos:** Plano de Marca Pessoal empacado (Cap 2) · Voz destilada (Cap 3) · Carta/Vídeo publicado (Cap 4, destino das DMs) · peças de feed rodando (Cap 5-7, sem o que o feed atrai, Stories não tem o que aprofundar). Stories AMPLIFICA o feed, sem feed, vira tagarelice diária sem direção.

**Cliente com voz própria destilada (ex.: `soft-voz-leo-molina`):** consulta esta reference antes de escrever. O tom íntimo de Stories exige domínio total da voz autoral, qualquer deslize soa creator genérico.

---

## Regra única

> **CARO é o arco. A Fórmula 7 se distribui ao longo dos frames. Cada frame: observação → interpretação → tese curta ancorada. Associação repetida > volume isolado. DM > link. Front-load sempre. Oferta nunca abre o dia.**


## Gate de saída obrigatório, o Crivo (bloqueante)

Antes de mostrar a peça, ela passa pelo Crivo embutido em `shared-references/crivo/`, nesta ordem:
1. **Ancoragem** (`crivo/01-entrada-verbatim.md`), na entrada e na checagem: toda fala entre aspas é verbatim literal da fonte real do cliente, e o ângulo-mãe tem N. Aspa que não bate na fonte reprova.
2. **Simulação na pele do avatar** (`crivo/02-simulacao-cliente.md`): onde ele larga, onde se reconhece, o teste dos 2 segundos.
3. **Gate CUB bloqueante + as 3 perguntas do Harry** (`crivo/03-gate-cub.md`): imprime a tabela, o veredito é o pior bloco, peça que falha não sai, volta pra reescrita.

O anti-IA limpa o robô; o Crivo dá a força. Limpo não é forte. Os dois, nessa ordem. **Sem a tabela do Crivo impressa junto, a peça não foi entregue.**
