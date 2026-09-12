"""Auditoria VISUAL do MP4 final: extrai frames, monta mosaico (prova pro dono)
e pergunta pra CLI de IA com visao se a composicao esta certa. OLHOS REAIS, sem chave paga nova.

O motor do agente em modo texto puro NAO ve imagem. Sem este passo, qualquer
"12/12 frames conferidos" e alucinacao de conformidade. Aqui a alegacao vira medicao.

A CLI de visao vem de VISAO_CLI (default "codex"); os argumentos de invocacao vem de
VISAO_CLI_ARGS; o modelo com visao vem de AUDIT_MODEL. Se a CLI nao existir no PATH, o script sai com codigo 2 (INDISPONIVEL)
e entrega so o mosaico: nunca finja auditoria visual que nao aconteceu.

Uso: python3 06_audit.py final.mp4 [pasta_audit] [N] [marcos_csv]
  marcos_csv: timestamps de transicao (fim do gancho, inicio do CTA), ex: "6.2,52.0"
Exit: 0=PASSA . 1=REPROVA . 2=AUDITORIA INDISPONIVEL (visao falhou; mosaico existe mesmo assim)
"""
import subprocess, os, sys, json, time, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _config as C

if len(sys.argv) < 2:
    print("uso: python3 06_audit.py final.mp4 [pasta_audit] [N] [marcos_csv] [verbos.json]"); sys.exit(2)

# Visao pela CLI de IA do ambiente (variavel VISAO_CLI, default 'codex'), sem chave paga nova.
SRC = os.path.abspath(sys.argv[1])
if not os.path.exists(SRC):
    print(f"AUDIT INDISPONIVEL: MP4 nao existe: {SRC}"); sys.exit(2)
AUD = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(C.OUTPUT_DIR, "audit")
N = int(sys.argv[3]) if len(sys.argv) > 3 else 12
MARCOS = [float(x) for x in sys.argv[4].split(",") if x.strip()] if len(sys.argv) > 4 else []
# Tabela de verbos do pedido (argv[5]): lista de {"verbo","estado","motivo_medido"}.
# Estado "nao_feito" reconcilia o status do veredito, pra o JSON nunca dizer PASSA
# enquanto o relatorio diz PASSA COM PENDENCIA.
VERBOS_PATH = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5].strip() else None
VERBOS = []
if VERBOS_PATH:
    if not os.path.exists(VERBOS_PATH):
        print(f"AUDIT INDISPONIVEL: tabela de verbos nao existe: {VERBOS_PATH}"); sys.exit(2)
    with open(VERBOS_PATH, encoding="utf-8") as _vh:
        _vd = json.load(_vh)
    VERBOS = _vd.get("verbos", _vd) if isinstance(_vd, dict) else _vd
    if not isinstance(VERBOS, list):
        print("AUDIT INDISPONIVEL: verbos.json tem que ser lista de {verbo, estado, motivo_medido}"); sys.exit(2)


def _pendencias_dos_verbos(verbos):
    """Verbo do pedido em 'nao_feito' vira entrada de problema, no formato da regra."""
    out = []
    for item in verbos:
        if not isinstance(item, dict):
            continue
        estado = str(item.get("estado", "")).strip().lower().replace(" ", "_")
        if estado in ("nao_feito", "não_feito"):
            out.append({"verbo": item.get("verbo", "?"),
                        "motivo_medido": item.get("motivo_medido", "sem motivo medido declarado")})
    return out
FRD = os.path.join(AUD, "frames"); os.makedirs(FRD, exist_ok=True)
# Reauditar na mesma pasta nao pode misturar frames de uma rodada anterior no mosaico.
for _old_frame in glob.glob(os.path.join(FRD, "f_*_t*.jpg")):
    try:
        os.unlink(_old_frame)
    except OSError:
        pass
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_HAS_FONT = os.path.exists(FONT)

def _fail(msg, code):
    """Registra veredito indisponivel e sai. Mosaico pode ou nao existir ainda."""
    try:
        json.dump({"status": "indisponivel", "erro": str(msg)[:300], "mp4": SRC,
                   "audited_at": time.time()}, open(os.path.join(AUD, "veredito.json"), "w"))
    except Exception:
        pass
    print(f"AUDIT INDISPONIVEL: {str(msg)[:160]}"); sys.exit(code)

