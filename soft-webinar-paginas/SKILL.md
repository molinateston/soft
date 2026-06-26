---
name: soft-webinar-paginas
description: "Escreve as 3 páginas que orbitam o webinar do método Soft: Cadastro (captura/qualifica), Obrigado/Lembrete (sobe comparecimento) e Checkout (abre a venda de quem já decidiu). Cada página tem UMA função, é mobile-first, passa pelo gate. Carrega: bio detalhada na última dobra (cadastro e obrigado), obrigado modelo web-v1 (nome dinâmico, badges anti-fuga, card da aula com timer, ficha wizard que fecha no WhatsApp, variante ao vivo), checkout ENXUTO (cronômetro 5min, 15 primeiros, garantia, provas, bônus, nada mais), variante wa.me sem form, formatos AO VIVO x PERPÉTUO, ticket até ~3k no botão x acima vai pro 1:1. Use quando o pedido for páginas do webinar, página de cadastro/inscrição/captura, página de obrigado/lembrete, checkout do webinar. NÃO use pro roteiro/oferta/deck/gravação/e-mails/anúncios/pós-webinar (soft-webinar irmãs); vendas/VSL/landing fora de webinar (soft-funil); headline isolada (soft-conteudo-headlines); posicionamento (soft-posicionamento); arte (soft-designer); script 1:1 (soft-vendas)."
---

# As 3 páginas que orbitam o webinar

**O que esta skill faz por você:** escreve as PÁGINAS do webinar (cadastro, obrigado, checkout) que enchem a sala e levam pra oferta, no padrão do método, cada bloco pronto pra colar na ferramenta.

**As 6 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, zero figura de linguagem vazia, só o que uma pessoa real diria, cria o contexto ANTES da afirmação; (2) abre ensinando o que faz e por que aquele passo importa; (3) é consultiva, puxa o contexto de você antes de gerar, nunca cospe no escuro; (4) contexto é rei, a estrutura flutua pelo assunto, não é trilho rígido; (5) **admite se faltar insumo, nunca inventa**, marca `[A CONFIRMAR]` no lugar exato do furo (número/case/fala/oferta que falta é pendência declarada, jamais buraco preenchido com algo plausível); (6) **doc de output enxuto pros 2 leitores** (o humano que cola a página + a IA que a recebe como contexto), zero texto além do necessário, corta meta-narração e bastidor. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0; as leis 5 e 6 também estão embutidas no gate do Passo 6.)

**Este SKILL.md é o processo inteiro e ele carrega o método.** Siga os passos na ordem, pare nos checkpoints, e rode o gate por dentro antes de mostrar qualquer página. A profundidade (falas verbatim, moldes visuais, exemplos por nicho) vive em `references/paginas-cadastro-obrigado-checkout.md`; cada passo que precisa dela DIZ qual seção ler e o que aplicar. Nenhuma técnica fica só na reference, o corpo sempre manda usar.

## A régua que governa as 3 páginas
A frase que abre o tema: a ferramenta não vende, a ferramenta protege. Quem cria desejo é a aula; a página só faz o desejo não vazar. Todo elemento existe por um de três motivos. Na dúvida se inclui algo, pergunta:
1. **Protege a atenção?** (impede a pessoa de pausar, sair, se distrair)
2. **Protege a venda?** (deixa o botão no instante exato em que a pessoa decide)
3. **Mede?** (te diz depois quem está quente e quem está frio)

Se não faz nenhuma das três, descarta. Enfeite que não protege nem mede é fricção.

**Página "feia" que roda ganha de página linda que enfeita.** Cada animação, cada enfeite é uma distração que tira a pessoa do único trabalho da página; página bonita demais converte menos. Não segura a operação esperando design polido. E o filtro Soft vale nas três: **filtra, não convence.** Lead errado não comparece, não compra, suja a métrica e queima a verba; "quanto mais lead" é mentira.

| # | Página | Função única | A pergunta que ela responde |
|---|--------|--------------|------------------------------|
| 1 | **Cadastro** | capturar e qualificar quem assiste | "isso é pra mim?" |
| 2 | **Obrigado/Lembrete** | garantir comparecimento + capturar o WhatsApp | "como eu não perco?" |
| 3 | **Checkout** | abrir a venda de quem já decidiu | "por que agora?" |

Quando o cadastro tenta vender, falha nas duas. Quando o checkout precisa convencer do zero, é a aula que não fez o trabalho.

## Output Contract (o que você entrega)
- **Uma página por vez** (Cadastro → Obrigado → Checkout), na ordem. A saída é **limpa, como no Claude Chat**: só a página, o texto bloco a bloco pronto pra colar na ferramenta. Nada de briefing genérico.
- **Doc enxuto pros 2 leitores (Lei 6):** o que sai serve o humano que cola E a IA que recebe a página como contexto. Só os blocos da página + os `[A CONFIRMAR]` + os rótulos mínimos pra navegar. Zero meta-narração ("isto é o bloco que faz X"), zero bastidor, zero explicação-do-método-pro-leitor.
- O gate roda **por dentro** (auditoria silenciosa); a tabela do gate NUNCA vai pra saída.
- Você **para e espera OK** depois de cada página antes de seguir pra próxima. Não despeja as 3 de uma vez.
- Você **nunca inventa fala, número, prova ou case do cliente** (Lei 5); sem fonte, marca `[A CONFIRMAR]` no lugar exato do furo e não conta como ancorado. Insumo que falta é pendência declarada, jamais buraco preenchido com algo plausível.
- Você **nunca mostra página que falhou no gate**.

## Passo 0, ancora antes de escrever (NÃO PULE)
Procura a fonte de fala/prova real, nesta ordem: **descrição do projeto** → **Plano/posicionamento colado** → **mensagens anteriores**. Puxa do tema: a **oferta** (stack + garantia + preço), a **promessa central + mecanismo nomeado**, **3-5 falas de DOR/DESEJO** literais (com o N de quantas vezes apareceram) e a **prova real** (resultado, case, número confirmado). Pra ancorar no verbatim sem inventar, lê `shared-references/crivo/01-entrada-verbatim.md` e aplica a régua de fonte.

