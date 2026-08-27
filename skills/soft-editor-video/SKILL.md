---
name: soft-editor-video
description: "Edita talking-head, reels e anúncios verticais 9:16: analisa a matéria-prima, preserva a fala, corta pausas, escolhe composição adaptativa, cria apoios de 2 a 3 segundos com imagem, tela real e cartela, usa legenda palavra por palavra, virada de layout, música discreta e auditoria visual. Pode gerar imagem pela conta ChatGPT e animar localmente ou por KAIROGEN, Higgsfield e Veo após conferir custo. Use quando o dono mandar vídeo cru, pedir edição, b-roll, animação de imagem, gancho, legenda, CTA, música, reel ou anúncio em vídeo. Não use para escrever o roteiro do zero, carrossel, landing page ou banner estático."
---

**Papel:** skill de domínio (operador de produção audiovisual). Suporte/infra, FORA do pipeline de copy dos funis - entra DEPOIS que o roteiro/ideia já existe (isso é da `soft-conteudo`/`soft-conteudo-reels`). Pega uma gravação talking-head e devolve um reels editado. **É marca-neutra como a `soft-designer`**: não embute a cara de ninguém - no onboarding entrevista o dono e salva o elenco/identidade dele em `config/personagens.json`, e cada cliente roda com a própria marca. Usa primeiro os recursos incluídos na conta e na máquina; recurso com créditos exige custo mostrado e aprovação. Método detalhado: `references/metodo.md`.

## 📦 O QUE ESTA SKILL PRODUZ

Um vídeo vertical 9:16 finalizado a partir de uma gravação crua, com:

- **Direção pela matéria-prima** - prova real pode ocupar a tela inteira; talking-head pode usar composição adaptativa; conteúdo puro pode ficar em tela cheia. Divisão fixa não é padrão automático.
- **Apoio image-first** - gera a imagem, aprova e só depois anima. Alterna cena, tela real e cartela conforme a fala.
- **Corte de roteiro + silêncio** - transcrição word-level (Whisper), enxuga o que não muda a mensagem (aprovado pelo dono) e tira os silêncios. Mais barato e mais ritmado.
- **Gancho / cold open (padrão v4)** - copia a frase mais forte pro comecinho, só o apresentador, com efeito + a mesma frase numa faixa, e transição pro corpo (`scripts/05_hook.py`).
- **Legenda** - gerada localmente palavra por palavra, ou reusa a que já veio no vídeo quando ela já segue a régua.
- **CTA fixo no final** (opcional) - card de encerramento do dono colado com transição suave.
- **Música de fundo discreta** - nivelada pra nunca cobrir a fala.
- **Export 1080x1920** por padrão. Só ampliar para 4K quando a fonte ou o destino justificarem.

**Identidade visual (marca-neutra):** os `personagens.json` SÃO a identidade do dono nas cenas (etnia/look do apresentador, mascote, sócio, ambiente, paleta, logo). Se o dono já tem ID visual definida na `soft-designer` (`identidade-visual-cliente`), puxe dela pra manter a mesma cara entre carrossel/banner e vídeo. Texto que aparece na tela passa pela `soft-critico-copy` e pelo lint anti-IA antes de queimar.

**Serve o agente:** equipa o LEON/cliente a produzir reels de atração sem editor humano. A IDEIA e o ROTEIRO vêm da `soft-conteudo`/`soft-conteudo-reels`; aqui é só a produção/edição.

---

## PASSO 0 - ONBOARDING (rodar SÓ se ainda não estiver configurado)

Antes de editar qualquer vídeo, verifique a configuração. **Se já existir, NÃO pergunte de novo** - siga direto pro pipeline.

### 0.1 Recursos de geração
1. Preferir transcrição local ou Groq, imagem pelo gerador da conta ChatGPT e movimento local. Chave OpenAI paga é proibida.
2. Tratar Gemini, KAIROGEN e Higgsfield como opcionais. Antes de usar créditos, consultar saldo e custo exato, mostrar o número ao dono e esperar o sim.
3. Nunca pedir chave que já existe. Conferir primeiro `config/`, ambiente e `CAMINHOS-CANONICOS.md`.
4. Ler `references/recursos-geracao.md` quando houver cena nova, animação externa, upscale ou troca de provedor.

