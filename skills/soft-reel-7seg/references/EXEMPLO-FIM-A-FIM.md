# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, marca, números, valores de crédito e resultados foram
> inventados só pra mostrar a FORMA de cada saída. Nada disso é caso real, nada disso pode ser
> copiado pra uma entrega de verdade. Num trabalho real, todo número e toda prova sem fonte nascem
> marcados `[A CONFIRMAR]` e o dono confirma antes de sair.

**O caso fictício:** uma restauradora de móveis antigos, que vende um curso de restauro pra
iniciante. Personagem: ela mesma, na oficina. Identidade fictícia dela: âmbar sobre madeira escura,
tipografia pesada. Assunto do reel: por que a maioria estraga o móvel na primeira lixada.

---

## 1 · O contexto recuperado (passo 1)

Do brain do agente vieram: público (adulto que herdou um móvel de família e tem medo de estragar),
voz (direta, sem termo técnico), oferta (curso de restauro pra iniciante), CTA (comentar uma palavra
pra receber o link).

O que não veio: a identidade visual. A skill pediu, e ela mandou a cor âmbar e a fonte.

**O que a skill NÃO fez:** herdar cor, prova ou CTA de um caso anterior que tinha funcionado. O
formato é reutilizável; a identidade de quem usou antes não é.

## 2 · O formato de referência (passo 2)

A skill leu `caso-matrix-validado.md` e separou o que é reutilizável do que era daquele caso:

| Reutilizável | Daquele caso, não copiar |
|---|---|
| headline em duas caixas | a tese do caso |
| microchamada só na segunda metade | a identidade visual dele |
| safe zone do rosto com folga medida | a prova e os números dele |
| variante incremental na correção | o CTA dele |

## 3 · O mosaico facial (passo 3)

Ela mandou 6 fotos na oficina. A skill montou o mosaico e fixou, por escrito, antes de gerar
qualquer imagem: cabelo preso, avental marrom com respingo de verniz, óculos de proteção na testa,
enquadramento do peito pra cima, luz vindo da janela à esquerda.

Fixar isso por escrito é o que evita o rosto mudar entre o quadro-base e o vídeo, que queima a peça
inteira e o crédito junto.

## 4 · O STOP do quadro-base (passo 4)

> "Esse é o quadro-base. Aprova antes de eu animar? Depois de animar, mudar o rosto custa crédito de
> novo."

**O que ela pediu:** os óculos na testa estavam tortos e o avental tinha saído limpo demais. Duas
correções no quadro-base, custo zero. As mesmas duas correções depois da animação custariam a
geração inteira.

## 5 · O STOP da cotação (passo 5)

> "Pra animar esse quadro em 7 segundos, o custo é de mais ou menos 4 créditos de geração de vídeo.
> Autoriza? Eu faço uma geração por autorização, e guardo o MP4-base pra qualquer correção depois
> não precisar gerar de novo."

Ela autorizou. Uma geração, e o MP4-base foi preservado no disco, intacto, o arquivo inteiro.

## 6 · A headline e a descrição (passo 6)

A headline nasceu aqui mesmo, pela régua própria da skill em `headline-de-emergencia.md`.

**Gatilho escolhido:** crença. O público acha que restaurar começa lixando, e é aí que ele estraga.
Um gatilho só, escolhido de propósito.

**Headline, nas duas caixas:**

> caixa 1: `O móvel da sua avó não estraga`
> caixa 2: `no verniz. Estraga na primeira lixada.`

Contagem: 29 e 38 caracteres. Contados, não estimados, porque a segunda caixa passando de linha é o
erro mais comum do formato.

**Microchamada:** `Leia a descrição ↓`, entrando aos 3,5 segundos de um vídeo de 7.

**Descrição (o que carrega a utilidade, resumida aqui):**

> Antes de encostar uma lixa em móvel antigo, faça isso.
>
> 1. Descubra o que é o acabamento. Passa álcool num pedaço escondido: se amolecer, é goma-laca, e
>    goma-laca sai sem lixa nenhuma.
> 2. Só lixe o que já está solto. Verniz firme não sai por lixa, sai por solvente.
> 3. Comece pela parte de baixo, onde ninguém olha. Você aprende a mão no lugar que perdoa erro.
> 4. Grão fino é mais lento e mais seguro. Grão grosso come a madeira e não tem volta.
>
> A madeira que você tirou não volta. O verniz sempre volta.
>
> Comenta RESTAURO que eu te mando o passo a passo completo.

