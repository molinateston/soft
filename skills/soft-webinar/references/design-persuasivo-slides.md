# Design persuasivo de slides, a régua de como cada tela é desenhada

> **CONTRATO VIGENTE (manda sobre este arquivo):** a Etapa AULA entrega o roteiro SLIDE A SLIDE (TÍTULO + OBJETIVO + CONTEÚDO). Esta skill não renderiza deck. O que está aqui entra no campo CONTEÚDO como direção de desenho pro renderizador (`soft-designer`, `scripts/deck_gen.py`), uma linha por slide.

Destilado da régua Flatline de desenho de tela pra webinar de alta conversão. O `geracao-de-slides.md` já responde **o que** vai em cada slide (Seção 0 o princípio-mãe, Seção 2 os 18 arquétipos, Seção 5 a regra de ouro, Seção 7 o checklist) e o `tela-granularidade-e-bloco.md` já responde **quanto** cabe numa tela. Aqui está só o que falta: **como** a tela é desenhada pra vender. Dúvida de "quantos slides" continua morando lá.

---

## Regra 1, hierarquia invertida

**A regra:** a informação é a fonte maior da tela e o título fica pequeno num canto, porque o título é a parte que menos carrega crença.

**Por quê:** o olho vai pro elemento maior e decide em menos de um segundo o que a tela significa; quando o maior é o rótulo, esse segundo vai pra uma palavra que não move nada. Nome, tagline, logo e foto ocupam área nobre sem pagar aluguel, porque quem assiste já sabe quem está falando. Número segue a mesma inversão: preço em fonte gigante parece mais caro, e quantidade vira objeto porque objeto se conta com o olho.

**Antes:** "O QUE VOCÊ VAI DESCOBRIR HOJE" em display no topo, logo e foto no rodapé, três bullets em fonte média; e "350 horas de suporte" com o 350 gigante.
**Depois:** o rótulo vira linha pequena num canto, logo e foto somem, o primeiro bullet ocupa metade da tela e os outros entram por clique, empilhando menores. O 350 fica pequeno e a tela mostra 350 relojinhos preenchendo o quadro; em vez de "30 casas", um calendário do mês com uma casinha por dia.

**Arquétipos:** 6, 3, 8 (aqui a regra CORRIGE o arquétipo: o gigante é o objeto ou o dado da fonte, o preço nunca), 17 (o preço é o item pequeno), 2 (capa, único lugar onde tagline sobrevive).

---

## Regra 2, mostrar em vez de contar

**A regra:** print real da tela onde a coisa aconteceu, no lugar de metáfora, ícone, banco de imagem ou imagem gerada.

**Por quê:** o lead calibra o quanto acredita pelo tipo de imagem. Print com data, contador e nome do veículo é verificável e o cérebro registra como fato; a mesma ideia em ícone é decoração, e decoração sinaliza que não havia fato. "70% das empresas já fazem isso" é opinião do apresentador; o print da fonte com a linha grifada é a fonte falando por ele. Banco de imagem entra só quando a coisa real não existe em tela nenhuma. Metáfora visual paga a passagem numa condição: se entrar, fica do começo ao fim, porque metáfora que aparece uma vez vira ruído.

**Antes:** a tendência vira gráfico genérico com seta subindo e a frase "o mercado mudou"; a prova social vira ícone de balão com o elogio digitado por cima.
**Depois:** a tendência vira o print da matéria, com o nome do veículo visível, a linha do dado grifada e a fonte embaixo; a prova social vira o print do post real, com foto, data e contador, recortado sem o resto da interface. Havendo vários, viram colagem de prints limpos e o volume prova sozinho.

**Arquétipos:** 9, 12 (print de sistema oficial vence card editável), 8 (estatística com a fonte grifada), 13 (print da área de membros vence render), 14 (prompt e resultado), 11 (cena de rotina, único lugar com licença de banco de imagem).

---

## Regra 3, a tela vista três vezes

**A regra:** todo slide de ensino aparece três vezes: teaser na agenda, no ensino, e no recap.

**Por quê:** a terceira vista é a que grava. Na agenda o lead vê um pedaço de tela que ainda não entende, e a curiosidade abre um loop que o segura até o ensino; no ensino ele reconhece a tela e entra com atenção preparada; no recap ela já é dele, e conteúdo que o lead sente como próprio é o que ele compra. O detalhe que faz funcionar: na agenda, alguns slides entram cortados na borda. Corte é promessa.

**Antes:** a agenda é uma lista de três bullets ("o método, os erros, o passo a passo") e o recap repete os mesmos três. Nenhuma tela se repete e o lead sai sem imagem mental.
**Depois:** a agenda mostra miniaturas dos próprios slides que virão, slide dentro de slide, duas inteiras e uma cortada na borda. No ensino cada uma abre em tela cheia; no recap as três voltam lado a lado, menores, com a marca de concluído. O lead viu o argumento três vezes sem ouvir a mesma frase três vezes.

**Arquétipos:** 6 (a agenda vira mosaico de telas), 10 e 15 (as telas de ensino que viram teaser), 7 (o presente também aparece cortado), e o recap do Mecanismo.

---

## Regra 4, mecanismo como bússola

**A regra:** o slide do framework volta a cada etapa, com a cumprida riscada e menor, a atual grande, a próxima opaca, e uma cor marcando onde a aula está.