Três estados de entrada (declara qual é o seu, sem imprimir explicação longa):
- **Tem oferta + fala real:** caminho ideal. Ancora nelas, cita o N real.
- **Tem nicho/fundação mas ZERO oferta fechada ou fala literal:** NÃO inventa. Cada bloco ancora em prova real; o que faltar entra como `[A CONFIRMAR]`. Avisa que a oferta precisa estar fechada antes do checkout (vem da soft-posicionamento/soft-webinar-plano).
- **Sem nada:** pergunta numa única mensagem (nicho em 1 linha + a promessa + 1 dor real que o cliente fala) e segue.

**Decide o MODELO antes de tudo**, porque ele muda os campos do formulário (é decisão de negócio, não estética):
- **Self-service** (a venda fecha sozinha no checkout, sem ninguém ligar) → só nome + e-mail. Pedir telefone derruba o cadastro e, sem comercial pra ligar, o telefone não paga o cadastro perdido.
- **High-ticket / 1:1** (esteira de WhatsApp + comercial atrás) → nome + e-mail + WhatsApp (+ qualificador). O WhatsApp vale mais que os cadastros perdidos: é o canal que sobe comparecimento e alimenta o comercial.

Não copia "só nome e e-mail" se tem comercial high-ticket; não pede telefone se é 100% self-service barato.

**Decide também o FORMATO antes de escrever** (é decisão de negócio, muda o que as 3 páginas dizem sobre data, contagem e replay; se não souber, pergunta na mesma mensagem do MODELO):
- **AO VIVO** (evento único, data e hora marcadas): cadastro mostra **data fixa real** ("quinta, 20h") + contagem regressiva **real até essa data** (dias/horas), não relativa; obrigado define o lembrete pra a data exata; anti-fuga é honesto ("não terá replay completo, é ao vivo"); o timer só vale quando a data chega. É o formato de **validação** e de turmas/lançamentos pontuais.
- **PERPÉTUO** (sessão que roda sempre, sem replay): a página **não tem data fixa** escrita, cada lead vê a SUA sessão/horário/link (a espinha do Passo 5). Cadastro mostra horário **relativo** ("próxima sessão começa em 12 min", just-in-time) ou horários fixos do dia (recurring); o anti-fuga "essa sessão não terá replay" é verdadeiro de fato (desliga o replay instantâneo na ferramenta); timer ao vivo quando a sessão começa em <60 min. Captura o **horário escolhido** no form (vira variável da automação).

Não escreve "data fixa" numa página de perpétuo, nem contagem "relativa de 12 min" num evento ao vivo de daqui a 3 dias. **No perpétuo, lê a seção "Dados dinâmicos do perpétuo" da reference antes de montar.**

> **Antes de montar página + automação, decide se é cedo pra isso.** Na **validação inicial** (ainda testando o webinar, ainda sem volume), NÃO investe em design polido nem automação: usa página **rústica** (Notion público, Carrd ou similar), ou pula direto pra variante crua do Passo 7 (`wa.me`-direto). Página feia que mede ganha de página linda que atrasa o teste. Só investe nas 3 páginas completas quando a conversão se provou. (Notas operacionais da reference confirmam: "não invista em design polido até validar".)

## Passo 0.5, EXTRAÇÃO CONSULTIVA, arranca o ouro do especialista ANTES de montar (NÃO PULE)
Antes de escrever QUALQUER bloco, a ordem é: **PERGUNTA pra arrancar o melhor do especialista → minera as fontes que o Passo 0 já achou → só então marca `[A CONFIRMAR]` no que sobrar.** Isto NÃO é o "tá bom? ajusto?" do fim (Passo 8); é puxar o material de ouro ANTES de montar, pra a página nascer da prova mais forte que ele tem, não de um molde genérico. Página boa não se inventa, se extrai: a melhor headline, a prova mais pesada e a objeção nº1 já estão na cabeça dele; a skill só faz as perguntas certas pra elas saírem.

Faz as 5 perguntas **numa única mensagem** (não interroga uma a uma; junta tudo, deixa ele responder no ritmo dele), espelhando o ramo "pergunta numa única mensagem" do Passo 0:

> Antes de montar suas páginas, me passa o ouro que só você tem (responde o que souber; o que faltar eu marco pra confirmar depois):
> 1. **Qual sua promessa / headline mais forte?** (a frase que faz seu cliente parar; pode ser tosca, eu lapido)
> 2. **Qual sua prova MAIS forte pro checkout?** (documento ou case REAL, na moeda da promessa, se promete salário, é a carteira; se promete cliente, é o print do fechamento)
> 3. **Qual a objeção nº1 que segura a compra do seu público?** (o "sim, mas..." que mais aparece)
> 4. **Qual seu diferencial único, o "só você"?** (o que o concorrente não consegue dizer igual)
> 5. **Qual o número real, preço e vagas?** (confirmado de fato, não estimado, número que você não bate de verdade vira `[A CONFIRMAR]`)

O que ele entregar vira a matéria-prima dos blocos: a resposta 1 alimenta a Headline (Passo 1.1) e a Subheadline; a 2 vira as Provas na moeda do checkout (Bloco D); a 3 vira o Contra-filtro (Passo 1.7) e cada bônus que mata 1 objeção (Bloco E); a 4 vira a bio detalhada/USP (Passo 1.B); a 5 fixa o Stack e a escassez auditável (Blocos A/B/E). Resposta vaga ou ausente NÃO autoriza inventar: minera primeiro as fontes do Passo 0, e o que ainda faltar entra como `[A CONFIRMAR]` e não conta como ancorado. Com o ouro na mão (extraído + minerado), segue pro Passo 1.

