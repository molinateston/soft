# Template dos 4 campos: clonar o criativo campeao pra um especialista novo

Preencha os 4 campos abaixo. Preencheu = roda os passos 4 a 7 do metodo
(render -> lint -> previa -> sobe pausado). Enquanto um campo estiver vazio,
NAO renderiza.

---

## CAMPO 1: FOTO DA AUTORIDADE
- Onde esta o banco de foto propria da especialista (pasta):
- Foto(s) escolhida(s) por peca (arquivo original, nunca thumbnail):
- Tratamento: P&B? colorida? (P&B e o padrao, por destacar o texto)
- Conferido que o corte nao come a cabeca (topo do cabelo e queixo dentro do quadro, com folga)? (sim/nao)

> Regra: foto REAL da autoridade tratada. Nunca banco de imagem. Sem banco de
> foto proprio, o criativo ja nasce fraco: resolver ISSO antes de renderizar.

## CAMPO 2: IDENTIDADE (identidade.json)
- Cor principal (RGB da marca):
- Fonte (arquivo da fonte, caminho; confira que ela tem os glifos acentuados):
- Selo/tag do topo ("PARA <NICHO> · AULA GRATUITA" ou equivalente):
- CTA do botao ("Cadastre-se" / "Quero participar" / ...):
- Assinatura (@perfil):

> O identidade.json mora na PASTA DE TRABALHO do lote, uma copia por
> cliente. Nada de cor, fonte, selo ou CTA escrito no codigo: tudo no JSON.

## CAMPO 3: 4 GANCHOS POR DOR (1 arte = 1 dor)
Escreva 4 ganchos, cada um mordendo UMA dor diferente do MESMO avatar. Passe
cada um no lint anti-IA antes de aprovar.

1. (dor A):
2. (dor B):
3. (dor C):
4. (dor D):

> Nunca uma arte generica pra todo mundo. Se dois ganchos mordem a mesma dor,
> um deles esta sobrando: troque por outra dor.

## CAMPO 4: DESTINO (link + evento + UTM)
- URL de inscricao/destino:
- Evento de conversao (Lead? CompleteRegistration? conversao custom?):
- Pixel/dataset id:
- Page id da marca (confirmado, nao chutado):
- UTM padrao:
  - utm_campaign = <FUNIL-FIXO do funil provado>
  - utm_content = {{ad.name}}
  - utm_term = {{adset.id}}

> Page/IG ficam BAKED no creative (immutable). Confirme a pagina ANTES de
> criar os creatives: errar = refazer tudo.

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

---

## Detalhe do render (passos 3 a 5 da Ação 1)

A regra que decide mora no SKILL.md, no passo. Aqui fica o como e o porquê.

### Foto e corte (passo 3)

Rosto real do especialista, tratado em preto e branco. Foto de banco nasce fraca. Antes de cortar, meça onde ficam o topo do cabelo e o queixo no arquivo original e mantenha os dois dentro do quadro com folga. Se a ferramenta de corte não achar o rosto sozinha, enquadre pelo olho e confira quadro a quadro.

### O `identidade.json` (passo 4)

Campos mínimos, com a origem de cada campo preenchido no objeto `origens`:

```json
{
  "cor_principal": [17, 17, 17],
  "cor_fundo": [250, 249, 246],
  "cor_texto_sobre_veu": [17, 17, 17],
  "cor_sub": [110, 110, 110],
  "fonte": "caminho/do/arquivo/da/fonte.ttf",
  "selo": "PARA <NICHO> · AULA GRATUITA",
  "cta": "Cadastre-se",
  "assinatura": "[A CONFIRMAR: @ do perfil, confirmado pelo dono]",
  "formato": [1080, 1350],
  "origens": {"cor_principal": "dono.md:12", "selo": "dono.md:30"}
}
```

Por que o JSON: troca o arquivo e o mesmo render cospe a identidade de outro cliente sem redesenhar nada. Por que o @ nunca é deduzido: um @ errado publicado é um anúncio apontando pro perfil de outra pessoa, e deduzir do nome do negócio ou do domínio não vale como confirmação. Por que a cor em palavra não vira RGB: "off-white" ou "acento verde" têm dezenas de valores, e o número adivinhado sai no feed como se fosse da marca.

### O `manifesto.json` (passo 5)

Uma entrada por peça:

```json
{
  "pecas": [
    {
      "foto": "fotos/autoridade-01.jpg",
      "gancho": "Você monta o plano. Quem segura a adesão?",
      "sub": "O que muda quando o retorno vira parte do protocolo.",
      "cta": "Comenta ADESAO aqui embaixo que eu te mando o roteiro",
      "texto_anuncio": "O plano funciona no papel. O retorno é onde o paciente decide ficar.",
      "titulo_anuncio": "O retorno que segura a adesão",
      "saida": "out/peca-01-adesao.jpg"
    }
  ]
}
```

A 1ª linha do `texto_anuncio` é a segunda coisa que o público lê. Trocar só texto e título, sem mexer na arte, é o teste mais barato quando a peça já vende.

### Por que as regras do CTA e da ressalva são duras

- **Chave `cta` nunca apagada.** Uma rodada tirou o marcador do CTA e o motor tirou a chamada à ação junto: quatro anúncios sem uma linha de ação, e o gate passou.
- **Palavra-chave sozinha não é CTA.** Uma rodada fechou três de quatro peças em `manda BASE40 no WhatsApp` sem dizer o que a pessoa ganha ao mandar. O certo: `manda BASE40 no WhatsApp que eu te mando a aula gratuita de 20 min`.
- **Ressalva só na última peça.** Colada embaixo de peça do meio, ela corta o gancho e some antes do CTA da última.

### A ferramenta de render, nesta ordem

1. um script de render que já venha com as skills de design instaladas (por exemplo em `soft-designer/scripts/`), chamado no shell;
2. um script próprio curto, na pasta de trabalho, com a biblioteca de imagem do ambiente (Pillow ou equivalente), lendo `identidade.json` e `manifesto.json`;
3. sem shell nem biblioteca de imagem: a skill não inventa pixel. Entrega `spec-render.md` com foto, texto exato, posição, cor, fonte e tamanho por peça, e segue nos passos 6 e 7.

Peça solo é anúncio de imagem única (foto, gancho, sub, CTA). O lote roda com checkpoint em `out/progress.json`: se cair, roda de novo e retoma de onde parou.

### Quando o checkpoint falha no meio do lote

- Peça que gravou no `progress.json` e tem arquivo em `out/` está pronta e não roda de novo.
- Peça que gravou e não tem arquivo está corrompida: apague a entrada dela e o jpg parcial, e rode outra vez.
- Duas falhas seguidas na MESMA peça param o lote: mostre o erro cru ao dono em 3 linhas, sem terceira tentativa.
- Glifo ausente na fonte não se retenta: troque a fonte no `identidade.json` e rode o lote inteiro.
