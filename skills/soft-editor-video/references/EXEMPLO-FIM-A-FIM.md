# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: este exemplo é ILUSTRATIVO (nicho fictício).** O dono, o vídeo, os tempos, os custos e
> os resultados foram inventados só pra mostrar a FORMA de cada saída. É PROIBIDO parafrasear ou
> reusar as frases, os números, o nicho ou a cena dele na peça real. A peça real nasce 100% do
> insumo e do config do dono; se você se pegar copiando uma frase ou uma cena deste exemplo, pare
> e volte ao insumo.

**O caso fictício:** um adestrador de cães que grava vídeos no celular, sozinho, no quintal de casa.
Ele vende um curso online de conduta de filhote. Pedido: "gravei esse vídeo agora, deixa pronto pra
postar".

Este arquivo mostra a saída resumida do fluxo inteiro, na ordem: matéria-prima, primeiro uso,
decisão de forma, pipeline, auditoria e o relatório final.

---

## A matéria-prima que chegou

| Item | O que veio |
|---|---|
| arquivo de vídeo | `cru-filhote-coleira.mov`, 2 min 47 s, 1080x1920 vertical, celular na mão |
| destino | não declarado |
| identidade | nada configurado, primeiro uso |
| material de apoio | uma gravação de tela de 12 s do aplicativo dele, e 3 fotos de filhote |
| card de encerramento | não existe |

As 2 perguntas que a skill fez, uma por vez:

1. "Isso vai como reel de atração ou como anúncio?"
   > "Reel mesmo, quero atrair gente nova."
2. "Você tem alguma tela, print ou gravação que MOSTRE o que você fala?"
   > "Tenho a gravação do app e umas fotos do Thor filhote."

---

## Passo 0 · Primeiro uso

### 0.1 · A ordem de grandeza do custo, mostrada ANTES de qualquer aprovação

A skill mostrou a tabela das 3 faixas e disse em 2 linhas:

> "Corte, legenda, gancho e música rodam de graça na máquina. Imagem gerada custa centavos por
> imagem e esse vídeo pediria umas 5. Animar imagem é a faixa cara, é preço por clipe de poucos
> segundos e esse vídeo pediria uns 6 clipes. Como você já tem a gravação do app e as fotos do Thor,
> dá pra fazer esse inteiro sem gastar nada. Quer assim?"

> Resposta do dono: "sem gastar."

Registrado: o vídeo roda com movimento local, prova real e cartela. Nenhum crédito consumido.

### 0.2 · O elenco, por entrevista

As 6 perguntas, uma por vez. Respostas resumidas: apresentador é ele mesmo, homem branco, barba
cheia, boné, camiseta preta; sem mascote humano, mas o cão dele (um pastor) aparece sempre; sem
sócio; ambiente é o quintal com muro de tijolo; paleta laranja e preto; logo é um osso estilizado.

`config/personagens.json` montado, com `trio_sempre` = apresentador e o pastor.

**STOP.** Uma imagem de teste de cada personagem foi gerada e mostrada.

> "É essa a sua cara nas cenas? Aprova, ou ajusto alguma coisa?"
> Dono: "o boné tá errado, o meu é de aba reta." Ajustado na descrição e regerado. Aprovado.

### 0.3 · Card de encerramento

> "Não tenho, deixa sem por enquanto."
Registrado. Entrega sai sem card, e a skill avisou em 1 linha que ele pode ser somado depois sem
refazer o vídeo.

---

## Passo 1 · A forma escolhida, e o porquê

A matéria-prima tem talking-head com apoio que ilustra, mais uma prova real curta (a gravação do
app) que não é o centro do vídeo, e é citada de passagem.

**Forma escolhida: B, composição adaptativa.** O motivo, gravado no relatório: o vídeo é fala
explicando, o apoio ilustra, e a prova real cabe num trecho só, sem precisar de tela cheia o tempo
inteiro. A Forma A foi descartada porque a gravação do app não é o argumento central. A Forma C foi
descartada porque a fala cita duas telas, não muitas. A Forma D foi descartada porque existe apoio
disponível.

Como o dono recusou gasto, os apoios da Forma B saem de prova real, foto dele e cartela, sem imagem
gerada. A forma não mudou por causa disso, só o material que preenche ela.

---

## Passos 2 ao 15 · O pipeline, resumido

| Passo | O que aconteceu |
|---|---|
| 2, ingestão | 2:47, sem legenda embutida, áudio limpo |
| 3, transcrição | 412 palavras com tempo. A fala tem 1 lista de 3 itens e 2 nomes próprios |
| 4, corte | começou na primeira fala completa aos 0:06, saíram 31 s de pausa e respiração, ficou em 2:09, sem 1,2x porque essa família ainda não foi aprovada nessa velocidade |
| 5, apoios | 34 trechos planejados, cada um com intenção, frase de apoio ou o motivo de não ter, frames e transição |
| 6, imagens | pulado, o dono recusou gasto |
| 7, animação | movimento local sobre as 3 fotos, zoom lento |
| 8, montagem | virada de layout por flash aos 0:38, apresentador grande passa a close embaixo |
| 9, gancho | a frase mais forte copiada pro começo com efeito preto e branco |
| 10, legenda | palavra por palavra, na altura do peito, palavra-chave destacada |
| 11, card | pulado, não existe |
| 12, música | leve, com fade, nunca por cima da fala |
| 13, inspeção de cortes | 9 emendas, 27 quadros gravados |
| 14, gate | exit 0 |
| 15, export | `final-filhote-coleira-1080x1920.mp4` |

