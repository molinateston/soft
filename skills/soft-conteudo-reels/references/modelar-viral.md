# Modelar um viral · dissecar por segundo e re-renderizar na tua voz

> **Dirigida pelo "Modo Modelar um viral" do SKILL.md.** Modelar aqui é o mesmo princípio da doutrina Soft: estudar a referência = extrair a PREMISSA (por que aquilo prende), nunca decalcar. Você não copia o roteiro do outro; você decompõe a engenharia dele por segundo, entende o que fez o scroll parar, e re-renderiza a estrutura no teu tema, na tua voz, com a tua prova. O resultado é um reel teu, autoral, que aproveita uma estrutura já provada de atenção.

## Índice
- 1. Quando esse modo entra (e quando não)
- 2. Os 3 ambientes (o que muda em cada um)
- 3. O protocolo de dissecação por timestamp (o checklist do que extrair)
- 4. Como transcrever o viral (a infra Apify + Whisper, ramo Claude Code / agente)
- 5. Ler a análise e virar premissa (não decalque)
- 6. As regras de roteiro que o viral confirma (reforçam o nosso método)
- 7. Fechar no gate de sempre (descarta a nota 95/100)
- 8. Exemplo denso, do link ao roteiro

---

## 1. Quando esse modo entra (e quando não)

Esse é um **modo opcional** da soft-conteudo-reels. Ele dispara quando o dono:
- cola a **URL de um reel de referência** (dele ou de fora) e diz "modela esse", "faz um parecido", "quero um reel na estrutura desse";
- aponta uma **base de referências** (anotações, pasta de reels salvos) e pede pra puxar a estrutura de um deles.

O fluxo normal da skill (headline do Passo 0 → APSD → gate) continua sendo o padrão. O modo modelar é um **atalho de estrutura**: em vez de partir do zero, você parte de uma espinha de atenção que já provou funcionar, extrai a premissa dela, e enche com o TEU conteúdo. Depois disso, o roteiro volta pro trilho normal e passa pelo mesmo gate.

**Quando NÃO usar esse modo:**
- Se o dono não tem referência e só quer um reel sobre um tema: fluxo normal, ignora esse arquivo.
- Se o "viral" de referência é de um concorrente direto e a estrutura é a identidade dele (bordão, formato-assinatura): modela a MECÂNICA de atenção, nunca o traço que só ele assina. Reel que parece cópia do concorrente queima reputação.
- Se a captura/transcrição falhar: **relata a falha e para. Nunca inventa a análise.** Uma transcrição inventada envenena o roteiro inteiro (é a Lei 5, admite se faltar insumo).

---

## 2. Os 3 ambientes (o que muda em cada um)

O mesmo pedido roda diferente conforme onde a skill está rodando. Declara qual é o ambiente antes de prometer captura automática.

**app / claude.ai (sem Bash):** você NÃO baixa nem transcreve o vídeo sozinho. Duas saídas honestas:
1. Pede ao dono pra **colar a transcrição** do reel (ele pode tirar das legendas/CC ou digitar o que é falado) e o print dos números (views, curtidas, comentários). Com o texto na mão, você faz toda a dissecação por timestamp aproximado, extrai a premissa e escreve o roteiro novo.
2. Se ele só tem o link e não a transcrição, você conduz pela ESTRUTURA visível (gancho que ele descreve, o que ele lembra da ordem) e avisa que a análise fica mais rasa sem a transcrição literal. Nunca finge que "assistiu" o vídeo.

**Claude Code (tem Bash, pipeline completo):** roda o pipeline inteiro (Seção 4): Apify pega o `videoUrl`, ffmpeg extrai o áudio, Groq Whisper transcreve, você disseca o texto por timestamp. Entrega o roteiro como arquivo `.md`.

**agente / Telegram (tem Bash, entrega é ARQUIVO):** roda o mesmo pipeline da Seção 4. A diferença é a ENTREGA: o roteiro final vai como **arquivo** e a resposta ao dono traz o **caminho completo do arquivo** (ex.: `/home/cloud/reels-modelados/reel-diagnostico-vende.md`), com as mensagens no chat em texto limpo, sem markdown pesado (sem tabela, sem bloco de código gigante despejado no Telegram). O dono abre o arquivo pra ver o roteiro rotulado; o chat carrega só o resumo e o path.

