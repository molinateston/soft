---
name: soft-reel-7seg
description: >-
  Entrega o arquivo de vídeo curto pronto de postar, com a legenda longa junto: uma cena com o
  personagem real, a frase de chamada em duas linhas por cima do vídeo, o convite no meio, e toda
  a utilidade escrita na legenda (o formato em que a pessoa lê a legenda enquanto o vídeo roda).
  Cuida do enquadramento, da área segura do rosto, da trilha, da conferência do arquivo e da troca
  da mídia num post já agendado. Use quando o pedido for: "faz um reel curto", "reel
  cinematográfico", "produz o vídeo de 7 segundos", "aquele formato de ler a legenda", "headline
  por cima do vídeo", "troca a mídia do post agendado", "valida esse reel antes de subir". NÃO use
  pra: escrever o roteiro do reel, inclusive a variante falada de 7 segundos
  (soft-conteudo-reels); editar gravação crua (soft-editor-video).
---

# Reel curto de read-caption

Este formato tem um trabalho só: a cena para o scroll, a headline dá o motivo de descer, e a descrição entrega a utilidade que faz a pessoa salvar. A skill cuida do caminho inteiro, do rosto na foto ao post atualizado, preservando identidade, mídia aprovada e agendamento.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um caso fictício de nicho neutro do início ao fim: o briefing, o mosaico facial, o STOP do quadro-base, a cotação da animação, a headline com o gatilho escolhido, a descrição longa, o comando de render, **os quatro quadros de conferência com o que foi visto em cada um**, e a atualização do post sem duplicata.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola a foto, a headline e o texto e eu produzo o reel). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): vai pra produção com o que o dono colou. Se faltar um insumo que o reel não vive sem (a foto do personagem, a headline), pergunta AQUELE insumo e segue, sem voltar pro briefing inteiro.
- **Modo guiado**: só quando o dono pede explicitamente. Faz o briefing curto, uma pergunta de cada vez (a foto, o gatilho da headline, a utilidade da descrição), e monta o reel com o que o dono for dando.

A pergunta do modo é UMA por reel. As outras três partes acontecem nos passos abaixo:

- **Ensina enquanto faz:** em cada escolha estrutural (o gatilho da headline, o enquadramento do rosto, o corte da cena) escreve UMA linha do porquê. O dono lê a razão e aprende a decidir sozinho na próxima.
- **Puxa o material bruto:** quando a utilidade da descrição vier rasa ("umas dicas", "o de sempre"), não segue com o genérico. Pede o concreto que só o dono tem: uma história de um cliente real, um número que aconteceu, a frase literal que o cliente falou. Material bruto vira a descrição que faz salvar; resposta rasa vira reel raso.
- **Oferece refinar no fim:** depois de entregar, fecha com UMA linha: "quer outra headline? outro enquadramento? a descrição mais direta? me diz o que ajustar que eu refaço só essa parte."

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Entra na ação |
|---|---|
| "faz um reel desse formato", "quero um reel cinematográfico", "reel de read-caption" (do zero) | **1 · REEL NOVO** |
| "corrige o reel", "troca a headline", "a mídia ficou ruim", "sobe uma versão nova sem perder o horário" | **2 · VARIANTE E TROCA DE MÍDIA** |
| "valida esse reel", "confere se está dentro do formato antes de eu subir" | **3 · VALIDAÇÃO** |

Pedido ambíguo ("faz um reel"): pergunte UMA coisa só, se é este formato (cena curta, headline na tela, utilidade na descrição) ou um reel falado comum, porque a segunda resposta manda o pedido pra **soft-conteudo-reels**.

## Como ler cada ação

Toda ação traz o mesmo bloco fixo: **O que faz** · **Precisa de** · **Sem o insumo** · **Entrega** · **Leia primeiro** · **Profundidade** · passos numerados com **STOP**.

**O perfil do dono vem do banco do agente.** Negócio, público, oferta, voz, identidade visual, personagem e CTA: leia do perfil/brain do agente quando existir; se não existir, peça ou infira só o mínimo reversível. **Nunca embuta a identidade de um caso anterior como padrão universal:** nome, oferta, prova, cor, fonte e CTA de um caso que deu certo antes são daquele caso, não do formato.

---

## Ação 1 · REEL NOVO

