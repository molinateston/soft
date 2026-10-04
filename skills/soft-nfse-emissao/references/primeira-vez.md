# Primeira vez: do zero à primeira nota

Roteiro para conduzir quem nunca emitiu nota por esta skill. Quem lê é o agente. O usuário pode ser leigo: não sabe o que é DPS, não tem a ficha pronta e talvez nem tenha o certificado. Você guia, ele responde.

## Como conduzir

1. **Comece sempre pelo `conferir`.** Antes de qualquer pergunta, rode `python3 scripts/nfse.py conferir` (com `--cliente <apelido>` quando já houver cliente). A saída diz onde ele parou; a tabela "Onde ele parou" leva ao passo. Ele pode ter feito metade ontem: retome dali e diga isso.
2. **Uma pergunta por vez.** Pergunte, espere, grave a resposta na ficha, confira de novo e só então faça a seguinte.
3. **Diga onde ele está.** Abra cada passo com "Passo N de 10" e uma linha do que falta depois dele.
4. **Todo pedido tem quatro partes:** por que você precisa, onde ele consegue, como entregar e o que fazer se não souber.
5. **Termo técnico explicado na primeira vez,** com a frase da tabela "Palavras que ele vai ouvir". Depois disso, use a palavra simples. Nomes de campo como opSimpNac, cTribNac ou tpRetISSQN servem para você e para o contador; com o usuário, fale a explicação, nunca a sigla sozinha.
6. **Senha do certificado nunca passa pela conversa.** Se ele colar a senha, não use, diga que ela precisa ir para o cofre de segredos e peça para apagar a mensagem.
7. **Nada de inventar dado fiscal.** Código de tributação, retenção, regime e percentuais são do contador. Na dúvida, mande a mensagem pronta do passo 4.

## Abertura (diga isto antes do passo 0)

Fale com as suas palavras, cobrindo:

- **O que vou te pedir:** confirmar que a sua cidade emite pelo sistema nacional, o certificado digital da empresa, os dados da empresa, algumas respostas do contador e os dados do primeiro cliente.
- **Quanto leva:** com os dados à mão, a nossa parte costuma caber em meia hora. O que mais demora é o certificado (se ainda não existe) e a resposta do contador.
- **O que você recebe no fim:** a nota autorizada em três formas: o XML, que é o documento fiscal; o PDF, que é a versão para ler e mandar ao cliente; e a chave de acesso de 50 dígitos, que identifica a nota na consulta pública.
- **O que só você pode fazer:** obter ou renovar o certificado digital e guardar a senha dele. Eu não compro certificado, não vejo a senha e não decido classificação fiscal.
- **Como funciona depois:** você me pede "emite a nota de setembro do cliente X, R$ 700", eu mostro o resumo, você confirma e eu emito.

## Palavras que ele vai ouvir

| Palavra | Explicação em uma frase |
|---|---|
| NFS-e | nota fiscal de serviço eletrônica, a nota que empresa de serviço emite ao cobrar o cliente |
| padrão nacional | o sistema único do governo para NFS-e, que substitui o sistema próprio da prefeitura nas cidades que aderiram |
| DPS | a declaração que a empresa manda ao governo pedindo a nota; aprovada, ela vira a NFS-e |
| XML | o arquivo da nota em formato de máquina; é ele que vale como documento fiscal |
| PDF da nota | a versão para ler e imprimir, gerada a partir do XML |
| chave de acesso | o número de 50 dígitos que identifica a nota em qualquer consulta |
| certificado digital | o arquivo que prova que é a sua empresa assinando; sem ele o governo não aceita o pedido |
| competência | o mês a que o serviço se refere, que pode ser diferente do dia da emissão |
| prestador e tomador | prestador é a sua empresa; tomador é o cliente que recebeu o serviço |
| ISS | o imposto da cidade sobre serviço |
| retenção do ISS | quando o cliente desconta o ISS do pagamento e recolhe ele mesmo; esta skill só emite nota sem retenção |
| código de tributação nacional | o número de 6 dígitos que diz ao governo que tipo de serviço foi prestado; quem define é o contador |
| produção restrita | o ambiente de teste do governo; a nota sai de verdade no sistema, mas sem valor fiscal |
| produção | o ambiente real; a nota emitida aqui vale e não se desfaz por esta skill |
| código IBGE | o número de 7 dígitos que identifica cada cidade nos sistemas do governo |
| palavra-passe | uma palavra que você escolhe para provar que foi você quem mandou emitir a nota real |
| série e número | a sequência das suas notas nesta skill; cada nota ganha o número seguinte, sem repetir |
| convênio nacional | o acordo da cidade com o governo federal para usar o emissor nacional |
| resumo e confirmação | antes de cada nota eu mostro cliente, valor, mês e descrição, e só emito depois do seu sim |

