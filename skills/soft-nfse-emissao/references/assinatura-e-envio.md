# Assinatura e envio

Como o DPS é assinado, embalado, enviado e lido de volta. Cada fato traz a origem: o leiaute e os manuais oficiais conferidos em 01/10/2026, ou o guia de origem quando a fonte oficial não foi lida. "Conforme o guia de origem" quer dizer: ainda não conferido na fonte oficial.

## Índice

1. A assinatura XMLDSig
2. Por que implementação própria e como ela foi provada
3. A embalagem do DPS
4. Ambientes e endereços
5. TLS mútuo com o .pfx
6. As chamadas que a skill usa
7. Desfechos do envio e o número do DPS
8. A chave de acesso e a consulta pública

## 1. A assinatura XMLDSig

O perfil que a skill monta:

- assinatura envelopada, com o bloco `Signature` dentro do `DPS`, depois do `infDPS`, sem prefixo de namespace (confirmado no XSD; a assinatura é obrigatória, erro E0717);
- canonicalização C14N inclusiva, `http://www.w3.org/TR/2001/REC-xml-c14n-20010315` (o XSD 1.00 fixa essa);
- uma referência, `URI="#<Id do infDPS>"`, com duas transformações: `enveloped-signature` e a C14N inclusiva. O XSD 1.00 descreve as duas; o alvo da referência no Id do infDPS vem do guia de origem e não tem texto oficial lido;
- certificado do emitente em `KeyInfo/X509Data/X509Certificate`. As regras oficiais pedem certificado com raiz ICP-Brasil, uso de assinatura digital e não repúdio e extensão de CNPJ ou CPF (E0716), do emitente da DPS (E0718). A skill confere o CNPJ gravado no certificado contra a ficha e recusa quando a raiz do CNPJ é outra.

O algoritmo vem de `NFSE_ASSINATURA_ALGORITMO`:

| Valor | Assinatura | Digest | Origem |
|---|---|---|---|
| `sha256` (padrão) | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` | `http://www.w3.org/2001/04/xmlenc#sha256` | o guia de origem relata uso em produção |
| `sha1` | `http://www.w3.org/2000/09/xmldsig#rsa-sha1` | `http://www.w3.org/2000/09/xmldsig#sha1` | o XSD 1.00 fixa este |

O XSD 1.01 deixa os algoritmos livres e nenhum texto oficial lido manda usar SHA-256. Só o envio na produção restrita, com o certificado do dono, prova qual deles o servidor aceita. Se a assinatura for recusada, a ordem de teste é: `sha1` com versão 1.00, depois `sha256` com `NFSE_VERSAO_DPS=1.01`.

## 2. Por que implementação própria e como ela foi provada

A assinatura usa lxml para a canonicalização e cryptography para a RSA, sem a biblioteca xmlsec. Motivo: a xmlsec depende da libxmlsec1 do sistema e precisa casar a versão da libxml2 com a do lxml, com erro conhecido de versão divergente na instalação. Para um perfil fixo de uma referência, lxml e cryptography bastam e instalam por pip em qualquer máquina.

Implementação própria só vale com prova por caminho independente. O autoteste confere cada assinatura por três caminhos que não usam o código que assinou:

1. canonicalização pela biblioteca padrão do Python (expat e C14N do ElementTree), sem lxml, mais a RSA conferida pela cryptography;
2. a RSA da `SignatureValue` conferida pelo `openssl dgst`;
3. a assinatura inteira conferida pela libxmlsec1 (módulo xmlsec ou binário xmlsec1), quando existem na máquina.

Foi esse cruzamento que achou o defeito mais sério da montagem: canonicalizar o subelemento direto (`etree.tostring(infDPS, method="c14n")`), com lxml 6.1 e libxml2 2.14, pôs `xmlns=""` nos netos e o digest divergiu do da libxmlsec1. A cura foi canonicalizar uma cópia do elemento como raiz. Depois dela, os três caminhos batem em sha256 e sha1, e adulterar um valor derruba a conferência.

## 3. A embalagem do DPS

Conforme o guia de origem: o XML assinado é comprimido com gzip, codificado em base 64 e enviado no corpo JSON `{"dpsXmlGZipB64": "<...>"}`. Os manuais oficiais dizem que a mensagem da API é JSON e que a área de dados chega em base 64 que o Sefin descompacta (erros E1225 e E1226), sem citar o nome do campo. O Swagger, que traria o nome, recusou o acesso automatizado.

## 4. Ambientes e endereços

| Ambiente | tpAmb | Base usada pela skill | Origem |
|---|---|---|---|
| produção restrita (padrão) | 2 | `https://sefin.producaorestrita.nfse.gov.br/SefinNacional` | guia de origem |
| produção | 1 | `https://sefin.nfse.gov.br/SefinNacional` | página oficial de APIs e manual |

A página oficial publica o Swagger da produção restrita em `https://sefin.producaorestrita.nfse.gov.br/API/SefinNacional/docs/index`, com o segmento `/API` que o guia omite. Qual base responde de fato só se sabe no primeiro envio. Para trocar, use `NFSE_URL_BASE`:

