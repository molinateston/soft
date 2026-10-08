---
name: soft-criativo-entregavel
description: "Produz criativos de vídeo verticais (1080x1920) para tráfego pago de infoproduto low-ticket a partir só do ÁUDIO de cada criativo: um avatar UGC brasileiro gerado no Higgsfield (FLUX 3) fala o gancho e o CTA, e o meio inteiro mostra o entregável (páginas/folhas animadas e takes de vídeo), com pausas da voz cortadas, mancha de transição, fundos com objetos flutuando e efeitos sonoros. Use SEMPRE que o usuário mandar um ou vários áudios de criativos (a leva costuma ter 5) e pedir para editar, montar, gerar ou produzir os vídeos; quando disser 'faz a leva', 'edita esses ADs', 'criativo com avatar', 'criativo com as folhas', 'com as prévias', 'com os takes', 'sem avatar só com o material', 'igual o AD 05', 'no formato avatar + folhas'; ou quando apontar a pasta raiz de uma oferta com os áudios dos anúncios e quiser os vídeos prontos, mesmo sem citar a skill. Não é para escrever copy nem escolher formato de criativo (isso é da criativos-formatos)."
---

# Criativos: avatar nas pontas, entregável no meio

Edita criativos de anúncio em que **o material é o protagonista**. A pessoa que assiste precisa ver logo do que se trata o produto (as folhas, as páginas, o tablet) e ter tempo de entender; o avatar existe para segurar a atenção no gancho e pedir o clique no fim.

Nesta casa: este é o motor de EDIÇÃO (áudio pronto vira vídeo). Ângulo, copy e plano de teste do anúncio ficam com soft-criativo-campeao; o roteiro/áudio vem de lá. Ambiente Linux: ffmpeg e uv já existem; o venv de Python (seção 2) ainda não foi criado e baixa ~750 MB na 1ª vez. Higgsfield só roda se o conector estiver na sessão; sem ele, use a configuração "sem avatar".

Fale com o usuário em português do Brasil, direto, sem emojis. Ele não é programador: evite jargão, explique em palavras simples o que está fazendo.

## O formato (e por quê)

| Parte | O que aparece | Voz |
|---|---|---|
| Gancho | Avatar gerado, **recortado, sem o fundo dele**, por cima de um print parado da primeira tela do corpo; fala a frase absurda **e a frase de alívio** | do avatar |
| Meio | Só material: páginas animadas e/ou takes de vídeo, com textos curtos e animados que repetem palavras da fala | do áudio recebido |
| CTA | Avatar apontando para baixo, no cenário dele, com setas animadas (ou tela de mockup + "Link aqui embaixo" se não houver avatar no CTA) | do avatar ou do áudio |

Regras que o usuário definiu depois de ver os testes. Elas valem para todo criativo:

