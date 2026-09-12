# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, empresa, documento, endereço, valores e datas foram
> inventados só pra mostrar a FORMA da saída. Nada disso é caso real, e nenhum documento aqui é
> válido. Num contrato de verdade, nenhum dado de parte é inventado: o que falta entra como
> `[a preencher]`.
>
> **Este exemplo também não é parecer jurídico.** Todo contrato gerado sai com o aviso de revisão
> por advogado.

**O caso fictício:** a contratada é consultora de operação pra redes de lavanderia. O contratante é
a Lavanderia Bem Passado ME, pessoa jurídica pequena, 4 lojas. O serviço é consultoria de 6 meses,
R$ 3.900 por mês, num total de R$ 23.400.

**O pedido que o dono deu, literal:** *"eles aceitaram. Manda o contrato que eu quero mandar pra
assinar hoje."*

---

## Ação 1 · MODO

O ticket total é R$ 23.400, acima dos R$ 15.000 do critério. A skill não perguntou: aplicou o modo
**robusto** e avisou em 1 linha por quê.

> "Vai no modo robusto, porque o total passa de R$ 15.000. Isso traz multa, juros e vencimento
> antecipado. Se você preferir o enxuto mesmo assim, me diz e eu troco."

O dono respondeu: *"não, esse eu quero blindado mesmo."*

**Sem STOP adicional**, porque o modo foi confirmado na mesma troca.

---

## Ação 2 · ENTREVISTA DE ESCOPO

O dono já tinha trazido metade no pedido. A skill extraiu o que dava e perguntou só o que faltava.

| Bloco | Preenchido |
|---|---|
| **A, partes** | Contratada: Marina Alencar Consultoria ME, CNPJ `[a preencher]`, Rua das Acácias 120, Ribeirão Claro. Contratante: Lavanderia Bem Passado ME, CNPJ 12.345.678/0001-90, Av. Central 88, Ribeirão Claro, contato renato@exemplo.com.br |
| **B, serviço** | Feito para você mais acompanhamento. Nome comercial: Programa Operação em 4 Lojas. Escopo: painel semanal por unidade, rotina de fechamento, 12 encontros quinzenais de 1 hora |
| **C, valor** | R$ 23.400 no total, em 6 parcelas mensais de R$ 3.900, primeira no ato da assinatura, as demais todo dia 10 |
| **D, casos** | Sem garantia de reembolso. Foro: comarca de Ribeirão Claro, cidade da contratada. Modo robusto |

**O que faltou e como a skill tratou:** o CNPJ da contratada não estava no perfil do dono. Pela regra,
documento faltando **avança** com `[a preencher]` no campo exato, e o contrato saiu com esta lista no
fim:

> **Falta preencher antes de mandar assinar:**
> - CNPJ da CONTRATADA (cláusula de qualificação das partes)

**STOP.** O dono conferiu o quadro e corrigiu o endereço da lavanderia.

---

## Ação 3 · MONTAGEM

Modo robusto, 13 cláusulas, montadas sobre `estrutura-base.md`, com a cláusula 1 pelo formato feito
para você, a cláusula 5 na modalidade parcelada e a cláusula 6 com a proteção contra calote no tom B.

**Recorte do contrato gerado**, pra calibrar o tom, sem juridiquês desnecessário:

> **CLÁUSULA 1ª. DO OBJETO**
>
> 1.1. A CONTRATADA prestará ao CONTRATANTE serviço de consultoria de operação, denominado
> comercialmente **Programa Operação em 4 Lojas**, compreendendo a implantação de painel de
> acompanhamento por unidade, a definição da rotina de fechamento semanal e o acompanhamento
> quinzenal da equipe do CONTRATANTE.
>
> 1.2. O serviço é prestado de forma remota, salvo as visitas presenciais previstas na Cláusula 2ª.

> **CLÁUSULA 5ª. DO INVESTIMENTO E DA FORMA DE PAGAMENTO**
>
> 5.1. Pelos serviços descritos na Cláusula 1ª, o CONTRATANTE pagará à CONTRATADA o valor total de
> **R$ 23.400,00 (vinte e três mil e quatrocentos reais)**, dividido em 6 (seis) parcelas mensais e
> sucessivas de **R$ 3.900,00 (três mil e novecentos reais)**.
>
> 5.2. A primeira parcela vence no ato da assinatura deste instrumento; as demais, todo dia 10 de
> cada mês subsequente.