**O que faz:** produz o reel inteiro, da seleção das fotos ao arquivo validado e publicado.

**Precisa de:** fotos reais do personagem, do dono · o assunto e o CTA, do dono · a identidade visual, do perfil/brain do agente · crédito de geração de imagem e de animação, autorizado pelo dono · shell com `ffmpeg`, `ffprobe`, uma fonte instalada e a ferramenta de montagem do mosaico.

**Sem o insumo:** sem fotos reais **e sem vídeo-base**, este formato não existe, porque ele vive do personagem: peça as fotos. Com vídeo-base legível em mãos, as fotos deixam de ser insumo (veja o passo 3). Sem crédito autorizado, pare na cotação e espere. Sem as dependências de mídia, veja a seção "O que fazer sem X".

**Vídeo sem fala é matéria-prima válida.** Este reel é headline sobre vídeo: a fala nunca foi requisito. Vídeo mudo, gerado por animação ou sem trilha própria **renderiza normalmente**, e o handoff declara em 1 linha que o vídeo base não tem fala e que o dono escolhe a música dentro do aplicativo na hora de postar. O render só para quando o arquivo de vídeo **não existe** ou está **ilegível** (o `ffprobe` não lê os streams): aí sim peça o arquivo de novo. Ausência de fala, de trilha ou de faixa de áudio no material nunca é motivo pra não renderizar, porque a escada de trilha da seção adiante resolve todas as três.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** `reel-<slug>-v1.mp4` (vertical, H.264 e AAC, abaixo do limite do agendador) · `quadros/quadro-01.png` a `quadro-04.png` mais `mosaico.jpg` · `descricao.md` com a descrição longa · o manifesto de validação. Tudo no diretório de saída do ambiente (`$OUTDIR`, ou a working dir).

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/caso-matrix-validado.md` (ao modelar o formato ou ao decidir safe zone, ritmo, trilha e atualização incremental; separe estrutura, ritmo e gesto visual da tese daquele caso, e nunca copie a tese, a identidade nem a prova).

**Profundidade:** `references/regua-de-titulos.md` (o cânone da headline, quando o pedido não traz uma pronta).

**Passos:**

1. **Contexto.** Recupere negócio, público, oferta, voz, identidade, personagem e CTA. Aplique a identidade do dono atual; sem ela, peça ou infira só o mínimo reversível.
2. **Formato de referência.** Recupere um formato validado e a métrica real dele. Separe estrutura, ritmo e gesto visual da tese. Nunca copie a tese, a identidade ou a prova de outro caso.
3. **Triagem do vídeo-base (checagem física, antes de qualquer decisão de parar).** Se o pedido já traz um arquivo de vídeo, rode `ffprobe` nele e cole a saída no relato. **Exit 0 torna o render obrigatório**, e você pula direto pro passo 7: com vídeo-base pronto não existe geração de imagem, não existe cotação de crédito e não existe mosaico facial. A **única** parada permitida aqui é exit diferente de 0 (arquivo inexistente ou ilegível): aí peça o arquivo de novo. Ausência de fala, de trilha, de rosto ou de personagem **nunca** é motivo pra parar, e citar a linha "Sem as fotos do personagem" com vídeo-base legível em mãos reprova a entrega. Só siga pro passo 4 quando **não** houver vídeo-base.
4. **Mosaico facial (só sem vídeo-base).** Selecione as fotos reais do personagem e monte o mosaico. Fixe traço literal, roupa, enquadramento e identidade **antes** de gerar a imagem-base. Rosto que muda entre a foto e o vídeo queima a peça inteira.
5. **STOP: mostre o quadro-base e espere a aprovação antes de animar.** Animar um quadro errado gasta crédito à toa.
6. **STOP: cote a animação antes de consumir crédito.** Informe o valor e espere a autorização. Uma geração por autorização, e preserve o MP4-base recebido, sempre.
7. **Headline e descrição.** **Headline dada pelo dono é literal.** Se o pedido traz a headline escrita, ela entra palavra por palavra, sem reescrita e sem corte. Quebrar em duas caixas é permitido, mudar palavra não. Se não couber, reduza o corpo da fonte e declare em 1 linha; nunca resuma nem reescreva a headline do dono. Checagem verificável antes de renderizar: cole a headline do pedido e a que foi pro manifesto uma embaixo da outra e confirme que são a mesma string; qualquer diferença reprova o render. Só quando o pedido NÃO traz a headline pronta é que você escreve uma, aqui mesmo, pela `references/regua-de-titulos.md` que esta skill carrega, que é o cânone da headline por família de gatilho. Pra um banco de headline avulso, fora deste reel, a `soft-conteudo-headlines` é a casa dedicada. Depois rode o **gate anti-IA inline** desta skill na headline e na descrição. Na tela vão só a HEADLINE curta e a microchamada; corpo, explicação e lista ficam na descrição grande, útil e salvável. Escreva na voz e nos limites comerciais do dono atual. Não invente prova, número, promessa nem dado pessoal.
8. **Render.** Renderize o overlay de modo determinístico com `scripts/render_reel.py`, aplicando tipografia, cor e composição da identidade atual. Rosto dentro da safe zone, headline dividida em duas caixas, microchamada só na segunda metade.
9. **Trilha.** Use música em alta na plataforma quando o fluxo de publicação der acesso a ela. Sem esse acesso, veja "A trilha quando não há música disponível".
10. **Export e validação.** Exporte vertical 9:16, em H.264 e AAC, abaixo do limite do agendador, **com altura maior ou igual à do arquivo-base: nunca exporte abaixo da resolução da fonte**. Checagem verificável: cole a dimensão da fonte e a da saída lado a lado; saída menor que a fonte reprova o export. Rode `scripts/validate_reel.py` e **abra os quatro quadros do arquivo final com o olho** (a seção "Os quatro quadros de conferência" diz o que procurar em cada um).
11. **STOP: mostre o mosaico dos quatro quadros e pergunte "pode subir?"** antes de publicar ou agendar.

---

## Ação 2 · VARIANTE E TROCA DE MÍDIA

**O que faz:** gera uma versão corrigida e atualiza o post que já está agendado, sem criar um post novo.

**Precisa de:** o MP4-base preservado · a variante anterior · o identificador do post agendado · o que precisa mudar, do dono.

**Sem o insumo:** sem o MP4-base preservado, a correção obriga a regerar a animação, o que custa crédito de novo: cote e espere a autorização antes. Sem acesso ao agendador, entregue o arquivo novo e diga em 1 linha o que o dono faz na mão (trocar a mídia do post existente, nunca criar outro).

**Entrega:** `reel-<slug>-v2.mp4` em diante, numerado, mais a prova da atualização: mesmo identificador, mesmo horário, mesmo texto, mesmo estado e nenhuma duplicata.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Passos:**

1. **Toda correção gera variante incremental.** Nunca sobrescreva imagem-base, MP4-base, copy aprovada nem variante aprovada. O que deu certo antes fica no disco.
2. Aplique a correção só no ponto que falhou. Headline errada refaz a headline e re-renderiza o overlay; não regera a animação.
3. Valide a variante nova pelo mesmo caminho da Ação 1, passo 9.
4. Suba a variante e **atualize o mesmo post trocando somente a mídia**.
5. **Leia o agendamento por fora** e prove: mesmo identificador, mesmo horário, mesmo texto, mesmo estado, nenhuma duplicata. Se a edição não for segura, preserve o post anterior e diga ao dono o que aconteceu.

---

## Ação 3 · VALIDAÇÃO

**O que faz:** audita um arquivo pronto contra o contrato do formato, sem produzir nada.

**Precisa de:** o arquivo de vídeo · o manifesto com os parâmetros esperados (tempo da microchamada, posição da safe zone, duração, limite de tamanho).

**Sem o insumo:** sem manifesto, valide o que é absoluto (dimensão vertical, codecs, duração, tamanho, presença de áudio, os quatro quadros) e declare em 1 linha que os parâmetros de safe zone e de tempo da microchamada ficaram por conferir porque não foram declarados.

**Entrega:** o veredito por critério, mais os quatro quadros e o mosaico.

**Passos:** roda `scripts/validate_reel.py` → abre os quatro quadros → devolve a tabela de gates com o veredito.

---

## Os gates do formato

- Identidade do dono atual confirmada ou recuperada. Nenhum nome, oferta, prova, cor, fonte ou CTA herdado de outro caso por padrão.
- Quadro-base aprovado antes da animação.
- Gasto autorizado antes do crédito.
- Cabeça inteira no quadro, com folga mensurável entre o cabelo e a caixa da headline.
- Microchamada ausente antes do tempo definido e presente depois.
- Read-caption sem corpo explicativo na tela: só a headline e a microchamada.
- Headline dada pelo dono entrou literal, conferida string contra string com a do pedido.
- Saída vertical 9:16 com altura maior ou igual à da fonte, com as duas dimensões coladas lado a lado.
- Gate anti-IA rodado na headline e na descrição, com veredito de aprovação.
- Quatro quadros, áudio, dimensão, duração, codecs e tamanho conferidos no arquivo final.
- Atualização externa sem post novo.

## Gate anti-IA inline (roda aqui, sem depender de outra skill)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.

**Marcador no texto de tela reprova o render (checagem mecânica, roda antes do STOP).** Antes do STOP, rode `grep -i 'A CONFIRMAR'` no manifesto de render e confira campo a campo o que vai virar pixel: headline, microchamada e qualquer legenda. Cole a saída do grep no relatório. Marcador em headline ou microchamada reprova o render e manda refazer o vídeo; o que falta confirmar sai da tela e vira pergunta ao dono, nunca vira string queimada no quadro.

Antes de renderizar, passe a headline e a descrição por estes checks. Uma falha refaz o ponto, não a peça inteira.

| Check | Reprova quando |
|---|---|
| Travessão longo | existe qualquer travessão longo no texto. Troque por ponto ou hífen comum |
| Família do verbo-freio banido | aparece o verbo de emperrar (a forma verbal, o particípio ou a forma com o prefixo de negação) fora de citação literal do dono. Substitua por emperrar, empacar, parar, freio ou amarra |
| Frase-emoldura | "a verdade é que", "o segredo é", "aqui vai o que você precisa saber", anúncio do que vai fazer |
| Verbo-clichê | revoluciona, transforma, potencializa, alavanca, eleva, desbloqueia |
| Tricolon performático | três itens paralelos só pelo ritmo, sem os três carregarem tese |
| Contraste em série | a construção de negar e afirmar aparece mais de uma vez na mesma peça |
| Conectivo formal | outrossim, ademais, vale ressaltar, em suma, portanto no meio de fala |
| Atribuição vaga | "especialistas apontam", "estudos mostram" sem fonte nomeada |
| Abstração sem imagem | a frase não vira cena na cabeça de quem lê frio |
| Prova sem lastro | número, caso ou promessa que não está no material do dono. Sem fonte, marca `[A CONFIRMAR]` |
| **VEREDITO** | é o pior item acima. Só tudo aprovado renderiza |

**Cinto extra:** com shell, rode `python3 scripts/lint_copy.py <arquivo>`, que pega o travessão longo e o verbo-freio banido de uma vez. Sem shell, faça a varredura no olho nos dois pontos que mais escapam, que são exatamente esses dois. Se a **soft-critico-copy** estiver instalada, ela é a auditoria mais completa e vale rodar por cima; o gate inline continua sendo o piso, porque não depende de nada instalado.

## Os quatro quadros de conferência (o que procurar em cada um)

O `validate_reel.py` extrai quatro quadros e monta o mosaico. Abrir e olhar é obrigatório: o script prova número, não prova imagem.

| Quadro | Momento | O que você procura |
|---|---|---|
| **01** | primeiro décimo | a headline já está legível · as duas caixas cabem sem cortar palavra · a microchamada está AUSENTE · o rosto está inteiro no quadro |
| **02** | antes do tempo da microchamada | a microchamada continua ausente · a folga entre o cabelo e a caixa é visível · a cena não escureceu a ponto de a headline sumir |
| **03** | logo depois do tempo da microchamada | a microchamada apareceu · ela não colidiu com a headline nem com o rosto · o texto dela está legível |
| **04** | último décimo | tudo continua no lugar no fim · a cena não estourou de brilho · nenhuma palavra órfã na segunda caixa |

### A área segura se MEDE, não se olha

Descrição em prosa nunca substitui medição. "As duas caixas cabem sem cortar palavra" é uma frase que o motor escreve porque espera que seja verdade, e o pixel costuma desmentir. Depois de gerar os quadros, rode a medição e cole a saída:

```
python3 -c "from PIL import Image; import numpy as np, sys; a=np.array(Image.open(sys.argv[1]).convert('RGB')); w=a.shape[1]; b=(a>200).all(axis=2); c=np.where(b.sum(axis=0)>0)[0]; print('margem esq', int(c.min()), 'margem dir', int(w-1-c.max()))" quadros/quadro-01.png
```

**Margem menor que 40 px em qualquer lado reprova o render** e manda refazer com a caixa mais estreita, porque a área segura do player vertical come as bordas: parte da primeira e da última letra some no aparelho real, e a placa colada no canto lê como erro de renderização. Uma faixa que vai da coluna 0 à última coluna da tela é placa encostada nos dois cantos, não headline centralizada. **A frase de inspeção só entra no arquivo de validação DEPOIS da linha de margem colada**, e um veredito de aprovado com margem abaixo do piso é relato que o arquivo desmente. Checagem colada: `margem esquerda: N px · margem direita: N px · piso: 40 px · veredito: passa ou refaz`.

**Liste ao dono o que você viu em cada quadro**, em 4 a 6 linhas. **Sem leitor de imagem**, declare em 1 linha: "não tenho leitor de imagem aqui, o validador aprovou dimensão, duração, codecs, tamanho, a folga do rosto em pixels e o tempo da microchamada; a conferência visual dos quatro quadros fica com você no mosaico antes de subir".

## A descrição é PEÇA PÚBLICA e passa pelos mesmos crivos do pixel

A legenda do reel é lida por todo mundo que assiste, então ela não é bastidor nem handoff: é copy publicada, e reprova pelas mesmas regras. Antes de fechar, rode os três crivos sobre ela:

1. **Marcador nenhum no miolo.** `grep -n 'A CONFIRMAR' descricao.md` e, pra cada linha devolvida, apague o marcador e releia a frase. O teste não é "ficou agramatical": é "a frase existiria sem esse dado?". Uma frase que perde o ponto quando o número sai ("voltou a subir escada sem dor [A CONFIRMAR: prazo]") tem duas saídas e nenhuma terceira: reescrever na versão que dispensa o dado, ou perguntar ao dono antes de escrever. O furo vai pro handoff.
2. **Nome próprio com origem classificada.** Liste os nomes de pessoa da legenda no formato `<nome> | origem: <arquivo> | autorização: <linha> ou anonimizado`. Sem a linha de autorização registrada, o nome SAI e a forma sem identificação toma o lugar dele. Rode os 3 passos do crivo de consentimento (`references/08-consentimento.md`) e cole a saída dos dois greps.
3. **Ressalva do nicho, quando a legenda toca corpo ou saúde.** Se a legenda cita resultado de saúde, dor, articulação, emagrecimento ou corpo, ela fecha com a linha de avaliação individual, numa linha própria e fora do gancho. Ressalva dentro do gancho o desativa; ressalva no relato de processo não protege ninguém, porque não é ela que o público lê.

Checagem colada na entrega: `marcadores no miolo: 0 · nomes sem autorização: 0 · ressalva do nicho: linha N ou não se aplica`.

## A trilha quando não há música disponível

Ordem de preferência, e o que fazer em cada degrau:

1. **Música em alta na plataforma**, quando o fluxo de publicação der acesso ao catálogo dela. É a primeira escolha, porque a plataforma distribui melhor o que usa o catálogo dela.
2. **Sem esse acesso:** apresente ao dono uma alternativa de trilha comercial gratuita e **espere a escolha dele** antes de incorporar. Nunca decida a trilha sozinho: música é identidade, e a errada estraga uma peça certa.
3. **Sem nenhuma trilha disponível:** exporte com a **faixa de áudio original da animação**, se ela tiver uma. O arquivo precisa sair com faixa de áudio válida, porque o validador exige e alguns agendadores recusam vídeo mudo.
4. **Sem áudio nenhum no material:** exporte com uma **faixa silenciosa** na mesma duração do vídeo (o `ffmpeg` gera uma faixa de silêncio e a multiplexa junto), e **diga ao dono em 1 linha** que o reel está sem trilha e que ele escolhe a música dentro do aplicativo na hora de postar. Nunca entregue arquivo sem faixa de áudio.

## O que fazer sem X

| Falta | O que a skill faz |
|---|---|
| **Sem `ffmpeg` ou `ffprobe`** | O render e a validação não rodam. Entrega a headline aprovada, a descrição, os parâmetros exatos do overlay (as duas linhas, a posição da caixa, o tempo da microchamada, a duração) e diz em 1 linha que basta rodar o script num ambiente com as dependências. Não finge que renderizou. |
| **Sem a ferramenta de montagem do mosaico** | Os quatro quadros saem individuais, sem o mosaico. Confira os quatro um por um e diga que o mosaico ficou de fora. |
| **Sem a fonte declarada instalada** | O `render_reel.py` recebe o caminho da fonte por argumento. Aponte pra uma fonte pesada que exista na máquina; sem nenhuma, avise o dono, porque fonte errada descaracteriza a peça e o certo é parar antes de renderizar torto. |
| **Sem crédito de animação autorizado** | Para na cotação. Não gera. |
| **Sem as fotos do personagem E sem vídeo-base** | Só nessa combinação o formato não existe. Peça as fotos, não substitua por banco de imagem. **Com vídeo-base legível (`ffprobe` exit 0), esta linha não se aplica:** o render é obrigatório e as fotos deixam de ser insumo, porque a imagem-base já veio pronta. |
| **Sem acesso ao agendador** | Entrega o arquivo e diz em 1 linha o que o dono faz na mão: trocar a mídia do post existente, nunca criar outro. |
| **Sem trilha** | Segue a escada da seção acima, e nunca entrega arquivo sem faixa de áudio. |
| **Vídeo base sem fala** | Renderiza igual: a fala não é insumo deste formato. Declara no handoff, em 1 linha, que o vídeo base não tem fala. Só para se o arquivo de vídeo não existir ou o `ffprobe` não conseguir ler os streams dele. |

## O que esta skill NÃO faz

Cada rota abaixo é sugestão. Se a skill indicada não estiver instalada, faço aqui em modo reduzido e digo em 1 linha o que ficou de fora.

- O **roteiro falado** de um reel comum, com fala e cortes → **soft-conteudo-reels**.
- A **edição de vídeo** longo, corte, legenda, b-roll → **soft-editor-video**.
- A **headline** fora deste formato → **soft-conteudo-headlines**.
- A **auditoria completa de copy** → **soft-critico-copy**.
- **Arte estática**, carrossel, capa, banner → **soft-designer**.
- **Campanha, verba e métrica** → **soft-trafego-meta**.

## Recursos da pasta

- `references/EXEMPLO-FIM-A-FIM.md`: o caso fictício de ponta a ponta, leia antes de começar.
- `references/caso-matrix-validado.md`: o caso validado que originou o formato, com o aprendizado reutilizável, a sequência que funcionou e os parâmetros que são daquele caso e não viram padrão universal.
- `references/regua-de-titulos.md`: o cânone da headline por família de gatilho, quando o pedido não traz uma pronta.
- `scripts/render_reel.py`: renderiza o overlay a partir do MP4-base (rode com a opção de ajuda pra ver os argumentos).
- `scripts/validate_reel.py`: valida o arquivo final e produz os quatro quadros mais o mosaico.
- `scripts/lint_copy.py`: o anti-IA em código, cinto extra do gate inline.
- `shared-references/filtro-anti-ia/`: a mesma régua anti-IA por escrito, pro motor que não tem shell pra rodar o lint. `padroes-banidos.md` lista o que reprova; `falsos-positivos.md` roda antes de reprovar qualquer trecho.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Sem sandbox (a régua escrita, quando o lint não roda).** Motor sem shell não executa `scripts/lint_copy.py`, e isso não dispensa o anti-IA: aplique a régua no olho por `shared-references/filtro-anti-ia/padroes-banidos.md`, padrão por padrão, e passe cada reprovação por `shared-references/filtro-anti-ia/falsos-positivos.md` antes de mandar o trecho de volta pro passo de escrita, porque prosa autoral do dono cai no mesmo crivo e some se ninguém conferir. A entrega sai do mesmo jeito, no melhor que esse motor alcança, e o relato fecha com uma linha dizendo que a conferência anti-IA foi no olho, sem código: `anti-IA: conferido no olho pela régua escrita (sem shell nesta rodada)`. Calar o que ficou de fora reprova a entrega; declarar em uma linha reprova nada.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
