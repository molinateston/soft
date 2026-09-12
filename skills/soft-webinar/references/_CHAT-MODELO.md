# MODELO FINAL, Chat Simulado do Webinar (base da Etapa 6 · CHAT desta skill)

> Esta é a especificação da skill que **substitui** a parte de chat de versões antigas. Foi destilada do modelo final REAL já produzido pro perpétuo do caso estudado, não de teoria.
>
> **Fontes do modelo (lidas pra montar este spec):**
> - A planilha de PLANEJAMENTO final do caso estudado (388 linhas, 7 colunas, com tipo+gatilho), o EXPORT final EverWebinar (4 colunas `username,message,minutes,seconds`) e o estado intermediário em JSON (prefixo `WAIT:` = sala de espera). Os arquivos vivem no modelo do dono via config, fora deste bundle.
> - `references/simulador-comentarios-ao-vivo.md (bundlada nesta skill)`, a doutrina (curva, honestidade, consistência, Crivo).
> - `references/interacao-chat-ao-vivo.md (bundlada nesta skill)`, a engenharia de interação do host (premissa AO VIVO; o que presta pra moderação).
> - O formato canônico de chat em massa confirmado no caso estudado (modelo do dono via config).

---

## Índice

- A REGRA-MÃE (a frase que governa tudo)
- 1. O FORMATO
- 2. O TEMPO: vídeo vs roteiro + a sala de espera
- 3. O RITMO E A DENSIDADE (quantos comentários, e onde)
- 4. OS TIPOS DE MENSAGEM (a taxonomia)
- 5. CONSISTÊNCIA COM O ROTEIRO (bidirecional)
- 6. REALISMO (anti-robótico): personas derivadas do avatar, rodízio proibido, coerência username e texto
- 7. AO VIVO × PERPÉTUO (a bifurcação-mãe da skill)
- 8. CHECKLIST FINAL (antes de subir e entregar)
- 9. ANTI-PADRÕES (o que quebra a simulação)
- 10. GATE DE SAÍDA (o Crivo), bloqueante
- O QUE MORRE das versões antigas de chat

---

## A REGRA-MÃE (a frase que governa tudo)

**Simula-se a SALA, nunca a PROVA.**

Um comentário simulado pode reproduzir a *conversa* de uma sala viva (chegada, dúvida, reação, "eu quero", "comprei agora"). NUNCA pode inventar a *prova do produto*, nada de "fiz o método e ganhei R$X", "perdi 18kg", número de vaga falso, preço/garantia/bônus que o host ainda não abriu. Resultado e número vêm do banco REAL do player ou não vêm.

| O que é REAL e nunca se simula | O que a simulação REPRODUZ |
|---|---|
| Vagas/lugares da sessão (escassez por sessão) | A energia típica de uma sala daquele tamanho |
| Contador de presença na faixa honesta | O movimento do chat: chegada, dúvida, "EU QUERO", compra |
| Resultados/depoimentos de clientes (reais) | A naturalidade de quem comenta (nomes, cidades, timing humano) |
| Preço, oferta, garantia, bônus | O FOMO e o social proof de uma sala convertendo |

---

## 1. O FORMATO

### 1.1 Formato canônico de IMPORT (EverWebinar / WebinarKit), o que SOBE na plataforma

São **4 colunas APENAS**, com header, ordenadas por `(minutes, seconds)` crescente:

```
username,message,minutes,seconds
Thiago R.,vamo ver no q da,1,9
Marcos,to ansioso pra essa,1,18
Ricardo M.,oi gente,1,47
```

| Coluna | O que é |
|---|---|
| **username** | quem comenta. Primeiro nome BR (ou nome + sobrenome curto: "Thiago R.", "Camila Souza"). A origem ("de SP") vai aqui ("Camila SP") OU embutida na `message`, e só quando o host pede de onde a pessoa é (senão polui). |
| **message** | a fala, em voz de participante BR (torta, abreviada, gíria leve). |
| **minutes** | o minuto **do vídeo** em que a mensagem dispara (ver §2 sobre tempo do vídeo vs tempo do roteiro). |
| **seconds** | o segundo (0-59) dentro daquele minuto. |

**Regras inegociáveis do formato:**
- Só essas 4 colunas. **NÃO existe** coluna de cidade nem de tipo no arquivo de import.
- Timestamp = **minuto + segundo do VÍDEO**, em duas colunas separadas (nunca um campo só, nunca `mm:ss`).
- Disparos **escalonados**: nunca dois comentários no mesmo `(minutes,seconds)`. Espalhe alguns segundos (sala real não fala em uníssono).
- **Sempre pedir/confirmar o modelo da plataforma do player ANTES de gerar.** Plataformas/contas diferentes têm colunas diferentes; gerar no formato errado obriga remapeamento manual. `username,message,minutes,seconds` é o default do corpus estudado, usado só quando não há outro modelo declarado.

