# O arquivo config.json

Fica ao lado da pasta `brain/`. Os caminhos são relativos à pasta do config.

| Campo | O que é |
|---|---|
| `titulo` | O nome que aparece no topo e no centro do mapa. |
| `subtitulo` | A linha de baixo. A data de hoje entra sozinha. |
| `raiz` | A pasta das notas. Padrão `brain`. |
| `saida` | Onde a página é gravada. Padrão `cerebro-site`. |
| `logo` | Imagem opcional (caminho). Vazio, sem logo. A imagem entra dentro da página. |
| `texto` | `resumo` (padrão: 700 primeiros caracteres da nota no painel), `completo` ou `nenhum` (a página não leva o conteúdo das notas, só os nomes). Use `nenhum` em endereço público. |
| `hubs` | Os núcleos, as grandes áreas. De 6 a 12. Cada um: `id`, `nome` e, se quiser, `cor` (`#rrggbb`). |
| `conceitos` | As palavras que costuram o cérebro. De 15 a 40. Cada um: `id`, `nome`, `hub`, `regex`. |
| `pastas` | Quais arquivos entram e em qual núcleo. |
| `notas_especiais` | O MAPA e a memória viva: ficam maiores e ligam no centro. |
| `pessoas` | Opcional. Cada pessoa: `id`, `nome`, `hub`, `conceitos` (lista de ids). |
| `acentos` | Corrige rótulos que vêm de nome de arquivo sem acento: `{"precos": "Preços"}`. Só vale para nota sem título `#`. |

## Um conceito

```json
{ "id": "oferta", "nome": "Oferta principal", "hub": "negocio", "regex": "oferta|programa" }
```

Toda nota que tiver "oferta" ou "programa" no texto se liga a ele. Acento não atrapalha: "diagnostico" encontra "diagnóstico".

## Uma pasta

```json
{ "caminho": "arquivo/*.md", "hub": "memoria", "rotulo_por_data": true, "liga_a": ["MEMORIA-VIVA.md"] }
```

- `caminho`: padrão relativo à `raiz`.
- `rotulo_por_data`: o rótulo vira `DD/MM/AAAA` quando o arquivo começa com a data.
- `liga_a`: liga cada arquivo da pasta a outro (por exemplo o diário à memória viva).
- Para cada pasta de entrega virar um ponto no mapa: `{ "caminho": "../trabalho/*/*/*/", "hub": "entregas", "tipo": "pastas" }` (a pasta pode ter um `README.md` com o resumo).

Quando duas pastas pegam o mesmo arquivo, vale a primeira da lista. Ponha a mais específica antes (`PESSOA-*.md` antes de `*.md`).

## Dicas

- Regex curta e específica. Palavra comum liga tudo com tudo.
- O rótulo de cada nota é o primeiro `# Título` dela (até 40 caracteres). Sem título, vale o nome do arquivo.
- Arquivo ou pasta que começa com `_` fica de fora, e a pasta `ESTADO` também.