def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", p],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0

D = dur(SRC)
if D < 1.0:
    _fail(f"duracao invalida ({D}s): MP4 corrompido ou vazio?", 2)

# ---- 1. timestamps: gancho(1s) + CTA(D-2) + marcos+0.8 (NUNCA no meio do xfade) + uniforme ----
ts = {1.0, max(0.5, D - 2.0)} | {min(D - 1.0, m + 0.8) for m in MARCOS}
i = 0
while len(ts) < N and i < N * 3:
    ts.add(round(2.0 + (D - 5.0) * (i + 0.5) / N, 2)); i += 1
TS = sorted(t for t in ts if 0.2 <= t <= D - 0.2)[:N]

# ---- 2. extrai frames (768 de largura, ts queimado pra a visao referenciar) ----
frames = []
for k, t in enumerate(TS):
    f = os.path.join(FRD, f"f_{k:02d}_t{t:.1f}.jpg")
    draw = (f",drawtext=fontfile={FONT}:text='t={t:.1f}s':x=12:y=12:fontsize=30:"
            f"fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=8") if _HAS_FONT else ""
    subprocess.run(["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", SRC, "-frames:v", "1", "-q:v", "2",
                    "-vf", f"scale=768:-2{draw}", f],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(f) and os.path.getsize(f) > 0:
        frames.append(f)
if len(frames) < max(4, N // 2):
    _fail(f"extracao de frames falhou (so {len(frames)} de {N})", 2)

# ---- 3. mosaico (a PROVA pra entrega; existe mesmo se a visao cair) ----
MOSAICO = os.path.join(AUD, "mosaico.jpg")
subprocess.run(["ffmpeg", "-y", "-framerate", "1", "-pattern_type", "glob", "-i", f"{FRD}/f_*.jpg",
                "-vf", "scale=360:640,tile=4x3", "-frames:v", "1", "-q:v", "3", MOSAICO],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
_mos_ok = os.path.exists(MOSAICO) and os.path.getsize(MOSAICO) > 0

# ---- 4. decodificacao integra (a alegacao "sem erros" vira medicao real) ----
r = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-f", "null", "-"],
                   capture_output=True, text=True)
decode_ok = (r.returncode == 0 and not r.stderr.strip())
if r.stderr.strip():
    open(os.path.join(AUD, "decode_errors.txt"), "w").write(r.stderr)

# ---- 5. VISAO via CLI de imagem (-i FILE...), JSON estrito por --output-schema ----
# A CLI e configuravel: VISAO_CLI (binario) e VISAO_CLI_ARGS (argumentos). O default
# usa a sessao ja autenticada da CLI, sem abrir chave paga nova. O motor fica cego
# quando ninguem passa os frames; aqui passamos.
CODEX = os.environ.get("VISAO_CLI", "codex")
# Modelo de visao passado pra CLI. Configuravel por AUDIT_MODEL: cada ambiente/motor
# nomeia o proprio modelo com visao, e o default so serve o caso mais comum.
AUDIT_MODEL = os.environ.get("AUDIT_MODEL", "gpt-5.6-terra")
AUDIT_MODE = os.environ.get("SOFT_EDITOR_AUDIT_MODE", "standard").strip().lower()
_gancho_files = [os.path.basename(f) for f in frames if "_t1.0.jpg" in f]
gancho = ", ".join(_gancho_files)
cta = os.path.basename(frames[-1])
_lista = "\n".join(f"  {i+1}. {os.path.basename(f)}" for i, f in enumerate(frames))
if AUDIT_MODE == "lesson_screen":
    PROMPT = f"""Voce audita uma AULA DE ONBOARDING em 16:9, gravada no Google Meet.
A composicao original alterna dois estados corretos: conversa com a camera do instrutor ocupando a tela e demonstracao com a tela compartilhada como prova principal, acompanhada pela coluna pequena dos participantes do Meet. Nao deve haver b-roll, headline, legenda queimada, CTA, musica visualizada, moldura nova ou layout artificial.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: false em tela compartilhada; em camera cheia, true somente se houver espaco vazio claramente excessivo acima da cabeca
- enquadramento_frouxo: false em tela compartilhada; em camera cheia, true somente se o instrutor estiver pequeno e perdido no quadro
- rosto_cortado: true se olhos, boca, queixo ou topo da cabeca estiverem cortados de modo ruim na camera cheia ou na miniatura do Meet
- faixa_broll_vazia: true somente se houver faixa, painel, moldura ou layout artificial acrescentado pela edicao; a coluna original do Meet nao e b-roll
- broll_deformado: true se a tela compartilhada estiver esticada, cortada, ilegivel por deformacao ou visualmente corrompida
- legenda_cobre_rosto: true se texto, legenda ou arte acrescentada cobrir rosto ou conteudo importante da tela; o relogio t= do canto e somente identificacao da auditoria e deve ser ignorado
- faixa_gancho_estoura: true se houver headline, selo, CTA ou gancho visual acrescentado; se nao houver, false
Confirme no resumo se os dois estados originais da aula foram preservados, se as telas continuam legiveis e se nao existe arte de reel. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. Mudanca normal de tela ou cursor entre cortes nao e defeito.
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "feed_plain":
    PROMPT = f"""Voce audita um video vertical 9:16 de FEED com tratamento minimo.
O enquadramento original do apresentador deve ser preservado. Esta peca NAO deve ter headline, legenda, apoio, slide, efeito, musica, CTA ou layout dividido. Espaco do ambiente acima da cabeca faz parte da gravacao original e NAO e defeito neste modo.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: false em todos os frames, pois o enquadramento original e intencional
- enquadramento_frouxo: true somente se o apresentador ficar pequeno demais para reconhecer; nao marque por preservar o quadro original
- rosto_cortado: true se olhos, boca, queixo ou topo da cabeca forem cortados de modo ruim
- faixa_broll_vazia: true se existir layout dividido ou faixa artificial; em tela cheia original, false
- broll_deformado: true se a imagem principal estiver esticada, quebrada ou visualmente corrompida
- legenda_cobre_rosto: true se qualquer texto ou legenda adicionada aparecer sobre o rosto; se nao houver texto, false
- faixa_gancho_estoura: true se houver headline, faixa ou selo adicionado; se nao houver, false
Confirme no resumo se o video permanece take original em tela cheia e sem arte adicional. CALIBRACAO: marque true SO para problema CLARAMENTE visivel.
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "pixel_hybrid":
    PROMPT = f"""Voce audita a COMPOSICAO de um anuncio vertical 9:16 no modelo Pixel hibrido.
Nos primeiros 7 segundos existe uma abertura em split horizontal: b-roll estatico na metade de cima, apresentador na metade de baixo, linha laranja fina na divisoria e headline em TRES caixas laranja alinhadas a esquerda e centradas na divisoria. Depois disso, o corpo e apresentador em tela cheia. Nao existe faixa de b-roll permanente, musica nem card final.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: true se houver ar vazio excessivo acima da cabeca no corpo; na abertura, false
- enquadramento_frouxo: true se o apresentador estiver pequeno e perdido no quadro; na abertura, false se ocupar bem a metade inferior
- rosto_cortado: true se olhos, boca, queixo ou topo da cabeca estiverem cortados de modo ruim
- faixa_broll_vazia: true SOMENTE na abertura se a metade superior estiver vazia, preta ou mal preenchida; no corpo em tela cheia, false
- broll_deformado: true SOMENTE na abertura se a imagem superior estiver esticada, quebrada ou com pessoa deformada; no corpo, false
- legenda_cobre_rosto: true se legenda, selo ou marca cobrir olhos, nariz, boca ou centro do rosto
- faixa_gancho_estoura: true SOMENTE na abertura se qualquer uma das tres caixas sair da tela, ficar ilegivel, fugir claramente da divisoria ou cobrir o rosto; tres caixas e o desenho correto e nao reprova
Confirme no resumo se a abertura split ocupa os primeiros segundos, se o corpo fica em tela cheia, se as legendas permanecem legiveis no terco inferior e se o final termina no rosto sem card. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. Na duvida ou problema leve, false e cite em "obs".
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "slides_fullscreen":
    PROMPT = f"""Voce audita a COMPOSICAO de uma APRESENTACAO VERTICAL 9:16 que alterna tres estados de tela inteira: take do apresentador, slide narrativo e prova real de tela (uma conversa, um app, um painel). NAO existe faixa de b-roll e NAO deve existir layout dividido permanente.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Frame inicial: {gancho or 'nenhum'}. Frame final: {cta}.
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: true SOMENTE em take do apresentador quando o ar vazio acima da cabeca for MAIOR que a altura da propria cabeca; em slide/prova, false
- enquadramento_frouxo: true SOMENTE em take do apresentador pequeno, com sobra clara em cima E laterais; em slide/prova, false
- rosto_cortado: true se rosto, topo da cabeca ou queixo estiverem cortados; em slide/prova, false
- faixa_broll_vazia: neste modo, true se houver split-screen constante, apresentador espremido ou prova de tela usada como rodape pequeno; false para take, slide e prova que ocupam o canvas inteiro
- broll_deformado: neste modo, true se slide estiver quebrado/deformado OU se a prova real de tela estiver pequena/ilegivel; false nos takes do apresentador
- legenda_cobre_rosto: true se qualquer texto cobrir o rosto do apresentador
- faixa_gancho_estoura: false em todos os frames; esta peca nao usa faixa de gancho
Confirme no resumo se ha alternancia clara entre apresentador, slides narrativos de tela inteira e prova real de tela em tela inteira. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. Na duvida ou problema leve, false e cite em "obs".
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "screen_captioned":
    PROMPT = f"""Voce audita uma GRAVACAO DE TELA vertical 9:16 em tela cheia com legenda queimada palavra por palavra.
A tela real e a prova principal. A unica arte acrescentada permitida e a legenda em Inter, branca, com uma palavra ativa verde, no terco inferior. Nao deve haver talking-head, split-screen, b-roll, slide, headline, CTA, moldura, efeito ou cartela.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: false em todos os frames, pois nao existe apresentador
- enquadramento_frouxo: true somente se a tela real nao preencher o quadro vertical ou ficar pequena com bordas artificiais
- rosto_cortado: false em todos os frames, pois nao existe apresentador
- faixa_broll_vazia: true se existir split-screen, faixa artificial ou painel vazio; tela real cheia deve ser false
- broll_deformado: true se a tela real estiver girada, esticada, cortada de modo inutilizavel ou visualmente corrompida
- legenda_cobre_rosto: use este campo como falha de POSICAO da legenda: true somente se a legenda cobrir uma informacao central claramente importante da tela ou estiver cortada; a legenda no terco inferior, legivel e com fundo discreto deve ser false
- faixa_gancho_estoura: true se aparecer headline, faixa de gancho, CTA ou cartela; a legenda comum nao conta
No resumo confirme se a legenda aparece ao longo do video, e legivel, tem no maximo duas linhas, usa branco com palavra ativa verde e se a gravacao permanece em tela cheia e corretamente orientada. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. O relogio t= no canto pertence a auditoria e deve ser ignorado.
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "cta_fullscreen":
    PROMPT = f"""Voce audita um CTA FINAL vertical 9:16 em tela cheia.
A peca usa um take cinematografico do apresentador caminhando como fundo continuo. De 0,25s a 3,70s aparece uma promessa no topo, com no maximo duas linhas. De 3,82s ao fim aparece somente o CTA no terco inferior, com no maximo duas linhas. Nao deve existir seta, split-screen, faixa de b-roll, slide ou cartela vazia. Texto branco com destaques verde-neon e fundo preto discreto e a identidade aprovada.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: true somente se houver vazio artificial excessivo acima da cena; o texto no topo nao conta como vazio
- enquadramento_frouxo: true somente se o apresentador ficar pequeno demais ou perdido no quadro
- rosto_cortado: true se olhos, boca, queixo ou topo da cabeca estiverem cortados de modo ruim
- faixa_broll_vazia: true somente se existir split-screen, faixa artificial ou painel vazio; take em tela cheia deve ser false
- broll_deformado: true se apresentador, membros, rosto ou ambiente estiverem visivelmente deformados ou corrompidos
- legenda_cobre_rosto: true se a promessa ou o CTA cobrirem o rosto, ficarem cortados ou ilegíveis; texto fora do rosto deve ser false
- faixa_gancho_estoura: true somente se a promessa do topo sair da area segura, ultrapassar duas linhas ou encostar nas bordas; caso contrario false
No resumo confirme se a promessa e o CTA sao legiveis, se nao existe seta, se o rosto permanece livre e se o take ocupa o quadro inteiro. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. O relogio t= pertence a auditoria e deve ser ignorado.
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "cta_fullscreen_3line":
    PROMPT = f"""Voce audita um CTA FINAL vertical 9:16 em tela cheia.
A peca usa um take cinematografico do apresentador caminhando como fundo continuo. De 0,10s ate o fim aparece uma promessa fixa no topo, obrigatoriamente em tres linhas. De 3,82s ao fim aparece tambem o CTA no terco inferior, com no maximo duas linhas. Nao deve existir seta, split-screen, faixa de b-roll, slide ou cartela vazia. Texto branco com destaques verde-neon e fundo preto discreto e a identidade aprovada.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: true somente se houver vazio artificial excessivo acima da cena; o texto no topo nao conta como vazio
- enquadramento_frouxo: true somente se o apresentador ficar pequeno demais ou perdido no quadro
- rosto_cortado: true se olhos, boca, queixo ou topo da cabeca estiverem cortados de modo ruim
- faixa_broll_vazia: true somente se existir split-screen, faixa artificial ou painel vazio; take em tela cheia deve ser false
- broll_deformado: true se apresentador, membros, rosto ou ambiente estiverem visivelmente deformados ou corrompidos
- legenda_cobre_rosto: true se a promessa ou o CTA cobrirem o rosto, ficarem cortados ou ilegíveis; texto fora do rosto deve ser false
- faixa_gancho_estoura: true somente se a promessa do topo sair da area segura, tiver quantidade diferente de tres linhas ou encostar nas bordas; tres linhas e o desenho correto e nao reprova
No resumo confirme se a promessa fixa de tres linhas e o CTA sao legiveis, se nao existe seta, se o rosto permanece livre e se o take ocupa o quadro inteiro. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. O relogio t= pertence a auditoria e deve ser ignorado.
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "cta_fullscreen_3line_from_start":
    PROMPT = f"""Voce audita um CTA FINAL vertical 9:16 em tela cheia.
A peca usa um take cinematografico do apresentador caminhando como fundo continuo. De 0,10s ate o fim aparecem ao mesmo tempo: uma promessa fixa no topo, obrigatoriamente em tres linhas, e o CTA no terco inferior, com no maximo duas linhas. Nao deve existir seta, split-screen, faixa de b-roll, slide ou cartela vazia. Texto branco com destaques verde-neon e fundo preto discreto e a identidade aprovada.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: true somente se houver vazio artificial excessivo acima da cena; o texto no topo nao conta como vazio
- enquadramento_frouxo: true somente se o apresentador ficar pequeno demais ou perdido no quadro
- rosto_cortado: true se olhos, boca, queixo ou topo da cabeca estiverem cortados de modo ruim
- faixa_broll_vazia: true somente se existir split-screen, faixa artificial ou painel vazio; take em tela cheia deve ser false
- broll_deformado: true se apresentador, membros, rosto ou ambiente estiverem visivelmente deformados ou corrompidos
- legenda_cobre_rosto: true se a promessa ou o CTA cobrirem o rosto, ficarem cortados ou ilegíveis; texto fora do rosto deve ser false
- faixa_gancho_estoura: true somente se a promessa do topo sair da area segura, tiver quantidade diferente de tres linhas, o CTA inferior tiver mais de duas linhas, um dos dois textos nao estiver presente desde o primeiro frame auditado ou encostar nas bordas
No resumo confirme se a promessa fixa de tres linhas e o CTA aparecem juntos desde o inicio e permanecem legiveis, se nao existe seta, se o rosto permanece livre e se o take ocupa o quadro inteiro. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. O relogio t= pertence a auditoria e deve ser ignorado.
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "organic_body_cta":
    PROMPT = f"""Voce audita uma variante organica vertical 9:16 composta por um corpo de video ja aprovado e um CTA final de 7 segundos.
O corpo pode ser talking-head com apresentador em cima e apoios embaixo ou gravacao de tela cheia. Preserve a composicao que ja existe: nao exija um unico layout para todos. No fim ha uma transicao curta e limpa, sem dupla exposicao, para o CTA em tela cheia com apresentador caminhando. Nesse CTA, a promessa fica fixa em tres linhas no topo e "Comente SOCIO para receber o link" fica em ate duas linhas no terco inferior, ambos desde o inicio do CTA. Nao deve haver seta.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: true somente se houver vazio artificial claramente ruim; espaco natural da gravacao nao conta
- enquadramento_frouxo: true somente se houver enquadramento claramente defeituoso, nunca apenas por diferenca de estilo entre os videos
- rosto_cortado: true se olhos, boca, queixo ou topo da cabeca estiverem cortados de modo ruim
- faixa_broll_vazia: true se existir painel ou faixa artificial vazia; gravacao de tela cheia e CTA em tela cheia devem ser false
- broll_deformado: true se imagem, tela, apresentador ou apoio estiverem visivelmente deformados, corrompidos ou com dupla exposicao na transicao
- legenda_cobre_rosto: true se legenda ou texto cobrir informacao central, rosto, ficar cortado ou ilegivel
- faixa_gancho_estoura: no corpo, true somente para arte claramente fora da area segura; no CTA, true se a promessa nao tiver tres linhas, o CTA inferior nao estiver presente, houver seta ou algum texto encostar nas bordas
No resumo confirme a integridade visual do corpo, a transicao limpa e a presenca simultanea da promessa de tres linhas e do CTA inferior no encerramento. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. O relogio t= pertence a auditoria e deve ser ignorado.
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "generated_clip":
    PROMPT = f"""Voce audita um CLIPE CURTO DE ANIMACAO GERADA, sem apresentador, legenda, headline ou CTA.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Avalie tambem a coerencia visual entre os frames sucessivos. Para CADA frame responda booleans usando estes campos legados:
- teto_morto: false em todos os frames, pois nao existe apresentador
- enquadramento_frouxo: false em todos os frames, pois a cena deve ocupar o quadro inteiro
- rosto_cortado: true somente se surgir rosto ou pessoa acidentalmente e estiver deformado ou cortado
- faixa_broll_vazia: true se o quadro estiver vazio, preto, quebrado ou sem a cena principal
- broll_deformado: true se houver objeto duplicado, geometria derretida, texto inventado, artefato grave, mudanca incoerente de cena ou deformacao evidente
- legenda_cobre_rosto: true se aparecer legenda, palavra, logo ou marca d'agua inventada; caso contrario false
- faixa_gancho_estoura: false em todos os frames, pois nao existe gancho
No resumo diga se a cena permanece coerente ao longo da sequencia e se ha movimento visual perceptivel entre os frames, sem inventar medidas de tempo. CALIBRACAO: marque true SO para problema CLARAMENTE visivel.
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "forma_d":
    PROMPT = f"""Voce audita a COMPOSICAO de um video vertical 9:16 na FORMA D (conteudo puro): o video original ocupa a tela INTEIRA do comeco ao fim.
Nesta forma NAO existe faixa de b-roll, NAO existe apoio gerado, NAO existe split-screen e NAO existe slide. A unica arte acrescentada permitida e uma headline curta nos primeiros 3 segundos e, quando houver, a legenda no terco inferior. Nada disso e defeito: e a forma escolhida.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: true SOMENTE se houver apresentador visivel E o ar vazio acima da cabeca for MAIOR que a altura da propria cabeca; sem apresentador na tela, false
- enquadramento_frouxo: true SOMENTE se houver apresentador visivel e ele ficar pequeno demais para reconhecer; sem apresentador, false
- rosto_cortado: true somente se houver rosto visivel cortado pela borda; sem rosto, false
- faixa_broll_vazia: false em todos os frames, pois a Forma D nao tem faixa de b-roll por design; marque true apenas se a edicao acrescentou uma faixa, painel ou moldura artificial que ficou vazia
- broll_deformado: true somente se a imagem principal estiver esticada, girada, cortada de modo inutilizavel ou visualmente corrompida
- legenda_cobre_rosto: true se a legenda cobrir rosto, informacao central da tela ou estiver cortada; legenda legivel no terco inferior deve ser false
- faixa_gancho_estoura: SO no frame de gancho dos 3 primeiros segundos, true se a headline tiver mais de 2 linhas, estourar a area segura ou encostar nas bordas; nos demais frames, false
No resumo confirme que a peca permanece em tela cheia e diga se a headline dos 3 primeiros segundos esta legivel e dentro da area segura. Nao cobre b-roll nem apoio: eles nao existem nesta forma. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. Na duvida ou problema leve, false e cite em "obs".
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
elif AUDIT_MODE == "split_no_hook":
    PROMPT = f"""Voce audita a COMPOSICAO de um video vertical 9:16 em split-screen 50/50 CONTINUO: apresentador na metade superior e slides narrativos na metade inferior.
Esta peca NAO tem gancho separado, CTA, b-roll de IA ou tela cheia. Portanto o frame de 1s e um frame comum do corpo, e `faixa_gancho_estoura` deve ser false em todos os frames.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Para CADA frame responda booleans:
- teto_morto: ar vazio acima da cabeca MAIOR que a altura da propria cabeca
- enquadramento_frouxo: apresentador pequeno no quadro, sobrando ar em cima E nas laterais
- rosto_cortado: rosto/cabeca cortados pela borda
- faixa_broll_vazia: true SOMENTE se a metade inferior estiver literalmente sem titulo, texto, card, diagrama ou outro elemento narrativo. Fundo preto faz parte da identidade e NAO significa vazio quando ha qualquer elemento legivel
- broll_deformado: true se o slide inferior estiver quebrado, ilegivel, cortado ou deformado
- legenda_cobre_rosto: true se a legenda cobrir olhos, nariz, boca ou centro do rosto; legenda sobre a camiseta/torax e correta e deve ser false
- faixa_gancho_estoura: false em todos os frames, pois nao existe faixa de gancho nesta peca
Confirme no resumo se o split 50/50 permanece estavel, com apresentador em cima e slide embaixo. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. Na duvida ou problema leve, false e cite em "obs".
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""
else:
    PROMPT = f"""Voce audita a COMPOSICAO de um reels 9:16 (apresentador em cima, faixa de b-roll 16:9 no rodape).
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Frame de GANCHO: {gancho or 'nenhum'}. Frame de CTA: {cta}.
Para CADA frame responda booleans:
- teto_morto: ar vazio acima da cabeca MAIOR que a altura da propria cabeca
- enquadramento_frouxo: apresentador pequeno no quadro, sobrando ar em cima E nas laterais
- rosto_cortado: rosto/cabeca cortados pela borda
- faixa_broll_vazia: faixa inferior ausente, preta, borrada, esticada ou mal preenchida (no gancho e no CTA a faixa NAO existe por design: marque false)
- broll_deformado: membro/rosto/texto deformado no b-roll (erro de IA)
- legenda_cobre_rosto: legenda sobre o rosto do apresentador
- faixa_gancho_estoura: SO no frame de gancho, faixa de texto com mais de 2 linhas ou fora do terco inferior (nos demais: false)
CALIBRACAO: marque true SO para problema CLARAMENTE visivel. Na duvida ou problema leve, false e cite em "obs".
Use exatamente os nomes de arquivo da lista no campo "arquivo". Responda SOMENTE o JSON pedido."""

# JSON Schema estrito: --output-schema forca o formato (melhor que parsear texto)
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["frames", "resumo"],
    "properties": {
        "frames": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["arquivo", "teto_morto", "enquadramento_frouxo", "rosto_cortado",
                             "faixa_broll_vazia", "broll_deformado", "legenda_cobre_rosto",
                             "faixa_gancho_estoura", "obs"],
                "properties": {
                    "arquivo": {"type": "string"},
                    "teto_morto": {"type": "boolean"},
                    "enquadramento_frouxo": {"type": "boolean"},
                    "rosto_cortado": {"type": "boolean"},
                    "faixa_broll_vazia": {"type": "boolean"},
                    "broll_deformado": {"type": "boolean"},
                    "legenda_cobre_rosto": {"type": "boolean"},
                    "faixa_gancho_estoura": {"type": "boolean"},
                    "obs": {"type": "string"},
                },
            },
        },
        "resumo": {"type": "string"},
    },
}

