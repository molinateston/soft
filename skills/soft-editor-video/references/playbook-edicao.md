# Playbook de edição por agente (destilado de uma live)

Este arquivo guarda o que uma sessão de edição de vídeo por agente demonstrou ao vivo e que soma ao que esta skill já faz. A skill já corta silêncio por script, monta gancho, planeja apoios de 2 a 3 segundos, legenda palavra por palavra com transcrição local, roda gate bloqueante e auditoria visual em mosaico. O playbook só vale pelo que acrescenta.

Cinco costuras entram como regra ativa (seções 1 a 5). O resto fica anotado como escopo futuro (seção 6), sem virar método, porque ainda não foi provado nesta máquina.

---

## 1. Tabela de cortes com minutagem ANTES de cortar

Todo corte que remove FALA (não só silêncio ou respiração) nasce de uma tabela em disco, nunca de uma decisão no olho durante o corte. O agente propõe, o dono aprova ou ajusta linha a linha, e só então o script aplica.

O artefato é `cortes-propostos.md` na pasta de trabalho do dono, uma linha por trecho:

```
início · fim · o que sai · por quê
00:00,0 · 00:03,2 · claquete de gravação ("take 5") · não é conteúdo
00:41,8 · 00:44,1 · gancho gravado em duplicata · fica a versão de 00:12
01:58,0 · 02:06,4 · CTA falado errado · o card do fim já cobre
```

O que costuma cair: claquete inicial, silêncio longo, gancho gravado duas vezes (fica uma), CTA falado que sai errado. Quando há duas gravações da mesma frase (gancho, abertura), o agente escolhe qual fica e registra o porquê na coluna.

O dono aprova a tabela inteira ou ajusta trecho por trecho. Corte que remove fala sem a tabela aprovada reprova. No relatório cola a conta: `trechos propostos: N · aprovados: N · ajustados: N`.

Isso torna a aprovação um artefato conferível em disco, no lugar de uma frase de chat que ninguém encontra depois.

---

## 2. Critérios ESCRITOS de auto-aprovação, e o teto de 3 tentativas

O agente aprova sozinho o que é MEDÍVEL e escala pro dono o que é JUÍZO ESTÉTICO. A régua fica escrita, e não vira sensação do turno.

**Auto-aprova SEM chamar o dono quando as QUATRO batem:**
- (a) nenhum elemento de tela (faixa, overlay, apoio, legenda) cobre o rosto ou o corpo do apresentador;
- (b) o tempo de entrada e de saída de cada elemento bate com o que o manifesto declarou;
- (c) quando há PIP ou bolha na tela, nenhum elemento de design fica por cima dela;
- (d) o áudio está sincronizado com a legenda karaokê, sem atraso perceptível.

**SEMPRE escala pro dono, o agente nunca decide sozinho:**
- se o RITMO funciona ou arrasta;
- se a composição tem a CARA da marca do dono.

**Teto de 3 correções automáticas.** Quando um critério medível falha, o agente corrige e refaz, até três vezes. Na quarta falha, para e chama o dono com o que emperrou. O teto vive no manifesto no campo `tentativas_auto` (ver seção 2.1) e o gate confere que não passou de 3.

Regra-mãe: o que a máquina mede, a máquina aprova; o que é gosto, vai pro humano. Isso não substitui o gate bloqueante nem a auditoria visual, formaliza o loop de correção que roda dentro deles.

### 2.1 O campo no manifesto

O `edit-manifest.json` ganha um bloco `tentativas_auto` com teto 3:

```json
"tentativas_auto": {
  "teto": 3,
  "usadas": 1,
  "criterios_medidos": ["nada_cobre_rosto", "tempos_batem", "nada_sobre_pip", "audio_sincronizado"],
  "escalou_ao_dono": false,
  "motivo_escala": null
}
```

`usadas` maior que `teto` reprova no gate. `escalou_ao_dono: true` exige `motivo_escala` preenchido (ritmo, cara da marca, ou o critério medível que não fechou em 3 tentativas).

---

## 3. Instruir por TEMPO, não por sensação

O agente NÃO assiste ao vídeo. Ele lê a transcrição temporizada e extrai quadros da timeline pra localizar onde inserir. Por isso toda direção de inserção aponta PALAVRA e TEMPO, nunca um estado emocional que só quem assiste enxerga.

Aprova: `apoio entra na palavra "resultado" em 00:12,4`; `marca-texto entre 00:12,4 e 00:15,0`; `lower-third na frase que começa em 00:31,0`.

Reprova, e volta pro dono reescrever: "quando ele fica sério", "no momento mais emocionante", "quando pega pesado". A skill não tem como localizar isso, e chutar vira apoio no lugar errado.

