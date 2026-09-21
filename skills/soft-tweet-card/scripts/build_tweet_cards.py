import asyncio, base64, re, os
from pathlib import Path
from playwright.async_api import async_playwright

# Identidade e caminhos vem do ambiente (onboarding da skill), nunca cravados aqui.
#   PERFIL_NOME   nome de exibicao do dono, como ele escreve
#   PERFIL_HANDLE handle do perfil, com arroba
#   PERFIL_AVATAR caminho do PNG do avatar (quadrado)
#   SAIDA_DIR     pasta de saida dos renders
SKILL_DIR = Path(__file__).resolve().parent.parent
NOME = os.environ.get("PERFIL_NOME", "<nome do dono>")
HANDLE = os.environ.get("PERFIL_HANDLE", "@handle")
AVATAR = os.environ.get("PERFIL_AVATAR", "")

if AVATAR and os.path.isfile(AVATAR):
    with open(AVATAR, 'rb') as f:
        AVATAR_B64 = base64.b64encode(f.read()).decode()
else:
    AVATAR_B64 = ""  # sem avatar real a peca sai como rascunho
    print("aviso: sem PERFIL_AVATAR valido, o cabecalho sai com placeholder (rascunho)")

def exigir_saida_dir():
    """SAIDA_DIR e obrigatoria: o script nunca escreve dentro da pasta da skill."""
    valor = os.environ.get("SAIDA_DIR", "").strip()
    if not valor:
        raise SystemExit(
            "ERRO: SAIDA_DIR e obrigatoria.\n"
            "Este script nao escreve dentro da pasta da skill. Aponte uma pasta de\n"
            "saida do dono antes de rodar. Exemplo:\n"
            "  SAIDA_DIR=./saida-tweet-card PERFIL_NOME=\"<nome>\" "
            "PERFIL_HANDLE=\"@<handle>\" \\\n"
            "    PERFIL_AVATAR=./avatar.png python3 scripts/build_tweet_cards.py"
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

T = dict(BG="#0A0A0A", TEXT="#F5F2EC", MUTED="#8A8580", KW="#4ade80",
         BODYBG="#1a1a1a", CHIP_BG="#111111", CHIP_BORDER="#262626")

def no_orphan(text):
    if not text: return text
    st = text.rstrip(); tr = text[len(st):]
    if ' ' not in st: return text
    head, tail = st.rsplit(' ', 1)
    return head + '&nbsp;' + tail + tr

def rp_money(text):
    return re.sub(r'R\$\s+[\d.,]+(?:\s+\w+)?', lambda m: m.group(0).replace(' ', '&nbsp;'), text)

def kw_once(text, kw):
    if not kw:
        return text
    pattern = r'(?:\s|&nbsp;)+'.join(re.escape(p) for p in kw.split(' '))
    m = re.search(pattern, text)
    if not m:
        return text
    return text[:m.start()] + f'<span class="kw">{m.group(0)}</span>' + text[m.end():]

def para(s, kw=None):
    # s pode ter \n\n separando paragrafos; kw destaca a 1a ocorrencia onde ela aparecer
    out = []
    done = False
    for p in s.split("\n\n"):
        p = no_orphan(p); p = rp_money(p)
        if kw and not done:
            new = kw_once(p, kw)
            if new != p:
                done = True
            p = new
        out.append(f'<p>{p}</p>')
    return "".join(out)

def fs(chars, base):
    # fonte adaptativa por comprimento
    if chars <= 90:  return base
    if chars <= 170: return base - 6
    if chars <= 280: return base - 14
    if chars <= 400: return base - 20
    return base - 26

def head_style(corpo_fs):
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; background:{T['BODYBG']};
  display:flex; align-items:center; justify-content:center;
  font-family:-apple-system,'Inter','Helvetica Neue',Arial,sans-serif; }}
.card {{ width:1080px; height:1350px; background:{T['BG']}; padding:96px 92px;
  display:flex; flex-direction:column; justify-content:flex-start; position:relative; overflow:hidden; }}