### 1.2 Formato de PLANEJAMENTO (interno da skill), NÃO sobe na plataforma

A skill planeja numa tabela rica de 7 colunas e só EXPORTA as 4 do §1.1. O planejamento é o que permite auditar a curva, casar ecos e bater consistência. Formato real do modelo do corpus estudado:

```
Tempo no vídeo,Tempo no roteiro,Nome,Nicho/Cidade,Comentário,Tipo,Gatilho
05:06,00:06,Patricia Nunes,arquiteta · Florianopolis,oi pessoal,entrada,[HOST] dando boas-vindas
05:24,00:24,Camila Souza,nutri · SP,"Camila aqui de SP, ouvindo direitinho",apresentacao,[HOST] pediu nome/cidade nos comentarios
```

- **Tempo no vídeo** → vira `minutes,seconds` no export.
- **Tempo no roteiro** → o minuto no SCRIPT (pré-sala de espera). Serve só pra casar com o roteiro/deck. Ver §2.
- **Nome** → vira `username`.
- **Nicho/Cidade** → contexto interno (perfil do avatar daquele comentarista). Só entra no export se o host pede origem, e aí vai dentro de `username`/`message`.
- **Comentário** → vira `message`.
- **Tipo / Gatilho** → **planejamento puro, nunca sobe.** O Tipo monta a curva; o Gatilho registra a QUE fala/comando do host o comentário responde (rastro de consistência).

> Estado intermediário observado nos JSON: a sala de espera é marcada com prefixo `WAIT:` no timestamp (ex.: `"ts": "WAIT:04:42"`). É um rótulo interno pra separar pré-roll do corpo da aula; some no export, vira tempo de vídeo normal.

---

## 2. O TEMPO: vídeo vs roteiro + a sala de espera (a mecânica que ninguém erra de boca)

O perpétuo tem DUAS linhas de tempo, e o export usa a do VÍDEO:

- **Tempo no roteiro** = o relógio do script gravado (o "oi" do host é 00:00 do roteiro).
- **Tempo no vídeo** = o relógio do arquivo que a plataforma toca. Inclui a **sala de espera / pré-roll** que roda ANTES do host começar a falar.
- No modelo do corpus estudado a sala de espera é de **~5 min**: roteiro `00:06` = vídeo `05:06`. Fórmula: **`vídeo = roteiro + offset da sala de espera`**.
- **Caso resolvido, com os números escritos (copie a forma).** Aula de **60 minutos**, oferta no **minuto 42**, sala de espera de **5 minutos**. Minuto do dono é do **roteiro** por padrão, a não ser que ele diga "no vídeo" com todas as letras. Então: link no vídeo em `42:00 + 05:00 = 47:00`; preço, parcela, garantia e bônus só depois de `47:00`; teto no vídeo em `60:00 + 05:00 = 65:00`, e o último comentário do CSV cai antes disso. Se em vez disso o dono declarar os 60 minutos como **duração do arquivo de vídeo**, a conta inverte e sai escrita assim: o roteiro termina em `55:00`, a oferta do minuto 42 do vídeo já é tempo de vídeo (link em `42:00`, sem somar de novo) e o teto é `60:00`. **Link e teto saem sempre do mesmo lado da conta**, e o lado escolhido vai declarado em 1 linha no planejamento.

Consequências operacionais:
- Comentários de chegada (`entrada`) acontecem DURANTE a sala de espera, no modelo do corpus estudado, do vídeo `00:34` até `~05:00`, ANTES de o host abrir a aula. É o que faz a sala já parecer cheia quando o vídeo "começa".
- O export usa o **tempo do vídeo**. Se a skill planeja no tempo do roteiro, soma o offset da sala de espera antes de exportar.
- **Sempre confirmar com o player a duração da sala de espera** (pode não ser 5 min). Sem isso, todo eco/comando sai dessincronizado do que aparece na tela.

---

## 3. O RITMO E A DENSIDADE (quantos comentários, e onde)

Régua a partir de **N = pessoas-alvo "ao vivo"** (coerente com o contador de presença honesto; nunca maior):

- **~10-15% da sala comenta**, cada uma 2-4 vezes (a escada de micro-compromissos faz o mesmo dedo voltar ao chat). N=200 → ~20-30 ativos × ~3 = **~60-90 comentários** numa aula de 60-90 min. O modelo final do corpus estudado tem ~387 linhas pra um perpétuo de ~2h20 com sala de espera, denso, mas o player calibra por N.
- **Régua de bolso:** ~1 comentário/minuto de MÉDIA, mas a média mente, a distribuição é em ondas.
- **Teto de poluição:** não estourar ~150-200 mensagens visíveis; acima disso ninguém presta atenção na aula, só no chat.
- **No meio do ensino puro a densidade CAI** (vale obrigatório): comentário demais durante a explicação rouba a atenção do conteúdo.