Vale pra toda instrução de inserção: apoio, marca-texto, frase palavra a palavra, lower-third, PIP, transição. Se a instrução do dono vier por sensação, o agente devolve o mapa de tempos que enxerga e pede pra ele apontar o segundo.

---

## 4. Memória de estilo em config/estilos.md

O primeiro tratamento aprovado de uma forma ou personagem vira molde declarado, pra a próxima edição pular a exploração inteira. Hoje só a Forma C tem esse molde cravado; a memória estende o hábito pras Formas A, B e D e pra cada personagem.

O arquivo é `config/estilos.md` dentro da pasta da skill, com um bloco por estilo nomeado:

```
## estilo "reels-padrao" (Forma B)
- legenda: karaokê palavra a palavra, palavra-chave destacada
- cor: #<hex da paleta do dono>
- posição da legenda: altura do peito
- transições: flash no terço inicial, corte na virada narrativa
- música: discreta, fade de entrada e saída
- CTA: card fixo do fim (config/cta_take.mp4)
```

Fluxo: na primeira vez que um estilo agrada, "salva esse estilo como <nome> em config/estilos.md". Nas seguintes, "edita no estilo <nome>", e o agente carrega o bloco em vez de redecidir cor, legenda, transição e música. É mecanismo declarado de economia: repetir a exploração de estilo a cada vídeo torra token à toa.

O `config/estilos.md` é configuração do dono; segue a regra da skill de não versionar dado do dono junto do código quando o deploy for compartilhado.

---

## 5. Régua de comparação entre motores (Claude e Codex)

Quando o mesmo ativo roda em dois motores, seja em paralelo (mesmo prompt, compara os dois) ou dividido (um corta, outro anima), o vencedor é o que passa a TABELA DE VERBOS DO PEDIDO inteira. Essa é a mesma régua do gate, aplicada agora à escolha entre dois outputs.

**"Motor X é mais rápido" NÃO é regra.** Num teste demonstrado ao vivo, um motor exportou antes de o outro terminar de ler a transcrição, MAS o output rápido saiu SEM LEGENDA, um verbo do pedido em `não feito`, então reprovou. Velocidade não é qualidade.

A régua, em ordem:
1. Cada output passa pela tabela de verbos do gate (cortar, legendar, verticalizar, musicar, ganchar). Output com qualquer verbo em `não feito` está fora, por mais rápido que tenha sido.
2. Entre os que passam a tabela INTEIRA, o cronômetro só desempata.
3. Nunca se escreve uma preferência fixa por motor. A escolha é por resultado medido, ativo a ativo.

Sobre a hierarquia de modelos, vale a doutrina da casa: o avaliador fica acima do executor. O caro planeja e revisa, o barato executa o mecânico. Divisão de trabalho entre motores (um corta, outro anima) é válida; corrida de velocidade sem passar pelo gate, não.

---

## 6. Correção técnica: granularidade da transcrição

A tese "Whisper é por frase, precisa pagar pra ter por palavra" está imprecisa. O Whisper cru devolve por segmento, mas `faster-whisper` e `whisper-timestamped` devolvem timestamp POR PALAVRA de graça, e com boa precisão. Esta skill já legenda palavra a palavra com transcrição local, então o dado por palavra já existe na máquina, sem custo.

A vantagem de uma transcrição paga (por exemplo ElevenLabs) fica restrita à precisão do ALINHAMENTO, não à existência do timestamp por palavra.

Regra: antes de pagar transcrição, MEDIR o desvio do alinhamento local numa amostra. Só troca pra a paga se a legenda atrasar de forma visível. Pagar sem medir o desvio primeiro reprova a decisão.

---

## 7. Escopo futuro (anotado, NÃO é método ativo)

Estes pontos apareceram na live mas NÃO entram como método porque ainda não foram provados nesta máquina. Entram só depois de rodar num vídeo real com o gate da casa em cima, pela lei de provar em casa real antes de servir.

- **Export do mesmo corte em 1:1, 9:16 e 16:9 com reenquadramento por rosto.** Esta skill é 9:16 por definição; três formatos mudariam a promessa.
- **Corte de longa duração (webinar de mais de uma hora pra versão curta).** É outra natureza de trabalho, corte semântico de blocos de fala inteiros; os gates de reels curto não se aplicam. Se virar demanda recorrente, nasce uma skill irmã de corte longo.
- **Skills externas de terceiros pra corte e para animação em HTML.** Não foram instaladas nem provadas aqui. Só entram após prova em casa real, com o gate da casa por cima.

Nada nesta seção deve ser tratado como passo do pipeline enquanto não houver prova.
