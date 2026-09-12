---
name: soft-plano-ofertas
description: >-
  Desenha, precifica e valida a oferta como stack, da pesquisa de público ao preço: PUV, Equação de Valor, entregáveis com o entregável-tese, prateleira e bônus, garantia do cardápio, ancoragem e esteira de preços. Use quando o pedido for: "desenha minha oferta", "minha oferta não fecha", "monta a stack", "que oferta eu faço pro meu público", "me dá ideias de oferta", "o que os concorrentes vendem", "avalia a oferta do concorrente", "desenha minha escada", "que produto de entrada eu faço", "quanto cobrar por isso", "que garantia eu dou", "monta meu order bump". NÃO use pra: "quanto devo cobrar" quando a conta é de custo, markup, margem ou DRE (soft-financeiro); posicionamento e nomear o mecanismo (soft-plano-posicionamento); a projeção e o roadmap (soft-plano-negocio); o próximo passo do fundador (soft-leon); a oferta dentro do webinar (soft-webinar); o script de venda (soft-vendas-closer); carta e landing (soft-funil-carta, soft-funil-landing). Leia e siga o fluxo inteiro do SKILL.md.
---

# Plano de Ofertas, a engenharia da oferta como stack

Oferta que fecha não é uma lista de itens com preço. É a tese virando produto: uma PUV que costura o posicionamento, uma stack onde cada peça soma valor ou tira fricção, um entregável-tese que só ESTE especialista entrega, uma garantia que inverte o risco e um preço cravado pela Equação, não pelo bolso do cliente. Esta skill desenha qualquer oferta por esse caminho, e trata mentoria, consultoria, curso, comunidade, serviço e produto de entrada como tipos dentro do mesmo molde.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Os arquivos que cada ação exige (`--exige`).** Conferência: `--conferir <pasta> --exige <lista>`, e arquivo ausente sai com exit 1 e `arquivo exigido pela ação ausente: <nome>`.
- Ação A · DESENHO: `--exige plano-de-ofertas.md` · Ação B · AUDITORIA: `--exige auditoria-da-oferta.md`
- Ação C · IDEAÇÃO: `--exige ideias-de-oferta.md` · Ação D · MERCADO: `--exige mapa-de-mercado.md`
- Ação E · ESTEIRA: `--exige esteira-de-ofertas.md` · **Entregar uma das ações num pedido que nomeou duas é entrega incompleta, não escopo reduzido.**

**O último capítulo, bloco ou seção carrega tese no título, como todos os outros.** `Resumo`, `Conclusão`, `Considerações finais`, `Fechamento` e `Recapitulando` são rótulos de estrutura e reprovam a régua. O lugar que o leitor lê por último recebe a frase mais concreta do material, jamais a mais geral. Cole `capítulos: N · com tese no título: N`, iguais.

**O H1 do documento interno carrega o número que o documento mede.** Forma: `<número medido> <o que ele custa ou libera>`. Rótulo de tipo de documento e nome do negócio sozinho reprovam. Cole `H1: <literal> · número medido no H1: sim/não`. **`títulos de abertura: 0` num documento que tem H1 é resultado inválido**, porque o H1 entra no universo da régua, e remover o H1 não é alternativa a escrevê-lo bem: `.md` de peça sem nenhuma linha `^# ` sai com exit 1 e `peça sem H1`.

**Saídas obrigatórias desta ação, no bloco de entrega** (linha por linha, e a ausência de qualquer uma reprova):
`mecanismo do problema: <nome> | substantivo trocado: <original> → <outro mercado> | sobrevive à troca de nicho? sim/não`
`mecanismo da solução: <nome>`
`convites na peça: N · com ação escrita: N · em marcador: 0` · `números não confirmados no perfil: N · publicados na peça: 0`

**Cada item da oferta é conferido contra o que a operação entrega hoje.** Rode `grep -rniE '<cada item da lista de inclusos>' <insumos>` e cole a saída. Item que aparecer numa reclamação, numa cobrança ou num registro de falha entra no handoff com `prometido na peça e em falha na operação: <item> · <arquivo:linha>`, pro dono decidir antes de publicar. A peça que promete o bônus que o cliente atual não está recebendo escreve a próxima reclamação.

**A frase que sobrevive não pode sobreviver à troca de nicho.** A frase-tese da peça passa pelo teste do nicho trocado como qualquer outra linha, e `sobrevive? sim` nela reprova, ao contrário da tabela de checagem. Cole `frase que sobrevive | substantivo trocado: <original> → <outro mercado> | sobrevive? não`. Máxima de marketing que qualquer negócio repetiria não é a frase da dona: é a frase de ninguém.

**Os títulos das etapas são teses, não rótulos.** `## P3` é numeração; `## P3: cada peça existe para impedir uma desistência específica` é a etapa dizendo o que decidiu. A isenção de rótulo estrutural vale pra cabeçalho de anexo, de tabela e de fonte, **nunca pras etapas do plano**: renomear uma etapa pra caber na isenção reprova a entrega, porque troca a qualidade da peça pela facilidade do gate, e o `--conferir` imprime cada caso como `rótulo no miolo: <linha>`. Cole `etapas: N · com tese no título: N`, iguais. **E nenhum cabeçalho nomeia um requisito da régua:** `Seção de fecho`, `Frase que sobrevive`, `Checagem`, `Inventário` e `Régua` são nomes do gate. A frase que sobrevive entra no fecho sem cabeçalho próprio, ou sob um cabeçalho que seja ela mesma. Cole `cabeçalhos que nomeiam um requisito do gate: 0`.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício de nicho neutro com as 5 ações no formato real da entrega: o gate de público com veredito, a PUV nos dois cortes, a Equação instanciada, a stack em tabela com a objeção de cada item, o Mapa de Valor, a garantia escolhida, o preço em slot, o leque de ideação ranqueado, o mapa de mercado pontuado e o mapa da esteira. Ler antes economiza uma rodada de retrabalho.

**O perfil do dono vem do banco do agente.** Avatar, mecanismo nomeado, banco de provas, voz e nicho: leia do perfil/brain do agente quando existir; se não existir, rode a entrevista curta descrita no "Sem o insumo" da ação. Nunca invente número, nunca crie arquivo de perfil.

> **A doutrina-mãe.** A oferta é o que o cliente vai VENDER de fato. Posicionamento raso ainda atrai; oferta rasa não fecha. Cada entregável tem que ser **coerente com o mecanismo**: o que contradiz a tese sai, por mais que "venda bem". Método "sem reunião" não tem oferta com quatro reuniões; método de autonomia não tem pacote que cria dependência. A coerência não é estética, é o que sustenta a venda.

> **A regra de prioridade (40/40/20).** Num resultado de venda, o PÚBLICO pesa ~40%, a OFERTA ~40%, a COPY ~20%. É regra de ORDEM de esforço, não licença: primeiro se crava o público e a oferta (o que esta skill faz), depois se lapida a frase (`soft-funil-carta`, `soft-conteudo-headlines`). O gate anti-IA continua obrigatório em toda frase, e oferta fraca com copy linda é o pior negócio.