## Onde ele parou

Percorra a tabela de cima para baixo: a primeira linha que aparecer na saída do `conferir` indica o passo. Certificado a caminho não segura o resto: siga pela linha seguinte que bater e volte ao passo 1 quando o arquivo chegar.

| O `conferir` mostra | Vá para |
|---|---|
| `NFSE_DADOS_DIR não está definida` | preparo da pasta (abaixo) e depois passo 0 |
| `falta a ficha da empresa` | rode `iniciar` e vá ao passo 0 |
| `Envios sem desfecho: 1` ou mais | resolva antes de tudo com `consultar --dps <Id>` (passo 8) |
| `LIMITE:` | a skill não serve para este caso; diga a frase de limite e pare |
| `Certificado: NFSE_PFX_PATH não definida` ou erro de certificado | passo 1 |
| `FALTA DADO` sobre CNPJ, município ou série | passo 2 |
| `FALTA DADO` sobre opSimpNac, regApTribSN ou regEspTrib | passo 3 |
| `FALTA DADO` sobre tributos aproximados | passo 4 |
| `Fichas completas (empresa)` sem cliente | passo 5 |
| `FALTA DADO` sobre o cliente | passo 5 |
| tudo completo, sem nota de teste autorizada | passo 6 e depois passo 7 |
| já há `nfse.xml` em `notas/restrita/` | passo 9 |

Para saber se já existe nota de teste autorizada: `ls "$NFSE_DADOS_DIR"/notas/restrita/*/*/nfse.xml`.

**Preparo da pasta, trabalho seu e sem pergunta técnica.** Escolha uma pasta local, fora de pasta sincronizada com nuvem e fora da pasta da skill (exemplo: `$HOME/nfse-dados`), use `NFSE_DADOS_DIR` com ela em todo comando e rode `python3 scripts/checar_dependencias.py` e `python3 scripts/nfse.py iniciar`. Se faltar biblioteca, o script imprime o comando de instalação; peça ao usuário para autorizar.

## Passo 0. A sua cidade emite pelo padrão nacional?

- **Por que:** a skill só emite pelo emissor nacional. Cidade fora do convênio nacional faz o governo recusar a nota (erro E0037).
- **Onde conseguir:** pergunte ao contador ("a minha cidade emite NFS-e pelo emissor nacional?") ou confira no portal nacional da NFS-e, na lista de municípios que aderiram.
- **Como entregar:** "sim" ou "não", e o nome da cidade.
- **Se não souber:** a pergunta 1 da mensagem pronta do passo 4 cobre isso. Siga com o passo 1 enquanto o contador responde, mas avise que o certificado só vale a pena com essa resposta em "sim".
- **Confira também agora:** a empresa é MEI? Se for, esta skill não serve (só cobre ME ou EPP do Simples), e é melhor saber antes de gastar com certificado.
- **Se a resposta for "não":** diga "Esse caso fica fora desta skill. Encaminhe ao contador ou emita pelo portal nacional." Se a cidade usa sistema próprio, a nota sai pelo sistema da prefeitura ou pelo contador.

## Passo 1. O certificado digital

