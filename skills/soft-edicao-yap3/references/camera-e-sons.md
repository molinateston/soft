# Câmera e sons do YAP

Lido nos passos 6 e 8 da ordem de edição do `SKILL.md`. "Medido" descreve uma amostra de 19 reels de um perfil de nicho (uma conta): é referência descritiva, não escala obrigatória nem cota.

## Câmera: a regra é permanecer, e mexer com motivo

- **Permanência como ponto de partida.** Mantenha escala e posição enquanto a ideia se desenvolve. Cortar uma pausa, trocar a legenda ou inserir um elemento não exige mover a câmera. Planeje os trechos de câmera parada antes dos movimentos.
- **Primeiro plano estático.** Do segundo plano em diante o movimento é opcional: não comece a mexer só porque o gancho terminou.
- **Aproximação motivada pela fala.** O punch-in no corte pode destacar uma informação importante. A mediana medida é 1,16 de escala (p25 1,07, p75 1,18): referência descritiva. Permaneça no enquadramento escolhido enquanto a mesma ideia continua.
- **Push-in seletivo em trecho longo.** Quando a fala justificar progressão ou ênfase, aproxime com sutileza e termine antes do último quadro, deixando a imagem permanecer no enquadramento final. Na amostra, apareceu em 41 de 235 planos de pelo menos 1,5 s (17%), cobrindo 26% do tempo: não é cota, duração mínima nem meta. Trecho longo também pode ficar estático.
- **Continuidade de escala e posição.** Nos cortes de continuidade da mesma ideia, o próximo plano herda a escala e a posição finais do anterior. Mudança intencional no corte leva o motivo registrado e a emenda conferida. Continuidade numérica sozinha não basta: inverter a direção em todo corte também produz oscilação.
- **Recuo com motivo próprio.** Abra o quadro por mudança de bloco ou por necessidade visual do briefing. Não volte ao aberto automaticamente depois de uma aproximação: o fim da frase não é motivo. Não alterne aproximação e recuo por índice, por tempo fixo nem a cada troca de plano.
- **Dosagem.** Deixe tempo na mesma cena. Não existe número ideal de movimentos; observar esses recursos numa amostra não obriga a combiná-los em ciclo.
- **Limite:** não corte orelha nem cabeça. Reposicione para caber o texto.
- **Erro que já aconteceu:** um mapa de câmera gerado por paridade do índice alternou 1,00 → 1,10 e 1,10 → 1,00 em todos os blocos do corpo. Mesmo com continuidade nos limites, isso virou movimento recorrente sem escolha pela fala, e a revisão reprovou. A conferência de câmera existe para pegar exatamente isso.
- **Cada bloco de câmera registra no briefing:** início e fim, escala e posição iniciais e finais, a fala que o motiva e o trecho de permanência. Por padrão `z1 = z`; só preencha valores diferentes com motivo descrito.

## Receitas de ffmpeg (1080x1920, 30 fps)

**Punch-in estático** (z escolhido no briefing; 1,16 é exemplo; cx 0,5; cy perto de 0,36 para o rosto):

```
crop=1080/z:1920/z:cx*1080*(1-1/z):cy*1920*(1-1/z),scale=1080:1920:flags=lanczos
```

**Push-in suave, sem tremor** (filtro `perspective`; z vai de 1,00 a 1,20 em 2,6 s, centro cx 0,5 e cy 0,36; troque `1`, `0.2`, `2.6`, `0.5` e `0.36` por z0, z1-z0, T, cx e cy):

```
ffmpeg -v error -y -ss 20 -t 3 -i bruto.mp4 -vf "perspective=x0='0.5*W*(1-1/(1+0.2*min(in/30/2.6,1)))':y0='0.36*H*(1-1/(1+0.2*min(in/30/2.6,1)))':x1='0.5*W*(1-1/(1+0.2*min(in/30/2.6,1)))+W/(1+0.2*min(in/30/2.6,1))':y1='0.36*H*(1-1/(1+0.2*min(in/30/2.6,1)))':x2='0.5*W*(1-1/(1+0.2*min(in/30/2.6,1)))':y2='0.36*H*(1-1/(1+0.2*min(in/30/2.6,1)))+H/(1+0.2*min(in/30/2.6,1))':x3='0.5*W*(1-1/(1+0.2*min(in/30/2.6,1)))+W/(1+0.2*min(in/30/2.6,1))':y3='0.36*H*(1-1/(1+0.2*min(in/30/2.6,1)))+H/(1+0.2*min(in/30/2.6,1))':interpolation=cubic:eval=frame" -c:v libx264 -crf 16 -preset veryfast -an push.mp4
```

Regras de uso:

- **Não use `zoompan`:** treme por arredondamento. Não use `split` mais `concat` por plano: é lento.
- **Num corpo com cortes**, aplique o `perspective` uma vez só, com z por partes: `z = Σ between(in-1,s,e-1)*(z0+dz*min((in-1-s)/F,1))`.
- **No `perspective`, `in` começa em 1** (testado). Com `in` puro o zoom muda um quadro depois do corte, o último quadro fica com z = 0 e o ffmpeg para com "Invalid argument". Use `in-1` para índice base 0.
- T (a duração do movimento) vem do briefing e é menor que a duração do bloco, para sobrar permanência. Terminar em 85 a 90% do bloco é só exemplo técnico.

## Sons

- **Um sonzinho na hora certa marca o número, a virada da história ou a entrada de um texto**, e ajuda a manter a retenção. O vídeo tem três camadas: fala, texto e som.
- **O som sempre entra por baixo da fala.** Calibre pelo p90 do RMS da voz do corpo.
- **Mapa por função** (sintetize localmente, sem pacote pago; cues em JSON, `{"t": segundos, "som": nome, "db": ganho}`):
  - **impacto grave:** junto do título no quadro 0, por baixo da primeira palavra (amostra: cerca de -4 dB em relação ao p90 da voz).
  - **clique curto:** texto ou item de lista entrando, de 10 a 15 dB abaixo da voz, um por item.
  - **pop suave:** emoji, print ou cartão entrando, de 15 a 25 dB abaixo da voz.
  - **moeda:** número de dinheiro.
  - **whoosh curto:** cartão ou bloco novo (cerca de 0,2 por 30 s).
  - **digitando rápido:** só se houver texto digitado na tela; na dúvida, nenhum.
  - **sting:** só com meme ou GIF.
  - **risada:** não sintetize; só com o ok do dono.
- **Nunca** som em legenda, em saída ou em sumiço de elemento.
- **Começa no primeiro quadro do elemento (mais ou menos 2 quadros).**
- **Contagem:** medido, cerca de 5 a 7 por 30 s. É referência anterior, não teto: se o dono pedir mais presença, marque entradas de elementos, cortes que mudam o plano e ênfases, registre o mapa e a contagem por versão, sempre abaixo da fala. Aumentar a contagem sozinho não atende ao pedido: o som precisa marcar o elemento.
- **Sem elemento, sem som.**
