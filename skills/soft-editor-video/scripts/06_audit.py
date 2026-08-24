"""Auditoria VISUAL do MP4 final: extrai frames, monta mosaico (prova pro dono)
e pergunta pro codex OAuth (conta ChatGPT) se a composicao esta certa. OLHOS REAIS, ZERO API paga.

O motor do LEON (codex exec, texto puro) NAO ve imagem. Sem este passo, qualquer
"12/12 frames conferidos" e alucinacao de conformidade. Aqui a alegacao vira medicao.

Uso: python3 06_audit.py final.mp4 [pasta_audit] [N] [marcos_csv]
  marcos_csv: timestamps de transicao (fim do gancho, inicio do CTA), ex: "6.2,52.0"
Exit: 0=PASSA . 1=REPROVA . 2=AUDITORIA INDISPONIVEL (visao falhou; mosaico existe mesmo assim)
"""
import subprocess, os, sys, json, time, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _config as C

if len(sys.argv) < 2:
    print("uso: python3 06_audit.py final.mp4 [pasta_audit] [N] [marcos_csv]"); sys.exit(2)

# Visao pelo codex OAuth (conta ChatGPT) — NAO exige OPENAI_API_KEY (nada de API paga).
SRC = os.path.abspath(sys.argv[1])
if not os.path.exists(SRC):
    print(f"AUDIT INDISPONIVEL: MP4 nao existe: {SRC}"); sys.exit(2)
AUD = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(C.OUTPUT_DIR, "audit")
N = int(sys.argv[3]) if len(sys.argv) > 3 else 12
MARCOS = [float(x) for x in sys.argv[4].split(",") if x.strip()] if len(sys.argv) > 4 else []
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
    _fail(f"duracao invalida ({D}s) — MP4 corrompido ou vazio?", 2)

# ---- 1. timestamps: gancho(1s) + CTA(D-2) + marcos+0.8 (NUNCA no meio do xfade) + uniforme ----
ts = {1.0, max(0.5, D - 2.0)} | {min(D - 1.0, m + 0.8) for m in MARCOS}
i = 0
while len(ts) < N and i < N * 3:
    ts.add(round(2.0 + (D - 5.0) * (i + 0.5) / N, 2)); i += 1
TS = sorted(t for t in ts if 0.2 <= t <= D - 0.2)[:N]

# ---- 2. extrai frames (768 de largura, ts queimado pra o codex referenciar) ----
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

# ---- 3. mosaico (a PROVA pro Telegram; existe mesmo se a visao cair) ----
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

# ---- 5. VISAO via codex OAuth (-i FILE...), JSON estrito por --output-schema ----
# VISAO PELO CODEX OAUTH (conta ChatGPT, ZERO API paga). O codex exec ve imagem
# nativamente via -i FILE... (17/08 Leo: "100% na conta oauth, nada de credito openai").
# O motor do LEON e cego SO porque o bridge nunca passava -i; aqui passamos os frames.
CODEX = "codex"
AUDIT_MODE = os.environ.get("SOFT_EDITOR_AUDIT_MODE", "standard").strip().lower()
_gancho_files = [os.path.basename(f) for f in frames if "_t1.0.jpg" in f]
gancho = ", ".join(_gancho_files)
cta = os.path.basename(frames[-1])
_lista = "\n".join(f"  {i+1}. {os.path.basename(f)}" for i, f in enumerate(frames))
if AUDIT_MODE == "feed_plain":
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
    PROMPT = f"""Voce audita a COMPOSICAO de uma APRESENTACAO VERTICAL 9:16 que alterna tres estados de tela inteira: take do apresentador, slide narrativo e prova real do Telegram. NAO existe faixa de b-roll e NAO deve existir layout dividido permanente.
Recebeu {len(frames)} frames em ordem cronologica (t= queimado no canto superior esquerdo), nesta ordem:
{_lista}
Frame inicial: {gancho or 'nenhum'}. Frame final: {cta}.
Para CADA frame responda booleans usando estes campos legados:
- teto_morto: true SOMENTE em take do apresentador quando o ar vazio acima da cabeca for MAIOR que a altura da propria cabeca; em slide/prova, false
- enquadramento_frouxo: true SOMENTE em take do apresentador pequeno, com sobra clara em cima E laterais; em slide/prova, false
- rosto_cortado: true se rosto, topo da cabeca ou queixo estiverem cortados; em slide/prova, false
- faixa_broll_vazia: neste modo, true se houver split-screen constante, apresentador espremido ou Telegram usado como rodape pequeno; false para take, slide e prova que ocupam o canvas inteiro
- broll_deformado: neste modo, true se slide estiver quebrado/deformado OU se a prova real do Telegram estiver pequena/ilegivel; false nos takes do apresentador
- legenda_cobre_rosto: true se qualquer texto cobrir o rosto do apresentador
- faixa_gancho_estoura: false em todos os frames; esta peca nao usa faixa de gancho
Confirme no resumo se ha alternancia clara entre apresentador, slides narrativos de tela inteira e prova real do Telegram em tela inteira. CALIBRACAO: marque true SO para problema CLARAMENTE visivel. Na duvida ou problema leve, false e cite em "obs".
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

# JSON Schema estrito: o codex --output-schema forca o formato (melhor que parsear texto)
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
    # prompt posicional como se fosse mais uma imagem (o codex entao acha o prompt vazio).
    args = [CODEX, "exec", "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox",
            "-m", "gpt-5.6-terra", "--output-schema", schema_path, "--output-last-message", last_path]
    for f in frames:
        args += ["-i", f]
    p = subprocess.run(args, input=PROMPT, capture_output=True, text=True, timeout=420)
    raw = ""
    if os.path.exists(last_path):
        raw = open(last_path).read().strip()
    if not raw:
        raw = (p.stdout or "").strip()
    if not raw:
        raise RuntimeError((p.stderr or "").strip()[-300:] or "codex exec nao devolveu resposta")
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

json.dump({"status": veredito, "problemas": probs, "resumo": v.get("resumo", ""), "frames": v["frames"],
           "decode_ok": decode_ok, "n_frames": len(frames), "mosaico": MOSAICO if _mos_ok else None,
           "mp4": SRC, "mp4_mtime": os.path.getmtime(SRC), "audited_at": time.time()},
          open(os.path.join(AUD, "veredito.json"), "w"), indent=1)
print(f"AUDIT {veredito}  frames={len(frames)}  decode={'ok' if decode_ok else 'ERRO'}  mosaico={MOSAICO}"
      + "".join("\n  - " + p for p in probs))
sys.exit(0 if veredito == "PASSA" else 1)