---

## 3. O protocolo de dissecação por timestamp (o checklist do que extrair)

Esse é o coração do modo, o que vale ouro: um **checklist frio do que ler num viral**, segundo a segundo. Não é opinião ("gostei do começo"), é engenharia (o que exatamente ele fez pra prender). Aplica esse checklist sobre a transcrição (Claude Code / agente) ou sobre a transcrição colada (app).

Extrai, na ordem:

**Transcrição por timestamp**
- Cada frase falada com a marca de tempo aproximada `[0:00]`, `[0:04]`, `[0:09]`... Não precisa de precisão de milissegundo; precisa da SEQUÊNCIA e do RITMO (quanto tempo cada bloco leva).

**Gancho (os 3 primeiros segundos)**
- As primeiras palavras ditas, exatas.
- Quantas palavras tem o gancho (conta de fato, não estima).
- O que faz o scroll parar? (número · quebra de padrão · promessa · confissão · imagem inesperada) Nomeia o gatilho.
- Ele abre com "Eu"? (se sim, é fraco; o nosso método nunca abre com "Eu".)

**Padrões de linguagem**
- Comprimento médio das frases (curtas e secas? longas?).
- Proporção **você/seu** vs **eu/meu** (viral de atração fala mais com "você" do que sobre "eu").
- Como ele faz as transições entre um ponto e o próximo (cada frase abre a próxima? tem tensão contínua?).
- Onde estão os minimizadores tipo "só", "basta", "simplesmente" (dão tom de simplicidade radical).

**Estrutura**
- Duração total.
- Quebra por seções com os tempos: gancho → tensão → ponto 1 → (ponto 2) → fechamento → CTA.
- Qual é o momento de **antes/depois** (o contraste que ele mostra)?
- Qual é o CTA e pra onde ele manda (comentar palavra · salvar · perfil)?
- Quantos pontos-chave ele carrega? (viral bom carrega 1 a 2, não 3; mais que isso vira aula pesada.)

**A sacada-chave**
- A ÚNICA técnica mais importante desse reel, a que você levaria pro teu. Uma frase. É a premissa que você vai importar; o resto é contexto.

Esse bloco vira um arquivo de análise (`analise-referencia-[slug].md` no Claude Code / agente) ou um resumo no chat (app). É insumo, não entregável final.

---

## 4. Como transcrever o viral (infra Apify + Whisper, ramo Claude Code / agente)

**Não usamos serviço de análise de vídeo por LLM multimodal.** A nossa infra transcreve o ÁUDIO e disseca o TEXTO. A perda: você não lê o visual automaticamente (cortes, texto na tela, b-roll); pega isso pela legenda/descrição ou pergunta ao dono. A vantagem: roda com o que já temos, sem depender de chave de terceiro que costuma estar morta.

O pipeline (já provado na nossa operação de transcrição de Instagram, `/home/cloud/insta-transcricoes`):

1. **Pega o `videoUrl`** com o Apify actor `apify/instagram-scraper` (assíncrono: POST no run, poll até `SUCCEEDED`, puxa o dataset). Token `APIFY_TOKEN` no `/home/cloud/.openclaw/.env`. Input mínimo: `{directUrls:[URL], resultsType:"posts", resultsLimit:1}`. Do item retornado, extrai `videoUrl` e os números (`videoViewCount`, `likesCount`, `commentsCount`, primeiros 200 caracteres da `caption`).
   - Molde pronto: `/home/cloud/insta-transcricoes/scrape.sh <saida.json> <url> '{"resultsLimit":1}'`.
2. **Extrai o áudio** com `ffmpeg -nostdin` (o `-nostdin` é obrigatório, senão o ffmpeg devora o stdin do laço e trunca o próximo item). Mono, 16 kHz, mp3.
3. **Transcreve** com Groq Whisper (`whisper-large-v3`, `language=pt`, `response_format=json`), chave `GROQ_API_KEY` no mesmo `.env`. O free tier tem RPM baixo: o backoff precisa **respeitar o "try again in Xs"** que a API devolve, senão estoura o limite.
   - Molde pronto: `/home/cloud/insta-transcricoes/transcribe.sh <dir>` (lê `<dir>/select.tsv` com `shortcode<TAB>videoUrl`, cospe `<dir>/txt/<shortcode>.txt`). Sequencial de propósito (a CDN do IG bloqueia download concorrente). Idempotente.
