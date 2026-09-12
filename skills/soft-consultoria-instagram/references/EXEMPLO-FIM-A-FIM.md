# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** O perfil, os números, as notas, os textos e o resultado foram
> inventados só pra mostrar a FORMA de cada saída. Nada disso é caso real e nada disso pode ser
> copiado pra uma entrega de verdade.

**O caso fictício:** um perfil de uma arquiteta que faz projeto de reforma de apartamento pequeno.
Perfil fictício `@estudio_treze_m` (nome inventado), 11 mil seguidores, posta 4 vezes por semana,
grade bonita, quase nenhuma mensagem chegando. Objetivo comercial declarado: agendar 4 conversas de
projeto por mês, ticket de 6 mil.

Este arquivo mostra a saída resumida das 4 etapas, na ordem, mais o `audit-score.json` preenchido.

---

## O anúncio do plano, a primeira coisa que ela leu

> "Vou coletar o perfil, pontuar as 10 dimensões, diagnosticar o gargalo principal e gerar o
> relatório em markdown e em HTML. Vou parar duas vezes pra você conferir: uma quando eu fechar a
> nota, outra antes de gerar o arquivo final."

## As 3 perguntas do objetivo comercial

1. "O que você vende e por quanto?"
   > "Projeto de reforma de apartamento até 60 m². Fica em torno de 6 mil."
2. "Quem você quer que chegue nesse perfil?"
   > "Casal que acabou de comprar o primeiro apartamento pequeno e não sabe por onde começar."
3. "Qual o próximo passo que você quer que a pessoa dê?"
   > "Me chamar no direct pra marcar uma conversa."

---

## Etapa 1 · Coleta, o que entrou e o que faltou

Fonte usada: coleta externa pelo script, mais 4 prints que ela mandou.

| Superfície | Situação |
|---|---|
| bio e link | completo |
| grade | completo, 30 posts |
| carrosséis | 22 de 26 com todos os slides. 4 incompletos |
| reels da amostra | 5 de 9 transcritos |
| destaques | 6 de 6 |
| destino do link | completo, cai num Linktree com 7 botões |

Marcado `parcial`, e o motivo escrito: 4 carrosséis e 4 reels não vieram inteiros.

Cobertura geral calculada: **74%**. Acima do mínimo de 70%, então a nota saiu definitiva. Se
tivesse dado 61%, a nota sairia marcada `preliminar`, as dimensões sem prova sairiam nulas em vez de
baixas, e a skill teria parado pra perguntar se ela conseguia liberar o que faltava.

---

## Etapa 2 · O `audit-score.json` preenchido (3 das 10 dimensões, pra ver o formato)

```json
{
  "perfil": "@estudio_treze_m",
  "data": "2026-09-04",
  "objetivo_comercial": "4 conversas de projeto por mês, ticket 6000",
  "cobertura": {
    "dimensoes": 0.90,
    "fontes": 0.74,
    "geral": 0.74,
    "confianca": 0.78,
    "status": "definitiva"
  },
  "dimensoes": [
    {
      "id": 1,
      "nome": "Posicionamento e comprador",
      "peso": 12,
      "score": 2,
      "evidence_quality": 0.9,
      "marca": "observado",
      "parametro": "o perfil diz para quem existe e que problema ocupa",
      "observado": "a bio diz 'arquitetura afetiva e atemporal'. Nenhuma das 30 legendas nomeia apartamento pequeno, metragem, ou casal comprando o primeiro imóvel.",
      "por_que_nao_menor": "existe uma categoria clara (arquitetura) e a grade é coerente.",
      "por_que_nao_maior": "o comprador que ela declarou não aparece em nenhuma superfície do perfil.",
      "proximo_nivel": "a bio nomear a metragem e o momento de compra; 3 legendas da amostra falarem com esse casal."
    },
    {
      "id": 4,
      "nome": "Oferta, link e próximo passo",
      "peso": 14,
      "score": 1,
      "evidence_quality": 1.0,
      "marca": "observado",
      "parametro": "o visitante sabe o que comprar e como avançar",
      "observado": "o link leva a uma página com 7 botões, sendo 3 mortos. Nenhum post da amostra tem chamada. A palavra 'projeto' aparece 2 vezes em 30 legendas.",
      "por_que_nao_menor": "existe um link e um canal de mensagem aberto.",
      "por_que_nao_maior": "não há um próximo passo único, e o caminho até a conversa tem 3 cliques.",
      "proximo_nivel": "link único para a conversa, e chamada explícita em pelo menos 1 post por semana."
    },
    {
      "id": 9,
      "nome": "Prova",
      "peso": 9,
      "score": null,
      "evidence_quality": 0,
      "marca": "não determinável externamente",
      "parametro": "o perfil mostra resultado de cliente com contexto",
      "observado": "os 4 carrosséis que não vieram inteiros são justamente os de antes e depois. Sem eles, não dá para pontuar prova.",
      "por_que_nao_menor": "ausência de acesso não equivale a ausência de prova.",
      "por_que_nao_maior": "sem os slides, não há evidência.",
      "proximo_nivel": "ela mandar os 4 carrosséis completos."
    }
  ]
}
```

