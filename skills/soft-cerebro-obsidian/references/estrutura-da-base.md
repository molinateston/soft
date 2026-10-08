# Estrutura da base de notas

## As pastas

```
brain/
  MAPA.md            o índice: uma linha por nota, com o link e uma frase
  MEMORIA-VIVA.md    o que está valendo agora, a mais nova no topo
  NOTA-PERMANENTE.md um arquivo por assunto que não muda toda semana
  agentes/<area>/licoes.md   as regras que o dono ditou em cada área
  arquivo/           o diário antigo, um arquivo por dia (AAAA-MM-DD.md)
  ideias/            capturas soltas, por data
  ESTADO/            arquivos de robôs. Fica fora do mapa
trabalho/<area>/<AAAA-MM>/<AAAA-MM-DD-nome>/   tudo que foi produzido, uma pasta por entrega
```

Arquivo ou pasta que começa com `_` também fica fora do mapa.

## MAPA.md

É a porta de entrada. Seções: Negócio, Método, Pessoas, Números, Preferências do dono. Uma linha por nota:

```
- [[OFERTA-PRINCIPAL]]: produto, preço e entregas
```

Toda nota nova ganha uma linha aqui, no mesmo momento em que é criada.

## MEMORIA-VIVA.md

- Uma linha por fato, a mais nova no topo.
- Sempre com data e hora, e sempre dizendo onde está o arquivo da prova.
- Pendência começa com `PENDENTE:`.
- Passou de umas 150 linhas: mova as antigas para `arquivo/AAAA-MM-DD.md`. O que for permanente vira nota própria.

```
- [2026-01-15 10:00] Proposta modelo pronta. trabalho/comercial/2026-01/2026-01-15-proposta-modelo/
- [2026-01-15 09:10] PENDENTE: confirmar o valor do programa com o sócio.
```

## Notas permanentes

Uma nota por assunto estável: cliente ideal, oferta, preços, método, objeções, identidade visual, pessoas.

- Nome em maiúsculas com hífen: `OFERTA-PRINCIPAL.md`.
- A primeira linha é o título (`# Oferta principal`), com acento. O mapa usa esse título como rótulo.
- Ligue uma nota na outra com `[[NOME-DA-NOTA]]`. Cada link vira uma ligação no mapa.
- Escreva a fonte de cada fato que for número, preço ou nome ("conforme o dono em AAAA-MM-DD" ou o caminho do arquivo).
- Nada de segredo.

Molde:

```
# Título da nota

O fato principal em uma ou duas frases. Fonte: <de onde veio>.

Relacionado: [[OUTRA-NOTA]], [[MAIS-UMA]].
```

## Lições por área

Um arquivo por área, `agentes/comercial/licoes.md`, `agentes/conteudo/licoes.md`. Cada correção que o dono fizer vira uma linha com data. Antes de trabalhar numa área, o agente lê as lições dela.

```
- 2026-01-13 · Proposta sempre em PDF, nunca só no texto.
```

## A regra de gravar na hora

Bloco para o arquivo de instruções do projeto (o que o agente lê ao abrir o projeto). O `inicia.py --grava-claude-md` acrescenta exatamente isto:

```
## Memória do negócio (brain/)
- Antes de responder sobre histórico, decisões, números, pessoas ou preferências: abra brain/MAPA.md, ache a nota certa e responda a partir dela.
- Aprendeu algo novo? Grave NA HORA:
  - decisão do dia: linha no topo de brain/MEMORIA-VIVA.md com [data hora] e o caminho da prova;
  - fato permanente: nota em brain/ e linha no brain/MAPA.md, com [[links]];
  - correção numa área: linha em brain/agentes/<area>/licoes.md.
- Toda entrega vai para trabalho/<area>/<AAAA-MM>/<AAAA-MM-DD-nome>/
- Nunca guarde senha, chave de API ou dado sensível de cliente nessas notas.
```

No Claude Code o arquivo é o `CLAUDE.md` na raiz do projeto; no Codex é o `AGENTS.md`. Se o projeto usa outro agente, cole o bloco no arquivo de instruções dele.

## Usar no Obsidian

Abra o Obsidian, escolha "Abrir pasta como cofre" e aponte para `brain/`. Os `[[links]]` funcionam, e a visão de grafo do próprio Obsidian mostra as ligações. O mapa desta skill é uma página própria, pensada para ver núcleos, buscar e abrir no celular.
