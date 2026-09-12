---
name: soft-plano-posicionamento
description: >-
  Constrói o Plano de Posicionamento completo do especialista num doc só: o Racional, o Grande Dominó, o Mecanismo do Problema e o da Solução nomeado, a Oferta com PUV, o Perfil Enxuto, a Fundação de Headlines e os 5 elementos de Voz. Use quando o pedido for: "monta meu posicionamento", "plano de marca", "preciso me reposicionar", "dá um nome pro meu método", "qual minha proposta de valor", "escreve minha bio do zero", "quem é meu cliente ideal", "qual meu problema avançado", "minha voz não soa minha", "quais meus pilares de conteúdo". NÃO use pra: "audita esse perfil" e reescrever bio e destaques do que já está no ar (soft-consultoria-instagram); a headline ou capa (soft-conteudo-headlines); o corpo do post (soft-conteudo-carrossel, -reels, -stories); a oferta como stack com preço (soft-plano-ofertas); a projeção e o roadmap (soft-plano-negocio); o próximo passo do fundador (soft-leon); carta ou página (soft-funil-carta, soft-funil-landing). Leia e siga o fluxo inteiro do SKILL.md.
---

# O Plano de Posicionamento, a fundação

Esta skill constrói um documento só, o **Plano de Posicionamento completo**: o **Posicionamento** (o que o especialista diz, o ângulo que o mercado validou e ninguém ocupou) e a **Voz** (como ele diz). Nascem juntos e respondem um ao outro, por isso uma skill só. É o documento mais profundo do sistema e vira o cérebro do agente do cliente: tudo que sai depois (conteúdo, funil, venda) nasce daqui. Exaustivo e preciso, nunca resumido.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**A linha do mecanismo é saída obrigatória.** No `conferencia/checagem-titulos.md` desta entrega saem, sempre: `mecanismo do problema: <nome> | substantivo trocado: <original> → <outro mercado> | sobrevive à troca de nicho? sim/não` · `mecanismo da solução: <nome>` · `números não confirmados no perfil: N · publicados na peça: 0`. Falta de qualquer uma invalida a entrega, e a ausência da linha do mecanismo custa mais que as outras: sem ela ninguém sabe se o problema foi batizado ou só descrito.

**O título é uma afirmação, e o nome da seção desta skill nunca é o título da peça.** Todo cabeçalho do documento entregue afirma a decisão daquela seção. É proibido usar como cabeçalho o nome do passo desta skill (`Passo N`, `Etapa N`, `Bloco N`), o prefixo `Seção:` e o nome do artefato (`PUV`, `Racional`, `Equação de Valor`): esses são o andaime da execução, e o dono abre o documento pra saber o que foi decidido, nunca onde o texto mora. Errado, porque rotula: `# Plano de Posicionamento · Studio Base 40`, `## Passo 5 · a prescrição`, `## Seção: a conta do tempo`. Certo, porque afirma: `# 3 sessões de 25 minutos vencem outro recomeço`, `# 12 semanas: o ombro escolhe a carga`, `# A sala aquece antes da oferta, sem fabricar prova`. Cole uma linha por cabeçalho, `H2: <literal> · afirma algo que o dono pode discordar: sim/não`, e feche com `cabeçalhos que afirmam: N de N`. Menos da metade volta pro passo de escrita.

**`--exige` por ação.** Rode `--conferir <pasta> --exige <lista>` com a linha da ação entregue; arquivo ausente sai com exit 1 e `arquivo exigido pela ação ausente: <nome>`.

| Ação | `--exige` |
|---|---|
| 1 PLANO COMPLETO | `plano-de-posicionamento.md,conferencia/checagem-titulos.md` |
| 2 PERFIL | `perfil.md,conferencia/checagem-titulos.md` |
| 3 PESQUISA | `dossie-de-nicho.md,conferencia/checagem-titulos.md` |
| 4 PILARES | `pilares-de-conteudo.md,conferencia/checagem-titulos.md` |


**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um Plano fechado inteiro num caso fictício de nicho neutro: a entrada que o dono deu, as perguntas que a skill fez, os 4 STOPs, e cada bloco preenchido no formato real da entrega (Racional, Narrativa, Grande Dominó, Mecanismo, Oferta, Perfil Enxuto, Fundação de Headlines, os 5 elementos de Voz) mais o Crivo rodado. Ler antes da primeira pergunta economiza uma rodada inteira de retrabalho.

**Quantos turnos isso leva.** De 8 a 14 turnos numa condução normal: 1 de briefing, 1 a 2 de pesquisa, 1 de entrevista dirigida, 1 de território, 4 de construção com STOP (Narrativa, Mecanismo, Oferta, Voz), 1 de Crivo e 1 de entrega. Fale isso ao dono no primeiro turno, pra ele saber que não é uma resposta única.

---

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola tudo que tem e eu monto teu Plano). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pra construção com o que o dono colou. Se faltar um insumo que o Plano não vive sem (a prova real, a fonte de fala do público), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista dirigida e a pesquisa, uma pergunta de cada vez, e ergue o Plano com o que o dono for dando.

A pergunta do modo é UMA por Plano. As outras três partes acontecem nos passos abaixo:

