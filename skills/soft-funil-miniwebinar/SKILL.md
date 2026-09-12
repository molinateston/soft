---
name: soft-funil-miniwebinar
description: >-
  Escreve o ROTEIRO do mini-webinar, o vídeo de cerca de 10 minutos que filtra quem não é cliente, instala uma virada de percepção e move pra conversa, e, sob pedido, veste esse roteiro de SLIDES e monta a PÁGINA que hospeda o vídeo. Use quando o pedido for: "mini webinar", "webinar curto", "aula de vendas curta", "webinar do funil", "mini aula em vídeo", "um vídeo de 10 minutos que vende", "slides do mini webinar", "deck do mini webinar", "página do mini webinar", "página que hospeda o vídeo". NÃO use pra: "faz uma VSL" ou o vídeo de vendas em arco de carta (soft-funil-carta); webinar completo ou perpétuo, o deck dele ou as 3 páginas dele (soft-webinar); a régua de mensagens pós-isca ou de aquecimento (soft-funil-nutricao); landing de captura ou de vendas (soft-funil-landing); isca (soft-funil-isca); lançamento com carrinho (soft-launch); script da conversa de venda (soft-vendas-closer); arte (soft-designer). Leia e siga o fluxo inteiro do SKILL.md.
---

# Mini-webinar, a carta com câmera

Vídeo de cerca de 10 minutos que faz UMA coisa: filtra quem não é cliente, instala UMA virada de percepção e move quem ficou pra conversa. Mesma engenharia da carta, mídia diferente. Não é aula-tutorial nem webinar completo: roda o arco comprimido, com o mecanismo nomeado no centro.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Os arquivos que cada ação exige (`--exige`).** A conferência da ação roda `python3 scripts/checar_titulos.py --conferir <pasta> --exige <lista>`, e arquivo da lista ausente sai com exit 1 e `arquivo exigido pela ação ausente: <nome>`.
- Ação 1 · VERSÃO-MESTRE: `--exige 00-versao-mestre.md`
- Ação 2 · ROTEIRO: `--exige 00-versao-mestre.md,01-roteiro-miniwebinar.md`
- Ação 3 · SLIDES: `--exige 02-slides-miniwebinar.pptx`
- Ação 4 · PÁGINA: `--exige 03-pagina-miniwebinar.md`
- Pacote (1, 2, 3, 4): `--exige 00-versao-mestre.md,01-roteiro-miniwebinar.md,02-slides-miniwebinar.pptx,03-pagina-miniwebinar.md`

"pacote", "o kit", "monta tudo" e "o pacote inteiro" caem todos na linha do pacote. **Entregar 2 das 4 ações num pedido de pacote é entrega incompleta, não escopo reduzido**: se você achar que o dono quis menos, entregue as quatro e diga em 1 linha o que achou.

**O último capítulo, bloco ou seção carrega tese no título, como todos os outros.** `Resumo`, `Conclusão`, `Considerações finais`, `Fechamento` e `Recapitulando` são rótulos de estrutura e reprovam a régua. O lugar que o leitor lê por último recebe a frase mais concreta do material, jamais a mais geral. Cole `capítulos: N · com tese no título: N`, iguais.

**Num universo acima de 20 títulos, a R7 exige versão morta colada.** `reescritos` igual a 0 ou 1 num lote desse tamanho é a régua rodando de leve: cole a versão morta de pelo menos três títulos, mostrando que a reescrita foi tentada e a original venceu. O `--conferir` sai com exit 1 quando `reescritos` fica abaixo de 5% do universo.

**A frase que sobrevive não pode sobreviver à troca de nicho.** A frase-tese da peça passa pelo teste do nicho trocado como qualquer outra linha, e `sobrevive? sim` nela reprova, ao contrário da tabela de checagem. Cole `frase que sobrevive | substantivo trocado: <original> → <outro mercado> | sobrevive? não`. Máxima de marketing que qualquer negócio repetiria não é a frase da dona: é a frase de ninguém.

**Os títulos das etapas são teses, não rótulos.** `## P3` é numeração; `## P3: cada peça existe para impedir uma desistência específica` é a etapa dizendo o que decidiu. A isenção de rótulo estrutural vale pra cabeçalho de anexo, de tabela e de fonte, **nunca pras etapas do plano**: renomear uma etapa pra caber na isenção reprova a entrega, porque troca a qualidade da peça pela facilidade do gate, e o `--conferir` imprime cada caso como `rótulo no miolo: <linha>`. Cole `etapas: N · com tese no título: N`, iguais. **E nenhum cabeçalho nomeia um requisito da régua:** `Seção de fecho`, `Frase que sobrevive`, `Checagem`, `Inventário` e `Régua` são nomes do gate. A frase que sobrevive entra no fecho sem cabeçalho próprio, ou sob um cabeçalho que seja ela mesma. Cole `cabeçalhos que nomeiam um requisito do gate: 0`.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**O que é obrigatório e o que é opcional, antes de qualquer coisa:**
- **O ROTEIRO é obrigatório.** É a espinha. Nada aqui existe sem ele.
- **Os SLIDES são opcionais**, entram só depois do roteiro fechado e aprovado, quando o dono pedir.
- **A PÁGINA é opcional**, mesma regra.

