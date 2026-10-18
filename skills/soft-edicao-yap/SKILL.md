---
name: soft-edicao-yap
description: >-
  Edita a gravação vertical de quem fala pra câmera no Yap, estilo celular: o reel com cara de editado no próprio celular, legenda de uma palavra por vez no jeito nativo do Instagram, prints crus acima da cabeça, cortes secos, nenhuma pausa e no máximo 90 s. Entrega o MP4 1080x1920 e o relatório da edição. Use quando o pedido for: "edita esse vídeo no estilo celular", "edita esse yap", "corta as pausas e põe legenda palavra por palavra", "põe meus prints em cima da cabeça", "quero com cara de editado no celular", "reel cru, sem cara de agência". NÃO use pra: o visual desenhado com serifa e acabamento de revista (soft-edicao-yap2); o YAP de websérie com título no quadro 0, uma versão por gancho e briefing de edição (soft-edicao-yap3); escrever o roteiro ou o gancho (soft-conteudo-reels, soft-conteudo-headlines); edição com b-roll e cartões (soft-editor-video). Leia e siga o fluxo inteiro do SKILL.md.
---

## Preservar a aparência de cor do bruto (dono, 15/10/2026 20:51)

Ordem explícita: “Corrige ambos então, a skill não pode mexer na cor ok?” Vale para edição completa, ajuste e exportação. Preserve a aparência de cor da gravação original. Sem pedido explícito do dono, não altere brilho, exposição, contraste, saturação ou balanço de branco; não aplique LUT, filtro de cor, embelezamento, retoque de pele nem correção automática. A identidade e a cor de acento das camadas gráficas não autorizam alterar a imagem filmada. Molde aprovado ou vídeo já editado não substitui o bruto como referência de cor.

Conversão técnica de HDR, HLG ou Dolby Vision para o formato de entrega não autoriza mudar a aparência. Antes do lote, inspecione metadados e estabeleça uma reprodução confiável do original, com gerenciamento de cor compatível com o material. Registre arquivo, player ou fluxo de reprodução, espaço de cor e condições conhecidas de comparação. Não trate uma extração crua de valores HLG ou uma prévia sem gerenciamento de cor como referência visual suficiente.

Confira a cadeia inteira, incluindo intermediários, composição e exportação. Os pixels convertidos e as tags de primárias, transferência, matriz e faixa precisam corresponder ao sinal real; trocar apenas tags não corrige a imagem. Nenhum preset de tone mapping, valor de luminância ou escurecimento arbitrário serve como solução universal. A mera ausência de filtro também não prova preservação da aparência.

Antes de entregar, compare o MP4 final decodificado com a reprodução confiável do bruto nos mesmos instantes de origem, mapeados pelos cortes, incluindo início, meio e fim dos trechos usados e mudanças de iluminação. Examine rosto, parede e roupa nas áreas sem sobreposição; confira luminosidade, contraste, cor da pele e saturação. Salve comparações e registre tempos de origem/saída, transformação aplicada, tags e limites da inspeção no relatório. Se a imagem ficar mais clara, lavada, escura ou com outra cor, corrija a cadeia e repita a comparação antes de entregar. Sem referência confiável, declare a pendência e não afirme correspondência visual comprovada. Não prometa identidade matemática entre espaços de cor distintos.

## Contrato de reprodução do molde (15/10/2026)

Antes de escolher fonte ou montar texto, leia [o contrato tipográfico](references/contrato-tipografico.md) e execute `python3 scripts/reproduzir_molde.py <pasta do molde>` (ou com `YAP_MOLDES_DIR`). Um perfil aprovado da mesma série tem prioridade sobre medidas genéricas desta skill. Para ajuste de texto, congele pessoa, ângulo, escala, enquadramento, cortes e áudio. Entregue amostra comparada com o molde antes do lote.



# Yap, estilo celular: o reel que parece editado no próprio celular

Esta skill pega a gravação vertical de uma pessoa falando pra câmera e devolve o reel pronto com cara de feito no editor do Instagram pelo próprio dono: legenda de uma palavra por vez, prints reais acima da cabeça, cortes secos e nenhuma pausa. Ela entra DEPOIS da gravação: aqui é edição, nunca escrita. É marca-neutra: a identidade (cor de acento, fonte, nome, usuário, avatar, seguidores) vem do `perfil.json` do dono, e cada cliente roda com a própria.