## Passo 1, Página de CADASTRO (captura e qualifica)
Três trabalhos, só três: comunicar de cara o que é a aula · qualificar (atrair o avatar certo, repelir o errado) · gerar desejo e curiosidade. O objetivo NÃO é volume máximo, é qualidade. Ordem dos blocos: Hook → Subheadline → Bullets → Foto/autoridade → Formulário → Infos do evento → Contra-filtro → Prova social discreta.

**1. Hook/Headline** (a peça mais importante, prende em 2s). Fôrma-mãe: "Como usar [mecanismo único] pra [objetivo final] mesmo sem [a principal objeção]" (+ opcional "em [tempo]"). Cabe em 1 linha no mobile (≤14 palavras), específica (não "ganhe mais"). O nome do mecanismo é SLOT do cliente; usa o que existe ou marca `[A CONFIRMAR]`. Troca os três campos da fôrma pelo nicho, **nunca copia headline alheia, copia a fôrma**.

  **Escolhe 1 das 4 variações pela TEMPERATURA do avatar** (não tem variação "padrão", a escolha é estratégica):
  - **Promessa primária direta** (avatar racional): "Como [resultado] em [tempo curto] mesmo sem [objeção primária]".
  - **Pergunta provocativa** (avatar reflexivo): "Por que [comportamento comum no nicho] está te custando [consequência], e o que fazer no lugar".
  - **Revelação contra-intuitiva** (avatar cético): "O que [as referências do nicho] não te contam sobre [tema]".
  - **Big Idea condensada** (posicionamento maduro): "[Nome do método (slot, a definir com o especialista)]: o caminho [adjetivo único] pra [resultado]".

  Avatar cético: começa com "Por que"/"O que" em vez de "Como", que não soa promessa fácil. **Lê `references/paginas-cadastro-obrigado-checkout.md` Bloco 1.1 e aplica os 4 moldes instanciados em nichos diferentes** (emprego, comportamento felino, gestão, posicionamento), pra ver a mesma fôrma virar 4 headlines reais e instanciar a do nicho atual.

**2. Subheadline** (opcional, recomendada): explica a promessa em 1-2 frases. Tem **duas funções, escolhe uma**: reforço por **urgência** ("saiba o que ajustar hoje mesmo") OU reforço por **prova social** ("a estratégia que já recolocou mais de mil pessoas"). Molde: "Webinar gratuito de [duração]. Você sai com [resultado tangível] e o método completo, sem enrolação." Sem número de prova confirmado, vira `[A CONFIRMAR]`.

**3. Bullets (4-6)**: diz O QUE aprende, nunca O COMO. Cada bullet toca **um dos 3 Ds** (Dor, Desejo OU Dúvida), fazendo a pessoa pensar "como ele sabe disso? isso é pra mim". Bullet que entrega o passo a passo já entregou o produto de graça. Um bullet pode plantar a **Big Domino** (a crença que abre a venda) e outro o **gancho de retenção** (o bônus só pra quem ficar até o fim). **Lê Bloco 1.3 e aplica os 5 moldes mapeados por D** (Dor/Dúvida/Desejo/Big Domino/gancho) + o exemplo de gestão pra calibrar.

**4. Foto/vídeo + autoridade breve** (no TOPO): 2-3 linhas só, não o currículo. Empatia ANTES do feito. A bio DETALHADA não vai aqui, vai na ÚLTIMA DOBRA (Passo 1.9, regra das 3 páginas). Molde topo: "[Nome]. [empatia: já passei por X]. [feito: hoje Y clientes têm Z]." Número só confirmado; sem fonte, `[A CONFIRMAR]`.

**5. Formulário**: campos pela regra de MODELO (Passo 0). No perpétuo, captura também o **horário escolhido** da sessão, que vira uma variável que acompanha o lead pela automação inteira (permite o "te vejo às 19h" e o link individual, ver Passo 5). Campos qualificadores (só high-ticket, opcionais): estágio atual (faturamento/tempo), maior obstáculo (lista pré-definida que segmenta a comunicação depois); mais campo = menos cadastro, porém lead mais qualificado. Botão: "Confirmar minha vaga" / "Quero participar" / "Reservar acesso"; nunca "Cadastrar" / "Registrar" / "Enviar" (palavra de formulário burocrático, não de evento). A aula é sempre GRÁTIS na captura (aula paga na captura não funciona); a barra de inscrição aparece direto, sem bolha pra clicar. Política de privacidade em linha discreta abaixo do botão.

  **Truque form-less do WhatsApp:** pedir o número no form derruba o cadastro. Em vez de pedir, faz a pessoa te mandar uma mensagem pré-pronta; ela acha que está só "confirmando a inscrição pelo WhatsApp" e você captura o número sem ter pedido. O clique no `wa.me` é, ele próprio, o cadastro + o opt-in num gesto só (é a ponte pra variante crua do Passo 7). **Lê Bloco 1.5 e aplica o detalhe do horário-variável + o truque form-less com a fala literal.**

**6. Informações do evento**: data / horário / duração / formato / plataforma (se aparece pro participante). **Ramifica pelo FORMATO (Passo 0):** no **ao vivo**, data fixa real ("quinta, 20h") + contagem regressiva real até a data; no **perpétuo**, horário **relativo** ("próxima sessão começa em 12 min", just-in-time) ou horários fixos do dia (recurring), nunca data fixa. **Escolher um horário vira compromisso** na cabeça do lead (vira um meeting, e quem tem compromisso aparece); é o que separa o webinar de uma VSL. **Quatro horários por dia é o ponto ótimo** (manhã/tarde/noite; os do exemplo do método são **9h / 11h / 14h / 19h**, achados do avatar DELE, o seu avatar pode comprar em outro horário): demais e a pessoa procrastina ("roda a qualquer hora"), de menos e ela não encaixa nenhum.

  > **Vitrine (detalhe de ferramenta):** o **EverWebinar** mostra os **dois** próximos horários na página; o **WebinarKit** mostra **quatro**. **Convertem igual**, só muda a vitrine; escolhe pela ferramenta que o cliente já usa, não por achar que "mais horário converte mais". (Bloco 1.6 traz o porquê do horário relativo com a fala do compromisso.)

