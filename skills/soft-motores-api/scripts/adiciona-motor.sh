#!/usr/bin/env bash
# adiciona-motor.sh: põe um provedor de IA por API no cadastro do LEON (motores-api.json), guarda a chave no .env e testa.
# Sem dependências novas: bash, python3 e o node do próprio LEON (o cadastro é conferido pelo validador do LEON).
# A chave NUNCA entra por argumento e NUNCA é impressa. Por padrão roda SIMULADO; para valer, acrescente --aplicar.
# Ações (a lista de provedores está em catalogo.json; os caminhos saem sozinhos; para apontar à mão: --env ARQ --cadastro ARQ):
#   adiciona --provedor X [--modelo M] [--id I] [--aplicar]
#   adiciona --provedor outro --id I --nome N --url U --modelo M [--aplicar]
#   chave --provedor X [--trocar-chave] [--aplicar] pede a chave escondida (não aparece na tela) e grava no .env
#   testa --provedor X [--modelo M] [--timeout S] [--confirmo-destino URL] [--aplicar]
set -euo pipefail
AQUI=$(CDPATH= cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)
command -v python3 >/dev/null 2>&1 || { echo "Preciso do python3 instalado na máquina. Peça ao suporte."; exit 2; }
exec python3 -I - "$AQUI" "$@" <<'PY'
import argparse, atexit, contextlib, fcntl, shlex, json, os, pwd, re, shutil, signal, socket, stat, subprocess, sys, tempfile, termios, time, urllib.error, urllib.parse, urllib.request

CATALOGO, PADRAO_ENV, PADRAO_CADASTRO = os.path.join(sys.argv[1], "catalogo.json"), "/home/cloud/lean-bridge/.env", "/home/cloud/.leon/motores-api.json"
COMANDO = "sudo bash " + shlex.quote(os.path.join(sys.argv[1], "adiciona-motor.sh"))   # o caminho completo, para colar no terminal
for k in ("http_proxy", "https_proxy", "all_proxy", "no_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"): os.environ.pop(k, None)   # nunca por proxy

# id e modelo: as mesmas expressões do lib/motores-api.cjs; MOTOR_*: regra a mais desta skill (a chave do motor nunca esconde outra integração)
RESERVADOS = {"motor", "claude", "codex", "modelo", "nivel", "status", "parar", "para", "reset", "login", "logout",
              "skills", "subagente", "integracoes", "automacoes", "subagentes", "ajuda", "start", "atualiza"}
ID, MODELO, MOTOR_NOME = re.compile(r"[a-z0-9][a-z0-9-]{0,23}"), re.compile(r"[\w.:/~\[\]-]{1,80}", re.ASCII), re.compile(r"MOTOR_[A-Z0-9_]{1,57}")

def seguro(caminho, dono):
    """Devolve o primeiro caminho (o arquivo ou uma pasta acima) com atalho, dono estranho ou escrita de grupo ou de outros; '' se tudo certo."""
    p = os.path.abspath(caminho)
    while True:
        st = os.lstat(p)
        if stat.S_ISLNK(st.st_mode) or st.st_uid not in (0, dono) or st.st_mode & 0o022: return p
        if p == "/": return ""
        p = os.path.dirname(p)

def leon_le(texto, env):
    """Pergunta ao validador do PRÓPRIO LEON (leon2/lib/motores-api.cjs da instalação do .env) como ele lê um cadastro.
    O node roda como o dono do LEON (nunca como root se o LEON não for do root), sem rede (unshare -n), com ambiente limpo.
    Devolve a lista de provedores normalizada, ou None quando ele recusa o arquivo ou não roda."""
    lib, node = os.path.join(os.path.dirname(os.path.abspath(env)), "leon2", "lib"), shutil.which("node")
    node = node and os.path.realpath(node)   # o node também tem de estar em pasta confiável
    if not node: sai("Não achei o programa node. Com sudo, o node pode ficar fora do caminho que o sudo procura (secure_path): rode como o usuário dono do LEON, sem sudo, ou peça ajuda ao suporte.")
    try:
        dono = os.stat(env).st_uid
        ruim = next((r for r in (seguro(f, dono) for f in (os.path.join(lib, "motores-api.cjs"), os.path.join(lib, "log.cjs"), node)) if r), "")
    except (OSError, KeyError): ruim = lib
    if ruim: sai("Não achei o LEON nesta máquina, ou este caminho pode ser alterado por outro usuário: %s. Ele tem de ser do root ou do dono do LEON, sem atalho e sem escrita de grupo nem de outros. Peça ao suporte para conferir (por exemplo: chmod g-w,o-w %s)." % (mostra(ruim), shlex.quote(mostra(ruim)) if mostra(ruim).startswith("/") else "<esse caminho>"))
    u = os.stat(os.path.join(lib, "motores-api.cjs")).st_uid or dono
    g = pwd.getpwuid(u).pw_gid
    js = ("const a=require(process.argv[1]).criar({motoresApiArquivo:process.argv[2],pastas:{leon2Estado:process.argv[3],dados:process.argv[3]}});"
          "const l=a.lista();console.log(JSON.stringify(a.invalido()?null:l))")
    if os.geteuid() != 0 and subprocess.run(["unshare", "-rn", "true"], capture_output=True).returncode != 0:
        sai("Esta máquina não deixa rodar a conferência isolada da rede sem root (restrição do sistema). Rode com sudo; se o sudo não achar o node, peça ajuda ao suporte.")
    tmp = tempfile.mkdtemp(prefix="leon-le.")
    try:
        arq = os.path.join(tmp, "motores-api.json")
        with open(arq, "wb") as f: f.write(texto)
        if os.geteuid() == 0: os.chown(tmp, u, g); os.chown(arq, u, g)
        pre = ["unshare", "-n", "setpriv", "--reuid=%d" % u, "--regid=%d" % g, "--clear-groups", "--"] if os.geteuid() == 0 else ["unshare", "-rn", "--"]
        r = subprocess.run(pre + [node, "-e", js, os.path.join(lib, "motores-api.cjs"), arq, os.path.join(tmp, "estado")], stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, timeout=30, cwd=tmp, env={"PATH": "/usr/bin:/bin", "HOME": tmp})
        return json.loads((r.stdout.strip().splitlines() or ["null"])[-1]) if r.returncode == 0 else None
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def _recusa(x):
    raise ValueError("número inválido")   # nunca o valor: o texto do arquivo não vai à tela

