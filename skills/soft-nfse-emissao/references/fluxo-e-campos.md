# Fluxo e campos do DPS

Referência dos campos que a skill monta, dos valores aceitos e de quem informa cada um. Fonte de cada fato: o leiaute oficial (XSD v1.01 de 09/02/2026 e Anexo I v1.01), conferido em 01/10/2026, e o guia de origem quando a fonte oficial não foi lida. Onde a frase diz "conforme o guia de origem", o fato ainda não foi conferido na fonte oficial.

## Índice

1. A nota nasce como DPS
2. O Id do infDPS
3. Os blocos e os campos
4. Valores aceitos
5. Quem informa o quê
6. Regras oficiais que a skill confere antes do envio
7. A NFS-e autorizada que volta

## 1. A nota nasce como DPS

A nota começa como um XML chamado DPS (Declaração de Prestação de Serviço), no namespace `http://www.sped.fazenda.gov.br/nfse`, com todos os elementos qualificados nesse namespace em todos os níveis e sem prefixo nenhum no XML inteiro (o Sefin recusa prefixo, erro E1228, e exige UTF-8, erro E1229).

```xml
<DPS xmlns="http://www.sped.fazenda.gov.br/nfse" versao="1.00">
  <infDPS Id="DPS...45 caracteres...">
    <tpAmb/> <dhEmi/> <verAplic/> <serie/> <nDPS/> <dCompet/> <tpEmit/> <cLocEmi/>
    <prest> CNPJ, IM, regTrib (opSimpNac, regApTribSN, regEspTrib) </prest>
    <toma> CNPJ ou CPF, xNome, end (endNac (cMun, CEP), xLgr, nro, xCpl, xBairro) </toma>
    <serv> locPrest (cLocPrestacao), cServ (cTribNac, xDescServ) </serv>
    <valores> vServPrest (vServ), trib (tribMun (tribISSQN, tpRetISSQN), totTrib (pTotTrib)) </valores>
  </infDPS>
  <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">...</Signature>
</DPS>
```

O desenho acima resume a ordem; o XML real sai sem espaços entre as marcas. A versão do leiaute vem de `NFSE_VERSAO_DPS`: `1.00` por padrão (o que o guia de origem relata) ou `1.01`, que é a do pacote oficial vigente. O esquema 1.01 ainda aceita o valor 1.00, mas o Sefin aplica prazo de aceitação por versão (erro E0001), e esse prazo para a 1.00 não foi achado. O grupo IBS/CBS só existe na 1.01 (erro E0854) e a skill não gera esse grupo em nenhuma das duas.

## 2. O Id do infDPS

São 45 caracteres: o literal `DPS` e mais 42 dígitos, todos com zeros à esquerda (confirmado no XSD, tipo TSIdDPS; o Sefin recusa Id diferente dessa concatenação, erro E0004).

| Pedaço | Tamanho | Exemplo fictício |
|---|---|---|
| prefixo | 3 | `DPS` |
| município emissor (IBGE) | 7 | `9999999` |
| tipo de inscrição (1 CPF, 2 CNPJ) | 1 | `2` |
| inscrição federal | 14 | `11222333000181` |
| série | 5 | `00001` |
| número do DPS | 15 | `000000000000042` |

Exemplo fictício completo: `DPS999999921122233300018100001000000000000042`. Os zeros à esquerda só existem dentro do Id. Nos elementos `serie` e `nDPS` o valor vai sem zero à esquerda (o XSD não aceita zero à esquerda em `nDPS`).

O número do DPS é sequencial por ambiente e série e nunca se repete. O contador fica em `contador-dps.json` na pasta de dados, protegido por cadeado de arquivo, e só avança depois que o pedido sai para o governo (ver `assinatura-e-envio.md`).

## 3. Os blocos e os campos

**infDPS**

| Campo | O que é | Como a skill preenche |
|---|---|---|
| tpAmb | 1 produção, 2 homologação (a produção restrita) | do ambiente da vez; o Sefin recusa tpAmb diferente do ambiente (E0006) |
| dhEmi | data e hora de emissão com fuso | hora do `preparar` menos 1 minuto, com o fuso de `NFSE_FUSO` |
| verAplic | versão do aplicativo emissor | `nfse-emissao-1.0` |
| serie | série do DPS | da ficha da empresa, de 1 a 49999 (aplicativo próprio, E0010) |
| nDPS | número do DPS | do contador |
| dCompet | data de competência | do pedido; `AAAA-MM` vira o dia 1 do mês |
| tpEmit | quem emite | sempre 1, o prestador (o Sefin recusa 2 e 3 hoje, E9996) |
| cLocEmi | município emissor (IBGE, 7 dígitos) | da ficha da empresa |

**prest (prestador)**

| Campo | O que é | Quem informa |
|---|---|---|
| CNPJ | CNPJ da empresa | dono |
| IM | inscrição municipal, quando o município usa | dono |
| regTrib/opSimpNac | situação no Simples | contador |
| regTrib/regApTribSN | regime de apuração no Simples | contador |
| regTrib/regEspTrib | regime especial de tributação | contador |

**toma (tomador, o cliente)**

| Campo | O que é |
|---|---|
| CNPJ ou CPF | documento do cliente |
| xNome | razão social ou nome |
| end/endNac/cMun | município do cliente (IBGE) |
| end/endNac/CEP | CEP, 8 dígitos |
| end/xLgr, nro, xCpl, xBairro | logradouro, número, complemento opcional, bairro |

O esquema trata o tomador como opcional (obrigatório só em casos como certos indicadores de operação, erro E0187). A skill sempre identifica o cliente, porque o pedido é "a nota do cliente X".