### 0.2 Personagens do dono (a "marca" dele nas cenas)
1. Verifique se existe `config/personagens.json`. Se não existir, **entreviste o dono** pra montar o elenco que vai aparecer no b-roll dos vídeos dele. Pergunte, um de cada vez:
   - "Quem é o **apresentador principal** (você)? Descreve aparência: etnia, cabelo/careca, barba, roupa, vibe."
   - "Quer um **mascote**? Como ele é? (animal, cor, estilo, roupa)"
   - "Tem mais alguém fixo na marca? (sócio, co-host, assistente de IA)"
   - "Qual o **ambiente/cenário** padrão? (ex: escritório futurista, estúdio clean, loja...)"
   - "Qual a **paleta de cores** da marca?"
   - "Tem um **logo** que aparece nas cenas?"
   (Se o dono já tem identidade visual na `soft-designer`, reaproveite ela aqui em vez de perguntar do zero.)
2. Monte `config/personagens.json` no formato do `config/personagens.example.md` (cada personagem com uma descrição detalhada em inglês pro gpt-image-2; mantenha consistência). Defina `trio_sempre` = quem aparece em TODA cena.
3. Confirme com o dono mostrando 1 imagem de teste de cada personagem antes de produzir vídeo (gere com `scripts/01_gen_images.py` a partir de um `scenes.json` de teste e abra pra ele aprovar).

### 0.3 CTA final (opcional)
Pergunte se o dono quer um **card de encerramento fixo** (aparece no fim de todo vídeo). Se sim, ajude a criar: gere a imagem 9:16 no gpt-image-2 com os personagens + o texto/oferta dele → anime no Veo → salve em `config/cta_take.mp4`. Reuse em todos os vídeos. (A copy do CTA passa pelo `soft-anti-ia`.)

---

## PIPELINE (depois do onboarding)
1. **Ingestão:** ffprobe; extrair áudio; conferir se o vídeo já tem legenda (printar frames) e onde está.
2. **Leitura da fala e da imagem:** transcrever com palavras e tempos e gravar `speech_words` no manifesto. Separar fala, prova real, listas, nomes próprios e CTA. Escolher a composição pela matéria-prima, nunca pelo vídeo anterior.
3. **Corte:** começar na primeira fala completa, remover respiração e pausa longa, aplicar 1,2x quando essa família já estiver aprovada. Preservar toda a mensagem. Corte semântico só entra depois de aprovação nominal. Rodar `scripts/00_silence_cut.py ... --manifest edit-manifest.json`; o script grava o mapa explícito de cortes e aplica fade de áudio de 30 ms na entrada e na saída de cada trecho.
4. **Planejar apoios:** mapear fala para cenas de 2 a 3 segundos. Prioridade: prova real, imagem gerada e animada, cartela. Imagem não pode ficar parada por 8 ou 10 segundos. Lista entra item por item no instante da fala.
5. **Gerar imagens** (`scripts/01_gen_images.py`): gpt-image-2 1536x1024 high + crop 16:9 `crop=1536:864:0:80` (safe-area no prompt). **Abrir no computador do dono e esperar ele aprovar.**
6. **Animar:** usar movimento local como padrão. Para clipe gerado, seguir `references/recursos-geracao.md`: image-to-video, uma geração por vez, imagem aprovada, custo confirmado e prompt negativo.
7. **Montar animações e overlays:** seguir `references/regua-adaptativa.md`. No talking-head com apoio, manter rosto fechado e centralizado e virar o layout por flash no terço inicial. Prova real importante pode assumir tela inteira. Fechar todas as animações, apoios, faixas e overlays antes da legenda.
8b. **GANCHO / cold open - PADRÃO v4 (ligado)** (`scripts/05_hook.py`): copiar a **FRASE COMPLETA mais forte** pro comecinho - **só o apresentador, SEM b-roll** - com um **efeito** (`pb` preto-e-branco / `vhs` / `fantasma` / `tv_velha`) E a **mesma frase numa faixa** na tela (gancho sonoro + visual). Depois **transição** (`xfade=fadeblack`) pro corpo. A frase continua no lugar original. Ordem final: **gancho → corpo → CTA → música**.
   - **FRASE COMPLETA, nunca cortada na metade** (A/B pegam a frase inteira, mesmo passando um pouco de 5s).
   - **Faixa: MÁX 2 LINHAS**, fonte ~50% menor (range 66→28px), posição centro+15% (terço inferior). Já está no `05_hook.py`.
   - **O agente escolhe a frase sozinho** pelos critérios: viralização · gera expectativa · forte/polêmica. A frase passa pelo `soft-anti-ia` (nada que soe de IA na faixa).