def _float(x):
    v = float(x)
    return _recusa(x) if v != v or v in (float("inf"), float("-inf")) else v

def json_estrito(b):
    return json.loads(b.decode("utf-8") if isinstance(b, bytes) else b, parse_constant=_recusa, parse_float=_float)

# ---- regras desta skill, mais rígidas que as do LEON ----
def url_ok(u):
    if not isinstance(u, str) or not u or len(u) > 300 or re.search(r"[\s?#@\"'<>\\]", u):
        return "o endereço tem espaço, senha embutida (@) ou caractere que não pode"
    try: porta = urllib.parse.urlsplit(u).port
    except ValueError: porta = -1
    if porta is not None and not 1 <= porta <= 65535: return "a porta do endereço precisa ser de 1 a 65535"
    if re.fullmatch(r"http://(127\.0\.0\.1|localhost)(:\d{1,5})?(/[A-Za-z0-9._~/-]*)?", u): return ""   # só a própria máquina (o tradutor) fica sem https
    if not re.fullmatch(r"https://[A-Za-z0-9.-]+\.[A-Za-z]{2,}(:\d{1,5})?(/[A-Za-z0-9._~/-]*)?", u):
        return "o endereço precisa começar com https:// (só o tradutor da própria máquina, http://127.0.0.1, pode ser sem https)"
    return "tire o /v1/messages do fim: o LEON acrescenta sozinho" if re.search(r"/v1/messages/?$", u) else ""

def confere_bloco(b):
    e = []
    pid = b.get("id") if isinstance(b.get("id"), str) else ""
    if not ID.fullmatch(pid): e.append("o id precisa ter só letras minúsculas, números e hífen, até 24, começando por letra ou número")
    elif pid in RESERVADOS: e.append("o id '%s' é um comando do LEON; escolha outro" % pid)
    if not str(b.get("nome") or "").strip() or len(str(b.get("nome"))) > 60: e.append("falta o nome (até 60 letras)")
    if url_ok(b.get("url")): e.append(url_ok(b.get("url")))
    k = str(b.get("chave") or "")
    if not MOTOR_NOME.fullmatch(k):
        e.append("o nome da chave precisa ser MOTOR_ seguido de letras maiúsculas, números ou _ (ex.: MOTOR_<SEU_ID>_API_KEY)")
    mod = b.get("modelo")
    if not isinstance(mod, str) or not mod.strip(): e.append("falta o nome do modelo")
    elif not MODELO.fullmatch(mod): e.append("o nome do modelo tem caractere que não pode (só letras, números e . : / ~ [ ] - _, até 80)")
    return e

def confere_final(lista, b):   # o LEON leu o arquivo e achou o id novo UMA vez, ligado, com o endereço, a chave e o modelo do bloco novo
    if lista is None: raise ValueError("o validador do LEON recusou o arquivo ou não rodou")
    alvos = [p for p in lista if p.get("id") == b["id"]]
    if len(alvos) != 1 or not alvos[0].get("ativo") or [alvos[0].get(k) for k in ("url", "chave", "modelo")] != [b["url"].rstrip("/"), b["chave"], b["modelo"]]:
        raise ValueError("o LEON não leria o provedor novo como cadastrado")

def diz(*l): print(*l, flush=True)
def sai(msg, cod=2): diz(msg); sys.exit(cod)

def escreve_tudo(fd, dados):
    o = 0
    while o < len(dados):
        n = os.write(fd, dados[o:])
        if n <= 0: raise OSError("escrita sem progresso (disco cheio?)")
        o += n

def le_tudo(fd):
    partes = [os.pread(fd, 1 << 20, 0)]
    while len(partes[-1]) == 1 << 20: partes.append(os.pread(fd, 1 << 20, sum(map(len, partes))))
    return b"".join(partes)