**O gate anti-IA inline rodou** na headline e na descrição. Ele reprovou a primeira versão da linha
de fechamento, que era "a verdade é que a madeira não volta", por frase-emoldura. Refez só aquela
linha, não a peça.

## 7 · O render (passo 7)

```bash
python3 scripts/render_reel.py \
  --base ./mp4-base.mp4 --audio ./trilha.m4a --output ./reel-restauro-v1.mp4 \
  --line1 "O móvel da sua avó não estraga" \
  --line2 "no verniz. Estraga na primeira lixada." \
  --headline-y 210 --face-top-y 430 --min-face-gap 32 \
  --font-size 40 --call "Leia a descrição ↓" --call-time 3.5 --call-y 800 \
  --duration 7.0 --max-mb 5.0
```

## 8 · A trilha (passo 8)

O fluxo de publicação deste ambiente não dava acesso ao catálogo da plataforma. A skill apresentou
duas opções de trilha comercial gratuita e **esperou a escolha dela**. Ela escolheu a segunda.

Se nenhuma existisse, a escada seguiria: áudio original da animação, e em último caso uma faixa
silenciosa da mesma duração, com o aviso de que ela escolhe a música dentro do aplicativo na hora de
postar. O que nunca sai é arquivo sem faixa de áudio.

## 9 · Os quatro quadros de conferência (passo 9)

```bash
python3 scripts/validate_reel.py --video ./reel-restauro-v1.mp4 \
  --manifest ./manifesto.json --frames-dir ./quadros
```

O validador aprovou: vertical, H.264 e AAC, 7,0 segundos, 3,8 MB, folga de 48 pixels entre o cabelo
e a caixa da headline, microchamada ausente antes de 3,5s e presente depois.

**Depois disso, os quatro quadros abertos com o olho:**

> - **Quadro 01 (0,7s):** headline legível, as duas caixas cabem sem cortar palavra, microchamada
>   ausente, cabeça inteira no quadro. Passou.
> - **Quadro 02 (3,0s):** microchamada ainda ausente, correto. A folga entre o cabelo e a caixa está
>   visível. Mas a cena escureceu neste trecho e a segunda linha da headline perdeu contraste contra
>   a madeira. **Reprovou:** subi o peso do fundo da caixa de 40% pra 65% de opacidade.
> - **Quadro 03 (4,2s):** microchamada apareceu, não colidiu com a headline nem com o rosto, texto
>   legível. Passou.
> - **Quadro 04 (6,6s):** tudo no lugar no fim, sem estouro de brilho. A palavra "lixada" ficou
>   sozinha na segunda caixa. **Reprovou:** ajustei a quebra pra "na primeira / lixada" virar uma
>   linha só.
>
> Re-renderizei com as duas correções e conferi os quatro quadros de novo: os quatro passaram.

Os dois problemas eram de imagem. O validador aprovou o arquivo nas duas vezes, porque ele prova
número, não prova imagem. É por isso que abrir os quadros é obrigatório.

## 10 · O STOP antes de subir (passo 10)

> "Esse é o mosaico dos quatro quadros. Pode subir?"

Ela aprovou.

---

## A Ação 2 no mesmo caso: a variante

Dois dias depois ela pediu pra trocar a palavra do CTA, de RESTAURO pra MADEIRA.

**O que a skill fez:**

1. Não sobrescreveu nada. Nem o MP4-base, nem a `v1`, nem a descrição aprovada.
2. Como a mudança era só na descrição, nem o overlay precisou de render novo. Se fosse na headline,
   re-renderizaria o overlay a partir do MP4-base preservado, **sem gerar animação de novo e sem
   gastar crédito**.
3. Subiu a `v2` e **atualizou o mesmo post agendado, trocando só a mídia**.
4. Leu o agendamento por fora e provou: mesmo identificador, mesmo horário, mesmo texto, estado
   ainda agendado, nenhuma duplicata na conta.

Se a edição não fosse segura, a regra é preservar o post anterior e contar o que aconteceu. Post
duplicado divide o alcance e some com a métrica.

## O que este exemplo prova sobre o fluxo

1. Os dois STOPs antes do gasto (quadro-base e cotação) são o que separa uma geração de três.
2. Contar os caracteres da headline em vez de estimar é o que evita a segunda caixa estourar.
3. O validador aprovou um arquivo que tinha dois defeitos visíveis. Os quatro quadros existem
   exatamente pra isso.
4. Preservar o MP4-base fez a correção custar zero crédito.
