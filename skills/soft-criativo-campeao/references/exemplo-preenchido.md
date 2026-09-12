# Exemplo preenchido (caso FICTICIO): nutricionista esportiva

Caso inventado, so pra mostrar como um especialista fica com os 4 campos de
pe. Nenhum numero, URL, id ou nome aqui e real: nao copie nada, preencha com
os dados do proprio dono.

## CAMPO 1: FOTO
- Banco: assets/ensaio-especialista/ (ensaio proprio, feito pra isso)
- Fotos por peca: 4 arquivos originais distintos, um por gancho
- Tratamento: P&B
- Corte conferido: topo do cabelo e queixo dentro do quadro, com folga

## CAMPO 2: IDENTIDADE
- Cor principal: a cor da marca do dono, em RGB
- Fonte: a fonte da marca, arquivo conferido com glifos acentuados
- Selo: "PARA NUTRICIONISTAS · AULA GRATUITA"
- CTA: "Cadastre-se"
- Formato: peca solo 1080x1350
- Pasta do lote: trabalho/trafego/<data>-criativos-<nicho>/
  (identidade.json + manifesto.json + out/PECA-0X.jpg)

## CAMPO 3: 4 GANCHOS (1 dor cada), todos passaram no gate anti-IA
1. "Voce monta o plano. Quem segura a adesao?"          (foto 1)
2. "O atleta melhora e some. E a consulta seguinte?"    (foto 2)
3. "O mesmo paciente pode valer o dobro."               (foto 3)
4. "Na periodizacao, voce decide ou repete?"            (foto 4)

Quatro dores distintas, um avatar so. Se dois ganchos mordem a mesma dor, um
deles esta sobrando.

## CAMPO 4: DESTINO
- URL: a pagina de inscricao do dono, ja publicada e aberta no navegador
- Evento de conversao: LEAD (confirmado com quem opera a conta)
- Pixel/dataset id: o da conta do dono
- Page id: lido de um anuncio ATIVO da propria conta, nunca chutado. O
  Instagram vem herdado da pagina
- UTM:
  - utm_campaign = <FUNIL-FIXO do funil provado>
  - utm_content  = {{ad.name}}
  - utm_term     = {{adset.id}}

## Como um lote assim vai ao ar
- Previas renderizadas -> dono aprova as previas -> so depois aprova as
  campanhas e as copys.
- Imagens copiadas pra pasta publica do site e DEPLOYADAS. Abra a URL final
  de cada imagem no navegador antes de apontar o anuncio pra ela.
- Campanha criada PAUSADA, com verba diaria combinada, um anuncio por
  gancho, publico aberto mais lookalike (a regra-mae: publico bom, nao
  interesse forcado caro).

## Erros que viraram as regras duras da skill
- Veu clareia a base creme, entao o texto da 1a linha tem que ser ESCURO.
- Refazer peca solo exige limpar o progress.json e os jpgs daquela peca.
- Manter acentos no manifesto e testar uma peca antes do lote inteiro.
- Deploy nao e commit: imagem so no ar depois do deploy.
- Pagina e Instagram ficam fixados no creative: confirmar a pagina antes.