**A regra que manda em tudo:** quem assiste precisa sentir que o dono editou no celular dele. Nunca pode parecer agência nem IA. Na dúvida, faça menos, mais cru, menor. Motion polido aqui é defeito.

**Origem e honestidade.** O estilo foi descrito a partir de um pacote de edição de terceiro e de reels de exemplo desse pacote (amostra pequena, sem métrica de retenção). Nada aqui foi medido em desempenho: o que a skill diz sobre "o que prende" é hipótese a confirmar nas métricas do próprio dono.

## A condução: a skill te ajuda a fazer, não só te entrega

Pergunte o modo uma vez, na primeira mensagem: "Eu já edito no modo direto (você manda o vídeo e eu monto). Se preferir ser guiado passo a passo, te pergunto uma coisa de cada vez." No silêncio, é o modo direto: pergunte só o que a edição não vive sem. No modo guiado, uma pergunta por vez, dizendo o que precisa, por quê, onde conseguir e o que vem depois:

1. **O vídeo:** o arquivo da gravação. É o único bloqueio duro: sem ele não há edição. Depois disso vem a transcrição.
2. **O perfil (uma vez só):** se não houver `perfil.json` na pasta de trabalho, peça numa mensagem só os campos de `references/perfil.md` e salve. Sem identidade declarada, só branco, sem cor de acento, com a fonte livre da skill.
3. **Os prints:** a pasta onde o dono guarda os prints do celular (perfil, insights, curtidas, comentários, directs). Sem print real para uma afirmação, peça o print exato daquela tela; nunca invente um.
4. **O limite:** a duração máxima (padrão 90 s) e o que não pode sair do corte.

Ensine enquanto faz (uma linha do porquê de cada escolha) e feche oferecendo o ajuste ("quer o corte mais seco, o texto menor, outra palavra em destaque?").

## Antes de editar: ambiente pronto, instalado por você

Quem prepara a máquina é você, o agente. O dono não instala nada na mão. Esta skill precisa de node 22, ffmpeg, HyperFrames, GSAP, o Chrome do render e a transcrição local. Nos comandos, `<S>` é a pasta `scripts` desta skill e `<pasta>` é a pasta de trabalho da edição. No Windows, troque `python3` por `python`.

1. **Instale:** `python3 <S>/instalar_ambiente.py --perfil hyperframes --pasta <pasta>`. Ele confere o sistema e instala sozinho o que faltar, dentro da pasta sempre que possível. Na primeira vez leva de 3 a 5 minutos; rodar de novo é seguro. Saída 0, ambiente pronto. Saída 3, falta algo que só o dono faz: passe a ele, em uma frase, o comando exato que o instalador imprimiu e espere. Saída 1, 2 ou 4, leia o motivo, rode de novo uma vez e, se repetir, mostre ao dono o passo e o log.
2. **Prove:** `python3 <S>/prova_render.py --perfil hyperframes --pasta <pasta> --audio <vídeo do dono>`. Só a linha `PROVA DE RENDER: OK` libera a edição. Reprovou, diga ao dono qual item falhou e não edite.
3. **Carregue o ambiente em todo comando:** Linux e Mac `. <pasta>/.ambiente/ativar.sh && <comando>`; Windows `call <pasta>\.ambiente\ativar.bat && <comando>`.
4. **Regra dura:** nunca entregue uma edição simplificada por falta de ferramenta. Ou o ambiente prova que renderiza, ou você para e diz o que falta. Cole a linha da prova no relatório.

O passo a passo completo, com a tabela de estados e as saídas, está em `references/ambiente.md`.

## Regras de partida (o dono pode mudar qualquer uma; registre a mudança no relatório)