### O trecho de manifesto de um apoio, pra ver o formato

```json
{
  "trecho": "00:00:41.200 - 00:00:43.600",
  "fala": "ele não puxa porque é teimoso, ele puxa porque a coleira está no lugar errado",
  "intencao": "renomear a causa",
  "estrategia_visual": "foto do pastor filhote em close no pescoço, zoom lento",
  "frase_apoio": "A coleira está no lugar errado.",
  "frame_inicial": "close no peitoral",
  "frame_final": "close no pescoço",
  "movimento": "zoom lento 1.0 para 1.12",
  "transicao_entrada": "corte seco na virada de argumento",
  "transicao_saida": "fusão de 0.3s"
}
```

### O gancho escolhido, e o crivo anti-IA

Frase escolhida: **"Seu filhote não puxa porque é teimoso."**

Passou pelo crivo curto (a skill de crítica de copy não estava instalada nesse caso fictício): sem
travessão, sem palavra de folheto, sem abertura de manual, sem três adjetivos, sem promessa vazia. A
frase é do próprio dono, saiu da transcrição.

Reprovada na primeira tentativa: "Neste vídeo você vai entender o real motivo." Abertura de manual.
Trocada pela fala real dele.

---

## A auditoria visual

```
python3 scripts/06_audit.py final-filhote-coleira-1080x1920.mp4 saida/audit 12 "0:00,0:06,0:38,1:12,2:05"
```

Primeira rodada: **REPROVA (exit 1)**. O `veredito.json` apontou o frame do marco 0:38 com dupla
exposição. Causa: o marco caiu no meio do flash da virada. Correção aplicada: o marco foi movido
0,8 segundo depois da transição, como manda a régua.

Segunda rodada: **PASSA (exit 0), 12 frames.**

Selo emitido, exato:

> Auditoria visual: PASSA (12 frames). Prova: `saida/audit/mosaico.jpg`

---

## A entrega, as duas peças

```
saida/final-filhote-coleira-1080x1920.mp4
saida/relatorio-edicao-filhote-coleira.md
```

### `relatorio-edicao-filhote-coleira.md`, resumido

```
vídeo: final-filhote-coleira-1080x1920.mp4  ·  2:09  ·  1080x1920

forma: B, composição adaptativa
motivo: fala que explica com apoio que ilustra; a prova real cabe num trecho só.
formas descartadas: A (a prova não é o centro), C (só 2 telas citadas), D (existe apoio).

custo: zero. O dono recusou gasto no primeiro uso; apoios saíram de prova real, foto e cartela.

corte: 2:47 para 2:09. 31s de pausa e respiração fora. Sem corte semântico. Sem 1,2x.
mapa de cortes: 9 emendas, todas com fade de 30 ms na entrada e na saída.

apoios: 34 trechos, todos com direção completa no manifesto.
gancho: "Seu filhote não puxa porque é teimoso." Efeito preto e branco, faixa de 1 linha.
        Primeira versão reprovada no crivo anti-IA (abertura de manual), trocada pela fala real.
legenda: palavra por palavra, altura do peito, aplicada por último.
card de encerramento: não existe. Pode ser somado depois sem refazer o vídeo.

inspeção de cortes: 9 emendas, 27 quadros gravados em saida/cortes/
gate da edição: exit 0
auditoria visual: PASSA (12 frames) na segunda rodada.
                  Primeira reprovou por marco dentro do flash; marco movido 0,8s depois.
prova: saida/audit/mosaico.jpg

pendências marcadas: nenhuma.
```

---

## O que teria mudado com outra matéria-prima

- **Se a gravação do app fosse o argumento central** (o dono mostrando o app resolver o problema na
  tela): Forma A, tela cheia de prova, e a fala dele viraria narração por cima.
- **Se ele citasse 6 telas diferentes ao longo da fala:** Forma C, topo-fixo, com o rosto fixo em
  cima e as telas embaixo, e o primeiro vídeo aprovado virando o molde da família.
- **Se ele não tivesse nem foto nem gravação:** Forma D, conteúdo puro, com uma headline curta nos 3
  primeiros segundos e nenhuma arte somada.
- **Se ele tivesse aprovado o gasto:** os 34 apoios ganhariam 5 imagens geradas e 6 clipes animados,
  com o saldo e o preço real do provedor mostrados antes, e o número consumido gravado no manifesto.