- **O que é:** um arquivo com final `.pfx` que funciona como a assinatura da empresa. O guia de origem indica o e-CNPJ A1 (conforme o guia, não confirmado na fonte oficial); as regras oficiais lidas aceitam certificado ICP-Brasil com CNPJ ou CPF. A skill lê o arquivo `.pfx`, então certificado que só existe em cartão ou token não serve aqui.
- **Por que:** sem a assinatura do certificado o governo não aceita o pedido de nota.
- **Onde conseguir:** compra-se numa autoridade certificadora credenciada na ICP-Brasil (empresa autorizada a emitir certificado; o contador costuma indicar uma). Peça o modelo em arquivo, para CNPJ.
- **Onde guardar o arquivo:** numa pasta da máquina do agente que só o usuário do agente lê, fora de pasta sincronizada com nuvem e fora da pasta da skill. Depois de copiar, rode `chmod 600 <arquivo.pfx>`. Aponte o caminho em `NFSE_PFX_PATH`.
- **Como entregar o arquivo:** o mais seguro é copiar direto para a máquina (ele mesmo, ou quem cuida da máquina). Se ele mandar o arquivo pela conversa, salve na pasta certa, ajuste a permissão e peça para apagar a mensagem. A senha nunca vai junto.
- **Como entregar a senha:** ela entra só pelo cofre de segredos do agente ou pela variável de ambiente `NFSE_PFX_PASSWORD`, colocada pelo usuário (ou por quem cuida da máquina) direto na máquina. Explique onde fica o cofre no ambiente de vocês. Se você não souber, diga isso e peça para quem instalou o agente configurar. A senha nunca vai em argumento de comando, em arquivo da pasta de dados ou na conversa.
- **Se não souber:** "não tenho certificado" leva à compra, e o resto do roteiro pode seguir em paralelo até o passo 7. "Esqueci a senha": a skill não guarda a senha em lugar nenhum; procure a autoridade certificadora que emitiu o certificado.
- **Confere:** `python3 scripts/nfse.py certificado` mostra a validade e o CNPJ gravado no certificado, sem mostrar a senha. Senha errada aparece como "senha errada ou .pfx corrompido". Permissão aberta demais faz o script recusar e mostrar o `chmod 600` exato.
- **Fica com ele:** renovar o certificado antes de vencer. Com 30 dias ou menos, os scripts avisam e você repassa o aviso.

## Passo 2. Os dados da empresa

Pergunte um campo por vez, grave em `empresa.json` e mantenha a permissão 600.

| Campo | O que é | Onde achar |
|---|---|---|
| razão social | o nome oficial da empresa | cartão do CNPJ, o comprovante de inscrição que se tira no site da Receita Federal |
| CNPJ | o número da empresa, 14 caracteres | cartão do CNPJ; precisa ser o mesmo do certificado |
| inscrição municipal | o número da empresa na prefeitura, quando a cidade usa | alvará, cadastro da prefeitura ou contador; se a cidade não usa, fica vazio |
| código IBGE da cidade | 7 dígitos que identificam a cidade | contador, ou busca por "código IBGE" e o nome da cidade no site do IBGE |
| série do DPS | o número da sequência das notas desta skill, de 1 a 49999 | escolha; se a empresa já emitiu por outro programa, use uma série que ele nunca usou |

- **Por que:** sem esses dados o pedido de nota não se monta. O CNPJ ainda é comparado com o do certificado.
- **Se não souber:** o contador tem todos. A inscrição municipal o `conferir` não pergunta sozinho, então pergunte você.
- **Série já usada antes:** grave a série e rode `python3 scripts/nfse.py contador --ajustar <último número usado>`, para a numeração continuar dali.
- **Confere:** `conferir` sem `FALTA DADO` de CNPJ, município ou série, e a linha do certificado sem alerta de CNPJ diferente.

## Passo 3. Simples Nacional, em palavras simples

Explique assim: o Simples Nacional é o jeito simplificado de a empresa pequena pagar impostos. ME é microempresa e EPP é empresa de pequeno porte. MEI é outra categoria e fica fora desta skill.

Três campos dizem ao governo como a empresa paga imposto. A skill só monta esta combinação:

| Nome técnico (para você e o contador) | Valor | O que quer dizer para ele |
|---|---|---|
| opSimpNac | 3 | a empresa é optante do Simples como ME ou EPP |
| regApTribSN | 1 | os impostos federais e o ISS são calculados dentro do Simples |
| regEspTrib | 0 | a empresa não tem regime especial de tributação |

- **Por que:** o governo confere a nota contra o cadastro do Simples. Valor errado faz a nota voltar recusada.
- **Onde conseguir:** com o contador. Estão nas perguntas 2, 3 e 4 da mensagem do passo 4.
- **Se a resposta for outra:** MEI, não optante, apuração 2 ou 3, ou regime especial diferente de 0 ficam fora. Diga a frase de limite e pare.
- **Confere:** `conferir` sem `FALTA DADO` desses campos e sem linha `LIMITE`.

