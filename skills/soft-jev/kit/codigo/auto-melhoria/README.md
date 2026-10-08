Auto-melhoria (ciclo noturno) — implementação de referência
=============================================================

Isto é uma implementação GENÉRICA e didática do método descrito em
`../../AUTO-MELHORIA.md`. Ela não chama nenhum serviço de verdade e não lê
nenhum histórico real: cada script traz dados fictícios embutidos e roda
sozinho, sem configuração nenhuma, só para você ver o método funcionando
ponta a ponta antes de ligar nos seus próprios dados.

Para usar com dados reais, o único ponto de extensão pensado de propósito é
a função `pontuacao_texto(pergunta, caso)` em `medir.py`: troque o corpo dela
por uma chamada real ao serviço de julgamento (TypeSafe/JEV — a mesma
credencial `TYPESAFE_API_KEY` e o mesmo formato de pergunta usados pelo
comando `jev ask` do restante deste kit), mantendo a assinatura da função.
Todo o resto (gabarito, split treino/teste, medição pareada, sombra, teto de
custo, calibração de limiar, promoção) já funciona sem mudar mais nada.

**Importante ao trocar por uma chamada paga:** passe sempre `--teto N` para
`propor_sombra.py` (e para `medir.py`, se chamado à mão) — veja "Teto de
custo" abaixo. Sem isso, nada limita quantas vezes o texto de produção pode
ser reavaliado por dia.

Onde tudo é gravado
--------------------

Por padrão os scripts gravam estado em `~/.local/share/jev-auto/auto-melhoria/`
(pasta criada sozinha no primeiro uso). Use `--dir CAMINHO` em qualquer
script para gravar em outro lugar, ou a variável de ambiente
`JEV_AUTOMELHORIA_DIR`.

Split treino/teste (por que um candidato não "avalia a si mesmo")
-------------------------------------------------------------------

`medir.dividir()` separa o gabarito em `selecao` (treino) e `teste`
(congelado), estratificado por rótulo. `propor_sombra.py` só olha a
`selecao` para propor um candidato, e só o `teste` para decidir se ele
"ganhou" da produção — nunca o mesmo conjunto nos dois papéis. A divisão é
congelada em `divisao.json`: caso novo entra num lado ou noutro por hash
determinístico (`sha256("42:id")`), sem nunca remexer nos ids antigos. Com
um gabarito pequeno (como o de exemplo deste kit) o lado de teste pode ficar
minúsculo e o resultado, ruidoso — isso é esperado, não é bug; cresça o
gabarito com `montar_gabarito.py` sobre dados reais para um teste mais
estável.

Teto de custo
--------------

`--teto N` em `medir.py`/`propor_sombra.py` limita a N o total de chamadas
ao julgador por dia, por rótulo — contado num `ledger.jsonl` compartilhado
entre os scripts (`medir.Orcamento`). Enquanto `pontuacao_texto` é a
heurística local grátis deste kit, o teto não muda nada na prática; ele
existe para já estar ativo no dia em que você trocar por uma chamada paga,
sem precisar mexer em mais nada. Sem `--teto` (ou `--teto 0`), não há
limite.

Ordem de execução
------------------

1. `python3 coletar.py` — lê históricos de conversa de um diretório
   configurável (`--entrada`) e produz `turnos.jsonl`. Sem `--entrada`, ou
   com o diretório vazio/inexistente, usa um conjunto pequeno de turnos
   fictícios embutidos, só para ter algo para os próximos passos
   processarem.
2. `python3 montar_gabarito.py` — lê `turnos.jsonl`, olha a reação humana no
   turno seguinte a cada resposta do agente (corrigiu, cobrou, confirmou) e
   produz `gabarito.jsonl`: um caso rotulado por linha.
3. `python3 medir.py` — mede o texto de produção (`producao.json`, criado com
   um exemplo na primeira vez) contra o gabarito: falso positivo, acerto,
   precisão, cobertura, AUC e custo (número de chamadas ao julgador). Rodar
   sozinho também mostra a mesma medição comparando produção × um candidato
   de exemplo, lado a lado.
