---
name: soft-vendas-contratos
description: >-
  Gera contrato de prestação de serviço pronto pra assinar, em português brasileiro, em dois modos: enxuto (11 cláusulas, sem multa, o padrão) e robusto (13 cláusulas, proteção completa contra calote). Cobre mentoria 1:1 e em grupo, curso gravado e serviço feito para você, com contratante pessoa física ou jurídica. Use quando o pedido for: "preciso de um contrato", "contrato de consultoria", "contrato de mentoria", "fechei um cliente, como formalizo", "como protejo o recebimento", "revisa esse contrato", "contrato com entrada e meta", "cláusula de cancelamento". NÃO use pra: a proposta que apresenta a oferta antes do sim (soft-vendas-proposta); conduzir a venda e responder objeção (soft-vendas-closer); prospecção e agendamento (soft-vendas-sdr); a campanha do mês (soft-vendas-estrategias); acordo de confidencialidade isolado, cessão de direitos, contrato internacional, societário ou trabalhista, que pedem advogado. Leia e siga o fluxo inteiro do SKILL.md.
---

# O contrato que formaliza a venda já fechada

Esta skill entrega um contrato de prestação de serviço pronto pra assinar: consultoria, mentoria, serviço feito para você, curso gravado ou qualquer venda de serviço já fechada. Ela decide o modo, coleta as variáveis das partes, monta o texto sobre um template validado e entrega em arquivo com nome previsível. O resultado é um documento que o dono manda pra assinatura no mesmo dia.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra, num caso fictício de nicho neutro, a entrada que o dono deu, as perguntas que a skill fez e o contrato resumido de saída, com as 11 cláusulas do modo enxuto no tom certo, sem juridiquês. Ler antes economiza uma rodada inteira de retrabalho.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola os dados das partes e do serviço e eu monto o contrato). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pra montagem com o que o dono colou. Se faltar uma variável que o contrato não vive sem (as partes, o valor, o prazo), pergunta AQUELA variável e segue, sem repetir a entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista de escopo, uma pergunta de cada vez, e monta o contrato com o que o dono for dando.

A pergunta do modo é UMA por contrato.

**Ensina enquanto faz:** na escolha do modo (enxuto por padrão, robusto por critério) e nas cláusulas de risco, escreve UMA linha do porquê. O dono lê a razão e sabe quando pedir a proteção maior.

**Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer o modo robusto? uma cláusula de cancelamento diferente? entrada e meta? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "preciso de um contrato", "fechei cliente", "manda o contrato de mentoria" | **1 · MODO**, e segue até a 4 |
| "quero a versão blindada", "esse cliente é grande", "cliente PJ desconhecida" | **1 · MODO**, no modo robusto |
| "revisa esse contrato", "adapta esse modelo que já usei" | **5 · MODELO DO PRÓPRIO DONO** |
| "como funciona a entrada com meta", "ele paga parte quando faturar" | **3 · MONTAGEM**, no bloco de entrada mais meta |
| "o cliente atrasou", "posso pausar o serviço" | **3 · MONTAGEM**, na cláusula de atraso |

Pedido ambíguo ("preciso formalizar isso"): pergunte UMA coisa só, a pergunta do modo, na Ação 1.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · passos numerados com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Nome, documento, endereço e cidade da contratada: leia do perfil/brain do agente quando existir; se não existir, pergunte uma vez e guarde. Nunca invente dado de parte.

---

## Ação 1 · MODO (enxuto por padrão, robusto por critério)

**O que faz:** decide entre os dois modos antes de qualquer redação.

**Precisa de:** o ticket · quem é o contratante · se há risco específico conhecido.

**Sem o insumo:** se o pedido não deixou claro, pergunte uma vez:

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

> *"Você quer no modelo enxuto (mais flexível, sem multa, o que já funcionou em venda real) ou robusto (com proteção completa contra calote)? O padrão é o enxuto."*

Não pergunte de novo se o dono já indicou no pedido inicial.

