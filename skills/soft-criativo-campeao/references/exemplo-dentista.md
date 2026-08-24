# Exemplo real preenchido — MEP dentista (Natalia Fischer), 18/08/2026

Caso que gerou as 4 melhores pecas solo da casa. Serve de molde de como um
especialista fica com os 4 campos preenchidos.

## CAMPO 1 — FOTO
- Banco: assets/nat-ensaio/ (ensaio local da Natalia)
- Fotos por peca: 5726 / 5313 / 5507 / 5805
- Tratamento: P&B
- Crop face-aware conferido (facecrop.py) — cabeca inteira, ok

## CAMPO 2 — IDENTIDADE
- Cor principal: vermelho da casa 234,60,59
- Fonte: Bricolage 800
- Selo: "PARA DENTISTAS · AULA GRATUITA"
- CTA: "Cadastre-se"
- Formato: peca solo 1080x1350
- Pasta do lote: trabalho/trafego/2026-08-18-criativos-dentista-mep/
  (identidade.json + manifesto.json + out/D-DENT-0X.jpg)

## CAMPO 3 — 4 GANCHOS (1 dor cada) — todos passaram no lint
1. "Voce domina a anatomia da face. E a pele?"            (foto 5726)
2. "Ela resolve o dente com voce. E a pele, fecha com outro." (foto 5313)
3. "A mesma paciente pode valer muito mais."              (foto 5507)
4. "Na pele, voce decide ou adivinha?"                    (foto 5805)

## CAMPO 4 — DESTINO
- URL: https://treinamento.ibho.com.br/web-inscricao/
- Evento de conversao: LEAD (confirmado com o Andrei)
- Pixel: 1044640029284783
- Page: "Sucesso em HOF" 188715172023548 (pega do effective_object_story_id
  de um ad ATIVO da V2 — nao chutada). IG herdado da pagina
  (@nataliafischer.oficial). NAO forçar instagram_user_id nessa conta.
- UTM:
  - utm_campaign = MEP-PERP-F   (funil provado, mantido)
  - utm_content  = {{ad.name}}
  - utm_term     = {{adset.id}}

## Como foi ao ar
- Previas renderizadas -> Andrei aprovou as previas -> depois aprovou "as
  campanhas e as copys".
- Imagens copiadas p/ public/ads/mep-dentista/ e DEPLOYADAS (bash deploy.sh,
  Cloudflare Pages leo-mini-treino) -> URL
  https://leo-mini-treino.pages.dev/ads/mep-dentista/D-DENT-0X.jpg
- Campanha [006][MEP-PERP-V2][DENTISTA | ABERTO+ADV] criada PAUSADA, CBO
  R$100/dia, 4 ads, publico aberto+ADV (a regra-mae: publico bom, nao
  interesse forcado).

## Erros que a casa pagou nesse lote (viraram as regras duras da skill)
- Veu clareia a base creme -> texto da 1a linha tinha que ser ESCURO.
- Peca solo nao aceita --refazer -> apagar progress.json + jpgs e rodar limpo.
- Manter acentos no manifesto (Bricolage 800 tem os glifos).
- Deploy != commit -> imagem so no ar depois do deploy.
- Page/IG baked no creative -> confirmar page antes; nao forçar IG nessa conta.