1. **Nada de pausa nem respiro.** Tudo abaixo de -30 dB por 0,15 s ou mais sai (`cortar.mjs`).
2. **Todo take repetido, começo em falso e frase dita duas vezes sai.** Fica o último take, o mais limpo.
3. **No máximo 90 s**, salvo pedido do dono. Diga no relatório o que saiu.
4. **Cortes J/L ligados por padrão** (`--jl 6` mais suave, `--no-jl` desliga).
5. **Uma cor de acento só, a do perfil**, e só num destaque de até 3 palavras de vez em quando ("agente de IA"). Sem identidade, tudo branco.
6. **Não publique, não envie, não use serviço pago sem pedido explícito.** Print só com origem conhecida e permissão do dono para expor. Nunca invente número, logo, capa nem print.

## O visual (inegociável)

| Elemento | Regra |
|---|---|
| Prints | Prints reais da pasta do dono (topo do perfil, insights, curtidas, comentários, salvamentos, compartilhamentos, visualizações, directs, posts). Recorte cru: **cantos retos, sem borda, sem sombra, sem moldura, sem cartão arredondado**. Acima da cabeça. |
| Texto acima da cabeça | Fonte do título, branca e **pequena**: títulos de 48 a 70 px (partida 62), rótulos e itens de lista de 40 a 48 px (partida 48) em 1080 de largura. Esses px valem para a **altura da letra**, não para o px nominal da fonte: o template fixa `font-size-adjust: 0.62`, então qualquer fonte do título sai com a letra da altura do molde (título com uns 76 px de altura medida, item com 44). Não aumente o px para compensar fonte de letra baixa. **Alinhado à esquerda com a borda esquerda do print; sem print, borda em 160 px.** Título que não cabe numa linha: primeiro a sigla de uso comum, depois px menor (até 48). Cor de acento só num destaque de até 3 palavras, de vez em quando (`.y`). Sem serifa grossa (`.sans`) só em rótulos curtos como "Ruim / Bom / Viral". |
| Sombra | Só quando a parede atrás é clara (`.sh`). Nunca caixa nem tarja atrás do texto. |
| Movimento | **Nenhum.** Tudo aparece e some num corte seco (`show()` e `hide()`). Sem fade, sem deslizar, sem escala, sem pulo. |
| Emoji | Emoji de verdade no template (✅ ❌ ❤️ 👇 🚨 e outros); o `montar-index.mjs` troca pela arte livre do Noto Emoji. Nunca desenhe ícone. |
| Legenda | **Uma palavra por vez**, 54 px de altura de letra na fonte do título (o mesmo `font-size-adjust`, uns 47 px de altura medida), branca com contorno preto grosso. Centrada no peito, logo abaixo do queixo (`capTop` no `reel.json`). Corte seco de palavra para palavra. |
| Título que fica | Um título do assunto pode ficar na tela por bastante tempo, com prints trocando acima dele. |
| Listas | Emoji e palavra (✅ Legenda / ❌ Título), item por item, na palavra falada. |
| Imitação de tela | Evite. Use print real. Só desenhe uma tela se não houver print E o dono pedir, com os dados do `perfil.json`. |

`references/exemplo-neutro.jpg` mostra o visual num vídeo de teste neutro (barras de cor, print fictício sem dado real): olhe antes de compor.

## Fluxo (rode na pasta de trabalho)

