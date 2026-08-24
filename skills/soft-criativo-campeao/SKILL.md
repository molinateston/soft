---
name: soft-criativo-campeao
description: "O METODO (nao o motor) de criativo de anuncio que VENDE, destilado do processo que gerou os melhores criativos da casa. Camada de ESTRATEGIA por cima do soft-criativo-lote: decide O QUE renderizar e valida ANTES de subir, enquanto o soft-criativo-lote decide COMO renderizar. Roda o processo replicavel por especialista em 7 passos: (1) 1 arte = 1 ANGULO DE DOR do avatar (nunca peca generica), (2) FOTO REAL da autoridade tratada (nunca banco de imagem), (3) IDENTIDADE travada num JSON (cor/fonte/selo/CTA da marca, nao chute), (4) render em LOTE pelo motor, (5) LINT anti-IA obrigatorio antes de virar pixel, (6) PREVIA pro dono ANTES de subir, (7) sobe PAUSADO com UTM padrao. Carrega a regra-mae PUBLICO ANTES DE CRIATIVO (nao troca arte antes de trocar publico) e um template de 4 campos pra clonar pra qualquer especialista novo (foto, identidade, 4 ganchos por dor, evento+UTM). Use quando o pedido for criar/planejar criativo campeao, replicar o processo de criativo pra outro nicho/especialista, montar o playbook de criativo de um cliente novo, ou decidir o angulo das pecas antes de renderizar. FRONTEIRA: soft-criativo-campeao = o METODO e o angulo (o cerebro); soft-criativo-lote = o motor Pillow que renderiza (a mao); soft-conteudo = escreve a copy/headline do zero; soft-designer = peca editorial unitaria; soft-trafego-meta = sobe e mede na conta. NAO renderiza sozinha (chama o soft-criativo-lote), NAO opera conta de anuncio, NAO escreve a copy do zero."
---

============================================================
CRIATIVO CAMPEAO — O METODO, NAO O MOTOR
============================================================

Esta skill e o CEREBRO. O soft-criativo-lote e a MAO.

Ela existe porque os melhores criativos da casa nao vieram de sorte no
Photoshop: vieram de um PROCESSO repetivel. O motor (soft-criativo-lote)
sabe renderizar pixel bonito; ele NAO sabe se a peca vai vender. O que faz
vender e o que esta ANTES do render: o angulo, a foto certa, o lint, a
previa. Esta skill guarda esse "antes" e chama o motor no fim.

Regra de ouro que resume tudo:

    A peca nao comeca no Photoshop. Comeca na DOR.
    E o PUBLICO decide mais que o CRIATIVO.


============================================================
QUANDO USAR / QUANDO NAO
============================================================

USE quando:
- Vai criar criativo de anuncio que precisa VENDER (nao so ser bonito).
- Quer REPLICAR o processo que deu certo pra um especialista/nicho novo.
- Precisa decidir o ANGULO das pecas antes de renderizar.
- Quer montar o playbook de criativo de um cliente novo (os 4 campos).

NAO use pra:
- Renderizar o pixel em si: isso e soft-criativo-lote (esta skill CHAMA ele).
- Escrever a copy/headline do zero: soft-conteudo.
- Peca editorial unica com diagrama/tabela: soft-designer.
- Subir, segmentar, medir na conta: soft-trafego-meta.


============================================================
O PROCESSO, EM 7 PASSOS (na ordem)
============================================================

1) ANGULO ANTES DA ARTE — 1 arte = 1 dor
   A peca nasce de um GANCHO por angulo de dor especifico do avatar, nao de
   "uma imagem bonita". Escreva 3-4 ganchos, cada um mordendo UMA dor
   diferente da mesma pessoa. Nunca uma arte generica pra todo mundo.
   Exemplo real (dentista, MEP): "Voce domina a anatomia da face. E a
   pele?" · "Ela resolve o dente com voce. E a pele, fecha com outro." · "A
   mesma paciente pode valer muito mais." · "Na pele, voce decide ou
   adivinha?" — 4 dores distintas, 1 avatar.

2) FOTO REAL DA AUTORIDADE — nunca banco de imagem
   Rosto real da especialista, tratado (P&B, crop face-aware que NUNCA corta
   a cabeca). Stock nasce fraco. Todo especialista precisa de um banco de
   foto proprio; sem isso o criativo ja larga atras. O motor tem o crop
   face-aware (soft-criativo-lote/scripts/facecrop.py).

3) IDENTIDADE TRAVADA NUM JSON — cor/fonte/selo/CTA, nao chute
   Vermelho da casa, fonte, selo ("PARA <NICHO> · AULA GRATUITA"), CTA
   ("Cadastre-se") saem de um identidade.json. E ISSO que torna o metodo
   portavel: troca o JSON, mesmo motor cospe a identidade de outro cliente
   sem redesenhar nada. Formato: soft-criativo-lote/references/identidade.md.

4) RENDER EM LOTE — chama o motor
   Monta o manifesto.json (foto + gancho por peca) e roda:

       python3 ~/.claude/skills/soft-criativo-lote/scripts/lote.py manifesto.json

   Pra peca solo (anuncio de imagem unica: foto + gancho + sub + CTA) usa o
   modo peca_solo. Lote com checkpoint: se cair, roda de novo e retoma.

