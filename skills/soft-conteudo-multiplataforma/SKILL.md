---
name: soft-conteudo-multiplataforma
description: >-
  Pega uma peça que já existe e a re-renderiza pra OUTRA plataforma (LinkedIn, X, Threads, e-mail, YouTube, TikTok, Shorts, PDF) num arquivo .md, sem diluir a tese. Âncora: a peça já EXISTE e vai VIAJAR = esta skill; a peça ainda vai NASCER pro Instagram = as irmãs de conteúdo. Use quando o pedido for: "adapta esse carrossel pra LinkedIn", "transforma esse reel em thread", "vira e-mail", "repurpose", "posta isso no X também", "aproveita essa peça em outro canal", "faz a versão de newsletter", "esse post rendeu, leva pra outro lugar". NÃO use pra: escrever o CORPO ORIGINAL de carrossel (soft-conteudo-carrossel), reel (soft-conteudo-reels) ou stories (soft-conteudo-stories); a headline do zero (soft-conteudo-headlines); decidir o tema (soft-conteudo-planner); o card print de tweet em PNG (soft-tweet-card); arte e PNG (soft-designer); a apostila de uma gravação (soft-apostila); carta e página (soft-funil-carta, soft-funil-landing). Leia e siga o fluxo inteiro do SKILL.md.
---

# Multiplataforma, a mesma peça em idioma nativo

Esta skill pega uma peça que já existe e a re-renderiza no idioma nativo de outra plataforma, entregando num arquivo `.md` pronto pra publicar lá. Ela não traduz tom: extrai o núcleo e os 5 papéis da peça original e reconstrói cada papel na forma do destino.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `shared-references/crivo/07-regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Número que o perfil confirma sai em algarismo, e o extenso não é rota de fuga do gate.** Quando o gate de número não confirmado marcar um número que o perfil confirma, cole `número confirmado em <perfil:linha> · falso positivo do gate · mantido em algarismo` e mantenha o algarismo. Trocar a grafia pra passar no gate (escrever `Sessenta e três` no lugar de `63`) burla o gate: ele existe pra tirar o dado que ninguém confirmou, nunca pra mudar como o dado confirmado é escrito.

**O teto de caracteres do formato é gate.** Cole `corpo: N caracteres · teto do formato: M · dentro do teto: sim`. Peça acima do teto volta pro corte antes de sair: a plataforma corta no 'ver mais' sem ler a justificativa, e declarar o estouro não autoriza o estouro. Some: horário e janela de publicação são chutados e avisados em uma linha (`sugeri terça às 19h, mude se não servir`), nunca marcador vazio no lugar de escolha operacional.

**Capacidade negada no perfil é fato, nunca lacuna a interpretar.** Antes de escolher a mecânica do CTA, rode `grep -in 'automação\|automacao\|robô\|bot' <perfil do dono>` e cole a saída literal. Linha que diz `nenhuma automação` responde `não`, e ela não é omissão nem falso positivo a contornar. Cole `mecânica exige automação? sim/não · perfil declara: <a linha literal> · mecânica adaptada: <qual>`. Negação no perfil sai como CTA sem robô, e manter a mecânica por leitura funcional, herança de outra plataforma ou hábito presumido reprova a peça.

**A fronteira, na primeira linha:** a peça já EXISTE e vai VIAJAR, esta skill. A peça ainda vai NASCER pro Instagram, são as irmãs (**soft-conteudo-carrossel**, **-reels**, **-stories**).

**A prova e o número da peça original VIAJAM JUNTO, e não crescem.** Nenhum número, nenhuma fala e nenhum case novo aparece na versão adaptada. O que a âncora tinha, a adaptação herda literal; o que a âncora não tinha, a adaptação não inventa. Adaptar encurta, nunca enche.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra, num caso fictício de nicho neutro, a peça-âncora colada pelo dono, as perguntas que a skill fez, o mapa dos 5 papéis e duas adaptações completas escritas no formato real da entrega.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `shared-references/crivo/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a peça pronta e me diz o destino, e eu adapto). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra a adaptação com a peça e o destino que o dono já colou. Se faltar um insumo que a adaptação não vive sem (a peça original, ou pra qual plataforma vai), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez (a peça-âncora, o destino, o objetivo) antes de adaptar.