**serv (serviço)**

| Campo | O que é | Quem informa |
|---|---|---|
| locPrest/cLocPrestacao | município da prestação (IBGE) | dono |
| cServ/cTribNac | código de tributação nacional, 6 dígitos | contador |
| cServ/xDescServ | descrição do serviço | dono, a cada nota |

**valores**

| Campo | O que é | Quem informa |
|---|---|---|
| vServPrest/vServ | valor do serviço, ponto decimal e 2 casas | dono, a cada nota |
| trib/tribMun/tribISSQN | tributação do ISS | contador |
| trib/tribMun/tpRetISSQN | retenção do ISS | contador |
| trib/totTrib/pTotTrib | percentuais aproximados federal, estadual e municipal (os três filhos são obrigatórios) | contador |

## 4. Valores aceitos

Conferidos no XSD e no Anexo I v1.01.

| Campo | Valores | Observação |
|---|---|---|
| tpAmb | 1 produção, 2 homologação | |
| tpEmit | 1 prestador, 2 tomador, 3 intermediário | só 1 é aceito hoje (E9996) |
| opSimpNac | 1 não optante, 2 MEI, 3 ME/EPP | conferido contra o cadastro do Simples na competência (E0160) |
| regApTribSN | 1 federais e ISS no Simples; 2 federais no Simples e ISS fora; 3 federais e ISS fora | obrigatório com opSimpNac 3 (E0166), proibido com 1 ou 2 (E0162) |
| regEspTrib | 0 nenhum, 1 ato cooperado, 2 estimativa, 3 microempresa municipal, 4 notário ou registrador, 5 profissional autônomo, 6 sociedade de profissionais, 9 outros (o 9 entrou na 1.01) | ME/EPP com regApTribSN 1 exige 0 (E0175) |
| tribISSQN | na 1.01: 1 tributável, 2 imunidade, 3 exportação, 4 não incidência | o XSD 1.00 descreve 2, 3 e 4 em outra ordem; só o 1 é seguro sem o Anexo I vigente |
| tpRetISSQN | 1 não retido, 2 retido pelo tomador, 3 retido pelo intermediário | retenção 2 exige tomador com documento e endereço nacional (E0204, E0237); MEI só usa 1 (E0583) |

A skill monta apenas opSimpNac 3, regApTribSN 1, regEspTrib 0, tribISSQN 1 e tpRetISSQN 1. O resto sai como LIMITE, com a frase de encaminhamento.

Sobre pAliq: com regApTribSN 1, a alíquota é proibida sem retenção (E0625, E0631) e obrigatória com retenção (E0621, E0628), com exceções de benefício municipal. Como a skill não monta pAliq, nota com retenção fica fora.

Sobre totTrib: ME/EPP não pode usar indTotTrib (E0712) e dispõe de pTotTribSN, vTotTrib e pTotTrib. A skill usa pTotTrib, como o guia de origem.

## 5. Quem informa o quê

| Dado | Quem informa | Onde fica | Muda a cada nota? |
|---|---|---|---|
| CNPJ, IM, município, série | dono | `empresa.json` | não |
| opSimpNac, regApTribSN, regEspTrib | contador | `empresa.json` | não |
| percentuais de tributos aproximados | contador | `empresa.json` | raramente |
| exigir palavra-passe em produção | dono | `empresa.json` | não |
| documento, nome e endereço do cliente | dono | `clientes/<apelido>.json` | não |
| cTribNac, local da prestação | contador e dono | `clientes/<apelido>.json` | não |
| tribISSQN e tpRetISSQN | contador | `clientes/<apelido>.json` | não |
| valor, competência, descrição do mês | dono | pedido da nota | sim |
| tpAmb, dhEmi, verAplic, nDPS, Id, tpEmit | script | DPS montado | sim |
| assinatura e certificado | script, com o .pfx do dono | DPS assinado | sim |

## 6. Regras oficiais que a skill confere antes do envio

O `preparar` roda a conferência de estrutura e recusa o rascunho quando algo falha:

- raiz `DPS` no namespace da NFS-e e `versao` igual à configurada;
- nenhum prefixo de namespace e nenhum elemento fora do namespace (fora o bloco de assinatura);
- Id de 45 caracteres e igual à concatenação dos campos;
- campos obrigatórios presentes e no formato (data, CEP, IBGE, valores com 2 casas, percentuais);
- série de 1 a 49999 e `nDPS` sem zero à esquerda;
- ME/EPP com regApTribSN presente;
- nenhum grupo IBSCBS na versão 1.00;
- ordem dos blocos do infDPS;
- competência que não fica no futuro (o Sefin recusa competência posterior à emissão, E0015) e emissão que não fica no futuro (E0008), daí o recuo de 1 minuto no dhEmi.

Esta conferência cobre o que a skill monta. A validação completa pelo esquema acontece no Sefin (E1235), e a primeira nota na produção restrita é a prova final.

## 7. A NFS-e autorizada que volta

O XML autorizado tem a raiz `NFSe` e o bloco `infNFSe` com `Id` igual a `NFS` mais a chave de acesso de 50 dígitos (confirmado no XSD, tipos TSIdNFSe e TSChaveNFSe). A chave junta município, ambiente gerador, tipo e número de inscrição, número da NFS-e, ano e mês, código numérico e dígito verificador. Dentro de `infNFSe` ficam o emitente (`emit`), os valores calculados (`valores`) e o próprio DPS assinado. O leitor da skill (`ler --xml`) qualifica o namespace em todo nível: `infNFSe/emit/CNPJ`, `infNFSe/DPS/infDPS/toma/xNome`, `infNFSe/DPS/infDPS/valores/vServPrest/vServ`.