- **Ensina enquanto faz:** em cada escolha estrutural (o Grande Dominó, o nome do mecanismo, o ângulo do território) escreve UMA linha do porquê, na voz de quem ensina a jogada. O dono lê a razão e aprende a decidir sozinho.
- **Puxa o material bruto:** quando a resposta vier rasa ("meus clientes querem crescer", "melhorar de vida"), não segue com o genérico. Pede o concreto que só o dono tem: "me conta de UM cliente, o que ele te falou quando te procurou, com as palavras dele?", ou um número que aconteceu, ou uma frase literal. Material bruto vira a âncora do Plano; resposta rasa vira Plano raso. Puxa uma vez, com jeito; se o dono não tiver, segue e marca o furo.
- **Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer outro ângulo de território? o mecanismo com outro nome? a Voz mais crua? me diz o que ajustar que eu refaço só essa parte."

## ⚠️ Checklist do que confirmar ANTES de começar

Cinco confirmações, todas no primeiro turno, antes da primeira pergunta de conteúdo:

1. **O perfil do dono existe?** Leia do perfil/brain do agente quando existir. Avatar, fonte de fala real do público, banco de provas, voz e nicho são DELE. Sem perfil, é entrevista curta aqui mesmo (o "Sem o insumo" da Ação 1), nunca dados assumidos de outra pessoa.
2. **O nicho é regulado?** Saúde, jurídico ou finanças (fisio, dentista, nutricionista, psicólogo, médico, enfermeiro, advogado, contador, consultor de investimento). Se for, marque o Plano como REGULADO agora: a Promessa e a Projeção não cravam prazo nem desfecho garantido, e o gate regulado passa a ser obrigatório no Crivo. Na dúvida, trate como regulado.
3. **O ambiente tem busca na web?** Se tiver, a pesquisa de mercado roda. Se não tiver, ela vira uma pergunta única ao dono ("me manda 3 concorrentes e o preço que eles praticam").
4. **O dono tem prova real na mão?** Caso com número, prazo e contexto. Sem prova, a promessa nasce rebaixada (o que o método FAZ, não o resultado garantido) e o número entra `[A CONFIRMAR]`.
5. **O dono sabe que são 8 a 14 turnos?** Diga em uma linha. Expectativa alinhada evita o pedido de "me dá tudo de uma vez" no meio do caminho.

---

## ⚠️ ENTREGA = UM doc, sempre

O resultado desta skill sai como **um documento markdown consolidado**. A condução (perguntas, escolhas, os STOPs de aprovação) acontece no chat; a PEÇA mora no doc. Ao parar num STOP, você mostra ou atualiza o doc e pergunta "ajusto?"; nunca reescreve a peça em pedaços no corpo da conversa. Sem o doc entregue, a skill não terminou.

- **Ambiente que renderiza markdown:** mostre o documento inteiro ali, com todos os blocos na ordem.
- **Ambiente com disco:** salve o arquivo `.md` e cite o nome dele na resposta.
- **Canal que anexa arquivo:** gere o `.md` e cite o nome; a condução vai em mensagens curtas, sem markdown pesado.

---

## Roteamento por pedido

Esta skill tem uma ação principal e três entradas laterais que reusam partes dela. Leia o pedido, ache a linha, entre direto.

| O dono pediu | Ação |
|---|---|
| "monta meu posicionamento", "plano de marca", "preciso me reposicionar", "quem é meu cliente ideal", "dá um nome pro meu método", "minha voz não soa minha" | **Ação 1 · O PLANO COMPLETO** (o caminho padrão) |
| "escreve minha bio", "arruma meu perfil", "meu LinkedIn", "audita esse perfil" | **Ação 2 · PERFIL** (usa o Plano se existir; senão faz o mínimo aqui) |
| "pesquisa esse nicho", "o que os concorrentes falam", "quanto o mercado cobra" | **Ação 3 · PESQUISA** (o Dossiê de Nicho isolado) |
| "meus pilares de conteúdo", "sobre o que eu falo", "meu círculo temático" | **Ação 4 · PILARES** (nasce da Voz; sem Plano, entrevista curta) |

Pedido ambíguo ("me ajuda com minha marca"): pergunte UMA coisa só, o que está faltando hoje, mostre a tabela como cardápio e siga pela resposta.

---

## Ação 1 · O PLANO COMPLETO

**O que faz:** conduz o especialista por entrevista e pesquisa até um Plano de Posicionamento fechado, com as duas metades (Posicionamento e Voz) num doc só.

**Precisa de:** o perfil do dono (avatar, prova, voz, nicho), do perfil/brain do agente quando existir · a pesquisa do mercado (concorrentes, vocabulário cru do público, preço praticado), buscada na web se o ambiente tiver acesso · as respostas da entrevista dirigida, sempre perguntadas ao dono.

**Sem o insumo:** entrevista curta de 6 perguntas aqui mesmo, uma por vez: qual o nicho e quem é o cliente específico · que resultado real você já entregou, com número e prazo · qual o problema que ele já tentou resolver e não resolveu · o que você faz que nenhum concorrente faz · que caso real você pode mostrar · qual seu ticket hoje e sua meta de 90 dias. O que sobrar vira `[A CONFIRMAR]` no doc e o Plano segue. Sem acesso à web, a pesquisa vira a pergunta única: "me manda 3 concorrentes e o preço que eles praticam".