> **CLÁUSULA 6ª. DO ATRASO NO PAGAMENTO**
>
> 6.1. O atraso no pagamento de qualquer parcela sujeita o CONTRATANTE a multa moratória de 2% (dois
> por cento) sobre o valor em atraso, acrescida de juros de 1% (um por cento) ao mês, calculados pro
> rata die, e correção monetária.
>
> 6.2. Persistindo o atraso por mais de 5 (cinco) dias, a CONTRATADA poderá suspender a execução dos
> serviços, sem que isso configure inadimplemento de sua parte.
>
> 6.3. Persistindo o atraso por mais de 15 (quinze) dias, vencem antecipadamente todas as parcelas
> vincendas, tornando-se o saldo integralmente exigível.

> **CLÁUSULA 8ª. DA NÃO GARANTIA DE RESULTADOS**
>
> 8.1. A obrigação assumida pela CONTRATADA é de meio, e não de fim. A CONTRATADA compromete-se a
> aplicar sua metodologia e seu conhecimento técnico, não sendo possível garantir resultado
> financeiro específico, o qual depende da execução, do mercado e de fatores alheios ao seu controle.

**Como o mesmo caso sairia no modo enxuto**, pra comparação, se o ticket fosse R$ 9.000:

> **9. ATRASO NO PAGAMENTO**
>
> Em caso de atraso no pagamento de qualquer parcela, as partes buscarão alinhamento sobre nova data
> de vencimento. Permanecendo o atraso por período superior a 15 (quinze) dias sem comunicação ou
> repactuação, o CONTRATADO poderá pausar a execução dos serviços e do suporte até a regularização.

A diferença é inteira: um cobra, o outro conversa. Por isso o critério de modo é numérico e não de
sensação.

**STOP.**

---

## Ação 4 · ENTREGA

**Arquivo:** `contrato-lavanderia-bem-passado-2026-09-04.docx`, salvo no diretório de saída, com o
caminho citado na resposta. Mais o markdown estruturado no chat, pra ele revisar rápido antes de
subir na plataforma de assinatura.

**Rodapé de rastreio, depois das assinaturas:**

```
Template revisado em (data do arquivo de referência, nunca a data de hoje): 2026-08-15
```

**O aviso, entregue junto:**

> Este contrato é um modelo testado, mas não substitui revisão jurídica em casos específicos. Para
> ticket alto, cliente pessoa jurídica de médio ou grande porte, ou risco específico, vale passar por
> um advogado antes de assinar.

**E a pendência, repetida na resposta:** o CNPJ da contratada continua `[a preencher]`.

---

## O mesmo caso com entrada mais meta (variante, pra mostrar a forma)

Se o acordo tivesse sido R$ 8.000 de entrada mais R$ 15.400 quando a rede batesse R$ 150.000 de
faturamento, a skill perguntaria qual das 3 variantes, e o dono escolheria a **B, meta acumulada**,
que é o padrão. O contrato sairia com a cláusula da meta mais as duas de proteção, obrigatórias:

> 4.3. O atingimento da meta é condição de timing de pagamento, não condição de existência da
> obrigação. Decorrido o prazo de 12 (doze) meses contados da assinatura deste contrato sem o
> atingimento da meta, o saldo torna-se exigível independentemente da ocorrência da meta.
>
> 4.4. A omissão do CONTRATANTE em comunicar o atingimento da meta não o exime da obrigação.
> Verificado o atingimento por qualquer meio (declaração pública, post, conteúdo publicado), a
> parcela torna-se imediatamente exigível.

Sem essas duas, o saldo fica nebuloso e nunca é cobrado.

---

## O que ficou pendente no caso fictício

- CNPJ da contratada: `[a preencher]` até o dono buscar no cartão da empresa.
- Assinatura das duas partes na plataforma que o dono usa.
- Depoimento e caso documentado, quando a consultoria terminar: isso é pós-venda, da
  `soft-vendas-closer`.