**7. Contra-filtro** (a parte mais Soft): "NÃO é pra você se… / É pra você se…". Diz pra quem NÃO é antes de pra quem é. **Mantém SEMPRE a linha anti-milagre no NÃO** (expulsa quem busca fórmula mágica / viralização / atalho); essa é a peça universal que não se troca por nicho. Promessa Soft: simples e honesto, nunca fácil e mágico. Quem não é avatar fecha a aba (ótimo, ele só sujaria a métrica); quem é, confirma "é pra mim" e entra mais comprometido. **Lê Bloco 1.7 e aplica o molde NÃO-é/É + os dois exemplos (Soft Business e gestão) com a linha anti-milagre marcada.**

**8. Prova social discreta** (1-2 elementos): logos, 1 depoimento curto, 2-3 prints reais, ou uma estatística condensada. Aqui ela só **endossa**; prova pesada é no checkout (Passo 3). No perpétuo, o mesmo depoimento pode rodar em **loop de pre-roll** dentro da sala antes do host aparecer, escolhido pra já contar a tese (vilão + contraste + promessa contraintuitiva); ver o exemplo verbatim de pre-roll em Bloco 1.8.

**9. BIO DETALHADA na última dobra**: ver a regra única no Passo 1.B (vale pro cadastro E pro obrigado; checkout NÃO leva). No cadastro fecha a página depois da prova social, antes do CTA repetido.

## Passo 1.B, a BIO DETALHADA na ÚLTIMA DOBRA (regra das páginas, do bench do Léo)
**Onde:** penúltima/última dobra, DEPOIS do conteúdo da aula/oferta, ANTES do fecho. NUNCA no topo. **Em quais:** CADASTRO e OBRIGADO. **CHECKOUT não leva** (já viu o cara na aula; bio lá é fricção). **Função:** valida autoridade SEM currículo. **Ordem fixa:** empatia/cicatriz ANTES do feito (cicatriz antes do troféu). **Lê `references/_PAGINAS-BENCH.md` Seção 1 pros 2 textos verbatim do Léo.**

**Escolhe 1 dos 2 formatos pelo tipo de página:**

| Formato | Onde | O que é |
|---|---|---|
| **A · Prosa 1ª pessoa** | captura/obrigado | foto P&B numa coluna + 5-6 parágrafos curtos, voz de boteco |
| **B · Prosa + grade de credenciais** | landing mais vendedora | 1 parágrafo denso + 4 cards numéricos (número verde + label mono) |

**O molde da prosa (5 parágrafos, a ordem que o Léo bate):**
1. Quebra de imagem / empatia: "não sou [estereótipo de guru], sou um cara normal" + a credencial-mãe em 1 linha.
2. Número-âncora COM ressalva honesta: o feito grande + a distinção que o concorrente não faz ("gerenciei, não faturei") → prova que é honesto.
3. A cicatriz (fundo do poço): quebrou / recomeçou do zero / "foi caindo que descobri".
4. O feito-prova DEPOIS da cicatriz: resultado grande nomeado e calculável (ex.: "R$13M, 2 anos, 5 pessoas, 1 funil"), não "milhões genéricos".
5. Anti-milagre + promessa: "não vim te vender milagre. Vim mostrar que [promessa]. E provar por A mais B."

**A grade do Formato B (4 cards, cada um = número + contexto-que-prova):** 4 ângulos: escala · amplitude · feito-âncora · cicatriz. Nunca número solto; cada um vem com o contexto que impede leitura inflada.

**Regras (valem nos 2 formatos):** 1ª pessoa, frase curta, voz de boteco · empatia/cicatriz ANTES do feito · número com lastro/ressalva · anti-milagre no fecho da prosa · foto P&B (grayscale + contraste, vertical 4/5, tag nome+cidade) · sem currículo/títulos · furo de dado do cliente = `[A CONFIRMAR]` no lugar, nunca número plausível.

## Passo 2, Página de OBRIGADO / Lembrete (modelo web-v1/obrigado)
Função única: **fazer a pessoa aparecer.** Alvo Soft 50%+ (benchmark 33-57%); o que move o número é o WhatsApp (**+54%, de 31% pra 47%** quando liga o canal). 3 trabalhos que valem dinheiro: lembrete (presença), ficha (inteligência), opt-in WhatsApp (comparecimento). Começo da inteligência, não fim do funil. **Lê `references/_PAGINAS-BENCH.md` Seção 2 pros blocos verbatim da página real.**

**Ordem dos blocos (a do web-v1, verbatim):** Confirmação c/ nome → 3 badges anti-fuga → card "Sua aula" → gate pra FICHA → presente de retenção. O WhatsApp é o destino FINAL (na tela última da ficha), não um bloco solto no topo.

