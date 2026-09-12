# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, números, posições e resultados foram inventados só pra mostrar
> a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega de
> verdade. Num trabalho real, todo número nasce com a fonte escrita ao lado, e o que não foi medido
> aparece como não medido.

**O caso fictício:** uma escola de marcenaria que dá cursos presenciais de fim de semana numa cidade
média, e vende também um curso longo de 6 meses. O site tem 14 páginas: a inicial, uma por curso, e
oito textos publicados entre dois e três anos atrás. Ninguém nunca mexeu em SEO. O dono fictício acha
que o problema é o site ser antigo.

Este arquivo mostra a saída resumida de cada ação, na ordem. A saída real é maior; aqui está só o
suficiente pra você reconhecer o formato antes de começar.

---

## O que o dono deu de entrada

> "Meu site existe há quatro anos e não traz aluno nenhum. Só entra gente que já me conhece do
> Instagram. Quando eu procuro 'curso de marcenaria' aparece um monte de gente de outra cidade e eu
> não apareço em lugar nenhum."

**O que faltava:** a região não estava declarada em nenhuma página do site, não havia palavra alvo
definida pra página nenhuma, e o dono nunca tinha aberto o painel do buscador para donos de site.

## As perguntas que a skill fez (uma por vez)

1. "Qual o endereço do site?" → *"[endereço fictício]"*
2. "O que você vende e pra quem?" → *"Curso de marcenaria de fim de semana pra quem trabalha em outra coisa e quer aprender por hobby, e um curso longo de 6 meses pra quem quer viver disso."*
3. "Você atende uma região específica ou o país inteiro?" → *"Só presencial, na minha cidade e nas duas vizinhas."*
4. "Quais três concorrentes aparecem quando você procura o que vende?" → *"Duas escolas de outra cidade e um canal de vídeo. Aqui perto não tem ninguém."*

**Premissa declarada em 1 linha:** o problema principal não é a idade do site, é que nenhuma página diz
em que cidade a escola fica, então o buscador nunca associou o site a busca local, e busca local é
exatamente onde a concorrência é quase zero.

**Sobre dados:** o ambiente não tinha ferramenta de SEO conectada nem acesso à web nesta sessão. A
demanda saiu classificada em alta, média e baixa por julgamento declarado, tudo marcado
`[A CONFIRMAR: volume]`, e a primeira tarefa do plano é o dono ligar o painel gratuito do buscador.

---

## Ação 1 · PALAVRAS

Saída real: `seo-palavras.md`. Resumo (7 das 18 linhas):

| Termo | Dificuldade | Oportunidade | Posição atual | Intenção | Tipo de página |
|---|---|---|---|---|---|
| curso de marcenaria em [cidade] | fácil `[A CONFIRMAR]` | **alta** | não medida | transacional | página de curso |
| aula de marcenaria fim de semana [cidade] | fácil | **alta** | não medida | transacional | página de curso |
| curso de marcenaria | difícil | baixa | não medida | comercial | não atacar agora |
| como começar na marcenaria sem oficina | fácil | **alta** | não medida | informacional | artigo |
| que ferramenta comprar pra começar marcenaria | fácil | **alta** | não medida | comercial | guia com lista |
| quanto custa montar uma marcenaria pequena | moderada | média | não medida | comercial | guia com calculadora |
| vale a pena viver de marcenaria | fácil | média | não medida | informacional | artigo |

**A conclusão da ação, em 1 frase:** as duas primeiras linhas valem mais que as outras dezesseis
juntas, porque ninguém disputa busca local naquela cidade e são elas que trazem quem paga.

**STOP.** A skill mostrou a tabela e perguntou "sigo pra auditoria das páginas?".

---

## Ação 2 · PÁGINA POR PÁGINA

Saída real: `seo-paginas.md`. Resumo (6 das 23 linhas):

| Página | Erro | Gravidade | Conserto |
|---|---|---|---|
| inicial | título da aba é "Início" | **alto** | trocar por: "Escola de marcenaria em [cidade] · cursos de fim de semana" |
| inicial | a cidade não aparece em lugar nenhum da página | **crítico** | escrever a cidade no título principal, no primeiro parágrafo e no rodapé com o endereço completo |
| curso de fim de semana | três títulos principais na mesma página | alto | deixar um só, os outros dois viram subtítulo de segundo nível |
| curso de 6 meses | sem descrição de resultado de busca | médio | escrever 155 caracteres com o que a pessoa aprende e o convite |
| 8 textos do blog | nenhum link interno apontando pras páginas de curso | alto | cada texto ganha um link no meio, com texto clicável descritivo |
| todas as imagens | texto alternativo vazio em 31 imagens | baixo (busca) / alto (acessibilidade) | descrever o que cada foto mostra |

**O erro crítico, em 1 frase:** um site de escola presencial que não escreve a própria cidade em lugar
nenhum está pedindo pro buscador não mostrá-lo em busca local.

---

## Ação 3 · BURACOS DE CONTEÚDO

Saída real: `seo-conteudo.md`. Resumo (5 linhas):

| Tema | Por que importa | Formato | Prioridade | Esforço |
|---|---|---|---|---|
| Que ferramenta comprar pra começar | busca de quem está decidindo entrar, e leva direto ao curso | guia com lista e faixa de preço | **alta** | meio dia |
| Como começar sem ter oficina | a objeção número um de quem mora em apartamento | artigo | **alta** | meio dia |
| Os 8 textos velhos, atualizados | já existem e já têm histórico; atualizar rende mais rápido que publicar novo | atualização | **alta** | rápido, um por semana |
| Quanto custa montar uma marcenaria pequena | busca de quem pensa em viver disso, alimenta o curso longo | guia com calculadora simples | média | obra |
| Página central "marcenaria pra iniciante" | existem 5 textos soltos do mesmo assunto e nada amarrando | página central com links | média | obra |