**Como o método trata número e exemplo.** Todo exemplo vem em nicho fictício rotulado, e nenhum número (ticket, valor de mercado, resultado) é afirmação universal: ou vira princípio sem número, ou vira slot do dono preenchido COM ele, marcado `[A CONFIRMAR]` até validar. Números de MECÂNICA (a régua de 2x, a régua 10x) ficam, porque são parâmetro do processo.

---

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, padrão em `shared-references/crivo/09-conducao-agente.md` (as quatro partes):
- **Diz o modo, 1x, na primeira mensagem:** "Nesta oferta eu já monto a stack com o brain + o que você colou (o que entrega e pra quem). Se quiser ser guiado passo a passo (te pergunto o que preciso pra montar a oferta, uma coisa de cada vez) em vez disso, é só pedir." Direto (default, roda no silêncio) pula pra execução com o brain do dono + o que ele colou, e só pergunta o insumo que a oferta não vive sem (o que entrega, pra quem, o resultado prometido); guiado, só quando o dono pede explicitamente, faz a entrevista uma pergunta de cada vez.
- **Ensina enquanto faz:** em cada escolha que muda a oferta (PUV, entregável-tese, cada entregável matando uma objeção, bônus sem preço, garantia, régua 10x), UMA linha do porquê, pra o dono aprender a empacotar sozinho na próxima.
- **Puxa o material bruto:** resposta rasa ("meu cliente quer resultado") não segue com o genérico; pede o concreto que só o dono tem (a objeção literal que emperra a venda, um case com número, o que o cliente tentou e não funcionou). Puxa uma vez; se não tiver, segue e marca o furo.
- **Oferece refinar no fim:** depois de mostrar, UMA linha: "Quer outra garantia? Mais um bônus-âncora? Outro preço na régua? Me diz o que ajustar que eu refaço só essa parte." Não substitui o gate nem o crivo adversarial.

## ⚠️ ENTREGA = UM doc, sempre

O resultado sai como **um documento markdown consolidado**, montado ao longo dos STOPs. A condução (perguntas, escolhas, aprovações) acontece no chat; a PEÇA (PUV, stack, Mapa, garantia, preço) mora no doc. Ao parar num STOP, você mostra ou atualiza o doc e pergunta "ajusto?"; nunca reescreve a peça em pedaços na conversa. Sem o doc entregue, a skill não terminou.

- **Ambiente que renderiza markdown como documento:** mostre ali.
- **Ambiente com disco:** salve o `.md` e cite o nome dele.
- **Canal de mensageria:** gere o arquivo e cite o nome; a condução vai em mensagens curtas, sem markdown pesado. Num app que não renderiza documento, o doc vai num bloco de código markdown fechado, separado da condução.

**Antes de escrever qualquer cena com pessoa, rode o passo de nomes.** A pessoa citada costuma ser justamente quem vai ler a peça. Rode antes da primeira linha da abertura:

```
python3 scripts/checar_titulos.py --peca <cada entregável> \
  --insumos <pasta de insumos do dono> --perfil <perfil do dono>
```

Ele imprime `nomes candidatos achados pelo script: N` e, por nome, `autorização no insumo: sim/não` e `mensagem privada: sim/não`. **Nome com `mensagem privada: sim` e `autorização: não` sai da peça** e vira a forma por faixa ("uma aluna na casa dos 50"). Lead com pergunta sem resposta nunca vira cena de abertura. Cole `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada: 0`.

**O marcador é campo, e campo tem tamanho.** Na peça pública ele cabe em `[A CONFIRMAR: <o dado>]`, no máximo 6 palavras, depois de um rótulo e no fim da linha. **O porquê da pendência nunca entra na peça**, vai pro handoff com o número da linha ao lado. O script conta e reprova acima do teto, em `marcadores acima de 6 palavras: N (teto 0)`.

**A frase que sobrevive fora do contexto.** No fecho, escolha a UMA frase que a dona repetiria de cor numa conversa, cole ela sozinha e responda por escrito por que ela sobrevive fora do contexto. Nenhuma significa que a peça está correta e não está viva. Cole `frase que sobrevive fora do contexto: <literal>`, com o porquê em uma linha.

**Forma do doc:** denso, tabelas e listas, nunca paredão de prosa. **Cada oferta fechada em si:** havendo mais de um nível, cada um vem inteiro e separado (pra quem, entregáveis, Mapa, preço, garantia, racional), lido sem depender do outro. **Fidelidade:** furo vira `[A CONFIRMAR]` no lugar exato, nunca número inventado.

**Duas regras duras de condução:** uma resposta = no máximo UM passo novo (o OK do passo N libera só o N+1, nunca o N+2), e **nunca narre o bastidor** (qual passo você detectou, qual ação está ativa, o que o OK autoriza). Conduz com a próxima pergunta, entrega o doc, ponto.

---

## Roteamento por pedido

Leia o pedido, ache a linha, entre direto na ação. As ações C, D e E desembocam na Ação A: elas decidem O QUE construir, a A constrói.

| O dono pediu | Ação |
|---|---|
| "desenha minha oferta", "monta a stack", "tenho o produto, preciso empacotar", "quanto cobrar por isso", "que garantia eu dou" | **Ação A · DESENHO DO ZERO** (o caminho padrão, P0 a P8) |
| "minha oferta não fecha", "quero refinar a oferta que já tenho", "por que ninguém compra" | **Ação B · AUDITORIA** |
| "que oferta eu faço pro meu público", "me dá ideias de oferta", "o que eu vendo pra essa gente" | **Ação C · IDEAÇÃO** |
| "o que os concorrentes vendem", "avalia a oferta do concorrente", "que ofertas rodam nesse nicho" | **Ação D · MERCADO** |
| "desenha minha escada", "esteira", "produto de entrada", "order bump", "upsell", "downsell", "recorrência" | **Ação E · ESTEIRA** |

Pedido ambíguo ("me ajuda com minha oferta"): pergunte UMA coisa só, se ele já tem uma oferta na mesa ou está partindo do zero, mostre a tabela como cardápio e siga pela resposta.

---

## Ação A · DESENHO DO ZERO (P0 a P8)

**O que faz:** desenha a oferta inteira, da ancoragem no posicionamento ao preço, num doc consolidado.

**Os dois modos da Ação A, declare o seu em 1 linha antes do P0.** O nome da ação diz "do zero", e é o caso mais comum, mas não é o único.
- **Modo CONSTRUÇÃO** (o padrão): o dono não tem preço, garantia nem stack. Você constrói cada peça no passo dela.
- **Modo REVISÃO:** o dono JÁ tem oferta rodando ou desenhada (preço, garantia, bônus, entregáveis definidos) e mesmo assim pediu "desenha minha oferta". Isso é Ação A, não Ação B, e o caminho é **partir do que existe, nunca zerar**. Rode os mesmos P0 a P8, mas em cada passo comece listando o que o dono já tem, marque cada peça como **mantém**, **ajusta** ou **falta**, e escreva o racional em 1 linha de toda peça que você mexeu. Preço, garantia e nome que já foram ao mercado só mudam com razão escrita e com o custo da mudança declarado (quem já comprou, o que a mudança faz com essa pessoa). A entrega sai igual, com uma linha a mais no topo: **o que mudou em relação à oferta atual**. Redesenhar do zero uma oferta que já vendeu joga fora a única validação real que existe no caso.