1. **O gancho inclui o alívio.** O gancho quase sempre é uma afirmação absurda seguida de uma frase que transfere a responsabilidade ("foi isso que um conhecido meu soltou", "foi uma das frases mais absurdas que eu ouvi"). As duas são do avatar. Se o corte ficar só na frase absurda, a outra voz entra explicando o que a primeira disse e o criativo perde o sentido.
2. **Material o quanto antes e o tempo todo.** Assim que o avatar termina, entra material e ele fica até o CTA. Nada de animação que não mostre o material (contador, bateria, balões de conversa e interruptores foram reprovados como "desnecessários"). Se a fala é sobre uma dor, mostre uma página do produto que trate daquele tema, com a pílula de texto.
3. **Tempo para ver.** Cada tela de material fica pelo menos uns 3,5 s; o comum é 5 a 9 s. Em vez de cortar para uma tela nova a cada frase curta, faça a tela anterior evoluir (a página cresce, entra uma pílula nova). Mas não tire a dinâmica: dentro da tela sempre acontece algo a cada 1 a 2 s.
4. **Pausas e respiros cortados** na voz do áudio.
5. **CTA sempre aponta para baixo** (gesto do avatar e setas).
6. **Sem legendas; textos curtos e animados, com variedade.** Só textos curtos com palavras que estão sendo ditas, nada de enchimento. Cada texto tem um estilo de animação (palavra por palavra, marca-texto, palavras soltas, faixa, ícone animado, texto grande) e o estilo muda ao longo do vídeo conforme o tipo da frase. Pílula branca igual do começo ao fim foi reprovada. Catálogo em `references/roteiro.md`, seção 6.
7. **Tudo na identidade visual do material.** Fundos, elementos que flutuam, fonte e cores dos textos são tirados das páginas do produto, para o vídeo inteiro parecer a mesma peça (pergaminho e aquarela para um material de mapas antigos, por exemplo). O 3D brilhante igual em toda oferta foi reprovado. Como ler a identidade e gerar os fundos: `references/oferta.md`, seções 3 e 5.
8. Duas vozes (avatar e áudio) são aceitas.
9. **O avatar fala como indicação, nunca como propaganda.** Tem que parecer vídeo orgânico: alguém contando para um conhecido uma coisa que está usando. Fala arrastada ("texto solto"), fala animada de apresentador e fala dura de teleprompter foram as três reprovadas. Quando a primeira frase do áudio não abre como gancho (é descritiva, tipo "Olha por dentro do Guia…"), adapte de leve o texto do avatar para virar uma chamada de conversa ("Ô, se liga só. Olha esse guia ilustrado da prova da PMPE por dentro."), sem prometer nada que a copy não promete. As palavras e o jeito seguem o público da oferta: concurso de Polícia Militar pede um homem sóbrio e direto; "gente" foi reprovado para avatar homem.
10. **No gancho o avatar aparece sem fundo, sobre um print do corpo.** Atrás dele fica uma imagem parada da primeira tela do corpo, como se ele estivesse mostrando o que vem a seguir; quando termina de falar, ele sai e essa imagem começa a se mexer. O corpo é planejado e animado como sempre: nada é criado, esticado ou adiantado para ficar atrás do avatar. É o padrão desde 2026-10-03 e sai sozinho (o motor e o `montar_base.py` já fazem); só desligue se o usuário pedir o avatar "com o quarto atrás" (`"gancho_sobre_material": false` no roteiro).

## 1. Antes de começar: combinar a configuração

Peça ao usuário, de uma vez (use perguntas com botões se a ferramenta existir):

- **Os áudios** da leva (um por criativo) e a **pasta raiz da oferta**, onde ficam as páginas, mockups e takes.
- **Avatar:** no gancho e no CTA / só no gancho / sem avatar.
- **Material do meio:** só as folhas (imagens das páginas da pasta) / só os takes de vídeo que ele gravou / mescla dos dois.

Essas duas escolhas dão as pré-configurações que ele costuma pedir pelo nome:

| Como ele chama | Avatar | Material |
|---|---|---|
| Avatar com as folhas (o do AD 05) | gancho+cta ou gancho | folhas |
| Avatar com os takes que gravei | gancho+cta ou gancho | takes ou mescla |
| Sem avatar, só as imagens da pasta | nenhum | folhas |
| Sem avatar, mescla | nenhum | mescla |

Vale a mesma configuração para a leva inteira, a não ser que ele diga o contrário. Se ele já disse a configuração no pedido, não pergunte de novo.

**A pergunta do material é obrigatória.** Não decida sozinho pelo que achou na pasta. Se a pasta da oferta não tem vídeos, pergunte mesmo assim e diga isso na pergunta ("não achei takes nesta pasta: quer só as folhas, ou os takes estão em outro lugar?"): ele pode ter gravado e ainda não ter colocado ali. O mesmo vale para o mockup que faltar.

**Higgsfield.** Os modos com avatar precisam do conector Higgsfield (gera o vídeo do avatar e, uma vez por oferta, os fundos). Confira se as ferramentas dele existem na sessão (procure por `generate_video`, `models_explore`, `balance` do Higgsfield; carregue-as se estiverem adiadas) e chame `balance` para ver os créditos. Se não houver conector, avise o usuário e pergunte se ele conecta agora ou se quer rodar sem avatar; sem Higgsfield os fundos saem em degradê gerado por código, mais simples.