**Antes de escrever qualquer cena com pessoa, rode o passo de nomes.** A pessoa citada costuma ser justamente quem vai ler a peça. Rode antes da primeira linha da abertura:

```
python3 scripts/checar_titulos.py --peca <cada entregável> \
  --insumos <pasta de insumos do dono> --perfil <perfil do dono>
```

Ele imprime `nomes candidatos achados pelo script: N` e, por nome, `autorização no insumo: sim/não` e `mensagem privada: sim/não`. **Nome com `mensagem privada: sim` e `autorização: não` sai da peça** e vira a forma por faixa ("uma aluna na casa dos 50"). Lead com pergunta sem resposta nunca vira cena de abertura. Cole `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada: 0`.

**O marcador é campo, e campo tem tamanho.** Na peça pública ele cabe em `[A CONFIRMAR: <o dado>]`, no máximo 6 palavras, depois de um rótulo e no fim da linha. **O porquê da pendência nunca entra na peça**, vai pro handoff com o número da linha ao lado. O script conta e reprova acima do teto, em `marcadores acima de 6 palavras: N (teto 0)`.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `plano-de-posicionamento.md`, com o Racional, os 3 blocos, as 2 saídas e os 5 elementos de Voz, mais o Mapa de Munição da Audiência como seção. **STOP em cada bloco.** **Junto do plano sai `conferencia/checagem-titulos.md`, arquivo obrigatório da entrega**, com a régua R1 a R7 rodada sobre TODO título que este documento produz: a PUV, o Grande Dominó, a tese central, o nome do mecanismo, cada inimigo nomeado, a bio do Perfil Enxuto e cada linha da Fundação de Headlines. Ele fecha com as 3 contagens (R3 teses distintas, R4 com inimigo ou inversão, R5 molde de antítese, esta última copiada da saída do lint sobre o documento inteiro, nunca contada à mão). **Entrega sem esse arquivo reprova, mesmo com o plano impecável**, porque este é o documento que mais produz título de toda a operação e é dele que nascem as capas dos meses seguintes.

**O passo de entrega abre com este bloco, sozinho, antes de qualquer outra instrução:** `python3 scripts/checar_titulos.py --peca <arquivos> --titulos titulos.txt --teses teses.txt --insumos <insumos> --perfil <perfil>` (passo 1, com a saída colada) → preencher `conferencia/checagem-titulos.md` → `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <insumos> --perfil <perfil> > conferir.txt 2>&1; echo exit=$? >> conferir.txt` → `ls` colado. **Nada mais entra nesse bloco:** lint por arquivo, inventário e consentimento são consequência dele, porque o `--conferir` já os roda. A régua está em `shared-references/crivo/07-regua-de-titulos.md`, e os arquivos da ação saem junto do `conferencia/checagem-titulos.md` e do `conferir.txt`.

**Leia primeiro:** `guia/02-plano-marca-pessoal.md` (a estrutura de um Plano fechado, os 3 blocos e as 2 saídas, a Equação de Valor, o Problema Avançado, os níveis de acesso) · `guia/CODIGO-DE-ESCRITA.md` (a lei de toda frase que sai).

**Profundidade:** `guia/03-identidade-voz.md` (os 5 elementos da Voz) · `guia/01-filosofia.md` (a régua da percepção) · `references/conducao-na-pratica.md` (o jeito de conduzir, consulte o tempo todo) · `references/super-pesquisa.md` · `references/mapa-de-municao.md` · `references/bloco-2-metodo.md` (engenharia de nomeação do método) · `references/bloco-3-oferta.md` (engenharia de execução da Oferta) · `references/bloco-5-fundacao-headlines.md` · `references/prompts-mente-cliente.md` · `references/descobrir-a-voz.md` · `references/narrativa-pessoal.md` · `references/bastidor-estrategico.md` · `references/valores-e-anti-valores.md` · `references/pilares-de-conteudo.md` · `references/conexao-vs-performance.md` · `references/circulo-tematico.md` · `references/modo-perfil.md`.

### Os passos, na ordem

1. **Briefing.** Nicho, cliente ideal específico, resultado real já entregue (número e prazo), o @, de 1 a 3 concorrentes. Se já veio do orquestrador, confirme e pule. **Roda aqui a checagem de nicho regulado do checklist acima.**

**Número de terceiro sai com a tripla completa.** Preço de concorrente, média de mercado e qualquer número que não seja do dono entram na forma:

```
<número> | trecho: "<literal>" | url: https://... | consultado em: <dd/mm/aaaa>
```

**Linha sem URL completa reprova o número**: a referência interna da ferramenta de busca não abre no navegador do dono. Feche com `números de terceiro: N · com trecho literal: N · com URL completa: N`, os três iguais. O `checar_titulos.py` conta e reprova quando divergem.

2. **Pesquisa de mercado.** Conduza a Super Pesquisa (`references/super-pesquisa.md`): concorrentes, vocabulário cru do público em fala literal, preço praticado, força do Problema Avançado, e já colha os 12 campos do Mapa de Munição (`references/mapa-de-municao.md`). É daqui que sai a densidade técnica e o vocabulário real, nunca da cabeça da IA. **Mire fechado:** uma pergunta de pesquisa enxuta (nicho + avatar + Problema Avançado) entrega mais e gasta menos. A frente mais validada é olhar o que o nicho **já compra**, não a dor que a IA imagina. Pra aprofundar o avatar depois da pesquisa, `references/prompts-mente-cliente.md`, mas é hipótese que **volta pra entrevista confirmar**.