**Detecção de modo, antes de tudo, e o modo não é escolha.** O gatilho é mecânico, não uma impressão: **se o perfil do dono traz preço, bônus ou garantia definidos, ou registra venda já realizada, o modo é REVISÃO**, mesmo que o pedido diga "desenha". Declare a linha antes do P0, nesta forma: `modo: REVISÃO (gatilho: <o que no perfil disparou, citado literal>)` ou `modo: CRIAÇÃO (a oferta não existe no perfil: sem preço, sem bônus, sem garantia, sem venda registrada)`. **Em modo REVISÃO, `[A CONFIRMAR]` sobre item que o perfil já respondeu reprova o doc**: perguntar ao dono o preço que está escrito no perfil dele é o sinal de que a peça foi tratada como oferta nova. Cole no fecho a conta `marcadores no doc: N · sobre item que o perfil já respondeu: 0`.

**Precisa de:** o posicionamento do dono com **mecanismo nomeado**, avatar e resultado real, do perfil/brain do agente · o banco de provas dele (de onde sai todo número canônico) · a lista do que ele entrega e do que já tem de prateleira, perguntada a ele.

**Sem o insumo:** **sem mecanismo nomeado, não pare: rode a Entrevista Mínima abaixo aqui mesmo.** Oferta sem mecanismo nomeado é slogan genérico, e genérico compete por preço. Se o dono já tiver o Plano de Posicionamento pronto, usar ele é mais curto e a sugestão fica de pé; se a `soft-plano-posicionamento` não estiver instalada, a Entrevista Mínima resolve o mínimo que a oferta precisa e o resto fica `[A CONFIRMAR]`.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `plano-de-ofertas.md`, com PUV nos 2 cortes · Equação calibrada · entregáveis mais o entregável-tese · prateleira, bônus sem preço e inclusos · Mapa de Valor e custo invisível · níveis de acesso · garantia · preço e ancoragem · racional de curadoria. **STOP a cada passo.**

**O passo de entrega abre com este bloco, sozinho, antes de qualquer outra instrução:** `python3 scripts/checar_titulos.py --peca <arquivos> --titulos titulos.txt --teses teses.txt --insumos <insumos> --perfil <perfil>` (passo 1, com a saída colada) → preencher `conferencia/checagem-titulos.md` → `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <insumos> --perfil <perfil> > conferir.txt 2>&1; echo exit=$? >> conferir.txt` → `ls` colado. **Nada mais entra nesse bloco:** lint por arquivo, inventário e consentimento são consequência dele, porque o `--conferir` já os roda. A régua está em `shared-references/crivo/07-regua-de-titulos.md`, e os arquivos da ação saem junto do `conferencia/checagem-titulos.md` e do `conferir.txt`.

**Escopo pedido manda no tamanho: quando o dono pede "só a stack principal" (ou nomeia UMA oferta), o doc traz SÓ a stack principal completa.** Os outros níveis de acesso não viram oferta completa: cada um sai em **até 3 linhas** (o que muda de acesso, pra quem serve, a proporção de preço em relação ao principal), como mapa do que existe em volta, e o doc registra numa linha que o desenho cheio deles fica pra quando o dono pedir. Desenhar os três níveis por inteiro num pedido de stack única é inflar a entrega, e reprova no gate.

**Leia primeiro:** `references/desenho-da-stack.md` (P1 a P4) e `references/ancoragem-e-precificacao.md` (P5 a P7). **Profundidade:** `references/tipos-de-oferta.md` (os 6 tipos, lida no P0) · `references/pesquisa-e-validacao.md` (P0.5 e P8) · `references/mentoria-operacional.md` (quando o tipo é mentoria) · `references/gate-da-oferta.md` (a tabela do gate) · `references/EXEMPLO-FIM-A-FIM.md`.

**Quando usar esta lista:** os 8 passos abaixo são o esqueleto da Ação A; rode-os na ordem, com STOP a cada um. O passo a passo detalhado de cada P (a mecânica, as tabelas, os gates internos e as regras de reprovação) está em `references/desenho-do-zero.md`, leia essa reference antes de rodar cada passo.

Os 8 passos, em ordem:

- **P0 · Ancoragem:** puxa posicionamento, mecanismo nomeado e banco de provas, detecta tipo, estágio e sofisticação do mercado; nenhum número vira âncora sem fonte no banco. Traz o P0-min (Entrevista Mínima quando não há posicionamento), o P0a (gate "o público sustenta oferta?", 4 indicadores) e liga o P0.5 quando falta verbatim.
- **P0.5 · Munição de fala real** (condicional, só quando falta verbatim): minera avaliação, comunidade, concorrente e entrevista de quem comprou, e sai a planilha de fala real mais o Mapa de Conversão (dor→promessa, objeção→componente, etc.).
- **P1 · A PUV:** destila (não inventa) a Proposta Única de Valor em 2 cortes, parágrafo e uma linha, com o gate anti-vago (resultado + número + prazo + "sem X"); promessa vaga reprova de saída.
- **P2 · Equação de Valor:** calibra `Valor = (Resultado × Probabilidade) ÷ (Tempo + Esforço)` antes de qualquer item, descendo o denominador (mais prova, resultado cedo, menos trabalho); cada caminho desses vira um entregável.
- **P3 · Entregáveis + entregável-tese:** cada entregável mata UMA objeção nomeada e nasce vendável sozinho como fascination; acha o entregável-tese (o mecanismo virando produto), varre o mapa de barreiras e crava o ativo de primeira vitória.
- **P4 · A prateleira, os inclusos e o bônus sem preço:** monta a tripartição que É a ancoragem (módulos sem preço · cursos de prateleira com preço real · UM bônus sem preço), mais inclusos que fecham portas de saída e as bandeiras de nicho regulado (saúde, finanças, direito, CREF).
- **P5 · Mapa de Valor + custo invisível:** soma os avulsos como âncora (régua ~2x) e trabalha o custo do problema não resolvido; abaixo de 2x, propõe dois ajustes ao dono e para, sem inflar valor avulso (inflar reprova no gate).
- **P6 · Níveis de acesso + garantia + preço:** três alturas de uma promessa (Faz Sozinho · Faço Com Você · Faço Por Você) mais porta de entrada, garantia do cardápio com o piso legal do CDC artigo 49, e preço pela régua 10x; 1ª vez sai sem preço público e chama pra conversa.
- **P7 · Ancoragem + racional de curadoria** (fecha): abre pelo alto, escassez só real, nomeia a oferta, fecha com o racional de curadoria de cada escolha estruturante e, em modo REVISÃO, com o achado; estágio "nunca vendeu" segue pro P8.
- **P8 · Validação pré-lançamento** (condicional, só quando nunca vendeu): pré-venda fundadora como caminho oficial (só dinheiro valida disposição a pagar) com número-alvo fixado por escrito ANTES do teste; vendeu, o preço entra no doc.