def visao():
    schema_path = os.path.join(AUD, "audit_schema.json")
    json.dump(SCHEMA, open(schema_path, "w"))
    last_path = os.path.join(AUD, "audit_last.json")
    # -i por frame; --output-schema forca JSON; --output-last-message captura so a resposta final.
    # O prompt vai por STDIN, nao posicional: -i e variadico (--image FILE...) e engoliria o
    # prompt posicional como se fosse mais uma imagem (a CLI entao acha o prompt vazio).
    args = [CODEX, "exec", "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox",
            "-m", AUDIT_MODEL, "--output-schema", schema_path, "--output-last-message", last_path]
    for f in frames:
        args += ["-i", f]
    p = subprocess.run(args, input=PROMPT, capture_output=True, text=True, timeout=420)
    raw = ""
    if os.path.exists(last_path):
        raw = open(last_path).read().strip()
    if not raw:
        raw = (p.stdout or "").strip()
    if not raw:
        raise RuntimeError((p.stderr or "").strip()[-300:] or f"{CODEX} nao devolveu resposta")
    limpo = re.sub(r"^```(json)?|```$", "", raw.strip(), flags=re.M).strip()
    v = json.loads(limpo)
    if "frames" not in v or not isinstance(v["frames"], list):
        raise RuntimeError("visao devolveu JSON sem lista 'frames'")
    return v