### O que o cálculo devolveu

```bash
python3 scripts/calcular_pontuacao.py audit-score.json
```

```
nota: 41 / 100  (definitiva)
cobertura das dimensões: 90%
cobertura das fontes: 74%
cobertura geral: 74%
confiança: 78%
teto comercial: o perfil sustenta atenção, não sustenta decisão de compra.
dimensões nulas: 1 (Prova)
```

**STOP.** A pergunta que a skill fez:

> "A nota é 41, com 74% de cobertura. O que mais pesa é que o casal que você quer não aparece em
> nenhuma superfície do perfil, e que o caminho até a conversa tem 3 cliques. Essa leitura bate com o
> que você vê? E consegue me mandar os 4 carrosséis de antes e depois, que são os que faltaram?"

---

## Etapa 3 · Diagnóstico, resumido

**Gargalo de maior impacto: o número 1 da ordem, comprador e tese.** A grade é bonita e coerente, e
fala com arquitetos, não com o casal que acabou de comprar 48 m². Todo o resto (link, chamada,
destaque) é sintoma disso: não existe próximo passo porque não existe pra quem.

Classificação das conclusões:
- `observado`: a bio não nomeia metragem nem momento de compra; o link tem 7 botões, 3 mortos.
- `inferido`: a ausência de mensagem chegando vem da ausência de próximo passo, sustentado pela
  contagem de chamadas (zero em 30 posts) e pelo caminho de 3 cliques.
- `hipótese`: o público atual pode ser majoritariamente de colegas de profissão, o que explicaria
  salvamento alto e mensagem baixa. Precisa dos dados internos dela pra validar.
- `não determinável externamente`: quantas pessoas chegaram a abrir o Linktree.

### As correções, com texto pronto

**Bio (texto pronto, é só colar):**

> Reforma de apartamento de até 60 m².
> Projeto que cabe na planta que você comprou.
> Primeira conversa sem custo, no botão abaixo.

**Link:** um só, direto pra conversa. Os 7 botões saem.

**Destaques, os 6 renomeados:**
`48 m² · antes e depois` · `Quanto custa` · `Como funciona` · `Marcenaria` · `Dúvidas de quem comprou` · `Fale comigo`

**Os 3 fixados:**
1. o antes e depois do apartamento de 48 m², com a planta;
2. "quanto custa um projeto de apartamento pequeno", com faixa e o que entra;
3. "os 4 erros de quem reforma antes de ter projeto".

**Rota de conversão:** post fala do problema do casal, chamada manda pra mensagem com uma palavra
combinada, a resposta pergunta a metragem e o momento da obra, e daí sai a conversa.

**Séries editoriais, 3:**
- "Planta de verdade": ela pega uma planta real de apartamento pequeno e mostra a decisão.
- "Quanto custa": faixa de preço por item, sem promessa.
- "Comprei, e agora": o passo a passo dos primeiros 30 dias depois da chave.

**Plano por prazo:**
- 48 horas: trocar a bio e o link, renomear os 6 destaques.
- 7 dias: publicar os 3 fixados.
- 30 dias: rodar as 3 séries, 1 post de cada por semana, e medir mensagem recebida por semana.

---

## Etapa 4 · Entrega

```
audit-score.json
relatorio-estudio-treze-m.md
relatorio-estudio-treze-m.html
```

### O gate, como foi preenchido

| Critério | Resultado |
|---|---|
| Testes da skill | `test_calculadora.py`, `test_estado.py`, `test_relatorio.py` passaram |
| Pontuação honesta | a dimensão Prova saiu `null`, não saiu 0 |
| Cobertura declarada | 74%, nota definitiva, declarada na abertura |
| Retomada | o estado gravou depois de cada superfície; a segunda rodada não recoletou nada |
| HTML fechado | nenhum marcador sobrou, o arquivo abre sozinho |
| Prova visual | aberto em computador e celular, print guardado; o cabeçalho cortava no celular e foi ajustado |
| Identidade | o relatório usa a identidade fixa desta skill, não o logo nem a cor dela |
| Anti-IA | a copy da bio e dos destaques passou no crivo, exit 0 |
| Publicação | nada foi publicado, tudo entregue pra ela aplicar |

---

## O que teria mudado com cobertura baixa

Se ela tivesse mandado só a bio e 6 posts, a cobertura ficaria em torno de 40%. Nesse caso:

- a nota sairia como **41 (preliminar)**, com a palavra na abertura do relatório, não no rodapé;
- 5 das 10 dimensões sairiam com `score: null` e `evidence_quality: 0`;
- o relatório abriria com a lista do que falta: os carrosséis inteiros, as transcrições dos reels, os
  destaques e o destino do link;
- o diagnóstico continuaria saindo, porque o gargalo de comprador aparece já na bio;
- nenhuma prioridade se apoiaria em dimensão nula.
