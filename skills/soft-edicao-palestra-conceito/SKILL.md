---
name: soft-edicao-palestra-conceito
description: Transforma um corte de palestra gravada em 16:9 num reel vertical 9:16 de no mínimo 1:30, no formato tarja preta com headline e sub em cima, palestrante no meio, legenda de uma palavra por vez e line drawing do conceito embaixo. Use quando pedirem reel, corte ou vídeo vertical de palestra, aula ou talk com desenho de conceito. Roda em 9 etapas com script, critério de pronto e gates que comparam a fala do bruto com a fala do final.
---

# Edição de palestra com conceito desenhado

Um trecho de palestra 16:9 vira um reel 1080x1920 assim:

```
+------------------------------+  y 0
| tarja preta                  |
| HEADLINE (2 linhas, 1 acento)|
| sub                          |
+------------------------------+  y 656
| palestrante 1080x608         |
|        legenda (1 palavra)   |  y 1172, fixa
+------------------------------+  y 1264
| tarja preta                  |
| line drawing do conceito     |
| que a fala diz agora         |
+------------------------------+  y 1920
```

Tudo que é da cliente (cores, fontes, CTA, velocidade, nomes próprios) fica no `marca.json`. Tudo que é do vídeo (fonte, cortes, headline, conceitos) fica no `ajustes.json` da pasta de trabalho. Os scripts não têm caminho fixo, token nem ID de nuvem.

## Processo obrigatório antes dos comandos

Leia `references/PROCESSO.md` e use os quatro modelos em `modelos/`. Identifique `palestra_conceito`, confira código/brutos/03/04 e feche decupagem antes de montar. Não usar este reframe em captura de monitor. Registre fala por palavra e todas as emendas ouvidas; preservar repetição proposital. Promessas/demonstrações fecham no corte, inclusive as feitas no cold open.

Depois da headline e antes de gerar conceitos, preencher `STORYBOARD.md` e `storyboard.json` com tempos da fonte e saída, fala literal, IDs de palavras, conceito que explica, desenho/material, composição, legenda, transição, CTA/loop e critério por cena. Validar: `python3 scripts/validar_storyboard.py TRAB/storyboard.json`. Produzir desenhos apenas depois de fechar essa tabela. Exemplo real em `exemplos/palestra/`, com reprovação histórica explícita.

Um vídeo por vez. Envolver cada etapa pesada no `scripts/executar_etapa.py` com todas as entradas/saídas declaradas e prazo máximo3600s, conforme `references/PROCESSO.md`. `rodar.sh` é sequência técnica e não implementa sozinho o limite por etapa: produção deve usar o wrapper por comando. `--de N` retoma etapa, mas não é prova automática de cache de todas as peças. Etapa02 usa hash do áudio/configuração/offset/versão do motor e hash da saída; gate de saída tem cache distinto. Arquivos antigos sem metadado coerente exigem nova transcrição uma vez, nunca adotar como cache validado só pelo nome.

Área segura por formato em `marca.json`: headline e desenho respeitam `area_segura`, legenda fixa y1172 e fora do rosto. Tarjas0..656/1264..1920, vídeo656..1264. Não confundir zona interna de desenho com UI de plataforma: adicionar perfil de destino na prévia e garantir que prova/texto não caia sob UI. A tarja inferior usa coordenadas locais y12..505, equivalentes a y1276..1769 do quadro. Esse é o contrato do montador de referência; y1400 pertence ao perfil YAP4 e não limita o desenho deste formato. Conferir separadamente a UI do destino na prévia. O gate visual mede geometria do formato, sem certificar a interface da plataforma.

Estado e limites em `VALIDACAO.md`. A prova revisada tem montagem integral e revisão semântica registradas; a autorização do dono para publicar as skills revisadas está vigente. A grafia pontual de nomes na legenda permanece uma conferência própria e não equivale a perda de áudio. Não resolver reprovação de fala com limiar menor. Se o gate reprovar palavra comum na emenda, voltar à decupagem e comprovar fala inteira antes de render.