| # | Bloco | O que vai dentro |
|---|---|---|
| 1 | **Confirmação enfática (nome dinâmico)** | eyebrow check verde "✓ Inscrição confirmada" · H1 "Informações importantes" · lead c/ nome: "Tá garantida, **[nome]**. O acesso é **gratuito e limitado**." Nome vem da URL (`?first_name=`) c/ fallback `localStorage` (funciona em qualquer aparelho) |
| 2 | **3 badges anti-fuga** (cards X vermelho) | "✗ Ao vivo, sem replay" · "✗ Sem material depois" · "✗ Só quem fica até o fim". É o anti-fuga virado 3 selos no topo; mata o "depois vejo a gravação" |
| 3 | **Card "Sua aula"** | Data + Horário (do horário que o lead escolheu na captura; perpétuo NUNCA tem data fixa, cada lead vê a SUA) · **timer OFICIAL da ferramenta** restilizado na marca ("Sua aula começa em: …"; ao zerar a página vira a sala) · linha de acesso dashed ("**Deixe esta página aberta.** Na hora ela vira sua sala e te leva pra dentro. O link chega no **e-mail** e **WhatsApp**.") · **agenda**: 3 botões Google/Outlook/.ICS c/ link individual embutido |
| 4 | **Gate "Passo decisivo" → FICHA** | card verde · selo "Passo decisivo" · H2 "Garanta sua vaga na sala" · "Assentos limitados. Preenche a ficha rápida (3 min) pra travar teu lugar. Uso tuas respostas pra preparar a sala pro teu caso." · botão "Garantir minha vaga →" pra `/ficha/` |
| 5 | **Presente de retenção** (fecho) | card discreto: "🎁 Tem um **presente pra quem ficar até o fim**. Entra no horário e fica até o final." |

> **Lê Bloco 2.2 pro molde do opt-in + a mensagem que sobe comparecimento, e Bloco 2.6 pros 3 usos da ficha (Lead Score / comercial / dor na voz do lead).** ~30% respondem a ficha sem incentivo. O timer é SEMPRE o oficial da ferramenta, nunca contagem em localStorage (quebra cross-device).

### A FICHA (web-v1/ficha): wizard 1-pergunta-por-tela, termina no WhatsApp
Barra de progresso · salva sozinha (retoma se fechar a aba) · prefill do que veio da captura (não repergunta nome/email/whats). Tela final = WhatsApp.

| Grupo | Pontua? | Campos |
|---|---|---|
| **Identificação** (só se NÃO veio da captura) | não | e-mail · nome · WhatsApp |
| **Segmentação** | não | tipo de especialista · nicho · tempo de mercado · ticket médio · usa IA · dor principal |
| **Score** (define HOT) | sim | urgência (0-10) · quando quer resolver · faturamento mensal · **quanto toparia investir** (piso HOT = topa 3k+) |
| **Insight** | não | "O que mais te trava hoje?" (campo aberto, na voz do lead) |

**Tela final:** "Pronto, [nome]. Vaga garantida." + único próximo passo = botão WhatsApp c/ msg pré-pronta ("Oi Léo! Acabei de preencher minha ficha da masterclass. Quero garantir minha vaga na sala.") + nota "A sala abre no horário que você escolheu · não falta, tem presente no fim".

### Variante AO VIVO (obrigado da imersão): quando o evento tem data fixa
| Elemento | No AO VIVO |
|---|---|
| H1 | "Tá dentro. Sua vaga gratuita tá reservada." |
| Estrutura | stepper de 3 passos: **Agora, responde a ficha** (libera o grupo no fim) → **Grupo de WhatsApp** (sai o link do Zoom, lembretes, materiais) → **dia/hora ao vivo** |
| Gate honesto | "Antes de liberar o grupo: leio cada ficha pra calibrar a aula. Sem a ficha, o grupo não abre." |
| CTA | "Responder a ficha agora" + nota "leva 5 min · libera o grupo no fim" |
| Diferença-chave | ao vivo o WhatsApp é um **grupo** (link do Zoom + lembretes); perpétuo é **conversa 1:1** + a página que vira sala sozinha |

## Passo 3, Página de CHECKOUT ENXUTO (abre a venda de quem já decidiu)
Quem chega já está ~80% decidido. A aula vendeu. **O checkout NÃO convence do zero**: tira a última hesitação e dá o trajeto mais curto pro cartão. Se precisa convencer, o furo está na aula. Conversão de quem ENTRA: 60-85%. **Lê `references/_PAGINAS-BENCH.md` Seção 3.**

> **A régua do Léo (não negocia):** checkout SÓ com **cronômetro 5min + "você está entre os 15 primeiros" + garantia + provas + bônus. NADA mais.** Cada bloco extra é fricção que faz a pessoa pensar de novo.

**Achado:** não há HTML de checkout deployado, o checkout do Léo é a tela do gateway (Cakto/WebinarKit). Os blocos são o que entra NA tela / no topo dela.

**Decide o DESENHO pelo ticket:** até ~3k = checkout impessoal (os blocos abaixo). High-ticket = fecha no **1:1** (CTA pro `wa.me`, **nunca o preço seco**; ver Passo 7).

**Os 5 blocos, na ordem na tela** (tudo acima/perto da dobra):

| # | Bloco | O que vai dentro |
|---|---|---|
| A | **Cronômetro 5min** (topo) | faixa verde fina · "Sua condição vale por: [04:59 → 00:00]" · some/volta o preço cheio ao zerar · escassez de **condição auditável** (o desconto/bônus do link da aula), nunca mentira de estoque |
| B | **"Você está entre os 15 primeiros"** | selo logo abaixo do timer: "Você está entre os 15 primeiros, bônus liberado." Vem do **link controlado** ("quem usar o link que eu disponibilizo AQUI ganha [vantagem]"); o checkout vira **prêmio**, não página passiva. Dispara InitiateCheckout |
| C | **Garantia em destaque** | escudo · garantia do **cardápio** (não dogma, escolhe pelo ticket) · inverte o risco. Molde incondicional: "🛡️ Garantia de [X] dias. Não é pra você, devolvemos 100%. Sem perguntas." (perpétuo do Léo fecha 90+90; MindMaster fecha sem garantia; desenho `[A CONFIRMAR]` por cliente). **Lê Bloco 3.4 pro cardápio** |
| D | **Provas (na moeda da promessa)** | 3-5 provas fortes, mais pesadas que na captura · **prova na MOEDA**: prometeu salário → foto da carteira; prometeu venda no automático → print do dashboard · documento bruto e feio > slide bonito · depoimento na boca do cliente. **Lê Bloco 3.3** |
| E | **Bônus (stack empilhado)** | cada item ancorado pelo valor avulso, soma riscada acima do preço · cada bônus mata UMA objeção; o de ação rápida ("15 primeiros") amarra com o Bloco B. Preço é slot, instancia pelo produto. **Lê Bloco 3.1** |

