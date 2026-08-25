---
name: soft-reel-7seg
description: Cria, corrige, valida e agenda Reels cinematográficos curtos cuja HEADLINE leva a pessoa a ler uma descrição longa e útil. Use quando o pedido envolver formato read-caption, personagem real em cena cinematográfica, HEADLINE sobre vídeo, microchamada na segunda metade, música, variante incremental, safe zone facial, substituição de mídia sem duplicar o post ou transformação desse fluxo em peça repetível.
---

# Soft Reel 7seg

Produzir um Reel curto que interrompe o scroll com uma cena forte, entrega a utilidade na descrição e preserva rosto, identidade, mídia aprovada e agendamento.

## Fluxo

1. Recuperar o contexto do usuário: negócio, público, oferta, voz, identidade visual, personagem e CTA. Se houver brand canônico do usuário, aplicá-lo; se não houver, pedir ou inferir somente o mínimo reversível. Nunca embutir o brand de um caso anterior como padrão universal.
2. Recuperar formato validado e métrica real. Separar estrutura, ritmo e gesto visual da tese do benchmark. Nunca copiar a tese, a identidade ou a prova.
3. Selecionar fotos reais do personagem e montar mosaico facial. Fixar traços literais, roupa, enquadramento e identidade antes de gerar a imagem-base.
4. Mostrar o quadro-base e parar no gate de aprovação antes de animar.
5. Cotar a animação antes de consumir crédito. Informar valor e esperar autorização. Fazer uma geração por autorização e preservar o MP4-base recebido.
6. Criar a HEADLINE com `soft-conteudo-headlines` e passar por `soft-critico-copy`. Para read-caption, escrever descrição grande, útil e salvável quando a ordem pedir. Escrever na voz, narrativa e limites comerciais do usuário atual. Não inventar prova, número, promessa ou dado pessoal.
7. Renderizar o overlay de modo determinístico com `scripts/render_reel.py`. Aplicar tipografia, cores e composição do brand atual. Manter o rosto dentro da safe zone, dividir a HEADLINE em duas caixas e mostrar a microchamada somente na segunda metade.
8. Usar música em alta no Instagram quando estiver disponível no fluxo de publicação. Se não estiver, apresentar a alternativa de trilha comercial gratuita e só incorporá-la depois da escolha do dono.
9. Exportar H.264/AAC, vertical, abaixo do limite do agendador. Rodar `scripts/validate_reel.py` e abrir quatro quadros do arquivo final com visão real.
10. Toda correção gera variante incremental. Nunca sobrescrever imagem-base, MP4-base, copy aprovada ou variante aprovada.
11. Fazer upload da nova variante e atualizar o mesmo post trocando somente a mídia. Ler o agendamento por fora e provar mesmo identificador, horário, texto, estado e ausência de duplicata. Se a edição não for segura, preservar o post anterior.

## Gates

- Brand do usuário atual confirmado ou recuperado; nenhum nome, oferta, prova, cor, fonte ou CTA herdado do caso Matrix por padrão.
- Quadro-base aprovado antes da animação.
- Gasto autorizado antes de crédito.
- Cabeça inteira, com folga mensurável entre cabelo e caixa.
- Microchamada ausente antes do tempo definido e presente depois.
- Quatro quadros, áudio, dimensões, duração, codecs e tamanho conferidos no arquivo final.
- Atualização externa sem novo post.

## Recursos

- Ler `references/caso-matrix-validado.md` ao modelar este formato ou ao decidir safe zone, ritmo, trilha e atualização incremental.
- Usar `scripts/render_reel.py --help` para renderizar a partir do MP4-base.
- Usar `scripts/validate_reel.py --help` para validar o arquivo final e produzir quatro quadros e mosaico.