## Ambiente preparado antes da fila

```
bash instalar.sh
```

O instalador opcional, executado somente pelo responsável pelo ambiente, instala ffmpeg (apt) e `requirements.txt` (faster-whisper, opencv-python, numpy, scipy, pillow). O modelo do whisper (large-v3, cerca de 3 GB) baixa sozinho na primeira transcrição. Fontes Inter (licença OFL) e o detector de rosto YuNet (MIT; leia assets/modelos/LICENCA.txt) já vêm em `assets/`.

## Regras fixas

1. Corte final longo de90 a300s. O gate atual aplica mínimo90; conferir máximo300 no storyboard e arquivo. Teste curto é prova de componentes.
2. Fala inteira: nenhuma palavra pode sumir, ser cortada no meio ou ficar na emenda. O gate 7a re-transcreve o final e compara com a transcrição do bruto.
3. Loop aberto fecha dentro do corte. Se o palestrante diz "vou te mostrar", o trecho que mostra entra no corte e fica registrado em `loops`.
4. Velocidade 1,15x no vídeo inteiro (atempo, sem mudar o tom da voz).
5. Sem música.
6. Legenda de uma palavra por vez, sempre no mesmo lugar (y 1172), em cima do vídeo, nunca nas tarjas.
7. Paleta fechada: marfim #faf9f5, tinta #141413, laranja #D4541C, linha #e6e3da. O verde #4ade80 é proibido em qualquer pixel das tarjas.
8. Headline e sub ficam do primeiro ao último quadro. Uma palavra em acento laranja, no máximo.
9. Um desenho por ideia, entrando no momento em que a fala diz a ideia. Desenho é traço fino, sem preenchimento chapado.
10. O vídeo não leva CTA queimado. O CTA vai no `legenda-post.txt`.
11. Nada é enviado, publicado ou subido. A entrega fica em `TRAB/entrega/`.

## Pasta de trabalho

Crie uma pasta por vídeo (chamada TRAB abaixo) e copie `exemplo/ajustes.json` para dentro. Todos os comandos rodam de dentro de `scripts/`:

```
cd scripts
python3 01_entrada.py /caminho/TRAB
```

Para rodar tudo de uma vez depois de preencher o `ajustes.json`: `bash scripts/rodar.sh TRAB` (para na primeira etapa que não der PRONTO; `--de N` recomeça da etapa N).

Todo tempo no `ajustes.json` é em segundos absolutos da fonte, os mesmos que aparecem no `trechos.txt`.

## As 9 etapas técnicas

Entre cortes e produção de conceitos, fechar o storyboard do processo. Os comandos abaixo não substituem a conferência pré-montagem nem a revisão independente.

### 1. Entrada

Preencha no `ajustes.json` o `fonte` (caminho do bruto), a `janela` [ini, fim] em que vai procurar o corte (deixe uns 5 min de folga) e o `slug`.

```
python3 01_entrada.py TRAB
```

Pronto quando: imprime PRONTO com resolução, fps e segundos de áudio extraídos (`entrada.json`, `fonte16.wav`).

### 2. Transcrição

```
python3 02_transcrever.py TRAB
```

Gera `transcricao.json` (tempo por palavra) e `trechos.txt` (frases com tempo, para ler e escolher). Os nomes próprios da cliente entram em `marca.json > whisper.prompt`. Em CPU leva de 1 a 3 vezes a duração do áudio.

Com a máquina carregada (load acima do número de núcleos) o script usa 1 thread sozinho, porque com 4 o whisper fica parado esperando CPU. Para forçar, use `THREADS=4`. Para um teste rápido, um `marca.json` na pasta de trabalho pode trocar `whisper.modelo` (por exemplo `tiny`) e `whisper.beam` (por exemplo 1); o gate de fala usa o mesmo modelo.

Pronto quando: imprime PRONTO e o `trechos.txt` lê como a fala real. Nome próprio errado se corrige depois em `substituir`.

