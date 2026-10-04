# Classificação de construção: como o anúncio foi montado, cruzada com o sinal de venda

Lida no passo R4b da Ação 1. A régua dos 5 sinais diz **se** o anúncio vende. Esta classificação diz **como ele foi construído**. Sozinha ela não prova venda: um anúncio bem construído pode estar parado, e um mal construído pode vender por oferta, por página ou por audiência. O valor está no cruzamento.

## Quando rodar e em quantos

Nos anúncios das classes `vendendo` e `candidato`, sem os marcados `fora do eixo` ou `descartado`. Até 40 por rodada, por ordem de pontos. Anúncio com o mesmo texto em várias páginas entra **uma vez** (as cópias já pontuaram no sinal). Anúncio sem texto fica de fora e a linha diz `sem texto`.

## O que ler

A planilha guarda só os 160 primeiros caracteres (`texto_inicio`). Isso basta pro gancho e pra especificidade. Pra "mostra resultado" e "prova" leia o texto inteiro no `link_biblioteca`, ou na transcrição quando o anúncio é vídeo (o gancho transcrito da Ação 3 serve). Sem o texto inteiro, essas duas perguntas valem `não visto`, nunca `não`.

## As 4 perguntas, todas de resposta fechada

Responda as quatro de uma vez, por anúncio, sem escrever análise.

1. **Gancho (a primeira frase).** Uma só opção:
   - `pergunta`: abre com pergunta ao espectador.
   - `dor_direta`: aponta um erro, custo ou problema que o espectador tem agora.
   - `promessa`: promete um resultado.
   - `curiosidade`: abre um mistério ou lacuna que só fecha lendo ou vendo.
   - `demonstracao`: abre mostrando algo funcionando.
   - `sem_gancho`: convite, nome de marca, descrição de produto ou condição de preço, sem nada que prenda a primeira frase.
   Na dúvida entre duas, vale a que aparece primeiro no texto. `sem_gancho` é resposta legítima e comum; não force um tipo. Casos de borda: slogan sem resultado nomeado (`a escolha certa`, `eleva qualquer look`) é `sem_gancho`, não `promessa`; descrever o problema do espectador é `dor_direta`, e `demonstracao` pede caso real ou produto em uso aparecendo.
2. **Especificidade do gancho (0 a 2).** 0 = vago, serve pra qualquer negócio. 1 = tem um detalhe concreto. 2 = número, ferramenta ou situação que o comprador reconhece como a dele.
3. **Mostra o resultado funcionando** em vez de só prometer: `sim`, `não` ou `não visto`.
4. **Tem prova concreta** (número, caso real, cliente, antes e depois): `sim`, `não` ou `não visto`.

## Construção forte, média ou fraca

- **Forte:** especificidade 2 e (mostra resultado `sim` ou prova `sim`).
- **Média:** especificidade 1 ou 2, ou mostra resultado `sim`, ou prova `sim`.
- **Fraca:** o resto.
Com 3 ou 4 respostas em `não visto`, a construção sai `incompleta` e o anúncio não entra no cruzamento até a leitura do texto inteiro.

Não some nem pese as quatro respostas numa nota única. Os pesos seriam chute, e a nota esconderia qual pergunta puxou o resultado.

## O cruzamento

| Classe de sinal | Construção | O que significa |
| --- | --- | --- |
| vendendo | forte ou média | A construção é candidata a explicar a venda. **Modele primeiro**, pelo princípio. |
| vendendo | fraca | Vende por outra coisa: oferta, página, audiência ou verba. **Não modele o texto**; vá à engenharia reversa do resto (Ação 3). |
| candidato ou observar | forte | Hipótese sem sinal ainda. Vai pra Em observação com a data da próxima coleta. |
| candidato ou observar | fraca ou média | Sem sinal e sem construção que se destaque. Fora do Radar. |

## Onde gravar

Num arquivo à parte, `construcao-<nicho>.csv`, uma linha por anúncio, ao lado da planilha: `id`, `gancho`, `especificidade`, `mostra_resultado`, `prova`, `texto_visto` (`160` ou `completo`), `construcao`, `cruzamento`. Não acrescente colunas na planilha principal: o recálculo regrava só as colunas que ele conhece e as outras se perdem.

## O que entra no Radar

Na seção 4 (o padrão que se repete): a contagem dos tipos de gancho entre os anúncios `vendendo`, a especificidade mais comum e quantos têm resultado e prova. Padrão só vale com 2 anunciantes ou mais; um anúncio sozinho é exemplo, não padrão. Na seção 3, a linha do porquê passa a citar a pergunta que sustenta (`gancho de dor direta com número`), nunca o texto dele.

## Limites a declarar

- A biblioteca mostra anúncio, não resultado: construção forte é padrão de montagem, não prova de venda.
- Com só 160 caracteres, prova e resultado ficam `não visto` e a construção tende a sair `média` ou `incompleta`. Diga isso no Radar.
- A rubrica mede o texto. Imagem, voz e edição do vídeo ficam fora dela.
- Não copie a frase do concorrente. Leve a estrutura (o tipo de gancho e o grau de especificidade) pro anúncio do dono, com as palavras e os números dele.