---

## Ação B · AUDITORIA (a oferta que já existe e não fecha)

**O que faz:** diz por que a oferta atual não fecha e devolve as correções, sem redesenhar o que está de pé.

**Precisa de:** a oferta atual inteira (promessa, entregáveis, preço, garantia, página se houver) · o número de conversão que ele tem hoje (quantos viram, quantos compraram), perguntado a ele.

**Sem o insumo:** sem número de conversão, pergunte só isso ("de cada 10 pessoas que ouvem a oferta, quantas compram?"). Sem nem estimativa, siga pela leitura estrutural e marque `[A CONFIRMAR]` a hipótese de onde o vazamento está.

**Entrega:** `auditoria-de-oferta.md`, com o diagnóstico por passo (qual P está quebrado), as correções no padrão **antes → depois**, e o que passa intacto. **STOP.**

**O passo de entrega abre com este bloco, sozinho, antes de qualquer outra instrução:** `python3 scripts/checar_titulos.py --peca <arquivos> --titulos titulos.txt --teses teses.txt --insumos <insumos> --perfil <perfil>` (passo 1, com a saída colada) → preencher `conferencia/checagem-titulos.md` → `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <insumos> --perfil <perfil> > conferir.txt 2>&1; echo exit=$? >> conferir.txt` → `ls` colado. **Nada mais entra nesse bloco:** lint por arquivo, inventário e consentimento são consequência dele, porque o `--conferir` já os roda. A régua está em `shared-references/crivo/07-regua-de-titulos.md`, e os arquivos da ação saem junto do `conferencia/checagem-titulos.md` e do `conferir.txt`.

**Leia primeiro:** `references/gate-da-oferta.md` (a tabela do gate é o instrumento da auditoria) mais os Anti-Patterns no fim deste arquivo. **Profundidade:** `references/desenho-da-stack.md` e `references/ancoragem-e-precificacao.md`, nos passos que a auditoria acusar.

**As três alavancas, nesta ordem, ANTES de tocar no preço:** **maximizar o resultado** · **minimizar o esforço** · **remover os obstáculos de partida**. São as variáveis da Equação por outro nome. Só depois de mexer nas três se discute preço. Rode o gate inteiro, ache os ✗, e reescreva **só o que quebrou**, nunca o doc todo.

---

## Ação C · IDEAÇÃO (tem o público, quer saber que oferta fecha)

**O que faz:** gera um leque de 3 a 6 conceitos de oferta em níveis diferentes, ranqueados, pro dono escolher qual construir.

**Precisa de:** o público definido · a fala real dele (do P0.5 ou do posicionamento) · o que o dono já tem de ativo e de capacidade de entrega.

**Sem o insumo:** sem fala real, rode o P0.5 antes; a lista de obstáculos sai da munição colhida, nunca da imaginação. Sem público definido, o C1 reprova e o encaminhamento é a `soft-plano-posicionamento`.

**Entrega:** `leque-de-conceitos.md`, com os conceitos ranqueados, o racional de cada um, os descartes com a razão e as discordâncias com o trade-off escrito. **STOP: o dono escolhe.**

**O passo de entrega abre com este bloco, sozinho, antes de qualquer outra instrução:** `python3 scripts/checar_titulos.py --peca <arquivos> --titulos titulos.txt --teses teses.txt --insumos <insumos> --perfil <perfil>` (passo 1, com a saída colada) → preencher `conferencia/checagem-titulos.md` → `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <insumos> --perfil <perfil> > conferir.txt 2>&1; echo exit=$? >> conferir.txt` → `ls` colado. **Nada mais entra nesse bloco:** lint por arquivo, inventário e consentimento são consequência dele, porque o `--conferir` já os roda. A régua está em `shared-references/crivo/07-regua-de-titulos.md`, e os arquivos da ação saem junto do `conferencia/checagem-titulos.md` e do `conferir.txt`.

**Leia primeiro:** `references/desenho-da-stack.md`, o miolo construtivo (as 4 categorias de obstáculo, o Delivery Cube, a matriz valor-custo). **Profundidade:** `references/pesquisa-e-validacao.md` (descobrir a oferta perguntando, quando o dono tem audiência).

**Regra dura de saída: entrega CONCEITOS, nunca oferta pronta.** Preço, garantia, Mapa de Valor e stack detalhada nascem na Ação A, depois da escolha. Conceito com preço cravado é atalho proibido.

**C1. Valida o público pelos 4 indicadores** (roda o P0a inteiro). Reprovou com 2 ✗ ou mais, para no mesmo lugar. **O mecanismo NÃO barra a entrada aqui**, que é a exceção à regra do P0: quem pergunta "o que eu vendo?" quase nunca tem mecanismo nomeado. Ele entra como slot `[A CONFIRMAR]` e os conceitos saem com nome de trabalho rotulado provisório. **A regra que não cede:** o conceito escolhido só desemboca no P1 depois de o mecanismo estar nomeado.

**C2. Lista os problemas do avatar, mirando 15 ou mais**, varridos nas 4 categorias (conhecimento, habilidade, ambiente, psicologia). Menos de 15 quase sempre significa varredura de superfície, e o sinal clássico é a lista inteira cair em "conhecimento". **C3. Inverte cada obstáculo em solução**, no molde **"como fazer [o resultado] sem [o obstáculo]"**, ainda sem formato nem preço.

**C4. Cruza com o Delivery Cube.** A mesma solução entregue de formas diferentes tem preços completamente diferentes. Cruze o **nível de esforço do cliente** com a **proximidade** (um pra muitos · pequeno grupo · um a um). A régua: **quanto menor a capacidade de execução do avatar ou maior a urgência dele, mais o formato migra pro feito-por-ele.** Curso puro só funciona bem com avatar de disciplina comprovada. O veículo não pode contradizer o mecanismo.

**C5. Gera o leque, 3 a 6 conceitos em NÍVEIS diferentes.** Cada um com: nome de trabalho rotulado provisório · pra quem dentro do público · o obstáculo-mãe que mata · a solução no molde "sem X" · a célula do Cube · o racional. **Os conceitos ocupam células diferentes do Cube**, nunca três variações da mesma. 3 é piso, 6 é teto; célula irrelevante pro avatar não entra só pra fazer volume.

**C6. Ranqueia pela Equação e pela fome do público**, com as duas leituras escritas: **A**, o que a Equação diz (conceito que não move nenhuma das 4 variáveis sai do leque); **B**, o que a fome diz (esse público já procura ISSO e paga por isso hoje?). **A régua de desempate, em ordem fixa:** concordância entre A e B vence discordância · entre concordantes, vence a menor distância do que o dono já tem · discordância declarada nunca ranqueia acima de concordância, mas fica no leque com o trade-off escrito · reprovado nas duas leituras sai e vai pra lista de descartes com o porquê.

**Desemboca na Ação A a partir do P1**, com o mecanismo nomeado.

