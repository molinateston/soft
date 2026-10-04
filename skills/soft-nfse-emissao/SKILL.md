---
name: soft-nfse-emissao
description: >-
  Emite NFS-e no padrão nacional (emissor nacional da NFS-e) para empresa do Simples Nacional ME/EPP, com portões: monta o DPS a partir das fichas da empresa e do cliente, mostra o resumo, espera a confirmação, assina com o certificado .pfx do dono, envia por TLS mútuo, guarda o XML autorizado e gera o PDF com QR da consulta pública. Começa sempre na produção restrita. Use quando o pedido for: "emite a nota", "nota fiscal de serviço", "NFS-e", "emitir nota do cliente X", "consulta a nota", "gera o PDF da nota", "essa nota foi cancelada?", "cadastra o cliente pra nota". NÃO use pra: calcular preço, imposto, regime ou DRE (soft-financeiro); contrato (soft-vendas-contratos); proposta (soft-vendas-proposta); converter arquivo qualquer em PDF (soft-exportar-documentos); nota de município com sistema próprio, fora do padrão nacional; MEI, não optante e regimes fora do Simples ME/EPP, em que a skill declara o limite e para; cancelar nota, que fica no portal ou com o contador. Leia e siga o fluxo inteiro do SKILL.md.
---

# Emissão de NFS-e padrão nacional

Esta skill emite a nota fiscal de serviço do dono direto na API do emissor nacional, sem portal, sem captcha e sem digitar nada além do pedido. Quem lê este arquivo é o agente do dono, com shell. O agente traduz o pedido ("emite a nota de setembro do cliente X, R$ 700, coordenação do curso") em dois comandos, mostra o resumo, espera o sim do dono e só então emite.

Três verdades guiam tudo aqui:

1. **O XML autorizado é o documento fiscal.** O PDF só representa o XML. O XML nunca se apaga.
2. **Emitir é irreversível.** Por isso a emissão tem dois passos, resumo, confirmação explícita e, em produção, palavra-passe.
3. **A skill emite o que o dono informa.** Código de tributação, retenção e regime são do contador. A skill pergunta e nunca adivinha.

Os scripts ficam em `scripts/` desta pasta. Rode tudo a partir da pasta da skill (`python3 scripts/nfse.py ...`). Se você leu este arquivo de um cache ou cópia sem a subpasta `scripts/`, pare e abra a pasta instalada.

## Para quem serve e quando não serve

Serve para empresa **optante do Simples Nacional como ME ou EPP** que emite pelo padrão nacional, nesta combinação, que é a única que a skill monta:

| Campo | Valor que a skill monta | Quem decide |
|---|---|---|
| opSimpNac | 3 (optante ME/EPP) | contador |
| regApTribSN | 1 (federais e ISS apurados no Simples) | contador |
| regEspTrib | 0 (as regras oficiais pedem 0 nesse caso, erro E0175) | contador |
| tribISSQN | 1 (operação tributável) | contador |
| tpRetISSQN | 1 (ISS não retido) | contador |

Fora dessa combinação a skill **declara o limite e para**, com esta frase: "Esse caso fica fora desta skill. Encaminhe ao contador ou emita pelo portal nacional." Ficam fora:

- MEI, não optante e regime de apuração 2 ou 3 (pedem campos de alíquota que a skill não monta);
- ISS retido pelo tomador ou intermediário (as regras oficiais exigem a alíquota pAliq nesse caso);
- imunidade, exportação e não incidência (os códigos 2 a 4 de tribISSQN mudam de significado entre as versões 1.00 e 1.01 do leiaute);
- município com sistema próprio de nota, fora do convênio nacional;
- cancelamento e substituição de nota (a skill só consulta os eventos);
- emissão em lote sem revisão nota por nota.

## O que é "pronto" nesta skill

Uma nota só está pronta quando o `emitir` imprimiu `NFS-e AUTORIZADA` com a chave de acesso de 50 dígitos e o arquivo `nfse.xml` está na pasta da nota. Rascunho preparado, envio incerto e rejeição ficam fora dessa conta, e o relato ao dono diz exatamente em qual desses estados a nota está. Dizer "emiti" sem a linha `NFS-e AUTORIZADA` na saída é a pior quebra de confiança desta skill.

## Pré-requisitos, uma vez por máquina

Para conduzir um usuário de primeira viagem por estes itens, use `references/primeira-vez.md`.

