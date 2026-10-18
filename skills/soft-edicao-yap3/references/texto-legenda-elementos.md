# Texto, elementos e legenda do YAP

Lido nos passos 4, 5 e 7 da ordem de edição do `SKILL.md`. "Medido" descreve uma amostra de 19 reels de um perfil de nicho: é referência descritiva, não meta. A identidade (cor, fonte, logo) é a do dono; sem identidade declarada, só branco.

## Título e textos do topo

- **Título no quadro 0, durante todo o primeiro plano**, saindo exatamente no corte gancho → corpo. Medido: mediana de 5,5 s (de 3,3 a 10,3 s), saindo num corte em 5 de 8 reels.
- **O texto do título é o que foi falado.** Literal, sem resumo.
- **Fonte do título:** display forte e legível, branca ou na cor da identidade, grande, de 2 a 3 linhas, centrada no espaço livre do rosto e dentro da área de recorte abaixo (a medição anterior de 12% a 26% da altura é descritiva). Quebre as linhas sem deixar palavra isolada.
- **Segunda frase do título em manuscrita**, entrando no instante em que é falada, logo abaixo. A entrada é seca na palavra: digitar caractere por caractere no primeiro plano seria motion de abertura, que a regra 3 proíbe. (No corpo, depois do primeiro plano, texto digitado é permitido.)
- **Texto começa no quadro do corte ou da palavra.**
- **Do terceiro texto em diante, sans negrito itálico**, perto do rosto e dentro da área de recorte abaixo. Nunca sobre a boca nem sobre os olhos.
- **Mais texto no começo, menos depois.** Trecho sem texto é normal.
- **Lista com marcador (✅)**, um item por vez, na palavra, um embaixo do outro. Os itens se acumulam para baixo.
- **Onde há prova, entra print e não texto.** Objeção pode virar texto com emoji de dúvida.
- **Número** é a parte mais importante do título. Pode ir na cor de acento nos textos do topo, com parcimônia; na legenda, nunca.
- Texto inclinado é só sensação de edição: opcional.

### Área de texto nos recortes do feed (dono, 15/10/2026; ep2 aprovado)

- Evidências (prints do dono, guardados fora da skill): `file_5350.jpg` mostra títulos cortados; `file_5351.jpg` mostra títulos inteiros com margem na grade do perfil Manuscrito. Modelar o espaço entre topo e cabeça, conferindo a caixa inteira, acentos, sombra e complemento. Os prints não fornecem coordenadas do canvas original.
- Simulações locais em 1080x1920: 4:5 em y285 a 1635; 3:4 em y240 a 1680; interseção x0 a 1080, y285 a 1635. Respiro vertical de referência de 30 px (y315 a 1605); margem lateral nominal de 60 px. São critérios locais, sem promessa de exibição da plataforma. Conferir o recorte real quando disponível. Em outros vídeos, modelar espaço, caixa inteira e margem proporcional, sem mover o rosto.
- Molde específico aprovado do gancho ep2 (vídeo do projeto original, guardado fora da skill): `gancho-ep2-ajuste-fino.mp4`. Caixas [44,315,1036,553] e [44,315,1036,663], com 30 px acima no recorte 4:5. Preservar a largura aprovada além da margem lateral nominal, sem distorcer nem diminuir o PNG. A translação +280 px pertence aos PNGs originais desse projeto, nunca é deslocamento universal.
- Ajuste exclusivo de posição move só a camada de texto. Preservar apresentador, ângulo, escala, enquadramento, fundo, cortes, áudio, velocidade, PNG original, tamanho, palavras, quebras, fontes, cores e entradas. Não cortar a cabeça nem preencher cenário para acomodar título. Se o texto não couber com olhos e boca livres, registrar o conflito e obter direção sobre o texto antes de alterar outro componente.
- Conferir cada composição do trecho autorizado, maior estado, entrada do complemento e último quadro. Produzir mosaico antes/depois 9:16 e simulações 4:5 e 3:4 nos mesmos tempos. Letra cortada reprova; avaliar respiro pela referência aprovada, sem impor novamente 60 px verticais. Registrar tempos e limites da inspeção. Preservar o restante do método.

### Fontes (todas livres)

- **Título e legenda:** uma família display ou serifada legível, em um peso regular a bold.
- **Segunda linha manuscrita:** Kalam Bold (OFL).
- **Textos seguintes, sans negrito itálico:** Inter Display Black Italic ou ExtraBold Italic.
- **Pares de fontes** (use um par só por série): Bodoni Moda e DM Sans, Sora e Mukta, Cormorant e Raleway, Instrument Serif e Poppins, Fraunces e DM Sans, Playfair Display e Poppins, Vesper Libre e Raleway, Merriweather e Manrope.

### Como montar

Textos do topo em PNG feitos com PIL, não em ASS: o libass não desenha emoji colorido nem faz glow. Emoji com `NotoColorEmoji.ttf` no tamanho 109 e `embedded_color=True`, depois redimensionado. Sombra escura suave em duas camadas (blur 10 e 3) quando o fundo for movimentado. Trecho entre colchetes no plano sai na cor de acento. Bloco empilhado e centrado dentro da área de recorte acima, com quebra em cerca de 960 px; lista em 2 colunas com ✅. Passe a pasta de fontes ao filtro: `subtitles=...:fontsdir=fontes`.

