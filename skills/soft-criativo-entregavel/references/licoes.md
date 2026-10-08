# Lições (erros que já custaram tempo ou créditos)

Leia quando algo falhar ou o resultado sair estranho.

## Entendimento do formato
- **Gancho = frase absurda + alívio.** Cortar só a frase absurda foi reprovado.
- **Animação que não mostra o material é desnecessária.** Contador "mente a mil", bateria descarregando, conversa em balões, interruptor: todas reprovadas. O usuário quer o material na tela o quanto antes e o tempo todo, com contexto (a pílula com as palavras da fala).
- **Cortes demais cansam.** Tela nova a cada ~3 s não deixa ver o material. Junte frases curtas na tela vizinha e faça a tela evoluir.
- **Sem legendas.** Só pílulas curtas. A exceção é o gancho sem avatar (tela `frase`).

## Voz e tempo
- **Tempo estimado erra.** Dividir a frase proporcionalmente pelas sílabas chegou a errar 1 s. Use sempre `alinhar.py` e amarre os eventos às palavras.
- **Resto de fala no fim do áudio.** Alguns áudios gerados terminam com um pedaço de palavra solto ("…ltima palavra"). A transcrição mostra; use `audio_fim` no `projeto.json` para cortar.
- **Áudios "Acelerado".** Já vêm no ritmo final; K = 1. Os outros pedem K entre 1,15 e 1,35. Compare com um anúncio oficial da oferta se houver dúvida (duração do áudio ÷ duração do oficial).
- **Reconhecedor falha em prefixos curtos.** Linhas com "[Música]" no alinhamento são falhas pontuais; use as linhas vizinhas.

## Avatar
- Ver `references/avatar.md`, seção 7. Resumo: não pedir silêncio, duração justa (o modelo espalha a fala pelo clipe), tom de indicação com prompt curto, divisa pela transcrição, gesto descrito com clareza, conferir palavra por palavra.
- **Volume.** O áudio do FLUX vem 10 a 18 dB mais baixo que a voz do áudio; o script nivela e reduz ruído. Se o usuário reclamar de chiado nas falas do avatar, é o ruído amplificado: regenere ou reduza o ganho.
- **Créditos.** Cada regeneração custa o clipe inteiro. Por isso conferir a fala antes de qualquer outra etapa e avisar o usuário antes de regenerar.

## Render e arquivos
- **Memória.** 24 processos de render de uma vez derrubaram o codificador ("malloc failed"). O padrão é 6; um render por vez. Se falhar, `render 4`.
- **Caminhos com acento.** O ffmpeg no Windows não lê lista de arquivos com acento se ela não estiver em UTF-8. O motor já usa nomes relativos; ao escrever scripts novos, grave arquivos de texto com `encoding='utf-8'` e passe filtros longos por arquivo (`-/filter_complex arquivo.txt`).
- **Disco.** Takes recortados ocupam ~83 MB por segundo. Confira o espaço antes e mantenha os takes curtos.
- **Python.** O Python padrão da máquina pode não ter as bibliotecas (ex.: 3.15 beta). Use o ambiente próprio em `~/.cache/soft-criativo-entregavel/venv`.
- **Último quadro de uma transição.** Quando o progresso da mancha chega a exatamente 0,5, só existe um dos dois lados; o motor já trata. Se aparecer `NoneType has no attribute copy`, o erro está numa tela nova que não devolve imagem.

## Fundos
- **Preenchimento em bloco.** Tirar o objeto do fundo deixa um retângulo visível se o preenchimento não for bem desfocado; `fundos.py` já difunde e costura as bordas. Se ainda aparecer, aumente a caixa.
- **Texto sobre objeto do fundo.** Título solto em cima de um objeto do fundo fica ruim de ler; por isso os textos vão em pílulas ou cartões brancos.

## Conferência
- Conferir por quadros (`folha`, `stills`) antes de renderizar; a folha leva segundos, o render leva minutos.
- Você não ouve o vídeo. No resumo, separe o que foi verificado (quadros, palavras reconhecidas, duração, volume) do que o usuário precisa ouvir.

## Siglas e nomes soletrados (oferta PMPE, 2026-10-03)
- **Sigla na fala do avatar.** Com "PMPE" no fim do gancho, o reconhecedor escreveu "PMP"/"APMP" e `montar_base.py` parou sem achar a última palavra. Ajuste `palavras.ultima_gancho` para a grafia que apareceu em "fala completa" e peça ao usuário para ouvir a sigla: pela transcrição não dá para saber se o avatar engoliu a última letra.
- **Duração com sigla.** Sigla soletrada conta como 3 palavras na conta da duração.
- **Caminho do áudio no `projeto.json`.** Escreva com barras normais (`D:/pasta/...`); barra invertida gravada pelo terminal quebra o JSON.
- **Oferta sem mockup e sem takes.** Funciona só com as páginas: a tela `capa` apresenta o produto e o CTA fica com o avatar. Páginas de tamanhos diferentes na mesma oferta (1055x1491 e 1024x1536) não atrapalham; as regiões são sempre na página com 1024 de largura.

## Recorte do avatar (gancho sobre o material, 2026-10-03)
- **Modelo de foto, quadro a quadro, é lento demais.** O birefnet (via rembg) levou 4 a 8 s por quadro e ~12 GB de memória: mais de 10 minutos para um gancho de 6 s, e com 2 processos faltou memória. O usuário recusou ("se for demorar tudo isso pra cada AD não vou querer"). O `recortar_avatar.py` usa o Robust Video Matting, feito para vídeo: 8 a 16 s para o gancho inteiro, recorte limpo.
- **Regra geral:** quando uma etapa local passar de 1 a 2 minutos por criativo, pare e procure uma ferramenta própria para vídeo antes de deixar rodando.
- **O modo virou padrão em 2026-10-03** ("torne padrão"), na versão do print parado.
- **Pedido simples, solução simples.** O pedido era "avatar sem fundo, com o primeiro frame do corpo atrás". Eu fiz a primeira tela rodar animada desde o segundo 0 e mexi no começo do corpo; ele reprovou: queria só um print parado, com o corpo igual ao de sempre. Quando o pedido couber em uma frase, faça o que a frase diz e, se houver duas leituras, diga em duas linhas o que entendeu antes de construir.

## Identidade visual e textos (2026-10-04)
- **"É sempre o mesmo 3D."** O estilo dos fundos era fixo e só mudavam cor e objeto. O usuário pediu que o fundo replicasse a identidade do entregável e aprovou. Hoje a identidade é lida do material em cada oferta (`references/oferta.md`).
- **Fundo com textura não aceita "tirar o objeto".** Por isso os fundos são gerados limpos e os elementos vêm de uma folha separada, em magenta, recortada por cor (`fundos_identidade.py`).
- **Pílula branca igual o vídeo inteiro foi reprovada.** "Quero variedades e não só esse padrão." Agora cada texto tem um estilo e o tema da oferta; o conjunto aprovado está em `references/roteiro.md`, seção 6.
- **Fonte faltando.** Baixar fonte do Google Fonts pelo GitHub pode devolver uma página de erro salva com extensão .ttf (arquivo de ~270 KB que não abre). Confira o código de resposta (200) e abra a fonte uma vez antes de usar.
- **Quadro preto na saída do avatar.** Buscar o último quadro do gancho podia cair no preto do corpo; o motor agora usa 3 quadros antes do fim.
