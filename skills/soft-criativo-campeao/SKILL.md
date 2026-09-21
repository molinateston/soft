---
name: soft-criativo-campeao
description: >-
  Planeja e entrega um LOTE de criativos de anúncio prontos pra subir: ângulo de dor por peça, foto real da autoridade, identidade num JSON, render em lote pelo manifesto, lint anti-IA antes do pixel e prévia aprovada pelo dono. Âncora: LOTE de anúncio com ângulo por peça = aqui; peça avulsa = soft-designer. Use quando o pedido for: "faz os criativos do anúncio", "preciso de 4 artes pra campanha", "monta o lote de criativo", "qual o ângulo das peças", "replica esse processo de criativo pro meu cliente novo", "monta o playbook de criativo desse especialista", "renderiza as artes do anúncio", "por que o criativo não vende". NÃO use pra: peça visual avulsa, carrossel em PNG, capa ou banner único (soft-designer); headline isolada (soft-conteudo-headlines); reel curto (soft-reel-7seg); edição de vídeo (soft-editor-video); deck (soft-apresentacao); criar campanha, decidir verba, ler métrica ou pausar na conta (soft-trafego-meta). Leia e siga o fluxo inteiro do SKILL.md.
---

# Criativo campeão: do ângulo ao pixel

Esta skill entrega um LOTE de criativos de anúncio prontos pra subir. Ela decide o ângulo de cada peça, fixa a identidade da marca num arquivo, renderiza em lote e valida antes de virar campanha.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**O render NUNCA aplica caixa alta na headline.** `text-transform: uppercase` não entra em manchete, capa, título de slide, título de card nem em qualquer texto grande que o leitor lê como a frase da peça: ênfase é por palavra, não por tecla, e a caixa alta engorda a linha, come a área segura e derruba a leitura no celular. **O versalete (small caps) e a caixa alta continuam liberados em três lugares e só neles:** tag ou etiqueta (`.slide-label`, `.tag`), rótulo de rodapé, e cabeçalho pequeno de topo, todos até 16px. Antes de exportar, confira que nenhuma regra de caixa alta alcança a classe da manchete, e cole `regras de caixa alta no render: N · alcançando a manchete: 0`. O `checar_titulos.py --render <arquivo.html>` e o `--conferir` leem os títulos do HTML e do deck e reprovam com `título em caixa alta: <linha>`.

**Os arquivos que cada ação exige (`--exige`).** Conferência: `--conferir <pasta> --exige <lista>`. Lote de criativos: `--exige criativos-*.md`; matriz: `--exige matriz-criativos.md`; identidade: `--exige identidade.json`; pacote: as três somadas. Arquivo ausente sai com exit 1.

**Pedido que nomeia evento, turma ou data: ao menos uma peça carrega a razão de agir agora.** Rode `grep -niE 'turma|vagas|come[çc]a|aula ao vivo|[0-9]{2}/[0-9]{2}' <perfil>` e cole a saída. O que voltar entra em pelo menos uma peça, com o número literal. Cole `peças no lote: N · com razão de agir agora: N`, e zero na segunda coluna, num pedido que nomeia turma ou evento, reprova o lote.

**Todo campo preenchido do JSON de identidade carrega a origem no próprio arquivo.** Some um objeto `origens` com uma entrada por campo preenchido, no formato `"<campo>": "<arquivo>:<linha>"`. Campo com valor e sem entrada em `origens` reprova, inclusive `@` de perfil, texto de selo e CTA. Cole `campos preenchidos: N · com origem apontada: N`, iguais. `null` com pendência declarada é resultado correto e dispensa origem.

**A conclusão nasce da saída do grep, e negar a saída colada reprova.** Depois de colar a saída, escreva uma linha por ocorrência: `<arquivo:linha> | ação: <verbo> | palavra: <literal> | usada? sim/não · porque: <motivo>`. **Conclusão negativa só é válida com a saída vazia**, e o `--conferir` sai com exit 1 e `conclusão contradiz a saída do grep` quando a peça diz `palavra-chave: nenhuma` com ocorrência colada na mesma checagem.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Capacidade negada no perfil é fato, nunca lacuna a interpretar.** Antes de escolher a mecânica do CTA, rode `grep -in 'automação\|automacao\|robô\|bot' <perfil do dono>` e cole a saída literal. Linha que diz `nenhuma automação` responde `não`, e ela não é omissão nem falso positivo a contornar. Cole `mecânica exige automação? sim/não · perfil declara: <a linha literal> · mecânica adaptada: <qual>`. Negação no perfil sai como CTA sem robô, e manter a mecânica por leitura funcional, herança de outra plataforma ou hábito presumido reprova a peça.

**O universo da R3 é o das unidades produzidas, nunca o dos pilares.** As `teses distintas` saem das pautas, headlines ou frames que a peça entrega, e a contagem igual ao número de pilares do dono é resultado inválido. Cole `unidades no lote: N · linhas em teses.txt: N`, os dois iguais, e só então a matriz de pares.

**`teses.txt` é arquivo obrigatório da pasta de saída**, uma tese de até 4 palavras por linha, ao lado do `conferencia/checagem-titulos.md`. Sem ele o gate não calcula a R3 e o campo do fecho sai com a instrução do script no lugar do número, o que reprova a entrega.

Existe porque criativo que vende não vem de sorte no editor de imagem, vem de um processo repetível. O pixel bonito é a parte fácil. O que faz vender é o que vem antes do render (o ângulo, a foto certa, o lint) e o que vem depois (a prévia aprovada).

**Regra de ouro:** a peça não começa no editor de imagem, começa na DOR. E o público decide mais que o criativo.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra um lote fictício de 4 peças em nicho neutro, do briefing do dono até as artes na pasta: as perguntas que a skill fez, o `identidade.json` preenchido, o `manifesto.json` com as 4 entradas, o resultado do lint e a mensagem de prévia. Ler antes economiza uma rodada de retrabalho.

