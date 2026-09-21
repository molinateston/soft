import asyncio, base64, os, re
from pathlib import Path
from playwright.async_api import async_playwright

# Identidade e caminhos vem do ambiente (onboarding da skill), nunca cravados aqui.
#   PERFIL_NOME / PERFIL_HANDLE / PERFIL_AVATAR / SAIDA_DIR
SKILL_DIR = Path(__file__).resolve().parent.parent
NOME = os.environ.get("PERFIL_NOME", "<nome do dono>")
HANDLE = os.environ.get("PERFIL_HANDLE", "@handle")
_AVATAR = os.environ.get("PERFIL_AVATAR", "")

if _AVATAR and os.path.isfile(_AVATAR):
    with open(_AVATAR, 'rb') as f:
        AVATAR_B64 = base64.b64encode(f.read()).decode()
else:
    AVATAR_B64 = ""
    print("aviso: sem PERFIL_AVATAR valido, o cabecalho sai com placeholder (rascunho)")

def exigir_saida_dir():
    """SAIDA_DIR e obrigatoria: o script nunca escreve dentro da pasta da skill.

    Resolvida na hora de escrever, pra que importar os frames (frame_thread,
    frame_quote, frame_poll, frame_chat) continue funcionando sem a variavel.
    """
    valor = os.environ.get("SAIDA_DIR", "").strip()
    if not valor:
        raise SystemExit(
            "ERRO: SAIDA_DIR e obrigatoria.\n"
            "Este script nao escreve dentro da pasta da skill. Aponte uma pasta de\n"
            "saida do dono antes de rodar. Exemplo:\n"
            "  SAIDA_DIR=./saida-tweet-card PERFIL_NOME=\"<nome>\" "
            "PERFIL_HANDLE=\"@<handle>\" \\\n"
            "    PERFIL_AVATAR=./avatar.png python3 scripts/build_frames.py"
        )
    caminho = Path(valor).expanduser().resolve()
    if caminho == SKILL_DIR or SKILL_DIR in caminho.parents:
        raise SystemExit(
            f"ERRO: SAIDA_DIR aponta pra dentro da pasta da skill ({caminho}).\n"
            "Escolha uma pasta fora de "
            f"{SKILL_DIR}."
        )
    os.makedirs(caminho, exist_ok=True)
    return str(caminho)
VERIFIED = "#1D9BF0"

THEMES = {
    "dark": dict(
        BG="#0A0A0A", TEXT="#F5F2EC", MUTED="#8A8580", KW="#4ade80",
        BODYBG="#1a1a1a",
        QUOTE_BG="#111111", QUOTE_BORDER="#262626",
        POLL_BARBG="#1c1c1c", POLL_FILL="rgba(74,222,128,0.22)",
        BUBBLE_IN_BG="#1c1c1c", BUBBLE_IN_TXT="#F5F2EC",
        BUBBLE_OUT_BG="#123a22", BUBBLE_OUT_TXT="#F5F2EC",
        THREAD_LINE="#2a2a2a",
    ),
    # BG do tema claro: off-white padrão. Branco puro só quando o dono pedir
    # branco puro; cor declarada pelo dono sobrescreve este default.
    "light": dict(
        BG=os.environ.get("TEMA_CLARO_BG", "#F7F9F9"),
        TEXT="#0F1419", MUTED="#536471", KW="#15803d",
        BODYBG="#EFF3F4",
        QUOTE_BG="#F7F9F9", QUOTE_BORDER="#E1E8ED",
        POLL_BARBG="#EFF3F4", POLL_FILL="rgba(21,128,61,0.16)",
        BUBBLE_IN_BG="#EFF3F4", BUBBLE_IN_TXT="#0F1419",
        BUBBLE_OUT_BG="#D3F3DE", BUBBLE_OUT_TXT="#0F1419",
        THREAD_LINE="#E1E8ED",
    ),
}