3. **Entrevista dirigida** (6 perguntas num bloco só): o Problema Avançado que achei bate? · transformação concreta com número e prazo · 3 conselhos de mercado que você quer quebrar · o que você faz que nenhum concorrente faz · casos reais com nome e número · ticket de hoje e meta de 90 dias. **A pergunta-teste do argumento-mestre:** "qual o único elemento que, se um concorrente me mostrasse, eu compraria na hora?" O que convence ele é candidato a argumento central.

4. **Território e racional.** Roda as 2 perguntas do território mais as 4 do que vende de verdade; decide os blocos e **abre o plano** na seção 0. Se o exemplo do guia já descreve o caso, desça uma camada na causa até achar o vão.

5. **Construção incremental, um bloco por vez, com STOP.** A ordem é Racional → Bloco 1 Narrativa → Bloco 2 Mecanismo → Bloco 3 Oferta → as 2 saídas → Parte B Voz. Cada bloco: lê a seção do guia, cruza com pesquisa e racional, escreve, mostra e **para** ("tá bom? ajusto?"). Os 4 STOPs que não podem faltar:
   - **STOP Narrativa:** mostra Cliente Ideal e Problema Avançado, confirma que o Problema Avançado bate na pele dele antes de seguir pro Mecanismo.
   - **STOP Mecanismo:** mostra o Grande Dominó, o Mecanismo do Problema, as crenças a quebrar e o Mecanismo da Solução nomeado. Confirma o NOME (nunca vem bom de primeira) e que a explicação contrapõe as crenças. Checa coerência: método "sem reunião" não tem oferta com quatro reuniões.
   - **STOP Oferta:** mostra a PUV, os níveis de acesso e a Equação de Valor.
   - **STOP Voz:** mostra os 5 elementos destilados da coleta, não prescritos, e confirma o tom.

6. **Auditoria silenciosa antes de fechar.** A régua da percepção (o cliente ideal lê e pensa "finalmente alguém que entende meu problema"?) mais os filtros `shared-references/filtro-anti-ia/`, `shared-references/filtro-mobile-first/` e `shared-references/filtro-cliente-primeiro.md`. Falhou, reescreve o bloco.

7. **Crivo do Plano.** Gate bloqueante, tabela completa em `references/crivo-do-plano.md`. Preencha e imprima antes do handoff. Veredito binário: uma falha reprova e re-roda o bloco.

8. **Entrega o doc.** Consolida o Plano inteiro num documento só, com todos os blocos na ordem. O chat foi a condução; o doc é o produto.

### O que o Plano entrega, bloco a bloco

**Parte A, Posicionamento:**

- **0. Racional** (território · o que vende de verdade · contra qual cultura luta · a tensão dor para desejo · o sentimento). Abre o plano e decide tudo. Sem ele visível, o resto vira lista rasa.
- **Bloco 1 · Narrativa:** Cliente Ideal (persona com nome INVENTADO, ver a regra da chamada da persona abaixo) · Problema Geral · **Problema Avançado** (a imprevisibilidade mais a invisibilidade; é o que as OUTRAS soluções já geraram nele, não a tática isolada) · Promessa · Projeção de Resultado.
- **O Grande Dominó** (logo após o Racional): a UMA tese-mãe que, se o lead aceita, a compra vira consequência. Volta em todo conteúdo.
- **Bloco 2 · Mecanismo** (o coração): o **Mecanismo do Problema** (por que ele está preso, explicado na causa) mais as **crenças a quebrar** mapeadas, mais o **Mecanismo da Solução** (o novo mecanismo único nomeado). A forma da explicação é livre (pilar, premissa, característica ou passo), desde que seja desejável, vendável e contraponha as crenças. **Não force passo 1, 2, 3.**

**O nome do mecanismo do problema passa pelo teste do nicho trocado, como qualquer título.** Cole `mecanismo do problema: <nome> | substantivo trocado: <original> → <outro mercado> | sobrevive à troca de nicho? sim/não`. **`sim` volta pro passo de nomear**, porque um mecanismo que serve pra qualquer mercado não explica este: "recomeço acelerado" sobrevive trocando treino por dieta, por estudo e por carreira, e por isso não é mecanismo, é rótulo. O nome sai do substantivo concreto do caso (o dia 12, o joelho que decide, os 78 que sumiram), nunca do adjetivo do comportamento. O mesmo teste vale pro Mecanismo da Solução.
- **Bloco 3 · Oferta:** abre pela **PUV** · Equação de Valor (4 fatores) · cada entregável com o que faz, que objeção resolve, valor avulso e por que ESTE · o entregável-tese · Mapa de Valor · ancoragem · níveis de acesso (Faz Sozinho / Faço Com Você / Faço Por Você) mais a porta de entrada · custo invisível · garantia · o racional de cada escolha.
- **Saída 1 · Perfil Enxuto:** @, Nome-SEO, Bio falada, 3 destaques (Problema · Método · Clientes).
- **Saída 2 · Fundação de Headlines:** o mecanismo destilado em frases-fonte que alimentam `soft-conteudo-headlines`.

