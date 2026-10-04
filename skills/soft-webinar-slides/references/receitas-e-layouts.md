# Rascunho de texto: o deck.json e os 13 layouts de molde

Fora do fluxo padrão. O `gerar.py` monta um deck pelos layouts de molde a partir do `deck.json`: serve pra ver rápido o texto de cada tela ou testar o motor, nunca como entrega (o resultado é slide de texto e foi reprovado pelo dono). A entrega é o brief do Claude Design ou o deck desenhado pelo agente (`receitas-visuais.md`). Os moldes abaixo trazem só lacunas.

## Estrutura

```json
{
  "titulo": "[DO DONO: nome da aula]",
  "perguntas": ["pergunta ao dono que não é de um slide só"],
  "bastidor": ["nota de bastidor que vai pro _notas-operador.md"],
  "slides": [
    {
      "nome": "nome curto do slide, só pras notas",
      "bloco": "Abertura",
      "layout": "frase",
      "...": "campos do layout",
      "notas": {
        "objetivo": "", "abre": "", "cliques": [""], "fecha": "", "transicao": "",
        "hora": "", "pode_pular": false,
        "publicos": {"quem ainda não faz": "", "quem está começando": "", "quem já é aluno": ""},
        "confirmar": ["o que ainda não é fato"],
        "historico": ["Mudou ([data], pedido de [quem])", "Saiu da tela: [o quê]"]
      }
    }
  ]
}
```

- `bloco`: o bloco da aula. O fundo troca (claro e escuro) quando o bloco muda, nunca slide a slide.
- `*palavra*` em qualquer texto de tela pinta a palavra na cor de destaque. Use em uma ou duas palavras, nunca na frase inteira.
- `notas.cliques` tem uma linha por clique da tela, na ordem. O `checar_deck.py` reprova quando o número não bate.
- `notas.confirmar` vira [A CONFIRMAR] na nota e pergunta no `_notas-operador.md`. Nunca na tela.
- `notas.transicao`, `notas.fala` (fala corrida sem clique) e `notas.obs` (lista) entram na nota como estão. O `ler_roteiro.py --rascunho` já preenche os três a partir do roteiro.
- `publicos` só com resposta que o insumo sustenta; sem isso, o campo fica de fora.

## Os 13 layouts

Na coluna "cliques", o que entra por clique, na ordem. O que não está ali já está na tela quando o slide abre.

| layout | campos | cliques | receita do guia |
|---|---|---|---|
| `capa` | promessa, apoio?, apresentador? | nenhum | promessa com as palavras do público |
| `frase` | rotulo?, frase, depois[]?, pilula? | cada `depois`, depois a pílula (aparecer) | combinado, afirmação ousada, pergunta pro chat, respiro |
| `lista` | rotulo?, frase?, itens[], conclusao? | cada item, a conclusão por último | desculpas nomeadas, loops abertos, recap |
| `cronograma` | rotulo?, linhas[{hora?, texto, oferta?}] | cada linha | cronograma sincero (a linha da oferta com `oferta: true`) |
| `escada` | rotulo?, pergunta?, degraus[{nome, promessa}], atual?, aqui?, revelar?, pergunta_clique? | cada degrau de baixo pra cima (se `revelar`), a pergunta (se `pergunta_clique`) | esquema principal, "você está aqui", decisão antes do pitch, módulos da oferta |
| `bussola` | rotulo?, passos[], atual | nenhum | mecanismo: feito riscado, atual grande, próximo apagado |
| `numero` | rotulo?, frase?, visual | depende do visual | número vira imagem |
| `print` | rotulo?, legenda, imagem? | nenhum | prova grande, sem moldura |
| `duas_colunas` | rotulo?, frase?, esquerda{titulo, itens}, direita{titulo, itens}, fecho? | esquerda, direita, fecho | dois caminhos, responsabilidade |
| `preco` | rotulo?, frase?, de, percentual?, parcela, avista? | risco, selo do percentual, a parcela | preço cortado em degraus |
| `oferta` | rotulo?, linhas[{item, valor, bonus?}], novas[]?, total_declarado?, percentual?, parcela?, avista?, link?, prazo{texto, motivo}?, chamada?, rotulo_total?, animar? | cada linha em `novas`, o total, o risco, o percentual, o painel | o carrinho, a tabela que volta a cada 2 bônus |
| `bonus` | tarja?, logo? ou nome, dor, promessa, aprende[], valor?, rotulo_aprende? | cada item de `aprende`, o valor, o risco, "R$0 pra você" com o valor oficial | bônus como produto inteiro |
| `cta` | rotulo?, frase, link, apoio? | o link (aparecer), o apoio | os CTAs |

### numero: os três visuais

- `{"tipo": "calendario", "total": 12, "marcados": [N], "rotulos": [...]}`: uma célula por mês ou dia; os marcados ganham um X no mesmo clique. `total` e `marcados` saem do insumo (meses ou dias de custo que o dono declarou).
- `{"tipo": "por_dia", "grande": "R$[valor]", "unidade": "por dia", "conta": "R$[parcela] ÷ 30 dias"}`: o valor por dia é a parcela do insumo dividida por 30; a conta entra no clique.
- `{"tipo": "comparacao", "barras": [{"rotulo": "", "valor": 0, "texto": "", "forte": true}]}`: barras proporcionais ao `valor`; uma barra por clique; `forte` pinta na cor de destaque.

### oferta: as regras que o script garante

- Toda linha precisa de `valor` numérico do insumo. Linha sem valor barra a montagem: a tabela sai e o valor vira pergunta.
- O total é a soma das linhas na tela; com `total_declarado`, o script compara e barra se não bater.
- Mais de 14 linhas barra: divida a pilha em duas telas (a tabela volta a cada 2 bônus).
- Geometria por número de linhas: até 8, de 9 a 11, 12, de 13 a 14. Nome que não cabe numa linha nem a 24px reprova no `checar_deck.py`: encurte o nome na tela e deixe o nome inteiro na nota.
- `prazo` sem `motivo` barra.
- O `percentual` fica ao lado do total riscado (ele é o desconto do à vista sobre o total). Só entra se o insumo trouxer o número.
- `animar: false` mostra a tabela inteira parada: é a tela fixa das perguntas.
- Sem `parcela`, `avista` e `link`, a tabela sai sozinha, centrada, sem painel e sem risco no total: é a tabela que cresce antes do preço.
- A tabela que cresce a cada 2 bônus: repita o slide `oferta` com as linhas que já foram mostradas e marque em `novas` só as que entram agora.

### bonus e print

- `tarja` só com o critério do dono; `logo` é o caminho da imagem (sem logo, o `nome` vira selo); `valor` só o declarado; até 4 itens em `aprende`.
- `imagem` do print é o caminho do arquivo (copiado pra `img/`); sem imagem, a vaga tracejada e o pedido ao dono. A legenda é o nome do print.

A condição de entrada de cada bloco (sem o dado, o bloco sai e vira pergunta) é a mesma do modo agente: `receitas-visuais.md`.