1. **Projeto e transcrição:** `node <S>/novo-reel.mjs "<video>" <slug>` cria `video-projects/<slug>/` com `assets/raw.mp4`, `raw.json`, `words.txt`, as fontes, o `reel.json` (identidade vinda do perfil) e o template. Sem transcrição instalada, ele monta o projeto e diz o que instalar.
2. **Enquadramento:** folha de contato do `raw.mp4` (`ffmpeg -i assets/raw.mp4 -vf fps=1/4,scale=180:-1,tile=12x1 -frames:v 1 enquadramento.jpg`) para achar o topo da cabeça e o queixo. As sobreposições vivem entre y 100 e o topo da cabeça; a legenda fica abaixo do queixo (`capTop` no `reel.json`).
3. **Escolha do corte:** leia `words.txt` e escreva `assets/keeps.json` (`{"fps":30,"keeps":[{"from":0,"to":12.4,"why":"take limpo do começo"}]}`).
4. **Corte:** dentro de `assets/`: `node <S>/cortar.mjs` gera `clean.mp4` e `edit-decisions.json`.
5. **Conferência do corte:** transcreva o `clean.mp4` de novo (`python <S>/transcrever.py clean.mp4 transcript.json`, com o python do faster-whisper) e leia do começo ao fim. **A transcrição esconde repetição e erra tempo de palavra:** procure frase dobrada, palavra comida e verbo faltando. Achou, volte ao passo 3. Palavra ouvida errado vai em `assets/caption-fixes.json`: `{"errada": "certa"}` troca toda ocorrência; chave com espaço troca o trecho (`{"Digita a gente": "Digita agente"}`); `{"_em": [{"em": 59.5, "para": "dou"}, {"em": 120.1, "juntar": 2, "para": "agente"}]}` troca só a palavra mais próxima daquele tempo (até 0,3 s), e `juntar` funde com as seguintes. Depois: `ffmpeg -i clean.mp4 -af silencedetect=noise=-30dB:d=0.25 -f null -` sem nenhum `silence_start`.
6. **Prints:** indexe a pasta de prints uma vez (e quando houver prints novos): `node <S>/indexar-prints.mjs` (usa `pasta_prints` do perfil, ou `--pasta <dir>`). Busque: `node <S>/achar-prints.mjs "<termos>" [--since 2026-01-01] [--min-w 600]`. SEMPRE abra e olhe o candidato antes de usar; recorte com ffmpeg para `assets/prints/` e anote a origem de cada um em `assets/prints/SOURCES.md`. Sem tesseract, o índice sai sem texto e a busca é por nome e data: liste a pasta, olhe os prováveis ou peça o print ao dono.
7. **Composição:** edite `src/index.template.html` (sobreposições e tempos com `show` e `hide`). Tempos na palavra falada: `node <S>/ancoras.mjs "frase" ...` na raiz do projeto. Só corte seco.
8. **Texto da tela pela régua da casa** (abaixo).
9. **Montagem e conferência:** `node <S>/montar-index.mjs`, depois `npx hyperframes lint`, depois o rascunho `node <S>/renderizar.mjs --rascunho`. Tire o mosaico com `node <S>/mosaico.mjs renders/draft.mp4` (um quadro em cada troca de sobreposição) e OLHE: rosto nunca coberto, texto legível, print inteiro. Por fim `node <S>/renderizar.mjs` gera `renders/<slug>-final.mp4`.
10. **Entrega** (em português, curta): caminho do arquivo final, o que foi cortado, prints usados, o que ficou incerto. Nunca publique nem envie nada.

O `renderizar.mjs` existe por um defeito medido: renderizado direto em 1080 px, o vídeo da câmera sai com uma faixa preta de 8 px na borda direita. O template usa janela de 1096 px, o render extrai os quadros em png e o script recorta de volta para 1080x1920.

## Texto da tela pela régua da casa

Título, rótulo e item de lista repetem o que foi falado, sem resumo e sem reescrita. A única troca permitida é a sigla de uso comum no lugar do nome por extenso (inteligência artificial vira IA), para o título caber numa linha: "O que é um agente de inteligência artificial?" vira "O que é um agente de IA?", com "agente de IA" em destaque.

1. Junte todo texto que vai queimado na tela em `textos-tela.md` (na raiz do projeto) e rode `python3 <S>/lint_copy.py textos-tela.md` até sair 0. Aviso de lint em fala literal não muda a fala: só anota no relatório.
2. Ponha os títulos, um por linha, em `conferencia/titulos.txt` e rode `python3 <S>/checar_titulos.py --peca textos-tela.md --titulos conferencia/titulos.txt --insumos assets > conferencia/checagem-titulos.md`. Preencha cada `<preencher>` do bloco. Linha que reprovaria por causa de fala literal vira nota ao dono, nunca reescrita.

## Conferências antes de entregar

- `ffprobe`: 1080x1920, 30 fps, áudio presente, duração até 90 s (ou a combinada). `ffmpeg -v error -i <final> -f null -` sem saída (o `renderizar.mjs` já imprime).
- Nenhum `silence_start` no `clean.mp4` com `silencedetect=noise=-30dB:d=0.25`.
- Mosaico olhado: rosto livre, legenda abaixo do queixo, texto alinhado à borda do print, só a cor de acento do perfil, nada cortado na borda, borda direita sem faixa preta.
- Cada print tem linha em `SOURCES.md`, e a permissão do dono para expor está anotada.
- Nenhuma animação: todo elemento entra e sai num corte seco.