try:
    v = visao()
except Exception as e:
    # degradacao HONESTA: entrega existe pelo mosaico, mas SEM selo de auditado
    json.dump({"status": "indisponivel", "erro": str(e)[:300], "mosaico": MOSAICO if _mos_ok else None,
               "mp4": SRC, "decode_ok": decode_ok, "n_frames": len(frames), "audited_at": time.time()},
              open(os.path.join(AUD, "veredito.json"), "w"), indent=1)
    print(f"AUDIT INDISPONIVEL ({str(e)[:120]})  mosaico={MOSAICO if _mos_ok else 'FALHOU'}"); sys.exit(2)

# ---- 6. decisao: hard = 1 frame basta; soft = precisa de 2+ (anti-falso-positivo) ----
HARD = ["rosto_cortado", "legenda_cobre_rosto", "faixa_gancho_estoura"]
SOFT = ["teto_morto", "enquadramento_frouxo", "faixa_broll_vazia", "broll_deformado"]
probs = []
for flag in HARD:
    hit = [fr.get("arquivo", "?") for fr in v["frames"] if fr.get(flag)]
    if hit:
        probs.append(f"{flag}: {', '.join(hit)}")
for flag in SOFT:
    hit = [fr.get("arquivo", "?") for fr in v["frames"] if fr.get(flag)]
    if len(hit) >= 2:
        probs.append(f"{flag}: {', '.join(hit)}")