---

## Ação D · MERCADO (o que já roda no nicho, e onde está a lacuna)

**O que faz:** varre as ofertas do mercado, pontua cada uma, devolve o mapa e as 3 lacunas que viram vantagem.

**Precisa de:** os concorrentes nomeados ou o nicho declarado · acesso à web pra colher o que é público, quando o ambiente tiver.

**Sem o insumo:** sem acesso à web, peça o material ao dono numa pergunta única ("me manda os links das 3 ofertas que você quer que eu avalie"). Sem nada, o mapa não sai: diga isso em uma linha em vez de inventar dados de mercado.

**Entrega:** `mapa-de-mercado.md`, com a pontuação de cada oferta, as 3 lacunas ligadas ao passo que as executa, e os Top 3 Fixes quando a oferta avaliada é a do próprio dono. Cada oferta avaliada também vira um bloco em `ofertas-benchmark/` na pasta de trabalho, em caminho relativo. **STOP.**

**O passo de entrega abre com este bloco, sozinho, antes de qualquer outra instrução:** `python3 scripts/checar_titulos.py --peca <arquivos> --titulos titulos.txt --teses teses.txt --insumos <insumos> --perfil <perfil>` (passo 1, com a saída colada) → preencher `conferencia/checagem-titulos.md` → `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <insumos> --perfil <perfil> > conferir.txt 2>&1; echo exit=$? >> conferir.txt` → `ls` colado. **Nada mais entra nesse bloco:** lint por arquivo, inventário e consentimento são consequência dele, porque o `--conferir` já os roda. A régua está em `shared-references/crivo/07-regua-de-titulos.md`, e os arquivos da ação saem junto do `conferencia/checagem-titulos.md` e do `conferir.txt`.

**Leia primeiro:** `references/ancoragem-e-precificacao.md` (os enhancers por dentro, pra ler os do concorrente). **Profundidade:** `references/pesquisa-e-validacao.md` (o concorrente como dado).

**D1. Colhe o que é público**, nas 4 fontes: biblioteca de anúncios (anúncio ativo há 90 dias ou mais é oferta que PAGA, e a data de início é o sinal) · a oferta na página dele · o FAQ dele (mapa de objeção escrito pelo próprio mercado) · a reclamação dos clientes dele. **Só o que está público e verificável:** número que o concorrente não publicou entra `[A CONFIRMAR]` ou não entra.

**D2. Pontua cada oferta, com a conta MOSTRADA.** A Equação vira nota em 4 eixos de 0 a 25 cada, total 100: **sonho de resultado** · **probabilidade percebida** · **prazo** · **esforço**. Os dois últimos são o denominador e pontuam invertido: quanto menor o prazo e o esforço exigidos, maior a nota. É onde a maioria das ofertas do mercado perde, porque todo mundo briga pra prometer mais e quase ninguém briga pra entregar mais rápido. **D3. Lê os enhancers presentes:** escassez (tem lastro verificável?) · urgência (prazo real ou teatro?) · bônus (nomeados e ancorados?) · garantia (cobre resultado ou decisão?). **Enhancer forte em cima de nota baixa é maquiagem**, e é a lacuna mais fácil de atacar.

**D4. Sai o mapa mais as 3 lacunas,** cada uma com a jogada que a explora, ligada ao passo que a executa: lacuna de prazo vira ativo de primeira vitória no P3; lacuna de esforço vira componente feito-pra-você no P3; lacuna de probabilidade vira demonstração ou garantia mais forte no P2 e P6. Três, não dez. **D5. Deposita no acervo:** um arquivo por oferta em `ofertas-benchmark/`, com data da colheita, fonte verificável, promessa e stack visível nas palavras dela, a pontuação com a conta escrita, a célula do Cube, os enhancers e as lacunas. Caminho sempre relativo à pasta de trabalho, zero nome de pessoa.

**A guarda contra o benchmark virar régua:** o mapa é insumo interno. Nenhum concorrente nomeado entra no doc do dono como âncora de preço ou prova. E o mapa não manda copiar: mostra onde o mercado está saturado pra o dono ir pra onde ele não está.

---

## Ação E · ESTEIRA (a sequência, não a oferta solta)

**O que faz:** mapeia a escada de degraus, com o papel de caixa de cada um, o preço relativo e a ordem de exposição.

**Precisa de:** o inventário do que o dono já vende e já tem de ativo empacotável · a capacidade de entrega dele hoje · o público validado.

**Sem o insumo:** sem o inventário, pergunte só isso ("o que você já vende hoje, e o que você tem parado que dá pra empacotar?"). A maior parte de uma esteira sai de recorte do que existe, não de produto novo.

**Entrega:** `mapa-da-esteira.md`, com uma linha por degrau (nome de trabalho · pra quem · papel de caixa · natureza do ativo · proporção de preço · slot de preço · a régua de saúde · a sequência de exposição · os riscos declarados). **STOP.**

**O passo de entrega abre com este bloco, sozinho, antes de qualquer outra instrução:** `python3 scripts/checar_titulos.py --peca <arquivos> --titulos titulos.txt --teses teses.txt --insumos <insumos> --perfil <perfil>` (passo 1, com a saída colada) → preencher `conferencia/checagem-titulos.md` → `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <insumos> --perfil <perfil> > conferir.txt 2>&1; echo exit=$? >> conferir.txt` → `ls` colado. **Nada mais entra nesse bloco:** lint por arquivo, inventário e consentimento são consequência dele, porque o `--conferir` já os roda. A régua está em `shared-references/crivo/07-regua-de-titulos.md`, e os arquivos da ação saem junto do `conferencia/checagem-titulos.md` e do `conferir.txt`.

**Leia primeiro:** `references/ancoragem-e-precificacao.md`, a esteira por dentro (os tipos de degrau de atração, os modos de subida e de descida, a apresentação da recorrência).

**Regra dura de saída: entrega o MAPA, nunca oferta pronta.** Cada degrau se constrói depois, rodando a Ação A pra ele.

**E1. Inventário do que já existe.** Ofertas que já vende com ticket e volume real, ativos empacotáveis, capacidade de entrega. E o público: **o P0a roda inteiro se nunca rodou**, porque esteira em cima de público sem fome multiplica o furo por todos os degraus.

**E2. Escolhe a espinha.** Uma decisão que muda tudo depois. Os 4 critérios, respondidos por escrito:

| Critério | Puxa pra começar pelo barato | Puxa pra começar pelo caro |
|---|---|---|
| **Audiência hoje** | grande e fria: precisa de volume e prova barata | pequena e quente: o volume não paga o atrito de montar funil inteiro |
| **Necessidade de caixa** | dá pra construir ativo com calma | o mês precisa fechar agora: poucas vendas altas resolvem |
| **Capacidade de entrega** | o método já escala sem o dono | o dono é o gargalo: vender volume que ele não atende quebra a entrega |
| **Maturidade da oferta** | método validado, casos na mão | método em validação: poucos clientes bem acompanhados geram a prova |