## Passo 4. O que só o contador responde

O código de tributação nacional, a tributação e a retenção do ISS e os percentuais aproximados de tributos são do contador. Você não sugere número. Dê ao usuário esta mensagem para copiar e mandar:

```text
Olá! Vou emitir a NFS-e da minha empresa pelo emissor nacional, com um sistema automático.
Empresa: <razão social>, CNPJ <CNPJ>, cidade <cidade>.
Preciso que você me confirme:
1. A cidade emite NFS-e pelo emissor nacional (convênio nacional)?
2. A empresa é optante do Simples Nacional como ME ou EPP (opSimpNac 3)?
3. O regime de apuração no Simples é federais e ISS dentro do Simples (regApTribSN 1)?
4. Existe regime especial de tributação (regEspTrib)? Espero 0, nenhum.
5. Qual o código de tributação nacional (cTribNac, 6 dígitos) deste serviço: <descreva o serviço>?
6. O ISS é tributável normalmente (tribISSQN 1)? Algum cliente retém o ISS?
7. Quais os percentuais aproximados de tributos federais, estaduais e municipais para a nota?
8. A empresa já emitiu NFS-e pelo emissor nacional? Se sim, com qual série e qual o último número?
Obrigado!
```

- **Por que:** a classificação fiscal define o imposto da nota. Erro aqui gera nota errada, e nota emitida em produção não se desfaz por esta skill.
- **Como entregar:** ele cola a resposta do contador na conversa. Você grava os percentuais em `empresa.json` e guarda o código e o ISS para a ficha do cliente (passo 5).
- **Se algum cliente retém o ISS:** a nota desse cliente fica fora da skill. Diga a frase de limite para esse cliente e siga com os outros.
- **Confere:** `conferir` sem `FALTA DADO` de tributos aproximados.

## Passo 5. O primeiro cliente

- **Por que:** a nota sai em nome de um cliente. Cada cliente tem uma ficha em `clientes/<apelido>.json`, preenchida uma vez.
- **Apelido:** um nome curto em minúsculas, com letras, números, hífen ou sublinhado (exemplo: `cliente-x`). É o nome que ele vai usar ao pedir a nota.
- **Pergunte um por vez:** CNPJ ou CPF, razão social ou nome completo, CEP, código IBGE da cidade do cliente, rua, número (ou S/N), complemento (opcional), bairro, cidade onde o serviço foi prestado, e um texto fixo de descrição se o serviço se repete todo mês (opcional).
- **Onde conseguir:** com o próprio cliente ou no cadastro que ele já tem dele (contrato, cartão do CNPJ do cliente). Código, tributação e retenção vêm da resposta do contador no passo 4.
- **Se não souber a cidade da prestação:** pergunte onde o serviço foi feito; se ele não tiver certeza, a pergunta vai ao contador.
- **Confere:** `python3 scripts/nfse.py conferir --cliente <apelido>` até mostrar "Fichas completas".

## Passo 6. A palavra-passe

- **O que é:** uma palavra que ele escolhe, com pelo menos 6 caracteres, diferente da senha do certificado. Ela é pedida a cada nota real, para provar que foi ele quem mandou emitir. O teste do passo 7 não pede.
- **Por que:** emitir nota real é irreversível. A palavra-passe impede que uma mensagem mal entendida vire nota.
- **Como entregar:** o melhor é ele mesmo rodar `python3 scripts/nfse.py palavra-passe --definir` no terminal da máquina e digitar (não aparece na tela). Se ele só fala pela conversa, ele manda a palavra, você entrega ao comando pela entrada padrão, nunca como argumento, e pede para apagar a mensagem. O arquivo guarda só uma impressão digital da palavra (hash com sal), nunca a palavra.
- **Se não souber qual usar:** sugira uma frase curta que só ele lembre, sem relação com a senha do certificado.
- **Confere:** `python3 scripts/nfse.py palavra-passe --status` mostra "Palavra-passe definida."

## Passo 7. A nota de teste na produção restrita

Explique antes: a produção restrita é o ambiente de teste do governo. A nota passa pelo sistema de verdade, mas **não vale como nota fiscal**, e o PDF sai marcado "NFS-e SEM VALIDADE JURÍDICA (produção restrita, ambiente de teste)". A numeração do teste é separada da numeração real.