4. **Confere antes de dissecar:** tamanho do arquivo de áudio > 0, transcrição não vazia, números batem com o que o dono espera. Se qualquer passo falhar nas tentativas, **relata e para** (Seção 1).

Com a transcrição na mão, aplica o checklist da Seção 3.

---

## 5. Ler a análise e virar premissa (não decalque)

Aqui é onde o modo modelar honra a doutrina Soft: **você importa a PREMISSA da estrutura, não o roteiro.** Pega a sacada-chave (Seção 3) e as regras de estrutura (quantos pontos, onde o antes/depois, como o gancho prende) e mapeia pro TEU tema.

O que você transporta do viral:
- a **forma do gancho** (se ele abriu com número, você abre com número TEU; se abriu com confissão, você confessa algo TEU);
- o **ritmo** (frase curta que abre a próxima, tensão que não relaxa);
- a **arquitetura de seções** (gancho → tensão → 1-2 pontos → fechamento → CTA), que é a nossa espinha APSD comprimida;
- o **tipo de CTA** (comentar palavra, salvar), adaptado ao destino do teu funil.

O que você NÃO transporta:
- o **conteúdo** dele (o teu vem da tua prova real, do teu verbatim, do teu mecanismo);
- **número, case ou fala** dele: número/experiência de terceiro NUNCA vira fato do teu método. Se a estrutura do viral dependia de "eu faturei X", a tua versão usa o TEU número real ou entra `[DADO: confirmar]`, jamais o número dele reaproveitado;
- o **traço-assinatura** dele (bordão, formato que só ele usa), que denunciaria cópia.

Regra de ouro da doutrina: a engenharia da estrutura é universal, só troca as variáveis. Um reel de nutrição "3 alimentos que parecem saudáveis mas emperram o intestino" vira, no teu nicho de gestão, "3 relatórios que parecem controle mas escondem o rombo". Mesma espinha, conteúdo 100% teu.

---

## 6. As regras de roteiro que o viral confirma (reforçam o nosso método)

Modelar vários virais mostra sempre os mesmos padrões, e eles batem com o que a soft-conteudo-reels já prega. Quando escrever o roteiro novo, reforça:

- **Nunca abre com "Eu".** Usa "isso", "você", um fato, um número ou um nome. Gancho que começa em "eu" fala de você antes de dar motivo pro leitor ficar.
- **Gatilho de comentário = UMA palavra em maiúscula**, sem aspas, sem "abaixo", sem pontuação no fim (ROTEIRO, GUIA, MAPA). Precisa ligar direto com o que foi prometido.
- **No máximo 2 pontos-chave, não 3.** Três pontos viram aula e pesam; dois prendem.
- **A legenda espelha o roteiro.** Atualiza os dois juntos; legenda que fala outra coisa quebra a promessa.
- **Frase curta, cada uma abre a próxima**, tensão que não relaxa (se o leitor prevê a próxima frase, pula).
- **Sem "link na bio".** O destino é comentário/salvar/carrossel, um próximo passo real do funil.

Essas regras já vivem no corpo do SKILL.md; o modo modelar só as confirma com prova de campo.

---

## 7. Fechar no gate de sempre (descarta a nota 95/100)

O roteiro que sai do modo modelar **passa pelo MESMO gate do Passo 5 do SKILL.md** (Ancorado, Um ponto só, 3 tipos de gancho, Tensão contínua, Lo-fi, Espinha APSD, CTA com destino, Dá pra ver, Dá pra falsificar, Só você diz, C/U/B, Anti-IA HARD). Um ✗ refaz o ponto que falhou.

**Não usa nota numérica tipo "95/100".** Nota inflada é teatro: dá sensação de rigor sem dizer o que está errado. O nosso veredito é binário e honesto, **PASSA ou REFAZ**, e o REFAZ aponta exatamente qual item falhou. Se o roteiro modelado não passa no Ancorado (porque só tinha número do viral, não teu), ele REFAZ, não "tira 88".