```bash
NFSE_URL_BASE="https://sefin.producaorestrita.nfse.gov.br/API/SefinNacional" python3 scripts/nfse.py emitir --hash <hash>
```

`NFSE_URL_BASE` passa por guarda: em produção só aceita o host `sefin.nfse.gov.br`; na produção restrita só aceita host da produção restrita ou endereço local de teste, e sempre `https`.

A produção exige as duas chaves juntas: `NFSE_AMBIENTE=producao` e a flag `--producao`. Uma sem a outra é recusada sem fazer nada.

## 5. TLS mútuo com o .pfx

A conexão se autentica pelo certificado: as regras de recepção pedem certificado de transmissão ICP-Brasil válido, com uso para autenticação de cliente e extensão de CNPJ ou CPF, e os manuais tratam o titular do certificado da conexão como o solicitante. Que login e senha do portal não servem para a API é afirmação do guia de origem, sem texto oficial lido.

Como o `cliente_sefin.py` monta o TLS:

1. abre o .pfx com a senha de `NFSE_PFX_PASSWORD`;
2. grava certificado e chave em PEM numa pasta temporária 0700, arquivos 0600, com a chave cifrada por uma senha de uso único que só existe na memória;
3. carrega os dois no contexto TLS e apaga os arquivos (sobrescreve com zeros, remove e remove a pasta) antes de qualquer conexão;
4. conecta com verificação do servidor sempre ligada e TLS 1.2 ou mais novo. Se a máquina não reconhecer a cadeia do servidor, aponte `NFSE_CA_BUNDLE`; desligar a verificação está fora de cogitação.

Usa só a biblioteca padrão (http.client e ssl), sem requests.

## 6. As chamadas que a skill usa

| Chamada | Para quê | Origem |
|---|---|---|
| `POST {base}/nfse` | gera a NFS-e a partir do DPS, de forma síncrona | manual de API, seção 1.3.2 |
| `GET {base}/dps/{id}` | devolve a chave de acesso a partir do Id do DPS, se o certificado for do prestador, tomador ou intermediário | manual de API, seção 1.4 |
| `GET {base}/nfse/{chave}` | baixa a NFS-e pela chave | Swagger não lido; o guia descreve a consulta pela chave |
| `GET {base}/nfse/{chave}/eventos` | lista os eventos da nota | manual de API, seção 1.5.2 |

O manual não diz se o `{id}` de `/dps/{id}` leva o prefixo `DPS` (45 caracteres) ou só os 42 dígitos. A skill tenta os dois e só conclui que a nota não existe quando os dois respondem 404. Também existe `HEAD /dps/{id}`, que só informa se a nota foi gerada; a skill não usa.

Fica fora: o registro de evento (`POST /nfse/{chave}/eventos`), que cancela a nota. O guia de origem não detalha o esquema do evento e a skill não o implementa. Cancelamento é pelo portal ou com o contador.

## 7. Desfechos do envio e o número do DPS

| Desfecho | Quando | Número do DPS | Estado gravado |
|---|---|---|---|
| autorizada | resposta 2xx com o XML da nota (o guia de origem diz 201, não confirmado) | avança | `autorizada` |
| rejeitada | 4xx com lista de erros | avança | `rejeitada` |
| incerta | o pedido saiu e a resposta caiu, demorou, veio 5xx, 408, 429, ou veio 2xx sem o campo esperado | avança | `incerta`, com a resposta bruta guardada |
| não enviada | a conexão nem abriu | fica livre | `nao_enviada` |

O leitor da resposta é tolerante: procura os campos sem depender de maiúscula e minúscula, e quando falta o campo esperado grava a resposta bruta em `resposta-bruta.txt` e trata o envio como incerto, em vez de quebrar e perder a informação.

Envio incerto bloqueia novas emissões no mesmo ambiente até ser resolvido por consulta. Pista oficial para testar na produção restrita: o Sefin recusa DPS cuja combinação de série, número, município e inscrição já gerou nota (E0014), o que sugere que reenviar o mesmo DPS não duplica nota. É inferência sem teste. Enquanto ela não for provada, a skill segue a regra segura: consulta pelo Id do DPS e pela chave antes de qualquer reenvio, e o número usado na tentativa incerta nunca volta.

## 8. A chave de acesso e a consulta pública

A chave de acesso tem 50 dígitos e fica no atributo `Id` de `infNFSe`, depois do prefixo `NFS` (confirmado no XSD). O QR do PDF aponta para a consulta pública no formato que a NT 008 manda:

```text
https://www.nfse.gov.br/ConsultaPublica/?tpc=1&chave=<chave de acesso>
```

A NT 008 também cita uma API oficial de geração do DANFSe com suspensão prevista para 01/07/2026, passando a geração aos softwares emissores. Por isso a skill gera o PDF localmente, a partir do XML, e não depende de API de PDF.