**Por quê:** ensino sem mapa vira lista de coisas soltas, e lista solta não vira método na cabeça de ninguém. A bússola faz três trabalhos de uma vez: mostra que o método tem começo e fim (logo é executável), que ele já avançou (logo vale ficar) e o que falta (logo tem loop aberto). Sem ela o pitch chega como assunto novo; com ela, é o último passo de um caminho que o lead viu andar. Nome de nível só entra quando o desenho é de fato em níveis, porque nomear nível num fluxo confunde mais do que organiza.

**Antes:** o framework aparece uma vez, completo, no começo do Mecanismo, nome do sistema em display com brilho, e some. Cada etapa vira slide independente e ninguém sabe em que ponto do mapa está.
**Depois:** o nome do sistema fica pequeno no canto, sem brilho, setas finas. Na etapa 2, a 1 encolhe com a marca de concluída, a 2 fica grande e recebe a cor de destaque, a 3 e a 4 ficam opacas. A tela volta na virada de cada etapa e o lead lê o próprio progresso sem narração.

**Arquétipos:** 15 (o build desta bússola), 10 (framework/diagrama), 16 (manifesto que fecha cada etapa) e a virada entre fases do arco.

---

## Regra 5, o molde do slide de CTA

**A regra:** stack à esquerda linha a linha, total em fonte maior que o preço, contagem regressiva em destaque, um CTA só, link em faixa na cor de alerta do deck com texto na cor de link, o par de maior contraste da paleta do dono no rodapé.

**Por quê:** é o slide que fica mais tempo na tela e o único em que o lead executa uma ação enquanto olha, e cada elemento tem função de conversão. Stack linha a linha, porque o olho lê de cima pra baixo e acompanha a soma. Total maior que o preço, porque a comparação de tamanho faz metade do trabalho da ancoragem. Contagem regressiva em destaque, porque depois do link é o elemento que mais move: sem relógio visível, a urgência é só uma frase que o apresentador falou. Um CTA só, porque duas ações devolvem o lead pra decisão em vez de empurrar pra execução. Link numa faixa de alerta no rodapé, no par de maior contraste da paleta do dono, porque tem que ser impossível de perder por quem entrou nos últimos dois minutos.

**Antes:** preço em display gigante no centro, total da stack numa linha fina acima, dois botões ("entrar agora" e "falar com a equipe"), link no rodapé em cinza pequeno, escassez só como frase.
**Depois:** metade esquerda com a stack somando linha a linha e o total em corpo grande; o preço embaixo, menor que o total; a contagem regressiva no canto superior direito, andando; um botão só; faixa de alerta atravessando o rodapé com o link na cor de link, do tamanho do total.

**Arquétipos:** 17 (ancoragem/stack/queda) e 18 (escassez, FAQ e CTA). É o slide-mestre que o checklist da Seção 7 manda ficar fixo na tela durante o FAQ.

---

## Regra 6, legibilidade que vende

**A regra:** fonte grande, leitura de cima pra baixo, duas cores, um ponto por slide, movimento a cada seis segundos.

**Por quê:** quem tem dinheiro pra comprar quase sempre passou dos 40 e assiste pelo celular, e texto que exige apertar os olhos é texto que ele pula. Leitura de cima pra baixo é a ordem natural, e o desenho lateral só se justifica em sequência de eventos no tempo. Duas cores bastam: uma serve o deck inteiro, a outra marca só o que importa, porque quando tudo tem cor nada tem destaque. Um ponto por slide, porque slide é de graça e atenção não é. Movimento a cada seis segundos, porque tela parada devolve o lead pro celular. E o ponto que dói em quem gosta de design: tela feia e legível converte mais que tela bonita e pequena, e acabamento caro demais reduz a confiança, porque o lead que não compra design lê o capricho como sinal de que o dinheiro foi pro embrulho.

**Antes:** fundo fotográfico, título em fonte fina clara sobre a foto, quatro cores de marca, três ideias na mesma tela, rótulo vertical na lateral e nada se movendo por 40 segundos de fala.
**Depois:** caixa escura com opacidade por cima da foto pra a fonte viver, texto em corpo grande, duas cores no deck inteiro, uma ideia só na tela, o rótulo lateral vira linha pequena no topo, e a tela troca ou o item entra por clique a cada seis segundos. A exceção é o contexto que se perde: quando dois slides seguidos só fazem sentido juntos (quem diz não vale zero, quem diz sim vale quarenta mil), os dois viram um, porque ali a comparação É o ponto.

**Arquétipos:** todos. Na prática 1 e 16 (a fonte grande é o slide inteiro), 5 (as duas cores fazem o semáforo), 4 e 11 (lateral permitida por ser sequência no tempo) e 13 (a foto pede a caixa escura).

---

## Apêndice, truques de produção

- **Tabela animada pra conta de dinheiro.** A projeção entra célula por célula (5 itens x R$1 x 50 pedidos = R$250 por dia = R$1.750 por semana = R$91.250 por ano). A conta feita na frente do lead vale mais que o resultado pronto.
- **Caixa branca a 80% por cima do slide anterior.** Duplica o slide, joga a caixa quase opaca em cima e escreve a revelação por cima dela. O número velho fica visível por baixo, e a revelação nasce dele em vez de chegar de fora.
- **Emoji como fonte escalável.** Copia, cola e cresce sem perder qualidade, e resolve ilustração de quantidade (pessoas, relógios, casas) sem depender de ícone desenhado.
- **Regra de três nas comparações.** Uma é caso, duas é coincidência, três é padrão. Sempre três colunas (2, 5 e 10 pessoas com os valores correspondentes), nunca duas.
- **Riscado animado pra ancoragem.** O valor antigo aparece inteiro, o risco entra por clique e o novo valor nasce embaixo, na mesma tela.
