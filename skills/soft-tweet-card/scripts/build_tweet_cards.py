import asyncio, base64, re, os
from playwright.async_api import async_playwright

AVATAR = "/tmp/lean-bridge/avatar-circle.png"
with open(AVATAR, 'rb') as f:
    AVATAR_B64 = base64.b64encode(f.read()).decode()

ROOT = "/home/cloud/trabalho/conteudo/2026-08/2026-08-13-carrosseis-banco-modelagem/render-tweet"
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

def header():
    return f"""
    <div class="autor">
      <div class="avatar"><img src="data:image/png;base64,{AVATAR_B64}"></div>
      <div class="autor-info">
        <div class="nome-linha">
          <span class="nome">Léo Molina</span>
          <svg class="selo" viewBox="0 0 24 24" fill="{VERIFIED}">
            <path d="M12 1l2.4 1.8 3-.5 1.1 2.8 2.8 1.1-.5 3L23 12l-1.8 2.4.5 3-2.8 1.1-1.1 2.8-3-.5L12 23l-2.4-1.8-3 .5-1.1-2.8-2.8-1.1.5-3L1 12l1.8-2.4-.5-3 2.8-1.1L6.4 2.3l3 .5L12 1z"/>
            <path d="M9.5 12.5l1.8 1.8 3.7-4.1" stroke="{T['BG']}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="handle">@instadoleomolina</div>
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
CARROSSEIS = {}

CARROSSEIS["01-imobiliaria-24h"] = [
    slide_texto("Montei uma operação de vendas do zero com IA em 24 horas.\n\nNo primeiro mês ela me deu mais de 10 mil reais.", kw="IA", big=True),
    slide_texto("Uma imobiliária, um empreendimento parado, e um dia de trabalho.\n\nNenhum curso no meio, nenhuma equipe contratada. Só operação montada."),
    slide_texto("De manhã eu não tinha nada. Nem página, nem lead, nem corretor conversando com ninguém.\n\nÀ noite, o empreendimento já tinha operação inteira no ar."),
    slide_texto("Primeiro passo: a página do empreendimento.\n\nSubiu no mesmo dia. Sem briefing de uma semana, sem agência, sem fila de aprovação."),
    slide_texto("Segundo passo: o tráfego.\n\nA IA montou e geriu a campanha. Não fiquei testando anúncio manualmente por três semanas. O lead começou a entrar no mesmo dia.", kw="IA"),
    slide_texto("Terceiro passo: o atendimento.\n\nO lead não caiu numa planilha esperando um corretor sobrar tempo. A IA atendeu na hora, como uma SDR: qualificou, tirou dúvida, e levou pra visita.", kw="IA"),
    slide_kpi("Resultado: visita marcada no mesmo mês.", "10 mil reais", "de comissão pra mim. Mais a comissão dos dois corretores que trabalharam comigo nesse empreendimento."),
    slide_chips("Isso é operação. Página, tráfego e atendimento rodaram como um sistema só.",
                [("Brain", "carrega o contexto do negócio."), ("Skills", "executam cada tarefa."), ("Orquestração", "encadeia tudo sozinha.")],
                "É isso que chamo de Sócio IA.", kw="Sócio IA"),
    slide_cta("Comenta SÓCIO que eu te mostro como montei o Brain, as Skills e a Orquestração dessa operação."),
]

CARROSSEIS["02-orquestra-ferramentas"] = [
    slide_texto("Você não precisa de 10 ferramentas de IA.\n\nPrecisa de 1 Sócio que orquestra todas elas.", kw="1 Sócio", big=True),
    slide_texto("O problema é excesso de ferramenta, não falta.\n\nCada tarefa nova, um aplicativo novo. E nenhum deles conversa com o outro."),
    slide_texto("Primeira tarefa: escrever.\n\nUma IA solta escreve o texto. Mas esquece o que você já vendeu, o preço que você cobra, o jeito que você fala."),
    slide_texto("Segunda tarefa: criar imagem.\n\nOutra aba, outro login, outro pedido do zero. O Sócio IA gera a arte já sabendo a identidade visual do seu negócio, sem você repetir o contexto.", kw="Sócio IA"),
    slide_texto("Terceira tarefa: responder o lead.\n\nVocê copia a pergunta de um aplicativo e cola em outro pra gerar a resposta. O Sócio IA lê a conversa, sabe o histórico do lead, e responde dentro do mesmo canal.", kw="Sócio IA"),
    slide_texto("Quarta tarefa: organizar a agenda.\n\nNenhuma IA solta marca compromisso sozinha. O Sócio IA marca, remarca e avisa, porque enxerga a agenda como parte da mesma operação.", kw="Sócio IA"),
    slide_texto("Quinta tarefa: guardar o histórico do negócio.\n\nCada ferramenta solta esquece tudo numa conversa nova. O Sócio IA carrega o histórico do seu negócio pronto pra qualquer tarefa, sem você reexplicar do zero.", kw="Sócio IA"),
    slide_texto("Dez ferramentas soltas custam tempo trocando de aba.\n\nUm sistema orquestrado custa zero.", kw="custa zero", big=True),
    slide_cta("Comenta SÓCIO que eu te mostro como monto essa orquestra de tarefas com Brain, Skills e Orquestração."),
]

CARROSSEIS["03-esteira-vende-todo-dia"] = [
    slide_texto("Montei uma esteira que vende todo dia.\n\nEu só aprovo.", kw="vende todo dia", big=True),
    slide_texto("Nos próximos slides, os passos pra montar uma esteira assim no seu negócio, sem contratar mais ninguém."),
    slide_texto("Passo 1. Um sistema lê o histórico do seu negócio: sua voz, sua oferta, seu preço, o que já vendeu antes."),
    slide_texto("Passo 2. Esse mesmo sistema escolhe o assunto do dia sozinho, puxando do que já funcionou com o seu cliente."),
    slide_texto("Passo 3. Ele escreve a peça na sua voz e monta a oferta que fecha o texto, sem você abrir um documento em branco."),
    slide_texto("Passo 4. Você recebe pronto, aprova em um clique, e o sistema publica. A esteira roda de novo amanhã sozinha.", kw="sozinha"),
    slide_chips("O motivo disso funcionar: 3 partes trabalhando juntas.",
                [("Brain", "guarda o contexto do seu negócio."), ("Skills", "executam cada tarefa."), ("Orquestração", "encadeia tudo sem você repetir comando.")],
                "É o mecanismo por trás do Sócio IA.", kw="Sócio IA"),
    slide_cta("Comenta SÓCIO que eu te mostro como monto essa esteira com Brain, Skills e Orquestração."),
]

CARROSSEIS["04-7-tarefas-socio-ia"] = [
    slide_texto("As 7 tarefas da sua semana que o Sócio IA assume por você.", kw="Sócio IA", big=True),
    slide_texto("Item 1. Escrever o conteúdo do dia.\n\nVocê não abre um documento em branco, o sistema já escreve na sua voz, com a sua oferta dentro do texto."),
    slide_texto("Item 2. Montar a arte da peça.\n\nO texto sai pronto e a imagem sai junto, no seu padrão visual, sem você abrir editor nenhum."),
    slide_texto("Item 3. Responder o lead que chegou.\n\nAlguém comenta ou manda mensagem, o sistema qualifica na hora, sem esperar você abrir o celular."),
    slide_texto("Item 4. Montar a proposta comercial.\n\nDepois da conversa, a proposta com preço e escopo sai pronta, sem você recortar de um modelo antigo."),
    slide_texto("Item 5. Fazer o follow-up de quem sumiu.\n\nQuem não respondeu em 3 dias recebe a próxima mensagem sozinho, sem entrar na sua lista de pendência."),
    slide_texto("Item 6. Organizar a agenda de reunião.\n\nO sistema encaixa o horário com o lead e já manda o convite, sem ida e volta de mensagem pra fechar hora."),
    slide_texto("Item 7. Montar o relatório da semana.\n\nToda sexta o número do que vendeu, do que empacou e do que precisa de atenção chega pronto pra você ler."),
    slide_chips("O motivo disso funcionar: 3 partes trabalhando juntas.",
                [("Brain", "guarda o contexto: voz, oferta, preço, histórico."), ("Skills", "executam cada tarefa."), ("Orquestração", "encadeia tudo sem você repetir comando.")],
                "É o mecanismo por trás do Sócio IA.", kw="Sócio IA"),
    slide_cta("Comenta SÓCIO que eu te mostro como coloco essas 7 tarefas pra rodar com Brain, Skills e Orquestração."),
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
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=2)
        for slug, slides in CARROSSEIS.items():
            d = f"{ROOT}/{slug}"; os.makedirs(d, exist_ok=True)
            paths = []
            await page.set_viewport_size({"width":1080,"height":1350})
            for i, html in enumerate(slides, 1):
                out = f"{d}/slide-{i:02d}.png"
                await page.set_content(html)
                await page.wait_for_timeout(120)
                await page.screenshot(path=out)
                paths.append(out); print("rendered", out)
            await build_mosaic(page, paths, f"{d}/_mosaico.png")
            print("mosaic", f"{d}/_mosaico.png")
        await browser.close()

asyncio.run(main())