8. **Legenda por último:** aplicar a legenda palavra por palavra somente depois de todas as animações e overlays; destacar a palavra-chave do trecho e manter a legenda no peito quando houver apresentador. Registrar `render_order` no manifesto. Legenda de bloco está reprovada nesta família.
9. **CTA no final** (se configurado): anexar `config/cta_take.mp4` com transição `xfade=fade:0.7` (sem corte seco). (`scripts/04_build_final.py` faz CTA + música.)
10. **Música de fundo discreta:** `loudnorm=I=-34:TP=-6:LRA=6` + `volume=0.38`, `amix normalize=0`, fade in/out. NUNCA sobrepõe a fala.
11. **Inspeção de cada corte:** renderizar o candidato e rodar `python3 scripts/06_inspect_cuts.py candidato.mp4 edit-manifest.json pasta/cortes`. O script abre os três quadros de cada emenda com a visão da conta ChatGPT e grava a prova. Ausência ou reprovação bloqueia o gate.
12. **Gate antes do export final:** salvar `edit-manifest.json` e rodar `python3 scripts/07_gate_edit.py edit-manifest.json`. O gate exige fala temporizada, mapa, fades de 30 ms, ordem da legenda e prova visual de cada corte. Falha bloqueia o export final.
13. **Export 1080x1920** + salvar na pasta de saída do dono. Abrir com visão real.
14. **AUDITORIA VISUAL (OBRIGATÓRIA, olhos reais):** escolher `SOFT_EDITOR_AUDIT_MODE` conforme a composição e rodar `python3 scripts/06_audit.py <final.mp4> <pasta>/audit 12 "<marcos>"`. O script extrai frames do MP4 entregue, monta `audit/mosaico.jpg`, mede a leitura integral e passa os quadros à visão da conta ChatGPT.
    - **PASSA (exit 0):** entregue o MP4 + `audit/mosaico.jpg` (os DOIS caminhos absolutos, cada um em linha isolada; a ponte sobe os dois no Telegram). Selo permitido, exato: "Auditoria visual: PASSA (N frames, codex). Prova: <mosaico>". Nada de "sync 0,000 ms" - isso não foi medido.
    - **REPROVA (exit 1):** NÃO é pronto. Corrige o problema apontado no `veredito.json` e re-roda a auditoria (1 ciclo). Persistiu ou é ambíguo: manda o mosaico + os motivos pro dono decidir.
    - **INDISPONÍVEL (exit 2, codex/visão fora do ar):** entregue o MP4 + mosaico com o aviso literal "não consegui auditar visualmente (visão indisponível), confere no mosaico". SEM selo.

