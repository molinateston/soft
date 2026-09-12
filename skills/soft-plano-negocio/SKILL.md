---
name: soft-plano-negocio
description: >-
  Monta o plano de negócio do especialista num doc só: onde ele está por número real, a meta de caixa, A Conta (cabe na vida?), a projeção em 3 cenários com premissa escrita, o Score de Nicho quando o nicho está em aberto, e o roadmap de 90 dias. Use quando o pedido for: "meu plano de negócio", "faz minha projeção", "quanto vou faturar", "que meta é realista", "faz a Conta", "quantos clientes eu preciso", "monta meu roadmap", "plano de 90 dias", "que nicho eu escolho", "vale a pena estreitar meu nicho". NÃO use pra: "cabe na minha rotina" e o dilema solto do fundador, que é a leitura curta da soft-leon; o mês de conteúdo (soft-conteudo-planner); posicionamento, marca e PUV (soft-plano-posicionamento); desenhar a oferta com stack, garantia e preço (soft-plano-ofertas); diagnosticar o funil por métrica (soft-negocio-metricas); DRE, margem e dívida (soft-financeiro). Leia e siga o fluxo inteiro do SKILL.md.
---

# O plano de negócio: onde está, a meta, a Conta, a projeção, o roadmap

Esta skill produz o documento que o especialista recebe, reabre e usa como bússola. Junta num lugar só o que sairia espalhado: onde ele está por número real, a meta de caixa, A Conta que diz se a meta cabe na vida dele, a projeção em 3 cenários com premissa escrita, o Score de Nicho quando o nicho está em aberto, e o roadmap de 90 dias. Não cria método novo e não inventa número: consolida e projeta o que o negócio JÁ tem.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **Verificador de lastro (obrigatório antes de pronto):** depois do gate e ANTES de dizer pronto, roda o segundo par de olhos de `references/10-verificador-lastro.md` (cego à peça, no papel de verificador) contra o perfil e os insumos do dono, conferindo cada afirmação (número, meta, conta, fato de oferta, promessa) e consertando ou removendo o que estiver sem lastro; a tabela `afirmação | lastro (arquivo:trecho) ou REMOVIDA` mora no bastidor, e sem ela a entrega não está pronta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Os títulos das etapas são teses, não rótulos.** `## P3` é numeração; `## P3: cada peça existe para impedir uma desistência específica` é a etapa dizendo o que decidiu. A isenção de rótulo estrutural vale pra cabeçalho de anexo, de tabela e de fonte, **nunca pras etapas do plano**: renomear uma etapa pra caber na isenção reprova a entrega, porque troca a qualidade da peça pela facilidade do gate, e o `--conferir` imprime cada caso como `rótulo no miolo: <linha>`. Cole `etapas: N · com tese no título: N`, iguais. **E nenhum cabeçalho nomeia um requisito da régua:** `Seção de fecho`, `Frase que sobrevive`, `Checagem`, `Inventário` e `Régua` são nomes do gate. A frase que sobrevive entra no fecho sem cabeçalho próprio, ou sob um cabeçalho que seja ela mesma. Cole `cabeçalhos que nomeiam um requisito do gate: 0`.

**A entrega tem um documento-mãe, e ele é o `Abra primeiro`.** O `PLANO-DE-NEGOCIO.md` é obrigatório e é sempre o `Abra primeiro:`; traz numa página a meta em destaque, a conta de horas com veredito, os três cenários e os três próximos passos. Entrega sem ele reprova, mesmo com as quatro seções completas. Numeração de arquivo é contínua, nunca pula de 03 pra 05. Com número faltando, a projeção entrega faixas mais perguntas, nunca página em branco, e a conta é reproduzível: a fórmula fica escrita. Cole `documento-mãe presente: sim · Abra primeiro aponta pra ele: sim`.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício de ponta a ponta: os números que o dono deu, o estágio identificado, A Conta que não fechou e o ajuste escolhido, os 3 cenários com premissa, o Score de Nicho e o roadmap de 90 dias fechando em ações datadas. Ler antes economiza uma rodada de retrabalho.

**Quantas perguntas o dono vai responder.** **Cinco, no mínimo, e no máximo nove.** As 5 do diagnóstico de partida são obrigatórias e vêm no começo, uma por vez. Mais 4 condicionais, que só aparecem se o caso pedir: as horas por cliente (quando A Conta roda), a escolha do ajuste (quando A Conta não fecha), o nicho em aberto (quando o Score dispara) e o canal de venda que ele usa hoje (quando a projeção precisa da taxa). Diga isso ao dono na primeira mensagem, pra ele saber o tamanho do caminho.

**O perfil do dono vem do banco do agente.** Onde qualquer ação precisar de oferta, ticket, avatar ou prova: leia do perfil/brain do agente quando existir; se não existir, pergunte, uma por vez. Nunca invente número, nunca crie arquivo de perfil.

