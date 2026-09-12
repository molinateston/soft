# Rubrica de sistema comercial: 100 pontos

## Escala comum

Pontue cada dimensao de `0` a `5`:

- `0`: contraditorio ou claramente ausente nas superficies auditadas;
- `1`: fragmentos isolados, sem funcao consistente;
- `2`: emergente, reconhecivel em algumas pecas;
- `3`: funcional, coerente na maior parte da amostra;
- `4`: forte, integrado e repetido com variacao;
- `5`: nivel benchmark: claro, memoravel, integrado e comercialmente consequente.

Use `null` quando nao houver acesso suficiente. `Nao observado` nao equivale a `0`.

No relatorio, cada nota deve responder quatro perguntas:

1. qual e o parametro buscado;
2. o que foi observado;
3. por que a nota nao e menor nem maior;
4. qual mudanca observavel leva ao nivel seguinte.

Uma descricao generica da dimensao nao explica a nota.

## Dez dimensoes

### 1. Posicionamento e comprador: peso 12

Mede se o perfil deixa claro para quem existe, qual problema ocupa, que transformacao oferece e por que isso importa agora.

### 2. Mecanismo e diferenciacao: peso 14

Mede se existe uma explicacao propria de como o resultado acontece, preferencialmente nomeavel, e se ela diferencia o perfil de alternativas comuns.

### 3. Narrativa e mudanca de crenca: peso 12

Mede tese-mae, inimigo ou modelo antigo, tensao recorrente, futuro desejado e progressao entre conteudos.

### 4. Vocabulario e repeticao: peso 8

Mede termos-assinatura, consistencia semantica e capacidade de repetir a tese por diferentes angulos sem publicar copias do mesmo conteudo.

### 5. Arquitetura editorial: peso 10

Mede se Reels, carrosseis, Stories, destaques e posts desempenham trabalhos identificaveis: atrair, nomear, explicar, provar, mostrar, relacionar e converter.

### 6. Prova e credibilidade: peso 8

Mede demonstracoes, objetos-prova, casos autorizados, processo visivel, clareza de status e separacao entre prova, conceito, simulacao e claim.

### 7. Funil e proximo passo: peso 12

Mede CTAs por estagio, microconversoes, continuidade entre post, perfil, DM, grupo, pagina ou oferta e ausencia de becos sem saida.

### 8. Bio, link e oferta: peso 10

Mede se nome, bio, link, fixados e destaque comercial apresentam comprador, mecanismo, promessa, oferta ou proximo passo coerente.

### 9. Voz, ambiencia e encarnacao: peso 8

Mede reconhecimento de voz, comportamento, roupa, ambiente, relacoes, mundo e continuidade. Nao exige lifestyle; exige sinais proprios adequados ao negocio.

### 10. Perfil como sistema: peso 6

Mede se a experiencia completa parece uma unica marca: grade, capas, destaques, series, frequencia semantica e rota comercial reforcam a mesma espinha dorsal.

## Evidencia e confianca

Para cada dimensao, atribua `evidence_quality`:

- `0`: sem evidencia direta;
- `1`: uma evidencia fraca, ambigua ou resumida por terceiro;
- `2`: duas ou mais evidencias diretas na mesma superficie, ou artefato fornecido bem documentado;
- `3`: evidencia primaria verificada diretamente em diferentes superficies ou formatos.

## Cobertura das fontes

Pontuar todas as dimensoes nao significa ter verificado o perfil inteiro. O JSON deve incluir seis superficies:

- `profile_surface`: nome, bio, contagens, fixados e grade;
- `posts_sample`: amostra definida e pecas individuais;
- `carousels`: todos os slides dos carrosseis incluidos;
- `reels`: hook, fala ou transcricao, legenda, CTA e ambiente;
- `highlights`: nomes e conteudo dos destaques relevantes;
- `link_destination`: destino e continuidade do link da bio.

Use um dos status:

- `verified`: fonte primaria verificada integralmente;
- `partial`: resumo, amostra incompleta ou acesso parcial;
- `not_accessed`: superficie relevante nao acessada;
- `not_applicable`: formato realmente inexistente, depois de verificar a superficie do perfil.

Pesos: perfil `15`, posts `25`, carrosseis `15`, Reels `20`, destaques `10`, destino do link `15`. Itens `not_applicable` saem do denominador.

## Tetos comerciais

Aplicar somente quando as dimensoes criticas foram avaliadas:

- Se `posicionamento` ou `mecanismo` receber `0` ou `1`, a nota final nao pode exceder `59`.
- Se `funil` e `bio_link_oferta` receberem ambos `0` ou `1`, a nota final nao pode exceder `69`.

O teto impede que estetica, volume ou acabamento compensem a falta de espinha comercial.

## Faixas de maturidade

- `90-100`: sistema comercial integrado.
- `80-89`: Marca comercial forte.
- `70-79`: Posicionamento funcional com lacunas.
- `55-69`: Sistema incompleto.
- `40-54`: Conteudo sem arquitetura comercial suficiente.
- `0-39`: Perfil fragmentado ou proposta ilegivel.

## Schema de `audit-score.json`

```json
{
  "profile": "@exemplo",
  "audited_at": "2026-08-27T14:00:00-04:00",
  "source_coverage": [
    {"id": "profile_surface", "status": "verified", "note": "Bio e grade abertas diretamente"},
    {"id": "posts_sample", "status": "verified", "note": "30 de 30 posts da amostra"},
    {"id": "carousels", "status": "partial", "note": "Dois carrosseis sem todos os slides"},
    {"id": "reels", "status": "verified", "note": "Hooks, falas, legendas e CTAs verificados"},
    {"id": "highlights", "status": "partial", "note": "Capas e nomes, sem todas as telas"},
    {"id": "link_destination", "status": "verified", "note": "Destino aberto e conferido"}
  ],
  "dimensions": [
    {
      "id": "posicionamento",
      "score": 4,
      "evidence_quality": 3,
      "evidence": [
        {"text": "Bio nomeia comprador e problema", "source": "perfil", "class": "observado"},
        {"text": "Post repete a tese", "source": "URL do post", "class": "observado"}
      ]
    }
  ]
}
```

Use exatamente estes ids:

`posicionamento`, `mecanismo`, `narrativa`, `repeticao`, `arquitetura_editorial`, `prova`, `funil`, `bio_link_oferta`, `encarnacao`, `perfil_sistema`.

Inclua as dez dimensoes. Cada evidencia pontuada e um objeto com `text`, `source` e `class`. As classes aceitas sao `observado`, `declarado`, `inferido`, `hipotese` e `nao_determinavel_externamente`. Qualidade 2 exige ao menos duas evidencias. Qualidade 3 exige ao menos duas fontes identificadas. Para dimensao nao avaliavel, use `"score": null`, `"evidence_quality": 0` e explique a limitacao em `evidence`.

O calculador retorna tres coberturas:

- `dimension_coverage_percent`: peso das dimensoes que puderam receber nota;
- `source_coverage_percent`: completude das superficies realmente verificadas;
- `coverage_percent`: a menor das duas, usada para definir o status.

O status numerico e `definitivo` somente quando `coverage_percent >= 70` e `confidence_percent >= 70`. Isso nao autoriza o rotulo `auditoria completa`: ele depende tambem dos gates de carrosseis, transcricoes, destaques e destino definidos em `references/coleta-visual.md`.
