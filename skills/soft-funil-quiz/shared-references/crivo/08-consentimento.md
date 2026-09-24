# Consentimento de nome real (crivo executável, roda antes de toda entrega pública)

> Vale pra toda peça que sai desta skill: headline, capa, slide, frame, mensagem de chat, e-mail, roteiro, fala, bloco de página, legenda. A regra escrita mora na 07 (bloco "Origem do depoimento"); aqui está o COMANDO que prova que ela foi cumprida. A contagem de nome nunca sai da memória: sai de duas varreduras do disco, coladas na entrega.

## Por que virou comando

A regra em texto já existia e a peça saiu com dois nomes de caixa de entrada dentro dela, e a linha `vindos de conversa privada sem autorização: 0` três parágrafos abaixo. O motor leu a regra, escreveu a frase, e nunca varreu o arquivo. Declarar de cabeça não é checagem: os dois greps abaixo é que são.

## Onde o nome FICA, antes de qualquer varredura

**Nome de pessoa fica no arquivo interno que o dono usa; a anonimização é só pra peça PÚBLICA.** A fila do dia, o dossiê da call, a lista de prospecção, o caso de reclamação e o relatório são ferramenta de trabalho: o dono responde no aplicativo de mensagem chamando a pessoa pelo nome, e trocar por "contato 1" ou "contato A" obriga ele a abrir um segundo arquivo e cruzar número com nome numa manhã corrida. Ali o nome é a coluna que faz o arquivo servir.

A régua deste documento vale na PEÇA PÚBLICA: post, carta, landing, anúncio, stories, reel, e-mail em massa. O `checar_titulos.py` classifica por nome de arquivo e por seção declarada de uso interno, imprime `uso interno: <arquivo>` e tira esse arquivo do gate de nome. Arquivo cujo nome diz peça pública (post, carrossel, carta, landing, anúncio, reel, e-mail) continua na régua mesmo quando também parece interno.

## Os 3 passos, nesta ordem, com a saída colada

**Passo 1 · extrair a lista de primeiros nomes dos insumos PRIVADOS.** Insumo privado é caixa de entrada, transcrição de call, print de conversa, reclamação, e o perfil do dono (`dono.md` ou como ele se chamar nesta rodada). Rode nos insumos, não na peça:

```
grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u
```

Some a essa lista todo nome que apareça em lista explícita colada pelo dono (uma linha `Cláudia, Ana Paula, Renata`, um cabeçalho `De: <nome>`, uma coluna de planilha). Cole a lista resultante na entrega, na forma `nomes nos insumos privados: <n1>, <n2>, ... (N nomes)`. Lista vazia é resultado válido e vai colada do mesmo jeito.

**Passo 2 · procurar cada nome dessa lista DENTRO da peça entregue.** Um comando por nome, palavra inteira, casamento literal, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê:

```
grep -nwF '<nome>' <peça>
```

**A peça é o arquivo inteiro**, campos de configuração, filtros, checklists e rodapé inclusos, não só as linhas que o destinatário lê. Com vários nomes, `grep -nwFf <arquivo-com-a-lista> <peça>` faz a varredura numa passada e serve igual, desde que a saída venha colada.

**Passo 3 · colar a saída literal e a contagem.** A entrega fecha com o bloco, sem reescrever nada:

```
nomes nos insumos privados: <lista> (N)
saída de grep -nwF na peça:
<cole aqui a saída literal, linha por linha, ou a palavra "vazio">
nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0
```

## O que reprova, mecanicamente

