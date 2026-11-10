#!/usr/bin/env python3
"""
coletar.py: coleta dado publico com programas gratis. Video e transcricao (yt-dlp) e
imagem (gallery-dl) sao o que funciona sem conta. Instagram (Instaloader) sem conta costuma
ser barrado em servidor: o caminho padrao para Instagram e a reserva paga descrita no
SKILL.md; coletar logado e opcao avancada, com risco para a conta usada.

Um subcomando por tipo de pedido. A saida vai sempre para uma pasta, com planilha (CSV),
dados completos (JSON) e um resumo.json dizendo quantos itens vieram e quantos falharam.

  python3 scripts/coletar.py instagram-perfil USUARIO [--max 12] [--cookies ARQ] [--baixar-midia]
  python3 scripts/coletar.py instagram-post LINK [--cookies ARQ] [--baixar-midia]
  python3 scripts/coletar.py video-dados LINK [--idiomas pt,en] [--comentarios] [--cookies ARQ]
  python3 scripts/coletar.py video-lista LINK [--max 30] [--cookies ARQ]
  python3 scripts/coletar.py video-baixar LINK [--so-audio] [--altura 720] [--cookies ARQ]
  python3 scripts/coletar.py imagens LINK [--max 20] [--so-dados] [--cookies ARQ]

Vale em todos: --saida PASTA (padrao: ./raspagem/<data>-<subcomando>-<alvo>) e
--extra "opcoes" (repassa opcoes do proprio programa; a lista esta em references/).

Codigo de saida: 0 veio tudo; 1 veio parte ou deu erro; 2 bloqueio ou pedido de login;
3 programa nao instalado (rode: bash scripts/instalar.sh).
"""
import argparse
import csv
import datetime
import json
import os
import random
import re
import shlex
import shutil
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
CASA = os.path.expanduser("~")
VENV_BIN = os.path.join(
    os.environ.get("SOFT_RASPAGEM_HOME", os.path.join(CASA, ".local", "share", "soft-raspagem")),
    "venv", "bin")

SAIU_OK, SAIU_PARCIAL, SAIU_BLOQUEIO, SAIU_SEM_PROGRAMA = 0, 1, 2, 3


# ------------------------------------------------------------------ apoio

def achar(nome):
    """Caminho do programa: PATH, depois ~/.local/bin, depois o ambiente proprio da skill."""
    c = shutil.which(nome)
    if c:
        return c
    for c in (os.path.join(CASA, ".local", "bin", nome), os.path.join(VENV_BIN, nome)):
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


def exigir(nome):
    c = achar(nome)
    if not c:
        print(f"PROGRAMA AUSENTE: {nome} nao esta instalado nesta maquina.")
        print(f"Rode primeiro: bash {os.path.join(AQUI, 'instalar.sh')}")
        sys.exit(SAIU_SEM_PROGRAMA)
    return c


def limpo(texto, tam=60):
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", texto).strip("-")[:tam] or "alvo"


def pasta_saida(args, alvo):
    if args.saida:
        p = os.path.abspath(args.saida)
    else:
        hoje = datetime.date.today().isoformat()
        p = os.path.abspath(os.path.join("raspagem", f"{hoje}-{args.comando}-{limpo(alvo)}"))
    os.makedirs(p, exist_ok=True)
    return p


def gravar_json(caminho, dado):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dado, f, ensure_ascii=False, indent=2, default=str)


def gravar_csv(caminho, linhas, colunas):
    # utf-8 com marca, para abrir com acento certo em planilha
    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colunas, extrasaction="ignore")
        w.writeheader()
        for l in linhas:
            w.writerow(l)