### A curva (onde concentrar)

```
densidade
 ALTA  │              ▂▂                                    ████ ← LINK NO AR / CARRINHO
       │   ▆▆        ▆██▆           ▅▅                      ████   + FECHAMENTO
 MÉDIA │  ▆██▆      ▆████▆   ▃▃    ▆██▆    ▃▃               ████
 BAIXA │▆██████▆▁▁▆████████▆████▆▆██████▆▆████▆▁▁▆████▆▁▁▆██████▆
       └────────────────────────────────────────────────────────
        SALA DE   "EU      PROVAS/  TRANSIÇÃO  A CONTA  Q&A/    LINK +
        ESPERA    QUERO"   VIRADAS  PRO PITCH  (números) OBJ.   CARRINHO
        + ABERTURA (1ª)                                          (PICO)
                          ↑baixo no meio do ensino puro↑
```

**Os picos, na ordem:**
1. **SALA DE ESPERA + ABERTURA (warm-up):** chegada + confirmação de áudio/vídeo + nome/cidade quando o host pede. Estabelece "a sala está cheia e viva" antes mesmo de a aula começar.
2. **COMANDOS do host** ("digita EU QUERO", "comenta SIM", "estão curtindo?"): cada comando dispara uma rajada concentrada.
3. **A CONTA / números** (no webinar do corpus estudado): quando o host faz a conta (ex.: "1000 inscritos / 25 compram / 37 mil"), vem onda de reação numérica ("a conta fecha sim", "37 mil com 1000 inscrito? caramba").
4. **LINK NO AR / CARRINHO (o MÁXIMO):** quando o host libera o link, dispara o flood de compra. É onde a sala trabalha mais duro.
5. **FECHAMENTO (urgência real):** "corre que tá acabando", "entrei nos 15 primeiros", despedidas de quem comprou.

---

## 4. OS TIPOS DE MENSAGEM (com a taxonomia REAL do modelo do corpus estudado)

Tipos extraídos do `chat-simulado-webinar.csv` (coluna `Tipo`), em ordem da curva. Cada um responde a um gatilho do roteiro:

| Tipo | Onde mora | Função | Exemplos REAIS do modelo |
|---|---|---|---|
| **entrada** | sala de espera | encher a sala antes da aula; chegada com saudação NEUTRA | "oi gente", "cheguei!", "presente", "primeira vez aqui, vim curioso", "salve salve" |
| **engajamento** | abertura + transversal | confirmar áudio/vídeo; reagir aos comandos | "to ouvindo sim [HOST]", "som perfeito aqui", "imagem otima daqui" |
| **apresentacao** | abertura (host pede nome/cidade) | nome + cidade + dor leve | "Camila aqui de SP, ouvindo direitinho", "Aline, Fortaleza! tudo certo por aqui" |
| **dor** | diagnóstico | identificação com o problema (sem antecipar solução) | "agenda cheia e conta vazia", "a imprevisibilidade me matou", "posto todo dia e nao converte" |
| **reação** | conteúdo/viradas (esparso) | concordância, "isso sou eu" | "nossa isso faz muito sentido", "to anotando tudo", "nunca tinha visto desse angulo" |
| **sim-eu-quero** | fim do mecanismo (comando do host) | rajada de micro-compromisso, curta e repetitiva | "EU QUERO", "quero sim", "to dentro", "eu quero demais" |
| **numero** | quando o host faz "a conta" | reage aos números da projeção | "a conta fecha sim", "37 mil com 1000 inscrito? caramba", "da pra justificar 15 mil tranquilo" |
| **duvida** | Q&A / perto do link | pergunta operacional (pagamento, acesso, garantia) | "tem pix?", "parcela em 12x mesmo?", "o acesso é vitalicio?", "aceita 2 cartoes?" |
| **pergunta** | conteúdo + FOMO de vaga | dúvida de conteúdo ou de vaga | "preciso ter audiencia pra comecar?", "ainda tem vaga dos 15?" |
| **objecao** | antes do pitch | o ceticismo que a sala tem (a ser neutralizado pela própria sala) | "ta, mas o perpetuo nao satura o pixel?", "achei meio puxado o valor" |
| **atrito** | reta final | o indeciso amolecendo (não fecha ainda) | "garantia parruda, mas vou analisar com calma", "quase me convenceu, to no limite do sim" |
| **anticipacao** | pré-link | já com o cartão na mão esperando o link | "ja to com o cartao na mao esperando o link", "cade o link [HOST], to pronto" |
| **compra** | LINK NO AR (pico) | social proof de compra, o flood | "comprei agora", "fechei", "acabei de garantir o meu", "to dentro!", "feito. paguei" |
| **hate** | longe do clímax (1-2 na aula) | o cético neutralizado pela sala/lógica | "na pratica nao funciona nao" → resolvido por outro participante |
| **prova-real** | junto das provas (SÓ se real) | validação ancorada em case verídico do player | (do banco real, ver regra de honestidade) |
| **despedida** | fechamento | quem já comprou se despedindo | "te vejo do outro lado", "melhor decisao, to dentro", "valeu [HOST]" |