**Créditos.** Antes de gerar qualquer coisa no Higgsfield, diga quanto custa (consulte com `get_cost: true`) e espere o ok para a leva. Antes de **regenerar** um avatar que saiu errado, avise de novo. Referência de 2026-10: `flux_3_video` 720p custa 5,5 créditos por segundo; um avatar de gancho+CTA fica entre 60 e 95 créditos.

**Gênero e perfil do avatar** não se perguntam se o áudio já responde: `analisar_audio.py` estima pela voz. Só pergunte se der "incerto".

## 2. Ambiente (uma vez por máquina)

**Antes de qualquer outra coisa, confira se a máquina tem o que a skill precisa** (numa máquina nova quase nunca tem tudo):

```bash
command -v ffmpeg ffprobe uv; ls ~/.cache/soft-criativo-entregavel/venv 2>/dev/null | head -1
```

Cada programa que existe aparece com o caminho; o que não aparecer está faltando. Se faltar algum, **pare e diga ao usuário, em palavras simples, o que falta e para que serve**, e pergunte se pode instalar (é programa novo no computador dele: não instale sem o ok). Com o ok:

| Falta | Para que serve | Windows | Mac | Linux |
|---|---|---|---|---|
| `ffmpeg` (traz o `ffprobe`) | cortar, juntar e gravar os vídeos | `winget install Gyan.FFmpeg` | `brew install ffmpeg` | `sudo apt install ffmpeg` |
| `uv` | criar o Python próprio da skill | `winget install astral-sh.uv` | `brew install uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

Depois de instalar, o terminal precisa ser reaberto para achar o programa novo: confira de novo com o comando acima e, se ainda não aparecer, peça ao usuário para fechar e abrir o aplicativo. Não siga para os criativos enquanto os três não aparecerem. Sem o conector do Higgsfield a skill ainda roda, só sem avatar e com fundo simples (seção 1).

Os scripts ficam em `scripts/` desta skill e rodam com um Python próprio:

```bash
PY=~/.cache/soft-criativo-entregavel/venv/Scripts/python.exe   # Windows; em Linux/Mac: venv/bin/python
S=~/.claude/skills/soft-criativo-entregavel/scripts             # a pasta scripts/ desta skill; no Codex: ~/.codex/skills/soft-criativo-entregavel/scripts
```

Se `$PY` não existir, crie (o Python padrão da máquina pode ser novo demais para as bibliotecas; use 3.13):

```bash
mkdir -p ~/.cache/soft-criativo-entregavel && cd ~/.cache/soft-criativo-entregavel && uv venv --python 3.13 venv
uv pip install --python venv/Scripts/python.exe pillow numpy scipy soundfile sherpa-onnx opencv-python-headless onnxruntime
```

No Mac e no Linux o Python do ambiente fica em `venv/bin/python` (troque nos dois comandos). Na primeira vez baixam sozinhos o modelo de transcrição (Whisper, ~640 MB) e o de recorte do avatar (107 MB): avise o usuário que essa primeira rodada demora mais e precisa de internet. Rode sempre com `export PYTHONIOENCODING=utf-8` e passe caminhos entre aspas (as pastas têm acento e espaço).

## 3. Kit da oferta (uma vez por oferta)

Tudo que é da oferta e serve para todos os criativos fica em `<pasta raiz>/_kit_criativos/`:

```
_kit_criativos/
  oferta.json        paleta, lista de páginas, regiões das páginas, mockup, takes
  bgs/               os três fundos (a, b, dark) já separados em fundo limpo + objetos
  takes/             recortes dos takes de vídeo (.npy)
  AD 05/ ...         uma pasta por criativo
  PRONTOS/           os vídeos finais