1. **Dependências.** `python3 scripts/checar_dependencias.py`. Obrigatório: lxml e cryptography. Para o PDF: fpdf2, qrcode e pillow. O script só informa o que falta e o comando de instalação; quem instala é o dono.
2. **Pasta de dados.** `NFSE_DADOS_DIR` aponta uma pasta fora da skill, local e só do usuário do agente. Depois: `python3 scripts/nfse.py iniciar`. Os scripts recusam rodar sem ela e recusam caminho dentro da pasta da skill, porque a skill vai para pacote público.
3. **Certificado.** `NFSE_PFX_PATH` aponta o arquivo .pfx (permissão 600, fora de pasta sincronizada com nuvem) e `NFSE_PFX_PASSWORD` traz a senha, vinda do cofre de segredos ou de variável de ambiente. A senha nunca passa pela conversa, por argumento ou por log. O guia de origem fala em e-CNPJ A1; as regras oficiais lidas aceitam certificado ICP-Brasil com CNPJ ou CPF, e a skill lê arquivo .pfx.
4. **Município conveniado.** O município do emitente precisa estar no convênio nacional (erro E0037 quando não está). Confira no portal antes da primeira nota.
5. **Palavra-passe de produção.** O dono define uma vez: `python3 scripts/nfse.py palavra-passe --definir` (ele digita; o arquivo guarda só hash com sal).
6. **Autoteste.** `python3 scripts/autoteste.py` prova a montagem, a assinatura, o leitor, o PDF e as guardas sem falar com o governo.

| Variável | Para quê | Padrão |
|---|---|---|
| `NFSE_DADOS_DIR` | pasta de dados do dono | obrigatória |
| `NFSE_PFX_PATH`, `NFSE_PFX_PASSWORD` | certificado e senha | obrigatórias para emitir e consultar |
| `NFSE_AMBIENTE` | `restrita` ou `producao` | `restrita` |
| `NFSE_VERSAO_DPS` | `1.00` ou `1.01` | `1.00` |
| `NFSE_ASSINATURA_ALGORITMO` | `sha256` ou `sha1` | `sha256` |
| `NFSE_URL_BASE` | troca a base da API do ambiente da vez | a base do guia de origem |
| `NFSE_CA_BUNDLE` | cadeia do servidor, se a máquina não reconhecer | a do sistema |
| `NFSE_FUSO` | fuso do horário de emissão | `America/Sao_Paulo` |

## A ficha de dados

A pasta de dados guarda uma ficha da empresa (`empresa.json`) e uma por cliente (`clientes/<apelido>.json`). O agente só preenche o que muda no mês: valor, competência e descrição. Os modelos com marcadores estão em `references/fichas-modelo.md`; o que cada campo significa e quem informa está em `references/fluxo-e-campos.md`.

Quando faltar dado, rode `python3 scripts/nfse.py conferir --cliente <apelido>`. Ele imprime a primeira pergunta pronta. Faça **uma pergunta por vez**, grave a resposta na ficha e confira de novo. Marcador de modelo (`<...>`) conta como dado faltando.

Pergunta de classificação fiscal (código de tributação nacional, retenção, regime) vai para o contador, com uma frase: "Essa classificação é do contador; pergunte a ele o código de tributação nacional e se há retenção, e com a resposta eu sigo."

## O fluxo de emissão com portões

**Antes de tudo.** Comece sempre rodando `python3 scripts/nfse.py conferir` para saber onde o usuário parou. Quando ele chega sem nada pronto ou diz que quer emitir pela primeira vez, siga `references/primeira-vez.md`: o roteiro conduz um leigo do zero à primeira nota, uma pergunta por vez, e retoma de onde ele parou.

**Portão 1, a ficha.** Extraia do pedido cliente, valor, mês de competência e descrição. Rode `conferir --cliente <apelido>`. Saída `FALTA DADO`: faça a pergunta impressa. Saída `LIMITE`: diga a frase de limite e pare.

**Portão 2, o rascunho.** Rode:

```bash
python3 scripts/nfse.py preparar --cliente <apelido> --valor 700 --competencia 2026-09 --descricao "texto do mês"
```

O `preparar` monta o DPS, confere a estrutura, grava o rascunho na pasta de dados e imprime o resumo (ambiente, cliente, valor, descrição, competência, ISS, número do DPS) e um **hash de 12 caracteres**. Nada vai ao governo neste passo.

**Portão 3, a confirmação.** Mostre o resumo ao dono em linguagem de gente e espere um sim explícito ("pode emitir", "confirmo"). Silêncio, "depois vejo" ou resposta ambígua não contam. Em produção, peça também a palavra-passe, a cada nota, e nunca reaproveite palavra-passe de mensagem anterior.

**Portão 4, a emissão.**

```bash
python3 scripts/nfse.py emitir --hash <hash>
```

Em produção, só com as duas chaves juntas, a variável e a flag, e a palavra-passe pela entrada padrão:

```bash
NFSE_AMBIENTE=producao python3 scripts/nfse.py emitir --hash <hash> --producao --palavra-passe-stdin
```