- **Nome presente sem linha de autorização reprova.** Cada linha devolvida pelo `grep -nwF` precisa da linha `autorizado por <dono> em <data>` no próprio insumo, apontada por `<arquivo:linha>`. Sem ela, o nome sai da peça e a forma anonimizada por faixa ("uma aluna na casa dos 50") toma o lugar dele, ou a peça não usa o caso.
- **Contagem sem as duas saídas coladas não conta como feita** e reprova antes da análise de conteúdo, do mesmo jeito que `em molde de antítese: N` sem a coluna.
- **`nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N.** Divergência reprova: a peça sai do lote e a versão anonimizada toma o lugar dela.
- **Declarar zero onde o grep devolveu linha reprova a entrega**, e essa é a falha que este arquivo existe pra matar.
- **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, nem anonimizada: o papel dela ainda não existe.
- **Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova:** o marcador registra a dúvida e não resolve o risco.
- **Persona-âncora, avatar nomeado e personagem de exemplo nunca levam nome de pessoa real dos insumos**, nem dentro de documento de estratégia. É deles que nascem as capas dos meses seguintes, e o lead com negociação em aberto na caixa de entrada é a primeira a ler a peça e a encontrar a própria transcrição virada em avatar. A persona sai por idade, profissão e situação (`55, contadora, operou o menisco`); quando o texto precisar mesmo de um nome, **use nome inventado e diga na mesma linha que é inventado** (`Marta (nome inventado), 55, contadora`). Depois de escrito, rode `grep -nwF -f nomes.txt <peça>` e cole a saída literal.
- **Lead que respondeu no chat e ainda não comprou nunca é chamada de aluna nem de cliente**, com nome ou sem.
- **Lead com pergunta sem resposta nunca vira cena de abertura.** Quem escreveu e ficou esperando lê a própria pergunta não respondida virada em copy, e reconhece a cena mesmo anonimizada. A abertura sai de prova declarada ou de fala de grupo, nunca da caixa de entrada.
- **Nome de terceiro nunca entra em pixel, e a pergunta da autorização vem ANTES do render.** Num PNG, num card, num deck ou em qualquer arte, o nome de pessoa real vira imagem que não se corrige por colagem: perguntar num arquivo já renderizado não desfaz o arquivo, e o dono que responde `pode` não repara que o nome já estava lá. Antes de renderizar, rode `grep -in 'autoriz' <perfil>` e cole a saída; sem uma linha do perfil autorizando aquele nome em peça pública, a arte sai com o papel (`uma aluna`, `uma paciente`) e a dúvida vai pro relato antes do render, escrita como pergunta em português. Rode também `python3 scripts/checar_titulos.py --render <html> --perfil <perfil>`: nome de terceiro sem autorização no HTML de render reprova com exit 1 e o render não sai. Cole `nomes de terceiro na arte: 0 · autorizações citadas no perfil: N`.

## O script acha o nome que ninguém declarou

O `nomes.txt` só lista o que o motor resolveu declarar, e declarar lista vazia era a saída fácil deste gate. Com `--insumos`, o `checar_titulos.py` varre a peça sozinho atrás de palavra capitalizada que também apareça nos insumos em linha de pessoa, e imprime por nome:

```
<Nome> · na peça: N · nos insumos: N · autorização no insumo: sim/não · mensagem privada: sim/não
```

`mensagem privada: sim` com `autorização: não` sai como `nome de conversa privada em peça pública: <Nome>` e reprova com exit 1. Vale no passo 1 e no `--conferir`, que aceita `--insumos` e `--perfil`: sem eles o gate não roda. O nome do próprio dono (linhas `- Nome`, `- Negócio`, `- Marca` do perfil) e o bastidor (handoff, checagem, relato) ficam de fora, porque lá o nome mora por regra.

## Número de terceiro sai com a tripla completa

Número de concorrente, de mercado ou de referência entra na peça na forma:

```
<número> | trecho: "<literal>" | url: https://... | consultado em: <dd/mm/aaaa>
```

Linha sem URL completa reprova o número: a referência interna da ferramenta não abre no navegador do dono. O script conta e cobra `números de terceiro: N · com trecho literal: N · com URL completa: N`, os três iguais.
## O crivo protege TERCEIROS citados, nunca o destinatário da mensagem

Este crivo cobre a pessoa CITADA dentro de uma peça, não a pessoa a quem a peça é endereçada. Aplicar a anonimização ao vocativo produz mensagem que o dono não envia: uma resposta a reclamação grave que abre com "F., você voltou hoje" trata quem reclamou como terceiro protegido e soa como erro de sistema para quem lê.

**O destinatário da mensagem usa o primeiro nome literal do insumo.** Sem nome no insumo, a mensagem abre sem vocativo, nunca com inicial. Cole:

```
mensagens escritas: N · com primeiro nome do destinatário no vocativo: N
```

Diferença entre os dois números reprova.

**Nome composto é UMA unidade no vocativo.** Copie a forma exata do insumo, sem encurtar, sem expandir e sem apelido: um insumo que traz `Ana Paula, 40` produz o vocativo `Ana Paula`, e `Olá Ana` reprova a mensagem. Cole:

```
vocativos: N · idênticos ao insumo: N
```

Os dois números iguais, e a diferença reprova.

**O papel do nome muda por ARQUIVO, e cada arquivo segue a regra do seu papel.** A mesma pessoa é destinatária no arquivo de mensagens e terceiro no documento que fala SOBRE ela, e a mesma entrega carrega os dois. No arquivo de mensagens ela usa o primeiro nome literal do insumo, em vocativo. Em qualquer documento de trabalho que fale sobre ela (fila, critério, triagem, planilha, relatório), ela entra sem identificação (`contato 3`), com o número da posição amarrando fila e mensagem. Cole as duas linhas separadas:

```
nomes literais no arquivo de mensagens: N (todos em vocativo)
nomes literais nos documentos de trabalho: 0
```

Apagar o vocativo do arquivo de mensagens pra fechar a segunda linha reprova: produz mensagem que o dono não envia. Levar o nome pro documento de trabalho pra fechar a primeira também reprova: quem lê o relatório não é quem escreveu a mensagem.

- **Anonimizar é impedir a REIDENTIFICAÇÃO, não só apagar o nome.** Idade exata mais condição de saúde mais resultado mais prazo devolvem a identidade da pessoa para quem convive com ela, e num destinatário da área de saúde isso é dado clínico de terceiro. A faixa etária substitui a idade exata ("mulher na casa dos 50"), e o prazo não confirmado sai da frase em vez de virar marcador.

## Prova declarada: a decisão sai do arquivo, não do julgamento da peça

Numa rodada, o MESMO caso (o da aula gravada, com nome e idade) foi anonimizado por seis entregas e publicado por duas, com o mesmo insumo e a mesma régua na mão. O que faltava não era rigor, era um lugar onde a decisão estivesse escrita.

**Prova que o dono declarou como prova é publicável COM o nome, e a autorização precisa estar escrita.** Quando o perfil traz um caso nominal como prova (banco de provas, case, print autorizado), a checagem cola, um por caso:

```
caso: <nome> | classe: prova declarada | linha de autorização no insumo: <arquivo:linha> ou AUSENTE
```

Com a linha, publica com o nome. **Sem a linha, publica anonimizado** (a inicial, ou uma forma sem identificação como "uma aluna na casa dos N", por faixa e nunca pela idade exata) e leva ao handoff a pergunta da autorização, numa frase pronta pro dono responder com sim ou não. O que não pode é a mesma rodada decidir diferente em duas peças com o mesmo insumo.

## O piso do inventário sai de comando

Num lote, os números declarados sobre o MESMO perfil foram 18, 29, 51, 62, 69, 84, 104, 112, 117 e 136, e o mesmo motor declarou 29 numa pasta e 112 noutra. Número que sai da cabeça varia com a cabeça. Fixe assim:

```
grep -c '^- ' <perfil do dono>
```

A saída é o número de campos de primeiro nível, e ele é o PISO. O total sai desdobrando cada campo composto nos seus valores. A entrega cola as DUAS linhas:

```
campos no perfil: N (piso, saída do grep)
valores desdobrados: M · usados: X · descartados com motivo: Y · sem destino: 0
```

com M maior ou igual a N. **Declarar um número abaixo do piso reprova; declarar só uma das duas linhas não conta como inventário feito.**

**Um dado por linha.** Agrupar dois dados numa linha reprova o crivo, mesmo quando parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. Campo de valor múltiplo desdobra: oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. A lista e a linha de fechamento moram em `conferencia/checagem-titulos.md`; no arquivo que o dono lê, o que ficou fora aparece só quando muda a decisão dele, em 1 linha.

## Sem shell

Sem terminal, o trabalho é o mesmo e à mão: escreva a lista de nomes dos insumos privados, leia a peça inteira procurando cada um, e cole a lista com o resultado por nome (`<nome>: não aparece` ou `<nome>: linha <N>`). O que não vale, com shell ou sem, é a contagem escrita sem a varredura por trás.

## Fala atribuída ao destinatário

Fórmula proibida: "você escreveu", "como você me disse", "você mesma falou" sobre fala que veio do perfil do dono e não da conversa com esta pessoa. Use a forma de grupo ("é o que eu mais escuto") ou descreva a cena sem atribuir. Checagem: para cada fala entre aspas na peça, cole `<fala> | origem: <arquivo:linha> | atribuída a: <quem> | esta pessoa disse isso? sim/não`; um "não" com atribuição direta reprova.

**Molde endereçado a pessoa nomeada exige o insumo dela aberto.** Antes de escrever a fala, rode e cole a saída:

```
grep -n '<Nome>' <insumo>
```

A fala usada sai na forma `<fala literal> | origem: <arquivo:linha> | esta pessoa disse isso? sim`. Fala atribuída sem trecho literal do insumo reprova. **É proibido preencher a fala dela com a dor-tipo do avatar e marcar `[A CONFIRMAR]`:** o marcador registra a dúvida e a mensagem já afirma, na segunda pessoa, que ela disse aquilo. Sem o insumo aberto, o molde sai na forma de grupo ou sem retomada. Cole `moldes com nome próprio: N · com fala literal do insumo: N`, os dois iguais.

## Instrução ao dono nunca entra no corpo da peça

O corpo da peça contém só o que o destinatário lê. Instrução ao dono ("confirme", "valide", "antes de publicar", "verifique com o conselho") vai no handoff ou no bloco de configuração, nunca dentro de mensagem, slide, frame, bloco de página ou fala. Checagem colada, restrita às seções públicas:

```
grep -nE 'antes de publicar|confirme|valide|verifique com' <peça>
```

Saída não vazia dentro de seção pública reprova a peça e a frase volta pro handoff.