if not decode_ok:
    probs.append("decodificacao com erros (ver audit/decode_errors.txt)")
veredito = "REPROVA" if probs else "PASSA"

# Reconciliacao com a tabela de verbos: o JSON e o relatorio dizem a mesma coisa.
pend_verbos = _pendencias_dos_verbos(VERBOS)
if pend_verbos:
    probs = probs + [f"verbo do pedido nao feito: {p['verbo']} ({p['motivo_medido']})" for p in pend_verbos]
    if veredito == "PASSA":
        veredito = "PASSA_COM_PENDENCIA"

json.dump({"status": veredito, "problemas": probs, "verbos": VERBOS, "pendencias_de_verbo": pend_verbos, "resumo": v.get("resumo", ""), "frames": v["frames"],
           "decode_ok": decode_ok, "n_frames": len(frames), "mosaico": MOSAICO if _mos_ok else None,
           "mp4": SRC, "mp4_mtime": os.path.getmtime(SRC), "audited_at": time.time()},
          open(os.path.join(AUD, "veredito.json"), "w"), indent=1)
print(f"AUDIT {veredito}  frames={len(frames)}  decode={'ok' if decode_ok else 'ERRO'}  mosaico={MOSAICO}"
      + "".join("\n  - " + p for p in probs))
sys.exit(0 if veredito in ("PASSA", "PASSA_COM_PENDENCIA") else 1)