## O que é "pronto"

O MP4 final em `renders/<slug>-final.mp4` passou nas conferências acima, o `textos-tela.md` saiu com lint 0, o `conferencia/checagem-titulos.md` está preenchido sem `<preencher>`, e o relatório no chat diz o caminho, a duração, o que foi cortado, os prints usados, o que ficou incerto e o que depende do dono.

## O que esta skill NÃO faz

- O visual desenhado com serifa e acabamento de revista: **soft-edicao-yap2**.
- O YAP de websérie com título no quadro 0, uma versão por gancho e briefing de edição: **soft-edicao-yap3**.
- Escrever ou corrigir o roteiro e o gancho: **soft-conteudo-reels** e **soft-conteudo-headlines**.
- Editar gravação com b-roll, cartões e apoio gerado: **soft-editor-video**.
- Publicar, agendar ou enviar o vídeo.

## Arquivos desta skill

- `references/perfil.md`: o esquema do `perfil.json`, onde cada campo aparece e como perguntar uma vez.
- `references/exemplo-neutro.jpg`: mosaico de um render de teste neutro com o visual da skill.
- `scripts/instalar_ambiente.py`: instala sozinho o ambiente da edição e grava `ambiente.json`.
- `scripts/prova_render.py`: prova que a máquina renderiza e transcreve antes de editar.
- `references/ambiente.md`: o passo a passo do ambiente, com saídas e regra dura.
- `scripts/conferir-ambiente.mjs`: confere as dependências e diz como instalar o que faltar.
- `scripts/novo-reel.mjs`: cria o projeto, aplica a identidade do perfil e transcreve.
- `scripts/transcrever.py`: transcrição local com tempo por palavra (faster-whisper).
- `scripts/cortar.mjs`: corte sem pausa, com cortes J/L.
- `scripts/indexar-prints.mjs` e `scripts/achar-prints.mjs`: índice e busca dos prints (OCR com tesseract, em qualquer sistema).
- `scripts/ancoras.mjs`: tempo de cada frase falada no vídeo limpo.
- `scripts/montar-index.mjs`: legenda por palavra, identidade e emoji livre no `index.html`.
- `scripts/renderizar.mjs`: render sem faixa preta, recortado em 1080x1920.
- `scripts/mosaico.mjs`: um quadro por troca de sobreposição, para olhar.
- `scripts/lint_copy.py` e `scripts/checar_titulos.py`: o lint de copy e a régua de títulos da casa.
- `template/index.template.html`: o visual, com a cor de acento e a fonte como variáveis.
- `template/fonts/`: DM Serif Display (título padrão) e Inter Bold (rótulos), ambas OFL 1.1.
- `template/emoji/`: arte do Noto Emoji para os emojis mais usados.
- `LICENCAS.md`: o que vem dentro da skill e a licença de cada item.

## Nome do arquivo e lint