4. `python3 propor_sombra.py [--teto N]` — a partir dos erros da produção na
   `selecao` (treino), gera um texto candidato, mede-o pareado contra a
   produção no `teste` (congelado), e grava o resultado em
   `sombra/candidatos.json` com `estado: "sombra"` se ganhou. Nunca toca em
   `producao.json`. Roda de novo todo dia; cada rodada também grava uma
   medição diária pareada em `sombra/diario.jsonl` (é esse log que vira a
   "semana em sombra" do passo 6).
5. `python3 calibrar_limiar.py` — mexe no LIMIAR em vez do texto: se a
   produção está acertando pouco no gabarito (abaixo de `--alvo-acerto`,
   padrão 70%, com pelo menos `--min-casos` casos), sobe o limiar aos poucos
   até o acerto voltar ao alvo ou até um teto de segurança (`--teto-limiar`,
   padrão 0,95). Nunca desce o limiar sozinho. Cada rodada grava uma linha
   em `calibracao-historico.jsonl`, mudando ou não.
6. `python3 promover.py [--dias-minimos 7]` — para cada candidato em sombra
   há tempo suficiente, decide: só promove se o candidato ganhou da produção
   no teste congelado E não piorou na semana em sombra (mínimo 5 medições
   para contar) E não piorou nenhum caso do arquivo de casos estáveis
   (`casos_estaveis.json`, com exemplos fictícios prontos — casos que a
   produção acerta hoje e que ninguém quer ver quebrar). Promovido =
   `producao.json` é sobrescrito com o texto do candidato. Reprovado ou
   bloqueado fica registrado no arquivo com o motivo e um histórico —
   nunca é apagado.
7. `python3 ciclo_noturno.py [--promover] [--dias-minimos N] [--teto N]` —
   chama os passos 1, 2, 4 e 5 acima em sequência (cada um como processo
   separado) e agrega o resultado num relatório só; com `--promover`,
   também chama o passo 6 no final. Pensado para rodar 1x por noite via
   cron, com `--promover` só uma vez por semana.

Exemplo de linha de cron (roda 1x por noite, promovendo 1x por semana):

```
0 3 * * *   /usr/bin/python3 /caminho/para/auto-melhoria/ciclo_noturno.py
0 3 * * 0   /usr/bin/python3 /caminho/para/auto-melhoria/ciclo_noturno.py --promover
```

Rodar `python3 ciclo_noturno.py --promover --dias-minimos 0` agora mesmo, num
diretório novo (`--dir`), já produz um ciclo completo de ponta a ponta com os
dados fictícios embutidos, incluindo uma promoção real — é o jeito mais
rápido de entender o fluxo antes de trocar pela fonte real. (`--dias-minimos
0` é só para ver o passo 6 acontecer na hora; no dia a dia deixe o padrão de
7 dias, que é o que dá tempo de a semana em sombra pesar na decisão.)

O que foi deixado de fora de propósito
----------------------------------------

Esta é uma implementação de referência, não um porte 1:1 do sistema que a
inspirou. Duas partes foram deixadas de fora, de propósito, por não fazerem
sentido fora de um ambiente com várias perguntas automáticas rodando ao
mesmo tempo e acesso a mais de um provedor de LLM:

- **Promoção automática de pergunta nova (ainda não ativa) para ativa por
  precisão.** O sistema original também decide sozinho quando uma pergunta
  candidata (ainda em teste, nunca perguntada em produção) deve estrear como
  pergunta ativa, com base na precisão acumulada. Isso só faz sentido
  demonstrar com várias perguntas concorrentes; `calibrar_limiar.py` cobre
  só a parte de recalibrar o limiar de uma pergunta que já está ativa.
- **Segunda opinião de outro provedor de LLM antes de promover uma reescrita
  de skill/instrução.** O sistema original roda um "juiz" de um provedor
  diferente como checagem extra antes de aplicar uma reescrita gerada por
  IA. Depende de assinatura/CLI específicos de quem está rodando; fica a
  cargo de quem adaptar este kit decidir se quer (e com qual provedor)
  replicar essa segunda checagem.