### Padrões de execução por tipo (o que faz cada um funcionar)

- **Saudação SEMPRE neutra (PROIBIDO hora do dia).** Nada de "bom dia/boa tarde/boa noite". O perpétuo roda o mesmo vídeo em vários horários; quem assiste às 21h vendo "boa tarde" percebe na hora que é gravado. Use: "oi gente", "cheguei", "opa", "presente", "primeira vez aqui".
- **A objeção SURGE e se RESOLVE** (movimento mais importante do carrinho): a dúvida aparece no chat e, 1-3 min depois, OUTRO participante (ou o eco do host) a derruba. A sala se autorregula; o host nunca briga. Pares reais do modelo: erro no cartão → "era só trocar pra crédito"; "achei puxado o valor" → "puxado é continuar no problema mais um ano, eu fechei".
- **Haters: no máximo 1-2 na aula inteira**, sempre resolvidos em 1-3 min, NUNCA perto do clímax de compra, neutralizados pela comunidade/lógica e não pelo host brigando.
- **Compra só DEPOIS de o link aparecer.** Antes do link só existe `anticipacao` ("to com o cartão na mão"). O primeiro `compra` é casado com a fala do host "valendo, to liberando o link". No modelo, o flood de compra começa em `2:25:46` (vídeo), exatamente quando o host libera.
- **FOMO pós-link** alimenta a escassez REAL (no caso do corpus estudado, os "15 primeiros" e a garantia 90+90), nunca inventa vaga.

---

## 5. CONSISTÊNCIA COM O ROTEIRO (a parte crítica, bidirecional)

O pior buraco possível: o host gravado **ECOA** um comentário que não existe ("muito legal, a Camila do Rio") e nenhuma Camila do Rio apareceu antes. Denuncia o gravado na hora.

1. **Todo ECO do host tem respaldo ANTES.** Pra cada "[nome] de [cidade]", "o [nome] perguntou [X]", "vários colocaram [Z]" no roteiro, tem que existir um comentário agendado com tempo de vídeo ANTERIOR ao eco, com nome/cidade/conteúdo exatos. Se não existe, a skill CRIA e posiciona alguns segundos/minutos antes. (Eco genérico "vários colocaram EU QUERO" é respaldado pela RAJADA, não por um nome.)
2. **Todo COMANDO do host tem rajada depois.** "comente nome e cidade" → onda de `apresentacao`; "digita EU QUERO" → rajada `sim-eu-quero`; "estão curtindo?" → onda de `reação`; "quem já se inscreveu coloca aqui" → onda de `compra`. Comando sem resposta é tão denunciador quanto eco órfão.

   **Sem roteiro na mão, a rajada não some: ela segue a espinha padrão.** Quando o player não entregou o roteiro (caso previsto na própria Etapa 6), você NÃO conclui "sem roteiro não há comando, logo não planto rajada". Você assume a espinha padrão de comandos abaixo, planta a rajada de cada um e **declara na auditoria qual comando foi assumido**, com o timestamp em que você o colocou:

   | Momento (tempo de vídeo) | Comando assumido do host | Rajada que você planta |
   |---|---|---|
   | logo após a abertura | "comenta seu nome e sua cidade" | onda de `apresentacao`, 6 a 10 linhas |
   | fim do bloco de diagnóstico | "faz sentido pra você? comenta SIM" | onda de `reação`, 4 a 8 linhas |
   | estreia do mecanismo | "quem quer o passo a passo digita EU QUERO" | rajada `sim-eu-quero`, 8 a 15 linhas |
   | **transição para o pitch** | "vou liberar o link agora, quem quiser entrar comenta EU QUERO" | a rajada MAIOR da aula, `sim-eu-quero` mais `anticipacao` |
   | link no ar | "quem já se inscreveu coloca aqui" | onda de `compra`, escalonada |
   | fechamento | "últimas vagas, quem entrou avisa" | `compra` mais `fomo` |

   A transição para o pitch é a única obrigatória: **planilha em modo sem roteiro que não tem rajada na transição para o pitch reprova.** Na auditoria, escreva: `Modo sem roteiro. Comandos assumidos: <lista com o timestamp de cada um>.`
3. **Nenhum comentário CONTRADIZ nem ANTECIPA o roteiro.** Reprovar/reescrever qualquer fala que cite preço/oferta/bônus antes de o host abrir, reaja a slide que não passou, ou discorde de um fato do roteiro. Cada comentário é reação ao que JÁ passou no vídeo naquele timestamp.
4. **Output de auditoria** (entregue junto da planilha): ecos sem respaldo encontrados + comentários criados pra fechá-los + comandos sem rajada + comentários reprovados por contradizer/antecipar (com motivo).