.autor {{ display:flex; align-items:center; gap:20px; margin-bottom:52px; }}
.avatar {{ width:96px; height:96px; border-radius:50%; flex-shrink:0; overflow:hidden; }}
.avatar img {{ width:100%; height:100%; object-fit:cover; }}
.autor-info {{ display:flex; flex-direction:column; justify-content:center; }}
.nome-linha {{ display:flex; align-items:center; gap:9px; }}
.nome {{ font-size:34px; font-weight:700; color:{T['TEXT']}; line-height:1.2; }}
.selo {{ width:28px; height:28px; flex-shrink:0; }}
.handle {{ font-size:27px; font-weight:400; color:{T['MUTED']}; margin-top:5px; }}
.corpo {{ font-size:{corpo_fs}px; font-weight:400; line-height:1.4; color:{T['TEXT']}; }}
.corpo p {{ margin-bottom:0.7em; }}
.corpo p:last-child {{ margin-bottom:0; }}
.corpo.big {{ font-weight:500; }}
.kw {{ font-weight:800; color:{T['KW']}; }}
.kpi-num {{ font-size:150px; font-weight:800; color:{T['KW']}; line-height:1.02; margin:40px 0; white-space:nowrap; }}
.chips {{ display:flex; flex-direction:column; gap:22px; margin:38px 0; }}
.chip {{ background:{T['CHIP_BG']}; border:2px solid {T['CHIP_BORDER']}; border-radius:18px;
  padding:26px 32px; font-size:38px; line-height:1.32; color:{T['TEXT']}; }}
.chip b {{ color:{T['KW']}; font-weight:800; }}
.footer {{ position:absolute; left:92px; bottom:56px; font-size:26px; color:{T['MUTED']}; }}
"""

def avatar_img():
    if AVATAR_B64:
        return f'<img src="data:image/png;base64,{AVATAR_B64}">'
    inicial = (NOME.strip() or "?")[0].upper()
    return (f'<div style="width:100%;height:100%;display:flex;align-items:center;'
            f'justify-content:center;background:{T["CHIP_BG"]};color:{T["MUTED"]};'
            f'font-size:44px;font-weight:800;">{inicial}</div>')

def header():
    return f"""
    <div class="autor">
      <div class="avatar">{avatar_img()}</div>
      <div class="autor-info">
        <div class="nome-linha">
          <span class="nome">{NOME}</span>
          <svg class="selo" viewBox="0 0 24 24" fill="{VERIFIED}">
            <path d="M12 1l2.4 1.8 3-.5 1.1 2.8 2.8 1.1-.5 3L23 12l-1.8 2.4.5 3-2.8 1.1-1.1 2.8-3-.5L12 23l-2.4-1.8-3 .5-1.1-2.8-2.8-1.1.5-3L1 12l1.8-2.4-.5-3 2.8-1.1L6.4 2.3l3 .5L12 1z"/>
            <path d="M9.5 12.5l1.8 1.8 3.7-4.1" stroke="{T['BG']}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="handle">{HANDLE}</div>
      </div>
    </div>"""

def wrap(inner, corpo_fs):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{head_style(corpo_fs)}</style></head>
<body><div class="card">{header()}{inner}</div></body></html>"""

def slide_texto(s, kw=None, big=False):
    cls = "corpo big" if big else "corpo"
    inner = f'<div class="{cls}">{para(s, kw)}</div>'
    return wrap(inner, fs(len(s), 60 if big else 52))

def slide_kpi(before, num, after, kw=None):
    inner = f"""
    <div class="corpo">{para(before)}</div>
    <div class="kpi-num">{num.replace(' ','&nbsp;')}</div>
    <div class="corpo">{para(after, kw)}</div>"""
    return wrap(inner, fs(len(before)+len(after), 44))

def slide_chips(intro, chips, closing, kw=None):
    chip_html = "".join(f'<div class="chip"><b>{n}</b> {no_orphan(d)}</div>' for n, d in chips)
    inner = f"""
    <div class="corpo">{para(intro)}</div>
    <div class="chips">{chip_html}</div>
    <div class="corpo">{para(closing, kw)}</div>"""
    return wrap(inner, 40)

def slide_cta(s, kw="SÓCIO"):
    inner = f'<div class="corpo big">{para(s, kw)}</div><div class="footer">Comenta -&gt;</div>'
    return wrap(inner, fs(len(s), 54))