3 ou 4 critérios apontando pro mesmo lado cravam a espinha; empate 2 a 2 é decisão do dono, e a skill mostra o trade-off escrito em vez de escolher. O risco de cada caminho entra declarado. **STOP** antes de desenhar degrau.

**E3. Desenha os degraus com o PAPEL DE CAIXA de cada um.** Degrau sem papel nomeado é produto sobrando e sai do mapa. Os 6 papéis, com a natureza do ativo: **atração** (cliente novo ao menor risco · informação) · **complemento de porta** (margem no mesmo checkout · ferramenta) · **núcleo** (a transformação principal · método) · **subida** (no calor do sim · implementação assistida) · **descida** (converte o não mudando a fricção, só em resposta a um não · recorte do núcleo) · **recorrência** (só depois de uma vitória tangível · manutenção do resultado).

**A progressão de natureza é o que impede canibalização:** informação → método → implementação → manutenção. Cada degrau vende uma CATEGORIA de valor diferente, não uma quantidade diferente da mesma coisa. Isso responde o medo mais comum ("se eu ensino tudo barato, ninguém compra o caro"): o barato entrega o mapa inteiro, e o caro é alguém corrigindo o caso específico dele enquanto ele executa. **A régua de saúde do conjunto, como slot:** o lucro bruto dos primeiros 30 dias de um cliente novo passa de 2x o custo de adquirir e servir ele? Dobrar, não empatar, porque metade da margem financia o próximo ciclo. Sem o custo de aquisição medido, o doc registra `[A CONFIRMAR]` e a régua vira pergunta pendente, nunca número inventado.

**E4. Preço RELATIVO entre degraus.** A skill não crava preço, crava a proporção: **entrada pro núcleo, 10x a 20x** · **núcleo pro alto, 5x a 15x** · **complemento de porta, 10% a 20%** do principal · **subida imediata, 2x a 3x** da compra que acabou de acontecer · **descida por corte de escopo, 40% a 60%** da oferta recusada. **Distância mínima entre vizinhos: menos de 2x é canibalização por proximidade.** O preço final de cada degrau é slot `[A CONFIRMAR]` até o dono validar. **E5. Checa canibalização** nos 3 modos: por proximidade de preço (afasta ou funde) · por sobreposição de entregável (devolve a progressão de natureza, nunca escondendo informação) · por âncora invertida (o topo exposto ao lead frio antes do núcleo faz o núcleo parecer a versão fraca, então a ordem de exposição segue a ordem da escada).

**Desemboca na Ação A:** o dono escolhe qual degrau constrói primeiro, quase sempre o núcleo, e ele entra no P1 com o P0 já resolvido aqui.

---

## Os 6 tipos de oferta (o mesmo molde, o modo de cada tipo)

O molde P0 a P7 é universal. O TIPO, detectado no P0, calibra o núcleo, o nível natural, a garantia provável e o canal. **Mentoria é UM tipo, não o padrão.**

| Tipo | Núcleo | Nível natural | Garantia provável | Canal |
|---|---|---|---|---|
| **Mentoria** | jornada em 4 etapas ao vivo a um, mais doc de 2 páginas | Faço Com Você | escada longa ou incondicional | conversa 1:1 acima de ~R$2k |
| **Consultoria** | 1 ou 2 calls sobre UM problema, mais plano e suporte curto | Faço Com Você, ou Por Você no premium | retorno como garantia, ou incondicional curta | conversa 1:1 |
| **Curso** | jornada em passos, clímax no item que TIRA trabalho | Faz Sozinho | 7 dias ou incondicional | checkout até ~R$2k |
| **Comunidade** | base de conteúdo enxuta mais encontro quinzenal e grupo | Faço Com Você assíncrono | acesso e suporte, ou incondicional | checkout |
| **Feito-pra-você** | execução entregue, com escopo tangível | Faço Por Você premium | retorno como garantia | 1:1 com aplicação |
| **Produto de entrada** | uma FATIA do principal, a porta que filtra | Faz Sozinho | 7 dias | checkout |

Profundidade de cada tipo em `references/tipos-de-oferta.md`; o tipo mentoria por dentro em `references/mentoria-operacional.md`.

---

## Gate de qualidade (roda por dentro, silencioso, não imprime)
**Ler o insumo de atendimento e de venda é parte do método, não zelo extra.** Antes de fechar o diagnóstico ou a stack, abra os insumos de atendimento e venda que o dono entregou (reclamação registrada, caixa de entrada, transcrição de call, cancelamento) e responda por escrito, citando o arquivo e a linha: o que eles dizem sobre a capacidade de ENTREGAR o que esta oferta vai vender? **"Não afeta a leitura numérica" não é resposta válida** quando o plano projeta multiplicar a base de alunos: a diferença entre vagas vendidas e vagas entregues mora justamente nesses arquivos. Quando a resposta apontar um item da stack que já falha hoje, o item muda de formato no desenho, e o documento diz que a correção é de operação, não de copy. Cole `insumos de atendimento e venda abertos: N · com resposta escrita e linha citada: N`.

**Régua de títulos (roda antes do resto do gate).** Todo título que sai desta skill passa pela régua `shared-references/crivo/07-regua-de-titulos.md`, R1 a R7. Rode a régua sobre a PUV, o touchstone, o nome da oferta e cada fascination de entregável: são os títulos que esta skill produz e entrega pra virar copy pública. A checagem sai colada num arquivo do disco que o dono abre, uma linha por título, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a entrega antes da análise de conteúdo. **O arquivo tem nome fixo: `conferencia/checagem-titulos.md`, na raiz da pasta de entrega**, e fecha com as três contagens: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. **O universo da régua é definido por esta skill, não por quem escreve.** São títulos, obrigatoriamente e sem exceção: a PUV, o touchstone, o nome da oferta, o nome de cada módulo ou fase, o nome de cada entregável, o nome de cada bônus, o nome de cada nível de acesso e cada linha do Mapa de Valor. Antes da tabela, extraia essa lista do próprio arquivo com `grep -nE '^\|.*\*\*|^#{3,4} ' <documento>` e cole a saída, depois escreva `títulos no documento: N · na tabela da régua: N`. **Os dois números vêm de fontes diferentes de propósito:** o primeiro sai do arquivo por comando, o segundo sai da sua tabela. Diferença entre eles reprova a entrega, e contar como produzido só o que você já passou pela régua é a forma mais comum de cumprir a letra da regra e furar o sentido dela.