## Elementos (prints, emojis, figurinhas)

- **Entra na palavra exata em que é citado.** Medido: mediana de -0,04 s do início da palavra (de -0,14 a +0,27). Entrada seca (ausente no quadro n-1, completo no n).
- **Surge e desaparece** quando o assunto muda. Medido: saída seca, de preferência num corte.
- **Nada atravessa o corte de plano.** Exceção: jump cut do mesmo enquadramento dentro da mesma frase (anote).
- **Prova social é a parte mais importante.** Tudo que dá para provar, prova-se: o print entra junto com a fala que ele prova.
- **Prints em sequência, no mesmo tamanho e na mesma posição.** Comentários podem entrar tortinhos, um de cada vez. Medido: cartões brancos arredondados.
- **Prova de número corresponde ao número e ao período da fala.** Um print que repete a alegação, ou uma medição atual de seguidores, não comprova resultado financeiro nem número histórico. Sem prova própria pública ou autorizada, mantenha a fala e registre a pendência.
- **Figurinha animada** gera retenção, mas é opcional e depende do estilo do dono.
- **Emoji quando "parece que está faltando"** um elemento.
- **Marcas gráficas** (círculo, seta, sublinhado, tachado): escolha pelo sentido. O círculo destaca um dado; a seta liga a prova ao ponto observado; o X rejeita uma alternativa; o tachado nega ou substitui o texto atingido (não risque uma afirmação verdadeira só para variar). A cor sai da identidade do dono. Sem função clara, não aplique.
- **Máscara "sanduíche"** (pessoa, figurinha, pessoa recortada para a cabeça passar na frente): não há recorte automático confiável. Não use sem pedido.
- **Sem música.** Medido: nenhum dos 19 reels tem música.
- **Apoio lateral em vídeo** (foto, print ou vídeo pequeno no instante em que a fala pede a demonstração): posição e tamanho pelo espaço livre junto da cabeça, preservando rosto, legenda e legibilidade da interface. O apoio de vídeo precisa de movimento real e origem conhecida. Uma demonstração de uso pede o celular e a tela completos, com a ação acelerada, nunca um recorte quadrado em que nada se mexe. Não mostre nome, contato nem conversa privada de terceiros. Quando houver pedido e resultado, confira a relação real entre eles: uma mensagem posterior não é o pedido inicial.
- **Sem print real, não invente.** Use o número em texto e deixe a pendência para o dono.
- **Cor da gravação e retoque de pele:** preserve a aparência do bruto. Sem pedido explícito, não aplique filtros, LUT, embelezamento, retoque ou correção automática nem altere brilho, exposição, contraste, saturação ou balanço de branco. Conversão HDR/HLG/Dolby Vision segue a seção “Preservar a aparência de cor do bruto” do `SKILL.md`, com referência de reprodução confiável e comparação do final nos mesmos instantes; a conversão não autoriza mudar a aparência.

## Legenda (só quando o dono pediu)

O padrão é SEM legenda. Pedida, ela vai por último e segue isto:

- **Uma palavra por vez, sempre uma linha.** Medido: troca seca a cada 0,23 a 0,37 s, aparecendo cerca de 0,05 s depois do início da palavra.
- **Serifada regular branca, sem contorno, pequena** (medido: cerca de 55 px em 1080).
- **No ombro, ao lado do rosto, não embaixo do pescoço.** Medido: centro em x de 0,60 a 0,68 e y de 0,49 a 0,61, posição fixa no vídeo inteiro, mesmo nos punch-ins. Confira no mosaico do bruto onde fica o queixo de cada gravação e ajuste a posição a esse enquadramento.
- **Grafia conferida contra a fala**, na caixa original.
- **Sem destaque colorido.**
- **Some quando um título ou print grande ocupa a área.**
- **Montagem em ASS (libass):** `Fontsize` perto de 56, `PrimaryColour=&H00FFFFFF`, `Outline=0`, `Shadow=0` (ou 1, fraca, só se a legibilidade pedir), `Alignment=5`, `\pos(x,y)`. Um `Dialogue` por palavra, do início da palavra ao início da seguinte (no máximo 0,7 s; some na pausa). Palavra com menos de 0,12 s junta com a seguinte. Tire vírgula, ponto e reticências do fim; mantenha o "?". Fixe no plano a grafia de marcas e siglas do dono.
- **Início da palavra no tempo de saída:** a palavra cujo início cai num corte vai para o primeiro quadro do segmento seguinte. O Whisper às vezes adianta o início em 0,3 a 0,5 s depois de uma pausa: corrija pela energia do áudio.
- **Textos maiores:** quando o dono pedir, aumente a partir das camadas anteriores à queima, mantenha hierarquia, cores e área livre do rosto, e compare antes e depois no tamanho de um celular. Confira todas as composições e a maior palavra da legenda: ampliação que corta texto ou cobre o rosto volta para correção.