def no_orphan(text):
    if not text:
        return text
    stripped = text.rstrip()
    trailing = text[len(stripped):]
    if ' ' not in stripped:
        return text
    head, tail = stripped.rsplit(' ', 1)
    return head + '&nbsp;' + tail + trailing

def rp_money(text):
    return re.sub(r'R\$\s+[\d.,]+(?:\s+\w+)?', lambda m: m.group(0).replace(' ', '&nbsp;'), text)

def kw_wrap(text, kw):
    if kw and kw in text:
        text = text.replace(kw, f'<span class="kw">{kw}</span>')
    return text

def txt(s, kw=None):
    s = no_orphan(s)
    s = rp_money(s)
    if kw:
        s = kw_wrap(s, kw)
    return s

def head_style(t):
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  width:1080px; height:1350px;
  background:{t['BODYBG']};
  display:flex; align-items:center; justify-content:center;
  font-family: -apple-system, 'Inter', 'Helvetica Neue', Arial, sans-serif;
}}
.card {{
  width:1080px; height:1350px;
  background:{t['BG']};
  padding:100px;
  display:flex;
  flex-direction:column;
  justify-content:flex-start;
  position:relative;
  overflow:hidden;
}}
.autor {{ display:flex; align-items:center; gap:20px; }}
.avatar {{ width:88px; height:88px; border-radius:50%; flex-shrink:0; overflow:hidden; position:relative; z-index:1; }}
.avatar img {{ width:100%; height:100%; object-fit:cover; }}
.autor-info {{ display:flex; flex-direction:column; justify-content:center; }}
.nome-linha {{ display:flex; align-items:center; gap:8px; }}
.nome {{ font-size:32px; font-weight:700; color:{t['TEXT']}; line-height:1.2; }}
.selo {{ width:26px; height:26px; flex-shrink:0; }}
.handle {{ font-size:26px; font-weight:400; color:{t['MUTED']}; margin-top:4px; }}
.corpo {{ font-size:54px; font-weight:400; line-height:1.35; color:{t['TEXT']}; }}
.corpo.tight {{ font-size:46px; }}
.kw {{ font-weight:800; color:{t['KW']}; }}
.divider {{ width:120px; height:6px; background:{t['KW']}; margin:44px 0; }}

/* THREAD */
.thread-wrap {{ position:relative; }}
.thread-line {{ position:absolute; left:44px; top:108px; bottom:0; width:3px; background:{t['THREAD_LINE']}; z-index:0; }}
.thread-item {{ position:relative; z-index:1; }}
.thread-item .autor {{ margin-bottom:28px; }}
.thread-first .corpo {{ padding-left:108px; }}
.thread-second {{ margin-top:44px; padding-left:108px; }}
.thread-second .corpo {{ color:{t['MUTED']}; }}

/* QUOTE */
.quote-card {{
  background:{t['QUOTE_BG']}; border:2px solid {t['QUOTE_BORDER']}; border-radius:20px;
  padding:36px; margin-top:40px;
}}
.quote-autor {{ font-size:26px; color:{t['MUTED']}; margin-bottom:16px; font-weight:600; }}
.quote-corpo {{ font-size:38px; line-height:1.4; color:{t['MUTED']}; }}

/* KPI */
.kpi-num {{ font-size:128px; font-weight:800; color:{t['KW']}; line-height:1.05; text-align:left; margin:40px 0; white-space:nowrap; }}
.kpi-num.small {{ font-size:100px; }}

/* POLL */
.poll {{ margin-top:44px; display:flex; flex-direction:column; gap:24px; }}
.poll-opt {{ position:relative; }}
.poll-bar-bg {{ background:{t['POLL_BARBG']}; border-radius:10px; overflow:hidden; height:88px; position:relative; }}
.poll-bar-fill {{ background:{t['POLL_FILL']}; border-left:5px solid {t['KW']}; height:100%; position:absolute; left:0; top:0; }}
.poll-opt-text {{ position:absolute; left:28px; top:0; height:100%; display:flex; align-items:center; font-size:36px; color:{t['TEXT']}; z-index:2; font-weight:600; }}
.poll-opt-pct {{ position:absolute; right:28px; top:0; height:100%; display:flex; align-items:center; font-size:36px; color:{t['TEXT']}; z-index:2; font-weight:800; }}
.poll-votes {{ font-size:26px; color:{t['MUTED']}; margin-top:24px; }}