Cuidado extra no modo modelar, dois ✗ que aparecem muito:
- **Ancorado ✗** porque o roteiro herdou o número/case do viral. Troca por prova tua ou `[DADO: confirmar]`.
- **Só você diz ✗** porque ficou parecido demais com o original. Reescreve até a estrutura sumir dentro da tua voz.

---

## 8. Exemplo denso, do link ao roteiro

**Entrada (Claude Code):** dono cola `https://www.instagram.com/reel/ABC123/` e diz "modela esse pro meu nicho de consultoria financeira pra clínicas".

**Pipeline (Seção 4):** Apify devolve `videoUrl` + 412 mil views, 9,1 mil curtidas, 380 comentários, legenda "o erro que quebra 8 em cada 10 clínicas". ffmpeg + Whisper transcrevem.

**Dissecação (Seção 3), resumida:**
- Transcrição por tempo: `[0:00]` "8 em cada 10 clínicas fecham no terceiro ano." `[0:03]` "E não é falta de paciente." `[0:06]` "É isso aqui..." (mostra planilha) `[0:14]` "O dono olha o faturamento e acha que tá indo bem." `[0:22]` "Mas o dinheiro que entra não é o dinheiro que fica." `[0:30]` "Comenta CAIXA que eu te mando o mapa."
- Gancho: "8 em cada 10 clínicas fecham no terceiro ano", 9 palavras, gatilho = número + choque de futuro. Não abre com "Eu". ✓
- Linguagem: frases curtas, mais "você/o dono" que "eu", minimizador ausente, transição por tensão ("e não é... é isso aqui").
- Estrutura: gancho (0-3) → tensão (3-6) → diagnóstico com visual (6-22) → virada (22-30) → CTA de comentário (30-33). 1 ponto-chave. Antes/depois = "faturamento parece bom" vs "dinheiro não fica".
- Sacada-chave: **o gancho é uma estatística de mortalidade + a negação imediata da causa óbvia** ("e não é falta de paciente"), que abre o loop na hora.

**Premissa importada (Seção 5):** estatística de fracasso do nicho + negar a causa óbvia + revelar a causa real com um visual + CTA de uma palavra. Zero conteúdo do original reaproveitado; o número 412 mil e o "8 em cada 10" ficam LÁ, não vêm pro meu roteiro.

**Roteiro novo (na voz do dono, tema consultoria financeira pra clínicas):**
- **[0:00-0:03] GANCHO (Atenção).** Fala: "Clínica que fatura R$120 mil por mês e não sobra nada no fim." Texto na tela: "R$120 mil e zero de sobra". `[DADO: confirmar o número que o dono usa de exemplo real]`
- **[0:03-0:07] TENSÃO (quebra de crença).** "E não é preço baixo. Não é falta de agenda." Abre o loop, nega a causa óbvia.
- **[0:07-0:18] DIAGNÓSTICO (vilão).** "O dono olha o faturamento cheio e acha que o negócio tá de pé. Só que faturamento não é lucro. O que entra sai antes dele ver." O modelo velho (confundir faturar com lucrar) é o culpado, não o dono.
- **[0:18-0:25] VIRADA (nova oportunidade).** "Existe um jeito de enxergar quanto de cada real fica com você, antes de gastar." Mostra que dá pra ver diferente.
- **[0:25-0:30] MECANISMO (função, não execução).** "É separar o dinheiro por função assim que entra. Sem isso, todo mês é adivinhação." Aponta pro método sem entregar o passo a passo.
- **[0:30-0:33] CTA (Ação, destino real).** "Comenta CAIXA que eu te mando o mapa de como fazer isso na sua clínica." (comentar = próximo passo do funil)

**Legenda (espelha):** "Faturar muito e não sobrar nada é o retrato de 8 em cada 10 clínicas. O problema quase nunca é o que parece. Comenta CAIXA."

**Gate (Seção 7):** roda o gate do Passo 5 por dentro. Ancorado depende do número real do dono, que entrou como `[DADO: confirmar]` porque não foi confirmado, então **não conta como Ancorado=✓** até o dono cravar. Só você diz ✓ (a estrutura sumiu dentro da voz dele, mecanismo próprio "separar por função"). Anti-IA ✓ (zero travessão, sem verbo-clichê). VEREDITO = REFAZ enquanto o número for `[DADO: confirmar]`; PASSA quando o dono confirmar o número real.