---

## 6. REALISMO (anti-robótico)

- **Elenco simulado nunca toca a prova real do dono (regra dura).** Nenhum nome, idade, cidade, profissão ou caso do chat simulado pode coincidir com pessoa citada na prova do dono (depoimento, print, estudo de caso, aluno nomeado no roteiro). Coincidência parcial também conta: "Marcia S., 52" ao lado de uma Márcia de 52 na prova é a mesma pessoa aos olhos de quem assiste, e transforma sala simulada em depoimento falso. **Checagem verificável antes de entregar:** liste os nomes citados na prova do dono e no roteiro, liste os nomes do elenco simulado, e escreva `Nomes da prova: <lista> · nomes do elenco: <lista> · coincidências (nome, primeiro nome, ou nome mais idade): 0`. Qualquer coincidência acima de zero, troque o nome do elenco, nunca o da prova.

  **A lista de nomes proibidos não se lembra: ela se extrai, com o comando do consentimento, e a saída vai colada.** Rode o passo 1 sobre TODOS os insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono), não só sobre o campo de prova: o risco não é citar a aluna do caso, é sortear pro elenco o primeiro nome de uma lead que está negociando e que vai assistir à aula. Cole `nomes nos insumos privados: <lista> (N)`. Depois rode o passo 2 sobre o CSV entregue, com um grep por nome, e cole a saída literal, inclusive vazia: `grep -nwF -f <lista> 06-chat-simulado.csv`. **Qualquer linha devolvida reprova a planilha e o nome é trocado antes da entrega**, valendo para o primeiro nome sozinho. Feche com `nomes nos insumos privados: N · colisões no elenco: 0`, e a segunda contagem só pode ser declarada depois da saída do grep colada. Uma lista de 3 nomes escrita de cabeça num perfil que tem 9 é o modo típico de falhar aqui, e ela passa despercebida porque os 3 lembrados costumam ser os certos.
- **Nomes BR variados:** alternar regiões e gerações; não repetir o mesmo nome em comentários próximos no tempo. Pool do modelo: Camila, Rafael, Patrícia, Marcos, Letícia, Vinícius, Fernanda, Tiago, Aline, Rodrigo, Vanessa, Diego, Larissa, Anderson, Gabriela, Wesley, Sandra, Eduardo, Felipe, Carlos.
- **Cidades espalhadas pelo país** (não só capitais do Sudeste): Manaus, Recife, Goiânia, Porto Alegre, Belém, Florianópolis, Fortaleza, Salvador, Curitiba, Maringá, Natal, Londrina, Uberlândia.
- **Os perfis das personas saem do AVATAR do dono, nunca desta página.** Antes de nomear qualquer persona, escreva o avatar em uma linha (faixa etária, gênero predominante, dor de entrada) e derive dela os nomes, as cidades e os perfis. O que dá textura é a variação DENTRO do avatar (algumas iniciantes, algumas céticas, algumas já clientes, dores de entrada diferentes), nunca a variação de profissão pescada de uma lista pronta. **Se você está copiando perfis de um exemplo, você errou.** Os perfis do corpus estudado ficam em `exemplos-por-bloco/`, como estudo do formato, nunca como lista de escolha.
  **Checagem contada, colada na auditoria antes de exportar:** `avatar declarado: <uma linha> · nomes coerentes com o gênero predominante do avatar: N de N · perfis derivados do avatar: N de N · perfis vindos de lista de exemplo: 0.` Qualquer divergência sem justificativa escrita reprova. Sala majoritariamente masculina num webinar cujo avatar é feminino, ou perfis de profissão que não têm relação com a dor de entrada do avatar, reprovam a planilha inteira.