---

## Ação 4 · TÉCNICA

Saída real: `seo-tecnico.md`. Resumo (7 das 8 linhas):

| Checagem | Situação | Detalhe | Conserto |
|---|---|---|---|
| Velocidade | **falhou** | 14 fotos de oficina em tamanho original na página inicial | comprimir e redimensionar; a inicial cai de 8 MB para menos de 1 MB |
| Celular | atenção | o menu cobre o conteúdo em tela pequena | ajustar a folha de estilo responsiva |
| Dados estruturados | **falhou** | nenhuma marcação; faltam organização, curso e trilha de navegação | adicionar as três e validar antes de publicar |
| Rastreamento | passou | o arquivo do robô não bloqueia nada indevido | mapa do site não existe: criar e enviar pelo painel |
| Links quebrados | atenção | 3 links internos apontam pra páginas apagadas em 2024 | corrigir o destino |
| Conexão segura | passou | site inteiro em conexão segura, sem conteúdo misto | nada a fazer |
| Indexação | `[A CONFIRMAR: não verificado]` | sem acesso ao painel do buscador nesta sessão | o dono liga o painel e a checagem volta na próxima rodada |

---

## Ação 5 · CONCORRENTE

Saída real: `seo-concorrente.md`. Resumo:

| Dimensão | O site do dono | Concorrente A | Concorrente B | Quem está melhor |
|---|---|---|---|---|
| Termos ranqueados | não medido | ~180 `[A CONFIRMAR]` | ~40 `[A CONFIRMAR]` | A |
| Profundidade de conteúdo | 8 textos, curtos | 60 textos, longos | 12 textos, médios | A |
| Frequência de publicação | zero há 2 anos | semanal | mensal | A |
| Sinais de link | poucos | muitos, de imprensa local | poucos | A |
| Situação técnica | lenta, sem marcação | rápida, com marcação | média | A |
| Espaços destacados | nenhum | resposta destacada em 4 termos | nenhum | A |
| **Busca local naquela cidade** | ausente | não atende a região | não atende a região | **ninguém** |

**As três conclusões:**

1. **O que explica a diferença hoje:** o concorrente A publica há dois anos e o site do dono está
   parado, mas isso é o segundo problema. O primeiro é que o site não declara a cidade, e por isso
   perde a única disputa que ele ganharia sem esforço.
2. **O que dá pra alcançar neste trimestre:** as duas buscas locais, porque nenhum dos concorrentes
   atende a região e o campo está vazio.
3. **O que não dá pra alcançar agora:** o termo geral e disputado. A entrada por ali é cauda longa e
   busca com pergunta, e leva mais de um trimestre.

---

## O plano final

Saída real: `seo-plano.md`.

### Resumo executivo

O site tem um bom acervo de textos e um domínio de quatro anos, e essa é a maior força. O problema não
é idade: nenhuma página declara a cidade, então a escola nunca disputou a única busca em que não tem
concorrente. As três prioridades de maior efeito são escrever a cidade nas páginas de curso, ligar o
painel gratuito do buscador pra parar de trabalhar às cegas, e comprimir as imagens da página inicial.
Veredito: base sólida, execução parada.

### Conserto rápido (esta semana)

| O que fazer | Efeito | Esforço |
|---|---|---|
| Escrever a cidade no título principal, no primeiro parágrafo e no rodapé das 3 páginas de curso | **alto** | 1 hora |
| Trocar o título da aba das 14 páginas por títulos únicos com a palavra alvo | **alto** | 2 horas |
| Comprimir as 14 fotos da página inicial | **alto** | 1 hora |
| Ligar o painel do buscador para donos de site e enviar o mapa do site | **alto** | 30 minutos |
| Corrigir os 3 links internos quebrados | médio | 20 minutos |
| Deixar um único título principal na página do curso de fim de semana | médio | 15 minutos |
| Escrever a descrição de resultado de busca das 3 páginas de curso | médio | 40 minutos |

### Obra do trimestre

| O que fazer | Efeito | Esforço | Dependência |
|---|---|---|---|
| Atualizar os 8 textos velhos, um por semana | **alto** | 8 semanas | nenhuma |
| Publicar o guia de ferramentas pra iniciante | **alto** | meio dia | nenhuma |
| Publicar o artigo de como começar sem oficina | **alto** | meio dia | nenhuma |
| Adicionar dados estruturados de organização, curso e trilha | médio | 1 dia | ajuda de quem mexe no código |
| Montar a página central de marcenaria pra iniciante | médio | 2 dias | depende dos 8 textos atualizados |
| Calculadora de custo de oficina pequena | médio | obra | ajuda de quem mexe no código |

---

## O que o gate reprovou no caminho (e por quê)

| Seção | O que estava escrito | Por que reprovou | Como ficou |
|---|---|---|---|
| Ação 1 | "volume: 2.400 buscas por mês" | número sem fonte, e nada foi medido | virou "demanda alta `[A CONFIRMAR: volume]`" mais a tarefa de ligar o painel |
| Ação 2 | "otimizar o título da página inicial" | conserto não executável | virou o texto novo do título, escrito por inteiro |
| Ação 4 | "indexação: passou" | não foi verificado, e passou por presunção | virou `[A CONFIRMAR: não verificado]` com o caminho pra medir |
| Ação 5 | promessa de que o plano ia revolucionar a busca da escola | verbo de transformação genérico (check 4) | virou "as duas buscas locais estão vazias e dá pra ocupá-las neste trimestre" |
| Plano | conserto rápido e obra na mesma lista | plano sem as duas colunas | separado, e o esforço escrito em cada linha |