1. Rode `python3 scripts/autoteste.py`. Ele prova a montagem, a assinatura e o PDF sem falar com o governo. Com falha, pare e relate.
2. Prepare uma nota com o primeiro cliente, um valor qualquer e o mês atual: `python3 scripts/nfse.py preparar --cliente <apelido> --valor <valor> --competencia <AAAA-MM> --descricao "teste"`.
3. Mostre o resumo em linguagem simples e espere um sim explícito, como em qualquer nota.
4. Rode `python3 scripts/nfse.py emitir --hash <hash>`.

Diga com honestidade: a skill foi provada contra um servidor de teste local, sem envio ao governo. Esta nota de teste é a primeira conversa real com o governo, e pode pedir um ajuste de endereço ou de assinatura (passo 8).

## Passo 8. Como ler o resultado

| O `emitir` mostra | O que quer dizer | O que fazer |
|---|---|---|
| `NFS-e AUTORIZADA` | o teste passou; XML e PDF guardados | mostre a chave e o PDF; siga para o passo 9 quando ele quiser |
| `REJEITADA` | o governo recusou e nenhuma nota saiu | mostre o código e a descrição do erro; erro de dado fiscal vai ao contador; corrija a ficha e prepare de novo |
| `ENVIO INCERTO` | o pedido saiu e a resposta não chegou inteira | não reenvie; rode `consultar --dps <Id>` |
| `NÃO ENVIADO` | a conexão nem abriu | pode repetir o mesmo `emitir` |
| `RECUSADO` | uma proteção da skill parou antes do envio | leia a mensagem e corrija |

Casos já previstos (detalhe em `armadilhas.md`):

- **Toda chamada volta 404:** a base do teste pode ter o segmento `/API`. Use `NFSE_URL_BASE` como a armadilha 11 descreve.
- **Assinatura recusada:** teste `NFSE_ASSINATURA_ALGORITMO=sha1`; se não resolver, volte ao sha256 e use `NFSE_VERSAO_DPS=1.01` (armadilha 10).
- **Erro E0037:** a cidade não está no convênio nacional; volte ao passo 0.
- **Envio incerto sem nota na consulta:** confira também no portal; só então ele libera com `resolver --dps <Id> --sem-nota`.

Relate em palavras simples: o que aconteceu, em qual ambiente e qual o próximo passo.

## Passo 9. Passar para a produção

- **Quando:** só quando ele disser, com essas palavras, que quer emitir de verdade, e depois de pelo menos uma nota autorizada no teste com o mesmo certificado e as mesmas fichas.
- **O que muda para ele:** a nota passa a valer como documento fiscal; cada nota pede a palavra-passe; nota emitida não se desfaz por esta skill (cancelar ou substituir fica no portal nacional ou com o contador).
- **Como você emite:** `preparar` com `NFSE_AMBIENTE=producao` na frente, resumo, sim dele, e então `NFSE_AMBIENTE=producao python3 scripts/nfse.py emitir --hash <hash> --producao --palavra-passe-stdin`, com a palavra-passe pela entrada padrão. Nunca reaproveite a palavra de uma mensagem anterior.
- **Confere:** o resumo do `preparar` mostra "PRODUÇÃO (nota com valor fiscal)" antes de ele confirmar.

## Passo 10. A primeira nota real e o que guardar

1. Faça o pedido como numa nota normal: cliente, valor, mês de competência e descrição. Rode `preparar`, mostre o resumo, espere o sim e a palavra-passe e rode `emitir` em produção.
2. Com `NFS-e AUTORIZADA`, relate: número, chave de acesso, onde estão o XML e o PDF, e o link da consulta pública.
3. **O que guardar:** o XML é o documento fiscal e nunca se apaga. O PDF fica ao lado e é o que se manda ao cliente. A pasta de dados guarda tudo por mês, com permissão só do usuário do agente.
4. **O que vem depois:** a cada mês ele pede "emite a nota de <mês> do cliente X, R$ <valor>". Cliente novo passa pelo passo 5. Para saber se uma nota foi cancelada, rode `eventos --chave <chave>`. Aviso de certificado vencendo vai para ele com antecedência.

Feche dizendo o que ele tem agora (a nota, o XML, o PDF e a chave) e como pedir a próxima.