## REGRAS INVIOLÁVEIS
- B-roll **image-first** (gpt-image-2 → Veo). Nunca texto→vídeo direto.
- A composição segue a matéria-prima. Nunca impor divisão de tela, gancho, CTA ou b-roll porque o vídeo anterior usou.
- Talking-head com apoio: enquadramento fechado, sem sobra acima da cabeça, legenda na altura do peito, apoio mudando a cada 2 a 3 segundos e virada de layout por flash no terço inicial.
- Lista aparece item por item. Legenda acende palavra por palavra. Esses dois pontos entram no manifesto e no gate.
- Fala compactada preserva palavras e tempos no manifesto. Toda edição grava um mapa explícito de cortes.
- Cada trecho cortado recebe fade de áudio de 30 ms na entrada e na saída. Corte seco de áudio reprova no gate.
- Legenda é a última camada visual: animações, apoios, faixas e overlays entram antes.
- Cada emenda passa pela inspeção visual de cortes antes da auditoria do arquivo final. Sem prova individual, o gate reprova.
- **Imagem aprovada = verdade absoluta.** O Veo só ANIMA, não recria. `negativePrompt` obrigatório.
- **Personagens sempre consistentes** com `config/personagens.json`. Trio (ou elenco fixo) presente em toda cena; extras conforme a fala.
- Checkpoint: **aprovar as imagens antes de animar.**
- **Texto na tela passa pelo `soft-anti-ia`** antes de queimar (gancho, faixa, CTA).
- **Mostrar, não afirmar.** "Conferido/auditado" só existe se `scripts/06_audit.py` rodou AGORA sobre o arquivo entregue e devolveu PASSA, com `audit/mosaico.jpg` anexo na mesma mensagem. Selo sem mosaico anexo é mentira, mesmo que o vídeo esteja bom.
- **Você não tem olhos.** Nunca descreva o conteúdo de um frame que nenhuma ferramenta de visão te devolveu. Proibido alegar "sync", "ms", "frames conferidos", "decodificação sem erros" ou qualidade visual de qualquer coisa que você não passou pelo `06_audit.py`.
- **Conclusão honesta.** Auditoria REPROVOU ou não rodou = a entrega NÃO ganha selo. Reprovado: corrige ou vai pro dono com o mosaico e os motivos. Indisponível: entrega com o aviso. "Concluída" por cima de reprovação não existe.
- **Custo da auditoria:** ZERO API paga - roda na conta OAuth do ChatGPT (mesmo motor do LEON). +40-100s no pipeline. Irrelevante perto do Veo.
- **Gotcha:** amostrar 0.8s DEPOIS de transição; frame no meio do `xfade` parece dupla exposição e reprova à toa (o `06_audit.py` já trata via marcos).

## RECURSOS E SKILLS LIGADAS

- `soft-conteudo-reels`: escreve ou corrige o roteiro antes da edição. Não reescrever roteiro dentro do Editor.
- `soft-critico-copy`: critica HEADLINE, gancho, CTA e qualquer texto público antes de queimar.
- `soft-designer`: fornece identidade visual, personagens, paleta, tipografia e direção das imagens.
- `remotion-best-practices`: aplicar quando a composição usa Remotion; o template local continua sendo a base visual aprovada.
- `references/recursos-geracao.md`: roteia ChatGPT, movimento local, KAIROGEN, Higgsfield, Veo e fallback.
- `references/regua-adaptativa.md`: governa enquadramento, ritmo, legenda, virada, prova real e escolha de composição.

---

## FORMAS (escolha pela matéria-prima)

Esta skill entrega em duas formas. Leia a linha e decida antes de produzir:

- **FORMA A - Tela cheia de prova:** use quando Telegram, página, produto ou demonstração real é a prova central.
- **FORMA B - Composição adaptativa:** talking-head com apoios rápidos, virada de layout e alternância de cenas, telas e cartelas. É a forma padrão dos anúncios novos. Leia `references/regua-adaptativa.md`.
- **FORMA C - Topo-fixo com slides e telas** (aprovada pelo Léo em 18/08/2026):
  rosto FIXO em cima, faixa de baixo com SLIDES de texto + TELAS reais de
  produto (print/gravação), legenda branca fina rente à divisão, fala tratada
  (corta respiração/pausa + 1.2x). Motor React/Remotion. Use quando o apoio é
  MOSTRAR o que a fala cita, não ilustrar. Receita completa, as 4 correções
  cravadas e o template pronto: **`references/forma-topo-fixo.md`** +
  **`templates/topo-fixo/`**.

Na Forma C, o IMG_4361 aprovado em 22/08/2026 é o molde visual intocável desta
família. Os critérios obrigatórios e o gate de amostra estão registrados na
receita completa. Não regenere nem altere o IMG_4361.
- **FORMA D - Conteúdo puro:** vídeo original em tela cheia com HEADLINE curta nos 3 segundos iniciais, ou sem arte adicional quando essa for a direção aprovada.