**Molde visual do stack (Bloco E):**
```
VOCÊ ESTÁ ADQUIRINDO:
✓ [Componente principal]        .... R$ X
✓ [Bônus 1: nome]               .... R$ Y
✓ [Bônus 2: nome]               .... R$ Z
✓ [Bônus ação rápida · 15 primeiros] R$ W
                                  ──────────
VALOR TOTAL                       ~~R$ soma~~
HOJE VOCÊ INVESTE                   R$ [preço]   (ou 12x de R$ ...)
```

**Pagamento:** cartão primeiro (mais converte), PIX visível, selo de segurança discreto. Acima/perto da dobra.

### O que NÃO entra no checkout enxuto (corte explícito)
| ❌ Fora | Por quê |
|---|---|
| FAQ longo (5-7 perguntas) | é o checkout "completo" da reference; o Léo pediu enxuto |
| Re-explicação do método / nova dobra de vendas | quem chegou já decidiu |
| Upsell agressivo | mata conversão |
| Bio detalhada | já foi na aula/captura (regra do Passo 1.B) |
| Qualquer enfeite | faz a pessoa parar e reconsiderar |

## Passo 4, princípio comum às 3 páginas (carrega antes de fechar)
| Princípio | A régua |
|---|---|
| **Mobile-first** | 70-85% do tráfego é celular. Headline sem scroll · botão ~44px · form enxuto · imagens leves · vídeo com thumbnail estático (**NÃO autoplay**). Abre no SEU celular e lê como o avatar. Visual → `shared-references/filtro-mobile-first/checklist-final.md` item a item |
| **Velocidade** | <3s · imagens WebP · sem fontes externas pesadas · CSS crítico inline. **Vídeo nunca em Vimeo** (engasga em banda fraca, mata o webinar); usa o servidor da ferramenta ou YouTube com código anti-clique |
| **Pixel + tracking** (antes do tráfego) | Pixel Meta no head das 3 · PageView auto · **Lead** no submit (pág 1) · **InitiateCheckout** ao entrar no checkout (pág 3, junto com o "15 primeiros" do Bloco B) · **Purchase** no pagamento. Em redirect o pixel carrega **síncrono** (`async=false`), senão perde o evento |
| **Coerência visual** | as 3 no mesmo padrão de marca (paleta/tipografia/tom); páginas de "empresas diferentes" destroem confiança |
| **Sem designer** | marca com padrão → monta em **template** (Hotmart Pages/ClickFunnels/Cartpanda). Não para esperando designer; a página converte, não impressiona |
| **A/B no MESMO mecanismo** | prioridade = headline do cadastro · 2 variantes, 50%/50%, **mín. 200 leads/variante** · erro caro: anúncio de um mecanismo numa página de outro despenca a conversão |

## Passo 5, a espinha invisível do perpétuo (o link único por lead)
Cada inscrito recebe um link só dele (ingresso nominal, sessão compartilhada: "link só seu, sala compartilhada"). É a peça da **medição**: você sabe até onde cada um foi (não veio / saiu cedo / ficou 50% / **viu a oferta**). A variável **nome/e-mail/horário/link** viaja da plataforma de webinar pro e-mail pro WhatsApp via API; por isso o cadastro captura o horário (Passo 1.5), o obrigado embute o link no calendário (card "Sua aula", Passo 2), e a mensagem dos 5 min antes chega com o link exato da sessão daquela pessoa. A **tag "viu a oferta"** (a oferta cai num timestamp exato da aula) separa quem viu e não comprou (objeção específica, recuperação de venda no pós) de quem mal entrou. Monta a estrutura de tags **AGORA, ao configurar** (a medição não é retroativa) e **não fica mexendo nas integrações depois que o webinar está rodando**, reconfigurar à toa quebra a medição inteira. (O uso completo das tags no pós é da soft-webinar-mensagens.) **Se o pedido for perpétuo, lê a seção "Dados dinâmicos do perpétuo" da reference e aplica a espinha do link único.**

