# Formato de saida — Markdown -> Google Doc

Cada elemento de Markdown, como cai no Google Doc depois do pandoc + gog --convert-to doc.
Testado com o doc-exemplo (id 1pCfoX3htfNhPTRatIugXCGqDLc9pDCDydI1gryZJvQY, 13/08).

| No Markdown            | No Google Doc                         | Quando usar                          |
|------------------------|---------------------------------------|--------------------------------------|
| `# Titulo`             | Titulo (Title) grande                 | 1x no topo, nome do documento        |
| `## Secao`             | Cabecalho 1                           | cada grande secao (vira indice)      |
| `### Subsecao`         | Cabecalho 2                           | quebra dentro de uma secao           |
| `**texto**`            | negrito                               | enfase de termo/numero-chave         |
| `*texto*`              | italico                               | citacao, nome de obra, aparte        |
| `` `texto` ``          | fonte monoespacada                    | comando, campo, valor literal        |
| bloco com ``` ``` ```  | bloco de codigo cinza                 | trecho de comando/exemplo            |
| `- item`               | marcador                              | lista sem ordem                      |
| `1. item`              | lista numerada                        | passos/decisoes em ordem             |
| `- [ ]` / `- [x]`      | checkbox vazio / marcado              | checklist de tarefas                 |
| tabela com `|`         | tabela nativa (bordas, celulas)       | qualquer dado comparavel/numeros     |
| `---`                  | linha horizontal divisoria            | separar grandes blocos               |
| `[texto](url)`         | link clicavel                         | referencia externa                   |
| linha em branco        | novo paragrafo                        | respiro entre paragrafos             |

## Regras de diagramacao (o dono reprova o contrario)

- Nunca "titulo + um blocao de texto". Toda secao longa se quebra em subtitulos + bullets/tabela.
- Dado comparavel (preco por faixa, antes/depois, cronograma) SEMPRE em tabela, nunca em prosa.
- Enfase e negrito/italico, nunca CAIXA ALTA nem `_underline_`.
- Documento entregavel comeca com um `#` titulo e, se for longo, um `##` "Sumario" ou "Norte"
  no topo antes das secoes.

## Exemplo minimo que exercita todos os elementos

```markdown
# Relatorio Q4

## Resumo
Faturamento **cresceu 18%** vs *Q3*.

| Trimestre | Receita |
|-----------|---------|
| Q3        | 100     |
| Q4        | 118     |

## Proximos passos
1. Revisar `pipeline` de vendas
2. Fechar contratacao

- [x] Fechar Q4
- [ ] Planejar Q1

---
Documento gerado pelo LEON.
```