```

Se `oferta.json` já existe, use-o como está e siga para os criativos. Se não existe, leia `references/oferta.md` e monte o kit: ele explica como achar as páginas na pasta, ler a identidade visual do material (paleta, tema dos textos, fundos e elementos no mesmo estilo), marcar as regiões das páginas para o zoom e escolher os takes. Avise o usuário que você vai criar essa pasta dentro da pasta da oferta.

## 4. Cada criativo, passo a passo

Crie a pasta `<kit>/<nome do criativo>/` (ex.: `AD 05`). Chame-a de `$PJ` abaixo.

### 4.1 Analisar o áudio

```bash
$PY "$S/analisar_audio.py" "<audio>" "$PJ"
```

Sai a transcrição, os blocos de fala com as pausas, o tom da voz (feminina/masculina) e a aceleração sugerida. Corrija nomes próprios na transcrição e divida o texto em três partes:

- **Gancho** = frase absurda + frase de alívio (regra 1). Na dúvida entre incluir ou não uma frase, pergunte-se: ela ainda é a pessoa reagindo ao que acabou de dizer, ou já é a história começando? Reação fica no gancho.
- **CTA** = a última frase, a que manda clicar ("vou deixar o link aqui embaixo…").
- **Corpo** = todo o resto.

Anote dois tempos do áudio olhando os blocos de fala: `gancho_fim` (um instante no silêncio logo depois da última palavra do gancho) e `cta_inicio` (um instante no silêncio logo antes da primeira palavra do CTA). Se o áudio termina com um resto de fala solto ou ruído depois do CTA, anote `audio_fim`.

**Aceleração (K).** Os anúncios aprovados ficaram entre 3,5 e 4,0 palavras por segundo (AD 05: 3,5, sem acelerar; AD 06: 3,05 no áudio, acelerado 1,32x). Decida assim:
1. Se a oferta tem o vídeo oficial do mesmo criativo (ex.: `Criativos/Oficiais/AD 05*.mp4`), use `K = duração do áudio ÷ duração do oficial` (entre 1,0 e 1,35): é o ritmo que o time já escolheu.
2. Senão, use a sugestão do script (alvo ~3,6 palavras/s).
Diga ao usuário o K usado no resumo de entrega; ele pode pedir mais rápido ou mais lento, e refazer só custa `montar_base.py` e o render.

### 4.2 Alinhar as palavras

```bash
$PY "$S/alinhar.py" "<audio>" "0.1,2.85,6.05,11.2,..." "$PJ"
```

Passe o início de cada frase (dos blocos de fala; quebre frases longas a cada ~3 s). O resultado, `alinhamento.txt`, mostra em que segundo cada palavra já foi dita. É dele que saem todos os tempos do roteiro. Rode em segundo plano e adiante o passo do avatar enquanto isso.

### 4.3 Avatar (pule se a configuração for "sem avatar")

Leia `references/avatar.md` antes de escrever o prompt: ele tem o modelo de prompt, como definir a pessoa e o cenário pela oferta, o cálculo da duração e os erros que já aconteceram. Em resumo:

- Um clipe só com gancho e CTA (ou só o gancho), `flux_3_video`, 720p, 9:16, áudio ligado, uma geração.
- Duração = palavras ÷ 2,7 + 1 s, arredondando para cima (limite do modelo: 5 a 20 s; sigla soletrada conta como 3 palavras). **Duração justa, sem folga grande:** o modelo espalha a fala pelo clipe inteiro, então clipe longo dá fala arrastada. Se o gancho sozinho tem menos de ~11 palavras, alongue o texto com uma chamada de conversa em vez de deixar sobra.
- Prompt curto, no padrão "mensagem espontânea para um amigo", com a intenção de cada frase em uma linha. Não empilhe proibições nem peça rosto neutro ou olhar fixo: é isso que dá cara de teleprompter.
- Não peça silêncio dentro do clipe.
- Para refazer só o gancho (ou só o CTA) mantendo a pessoa, use um quadro do clipe anterior como `start_image` e depois junte os dois clipes num arquivo só (ver `references/avatar.md`).
- Na leva, gere os avatares de todos os criativos ao mesmo tempo (ferramenta de lote) e varie as pessoas de verdade.

Baixe o resultado para `$PJ/avatar_raw.mp4`.

### 4.4 projeto.json

```json
{
  "nome": "AD 05",
  "kit_oferta": "..",
  "audio": "D:/.../Criativos/AD 05 - BUD (Acelerado).mp3",
  "avatar": "gancho+cta",
  "material": "folhas",
  "K": 1.0,
  "gancho_fim": 5.9,
  "cta_inicio": 52.04,
  "palavras": {"ultima_gancho": "dias", "primeira_cta": "vou"},
  "saida": "AD 05 - AVATAR + FOLHAS v1.mp4"
}
```

`avatar`: `gancho+cta`, `gancho` ou `nenhum`. `palavras` só é usado em `gancho+cta`: a última palavra do gancho e a primeira do CTA, como o avatar deve dizê-las; é por elas que o script acha onde separar as duas falas no clipe. Opcionais: `"avatar_video"` (outro arquivo no lugar de `avatar_raw.mp4`) e `"gancho_inteiro": false`. O padrão é o gancho do avatar entrar inteiro, sem cortar os silêncios dele: ele fica recortado sobre um fundo parado, e corte seco ali apareceria como um salto. Com `false` os silêncios acima de 0,35 s são cortados (só faz sentido junto com `"gancho_sobre_material": false`).

### 4.5 Montar a base

```bash
$PY "$S/montar_base.py" "$PJ"
```

Corta as pausas da voz, confere o clipe do avatar, nivela o volume das duas vozes, grava `base.mp4` e `tempo.json` e recorta o avatar do fundo nos quadros do gancho (`gancho_alpha.npy`, menos de 1 minuto, sem créditos). **Leia a saída inteira**, ela é a conferência:

- "fala completa" do avatar tem que bater palavra por palavra com o gancho e o CTA. Palavra trocada, repetida ou faltando: não siga; avise o usuário e combine a regeneração (ver `references/avatar.md`, "quando sai errado").
- "ATENCAO: a fala encosta no fim do clipe" quer dizer que a última palavra pode ter sido cortada. Avise o usuário para ouvir; se cortou, regenere com 1 s a mais.
- "ritmo do gancho" abaixo de 2,3 palavras por segundo sai marcado como LENTO: o gancho vai soar arrastado. Não siga; regenere com duração mais justa (avisando o custo).
- "RECORTE" diz quanto do quadro o avatar ocupa (o normal é 30 a 55%). Marcado como SUSPEITO, ou com "ATENCAO: nao consegui recortar", olhe os quadros do gancho na folha de conferência antes de renderizar.
- As linhas "CONFERENCIA" mostram o que ficou na base em cada parte; o começo do corpo tem que ser a primeira frase depois do alívio.

### 4.6 Escrever o roteiro das telas

Leia `references/roteiro.md` (catálogo de telas, campos e o roteiro do AD 05 comentado) e escreva `$PJ/roteiro.json`. O raciocínio:

1. Liste as frases do corpo com início e fim (do alinhamento).
2. Para cada frase ou par de frases, escolha a tela de material que melhor a ilustra e a página do produto cujo tema combina com o que é dito.
3. Junte frases curtas na tela vizinha (regra 3) e alterne os fundos `a` e `b`.
4. Amarre cada evento (texto, check, selo, zoom) ao segundo em que a palavra é dita, e dê a cada texto um estilo de animação conforme o tipo da frase, variando ao longo do vídeo (`references/roteiro.md`, seção 6).
5. Respeite a configuração de material: `folhas` usa só telas de página; `takes` usa `take` e `take_lista`; `mescla` alterna as duas famílias, começando pela que mostra melhor o produto.

Todos os tempos do roteiro são **segundos do áudio original**; o motor converte para o tempo do vídeo.

### 4.7 Conferir antes de renderizar

```bash
$PY "$S/kit.py" "$PJ" segs            # telas, durações, tempo de avatar x material
$PY "$S/kit.py" "$PJ" folha           # $PJ/folha.jpg: 5 quadros por tela
```

Olhe `folha.jpg` (leia a imagem). Confira: nada cortado nas bordas, textos legíveis, com estilos variados e sem cobrir o que importa, a página certa em cada fala, checks e zooms no lugar, nenhuma tela com menos de 3 s (o `segs` avisa), material com bem mais tempo que o avatar. Para ver um instante específico: `kit.py "$PJ" stills fora.jpg 12.4,13.1`. Corrija o roteiro e repita até ficar certo; refazer a folha leva segundos.

### 4.8 Renderizar e entregar

```bash
$PY "$S/kit.py" "$PJ" render          # ~100 s para um vídeo de 1 min
```

Gera os efeitos sonoros, renderiza em 6 processos, junta, mixa (voz + efeitos a 30%) e grava o vídeo final, `folha_final.jpg` (um quadro por segundo) e os números de conferência. Olhe a folha final, confira quadros e duração, copie o vídeo para `<kit>/PRONTOS/` e mostre ao usuário.

No resumo de entrega, diga com honestidade o que você verificou e o que não: você confere por quadros e por transcrição automática, **não ouve**. Entonação, pronúncia e "cara de teleprompter" só o usuário julga. Liste o que ele deve ouvir (palavras que a transcrição hesitou, fala que encostou no fim do clipe, cortes dentro do gancho).

## 5. A leva inteira

Para não demorar, faça em ondas em vez de um criativo por vez:

1. `analisar_audio.py` em todos os áudios; decida gancho/corpo/CTA de todos.
2. Dispare `alinhar.py` de todos em segundo plano e, ao mesmo tempo, gere os avatares de todos em lote (depois do ok de custo).
3. Enquanto isso, escreva os roteiros.
4. `montar_base.py`, folha de conferência e render, um criativo depois do outro. Não rode dois renders ao mesmo tempo: cada um já usa 6 processos, e mais que isso estoura a memória.

Planeje a variedade antes de começar: avatares diferentes de verdade entre os criativos (rosto, idade, cabelo, roupa, cenário) e páginas diferentes em destaque, para a leva não parecer o mesmo vídeo cinco vezes.

## 6. Quando algo dá errado

Leia `references/licoes.md` se um passo falhar ou o resultado sair estranho. Os mais comuns:

- **`montar_base.py` não acha a última palavra do gancho:** o avatar disse outra coisa ou o reconhecedor escreveu diferente. Veja a "fala completa" e ajuste `palavras` para como ele escreveu (ex.: "pra" virou "para").
- **Render falha com erro de memória:** rode `render 4` (menos processos).
- **Texto largo demais ou cobrindo o conteúdo:** encurte (até ~32 caracteres) ou mude o `y` dele.
- **Página errada para a fala:** troque a página no roteiro; a regra é combinar pelo tema escrito no título da página.

## Arquivos desta skill

- `scripts/kit.py`: o motor (telas, mancha, fundos, render, mixagem).
- `scripts/analisar_audio.py`, `alinhar.py`, `montar_base.py`: os passos de cada criativo.
- `scripts/recortar_avatar.py`: recorte do avatar no gancho (o `montar_base.py` já chama; rode à parte só para refazer).
- `scripts/fundos_identidade.py`, `preparar_takes.py`: preparação do kit da oferta (`fundos.py` é o modo antigo dos fundos 3D).
- `scripts/engine.py`, `motion.py`, `coral_lib.py`, `reel_example.py`, `sfx_coral.py`, `transcribe.py`, `align_voice.py`: base herdada da skill `claude-coral-reels` (movimento, transição, som, transcrição). Não edite; a única mudança em relação à original são os arquivos temporários com nome único.
- `references/roteiro.md`: catálogo das telas e como escrever o roteiro.
- `references/avatar.md`: como gerar o avatar no FLUX 3.
- `references/oferta.md`: como montar o kit de uma oferta nova.
- `references/licoes.md`: erros já cometidos e como evitá-los.
- `references/exemplo-identidade/`: `oferta.json` (com o tema dos textos), `layout.json` dos fundos, `projeto.json` e `roteiro.json` do AD 01 da Jornada de Jesus, o padrão visual aprovado (fundos na identidade do material, textos animados, mescla de folhas e takes).
- `references/exemplo/`: `oferta.json`, `caixas.json`, `projeto.json` e `roteiro.json` do AD 05 de Budismo (visual antigo: fundos 3D e pílulas simples; vale pela estrutura das telas).