**O perfil do dono vem do banco do agente.** Onde a skill precisar de voz, avatar, dor, prova, cor, fonte ou @perfil: leia do perfil/brain do agente quando existir; se não existir, faça a entrevista curta do bloco "Sem o insumo" e siga com o que faltar marcado `[A CONFIRMAR]`. Nunca invente, nunca pare por causa disso.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md` (as quatro partes). Na prática, aqui:

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Nesta peça eu já faço no modo direto (você cola o ângulo, a oferta e a prova e eu monto o lote). Se quiser ser guiado passo a passo (te pergunto o que preciso, uma coisa de cada vez) em vez disso, é só pedir.

- **Modo direto** (default, e o que roda no silêncio): pula pra o lote com o que o dono já colou. Se faltar um insumo que o criativo não vive sem (o ângulo, ou a prova que sustenta a promessa), pergunta AQUELE insumo e segue, sem voltar pra entrevista inteira.
- **Modo guiado**: só quando o dono pede explicitamente. Faz a entrevista curta uma pergunta de cada vez (o público, o ângulo, a oferta, a prova, a identidade) antes de gerar o lote.

A pergunta do modo é UMA por lote. As outras três partes entram nas ações abaixo:

- **Ensina enquanto faz:** ao escolher o ângulo de cada peça do lote, escreve UMA linha do porquê ("esse ângulo ataca a objeção de preço porque é aí que o teu público empaca; um ângulo de resultado atrai mais clique, mas qualifica menos"), pra o dono decidir sozinho na próxima.
- **Puxa o material bruto:** quando a dor ou a prova vier rasa ("meus clientes querem resultado"), não segue no genérico. Pede o concreto que só o dono tem: "me conta de UM cliente, o que ele te falou quando te procurou, com as palavras dele?", ou o número/print que aconteceu. Prova concreta vira criativo forte; alegação vazia vira criativo fraco.
- **Oferece refinar no fim:** depois de mostrar a prévia do lote, fecha com UMA linha de ajuste ("quer outro ângulo em uma delas? mais peças? outro CTA? refaço só a peça que você pedir"), pra o dono saber que dá pra ajustar sem começar do zero.

## Roteamento: o dono pediu X, você entra na ação N

| O dono pediu | Ação |
|---|---|
| "faz os criativos", "preciso de 4 artes pra campanha", "monta o lote", "renderiza as peças" | **1 · LOTE DE CRIATIVOS** (o caminho inteiro, passos 1 a 7) |
| "roteiro do anúncio em vídeo", "criativo em vídeo pra VSL", "o script do ad", "monta o lote de vídeo" | **1**, tipo de peça VÍDEO (ver `references/playbook-video-ads.md`) |
| "quantos criativos eu faço", "quando desisto da VSL", "o que varia primeiro", "esse criativo já validou?", "por que empacou na escala" | **4 · FÁBRICA E LEITURA DE MÉTRICA** |
| "qual o ângulo das peças", "que dor cada arte ataca", "só os ganchos por enquanto" | **1**, parando no STOP do passo 2 |
| "monta o playbook de criativo desse cliente", "replica o processo pro especialista novo", "quero o método pra outro nicho" | **2 · PLAYBOOK DE 4 CAMPOS** |
| "o criativo não vende", "CPL subiu, troco a arte?" | **3 · DIAGNÓSTICO PÚBLICO ANTES DE CRIATIVO** |

Pedido ambíguo ("me ajuda com o criativo"): pergunte UMA coisa só, "você quer as peças renderizadas agora, o playbook pra clonar o processo, entender por que o criativo atual não rende, ou o vídeo e a fábrica em volta (quantos criativos, o que varia, leitura de métrica)?", mostre a tabela como cardápio e siga pela resposta.

---

## Ação 1 · LOTE DE CRIATIVOS (do ângulo ao arquivo)

**O que faz:** entrega um lote de artes de anúncio, cada uma nascida de um ângulo de dor diferente do mesmo avatar, com identidade da marca aplicada e copy aprovada no lint.

**Precisa de:** o avatar e as dores dele, do perfil/brain do agente · a foto real da autoridade, sempre pedida ao dono (arquivo ou pasta) · a identidade visual (cor, fonte, selo, CTA, @perfil, formato), do perfil/brain quando existir · o destino do anúncio (URL de inscrição e evento de conversão), perguntado ao dono.

**Sem o insumo:** entrevista curta de 5 perguntas, uma por vez: quem é a pessoa que você quer atingir e o que dói nela · me manda 2 ou 3 fotos suas em boa resolução · qual a cor e a fonte da sua marca (se não souber, use preto e uma sem-serifa do sistema e marque `[A CONFIRMAR]`) · pra onde a pessoa vai quando clica · o que ela ganha lá. Sem foto real do dono não existe lote: pare e peça a foto, é o único bloqueio duro desta skill.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** na pasta de trabalho do lote, `identidade.json` (a marca), `manifesto.json` (uma entrada por peça), `copy-lote.md` (as linhas de texto, o arquivo que passa no lint), `out/` com as imagens renderizadas e `out/progress.json` (o checkpoint). Sem ferramenta de imagem no ambiente: `spec-render.md` com a especificação visual peça a peça, pro dono renderizar na ferramenta dele.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**O `out/progress.json` sai sempre, mesmo quando nada renderiza.** Quando o bloqueio de foto ou a falta de ferramenta de imagem impede o render, crie a pasta `out/` de verdade e grave o `progress.json` assim mesmo, com `"concluidas": []` e o motivo em `"bloqueio"`. Ele é o comprovante de que nada foi renderizado, e é o que separa "não rodou" de "rodou e não gravou". Checagem verificável antes de fechar: liste a pasta `out/` e confirme que ela existe no disco e que o `progress.json` está lá; nunca afirme que uma pasta foi criada sem listá-la, porque essa afirmação se confere em um comando.

**Leia primeiro:** `references/metodo-4-campos.md` (os 4 campos que sustentam qualquer lote) · `references/angulos-de-cpc.md` (o arsenal de 5 ângulos de CPC baixo, com a régua de lastro) · `references/EXEMPLO-FIM-A-FIM.md` (a forma da entrega). Quando o pedido é anúncio em VÍDEO, ou o dono já roda ads e precisa da fábrica em volta da peça (quantos criativos, o que varia primeiro, como a métrica volta pra copy): `references/playbook-video-ads.md`.

**Profundidade:** `references/exemplo-preenchido.md` (um caso fictício com os 4 campos de pé).

### Os 7 passos

**Passo 1 · ÂNGULO ANTES DA ARTE: 1 arte = 1 dor.** A peça nasce de um gancho por ângulo de dor específico do avatar, nunca de "uma imagem bonita". Escreva 3 ou 4 ganchos, cada um mordendo UMA dor diferente da mesma pessoa. Exemplo (nicho fictício, nutrição esportiva): "Você monta o plano. Quem segura a adesão?" · "O atleta melhora e some. E a consulta seguinte?" · "O mesmo paciente pode valer o dobro." · "Na periodização, você decide ou repete?" Quatro dores distintas, um avatar só.

**O arsenal de ângulos (técnicas de CPC baixo).** A dor continua sendo o alvo; o ângulo escolhe COMO a dor vira gancho. Cinco técnicas tiram o anúncio do leilão saturado (comunicação única, leilão limpo, CPC menor): **Falar sem dizer** (camuflar o gancho validado), **Segmentação reversa** (o criativo exclui quem não é o avatar), **Storytelling com plot twist**, **O Patinho Feio** (inverter a dor em vantagem) e **Trends virais** (gancho nativo do feed). O detalhe de cada um, quando usar, exemplo ancorado e a régua estão em `references/angulos-de-cpc.md`. **Régua de lastro (dura):** o Patinho Feio e o Plot Twist SÓ valem com verdade real. A inversão precisa do porquê verdadeiro e do perfil do dono; a história precisa ter acontecido. Inversão sem prova, choque vazio ou história inventada reprovam, a régua zero-inventado manda. Sem o fato na mão do dono, o gancho vira `[A CONFIRMAR]` e para ali.

**Passo 2 · STOP.** Mostre os ganchos ao dono e pergunte: "esses 4 ângulos batem com o que dói no seu cliente? Corto algum, troco algum?" Só siga com o OK.

**Passo 3 · FOTO REAL DA AUTORIDADE: nunca banco de imagem.** Rosto real do especialista, tratado (preto e branco, corte que NUNCA corta a cabeça). Foto de banco nasce fraca. Regra do corte: antes de cortar, meça onde ficam o topo do cabelo e o queixo no arquivo original e mantenha os dois dentro do quadro com folga; se a ferramenta de corte não achar o rosto sozinha, enquadre pelo olho e confira quadro a quadro. Cabeça cortada reprova a peça, sem exceção.

**Passo 4 · IDENTIDADE FIXADA NUM JSON.** Cor, fonte, selo e CTA saem do `identidade.json` na pasta de trabalho, nunca escritos dentro do código. É isso que torna o método portável: troca o JSON e o mesmo render cospe a identidade de outro cliente sem redesenhar nada. Campos mínimos:

```json
{
  "cor_principal": [17, 17, 17],
  "cor_fundo": [250, 249, 246],
  "cor_texto_sobre_veu": [17, 17, 17],
  "cor_sub": [110, 110, 110],
  "fonte": "caminho/do/arquivo/da/fonte.ttf",
  "selo": "PARA <NICHO> · AULA GRATUITA",
  "cta": "Cadastre-se",
  "assinatura": "[A CONFIRMAR: @ do perfil, confirmado pelo dono]",
  "formato": [1080, 1350]
}
```

**Identificador do dono nunca é deduzido, do mesmo jeito que a cor.** `assinatura`, `selo` e `cta` carregam o rosto do dono na peça, e um @ errado publicado é um anúncio apontando pra perfil de outra pessoa. O `@` só entra literal quando veio do dono, do perfil/brain do agente ou do insumo dele; deduzir do nome do negócio, do domínio ou de outro material **não vale como confirmação**. Sem essa origem, o campo fica `"assinatura": "[A CONFIRMAR: @ do perfil]"` e o render para nesse campo. Checagem verificável antes de fechar: para o `assinatura`, o `selo` e o `cta` preenchidos com texto literal, aponte ao lado a linha do insumo ou a resposta do dono que produziu cada um; campo literal sem origem apontada reprova a entrega, igual a número de cor sem origem.

**Cor descrita em palavra nunca vira valor exato.** O dono descreve a identidade em palavra ("off-white", "preto", "acento verde") e a skill nunca converte adjetivo de cor em RGB nem em hexadecimal. Sem o valor dado pelo dono, o campo entra como `"cor_acento": "[A CONFIRMAR: RGB de verde]"` e o render para nesse campo em vez de adivinhar. O `cor_fundo` é obrigatório sempre que o dono nomear a cor de fundo, mesmo que só em palavra. Checagem verificável antes de fechar: para cada campo de cor com número no `identidade.json`, aponte onde o dono deu aquele valor; número sem origem apontada reprova a entrega.

**Passo 5 · RENDER EM LOTE: o manifesto manda.** Monte o `manifesto.json`, uma entrada por peça, cada uma com a foto, o gancho (1ª linha), o sub (2ª linha, opcional), a chamada à ação e o nome de saída. O manifesto é a única fonte da verdade do lote; nada de gancho digitado na mão na hora de renderizar.

```json
{
  "pecas": [
    {
      "foto": "fotos/autoridade-01.jpg",
      "gancho": "Você monta o plano. Quem segura a adesão?",
      "sub": "O que muda quando o retorno vira parte do protocolo.",
      "cta": "Comenta ADESAO aqui embaixo que eu te mando o roteiro",
      "saida": "out/peca-01-adesao.jpg"
    }
  ]
}
```

**A chave `cta` é obrigatória em cada peça, com texto literal, e nunca é apagada pra passar no gate.** Uma rodada tirou o marcador do CTA e o motor tirou a chamada à ação junto: quatro anúncios sem uma linha de ação, e o gate passou. O texto vem, nesta ordem: (1) da ação que o dono já usa nos insumos, achada por `grep -rniE 'manda |chama |responde |comenta |envia ' <insumos>` com a saída colada; (2) da ação nativa da plataforma do anúncio; (3) do convite ao evento datado. Sem as três, sai a frase falada que dispensa botão (`me chama no Direct e eu te mando o link`), nunca um marcador e nunca a chave ausente. Antes de renderizar, rode e cole as duas saídas:

```
python3 -c "import json;d=json.load(open('manifesto.json'));print(len(d['pecas']))"
grep -c '"cta"' manifesto.json
```

Os dois números têm que ser iguais. Cole `CTAs no lote: N · com texto escrito: N · em marcador: 0 · ausentes: 0`, e qualquer linha diferente de zero nas duas últimas volta pro passo de escrita.

**Todo CTA diz O QUE o lead recebe ao agir, nunca só a palavra-chave (checagem que reprova).** Uma rodada fechou três de quatro peças em `manda BASE40 no WhatsApp` sem dizer o que a pessoa ganha ao mandar: sem aula, sem data, sem oferta, só a senha. A palavra-chave sozinha não é CTA, é um código sem promessa. O CTA carrega a palavra-chave MAIS o próximo passo concreto que o lead recebe: `manda BASE40 no WhatsApp que eu te mando a aula gratuita de 20 min` ou `comenta VAGA aqui embaixo que eu te mando o link da turma que abre dia 12`. A promessa vem do insumo do dono (o que ele de fato entrega no próximo passo: aula, PDF, diagnóstico, link de inscrição, oferta); sem esse insumo, pergunte AQUELE dado, nunca invente o brinde. Checagem antes de renderizar: para cada peça com CTA, escreva `peça <n> | palavra-chave: <literal> | recebe: <o que o lead ganha>`; qualquer peça com palavra-chave e sem o `recebe` preenchido reprova o lote.

**A ressalva de resultado (o range clínico, o "resultados variam") entra UMA vez, no fim da ÚLTIMA peça do lote (checagem que reprova se aparecer no meio).** A ressalva é rodapé do lote, não legenda de cada peça. Uma rodada colou o range clínico embaixo de peças do meio, onde ela corta o gancho e some antes do CTA da última. Regra: a ressalva sai só na peça de índice mais alto do lote, depois do CTA dela, e em nenhuma outra. Checagem antes de fechar: rode `grep -niE 'resultado.{0,20}(varia|individual|não.{0,3}garant)|resultados podem variar|cada caso' copy-lote.md` e confira que toda ocorrência cai dentro do bloco da última peça; ocorrência no bloco de qualquer peça anterior reprova o lote. Cole `ressalvas no lote: N · na última peça: N · em peça do meio: 0`, e a última coluna diferente de zero volta pro passo de escrita.

**Nome de terceiro nunca entra em pixel, e a pergunta da autorização vem antes do render.** Antes de renderizar, rode `grep -in 'autoriz' <perfil>`; sem uma linha do perfil autorizando o nome em peça pública, a arte sai com o papel (`uma aluna`) e a dúvida vai pro relato antes do render, porque perguntar num PNG já gerado não desfaz o PNG. `python3 scripts/checar_titulos.py --render <html> --perfil <perfil>` reprova nome sem autorização no HTML antes de exportar. Cole `nomes de terceiro na arte: 0 · autorizações citadas no perfil: N`.

**Nenhum card sai com marca d'água de teste na arte.** Antes de renderizar, rode e cole a saída:

```
grep -rniE 'teste|test|placeholder|sample|lorem|sintetico' <manifesto> <pasta de assets>
```

Frame de teste prova o pipeline e **nunca entra na peça entregue**: achado na saída, o frame sai do manifesto e a peça vira PARCIAL, sem render. Sem foto real, o card sai com tratamento de fundo declarado e sem imagem. Cole `cards com texto de teste na arte: 0`.

**O número colado é copiado da saída, não redigitado.** Redirecione a saída do contador pra um arquivo e cole o arquivo: `<comando do contador> > contagem.txt`, depois `cat contagem.txt` colado inteiro. Número redigitado que não reproduz reprova a contagem, mesmo quando o veredito é o certo.

**A varredura de imagem no disco roda antes de marcar PARCIAL.** Rode e cole a saída, inclusive vazia:

```
find <pasta de insumos> -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.mp4' -o -iname '*.mov'
```

**Vídeo conta como fonte:** havendo `.mp4` ou `.mov`, extraia os frames com `ffmpeg -i <video> -vf fps=1/4 -frames:v 4 frame-%02d.png` e use na peça. **Marcar PARCIAL sem a saída do find colada reprova a entrega.**

O render (foto tratada + véu + texto + selo + CTA, no formato do `identidade.json`) roda com a ferramenta de imagem que o ambiente tiver, nesta ordem:
1. um script de render que já venha com as skills de design instaladas (por exemplo em `soft-designer/scripts/`), chamado no shell;
2. um script próprio curto, escrito na pasta de trabalho, com a biblioteca de imagem do ambiente (Pillow ou equivalente), lendo `identidade.json` e `manifesto.json`;
3. sem shell nem biblioteca de imagem: a skill NÃO inventa pixel. Entrega `spec-render.md` com foto, texto exato, posição, cor, fonte e tamanho por peça, e segue nos passos 6 e 7 normalmente.

Peça solo = anúncio de imagem única (foto + gancho + sub + CTA). Rode o lote com checkpoint (grava o que já saiu em `out/progress.json`): se cair, roda de novo e retoma de onde parou.

**Quando o checkpoint falha no meio do lote:** o critério é o mesmo sempre. Peça que gravou no `progress.json` e tem arquivo em `out/` está pronta, não roda de novo. Peça que gravou e não tem arquivo está corrompida: apague a entrada dela do `progress.json` e o jpg parcial, e rode outra vez. Duas falhas seguidas na MESMA peça param o lote: mostre o erro cru ao dono em 3 linhas, não tente uma terceira. Erro de glifo ausente na fonte não é para retentar, é para trocar a fonte no `identidade.json` e rodar o lote inteiro de novo.

**Passo 6 · LINT ANTI-IA: obrigatório ANTES de virar pixel.** Toda linha de copy passa no gate antes de renderizar. Depois de renderizado, corrigir texto custa o lote inteiro.

Com shell: `python3 scripts/lint_copy.py copy-lote.md` (o script vem dentro desta skill). Só segue com exit 0.

Sem shell, o gate roda no olho, linha por linha, e reprova (falha dura): travessão longo, o verbo-freio banido (a forma verbal, o particípio e a forma com "des-"), frase-emoldura que promete revelação ("a verdade é que", "o segredo"), verbo-clichê (revoluciona, transforma, potencializa, alavanca), tricolon só pelo ritmo, "não é X, é Y" repetido, e qualquer número ou prova sem lastro no material do dono.

**Passo 7 · PRÉVIA PRO DONO, e STOP.** Renderize as prévias e mande pro dono aprovar ANTES de existir campanha. Nunca sobe criativo sem o dono ver. A ordem que evita refação: o dono aprova as PEÇAS primeiro, e só depois as campanhas e as copys. Pergunta literal: "essas são as 4 peças. Aprova todas, corto alguma, refaço alguma?"

**Passo 8 · SOBE PAUSADO + UTM PADRÃO.** A campanha nasce PAUSADA, com o UTM padrão pra casar lead com anúncio e conjunto:
`utm_campaign=<FUNIL-FIXO>` · `utm_content={{ad.name}}` · `utm_term={{adset.id}}`
Subir e segmentar de verdade é com **soft-trafego-meta**; se ela não estiver instalada, este passo sai como especificação escrita pro dono subir na mão.

---

## Ação 2 · PLAYBOOK DE 4 CAMPOS (clonar o processo pra outro especialista)

**O que faz:** monta o playbook de criativo de um cliente novo, pra qualquer pessoa rodar a Ação 1 nesse nicho sem redecidir nada.

**Precisa de:** quem é o especialista e o que ele vende · o avatar dele · a marca dele (cor, fonte, selo, CTA) · o destino do anúncio.

**Sem o insumo:** entrevista curta de 4 perguntas, uma por campo, na ordem abaixo. Campo sem resposta vira `[A CONFIRMAR]` no playbook e não impede a entrega.

**Entrega:** `playbook-criativo-<especialista>.md` na pasta de trabalho, com os 4 campos preenchidos e o `identidade.json` já montado dentro.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**Leia primeiro:** `references/metodo-4-campos.md` (o template completo).

**Profundidade:** `references/exemplo-preenchido.md`.

Os 4 campos:
- **CAMPO 1 (FOTO):** banco de foto própria da autoridade, tratada em preto e branco.
- **CAMPO 2 (IDENTIDADE):** o `identidade.json` (cor, fonte, selo, CTA, assinatura, formato).
- **CAMPO 3 (4 GANCHOS):** 4 dores distintas do avatar, 1 gancho por dor.
- **CAMPO 4 (DESTINO):** URL de inscrição, evento de conversão e o UTM padrão.

Preencheu os 4, roda a Ação 1 a partir do passo 4. **STOP:** o dono confirma os 4 campos antes de qualquer render.

---

## Ação 3 · DIAGNÓSTICO: público antes de criativo

**O que faz:** responde se a arte é mesmo o problema, antes do dono gastar um lote novo.

**Precisa de:** em que público cada criativo rodou, e o custo por lead de cada combinação, perguntados ao dono ou lidos do relatório da conta.

**Sem o insumo:** pergunte UMA coisa: "esse criativo rodou em quantos públicos diferentes, e qual foi o custo por lead em cada um?" Sem essa resposta, não existe diagnóstico, só chute.

**Entrega:** `diagnostico-criativo.md`, com a tabela criativo × público × custo por lead e o veredito em 1 linha.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou.

**A regra-mãe.** Antes de trocar ou matar um criativo, verifique o PÚBLICO. O mesmo criativo muda de custo por lead em ordem de grandeza só trocando o público: barato no público aberto mais semelhante, caro num interesse forçado. Mesma arte, custo multiplicado. No público certo, todos os criativos rodam na faixa boa e nenhum está "morto". [prova do dono: custo por lead nos dois públicos, período e conta]

Consequência pro método:
- Custo por lead alto NÃO é motivo pra refazer a arte antes de olhar em QUE público ela rodou.
- A alavanca de custo está no conjunto e no público, não na peça, quando a peça já passou pelos 7 passos.
- Só se troca criativo quando ele está ruim NO PÚBLICO BOM.

---

## Ação 4 · FÁBRICA E LEITURA DE MÉTRICA (a peça em vídeo e o que decide se vira dinheiro)

**O que faz:** responde as perguntas que ficam depois da peça pronta. Quantos criativos, de que tipo, em que cadência; o que varia primeiro quando um já vendeu; o que a métrica ruim manda reescrever; e quando um criativo conta como validado. É a camada de VÍDEO e de fábrica por cima do lote de imagem. **O detalhe inteiro está em `references/playbook-video-ads.md`, leia antes de responder.** Aqui ficam só as costuras.

**Anatomia do anúncio em vídeo (segundo tipo de peça, ao lado da imagem).** Hook de 3 a 5 segundos com função dupla (visual capta atenção, narrativo segmenta o público; fórmula `HOOK = ÂNGULO + BENEFÍCIO ou DOR`; antipadrão "Big Guru format" pra quem não é rosto público). Corpo com 3 elementos (mecanismo do problema, mecanismo da solução, prova) e a prova reposicionável em 3 lugares, o que rende 3 anúncios da mesma matéria-prima antes de escrever linha nova. CTA em 3 golpes (benefício, urgência, segmentação final) mais banner estático de 10 segundos. O roteiro de vídeo é copy e nasce aqui; a edição é da **soft-editor-video**, a execução na conta é da **soft-trafego-meta**. O roteiro passa pelo mesmo lint anti-IA e pela mesma régua de lastro do lote estático.

**Os 3 lotes.** Validação (5 corpos x 2 a 3 hooks, cerca de 15 peças, achar formato e corpo), escala (mantém o vencedor e varia o formato em 5 versões), manutenção (micro-variação da copy dentro do validado, voz clonada por IA, só depois de base validada). **Piso de 50 criativos antes de condenar uma VSL**, e 5 a 10 antes de julgar produto novo.

**Hierarquia de variação.** Ordem fixa: creative adaptation (trocar o formato) → novos hooks (mínimo 3) → SMDW → copy upgrade. **Teto de 2 a 3 hooks por criativo**, nunca 4 ou mais. Formato e corpo validam; hook é o último ajuste. Quem está aprendendo entrega 1 anúncio completo por vez.

**Mapa métrica → causa na copy.** CPM alto = FORMATO (trocar por nativo do feed). Hook rate baixo = ÂNGULO (reescrever os 3 a 5 segundos). CTR baixo = ESTRUTURA DA CTA (os 3 golpes com prova específica). Hold rate baixo = EDIÇÃO. Sempre contra o próprio recorde, nunca contra o mercado. Nunca reescrever a VSL sem olhar a métrica do criativo antes, e nunca retestar com criativo que não vendeu nada.

**Critério de VALIDADO (mora AQUI, a conta só executa).** Validado = 3 a 4 vendas dentro do CPA esperado; uma venda isolada é sorte. Campanha de escala só recebe validado. **Esta é a fronteira fechada:** o critério de validado e o mapa métrica → copy são decisão desta skill; a **soft-trafego-meta** cria, sobe, lê a métrica bruta, pausa e escala com o critério que sai daqui, e a separação estrutural teste vs escala é dela.

**Entrega:** quando o pedido é análise, `analise-criativos.md` na pasta de trabalho, com o mapa métrica → causa aplicado aos criativos do dono e o veredito de validado por peça. Quando é peça de vídeo, os mesmos arquivos da Ação 1 com o roteiro no lugar do manifesto de imagem. **Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último.**

---

**Número de terceiro sai com a tripla completa.** Preço de concorrente, média de mercado e qualquer número que não seja do dono entram na forma:

```
<número> | trecho: "<literal>" | url: https://... | consultado em: <dd/mm/aaaa>
```

**Linha sem URL completa reprova o número**: a referência interna da ferramenta de busca não abre no navegador do dono. Feche com `números de terceiro: N · com trecho literal: N · com URL completa: N`, os três iguais. O `checar_titulos.py` conta e reprova quando divergem.

## Gate de qualidade (roda antes de toda entrega)

**Número não confirmado nunca vira pixel (a arte publicada não carrega ressalva).** Antes de renderizar, rode `grep -n 'A CONFIRMAR' <perfil do dono>`, extraia cada valor marcado, e rode `grep -nF '<valor>' <copy da peça>` por valor, colando as duas saídas. Valor marcado sai da frase e entra a forma sem número ("algumas semanas", "depois de um tempo"), nunca o marcador e nunca o número cru: o card sai no feed sozinho, e quem lê não vê a ressalva que ficou no bastidor. Cole `valores não confirmados no perfil: N · renderizados na arte: 0`, e qualquer número acima de zero na segunda coluna reprova o render antes de exportar.

**Capa que chega pronta na copy fonte não se troca por outra pior.** Quando a peça nasce de uma copy que já tem capa ou headline escolhida, a capa da fonte é a linha a bater, nunca a linha a descartar por hábito. Cole `capa da fonte: <literal> · capa publicada: <literal> · motivo da troca: <escrito>`, passe a publicada pela régua com o gatilho nomeado, e feche com `manchetes idênticas à fonte: N de N`. **Capa publicada em molde `Como <resultado> sem <obstáculo>` reprova a troca**: é o molde mais batido do mercado, e é o que a régua existe pra superar. Sem motivo escrito, a capa da fonte volta.

**Os gates de arte saem em linha de saída, cada um com o comando literal ao lado.** Prosa não conta como contagem, e foi por isso que três exigências passaram sem número em duas entregas seguidas. O passo de render fecha com estas linhas, uma por linha, na forma `<gate>: <valor> | comando: <literal>`, cada uma com a saída crua colada acima dela:

```
realpath config: <saída> | comando: realpath <caminho do config do dono>
realpath skill: <saída> | comando: realpath <pasta desta skill>
a primeira começa pela segunda: não | comando: a comparação das duas saídas acima
cores medidas no PNG: <lista hex> | comando: python3 -c "from PIL import Image; ..." ou o medidor da skill
imagens fortes no PNG: N de N exigidas | comando: a contagem sobre os arquivos renderizados
cards com GIF: N de N exigidos | comando: ls *.gif
geradores testados: N (mínimo 2) · falharam: N | comando: um por linha na forma `gerador: X | testado: sim | resultado: Y`
```

Qualquer uma dessas linhas ausente reprova antes da análise de arte, e declarar sem a saída colada não conta como feito.


**Régua de títulos (vale em todo título, capa, assunto e nome de bloco que vai ao público).** Todo título, capa ou assunto passa pela régua de títulos (`references/regua-de-titulos.md`) e a checagem lista cada um com gatilho e veredito, nesta forma: `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. Checagem que só declara "conferido" não conta como feita, e título sem gatilho nomeado reprova a peça. **A checagem sai SEMPRE no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de entrega, mesmo quando esta skill já entrega crivo, prova, handoff ou relato: nome fixo é achável por `ls`, seção no meio de outro documento não é.** Ele fecha com as três contagens, nesta forma: `títulos produzidos: N · passados pela régua: N · reprovados e reescritos: N`. Os dois primeiros números têm que ser iguais, e qualquer diferença reprova, porque a régua não é amostra: conte os títulos antes de rodar, e o universo são TODOS os textos que o público lê como título, não só os de abertura. Entrega sem esse arquivo reprova antes da análise de conteúdo. **O gatilho sai da lista fechada, e a checagem imprime a lista antes da tabela:** `famílias válidas: Recompensa · Mistério · Crença · Disrupção · Popularidade · Reconhecimento`. Palavra fora dessa lista não conta como gatilho, e critério de R4 (inimigo nomeado, ordem invertida) NÃO é gatilho: é outra régua, e usá-la como gatilho deixa o título com zero rastreáveis. Cole `gatilhos fora da lista fechada: 0`, e qualquer número maior reprova o lote.