**Levantamento BLOQUEANTE antes de escrever (roda como a ancoragem do gate, e é COMANDO, nunca de memória).** Antes de montar qualquer peça, LEIA o perfil e os insumos do dono e cole no processo uma linha por dado-chave, nesta forma: `<campo> | <valor encontrado> (<arquivo>:<trecho>) | ou [A CONFIRMAR] só se o ls/leitura devolveu vazio`. Os campos-chave desta skill: faturamento médio, mix com ticket, meta de caixa, horas por semana, tráfego, pró-labore desejado, custo fixo, dívida, reserva. **Marcar `[A CONFIRMAR]` um dado que EXISTE no insumo reprova a entrega**, então rode a leitura antes de decidir: com shell, `grep -niE 'pro.?labore|custo fix|divida|reserva|faturament|ticket|meta' <perfil>` e cole a saída. A tabela de levantamento fecha com `campos-chave: N · encontrados no insumo: N · [A CONFIRMAR] com leitura vazia comprovada: N`, e a soma fecha em N. Só depois desta tabela a peça começa.

**O exemplo é ILUSTRATIVO, é PROIBIDO parafrasear.** `references/EXEMPLO-FIM-A-FIM.md` usa um nicho fictício só pra mostrar a FORMA. É proibido reusar as frases, os números ou o nicho dele na peça real. A peça real nasce 100% do insumo do dono; se você se pegar copiando uma frase do exemplo, pare e volte ao insumo.