Ninguém monta deck sem roteiro fechado, porque o deck nasce do roteiro, nunca do zero.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra o fluxo num caso fictício de nicho neutro: a versão-mestre, uma fase do roteiro escrita por inteiro com o tom e a densidade que se espera, dois slides no formato de entrega, três blocos da página, e o que o gate reprovou.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola tudo que tem sobre a oferta e o público e eu escrevo o mini-webinar). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra execução com o que o dono colou. Se faltar um insumo que o mini-webinar não vive sem (a oferta, a promessa única, o público), pergunta AQUELE insumo e segue, sem voltar pra ancoragem inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a ancoragem e o briefing uma pergunta de cada vez, e monta o roteiro com o que o dono for dando.

**Ensina enquanto faz (parte 2):** em cada escolha que muda o roteiro (a promessa, o mecanismo nomeado, a ordem das 4 fases, o convite), escreve UMA linha do porquê na voz de quem ensina o método, pra o dono aprender a decidir sozinho na próxima.

**Puxa o material bruto (parte 3):** quando a resposta vier rasa ("quero vender mais", "o público de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: a frase literal de um cliente na dor, um case real com número, a objeção que mais aparece. Verbatim real vira a âncora do roteiro; resposta rasa vira mini-webinar raso. Puxa uma vez, com jeito; se o dono não tiver, segue com o que há e marca o furo.

**Oferece refinar no fim (parte 4):** depois de mostrar a fase ou a peça, fecha com UMA linha: "Quer outro gancho na abertura? Mais curto? Outra prova? Me diz o que ajustar que eu refaço só essa parte." A oferta de refino não substitui o STOP nem o gate.


## Quando cada peça entra (a tabela única)

| O dono pediu | Entra na ação | Pré-requisito |
|---|---|---|
| "mini webinar", "webinar curto", "aula de vendas curta", "webinar do funil", "mini aula em vídeo", "a versão em vídeo da carta", "um vídeo de 10 minutos que vende" | **1 · VERSÃO-MESTRE**, depois **2 · ROTEIRO** | nenhum |
| "slides do mini webinar", "deck do mini webinar", "monta as telas" | **3 · SLIDES** | o roteiro fechado e aprovado |
| "página do mini webinar", "página que hospeda o vídeo", "onde eu coloco esse vídeo" | **4 · PÁGINA** | o roteiro fechado (a página cita a promessa dele) |
| "o pacote inteiro" | **1, 2, 3, 4**, na ordem, com parada em cada | nenhum |
| "olha esse roteiro aqui e diz o que está errado" | **5 · GATE** em modo auditoria | a peça colada |

Se o dono pedir slides ou página sem roteiro fechado: **PARA e fecha o roteiro primeiro.** Diga isso em 1 linha, não invente fala de palco.

## Como ler cada ação

Toda ação traz o mesmo bloco: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · os passos numerados, com **STOP** onde o dono aprova.

**O perfil do dono vem do banco do agente.** Onde a ação precisar de posicionamento, avatar, mecanismo nomeado, voz, oferta ou prova: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta do "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR: o quê]`. Nunca invente, nunca pare por causa disso.

**Antes de escrever qualquer cena com pessoa, rode o passo de nomes.** A pessoa citada costuma ser justamente quem vai ler a peça. Rode antes da primeira linha da abertura:

```
python3 scripts/checar_titulos.py --peca <cada entregável> \
  --insumos <pasta de insumos do dono> --perfil <perfil do dono>
```

Ele imprime `nomes candidatos achados pelo script: N` e, por nome, `autorização no insumo: sim/não` e `mensagem privada: sim/não`. **Nome com `mensagem privada: sim` e `autorização: não` sai da peça** e vira a forma por faixa ("uma aluna na casa dos 50"). Lead com pergunta sem resposta nunca vira cena de abertura. Cole `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada: 0`.

**O marcador é campo, e campo tem tamanho.** Na peça pública ele cabe em `[A CONFIRMAR: <o dado>]`, no máximo 6 palavras, depois de um rótulo e no fim da linha. **O porquê da pendência nunca entra na peça**, vai pro handoff com o número da linha ao lado. O script conta e reprova acima do teto, em `marcadores acima de 6 palavras: N (teto 0)`.

**A frase que sobrevive fora do contexto.** No fecho, escolha a UMA frase que a dona repetiria de cor numa conversa, cole ela sozinha e responda por escrito por que ela sobrevive fora do contexto. Nenhuma significa que a peça está correta e não está viva. Cole `frase que sobrevive fora do contexto: <literal>`, com o porquê em uma linha.

**As 6 leis de operação** (detalhe em `shared-references/operacao-padrao.md`, Seção 0): (1) cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**; (6) **doc de saída enxuto pros 2 leitores**, zero meta-narração, só o insumo denso mais `[A CONFIRMAR]` onde falta.

**Re-gate ao condensar:** o texto de TELA de cada slide e os blocos NOVOS de copy da página são condensações novas que o lead LÊ, não a fala original do roteiro. Elas re-passam pelo gate antes de sair, do mesmo jeito que o roteiro passou.

---

## Ação 0 · ANCORAGEM (roda antes de tudo, não pula)

**O que faz:** abre a fonte de fala real e puxa a matéria-prima da abertura e do diagnóstico.

**Precisa de:** a fonte, nesta ordem: descrição do projeto → posicionamento do dono → mensagens anteriores. De lá saem **3 a 5 falas de DOR e 3 a 5 de DESEJO**, literais, com o N.

**Sem o insumo:** três estados, declare o seu em 1 linha.
- **Tem fala real com N:** ancora nela e cita o N.
- **Tem posicionamento, zero fala literal:** não invente. Ancore em prova real do dono; número não confirmado vira `[A CONFIRMAR: número]`.
- **Sem nada:** pergunte numa mensagem só as 6 entradas do briefing (cliente ideal · problema avançado · soluções comuns que falham · método nomeado · casos e prova · oferta) e siga.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Ativo de prova citado se confere contra o perfil.** Antes de escrever qualquer frase que ASSUMA a existência de um ativo de prova (destaques no perfil, prints, depoimentos gravados, página no ar, link, portfólio, avaliações), confira se o perfil do dono registra que ele existe. Se o perfil diz que não existe, ou não diz nada, **a frase não entra** e o bloco sai com `[A CONFIRMAR: prova]`. Mandar a audiência conferir uma prova que não está lá queima a peça inteira na hora em que alguém vai olhar. Checagem verificável antes de fechar: liste toda frase que manda a audiência ver alguma coisa, uma por linha, na forma `<frase> | ativo <nome> | o perfil registra que existe: sim ou não`; qualquer `não` reprova a frase e manda trocar pelo marcador.

**Entrega:** nada de arquivo.

**Leia primeiro:** `shared-references/crivo/01-entrada-verbatim.md`.

---

## Ação 1 · VERSÃO-MESTRE (a narrativa neutra, antes dos 12 blocos)

**O que faz:** produz a narrativa de venda em texto corrido, nos 7 passos do discurso base, que vira o andaime dos 12 blocos do roteiro. **É uma etapa própria e consome uma rodada inteira.** Ela não é parte do passo zero.

**Precisa de:** o briefing da Ação 0 · o mecanismo nomeado · a prova.

**Sem o insumo:** sem mecanismo nomeado, escreva a versão-mestre com o mecanismo descrito pela função e marque `[A CONFIRMAR: nome do mecanismo]`. O nome pode nascer aqui, e nesse caso proponha 2 ou 3 e deixe o dono escolher.

**Entrega:** `00-versao-mestre.md`, os 7 passos em texto corrido neutro: gancho · diagnóstico sem culpa · por que as soluções comuns falham · método nomeado · prova específica · objeções · oferta e convite. **STOP.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/discurso-base-7-passos.md` (o objetivo, o conteúdo, o tom, os erros e o exemplo de cada passo, mais as 3 objeções universais e o template da versão-mestre).

**Profundidade:** `references/modo-mini-webinar.md` (o mapeamento de cada passo pras 4 fases).

**Por que ela existe:** sem essa espinha, os 12 blocos saem soltos e o vídeo perde a costura. Cada passo da versão-mestre se distribui nas 4 fases depois, e é isso que garante que a fala do minuto 8 ainda esteja falando com a promessa do minuto 1.

**Também confirme aqui, numa mensagem só, duas perguntas de oferta:**
- **Oferta secundária estruturada?** (programa pra quem implementa, certificação, coprodução). Se sim, entra no bloco D.6. Se não, some.
- **Garantia?** Se sim, entra em 1 frase na fase de ação. Se não, some.

Não force nenhuma das duas. Ausência some, não vira recheio.

---

## Ação 2 · ROTEIRO (as 4 fases, uma por vez)

**O que faz:** quebra a versão-mestre em 12 blocos dentro das 4 fases, com timestamps, entregando **uma fase por vez**.

**Precisa de:** a versão-mestre aprovada · as falas da Ação 0 · a resposta das 2 perguntas de oferta.

**Sem o insumo:** sem versão-mestre, volte pra Ação 1. Ela não se pula.

**Entrega:** `01-roteiro-miniwebinar.md`, de 9 a 11 minutos, 12 blocos nas 4 fases, com timestamps. **STOP por fase** (atenção → diagnóstico → mecanismo → ação), nunca o roteiro inteiro de uma vez.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/modo-mini-webinar.md` (os 12 blocos com modelo e exemplo de cada um, o mapeamento do discurso base, as métricas e o diagnóstico por sintoma).

**Profundidade:** `references/tom-e-ritmo-desejo.md` (as 7 categorias de corte, na hora do gate anti-IA; vídeo tem tom falado, e as regras de ritmo de leitura não valem aqui) · `references/conducao-na-pratica.md` (a congruência: o vídeo repete a mesma tese e o mesmo mecanismo do feed e da carta, na mesma voz).

### Fase ATENÇÃO (0:00 a 1:30)
Prende quem é avatar e expulsa quem não é, em 90 segundos.
- **A.1 · Promessa direta e filtragem (45 a 60s):** promessa quantificada em 1 frase mais a lista de 5 ou mais perfis específicos do nicho. Abre amplo, nicha do meio pro fim.
- **A.2 · Prova social ancorada (30s):** aponta pra prova externa visível (depoimentos, prints), "pode pausar e olhar agora". Prova antes do problema antecipa autoridade.

### Fase DIAGNÓSTICO (1:30 a 3:00)
Amplia a dor, tira a culpa do lead, nomeia o inimigo, que nunca é o próprio lead.
- **I.1 · Problema geral (45 a 60s):** a dor óbvia do nicho em segunda pessoa, 3 ou 4 sintomas concretos, e o "mesmo assim, [resultado insuficiente]". Quanto mais específico o sintoma, mais o lead pensa "é isso".
- **I.2 · Problema avançado (30 a 45s, opcional):** só se o dono tem problema avançado nomeado. "O problema não é [culpa aparente]. É que [as soluções comuns] adicionaram complexidade." Nomeia o vilão, tira a culpa, joga a raiva pra fora.

### Fase MECANISMO (3:00 a 9:00), o coração
Instala a crença única, entrega o mecanismo nomeado, prova, faz querer. É 60% do vídeo. Sem o mecanismo nomeado no centro, não é mini-webinar, é palestra.
- **D.1 · Promessa expandida, método nomeado e projeção (3:00 a 4:30):** resultado principal mais 2 amplificadores, **diz o nome do método**, camada opcional de "sem" como filtro, projeta o estado desejado.
- **D.2 · Mecanismo demonstrado (4:30 a 6:00):** compromisso pessoal, as 3 peças nomeadas, a jornada do lead dentro do método, a peça de redenção pra quem já tentou, o grau de automação.
- **D.3 · Demonstração prática (6:00 a 6:30):** o passo a passo do trabalho DO CLIENTE em segunda pessoa ("você vai..."), com tempo de execução. Reduz a abstração.
- **D.4 · Prova e estado final (6:30 a 7:30):** número agregado, variedade do que já foi vendido pelo método, onde ver, rotina simplificada depois.
- **D.5 · Validação, métrica e recorte (7:30 a 8:30):** ancora numa categoria em alta, uma métrica de saúde concreta, e 1 recorte que filtra o lead atento.
- **D.6 · Amplitude dupla e oferta secundária opcional (8:30 a 9:00):** benefício pra quem já fatura, benefício pra quem não fatura, e a porta do implementador, só se confirmada na Ação 1.

### Fase AÇÃO (9:00 a 10:00)
Move pra conversa sem empurrar venda. Aqui a ação é LEVE: convida, não fecha no checkout.
- **A.1 · Dois caminhos, prazo e garantia opcional (9:00 a 9:30):** caminho 1 sozinho (com pré-requisito honesto) · caminho 2 comigo (com ressalva humanizadora e prazo de implantação, nunca prazo de resultado) · garantia em 1 frase, se confirmada.
- **A.2 · Convite e fechamento afetivo (9:30 a 10:00):** a ação concreta e de baixa fricção com **destino claro** (a palavra no direct ou o link), "não é compra, é conversa", o compromisso pessoal repetido, despedida curta.

**Ao fim da fase de ação**, com o roteiro fechado, ofereça o menu: *"roteiro fechado. Quer que eu monte os slides, a página, ou os dois? Os dois são parte do mesmo mini-webinar e entram sob pedido."* Não despeje nenhum dos dois sem pedido.

---

## Ação 3 · SLIDES (OPCIONAL, veste o roteiro de tela)

**O que faz:** projeta os 12 blocos nos slides, com a copy falada na nota e só o reforço na tela.

**Precisa de:** **o roteiro fechado e aprovado** (pré-requisito duro) · o nome do método · os números reais que viram manchete.

**Sem o insumo:** sem roteiro fechado, PARA e fecha o roteiro primeiro. Sem número real pro slide de número gigante, esse slide não existe: troque por uma frase de reforço e marque `[A CONFIRMAR: número]`.

**Entrega:** `02-slides-miniwebinar.md`, por slide: o **arquétipo**, o **reforço visível** (1 frase OU 1 número OU 1 imagem-conceito) e a **copy falada na nota**. Entrega **por fase**, nunca o deck inteiro de uma vez. **STOP por fase.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/geracao-slides-miniwebinar.md` (antes de montar o primeiro slide).

**Profundidade:** `references/modo-mini-webinar.md`.

**A regra de ouro:** a copy falada mora na NOTA; a tela recebe só o reforço. **Pergunta-teste por slide:** "dá pra narrar lendo só a tela?" Se dá, está errado, joga o texto pra nota.

**Arquétipo pela função do beat:** respiro (tela preta, 1 frase) em toda virada de fase · capa na abertura · número gigante só com número real · dicotomia com cor (o medo primeiro, o desejo depois) · cena de dor (1 cena por slide) · revelação progressiva SIMPLES do mecanismo, peça a peça · manifesto · convite com destino.

**Calibragem:** deck enxuto de **12 a 20 slides**, não 72, porque o vídeo tem 10 minutos. **Sem a maquinaria de empilhamento e preço**, porque a ação convida pra conversa. Persegue o RITMO (respiro em toda virada), não uma contagem-alvo. Reserva a zona da câmera na nota. Tela legível no celular.

**Os dois caminhos de saída, e o que fazer quando o gerador não está disponível:**
- **Teste antes de escolher o caminho, sempre.** Rode `python3 scripts/deck_gen.py --help` e cole a saída no relatório, junto do código de saída (`echo $?`). Saída de ajuda com código 0 prova que o script está íntegro e o arquivo de apresentação passa a ser obrigatório. O caminho do `.md` só vale quando esse comando falha, ou quando a geração em si quebra: nesse caso cole a mensagem de erro **da geração**, nunca a de um comando de ajuda. Um segundo teste, se você quiser confirmar o esquema dos dados antes de gastar a renderização: `python3 scripts/deck_gen.py --check <arquivo de dados>`. É esse teste, não a sua leitura da regra, que decide qual dos dois caminhos vale.
- **Com shell e com o script:** monta o array de dados no formato que `scripts/deck_gen.py` espera (o campo de nota carrega a copy falada) e gera o arquivo de apresentação. **Com o script presente e shell disponível, o arquivo de apresentação é obrigatório e o `.md` sozinho reprova a Ação 3**, por mais completa que a descrição esteja: o dono pediu o pacote e receber a descrição do deck no lugar do deck é entrega faltando uma peça. Nome do arquivo: `02-slides-miniwebinar.pptx`, ao lado do `.md`.
- **O deck entregue sai do gerador, e você prova isso.** O título de cada slide sai em caixa normal (só o kicker e o rodapé, os rótulos de até 16px, vão em caixa alta): o próprio gerador já produz assim, e um `.pptx` que chega em caixa alta no título saiu de outra ferramenta ou foi tocado à mão. Depois de gerar, rode o gerador uma segunda vez a partir do mesmo array de dados, num caminho temporário, e compare o texto dos dois slide a slide com `python-pptx`. Cole `slides iguais: N de N` e `deck reproduzido do JSON: sim`. Divergência quer dizer que o binário foi editado por fora, e o certo é consertar os dados ou o gerador, nunca o `.pptx` na mão. Confira também o campo `Application` do `.pptx` (`docProps/app.xml`): deck que não bate com o do gerador entra como deck fora do método.
- **Só quando o script não existe ou quebra ao rodar:** **não falhe em silêncio.** Entregue o deck descrito slide a slide no `.md`, com arquétipo, reforço e nota, mais o identificador visual de cada um, e diga em 1 linha por que o gerador não rodou, colando a mensagem de erro. Aí sim esse `.md` é entrega completa: qualquer renderizador, inclusive uma pessoa montando à mão, consegue trabalhar em cima dele.
- **Nada de marcador dentro do pixel do slide.** Antes de gerar, rode `grep -n 'A CONFIRMAR' <arquivo de dados dos slides>` e confira campo a campo: nenhum título, reforço, subtítulo, nota ou rodapé de slide pode conter marcador de pendência, porque o slide é pixel projetado numa sala e não texto que o leitor edita. Prova depois de gerar, com a saída colada: `python3 -c "from pptx import Presentation; import sys; print(sum(sh.text_frame.text.count('A CONFIRMAR') for s in Presentation(sys.argv[1]).slides for sh in s.shapes if sh.has_text_frame))" 02-slides-miniwebinar.pptx`. Qualquer valor diferente de 0 reprova a Ação 3 e manda refazer o slide. Quando o dado falta, o slide sai sem o slide: prova sem autorização registrada não vira tela, vira linha do handoff.
- **Nenhum slide repetido em sequência.** Antes de fechar, liste os slides em coluna com o texto de tela de cada um e compare cada linha com a seguinte; duas telas iguais coladas não são respiro, são erro de montagem. Cole `slides: N · pares consecutivos iguais: 0`.
- **O binário é lido de volta antes de fechar, e o `.md` de origem não responde por ele.** Depois de gerar o deck, extraia o texto do arquivo que o dono recebe e cole a contagem:

```
python3 -c "import zipfile,re,sys; z=zipfile.ZipFile(sys.argv[1]); \
t='\n'.join(' '.join(re.findall(r'<a:t>(.*?)</a:t>', z.read(n).decode('utf-8'), re.S)) \
for n in sorted(z.namelist()) if re.match(r'ppt/slides/slide\d+\.xml$', n)); \
print('caracteres:', len(t)); print('linhas com acento:', \
sum(1 for l in t.splitlines() if re.search('[áéíóúâêôãõç]', l, re.I)))" <deck>.pptx
grep -c '[áéíóúâêôãõç]' <deck>.md
```

**`linhas com acento: 0` num texto em português com mais de 200 caracteres reprova o deck**, porque a origem foi escrita sem acento pra fugir de encoding e ninguém abriu o resultado. Rode o lint sobre o texto extraído, nunca só sobre o `.md` de origem, e cole `<deck>.pptx (texto extraído): exit N`. O `python3 scripts/checar_titulos.py --conferir <pasta>` refaz as duas contagens e reprova sozinho com `deck sem acentos`.

Mesmo deck conceitual nos dois casos. Só muda o motor que renderiza.

---

## Ação 4 · PÁGINA (OPCIONAL, emoldura o player e carrega o argumento)

**O que faz:** monta a página que hospeda o vídeo, bloco a bloco.

**Precisa de:** o roteiro fechado (a headline é o espelho da promessa do bloco A.1) · a prova · a bio do dono · o ticket (decide o destino do botão).

**Sem o insumo:** sem prova, os blocos de prova saem com `[A CONFIRMAR: prova]` e a página não sai como pronta pra publicar. Sem ticket declarado, assuma ticket alto (o botão vira conversa, nunca preço seco) e diga a premissa em 1 linha.

**Entrega:** `03-pagina-miniwebinar.md`, bloco a bloco, na ordem em que aparecem na tela. **STOP por bloco.**

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/pagina-hospedagem-rica.md` (antes de montar o primeiro bloco).

**A régua-mãe:** cada bloco **protege a atenção OU protege a venda OU mede**. Se não faz nenhuma das três, corta. Mobile-first é a régua, o vídeo fica num player com boa entrega em celular, e o botão fica sempre ABAIXO do player.

**A ordem dos blocos:**
1. **Headline:** espelho da promessa direta do bloco A.1 do roteiro.
2. **Sub-headline:** o "sem" ou o filtro de avatar, em 1 linha.
3. **Para quem é:** 4 a 6 perfis específicos, a mesma filtragem do bloco A.1.
4. **O player:** centro da página, botão logo abaixo, capa com rosto, sem reprodução automática no celular.
5. **O argumento em estilo de carta**, abaixo do player: os 7 passos da versão-mestre, condensados (gancho, diagnóstico sem culpa, por que as soluções comuns falham, o método nomeado como arquitetura, prova específica, as 3 objeções universais, convite único). Mostra resultado e função, nunca o passo a passo executável.
6. **Provas:** muitas, na moeda da promessa (nome, nicho, número, prazo), com prints. Documento bruto vale mais que slide bonito.
7. **Perguntas frequentes:** mata as objeções reais do avatar, em tom de conversa, sem urgência fabricada. A página é permanente, então nada de cronômetro que reinicia.
8. **Bio na ÚLTIMA dobra:** empatia e cicatriz antes do feito, número com ressalva honesta, fecho sem promessa milagrosa. Nunca o currículo no topo.
9. **Convite final único**, com destino concreto: "conversa, não compra" (a palavra no direct ou o link).

**Decisão de negócio pelo ticket:** ticket baixo pode levar direto ao checkout; ticket alto fecha na conversa, com botão pro canal de mensagem, nunca o preço seco na página.

---

## Ação 5 · O GATE (roda por dentro, por fase e por peça, e não imprime)

**Régua de títulos (roda antes do resto do gate).** Todo título que sai desta skill passa pela régua `shared-references/crivo/07-regua-de-titulos.md`, R1 a R7. Rode a régua sobre a headline e a subheadline da página, sobre o título de cada bloco e sobre o reforço visível de cada slide do deck. A checagem sai colada num arquivo do disco que o dono abre, uma linha por título, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a entrega antes da análise de conteúdo. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Rótulo de seção não é título, e a coluna diz qual é qual.** Classifique cada título de bloco e reforço de slide como `rótulo` ou `tese`, numa coluna própria da checagem. Rótulo nomeia o assunto e não afirma nada (`Resumo`, `Introdução`, `O método`, `Próximos passos`); tese afirma alguma coisa que o leitor pode discordar (`O passo que todo mundo pula é o que decide`). O título de bloco e reforço de slide é a primeira coisa que o leitor lê antes de decidir se continua, e um documento de rótulos não segura ninguém. Cole a coluna inteira, um por linha, na forma `<título> | rótulo ou tese`, e **todo `rótulo` volta pro passo de escrita** antes de a peça sair. Feche com `títulos de seção: N · em tese: N · rótulos restantes: 0`.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Todo marcador nasce de uma busca que falhou, nunca de uma lacuna presumida.** Antes de escrever `[A CONFIRMAR: <dado>]`, rode `grep -rin '<termo>' <insumos do dono>` sobre os insumos que o dono entregou (transcrição, caixa de entrada, perfil, reclamação, call) e cole a saída ao lado do marcador. **Saída não vazia proíbe o marcador:** o dado existe, leia a linha e escreva o valor na frase. Cole `marcadores na peça: N · com grep colado: N · com grep vazio: N`. Marcador sem grep colado reprova a peça, porque presumir lacuna sobre arquivo que ninguém abriu é o jeito mais barato de transformar dado disponível em pendência.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**A chamada da persona nunca leva nome real.** Persona, avatar, persona-âncora, cena-assinatura e célula do Mapa de Munição são peça pública, mesmo dentro de um documento de estratégia: é deles que nascem as capas dos meses seguintes. Rode `grep -rn 'autorizado por' <insumos>`; **saída vazia proíbe nome próprio de pessoa real em qualquer um desses cinco lugares.** A persona sai por idade, profissão e situação (`55, contadora, operou o menisco`). Quando o texto precisar mesmo de um nome pra chamar a pessoa, **use um nome inventado e diga na mesma linha que é inventado**: `Marta (nome inventado), 55, contadora`. **Lead com negociação em aberto na caixa de entrada nunca vira persona-âncora**: ela é a primeira a ler a peça e vai encontrar a própria transcrição virada em avatar. Feche com `personas na peça: N · com nome inventado declarado: N · com nome real dos insumos: 0`.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.

**O piso do inventário é contável e a conta vai colada.** Rode `grep -c '^- ' <perfil>` e cole a saída do comando: esse número é o PISO BRUTO. Depois desdobre toda linha que carrega mais de um valor (a oferta com preço, parcela, 3 bônus e garantia conta 6, não 1) e cole `piso bruto: N · desdobrados: M · Dados fornecidos: N+M`. **`Dados fornecidos` menor que o piso bruto reprova a entrega**, porque significa que a peça descartou campo sem registrar o motivo. Não qualifique a linha com recorte de escopo: o total é o total, e o filtro de relevância mora na coluna de destino de cada dado, nunca no total.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


**O que faz:** reprova a fase ou o bloco que não serve, antes de o dono ver. Serve também como modo auditoria, quando o dono cola um roteiro pronto.

**Precisa de:** a peça escrita.

**Entrega:** nada em modo normal (auditoria silenciosa, a tabela **nunca** vai pra saída). Em modo auditoria, entrega `diagnostico-miniwebinar.md` com a fase, o check que falhou e a correção.

**Leia primeiro:** `shared-references/crivo/03-gate-cub.md`.

**Profundidade:** `references/tom-e-ritmo-desejo.md` · `shared-references/crivo/02-simulacao-cliente.md` (o teste dos 2 segundos: onde o lead larga, onde ele se reconhece) · `shared-references/filtro-anti-ia/padroes-banidos.md` e `falsos-positivos.md`.

**O veredito é o PIOR item.** Um ✗ refaz **só a peça ou a fase que falhou**, nunca o pacote inteiro. Os checks do roteiro valem sempre; os marcados **(slides)** só ativam na Ação 3, e os **(página)** só na Ação 4.

| Check | Passa se |
|---|---|
| **Ancorado** | a dor e a promessa nascem de fala literal da fonte (cita o N **real**) ou de prova real do dono. N inventado reprova na hora |
| **Cada fase faz só o trabalho dela** | a fase cumpre a função dela e cabe no tempo. Nenhuma rouba a função de outra: a atenção filtra, o diagnóstico dói, o mecanismo prova, a ação move |
| **Mecanismo é o coração** | o **nome do método** aparece e ocupa o centro (60% do vídeo). A peça vende uma virada de percepção, não ensina um tutorial executável |
| **É o degrau curto, não o webinar completo** | a ação CONVIDA pra conversa, não fecha no checkout nem vira o webinar de uma hora |
| **Uma virada, não uma aula** | o lead sai com UMA percepção nova, não com um passo a passo que dispensa o dono |
| **C/U/B** | não é **C**onfuso (uma ideia por frase), não é **I**nacreditável (a prova sustenta), não é **B**oring (zero enchimento, zero motivacional) |
| **Dá pra ver** | fecha o olho e enxerga a cena. Reprova "tenha mais clareza". Passa "a recepcionista diz: semana que vem enche" |
| **Dá pra falsificar** | é fato falsificável, não adjetivo bonito |
| **Só você diz** | o concorrente direto não assina igual |
| **Convite com destino** | a ação tem destino concreto (a palavra no direct ou o link nomeado) e é "conversa, não compra" |
| **Anti-IA (duro)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz (o verbo que rima com "cravar" e as flexões dele; exceção: aspa literal do cliente) · sem frase-emoldura · sem verbo-clichê de hype · zero advérbio gratuito · zero hesitação · zero auto-elogio · zero paráfrase · zero transição mole. As 7 categorias de corte estão em `references/tom-e-ritmo-desejo.md` |
| **(slides) 1 ideia por slide** | passa a pergunta-teste (não dá pra narrar lendo só a tela). A copy falada está na nota |
| **(slides) Densidade baixa** | framework simples, sem diagrama de consultoria. Só o slide de prova pode ser denso |
| **(slides) Respiro em toda virada** | tela de respiro com 1 frase em cada virada de fase |
| **(slides) Deck curto** | sem empilhamento nem preço, de 12 a 20 slides |
| **(slides) Número gigante só real** | o número que vira manchete é dado real. Inventado reprova na hora |
| **(página) Cada bloco protege ou mede** | protege a atenção, protege a venda ou mede. Enfeite que não faz nenhuma das três é cortado |
| **(página) Botão abaixo do player** | o botão fica abaixo, nunca acima. Mobile-first |
| **(página) Bio na última dobra** | empatia e cicatriz antes do feito, nunca o currículo no topo |
| **(página) Provas na moeda da promessa** | nome, nicho, número e prazo, na moeda do que foi prometido |
| **(página) Perguntas frequentes sem urgência falsa** | responde as objeções reais, zero cronômetro numa página permanente |
| **(página) Argumento sem o passo a passo** | vende a virada, não entrega a receita |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ refaz só a peça ou a fase que falhou |

Com shell disponível, rode o lint de copy em `scripts/lint_copy.py` sobre o roteiro, sobre a copy de tela dos slides e sobre os blocos da página. Sem shell, faça a busca manual pelos dois bloqueios duros antes de marcar o anti-IA.

---

## Ação 6 · FECHO (mostra e para)

**Entrega:** só a fase ou o bloco, limpo, sem tabela de gate e sem meta. Pergunta se serve e **espera o OK** antes de seguir.

**Prova forte descartada se declara na própria peça.** Se um caso, depoimento ou número de prova REAL do dono existia e ficou de fora, declare em 1 linha na própria entrega por quê. O dono precisa ver a ausência sem abrir o relato de processo. Checagem verificável antes de fechar: liste as provas reais disponíveis, uma por linha, na forma `<prova> | usada em <bloco> ou descartada porque <motivo>`, e confirme que todo descarte tem a linha correspondente dentro da entrega, não só no relato.

---

## O que esta skill NÃO faz

Cada rota é sugestão. **Se a skill irmã não estiver instalada, esta faz o mínimo aqui**, e diz em 1 linha o que ficou reduzido.

| O pedido é | Vai pra | Mínimo que faço aqui se ela faltar |
|---|---|---|
| Webinar completo ou perpétuo, com a oferta fechando metade do tempo | **soft-webinar** | não faço. Aqui é o vídeo curto que convida pra conversa |
| O deck do webinar completo, com empilhamento e preço, de 50 slides ou mais | **soft-webinar** | não faço. Aqui é o deck curto, de 12 a 20 |
| As 3 páginas do webinar (cadastro, obrigado, checkout) | **soft-webinar** | monto só a página de hospedagem do vídeo |
| Lançamento com carrinho e evento | **soft-launch** | não faço |
| Carta ou VSL em texto | **soft-funil-carta** | escrevo a versão-mestre da Ação 1, que já é a narrativa em texto corrido |
| Landing de captura ou de vendas | **soft-funil-landing** | monto a página de hospedagem pela receita da Ação 4 |
| Isca, material gratuito | **soft-funil-isca** | não faço |
| A régua de mensagens que leva ao vídeo | **soft-funil-nutricao** | escrevo a mensagem de convite, e mais nada |
| Headline isolada | **soft-conteudo-headlines** | escrevo a promessa do bloco A.1 |
| Conteúdo de feed | **soft-conteudo-*** | não faço |
| Script da conversa de venda, objeção, fechamento | **soft-vendas-closer** | não faço |
| Posicionamento, nomear mecanismo | **soft-plano-posicionamento** | uso as 6 entradas do briefing da Ação 0 |
| Arte, visual, PNG, render do deck | **soft-designer** | entrego o `.md` slide a slide, sem o visual |

## Anti-patterns (sintoma → correção)

| Sintoma | Correção |
|---|---|
| Despejou o roteiro inteiro de uma vez | Volta: uma fase por vez, com gate e parada |
| Virou aula-tutorial com passo a passo executável | Mostra resultado e função, entrega UMA virada, não a receita |
| O mecanismo não tem nome ou é coadjuvante | Nomeia o método e põe no centro. É 60% do vídeo |
| A ação fechou no checkout | Aqui a ação convida pra conversa. "Conversa, não compra" |
| Inventou número ou fala plausível | Só dado real. Sem fonte, `[A CONFIRMAR: o quê]` |
| O inimigo virou o próprio lead | Tira a culpa dele, joga a raiva pras soluções que o mercado vendeu |
| Oferta secundária ou garantia forçada | Só entra se confirmada na Ação 1. Ausência some |
| Pulou a versão-mestre e foi direto pros 12 blocos | Os blocos saem soltos. A versão-mestre é etapa própria, não parte do passo zero |
| Montou slides sem roteiro fechado | PARA e fecha o roteiro. O deck nasce do roteiro |
| O gerador de deck não estava disponível e o fluxo morreu calado | Diga em 1 linha e entregue o deck descrito no `.md`. Nunca falhe em silêncio |
| Pôs o parágrafo da fala na tela do slide | Joga pra nota. Na tela só o reforço |
| Deck inflado com empilhamento e preço | É o degrau curto, sem maquinaria de venda |
| Diagrama gigante no mecanismo | Revelação simples, peça a peça |
| Página virou vitrine pelada, sem argumento | A página leva provas, bio, perguntas frequentes e o argumento abaixo do player |
| Botão acima do player | Sempre abaixo |
| Bio no topo da página | Última dobra, empatia antes do feito |
| Urgência fabricada numa página permanente | Fecha com convicção, sem cronômetro que reinicia |
| Narrou o fluxo ("agora vou escrever a atenção") | Executa em silêncio e entrega a fase limpa |
| Imprimiu a tabela do gate | O gate é interno |

## Transversais

`references/EXEMPLO-FIM-A-FIM.md` (o caso fictício de ponta a ponta) · `references/discurso-base-7-passos.md` (a versão-mestre, Ação 1) · `references/modo-mini-webinar.md` (os 12 blocos com exemplo, o mapeamento, as indicações de gravação, o checklist antes de gravar e as 5 camadas de revisão) · `references/geracao-slides-miniwebinar.md` (Ação 3) · `references/pagina-hospedagem-rica.md` (Ação 4) · `references/tom-e-ritmo-desejo.md` (as 7 categorias de corte) · `references/conducao-na-pratica.md` (a congruência) · `shared-references/operacao-padrao.md`, `crivo/`, `filtro-anti-ia/` · `scripts/lint_copy.py` · `scripts/deck_gen.py`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **O lint é gate com código de saída, não relatório.** Rode `python3 scripts/lint_copy.py <todos os .md da entrega>; echo "exit=$?"` e cole a linha `exit=` no relatório. **`exit` diferente de 0 proíbe a entrega:** volte pro passo de escrita, conserte e rode de novo, até sair 0. Declarar que rodou o lint sem colar o veredito não conta como gate cumprido. E a frase de fecho entra na varredura junto com o resto: o CTA é o texto que mais se repete no pacote, então um molde banido ali se multiplica por todos os arquivos e pelos dados que alimentam qualquer gerador. Cole `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `shared-references/crivo/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