def rodar(cmd, limite=900):
    """Roda o programa e devolve (codigo, saida, erro). Nunca levanta."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=limite,
                           stdin=subprocess.DEVNULL)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired as e:
        err = e.stderr if isinstance(e.stderr, str) else (e.stderr or b"").decode("utf-8", "replace")
        return 124, "", (err or "") + f"\nTempo esgotado depois de {limite} segundos."


# Ordem importa: o primeiro padrao que casar decide o diagnostico.
DIAGNOSTICOS = [
    ("login", r"sign in to confirm|login.?required|redirected to login|requires login|"
              r"--login|not logged in|use --cookies|cookies for the authentication|"
              r"private (profile|video|account)|is private|401 unauthorized|"
              r"please wait a few minutes|authentication required|account credentials|"
              r"log in to|logged-in",
     "PEDIDO DE LOGIN: o site so entrega isso para quem esta logado, ou desconfiou de acesso "
     "automatico vindo deste servidor. Caminhos: (1) tentar mais tarde, uma vez, sem "
     "insistir; (2) o dono exporta os cookies do navegador dele com uma extensao, manda o "
     "arquivo, e voce repete com --cookies ARQUIVO; (3) a reserva paga, com aviso de custo "
     "antes."),
    ("bloqueio", r"403 forbidden|429|too many requests|ip address is blocked|rate.?limit|"
                 r"checkpoint|challenge_required|temporarily blocked|http error 403|"
                 r"feedback_required|captcha",
     "BLOQUEIO DO SITE: o site recusou o acesso deste servidor (bloqueio por volume ou por "
     "endereco de rede). Nao insista em seguida, porque piora. Caminhos: (1) esperar "
     "algumas horas e tentar de novo com menos itens; (2) repetir com o arquivo de cookies "
     "que o dono exportou do navegador dele (--cookies ARQUIVO); (3) a reserva paga, com "
     "aviso de custo antes."),
    ("inexistente", r"does not exist|404 not found|http error 404|video unavailable|"
                    r"profilenotexists|not found|has been removed|no longer available",
     "NAO ENCONTRADO: o perfil, o post ou o link nao existe mais, ou foi digitado errado. "
     "Confira o endereco com o dono."),
    ("sem_suporte", r"unsupported url|no suitable extractor|no extractor found",
     "LINK SEM SUPORTE: este programa nao conhece esse endereco. Tente o outro subcomando "
     "(video-dados para video, imagens para galeria) ou confira o link."),
    ("tempo", r"tempo esgotado|timed out|timeout",
     "DEMOROU DEMAIS: a coleta passou do tempo limite. Tente de novo com menos itens."),
]


# Instagram tem mensagem propria: a reserva paga vem primeiro, o login vem por ultimo e com aviso.
MSG_INSTAGRAM_BARROU = (
    "INSTAGRAM BARROU A COLETA GRATIS: sem conta, o Instagram recusa acesso automatico vindo "
    "de servidor. Isso e o comum, nao e defeito. Nao repita em seguida, porque piora.\n"
    "Caminhos, nesta ordem:\n"
    "  1. RESERVA PAGA (Apify), o caminho padrao para Instagram: custa centavos por coleta e "
    "nao expoe a conta de ninguem. Diga o custo ao dono antes de rodar. Teto de US$ 1 por "
    "coleta; acima disso, so com nova ordem dele. Passo a passo no SKILL.md, secao "
    "\"Instagram: caminho padrao\".\n"
    "  2. OPCAO AVANCADA (coletar logado), so se o dono pedir depois de ler o aviso. "
    "RISCO: conta usada para coleta automatica pode ser limitada ou bloqueada pelo "
    "Instagram. So conta secundaria, nunca a conta principal. Como fazer: SKILL.md, secao "
    "\"Opcao avancada\".")
MSG_INSTAGRAM_BARROU_LOGADO = (
    "INSTAGRAM BARROU MESMO COM A CONTA: a coleta foi feita logada e o Instagram recusou. "
    "PARE de usar essa conta para coleta agora: insistir e o que leva a bloqueio. Peca ao "
    "dono para abrir o aplicativo nessa conta e ver se ha pedido de confirmacao. Os cookies "
    "podem tambem ter vencido (ele exporta de novo). Para a coleta em si, use a RESERVA "
    "PAGA (Apify): centavos por coleta, sem expor conta, custo avisado antes, teto de "
    "US$ 1. Passo a passo no SKILL.md, secao \"Instagram: caminho padrao\".")


def diagnosticar(texto):
    """Le a mensagem de erro do programa e devolve (tipo, explicacao em portugues)."""
    t = (texto or "").lower()
    for tipo, padrao, msg in DIAGNOSTICOS:
        if re.search(padrao, t):
            return tipo, msg
    return "erro", ("ERRO NAO CLASSIFICADO: o programa devolveu um erro que eu nao reconheco. "
                    "Leia o erro bruto abaixo e a referencia do programa em references/.")


def ultimas_linhas_de_erro(texto, n=6):
    linhas = [l.strip() for l in (texto or "").splitlines() if l.strip()]
    graves = [l for l in linhas if re.search(r"error|erro|forbidden|unauthorized|blocked|tempo esgotado|429|too many|sign in", l, re.I)]
    return "\n".join((graves or linhas)[-n:])[:1500]


def fechar(args, pasta, alvo, programa, vieram, falharam, arquivos, erro_bruto="", avisos=None):
    """Grava o resumo, imprime o fecho em portugues e sai com o codigo certo."""
    tipo, msg = ("ok", "")
    if erro_bruto and (falharam or not vieram):
        tipo, msg = diagnosticar(erro_bruto)
        if programa == "Instaloader" and tipo in ("login", "bloqueio"):
            logado = getattr(args, "sessao", None) or getattr(args, "cookies", None)
            msg = MSG_INSTAGRAM_BARROU_LOGADO if logado else MSG_INSTAGRAM_BARROU
    if vieram and not falharam:
        situacao = "completo"
    elif vieram:
        situacao = "parcial"
    else:
        situacao = "nada veio"
    resumo = {
        "comando": args.comando, "alvo": alvo, "programa": programa,
        "quando": datetime.datetime.now().isoformat(timespec="seconds"),
        "situacao": situacao, "vieram": vieram, "falharam": falharam,
        "diagnostico": tipo, "mensagem": msg,
        "erro_bruto": ultimas_linhas_de_erro(erro_bruto) if (falharam or not vieram) else "",
        "avisos": avisos or [], "pasta": pasta,
        "arquivos": sorted(os.path.basename(a) for a in arquivos if os.path.exists(a)),
    }
    gravar_json(os.path.join(pasta, "resumo.json"), resumo)
    print(f"== {args.comando}: {alvo} ({programa}) ==")
    print(f"Situacao: {situacao} | vieram: {vieram} | falharam: {falharam}")
    for a in avisos or []:
        print(f"Aviso: {a}")
    if msg:
        print(msg)
    if resumo["erro_bruto"]:
        print("Erro bruto do programa:")
        for l in resumo["erro_bruto"].splitlines():
            print(f"  {l}")
    print(f"Pasta: {pasta}")
    print("Arquivos: " + ", ".join(resumo["arquivos"] + ["resumo.json"]))
    if situacao == "completo":
        sys.exit(SAIU_OK)
    sys.exit(SAIU_BLOQUEIO if tipo in ("login", "bloqueio") else SAIU_PARCIAL)


def extras(args):
    return shlex.split(args.extra) if args.extra else []


# ------------------------------------------------------------------ Instagram (Instaloader)

def garantir_instaloader():
    """O Instaloader pode morar num ambiente proprio (pipx ou venv). Se este Python nao
    enxerga a biblioteca, troca para o Python que roda o programa instaloader."""
    try:
        import instaloader  # noqa: F401
        return
    except ImportError:
        pass
    prog = exigir("instaloader")
    if os.environ.get("SOFT_RASPAGEM_TROCOU"):
        print("O Instaloader esta instalado, mas a biblioteca nao abriu. Rode: bash "
              + os.path.join(AQUI, "instalar.sh") + " --atualizar")
        sys.exit(SAIU_SEM_PROGRAMA)
    interp = None
    try:
        with open(os.path.realpath(prog), "r", encoding="utf-8", errors="replace") as f:
            primeira = f.readline().strip()
        if primeira.startswith("#!"):
            interp = primeira[2:].strip().split()[0]
    except OSError:
        pass
    if not interp or not os.path.exists(interp):
        print("Nao achei o Python do Instaloader. Rode: bash " + os.path.join(AQUI, "instalar.sh"))
        sys.exit(SAIU_SEM_PROGRAMA)
    os.environ["SOFT_RASPAGEM_TROCOU"] = "1"
    os.execv(interp, [interp, os.path.abspath(__file__)] + sys.argv[1:])


COLUNAS_POST = ["link", "data", "tipo", "legenda", "curtidas", "comentarios", "visualizacoes",
                "hashtags", "mencoes", "autor", "midia", "codigo"]


def post_para_linha(post):
    tipo = {"GraphImage": "foto", "GraphVideo": "video", "GraphSidecar": "carrossel"}.get(
        post.typename, post.typename)

    def seguro(f, padrao=None):
        try:
            return f()
        except Exception:
            return padrao
    return {
        "link": f"https://www.instagram.com/p/{post.shortcode}/",
        "data": seguro(lambda: post.date_local.strftime("%Y-%m-%d %H:%M"), ""),
        "tipo": tipo,
        "legenda": seguro(lambda: post.caption, "") or "",
        "curtidas": seguro(lambda: post.likes),
        "comentarios": seguro(lambda: post.comments),
        "visualizacoes": seguro(lambda: post.video_view_count if post.is_video else None),
        "hashtags": " ".join("#" + h for h in seguro(lambda: post.caption_hashtags, []) or []),
        "mencoes": " ".join("@" + m for m in seguro(lambda: post.caption_mentions, []) or []),
        "autor": seguro(lambda: post.owner_username, ""),
        "midia": seguro(lambda: post.video_url if post.is_video else post.url, ""),
        "codigo": post.shortcode,
    }


def abrir_instaloader(args, pasta):
    import instaloader

    class SemEsperaLonga(instaloader.RateController):
        """O padrao do Instaloader, ao ser barrado, dorme ate meia hora e tenta de novo.
        Num agente isso vira silencio. Aqui a espera longa vira erro claro."""
        def sleep(self, secs):
            if secs > 90:
                raise instaloader.exceptions.ConnectionException(
                    f"429 Too Many Requests: o Instagram mandou esperar {int(secs)} segundos.")
            time.sleep(secs)

    L = instaloader.Instaloader(
        quiet=True, max_connection_attempts=1, request_timeout=60,
        download_comments=False, save_metadata=False, compress_json=False,
        dirname_pattern=os.path.join(pasta, "midia"),
        rate_controller=lambda ctx: SemEsperaLonga(ctx))
    # Sem --cookies e sem --sessao a coleta e anonima: tenta uma vez e, se o site barrar,
    # o fecho aponta a reserva paga. A senha de ninguem passa por este script.
    if args.cookies:
        usuario, biscoitos = ler_cookies_instagram(args.cookies)
        L.load_session(usuario, biscoitos)
    elif args.sessao:
        L.load_session_from_file(args.sessao)
    return instaloader, L


def ler_cookies_instagram(caminho):
    """Le o arquivo de cookies exportado do navegador (formato Netscape, cookies.txt) e
    devolve (rotulo da conta, dicionario de cookies do Instagram). Nao acessa a rede."""
    import http.cookiejar
    caminho = os.path.abspath(os.path.expanduser(caminho))
    raiz_skill = os.path.dirname(AQUI)
    if os.path.commonpath([caminho, raiz_skill]) == raiz_skill:
        raise ValueError("arquivo de cookies dentro da pasta da skill. Guarde fora dela "
                         "(por exemplo em ~/.config/soft-raspagem/) e passe o novo caminho.")
    if not os.path.isfile(caminho):
        raise ValueError(f"arquivo de cookies nao encontrado: {caminho}")
    pote = http.cookiejar.MozillaCookieJar()
    try:
        pote.load(caminho, ignore_discard=True, ignore_expires=True)
    except (http.cookiejar.LoadError, OSError) as e:
        raise ValueError("o arquivo de cookies nao esta no formato Netscape (cookies.txt). "
                         f"Peca ao dono para exportar de novo com a extensao. Detalhe: {e}")
    biscoitos = {c.name: c.value for c in pote if "instagram.com" in (c.domain or "")}
    faltam = [n for n in ("sessionid", "csrftoken") if not biscoitos.get(n)]
    if faltam:
        raise ValueError("o arquivo de cookies nao traz o Instagram logado (falta: "
                         + ", ".join(faltam) + "). O dono precisa exportar com a conta "
                         "secundaria aberta no instagram.com.")
    return "conta-" + str(biscoitos.get("ds_user_id") or "dos-cookies"), biscoitos


def cmd_instagram_perfil(args):
    exigir("instaloader")
    garantir_instaloader()
    usuario = args.alvo.strip().lstrip("@")
    m = re.search(r"instagram\.com/([A-Za-z0-9_.]+)", usuario)
    if m:
        usuario = m.group(1)
    pasta = pasta_saida(args, usuario)
    arquivos, linhas, falharam, erro = [], [], 0, ""
    try:
        instaloader, L = abrir_instaloader(args, pasta)
        perfil = instaloader.Profile.from_username(L.context, usuario)
        dados_perfil = {
            "usuario": perfil.username, "nome": perfil.full_name, "bio": perfil.biography,
            "link_da_bio": perfil.external_url, "seguidores": perfil.followers,
            "seguindo": perfil.followees, "publicacoes": perfil.mediacount,
            "privado": perfil.is_private, "verificado": perfil.is_verified,
            "link": f"https://www.instagram.com/{perfil.username}/",
        }
        gravar_json(os.path.join(pasta, "perfil.json"), dados_perfil)
        arquivos.append(os.path.join(pasta, "perfil.json"))
        if perfil.is_private and not (args.sessao or args.cookies):
            erro = "Private profile: login required to see the posts."
        else:
            for post in perfil.get_posts():
                if len(linhas) >= args.max:
                    break
                try:
                    linhas.append(post_para_linha(post))
                    if args.baixar_midia:
                        L.download_post(post, target=usuario)
                except Exception as e:  # um post ruim nao derruba os outros
                    falharam += 1
                    erro = f"{type(e).__name__}: {e}"
                time.sleep(random.uniform(args.pausa, args.pausa * 2))
    except Exception as e:
        erro = f"{type(e).__name__}: {e}"
        falharam += 1 if not linhas else 0
    if linhas:
        gravar_csv(os.path.join(pasta, "posts.csv"), linhas, COLUNAS_POST)
        gravar_json(os.path.join(pasta, "posts.json"), linhas)
        arquivos += [os.path.join(pasta, "posts.csv"), os.path.join(pasta, "posts.json")]
    avisos = []
    if linhas and len(linhas) < args.max and not erro:
        avisos.append(f"o perfil so tinha {len(linhas)} posts visiveis (pedido: {args.max})")
    if erro and linhas and len(linhas) < args.max:
        falharam = max(falharam, 1)
    fechar(args, pasta, "@" + usuario, "Instaloader", len(linhas), falharam, arquivos, erro, avisos)


def cmd_instagram_post(args):
    exigir("instaloader")
    garantir_instaloader()
    m = re.search(r"/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)", args.alvo)
    codigo = m.group(1) if m else args.alvo.strip().strip("/")
    pasta = pasta_saida(args, codigo)
    arquivos, linhas, erro = [], [], ""
    try:
        instaloader, L = abrir_instaloader(args, pasta)
        post = instaloader.Post.from_shortcode(L.context, codigo)
        linhas.append(post_para_linha(post))
        if args.baixar_midia:
            L.download_post(post, target=codigo)
    except Exception as e:
        erro = f"{type(e).__name__}: {e}"
    if linhas:
        gravar_csv(os.path.join(pasta, "post.csv"), linhas, COLUNAS_POST)
        gravar_json(os.path.join(pasta, "post.json"), linhas[0])
        arquivos += [os.path.join(pasta, "post.csv"), os.path.join(pasta, "post.json")]
    fechar(args, pasta, codigo, "Instaloader", len(linhas), 0 if linhas and not erro else 1,
           arquivos, erro)


# ------------------------------------------------------------------ video (yt-dlp)

CAMPOS_VIDEO = [("id", "id"), ("titulo", "title"), ("link", "webpage_url"), ("canal", "channel"),
                ("autor", "uploader"), ("data", "upload_date"), ("duracao_segundos", "duration"),
                ("visualizacoes", "view_count"), ("curtidas", "like_count"),
                ("comentarios", "comment_count"), ("descricao", "description"),
                ("etiquetas", "tags"), ("idioma", "language"), ("site", "extractor_key"),
                ("miniatura", "thumbnail")]


def resumo_video(info):
    d = {}
    for nosso, deles in CAMPOS_VIDEO:
        v = info.get(deles)
        if deles == "upload_date" and v and len(str(v)) == 8:
            v = f"{v[:4]}-{v[4:6]}-{v[6:]}"
        if isinstance(v, list):
            v = ", ".join(str(x) for x in v)
        d[nosso] = v
    if not d.get("link"):
        d["link"] = info.get("url") or info.get("original_url")
    return d


def legenda_para_texto(caminho):
    """Tira horario, marca e repeticao de um .vtt ou .srt e devolve so a fala."""
    with open(caminho, "r", encoding="utf-8", errors="replace") as f:
        bruto = f.read()
    saida, ultima = [], None
    for linha in bruto.splitlines():
        l = linha.strip()
        if (not l or l == "WEBVTT" or "-->" in l or l.isdigit()
                or re.match(r"^(Kind|Language|NOTE|STYLE|REGION)\b", l)):
            continue
        l = re.sub(r"<[^>]+>", "", l)
        l = l.replace("&amp;", "&").replace("&nbsp;", " ").replace("&gt;", ">").replace("&lt;", "<")
        l = re.sub(r"\s+", " ", l).strip()
        if l and l != ultima:
            saida.append(l)
            ultima = l
    return "\n".join(saida)


def base_ytdlp(args):
    cmd = [exigir("yt-dlp"), "--no-update", "--no-warnings", "--no-progress", "--ignore-config"]
    if not shutil.which("deno") and shutil.which("node"):
        cmd += ["--js-runtimes", "node"]
    if args.cookies:
        cmd += ["--cookies", args.cookies]
    return cmd


def cmd_video_dados(args):
    pasta = pasta_saida(args, re.sub(r"^https?://(www\.)?", "", args.alvo))
    cmd = base_ytdlp(args) + [
        "--skip-download", "--no-playlist", "--write-info-json",
        "--write-subs", "--write-auto-subs", "--sub-langs", args.idiomas,
        "--sub-format", "vtt/srt/best", "--sleep-subtitles", "1",
        "-o", os.path.join(pasta, "%(id)s.%(ext)s")]
    if args.comentarios:
        cmd.append("--write-comments")
    cod, out, err = rodar(cmd + extras(args) + [args.alvo])
    arquivos, avisos, vieram, falharam = [], [], 0, 0
    infos = [f for f in os.listdir(pasta) if f.endswith(".info.json")]
    for nome in infos:
        with open(os.path.join(pasta, nome), "r", encoding="utf-8") as f:
            info = json.load(f)
        dados = resumo_video(info)
        if args.comentarios and info.get("comments"):
            coms = [{"autor": c.get("author"), "texto": c.get("text"), "curtidas": c.get("like_count"),
                     "quando": c.get("timestamp")} for c in info["comments"]]
            gravar_csv(os.path.join(pasta, "comentarios.csv"), coms, ["autor", "texto", "curtidas", "quando"])
            arquivos.append(os.path.join(pasta, "comentarios.csv"))
            dados["comentarios_coletados"] = len(coms)
        gravar_json(os.path.join(pasta, "dados.json"), dados)
        gravar_csv(os.path.join(pasta, "dados.csv"), [dados], [c for c, _ in CAMPOS_VIDEO])
        arquivos += [os.path.join(pasta, "dados.json"), os.path.join(pasta, "dados.csv"),
                     os.path.join(pasta, nome)]
        vieram += 1
    legendas = sorted(f for f in os.listdir(pasta) if f.endswith((".vtt", ".srt")))
    for nome in legendas:
        texto = legenda_para_texto(os.path.join(pasta, nome))
        destino = os.path.join(pasta, "transcricao-" + nome.rsplit(".", 2)[-2] + ".txt")
        with open(destino, "w", encoding="utf-8") as f:
            f.write(texto + "\n")
        arquivos += [os.path.join(pasta, nome), destino]
    if vieram and not legendas:
        avisos.append("o video nao tem legenda nos idiomas pedidos (" + args.idiomas +
                      "), ou o site negou a legenda. Os dados vieram. Para a fala, baixe o audio "
                      "(video-baixar --so-audio) e transcreva.")
    if not vieram:
        falharam = 1
    elif cod != 0 and legendas == []:
        falharam = 1
    fechar(args, pasta, args.alvo, "yt-dlp", vieram, falharam, arquivos, err, avisos)


def cmd_video_lista(args):
    pasta = pasta_saida(args, re.sub(r"^https?://(www\.)?", "", args.alvo))
    cmd = base_ytdlp(args) + ["--flat-playlist", "-J", "-I", f"1:{args.max}"]
    cod, out, err = rodar(cmd + extras(args) + [args.alvo])
    linhas, arquivos = [], []
    try:
        info = json.loads(out) if out.strip() else {}
    except ValueError:
        info = {}
    for e in (info or {}).get("entries") or []:
        if not e:
            continue
        l = resumo_video(e)
        if not l.get("link") and e.get("id") and "youtube" in str(e.get("ie_key", "")).lower():
            l["link"] = "https://www.youtube.com/watch?v=" + e["id"]
        linhas.append(l)
    colunas = ["titulo", "link", "visualizacoes", "duracao_segundos", "data", "canal", "descricao", "id"]
    if linhas:
        gravar_csv(os.path.join(pasta, "lista.csv"), linhas, colunas)
        gravar_json(os.path.join(pasta, "lista.json"),
                    {"titulo": info.get("title"), "canal": info.get("channel") or info.get("uploader"),
                     "link": info.get("webpage_url"), "itens": linhas})
        arquivos += [os.path.join(pasta, "lista.csv"), os.path.join(pasta, "lista.json")]
    avisos = []
    if linhas and not any(l.get("data") for l in linhas):
        avisos.append("a lista rapida nao traz data nem curtidas de cada video; para isso rode "
                      "video-dados em cada link que interessar")
    fechar(args, pasta, args.alvo, "yt-dlp", len(linhas), 0 if linhas else 1, arquivos, err, avisos)


def cmd_video_baixar(args):
    pasta = pasta_saida(args, re.sub(r"^https?://(www\.)?", "", args.alvo))
    cmd = base_ytdlp(args) + ["--no-playlist", "--restrict-filenames",
                              "-o", os.path.join(pasta, "%(title).80s-%(id)s.%(ext)s")]
    avisos = []
    tem_ffmpeg = bool(shutil.which("ffmpeg"))
    if args.so_audio:
        if tem_ffmpeg:
            cmd += ["-f", "ba/b", "-x", "--audio-format", "mp3"]
        else:
            cmd += ["-f", "ba/b"]
            avisos.append("sem ffmpeg: o audio veio no formato original, sem converter para mp3")
    else:
        a = args.altura
        if tem_ffmpeg:
            cmd += ["-f", f"bv*[height<={a}]+ba/b[height<={a}]/b", "--merge-output-format", "mp4"]
        else:
            cmd += ["-f", f"b[height<={a}]/b"]
            avisos.append("sem ffmpeg: veio o melhor arquivo unico disponivel, que pode ter qualidade menor")
    antes = set(os.listdir(pasta))
    cod, out, err = rodar(cmd + extras(args) + [args.alvo], limite=3600)
    novos = [os.path.join(pasta, f) for f in sorted(set(os.listdir(pasta)) - antes)
             if not f.endswith((".part", ".ytdl"))]
    fechar(args, pasta, args.alvo, "yt-dlp", len(novos), 0 if (novos and cod == 0) else 1,
           novos, err, avisos)


# ------------------------------------------------------------------ imagens (gallery-dl)

def cmd_imagens(args):
    pasta = pasta_saida(args, re.sub(r"^https?://(www\.)?", "", args.alvo))
    prog = exigir("gallery-dl")
    base = [prog, "--no-input", "--no-colors", "--range", f"1-{args.max}"]
    if args.cookies:
        base += ["--cookies", args.cookies]
    linhas, arquivos, falharam = [], [], 0
    if args.so_dados:
        cod, out, err = rodar(base + ["-j"] + extras(args) + [args.alvo])
        try:
            itens = json.loads(out) if out.strip() else []
        except ValueError:
            itens = []
        for it in itens:
            if isinstance(it, list) and len(it) >= 3 and it[0] == 3:
                meta = it[2] if isinstance(it[2], dict) else {}
                linhas.append(linha_imagem(it[1], meta, ""))
            elif isinstance(it, list) and it and it[0] in (-1, "error"):
                falharam += 1
                err += "\n" + json.dumps(it[1:], ensure_ascii=False)[:400]
    else:
        destino = os.path.join(pasta, "arquivos")
        os.makedirs(destino, exist_ok=True)
        cod, out, err = rodar(base + ["-D", destino, "--write-metadata", "--sleep", "0.5-1.5"]
                              + extras(args) + [args.alvo], limite=3600)
        for nome in sorted(os.listdir(destino)):
            if nome.endswith(".json") or nome.endswith(".part"):
                continue
            meta = {}
            lado = os.path.join(destino, nome + ".json")
            if os.path.exists(lado):
                try:
                    with open(lado, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                except ValueError:
                    meta = {}
            linhas.append(linha_imagem(meta.get("url") or meta.get("file_url") or "", meta,
                                       os.path.join("arquivos", nome)))
        falharam = len(re.findall(r"\[error\]", err))
    if linhas:
        gravar_csv(os.path.join(pasta, "itens.csv"), linhas, COLUNAS_IMAGEM)
        gravar_json(os.path.join(pasta, "itens.json"), linhas)
        arquivos += [os.path.join(pasta, "itens.csv"), os.path.join(pasta, "itens.json")]
        if not args.so_dados:
            arquivos.append(os.path.join(pasta, "arquivos"))
    if not linhas:
        falharam = max(falharam, 1)
    fechar(args, pasta, args.alvo, "gallery-dl", len(linhas), falharam, arquivos,
           err if (cod != 0 or not linhas) else "")


COLUNAS_IMAGEM = ["arquivo", "link_do_arquivo", "titulo", "descricao", "autor", "data", "site",
                  "largura", "altura", "curtidas", "etiquetas"]


def linha_imagem(url, meta, arquivo):
    def pega(*chaves):
        for c in chaves:
            v = meta.get(c)
            if isinstance(v, dict):
                v = v.get("name") or v.get("username") or v.get("nick")
            if v not in (None, "", [], {}):
                return ", ".join(str(x) for x in v) if isinstance(v, list) else v
        return ""
    return {
        "arquivo": arquivo or (str(pega("filename")) + "." + str(pega("extension"))).strip("."),
        "link_do_arquivo": url,
        "titulo": pega("title", "canonicaltitle", "filename"),
        "descricao": str(pega("description", "content", "caption", "comment"))[:2000],
        "autor": pega("author", "user", "username", "uploader", "artist", "owner"),
        "data": pega("date", "timestamp", "created_at"),
        "site": pega("category"),
        "largura": pega("width", "image_width"),
        "altura": pega("height", "image_height"),
        "curtidas": pega("likes", "like_count", "favorite_count", "score"),
        "etiquetas": pega("tags", "hashtags"),
    }


# ------------------------------------------------------------------ entrada

def main():
    comum = argparse.ArgumentParser(add_help=False)
    comum.add_argument("--saida", help="pasta onde gravar (padrao: ./raspagem/<data>-<subcomando>-<alvo>)")
    comum.add_argument("--extra", help='opcoes do proprio programa, entre aspas (so vale para yt-dlp e gallery-dl)')

    p = argparse.ArgumentParser(description="Coleta de dado publico: video e transcricao (yt-dlp), imagem "
                                "(gallery-dl) e, como opcao avancada, Instagram (Instaloader).")
    sub = p.add_subparsers(dest="comando", required=True)

    def insta(nome, ajuda, alvo):
        s = sub.add_parser(nome, parents=[comum], help=ajuda)
        s.add_argument("alvo", help=alvo)
        s.add_argument("--cookies", help="OPCAO AVANCADA, com risco para a conta: arquivo de cookies "
                       "(cookies.txt) de uma conta SECUNDARIA do dono, exportado do navegador dele")
        s.add_argument("--sessao", help="OPCAO AVANCADA, com risco para a conta: nome do usuario que ja "
                       "tem arquivo de sessao do Instaloader nesta maquina")
        s.add_argument("--baixar-midia", action="store_true", help="baixa tambem as fotos e os videos")
        return s

    s = insta("instagram-perfil", "posts de um perfil do Instagram, em planilha (sem conta costuma ser barrado)",
              "usuario, @usuario ou link do perfil")
    s.add_argument("--max", type=int, default=12, help="quantos posts no maximo (padrao 12)")
    s.add_argument("--pausa", type=float, default=2.0, help="pausa minima entre posts, em segundos (padrao 2)")
    s.set_defaults(func=cmd_instagram_perfil)

    s = insta("instagram-post", "um post ou reel do Instagram, pelo link (sem conta costuma ser barrado)",
              "link do post ou do reel")
    s.set_defaults(func=cmd_instagram_post)

    def video(nome, ajuda):
        s = sub.add_parser(nome, parents=[comum], help=ajuda)
        s.add_argument("alvo", help="link")
        s.add_argument("--cookies", help="arquivo de cookies exportado pelo dono, quando o site pede login")
        return s

    s = video("video-dados", "dados e transcricao de um video (YouTube, TikTok e centenas de sites), sem baixar o video")
    s.add_argument("--idiomas", default="pt.*,en.*", help='idiomas da legenda (padrao "pt.*,en.*")')
    s.add_argument("--comentarios", action="store_true", help="traz tambem os comentarios do video")
    s.set_defaults(func=cmd_video_dados)

    s = video("video-lista", "lista os videos de um canal, playlist ou perfil, em planilha")
    s.add_argument("--max", type=int, default=30, help="quantos videos no maximo (padrao 30)")
    s.set_defaults(func=cmd_video_lista)

    s = video("video-baixar", "baixa o video (ou so o audio) de um link")
    s.add_argument("--so-audio", action="store_true", help="baixa so o audio, em mp3")
    s.add_argument("--altura", type=int, default=720, help="altura maxima do video (padrao 720)")
    s.set_defaults(func=cmd_video_baixar)

    s = video("imagens", "imagens de uma galeria, post ou perfil (Pinterest, X, Reddit, Tumblr e outros)")
    s.add_argument("--max", type=int, default=20, help="quantos arquivos no maximo (padrao 20)")
    s.add_argument("--so-dados", action="store_true", help="so a planilha com os links, sem baixar")
    s.set_defaults(func=cmd_imagens)

    args = p.parse_args()
    if getattr(args, "max", 1) < 1:
        p.error("--max precisa ser 1 ou mais")
    args.func(args)


if __name__ == "__main__":
    main()