**O primeiro número sai CRU do comando, sem qualificador.** Cole `títulos no documento: <saída literal do shell>`. **Parênteses nessa linha reprovam a entrega**: recortar o universo com "(que disputam atenção pública)" transforma 23 em 2 e apaga o gate. Rótulo estrutural não sai da conta: ele entra na tabela com a coluna `rótulo de seção fora da régua: sim` e continua contado no primeiro número.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**O piso do inventário é contável e a conta vai colada.** Rode `grep -c '^- ' <perfil>` e cole a saída do comando: esse número é o PISO BRUTO. Depois desdobre toda linha que carrega mais de um valor (a oferta com preço, parcela, 3 bônus e garantia conta 6, não 1) e cole `piso bruto: N · desdobrados: M · Dados fornecidos: N+M`. **`Dados fornecidos` menor que o piso bruto reprova a entrega**, porque significa que a peça descartou campo sem registrar o motivo. Não qualifique a linha com recorte de escopo: o total é o total, e o filtro de relevância mora na coluna de destino de cada dado, nunca no total.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Fontes consultadas (esta skill pesquisa, então a seção é obrigatória).** A seção "Fontes consultadas" da entrega lista só o que foi de fato aberto neste turno, e cada linha traz o comando ou a chamada de ferramenta que abriu aquela fonte. Sem acesso à web no ambiente, a seção diz exatamente "sem acesso à web neste ambiente" e nada mais: nenhum domínio, nenhum nome de marca, nenhuma data de busca. Checagem verificável antes de fechar: conte as linhas da seção e conte os comandos registrados no relatório e escreva os dois números lado a lado, nesta forma: `fontes declaradas: N · comandos no log: N`. **Declarar 4 buscas com 1 comando no log reprova**, e o conserto é apagar as 3 linhas sem comando, nunca inventar o comando. **Cada linha de tabela sobre terceiro traz a consulta que a produziu e o trecho citado da página aberta.** Número (preço, prazo, prazo de entrega, volume, quantidade de alunos, faturamento) vindo de página de terceiro só entra com o trecho colado ao lado; sem trecho colado, o campo sai como `[A CONFIRMAR: exige abrir a página]`, e cravar o número mesmo assim reprova a entrega inteira. Memória de treino e inferência plausível não são fonte.

A tabela completa, com os 30 checks e o veredito, está em `references/gate-da-oferta.md`. **O gate confere TODAS as linhas de lá, uma a uma, na ordem: conferir só PUV e Equação e carimbar "passa" é veredito inválido.** Um ✗ refaz **o item**, não o doc inteiro. Só doc com veredito PASSA vai pro dono. O núcleo do que ele confere:

1. **Ancoragem no dono:** avatar, mecanismo nomeado e resultado real herdados, ou a Entrevista Mínima rodada. **Gate de público (P0a):** os 4 indicadores com veredito e razão escrita, nenhum ✗ "consertado" com bônus ou escassez.
2. **PUV destilada** nos 2 cortes, passando no teste do "nunca vi explicar assim", com promessa anti-vaga (número, prazo, condição "sem X"). **Coerência com a tese:** nenhum entregável contradiz o mecanismo. **Equação rodada item a item**, com a variável nomeada em cada peça.
3. **Entregáveis nomeados um a um**, cada um matando UMA objeção, descritos pelo que a pessoa VIRA; oferta sem lista de entregáveis reprova na hora. **Entregável-tese presente.** **Prateleira pela tripartição**, com "bônus" reservado a UM item e pelo menos um item valendo mais que o principal.
4. **Mapa de Valor honesto** (em torno de 2x o preço, ou o custo invisível como âncora primária, zero número inventado). **Garantia do cardápio** com o piso legal declarado. **Preço pela régua 10x, só se validado.** **Ancoragem abre pelo alto**, com o destino do CTA certo pela faixa. **Racional de curadoria** em cada escolha estruturante.
5. **Números do dono**, sempre: zero invenção plausível, zero benchmark nomeado no doc dele.
6. **Anti-IA (HARD):** zero travessão longo (U+2014), zero da família do verbo-freio banida pela régua anti-voz, sem frase-emoldura, sem verbo-clichê de hype. **Declarar ✓ sem buscar é gate falso.** Com shell, rode `python3 scripts/lint_copy.py` no doc final e siga só com saída limpa; sem shell, varra o texto inteiro caractere a caractere. Achou um travessão longo, reescreva (aposto vira vírgula, anúncio de consequência vira dois-pontos, separação de duas ideias vira ponto) e varra de novo. A régua completa em `shared-references/crivo/06-regua-de-escrita.md`.

---

## Crivo adversarial (gate opcional de saída, 4 lentes)

**Dispara quando o dono pede "crivo pesado", "bate forte nessa oferta", ou por decisão da skill antes de subir uma oferta cara.** O gate confere se a peça obedece ao método; este crivo pergunta se ela sobrevive a quem discorda. Roda depois do gate, nunca no lugar dele.

| Lente | A pergunta que ela faz | O que ela reprova |
|---|---|---|
| **A fome** | essa multidão existe, está concentrada e paga hoje por algo parecido? | oferta linda pra um público que ninguém consegue nomear onde está |
| **O estágio** | nesse nível de sofisticação, essa promessa ainda vende ou virou ruído? | promessa nua num mercado que já ouviu isso de cinco concorrentes |
| **A Equação** | em qual das 4 variáveis a nota cai, e o que falta pra levantá-la? | numerador inflado enquanto o denominador continua pesado |
| **A ascensão** | esse degrau alimenta o próximo, ou é um beco? | oferta sem pra onde subir, e degrau que canibaliza o de cima |

**As regras:** **um dos quatro é obrigado a atacar**, nomeado antes de os pareceres serem escritos; dissidente sem ataque real reprova o crivo inteiro. Sai um **mapa de discordância** com 2 a 3 conflitos, cada um com o trade-off dito por escrito. **As guardas:** é SIMULAÇÃO de lente, rotulada como tal (critérios de escola, não pessoas falando) · **citação inventada é proibida** · proibido aprovar por educação, porque quatro pareceres favoráveis é sinal de crivo mal rodado.

---

## O que esta skill NÃO faz

Em toda rota abaixo: se a skill não estiver instalada, faço aqui em modo reduzido, com o que esta skill carrega, e marco o que ficou raso como `[A CONFIRMAR]`.

- **Posicionamento, avatar do zero, nomear o mecanismo, PUV embrionária** → `soft-plano-posicionamento`. Esta skill DESTILA a PUV do posicionamento pronto, não o cria.
- **A projeção do negócio, A Conta e o roadmap de 90 dias** → `soft-plano-negocio`.
- **Margem, markup, DRE, fluxo de caixa por cálculo** → `soft-financeiro`.
- **A oferta apresentada dentro do webinar** (ancoragem ao vivo, stack semeada na aula) → `soft-webinar`. Aqui ela é desenhada como ativo; lá ela cai na tela.
- **A estratégia de lançar e escalar a oferta** (vender antes de montar, turma fundadora, subir de um a um pra grupo) → `soft-vendas-estrategias`.
- **Script de venda, objeção, fechamento** → `soft-vendas-closer`. Prospecção → `soft-vendas-sdr`. Proposta pós-call → `soft-vendas-proposta`. Contrato → `soft-vendas-contratos`.
- **Carta, VSL, landing, isca** → `soft-funil-carta`, `soft-funil-landing`, `soft-funil-isca`.
- **"Por onde começo", "próximo passo", "valida isso"** → `soft-leon`.