Nome de arquivo em minúsculas, sem acento, com hífens. Todo `.md` que a skill entregar passa por `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) antes de ser dado como pronto.


## Nova edição completa e correção de fluidez, 15/10/2026 16:02

A ordem de congelar pessoa, ângulo e áudio aplica-se a ajuste restrito de posição de texto. Uma nova edição completa autorizada volta ao bruto e decide cortes, aproximações, recuos, sons e apoios pela fala; não herda o corpo rejeitado como pronto. Preserve a identidade deste estilo e a prioridade do perfil aprovado da série.

Antes de renderizar, salve mapa por fala com: intervalo do bruto, frase literal, tentativa descartada e retomada escolhida, tempo de saída, função tipográfica, arquivo de fonte, câmera inicial/final e motivo, apoio e sua origem, som e instante de entrada. Detecte repetições, gagueiras, início abortado e autocorreção na transcrição com palavras temporizadas. Compare as tentativas no áudio; mantenha a retomada mais fluida e remova a primeira tentativa quando ela for erro. Não corte uma repetição intencional só porque a palavra repete. Transcrição automática sozinha não prova emenda fonética: confira bordas, consoantes, respiração e continuidade; documente tempos antes/depois e incerteza real. Guarde bordas de áudio suficientes para preservar a sílaba, em vez de cortar exatamente no timestamp estimado de palavra.

Varie a tipografia por função dentro dos pares comprovados do estilo: título, complemento/contraponto e legenda não são uma camada indiferenciada. Leia o perfil e referências locais; registre caminho e hash das fontes e falhe se o arquivo não carregar. Não invente fonte nem use fallback silencioso. No perfil Manuscrito (ep2), a referência local é Advercase Bold85 para título, Kalam Bold54 para complemento e Advercase72 para legenda; topo315 e folga de30px do recorte4:5. Esse perfil não substitui a identidade celular ou editorial de outro pedido.

Planeje sons nas entradas motivadas de texto, lista, demonstração, comparação ou ênfase; sincronize o som ao evento e mantenha a voz dominante. A reclamação de poucos sons exige rever oportunidades concretas, não preencher uma cota. Aproximação gradual pode sustentar uma fala que cresce em importância; recuo precisa de motivo próprio, como abrir área para lista ou iniciar etapa. Registre escala e duração, preserve continuidade em cortes de limpeza e permita permanência. Não alternar zoom in/out por índice, por intervalo fixo nem por obrigação de variar.

Escolha elementos pertinentes aos substantivos, ações e relações da fala: lista progressiva, número, contraste, seta ou demonstração real quando houver fonte. Não invente prova ou resultado. Audite cada estado no feed9:16 e recortes4:5/3:4, olhos e boca livres, título e complemento com hierarquia e sem palavra órfã. Confira duração final até90s, CTA literal completo, cortes, áudio/canais/truepeak e decodificação integral. Declare exatamente o que foi executado; não alegue escuta humana ou revisão independente inexistente. Sem música, EQ, compressor ou limiter nesta correção do dono.


## Refinamento de fluidez, elementos e câmera, 15/10/2026 17:11

O dono elogiou a direção visual da v1 e pediu outra edição completa: ainda havia erros/gaguejos e faltavam GIFs pertinentes e jogo de câmera perceptível. Elogio com ressalva não representa aprovação integral. Leia `references/revisao-fluidez-elementos-camera-2026-10-15.md` ao executar esse refinamento. Respeite a identidade própria desta skill.

ASR é mapa, não revisão fonética: pode normalizar sílabas repetidas, falsos começos e muletas. Faça varredura de todas as frases selecionadas, incluindo respirações e as emendas internas, em vez de conferir apenas os erros já apontados. Examine áudio quando a ferramenta permitir; na ausência de escuta, combine janelas curtas sobrepostas, análise acústica e margem de fonema, registre a limitação e nunca declare todos os gaguejos removidos só porque a transcrição está limpa. Compare candidatos por fluidez, preserve a retomada literal mais completa e mantenha o CTA até o último fonema. Acelerar não corrige gaguejo; esta nova tentativa do EP2 usa velocidade natural.

GIF/figurinha animada é recurso opcional, escolhido pelo substantivo, ação ou reação da fala. Demonstre que o arquivo anima no render, entra na palavra e sai com a troca do assunto. Identifique ilustração criada como ilustração; não use animação ou imagem genérica como prova de resultado. Falta de fonte real para contrato ou valor permanece limite, nunca vira print inventado.

Para câmera, a prova é o MP4 decodificado: compare começo/meio/fim de cada trajetória com a imagem fonte, além das duas bordas de cada emenda. Meça ou mostre escala/posição realmente realizadas; registre inversão, tremor, reset ou ausência de progressão. Trocar algoritmo exige repetir a prova curta do movimento. Push-in lento deve ser perceptível e terminar antes da fala para permitir permanência; recuo e punch precisam de motivo próprio. Preserve escala e posição em cortes de limpeza. Não alternar automaticamente por corte. Abertura estática permanece. Nova edição completa autoriza esses movimentos; take fixo de um ajuste de texto não congela uma edição posterior autorizada.