- **Timing escalonado:** numa rajada, intervalos irregulares (3s, 7s, 4s, 11s…). Sala real digita em velocidades diferentes.
- **Rodízio determinístico é proibido, e a proibição é contável.** Sala real não é lista circular. Duas regras que você mede no CSV antes de entregar:
  1. **Nenhum participante fala em intervalo fixo.** Pra cada nome com 3 ou mais comentários, calcule os intervalos entre falas consecutivas; se dois intervalos seguidos do mesmo nome forem iguais, ou variarem menos de 15%, refaça o posicionamento. Ninguém volta ao chat de minuto em minuto cravado.
  2. **A ordem dos nomes não se repete como ciclo.** Nenhuma sequência de 3 nomes consecutivos aparece duas vezes na mesma ordem no arquivo inteiro.
  Além disso, dê a cada persona uma **ficha de digitação** própria (velocidade, tamanho típico de mensagem, se usa emoji, se abrevia, se erra acento) e mantenha a ficha coerente do começo ao fim: quem escreve "vc" no minuto 8 não escreve "você" no minuto 70. Salve as fichas junto da planilha, num arquivo `personas-digitacao.csv` com as colunas `nome,cidade,perfil,velocidade,tamanho_tipico,emoji,abrevia,erra_acento`.
  **Checagem escrita na auditoria:** `Nomes com 3+ falas: N (mínimo 8, e piso de 20% do elenco) · nomes com intervalo fixo: 0 · sequências de 3 nomes repetidas: 0 · fichas de digitação: <N linhas em personas-digitacao.csv>.` Qualquer número diferente de zero nos dois do meio reprova, **e `Nomes com 3+ falas` abaixo do mínimo reprova igualmente**: sala sem reincidência não tem escada de micro-compromissos, que é o mecanismo central do formato. Uma pessoa que volta ao chat pela terceira vez já se comprometeu em público três vezes e chega no pitch preparada pra decidir; 46 estranhos que dizem no máximo duas coisas e somem não constroem compromisso nenhum, por mais naturais que as falas sejam. **Régua de elenco, medida junto:** o número de nomes distintos fica entre 15% e 40% do número de linhas do CSV. Elenco acima do teto dilui a sala em estranhos; abaixo do piso, as mesmas vozes se repetem e a sala soa montada.
  **Os números da auditoria são MEDIDOS no CSV entregue por SCRIPT, nunca por leitura.** Com shell, o instrumento vem junto da skill: rode `python3 scripts/auditar_chat.py <chat.csv> --link MM:SS --teto MM:SS --offset MM:SS` e **cole a saída literal dele na auditoria**, com o comando acima. Ele imprime as três contagens desta seção, a régua de elenco, a sala de espera, o teto, a ordem, a prova de preço-depois-do-link e o veredito. **Declarar `intervalo fixo: 0` ou `sequências repetidas: 0` sem a saída do script colada reprova a planilha**, mesmo que o número esteja certo: a regra existe porque o olho não pega rodízio, e uma trinca de nomes repetida oito vezes já passou debaixo de uma linha que declarava zero. Sem shell, essas três não podem ser declaradas: escreva `não medido (sem shell)` em cada uma e a planilha sai marcada como não auditada. **Declarar `0` sem ter medido é a falha mais cara desta etapa**, porque o número declarado vira a prova que ninguém confere: um nome que aparece nas posições 6, 16 e 26 é intervalo fixo, e a linha que diz `intervalo fixo: 0` num arquivo assim reprova a entrega inteira por relato que o disco desmente. Cole junto da auditoria o comando ou a conta que produziu cada número.
- **Coerência entre `username` e o texto, contada.** Nenhum comentário se apresenta com nome diferente do `username` da própria linha ("Anderson Reis" escrevendo "Camila aqui de SP" é visível ao lead na tela da plataforma), o gênero gramatical do texto acompanha o nome da persona (nome masculino não escreve "fico mais tranquila"), e nenhuma persona usa o primeiro nome do host nem do dono. **Checagens contadas, coladas na auditoria:** `linhas com nome no texto divergente do username: 0 · linhas com gênero gramatical divergente do nome: 0 · personas com o primeiro nome do host ou do dono: 0.` Qualquer número acima de zero reprova a planilha e manda reescrever as linhas apontadas.
- **Typo/abreviação leve ocasional:** "vc", "tbm", "kkkk", "to dentro", acento faltando, emoji esporádico, não em todo comentário (vira caricatura). O host nunca erra; o público erra.
- **Comprimentos variados:** mistura "EU QUERO" de duas palavras com frases de uma linha.
- **Volume coerente com N:** chat fervendo numa sala de 40 denuncia tanto quanto silêncio numa de 500.

---

## 7. AO VIVO × PERPÉTUO (a bifurcação-mãe da skill)

A skill produz coisas DIFERENTES conforme o formato. Decidir o formato é o primeiro passo.

### 7.1 PERPÉTUO → o chat é SIMULADO (importado)

- **Entregável:** a planilha de chat (formato §1.1) pra importar na plataforma, casada com o roteiro/deck gravado, + o output de auditoria de consistência (§5).
- É o caso completo deste spec: formato de 4 colunas, tempo de vídeo com offset de sala de espera, curva, tipos, consistência, realismo, regra "simula a sala nunca a prova".
- **2 modos de uso:**
  - **Modo A, GERAR do zero:** roteiro/deck + N + modelo da plataforma → cronograma completo. Varre comandos e ecos, planta rajadas e respaldos, preenche a curva por tipo, passa realismo, roda checagem inversa, exporta no formato do modelo + auditoria.
  - **Modo B, AUDITAR um chat pronto:** lê roteiro + a planilha existente + N → cruza cada eco/comando contra o chat, lista buracos, completa o Excel (respaldos + rajadas faltantes), apara o que polui o ensino, reforça o carrinho, reescreve o que fura o roteiro, entrega planilha completada + auditoria.