**Marcador nunca no miolo da fala (vale em toda peça que o lead lê ou ouve).** `[A CONFIRMAR: x]` e todo marcador de pendência só entram na peça em posição de CAMPO: um link, um telefone, uma data, um valor, sempre no fim da linha e substituível por colagem sem reescrever a frase. É PROIBIDO no miolo de uma frase falada ou lida, isto é, onde a frase perde o sentido sem o valor. Quando o dado falta no miolo há duas saídas e nenhuma terceira: escrever a frase na versão que dispensa o dado, ou perguntar ao dono ANTES de escrever a peça. O furo em si vai pro handoff, nunca pra fala. Checagem verificável: com shell, `grep -n "\[A CONFIRMAR" <peça>`; sem shell, leia linha a linha. Pra cada marcador, apague o marcador e releia a frase; se ela virar agramatical ou mudar de sentido, o marcador está no miolo e reprova. Cole a linha `marcadores na peça: N · em posição de campo: N · no miolo de frase: 0`.

**Nome de pessoa real em copy pública (vale em toda peça desta skill).** Nome, caso, frase ou história de pessoa real que veio de mensagem privada, caixa de entrada ou call NUNCA entra em copy pública sem autorização registrada pelo dono, isto é, uma linha `autorizado por <dono> em <data>` no próprio insumo. Sem essa linha: anonimiza (a primeira letra do nome, ou uma forma sem identificação como "uma aluna", sem cirurgia, idade e histórico que devolvam a identidade) ou não usa. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.** Marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova: o marcador registra a dúvida e não resolve o risco. **A checagem é COMANDO, nunca de memória**, nestes 3 passos: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, call, reclamação, perfil do dono) com `grep -hoE '\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{2,}(?=[,:] ?|[,:]$| [0-9]{2} anos)' <insumos privados> | sort -u`, somando toda lista de nomes colada pelo dono; (2) rode `grep -nwF '<nome>' <peça>` para cada nome, sobre o arquivo INTEIRO da peça (campos de configuração, filtros e checklists inclusos), não só as linhas que o destinatário lê; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente na saída sem a linha de autorização apontada por `<arquivo:linha>` reprova a entrega**, e `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N. Contagem declarada sem a saída colada não conta como feita, e declarar zero num arquivo onde o grep devolveu nome reprova.

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.

**Marcador fora da peça exportada (esta skill renderiza, então a regra é dura).** `[A CONFIRMAR]` nunca aparece DENTRO da peça exportada: PNG, PDF, HTML, vídeo, `.docx`, slide ou qualquer arquivo que o público final abre. O que falta confirmar vai pro handoff e pro relatório, ao lado do nome do arquivo e do lugar exato onde entra. Checagem verificável antes de fechar: busque `A CONFIRMAR` no texto que foi renderizado e nos arquivos exportados; uma ocorrência que seja reprova a peça e manda refazer o render.


| Critério | Passa se |
|---|---|
| Anti-IA na copy | o gate roda em TODO arquivo entregue, não só nos `.md`: `for f in $(find <pasta> -type f \( -name '*.md' -o -name '*.json' -o -name '*.txt' \)); do python3 scripts/lint_copy.py "$f"; done`, com a saída colada no relato e a contagem `arquivos linteados: N · exit 0: N`. Campo de texto livre dentro de JSON (motivo de bloqueio, descrição, nota) é copy e obedece às mesmas regras duras. Sem shell, a leitura linha a linha do passo 6 não acha nenhum item da lista dura |
| Ângulo por peça | cada peça do manifesto morde UMA dor nomeada, e duas peças não repetem a mesma dor |
| Foto | rosto real do dono, topo do cabelo e queixo dentro do quadro em toda peça |
| Identidade | cor, fonte, selo e CTA vieram do `identidade.json`, nenhum valor escrito dentro do código |
| Contraste | com véu claro, o texto da 1ª linha é escuro e o sub é cinza médio, conferido no arquivo final e não no preview |
| Lastro | todo número e toda prova na copy têm origem no material do dono, ou saem marcados `[A CONFIRMAR]` |
| CTA escrito | **o texto do botão nunca sai em marcador.** Ele vem, nesta ordem, da ação que o dono já usa nos insumos, da ação nativa da plataforma, ou do convite ao evento datado do perfil. Sem nenhuma das três, o CTA sai na versão que dispensa o botão. Cole `CTAs no lote: N · com texto escrito: N · em marcador: 0` |
| Ressalva no lote | a peça é o LOTE, nunca o arquivo: a ressalva clínica ou regulada entra UMA vez no conjunto, no fim da última peça. Cole a soma de `grep -c '<a frase da ressalva>'` sobre TODOS os arquivos da entrega, e ela tem que dar 1 |
| Prévia | o dono viu e aprovou as peças antes de existir campanha |

O veredito é o pior item da tabela. Falhou um, o lote não sai.

## Regras duras (cada uma nasceu de um erro que custou um lote)

1. **VÉU CLAREIA A BASE.** Quando o véu clareia a base pra um tom creme, o texto da 1ª linha tem que ser ESCURO, senão some. O sub usa cinza médio, não claro. Confira no arquivo final.
2. **REFAZER PEÇA SOLO É LIMPAR O CHECKPOINT.** Apague a entrada dela no `progress.json` e os jpgs daquela peça antes de rodar de novo, senão o checkpoint acha que ela já saiu e pula o item.
3. **MANTER ACENTOS NO MANIFESTO.** Escreva o texto com acento correto e teste UMA peça antes do lote. Se faltar glifo, troque a fonte, nunca tire o acento do texto.
4. **PUBLICAR NÃO É COMMITAR.** Guardar a imagem no repositório não coloca ela no ar. Abra a URL final da imagem no navegador antes de apontar o anúncio pra ela.
5. **PÁGINA E PERFIL SÃO FIXADOS NO CRIATIVO.** Ficam imutáveis dentro do criativo; errar significa refazer todos. Confirme a página certa ANTES, lendo o identificador de um anúncio ATIVO da própria conta, nunca chutando.
6. **LINT ANTES DE RENDERIZAR.** Copy passa no lint antes de virar pixel.
7. **PRÉVIA ANTES DE SUBIR.** O dono vê a prévia antes de existir campanha. Sempre.

## O que esta skill NÃO faz

Se a skill de destino não estiver instalada, esta faz o mínimo aqui, do jeito que está escrito no passo correspondente.

- Escrever a headline ou o gancho do zero como peça própria, com banco de fórmulas: **soft-conteudo-headlines**. Sem ela, os ganchos nascem aqui no passo 1.
- Peça editorial única com diagrama, tabela ou layout complexo: **soft-designer**. Sem ela, vale a ordem de preferência do passo 5.
- Criar campanha, segmentar, ler métrica, escalar ou pausar na conta: **soft-trafego-meta**. Sem ela, o passo 8 sai como especificação escrita.
- Decidir verba, distribuição e o que turbinar: **soft-trafego-meta**, na Ação 1 dela. Sem ela, entregue as peças e diga em 1 linha que a decisão de verba ficou em aberto.

## Arquivos

`references/regua-de-titulos.md` (a régua de títulos, as 7 regras que decidem se um título existe) · `references/metodo-4-campos.md` (o template de 4 campos) · `references/exemplo-preenchido.md` (um caso fictício com os campos de pé) · `references/EXEMPLO-FIM-A-FIM.md` (o lote inteiro, do briefing às artes) · `references/angulos-de-cpc.md` (os 5 ângulos de CPC baixo) · `references/playbook-video-ads.md` (a peça em vídeo e a fábrica: anatomia, 3 lotes, hierarquia de variação, mapa métrica, critério de validado) · `scripts/lint_copy.py` (o gate anti-IA em código) · `shared-references/filtro-anti-ia/` (a mesma régua por escrito, pro motor sem shell: `padroes-banidos.md` diz o que reprova, `falsos-positivos.md` roda antes de reprovar).

Insumos que a skill produz na PASTA DE TRABALHO do lote, não aqui: `identidade.json` · `manifesto.json` · `copy-lote.md` · `out/` com as imagens e o `progress.json`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Sem sandbox (a régua escrita, quando o lint não roda).** Motor sem shell não executa `scripts/lint_copy.py`, e isso não dispensa o anti-IA: aplique a régua no olho por `shared-references/filtro-anti-ia/padroes-banidos.md`, padrão por padrão, e passe cada reprovação por `shared-references/filtro-anti-ia/falsos-positivos.md` antes de mandar o trecho de volta pro passo de escrita, porque prosa autoral do dono cai no mesmo crivo e some se ninguém conferir. A entrega sai do mesmo jeito, no melhor que esse motor alcança, e o relato fecha com uma linha dizendo que a conferência anti-IA foi no olho, sem código: `anti-IA: conferido no olho pela régua escrita (sem shell nesta rodada)`. Calar o que ficou de fora reprova a entrega; declarar em uma linha reprova nada.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Nome presente sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` reprova**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. **Lead em negociação aberta nunca é chamada de aluna nem de cliente.**

## Passo 2 da checagem (fecho, roda por comando)

Depois de gravar todos os entregáveis, rode `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos> --perfil <perfil do dono>; echo exit=$?` e cole a saída. Ele exige o `conferencia/checagem-titulos.md` na pasta, confere o inventário (os 4 inteiros, o piso e o `inventário duplicado`), o universo dos títulos, o marcador acima de 6 palavras, o nome de conversa privada, a `saída do script reescrita` e o lint de todo `.md`, RELATO incluso. **`exit` diferente de 0 reprova a entrega inteira, antes da análise de conteúdo.**
