# Armadilhas

As sete lições do guia de origem, reescritas, e as que apareceram na montagem e na conferência contra a documentação oficial. Cada uma traz o sintoma, que é como ela aparece no dia a dia, e a cura, que é o que a skill já faz ou o que o agente faz.

## As sete lições do guia de origem

### 1. Contar com o PDF pela API

**Sintoma.** O endereço de PDF da API devolve erro ou está fora do ar, e a nota emitida fica sem PDF para mandar ao cliente.

**Cura.** O PDF sai do XML, localmente, pelo `danfse.py`. A NT 008 confirma que a API oficial de DANFSe tinha suspensão prevista para 01/07/2026, com a geração passando aos softwares emissores. Sem fpdf2 e qrcode instalados, a nota sai igual (o XML é o documento fiscal) e o PDF fica para depois do `pip install`.

### 2. QR apontando para endereço que não abre

**Sintoma.** O cliente lê o QR do PDF e cai numa página quebrada. Passa meses sem ninguém notar.

**Cura.** O QR usa o formato da consulta pública que a NT 008 manda: `https://www.nfse.gov.br/ConsultaPublica/?tpc=1&chave=<chave>`. O autoteste renderiza o PDF, lê o QR por máquina e confere o endereço caractere a caractere.

### 3. Namespace só no primeiro nível

**Sintoma.** O governo aceita a nota, mas o PDF sai sem CNPJ, sem cliente e sem valor. A leitura qualificou só o primeiro nível (por exemplo `emit/CNPJ` com namespace só em `emit`) e os campos de dentro voltaram vazios.

**Cura.** O leitor da skill qualifica o namespace em cada nível de cada caminho. O autoteste roda os dois leitores no mesmo XML fictício: o da skill acha CNPJ, cliente e valor; o ingênuo volta vazio nos três. Qualquer leitor novo passa por esse teste antes de entrar.

### 4. Confundir o código de retenção do ISS

**Sintoma.** A nota sai com ISS retido quando devia sair sem retenção, ou o contrário, e o acerto vira retrabalho com o cliente e o contador.

**Cura.** No padrão nacional, `tpRetISSQN` 1 é não retido, 2 retido pelo tomador, 3 retido pelo intermediário (confirmado no XSD). Segundo o guia de origem, ainda não conferido na fonte oficial, o padrão antigo das prefeituras usava 1 para "sim". O valor vem do contador e fica na ficha do cliente, nunca do palpite do agente. Retenção 2 ou 3 sai como LIMITE, porque as regras oficiais exigem a alíquota nesse caso.

### 5. Achar que o XML mostra o cancelamento

**Sintoma.** A nota foi cancelada no portal, mas o PDF gerado do XML continua mostrando a nota como normal.

**Cura.** Cancelamento é um evento à parte (e101101; a substituição gera e105102). Rode `eventos --chave <chave>`: a skill grava o resultado na pasta da nota e o `pdf` seguinte sai com a marca CANCELADA ou SUBSTITUÍDA. PDF gerado sem consulta de eventos diz no rodapé que a situação não foi consultada. Que o XML da nota fica intacto depois do cancelamento é inferência do modelo de eventos, sem frase oficial lida.

### 6. Certificado vencido de surpresa

**Sintoma.** Num dia qualquer nada funciona: a assinatura e a conexão falham ao mesmo tempo.

**Cura.** Todo `preparar`, `emitir`, `consultar` e `conferir` lê a validade do .pfx. Com 30 dias ou menos, imprime `AVISO: o certificado vence em N dia(s)`, e o agente repassa o aviso ao dono na mesma conversa. Vencido, recusa. O comando `certificado` sai com código 1 quando faltam 30 dias ou menos, para entrar numa rotina agendada se o dono quiser.

### 7. Erro de rede na hora de emitir

**Sintoma.** A conexão cai depois que o pedido saiu. O agente tenta de novo, com número novo de DPS, e o cliente recebe duas notas.

**Cura.** A skill nunca tenta de novo sozinha. Grava a tentativa como incerta, bloqueia novas emissões no mesmo ambiente e manda rodar `consultar --dps <Id>`. Achou a nota: ela é baixada e a pendência some. Não achou nos dois formatos de Id: o dono confere no portal e libera com `resolver --dps <Id> --sem-nota`. Conexão que nem abriu fica registrada como não enviada e o mesmo rascunho pode ir de novo.

## O que apareceu na montagem e na conferência oficial

### 8. Canonicalização do subelemento

**Sintoma.** A assinatura confere no próprio código que assinou e é recusada por qualquer validador de fora.

**Cura.** Com lxml 6.1 e libxml2 2.14, canonicalizar o subelemento direto pôs `xmlns=""` nos netos. A skill canonicaliza uma cópia do elemento como raiz, e o autoteste confere com libxmlsec1, openssl e a canonicalização da biblioteca padrão. Conferir a assinatura só com o mesmo código que assinou esconde esse tipo de erro.

### 9. Relógio adiantado

**Sintoma.** Rejeição por data de emissão posterior ao processamento (E0008) ou competência posterior à emissão (E0015).

**Cura.** O `dhEmi` recua 1 minuto e a competência no futuro é recusada no `preparar`. Relógio muito adiantado continua dando erro: mantenha a hora da máquina sincronizada.

### 10. Algoritmo e versão sem resposta oficial

**Sintoma.** A primeira nota na produção restrita volta com erro de assinatura ou de esquema.

**Cura.** O XSD 1.00 fixa RSA-SHA1, o 1.01 deixa livre e nenhum texto oficial lido manda SHA-256, que é o que o guia de origem relata. Teste nesta ordem: o padrão (`sha256`, versão 1.00); depois `NFSE_ASSINATURA_ALGORITMO=sha1`; depois `NFSE_VERSAO_DPS=1.01` com `sha256`. Registre qual passou e use o mesmo par em produção.

### 11. Base da produção restrita

**Sintoma.** Toda chamada na produção restrita volta 404.

**Cura.** A página oficial mostra o Swagger em `https://sefin.producaorestrita.nfse.gov.br/API/SefinNacional/docs/index`, com o segmento `/API` que o guia de origem omite. Use `NFSE_URL_BASE` com esse segmento e tente de novo. Um 404 no envio vem como rejeição, então nada foi emitido.

### 12. Regime fora do que a skill monta

**Sintoma.** Rejeição por regime especial (E0175), por alíquota ausente com retenção (E0621, E0628) ou por opção do Simples que não bate com o cadastro (E0160).

**Cura.** A skill só monta ME/EPP com regApTribSN 1, regEspTrib 0, tribISSQN 1 e sem retenção, e recusa o resto antes do envio com a frase de limite. Se o cadastro do Simples na competência não bater com a ficha, a correção é do contador.

### 13. Certificado de outro CNPJ

**Sintoma.** Rejeição porque a assinatura não é do emitente (E0718).

**Cura.** A skill lê o CNPJ gravado no certificado e compara com a ficha. Raiz diferente: recusa antes do envio. Mesma raiz e filial diferente: avisa e segue, para a produção restrita confirmar.