## Passo 6, roda o gate por DENTRO (auditoria silenciosa, NÃO imprime)
Roda o gate em CADA página **internamente**. Só página com VEREDITO=PASSA vai pro cliente. Uma falha refaz o bloco que falhou (não a página inteira). A tabela abaixo é o teu **checklist INTERNO**, nunca a saída: o cliente recebe só a página limpa (Passo 8), jamais a tabela.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Ancorada no verbatim** | promessa/bullets/prova nascem de fala ou prova REAL do cliente (cita N real); número/case/fala inventado = ✗ automático (vira `[A CONFIRMAR]`) | |
| **Uma função só** | cadastro qualifica (não vende), obrigado faz aparecer (não vende), checkout abre venda decidida; nenhuma página invade a função da outra | |
| **Cadastro = 1 promessa + 1 CTA** | um hook claro (1 das 4 variações pela temperatura), um único caminho de ação, form só com os campos que o MODELO justifica, contra-filtro com a linha anti-milagre | |
| **Obrigado com "como não perco" respondido** | a pessoa sai sabendo data/hora, como acessa, tem o opt-in/lembrete e a ficha; aparecer ficou fácil | |
| **Checkout ENXUTO (5 blocos, nada mais)** | só: cronômetro 5min + "15 primeiros" + garantia (cardápio) + provas (na moeda) + bônus/stack (cada item mata 1 objeção + soma riscada) + pagamento. SEM FAQ, SEM re-explicar método, SEM upsell, SEM bio. Qualquer bloco extra = ✗ | |
| **Bio detalhada na última dobra** | cadastro E obrigado terminam com a bio DETALHADA (empatia/cicatriz ANTES do feito, número com ressalva, anti-milagre no fecho); checkout NÃO tem bio. Bio no topo ou ausente nas 2 primeiras = ✗ | |
| **Mobile-first** | headline sem scroll, botão ≥44px, form enxuto, sem autoplay, carrega leve; testado como avatar no celular | |
| **C / U / B** | Clareza (entende em 2s) · Utilidade (sabe o que ganha) · Boa-vontade (sem hype, sem promessa fácil). Os três de pé | |
| **Sem promessa fabricada** | nenhuma promessa de resultado, número de prova ou garantia que o cliente não confirmou de fato | |
| **CTA com destino** | todo botão diz o que acontece ao clicar e tem destino real (form / wa.me / calendário / gateway), nunca "Saiba mais" vago | |
| **3 perguntas do Harry** | Dá pra VER? (cena/chão, não tese) · Dá pra FALSIFICAR? (fato, não adjetivo) · SÓ você diz? (o concorrente não assina igual) | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, transforma"). **No chat (sem o lint), faz CTRL+F manual de "—" e da família "travar" antes de marcar ✓.** No Code, roda `python3 scripts/lint_copy.py`. | |
| **Coerência de formato** | página de **ao vivo** tem data fixa real + contagem real até a data; página de **perpétuo** NÃO tem data fixa, usa horário relativo/recurring + link único. Misturou (data fixa no perpétuo, "12 min" num evento de 3 dias) = ✗ | |
| **Lei 5, admite-não-inventa** | todo furo de insumo (número, case, fala, oferta, vagas, preço) está marcado `[A CONFIRMAR]` no lugar exato, NUNCA preenchido com algo plausível; nenhum dado parece real sem fonte | |
| **Lei 6, doc enxuto pros 2 leitores** | a saída é só a página colável: blocos + `[A CONFIRMAR]` + rótulos mínimos. Zero meta-narração, zero bastidor/racional, zero explicação-do-método-pro-leitor, zero repetição. Serve humano que cola E IA que recebe como contexto | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

(O detalhamento de C/U/B + as 3 perguntas do Harry: `shared-references/crivo/03-gate-cub.md`. Padrões banidos + reescrita do anti-IA: `shared-references/filtro-anti-ia/`.)

## Passo 7, a variante crua (CTA direto pro WhatsApp, SEM formulário)
Tudo acima é o caminho padrão (form + 3 páginas). A variante crua manda o lead **direto pro WhatsApp** (`wa.me`) em vez de um formulário, e funciona em **dois cenários**: (1) **validação** (não vale montar páginas e automação ainda); (2) **ticket que pede conversa humana** (fechamento 1:1). Passo a passo:
1. **O CTA é o número/link `wa.me`, não botão de form.** O clique no `wa.me` É o cadastro E o opt-in num gesto só. Molde: "se isso é pra você, manda uma mensagem pro meu WhatsApp e minha equipe te explica como funciona."
2. **A primeira mensagem do lead é o opt-in.** Quando ele escreve, optou (você não dispara pra base fria). Responde abrindo a conversa, não despejando preço.
3. **Qualifica com curiosidade, nunca com pitch:** "Oi [nome], tô curioso: por que você quer resolver [tema] agora?"
4. **Nunca dá o preço seco.** "Quanto custa?" respondido com o número = perdeu (o único parâmetro vira o bolso). Dá um passo atrás: "antes, me conta por que você tá buscando resolver isso agora?"

**Quando NÃO usar a variante crua:** **volume alto com ticket baixo**. Conversa humana não escala num produto de R$300, aí o checkout direto é mais barato e mais rápido. Formulário e `wa.me`-direto não são rivais, são o mesmo funil em dois níveis: o form escala o low/mid-ticket, o `wa.me` pega o lead quente que precisa de mão humana. **Lê a seção "Variante crua" da reference e aplica os exemplos (incluindo o redirecionamento dos indecisos pro WhatsApp na sala secreta).**

## Passo 8, mostra e PARA
Mostra **só a página LIMPA** (como no Claude Chat), o texto bloco a bloco pronto pra colar. Sem tabela de gate, sem meta, sem narrar o fluxo. Pergunta "essa te serve? ajusto, ou sigo pra próxima página?" e **espera o OK** antes de gerar a próxima.

## Números de referência de uma máquina bem montada
| Etapa | Faixa saudável |
|-------|----------------|
| Página → lead | 30-40% |
| Comparecimento (inscrito → presente) | benchmark 33-57%, **alvo Soft 50%+**; **+54% (de 31% pra 47%) quando liga o WhatsApp** |
| Compra automática no checkout (de quem compareceu) | 6-8%, antes de qualquer comercial tocar (de quem ENTRA no checkout, 60-85%) |

Se os indicadores estão muito abaixo disso, o furo quase sempre está numa **peça técnica** (a página, o horário, a hospedagem do vídeo, a mensageria), **não na copy**. Audita o encanamento (vídeo engasgando, horário mal escolhido, WhatsApp não ligado) antes de reescrever a aula no desespero.