/* CHAT */
.chat {{ margin-top:44px; display:flex; flex-direction:column; gap:26px; }}
.bubble {{ max-width:78%; padding:26px 32px; border-radius:28px; font-size:34px; line-height:1.35; align-self:flex-start; }}
.bubble-in {{ background:{t['BUBBLE_IN_BG']}; color:{t['BUBBLE_IN_TXT']}; border-bottom-left-radius:8px; }}
.bubble-out {{ background:{t['BUBBLE_OUT_BG']}; color:{t['BUBBLE_OUT_TXT']}; align-self:flex-end; border-bottom-right-radius:8px; }}
"""

def avatar_img(t):
    if AVATAR_B64:
        return f'<img src="data:image/png;base64,{AVATAR_B64}">'
    inicial = (NOME.strip() or "?")[0].upper()
    return (f'<div style="width:100%;height:100%;display:flex;align-items:center;'
            f'justify-content:center;background:{t["BG"]};color:{t["MUTED"]};'
            f'font-size:44px;font-weight:800;">{inicial}</div>')

def avatar_header(t, small=False):
    scale = "transform:scale(0.86); transform-origin:left center;" if small else ""
    return f"""
    <div class="autor" style="{scale}">
      <div class="avatar">{avatar_img(t)}</div>
      <div class="autor-info">
        <div class="nome-linha">
          <span class="nome">{NOME}</span>
          <svg class="selo" viewBox="0 0 24 24" fill="{VERIFIED}">
            <path d="M12 1l2.4 1.8 3-.5 1.1 2.8 2.8 1.1-.5 3L23 12l-1.8 2.4.5 3-2.8 1.1-1.1 2.8-3-.5L12 23l-2.4-1.8-3 .5-1.1-2.8-2.8-1.1.5-3L1 12l1.8-2.4-.5-3 2.8-1.1L6.4 2.3l3 .5L12 1z"/>
            <path d="M9.5 12.5l1.8 1.8 3.7-4.1" stroke="{t['BG']}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="handle">{HANDLE}</div>
      </div>
    </div>
    """

def wrap(inner, t):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{head_style(t)}</style></head>
<body><div class="card">{inner}</div></body></html>"""

# 1. THREAD: cabecalho UMA vez so; segundo tweet so texto, conectado pela linha
def frame_thread(t):
    inner = f"""
    <div class="thread-wrap">
      <div class="thread-line"></div>
      <div class="thread-item thread-first">
        {avatar_header(t)}
        <div class="corpo" style="padding-left:108px; margin-top:28px;">
          {txt("Agência cobra R$ mil pra fazer o que você mesmo pilota com IA hoje.", "IA")}
        </div>
      </div>
      <div class="thread-second">
        <div class="corpo tight">
          {txt("E o melhor: você não larga o controle, só larga o trabalho braçal…", "controle")}
        </div>
      </div>
    </div>
    """
    return wrap(inner, t)

# 2. QUOTE / CITACAO
def frame_quote(t):
    inner = f"""
    {avatar_header(t)}
    <div class="corpo" style="margin-top:44px;">
      {txt("Tem gente vendendo isso como se fosse mágico. Não é. É pilotar.", "pilotar")}
    </div>
    <div class="quote-card">
      <div class="quote-autor">@mentor.generico</div>
      <div class="quote-corpo">
        {txt("A IA vai substituir todo mundo que trabalha com marketing digital.")}
      </div>
    </div>
    """
    return wrap(inner, t)