@contextlib.contextmanager
def trava(alvo):
    """Fechadura (flock) num arquivo .lock na mesma pasta: dois scripts nunca alteram o mesmo arquivo juntos."""
    fd = os.open(alvo + ".lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        if os.geteuid() == 0: sp = os.stat(os.path.dirname(alvo) or "."); os.fchown(fd, sp.st_uid, sp.st_gid)
        try: fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: sai("Outra alteração está em andamento agora neste arquivo. Espere um minuto e rode de novo.", 3)
        yield
    finally: os.close(fd)

def le_env_texto(txt):
    """O mesmo leitor do config.cjs do LEON: a última linha ativa vale, aspas saem, comentário no fim sai."""
    out = {}
    for linha in txt.split("\n"):
        if re.match(r"^\s*#", linha): continue
        m = re.match(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*(.*?)\s*$", linha)
        if not m: continue
        v = re.sub(r"\s+#.*$", "", m.group(2)).strip()
        if len(v) > 1 and v[0] in "\"'" and v.endswith(v[0]): v = v[1:-1]
        if not re.search(r"[\r\n\0]", v): out[m.group(1)] = v
    return out

def dono_nome(uid): return next((u.pw_name for u in pwd.getpwall() if u.pw_uid == uid), str(uid))

def abre_env(path, escrita=False):
    """Abre o .env sem seguir atalho e confere o que o LEON exige. Devolve (fd, fstat)."""
    try:
        fd = os.open(path, (os.O_RDWR | os.O_APPEND if escrita else os.O_RDONLY) | os.O_NOFOLLOW | os.O_CLOEXEC)
    except FileNotFoundError: sai("Não achei o .env em %s. Use --env com o caminho certo." % mostra(path))
    except PermissionError: sai("Sem permissão para abrir o .env. Rode com sudo, ou como o usuário dono do LEON.")
    except OSError as e: sai("O .env (%s) %s. Peça ao suporte para conferir." % (mostra(path), "é um atalho (link), e o LEON recusa" if e.errno == 40 else "não abriu (%s)" % (os.strerror(e.errno) if e.errno else "erro de disco")))
    st = os.fstat(fd)
    probs = [m for c, m in ((not stat.S_ISREG(st.st_mode), "não é arquivo comum"), (st.st_nlink != 1, "tem mais de um nome (nlink %d), o LEON exige 1" % st.st_nlink),
                            (stat.S_IMODE(st.st_mode) != 0o600, "modo %o, o LEON exige 600" % stat.S_IMODE(st.st_mode))) if c]
    if probs:
        os.close(fd); sai("O .env (%s) está fora do que o LEON aceita: %s. Peça ao suporte para conferir antes de seguir." % (mostra(path), "; ".join(probs)))
    return fd, st

def le_env(path):
    fd, _ = abre_env(path)
    try: return le_env_texto(le_tudo(fd).decode("utf-8", "replace"))
    finally: os.close(fd)

def descobre(a):
    env, origem = (a.env, "--env") if a.env else (PADRAO_ENV, "padrão da casa")
    if not os.path.exists(env): sai("Não achei o .env do LEON em %s. Peça ao suporte o caminho e rode de novo com --env <caminho>." % mostra(env))
    m, cad, ocad = le_env(env), a.cadastro, "--cadastro"
    do_env = (m.get("LEON_MOTORES_API"), "LEON_MOTORES_API") if m.get("LEON_MOTORES_API") else (m.get("LEON_DATA_DIR") and os.path.join(m["LEON_DATA_DIR"], "motores-api.json"), "LEON_DATA_DIR")
    if not cad and do_env[0]:   # caminho vindo do .env: absoluto, .json, em pasta confiável; NUNCA impresso
        global OCULTO; cad, ocad = os.path.normpath(do_env[0]), "%s no .env" % do_env[1]; OCULTO = os.path.normpath(os.path.abspath(cad))
        try: ruim = not os.path.isabs(do_env[0]) or not cad.endswith(".json") or seguro(os.path.dirname(cad), os.stat(env).st_uid)
        except OSError: ruim = True
        if ruim: sai("O caminho do cadastro indicado no .env (%s) não é aceito: precisa ser absoluto, terminar em .json e ficar numa pasta do dono do LEON sem escrita de grupo nem de outros. Peça ao suporte para conferir." % do_env[1])
    elif not cad and env == PADRAO_ENV: cad, ocad = PADRAO_CADASTRO, "padrão da casa"
    elif not cad: cad, ocad = os.path.join(pwd.getpwuid(os.stat(env).st_uid).pw_dir, ".leon", "motores-api.json"), "pasta .leon do dono do .env"
    return env, origem, cad, ocad

OCULTO, CRIADO = "", []   # o cadastro que veio do .env (e o .lock e a cópia .antes- dele) nunca vai à tela
def mostra(p):   # LISTA DE PERMISSÃO por caminho EXATO (os padrões da casa e o node do sistema); qualquer outro vira o rótulo fixo
    q, L = os.path.normpath(os.path.abspath(str(p))), os.path.join(os.path.dirname(PADRAO_ENV), "leon2", "lib")
    fixos = {PADRAO_ENV, PADRAO_CADASTRO, PADRAO_CADASTRO + ".lock", L, os.path.dirname(L), "/usr/bin/node", "/usr/local/bin/node", "/usr/bin", "/usr/local/bin", "/usr", "/usr/local", os.path.join(L, "motores-api.cjs"),
             os.path.join(L, "log.cjs")} | {x for c in (PADRAO_ENV, PADRAO_CADASTRO) for x in (os.path.dirname(c), "/home/cloud", "/home", "/")}
    ok = not (OCULTO and q.startswith(OCULTO)) and (q in fixos or q in CRIADO)   # CRIADO: só a cópia .antes- que ESTA execução acabou de criar
    return q if ok else "(caminho que você indicou)"

def vis_nome(nome, onde, a):   # o nome MOTOR_ derivado de um --id digitado não vai à tela (o do cadastro e o do catálogo vão)
    return nome if onde == "cadastro" or not a.id or item_catalogo(a.id) else "(o nome derivado do id)"

def catalogo(): return json.load(open(CATALOGO, encoding="utf-8"))["provedores"]
def item_catalogo(escolha): return next((p for p in catalogo() if p["escolha"] == escolha), None)

def le_cadastro(cad, env):
    """Devolve (bytes, doc, fstat, lista do LEON). Sem cadastro: (None, {'provedores': []}, None, [])."""
    try: fd = os.open(cad, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    except FileNotFoundError: return None, {"provedores": []}, None, []
    except PermissionError: sai("Sem permissão para ler o cadastro. Rode com sudo, ou como o usuário dono do LEON.")
    except OSError as e: sai("O cadastro %s %s. Peça ao suporte para conferir." % (mostra(cad), "é um atalho (link)" if e.errno == 40 else "não abriu (%s)" % (os.strerror(e.errno) if e.errno else "erro de disco")))
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
            sai("O cadastro %s não é um arquivo comum com um nome só (nlink %d). Peça ao suporte para conferir." % (mostra(cad), st.st_nlink))
        cru = le_tudo(fd)
    finally: os.close(fd)
    try:
        doc = json_estrito(cru)
        if not isinstance(doc, dict) or not isinstance(doc.get("provedores"), list): raise ValueError("falta a lista provedores")
        json.dumps(doc, ensure_ascii=False).encode("utf-8")   # texto com caractere inválido (ex.: \\ud800) para aqui
    except (ValueError, UnicodeDecodeError, RecursionError) as e:
        sai("O cadastro tem um valor que o LEON não aceita. Não mexo nele: peça ao suporte para consertar primeiro.")
    lista = leon_le(cru, env)
    if lista is None: sai("O LEON já recusa o cadastro atual (ou a conferência dele não rodou). Não mexo nele: peça ao suporte para consertar primeiro.")
    return cru, doc, st, lista

def com_id(b, novo_id): b.update(id=novo_id, chave="MOTOR_%s_API_KEY" % novo_id.upper().replace("-", "_")); return b

def bloco_do(a, lista):
    """O provedor como o LEON o lê no cadastro; se ainda não estiver lá, o bloco do catálogo."""
    pid = a.id or a.provedor
    p = next((p for p in lista if p.get("id") == pid), None)
    if p: return p, "cadastro"
    it = item_catalogo(a.provedor)
    if it and "bloco" in it: return (com_id(dict(it["bloco"]), a.id) if a.id else dict(it["bloco"])), "catálogo"
    return None, ""

# ---- ações ----
def monta_bloco(a):
    if a.provedor == "outro-openai": sai("Esse provedor só fala o formato OpenAI e precisa do tradutor, que o suporte liga. Depois, ele entra pela opção outro.")
    if a.provedor == "outro":
        if not (a.id and a.nome and a.url and a.modelo): sai("Para outro provedor preciso de --id, --nome, --url e --modelo.")
        b = com_id({"nome": a.nome, "atalhos": [], "url": a.url.rstrip("/"), "modelo": a.modelo, "modelos": [a.modelo], "esforco": False, "timeout_ms": 600000}, a.id)
    else:
        it = item_catalogo(a.provedor)
        if not it or "bloco" not in it: sai("Não conheço esse provedor. Veja a lista em catalogo.json, ou use --provedor outro.")
        b = json.loads(json.dumps(it["bloco"]))
        if a.id: com_id(b, a.id)["atalhos"] = []
        if a.modelo is not None:
            if a.modelo and a.modelo not in b["modelos"]:
                sai("O modelo escolhido não está na lista deste provedor em catalogo.json. Para um modelo fora da lista, use --provedor outro.")
            b["modelo"] = a.modelo
    return b

class Publicado(OSError): pass
def grava_atomico(cad, dados, modo, uid, gid):
    """Temporário exclusivo na mesma pasta, escrita completa, dono e modo, fsync, troca de nome. Falha antes da troca não mexe no cadastro."""
    d = os.path.dirname(cad) or "."
    fd, tmp = tempfile.mkstemp(prefix=".motores-api.", suffix=".tmp", dir=d)
    try:
        escreve_tudo(fd, dados); os.fchmod(fd, modo)
        if (os.fstat(fd).st_uid, os.fstat(fd).st_gid) != (uid, gid): os.fchown(fd, uid, gid)
        os.fsync(fd); os.close(fd); fd = -1
        os.rename(tmp, cad); tmp = None
        try:
            dfd = os.open(d, os.O_RDONLY)
            try: os.fsync(dfd)
            finally: os.close(dfd)
        except OSError as e: raise Publicado("o arquivo novo já está no lugar, mas a pasta não confirmou a gravação (%s)" % (os.strerror(e.errno) if e.errno else "erro de disco"))
    finally:
        if fd >= 0: os.close(fd)
        if tmp:
            with contextlib.suppress(FileNotFoundError): os.unlink(tmp)   # já trocado: quem chamou confere pelo conteúdo

@contextlib.contextmanager
def sem_sinais():   # a recuperação não pode ser interrompida: Ctrl-C e os outros sinais esperam até ela terminar
    sinais = set(SINAIS) | {signal.SIGINT}; signal.pthread_sigmask(signal.SIG_BLOCK, sinais)
    try: yield
    finally:
        with contextlib.suppress(OSError): signal.pthread_sigmask(signal.SIG_UNBLOCK, sinais)   # sinal pendente que já virou "ignorar"

SINAIS = (signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT, signal.SIGTSTP, signal.SIGUSR1, signal.SIGUSR2, signal.SIGALRM)

def para_com_sinal():   # todo sinal capturável vira saída controlada: os finally (eco, volta, limpeza) sempre rodam
    def sair(n, f):   # o primeiro sinal decide a saída; os seguintes são ignorados (nada de exceção na hora de fechar)
        [signal.signal(x, lambda n, f: None) for x in SINAIS]; sys.exit(128 + n)   # função vazia, não SIG_IGN: sem "race condition"
    for sig in SINAIS: signal.signal(sig, sair)

def ac_adiciona(a):
    env, _, cad, ocad = descobre(a)
    b = monta_bloco(a)
    with (trava(cad) if a.aplicar else contextlib.nullcontext()):
        cru, doc, st, lista = le_cadastro(cad, env)
        erros = confere_bloco(b)
        if b.get("id") in [p["id"] for p in lista]:
            erros.append("já existe um provedor com esse id no cadastro; para outra conta do mesmo provedor use --id com outro nome")
        if b.get("chave") in [p.get("chave") for p in lista]: erros.append("esse nome de chave já é usado por outro provedor do cadastro")
        if erros:
            diz("Não dá para cadastrar assim:"); [diz("  - " + e) for e in erros]; return 2
        tomados = {x for p in lista for x in p["atalhos"] + [p["id"]]}
        tira = [x for x in b.get("atalhos", []) if x in tomados]
        if tira:
            b["atalhos"] = [x for x in b["atalhos"] if x not in tomados]
            diz("Aviso: %d atalho(s) deste provedor já são de outro e ficaram de fora." % len(tira))
        novo = json.loads(json.dumps(doc)); novo["provedores"].append(b)
        texto = (json.dumps(novo, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
        try: confere_final(leon_le(texto, env), b)
        except ValueError: diz("Não dá para cadastrar: o LEON não aceitaria este provedor como está."); return 2
        diz("Vai entrar um provedor novo no cadastro, sem chave nenhuma (a chave vai depois no .env, com o nome %s)." % vis_nome(b["chave"], "catálogo", a))
        diz("Cadastro: %s (%s)" % (mostra(cad), ocad))
        if a.provedor == "outro": diz("ATENÇÃO: a sua chave vai ser enviada para o host %s. Confira na documentação OFICIAL do provedor se esse endereço é mesmo dele." % urllib.parse.urlsplit(b["url"]).hostname)
        if not a.aplicar:
            diz("\nSIMULADO: nada foi escrito. Para valer, rode de novo com --aplicar."); return 0
        pasta = os.path.dirname(cad) or "."
        if not os.path.isdir(pasta): sai("A pasta %s não existe. O LEON está instalado nesta máquina? Peça ao suporte." % mostra(pasta))
        if st: modo, uid, gid = stat.S_IMODE(st.st_mode), st.st_uid, st.st_gid
        else: sp = os.stat(pasta); modo, uid, gid = 0o600, sp.st_uid, sp.st_gid
        if os.geteuid() not in (0, uid):
            sai("O cadastro é do usuário %s e você está rodando como %s: eu não conseguiria manter o dono. Rode como %s ou com sudo." % (dono_nome(uid), dono_nome(os.geteuid()), dono_nome(uid)))
        backup = None
        if cru is not None:
            hora, n = time.strftime("%Y%m%d-%H%M%S"), 1
            backup = "%s.antes-%s" % (cad, hora)
            while os.path.lexists(backup): n += 1; backup = "%s.antes-%s-%d" % (cad, hora, n)
            try: grava_atomico(backup, cru, modo, uid, gid); CRIADO.extend([os.path.normpath(os.path.abspath(backup))] if os.path.normpath(os.path.abspath(cad)) == PADRAO_CADASTRO else [])   # só se o cadastro É o padrão (igualdade exata)
            except OSError as e: sai("Não consegui guardar a cópia de antes (%s). Nada foi trocado." % (os.strerror(e.errno) if e.errno else "erro de disco"), 1)
        motivo = ""
        try:   # janela da troca: qualquer saída daqui (erro, sinal, Ctrl-C, sai()) passa pela conferência e pela volta
            grava_atomico(cad, texto, modo, uid, gid)
            fd = os.open(cad, os.O_RDONLY | os.O_NOFOLLOW)
            try: st2, lido = os.fstat(fd), le_tudo(fd)
            finally: os.close(fd)
            if (st2.st_uid, st2.st_gid, stat.S_IMODE(st2.st_mode), st2.st_nlink) != (uid, gid, modo, 1): motivo = "dono ou modo não ficaram iguais"
            else: confere_final(leon_le(lido, env), b)
        except Publicado as e: motivo = str(e)
        except (OSError, ValueError) as e: motivo = os.strerror(e.errno) if isinstance(e, OSError) and e.errno else "a conferência final recusou o cadastro"
        except SystemExit: motivo = "interrompido, ou a conferência do LEON não rodou"
        except BaseException: motivo = "interrompido no meio"
        if motivo:
            with sem_sinais():
                try:
                    with open(cad, "rb") as f: atual = f.read()
                except FileNotFoundError: atual = None
                except OSError: atual = b""
                if atual == cru:
                    diz("Não deu certo (%s). Conferi: o cadastro de antes continua no lugar." % motivo); return 1
                try:
                    if cru is not None: grava_atomico(cad, cru, modo, uid, gid); diz("Não terminou bem (%s). Devolvi o cadastro de antes; confira com /motor no Telegram." % motivo)
                    else: os.unlink(cad); diz("Não terminou bem (%s). Tirei o cadastro novo; confira com /motor no Telegram." % motivo)
                except Publicado: diz("Não terminou bem (%s). Devolvi o cadastro de antes, mas o disco não confirmou a gravação; confira com /motor." % motivo)
                except OSError: diz("Não terminou bem (%s) e NÃO consegui devolver o de antes. Peça ao suporte: a cópia está em %s." % (motivo, mostra(backup)))
            return 1
    diz("\nPronto: o provedor novo entrou no cadastro, conferido pelo validador do próprio LEON.")
    if backup: diz("O cadastro de antes ficou guardado em %s." % mostra(backup))
    diz("Próximo passo: guardar a chave. Rode %s chave --aplicar, com os mesmos --provedor, --id, --env e --cadastro de agora." % COMANDO)
    return 0

def valida_chave(valor):
    if "\n" in valor or "\r" in valor: return "tem mais de uma linha. Deixe só a chave, numa linha"
    if not re.fullmatch(r"[A-Za-z0-9._~+/=:-]{8,512}", valor): return "não parece uma chave (tem espaço, aspas, ou é curta demais). Copie de novo do painel do provedor"
    return ""

@contextlib.contextmanager
def terminal_sem_eco():
    """PRIMEIRO ato da ação chave: desliga o eco (o mesmo que read -rs) antes de qualquer pedido. Ele volta no fim, no erro,
    em qualquer sinal capturável e na saída do programa (atexit); se a volta falhar, roda stty sane e avisa para digitar reset."""
    try: fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY)
    except OSError: sai("Não achei um terminal para pedir a chave escondida. Rode este comando no terminal do servidor, ou peça ajuda ao suporte.")
    velho = termios.tcgetattr(fd); novo = termios.tcgetattr(fd); novo[3] &= ~(termios.ECHO | termios.ECHOE | termios.ECHOK | termios.ECHONL)
    feito = []
    def volta():   # só marca feita DEPOIS de devolver o eco, e com os sinais bloqueados: um segundo sinal não a deixa pela metade
        with sem_sinais():
            if feito: return
            try: termios.tcsetattr(fd, termios.TCSAFLUSH, velho)
            except termios.error:
                subprocess.run(["stty", "sane"], stdin=fd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                diz("Confira o terminal: se o que você digita não aparecer, digite reset e aperte Enter.")
            feito.append(1); os.write(fd, b"\n"); os.close(fd)
    atexit.register(volta)
    try: termios.tcsetattr(fd, termios.TCSAFLUSH, novo); yield fd
    finally: volta()

def le_oculto(fd, texto):
    """Pede e lê a chave com o eco já desligado: nada aparece na tela, nada vai para argumento nem histórico."""
    termios.tcflush(fd, termios.TCIFLUSH); os.write(fd, texto.encode()); b = b""   # o que foi colado antes do pedido é jogado fora
    while not b.endswith(b"\n") and len(b) < 8192 and (c := os.read(fd, 1024)): b += c
    return b.decode("utf-8", "replace").replace("\x1b[200~", "").replace("\x1b[201~", "").strip()

def desfaz(fd, tam_antes, linha):
    """Só corta o que ESTE script acrescentou: o tamanho e o fim do arquivo têm de bater com a linha nossa."""
    tam = os.fstat(fd).st_size
    if tam == tam_antes: return True
    k = tam - tam_antes
    if 0 < k <= len(linha) and os.pread(fd, k, tam_antes) == linha[:k]:
        os.ftruncate(fd, tam_antes); os.fsync(fd); return True
    return False

def ac_chave(a):
    with (terminal_sem_eco() if a.aplicar else contextlib.nullcontext()) as tty:   # eco desligado antes de tudo
        return chave_no_env(a, tty)

def chave_no_env(a, tty):
    env, _, cad, _ = descobre(a)
    b, onde = bloco_do(a, le_cadastro(cad, env)[3])
    if not b: sai("Não achei esse provedor nem no cadastro nem no catálogo.")
    nome = str(b.get("chave") or ""); vn = vis_nome(nome, onde, a)
    if not MOTOR_NOME.fullmatch(nome): sai("O nome da chave deste provedor não é MOTOR_*. Cadastre de novo pelo adiciona.")
    if not a.aplicar:
        diz("SIMULADO: pediria a chave escondida (ela não aparece na tela) e acrescentaria a linha %s=<chave> no fim de %s, sem recriar o arquivo. Para valer, use --aplicar." % (vn, mostra(env)))
        return 0
    falhou, desfeito = "", True
    with trava(env):   # a fechadura vem ANTES de pedir a chave
        if le_env(env).get(nome) and not a.trocar_chave:
            sai("O .env já tem um valor para %s. Para trocar a chave, rode de novo com --trocar-chave (a linha nova vale, a antiga fica no arquivo)." % vn)
        valor = le_oculto(tty, "Cole a chave e aperte Enter (ela NÃO aparece na tela, é normal): ")
        erro = valida_chave(valor)
        if erro: sai("A chave %s. Nada foi gravado." % erro)
        diz("Chave recebida: %d caracteres (o valor não aparece)." % len(valor))
        fd, st0 = abre_env(env, escrita=True)
        try:
            antes = le_tudo(fd)
            linha = (b"" if not antes or antes.endswith(b"\n") else b"\n") + ("%s=%s\n" % (nome, valor)).encode()
            try:
                escreve_tudo(fd, linha); os.fsync(fd)
                st1, depois = os.fstat(fd), le_tudo(fd)
                if (st1.st_uid, st1.st_gid, st1.st_mode, st1.st_nlink, st1.st_ino) != (st0.st_uid, st0.st_gid, st0.st_mode, st0.st_nlink, st0.st_ino) or os.lstat(env).st_ino != st0.st_ino:
                    falhou = "o .env mudou de dono, modo ou identidade"
                elif depois != antes + linha: falhou = "o arquivo não ficou como esperado (outro programa escreveu junto?)"
                elif le_env_texto(depois.decode("utf-8", "replace")).get(nome) != valor: falhou = "o LEON não leria a chave"
            except (OSError, KeyboardInterrupt, SystemExit) as e:
                falhou = "erro ao gravar: %s" % (os.strerror(e.errno) if e.errno else "erro de disco") if isinstance(e, OSError) else "interrompido no meio"
            if falhou:
                with sem_sinais():   # a volta não pode ser interrompida por um segundo sinal
                    try: desfeito = desfaz(fd, len(antes), linha)
                    except OSError: desfeito = None
        finally: os.close(fd)
    if falhou:
        if desfeito: sai("Não deu certo (%s). Conferi e desfiz o acréscimo; o .env ficou como antes." % falhou, 1)
        if desfeito is None: sai("Não deu certo (%s) e a recuperação FALHOU: confira o .env à mão (a última linha, %s, pode estar pela metade). Peça ajuda ao suporte." % (falhou, vn), 1)
        sai("Não deu certo (%s) e o fim do .env não é só o que eu acrescentei, então NÃO apaguei nada. Peça ao suporte para conferir as últimas linhas do .env." % falhou, 1)
    diz("Pronto: a chave %s entrou no .env. Dono, modo 600 e identidade do arquivo iguais aos de antes; as outras linhas intactas." % vn)
    diz("Próximo passo: testar a chave. Rode %s testa, com os mesmos --provedor, --id, --env e --cadastro de agora." % COMANDO)
    return 0

class SemRedirecionar(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *x, **k):
        return None   # nunca segue: a chave nunca vai para outro endereço

# Lista FECHADA de tipos de erro conhecidos: só estes rótulos aparecem na tela. Nenhum texto vindo do provedor é impresso.
ROTULOS = {"invalid_api_key": "chave", "authentication_error": "chave", "permission_error": "chave", "insufficient_quota": "saldo",
           "billing_error": "saldo", "1113": "saldo", "rate_limit_error": "limite", "rate_limit_exceeded": "limite",
           "model_not_found": "modelo", "not_found_error": "modelo", "overloaded_error": "fora", "api_error": "fora"}

def destino(u):
    x = urllib.parse.urlsplit(u.rstrip("/"))
    return "%s://%s:%d%s" % (x.scheme, x.hostname, x.port or (443 if x.scheme == "https" else 80), x.path.rstrip("/"))

MSG = {"ok": "Funcionou: a chave e o modelo estão certos.", "chave": "A chave foi recusada. Ela pode ter sido copiada pela metade ou apagada no painel. Gere uma nova e guarde de novo (ação chave).", "saldo": "A conta no provedor está sem saldo. Ponha crédito no painel do provedor e teste de novo.",
       "limite": "O provedor disse que passou do limite ou que acabou o saldo. Confira o crédito no painel; se tiver saldo, espere alguns minutos e teste de novo.", "modelo": "O provedor não conhece esse modelo (ou o endereço está errado). Confira o nome exato do modelo no painel.", "redir": "O provedor redirecionou para outro endereço. Por segurança não segui (a chave iria junto). Confira a URL na documentação oficial do provedor.",
       "fora": "O provedor está com problema agora. Tente de novo mais tarde.", "vazio": "O provedor respondeu, mas sem texto (resposta vazia ou ilegível). Confira o modelo e tente de novo.", "pensou": "O provedor respondeu, mas o modelo só pensou e não escreveu; a chave está boa.",
       "outro": "Erro do provedor. Confira modelo e endereço, ou peça ajuda ao suporte.", "tempo": "O provedor não respondeu a tempo. Pode ser lentidão do lado dele: tente de novo em alguns minutos.", "recusado": "Ninguém atendeu nesse endereço. Se for um provedor via tradutor, o tradutor está desligado: peça ao suporte para ligar.",
       "rede": "Não consegui falar com o endereço do provedor. Confira o endereço ou a internet da casa.", "incompleta": "O provedor não terminou a resposta a tempo. Tente de novo em alguns minutos.", "malformada": "Resposta do provedor malformada. Confira o endereço; se repetir, peça ajuda ao suporte."}

def classe(status, rotulo):
    if status and 300 <= status < 400: return "redir"
    if status and status != 200 and rotulo: return ROTULOS[rotulo]
    return {200: "ok", 401: "chave", 403: "chave", 402: "saldo", 429: "limite", 404: "modelo"}.get(status, "fora" if status and status >= 500 else "outro")

def ac_testa(a):
    env, _, cad, _ = descobre(a)
    b, onde = bloco_do(a, le_cadastro(cad, env)[3])
    if not b: sai("Não achei esse provedor nem no cadastro nem no catálogo.")
    modelo, nome = a.modelo or b.get("modelo"), str(b.get("chave") or ""); vn = vis_nome(nome, onde, a)
    if not modelo or not MODELO.fullmatch(modelo) or url_ok(b.get("url")) or not MOTOR_NOME.fullmatch(nome):
        sai("Este provedor está fora do padrão (modelo, endereço https ou chave MOTOR_*). Cadastre de novo pelo adiciona.")
    chave = le_env(env).get(nome, "")
    if not chave: sai("A chave %s ainda não está no .env. Faça a ação chave primeiro." % vn)
    if valida_chave(chave): sai("A chave %s no .env tem caractere inválido (acento, espaço ou caractere de controle). Guarde de novo pela ação chave, com --trocar-chave." % vn)
    alvo, d = b["url"].rstrip("/") + "/v1/messages", destino(b["url"])
    v = d[:len(d) - len(urllib.parse.urlsplit(d).path)]   # na tela só esquema, host e porta; o caminho é conferido por dentro
    diz("Teste do provedor escolhido (bloco do %s), modelo %s.\n>>> A CHAVE SERÁ ENVIADA PARA: %s <<<" % (onde, "escolhido em --modelo" if a.modelo else "padrão", v))
    if not a.aplicar:
        diz("SIMULADO: faria UMA chamada mínima (costuma custar centavos; confira o seu painel). Para valer, use --aplicar."); return 0
    cat = {destino(p["bloco"]["url"]) for p in catalogo() if "bloco" in p}
    if d not in cat and a.confirmo_destino != v:
        sai("%s. Confira na documentação OFICIAL do provedor; a chave vai para quem estiver nesse endereço. Se estiver certo, rode de novo com --confirmo-destino %s" % (
            "O caminho do endereço difere do catálogo" if any(c.startswith(v + "/") or c == v for c in cat) else "Esse endereço (esquema, host e porta) não é de um provedor do catálogo", v))
    corpo = json.dumps({"model": modelo, "max_tokens": 256, "messages": [{"role": "user", "content": "Responda só: ok"}]}).encode()
    req = urllib.request.Request(alvo, data=corpo, method="POST", headers={
        "content-type": "application/json", "anthropic-version": "2023-06-01", "x-api-key": chave, "authorization": "Bearer " + chave})
    status, bruto, erro = None, b"", ""
    t0 = time.time()
    def corpo(r):   # leitura protegida: corpo malformado ou incompleto vira mensagem fixa, NUNCA o texto da exceção
        try: b = r.read(65536); return None if getattr(r, "length", None) else b
        except (socket.timeout, TimeoutError): return False
        except Exception: return None
    def prazo(n, f): raise TimeoutError()
    signal.signal(signal.SIGALRM, prazo); signal.alarm(max(1, a.timeout))   # prazo TOTAL do pedido, não por pedaço lido
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({}), SemRedirecionar).open(req, timeout=a.timeout) as r:
            status, bruto = r.status, corpo(r)
    except urllib.error.HTTPError as e:
        status, bruto = e.code, corpo(e) if e.fp else b""
    except Exception as e:   # tempo esgotado, porta fechada (tradutor desligado) ou rede
        rz = getattr(e, "reason", e)
        erro = "tempo" if isinstance(rz, (socket.timeout, TimeoutError)) or "timed out" in str(rz) else "recusado" if isinstance(rz, ConnectionRefusedError) else "rede"
    signal.alarm(0); para_com_sinal(); dt = time.time() - t0
    if bruto is None or bruto is False: erro, bruto = "malformada" if bruto is None else "incompleta", b""
    try: j = json.loads(bruto.decode("utf-8", "replace"))
    except ValueError: j = None
    except RecursionError: j, erro = None, erro or "malformada"   # JSON fundo demais
    e = (j.get("error") if isinstance(j, dict) and isinstance(j.get("error"), dict) else j) if isinstance(j, dict) else {}
    rotulo = next((str(e.get(c)) for c in ("code", "type") if str(e.get(c)) in ROTULOS), "")
    if not rotulo and status and status != 200 and re.search(rb"\b1113\b", bruto): rotulo = "1113"
    k = erro or classe(status, rotulo)
    if k == "ok":
        partes = j.get("content") if isinstance(j, dict) and isinstance(j.get("content"), list) else []
        if not any(isinstance(x, dict) and x.get("type") == "text" and x.get("text") for x in partes):
            k = "pensou" if any(isinstance(x, dict) and x.get("type") in ("thinking", "redacted_thinking") for x in partes) or (isinstance(j, dict) and j.get("stop_reason") == "max_tokens") else "vazio"
    diz("Resultado: " + MSG[k])
    diz("(código HTTP %s%s, %.1f s)" % (status or "sem resposta", ", tipo de erro conhecido: %s" % rotulo if rotulo and k not in ("ok", "pensou", "vazio") else "", dt))
    return 0 if k in ("ok", "pensou") else 1

para_com_sinal()   # TERM, HUP, QUIT, TSTP, USR1, USR2 e ALRM viram saída controlada em todas as ações
sys.excepthook = lambda *x: print("Erro inesperado. Confira o cadastro e o .env antes de seguir; se repetir, peça ajuda ao suporte.", file=sys.stderr)
class Args(argparse.ArgumentParser):   # erro de argumento: frase fixa, sem repetir o valor digitado (pode ser uma chave colada por engano)
    def error(self, m): sai("Argumento inválido; use --help.")
pa = Args(prog="adiciona-motor.sh")
pa.add_argument("acao", choices=["adiciona", "chave", "testa"])
for o in ("--env", "--cadastro", "--provedor", "--modelo", "--id", "--nome", "--url", "--confirmo-destino"):
    pa.add_argument(o)
pa.add_argument("--timeout", type=int, default=60)
for o in ("--aplicar", "--trocar-chave"):
    pa.add_argument(o, action="store_true")
args = pa.parse_args(sys.argv[2:])
if any(x is not None and not ID.fullmatch(x) for x in (args.provedor, args.id)) or any(".." in x.split("/") for x in (args.env, args.cadastro) if x): sai("O --provedor e o --id só aceitam letras minúsculas, números e hífen, até 24; --env e --cadastro não aceitam '..'.")
if args.acao in ("adiciona", "chave", "testa") and not args.provedor: sai("Diga qual provedor com --provedor (a lista está em catalogo.json, na pasta desta skill).")
try:
    sys.exit({"adiciona": ac_adiciona, "chave": ac_chave, "testa": ac_testa}[args.acao](args))
except PermissionError as e:
    sai("Sem permissão para abrir um arquivo. Rode com sudo, ou como o usuário dono do LEON.")
except OSError as e:
    sai("Erro de arquivo ou disco (%s). Confira o cadastro (/motor no Telegram) e o .env antes de seguir; se repetir, peça ajuda ao suporte." % (os.strerror(e.errno) if e.errno else type(e).__name__), 1)
except Exception:   # nunca o texto da exceção (pode trazer pedaço da chave)
    sai("Erro inesperado. Confira o cadastro e o .env antes de seguir; se repetir, peça ajuda ao suporte.", 1)
except KeyboardInterrupt:
    sai("\nParei a pedido. Confira o cadastro (/motor no Telegram) antes de seguir.", 130)
PY