### 3. Cortes

Leia o `trechos.txt` e escolha uma ideia completa: começa numa frase que se entende sem contexto, termina quando a ideia fecha. Preencha:

- `blocos`: [[ini, fim], ...] em ordem; pode pular trechos (exemplo repetido, digressão);
- `cold_open` [ini, fim]: 2 a 4 s da frase mais forte, que abre o vídeo antes do início;
- `cortar`: gaguejo ou recomeço a tirar de propósito;
- `substituir`: palavra que o whisper errou, [de, até, [[palavra, t0, t1]]];
- `loops`: cada promessa ("vou mostrar") com o tempo em que abre e em que fecha.

```
python3 03_cortes.py TRAB
```

O script só tira pausa que o silencedetect confirma no áudio (0,35 s ou mais abaixo de -35 dB), com folga de 0,15 s de cada palavra com timestamp. O vão entre timestamps do whisper não conta como pausa, porque pode ter fala. Depois ajusta cada bloco a um número inteiro de quadros.

Pronto quando: PRONTO, ou seja, duração final de no mínimo 90 s, nenhuma borda de bloco no meio de uma palavra, nenhum corte fora de silêncio comprovado ou perto de palavra e nenhum loop aberto sem fechamento dentro do corte. Leia os avisos de ATENCAO (bloco que termina sem ponto final, bloco que começa no meio de frase) e resolva cada um.

### 4. Headline e sub

Escreva `TRAB/headlines.md` com 3 candidatas (Headline: e Sub:), marque uma como ESCOLHIDA e diga o porquê (modelo em `exemplo/headlines.md`). Coloque a escolhida em `ajustes.json > headline` {headline, sub, destaque}.

Critério de qualidade da headline:

- diz o assunto do trecho inteiro, não só da primeira frase;
- promete só o que o corte entrega (nada de "o segredo" se o segredo não aparece);
- fala com quem assiste (você, seu), em português falado, de 4 a 9 palavras;
- o destaque é a palavra que o desenho também mostra;
- a sub completa a headline, não repete: dá o porquê, o como ou o para quem.

```
python3 04_headline.py TRAB
```

Pronto quando: PRONTO e o `topo-previa.png` lê bem em tamanho de celular. O script reprova headline com mais de 2 linhas, palavra sozinha na 2a linha, linha acima de 990 px, destaque que não está no texto, travessão e `headlines.md` sem 3 candidatas ou sem ESCOLHIDA. Se `marca.json > lint_copy` apontar um linter de texto, ele também precisa sair com 0.

### 5. Conceitos

Liste em `ajustes.json > conceitos` uma ideia por momento da fala: `id` (desenho do módulo), `grupo` (desenhos do mesmo grupo acumulam, como degraus de uma escada), `ts` (segundo da fonte em que a fala diz a ideia), `prova` (palavra dita perto de ts), `fala` e `mostra`. `cold_conceito` é o desenho do cold open. `desenhos` é o módulo de desenhos (padrão `desenhos_exemplo`).

```
python3 05_conceitos.py TRAB
```

Pronto quando: PRONTO (todo id existe, todo ts cai dentro de um bloco, a palavra de prova está a até 3 s de ts, todo desenho cabe na zona útil) e o `conceitos-previa.jpg` mostra cada desenho legível. Conceito parado mais de 20 s gera ATENCAO: divida a ideia ou acrescente um desenho.

### 6. Render

```
python3 06_base.py TRAB      # corta as peças da fonte, acelera 1,15x, áudio em -14 LUFS
python3 06_rosto.py TRAB     # acha o rosto a cada 0,1 s
python3 06_reframe.py TRAB   # caixa 16:9 que segue o rosto, punch-in alternado nas emendas
python3 06_compor.py TRAB    # monta o 1080x1920 final
```

Quando a fonte tem slide e câmera lado a lado, defina `painel` [x0, y0, x1, y1] com a região da câmera. Se o corte cai num plano anterior, use `hold_ini` (quadros). Para testar só o começo: `06_compor.py TRAB --ate 15`.