# 3. KPI / NUMERO
def frame_kpi(t):
    inner = f"""
    {avatar_header(t)}
    <div class="corpo tight" style="margin-top:40px;">
      {txt("Um aluno meu roda a operação inteira sozinho e fatura", None)}
    </div>
    <div class="kpi-num">R$&nbsp;15,5&nbsp;mil</div>
    <div class="corpo tight">
      {txt("a menos por mês do que pagava de agência, com o mesmo resultado.", "mesmo resultado")}
    </div>
    """
    return wrap(inner, t)

# 4. ENQUETE / POLL
def frame_poll(t):
    opts = [
        ("Quase tudo", 42),
        ("Metade", 31),
        ("Quase nada", 18),
        ("Nada ainda", 9),
    ]
    bars = ""
    for label, pct in opts:
        bars += f"""
        <div class="poll-opt">
          <div class="poll-bar-bg">
            <div class="poll-bar-fill" style="width:{pct}%;"></div>
            <div class="poll-opt-text">{no_orphan(label)}</div>
            <div class="poll-opt-pct">{pct}%</div>
          </div>
        </div>
        """
    inner = f"""
    {avatar_header(t)}
    <div class="corpo" style="margin-top:44px;">
      {txt("Quanto do teu operacional já roda sem você precisar tocar?", "operacional")}
    </div>
    <div class="poll">{bars}</div>
    <div class="poll-votes">2.847 votos</div>
    """
    return wrap(inner, t)

# 5. CONVERSA / DM
def frame_chat(t):
    inner = f"""
    {avatar_header(t)}
    <div class="corpo tight" style="margin-top:36px;">
      {txt("Print de uma DM que recebo direto:")}
    </div>
    <div class="chat">
      <div class="bubble bubble-in">{txt("Contratar agência ainda vale a pena ou dá pra fazer sozinho?")}</div>
      <div class="bubble bubble-out">{txt("Dá. O que falta não é habilidade, é saber pilotar a IA certa pra cada etapa.", "pilotar")}</div>
      <div class="bubble bubble-in">{txt("E se eu nunca programei na vida?")}</div>
      <div class="bubble bubble-out">{txt("Não precisa. Você comanda, a IA executa.")}</div>
    </div>
    """
    return wrap(inner, t)

FRAME_BUILDERS = [
    ("frame-1-thread", frame_thread),
    ("frame-2-citacao", frame_quote),
    ("frame-3-numero", frame_kpi),
    ("frame-4-enquete", frame_poll),
    ("frame-5-conversa", frame_chat),
]

async def render(html, out_path, page):
    await page.set_content(html)
    await page.wait_for_timeout(150)
    await page.screenshot(path=out_path)

async def build_mosaic(page, paths, out_path):
    def b64img(p):
        with open(p, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    imgs = "".join(f'<img src="data:image/png;base64,{b64img(p)}">' for p in paths)
    html = f"""<!DOCTYPE html><html><head><style>
    * {{ margin:0; padding:0; }}
    body {{ display:flex; background:#000; }}
    img {{ width:432px; height:540px; display:block; }}
    </style></head><body>{imgs}</body></html>"""
    await page.set_viewport_size({"width": 432*5, "height": 540})
    await page.set_content(html)
    await page.wait_for_timeout(150)
    await page.screenshot(path=out_path)

async def main():
    OUTDIR = exigir_saida_dir()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=2)

        outputs = {"dark": [], "light": []}
        for theme_name, t in THEMES.items():
            for slug, builder in FRAME_BUILDERS:
                out = f"{OUTDIR}/{slug}-{theme_name}.png"
                await render(builder(t), out, page)
                outputs[theme_name].append(out)
                print("rendered", out)

        for theme_name in ("dark", "light"):
            mosaic_out = f"{OUTDIR}/mosaico-{theme_name}.png"
            await build_mosaic(page, outputs[theme_name], mosaic_out)
            print("rendered", mosaic_out)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