**Entrega:** o modo declarado, em 1 linha, no topo do rascunho. **STOP só se o modo virar robusto sem o dono ter pedido**, porque aí ele precisa saber por quê.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/modo-soft-enxuto.md` no modo enxuto; `references/estrutura-base.md` no modo robusto.

### O critério numérico, pra não haver zona cinzenta

| Sinal | Modo |
|---|---|
| Ticket até **R$ 15.000**, contratante pessoa física, MEI ou empresa pequena, cliente que o dono já conhece | **enxuto** (o padrão) |
| Ticket **acima de R$ 15.000** | **robusto**, e avise o dono em 1 linha por quê |
| Contratante com **mais de 50 funcionários**, ou faturamento declarado acima de **R$ 4,8 milhões por ano**, ou empresa que o dono nunca atendeu | **robusto** |
| Contratante que **exige passar pelo jurídico dele** antes de assinar | **robusto** |
| Há histórico de risco (calote conhecido, briga anterior), tratamento de dados pessoais de terceiros, ou entregável com propriedade intelectual relevante | **robusto**, mesmo abaixo dos R$ 15.000 |
| O dono pediu explicitamente a versão blindada | **robusto** |

**Modo enxuto:** 11 cláusulas, linguagem direta, tom flexível no pagamento, sem multa, sem juros, sem suspensão automática agressiva. A cláusula de atraso prevê conversa primeiro e pausa só se o cliente sumir. Sem citação de lei no corpo. Tamanho típico, 3 a 5 páginas.

**Modo robusto:** 13 cláusulas, multa de mora de 2%, juros de 1% ao mês, correção, protesto e título executivo, vencimento antecipado, cláusula penal, limitação de responsabilidade, e cláusulas de proteção de dados quando aplicável. Tamanho típico, 8 a 12 páginas.

---

## Ação 2 · ENTREVISTA DE ESCOPO (as variáveis, uma vez só)

**O que faz:** coleta os dados das partes, do serviço, do valor e dos casos específicos.

**Precisa de:** os 4 blocos abaixo. Se o dono já trouxe parte no texto, extraia e confirme, não pergunte de novo.

**Sem o insumo:** aqui a regra é diferente das outras skills, porque contrato é peça jurídica.

**Entrega:** o quadro de variáveis preenchido, com o que falta marcado. **STOP.**

### O que a skill coleta

**Bloco A, partes.** Nome ou razão social da contratada · documento e endereço dela · se o contratante é pessoa física ou jurídica · nome ou razão social do contratante · documento, endereço e e-mail dele.

**Só assina quem disse sim (a regra que decide o nome do CONTRATANTE).** O nome do contratante vem de um REGISTRO EXPLÍCITO DE FECHAMENTO no insumo, e só de lá: o dono dizendo que a pessoa fechou, um pagamento confirmado, ou uma fala literal de aceite. **Transcrição de call NÃO conta como registro de fechamento**, porque uma call termina em proposta e nunca em contrato, e frase como "prefiro à vista" é preferência de pagamento dentro de uma negociação aberta, não um sim. Antes de escrever o nome, rode a busca e cole a linha `fechamento: <arquivo>:<linha> · fala literal: "<citação>"`. Com shell, `grep -rniE 'fechou|fechei|pagou|pagamento confirmado|aceito|topo|vamos fechar|pode mandar o contrato' <pasta de insumos>` lista os candidatos pra conferir um a um. **Sem essa linha, o campo sai aberto, com a grafia exata:** `[CONTRATANTE: preencher após o fechamento]`, e o nome do arquivo usa a OFERTA, não a pessoa (`contrato-<oferta>-AAAA-MM-DD`). Essa grafia é fixa e diferente do marcador comum de dado faltante de propósito: ela diz ao dono que o que falta não é o CPF da pessoa, é o sim dela. Lead que fez a call e pediu a proposta escrita, lead que perguntou se ainda tem vaga, lead que respondeu no chat e não comprou: todas recebem esse campo, nunca o nome. Chamar de cliente quem pediu a proposta e ainda está decidindo reprova a Ação 2 mesmo com todos os outros campos certos, e o dano é concreto: o dono manda pra assinar um documento que presume um sim que a pessoa não deu, às vezes antes do prazo que ela mesma pediu, que é o pior momento possível pra parecer que não se escutou. O erro está em presumir o sim, nunca na qualidade do dado. Checagem colada no quadro de variáveis: `registro de fechamento: <arquivo>:<linha> ou ausente · nome do contratante: <nome> ou campo aberto`.

**Bloco B, serviço.** Formato (mentoria 1:1 ao vivo, mentoria em grupo, curso gravado, feito para você, ou combinação) · nome comercial do programa · descrição objetiva do escopo · quantidade de sessões ou período de acompanhamento.

**Bloco C, valor e pagamento.** Valor total · modalidade (à vista, parcelado, entrada mais meta, recorrência mensal) · datas e cronograma.

**Bloco D, casos específicos.** Tem garantia, com prazo e condição · foro preferencial (padrão: cidade da contratada) · o modo definido na Ação 1.

### Quando falta um dado das partes: avança ou para

A regra é explícita, sem zona cinzenta:

| O que falta | O que a skill faz |
|---|---|
| Documento (CPF ou CNPJ), endereço ou e-mail de qualquer parte | **avança** e gera o contrato com `[a preencher]` no campo exato, mais uma lista no fim do documento com tudo que falta. O dono preenche antes de mandar assinar |
| Nome ou razão social de qualquer parte | **para** e pergunta. Contrato sem parte identificada não é contrato |
| Valor total, ou a modalidade de pagamento | **para** e pergunta. É o núcleo da obrigação |
| Descrição do escopo | **para** e pergunta. Sem escopo não há objeto |
| Prazo, quantidade de sessões, garantia, foro | **avança** com o padrão declarado (foro na cidade da contratada; sem garantia se ele não citou) e avisa em 1 linha o que assumiu |

**Nunca invente documento, endereço, e-mail ou valor.** Nem uma vez, nem "de exemplo".

---

## Ação 3 · MONTAGEM (o texto sobre o template)

**O que faz:** monta o contrato aplicando as variantes de pagamento e o tom de atraso do modo.

**Precisa de:** o modo da Ação 1 e as variáveis da Ação 2.

**Sem o insumo:** com os campos obrigatórios preenchidos e os opcionais marcados, monte assim mesmo.

**Entrega:** o contrato completo, no formato da Ação 4. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro, no modo enxuto:** `references/modo-soft-enxuto.md` (o template completo das 11 cláusulas), preenchendo as variáveis, aplicando a variante de pagamento e o tom de atraso flexível na cláusula 9.

**Leia primeiro, no modo robusto:** `references/estrutura-base.md` (as 13 cláusulas), mais `references/clausulas-por-formato.md` na cláusula 1, `references/clausulas-pagamento.md` na cláusula 5, `references/clausulas-anti-calote.md` na cláusula 6, e `references/clausulas-pf-vs-pj.md` quando o contratante for pessoa jurídica.

**Profundidade:** `references/glossario-juridico.md` (os termos técnicos) · `references/processo-contratos.md` (o processo detalhado).

### As 11 cláusulas do modo enxuto

1. Objeto do contrato · 2. Escopo dos serviços, com subitens por sessão e suporte · 3. Prazo · 4. Investimento e forma de pagamento · 5. Obrigações do contratante · 6. Obrigações da contratada · 7. Não garantia de resultados · 8. Cancelamento e reembolso · 9. Atraso no pagamento, sem multa · 10. Confidencialidade · 11. Foro.

### Entrada mais meta: as 3 variantes

Quando o pagamento é entrada mais saldo condicionado a meta, pergunte qual variante:

- **A, meta mensal.** "Saldo devido quando o contratante atingir R$ X de faturamento **em um único mês**." Mais restritiva. Use quando o dono pedir explicitamente.
- **B, meta acumulada (o padrão).** "Saldo devido quando o contratante atingir R$ X de faturamento **em valor acumulado**, podendo ser composto por uma ou mais vendas geradas com aplicação da estratégia, sem exigência de mês único." Mais flexível, e o padrão quando não houver indicação contrária.
- **C, meta por evento.** "Saldo devido quando o contratante fechar o primeiro cliente do programa com pagamento confirmado de valor igual ou superior a R$ Y." Quando a meta é um marco binário, não financeiro.

**As duas cláusulas de proteção da meta são obrigatórias em qualquer variante.** Sem elas o saldo fica nebuloso:

```
4.X. O atingimento da meta é condição de timing de pagamento, não condição
de existência da obrigação. Decorrido o prazo de 12 (doze) meses contados
da assinatura deste contrato sem o atingimento da meta, o saldo torna-se
exigível independentemente da ocorrência da meta.