O `emitir` assina e envia **só** se o hash bater com o rascunho. Rascunho alterado, vencido (mais de 12 horas), de outro ambiente ou com número de DPS já usado é recusado, e o caminho é rodar `preparar` de novo e mostrar o resumo novo.

**Os desfechos do emitir**, pelo código de saída:

| Saída | O que aconteceu | O que fazer |
|---|---|---|
| 0, `NFS-e AUTORIZADA` | nota emitida, XML e PDF guardados | relatar ao dono |
| 5, `REJEITADA` | o governo recusou, nenhuma nota saiu | mostrar o erro; dado fiscal vai ao contador; preparar de novo |
| 6, `ENVIO INCERTO` | o pedido saiu e a resposta não fechou | **não reenviar**; rodar `consultar --dps <Id>` |
| 7, `NÃO ENVIADO` | a conexão nem abriu | pode repetir o mesmo `emitir` |
| 2, `RECUSADO` | uma guarda parou antes do envio | ler a mensagem e corrigir |

**Envio incerto.** A tentativa fica gravada como incerta e bloqueia novas emissões no mesmo ambiente. Rode `consultar --dps <Id>`: se a nota existir, ela é baixada e a pendência some sozinha. Se a consulta não achar nada, confira também no portal; só então o dono libera com `resolver --dps <Id> --sem-nota`. A regra vem da lição mais cara do guia de origem: repetir no escuro pode gerar nota em dobro.

**Passagem para produção.** Só quando o dono disser, com essas palavras, que quer emitir de verdade, e depois de pelo menos uma nota autorizada na produção restrita com o mesmo certificado e as mesmas fichas.

## Comandos

| Comando | Para quê |
|---|---|
| `iniciar` | cria a pasta de dados e as fichas-modelo |
| `conferir [--cliente X]` | o que falta, uma pergunta por vez; certificado, palavra-passe e pendências |
| `certificado` | validade do .pfx; saída 1 quando faltam 30 dias ou menos |
| `palavra-passe --definir, --trocar, --status` | palavra-passe de produção |
| `contador [--ajustar N]` | último número de DPS usado; só sobe |
| `preparar ...` | rascunho, resumo e hash |
| `emitir --hash H` | assina e envia o rascunho confirmado |
| `consultar --dps ID` ou `--chave C` | busca a nota pelo Id do DPS ou pela chave |
| `resolver --dps ID --sem-nota` | libera envio incerto que o dono conferiu sem nota |
| `eventos --chave C` | eventos da nota; marca cancelamento e substituição |
| `pdf --xml ARQ` | PDF de representação a partir do XML |
| `ler --xml ARQ` | campos do XML autorizado, lidos com namespace em todo nível |

Comandos de rede (`emitir`, `consultar`, `eventos`) também aceitam `--producao`, sempre junto de `NFSE_AMBIENTE=producao`.

## Regras de segurança

O detalhe está em `references/seguranca.md`. O essencial:

- Nunca emitir sem resumo e confirmação explícita. Nunca em lote: cada nota passa por `preparar`, resumo, sim do dono e `emitir`. O contador do DPS impede dois rascunhos pendurados com o mesmo número.
- Senha do certificado só em cofre ou variável de ambiente. Se o dono colar a senha na conversa, não use, diga que ela precisa ir para o cofre e peça para apagar a mensagem.
- Palavra-passe só pela entrada padrão, nunca como argumento de comando.
- Dado fiscal só em `NFSE_DADOS_DIR`, com permissão 600. Nada do dono dentro da pasta da skill.
- A chave privada só toca o disco em arquivo temporário 0600, cifrado com senha de uso único, apagado logo depois do carregamento e antes de qualquer conexão.
- Certificado vencido para tudo; com 30 dias ou menos, os scripts avisam e o agente repassa o aviso ao dono.

## Lições que já custaram caro

O sintoma e a cura de cada uma estão em `references/armadilhas.md`.

1. PDF pela API oficial falhou no guia de origem e a API de DANFSe tinha suspensão prevista pela NT 008: o PDF sai do XML, localmente.
2. QR no endereço errado: use o da consulta pública com `tpc=1&chave=`, confirmado pela NT 008.
3. Namespace em cada nível: leitura que qualifica só o primeiro nível devolve CNPJ, cliente e valor vazios.
4. Retenção de ISS: no padrão nacional, 1 é não retido, 2 retido pelo tomador e 3 retido pelo intermediário (confirmado no XSD). Segundo o guia de origem, ainda não conferido na fonte oficial, o padrão antigo das prefeituras usava 1 para "sim".
5. Cancelamento é evento à parte: o PDF só mostra cancelada depois de `eventos`.
6. Certificado vence: aviso com 30 dias.
7. Erro de rede: consultar antes de qualquer reenvio.
8. Canonicalização: com lxml 6.1 e libxml2 2.14, canonicalizar o subelemento direto gerou digest errado; a skill canonicaliza uma cópia como raiz e o autoteste confere com a libxmlsec1.

