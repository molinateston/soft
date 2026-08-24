# Template dos 4 campos — clonar o criativo campeao pra um especialista novo

Preencha os 4 campos abaixo. Preencheu = roda os passos 4 a 7 do metodo
(render -> lint -> previa -> sobe pausado). Enquanto um campo estiver vazio,
NAO renderiza.

---

## CAMPO 1 — FOTO DA AUTORIDADE
- Onde esta o banco de foto propria da especialista (pasta):
- Foto(s) escolhida(s) por peca (arquivo original, nunca thumbnail):
- Tratamento: P&B? colorida? (padrao da casa = P&B)
- Conferido que o crop face-aware nao corta a cabeca? (sim/nao)

> Regra: foto REAL da autoridade tratada. Nunca banco de imagem. Sem banco de
> foto proprio, o criativo ja nasce fraco — resolver ISSO antes de renderizar.

## CAMPO 2 — IDENTIDADE (identidade.json)
- Cor principal (RGB da marca):
- Fonte (arquivo .ttf, caminho absoluto):
- Selo/tag do topo ("PARA <NICHO> · AULA GRATUITA" ou equivalente):
- CTA do botao ("Cadastre-se" / "Quero participar" / ...):
- Assinatura (@perfil):

> Copie o exemplo soft-criativo-lote/assets/identidade-exemplo.json, nunca
> edite o original. Nada de cor/fonte/selo/CTA no codigo — tudo no JSON.

## CAMPO 3 — 4 GANCHOS POR DOR (1 arte = 1 dor)
Escreva 4 ganchos, cada um mordendo UMA dor diferente do MESMO avatar. Passe
cada um no lint anti-IA antes de aprovar.

1. (dor A):
2. (dor B):
3. (dor C):
4. (dor D):

> Nunca uma arte generica pra todo mundo. Se dois ganchos mordem a mesma dor,
> um deles esta sobrando — troque por outra dor.

## CAMPO 4 — DESTINO (link + evento + UTM)
- URL de inscricao/destino:
- Evento de conversao (Lead? CompleteRegistration? conversao custom?):
- Pixel/dataset id:
- Page id da marca (confirmado, nao chutado):
- UTM padrao:
  - utm_campaign = <FUNIL-FIXO do funil provado>
  - utm_content = {{ad.name}}
  - utm_term = {{adset.id}}

> Page/IG ficam BAKED no creative (immutable). Confirme a pagina ANTES de
> criar os creatives — errar = refazer tudo.

---

## Checklist antes de subir
- [ ] 4 ganchos passaram no lint anti-IA (HARD limpo)
- [ ] Previas renderizadas e enviadas pro dono
- [ ] Dono aprovou as pecas E as campanhas
- [ ] Imagens DEPLOYADAS (nao so commitadas) e URL no ar
- [ ] Campanha criada PAUSADA
- [ ] UTM conferido (casa lead com ad.name e adset.id)
- [ ] Regra-mae: o publico escolhido e o bom (aberto+lookalike), nao
      interesse forcado caro
