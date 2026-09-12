---
name: soft-negocio-metricas
description: >-
  Lê os números do negócio e devolve um diagnóstico com a conta na tela: em qual etapa do funil o resultado quebrou, o quanto ficou abaixo do projetado, e UMA ação com número-alvo pro próximo ciclo. Barra a recomendação quando a amostra é pequena ou o rastreio está furado, em vez de chutar. Use quando o pedido for: "por que não converteu?", "diagnostica meu funil", "os números da semana", "caiu o resultado", "bati a meta?", "vale escalar?", "meu anúncio não deu venda", "compara com a semana passada", "esse post foi bom?". NÃO use pra: "por que meu perfil não converte" quando o pedido é auditar o Instagram inteiro (soft-consultoria-instagram); "por que essa copy não convence" numa peça isolada (soft-critico-copy); montar a projeção ou o plano do zero (soft-plano-negocio); DRE, margem e caixa (soft-financeiro); decidir verba e público do anúncio (soft-trafego-meta); reescrever a peça (soft-conteudo-*); oferta e ticket (soft-plano-ofertas). Leia e siga o fluxo inteiro do SKILL.md.
---

# Ler o número e dizer o que fazer

O funil não quebra inteiro. Quebra em **uma etapa**, e todas depois dela parecem ruins por consequência. Esta skill pega os números crus, prova com a conta na tela em qual etapa o resultado vazou, compara com o que estava projetado, e devolve **uma ação só**, com o número que confirma se ela funcionou. Quando o dado não sustenta uma conclusão, a entrega vira "como medir direito", não um palpite com cara de fato.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra o diagnóstico inteiro num caso fictício: os 9 números que o dono mandou, os 4 testes de confiabilidade rodados, a conta etapa a etapa, o delta contra a projeção, a ação única entregue, e como o repasse pra outra skill acontece na prática. Tem também a comparação semana a semana e um caso que a skill se recusou a diagnosticar.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola todos os números que tem e eu faço a leitura). Se quiser ser guiado passo a passo (te pergunto cada número, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com os números que o dono colou. Se faltar o número que a leitura não vive sem (faturamento, número de leads, taxa de fechamento), pergunta AQUELE número e segue.
- **Modo guiado**: só quando o dono pede explicitamente. Pergunta cada número uma de cada vez, e monta a leitura com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada leitura (por que esse número é o gargalo, por que olhar taxa e não volume, o que a comparação entre períodos revela), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a ler o próprio funil sozinho.

**Puxa o material bruto (parte 3):** quando o número vier redondo demais ("uns 100 leads", "fecho mais ou menos metade"), não faz a leitura em cima do chute. Pede o dado cru: o número exato do painel, o print do relatório, o total real do mês. Número real vira diagnóstico confiável; chute vira leitura frágil. Puxa uma vez; se o dono só tiver o aproximado, lê e marca a premissa em uma linha.

**Oferece refinar no fim (parte 4):** depois da leitura, fecha com UMA linha: "Quer que eu compare com outro período, ou detalhe um número específico? Me diz que eu aprofundo." A oferta de refino não substitui o gate.


## Roteamento por pedido

| O dono pediu | Ação |
|---|---|
| "por que não converteu", "diagnostica o funil", "os números da semana", "caiu o resultado", "esse post foi bom" | **Ação 1 · DIAGNÓSTICO** (passos 0 a 8) |
| "compara com a semana passada", "melhorou ou piorou", "o que mudou desde o mês passado" | **Ação 2 · COMPARAÇÃO ENTRE PERÍODOS** (roda depois do diagnóstico, ou sozinha) |
| "vale escalar o tráfego", "quanto custa cada call", "quantas pessoas eu preciso", "quando contrato" | **Ação 3 · ESCALA** (funil em reais e dimensionamento de time) |

Pedido ambíguo ("olha esses números aí"): pergunte uma coisa só, se o dono quer saber **o que quebrou** ou **se melhorou**, e siga pela resposta. A tabela acima é o cardápio.

**Toda ação obedece ao mesmo contrato de saída:** a conta na tela · todo número com fonte e data (`Insights do Reel, 12 a 18/03`) · nenhuma recomendação sem o delta projetado contra real escrito · amostra que não sustenta vira recusa declarada, não recomendação · sem referência do dono, `[A DEFINIR com o dono]`, nunca benchmark inventado.

### O modelo de marcação de dado a confirmar

Use exatamente estas três marcas, sempre coladas ao número, nunca numa nota de rodapé:

| Marca | Quando usar | Como fica na linha |
|---|---|---|
| `[A DEFINIR com o dono]` | não existe referência própria nem meta declarada pra essa etapa | `conversa → reunião: 3 ÷ 12 = 25% · referência [A DEFINIR com o dono]` |
| `[FONTE?]` | o número veio, mas o dono não disse de onde nem de que período | `31 DMs [FONTE? qual painel, que datas]` |
| `[AMOSTRA INSUFICIENTE, piso N]` | o número existe e é confiável, mas o volume não sustenta uma taxa | `reunião → venda: 0 ÷ 3 = 0% [AMOSTRA INSUFICIENTE, piso 10]` |

Linha marcada não gera recomendação. Ela gera uma pergunta ou uma instrução de medição, e o diagnóstico segue pelas etapas que passaram.

---

## Ação 1 · DIAGNÓSTICO (a leitura completa)

**O que faz:** acha a etapa onde o funil vazou, prova com a conta, e entrega uma ação com número-alvo.

**Precisa de:** os 9 números da semana (peças publicadas, alcance, engajamento qualificado, cliques, DMs qualificados, conversas, reuniões, vendas e receita) com a fonte e o período de cada um · a meta, o ticket e a projeção que geraram o plano · o histórico próprio, quando existir. O dono é a origem de tudo isso; o perfil ou banco do agente cobre ticket, oferta e meta quando já estiverem lá.

**Sem o insumo:** peça o que falta **numa única mensagem**, nunca um número por vez. Sem número nenhum não existe diagnóstico, e a skill usa essa palavra: é palpite. Sem meta e sem histórico, a leitura sai só contra a referência genérica, declarada em uma linha, e as etapas sem referência ficam `[A DEFINIR com o dono]`.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `diagnostico-AAAA-MM-DD.md`, curto: a tabela da conta etapa a etapa, o delta contra a projeção, o gargalo em uma frase, a ação única com o número-alvo, e a skill de destino. Se o ambiente renderizar markdown, mostre também.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/confiabilidade-do-dado.md` (bloqueante, antes de ler qualquer taxa) · `references/funil-etapa-a-etapa.md` (as fórmulas e as faixas).

**Profundidade:** `references/coleta-e-fontes.md` (os 9 números e onde medir cada um) · `references/diagnostico-por-etapa.md` (sintoma, causa candidata, o que medir) · `references/projetado-x-realizado.md` (o molde da comparação e os 3 deltas).

### Passo 0. Colete os números, numa pergunta só

Comece pelos **9 números da semana** e pela **fonte de cada um**. Faltando algum, peça tudo que falta numa única mensagem. Ancore também na meta, no ticket, na projeção e no histórico; sem eles sobra o benchmark genérico, e isso vai declarado em uma linha. Detalhe em `references/coleta-e-fontes.md`.

### Passo 1. Confiabilidade ANTES da leitura (bloqueante, não pule)

Chutar em cima de dado ruim é pior que não medir, porque gera decisão errada com cara de fato. Antes de ler qualquer taxa, rode os 4 testes: **amostra** (o volume sustenta a taxa?), **janela** (o período cobre o ciclo de venda inteiro?), **rastreio** (clique, etiqueta e origem batem entre si?), **atribuição** (a venda desta semana veio do lead desta semana?).

**Os pisos de amostra, que decidem se a etapa pode ou não virar recomendação:**

| Etapa | Piso pra ler a taxa | Abaixo do piso |
|---|---|---|
| Alcance por peça | 3 peças no período | lê peça a peça, não taxa média |
| Engajamento qualificado | 1.000 de alcance somado | só direção, não decisão |
| Cliques | 30 cliques | não compara com faixa |
| DMs qualificados | 10 DMs | não calcula a taxa de DM para conversa |
| Conversas para reunião | 10 conversas | não calcula agendamento |
| Reunião para fechamento | 10 reuniões realizadas | **nunca** conclui sobre o closer |
| Teste entre duas variantes | 1.000 impressões por variante | não declara vencedor |

A regra do fechamento é a mais violada. Com 4 reuniões e 1 venda ninguém sabe se o script está ruim: a diferença entre 25% e 50% nesse volume é uma reunião. A skill diz isso, em vez de mandar treinar o closer.

**Teste reprovado, a saída é como medir direito, não a recomendação:** escreva `AMOSTRA INSUFICIENTE` ou `RASTREIO QUEBRADO`, diga quanto falta e em quantas semanas o piso chega no ritmo atual, e siga o diagnóstico só pelas etapas que passaram. A janela mínima por ticket e os moldes de recusa estão em `references/confiabilidade-do-dado.md`.

### Passo 2. Calcule a conversão de CADA etapa e mostre a conta

Não descreva, calcule: `etapa N+1 ÷ etapa N`, uma linha por etapa, o real ao lado da referência.

```
DM → conversa:      12 ÷ 31 = 39%  · faixa 25-50% · VERDE
conversa → reunião:  3 ÷ 12 = 25%  · faixa 25-45% · VERDE (no limite)
reunião → venda:     0 ÷ 3  =  0%  · [AMOSTRA INSUFICIENTE, piso 10]
```

**A faixa baixa é o padrão**, a faixa alta só com 60 ou mais dias de histórico próprio acima dela. **Do mês 3 em diante o benchmark sai e entram as taxas próprias:** quando referência e histórico discordam, vence o histórico. Faixas e pisos de vazamento em `references/funil-etapa-a-etapa.md`.

### Passo 3. Nomeie UM gargalo (a primeira etapa vermelha)

A regra não é "a pior taxa", é **a primeira etapa vermelha de cima pra baixo**: mexer na etapa 6 com a 2 furada é remendo num cano que segue vazando. Vermelho é abaixo de 70% da referência, amarelo entre 70% e 99% (monitora, não mexe), verde na faixa ou acima. Nomeie em **uma frase**. Detalhe em `references/diagnostico-por-etapa.md`.

### Passo 4. Feche o loop projetado contra realizado

Diagnóstico sem a meta é conserto sem destino. Compare com a projeção em **três deltas**: **volume** (entrou menos gente), **taxa** (entrou o volume e converteu menos), **receita** (volume e taxa bateram, o ticket caiu). Cada um pede conserto diferente, e confundi-los é o erro mais caro. **Nenhuma recomendação sai sem o delta na tela:** `projetado 40 DMs · real 23 · delta -42%`. Molde em `references/projetado-x-realizado.md`.

**A exceção, e é a única (fecha a contradição com o Passo 7).** Quando o dono não declarou meta nem projeção, não existe delta pra calcular, e aí a regra "nenhuma recomendação sem delta" NÃO paralisa a entrega: ela determina qual é a ação única. **Sem meta declarada, a ação única do Passo 7 é obrigatoriamente medir ou declarar a meta**, com alvo e prazo, nunca uma recomendação de operação (mudar gancho, subir verba, trocar oferta). Escreva no diagnóstico, com essa grafia: `Sem meta declarada: a ação única deste ciclo é de medição.` A recomendação de operação volta a ser permitida no ciclo seguinte, quando existir meta contra a qual medir.

### Passo 5. Separe o número que decide do de vaidade

Dois filtros na mesma peça: **algorítmico** (ficou acima do típico do próprio perfil?) e **financeiro** (tem chance de virar cheque?). **Divergiu, o financeiro vence:** peça abaixo da média que trouxe venda fica; peça acima da média que não move nada manda reavaliar a segmentação, não replicar. Vaidade é curtida absoluta, seguidor total, impressão inflada. O retorno sobre o anúncio isolado entra na lista: número de palco não é o que paga a conta, e um valor muito alto costuma sinalizar subinvestimento.

### Passo 6. Responda "por que não converteu"

Pergunta aberta não se responde com opinião. Desça a escada: **sintoma → etapa onde o número parou → causa candidata → o que medir pra confirmar → ação**. O mesmo anúncio quebra em lugar diferente conforme onde parou: não viu (entrega e público), viu e não clicou (criativo e promessa), clicou e não virou lead (página e mensagem), virou lead e não comprou (oferta, preço ou conversa).

### Passo 7. Entregue UMA ação e faça o repasse

Uma ação por ciclo, medida no ciclo seguinte, com o alvo declarado antes. Cinco ações juntas destroem o aprendizado, porque nada fica atribuível.

**A ação única existe sempre, e o Passo 4 diz de que tipo ela é.** Com meta e delta na tela, a ação é de operação. Sem meta declarada, ou com teste de confiabilidade reprovado, a ação única é de medição ou de rastreio (declarar a meta, instalar a etiqueta, montar a coorte), com alvo e prazo iguais aos de qualquer outra ação. Nunca entregue "nenhuma ação"; nunca entregue ação de operação sem delta.

**O repasse pra outra skill não é um nome solto no fim da mensagem.** Ele sai com quatro campos, sempre:

```
AÇÃO ÚNICA DO CICLO
  o quê:     reescrever o gancho dos 3 primeiros segundos dos próximos 4 reels
  por quê:   retenção 3s em 31%, faixa baixa é 50%, é a primeira etapa vermelha
  alvo:      retenção 3s acima de 45% na média das 4 peças
  quando medir: próxima leitura, 7 dias, com os mesmos Insights do Reel

REPASSE
  skill:     soft-conteudo-reels
  leve isto: retenção 3s atual 31% · alvo 45% · avatar e promessa que já rodam
             hoje · as 2 peças que passaram de 45% no último mês, como referência
  o que NÃO peça lá: mudança de oferta ou de público, isso não é o gargalo desta semana
```

O mapa de destino por causa: gancho ou copy fraca → `soft-conteudo-reels`, `soft-conteudo-carrossel`, `soft-conteudo-headlines` · público errado ou promessa desalinhada → `soft-plano-posicionamento` · oferta ou preço → `soft-plano-posicionamento` · objeção na conversa → `soft-vendas-closer` · verba e segmentação do anúncio → `soft-trafego-meta`. Se a skill de destino não estiver instalada, faço aqui o mínimo: entrego a ação escrita e o alvo, sem produzir a peça.

### Passo 8. Rode o gate e PARE

Confira em silêncio (a tabela nunca vai pra saída), mostre a leitura limpa, e pare. O gate está no bloco próprio, mais abaixo.

---

## Ação 2 · COMPARAÇÃO ENTRE PERÍODOS (o que mudou, e por causa de quê)

**O que faz:** compara dois períodos e decompõe a diferença de receita nos fatores que a causaram, em vez de dizer só "caiu".

**Precisa de:** os mesmos 9 números em **dois períodos** de igual duração, com a mesma fonte · o que mudou entre eles que o dono saiba (peça nova, verba diferente, feriado, mudança de oferta).

**Sem o insumo:** um dos períodos incompleto, compare só as etapas que existem nos dois e diga em uma linha quais ficaram de fora. Períodos de duração diferente não se comparam em valor absoluto: normalize pra taxa, ou recuse a comparação e explique por quê. Sem saber o que mudou entre os períodos, pergunte isso e só isso.

**Entrega:** `comparacao-<periodo-a>-vs-<periodo-b>.md`, com a tabela lado a lado, a decomposição da diferença, e a leitura em uma frase. Roda depois do diagnóstico, ou sozinha quando o dono só quer saber se melhorou.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/projetado-x-realizado.md` (a mesma lógica dos 3 deltas serve aqui) · `references/funil-etapa-a-etapa.md`.

### Como decompor a diferença

Receita é produto de fatores. Quando ela muda, a pergunta útil é qual fator mudou, e o método é mexer num fator por vez, mantendo os outros no valor do período A:

```
Período A (05 a 11/03) → Período B (12 a 18/03): receita 8.400 → 5.600 · delta -2.800 (-33%)

Decomposição, um fator por vez:
  1. leads:            31 → 23   (-26%)   efeito na receita:  -2.180
  2. taxa lead→reunião: 39% → 41% (+5%)   efeito na receita:    +290
  3. taxa reunião→venda: 25% → 22% (-12%) efeito na receita:    -640
  4. ticket médio:     2.800 → 2.800 (0%) efeito na receita:      -0
                                          soma dos efeitos:   -2.530
  resíduo de interação (fatores mudando juntos):                 -270
                                          total conferido:    -2.800

Leitura: a queda é de VOLUME. O funil converteu igual ou melhor;
entraram 8 leads a menos e isso responde por 78% da diferença.
```

Regras da decomposição:

- **A soma tem que fechar com o delta real.** Não fechou, tem número errado ou etapa faltando. Não entregue uma decomposição que não reconcilia.
- **O resíduo entra declarado**, não distribuído nos fatores pra ficar bonito.
- **Um fator só costuma dominar.** Nomeie ele em uma frase e trate os outros como ruído do período, a menos que dois passem de 25% do delta cada.
- **Etapa que reprovou no teste de amostra num dos períodos fica fora da decomposição**, marcada, porque comparar duas taxas instáveis produz uma terceira mais instável ainda.
- **Variação abaixo de 10% em período curto é ruído**, não tendência. Diga isso em vez de inventar causa.

Quando a comparação é entre mês e mês, ou trimestre e trimestre, o mesmo formato serve, e aí o resíduo importa menos porque os volumes são maiores.

---

## Ação 3 · ESCALA (o funil em reais e o tamanho do time)

**O que faz:** responde duas perguntas que só aparecem quando a operação cresce, "vale escalar o tráfego?" e "quantas pessoas eu preciso, e quando contrato?".

**Precisa de:** o funil em dinheiro (custo por lead, custo por agendamento, custo por comparecimento, custo por call realizada, e o faturamento por call realizada) · o volume de leads por mês e a capacidade atual do time.

**Sem o insumo:** sem os custos, esta ação não roda; peça os 5 números numa mensagem só. Sem o faturamento por call, a decisão de escala fica `[A DEFINIR com o dono]` e a skill entrega só o custo, sem o veredito.

**Entrega:** a tabela das 5 contas em dinheiro com a leitura de escala, ou a régua de capacidade com o gatilho de contratação, conforme a pergunta.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/funil-em-reais.md` (as 5 contas e a decisão de escala) ou `references/dimensionamento-de-time.md` (capacidade por função e gatilhos), conforme o caso.

Esta ação vale em **operação com time e escala**, e convive com o modo de atendimento individual em vez de substituí-lo. É a leitura própria de esteira que fecha em call, com ticket acima de cerca de R$3.000. As réguas de capacidade e os quatro degraus de meta estão na reference; a leitura de retorno sobre anúncio segue a do passo 5, valor muito alto sinaliza subinvestimento.

---

## Gate de qualidade (antes de mostrar a leitura)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


Confira em silêncio. Item reprovado refaz o passo dele, não a análise inteira:

1. **Fonte e data em toda métrica.** Número sem origem vira `[FONTE?]`, não vira conclusão.
2. **Confiabilidade rodada.** Os 4 testes passaram, ou a saída virou "como medir direito" nas etapas que reprovaram.
3. **A conta na tela.** Toda taxa aparece como divisão, não como adjetivo.
4. **O delta escrito.** Nenhuma recomendação sem `projetado X · real Y · delta Z%`.
5. **Um gargalo só**, e é a primeira etapa vermelha de cima pra baixo, não a pior taxa.
6. **Uma ação só**, com número-alvo e prazo de medição declarados antes.
7. **Repasse com os quatro campos** (skill, o que levar, o que não pedir lá), não um nome solto.
8. **Zero benchmark inventado.** Sem referência do dono, `[A DEFINIR com o dono]`.
9. **Comparação que fecha.** Quando houver decomposição, a soma dos efeitos mais o resíduo bate com o delta real.
10. **Anti-IA.** Zero travessão, zero verbo da família banida pela régua anti-voz, sem caixa alta em texto corrido. A régua está em `shared-references/filtro-anti-ia/padroes-banidos.md`; na prática, faça a busca dos dois padrões duros no texto antes de mostrar.

## O que esta skill NÃO faz

Em toda rota abaixo: se a skill de destino não estiver instalada, faço aqui o mínimo e digo o que ficou de fora.

- **Montar a projeção, a rotina ou o plano do zero** → `soft-leon`. Esta skill lê o número contra uma projeção que já existe; quem constrói a projeção é a outra.
- **DRE, margem, preço, capital de giro, fluxo de caixa** → `soft-financeiro`. Aqui o dinheiro entra só como receita e ticket dentro do funil.
- **Decidir verba, público e o que turbinar** → `soft-trafego-meta`. Esta skill diz que o gargalo é o anúncio; ela não escolhe o valor nem a segmentação.
- **Reescrever a peça que converteu mal** → `soft-conteudo-*`. O diagnóstico sai daqui com o alvo; a peça nasce lá.
- **Carta, página ou funil** → `soft-funil-*`.
- **Script de venda e objeção** → `soft-vendas-closer`.
- **Oferta, ticket e posicionamento** → `soft-plano-posicionamento`.

## References

- `references/coleta-e-fontes.md` (passo 0): os 9 números, onde medir cada um, a pergunta única.
- `references/confiabilidade-do-dado.md` (passo 1, bloqueante): os 4 testes, os pisos, o prazo de janela por ticket, os moldes de recusa.
- `references/funil-etapa-a-etapa.md` (passo 2): as 7 etapas, fórmulas, faixas, piso de vazamento, migração pra taxa própria.
- `references/diagnostico-por-etapa.md` (passo 3): sintoma, causa candidata, o que medir; vazamento por estágio de consciência.
- `references/projetado-x-realizado.md` (passo 4 e ação 2): o molde da comparação, os 3 deltas, a revisão semanal, mensal e trimestral.
- `references/funil-em-reais.md` (ação 3): as 5 contas em dinheiro e a decisão de escala.
- `references/dimensionamento-de-time.md` (ação 3): capacidade por função, metas em 4 degraus, gatilhos de contratação, as 3 formações.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** quando a ação já crava o nome, o nome da ação manda e a regra de slug não se aplica. O diagnóstico da Ação 1 sai como `diagnostico-AAAA-MM-DD.md`, com a data da leitura, nunca com slug de tema. Só entrega sem nome cravado na ação usa slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras.
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `shared-references/crivo/07-regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `shared-references/crivo/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