A pergunta do modo é UMA por adaptação. As outras três partes entram nos passos abaixo:

- **Ensina enquanto faz:** ao re-renderizar cada papel no idioma do destino, escreve UMA linha do porquê ("no LinkedIn abro com a tese seca, sem gancho de story, porque o feed de lá pune o clickbait e premia a afirmação forte"), pra o dono aprender a migrar sozinho na próxima.
- **Puxa o material bruto:** quando o dono mandar a peça sem contexto do destino ("põe isso no LinkedIn"), não segue no genérico. Pede o concreto: "quem lê no destino, e o que você quer que essa pessoa faça depois de ler?". O contexto do destino muda a re-renderização.
- **Oferece refinar no fim:** depois de mostrar a adaptação, fecha com UMA linha de ajuste ("quer mais curto? mais formal? outro destino da mesma peça? refaço só a versão que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Os destinos, numa tabela só (cada papel migra preservando a função)

| Destino | Capa | Capa Reserva | Contexto | Conteúdo | CTA |
|---|---|---|---|---|---|
| **LinkedIn** | 1ª linha (antes do "ver mais") | parágrafo 2 | parágrafo 3 | corpo 3 a 5 parágrafos | última linha + P.S. |
| **X / Threads** | 1º tweet | 2º tweet | 3º tweet | tweets 4 a 8 | último tweet |
| **Substack / newsletter / e-mail** | assunto (≤50 car.) + pre-header | 1ª linha | parágrafo 1 | parágrafos 2 a 4 | P.S. ou botão |
| **YouTube longo** | título + thumb | primeiros 15s | 1º minuto | corpo 3 a 8 min | chamada de inscrição |
| **PDF / Notion** | capa do doc + título | intro de 1 parágrafo | cena/dado concreto | seções principais | CTA de fechamento |
| **TikTok / Shorts** | 0 a 3s | 3 a 6s | 6 a 12s | 12 a 40s | 40 a 50s |
| **Mini Webinar** | abertura 0 a 30s | 30s a 1 min | 1 a 2 min | corpo 2 a 8 min | fechamento com convite |

**Dá pra encadear mais de uma plataforma na mesma sessão?** Dá, e é comum ("leva pro LinkedIn e pro e-mail"). A regra é a ordem, nunca o despejo: **uma plataforma por vez, com o gate rodado e o STOP do dono antes da próxima**. Você anota a fila que ele pediu, entrega a primeira, espera o OK, e só então faz a segunda. Cada destino sai no seu próprio arquivo. Nunca joga três versões de uma vez.

## O perfil do dono vem do banco do agente

Onde esta skill precisa de voz, avatar, mecanismo, campo semântico ou prova: **leia do perfil/brain do agente quando existir**; se não existir, use o que a peça-âncora já carrega e marque o resto `[DADO: confirmar]`. Nunca invente, nunca crie um arquivo de perfil.

## O bloco da ação (esta skill tem uma ação só: adaptar uma peça pra um destino)

**O que faz:** re-renderiza uma peça-âncora no formato e no idioma nativos de uma plataforma de destino, preservando a tese e os 5 papéis.

**Precisa de:** a **peça-âncora** colada pelo dono (carrossel, reel, story, carta, post pronto) · o **destino** · a **preferência do dono** pro destino (duração, formato, tom) · o verbatim que sustenta a âncora, do perfil/brain do agente.

**Sem o insumo:**
- **Sem peça-âncora:** pergunta numa mensagem só, "qual peça você quer adaptar, e pra qual plataforma?", e PARA. Sem âncora não há o que adaptar, e esta skill não escreve peça do zero.
- **Sem destino declarado:** pergunta UMA vez, com a tabela de destinos acima como cardápio.
- **Sem preferência declarada:** pergunta a que muda a peça naquele destino. YouTube, qual duração e formato (corte curto ou aula longa)? E-mail, mais pessoal ou mais direto? LinkedIn, primeira pessoa ou caso de terceiro? Uma pergunta por destino, não um questionário.
- **Sem verbatim por trás da âncora:** mantém o que a âncora já tinha e marca todo número não confirmado como `[DADO: confirmar]`. Não conta como ancorado.
- **Se um dos 6 componentes do núcleo sumiu na âncora** (problema, método nomeado, vilão-categoria, CTA filtrante, os movimentos de persuasão, campo semântico): pergunta antes de adaptar. Adaptar com núcleo incompleto produz peça fraca.

**O CTA é o papel que MAIS muda entre plataformas, e a palavra-chave quase nunca sobrevive.** Pra cada destino, escreva no mapa dos 5 papéis: `mecânica do CTA na âncora: <qual> · existe nesta plataforma? sim/não · o dono tem a automação que ela exige? sim/não · CTA adaptado: <literal>`. Comentário-para-direct com palavra-chave só sobrevive onde há automação declarada no perfil do dono; sem ela, o CTA vira a ação nativa da plataforma (no LinkedIn, responder ao post ou mandar mensagem; no e-mail, responder a mensagem; na newsletter, o link). Copiar a palavra-chave de uma plataforma pra outra sem essa linha reprova a adaptação, porque manda o leitor digitar uma palavra que ninguém do outro lado está esperando.

**E a palavra-chave em si não se inventa: quem confere é o script.** Rode, antes de mostrar qualquer peça:

```
python3 scripts/checar_titulos.py --peca <cada peça adaptada> \
  --insumos <pasta de insumos do dono> --perfil <perfil do dono>
```

Ele extrai as palavras em CAIXA ALTA dos CTAs das peças, cruza com o grep nos insumos do dono, e sai com **exit 1** em `palavra-chave inventada: <X>`. Também imprime `automação declarada no perfil: sim/não`, e palavra-chave no CTA sem automação declarada reprova, mesmo quando a palavra existe no disco. Cole `palavra-chave: <literal> | origem: <arquivo:linha>`, ou `palavra-chave: nenhuma (CTA sem palavra)`. A grafia é a EXATA: "BASE", "BASE 40" e "BASE40" são três palavras diferentes pra quem digita, e quem digita a errada cai em lugar nenhum. Trocar a palavra do dono por outra mais bonita é o defeito, não a adaptação: a palavra é um endereço, não copy.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** um arquivo por destino, `[peça]-[destino].md`, com o **mapa dos 5 papéis** no topo (o que da âncora virou o quê) e a versão adaptada embaixo, no formato nativo. No YouTube longo, o doc traz também o pacote de publicação (título, descrição, capítulos, tags, sugestão de thumbnail). Em ambiente que renderiza markdown, mostre o doc renderizado; com sistema de arquivo, salve o `.md`; num agente de mensageria, grave o arquivo e cite o path completo. **STOP** por destino.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `shared-references/crivo/07-regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** a reference do destino (`references/plataforma-linkedin.md` · `plataforma-x-threads.md` · `plataforma-substack-email.md` · `plataforma-tiktok-shorts.md` · `plataforma-youtube-longo.md` · `plataforma-pdf-notion.md` · `plataforma-mini-webinar.md`) · `references/nucleo-soft-extracao.md` (o protocolo de extração do núcleo).

**Profundidade:** `references/estrutura-peca.md` (a base da engenharia reversa dos 5 papéis) · `references/processo-multiplataforma.md` (o processo completo com mais formato e exemplo) · `references/conducao-na-pratica.md` (quando a adaptação está certa e sem alma).

Passos: 0 (ancora) → 1 (âncora e destino) → 2 (extrai o núcleo) → 3 (mapeia os 5 papéis) → 4 (re-renderiza) → 5 (gate por dentro) → 6 (mostra e PARA).

---

## Por que adaptar não é traduzir (a doutrina, em 4 linhas)

Adaptar é fazer engenharia reversa da peça, não traduzir o tom dela. Você pega uma peça deste método que já funcionou, extrai os 5 papéis e o núcleo dela, e re-renderiza no formato do destino preservando a função de cada parte. Se a versão adaptada parece igual a qualquer post daquela plataforma, falhou: perdeu o filtro. O que viaja entre plataformas é a TESE e os 5 papéis; o que muda é só o tempo de exposição e a unidade de entrega.

**O que esta skill faz por você:** pega uma peça que já funcionou e a leva pra outra plataforma (LinkedIn, X, YouTube, email, newsletter) sem perder a tese, falando o idioma nativo de cada uma. É como você multiplica uma ideia boa sem reescrever do zero.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa de você a preferência (duração, formato, tom) antes de gerar; (4) contexto é rei; (5) **admite se faltar insumo, nunca inventa**: confere se tem a peça-âncora/o número/o case antes de adaptar e, se faltar, marca `[DADO: confirmar]` no lugar do furo e diz o que falta, jamais preenche com algo plausível; (6) **doc de output enxuto pros 2 leitores**: o que sai é otimizado pro humano que lê E pra IA que recebe como contexto: só a versão adaptada limpa + `[DADO: confirmar]`, zero meta-narração. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar a versão adaptada.**

## Output Contract (o que você entrega)
- **Uma versão adaptada por vez**, da peça-âncora pro destino pedido, com o **mapa dos 5 papéis no original** (o que vira o quê) impresso antes da peça.
- A versão sai no **formato e idioma nativos do destino** (subject+pre-header no email, thread numerada no X, primeira-linha-antes-do-ver-mais no LinkedIn, título+capítulos no YouTube).
- O gate roda **por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída. Versão que falha no gate não sai.
- Você **para e espera** o OK antes de adaptar pra um segundo destino ou gerar variação.
- Você **nunca inventa fala nem número do cliente** e **nunca dilui a tese pra caber no formato**.

## Passo 0, ancora antes de adaptar (NÃO PULE)
O fluxo assume que a peça-âncora já passou pelo gate dela. Confirma duas coisas antes de mexer:
- **A headline/abertura já está escolhida?** Você adapta a partir de uma peça pronta, não cria a peça do zero. Se a âncora existe mas ainda não tem headline aprovada, você escreve a headline AQUI pela régua de título que esta skill carrega (`shared-references/crivo/07-regua-de-titulos.md`) e segue. Quem quer um banco maior de variações pode passar pela soft-conteudo-headlines, mas isso é opção, a headline se resolve aqui.
- **Onde está o verbatim real?** Procura a fonte de fala do cliente nesta ordem: descrição do projeto → Plano colado → mensagens anteriores. A peça adaptada herda a mesma âncora; nenhuma fala ou número novo aparece sem fonte.

Três estados de entrada (declara qual é o seu antes de adaptar):
- **Peça-âncora colada + verbatim com N:** caminho ideal. Adapta preservando a fala literal e o N real.
- **Peça-âncora colada, mas sem a fala literal por trás:** mantém o que a âncora já tinha; qualquer número que você não confirmou entra como `[DADO: confirmar]` e **NÃO conta como Ancorada=✓**.
- **Nada colado:** pergunta numa única mensagem ("qual peça você quer adaptar, e pra qual plataforma?") e para. Sem peça-âncora não há o que adaptar.

## Passo 1, identifica a peça-âncora e o destino
- **Âncora:** o que foi colado? Carrossel, reel, story, carta, post pronto. Anota o tipo.
- **Destino:** se não disseram, pergunta UMA vez: "Pra qual plataforma? LinkedIn, X/Threads, Substack/email, YouTube, newsletter, PDF/Notion?" e para.
- **Preferência do especialista (Lei 3, consultiva):** puxa como ELE quer a peça no destino antes de gerar. Ex.: YouTube, que duração e formato (corte curto, aula longa)? Email, mais pessoal ou mais direto? Não sai gerando sem extrair a ideia que está na cabeça dele.
- Regra de fundo: o formato não muda a arquitetura. Muda o **tempo de exposição** (3s de capa vira primeira linha do LinkedIn) e a **unidade de entrega** (slide vira parágrafo, vira tweet, vira minuto de vídeo).

## Passo 2, extrai o núcleo da peça da âncora (interno, antes de re-renderizar)
Antes de traduzir, escreve internamente os **6 componentes do núcleo** que viajam inalterados (detalhe + checklist pós-extração em `references/nucleo-soft-extracao.md`):
- **Problema Sofisticado (3ª Camada):** a dor real nomeada como inimigo-categoria, nunca defeito do cliente.
- **Método com nome próprio:** sempre nomeado, mesmo em 280 caracteres.
- **Vilão-categoria:** a prática/sistema/crença atacada, nunca pessoa ou marca.
- **CTA filtrante:** pra onde o lead vai (Direct com palavra, comentário, reply do email); nunca "curte e compartilha".
- **≥3 dos 5 movimentos Blair Warren:** incentiva sonho · justifica falha · aplaca medo · confirma desconfiança · atira pedra no inimigo. Princípio de fundo, nunca lista citada na peça.
- **Campo semântico do cliente:** vocabulário do nicho, nunca "lead/funil/conversão"; monta a tabela de tradução antes de adaptar.

A **prova específica** real da âncora (número/cena) viaja junto. Se algum dos 6 sumiu na âncora, pergunta antes de adaptar. Adaptar com núcleo incompleto produz peça fraca.

## Passo 3, mapeia os 5 papéis da Estrutura-Mãe no original
Identifica qual trecho da âncora faz cada papel. Isso é o mapa que você imprime no Passo 5.

1. **Capa** (o que parou o leitor)
2. **Capa Reserva** (o que aprofundou o loop)
3. **Contexto** (como o leitor foi aterrado)
4. **Conteúdo** (a virada + o método via contraste)
5. **CTA** (a ação filtrante)

Anti-padrão: traduzir cada slide em 1 parágrafo/tweet sem repensar os papéis. O carrossel tem N slides, mas os 5 papéis não são N unidades: alguns papéis ocupam vários slides (Conteúdo), outros colapsam (Capa + Capa Reserva num formato curto). Adaptação fiel preserva os **papéis**, não o número de unidades.

## Passo 4, re-renderiza no idioma nativo do destino
Usa a **tabela de destinos do topo desta skill** como ponto de partida. Cada papel migra preservando a função, no formato do destino.

**Abre a reference da plataforma e segue as regras nativas dela** (formato, limites, exemplos, SEO/UTM). Não adapta de cabeça: a reference tem as regras que mudam a peça:
- LinkedIn → `references/plataforma-linkedin.md` · X/Threads → `references/plataforma-x-threads.md` · Substack/Email → `references/plataforma-substack-email.md`
- TikTok/Shorts → `references/plataforma-tiktok-shorts.md` · YouTube longo → `references/plataforma-youtube-longo.md` (traz o **pacote completo de publicação**: título, descrição, tags, capítulos, thumbnail, SEO, UTM)
- PDF/Notion → `references/plataforma-pdf-notion.md` · Mini Webinar → `references/plataforma-mini-webinar.md` (distribuição/hospedagem; a construção do roteiro é da `soft-funil-*`)

**Idioma nativo, não copia-cola do Instagram.** LinkedIn e email são armadilha pra jargão de marketing: zero "lead/funil/ticket/conversão", sempre o campo semântico do cliente final. No formato curto (tweet único, email brevíssimo), papéis podem colapsar de propósito (Manifesto = Capa+CTA · Sentença = só Capa · Único = 1 unidade faz tudo). Colapso consciente não é traição da estrutura; perder um papel sem querer, sim.

**Se o destino for YouTube longo**, entrega também o pacote de publicação: título, descrição, capítulos, tags, sugestão de thumbnail.

## Passo 5, roda o GATE por dentro (auditoria silenciosa, NÃO imprime)

**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`shared-references/crivo/07-regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo.

**Marcador da âncora NÃO se herda.** A peça de origem é rascunho; a adaptação é publicação, e o que saiu daqui é o que o público lê. Copiar `[DADO: confirmar número exato de semanas]` do miolo de uma frase de prova só porque a âncora o tinha entrega ao público a pendência do dono. Para CADA marcador da âncora há duas saídas e nenhuma terceira: **reescrever a frase sem o dado**, ou **tirar a frase**. Rode `grep -nE '\[(A CONFIRMAR|DADO|CONFIRMAR)' <âncora>` e cole a saída antes de adaptar, depois feche com `marcadores na âncora: N · resolvidos por reescrita: N · removidos: N · copiados: 0`. Valor maior que zero em `copiados` reprova a adaptação.

**Frase genérica se corrige com CENA, nunca com adjetivo.** Quando uma frase sobrevive à troca de nicho, a correção não é somar um adjetivo forte nem trocar o verbo: é **substituir o substantivo abstrato** (obstáculo, desculpa, consistência, movimento, plano, jornada, transformação) por uma cena que só existe neste negócio. As cenas estão nos insumos e não na sua cabeça: **liste as disponíveis ANTES de escrever**, rodando o grep abaixo sobre a pasta de insumos e colando a saída.

```
grep -rniE 'quando eu|toda vez que|no dia|a hora que|eu vi|eu percebi|me disse|escreveu' <pasta de insumos>
```

Cole a lista na forma `cena: <descrição em 6 palavras> | origem: <arquivo:linha>`, uma por linha, e marque quais foram usadas na peça. Feche com `cenas disponíveis: N · usadas na peça: N`. Peça com `usadas: 0` e insumos com cena disponível volta pro passo de escrita: a frase morna não é falta de talento, é a cena que estava no disco e ninguém abriu.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória** (`shared-references/crivo/08-consentimento.md`, os 3 passos): (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

Roda o gate na versão adaptada **internamente** (auditoria silenciosa). Só versão com VEREDITO=PASSA vai pro cliente. Um ✗ refaz. A tabela abaixo é o teu **checklist interno**, nunca a saída: o usuário recebe só a versão limpa (Passo 6), jamais a tabela. A âncora já passou no gate dela; a adaptação passa de novo no idioma novo.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorada** | herda fala literal/N **real** da âncora OU prova real do autor; **N inventado/plausível = ✗ automático**; fecha em chão/número/cena, não em tese solta bonita | |
| **Tese preservada** | a percepção central da âncora chegou inteira; **não foi diluída pra caber no formato** (encurtar ≠ esvaziar) | |
| **Nada sem lastro na âncora** | escassez, prazo, vaga, lista de espera e número que não estão na peça-fonte nem no perfil do dono **não entram**, mesmo em PS, mesmo em assunto de e-mail, mesmo como "só pra fechar". Adaptar é vestir a mesma tese no idioma do destino, nunca acrescentar promessa que o dono vai ter que sustentar depois. Checagem: para cada urgência, prazo ou número da adaptação, aponte a linha da âncora de onde saiu; sem linha apontada, corta | |
| **Nativo do destino** | formato e vocabulário são da plataforma alvo (subject/thread/1ª-linha/capítulos certos), **não um copia-cola do post do Instagram** | |
| **5 papéis re-renderizados** | os 5 papéis aparecem (ou colapsam de propósito, declarado); **nenhum papel sumiu por acidente** | |
| **CTA com destino** | filtrante e direcional no idioma do destino (Direct/comentário/reply/botão), **nunca "curte e compartilha"** | |
| **Confuso? (C)** | leigo do nicho entende na 1ª passada, sem reler | |
| **Inacreditável? (U)** | promessa/número soa crível, não exagero de guru | |
| **Chato? (B)** | tem cena/tensão/opinião; não é parágrafo morno informativo | |
| **As 3 perguntas, dá pra ver?** | fecha o olho e enxerga a cena. ✗ "tenha mais clareza" · ✓ "a recepcionista diz: semana que vem enche" | |
| **As 3 perguntas, dá pra falsificar?** | é fato falsificável, não adjetivo | |
| **As 3 perguntas, só você diz?** | o concorrente direto não assina igual (cena/mecanismo proprietário, não promessa banal do nicho) | |
| **Anti-IA (HARD)** | zero travessão longo (U+2014) · zero da família do verbo-freio banida pela régua anti-voz, o verbo que rima com "cravar" e suas flexões (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê de hype (o "revoluciona/transforma" e o próprio verbo-freio banido). **No chat (sem o lint), faz um CTRL+F manual do travessão longo (U+2014) e a família do verbo-freio banida antes de marcar ✓.** | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

## Passo 6, mostra e PARA
Mostra **só a versão que passou, LIMPO**, no doc: a peça adaptada no formato e idioma nativos do destino. Sem tabela de gate, sem meta. Pergunta "essa serve? ajusto, ou adapto pra outra plataforma?". **Espera o OK** antes de adaptar pro próximo destino ou gerar variação. Uma plataforma por vez, nunca despeja todas de uma vez.

## O que esta skill NÃO faz (e pra onde vai)

Esta skill re-renderiza uma peça que JÁ EXISTE e para aí. Em toda rota abaixo, se a skill de destino não estiver instalada, esta faz o mínimo aqui e diz o que fez.

| O pedido é | Vai pra | Se não estiver instalada |
|---|---|---|
| O **CORPO ORIGINAL** de um carrossel pro Instagram | **soft-conteudo-carrossel** | adapta a partir do que o dono colar; sem âncora, para e pede a peça |
| O **roteiro original** de um reel | **soft-conteudo-reels** | idem: sem âncora, para e pede a peça |
| A **sequência original** de stories | **soft-conteudo-stories** | idem |
| A **headline/gancho do zero** | **soft-conteudo-headlines** | usa a capa que a âncora já tem e a re-renderiza no teto do destino |
| Decidir **sobre o que postar** (tema da semana ou do mês) | **soft-conteudo-planner** | pergunta ao dono qual peça ele quer levar adiante |
| **Arte, PNG, visual** da versão adaptada | **soft-designer** | entrega só o texto e diz que a arte fica pendente |
| **Posicionamento, mecanismo, pilares** | **soft-plano-posicionamento** | usa o que a âncora carrega e marca o resto `[DADO: confirmar]` |
| **Carta, página de vendas, VSL, micro-aula** | **soft-funil-carta** / **soft-funil-landing** / **soft-funil-miniwebinar** | adapta só o conteúdo e aponta o que falta |

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Traduziu cada slide em 1 parágrafo/tweet sem repensar os papéis | Mapeia os 5 papéis primeiro; re-renderiza por função, não por unidade |
| Encurtou pra caber e a tese virou frase morna | Tese preservada = ✗; reescreve mantendo a percepção central inteira |
| Versão de LinkedIn/email com cara de post do Instagram | Idioma nativo do destino (subject, 1ª linha, thread); zero copia-cola |
| Vazou "lead/funil/conversão" no LinkedIn ou no email | Volta pro campo semântico do cliente final |
| CTA virou "curte e compartilha" | CTA filtrante com destino (Direct/comentário/reply/botão) |
| Sumiu um papel sem querer (Contexto evaporou) | 5 papéis re-renderizados = ✗; recoloca o papel ou declara o colapso |
| Inventou um número/fala "plausível" na adaptação | Só herda número/fala REAL da âncora; sem fonte, `[DADO: confirmar]` e não conta como Ancorada=✓ |
| Despejou LinkedIn + X + email de uma vez | Uma plataforma por vez, com gate, e PARA pro OK |
| Narrou o fluxo ("agora vou extrair o núcleo") | Não narra: executa em silêncio e entrega só o mapa + a versão limpa, sem a tabela do gate |
| Gerou a adaptação sem perguntar a preferência do especialista | Consultiva (Lei 3): extrai duração, formato e tom desejado antes de re-renderizar |
| Imprimiu a tabela do gate na saída | O gate é INTERNO (auditoria silenciosa); a saída é só a peça limpa |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `shared-references/crivo/07-regua-de-titulos.md`: **a régua de títulos** (as 7 regras que decidem se um título existe: teste do enunciado, proibição do título que só descreve, teses contadas, inimigo ou inversão, cota de antítese, crivo clínico e regulado, assinatura de copywriter), mais o gatilho nomeado, a contagem física e as 3 melhores marcadas.
- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta (a entrada do dono, as perguntas feitas e a saída real de cada ação). **Leia antes da primeira pergunta.**
- `references/processo-multiplataforma.md`: a engenharia reversa completa, a tabela de mapeamento com TikTok/Shorts e Mini Webinar, e os colapsos conscientes detalhados. É o mesmo processo, com mais formato e exemplo.
- `references/nucleo-soft-extracao.md`: o protocolo de extração do núcleo do Passo 2, com os 6 componentes e o checklist pós-extração.
- `references/conducao-na-pratica.md`: o porquê por trás (conteúdo reorganiza percepção, não dá passo a passo; estoura a bolha; polariza; aponta sempre pro método). Lê quando a adaptação está tecnicamente certa mas sem alma.
- `references/estrutura-peca.md`: a Estrutura-Mãe dos 5 papéis (Capa · Capa Reserva · Contexto · Conteúdo · CTA) com as formas de cada um. É a base da engenharia reversa do Passo 3.
- **Uma reference por plataforma (dirigidas no Passo 4):** `references/plataforma-linkedin.md` · `plataforma-x-threads.md` · `plataforma-substack-email.md` · `plataforma-tiktok-shorts.md` · `plataforma-youtube-longo.md` (com o pacote de publicação) · `plataforma-pdf-notion.md` · `plataforma-mini-webinar.md`. Cada uma traz regras de formato, exemplos e checklist nativos do destino.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.