## Anti-Patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Abriu nos entregáveis, sem PUV, ou virou loja | Destila a PUV antes de listar; uma promessa, três alturas, níveis é lente e não estrutura |
| Entregável sem objeção nomeada, ou descrito por "120 aulas" | Corta ou nomeia a crença que ele quebra; descreve pelo que a pessoa VIRA |
| Sem entregável-tese, ou stack de volume vazio; oferta que contradiz a tese | Acha o item que materializa o mecanismo, que só ESTE especialista entrega; curadoria pela coerência, o que trai a promessa sai |
| Chamou tudo de "bônus", ou objeção de mecanismo virou bônus | "Bônus" fica com UM item; objeção de mecanismo vai PARA DENTRO do escopo |
| Mapa com número inventado ou redondo | Só valor defensável, ou custo invisível como âncora. Na dúvida, subestima |
| Preço pelo bolso do cliente, cravado sem ter vendido, ancoragem começando pelo barato, ou 3k no checkout | Crava pela Equação e pela régua 10x; a 1ª oferta sai sem preço; abre pelo alto; ticket alto fecha no 1:1 |
| Super-garantia onde o avatar já confia; nível de baixo individual e barato | Garantia do tamanho da objeção e não maior; escala via grupo, triagem ou assíncrono |
| Tratou mentoria como o padrão | Mentoria é UM dos 6 tipos: detecta no P0 e usa o modo dele |
| Desenhou oferta pra público sem fome, ou tentou salvar oferta rasa com bônus e escassez | Roda o P0a antes; 2 ✗ volta pro posicionamento. Enhancer não conserta oferta fraca |
| Leque com 3 versões da mesma coisa, ou varredura de obstáculos só em "conhecimento" | Conceitos em células diferentes do Cube; varre ambiente e psicologia também, é lá que moram os entregáveis que o concorrente não tem |
| Esteira como lista de preços, ou mapa de esteira com preço cravado | Cada degrau declara o PAPEL DE CAIXA e degrau sem papel sai; preço é proporção mais slot do dono |
| Degrau barato entregando a mesma vitória do caro; dois degraus a menos de 2x; descida antes da venda cheia | Devolve a progressão de natureza sem esconder informação; afasta ou funde; a descida só responde a um não |
| Crivo adversarial aprovando por unanimidade; copiou a oferta do concorrente do mapa | O dissidente não atacou, nomeia antes dos pareceres e refaz; o mapa mostra onde o mercado está saturado, pra ir pra onde ele não está |
| Narrou o bastidor ("detectei o modo C, agora vou pro P2") | Não narra: conduz com a próxima pergunta e entrega o doc |

## Handoff

Plano de Ofertas aprovado alimenta: `soft-funil-carta` e `soft-funil-landing` (a oferta virando carta e página), `soft-vendas-closer` (virando conversa), `soft-vendas-estrategias` (como e quando lançar), `soft-webinar` (caindo na tela), `soft-vendas-proposta` (pra um cliente específico), `soft-vendas-contratos` (o contrato do ciclo). Doc vivo: muda a oferta principal, revisa carta, script e páginas.

## References

- `references/desenho-do-zero.md`: o passo a passo detalhado da Ação A, P0 a P8, com o P0-min (Entrevista Mínima), o P0a (o público sustenta oferta?), o P0.5 (munição de fala real), o pré-flight de copy e a mecânica, as tabelas e os gates internos de cada passo.
- `references/desenho-da-stack.md`: aprofunda P1 a P4 (escolha e reembalagem do mecanismo, PUV com anatomia e teste, Equação com o mapa de tipo pra variável, engenharia de valor percebido, entregáveis com as 5 perguntas, fascinations e o repertório de bullets, entregável-tese, mapa de barreiras, primeira vitória e as primeiras 24 horas, cardápio de componentes, régua de bônus, rubrica de corte, naming e escada de fadiga, o miolo construtivo com o Delivery Cube e a matriz valor-custo, o teste-relâmpago das 4 perguntas e a Touchstone).
- `references/ancoragem-e-precificacao.md`: aprofunda P5 a P7 (Mapa de Valor e as 2 âncoras, os três registros, a régua de 2x, o custo invisível, o cardápio de garantias com o piso legal e a escada de reversão, régua 10x e condições de pagamento, psicologia de preço com lastro e limite de cada régua, a mesa de tensões pra arbitrar regras que se contradizem, níveis de acesso, ancoragem, espectro de ticket, fechamento com escassez, os enhancers por dentro, a esteira por dentro degrau a degrau).
- `references/tipos-de-oferta.md`: os 6 tipos, cada um com núcleo, nível natural, entregável-tese típico, garantia, canal e PUV. · `references/mentoria-operacional.md`: o tipo mentoria por dentro (extração de conhecimento, mapa da transformação, as 4 ferramentas de acompanhamento, ficha técnica, o doc de 2 páginas).
- `references/pesquisa-e-validacao.md`: os dois passos condicionais por dentro. O P0.5 (as 4 minas de fala real e o Mapa de Conversão), o caminho de descobrir a oferta perguntando quando o dono tem audiência, a variação de mercado, e o P8 (hierarquia do sinal, pré-venda fundadora campo a campo, os testes auxiliares).
- `references/gate-da-oferta.md`: a tabela completa do gate, check a check, com o veredito e a reescrita obrigatória do travessão. · `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta, com as 5 ações no formato real da entrega.
- Transversais: `shared-references/crivo/` (perfil do usuário, entrada de fala real, simulação de cliente, gate das 3 perguntas, gate regulado, premissas mestras, régua de escrita) · `scripts/lint_copy.py` (anti-IA em código, rode no shell quando o ambiente permitir).

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **O lint é gate com código de saída, não relatório.** Rode `python3 scripts/lint_copy.py <todos os .md da entrega>; echo "exit=$?"` e cole a linha `exit=` no relatório. **`exit` diferente de 0 proíbe a entrega:** volte pro passo de escrita, conserte e rode de novo, até sair 0. Declarar que rodou o lint sem colar o veredito não conta como gate cumprido. E a frase de fecho entra na varredura junto com o resto: o CTA é o texto que mais se repete no pacote, então um molde banido ali se multiplica por todos os arquivos e pelos dados que alimentam qualquer gerador. Cole `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `shared-references/crivo/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
- **A chamada da persona nunca leva nome real.** Persona, avatar, persona-âncora, cena-assinatura e célula do Mapa de Munição são peça pública, mesmo dentro de um documento de estratégia: é deles que nascem as capas dos meses seguintes. Rode `grep -rn 'autorizado por' <insumos>`; **saída vazia proíbe nome próprio de pessoa real em qualquer um desses cinco lugares.** A persona sai por idade, profissão e situação (`55, contadora, operou o menisco`). Quando o texto precisar mesmo de um nome pra chamar a pessoa, **use um nome inventado e diga na mesma linha que é inventado**: `Marta (nome inventado), 55, contadora`. **Lead com negociação em aberto na caixa de entrada nunca vira persona-âncora**: ela é a primeira a ler a peça e vai encontrar a própria transcrição virada em avatar. Feche com `personas na peça: N · com nome inventado declarado: N · com nome real dos insumos: 0`.