## O que fazer sem shell

Sem shell não há emissão. O agente monta com o dono a ficha da empresa e a do cliente (os JSON de `references/fichas-modelo.md`), escreve o resumo da nota e entrega os comandos prontos, na ordem: `iniciar`, `conferir`, `preparar` e `emitir`. A frase de fecho é literal: "A nota ainda não foi emitida. Rode estes comandos numa máquina com shell e o certificado configurado." Nunca diga que emitiu.

## Relato ao dono

Fale como numa conversa, sem rótulo fixo: o que foi feito, em qual ambiente, número e chave de acesso, onde estão o XML e o PDF, e o que falta. Exemplo: "Emiti na produção restrita a nota do cliente X, número 12, de R$ 700,00. O XML, que é o documento fiscal, ficou em `<pasta da nota>/nfse.xml` e o PDF ao lado. Chave de acesso 3550... Falta você me dizer quando passamos para produção." Em envio incerto, diga isso com todas as letras e diga que vai consultar antes de qualquer reenvio.

## Limites e encaminhamento ao contador

- Classificação fiscal (código de tributação, retenção, regime, alíquota) é do contador. Na dúvida, pare e encaminhe com uma frase.
- Cancelar ou substituir nota: pelo portal nacional ou com o contador. A skill não registra evento; só consulta.
- Rejeição com erro de dado fiscal: mostre o código e a descrição do erro e leve ao contador.
- Preço, imposto, regime e DRE ficam com soft-financeiro; contrato com soft-vendas-contratos; proposta com soft-vendas-proposta; converter arquivo em PDF com soft-exportar-documentos.

## O que está provado e o que não está

**Provado pelo autoteste, sem nenhuma chamada ao governo:** Id do DPS com 45 caracteres e composição certa nas versões 1.00 e 1.01; namespace da NFS-e em todos os níveis e nenhum prefixo; assinatura conferida por três caminhos independentes do código que assinou (libxmlsec1, openssl e a canonicalização da biblioteca padrão), em sha256 e sha1, com adulteração detectada; leitor que acha CNPJ, cliente e valor onde o leitor ingênuo volta vazio; PDF com CNPJ, cliente, valor, chave, aviso de teste e QR lido por máquina; todas as guardas com mensagem literal; senha e palavra-passe fora de toda saída e arquivo; chave temporária 0600, cifrada e apagada antes da conexão; e o fluxo completo contra um servidor local de mentira com TLS mútuo (autorizada, rejeitada, incerta que virou nota, incerta sem nota, eventos com cancelamento).

**Ainda sem prova:** nenhum envio ao governo foi feito, porque falta o certificado real do dono. A primeira nota na produção restrita é a prova que falta, e estes pontos só se fecham ali:

- nomes dos campos JSON (`dpsXmlGZipB64`, `nfseXmlGZipB64`), o sucesso 201 e o empacotamento gzip com base 64: conforme o guia de origem, não confirmados na fonte oficial (o Swagger recusou acesso);
- base da produção restrita: o guia usa `https://sefin.producaorestrita.nfse.gov.br/SefinNacional`, a página oficial mostra o Swagger em `https://sefin.producaorestrita.nfse.gov.br/API/SefinNacional`; se a primeira tentativa der 404, use `NFSE_URL_BASE` com o segmento `/API`;
- algoritmo da assinatura: o XSD 1.00 fixa RSA-SHA1, o 1.01 deixa livre e nenhum texto oficial lido manda SHA-256; o padrão segue o guia (sha256) e, se a assinatura for recusada, teste `NFSE_ASSINATURA_ALGORITMO=sha1` ou `NFSE_VERSAO_DPS=1.01`;
- alvo da referência da assinatura no Id do infDPS: conforme o guia, não confirmado; a skill usa as duas transformações que o XSD 1.00 descreve;
- até quando a versão 1.00 é aceita (o erro E0001 indica prazo por versão, que não foi achado);
- se o Id em `/dps/{id}` leva o prefixo DPS; a skill tenta os dois formatos e só conclui ausência com 404 nos dois;
- tipo do certificado (A1, e-CNPJ) e a frase de que login e senha do portal não servem para a API: conforme o guia, não confirmados;
- adesão obrigatória dos municípios: não conferida;
- formato da resposta de eventos e o XML intacto depois do cancelamento: não conferidos em nota real;
- reenviar o mesmo DPS sem nota em dobro (pista do erro E0014): inferência não testada; a skill segue a regra segura de consultar antes.
