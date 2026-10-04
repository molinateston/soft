# O que foi medido (e o que não foi)

Só números medidos. Servem pra decidir se o processo desta versão (dividir, uma ideia por tela, número como imagem, esquema reusado) vale a pena, e pra dizer ao dono o que esperar.

## 1. Os decks na régua do guia

Um avaliador independente (modelo com visão, rubrica por slide, mais um revisor cético por deck que tenta derrubar cada achado) mediu três versões do mesmo roteiro com a régua do guia. Só entram achados que sobreviveram ao cético.

| medida | instalada (molde de texto) | v3 | piloto v4 |
|---|---|---|---|
| slides avaliados | 60 | 18 | 73 |
| uma ideia por slide | 63% | 67% | 85% |
| lida em 3 segundos | 25% | 39% | 84% |
| com imagem ou gráfico | 0% | 100% | 95% |
| palavras por slide (mediana) | 38 | 30 | 12 |
| hierarquia certa (o que decide é o maior) | 17% | 56% | 71% |
| número que virou imagem, entre os que têm número | 0% | 63% | 59% |
| prova visível, entre os que pedem prova | 0% | 0% | 0% |
| itens do deck atendidos, de 10 | 1 | 3 | 2 |

A prova visível é 0 nas três por um motivo só: não havia print real nem foto de cliente pra colar. O piloto deixa a vaga tracejada no lugar; o número só se move quando o print chega.

Depois dessa rodada, o piloto ganhou o produto desenhado como escada, o preço cheio fora do tamanho gigante isolado, os números de dinheiro e de vendas como pictograma de blocos com escala única e o texto maior (menor fonte medida por script entre 32 e 44px nos blocos). Essas mudanças passaram no script do deck, mas não foram julgadas de novo pelo avaliador: os 59% de número como imagem são anteriores a elas.

## 2. O processo em escala

- O roteiro inteiro de 64 slides virou 220 telas em 12 blocos, depois do passo "Dividir" e do desenho slide a slide. Dois slides ficaram fora do deck, um por falta de fonte de mercado e outro por falta de uma cena concreta, e viraram perguntas.
- Um modelo de porte médio (Sonnet) operou o modo agente em 8 blocos: 84 slides novos num primeiro grupo de 4 blocos e 63 num segundo grupo de 4. Todos fecharam APROVADO no script do deck, com a conferência de números contra o roteiro passando e nada inventado. Menor fonte medida: de 32 a 44px. Seis vagas de print, nos slides em que o roteiro afirma resultado sem trazer o print.
- Conferência da divisão: nos três blocos testados com `conferir_fontes.py` contra o roteiro original, nenhum número ficou sem fonte.
- A conferência de números reprova a legenda da escala de blocos, porque ela não existe no roteiro. Com a escala declarada num arquivo de unidade, o mesmo deck fecha APROVADO e mais nada muda.

## 3. Limites, ditos sem enfeite

- **O avaliador mede as regras do guia e deixa a beleza de fora.** Um deck passa em todas as regras e ainda pode não agradar. O veredito visual é do dono.
- **A comparação favorece o piloto.** A instalada é a aula inteira (60 slides); o piloto foram 4 trechos (abertura, história, escada do método com a decisão, oferta). O percentual de trechos escolhidos é mais alto que o de uma aula com todo o ensino. A v3 tem só 18 slides: cada um pesa mais de 5 pontos.
- **O deck da instalada foi gerado por um conversor do roteiro** (corta linhas, joga tabela como itens soltos). Parte do texto cortado pode ser do conversor. O que é estrutural: o molde de texto não tem imagem, gráfico nem animação.
- **Texto pequeno:** a nota dos avaliadores de visão (78%) não é confiável pra medir tamanho. O que vale é a medição por script em 1920x1080: menor fonte de 32 a 44px nos blocos do piloto. Só o piloto foi medido assim.
- **Não medido:** tempo de fala por slide (o PNG não mostra), animação por clique no PowerPoint, página de vendas e checkout (se o deck bate com eles).
- **O PPTX nunca foi aberto no PowerPoint real.** Foi gerado e conferido por script. Abra num PowerPoint antes de apresentar.
- **Nenhum slide de referência de terceiros foi visto.** A régua do guia vem do que se fala sobre os slides; nenhuma imagem deles entrou.
- **Metáforas do designer** (balança, espelho, âncora, engrenagem, mapa e outras) não têm medida: cada uma precisa bater com a fala, e quem confere é o dono.