Pronto quando: os quatro imprimem PRONTO (duração da base igual ao plano, rosto em pelo menos 70% das peças, toda caixa dentro do painel, `final.mp4` com 1 trilha de vídeo e 1 de áudio).

### 7. Gates

```
python3 07_gate_fala.py TRAB
python3 07_gate_visual.py TRAB
```

O gate de fala transcreve o `final.mp4` de novo e compara palavra por palavra com a transcrição do bruto, descontando o que está em `cortar`. Reprova palavra de 3 letras ou mais ausente, cobertura abaixo de 97%, fala engolida entre duas peças e palavra atravessando uma emenda.

O gate visual reprova: formato diferente de 1080x1920 a 30 fps; duração abaixo de 90 s ou diferente do plano; velocidade diferente de 1,15x; cor proibida ou fora da paleta nas tarjas; headline, desenho ou legenda fora da área segura; vídeo congelado; áudio mudo.

Pronto quando: os dois saem com PRONTO (`gate-fala.json` e `gate-visual.json` sem falha). Falha de fala se resolve na etapa 3 (borda, `cortar`, `substituir`) e depois roda de novo a partir da 6.

### 8. Mosaico

```
python3 08_mosaico.py TRAB
```

Abra o `mosaico.jpg` (24 quadros do vídeo inteiro) e os `quadro-0s/1s/3s/5s.jpg`.

Pronto quando: você olhou e confirmou, quadro a quadro, que a headline está inteira e legível, o rosto está inteiro na faixa (testa e queixo), a legenda não cobre a boca, o desenho bate com a fala do momento e não há quadro preto, verde ou com slide errado. O quadro 0 é a capa: ele tem que funcionar sozinho.

### 9. Entrega

```
python3 09_entrega.py TRAB
```

Monta `TRAB/entrega/` com `SLUG-master.mp4`, `SLUG-leve.mp4` (cerca de 1 MB/min, para WhatsApp e revisão), `edit-manifest.json`, `verbos-pedido.json` (cada verbo do pedido com o número medido na fonte e no final) e `legenda-post.txt` (com o CTA da marca).

Pronto quando: PRONTO e os 5 arquivos existem. Só roda com os dois gates sem falha. Envio e publicação ficam com quem pediu.

## Teste rápido

Para provar a instalação num trecho curto (10 a 20 s), use `--prova` nas etapas 3, 7b e 9: a duração mínima vira aviso e a entrega sai como `SLUG-prova-master.mp4`.

```
bash scripts/rodar.sh TRAB --prova
```

## Para outra cliente

Troque só isto:

1. `marca.json`: cores, paleta, cores proibidas, fontes, tamanhos, CTA, velocidade, duração mínima e `whisper.prompt` com os nomes próprios da cliente. Pode ficar dentro da pasta de trabalho (tem prioridade sobre o da skill).
2. Fontes: coloque os arquivos em `assets/fontes/` e aponte em `marca.json > fontes`.
3. Desenhos: copie `scripts/desenhos_exemplo.py` para a pasta de trabalho com outro nome (por exemplo `desenhos_cliente.py`), troque os desenhos e aponte `ajustes.json > desenhos` para `desenhos_cliente`.
4. `loops_abertos`: as expressões que a palestrante usa para prometer algo para depois.

Os scripts não mudam.

## Arquivos

- `scripts/`: uma etapa por arquivo, mais `comum.py` (layout e leitura de config), `tarjas.py` (headline e legenda), `linhas.py` e `escala.py` (motor dos desenhos), `desenhos_exemplo.py` (biblioteca de exemplo) e `rodar.sh`.
- `assets/fontes/`: Inter (OFL). `assets/modelos/`: YuNet para rosto.
- `exemplo/`: `ajustes.json`, `headlines.md` e `verbos-pedido.json` preenchidos como modelo.
- `marca.json`: padrão do MARCA, como exemplo.