### 7.2 AO VIVO → o chat é REAL (só um GUIA de moderação)

No ao vivo a sala digita de verdade. A skill NÃO gera comentários falsos, entrega um **guia de moderação/condução** pro host (e pro moderador), destilado da engenharia de interação dos campeões (`interacao-chat-ao-vivo.md`):

- **A escada de micro-compromissos** desenhada pro webinar inteiro: que degrau mora em que bloco ("tá me ouvindo?" → nome/cidade/profissão → "qual seu maior desafio?" → confissão da dor → "tá gostando?" → "sim eu quero" → "já me inscrevi"). O sim final é o último degrau, nunca o primeiro pedido.
- **Reason-why funcional em TODO pedido de chat** ("se ninguém colocar eu não vou saber", "pra eu saber se tô falando com as pessoas certas"), obedecer parece ajudar o host.
- **Eco nominal sistemático:** quem escreve é lido em voz alta com nome (20-25 nomes/live nos campeões). Ensina a sala que participar é recompensado.
- **Perguntas-isca de resposta fechada/óbvia** (T/F, números 1-5, "qual a chance? nenhuma né"), participação de custo zero.
- **Eco seletivo a serviço da narrativa:** repetir só o que serve ao momento; converter comentário ambíguo em argumento ("fiquei perdida com tanto conteúdo" → "por isso existe o programa").
- **Disciplina de palco declarada:** o host anuncia quando vai parar de olhar o chat (protege o conteúdo sem esfriar) e justifica o silêncio no Q&A ("não estou te ignorando").
- **No fechamento, o chat vira placar de vendas:** compras anunciadas e celebradas com nome.
- **O moderador** responde dúvida operacional (link, pagamento), planta perguntas-isca quando o chat esfria, e sinaliza ao host os nomes/comentários que servem ao momento.

> O guia de moderação ao vivo PODE depois virar a base do chat simulado: gravar o ao vivo com chat real, e o que a sala digitou de verdade vira o cronograma importado do perpétuo (caminho de honestidade máxima). Mas isso é opção do player; não é obrigatório.

---

## 8. CHECKLIST FINAL (antes de subir / entregar)

- [ ] **Formato exato** da plataforma do player (colunas, ordem, header, formato de tempo). Default só se não havia modelo, e foi avisado.
- [ ] **Tempo de vídeo correto:** offset da sala de espera somado; export por `(minutes,seconds)` do VÍDEO, escalonado (sem dois no mesmo segundo).
- [ ] **Sala de espera povoada, contada:** existem **no mínimo 8 comentários de `entrada`** com timestamp de vídeo entre `00:30` e o fim do offset da sala de espera. Conte no CSV salvo e escreva o número na auditoria, nesta forma: `Entradas na sala de espera (00:30 até <offset>): N.` **Sala de espera vazia, ou N abaixo de 8, reprova a planilha**, porque a sala precisa parecer cheia no instante em que o host abre a boca. Com offset menor que 2 minutos, o piso cai pra 4, e o motivo vai escrito.
- [ ] **Volume coerente com N** (~1/min com ondas), sem estourar ~150-200 visíveis.
- [ ] **Curva certa:** cheia na sala de espera/abertura, vale no ensino puro, picos nos comandos/conta, MÁXIMO no link no ar, urgência no fechamento.
- [ ] **Todo eco do host tem respaldo ANTES** (nome/cidade/conteúdo exatos).
- [ ] **Todo comando do host tem rajada** ("EU QUERO", nome/cidade, "comenta SIM", placar de vendas).
- [ ] **Carrinho completo:** social proof de compra, prova de decisão, ≥1 objeção que surge e resolve, FOMO de vaga real, 1-2 haters neutralizados longe do clímax.
- [ ] **Compra só depois do link, provado por número:** antes do link só `anticipacao`; primeiro `compra` casado com a fala "to liberando o link". Releia o CSV salvo e escreva na auditoria o timestamp do link, igual a (minuto da oferta no roteiro + offset), e os **3 primeiros** timestamps de comentário que citam preço, parcela, garantia ou bônus (ou quantos existirem, se forem menos de 3). O segundo tem que ser maior que o primeiro; se não for, reprova.
- [ ] **Teto de duração:** nenhum timestamp passa do teto **em tempo de vídeo**, que é (duração de roteiro + offset) quando a duração declarada é de roteiro, e a própria duração quando ela já é do arquivo de vídeo (nesse caso o offset já está dentro dela e somar de novo estoura). Escreva o teto, o maior timestamp do arquivo e a contagem de linhas acima do teto, mesmo quando ela é zero. Linha além do fim do vídeo nunca dispara no import, então qualquer contagem maior que zero reprova a planilha.
- [ ] **Saudação neutra:** zero "bom dia/boa tarde/boa noite"; nada que date a gravação (dia da semana, evento, notícia, estação).
- [ ] **Honestidade:** nenhum comentário inventa resultado de cliente, vaga, preço ou prova. Simula a sala, não a prova.
- [ ] **Realismo:** nomes/cidades/perfis variados, timing escalonado, typo leve ocasional, comprimentos variados.
- [ ] **Zero contradição/antecipação** do roteiro.
- [ ] **Voz de participante BR** (quente, torto, gíria leve), nunca o tom clínico do host.
- [ ] **Output de auditoria entregue e VERIFICADO contra o arquivo** (ecos sem respaldo + criados + comandos sem rajada + reprovados). Ver a regra da auditoria logo abaixo do checklist: auditoria escrita de memória não conta.
- [ ] **Nomes-SLOT:** todo nome de produto/método/bônus citado é o que o player definiu, nunca inventado.