# ---------- CARROSSEIS ----------
# Banco de exemplo, FICTICIO, so pra exercitar os frames e o arco. Substitua pelo carrossel
# real do dono antes de renderizar qualquer peca de verdade: a copy nunca nasce aqui, ela
# chega pronta da skill de copy e este script so a veste no formato.
CARROSSEIS = {}

CARROSSEIS["exemplo-oficina-em-um-dia"] = [
    slide_texto("Montei a operacao de vendas de uma oficina mecanica do zero em um dia.\n\nNo primeiro mes ela pagou o proprio custo tres vezes.", kw="um dia", big=True),
    slide_texto("Uma oficina de bairro, uma agenda vazia e um dia de trabalho.\n\nNenhum curso no meio, nenhuma equipe contratada. So operacao montada."),
    slide_texto("De manha nao existia nada. Nem pagina, nem orcamento saindo, nem cliente conversando com ninguem.\n\nA noite, a oficina ja tinha operacao inteira no ar."),
    slide_texto("Primeiro passo: a pagina do servico.\n\nSubiu no mesmo dia. Sem briefing de uma semana, sem agencia, sem fila de aprovacao."),
    slide_texto("Segundo passo: o anuncio.\n\nO sistema montou e geriu a campanha. O primeiro pedido de orcamento entrou no mesmo dia.", kw="mesmo dia"),
    slide_texto("Terceiro passo: o atendimento.\n\nO pedido nao caiu numa planilha esperando alguem sobrar tempo. Foi atendido na hora: qualificou, tirou duvida, marcou a revisao."),
    slide_kpi("Resultado do primeiro mes.", "3x o custo", "de retorno, contando so as revisoes que entraram pela pagina nova."),
    slide_chips("Isso e operacao. Pagina, anuncio e atendimento rodaram como um sistema so.",
                [("Contexto", "guarda o que o negocio vende e por quanto."), ("Tarefas", "executam cada etapa."), ("Encadeamento", "liga uma na outra sozinho.")],
                "E o mecanismo por tras disso.", kw="mecanismo"),
    slide_cta("Comenta OPERACAO que eu te mostro como montei o contexto, as tarefas e o encadeamento dessa operacao."),
]

async def build_mosaic(page, paths, out_path):
    def b64(p):
        with open(p, 'rb') as f: return base64.b64encode(f.read()).decode()
    imgs = "".join(f'<img src="data:image/png;base64,{b64(p)}">' for p in paths)
    n = len(paths)
    cols = min(n, 5); rows = (n + cols - 1)//cols
    html = f"""<!DOCTYPE html><html><head><style>
    * {{margin:0;padding:0;box-sizing:border-box;}} body{{display:flex;flex-wrap:wrap;background:#000;width:{272*cols}px;}}
    img{{width:272px;height:340px;display:block;border:1px solid #222;}}
    </style></head><body>{imgs}</body></html>"""
    await page.set_viewport_size({"width": 272*cols, "height": 340*rows})
    await page.set_content(html)
    await page.wait_for_timeout(150)
    await page.screenshot(path=out_path)

async def main():
    ROOT = exigir_saida_dir()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=2)
        for slug, slides in CARROSSEIS.items():
            d = f"{ROOT}/{slug}"; os.makedirs(d, exist_ok=True)
            paths = []
            await page.set_viewport_size({"width":1080,"height":1350})
            fonte = f"{d}/_fonte"; os.makedirs(fonte, exist_ok=True)
            for i, html in enumerate(slides, 1):
                out = f"{d}/slide-{i:02d}.png"
                # o HTML de cada card fica no disco pro verificador contar o verde
                # de acento por card e conferir o cabeçalho sem depender do pixel
                with open(f"{fonte}/slide-{i:02d}.html", "w", encoding="utf-8") as fh:
                    fh.write(html)
                await page.set_content(html)
                await page.wait_for_timeout(120)
                await page.screenshot(path=out)
                paths.append(out); print("rendered", out)
            await build_mosaic(page, paths, f"{d}/_mosaico.png")
            print("mosaic", f"{d}/_mosaico.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
