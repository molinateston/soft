# Sinais de venda: a régua dos 5 sinais e o acompanhamento

Lida no passo R4 da Ação 1 e na Ação 2. Os números abaixo são faixa de partida, relatada por operadores de resposta direta e não auditada. Depois de 3 coletas semanais no nicho do dono (3 semanas, porque o sinal medido pede ao menos 3 pontos no tempo), a planilha dele substitui a régua. Dado de campanha do próprio dono, quando existir, substitui depois de 7 dias rodando.

## Por que somar sinais

Quem anuncia só gasta tempo duplicando, espalhando e variando o que está dando dinheiro. Cada sinal sozinho engana:
- anúncio bom cai por reprovação ou troca de metadado e some da biblioteca antes da hora;
- anúncio velho pode seguir no ar esquecido, com verba mínima;
- anunciante com muitos anúncios ativos pode estar só testando, e anunciante com poucos pode estar pondo verba alta em cada um.

Por isso o anúncio ganha pontos por sinal, e nenhum tipo de sinal decide sozinho.

## Os 5 sinais

| Sinal | Coluna | Ponto | Regra |
|---|---|---|---|
| S1 · Cópias | `s1_copias` | 1, ou 2 | 7 cópias ou mais do mesmo anúncio na biblioteca vale 1. 10 cópias ou mais com até 14 dias no ar vale 2 (recente e já duplicado; a fonte fala em 10 com 5 dias, e 14 dá folga pra coleta semanal). S1 vale 2 pontos, mas conta como 1 sinal |
| S2 · Várias páginas | `s2_paginas` | 1 | o mesmo texto ou o mesmo vídeo rodando em 2 páginas ou mais |
| S3 · Variações circulando | `s3_versoes` | 1 | a mesma página com 3 versões ou mais do mesmo corpo (gancho, formato ou copy trocados) |
| S4 · Views subindo | `s4_views` | 1 | views do mesmo vídeo crescem 50% ou mais entre duas coletas com até 7 dias de distância (um salto de 50 mil pra 200 mil em poucos dias é o caso típico) |
| S5 · Tempo no ar | `s5_tempo` | 1 | 7 dias ou mais ativo. De 1 a 2 meses conta como forte na leitura, mas o ponto continua 1 |

## A classe

| Classe | Regra | O que fazer |
|---|---|---|
| vendendo | 3 pontos ou mais, com pelo menos 2 sinais distintos além do tempo no ar | entra no Radar como modelável; é a única classe que se desmonta pra modelar |
| candidato | 2 pontos, com pelo menos 1 sinal além do tempo no ar | entra no acompanhamento semanal |
| observar | o resto, inclusive quem só tem tempo no ar | fica na planilha; não entra no topo |

O script calcula S1, S2, S3 e S5 na coleta e S4 no `--recalcular`. No caminho manual, a skill aplica a mesma tabela no olho e escreve os pontos na planilha.

**Limite do S2 e do S3 no script:** eles contam dentro da coleta. Uma busca estreita pode esconder a outra página que roda o mesmo texto. Quando um anúncio tem S1 alto e S2 zero, busque uma frase do texto dele como termo novo antes de fechar.

## Recência

- Começou há até 30 dias e já tem cópias: é o que está esquentando agora, e pesa mais no Radar.
- Antigo, sem cópia nova e sem variação entre duas coletas: serve de estrutura pra estudar, não de tendência.
- Ferramenta com atraso de semanas esconde o presente. A data da coleta vai em toda linha.

## Número de concorrente é sinal

Cópias, dias, views e preço de terceiro mostram onde o mercado está pondo dinheiro. Nenhum deles diz quanto o anunciante lucra, e nenhum vira promessa ou projeção pro dono. A escala de um anunciante depende também de capital pra tráfego e do funil inteiro (upsell, margem), que a biblioteca não mostra.

## Acompanhamento (Ação 2)

1. **Frequência:** uma coleta por semana no mínimo; na semana de decisão, a cada 2 ou 3 dias.
2. **Mesma planilha, mais linhas.** `--acrescentar` soma a coleta nova e liga cada anúncio à coleta anterior (`copias_antes`). Views vão na coluna `views` da linha do dia; `--recalcular` compara com a coleta anterior.
3. **Sinal repetido promove.** Candidato vira "vendendo" quando o sinal aparece em 2 coletas ou mais.
4. **Sumiço não rebaixa.** Anúncio que some fica com `sumiu em <data>` na nota; olhe se as variações dele seguem no ar.
5. **O que vale uma frase no topo do Radar:** anúncio novo que já entrou com cópias, candidato que virou vendendo, formato que apareceu em 2 anunciantes diferentes na mesma semana.
6. **Arquivo de referências do dono:** por nicho e por formato (anúncio, VSL, página), com link, print e, quando der, o vídeo baixado, que é material de estudo interno: nunca sobe em anúncio nem sai da pasta do dono.

## Planilha: as colunas

`data_coleta, termo, id, id_grupo, pagina, pagina_id, inicio, dias_no_ar, ativo, copias, copias_antes, paginas_mesmo_texto, versoes_da_pagina, formato, cta, destino, plataformas, texto_inicio, views, views_antes, s1_copias, s2_paginas, s3_versoes, s4_views, s5_tempo, recente, pontos, classe, link_biblioteca, nota`

No caminho manual, preencha pelo menos: `data_coleta`, `pagina`, `inicio`, `dias_no_ar`, `copias`, `versoes_da_pagina`, `views`, os 5 sinais, `pontos`, `classe` e `link_biblioteca`.