**Parte B, Voz** (os 5 elementos, observados na coleta e não prescritos): **Tom destilado** · **Narrativa pessoal** · **Bastidor estratégico** · **Valores e anti-valores** · **Pilares de conteúdo**.

### A chamada da persona nunca leva nome real

**Persona, avatar, persona-âncora, cena-assinatura e célula do Mapa de Munição são peça pública**, mesmo dentro deste documento de estratégia: é deles que nascem as capas dos meses seguintes, e é por isso que este é o documento de maior risco da operação. Rode `grep -rn 'autorizado por' <insumos>`; **saída vazia proíbe nome próprio de pessoa real em qualquer um desses cinco lugares.** A persona sai por idade, profissão e situação (`55, contadora, operou o menisco`). Quando a narrativa precisar mesmo de um nome pra chamar a pessoa, **use um nome inventado e diga na mesma linha que é inventado**: `Marta (nome inventado), 55, contadora`. **Lead com negociação em aberto na caixa de entrada nunca vira persona-âncora**: ela é a primeira a ler a peça e vai encontrar a própria transcrição virada em avatar. Depois de escrito, rode `grep -nwF -f nomes.txt <peça>`, cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada: 0 · personas com nome inventado declarado: N`.

### O Mapa de Munição da Audiência

Além do mecanismo e da Voz, o Plano entrega os 12 campos do que se sabe do público, cada um matéria-prima de um gatilho de headline. Coletado na Super Pesquisa em fala literal e na entrevista, salvo como seção do Plano. Campo sem lastro entra como `[A PREENCHER]`. Perguntas-guia de cada campo em `references/mapa-de-municao.md`.

| # | Campo | Alimenta o gatilho |
|---|---|---|
| 1 | Desejos | Recompensa |
| 2 | Problemas e dores | Recompensa, Mistério |
| 3 | Medos | Crença, Mistério |
| 4 | Situações e hábitos comuns | Reconhecimento |
| 5 | Filmes, séries e músicas conhecidos | Popularidade |
| 6 | Técnicas e procedimentos conhecidos | Popularidade |
| 7 | Pessoas e personagens conhecidos | Popularidade |
| 8 | Instituições conhecidas | Popularidade |
| 9 | Itens, objetos e ferramentas comuns | Popularidade |
| 10 | Crenças da audiência | Crença |
| 11 | Comportamentos que violam a expectativa do avatar | Disrupção |
| 12 | Características do avatar | Reconhecimento |

Quem consome: `soft-conteudo-headlines` (cada slot das fórmulas puxa de um destes campos) e as demais skills de conteúdo. Sem o Mapa, a skill de headline cai em palavra genérica.

---

## Ação 2 · PERFIL (bio, @, destaques, auditoria)

**O que faz:** escreve ou audita o perfil público do especialista (@, Nome-SEO, bio falada, os 3 destaques), ou dá nota ao perfil de um terceiro.

**Precisa de:** a Saída 1 do Plano (Perfil Enxuto), quando o Plano existir · o @ atual e o print ou o texto do perfil, pedidos ao dono.

**Sem o insumo:** sem Plano, entrevista curta de 4 perguntas: pra quem você trabalha · qual o problema que você resolve · o que você faz diferente · que prova você tem. Com essas 4 a bio sai; marque `[A CONFIRMAR]` o que faltar e diga em uma linha que o Plano completo deixaria a bio mais afiada.

**Entrega:** `perfil.md`, com @, Nome-SEO, bio falada, os 3 destaques e, em modo auditoria, a nota com o que corrigir linha a linha. **STOP.**

**O passo de entrega abre com este bloco, sozinho, antes de qualquer outra instrução:** `python3 scripts/checar_titulos.py --peca <arquivos> --titulos titulos.txt --teses teses.txt --insumos <insumos> --perfil <perfil>` (passo 1, com a saída colada) → preencher `conferencia/checagem-titulos.md` → `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <insumos> --perfil <perfil> > conferir.txt 2>&1; echo exit=$? >> conferir.txt` → `ls` colado. **Nada mais entra nesse bloco:** lint por arquivo, inventário e consentimento são consequência dele, porque o `--conferir` já os roda. A régua está em `shared-references/crivo/07-regua-de-titulos.md`, e os arquivos da ação saem junto do `conferencia/checagem-titulos.md` e do `conferir.txt`.

**Leia primeiro:** `references/modo-perfil.md`.

**Profundidade:** `references/bloco-5-fundacao-headlines.md` · `scripts/score_perfil.py` (o Score de Autenticidade pra auditar perfil de terceiro; rode no shell quando o ambiente permitir).

---

## Ação 3 · PESQUISA (o Dossiê de Nicho isolado)

**O que faz:** entrega a Super Pesquisa estruturada do nicho sem construir o Plano inteiro: concorrentes, vocabulário cru do público em fala literal, preços, força do Problema Avançado e os 12 campos do Mapa de Munição.

**Precisa de:** o nicho e o avatar declarados pelo dono · acesso à web, quando o ambiente tiver.

**Sem o insumo:** sem acesso à web, peça o material ao dono numa pergunta única ("me manda 3 concorrentes, os links, e o preço que eles praticam") e trabalhe em cima do que ele mandar. Sem nada disso, a pesquisa não roda: diga isso em uma linha em vez de inventar dados de mercado.

**Gate de proveniência da pesquisa.** Nome de marca, de pessoa, domínio, identificador de fórum ou preço de concorrente só entra no dossiê com a chamada de busca que o produziu citada na mesma linha. Sem ferramenta de busca no ambiente e sem os links colados pelo dono, a tabela de concorrente sai como categoria sem nome (`Concorrente A [A CONFIRMAR: exige busca]`) e o campo de preço fica com o mesmo marcador. Nunca declare que a pesquisa pública foi executada quando nenhuma busca rodou, e nunca date uma busca que não aconteceu. Inventar concorrente reprova a entrega inteira, e num nicho regulado vira risco jurídico pro dono.

**Ausência de capacidade se prova por comando.** Antes de declarar que o ambiente não tem busca, gerador de imagem, ferramenta de conta ou shell, rode e cole a saída literal, o erro incluso. Numa rodada uma entrega declarou `sem acesso à web, ambiente sem busca configurada` e fechou com `fontes declaradas: 0 · comandos no log: 0`; a outra, no mesmo ambiente, abriu três URLs e colou duas triplas com trecho, URL e data, e a declaração custou metade do plano. `sem acesso à web` sem o comando que falhou colado ao lado deixa de ser caminho previsto e passa a contar como pesquisa não tentada. Cole `busca tentada: <comando> · resultado: <saída literal>`, e no `RELATO.md` a linha que declara a ausência leva o bloco cercado com o comando nas 3 linhas seguintes: sem ele o `--conferir` sai com `afirmação de ausência sem comando colado` e exit 1.

**Entrega:** `dossie-de-nicho.md`, com as frentes da Super Pesquisa em tabela e o Mapa de Munição com os 12 campos preenchidos ou `[A PREENCHER]`. **STOP.**

**O passo de entrega abre com este bloco, sozinho, antes de qualquer outra instrução:** `python3 scripts/checar_titulos.py --peca <arquivos> --titulos titulos.txt --teses teses.txt --insumos <insumos> --perfil <perfil>` (passo 1, com a saída colada) → preencher `conferencia/checagem-titulos.md` → `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <insumos> --perfil <perfil> > conferir.txt 2>&1; echo exit=$? >> conferir.txt` → `ls` colado. **Nada mais entra nesse bloco:** lint por arquivo, inventário e consentimento são consequência dele, porque o `--conferir` já os roda. A régua está em `shared-references/crivo/07-regua-de-titulos.md`, e os arquivos da ação saem junto do `conferencia/checagem-titulos.md` e do `conferir.txt`.

**Leia primeiro:** `references/super-pesquisa.md`.

**Profundidade:** `references/mapa-de-municao.md` · `references/prompts-mente-cliente.md` (hipótese que volta pra entrevista confirmar).

---

## Ação 4 · PILARES (o que ele fala, e em que proporção)

**O que faz:** define os pilares de conteúdo e o círculo temático do especialista, a partir da Voz e do mecanismo.

**Precisa de:** a Parte B do Plano (os 5 elementos de Voz) e o Mecanismo da Solução, quando o Plano existir.

**Sem o insumo:** entrevista curta de 3 perguntas: sobre o que você fala quando ninguém está pedindo · que assunto do seu mercado te dá raiva · o que você recusa fazer que todo mundo faz. Dessas 3 saem os pilares; marque `[A CONFIRMAR]` e siga.

**Entrega:** `pilares-de-conteudo.md`, com os pilares nomeados, o que cada um cobre, a proporção sugerida e o círculo temático. **STOP.**

**O passo de entrega abre com este bloco, sozinho, antes de qualquer outra instrução:** `python3 scripts/checar_titulos.py --peca <arquivos> --titulos titulos.txt --teses teses.txt --insumos <insumos> --perfil <perfil>` (passo 1, com a saída colada) → preencher `conferencia/checagem-titulos.md` → `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <insumos> --perfil <perfil> > conferir.txt 2>&1; echo exit=$? >> conferir.txt` → `ls` colado. **Nada mais entra nesse bloco:** lint por arquivo, inventário e consentimento são consequência dele, porque o `--conferir` já os roda. A régua está em `shared-references/crivo/07-regua-de-titulos.md`, e os arquivos da ação saem junto do `conferencia/checagem-titulos.md` e do `conferir.txt`.

**Leia primeiro:** `references/pilares-de-conteudo.md`.

**Profundidade:** `references/circulo-tematico.md` · `references/conexao-vs-performance.md`.

---

## Gate de qualidade (antes de entregar)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**O piso do inventário é contável e a conta vai colada.** Rode `grep -c '^- ' <perfil>` e cole a saída do comando: esse número é o PISO BRUTO. Depois desdobre toda linha que carrega mais de um valor (a oferta com preço, parcela, 3 bônus e garantia conta 6, não 1) e cole `piso bruto: N · desdobrados: M · Dados fornecidos: N+M`. **`Dados fornecidos` menor que o piso bruto reprova a entrega**, porque significa que a peça descartou campo sem registrar o motivo. Não qualifique a linha com recorte de escopo: o total é o total, e o filtro de relevância mora na coluna de destino de cada dado, nunca no total.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Fontes consultadas (esta skill pesquisa, então a seção é obrigatória).** A seção "Fontes consultadas" da entrega lista só o que foi de fato aberto neste turno, e cada linha traz o comando ou a chamada de ferramenta que abriu aquela fonte. Sem acesso à web no ambiente, a seção diz exatamente "sem acesso à web neste ambiente" e nada mais: nenhum domínio, nenhum nome de marca, nenhuma data de busca. Checagem verificável antes de fechar: conte as linhas da seção e conte os comandos registrados no relatório e escreva os dois números lado a lado, nesta forma: `fontes declaradas: N · comandos no log: N`. **Declarar 4 buscas com 1 comando no log reprova**, e o conserto é apagar as 3 linhas sem comando, nunca inventar o comando. **Cada linha de tabela sobre terceiro traz a consulta que a produziu e o trecho citado da página aberta.** Número (preço, prazo, prazo de entrega, volume, quantidade de alunos, faturamento) vindo de página de terceiro só entra com o trecho colado ao lado; sem trecho colado, o campo sai como `[A CONFIRMAR: exige abrir a página]`, e cravar o número mesmo assim reprova a entrega inteira. Memória de treino e inferência plausível não são fonte. **Descrever a fonte não é citá-la.** O trecho colado é o texto que a página devolveu, entre aspas, exatamente como veio, ao lado da URL: escrever "linhas 4 a 13 abertas", "conforme a página de planos" ou "consultado no site oficial" sem o texto dessas linhas não é prova, é a descrição de uma prova, e reprova igual a número inventado. **Se o trecho literal não estiver disponível pra colar, o número não entra:** a comparação sai sem ele, ou com a faixa marcada `[A CONFIRMAR: preço não verificado na fonte]`. Cole `números de terceiro no doc: N · com trecho literal colado: N`; diferença reprova o bloco de concorrência inteiro, e a âncora de mercado construída sobre esses números cai junto, porque é ela que o dono vai usar pra decidir se o preço dele está caro.


O gate completo, com os 13 checks e a coluna de evidência, mora em `references/crivo-do-plano.md`. Preencha a tabela de lá, imprima junto do doc, e leia o veredito. Um ✗ reprova o Plano inteiro e re-roda o bloco que falhou; Plano fraco vira entrada podre pra todas as outras skills. O resumo do que ele confere:

1. **Racional visível**, decidindo os blocos, não uma lista rasa.
2. **Dor ancorada em fala literal** da pesquisa; dor inventada reprova.
3. **Problema Avançado real**, o que as outras soluções já geraram, não o Problema Geral.
4. **O Grande Dominó existe** e cabe em uma frase.
5. **Mecanismo do Problema e da Solução**, o da Solução nomeado e concreto.
6. **Crenças contrapostas**, cada uma com o como derrubar.
7. **Clareza radical**, específico acima de abstrato.
8. **As 3 perguntas na PUV e no Mecanismo:** dá pra ver? dá pra falsificar? só você assina?
9. **Oferta por valor**, com Equação, níveis, entregável-tese e garantia.
10. **Voz observada**, saída da coleta, nunca arquétipo de catálogo.
11. **Cliente-primeiro**, zero jargão de cozinha vazado, zero traço do autor do método.
12. **Anti-IA (HARD), última ação sobre o texto final:** roda sobre o doc consolidado pronto. Conte os travessões longos (U+2014) no texto inteiro, títulos e notas de STOP inclusos. Se a conta for maior que zero, o Plano não passou: reescreve trocando por ponto ou vírgula e reconta. O mesmo pra `™`, `®` e pra família do verbo-freio banida pela régua anti-voz. Com shell, rode `python3 scripts/lint_copy.py` sobre o doc final e siga só com saída limpa; sem shell, busque à mão e confira que a conta é zero.
13. **Regulado**, disparo automático: em nicho de saúde, jurídico ou finanças a Promessa e a Projeção não cravam prazo nem desfecho garantido, e o gate não pode ser marcado como não aplicável.

---

## O que esta skill protege

- **Território:** alto resultado com baixa complexidade, o oposto da cultura do "adicione mais".
- **Mecanismo NOMEADO.** O método do especialista ganha um nome próprio, um artefato batizado, não uma ideia genérica. É o que separa posição de promessa. O nome sai **limpo**, sem `™` nem `®` colado: é maneirismo de máquina, e pra profissional de saúde é uma alegação de marca registrada que ele não tem.
- **Mecanismo = Problema + Solução, não processo.** A forma da explicação é livre, desde que seja desejável, vendável e contraponha as crenças.
- **Avatar:** o especialista de verdade, do iniciante com habilidade ao avançado cansado. Quem tem método próprio e gera resultado real. Não é quem quer viver de marketing digital.
- **Problema Avançado:** a imprevisibilidade mais a invisibilidade. O inimigo é a complexidade somada ao improviso, não a tática isolada.
- **Tensão-mestre própria.** Cada especialista crava a virada que o método DELE promete, com o avatar e a dor dele. Nunca uma frase herdada de outro.
- **Anti-raso do Mecanismo:** se a premissa cabe em qualquer especialista do nicho, está rasa. Desça até o fenômeno técnico real, que sai da pesquisa e da entrevista.
- **Anti-raso da Oferta:** é o produto que o cliente vai vender, o bloco mais detalhado, nunca enxuto.
- **Rótulo não é explicação:** "o problema é posição" é vazio; "ninguém lembra do teu nome primeiro" é a explicação.
- **Clareza radical:** simples, curto, específico acima de abstrato. Se o lead precisa gastar energia mental pra entender, reescreve.
- **Preço é do especialista**, construído pela Equação de Valor. O método ensina a precificar, não crava número.
- **Vocabulário do cliente final**, nunca jargão de marketing.
- **Sem narrar o fluxo.** Não anuncie "agora vou pra etapa X": conduza por pergunta.

---

## O que esta skill NÃO faz

Em toda rota abaixo: se a skill não estiver instalada, faço aqui em modo reduzido, com o que esta skill carrega, e marco o que ficou raso como `[A CONFIRMAR]`.

- **A headline, o gancho ou a capa da peça** → `soft-conteudo-headlines`. Aqui sai só a Fundação de Headlines, as frases-fonte.
- **O corpo da peça** (carrossel, reel, stories, repurpose) → `soft-conteudo-carrossel`, `soft-conteudo-reels`, `soft-conteudo-stories`, `soft-conteudo-multiplataforma`. Arte e PNG → `soft-designer`.
- **A oferta desenhada como stack**, com garantia escolhida, preço e esteira → `soft-plano-ofertas`. Aqui a Oferta entra como bloco do Plano, com PUV e níveis; lá ela vira produto precificado.
- **A projeção em 3 cenários, a Conta e o roadmap de 90 dias** → `soft-plano-negocio`.
- **Carta, VSL, landing, mini-webinar, isca** → `soft-funil-carta`, `soft-funil-landing`, `soft-funil-miniwebinar`, `soft-funil-isca`.
- **Script de venda, objeção, fechamento** → `soft-vendas-closer`. Prospecção e lead frio → `soft-vendas-sdr`.
- **Webinário e perpétuo** → `soft-webinar`. Lançamento → `soft-launch`.
- **"Por onde começo", "próximo passo", "valida isso"** → `soft-leon`.

## Anti-Patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Despejou o plano inteiro de uma vez | Um bloco por vez, mostra e para nos 4 STOPs antes de avançar |
| Mecanismo genérico que qualquer concorrente assina | Falha no "só você diz": desce ao fenômeno técnico real do nicho, nomeia e bate nele |
| Inventou a dor do avatar plausível | Só dor com fala real da pesquisa; sem lastro, reprova no Crivo |
| Problema Avançado virou o Problema Geral ("vender mais") | Reescreve como o que as outras soluções já geraram nele |
| Cravou o preço pelo bolso do cliente | Constrói pela Equação de Valor; o número é do especialista |
| Voz saiu de arquétipo de catálogo | Volta à coleta: a voz é observada e amplificada, nunca prescrita |
| Vazou jargão de cozinha ou o jeito do autor do método | Idioma do nicho do cliente final; roda o `shared-references/filtro-cliente-primeiro.md` |
| Fechou o Plano sem imprimir o Crivo | Sem a tabela preenchida não há handoff; preenche e re-roda o que falhou |
| Narrou o fluxo ("agora vou pra etapa X") | Não narra: conduz por pergunta e entrega o bloco limpo |
| Plano ficou espalhado no chat, nunca virou doc | O entregável é um doc consolidado no fim; o chat é só a condução |
| Colocou `™` ou `®` colado no nome do método | Nome limpo, sempre. É maneirismo de máquina e alegação que ele não tem |

## Handoff

Plano completo (Racional, os 3 blocos, as 2 saídas e os 5 elementos de Voz) é a fundação. Vira o conhecimento do agente do cliente e a fonte de toda peça: `soft-conteudo-*` (atração), `soft-plano-ofertas` (a oferta virando produto precificado), `soft-funil-*`, `soft-webinar`, `soft-launch`, `soft-vendas-sdr` e `soft-vendas-closer`. É doc vivo: revise quando mudar a oferta principal, a audiência, o inimigo do mercado, ou quando a narrativa ganhar capítulo novo.

## Transversais

`shared-references/` (operação-padrão, crivo, filtro-anti-ia, filtro-mobile-first, filtro-cliente-primeiro, dicionário conversacional, adaptação semântica) · `guia/` (a fonte do framework e o código de escrita) · `scripts/lint_copy.py` (anti-IA em código, rode no shell quando o ambiente permitir) · `scripts/score_perfil.py` · `references/EXEMPLO-FIM-A-FIM.md` · `references/crivo-do-plano.md`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **O lint é gate com código de saída, não relatório.** Rode `python3 scripts/lint_copy.py <todos os .md da entrega>; echo "exit=$?"` e cole a linha `exit=` no relatório. **`exit` diferente de 0 proíbe a entrega:** volte pro passo de escrita, conserte e rode de novo, até sair 0. Declarar que rodou o lint sem colar o veredito não conta como gate cumprido. E a frase de fecho entra na varredura junto com o resto: o CTA é o texto que mais se repete no pacote, então um molde banido ali se multiplica por todos os arquivos e pelos dados que alimentam qualquer gerador. Cole `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `shared-references/crivo/07-regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `shared-references/crivo/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**
