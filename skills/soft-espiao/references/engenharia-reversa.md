# Engenharia reversa: a ficha de 8 campos

Lida na Ação 3. A ficha desmonta um anúncio, uma VSL ou um funil concorrente pra achar o princípio que faz vender. Ela é material de estudo do dono e nunca vai a público.

## Antes de desmontar

- **Confirme a classe.** Desmonte pra modelar só anúncio da classe `vendendo` da planilha (`sinais-de-venda.md`). Fora dela, pode ser oferta quebrada: o erro mais comum é modelar VSL que já está falindo. Se o dono pedir assim mesmo, a primeira linha da ficha diz `sem sinal de venda confirmado`.
- **Anúncio que o dono só colou (sem linha na planilha).** Com shell e token, rode a coleta com `--pagina-id` da página dele e cole a linha do anúncio; sem shell, peça o link da biblioteca e o print com "Veiculação iniciada em" e "N anúncios usam este criativo". Sem nenhum dos dois, a ficha abre com `sinais não medidos`.
- **Black sai antes dos sinais.** Link que abre página diferente da anunciada, falso especialista, cura ou prazo garantido, rede de páginas de nome genérico: a ficha não modela, diz `descartado: <motivo>` em 1 linha, e o sinal de venda não muda isso.
- **Técnica ou personalidade.** Técnica: anúncio ativo há semanas, especialista pouco conhecido fora do nicho, venda puxada por tráfego pago. Personalidade: pouca ou nenhuma mídia paga, audiência grande que compra a pessoa. Peça de personalidade serve de estudo, nunca de régua pro dono sem a mesma audiência, porque ali a autoridade vende até copy fraca.
- **Material.** Link da biblioteca, o vídeo ou a transcrição, a página de destino aberta. Sem transcrição, a skill pede ao dono que cole a fala dos primeiros 30 segundos.

## A ficha

Cada campo leva o que se viu e onde se viu (minuto do vídeo, trecho da página). Citação literal do concorrente vai dentro de bloco de código cercado, marcada como estudo.

| Campo | O que anotar |
|---|---|
| 1 · Ângulo | a dor ou o desejo que o anúncio ataca, e pra quem (quem fica de fora) |
| 2 · Gancho | os primeiros 3 a 5 segundos: o que se vê e o que se ouve. Tipo: pergunta, afirmação que contraria, história, demonstração, notícia |
| 3 · Formato | apresentador falando, conversa em estúdio com microfone, entrevista de rua, conteúdo de criador, slides, animação, depoimento. Duração e ritmo |
| 4 · Estrutura invisível | frase a frase, a FUNÇÃO de cada uma: credibilidade, história, prova, mecanismo do problema, mecanismo da solução, quebra de objeção, chamada. É a ordem dessas funções que se modela |
| 5 · Mecanismo | o nome que ele dá ao problema e à solução, e quanto disso o público já conhecia |
| 6 · Oferta | preço, parcelamento, bônus, garantia, escassez, tipo de produto |
| 7 · Página e funil | pra onde o clique vai: VSL, quiz, carta, página de captura, checkout. O que aparece depois da compra quando dá pra ver |
| 8 · Técnica ou personalidade | o veredito do item acima, com o motivo |

**O que não dá pra ver sai `não visível`:** margem, verba, upsell escondido, taxa de conversão. Palpite sobre esses campos não entra na ficha.

## Leitura em grupo (quando o dono tem time)

Assistir o anúncio de 5 a 10 vezes sem julgar, com 3 olhares: quem escreve olha mecanismo, argumento e estrutura invisível; quem edita olha trilha, corte e take; o especialista olha como gravou (roupa, tom, cenário). Padrão que só um dos três viu entra como hipótese.

## Fechamento da ficha

Termine com 3 linhas:
- `princípio:` por que isso vende, em 1 frase, sem citar a peça;
- `modelável:` sim ou não, e o nível (rasa, estudiosa, nicho vizinho) que cabe;
- `fica de fora:` o que depende do concorrente e não se leva (a história dele, a audiência dele, a prova dele).