5) LINT ANTI-IA — obrigatorio ANTES de virar pixel
   Toda linha de copy passa no lint antes de renderizar. Depois de
   renderizado, corrigir texto custa o lote inteiro.

       python3 ~/.claude/skills/soft-designer/scripts/lint_copy.py peca.txt

   HARD (em-dash, familia "travar", palavra proibida) bloqueia.

6) PREVIA PRO DONO — ANTES de subir (regra que salvou refacao)
   Renderiza as previas e manda pro dono aprovar ANTES de criar campanha.
   Nunca sobe criativo sem o dono ver a previa. No caso dentista, o Andrei
   viu as 4 previas e so entao aprovou "as campanhas e as copys".

7) SOBE PAUSADO + UTM PADRAO
   Cria a campanha PAUSADA, com o UTM da casa pra casar lead com
   anuncio/adset. Padrao provado:
   utm_campaign=<FUNIL-FIXO> · utm_content={{ad.name}} · utm_term={{adset.id}}
   Subir/segmentar e com soft-trafego-meta.


============================================================
A REGRA-MAE: PUBLICO ANTES DE CRIATIVO
============================================================

Antes de trocar/matar um criativo, verifique o PUBLICO. Ficou provado no
MEP e no ERP: o MESMO criativo faz R$4/lead no publico aberto+lookalike e
R$66/lead num interesse forcado — 15x, mesma arte. No publico certo, TODOS
os criativos rodam na faixa boa; nenhum esta "morto".

Consequencia pro metodo:
- Criativo com CPL alto NAO e motivo pra refazer a arte antes de olhar em
  QUE publico ele rodou.
- A alavanca de custo esta no conjunto/publico, nao na peca, quando a peca
  ja passou pelos 7 passos.
- So se troca criativo quando ele esta ruim NO PUBLICO BOM.


============================================================
COMO CLONAR PRA QUALQUER ESPECIALISTA (4 CAMPOS)
============================================================

Especialista novo = preencher 4 campos e rodar os 7 passos. Template
completo em references/metodo-4-campos.md. Exemplo real preenchido (dentista)
em references/exemplo-dentista.md.

  CAMPO 1 — FOTO: banco de foto propria da autoridade, tratada (P&B).
  CAMPO 2 — IDENTIDADE: identidade.json (cor, fonte, selo, CTA da marca).
  CAMPO 3 — 4 GANCHOS: 4 dores distintas do avatar, 1 gancho por dor.
  CAMPO 4 — DESTINO: URL de inscricao + evento de conversao + UTM padrao.

Preencheu os 4 -> roda passo 4 a 7 -> previa -> sobe pausado.


============================================================
REGRAS DURAS (cada uma nasceu de um erro real que a casa pagou)
============================================================

1. VEU CLAREIA A BASE. No motor, o veu clareia pra base creme: o texto da
   1a linha ("tinta") tem que ser ESCURO, senao some. Sub usa cor mid-grey,
   nao clara.

2. SOLO NAO ACEITA --refazer. O flag --refazer so vale pra carrossel. Pra
   refazer peca solo: apaga out/progress.json + os jpgs e roda limpo, senao
   o checkpoint pula o item.

3. MANTER ACENTOS NO MANIFESTO. A fonte da casa (Bricolage 800) tem os
   glifos — Voce/Natalia/adivinha renderizam certo. Nao "despentelhar"
   acento no manifesto.

4. DEPLOY != COMMIT. Commitar a imagem no git NAO publica. As artes so ficam
   no ar depois do deploy (no caso MEP: bash deploy.sh, Cloudflare Pages).
   Anuncio que aponta pra imagem nao-deployada quebra.

5. PAGE/IG SAO BAKED NO CREATIVE. Page e Instagram ficam immutable no
   creative. Errar = refazer todos os creatives. Confirme a pagina certa
   ANTES (no MEP: pega do effective_object_story_id de um ad ATIVO, nao
   chuta). Nessa conta, NAO forçar instagram_user_id (token sem escopo IG);
   criar creative so com page_id que o IG vem da pagina.

6. LINT ANTES DE RENDERIZAR. Copy passa no lint antes de virar pixel.
   Depois, cada correcao custa um lote novo.

7. PREVIA ANTES DE SUBIR. O dono ve a previa antes de existir campanha.
   Sempre.


============================================================
COMO OUTRAS SKILLS PLUGAM ESTA
============================================================

Qualquer fluxo de especialista que va gerar criativo de anuncio deve, no
ponto em que decide as pecas, invocar esta skill (soft-criativo-campeao)
para rodar os 7 passos, e ela por sua vez chama:
  - soft-conteudo    -> se a copy/gancho ainda nao existe
  - soft-criativo-lote -> pra renderizar o lote
  - soft-designer/lint_copy.py -> gate anti-IA
  - soft-trafego-meta -> pra subir pausado

Ela e o orquestrador do "criativo que vende"; as outras sao as ferramentas.


============================================================
ARQUIVOS
============================================================

references/metodo-4-campos.md   template de 4 campos pra clonar por especialista
references/exemplo-dentista.md  o caso real (MEP dentista) preenchido ponta a ponta

Motor e insumos ficam em soft-criativo-lote (nao duplicar aqui):
  scripts/lote.py, scripts/motor.py (peca_solo), scripts/facecrop.py
  references/identidade.md, references/receita-carrossel.md, references/regras-visuais.md
Lint anti-IA em soft-designer/scripts/lint_copy.py.