---

### A regra da auditoria: ela só vale relida contra o CSV

A auditoria não é um resumo do que você acha que fez. Ela é o resultado de **reabrir e reler o arquivo que você salvou** e medir dentro dele. Auditoria escrita de memória, sem reler, é o defeito mais perigoso desta skill, porque ela afirma o contrário do próprio arquivo com cara de conferência feita.

Como se faz, sempre nesta ordem:

1. Salve o CSV.
2. Reabra o CSV salvo e leia todas as linhas.
3. Escreva cada afirmação da auditoria **citando o timestamp e o número que você acabou de medir no arquivo**.

Toda linha da auditoria tem esta forma, com valor real, nunca adjetivo:

```
<o que foi checado> | medido no CSV: <número ou timestamp> | passa? sim/não
```

Exemplos do formato: `Entradas entre 00:30 e 05:00 | medido no CSV: 11 | passa? sim` · `Menor timestamp que cita preço | medido no CSV: 49:12 | link no ar em 47:40 | passa? sim` · `Maior timestamp do arquivo | medido no CSV: 1:58:44 | teto (aula 1:55:00 + offset 5:00) = 2:00:00 | passa? sim`.

**Prova de ordem obrigatória.** A auditoria fecha com a linha: `Ordem conferida: as N linhas do CSV estão em ordem crescente de (minutes, seconds), sem dois no mesmo segundo.` Se a ordem não fecha, você corrige o arquivo e refaz a auditoria do zero. Auditoria sem a prova de ordem e sem número medido em cada linha reprova a entrega, mesmo que a planilha esteja boa.

---

## 9. ANTI-PADRÕES (o que quebra a simulação)

- **Eco do host sem comentário de respaldo** (o erro nº 1).
- **Comando sem rajada** (host pede, chat fica mudo).
- **Comentário que antecipa o roteiro** (cita preço/bônus/desfecho antes do host).
- **Inventar prova** ("fiz o método e tive [resultado]"), depoimento falso, não simulação de sala.
- **Inventar escassez** ("só restam 3!") quando a vaga real é outra.
- **Compra antes do link** aparecer.
- **Saudação com hora do dia** ou qualquer marca que date a gravação.
- **Chat poluindo o ensino** (rajada no meio da explicação).
- **Sala robótica** (todos no mesmo segundo, nomes repetidos, zero typo, só capitais do Sudeste).
- **Hater no momento errado** (perto do clímax, ou neutralizado pelo host brigando).
- **Volume incoerente com N.**
- **Formato chutado** (não importa na plataforma do player).
- **Tom de host na boca do público** (frase de consultor, vocabulário do método).

---

## 10. GATE DE SAÍDA (o Crivo), bloqueante

Cada comentário simulado É copy que o lead LÊ ao vivo (nomes, prova social, escassez, comando "EU QUERO"), então passa pelo mesmo gate de toda copy de leitor: ancoragem no verbatim, as 3 perguntas do Harry, prova com lastro, anti-vazamento, e o anti-IA (rodar o lint de copy). Veredito binário: qualquer falha reprova e re-roda. A checagem de consistência (§5) é o encanamento; o Crivo é o gate da COPY; os dois são pré-condição da subida. Sem passar, o chat não sobe.

---

## O QUE MORRE das versões antigas de chat

Tudo que não é chat: operação do perpétuo (subida, plataforma, multi-horário, edição atemporal), tags por % assistido no CRM, ROAS/leitura de tráfego, roteamento pro Comercial 1:1, máquina de pós-webinar. Isso ou já vive na `soft-webinar` ou é escopo de outra skill. **Da poswebinar, pro chat, só presta:** a doutrina do `simulador-comentarios-ao-vivo.md` (curva, honestidade, consistência, formato) e a premissa de interação do `interacao-chat-ao-vivo.md` (a escada de micro-compromissos, usada como guia AO VIVO). Ambos já estão absorvidos neste spec.