4.X. A omissão do CONTRATANTE em comunicar o atingimento da meta não o
exime da obrigação. Verificado o atingimento por qualquer meio (declaração
pública, post, conteúdo publicado), a parcela torna-se imediatamente
exigível.
```

### A cláusula de atraso: os 3 tons

**Tom A, flexível (o padrão do modo enxuto):**

```
9. ATRASO NO PAGAMENTO

Em caso de atraso no pagamento de qualquer parcela, as partes buscarão
alinhamento sobre nova data de vencimento. Permanecendo o atraso por
período superior a 15 (quinze) dias sem comunicação ou repactuação, o
CONTRATADO poderá pausar a execução dos serviços e do suporte até a
regularização.
```

Sem multa, sem juros, sem suspensão automática agressiva: conversa primeiro.

**Tom B, padrão (no modo robusto):** multa de 2%, juros de 1% ao mês, suspensão em 5 dias, vencimento antecipado em 15 dias. Em `references/clausulas-anti-calote.md`.

**Tom C, reforçado:** o tom B mais cláusula penal compensatória, autorização de protesto e título executivo. Pra ticket muito alto ou cliente de risco. As variações estão na mesma referência.

---

## Ação 4 · ENTREGA (dois formatos e o nome do arquivo)

**O que faz:** entrega o contrato em formato revisável e em formato assinável, com nome previsível.

**Precisa de:** o contrato montado na Ação 3.

**Sem o insumo:** **em ambiente sem escrita em disco**, não tente gerar o arquivo editável: entregue o contrato como markdown estruturado, pronto pra copiar direto pra plataforma de assinatura. O conteúdo das cláusulas é o mesmo; muda só o formato.

**Entrega:** os dois formatos, mais o aviso obrigatório. **STOP.**

### O nome do arquivo, com formato de data fixo

`contrato-<cliente>-AAAA-MM-DD.docx`

A data é a da geração, sempre no formato ano-mês-dia com 4 dígitos no ano, pra a ordenação por nome não quebrar quando o dono tiver 30 contratos na mesma pasta. Nada de dia primeiro, nada de ano com 2 dígitos. O nome do cliente vai em minúsculas, sem acento e sem espaço, com hífen no lugar do espaço.

Exemplo: `contrato-lavanderia-bem-passado-2026-09-04.docx`.

Salve no diretório de saída do ambiente. Se o ambiente tiver um apresentador de arquivo nativo, apresente por ele; senão informe o caminho completo na resposta.

### O rodapé de rastreio, obrigatório em todo contrato gerado

No fim do documento, depois das assinaturas, entra sempre esta linha:

```
Template revisado em (data do arquivo de referência, nunca a data de hoje): [A CONFIRMAR: data da última revisão do template]
```

A data é a da última revisão do template usado, nunca a da geração, e o valor padrão do campo é `[A CONFIRMAR]`: sem saber de que revisão o template veio, o marcador fica e o dono preenche. Checagem verificável antes de fechar: compare a data do rodapé com a data de hoje; se forem iguais, quase sempre é a data de geração no campo errado, e aí volta pro marcador. Ela existe pra que, quando a lei ou a prática mudar, o dono saiba de imediato quais contratos nasceram de um modelo velho e quais já nasceram do novo. Sem esse campo, um modelo desatualizado circula por anos sem ninguém notar.

### O lint roda no que a pessoa assina, não só no rascunho

O gate de copy roda no `.md` de origem e o documento que a pessoa assina é o exportado, então o travessão longo que passa despercebido na conversão chega no papel do cliente. Depois de gerar o arquivo editável, extraia o texto de volta e linte o texto extraído:

```
python3 -c "import docx,sys; print(chr(10).join(p.text for p in docx.Document(sys.argv[1]).paragraphs))" <arquivo>.docx > contrato-extraido.txt
python3 scripts/lint_copy.py contrato-extraido.txt
```

Cole a linha `<arquivo>.docx: exit N` na lista do gate, junto das linhas dos `.md`. Exit diferente de 0 reprova a entrega e manda corrigir o `.md` de origem antes de reexportar, nunca editar o exportado à mão: o `.md` é a fonte e o exportado é derivado. A mesma regra vale pro relatório de processo: exit 1 nele significa gate não cumprido, e nunca detalhe de bastidor.

### Cláusula sem valor nenhum sai do contrato, não entra vazia

Marcar o dado que falta está certo, e uma cláusula cujo conteúdo INTEIRO é marcador não é cláusula, é um buraco com número. `O suporte ocorrerá em [A CONFIRMAR: dias e horário], com prazo de resposta de até [A CONFIRMAR: prazo] horas` promete nível de serviço e não define nenhum, o que é pior que não prometer. A regra: cláusula com pelo menos um valor real fica, com o campo que falta marcado; cláusula em que todos os valores são marcador SAI do contrato e a pendência vai pro handoff, com a linha `cláusula removida por falta de dado: <qual> · dado que falta: <o quê>`. Checagem colada: `cláusulas no contrato: N · com todos os valores em marcador: 0`.

### O aviso, obrigatório em toda entrega

> Este contrato é um modelo testado, mas não substitui revisão jurídica em casos específicos. Para ticket alto, cliente pessoa jurídica de médio ou grande porte, ou risco específico, vale passar por um advogado antes de assinar.

---

## Ação 5 · MODELO DO PRÓPRIO DONO (quando ele já tem um que funcionou)

**O que faz:** adapta o modelo que o dono já usou em venda real, em vez de substituir pelo template.

**Precisa de:** o modelo dele colado ou em arquivo · o que muda no caso novo.

**Sem o insumo:** sem o modelo em mãos, use o template desta skill e diga em 1 linha que, se ele tiver um validado, o dele vale mais.

**Entrega:** o contrato dele adaptado, com um resumo em lista do que mudou e por quê. **STOP.**

**Modelo validado em venda real vale mais que template teórico.** Aplique só os ajustes que o caso novo exige (modalidade de pagamento diferente, formato diferente), e diga quais cláusulas você mexeu. Se enxergar um risco no modelo dele, aponte em 1 linha e deixe a decisão com ele; não reescreva por conta.

---

## Gate de qualidade (roda antes de entregar, sempre)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


| Check | Passa se |
|---|---|
| **Modo justificado** | o modo saiu do critério numérico, e o robusto sem pedido do dono foi avisado |
| **Nenhum dado inventado** | todo documento, endereço, e-mail e valor veio do dono; o que faltou está como `[a preencher]` |
| **Partes identificadas** | nome ou razão social das duas partes existe; sem isso o contrato não sai |
| **Escopo e valor presentes** | objeto e obrigação de pagamento estão escritos, sem lacuna |
| **Não garantia de resultado** | a cláusula existe nos dois modos; nunca se promete resultado financeiro específico |
| **Entrada mais meta** | as duas cláusulas de proteção da meta entraram em qualquer variante |
| **Foro definido** | existe foro; o padrão é a comarca da cidade da contratada |
| **Sem cláusula abusiva** | nada de retenção integral em rescisão imotivada na primeira semana, nem penalidade desproporcional contra consumidor |
| **Sem linguagem de venda** | peça jurídica é peça jurídica; nome do programa aparece só como nome próprio |
| **Nome do arquivo** | segue `contrato-<cliente>-AAAA-MM-DD`, com a data em 4 dígitos de ano |
| **Rodapé de rastreio** | a linha "Template revisado em" está no fim do documento, com a data da revisão do template ou `[A CONFIRMAR]`, nunca a data de hoje |
| **Aviso entregue** | o aviso de revisão jurídica foi dito ao dono |
| **VEREDITO** | é o pior item; um ✗ refaz o item, não o contrato inteiro |

## Princípios de escrita

- Português brasileiro. No modo enxuto, direto, frases curtas, sem juridiquês: nada de "ad cautelam", "ex vi", "data venia". No modo robusto, técnico mas legível.
- Estrutura visual: no enxuto, cláusulas numeradas em decimais (1, 2, 3) com subitens 1.1 e 1.2. No robusto, ordinais (1ª, 2ª, 3ª) com subitens decimais. Negrito nas palavras-chave, espaço entre cláusulas.
- **Nunca prometer resultado financeiro específico.** A cláusula deixa claro que é obrigação de meio, não de fim. Se o dono explicitamente quiser garantia de resultado, alerte sobre o risco jurídico antes de redigir.
- **Proteção da contratada é o padrão.** Se o caso pedir o inverso, avise e confirme.
- **Nunca prometa blindagem total.** Contrato bem feito reduz risco, não elimina.

## Casos especiais

- **Serviço já em andamento:** inclua cláusula de ratificação retroativa, e o contrato passa a reger a relação que já existia desde a data X.
- **Cliente quer adicionar cláusula específica:** avalie se é válida e se não cria contradição. Válida, inclua. De risco (penalidade acima de 10% do total contra consumidor pessoa física, por exemplo), explique antes.
- **Cliente estrangeiro ou serviço fora do Brasil:** recuse e oriente advogado de direito internacional.

## O que esta skill NÃO faz

Estes casos pedem advogado especializado, e a skill não improvisa: acordo de confidencialidade isolado · cessão de direitos autorais · contrato internacional · contrato societário, fusão ou participação · contrato de trabalho ou prestação com vínculo · termo de uso de plataforma. Avise o dono e pare.

Roteamento pras irmãs, e se a outra não estiver instalada, esta faz o mínimo aqui e diz que fez:

- **A proposta que apresenta a oferta antes do sim** → **soft-vendas-proposta**.
- **Conduzir a venda, responder objeção, pedir o sim** → **soft-vendas-closer**.
- **Definir preço, oferta e posicionamento** → **soft-plano-posicionamento**.

## Anti-patterns

| Erro | Por que quebra | Faz assim |
|---|---|---|
| Inventou CPF, endereço ou valor pra não parar | Documento com dado falso é imprestável e expõe o dono | `[a preencher]` no campo exato, mais a lista do que falta |
| Gerou contrato sem foro | Deixa a execução sem lugar definido | Padrão: comarca da cidade da contratada |
| Usou o modo robusto por reflexo | Assusta cliente pequeno e emperra venda que já estava fechada | Enxuto é o padrão; robusto só pelo critério |
| Prometeu resultado no contrato | Cria obrigação de fim, e o dono responde por ela | Cláusula de não garantia, obrigação de meio |
| Entrada mais meta sem as 2 cláusulas de proteção | O saldo fica nebuloso e nunca é cobrado | As duas entram em qualquer variante |
| Substituiu o modelo validado do dono pelo template | Modelo que já funcionou em venda real vale mais | Adapta o dele e lista o que mudou |
| Nome de arquivo com data solta | 30 contratos na pasta e nenhum ordena direito | `contrato-<cliente>-AAAA-MM-DD` |
| Contrato sem a data de revisão do modelo | Modelo velho circula por anos sem ninguém notar | Rodapé "Template revisado em" sempre, com `[A CONFIRMAR]` quando a revisão do template for desconhecida |
| Linguagem de venda dentro do contrato | Peça jurídica com tom de anúncio perde força | Nome do programa só como nome próprio |

## Handoff

- **Pra trás:** a condução da venda é da **soft-vendas-closer**; a proposta que apresentou a oferta é da **soft-vendas-proposta**.
- **Pra frente:** contrato assinado, o cliente entra na entrega. O caso, quando der resultado, vira prova pra `soft-plano-posicionamento` e pras `soft-conteudo-*`, e o pedido de depoimento é do pós-venda na **soft-vendas-closer**.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