## When NOT to use (manda pra skill certa)
- Pediu **oferta / stack / garantia / ancoragem do webinar** → **soft-webinar-plano** (esta skill só monta as 3 páginas; a oferta nasce lá).
- Pediu **roteiro / estrutura ADMA** → **soft-webinar-script**. **Deck/slides** → **soft-webinar-slides**. **Gravação/perpetuação** → **soft-webinar-plano**. **E-mails/WhatsApp** → **soft-webinar-mensagens**. **Anúncios** → **soft-conteudo-impulsionar**. **Pós-webinar/esteira** → **soft-webinar-mensagens**. **Plano/diagnóstico do webinar** → **soft-webinar-plano**.
- Pediu **página de vendas / VSL / landing** fora do contexto de webinar → **soft-funil**.
- Pediu **só a headline** (isolada, banco de ganchos) → **soft-conteudo-headlines**.
- Pediu o **CORPO de conteúdo de feed** (carrossel, reel, stories) → **soft-conteudo**.
- Pediu **posicionamento / oferta-mãe / mecanismo nomeado** → **soft-posicionamento**.
- Pediu **arte / PNG / visual** da página → **soft-designer**.
- Pediu **script de venda / objeção no 1:1** → **soft-vendas**.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Página de cadastro tentando vender o produto | Volta: cadastro só qualifica e gera desejo; venda mora no checkout |
| Headline "padrão" sem escolher pela temperatura | Escolhe 1 das 4 variações (direta/pergunta/contra-intuitiva/big idea) pelo avatar |
| Checkout pelado (só botão e preço) | Checkout ENXUTO = cronômetro 5min + "15 primeiros" + garantia + provas (na moeda) + bônus/stack (cada item mata 1 objeção) |
| Checkout inchado (FAQ, re-explicação, upsell, bio) | Corta tudo isso; o checkout é os 5 blocos só. Cada extra é fricção (lista de corte no Passo 3) |
| Checkout reexplicando a aula do zero | Quem chegou já decidiu; o checkout abre o caminho, não convence |
| Stack que só lista, sem ancorar | Cada item com valor avulso + soma riscada acima do preço; cada item mata UMA objeção nomeada |
| Prova fraca no checkout (igual ao cadastro) | No checkout a prova é mais FORTE e na MOEDA da promessa (documento bruto > slide bonito) |
| Garantia decalcada num número fixo | Cardápio pelo ticket; condicional = condições viram protocolo de implementação |
| Bio no topo da página, ou ausente | Bio DETALHADA na ÚLTIMA dobra do cadastro E do obrigado (empatia antes do feito); checkout não leva bio |
| Obrigado com WhatsApp solto no topo / sem ficha | Modelo web-v1: confirma → 3 badges → card "Sua aula" → gate pra ficha; WhatsApp é o destino FINAL da ficha |
| Timer do obrigado em localStorage | Timer SEMPRE o oficial da ferramenta (localStorage quebra cross-device) |
| Form pedindo telefone num produto self-service barato | Decide campos pelo MODELO (Passo 0), não por dogma; menos campo = mais cadastro |
| Bullets entregando o passo a passo | Troca por resultado/função (cada bullet num D); o COMO fica dentro do produto |
| Apagou a linha anti-milagre do contra-filtro | Recoloca: é a peça universal que não se troca por nicho |
| Inventou número de prova / case "plausível" | Só prova REAL; sem fonte vira `[A CONFIRMAR]` e não conta como ancorado |
| Vitrine "mais horário converte mais" | EverWebinar (2) e WebinarKit (4) convertem igual; escolhe pela ferramenta |
| Investiu design/automação antes de validar | Página rústica (Notion/Carrd) ou `wa.me`-direto na validação; só investe depois de provar conversão |
| A/B com anúncio e página de mecanismos diferentes | A/B só dentro do MESMO mecanismo, 200 leads/variante antes de decidir |
| `wa.me`-direto em volume alto + ticket baixo | Aí o checkout direto escala melhor; `wa.me` é pro lead quente high-ticket |
| Página linda mas pesada/lenta no mobile | Mobile-first é a régua; corta enfeite que não protege nem mede; template serve |
| Despejou as 3 páginas de uma vez | Uma por vez, com gate por dentro, e PARA pro OK antes da próxima |
| Imprimiu a tabela do gate ou narrou o fluxo na saída | O gate é INTERNO (auditoria silenciosa); a saída é só a peça limpa |

## References (o corpo acima carrega o método; esta guarda a profundidade que os passos mandam ler)
- `references/_PAGINAS-BENCH.md`: o BENCHMARK das páginas REAIS do Léo (no ar). Dirigido assim: Seção 1 (bio detalhada na última dobra, 2 formatos verbatim, Passo 1.B) · Seção 2 (obrigado web-v1 + ficha wizard + variante ao vivo, Passo 2) · Seção 3 (checkout enxuto, 5 blocos + lista de corte, Passo 3). É a régua que governa as 3 páginas; lê antes de montar.
- `references/paginas-cadastro-obrigado-checkout.md`: a profundidade do tema inteiro, falas verbatim, moldes visuais e exemplos por nicho. Dirigida assim: Bloco 1.1 (4 headlines instanciadas, Passo 1.1) · Bloco 1.3 (bullets por D, Passo 1.3) · Bloco 1.5 (horário-variável + form-less, Passo 1.5) · Bloco 1.6 (vitrine 2 vs 4, Passo 1.6) · Bloco 1.7 (contra-filtro, Passo 1.7) · Bloco 1.8 (pre-roll, Passo 1.8) · Bloco 2.2 (opt-in WhatsApp, Passo 2.2) · Bloco 2.6 (ficha/mina de ouro, Passo 2.6) · Bloco 3.1 (stack + ancoragem em degraus, Bloco E) · Bloco 3.3 (prova na moeda, Bloco D) · Bloco 3.4 (cardápio de garantia, Bloco C) · "Variante crua" (Passo 7) · "Dados dinâmicos do perpétuo" (Passo 5) · "Notas operacionais" (página rústica, A/B, designer, Passos 0 e 4).
- `shared-references/crivo/01-entrada-verbatim.md`: como ancorar no verbatim real (Passo 0).
- `shared-references/crivo/03-gate-cub.md`: C/U/B + as 3 perguntas do Harry do gate (Passo 6).
- `shared-references/filtro-anti-ia/`: padrões banidos + reescrita do anti-IA HARD (Passo 6).
- `shared-references/filtro-mobile-first/`: checklist mobile-first item a item, quando a página vira visual (Passo 4).
- `scripts/lint_copy.py`: no Claude Code, roda `python3 scripts/lint_copy.py` na copy de cada página como cinto extra do anti-IA. No chat não roda, por isso o CTRL+F manual do gate.