---

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola tudo que tem, os números e a meta, e eu monto o plano). Se quiser ser guiado passo a passo (te pergunto cada número e cada meta, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou. Se faltar um número que o plano não vive sem (faturamento hoje, a meta, o ticket), pergunta AQUELE número e segue.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o diagnóstico dos 5 números uma pergunta de cada vez, e monta o plano com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda o plano (o estágio pela leitura dos 5 números, a Conta antes da projeção, o funil reverso, o recorte do roadmap), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a planejar sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier redonda demais ("uns 20 mil por mês", "quero dobrar"), não monta o plano em cima do chute. Pede o dado real: o faturamento exato dos últimos meses, o ticket que ele de fato cobra, quantos clientes fechou. Número real vira projeção confiável; chute vira plano frágil. Puxa uma vez; se o dono só tiver o aproximado, segue e marca a premissa em uma linha.

**Oferece refinar no fim (parte 4):** depois de mostrar o plano, fecha com UMA linha: "Quer rodar a projeção com outra meta, outro ticket, ou outro prazo? Me diz que eu refaço a conta." A oferta de refino não substitui o gate.

**Jargão do método fica no bastidor, NUNCA na entrega pro dono leigo (checagem que reprova).** Os nomes internos do método são ferramenta de quem monta o plano, não vocabulário do dono. Na entrega escrita, fale em português simples: "seu estágio hoje" no lugar de **Pré-Desemperrar/Desemperrar/Escalar**, "vale a pena focar num nicho mais estreito?" no lugar de **Score de Nicho**, "as taxas de referência que ainda vou calibrar com os seus números" no lugar de **benchmark cego**, "subir o ticket / concentrar as ofertas / rebaixar a meta / abrir mais horas" no lugar de **Ajuste 1/2/3/4**. Antes de fechar, dê um grep na entrega pelos termos internos (`grep -niE 'pré.?desemperrar|desemperrar|score de nicho|benchmark|ajuste [0-9]' <entrega>`); qualquer ocorrência num arquivo que o dono lê reprova. O jargão pode viver no processo/handoff interno, jamais no doc que o dono abre.


## ⚠️ ENTREGA = UM doc, sempre

O resultado desta skill sai como **um documento markdown consolidado**, no formato mapa-mental (macro-tópico mais bullets com número). A condução (as perguntas do diagnóstico, as escolhas de ajuste, os STOPs) acontece no chat; o PLANO mora no doc. Ao parar num STOP, você mostra ou atualiza o doc e pergunta "ajusto?"; nunca reescreve o plano em pedaços na conversa. Sem o doc entregue, a skill não terminou.

- **Ambiente que renderiza markdown:** mostre o documento inteiro ali.
- **Ambiente com disco:** salve o arquivo `.md` e cite o nome dele na resposta.
- **Canal que anexa arquivo:** gere o `.md` e cite o nome; a condução vai em mensagens curtas, sem markdown pesado.
- **Se o dono pedir o plano publicado como página:** o motor de site é da `soft-vendas-proposta` e a identidade visual é da `soft-designer`. Se qualquer uma das duas não estiver instalada, faço aqui em modo reduzido, entregando o `.md` e dizendo em uma linha o que ficou de fora.

---

## Duas leis que vêm antes de tudo

1. **Sem número real, não existe plano. Nunca invente.** Falta o faturamento, o ticket, as horas, o investimento? Pergunte, uma por vez, ou marque `[A CONFIRMAR]`. Jamais calcule com número plausível, jamais use "média do mercado". Dono que dá faixa ("uns 8k a 12k"), você pede o exato: "soma os 3 meses, divide por 3, me dá o número."
2. **Projeção sempre em 3 cenários com premissa escrita.** Nenhum cenário sem premissa (quanto executa, se liga tráfego, se a bola de neve das provas já roda). A régua de realismo é obrigatória antes de mostrar.

**O padrão quando faltam números: a versão com FAIXAS mais a lista de perguntas, nunca a página em branco.** Faltando qualquer um dos 5 números obrigatórios, esta skill não entrega a projeção fechada. Ela entrega o que dá pra entregar: o diagnóstico do que já dá pra ler, as contas que fecham com o que existe (20 alunas a tal ticket dá tanto), e a projeção em FAIXA declarada como faixa, com a premissa escrita ao lado de cada ponta. Faixa não é número assumido: ela mostra o tamanho do intervalo e diz que o número exato depende da resposta do dono.

**A entrega em branco reprova tanto quanto o número inventado.** Uma tabela inteira de `[A CONFIRMAR]` devolve ao dono uma planilha vazia, e ele leu isso como "não fez nada": um dos dois motores entregou assim e o dono não pagaria. O outro entregou a conta de 20 alunas e serviu, mesmo parcial. Então: nada de página com projeção só de marcador, nada de nome de arquivo gritando o bloqueio (`03-projecao-NAO-LIBERADA.md` parece defeito do sistema pra quem abre a pasta; o arquivo se chama `03-projecao-em-faixas.md` e o aviso mora na primeira linha dentro dele).

**O aviso vai no topo, em uma linha, e as perguntas vão numa lista só, no fim.** A primeira linha do documento diz o que está parcial e por quê, em português. As pendências não ficam espalhadas pelo miolo: elas viram a seção final `Perguntas pra você`, cada uma escrita como pergunta que o dono responde num áudio de 10 segundos ("qual foi seu faturamento em junho e em julho?"). Entregar projeção com número assumido continua sendo a falha grave desta skill. Checagem verificável antes de fechar: some os marcadores `[A CONFIRMAR]` da entrega; se for maior que zero e o doc trouxer projeção fechada como se fosse exata, reprova; e se for maior que zero sem a seção `Perguntas pra você`, reprova também.

---

## Roteamento por pedido

| O dono pediu | Ação |
|---|---|
| "meu plano de negócio", "monta o plano fechado", "consolida tudo" | **Ações 1 a 5, na ordem, com STOP em cada** |
| "onde eu tô", "que estágio é o meu", "diagnostica meu negócio" | **Ação 1 · DIAGNÓSTICO** |
| "faz a Conta", "quantos clientes eu preciso", "cabe na minha rotina" | **Ação 2 · A CONTA** |
| "minha projeção", "quanto vou faturar", "que meta é realista" | **Ação 3 · PROJEÇÃO** |
| "que nicho eu escolho", "meu nicho vale a pena", "vale estreitar" | **Ação 4 · SCORE DE NICHO** |
| "roadmap", "plano de 90 dias", "por onde começo essa semana" | **Ação 5 · ROADMAP** |

Pedido ambíguo ("me ajuda a planejar"): pergunte UMA coisa só, o que ele quer decidir com o plano, mostre a tabela como cardápio e siga.

**O roadmap de 90 dias sai sempre no plano completo**, e é ele que fecha o doc. Sozinho, só quando o dono pede por nome. Ele nunca é opcional dentro do plano fechado: plano sem próximos passos datados é relatório, não bússola.

---

## Ação 1 · DIAGNÓSTICO (os 5 números, e o estágio)

**O que faz:** coleta os 5 números de partida e nomeia o estágio do negócio, que é o que calibra todo o resto.

**Precisa de:** faturamento médio dos últimos 3 meses · mix de oferta com ticket de cada · meta de caixa em 6 meses · horas reais por semana · investimento mensal em tráfego. Tudo perguntado ao dono, um por vez.

**Sem o insumo:** não estime e não use média do mercado. **Se o dono não tiver o número na mão: sai a versão em faixas, e a skill avisa isso na primeira linha.** O que sai é o máximo honesto: as contas que já fecham com o que existe, a projeção em faixa com a premissa de cada ponta, e a lista das perguntas que fecham o número exato. Se ele der 3 dos 5 (faturamento, ticket e meta), sai um **plano parcial**, com A Conta e o roadmap, sem a projeção em 3 cenários, e o doc declara no topo que é parcial e o que falta.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `01-diagnostico.md`, com os 5 números, o estágio nomeado e o teto de crescimento realista dele. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/diagnostico-partida.md` (as 5 perguntas duras, como tratar resposta vaga, os 3 casos de plano inviável).

**Profundidade:** `references/entregavel-e-output.md` (o esqueleto do doc consolidado).

### Os 5 números

1. **Faturamento médio dos últimos 3 meses.** Exato, não faixa. "Pega os 3 últimos meses fechados, soma o que entrou de cliente pagante, divide por 3."
2. **Mix de oferta atual mais o ticket de cada.** Mais de 3 ofertas, corta pra 1 ou 2.
3. **Meta de caixa em 6 meses.** Caixa é o que sobra depois de custo direto e imposto, não receita. "Quanto quer embolsar no mês 6, líquido?" **Obrigatório LER e USAR os campos financeiros do perfil antes de marcar esta linha:** pró-labore desejado, custo fixo, dívida, reserva. **A meta de caixa NUNCA sai `[A CONFIRMAR]` quando o perfil traz pró-labore:** a meta mínima deriva do pró-labore desejado, mais o aporte de reserva e a parcela mensal da dívida quando existirem. **O custo fixo NÃO entra aqui:** ele já sai na margem de caixa da projeção (ver a ORDEM CERTA na Ação 3). Somar o custo fixo na meta E dividir pela margem que já o desconta conta o mesmo custo duas vezes; esta é a conta que reprova o gate. Cole a conta na entrega, na forma `3.500 (pró-labore) + 2.300 (reserva) + 276 (parcela da dívida) = 6.076` com os números do dono, e declare que é o piso derivado, não o teto. Só marque `[A CONFIRMAR]` se a leitura do perfil devolveu vazio nesses campos, e cole a leitura que comprova o vazio.
4. **Horas reais por semana.** Real, não ideal. Já descontando a entrega dos clientes atuais, a vida e a operação base.
5. **Investimento mensal em tráfego.** Pode ser R$0.

### O estágio (é o que calibra o resto)

| Faturamento médio | Estágio | Crescimento máximo realista no mês 6 |
|---|---|---|
| R$0 a R$5k por mês | Pré-Desemperrar | 5x a 10x (o salto sai da inexistência) |
| R$5k a R$15k por mês | Desemperrar | 3x a 5x |
| R$15k a R$50k por mês | Escalar | 2x a 3x |
| R$50k a R$150k por mês | Estabilizar | 1,5x a 2x |
| R$150k por mês pra cima | Verticalizar | 1,3x a 1,8x |

Nos `references/` deste diretório o mesmo estágio às vezes aparece com o nome antigo, formado sobre o verbo que a régua anti-voz proíbe. É o mesmo estágio, mesma faixa, mesmo teto.

**Fronteira do posicionamento:** se o especialista não tem posicionamento cravado (nicho, oferta, mecanismo), o plano projeta em cima do vazio. Avise: *"o plano precisa de posicionamento cravado pra número não virar chute. Roda a `soft-plano-posicionamento` antes, ou seguimos com o ticket-base do que o método sustenta no seu nicho e recalibramos depois."*

---

## Ação 2 · A CONTA (cabe na vida? o freio antes da projeção)

**O que faz:** calcula se a meta cabe na semana real do especialista, e escolhe o ajuste quando não cabe.

**Precisa de:** a meta de caixa e o ticket médio, da Ação 1 · as horas por cliente do começo ao fim, contando deslocamento, perguntadas ao dono · as horas disponíveis por semana, da Ação 1.

**Sem o insumo:** sem as horas por cliente, pergunte só isso, é a única que falta ("quantas horas cada cliente te consome do começo ao fim?"). Sem resposta, use a faixa de `references/a-conta.md` pro tipo de atendimento dele, marque `[A CONFIRMAR]` e avise em uma linha que o número precisa ser confirmado.

**Entrega:** `02-a-conta.md`, com a conta rodada linha a linha, o veredito (cabe ou não cabe) e, quando não cabe, o ajuste escolhido pelo dono. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/a-conta.md` (A Conta em 4 etapas, os 4 ajustes em ordem, as faixas de horas por tipo de atendimento).

**Profundidade:** `references/esteira-e-conta.md` (a esteira mínima viável e como ela se calibra pela meta).

```
Meta de caixa ÷ ticket médio        = clientes necessários por mês
clientes × horas por cliente
  + horas de produção de conteúdo
  + horas de operação (venda, follow-up, administração)
  + horas de aprendizado
                                     = TOTAL de horas por semana exigidas
```

- **Exigido menor ou igual ao disponível:** cabe. Segue pra projeção.
- **Exigido maior que o disponível:** não cabe. Aplica um ajuste, **nesta ordem de preferência**:
  1. **Subir o ticket** (preferido: mantém a meta, reduz o volume, melhora o cliente).
  2. **Refazer a esteira** (concentra em 1 ou 2 ofertas premium; o ticket médio sobe).
  3. **Baixar a meta** (calibragem, não desistência: "R$35k em 6 meses, R$50k em 12").
  4. **Subir as horas** (último recurso, só por janela de até 90 dias, com revisão marcada).

**Não é ajuste aceitável:** trabalhar de madrugada, cortar tempo com família, sacrificar saúde, "vai apertado mas dou conta". O plano não aceita.

**STOP obrigatório:** A Conta não fechou? Mostre as 4 opções e deixe o dono escolher, antes de projetar. Pergunte também, quando a meta exige operação pesada: *"olhando esse total de horas e essa meta, você ainda quer isso?"*

---

## Ação 3 · PROJEÇÃO (o funil reverso, três vezes)

**O que faz:** roda o funil reverso três vezes, com premissa escrita em cada, e passa os três pela régua de realismo antes de mostrar.

**Precisa de:** a meta de caixa e o ticket, da Ação 1 · A Conta fechada ou ajustada, da Ação 2 · o canal de venda que ele usa hoje, perguntado a ele, pra escolher as taxas certas.

**Sem o insumo:** sem o canal declarado, use as taxas-âncora do Benchmark na **faixa baixa** e diga em uma linha qual premissa você assumiu. Nunca invente taxa.

**Entrega:** `03-projecao.md`, com a tabela dos 3 cenários (faturamento no mês 6 e anual), a premissa escrita de cada um e a curva mês a mês do realista. Prosa mínima, número protagonista. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/projecao-funil-reverso.md` (a mecânica completa, o Benchmark com as taxas por etapa, as premissas dos 3 cenários, exemplos densos por estágio).

```
META DE CAIXA (mês 6) ÷ margem (caixa sobre receita, ~70%) = RECEITA NECESSÁRIA
  ÷ ticket médio do mix        = VENDAS por mês
  ÷ taxa de fechamento         = CONVERSAS realizadas por mês
  ÷ taxa de comparecimento     = CONVERSAS agendadas por mês
  ÷ taxa de mensagem pra conversa = MENSAGENS qualificadas por mês
  ÷ taxa de clique pra mensagem   = CLIQUES por mês
  ÷ taxa de engajamento pra clique = ENGAJAMENTO qualificado por mês
  ÷ taxa de alcance pra engajamento = ALCANCE qualificado por mês
  ÷ alcance médio por peça     = PEÇAS por mês  ÷ 4 = PEÇAS por semana
  × tempo médio por peça       = HORAS de produção por semana
```

**ORDEM CERTA da conta (checagem que reprova a conta furada).** O custo entra UMA vez só. A margem de caixa (~70%) já é `caixa ÷ receita`, ou seja, já desconta custo fixo, custo direto e imposto. Então:

1. A **meta de caixa** é o que o dono leva pra casa: pró-labore desejado + aporte de reserva + parcela mensal da dívida. **NUNCA some o custo fixo aqui**, porque a margem já vai descontá-lo no passo 2.
2. Divida a meta pela margem: `receita = meta ÷ margem`. É a margem que remove o custo fixo, o custo direto e o imposto da receita.
3. A **parcela da dívida (juros mais amortização) é saída mensal DENTRO da meta de caixa**, no passo 1. Não é "pressão extra" comentada de lado nem some da conta: se o dono paga ~R$276/mês de dívida, esses R$276 entram na meta.

Mini-exemplo CORRETO (dono com pró-labore R$3.500, reserva R$2.300, dívida R$276/mês, custo fixo R$1.180, margem 70%):

```
meta de caixa = 3.500 + 2.300 + 276 = 6.076   (custo fixo FORA: a margem o desconta)
receita necessária = 6.076 ÷ 0,70 = 8.680      (o custo fixo de 1.180 sai aqui, uma vez)
```

Contar o custo fixo duas vezes (somar 1.180 na meta E dividir por 0,70) inflaria a receita pra `10.366` e reprova o gate.

| Cenário | Premissa-chave | O que é |
|---|---|---|
| **Conservador** (piso) | ~60% de execução, orgânico puro, faixa baixa do benchmark, sem nenhum empurrão externo | o número que bate mesmo num mês ruim |
| **Realista** (alvo) | ~80% de execução, tráfego crescente, dentro do benchmark, alguma bola de neve | **a meta oficial do roadmap.** Costura com A Conta |
| **Agressivo** (teto) | execução plena, tráfego no teto, acima do benchmark, 1 premium por mês | o teto quando tudo dá certo. **Não é promessa** |

### A régua de realismo (obrigatória antes de mostrar)

- **Piso ancorado no atual.** O agressivo não multiplica o faturamento num salto que o nicho não sustenta. Quem faz ~R$15k por mês tem teto realista no agressivo em ~R$80k a R$150k em 12 meses, não R$300k.
- **Sem base, sem número.** Projeção que não amarra num benchmark real nem no histórico do próprio dono é marcada como estimativa e puxada pra baixo.
- **Virou fantasia, corta.** Corta 30% a 50% e revisa as premissas. Se cortado continua irreal, o problema é ticket baixo demais ou nicho errado: volta pra Ação 2 ou pra Ação 4.
- **Casa com o estágio.** O teto da tabela da Ação 1 é o limite de cima. Agressivo que estoura é cortado, com o aviso: *"esse patamar o método não cobre em 6 meses; realista é X agora mais Y nos 6 seguintes."*

Se um número intermediário estourar (do tipo "648.000 engajamentos qualificados por mês"), é sinal de premissa irreal: o problema é ticket baixo demais ou nicho pequeno demais. Volte, não force o número.

### Sub-régua: a conta por funil (a camada de portfólio)

Quando o negócio já tem, ou pretende ter, mais de uma frente de monetização, a projeção não fica só na venda agregada: ela nomeia as **3 camadas do portfólio** e mede o lucro de cada uma separado. Detalhe em `references/playbook-ecossistema-funis.md`.

- **As 3 camadas** (a faixa de ticket entra como REFERÊNCIA relatada, nunca como meta; o número do dono manda): compra de base (front, faixa relatada de R$47 a R$997), recompra (ticket baixo, faixa relatada de R$27 a R$67), ascensão (ticket alto, faixa relatada de R$800 a R$3.000, só pra quem já é da base). O plano nomeia as 3 mesmo quando 2 ainda não existem.
- **Lucro medido separado por funil.** Cada camada entra com o próprio lucro numa linha; faturamento sem lucro ao lado não entra. A métrica-mãe é lucro, não faturamento agregado.
- **O teto matemático em cascata**, a conta obrigatória antes de escolher onde investir energia (escalar frio contra monetizar base): roda a cascata (entrada, grupo, comparecimento, conversão, ticket) pros dois caminhos e escolhe o de maior lucro. É um MODELO DE CONTA com os campos vazios pro dono preencher; nenhum percentual é referência da casa. O molde da cascata está no reference.
- **CPA aceitável pelo LTV do ecossistema.** A decisão de mídia usa front mais recompra mais ascensão, com o lucro de cada um medido separado, nunca só o ticket do front. É o que sustenta a régua "a aquisição paga a si mesma", e o vermelho na aquisição só entra com a conta de LTV escrita e a prova do backend na mesa.
- **A ressalva de ouro.** O fechamento do ticket alto continua na SESSÃO, a régua da casa; o modelo relatado que fecha alto ticket no gravado ou no direct fica ABAIXO dela e não a substitui.

---

## Ação 4 · SCORE DE NICHO (só quando o gatilho dispara)

**O que faz:** dá número defensável à decisão de sub-nicho, em vez de decidir no olho.

**O gatilho é objetivo, não é sensação.** Roda quando qualquer um destes três for verdade, e só então:

1. O dono nomeou mais de um nicho como candidato na Ação 1 ("atendo dentista e fisio, não sei qual foco").
2. O faturamento médio ficou abaixo de R$5k por mês com 6 meses ou mais de operação (o nicho não está pagando).
3. A projeção da Ação 3 estourou um número intermediário irreal mesmo depois do corte de 30% a 50% (nicho pequeno demais pro ticket).

Fora desses três, não roda. Nicho que já paga não precisa de score.

**Gate de mercado endereçável (roda ANTES de pontuar).** Antes do score, confira se o mercado do dono é endereçável pra tráfego direto, detalhe em `references/playbook-ecossistema-funis.md`: sem barreira de geolocalização que trave a oferta, sem exigir formação ou licença profissional do comprador, e com massa suficiente pra escalar. Falhou no gate? O que muda é o MODELO DE CONTRATO (implementação avulsa em vez de coprodução por percentual), não o desenho do funil. Vale também o "subir uma casa" no rótulo do produto de entrada: o nome sobe um nível de generalidade pra alargar o mercado endereçável, o mecanismo fica igual.

**Precisa de:** os nichos candidatos declarados pelo dono · a conexão real dele com cada um (história, vivência, expertise), perguntada a ele.

**Sem o insumo:** sem os candidatos nomeados, pergunte só isso ("entre que nichos você está em cima do muro?"). Sem resposta, não pontue nichos que o dono não citou: diga em uma linha que o Score precisa de candidatos e siga o plano sem ele.

**Entrega:** `04-score-de-nicho.md`, com cada candidato pontuado nos 5 critérios, a faixa nomeada e a recomendação com o afunilamento sugerido. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/score-de-nicho.md` (os 5 critérios com as faixas de nota, a regra do afunilamento, o freio do critério 4, exemplo denso).

Cada critério de 0 a 10, soma de 0 a 50:

1. **Dor latente:** quão aguda é a dor. (8 a 10: busca solução ativa, paga rápido.)
2. **Disposição a pagar:** o mercado paga bem, tem caso de ticket alto? (8 a 10: premium é regra.)
3. **Recorrência:** compra de novo, cabe continuado? (8 a 10: fica meses ou anos.)
4. **Conexão pessoal:** história, vivência, expertise real no nicho? (8 a 10: vive o nicho.)
5. **Tamanho e concorrência:** grande o bastante, tem brecha? (8 a 10: espaço aberto.)

**Faixas:** 0 a 20 ruim (repensar) · 21 a 30 fraco (só com argumento forte) · 31 a 40 bom (seguir com confiança) · 41 a 50 ouro (foco total).

**A regra do afunilamento:** nicho macro quase sempre pontua fraco ou bom, por saturação. Pra chegar em ouro, estreita. **O freio do critério 4:** nota alta com conexão pessoal baixa (0 a 3) volta pra mesa, não vira posicionamento fictício. Sem conexão real, sem nicho.

Isto **não substitui** a pesquisa profunda da `soft-plano-posicionamento`, que é a fundação.

---

## Ação 5 · ROADMAP (os 90 dias, fechando em ações datadas)

**O que faz:** transforma o cenário realista em três meses de execução com objetivo, ações por semana, métrica e checkpoint, fechando em 3 a 5 próximos passos concretos e datados pra ESSA semana.

**Precisa de:** o cenário realista da Ação 3 (é dele que a meta do roadmap nasce) · o estágio da Ação 1 (que muda o conteúdo dos 3 meses).

**Sem o insumo:** sem a projeção rodada, use a meta de caixa declarada na Ação 1 como alvo do mês 3 e diga em uma linha que o roadmap está calibrado pela meta e não pela projeção. Sem nem a meta, o roadmap não sai: são as ações que dependem do número, não o contrário.

**Entrega:** `05-roadmap-90-dias.md`, com os 3 meses (Montar e vender · Validar e repetir · Escalar e subir ticket), cada um com objetivo, ações por semana, métrica e checkpoint, mais os 3 a 5 próximos passos datados pra essa semana. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/roadmap-90-dias.md` (os 3 meses semana a semana, o fechamento com os próximos passos, o que muda por estágio, a ponte pros meses 4 a 6).

**Nunca fecha com "estudar mais" ou "pensar melhor".** Cada próximo passo tem verbo, objeto e data.

**A ordem de implementação dos 3 funis** (quando o plano abre a camada de portfólio, detalhe em `references/playbook-ecossistema-funis.md`): primeiro valida a oferta em tráfego direto, depois a narrativa de ativação da base, e só então recompra (pesquisa mais micro-produtos) em paralelo com ascensão (evento pago, webinário). Dono com audiência formada começa pelo evento pago; sem audiência, pelo tráfego direto. A recompra nasce de pesquisa na jornada, nunca de palpite.

**Gatilho de saída do operacional (marco dos meses 4 a 6):** por volta de 8 a 10 pessoas na operação (faixa relatada, não regra fixa), o dono não deveria mais estar no operacional. Entra como marco do roadmap, não como exigência do dia 1.

---

## Gate de qualidade (preencha, imprima e só então libere o plano)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


Preencha a tabela abaixo **no próprio output**, é o artefato visível obrigatório. Qualquer ✗ reprova: corrija e repreencha.

| Check | Passa se (✓) | ✓/✗ |
|---|---|---|
| **Origem do número** | todo cálculo parte de número que o dono deu; o que faltou está `[A CONFIRMAR]`, nunca preenchido com plausível nem "média do mercado" | |
| **Conta conferida** | toda projeção sai com a conta reproduzível ao lado, fórmula e números, na forma `4 × 1.497 = 5.988`. Refaça cada multiplicação e divisão do doc e cole o resultado do recálculo na célula de evidência. Conta que não fecha, mesmo por 1 real, reprova o gate e o doc não sai | |
| **3 cenários com premissa** | a projeção tem os três, cada um com a premissa escrita do que muda entre eles | |
| **Régua de realismo aplicada** | o agressivo está ancorado no atual e no teto do estágio; nada quebrando credibilidade. Fantasia foi cortada de 30% a 50% | |
| **A Conta fecha (ou tem ajuste)** | meta ÷ ticket, clientes, horas confere com as horas disponíveis; se não coube, tem o ajuste escolhido, ticket primeiro, nunca volume | |
| **Nicho com conexão** (se o Score rodou) | nenhum nicho recomendado com o critério 4 baixo. Score alto mais conexão baixa volta pra mesa | |
| **Roadmap fecha com próximos passos** | o plano fecha com 3 a 5 ações concretas e datadas pra ESSA semana | |
| **Marca-neutra** | cor, fonte, logo e prova são do especialista. Zero número de terceiro, zero inventado | |
| **Contrato de formato** | saiu um doc `.md` nomeado, em mapa-mental, com tabela e número acima de prosa | |
| **Anti-IA (HARD), com PROVA** | busque e cole o RESULTADO COMO NÚMERO na célula, não um "ok". Exemplo: `travessão longo U+2014: 0 · verbo-freio banido e flexões: 0`. Zero travessão longo em frase de copy; zero da família do verbo-freio banida pela régua anti-voz, todas as flexões, título incluso; sem frase-emoldura ("a verdade é", "o segredo"); sem verbo-clichê de hype. **Número maior que zero em prosa = ✗ automático, sem exceção.** Com shell, rode um lint de copy sobre o doc final e siga só com saída limpa | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo ✓ = LIBERA o plano | |

**STOP final:** mostre o plano com a tabela do gate preenchida e pergunte se serve ou se quer ajuste, antes de dar por encerrado. Produz, mostra, espera OK.

---

## O que esta skill NÃO faz

Em toda rota abaixo: se a skill não estiver instalada, faço aqui em modo reduzido, com o que esta skill carrega, e marco o que ficou raso como `[A CONFIRMAR]`.

- **Posicionamento, marca, oferta, PUV, nomear mecanismo, tom de voz** → `soft-plano-posicionamento`. Esta skill projeta o negócio; não define quem ele é pro mercado.
- **A oferta desenhada como stack**, com garantia, preço e esteira → `soft-plano-ofertas`.
- **O planejamento do mês de conteúdo, pauta e calendário editorial** → `soft-conteudo-planner`. Aqui o plano diz quantas peças por semana o número exige; lá se decide sobre o que são.
- **Diagnóstico do funil por métrica** ("por que não converteu", "caiu o resultado") → `soft-negocio-metricas`.
- **Preço, markup, margem, DRE, fluxo de caixa, capital de giro, dívida, regime tributário** → `soft-financeiro`. Esta skill projeta o faturamento; não faz a contabilidade.
- **Conteúdo, carta, VSL, landing, funil, script de venda** → `soft-conteudo-*`, `soft-funil-*`, `soft-vendas-*`.
- **A proposta comercial em site pós-call** → `soft-vendas-proposta`.
- **Estratégia de 12 meses ou mais, planejamento de 3 anos** → o método opera em 6 meses. Explique e ofereça o plano de 90 dias mais a curva de 6 meses no lugar.
- **"Por onde começo", "próximo passo", "valida isso"** → `soft-leon`.

## Regras inegociáveis

1. **Sem número real, não existe plano.** Falta, pergunta ou `[A CONFIRMAR]`.
2. **Projeção sempre em 3 cenários com premissa escrita**, e a régua de realismo antes de mostrar.
3. **A Conta antes da projeção detalhada.** Não cabe, sobe o ticket primeiro, nunca o volume. Nenhum ajuste sacrifica vida, saúde ou família.
4. **Nicho sem conexão real não vira posicionamento.**
5. **Roadmap fecha com 3 a 5 próximos passos concretos e datados** pra essa semana.
6. **Marca-neutra.** A prova é sempre real do especialista.
7. **Não cria método novo.** Consolida e projeta o que o negócio já tem, e entrega como um doc.
8. **Tom clínico e direto, sem motivacional.** Tabela e número acima de prosa. O plano é bússola, não relatório de 30 páginas: cabe em uma página visual.

## Anti-Patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Projetou com "média do mercado" ou número plausível pra faltante | Volta pro real: pergunta o exato ou marca `[A CONFIRMAR]` |
| Deu um cenário único ("você vai faturar R$X") | Roda os 3 com premissa escrita; o realista vira a meta do roadmap |
| Agressivo inflado (30x, R$300k pra quem faz R$15k) | Aplica a régua de realismo: ancora no atual mais o teto do estágio, corta de 30% a 50% |
| Meta não cabe na vida e mandou "trabalhar mais" | Aplica A Conta: sobe o ticket primeiro, nunca o volume |
| Rodou o Score de Nicho por sensação | O gatilho é objetivo: só os 3 casos da Ação 4 disparam |
| Recomendou nicho com Score alto e conexão pessoal baixa | Freio do critério 4: volta pra mesa |
| Roadmap fechou com "estudar mais", "pensar melhor" | Fecha com 3 a 5 ações concretas e datadas pra essa semana |
| Dono não deu número e a skill projetou assim mesmo | Sem número, sem plano: lista o que falta e por que cada um segura um pedaço, e para |
| Pingou o plano em pedaços no chat | Um doc consolidado. A condução no chat, o plano no doc |
| Virou plano de estratégia de 3 anos | 90 dias cravados mais a curva de 6 meses |
| Entregou o plano sem a tabela do gate | Sem a tabela preenchida o plano não foi entregue |

## References (profundidade; o fluxo acima é autossuficiente)

- `references/diagnostico-partida.md`: as 5 perguntas duras, como tratar resposta vaga, como identificar o estágio, os 3 casos de plano inviável.
- `references/a-conta.md`: A Conta em 4 etapas, os 4 ajustes em ordem, as faixas de horas por tipo de atendimento, calibragem por estágio, quando refazer.
- `references/projecao-funil-reverso.md`: a mecânica completa do funil reverso, o Benchmark com taxa por etapa e sinal de vazamento, as premissas dos 3 cenários, exemplos densos por estágio.
- `references/score-de-nicho.md`: os 5 critérios com as faixas de nota, as faixas do score, a regra do afunilamento, o freio do critério 4, exemplo denso.
- `references/roadmap-90-dias.md`: os 3 meses semana a semana com objetivo, ações, métricas e checkpoint; o fechamento com os próximos passos; o que muda por estágio; a ponte pros meses 4 a 6.
- `references/esteira-e-conta.md`: a esteira mínima viável, os 2 formatos, os tickets recomendados, como a esteira se calibra pela meta.
- `references/entregavel-e-output.md`: o esqueleto do doc consolidado, a adaptação de output ao ambiente, os invioláveis do entregável.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta, com as 5 ações no formato real da entrega.
- `references/playbook-ecossistema-funis.md`: a camada de portfólio (as 3 camadas com lucro separado, o teto em cascata, CPA pelo LTV do ecossistema, o gate de mercado endereçável, a ordem de implementação e o gatilho de 8 a 10 pessoas), tudo com a régua de número relatado sem prova e a ressalva de que o fechamento do ticket alto continua na sessão. Costura nas Ações 3, 4 e 5.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
