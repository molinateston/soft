---
name: soft-edicao-yap
description: >-
  Edita a gravação vertical de quem fala pra câmera no Yap, estilo celular: o reel com cara de editado no próprio celular, legenda de uma palavra por vez no jeito nativo do Instagram, prints crus acima da cabeça, cortes secos, nenhuma pausa e no máximo 90 s. Entrega o MP4 1080x1920 e o relatório da edição. Use quando o pedido for: "edita esse vídeo no estilo celular", "edita esse yap", "corta as pausas e põe legenda palavra por palavra", "põe meus prints em cima da cabeça", "quero com cara de editado no celular", "reel cru, sem cara de agência". NÃO use pra: o visual desenhado com serifa e acabamento de revista (soft-edicao-yap2); o YAP de websérie com título no quadro 0, uma versão por gancho e briefing de edição (soft-edicao-yap3); escrever o roteiro ou o gancho (soft-conteudo-reels, soft-conteudo-headlines); edição com b-roll e cartões (soft-editor-video). Leia e siga o fluxo inteiro do SKILL.md.
---

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
